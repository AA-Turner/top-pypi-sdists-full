# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from airbyte_ops_mcp.registry._enums import (
    ConnectorLanguage,
    ConnectorType,
    SupportLevel,
)
from airbyte_ops_mcp.registry.compile import (
    CompileResult,
    PurgeLatestResult,
    compile_registry,
    purge_latest_dirs,
)
from airbyte_ops_mcp.registry.connector_stubs import (
    CONNECTOR_STUBS_PATH,
    ConnectorStub,
    load_local_stubs,
    read_connector_stubs,
    write_connector_stubs,
)
from airbyte_ops_mcp.registry.operations import (
    get_registry_entry,
    list_connector_versions,
    list_registry_connectors,
    list_registry_connectors_filtered,
)
from airbyte_ops_mcp.registry.progressive_rollout_marker import (
    ProgressiveRolloutMarkerResult,
    finalize_progressive_rollout_marker,
)
from airbyte_ops_mcp.registry.publish_artifacts import (
    PublishArtifactsResult,
    publish_version_artifacts,
)
from airbyte_ops_mcp.registry.rebuild import OutputMode, RebuildResult, rebuild_registry
from airbyte_ops_mcp.registry.registry_store_base import Registry
from airbyte_ops_mcp.registry.store import RegistryStore
from airbyte_ops_mcp.registry.yank import (
    YankResult,
    unyank_connector_version,
    yank_connector_version,
)


