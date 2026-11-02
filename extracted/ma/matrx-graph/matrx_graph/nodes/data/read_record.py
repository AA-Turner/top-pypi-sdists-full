"""``data.read_record`` — read ONE platform Record, as the operator.

THE THIRD PLACE. A Google object (or any other platform entity) has to be
reachable in three places with no seam: its own home screen, the chat, and the
custom-data system as a Record a workflow reads. This node is that third place,
and it is ONE platform unit rather than a reader per capability: it takes an
entity type + a record id and answers with the row, shaped as the registered
``platform_record`` kind.

IDENTITY IS CARRIED, NEVER PASSED IN. There is no ``user_id`` /
``organization_id`` input and there never will be: the actor and organization
are minted at the boundary and ride the run's context
(``ctx.user_id`` / ``ctx.organization_id``). A workflow author cannot choose
whose eyes this reads with.

ACCESS HAS ONE ANSWER. ``iam.has_access_for(actor, token, id, 'viewer')``,
reached through the injected gateway (``matrx_orm.platform_access_check``
host-side). Never ``organization_id ==`` and never ``created_by ==``:
organization is TENANCY, never permission — the row's org is REPORTED in the
payload and is not consulted for the decision.

EVERY MISS IS A NAMED REFUSAL, never an empty success. Unknown entity type,
absent row, denied access, no actor, no wiring — each is a node ``Failure``
carrying a sentence a person can read and the remedy. A denied read leaks
nothing: no fields, no label, no organization.
"""

from __future__ import annotations

import json
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.records import RecordReadRefused, get_record_gateway
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras

#: How many known entity types the unknown-type refusal names. A refusal that
#: dumps 240 tokens is unreadable; a handful of real ones is a usable remedy.
_SUGGESTION_LIMIT = 12

#: Columns that, when present, carry a row's human name — checked in this order,
#: and ONLY when the registry declares no ``title_column`` for the entity. The
#: registry is the first authority; this is the fallback, and it is presentation
#: only (the payload always carries the row under ``fields``).
_LABEL_COLUMNS: tuple[str, ...] = (
    "name",
    "title",
    "label",
    "display_name",
    "subject",
    "summary",
    "slug",
    "email",
)


class ReadRecordInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_type: str = Field(
        min_length=1,
        description=(
            "The platform entity type token (platform.entity_types.token), e.g. "
            "'google_document', 'calendar_event', 'party'."
        ),
        title="Table",
        json_schema_extra=field_extras(widget="entity_type_picker", order=1),
    )
    record_id: str = Field(
        min_length=1,
        title="Record",
        description="The record to read.",
        json_schema_extra=field_extras(widget="record_picker", entity_field="entity_type", order=2),
    )


class PlatformRecord(KindModel, kind="platform_record"):
    """One platform Record, read as the operator.

    The kind is deliberately generic: the platform has one Record shape and
    every entity type answers in it, so a workflow (and every renderer) learns
    it once instead of once per table. The row's own columns live under
    ``fields`` — the columns are the table's business, not this kind's.
    """

    entity_type: str = Field(description="platform.entity_types token this row belongs to.")
    record_id: str = Field(description="The record's id.")
    table: str = Field(description="Schema-qualified table the row was read from.")
    entity_label: str = Field(
        default="",
        description="Human label of the TYPE, from the registry (e.g. 'Google Document').",
    )
    record_label: str = Field(
        default="",
        description=(
            "Human name of THIS row, taken from whichever of name/title/label/… "
            "the table carries. Empty when it carries none."
        ),
    )
    organization_id: str | None = Field(
        default=None,
        description=(
            "The row's tenancy stamp, REPORTED for downstream scoping. Never the "
            "basis of the access decision — that is iam.has_access_for alone."
        ),
    )
    fields: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="The row's columns, JSON-safe, minus any the registry excludes.",
    )
    hidden_fields: list[str] = Field(
        default_factory=list,
        description=(
            "Columns the entity registry marks as not-for-clients, withheld from "
            "``fields``. Named rather than silently dropped."
        ),
    )


def _jsonable(row: dict[str, Any]) -> dict[str, JsonValue]:
    return json.loads(json.dumps(row, default=str))


def _record_label(fields: dict[str, JsonValue], title_column: str) -> str:
    for column in (title_column, *_LABEL_COLUMNS) if title_column else _LABEL_COLUMNS:
        value = fields.get(column)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


