"""WriterLeaseMixin, Run's methods: the writer lease at close: what a lease answer says, the
draining beat, and the release write."""

from __future__ import annotations
import time
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from probe.sdk.routes import WriteOp, path_for


#: How long a finishing writer's draining beat keeps its lease live (2.8):
#: the server's cap. The queued release ends it sooner when it lands.
_LEASE_DRAIN_SECONDS = 3600.0
#: The most a close spends on one lease beat of its own (the draining beat, or
#: the beat that learns an unknown protocol): a liveness hint must never hold a
#: pre-empted job's exit (review of #2060).
_CLOSE_BEAT_SECONDS = 5.0
#: The least a deferred close's draining beat gets. That beat goes out AFTER
#: the close's own budget ran out -- the reason it deferred -- so under what was
#: left of it the beat was never sent: the lease then expired while the worker
#: was still delivering, and `writer_lost` fired falsely. It holds a close past
#: its deadline by at most this much.
_DRAINING_BEAT_MIN_SECONDS = 1.0


class WriterLeaseMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _owns_run_fields(self) -> bool:
        """A leased writer whose close carries the run's own fields (end
        time, headline scalars): an owner or a launcher, never a rank."""
        return getattr(self, "_sends_terminal_status", True) and (
            (self._lease or {}).get("role") != "rank"
        )

    def _leased(self) -> bool:
        """Whether this handle closes through its lease (2.8): it has one, and
        the server said the run follows the lease rules. Anything else -- the
        server's `legacy` (NULL, flipped, the kill switch off) or no answer
        yet -- closes the pre-2.8 way (review of #2060, HIGH-1)."""
        return self._lease is not None and self._lease_protocol == "leases"

    def _note_lease_answer(self, resp: Any) -> None:
        """What a lease beat's answer says: the lease is registered, which rules
        the run follows, and -- once -- that something reported this writer
        dead while it still runs (its lease is GONE: its verdict reads
        `crashed` unless its own recovery reopens the run)."""
        self._lease_registered = True
        if not isinstance(resp, dict):
            return
        if resp.get("liveness_protocol"):
            self._lease_protocol = resp["liveness_protocol"]
        if "commands_seq" in resp:
            self._check_sample_commands(resp["commands_seq"])
        if resp.get("lease") == "gone" and not getattr(self, "_lease_gone_warned", False):
            self._lease_gone_warned = True
            _diagnostics.warn(
                f"probe: run {self.id}: this process was reported dead (writer-gone) while "
                "it is still running; the server counts its lease as crashed."
            )

    def _release_body(self, status: str) -> dict:
        """A release names its writer, so a lease no beat registered still counts."""
        writer = {k: v for k, v in (self._lease or {}).items() if k != "session_id"}
        return {"write_epoch": self.write_epoch or 1, "exit_status": status, "writer": writer}

    def _send_release(self, status: str, *, sync: bool, strict: bool | None):
        """POST this writer's release through `Client.write` (journaled on a
        transport failure, behind whatever this close already wrote)."""
        session = self._lease["session_id"]
        # Literal call site: the tests/test_parity.py AST scan must see the route.
        return self._client.write(
            "POST",
            f"/v1/runs/{self.id}/writers/{session}/release",
            self._release_body(status),
            sync=sync,
            strict=strict,
        )

    def _release_dead_writer(self, status: str) -> None:
        """A child this launcher ran was stopped on purpose (`execute`), and its own writer lease
        is still open: release it with that verdict, before this machine's watcher reports it gone
        (counted `crashed`, worse than `canceled`). The child is the watcher registry's entry for
        this run naming a process that is gone and whose parent was this one: never another
        rank's lease, whose own death may be a real crash. Never raises."""
        try:
            import os

            from ..watcher import registry

            for entry in registry.entries():
                writer = entry.get("writer") or {}
                session = writer.get("session_id")
                if (
                    entry.get("run_id") != self.id
                    or not registry.is_local(entry)
                    or entry.get("ppid") != os.getpid()
                    or not session
                    or session == getattr(self, "session_id", None)
                    or writer.get("write_epoch") is None
                    or registry.process_is_alive(entry)
                ):
                    continue
                body = {"write_epoch": int(writer["write_epoch"]), "exit_status": status}
                try:
                    # A refusal (no such lease) is not worth a dead letter; a blip is journaled.
                    self._client.write(
                        "POST",
                        f"/v1/runs/{self.id}/writers/{session}/release",
                        body,
                        sync=True,
                        strict=False,
                        raise_permanent=True,
                    )
                except Exception:  # noqa: BLE001
                    continue
                registry.deregister(self.id)
        except Exception:  # noqa: BLE001 -- the watcher's report and the reaper still end the run
            pass

    def _release_lease(
        self,
        status: str,
        *,
        ended_at: str | None,
        summary: dict | None,
        sync: bool,
        strict: bool | None,
    ):
        """The terminal write of a leased handle on a `leases` run (2.8).

        The run's own fields (the end time, the headline scalars) still go as
        a PATCH -- WITHOUT `status`, which is now the server's to decide -- from
        a writer whose verdict the run carries (not a non-zero rank's, as
        before). Then the release, naming the writer. Both go through
        `Client.write`, so a transport failure journals them in this order,
        behind the run's data, and `finish()` settles a journaled close as it
        always has. A run flipped to legacy between the last beat and this
        release needs nothing more: on a run that is not `leases` the server
        closes it on an owner's or launcher's release, with its verdict."""
        self.stop_heartbeat()
        self._promote_uploads_before_close(
            strict=(not self._client.fail_open) if strict is None else bool(strict)
        )
        data = None
        # The run's own fields (end time, headline scalars) come from a writer
        # whose verdict the run carries: an owner or a launcher. A job that
        # joined from inside the work and owns its verdict (a forwarded
        # PROBE_RUN_ID, a hand-off) holds an OWNER lease for exactly that; a
        # rank, or a job under a finalizing launcher, sends none. Nobody sends
        # `status`: the leases decide it, and a status written after their
        # close overwrote the worst verdict (review of #2060).
        owns_verdict = self._owns_run_fields()
        if owns_verdict and (ended_at is not None or summary is not None):
            body: dict[str, Any] = {}
            if ended_at is not None:
                body["ended_at"] = ended_at
            if summary is not None:
                body.update(_summary_wire(summary))
            data = self._client.write("PATCH", path_for(WriteOp.RUN_PATCH, self.id), body, sync=sync, strict=strict)
        resp = self._send_release(status, sync=sync, strict=strict)
        self._closed_status = status
        from ..launch import daemon_channel

        daemon_channel.run_ended(self.id, status)
        if not isinstance(resp, dict):
            # Journaled (fail-open) or queued: the release lands on the next
            # drain. `finish()` reads it as the pending terminal op.
            return None if owns_verdict or data is None else data
        if resp.get("liveness_protocol"):
            self._lease_protocol = resp["liveness_protocol"]
        if "commands_seq" in resp:
            self._check_sample_commands(resp["commands_seq"])
        row = dict(data if isinstance(data, dict) else self._data)
        if resp.get("run_status"):
            row["status"] = resp["run_status"]
        self._data = row
        return row

    def _draining_beat(self, *, draining: bool = True) -> None:
        """One synchronous lease beat saying this writer is finishing (2.8),
        or (``draining=False``) registering it and learning the run's rules.
        Best-effort and bounded (`_CLOSE_BEAT_SECONDS`; the registering beat
        also inside any close's own deadline, the draining one given at least
        `_DRAINING_BEAT_MIN_SECONDS` of its own): nothing informs a server
        without a network, and the lease then simply expires."""
        from ...delivery.transport.deadlines import deadline_remaining, deadline_scope, fresh_deadline_scope

        lease = self._lease or {}
        body = {k: v for k, v in lease.items() if k != "session_id"}
        body.update({"write_epoch": self.write_epoch or 1, **self._progress.snapshot()})
        # What this script can be asked: a beat without it reads as an SDK older than run commands (W16).
        body["capabilities"] = self._get_command_capabilities()
        if getattr(self, "attached", False):
            body["attached"] = True
        delivery = _delivery_body(self._client, self.id)
        if delivery:
            body["delivery"] = delivery  # R13: the backlog this writer leaves the worker
        if draining:
            body["draining_for_seconds"] = _LEASE_DRAIN_SECONDS
            # What is left of the close's budget, but never under
            # `_DRAINING_BEAT_MIN_SECONDS`: a nested `deadline_scope` would keep
            # the close's spent deadline and raise before sending.
            left = deadline_remaining(_CLOSE_BEAT_SECONDS)
            scope = fresh_deadline_scope(
                time.monotonic() + max(left, _DRAINING_BEAT_MIN_SECONDS)
            )
        else:
            scope = deadline_scope(time.monotonic() + _CLOSE_BEAT_SECONDS)
        try:
            with scope:
                resp = self._client.beat_writer(self.id, lease["session_id"], body)
            self._note_lease_answer(resp)
        except Exception:  # noqa: BLE001 -- a liveness hint, never a reason a close fails
            pass
from probe.sdk.run.summary import _summary_wire  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.closing.heartbeat import _delivery_body  # noqa: E402 -- pieces need each other; the front door loads this one first
