"""Consistency tests for the per-client native plugin layout table."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from runlayer_cli.api import PluginDetail
from runlayer_cli.plugins import layouts as plugin_layouts
from runlayer_cli.plugins.installer import _plugin_install_name, resolve_plugin_dirs
from runlayer_cli.plugins.layouts import (
    CODEX_NATIVE_INSTALL_MODE,
    CURSOR_NATIVE_INSTALL_MODE,
    NATIVE_INSTALL_MODES,
    NATIVE_LAYOUTS,
    cleanup_native_install,
    native_layout,
    project_scope_unsupported_reason,
)
from runlayer_cli.scan.clients import get_client_by_name

CLIENTS = sorted(NATIVE_LAYOUTS)
NON_CODEX_MODES = sorted(NATIVE_INSTALL_MODES - {CODEX_NATIVE_INSTALL_MODE})


@pytest.mark.parametrize(
    ("client", "install_mode"),
    [
        ("claude_code", "native"),
        ("vscode", "native"),
        ("codex", CODEX_NATIVE_INSTALL_MODE),
        ("cursor", CURSOR_NATIVE_INSTALL_MODE),
    ],
)
def test_install_mode(client: str, install_mode: str):
    assert native_layout(client).install_mode == install_mode
    assert install_mode in NATIVE_INSTALL_MODES


def test_native_install_modes_includes_plain_native():
    """A pre-`local/` Cursor entry is recorded as plain `native`."""
    assert "native" in NATIVE_INSTALL_MODES
    assert NATIVE_INSTALL_MODES == frozenset(
        {"native", CODEX_NATIVE_INSTALL_MODE, CURSOR_NATIVE_INSTALL_MODE}
    )


@pytest.mark.parametrize(
    ("client", "manifest_dir"),
    [
        ("claude_code", ".claude-plugin"),
        ("cursor", ".cursor-plugin"),
        ("vscode", ".vscode-plugin"),
        ("codex", ".codex-plugin"),
    ],
)
def test_manifest_dir(client: str, manifest_dir: str):
    assert native_layout(client).manifest_dir == manifest_dir


@pytest.mark.parametrize(
    ("client", "editor_rel"),
    [
        ("claude_code", ".claude/plugins"),
        ("cursor", ".cursor/plugins/local"),
        ("vscode", ".vscode/plugins"),
        # Codex loads the canonical tree through its marketplace record.
        ("codex", None),
    ],
)
def test_editor_dirs_are_the_same_in_both_scopes(client: str, editor_rel: str | None):
    layout = native_layout(client)
    assert layout.project_rel == editor_rel
    assert layout.global_rel == editor_rel


@pytest.mark.parametrize("client", CLIENTS)
def test_http_type_mcp_only_for_claude_code_and_vscode(client: str):
    expected = client in {"claude_code", "vscode"}
    assert native_layout(client).http_type_mcp is expected


@pytest.mark.parametrize("client", CLIENTS)
def test_skill_frontmatter_rewrite_only_for_claude_code_and_codex(client: str):
    expected = client in {"claude_code", "codex"}
    assert native_layout(client).rewrites_skill_frontmatter is expected


@pytest.mark.parametrize("client", CLIENTS)
def test_global_registration_hooks_only_for_claude_code(client: str):
    """Every other layout carries the no-ops, so callers never test for None."""
    layout = native_layout(client)
    expected = client == "claude_code"
    assert (
        layout.register_global is not plugin_layouts._no_register_global
    ) is expected
    assert (
        layout.unregister_global is not plugin_layouts._no_unregister_global
    ) is expected


def test_no_op_registration_hooks_touch_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """The defaults are safe to call unconditionally on a global install."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))
    layout = native_layout("cursor")

    layout.register_global(
        PluginDetail(id="p1", name="My Plugin"), tmp_path, "My Plugin"
    )
    layout.unregister_global("My Plugin")

    assert list(home.iterdir()) == []


@pytest.mark.parametrize(
    ("client", "expected"),
    [
        ("claude_code", "my-plugin"),
        ("codex", "my-plugin"),
        ("cursor", "My Plugin"),
        ("vscode", "My Plugin"),
    ],
)
def test_install_name_is_what_the_installer_writes(client: str, expected: str):
    """The table's name function is the one `plugins add` installs under."""
    assert native_layout(client).install_name("My Plugin") == expected
    assert _plugin_install_name(client, PluginDetail(id="p1", name="My Plugin")) == (
        expected
    )


