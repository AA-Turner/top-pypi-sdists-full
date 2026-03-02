"""Compaction strategy interface and implementations.

Provides a pluggable strategy for managing conversation context when it
grows too large.  Two built-in implementations:

* **LLMSummaryStrategy** – wraps the existing ``compact_messages_with_llm``
  behaviour (reactive, triggers at a % of the context limit).
* **ObservationalMemoryStrategy** – uses the ``emdash_observational_memory``
  package to incrementally observe / reflect and replace already-observed
  messages with compressed observations (continuous, Mastra-style triggers).

Select a strategy via the ``EMDASH_COMPACTION_STRATEGY`` env-var
(``llm_summary`` | ``observational_memory``).

Trigger model
-------------

Each strategy defines its own trigger semantics:

* **LLM Summary**: Single trigger — fires when estimated context tokens
  exceed ``threshold`` % of the model's context limit (default 80%).

* **Observational Memory** (Mastra-style, 4 triggers):

  1. **Buffer trigger** (``buffer_tokens``): At regular intervals (default
     20% of ``message_tokens``), run Observer in the background to
     pre-generate observation chunks without blocking the agent.
  2. **Activation trigger** (``message_tokens``, default 30k): When
     unobserved message tokens reach this threshold, activate buffered
     observations — remove observed raw messages, inject observations
     into the system prompt.
  3. **Reflection trigger** (``observation_tokens``, default 40k): When
     total observation tokens exceed this, Reflector condenses observations.
  4. **Safety block** (``block_after``, default 1.2x ``message_tokens``):
     If the background buffer cannot keep up, force synchronous observation
     to prevent context overflow.
"""

from __future__ import annotations

import asyncio
import os
import threading
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Optional, Protocol, runtime_checkable

from ..utils.logger import log

if TYPE_CHECKING:
    from .toolkit import AgentToolkit
    from .events import AgentEventEmitter

# Type for the pre-compaction memory flush callback.
# Receives (messages_to_summarize, emitter) and should persist important info.
PreCompactHook = Callable[
    [list[dict], Optional["AgentEventEmitter"]],
    None,
]


# ---------------------------------------------------------------------------
# Lightweight helpers (avoid importing runner package at module level)
# ---------------------------------------------------------------------------

