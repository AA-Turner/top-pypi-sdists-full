"""read each followed session's transcript tail and turn its lines into triggers and window looks."""

from __future__ import annotations

import contextlib
import json
import os
import stat
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ..watch.alertpoll import Endpoint
from probe.service.hints.delivery import DeliveryState
from probe.service.hints.state import Followed, Lookup, _Facts, _State
from probe.service.hints.trigger import MAIN_STREAM, Trigger, trigger_of
from probe.service.hints.triggers.window import SCAN_MARGIN_CHARS, WINDOW_SEGMENT_CHARS, shows_mid_turn, window_due
#: A served session's hint marker (`mailbox.hints_live_path`) is touched at most
#: this often; its daemon reads one older than `model.HINTS_LIVE_TTL_S` (120 s)
#: as no hint lane here, and its reader wakes at prompts again.
HINTS_LIVE_BEAT_S = 30.0
#: This many window lookups in a row failing (no answer, any refusal,
#: `engine_error` or `rate_limited`), the session's or its key's, stop the
#: session's window marker until one works again.
WINDOW_FAILURES_STOP = 2
#: The session's transcript must have been read this recently for its window marker.
WINDOW_READ_FRESH_S = 60.0
#: A window clock older than this (the reader's check-in interval) means the
#: lane has not looked at the turn's work for that long (tool calls only, or a
#: window that could not go): its window marker stops and the check-in returns.
WINDOW_COVERS_S = 1800.0
#: Sessions with a lookup waiting, at most: the oldest goes past it.
MAX_PENDING = 64
#: One read of a transcript, at most; a line longer than this is skipped.
MAX_READ_BYTES = 2 * 1024 * 1024
#: A session first seen is read from this far before its end...
INITIAL_BACK_BYTES = 64 * 1024
#: ...and there only lines this young (by their own stamp) trigger: a first
#: prompt written just before the lane looked, never the history of a resumed one.
FRESH_S = 30.0
#: A Codex session names a folder: its rollout is looked for this often until found.
RESOLVE_EVERY_S = 15.0
#: An undeliverable session is still asked about at a researcher's prompt, at
#: most this often: the probe whose hint, once shown, ends it.
UNDELIVERABLE_PROBE_S = 1800.0


def _safe(sid: str) -> str:
    """`probe.shared.mailbox.layout._safe`: a session id as a file stem."""
    return "".join(c for c in sid if c.isalnum() or c in "-_") or "session"


def _epoch(stamp: object) -> float | None:
    if not isinstance(stamp, str) or not stamp:
        return None
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


@dataclass
class _Tail:
    adapter: object
    filter: object
    path: Path | None = None
    inode: int | None = None
    offset: int | None = None
    skipping: bool = False
    first: bool = True
    seen_at: float = 0.0
    resolve_at: float = 0.0
    #: When the transcript was last read without an error (`clock`).
    read_ok_at: float = float("-inf")
    #: The file's size when all that was left past `offset` was an unfinished
    #: line: not read again until it grows.
    partial_at: int | None = None


