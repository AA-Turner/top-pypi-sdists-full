# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Fetch full stack traces from Google Cloud Logs by error ID.

This module provides functionality to look up error details from GCP Cloud Logging
using an error ID (UUID). This is useful for debugging API errors that return
only an error ID in the response.

Example:
    from airbyte_ops_mcp.gcp_logs import fetch_error_logs

    result = fetch_error_logs(
        error_id="3173452e-8f22-4286-a1ec-b0f16c1e078a",
        project="prod-ab-cloud-proj",
        lookback_days=7,
    )
    for entry in result.entries:
        print(entry.message)
"""

from __future__ import annotations

import re
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from google.cloud import logging as gcp_logging
from google.cloud.logging_v2 import entries
from pydantic import BaseModel, Field

from airbyte_ops_mcp.gcp_auth import get_logging_client

# Default GCP project for Airbyte Cloud
DEFAULT_GCP_PROJECT = "prod-ab-cloud-proj"


class GCPSeverity(StrEnum):
    """Valid GCP Cloud Logging severity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    ALERT = "ALERT"
    EMERGENCY = "EMERGENCY"


class GCPLogResourceLabels(BaseModel):
    """Resource labels from a GCP log entry."""

    pod_name: str | None = Field(default=None, description="Kubernetes pod name")
    container_name: str | None = Field(
        default=None, description="Container name within the pod"
    )
    namespace_name: str | None = Field(default=None, description="Kubernetes namespace")
    cluster_name: str | None = Field(default=None, description="GKE cluster name")


class GCPLogResource(BaseModel):
    """Resource information from a GCP log entry."""

    type: str | None = Field(default=None, description="Resource type")
    labels: GCPLogResourceLabels = Field(
        default_factory=GCPLogResourceLabels, description="Resource labels"
    )


class GCPLogSourceLocation(BaseModel):
    """Source location information from a GCP log entry."""

    file: str | None = Field(default=None, description="Source file path")
    line: int | None = Field(default=None, description="Line number")
    function: str | None = Field(default=None, description="Function name")


class GCPLogEntry(BaseModel):
    """A single log entry from GCP Cloud Logging."""

    timestamp: datetime | None = Field(
        default=None, description="When the log entry was created"
    )
    severity: str | None = Field(
        default=None, description="Log severity (DEBUG, INFO, WARNING, ERROR, etc.)"
    )
    log_name: str | None = Field(default=None, description="Full log name path")
    insert_id: str | None = Field(
        default=None, description="Unique identifier for the log entry"
    )
    trace: str | None = Field(
        default=None, description="Trace ID for distributed tracing"
    )
    span_id: str | None = Field(default=None, description="Span ID within the trace")
    payload: Any = Field(default=None, description="Log entry payload (text or struct)")
    payload_type: str | None = Field(
        default=None, description="Type of payload (text, struct, protobuf)"
    )
    resource: GCPLogResource = Field(
        default_factory=GCPLogResource, description="Resource information"
    )
    source_location: GCPLogSourceLocation | None = Field(
        default=None, description="Source code location"
    )
    labels: dict[str, str] = Field(
        default_factory=dict, description="User-defined labels"
    )


class GCPLogPayload(BaseModel):
    """Extracted and combined payload from grouped log entries."""

    timestamp: datetime | None = Field(
        default=None, description="Timestamp of the first entry in the group"
    )
    severity: str | None = Field(default=None, description="Severity of the log group")
    resource: GCPLogResource = Field(
        default_factory=GCPLogResource, description="Resource information"
    )
    num_log_lines: int = Field(
        default=0, description="Number of log lines combined into this payload"
    )
    message: str = Field(default="", description="Combined message from all log lines")