def _estimate_context_tokens(
    messages: list[dict], system_prompt: Optional[str] = None
) -> int:
    """Estimate context window size in tokens (~4 chars/token).

    Duplicates the logic in ``runner.context.estimate_context_tokens``
    to avoid importing the runner package (which has heavy transitive deps).
    """
    total_chars = 0
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str):
            total_chars += len(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    total_chars += len(part["text"])
        total_chars += 16  # role/structure overhead
    if system_prompt:
        total_chars += len(system_prompt)
    return total_chars // 4


def _estimate_message_tokens(messages: list[dict]) -> int:
    """Estimate token count for raw messages only (no system prompt)."""
    return _estimate_context_tokens(messages)


def _compact_messages_with_llm(
    messages: list[dict],
    emitter: object,
    target_tokens: int,
    toolkit: object = None,
) -> list[dict]:
    """Lazy-import wrapper around ``runner.context.compact_messages_with_llm``."""
    # Import at call-time to avoid the heavy runner init at module-load.
    from .runner.context import compact_messages_with_llm
    return compact_messages_with_llm(messages, emitter, target_tokens, toolkit=toolkit)


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class CompactionResult:
    """Outcome of a compaction attempt.

    Attributes:
        messages: The (possibly compacted) message list.
        system_prompt: If not *None*, an enhanced system prompt that should
            replace the base prompt for the current LLM call.
        compacted: Whether any compaction actually happened.
    """

    messages: list[dict] = field(default_factory=list)
    system_prompt: Optional[str] = None
    compacted: bool = False


# ---------------------------------------------------------------------------
# Strategy protocol
# ---------------------------------------------------------------------------

@runtime_checkable
class CompactionStrategy(Protocol):
    """Strategy for managing conversation context growth.

    Different strategies use different trigger semantics:

    * **LLM Summary** uses the ``threshold`` parameter (% of context limit).
    * **Observational Memory** uses its own absolute token thresholds
      (``message_tokens``, ``observation_tokens``, etc.) and only falls
      back to the caller's ``threshold`` as a safety net.
    """

    def on_turn_complete(
        self,
        thread_id: str,
        new_messages: list[dict],
    ) -> None:
        """Called after each agent turn with the latest messages.

        Continuous strategies (observational memory) use this to feed
        new messages into the observation pipeline and trigger background
        buffering.  Reactive strategies (LLM summary) can ignore this.
        """
        ...

    def compact(
        self,
        thread_id: str,
        messages: list[dict],
        system_prompt: str,
        context_limit: int,
        threshold: float,
        toolkit: Optional["AgentToolkit"] = None,
        emitter: Optional["AgentEventEmitter"] = None,
    ) -> CompactionResult:
        """Check triggers and compact context if needed.

        Each strategy implements its own trigger logic:

        * **LLM Summary**: fires when ``estimated_tokens >= context_limit * threshold``
        * **Observational Memory**: fires when unobserved message tokens
          exceed ``message_tokens`` (default 30 000).  The ``threshold``
          and ``context_limit`` are only used as a last-resort safety net.

        Returns a :class:`CompactionResult` with possibly modified messages
        and/or system prompt.
        """
        ...


# ---------------------------------------------------------------------------
# Implementation: LLM Summary (current default)
# ---------------------------------------------------------------------------

class LLMSummaryStrategy:
    """Wraps the existing ``compact_messages_with_llm`` behaviour.

    This is the default strategy – purely reactive, triggering only when
    the estimated context tokens exceed *threshold* % of the context limit.
    ``on_turn_complete`` is a no-op.

    Supports an optional **pre-compact hook** (memory flush) that fires at
    a *soft* threshold before actual compaction.  This lets the agent persist
    important information to durable storage before compaction summarises
    (and potentially loses) message detail.  Inspired by OpenClaw's
    pre-compaction memory flush mechanism.

    Soft threshold = ``threshold * soft_threshold_ratio`` (default 0.9,
    so 0.72 when the compaction threshold is 0.8).
    """

    def __init__(
        self,
        *,
        soft_threshold_ratio: float = 0.9,
    ) -> None:
        self._pre_compact_hook: Optional[PreCompactHook] = None
        self._soft_threshold_ratio = soft_threshold_ratio
        # Tracks whether the flush already ran for the current compaction
        # cycle.  Reset after each actual compaction.
        self._flushed_this_cycle: bool = False

    # -- Hook wiring ----------------------------------------------------------

    def set_pre_compact_hook(self, hook: PreCompactHook) -> None:
        """Register a callback that runs once before each compaction.

        The hook receives ``(messages, emitter)`` and should persist any
        important information to durable storage (memory files, DB, etc.).
        """
        self._pre_compact_hook = hook

    # -- Protocol methods -----------------------------------------------------

    def on_turn_complete(
        self,
        thread_id: str,
        new_messages: list[dict],
    ) -> None:
        pass  # reactive strategy – nothing to do per-turn

    def compact(
        self,
        thread_id: str,
        messages: list[dict],
        system_prompt: str,
        context_limit: int,
        threshold: float,
        toolkit: Optional["AgentToolkit"] = None,
        emitter: Optional["AgentEventEmitter"] = None,
    ) -> CompactionResult:
        context_tokens = _estimate_context_tokens(messages, system_prompt)
        soft_threshold = threshold * self._soft_threshold_ratio

        # --- Soft threshold → memory flush (once per cycle) ------------------
        if (
            self._pre_compact_hook is not None
            and not self._flushed_this_cycle
            and context_tokens >= context_limit * soft_threshold
        ):
            log.info(
                "LLMSummaryStrategy: soft threshold reached (%s/%s tokens, "
                "%.0f%% >= %.0f%%) — running pre-compact memory flush",
                f"{context_tokens:,}",
                f"{context_limit:,}",
                context_tokens / context_limit * 100,
                soft_threshold * 100,
            )
            try:
                self._pre_compact_hook(messages, emitter)
            except Exception as exc:
                log.warning("Pre-compact hook failed (continuing): %s", exc)
            self._flushed_this_cycle = True

        # --- Hard threshold → actual compaction ------------------------------
        if context_tokens < context_limit * threshold:
            return CompactionResult(messages=messages, compacted=False)

        log.info(
            "LLMSummaryStrategy: context at %s/%s tokens (%s%%), compacting...",
            f"{context_tokens:,}",
            f"{context_limit:,}",
            f"{context_tokens / context_limit:.0%}",
        )

        compacted = _compact_messages_with_llm(
            messages,
            emitter=emitter,
            target_tokens=int(context_limit * 0.5),
            toolkit=toolkit,
        )

        # Reset flush tracking for the next cycle
        self._flushed_this_cycle = False

        return CompactionResult(messages=compacted, compacted=True)


# ---------------------------------------------------------------------------
# Implementation: Observational Memory (Mastra-style triggers)
# ---------------------------------------------------------------------------

@dataclass
class ObservationalMemoryConfig:
    """Configuration for Mastra-style observational memory triggers.

    Mirrors the triggering model described at
    https://mastra.ai/docs/memory/observational-memory:

    * ``message_tokens`` (default 30 000) – when unobserved message
      tokens reach this level, buffered observations activate and
      observed messages are removed from the context.
    * ``buffer_tokens`` (default 0.2) – fraction of ``message_tokens``
      at which a background Observer call runs to pre-generate
      observation chunks.  Set to ``0`` to disable background buffering
      (Observer then runs synchronously at ``message_tokens``).
    * ``buffer_activation`` (default 0.8) – aggressiveness of message
      removal on activation.  0.8 = keep ~20% of message history.
    * ``block_after`` (default 1.2) – safety multiplier.  If unobserved
      tokens exceed ``message_tokens * block_after``, a synchronous
      observation is forced even when buffering is enabled.
    * ``observation_tokens`` (default 40 000) – when total observation
      tokens exceed this, the Reflector condenses them.
    """

    message_tokens: int = 30_000
    buffer_tokens: float = 0.2       # fraction of message_tokens (0 = sync-only)
    buffer_activation: float = 0.8   # how aggressively to remove messages
    block_after: float = 1.2         # safety multiplier
    observation_tokens: int = 40_000


class ObservationalMemoryStrategy:
    """Uses ``emdash_observational_memory`` with Mastra-style triggers.

    Unlike the LLM summary strategy this is *continuous*:

    1. **Background buffering** – ``on_turn_complete()`` tracks message
       tokens and runs background Observer calls at ``buffer_tokens``
       intervals to pre-generate observations without blocking the agent.

    2. **Activation** – ``compact()`` checks if message tokens have
       reached ``message_tokens``.  When they have and buffered/existing
       observations are ready, it activates: observed messages are removed,
       observations are injected into the system prompt.

    3. **Reflection** – if observation tokens exceed ``observation_tokens``,
       the Reflector condenses them (happens inside ``process_turn``).

    4. **Safety block** – if message tokens exceed
       ``message_tokens * block_after``, a synchronous observation is
       forced (the ``blockAfter`` safety valve from Mastra).

    Falls back to ``LLMSummaryStrategy`` when no observations have been
    extracted yet (cold start) and context is critically full.
    """

    def __init__(
        self,
        memory: object,
        thread_id: str = "default",
        config: Optional[ObservationalMemoryConfig] = None,
    ):
        self._memory = memory
        self._default_thread_id = thread_id
        self._config = config or ObservationalMemoryConfig()
        self._fallback = LLMSummaryStrategy()

        # Background buffering state
        self._tokens_since_last_buffer: int = 0
        self._buffer_interval: int = (
            int(self._config.message_tokens * self._config.buffer_tokens)
            if self._config.buffer_tokens > 0
            else 0
        )
        # Lock for thread safety on buffering state
        self._lock = threading.Lock()
        # Track whether a background observation is in flight
        self._buffer_in_flight = False

    # ----- on_turn_complete: background buffering + safety block -----

    def on_turn_complete(
        self,
        thread_id: str,
        new_messages: list[dict],
    ) -> None:
        """Feed new messages and trigger background buffering if interval reached.

        Also enforces the ``block_after`` safety threshold: if unobserved
        message tokens exceed ``message_tokens * block_after``, a synchronous
        observation is forced to prevent context blow-up.
        """
        if not new_messages:
            return

        tid = thread_id or self._default_thread_id

        # Estimate tokens in the new messages
        new_tokens = _estimate_message_tokens(new_messages)

        with self._lock:
            self._tokens_since_last_buffer += new_tokens

        # --- Safety block: force sync observation if way over threshold ---
        block_threshold = int(self._config.message_tokens * self._config.block_after)
        status = self._memory.get_status(tid)
        unobserved_tokens = status.get("unobserved_tokens", 0) + new_tokens

        if unobserved_tokens >= block_threshold:
            log.warning(
                "ObservationalMemory safety block: %s unobserved tokens >= "
                "%s (block_after=%s). Forcing synchronous observation.",
                f"{unobserved_tokens:,}",
                f"{block_threshold:,}",
                self._config.block_after,
            )
            _run_sync(self._memory.process_turn(tid, new_messages))
            with self._lock:
                self._tokens_since_last_buffer = 0
            return

        # --- Background buffering: trigger at buffer_interval ---
        should_buffer = False
        with self._lock:
            if (
                self._buffer_interval > 0
                and self._tokens_since_last_buffer >= self._buffer_interval
                and not self._buffer_in_flight
            ):
                should_buffer = True
                self._buffer_in_flight = True
                self._tokens_since_last_buffer = 0

        if should_buffer:
            log.debug(
                "ObservationalMemory: buffer interval reached (%s tokens), "
                "running background observation",
                self._buffer_interval,
            )
            self._run_background(tid, new_messages)
        else:
            # Still ingest messages even if not observing yet
            _run_sync(self._memory.process_turn(tid, new_messages))

    # ----- compact: activation trigger -----

    def compact(
        self,
        thread_id: str,
        messages: list[dict],
        system_prompt: str,
        context_limit: int,
        threshold: float,
        toolkit: Optional["AgentToolkit"] = None,
        emitter: Optional["AgentEventEmitter"] = None,
    ) -> CompactionResult:
        """Check Mastra-style triggers and activate if message threshold is reached.

        Trigger logic (in order of priority):

        1. If unobserved message tokens < ``message_tokens`` — **no activation**,
           but still enhance system prompt with any existing observations.
        2. If unobserved message tokens >= ``message_tokens`` AND observations
           exist — **activate**: remove observed messages, inject observations.
        3. If unobserved message tokens >= ``message_tokens`` but no observations
           — **cold-start fallback**: delegate to LLM summary strategy.
        4. Context-limit safety net: if full context exceeds
           ``context_limit * threshold`` and observations exist, activate
           even if ``message_tokens`` hasn't been reached yet.
        """
        tid = thread_id or self._default_thread_id
        msg_tokens = _estimate_message_tokens(messages)

        # Get current observation state
        obs_context = self._memory.get_prompt_context(tid)
        has_observations = bool(obs_context)

        # Primary trigger: absolute message_tokens threshold
        message_threshold_reached = msg_tokens >= self._config.message_tokens

        # Safety-net trigger: context-limit % (uses the caller's threshold)
        full_tokens = _estimate_context_tokens(messages, system_prompt)
        context_safety_reached = full_tokens >= context_limit * threshold

        needs_activation = message_threshold_reached or context_safety_reached

        if not needs_activation:
            # Below all thresholds — just enhance system prompt if observations exist
            if has_observations:
                return CompactionResult(
                    messages=messages,
                    system_prompt=f"{system_prompt}\n\n{obs_context}",
                    compacted=False,
                )
            return CompactionResult(messages=messages, compacted=False)

        # ---- Activation needed ----

        if not has_observations:
            # Cold start — no observations yet, fall back to LLM summary
            trigger = (
                f"message_tokens ({msg_tokens:,} >= {self._config.message_tokens:,})"
                if message_threshold_reached
                else f"context_safety ({full_tokens:,} >= {int(context_limit * threshold):,})"
            )
            log.info(
                "ObservationalMemoryStrategy: activation needed (%s) but no "
                "observations yet — falling back to LLM summary",
                trigger,
            )
            return self._fallback.compact(
                thread_id=tid,
                messages=messages,
                system_prompt=system_prompt,
                context_limit=context_limit,
                threshold=threshold,
                toolkit=toolkit,
                emitter=emitter,
            )

        trigger_reason = (
            f"message_tokens ({msg_tokens:,} >= {self._config.message_tokens:,})"
            if message_threshold_reached
            else f"context_safety ({full_tokens:,} >= {int(context_limit * threshold):,})"
        )
        log.info(
            "ObservationalMemoryStrategy: activating observations "
            "(trigger: %s)",
            trigger_reason,
        )

        if emitter:
            emitter.emit_thinking(
                f"Activating observational memory ({trigger_reason})..."
            )

        # Filter out already-observed messages
        filtered = self._memory.filter_observed_messages(tid, messages)

        # Enforce buffer_activation — keep only (1 - activation) of message
        # history after the first message (original request).
        # activation=0.8 → keep 20% of filtered messages (aggressive)
        # activation=0.5 → keep 50% (moderate)
        if self._config.buffer_activation > 0 and len(filtered) > 2:
            keep_ratio = 1.0 - self._config.buffer_activation
            keep_count = max(2, int(len(filtered) * keep_ratio))
            first_msg = filtered[0]
            recent_msgs = filtered[-keep_count + 1:]
            filtered = [first_msg] + recent_msgs

        # Keep first message (original request) even if observed
        first_msg = messages[0] if messages else None
        if first_msg and first_msg not in filtered:
            filtered = [first_msg] + filtered

        # Inject continuation hint if observations replaced messages
        if len(filtered) < len(messages):
            hint = {
                "role": "user",
                "content": (
                    "<system-reminder>\n"
                    "This message is not from the user. The conversation history "
                    "grew too long and was compressed into the observations in "
                    "the system prompt. Please continue from where the "
                    "observations left off. Do not refer to your 'memory "
                    "observations' directly — just use the knowledge naturally "
                    "as if you remember the conversation.\n"
                    "</system-reminder>"
                ),
            }
            # Insert hint after first message
            if first_msg and len(filtered) > 0 and filtered[0] is first_msg:
                filtered = [first_msg, hint] + filtered[1:]
            else:
                filtered = [hint] + filtered

        # Reset file tracking so LLM can re-read files
        if toolkit:
            toolkit.partial_reset_for_compaction()
            log.info("Cleared file tracking after observational memory activation")

        enhanced_prompt = f"{system_prompt}\n\n{obs_context}"

        return CompactionResult(
            messages=filtered,
            system_prompt=enhanced_prompt,
            compacted=True,
        )

    # ----- Internal helpers -----

    def _run_background(self, thread_id: str, messages: list[dict]) -> None:
        """Run observation in a background thread to avoid blocking the agent."""

        def _bg():
            try:
                asyncio.run(self._memory.process_turn(thread_id, messages))
                log.debug("Background observation completed for thread %s", thread_id)
            except Exception as exc:
                log.warning("Background observation failed: %s", exc)
            finally:
                with self._lock:
                    self._buffer_in_flight = False

        t = threading.Thread(target=_bg, daemon=True)
        t.start()


# ---------------------------------------------------------------------------
# Async helper
# ---------------------------------------------------------------------------

def _run_sync(coro: object) -> object:
    """Run an async coroutine synchronously."""
    try:
        loop = asyncio.get_running_loop()
        return loop.create_task(coro)
    except RuntimeError:
        return asyncio.run(coro)


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def get_compaction_strategy(
    thread_id: str = "default",
) -> CompactionStrategy:
    """Create a compaction strategy based on ``EMDASH_COMPACTION_STRATEGY``.

    Values:
        ``llm_summary`` (default) – reactive LLM-based summarisation.
        ``observational_memory`` – continuous observation / reflection
        with Mastra-style multi-threshold triggers.
    """
    strategy_name = os.getenv("EMDASH_COMPACTION_STRATEGY", "llm_summary")

    if strategy_name == "observational_memory":
        try:
            from emdash_observational_memory import ObservationalMemory
            from emdash_observational_memory.config import get_config

            memory = ObservationalMemory(get_config())

            # Only the two core thresholds are env-configurable.
            # buffer_tokens, buffer_activation, block_after use sensible
            # defaults derived from message_tokens (overridable via code).
            config = ObservationalMemoryConfig(
                message_tokens=int(os.getenv(
                    "EMDASH_OM_MESSAGE_TOKENS", "30000"
                )),
                observation_tokens=int(os.getenv(
                    "EMDASH_OM_OBSERVATION_TOKENS", "40000"
                )),
            )

            log.info(
                "Using ObservationalMemoryStrategy "
                "(message_tokens=%s, observation_tokens=%s)",
                config.message_tokens,
                config.observation_tokens,
            )
            return ObservationalMemoryStrategy(memory, thread_id, config)
        except ImportError:
            log.warning(
                "emdash_observational_memory not installed – "
                "falling back to LLMSummaryStrategy"
            )
            return LLMSummaryStrategy()

    return LLMSummaryStrategy()
