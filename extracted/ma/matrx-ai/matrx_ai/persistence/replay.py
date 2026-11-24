"""Replay dropped ops from system_write_failure.

When a coordinator flush fails, the fallback writer captures every op
(table, op_type, primary_key, payload, depends_on) to system_write_failure
on a fresh connection. The data is intact — only the original
transaction failed.

This module reads back those rows, reconstructs :class:`WriteOp` instances,
groups them by ``request_id`` (so each replay attempt covers one request's
ops as a single transaction), and runs them through the same
:func:`matrx_ai.persistence.flush.execute_tiers` path that the live
coordinator uses. On successful replay, the row's ``recovered_at`` and
``recovery_op_id`` are stamped so the watchdog stops re-alerting.

Usage::

    from matrx_ai.persistence.replay import replay_pending

    report = await replay_pending(dry_run=False)
    print(report.recovered_count, report.still_failed_count)

The replay is conservative — only ops with the InterfaceError signature
(the gather-in-transaction bug fixed in this PR) are eligible by default.
Other failure modes likely indicate semantic bugs that need investigation
before blindly retrying.

Two classifiers decide a row's fate in the auto loop:
:data:`RECOVERABLE_RETRY_ERRORS` says WHICH rows are worth a sweep, and
:data:`PERMANENT_FAILURE_SIGNATURES` overrides it — a recoverable marker
wrapped around a deterministic refusal (trigger RAISE, constraint, schema
drift, deleted actor) is quarantined on sight, never attempted, and captured
exactly once as ``persistence_replay_quarantined``.
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from matrx_orm import db_sqlstate
from matrx_orm.session.coalesce import coalesce_ops
from matrx_orm.session.dag import tier_ops
from matrx_orm.session.fallback import (
    DIRECT_WRITE_PRESERVED_MARKER,
    DISK_SPILL_RECOVERED_MARKER,
    IMMUTABLE_WRITE_PRESERVED_MARKER,
    immutable_row_differences,
)
from matrx_orm.session.flush import _unmatched_updates, execute_tiers
from matrx_orm.session.op import SessionOp, make_delete, make_insert, make_update
from matrx_utils import vcprint

from matrx_ai.db import message_positions as _message_positions  # noqa: F401 — declares the append sentinel
from matrx_ai.persistence.registry import get_model

logger = logging.getLogger("matrx_ai.persistence.replay")


class ImmutableReplayConflictError(RuntimeError):
    """A preserved immutable insert collides with a different committed row."""


@dataclass(slots=True)
class ReplayReport:
    candidates: int = 0
    eligible: int = 0
    recovered_count: int = 0
    still_failed_count: int = 0
    quarantined_count: int = 0
    conflict_count: int = 0
    """Rows given up on this sweep — permanent failures, no longer retried/alerted."""
    skipped_count: int = 0
    by_request: dict[str, str] = field(default_factory=dict)
    """request_id → 'recovered' | 'failed' | 'skipped' (with reason)."""
    errors: list[str] = field(default_factory=list)


# Default eligibility filter — only retry the failure mode we know is now fixed.
DEFAULT_RETRY_ERRORS: tuple[str, ...] = (
    "InterfaceError: cannot perform operation: another operation is in progress",
)

# Error-CLASS signatures that are SELF-HEALING — a later sweep simply succeeds
# once the world catches up, with no code change and no human judgment needed:
#
#   * ForeignKeyViolationError — the op references a parent row that wasn't in
#     the DB yet at flush time (the canonical case: a sub-agent CHILD
#     conversation persisted by one request/Coordinator races ahead of the
#     PARENT conversation's fire-and-forget commit in another request — the
#     single-Session FK-DAG can't order across sessions). Once the parent lands,
#     the replay just works.
#   * InterfaceError (concurrent op on a shared connection) — a transient
#     asyncpg collision; the replay runs on a clean connection.
#
# Everything ELSE (check-constraint violations, schema drift, unique
# violations, NOT-NULL) is a genuine bug, NOT an ordering race — it must NOT be
# blindly auto-retried, because retrying can't fix it and would mask it. The
# auto-replay QUARANTINES those on sight (retry_count pinned at the cap) and
# files ONE ``persistence_replay_quarantined`` system_error per request group —
# the human queue — instead of leaving them below the cap where the lifecycle
# watchdog re-fired on them every hour forever (4 rows, ~68h, 2026-09-28).
# This list is the precise boundary between "the platform self-heals" and
# "stop the line".
#   * DiskSpillRecovered — an op that was spilled to disk during a TOTAL DB
#     outage (record_failures couldn't even reach system_write_failure) and then
#     re-landed into the table by drain_spilled_ops once the DB returned. The
#     outage is definitionally self-healing, so the re-applied write just works.
#   * DirectWritePreserved — a DIRECT (non-Session) write of an already-paid-for
#     artifact that failed and had its payload preserved by
#     ``matrx_orm.create_or_capture``. The failures that kill such a write are
#     environmental (statement timeout, connection reset, pool exhaustion), so
#     re-applying it is exactly right; and the alternative — leaving it parked —
#     means a user is billed again for output we are already holding.
#   * commit hard-deadline — a Coordinator background flush exceeded its hard
#     database deadline. The full operation payload was durably captured after
#     the transaction was canceled, so replay is the required completion of a
#     transient infrastructure failure, not a blind retry of ambiguous SQL.
#   * QueryTimeoutError — the failed transaction has already rolled back and
#     its operation was captured on a fresh connection. A fresh replay is the
#     bounded recovery path for temporary relation-lock or database-load
#     contention; a persistent failure reaches the existing five-attempt
#     quarantine boundary.
#   * LockNotAvailableError — PostgreSQL refused the statement before it could
#     acquire the required relation lock. The transaction is rolled back and
#     the complete operation is safe to retry on a fresh connection.
#   * coordinator drop — the Coordinator could not QUEUE the op (its phase had
#     already errored or closed) and ``_capture_lost_op`` preserved it
#     byte-for-byte precisely so it could be replayed. It was never attempted.
#   * NOT NULL on an inherited ``organization_id`` — the parent the DB copies it
#     from had not landed yet (see INHERITED_COLUMN_NOTNULL_SIGNATURES). It was
#     always classified recoverable but never ELIGIBLE, so it sat unreplayed.
COORDINATOR_DROP_MARKER = "coordinator drop:"

# An UPDATE that ran before its row existed. It is no class of its own: it is worth a
# sweep exactly when the row can still take it — the row's INSERT is waiting in this
# sweep, or landed since (live 2026-11-03: three refused rag.pdf_page_cleaner requests
# got their INSERT replayed ``pending`` while their ``failed`` UPDATE was quarantined
# unattempted, and stood pending until the watchdog abandoned them).
UNMATCHED_UPDATE_MARKER = "UPDATE(s) matched no row"

RECOVERABLE_RETRY_ERRORS: tuple[str, ...] = (
    "ForeignKeyViolationError",
    "InterfaceError: cannot perform operation: another operation is in progress",
    DISK_SPILL_RECOVERED_MARKER,
    DIRECT_WRITE_PRESERVED_MARKER,
    IMMUTABLE_WRITE_PRESERVED_MARKER,
    "commit hard-deadline",
    "QueryTimeoutError",
    "TransactionTimeoutError",
    "LockNotAvailableError",
    COORDINATOR_DROP_MARKER,
    'null value in column "organization_id"',
)


# A TRANSACTION timeout (SQLSTATE 25P04, ``transaction_timeout``) terminates the
# connection mid-transaction: like a statement timeout its COMMIT is unknown, so it rides
# the same INSERT-only, read-the-key-first path. Live 2026-11-06 (feedback d231594e): a
# chat.message insert lost to one was quarantined on sight as "no self-healing class".
_QUERY_TIMEOUT_CAPTURE_HEADS = (
    "matrx_orm.exceptions.QueryTimeoutError:",
    "QueryTimeoutError:",
    "asyncpg.exceptions.TransactionTimeoutError:",
    "TransactionTimeoutError:",
)


def _is_query_timeout_capture_text(error_text: str | None) -> bool:
    """Whether the captured exception itself, rather than its payload, timed out."""
    return bool(error_text and error_text.lstrip().startswith(_QUERY_TIMEOUT_CAPTURE_HEADS))


# Modules whose exception ``str()`` may embed SQL text or bound arguments
# (a matrx_orm ``QueryError`` banner prints ``Args:``). Their message is only
# trusted when it is Postgres's own primary message (a SQLSTATE is present):
# that message names the relation / column / constraint, never a row value —
# the values live in ``detail``, which is never copied.
_ARG_BEARING_EXCEPTION_MODULES = ("asyncpg", "psycopg", "psycopg2", "matrx_orm", "postgrest")
_REPLAY_TEXT_MAX = 300  # protocol-constant: length of a diagnostic excerpt in a replay log line, not a behavior an admin tunes
_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _bounded_line(text: str | None, *, limit: int = _REPLAY_TEXT_MAX) -> str:
    """First meaningful line of ``text``: ANSI stripped, row values cut, bounded."""
    if not text:
        return ""
    cleaned = _ANSI_ESCAPE.sub("", str(text))
    line = next((ln.strip() for ln in cleaned.splitlines() if ln.strip().strip("-=")), "")
    # ``describe_db_exception().as_text()`` appends ``detail=`` (the failing
    # row's VALUES) and ``hint=`` after the identifiers — never carry them.
    for cut in (" detail=", " hint=", " Args:"):
        idx = line.find(cut)
        if idx != -1:
            line = line[:idx]
    return line[:limit]


# Non-database exceptions whose message is written by our own persistence code
# and never interpolates a payload: the session's "UPDATE matched no row", the
# commit hard-deadline, the immutable-conflict verdict, and the sweep's own
# "Replay refused: …" reasons. Any other exception's text may carry row data,
# so only its class name travels.
_OWN_MESSAGE_TYPES: tuple[str, ...] = ("LookupError", "TimeoutError", "ImmutableReplayConflictError")
_OWN_MESSAGE_PREFIX = "Replay refused:"


def _message_is_ours(exc: BaseException) -> bool:
    module = (type(exc).__module__ or "").split(".", 1)[0]
    if module in _ARG_BEARING_EXCEPTION_MODULES:
        return False
    if type(exc).__name__ in _OWN_MESSAGE_TYPES:
        return True
    return str(exc).startswith(_OWN_MESSAGE_PREFIX)


def _safe_replay_failure_text(exc: BaseException) -> str:
    """A bounded diagnostic that names the REAL cause without serializing data.

    Carries the exception class, SQLSTATE, constraint / table / column, and the
    reason message — Postgres's primary message for a database refusal, or the
    message of our own non-database exception (a quarantine reason, a
    LookupError). It never carries SQL text, bound arguments, ``detail``
    (row values) or a traceback. Until 2026-11-03 it carried only the class
    name, so 434 quarantines and 163 FK failures all read "replay execution
    failed" and nobody could tell which constraint or which refusal.
    """
    from matrx_orm.exceptions import describe_db_exception

    parts = [f"{type(exc).__name__}: replay execution failed"]
    message = ""
    try:
        info = describe_db_exception(exc)
        if info.sqlstate:
            parts.append(f"[SQLSTATE {info.sqlstate}]")
            if info.constraint:
                parts.append(f"constraint={info.constraint}")
            if info.table:
                table = f"{info.schema}.{info.table}" if info.schema else info.table
                parts.append(f"table={table}")
            if info.column:
                parts.append(f"column={info.column}")
            message = _bounded_line(info.message)
    except Exception:  # noqa: BLE001 — failure reporting must not fail closed
        pass
    if not message and _message_is_ours(exc):
        message = _bounded_line(str(exc))
    text = " ".join(parts)
    return f"{text}: {message}" if message else text


def _captured_failure_heads(rows: Sequence[Any], *, limit: int = 5) -> list[str]:
    """The distinct ORIGINAL failures behind ``rows`` (first line, no row values).

    A quarantine refuses a row because of what killed it at CAPTURE time —
    without this, the system_error says only that the sweep gave up.
    """
    heads: list[str] = []
    for row in rows:
        try:
            text = row.get("error_text") if hasattr(row, "get") else row["error_text"]
        except Exception:  # noqa: BLE001
            text = None
        head = _bounded_line(text, limit=240)
        if head and head not in heads:
            heads.append(head)
            if len(heads) >= limit:
                break
    return heads

# Error-CLASS signatures that are PERMANENT — the database REFUSED the write on
# its merits, so re-sending the identical row can never succeed. These override
# every recoverable marker above: a spilled or preserved op is only self-healing
# when what killed it was the ENVIRONMENT (outage, timeout, pool, ordering).
# When the wrapped failure is one of these, the marker is a lie about that row
# and the replay must quarantine it on sight — attempting it burns five sweeps,
# lands five identical ``persistence_replay_failed`` system_error rows, and
# teaches nobody anything (live evidence 2026-09-12: eight ``chat.message``
# spills whose ``created_by`` named a user that does not exist; the
# ``_stamp_org_default`` trigger raised P0001 on every one of the 40 attempts).
#
# Matched as substrings of ``error_text`` (``describe_db_exception`` renders
# both the asyncpg class name and ``[SQLSTATE xxxxx]``), and of the live
# exception a replay attempt raises — ONE classifier for both moments.
PERMANENT_FAILURE_SIGNATURES: tuple[str, ...] = (
    # A trigger / RAISE EXCEPTION rejected the row (a missing-user check,
    # component guards, doctrine checks). The refusal is deterministic.
    "RaiseError",
    "[SQLSTATE P0001]",
    # Declarative constraint refusals — the row itself is wrong.
    "CheckViolationError",
    "[SQLSTATE 23514]",
    "NotNullViolationError",
    "[SQLSTATE 23502]",
    "UniqueViolationError",
    "[SQLSTATE 23505]",
    # Schema drift — the payload names something the schema no longer has.
    "UndefinedColumnError",
    "[SQLSTATE 42703]",
    "UndefinedTableError",
    "[SQLSTATE 42P01]",
    "UndefinedFunctionError",
    "[SQLSTATE 42883]",
    "DatatypeMismatchError",
    "[SQLSTATE 42804]",
    # Value refusals — a poisoned payload.
    "InvalidTextRepresentationError",
    "[SQLSTATE 22P02]",
    "StringDataRightTruncationError",
    "[SQLSTATE 22001]",
    # The capture lane already proved the acting user is gone
    # (``drain_spilled_ops`` stamps this when the actor FK cannot be satisfied).
    # Every org-scoped target derives its org from that actor, so the write can
    # never land.
    "capture_actor_missing=",
    # Sibling refusals the 2026-09-12 review censused in db/migrations: the same
    # trigger families RAISE with an explicit ERRCODE other than P0001, and
    # asyncpg maps each to its own class — none of them contains "RaiseError".
    #   * P0002 no_data_found — ``message_not_found`` guards
    #     (0046_context_visibility, 0151_cx_message_set_content_tool_graph_guard)
    #   * 28000 — ``no_session`` guards (same files)
    #   * 42501 insufficient_privilege — ownership guards (0031, 0126, 0177, 0198, 0222)
    "NoDataFoundError",
    "[SQLSTATE P0002]",
    "InvalidAuthorizationSpecificationError",
    "[SQLSTATE 28000]",
    "InsufficientPrivilegeError",
    "[SQLSTATE 42501]",
    # 0178_enforce_agent_tool_references RAISEs with ERRCODE foreign_key_violation
    # for a BUSINESS-RULE refusal (an agent naming a tool id that does not exist).
    # It wears the recoverable FK class as a disguise, but no sibling request
    # will ever create that tool row, so it is permanent by its message.
    "references missing tool ids",
    "is referenced by an agent definition",
)


# A foreign-key violation is the ONE class that is recoverable or permanent
# depending on WHICH parent is missing. A parent row another request is still
# committing (a conversation, a user_request) arrives within seconds — that is
# the race RECOVERABLE_RETRY_ERRORS exists for. A missing *actor* never arrives:
# ``auth.users`` rows are created by sign-up, not by a sibling request, so an FK
# to it that fails today fails forever. ``describe_db_exception`` renders the
# constraint name and Postgres's own detail (``Key (created_by)=(…) is not
# present in table "users"``); either is enough to tell the two apart.
ACTOR_FK_SIGNATURES: tuple[str, ...] = (
    'is not present in table "users"',
    "_created_by_fkey",
    "_user_id_fkey",
    "_owner_id_fkey",
    "_updated_by_fkey",
)


# A NOT NULL refusal on a column the DATABASE fills from a parent row is the
# mirror of the FK split above: it is recoverable or permanent depending on
# whether that parent has landed yet.
#
# ``chat.request`` never carries an ``organization_id`` in its payload — the
# writer does not send one. ``platform.inherit_org_from_parent`` reads it off
# the row's ``chat.conversation`` parent on INSERT. And
# ``cx_request_conversation_id_fkey`` is DEFERRABLE INITIALLY DEFERRED, so when
# the parent conversation is itself still quarantined the BEFORE-INSERT trigger
# finds nothing, leaves the column NULL, and the NOT NULL fires FIRST — wearing
# the permanent "the row itself is wrong" costume while the truth is "the
# parent has not arrived yet". The deferred FK, which would have named the real
# problem, never gets to speak.
#
# Live evidence 2026-09-17 (seo.page_mapper): three chat.request rows refused
# this way at 16:59, 17:00 and 17:01, each while its parent conversation sat
# unrecovered in system_write_failure. All three parents were written at
# 17:02 — 60 to 180 seconds later, well inside FK_RACE_MAX_AGE_SECONDS. The
# children would have inserted cleanly on the very next sweep, but
# ``NotNullViolationError`` is listed above, so they were quarantined on sight
# and $0.134860 of paid, already-billed model work was lost from the ledger
# permanently.
#
# Treating this as recoverable is bounded twice over and cannot spin: the sweep
# gives up after AUTO_REPLAY_MAX_ATTEMPTS and quarantines anything already older
# than FK_RACE_MAX_AGE_SECONDS on its first failed sweep. If the parent really
# never comes, the row is quarantined ~5 minutes later exactly as before.
INHERITED_COLUMN_NOTNULL_SIGNATURES: tuple[str, ...] = (
    'null value in column "organization_id"',
)

# Relations that are the ROOT of the org inheritance chain: nothing copies an
# ``organization_id`` onto them (live 2026-11-03: ``chat.conversation`` carries
# no org-inheriting trigger). A NULL org on one of these is the writer's own
# missing organization — no parent will ever arrive — so it is a permanent
# refusal, quarantined on sight with ONE system_error, never five attempts.
# Live evidence 2026-11-03: ``__tool_test__`` conversations inserted with no
# organization burned the whole attempt budget, one IntegrityError each sweep.
ORG_ROOT_RELATION_SIGNATURES: tuple[str, ...] = (
    'of relation "conversation"',
    "table=conversation ",
)


# The organization is the other parent no sibling request ever creates: an
# ``iam.organizations`` row is made by a person (sign-up, "new organization"), never
# by a Coordinator flush. An FK to one that is missing today is missing forever.
# Live evidence (2026-10-23..30): nine ``chat.user_request`` inserts filed under a
# test-fixture organization that never existed were classified as an FK RACE,
# attempted five times each, and landed 45 ``persistence_replay_failed`` rows —
# one per attempt — before quarantine.
ORGANIZATION_FK_SIGNATURES: tuple[str, ...] = (
    'is not present in table "organizations"',
    "_organization_id_fkey",
)


def is_actor_fk_violation_text(error_text: str | None) -> bool:
    """True for a foreign-key refusal whose missing parent is a user (never a race)."""
    if not error_text or "ForeignKeyViolationError" not in error_text:
        return False
    return any(sig in error_text for sig in ACTOR_FK_SIGNATURES)


def is_organization_fk_violation_text(error_text: str | None) -> bool:
    """True for a foreign-key refusal whose missing parent is an organization (never a race)."""
    if not error_text:
        return False
    if "ForeignKeyViolationError" not in error_text and "[SQLSTATE 23503]" not in error_text:
        return False
    return any(sig in error_text for sig in ORGANIZATION_FK_SIGNATURES)


#: What ``ops.seal_confidential_write_failure`` (a BEFORE INSERT trigger on
#: ``ops.system_write_failure``) writes into ``payload.redacted`` when the failed op
#: belongs to a confidential conversation: the payload is reduced to
#: ``{id, conversation_id, role, position, redacted}`` by design, so the original
#: write can never be rebuilt from it. Live evidence (2026-10-22..27): eight such rows
#: (a ``chat.message`` insert + a ``chat.user_request`` update per request) were
#: attempted five times each — every attempt a ``ValueError`` reconstructing the op —
#: and landed 20 ``persistence_replay_failed`` rows.
SEALED_REDACTION_MARKER = "confidential conversation: content not kept"


def is_sealed_redacted_row(row: Any) -> bool:
    """True when the captured payload was deliberately redacted for a confidential chat."""
    try:
        payload = row.get("payload") if hasattr(row, "get") else row["payload"]
    except Exception:  # noqa: BLE001 — classification must never raise
        return False
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except ValueError:
            return False
    return isinstance(payload, dict) and payload.get("redacted") == SEALED_REDACTION_MARKER


def is_inherited_column_notnull_text(error_text: str | None) -> bool:
    """True for a NOT NULL refusal on a column the DB inherits from a parent row.

    Recoverable, not permanent: the column is NULL because the parent has not
    landed yet, and the sweep's attempt + age ceilings bound the retrying.
    """
    if not error_text:
        return False
    if "NotNullViolationError" not in error_text and "[SQLSTATE 23502]" not in error_text:
        return False
    if any(sig in error_text for sig in ORG_ROOT_RELATION_SIGNATURES):
        return False
    return any(sig in error_text for sig in INHERITED_COLUMN_NOTNULL_SIGNATURES)


def is_permanent_failure_text(error_text: str | None) -> bool:
    """True when ``error_text`` carries a signature the DB refuses deterministically."""
    if not error_text:
        return False
    # Checked BEFORE the signature sweep: this shape matches
    # NotNullViolationError, and the whole point is that it is the one NOT NULL
    # that is a race rather than a verdict on the row.
    if is_inherited_column_notnull_text(error_text):
        return False
    if any(sig in error_text for sig in PERMANENT_FAILURE_SIGNATURES):
        return True
    return is_actor_fk_violation_text(error_text) or is_organization_fk_violation_text(error_text)


def is_permanent_failure_exception(exc: BaseException) -> bool:
    """True when a live replay attempt died of a deterministic refusal."""
    if isinstance(exc, ImmutableReplayConflictError):
        return True
    from matrx_orm.exceptions import describe_db_exception

    try:
        text = describe_db_exception(exc).as_text()
    except Exception:  # noqa: BLE001 — classification must never raise
        text = f"{type(exc).__name__}: {exc}"
    return is_permanent_failure_text(text)


# Auto-replay loop cadence. A minute is plenty: the only thing it waits on is a
# parent row from a sibling request landing, which happens in seconds. A short
# interval keeps stuck-row dwell time (and the watchdog's CRITICAL window) low
# without hammering the DB.
DEFAULT_AUTO_REPLAY_INTERVAL_SECS: float = 60.0
DEFAULT_AUTO_REPLAY_LIMIT: int = 200

# Give-up boundary for SELF-HEALING failures. A cross-session FK-ordering race
# resolves within seconds (once the sibling request's parent row lands); a
# transient asyncpg collision clears on the very next clean-connection replay.
# A row that is STILL failing after this many auto-replay sweeps is therefore
# NOT a race — it is a PERMANENT orphan (e.g. a cx_tool_call whose parent
# cx_user_request was never created at all). Past this point the auto-replay
# loop stops re-fetching it AND the lifecycle watchdog stops alerting on it
# (both bound their attention by `retry_count < AUTO_REPLAY_MAX_ATTEMPTS`).
#
# The row is NOT marked recovered — `recovered_at` stays NULL because it was
# never actually written. It is simply quarantined: honestly visible to a
# human via `WHERE recovered_at IS NULL AND retry_count >= AUTO_REPLAY_MAX_ATTEMPTS`
# (the admin /persistence views), but no longer spamming the log every minute
# or holding the watchdog at CRITICAL forever.
#
# 5 sweeps × 60s = ~5 min, orders of magnitude beyond any real race window.
# IMPORTANT: aidream/db/watchdog_configs.py imports this constant to build the
# system_write_failure watchdog predicate — keep them in lockstep (single
# source of truth) by referencing this value, never hardcoding a copy.
AUTO_REPLAY_MAX_ATTEMPTS: int = 5

# A genuine cross-session FK race is resolved within seconds. Any recoverable
# failure already OLDER than this at sweep time is structurally permanent (the
# parent row is never coming), so it is quarantined on the FIRST failed sweep
# rather than burning the full attempt budget — this clears a startup backlog
# of stale orphans immediately instead of logging them ~5 times each first.
FK_RACE_MAX_AGE_SECONDS: float = 900.0


def _model_for_table(table: str) -> Any:
    try:
        return get_model(table)
    except KeyError:
        # The persistence registry only pre-registers Coordinator-owned tables.
        # A row captured by `matrx_orm.create_or_capture` can name ANY table
        # (its whole point is direct writes outside the Coordinator), so fall
        # back to the ORM's own (schema, table) → Model registry rather than
        # refusing to replay a preserved artifact.
        from matrx_orm.core.registry import get_model_by_table_name

        schema, _, table_name = table.partition(".")
        return get_model_by_table_name(schema, table_name)


def _row_target(row: Any) -> tuple[str, str] | None:
    """The (table, primary key) a failure row writes, or None when it does not say."""
    pk_raw = row.get("primary_key")
    pk_map = json.loads(pk_raw) if isinstance(pk_raw, str) else pk_raw
    if not pk_map:
        return None
    return str(row.get("table_target")), str(next(iter(pk_map.values())))


def _is_unmatched_update(row: Any) -> bool:
    return row.get("op_type") == "update" and UNMATCHED_UPDATE_MARKER in str(row.get("error_text") or "")


def _group_rows(rows: Sequence[Any]) -> dict[str, list[Any]]:
    """One replay transaction per request; a row's UPDATE rides with the row's INSERT.

    Captures of one row carry different ``request_id``s when separate flushes wrote
    them, so the key alone would replay an UPDATE with no row under it. A redacted
    UPDATE stays out: its group is quarantined whole, and the INSERT need not be."""
    insert_group: dict[tuple[str, str], str] = {}
    for r in rows:
        target = _row_target(r)
        if r.get("op_type") == "insert" and target is not None:
            insert_group[target] = r["request_id"] or "_orphan"
    by_request: dict[str, list[Any]] = {}
    for r in rows:
        key = r["request_id"] or "_orphan"
        target = _row_target(r)
        if r.get("op_type") == "update" and target is not None and not is_sealed_redacted_row(r):
            key = insert_group.get(target, key)
        by_request.setdefault(key, []).append(r)
    return by_request


async def _insert_already_landed(row: Any) -> bool:
    """Whether a timed-out INSERT's row is already in its table (the COMMIT may have
    succeeded before the client gave up). Read by primary key, uncached."""
    pk_raw = row["primary_key"]
    pk_map = json.loads(pk_raw) if isinstance(pk_raw, str) else pk_raw
    pk_col, pk_val = next(iter(pk_map.items()))
    model_cls = _model_for_table(row["table_target"])
    found = await model_cls.filter(**{pk_col: str(pk_val)}).values(pk_col)
    return bool(found)


def _row_to_op(row: Any) -> SessionOp:
    """Reconstruct a SessionOp from a system_write_failure row.

    The row carries primary_key as a jsonb mapping ({column: value}) and
    depends_on as a jsonb list of [table, value] pairs (ignored — Session
    derives ordering from FK declarations). payload is jsonb.

    Resolves table_target → matrx-orm Model class via the persistence
    registry so the SessionOp carries the actual class, which is what
    the new tier_ops / execute_tiers expect.
    """
    payload_raw = row["payload"]
    payload = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw

    pk_raw = row["primary_key"]
    pk_map = json.loads(pk_raw) if isinstance(pk_raw, str) else pk_raw
    pk_col, pk_val = next(iter(pk_map.items()))

    model_cls = _model_for_table(row["table_target"])
    op_type = row["op_type"]

    if op_type == "insert":
        merged = dict(payload)
        merged.setdefault(pk_col, str(pk_val))
        return make_insert(model_cls, merged, pk_value=str(pk_val))
    if op_type == "update":
        return make_update(model_cls, str(pk_val), dict(payload))
    if op_type == "delete":
        return make_delete(model_cls, str(pk_val))
    raise ValueError(f"Unknown op_type {op_type!r} in system_write_failure row")


def _payload_dict(row: Any) -> dict[str, Any]:
    payload_raw = row["payload"]
    payload = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw
    return dict(payload or {})


async def _upgrade_legacy_chat_payloads(rows: Sequence[Any]) -> list[dict[str, Any]]:
    """Restore attribution omitted by pre-org-schema chat write payloads.

    Failure rows are durable artifacts and may outlive the schema version that
    created them. The 2026 chat schema moved ownership from ``user_id`` to
    ``created_by`` and made ``organization_id`` mandatory. A preserved
    ``chat.user_request`` can therefore carry its old actor but not the current
    columns, while its sibling ``chat.request`` identifies the authoritative
    conversation. Rebuild both rows from those preserved relationships before
    replaying them through today's models.

    This stays inside matrx-ai: chat relations belong to the package, and all
    lookups go through its injected matrx-orm models. No aidream host import or
    privileged database path is needed.
    """
    upgraded = [dict(row) for row in rows]
    for row in upgraded:
        row["payload"] = _payload_dict(row)

    request_rows = [row for row in upgraded if row["table_target"] == "chat.request"]
    snapshot_rows = [
        row for row in upgraded if row["table_target"] == "chat.request_snapshot"
    ]
    user_request_rows = {
        str(row["primary_key"].get("id")): row
        for row in upgraded
        if row["table_target"] == "chat.user_request"
        and isinstance(row.get("primary_key"), dict)
        and row["primary_key"].get("id")
    }
    if not request_rows and not user_request_rows and not snapshot_rows:
        return upgraded

    conversation_attribution: dict[str, dict[str, Any]] = {}
    for row in upgraded:
        if row["table_target"] != "chat.conversation":
            continue
        payload = row["payload"]
        conversation_id = payload.get("id")
        if conversation_id:
            conversation_attribution[str(conversation_id)] = {
                "organization_id": payload.get("organization_id"),
                "created_by": payload.get("created_by"),
            }

    conversation_ids = {
        str(row["payload"]["conversation_id"])
        for row in [*request_rows, *snapshot_rows]
        if row["payload"].get("conversation_id")
    }
    missing_ids = conversation_ids - conversation_attribution.keys()
    if missing_ids:
        Conversation = get_model("chat.conversation")
        for conversation_id in sorted(missing_ids):
            found = await Conversation.filter(id=conversation_id).values(
                "organization_id", "created_by"
            )
            if found:
                conversation_attribution[conversation_id] = dict(found[0])

    conversation_by_user_request: dict[str, str] = {}
    for row in request_rows:
        payload = row["payload"]
        user_request_id = payload.get("user_request_id")
        conversation_id = payload.get("conversation_id")
        if user_request_id and conversation_id:
            conversation_by_user_request[str(user_request_id)] = str(conversation_id)

    user_request_attribution: dict[str, dict[str, Any]] = {}
    for user_request_id, row in user_request_rows.items():
        payload = row["payload"]
        conversation_id = conversation_by_user_request.get(user_request_id)
        conversation = conversation_attribution.get(conversation_id or "", {})
        owner_id = (
            payload.get("created_by")
            or payload.get("user_id")
            or row.get("created_by")
            or row.get("user_id")
            or conversation.get("created_by")
        )
        organization_id = (
            payload.get("organization_id")
            or conversation.get("organization_id")
            or row.get("organization_id")
        )
        if owner_id:
            payload.setdefault("created_by", owner_id)
        if organization_id:
            payload.setdefault("organization_id", organization_id)
        user_request_attribution[user_request_id] = {
            "created_by": owner_id,
            "organization_id": organization_id,
        }

    for row in request_rows:
        payload = row["payload"]
        user_request = user_request_attribution.get(str(payload.get("user_request_id") or ""), {})
        conversation = conversation_attribution.get(str(payload.get("conversation_id") or ""), {})
        owner_id = (
            payload.get("created_by")
            or user_request.get("created_by")
            or row.get("created_by")
            or row.get("user_id")
            or conversation.get("created_by")
        )
        organization_id = (
            payload.get("organization_id")
            or conversation.get("organization_id")
            or user_request.get("organization_id")
            or row.get("organization_id")
        )
        if owner_id:
            payload.setdefault("created_by", owner_id)
        if organization_id:
            payload.setdefault("organization_id", organization_id)

    for row in snapshot_rows:
        payload = row["payload"]
        conversation = conversation_attribution.get(
            str(payload.get("conversation_id") or ""), {}
        )
        organization_id = (
            payload.get("organization_id")
            or conversation.get("organization_id")
            or row.get("organization_id")
        )
        if organization_id:
            payload.setdefault("organization_id", organization_id)

    return upgraded


_LEGACY_UNAMBIGUOUS_FIELD_RENAMES: dict[str, dict[str, str]] = {
    # ``workbench.notes`` uses ``label`` as its canonical display-title field.
    # A past producer emitted ``name`` into a captured coordinator UPDATE.
    # Keep this as a narrow, versioned replay migration rather than a generic
    # field guesser: replay is allowed to upgrade only a synonym that maps to
    # one known column on one known relation.
    "workbench.notes": {"name": "label"},
}

_LEGACY_UNAMBIGUOUS_VALUE_REWRITES: dict[str, dict[str, dict[Any, Any]]] = {
    # The media-catalog producer used the provider name as the transcript's
    # source category before e46f9fb95f. The database has always accepted the
    # media category (audio|video|meeting|interview|other), while the provider
    # already lives in metadata.media.adapter. A YouTube upload is therefore
    # unambiguously a video; changing only this value restores the preserved
    # payload without discarding any provider provenance.
    "transcripts.transcripts": {"source_type": {"youtube": "video"}},
}


async def _upgrade_legacy_payloads(rows: Sequence[Any]) -> list[dict[str, Any]]:
    """Upgrade durable payloads whose pre-normalization spelling is unambiguous.

    The replay queue is forensic evidence, so upgrades are in-memory only: the
    original ``ops.system_write_failure.payload`` remains intact while the
    reconstructed ``SessionOp`` targets today's model contract.  A source key
    is rewritten only when its canonical target is absent; a payload that
    contains both remains untouched and is deliberately left for the model to
    refuse rather than silently choosing a value.
    """
    upgraded = await _upgrade_legacy_chat_payloads(rows)
    for row in upgraded:
        renames = _LEGACY_UNAMBIGUOUS_FIELD_RENAMES.get(str(row["table_target"]))
        payload = row["payload"]
        for legacy_name, canonical_name in (renames or {}).items():
            if legacy_name in payload and canonical_name not in payload:
                payload[canonical_name] = payload.pop(legacy_name)
        rewrites = _LEGACY_UNAMBIGUOUS_VALUE_REWRITES.get(str(row["table_target"]))
        for field_name, values in (rewrites or {}).items():
            current = payload.get(field_name)
            if current in values:
                payload[field_name] = values[current]
    return upgraded


async def _op_already_satisfied(op: SessionOp, *, verify_exact: bool = False) -> bool:
    """Return whether an idempotent replay op already has its final state.

    An INSERT whose primary-key row exists already landed, even if the process
    died before marking its failure artifact recovered. A DELETE whose row is
    absent is likewise complete. Updates remain strict because absence cannot
    satisfy an update intent.
    """
    if op.op_type not in {"insert", "delete"}:
        return False
    meta = getattr(op.model_cls, "_meta", None)
    primary_keys = tuple(getattr(meta, "primary_keys", ()) or (op.pk_field,))
    if len(primary_keys) == 1:
        primary_key = primary_keys[0]
        primary_value = op.payload.get(primary_key, op.pk_value)
        filters = {primary_key: primary_value} if primary_value is not None else {}
    else:
        filters = {
            primary_key: op.payload.get(primary_key)
            for primary_key in primary_keys
            if op.payload.get(primary_key) is not None
        }
    if len(filters) != len(primary_keys):
        return False
    exists = await op.model_cls.exists(**filters)
    if op.op_type != "insert":
        return not exists
    if not exists:
        return False
    if not verify_exact:
        return True
    # Preserved immutable inserts must never mistake PK existence for recovery.
    # The exact comparator is shared with the live writer.
    rows = await op.model_cls.filter(**filters).limit(1).all()
    if not rows:
        return False
    differences = immutable_row_differences(rows[0], op.payload, table=op.table)
    if differences:
        raise ImmutableReplayConflictError(
            "immutable replay conflict: existing row differs from preserved payload "
            f"for {op.table} {op.pk_value}: {sorted(differences)}"
        )
    return True


_RECOVERED_BY_PEER = "recovered (by a concurrent replay)"

#: deadlock_detected, serialization_failure, lock_not_available: another writer held the row.
_LOCK_CONTENTION_SQLSTATES = frozenset({"40P01", "40001", "55P03"})


async def _rows_recovered_by_peer(rows: Sequence[Any]) -> bool:
    """Whether every failure row was already marked recovered by another sweep."""
    ids = [str(r["id"]) for r in rows]
    if not ids:
        return False
    open_rows = await _swf_model().filter(id__in=ids, recovered_at__isnull=True).values("id")
    return not open_rows


async def _settle_unique_collision(
    pending_ops: Sequence[SessionOp],
    group_rows: Sequence[Any],
    *,
    database: str | None,
    transaction: Any,
) -> str | None:
    """Settle a group whose replay hit a unique violation; ``None`` = not settled.

    1. A peer sweep already recovered every row → nothing to write.
    2. Otherwise each INSERT whose row now exists is satisfied — by PK existence
       for an ordinary capture, by the exact comparator (which honours
       database-assigned sentinels such as the append position) for an
       immutable capture. A differing immutable row still raises
       :class:`ImmutableReplayConflictError` (a real conflict).
    3. The ops left (UPDATEs and any insert still absent) are replayed once.
       Before 2026-11-11 every op was exact-verified, so an UPDATE in the group
       (never "satisfied") or a trigger-assigned column turned a landed write
       into a quarantine.
    """
    if await _rows_recovered_by_peer(group_rows):
        return _RECOVERED_BY_PEER
    immutable_targets = {
        _row_target(r)
        for r in group_rows
        if IMMUTABLE_WRITE_PRESERVED_MARKER in str(r.get("error_text", ""))
    }
    remaining: list[SessionOp] = []
    for op in pending_ops:
        exact = (op.table, str(op.pk_value)) in immutable_targets
        if not await _op_already_satisfied(op, verify_exact=exact):
            remaining.append(op)
    if not remaining:
        return "recovered (concurrent insert)"
    if any(op.op_type == "insert" for op in remaining):
        return None  # an insert collided yet its row is absent: not ours to call settled
    unmatched: list[SessionOp] = []
    token = _unmatched_updates.set(unmatched)
    try:
        async with transaction(database) if database else transaction():
            await execute_tiers(tier_ops(coalesce_ops(remaining)))
    finally:
        _unmatched_updates.reset(token)
    if unmatched:
        return None
    return "recovered (concurrent insert, updates re-applied)"


def _swf_model() -> Any:
    from matrx_ai.db._registry import get_model as get_db_model

    return get_db_model("SystemWriteFailure")


async def _fetch_pending(
    *,
    retry_errors: Sequence[str] | None,
    limit: int,
    max_attempts: int | None = None,
    ids: Sequence[str] | None = None,
    unreplayable: list[dict[str, Any]] | None = None,
) -> list[Any]:
    """Fetch unrecovered failure rows, optionally filtered by error_text.

    ``unreplayable`` (when given) receives every scanned row the
    ``retry_errors`` filter REFUSED, so the caller can settle it instead of
    leaving it below the attempt cap forever.

    Two-stage fetch:
      1. SELECT id+error_text only (small, fast) for ALL unrecovered rows.
         Filter by error_text in Python.
      2. SELECT the full payload columns ONLY for the eligible ids, in
         small batches. Avoids Supavisor's prepared-statement caching
         quirks on large multi-row SELECTs (which timed out in testing).

    ``max_attempts`` (when set) excludes rows that have already been retried
    that many times — the auto-replay loop's give-up boundary, so a permanent
    orphan is fetched at most ``max_attempts`` times and then left alone.

    ``ids`` (when set) restricts the sweep to exactly those failure rows — the
    per-row admin "Replay" button. Without it, a single-row retry has to be
    expressed as an error_text filter, which fans out to every unrelated row
    sharing that message.
    """
    Swf = _swf_model()
    id_qb = Swf.filter(recovered_at__isnull=True)
    if ids is not None:
        if not ids:
            return []
        id_qb = id_qb.filter(id__in=list(ids))
    if max_attempts is not None:
        id_qb = id_qb.filter(retry_count__lt=int(max_attempts))
    id_rows = await id_qb.order_by("failed_at").limit(int(limit)).values(
        "id",
        "op_type",
        "error_text",
        "request_id",
        "table_target",
        "retry_count",
        "failed_at",
        "user_id",
        "conversation_id",
        "primary_key",
    )
    if retry_errors is not None:
        # SUBSTRING match, not exact. A failure's error_text carries variable
        # per-row detail (e.g. a FK violation embeds the specific key/UUID), so
        # eligibility is keyed off an error-CLASS signature appearing anywhere
        # in the text. Exact-match would never catch the FK-ordering class.
        signatures = tuple(retry_errors)
        eligible_ids = []
        unmatched_updates: list[Any] = []
        waiting_inserts: set[tuple[str, str]] = set()
        for r in id_rows:
            timed_out = _is_query_timeout_capture_text(r["error_text"])
            if r["error_text"] and any(sig in r["error_text"] for sig in signatures) and (
                not timed_out or r.get("op_type") == "insert"
            ):
                # A timed-out capture is an unknown COMMIT. An INSERT is still safe: stage 2 reads
                # its primary key first and replays only a row that never landed (feedback f29cab05:
                # a chat.message insert lost to an overload burst was never retried).
                eligible_ids.append(r["id"])
                target = _row_target(r)
                if r.get("op_type") == "insert" and target is not None:
                    waiting_inserts.add(target)
            elif _is_unmatched_update(r):
                unmatched_updates.append(r)
            elif unreplayable is not None:
                unreplayable.append(dict(r))
        for r in unmatched_updates:
            if _row_target(r) in waiting_inserts or await _insert_already_landed(r):
                eligible_ids.append(r["id"])
            elif unreplayable is not None:
                unreplayable.append(dict(r))
    else:
        eligible_ids = [r["id"] for r in id_rows]
    if not eligible_ids:
        return []

    # Stage 2: per-id fetch (one round-trip per row keeps each query tiny
    # and avoids the array-binding Supavisor hiccup).
    out: list[Any] = []
    for row_id in eligible_ids:
        full_rows = await Swf.filter(id=row_id).values(
            "id",
            "op_id",
            "request_id",
            "table_target",
            "op_type",
            "primary_key",
            "payload",
            "depends_on",
            "error_text",
            "retry_count",
            "failed_at",
            "user_id",
            "conversation_id",
            "organization_id",
            "created_by",
        )
        if not full_rows:
            continue
        row = full_rows[0]
        if row.get("op_type") == "insert" and _is_query_timeout_capture_text(row.get("error_text")):
            if await _insert_already_landed(row):
                await _mark_recovered([row["id"]], "already_landed")
                continue
        out.append(row)
    return out


async def _mark_recovered(ids: Sequence[str], recovery_op_id: str) -> None:
    if not ids:
        return
    from datetime import UTC, datetime

    await _swf_model().update_where(
        {"id__in": list(ids)},
        recovered_at=datetime.now(UTC),
        recovery_op_id=recovery_op_id,
    )


async def _record_failed_attempt(
    rows: Sequence[Any], *, max_attempts: int | None, permanent: bool = False
) -> int:
    """Account for a failed replay of ``rows``: increment each row's
    ``retry_count``, and quarantine (jump ``retry_count`` to the cap) any row
    that has now exhausted its attempt budget or aged past the FK-race window.

    Returns the number of rows quarantined this call. When ``max_attempts`` is
    None (e.g. a manual/admin force-replay) rows are only incremented, never
    quarantined — a human asked for the retry, so don't silently give up.

    The quarantine signal is ``retry_count`` itself (NOT ``recovered_at``): the
    row was never written, so it stays honestly unrecovered, but both the
    auto-replay loop and the lifecycle watchdog bound their attention by
    ``retry_count < AUTO_REPLAY_MAX_ATTEMPTS``.

    ``permanent=True`` says the failure was a deterministic refusal
    (:data:`PERMANENT_FAILURE_SIGNATURES`): every row is quarantined on this
    very call, whatever its age or attempt count — waiting cannot change the
    answer.
    """
    if not rows:
        return 0
    from datetime import UTC, datetime

    now = datetime.now(UTC)
    bump_ids: list[str] = []
    giveup_ids: list[str] = []
    for r in rows:
        retry_count = r["retry_count"] or 0
        failed_at = r["failed_at"]
        age = (now - failed_at).total_seconds() if failed_at else 0.0
        if max_attempts is not None and (
            permanent or retry_count + 1 >= max_attempts or age > FK_RACE_MAX_AGE_SECONDS
        ):
            giveup_ids.append(r["id"])
        else:
            bump_ids.append(r["id"])

    from matrx_orm import F

    Swf = _swf_model()
    if bump_ids:
        # atomic column-relative increment — F() renders retry_count = retry_count + 1
        await Swf.filter(id__in=bump_ids).update(retry_count=F("retry_count") + 1)
    if giveup_ids and max_attempts is not None:
        await Swf.update_where({"id__in": giveup_ids}, retry_count=int(max_attempts))
    return len(giveup_ids)


async def _capture_replay_failure(
    exc: Exception,
    *,
    request_id: str,
    rows: Sequence[Any],
    phase: str,
    kind: str = "persistence_replay_failed",
) -> None:
    """Capture a replay failure at the boundary that intentionally absorbs it.

    ``kind`` is ``persistence_replay_quarantined`` when the sweep gave the rows
    up as permanent — exactly one such row per request group, ever, instead of
    one ``persistence_replay_failed`` per attempt.
    """
    try:
        from matrx_connect.streaming.error_capture import capture_error

        first = rows[0] if rows else {}
        safe_text = _safe_replay_failure_text(exc)
        captured_heads = _captured_failure_heads(rows)
        # A quarantine verdict alone ("Replay refused: …") is not a cause: name
        # the original failure it refused so the error class says WHY.
        if phase in {"unreplayable_class", "classify"} and captured_heads:
            safe_text = f"{safe_text} | captured: {captured_heads[0]}"
        safe_exc = RuntimeError(safe_text)
        await capture_error(
            safe_exc,
            kind=kind,
            route="matrx_ai.persistence.replay.replay_pending",
            error_type=type(exc).__name__,
            request_id=None if request_id == "_orphan" else request_id,
            user_id=first.get("user_id"),
            conversation_id=first.get("conversation_id"),
            context={
                "phase": phase,
                "failure_row_ids": [str(row["id"]) for row in rows],
                "table_targets": sorted({str(row["table_target"]) for row in rows}),
                "op_types": sorted({str(row.get("op_type")) for row in rows if row.get("op_type")}),
                "replay_error": safe_text,
                "captured_errors": captured_heads,
            },
        )
    except Exception:
        # The preserved system_write_failure rows remain authoritative. Error
        # capture is a safety-net signal and cannot block later replay groups.
        logger.exception("persistence_replay_error_capture_failed")


async def _quarantine_unreplayable(
    rows: Sequence[dict[str, Any]], report: ReplayReport, *, max_attempts: int | None
) -> None:
    """Settle rows no self-healing class covers: quarantine them, say so ONCE.

    A row the auto-replay will never attempt can only change by a human's hand,
    so it leaves the watchdog's hourly alarm (retry_count pinned at the cap —
    the same boundary both loops read) and lands as one
    ``persistence_replay_quarantined`` system_error per request group, with the
    rows still honestly unrecovered in the admin /persistence quarantine view,
    where a person can force-replay them.
    """
    by_request: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        # An INSERT whose row is already in its table was not lost: another writer (the
        # coding-session bridge re-sending its line, a client retry) landed it. Settle it
        # as recovered instead of quarantining a write that exists (feedback d231594e).
        if row.get("op_type") == "insert" and _row_target(row) is not None:
            try:
                if await _insert_already_landed(row):
                    await _mark_recovered([row["id"]], "already_landed")
                    continue
            except Exception as probe_exc:  # noqa: BLE001 — a failed probe falls through to quarantine
                vcprint(
                    f"[Replay] landed-check failed for {row.get('id')}: "
                    f"{type(probe_exc).__name__}: {probe_exc}",
                    color="red",
                )
        by_request.setdefault(str(row.get("request_id") or "_orphan"), []).append(row)
    for request_id, group_rows in by_request.items():
        reason = RuntimeError(
            "Replay refused: the captured failure matches no self-healing class "
            "(a deterministic refusal, or a write whose own completion is ambiguous), "
            "so re-sending it automatically cannot be trusted. Quarantined for a "
            "human (admin /persistence)."
        )
        await _capture_replay_failure(
            reason,
            request_id=request_id,
            rows=group_rows,
            phase="unreplayable_class",
            kind="persistence_replay_quarantined",
        )
        try:
            report.quarantined_count += await _record_failed_attempt(
                group_rows, max_attempts=max_attempts, permanent=True
            )
        except Exception as bump_exc:  # noqa: BLE001 — accounting must never crash the sweep
            vcprint(
                f"[Replay] failed to quarantine unreplayable request {request_id}: "
                f"{type(bump_exc).__name__}: {bump_exc}",
                color="red",
            )
            continue
        report.by_request[request_id] = "quarantined (unreplayable class)"
        vcprint(
            f"[Replay] QUARANTINED {len(group_rows)} unreplayable op(s) for request "
            f"{request_id} ({', '.join(sorted({str(r.get('table_target')) for r in group_rows}))})",
            color="yellow",
        )


async def replay_pending(
    *,
    dry_run: bool = True,
    retry_errors: Sequence[str] | None = DEFAULT_RETRY_ERRORS,
    limit: int = 500,
    database: str | None = None,
    max_attempts: int | None = None,
    ids: Sequence[str] | None = None,
) -> ReplayReport:
    """Read pending failures and try to land them.

    ``retry_errors=None`` skips error-class filtering — replays every
    unrecovered row regardless of cause. Use sparingly; the default
    restricts to the bug class fixed by the flush-sequentialization PR.

    ``ids`` restricts the sweep to those exact failure rows (the admin
    per-row Replay). It composes with ``retry_errors``; pass
    ``retry_errors=None`` alongside it to retry a specific row whatever
    its error class.

    Each ``request_id`` group is replayed as one transaction. If that
    transaction succeeds, every contributing failure row is marked
    ``recovered_at``. If it fails, the rows stay unrecovered and the
    new failure is captured by the same fallback path (which would
    re-fire the watchdog with a different error_text, surfacing it).
    """
    from matrx_orm import transaction
    from matrx_orm.core.config import get_all_database_project_names

    # Ensure every cx_ table has a Model bound in the persistence registry.
    # In a live request this happens inside get_coordinator() on first queue;
    # replay bypasses that path and needs explicit registration.
    from matrx_ai.persistence.queue_helpers import _ensure_cx_registered

    _ensure_cx_registered()

    if database is None:
        names = get_all_database_project_names()
        database = names[0] if names else "matrx"

    report = ReplayReport()

    # Phase 1: SELECT candidate failures. In AUTO mode (a give-up boundary, an
    # error-class filter, no hand-picked ids) the rows the filter refuses are
    # collected too: the sweep settles EVERY row the lifecycle watchdog watches,
    # never leaves one below the cap to alarm forever.
    settles_unreplayable = (
        not dry_run and max_attempts is not None and retry_errors is not None and ids is None
    )
    unreplayable: list[dict[str, Any]] = []
    rows = await _fetch_pending(
        retry_errors=retry_errors,
        limit=limit,
        max_attempts=max_attempts,
        ids=ids,
        unreplayable=unreplayable if settles_unreplayable else None,
    )
    if unreplayable:
        await _quarantine_unreplayable(unreplayable, report, max_attempts=max_attempts)

    report.candidates = len(rows)
    report.eligible = len(rows)
    if not rows:
        return report

    # Group by request_id; rows without a request_id form one synthetic
    # "_orphan" group so they still get replayed.
    by_request = _group_rows(rows)

    vcprint(
        f"[Replay] {len(rows)} eligible op(s) across {len(by_request)} request(s)"
        + (" (DRY RUN)" if dry_run else ""),
        color="cyan",
    )

    # Phase 2: per-request replay. Each request gets its own transaction so
    # one bad request can't poison the others.
    for request_id, group_rows in by_request.items():
        # REDACTED AT CAPTURE: a confidential conversation's failed op keeps only its
        # identity (the DB trigger dropped the rest), so there is nothing to re-send.
        # Quarantine the group once, naming why, instead of five ValueErrors.
        if (
            not dry_run
            and max_attempts is not None
            and any(is_sealed_redacted_row(r) for r in group_rows)
        ):
            report.still_failed_count += len(group_rows)
            reason = RuntimeError(
                "Replay refused: the captured payload belongs to a confidential "
                "conversation and was redacted on capture, so the write cannot be rebuilt. "
                "Quarantined for a human (admin /persistence)."
            )
            report.by_request[request_id] = "quarantined (confidential payload redacted)"
            await _capture_replay_failure(
                reason,
                request_id=request_id,
                rows=group_rows,
                phase="classify",
                kind="persistence_replay_quarantined",
            )
            try:
                report.quarantined_count += await _record_failed_attempt(
                    group_rows, max_attempts=max_attempts, permanent=True
                )
            except Exception as bump_exc:  # noqa: BLE001 — accounting must never crash the sweep
                vcprint(
                    f"[Replay] failed to quarantine redacted request {request_id}: "
                    f"{type(bump_exc).__name__}: {bump_exc}",
                    color="red",
                )
            continue

        # PERMANENT AT CAPTURE: the failure text already names a deterministic
        # refusal, so an attempt is pointless. Quarantine the group now (auto
        # mode only — a human's explicit retry still runs) and say so ONCE.
        if (
            not dry_run
            and max_attempts is not None
            and any(is_permanent_failure_text(r.get("error_text")) for r in group_rows)
        ):
            report.still_failed_count += len(group_rows)
            reason = RuntimeError(
                "Replay refused: the captured failure is a deterministic database "
                "refusal, not an outage — re-sending the same row cannot succeed. "
                "Quarantined for a human (admin /persistence)."
            )
            report.by_request[request_id] = "quarantined (permanent at capture)"
            vcprint(
                f"[Replay] QUARANTINED {len(group_rows)} op(s) for request {request_id} "
                f"without attempting: permanent refusal already recorded in error_text",
                color="yellow",
            )
            await _capture_replay_failure(
                reason,
                request_id=request_id,
                rows=group_rows,
                phase="classify",
                kind="persistence_replay_quarantined",
            )
            try:
                report.quarantined_count += await _record_failed_attempt(
                    group_rows, max_attempts=max_attempts, permanent=True
                )
            except Exception as bump_exc:  # noqa: BLE001 — accounting must never crash the sweep
                vcprint(
                    f"[Replay] failed to quarantine request {request_id}: "
                    f"{type(bump_exc).__name__}: {bump_exc}",
                    color="red",
                )
            continue

        try:
            group_rows = await _upgrade_legacy_payloads(group_rows)
            ops = [_row_to_op(r) for r in group_rows]
            pending_ops = []
            for op, row in zip(ops, group_rows, strict=True):
                immutable = IMMUTABLE_WRITE_PRESERVED_MARKER in str(row.get("error_text", ""))
                satisfied = (
                    await _op_already_satisfied(op, verify_exact=True)
                    if immutable
                    else await _op_already_satisfied(op)
                )
                if not satisfied:
                    pending_ops.append(op)
        except Exception as exc:
            immutable_rows = [
                row for row in group_rows
                if IMMUTABLE_WRITE_PRESERVED_MARKER in str(row.get("error_text", ""))
            ]
            if immutable_rows and "immutable replay conflict" in str(exc):
                report.still_failed_count += len(group_rows)
                report.conflict_count += len(immutable_rows)
                report.by_request[request_id] = (
                    "would-quarantine (immutable conflict)" if dry_run else "quarantined (immutable conflict)"
                )
                if not dry_run:
                    await _capture_replay_failure(
                        exc, request_id=request_id, rows=group_rows, phase="exact-verify",
                        kind="persistence_replay_quarantined",
                    )
                    report.quarantined_count += await _record_failed_attempt(
                        group_rows, max_attempts=max_attempts, permanent=True
                    )
                continue
            report.still_failed_count += len(group_rows)
            report.by_request[request_id] = f"failed: replay preparation: {exc}"
            report.errors.append(f"{request_id}: prepare {exc}")
            await _capture_replay_failure(
                exc, request_id=request_id, rows=group_rows, phase="prepare"
            )
            continue

        try:
            # ``tier_ops`` keeps ONE op per row: an INSERT and an UPDATE of a row must
            # be one op before it, or the INSERT vanishes and is marked recovered.
            tiers = tier_ops(coalesce_ops(pending_ops))
        except Exception as exc:
            report.still_failed_count += len(group_rows)
            report.by_request[request_id] = f"failed: DAG: {exc}"
            report.errors.append(f"{request_id}: dag {exc}")
            await _capture_replay_failure(
                exc, request_id=request_id, rows=group_rows, phase="dag"
            )
            continue

        if dry_run:
            report.recovered_count += len(group_rows)
            report.by_request[request_id] = "would-recover"
            continue

        recovery_op_id = str(uuid4())
        try:
            # An UPDATE of a row that is not there commits "successfully" and changes
            # nothing: collected here, and never called recovered.
            unmatched: list[SessionOp] = []
            if pending_ops:
                unmatched_token = _unmatched_updates.set(unmatched)
                try:
                    async with transaction(database) if database else transaction():
                        await execute_tiers(tiers)
                finally:
                    _unmatched_updates.reset(unmatched_token)
            unmatched_pks = {str(op.pk_value) for op in unmatched}
            still_unmatched = [
                r for r in group_rows
                if r.get("op_type") == "update" and (_row_target(r) or ("", ""))[1] in unmatched_pks
            ]
            landed = [r for r in group_rows if not any(r is s for s in still_unmatched)]
            # Mark the rows recovered outside the replay transaction so we
            # don't block the replay path.
            await _mark_recovered([r["id"] for r in landed], recovery_op_id)
            report.recovered_count += len(landed)
            if still_unmatched:
                # What landed is settled; the rest takes the failed-attempt path below.
                group_rows = still_unmatched
                raise LookupError(
                    f"{len(still_unmatched)} UPDATE(s) matched no row on replay: "
                    "the row is not there and nothing was written"
                )
            report.by_request[request_id] = "recovered"
            vcprint(
                f"[Replay] recovered {len(group_rows)} op(s) for request {request_id} "
                f"(recovery_op_id={recovery_op_id})",
                color="green",
            )
        except Exception as exc:
            if db_sqlstate(exc) == "23505":
                # A unique collision means ANOTHER writer landed one of these rows between
                # the pre-insert probe and the INSERT: a concurrent replay sweep (one per
                # server task) or the live writer whose "timed-out" commit actually landed.
                # The intent is idempotent, so settle it, never quarantine it (2026-11-10,
                # request dd82cc0c: two sweeps quarantined a message a third had just landed).
                try:
                    verdict = await _settle_unique_collision(
                        pending_ops, group_rows, database=database, transaction=transaction
                    )
                    if verdict is not None:
                        if verdict != _RECOVERED_BY_PEER:
                            await _mark_recovered([r["id"] for r in group_rows], recovery_op_id)
                        report.recovered_count += len(group_rows)
                        report.by_request[request_id] = verdict
                        continue
                except Exception as verify_exc:
                    exc = verify_exc
            if db_sqlstate(exc) in _LOCK_CONTENTION_SQLSTATES:
                # LOCK CONTENTION IS A PEER, NOT A FAILURE (2026-11-12, sec_f2d07e…): every server
                # process runs its own sweep, so two sweeps reach the same group together and the
                # loser waits out lock_timeout on the row the winner is writing. On 2026-11-10 two
                # sweeps each filed persistence_replay_failed for failure row c24828b1 at 00:17:06/07
                # and the third landed it at 00:17:07.68. The attempt is still counted (a row that
                # never lands still reaches the quarantine), but only a quarantine is filed.
                if await _rows_recovered_by_peer(group_rows):
                    report.recovered_count += len(group_rows)
                    report.by_request[request_id] = _RECOVERED_BY_PEER
                    continue
                report.still_failed_count += len(group_rows)
                report.by_request[request_id] = "deferred: a concurrent writer held the row"
                if not dry_run:
                    gave_up = 0
                    try:
                        gave_up = await _record_failed_attempt(group_rows, max_attempts=max_attempts)
                    except Exception as bump_exc:  # noqa: BLE001 — accounting must never crash the sweep
                        vcprint(
                            f"[Replay] failed to record attempt for request "
                            f"{request_id}: {type(bump_exc).__name__}: {bump_exc}",
                            color="red",
                        )
                    if gave_up:
                        report.quarantined_count += gave_up
                        report.by_request[request_id] = f"quarantined: {type(exc).__name__}"
                        await _capture_replay_failure(
                            exc, request_id=request_id, rows=group_rows, phase="execute",
                            kind="persistence_replay_quarantined",
                        )
                continue
            report.still_failed_count += len(group_rows)
            safe_error = _safe_replay_failure_text(exc)
            report.by_request[request_id] = f"failed: {safe_error}"
            report.errors.append(f"{request_id}: {safe_error}")
            vcprint(
                f"[Replay] FAILED for request {request_id}: {safe_error}",
                color="red",
            )
            # A deterministic refusal (trigger RAISE, constraint, schema drift)
            # is quarantined on THIS attempt in auto mode: no second sweep, no
            # second system_error row. Everything else burns its attempt budget.
            permanent = max_attempts is not None and is_permanent_failure_exception(exc)
            # ONE system_error per failing write, not one per attempt (live 2026-11-14: one orphan
            # chat.tool_call insert retried five times filed five rows). A recoverable failure is
            # filed on the write's FIRST attempt only; the later sweeps of the same write stay
            # silent (the row's retry_count and the quarantine state carry the rest). A human's
            # explicit retry (max_attempts None) always files, and so does a permanent verdict.
            first_attempt = all(int(r.get("retry_count") or 0) == 0 for r in group_rows)
            if permanent or max_attempts is None or first_attempt:
                await _capture_replay_failure(
                    exc,
                    request_id=request_id,
                    rows=group_rows,
                    phase="execute",
                    kind="persistence_replay_quarantined" if permanent else "persistence_replay_failed",
                )
            # Record the failed attempt so a permanent orphan stops being
            # retried forever (and the watchdog stops alerting on it). No-op
            # accounting for dry runs.
            if not dry_run:
                try:
                    gave_up = await _record_failed_attempt(
                        group_rows, max_attempts=max_attempts, permanent=permanent
                    )
                    report.quarantined_count += gave_up
                    if gave_up:
                        report.by_request[request_id] = (
                            f"quarantined (permanent): {type(exc).__name__}"
                        )
                except Exception as bump_exc:  # noqa: BLE001 — accounting must never crash the sweep
                    vcprint(
                        f"[Replay] failed to record attempt for request "
                        f"{request_id}: {type(bump_exc).__name__}: {bump_exc}",
                        color="red",
                    )

    return report


async def run_auto_replay_loop(
    *,
    interval_secs: float = DEFAULT_AUTO_REPLAY_INTERVAL_SECS,
    limit: int = DEFAULT_AUTO_REPLAY_LIMIT,
    retry_errors: Sequence[str] | None = RECOVERABLE_RETRY_ERRORS,
    database: str | None = None,
    max_attempts: int = AUTO_REPLAY_MAX_ATTEMPTS,
) -> None:
    """Periodically self-heal SELF-HEALING write failures from
    ``system_write_failure`` so the app never has to think about cross-session
    write ordering.

    This is the recovery counterpart to the lifecycle watchdog: the watchdog
    *detects + alerts* on stuck rows; this loop *fixes* the subset that is
    structurally recoverable (FK-ordering races, transient asyncpg collisions).
    A row only survives a sweep if it is a genuine bug the platform should NOT
    silently paper over — that's exactly when a human should look.

    Cancel the task to stop. The outer guard keeps the loop alive across any
    transient failure (sleep, retry); only cancellation stops it.
    """
    import asyncio

    vcprint(
        f"[Replay] Auto-replay loop started (every {interval_secs:.0f}s, "
        f"batch {limit}, classes={len(retry_errors or ())}, "
        f"give-up after {max_attempts} attempts)",
        color="green",
    )
    while True:
        try:
            # Disk-spill drain runs FIRST each tick: re-land any ops that were
            # spilled to disk during a total DB outage (record_failures couldn't
            # even reach system_write_failure) back INTO system_write_failure, so
            # the replay below then re-applies them to the real tables. The first
            # tick (at boot) is the "startup drain"; every tick after is the
            # periodic watcher — one wiring point covers both. Best-effort.
            try:
                from matrx_orm import drain_spilled_ops

                await drain_spilled_ops(database=database)
            except Exception as drain_exc:  # noqa: BLE001 — never kill the loop
                vcprint(
                    f"[Replay] disk-spill drain raised {type(drain_exc).__name__}: "
                    f"{drain_exc} — continuing",
                    color="yellow",
                )

            report = await replay_pending(
                dry_run=False,
                retry_errors=retry_errors,
                limit=limit,
                database=database,
                max_attempts=max_attempts,
            )
            if report.recovered_count or report.still_failed_count:
                msg = (
                    f"[Replay] Auto-replay swept {report.candidates} eligible op(s): "
                    f"{report.recovered_count} recovered, "
                    f"{report.still_failed_count} still failed"
                )
                if report.quarantined_count:
                    msg += (
                        f", {report.quarantined_count} given up as PERMANENT "
                        f"(no longer retried/alerted — inspect via /admin persistence)"
                    )
                vcprint(
                    msg,
                    color="green" if not report.still_failed_count else "yellow",
                )
        except asyncio.CancelledError:
            vcprint("[Replay] Auto-replay loop stopping", color="green")
            raise
        except Exception as exc:  # noqa: BLE001 — loop must never die on a tick
            vcprint(
                f"[Replay] Auto-replay tick raised {type(exc).__name__}: {exc} "
                f"— continuing after interval",
                color="red",
            )
            logger.exception("auto_replay_tick_failed")
        try:
            await asyncio.sleep(interval_secs)
        except asyncio.CancelledError:
            vcprint("[Replay] Auto-replay loop stopping", color="green")
            raise
