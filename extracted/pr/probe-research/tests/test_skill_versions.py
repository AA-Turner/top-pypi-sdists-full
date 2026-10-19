"""`track-work` is one base and two versions (Richard 2026-09-28): the main
agent reads its version in the plugins, the daemon's writer reads its own in the
daemon's instructions, and neither sees the other's header or footer. The
writer's `bash` commands are an extra of its version, shown only with that tool
set (10-19). The approved renders are copied under fixtures/daemon_prompts/reads/skills/.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from probe import skill_versions
from probe.daemon import bite as bite_mod
from probe.daemon import toolset

_ROOT = Path(__file__).resolve().parent.parent
TRACK_WORK = _ROOT / "skills" / "track-work"
APPROVED = Path(__file__).parent / "fixtures" / "daemon_prompts" / "reads" / "skills" / "track-work"


def _lines(name: str) -> list[str]:
    """The distinctive lines of a header or footer (its title line is shared)."""
    text = (TRACK_WORK / "versions" / name).read_text(encoding="utf-8")
    return [line for line in text.splitlines() if line.strip() and line.strip() != "# Track work"]


def test_each_version_is_the_approved_render():
    assert skill_versions.render(TRACK_WORK, skill_versions.MAIN_AGENT) == (
        APPROVED / "RENDERED.main-agent.md").read_text(encoding="utf-8")
    assert skill_versions.render(TRACK_WORK, skill_versions.WRITER, (bite_mod.WRITER_COMMANDS, bite_mod.WRITER_TASK)) \
        == (APPROVED / "RENDERED.writer.md").read_text(encoding="utf-8")


def test_no_version_carries_the_other_readers_text():
    main = skill_versions.render(TRACK_WORK, skill_versions.MAIN_AGENT)
    writer = skill_versions.render(TRACK_WORK, skill_versions.WRITER, (bite_mod.WRITER_COMMANDS, bite_mod.WRITER_TASK))
    for line in _lines("header.writer.md") + _lines("footer.writer.md"):
        assert line not in main, line
    for extra in ("commands.writer.md", "task.writer.md"):
        piece = (TRACK_WORK / "versions" / extra).read_text(encoding="utf-8").strip()
        assert piece in writer and piece not in main, extra
    assert "probe draft edit" not in main and "probe daemon task" not in main
    for line in _lines("header.main-agent.md"):
        assert line not in writer, line
    assert "--evidence" not in main, "the daemon-only option stays the writer's"
    assert main.startswith("---\nname: track-work\n") and not writer.startswith("---")


def test_the_writer_reads_its_own_version(monkeypatch):
    monkeypatch.setattr(bite_mod, "skills_root", lambda: _ROOT / "skills")
    text = bite_mod.skills_text()
    writer = bite_mod.writer_skill(TRACK_WORK).strip()
    assert f"# Skill: track-work\n\n{writer}" in text
    assert "You are the main agent" not in text


def test_the_writer_sees_its_commands_only_with_the_bash_tool_set(monkeypatch):
    """Review 10-19: under the kill switch the writer has no `bash`, so its
    commands are left out; with tasks off, its `probe daemon task` piece, and
    nothing else."""
    approved = (APPROVED / "RENDERED.writer.md").read_text(encoding="utf-8")
    task = (TRACK_WORK / "versions" / "task.writer.md").read_text(encoding="utf-8").strip()
    monkeypatch.setenv(toolset.TOOLS_ENV, "bash")
    monkeypatch.delenv(toolset.TASKS_ENV, raising=False)
    assert bite_mod.writer_skill(TRACK_WORK) == approved
    monkeypatch.setenv(toolset.TASKS_ENV, "0")
    assert bite_mod.writer_skill(TRACK_WORK) == approved.replace(task + "\n\n", "", 1)
    assert "probe daemon task" not in bite_mod.writer_skill(TRACK_WORK)
    monkeypatch.setenv(toolset.TOOLS_ENV, "classic")
    classic = bite_mod.writer_skill(TRACK_WORK)
    assert classic == skill_versions.render(TRACK_WORK, skill_versions.WRITER)
    assert "`bash`" not in classic and "probe draft edit" not in classic and "probe daemon task" not in classic


def test_a_skill_without_versions_is_its_skill_file():
    edit_notes = _ROOT / "skills" / "edit-notes"
    assert skill_versions.render(edit_notes, skill_versions.WRITER) == (edit_notes / "SKILL.md").read_text()


def test_an_unknown_reader_is_refused():
    with pytest.raises(ValueError, match="unknown reader"):
        skill_versions.render(TRACK_WORK, "researcher")
