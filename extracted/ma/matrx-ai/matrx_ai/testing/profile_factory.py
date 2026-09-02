"""Test/standalone factory for ``ResolvedCallProfile`` objects.

The B4 flip made every chat translator take the resolved call profile
(``profile.controls`` drives param shaping; ``profile.capabilities`` drives the
structural TTS/vision branches). Tests and client-side scripts build profiles here
instead of hand-constructing the Pydantic object — one factory, honest
defaults, and the control rules can come straight from a chat-param-golden
fixture's ``rules`` payload so tests exercise the REAL rule snapshot.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule, ResolvedCallProfile
from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

_DEFAULT_CHAT_CAPABILITIES: dict[str, Any] = {
    "input": ["text", "image"],
    "output": ["text"],
    "features": ["function_calling", "structured_output"],
    "interaction": "turn",
    "multilingual": True,
}


class _CapSource:
    def __init__(self, name: str, capabilities: dict[str, Any]) -> None:
        self.name = name
        self.capabilities = capabilities


def compile_rules(
    rules: dict[str, Any] | None, value_orders: dict[str, list[Any]] | None = None
) -> CompiledControlsMap:
    """Build a ``CompiledControlsMap`` from plain rule dicts (e.g. a golden
    fixture's ``rules`` payload, or an inline dict in a test)."""
    compiled = {
        key: rule if isinstance(rule, ControlRule) else ControlRule.model_validate(rule)
        for key, rule in (rules or {}).items()
    }
    return CompiledControlsMap(rules=compiled, value_orders=value_orders or {})


def make_profile(
    *,
    model_name: str = "test-model",
    wire_format: str = "openai_chat",
    rules: dict[str, Any] | None = None,
    value_orders: dict[str, list[Any]] | None = None,
    controls: CompiledControlsMap | None = None,
    capabilities: dict[str, Any] | None = None,
    provider_model_id: str | None = None,
    vendor: str | None = None,
    request_defaults: dict[str, Any] | None = None,
) -> ResolvedCallProfile:
    resolved_vendor = vendor or (
        wire_format.rsplit("_", 1)[0] if "_" in wire_format else wire_format
    )
    caps = resolve_model_capabilities(
        _CapSource(model_name, capabilities or dict(_DEFAULT_CHAT_CAPABILITIES))
    )
    return ResolvedCallProfile(
        model_id=f"test:{model_name}",
        model_name=model_name,
        provider_model_id=provider_model_id or model_name,
        offering_id=f"test-offering:{model_name}",
        endpoint_id=f"test-endpoint:{resolved_vendor}",
        api_id=f"test-api:{wire_format}",
        provider_name=resolved_vendor,
        vendor=resolved_vendor,
        wire_format=wire_format,
        client_attr=wire_format,
        base_url=None,
        auth_ref={},
        byok_secret_key=None,
        capabilities=caps,
        controls=controls if controls is not None else compile_rules(rules, value_orders),
        request_defaults=request_defaults or {},
        pricing=None,
        usage_basis=None,
        token_billed=False,
    )


__all__ = ["compile_rules", "make_profile"]
