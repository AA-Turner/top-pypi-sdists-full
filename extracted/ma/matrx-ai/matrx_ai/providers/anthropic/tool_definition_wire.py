"""Anthropic wire calls a TOOL-DEFINITION check needs, kept in the provider layer.

Why this is a provider-layer primitive and not script-local code
---------------------------------------------------------------
``scripts/tool_definition_lint.py`` prices a tool definition in tokens and
``scripts/tool_definition_trial.py`` asks a model whether a condensed definition
is still called correctly. Both built a raw ``anthropic.Anthropic`` client in a
script, which ``scripts/check_raw_llm_clients.py`` rightly refuses
(``scripts/`` is not an allowed home for a provider client). The question each one
asks -- "how many tokens is this body", "does the model call this tool correctly"
-- is provider knowledge, so the wire lives HERE, beside the translators, exactly
like ``providers/structured_output_probe.py``.

* ``count_input_tokens`` is the ``/v1/messages/count_tokens`` endpoint: it counts
  and SPENDS NOTHING (no inference, no sampling).
* ``tool_call_trial`` is ONE real Messages call (paid, a few thousand tokens) over
  a caller-supplied RAW tool definition. It cannot be a Holder run: the thing under
  test is the definition itself, and a Holder fixes its own tools. It returns the
  tool input the model chose plus the tokens it spent, so the caller reports the cost.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx

from matrx_ai.providers.anthropic.broker import ANTHROPIC_API_VERSION, COUNT_TOKENS_URL, MESSAGES_URL

_RETRYABLE = frozenset({408, 409, 429, 500, 502, 503, 504, 529})


def _headers(api_key: str) -> dict[str, str]:
    return {"x-api-key": api_key, "anthropic-version": ANTHROPIC_API_VERSION, "content-type": "application/json"}


def _post(url: str, api_key: str, body: dict[str, Any], *, max_retries: int, timeout: float) -> dict[str, Any]:
    """POST with the SDK's own retry shape (backoff on 429/5xx); raises ``httpx.HTTPStatusError`` otherwise."""
    last: httpx.Response | None = None
    for attempt in range(max_retries + 1):
        resp = httpx.post(url, headers=_headers(api_key), json=body, timeout=timeout)
        if resp.status_code not in _RETRYABLE:
            resp.raise_for_status()
            return resp.json()
        last = resp
        time.sleep(min(2.0**attempt, 30.0))
    assert last is not None
    last.raise_for_status()
    return last.json()


def count_input_tokens(
    *,
    api_key: str,
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    system: str | None = None,
    max_retries: int = 8,
    timeout: float = 60.0,
) -> int:
    """Input tokens Anthropic would bill for this body. Free: no inference runs."""
    body: dict[str, Any] = {"model": model, "messages": messages}
    if tools:
        body["tools"] = tools
    if system:
        body["system"] = system
    return int(_post(COUNT_TOKENS_URL, api_key, body, max_retries=max_retries, timeout=timeout)["input_tokens"])


@dataclass(frozen=True)
class ToolCallTrial:
    """What one trial call produced. ``tool_input`` is ``None`` when the model chose not to call a tool."""

    tool_input: dict[str, Any] | None
    input_tokens: int
    output_tokens: int


def tool_call_trial(
    *,
    api_key: str,
    model: str,
    system: str,
    prompt: str,
    tools: list[dict[str, Any]],
    max_tokens: int = 2048,
    max_retries: int = 8,
    timeout: float = 120.0,
) -> ToolCallTrial:
    """One paid Messages call over a raw tool definition; returns the first ``tool_use`` input."""
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "tools": tools,
        "messages": [{"role": "user", "content": prompt}],
    }
    payload = _post(MESSAGES_URL, api_key, body, max_retries=max_retries, timeout=timeout)
    call = next((b.get("input") for b in payload.get("content") or [] if b.get("type") == "tool_use"), None)
    usage = payload.get("usage") or {}
    return ToolCallTrial(call, int(usage.get("input_tokens") or 0), int(usage.get("output_tokens") or 0))
