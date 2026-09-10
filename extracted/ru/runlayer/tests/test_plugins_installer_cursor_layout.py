"""Tests for the Cursor plugin layout: copy-into-``local/`` and legacy links."""

from __future__ import annotations

import datetime
import os
from pathlib import Path

import pytest

from runlayer_cli.api import (
    PluginDetail,
    PluginSkillRef,
    SkillDetail,
    SkillFileDetail,
)
from runlayer_cli.plugins import installer as plugin_installer
from runlayer_cli.plugins import layouts as plugin_layouts
from runlayer_cli.plugins.installer import (
    PluginLockEntry,
    _write_plugin_lockfile,
    install_plugins,
    read_plugin_lockfile,
    resolve_plugin_dirs,
    update_plugins,
)
from runlayer_cli.plugins.layouts import CODEX_NATIVE_INSTALL_MODE
from tests.plugin_installer_helpers import (
    FakeClientSinglePlugin,
    lock_entry,
    plugin,
)


def _seed_pre_local_cursor_install(
    tmp_path: Path, *, with_editor_copy: bool = False
) -> tuple[Path, Path, Path, Path]:
    """A Cursor install from before the copy-into-``local/`` layout.

    Canonical dir under ``.agents/plugins``, a link one level above ``local/``
    (which Cursor never scanned), and a lock entry recorded as plain ``native``.
    ``with_editor_copy`` also plants a copy inside ``local/``.
    """
    canonical = tmp_path / ".agents" / "plugins"
    editor = tmp_path / ".cursor" / "plugins" / "local"
    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    plugin_dir = canonical / "my-plugin"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / ".installed").write_text("", encoding="utf-8")
    legacy = editor.parent / "my-plugin"
    legacy.parent.mkdir(parents=True)
    legacy.symlink_to(plugin_dir)
    _write_plugin_lockfile(
        lockfile, [lock_entry(client="cursor", install_mode="native")]
    )
    if with_editor_copy:
        installed = editor / "my-plugin"
        installed.mkdir(parents=True)
        (installed / ".mcp.json").write_text("{}", encoding="utf-8")
    return canonical, editor, lockfile, legacy


@pytest.mark.parametrize("global_install", [True, False])
def test_resolve_plugin_dirs_cursor_uses_local_subdir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, global_install: bool
):
    """Cursor only scans user-local plugins under `.cursor/plugins/local`."""
    home = tmp_path / "home"
    cwd = tmp_path / "project"
    monkeypatch.setattr(Path, "home", lambda: home)

    canonical, editor, lockfile = resolve_plugin_dirs("cursor", global_install, cwd)

    base = home if global_install else cwd
    assert editor == base / ".cursor" / "plugins" / "local"
    assert canonical == base / ".agents" / "plugins"
    assert lockfile == base / ".runlayer" / "plugin-lock.yml"


def _seed_canonical_plugin(canonical: Path, name: str = "my-plugin") -> Path:
    plugin_dir = canonical / name
    (plugin_dir / ".cursor-plugin").mkdir(parents=True)
    (plugin_dir / ".cursor-plugin" / "plugin.json").write_text('{"name": "my-plugin"}')
    (plugin_dir / ".mcp.json").write_text('{"mcpServers": {}}')
    (plugin_dir / ".installed").write_text("")
    return plugin_dir


def test_finalize_native_install_cursor_copies_real_files(tmp_path: Path):
    """Cursor rejects a link out of local/, so the install must be real files."""
    canonical, editor = tmp_path / "canonical", tmp_path / "editor" / "local"
    _seed_canonical_plugin(canonical)

    plugin_layouts.native_layout("cursor").finalize(canonical, editor, "my-plugin")

    dest = editor / "my-plugin"
    assert not dest.is_symlink()
    assert dest.is_dir()
    assert (dest / ".cursor-plugin" / "plugin.json").is_file()
    assert (dest / ".mcp.json").is_file()
    # Canonical is untouched and remains the source of truth.
    assert (canonical / "my-plugin" / ".mcp.json").is_file()


