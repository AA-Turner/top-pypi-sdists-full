"""
DataRef — universal system-table data references for LLM context injection.

A DataRef is a small JSON object the frontend generates to describe "attach
this data to the message".  The backend resolves it, fetches from the DB, and
renders the result as XML that the model can read and act on.

Three ref types:
  db_record  — one full row by primary key
  db_query   — multiple rows with optional filter / field projection / sort / limit
  db_field   — a single field value from one row

The allowlist (ALLOWED_TABLES) controls which tables React devs may reference.
It is intentionally a plain dict so it can be moved to the database later
without changing the resolution logic.  Each entry declares:
  - fields_allowed : list[str] | None   — None means "all fields" for OUTPUT
    projection ONLY; sort/filter/field-name access is REFUSED without an
    explicit allowlist (fail-closed — see _require_field_allowlist)
  - label          : str                — human-readable name for XML context
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Annotated, Any, Literal

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field, field_validator

# ---------------------------------------------------------------------------
# Allowlist — tables React devs may reference.
# fields_allowed=None means the full row is permitted.
# Add new tables here; move to DB later.
# ---------------------------------------------------------------------------


@dataclass
class _TableSpec:
    label: str
    table_name: str | None = (
        None  # physical schema-qualified table; None = same as the allowlist key
    )
    # None = all fields returned on OUTPUT, but sort/filter/field-ref REFUSED
    # (fail-closed, #13). Register an explicit list to enable query shaping.
    fields_allowed: list[str] | None = None
    model_key: str = ""  # host-injected ORM model name (matrx_ai.db._registry)


# Keys match the frontend DataRefTable allowlist (notes/tasks/projects/organizations);
# `table_name` is the physical schema-qualified table after the 2026 schema reorg
# (notes -> workbench, tasks/projects -> workspace). The key stays the FE-facing
# display name; table_name is what hits the SQL.
ALLOWED_TABLES: dict[str, _TableSpec] = {
    # Core user content
    "notes": _TableSpec(
        label="Note",
        table_name="workbench.notes",
        model_key="Notes",
        fields_allowed=[
            "id",
            "label",
            "content",
            "folder_name",
            "tags",
            "visibility",
            "created_at",
            "updated_at",
        ],
    ),
    "tasks": _TableSpec(
        label="Task",
        table_name="workspace.tasks",
        model_key="Tasks",
        fields_allowed=[
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "project_id",
            "parent_task_id",
            "assignee_id",
            "visibility",
            "created_at",
            "updated_at",
        ],
    ),
    # Projects
    "projects": _TableSpec(
        label="Project",
        table_name="workspace.projects",
        model_key="Projects",
        fields_allowed=[
            "id",
            "name",
            "description",
            "status",
            "organization_id",
            "created_at",
            "updated_at",
        ],
    ),
    "organizations": _TableSpec(
        label="Organization",
        table_name="iam.organizations",
        model_key="Organizations",
        fields_allowed=["id", "name", "description", "created_at", "updated_at"],
    ),
}


def _require_field_allowlist(spec: _TableSpec, table: str, usage: str) -> list[str]:
    """FAIL-CLOSED default (review #13): ``fields_allowed=None`` means "all fields
    project on output", but it must NEVER waive the sort/filter/field-name
    allowlist — those names reach the query builder (order_by interpolates the
    sort term verbatim), so an unlisted table would silently reopen the
    injection surface. A table that wants query-shaping MUST register an
    explicit ``fields_allowed`` list.
    """
    if spec.fields_allowed is None:
        raise ValueError(
            f"DataRef REFUSED: table {table!r} is registered without an explicit "
            f"fields_allowed allowlist, so {usage} by arbitrary fields is not "
            "permitted (fail-closed). Fix: declare fields_allowed on its "
            "_TableSpec in ALLOWED_TABLES."
        )
    return spec.fields_allowed


def _check_table(table: str) -> _TableSpec:
    spec = ALLOWED_TABLES.get(table)
    if spec is None:
        allowed = ", ".join(sorted(ALLOWED_TABLES))
        raise ValueError(
            f"Table {table!r} is not in the DataRef allowlist. Allowed tables: {allowed}"
        )
    return spec


def _filter_fields(
    row: dict[str, Any], fields_allowed: list[str] | None, requested: list[str] | None
) -> dict[str, Any]:
    """Return only fields that are (a) in the allowlist and (b) requested by the caller."""
    if fields_allowed is not None:
        row = {k: v for k, v in row.items() if k in fields_allowed}
    if requested:
        row = {k: v for k, v in row.items() if k in requested}
    return row


# ---------------------------------------------------------------------------
# DataRef dataclasses — the three wire shapes
# ---------------------------------------------------------------------------


NonEmptyString = Annotated[str, Field(min_length=1)]
DataRefTable = Literal["notes", "tasks", "projects", "organizations"]


class _DataRefBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table: DataRefTable
    label: str = ""
    optional_context: bool = False

    @field_validator("table")
    @classmethod
    def _table_must_be_registered(cls, value: str) -> str:
        _check_table(value)
        return value


class DbRecordRef(_DataRefBase):
    """Fetch one full row from a system table by primary key."""

    ref_type: Literal["db_record"]
    id: NonEmptyString
    fields: list[str] | None = None  # None = all allowed fields

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DbRecordRef:
        return cls.model_validate(d)


class DataRefSort(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: NonEmptyString
    direction: Literal["asc", "desc"] = "asc"


class DbQueryRef(_DataRefBase):
    """Fetch multiple rows from a system table with optional filters."""

    ref_type: Literal["db_query"]
    filter: dict[str, Any] = Field(default_factory=dict)
    fields: list[str] | None = None  # None = all allowed fields
    sort: DataRefSort | None = None
    limit: int = Field(default=50, ge=1, le=1000)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DbQueryRef:
        return cls.model_validate(d)


class DbFieldRef(_DataRefBase):
    """Fetch a single field value from one row of a system table."""

    ref_type: Literal["db_field"]
    id: NonEmptyString
    field_name: NonEmptyString

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DbFieldRef:
        return cls.model_validate(d)


DataRef = Annotated[DbRecordRef | DbQueryRef | DbFieldRef, Field(discriminator="ref_type")]


def parse_data_ref(d: dict[str, Any]) -> DataRef:
    ref_type = d.get("ref_type", "")
    if ref_type == "db_record":
        return DbRecordRef.from_dict(d)
    if ref_type == "db_query":
        return DbQueryRef.from_dict(d)
    if ref_type == "db_field":
        return DbFieldRef.from_dict(d)
    raise ValueError(
        f"Unknown DataRef ref_type {ref_type!r}. Expected: db_record, db_query, db_field"
    )


# ---------------------------------------------------------------------------
# DB fetch helpers — host-injected ORM models (matrx_ai.db._registry)
# ---------------------------------------------------------------------------


def _get_model(spec: _TableSpec) -> Any:
    from matrx_ai.db._registry import get_model

    if not spec.model_key:
        raise ValueError(f"DataRef table spec for {spec.label!r} has no model_key configured")
    return get_model(spec.model_key)


async def _fetch_row(spec: _TableSpec, row_id: str) -> dict[str, Any] | None:
    rows = await _get_model(spec).filter(id=row_id).limit(1).values()
    return rows[0] if rows else None


async def _fetch_rows(
    spec: _TableSpec,
    filter_: dict[str, Any],
    sort: DataRefSort | None,
    limit: int,
) -> list[dict[str, Any]]:
    order_term: str | None = None
    if sort:
        sort_field = sort.field
        # sort.field comes from the frontend — allowlist it like filter keys
        # (order_by interpolates the term verbatim; never pass it unchecked).
        # fields_allowed=None does NOT bypass this check — it refuses (#13).
        # Validated BEFORE any DB/model access so the guard can never be
        # masked by an unconfigured registry.
        allowed = _require_field_allowlist(spec, spec.label, "sorting")
        if sort_field not in allowed:
            raise ValueError(
                f"Sort field {sort_field!r} is not in the allowlist for {spec.label!r}. "
                f"Allowed: {allowed}"
            )
        prefix = "-" if sort.direction == "desc" else ""
        order_term = f"{prefix}{sort_field}"
    qb = _get_model(spec).filter(**filter_)
    if order_term is not None:
        qb = qb.order_by(order_term)
    return await qb.limit(int(limit)).values()


# ---------------------------------------------------------------------------
# XML renderers
# ---------------------------------------------------------------------------


def _record_to_xml(
    row: dict[str, Any] | None,
    table: str,
    row_id: str,
    label: str,
) -> str:
    display_label = label or ALLOWED_TABLES.get(table, _TableSpec(table)).label
    if row is None:
        return (
            f"<record table={json.dumps(table)} label={json.dumps(display_label)} "
            f'id={json.dumps(row_id)} found="false"/>'
        )
    attrs = f"table={json.dumps(table)} label={json.dumps(display_label)} id={json.dumps(row_id)}"
    lines = [f"<record {attrs}>"]
    for k, v in row.items():
        if v is not None:
            lines.append(f"  <{k}>{v}</{k}>")
    lines.append("</record>")
    return "\n".join(lines)


def _rows_to_xml(
    rows: list[dict[str, Any]],
    table: str,
    label: str,
) -> str:
    display_label = label or ALLOWED_TABLES.get(table, _TableSpec(table)).label
    attrs = f'table={json.dumps(table)} label={json.dumps(display_label)} count="{len(rows)}"'
    lines = [f"<records {attrs}>"]
    for row in rows:
        row_id = str(row.get("id", ""))
        lines.append(f"  <row id={json.dumps(row_id)}>")
        for k, v in row.items():
            if k != "id" and v is not None:
                lines.append(f"    <{k}>{v}</{k}>")
        lines.append("  </row>")
    lines.append("</records>")
    return "\n".join(lines)


def _field_to_xml(
    value: Any,
    table: str,
    row_id: str,
    field_name: str,
    label: str,
) -> str:
    display_label = label or field_name
    if value is None:
        return (
            f"<field table={json.dumps(table)} record_id={json.dumps(row_id)} "
            f'name={json.dumps(field_name)} label={json.dumps(display_label)} found="false"/>'
        )
    return (
        f"<field table={json.dumps(table)} record_id={json.dumps(row_id)} "
        f"name={json.dumps(field_name)} label={json.dumps(display_label)}>{value}</field>"
    )


# ---------------------------------------------------------------------------
# Public resolution — called by the structured input resolver
# ---------------------------------------------------------------------------


async def resolve_data_ref(ref: DataRef) -> str | None:
    """
    Fetch data for one DataRef and return it as an XML string.
    Returns None if the row/field is not found (caller decides whether to
    surface the error based on optional_context).
    Raises ValueError for allowlist violations or malformed refs.
    """
    if isinstance(ref, DbRecordRef):
        if not ref.table or not ref.id:
            raise ValueError("db_record ref requires 'table' and 'id'")
        spec = _check_table(ref.table)
        row = await _fetch_row(spec, ref.id)
        if row is not None:
            row = _filter_fields(row, spec.fields_allowed, ref.fields)
        return _record_to_xml(row, ref.table, ref.id, ref.label or spec.label)

    if isinstance(ref, DbQueryRef):
        if not ref.table:
            raise ValueError("db_query ref requires 'table'")
        spec = _check_table(ref.table)
        # Validate filter keys against the allowlist. fields_allowed=None does
        # NOT bypass this — filtering is refused for unlisted tables (#13).
        if ref.filter:
            allowed = _require_field_allowlist(spec, ref.table, "filtering")
            bad = [k for k in ref.filter if k not in allowed]
            if bad:
                raise ValueError(
                    f"Filter keys {bad} are not in the allowlist for table {ref.table!r}"
                )
        rows = await _fetch_rows(spec, ref.filter, ref.sort, ref.limit)
        rows = [_filter_fields(r, spec.fields_allowed, ref.fields) for r in rows]
        return _rows_to_xml(rows, ref.table, ref.label or spec.label)

    if isinstance(ref, DbFieldRef):
        if not ref.table or not ref.id or not ref.field_name:
            raise ValueError("db_field ref requires 'table', 'id', and 'field_name'")
        spec = _check_table(ref.table)
        # fields_allowed=None does NOT bypass the field-name check — refused (#13).
        allowed = _require_field_allowlist(spec, ref.table, "field access")
        if ref.field_name not in allowed:
            raise ValueError(
                f"Field {ref.field_name!r} is not in the allowlist for table {ref.table!r}. "
                f"Allowed: {allowed}"
            )
        row = await _fetch_row(spec, ref.id)
        value = row.get(ref.field_name) if row else None
        return _field_to_xml(value, ref.table, ref.id, ref.field_name, ref.label)

    raise ValueError(f"Unknown DataRef type: {type(ref)}")


async def resolve_data_refs(refs: list[dict[str, Any]]) -> tuple[str, list[str]]:
    """
    Resolve a list of raw DataRef dicts (as sent from the frontend).
    Returns (xml_block, errors).

    xml_block: all resolved refs wrapped in <data_context>...</data_context>,
               or empty string if nothing resolved.
    errors:    list of error strings for any refs that failed.
    """
    parts: list[str] = []
    errors: list[str] = []

    for raw in refs:
        try:
            ref = parse_data_ref(raw)
            xml = await resolve_data_ref(ref)
            if xml:
                parts.append(xml)
        except Exception as exc:
            optional = raw.get("optional_context", False)
            msg = f"DataRef resolution failed for {raw.get('ref_type', '?')}:{raw.get('table', '?')} — {exc}"
            vcprint(f"[DataRef] {msg}", color="yellow" if optional else "red")
            if not optional:
                errors.append(msg)

    if not parts:
        return "", errors

    xml_block = "<data_context>\n\n" + "\n\n".join(parts) + "\n\n</data_context>"
    return xml_block, errors
