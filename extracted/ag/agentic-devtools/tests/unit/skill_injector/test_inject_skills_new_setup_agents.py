"""Tests for inject_skills including the three new setup agents."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.skill_injector import inject_skills

_AGENT_FILES = [
    "agdt.run-setup.agent.md",
    "agdt.report-setup-bug.agent.md",
    "agdt.report-setup-feature.agent.md",
]

_PROMPT_FILES = [
    "agdt.run-setup.prompt.md",
    "agdt.report-setup-bug.prompt.md",
    "agdt.report-setup-feature.prompt.md",
]

_AGENT_CONTENTS = {
    "agdt.run-setup.agent.md": (
        '---\ndescription: "Run Setup: Orchestrated setup with fix-loop"\nagdt:\n  always: true\n---\n## User Input\n'
    ),
    "agdt.report-setup-bug.agent.md": (
        '---\ndescription: "Report Setup Bug: File a sanitized bug report"\nagdt:\n  always: true\n---\n## User Input\n'
    ),
    "agdt.report-setup-feature.agent.md": (
        '---\ndescription: "Report Setup Feature: File a feature request"\nagdt:\n  always: true\n---\n## User Input\n'
    ),
}

_PROMPT_CONTENTS = {
    "agdt.run-setup.prompt.md": "---\nagent: agdt.run-setup\nagdt:\n  always: true\n---\n",
    "agdt.report-setup-bug.prompt.md": "---\nagent: agdt.report-setup-bug\nagdt:\n  always: true\n---\n",
    "agdt.report-setup-feature.prompt.md": "---\nagent: agdt.report-setup-feature\nagdt:\n  always: true\n---\n",
}


class TestInjectSkillsNewSetupAgents:
    """Verify inject_skills copies all six new setup agent/prompt files."""

    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

    def test_all_six_files_present_after_injection(self, tmp_path) -> None:
        """All 3 agent files and 3 prompt files are injected into target."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        for name, content in _AGENT_CONTENTS.items():
            (agents_source / name).write_text(content, encoding="utf-8")

        for name, content in _PROMPT_CONTENTS.items():
            (prompts_source / name).write_text(content, encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            result = inject_skills(tmp_path)

        assert result is True

        agents_target = tmp_path / ".github" / "agents"
        prompts_target = tmp_path / ".github" / "prompts"

        for name in _AGENT_FILES:
            assert (agents_target / name).exists(), f"Missing agent file: {name}"

        for name in _PROMPT_FILES:
            assert (prompts_target / name).exists(), f"Missing prompt file: {name}"

    def test_readme_manifest_includes_all_three_agents(self, tmp_path) -> None:
        """agdt.README.md manifest includes all three agents with descriptions."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        for name, content in _AGENT_CONTENTS.items():
            (agents_source / name).write_text(content, encoding="utf-8")

        for name, content in _PROMPT_CONTENTS.items():
            (prompts_source / name).write_text(content, encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path)

        readme = (tmp_path / ".github" / "agents" / "agdt.README.md").read_text(encoding="utf-8")

        assert "agdt.run-setup.agent.md" in readme
        assert "agdt.report-setup-bug.agent.md" in readme
        assert "agdt.report-setup-feature.agent.md" in readme
        # Descriptions should appear in manifest
        assert "Run Setup" in readme
        assert "Report Setup Bug" in readme
        assert "Report Setup Feature" in readme
