"""DeliveryNoticesMixin, Client's methods: poll and report what the drain delivered, dropped or was
refused, in plain lines."""

from __future__ import annotations
import threading
from typing import Any
from ...foundation.safe_warn import safe_warn as _diagnostics
from .journal.journal import Journal
from .transport.deadlines import without_patience

# Eager, not lazy (review of #2056): first importing a module during
# interpreter finalization made an uncaught Ctrl-C exit 1 instead of
# re-raising SIGINT (observed on 3.12; pre-importing fixes it).
# `_report_delivery` below used to do this import lazily, right there in the
# finalizer -- which is exactly the first-import-at-exit case that trips it.
# Importing it here, at ordinary module load time (well before any close can
# run), keeps the module already imported by the time exit teardown starts.
from probe import analytics as _telemetry

def _age_seconds(stamp: object) -> int | None:
    """Seconds since an ISO timestamp from status.json, or None."""
    if not stamp:
        return None
    try:
        from datetime import datetime, timezone

        then = datetime.fromisoformat(str(stamp))
        if then.tzinfo is None:
            then = then.replace(tzinfo=timezone.utc)
        return max(0, int((datetime.now(timezone.utc) - then).total_seconds()))
    except (TypeError, ValueError):
        return None


def _minutes_since(stamp: object) -> int | None:
    try:
        from datetime import datetime, timezone

        then = datetime.fromisoformat(str(stamp))
        if then.tzinfo is None:
            then = then.replace(tzinfo=timezone.utc)
        return max(0, int((datetime.now(timezone.utc) - then).total_seconds() // 60))
    except (TypeError, ValueError):
        return None


class DeliveryNoticesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _init_delivery_notices(self) -> None:
        """The baseline the delivery poller compares against (plan 1.7): what
        was already dead-lettered or auth-blocked before this client existed
        is not news."""
        from .journal.paths import _rank_suffix
        from ...foundation.safe_warn.safe_warn import DeliveryNotices

        try:
            suffix = _rank_suffix()
        except Exception:  # noqa: BLE001
            suffix = None
        self._notices = DeliveryNotices(prefix=f"probe[{suffix}]" if suffix else "probe")
        self._notice_polled_at = self._notices.clock()
        self._my_runs: set[str] = set()
        try:
            status = Journal.read_status(self.journal.dir) or {}
            recent = self.journal.recent_dead_letters()
        except Exception:  # noqa: BLE001
            status, recent = {}, []
        self._dead_seen = {str(entry.get("op_id")) for entry in recent}
        self._failed_seen = int(status.get("failed") or 0)
        self._auth_seen = self._auth_blocked_since(status)
        self._auth_block_started(self._auth_seen)
        self._pending_seen = int(status.get("pending") or 0)
        self._delivered_seen = self._own_delivered()
        # Plan 1.12: what this process's delivery report counts, and what its
        # last report already said (the report carries deltas).
        self._attempted_writes = 0
        self._dead_lettered_mine = 0
        self._dead_lettered_by_status: dict[str, int] = {}
        self._last_status: dict = {}
        self._reported: dict = {}
        self._reported_at = self._notice_polled_at

    def _auth_blocked_since(self, status: dict) -> str | None:
        """When delivery of this client's writes was last refused (401/403),
        or None: the queue-wide block, or THIS client's credential among the
        ones a drain set aside (`journal.auth_blocked_since`)."""
        from .journal.status_file import auth_blocked_since

        mine = set(self.__dict__.get("_credential_fingerprints") or ())
        mine |= set(self.__dict__.get("_ingest_fingerprints") or ())
        return auth_blocked_since(status, mine)

    def _auth_block_started(self, blocked: str | None) -> str | None:
        """When the current, unbroken block began, as far as this client has
        seen: the first `_auth_blocked_since` stamp of it. A drain rewrites
        that stamp at every refusal (the credential cooldown counts from the
        latest), so "stopped for N min" read from it always said 0-5 min."""
        if not blocked:
            self._auth_first = None
            return None
        first = self.__dict__.get("_auth_first")
        if first is None:
            self._auth_first = first = blocked
        return first

    def _own_delivered(self) -> int | None:
        """How many of this client's queued writes have landed so far (its
        producer record, one small file), or None without a producer."""
        producer_id = getattr(self.journal, "_producer_id", None)
        if not producer_id:
            return None
        try:
            record = self.journal._read_producer_locked(producer_id)
            return int(record.get("delivered") or 0)
        except Exception:  # noqa: BLE001
            return None

    def _note_drop(self, detail: str) -> None:
        """One dropped write, through the rate-limited notices (plan 1.7)."""
        notices = getattr(self, "_notices", None)
        if notices is None:  # a Client built without __init__ (a test double)
            _diagnostics.warn(f"probe: dropped a write before it reached the outbox: {detail}")
            return
        notices.note(notices.DROP, "{n} write(s) dropped before they reached the outbox",
                     detail=detail)

    def _poll_delivery(self, *, force: bool = False) -> None:
        """Say, in THIS process, when this process's writes are in trouble:
        dead letters of its own runs, an auth block, a queue stalled for 10
        minutes. At most one status.json read per `NOTICE_POLL_SECONDS`.
        Never raises. Not for a queue only `probe sync` drains (an offline run,
        plan 2.12): nothing delivers it by design, so "stalled" would be noise."""
        if getattr(self, "_drains_by_hand", False):
            return
        try:
            now = self._notices.clock()
            if not force and now - self._notice_polled_at < self.NOTICE_POLL_SECONDS:
                return
            self._notice_polled_at = now
            status = Journal.read_status(self.journal.dir) or {}
            notices = self._notices
            recent = self.journal.recent_dead_letters()
            fresh = [e for e in recent if str(e.get("op_id")) not in self._dead_seen]
            self._dead_seen = {str(e.get("op_id")) for e in recent}
            mine = [e for e in fresh if e.get("run_ref") in self._my_runs]
            self._dead_lettered_mine += len(mine)
            for entry in mine:
                code = str(entry.get("status") or "none")
                self._dead_lettered_by_status[code] = self._dead_lettered_by_status.get(code, 0) + 1
            self._last_status = status
            if mine:
                notices.note(
                    notices.DEAD_LETTER,
                    "{n} of this process's writes were permanently rejected by the "
                    "server (dead-lettered)",
                    count=len(mine),
                    detail=str(mine[-1].get("error") or "")[:200] or None,
                )
            # Dead letters no status entry accounts for were written by a worker
            # that predates 1.7 (it names no runs): the machine's, said so.
            failed = int(status.get("failed") or 0)
            unnamed = failed - self._failed_seen - len(fresh)
            if unnamed > 0:
                notices.note(
                    notices.DEAD_LETTER,
                    "{n} write(s) in this machine's outbox were dead-lettered",
                    count=unnamed,
                )
            self._failed_seen = failed
            blocked = self._auth_blocked_since(status)
            started = self._auth_block_started(blocked)
            if blocked and blocked != self._auth_seen:
                # The elapsed time is in the text: Python's default warning
                # filter shows an identical message from one place only once,
                # so a reminder that never changed never repeated (review of
                # #2055).
                minutes = _minutes_since(started)
                notices.note(
                    notices.AUTH_BLOCK,
                    "delivery has been stopped"
                    + (f" for {minutes} min" if minutes is not None else "")
                    + f": the server refused this machine's credential (401/403) since {started}",
                )
            oldest = status.get("oldest_pending")
            pending = int(status.get("pending") or 0)
            # Progress since the last look -- this client's writes landing, or
            # the queue shrinking -- means a drain is working through it, if
            # slowly (a long recovery pass after an outage), not stalled
            # (review of #2055).
            delivered = self._own_delivered()
            progressed = (
                delivered is not None
                and self._delivered_seen is not None
                and delivered > self._delivered_seen
            ) or pending < self._pending_seen
            self._delivered_seen, self._pending_seen = delivered, pending
            if pending and oldest and not progressed:
                from datetime import datetime, timezone

                waited = (
                    datetime.now(timezone.utc) - datetime.fromisoformat(str(oldest))
                ).total_seconds()
                if waited >= self.STALLED_AFTER_SECONDS:
                    notices.note(
                        notices.STALLED,
                        f"{pending} write(s) are queued and the oldest has waited "
                        f"{int(waited // 60)} min: the server is not taking them",
                    )
            if not force and now - self._reported_at >= self.DELIVERY_REPORT_SECONDS:
                self._report_delivery()
        except Exception:  # noqa: BLE001 -- a notice may never break a write
            pass

    def _report_delivery(self, *, final: bool = False) -> None:
        """Send this process's delivery counts since its last report to our
        telemetry (plan 1.12): counts only, never a key, body, name or path;
        nothing when the telemetry opt-out is set or the backend is not ours,
        and never for a queue only `probe sync` drains (an offline run, plan
        2.12, which must not touch the network). Skipped when there is
        nothing to say, except at a close.

        A periodic report goes out from a daemon thread (its first send
        imports the telemetry module and resolves an identity, which must not
        cost the training loop). A CLOSE's report is handed to the telemetry
        sender on the CALLING thread, after re-reading the outbox's status:
        the interpreter often shuts down milliseconds after `finish()`, too
        soon for a thread to start or register the sender's exit flush, and
        the 15 s poll's numbers can be stale (review of #2056). During
        interpreter exit (the auto-close at exit) it is flushed right away,
        since the sender's own exit flush may already have run."""
        if getattr(self, "_drains_by_hand", False):
            return
        try:
            if final:
                self._poll_delivery(force=True)
            now = self._notices.clock()
            status = self._last_status or {}
            counts = {
                "attempted": self._attempted_writes,
                "dropped": int(self.dropped_writes or 0),
                "direct_sends": int(self.direct_sends or 0),
                "dead_lettered": self._dead_lettered_mine,
                "discarded": int(getattr(self, "_discarded_requests", 0) or 0),
            }
            delta = {k: v - int(self._reported.get(k, 0)) for k, v in counts.items()}
            by_status = {
                code: n - int((self._reported.get("dead_lettered_by_status") or {}).get(code, 0))
                for code, n in self._dead_lettered_by_status.items()
            }
            by_status = {code: n for code, n in by_status.items() if n > 0}
            if not final and not any(delta.values()):
                return
            props: dict[str, Any] = {
                **delta,
                "dead_lettered_by_status": by_status or None,
                "pending": int(status.get("pending") or 0),
                "oldest_pending_s": _age_seconds(status.get("oldest_pending")),
                "auth_blocked_s": _age_seconds(
                    self._auth_block_started(self._auth_blocked_since(status))
                ),
                "final": final,
                "interval_s": round(now - self._reported_at, 1),
            }
            self._reported = {
                **counts, "dead_lettered_by_status": dict(self._dead_lettered_by_status)
            }
            self._reported_at = now
            base_url = self.settings.base_url

            def send(flush: bool = False) -> None:
                try:
                    _telemetry.emit_delivery_summary(base_url=base_url, flush=flush, **props)
                except Exception:  # noqa: BLE001 -- observability is a bystander
                    pass

            if final:
                send(flush=not threading.main_thread().is_alive())
            else:
                threading.Thread(target=send, name="probe-delivery-report", daemon=True).start()
        except Exception:  # noqa: BLE001
            pass

    def _after_enqueue(self) -> None:
        """Wake delivery for a just-journaled op (F1/F2). A DEAD exporter is
        not respawned: the only thing that kills one is an auth block, and
        respawning per write would retry rejected credentials forever -- the
        zombie-uploader pitfall. Re-login + `probe outbox retry` resumes."""
        self._poll_delivery()
        if self._drain_interval is not None:
            exporter = self._exporter
            if exporter is None:
                with self._exporter_lock:
                    exporter = self._exporter
                    if exporter is None:
                        from .outbox.drainers.in_process import OutboxExporter

                        # Its thread outlives any patience scope a write here
                        # happens inside (init); see `_wrap_run`.
                        with without_patience():
                            exporter = OutboxExporter(self, self._drain_interval)
                            self._learn_identity()
                        self._exporter = exporter
            exporter.wake()
            return
        self._kick_drainer()