@pytest.mark.skipif(os.name == "nt", reason="POSIX file modes")
def test_cursor_copy_keeps_mcp_config_owner_only(tmp_path: Path):
    """Pins ``copy2`` mode preservation through the Cursor copy.

    That is why the copy needs no chmod of its own. The security property --
    that the key never lands world-readable -- is proven by the install-level
    tests, which write the canonical file for real.
    """
    canonical, editor = tmp_path / "canonical", tmp_path / "editor" / "local"
    plugin_dir = _seed_canonical_plugin(canonical)
    os.chmod(plugin_dir / ".mcp.json", 0o600)

    plugin_layouts.native_layout("cursor").finalize(canonical, editor, "my-plugin")

    mode = (editor / "my-plugin" / ".mcp.json").stat().st_mode & 0o777
    assert mode == 0o600


def test_cursor_copy_skips_links_inside_the_tree(tmp_path: Path):
    """A planted link must not pull foreign content into the editor copy."""
    canonical, editor = tmp_path / "canonical", tmp_path / "editor" / "local"
    plugin_dir = _seed_canonical_plugin(canonical)
    outsider = tmp_path / "outsider.txt"
    outsider.write_text("secret")
    (plugin_dir / "linked.txt").symlink_to(outsider)

    plugin_layouts.native_layout("cursor").finalize(canonical, editor, "my-plugin")

    assert not (editor / "my-plugin" / "linked.txt").exists()


def test_cursor_copy_replaces_a_stale_symlink_install(tmp_path: Path):
    """Upgrading over a pre-copy install must not leave the old link behind."""
    canonical, editor = tmp_path / "canonical", tmp_path / "editor" / "local"
    _seed_canonical_plugin(canonical)
    editor.mkdir(parents=True)
    (editor / "my-plugin").symlink_to(canonical / "my-plugin")

    plugin_layouts.native_layout("cursor").finalize(canonical, editor, "my-plugin")

    dest = editor / "my-plugin"
    assert not dest.is_symlink()
    assert (dest / ".mcp.json").is_file()


def test_cursor_install_clears_legacy_pre_local_link(tmp_path: Path):
    """Upgrading is enough to clear the link older CLIs left one level up."""
    canonical = tmp_path / "canonical"
    plugins_root = tmp_path / ".cursor" / "plugins"
    editor = plugins_root / "local"
    _seed_canonical_plugin(canonical)
    plugins_root.mkdir(parents=True)
    legacy = plugins_root / "my-plugin"
    legacy.symlink_to(canonical / "my-plugin")

    plugin_layouts.native_layout("cursor").finalize(canonical, editor, "my-plugin")

    assert not legacy.exists() and not legacy.is_symlink()
    assert (editor / "my-plugin" / ".mcp.json").is_file()


def test_cursor_install_clears_dangling_legacy_link(tmp_path: Path):
    """The stale link is usually dangling, since removal deleted canonical."""
    canonical = tmp_path / "canonical"
    plugins_root = tmp_path / ".cursor" / "plugins"
    editor = plugins_root / "local"
    _seed_canonical_plugin(canonical)
    plugins_root.mkdir(parents=True)
    legacy = plugins_root / "my-plugin"
    legacy.symlink_to(canonical / "gone")
    # Points into canonical but at a name we do not own.
    plugin_layouts._remove_legacy_cursor_link(canonical, editor, "my-plugin")
    assert legacy.is_symlink()

    legacy.unlink()
    legacy.symlink_to(canonical / "my-plugin")
    (canonical / "my-plugin").rename(canonical / "moved")
    plugin_layouts._remove_legacy_cursor_link(canonical, editor, "my-plugin")
    assert not legacy.is_symlink()


def test_legacy_cleanup_leaves_user_owned_content_alone(tmp_path: Path):
    """A real directory at the legacy path is the user's, not ours."""
    canonical = tmp_path / "canonical"
    plugins_root = tmp_path / ".cursor" / "plugins"
    editor = plugins_root / "local"
    _seed_canonical_plugin(canonical)
    user_dir = plugins_root / "my-plugin"
    (user_dir / ".cursor-plugin").mkdir(parents=True)
    (user_dir / "mine.txt").write_text("hand-written")

    plugin_layouts._remove_legacy_cursor_link(canonical, editor, "my-plugin")

    assert (user_dir / "mine.txt").read_text() == "hand-written"


