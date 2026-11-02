"""End-to-end skill injection scenarios."""

from unittest.mock import patch

import pytest

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

    def test_unicode_decode_error_in_filter_phase_keeps_file(self, tmp_path):
        """UnicodeDecodeError in filter phase treats file as injectable."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Binary file that can't be decoded
        (source / "agdt.binary.agent.md").write_bytes(b"\xff\xfe\xfa")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        # File is kept (injected) but overall_success is False due to copy phase decode error
        assert result is False
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.binary.agent.md").exists()

    def test_malformed_yaml_treated_as_universal(self, tmp_path):
        """Malformed frontmatter yields universal classification (file is kept)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.malformed.agent.md").write_text(
            "---\n: invalid: yaml: [unclosed\n---\n# Content",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.malformed.agent.md").exists()

    def test_empty_string_issue_adapter_normalized_to_none(self, tmp_path):
        """Empty string issue_adapter is normalized to None (inject-all for that axis)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # Empty string is normalized to None (unresolved), so inject-all applies
        assert (target / "agdt.jira.agent.md").exists()
        assert (target / "agdt.universal.agent.md").exists()

    def test_empty_string_code_hosting_normalized_to_none(self, tmp_path):
        """Empty string code_hosting is normalized to None (inject-all for that axis)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter=None, code_hosting="")

        target = tmp_path / ".github" / "agents"
        # Empty string is normalized to None (unresolved), so inject-all applies
        assert (target / "agdt.ado.agent.md").exists()
        assert (target / "agdt.universal.agent.md").exists()

    def test_whitespace_issue_adapter_normalized_to_none(self, tmp_path):
        """Whitespace-only issue_adapter is normalized to None (inject-all for that axis)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="   ", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # Whitespace-only string normalized to None — inject-all applies
        assert (target / "agdt.jira.agent.md").exists()

    def test_invalid_issue_adapter_warns_and_falls_back_to_inject_all(self, tmp_path):
        """Unknown issue_adapter value emits a RuntimeWarning and falls back to inject-all."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            with pytest.warns(
                RuntimeWarning,
                match=r"unknown issue_adapter value 'nonexistent'.*valid options are",
            ):
                inject_skills(tmp_path, issue_adapter="nonexistent", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # Invalid value treated as unresolved — inject-all applies
        assert (target / "agdt.jira.agent.md").exists()

    def test_invalid_code_hosting_warns_and_falls_back_to_inject_all(self, tmp_path):
        """Unknown code_hosting value emits a RuntimeWarning and falls back to inject-all."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            with pytest.warns(
                RuntimeWarning,
                match=r"unknown code_hosting value 'unknown_host'.*valid options are",
            ):
                inject_skills(tmp_path, issue_adapter=None, code_hosting="unknown_host")

        target = tmp_path / ".github" / "agents"
        # Invalid value treated as unresolved — inject-all applies
        assert (target / "agdt.ado.agent.md").exists()

    def test_user_files_never_removed_with_filtering(self, tmp_path):
        """Non-agdt files are untouched even with classification filtering active."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        user_file = target_dir / "my-custom.agent.md"
        user_file.write_text("user content", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert user_file.exists()
        assert user_file.read_text(encoding="utf-8") == "user content"

    def test_readme_never_deleted_with_filtering(self, tmp_path):
        """agdt.README.md is regenerated (not deleted) with classification filtering."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        readme = target_dir / "agdt.README.md"
        readme.write_text("old readme content", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert readme.exists()
        content = readme.read_text(encoding="utf-8")
        assert "old readme content" not in content
        assert "Managed" in content

    def test_collision_not_emitted_when_one_file_filtered(self, tmp_path):
        """Collision warning is suppressed when only one of two colliding files passes."""
        import warnings as _warnings

        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Two subdirectories that sanitize to the same flat name
        dir_a = source / "sub-1"
        dir_b = source / "sub_1"
        dir_a.mkdir()
        dir_b.mkdir()
        # dir_a file requires jira (will be filtered out)
        (dir_a / "agdt.dup.agent.md").write_text(
            "---\ndescription: dup A\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # dir_b file requires github (will pass)
        (dir_b / "agdt.dup.agent.md").write_text(
            "---\ndescription: dup B\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with _warnings.catch_warnings(record=True) as caught:
                _warnings.simplefilter("always")
                mock_src.side_effect = self._source_selector(source, prompts_source)
                inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        dup_warnings = [w for w in caught if "duplicate flat filename" in str(w.message)]
        assert len(dup_warnings) == 0

    def test_casefold_collision_no_warning_when_one_file_filtered(self, tmp_path):
        """Pinned sys.platform: collision warning suppressed when one file is filtered."""
        import warnings as _warnings

        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Two subdirectories that differ only by case
        dir_a = source / "Sub"
        dir_b = source / "sub"
        dir_a.mkdir()
        dir_b.mkdir()
        # dir_a file requires jira (will be filtered out)
        (dir_a / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci upper\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # dir_b file requires github (will pass)
        (dir_b / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci lower\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with patch("sys.platform", "win32"):
                with _warnings.catch_warnings(record=True) as caught:
                    _warnings.simplefilter("always")
                    mock_src.side_effect = self._source_selector(source, prompts_source)
                    inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        ci_warnings = [w for w in caught if "case-insensitive" in str(w.message)]
        assert len(ci_warnings) == 0

    def test_casefold_collision_warns_when_both_files_pass(self, tmp_path):
        """Pinned sys.platform: collision warning preserved when both files pass."""
        import warnings as _warnings

        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Two subdirectories that differ only by case
        dir_a = source / "Sub"
        dir_b = source / "sub"
        dir_a.mkdir()
        dir_b.mkdir()
        # Both files require github (both pass)
        (dir_a / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci upper\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )
        (dir_b / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci lower\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with patch("sys.platform", "win32"):
                with _warnings.catch_warnings(record=True) as caught:
                    _warnings.simplefilter("always")
                    mock_src.side_effect = self._source_selector(source, prompts_source)
                    inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        ci_warnings = [w for w in caught if "case-insensitive" in str(w.message)]
        assert len(ci_warnings) == 1
