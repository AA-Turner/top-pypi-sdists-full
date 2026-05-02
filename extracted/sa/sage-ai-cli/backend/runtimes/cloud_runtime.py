"""Legacy cloud runtime stub — Pollinations-backed inference has been removed.

Use :class:`OllamaRuntime` or GGUF runtimes instead.
"""

from __future__ import annotations

from ..schemas import ChatMessage
from .base import RuntimeAdapter


class CloudRuntime(RuntimeAdapter):
    """Disabled — cloud inference via Pollinations is no longer supported."""

    def load(self, model_path: str, threads: int | None = None) -> None:
        raise RuntimeError(
            "Pollinations cloud inference has been removed from Sage. "
            "Use an Ollama model (ollama:<name>) or register a local GGUF model."
        )

    def chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ) -> str:
        raise RuntimeError("Cloud runtime is disabled.")

    def stream_chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ):
        raise RuntimeError("Cloud runtime is disabled.")
