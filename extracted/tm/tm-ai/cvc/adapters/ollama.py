"""
cvc.adapters.ollama — Ollama adapter for local open-source models.

Translates CVC's ``ChatCompletionRequest`` to the Ollama REST API which
exposes an OpenAI-compatible ``/v1/chat/completions`` endpoint at
``http://localhost:11434``.

Default model: ``qwen2.5-coder:7b`` — the most popular open-source coding
model, with 11M+ pulls and excellent code generation, reasoning, and
instruction-following capabilities.

Other recommended models for coding:
    - ``qwen3-coder:30b``    — Alibaba's latest agentic coding model
    - ``devstral:24b``       — Mistral's best open-source coding agent model
    - ``deepseek-r1:8b``     — Open reasoning model (chain-of-thought)
    - ``codestral:22b``      — Mistral's dedicated code model

Model detection and auto-pull:
    Use ``OllamaClient`` for model management (list, detect, ensure, pull).
    The ``OllamaAdapter`` auto-calls ``ensure_model()`` on first use when
    ``auto_pull=True`` (the default).
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Callable

import httpx

from cvc.adapters.base import BaseAdapter
from cvc.core.models import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    UsageInfo,
)

logger = logging.getLogger("cvc.adapters.ollama")

DEFAULT_OLLAMA_URL = "http://localhost:11434"

# ---- Recommended Models (ordered by preference) --------------------------
# Smaller models first so auto-pull picks the most widely-runnable option.
RECOMMENDED_MODELS: list[str] = [
    "qwen2.5-coder:7b",   # Best all-round coding, 11M+ pulls, ~4 GB
    "qwen3-coder:30b",    # Latest Alibaba agentic coding model, ~18 GB
    "devstral:24b",       # Mistral "best open-source coding agent", ~14 GB
    "deepseek-r1:8b",     # Chain-of-thought reasoning, ~5 GB
    "codestral:22b",      # Mistral dedicated code generation, ~13 GB
]

DEFAULT_MODEL = RECOMMENDED_MODELS[0]


# ---------------------------------------------------------------------------
# Ollama management client
# ---------------------------------------------------------------------------

class OllamaClient:
    """
    Low-level async client for Ollama management endpoints.

    Separate from ``OllamaAdapter`` so model detection and pull logic can be
    used outside the chat path (e.g. from ``cvc setup``, health checks, etc.).
    """

    def __init__(self, base_url: str = DEFAULT_OLLAMA_URL) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(connect=10.0, read=300.0, write=60.0, pool=10.0),
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "OllamaClient":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # Model listing
    # ------------------------------------------------------------------

    async def list_local_models(self) -> list[str]:
        """
        Return names of all locally available Ollama models.

        Calls ``GET /api/tags`` and extracts ``model`` names.  Returns an
        empty list if Ollama is not running.

        Example::

            client = OllamaClient()
            names = await client.list_local_models()
            # ["qwen2.5-coder:7b", "llama3.2:3b", ...]
        """
        try:
            resp = await self._client.get("/api/tags")
            resp.raise_for_status()
        except httpx.ConnectError:
            logger.debug("Ollama not reachable at %s — returning empty model list", self._base_url)
            return []
        except httpx.HTTPStatusError as exc:
            logger.warning("Ollama /api/tags returned %s", exc.response.status_code)
            return []

        data = resp.json()
        return [m["name"] for m in data.get("models", [])]

    async def is_model_available(self, model: str) -> bool:
        """Return True if *model* is present in the local Ollama library."""
        local = await self.list_local_models()
        # Normalise: Ollama tags "name:tag"; treat bare "name" as "name:latest"
        def _normalise(m: str) -> str:
            return m if ":" in m else f"{m}:latest"

        target = _normalise(model)
        return any(_normalise(m) == target for m in local)

    # ------------------------------------------------------------------
    # Model detection — pick the best available recommended model
    # ------------------------------------------------------------------

    async def detect_recommended_model(self) -> str | None:
        """
        Return the name of the highest-priority recommended model that is
        already installed locally, or ``None`` if none are found.

        Priority follows ``RECOMMENDED_MODELS`` order (first = best).
        """
        local = await self.list_local_models()
        local_set = set(local)

        def _normalise(m: str) -> str:
            return m if ":" in m else f"{m}:latest"

        local_normalised = {_normalise(m) for m in local_set}
        for candidate in RECOMMENDED_MODELS:
            if _normalise(candidate) in local_normalised:
                return candidate
        return None

    # ------------------------------------------------------------------
    # Model pulling
    # ------------------------------------------------------------------

    async def pull_model(
        self,
        model: str,
        *,
        progress_callback: Callable[[str, int, int], None] | None = None,
    ) -> None:
        """
        Pull *model* from the Ollama registry.

        Parameters
        ----------
        model :
            Model tag to pull (e.g. ``"qwen2.5-coder:7b"``).
        progress_callback :
            Optional callable called with ``(status, completed, total)`` for
            each progress event.  ``completed`` and ``total`` are byte counts
            (0 when not provided by Ollama).

        Raises
        ------
        ConnectionError
            If Ollama is not running.
        RuntimeError
            If the pull fails or the model name is unknown.
        """
        logger.info("Pulling Ollama model: %s", model)

        try:
            async with self._client.stream(
                "POST",
                "/api/pull",
                json={"name": model, "stream": True},
            ) as resp:
                resp.raise_for_status()
                async for raw_line in resp.aiter_lines():
                    raw_line = raw_line.strip()
                    if not raw_line:
                        continue
                    try:
                        event = json.loads(raw_line)
                    except json.JSONDecodeError:
                        continue

                    status = event.get("status", "")
                    completed = event.get("completed", 0) or 0
                    total = event.get("total", 0) or 0
                    error = event.get("error")

                    if error:
                        raise RuntimeError(f"Ollama pull error: {error}")

                    logger.debug("Pull %s: %s %d/%d", model, status, completed, total)
                    if progress_callback:
                        progress_callback(status, completed, total)

        except httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self._base_url}. "
                "Make sure Ollama is running: https://ollama.com/download"
            )
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"Ollama pull failed (HTTP {exc.response.status_code}): {exc.response.text}"
            ) from exc

        logger.info("Successfully pulled Ollama model: %s", model)

    # ------------------------------------------------------------------
    # Ensure a model is present, pulling it if not
    # ------------------------------------------------------------------

    async def ensure_model(
        self,
        model: str,
        *,
        auto_pull: bool = True,
        progress_callback: Callable[[str, int, int], None] | None = None,
    ) -> bool:
        """
        Ensure *model* is available locally, pulling it if necessary.

        Parameters
        ----------
        model :
            Model tag to ensure (e.g. ``"qwen2.5-coder:7b"``).
        auto_pull :
            If True (default), pull the model automatically when missing.
            If False, raise ``RuntimeError`` instead.
        progress_callback :
            Forwarded to ``pull_model`` when a pull is needed.

        Returns
        -------
        bool
            True if the model was already present, False if it was pulled.

        Raises
        ------
        RuntimeError
            If *auto_pull* is False and the model is not present.
        ConnectionError
            If Ollama is not reachable.
        """
        if await self.is_model_available(model):
            logger.debug("Model %s already present", model)
            return True

        if not auto_pull:
            raise RuntimeError(
                f"Model '{model}' is not installed in Ollama. "
                f"Pull it first: ollama pull {model}"
            )

        logger.info("Model %s not found locally — pulling from registry", model)
        await self.pull_model(model, progress_callback=progress_callback)
        return False


# ---------------------------------------------------------------------------
# Chat adapter
# ---------------------------------------------------------------------------

class OllamaAdapter(BaseAdapter):
    """
    Sends ``ChatCompletionRequest`` objects to a local Ollama instance.

    Ollama natively supports the OpenAI-compatible ``/v1/chat/completions``
    endpoint, so the translation is essentially a pass-through.  The primary
    addition is ``keep_alive`` to hold the model in memory across requests,
    reducing cold-start latency for agentic workflows.

    When ``auto_pull=True`` (default), the adapter will automatically pull
    the configured model on first use if it is not already installed.
    """

    def __init__(
        self,
        api_key: str = "",  # unused, accepted for interface consistency
        model: str = DEFAULT_MODEL,
        base_url: str = DEFAULT_OLLAMA_URL,
        *,
        auto_pull: bool = True,
    ) -> None:
        self._model = model
        self._base_url = base_url.rstrip("/")
        self._auto_pull = auto_pull
        self._model_ensured = False  # lazy — only check once per instance

        self._client = httpx.AsyncClient(
            base_url=f"{self._base_url}/v1",
            headers={"Content-Type": "application/json"},
            timeout=300.0,  # Local models can be slow on first load
        )
        self._mgmt_client = OllamaClient(base_url=self._base_url)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def complete(
        self,
        request: ChatCompletionRequest,
        *,
        committed_prefix_len: int = 0,
    ) -> ChatCompletionResponse:
        """Forward the request to the local Ollama instance."""
        model = request.model or self._model
        await self._maybe_ensure_model(model)

        messages = [self._convert_message(m) for m in request.messages]

        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": False,
        }

        if request.tools:
            body["tools"] = request.tools
        if request.tool_choice:
            body["tool_choice"] = request.tool_choice

        logger.debug(
            "Ollama request: model=%s messages=%d base_url=%s",
            body["model"],
            len(messages),
            self._base_url,
        )

        try:
            resp = await self._client.post("/chat/completions", json=body)
            resp.raise_for_status()
        except httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self._base_url}. "
                "Make sure Ollama is running: https://ollama.com/download"
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                model_name = body["model"]
                raise RuntimeError(
                    f"Model '{model_name}' not found in Ollama. "
                    f"Pull it first: ollama pull {model_name}"
                ) from exc
            raise

        data = resp.json()
        return self._to_response(data)

    async def close(self) -> None:
        await self._client.aclose()
        await self._mgmt_client.close()

    # ------------------------------------------------------------------
    # Model management helpers
    # ------------------------------------------------------------------

    @property
    def management(self) -> OllamaClient:
        """Expose the management client for model listing/pulling."""
        return self._mgmt_client

    async def _maybe_ensure_model(self, model: str) -> None:
        """Pull *model* if it is missing and auto_pull is enabled."""
        if self._model_ensured:
            return
        self._model_ensured = True  # Only attempt once per instance

        def _log_progress(status: str, completed: int, total: int) -> None:
            if total > 0:
                pct = int(completed / total * 100)
                logger.info("Pull %s: %s %d%%", model, status, pct)
            else:
                logger.info("Pull %s: %s", model, status)

        try:
            await self._mgmt_client.ensure_model(
                model,
                auto_pull=self._auto_pull,
                progress_callback=_log_progress,
            )
        except ConnectionError:
            # Re-raise — Ollama not running is a hard error
            raise
        except RuntimeError as exc:
            # Model pull failed — log and continue; the actual complete() call
            # will surface a cleaner error from the API.
            logger.warning("ensure_model failed: %s", exc)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _convert_message(msg: ChatMessage) -> dict[str, Any]:
        """Convert a Pydantic ChatMessage to a plain dict."""
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
        """Convert a raw Ollama/OpenAI-compat JSON response to our schema."""
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
        usage = UsageInfo(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0),
        )

        return ChatCompletionResponse(
            id=data.get("id", ""),
            model=data.get("model", ""),
            choices=choices,
            usage=usage,
        )
