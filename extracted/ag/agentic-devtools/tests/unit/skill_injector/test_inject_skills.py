"""End-to-end skill injection scenarios."""

from unittest.mock import patch

from agentic_devtools.skill_injector import inject_skills


class TestInjectSkills:
    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

    def test_returns_false_when_git_root_is_none(self):
        """Returns False when git_root is None."""
        assert inject_skills(None) is False

    def test_creates_target_dirs_if_missing(self, tmp_path):
        """Creates .github/agents/ and .github/prompts/ directories with agdt.README.md."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            result = inject_skills(tmp_path)

        assert result is True
        assert (tmp_path / ".github" / "agents").is_dir()
        assert (tmp_path / ".github" / "prompts").is_dir()
        assert (tmp_path / ".github" / "agents" / "agdt.README.md").exists()
        assert (tmp_path / ".github" / "prompts" / "agdt.README.md").exists()
