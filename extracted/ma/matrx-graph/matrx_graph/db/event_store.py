from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from matrx_utils import client_error_text


class EventStore:
    """Append-only writer/reader for ``workflow.node_events`` with per-run ``seq``.

    Why this exists (audit P1-5/6/7/8): event identity used to be
    ``event_ts`` (millisecond resolution) — parallel nodes share a
    millisecond, so a strict ``event_ts > cursor`` poll PERMANENTLY skipped
    the second event when two same-ms events split across fetches. ``seq``
    is a per-run serial assigned here.

    The insert is ONE statement: a CTE bumps ``workflow.run.event_seq`` and feeds
    the ``INSERT``. The ``UPDATE`` takes the workflow.run row lock, so concurrent
    event inserts for the same run serialize and **commit order == seq
    order** — a ``seq > cursor`` poll can never miss a row that becomes
    visible later (no out-of-order commit window, unlike timestamps or a
    global sequence).
    """

    async def insert_event(
        self,
        run_id: str,
        *,
        event_type: str,
        payload: dict[str, Any],
        step: int | None = None,
        node_id: str | None = None,
        spec_type: str | None = None,
        attempt: int | None = None,
        duration_ms: int | None = None,
        checkpoint_id: str | None = None,
        error_type: str | None = None,
        error_message: str | None = None,
        event_ts: datetime | None = None,
    ) -> int:
        """Insert one event; returns its per-run ``seq`` (1-based)."""
        # MKT-167: large data values go by reference into the run's value store
        # BEFORE the row is written (a payload the host already interned is unchanged).
        from matrx_graph.checkpoint.value_store import intern_event_payload

        payload = await intern_event_payload(run_id, payload)
        cp_uuid: UUID | None = None
        if checkpoint_id:
            try:
                cp_uuid = UUID(checkpoint_id)
            except (ValueError, TypeError):
                cp_uuid = None

        from matrx_orm import F, transaction

        from matrx_graph.db._registry import get_model
        from matrx_graph.db.run_store import update_run

        run_uuid = UUID(run_id)
        # Atomically bump workflow.run.event_seq (row lock held until COMMIT)
        # then insert the event carrying that seq — both statements ride the
        # SAME connection/transaction via matrx-orm's transaction() ContextVar,
        # so the run row lock still serializes concurrent inserts for the same
        # run and commit order still == seq order (the invariant this store
        # exists to guarantee), exactly like the single-CTE statement it
        # replaces.
        async with transaction():
            bump = await update_run(
                {"id": run_uuid}, returning=("id", "event_seq", "organization_id"), event_seq=F("event_seq") + 1
            )
            if not bump.updated_rows:
                raise ValueError(f"insert_event: run '{run_id}' not found in workflow.run")
            seq = bump.updated_rows[0]["event_seq"]
            # workflow.node_events.organization_id is NOT NULL. An event is a
            # CHILD of its run — the UPDATE above hands back organization_id
            # beside the seq (never the whole row), so carry it from there
            # rather than a second lookup or a default.
            organization_id = bump.updated_rows[0].get("organization_id")
            if not organization_id:
                raise ValueError(
                    f"insert_event: run '{run_id}' has no resolvable organization_id"
                )
            from matrx_graph.failure import client_safe_error_payload

            instance = await get_model("WfNodeEvents").create(
                run_id=run_uuid,
                organization_id=organization_id,
                event_type=event_type,
                step=step,
                node_id=node_id,
                spec_type=spec_type,
                attempt=attempt,
                duration_ms=duration_ms,
                checkpoint_id=cp_uuid,
                error_type=error_type,
                error_message=client_error_text(error_message) if error_message else error_message,
                payload=client_safe_error_payload(payload),
                event_ts=event_ts or datetime.now(UTC),
                seq=seq,
            )
        return int(instance.seq)

    async def insert_events(
        self, run_id: str, events: list[dict[str, Any]], *, run_updates: dict[str, Any] | None = None
    ) -> list[int]:
        """Insert several events of one run in ONE transaction; returns their ``seq`` in order.

        Same invariant as :meth:`insert_event` (the run row lock serializes seq assignment; commit order ==
        seq order): ONE bump reserves ``len(events)`` consecutive seqs, ONE multi-row INSERT writes them in
        list order. A burst of N events costs 4 round trips instead of 4N — what keeps the screen's event
        tail from lagging behind the run. Each dict carries :meth:`insert_event`'s keyword arguments.

        ``run_updates``: other ``workflow.run`` columns the host writes with these events (its
        heartbeat), set by the SAME statement that reserves the seqs, so the run row is locked once
        per batch, never again by a second write of its own.
        """
        if not events:
            return []
        from matrx_graph.checkpoint.value_store import intern_event_payload

        events = [{**ev, "payload": await intern_event_payload(run_id, ev.get("payload") or {})} for ev in events]
        from matrx_orm import F, transaction

        from matrx_graph.db._registry import get_model
        from matrx_graph.db.run_store import update_run
        from matrx_graph.failure import client_safe_error_payload

        run_uuid = UUID(run_id)
        n = len(events)
        async with transaction():
            bump = await update_run(
                {"id": run_uuid},
                returning=("id", "event_seq", "organization_id"),
                **(run_updates or {}),
                event_seq=F("event_seq") + n,
            )
            if not bump.updated_rows:
                raise ValueError(f"insert_events: run '{run_id}' not found in workflow.run")
            last = int(bump.updated_rows[0]["event_seq"])
            organization_id = bump.updated_rows[0].get("organization_id")
            if not organization_id:
                raise ValueError(f"insert_events: run '{run_id}' has no resolvable organization_id")
            rows: list[dict[str, Any]] = []
            seqs = list(range(last - n + 1, last + 1))
            for seq, ev in zip(seqs, events, strict=True):
                checkpoint_id = ev.get("checkpoint_id")
                try:
                    cp_uuid = UUID(checkpoint_id) if checkpoint_id else None
                except (ValueError, TypeError):
                    cp_uuid = None
                error_message = ev.get("error_message")
                rows.append({
                    "run_id": run_uuid,
                    "organization_id": organization_id,
                    "event_type": ev["event_type"],
                    "step": ev.get("step"),
                    "node_id": ev.get("node_id"),
                    "spec_type": ev.get("spec_type"),
                    "attempt": ev.get("attempt"),
                    "duration_ms": ev.get("duration_ms"),
                    "checkpoint_id": cp_uuid,
                    "error_type": ev.get("error_type"),
                    "error_message": client_error_text(error_message) if error_message else error_message,
                    "payload": client_safe_error_payload(ev.get("payload") or {}),
                    "event_ts": ev.get("event_ts") or datetime.now(UTC),
                    "seq": seq,
                })
            # Only ids come back: an event row carries node inputs/outputs, and
            # RETURNING * read every one back, decoded it, and cached it (MKT-111).
            await get_model("WfNodeEvents").bulk_create(
                [{**row, "organization_id": row["organization_id"]} for row in rows],
                returning=["id"],
            )
        return seqs

    # pg_notify payload hard cap is 8000 bytes; keep headroom for the
    # envelope + multi-byte characters after JSON escaping.
    NOTIFY_MAX_BYTES = 7_800

    async def publish_ephemeral(
        self,
        run_id: str,
        event_type: str,
        payload: dict[str, Any],
    ) -> bool:
        """Publish an EPHEMERAL event on the ``wf_event`` NOTIFY channel.

        Companion to the durable path (``insert_event`` + the 0014 trigger):
        the notification reaches the same LISTEN consumers, but nothing is
        written to ``workflow.node_events`` — no ``seq`` is assigned and the
        event is invisible to replay/polling. Use for high-frequency,
        loss-tolerant signals (live LLM token deltas, refetch hints) whose
        durable snapshot lives elsewhere (e.g. the wf_run streaming
        heartbeat).

        Wire contract: durable NOTIFYs carry ``{id, run_id, event_type,
        event_ts}`` and consumers hydrate the row by id; ephemeral NOTIFYs
        carry the full event inline under ``payload`` and no ``id``.

        Returns False (never raises) when the payload exceeds the pg_notify
        8000-byte cap or the publish fails — callers stream best-effort and
        must chunk large deltas themselves.
        """
        envelope = json.dumps(
            {"run_id": run_id, "event_type": event_type, "payload": payload},
            default=str,
        )
        if len(envelope.encode("utf-8")) > self.NOTIFY_MAX_BYTES:
            return False
        try:
            from matrx_orm import call_function

            from matrx_graph.db._registry import get_model

            # pg_notify is a builtin pg_catalog function — the matrx-orm
            # call_function primitive (same one used for a SECURITY DEFINER
            # RPC) covers this exactly: bound args, no table.
            await call_function(
                get_model("WfRun")._database,
                "pg_catalog",
                "pg_notify",
                "wf_event",
                envelope,
                mode="none",
            )
            return True
        except Exception:  # noqa: BLE001 — ephemeral publish is never load-bearing
            import logging

            logging.getLogger(__name__).warning(
                "publish_ephemeral failed (run=%s event=%s) — live stream misses one delta",
                run_id[:8],
                event_type,
                exc_info=True,
            )
            return False

    async def list_events(
        self,
        run_id: str,
        *,
        after_seq: int | None = None,
        event_types: list[str] | None = None,
        limit: int = 1000,
    ) -> list[dict[str, Any]]:
        """Cursor read ordered by ``seq``. ``after_seq`` is exclusive.

        ``limit`` is ALWAYS applied (default 1000) — the unbounded
        full-history fetch was an audit finding (C4); callers wanting more
        page with the cursor.
        """
        from matrx_orm import OrderBy

        from matrx_graph.db._registry import get_model

        filters: dict[str, Any] = {"run_id": str(UUID(run_id))}
        if after_seq is not None:
            filters["seq__gt"] = after_seq
        if event_types:
            filters["event_type__in"] = list(event_types)
        rows = await (
            get_model("WfNodeEvents")
            .filter(**filters)
            .order_by(OrderBy("seq", nulls="first"), "event_ts")
            .limit(limit)
            .values(
                "id",
                "run_id",
                "event_type",
                "step",
                "node_id",
                "spec_type",
                "attempt",
                "duration_ms",
                "checkpoint_id",
                "error_type",
                "error_message",
                "payload",
                "event_ts",
                "seq",
            )
        )
        out: list[dict[str, Any]] = []
        for r in rows:
            payload = r["payload"]
            if isinstance(payload, str):
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError:
                    payload = {"raw": payload}
            from matrx_graph.failure import client_safe_error_payload

            payload = client_safe_error_payload(payload)
            stored_error_message = r["error_message"]
            out.append(
                {
                    "id": str(r["id"]),
                    "run_id": str(r["run_id"]),
                    "event_type": r["event_type"],
                    "step": r["step"],
                    "node_id": r["node_id"],
                    "spec_type": r["spec_type"],
                    "attempt": r["attempt"],
                    "duration_ms": r["duration_ms"],
                    "checkpoint_id": str(r["checkpoint_id"]) if r["checkpoint_id"] else None,
                    "error_type": r["error_type"],
                    "error_message": (
                        client_error_text(stored_error_message)
                        if isinstance(stored_error_message, str)
                        else stored_error_message
                    ),
                    "payload": payload,
                    "event_ts": r["event_ts"],
                    "seq": r["seq"],
                }
            )
        return out
