from __future__ import annotations

import logging
import time
from typing import Any

from matrx_utils import vcprint
from pydantic import ValidationError
from pydantic_core import to_jsonable_python

from matrx_ai.db.ownership_fields import stamp_row_owner
from matrx_ai.tools import db_hints as _db_hints
from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models.db_args import (
    DbInsertArgs,
    DbQueryArgs,
    DbSchemaArgs,
    DbUpdateArgs,
    SqlArgs,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)


def _get_database_name() -> str:
    """The registered matrx-orm database/project name backing the host's
    generated model set. Every generated host Model carries the same
    ``_database`` class attribute (see ``BASE_CLASS_METHODS.md`` — the
    ``call_function`` example reads it off an arbitrary Model the same way),
    so borrow one from the injection registry rather than hardcoding it or
    reaching into aidream settings (forbidden — package boundary)."""
    from matrx_ai.db._registry import get_model as get_db_model

    return get_db_model("Definition")._database


# Exact relations that are never writable through the generic database tool.
BLOCKED_RELATIONS = {
    "chat.conversation",
    "chat.message",
    "chat.user_request",
    "chat.request",
}
# Read-only tables, schema-qualified (a bare name is ambiguous across schemas now).
# agent.definition is the canonical agent table (was prompt_builtins).
READ_ONLY_TABLES = {"agent.definition"}

# Schemas that are NOT application data. Excluded from `schema` discovery and
# blocked for writes. `graveyard` holds retired tables (reachable only by an
# explicit `graveyard.x` reference, never listed). Everything NOT in here is a
# real app schema the agent may read AND write (PostgREST exposes them all).
_NON_APP_SCHEMAS: frozenset[str] = frozenset(
    {
        "pg_catalog",
        "information_schema",
        "pg_toast",
        "auth",
        "storage",
        "vault",
        "pgsodium",
        "realtime",
        "cron",
        "net",
        "extensions",
        "graphql",
        "graphql_public",
        "supabase_migrations",
        "supabase_functions",
        "pgbouncer",
        "_analytics",
        "_realtime",
        "graveyard",
    }
)

# Schemas that ARE real application data (readable, discoverable) but whose
# writes MUST go through a governed service instead of this raw tool.
#
# `crm`: every `crm.party` row needs name-key canonicalization, natural-key
# dedup (lowercase email / E.164 phone / domain / external id), `source`
# stamping, and merge-lineage awareness. A raw INSERT here is a duplicate
# factory — the exact "jerry-rigged mess" the CRM design forbids. The governed
# paths exist since Wave 1 (2026-08-12): the aidream party resolver
# (aidream/services/crm/), the `party` agent_data resource, and the
# `resolve_contact` data_action. The guard STAYS anyway — a raw INSERT still
# skips the resolver, and the other crm tables have no governed path yet.
WRITE_GOVERNED_SCHEMAS: frozenset[str] = frozenset({"crm"})

_WRITE_GOVERNED_REASON: dict[str, str] = {
    "crm": (
        "CRM rows must be created through the governed party path (find-or-create "
        "with canonicalization, dedup and source stamping), not a raw insert. "
        "A raw write here creates duplicate parties that the merge system then "
        "has to clean up."
    ),
}

MAX_QUERY_TIMEOUT = 10


def _json_safe(value: Any) -> Any:
    return to_jsonable_python(value, serialize_unknown=True, fallback=str)


def _write_output(verb: str, rows: Any, returning: str) -> dict[str, Any]:
    """Shape a write result. ``full`` (default) echoes the affected rows;
    ``minimal`` returns only the generated id(s) — keeps large rows (e.g.
    ai_model's jsonb columns) out of the model context."""
    rows = _json_safe(rows or [])
    count = len(rows) if isinstance(rows, list) else 0
    if returning == "minimal":
        ids = [r.get("id") for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []
        return {verb: count, "ids": ids}
    return {verb: count, "data": rows}


def _announce_corrections(
    tool: str, corrections: list[str], output: dict[str, Any]
) -> dict[str, Any]:
    """Put vocabulary corrections in the tool result AND the server log.
    An automatic intervention that nobody is told about is indistinguishable
    from corrupt data landing quietly."""
    if not corrections:
        return output
    for note in corrections:
        vcprint(f"[{tool}] capability vocabulary corrected: {note}", color="yellow")
    return {**output, "vocabulary_corrections": corrections}


def _split_schema_table(table: str) -> tuple[str | None, str]:
    """Split a (possibly schema-qualified) reference into (schema|None, table).

    ``"chat.message"`` -> ``("chat", "message")`` · ``"content_blocks"`` ->
    ``(None, "content_blocks")``. Identifiers are lower-cased and de-quoted.
    """
    raw = (table or "").strip().strip('"').strip("'")
    if "." in raw:
        schema, _, name = raw.partition(".")
        schema = schema.strip().strip('"').strip().lower()
        name = name.strip().strip('"').strip().lower()
        return (schema or None), name
    return None, raw.lower()


# Process-level caches. Schema layout / column sets rarely change within a
# process; a new migration is picked up on the next restart.
_APP_SCHEMAS_CACHE: list[str] | None = None
_TABLE_COLUMNS_CACHE: dict[str, frozenset[str]] = {}  # "schema.table" -> column names
_TABLES_BY_SCHEMA_CACHE: dict[str, list[str]] | None = None  # schema -> [table names]


def _str_rows(rows: list[Any], key: str) -> list[str]:
    return [r[key] for r in rows if isinstance(r, dict) and r.get(key)]


async def _app_schemas() -> list[str]:
    """Every application schema (all non-system schemas), discovered live."""
    global _APP_SCHEMAS_CACHE
    if _APP_SCHEMAS_CACHE is not None:
        return _APP_SCHEMAS_CACHE
    from matrx_orm.catalog import application_schemas

    schemas = await application_schemas(
        _get_database_name(), exclude_schemas=sorted(_NON_APP_SCHEMAS)
    )
    if schemas:
        _APP_SCHEMAS_CACHE = schemas
    return schemas


async def _schemas_for_table(name: str) -> list[str]:
    """Discover every application schema containing the requested relation name.

    Bare input is supported only as a discovery request. It is deliberately not
    cached: a bare table name is not a stable identity and must never become a
    process key.
    """
    from matrx_orm.catalog import relation_schemas

    return await relation_schemas(
        _get_database_name(),
        table=name,
        exclude_schemas=sorted(_NON_APP_SCHEMAS),
    )


async def _resolve_table(table: str) -> tuple[str | None, str, list[str]]:
    """Resolve a reference to ``(schema, table, candidates)``.

    * schema-qualified (``chat.message``) → that exact (schema, name).
    * bare name in exactly one schema → that schema.
    * bare name in multiple schemas → ``(None, name, [qualified...])``.
    * bare name in no schema → ``(None, name, [])``.
    """
    schema, name = _split_schema_table(table)
    if schema is not None:
        return schema, name, []
    schemas = await _schemas_for_table(name)
    if len(schemas) == 1:
        return schemas[0], name, []
    if not schemas:
        return None, name, []
    return None, name, [f"{s}.{name}" for s in schemas]


def _is_blocked_table(table: str) -> bool:
    schema, name = _split_schema_table(table)
    if schema is None:
        raise ValueError(f"blocked-table guard requires schema.table, got {table!r}")
    if f"{schema}.{name}" in BLOCKED_RELATIONS:
        return True
    if schema is not None and schema in _NON_APP_SCHEMAS:
        return True
    return False


def _is_read_only(schema: str, name: str) -> bool:
    return f"{schema}.{name}" in READ_ONLY_TABLES


async def _get_table_columns(schema: str, name: str) -> frozenset[str]:
    key = f"{schema}.{name}"
    cached = _TABLE_COLUMNS_CACHE.get(key)
    if cached is not None:
        return cached

    from matrx_orm.catalog import describe_relation_columns

    rows = await describe_relation_columns(_get_database_name(), schema=schema, table=name)

    columns = frozenset(_str_rows(rows, "column_name"))
    # Only cache a positive result. An empty set means either the table
    # doesn't exist or the lookup raced/failed — don't poison the cache so a
    # real table gets a clean retry on the next write.
    if columns:
        _TABLE_COLUMNS_CACHE[key] = columns
    return columns


async def _tables_by_schema() -> dict[str, list[str]]:
    """Every app table grouped by schema — the hint/auto-heal vocabulary.
    Positive-only cache, same convention as the caches above."""
    global _TABLES_BY_SCHEMA_CACHE
    if _TABLES_BY_SCHEMA_CACHE is not None:
        return _TABLES_BY_SCHEMA_CACHE
    grouped = (await _list_tables(only_schema=None)).get("schemas") or {}
    if grouped:
        _TABLES_BY_SCHEMA_CACHE = grouped
    return grouped


def _instance_to_dict(instance: Any) -> dict[str, Any]:
    """Arbitrary (runtime-resolved) Model instance -> plain dict, PostgREST-
    compatible shape (ISO-8601 datetimes, string UUIDs), for tables whose
    columns aren't known until the agent names them at call time."""
    from datetime import datetime
    from uuid import UUID as _UUID

    out: dict[str, Any] = {}
    for name in instance._fields:
        value = getattr(instance, name, None)
        if isinstance(value, datetime):
            out[name] = value.isoformat()
        elif isinstance(value, _UUID):
            out[name] = str(value)
        else:
            out[name] = value
    return out


def _resolve_write_model(schema: str, name: str) -> Any:
    """The registered matrx-orm Model for a runtime-resolved ``(schema, name)``
    write target — the sanctioned "table name known only at runtime" lookup
    (BASE_CLASS_METHODS.md) instead of a raw PostgREST ``.table()`` builder.
    Raises ``ValueError`` (caught by every caller's existing except-block and
    turned into the same "table not found" style message) if the table has no
    generated ORM model yet — e.g. a brand new table before the next
    ``db/generate.py`` run."""
    from matrx_orm import get_model_by_table_name

    return get_model_by_table_name(schema, name)


async def _stamp_auto_fields(schema: str, name: str, rows: list[Any], ctx: ToolContext) -> None:
    """Schema-aware identity stamping: set ownership on every write row for columns
    the table actually owns. Prefers ``created_by``; keeps ``user_id`` on dual-
    column tables until the DB contract phase drops it."""
    try:
        columns = await _get_table_columns(schema, name)
    except Exception as exc:  # schema lookup is best-effort
        logger.warning(
            "Column lookup failed for table %r; falling back to stamping all auto fields: %s",
            f"{schema}.{name}",
            exc,
        )
        columns = None

    if columns is not None and not columns:
        columns = None

    owner_id = getattr(ctx, "user_id", None)
    if not owner_id:
        return

    for row in rows:
        if isinstance(row, dict):
            stamp_row_owner(row, owner_id, table_columns=columns)


#: Tables the server's in-memory AI catalog is built from. A successful write
#: to any of them (through this tool) notifies the host so it can reload the
#: catalog — otherwise a synced model is not callable until a human reloads.
AI_CATALOG_TABLES: frozenset[str] = frozenset(
    {
        "ai.provider",
        "ai.model_definition",
        "ai.endpoint",
        "ai.api",
        "ai.offering",
        "ai.setting",
        "ai.model_alias",
        "ai.voices",
    }
)


def _after_catalog_write(schema: str | None, name: str, verb: str) -> None:
    """Tell the host a catalog table changed. Never raises, never blocks."""
    if not schema or f"{schema}.{name}" not in AI_CATALOG_TABLES:
        return
    try:
        from matrx_ai._ext import get_ai_catalog_write_hook

        hook = get_ai_catalog_write_hook()
        if hook is None:
            vcprint(
                f"[sql] {verb} on {schema}.{name} changed the AI catalog but no host "
                "reload hook is registered — the server will keep serving the OLD "
                "catalog until POST /api/admin/ai-catalog/reload runs.",
                color="yellow",
            )
            return
        hook(schema, name, verb)
    except Exception as exc:  # noqa: BLE001 — a reload request must never fail a write
        vcprint(f"[sql] catalog write hook raised (ignored): {exc}", color="yellow")


#: Catalog columns whose VALUE has a canonical vocabulary, and the validator
#: that owns it. The generic sql/db_* tools are how the model-sync agent writes
#: the catalog, so this is the choke point every agent write passes through.
#: Before this existed, provider-doc spellings ("structured_outputs",
#: "reasoning", "code_interpreter", "batch", "pdf_input") landed verbatim in
#: ai.model_definition.capabilities and silently turned capabilities OFF —
#: `_structured_mode` matches the literal "structured_output", so gpt-6-astra
#: resolved to TEXT mode with schema output declared (2026-09-12).
_VOCABULARY_GUARDED_COLUMNS: dict[str, tuple[str, ...]] = {
    "ai.model_definition": ("capabilities",),
}

_CATALOG_RULE_COLUMNS: dict[str, str] = {
    "ai.api": "rules",
    "ai.offering": "override",
}


def _guard_catalog_rules(schema: str | None, name: str, rows: list[Any]) -> str | None:
    """Refuse catalog rules that the compiler would otherwise quarantine."""
    column = _CATALOG_RULE_COLUMNS.get(f"{schema}.{name}")
    if column is None:
        return None

    from matrx_ai.catalog.models import RulesEnvelope

    for row in rows:
        if not isinstance(row, dict) or column not in row or row[column] is None:
            continue
        try:
            RulesEnvelope.model_validate(row[column])
        except ValidationError as exc:
            label = str(row.get("id") or row.get("name") or "submitted row")
            return (
                f"Catalog rule write refused for {schema}.{name} {label}: {exc}. "
                "Fix the full rules envelope before retrying; a processor cannot coexist "
                "with value_map or const."
            )
    return None


def _guard_vocabulary(
    schema: str | None, name: str, rows: list[Any]
) -> tuple[str | None, list[str]]:
    """Canonicalize and validate vocabulary-owned columns on a write payload.

    Aliases are rewritten IN PLACE and returned as ``corrections`` for the
    caller to announce — a silent correction is the same bug as a silent drop.
    A value nobody has a word for returns an error message: the write is
    refused with the fix spelled out, never accepted and half-honoured.
    """
    columns = _VOCABULARY_GUARDED_COLUMNS.get(f"{schema}.{name}")
    if not columns:
        return None, []

    from matrx_ai.providers.capability_vocabulary import normalize_capabilities

    corrections: list[str] = []
    rejections: list[str] = []
    replacements: list[tuple[dict[str, Any], str, dict[str, Any]]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        for column in columns:
            if column not in row or row[column] is None:
                continue
            label = str(row.get("name") or row.get("id") or "")
            result = normalize_capabilities(row[column], label=label)
            corrections.extend(result.corrections)
            if result.ok:
                replacements.append((row, column, result.value))
            else:
                rejections.append(result.rejection_message())

    if rejections:
        # The enclosing write is refused. Do not leave an in-memory batch
        # partly canonicalized: callers must be able to correct and retry the
        # exact payload they supplied, and every announced correction must
        # correspond to a value that will actually be written.
        return " | ".join(dict.fromkeys(rejections)), []
    for row, column, value in replacements:
        row[column] = value
    return None, corrections


def _orm_lookups(match: dict[str, Any]) -> dict[str, Any]:
    """Translate the tool's ``match`` into ORM lookup kwargs.

    The read path already treats a LIST value as IN (``match_filters``); the
    write paths passed ``match`` straight to ``update_where``/``delete_where``,
    which bound the list as one uuid and failed ("invalid input syntax for type
    uuid: ['…', '…']"). Same contract everywhere: scalar = equality, list =
    ``field__in``, None = IS NULL (``field__isnull``).
    """
    out: dict[str, Any] = {}
    for field, value in match.items():
        if isinstance(value, (list, tuple)):
            out[f"{field}__in"] = list(value)
        elif value is None:
            out[f"{field}__isnull"] = True
        else:
            out[field] = value
    return out


def match_filters(match: dict[str, Any]) -> tuple[Any, ...]:
    """Translate the ``sql`` tool's ``match`` object into typed ORM filters.

    * scalar value → ``eq``
    * ``None``     → ``isnull``
    * list / tuple → ``in`` (one query for many ids — the shape that lets an
      agent read "the offerings for THESE models" in one call instead of one
      call per model, or an unfiltered dump of the whole table).

    Shared by the super-admin path here and the host's RLS runner
    (``aidream/db/scoped_sql.py``) so both paths accept the same ``match``.
    """
    from matrx_orm.operations.dynamic_crud import DynamicFilter

    filters: list[Any] = []
    for field, value in match.items():
        if isinstance(value, (list, tuple)):
            filters.append(DynamicFilter(field=field, operator="in", value=list(value)))
        elif value is None:
            filters.append(DynamicFilter(field=field, operator="isnull", value=True))
        else:
            filters.append(DynamicFilter(field=field, value=value))
    return tuple(filters)


async def db_query(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = DbQueryArgs(**args)

    try:
        from matrx_orm.operations.dynamic_crud import dynamic_select

        rows = await dynamic_select(
            parsed.table,
            filters=match_filters(parsed.match),
            columns=tuple(parsed.fields),
            order_by=tuple(parsed.order_by),
            limit=parsed.limit,
            offset=parsed.offset,
            database=_get_database_name(),
        )

        return ToolResult(
            success=True,
            output={
                "rows": _json_safe(rows),
                "count": len(rows),
            },
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_query",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        message, suggested = await _agent_db_error(exc)
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type=_structured_query_error_type(exc),
                message=f"Query failed. {message}",
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_query",
            call_id=ctx.call_id,
        )


async def _resolve_write_target(
    table: str,
) -> tuple[str | None, str | None, str | None, str | None]:
    """Resolve + authorize a write target. Returns ``(schema, name, error_type, message)``;
    on success ``error_type`` is ``None``. Works across every exposed schema."""
    raw = (table or "").strip()
    if not raw:
        return None, None, "validation", "table is required."
    schema, name, candidates = await _resolve_table(raw)
    if schema is None:
        if candidates:
            return (
                None,
                None,
                "validation",
                (
                    f"Table '{raw}' exists in multiple schemas; qualify it as schema.table "
                    f"(e.g. {candidates[0]!r}). Candidates: {candidates}."
                ),
            )
        return None, None, "validation", f"Table '{raw}' was not found in any exposed schema."
    if schema in WRITE_GOVERNED_SCHEMAS:
        return (
            None,
            None,
            "permission",
            (
                f"Table '{schema}.{name}' is read-only for this tool. "
                f"{_WRITE_GOVERNED_REASON.get(schema, '')}"
            ).strip(),
        )
    if _is_blocked_table(f"{schema}.{name}"):
        return None, None, "permission", f"Table '{schema}.{name}' is blocked for direct writes."
    if _is_read_only(schema, name):
        return None, None, "permission", f"Table '{schema}.{name}' is read-only."
    return schema, name, None, None


async def db_insert(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = DbInsertArgs(**args)

    schema, name, err_type, err_msg = await _resolve_write_target(parsed.table)
    if err_type:
        return ToolResult(
            success=False,
            error=ToolError(error_type=err_type, message=err_msg or ""),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_insert",
            call_id=ctx.call_id,
        )

    try:
        data = parsed.data if isinstance(parsed.data, list) else [parsed.data]
        rules_error = _guard_catalog_rules(schema, name, data)
        if rules_error:
            return ToolResult(
                success=False,
                error=ToolError(error_type="validation", message=rules_error),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="db_insert",
                call_id=ctx.call_id,
            )
        vocab_error, corrections = _guard_vocabulary(schema, name, data)
        if vocab_error:
            return ToolResult(
                success=False,
                error=ToolError(error_type="validation", message=f"Insert refused. {vocab_error}"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="db_insert",
                call_id=ctx.call_id,
            )
        await _stamp_auto_fields(schema, name, data, ctx)

        Model = _resolve_write_model(schema, name)
        created_rows = await Model.bulk_create(data)
        _after_catalog_write(schema, name, "insert")
        return ToolResult(
            success=True,
            output=_announce_corrections(
                "db_insert",
                corrections,
                _write_output(
                    "inserted", [_instance_to_dict(r) for r in created_rows], parsed.returning
                ),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_insert",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        message, suggested = await _agent_db_error(exc)
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="database",
                message=f"Insert failed. {message}",
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_insert",
            call_id=ctx.call_id,
        )


async def db_update(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = DbUpdateArgs(**args)

    schema, name, err_type, err_msg = await _resolve_write_target(parsed.table)
    if err_type:
        return ToolResult(
            success=False,
            error=ToolError(error_type=err_type, message=err_msg or ""),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_update",
            call_id=ctx.call_id,
        )

    try:
        update_data = dict(parsed.data)
        rules_error = _guard_catalog_rules(schema, name, [update_data])
        if rules_error:
            return ToolResult(
                success=False,
                error=ToolError(error_type="validation", message=rules_error),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="db_update",
                call_id=ctx.call_id,
            )
        vocab_error, corrections = _guard_vocabulary(schema, name, [update_data])
        if vocab_error:
            return ToolResult(
                success=False,
                error=ToolError(error_type="validation", message=f"Update refused. {vocab_error}"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="db_update",
                call_id=ctx.call_id,
            )
        Model = _resolve_write_model(schema, name)
        # update_where() is a single UPDATE statement with no RETURNING —
        # re-select by the same match filters afterward so the tool can still
        # echo the updated rows (PostgREST's `.update(...).execute()` did this
        # atomically; this is a fetch-after-write, same as the rest of this
        # file's dynamic write paths — see the ORM-gap note in the final report).
        lookups = _orm_lookups(parsed.match)
        await Model.update_where(lookups, **update_data)
        updated_rows = await Model.filter(**lookups).all()
        _after_catalog_write(schema, name, "update")

        return ToolResult(
            success=True,
            output=_announce_corrections(
                "db_update",
                corrections,
                _write_output(
                    "updated", [_instance_to_dict(r) for r in updated_rows], parsed.returning
                ),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_update",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        message, suggested = await _agent_db_error(exc)
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="database",
                message=f"Update failed. {message}",
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_update",
            call_id=ctx.call_id,
        )


async def _get_table_fks(schema: str, table: str) -> dict[str, list[str]]:
    """Compact FK relationships for a table, both directions:
    foreign_keys  -> 'local_col -> other_table.other_col'  (this table references X)
    referenced_by -> 'other_table.other_col_in_that_table -> local_col_here'
                     i.e. 'recipe_model.ai_model -> id'     (X references this table)
    """
    from matrx_orm.catalog import relation_foreign_key_columns

    rows = await relation_foreign_key_columns(_get_database_name(), schema=schema, table=table)
    foreign_keys: list[str] = []
    referenced_by: list[str] = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        if r.get("direction") == "out":
            foreign_keys.append(
                f"{r.get('local_col')} -> {r.get('other_table')}.{r.get('other_col')}"
            )
        else:
            referenced_by.append(
                f"{r.get('other_table')}.{r.get('local_col')} -> {r.get('other_col')}"
            )
    return {"foreign_keys": foreign_keys, "referenced_by": referenced_by}


async def _list_tables(only_schema: str | None) -> dict[str, Any]:
    """List base tables/views across every app schema, grouped + schema-qualified.

    ``only_schema`` narrows the listing to a single schema. The agent then calls
    ``schema`` again with a ``schema.table`` value to see that table's columns.
    """
    from matrx_orm.catalog import list_relations

    rows = await list_relations(
        _get_database_name(),
        schemas=[only_schema] if only_schema else None,
        exclude_schemas=None if only_schema else sorted(_NON_APP_SCHEMAS),
    )

    grouped: dict[str, list[str]] = {}
    total = 0
    for r in rows:
        if not isinstance(r, dict):
            continue
        sch = r.get("table_schema")
        tbl = r.get("table_name")
        if not sch or not tbl:
            continue
        grouped.setdefault(sch, []).append(tbl)
        total += 1

    return {
        "schemas": grouped,
        "schema_count": len(grouped),
        "total_tables": total,
        "note": (
            "Tables are grouped by schema and names are schema-qualified. "
            "To inspect one table's columns, call schema with a 'schema.table' "
            "value (e.g. 'chat.message')."
        ),
    }


async def db_schema(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = DbSchemaArgs(**args)

    try:
        # No `table` → list every app schema's tables, grouped + qualified.
        if not parsed.table:
            return ToolResult(
                success=True,
                output=await _list_tables(only_schema=None),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="db_schema",
                call_id=ctx.call_id,
            )

        requested = parsed.table.strip()
        # A bare token that names a schema (not a dotted ref) → list that schema.
        if "." not in requested and requested.lower() in set(await _app_schemas()):
            return ToolResult(
                success=True,
                output=await _list_tables(only_schema=requested.lower()),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="db_schema",
                call_id=ctx.call_id,
            )

        # Otherwise describe one table — resolving its schema across the DB.
        schema, name, candidates = await _resolve_table(requested)
        if schema is None:
            note = (
                f"'{requested}' exists in multiple schemas — call again with one of: {candidates}."
                if candidates
                else f"No table named '{requested}' was found in any exposed schema."
            )
            return ToolResult(
                success=True,
                output={
                    "table": requested,
                    "columns": [],
                    "ambiguous": bool(candidates),
                    "candidates": candidates,
                    "note": note,
                },
                started_at=started_at,
                completed_at=time.time(),
                tool_name="db_schema",
                call_id=ctx.call_id,
            )

        from matrx_orm.catalog import describe_relation_columns

        columns = await describe_relation_columns(_get_database_name(), schema=schema, table=name)

        # The bare `schema` key was dropped with the kind reshape — `table` is
        # already schema-qualified (KIND_TOOL_LEDGER, `sql_tool_result`).
        output: dict[str, Any] = {"table": f"{schema}.{name}", "columns": columns}
        # FK relationships are supplementary — never let a lookup failure
        # sink the core columns response. Surface the failure in the output
        # (and the log) rather than silently implying "no FKs".
        try:
            output.update(await _get_table_fks(schema, name))
        except Exception as fk_exc:
            logger.warning("FK lookup failed for table %r: %s", f"{schema}.{name}", fk_exc)
            output["foreign_keys"] = []
            output["referenced_by"] = []
            output["fk_lookup_error"] = {"message": str(fk_exc)}

        return ToolResult(
            success=True,
            output=output,
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_schema",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        message, suggested = await _agent_db_error(exc)
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="database",
                message=f"Schema query failed. {message}",
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="db_schema",
            call_id=ctx.call_id,
        )


# ---------------------------------------------------------------------------
# sql — unified action dispatcher (replaces db_query / db_insert / db_update / db_schema)
# Adds two new actions: delete, upsert.
# ---------------------------------------------------------------------------

# Valid `sql` actions are enforced by the SqlArgs discriminated union
# (arg_models/db_args.py) + tool_def.parameters."$variants" — the source of truth.


def _sql_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "sql"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _sql_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="sql",
        call_id=ctx.call_id,
    )


def _sql_permission_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="permission", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="sql",
        call_id=ctx.call_id,
    )


async def _sql_delete(args: dict[str, Any], ctx: ToolContext, started_at: float) -> ToolResult:
    table = (args.get("table") or "").strip()
    match = args.get("match") or {}
    if not table:
        return _sql_validation_error("table is required for action=delete.", started_at, ctx)
    if not isinstance(match, dict) or not match:
        return _sql_validation_error(
            "match must be a non-empty object of column=value filters for "
            "action=delete (refusing unbounded DELETE).",
            started_at,
            ctx,
        )
    schema, name, err_type, err_msg = await _resolve_write_target(table)
    if err_type == "permission":
        return _sql_permission_error(err_msg or "", started_at, ctx)
    if err_type:
        return _sql_validation_error(err_msg or "", started_at, ctx)

    try:
        Model = _resolve_write_model(schema, name)
        # No DELETE ... RETURNING primitive on the ORM yet — fetch the matched
        # rows first so the tool can still echo what it deleted (same
        # fetch-then-write shape as db_update above; see the ORM-gap note in
        # the final report). A concurrent writer racing between the two
        # statements is the same admin-bypass-RLS risk this whole tool already
        # carries by design.
        lookups = _orm_lookups(match)
        rows_to_delete = await Model.filter(**lookups).all()
        deleted_data = [_instance_to_dict(r) for r in rows_to_delete]
        deleted_count = await Model.delete_where(**lookups)
        _after_catalog_write(schema, name, "delete")
        return ToolResult(
            success=True,
            output={"deleted": deleted_count, "data": deleted_data},
            started_at=started_at,
            completed_at=time.time(),
            tool_name="sql",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        message, suggested = await _agent_db_error(exc)
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="database",
                message=f"Delete failed. {message}",
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="sql",
            call_id=ctx.call_id,
        )


async def _sql_upsert(args: dict[str, Any], ctx: ToolContext, started_at: float) -> ToolResult:
    table = (args.get("table") or "").strip()
    data = args.get("data")
    on_conflict = args.get("on_conflict")
    if not table:
        return _sql_validation_error("table is required for action=upsert.", started_at, ctx)
    if data is None:
        return _sql_validation_error(
            "data is required for action=upsert (object or list of objects).",
            started_at,
            ctx,
        )
    schema, name, err_type, err_msg = await _resolve_write_target(table)
    if err_type == "permission":
        return _sql_permission_error(err_msg or "", started_at, ctx)
    if err_type:
        return _sql_validation_error(err_msg or "", started_at, ctx)

    rows = data if isinstance(data, list) else [data]
    rules_error = _guard_catalog_rules(schema, name, rows)
    if rules_error:
        return _sql_validation_error(rules_error, started_at, ctx)
    vocab_error, corrections = _guard_vocabulary(schema, name, rows)
    if vocab_error:
        return _sql_validation_error(f"Upsert refused. {vocab_error}", started_at, ctx)
    await _stamp_auto_fields(schema, name, rows, ctx)
    returning = args.get("returning") or "full"

    try:
        Model = _resolve_write_model(schema, name)
        # PostgREST's own upsert defaults an unspecified conflict target to the
        # table's primary key — mirror that so callers that omit on_conflict
        # keep the same behavior.
        conflict_fields = (
            [c.strip() for c in on_conflict.split(",") if c.strip()]
            if on_conflict
            else list(Model._meta.primary_keys)
        )
        upserted_rows = await Model.bulk_upsert(rows, conflict_fields=conflict_fields)
        _after_catalog_write(schema, name, "upsert")
        return ToolResult(
            success=True,
            output=_announce_corrections(
                "sql",
                corrections,
                _write_output("upserted", [_instance_to_dict(r) for r in upserted_rows], returning),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="sql",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        message, suggested = await _agent_db_error(exc)
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="database",
                message=f"Upsert failed. {message}",
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="sql",
            call_id=ctx.call_id,
        )


SUPER_ADMIN = "super_admin"


def _current_admin_level() -> str | None:
    """The caller's admin tier from AppContext, or None. The executor's
    admin_only gate already guarantees SOME admin reached here; this decides
    which tier's authority the statement runs under."""
    try:
        from matrx_connect import get_app_context

        return getattr(get_app_context(), "admin_level", None)
    except Exception:
        return None


async def _agent_db_error(exc: Exception, query: str | None = None) -> tuple[str, str]:
    """Translate a raw DB exception into (message, suggested_action) written to
    an intelligent caller — say what happened and what to do next, never a bare
    Postgres error dict, and NEVER ``str(exc)`` on an ORM error (that is the
    ANSI developer banner). On a schema miss, attach what makes the next call
    succeed: did-you-mean tables, the schema's table list, or the real columns.
    """
    # Classification is by SQLSTATE / exception type ONLY. It used to be by
    # substring — `"policy" in text` — which reported an unknown column named
    # `sync_policy` as a permissions failure (2026-09-11 incident) and sent a
    # super-admin agent chasing access it already had.
    if _db_hints.is_read_only_error(exc):
        return (
            "The `query` action is read-only — it cannot modify data. To change "
            "data, use action 'insert' / 'update' / 'delete' / 'upsert' if you are "
            "a super_admin, or the `data` / `data_action` tools, which write under "
            "your own permissions.",
            "Re-issue the change as a write action, or use the `data` tools.",
        )
    if _db_hints.is_permission_error(exc):
        return (
            "That statement touched rows or tables your access level doesn't permit "
            "(Postgres SQLSTATE 42501 — insufficient privilege or a row-level-security "
            "policy denial). Non-super-admin database access runs under your own "
            "row-level-security permissions — you can only read/write what you own or "
            "have been granted. Broader access requires super_admin.",
            "Scope the query to data you own, or ask a super_admin if you need more.",
        )
    facts = _db_hints.parse_db_error(exc)
    return await _db_hints.build_hint(
        facts,
        query or "",
        app_schemas=_app_schemas,
        tables_by_schema=_tables_by_schema,
        schemas_for_table=_schemas_for_table,
        get_table_columns=_get_table_columns,
    )


def _structured_query_error_type(exc: Exception) -> str:
    """Separate caller-correctable query shape misses from DB failures.

    ``dynamic_select`` raises ``ValueError`` before I/O for an unregistered
    table, unknown field/filter/order key, or malformed table identity. ORM
    schema-mismatch exceptions expose the same classification through
    ``db_hints``. Those are feedback to the calling model, not production
    incidents. Connection, timeout, and server exceptions remain ``database``
    so the executor captures them for repair patrol.
    """
    if isinstance(exc, ValueError) or _db_hints.parse_db_error(exc).kind is not None:
        return "validation"
    return "database"


async def _resolve_read_target(table: str) -> tuple[str | None, str | None]:
    """Authorize a READ target. Returns ``(schema.table, error_message)``.

    Reads no longer require a registered ORM model (a live view is readable the
    moment it exists), so the schema guard that writes always had now applies to
    reads too: nothing outside an application schema is reachable through this
    tool. A bare name that exists in exactly one app schema is qualified here;
    anything unresolvable is handed back to the normal error/hint path, which
    knows how to say "did you mean".
    """
    raw = (table or "").strip()
    if not raw:
        return None, "table is required."
    schema, name = _split_schema_table(raw)
    if schema is None:
        schemas = await _schemas_for_table(name)
        if len(schemas) == 1:
            schema = schemas[0]
        elif len(schemas) > 1:
            return None, (
                f"Table '{raw}' exists in multiple schemas; qualify it as schema.table "
                f"(candidates: {[f'{s}.{name}' for s in schemas]})."
            )
        else:
            # Unknown name — let the query fail through the hint builder, which
            # produces did-you-mean suggestions instead of a flat refusal.
            return raw, None
    if schema in _NON_APP_SCHEMAS:
        return None, (
            f"Schema '{schema}' is not application data and is not readable through the `sql` tool."
        )
    return f"{schema}.{name}", None


async def _sql_query_scoped(
    inner_args: dict[str, Any], ctx: ToolContext, started_at: float, admin_level: str | None
) -> ToolResult:
    """Structured read path; non-super admins run under host-provided RLS."""
    from matrx_ai._ext import get_scoped_query_runner

    parsed = DbQueryArgs(**inner_args)
    qualified, read_error = await _resolve_read_target(parsed.table)
    if read_error:
        return _sql_permission_error(read_error, started_at, ctx)
    if qualified and qualified != parsed.table:
        inner_args = {**inner_args, "table": qualified}
        parsed = DbQueryArgs(**inner_args)
    runner = get_scoped_query_runner()
    if admin_level == SUPER_ADMIN:
        return _sql_stamp(await db_query(inner_args, ctx), started_at, ctx)
    if runner is None:
        return _sql_validation_error(
            "Structured database reads require a host-provided RLS query runner.",
            started_at,
            ctx,
        )
    try:
        rows = await runner(
            table=parsed.table,
            match=parsed.match,
            fields=parsed.fields,
            order_by=parsed.order_by,
            limit=parsed.limit,
            offset=parsed.offset,
        )
    except Exception as exc:
        message, suggested = await _agent_db_error(exc)
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,
                error_type="database",
                message=message,
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="sql",
            call_id=ctx.call_id,
        )
    return ToolResult(
        success=True,
        output={"rows": _json_safe(rows), "count": len(rows)},
        started_at=started_at,
        completed_at=time.time(),
        tool_name="sql",
        call_id=ctx.call_id,
    )


def _write_requires_super_admin(
    action: str, level: str | None, started_at: float, ctx: ToolContext
) -> ToolResult:
    """Human message when a non-super-admin attempts a raw write on the `sql`
    tool. Non-super-admin DB access is RLS-only — point them at the tools that
    already do exactly that under their own permissions."""
    who = level or "a non-super-admin"
    return _sql_permission_error(
        f"Raw table writes through the `sql` tool (action='{action}') require the "
        f"super_admin tier — you are {who}. This isn't a limit on the task, only on "
        f"this god-mode path: use the `data` and `data_action` tools instead, which "
        f"perform create / update / delete under your OWN permissions (row-level "
        f"security) — exactly the access your tier has. If the change genuinely needs "
        f"elevated privileges (another user's data, DDL, grants), it needs a "
        f"super_admin or a migration.",
        started_at,
        ctx,
    )


async def sql(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    # KindModel result (KIND_TOOL_LEDGER): one stamp funnel over every action
    # branch. Loud-not-fatal, the same posture as aidream/tools/_kind_stamp.py
    # (this package may not import aidream) — a payload the declared model
    # refuses is logged and returned UNSTAMPED so the executor's declared-kind
    # enforcement records the miss.
    from matrx_ai.tools.kind_stamp import stamp_result_kind
    from matrx_ai.tools.kinds.database_tools import SqlToolResult

    return stamp_result_kind(await _sql_impl(args, ctx), SqlToolResult)


async def _sql_impl(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    # The executor already validated `args` against SqlArgs (the discriminated
    # union) before dispatch; re-derive the typed variant so the body is bound to
    # the per-action contract the drift gate proves against the DB.
    try:
        parsed = SqlArgs.model_validate(args).root
    except ValidationError as exc:
        return _sql_validation_error(format_args_error(exc), started_at, ctx)

    action = parsed.action
    # exclude_unset: pass only the keys the caller actually sent (so worker
    # partial-update semantics are unchanged — no materialised defaults leak in).
    inner_args = parsed.model_dump(exclude={"action"}, exclude_unset=True)

    # Authorization is by admin TIER, not by scanning the SQL text. The executor's
    # admin_only gate already blocked non-admins; here the tier decides authority.
    level = _current_admin_level()
    is_super = level == SUPER_ADMIN

    if action == "query":
        # super_admin → unrestricted pool; any other tier → their own RLS scope.
        return await _sql_query_scoped(inner_args, ctx, started_at, level)
    if action == "schema":
        # Read-only schema introspection — available to any admin tier.
        return _sql_stamp(await db_schema(inner_args, ctx), started_at, ctx)

    # Everything below MUTATES via the privileged (service-role) path, which
    # bypasses RLS — so it is super_admin-only. Non-super tiers are redirected to
    # the RLS-enforced `data` tools (their sanctioned write path).
    if not is_super:
        return _write_requires_super_admin(action, level, started_at, ctx)

    if action == "insert":
        return _sql_stamp(await db_insert(inner_args, ctx), started_at, ctx)
    if action == "update":
        return _sql_stamp(await db_update(inner_args, ctx), started_at, ctx)
    if action == "delete":
        return await _sql_delete(inner_args, ctx, started_at)
    # action == "upsert"
    return await _sql_upsert(inner_args, ctx, started_at)
