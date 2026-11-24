"""Store for ``workflow.node_data_slot`` — the sample-data spine (ENGINE_SPEC §7).

Three persisted data slots per node, per DEFINITION (never per run):
``declared_sample`` (user-authored), ``last_test_output`` (auto-captured on a
successful single-node test), ``last_live_output`` (adopted from a run's
latest error-NULL executor outcomes at terminal/park time). One row per
``(definition_id, node_id, slot)`` — upsert-only; run history stays in
``workflow.node_outcome``.

Everything goes through the host-injected matrx-orm model (``WfNodeDataSlot``)
or matrx-orm's conflict-write / insert-select primitives. Migration 0022
creates the table.
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

logger = logging.getLogger(__name__)

VALID_SLOTS: tuple[str, ...] = ("declared_sample", "last_test_output", "last_live_output")
"""The only slot names that exist — mirrors the table CHECK constraint."""

MAX_SLOT_VALUE_BYTES: int = 256 * 1024
"""Upper bound on one slot's serialized ``value`` (and ``emissions``).

Slots are design-time samples for edge-Satisfied derivation, previews, and
mapping pickers — not an archive. A multi-MB output belongs in
``workflow.node_outcome`` (where it already is); shoving it into the slot
table would bloat every studio bulk fetch."""


class SlotValueTooLargeError(ValueError):
    """Raised when a slot write exceeds :data:`MAX_SLOT_VALUE_BYTES`.

    Carries the offending size so callers can surface an actionable message
    instead of a bare constraint failure."""

    def __init__(self, *, field: str, size_bytes: int) -> None:
        self.field = field
        self.size_bytes = size_bytes
        super().__init__(
            f"node_data_slot.{field} is {size_bytes} bytes serialized — exceeds the "
            f"{MAX_SLOT_VALUE_BYTES}-byte slot cap. Slots hold design-time samples, "
            f"not archives; trim the payload (full run outputs stay in "
            f"workflow.node_outcome)."
        )


class NodeDataSlotRow(BaseModel):
    """Row shape for workflow.node_data_slot queries."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    definition_id: str
    node_id: str
    slot: str
    value: Any  # JSONB — the node's captured/declared output payload
    emissions: dict[str, Any] = Field(default_factory=dict)
    output_kind: str | None = None
    source: str
    captured_at: datetime
    captured_by: str | None = None
    created_by: str


