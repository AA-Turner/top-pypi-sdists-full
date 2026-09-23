"""A `relation` cell reaches the model as a NAME, or the seam says so out loud.

``usertable_get_data`` / ``usertable_search_data`` read the older user-data tables, where a
``relation`` column STORES a record's id and MEANS that record's name. Every other server
reader was routed through the one resolver by lane OLD-TABLES-3; these two could not be,
because the resolver lives in matrx-records and matrx-records depends on matrx-ai. So the
host injects it (``matrx_ai.configure(relation_words_resolver=...)``).

Two halves, and the second is the one that matters: an unwired host must get its page back
UNCHANGED **and hear about it**. A silent pass-through is indistinguishable from a working
seam while raw uuids pour into prompts.
"""

from __future__ import annotations

import logging

import pytest

import matrx_ai
from matrx_ai.tools import relation_words as relation_words_seam
from matrx_ai.tools.implementations import datasets_tools
from matrx_ai.tools.models import ToolContext

_TABLE_ID = "11111111-1111-4111-8111-111111111111"
_CUSTOMER_ID = "22222222-2222-4222-8222-222222222222"


class _Ctx(ToolContext):
    @property
    def user_id(self) -> str:
        return "33333333-3333-4333-8333-333333333333"


def _ctx() -> _Ctx:
    return _Ctx(call_id="call-1", tool_name="usertable_get_data")


@pytest.fixture(autouse=True)
def _stub_query(monkeypatch):
    """One stored page: a `relation` cell holding an id, beside an ordinary cell."""

    def _run_query(name: str, params: dict):
        return [
            {
                "id": "44444444-4444-4444-8444-444444444444",
                "data": {"account": _CUSTOMER_ID, "amount": "1200"},
                "created_at": "2026-09-22",
            }
        ]

    monkeypatch.setattr(datasets_tools, "_run_query", _run_query)


@pytest.fixture(autouse=True)
def _fresh_announcements(monkeypatch):
    monkeypatch.setattr(relation_words_seam, "_announced", set())


async def _resolver(table_id, rows, *, user_id):
    assert table_id == _TABLE_ID
    assert user_id == "33333333-3333-4333-8333-333333333333"
    return [
        {**row, "account": "All Green Recycling"} if row.get("account") == _CUSTOMER_ID else row
        for row in rows
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool, args",
    [
        (datasets_tools.usertable_get_data, {"table_id": _TABLE_ID}),
        (
            datasets_tools.usertable_search_data,
            {"table_id": _TABLE_ID, "search_term": "green"},
        ),
    ],
)
async def test_relation_cell_reaches_the_model_as_words(tool, args):
    matrx_ai.configure(relation_words_resolver=_resolver)
    result = await tool(args, _ctx())
    assert result.success, result.error
    assert result.output["rows"][0]["data"]["account"] == "All Green Recycling"
    assert result.output["rows"][0]["data"]["amount"] == "1200"


@pytest.mark.asyncio
async def test_unwired_host_gets_the_page_unchanged_and_is_told(caplog):
    with caplog.at_level(logging.WARNING, logger=relation_words_seam.__name__):
        result = await datasets_tools.usertable_get_data({"table_id": _TABLE_ID}, _ctx())

    assert result.success, result.error
    assert result.output["rows"][0]["data"]["account"] == _CUSTOMER_ID

    announcements = [r.getMessage() for r in caplog.records if r.levelno >= logging.WARNING]
    assert announcements, "the absent resolver passed the page through in SILENCE"
    message = announcements[0]
    assert "relation_words_resolver" in message
    assert "package_integration.py" in message
    assert "REMEDY" in message


@pytest.mark.asyncio
async def test_a_raising_resolver_never_breaks_the_tool_and_is_announced(caplog):
    async def _boom(table_id, rows, *, user_id):
        raise RuntimeError("words door unavailable")

    matrx_ai.configure(relation_words_resolver=_boom)
    with caplog.at_level(logging.WARNING, logger=relation_words_seam.__name__):
        result = await datasets_tools.usertable_get_data({"table_id": _TABLE_ID}, _ctx())

    assert result.success, result.error
    assert result.output["rows"][0]["data"]["account"] == _CUSTOMER_ID
    assert any("REMEDY" in r.getMessage() for r in caplog.records)
