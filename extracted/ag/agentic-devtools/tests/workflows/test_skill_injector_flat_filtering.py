"""End-to-end skill injection scenarios."""

from unittest.mock import patch

from agentic_devtools.skill_injector import inject_skills


class TestInjectSkillsWorkflow:
    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

    def test_filters_by_issue_adapter(self, tmp_path):
        """Files requiring a non-matching issue_adapter are excluded."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring jira — should be excluded when issue_adapter="github"
        (source / "agdt.jira-only.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # File requiring github — should be kept
        (source / "agdt.github-issue.agent.md").write_text(
            "---\ndescription: GitHub agent\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert not (target / "agdt.jira-only.agent.md").exists()
        assert (target / "agdt.github-issue.agent.md").exists()

    def test_filters_by_code_hosting(self, tmp_path):
        """Files requiring a non-matching code_hosting are excluded."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring azure_devops — should be excluded when code_hosting="github"
        (source / "agdt.ado-only.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )
        # File requiring github — should be kept
        (source / "agdt.gh-hosting.agent.md").write_text(
            "---\ndescription: GH hosting agent\nagdt:\n  requires:\n    code_hosting: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert not (target / "agdt.ado-only.agent.md").exists()
        assert (target / "agdt.gh-hosting.agent.md").exists()

    def test_always_true_bypasses_filter(self, tmp_path):
        """Files with always: true are always injected regardless of platform."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.always-inject.agent.md").write_text(
            "---\ndescription: Always agent\nagdt:\n  always: true\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.always-inject.agent.md").exists()

    def test_universal_files_always_injected(self, tmp_path):
        """Files with no requires block pass any filter (universal)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal agent\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.universal.agent.md").exists()

    def test_stale_cleanup_removes_previously_injected_excluded_files(self, tmp_path):
        """Stale files from a prior run are pruned when classification excludes them (opt-in given)."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()
        # Source contains a jira-only file
        (agents_source / "agdt.jira-only.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        # Simulate a previously injected file in target that won't be in new source set
        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        stale = target_dir / "agdt.jira-only.agent.md"
        stale.write_text("previously injected", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github", assume_yes=True)

        # The file should be removed because it was excluded by filter
        # and therefore not in source_rel_names
        assert not stale.exists()

    def test_manifest_reflects_only_injected_files(self, tmp_path):
        """README manifest lists only files that passed the classification filter."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.kept.agent.md").write_text(
            "---\ndescription: Kept agent\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.excluded.agent.md").write_text(
            "---\ndescription: Excluded agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        readme = tmp_path / ".github" / "agents" / "agdt.README.md"
        content = readme.read_text(encoding="utf-8")
        assert "agdt.kept.agent.md" in content
        assert "agdt.excluded.agent.md" not in content

    def test_both_none_preserves_all_files(self, tmp_path):
        """All files are injected when both axes are None (filter phase skipped)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira-only.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal agent\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path)

        target = tmp_path / ".github" / "agents"
        # Both files should be injected when no filter is applied
        assert (target / "agdt.jira-only.agent.md").exists()
        assert (target / "agdt.universal.agent.md").exists()
        # README lists both
        readme_content = (target / "agdt.README.md").read_text(encoding="utf-8")
        assert "agdt.jira-only.agent.md" in readme_content
        assert "agdt.universal.agent.md" in readme_content

    def test_single_axis_filtering_issue_adapter_only(self, tmp_path):
        """Only the resolved axis filters; code_hosting=None is unrestricted."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring jira issue_adapter
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # File requiring azure_devops code_hosting (should pass since code_hosting is None)
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # jira issue_adapter is excluded because issue_adapter="github" != "jira"
        assert not (target / "agdt.jira.agent.md").exists()
        # azure_devops code_hosting passes because code_hosting=None is unrestricted
        assert (target / "agdt.ado.agent.md").exists()

    def test_single_axis_filtering_code_hosting_only(self, tmp_path):
        """Only the resolved axis filters; issue_adapter=None is unrestricted."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring jira issue_adapter (should pass since issue_adapter is None)
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # File requiring azure_devops code_hosting
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter=None, code_hosting="github")

        target = tmp_path / ".github" / "agents"
        # jira issue_adapter passes because issue_adapter=None is unrestricted
        assert (target / "agdt.jira.agent.md").exists()
        # azure_devops code_hosting is excluded because code_hosting="github" != "azure_devops"
        assert not (target / "agdt.ado.agent.md").exists()
