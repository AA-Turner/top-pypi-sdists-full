# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for ProtocolProjectionDatabase (async adapter protocol)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from omnibase_compat.protocols.protocol_projection_database import ProtocolProjectionDatabase


class _MockAdapter:
    async def execute(self, query: str, *params: Any) -> list[dict[str, Any]]:
        return []

    async def execute_many(self, query: str, params_list: list[tuple[Any, ...]]) -> None:
        return None

    async def fetchval(self, query: str, *params: Any) -> Any:
        return None

    async def close(self) -> None:
        return None


class _MissingExecute:
    async def execute_many(self, query: str, params_list: list[tuple[Any, ...]]) -> None:
        return None

    async def fetchval(self, query: str, *params: Any) -> Any:
        return None

    async def close(self) -> None:
        return None


class _MissingClose:
    async def execute(self, query: str, *params: Any) -> list[dict[str, Any]]:
        return []

    async def execute_many(self, query: str, params_list: list[tuple[Any, ...]]) -> None:
        return None

    async def fetchval(self, query: str, *params: Any) -> Any:
        return None


@pytest.mark.unit
def test_runtime_checkable_mock_is_instance() -> None:
    assert isinstance(_MockAdapter(), ProtocolProjectionDatabase)


@pytest.mark.unit
def test_missing_execute_is_not_instance() -> None:
    assert not isinstance(_MissingExecute(), ProtocolProjectionDatabase)


@pytest.mark.unit
def test_missing_close_is_not_instance() -> None:
    assert not isinstance(_MissingClose(), ProtocolProjectionDatabase)


@pytest.mark.unit
def test_empty_adapter_is_not_instance(empty_projection_adapter: object) -> None:
    assert not isinstance(empty_projection_adapter, ProtocolProjectionDatabase)


@pytest.mark.unit
def test_protocol_is_runtime_checkable(
    assert_runtime_checkable_protocol: Callable[[type[Any]], None],
) -> None:
    assert_runtime_checkable_protocol(ProtocolProjectionDatabase)


@pytest.mark.unit
def test_protocol_class_name() -> None:
    assert ProtocolProjectionDatabase.__name__ == "ProtocolProjectionDatabase"


@pytest.mark.unit
def test_protocol_has_expected_methods(
    assert_protocol_methods: Callable[[type[Any], set[str]], None],
) -> None:
    assert_protocol_methods(
        ProtocolProjectionDatabase,
        {"execute", "execute_many", "fetchval", "close"},
    )