@pytest.mark.parametrize("client", ["claude_code", "codex"])
def test_slug_error_names_the_client(client: str):
    """The slug label is the table's display name, not a second spelling."""
    label = native_layout(client).display_name
    with pytest.raises(ValueError, match=f"invalid {label} plugin or skill name"):
        native_layout(client).install_name("!!!")


@pytest.mark.parametrize("client", CLIENTS)
def test_display_name_matches_the_scan_client_registry(client: str):
    """The layout's user-facing name is the one the rest of the CLI shows."""
    client_def = get_client_by_name(client)
    assert client_def is not None
    assert native_layout(client).display_name == client_def.display_name


@pytest.mark.parametrize("client", CLIENTS)
def test_project_scope_is_unsupported_only_for_cursor(client: str):
    layout = native_layout(client)
    expected = client == "cursor"
    assert (layout.project_scope_unsupported_reason is not None) is expected


@pytest.mark.parametrize("client", CLIENTS)
def test_project_scope_unsupported_reason_matches_the_table(client: str):
    assert (
        project_scope_unsupported_reason(client)
        == native_layout(client).project_scope_unsupported_reason
    )


def test_project_scope_unsupported_reason_is_none_for_mcp_fallback_clients():
    assert project_scope_unsupported_reason("windsurf") is None


@pytest.mark.parametrize("client", CLIENTS)
def test_legacy_install_modes_only_for_codex(client: str):
    """Only Codex still serves a pre-current-layout mode as-is."""
    layout = native_layout(client)
    expected = frozenset({"native"}) if client == "codex" else frozenset()
    assert layout.legacy_install_modes == expected


@pytest.mark.parametrize("client", CLIENTS)
def test_current_install_mode_is_never_a_legacy_mode(client: str):
    layout = native_layout(client)
    assert layout.install_mode not in layout.legacy_install_modes


def test_native_layout_rejects_a_non_native_client():
    with pytest.raises(ValueError, match="unsupported native plugin client: windsurf"):
        native_layout("windsurf")


@pytest.mark.parametrize("client", CLIENTS)
@pytest.mark.parametrize("global_install", [True, False])
def test_resolve_plugin_dirs_follows_the_table(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    client: str,
    global_install: bool,
):
    home = tmp_path / "home"
    cwd = tmp_path / "project"
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))

    canonical, editor, lockfile = resolve_plugin_dirs(client, global_install, cwd)

    base = home if global_install else cwd
    layout = native_layout(client)
    editor_rel = layout.global_rel if global_install else layout.project_rel
    assert canonical == base / ".agents" / "plugins"
    # No editor-relative dir (Codex) means the client reads the canonical tree.
    assert editor == (canonical if editor_rel is None else base / editor_rel)
    assert lockfile == base / ".runlayer" / "plugin-lock.yml"


@pytest.mark.parametrize("install_mode", sorted(NATIVE_INSTALL_MODES))
def test_cleanup_accepts_every_recorded_install_mode(tmp_path: Path, install_mode: str):
    """Cleanup keys off the recorded mode, so every mode must reach a branch."""
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    canonical.mkdir()
    editor.mkdir()

    cleanup_native_install(canonical, editor, "my-plugin", install_mode)


def _seed_codex_marketplace(canonical: Path) -> Path:
    canonical.mkdir(parents=True, exist_ok=True)
    path = canonical / "marketplace.json"
    path.write_text(
        json.dumps({"name": "runlayer-local", "plugins": [{"name": "my-plugin"}]}),
        encoding="utf-8",
    )
    return path


def test_codex_cleanup_drops_the_marketplace_entry(tmp_path: Path):
    canonical = tmp_path / "canonical"
    marketplace = _seed_codex_marketplace(canonical)

    cleanup_native_install(canonical, canonical, "my-plugin", CODEX_NATIVE_INSTALL_MODE)

    assert json.loads(marketplace.read_text(encoding="utf-8"))["plugins"] == []


@pytest.mark.parametrize("install_mode", NON_CODEX_MODES)
def test_non_codex_cleanup_leaves_the_marketplace_entry(
    tmp_path: Path, install_mode: str
):
    canonical = tmp_path / "canonical"
    marketplace = _seed_codex_marketplace(canonical)

    cleanup_native_install(canonical, tmp_path / "editor", "my-plugin", install_mode)

    assert json.loads(marketplace.read_text(encoding="utf-8"))["plugins"] == [
        {"name": "my-plugin"}
    ]
