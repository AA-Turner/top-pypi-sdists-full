"""Tests for agentic_devtools.skill_injector._inject_skills_with_summary."""

from __future__ import annotations

import hashlib
import warnings
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import (
    InjectionPlan,
    InjectionSummary,
    _generate_readme,
    _inject_skills_with_summary,
)


class TestInjectSkillsWithSummary:
    """Tests for the _inject_skills_with_summary function."""

    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

    def test_returns_false_and_zero_summary_when_git_root_none(self) -> None:
        """git_root=None → (False, InjectionSummary(0, 0)) with no work done."""
        success, summary = _inject_skills_with_summary(None)
        assert success is False
        assert summary == InjectionSummary(injected=0, pruned=0)

    def test_success_no_filter_counts_all_injected(self, tmp_path) -> None:
        """Both axes None → filter skipped; injected counts every file, pruned=0."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.a.agent.md").write_text("---\ndescription: A\n---\n", encoding="utf-8")
        (agents / "agdt.b.agent.md").write_text("---\ndescription: B\n---\n", encoding="utf-8")
        (prompts / "agdt.c.prompt.md").write_text("---\ndescription: C\n---\n", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = _inject_skills_with_summary(tmp_path)

        assert success is True
        assert summary == InjectionSummary(injected=3, pruned=0)

    def test_success_with_filter_counts_pruned(self, tmp_path) -> None:
        """A resolved axis prunes non-matching files; counts reflect the split."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.jira-only.agent.md").write_text(
            "---\ndescription: Jira\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        (agents / "agdt.github-only.agent.md").write_text(
            "---\ndescription: GitHub\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = _inject_skills_with_summary(tmp_path, issue_adapter="github", code_hosting="github")

        assert success is True
        # github-only kept (injected=1), jira-only pruned (pruned=1)
        assert summary == InjectionSummary(injected=1, pruned=1)
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.github-only.agent.md").exists()
        assert not (target / "agdt.jira-only.agent.md").exists()

    def test_missing_source_dir_returns_false_but_counts_other_kind(self, tmp_path) -> None:
        """A missing source for one kind → success False; the other kind is still counted."""
        prompts = tmp_path / "source_prompts"
        prompts.mkdir()
        (prompts / "agdt.c.prompt.md").write_text("---\ndescription: C\n---\n", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            # agents source missing (None), prompts source present
            mock_src.side_effect = self._source_selector(None, prompts)
            success, summary = _inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary == InjectionSummary(injected=1, pruned=0)

    def test_returns_false_and_zero_summary_on_mkdir_oserror(self, tmp_path) -> None:
        """An OSError before any counting → (False, InjectionSummary(0, 0))."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            with patch("pathlib.Path.mkdir", side_effect=OSError("permission denied")):
                success, summary = _inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary == InjectionSummary(injected=0, pruned=0)

    def test_best_effort_counts_populated_on_oserror(self, tmp_path) -> None:
        """An OSError after the first kind is counted still returns best-effort counts."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.a.agent.md").write_text("---\ndescription: A\n---\n", encoding="utf-8")
        (agents / "agdt.b.agent.md").write_text("---\ndescription: B\n---\n", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            # The atomic rename raises AFTER agents' source_rel_names is counted.
            with patch("agentic_devtools.skill_injector.os.replace", side_effect=OSError("disk full")):
                success, summary = _inject_skills_with_summary(tmp_path)

        assert success is False
        # agents counted before the readme write failed; prompts never reached.
        assert summary == InjectionSummary(injected=2, pruned=0)
        assert any(plan.kind == "agents" for plan in summary.plans)

    def test_atomic_manifest_tmpfile_unlink_failure_is_swallowed(self, tmp_path) -> None:
        """If temp-file cleanup itself raises OSError the original error is still re-raised."""
        import os as real_os

        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.a.agent.md").write_text("---\ndescription: A\n---\n", encoding="utf-8")

        # Save the real unlink reference BEFORE patching so the side_effect can
        # call through for non-temp-file paths without infinite recursion.
        real_unlink = real_os.unlink

        def _unlink_side_effect(path):
            if ".agdt.README." in str(path):
                raise OSError("can't unlink temp file")
            return real_unlink(path)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            with patch("agentic_devtools.skill_injector.os.replace", side_effect=OSError("disk full")):
                with patch("agentic_devtools.skill_injector.os.unlink", side_effect=_unlink_side_effect):
                    success, summary = _inject_skills_with_summary(tmp_path)

        # The OSError from os.replace is propagated; the unlink failure is swallowed.
        assert success is False

    @staticmethod
    def _make_self_checkout(root) -> None:
        """Create the marker files that identify an agentic-devtools checkout."""
        package = root / "agentic_devtools"
        package.mkdir(parents=True, exist_ok=True)
        (package / "skill_injector.py").write_text("", encoding="utf-8")
        (root / "pyproject.toml").write_text(
            '[project]\nname = "agentic-devtools"\n',
            encoding="utf-8",
        )

    def test_self_repo_wheel_install_is_a_no_op(self, tmp_path) -> None:
        """Wheel install targeting this repo must not copy, delete or overwrite."""
        self._make_self_checkout(tmp_path)
        # Bundled (wheel) source carries different/older content.
        bundled_agents = tmp_path / "site_packages" / "agents"
        bundled_prompts = tmp_path / "site_packages" / "prompts"
        bundled_agents.mkdir(parents=True)
        bundled_prompts.mkdir(parents=True)
        (bundled_agents / "agdt.kept.agent.md").write_text("old released content", encoding="utf-8")

        # The repo's own tracked source — including a file the classification
        # filter would prune, and therefore stale-cleanup would delete.
        target_agents = tmp_path / ".github" / "agents"
        target_agents.mkdir(parents=True)
        (target_agents / "agdt.kept.agent.md").write_text("tracked source", encoding="utf-8")
        (target_agents / "agdt.filtered.agent.md").write_text("tracked source", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(bundled_agents, bundled_prompts)
            with pytest.warns(RuntimeWarning, match="skipping skill injection"):
                success, summary = _inject_skills_with_summary(tmp_path, issue_adapter="github", code_hosting="github")

        assert success is True
        assert summary == InjectionSummary(injected=0, pruned=0)
        assert (target_agents / "agdt.filtered.agent.md").exists()
        assert (target_agents / "agdt.kept.agent.md").read_text(encoding="utf-8") == "tracked source"
        assert not (target_agents / "agdt.README.md").exists()

    def test_self_repo_editable_install_is_a_no_op(self, tmp_path) -> None:
        """Editable install targeting this repo must not delete tracked files."""
        module_path = tmp_path / "agentic_devtools" / "skill_injector.py"
        module_path.parent.mkdir(parents=True)
        module_path.write_text("", encoding="utf-8")

        # Editable install: source dir *is* the repo's own .github/<kind>.
        target_agents = tmp_path / ".github" / "agents"
        target_prompts = tmp_path / ".github" / "prompts"
        target_agents.mkdir(parents=True)
        target_prompts.mkdir(parents=True)
        (target_agents / "agdt.filtered.agent.md").write_text(
            "---\ndescription: Jira\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector.__file__", str(module_path)):
            with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
                mock_src.side_effect = self._source_selector(target_agents, target_prompts)
                with pytest.warns(RuntimeWarning, match="skipping skill injection"):
                    success, summary = _inject_skills_with_summary(
                        tmp_path, issue_adapter="github", code_hosting="github"
                    )

        assert success is True
        assert summary == InjectionSummary(injected=0, pruned=0)
        assert (target_agents / "agdt.filtered.agent.md").exists()
        assert not (target_agents / "agdt.README.md").exists()

    # ── Manifest diff / dry run / deletion gate ──────────────────────────

    @staticmethod
    def _snapshot(root):
        """Return {relative path: sha256} for every file under *root*."""
        return {
            str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*"))
            if p.is_file()
        }

    def _fixture(self, tmp_path):
        """Build a source/target pair with one add, one overwrite and one delete."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.new.agent.md").write_text("---\ndescription: New\n---\n", encoding="utf-8")
        (agents / "agdt.changed.agent.md").write_text("---\ndescription: New content\n---\n", encoding="utf-8")

        target_agents = tmp_path / ".github" / "agents"
        target_agents.mkdir(parents=True)
        (target_agents / "agdt.changed.agent.md").write_text("---\ndescription: Old content\n---\n", encoding="utf-8")
        (target_agents / "agdt.stale.agent.md").write_text("stale", encoding="utf-8")
        return agents, prompts, target_agents

    def test_dry_run_writes_nothing_and_prints_three_lists(self, tmp_path, capsys) -> None:
        """Dry run leaves every file byte-identical and prints adds/overwrites/deletes."""
        agents, prompts, _target = self._fixture(tmp_path)
        before = self._snapshot(tmp_path)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = _inject_skills_with_summary(tmp_path, dry_run=True)

        assert success is True
        assert self._snapshot(tmp_path) == before

        out = capsys.readouterr().out
        assert "adds (1):" in out
        assert "+ agdt.new.agent.md" in out
        assert "overwrites (1):" in out
        assert "~ agdt.changed.agent.md" in out
        assert "deletes (1):" in out
        assert "- agdt.stale.agent.md" in out

        agents_plan = next(plan for plan in summary.plans if plan.kind == "agents")
        assert agents_plan.added == ("agdt.new.agent.md",)
        assert agents_plan.overwritten == ("agdt.changed.agent.md",)
        assert agents_plan.deleted == ("agdt.stale.agent.md",)
        assert summary.deletions_blocked is False

    def test_pending_deletions_without_opt_in_change_nothing(self, tmp_path, capsys) -> None:
        """Deletions without assume_yes → failure, nothing written or unlinked."""
        agents, prompts, _target = self._fixture(tmp_path)
        before = self._snapshot(tmp_path)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = _inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary.deletions_blocked is True
        assert self._snapshot(tmp_path) == before
        err = capsys.readouterr().err
        assert "assume_yes=True" in err
        assert "--yes" in err
        assert "- agdt.stale.agent.md" in err

    def test_legacy_dot_agdt_delete_is_planned_and_blocked_without_opt_in(self, tmp_path) -> None:
        """Legacy .agdt migration is in the plan and requires assume_yes."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        old_agdt = tmp_path / ".github" / "agents" / ".agdt"
        old_agdt.mkdir(parents=True)
        (old_agdt / "old.agent.md").write_text("old", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            _dry_success, dry_summary = _inject_skills_with_summary(tmp_path, dry_run=True)

        agents_plan = next(plan for plan in dry_summary.plans if plan.kind == "agents")
        assert ".agdt/" in agents_plan.deleted

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, blocked_summary = _inject_skills_with_summary(tmp_path)

        assert success is False
        assert blocked_summary.deletions_blocked is True
        assert old_agdt.exists()

    def test_legacy_dot_agdt_disappearing_after_plan_does_not_crash(self, tmp_path) -> None:
        """If legacy .agdt disappears after planning, execution skips rmtree safely."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        old_agdt = tmp_path / ".github" / "agents" / ".agdt"
        old_agdt.mkdir(parents=True)

        real_is_dir = Path.is_dir
        old_agdt_is_dir_calls = 0

        def _is_dir(path: Path) -> bool:
            nonlocal old_agdt_is_dir_calls
            if path == old_agdt:
                old_agdt_is_dir_calls += 1
                return old_agdt_is_dir_calls == 1
            return real_is_dir(path)

        with patch("pathlib.Path.is_dir", autospec=True, side_effect=_is_dir):
            with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
                mock_src.side_effect = self._source_selector(agents, prompts)
                success, summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert any(".agdt/" in plan.deleted for plan in summary.plans)
        assert old_agdt.exists()

    def test_opt_in_executes_exactly_the_predicted_deletions(self, tmp_path, capsys) -> None:
        """With assume_yes the executed deletions equal the dry-run prediction."""
        agents, prompts, target = self._fixture(tmp_path)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            _success, predicted = _inject_skills_with_summary(tmp_path, dry_run=True)

        before = set(self._snapshot(tmp_path))

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert summary.deletions_blocked is False

        after = set(self._snapshot(tmp_path))
        executed_deletions = {Path(rel).name for rel in before - after}
        predicted_deletions = {name for plan in predicted.plans for name in plan.deleted}
        assert executed_deletions == predicted_deletions == {"agdt.stale.agent.md"}

        # The printed counts match what was executed.
        assert (target / "agdt.new.agent.md").exists()
        assert (target / "agdt.changed.agent.md").read_text(encoding="utf-8") == "---\ndescription: New content\n---\n"
        out = capsys.readouterr().out
        assert "1 add(s), 1 overwrite(s), 1 delete(s)" in out

    def test_runs_without_deletions_need_no_opt_in(self, tmp_path) -> None:
        """An add-only run proceeds without assume_yes."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.new.agent.md").write_text("---\ndescription: New\n---\n", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = _inject_skills_with_summary(tmp_path)

        assert success is True
        assert summary.deletions_blocked is False
        assert (tmp_path / ".github" / "agents" / "agdt.new.agent.md").exists()

    def test_no_resolvable_sources_print_no_diff(self, tmp_path, capsys) -> None:
        """When no kind resolves a source there is no manifest diff to print."""
        with patch("agentic_devtools.skill_injector._get_source_dir", return_value=None):
            success, summary = _inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary.plans == ()
        assert capsys.readouterr().out == ""

    # ── The directory-shaped skills kind ─────────────────────────────────

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
            success, summary = _inject_skills_with_summary(tmp_path)

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
            _success, _summary = _inject_skills_with_summary(tmp_path)

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
            success, summary = _inject_skills_with_summary(tmp_path, issue_adapter="github", code_hosting="github")

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
            blocked_success, blocked_summary = _inject_skills_with_summary(tmp_path)

        assert blocked_success is False
        assert blocked_summary.deletions_blocked is True
        assert (stale_dir / "SKILL.md").exists()
        assert "- retired-skill/SKILL.md" in capsys.readouterr().err

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

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
            success, summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

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
            success, summary = _inject_skills_with_summary(tmp_path)

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
                success, summary = _inject_skills_with_summary(tmp_path)

        assert success is True
        assert summary.injected == 1
        assert summary.pruned == 0
        assert (user_skill / "SKILL.md").read_text(encoding="utf-8") == "mine"
        assert (tmp_path / ".agents" / "skills" / "managed-skill" / "SKILL.md").exists()

        manifest = (tmp_path / ".agents" / "skills" / "agdt.README.md").read_text(encoding="utf-8")
        assert "`managed-skill/SKILL.md`" in manifest
        assert "`user-skill/SKILL.md`" not in manifest

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
                success, _summary = _inject_skills_with_summary(tmp_path)

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
            success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert (target / "SKILL.md").exists()
        assert not (target / "gone.md").exists()

    def test_binary_skill_resource_does_not_fail_injection(self, tmp_path) -> None:
        """A non-UTF-8 skill resource is injected without setting overall_success=False."""
        source = tmp_path / "source_skills"
        skill_src = source / "binary-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text(
            "---\ndescription: Binary resource test\n---\n# binary-skill\n",
            encoding="utf-8",
        )
        # Write a non-UTF-8 resource file (e.g. a PNG header)
        (skill_src / "icon.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, summary = _inject_skills_with_summary(tmp_path)

        assert success is True
        target = tmp_path / ".agents" / "skills"
        assert (target / "binary-skill" / "SKILL.md").exists()
        assert (target / "binary-skill" / "icon.png").exists()
        readme = (target / "agdt.README.md").read_text(encoding="utf-8")
        assert "binary-skill/icon.png" in readme

    def test_case_only_resource_rename_not_treated_as_collision_when_same_inode(self, tmp_path) -> None:
        """A case-only resource rename on a case-insensitive FS is not flagged as a collision.

        When the manifest lists ``my-skill/Guide.md`` and the next wheel ships
        ``my-skill/guide.md``, the destination path exists because both spellings
        resolve to the same inode on macOS/Windows.  The injection must update the
        file and the manifest without raising a collision warning.
        """
        source = tmp_path / "source_skills"
        skill_src = source / "my-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_src / "guide.md").write_text("new guide content", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skill_dest = skills_dir / "my-skill"
        skill_dest.mkdir(parents=True)
        (skill_dest / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        guide_old = skill_dest / "Guide.md"
        guide_old.write_text("old guide content", encoding="utf-8")

        skills_dir.joinpath("agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "My skill"), ("my-skill/Guide.md", "Guide")], "skills"),
            encoding="utf-8",
        )

        # Simulate a case-insensitive filesystem by hard-linking both spellings
        # to the same inode so stat() returns identical st_ino / st_dev values.
        guide_new = skill_dest / "guide.md"
        try:
            guide_new.hardlink_to(guide_old)
        except OSError:
            pytest.skip("hard links not supported on this platform")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                success, _summary = _inject_skills_with_summary(tmp_path)

        assert success is True

    def test_case_rename_stat_oserror_in_collision_check_does_not_block_injection(self, tmp_path) -> None:
        """stat() raising OSError in the collision check falls through gracefully.

        When ``guide.md`` (new spelling) is not yet present in the target directory,
        ``stat()`` raises ``OSError``.  The exception is caught, ``not_in_manifest``
        stays ``True``, but ``dest.exists()`` returns ``False``, so no collision is
        falsely reported and the skill is injected normally.
        """
        source = tmp_path / "source_skills"
        skill_src = source / "my-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_src / "guide.md").write_text("guide content", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skill_dest = skills_dir / "my-skill"
        skill_dest.mkdir(parents=True)
        (skill_dest / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_dest / "Guide.md").write_text("old guide content", encoding="utf-8")
        # guide.md is NOT present in the target: stat() on the dest path will raise
        # FileNotFoundError (an OSError), exercising the except branch.

        skills_dir.joinpath("agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "My skill"), ("my-skill/Guide.md", "Guide")], "skills"),
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                success, summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert summary.injected == 1
        assert (skill_dest / "guide.md").exists()

    def test_case_resource_with_distinct_inode_still_treated_as_collision(self, tmp_path) -> None:
        """A same-casefold file with a different inode is still a consumer collision.

        On a case-sensitive filesystem both ``Guide.md`` (managed) and ``guide.md``
        (consumer-authored) can coexist with distinct inodes.  When the new source
        introduces ``guide.md`` the inode check returns False, ``not_in_manifest``
        stays ``True``, and the skill is correctly skipped as a collision.
        """
        source = tmp_path / "source_skills"
        skill_src = source / "my-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_src / "guide.md").write_text("bundled guide", encoding="utf-8")
        kept_skill_src = source / "kept-skill"
        kept_skill_src.mkdir(parents=True)
        (kept_skill_src / "SKILL.md").write_text("---\ndescription: Kept skill\n---\n# kept-skill\n", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skill_dest = skills_dir / "my-skill"
        skill_dest.mkdir(parents=True)
        (skill_dest / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_dest / "Guide.md").write_text("managed guide", encoding="utf-8")
        (skill_dest / "guide.md").write_text("consumer guide", encoding="utf-8")  # distinct inode
        kept_skill_dest = skills_dir / "kept-skill"
        kept_skill_dest.mkdir(parents=True)
        (kept_skill_dest / "SKILL.md").write_text(
            "---\ndescription: Kept skill\n---\n# kept-skill\n",
            encoding="utf-8",
        )

        skills_dir.joinpath("agdt.README.md").write_text(
            _generate_readme(
                [
                    ("my-skill/SKILL.md", "My skill"),
                    ("my-skill/Guide.md", "Guide"),
                    ("my-skill/old.md", "Old"),
                    ("kept-skill/SKILL.md", "Kept skill"),
                ],
                "skills",
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with pytest.warns(RuntimeWarning, match="collide with consumer-authored files"):
                success, summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert summary.injected == 1
        assert (
            (kept_skill_dest / "SKILL.md").read_text(encoding="utf-8").startswith("---\ndescription: Kept skill\n---\n")
        )
        assert (skill_dest / "SKILL.md").read_text(encoding="utf-8").startswith("---\ndescription: My skill\n---\n")
        assert (skill_dest / "Guide.md").read_text(encoding="utf-8") == "managed guide"
        assert (skill_dest / "guide.md").read_text(encoding="utf-8") == "consumer guide"
        manifest = skills_dir.joinpath("agdt.README.md").read_text(encoding="utf-8")
        assert "`my-skill/SKILL.md`" in manifest
        assert "`my-skill/Guide.md`" in manifest
        assert "`my-skill/guide.md`" not in manifest
        assert "`my-skill/old.md`" not in manifest
        assert "`kept-skill/SKILL.md`" in manifest

    def test_partial_copy_failure_rolls_back_newly_created_files(self, tmp_path) -> None:
        """Files created in a failed run are rolled back so the next run can retry.

        If the second copy raises ``OSError``, the first file that was newly
        created (not previously on disk) must be removed.  This ensures the
        on-disk state still matches the old manifest so the next invocation
        treats the skill as un-injected rather than consumer-authored.
        """
        import shutil as _shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "extra.md").write_text("# Extra", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)
        # No manifest yet — simulates a first-ever injection.

        copy_calls: list[Path] = []
        original_copy2 = _shutil.copy2

        def _failing_copy2(src, dst, **kw):
            copy_calls.append(Path(src))
            if len(copy_calls) == 2:
                raise OSError("simulated disk error on second copy")
            return original_copy2(src, dst, **kw)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with patch("agentic_devtools.skill_injector.shutil.copy2", side_effect=_failing_copy2):
                success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False
        dest_skill_dir = skills_dir / "my-skill"
        assert not dest_skill_dir.exists()
        # The manifest must not have been written (still absent).
        assert not (skills_dir / "agdt.README.md").exists()

    def test_partial_new_file_is_rolled_back_when_copy_raises_after_creating_it(self, tmp_path) -> None:
        """A file created before ``copy2()`` raises is still removed during rollback."""
        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "extra.md").write_text("# Extra", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)

        copy_calls = 0

        def _partial_copy_then_fail(src, dst, **_kw):
            nonlocal copy_calls
            copy_calls += 1
            Path(dst).write_text("partial", encoding="utf-8")
            raise OSError(f"simulated copy failure {copy_calls}")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with patch("agentic_devtools.skill_injector.shutil.copy2", side_effect=_partial_copy_then_fail):
                success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False
        assert not (skills_dir / "my-skill").exists()
        assert not (skills_dir / "agdt.README.md").exists()

    def test_partial_copy_failure_rollback_survives_unlink_error(self, tmp_path) -> None:
        """The rollback loop tolerates ``OSError`` from ``unlink()`` and still raises.

        If removing a newly-created file fails (e.g. read-only filesystem),
        the inner ``OSError`` is swallowed and the outer one is still re-raised,
        so the overall function returns ``False``.
        """
        import shutil as _shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "extra.md").write_text("# Extra", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)

        copy_calls: list[Path] = []
        original_copy2 = _shutil.copy2

        def _failing_copy2(src, dst, **kw):
            copy_calls.append(Path(src))
            if len(copy_calls) == 2:
                raise OSError("disk error")
            return original_copy2(src, dst, **kw)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with patch("agentic_devtools.skill_injector.shutil.copy2", side_effect=_failing_copy2):
                # Simulate unlink also failing during rollback.
                with patch("pathlib.Path.unlink", side_effect=OSError("permission denied")):
                    success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False

    def test_case_rename_fallback_when_old_path_absent(self, tmp_path) -> None:
        """When old_path is absent at execution time the copy falls back to a normal copy."""
        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("guide content", encoding="utf-8")

        # Target does not contain Guide.md, so old_path.is_file() will be False
        # for the case rename path.  Mock _plan_skills_kind to inject case_renames
        # pointing to the absent old spelling.
        mocked_plan = InjectionPlan(
            kind="skills",
            added=("my-skill/SKILL.md", "my-skill/guide.md"),
            overwritten=(),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )
        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        target_dir = tmp_path / ".agents" / "skills"
        assert success is True
        # guide.md must be written via the fallback path
        assert (target_dir / "my-skill" / "guide.md").read_text(encoding="utf-8") == "guide content"

    def test_case_rename_fallback_when_dest_already_exists(self, tmp_path) -> None:
        """Fallback path does not mark dest as newly_created when it already exists."""
        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("new guide content", encoding="utf-8")

        # Target has guide.md (lowercased, already managed) but NOT Guide.md.
        target_dir = tmp_path / ".agents" / "skills"
        (target_dir / "my-skill").mkdir(parents=True)
        (target_dir / "my-skill" / "guide.md").write_text("old guide content", encoding="utf-8")
        # Write a manifest that claims ownership of the existing guide.md so it
        # is not treated as consumer-authored during the collision check.
        (target_dir / "agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "A skill"), ("my-skill/guide.md", "guide")], "skills"),
            encoding="utf-8",
        )

        mocked_plan = InjectionPlan(
            kind="skills",
            added=(),
            overwritten=("my-skill/SKILL.md", "my-skill/guide.md"),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )
        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        # guide.md content updated via fallback overwrite (existed_before=True path)
        assert (target_dir / "my-skill" / "guide.md").read_text(encoding="utf-8") == "new guide content"

    def test_case_rename_rollback_restores_old_casing_on_copy_failure(self, tmp_path) -> None:
        """When copy2 fails during a case rename, the old-cased file is restored."""
        import shutil as real_shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("new guide", encoding="utf-8")

        # Pre-populate target with old-cased file and a matching manifest.
        target_dir = tmp_path / ".agents" / "skills"
        (target_dir / "my-skill").mkdir(parents=True)
        (target_dir / "my-skill" / "SKILL.md").write_text(
            "---\ndescription: A skill\n---\n# my-skill\n", encoding="utf-8"
        )
        (target_dir / "my-skill" / "Guide.md").write_text("old guide", encoding="utf-8")
        (target_dir / "agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "A skill"), ("my-skill/Guide.md", "guide")], "skills"),
            encoding="utf-8",
        )

        mocked_plan = InjectionPlan(
            kind="skills",
            added=(),
            overwritten=("my-skill/SKILL.md", "my-skill/guide.md"),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )

        # Save the real copy2 before entering the patch context so the side
        # effect can call through without triggering recursive mock calls.
        _real_copy2 = real_shutil.copy2

        def _copy2_raise_for_guide(src, dst, **kw):
            if Path(dst).name == "guide.md":
                raise OSError("disk full during guide copy")
            return _real_copy2(src, dst, **kw)

        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
            patch("agentic_devtools.skill_injector.shutil.copy2", side_effect=_copy2_raise_for_guide),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False
        # Old-cased Guide.md must be restored by the rollback
        assert (target_dir / "my-skill" / "Guide.md").read_text(encoding="utf-8") == "old guide"

    def test_case_rename_rollback_os_replace_failure_is_swallowed(self, tmp_path) -> None:
        """When the rollback os.replace also fails, the original error is still re-raised."""
        import os as real_os
        import shutil as real_shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("new guide", encoding="utf-8")

        target_dir = tmp_path / ".agents" / "skills"
        (target_dir / "my-skill").mkdir(parents=True)
        (target_dir / "my-skill" / "SKILL.md").write_text(
            "---\ndescription: A skill\n---\n# my-skill\n", encoding="utf-8"
        )
        (target_dir / "my-skill" / "Guide.md").write_text("old guide", encoding="utf-8")
        (target_dir / "agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "A skill"), ("my-skill/Guide.md", "guide")], "skills"),
            encoding="utf-8",
        )

        mocked_plan = InjectionPlan(
            kind="skills",
            added=(),
            overwritten=("my-skill/SKILL.md", "my-skill/guide.md"),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )

        _real_copy2 = real_shutil.copy2
        _real_replace = real_os.replace

        def _copy2_raise_for_guide(src, dst, **kw):
            if Path(dst).name == "guide.md":
                raise OSError("disk full during guide copy")
            return _real_copy2(src, dst, **kw)

        def _replace_fail_on_rollback(src, dst):
            # Fail the rollback specifically: the rollback tries to rename the
            # temp file *back* to Guide.md (dst ends with Guide.md).  All other
            # os.replace calls (initial rename, manifest writes) are passed through.
            if Path(dst).name == "Guide.md":
                raise OSError("cannot restore temp file")
            return _real_replace(src, dst)

        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
            patch("agentic_devtools.skill_injector.shutil.copy2", side_effect=_copy2_raise_for_guide),
            patch("agentic_devtools.skill_injector.os.replace", side_effect=_replace_fail_on_rollback),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = _inject_skills_with_summary(tmp_path, assume_yes=True)

        # The original OSError from copy2 is still propagated even though rollback failed.
        assert success is False
