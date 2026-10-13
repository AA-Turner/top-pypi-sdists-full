"""The daemon profile's `visualize-progress` (Richard 2026-10-12: "Added to the
daemon mode as well").

The lean plugin's copy is hand-kept: in the daemon profile the agent cannot
read Probe (the guard refuses every read but `probe ask` and `probe session
status`), so it asks the daemon once and draws from the answer. Only WHERE a
fact comes from differs from the canonical skill; the drawing is the same
doctrine, held to it here section by section, and cell by cell in its tables,
so the two cannot drift.
"""

from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path

import pytest

import probe
from probe.sdk import session_marker
from probe.sdk.run import Run
from tests.test_skills_commands_exist import _invocations

AGENT = Path(__file__).resolve().parents[1]
CANONICAL = AGENT / "skills" / "visualize-progress" / "SKILL.md"
DAEMON = AGENT / "plugins" / "probe-research-daemon" / "agent-skills" / "visualize-progress" / "SKILL.md"

#: The one line of shared doctrine the daemon copy words differently: the
#: example's next action. `probe artifact add` from the agent's own shell is
#: the daemon's write in this profile (`DAEMON_RUN_WRITES`); the SDK call in
#: the run is the same write, the run's own.
SWAPS = {
    " NEXT  probe artifact add tunneling-sambar-254 ckpt-4000.pt --name ckpt":
        ' NEXT  probe.log_artifact("ckpt", path="ckpt-4000.pt") in the training loop',
}

#: Table rows whose rule the daemon copy words differently, and why.
CELL_SWAPS = {
    # Canonical names the outbox; the guard refuses `probe outbox status`.
    ("## THE STATUS BLOCK:", "`missing`"),
    # Canonical reads the project card's notes excerpt; the daemon's answer carries it.
    ("## THE STATUS BLOCK:", "`attention`"),
    # "tracking OFF" here is `read only (daemon)`: under `off` the ask is refused.
    ("## THE STATUS BLOCK:", "`tracking`"),
    # "the record" is the execution record `reproduce` names, an MCP read here.
    ("## THE TIMELINE:", "snapshot"),
    # `snapshot-restore --verify-only` is refused in this profile.
    ("## THE TIMELINE:", "inputs captured"),
}


def _sections(path: Path) -> dict[str, str]:
    """Heading line -> the text under it, up to the next heading of any level."""
    out: dict[str, str] = {}
    heading = None
    lines: list[str] = []
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and re.match(r"^#{2,3} ", line):
            if heading is not None:
                out[heading] = "\n".join(lines)
            heading, lines = line, []
        elif heading is not None:
            lines.append(line)
    if heading is not None:
        out[heading] = "\n".join(lines)
    return out


def _swapped(text: str) -> str:
    for canonical, daemon in SWAPS.items():
        text = text.replace(canonical, daemon)
    return text


def _prose(text: str) -> str:
    """The section without its table: the daemon copy drops "read it from"."""
    return "\n".join(line for line in text.splitlines() if not line.startswith("|"))


def _rows(text: str) -> dict[str, str]:
    """First cell -> second cell, past the header and the rule."""
    rows = [line for line in text.splitlines() if line.startswith("| ")][2:]
    return {row.split("|")[1].strip(): row.split("|")[2].strip() for row in rows}


CANON, LEAN = _sections(CANONICAL), _sections(DAEMON)


def test_the_two_copies_have_the_same_sections_in_the_same_order():
    assert list(LEAN) == list(CANON)


def test_the_front_matter_is_the_canonical_skills():
    assert DAEMON.read_text().split("---", 2)[1] == CANONICAL.read_text().split("---", 2)[1]


@pytest.mark.parametrize("heading", ["### Glyphs", "### Draw it", "## CLOSE WITH ONE NEXT ACTION:"])
def test_the_drawing_is_the_canonical_doctrine(heading):
    assert LEAN[heading] == _swapped(CANON[heading]), (
        f"{heading} drifted from skills/visualize-progress: edit both, or add the difference to SWAPS")


def test_every_swap_still_matches_the_canonical_text():
    canonical = CANONICAL.read_text()
    for line in SWAPS:
        assert line in canonical, f"SWAPS names a line skills/visualize-progress no longer has: {line!r}"
    for heading, key in CELL_SWAPS:
        assert key in _rows(CANON[heading]), f"CELL_SWAPS names a row canonical no longer has: {key}"


@pytest.mark.parametrize("heading", ["## THE STATUS BLOCK:", "## THE TIMELINE:"])
def test_the_status_block_and_timeline_differ_only_where_a_read_differs(heading):
    assert _prose(LEAN[heading]) == _prose(CANON[heading])
    lean, canon = _rows(LEAN[heading]), _rows(CANON[heading])
    assert list(lean) == list(canon), "same lines and stages, same order"
    for key, rule in canon.items():
        if (heading, key) not in CELL_SWAPS:
            assert lean[key] == rule, f"{key}: its rule drifted from skills/visualize-progress"


def test_it_asks_the_daemon_and_names_no_command_the_profile_refuses():
    """Inline spans AND fenced blocks (`_invocations`): the fenced NEXT line is
    the one a reader copies, and a backtick-only scan passed with canonical's
    refused `probe artifact add` sitting in it."""
    text = DAEMON.read_text()
    assert "probe ask --wait '<question>'" in text, "single quotes: backticks in the question must not run"
    commands = _invocations(text)
    assert "ask" in commands and "session status" in commands
    for command in commands:
        allowed, matched = session_marker.daemon_profile_allows(command.split())
        assert allowed, f"the daemon-profile guard refuses `{matched}`, which the skill tells the agent to run"


def test_the_command_scan_sees_a_refused_command_in_a_fence():
    fenced = "```\n NEXT  probe artifact add r ckpt.pt --name ckpt\n```\n"
    assert not all(session_marker.daemon_profile_allows(c.split())[0] for c in _invocations(fenced))


def test_every_sdk_call_it_shows_binds_to_the_real_signature():
    """The example NEXT is copied into training loops: a call the SDK rejects
    crashes the run at its first checkpoint."""
    calls = re.findall(r"probe\.(\w+)\((.*?)\)(?=\s|$)", DAEMON.read_text(), re.MULTILINE)
    assert calls, "the skill shows no SDK call"
    for name, args in calls:
        call = ast.parse(f"f({args})", mode="eval").body
        positional = [ast.literal_eval(a) for a in call.args]
        keywords = {k.arg: ast.literal_eval(k.value) for k in call.keywords}
        method = getattr(Run, name, None)
        if method is not None:  # the fluent `probe.X` forwards **kw to `Run.X`
            inspect.signature(method).bind(None, *positional, **keywords)
        else:
            inspect.signature(getattr(probe, name)).bind(*positional, **keywords)


def test_it_names_no_mcp_read_and_no_skill_the_profile_lacks():
    """The daemon-profile agent has no MCP and is told nothing about it
    (Richard 2026-09-27: only the SDK and some probe CLI commands), and the
    profile ships no `track-work`."""
    text = DAEMON.read_text()
    # Backticked: "at handoff" is the doctrine's own English, `handoff` the tool.
    words = ("`browse`", "`entity", "`handoff`", "`reproduce`", "snapshot-restore", "outbox status", "`track-work`")
    for word in ("MCP", "view=", *words):
        assert word not in text, word
    for word in words:
        assert word in CANONICAL.read_text(), f"{word} left the canonical skill: this guard checks nothing"
