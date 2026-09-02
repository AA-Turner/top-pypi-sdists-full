"""_db_hints — agent-facing DB error hints, rewrite safety, auto-heal gate.

Fixtures replay the real misses from conversation 2e7c9ff2 (2026-07-05):
``public.content_block`` (singular/plural), ``c.label`` (wrong column), and a
guessed ``description`` column.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools import db_hints as _db_hints
from matrx_ai.tools.db_hints import (
    DbErrorFacts,
    autoheal_candidate,
    build_hint,
    parse_db_error,
    parse_from_join,
    rewrite_table_ref,
    strip_ansi,
)

# ── canned schema world ──────────────────────────────────────────────────────

SCHEMAS = ["admin", "chat", "platform", "public"]
TABLES = {
    "public": ["content_blocks", "user_secrets"],
    "admin": ["admins"],
    "platform": ["categories", "gizmo_categories", "shareable_resource_registry"],
    "chat": ["conversation_value"],
}
COLUMNS = {
    "platform.categories": frozenset({"id", "name", "slug", "metadata", "parent_id"}),
    "public.content_blocks": frozenset({"id", "label", "category_id", "content"}),
}


async def app_schemas() -> list[str]:
    return SCHEMAS


async def tables_by_schema() -> dict[str, list[str]]:
    return TABLES


async def schemas_for_table(name: str) -> list[str]:
    return [s for s, tables in TABLES.items() if name in tables]


async def get_table_columns(schema: str, name: str) -> frozenset[str]:
    return COLUMNS.get(f"{schema}.{name}", frozenset())


RESOLVERS = dict(
    app_schemas=app_schemas,
    tables_by_schema=tables_by_schema,
    schemas_for_table=schemas_for_table,
    get_table_columns=get_table_columns,
)


class _OrmishError(Exception):
    """Duck-typed matrx-orm DatabaseError: details dict + agent_message()."""

    def __init__(self, message: str, details: dict):
        super().__init__(message)
        self.details = details
        self._msg = message

    def agent_message(self) -> str:
        return self._msg


# ── parse_db_error ───────────────────────────────────────────────────────────


class TestParseDbError:
    def test_structured_path(self):
        exc = _OrmishError(
            "Table / relation does not exist: relation \"public.content_block\" does not exist",
            {
                "kind": "table",
                "sqlstate": "42P01",
                "missing_table": "content_block",
                "missing_schema": "public",
                "missing_column": None,
                "column_qualifier": None,
                "pg_suggestion": None,
            },
        )
        facts = parse_db_error(exc)
        assert facts.kind == "table"
        assert facts.missing_table == "content_block"
        assert facts.missing_schema == "public"

    def test_fallback_text_path(self):
        facts = parse_db_error(Exception('relation "public.content_block" does not exist'))
        assert facts.kind == "table"
        assert facts.missing_table == "content_block"
        assert facts.missing_schema == "public"

    def test_fallback_column_alias(self):
        facts = parse_db_error(Exception("column c.label does not exist"))
        assert facts.kind == "column"
        assert facts.missing_column == "label"
        assert facts.column_qualifier == "c"

    def test_ansi_stripped_and_bounded(self):
        big = "\x1b[91m" + "x" * 2000 + "\x1b[0m"
        facts = parse_db_error(Exception(big))
        assert "\x1b[" not in facts.message
        assert len(facts.message) <= 501 + 1

    def test_strip_ansi(self):
        assert strip_ansi("\x1b[91mred\x1b[0m") == "red"


# ── parse_from_join ──────────────────────────────────────────────────────────


class TestParseFromJoin:
    def test_alias_map(self):
        q = (
            "SELECT c.id, count(b.id) FROM platform.categories c "
            "LEFT JOIN public.content_blocks b ON b.category_id = c.id"
        )
        m = parse_from_join(q)
        assert m["c"] == "platform.categories"
        assert m["b"] == "public.content_blocks"
        assert m["categories"] == "platform.categories"

    def test_as_keyword_and_keywords_not_aliases(self):
        m = parse_from_join("SELECT * FROM admin.admins AS a WHERE a.id = 1")
        assert m["a"] == "admin.admins"
        m2 = parse_from_join("SELECT * FROM admin.admins WHERE id = 1")
        assert "where" not in m2

    def test_literals_masked(self):
        m = parse_from_join("SELECT * FROM admins WHERE note = 'FROM fake_table x'")
        assert "fake_table" not in m.values()


# ── build_hint scenarios ─────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestBuildHint:
    async def test_wrong_table_in_existing_schema(self):
        facts = parse_db_error(Exception('relation "public.content_block" does not exist'))
        msg, action = await build_hint(facts, "SELECT * FROM public.content_block", **RESOLVERS)
        assert "content_blocks" in msg  # close match surfaced
        assert "public.content_blocks" in action
        assert "\x1b[" not in msg

    async def test_wrong_schema(self):
        facts = parse_db_error(Exception('schema "platfrm" does not exist'))
        msg, action = await build_hint(facts, "SELECT * FROM platfrm.categories", **RESOLVERS)
        assert "platform" in msg and "public" in msg and "chat" in msg
        assert "platform" in action

    async def test_table_exists_elsewhere(self):
        ref = "public" + ".gizmo_categories"  # split so schema guards don't read it as a live ref
        facts = parse_db_error(Exception(f'relation "{ref}" does not exist'))
        msg, action = await build_hint(facts, f"SELECT * FROM {ref}", **RESOLVERS)
        assert "platform" in msg

    async def test_column_with_alias_returns_single_table_columns(self):
        facts = parse_db_error(Exception("column c.label does not exist"))
        q = (
            "SELECT c.label FROM platform.categories c "
            "LEFT JOIN public.content_blocks b ON b.category_id = c.id"
        )
        msg, _ = await build_hint(facts, q, **RESOLVERS)
        assert "platform.categories" in msg
        assert "name" in msg and "slug" in msg
        # Only the aliased table's columns, not the join partner's.
        assert "public.content_blocks:" not in msg.replace("Columns of public.content_blocks", "X")

    async def test_unqualified_column_falls_back_to_from_tables(self):
        facts = parse_db_error(Exception('column "description" does not exist'))
        msg, _ = await build_hint(
            facts, "SELECT id, description FROM platform.categories", **RESOLVERS
        )
        assert "Columns of platform.categories" in msg

    async def test_pg_suggestion_passthrough(self):
        facts = DbErrorFacts(
            kind="column",
            message="column c.label does not exist",
            missing_column="label",
            column_qualifier="c",
            pg_suggestion="c.name",
        )
        msg, action = await build_hint(facts, "SELECT c.label FROM platform.categories c", **RESOLVERS)
        assert 'c.name' in msg
        assert 'c.name' in action

    async def test_resolver_failure_degrades_gracefully(self):
        async def boom() -> list[str]:
            raise RuntimeError("no db")

        facts = parse_db_error(Exception('schema "platfrm" does not exist'))
        msg, action = await build_hint(
            facts,
            "SELECT 1",
            app_schemas=boom,
            tables_by_schema=tables_by_schema,
            schemas_for_table=schemas_for_table,
            get_table_columns=get_table_columns,
        )
        assert "platfrm" in msg  # original message survives
        assert action  # generic action

    async def test_message_bounded(self):
        many = {"public": [f"table_{i:04d}" for i in range(400)]}

        async def big_tables() -> dict[str, list[str]]:
            return many

        facts = parse_db_error(Exception('relation "public.nope" does not exist'))
        msg, _ = await build_hint(
            facts,
            "SELECT * FROM public.nope",
            app_schemas=app_schemas,
            tables_by_schema=big_tables,
            schemas_for_table=schemas_for_table,
            get_table_columns=get_table_columns,
        )
        assert len(msg) <= _db_hints.AGENT_DB_ERROR_MAX_CHARS + 1
        assert "too many to list" in msg or "more" in msg


# ── rewrite safety ───────────────────────────────────────────────────────────


class TestRewriteTableRef:
    def test_qualified_from(self):
        q = "SELECT * FROM public.content_block WHERE id = 'x'"
        out = rewrite_table_ref(q, "public.content_block", "public.content_blocks")
        assert out == "SELECT * FROM public.content_blocks WHERE id = 'x'"

    def test_join_position(self):
        q = "SELECT * FROM a JOIN public.content_block b ON b.id = a.bid"
        out = rewrite_table_ref(q, "public.content_block", "public.content_blocks")
        assert "JOIN public.content_blocks b" in out

    def test_string_literal_untouched(self):
        q = "SELECT * FROM public.content_block WHERE note = 'public.content_block'"
        out = rewrite_table_ref(q, "public.content_block", "public.content_blocks")
        assert out is not None
        assert "FROM public.content_blocks" in out
        assert "'public.content_block'" in out  # literal preserved

    def test_column_ref_not_rewritten(self):
        # bare table name also appears as alias-qualified column elsewhere
        q = "SELECT x.agent FROM agent WHERE x.agent = 1"
        out = rewrite_table_ref(q, "agent", "agents")
        assert out is not None
        assert "FROM agents" in out
        assert "x.agent " in out and "x.agent =" in out

    def test_no_occurrence_returns_none(self):
        assert rewrite_table_ref("SELECT 1", "nope", "nopes") is None

    def test_same_ref_returns_none(self):
        assert rewrite_table_ref("SELECT * FROM t", "t", "t") is None

    def test_comma_from_list_stage_b(self):
        q = "SELECT * FROM a, content_block WHERE a.id = content_block.aid"
        out = rewrite_table_ref(q, "content_block", "content_blocks")
        assert out is not None
        assert "a, content_blocks" in out
        # dotted qualifier occurrence: content_block.aid — the token after the
        # rewrite must reference the corrected name or stay consistent; Stage B
        # replaces the bare token, and `content_block.aid` starts a token match
        # too (not preceded by dot) — verify both got corrected.
        assert "content_blocks.aid" in out


# ── auto-heal candidate gate ─────────────────────────────────────────────────


@pytest.mark.asyncio
class TestAutohealCandidate:
    async def test_plural_singular_single_candidate(self):
        facts = parse_db_error(Exception('relation "public.content_block" does not exist'))
        cand = await autoheal_candidate(
            facts, schemas_for_table=schemas_for_table, tables_by_schema=tables_by_schema
        )
        assert cand == "public.content_blocks"

    async def test_wrong_schema_exact_name_single_candidate(self):
        ref = "public" + ".gizmo_categories"
        facts = parse_db_error(Exception(f'relation "{ref}" does not exist'))
        cand = await autoheal_candidate(
            facts, schemas_for_table=schemas_for_table, tables_by_schema=tables_by_schema
        )
        assert cand == "platform.gizmo_categories"

    async def test_ambiguous_refused(self):
        tables = {
            "public": ["agents", "agent_x"],
            "platform": ["agent"],
        }

        async def tbs() -> dict[str, list[str]]:
            return tables

        async def sft(name: str) -> list[str]:
            return [s for s, ts in tables.items() if name in ts]

        # bare 'agent' miss: exists exactly in platform (exact candidate) AND
        # fuzzy-matches public.agents → two candidates → refuse.
        facts = parse_db_error(Exception('relation "agent" does not exist'))
        cand = await autoheal_candidate(facts, schemas_for_table=sft, tables_by_schema=tbs)
        assert cand is None

    async def test_column_error_never_heals(self):
        facts = parse_db_error(Exception("column c.label does not exist"))
        cand = await autoheal_candidate(
            facts, schemas_for_table=schemas_for_table, tables_by_schema=tables_by_schema
        )
        assert cand is None

    async def test_low_similarity_refused(self):
        facts = parse_db_error(Exception('relation "public.zzz_nothing" does not exist'))
        cand = await autoheal_candidate(
            facts, schemas_for_table=schemas_for_table, tables_by_schema=tables_by_schema
        )
        assert cand is None
