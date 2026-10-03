"""pi briefs a session with the team note only where the CLI would render it.

The CLI renders the team note only into an instruction file that carries Probe's
pointer block (no pointer, no note: the absent block IS the `--no-agent-rules`
opt-out). pi gets the note injected into its prompt instead of rendered, so the
extension checks pi's `AGENTS.md` for the same block itself
(`plugins/probe-research-pi/src/core/teamNote.ts::hasProbePointer`). Its copy of the
markers and of the file it reads must be the CLI's, or pi would brief an
opted-out session, or silence an opted-in one.
"""

from __future__ import annotations

from pathlib import Path

from probe.cli import agent_rules
from tests.ts_source import ts_string

PI_CORE = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-pi" / "src" / "core"


def test_the_pointer_markers_are_agent_rules():
    assert ts_string(PI_CORE / "teamNote.ts", "POINTER_BEGIN_MARKER") == agent_rules.BEGIN_MARKER
    assert ts_string(PI_CORE / "teamNote.ts", "POINTER_END_MARKER") == agent_rules.END_MARKER
    assert (agent_rules.POINTER_BLOCK.begin, agent_rules.POINTER_BLOCK.end) == (
        agent_rules.BEGIN_MARKER,
        agent_rules.END_MARKER,
    )


def test_the_file_checked_is_the_one_the_wizard_writes(tmp_path, monkeypatch):
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path))
    assert agent_rules.memory_path("pi") == tmp_path / ts_string(PI_CORE / "paths.ts", "PI_AGENTS_FILE")


def test_a_damaged_block_counts_on_both_sides(tmp_path):
    """`has_block` is the Python twin: either marker is enough."""
    path = tmp_path / "AGENTS.md"
    for text, expected in (
        (agent_rules.BEGIN_MARKER + "\nbody\n" + agent_rules.END_MARKER + "\n", True),
        (agent_rules.BEGIN_MARKER + "\nbody\n", True),
        ("body\n" + agent_rules.END_MARKER + "\n", True),
        ("# my own rules\n", False),
    ):
        path.write_text(text, encoding="utf-8")
        assert agent_rules.has_block(path, agent_rules.POINTER_BLOCK) is expected
    source = (PI_CORE / "teamNote.ts").read_text(encoding="utf-8")
    assert "text.includes(POINTER_BEGIN_MARKER) || text.includes(POINTER_END_MARKER)" in source
