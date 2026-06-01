# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Connector registry metrics from the analytics JSONL export."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Protocol, cast

import gcsfs

from airbyte_ops_mcp.registry._gcs_helpers import get_gcs_credentials_token

logger = logging.getLogger(__name__)

CONNECTOR_METRICS_BUCKET = "ab-analytics-connector-metrics"
CONNECTOR_METRICS_PREFIX = "data/connector_quality_metrics"


class MetricsFileSystem(Protocol):
    """Filesystem operations needed for connector metrics."""

    def glob(self, pattern: str) -> list[str]:
        """Return paths matching the glob pattern."""
        ...

    def open(self, path: str, mode: str = "r") -> Any:
        """Open a metrics export for reading."""
        ...


@dataclass(frozen=True)
class ConnectorPlatformMetrics:
    """Metrics for one connector on one Airbyte platform."""

    sync_success_rate: str | None = None
    usage: str | None = None

    def to_registry_dict(self) -> dict[str, str | None]:
        """Return the registry JSON shape for this platform."""
        return {
            "sync_success_rate": self.sync_success_rate,
            "usage": self.usage,
        }


@dataclass(frozen=True)
class ConnectorMetrics:
    """Metrics for one connector across Airbyte platforms."""

    platforms: dict[str, ConnectorPlatformMetrics] = field(default_factory=dict)

    def to_registry_dict(self) -> dict[str, dict[str, str | None]]:
        """Return the `generated.metrics` registry JSON shape."""
        return {
            platform: metrics.to_registry_dict()
            for platform, metrics in sorted(self.platforms.items())
        }


@dataclass(frozen=True)
class ConnectorMetricsBundle:
    """Latest connector metrics export parsed for registry injection."""

    blob_path: str | None
    metrics_by_definition_id: dict[str, ConnectorMetrics] = field(default_factory=dict)

    @property
    def connector_count(self) -> int:
        """Return the number of connector definition IDs with metrics."""
        return len(self.metrics_by_definition_id)

    def registry_metrics_for_definition_id(
        self,
        definition_id: str,
    ) -> dict[str, dict[str, str | None]]:
        """Return registry metrics for a connector definition ID."""
        connector_metrics = self.metrics_by_definition_id.get(definition_id)
        if connector_metrics is None:
            return {}
        return connector_metrics.to_registry_dict()


def decode_string_nulls(obj: dict[str, Any]) -> dict[str, Any]:
    """Convert string `null` values to `None`."""
    return {key: None if value == "null" else value for key, value in obj.items()}


def parse_connector_metrics_jsonl(
    jsonl_content: str,
    *,
    blob_path: str | None = None,
) -> ConnectorMetricsBundle:
    """Parse connector metrics JSONL into a metrics bundle."""
    platforms_by_definition_id: dict[str, dict[str, ConnectorPlatformMetrics]] = {}

    for line_number, line in enumerate(jsonl_content.splitlines(), start=1):
        if not line.strip():
            continue

        row = json.loads(line, object_hook=decode_string_nulls)
        airbyte_data = row.get("_airbyte_data")
        if not isinstance(airbyte_data, dict):
            logger.warning(
                "Skipping metrics row %d without _airbyte_data in %s",
                line_number,
                blob_path or "<inline>",
            )
            continue

        definition_id = airbyte_data.get("connector_definition_id")
        platform = airbyte_data.get("airbyte_platform")
        if not isinstance(definition_id, str) or not definition_id:
            logger.warning(
                "Skipping metrics row %d without connector_definition_id in %s",
                line_number,
                blob_path or "<inline>",
            )
            continue
        if not isinstance(platform, str) or not platform:
            logger.warning(
                "Skipping metrics row %d without airbyte_platform in %s",
                line_number,
                blob_path or "<inline>",
            )
            continue

        sync_success_rate = airbyte_data.get("sync_success_rate")
        usage = airbyte_data.get("usage")
        platforms_by_definition_id.setdefault(definition_id, {})[platform] = (
            ConnectorPlatformMetrics(
                sync_success_rate=(
                    sync_success_rate if isinstance(sync_success_rate, str) else None
                ),
                usage=usage if isinstance(usage, str) else None,
            )
        )

    return ConnectorMetricsBundle(
        blob_path=blob_path,
        metrics_by_definition_id={
            definition_id: ConnectorMetrics(platforms=platforms)
            for definition_id, platforms in platforms_by_definition_id.items()
        },
    )


def find_latest_connector_metrics_blob(
    fs: MetricsFileSystem,
    *,
    bucket: str = CONNECTOR_METRICS_BUCKET,
    prefix: str = CONNECTOR_METRICS_PREFIX,
) -> str | None:
    """Find the newest connector metrics JSONL blob by object name."""
    pattern = f"{bucket}/{prefix}/*.jsonl"
    matches = sorted(fs.glob(pattern), reverse=True)
    if not matches:
        return None
    return matches[0]


def read_latest_connector_metrics(
    *,
    fs: MetricsFileSystem | None = None,
    bucket: str = CONNECTOR_METRICS_BUCKET,
    prefix: str = CONNECTOR_METRICS_PREFIX,
) -> ConnectorMetricsBundle:
    """Read and parse the latest connector metrics JSONL export."""
    metrics_fs: MetricsFileSystem = fs or cast(
        MetricsFileSystem,
        gcsfs.GCSFileSystem(token=get_gcs_credentials_token()),
    )
    latest_blob_path = find_latest_connector_metrics_blob(
        metrics_fs,
        bucket=bucket,
        prefix=prefix,
    )
    if latest_blob_path is None:
        logger.warning(
            "No connector metrics JSONL files found at gs://%s/%s",
            bucket,
            prefix,
        )
        return ConnectorMetricsBundle(blob_path=None)

    with metrics_fs.open(latest_blob_path, "r") as handle:
        raw_content: bytes | str = handle.read()
    content = (
        raw_content.decode("utf-8") if isinstance(raw_content, bytes) else raw_content
    )

    return parse_connector_metrics_jsonl(content, blob_path=latest_blob_path)


def apply_metrics_to_registry_entries(
    entries: list[dict[str, Any]],
    metrics_bundle: ConnectorMetricsBundle,
) -> int:
    """Inject connector metrics into registry entries and return match count."""
    injected_count = 0
    for entry in entries:
        definition_id = entry.get("sourceDefinitionId") or entry.get(
            "destinationDefinitionId"
        )
        if not isinstance(definition_id, str) or not definition_id:
            continue

        metrics = metrics_bundle.registry_metrics_for_definition_id(definition_id)
        if not metrics:
            continue

        generated = entry.get("generated")
        if not isinstance(generated, dict):
            generated = {}
            entry["generated"] = generated
        generated["metrics"] = metrics
        injected_count += 1

    return injected_count
