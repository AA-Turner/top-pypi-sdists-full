"""End-to-end summary, planning, and execution scenarios for skill injection."""

from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import inject_skills_with_summary
from agentic_devtools.skill_injector_models import InjectionSummary


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
    def _make_self_checkout(root) -> None:
        """Create the marker files that identify an agentic-devtools checkout."""
        package = root / "agentic_devtools"
        package.mkdir(parents=True, exist_ok=True)
        (package / "skill_injector.py").write_text("", encoding="utf-8")
        (root / "pyproject.toml").write_text(
            '[project]\nname = "agentic-devtools"\n',
            encoding="utf-8",
        )

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
            success, summary = inject_skills_with_summary(tmp_path, issue_adapter="github", code_hosting="github")

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

    def test_flat_planning_oserror_preserves_selected_and_pruned_counts(self, tmp_path) -> None:
        """Flat preparation counts remain available when planning raises."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        agents.mkdir()
        prompts.mkdir()
        (agents / "agdt.keep.agent.md").write_text(
            "---\ndescription: Keep\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )
        (agents / "agdt.drop.agent.md").write_text(
            "---\ndescription: Drop\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents, prompts)
            with patch(
                "agentic_devtools.skill_injector_prepare_flat._plan_kind",
                side_effect=PermissionError("destination is unreadable"),
            ):
                success, summary = inject_skills_with_summary(tmp_path, issue_adapter="github")

        assert success is False
        assert summary == InjectionSummary(injected=1, pruned=1)

    def test_skill_planning_oserror_preserves_selected_and_pruned_counts(self, tmp_path) -> None:
        """Skill preparation counts remain available when planning raises."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        skills = tmp_path / "source_skills"
        agents.mkdir()
        prompts.mkdir()
        (skills / "keep" / "SKILL.md").parent.mkdir(parents=True)
        (skills / "keep" / "SKILL.md").write_text(
            "---\nname: keep\ndescription: Keep\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )
        (skills / "drop" / "SKILL.md").parent.mkdir(parents=True)
        (skills / "drop" / "SKILL.md").write_text(
            "---\nname: drop\ndescription: Drop\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = {"agents": agents, "prompts": prompts, "skills": skills}.__getitem__
            with patch(
                "agentic_devtools.skill_injector._plan_skills_kind",
                side_effect=PermissionError("destination is unreadable"),
            ):
                success, summary = inject_skills_with_summary(tmp_path, issue_adapter="github")

        assert success is False
        assert summary == InjectionSummary(injected=1, pruned=1)

    def test_invalid_skill_manifest_preserves_pruned_count(self, tmp_path) -> None:
        """Skill filtering counts remain available when manifest validation fails."""
        agents = tmp_path / "source_agents"
        prompts = tmp_path / "source_prompts"
        skills = tmp_path / "source_skills"
        agents.mkdir()
        prompts.mkdir()
        (skills / "drop" / "SKILL.md").parent.mkdir(parents=True)
        (skills / "drop" / "SKILL.md").write_text(
            "---\nname: drop\ndescription: Drop\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        target_skills = tmp_path / ".agents" / "skills"
        target_skills.mkdir(parents=True)
        (target_skills / "agdt.README.md").write_text("untrusted manifest", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = {"agents": agents, "prompts": prompts, "skills": skills}.__getitem__
            success, summary = inject_skills_with_summary(tmp_path, issue_adapter="github")

        assert success is False
        assert summary == InjectionSummary(injected=0, pruned=1)

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
            with patch("agentic_devtools.skill_injector_execution.os.replace", side_effect=OSError("disk full")):
                with patch("agentic_devtools.skill_injector_execution.os.unlink", side_effect=_unlink_side_effect):
                    success, summary = inject_skills_with_summary(tmp_path)

        # The OSError from os.replace is propagated; the unlink failure is swallowed.
        assert success is False

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
