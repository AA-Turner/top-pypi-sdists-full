"""The shared conformance suite for daemon harness adapters (D23).

Every adapter runs the SAME tests against its own three recorded, scrubbed
sessions (`tests/fixtures/daemon_adapters/<harness>/session{1,2,3}.jsonl`;
structure only, made with `scrub.py` -- real transcripts are never committed).
Adding a harness = an adapter module + three fixtures + this suite passing.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from probe.daemon import adapters
from probe.daemon.adapters.base import MODE_BYPASS, MODE_DEFAULT, Capabilities
from probe.daemon.events import Kind

FIXTURES = Path(__file__).parent / "fixtures" / "daemon_adapters"
HARNESSES = adapters.known()


def _events(harness: str, path: Path):
    a = adapters.for_source(harness)
    out, off, modes = [], 0, []
    for raw in path.read_bytes().splitlines(keepends=True):
        off += len(raw)
        try:
            obj = json.loads(raw)
        except ValueError:
            continue
        mode = a.permission_mode(obj)
        if mode:
            modes.append(mode)
        out.extend(a.parse_bytes(raw.rstrip(b"\n"), stream="main", offset=off))
    return a, out, modes


@pytest.mark.parametrize("harness", HARNESSES)
def test_every_adapter_has_three_fixtures(harness):
    assert sorted(p.name for p in (FIXTURES / harness).glob("session*.jsonl")) == [
        "session1.jsonl", "session2.jsonl", "session3.jsonl"]


@pytest.mark.parametrize("harness", HARNESSES)
@pytest.mark.parametrize("n", [1, 2, 3])
def test_events_are_normalized_ordered_and_labelled(harness, n):
    a, events, modes = _events(harness, FIXTURES / harness / f"session{n}.jsonl")
    assert events, "a real session yields events"
    assert all(isinstance(e.kind, Kind) for e in events)
    offsets = [(e.offset, e.index) for e in events]
    assert offsets == sorted(offsets), "events come out in log order"
    assert len({e.event_id for e in events}) == len(events), "event ids are unique and stable"
    kinds = {e.kind for e in events}
    assert Kind.TOOL_CALL in kinds and Kind.TOOL_OUTPUT in kinds
    assert Kind.PROMPT in kinds or Kind.META in kinds
    calls = {e.call_id for e in events if e.kind == Kind.TOOL_CALL and e.call_id}
    answered = [e for e in events if e.kind == Kind.TOOL_OUTPUT and e.call_id]
    assert any(e.call_id in calls for e in answered), "outputs are tied to the calls that made them"
    for e in events:
        if e.kind == Kind.PROMPT:
            assert e.stream == "main" and not e.text.lstrip().startswith(("<task-notification>", "Caveat:"))
    # Re-parsing the same bytes gives the same ids: the store's idempotency rests on this.
    _, again, _ = _events(harness, FIXTURES / harness / f"session{n}.jsonl")
    assert [e.event_id for e in again] == [e.event_id for e in events]
    for mode in modes:
        assert mode in (MODE_BYPASS, MODE_DEFAULT)


@pytest.mark.parametrize("harness", HARNESSES)
def test_turn_ends_are_found(harness):
    found = sum(1 for n in (1, 2, 3) for e in _events(harness, FIXTURES / harness / f"session{n}.jsonl")[1]
                if e.kind == Kind.TURN_END)
    assert found >= 1


@pytest.mark.parametrize("harness", HARNESSES)
def test_the_capability_table_matches_what_the_adapter_does(harness):
    a = adapters.for_source(harness)
    caps = a.capabilities
    assert isinstance(caps, Capabilities)
    # A question tool is only claimed with a tool name and the hooks to read its answer.
    assert caps.question_tool == bool(a.question_tool_name)
    if caps.question_tool:
        assert caps.hooks
    if caps.question_tool:
        # Asking through the agent needs the one-line nudge at the next prompt.
        assert caps.inject_line
    # Daemon reads: a message after a tool call, and the wake, are hooks -- or,
    # on pi, its extension (probe-research-pi/src/reads.ts).
    if caps.inject_tool or caps.wake:
        assert caps.hooks or harness == "pi"
    assert caps.instruction_files, "every harness names its instruction files"


def test_daemon_reads_delivery_capabilities_per_harness():
    """Claude Code delivers after tool calls and wakes a finished turn (T3);
    Codex delivers after tool calls with no wake, pi through its extension, which
    steers a message in and can start a turn (T11)."""
    caps = {name: adapters.for_source(name).capabilities for name in HARNESSES}
    assert {name: (c.inject_tool, c.wake) for name, c in caps.items()} == {
        "claude_code": (True, True),
        "codex": (True, False),
        "pi": (True, True),
    }


@pytest.mark.parametrize("harness", HARNESSES)
def test_context_files_are_found_where_they_exist(harness, tmp_path):
    a = adapters.for_source(harness)
    home = tmp_path / "home"
    repo = home / "repo"
    (repo / ".git").mkdir(parents=True)
    for name in a.capabilities.instruction_files:
        (repo / name).write_text("instructions for the coding agent")
    found = a.context_files(repo, home)
    assert any(f.path.parent == repo for f in found)
    assert all(f.path.is_file() or f.path.is_dir() for f in found)
