"""Recover per-tool-call timing that ATIF drops in translation.

ATIF's ``ToolCall`` is ``tool_call_id`` / ``function_name`` / ``arguments`` /
``extra`` and nothing else -- ``model_config = {"extra": "forbid"}``, so there
is nowhere for a timestamp to live even if a producer wanted to send one. But
the agent's OWN transcript, which Harbor captures verbatim as a trial file, does
timestamp every message. So the numbers are not unmeasurable; they were
projected away, and this reads them back out of the artifact Harbor already
stored.

WHAT THIS DOES AND DOES NOT MEASURE
-----------------------------------

Claude Code dispatches every ``tool_use`` block in one assistant message
together, then records each ``tool_result`` as it arrives::

    assistant  10:00:00   tool_use rg          ┐ one dispatch instant
                          tool_use read_file   ┘ shared by both calls
    user       10:00:03   tool_result (rg)
    user       10:00:07   tool_result (read_file)

So the START is real but SHARED across a batch, and each END is real and its
own. A call's extent is therefore dispatch-to-result: exact when the batch ran
concurrently, an upper bound when the agent serialized it. That is a genuinely
better number than the inferred next-step gap it replaces -- it never includes
the following turn's inference latency -- and it is still a bound, which is why
it carries its own ``timing_source`` rather than being folded into the ATIF
vocabulary.

THIS IS PER-AGENT, AND THAT IS NOT A BUG TO FIX LATER
-----------------------------------------------------

Harbor ships ~40 agent adapters and each writes its own native transcript. This
module reads Claude Code's. Every other agent keeps the inferred timing, which
is exactly why ``elapsed_ms`` and ``elapsed_source`` stay: they are the floor,
not a deprecated fallback. ``coverage`` reports how much of a trial this
actually reached so a reader can tell a trial with real tool timing from one
without, instead of guessing from whether a bar looks solid.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

#: Provenance for an end recovered from the agent's own transcript.
TOOL_TIMING_SOURCE_SESSION_LOG = "agent_session_log"

#: Stamped when a call shared its dispatch instant with siblings, so a reader
#: can tell "these three ran together" from "this one took that long".
TOOL_TIMING_BATCHED = "batched_dispatch"

#: Hard ceilings on a file a TRIAL controls. A transcript is captured from
#: inside a sandbox, so its size is an attacker-influenced input, not a fact:
#: without a cap a single enormous line (or a symlink to /dev/zero) hangs or
#: OOMs the capture worker for every other trial in the run.
MAX_LOG_BYTES = 64 * 1024 * 1024
MAX_LOG_LINE_BYTES = 4 * 1024 * 1024
MAX_TOOL_CALLS = 100_000

#: Only Claude Code's transcript is understood today. Named so a caller can
#: check before paying for a parse, and so the skip is explicit in reports.
SUPPORTED_AGENTS = frozenset({"claude-code"})


class ToolTiming:
    """One tool call's recovered window."""

    __slots__ = ("started_at", "ended_at", "batched")

    def __init__(self, started_at: str, ended_at: str, batched: bool):
        self.started_at = started_at
        self.ended_at = ended_at
        self.batched = batched

    def attributes(self) -> dict[str, Any]:
        out: dict[str, Any] = {"timing_source": TOOL_TIMING_SOURCE_SESSION_LOG}
        if self.batched:
            out["dispatch"] = TOOL_TIMING_BATCHED
        return out