class NodeDataSlotStore:
    """CRUD + adoption over ``workflow.node_data_slot``.

    Write rules (spec §7.2): ``declared_sample`` only via the explicit API;
    ``last_test_output`` by the node-test endpoint on success;
    ``last_live_output`` by :meth:`adopt_live_outputs` at run terminal/park.
    """

    async def upsert_slot(
        self,
        *,
        definition_id: str,
        node_id: str,
        slot: str,
        value: Any,
        emissions: dict[str, Any] | None = None,
        output_kind: str | None = None,
        source: str,
        user_id: str,
        captured_by: str | None = None,
    ) -> NodeDataSlotRow:
        """Insert-or-replace ONE mandate row. Returns the stored row.

        Raises ``ValueError`` on an unknown slot name and
        :class:`SlotValueTooLargeError` when ``value``/``emissions`` exceed
        the serialized-size cap."""
        # Validate (slot name, owner, size cap) BEFORE the model is resolved:
        # these gates must fire without a configured database.
        write = _slot_write(
            definition_id=definition_id,
            node_id=node_id,
            slot=slot,
            value=value,
            emissions=emissions,
            output_kind=output_kind,
            source=source,
            user_id=user_id,
            captured_by=captured_by,
        )

        from matrx_orm.operations.conflict_writes import upsert_with_conflict

        from matrx_graph.db._registry import get_model

        row = await upsert_with_conflict(
            get_model("WfNodeDataSlot"),
            write,
            on_conflict=list(_SLOT_KEY),
            set_fields=_slot_set_fields(),
        )
        return _row_to_slot(row)

    async def get_slots(
        self, definition_id: str, node_id: str | None = None
    ) -> list[NodeDataSlotRow]:
        """All mandate row for one node, or for the whole definition
        (``node_id=None`` — the studio's bulk fetch for edge-Satisfied
        derivation)."""
        from matrx_graph.db._registry import get_model

        if node_id is None:
            rows = await (
                get_model("WfNodeDataSlot")
                .filter(definition_id=str(UUID(definition_id)))
                .order_by("node_id", "slot")
                .values()
            )
        else:
            rows = await (
                get_model("WfNodeDataSlot")
                .filter(definition_id=str(UUID(definition_id)), node_id=node_id)
                .order_by("slot")
                .values()
            )
        return [slot for slot in (_row_to_slot(r) for r in rows) if not _holds_run_reference(slot)]

    async def delete_slot(self, definition_id: str, node_id: str, slot: str) -> bool:
        """Delete ONE mandate row. True iff a row was deleted."""
        if slot not in VALID_SLOTS:
            raise ValueError(f"unknown node_data_slot {slot!r} (valid: {', '.join(VALID_SLOTS)})")
        from matrx_graph.db._registry import get_model

        deleted = await get_model("WfNodeDataSlot").delete_where(
            definition_id=str(UUID(definition_id)),
            node_id=node_id,
            slot=slot,
        )
        return deleted == 1

    async def delete_missing_nodes(self, definition_id: str, keep_node_ids: list[str]) -> int:
        """Drop slots for nodes no longer in the draft (spec §7.2: deleting a
        node deletes its slots). Returns the number of rows removed."""
        from matrx_graph.db._registry import get_model

        return await get_model("WfNodeDataSlot").delete_where(
            definition_id=str(UUID(definition_id)),
            node_id__not_in=list(keep_node_ids),
        )

    async def adopt_live_outputs(self, *, run_id: str, definition_id: str, user_id: str) -> int:
        """Copy a run's per-node latest error-NULL EXECUTOR outcomes into the
        ``last_live_output`` slots (spec §7.2, run terminal/park time).

        Per node, the newest ``(step, attempt)`` outcome with ``error IS NULL
        AND source = 'executor'`` wins — skip/mock/user sources never pollute
        the sample spine. Idempotent (upsert per node).

        A slot holds the step's WHOLE result. ``node_outcome.output`` keeps a
        large value by reference (``{REF_KEY: <sha256>}``, MKT-171) and that
        hash means something only inside the run that stored it, so every
        reference is resolved here through the run value store
        (``resolve_run_values``) before the sample is written — a definition's
        sample never carries a run's marker (2026-10-28: 1,567 live slots did,
        and the design-time "Only when" over them saw a one-key dict instead of
        the list). A result over the slot cap once whole, or whose stored value
        is gone, is left out (the slot keeps what it had; the full payload
        stays in the run).

        Cost (2026-10-28, run 322b35c1): every referenced value used to be read back whole, one step at a
        time, only for the slot cap to refuse most of them (a 600-item list is 0.4-2 MB; the cap is 256 KB).
        So the stored sizes are read first in ONE query, a step whose referenced values alone already exceed
        the cap is left out without reading them, and the rest resolve in ONE read for the whole run.

        Returns the number of node slots that actually landed."""
        from matrx_graph.checkpoint.value_store import MAX_HASHES_PER_READ, load_run_values
        from matrx_graph.checkpoint.values import (
            _REF_BYTES,
            referenced_hashes,
        )
        from matrx_graph.db._registry import get_model

        rows = await (
            get_model("WfNodeOutcome")
            .filter(run_id=str(UUID(run_id)), error__isnull=True, source="executor")
            .order_by("-step", "-attempt")
            .values("node_id", "output", "emissions", "output_kind")
        )
        latest: dict[str, dict[str, Any]] = {}
        for row in rows:
            latest.setdefault(str(row["node_id"]), row)

        decoded = {
            node_id: (_coerce_json(row["output"]), _coerce_json(row["emissions"]) or {})
            for node_id, row in latest.items()
        }
        refs = {node_id: referenced_hashes(v) | referenced_hashes(e) for node_id, (v, e) in decoded.items()}
        wanted = set().union(*refs.values()) if refs else set()
        sizes: dict[str, int] = {}
        if wanted:
            ordered = sorted(wanted)
            for i in range(0, len(ordered), MAX_HASHES_PER_READ):
                for found in await get_model("WfCheckpointValue").filter(
                    run_id=str(UUID(run_id)), value_hash__in=ordered[i : i + MAX_HASHES_PER_READ]
                ).values("value_hash", "size_bytes"):
                    sizes[str(found["value_hash"])] = int(found["size_bytes"] or 0)
        # A stored value's size counts each nested reference as its marker, so the whole result is at least
        # the referenced values' sizes less their markers: over the cap by that alone = over the cap whole.
        too_large = {
            node_id
            for node_id, hashes in refs.items()
            if sum(sizes.get(h, 0) - _REF_BYTES for h in hashes) > MAX_SLOT_VALUE_BYTES
        }
        store: dict[str, Any] = {}
        readable = sorted(set().union(*(refs[n] for n in refs if n not in too_large))) if refs else []
        for i in range(0, len(readable), MAX_HASHES_PER_READ):
            store.update(await load_run_values(run_id, readable[i : i + MAX_HASHES_PER_READ]))

        # ONE statement for the whole run (L-SPEED 6k): one upsert per step was ~71 single-row writes
        # per research run on the shared pool.
        # 🚨 OFF THE EVENT LOOP (2026-11-17): resolving every step's references and serialising its whole
        # result is pure CPU — live it froze the server's loop for 1,129 ms (json.dumps in _bounded_dumps,
        # task wf_slot_adoption), so no request was served meanwhile. It runs in a worker thread.
        writes = await asyncio.to_thread(
            _build_live_writes,
            latest=latest,
            decoded=decoded,
            refs=refs,
            too_large=too_large,
            store=store,
            definition_id=definition_id,
            user_id=user_id,
            run_id=run_id,
        )
        # A result that IS JSON null cannot ride the bulk write (its prep drops a None column, and the
        # column is NOT NULL); those few go one at a time through the single write, which keeps it.
        bulk = [w for w in writes if w["value"].text != "null"]
        singles = [w for w in writes if w["value"].text == "null"]
        landed = 0
        if bulk:
            from matrx_orm.operations.create import bulk_upsert

            try:
                # The bulk write sets every column exactly as the single write does: a column a row has as
                # None (no output kind, no capturer) is written NULL, never COALESCEd to the stored value.
                rows = await bulk_upsert(
                    get_model("WfNodeDataSlot"),
                    bulk,
                    list(_SLOT_KEY),
                    list(_slot_set_fields()),
                    returning=["id"],
                    clear_when_empty=_SLOT_NULLABLE,
                )
                landed += len(rows)
            except Exception:
                # One bad row fails the whole statement; every other step's sample still lands, one at a time.
                logger.warning(
                    "[wf-slots] run %s: the bulk sample write failed — writing %d samples one at a time",
                    run_id[:8],
                    len(bulk),
                    exc_info=True,
                )
                singles = bulk + singles
        if singles:
            from matrx_orm.operations.conflict_writes import upsert_with_conflict

            for write in singles:
                try:
                    await upsert_with_conflict(
                        get_model("WfNodeDataSlot"),
                        write,
                        on_conflict=list(_SLOT_KEY),
                        set_fields=_slot_set_fields(),
                    )
                    landed += 1
                except Exception:
                    logger.warning(
                        "[wf-slots] run %s step %s: sample write failed — slot keeps what it had",
                        run_id[:8],
                        write["node_id"],
                        exc_info=True,
                    )
        return landed



