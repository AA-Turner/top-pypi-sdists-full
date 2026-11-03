"""StatusMixin, Run's methods: run.set_status and the status a sys.exit code or exception means."""

from __future__ import annotations
from typing import Any
from probe.sdk.routes import WriteOp, path_for


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
            # The open's snapshot writes are queued AHEAD of the verdict, never behind it (plan O3).
            self._settle_open_snapshot()
            if self._lease_protocol is None and sync:
                # No beat of this lease has answered yet: one bounded beat
                # learns which rules the run follows (and registers the lease).
                self._draining_beat(draining=False)
            if self._leased():
                # 2.8: a lease's writer RELEASES it with its verdict; the server closes on the worst one.
                return self._release_lease(
                    status, ended_at=ended_at, summary=summary, sync=sync, strict=strict
                )
            # A lease on a run NOT on leases closes as before 2.8, then releases (#2060 review, HIGH-1).
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
            # A non-zero rank on a SHARED run (interim, plan 2.8): rank 0 and the launcher own the close.
            self.stop_heartbeat()
            self._closed_status = status
            return self._data
        # 0205: `only_if_running` skips the write when the run is already terminal, so the finalizer
        # never overwrites a verdict the job wrote itself (DESIGN.md).
        if only_if_running:
            # RE-READ, never the cached row: trusting it let a launcher overwrite a child's `failed` (DESIGN.md).
            try:
                current = self._recorded_status()
            except Exception:
                # Cannot prove the run is open: do not write (the reaper ends it; a stomped verdict is lost).
                return None
            # `crashed` is the reaper's guess: a launcher holding the real exit code replaces it.
            if current in _TERMINAL_STATUSES and current != "crashed":
                return None
        if status in _TERMINAL_STATUSES:
            # Stop beating before the PATCH: a beat racing the flip is noise.
            self.stop_heartbeat()
            # The open's snapshot writes are queued AHEAD of the verdict, never behind it (plan O3).
            self._settle_open_snapshot()
            # Every close lands BEHIND this run's uploads: finish their credential scans first.
            self._promote_uploads_before_close(
                strict=(not self._client.fail_open) if strict is None else bool(strict)
            )
        body: dict[str, Any] = {"status": status}
        # 1.10: name this generation, so a superseded attempt's close is refused (known epochs only).
        if self.write_epoch is not None:
            body["write_epoch"] = self.write_epoch
        if ended_at is not None:
            body["ended_at"] = ended_at
        if summary is not None:
            body.update(_summary_wire(summary))
        # `sync` is the caller's (finish() needs the row). Fail-open into the journal unless `strict` (the
        # CLI's `probe run end`); the terminal op is `admitted` past the queue cap (#2014 H5b). DESIGN.md.
        data = self._client.write(
            "PATCH",
            path_for(WriteOp.RUN_PATCH, self.id),
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

    def _recorded_status(self) -> str | None:
        """The run's status where its record lives (the server); an offline run reads its queue."""
        return self._client.get_run(self.id).get("status")
from probe.sdk.run.summary import _one_summary, _summary_wire  # noqa: E402 -- pieces need each other; the front door loads this one first
