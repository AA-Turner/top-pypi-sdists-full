"""Google Gemini provider — uses the free-tier REST API via httpx."""

from __future__ import annotations

import json
import time
from collections.abc import Iterator

import httpx

from ..config import SageConfig
from .base import Message, ModelInfo, ProviderBase
from .retry import (
    CircuitBreaker,
    RetryConfig,
    get_rate_limiter,
    get_retry_after,
    is_transient_error,
)

_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Models available on the Gemini free tier
_FREE_MODELS = [
    ModelInfo(
        id="gemini-2.0-flash",
        provider="gemini",
        name="Gemini 2.0 Flash",
        local=False,
        description="Fast, capable model for most coding tasks",
        pros="Free tier, fast, good code generation",
        cons="May struggle with complex architecture",
    ),
    ModelInfo(
        id="gemini-2.5-flash-preview-05-20",
        provider="gemini",
        name="Gemini 2.5 Flash Preview",
        local=False,
        description="Latest preview with improved reasoning",
        pros="Free tier, newest capabilities, better reasoning",
        cons="Preview (may be unstable), rate limited",
    ),
    ModelInfo(
        id="gemini-1.5-flash",
        provider="gemini",
        name="Gemini 1.5 Flash",
        local=False,
        description="Balanced model with long context",
        pros="Free tier, 1M token context, stable",
        cons="Older model, less capable than 2.0",
    ),
]


def _build_payload(
    messages: list[Message],
    temperature: float,
    max_tokens: int,
) -> dict:
    """Convert internal messages to Gemini API format."""
    system_parts: list[dict] = []
    contents: list[dict] = []

    for msg in messages:
        if msg.role == "system":
            system_parts.append({"text": msg.content})
            continue
        # Gemini uses "user" and "model" (not "assistant")
        role = "model" if msg.role == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg.content}]})

    # Gemini requires contents to start with a user turn.
    # If conversation starts with assistant (shouldn't normally), prepend empty user.
    if contents and contents[0]["role"] == "model":
        contents.insert(0, {"role": "user", "parts": [{"text": ""}]})

    payload: dict = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }
    if system_parts:
        payload["systemInstruction"] = {"parts": system_parts}
    return payload


def _extract_text(data: dict) -> str:
    """Pull generated text from a Gemini response chunk."""
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        return ""


class GeminiProvider(ProviderBase):
    """Gemini free-tier provider using the REST API with retry support."""

    name = "gemini"

    # Retry configuration for Gemini API
    _retry_config = RetryConfig(max_attempts=3, base_delay=1.0, max_delay=30.0)
    _circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60.0)

    def __init__(self, config: SageConfig) -> None:
        self._api_key = config.gemini_api_key()
        self._rate_limiter = get_rate_limiter("gemini", requests_per_minute=60)

    def is_available(self) -> bool:
        if not self._api_key:
            return False
        # Check circuit breaker
        if self._circuit_breaker.is_open():
            return False
        return True

    def list_models(self) -> list[ModelInfo]:
        if not self.is_available():
            return []
        return list(_FREE_MODELS)

    # ── Structured tool protocol (B5) ──────────────────────────────────

    def supports_tools(self) -> bool:
        # Gemini 1.5+ / 2.x reliably follow function-calling. We expose
        # the capability unconditionally so the engine can opt into
        # structured tools regardless of which Gemini model is selected.
        return True

    def format_tools(self, specs):
        """Convert sage's ToolSpec list to Gemini's function_declarations.

        Gemini wire format:
          {
            "function_declarations": [
              {"name": "READ",
               "description": "...",
               "parameters": {
                 "type": "object",
                 "properties": {"path": {"type": "string", ...}},
                 "required": ["path"]
               }},
              ...
            ]
          }
        """
        decls = []
        for spec in specs:
            decls.append({
                "name": spec.name,
                "description": spec.description,
                "parameters": {
                    "type": "object",
                    "properties": dict(spec.parameters),
                    "required": list(spec.required),
                },
            })
        return {"function_declarations": decls}

    def _make_request_with_retry(
        self,
        client: httpx.Client,
        url: str,
        payload: dict,
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        last_exception: Exception | None = None

        for attempt in range(self._retry_config.max_attempts):
            try:
                # Rate limiting
                if not self._rate_limiter.try_acquire():
                    self._rate_limiter.acquire(timeout=10.0)

                resp = client.post(url, json=payload)
                resp.raise_for_status()
                self._circuit_breaker.record_success()
                return resp

            except KeyboardInterrupt:
                raise
            except Exception as exc:
                last_exception = exc

                if not is_transient_error(exc):
                    # Permanent error, don't retry
                    raise

                self._circuit_breaker.record_failure()

                if attempt < self._retry_config.max_attempts - 1:
                    retry_after = get_retry_after(exc)
                    delay = self._retry_config.calculate_delay(attempt, retry_after)
                    time.sleep(delay)

        if last_exception:
            raise last_exception
        raise RuntimeError("Request failed without exception")

    def generate(
        self,
        messages: list[Message],
        model: str = "gemini-2.0-flash",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self._api_key:
            raise RuntimeError(
                "Gemini API key not configured. Run: sage config set api_keys.gemini YOUR_KEY"
            )

        if self._circuit_breaker.is_open():
            raise RuntimeError("Gemini API circuit breaker open. Service may be unavailable.")

        url = f"{_BASE_URL}/models/{model}:generateContent?key={self._api_key}"
        payload = _build_payload(messages, temperature, max_tokens)

        with httpx.Client(timeout=120) as client:
            resp = self._make_request_with_retry(client, url, payload)
            return _extract_text(resp.json())

    def stream(
        self,
        messages: list[Message],
        model: str = "gemini-2.0-flash",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        if not self._api_key:
            raise RuntimeError(
                "Gemini API key not configured. Run: sage config set api_keys.gemini YOUR_KEY"
            )

        if self._circuit_breaker.is_open():
            raise RuntimeError("Gemini API circuit breaker open. Service may be unavailable.")

        url = f"{_BASE_URL}/models/{model}:streamGenerateContent?alt=sse&key={self._api_key}"
        payload = _build_payload(messages, temperature, max_tokens)

        # Rate limiting before stream
        if not self._rate_limiter.try_acquire():
            self._rate_limiter.acquire(timeout=10.0)

        last_exception: Exception | None = None

        for attempt in range(self._retry_config.max_attempts):
            try:
                with httpx.Client(timeout=120) as client:
                    with client.stream("POST", url, json=payload) as resp:
                        resp.raise_for_status()
                        self._circuit_breaker.record_success()
                        for line in resp.iter_lines():
                            if not line.startswith("data: "):
                                continue
                            try:
                                chunk = json.loads(line[6:])
                            except json.JSONDecodeError:
                                continue
                            text = _extract_text(chunk)
                            if text:
                                yield text
                        return  # Success, exit retry loop

            except KeyboardInterrupt:
                raise
            except Exception as exc:
                last_exception = exc

                if not is_transient_error(exc):
                    raise

                self._circuit_breaker.record_failure()

                if attempt < self._retry_config.max_attempts - 1:
                    retry_after = get_retry_after(exc)
                    delay = self._retry_config.calculate_delay(attempt, retry_after)
                    time.sleep(delay)

        if last_exception:
            raise last_exception
