"""Phase 3a — generic_openai instance registry tests.

Locks the contract matrx-local depends on:

* ``register_generic_openai_instance(name, instance)`` stores the
  instance under that name.
* ``unregister_generic_openai_instance(name)`` removes it.
* ``get_generic_openai_instance(name)`` looks it up.
* Re-registering the same name replaces silently (idempotent).
* The registry survives import boundaries — matrx-local imports the
  functions; the storage lives at module scope inside
  ``matrx_ai.providers.unified_client``.

Also locks the dispatch contract:

* ``UnifiedAIClient.execute()`` for the ``generic_openai_chat``
  endpoint resolves ``model_name`` against the registry FIRST.
* Misses fall through to the ``"default"`` registered instance.
* If neither is registered, the legacy ``huggingface_chat`` singleton
  is used (preserves any cloud usage of ``generic_openai_standard``).

We test the dispatch via a stub UnifiedAIClient subclass so we don't
need real API keys or the full instantiation chain.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_ai.providers import unified_client as uc_mod


@pytest.fixture(autouse=True)
def _clean_registry():
    """Reset the module-level registry between tests so state can't
    leak between cases."""
    snapshot = dict(uc_mod._generic_openai_instances)
    uc_mod._generic_openai_instances.clear()
    yield
    uc_mod._generic_openai_instances.clear()
    uc_mod._generic_openai_instances.update(snapshot)


# ---------------------------------------------------------------------------
# Registry contract
# ---------------------------------------------------------------------------


def test_register_stores_instance():
    sentinel = object()
    uc_mod.register_generic_openai_instance("llama_cpp/qwen2.5", sentinel)
    assert uc_mod.get_generic_openai_instance("llama_cpp/qwen2.5") is sentinel


def test_register_is_idempotent():
    first = object()
    second = object()
    uc_mod.register_generic_openai_instance("model-a", first)
    uc_mod.register_generic_openai_instance("model-a", second)
    assert uc_mod.get_generic_openai_instance("model-a") is second


def test_register_signature_is_name_and_instance_only():
    """The registry is keyed purely by canonical model name. No routing hint is
    accepted — the wire route comes from the catalog, never from the caller."""
    import inspect

    params = list(inspect.signature(uc_mod.register_generic_openai_instance).parameters)
    assert params == ["name", "instance"]

    sentinel = object()
    uc_mod.register_generic_openai_instance("model-b", sentinel)
    assert uc_mod.get_generic_openai_instance("model-b") is sentinel


def test_unregister_removes_instance():
    uc_mod.register_generic_openai_instance("model-c", object())
    uc_mod.unregister_generic_openai_instance("model-c")
    assert uc_mod.get_generic_openai_instance("model-c") is None


def test_unregister_unknown_is_noop():
    """No exception when removing a name that was never registered."""
    uc_mod.unregister_generic_openai_instance("never-registered")
    assert uc_mod.get_generic_openai_instance("never-registered") is None


def test_get_returns_none_for_unknown():
    assert uc_mod.get_generic_openai_instance("unknown") is None


# ---------------------------------------------------------------------------
# Dispatch contract — UnifiedAIClient.execute() resolution order
# ---------------------------------------------------------------------------


@dataclass
class _StubResult:
    routed_to: str
    config: Any = None
    profile: object | None = None


class _StubChat:
    """Minimal chat-execute target — records that .execute() was hit
    so the dispatch test can assert which instance won the lookup."""

    def __init__(self, label: str):
        self.label = label
        self.calls: list[_StubResult] = []

    async def execute(self, config, profile, debug):  # noqa: ARG002
        result = _StubResult(routed_to=self.label, config=config, profile=profile)
        self.calls.append(result)
        return {"routed_to": self.label}


@dataclass
class _StubConfig:
    model: str
    messages: list = field(default_factory=list)
    matrx_model_name: str | None = None
    response_format: Any = None
    internal_web_search: Any = None
    internal_x_search: Any = None
    dictionary: Any = None
    system_instruction: Any = None
    tools: list = field(default_factory=list)
    custom_tools: list = field(default_factory=list)
    mcp_servers: list = field(default_factory=list)
    internal_url_context: Any = None


@dataclass
class _StubRequest:
    config: _StubConfig
    debug: bool = False

    def add_usage(self, usage):  # noqa: ARG002
        pass


def _profile(model_name: str, wire_format: str, _unused_api_class: str = ""):
    """A ResolvedCallProfile-shaped stub. Routing is entirely the catalog's answer —
    the client never re-derives it, so the test hands it the answer directly."""
    from types import SimpleNamespace

    from matrx_ai.catalog.resolve import client_attr_for_wire_format
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    caps = resolve_model_capabilities(
        SimpleNamespace(
            name=model_name,
            capabilities={
                "input": ["text"],
                "output": ["text"],
                "features": ["function_calling", "structured_output", "json_mode"],
            },
        )
    )
    return SimpleNamespace(
        model_id="00000000-0000-0000-0000-000000000000",
        model_name=model_name,
        provider_model_id=model_name,
        offering_id="off",
        endpoint_id="ep",
        api_id="api",
        provider_name="Test",
        wire_format=wire_format,
        client_attr=client_attr_for_wire_format(wire_format),
        capabilities=caps,
    )


def _build_client(profile, monkeypatch):
    """Construct a UnifiedAIClient with the heavy provider singletons + the catalog
    resolve stubbed out so we can exercise dispatch without a DB or real SDKs."""
    from matrx_ai.catalog import resolve as resolve_mod
    from matrx_ai.providers.unified_client import UnifiedAIClient

    async def _fake_resolve(model_ref, endpoint_hint=None, offering_id=None):  # noqa: ARG001
        return profile

    monkeypatch.setattr(resolve_mod, "resolve_call_profile", _fake_resolve)
    monkeypatch.setattr(
        "matrx_ai.processing.audio.audio_preprocessing.should_preprocess_audio",
        lambda *a, **kw: False,
    )

    client = UnifiedAIClient.__new__(UnifiedAIClient)
    # Only the huggingface_chat fallback matters for the generic_openai_chat branch.
    client.huggingface_chat = _StubChat("huggingface_chat_fallback")

    async def _noop(*a, **kw):
        return None

    client._annotate_and_resolve_image_refs = _noop
    return client


@pytest.mark.asyncio
async def test_dispatch_uses_exact_name_match(monkeypatch):
    """A registered exact-name match wins over both 'default' and the
    huggingface_chat fallback."""
    exact = _StubChat("exact")
    default = _StubChat("default")
    uc_mod.register_generic_openai_instance("llama_cpp/qwen2.5", exact)
    uc_mod.register_generic_openai_instance("default", default)

    profile = _profile("llama_cpp/qwen2.5", "generic_openai_chat", "generic_openai_standard")
    client = _build_client(profile, monkeypatch)
    request = _StubRequest(config=_StubConfig(model="llama_cpp/qwen2.5"))
    out = await client.execute(request)
    assert out == {"routed_to": "exact"}
    assert len(exact.calls) == 1
    assert default.calls == []
    assert client.huggingface_chat.calls == []


@pytest.mark.asyncio
async def test_dispatch_lookup_uses_canonical_name_not_provider_model_id(monkeypatch):
    """The registry is keyed by the canonical name while only the call clone uses
    the offering's provider model id."""
    exact = _StubChat("exact")
    uc_mod.register_generic_openai_instance("llama_cpp/qwen2.5", exact)

    profile = _profile("llama_cpp/qwen2.5", "generic_openai_chat", "generic_openai_standard")
    profile.provider_model_id = "qwen2.5-7b-instruct-q4"
    client = _build_client(profile, monkeypatch)
    request = _StubRequest(config=_StubConfig(model="llama_cpp/qwen2.5"))
    out = await client.execute(request)
    assert out == {"routed_to": "exact"}
    # The provider id — not the canonical name — is what goes on the wire.
    assert exact.calls[0].config.model == "qwen2.5-7b-instruct-q4"
    assert exact.calls[0].config.matrx_model_name == "llama_cpp/qwen2.5"
    # Durable request state must remain resolvable for retries and later turns.
    assert request.config.model == "llama_cpp/qwen2.5"
    assert request.config.matrx_model_name is None


