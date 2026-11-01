"""StatusMixin, Run's methods: run.set_status and the status a sys.exit code or exception means."""

from __future__ import annotations
from typing import Any


#: Statuses after which a run can never beat again. Mirrors the server's CHECK
#: constraint minus 'created'/'running' (db/experiment/schema.sql in research-os).
_TERMINAL_STATUSES = frozenset({"completed", "failed", "crashed", "canceled", "untracked"})


def _status_for_system_exit(code: object, in_flight: BaseException | None) -> tuple[str, int]:
    """(run status, process exit status) for ``sys.exit(code)`` / ``SystemExit(code)``.

    The exit status is what the OS will report: None and False are 0, an int
    is taken modulo 256 (``sys.exit(-1)`` exits 255, ``sys.exit(256)`` exits
    0), anything else -- a message -- prints and exits 1. Never negative, so a
    stored code can never read as "killed by a signal". Ctrl-C in flight
    (Lightning's ``except KeyboardInterrupt: sys.exit(1)``) is ``canceled``."""
    exit_code = (int(code) & 0xFF) if isinstance(code, int) else (0 if code is None else 1)
    if isinstance(in_flight, KeyboardInterrupt):
        return "canceled", exit_code
    return ("completed" if exit_code == 0 else "failed"), exit_code


#: A child's exit reported as a RUN status.
#:
#: SIGINT IS A DECISION, NOT A DEFECT. `fluent.py` already says so for the
#: in-process path -- it maps KeyboardInterrupt to 'canceled' -- but `execute`
#: mapped purely on "is the code zero", so Ctrl-C under `probe exec` closed the
#: run 'failed' and mailed the researcher a crash notice about a run they had
#: just stopped themselves. That lands in the client-reported bucket, which is
#: otherwise the trustworthy 85% of crash alerts.
#:
#: BOTH SPELLINGS. `subprocess.run` reports a signalled child as -N; a shell in
#: between reports 128+N. Ctrl-C therefore arrives as -2 or 130 depending on
#: what was wrapped.
#:
#: SIGTERM IS DELIBERATELY NOT HERE. A scheduler preempting a job, an eviction,
#: a `kill` from another session -- those are exactly the deaths a researcher
#: does NOT already know about, and they are the case the crash email exists
#: for. Only the interrupt the person typed is a decision.
def _status_for_exit(returncode: int) -> str:
    import signal as _signal

    if returncode == 0:
        return "completed"
    if returncode in (-_signal.SIGINT, 128 + int(_signal.SIGINT)):
        return "canceled"
    return "failed"


class StatusMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- lifecycle ----------------------------------------------------------
    def set_status(
        self,
        status: str,
        *,
        ended_at: str | None = None,
        summary_metrics: dict | None = None,
        summary: dict | None = None,
        sync: bool = False,
        strict: bool | None = None,
        only_if_running: bool = False,
    ):
        summary = _one_summary(summary_metrics, summary)
        if status in _TERMINAL_STATUSES and self._lease is not None:
            if self._lease_protocol is None and sync:
                # No beat of this lease has answered yet: one bounded beat
                # learns which rules the run follows (and registers the lease).
                self._draining_beat(draining=False)
            if self._leased():
                # 2.8: a writer on a lease RELEASES it with its verdict and the
                # server closes the run once its leases say the work ended --
                # the worst of every writer's verdict, never whichever landed
                # last.
                return self._release_lease(
                    status, ended_at=ended_at, summary=summary, sync=sync, strict=strict
                )
            # A lease on a run that is NOT on leases (NULL: opened before 0271 or
            # by an older client; flipped; the kill switch off; or not known):
            # close it exactly as before 2.8, then release the lease so it reads
            # released rather than expired (review of #2060, HIGH-1).
            lease, self._lease = self._lease, None
            try:
                data = self.set_status(
                    status,
                    ended_at=ended_at,
                    summary=summary,
                    sync=sync,
                    strict=strict,
                    only_if_running=only_if_running,
                )
            finally:
                self._lease = lease
            # Only after a close that did not raise: a strict close that failed
            # must not be completed later by a queued release.
            self._send_release(status, sync=sync, strict=False)
            return data
        if status in _TERMINAL_STATUSES and not getattr(self, "_sends_terminal_status", True):
            # A non-zero rank attached to a SHARED run (`fluent.init` sets the
            # flag; interim until per-writer leases, plan 2.8). Its ending is
            # one rank's, not the run's: rank 0 and the launcher own the close.
            # It stops beating and leaves the row as it is.
            self.stop_heartbeat()
            self._closed_status = status
            return self._data
        # 0205. `only_if_running` makes this write CONDITIONAL: it is skipped
        # when the row this handle last saw is already terminal. The designated
        # finalizer of a wrapped run (the launcher, holding the exit code) uses
        # it so it can close a run nobody else ended WITHOUT overwriting a
        # verdict the job itself already wrote from inside the work. Terminal
        # authority belongs to whoever spoke with knowledge, not to whoever's
        # request happened to land second.
        #
        # The local view can be stale, which is fine in the safe direction: if
        # the child finished after our last read we may still PATCH, and the
        # server's own guard (WHERE status = 'running') refuses it there. This
        # check exists to avoid the pointless write and the confusing audit
        # event, not as the only lock.
        if only_if_running:
            # RE-READ. The launcher's cached row is whatever it saw at attach
            # time -- always 'running' on the execute() path -- and the server
            # has NO terminal guard of its own (patch_run appends `status = $n`
            # unconditionally). Trusting the cache let a launcher exiting 0
            # overwrite a child's own `finish("failed")` with 'completed',
            # which is the verdict-authority bug this flag exists to prevent.
            # One GET, on the finalize path only.
            try:
                current = self._client.get_run(self.id).get("status")
            except Exception:
                # Cannot prove the run is still open -> do not write. A missed
                # terminal flip is recoverable (the reaper ends it); stomping a
                # real verdict is not.
                return None
            # `crashed` is the one terminal status nobody wrote with
            # knowledge: it is the reaper's GUESS (or a writer-gone report)
            # about a process that went quiet. A launcher holding the real
            # exit code replaces it -- a wrapped job that exited 0 through an
            # outage whose recovery could not run must not end `crashed`.
            # Every verdict a writer chose (completed, failed, canceled) and
            # `untracked` still stand.
            if current in _TERMINAL_STATUSES and current != "crashed":
                return None
        if status in _TERMINAL_STATUSES:
            # Stop before the PATCH: once the intent is to end the run, a beat
            # racing the flip is noise (the server no-ops late beats anyway), and
            # if the PATCH itself fails the reaper finishing the job is correct.
            self.stop_heartbeat()
            # Every close -- finish(), `probe run end` (either mode), a caller's
            # own set_status -- must land BEHIND this run's uploads, and an
            # upload still waiting for its credential scan is not in the queue
            # yet. Scanning is local CPU: finish it here, before the PATCH is
            # written or journaled.
            self._promote_uploads_before_close(
                strict=(not self._client.fail_open) if strict is None else bool(strict)
            )
        body: dict[str, Any] = {"status": status}
        # 1.10: a status write names the generation that sent it, so a
        # superseded attempt's close (sync, or replayed from the outbox after
        # a relaunch took the run over) is refused instead of closing the live
        # attempt. Only a KNOWN epoch; a server predating 1.10 ignores it.
        if self.write_epoch is not None:
            body["write_epoch"] = self.write_epoch
        if ended_at is not None:
            body["ended_at"] = ended_at
        if summary is not None:
            body.update(_summary_wire(summary))
        # `sync` belongs to the CALLER, not to this method: `finish()` drains
        # and then closes, so it needs the row in hand and passes sync=True,
        # while `probe run end --async` deliberately queues the close behind
        # the run's own data and must stay journaled.
        #
        # Fail-open, though it used to be strict=True (ProSeCo, 2026-08-19).
        # This was the one write in the SDK that propagated a TransportError,
        # and `Run.__exit__` calls it from inside an exception handler -- so a
        # network blip while a run was already failing replaced the body's real
        # traceback with a transport one and took the process down. Journaling
        # is strictly better: the status still lands on the next drain, and the
        # reaper already closes a run whose terminal flip never arrives.
        # `strict` is the CLI's door back to the old loud behaviour: `probe run
        # end` is documented as the delivery barrier, so it must still raise
        # rather than journal-and-exit-0. The SDK's finish() leaves it None and
        # fail-opens, which is what keeps a blip from killing a training
        # process; the two callers want opposite things from the same PATCH.
        # A terminal status that fails open into the journal is `admitted`: the
        # queue-length cap must not refuse the one op that closes the run, as
        # the deferred close already is not (review of #2014, H5b).
        data = self._client.write(
            "PATCH",
            f"/v1/runs/{self.id}",
            body,
            sync=sync,
            strict=strict,
            admitted=status in _TERMINAL_STATUSES,
        )
        if data:
            self._data = data
        if status in _TERMINAL_STATUSES:
            self._closed_status = status
            # This process ended the run (written, or journaled to land): tell
            # the session's daemon. Fire-and-forget, never raises.
            from ..launch import daemon_channel

            daemon_channel.run_ended(self.id, status)
        return data
from probe.sdk.run.summary import _one_summary, _summary_wire  # noqa: E402 -- pieces need each other; the front door loads this one first
