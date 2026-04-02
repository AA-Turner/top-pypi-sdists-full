"""Tests for plato.tools workspace helpers."""

from pathlib import Path

from plato.tools import get_workspace, set_workspace


def test_get_workspace_default():
    """get_workspace returns /workspace by default."""
    set_workspace("/workspace")
    assert get_workspace() == Path("/workspace")


def test_set_and_get_workspace():
    """set_workspace / get_workspace round-trip."""
    set_workspace("/tmp/my-workspace")
    assert get_workspace() == Path("/tmp/my-workspace")
    set_workspace("/workspace")


def test_handler_can_use_get_workspace_after_set_workspace():
    """Handlers can resolve workspace-relative paths after set_workspace()."""
    set_workspace("/tmp/my-workspace")

    def workspace_handler() -> str:
        return str(get_workspace() / "output.txt")

    assert workspace_handler() == "/tmp/my-workspace/output.txt"
    set_workspace("/workspace")
