"""Build a ready-to-use ObservationalMemory from an AppContext.

Returns ``None`` (not an instance) when the feature is off for any reason —
kill switch, non-admin toggle, ephemeral conversation, anonymous user. This
lets the caller use the returned value as a boolean gate::

    om = build_observational_memory(ctx, conversation_id)
    if om is None:
        return  # memory disabled

The Observer and Reflector run on their mandates' Holders (memory.observer /
memory.reflector) — model, instructions, sampling. ``ctx.run.memory_model`` is a
run-scope override only when a request explicitly names one.
"""
from __future__ import annotations

import logging
from typing import Any

from matrx_ai.code_call_mandate_keys import MEMORY_OBSERVER_MANDATE, MEMORY_REFLECTOR_MANDATE

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
            from matrx_ai.config.context_trim import estimate_budget_tokens

            return max(1, estimate_budget_tokens(len(text or ""), "prose"))

    return _count


def build_observational_memory(ctx: Any, conversation_id: str) -> ObservationalMemory | None:
    """Return a configured OM orchestrator, or ``None`` if memory is off."""
    run = ctx.run
    if not run.memory_enabled:
        return None
    # What the REAL send carries decides whether the model sees memory: a dry run (store=False so it
    # writes nothing) answers as the real run would, so the preview shows the observations (PB-07).
    from matrx_ai.config.person_context import wire_store

    if not wire_store(ctx):
        logger.debug("OM disabled: ephemeral conversation (store=False)")
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

    # An explicitly requested model is run scope; otherwise the Holder decides.
    override = str(run.memory_model or "").strip() or None
    # Its chosen class rides only with it (dropped loudly otherwise).
    from matrx_ai.graph_nodes.class_pin import node_class_pin

    override_class = node_class_pin(
        override, run.memory_offering_id, where="observational memory"
    )
    scope = _resolve_scope(run.memory_scope)

    observer_model = ModelConfig(
        mandate_key=MEMORY_OBSERVER_MANDATE, model=override, offering_id=override_class
    )
    reflector_model = ModelConfig(
        mandate_key=MEMORY_REFLECTOR_MANDATE, model=override, offering_id=override_class
    )
    config = ObservationalMemoryConfig(
        scope=scope,
        organization_id=str(getattr(ctx, "organization_id", "") or "") or None,
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
