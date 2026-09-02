"""Tests for agentic_devtools.skill_injector._plan_skills_kind."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.skill_injector import _generate_readme, _plan_skills_kind


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _manifest(target_dir: Path, *entries: str) -> None:
    files = [(entry, "desc") for entry in entries]
    _write(target_dir / "agdt.README.md", _generate_readme(files, "skills"))


class TestPlanSkillsKind:
    """Tests for the _plan_skills_kind planning helper."""

    def test_missing_target_dir_yields_only_adds(self, tmp_path: Path) -> None:
        """Every source file is an add when the target directory does not exist."""
        src = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "body")
        plan = _plan_skills_kind(tmp_path / ".agents" / "skills", {"my-skill/SKILL.md": src})
        assert plan.kind == "skills"
        assert plan.added == ("my-skill/SKILL.md",)
        assert plan.overwritten == ()
        assert plan.deleted == ()

    def test_changed_bytes_are_reported_as_overwrite(self, tmp_path: Path) -> None:
        """A mirrored file whose content changed is an overwrite."""
        src = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "new")
        target = tmp_path / "target"
        _write(target / "my-skill" / "SKILL.md", "old")
        plan = _plan_skills_kind(target, {"my-skill/SKILL.md": src})
        assert plan.overwritten == ("my-skill/SKILL.md",)

    def test_manifest_entries_absent_from_source_are_deletes(self, tmp_path: Path) -> None:
        """A previously-injected skill missing from the source set is stale."""
        target = tmp_path / "target"
        _write(target / "old-skill" / "SKILL.md", "old")
        _write(target / "old-skill" / "notes.md", "old notes")
        _manifest(target, "old-skill/SKILL.md", "old-skill/notes.md")
        plan = _plan_skills_kind(target, {})
        assert plan.deleted == ("old-skill/SKILL.md", "old-skill/notes.md")

    def test_manifest_entries_already_gone_are_not_deletes(self, tmp_path: Path) -> None:
        """A manifest entry with no file on disk is not planned for deletion."""
        target = tmp_path / "target"
        _manifest(target, "old-skill/SKILL.md")
        plan = _plan_skills_kind(target, {})
        assert plan.deleted == ()

    def test_consumer_authored_skills_are_never_deleted(self, tmp_path: Path) -> None:
        """A skill absent from the manifest is not managed and is left alone."""
        target = tmp_path / "target"
        _write(target / "user-skill" / "SKILL.md", "mine")
        _manifest(target)
        plan = _plan_skills_kind(target, {})
        assert plan.deleted == ()

    def test_symlinked_skill_directory_is_rejected(self, tmp_path: Path) -> None:
        """Planning fails when a managed skill directory is a symlink."""
        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "SKILL.md").write_text("outside", encoding="utf-8")

        target = tmp_path / "target"
        target.mkdir()
        link = target / "my-skill"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not supported on this platform")

        src = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "new")
        with pytest.raises(OSError, match="symlinked directory"):
            _plan_skills_kind(target, {"my-skill/SKILL.md": src})

    def test_manifest_symlinked_skill_directory_is_rejected(self, tmp_path: Path) -> None:
        """Deletion planning rejects a manifest entry that resolves through a symlink."""
        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "SKILL.md").write_text("outside", encoding="utf-8")

        target = tmp_path / "target"
        target.mkdir()
        link = target / "my-skill"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not supported on this platform")

        _manifest(target, "my-skill/SKILL.md")
        src = _write(tmp_path / "source" / "other-skill" / "SKILL.md", "new")
        with pytest.raises(OSError, match="symlinked directory"):
            _plan_skills_kind(target, {"other-skill/SKILL.md": src})

    def test_rejects_symlinked_target_dir(self, tmp_path: Path) -> None:
        """Planning fails when target_dir itself is a symlink."""
        real = tmp_path / "real"
        real.mkdir()
        link = tmp_path / "link"
        try:
            link.symlink_to(real, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not supported on this platform")

        src = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "x")
        with pytest.raises(OSError, match="symlinked component"):
            _plan_skills_kind(link, {"my-skill/SKILL.md": src})

    def test_rejects_symlinked_target_parent(self, tmp_path: Path) -> None:
        """Planning fails when the parent of target_dir is a symlink."""
        real = tmp_path / "real"
        real.mkdir()
        link = tmp_path / "link"
        try:
            link.symlink_to(real, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not supported on this platform")
        target = link / "skills"

        src = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "x")
        with pytest.raises(OSError, match="symlinked component"):
            _plan_skills_kind(target, {"my-skill/SKILL.md": src})

    def test_rejects_symlinked_manifest_file(self, tmp_path: Path) -> None:
        """Planning fails when the managed manifest is a symlink."""
        target = tmp_path / "target"
        target.mkdir()
        outside = tmp_path / "outside.md"
        outside.write_text("x", encoding="utf-8")
        manifest = target / "agdt.README.md"
        try:
            manifest.symlink_to(outside)
        except OSError:
            pytest.skip("symlink creation not supported on this platform")

        src = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "x")
        with pytest.raises(OSError, match="symlink"):
            _plan_skills_kind(target, {"my-skill/SKILL.md": src})

    def test_untrusted_manifest_is_rejected(self, tmp_path: Path) -> None:
        """Planning fails when agdt.README.md is not a managed manifest."""
        target = tmp_path / "target"
        target.mkdir()
        _write(
            target / "agdt.README.md",
            "| File | Description |\n| ---- | ----------- |\n| `my-skill/SKILL.md` | x |\n",
        )
        src = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "x")

        with pytest.raises(OSError, match="Refusing untrusted skills manifest"):
            _plan_skills_kind(target, {"my-skill/SKILL.md": src})

    def test_case_only_resource_rename_not_deleted_when_same_inode(self, tmp_path: Path) -> None:
        """Old-cased entry is suppressed from deletion when both spellings share one inode.

        On a case-insensitive filesystem a resource renamed from ``Guide.md`` to
        ``guide.md`` resolves to the same inode.  The stale-deletion plan must not
        schedule the old spelling for deletion in that situation.
        """
        target = tmp_path / "target"
        _write(target / "my-skill" / "SKILL.md", "skill body")
        guide_old = _write(target / "my-skill" / "Guide.md", "guide body")
        _manifest(target, "my-skill/SKILL.md", "my-skill/Guide.md")

        src_skill = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "skill body")
        src_guide = _write(tmp_path / "source" / "my-skill" / "guide.md", "guide body")

        # Simulate a case-insensitive filesystem by hard-linking both spellings
        # to the same inode so stat() returns identical st_ino / st_dev values.
        guide_new = target / "my-skill" / "guide.md"
        try:
            guide_new.hardlink_to(guide_old)
        except OSError:
            pytest.skip("hard links not supported on this platform")

        plan = _plan_skills_kind(target, {"my-skill/SKILL.md": src_skill, "my-skill/guide.md": src_guide})

        assert "my-skill/Guide.md" not in plan.deleted

    def test_case_variant_with_distinct_inode_remains_a_deletion_candidate(self, tmp_path: Path) -> None:
        """Old-cased entry is still planned for deletion when inodes differ.

        On a case-sensitive filesystem ``Guide.md`` and ``guide.md`` are two
        separate files with distinct inodes, so the old spelling must remain a
        deletion candidate even though the new source uses lowercase.
        """
        target = tmp_path / "target"
        _write(target / "my-skill" / "SKILL.md", "skill body")
        _write(target / "my-skill" / "Guide.md", "old guide")
        _write(target / "my-skill" / "guide.md", "new guide")  # distinct inode
        _manifest(target, "my-skill/SKILL.md", "my-skill/Guide.md")

        src_skill = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "skill body")
        src_guide = _write(tmp_path / "source" / "my-skill" / "guide.md", "new guide")

        plan = _plan_skills_kind(target, {"my-skill/SKILL.md": src_skill, "my-skill/guide.md": src_guide})

        assert "my-skill/Guide.md" in plan.deleted

    def test_case_variant_new_spelling_absent_falls_through_to_deletion(self, tmp_path: Path) -> None:
        """Old-cased entry is deleted when the new spelling has no target-side file.

        On a case-sensitive filesystem the new lowercase path may not exist in the
        target directory yet (first-ever injection of the renamed resource).  In
        that case ``stat()`` on the new spelling raises ``OSError``, the exception
        is caught, and the old entry remains a deletion candidate.
        """
        target = tmp_path / "target"
        _write(target / "my-skill" / "SKILL.md", "skill body")
        _write(target / "my-skill" / "Guide.md", "old guide")
        # guide.md is NOT written to target — simulates the absent-new-path scenario.
        _manifest(target, "my-skill/SKILL.md", "my-skill/Guide.md")

        src_skill = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "skill body")
        src_guide = _write(tmp_path / "source" / "my-skill" / "guide.md", "new guide")

        plan = _plan_skills_kind(target, {"my-skill/SKILL.md": src_skill, "my-skill/guide.md": src_guide})

        assert "my-skill/Guide.md" in plan.deleted

    def test_case_only_rename_populates_case_renames(self, tmp_path: Path) -> None:
        """case_renames is populated with (old, new) when same-inode case rename detected."""
        target = tmp_path / "target"
        _write(target / "my-skill" / "SKILL.md", "skill body")
        guide_old = _write(target / "my-skill" / "Guide.md", "guide body")
        _manifest(target, "my-skill/SKILL.md", "my-skill/Guide.md")

        src_skill = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "skill body")
        src_guide = _write(tmp_path / "source" / "my-skill" / "guide.md", "guide body")

        guide_new = target / "my-skill" / "guide.md"
        try:
            guide_new.hardlink_to(guide_old)
        except OSError:
            pytest.skip("hard links not supported on this platform")

        plan = _plan_skills_kind(target, {"my-skill/SKILL.md": src_skill, "my-skill/guide.md": src_guide})

        assert ("my-skill/Guide.md", "my-skill/guide.md") in plan.case_renames
        assert "my-skill/Guide.md" not in plan.deleted

    def test_no_case_renames_when_no_same_inode(self, tmp_path: Path) -> None:
        """case_renames is empty when there are no case-rename pairs."""
        target = tmp_path / "target"
        _write(target / "my-skill" / "SKILL.md", "skill body")
        _manifest(target, "my-skill/SKILL.md")

        src_skill = _write(tmp_path / "source" / "my-skill" / "SKILL.md", "skill body")
        plan = _plan_skills_kind(target, {"my-skill/SKILL.md": src_skill})

        assert plan.case_renames == ()
