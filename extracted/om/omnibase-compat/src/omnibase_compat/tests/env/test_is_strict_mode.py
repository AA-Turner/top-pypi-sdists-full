# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Tests for ``omnibase_compat.env.is_strict_mode``.

These tests pin the literal-``"1"``-only semantic of the ``AUTOWIRE_STRICT``
env var. The helper must NOT interpret common truthy strings (``"true"``,
``"yes"``, ``"True"``, whitespace-padded ``"1 "``) as strict. It must only
return ``True`` when the env var is set to the exact single-character
string ``"1"``.

This invariant preserves the hot-patch semantic from the runtime-boot
durability plan (``2026-04-19-runtime-permanent-fix-and-regression-guard-part-1``
Task 3) exactly, so a state-triggered follow-up can later flip the default
by replacing a single comparison site.
"""

from __future__ import annotations

import pytest

from omnibase_compat.env import is_strict_mode
from omnibase_compat.env.util_is_strict_mode import is_strict_mode as _direct_import


def test_is_strict_mode_returns_false_when_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With ``AUTOWIRE_STRICT`` absent from the environment, returns False."""
    monkeypatch.delenv("AUTOWIRE_STRICT", raising=False)
    assert is_strict_mode() is False


def test_is_strict_mode_returns_false_when_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty string is NOT strict."""
    monkeypatch.setenv("AUTOWIRE_STRICT", "")
    assert is_strict_mode() is False


def test_is_strict_mode_returns_false_for_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Literal ``"0"`` is NOT strict."""
    monkeypatch.setenv("AUTOWIRE_STRICT", "0")
    assert is_strict_mode() is False


def test_is_strict_mode_returns_false_for_lowercase_true(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truthy-looking string ``"true"`` is NOT strict — literal-1 semantic."""
    monkeypatch.setenv("AUTOWIRE_STRICT", "true")
    assert is_strict_mode() is False


def test_is_strict_mode_returns_false_for_uppercase_true(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truthy-looking string ``"TRUE"`` is NOT strict — literal-1 semantic."""
    monkeypatch.setenv("AUTOWIRE_STRICT", "TRUE")
    assert is_strict_mode() is False


def test_is_strict_mode_returns_false_for_trailing_whitespace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trailing whitespace breaks the literal-``"1"`` match."""
    monkeypatch.setenv("AUTOWIRE_STRICT", "1 ")
    assert is_strict_mode() is False


def test_is_strict_mode_returns_true_for_literal_one(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only the exact single-character string ``"1"`` enables strict mode."""
    monkeypatch.setenv("AUTOWIRE_STRICT", "1")
    assert is_strict_mode() is True


def test_reexport_matches_direct_import() -> None:
    """``omnibase_compat.env.is_strict_mode`` must be the same callable as the
    direct module import — confirms the ``__init__.py`` re-export is wired.
    """
    assert is_strict_mode is _direct_import
