"""Multi-provider LLM client with fallback chain (BYOK)."""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

import httpx

from .. import config, constants

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(30.0, connect=10.0, read=120.0)


class LLMError(Exception):
    """Raised when all LLM providers fail."""


class LLMClient:
    """LLM client that tries providers in priority order.

    Usage:
        client = LLMClient()
        result = await client.generate("Analyze this profile...", system="You are a sales expert.")
    """

    def __init__(self) -> None:
        cfg = config.load_config()
        self.api_keys: dict[str, str] = cfg.get("api_keys", {})
        self.priority: list[str] = cfg.get("llm_priority", constants.DEFAULT_LLM_PRIORITY)
        self.models: dict[str, str] = {
            "gemini": cfg.get("gemini_model", constants.DEFAULT_GEMINI_MODEL),
            "claude": cfg.get("claude_model", constants.DEFAULT_CLAUDE_MODEL),
            "openai": cfg.get("openai_model", constants.DEFAULT_OPENAI_MODEL),
        }

    def _available_providers(self) -> list[str]:
        """Return providers that have API keys configured."""
        return [p for p in self.priority if self.api_keys.get(p)]

    async def generate(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate text using the first available LLM provider.

        Tries each provider in priority order. Returns the generated text.
        Raises LLMError if all providers fail.
        """
        providers = self._available_providers()
        if not providers:
            raise LLMError(
                "No LLM API keys configured.\n\n"
                "Add at least one API key to ~/.heylead/config.json:\n"
                '  "api_keys": {\n'
                '    "gemini": "YOUR_KEY_HERE"\n'
                "  }\n\n"
                "Get a free Gemini key at: https://aistudio.google.com/apikey"
            )

        errors = []
        for provider in providers:
            try:
                logger.debug(f"Trying LLM provider: {provider}")
                result = await self._call_provider(
                    provider, prompt, system, temperature, max_tokens
                )
                return result
            except Exception as e:
                logger.warning(f"LLM provider {provider} failed: {e}")
                errors.append(f"{provider}: {e}")

        raise LLMError(
            "All LLM providers failed:\n" + "\n".join(f"  - {e}" for e in errors)
        )

    async def _call_provider(
        self,
        provider: str,
        prompt: str,
        system: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        if provider == "gemini":
            return await self._call_gemini(prompt, system, temperature, max_tokens)
        elif provider == "claude":
            return await self._call_claude(prompt, system, temperature, max_tokens)
        elif provider == "openai":
            return await self._call_openai(prompt, system, temperature, max_tokens)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    # ──────────────────────────────────────
    # Gemini
    # ──────────────────────────────────────

    async def _call_gemini(
        self, prompt: str, system: str, temperature: float, max_tokens: int
    ) -> str:
        api_key = self.api_keys["gemini"]
        model = self.models["gemini"]
        url = f"{constants.GEMINI_API_URL}/{model}:generateContent?key={api_key}"

        body: dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=body, timeout=_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()

        candidates = data.get("candidates", [])
        if not candidates:
            raise LLMError("Gemini returned no candidates")

        parts = candidates[0].get("content", {}).get("parts", [])
        return parts[0].get("text", "") if parts else ""

    # ──────────────────────────────────────
    # Claude (Anthropic)
    # ──────────────────────────────────────

    async def _call_claude(
        self, prompt: str, system: str, temperature: float, max_tokens: int
    ) -> str:
        api_key = self.api_keys["claude"]
        model = self.models["claude"]

        headers = {
            "x-api-key": api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        body: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            body["system"] = system

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                constants.CLAUDE_API_URL, headers=headers, json=body, timeout=_TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()

        content = data.get("content", [])
        return content[0].get("text", "") if content else ""

    # ──────────────────────────────────────
    # OpenAI
    # ──────────────────────────────────────

    async def _call_openai(
        self, prompt: str, system: str, temperature: float, max_tokens: int
    ) -> str:
        api_key = self.api_keys["openai"]
        model = self.models["openai"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                constants.OPENAI_API_URL, headers=headers, json=body, timeout=_TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()

        choices = data.get("choices", [])
        return choices[0].get("message", {}).get("content", "") if choices else ""
