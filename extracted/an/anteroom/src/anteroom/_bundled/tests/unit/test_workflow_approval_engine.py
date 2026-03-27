"""Tests proving the real engine approval path: agent step → callback → pause → resume.

These tests use a mock AI service + mock tool executor to exercise the
actual WorkflowEngine approval callback, pause_signal, and resume path
without needing a real LLM endpoint.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.ai_service import AIService
from anteroom.services.workflow_engine import WorkflowEngine, load_definition, register_gate_condition
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    get_pending_approval,
    list_workflow_steps,
    resolve_approval_request,
)

# Workflow with an agent runner step that will trigger tool approval
AGENT_WORKFLOW = """\
kind: workflow
id: test_agent_approval
version: 0.1.0
inputs: {}
steps:
  - id: write_code
    type: runner
    runner: cli_claude
    prompt: "Write a file"
    timeout: 30
"""


def _make_ai_service() -> AIService:
    service = AIService.__new__(AIService)
    service.config = type(
        "C",
        (),
        {
            "base_url": "http://localhost/v1",
            "api_key": "test",
            "model": "gpt-4",
            "request_timeout": 120,
            "verify_ssl": True,
            "max_output_tokens": 4096,
        },
    )()
    service._token_provider = None
    service.client = AsyncMock()
    return service


def _mock_ai_with_tool_call() -> AIService:
    """AI service that returns a write_file tool call."""
    service = _make_ai_service()
    call_count = 0

    async def fake_stream(messages: Any, **kwargs: Any):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            yield {
                "event": "tool_call",
                "data": {
                    "id": "tc1",
                    "function_name": "write_file",
                    "arguments": {"path": "/src/foo.py", "content": "# new file"},
                },
            }
            yield {"event": "done", "data": {}}
        else:
            yield {"event": "token", "data": {"content": "Done writing file."}}
            yield {"event": "done", "data": {}}

    service.stream_chat = fake_stream
    return service


def _make_approval_triggering_executor():
    """Tool executor that simulates a tool needing approval.

    When called with confirm_callback, it invokes the callback with
    needs_approval=True. If the callback returns False, it returns
    a denied result. If True, it returns success.
    """

    async def executor(name: str, args: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        confirm_callback = kwargs.get("confirm_callback")
        if confirm_callback is not None:
            # Create a mock SafetyVerdict
            verdict = type(
                "SafetyVerdict",
                (),
                {
                    "tool_name": name,
                    "needs_approval": True,
                    "is_hard_blocked": False,
                    "reason": "Write operation requires approval",
                    "details": args,
                    "tier": "WRITE",
                },
            )()
            approved = await confirm_callback(verdict)
            if not approved:
                return {"error": "Operation denied by user", "_approval_decision": "denied"}
        return {"result": f"{name} executed", "_approval_decision": "auto"}

    return executor


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture(autouse=True)
def _register_gates():
    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)
    yield


class TestRealApprovalPath:
    """Prove the engine's actual approval callback fires and pauses correctly."""

    @pytest.mark.asyncio
    async def test_agent_step_pauses_on_approval(self, db: Any) -> None:
        """Agent runner step triggers approval → run enters waiting_for_approval."""
        ai = _mock_ai_with_tool_call()
        executor = _make_approval_triggering_executor()

        engine = WorkflowEngine(
            db,
            WorkflowConfig(),
            create_default_registry(),
            ai_service=ai,
            tool_executor=executor,
            tools_openai=[{"type": "function", "function": {"name": "write_file"}}],
        )

        defn = load_definition(AGENT_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        # The run should be paused for approval, not completed
        assert run["status"] == "waiting_for_approval", (
            f"Expected waiting_for_approval, got {run['status']} (stop_reason: {run.get('stop_reason')})"
        )

        # A pending approval request should exist
        pending = get_pending_approval(db, run["id"])
        assert pending is not None
        assert pending["tool_name"] == "write_file"
        assert pending["risk_tier"] == "WRITE"
        assert pending["status"] == "pending"

    @pytest.mark.asyncio
    async def test_approval_request_id_stored_on_step(self, db: Any) -> None:
        """The approval request ID is stored on the step record."""
        ai = _mock_ai_with_tool_call()
        executor = _make_approval_triggering_executor()

        engine = WorkflowEngine(
            db,
            WorkflowConfig(),
            create_default_registry(),
            ai_service=ai,
            tool_executor=executor,
            tools_openai=[{"type": "function", "function": {"name": "write_file"}}],
        )

        defn = load_definition(AGENT_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t2")

        steps = list_workflow_steps(db, run["id"])
        assert len(steps) >= 1
        # The step that triggered approval should have approval_request_id
        approval_step = next((s for s in steps if s.get("approval_request_id")), None)
        assert approval_step is not None, f"No step has approval_request_id. Steps: {steps}"

    @pytest.mark.asyncio
    async def test_approve_then_resume_completes(self, db: Any) -> None:
        """Approve the request, resume the run → run completes."""
        ai = _mock_ai_with_tool_call()
        executor = _make_approval_triggering_executor()

        engine = WorkflowEngine(
            db,
            WorkflowConfig(),
            create_default_registry(),
            ai_service=ai,
            tool_executor=executor,
            tools_openai=[{"type": "function", "function": {"name": "write_file"}}],
        )

        defn = load_definition(AGENT_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t3")
        assert run["status"] == "waiting_for_approval"

        # Approve the request
        pending = get_pending_approval(db, run["id"])
        resolve_approval_request(db, pending["id"], status="approved", resolved_by="operator")

        # Resume — the pre-approved callback should let the tool through
        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "completed", (
            f"Expected completed, got {result['status']} (stop_reason: {result.get('stop_reason')})"
        )

    @pytest.mark.asyncio
    async def test_deny_then_resume_cancels(self, db: Any) -> None:
        """Deny the request, resume → run is cancelled."""
        ai = _mock_ai_with_tool_call()
        executor = _make_approval_triggering_executor()

        engine = WorkflowEngine(
            db,
            WorkflowConfig(),
            create_default_registry(),
            ai_service=ai,
            tool_executor=executor,
            tools_openai=[{"type": "function", "function": {"name": "write_file"}}],
        )

        defn = load_definition(AGENT_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t4")
        assert run["status"] == "waiting_for_approval"

        pending = get_pending_approval(db, run["id"])
        resolve_approval_request(db, pending["id"], status="denied", resolved_by="operator")

        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "cancelled"
        assert "denied" in (result.get("stop_reason") or "")
