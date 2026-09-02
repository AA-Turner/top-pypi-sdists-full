"""Build a ready-to-use ObservationalMemory from an AppContext.

Returns ``None`` (not an instance) when the feature is off for any reason —
kill switch, non-admin toggle, ephemeral conversation, anonymous user. This
lets the caller use the returned value as a boolean gate::

    om = build_observational_memory(ctx, conversation_id)
    if om is None:
        return  # memory disabled

The default model is ``MATRX_OM_DEFAULT_MODEL`` from the environment, or
``gemini-2.5-flash`` as a final fallback. Per-conversation overrides
come through ``ctx.memory_model``.
"""
from __future__ import annotations

import logging
from typing import Any

from .llm_adapter import MemoryLLMAdapter
from .observational_memory import ObservationalMemory
from .storage_db import DbObservationalMemoryStorage
from .token_counter import count_tokens as _count_tokens
from .types import (
    MemoryScope,
    ModelConfig,
    ObservationalMemoryConfig,
    ObservationConfig,
    ReflectionConfig,
)

logger = logging.getLogger(__name__)


# Default observational-memory model when ctx carries no per-conversation
# override. A code-reviewed constant, not an env var. (Was MATRX_OM_DEFAULT_MODEL.)
_DEFAULT_MODEL = "gemini-2.5-flash"

# ── KILL SWITCH (code-reviewed, NOT an env var) ──────────────────────────
# Emergency disable of Observational Memory for ALL conversations. Default
# False (OM on). Flip here and ship via git if OM must be turned off fast.
# (Was MATRX_OM_KILL_SWITCH.) Tracked in /docs/ENV_FLAG_ERADICATION.md.
OBSERVATIONAL_MEMORY_KILL_SWITCH: bool = False


def _kill_switch_on() -> bool:
    return OBSERVATIONAL_MEMORY_KILL_SWITCH


def _resolve_scope(raw: Any) -> MemoryScope:
    if isinstance(raw, MemoryScope):
        return raw
    try:
        return MemoryScope(str(raw or "thread"))
    except Exception:
        return MemoryScope.THREAD


def _make_token_counter():
    # Wraps the memory package's own tiktoken-with-fallback counter. Returns
    # a plain ``(str) -> int`` to match the OM contract.
    def _count(text: str) -> int:
        try:
            return _count_tokens(text or "")
        except Exception:
            return max(1, len(text or "") // 4)

    return _count


def build_observational_memory(ctx: Any, conversation_id: str) -> ObservationalMemory | None:
    """Return a configured OM orchestrator, or ``None`` if memory is off."""
    if not getattr(ctx, "memory_enabled", False):
        return None
    if not getattr(ctx, "store", True):
        logger.debug("OM disabled: ctx.store=False (ephemeral conversation)")
        return None
    user_id = str(getattr(ctx, "user_id", "") or "")
    if not user_id:
        logger.debug("OM disabled: anonymous or unauthenticated user")
        return None
    if not conversation_id:
        logger.debug("OM disabled: no conversation_id")
        return None
    if _kill_switch_on():
        logger.info("OM kill switch engaged (memory.factory.OBSERVATIONAL_MEMORY_KILL_SWITCH)")
        return None

    model = str(getattr(ctx, "memory_model", None) or _DEFAULT_MODEL)
    scope = _resolve_scope(getattr(ctx, "memory_scope", "thread"))

    observer_model = ModelConfig(
        model=model,
        temperature=0.3,
        max_tokens=16_000,
    )
    reflector_model = ModelConfig(
        model=model,
        temperature=0.0,
        max_tokens=16_000,
    )
    config = ObservationalMemoryConfig(
        scope=scope,
        observation=ObservationConfig(
            token_threshold=30_000,
            model=observer_model,
            buffer_tokens=0.2,
            block_after=1.2,
        ),
        reflection=ReflectionConfig(
            token_threshold=40_000,
            model=reflector_model,
            buffer_activation=0.5,
        ),
    )

    adapter = MemoryLLMAdapter(ctx=ctx, conversation_id=conversation_id)

    try:
        storage = DbObservationalMemoryStorage()
    except Exception as exc:
        logger.warning("OM storage init failed, memory disabled for this turn: %s", exc)
        return None

    om = ObservationalMemory(
        config=config,
        storage=storage,
        count_tokens_fn=_make_token_counter(),
        llm_call_fn=adapter,
    )
    # Stash the adapter so the caller can bind the record id once known.
    om._matrx_adapter = adapter  # type: ignore[attr-defined]
    return om