class GCPLogSearchResult(BaseModel):
    """Result of searching GCP Cloud Logging for an error ID."""

    error_id: str = Field(description="The error ID that was searched for")
    project: str = Field(description="GCP project that was searched")
    lookback_days_searched: int = Field(
        description="Number of lookback days that were searched"
    )
    total_entries_found: int = Field(
        description="Total number of log entries found (including related entries)"
    )
    entries: list[GCPLogEntry] = Field(
        default_factory=list, description="Raw log entries found"
    )
    payloads: list[GCPLogPayload] = Field(
        default_factory=list,
        description="Extracted and grouped payloads (reconstructed stack traces)",
    )


def _build_filter(
    error_id: str,
    lookback_days: int,
    min_severity_filter: GCPSeverity | None,
) -> str:
    """Build the Cloud Logging filter query."""
    filter_parts = [f'"{error_id}"']

    start_time = datetime.now(UTC) - timedelta(days=lookback_days)
    filter_parts.append(f'timestamp >= "{start_time.isoformat()}"')

    if min_severity_filter:
        filter_parts.append(f"severity>={min_severity_filter}")

    return " AND ".join(filter_parts)


def _entry_to_model(
    entry: entries.StructEntry | entries.TextEntry | entries.ProtobufEntry,
) -> GCPLogEntry:
    """Convert a GCP log entry to a Pydantic model."""
    resource_labels = {}
    if entry.resource and entry.resource.labels:
        resource_labels = dict(entry.resource.labels)

    resource = GCPLogResource(
        type=entry.resource.type if entry.resource else None,
        labels=GCPLogResourceLabels(
            pod_name=resource_labels.get("pod_name"),
            container_name=resource_labels.get("container_name"),
            namespace_name=resource_labels.get("namespace_name"),
            cluster_name=resource_labels.get("cluster_name"),
        ),
    )

    source_location = None
    if entry.source_location:
        source_location = GCPLogSourceLocation(
            file=entry.source_location.get("file"),
            line=entry.source_location.get("line"),
            function=entry.source_location.get("function"),
        )

    payload: Any = None
    payload_type = "unknown"
    if isinstance(entry, entries.StructEntry):
        payload = entry.payload
        payload_type = "struct"
    elif isinstance(entry, entries.TextEntry):
        payload = entry.payload
        payload_type = "text"
    elif isinstance(entry, entries.ProtobufEntry):
        payload = str(entry.payload)
        payload_type = "protobuf"

    return GCPLogEntry(
        timestamp=entry.timestamp,
        severity=entry.severity,
        log_name=entry.log_name,
        insert_id=entry.insert_id,
        trace=entry.trace,
        span_id=entry.span_id,
        payload=payload,
        payload_type=payload_type,
        resource=resource,
        source_location=source_location,
        labels=dict(entry.labels) if entry.labels else {},
    )


def _group_entries_by_occurrence(
    log_entries: list[GCPLogEntry],
) -> list[list[GCPLogEntry]]:
    """Group log entries by occurrence (timestamp clusters within 1 second)."""
    if not log_entries:
        return []

    sorted_entries = sorted(
        log_entries, key=lambda x: x.timestamp or datetime.min.replace(tzinfo=UTC)
    )

    groups: list[list[GCPLogEntry]] = []
    current_group = [sorted_entries[0]]
    current_timestamp = sorted_entries[0].timestamp or datetime.min.replace(tzinfo=UTC)

    for entry in sorted_entries[1:]:
        entry_timestamp = entry.timestamp or datetime.min.replace(tzinfo=UTC)
        time_diff = abs((entry_timestamp - current_timestamp).total_seconds())

        current_pod = current_group[0].resource.labels.pod_name
        entry_pod = entry.resource.labels.pod_name

        if time_diff <= 1 and entry_pod == current_pod:
            current_group.append(entry)
        else:
            groups.append(current_group)
            current_group = [entry]
            current_timestamp = entry_timestamp

    if current_group:
        groups.append(current_group)

    return groups


