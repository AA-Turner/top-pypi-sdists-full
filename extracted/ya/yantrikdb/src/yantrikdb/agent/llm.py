"""LLM client for llama.cpp OpenAI-compatible API."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx

from yantrikdb.agent.config import LLMConfig

log = logging.getLogger("yantrik.llm")


@dataclass
class LLMResponse:
    content: str = ""
    tool_calls: Optional[list[dict]] = None
    finish_reason: str = "stop"
    usage: dict = field(default_factory=dict)


class LLMClient:
    """Async HTTP client for llama.cpp's OpenAI-compatible API."""

    def __init__(self, config: LLMConfig):
        self.config = config
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=httpx.Timeout(180.0, connect=10.0),
        )

    async def chat(
        self,
        messages: list[dict],
        tools: Optional[list[dict]] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": self.config.temperature,
        }
        if tools:
            payload["tools"] = tools

        try:
            resp = await self._client.post("/v1/chat/completions", json=payload)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            log.error("LLM HTTP error: %s %s", e.response.status_code, e.response.text[:200])
            raise
        except httpx.ConnectError:
            log.error("Cannot connect to LLM at %s", self.config.base_url)
            raise

        choice = data["choices"][0]
        msg = choice["message"]

        tool_calls = None
        if msg.get("tool_calls"):
            tool_calls = []
            for tc in msg["tool_calls"]:
                tool_calls.append({
                    "id": tc.get("id", ""),
                    "function": {
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"],
                    },
                })

        return LLMResponse(
            content=msg.get("content") or "",
            tool_calls=tool_calls,
            finish_reason=choice.get("finish_reason", "stop"),
            usage=data.get("usage", {}),
        )

    async def chat_stream(
        self,
        messages: list[dict],
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """Stream tokens from llama.cpp. Yields content strings as they arrive."""
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": True,
        }

        try:
            async with self._client.stream(
                "POST", "/v1/chat/completions", json=payload
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk["choices"][0].get("delta", {})
                        token = delta.get("content")
                        if token:
                            yield token
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
        except httpx.HTTPStatusError as e:
            log.error("LLM stream HTTP error: %s", e.response.status_code)
            raise
        except httpx.ConnectError:
            log.error("Cannot connect to LLM at %s", self.config.base_url)
            raise

    async def close(self):
        await self._client.aclose()