def _instant(value: Any) -> datetime | None:
    """A tz-aware datetime, or ``None`` for anything we refuse to order on.

    Timestamps here come from inside the sandbox, so they are untrusted STRINGS
    until parsed. Comparing them as strings would order ``10:00+02:00`` before
    ``09:00Z`` even though the second instant is later, and would happily accept
    ``"a" < "b"`` as a duration.
    """
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _lines(path: Path) -> Iterator[dict]:
    """Every parseable JSON object in a JSONL file, under a hard byte ceiling.

    A corrupt line is skipped rather than failing the trial: this is an
    enrichment over a capture that already succeeded, and losing one tool call's
    end is a smaller harm than losing the whole ingest. An OVERSIZED file is a
    different thing and stops the read outright -- a trial does not get to
    decide how much memory the capture worker spends on it.
    """
    if path.is_symlink():
        # The path is inside a directory the trial wrote. A symlink there can
        # point at /dev/zero, a socket, or anything else outside the capture
        # scope; reading it is the trial choosing what we read.
        return
    try:
        if path.stat().st_size > MAX_LOG_BYTES:
            return
    except OSError:
        return
    budget = MAX_LOG_BYTES
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                budget -= len(line)
                if budget <= 0:
                    return
                if len(line) > MAX_LOG_LINE_BYTES:
                    continue
                line = line.strip()
                if not line:
                    continue
                try:
                    value = json.loads(line)
                except ValueError:
                    continue
                if isinstance(value, dict):
                    yield value
    except OSError:
        return


def _content(event: dict) -> list[dict]:
    message = event.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, list):
        return [block for block in content if isinstance(block, dict)]
    return []


def parse_session_log(path: Path) -> dict[str, ToolTiming]:
    """``{tool_use_id: ToolTiming}`` from one Claude Code session transcript.

    Ids are the join key and they are EXACT: ATIF's ``tool_call_id`` is Claude's
    own ``toolu_...`` string, carried through the adapter untouched. Nothing
    here matches on name, index or position.

    A call whose result never arrived -- the agent was killed, the trial timed
    out -- is absent rather than closed at the transcript's end. An aborted call
    has no measured end, and inventing one would put a duration on work that
    never finished.
    """
    dispatched: dict[str, tuple[str, datetime, bool]] = {}
    timings: dict[str, ToolTiming] = {}
    for event in _lines(path):
        timestamp = event.get("timestamp")
        instant = _instant(timestamp)
        if instant is None:
            continue
        blocks = _content(event)
        uses = [b for b in blocks if b.get("type") == "tool_use" and b.get("id")]
        for block in uses:
            if len(dispatched) >= MAX_TOOL_CALLS:
                break
            dispatched[str(block["id"])] = (timestamp, instant, len(uses) > 1)
        for block in blocks:
            if block.get("type") != "tool_result":
                continue
            call_id = block.get("tool_use_id")
            if not isinstance(call_id, str):
                continue
            start = dispatched.get(call_id)
            # A result with no dispatch is a transcript we do not understand
            # well enough to time. Skip it rather than anchoring the call to
            # whatever timestamp happens to be nearby.
            if start is None:
                continue
            started_at, started_instant, batched = start
            # Parsed instants, never the raw strings: two stamps can be
            # correctly ordered and lexically reversed at the same time.
            if instant < started_instant:
                continue
            timings[call_id] = ToolTiming(started_at, timestamp, batched)
    return timings


def session_log_path(trial_dir: Path) -> Path | None:
    """The Claude Code session transcript inside a captured trial directory.

    Harbor stores it under ``agent/sessions/projects/<slug>/<uuid>.jsonl``. More
    than one means a resumed or forked session and there is no non-arbitrary way
    to pick, so this declines rather than guessing -- the trial keeps inferred
    timing and the report says why.
    """
    root = trial_dir / "agent" / "sessions" / "projects"
    if not root.is_dir() or root.is_symlink():
        return None
    found = [p for p in sorted(root.glob("*/*.jsonl")) if p.is_file() and not p.is_symlink()]
    return found[0] if len(found) == 1 else None


def agent_is_supported(agent_info: Any) -> bool:
    """Whether this trial's agent writes a transcript shape we can read."""
    name = agent_info.get("name") if isinstance(agent_info, dict) else None
    return isinstance(name, str) and name in SUPPORTED_AGENTS


def coverage(timings: dict[str, ToolTiming], tool_call_ids: list[str]) -> dict[str, Any]:
    """How much of this trial's tool timing is measured rather than inferred."""
    matched = sum(1 for call_id in tool_call_ids if call_id in timings)
    return {
        "tool_calls": len(tool_call_ids),
        "measured": matched,
        "source": TOOL_TIMING_SOURCE_SESSION_LOG,
    }