def _extract_payloads(log_entries: list[GCPLogEntry]) -> list[GCPLogPayload]:
    """Extract and group payloads by occurrence."""
    if not log_entries:
        return []

    grouped = _group_entries_by_occurrence(log_entries)

    results = []
    for group in grouped:
        payloads = []
        for entry in group:
            if entry.payload:
                payload_text = str(entry.payload)
                payload_text = re.sub(r"\x1b\[[0-9;]*m", "", payload_text)
                payloads.append(payload_text)

        combined_message = "\n".join(payloads)

        first_entry = group[0]
        result = GCPLogPayload(
            timestamp=first_entry.timestamp,
            severity=first_entry.severity,
            resource=first_entry.resource,
            num_log_lines=len(group),
            message=combined_message,
        )
        results.append(result)

    return results


def fetch_error_logs(
    error_id: str,
    project: str = DEFAULT_GCP_PROJECT,
    lookback_days: int = 7,
    min_severity_filter: GCPSeverity | None = None,
    include_log_envelope_seconds: float = 1.0,
    max_log_entries: int | None = None,
) -> GCPLogSearchResult:
    """Fetch logs from Google Cloud Logging by error ID.

    This function searches GCP Cloud Logging for log entries containing the
    specified error ID, then fetches related log entries (multi-line stack traces)
    from the same timestamp and resource.
    """
    client = get_logging_client(project)

    filter_str = _build_filter(error_id, lookback_days, min_severity_filter)

    entries_iterator = client.list_entries(
        filter_=filter_str,
        order_by=gcp_logging.DESCENDING,
    )

    initial_matches = list(entries_iterator)

    if not initial_matches:
        return GCPLogSearchResult(
            error_id=error_id,
            project=project,
            lookback_days_searched=lookback_days,
            total_entries_found=0,
            entries=[],
            payloads=[],
        )

    all_results: list[GCPLogEntry] = []
    seen_insert_ids: set[str] = set()

    for match in initial_matches:
        timestamp = match.timestamp
        resource_type_val = match.resource.type if match.resource else None
        resource_labels = (
            dict(match.resource.labels)
            if match.resource and match.resource.labels
            else {}
        )
        log_name = match.log_name

        start_time = timestamp - timedelta(seconds=include_log_envelope_seconds)
        end_time = timestamp + timedelta(seconds=include_log_envelope_seconds)

        related_filter_parts = [
            f'timestamp >= "{start_time.isoformat()}"',
            f'timestamp <= "{end_time.isoformat()}"',
        ]

        if log_name:
            related_filter_parts.append(f'logName="{log_name}"')

        if resource_type_val:
            related_filter_parts.append(f'resource.type="{resource_type_val}"')

        if "pod_name" in resource_labels:
            related_filter_parts.append(
                f'resource.labels.pod_name="{resource_labels["pod_name"]}"'
            )
        if "container_name" in resource_labels:
            related_filter_parts.append(
                f'resource.labels.container_name="{resource_labels["container_name"]}"'
            )

        # Note: resource_type_val is extracted from the matched entry, and
        # min_severity_filter is already applied in the initial search filter

        related_filter = " AND ".join(related_filter_parts)

        related_entries = client.list_entries(
            filter_=related_filter,
            order_by=gcp_logging.ASCENDING,
        )

        for entry in related_entries:
            if entry.insert_id and entry.insert_id not in seen_insert_ids:
                seen_insert_ids.add(entry.insert_id)
                all_results.append(_entry_to_model(entry))

    all_results.sort(
        key=lambda x: x.timestamp or datetime.min.replace(tzinfo=UTC), reverse=True
    )

    if max_log_entries:
        all_results = all_results[:max_log_entries]

    payloads = _extract_payloads(all_results)

    return GCPLogSearchResult(
        error_id=error_id,
        project=project,
        lookback_days_searched=lookback_days,
        total_entries_found=len(all_results),
        entries=all_results,
        payloads=payloads,
    )
