"""ONE strict parser for a CHECK's allowed values (``db_hints.allowed_values_from_check``).

The sql tool (schema action + refusal note) and aidream's data catalog read the same function.
A CHECK names its allowed set only when it is EXACTLY one pick-list on one column; the loose
predecessor read the first list it found, so ``kind = ANY(ARRAY['a']) OR y = ANY(ARRAY['z'])``
reported ``['a']`` as kind's whole vocabulary (review of 4bd5fece59, 2026-11-12).
aidream's twin, ``aidream/services/agent_data/tests/test_one_allowed_values_parser.py``, runs
these CASES through ``registry.check_constraint_choices``.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools import db_hints

#: (definition, column, allowed). ``column`` is what a column-aware caller passes; the
#: refusal note passes none, and gets the same answer.
CASES: list[tuple[str, str, list[str]]] = [
    ("CHECK ((status = ANY (ARRAY['a'::text, 'b'::text])))", "status", ["a", "b"]),
    ("CHECK (((d IS NULL) OR (d = ANY (ARRAY['easy'::text, 'hard'::text]))))", "d", ["easy", "hard"]),
    ("CHECK (((kind)::text = ANY ((ARRAY['a'::character varying, 'it''s'::character varying])::text[])))",
     "kind", ["a", "it's"]),
    ("CHECK (mode IN ('x', 'y'))", "mode", ["x", "y"]),
    ("CHECK ((roles <@ ARRAY['member'::text, 'incorporator'::text]))", "roles", ["member", "incorporator"]),
    # Compound: never a pick-list, whichever column.
    ("CHECK (((kind = ANY (ARRAY['a'::text])) OR (y = ANY (ARRAY['z'::text]))))", "kind", []),
    ("CHECK (((status = ANY (ARRAY['a'::text])) AND (length(status) > 0)))", "status", []),
    ("CHECK (((roles <@ ARRAY['a'::text]) AND (cardinality(roles) > 0)))", "roles", []),
    # Negations and patterns name forbidden values, never allowed ones.
    ("CHECK ((NOT (kind IN ('a', 'b'))))", "kind", []),
    ("CHECK ((kind <> ALL (ARRAY['a'::text, 'b'::text])))", "kind", []),
    ("CHECK ((status <> 'deleted'::text))", "status", []),
    ("CHECK ((code ~ '^[A-Z]{3}$'::text))", "code", []),
    ("CHECK (((p >= 0) AND (p <= 100)))", "p", []),
    # Two different columns in one CHECK.
    ("CHECK (((other IS NULL) OR (mode = ANY (ARRAY['x'::text]))))", "mode", []),
]


@pytest.mark.parametrize(("definition", "column", "allowed"), CASES)
def test_column_aware_caller(definition: str, column: str, allowed: list[str]) -> None:
    assert db_hints.allowed_values_from_check(definition, column=column) == allowed


@pytest.mark.parametrize(("definition", "column", "allowed"), CASES)
def test_refusal_note_caller_passes_no_column(definition: str, column: str, allowed: list[str]) -> None:
    assert db_hints.allowed_values_from_check(definition) == allowed


def test_another_columns_list_is_never_this_columns() -> None:
    assert db_hints.allowed_values_from_check(CASES[0][0], column="kind") == []


def test_the_cap_bounds_the_list_and_none_keeps_every_value() -> None:
    many = "CHECK ((k = ANY (ARRAY[" + ", ".join(f"'v{i}'::text" for i in range(60)) + "])))"
    assert len(db_hints.allowed_values_from_check(many)) == 40
    assert len(db_hints.allowed_values_from_check(many, cap=None)) == 60
