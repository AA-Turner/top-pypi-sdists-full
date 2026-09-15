"""Forcing-function: the AI's ANSWER is recorded in full (KI-049, 2026-09-14).

Run history — the run console tab where a person clicks through every AI call a
run made and reads what it generated — reads the answer out of
``chat.request_snapshot.response_payload``. The snapshot writer ran every string
in that payload through ``LargeBinaryStringRedactor`` (64 KiB), a guard built to
stop multi-MB base64 files. A keyword-classifier structured answer is ~73 KB of
JSON, so live, 78 of 415 recorded outputs in 30 days were stored as 128
characters + a marker + 128 characters: the calls that matter most showed a
fragment, and the rest of what the model said was gone for good.

Decision: assistant ``type="text"`` blocks in the response are exempt. Base64 /
data-URL strings are still redacted — everywhere else, AND inside assistant
content (an image block's ``base64_data``, or a "text" that is itself a blob).

These tests drive the REAL writer (``_write_request_snapshot``) and read what it
queues for persistence; they fail on the pre-fix pipeline.
"""

from __future__ import annotations

import base64
import json
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.orchestrator import executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.providers import snapshot_redactors as redactors_mod
from matrx_ai.providers.snapshot_redactors import MARKER_OPEN


def _classifier_answer(target_bytes: int = 73_000) -> str:
    """A keyword-classifier structured answer the size of the live ones (~73 KB),
    carrying its ``__kind`` marker the way a structured output does."""
    rows: list[dict[str, Any]] = []
    i = 0
    while True:
        rows.append(
            {
                "keyword": f"electronics recycling near me {i}",
                "intent": "transactional",
                "topic": "IT asset disposition",
                "value_tier": "money",
                "reason": (
                    "Searcher wants a local provider to take retired laptops and "
                    "servers; matches the ITAD service page, not the blog."
                ),
            }
        )
        i += 1
        text = json.dumps({"__kind": "seo_keyword_classification", "rows": rows}, ensure_ascii=False)
        if len(text.encode("utf-8")) >= target_bytes:
            return text


class _FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload
        self.metadata: dict[str, Any] = {}

    def to_dict(self) -> dict[str, Any]:
        return self._payload


async def _queued_response_payload(monkeypatch, response: dict[str, Any]) -> dict[str, Any]:
    queued: list[dict[str, Any]] = []
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.get_coordinator", lambda: object())
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )
    exec_ctx = SimpleNamespace(store=True, conversation_id=str(uuid4()), request_id=str(uuid4()))
    await executor_mod._write_request_snapshot(
        exec_ctx=exec_ctx,
        iteration=1,
        api_response=_FakeResponse(response),  # type: ignore[arg-type]
        request_payload={"messages": []},
        unified_payload=None,
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        provider="google",
        model="gemini-3.8-flash",
    )
    assert len(queued) == 1, "the writer queued nothing — the test is not exercising it"
    return queued[0]["response_payload"]


@pytest.mark.asyncio
async def test_a_73kb_structured_answer_is_stored_in_full(monkeypatch) -> None:
    answer = _classifier_answer()
    assert len(answer.encode("utf-8")) > 65_536, "the fixture must exceed the blob redactor's limit"

    stored = await _queued_response_payload(
        monkeypatch,
        {
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {"type": "thinking", "text": "", "signature": "EmcKZQER"},
                        {"type": "text", "text": answer, "id": ""},
                    ],
                }
            ],
            "finish_reason": "stop",
        },
    )

    kept = stored["messages"][0]["content"][1]["text"]
    assert MARKER_OPEN not in kept, (
        "the assistant's answer was shortened by the snapshot redactor — Run history "
        "will show a 595-character fragment of a 73 KB answer"
    )
    assert kept == answer
    assert json.loads(kept)["__kind"] == "seo_keyword_classification", "the __kind marker must survive"


@pytest.mark.asyncio
async def test_base64_inside_assistant_content_is_still_redacted(monkeypatch) -> None:
    blob = base64.b64encode(b"\x89PNG" + b"\x00" * 200_000).decode("ascii")

    stored = await _queued_response_payload(
        monkeypatch,
        {
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {"type": "image", "base64_data": blob, "mime_type": "image/png"},
                        {"type": "text", "text": blob},
                        {"type": "text", "text": f"data:image/png;base64,{blob}"},
                    ],
                }
            ],
        },
    )

    blocks = stored["messages"][0]["content"]
    assert MARKER_OPEN in blocks[0]["base64_data"], "an image blob in assistant content escaped redaction"
    assert MARKER_OPEN in blocks[1]["text"], "a bare base64 'text' escaped redaction"
    assert MARKER_OPEN in blocks[2]["text"], "a data-URL 'text' escaped redaction"


@pytest.mark.asyncio
async def test_large_strings_outside_assistant_text_are_still_redacted(monkeypatch) -> None:
    big = "x " * 40_000  # not base64, but not an assistant text block either
    stored = await _queued_response_payload(
        monkeypatch,
        {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": big}]},
                {"role": "assistant", "content": [{"type": "tool_call", "arguments": {"q": big}}]},
            ],
            "raw_response": {"candidates": [{"blob": big}]},
        },
    )
    assert MARKER_OPEN in stored["messages"][0]["content"][0]["text"]
    assert MARKER_OPEN in stored["messages"][1]["content"][0]["arguments"]["q"]
    assert MARKER_OPEN in stored["raw_response"]["candidates"][0]["blob"]


@pytest.mark.asyncio
async def test_an_answer_over_the_knob_is_kept_and_announced(monkeypatch, caplog) -> None:
    monkeypatch.setattr(redactors_mod, "_knob_reader", lambda key: 70_000)
    answer = _classifier_answer(80_000)
    with caplog.at_level("WARNING"):
        stored = await _queued_response_payload(
            monkeypatch,
            {"messages": [{"role": "assistant", "content": [{"type": "text", "text": answer}]}]},
        )
    assert stored["messages"][0]["content"][0]["text"] == answer, "over the ceiling must still store in full"
    assert any("assistant_text_announce_bytes" in r.getMessage() for r in caplog.records), (
        "an answer over the ceiling was stored without announcing itself"
    )