@pytest.mark.asyncio
async def test_dispatch_falls_back_to_default(monkeypatch):
    """When no exact-name match exists, 'default' is used."""
    default = _StubChat("default")
    uc_mod.register_generic_openai_instance("default", default)

    profile = _profile("llama_cpp/unknown-model", "generic_openai_chat", "generic_openai_standard")
    client = _build_client(profile, monkeypatch)
    request = _StubRequest(config=_StubConfig(model="llama_cpp/unknown-model"))
    out = await client.execute(request)
    assert out == {"routed_to": "default"}
    assert default.calls[0].profile.wire_format == "generic_openai_chat"


@pytest.mark.asyncio
async def test_dispatch_falls_back_to_huggingface_chat_when_registry_empty(monkeypatch):
    """No registered instances → the HuggingFaceChat singleton path."""
    profile = _profile("some-model", "generic_openai_chat", "generic_openai_standard")
    client = _build_client(profile, monkeypatch)
    request = _StubRequest(config=_StubConfig(model="some-model"))
    out = await client.execute(request)
    assert out == {"routed_to": "huggingface_chat_fallback"}


@pytest.mark.asyncio
async def test_dispatch_default_does_not_override_huggingface_route(monkeypatch):
    """A registered 'default' must NOT intercept the ``huggingface_chat`` wire route —
    that dispatches to the huggingface_chat client attr. Only the
    ``generic_openai_chat`` route consults the registry."""
    default = _StubChat("default")
    uc_mod.register_generic_openai_instance("default", default)

    profile = _profile("hf-cloud-model", "huggingface_chat", "huggingface_standard")
    client = _build_client(profile, monkeypatch)
    client.huggingface_chat = _StubChat("huggingface_chat")

    request = _StubRequest(config=_StubConfig(model="hf-cloud-model"))
    out = await client.execute(request)
    assert out == {"routed_to": "huggingface_chat"}
    # The registry's "default" must NOT have been invoked.
    assert default.calls == []


@pytest.mark.asyncio
async def test_dispatch_raises_loudly_for_an_unknown_wire_format(monkeypatch):
    """A wire_format with no client is a catalog data bug — it must raise, never
    silently pick a provider."""
    profile = _profile("weird", "quantum_chat", "quantum_standard")
    client = _build_client(profile, monkeypatch)
    request = _StubRequest(config=_StubConfig(model="weird"))
    with pytest.raises(ValueError, match="no dispatch for wire_format"):
        await client.execute(request)


# ---------------------------------------------------------------------------
# Module-level export contract
# ---------------------------------------------------------------------------


def test_functions_importable_from_unified_client_module():
    """matrx-local imports these names by their full dotted path. Lock
    the import contract so a future rename forces a deliberate update
    here AND on the matrx-local side."""
    from matrx_ai.providers.unified_client import (
        get_generic_openai_instance,
        register_generic_openai_instance,
        unregister_generic_openai_instance,
    )

    assert callable(register_generic_openai_instance)
    assert callable(unregister_generic_openai_instance)
    assert callable(get_generic_openai_instance)
