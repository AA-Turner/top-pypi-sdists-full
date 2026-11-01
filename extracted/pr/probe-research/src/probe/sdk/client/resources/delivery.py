"""DeliveryMixin, Client's methods: flush, drain for close, delivery receipts and state,
discard/resume, queued artifact uploads (twin: app/artifacts)."""

from __future__ import annotations
from ...delivery.ops.ops import UNPLACED_PROJECT
from ...delivery.journal.journal import Journal


#: What an artifact hangs off (`anchors.py`, where the lower layers can import
#: it without this module). Re-exported: `client.Anchor` is the one class.
from ...artifact.anchors import Anchor  # noqa: E402


class DeliveryMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def flush(self, *, run_ref: str | None = None, on_error=None, on_delivered=None) -> int:
        """Foreground-drain the journal; returns the delivered count.

        MACHINE-WIDE by default, and that default is load-bearing: `probe
        outbox drain`, recovery after an outage and the tests that assert a
        whole queue lands all rely on one call moving every run's ops. This is
        a NEW keyword rather than a changed default for exactly that reason.

        ``run_ref`` scopes the pass to one run's ops -- a barrier drain (T3-A),
        the same scoping ``drain(run_ref=...)`` has always offered. Pass it
        wherever the drain exists to make ONE run's writes durable, so a
        neighbour's undeliverable op cannot decide this run's outcome. The
        journal is shared per directory across runs, so an unscoped barrier
        drain stops at the first stuck op in the whole queue no matter whose
        it is.

        FIFO is not weakened by scoping: ops are still attempted in enqueue
        order within the scope, and a run's own writes only ever need to be
        ordered against each other. `Run._queue_deferred_finish` depends on
        that and no more.

        ``on_error`` observes typed delivery errors and may raise to leave the
        current operation queued for a caller that owns its retry policy.
        ``on_delivered(correlation)`` observes each durably completed operation.
        Observer failures cannot change delivery; legacy ops have no correlation.
        """
        from ...delivery.outbox.drain.drain import drain

        def one_pass():
            return drain(
                self.journal,
                run_ref=run_ref,
                client_factory=self._outbox_client_factory(),
                on_error=on_error,
                on_delivered=on_delivered,
            )

        refused = self.settings.token
        report = one_pass()
        if self._own_credential_refusal(report) and self.refresh_credentials(refused=refused):
            # Plan 2.7: a re-login revoked the token this process was built
            # with. One more pass under the current one.
            return report.delivered + one_pass().delivered
        return report.delivered

    def _drain_for_close(self, run_ref: str, *, lock_timeout: float | None):
        """One barrier pass over ``run_ref``'s ops for `Run.finish()`; returns
        the whole `DrainReport` (flush() keeps only the count), because the
        close loop needs the server's Retry-After, whether the pass got the
        drain lock, and whether it hit an auth block. ``lock_timeout`` bounds
        both the wait for that lock -- a detached worker mid-pass -- and the
        pass's promotion of waiting uploads, so neither can outlive the close's
        deadline (plan 0.6)."""
        from ...delivery.outbox.drain.drain import drain

        return drain(
            self.journal,
            run_ref=run_ref,
            client_factory=self._outbox_client_factory(),
            lock_timeout=lock_timeout,
            promote_timeout=lock_timeout,
        )

    def _delivery_journal(self) -> Journal:
        return Journal.for_receipts(
            self.journal.dir,
            context=self.journal.context,
            attribution=self.journal.attribution,
        )

    def enqueue_artifact_upload(
        self,
        *,
        correlation: str,
        anchor: Anchor | str,
        anchor_id: str,
        name: str,
        path: str,
        notes: str | None = None,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        expected_content_hash: str | None = None,
    ) -> dict:
        """Queue immutable artifact bytes with a durable, replayable receipt.

        Backpressure and source changes raise: the importer retains its intent.
        Reusing a correlation replays the frozen request, never newer source bytes.
        ``notes`` is accepted and ignored (files no longer carry notes).
        """
        from ...reads.notes_cap import FILE_NOTES_REMOVED, warn_notes_ignored
        # scanning disabled: from .redaction import default_scrub

        warn_notes_ignored(notes, FILE_NOTES_REMOVED)
        result = self._delivery_journal().append_upload(
            correlation=correlation,
            anchor=Anchor(anchor).value,
            anchor_id=anchor_id,
            name=name,
            src_path=path,
            # scanning disabled: meta=default_scrub(meta) if meta is not None else None,
            meta=meta,
            content_type=content_type,
            kind=kind,
            expected_content_hash=expected_content_hash,
        )
        self._wake_delivery()
        return result

    def enqueue_artifact_reference(
        self,
        *,
        correlation: str,
        anchor: Anchor | str,
        anchor_id: str,
        name: str,
        uri: str,
        notes: str | None = None,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        content_hash: str | None = None,
        size_bytes: int | None = None,
    ) -> dict:
        """Record a pointer through the same outbox, retaining its artifact ID.
        ``notes`` is accepted and ignored (files no longer carry notes)."""
        from ...reads.notes_cap import FILE_NOTES_REMOVED, warn_notes_ignored
        # scanning disabled: from .redaction import default_scrub

        warn_notes_ignored(notes, FILE_NOTES_REMOVED)
        anchor = Anchor(anchor)
        # Literal paths, one per anchor, for the reason `_presign_anchored` gives:
        # a segment table here once mapped EXPERIMENT to `experiments`, which the
        # parity guard could not see, so after the 5b cut an experiment-anchored
        # reference was journaled to a 410 and dead-lettered on drain.
        if anchor is Anchor.RUN:
            path = f"/v1/runs/{anchor_id}/artifacts"
        elif anchor is Anchor.EXPERIMENT:
            # Journaled by the experiment alone and placed when it drains
            # (`journal._placed`): queueing needs no network, a move before
            # delivery cannot dead-letter it, and the correlation digest names
            # no project.
            path = f"/v1/projects/{UNPLACED_PROJECT}/experiments/{anchor_id}/artifacts"
        elif anchor is Anchor.PROJECT:
            path = f"/v1/projects/{anchor_id}/artifacts"
        else:
            raise ValueError("receipt references require a run, experiment or project")
        body = {
            k: v
            for k, v in {
                "name": name,
                "uri": uri,
                "is_reference": True,
                # scanning disabled: "meta": default_scrub(meta) if meta is not None else None,
                "meta": meta,
                "kind": kind,
                "content_type": content_type,
                "content_hash": content_hash,
                "size_bytes": size_bytes,
            }.items()
            if v is not None
        }
        journal = self._delivery_journal()
        op_id = journal.append_http(
            "POST",
            path,
            body,
            correlation=correlation,
        )
        self._wake_delivery()
        return {**journal.delivery_state(correlation), "op_id": op_id}

    def delivery_receipt(self, correlation: str) -> dict | None:
        return self._delivery_journal().receipt(correlation)

    def compact_delivery_receipts(
        self, *, max_records: int = 256, max_seconds: float = 1.0
    ) -> dict:
        """Bounded local maintenance; every historical delivery identity remains readable."""
        return self._delivery_journal().compact_receipts(
            max_records=max_records, max_seconds=max_seconds
        )

    def delivery_state(self, correlation: str) -> dict:
        """Read queued, failed, discarded, or delivered state without waking a worker."""
        return self._delivery_journal().delivery_state(correlation)

    def discard_delivery(self, correlation: str) -> dict:
        """Tombstone a request that has not delivered -- queued, dead-lettered
        or half-appended -- so no drain or retry sends it again. It moves to
        ``discarded/``, like `probe outbox discard`; a delivered or unknown one
        is left as it is. Returns the state afterwards: still ``queued`` when
        another drain held the outbox (see `Journal.discard_request`)."""
        from ...delivery.journal.failures.discards import WAITING_STATES

        journal = self._delivery_journal()
        before = journal.delivery_state(correlation)["state"]
        state = journal.discard_request(correlation)
        if before in WAITING_STATES and state.get("state") == "discarded":
            with self._direct_lock:
                self._discarded_requests += 1
        return state

    def resume_delivery(self, correlation: str) -> dict:
        """Resume an already frozen request, including after the source is remounted."""
        journal = self._delivery_journal()
        state = journal.delivery_state(correlation)
        if state["state"] == "pending":
            journal.recover_intents()
        elif state["state"] == "failed":
            journal.retry_failed(state["op_id"])
        if state["state"] not in {"unknown", "discarded", "delivered"}:
            self._wake_delivery()
        return journal.delivery_state(correlation)

    def _wake_delivery(self) -> None:
        if self._drain_interval is not None:
            self._after_enqueue()
        elif self._delivery_auto_drain:
            self._kick_drainer(force=True)
