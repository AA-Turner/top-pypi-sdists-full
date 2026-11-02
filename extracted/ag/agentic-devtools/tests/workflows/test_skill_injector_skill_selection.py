"""End-to-end summary, planning, and execution scenarios for skill injection."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import inject_skills_with_summary
from agentic_devtools.skill_injector_markdown import _generate_readme
from agentic_devtools.skill_injector_models import InjectionSummary


class TestSkillInjectorWorkflow:
    @staticmethod
    def _skills_selector(skills_source):
        """Return a side_effect for _get_source_dir with only a skills source."""
        empty = skills_source.parent / "empty_source"
        empty.mkdir(exist_ok=True)

        def _select(kind):
            if kind == "skills":
                return skills_source
            return empty

        return _select

    @staticmethod
    def _write_skill(source: Path, name: str, frontmatter: str = "---\ndescription: A skill\n---\n") -> Path:
        skill_dir = source / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"{frontmatter}# {name}\n", encoding="utf-8")
        return skill_dir

    def test_skill_directory_and_nested_resource_survive_the_mirror(self, tmp_path) -> None:
        """A skill's directory, entry file and bundled resource are mirrored verbatim."""
        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "run-targeted-checks")
        (skill_dir / "reference.md").write_text("# Reference", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is True
        target = tmp_path / ".agents" / "skills" / "run-targeted-checks"
        assert (target / "SKILL.md").read_text(encoding="utf-8").endswith("# run-targeted-checks\n")
        assert (target / "reference.md").read_text(encoding="utf-8") == "# Reference"
        # One skill counted as one injected unit, resources not counted separately.
        assert summary.injected == 1

    def test_skill_names_are_never_flattened(self, tmp_path) -> None:
        """No mirrored skill directory name contains a dot."""
        source = tmp_path / "source_skills"
        self._write_skill(source, "write-github-commit-message")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            inject_skills_with_summary(tmp_path)

        target = tmp_path / ".agents" / "skills"
        mirrored = [p.name for p in target.iterdir() if p.is_dir()]
        assert mirrored == ["write-github-commit-message"]
        assert all("." not in name for name in mirrored)

    def test_skills_honour_the_classification_filter(self, tmp_path) -> None:
        """A skill requiring an axis the consumer does not match is not mirrored."""
        source = tmp_path / "source_skills"
        self._write_skill(
            source,
            "jira-only",
            frontmatter="---\ndescription: Jira\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
        )
        self._write_skill(source, "universal")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, summary = inject_skills_with_summary(tmp_path, issue_adapter="github", code_hosting="github")

        assert success is True
        target = tmp_path / ".agents" / "skills"
        assert (target / "universal" / "SKILL.md").exists()
        assert not (target / "jira-only").exists()
        assert summary == InjectionSummary(injected=1, pruned=1)

    def test_skill_deletions_are_gated_by_the_same_opt_in(self, tmp_path, capsys) -> None:
        """A retired skill is only removed with assume_yes, and its directory goes too."""
        source = tmp_path / "source_skills"
        source.mkdir()
        target = tmp_path / ".agents" / "skills"
        stale_dir = target / "retired-skill"
        stale_dir.mkdir(parents=True)
        (stale_dir / "SKILL.md").write_text("old", encoding="utf-8")
        (target / "agdt.README.md").write_text(
            _generate_readme([("retired-skill/SKILL.md", "Old")], "skills"),
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            blocked_success, blocked_summary = inject_skills_with_summary(tmp_path)

        assert blocked_success is False
        assert blocked_summary.deletions_blocked is True
        assert (stale_dir / "SKILL.md").exists()
        assert "- retired-skill/SKILL.md" in capsys.readouterr().err

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert not stale_dir.exists()

    def test_untrusted_skills_manifest_aborts_without_writes(self, tmp_path) -> None:
        """A pre-existing non-managed manifest prevents any mutation."""
        source = tmp_path / "source_skills"
        self._write_skill(source, "managed-skill")
        target = tmp_path / ".agents" / "skills"
        target.mkdir(parents=True)
        manifest = "| File | Description |\n| ---- | ----------- |\n| `managed-skill/SKILL.md` | forged |\n"
        (target / "agdt.README.md").write_text(manifest, encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False
        assert summary.injected == 0
        assert not (target / "managed-skill" / "SKILL.md").exists()
        assert (target / "agdt.README.md").read_text(encoding="utf-8") == manifest

    def test_consumer_authored_skill_is_never_deleted(self, tmp_path) -> None:
        """A skill the injector never wrote is absent from the manifest and survives."""
        source = tmp_path / "source_skills"
        source.mkdir()
        user_skill = tmp_path / ".agents" / "skills" / "user-skill"
        user_skill.mkdir(parents=True)
        (user_skill / "SKILL.md").write_text("mine", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is True
        assert summary.deletions_blocked is False
        assert (user_skill / "SKILL.md").read_text(encoding="utf-8") == "mine"

    def test_colliding_consumer_skill_is_not_adopted_or_overwritten(self, tmp_path) -> None:
        """A first-run collision with a consumer skill is skipped entirely."""
        source = tmp_path / "source_skills"
        self._write_skill(source, "user-skill")
        self._write_skill(source, "managed-skill")

        user_skill = tmp_path / ".agents" / "skills" / "user-skill"
        user_skill.mkdir(parents=True)
        (user_skill / "SKILL.md").write_text("mine", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with pytest.warns(RuntimeWarning, match="collide with consumer-authored files"):
                success, summary = inject_skills_with_summary(tmp_path)

        assert success is True
        assert summary.injected == 1
        assert summary.pruned == 0
        assert (user_skill / "SKILL.md").read_text(encoding="utf-8") == "mine"
        assert (tmp_path / ".agents" / "skills" / "managed-skill" / "SKILL.md").exists()

        manifest = (tmp_path / ".agents" / "skills" / "agdt.README.md").read_text(encoding="utf-8")
        assert "`managed-skill/SKILL.md`" in manifest
        assert "`user-skill/SKILL.md`" not in manifest

    def test_shared_resource_collision_aborts_before_injecting_dependent_skills(self, tmp_path) -> None:
        """A consumer fingerprint helper collision prevents bundled skill injection."""
        source = tmp_path / "source_skills"
        self._write_skill(source, "managed-skill")
        (source / "fingerprint.py").write_text("bundled", encoding="utf-8")

        target = tmp_path / ".agents" / "skills"
        target.mkdir(parents=True)
        (target / "fingerprint.py").write_text("consumer-authored", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with pytest.warns(RuntimeWarning, match="shared resource"):
                success, summary = inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary.injected == 1
        skills_plan = next(plan for plan in summary.plans if plan.kind == "skills")
        assert "managed-skill/SKILL.md" in skills_plan.added
        assert "fingerprint.py" in skills_plan.overwritten
        assert (target / "fingerprint.py").read_text(encoding="utf-8") == "consumer-authored"
        assert not (target / "managed-skill").exists()
        assert not (target / "agdt.README.md").exists()

    def test_shared_resource_collision_dry_run_prints_plans_without_mutation(self, tmp_path, capsys) -> None:
        """Dry-run reports all planned skill changes when a shared resource collides."""
        source = tmp_path / "source_skills"
        self._write_skill(source, "managed-skill")
        (source / "fingerprint.py").write_text("bundled", encoding="utf-8")

        target = tmp_path / ".agents" / "skills"
        target.mkdir(parents=True)
        (target / "fingerprint.py").write_text("consumer-authored", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with pytest.warns(RuntimeWarning, match="shared resource"):
                success, summary = inject_skills_with_summary(tmp_path, dry_run=True)

        assert success is False
        assert any(plan.kind == "skills" for plan in summary.plans)
        assert "Manifest diff — skills:" in capsys.readouterr().out
        assert (target / "fingerprint.py").read_text(encoding="utf-8") == "consumer-authored"
        assert not (target / "managed-skill").exists()
        assert not (target / "agdt.README.md").exists()

    def test_existing_unmanaged_skill_directory_blocks_new_skill_files(self, tmp_path) -> None:
        """An unmanaged pre-existing skill directory blocks bundled writes for that skill."""
        source = tmp_path / "source_skills"
        self._write_skill(source, "user-skill")

        user_skill = tmp_path / ".agents" / "skills" / "user-skill"
        user_skill.mkdir(parents=True)
        (user_skill / "notes.md").write_text("mine", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with pytest.warns(RuntimeWarning, match="collide with consumer-authored files"):
                success, _summary = inject_skills_with_summary(tmp_path)

        assert success is True
        assert (user_skill / "notes.md").read_text(encoding="utf-8") == "mine"
        assert not (user_skill / "SKILL.md").exists()

        manifest = (tmp_path / ".agents" / "skills" / "agdt.README.md").read_text(encoding="utf-8")
        assert "`user-skill/SKILL.md`" not in manifest

    def test_stale_skill_file_leaves_a_retained_directory_in_place(self, tmp_path) -> None:
        """Removing one resource of a still-mirrored skill keeps its directory."""
        source = tmp_path / "source_skills"
        self._write_skill(source, "kept-skill")
        target = tmp_path / ".agents" / "skills" / "kept-skill"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("---\ndescription: A skill\n---\n# kept-skill\n", encoding="utf-8")
        (target / "gone.md").write_text("retired resource", encoding="utf-8")
        (tmp_path / ".agents" / "skills" / "agdt.README.md").write_text(
            _generate_readme(
                [("kept-skill/SKILL.md", "A skill"), ("kept-skill/gone.md", "Retired")],
                "skills",
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert (target / "SKILL.md").exists()
        assert not (target / "gone.md").exists()
