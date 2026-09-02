"""ModelCatalog seam: routing/resolution from an injected catalog, with the
runtime-model registry round-tripping through unified_client's generic-openai
dispatch — no DB anywhere."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


class _StaticCatalog:
    def __init__(self, models: list[dict]) -> None:
        self._models = models

    async def list_models(self) -> list[dict]:
        return self._models

    async def get_model(self, id_or_name: str) -> dict | None:
        for model in self._models:
            if id_or_name in (str(model.get("id")), model.get("name")):
                return model
        return None


_MOCK_MODEL = {
    "id": "11111111-1111-1111-1111-111111111111",
    "name": "mock-model",
    "api_class": "mock_standard",
    "wire_format": "mock_chat",
    "provider": "mock",
    "pricing": [{"input": 0, "output": 0}],
    "capabilities": {
        "input": ["text"],
        "output": ["text"],
        "features": ["function_calling"],
    },
}


@pytest.mark.asyncio
async def test_resolve_call_profile_from_injected_catalog():
    configure_ext(model_catalog=_StaticCatalog([_MOCK_MODEL]))

    from matrx_ai.catalog.resolve import resolve_call_profile

    profile = await resolve_call_profile("mock-model")
    assert profile.wire_format == "mock_chat"
    assert profile.client_attr == "mock_chat"
    assert profile.provider_model_id == "mock-model"
    assert profile.capabilities.supports_function_calling is True
    assert profile.offering_id == "catalog:mock-model"

    # id lookup resolves the same model
    by_id = await resolve_call_profile(_MOCK_MODEL["id"])
    assert by_id.model_name == "mock-model"


@pytest.mark.asyncio
async def test_manager_lists_catalog_plus_runtime_models():
    configure_ext(model_catalog=_StaticCatalog([_MOCK_MODEL]))
    from matrx_ai.catalog import register_runtime_model, unregister_runtime_model
    from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

    register_runtime_model(
        {
            "id": "local/test-llm",
            "name": "local/test-llm",
            "api_class": "generic_openai_standard",
            "display_name": "test-llm (Local)",
            "provider": "local",
            "is_active": True,
            "endpoints": ["generic_openai_chat"],
        }
    )
    names = [m.name for m in await ai_model_manager_instance.load_all_models()]
    assert names == ["mock-model", "local/test-llm"]

    assert unregister_runtime_model("local/test-llm") is True
    names = [m.name for m in await ai_model_manager_instance.load_all_models()]
    assert names == ["mock-model"]


@pytest.mark.asyncio
async def test_runtime_model_routes_through_generic_openai_dispatch():
    """register_runtime_model → resolve → UnifiedAIClient.execute dispatches to
    the registered GenericOpenAI instance (the matrx-local local-LLM path)."""
    configure_ext(model_catalog=_StaticCatalog([_MOCK_MODEL]))

    from matrx_ai.catalog import register_runtime_model
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import (
        UnifiedAIClient,
        register_generic_openai_instance,
        unregister_generic_openai_instance,
    )

    register_runtime_model(
        {
            "id": "local/test-llm",
            "name": "local/test-llm",
            "api_class": "generic_openai_standard",
            "display_name": "test-llm (Local)",
            "provider": "local",
            "is_active": True,
            "endpoints": ["generic_openai_chat"],
        }
    )

    calls: list[tuple[str, str]] = []

    class _FakeLocalInstance:
        async def execute(self, config, profile, debug=False):
            calls.append((config.model, profile.wire_format))
            return {"ok": True}

    register_generic_openai_instance("local/test-llm", _FakeLocalInstance())
    try:
        config = UnifiedConfig(
            model="local/test-llm",
            messages=MessageList(
                _messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]
            ),
        )
        request = AIMatrixRequest(conversation_id="conv-x", config=config)
        result = await UnifiedAIClient().execute(request)
    finally:
        unregister_generic_openai_instance("local/test-llm")

    assert result == {"ok": True}
    assert calls == [("local/test-llm", "generic_openai_chat")]


@pytest.mark.asyncio
async def test_unroutable_catalog_model_raises_loudly():
    configure_ext(
        model_catalog=_StaticCatalog(
            [{"id": "x", "name": "mystery-model", "api_class": "someday_standard"}]
        )
    )
    from matrx_ai.catalog.resolve import resolve_call_profile

    with pytest.raises(ValueError, match="no routable wire format"):
        await resolve_call_profile("mystery-model")


def test_catalog_resolution_in_clean_subprocess():
    """The whole catalog path resolves with ZERO DB config in a scrubbed
    subprocess — no DBNotConfiguredError anywhere."""
    code = """
import asyncio
import matrx_ai

class Catalog:
    async def list_models(self):
        return [MODEL]
    async def get_model(self, id_or_name):
        return MODEL if id_or_name in (MODEL["id"], MODEL["name"]) else None

MODEL = {
    "id": "11111111-1111-1111-1111-111111111111",
    "name": "mock-model",
    "api_class": "mock_standard",
    "wire_format": "mock_chat",
    "provider": "mock",
    "capabilities": {"input": ["text"], "output": ["text"], "features": []},
}

matrx_ai.configure(model_catalog=Catalog())

from matrx_ai.catalog.resolve import resolve_call_profile

async def main():
    profile = await resolve_call_profile("mock-model")
    assert profile.wire_format == "mock_chat", profile

asyncio.run(main())
"""
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
    }
    if "VIRTUAL_ENV" in os.environ:
        env["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV"]
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
