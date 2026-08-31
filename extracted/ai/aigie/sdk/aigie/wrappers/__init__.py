"""Per-provider wrappers for automatic tracing of raw LLM calls.

A wrapper stands in for a provider's client object, passes every call through
untouched, and emits one finalized `llm` span for it. These are distinct from
`aigie.integrations`, which traces a whole agent run through someone else's
framework — a wrapper sees one API call and knows nothing about a framework.

One module per provider:

- `openai`    — OpenAI and Azure OpenAI
- `anthropic` — Anthropic Claude
- `gemini`    — Google Gemini
- `bedrock`   — AWS Bedrock
- `cohere`    — Cohere

Resolution is lazy, per name, so reaching for one provider does not import the
other four. That matters because `aigie/__init__.py` is itself lazy for exactly
this reason: re-exporting eagerly here would undo it and make
`aigie.wrap_bedrock` pay for the OpenAI and Anthropic modules it never touches.
`test_wrapper_public_api.py` pins it.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

# Exported name -> the module in this package that defines it.
_EXPORTS: dict[str, str] = {
    "AnthropicWrapper": "anthropic",
    "wrap_anthropic": "anthropic",
    "create_traced_bedrock": "bedrock",
    "unwrap_bedrock": "bedrock",
    "wrap_bedrock": "bedrock",
    "create_traced_cohere": "cohere",
    "unwrap_cohere": "cohere",
    "wrap_cohere": "cohere",
    "wrap_gemini": "gemini",
    "OpenAIWrapper": "openai",
    "wrap_openai": "openai",
}


def __getattr__(name: str) -> Any:
    """Import the one provider module that defines `name`, on first access."""
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    # Deliberately not cached in globals(): caching would freeze the binding, so
    # mock.patch("aigie.wrappers.<provider>.<name>") would stop being visible
    # through the facade. This is a setup-time lookup, not a per-call path.
    return getattr(import_module(f"aigie.wrappers.{module_name}"), name)


def __dir__() -> list[str]:
    return sorted(__all__)


if TYPE_CHECKING:
    from aigie.wrappers.anthropic import AnthropicWrapper, wrap_anthropic
    from aigie.wrappers.bedrock import create_traced_bedrock, unwrap_bedrock, wrap_bedrock
    from aigie.wrappers.cohere import create_traced_cohere, unwrap_cohere, wrap_cohere
    from aigie.wrappers.gemini import wrap_gemini
    from aigie.wrappers.openai import OpenAIWrapper, wrap_openai

__all__ = [
    "AnthropicWrapper",
    "OpenAIWrapper",
    "create_traced_bedrock",
    "create_traced_cohere",
    "unwrap_bedrock",
    "unwrap_cohere",
    "wrap_anthropic",
    "wrap_bedrock",
    "wrap_cohere",
    "wrap_gemini",
    "wrap_openai",
]
