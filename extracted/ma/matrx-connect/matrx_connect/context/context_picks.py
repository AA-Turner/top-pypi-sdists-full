"""The pick: one context value for any table.

A context is an ordered list of picks, possibly across organizations. A pick is an organization, a
table (a custom Table's uuid or a built-in ``entity:<token>`` address, optionally a named view of it),
and optionally records and fields. Contract:
common-docs/systems/data/scopes-context/projects/any-table-context/CONTRACT.md (§1, §2).

Pure functions, no I/O. The legacy wire fields (``scope_ids``, ``active_scope_type_ids``) are read
through :func:`fold_legacy_selection` and written back through :func:`legacy_selection`. A pick folded
from a legacy field has ``organization_id = None`` (and ``table = None`` for a record id) until its door
completes it. Shared cases with the TypeScript twin: ``tests/fixtures/context_picks_cases.json``.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, NamedTuple
from uuid import UUID

from matrx_utils.entity_address import ENTITY_PREFIX, parse_entity_address
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ContextPick(BaseModel):
    """One picked table, or records of it, or fields of those, in one organization."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    organization_id: UUID | None = Field(
        description="The organization this pick lives in. Null only on a pick folded from a legacy field.",
    )
    table: str | None = Field(
        description="A custom Table id, or a built-in table as 'entity:<token>' (no '@org'). Null only on a legacy record id.",
    )
    view: str | None = Field(default=None, description="A named view of the built-in table.")
    record_ids: list[UUID] = Field(
        default_factory=list, description="Picked records; empty means the whole table."
    )
    fields: list[str] = Field(
        default_factory=list, description="Spotlighted fields: a custom Field id or a column key."
    )

    @field_validator("table")
    @classmethod
    def _one_table_address(cls, value: str | None) -> str | None:
        if value is None:
            return None
        text = value.strip()
        if text.startswith(ENTITY_PREFIX):
            address = parse_entity_address(text)
            if address is None:
                raise ValueError(f"{value!r} is not a built-in table address (entity:<token>)")
            if address.organization_id is not None:
                raise ValueError(
                    "a pick names its organization in organization_id, never as '@org' on the table"
                )
            return text
        try:
            return str(UUID(text))
        except ValueError:
            raise ValueError(
                f"{value!r} is neither a custom Table id nor an entity:<token> address"
            ) from None

    @model_validator(mode="after")
    def _a_tableless_pick_is_a_folded_record_pick(self) -> ContextPick:
        # table=None exists only for a legacy scope id read before its door completes it: no
        # organization yet, and at least one record. Anything else would vanish in canonical_picks.
        if self.table is None and (self.organization_id is not None or not self.record_ids):
            raise ValueError(
                "a pick with no table is a folded legacy record pick: organization_id must be null "
                "and record_ids non-empty"
            )
        return self

    @property
    def is_built_in(self) -> bool:
        return self.table is not None and self.table.startswith(ENTITY_PREFIX)


class LegacySelection(NamedTuple):
    """What the legacy wire fields can carry of a context, plus the built-in picks they cannot."""

    scope_ids: list[str]
    active_scope_type_ids: list[str]
    built_in: list[ContextPick]


#: A pick as given: the model, or its JSON object (validated on read).
type PickInput = ContextPick | Mapping[str, object]


def _as_pick(value: PickInput) -> ContextPick:
    return value if isinstance(value, ContextPick) else ContextPick.model_validate(value)


def _unique(values: Iterable[Any]) -> list[Any]:
    return list(dict.fromkeys(values))


def canonical_picks(picks: Iterable[PickInput] | None) -> list[ContextPick]:
    """Merge picks of the same organization, table, view and whole-or-records (records and fields
    unioned, first-seen order), and drop what a folded legacy pick repeats of a filled one."""
    given = [_as_pick(p) for p in (picks or [])]
    filled_records = {r for p in given if p.table is not None for r in p.record_ids}
    filled_tables = {
        p.table for p in given if p.organization_id is not None and p.table and not p.record_ids
    }
    merged: dict[tuple[Any, ...], dict[str, Any]] = {}
    for pick in given:
        records = pick.record_ids
        if pick.table is None:
            records = [r for r in records if r not in filled_records]
            if not records:
                continue
        elif pick.organization_id is None and not records and pick.table in filled_tables:
            continue
        key = (pick.organization_id, pick.table, pick.view, bool(records))
        slot = merged.setdefault(key, {"pick": pick, "record_ids": [], "fields": []})
        slot["record_ids"].extend(records)
        slot["fields"].extend(pick.fields)
    return [
        slot["pick"].model_copy(
            update={"record_ids": _unique(slot["record_ids"]), "fields": _unique(slot["fields"])}
        )
        for slot in merged.values()
    ]


def _uuid_or_none(value: object) -> UUID | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return UUID(value.strip())
    except ValueError:
        return None


