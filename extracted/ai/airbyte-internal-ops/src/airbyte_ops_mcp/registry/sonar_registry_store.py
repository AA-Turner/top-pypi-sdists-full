# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

from __future__ import annotations

from airbyte_ops_mcp.registry._enums import (
    ConnectorLanguage,
    ConnectorType,
    SupportLevel,
)
from airbyte_ops_mcp.registry.registry_store_base import Registry
from airbyte_ops_mcp.registry.store import RegistryStore


class SonarRegistry(Registry):
    """Sonar (S3) implementation of `Registry`.

    Stubbed initially. Methods should be implemented as sonar registry support
    is built out.
    """

    def __init__(self, store: RegistryStore) -> None:
        super().__init__(store)

    def list_connectors(
        self,
        *,
        support_level: SupportLevel | None = None,
        min_support_level: SupportLevel | None = None,
        connector_type: ConnectorType | None = None,
        language: ConnectorLanguage | None = None,
    ) -> list[str]:
        raise NotImplementedError(
            f"Operation 'list_connectors' is not implemented for store type '{self.store_type.value}'."
        )
