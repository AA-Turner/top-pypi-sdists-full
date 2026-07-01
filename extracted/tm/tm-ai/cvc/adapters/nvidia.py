"""cvc.adapters.nvidia — NVIDIA NIM adapter (OpenAI-compatible).

Free-tier hosted inference for Nemotron 3 Super 120B (262K ctx), Kimi K2,
MiniMax M2, and other models served via https://integrate.api.nvidia.com.

Wire format identical to OpenAI Chat Completions, so we subclass OpenAIAdapter
and only override the base_url + default model.
"""

from __future__ import annotations

import httpx

from cvc.adapters.openai import OpenAIAdapter

NVIDIA_API_BASE = "https://integrate.api.nvidia.com"
DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-instruct"


class NvidiaAdapter(OpenAIAdapter):
    """OpenAI-compatible adapter pointed at NVIDIA NIM endpoints."""

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL) -> None:
        # Skip OpenAIAdapter.__init__ — its base_url is hardcoded to OpenAI.
        # Mirror its initialisation but point at NVIDIA NIM.
        self._api_key = api_key
        self._model = model
        self._client = httpx.AsyncClient(
            base_url=NVIDIA_API_BASE,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )


__all__ = ["NvidiaAdapter", "NVIDIA_API_BASE", "DEFAULT_MODEL"]
