"""Tests for the orchestrator-level structured_output emission.

These exercise ``_emit_structured_output_if_schema`` directly against a
captured emitter, so they need neither a live LLM nor a DB. The hook lives in
``_finalize_and_persist`` (the single chokepoint every exit path passes
through), but the helper is testable in isolation by passing a fake
``CompletedRequest``-shaped object.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from matrx_ai.orchestrator.executor import _emit_structured_output_if_schema

WC_MEDICAL_SCHEMA_INNER = {
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["date"],
                "properties": {"date": {"type": "string"}},
            },
        }
    },
}

WC_MEDICAL_RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "combined_sdt_index",
        "schema": WC_MEDICAL_SCHEMA_INNER,
        "strict": True,
    },
}

FINAL_TEXT_WITH_BARE_ARRAY = """Sure, here's the data:

```json
[{"date": "11/16/2023", "note": "ultrasound"}]
```
"""

FINAL_TEXT_UNPARSEABLE = "I cannot find any qualifying entries — nothing structured to return."


# ---------------------------------------------------------------------------
# Minimal stand-ins for the orchestrator structures the hook reads
# ---------------------------------------------------------------------------


@dataclass
class _FakeConfig:
    response_format: dict[str, Any] | None
    _last_output: str = ""

    def get_last_output(self) -> str:
        return self._last_output


@dataclass
class _FakeRequest:
    config: _FakeConfig


@dataclass
class _FakeCompleted:
    request: _FakeRequest


class _CapturingEmitter:
    def __init__(self) -> None:
        self.captured: list[Any] = []

    async def send_structured_output(self, payload: Any) -> None:
        self.captured.append(payload)


class _AppCtx:
    def __init__(
        self, emitter: _CapturingEmitter, operation_id: str = "", agent_id: str | None = None
    ) -> None:
        self.emitter = emitter
        self.operation_id = operation_id
        self.agent_id = agent_id
        self.metadata: dict[str, Any] = {}


@pytest.fixture
def emitter_ctx(monkeypatch: pytest.MonkeyPatch) -> _CapturingEmitter:
    emitter = _CapturingEmitter()
    ctx = _AppCtx(emitter, operation_id="op-abc", agent_id="agent-1")

    import matrx_connect

    monkeypatch.setattr(matrx_connect, "try_get_app_context", lambda: ctx)
    return emitter


def _make_completed(response_format: dict[str, Any] | None, final_text: str) -> _FakeCompleted:
    return _FakeCompleted(
        request=_FakeRequest(
            config=_FakeConfig(response_format=response_format, _last_output=final_text),
        )
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_emits_with_normalized_data_on_success(emitter_ctx: _CapturingEmitter) -> None:
    completed = _make_completed(WC_MEDICAL_RESPONSE_FORMAT, FINAL_TEXT_WITH_BARE_ARRAY)
    await _emit_structured_output_if_schema(completed)  # type: ignore[arg-type]

    assert len(emitter_ctx.captured) == 1
    p = emitter_ctx.captured[0]
    assert p.success is True
    assert p.schema_name == "combined_sdt_index"
    assert p.json_schema == WC_MEDICAL_SCHEMA_INNER
    # Bare array auto-wrapped into {items: [...]} per schema
    assert isinstance(p.data, dict)
    assert "items" in p.data
    assert p.data["items"][0]["date"] == "11/16/2023"
    assert p.operation_id == "op-abc"
    assert p.match_count >= 1


@pytest.mark.asyncio
async def test_emits_failure_when_response_has_no_json(emitter_ctx: _CapturingEmitter) -> None:
    completed = _make_completed(WC_MEDICAL_RESPONSE_FORMAT, FINAL_TEXT_UNPARSEABLE)
    await _emit_structured_output_if_schema(completed)  # type: ignore[arg-type]

    assert len(emitter_ctx.captured) == 1
    p = emitter_ctx.captured[0]
    assert p.success is False
    assert p.data is None
    assert p.reason != ""
    assert p.match_count == 0


@pytest.mark.asyncio
async def test_kind_verdict_is_stamped_only_for_bound_agent_contract(
    emitter_ctx: _CapturingEmitter,
) -> None:
    completed = _make_completed(WC_MEDICAL_RESPONSE_FORMAT, FINAL_TEXT_WITH_BARE_ARRAY)
    await _emit_structured_output_if_schema(completed)  # type: ignore[arg-type]
    assert emitter_ctx.captured[-1].kind is None
    assert emitter_ctx.captured[-1].kind_checked is False

    import matrx_connect

    ctx = matrx_connect.try_get_app_context()
    ctx.metadata["structured_output_content_ir"] = {
        "kind": "agent_io_agent_1_abcd1234_output",
        "version": 3,
    }
    await _emit_structured_output_if_schema(completed)  # type: ignore[arg-type]
    payload = emitter_ctx.captured[-1]
    assert payload.kind == "agent_io_agent_1_abcd1234_output"
    assert payload.kind_version == 3
    assert payload.kind_checked is True
    assert payload.kind_errors == []


@pytest.mark.asyncio
async def test_no_emission_without_response_format(emitter_ctx: _CapturingEmitter) -> None:
    completed = _make_completed(None, FINAL_TEXT_WITH_BARE_ARRAY)
    await _emit_structured_output_if_schema(completed)  # type: ignore[arg-type]
    assert emitter_ctx.captured == []


@pytest.mark.asyncio
async def test_no_emission_for_json_object_response_format(emitter_ctx: _CapturingEmitter) -> None:
    """``json_object`` is a contract about *type*, not a schema, so it doesn't
    fire STRUCTURED_OUTPUT — that event is for schema-bearing contracts only.
    """
    completed = _make_completed({"type": "json_object"}, FINAL_TEXT_WITH_BARE_ARRAY)
    await _emit_structured_output_if_schema(completed)  # type: ignore[arg-type]
    assert emitter_ctx.captured == []


@pytest.mark.asyncio
async def test_no_emission_when_emitter_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_connect

    monkeypatch.setattr(matrx_connect, "try_get_app_context", lambda: None)

    completed = _make_completed(WC_MEDICAL_RESPONSE_FORMAT, FINAL_TEXT_WITH_BARE_ARRAY)
    # Must silently no-op — never raise
    await _emit_structured_output_if_schema(completed)  # type: ignore[arg-type]
