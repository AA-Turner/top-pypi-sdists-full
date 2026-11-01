"""hold the write lease, say why no bite may start now, and begin stopping on a signal."""

from __future__ import annotations
import json
import time
from probe.daemon.host import lease
from probe.shared import mailbox
from probe.daemon.worker import alerts
from probe.shared.mailbox import requests as requests_mod
from probe.daemon.store.device import LANE_WRITE
#: At session end, the daemon finishes its queue for at most this long, counted
#: from the signal (or from noticing capture is gone).
FINISH_CAP_S = 35 * 60
#: The session's switch unreadable this long: the worker releases the lease and
#: exits EXIT_RESPAWN_LATER (the supervisor starts one again once it reads `daemon`).
SWITCH_UNREADABLE_EXIT_S = 60.0
#: Releases this worker made that a model round answering again takes back.
_RECOVERABLE = (lease.REASON_UNAUTHORIZED, lease.REASON_BUDGET, lease.REASON_GATEWAY)


class LeaseMixin:
    """Part of Worker: its methods run with `self` the Worker; compose() folds them into Worker."""

    # -- the lease ------------------------------------------------------------
    def _renew(self) -> bool:
        """Renew the write lease -- only while recording works (A1): never while a
        release this worker made stands (a refused key, the budget), never when
        the writer does not record the session (`lease.records`: the switch reads
        `daemon`), never over another process's live lease."""
        if self.released_reason is not None:
            return False
        sid = self.session.session_id
        if self.replay is None and (not lease.records(sid) or _foreign_lease(sid)):
            return False
        return lease.renew(sid)

    def _release(self, reason: str, *, offline: bool = False) -> None:
        lease.release(self.session.session_id, reason, offline=offline)
        self.released_reason = reason
        self.released_offline = offline

    def _quota_inline(self, exc: BaseException, expected_state: str) -> bool:
        """A confirmed monthly allowance refusal hands this session to the agent.

        Generic rate limits, outages, local token limits and strings mentioning
        a budget never change the user's mode. Replays do not touch live state.
        """
        from pydantic_ai.exceptions import ModelHTTPError

        if (self.replay is not None or not isinstance(exc, ModelHTTPError)
                or int(exc.status_code) != 429 or _refusal_code(exc) != "budget_exhausted"):
            return False
        from probe.sdk import session_marker

        if not session_marker.inline_on_budget(self.session.session_id, expected_state):
            return False
        self._release(lease.REASON_BUDGET)
        self.fail_requests(requests_mod.REASON_INLINE)
        if self.reader is not None:
            self.reader.take_asks()
            self.reader.fail_open_asks("the free daemon allowance is exhausted; Probe is inline")
        log.info("the free daemon allowance is exhausted: Probe is inline for this session")
        return True

    def _model_answered(self) -> None:
        """A model round answered (`agent.answered`): progress. A release made for
        the key, the budget, the gateway or answers the token limit ate ends here,
        and the lease is renewed -- except one made because
        PROBE refused the key: the model's route may take a key Probe's other
        routes refuse, so only `_probe_accepts_key` passing ends that one."""
        self.gateway_failures = 0
        self.no_answers = 0
        if self.released_reason in _RECOVERABLE and not self.probe_refused_key:
            log.info("the model answers again: taking the lease back (released: %s)", self.released_reason)
            self.released_reason = None
        self._renew()

    def _lease_ours(self) -> bool:
        """Do we still hold a live lease while the writer records the session
        (`lease.records`; the replay has none)?"""
        if self.replay is not None:
            return True
        return lease.may_write(self.session.session_id) is None

    def _bite_blocked(self) -> str | None:
        """Why no bite (no model call) may start now, or None. A release THIS worker
        made for a reason a model round answering takes back (the key, the budget,
        the gateway) does not block: that round is how the lease comes back.
        Anything else that keeps this process from writing does: the switch cannot
        be read, another process holds a live lease (a predecessor killed without
        releasing it, until it lapses), the lease could not be renewed."""
        if self.replay is not None:
            return None
        if self.catching_up():
            return "reading the history the session held before its first worker"
        sid = self.session.session_id
        if not lease.records(sid):
            return "the session's switch cannot be read"
        if _foreign_lease(sid):
            return lease.FOREIGN_HOLDER
        if self.released_reason in _RECOVERABLE:
            return None
        return lease.may_write(sid)

    def _switch_unreadable(self) -> int | None:
        """The switch cannot be read: no bite starts (`_bite_blocked`); after
        SWITCH_UNREADABLE_EXIT_S of it, release the lease and exit
        EXIT_RESPAWN_LATER -- the supervisor starts a worker again once the
        switch reads `daemon`, even if it already does by the time it looks."""
        now = self.clock()
        if self.switch_unreadable_since is None:
            self.switch_unreadable_since = now
            log.warning("the session's switch cannot be read: no model calls until it can")
            return None
        if now - self.switch_unreadable_since < SWITCH_UNREADABLE_EXIT_S:
            return None
        sid = self.session.session_id
        log.error("the session's switch has been unreadable for %.0fs: stopping", now - self.switch_unreadable_since)
        self._release(lease.REASON_ERROR)
        _device_error(f"session {sid}: its switch file could not be read for {SWITCH_UNREADABLE_EXIT_S:.0f}s; "
                      "the daemon stopped and the agent records")
        alerts.report(alerts.Kind.SWITCH_UNREADABLE, session_id=sid, lane=LANE_WRITE,
                      text=f"switch file unreadable for {SWITCH_UNREADABLE_EXIT_S:.0f}s")
        return EXIT_RESPAWN_LATER

    def _went_inline(self) -> bool:
        """Manual or confirmed-quota inline while a bite runs: stop at the next
        poll of its model call or between two rounds, not at the call's end."""
        return self.replay is None and lease.inline(self.session.session_id)

    def _parent_gone(self) -> bool:
        """Its supervisor (the service, or `tap watch`) exited: this worker is orphaned."""
        if self.supervisor_gone is not None:
            return self.supervisor_gone()
        return parent_gone(self.supervisor, self.parent_pid)

    # -- stopping -----------------------------------------------------------
    def begin_stopping(self) -> None:
        """SIGTERM or SIGINT (the signal handler calls this), or capture gone: the
        finish budget starts NOW, a run already going included, and what is on
        disk now is all this worker still takes on."""
        self.stopping = True
        if self.finish_by is None:
            self.finish_by = self.clock() + FINISH_CAP_S
            _mark(mailbox.finishing_path(self.session.session_id))
        if self._stop_ends is None:
            try:
                self._stop_ends = self._end_offsets()
            except Exception:  # noqa: BLE001 -- in a signal handler: the next poll takes the snapshot
                pass
        self.poke()  # an idle run's wait (the daemon host) ends now, not at its next look

    def _take_input(self) -> None:
        """A poll's reading: the next chunk of every stream -- or, stopping, what was
        on disk when stopping began, read to its end once, and nothing after it.
        (`stopping` set without `begin_stopping` starts the budget here.)"""
        if not self.stopping:
            self.read_new()
            return
        self.begin_stopping()
        if not self.drained:
            self.drained = True
            self.drain(self._stop_ends if self._stop_ends is not None else self._end_offsets())


def _hook_mode(session_id: str) -> str | None:
    try:
        raw = (_state_base() / "sessions" / f"{session_id}.mode").read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return raw or None


def _foreign_lease(session_id: str) -> bool:
    """Does ANOTHER process -- or, in the daemon host, another run -- hold a live
    lease on this session?"""
    try:
        data = json.loads(lease.lease_path(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return (isinstance(data, dict) and not lease.ours(data) and not data.get("reason")
            and float(data.get("expires_at") or 0) > time.time())
from probe.daemon.worker.error_log import _device_error  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.files import _mark, _state_base  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.failures import _refusal_code  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.loop.reading import log  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.worker.supervisor import EXIT_RESPAWN_LATER, parent_gone  # noqa: E402 -- pieces need each other; the front door loads this one first
