"""Ask AI (``ai.llm.chat``) carries everything Extract with AI did, so the fold loses nothing.

Extract with AI (``ai.extract``) was folded into Ask AI on 2026-10-29. Its guards moved here:

* the model field has NO default — a schema default naming a model is a lie with a shelf
  life (2026-09-10: ``gpt-4o-mini`` was copied into three nodes and every run died);
* an unknown model fails by NAME (``model_unknown``) before any provider call — never as
  "the model returned no output text";
* the node never forces a sampling temperature (Claude 5 models reject the parameter);
* with an ``output_schema`` the request carries a strict ``json_schema`` response_format
  and the parsed answer arrives in ``structured_output`` (the raw reply in ``final_text``),
  which is where a converted Extract step's downstream reads now point.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from pydantic import ValidationError

from matrx_ai.graph_nodes.llm_action import LlmChatInput, llm_chat


def test_llm_chat_input_has_no_model_default():
    with pytest.raises(ValidationError):
        LlmChatInput(prompt="hello")
    assert "default" not in LlmChatInput.model_json_schema()["properties"]["model"]


class _NoSuchModelCatalog:
    async def list_models(self):
        return []

    async def get_model(self, id_or_name: str):
        return None


def test_unknown_model_is_a_named_failure(monkeypatch: pytest.MonkeyPatch):
    import matrx_ai.catalog.host_catalog as host_catalog
    import matrx_ai.orchestrator.executor as executor

    monkeypatch.setattr(host_catalog, "get_model_catalog", lambda: _NoSuchModelCatalog())
    called = {"executor": False}

    async def _never(*_a, **_k):  # the provider must not be called at all
        called["executor"] = True
        raise AssertionError("execute_ai_request must not run for an unknown model")

    monkeypatch.setattr(executor, "execute_ai_request", _never)

    result = asyncio.run(llm_chat(None, LlmChatInput(model="gpt-4o-mini", prompt="x" * 10)))
    assert result.status == "error"
    assert result.error.code == "model_unknown"
    assert "gpt-4o-mini" in result.error.message
    assert called["executor"] is False


def _capture_config(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    import matrx_ai.catalog.host_catalog as host_catalog
    import matrx_ai.graph_nodes.llm_action as llm_action
    import matrx_ai.orchestrator.executor as executor

    monkeypatch.setattr(host_catalog, "get_model_catalog", lambda: None)

    class _Held:
        def __init__(self, config: dict[str, Any]) -> None:
            self.config = config
            self.metadata: dict[str, Any] = {}

    async def _hold(config, **_k):
        return _Held(dict(config))

    async def _no_skills(*_a, **_k):
        return None

    monkeypatch.setattr(llm_action, "hold_step", _hold)
    monkeypatch.setattr(llm_action, "assemble_held_step_skills", _no_skills)
    seen: dict[str, Any] = {}

    async def _capture(config, **_k):
        seen["temperature"] = getattr(config, "temperature", None)
        seen["response_format"] = getattr(config, "response_format", None)
        seen["system_instruction"] = getattr(config, "system_instruction", None)
        raise RuntimeError("stop here — the config is what this test inspects")

    monkeypatch.setattr(executor, "execute_ai_request", _capture)
    return seen


def test_llm_chat_never_forces_temperature(monkeypatch: pytest.MonkeyPatch):
    seen = _capture_config(monkeypatch)
    with pytest.raises(RuntimeError):
        asyncio.run(llm_chat(None, LlmChatInput(model="claude-opus-5", prompt="x" * 10)))
    assert seen["temperature"] is None


def test_extraction_shape_sends_strict_schema_and_instruction(monkeypatch: pytest.MonkeyPatch):
    """The converted Extract step: text -> prompt, instruction -> system_instruction,
    schema_definition -> output_schema. The schema is enforced natively and strictly."""
    seen = _capture_config(monkeypatch)
    schema = {
        "type": "object",
        "properties": {"total": {"type": "number"}},
        "required": ["total"],
    }
    with pytest.raises(RuntimeError):
        asyncio.run(
            llm_chat(
                None,
                LlmChatInput(
                    model="claude-opus-5",
                    prompt="the total is $5",
                    system_instruction="Extract the total.",
                    output_schema=schema,
                ),
            )
        )
    rf = seen["response_format"]
    assert rf["type"] == "json_schema"
    assert rf["json_schema"]["strict"] is True
    assert rf["json_schema"]["schema"]["properties"] == schema["properties"]
    assert "Extract the total." in str(seen["system_instruction"])
