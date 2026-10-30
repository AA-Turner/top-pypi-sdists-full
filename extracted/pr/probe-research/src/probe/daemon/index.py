"""The writer's event indexer (daemon cost round 5).

With `WriterEvents.INDEX` a run's new events reach the writer as an index: a
cheap model -- the server's `index` alias, on its own lane (`model.LANE_INDEX`) --
writes one line per step with the event ids where it happened, and the writer
opens the raw events (`session` op=open / op=search) for anything it records.
Measured 10-13 on a 2.9 h session: the same cost as the raw events with a
lean history, 7/7 checks in both runs (raw: 7 and 6).

Plain code, not the model, keeps what must not be paraphrased: the researcher's
prompts, the main agent's requests to the writer, the reader's messages and the
daemon's own notices are shown whole,
and the events between them are indexed one stretch per call: at most about
STRETCH_TOKENS each as the writer would read them (a file burst a list, a file
change one line: `bite.rendered_groups`), at most CONCURRENT_CALLS at once. An
id the model did not get is removed from its line, and a line left with no id
says so. Any failure of a call -- an error, a refusal (the server answers one
with an error on this lane), a timeout, an empty answer -- shows that stretch
raw.
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass
from typing import Any

from probe.daemon import toolset
from probe.daemon.bite import CHARS_PER_TOKEN, NOTICE_STREAM, render, rendered_groups
from probe.daemon.events import READER_SOURCE, REQUEST_SOURCE, Kind
from probe.daemon.store import StoredEvent

log = logging.getLogger("probe.daemon")

#: One index call's time limit (the server's deadline on this lane is 30 s too):
#: past it that stretch goes raw.
INDEX_TIMEOUT_S = 30.0
#: One call's stretch, about this many tokens at most (swarm friction T19): a
#: whole backlog in one call ran past the proxy's limit (183 of 1,191 index calls
#: failed in the 10-28 swarm, each then shown raw to the writer).
STRETCH_TOKENS = 8_000
#: At most this many index calls at once: they share the writer's slots on the
#: model route.
CONCURRENT_CALLS = 2

INSTRUCTIONS = """You index part of a coding session for a recorder that files the session's ML work in a tracking system. The recorder can open any event by its id, so write an index, not a copy.

Each event starts with a tag in square brackets that holds its id, like `main:1234:0`. Write one short line per step of the work, in order: what was done, decided or found, then the id(s) where it is, like `(main:1234:0)`. Name results ("results for X") without copying their numbers, unless a number is the point of the step. Skip anything that is not about the work.
Reply with the index only."""

#: What the writer reads above an index.
HEADER = ("(An index of these events, made by a smaller model: one line per step with its event ids. It leaves "
          "numbers, paths and commands out. Open the events for anything you record: `session` op=open "
          "event_id=<id>, or op=search query=<words>.)")
#: The same with the `bash` tool set (NEW wording, fixtures/daemon_prompts/bite/bash-markers.NEW.md).
HEADER_BASH = ("(An index of these events by a smaller model: one line per step with its event ids, no numbers, "
               "paths or commands. Open the events for anything you record: `probe daemon session open <id>` or "
               "`probe daemon session search \"<words>\"`.)")
NO_SOURCE = " (no source: search before recording it)"
_ID = re.compile(r"\b[A-Za-z][\w.-]*:\d+:\d+\b")


@dataclass
class Indexed:
    """A run's new events as the writer reads them, and what making it cost."""

    text: str
    #: The (first, last) seq of the events indexed (set by the worker).
    span: tuple[int, int] | None = None
    calls: int = 0
    failed: int = 0
    bad_ids: int = 0
    usd: float = 0.0

    def facts(self) -> dict[str, Any]:
        """For the run's trace."""
        return {"index_calls": self.calls, "index_failed": self.failed, "index_bad_ids": self.bad_ids,
                "index_usd": round(self.usd, 6)}


def shown_whole(ev: StoredEvent) -> bool:
    """Events plain code shows whole, never through the model."""
    return (ev.kind == Kind.PROMPT or ev.source in (READER_SOURCE, REQUEST_SOURCE)
            or (ev.kind == Kind.META and ev.stream == NOTICE_STREAM))


