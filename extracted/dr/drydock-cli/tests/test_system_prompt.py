from __future__ import annotations

import sys

import pytest

from tests.conftest import build_test_drydock_config
from drydock.core.agents import AgentManager
from drydock.core.skills.manager import SkillManager
from drydock.core.system_prompt import get_universal_system_prompt
from drydock.core.tools.manager import ToolManager


def test_get_universal_system_prompt_includes_windows_prompt_on_windows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setenv("COMSPEC", "C:\\Windows\\System32\\cmd.exe")

    config = build_test_drydock_config(
        system_prompt_id="tests",
        include_project_context=False,
        include_prompt_detail=True,
        include_model_info=False,
        include_commit_signature=False,
    )
    tool_manager = ToolManager(lambda: config)
    skill_manager = SkillManager(lambda: config)
    agent_manager = AgentManager(lambda: config)

    prompt = get_universal_system_prompt(
        tool_manager, config, skill_manager, agent_manager
    )

    assert "You are Vibe, a super useful programming assistant." in prompt
    assert (
        "The operating system is Windows with shell `C:\\Windows\\System32\\cmd.exe`"
        in prompt
    )
    assert "DO NOT use Unix commands like `ls`, `grep`, `cat`" in prompt
    assert "Use: `dir` (Windows) for directory listings" in prompt
    assert "Use: backslashes (\\\\) for paths" in prompt
    assert "Check command availability with: `where command` (Windows)" in prompt
    assert "Script shebang: Not applicable on Windows" in prompt


def test_cli_md_investigate_permits_artifact_writes() -> None:
    """Investigate branch must not block write_file for explicitly-requested output files.

    Regression for: comprehension test cases asking "write to ANSWER.md" were
    silently blocked because "Do not edit files" was too broad.
    """
    import pathlib
    cli_md = (pathlib.Path(__file__).parent.parent / "drydock" / "core" / "prompts" / "cli.md").read_text()
    # Must allow writing named output artifacts in investigate mode
    assert "write your answer to" in cli_md or "named output file" in cli_md, (
        "cli.md investigate branch must permit writing explicit output artifacts"
    )
    # Must not have the old blanket ban
    assert "Do not edit files." not in cli_md, (
        "cli.md must not blanket-ban all file edits in investigate mode"
    )
