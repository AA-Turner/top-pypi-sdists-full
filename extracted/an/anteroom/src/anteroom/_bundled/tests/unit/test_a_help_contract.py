"""Tests pinning /a-help prompt behavioral contracts and CLI invocation path (#1180)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

_REPO_ROOT = Path(__file__).resolve().parents[2]
_A_HELP_PATH = _REPO_ROOT / "src" / "anteroom" / "cli" / "default_skills" / "a-help.yaml"
_SRC_ROOT = _REPO_ROOT / "src" / "anteroom"

_EXPECTED_INTROSPECT_SECTIONS = [
    "config",
    "instructions",
    "tools",
    "safety",
    "skills",
    "budget",
    "spaces",
    "package",
    "runtime",
]


@pytest.fixture(scope="module")
def _a_help_data() -> dict:
    return yaml.safe_load(_A_HELP_PATH.read_text())


@pytest.fixture(scope="module")
def _prompt(_a_help_data: dict) -> str:
    return _a_help_data["prompt"]


class TestAHelpPromptContract:
    """Pin that the a-help prompt contains required structural elements."""

    @pytest.fixture()
    def prompt(self) -> str:
        text = _A_HELP_PATH.read_text()
        data = yaml.safe_load(text)
        return data["prompt"]

    def test_docs_first_strategy(self, prompt: str) -> None:
        assert "Check the inline quick reference FIRST" in prompt

    def test_has_source_code_index(self, prompt: str) -> None:
        assert "Source Code Index" in prompt

    def test_has_introspect_guidance(self, prompt: str) -> None:
        assert "introspect section=package" in prompt

    def test_has_scope_guardrail(self, prompt: str) -> None:
        assert "Anteroom's own installed" in prompt or "do not read arbitrary user project files" in prompt

    def test_under_size_budget(self) -> None:
        size = _A_HELP_PATH.stat().st_size
        assert size < 15_000, f"a-help.yaml is {size} bytes, budget is 15,000 bytes"


class TestAHelpCliInvocationPath:
    """Verify /a-help resolves through SkillRegistry.resolve_input() — the CLI path."""

    def test_resolves_via_resolve_input(self) -> None:
        from anteroom.cli.skills import SkillRegistry

        reg = SkillRegistry()
        reg.load()
        is_skill, expanded_prompt = reg.resolve_input("/a-help how does the agent loop work?")
        assert is_skill is True
        assert "how does the agent loop work?" in expanded_prompt
        assert "Source Code Index" in expanded_prompt


class TestAHelpRuntimeIntrospectGuidance:
    """Contract tests pinning the a-help runtime introspection guidance.

    These tests catch unintended drift in the prompt's guidance around
    ``introspect section=runtime`` for session diagnostics.
    """

    def test_prompt_mentions_introspect_runtime(self, _prompt: str) -> None:
        """Strategy step must direct the AI to use introspect section=runtime for session diagnostics."""
        assert "introspect section=runtime" in _prompt

    def test_runtime_described_as_bounded_metadata(self, _prompt: str) -> None:
        """The prompt must clarify that runtime inspection yields bounded session metadata."""
        assert "bounded" in _prompt
        assert "session metadata" in _prompt

    def test_runtime_not_general_db_browsing(self, _prompt: str) -> None:
        """The prompt must explicitly disclaim general DB browsing.

        The YAML block scalar may wrap across lines, so the disclaimer is
        checked as two adjacent tokens rather than a single phrase.
        """
        # The prompt reads "— not general DB\n   browsing." across a line wrap.
        assert "not general DB" in _prompt and "browsing" in _prompt

    def test_mentions_conversation_id(self, _prompt: str) -> None:
        """Key runtime field conversation_id must be referenced."""
        assert "conversation id" in _prompt.lower() or "conversation_id" in _prompt

    def test_mentions_message_count(self, _prompt: str) -> None:
        """Key runtime field message_count must be referenced."""
        assert "message count" in _prompt.lower() or "message_count" in _prompt

    def test_mentions_token_totals(self, _prompt: str) -> None:
        """Key runtime field token_totals must be referenced."""
        assert "token_totals" in _prompt or "token totals" in _prompt.lower()

    def test_mentions_active_space(self, _prompt: str) -> None:
        """Key runtime field active_space must be referenced."""
        assert "active space" in _prompt.lower() or "active_space" in _prompt


@pytest.mark.parametrize("section", _EXPECTED_INTROSPECT_SECTIONS)
def test_introspect_section_present(_prompt: str, section: str) -> None:
    """Every expected introspect section must be referenced in the prompt.

    If a section is intentionally removed, update ``_EXPECTED_INTROSPECT_SECTIONS``
    in this file along with a comment explaining the rationale.
    """
    assert f"section={section}" in _prompt, (
        f"Expected 'section={section}' to appear in the a-help prompt, but it was not found. "
        "If this section was intentionally removed, update _EXPECTED_INTROSPECT_SECTIONS."
    )


# ---------------------------------------------------------------------------
# Live-source validation tests (#1180)
# ---------------------------------------------------------------------------


class TestIntrospectSectionsMatchLive:
    """Introspect sections in a-help.yaml must match the live introspect tool enum."""

    def test_introspect_sections_match_live(self, _prompt: str) -> None:
        from anteroom.tools.introspect import DEFINITION

        live_sections = set(DEFINITION["parameters"]["properties"]["section"]["enum"])
        prompt_sections = {s for s in live_sections if f"section={s}" in _prompt}
        assert prompt_sections == live_sections, (
            f"a-help.yaml is missing introspect sections: {live_sections - prompt_sections}"
        )


class TestDocIndexPathsExist:
    """Every docs/ path in a-help.yaml Documentation Index must exist."""

    def test_doc_index_paths_exist(self, _prompt: str) -> None:
        doc_paths: set[str] = set()
        for m in re.finditer(r"`(docs/[^`]+)`", _prompt):
            doc_paths.add(m.group(1))
        assert doc_paths, "No docs/ paths found in prompt"
        missing = sorted(p for p in doc_paths if not (_REPO_ROOT / p).is_file())
        assert not missing, "a-help.yaml references missing doc files:\n" + "\n".join(f"  - {p}" for p in missing)


class TestSourceIndexPathsExist:
    """Every source path in the Source Code Index must resolve under src/anteroom/."""

    def test_source_index_paths_exist(self, _prompt: str) -> None:
        in_source_index = False
        paths: set[str] = set()
        for line in _prompt.splitlines():
            if "## Source Code Index" in line:
                in_source_index = True
                continue
            if in_source_index and line.strip().startswith("## "):
                break
            if in_source_index and "|" in line:
                for m in re.finditer(r"`([^`]+\.py)`", line):
                    paths.add(m.group(1))
                for m in re.finditer(r"`([^`]+/)`", line):
                    paths.add(m.group(1))
        assert paths, "No source paths found in Source Code Index"
        missing: list[str] = []
        for p in sorted(paths):
            if p.endswith("/"):
                if not (_SRC_ROOT / p).is_dir():
                    missing.append(p)
            else:
                if not (_SRC_ROOT / p).is_file():
                    missing.append(p)
        assert not missing, "Source Code Index references missing paths:\n" + "\n".join(f"  - {p}" for p in missing)


class TestToolNamesMatchRegistered:
    """Core tool names in a-help.yaml must match register_default_tools()."""

    _CORE_TOOLS = {
        "read_file",
        "write_file",
        "edit_file",
        "bash",
        "glob_files",
        "grep",
        "create_canvas",
        "update_canvas",
        "patch_canvas",
        "run_agent",
        "ask_user",
        "introspect",
    }
    _OPTIONAL_TOOLS = {"docx", "xlsx", "pptx"}

    def test_tool_names_match_registered(self, _prompt: str) -> None:
        from anteroom.tools import ToolRegistry, register_default_tools

        reg = ToolRegistry()
        register_default_tools(reg)
        registered_names = set(reg._definitions.keys())
        assert self._CORE_TOOLS.issubset(registered_names), (
            f"Core tools missing from registry: {self._CORE_TOOLS - registered_names}"
        )
        for tool in self._CORE_TOOLS:
            assert tool in _prompt, f"Core tool '{tool}' not mentioned in a-help.yaml"

    def test_optional_tools_in_optional_context(self, _prompt: str) -> None:
        for tool in self._OPTIONAL_TOOLS:
            if tool in _prompt:
                idx = _prompt.index(tool)
                context = _prompt[max(0, idx - 200) : idx + 200]
                assert "optional" in context.lower() or "office" in context.lower(), (
                    f"Optional tool '{tool}' appears without optional/office context"
                )


class TestCommandsSubsetOfCanonical:
    """Slash commands in the REPL Slash Commands table must all be valid."""

    def test_commands_subset_of_canonical(self, _prompt: str) -> None:
        from anteroom.cli.commands import ALL_COMMAND_NAMES

        canonical = set(ALL_COMMAND_NAMES)
        in_table = False
        listed_commands: set[str] = set()
        for line in _prompt.splitlines():
            if "### REPL Slash Commands" in line:
                in_table = True
                continue
            if in_table and line.strip().startswith("### "):
                break
            if in_table and "|" in line:
                m = re.match(r"\s*\|\s*/(\S+)", line)
                if m:
                    listed_commands.add(m.group(1))
        assert listed_commands, "No commands found in REPL Slash Commands table"
        not_in_canonical = listed_commands - canonical
        assert not not_in_canonical, f"a-help.yaml lists commands not in ALL_COMMAND_NAMES: {not_in_canonical}"
