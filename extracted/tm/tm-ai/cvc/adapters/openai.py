"""
cvc.adapters.openai — OpenAI adapter for GPT-5.2 and GPT-series models.

Translates CVC's internal ``ChatCompletionRequest`` to the OpenAI Chat
Completions API, forwarding prompt-caching hints where supported.

Default model: ``gpt-5.2`` — OpenAI's best model for coding and agentic tasks.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

import httpx

from cvc.adapters.base import BaseAdapter
from cvc.core.models import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    UsageInfo,
)

logger = logging.getLogger("cvc.adapters.openai")

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# ---- Available Models (verified Feb 2026) --------------------------------
# gpt-5.3         — Newest flagship: best reasoning & coding
# gpt-5.2         — Previous flagship: coding & agentic tasks
# gpt-5.2-codex   — Optimized for long-horizon agentic coding
# gpt-5.2-pro     — Higher quality, more compute
# gpt-5-mini      — Fast & cost-efficient
# gpt-5-nano      — Fastest & cheapest
# gpt-4.1         — Smartest non-reasoning model
# --------------------------------------------------------------------------

DEFAULT_MODEL = "gpt-5.2"


class OpenAIAdapter(BaseAdapter):
    """
    Sends ``ChatCompletionRequest`` objects to the OpenAI API.

    Since the CVC proxy already speaks the OpenAI wire format, translation
    is minimal.  The adapter injects a ``store: true`` hint on committed
    prefix messages so that OpenAI's server-side prompt caching can take
    effect (available on GPT-4+ with prompts > 1 024 tokens).
    """

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        base_url: str = "https://api.openai.com",
        chat_completions_path: str = "/v1/chat/completions",
    ) -> None:
        """Initialise the OpenAI adapter.

        ``base_url`` defaults to the public OpenAI endpoint. Pass an
        alternate base URL (no trailing /v1) to point the adapter at
        any OpenAI-compatible service — z.ai/GLM, Kimi, OpenCode, etc.

        ``chat_completions_path`` lets you override the request path
        (default ``/v1/chat/completions``). Providers like z.ai that
        expose the OpenAI shape at a non-``/v1`` URL (e.g. z.ai's
        ``/api/paas/v4/chat/completions``) can pass
        ``chat_completions_path="/chat/completions"`` to make the full
        request land at ``https://api.z.ai/api/paas/v4/chat/completions``.

        The base URL is auto-normalised: any trailing ``/v1`` is stripped
        so the path joins cleanly. Paths like ``/api/paas/v4`` are left
        alone — we don't strip random version segments.
        """
        self._api_key = api_key
        self._model = model
        self._chat_completions_path = chat_completions_path
        base = (base_url or "https://api.openai.com").rstrip("/")
        if base.endswith("/v1"):
            base = base[:-3]
        # ``_client.base_url`` is a ``httpx.URL``; httpx normalises the
        # path when it sees ``//``, so we don't need to chase trailing
        # slashes manually. However, when we hand the chat path directly
        # to ``client.post()``, httpx joins it as-is, so we have to
        # ensure our path starts with exactly one ``/`` and doesn't get
        # re-joined onto a trailing slash.
        if not chat_completions_path.startswith("/"):
            self._chat_completions_path = "/" + chat_completions_path
        self._client = httpx.AsyncClient(
            base_url=base,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def complete(
        self,
        request: ChatCompletionRequest,
        *,
        committed_prefix_len: int = 0,
    ) -> ChatCompletionResponse:
        """Forward the request to OpenAI, returning a normalised response."""
        messages = [self._convert_message(m) for m in request.messages]

        body: dict[str, Any] = {
            "model": request.model or self._model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        if request.tools:
            body["tools"] = request.tools
        if request.tool_choice:
            body["tool_choice"] = request.tool_choice

        # Enable automatic prompt caching (prefix-based)
        if committed_prefix_len > 0:
            body["store"] = True

        logger.debug(
            "OpenAI request: model=%s messages=%d prefix=%d",
            body["model"],
            len(messages),
            committed_prefix_len,
        )

        resp = await self._client.post(self._chat_completions_path, json=body)
        resp.raise_for_status()
        data = resp.json()

        return self._to_response(data)

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _convert_message(msg: ChatMessage) -> dict[str, Any]:
        """Convert a Pydantic ChatMessage to a plain dict for the API."""
        entry: dict[str, Any] = {"role": msg.role}
        if msg.content is not None:
            entry["content"] = msg.content
        if msg.name:
            entry["name"] = msg.name
        if msg.tool_call_id:
            entry["tool_call_id"] = msg.tool_call_id
        if msg.tool_calls:
            entry["tool_calls"] = msg.tool_calls
        return entry

    @staticmethod
    def _to_response(data: dict[str, Any]) -> ChatCompletionResponse:
        """Convert a raw OpenAI JSON response to our internal schema."""
        choices: list[ChatCompletionChoice] = []
        for c in data.get("choices", []):
            raw_msg = c.get("message", {})
            msg = ChatMessage(
                role=raw_msg.get("role", "assistant"),
                content=raw_msg.get("content"),
                tool_calls=raw_msg.get("tool_calls"),
            )
            choices.append(
                ChatCompletionChoice(
                    index=c.get("index", 0),
                    message=msg,
                    finish_reason=c.get("finish_reason", "stop"),
                )
            )

        usage_data = data.get("usage", {})
        cache_read = usage_data.get("prompt_tokens_details", {}).get(
            "cached_tokens", 0
        )
        usage = UsageInfo(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0),
            cache_read_tokens=cache_read,
            cache_creation_tokens=0,
        )

        return ChatCompletionResponse(
            id=data.get("id", ""),
            model=data.get("model", ""),
            choices=choices,
            usage=usage,
        )
