"""A JSON STRING where the schema publishes an object/array is READ — never emptied, never replaced.

Live 2026-11-06 (review 12 C1, conversation ca7de323, 3 of 3 ask_person calls): the model sent
``payload`` as a JSON string that dropped its final ``}``. Nothing decoded it before the tool's own
input repair, which read it as empty and made the call's lead-in the only "question" — the real
questions were thrown away and the person saw one empty box. Two layers now hold:

1. the executor decodes a top-level string by the PUBLISHED schema before anything else sees the call
   (``decode_stringified_by_schema``), so a tool-side repair never meets the string at all;
2. both decoders read through the one funnel (``parse_json_document``): strict, then a faithful repair
   of near-miss syntax; text cut off inside a string, or not a document at all, is refused as sent.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from matrx_ai.agents.response_parser import parse_json_document
from matrx_ai.tools._dispatch_util import (
    coerce_stringified_containers,
    decode_stringified_by_schema,
)

#: The live payload string (call toolu_01Y3LRoyErseVRxWWGqWqMRJ), final ``}`` missing as sent.
LIVE_PAYLOAD = (
    '{"questions": [{"id": "understanding.industry", "type": "choice", "header": "Service style", '
    '"options": ["Drop-off only", "Drop-off plus setup", "Full service with staff", "Mix"], '
    '"question": "How does Pinecrest serve most office lunches?"}, '
    '{"id": "understanding.biggest_bottleneck", "type": "choice", "header": "Main constraint", '
    '"options": ["Not enough orders", "Kitchen capacity", "Staff hours"], '
    '"question": "What limits Pinecrest\'s growth most?"}, '
    '{"id": "food_cost", "type": "text", "header": "Cost per head", '
    '"question": "What does a typical lunch cost you in food, and what do you charge now?"}]'
)
PARAMETERS = {
    "kind": {"type": "string"},
    "message": {"type": "string"},
    "payload": {"type": "object", "additionalProperties": True},
    "tags": {"type": "array"},
    "either": {"anyOf": [{"type": "object"}, {"type": "string"}]},
}


def test_the_live_payload_reads_whole_with_every_question() -> None:
    read = parse_json_document(LIVE_PAYLOAD)
    assert isinstance(read, dict)
    assert [q["id"] for q in read["questions"]] == [
        "understanding.industry", "understanding.biggest_bottleneck", "food_cost"]


@pytest.mark.parametrize("text", [
    "Got it: walk-in plus a Saturday market. Now the two things that shape my advice most.",
    '{"questions": [{"question": "How does Pinecrest ser',  # cut off inside a string: a lost tail
    "{{{{ unbalanced",
    "",
])
def test_text_that_is_not_one_readable_document_is_never_guessed(text: str) -> None:
    assert parse_json_document(text) is None


def test_the_executor_layer_decodes_by_the_published_schema() -> None:
    arguments = {"kind": "questions", "message": "Lead-in.", "payload": LIVE_PAYLOAD, "tags": '["a", "b"]'}
    decoded = decode_stringified_by_schema(arguments, PARAMETERS)
    assert decoded is not None
    fixed, fields = decoded
    assert fields == ["payload", "tags"]
    assert len(fixed["payload"]["questions"]) == 3
    assert fixed["tags"] == ["a", "b"]
    assert fixed["message"] == "Lead-in."  # no other field is touched


def test_a_string_the_schema_allows_or_that_does_not_read_is_left_as_sent() -> None:
    arguments: dict[str, Any] = {"message": '{"looks": "like json"}', "either": '{"a": 1}',
                                 "payload": "Got it. Two questions."}
    assert decode_stringified_by_schema(arguments, PARAMETERS) is None
    assert decode_stringified_by_schema(arguments, {"properties": PARAMETERS}) is None


def test_the_validation_layer_reads_the_same_near_miss() -> None:
    class Args(BaseModel):
        payload: dict[str, Any]

    with pytest.raises(ValidationError) as exc:
        Args.model_validate({"payload": LIVE_PAYLOAD})
    recovered = coerce_stringified_containers({"payload": LIVE_PAYLOAD}, exc.value)
    assert recovered is not None
    assert len(recovered[0]["payload"]["questions"]) == 3


# ── layer 1, driven through a real ToolExecutor.execute ──────────────────────────────────────────

@pytest.fixture
def registry():
    from matrx_ai.tools.registry import ToolRegistry

    reg = ToolRegistry.get_instance()
    saved = dict(reg._tools)
    yield reg
    reg._tools = saved


@pytest.fixture
def app_ctx():
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    from matrx_ai.tools.tests.test_dispatch_validation import _NullEmitter

    token = set_app_context(AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True))
    yield
    clear_app_context(token)


async def test_the_tool_receives_the_object_and_no_drift_is_filed(registry, monkeypatch, app_ctx) -> None:
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.guardrails import GuardrailEngine
    from matrx_ai.tools.lifecycle import ToolLifecycleManager
    from matrx_ai.tools.logger import ToolExecutionLogger
    from matrx_ai.tools.models import ToolDefinition, ToolResult, ToolType
    from matrx_ai.tools.tests.test_dispatch_validation import _make_ctx

    received: list[Any] = []

    async def body(args: dict[str, Any], _ctx: Any) -> ToolResult:
        received.append(args["payload"])
        return ToolResult(success=True, output={"ok": True})

    definition = ToolDefinition(
        name="payload_probe",
        description="A tool whose payload is an object",
        parameters={"message": {"type": "string", "required": True},
                    "payload": {"type": "object", "additionalProperties": True}},
        tool_type=ToolType.LOCAL,
        function_path="matrx_ai.tools.tests.payload_probe",
    )
    definition._callable = body
    registry._tools["payload_probe"] = definition
    filed: list[str] = []

    async def capture_spy(*_args: Any, **kwargs: Any) -> None:
        filed.append(str(kwargs.get("kind")))

    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", capture_spy)
    executor = ToolExecutor(registry=registry, guardrails=GuardrailEngine(),
                            execution_logger=ToolExecutionLogger(), lifecycle=ToolLifecycleManager.get_instance())
    _content, result = await executor.execute(
        "payload_probe", {"message": "Lead-in.", "payload": LIVE_PAYLOAD}, _make_ctx())

    assert result.success is True, result.error
    assert isinstance(received[0], dict) and len(received[0]["questions"]) == 3
    assert "tool_input_contract_drift" not in filed, filed
