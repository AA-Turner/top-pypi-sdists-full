"""ReopenMixin, Client's methods: resume an incumbent run: deliver its queued backlog and close
before taking over (twin: app/runs)."""

from __future__ import annotations
import time
import uuid
from ......foundation.safe_warn import safe_warn as _diagnostics

from ..... import errors


# Late import to avoid a cycle at module load (Run needs Client, Client returns Run).
from .....run.run import Run  # noqa: E402
_TAKEOVER_DRAIN_SECONDS = 120.0


def _is_waited_for(op: dict) -> bool:
    """Whether the takeover barrier waits for ``op``, and sends it: not a non-blocking op on a lane
    of its own (the open's code-bytes archive; multipart uploads have a queue no barrier reads).
    Nothing of the run is ordered after one, no write epoch fences an upload, and a store that
    never answers it must not spend the barrier's budget."""
    return not (op.get("blocking") is False and isinstance(op.get("lane"), str) and op["lane"])


class ReopenMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _resume_run(
        self,
        old: dict,
        run_kw: dict,
        *,
        rewind_to_step: int | None = None,
        takeover: bool = False,
    ) -> Run:
        """Reopen a dead incumbent and hand back a live handle on it.

        The session id minted here is the writer fingerprint the reopen
        registers (research-os#364): the engine's write epoch bumps, so a
        zombie predecessor still logging can be told apart from this process
        — and, since 0185, refused at the door (the receipt's epoch rides on
        every write the handle makes). The receipt's ``last_step`` arms the
        handle's resume guard. Snapshot again after this returns — each
        attempt's code+env is its own execution record.

        ``rewind_to_step`` asks the reopen to discard the record from that
        step onward in the same transaction. The echo check is the second
        lock behind the feature preflight: never trust a destructive request
        a server did not explicitly confirm honoring.

        ``takeover`` (2.3) reopens a `running` incumbent the server judges
        silent, waiting within ``PROBE_TAKEOVER_WAIT_SEC`` when it is not
        silent yet. Either way the incumbent's own queued ops in this outbox
        are delivered FIRST: a replacement pod on a persistent outbox finds
        the old attempt's epoch-E ops there, and the reopen's E+1 would fence
        every one of them.

        The incumbent's queued STATUS writes are held aside meanwhile, and
        retired only once the reopen succeeds: then the relaunch owns the
        verdict (and 1.10's fence would refuse them anyway). Any refusal or
        error puts them back, so a relaunch that does NOT take over never
        costs the incumbent its close (review of #2019, MED-A)."""
        from .....delivery.transport.deadlines import without_patience

        # Both long steps have their own bounds (PROBE_TAKEOVER_DRAIN_SEC and
        # PROBE_TAKEOVER_WAIT_SEC), and `probe.init()`'s budget (#2027,
        # PROBE_INIT_TIMEOUT_SEC) must not cut them off: a requeue that waits
        # for its dead incumbent to go quiet would otherwise die at 90 s with
        # a DeadlineExceeded after doing most of the wait.
        closes = self._queued_completed_close(old) if takeover else False
        with without_patience():
            held = self._drain_before_takeover(old)
        if closes:
            # The incumbent FINISHED: its `completed` close was still queued
            # here, and the barrier just delivered it. A resume never appends
            # onto a completed run; a rewind still may (review of #2019).
            fresh = self.get_run(old["id"])
            if fresh.get("status") == "completed":
                if rewind_to_step is None:
                    self._release_status_writes(held, retire=False)
                    name = old.get("slug") or old.get("id")
                    raise errors.ConflictError(
                        f"run {name!r} already completed -- its close was still queued "
                        "in this outbox and has now been delivered. Resuming would append "
                        'onto a good record. Repeat it deliberately with on_conflict='
                        '"supersede", or rewind it from a checkpoint with '
                        "on_conflict=probe.Rewind(step=N)."
                    )
                takeover = False  # a rewind of a completed run is a plain reopen
        session_id = str(uuid.uuid4())
        # 2.8: the resumed attempt writes under its own lease -- a launcher's
        # when a launcher resumes, and none when it will not beat (as a create).
        writer = (
            _writer_lease("launcher" if run_kw.get("launcher") else "owner", session_id)
            if run_kw.get("heartbeat", True) and self._leases_available()
            else None
        )
        try:
            if takeover:
                with without_patience():
                    receipt = self._reopen_taking_over(
                        old,
                        session_id,
                        rewind_to_step,
                        heartbeat=run_kw.get("heartbeat", True),
                        launcher=bool(run_kw.get("launcher")),
                        writer=writer,
                    )
            else:
                receipt = self.reopen_run(
                    old["id"], session_id=session_id, rewind_to_step=rewind_to_step, writer=writer
                )
        except BaseException:
            self._release_status_writes(held, retire=False)
            raise
        self._release_status_writes(held, retire=True)
        self._clear_draining_tag(old, receipt)
        if rewind_to_step is not None and receipt.get("rewound_to") != rewind_to_step:
            raise errors.ConflictError(
                f"reopen returned no rewind echo for step {rewind_to_step} — "
                "the server did not honor the rewind (a pre-0185 backend "
                f"drops the field silently). Run {old['id']} is now reopened "
                "WITHOUT anything deleted; its old points still hold their "
                "steps. Upgrade the server, then retry."
            )
        row = receipt.get("run") or receipt
        if receipt.get("write_epoch") is not None:
            _repin_bracket_lease(old["id"], receipt["write_epoch"])
        handle = self.attach_run(
            row,
            heartbeat=run_kw.get("heartbeat", True),
            session_id=session_id,
            resume_from_step=receipt.get("last_step"),
            write_epoch=receipt.get("write_epoch"),
            writer=writer,
        )
        # A retry wrapper resuming inside the last attempt's `except`: that error is not this one's.
        from probe.sdk.diagnostics import mark_run_opened_during

        mark_run_opened_during(handle)
        return handle

    def _queued_completed_close(self, old: dict) -> bool:
        """Whether this outbox still holds the incumbent's queued `completed`
        close (one read of the queue; False when it cannot be read)."""
        refs = {str(r) for r in (old.get("id"), old.get("slug")) if r}
        try:
            return any(
                op.get("run_ref") in refs
                and (
                    (
                        op.get("method") == "PATCH"
                        and (op.get("body") or {}).get("status") == "completed"
                    )
                    # 2.8: a leased writer's verdict is its queued release.
                    or (
                        op.get("method") == "POST"
                        and str(op.get("path") or "").endswith("/release")
                        and (op.get("body") or {}).get("exit_status") == "completed"
                    )
                )
                for _, op in self.journal.pending()
            )
        except Exception:  # noqa: BLE001 -- unreadable: nothing is known to be queued
            return False

    def _drain_before_takeover(self, old: dict) -> None:
        """Deliver what the incumbent left queued HERE before its epoch moves.

        Scoped to the incumbent's refs (its id, and its slug for CLI ops), and
        to the ops queued BEFORE this barrier began: an op of those refs that
        appears meanwhile means a LIVE writer shares this outbox (a duplicate
        launch on the same box), so the barrier stops at once and the takeover
        conflicts as it should, instead of chasing a live queue and then
        warning about ops that are not a dead attempt's.

        The incumbent's queued STATUS writes are HELD aside, never delivered
        by the barrier: a queued `completed` would close the run the relaunch
        is taking over (and fail it), a queued `failed` would mail a crash
        notice. Returns their names; `_resume_run` retires them once the
        reopen succeeds and puts them back otherwise. Data still lands, under
        the old epoch, before the reopen moves it.

        Bounded by ``PROBE_TAKEOVER_DRAIN_SEC`` (120), every request of every
        pass included (`deadline_scope`). A detached worker mid-pass holds the
        drain lock, so this never blocks on it.
        What is still queued at the bound is SAID, not silently fenced."""
        refs = {str(r) for r in (old.get("id"), old.get("slug")) if r}
        mine = str(self.journal.dir)

        def _add_waiting(queue, where: str, out: dict) -> None:
            for name, op_id, ref, readable, _blocking in queue._waiting_items():
                if readable and ref in refs:
                    out.setdefault((where, name), {"op_id": op_id, "run_ref": ref})

        def queued() -> dict[tuple[str, str], dict]:
            """The incumbent's queued ops, by (queue, name): this client's queue,
            and every other queue of the outbox whose own worker is running --
            writes of the run queued under another credential (#2035) that
            someone is delivering right now (#2041 round 5). One nobody can
            send here is only named in the warning below. The ops the barrier
            does not wait for (`_is_waited_for`: the open's archive) are left out.
            Uploads still in a waiting room count too, under the name their
            promotion writes them as: promoted meanwhile (by a barrier pass, by
            a worker), they are the same backlog, not a live writer's."""
            out: dict[tuple[str, str], dict] = {}
            try:
                for path, op in self.journal.pending():
                    if op.get("run_ref") in refs and _is_waited_for(op):
                        out[(mine, path.name)] = op
                _add_waiting(self.journal, mine, out)
                for queue in self.journal.other_queues():
                    if queue.receipt_enabled or not queue.worker_alive():
                        continue
                    for path, op in queue.pending():
                        if op.get("run_ref") in refs and _is_waited_for(op):
                            out[(str(queue.dir), path.name)] = op
                    _add_waiting(queue, str(queue.dir), out)
            except Exception:  # noqa: BLE001 -- an unreadable queue has nothing to barrier
                return out
            return out

        # A relaunch killed mid-barrier left its hold behind: put it back.
        self._restore_expired_holds()
        if not refs:
            return []
        before = queued()
        if not before and not self._incumbent_writes_elsewhere(refs):
            return []
        held = self._hold_status_writes(
            old, {name: op for (where, name), op in before.items() if where == mine}
        )
        try:
            return self._deliver_backlog(old, refs, queued, held)
        except BaseException:
            # Ctrl-C or a bug mid-barrier: the hold must not outlive it.
            self._release_status_writes(held, retire=False)
            raise

    def _deliver_backlog(self, old: dict, refs: set[str], queued, held: list[str]) -> list[str]:
        """The barrier's delivery loop (see `_drain_before_takeover`).

        ONE deadline, inside a pass too (#2011's `deadline_scope`): each
        request of the drain is bounded by what is left of
        ``PROBE_TAKEOVER_DRAIN_SEC``, and one that would start after it is not
        sent, so a long backlog can no longer hold a relaunch's `init()` for as
        long as a whole pass takes (review of #2019, MED-2)."""
        from ......foundation.durable.durable import backoff_delays
        from .....delivery.outbox.drain.drain import drain
        from .....delivery.transport.deadlines import deadline_scope

        before = queued()
        # Only what it waits for: a pass sending the open's archive could spend the budget on it.
        waited_for = frozenset(op.get("op_id") for op in before.values() if op.get("op_id"))
        budget = _env_seconds("PROBE_TAKEOVER_DRAIN_SEC", _TAKEOVER_DRAIN_SECONDS)
        deadline = time.monotonic() + budget
        delays = backoff_delays(1_000_000, (0.5, 10.0))
        remaining: set[str] = set(before)
        outage = False
        while remaining:
            for ref in sorted(refs):
                if time.monotonic() >= deadline:
                    break
                try:
                    with deadline_scope(deadline):
                        report = drain(
                            self.journal,
                            run_ref=ref,
                            only_ops=waited_for,
                            client_factory=self._outbox_client_factory(),
                            wait_for_lock=False,
                            promote_timeout=max(0.0, deadline - time.monotonic()),
                        )
                except errors.TransportError:
                    outage = True
                except Exception:  # noqa: BLE001 -- the bound below decides, not one error
                    pass
                else:
                    # The run's own lane only: an upload on a lane of its own (the open's
                    # archive) stalls on the store, which says nothing about the API.
                    stall = (report.stalled_runs or {}).get(ref)
                    if (
                        report.unreachable
                        or report.auth_blocked
                        or (
                            stall is not None
                            and stall.status is None
                            # A HELD run sent nothing, so says nothing about the
                            # server (#2041 round 5).
                            and not getattr(stall, "held", False)
                        )
                    ):
                        # The server cannot be reached (or refuses the
                        # credential): nothing of the backlog can land, and the
                        # reopen after this would fail the same way. Stop now
                        # rather than loop for the whole budget outside
                        # `probe.init()`'s own (review of #2019).
                        outage = True
                if outage:
                    break
            if outage:
                break
            now_queued = queued()
            if set(now_queued) - set(before):
                # A live writer is appending: not a dead attempt's backlog, and
                # its verdict is its own. Back at once, ahead of what it adds.
                self._release_status_writes(held, retire=False)
                return []
            remaining = set(now_queued) & set(before)
            now = time.monotonic()
            if not remaining or now >= deadline:
                break
            time.sleep(min(next(delays), max(deadline - now, 0.0)))
        if outage:
            remaining = set(queued()) & set(before)
        stranded = self._incumbent_writes_elsewhere(refs)
        if remaining or stranded:
            why = (
                "the server could not be reached"
                if outage
                else f"not delivered within {budget:g}s (PROBE_TAKEOVER_DRAIN_SEC)"
            )
            also = (
                f" {stranded} of them are queued under another credential this process "
                "does not hold (a rotated PROBE_TOKEN, say) and no worker of that "
                "credential is running: they cannot land before the reopen."
                if stranded
                else ""
            )
            _diagnostics.warn(
                f"probe: {len(remaining) + stranded} op(s) the previous attempt of run "
                f"{old.get('slug') or old.get('id')} queued in this outbox were not "
                f"delivered: {why if remaining else 'nothing here may send them'}.{also} If "
                "this relaunch reopens the run under a new write epoch the server will "
                "refuse them; they stay visible in `probe outbox status`."
            )
        return held

    def _incumbent_writes_elsewhere(self, refs: set[str]) -> int:
        """The incumbent's queued writes in OTHER credential queues (#2035)
        that no running worker is delivering: stranded as far as a takeover
        is concerned (#2041 round 5, a relaunch with a rotated PROBE_TOKEN)."""
        count = 0
        try:
            for queue in self.journal.other_queues():
                if queue.receipt_enabled or queue.worker_alive():
                    continue
                count += sum(
                    1 for _path, op in queue.pending() if op.get("run_ref") in refs and _is_waited_for(op)
                )
        except Exception:  # noqa: BLE001 -- best-effort: the warning is the point
            return count
        return count
from probe.sdk.client.resources.runs.reopen.conflict import _repin_bracket_lease, _writer_lease  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.runs.reopen.takeover import _env_seconds  # noqa: E402 -- pieces need each other; the front door loads this one first
