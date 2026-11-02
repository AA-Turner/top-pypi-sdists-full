"""Tests for _resolve_base_sha."""

from types import MethodType
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_builder import _resolve_base_sha


def test_unsupported_base_ref_lookup_returns_empty_metadata() -> None:
    """The inherited or absent lookup preserves the unpinned fallback."""
    provider = MagicMock()
    provider.get_ref_sha = None

    assert _resolve_base_sha(provider, 7, "main") == ("", {})


def test_supported_lookup_returns_the_base_sha() -> None:
    """An overridden base-ref lookup pins the snapshot to its resolved SHA."""
    provider = MagicMock()
    provider.get_ref_sha = MethodType(lambda _self, _ref: "base", provider)

    assert _resolve_base_sha(provider, 7, "main") == ("base", {"base_sha": "base"})


def test_supported_lookup_without_sha_fails_closed() -> None:
    """An implemented lookup that cannot resolve the branch cannot be ignored."""
    provider = MagicMock()
    provider.get_ref_sha = MethodType(lambda _self, _ref: "", provider)

    with pytest.raises(RuntimeError, match="PR #7: base branch SHA unavailable"):
        _resolve_base_sha(provider, 7, "main")