def stretches(events: list[StoredEvent]) -> list[tuple[bool, list[StoredEvent]]]:
    """`events` in order, as (shown whole, events): each whole one alone, the
    others in runs between them."""
    out: list[tuple[bool, list[StoredEvent]]] = []
    for ev in events:
        whole = shown_whole(ev)
        if not whole and out and not out[-1][0]:
            out[-1][1].append(ev)
        else:
            out.append((whole, [ev]))
    return out


def checked(text: str, known: set[str]) -> tuple[str, int]:
    """`text` with every id not in `known` removed, and a line left with none
    marked; the number of ids removed."""
    bad = 0
    lines = []
    for line in text.splitlines():
        ids = _ID.findall(line)
        for found in ids:
            if found not in known:
                bad += 1
                line = line.replace(found, "")
        line = re.sub(r"\(\s*[,;\s]*\)", "", line).rstrip()
        if line.strip() and not line.lstrip().startswith("#") and not any(i in known for i in ids):
            line += NO_SOURCE
        lines.append(line)
    return "\n".join(lines).strip(), bad


def chunks(events: list[StoredEvent]) -> list[list[tuple[list[StoredEvent], str]]]:
    """One stretch's events as the writer reads them (`bite.rendered_groups`), cut
    into calls of at most about STRETCH_TOKENS each (one item at least)."""
    out: list[list[tuple[list[StoredEvent], str]]] = []
    used = 0
    for item in rendered_groups(events):
        if not out or (used + len(item[1]) > STRETCH_TOKENS * CHARS_PER_TOKEN and out[-1]):
            out.append([])
            used = 0
        out[-1].append(item)
        used += len(item[1])
    return out


async def _index_one(model: Any, items: list[tuple[list[StoredEvent], str]], timeout_s: float,
                     slots: asyncio.Semaphore) -> tuple[str | None, int, float]:
    """(the index, ids removed, $) of one call's items; None when the call failed."""
    from pydantic_ai import Agent, capture_run_messages
    from pydantic_ai.usage import UsageLimits

    from probe.daemon import usage as usage_mod

    usd = 0.0
    raw = "\n\n".join(text for _, text in items)
    async with slots:
        with capture_run_messages() as messages:
            try:
                result = await asyncio.wait_for(
                    Agent(model, instructions=INSTRUCTIONS).run(raw, usage_limits=UsageLimits(request_limit=1)),
                    timeout=timeout_s)
                text = (result.output or "").strip()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 -- a failed index shows the stretch raw, never stops the run
                log.warning("index call failed, the events go raw: %s: %s", type(exc).__name__, exc)
                text = ""
            for m in messages:
                if getattr(m, "usage", None) is not None and getattr(m, "model_name", None):
                    usd += float(usage_mod.response_cost(m) or 0.0)
    if not text:
        return None, 0, usd
    out, bad = checked(text, {ev.event_id for group, _ in items for ev in group})
    return (out or None), bad, usd


async def index_events(model: Any, events: list[StoredEvent], *, timeout_s: float = INDEX_TIMEOUT_S) -> Indexed:
    """The writer's view of `events`: the whole ones as `render` shows them, the
    others indexed (`chunks`, CONCURRENT_CALLS at a time); a call that fails
    shows its items raw."""
    # In order: a whole event, or one call's items.
    plan: list[StoredEvent | list[tuple[list[StoredEvent], str]]] = []
    for whole, evs in stretches(events):
        plan.extend(evs if whole else chunks(evs))
    slots = asyncio.Semaphore(CONCURRENT_CALLS)
    todo = [items for items in plan if isinstance(items, list)]
    answers = iter(await asyncio.gather(*(_index_one(model, items, timeout_s, slots) for items in todo)))
    out = Indexed(text="", calls=len(todo))
    blocks = []
    for items in plan:
        if not isinstance(items, list):
            blocks.append(render(items))
            continue
        text, bad, usd = next(answers)
        out.usd += usd
        out.bad_ids += bad
        if text is None:
            out.failed += 1
            blocks.extend(shown for _, shown in items)
        else:
            blocks.append(f"{toolset.pick(HEADER, HEADER_BASH)}\n{text}")
    out.text = "\n\n".join(blocks)
    return out
