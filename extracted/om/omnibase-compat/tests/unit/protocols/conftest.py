# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Shared fixtures for projection protocol tests."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest


class _EmptyProjectionAdapter:
    """Adapter with no protocol methods."""


@pytest.fixture
def empty_projection_adapter() -> object:
    """Return an object that should not satisfy projection protocols."""
    return _EmptyProjectionAdapter()


@pytest.fixture
def assert_runtime_checkable_protocol() -> Callable[[type[Any]], None]:
    """Return an assertion helper for runtime-checkable protocols."""

    def _assert_runtime_checkable(protocol: type[Any]) -> None:
        try:
            isinstance(object(), protocol)
        except TypeError:
            pytest.fail(f"{protocol.__name__} is not @runtime_checkable")

    return _assert_runtime_checkable


@pytest.fixture
def assert_protocol_methods() -> Callable[[type[Any], set[str]], None]:
    """Return an assertion helper for protocol method presence."""

    def _assert_protocol_methods(protocol: type[Any], methods: set[str]) -> None:
        for method in methods:
            assert hasattr(protocol, method), f"Missing method: {method}"

    return _assert_protocol_methods
