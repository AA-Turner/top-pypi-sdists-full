# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Registry store interface.

This module defines the single high-level interface the CLI should depend on.
Concrete stores (coral/sonar) implement this interface.

Design goal: avoid store-type branching in the CLI.
Unsupported operations should raise NotImplementedError from the store
implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from airbyte_ops_mcp.registry._enums import (
    ConnectorLanguage,
    ConnectorType,
    SupportLevel,
)
from airbyte_ops_mcp.registry.compile import CompileResult, PurgeLatestResult
from airbyte_ops_mcp.registry.models import ConnectorPublishResult
from airbyte_ops_mcp.registry.publish_artifacts import PublishArtifactsResult
from airbyte_ops_mcp.registry.rebuild import OutputMode, RebuildResult
from airbyte_ops_mcp.registry.store import RegistryStore, StoreType
from airbyte_ops_mcp.registry.yank import YankResult


def _op_not_implemented_message(store_type: StoreType, op_name: str) -> str:
    return (
        f"Operation '{op_name}' is not implemented for store type '{store_type.value}'."
    )


class Registry(ABC):
    """A configured connector registry store.

    A Registry is bound to a specific `airbyte_ops_mcp.registry.store.RegistryStore`
    (store type + env + optional prefix), and provides methods used by the CLI to
    read/write registry contents.
    """

    def __init__(self, store: RegistryStore) -> None:
        self.store = store

    @property
    def store_type(self) -> StoreType:
        return self.store.store_type

    @property
    def bucket_name(self) -> str:
        return self.store.bucket

    @property
    def prefix(self) -> str:
        return self.store.prefix

    def _require_no_prefix(self, op_name: str) -> None:
        """Raise if this op doesn't support prefixed targets."""

        if self.prefix:
            raise NotImplementedError(
                f"Operation '{op_name}' does not yet support store prefixes (got prefix='{self.prefix}')."
            )

    # ---------------------------------------------------------------------
    # Read operations
    # ---------------------------------------------------------------------

    @abstractmethod
    def list_connectors(
        self,
        *,
        support_level: SupportLevel | None = None,
        min_support_level: SupportLevel | None = None,
        connector_type: ConnectorType | None = None,
        language: ConnectorLanguage | None = None,
    ) -> list[str]:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "list_connectors")
        )

    def list_connector_versions(self, connector_name: str) -> list[str]:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "list_connector_versions")
        )

    def get_connector_metadata(
        self, connector_name: str, version: str = "latest"
    ) -> dict[str, Any]:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "get_connector_metadata")
        )

    # ---------------------------------------------------------------------
    # Write / mutate operations
    # ---------------------------------------------------------------------

    def progressive_rollout_create(
        self,
        repo_path: Path,
        connector_name: str,
        dry_run: bool = False,
    ) -> ConnectorPublishResult:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "progressive_rollout_create")
        )

    def progressive_rollout_cleanup(
        self,
        repo_path: Path,
        connector_name: str,
        dry_run: bool = False,
    ) -> ConnectorPublishResult:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "progressive_rollout_cleanup")
        )

    def yank(
        self,
        connector_name: str,
        version: str,
        reason: str = "",
        dry_run: bool = False,
    ) -> YankResult:
        raise NotImplementedError(_op_not_implemented_message(self.store_type, "yank"))

    def unyank(
        self,
        connector_name: str,
        version: str,
        dry_run: bool = False,
    ) -> YankResult:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "unyank")
        )

    def publish_version_artifacts(
        self,
        connector_name: str,
        version: str,
        artifacts_dir: Path,
        dry_run: bool = False,
        with_validate: bool = True,
    ) -> PublishArtifactsResult:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "publish_version_artifacts")
        )

    def delete_dev_latest(
        self,
        connector_name: list[str] | None = None,
        dry_run: bool = False,
    ) -> PurgeLatestResult:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "delete_dev_latest")
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
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "compile")
        )

    def marketing_stubs_check(self, repo_root: Path) -> dict[str, Any]:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "marketing_stubs_check")
        )

    def marketing_stubs_sync(
        self,
        repo_root: Path,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "marketing_stubs_sync")
        )

    def mirror(
        self,
        output_mode: OutputMode,
        output_path_root: str | None = None,
        gcs_bucket: str | None = None,
        s3_bucket: str | None = None,
        dry_run: bool = False,
        connector_name: list[str] | None = None,
    ) -> RebuildResult:
        raise NotImplementedError(
            _op_not_implemented_message(self.store_type, "mirror")
        )


def get_registry(store: RegistryStore) -> Registry:
    """Factory for obtaining the right store implementation."""

    if store.store_type == StoreType.CORAL:
        from airbyte_ops_mcp.registry.coral_registry_store import CoralRegistry

        return CoralRegistry(store)

    if store.store_type == StoreType.SONAR:
        from airbyte_ops_mcp.registry.sonar_registry_store import SonarRegistry

        return SonarRegistry(store)

    # defensive: StoreType is an Enum, but keep this for readability
    raise ValueError(f"Unknown store type: {store.store_type}")
