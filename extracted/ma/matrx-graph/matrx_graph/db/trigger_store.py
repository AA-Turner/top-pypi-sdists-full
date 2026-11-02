"""CRUD + scheduling over workflow.trigger.

Everything — including the cron claim — goes through the host-injected
matrx-orm models (``configure_db`` + ``db_requirements``): the claim rides
matrx-orm's ``transaction()`` ContextVar so the ``FOR UPDATE SKIP LOCKED``
SELECT and the per-row ``next_run_at`` advance share one connection/
transaction, same as a hand-written claim transaction would.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    JsonValue,
    Tag,
    TypeAdapter,
    model_validator,
)

from matrx_graph.db._registry import get_model

TriggerKind = Literal["cron", "webhook", "manual", "event"]
#: A table event source's tenant fence (``TableEventSource.organization_scope``).
OrganizationScope = Literal["own", "any"]

_TABLE_PATTERN = r"^[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*$"


class TableEventSource(BaseModel):
    """kind='event' config, ``source='table'`` arm — a raw-table data change.

    Matching happens in the DB capture function (workflow.emit_trigger_events,
    migration 0111): a write on the watched ``table`` with the matching
    ``operation`` — and, when ``when_column`` is set, a TRANSITION into
    ``when_value`` — enqueues a durable workflow.trigger_event row. A table
    only produces events after ``workflow.watch_table(...)`` attached the
    capture trigger.

    ``when_from_value`` (UPDATE only, needs ``when_column``/``when_value``) narrows the
    transition to ONE hop: the old value must equal it — ``analysis -> research`` and
    ``review -> research`` are two triggers on the same column.

    ``organization_scope`` is the tenant fence. ``"own"`` (default): only rows whose
    organization_id equals the trigger's fire it. ``"any"``: one trigger serves every
    organization's rows — honored by the capture function ONLY for a trigger filed in the
    platform's system organization (``iam.system_orgs`` key ``system``); anywhere else it
    falls back to ``"own"``. The queued event keeps the ROW's organization, and the host
    creates the run there (:func:`event_run_organization_id`). A row with no organization
    never fires under either scope.

    ``input_map`` maps run input names to columns of the watched row; the
    full event also rides the run inputs under the reserved key ``event``.
    ``debounce_seconds`` is the settle window: while an event for the same
    entity is still pending, a newer change replaces it and pushes the fire
    time forward instead of firing once per write.
    """

    model_config = ConfigDict(extra="forbid")

    source: Literal["table"] = "table"
    table: str = Field(pattern=_TABLE_PATTERN, description="Schema-qualified watched table.")
    operation: Literal["insert", "update"] = "insert"
    when_column: str | None = None
    when_value: str | None = None
    # Only the hop FROM this value (OLD.<when_column>); UPDATE only. Absent = any prior value.
    when_from_value: str | None = None
    entity_key_column: str = "id"
    debounce_seconds: int = Field(default=0, ge=0, le=86_400)
    input_map: dict[str, str] = Field(default_factory=dict)
    # Opt-in: also pass the full event envelope as run input ``event``.
    # OFF by default — trigger inputs are broadcast to entry nodes
    # unfiltered, so an uninvited extra key breaks any strict
    # (extra="forbid") entry-node input schema.
    include_event: bool = False
    # Tenant fence: "own" = the trigger's organization's rows only; "any" = every
    # organization's rows (system-organization triggers only — see the class docstring).
    organization_scope: OrganizationScope = "own"

    @model_validator(mode="after")
    def _when_pair(self) -> TableEventSource:
        if (self.when_column is None) != (self.when_value is None):
            raise ValueError("when_column and when_value must be set together")
        if self.when_from_value is not None:
            if self.when_column is None:
                raise ValueError("when_from_value needs when_column and when_value")
            if self.operation != "update":
                raise ValueError("when_from_value only applies to operation='update'")
            if self.when_from_value == self.when_value:
                raise ValueError(
                    "when_from_value equals when_value — that hop is not a transition "
                    "and would never fire"
                )
        return self


#: Keys added to the table arm after rows were stored. ``event_source_json`` leaves each
#: out while it holds its default, so a spec that does not use them stores the exact JSON
#: it stored before they existed.
_TABLE_KEYS_OMITTED_AT_DEFAULT: dict[str, Any] = {
    "when_from_value": None,
    "organization_scope": "own",
}


StoreEvent = Literal[
    "record.created", "record.updated", "record.archived", "record.matches",
    # A created record that came through that door (``metadata.change.via``, chairdoors4_b).
    "form.answered", "booking.made",
]
#: The outbox's change words (``custom.io_outbox.operation``); an archive is ``deleted``.
StoreOperation = Literal["created", "updated", "deleted"]
#: The door words a change carries as ``metadata.change.via`` (chairdoors4_b).
StoreVia = Literal["form", "booking", "import", "agent", "api", "person"]


class StoreEventSource(BaseModel):
    """kind='event' config, ``source='store'`` arm — a change to a record of a custom Table.

    Matched by the store's emitter (an AFTER INSERT trigger on ``custom.io_outbox``, the
    chair's), which writes one ``workflow.trigger_event`` per change with
    ``entity_key = <outbox id>`` and a payload of ids only: ``{change_id, record_id,
    table_id, operation, changed_field_ids, new_version, chain}``. That payload rides the
    run as the input ``trigger`` (``build_event_inputs``).

    It never matches the raw-table emitter ``workflow.emit_trigger_events``, which selects
    on ``event_source->>'table'`` — this arm has no ``table`` key at all (WF-026).
    """

    model_config = ConfigDict(extra="forbid")

    source: Literal["store"]
    event: StoreEvent
    table_id: UUID
    operations: list[StoreOperation] = Field(default_factory=list)
    field_ids: list[UUID] = Field(default_factory=list)
    # Only changes that came through these doors (``metadata.change.via``); empty = any door.
    # form.answered and booking.made imply their own door whatever this says.
    via: list[StoreVia] = Field(default_factory=list)
    # A Rule expression (custom.rule_eval shape); for record.matches, the truth entered.
    to: dict[str, JsonValue] | None = None
    # Off by default: two quick edits are two runs (one pending row per change).
    debounce_per_record: bool = False
    # SERVER-SET at bind time (create / turn on): the compiled-graph hash of the bound published
    # version. Never trusted from a request — the endpoints overwrite it.
    bound_graph_hash: str | None = None


def _event_source_arm(value: Any) -> str:
    """The discriminator. A spec with no ``source`` is the table arm, so every row and
    caller from before the store arm keeps validating unchanged."""
    if isinstance(value, dict):
        return str(value.get("source") or "table")
    return str(getattr(value, "source", None) or "table")


EventSourceSpec = Annotated[
    Annotated[TableEventSource, Tag("table")] | Annotated[StoreEventSource, Tag("store")],
    Discriminator(_event_source_arm),
]
"""kind='event' config: what change fires this trigger — ``source: 'table' | 'store'``."""

_EVENT_SOURCE = TypeAdapter(EventSourceSpec)


def validate_event_source(value: Any) -> TableEventSource | StoreEventSource:
    """Validate a stored/requested event_source into its arm (default arm: table)."""
    return _EVENT_SOURCE.validate_python(value)


def event_source_json(value: Any) -> dict[str, Any]:
    """The JSONB shape stored on workflow.trigger.event_source for a validated spec."""
    spec = validate_event_source(value)
    dumped = spec.model_dump(mode="json")
    if isinstance(spec, TableEventSource):
        for key, default in _TABLE_KEYS_OMITTED_AT_DEFAULT.items():
            if dumped.get(key) == default:
                dumped.pop(key, None)
    return dumped


def event_scope_is_any(event_source: dict[str, Any] | None) -> bool:
    """True when a stored table event source opted into ``organization_scope: "any"``."""
    source = event_source or {}
    return source.get("source", "table") == "table" and source.get("organization_scope") == "any"


def event_run_organization_id(
    *,
    event_source: dict[str, Any] | None,
    event_organization_id: str | None,
    trigger_organization_id: str | None,
) -> str | None:
    """The organization an event-fired run is created in.

    ``"own"`` scope (and every store trigger): the trigger's organization — the row's is
    the same by the capture function's fence. ``"any"`` scope: the ROW's organization, as
    the capture function wrote it onto the queued ``workflow.trigger_event``; a run for
    tenant B's row never lands in the system organization. An ``"any"`` event with no
    organization raises: the capture function never writes one, so it is a corrupt row.
    """
    if not event_scope_is_any(event_source):
        return trigger_organization_id
    if not event_organization_id:
        raise ValueError(
            "organization_scope='any' event carries no organization_id — refusing to run it "
            "in the trigger's organization"
        )
    return str(event_organization_id)


class TriggerRow(BaseModel):
    """Row shape for workflow.trigger CRUD responses."""

    model_config = ConfigDict(extra="allow")

    id: str
    definition_id: str
    definition_version_id: str | None = None
    name: str
    description: str | None = None
    kind: TriggerKind
    cron_expression: str | None = None
    timezone: str = "UTC"
    webhook_secret: str | None = None
    # kind='event' only — validated EventSourceSpec shape (stored as JSONB).
    event_source: dict[str, Any] | None = None
    default_inputs: dict[str, Any] = Field(default_factory=dict)
    max_steps: int = 1000
    # Terminal-completion callback: runs fired by this trigger carry the URL
    # in wf_run.metadata._settings.callback_url and receive a summary POST
    # when they settle (host-side delivery — see aidream run_callbacks).
    callback_url: str | None = None
    is_active: bool = True
    last_fired_at: datetime | None = None
    last_run_id: str | None = None
    next_run_at: datetime | None = None
    fire_count: int = 0
    created_by: str | None = None
    organization_id: str | None = None
    project_id: str | None = None
    task_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TriggerStore:
    """CRUD + scheduling helpers over workflow.trigger."""

    async def create(
        self,
        *,
        definition_id: str,
        name: str,
        kind: TriggerKind,
        cron_expression: str | None = None,
        timezone: str = "UTC",
        webhook_secret: str | None = None,
        event_source: dict[str, Any] | None = None,
        default_inputs: dict[str, Any] | None = None,
        max_steps: int = 1000,
        description: str | None = None,
        definition_version_id: str | None = None,
        callback_url: str | None = None,
        user_id: str | None = None,
        organization_id: str | None = None,
        project_id: str | None = None,
        task_id: str | None = None,
    ) -> TriggerRow:
        trigger_id = str(uuid4())
        next_run_at: datetime | None = None
        if kind == "cron" and cron_expression:
            next_run_at = _compute_next_run(cron_expression, timezone, base=None)
        if kind == "event":
            # Same posture as the cron-expression check: a malformed spec is a
            # ValueError at the store boundary, never a stored row the capture
            # function silently skips.
            try:
                event_source = event_source_json(event_source or {})
            except Exception as e:
                raise ValueError(f"invalid event_source: {e}") from e
        elif event_source is not None:
            raise ValueError("event_source is only valid on kind='event' triggers")

        instance = await get_model("WfTrigger").create(
            id=trigger_id,
            definition_id=str(UUID(definition_id)),
            definition_version_id=_to_uuid(definition_version_id),
            name=name,
            description=description,
            kind=kind,
            cron_expression=cron_expression,
            timezone=timezone,
            webhook_secret=webhook_secret,
            event_source=event_source,
            default_inputs=default_inputs or {},
            max_steps=max_steps,
            callback_url=callback_url,
            is_active=True,
            next_run_at=next_run_at,
            created_by=_to_uuid(user_id),
            organization_id=_to_uuid(organization_id),
            project_id=_to_uuid(project_id),
            task_id=_to_uuid(task_id),
        )
        return _row_to_trigger(_instance_to_mapping(instance))

    async def load(self, trigger_id: str) -> TriggerRow | None:
        coerced = _to_uuid(trigger_id)
        if coerced is None:
            return None
        rows = await get_model("WfTrigger").filter(id=coerced, deleted_at__isnull=True).values()
        return _row_to_trigger(rows[0]) if rows else None

    async def list_for_user(
        self,
        *,
        user_id: str | None = None,
        organization_id: str | None = None,
        definition_id: str | None = None,
        kind: TriggerKind | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TriggerRow]:
        filters: dict[str, Any] = {}
        for field, raw_value in (
            ("created_by", user_id),
            ("organization_id", organization_id),
            ("definition_id", definition_id),
        ):
            if raw_value:
                coerced = _to_uuid(raw_value)
                if coerced is None:
                    # Provided-but-invalid UUID matched nothing in the raw SQL
                    # (`col = NULL`); an ORM `IS NULL` filter would leak
                    # ownerless rows instead. Preserve "matches nothing".
                    return []
                filters[field] = coerced
        if kind:
            filters["kind"] = kind
        filters["deleted_at__isnull"] = True

        rows = await (
            get_model("WfTrigger")
            .filter(**filters)
            .order_by("-created_at")
            .limit(limit)
            .offset(offset)
            .values()
        )
        return [_row_to_trigger(r) for r in rows]

    async def set_active(self, trigger_id: str, active: bool) -> None:
        await get_model("WfTrigger").update_where(
            {"id": _to_uuid(trigger_id), "deleted_at__isnull": True}, is_active=active
        )

    async def bind_version(
        self, trigger_id: str, definition_version_id: str, graph_hash: str
    ) -> None:
        """Bind the published version a store trigger fires AND the compiled-graph hash it had
        when bound (server-only: workflow.trigger is not client-writable). The fire refuses a
        version whose content no longer compiles to this hash (lane 11 rounds 6-7, B2)."""
        from matrx_orm import JsonbMerge

        await get_model("WfTrigger").update_where(
            {"id": _to_uuid(trigger_id), "deleted_at__isnull": True},
            definition_version_id=_to_uuid(definition_version_id),
            event_source=JsonbMerge("event_source", {"bound_graph_hash": str(graph_hash)}),
        )

    async def delete(self, trigger_id: str) -> None:
        """Canonical SOFT delete — the row survives for audit/undelete but
        disappears from every store read and from cron claiming (all filter
        ``deleted_at IS NULL``). Deactivated in the same write so no scheduler
        path can treat it as live. Was a hard ``delete_where`` until 2026-08-10."""
        coerced = _to_uuid(trigger_id)
        if coerced is None:
            return
        await get_model("WfTrigger").update_where(
            {"id": coerced, "deleted_at__isnull": True},
            deleted_at=datetime.now(UTC),
            is_active=False,
        )

    # -- Scheduling -------------------------------------------------------

    async def claim_due(self, *, now: datetime | None = None, limit: int = 100) -> list[TriggerRow]:
        """Atomically claim due cron triggers by advancing their next_run_at.

        Returns the rows BEFORE advancement so the caller knows what to
        enqueue. FOR UPDATE SKIP LOCKED ensures two watchers can run
        concurrently without double-firing.
        """
        now = now or datetime.now(UTC)
        from matrx_orm import transaction

        # FOR UPDATE SKIP LOCKED claim: two watchers must never double-fire
        # the same trigger. matrx-orm's transaction() binds every ORM call
        # inside this block to ONE connection via a ContextVar, so the
        # row-lock SELECT and the per-row next_run_at UPDATE ride the same
        # transaction/connection exactly like a hand-written claim would —
        # the row lock from select_for_update(skip_locked=True) is held
        # until this block commits, serializing concurrent claims.
        async with transaction():
            rows = await (
                get_model("WfTrigger")
                .filter(
                    is_active=True,
                    kind="cron",
                    deleted_at__isnull=True,
                    next_run_at__isnull=False,
                    next_run_at__lte=now,
                )
                .order_by("next_run_at")
                .limit(limit)
                .select_for_update(skip_locked=True)
                .values()
            )
            due = [_row_to_trigger(r) for r in rows]
            for trig in due:
                assert trig.cron_expression is not None
                upcoming = _compute_next_run(trig.cron_expression, trig.timezone, base=now)
                await get_model("WfTrigger").update_where(
                    {"id": UUID(trig.id)}, next_run_at=upcoming
                )
        return due

    async def record_fire(
        self, trigger_id: str, run_id: str, *, fired_at: datetime | None = None
    ) -> None:
        """Bump fire_count, set last_fired_at + last_run_id. Doesn't touch
        next_run_at (claim_due already advanced it)."""
        from matrx_orm import F

        fired_at = fired_at or datetime.now(UTC)
        await get_model("WfTrigger").update_where(
            {"id": str(UUID(trigger_id))},
            fire_count=F("fire_count") + 1,
            last_fired_at=fired_at,
            last_run_id=str(UUID(run_id)),
        )


def _compute_next_run(cron_expression: str, timezone: str, base: datetime | None) -> datetime:
    """Compute the next fire time for a cron expression, honoring timezone.

    Uses croniter — handles 5-field (minute/hour/dom/month/dow) and 6-field
    (with seconds) expressions. Raises ValueError on malformed expressions.
    """
    from zoneinfo import ZoneInfo

    from croniter import croniter

    try:
        zone = ZoneInfo(timezone)
    except Exception as e:
        raise ValueError(f"Unknown timezone '{timezone}'") from e

    base = base or datetime.now(UTC)
    # croniter needs a naive datetime in the trigger's timezone; we return UTC.
    local_base = base.astimezone(zone).replace(tzinfo=None)
    it = croniter(cron_expression, local_base)
    local_next = it.get_next(datetime)
    return local_next.replace(tzinfo=zone).astimezone(UTC)


def _to_uuid(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return str(UUID(str(value)))
    except (ValueError, AttributeError, TypeError):
        return None


def _instance_to_mapping(instance: Any) -> dict[str, Any]:
    """Flatten a hydrated model instance into the plain column mapping
    ``_row_to_trigger`` consumes (same keys an asyncpg Record carried)."""
    return {name: getattr(instance, name) for name in type(instance)._fields}


def _row_to_trigger(row: Any) -> TriggerRow:
    def _coerce(v: Any) -> Any:
        if v is None or not isinstance(v, str):
            return v
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            return v

    return TriggerRow(
        id=str(row["id"]),
        definition_id=str(row["definition_id"]),
        definition_version_id=str(row["definition_version_id"])
        if row["definition_version_id"]
        else None,
        name=row["name"],
        description=row["description"],
        kind=row["kind"],
        cron_expression=row["cron_expression"],
        timezone=row["timezone"],
        webhook_secret=row["webhook_secret"],
        # Guarded like callback_url: standalone hosts on an older baseline may
        # not carry the column yet.
        event_source=(_coerce(row["event_source"]) if "event_source" in dict(row) else None),
        default_inputs=_coerce(row["default_inputs"]) or {},
        max_steps=row["max_steps"],
        callback_url=row["callback_url"] if "callback_url" in dict(row) else None,
        is_active=row["is_active"],
        last_fired_at=row["last_fired_at"],
        last_run_id=str(row["last_run_id"]) if row["last_run_id"] else None,
        next_run_at=row["next_run_at"],
        fire_count=row["fire_count"],
        created_by=str(row["created_by"]) if row["created_by"] else None,
        organization_id=str(row["organization_id"]) if row["organization_id"] else None,
        project_id=str(row["project_id"]) if row["project_id"] else None,
        task_id=str(row["task_id"]) if row["task_id"] else None,
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )
