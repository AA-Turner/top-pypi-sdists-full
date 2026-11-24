"""Agent-facing DB error hints — the funnel that turns a schema miss into the
information that makes the NEXT call succeed.

Born from a real incident (conversation 2e7c9ff2): an agent's ad-hoc SQL missed
on ``content_block`` vs ``content_blocks`` and a guessed column, and each miss
returned the matrx-orm developer banner (~1.2 KB, ANSI codes, drift advice for
humans) into the model context. This module produces the opposite: a compact,
ANSI-free message carrying did-you-mean suggestions, the real column list, or
the tables of the schema the agent aimed at — plus the read-only auto-heal
helpers (confident single-candidate table correction, rewrite, retry-once).

Pure logic, no I/O of its own: every schema lookup is an injected async
callable, so the module is unit-testable without a DB and reusable by any tool
family that has a table/column vocabulary (the ``sql`` tool injects its cached
information_schema helpers; db_grants can inject its zero-DB registry
resolvers). It deliberately re-parses Postgres message text as a fallback —
matrx-orm's ``SchemaMismatchError.details`` is the primary source (duck-typed,
no matrx-orm import), and the local parser is the independent second layer for
non-ORM errors (PostgREST APIError carries the same shapes).
"""
from __future__ import annotations

import difflib
import re
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass

from matrx_utils import did_you_mean, format_options

# Bounds — always on, tune here (never a flag). They keep a hint smaller than
# the failure it explains: an unbounded table list would recreate the original
# context-bloat bug in friendlier clothes.
HINT_MAX_TABLES = 50  # full table list allowed up to this many names
HINT_CLOSE_TABLES = 15  # above that, only the closest N + a count
HINT_MAX_COLUMNS = 60  # per-table column list bound
HINT_MAX_FALLBACK_TABLES = 3  # column hints when the failing column is unqualified
AUTOHEAL_MIN_RATIO = 0.85  # difflib ratio for a confident single-candidate heal
AGENT_DB_ERROR_MAX_CHARS = 2000  # hard ceiling on the final message

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

# Fallback message-shape parsers (second layer; primary is the structured
# details on matrx-orm's SchemaMismatchError). Kept byte-compatible with
# matrx_orm.exceptions.parse_undefined_identifier.
_UNDEF_RELATION_RE = re.compile(r'relation "([^"]+)" does not exist')
_UNDEF_SCHEMA_RE = re.compile(r'schema "([^"]+)" does not exist')
_UNDEF_COLUMN_OF_RELATION_RE = re.compile(r'column "([^"]+)" of relation "([^"]+)"')
_UNDEF_COLUMN_QUOTED_RE = re.compile(r'column "([^"]+)" does not exist')
_UNDEF_COLUMN_BARE_RE = re.compile(r"column ([\w$]+(?:\.[\w$]+)*) does not exist")
_PG_COLUMN_SUGGESTION_RE = re.compile(r'Perhaps you meant to reference the column "([^"]+)"')

# Statement text that must never be touched or matched: string literals,
# dollar-quoted bodies, comments. Mirrors the guards in database.py.
_PROTECTED_SPAN_RES = (
    re.compile(r"/\*.*?\*/", re.DOTALL),
    re.compile(r"--[^\n]*"),
    re.compile(r"\$(\w*)\$.*?\$\1\$", re.DOTALL),
    re.compile(r"'(?:[^']|'')*'"),
)

_FROM_JOIN_RE = re.compile(
    r'(?i)\b(?:FROM|JOIN)\s+((?:"[^"]+"|[\w$]+)(?:\s*\.\s*(?:"[^"]+"|[\w$]+))?)'
    r"(?:\s+(?:AS\s+)?"
    r"(?!(?:ON|USING|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|FULL|CROSS|GROUP|ORDER|LIMIT|SET|NATURAL|LATERAL|UNION|HAVING)\b)"
    r"([\w$]+))?"
)

AsyncStrList = Callable[[], Awaitable[list[str]]]
AsyncTablesBySchema = Callable[[], Awaitable[dict[str, list[str]]]]
AsyncSchemasForTable = Callable[[str], Awaitable[list[str]]]
AsyncTableColumns = Callable[[str, str], Awaitable[frozenset[str]]]


@dataclass(frozen=True)
class DbErrorFacts:
    """What we know about a failed statement, source-agnostic."""

    kind: str | None  # "table" | "column" | "schema" | None (unclassified)
    message: str  # concise, ANSI-free, agent-audience
    sqlstate: str | None = None
    missing_schema: str | None = None
    missing_table: str | None = None
    missing_column: str | None = None
    column_qualifier: str | None = None  # the "c" in `column c.label` — alias or table
    pg_suggestion: str | None = None  # PG's own `Perhaps you meant …` column


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


# ---------------------------------------------------------------------------
# Classification by SQLSTATE / exception type — NEVER by words in the message.
#
# The 2026-09-11 incident: `sql query table=ai.provider fields=[…, sync_policy]`
# failed on an unknown column and was reported to the agent as "your access level
# doesn't permit… requires super_admin", because the classifier asked
# `"policy" in message_text` and the COLUMN IS NAMED sync_policy. The agent spent
# its turn chasing permissions it already had. Message text is prose that changes
# with every Postgres release and every ORM banner; SQLSTATE is the contract.
# ---------------------------------------------------------------------------

SQLSTATE_INSUFFICIENT_PRIVILEGE = "42501"  # incl. RLS policy denial
SQLSTATE_UNDEFINED_TABLE = "42P01"
SQLSTATE_UNDEFINED_COLUMN = "42703"
SQLSTATE_UNDEFINED_SCHEMA = "3F000"
SQLSTATE_READ_ONLY_TRANSACTION = "25006"

# Exception TYPE names that carry the same meaning without a SQLSTATE reaching us
# (matrx-orm wrappers, asyncpg classes). Duck-typed by name so this module keeps
# its zero-import contract.
_PERMISSION_EXC_NAMES = frozenset(
    {"PermissionDeniedError", "InsufficientPrivilegeError", "RLSViolationError"}
)
_READ_ONLY_EXC_NAMES = frozenset({"ReadOnlyTransactionError", "ReadOnlyModelError"})

_KIND_BY_SQLSTATE: dict[str, str] = {
    SQLSTATE_UNDEFINED_TABLE: "table",
    SQLSTATE_UNDEFINED_COLUMN: "column",
    SQLSTATE_UNDEFINED_SCHEMA: "schema",
}


def exception_chain(exc: BaseException | None) -> list[BaseException]:
    """The exception and every ``__cause__`` / ``__context__`` beneath it."""
    chain: list[BaseException] = []
    seen: set[int] = set()
    cur: BaseException | None = exc
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        chain.append(cur)
        cur = cur.__cause__ or cur.__context__
    return chain


def sqlstate_of(exc: BaseException | None) -> str | None:
    """The Postgres SQLSTATE behind an exception, wrappers walked.

    Sources, in order of trust: the driver's own ``sqlstate`` attribute, an ORM
    exception's ``details['sqlstate']`` / ``['code']``, psycopg's ``pgcode``.
    """
    for item in exception_chain(exc):
        state = getattr(item, "sqlstate", None) or getattr(item, "pgcode", None)
        if isinstance(state, str) and state:
            return state
        details = getattr(item, "details", None)
        if isinstance(details, dict):
            state = details.get("sqlstate") or details.get("code")
            if isinstance(state, str) and state:
                return state
    return None


#: A statement the database refused because the CALLER's values break a rule: integrity
#: violations (class 23: check / foreign key / unique / not-null) and data exceptions
#: (class 22: bad enum label, bad uuid text, out-of-range). The model corrects them on its next
#: step; they are never a platform fault (2026-11-11: ``legal_entity_person_roles_check``,
#: ``..._identifier_kind_check`` and ``..._document_type_id_fkey`` filed as system_error).
CONSTRAINT_REFUSAL_ERROR_TYPE = "constraint_violation"
_CONSTRAINT_MESSAGE_RE = re.compile(
    r'violates (check|foreign key|unique|not-null) constraint|null value in column|'
    r'invalid input (?:value for enum|syntax for type)'
)
_CHECK_CONSTRAINT_RE = re.compile(r'violates check constraint "([^"]+)"')
_QUOTED_LITERAL_RE = re.compile(r"'((?:[^']|'')*)'(?:::[\w\s\[\]]+)?")


