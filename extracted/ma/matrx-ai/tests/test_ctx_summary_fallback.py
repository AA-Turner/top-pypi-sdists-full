"""context mode=summary must never hard-fail.

Resolution order:
  1. AI summary when summary_agent_id is set
  2. source-backed: precomputed descriptor.summary
  3. otherwise the first page with fell_back_from=summary
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from matrx_ai.tools.implementations.ctx import ctx_get
from matrx_ai.tools.models import ToolContext


def _ctx() -> ToolContext:
    return ToolContext(
        call_id="call_test",
        user_id="user_test",
        conversation_id="conv_test",
        emitter=None,
    )


def _manifest(obj: Any) -> MagicMock:
    m = MagicMock()
    m.get.return_value = obj
    m.all.return_value = [obj]
    return m


@pytest.mark.asyncio
async def test_summary_on_lazy_source_returns_descriptor() -> None:
    desc = SimpleNamespace(
        summary="DOC: 12 pages · clean text · sections: Intro, Methods",
        primary_size_chars=48000,
    )
    obj = SimpleNamespace(
        key="attached_document_abc",
        type=SimpleNamespace(value="json"),
        label="Report.pdf",
        summary_agent_id=None,
        descriptor=desc,
        source=SimpleNamespace(kind="processed_document", id="pd-1"),
        is_lazy_source=lambda: True,
        content_as_str=lambda: "",
    )
    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=MagicMock()),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: _manifest(obj)),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        result = await ctx_get({"key": "attached_document_abc", "mode": "summary"}, _ctx())

    assert result.success is True
    assert result.output is not None
    assert result.output.summary_kind == "descriptor"
    assert "12 pages" in result.output.summary
    assert result.output.fell_back_from is None


@pytest.mark.asyncio
async def test_summary_without_agent_falls_back_to_page() -> None:
    content = "A" * 9000
    obj = SimpleNamespace(
        key="notes",
        type=SimpleNamespace(value="text"),
        label="Notes",
        summary_agent_id=None,
        descriptor=None,
        source=None,
        is_lazy_source=lambda: False,
        content_as_str=lambda: content,
    )
    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=MagicMock()),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: _manifest(obj)),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        result = await ctx_get({"key": "notes", "mode": "summary"}, _ctx())

    assert result.success is True
    assert result.output is not None
    assert result.output.fell_back_from == "summary"
    assert result.output.mode == "page"
    assert result.output.content == content[:4000]
    assert result.output.has_more is True


@pytest.mark.asyncio
async def test_summary_with_agent_still_runs_agent() -> None:
    obj = SimpleNamespace(
        key="big_doc",
        type=SimpleNamespace(value="text"),
        label="Big",
        summary_agent_id="agent-summary-1",
        descriptor=None,
        source=None,
        is_lazy_source=lambda: False,
        content_as_str=lambda: "long content here",
    )
    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=MagicMock()),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: _manifest(obj)),
        patch("matrx_ai._ext.has_ext", return_value=False),
        patch(
            "matrx_ai.tools.implementations.ctx._run_summary_agent",
            new_callable=AsyncMock,
            return_value="AI SUMMARY",
        ) as run_agent,
    ):
        result = await ctx_get({"key": "big_doc", "mode": "summary"}, _ctx())

    assert result.success is True
    assert result.output is not None
    assert result.output.summary == "AI SUMMARY"
    assert result.output.summary_kind == "agent"
    run_agent.assert_awaited_once()