def test_legacy_cleanup_leaves_links_pointing_elsewhere_alone(tmp_path: Path):
    """Only a link into our own canonical store is ours to remove."""
    canonical = tmp_path / "canonical"
    plugins_root = tmp_path / ".cursor" / "plugins"
    editor = plugins_root / "local"
    _seed_canonical_plugin(canonical)
    elsewhere = tmp_path / "somewhere-else"
    elsewhere.mkdir()
    plugins_root.mkdir(parents=True)
    legacy = plugins_root / "my-plugin"
    legacy.symlink_to(elsewhere)

    plugin_layouts._remove_legacy_cursor_link(canonical, editor, "my-plugin")

    assert legacy.is_symlink()


def test_legacy_cleanup_is_scoped_to_the_local_editor_dir(tmp_path: Path):
    """Other clients must never have a sibling directory cleaned."""
    canonical = tmp_path / "canonical"
    plugins_root = tmp_path / ".claude" / "plugins"
    _seed_canonical_plugin(canonical)
    plugins_root.mkdir(parents=True)
    sibling = plugins_root.parent / "my-plugin"
    sibling.symlink_to(canonical / "my-plugin")

    plugin_layouts._remove_legacy_cursor_link(canonical, plugins_root, "my-plugin")

    assert sibling.is_symlink()


# Kept with the Cursor tests: only Cursor has a migrating layout (Codex: ENG-6376).
@pytest.mark.parametrize(
    ("client", "install_mode", "expected"),
    [
        ("cursor", "native", True),
        ("cursor", "native_copy", False),
        ("cursor", "mcp_fallback", False),
        ("claude_code", "native", False),
        ("vscode", "native", False),
        # Plain `native` is a declared legacy mode for Codex, served as-is.
        ("codex", "native", False),
        ("codex", CODEX_NATIVE_INSTALL_MODE, False),
        ("windsurf", "mcp_fallback", False),
    ],
)
def test_layout_stale(client: str, install_mode: str, expected: bool):
    entry = lock_entry(client=client, install_mode=install_mode)
    assert plugin_installer._layout_stale(entry) is expected


def test_remove_native_entry_purges_unshared_canonical(tmp_path: Path):
    canonical, editor, _lockfile, legacy = _seed_pre_local_cursor_install(
        tmp_path, with_editor_copy=True
    )
    entry = lock_entry(client="cursor", install_mode="native")

    plugin_installer._remove_native_entry(
        entry, [], canonical, editor, install_scope="project", reinstalling=True
    )

    assert not (canonical / "my-plugin").exists()
    assert not legacy.is_symlink() and not legacy.exists()
    assert not (editor / "my-plugin").exists()


def test_remove_native_entry_keeps_canonical_shared_with_other_client(
    tmp_path: Path,
):
    canonical, editor, _lockfile, legacy = _seed_pre_local_cursor_install(
        tmp_path, with_editor_copy=True
    )
    entry = lock_entry(client="cursor", install_mode="native")
    other_client = lock_entry(client="claude_code", install_mode="native")

    plugin_installer._remove_native_entry(
        entry,
        [entry, other_client],
        canonical,
        editor,
        install_scope="project",
        reinstalling=True,
    )

    # Shared across clients, so the canonical tree stays put.
    assert (canonical / "my-plugin").is_dir()
    assert not legacy.is_symlink() and not legacy.exists()
    assert not (editor / "my-plugin").exists()


def test_remove_native_entry_ignores_the_entry_being_migrated(
    tmp_path: Path,
):
    """Same client and same id is this install, not another client's."""
    canonical, editor, _lockfile, legacy = _seed_pre_local_cursor_install(
        tmp_path, with_editor_copy=True
    )
    entry = lock_entry(client="cursor", install_mode="native")
    same_entry = lock_entry(client="cursor", install_mode="native")

    plugin_installer._remove_native_entry(
        entry,
        [entry, same_entry],
        canonical,
        editor,
        install_scope="project",
        reinstalling=True,
    )

    assert not (canonical / "my-plugin").exists()
    assert not legacy.is_symlink() and not legacy.exists()


@pytest.mark.asyncio
async def test_install_reinstalls_pre_local_cursor_layout(tmp_path: Path):
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)
    progress: list[tuple[str, str]] = []

    result = await install_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
        on_progress=lambda name, status: progress.append((name, status)),
    )

    assert result.installed == ["my-plugin"]
    assert result.skipped == []
    assert result.errors == []
    assert progress == [("my-plugin", "reinstalled")]
    installed = editor / "my-plugin"
    assert installed.is_dir() and not installed.is_symlink()
    assert (installed / ".cursor-plugin" / "plugin.json").is_file()
    assert not legacy.is_symlink() and not legacy.exists()
    entries = read_plugin_lockfile(lockfile)
    assert [(e.client, e.id, e.install_mode) for e in entries] == [
        ("cursor", "p1", "native_copy")
    ]


@pytest.mark.asyncio
async def test_install_skips_current_cursor_layout(tmp_path: Path):
    canonical = tmp_path / ".agents" / "plugins"
    editor = tmp_path / ".cursor" / "plugins" / "local"
    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    _write_plugin_lockfile(
        lockfile, [lock_entry(client="cursor", install_mode="native_copy")]
    )

    result = await install_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.skipped == ["my-plugin"]
    assert result.installed == []
    assert not (editor / "my-plugin").exists()


@pytest.mark.asyncio
async def test_install_dry_run_reports_pre_local_cursor_reinstall(tmp_path: Path):
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)
    progress: list[tuple[str, str]] = []

    result = await install_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
        dry_run=True,
        on_progress=lambda name, status: progress.append((name, status)),
    )

    assert result.installed == ["my-plugin"]
    assert progress == [("my-plugin", "would reinstall")]
    assert legacy.is_symlink()
    assert not (editor / "my-plugin").exists()
    assert read_plugin_lockfile(lockfile)[0].install_mode == "native"


class _FakeClientStaleReinstallFails(FakeClientSinglePlugin):
    """Namespace lists the stale plugin (whose skill fetch fails) plus a fresh one."""

    def list_plugins_detailed(
        self,
        namespace: str | None = None,
        *,
        filter: str = "created_by_me",
        query: str | None = None,
    ):
        return [
            plugin(skills=[PluginSkillRef(id="sk-boom", name="boom")]),
            plugin(id="p2", name="other-plugin"),
        ]

    def get_skill(self, skill_id: str) -> SkillDetail:
        if skill_id == "sk-boom":
            raise RuntimeError("skill fetch failed")
        return super().get_skill(skill_id)


class _FakeClientStaleReinstallFileFetchFails(_FakeClientStaleReinstallFails):
    """The skill lists fine; one of its files is what fails to download."""

    def get_skill(self, skill_id: str) -> SkillDetail:
        return FakeClientSinglePlugin.get_skill(self, skill_id)

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        if skill_id == "sk-boom":
            raise RuntimeError("skill file fetch failed")
        return super().get_skill_file(skill_id, file_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "failing_client",
    [_FakeClientStaleReinstallFails, _FakeClientStaleReinstallFileFetchFails],
    ids=["skill_list_fails", "skill_file_fails"],
)
async def test_install_failed_cursor_reinstall_keeps_stale_install(
    tmp_path: Path,
    failing_client: type[_FakeClientStaleReinstallFails],
):
    """Content is fetched before anything is destroyed, so a failure changes nothing."""
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)

    result = await install_plugins(
        client=failing_client(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.installed == ["other-plugin"]
    assert len(result.errors) == 1 and result.errors[0].startswith("my-plugin:")
    entries = {(e.id, e.install_mode) for e in read_plugin_lockfile(lockfile)}
    # The stale entry survives the failed reinstall, so the next add retries it.
    assert entries == {("p1", "native"), ("p2", "native_copy")}
    # ... and so do its files, so the entry never points at a cleaned tree.
    assert (canonical / "my-plugin" / ".installed").is_file()
    assert legacy.is_symlink()


@pytest.mark.asyncio
async def test_install_cursor_reinstall_keeps_canonical_shared_with_other_client(
    tmp_path: Path,
):
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)
    other_manifest = canonical / "my-plugin" / ".claude-plugin" / "plugin.json"
    other_manifest.parent.mkdir()
    other_manifest.write_text("{}", encoding="utf-8")
    stale_skill = canonical / "my-plugin" / "skills" / "old-skill" / "SKILL.md"
    stale_skill.parent.mkdir(parents=True)
    stale_skill.write_text("# old", encoding="utf-8")
    _write_plugin_lockfile(
        lockfile,
        [
            lock_entry(client="cursor", install_mode="native"),
            lock_entry(client="claude_code", install_mode="native"),
        ],
    )

    result = await install_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.installed == ["my-plugin"]
    assert result.errors == []
    assert other_manifest.is_file()
    # The reinstall owns `skills/`, so content dropped upstream goes with it
    # even though the tree itself is kept for the other client.
    assert not (canonical / "my-plugin" / "skills").exists()
    assert (editor / "my-plugin" / ".cursor-plugin" / "plugin.json").is_file()
    assert not legacy.is_symlink()
    entries = sorted((e.client, e.install_mode) for e in read_plugin_lockfile(lockfile))
    assert entries == [("claude_code", "native"), ("cursor", "native_copy")]


@pytest.mark.asyncio
async def test_install_cursor_reinstall_purges_unshared_canonical(tmp_path: Path):
    """Nothing else claims the name, so the canonical tree is rebuilt clean."""
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)
    stale_skill = canonical / "my-plugin" / "skills" / "old-skill" / "SKILL.md"
    stale_skill.parent.mkdir(parents=True)
    stale_skill.write_text("# old", encoding="utf-8")

    result = await install_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.installed == ["my-plugin"]
    assert result.errors == []
    assert not stale_skill.exists()
    assert not (canonical / "my-plugin" / "skills").exists()
    assert (canonical / "my-plugin" / ".cursor-plugin" / "plugin.json").is_file()
    assert (editor / "my-plugin" / ".cursor-plugin" / "plugin.json").is_file()
    assert not legacy.is_symlink() and not legacy.exists()


@pytest.mark.skipif(os.name == "nt", reason="POSIX file modes")
@pytest.mark.asyncio
async def test_install_cursor_global_keeps_api_key_files_owner_only(tmp_path: Path):
    canonical = tmp_path / "global" / ".agents" / "plugins"
    editor = tmp_path / "global" / ".cursor" / "plugins" / "local"
    lockfile = tmp_path / "global" / ".runlayer" / "plugin-lock.yml"

    result = await install_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
        secret="rl_secret",
    )

    assert result.installed == ["my-plugin"]
    assert (editor / "my-plugin" / ".cursor-plugin" / "plugin.json").is_file()
    for mcp_path in (
        canonical / "my-plugin" / ".mcp.json",
        editor / "my-plugin" / ".mcp.json",
    ):
        assert "rl_secret" in mcp_path.read_text()
        assert mcp_path.stat().st_mode & 0o777 == 0o600

    # Project scope never embeds the key: those files live inside a git repo.
    # Checked on Claude Code because Cursor refuses a project-scope install.
    project_canonical = tmp_path / "project" / ".agents" / "plugins"
    project_editor = tmp_path / "project" / ".claude" / "plugins"
    project_result = await install_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        source="org/repo",
        install_all=False,
        plugin_name=None,
        canonical_dir=project_canonical,
        editor_dir=project_editor,
        lockfile_path=tmp_path / "project" / ".runlayer" / "plugin-lock.yml",
        client_name="claude_code",
        host="https://example.com",
        install_scope="project",
        secret="rl_secret",
    )

    assert project_result.installed == ["my-plugin"]
    for mcp_path in (
        project_canonical / "my-plugin" / ".mcp.json",
        project_editor / "my-plugin" / ".mcp.json",
    ):
        assert "rl_secret" not in mcp_path.read_text()
        assert mcp_path.stat().st_mode & 0o777 == 0o600


@pytest.mark.asyncio
async def test_update_migrates_pre_local_cursor_layout_with_same_timestamp(
    tmp_path: Path,
):
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)

    result = await update_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.updated == ["my-plugin"]
    assert result.up_to_date == []
    assert result.errors == []
    installed = editor / "my-plugin"
    assert installed.is_dir() and not installed.is_symlink()
    assert (installed / ".cursor-plugin" / "plugin.json").is_file()
    assert not legacy.is_symlink() and not legacy.exists()
    assert read_plugin_lockfile(lockfile)[0].install_mode == "native_copy"

    second_result = await update_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert second_result.updated == []
    assert second_result.up_to_date == ["my-plugin"]