def is_constraint_refusal(exc: BaseException | None) -> bool:
    """True when the database refused the caller's own values (SQLSTATE class 22/23, or
    the exception text says so when the driver wrapper hides the code)."""
    state = sqlstate_of(exc)
    if state and state[:2] in ("22", "23"):
        return True
    if state:
        return False
    for item in exception_chain(exc):
        if "IntegrityError" in type(item).__name__ or "CheckViolation" in type(item).__name__:
            return True
        if _CONSTRAINT_MESSAGE_RE.search(strip_ansi(str(item))):
            return True
    return False


def check_constraint_name(exc: BaseException | None) -> str | None:
    """The CHECK constraint a refusal names, or None."""
    for item in exception_chain(exc):
        m = _CHECK_CONSTRAINT_RE.search(strip_ansi(str(item)))
        if m:
            return m.group(1)
    return None


_SQL_LITERAL = r"'((?:[^']|'')*)'(?:::[\w\s\".\[\]]+?)?"


def _pick_list_pattern() -> re.Pattern[str]:
    """ONE compiled pattern for every column's pick-list CHECK.

    The column is captured (group 1 in the ``IS NULL OR`` arm, 2-4 in the list) and compared
    afterwards, so nothing is compiled per column: a pattern holding the column name compiled
    a fresh regex per (column, CHECK) pair, more than ``re``'s cache holds, and froze aidream's
    catalog rebuild ~1 s (event_loop_stall aidream-api:59bc42dd96262433).
    """

    def col_ref(n: int) -> str:
        return rf'\(*(?:"(?P<q{n}>[^"]+)"|(?P<u{n}>\w+))\)*(?:::[\w\s]+)?'

    null_or = rf"(?:\(*{col_ref(1)}\s+IS\s+NULL\)*\s+OR\s+)?"
    items = rf"{_SQL_LITERAL}(?:\s*,\s*{_SQL_LITERAL})*"
    any_array = rf"\(*{col_ref(2)}\s*=\s*ANY\s*\(+ARRAY\[(?P<a>{items})\](?:\)::[\w\s]+\[\])?\)+"
    in_list = rf"\(*{col_ref(3)}\s+IN\s*\((?P<i>{items})\)\)*"
    # An ARRAY column whose every element comes from the list (``roles <@ ARRAY[...]``).
    subset = rf"\(*{col_ref(4)}\s*<@\s*\(*ARRAY\[(?P<s>{items})\](?:\)?::[\w\s]+\[\])?\)*"
    return re.compile(rf"{null_or}(?:{any_array}|{in_list}|{subset})", flags=re.IGNORECASE)


_PICK_LIST = _pick_list_pattern()
_PICK_LITERAL = re.compile(_SQL_LITERAL)


def _balanced(text: str) -> bool:
    depth = 0
    in_str = False
    for ch in text:
        if ch == "'":
            in_str = not in_str
        elif not in_str:
            depth += ch == "("
            depth -= ch == ")"
            if depth < 0:
                return False
    return depth == 0


def allowed_values_from_check(
    definition: str, *, column: str | None = None, cap: int | None = 40
) -> list[str]:
    """The allowed values of a CHECK that is EXACTLY a pick-list on one column, else ``[]``.

    The ONE parser (the sql tool's schema action and refusal note, aidream's data catalog).
    Accepts what ``pg_get_constraintdef`` prints for ``col = ANY (ARRAY[...])`` (Postgres
    rewrites ``col IN (...)`` to it), its ``col IS NULL OR …`` form, the varchar
    ``(col)::text = ANY ((ARRAY[...])::text[])`` form, a literal ``IN (...)``, and an array
    column's ``col <@ ARRAY[...]``. Anything else — ``NOT``, ``<>``, a regex, a range, a list
    joined by AND/OR with any further condition, two different columns — is not a pick-list:
    a literal there is a forbidden or partial value, never the allowed set. ``column`` given:
    the CHECK must be on that column. ``cap`` bounds the list (``None``: every value)."""
    body = (definition or "").strip()
    if not body.upper().startswith("CHECK"):
        return []
    body = body[5:].strip()
    while body.startswith("(") and body.endswith(")") and _balanced(body[1:-1]):
        body = body[1:-1].strip()
    m = _PICK_LIST.fullmatch(body)
    if m is None:
        return []
    named = {
        name.lower()
        for n in (1, 2, 3, 4)
        if (name := m.group(f"q{n}") or m.group(f"u{n}")) is not None
    }
    if len(named) != 1 or (column is not None and named != {column.lower()}):
        return []
    listed = m.group("a") or m.group("i") or m.group("s") or ""
    seen: list[str] = []
    for raw in _PICK_LITERAL.findall(listed):
        value = raw.replace("''", "'")
        if value not in seen:
            seen.append(value)
        if cap is not None and len(seen) >= cap:
            break
    return seen