def fold_legacy_selection(
    scope_ids: Iterable[object] | None,
    active_scope_type_ids: Iterable[object] | None,
    picks: Iterable[PickInput] | None = None,
) -> list[ContextPick]:
    """``picks`` plus the legacy fields read as picks, canonical. A legacy id that is not a uuid is
    skipped, never raised: the legacy field keeps it and its readers drop it as they always have."""
    record_ids = [u for u in (_uuid_or_none(s) for s in (scope_ids or [])) if u is not None]
    type_ids = [
        u for u in (_uuid_or_none(t) for t in (active_scope_type_ids or [])) if u is not None
    ]
    folded: list[ContextPick] = []
    if record_ids:
        folded.append(ContextPick(organization_id=None, table=None, record_ids=record_ids))
    folded.extend(ContextPick(organization_id=None, table=str(t)) for t in type_ids)
    return canonical_picks([*(picks or []), *folded])


def legacy_selection(picks: Iterable[PickInput] | None) -> LegacySelection:
    """The legacy wire fields of ``picks``: custom-table record ids, whole custom tables, and the
    built-in picks, which never enter ``scope_ids`` (the custom resolver would refuse them)."""
    scope_ids: list[str] = []
    type_ids: list[str] = []
    built_in: list[ContextPick] = []
    for pick in canonical_picks(picks):
        if pick.is_built_in:
            built_in.append(pick)
        elif pick.record_ids:
            scope_ids.extend(str(r) for r in pick.record_ids)
        elif pick.table is not None:
            type_ids.append(pick.table)
    return LegacySelection(_unique(scope_ids), _unique(type_ids), built_in)


#: The legacy wire fields a request may declare beside ``context_picks``.
_LEGACY_FIELDS = ("scope_ids", "active_scope_type_ids")


def legacy_ids_kept(sent: object, derived: list[str]) -> list[str] | None:
    """A legacy field as the caller sent it, byte for byte, then each id derived from the picks it
    does not already name (compared as uuids). None when both are empty and nothing was sent."""
    kept = list(sent) if isinstance(sent, list | tuple) else []
    named = {str(_uuid_or_none(s) or s) for s in kept}
    out = kept + [d for d in derived if d not in named]
    return out or (None if sent is None else out)


def _write_selection(
    request: BaseModel,
    picks: list[ContextPick],
    sent: Mapping[str, object],
    *,
    mark_set: bool,
) -> BaseModel:
    legacy = legacy_selection(picks)
    derived = {"scope_ids": legacy.scope_ids, "active_scope_type_ids": legacy.active_scope_type_ids}
    fields = type(request).model_fields
    update: dict[str, object] = {"context_picks": picks or None}
    for name in _LEGACY_FIELDS:
        if name in fields:
            update[name] = legacy_ids_kept(sent.get(name), derived[name])
    if request.model_config.get("frozen"):
        return request.model_copy(update=update)
    # Written through __dict__: a validate_assignment model would re-run the fold between two of
    # the three writes and mix the old selection into the new one.
    for name, value in update.items():
        if value != getattr(request, name, None):
            request.__dict__[name] = value
            if mark_set:
                request.__pydantic_fields_set__.add(name)
    return request


class CarriesContextPicks(BaseModel):
    """A request that carries a context: ``context_picks``, kept in agreement with the legacy
    ``scope_ids`` / ``active_scope_type_ids`` the model declares (CONTRACT.md §2).

    At construction the picks become ``fold_legacy_selection(legacy fields, context_picks)`` and each
    legacy field becomes what the body sent, then the ids only the picks name, so a legacy body's
    legacy fields are byte-identical. After construction every write goes through
    :func:`set_request_selection`."""

    context_picks: list[ContextPick] | None = Field(
        default=None,
        description=(
            "The context of this call: picked tables, records and fields, possibly across organizations. "
            "Read together with scope_ids and active_scope_type_ids, which it supersedes."
        ),
    )

    @model_validator(mode="after")
    def _carry_context_picks(self) -> CarriesContextPicks:
        fields = type(self).model_fields
        sent = {name: getattr(self, name, None) for name in _LEGACY_FIELDS if name in fields}
        picks = fold_legacy_selection(
            sent.get("scope_ids"), sent.get("active_scope_type_ids"), self.context_picks
        )
        # Derived picks are not "sent": a legacy body's exclude_unset dump stays what it sent; ids
        # only the sent picks name do count as sent in the legacy fields.
        sent_picks = "context_picks" in self.__pydantic_fields_set__
        _write_selection(self, picks, sent, mark_set=sent_picks)
        return self


def set_request_selection[R: BaseModel](
    request: R,
    picks: Iterable[PickInput] | None,
    *,
    scope_ids: object = None,
    active_scope_type_ids: object = None,
) -> R:
    """THE one write of a request's selection after construction: ``context_picks`` and both legacy
    fields together. ``scope_ids`` / ``active_scope_type_ids`` are legacy values the caller holds
    (kept byte for byte, as the validator keeps a body's); the picks' own ids are appended. Returns
    the request, or a copy of a frozen one."""
    canonical = fold_legacy_selection(scope_ids, active_scope_type_ids, picks)
    sent = {"scope_ids": scope_ids, "active_scope_type_ids": active_scope_type_ids}
    return _write_selection(request, canonical, sent, mark_set=True)  # type: ignore[return-value]


__all__ = [
    "CarriesContextPicks",
    "ContextPick",
    "LegacySelection",
    "PickInput",
    "canonical_picks",
    "fold_legacy_selection",
    "legacy_ids_kept",
    "legacy_selection",
    "set_request_selection",
]
