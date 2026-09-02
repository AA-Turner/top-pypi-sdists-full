"""Tests for agentic_devtools.skill_injector._plan_kind."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.skill_injector import _plan_kind


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


class TestPlanKind:
    """Tests for the _plan_kind planning helper."""

    def test_missing_target_dir_yields_only_adds(self, tmp_path: Path) -> None:
        """Every source file is an add when the target directory does not exist."""
        src = _write(tmp_path / "source" / "agdt.a.agent.md", "a")
        plan = _plan_kind("agents", tmp_path / ".github" / "agents", {"agdt.a.agent.md": src})
        assert plan == type(plan)(kind="agents", added=("agdt.a.agent.md",), overwritten=(), deleted=())

    def test_identical_bytes_are_neither_add_nor_overwrite(self, tmp_path: Path) -> None:
        """A target file with identical content is not reported at all."""
        src = _write(tmp_path / "source" / "agdt.a.agent.md", "same")
        target = tmp_path / "target"
        _write(target / "agdt.a.agent.md", "same")
        plan = _plan_kind("agents", target, {"agdt.a.agent.md": src})
        assert plan.added == ()
        assert plan.overwritten == ()
        assert plan.deleted == ()

    def test_different_bytes_are_reported_as_overwrite(self, tmp_path: Path) -> None:
        """A target file with different content is an overwrite."""
        src = _write(tmp_path / "source" / "agdt.a.agent.md", "new")
        target = tmp_path / "target"
        _write(target / "agdt.a.agent.md", "old")
        plan = _plan_kind("agents", target, {"agdt.a.agent.md": src})
        assert plan.overwritten == ("agdt.a.agent.md",)
        assert plan.added == ()

    def test_deletes_cover_managed_files_absent_from_source(self, tmp_path: Path) -> None:
        """Managed agdt.* files not in the source set are deletes."""
        target = tmp_path / "target"
        _write(target / "agdt.stale.agent.md", "stale")
        _write(target / "agdt.other.agent.md", "stale")
        plan = _plan_kind("agents", target, {})
        assert plan.deleted == ("agdt.other.agent.md", "agdt.stale.agent.md")

    def test_legacy_dot_agdt_directory_is_planned_as_delete(self, tmp_path: Path) -> None:
        """The legacy .agdt subdirectory is represented in the delete plan."""
        target = tmp_path / "target"
        (target / ".agdt").mkdir(parents=True)
        plan = _plan_kind("agents", target, {})
        assert plan.deleted == (".agdt/",)

    def test_case_variant_existing_file_is_stale_on_case_sensitive_fs(self, tmp_path: Path) -> None:
        """On case-sensitive filesystems, a case-only variant is planned for deletion.

        The inode check suppresses the delete only when both spellings resolve to
        the same file (case-insensitive filesystem).  On case-sensitive filesystems
        (Linux tmpfs/ext4) the candidate path does not exist, so stat() raises
        OSError and the variant is listed as stale.
        """
        src = _write(tmp_path / "source" / "agdt.foo.agent.md", "new")
        target = tmp_path / "target"
        _write(target / "agdt.Foo.agent.md", "old")
        # Detect actual filesystem behaviour rather than assuming platform.
        case_insensitive = (target / "agdt.foo.agent.md").exists()
        plan = _plan_kind("agents", target, {"agdt.foo.agent.md": src})
        if case_insensitive:
            # macOS/Windows: both spellings are the same file — not stale.
            assert "agdt.Foo.agent.md" not in plan.deleted
        else:
            # Linux: different files — the variant is stale.
            assert "agdt.Foo.agent.md" in plan.deleted

    def test_case_variant_suppressed_when_same_inode(self, tmp_path: Path) -> None:
        """A case-only variant is not stale when both spellings share the same inode.

        Hard-linking the two paths simulates what a case-insensitive filesystem
        does: both spellings resolve to the same physical file.  The inode check
        sees matching st_ino/st_dev and suppresses the deletion.
        """
        target = tmp_path / "target"
        target.mkdir(parents=True)
        canonical = target / "agdt.foo.agent.md"
        canonical.write_text("content", encoding="utf-8")
        variant = target / "agdt.Foo.agent.md"
        variant.hardlink_to(canonical)  # same inode → simulates case-insensitive FS
        src = _write(tmp_path / "source" / "agdt.foo.agent.md", "content")
        plan = _plan_kind("agents", target, {"agdt.foo.agent.md": src})
        assert "agdt.Foo.agent.md" not in plan.deleted

    def test_case_variant_is_stale_when_different_inodes(self, tmp_path: Path) -> None:
        """A case-only variant with a different inode is planned for deletion.

        When both spellings exist on the filesystem with different inodes the
        inode check finds no match and the variant is added to the delete list.
        Skipped on case-insensitive filesystems where the two spellings resolve
        to the same file.
        """
        target = tmp_path / "target"
        target.mkdir(parents=True)
        # Write both spellings as separate files (different inodes).
        (target / "agdt.foo.agent.md").write_text("source-content", encoding="utf-8")
        (target / "agdt.Foo.agent.md").write_text("variant-content", encoding="utf-8")
        # On a case-insensitive filesystem both writes go to the same file;
        # detecting that avoids a misleading assertion on macOS/Windows.
        if (target / "agdt.foo.agent.md").stat().st_ino == (target / "agdt.Foo.agent.md").stat().st_ino:
            pytest.skip("case-insensitive filesystem — variant cannot have a different inode")
        src = _write(tmp_path / "source" / "agdt.foo.agent.md", "source-content")
        plan = _plan_kind("agents", target, {"agdt.foo.agent.md": src})
        # agdt.Foo.agent.md has a different inode — not suppressed, listed as stale.
        assert "agdt.Foo.agent.md" in plan.deleted

    def test_manifest_unprefixed_files_and_dirs_are_never_deleted(self, tmp_path: Path) -> None:
        """The managed README, unprefixed files and subdirectories are left alone."""
        target = tmp_path / "target"
        _write(target / "agdt.README.md", "manifest")
        _write(target / "notes.md", "user file")
        (target / "agdt.subdir").mkdir()
        plan = _plan_kind("prompts", target, {})
        assert plan.deleted == ()
        assert plan.kind == "prompts"
