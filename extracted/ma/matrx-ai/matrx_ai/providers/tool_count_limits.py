"""Provider-enforced ceilings on the number of tool declarations in ONE request.

These are wire facts of each provider's API (a request over the ceiling is
refused), not platform opinions, so they live with the provider layer
(root CLAUDE.md: "provider limits live in matrx_ai/providers"). The tool
declaration ledger (matrx_ai/tools/declaration_ledger.py) reads them so its
append-only array never grows past what the provider accepts.

``None`` = no documented ceiling known for that wire; the ledger then never
evicts on count. Add a wire here the day its documented limit is known.
"""

from __future__ import annotations

#: OpenAI documents a maximum of 128 tools (functions) per request on Chat
#: Completions and Responses. The OpenAI-compatible wires mirror that schema and
#: are held to the same ceiling rather than guessed higher.
_OPENAI_FUNCTION_CEILING = 128

PROVIDER_TOOL_CEILINGS: dict[str, int | None] = {
    "openai": _OPENAI_FUNCTION_CEILING,
    "generic_openai": _OPENAI_FUNCTION_CEILING,
    "groq": _OPENAI_FUNCTION_CEILING,
    "cerebras": _OPENAI_FUNCTION_CEILING,
    "together": _OPENAI_FUNCTION_CEILING,
    "xai": _OPENAI_FUNCTION_CEILING,
    # No documented per-request tool-count ceiling known for these wires.
    "anthropic": None,
    "google": None,
}


def provider_tool_ceiling(provider: str | None) -> int | None:
    return PROVIDER_TOOL_CEILINGS.get(str(provider or "").lower())