def _exc_type_names(exc: BaseException | None) -> set[str]:
    return {type(item).__name__ for item in exception_chain(exc)}


def is_permission_error(exc: BaseException | None) -> bool:
    """True only for a genuine privilege / RLS denial (42501 or a typed wrapper)."""
    if sqlstate_of(exc) == SQLSTATE_INSUFFICIENT_PRIVILEGE:
        return True
    return bool(_exc_type_names(exc) & _PERMISSION_EXC_NAMES)


#: How Postgres itself words a privilege or row-level-security denial. Any OTHER 42501 text was
#: written by a guard (a RAISE in a trigger or function) and names the rule and the right door.
_PRIVILEGE_DENIAL_PREFIXES = (
    "permission denied", "new row violates row-level security", "must be owner", "must be superuser",
    "must be member", "must have",
)


def guard_refusal_text(exc: BaseException | None) -> str | None:
    """The database's own words when a 42501 came from a GUARD (a trigger / function RAISE that
    names the rule, e.g. "parent_folder_id ... is written ONLY by public.move_file"), else None.

    A guard refusal is the caller's correctable mistake: the generic "your access level doesn't
    permit ... requires super_admin" sends the model chasing access instead of the named door
    (system_error a6e69644, 2026-11-13)."""
    for item in exception_chain(exc):
        for cand in (item, getattr(item, "original_error", None)):
            if cand is None or getattr(cand, "sqlstate", None) != SQLSTATE_INSUFFICIENT_PRIVILEGE:
                continue
            text = getattr(cand, "message", None)
            if not isinstance(text, str) or not text.strip():
                text = str(cand.args[0]) if getattr(cand, "args", None) else ""
            text = strip_ansi(text).strip()
            if not text or text.lower().startswith(_PRIVILEGE_DENIAL_PREFIXES):
                return None
            return text
    return None


def is_read_only_error(exc: BaseException | None) -> bool:
    """True for a read-only transaction / read-only model refusal."""
    if sqlstate_of(exc) == SQLSTATE_READ_ONLY_TRANSACTION:
        return True
    return bool(_exc_type_names(exc) & _READ_ONLY_EXC_NAMES)


def _parse_message_text(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    if m := _UNDEF_COLUMN_OF_RELATION_RE.search(text):
        out["missing_column"] = m.group(1)
        out["missing_table"] = m.group(2)
    elif m := _UNDEF_COLUMN_QUOTED_RE.search(text):
        out["missing_column"] = m.group(1)
    elif m := _UNDEF_COLUMN_BARE_RE.search(text):
        ref = m.group(1)
        if "." in ref:
            qualifier, _, column = ref.rpartition(".")
            out["column_qualifier"] = qualifier
            out["missing_column"] = column
        else:
            out["missing_column"] = ref
    elif m := _UNDEF_RELATION_RE.search(text):
        ref = m.group(1)
        if "." in ref:
            schema, _, table = ref.partition(".")
            out["missing_schema"] = schema
            out["missing_table"] = table
        else:
            out["missing_table"] = ref
    elif m := _UNDEF_SCHEMA_RE.search(text):
        out["missing_schema"] = m.group(1)
    if m := _PG_COLUMN_SUGGESTION_RE.search(text):
        out["pg_suggestion"] = m.group(1)
    return out


def parse_db_error(exc: Exception) -> DbErrorFacts:
    """Extract structured facts from any DB-layer exception.

    Primary source: a matrx-orm ``SchemaMismatchError`` (duck-typed via its
    ``details`` dict + ``agent_message()``). Fallback: parse the (ANSI-stripped)
    exception text for the same Postgres shapes — covers PostgREST/APIError and
    any raw driver error.
    """
    details = getattr(exc, "details", None)
    agent_message = getattr(exc, "agent_message", None)
    if isinstance(details, dict) and callable(agent_message):
        message = strip_ansi(str(agent_message()))
        kind = details.get("kind")
        return DbErrorFacts(
            kind=kind if kind in ("table", "column", "schema") else None,
            message=message,
            sqlstate=details.get("sqlstate") or sqlstate_of(exc),
            missing_schema=details.get("missing_schema") or None,
            missing_table=details.get("missing_table") or None,
            missing_column=details.get("missing_column") or None,
            column_qualifier=details.get("column_qualifier") or None,
            pg_suggestion=details.get("pg_suggestion") or None,
        )

    text = strip_ansi(str(exc)).strip()
    parsed = _parse_message_text(text)
    kind: str | None = None
    if parsed.get("missing_column"):
        kind = "column"
    elif parsed.get("missing_table"):
        kind = "table"
    elif parsed.get("missing_schema"):
        kind = "schema"
    if kind is None:
        # No recognizable message shape — the SQLSTATE still classifies it.
        kind = _KIND_BY_SQLSTATE.get(sqlstate_of(exc) or "")
    # Non-ORM errors can be arbitrarily long too — keep the head, which for
    # Postgres/PostgREST always carries the reason.
    if len(text) > 500:
        text = text[:500] + "…"
    return DbErrorFacts(
        kind=kind,
        message=text,
        sqlstate=sqlstate_of(exc),
        missing_schema=parsed.get("missing_schema"),
        missing_table=parsed.get("missing_table"),
        missing_column=parsed.get("missing_column"),
        column_qualifier=parsed.get("column_qualifier"),
        pg_suggestion=parsed.get("pg_suggestion"),
    )


def parse_from_join(query: str) -> dict[str, str]:
    """Map alias → table reference (and bare/qualified name → itself) from every
    FROM/JOIN clause, string literals and comments masked out first."""
    masked = _mask_protected(query)
    out: dict[str, str] = {}
    for m in _FROM_JOIN_RE.finditer(masked):
        ref = re.sub(r"\s*\.\s*", ".", m.group(1)).strip('"').lower()
        ref = ".".join(part.strip('"') for part in ref.split("."))
        alias = (m.group(2) or "").lower()
        bare = ref.rpartition(".")[2]
        out.setdefault(ref, ref)
        out.setdefault(bare, ref)
        if alias:
            out[alias] = ref
    return out


def _mask_protected(query: str) -> str:
    """Blank out (preserve length) every protected span so regex scans can't
    match inside literals/comments."""
    masked = query
    for pattern in _PROTECTED_SPAN_RES:
        masked = pattern.sub(lambda m: " " * len(m.group(0)), masked)
    return masked


def _protected_spans(query: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for pattern in _PROTECTED_SPAN_RES:
        spans.extend(m.span() for m in pattern.finditer(query))
    return spans


def _in_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in spans)


def _ref_regex(ref: str) -> str:
    """Regex matching a (possibly qualified) identifier, each part optionally
    double-quoted, whitespace tolerated around the dot."""
    parts = [rf'(?:"{re.escape(p)}"|{re.escape(p)})' for p in ref.split(".")]
    return r"\s*\.\s*".join(parts)


def rewrite_table_ref(query: str, old_ref: str, new_ref: str) -> str | None:
    """Rewrite ``old_ref`` → ``new_ref`` in a SQL statement, conservatively.

    Stage A replaces only occurrences anchored to FROM/JOIN — the only position
    a 42P01 relation can be referenced from. Stage B (only when A matched
    nothing, e.g. comma-separated FROM lists) does an exact-token replace
    outside string-literal/comment spans, refusing dotted false positives.
    Returns the rewritten query, or None when no safe substitution was made.
    """
    if not old_ref or not new_ref or old_ref == new_ref:
        return None
    ref_re = _ref_regex(old_ref)

    stage_a = re.compile(rf'(?i)(\b(?:FROM|JOIN)\s+){ref_re}(?![\w"$])')
    spans = _protected_spans(query)
    result_parts: list[str] = []
    last = 0
    count = 0
    for m in stage_a.finditer(query):
        if _in_spans(m.start(), spans):
            continue
        result_parts.append(query[last : m.start()])
        result_parts.append(m.group(1) + new_ref)
        last = m.end()
        count += 1
    if count:
        result_parts.append(query[last:])
        return "".join(result_parts)

    # Stage B — exact token, not preceded by a dot (protects alias.column and
    # other_table.column references), outside protected spans.
    stage_b = re.compile(rf'(?<![\w.$"]){ref_re}(?![\w"$])')
    result_parts = []
    last = 0
    count = 0
    for m in stage_b.finditer(query):
        if _in_spans(m.start(), spans):
            continue
        result_parts.append(query[last : m.start()])
        result_parts.append(new_ref)
        last = m.end()
        count += 1
    if not count:
        return None
    result_parts.append(query[last:])
    rewritten = "".join(result_parts)
    return rewritten if rewritten != query else None


def _close(name: str, candidates: Iterable[str], n: int = 5, cutoff: float = 0.6) -> list[str]:
    return did_you_mean(name, candidates, n=n, cutoff=cutoff)


def _fmt_names(names: list[str], cap: int) -> str:
    return format_options(names, cap)


async def build_hint(
    facts: DbErrorFacts,
    query: str,
    *,
    app_schemas: AsyncStrList,
    tables_by_schema: AsyncTablesBySchema,
    schemas_for_table: AsyncSchemasForTable,
    get_table_columns: AsyncTableColumns,
) -> tuple[str, str]:
    """Build (message, suggested_action) for a failed statement.

    Best-effort by contract: any resolver failure degrades to the concise
    message without hints — a hint must never mask the original error.
    """
    try:
        return await _build_hint_inner(
            facts,
            query,
            app_schemas=app_schemas,
            tables_by_schema=tables_by_schema,
            schemas_for_table=schemas_for_table,
            get_table_columns=get_table_columns,
        )
    except Exception:
        return _bounded(facts.message), _GENERIC_ACTION


_GENERIC_ACTION = (
    "Check the table/column names against the real schema — the sql tool's "
    "{action:'schema'} lists schemas, tables, and columns — then retry."
)


def _bounded(message: str) -> str:
    if len(message) > AGENT_DB_ERROR_MAX_CHARS:
        return message[: AGENT_DB_ERROR_MAX_CHARS] + "…"
    return message


async def _build_hint_inner(
    facts: DbErrorFacts,
    query: str,
    *,
    app_schemas: AsyncStrList,
    tables_by_schema: AsyncTablesBySchema,
    schemas_for_table: AsyncSchemasForTable,
    get_table_columns: AsyncTableColumns,
) -> tuple[str, str]:
    lines = [facts.message]
    action = _GENERIC_ACTION

    if facts.kind == "schema" or (facts.kind == "table" and facts.missing_schema):
        schemas = await app_schemas()
        schema_exists = facts.missing_schema in schemas if facts.missing_schema else False
        if facts.kind == "schema" or not schema_exists:
            wrong = facts.missing_schema or ""
            close = _close(wrong, schemas)
            lines.append(f"Schema '{wrong}' does not exist. Available schemas: {_fmt_names(sorted(schemas), HINT_MAX_TABLES)}.")
            if close:
                action = f"Retry with schema '{close[0]}'."
            return _bounded("\n".join(lines)), action

    if facts.kind == "table" and facts.missing_table:
        wrong = facts.missing_table
        elsewhere = [s for s in await schemas_for_table(wrong) if s != facts.missing_schema]
        if facts.missing_schema:
            in_schema = sorted((await tables_by_schema()).get(facts.missing_schema, []))
            close = [f"{facts.missing_schema}.{t}" for t in _close(wrong, in_schema)]
        else:
            by_schema = await tables_by_schema()
            qualified = [f"{s}.{t}" for s, tables in by_schema.items() for t in tables]
            close = sorted(qualified, key=lambda q: difflib.SequenceMatcher(None, wrong, q.rpartition(".")[2]).ratio(), reverse=True)
            close = [q for q in close if difflib.SequenceMatcher(None, wrong, q.rpartition(".")[2]).ratio() >= 0.6][:5]
            in_schema = []
        if elsewhere:
            lines.append(
                f"A table named '{wrong}' exists in schema(s): {_fmt_names(sorted(elsewhere), HINT_CLOSE_TABLES)} — qualify it."
            )
        if close:
            lines.append(f"Close matches: {_fmt_names(close, HINT_CLOSE_TABLES)}.")
        if facts.missing_schema and in_schema:
            if len(in_schema) <= HINT_MAX_TABLES:
                lines.append(f"Tables in schema '{facts.missing_schema}': {', '.join(in_schema)}.")
            else:
                lines.append(
                    f"Schema '{facts.missing_schema}' has {len(in_schema)} tables (too many to list) — "
                    "use {action:'schema', schema:'" + facts.missing_schema + "'} for the full list."
                )
        if elsewhere and not close:
            action = f"Retry with table '{sorted(elsewhere)[0]}.{wrong}'."
        elif close:
            action = f"Retry with table '{close[0]}'."
        return _bounded("\n".join(lines)), action

    if facts.kind == "column" and facts.missing_column:
        if facts.pg_suggestion:
            lines.append(f"Postgres suggests the column you meant is \"{facts.pg_suggestion}\".")
            action = f"Retry using column \"{facts.pg_suggestion}\"."
        alias_map = parse_from_join(query)
        target_refs: list[str] = []
        if facts.missing_table:
            target_refs = [alias_map.get(facts.missing_table.lower(), facts.missing_table.lower())]
        elif facts.column_qualifier:
            ref = alias_map.get(facts.column_qualifier.lower())
            if ref:
                target_refs = [ref]
        if not target_refs:
            # Unqualified column (or unresolvable alias): every FROM/JOIN table, bounded.
            target_refs = sorted(set(alias_map.values()))[:HINT_MAX_FALLBACK_TABLES]
        for ref in target_refs:
            schema, _, name = ref.rpartition(".")
            if not schema:
                schemas = await schemas_for_table(name)
                if len(schemas) == 1:
                    schema = schemas[0]
                elif "public" in schemas:
                    schema = "public"
                else:
                    continue
            columns = sorted(await get_table_columns(schema, name))
            if columns:
                lines.append(
                    f"Columns of {schema}.{name}: {_fmt_names(columns, HINT_MAX_COLUMNS)}."
                )
        return _bounded("\n".join(lines)), action

    return _bounded(facts.message), action


async def autoheal_candidate(
    facts: DbErrorFacts,
    *,
    schemas_for_table: AsyncSchemasForTable,
    tables_by_schema: AsyncTablesBySchema,
) -> str | None:
    """The single confident correction for a missing TABLE, or None.

    Two candidate sources: the same bare name in another schema (a schema
    mistake), and a high-similarity name (plural/singular class). The gate is
    strict: exactly ONE candidate across both sources, else refuse — ambiguity
    goes to hints, never a guess. Returns a qualified ``schema.table``.
    """
    if facts.kind != "table" or not facts.missing_table:
        return None
    wrong = facts.missing_table
    exact = [f"{s}.{wrong}" for s in await schemas_for_table(wrong)]

    by_schema = await tables_by_schema()
    if facts.missing_schema:
        # Qualified miss: fuzzy candidates only within the schema the agent aimed at.
        pool = [(facts.missing_schema, t) for t in by_schema.get(facts.missing_schema, [])]
    else:
        pool = [(s, t) for s, tables in by_schema.items() for t in tables]
    fuzzy = [
        f"{s}.{t}"
        for s, t in pool
        if t != wrong and difflib.SequenceMatcher(None, wrong, t).ratio() >= AUTOHEAL_MIN_RATIO
    ]

    candidates = sorted(set(exact) | set(fuzzy))
    if len(candidates) == 1:
        return candidates[0]
    return None