class TailMixin:
    """Part of HintLane: its methods run with `self` the HintLane; compose() folds them into HintLane."""

    # -- the tail ---------------------------------------------------------------

    def _tail_loop(self) -> None:
        while not self._closed:
            # Cleared before the look: a `changed` during it makes the next one at once.
            self._wake.clear()
            try:
                active = self.read_once()
            except Exception as exc:  # noqa: BLE001 -- the thread outlives a bug
                self._log(f"hints: a read failed: {exc!r}")
                active = True
            self._wake.wait(self.poll_s if active else None)

    def read_once(self) -> bool:
        """One look at every followed session's transcript. False when none is
        followed (the tail then waits for `changed` with no timer)."""
        try:
            sessions = list(self._sessions())
        except Exception as exc:  # noqa: BLE001
            self._log(f"hints: the sessions could not be listed: {exc!r}")
            sessions = []
        seen = set()
        for session in sessions:
            seen.add(session.sid)
            try:
                self._read(session)
            except Exception as exc:  # noqa: BLE001 -- one transcript never stops another
                self._log(f"hints: session {session.sid}: a read failed: {exc!r}")
            try:
                self._beat(session)
            except Exception as exc:  # noqa: BLE001 -- a stale marker only wakes the reader
                self._log(f"hints: session {session.sid}: the hint marker failed: {exc!r}")
        # No longer read here (it ended, or its recorder let go of it). The
        # states too: a lookup in flight when its session went makes one anew.
        for sid in [s for s in {*self._tails, *self._states, *self._beats} if s not in seen]:
            self._beats.pop(sid, None)
            self._tails.pop(sid, None)
            with self._cv:
                self._pending.pop(sid, None)
                self._states.pop(sid, None)
        return bool(sessions)

    def _beat(self, session: Followed) -> None:
        """While this lane can hint `session` (followed here, a key its own config
        resolves, the server neither refusing the key nor lacking the route nor
        answering `mode: off`), its marker is touched, at most every
        HINTS_LIVE_BEAT_S: the session's daemon then leaves prompt time to hints
        (`model.hints_live`). Not touched, the marker goes stale and the reader
        wakes at prompts again. Its `.window` marker is touched in the same beat
        only while window hints are proven working for it (`_window_works`): its
        reader then stops its check-ins (`model.window_hints_live`). Neither is
        touched unless the hints posted here reach the agent (`delivery_receipt`
        OK: a deliverer's heartbeat, or a hint shown lately)."""
        now = self.clock()
        if now - self._beats.get(session.sid, float("-inf")) < HINTS_LIVE_BEAT_S:
            return
        self._beats[session.sid] = now  # looked at, touched or not: the next look in a beat
        ep = self.endpoint_of(session.env)
        if ep is None:
            return
        key, server, _pair = _scopes(ep)
        with self._cv:
            if (max(self._holds.get(key, float("-inf")), self._holds.get(server, float("-inf"))) > now
                    or self._off.get((ep.base_url, ep.key), float("-inf")) > now):
                return  # a 429 (`pair`) passes: a busy server still hints
        receipt = self._receipt(session, self._state(session.sid))
        if receipt is None or receipt["state"] != DeliveryState.OK:
            # Lookups work, but nothing says a hint reaches this agent: its
            # reader keeps its prompt turns and check-ins (plan hints-relevance R12).
            return
        from probe.shared import mailbox

        with mailbox.rooted(session.state):
            path = mailbox.hints_live_path(session.sid)
            window = mailbox.hints_window_path(session.sid)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()  # an existing one's mtime moves to now
        if self._window_works(session, ep, now):
            window.touch()

    def _window_works(self, session: Followed, ep: Endpoint, now: float) -> bool:
        """Window hints proven working for `session` (plan hints-window-trigger
        W3): its transcript read without an error within WINDOW_READ_FRESH_S;
        its server and key answered a window lookup as one, with no 404 (or 422
        naming `trigger`) to one since; and fewer than WINDOW_FAILURES_STOP of its window lookups
        in a row failed, its own or its key's; its harness shows a hint mid-turn
        (`shows_mid_turn`); and its window clock started within WINDOW_COVERS_S
        (a turn of tool calls only, or a window that could not go, is looked at
        by no one). Until then its reader keeps its check-ins."""
        tail = self._tails.get(session.sid)
        if tail is None or now - tail.read_ok_at > WINDOW_READ_FRESH_S or not shows_mid_turn(tail.adapter):
            return False
        pair = (ep.base_url, ep.key)
        with self._cv:
            state = self._states.get(session.sid)
            failures = state.window_failures if state is not None else 0
            since = state.window_since if state is not None else None
            return (self._window_ok.get(pair, False) and failures < WINDOW_FAILURES_STOP
                    and self._window_key_failures.get(pair, 0) < WINDOW_FAILURES_STOP
                    and (since is None or self.wall() - since <= WINDOW_COVERS_S))

    def _tail(self, session: Followed) -> _Tail | None:
        tail = self._tails.get(session.sid)
        if tail is not None:
            return tail
        from probe.shared.harness import lookup as adapters
        from probe.shared.harness.session_filter import Filter

        try:
            adapter = adapters.for_source(session.harness)
        except LookupError:
            return None
        tail = _Tail(adapter=adapter, filter=Filter(_Facts(), session.sid, session.cwd or None),
                     seen_at=self.wall())
        self._tails[session.sid] = tail
        return tail

    def _path(self, session: Followed, tail: _Tail) -> Path | None:
        if tail.path is not None:
            return tail.path
        if session.transcript:
            tail.path = Path(session.transcript)
        elif session.transcript_dir and self.clock() >= tail.resolve_at:
            # Codex: its rollout under a dated folder (`tap.main._resolve_codex_transcript`).
            tail.resolve_at = self.clock() + RESOLVE_EVERY_S
            folder = Path(session.transcript_dir)
            found = sorted(folder.rglob(f"*{session.sid}.jsonl")) if folder.is_dir() else []
            tail.path = found[0] if found else None
        if tail.path is not None:
            with contextlib.suppress(Exception):
                tail.adapter.session_files(tail.path)
        return tail.path

    def _read(self, session: Followed) -> None:
        tail = self._tail(session)
        if tail is None:
            return
        path = self._path(session, tail)
        if path is None:
            return
        try:
            # Never a blocking open (a FIFO, a device): one path a caller named
            # must not stop every session's tail (`mailwatch.read_regular`).
            fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOCTTY", 0))
        except OSError:
            return
        handle = os.fdopen(fd, "rb")
        with handle:
            info = os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode):
                return
            tail.read_ok_at = self.clock()
            if tail.offset is None:
                tail.inode = info.st_ino
                tail.offset = max(0, info.st_size - INITIAL_BACK_BYTES)
                tail.skipping = tail.offset > 0  # mid-line: on from the next line
            elif info.st_ino != tail.inode or info.st_size < tail.offset:
                # Rewritten or replaced under the offset: on from its end.
                tail.inode, tail.offset, tail.skipping = info.st_ino, info.st_size, False
                tail.partial_at = None
                return
            if info.st_size <= tail.offset:
                tail.first = False
                return
            if tail.partial_at == info.st_size:
                return  # only an unfinished line past the offset, and no new byte
            size = info.st_size
            handle.seek(tail.offset)
            buf = handle.read(min(MAX_READ_BYTES, info.st_size - tail.offset))
        start = tail.offset
        if tail.skipping:
            nl = buf.find(b"\n")
            if nl < 0:
                tail.offset += len(buf)
                return
            tail.skipping = False
            start += nl + 1
            buf = buf[nl + 1:]
        last = buf.rfind(b"\n")
        if last < 0:
            if len(buf) >= MAX_READ_BYTES:
                tail.offset, tail.skipping = start + len(buf), True  # a line over MAX_READ_BYTES: skipped
            else:
                tail.offset, tail.partial_at = start, size
            return
        tail.partial_at = None
        tail.offset = start + last + 1
        fresh_after = tail.seen_at - FRESH_S if tail.first else None
        tail.first = False
        pos = 0
        while pos <= last:
            nl = buf.find(b"\n", pos)
            line, end = buf[pos:nl], start + nl + 1
            pos = nl + 1
            self._line(session, tail, line, end, fresh_after)

    def _line(self, session: Followed, tail: _Tail, line: bytes, end: int, fresh_after: float | None) -> None:
        if not line.strip():
            return
        try:
            obj = json.loads(line)
        except (ValueError, RecursionError):
            return  # a line nested too deep for the parser too: the next one is read
        if not isinstance(obj, dict):
            return
        stamp = _epoch(tail.adapter.line_ts(obj))
        if fresh_after is not None and (stamp is None or stamp < fresh_after):
            return  # the history of a session first seen
        try:
            events = list(tail.adapter.parse_line(obj, stream=MAIN_STREAM, offset=end))
        except Exception:  # noqa: BLE001 -- a line the adapter cannot read is skipped, as the worker does
            return
        for index, event in enumerate(events):
            event.index = index
        # A first look's prompts and turn ends are no newer than a hint the last
        # service posted for them: they withdraw nothing.
        newer = fresh_after is None
        from probe.shared.harness.events import Kind

        when = stamp if stamp is not None else self.wall()
        marks = [e.kind for e in events
                 if e.stream == MAIN_STREAM and e.kind in (Kind.TOOL_CALL, Kind.PROMPT, Kind.TURN_END)]
        if marks:
            # A waiting hint's chances to be shown (`delivery_receipt`): tool
            # calls, and the prompts that start a turn. One typed into a
            # running turn (pi's steer or follow-up, a queued message) starts
            # none: its deliverer's one hint slot for the turn stays taken.
            seen = self._state(session.sid)
            with seen.lock:
                for kind in marks:
                    if kind == Kind.TOOL_CALL:
                        seen.tool_calls.append(when)
                    elif kind == Kind.TURN_END:
                        seen.turn_open = False
                    elif not seen.turn_open:
                        seen.prompts.append(when)
                        seen.turn_open = True
        ended = any(e.stream == MAIN_STREAM and e.kind == Kind.TURN_END for e in events)
        found = [(event, hit) for event in events if (hit := trigger_of(event)) is not None]
        # The agent's steps (W1): its messages and tool calls; never a tool's
        # output, nor its reasoning. None where a window hint could not be shown.
        steps = [e for e in events if e.stream == MAIN_STREAM and e.kind in (Kind.AGENT_TEXT, Kind.TOOL_CALL)]
        if not shows_mid_turn(tail.adapter):
            steps = []
        kept: set = set()
        if found or steps:
            # `.probe.config`: the worker's own filter, over the events that would
            # ask and the messages a window would send. A tool call that is only
            # counted gets the folder's verdict alone: the filter's per-call reads
            # walk trees, and nothing of it leaves.
            line_cwd = obj.get("cwd") if isinstance(obj.get("cwd"), str) else None
            asking = {id(e) for e, _ in found} | {id(e) for e in steps if e.kind == Kind.AGENT_TEXT}
            kept = {id(e) for e in tail.filter.keep([e for e in events if id(e) in asking], stream=MAIN_STREAM,
                                                    line_cwd=line_cwd)}
            kept |= {id(e) for e in steps if id(e) not in asking
                     and not tail.filter.folder_excluded(e, line_cwd=line_cwd)}
        # Before the turn end: a line can end the turn with its last message (pi),
        # and the turn's end ends its window too.
        self._window_steps(session, [e for e in steps if id(e) in kept], when)
        if ended:
            self.turn_ended(session, newer=newer)
        for event, (trigger, text, senders) in found:
            if id(event) not in kept:
                self.stats["excluded"] += 1
                # Never asked about, but still a newer prompt: a waiting hint is stale.
                text = ""
            self.trigger(session, trigger, text, senders, happened=stamp, newer=newer)

    def _window_steps(self, session: Followed, steps: list, stamp: float) -> None:
        """The agent's steps of one line, for the window (W1): its messages kept
        (the newest WINDOW_MAX_SEGMENTS), and a window look queued at the first
        step it is due (`window_due`). Its messages are taken when it goes
        (`take_due`), so one replaced while it waits loses nothing."""
        if not steps:
            return
        from probe.shared.harness.events import Kind

        state = self._state(session.sid)
        with self._cv:
            if state.window_since is None:
                state.window_since = stamp  # the clock starts at the session's first step seen here
            state.window_seen = stamp
            for event in steps:
                text = (event.text or "").strip() if event.kind == Kind.AGENT_TEXT else ""
                if text:
                    state.window_messages.append(text[:WINDOW_SEGMENT_CHARS + SCAN_MARGIN_CHARS])
            if not window_due(stamp, state.window_since, state.window_messages):
                return
            if session.sid in self._pending:
                return  # a lookup waits (a window, or another trigger's): again at a later step
        self._queue_window(session, state, stamp)

    def _may_ask(self, state: _State, trigger: str) -> bool:
        """An UNDELIVERABLE session is asked about only at a researcher's
        prompt, at most every UNDELIVERABLE_PROBE_S: the probe whose hint, once
        shown, ends it. Every other session, always."""
        with state.lock:
            if (state.delivery or {}).get("state") != DeliveryState.UNDELIVERABLE:
                return True
            now = self.clock()
            if trigger == Trigger.PROMPT and now - state.probe_at >= UNDELIVERABLE_PROBE_S:
                state.probe_at = now
                return True
        self.stats["undeliverable_skipped"] += 1
        return False

    def _queue_window(self, session: Followed, state: _State, stamp: float) -> None:
        """A window look, queued. With no key, the team's hints off, or a
        session its hints do not reach, none is, and the clock starts again:
        the next is WINDOW_GAP_S on."""
        if not self._may_ask(state, Trigger.WINDOW):
            with self._cv:
                state.window_since = stamp
                state.window_messages.clear()
            return
        try:
            ep = self.endpoint_of(session.env)
        except Exception:  # noqa: BLE001 -- unknown: not asked
            ep = None
        now = self.clock()
        with self._cv:
            if ep is None or now < self._off.get((ep.base_url, ep.key), float("-inf")):
                self.stats["no_key" if ep is None else "quiet"] += 1
                state.window_since = stamp
                state.window_messages.clear()
                return
            if session.sid in self._pending:
                return
            self._pending[session.sid] = Lookup(
                sid=session.sid, session=session, trigger=Trigger.WINDOW, text="", senders=[], queued=now,
                happened=stamp, epoch=state.epoch, ep=ep)
            self._evict()
            self.stats[f"trigger_{Trigger.WINDOW}"] += 1
            # notify_all: two lookup threads wait on this condition, each for its
            # own kind, and the one woken must be the one with work.
            self._cv.notify_all()

    def _evict(self) -> None:
        """Past MAX_PENDING, the oldest waiting window goes first (the least
        asked-for), else the oldest lookup. Under the lane's condition."""
        while len(self._pending) > MAX_PENDING:
            window = next((sid for sid, job in self._pending.items() if job.trigger == Trigger.WINDOW), None)
            if window is None:
                self._pending.popitem(last=False)
            else:
                del self._pending[window]
            self.stats["dropped"] += 1


def _scopes(ep: Endpoint | None) -> tuple:
    """What a hold is kept for (as `alertpoll`): the key, wherever it is used (a
    401 / 403); the server, for every key (a 404); that key on that server (a 429)."""
    if ep is None:
        return ()
    return (("key", ep.key), ("server", ep.base_url), ("pair", ep.base_url, ep.key))