def _build_live_writes(
    *,
    latest: dict[str, dict[str, Any]],
    decoded: dict[str, tuple[Any, Any]],
    refs: dict[str, set[str]],
    too_large: set[str],
    store: dict[str, Any],
    definition_id: str,
    user_id: str,
    run_id: str,
) -> list[dict[str, Any]]:
    """Every adopted step's slot row, resolved and serialised (sync, CPU-bound — run in a thread)."""
    from matrx_graph.checkpoint.values import MissingCheckpointValueError, resolve_values

    writes: list[dict[str, Any]] = []
    for node_id, row in latest.items():
        if node_id in too_large:
            continue
        value, emissions = decoded[node_id]
        try:
            if refs[node_id]:
                value = resolve_values(value, store)
                emissions = resolve_values(emissions, store)
            writes.append(
                _slot_write(
                    definition_id=definition_id,
                    node_id=node_id,
                    slot="last_live_output",
                    value=value,
                    emissions=emissions if isinstance(emissions, dict) else {},
                    output_kind=row["output_kind"],
                    source="live_run",
                    user_id=user_id,
                    captured_by=user_id,
                )
            )
        except SlotValueTooLargeError:
            continue
        except MissingCheckpointValueError:
            logger.warning(
                "[wf-slots] run %s step %s: a stored value of its result is gone — sample not adopted",
                run_id[:8],
                node_id,
            )
            continue
    return writes


