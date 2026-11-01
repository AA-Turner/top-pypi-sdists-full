"""op=search and op=logbook: full-text search over the session's events or the writer's logbook."""

from __future__ import annotations
from probe.shared.harness.events import PEER_TOOL


def session_search(deps: Deps, query: str, kind: str | None = None, turn_from: int | None = None,
                   turn_to: int | None = None, logbook: bool = False) -> str:
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    if logbook:
        rows = deps.store.search_logbook(query, limit=SEARCH_LIMIT, writes_only=deps.reader)
        if not rows:
            whose = "the writer's" if deps.reader else "your"
            return f"nothing in {whose} logbook matches {query!r}"
        return "\n".join(f"- {r['what']} #{r['id']}: {r['body'][:300]} {r['status'] or ''} {(r['reason'] or '')[:200]}"
                         for r in rows)
    kinds = [kind] if kind else None
    # The writer never sees what arrived in `read only (daemon)`; the reader does.
    hits = deps.store.search(query, kinds=kinds, turn_from=turn_from, turn_to=turn_to, limit=SEARCH_LIMIT,
                             recorded=not deps.reader)
    if _logs_lookups(deps):  # the logbook is the writer's
        deps.store.log_lookup(bite=deps.bite_id, tool="session.search", query=query, result=f"{len(hits)} hits")
    if not hits:
        return f"no event matches {query!r}" + (f" (kind {kind})" if kind else "")
    out = []
    for ev in hits:
        # A peer agent's message keeps its sender in `command`: its text is the message.
        text = ev.text if ev.tool == PEER_TOOL else (ev.command or ev.text)
        at = text.lower().find(query.split()[0].lower()) if query.split() else 0
        start = max(0, at - 200)
        snippet = text[start:start + 500].replace("\n", " ⏎ ")
        tag = f" ({ev.note})" if ev.note else ""
        out.append(f"- {ev.event_id} · turn {ev.turn} · {ev.kind.value}{' · ' + ev.tool if ev.tool else ''}: "
                   f"{snippet}{tag}")
    return "\n".join(out)
from probe.daemon.agent.tools.refusals import write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, SEARCH_LIMIT, _logs_lookups  # noqa: E402 -- pieces need each other; the front door loads this one first
