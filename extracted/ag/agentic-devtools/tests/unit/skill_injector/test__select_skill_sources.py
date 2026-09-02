"""Tests for agentic_devtools.skill_injector._select_skill_sources."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.skill_injector import _select_skill_sources


def _skill(source_dir: Path, name: str, frontmatter: str = "", body: str = "# Body") -> Path:
    skill_dir = source_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(f"{frontmatter}{body}\n", encoding="utf-8")
    return skill_dir


class TestSelectSkillSources:
    """Tests for the _select_skill_sources helper."""

    def test_entry_and_one_level_resources_are_selected(self, tmp_path: Path) -> None:
        """A skill contributes its SKILL.md and every non-hidden file beside it."""
        skill_dir = _skill(tmp_path, "my-skill")
        (skill_dir / "notes.md").write_text("# Notes", encoding="utf-8")
        (skill_dir / "usage guide.md").write_text("# Guide", encoding="utf-8")
        (skill_dir / ".hidden.md").write_text("hidden", encoding="utf-8")

        origins, fm_cache, pruned = _select_skill_sources(tmp_path, issue_adapter=None, code_hosting=None)

        assert set(origins) == {"my-skill/SKILL.md", "my-skill/notes.md", "my-skill/usage guide.md"}
        assert fm_cache == {}
        assert pruned == 0

    def test_directories_without_entry_file_and_loose_files_are_ignored(self, tmp_path: Path) -> None:
        """Only directories carrying a SKILL.md are skills; loose files are not."""
        (tmp_path / "not-a-skill").mkdir()
        (tmp_path / "not-a-skill" / "notes.md").write_text("x", encoding="utf-8")
        (tmp_path / ".hidden-skill").mkdir()
        (tmp_path / ".hidden-skill" / "SKILL.md").write_text("x", encoding="utf-8")
        (tmp_path / "README.md").write_text("tree readme", encoding="utf-8")

        origins, _fm_cache, pruned = _select_skill_sources(tmp_path, issue_adapter=None, code_hosting=None)

        assert origins == {}
        assert pruned == 0

    def test_names_are_mirrored_verbatim_and_never_flattened(self, tmp_path: Path) -> None:
        """The destination path keeps the skill directory — no dotted flat name."""
        _skill(tmp_path, "run-targeted-checks")

        origins, _fm_cache, _pruned = _select_skill_sources(tmp_path, issue_adapter=None, code_hosting=None)

        assert list(origins) == ["run-targeted-checks/SKILL.md"]
        assert all("." not in Path(rel).parts[0] for rel in origins)

    def test_classification_prunes_whole_skill(self, tmp_path: Path) -> None:
        """A skill whose required axis does not match is pruned with its resources."""
        jira_only = _skill(
            tmp_path,
            "jira-only",
            frontmatter="---\ndescription: Jira\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
        )
        (jira_only / "extra.md").write_text("resource", encoding="utf-8")
        _skill(tmp_path, "universal", frontmatter="---\ndescription: Any\n---\n")

        origins, fm_cache, pruned = _select_skill_sources(tmp_path, issue_adapter="github", code_hosting=None)

        assert set(origins) == {"universal/SKILL.md"}
        assert pruned == 1
        assert list(fm_cache) == [tmp_path / "universal" / "SKILL.md"]

    def test_non_utf8_entry_file_is_kept_without_cached_frontmatter(self, tmp_path: Path) -> None:
        """A SKILL.md that cannot be decoded is kept for the copy phase to report."""
        skill_dir = tmp_path / "binary-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_bytes(b"\xff\xfe not utf-8")

        origins, fm_cache, pruned = _select_skill_sources(tmp_path, issue_adapter="github", code_hosting="github")

        assert set(origins) == {"binary-skill/SKILL.md"}
        assert fm_cache == {}
        assert pruned == 0

    def test_case_fold_resource_collision_prunes_whole_skill(self, tmp_path: Path) -> None:
        """A skill with case-only differing resource names is pruned as ambiguous.

        ``Guide.md`` and ``guide.md`` in the same skill directory resolve to the
        same destination on a case-insensitive filesystem.  The whole skill is
        skipped to prevent silent data loss.
        """
        import warnings

        skill_dir = tmp_path / "ambiguous-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Ambiguous", encoding="utf-8")
        (skill_dir / "Guide.md").write_text("# Upper", encoding="utf-8")
        (skill_dir / "guide.md").write_text("# Lower", encoding="utf-8")
        _skill(tmp_path, "clean-skill")

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            origins, fm_cache, pruned = _select_skill_sources(tmp_path, issue_adapter=None, code_hosting=None)

        assert set(origins) == {"clean-skill/SKILL.md"}
        assert pruned == 0
        assert any("ambiguous-skill" in str(w.message) and issubclass(w.category, RuntimeWarning) for w in caught)

    def test_single_resource_no_collision_is_not_pruned(self, tmp_path: Path) -> None:
        """A skill with only one resource is never pruned for case-fold collision."""
        skill_dir = _skill(tmp_path, "solo-skill")
        (skill_dir / "guide.md").write_text("only resource", encoding="utf-8")

        origins, _fm_cache, pruned = _select_skill_sources(tmp_path, issue_adapter=None, code_hosting=None)

        assert "solo-skill/guide.md" in origins
        assert pruned == 0

    def test_resource_case_colliding_with_skill_entry_skips_skill(self, tmp_path: Path) -> None:
        """A resource named like SKILL.md (case-insensitive) is rejected."""
        import warnings

        skill_dir = _skill(tmp_path, "entry-collision")
        (skill_dir / "skill.md").write_text("# duplicate entry name", encoding="utf-8")
        _skill(tmp_path, "clean-skill")

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            origins, _fm_cache, pruned = _select_skill_sources(tmp_path, issue_adapter=None, code_hosting=None)

        assert set(origins) == {"clean-skill/SKILL.md"}
        assert pruned == 0
        assert any("entry-collision" in str(w.message) and "SKILL.md" in str(w.message) for w in caught)