_SLOT_KEY: tuple[str, ...] = ("definition_id", "node_id", "slot")

_SLOT_NULLABLE: tuple[str, ...] = ("output_kind", "captured_by")
"""The slot columns a write may carry as None; the bulk write must clear them, as the single write does."""


def _slot_set_fields() -> dict[str, Any]:
    """Every non-key column is set unconditionally on conflict — captured_by included, which the ORM would
    otherwise leave out of the SET clause when it is None."""
    from matrx_orm import Excluded

    cols = ("value", "emissions", "output_kind", "source", "captured_at", "captured_by", "created_by")
    return {col: Excluded(col) for col in cols}


def _slot_write(
    *,
    definition_id: str,
    node_id: str,
    slot: str,
    value: Any,
    emissions: dict[str, Any] | None,
    output_kind: str | None,
    source: str,
    user_id: str,
    captured_by: str | None,
) -> dict[str, Any]:
    """One slot row, checked and serialised — the single shape every slot write sends.

    Raises ``ValueError`` (unknown slot, no owner) and :class:`SlotValueTooLargeError`.

    ``value`` is serialised BEFORE it reaches the ORM: it may legitimately be JSON null ('null'::jsonb in a
    NOT NULL column), and the ORM write path drops a Python ``None`` from the INSERT. The text goes in as
    ``RawJson`` (a plain ``str`` in a json field is stored as a JSON string, matrx-orm c73b6d29)."""
    if slot not in VALID_SLOTS:
        raise ValueError(f"unknown node_data_slot {slot!r} (valid: {', '.join(VALID_SLOTS)})")
    if not user_id:
        raise ValueError("node_data_slot.created_by is required — refusing ownerless write")
    from matrx_orm import RawJson

    return {
        "definition_id": UUID(definition_id),
        "node_id": node_id,
        "slot": slot,
        "value": RawJson(_bounded_dumps(value, field="value")),
        "emissions": RawJson(_bounded_dumps(emissions or {}, field="emissions")),
        "output_kind": output_kind,
        "source": source,
        "captured_at": datetime.now(UTC),
        "captured_by": _to_uuid(captured_by),
        "created_by": UUID(user_id),
    }

def _holds_run_reference(slot: NodeDataSlotRow) -> bool:
    """A slot adopted before 2026-10-28 may hold a run's reference marker instead of the value; the
    slot keeps no run id to resolve it, so it is no sample at all — absent until the next run adopts the
    whole result (``adopt_live_outputs``)."""
    from matrx_graph.checkpoint.values import referenced_hashes

    if referenced_hashes(slot.value) or referenced_hashes(slot.emissions):
        logger.warning(
            "[wf-slots] %s/%s %s holds a run's reference marker, not a value — not offered as a sample",
            slot.definition_id[:8],
            slot.node_id,
            slot.slot,
        )
        return True
    return False


def _coerce_json(value: Any) -> Any:
    """A jsonb column as Python: the driver codec decodes it; text from an older pool is parsed."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def _bounded_dumps(value: Any, *, field: str) -> str:
    encoded = json.dumps(value)
    size = len(encoded.encode("utf-8"))
    if size > MAX_SLOT_VALUE_BYTES:
        raise SlotValueTooLargeError(field=field, size_bytes=size)
    return encoded


def _to_uuid(value: str | None) -> UUID | None:
    """Coerce a string to a UUID, or None. See definition_store._to_uuid."""
    if not value:
        return None
    try:
        return UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return None


def _row_to_slot(row: Any) -> NodeDataSlotRow:
    def _coerce(v: Any) -> Any:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return v
        return v

    emissions = _coerce(row["emissions"]) or {}
    return NodeDataSlotRow(
        id=str(row["id"]),
        definition_id=str(row["definition_id"]),
        node_id=row["node_id"],
        slot=row["slot"],
        value=_coerce(row["value"]),
        emissions=emissions if isinstance(emissions, dict) else {},
        output_kind=row["output_kind"],
        source=row["source"],
        captured_at=row["captured_at"],
        captured_by=str(row["captured_by"]) if row["captured_by"] else None,
        created_by=str(row["created_by"]),
    )
