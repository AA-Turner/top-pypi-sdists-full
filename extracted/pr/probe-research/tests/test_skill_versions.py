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
    audit = _ROOT / "skills" / "audit-team-note"
    assert not (audit / "versions").exists()
    assert skill_versions.render(audit, skill_versions.WRITER) == (audit / "SKILL.md").read_text()


EDIT_NOTES = _ROOT / "skills" / "edit-notes"
EDIT_NOTES_APPROVED = APPROVED.parent / "edit-notes"
#: Richard's line for the daemon writer (daemon cost round 7, S2, OK'd 10-25), and
#: the main agent's, unchanged.
WRITER_LINE_13 = ("- Before changing one fact, find the paragraphs it touches with `probe notes find` and edit those; "
                  "read the whole note first when you restructure it. Never write from memory or from your last push.")
MAIN_LINE_13 = "- Read the whole note first. Never write from memory or from your last push."


def test_edit_notes_versions_differ_only_in_how_the_writer_reads_a_note_first():
    """Daemon cost round 7, S2: the writer finds the paragraph it changes; the
    main agent (and the plugins' copies, its render) still reads the whole note."""
    main = skill_versions.render(EDIT_NOTES, skill_versions.MAIN_AGENT)
    writer = skill_versions.render(EDIT_NOTES, skill_versions.WRITER)
    assert main == (EDIT_NOTES_APPROVED / "RENDERED.main-agent.md").read_text(encoding="utf-8")
    assert writer == (EDIT_NOTES_APPROVED / "RENDERED.writer.md").read_text(encoding="utf-8")
    assert MAIN_LINE_13 in main and WRITER_LINE_13 not in main
    assert WRITER_LINE_13 in writer and MAIN_LINE_13 not in writer
    body = main[main.index("# Notes"):]
    assert writer == body.replace(MAIN_LINE_13, WRITER_LINE_13, 1), "nothing else differs"


def test_the_plugins_edit_notes_is_the_main_agents_version():
    """The plugins carry the main agent's render (`make sync-plugin-skills`), byte for byte."""
    main = skill_versions.render(EDIT_NOTES, skill_versions.MAIN_AGENT)
    copy = _ROOT / "plugins" / "probe-research" / "agent-skills" / "edit-notes" / "SKILL.md"
    assert copy.read_text(encoding="utf-8") == main


def test_an_unknown_reader_is_refused():
    with pytest.raises(ValueError, match="unknown reader"):
        skill_versions.render(TRACK_WORK, "researcher")
