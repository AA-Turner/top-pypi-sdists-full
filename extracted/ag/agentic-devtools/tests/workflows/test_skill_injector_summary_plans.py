"""End-to-end summary, planning, and execution scenarios for skill injection."""

import hashlib
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.skill_injector import inject_skills_with_summary


class TestSkillInjectorWorkflow:
    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

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
            _dry_success, dry_summary = inject_skills_with_summary(tmp_path, dry_run=True)

        agents_plan = next(plan for plan in dry_summary.plans if plan.kind == "agents")
        assert ".agdt/" in agents_plan.deleted

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, blocked_summary = inject_skills_with_summary(tmp_path)

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
                success, summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert any(".agdt/" in plan.deleted for plan in summary.plans)
        assert old_agdt.exists()

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

    def test_runs_without_deletions_need_no_opt_in(self, tmp_path) -> None:
        """An add-only run proceeds without assume_yes."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.new.agent.md").write_text("---\ndescription: New\n---\n", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is True
        assert summary.deletions_blocked is False
        assert (tmp_path / ".github" / "agents" / "agdt.new.agent.md").exists()

    def test_no_resolvable_sources_print_no_diff(self, tmp_path, capsys) -> None:
        """When no kind resolves a source there is no manifest diff to print."""
        with patch("agentic_devtools.skill_injector._get_source_dir", return_value=None):
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is False
        assert summary.plans == ()
        assert capsys.readouterr().out == ""
