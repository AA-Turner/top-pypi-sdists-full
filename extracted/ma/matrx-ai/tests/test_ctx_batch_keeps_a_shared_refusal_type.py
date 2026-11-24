"""A ctx_batch whose every sub-failure is one refusal type keeps that type at the executor boundary.

Live 2026-11-10: two "[validation] key is required." sub-requests became ``batch_all_failed`` and the
tool executor filed a system_error for the model's own omission. SUT: the real ``ctx_batch`` (only
validation paths, no database) and the executor's real ``_is_expected_domain_failure``."""

from __future__ import annotations

import importlib

import pytest

from matrx_ai.tools.executor import _is_expected_domain_failure
from matrx_ai.tools.models import ToolContext

ctx_module = importlib.import_module("matrx_ai.tools.implementations.ctx")


@pytest.mark.asyncio
async def test_all_validation_sub_failures_stay_a_validation_refusal() -> None:
    result = await ctx_module.ctx_batch({"requests": ["not-an-object", 7]}, ToolContext(call_id="call-1"))
    assert result.success is False and result.error is not None
    assert result.error.error_type == "validation"
    assert _is_expected_domain_failure(tool_name="context", error_type=result.error.error_type, message=result.error.message)


@pytest.mark.asyncio
async def test_mixed_sub_failures_stay_a_batch_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.tools.models import ToolError, ToolResult

    async def broken_get(args, _ctx, budget=None):
        return ToolResult(success=False, error=ToolError(error_type="database", message="boom"))

    monkeypatch.setattr(ctx_module, "ctx_get", broken_get)
    result = await ctx_module.ctx_batch({"requests": ["not-an-object", {"key": "k"}]}, ToolContext(call_id="call-1"))
    assert result.success is False and result.error is not None
    assert result.error.error_type == "batch_all_failed"
