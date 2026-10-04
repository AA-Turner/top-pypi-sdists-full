"""Ask a real provider whether it ACCEPTS a translated output contract.

Why this is a provider-layer primitive and not script-local code
---------------------------------------------------------------
Arman, 2026-09-27: *the shape we hold is modified by each provider's translator;
a provider rejecting our request is OUR translator's bug.* Proving that means
asking the provider — no local metric predicts Anthropic's compiled-grammar
budget or OpenAI's strict rules (see ``scripts/check_kind_grammar_budget.py``'s
header for the measurements). "Does vendor X accept this body?" is provider
knowledge, so the wire call lives HERE, beside the translators, in the one place
``scripts/check_raw_llm_clients.py`` sanctions a provider call
(``CALL_SHAPE_EXECUTORS`` / ``ALLOWED`` → ``packages/matrx-ai/matrx_ai/providers/``).

Two guards used to each own a private copy of this wire instead:

* ``scripts/check_structured_output_corpus.py`` built raw ``Anthropic()`` /
  ``OpenAI()`` / ``genai.Client()`` clients — 7 sites the guard reported the day
  they landed (2026-09-27), because ``scripts/`` was deliberately removed from
  the allow-list on 2026-09-25: *a paid call from a script is a paid call*;
* ``scripts/check_kind_grammar_budget.py`` imported ``MESSAGES_URL`` from
  ``providers/anthropic/broker.py`` and POSTed to it with ``httpx``, which the
  guard could not see at all (its host detection was literal-string-only).

Neither belonged in a script. The right answer to both is ONE primitive, which is
also why the answer is reusable: the in-app checks system
(``common-docs/systems/architecture/observability/projects/checks-run-in-the-app``) can run these probes on a
schedule without a second implementation.

What a probe is, and is not
---------------------------
A probe is a COMPILE/VALIDATE question, not a generation: ``max_tokens`` sits at
the floor, the prompt is one line, and nothing useful is sampled. It is still a
PAID call (a handful of input tokens), so every function returns the tokens it
spent and the caller reports the cost — a probe never hides what it spends.

A probe deliberately does NOT go through ``UnifiedAIClient.execute``: the
question is whether the RAW body our translator produced is accepted, so putting
the retry ladder, the catalog and the cost ledger between the question and the
answer would mask exactly the regression these guards exist to catch. That is
why this module takes an already-translated body and sends nothing else.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from matrx_ai.providers.anthropic.broker import ANTHROPIC_API_VERSION, MESSAGES_URL
from matrx_ai.providers.openai.broker import RESPONSES_URL

#: Google's generateContent endpoint. Google has no broker module to hold it yet;
#: when one lands, this constant moves there and this import follows.
GOOGLE_GENERATE_CONTENT_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
#: Cerebras speaks the OpenAI Chat Completions shape at its own host.
CEREBRAS_CHAT_COMPLETIONS_URL = "https://api.cerebras.ai/v1/chat/completions"
#: The other three OpenAI-compatible chat hosts. All four reach the wire through
#: the SAME translator (``BaseTranslator.build_openai_chat_response_format`` /
#: ``translate_openai_compatible_output_schema``), so a change to it could only
#: ever be proven on one of the four endpoints it feeds until these existed —
#: and it feeds all four, which is the whole reason it is shared.
GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"
XAI_CHAT_COMPLETIONS_URL = "https://api.x.ai/v1/chat/completions"
TOGETHER_CHAT_COMPLETIONS_URL = "https://api.together.xyz/v1/chat/completions"

#: provider → (url, name of the env var holding its key). ONE table, so a caller
#: cannot quietly probe the wrong host with the wrong key.
OPENAI_COMPATIBLE_CHAT_ENDPOINTS: dict[str, tuple[str, str]] = {
    "cerebras": (CEREBRAS_CHAT_COMPLETIONS_URL, "CEREBRAS_API_KEY"),
    "groq": (GROQ_CHAT_COMPLETIONS_URL, "GROQ_API_KEY"),
    "xai": (XAI_CHAT_COMPLETIONS_URL, "XAI_API_KEY"),
    "together": (TOGETHER_CHAT_COMPLETIONS_URL, "TOGETHER_API_KEY"),
}

PROBE_PROMPT = "Reply with the smallest valid answer."
_TIMEOUT_SECONDS = 400.0


@dataclass(frozen=True)
class ProbeResult:
    """What the provider said about one body."""

    accepted: bool
    #: Provider error text when refused (empty when accepted).
    error: str = ""
    tokens_in: int = 0
    tokens_out: int = 0
    #: True when the probe never reached the provider (transport failure) — a
    #: non-verdict the caller must not read as a refusal.
    unreachable: bool = False


def _key(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"{name} is not set; the structured-output probe asks the real provider "
            f"and cannot answer without it."
        )
    return value


async def _post(url: str, *, headers: dict[str, str], body: dict[str, Any]) -> Any:
    import httpx

    async with httpx.AsyncClient(timeout=_TIMEOUT_SECONDS) as client:
        return await client.post(url, headers=headers, json=body)


def _error_text(response: Any) -> str:
    try:
        payload = response.json()
    except Exception:  # noqa: BLE001 — a non-JSON body is still the error
        return str(response.text)[:600]
    error = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(error, dict):
        return str(error.get("message") or error)[:600]
    return str(payload)[:600]


async def probe_anthropic_messages(body: dict[str, Any]) -> ProbeResult:
    """Send an already-built Anthropic Messages body exactly as given.

    Takes the WHOLE body so a caller can drive the real retry ladder
    (``AnthropicChat._retry_over_grammar_budget``) through this one wire.
    """
    try:
        response = await _post(
            MESSAGES_URL,
            headers={
                "x-api-key": _key("ANTHROPIC_API_KEY"),
                "anthropic-version": ANTHROPIC_API_VERSION,
                "content-type": "application/json",
            },
            body=body,
        )
    except Exception as exc:  # noqa: BLE001 — transport failure is not a verdict
        return ProbeResult(accepted=False, error=f"unreachable: {exc}", unreachable=True)
    if response.status_code != 200:
        return ProbeResult(accepted=False, error=_error_text(response))
    usage = (response.json() or {}).get("usage") or {}
    return ProbeResult(
        accepted=True,
        tokens_in=int(usage.get("input_tokens") or 0),
        tokens_out=int(usage.get("output_tokens") or 0),
    )


async def probe_anthropic_output_format(
    model: str,
    output_format: dict[str, Any] | None,
    tools: list[dict[str, Any]] | None = None,
    *,
    max_tokens: int = 64,
    effort: str | None = "low",
    prompt: str = PROBE_PROMPT,
) -> ProbeResult:
    """Minimal Messages request carrying ``output_format`` (and optional tools)."""
    output_config: dict[str, Any] = {}
    if effort:
        output_config["effort"] = effort
    if output_format:
        output_config["format"] = output_format
    body: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if output_config:
        body["output_config"] = output_config
    if tools:
        body["tools"] = tools
    return await probe_anthropic_messages(body)


async def probe_openai_text_format(
    model: str,
    text_format: dict[str, Any] | None,
    *,
    max_output_tokens: int = 64,
    prompt: str = PROBE_PROMPT,
) -> ProbeResult:
    """Minimal Responses request carrying ``text.format`` as translated."""
    body: dict[str, Any] = {
        "model": model,
        "input": prompt,
        "max_output_tokens": max_output_tokens,
    }
    if text_format:
        body["text"] = {"format": text_format}
    try:
        response = await _post(
            RESPONSES_URL,
            headers={
                "authorization": f"Bearer {_key('OPENAI_API_KEY')}",
                "content-type": "application/json",
            },
            body=body,
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(accepted=False, error=f"unreachable: {exc}", unreachable=True)
    if response.status_code != 200:
        return ProbeResult(accepted=False, error=_error_text(response))
    usage = (response.json() or {}).get("usage") or {}
    return ProbeResult(
        accepted=True,
        tokens_in=int(usage.get("input_tokens") or 0),
        tokens_out=int(usage.get("output_tokens") or 0),
    )


async def probe_google_response_schema(
    model: str,
    response_schema: dict[str, Any] | None,
    *,
    max_output_tokens: int = 256,
    prompt: str = PROBE_PROMPT,
) -> ProbeResult:
    """Minimal generateContent request carrying the translated JSON schema."""
    generation_config: dict[str, Any] = {
        "maxOutputTokens": max_output_tokens,
        "thinkingConfig": {"thinkingBudget": 0},
    }
    if response_schema is not None:
        generation_config["responseMimeType"] = "application/json"
        generation_config["responseJsonSchema"] = response_schema
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": generation_config,
    }
    try:
        response = await _post(
            GOOGLE_GENERATE_CONTENT_URL.format(model=model),
            headers={
                "x-goog-api-key": _key("GEMINI_API_KEY"),
                "content-type": "application/json",
            },
            body=body,
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(accepted=False, error=f"unreachable: {exc}", unreachable=True)
    if response.status_code != 200:
        return ProbeResult(accepted=False, error=_error_text(response))
    usage = (response.json() or {}).get("usageMetadata") or {}
    return ProbeResult(
        accepted=True,
        tokens_in=int(usage.get("promptTokenCount") or 0),
        tokens_out=int(usage.get("candidatesTokenCount") or 0),
    )


async def probe_openai_compatible_response_format(
    provider: str,
    model: str,
    response_format: dict[str, Any] | None,
    *,
    max_tokens: int = 64,
    prompt: str = PROBE_PROMPT,
) -> ProbeResult:
    """Minimal Chat Completions request carrying ``response_format``, at whichever
    of the four OpenAI-compatible hosts ``provider`` names.

    One function for all four because ONE translator builds the body for all four;
    a per-provider copy is how four endpoints ended up with one endpoint's worth
    of evidence.
    """
    endpoint = OPENAI_COMPATIBLE_CHAT_ENDPOINTS.get(provider)
    if endpoint is None:
        raise RuntimeError(
            f"{provider!r} is not an OpenAI-compatible chat provider this probe knows; "
            f"known: {sorted(OPENAI_COMPATIBLE_CHAT_ENDPOINTS)}"
        )
    url, key_name = endpoint
    body: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    if response_format:
        body["response_format"] = response_format
    try:
        response = await _post(
            url,
            headers={
                "authorization": f"Bearer {_key(key_name)}",
                "content-type": "application/json",
            },
            body=body,
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(accepted=False, error=f"unreachable: {exc}", unreachable=True)
    if response.status_code != 200:
        return ProbeResult(accepted=False, error=_error_text(response))
    usage = (response.json() or {}).get("usage") or {}
    return ProbeResult(
        accepted=True,
        tokens_in=int(usage.get("prompt_tokens") or 0),
        tokens_out=int(usage.get("completion_tokens") or 0),
    )


__all__ = [
    "CEREBRAS_CHAT_COMPLETIONS_URL",
    "GOOGLE_GENERATE_CONTENT_URL",
    "GROQ_CHAT_COMPLETIONS_URL",
    "OPENAI_COMPATIBLE_CHAT_ENDPOINTS",
    "PROBE_PROMPT",
    "TOGETHER_CHAT_COMPLETIONS_URL",
    "XAI_CHAT_COMPLETIONS_URL",
    "ProbeResult",
    "probe_anthropic_messages",
    "probe_anthropic_output_format",
    "probe_google_response_schema",
    "probe_openai_compatible_response_format",
    "probe_openai_text_format",
]
