"""Wave 3 slice 2 — ``resolve_kind("table:<uuid>")``: the one resolver, its memo, its refusal.

KINDS-GLUE wave 3 §1.2–1.3. A fake host reader stands in for matrx-records' ``table_kind_reader``
(the live leg, as admin@admin.com and test@test.com, is aidream
``aidream/services/kind_records/tests/test_record_as_kind_live.py``). Data is random generic.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_graph import kinds
from matrx_graph.db import _registry
from matrx_graph.kinds import KindDegradedReason, check_against_kind, resolve_kind, resolve_kind_edges
from matrx_graph.table_kinds import TableKindRefused, table_kind_slug

OPEN = str(uuid.uuid4())
LOCKED = str(uuid.uuid4())
SENTENCE = "You do not have access to this table, so custom.table_kind_facts has nothing to show you."


def _facts(table_id: str) -> dict[str, Any]:
    return {
        "organization_id": str(uuid.uuid4()),
        "table_id": table_id,
        "name": "amber list",
        "version": 3,
        "stamp": "s-1",
        "column_source": "fields",
        "platform_keys": [],
        "fields": [
            {"key": "word", "type": "text", "required": True, "id": str(uuid.uuid4()), "version": 1},
            {"key": "size", "type": "number", "id": str(uuid.uuid4()), "version": 1},
        ],
        "choices": {},
    }


calls_people: list[list[tuple[Any, Any]]] = [[]]


@pytest.fixture
def reads(monkeypatch) -> list[str]:
    calls: list[str] = []
    people: list[tuple[Any, Any]] = []

    async def reader(table_id: str, **who: Any) -> dict[str, Any]:
        calls.append(table_id)
        people.append((who.get("user_id"), who.get("organization_id")))
        if table_id == LOCKED:
            raise TableKindRefused(SENTENCE)
        return _facts(table_id)

    monkeypatch.setitem(_registry._extras, "table_kind_reader", reader)
    kinds.invalidate_kind_catalog_cache()
    calls_people[0] = people
    return calls


def _request(monkeypatch, request_id: str) -> None:
    from types import SimpleNamespace

    import matrx_connect.context.app_context as app_context

    monkeypatch.setattr(
        app_context, "try_get_app_context", lambda: SimpleNamespace(request_id=request_id, user_id="u-1", organization_id="o-1")
    )


async def test_a_table_kind_resolves_live_with_its_stored_schema(reads, monkeypatch) -> None:
    _request(monkeypatch, "")
    entry, reason = await resolve_kind(table_kind_slug(OPEN))
    assert reason is None and entry is not None
    assert entry.disposition == "record" and entry.stamp == "s-1" and entry.version == 3
    assert entry.json_schema["properties"]["word"] == {"type": "string"}
    assert await resolve_kind_edges(table_kind_slug(OPEN)) == ()
    good = await check_against_kind({"__kind": table_kind_slug(OPEN), "word": "birch", "size": 4}, table_kind_slug(OPEN))
    bad = await check_against_kind({"__kind": table_kind_slug(OPEN), "word": 5}, table_kind_slug(OPEN))
    assert good.checked and not good.errors
    assert bad.checked and bad.errors


async def test_a_refused_table_carries_the_stores_sentence_and_is_never_a_pass(reads, monkeypatch) -> None:
    _request(monkeypatch, "")
    entry, reason = await resolve_kind(table_kind_slug(LOCKED))
    assert reason is KindDegradedReason.KIND_NOT_READABLE
    assert entry is not None and entry.refusal == SENTENCE and entry.json_schema is None
    check = await check_against_kind({"word": "x"}, table_kind_slug(LOCKED))
    assert check.checked is False and check.refusal == SENTENCE
    assert kinds.degraded_escalation(KindDegradedReason.KIND_NOT_READABLE) == "fatal"


async def test_nothing_is_cached_without_a_request_and_one_request_reads_once(reads, monkeypatch) -> None:
    slug = table_kind_slug(OPEN)
    _request(monkeypatch, "")
    await resolve_kind(slug)
    await resolve_kind(slug)
    assert len(reads) == 2, "with no request id every call reads"
    _request(monkeypatch, "req-a")
    for _ in range(5):
        await resolve_kind(slug)
    assert len(reads) == 3, "one request reads a Table once"
    _request(monkeypatch, "req-b")
    await resolve_kind(slug)
    assert len(reads) == 4, "another request reads again"
    assert slug not in kinds._cache, "a table kind never enters the process-wide registry cache"


async def test_two_people_in_one_request_never_share_an_answer(reads, monkeypatch) -> None:
    """The memo names the person the read RUNS AS, with the organization, never the slug alone."""
    from matrx_graph.table_kinds import read_table_kind

    slug = table_kind_slug(OPEN)
    one, two = str(uuid.uuid4()), str(uuid.uuid4())
    org_a, org_b = str(uuid.uuid4()), str(uuid.uuid4())
    _request(monkeypatch, "req-two-people")
    await read_table_kind(slug, user_id=one, organization_id=org_a)
    await read_table_kind(slug, user_id=two, organization_id=org_a)
    await read_table_kind(slug, user_id=one, organization_id=org_b)
    assert len(reads) == 3, "each person, and each organization, reads for themselves"
    await read_table_kind(slug, user_id=one, organization_id=org_a)
    await read_table_kind(slug)  # the carried person (u-1 in o-1)
    await read_table_kind(slug, organization_id=org_b)  # the carried person, in org_b
    assert len(reads) == 5, "a repeat by the same person is the memo; the carried person is someone else"
    await read_table_kind(slug)
    assert len(reads) == 5
    assert calls_people[0][:3] == [(one, org_a), (two, org_a), (one, org_b)]
    # A user without an organization would be read as the carried person: refused, never mis-keyed.
    with pytest.raises(ValueError):
        await read_table_kind(slug, user_id=two)


async def test_no_reader_wired_is_an_outage_never_a_pass(monkeypatch) -> None:
    monkeypatch.delitem(_registry._extras, "table_kind_reader", raising=False)
    _request(monkeypatch, "")
    kinds._warned_slugs.clear()
    entry, reason = await resolve_kind(table_kind_slug(OPEN))
    assert entry is None and reason is KindDegradedReason.CATALOG_UNREACHABLE
