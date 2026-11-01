"""op=open: one stored event (or turn) in full, paged, side files from this session only."""

from __future__ import annotations
from pathlib import Path
from probe.shared.harness.events import PEER_TOOL, Kind
from probe.daemon.store.events import scrub


def session_open(deps: Deps, event_id: str | None = None, turn: int | None = None, outline: bool = False,
                 page: int = 0) -> str:
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    recorded = not deps.reader  # the writer never sees `read only (daemon)`
    if outline:
        return _outline(deps.store, recorded=recorded)
    if turn is not None:
        from probe.daemon.worker.bite.bite import rendered

        rows = deps.store.db.execute("SELECT seq FROM events WHERE turn = ? ORDER BY seq", (turn,)).fetchall()
        if not rows:
            return f"no turn {turn}"
        events = deps.store.events_between(rows[0]["seq"], rows[-1]["seq"], recorded=recorded)
        # As a bite shows them: a file change one line, a file burst a list. Its
        # content is one `op=open event_id=` away.
        text = "\n\n".join(shown for _, shown in rendered([ev for ev in events if ev.turn == turn]))
        return _page(text, page, f"turn {turn}")
    if not event_id:
        return "give an event_id or a turn (op=outline: one line per turn)"
    ev = deps.store.get(event_id, recorded=recorded)
    if ev is None:
        return f"no event {event_id}"
    text = ev.text
    if ev.side_file:
        side = _read_side(deps, ev.side_file)
        if side is not None:  # the full text: scrubbed as the preview was at intake
            text = _off_scrubbed(deps, side, Path(ev.cwd or deps.cwd))
    if ev.note:
        text = f"({ev.note})\n{text}"
    if ev.kind == Kind.TOOL_OUTPUT:
        call = deps.store.call_for(ev.call_id, recorded=recorded)
        head = f"output of: {call.command or ' '.join(filter(None, (call.tool, call.text)))}\n" if call else ""
        text = head + text
    elif ev.command and ev.tool != PEER_TOOL:  # a peer agent's message: its text, never its sender
        text = ev.command
    return _page(scrub(text), page, event_id)


def _read_side(deps: Deps, path: str) -> str | None:
    """A persisted output's full text: only from THIS session's side folder
    (`<session id>/tool-results/`; the adapter checked the path against the
    session's own folder when it read the line, and this checks again)."""
    try:
        resolved = Path(path).resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if resolved.parent.name != "tool-results" or resolved.parent.parent.name != deps.session_id:
        return None
    if not resolved.is_file() or resolved.stat().st_size > MAX_SIDE_FILE_BYTES:
        return None
    try:
        return resolved.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _page(text: str, page: int, label: str) -> str:
    pages = max(1, -(-len(text) // OPEN_PAGE_CHARS))
    page = max(0, min(page, pages - 1))
    chunk = text[page * OPEN_PAGE_CHARS:(page + 1) * OPEN_PAGE_CHARS]
    more = f"\n[page {page + 1} of {pages}; page={page + 1} for more]" if page + 1 < pages else ""
    return f"[{label} · page {page + 1} of {pages}]\n{chunk}{more}"
from probe.daemon.agent.tools.probe_cli.config import _off_scrubbed  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.refusals import write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.session_ops.outline import _outline  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, MAX_SIDE_FILE_BYTES, OPEN_PAGE_CHARS  # noqa: E402 -- pieces need each other; the front door loads this one first
