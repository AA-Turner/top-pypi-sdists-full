"""Fallback chain wrapper for AgentLLM.

Wraps multiple `AgentLLM` instances and tries them in priority order, falling
through to the next on transient errors (429, 5xx, timeout, quota exhaustion).

Designed for Jai's preferred chain:
    Primary: Copilot (claude-sonnet-4.6)
    Free-tier heavy: NVIDIA NIM (nemotron-3-super-120b)
    Fallbacks: Gemini 3.1 Pro Preview → Flash Lite → Gemma 4 31B
                → Kimi K2.5 → MiniMax M2.5 → GLM5

Usage:
    from cvc.agent.fallback_chain import FallbackLLM, ChainSpec
    llm = FallbackLLM([
        ChainSpec("github", "claude-sonnet-4.6", api_key=""),
        ChainSpec("nvidia", "nvidia/nemotron-3-super-120b-instruct", api_key=os.environ["NVIDIA_API_KEY"]),
        ChainSpec("google", "gemini-3.1-pro-preview", api_key=os.environ["GOOGLE_API_KEY"]),
    ])
    resp = await llm.chat(messages, tools, temperature=0.7, max_tokens=4096)
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, AsyncIterator, List, Optional

import httpx

from cvc.agent.llm import AgentLLM, LLMResponse, StreamEvent, RetriesExhaustedError

logger = logging.getLogger(__name__)


# ── Error classification ──────────────────────────────────────────────

# HTTP codes that indicate "try the next provider" vs. real failure
_FALLBACK_HTTP_CODES = {408, 429, 500, 502, 503, 504}


def _is_fallbackable(exc: BaseException) -> bool:
    """Should we move to the next chain entry on this error?"""
    if isinstance(exc, (RetriesExhaustedError, httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in _FALLBACK_HTTP_CODES
    msg = str(exc).lower()
    fallback_markers = (
        "rate limit", "quota", "exhausted", "overloaded",
        "service unavailable", "timeout", "timed out",
    )
    return any(m in msg for m in fallback_markers)


# ── Chain spec ────────────────────────────────────────────────────────

@dataclass
class ChainSpec:
    """One link in the fallback chain."""
    provider: str
    model: str
    api_key: str = ""
    base_url: str = ""
    no_think: bool = False
    label: str = ""

    def display(self) -> str:
        return self.label or f"{self.provider}/{self.model}"


# ── FallbackLLM wrapper ───────────────────────────────────────────────

class FallbackLLM:
    """AgentLLM-compatible wrapper that fails over through a list of specs.

    Lazy-instantiates each AgentLLM only when first needed, so chains with
    missing API keys don't blow up at construction.
    """

    def __init__(self, specs: List[ChainSpec]) -> None:
        if not specs:
            raise ValueError("FallbackLLM requires at least one ChainSpec.")
        self._specs = specs
        self._instances: List[Optional[AgentLLM]] = [None] * len(specs)

        # Mirror primary's identity so callers reading `.provider` / `.model` see
        # the active head of the chain (updated as we rotate).
        self._active_idx = 0

    # ── Identity passthroughs ────────────────────────────────────────
    @property
    def provider(self) -> str:
        return self._specs[self._active_idx].provider

    @property
    def model(self) -> str:
        return self._specs[self._active_idx].model

    @property
    def specs(self) -> List[ChainSpec]:
        return list(self._specs)

    # ── Lazy instance access ─────────────────────────────────────────
    def _get(self, idx: int) -> AgentLLM:
        inst = self._instances[idx]
        if inst is None:
            spec = self._specs[idx]
            inst = AgentLLM(
                provider=spec.provider,
                api_key=spec.api_key,
                model=spec.model,
                base_url=spec.base_url,
                no_think=spec.no_think,
            )
            self._instances[idx] = inst
        return inst

    # ── Core chat with fallback ──────────────────────────────────────
    async def chat(self, messages: list[dict], tools: list[dict],
                   temperature: float, max_tokens: int) -> LLMResponse:
        last_exc: Optional[BaseException] = None
        for idx in range(len(self._specs)):
            spec = self._specs[idx]
            try:
                llm = self._get(idx)
            except Exception as exc:  # noqa: BLE001
                logger.warning("FallbackLLM: skipping %s (init failed: %s)", spec.display(), exc)
                last_exc = exc
                continue
            try:
                resp = await llm.chat(messages, tools, temperature, max_tokens)
                self._active_idx = idx
                if idx > 0:
                    logger.info("FallbackLLM: succeeded on fallback #%d (%s)", idx, spec.display())
                return resp
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if _is_fallbackable(exc) and idx < len(self._specs) - 1:
                    logger.warning("FallbackLLM: %s failed (%s) — falling through", spec.display(), exc)
                    continue
                # Non-fallbackable or last link → propagate
                raise
        # All chain links rejected at init time
        raise RuntimeError(f"FallbackLLM: all chain links failed. Last error: {last_exc}")

    # ── Streaming with fallback ──────────────────────────────────────
    async def stream_chat(self, messages: list[dict], tools: list[dict],
                          temperature: float, max_tokens: int,
                          thinking_level: str = "low") -> AsyncIterator[StreamEvent]:
        # For streaming, we can only fail over BEFORE first token. Once a token
        # has flushed to the caller, switching mid-stream would corrupt UX.
        last_exc: Optional[BaseException] = None
        for idx in range(len(self._specs)):
            spec = self._specs[idx]
            try:
                llm = self._get(idx)
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                continue

            try:
                stream = llm.stream_chat(messages, tools, temperature, max_tokens, thinking_level=thinking_level)
                first = await stream.__anext__()
            except StopAsyncIteration:
                # Empty stream — try next
                last_exc = RuntimeError(f"{spec.display()} returned empty stream")
                continue
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if _is_fallbackable(exc) and idx < len(self._specs) - 1:
                    logger.warning("FallbackLLM[stream]: %s failed (%s) — falling through", spec.display(), exc)
                    continue
                raise

            # First token landed — commit to this provider for the rest of the stream
            self._active_idx = idx
            if idx > 0:
                logger.info("FallbackLLM[stream]: succeeded on fallback #%d (%s)", idx, spec.display())
            yield first
            async for event in stream:
                yield event
            return
        raise RuntimeError(f"FallbackLLM[stream]: all chain links failed. Last: {last_exc}")

    # ── Compatibility helpers ────────────────────────────────────────
    async def warm_connection(self) -> None:
        try:
            await self._get(0).warm_connection()
        except Exception as exc:  # noqa: BLE001
            logger.debug("FallbackLLM: primary warm failed: %s", exc)


# ── Default chain builders ────────────────────────────────────────────

def build_default_chain(*,
                         copilot: bool = True,
                         nvidia_api_key: str = "",
                         google_api_key: str = "") -> List[ChainSpec]:
    """Build Jai's preferred fallback chain.

    Order:
        1. Copilot (claude-sonnet-4.6) — primary, zero-cost via OAuth pool
        2. NVIDIA NIM Nemotron 3 Super 120B — free heavy-workload tier
        3. Gemini 3.1 Pro Preview — paid fallback
        4. Gemini 3.1 Flash Lite — paid fast fallback
        5. Gemma 4 31B (via Google) — final fallback
    """
    chain: List[ChainSpec] = []

    if copilot:
        chain.append(ChainSpec("github", "claude-sonnet-4.6", label="copilot/sonnet-4.6"))

    if nvidia_api_key:
        chain.append(ChainSpec(
            "nvidia", "nvidia/nemotron-3-super-120b-instruct",
            api_key=nvidia_api_key, label="nvidia/nemotron-3-super-120b",
        ))

    if google_api_key:
        chain.extend([
            ChainSpec("google", "gemini-3.1-pro-preview", api_key=google_api_key, label="google/gemini-3.1-pro"),
            ChainSpec("google", "gemini-3-flash-preview", api_key=google_api_key, label="google/gemini-3-flash"),
        ])

    if not chain:
        raise ValueError("build_default_chain: no providers configured (set NVIDIA_API_KEY / GOOGLE_API_KEY or enable copilot).")

    return chain


def build_chain_from_env() -> "FallbackLLM":
    """Build a FallbackLLM from CVC env vars."""
    import os
    specs = build_default_chain(
        copilot=os.environ.get("CVC_COPILOT_DISABLE", "").lower() not in ("1", "true", "yes"),
        nvidia_api_key=os.environ.get("NVIDIA_API_KEY", ""),
        google_api_key=os.environ.get("GOOGLE_API_KEY", "") or os.environ.get("GEMINI_API_KEY", ""),
    )
    return FallbackLLM(specs)