class ReadRecordExecutor:
    """Read one platform Record by entity type + id, as the run's operator."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.read_record",
        category=NodeCategory.DATA,
        display_name="Read a Record",
        description=(
            "Read one record from the platform — any registered entity type — "
            "with your own access."
        ),
        input_schema=ReadRecordInput,
        output_schema=PlatformRecord,
        output_kind="platform_record",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        # A read is safe to re-invoke on resume; it changes nothing.
        determinism=ActionTier.IDEMPOTENT,
        icon="database",
        tags=("data", "record", "read", "platform"),
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ReadRecordInput,
        config: BaseModel,
    ) -> NodeResult[PlatformRecord]:
        _ = config
        gateway = get_record_gateway()
        if gateway is None:
            return failure(
                "record_gateway_unavailable",
                "This workflow cannot read platform records because the host has "
                "not wired the record gateway, so there is nothing to read "
                "through. Remedy: call "
                "matrx_graph.configure_record_gateway(<gateway>) once at "
                "startup (aidream does this in _configure_matrx_graph).",
            )

        entity_type = inputs.entity_type.strip()
        record_id = inputs.record_id.strip()
        if not entity_type or not record_id:
            return failure(
                "incomplete_reference",
                "A record is addressed by BOTH its entity type and its id, and "
                f"one of them arrived empty (entity_type={inputs.entity_type!r}, "
                f"record_id={inputs.record_id!r}). Remedy: wire both inputs from "
                "the step that produced the record.",
            )

        actor_id = (ctx.user_id or "").strip()
        if not actor_id:
            return failure(
                "no_actor_in_context",
                "This run carries no actor, so whether a person may read "
                f"{entity_type} {record_id} cannot be answered — and this node "
                "never reads on a default identity. Remedy: start the run with a "
                "real actor (the boundary mints it; a worker or schedule passes "
                "system_app_context(feature, user_id=…, organization_id=…)).",
            )

        entity = await gateway.describe_entity(entity_type)
        if entity is None:
            known = list(await gateway.known_entity_types())
            shown = ", ".join(sorted(known)[:_SUGGESTION_LIMIT])
            more = (
                f" (and {len(known) - _SUGGESTION_LIMIT} more)"
                if len(known) > _SUGGESTION_LIMIT
                else ""
            )
            return failure(
                "unknown_entity_type",
                f"There is no platform entity type called '{entity_type}' — the "
                "platform's entity registry does not list it, so no table "
                "answers to that name. Remedy: use one of the registered types "
                f"({shown}{more}), or register the table in the entity registry "
                "and regenerate models.",
                details={"entity_type": entity_type},
            )

        if not await gateway.may_read(
            actor_id=actor_id, entity_type=entity.entity_type, record_id=record_id
        ):
            # Deliberately leaks NOTHING about the row — not its label, not its
            # organization, not whether it even exists.
            return failure(
                "access_denied",
                f"You do not have access to this {entity.label or entity.entity_type} "
                f"({entity_type} {record_id}), so the workflow cannot read it. "
                "Remedy: ask someone who can already open it to share it with "
                "you at view level, then run this again.",
                details={"entity_type": entity.entity_type, "record_id": record_id},
            )

        try:
            row = await gateway.read_row(entity=entity, record_id=record_id)
        except RecordReadRefused as refused:
            return failure(
                "record_type_not_readable",
                f"{refused.reason} Remedy: read this {entity.label or entity.entity_type} "
                "through the record store's own doors instead of by id here.",
                details={"entity_type": entity.entity_type, "record_id": record_id},
            )
        if row is None:
            return failure(
                "record_not_found",
                f"No {entity.label or entity.entity_type} with id {record_id} "
                f"exists in {entity.qualified_table} (it was deleted, or the id "
                "belongs to a different type). Remedy: check the id, or read the "
                "record from the step that created it.",
                details={"entity_type": entity.entity_type, "record_id": record_id},
            )

        fields = _jsonable(dict(row))
        hidden = sorted(c for c in entity.excluded_columns if c in fields)
        for column in hidden:
            fields.pop(column, None)
        organization_id = fields.get("organization_id")
        return success(
            PlatformRecord(
                entity_type=entity.entity_type,
                record_id=record_id,
                table=entity.qualified_table,
                entity_label=entity.label or "",
                record_label=_record_label(fields, entity.title_column),
                organization_id=(
                    str(organization_id) if isinstance(organization_id, str) else None
                ),
                fields=fields,
                hidden_fields=hidden,
            )
        )


__all__ = ["PlatformRecord", "ReadRecordExecutor", "ReadRecordInput"]
