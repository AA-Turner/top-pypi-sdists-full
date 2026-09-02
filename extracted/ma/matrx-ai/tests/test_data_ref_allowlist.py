"""DataRef allowlist fail-closed default (adversarial review #13).

``_TableSpec.fields_allowed=None`` historically meant "all allowed" and
BYPASSED the sort/filter/field-name allowlists — the sort term is interpolated
verbatim into ORDER BY, so any future table registered without an allowlist
would silently reopen the injection surface. The default is now fail-closed:
None permits full-row OUTPUT projection only; sorting/filtering/field-refs are
REFUSED with a loud error naming the fix.
"""

from __future__ import annotations

import pytest

from matrx_ai.db.content_types.data_ref import (
    ALLOWED_TABLES,
    DataRefSort,
    DbFieldRef,
    DbQueryRef,
    _TableSpec,
    resolve_data_ref,
)


@pytest.fixture
def unlisted_table():
    """Register a spec WITHOUT fields_allowed (the future-table landmine)."""
    key = "_test_no_allowlist"
    ALLOWED_TABLES[key] = _TableSpec(
        label="TestNoAllowlist",
        table_name="public.test_no_allowlist",
        model_key="TestNoAllowlist",
        fields_allowed=None,
    )
    try:
        yield key
    finally:
        ALLOWED_TABLES.pop(key, None)


async def test_sort_refused_without_allowlist(unlisted_table):
    ref = DbQueryRef.model_construct(
        ref_type="db_query",
        table=unlisted_table,
        sort=DataRefSort(field="id); DROP TABLE x; --", direction="asc"),
    )
    with pytest.raises(ValueError, match="REFUSED"):
        await resolve_data_ref(ref)


async def test_filter_refused_without_allowlist(unlisted_table):
    ref = DbQueryRef.model_construct(
        ref_type="db_query", table=unlisted_table, filter={"anything": "x"}
    )
    with pytest.raises(ValueError, match="REFUSED"):
        await resolve_data_ref(ref)


async def test_field_ref_refused_without_allowlist(unlisted_table):
    ref = DbFieldRef.model_construct(
        ref_type="db_field",
        table=unlisted_table,
        id="some-id",
        field_name="secret_col",
    )
    with pytest.raises(ValueError, match="REFUSED"):
        await resolve_data_ref(ref)


def test_every_registered_table_declares_an_allowlist():
    """The 4 shipped tables must keep explicit allowlists (query shaping keeps
    working); a new table added without one trips the runtime refusal above,
    and this test documents the expectation at registration time."""
    for key, spec in ALLOWED_TABLES.items():
        assert spec.fields_allowed, f"{key} must declare fields_allowed"


async def test_sort_field_outside_allowlist_still_refused():
    """Existing behavior preserved: a listed table refuses an unlisted sort
    field (validated BEFORE any model/DB access)."""
    ref = DbQueryRef(
        ref_type="db_query",
        table="notes",
        sort={"field": "owner_id", "direction": "desc"},
    )
    with pytest.raises(ValueError, match="not in the allowlist"):
        await resolve_data_ref(ref)
