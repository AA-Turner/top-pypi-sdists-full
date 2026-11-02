"""TerminalMixin, Run's methods: journal the terminal status behind the run's queued ops and settle
a finish that fell into the journal."""

from __future__ import annotations
import time
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from probe.sdk.routes import WriteOp, path_for


class TerminalMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _queue_deferred_finish(
        self,
        status: str,
        summary: dict | None,
        pending_count: int,
        *,
        accounting: dict | None = None,
        beacon: bool = True,
    ) -> dict:
        """Journal the terminal status BEHIND this run's queued ops (F3/F3a).

        FIFO is the correctness guarantee: the run can never read terminal
        ahead of the data queued before it. The op carries the accounting a
        late drain needs -- the REAL local end time, the pending count at
        exit, and the writing session -- so "final data arrived late via the
        outbox" stays visible on the run after it lands, not just while
        queued. A best-effort beacon tags the run "draining" so the dashboard
        shows intent instead of a phantom "running"; the queued finish
        restores the tags, so the tag lives exactly as long as the drain gap.
        When the network is down (the very reason the flush timed out) the
        beacon fails silently -- nothing informs a server without a network.

        A leased handle (2.8) queues its release as the close, and only THEN
        sends one bounded DRAINING beat (`_queue_terminal_op`): its lease stays
        live (not beating) for up to an hour, so a close still delivering its
        backlog is neither closed early nor alerted on, while a requeue can
        still take the run over. Verdict first: a pre-empted job killed
        during that beat has already saved it (review of #2060).
        """
        self.stop_heartbeat()
        if not getattr(self, "_sends_terminal_status", True) and not self._leased():
            # Same rule as `set_status`: this rank's data stays queued for the
            # detached worker, but no terminal op rides behind it.
            self._client.hand_off_delivery()
            self._closed_status = status
            return {"finish_queued": False, "delivered": 0, "remaining": pending_count}
        ended_at = _now()
        # The close is queued behind the run's data, but this process is done
        # with the run: the daemon hears it now (fire-and-forget).
        from ..launch import daemon_channel

        daemon_channel.run_ended(self.id, status)
        beacon_tags: list | None = None
        # A queued tag write makes the beacon unsafe. `set_tags` REPLACES the
        # whole list, so under async the caller's tags may be sitting in the
        # queue while the server still holds the old ones. Reading the server
        # here would capture that stale list, and FIFO replay then lands the
        # queued write FIRST and this restore SECOND -- silently reverting a
        # tag change the caller made before closing. Skip the beacon entirely
        # in that case: a missing "draining" hint costs a dashboard some
        # nuance for the length of the drain, while the clobber loses data.
        if not beacon or self._has_queued_tag_write():
            return self._queue_terminal_op(
                status, summary, pending_count, ended_at, None, accounting=accounting
            )
        try:
            row = self._client.get_run(self.id)
            current = [t for t in (row.get("tags") or []) if t != "draining"]
            self._client.transport.request(
                "PATCH",
                path_for(WriteOp.RUN_PATCH, self.id),
                json_body={"tags": [*current, "draining"]},
            )
            beacon_tags = current
        except Exception:  # noqa: BLE001 -- the beacon is best-effort by definition
            beacon_tags = None
        return self._queue_terminal_op(
            status, summary, pending_count, ended_at, beacon_tags, accounting=accounting
        )

    def _queue_terminal_op(
        self,
        status: str,
        summary: dict | None,
        pending_count: int,
        ended_at: str,
        beacon_tags: list | None,
        *,
        accounting: dict | None = None,
    ) -> dict:
        """Journal the terminal PATCH behind this run's queued ops."""
        # Behind the open's snapshot writes too: an interrupted close may get here before
        # `_close_finalize` settled them, so shut that gate now, without waiting (plan O3).
        self._settle_open_snapshot(time.monotonic())
        block: dict[str, Any] = {
            **(accounting or {}),
            "deferred": True,
            "ended_at": ended_at,
            "pending_at_exit": pending_count,
            "session_id": self.session_id,
        }
        body: dict[str, Any] = {
            "status": status,
            "ended_at": ended_at,
            **_summary_wire(_with_finish_accounting(summary, block)),
        }
        leased = self._leased()
        if leased:
            # 2.8: the verdict is the lease release queued right behind this
            # PATCH; the server sets `status` when the leases say the run ended.
            del body["status"]
        if beacon_tags is not None:
            body["tags"] = beacon_tags  # clears "draining" atomically with the flip
        if self.write_epoch is not None:
            # 1.10: this op can land long after a relaunch took the run over;
            # the epoch is what lets the server refuse it then.
            body["write_epoch"] = self.write_epoch
        try:
            # `admitted`: the close skips the queue-length cap. A run whose
            # writes were dropped at the cap still has a near-full queue here,
            # and the cap refusing its close lost both the verdict and the
            # `dropped_writes` marker (review of #2014). One small op.
            if not leased or self._owns_run_fields():
                self._client.journal.append_http(
                    "PATCH", path_for(WriteOp.RUN_PATCH, self.id), body, run_ref=self.id, admitted=True
                )
            if self._lease is not None:
                # Leased: the verdict. On a run that is not `leases` the PATCH
                # above keeps its `status` (HIGH-1) and this marks the lease
                # released behind it.
                session = self._lease["session_id"]
                self._client.journal.append_http(
                    "POST",
                    f"/v1/runs/{self.id}/writers/{session}/release",
                    self._release_body(status),
                    run_ref=self.id,
                    admitted=True,
                )
            self._closed_status = status
        except Exception as exc:  # noqa: BLE001 -- a close never raises over its bookkeeping
            # Nowhere left to record the verdict: the server did not take the
            # data in time and the outbox cannot take the close (read-only,
            # full). Raising here would turn a finished run into a crashed
            # script at its last line. Say so; the run stays open until the
            # server's reaper closes it, and whatever data IS queued is still
            # handed to the worker below.
            _diagnostics.warn(
                f"probe: run {self.id} could not be closed: the server did not take "
                f"its last {pending_count} write(s) in time and the outbox cannot "
                f"record the close ({_diagnostics.describe(exc)}). The server will "
                "close the run when it goes quiet. See `probe outbox status`.",
                stacklevel=3,
            )
            try:
                self._client.hand_off_delivery()
            except Exception:  # noqa: BLE001
                pass
            return {
                "finish_queued": False,
                "delivered": 0,
                "remaining": pending_count,
                "close_unrecorded": True,
            }
        # The in-process exporter dies with this (exiting) process; hand the
        # journal to the crash-surviving detached worker instead. One shared
        # helper, because this site and `_settle_journaled_finish` used to be
        # near-duplicates and only one of them got fixed.
        self._client.hand_off_delivery()
        if leased:
            # AFTER the verdict is on disk: bounded, best-effort.
            self._draining_beat()
        return {"finish_queued": True, "delivered": 0, "remaining": pending_count + 1}

    def _latest_terminal_patch(self) -> tuple[str, Any] | None:
        """``("pending" | "failed", path)`` for this run's NEWEST queued
        terminal-status PATCH, or None. Op filenames sort by enqueue time."""
        journal = self._client.journal
        best: tuple[str, Any] | None = None
        for where, rows in (("pending", journal.pending()), ("failed", journal.failed())):
            for path, op in rows:
                terminal = (
                    op.get("method") == "PATCH"
                    and (op.get("body") or {}).get("status") in _TERMINAL_STATUSES
                ) or (
                    # 2.8: a leased handle's terminal op is its lease release.
                    op.get("method") == "POST"
                    and str(op.get("path") or "").endswith("/release")
                )
                if (
                    op.get("run_ref") == self.id
                    and terminal
                    and (best is None or path.name > best[1].name)
                ):
                    best = (where, path)
        return best

    def _settle_journaled_finish(
        self, *, strict: bool, deadline: float | None = None, dropped: bool = False
    ) -> dict:
        """The terminal PATCH fail-opened into the journal instead of landing.

        `set_status` no longer raises on a transport failure, which is what
        keeps a blip from killing a training process -- but the run is then not
        closed server-side yet, and returning the caller a bare None would be
        the very "closed 'completed' over silently missing data" that the
        barrier exists to prevent. So: drain once more (within what is left of
        the close's ``deadline``), then say plainly which of the two happened,
        in the same shape a deferred finish reports.

        Judged by the TERMINAL PATCH itself, never by the run's dead letters in
        general: a default close now proceeds past DATA dead letters (it marks
        them on the run), and counting those read a close that had landed as
        "the terminal status was rejected" (review of #2011). A rejected close
        raises only under ``strict``; otherwise it warns and the server's reaper
        closes the run. Whatever of the run is still queued is handed to the
        detached worker either way.

        The run lock is NOT released while anything is queued: the close has
        not been confirmed, and holding the lock slightly too long is the cheap
        failure.

        ``dropped``: the terminal PATCH did not even reach the journal (an
        unwritable outbox). The close is then reported ``close_unrecorded``,
        never as delivered, and the server's reaper closes the run (review of
        #2014, H5b).
        """
        journal = self._client.journal
        if dropped and self._latest_terminal_patch() is None:
            _diagnostics.warn(
                f"probe: run {self.id} could not be closed: the server did not take its "
                "status in time and the outbox cannot record it. The server will mark the "
                "run crashed once it goes quiet (about 15 minutes; a run over 3 hours also "
                "sends a crash email). See `probe outbox status`."
            )
            self._client.hand_off_delivery()
            return {
                "finish_queued": False,
                "delivered": 0,
                "remaining": len(self._queued_ops(journal.pending())),
                "close_unrecorded": True,
            }
        left = None if deadline is None else max(0.0, deadline - time.monotonic())
        try:
            # Scoped, like the loop in finish(): this drain exists to land THIS
            # run's fail-opened terminal PATCH. The lock wait and the promotion
            # are bounded by the close's deadline, like every other wait in it.
            self._client._drain_for_close(self.id, lock_timeout=left)
        except Exception:  # noqa: BLE001 -- drain records last_error itself
            pass
        terminal = self._latest_terminal_patch()
        remaining = len(self._queued_ops(journal.pending()))
        if remaining:
            # Wake delivery. The op arrived through the sync fail-open branch,
            # which -- unlike the async branch -- does NOT call `_after_enqueue`,
            # so nothing has kicked a drainer. `Run.__exit__` usually exits the
            # process immediately after this, so without the handoff the close
            # sits on disk until some unrelated future `probe` command. See
            # `Client.hand_off_delivery` for why this is gated on the transport
            # and why a dead exporter is not cleared.
            self._client.hand_off_delivery()
        if terminal is not None and terminal[0] == "failed":
            message = (
                f"run {self.id} not closed: the terminal status was rejected and "
                "dead-lettered — see `probe outbox status`, then `probe outbox retry`"
            )
            if strict:
                raise errors.RosError(message)
            _diagnostics.warn(f"probe: {message}. The server will close the run when it goes quiet.")
            return {
                "finish_queued": False,
                "delivered": 0,
                "remaining": remaining,
                "close_rejected": True,
            }
        if not remaining:
            self._release_run_lock()
        return {
            "finish_queued": bool(remaining),
            "delivered": 0 if remaining else 1,
            "remaining": remaining,
        }

    def _close_recorded(self, report: dict) -> bool:
        """Whether the terminal status -- and the accounting it carries -- was
        written or queued, as opposed to refused or unrecordable."""
        return (
            getattr(self, "_closed_status", None) is not None
            and not report.get("close_unrecorded")
            and not report.get("close_rejected")
        )
from probe.sdk.run.closing.status import _TERMINAL_STATUSES  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.metrics.values import _now  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.summary import _summary_wire, _with_finish_accounting  # noqa: E402 -- pieces need each other; the front door loads this one first
