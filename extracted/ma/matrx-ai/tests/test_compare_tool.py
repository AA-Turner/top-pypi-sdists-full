"""``compare``: the agent's call reaches only the host's plan/status doors — it has no way to start a run."""

from __future__ import annotations

import pytest
from matrx_scraper import _ext

from matrx_ai.tools.arg_models.web_args import CompareArgs
from matrx_ai.tools.implementations import compare as tool
from matrx_ai.tools.models import ToolContext


@pytest.fixture(autouse=True)
def _ext_state():
    saved = dict(_ext._registry)
    yield
    _ext._registry.clear()
    _ext._registry.update(saved)


def _ctx() -> ToolContext:
    return ToolContext(call_id="call-9", tool_name="compare")


def test_args_have_no_way_to_confirm():
    assert set(CompareArgs.model_fields) == {"items", "concept", "kind", "city", "run_id"}


@pytest.mark.asyncio
async def test_plan_door_gets_items_and_call_id():
    seen = []

    async def plan(items, kind, city, call_id, concept=None):
        seen.append((items, kind, city, call_id, concept))
        return {"status": "awaiting_confirmation"}

    _ext.configure_ext(**{tool.EXT_PLAN: plan})
    res = await tool.compare({"items": ["a", "b"], "city": "Austin"}, _ctx())
    assert res.success and res.output["status"] == "awaiting_confirmation"
    assert seen == [(["a", "b"], "auto", "Austin", "call-9", None)]
    res = await tool.compare({"concept": "best bike shops in Bend, OR"}, _ctx())
    assert res.success and seen[-1] == ([], "auto", None, "call-9", "best bike shops in Bend, OR")


@pytest.mark.asyncio
async def test_run_id_reads_status_and_never_plans():
    async def plan(*a):
        raise AssertionError("must not plan")

    async def status(run_id):
        return {"status": "running", "run": run_id}

    _ext.configure_ext(**{tool.EXT_PLAN: plan, tool.EXT_STATUS: status})
    res = await tool.compare({"run_id": "r1"}, _ctx())
    assert res.output == {"status": "running", "run": "r1"}


@pytest.mark.asyncio
async def test_one_item_is_refused_and_unwired_server_says_so():
    _ext.configure_ext(**{tool.EXT_PLAN: lambda *a: None})
    res = await tool.compare({"items": ["only"]}, _ctx())
    assert not res.success
    _ext._registry.pop(tool.EXT_PLAN)
    res = await tool.compare({"items": ["a", "b"]}, _ctx())
    assert not res.success and "not set up" in res.error.message


@pytest.mark.asyncio
async def test_items_may_carry_name_and_city_apart():
    seen = []

    async def plan(items, kind, city, call_id, concept=None):
        seen.append(items)
        return {"status": "awaiting_confirmation"}

    _ext.configure_ext(**{tool.EXT_PLAN: plan})
    res = await tool.compare({"items": [{"name": "Pop-A-Lock", "city": "Ithaca NY"}, "https://x.com"]}, _ctx())
    assert res.success and seen == [[{"name": "Pop-A-Lock", "city": "Ithaca NY"}, "https://x.com"]]
