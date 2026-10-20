"""A tool call refused for its arguments is a normal tool result, never a platform error.

PB-08 (2026-10-19, conversation b924e5b7…): the lead's first ``agent`` call left out
``agent_id``. The executor refused it with a model-readable message and the lead
called again correctly 1 s later — and the same refusal was ALSO filed as
system_error e276ec49 (``tool_argument_validation_failed``). A refusal the model
can correct and the loop handles is the model's mistake, not the server's: it is
a tool result plus a WARNING log line. Only a server fault is an error.

This is the ONE place argument-validation refusals are filed
(``ToolExecutor._reject_invalid_arguments``), so the guard drives a real
``ToolExecutor.execute`` with arguments its declared model refuses.

Run: ``uv run pytest packages/matrx-ai/matrx_ai/tools/tests/test_a_model_correctable_refusal_is_never_a_platform_error.py``
"""

from __future__ import annotations

import logging
from typing import Any

import pytest

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.guardrails import GuardrailEngine
from matrx_ai.tools.lifecycle import ToolLifecycleManager
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.tests.test_dispatch_validation import _make_ctx, _NullEmitter


@pytest.fixture
def registry():
    reg = ToolRegistry.get_instance()
    saved = dict(reg._tools)
    yield reg
    reg._tools = saved


@pytest.fixture
def app_ctx():
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    token = set_app_context(AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True))
    yield
    clear_app_context(token)


async def test_an_argument_refusal_files_no_system_error_and_logs_a_warning(
    registry, monkeypatch, app_ctx, caplog
) -> None:
    executor = ToolExecutor(
        registry=registry,
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )
    import matrx_ai.tools._generated_declarations  # noqa: F401 — the declared web args model

    definition = ToolDefinition(
        name="web",
        description="Web dispatcher",
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.implementations.web.web",
    )

    async def must_not_run(*_a: Any, **_kw: Any) -> None:
        raise AssertionError("refused arguments reached the tool body")

    definition._callable = must_not_run
    registry._tools["web"] = definition

    filed: list[dict[str, Any]] = []

    async def capture_spy(*_args: Any, **kwargs: Any) -> None:
        filed.append(kwargs)

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_spy)
    caplog.set_level(logging.DEBUG)

    content, result = await executor.execute(
        "web",
        {"action": "search", "queries": [f"query-{i}" for i in range(8)]},
        _make_ctx(),
    )

    # The model gets its refusal, as a normal tool result it can correct.
    assert result.success is False and result.error is not None
    assert result.error.error_type == "invalid_arguments"
    assert "at most 5 items" in result.error.message
    assert content

    # Nothing is filed on the errors surface for the model's own mistake.
    assert [f.get("kind") for f in filed] == [], (
        "a model-correctable argument refusal was filed as a platform error: "
        f"{[f.get('kind') for f in filed]}"
    )
    # It is logged at WARNING, never ERROR.
    errors = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert errors == [], f"an argument refusal logged at ERROR: {[r.getMessage()[:200] for r in errors]}"
    warnings = [
        r
        for r in caplog.records
        if r.levelno == logging.WARNING and "web" in r.getMessage() and "refused" in r.getMessage()
    ]
    assert warnings, "an argument refusal must leave one WARNING line naming the tool"
    # The warning never carries what the model sent.
    assert "query-7" not in " ".join(r.getMessage() for r in warnings)
