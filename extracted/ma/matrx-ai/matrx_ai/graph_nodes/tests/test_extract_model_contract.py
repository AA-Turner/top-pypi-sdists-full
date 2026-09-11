"""Guard for the 2026-09-10 class: ``ai.extract`` never advertises a dead
default model, and an unknown model fails by NAME — never as "the model
returned no output text".

Before the fix the schema default was ``"gpt-4o-mini"`` (absent from the live
catalog); the Masterwork Conductor copied it into three nodes and every run
died at step one with zero tokens and an empty answer.
"""

from __future__ import annotations

import asyncio

import pytest
from pydantic import ValidationError

from matrx_ai.graph_nodes import extract_action
from matrx_ai.graph_nodes.extract_action import ExtractInput, ai_extract


def test_extract_input_has_no_model_default():
    with pytest.raises(ValidationError):
        ExtractInput(text="hello", instruction="extract the greeting")
    assert "default" not in ExtractInput.model_json_schema()["properties"]["model"]


class _NoSuchModelCatalog:
    async def list_models(self):
        return []

    async def get_model(self, id_or_name: str):
        return None


def test_unknown_model_is_a_named_failure(monkeypatch: pytest.MonkeyPatch):
    import matrx_ai.catalog.host_catalog as host_catalog

    monkeypatch.setattr(host_catalog, "get_model_catalog", lambda: _NoSuchModelCatalog())

    called = {"executor": False}

    async def _never(*_a, **_k):  # the provider must not be called at all
        called["executor"] = True
        raise AssertionError("execute_ai_request must not run for an unknown model")

    import matrx_ai.orchestrator.executor as executor

    monkeypatch.setattr(executor, "execute_ai_request", _never)

    result = asyncio.run(
        ai_extract(
            None,  # the node never touches ctx before the pre-flight
            ExtractInput(model="gpt-4o-mini", text="x" * 10, instruction="extract"),
        )
    )
    assert result.status == "error"
    assert result.error.code == "model_unknown"
    assert "gpt-4o-mini" in result.error.message
    assert called["executor"] is False
    assert extract_action is not None


def test_extract_never_forces_temperature(monkeypatch: pytest.MonkeyPatch):
    """Claude 5 models reject `temperature`; the node must not send one."""
    import matrx_ai.catalog.host_catalog as host_catalog
    import matrx_ai.orchestrator.executor as executor

    monkeypatch.setattr(host_catalog, "get_model_catalog", lambda: None)
    seen: dict[str, object] = {}

    async def _capture(config, **_k):
        seen["temperature"] = getattr(config, "temperature", None)
        raise RuntimeError("stop here — the config is what this test inspects")

    monkeypatch.setattr(executor, "execute_ai_request", _capture)
    with pytest.raises(RuntimeError):
        asyncio.run(
            ai_extract(
                None, ExtractInput(model="claude-opus-5", text="x" * 10, instruction="extract")
            )
        )
    assert seen["temperature"] is None
