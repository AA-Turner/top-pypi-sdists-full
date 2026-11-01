"""read-only and inline stretches: what the writer leaves unrecorded and is told about once."""

from __future__ import annotations
from probe.daemon.session import session as folders
from probe.daemon.host import lease
from probe.shared.mailbox import requests as requests_mod


#: Store facts: where `read only (daemon)` began (first event seq, turn), while it lasts.
READ_ONLY_FROM = "read_only_from"
READ_ONLY_TURN = "read_only_turn"
#: `{since: [first, last]}`: per inline stretch (`/probe inline`), the turns the
#: writer left to the agent, until it is told once that the stretch ended.
INLINE_SKIPPED = "inline_skipped"
#: The stretches (`since` keys) the writer was already told about: a late event
#: from one of them is still left to the agent, without a second notice.
INLINE_ANNOUNCED = "inline_announced"
#: That telling (Richard's approved text, 2026-10-06).
INLINE_NOTICE = "the daemon skipped {turns}: Probe was inline, the agent's to record."
#: Why a bite running when `/probe inline` landed stopped (its events stay queued).
INLINE_STOP = "the researcher set Probe inline"


class StretchesMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    async def _read_only_tick(self) -> int | None:
        """One poll in `read only (daemon)` (Richard 2026-09-29): the reader keeps
        reading what arrives; the writer records none of it, now or once the switch
        is back on. Without a reader (reads are off for this agent) the worker
        still reads and marks, so a later worker never records the interval."""
        sid = self.session.session_id
        if self.read_only_from is None:
            log.info("read only (daemon): the writer stops, the reader keeps reading")
            self.read_only_from = self.store.next_seq()
            self.read_only_turn = self.store.current_turn()
            with self.store.tx():
                self.store.set_fact(READ_ONLY_FROM, self.read_only_from)
                self.store.set_fact(READ_ONLY_TURN, self.read_only_turn)
        if lease.held(sid):
            self._release(lease.REASON_STOPPED)
        self.read_new()
        # The writer records nothing here: a request filed now, or still waiting, fails.
        self.fail_requests(requests_mod.REASON_READ_ONLY)
        with self.store.tx():
            self.store.leave_unrecorded(self.read_only_from)
        if self.stopping or self._parent_gone():
            return 0  # ending: nothing to finish, what arrived is marked
        # The folder snapshot moves on silently, so a file written now is never
        # announced to the writer once the switch is back on.
        await self._check_folders(folders.working_folders(self.store, self.session.cwd, self.session.home),
                                  emit=False)
        return None

    async def _end_read_only(self) -> None:
        """Back to `on (daemon)`: what the read-only interval left unread is marked
        by its stamps (the switch's last write is when it ended), the folder
        snapshot catches up silently, the writer is told once which turns went
        unrecorded, and the lease this worker released for read only comes back."""
        ended = lease.state_changed_at(self.session.session_id)
        if ended is not None:
            self.read_new()
            with self.store.tx():
                self.store.leave_unrecorded_before(self.read_only_from, ended)
        await self._check_folders(folders.working_folders(self.store, self.session.cwd, self.session.home),
                                  emit=False, force=True)
        first, last = self.read_only_turn, self.store.current_turn()
        log.info("on (daemon) again: turns %s-%s stay unrecorded", first, last)
        self._notice(f"the researcher set Probe to read only from turn {first} to turn {last}: "
                     "nothing from those turns is recorded")
        self.read_only_from = None
        with self.store.tx():
            self.store.set_fact(READ_ONLY_FROM, None)
            self.store.set_fact(READ_ONLY_TURN, None)
        if self.released_reason == lease.REASON_STOPPED:
            self.released_reason = None

    def _mark_inline(self) -> None:
        """`/probe inline` (Richard 2026-10-06): the events stamped inside a stretch
        the researcher handed Probe to the agent are the agent's, so no bite ever
        covers them. Runs wherever events enter the store (`read_new`: the poll,
        the reader's tick, between model rounds, a folder check), so the writer
        never sees one unmarked. By the events' own stamps against the times the
        switch wrote: no worker runs while inline, so the next one marks the
        stretch from its stamps. Only events newer than the last pass are
        checked until the set of intervals changes."""
        if self.replay is None:
            from probe.sdk import session_marker

            intervals = tuple(session_marker.inline_intervals(self.session.session_id))
        else:
            intervals = ()
        if not intervals:
            self._inline_seen = intervals
            return
        after = self._inline_seq if intervals == self._inline_seen else 0
        self._inline_seen = intervals
        self._inline_seq = self.store.next_seq() - 1
        marked = self.store.leave_unrecorded_in(list(intervals), after_seq=after)
        if not marked:
            return
        with self.store.tx():
            spans = _spans(self.store.fact(INLINE_SKIPPED))
            announced = set(self.store.fact(INLINE_ANNOUNCED) or [])
            for since, turn in marked:
                key = repr(since)
                if key in announced:
                    continue
                first, last = spans.get(key, (turn, turn))
                spans[key] = [min(first, turn), max(last, turn)]
            self.store.set_fact(INLINE_SKIPPED, spans or None)

    def _inline_unannounced(self) -> bool:
        """An inline stretch has ended that the writer was not told about yet."""
        from probe.sdk import session_marker

        announced = set(self.store.fact(INLINE_ANNOUNCED) or [])
        return any(until is not None and repr(since) not in announced
                   for since, until in session_marker.inline_intervals(self.session.session_id))

    def _announce_inline(self) -> None:
        """Each tick on the recording path: the writer is told once per ended
        inline stretch which turns it left to the agent -- the notice and its
        bookkeeping in one transaction, so a restart cannot tell it twice."""
        if self.replay is not None:
            return
        sid = self.session.session_id
        spans = _spans(self.store.fact(INLINE_SKIPPED))
        if not spans:
            return
        from probe.sdk import session_marker

        open_since = {repr(since) for since, until in session_marker.inline_intervals(sid) if until is None}
        ended = {key: span for key, span in spans.items() if key not in open_since}
        if not ended:
            return
        notices = []
        for first, last in sorted(ended.values()):
            turns_text = f"turn {first}" if first == last else f"turns {first}-{last}"
            notices.append(_notice_event(self.store, INLINE_NOTICE.format(turns=turns_text)))
        with self.store.tx():
            self.store.add(notices)
            self.store.set_fact(INLINE_SKIPPED, {k: v for k, v in spans.items() if k in open_since} or None)
            announced = list(self.store.fact(INLINE_ANNOUNCED) or [])
            self.store.set_fact(INLINE_ANNOUNCED, announced + [k for k in ended if k not in announced])


def _spans(value: object) -> dict:
    """The INLINE_SKIPPED fact as `{since: [first, last]}`; any other shape (a
    store written by an earlier build) reads as none."""
    if not isinstance(value, dict):
        return {}
    return {k: v for k, v in value.items() if isinstance(v, list) and len(v) == 2}
from probe.daemon.worker.loop.held import _notice_event  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
