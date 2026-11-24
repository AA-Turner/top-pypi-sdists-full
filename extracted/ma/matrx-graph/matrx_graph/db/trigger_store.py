"""CRUD over workflow.trigger, through the host-injected matrx-orm models
(``configure_db`` + ``db_requirements``).

A cron trigger's CLOCK is not here: this store validates its expression and
the host schedules it (aidream: one person-owned ``sch_task`` per trigger).
There is no cron claim and ``next_run_at`` is never written for a cron row.
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

# "schedule": the cadence is the host scheduler's own trigger (interval, one-shot, cron) and that scheduler is its clock.
TriggerKind = Literal["cron", "webhook", "manual", "event", "schedule"]
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


OfficeEvent = Literal["sheet.range_changed", "document.saved", "live_table.record_changed"]
#: The store event a ``live_table.record_changed`` source becomes (the tab's table, any record change).
LIVE_TABLE_STORE_EVENT = "record.updated"


class OfficeEventSource(BaseModel):
    """kind='event' config, ``source='office'`` arm — a change to a workbook or a document (office W11).

    ``sheet.range_changed``: the cells of ``range`` on ``sheet`` of the workbook ``record_id`` changed.
    ``document.saved``: the document ``record_id`` changed (a save, or edits in its co-editing room).
    ``live_table.record_changed``: a record of the table a workbook's live table tab shows changed — the
    host rewrites it into the ``store`` arm on that tab's table when the trigger is created, so it IS a
    store trigger (one trigger system, one record-change feed).

    Matched by the DB capture function ``workflow.emit_office_trigger_events`` (a new snapshot row, or a
    room op of the record), which queues ONE pending ``workflow.trigger_event`` per (trigger, record):
    a newer change while it is pending pushes the fire time forward — the settle window
    ``debounce_seconds``, or the knob ``office.trigger_debounce_seconds`` when unset. The payload is
    ids only and never trusted: the host's fire re-reads the record as the trigger's owner and runs
    only when the watched content's fingerprint moved.

    ``fingerprint`` is SERVER-SET (the content's hash when the trigger was created or last fired);
    a request carrying it is refused, like ``bound_graph_hash``.
    """

    model_config = ConfigDict(extra="forbid")

    source: Literal["office"]
    event: OfficeEvent
    record_id: UUID = Field(description="The workbook (sheet.range_changed, live_table.record_changed) or document.")
    sheet: str | None = Field(default=None, description="Sheet name or id; for a live table, the tab's id or label.")
    range: str | None = Field(default=None, description="A1 range watched (sheet.range_changed), e.g. B2:D20.")
    debounce_seconds: int | None = Field(default=None, ge=0, le=86_400)
    fingerprint: str | None = None

    @model_validator(mode="after")
    def _what_it_watches(self) -> OfficeEventSource:
        if self.event == "sheet.range_changed" and not (self.range or "").strip():
            raise ValueError("sheet.range_changed needs the A1 range it watches (range)")
        if self.event == "live_table.record_changed" and not (self.sheet or "").strip():
            raise ValueError("live_table.record_changed needs the live table tab (sheet: its id or label)")
        if self.event == "document.saved" and (self.sheet or self.range):
            raise ValueError("document.saved watches the whole document; sheet and range do not apply")
        return self


class AppEventSource(BaseModel):
    """kind='event' config, ``source='app'`` arm — an outside event arrived through the host's one
    event intake (Triggers Phase 5): a connected app's push, or a provider delivery.

    ``app`` and ``event`` are OPAQUE strings here; the host validates its closed lists at create.
    ``account`` is the provider account the event belongs to (the intake's ``external_account_key``,
    e.g. a Stripe account id or a Slack team id) — REQUIRED, so a trigger never hears another
    tenant's account. ``connection_id`` names the host connection the account came from (the host
    checks the bound person still owns it at fire). ``filter``: the event payload must CONTAIN it
    (JSON containment, ``payload @> filter``).

    Matched by the DB intake function ``workflow.ingest_app_event``, which stores the event ONCE and
    queues one ``workflow.trigger_event`` per matching trigger exactly once (entity_key
    ``source:account:event_id``). The payload is ids only and never trusted: the host's fire re-reads
    the stored event.
    """

    model_config = ConfigDict(extra="forbid")

    source: Literal["app"]
    app: str = Field(min_length=1, max_length=64)
    event: str = Field(min_length=1, max_length=128)
    account: str = Field(min_length=1, max_length=255)
    connection_id: UUID | None = None
    filter: dict[str, Any] | None = None
    #: A first-party app (the host's own events, e.g. its mail): no connection exists; ``account`` IS the
    #: trigger's organization and the intake matches only that organization (migration 0133). Set by the
    #: host at create from its closed list of first-party apps — never trusted from a caller.
    first_party: bool = False


def _event_source_arm(value: Any) -> str:
    """The discriminator. A spec with no ``source`` is the table arm, so every row and
    caller from before the store arm keeps validating unchanged."""
    if isinstance(value, dict):
        return str(value.get("source") or "table")
    return str(getattr(value, "source", None) or "table")


EventSourceSpec = Annotated[
    Annotated[TableEventSource, Tag("table")]
    | Annotated[StoreEventSource, Tag("store")]
    | Annotated[OfficeEventSource, Tag("office")]
    | Annotated[AppEventSource, Tag("app")],
    Discriminator(_event_source_arm),
]
"""kind='event' config: what fires this trigger — ``source: 'table' | 'store' | 'office' | 'app'``."""

_EVENT_SOURCE = TypeAdapter(EventSourceSpec)


def validate_event_source(
    value: Any,
) -> TableEventSource | StoreEventSource | OfficeEventSource | AppEventSource:
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


#: ``link_kind`` of a fire that started a workflow run (``link_id`` = the run id).
LINK_WORKFLOW_RUN = "workflow_run"
#: ``link_kind`` of an Action fire whose apply gate put the call in front of a person
#: (``link_id`` = the approval id): nothing ran yet, the fire is waiting on a person.
LINK_APPROVAL = "approval"


class FireOutcome(BaseModel):
    """What one trigger fire produced — the host's fire returns it, the stores record it.

    A workflow target: ``run_id`` + ``link_kind='workflow_run'``. An Action target
    (``workflow.trigger.target_action``): ``action`` + whatever the Action produced —
    ``link_kind``/``link_id`` name its record, its operation, or the approval it waits on
    (``LINK_APPROVAL``); ``run_id`` stays None. The package never runs an Action: the
    host's injected fire does (``matrx_graph.actions`` is never imported here).
    """

    model_config = ConfigDict(extra="forbid")

    run_id: str | None = None
    action: str | None = None
    link_kind: str | None = None
    link_id: str | None = None
    #: True when the fire is waiting on a person (an Action the apply gate queued).
    waiting_on_person: bool = False
    #: True when the fire started NOTHING (the target said a run is already in progress): the fire
    #: history still says so, but the trigger's fire_count / last_fired_at are never bumped for it
    #: (``record_outcome``).
    skipped: bool = False

    @classmethod
    def for_run(cls, run_id: str) -> FireOutcome:
        return cls(run_id=str(run_id), link_kind=LINK_WORKFLOW_RUN, link_id=str(run_id))


class TriggerFireRefused(Exception):  # noqa: N818 — the name says what the watcher reads
    """A fire that must never be retried: the watcher dead-letters its event with this sentence
    and nothing runs (the actor lost the organization, the trigger needs reconnecting, the
    target refuses for good). A transient failure raises anything else and is retried."""


class TriggerFireHeld(Exception):  # noqa: N818 — the name says what the watcher reads
    """A fire HELD, not failed: the trigger may fire again after ``retry_after_seconds`` (the host's
    per-trigger rate limit). The watcher releases the event to pending at that time without
    spending an attempt, never dead-letters it and never records it as an error."""

    def __init__(self, message: str, *, retry_after_seconds: float) -> None:
        super().__init__(message)
        self.retry_after_seconds = max(float(retry_after_seconds), 0.0)


#: The prefix of a workflow's generated Action name (``workflow.<key>`` / ``workflow.id_<hex>``).
WORKFLOW_ACTION_PREFIX = "workflow."


def fires_an_action(trigger: Any) -> bool:
    """True when a trigger's fire runs its ``target_action`` rather than its workflow.

    A ``workflow.<key>`` target is still a workflow target: it keeps its definition, its
    published-version pin and the bound-graph proof (Triggers PLAN Rule 1)."""
    target = getattr(trigger, "target_action", None)
    return bool(target) and not str(target).startswith(WORKFLOW_ACTION_PREFIX)


class TriggerRow(BaseModel):
    """Row shape for workflow.trigger CRUD responses."""

    model_config = ConfigDict(extra="allow")

    id: str
    # None only for an Action target (``target_action``); the DB CHECK keeps it for workflows.
    definition_id: str | None = None
    definition_version_id: str | None = None
    # The registered Action a fire runs (an opaque registry name here — the host validates it).
    target_action: str | None = None
    # The Action's static input; the event's own inputs merge over it (host-side).
    target_input: dict[str, Any] = Field(default_factory=dict)
    # A sentence while the bound actor lost the organization / connection a fire needs.
    needs_reconnect: str | None = None
    # The row's free-form jsonb (``created_via='person'`` marks a trigger a signed-in person made).
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _a_workflow_target_names_its_workflow(self) -> TriggerRow:
        # The row-shape twin of the DB CHECK wf_trigger_workflow_target_has_definition (0123).
        if self.definition_id is None and not fires_an_action(self):
            raise ValueError("a workflow trigger names its workflow (definition_id)")
        return self
    name: str
    description: str | None = None
    kind: TriggerKind
    cron_expression: str | None = None
    timezone: str = "UTC"
    webhook_secret: str | None = None
    # kind='webhook' only (0125): how the door verifies a delivery; None = the matrx header. Opaque here.
    signature_scheme: str | None = None
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
    # The row's revision (the host's canonical ``version`` column, bumped on every write): an editor sends
    # back the one it loaded and ``update_fields(expected_version=)`` refuses a stale save. None on a
    # standalone baseline without the column.
    version: int | None = None


class TriggerStore:
    """CRUD + scheduling helpers over workflow.trigger."""

    async def create(
        self,
        *,
        definition_id: str | None,
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
        target_action: str | None = None,
        target_input: dict[str, Any] | None = None,
        signature_scheme: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> TriggerRow:
        trigger_id = str(uuid4())
        target_action = (target_action or "").strip() or None
        if definition_id is None and (
            target_action is None or target_action.startswith(WORKFLOW_ACTION_PREFIX)
        ):
            # The same rule as the DB CHECK (wf_trigger_workflow_target_has_definition), said here.
            raise ValueError(
                "a trigger names the workflow it runs (definition_id) unless it targets an Action "
                "(target_action, not a workflow.* name)"
            )
        if kind == "cron" and cron_expression:
            # Validates the expression + timezone (ValueError at the store boundary). The
            # clock itself is the HOST's scheduler, never this row: next_run_at stays empty.
            _compute_next_run(cron_expression, timezone, base=None)
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
        signature_scheme = (signature_scheme or "").strip() or None
        if signature_scheme is not None and kind != "webhook":
            raise ValueError("signature_scheme is only valid on kind='webhook' triggers")

        instance = await get_model("WfTrigger").create(
            id=trigger_id,
            definition_id=str(UUID(definition_id)) if definition_id is not None else None,
            target_action=target_action,
            target_input=dict(target_input or {}),
            definition_version_id=_to_uuid(definition_version_id),
            name=name,
            description=description,
            kind=kind,
            cron_expression=cron_expression,
            timezone=timezone,
            webhook_secret=webhook_secret,
            signature_scheme=signature_scheme,
            event_source=event_source,
            default_inputs=default_inputs or {},
            max_steps=max_steps,
            callback_url=callback_url,
            is_active=True,
            next_run_at=None,
            created_by=_to_uuid(user_id),
            organization_id=_to_uuid(organization_id),
            project_id=_to_uuid(project_id),
            task_id=_to_uuid(task_id),
            **({"metadata": dict(metadata)} if metadata else {}),
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
        target_action: str | None = None,
        ids: list[str] | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[TriggerRow]:
        """Live triggers matching every filter given. ``ids`` = only these rows (the host's canonical
        reachable set — the store decides no access itself); an empty list matches nothing."""
        filters: dict[str, Any] = {}
        if ids is not None:
            wanted = [u for u in (_to_uuid(i) for i in ids) if u is not None]
            if not wanted:
                return []
            filters["id__in"] = wanted
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
        if target_action:
            filters["target_action"] = target_action
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

    async def set_office_fingerprint(self, trigger_id: str, fingerprint: str) -> None:
        """Record the watched content's fingerprint an office trigger last saw (server-only, like
        ``bind_version``): its next fire runs only when the content moved off it."""
        from matrx_orm import JsonbMerge

        await get_model("WfTrigger").update_where(
            {"id": _to_uuid(trigger_id), "deleted_at__isnull": True},
            event_source=JsonbMerge("event_source", {"fingerprint": str(fingerprint)}),
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

    async def record_fire(
        self, trigger_id: str, run_id: str | None, *, fired_at: datetime | None = None
    ) -> None:
        """Bump fire_count, set last_fired_at (+ last_run_id when the fire started a workflow
        run; an Action fire starts none and leaves it). Never touches next_run_at: a cron
        trigger's clock is the host's scheduler."""
        from matrx_orm import F

        fired_at = fired_at or datetime.now(UTC)
        values: dict[str, Any] = {"fire_count": F("fire_count") + 1, "last_fired_at": fired_at}
        if run_id:
            values["last_run_id"] = str(UUID(run_id))
        await get_model("WfTrigger").update_where({"id": str(UUID(trigger_id))}, **values)

    async def record_outcome(self, trigger_id: str, outcome: FireOutcome) -> bool:
        """``record_fire`` for one fire's outcome — the ONE door every fire path uses: a skipped fire
        (nothing ran) bumps nothing. Returns True when the counters moved."""
        if outcome.skipped:
            return False
        await self.record_fire(trigger_id, outcome.run_id)
        return True

    async def set_target_input(self, trigger_id: str, target_input: dict[str, Any]) -> None:
        """Replace an Action-target trigger's ``target_input`` (static values and its declared
        ``{"$event": path}`` bindings). The host validates it against the Action first."""
        await get_model("WfTrigger").update_where(
            {"id": _to_uuid(trigger_id), "deleted_at__isnull": True}, target_input=dict(target_input or {})
        )

    async def update_fields(
        self,
        trigger_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        cron_expression: str | None = None,
        timezone: str | None = None,
        event_source: dict[str, Any] | None = None,
        default_inputs: dict[str, Any] | None = None,
        target_input: dict[str, Any] | None = None,
        definition_version_id: str | None = None,
        expected_version: int | None = None,
        touch: bool = False,
    ) -> TriggerRow | None:
        """Edit a live trigger's own fields (None = leave it) in ONE UPDATE. The same store-boundary
        checks as ``create``, all run before anything is written: a cron expression + timezone must
        compute a next fire, an event source must be a valid spec and belongs to kind='event' only.
        Kind and target never change here — a trigger that should run something else, or start another
        way, is a new trigger. ``target_input`` is an Action target's input (the host validates it
        against the Action first); ``definition_version_id`` binds the published version a store source
        fires (its graph hash rides ``event_source``).

        ``expected_version`` (optional): the row's ``version`` the editor loaded. When given, the write
        is a compare-and-swap on it (matrx-orm ``update_where(expected_version=)``) — a row someone
        else changed since raises ``OptimisticLockError`` (the host answers 409 version_conflict) and
        writes nothing. Omitted = last-write-wins (the on/off toggle and older callers). ``touch``
        writes the row even when no column of its own changes (a clock-only cadence edit), so the
        guard still runs and the version still moves. Returns the row."""
        row = await self.load(trigger_id)
        if row is None:
            return None
        values: dict[str, Any] = {}
        if name is not None:
            values["name"] = name
        if description is not None:
            values["description"] = description
        if cron_expression is not None or timezone is not None:
            if cron_expression is not None and row.kind != "cron":
                raise ValueError("cron_expression is only valid on kind='cron' triggers")
            expression = cron_expression if cron_expression is not None else row.cron_expression
            zone = timezone if timezone is not None else row.timezone
            if row.kind == "cron" and expression:
                _compute_next_run(expression, zone, base=None)
            if cron_expression is not None:
                values["cron_expression"] = cron_expression
            if timezone is not None:
                values["timezone"] = timezone
        if event_source is not None:
            if row.kind != "event":
                raise ValueError("event_source is only valid on kind='event' triggers")
            try:
                values["event_source"] = event_source_json(event_source)
            except Exception as e:
                raise ValueError(f"invalid event_source: {e}") from e
        if default_inputs is not None:
            values["default_inputs"] = dict(default_inputs)
        if target_input is not None:
            values["target_input"] = dict(target_input)
        if definition_version_id is not None:
            values["definition_version_id"] = _to_uuid(definition_version_id)
        if not values and (touch or expected_version is not None):
            values["name"] = row.name  # no column of its own changed: the write still guards + moves the version
        if values:
            guard = {"expected_version": int(expected_version)} if expected_version is not None else {}
            await get_model("WfTrigger").update_where(
                {"id": _to_uuid(trigger_id), "deleted_at__isnull": True}, **guard, **values
            )
        return await self.load(trigger_id)

    def write_transaction(self) -> Any:
        """One transaction over the trigger's database: an edit's row write and its clock's write
        (``scheduler.*``, the same database) land together or not at all."""
        from matrx_orm import transaction

        return transaction(getattr(get_model("WfTrigger"), "_database", None))

    async def set_needs_reconnect(self, trigger_id: str, sentence: str | None) -> None:
        """Set (a sentence) or clear (None) the trigger's ``needs_reconnect`` state.

        Setting it also turns the trigger OFF in the same write: a trigger waiting on a reconnect
        never reads as on (one consistent state for every list, clock and sync). Clearing it
        leaves ``is_active`` alone — turning it on again is the caller's own, separate step."""
        values: dict[str, Any] = {"needs_reconnect": sentence}
        if sentence:
            values["is_active"] = False
        await get_model("WfTrigger").update_where(
            {"id": _to_uuid(trigger_id), "deleted_at__isnull": True}, **values
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

    mapping = dict(row)
    return TriggerRow(
        id=str(row["id"]),
        definition_id=str(row["definition_id"]) if row["definition_id"] else None,
        # Guarded like callback_url: a standalone host on an older baseline may not carry them.
        target_action=mapping.get("target_action"),
        target_input=_coerce(mapping.get("target_input")) or {},
        needs_reconnect=mapping.get("needs_reconnect"),
        metadata=_coerce(mapping.get("metadata")) or {},
        definition_version_id=str(row["definition_version_id"])
        if row["definition_version_id"]
        else None,
        name=row["name"],
        description=row["description"],
        kind=row["kind"],
        cron_expression=row["cron_expression"],
        timezone=row["timezone"],
        webhook_secret=row["webhook_secret"],
        signature_scheme=mapping.get("signature_scheme"),
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
        version=mapping.get("version"),
    )
