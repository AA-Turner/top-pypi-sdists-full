"""Tests for the anyio-free skills installer core (fs + lockfile primitives)."""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest
from pydantic import BaseModel

from runlayer_cli.skills.installer_core import (
    _COPY_STAGING_INFIX,
    INSTALLED_MARKER,
    LockEntry,
    _remove_skill_files,
    _sanitize_name,
    _symlink_skill,
    _write_lockfile,
    _write_skill_files,
    link_or_copy_skill_dir,
    read_lock_entries,
    read_lockfile,
    write_lock_entries,
)


class _FilePayload:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class TestSanitizeName:
    @pytest.mark.parametrize(
        "name",
        ["", "/abs", "../up", "a/../b", ".", "with\\backslash"],
    )
    def test_rejects_unsafe(self, name: str):
        with pytest.raises(ValueError):
            _sanitize_name(name)

    def test_accepts_plain_name(self):
        assert _sanitize_name("my-skill") == "my-skill"


class TestLockfileRoundtrip:
    def test_roundtrip(self, tmp_path: Path):
        path = tmp_path / ".runlayer" / "skill-lock.yml"
        entries = [
            LockEntry(name="a", id="s1", identifier="i1", client="cursor"),
            LockEntry(name="b", id="s2"),
        ]
        _write_lockfile(path, entries)
        assert read_lockfile(path) == entries

    def test_missing_file_is_empty(self, tmp_path: Path):
        assert read_lockfile(tmp_path / "nope.yml") == []

    def test_legacy_entry_defaults_client(self, tmp_path: Path):
        path = tmp_path / "skill-lock.yml"
        path.write_text("skills:\n- name: a\n  id: s1\n", encoding="utf-8")
        [entry] = read_lockfile(path)
        assert entry.client == "claude_code"

    def test_corrupt_yaml_raises(self, tmp_path: Path):
        path = tmp_path / "skill-lock.yml"
        path.write_text("skills: [unclosed", encoding="utf-8")
        with pytest.raises(ValueError, match="invalid lockfile YAML"):
            read_lockfile(path)

    def test_non_list_skills_raises(self, tmp_path: Path):
        path = tmp_path / "skill-lock.yml"
        path.write_text("skills: 42\n", encoding="utf-8")
        with pytest.raises(ValueError, match="must be a list"):
            read_lockfile(path)

    def test_non_mapping_entry_raises(self, tmp_path: Path):
        path = tmp_path / "skill-lock.yml"
        path.write_text("skills:\n- just-a-string\n", encoding="utf-8")
        with pytest.raises(ValueError, match="expected mapping"):
            read_lockfile(path)


class _MiniEntry(BaseModel):
    name: str


class TestGenericLockEntries:
    def test_custom_model_roundtrip_with_header(self, tmp_path: Path):
        path = tmp_path / "lock.yml"
        write_lock_entries(path, [_MiniEntry(name="x")], header="test harness")
        assert path.read_text(encoding="utf-8").startswith("# managed by: test harness")
        assert read_lock_entries(path, _MiniEntry) == [_MiniEntry(name="x")]

    def test_preprocess_hook_applied(self, tmp_path: Path):
        path = tmp_path / "lock.yml"
        path.write_text("skills:\n- {}\n", encoding="utf-8")
        entries = read_lock_entries(
            path, _MiniEntry, preprocess=lambda item: {**item, "name": "filled"}
        )
        assert entries == [_MiniEntry(name="filled")]

    def test_write_leaves_no_tmp_files(self, tmp_path: Path):
        path = tmp_path / "lock.yml"
        write_lock_entries(path, [_MiniEntry(name="x")], header="h")
        leftovers = [p for p in tmp_path.iterdir() if p.name != "lock.yml"]
        assert leftovers == []


class TestWriteSkillFiles:
    def test_writes_marker_and_files(self, tmp_path: Path):
        _write_skill_files(
            tmp_path,
            "my-skill",
            [
                _FilePayload("reference.md", "# ref"),
                _FilePayload("scripts/run.py", "print('hi')"),
            ],
        )
        skill_dir = tmp_path / "my-skill"
        assert (skill_dir / INSTALLED_MARKER).exists()
        assert (skill_dir / "reference.md").read_text() == "# ref"
        assert (skill_dir / "scripts" / "run.py").read_text() == "print('hi')"

    def test_rewrites_skill_md_frontmatter_name(self, tmp_path: Path):
        _write_skill_files(
            tmp_path,
            "installed-name",
            [_FilePayload("SKILL.md", "---\nname: upstream\n---\nbody")],
        )
        content = (tmp_path / "installed-name" / "SKILL.md").read_text()
        assert "name: installed-name" in content
        assert "name: upstream" not in content

    def test_rejects_traversal_skill_name(self, tmp_path: Path):
        with pytest.raises(ValueError):
            _write_skill_files(tmp_path, "../evil", [])

    def test_rejects_traversal_file_title(self, tmp_path: Path):
        with pytest.raises(ValueError):
            _write_skill_files(tmp_path, "ok", [_FilePayload("../../escape.md", "x")])


class TestSymlinkSkill:
    def _seed(self, tmp_path: Path) -> tuple[Path, Path]:
        canonical = tmp_path / "canonical"
        editor = tmp_path / "editor"
        (canonical / "my-skill").mkdir(parents=True)
        (canonical / "my-skill" / "SKILL.md").write_text("# hi", encoding="utf-8")
        return canonical, editor

    def test_creates_relative_symlink(self, tmp_path: Path):
        canonical, editor = self._seed(tmp_path)
        _symlink_skill(canonical, editor, "my-skill")
        dest = editor / "my-skill"
        assert dest.is_symlink()
        assert not os.path.isabs(os.readlink(dest))
        assert (dest / "SKILL.md").read_text() == "# hi"

    def test_replaces_stale_symlink(self, tmp_path: Path):
        canonical, editor = self._seed(tmp_path)
        editor.mkdir()
        (editor / "my-skill").symlink_to(tmp_path / "elsewhere")
        _symlink_skill(canonical, editor, "my-skill")
        assert (editor / "my-skill" / "SKILL.md").read_text() == "# hi"

    def test_replaces_real_dir_at_dest(self, tmp_path: Path):
        canonical, editor = self._seed(tmp_path)
        (editor / "my-skill").mkdir(parents=True)
        (editor / "my-skill" / "old.md").write_text("old", encoding="utf-8")
        _symlink_skill(canonical, editor, "my-skill")
        dest = editor / "my-skill"
        assert dest.is_symlink()
        assert not (dest / "old.md").exists()

    def test_same_dir_is_noop(self, tmp_path: Path):
        canonical, _ = self._seed(tmp_path)
        _symlink_skill(canonical, canonical, "my-skill")
        assert not (canonical / "my-skill").is_symlink()


class TestRemoveSkillFiles:
    def _seed(self, tmp_path: Path) -> tuple[Path, Path]:
        canonical = tmp_path / "canonical"
        editor = tmp_path / "editor"
        (canonical / "my-skill").mkdir(parents=True)
        editor.mkdir()
        (editor / "my-skill").symlink_to(canonical / "my-skill")
        return canonical, editor

    def test_removes_canonical_and_link(self, tmp_path: Path):
        canonical, editor = self._seed(tmp_path)
        _remove_skill_files(canonical, editor, "my-skill")
        assert not (canonical / "my-skill").exists()
        assert not (editor / "my-skill").is_symlink()

    def test_keep_canonical_removes_only_link(self, tmp_path: Path):
        canonical, editor = self._seed(tmp_path)
        _remove_skill_files(canonical, editor, "my-skill", remove_canonical=False)
        assert (canonical / "my-skill").exists()
        assert not (editor / "my-skill").is_symlink()

    def test_removes_copy_mode_dir_at_editor_path(self, tmp_path: Path):
        canonical, editor = self._seed(tmp_path)
        (editor / "my-skill").unlink()
        (editor / "my-skill").mkdir()
        _remove_skill_files(canonical, editor, "my-skill")
        assert not (editor / "my-skill").exists()

    def test_same_dir_removes_once(self, tmp_path: Path):
        canonical = tmp_path / "canonical"
        (canonical / "my-skill").mkdir(parents=True)
        _remove_skill_files(canonical, canonical, "my-skill")
        assert not (canonical / "my-skill").exists()


class TestLinkOrCopySkillDir:
    def _seed(self, tmp_path: Path) -> tuple[Path, Path]:
        src = tmp_path / "canonical" / "my-skill"
        src.mkdir(parents=True)
        (src / "SKILL.md").write_text("# hi", encoding="utf-8")
        dest_parent = tmp_path / "editor"
        dest_parent.mkdir()
        return src, dest_parent / "my-skill"

    def _break_symlinks(self, monkeypatch: pytest.MonkeyPatch):
        def _no_symlink(self, target, target_is_directory=False):
            raise OSError("symlink privilege not held")

        monkeypatch.setattr(Path, "symlink_to", _no_symlink)

    def test_symlink_success(self, tmp_path: Path):
        src, dest = self._seed(tmp_path)
        link_or_copy_skill_dir(src, dest)
        assert dest.is_symlink()
        assert (dest / "SKILL.md").read_text() == "# hi"

    def test_copy_fallback_when_symlink_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        src, dest = self._seed(tmp_path)
        self._break_symlinks(monkeypatch)
        link_or_copy_skill_dir(src, dest)
        assert dest.is_dir() and not dest.is_symlink()
        assert (dest / "SKILL.md").read_text() == "# hi"

    def test_copy_fallback_leaves_no_staging(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        src, dest = self._seed(tmp_path)
        self._break_symlinks(monkeypatch)
        link_or_copy_skill_dir(src, dest)
        leftovers = [p for p in dest.parent.iterdir() if p.name != dest.name]
        assert leftovers == []

    def test_crashed_staging_leftover_cleared(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        src, dest = self._seed(tmp_path)
        stale = dest.parent / f".{dest.name}{_COPY_STAGING_INFIX}dead"
        stale.mkdir()
        old = time.time() - 7200
        os.utime(stale, (old, old))
        self._break_symlinks(monkeypatch)
        link_or_copy_skill_dir(src, dest)
        assert not stale.exists()
        assert (dest / "SKILL.md").read_text() == "# hi"

    def test_recent_staging_sibling_left_alone(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # A young sibling may be a live concurrent run's in-flight copy.
        src, dest = self._seed(tmp_path)
        live = dest.parent / f".{dest.name}{_COPY_STAGING_INFIX}live"
        live.mkdir()
        self._break_symlinks(monkeypatch)
        link_or_copy_skill_dir(src, dest)
        assert live.exists()

    def test_symlink_skill_copies_when_symlink_fails(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        canonical = tmp_path / "canonical"
        editor = tmp_path / "editor"
        (canonical / "my-skill").mkdir(parents=True)
        (canonical / "my-skill" / "SKILL.md").write_text("# hi", encoding="utf-8")
        self._break_symlinks(monkeypatch)
        _symlink_skill(canonical, editor, "my-skill")
        dest = editor / "my-skill"
        assert dest.is_dir() and not dest.is_symlink()
        assert (dest / "SKILL.md").read_text() == "# hi"