@pytest.mark.asyncio
async def test_update_cursor_reinstall_keeps_canonical_shared_with_other_client(
    tmp_path: Path,
):
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)
    other_manifest = canonical / "my-plugin" / ".claude-plugin" / "plugin.json"
    other_manifest.parent.mkdir()
    other_manifest.write_text("{}", encoding="utf-8")
    _write_plugin_lockfile(
        lockfile,
        [
            lock_entry(client="cursor", install_mode="native"),
            lock_entry(client="claude_code", install_mode="native"),
        ],
    )

    result = await update_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.updated == ["my-plugin"]
    assert result.errors == []
    assert other_manifest.is_file()
    assert (editor / "my-plugin" / ".cursor-plugin" / "plugin.json").is_file()
    assert not legacy.is_symlink() and not legacy.exists()
    entries = sorted((e.client, e.install_mode) for e in read_plugin_lockfile(lockfile))
    assert entries == [("claude_code", "native"), ("cursor", "native_copy")]

    second_result = await update_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert second_result.updated == []
    assert second_result.up_to_date == ["my-plugin"]


@pytest.mark.asyncio
async def test_update_cursor_reinstall_purges_unshared_canonical(tmp_path: Path):
    canonical, editor, lockfile, legacy = _seed_pre_local_cursor_install(tmp_path)
    stale_skill = canonical / "my-plugin" / "skills" / "old-skill" / "SKILL.md"
    stale_skill.parent.mkdir(parents=True)
    stale_skill.write_text("# old", encoding="utf-8")

    result = await update_plugins(
        client=FakeClientSinglePlugin(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.updated == ["my-plugin"]
    assert result.errors == []
    assert not stale_skill.exists()
    assert not (canonical / "my-plugin" / "skills").exists()
    assert (editor / "my-plugin" / ".cursor-plugin" / "plugin.json").is_file()
    assert not legacy.is_symlink() and not legacy.exists()


class _FakeClientStaleUpdateFails(FakeClientSinglePlugin):
    """The stale plugin's skill fetch fails; a second, newer plugin updates fine."""

    def get_plugin(self, plugin_id: str) -> PluginDetail:
        if plugin_id == "p1":
            return plugin(skills=[PluginSkillRef(id="sk-boom", name="boom")])
        return plugin(
            id="p2",
            name="other-plugin",
            updated_at=datetime.datetime(2024, 2, 1, tzinfo=datetime.timezone.utc),
        )

    def get_skill(self, skill_id: str) -> SkillDetail:
        if skill_id == "sk-boom":
            raise RuntimeError("skill fetch failed")
        return super().get_skill(skill_id)


@pytest.mark.asyncio
async def test_update_failed_cursor_reinstall_keeps_stale_lock_entry(tmp_path: Path):
    canonical, editor, lockfile, _legacy = _seed_pre_local_cursor_install(tmp_path)
    _write_plugin_lockfile(
        lockfile,
        [
            lock_entry(client="cursor", install_mode="native"),
            PluginLockEntry(
                name="other-plugin",
                id="p2",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="cursor",
                install_mode="native_copy",
                server_ids=["srv-1"],
            ),
        ],
    )

    result = await update_plugins(
        client=_FakeClientStaleUpdateFails(),  # type: ignore
        plugin_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="cursor",
        host="https://example.com",
        install_scope="global",
    )

    assert result.updated == ["other-plugin"]
    assert len(result.errors) == 1 and result.errors[0].startswith("my-plugin:")

    entries = {e.id: e for e in read_plugin_lockfile(lockfile)}
    # Still plain `native`, so the next add/update retries the migration.
    assert entries["p1"].install_mode == "native"
    assert entries["p1"].updated_at == datetime.datetime(
        2024, 1, 1, tzinfo=datetime.timezone.utc
    )
    assert entries["p2"].install_mode == "native_copy"
    assert entries["p2"].updated_at == datetime.datetime(
        2024, 2, 1, tzinfo=datetime.timezone.utc
    )
    assert (editor / "other-plugin" / ".cursor-plugin" / "plugin.json").is_file()
