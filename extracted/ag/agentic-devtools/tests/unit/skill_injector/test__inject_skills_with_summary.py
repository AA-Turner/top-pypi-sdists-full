"""End-to-end summary, planning, and execution scenarios for skill injection."""

import hashlib
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import inject_skills_with_summary
from agentic_devtools.skill_injector_models import InjectionSummary


class TestInjectSkillsWithSummary:
    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

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

    def test_returns_false_and_zero_summary_when_git_root_none(self) -> None:
        """git_root=None → (False, InjectionSummary(0, 0)) with no work done."""
        success, summary = inject_skills_with_summary(None)
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
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is True
        assert summary == InjectionSummary(injected=3, pruned=0)

    def test_missing_source_dir_returns_false_but_counts_other_kind(self, tmp_path) -> None:
        """A missing source for one kind → success False; the other kind is still counted."""
        prompts = tmp_path / "source_prompts"
        prompts.mkdir()
        (prompts / "agdt.c.prompt.md").write_text("---\ndescription: C\n---\n", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            # agents source missing (None), prompts source present
            mock_src.side_effect = self._source_selector(None, prompts)
            success, summary = inject_skills_with_summary(tmp_path)

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
                success, summary = inject_skills_with_summary(tmp_path)

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
            with patch("agentic_devtools.skill_injector_execution.os.replace", side_effect=OSError("disk full")):
                success, summary = inject_skills_with_summary(tmp_path)

        assert success is False
        # agents counted before the readme write failed; prompts never reached.
        assert summary == InjectionSummary(injected=2, pruned=0)
        assert any(plan.kind == "agents" for plan in summary.plans)

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
                success, summary = inject_skills_with_summary(tmp_path, issue_adapter="github", code_hosting="github")

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

        with patch("agentic_devtools.skill_injector_repo.__file__", str(module_path)):
            with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
                mock_src.side_effect = self._source_selector(target_agents, target_prompts)
                with pytest.warns(RuntimeWarning, match="skipping skill injection"):
                    success, summary = inject_skills_with_summary(
                        tmp_path, issue_adapter="github", code_hosting="github"
                    )

        assert success is True
        assert summary == InjectionSummary(injected=0, pruned=0)
        assert (target_agents / "agdt.filtered.agent.md").exists()
        assert not (target_agents / "agdt.README.md").exists()

    def test_dry_run_writes_nothing_and_prints_three_lists(self, tmp_path, capsys) -> None:
        """Dry run leaves every file byte-identical and prints adds/overwrites/deletes."""
        agents, prompts, _target = self._fixture(tmp_path)
        before = self._snapshot(tmp_path)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = inject_skills_with_summary(tmp_path, dry_run=True)

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
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary.deletions_blocked is True
        assert self._snapshot(tmp_path) == before
        err = capsys.readouterr().err
        assert "assume_yes=True" in err
        assert "--yes" in err
        assert "- agdt.stale.agent.md" in err

    def test_opt_in_executes_exactly_the_predicted_deletions(self, tmp_path, capsys) -> None:
        """With assume_yes the executed deletions equal the dry-run prediction."""
        agents, prompts, target = self._fixture(tmp_path)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            _success, predicted = inject_skills_with_summary(tmp_path, dry_run=True)

        before = set(self._snapshot(tmp_path))

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = inject_skills_with_summary(tmp_path, assume_yes=True)

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

    def test_no_resolvable_sources_print_no_diff(self, tmp_path, capsys) -> None:
        """When no kind resolves a source there is no manifest diff to print."""
        with patch("agentic_devtools.skill_injector._get_source_dir", return_value=None):
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary.plans == ()
        assert capsys.readouterr().out == ""

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
