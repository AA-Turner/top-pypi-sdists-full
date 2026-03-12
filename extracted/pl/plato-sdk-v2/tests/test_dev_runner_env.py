"""Tests for DevRunner debug env forwarding and world command env vars."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from plato.cli.chronos.dev.runner import DevRunner


@pytest.fixture
def runner() -> DevRunner:
    """Create a DevRunner with minimal mocked config."""
    config = MagicMock()
    config.dev.world = None
    config.dev.agents = {}
    config.dev.extra_sync = {}
    config.dev.sync_sdk = False
    with patch.dict(os.environ, {"PLATO_API_KEY": "test-key-123"}):
        return DevRunner(config=config, config_path=Path("/tmp/fake-config.json"))


def test_forwarded_debug_env_empty(runner: DevRunner) -> None:
    """No debug env vars set → empty string."""
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("PLATO_FUSE_DEBUG", None)
        os.environ.pop("PLATO_SMART_COMMIT_DEBUG", None)
        os.environ.pop("RUST_LOG", None)
        assert runner._forwarded_debug_env_assignments() == ""


def test_forwarded_debug_env_single(runner: DevRunner) -> None:
    """One debug var set → forwarded."""
    with patch.dict(os.environ, {"PLATO_FUSE_DEBUG": "1"}, clear=False):
        os.environ.pop("PLATO_SMART_COMMIT_DEBUG", None)
        os.environ.pop("RUST_LOG", None)
        result = runner._forwarded_debug_env_assignments()
        assert "PLATO_FUSE_DEBUG=1" in result


def test_forwarded_debug_env_multiple(runner: DevRunner) -> None:
    """Multiple debug vars → all forwarded."""
    env = {"PLATO_FUSE_DEBUG": "1", "RUST_LOG": "debug", "PLATO_SMART_COMMIT_DEBUG": "trace"}
    with patch.dict(os.environ, env, clear=False):
        result = runner._forwarded_debug_env_assignments()
        assert "PLATO_FUSE_DEBUG=1" in result
        assert "RUST_LOG=debug" in result
        assert "PLATO_SMART_COMMIT_DEBUG=trace" in result


def test_forwarded_debug_env_quotes_special_chars(runner: DevRunner) -> None:
    """Values with spaces/special chars are shell-quoted."""
    with patch.dict(os.environ, {"RUST_LOG": "plato_fuse=debug,warn"}, clear=False):
        os.environ.pop("PLATO_FUSE_DEBUG", None)
        os.environ.pop("PLATO_SMART_COMMIT_DEBUG", None)
        result = runner._forwarded_debug_env_assignments()
        assert "RUST_LOG=" in result
        # shlex.quote should handle the comma
        assert "plato_fuse=debug,warn" in result
