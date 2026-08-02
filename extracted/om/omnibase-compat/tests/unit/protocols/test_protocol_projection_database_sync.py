# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for ProtocolProjectionDatabaseSync (sync adapter protocol)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from omnibase_compat.protocols.protocol_projection_database_sync import (
    ProtocolProjectionDatabaseSync,
)


class _MockSyncAdapter:
    def upsert(self, table: str, conflict_key: str, row: dict[str, object]) -> bool:
        return True

    def query(
        self,
        table: str,
        filters: dict[str, object] | None = None,
    ) -> list[dict[str, object]]:
        return []


class _MissingUpsert:
    def query(
        self,
        table: str,
        filters: dict[str, object] | None = None,
    ) -> list[dict[str, object]]:
        return []


class _MissingQuery:
    def upsert(self, table: str, conflict_key: str, row: dict[str, object]) -> bool:
        return True


@pytest.mark.unit
def test_runtime_checkable_mock_is_instance() -> None:
    assert isinstance(_MockSyncAdapter(), ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_missing_upsert_is_not_instance() -> None:
    assert not isinstance(_MissingUpsert(), ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_missing_query_is_not_instance() -> None:
    assert not isinstance(_MissingQuery(), ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_empty_adapter_is_not_instance(empty_projection_adapter: object) -> None:
    assert not isinstance(empty_projection_adapter, ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_protocol_is_runtime_checkable(
    assert_runtime_checkable_protocol: Callable[[type[Any]], None],
) -> None:
    assert_runtime_checkable_protocol(ProtocolProjectionDatabaseSync)


@pytest.mark.unit
def test_protocol_class_name() -> None:
    assert ProtocolProjectionDatabaseSync.__name__ == "ProtocolProjectionDatabaseSync"


@pytest.mark.unit
def test_protocol_has_expected_methods(
    assert_protocol_methods: Callable[[type[Any], set[str]], None],
) -> None:
    assert_protocol_methods(ProtocolProjectionDatabaseSync, {"upsert", "query"})
