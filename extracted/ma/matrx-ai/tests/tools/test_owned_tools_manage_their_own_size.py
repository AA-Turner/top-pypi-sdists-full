"""Owned tools (skill, workflow_run, workflow_catalog, knowledge_search, knowledge_open, records)
bound their own result through ONE helper, so the size gate's 'unmanaged' alarm stops firing.

Red before: ``bound_owned_output`` / ``self_bounded_result`` did not exist and the five entry
points returned an oversized dict untouched (the gate cut it blunt and filed
``tool_result_size_unmanaged``).
"""

import asyncio
import json

from matrx_ai.tools.models import ToolResult
from matrx_ai.tools.output_caps import (
    TOOL_RESULT_SOFT_CAP_CHARS,
    bound_owned_output,
    self_bounded_result,
)


def _page(n: int) -> dict:
    return {"rows": [{"id": f"r{i}", "body": "x" * 2000} for i in range(n)]}


def test_a_big_dict_is_cut_whole_rows_and_announced():
    body, bounded = bound_owned_output(_page(200))
    assert bounded is True
    assert len(json.dumps(body, ensure_ascii=False)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert body["truncated"] is True and body["more_available"] is True
    assert "not shown" in body["size_note"]
    assert 0 < len(body["rows"]) < 200


def test_a_small_dict_is_untouched():
    page = _page(3)
    body, bounded = bound_owned_output(page)
    assert bounded is False and body is page


def test_the_decorator_declares_self_capped_only_when_it_cut():
    @self_bounded_result
    async def big(args, ctx):
        return ToolResult(success=True, output=_page(200), tool_name="t", call_id="c")

    @self_bounded_result
    async def small(args, ctx):
        return ToolResult(success=True, output=_page(2), tool_name="t", call_id="c")

    r = asyncio.run(big({}, None))
    assert r.output_self_capped is True and len(r.output["rows"]) < 200
    s = asyncio.run(small({}, None))
    assert s.output_self_capped is False and "truncated" not in s.output