class CoralRegistry(Registry):
    """Coral (GCS) implementation of `Registry`."""

    def __init__(self, store: RegistryStore) -> None:
        super().__init__(store)

    # ---------------------------------------------------------------------
    # Read operations
    # ---------------------------------------------------------------------

    def list_connectors(
        self,
        *,
        support_level: SupportLevel | None = None,
        min_support_level: SupportLevel | None = None,
        connector_type: ConnectorType | None = None,
        language: ConnectorLanguage | None = None,
    ) -> list[str]:
        has_filters = any([support_level, min_support_level, connector_type, language])
        if has_filters:
            return list_registry_connectors_filtered(
                bucket_name=self.bucket_name,
                support_level=support_level,
                min_support_level=min_support_level,
                connector_type=connector_type,
                language=language,
                prefix=self.prefix,
            )
        self._require_no_prefix("list_connectors")
        return list_registry_connectors(bucket_name=self.bucket_name)

    def list_connector_versions(self, connector_name: str) -> list[str]:
        self._require_no_prefix("list_connector_versions")
        return list_connector_versions(
            connector_name=connector_name,
            bucket_name=self.bucket_name,
        )

    def get_connector_metadata(
        self,
        connector_name: str,
        version: str = "latest",
    ) -> dict[str, Any]:
        self._require_no_prefix("get_connector_metadata")
        return get_registry_entry(
            connector_name=connector_name,
            bucket_name=self.bucket_name,
            version=version,
        )

    # ---------------------------------------------------------------------
    # Write / mutate operations
    # ---------------------------------------------------------------------

    def yank(
        self,
        connector_name: str,
        version: str,
        reason: str = "",
        approval_url: str = "",
        dry_run: bool = False,
    ) -> YankResult:
        self._require_no_prefix("yank")
        return yank_connector_version(
            connector_name=connector_name,
            version=version,
            bucket_name=self.bucket_name,
            reason=reason,
            approval_url=approval_url,
            dry_run=dry_run,
        )

    def unyank(
        self,
        connector_name: str,
        version: str,
        dry_run: bool = False,
    ) -> YankResult:
        self._require_no_prefix("unyank")
        return unyank_connector_version(
            connector_name=connector_name,
            version=version,
            bucket_name=self.bucket_name,
            dry_run=dry_run,
        )

    def finalize_progressive_rollout_marker(
        self,
        connector_name: str,
        outcome: Literal["promoted", "aborted"],
        version: str | None = None,
        dry_run: bool = False,
    ) -> ProgressiveRolloutMarkerResult:
        return finalize_progressive_rollout_marker(
            connector_name=connector_name,
            store=self.store,
            outcome=outcome,
            version=version,
            dry_run=dry_run,
        )

    def publish_version_artifacts(
        self,
        connector_name: str,
        version: str,
        artifacts_dir: Path,
        dry_run: bool = False,
        with_validate: bool = True,
    ) -> PublishArtifactsResult:
        return publish_version_artifacts(
            connector_name=connector_name,
            version=version,
            artifacts_dir=artifacts_dir,
            store=self.store,
            dry_run=dry_run,
            with_validate=with_validate,
        )

    def delete_dev_latest(
        self,
        connector_name: list[str] | None = None,
        dry_run: bool = False,
    ) -> PurgeLatestResult:
        return purge_latest_dirs(
            store=self.store,
            connector_name=connector_name,
            dry_run=dry_run,
        )

    def compile(
        self,
        connector_name: list[str] | None = None,
        dry_run: bool = False,
        with_secrets_mask: bool = False,
        with_legacy_migration: str | None = None,
        with_metrics: bool = True,
        force: bool = False,
    ) -> CompileResult:
        return compile_registry(
            store=self.store,
            connector_name=connector_name,
            dry_run=dry_run,
            with_secrets_mask=with_secrets_mask,
            with_legacy_migration=with_legacy_migration,
            with_metrics=with_metrics,
            force=force,
        )

    def marketing_stubs_check(self, repo_root: Path) -> dict[str, Any]:
        self._require_no_prefix("marketing_stubs_check")

        local_stubs = load_local_stubs(repo_root)
        published_stubs = read_connector_stubs(self.bucket_name)

        local_by_id = {stub["id"]: stub for stub in local_stubs if stub.get("id")}
        published_by_id = {
            stub["id"]: stub for stub in published_stubs if stub.get("id")
        }

        all_ids = set(local_by_id.keys()) | set(published_by_id.keys())
        differences: list[dict[str, str]] = []

        for stub_id in sorted(all_ids):
            local_stub = local_by_id.get(stub_id)
            published_stub = published_by_id.get(stub_id)

            if local_stub is None:
                differences.append({"id": stub_id, "status": "only_in_gcs"})
            elif published_stub is None:
                differences.append({"id": stub_id, "status": "only_in_local"})
            elif local_stub != published_stub:
                differences.append({"id": stub_id, "status": "modified"})

        return {
            "local_count": len(local_stubs),
            "published_count": len(published_stubs),
            "in_sync": len(differences) == 0,
            "differences": differences,
            "bucket": self.bucket_name,
            "path": CONNECTOR_STUBS_PATH,
        }

    def marketing_stubs_sync(
        self,
        repo_root: Path,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        self._require_no_prefix("marketing_stubs_sync")

        local_stubs = load_local_stubs(repo_root)
        for stub in local_stubs:
            ConnectorStub(**stub)

        if dry_run:
            return {
                "dry_run": True,
                "stub_count": len(local_stubs),
                "bucket": self.bucket_name,
                "path": CONNECTOR_STUBS_PATH,
            }

        write_connector_stubs(self.bucket_name, local_stubs)

        return {
            "dry_run": False,
            "stub_count": len(local_stubs),
            "bucket": self.bucket_name,
            "path": CONNECTOR_STUBS_PATH,
            "stub_ids": [stub.get("id") for stub in local_stubs],
        }

    def mirror(
        self,
        output_mode: OutputMode,
        output_path_root: str | None = None,
        gcs_bucket: str | None = None,
        s3_bucket: str | None = None,
        dry_run: bool = False,
        connector_name: list[str] | None = None,
    ) -> RebuildResult:
        self._require_no_prefix("mirror")
        return rebuild_registry(
            source_bucket=self.bucket_name,
            output_mode=output_mode,
            output_path_root=output_path_root,
            gcs_bucket=gcs_bucket,
            s3_bucket=s3_bucket,
            dry_run=dry_run,
            connector_name=connector_name,
        )
