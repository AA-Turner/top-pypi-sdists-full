"""Durable queue behind kind='event' workflow triggers (workflow.trigger_event).

Rows are written by the DB capture function ``workflow.emit_trigger_events()``
(migration 0111) whenever a watched table changes in a way that matches an
active event trigger. The EventWatcher (``matrx_graph.workers.event_watcher``)
claims due rows here and fires the trigger; the row is the truth, the poll is
the drain — mirrors the CronWatcher posture, so there is no NOTIFY to lose
and no separate reconcile schedule.

Lifecycle: ``pending`` → ``claimed`` (lease-fenced, attempts+1) → ``fired``
(run_id recorded) | back to ``pending`` with backoff on a failed fire |
``dead`` after max_attempts. A claim whose watcher died past the lease is
reclaimed to ``pending`` at the top of the next claim pass.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from matrx_utils import client_error_text

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.db._registry import get_model

RETRY_BACKOFF_BASE_SECONDS = 30
RETRY_BACKOFF_CAP_SECONDS = 600


class TriggerEventRow(BaseModel):
    """Row shape for workflow.trigger_event reads."""

    model_config = ConfigDict(extra="allow")

    id: str
    trigger_id: str
    entity_key: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    claim_at: datetime | None = None
    claimed_at: datetime | None = None
    attempts: int = 0
    max_attempts: int = 5
    run_id: str | None = None
    last_error: str | None = None
    organization_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TriggerEventStore:
    """Claim/settle helpers over workflow.trigger_event."""

    async def claim_due(
        self,
        *,
        now: datetime | None = None,
        limit: int = 50,
        lease_seconds: int = 600,
    ) -> list[TriggerEventRow]:
        """Atomically claim due pending events (FOR UPDATE SKIP LOCKED).

        Reclaims expired claims first (a watcher that died mid-fire releases
        its events after ``lease_seconds``), then claims up to ``limit`` due
        rows, bumping ``attempts`` in the same transaction. Returned rows
        carry the post-claim attempts value.
        """
        now = now or datetime.now(UTC)
        from matrx_orm import F, transaction

        async with transaction():
            await get_model("WfTriggerEvent").update_where(
                {
                    "status": "claimed",
                    "claimed_at__lt": now - timedelta(seconds=lease_seconds),
                },
                status="pending",
                claim_at=now,
                updated_at=now,
            )
            rows = await (
                get_model("WfTriggerEvent")
                .filter(status="pending", claim_at__lte=now)
                .order_by("claim_at")
                .limit(limit)
                .select_for_update(skip_locked=True)
                .values()
            )
            events = [_row_to_event(r) for r in rows]
            for ev in events:
                await get_model("WfTriggerEvent").update_where(
                    {"id": UUID(ev.id)},
                    status="claimed",
                    claimed_at=now,
                    attempts=F("attempts") + 1,
                    updated_at=now,
                )
                ev.status = "claimed"
                ev.claimed_at = now
                ev.attempts += 1
        return events

    async def mark_fired(self, event_id: str, run_id: str) -> None:
        await get_model("WfTriggerEvent").update_where(
            {"id": UUID(event_id)},
            status="fired",
            run_id=str(UUID(run_id)),
            last_error=None,
            updated_at=datetime.now(UTC),
        )

    async def mark_failed(
        self, event_id: str, *, error: str, now: datetime | None = None
    ) -> None:
        """Failed fire: back to pending with exponential backoff, or dead
        once attempts (bumped at claim) reached max_attempts."""
        now = now or datetime.now(UTC)
        rows = await (
            get_model("WfTriggerEvent")
            .filter(id=UUID(event_id))
            .values("attempts", "max_attempts")
        )
        if not rows:
            return
        attempts = int(rows[0]["attempts"] or 0)
        max_attempts = int(rows[0]["max_attempts"] or 5)
        truncated = client_error_text(error, limit=2000)
        if attempts >= max_attempts:
            await get_model("WfTriggerEvent").update_where(
                {"id": UUID(event_id)},
                status="dead",
                last_error=truncated,
                updated_at=now,
            )
            return
        backoff = min(
            RETRY_BACKOFF_BASE_SECONDS * (2 ** max(attempts - 1, 0)),
            RETRY_BACKOFF_CAP_SECONDS,
        )
        await get_model("WfTriggerEvent").update_where(
            {"id": UUID(event_id)},
            status="pending",
            claim_at=now + timedelta(seconds=backoff),
            last_error=truncated,
            updated_at=now,
        )

    async def mark_dead(self, event_id: str, *, error: str) -> None:
        """Terminal without retry — e.g. the parent trigger vanished."""
        await get_model("WfTriggerEvent").update_where(
            {"id": UUID(event_id)},
            status="dead",
            last_error=client_error_text(error, limit=2000),
            updated_at=datetime.now(UTC),
        )

    async def enqueue_store_change(
        self, *, trigger_id: str, organization_id: str, change_id: str
    ) -> bool:
        """Queue one store change for one store trigger (lane 11 round 6). Server-side only:
        the host's record-changes subscriber calls it; the EventWatcher fires it, re-reading
        the outbox row as the proof. The payload is the change id alone.

        Idempotent per (trigger, change): a change delivered again (a handed-back page) is not
        queued twice. Returns True when a row was written."""
        model = get_model("WfTriggerEvent")
        existing = await model.filter(trigger_id=UUID(trigger_id), entity_key=str(change_id)).values("id")
        if existing:
            return False
        now = datetime.now(UTC)
        await model.create(
            id=str(uuid4()),
            trigger_id=str(UUID(trigger_id)),
            entity_key=str(change_id),
            payload={"change_id": str(change_id)},
            status="pending",
            claim_at=now,
            organization_id=str(UUID(organization_id)),
        )
        return True

    async def list_for_trigger(
        self, trigger_id: str, *, limit: int = 100
    ) -> list[TriggerEventRow]:
        rows = await (
            get_model("WfTriggerEvent")
            .filter(trigger_id=UUID(trigger_id))
            .order_by("-created_at")
            .limit(limit)
            .values()
        )
        return [_row_to_event(r) for r in rows]


def _refuse_store_payload(where: str) -> None:
    """A store trigger's run is NEVER built from an event payload (lane 11 round 3/4):
    ``authenticated`` may INSERT ``workflow.trigger_event`` rows, payload included."""
    from matrx_graph.db.store_change import StoreChangeRefused

    raise StoreChangeRefused(
        f"{where}: a store trigger's run is never built from an event payload — a trigger "
        "editor can insert that payload. Fire it through the host's verified store fire "
        "(aidream: services/runtime/store_triggers.fire_store_event, on "
        "matrx_graph.db.store_change.verified_store_change), which builds the run from the "
        "store's custom.io_outbox row."
    )


def build_event_inputs(
    *,
    default_inputs: dict[str, Any] | None,
    event_source: dict[str, Any] | None,
    event: TriggerEventRow,
) -> dict[str, Any]:
    """Run inputs for an event fire: default_inputs, then input_map-resolved
    row columns, then — only when the spec opts in via ``include_event`` —
    the full event envelope under the reserved key ``event``. The envelope
    is opt-in because trigger inputs are broadcast to entry nodes
    unfiltered, and an uninvited extra key breaks any strict
    (extra="forbid") entry-node input schema."""
    inputs: dict[str, Any] = dict(default_inputs or {})
    payload = event.payload or {}
    source = event_source or {}
    if source.get("source") == "store":
        _refuse_store_payload("build_event_inputs")
    row = payload.get("row") or {}
    input_map = source.get("input_map") or {}
    for input_name, column in input_map.items():
        if isinstance(column, str) and column in row:
            inputs[input_name] = row[column]
    if source.get("include_event"):
        inputs["event"] = {
            "table": payload.get("table"),
            "operation": payload.get("operation"),
            # The RAW key. Under organization_scope 'any' the queued row's
            # entity_key is '<org>:<key>' (so pending rows of two tenants never
            # coalesce) while payload.entity_key stays the key itself; a hand
            # fire builds its event from the raw key too. One meaning on the
            # wire: the row's key, never the queue's dedupe handle.
            "entity_key": payload.get("entity_key") or event.entity_key,
            "row": row,
        }
    return inputs


ROW_ACTOR_COLUMNS = ("updated_by", "created_by")


def event_row_actor(
    *, event_source: dict[str, Any] | None, event: TriggerEventRow
) -> str | None:
    """The party a raw-table event SERVES: the user who made the captured change
    (the watched row's ``updated_by``, else ``created_by``, as captured by
    ``workflow.emit_trigger_events``). A host fires the run AS that party — the
    automation-model rule: work for a person runs as, and bills, that person,
    never the trigger's owner. None when the row names no actor (a service
    write, an import) or for a store source, whose change carries its own
    verified actor."""
    source = event_source or {}
    if source.get("source") == "store":
        return None
    row = (event.payload or {}).get("row") or {}
    for column in ROW_ACTOR_COLUMNS:
        text = str(row.get(column) or "").strip()
        if text and text.lower() not in {"none", "null"}:
            return text
    return None


STORE_CHANGE_KEYS = (
    "change_id",
    "record_id",
    "table_id",
    "operation",
    "changed_field_ids",
    "new_version",
    "chain",
)


def store_change_of(payload: dict[str, Any], *, entity_key: str | None = None) -> dict[str, Any]:
    """The store emitter's change payload, exactly its documented keys.

    ``change_id`` falls back to the event's ``entity_key`` — for a store trigger that IS
    the outbox id (one pending row per change, §0.2)."""
    change = {key: payload.get(key) for key in STORE_CHANGE_KEYS}
    if not change["change_id"] and entity_key:
        change["change_id"] = entity_key
    if change["changed_field_ids"] is None:
        change["changed_field_ids"] = []
    return change


def event_run_metadata(
    *, event_source: dict[str, Any] | None, event: TriggerEventRow
) -> dict[str, Any]:
    """Extra ``workflow.run.metadata`` for an event-fired run.

    A store change stamps ``{record_id, change_id, chain}`` (beside the host's
    ``trigger_id``) so "what ran on this record" is ``metadata->>'record_id' = <id>``.
    A raw-table event adds nothing."""
    if (event_source or {}).get("source") != "store":
        return {}
    _refuse_store_payload("event_run_metadata")


def _coerce_json(value: Any) -> Any:
    if value is None or not isinstance(value, str):
        return value
    import json

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _row_to_event(row: Any) -> TriggerEventRow:
    return TriggerEventRow(
        id=str(row["id"]),
        trigger_id=str(row["trigger_id"]),
        entity_key=row["entity_key"],
        payload=_coerce_json(row["payload"]) or {},
        status=row["status"],
        claim_at=row["claim_at"],
        claimed_at=row["claimed_at"],
        attempts=row["attempts"],
        max_attempts=row["max_attempts"],
        run_id=str(row["run_id"]) if row["run_id"] else None,
        last_error=(
            client_error_text(row["last_error"], limit=2000)
            if isinstance(row["last_error"], str)
            else row["last_error"]
        ),
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )
