from __future__ import annotations

import importlib.util
import inspect

import pytest

from matrx_ai.tools import vfs_routing
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.vfs_routing import (
    FS_EDIT_TOOL_DEFINITION,
    VFS_REMAP_TABLE,
    is_vfs_globally_enabled,
    remap,
    should_route_to_vfs,
)

VFS_ADAPTERS_PRESENT = (
    importlib.util.find_spec("matrx_ai.tools.implementations.vfs_filesystem")
    is not None
    and importlib.util.find_spec("matrx_ai.tools.implementations.vfs_shell")
    is not None
)


def _enable_vfs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Flip the code-level VFS toggle on for the duration of a test.

    VFS routing is gated by the module-level ``VFS_GLOBALLY_ENABLED`` constant
    (the 2026-06-11 replacement for the ``MATRX_VFS_ENABLED`` env var), read at
    call time by ``is_vfs_globally_enabled`` / ``should_route_to_vfs``.
    """
    monkeypatch.setattr(vfs_routing, "VFS_GLOBALLY_ENABLED", True)


# ---------------------------------------------------------------------------
# Pure-function unit tests for the routing module
# ---------------------------------------------------------------------------


def test_remap_table_covers_expected_paths() -> None:
    expected = {
        "matrx_ai.tools.implementations.filesystem.fs_read",
        "matrx_ai.tools.implementations.filesystem.fs_write",
        "matrx_ai.tools.implementations.filesystem.fs_list",
        "matrx_ai.tools.implementations.filesystem.fs_search",
        "matrx_ai.tools.implementations.filesystem.fs_mkdir",
        "matrx_ai.tools.implementations.shell.shell_execute",
    }
    assert expected.issubset(VFS_REMAP_TABLE.keys())


def test_globally_enabled_when_constant_true(monkeypatch: pytest.MonkeyPatch) -> None:
    _enable_vfs(monkeypatch)
    assert is_vfs_globally_enabled()


def test_disabled_by_default() -> None:
    # The toggle ships OFF; flipping it requires a code change (git), not an env var.
    assert vfs_routing.VFS_GLOBALLY_ENABLED is False
    assert not is_vfs_globally_enabled()


def test_remap_known_path() -> None:
    p = "matrx_ai.tools.implementations.filesystem.fs_read"
    assert remap(p) == "matrx_ai.tools.implementations.vfs_filesystem.fs_read"


def test_remap_unknown_passthrough() -> None:
    p = "matrx_ai.tools.implementations.no_such_module.browser_open"
    assert remap(p) == p


def test_should_route_when_globally_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    _enable_vfs(monkeypatch)
    assert should_route_to_vfs(
        "matrx_ai.tools.implementations.filesystem.fs_read", "native"
    )


def test_should_route_explicit_source_kind() -> None:
    # Even with VFS off globally, explicit "matrx_vfs" routes.
    assert should_route_to_vfs("anything", "matrx_vfs")


def test_should_not_route_unknown_with_global_on(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _enable_vfs(monkeypatch)
    assert not should_route_to_vfs(
        "matrx_ai.tools.implementations.no_such_module.browser_open", "native"
    )


def test_should_not_route_external_handler(monkeypatch: pytest.MonkeyPatch) -> None:
    _enable_vfs(monkeypatch)
    # Any source_kind value that isn't "native" / VFS_SOURCE_KIND must not route.
    assert not should_route_to_vfs("anything", "admin_authored")


def test_should_not_route_when_disabled() -> None:
    assert not should_route_to_vfs(
        "matrx_ai.tools.implementations.filesystem.fs_read", "native"
    )


def test_should_not_route_when_source_kind_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _enable_vfs(monkeypatch)
    assert not should_route_to_vfs(
        "matrx_ai.tools.implementations.filesystem.fs_read", None
    )


# ---------------------------------------------------------------------------
# Integration tests against ToolRegistry
# ---------------------------------------------------------------------------


def _fs_read_definition() -> ToolDefinition:
    return ToolDefinition(
        name="fs_read",
        description="Read a file",
        parameters={"path": {"type": "string", "required": True}},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.implementations.filesystem.fs_read",
        source_kind="native",
        is_active=True,
    )


def _module_of(callable_obj: object) -> str:
    mod = inspect.getmodule(callable_obj)
    return mod.__name__ if mod is not None else getattr(callable_obj, "__module__", "")


@pytest.mark.skipif(
    not VFS_ADAPTERS_PRESENT, reason="Phase E (vfs_filesystem/vfs_shell) not ready"
)
def test_registry_routes_fs_read_when_vfs_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _enable_vfs(monkeypatch)
    registry = ToolRegistry()
    registry.load_from_definitions([_fs_read_definition()])
    entry = registry.get("fs_read")
    assert entry is not None
    assert entry._routed_to_vfs is True
    assert entry._original_function_path == (
        "matrx_ai.tools.implementations.filesystem.fs_read"
    )
    assert entry.function_path == (
        "matrx_ai.tools.implementations.vfs_filesystem.fs_read"
    )
    assert entry._callable is not None
    assert "vfs_filesystem" in _module_of(entry._callable)


def test_registry_passthrough_when_vfs_disabled() -> None:
    registry = ToolRegistry()
    registry.load_from_definitions([_fs_read_definition()])
    entry = registry.get("fs_read")
    assert entry is not None
    assert entry._routed_to_vfs is False
    assert entry._original_function_path is None
    assert entry.function_path == (
        "matrx_ai.tools.implementations.filesystem.fs_read"
    )
    assert entry._callable is not None
    assert "vfs_filesystem" not in _module_of(entry._callable)


def test_registry_does_not_inject_fs_edit_when_disabled() -> None:
    registry = ToolRegistry()
    registry.load_from_definitions([])
    assert registry.get("fs_edit") is None


@pytest.mark.skipif(
    not VFS_ADAPTERS_PRESENT, reason="Phase E (vfs_filesystem/vfs_shell) not ready"
)
def test_fs_edit_synthetic_added_when_vfs_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _enable_vfs(monkeypatch)
    registry = ToolRegistry()
    registry.load_from_definitions([])
    entry = registry.get("fs_edit")
    assert entry is not None
    assert entry.source_kind == "matrx_vfs"
    assert entry.function_path == FS_EDIT_TOOL_DEFINITION["function_path"]


@pytest.mark.skipif(
    not VFS_ADAPTERS_PRESENT, reason="Phase E (vfs_filesystem/vfs_shell) not ready"
)
def test_fs_edit_not_double_registered(monkeypatch: pytest.MonkeyPatch) -> None:
    _enable_vfs(monkeypatch)
    registry = ToolRegistry()
    pre_existing = ToolDefinition(
        name="fs_edit",
        description="DB-provided fs_edit",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.implementations.vfs_filesystem.fs_edit",
        source_kind="matrx_vfs",
        is_active=True,
    )
    registry.load_from_definitions([pre_existing])
    entry = registry.get("fs_edit")
    assert entry is not None
    assert entry.description == "DB-provided fs_edit"


def test_registry_explicit_vfs_source_kind_routes_without_global() -> None:
    # source_kind=matrx_vfs forces routing even with the global toggle off, which
    # is the per-tool override path.
    tool_def = ToolDefinition(
        name="fs_read_forced",
        description="x",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.implementations.filesystem.fs_read",
        source_kind="matrx_vfs",
        is_active=True,
    )
    # We want to verify the routing decision fires, not that the import
    # succeeds (Phase E may be missing). Inspect after _apply_vfs_routing.
    ToolRegistry._apply_vfs_routing(tool_def)
    assert tool_def._routed_to_vfs is True
    assert tool_def.function_path == (
        "matrx_ai.tools.implementations.vfs_filesystem.fs_read"
    )
