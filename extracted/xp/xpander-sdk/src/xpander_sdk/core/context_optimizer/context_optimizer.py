"""
Agno Context Optimizer for xpander.ai SDK.

4-layer context management pipeline:
  Layer 0 — headroom compaction: losslessly densify JSON tool results (in tool hook, zero cost).
  Layer 1 — Microcompaction: offload large tool outputs to workspace, keep preview (zero LLM cost).
  Layer 2 — Auto-compaction: LLM summarisation when approaching token ceiling.
  Layer 3 — Manual compaction: agent-triggered on-demand compression with focus hint.
  Emergency — Near-ceiling safety net at 88% capacity, bypasses circuit breaker.

Thresholds based on industry best practices for agentic context management.

Module layout (post-refactor):
  - ``constants.py``         — numeric thresholds, env-overridable knobs, rate-limit classifier
  - ``prompts.py``           — Layer 2 / Layer 3 / pre-retry prompt templates + builder
  - ``error_patterns.py``    — provider context-overflow detection + max-tokens parser
  - ``compact_retry_result.py`` — ``CompactRetryResult`` dataclass
  - ``helpers/secrets.py``   — secret redaction
  - ``helpers/xml_safety.py``— XML 1.0 safety helpers
  - ``helpers/tool_result.py``— ``ToolInvocationResult`` repr unwrapping
  - ``helpers/recent_actions.py`` — ``<recent_actions>`` block builder
  - ``helpers/chunking.py``  — Layer 2 message chunking
  - ``workspace_cache.py``   — Layer 1 in-memory cache + workspace write queue
  - ``structure_sketch.py``  — deterministic JSON shape line for Layer 1 previews
  - ``encryption.py``        — XOR stream cipher + key derivation
  - ``context_optimizer.py`` — ``XPanderContextOptimizer`` class itself
"""

import asyncio
import json
import random
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Type, Union

from pydantic import BaseModel

from loguru import logger

from agno.compression import CompressionManager
from agno.models.base import Model
from agno.models.message import Message
from agno.models.utils import get_model

from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.context_optimizer.action_ledger import (
    ActionLedger,
    attach_to_task,
    get_attached_ledger,
)
from xpander_sdk.core.context_optimizer.compact_retry_result import CompactRetryResult
from xpander_sdk.core.context_optimizer.completion_evidence import (
    detect_completion_evidence,
)
from xpander_sdk.core.context_optimizer.constants import (
    DEFAULT_CHUNKED_COMPACT_THRESHOLD_FRAC,
    DEFAULT_MAP_PHASE_MAX_CONCURRENCY,
    DEFAULT_MAX_CHUNK_INPUT_TOKENS,
    DYNAMIC_DISPATCH_META_TOOL,
    EMERGENCY_COMPACT_FRACTION,
    FINALIZE_MODE_ENABLED,
    INCLUDE_RECENT_ACTIONS,
    L1_ALWAYS_SKIP,
    L1_HEADROOM_BANDS,
    L1_XP_OFFLOAD_ELIGIBLE,
    LEDGER_ENABLED,
    PINNED_SKILL_MAX_CHARS,
    PINNED_SKILLS_MAX,
    SKILL_PIN_TOOL_NAMES,
    EMERGENCY_CONNECTIVITY_RETRY_BASE_DELAY,
    EMERGENCY_CONNECTIVITY_RETRY_MAX_ATTEMPTS,
    EMERGENCY_CONNECTIVITY_RETRY_MAX_DELAY,
    MAX_COMPACTIONS_PER_ARUN,
    MAX_COMPACTIONS_PER_TASK,
    MAX_CONSECUTIVE_COMPACT_FAILURES,
    MAX_PRE_RETRY_COMPACTIONS,
    MAX_STAGNANT_COMPACTIONS,
    MIN_TOKENS_FOR_PRE_RETRY_COMPACT,
    OFFLOAD_SUMMARY_MAX_CHARS,
    PENDING_SUMMARY_MAX_PASSES,
    PLAN_BLOCK_LABEL,
    PRE_RETRY_COMPACT_MAX_ATTEMPTS,
    PRE_RETRY_COMPACT_MAX_NONTIMEOUT_ATTEMPTS,
    PRE_RETRY_COMPACT_RETRY_BASE_DELAY,
    PRE_RETRY_COMPACT_RETRY_JITTER,
    PRE_RETRY_COMPACT_RETRY_MAX_DELAY,
    PROMPT_BUDGET_ENABLED,
    RECENT_ACTIONS_ARGS_HEAD,
    RECENT_ACTIONS_ARGS_TAIL,
    RECENT_ACTIONS_COUNT,
    RECENT_ACTIONS_RESULT_HEAD,
    RECENT_ACTIONS_RESULT_TAIL,
    SESSION_COMPACT_TIMEOUT,
    STAGNANT_COMPACTION_WARN_AT,
    TOKEN_FLOOR_PROGRESS_GUARD,
    _MAP_CHUNK_RETRY_ATTEMPTS,
    _MAP_CHUNK_RETRY_BASE_DELAY,
    _MAP_CHUNK_RETRY_JITTER,
    _env_float,
    _env_int,
    _is_connectivity_error,
    _is_rate_limit_error,
)
from xpander_sdk.exceptions.module_exception import ProviderUnreachableError
from xpander_sdk.core.context_optimizer.finalize_mode import (
    enter_finalize_mode,
    is_finalize_active,
)
from xpander_sdk.core.context_optimizer.encryption import (
    aencrypt,
    conversation_scope_id,
    derive_key,
)
from xpander_sdk.core.context_optimizer.error_patterns import (
    _is_context_overflow_error,
    _parse_provider_max_tokens,
)
from xpander_sdk.core.context_optimizer.helpers.chunking import (
    _message_char_size,
    _split_messages_into_chunks,
    _split_oversized_message_text,
)
from xpander_sdk.core.context_optimizer.helpers.recent_actions import (
    _build_recent_actions_block,
)
from xpander_sdk.core.context_optimizer.helpers.secrets import (
    _redact_sensitive_payload,
    _redact_sensitive_text,
)
from xpander_sdk.core.context_optimizer.helpers.tool_result import (
    _extract_balanced_value,
    _extract_repr_field,
    _head_tail_preview,
    _TOOL_INVOCATION_REPR_PREFIX,
    unwrap_tool_result_content,
)
from xpander_sdk.core.context_optimizer.helpers.xml_safety import (
    _ILLEGAL_XML_CHARS_RE,
    _looks_like_error_payload,
    _strip_illegal_xml_chars,
    _xml_attr_escape,
)
from xpander_sdk.core.context_optimizer.prompts import (
    AUTO_COMPACT_SYSTEM_PROMPT,
    AUTO_COMPACT_USER_PROMPT_TEMPLATE,
    CONTINUATION_MESSAGE_TEMPLATE,
    PARTIAL_COMPACT_SYSTEM_PROMPT,
    PARTIAL_COMPACT_USER_PROMPT_TEMPLATE,
    RECENT_ACTION_ENTRY_TEMPLATE,
    RECENT_ACTIONS_BLOCK_TEMPLATE,
    build_pre_retry_focus_instructions,
)
from xpander_sdk.core.context_optimizer.structure_sketch import sketch_structure
from xpander_sdk.core.context_optimizer.mixins import MapReduceMixin
from xpander_sdk.core.context_optimizer.workspace_cache import WorkspaceCache
from xpander_sdk.core.xpander_api_client import APIClient
from xpander_sdk.utils.event_loop import run_sync

if TYPE_CHECKING:
    from agno.metrics import RunMetrics
    from xpander_sdk.modules.agents.sub_modules.agent import Agent
    from xpander_sdk.modules.tasks.sub_modules.task import Task


__all__ = [
    # Public API
    "XPanderContextOptimizer",
    "CompactRetryResult",
    "build_pre_retry_focus_instructions",
    # Re-exported constants / templates kept for back-compat with internal
    # callers (events_module, agno.py) and tests that still import these from
    # ``context_optimizer.context_optimizer``. New code should import from
    # the new module homes (``constants.py``, ``prompts.py``, etc.).
    "AUTO_COMPACT_SYSTEM_PROMPT",
    "AUTO_COMPACT_USER_PROMPT_TEMPLATE",
    "CONTINUATION_MESSAGE_TEMPLATE",
    "PARTIAL_COMPACT_SYSTEM_PROMPT",
    "PARTIAL_COMPACT_USER_PROMPT_TEMPLATE",
    "RECENT_ACTIONS_BLOCK_TEMPLATE",
    "RECENT_ACTION_ENTRY_TEMPLATE",
    "MAX_CONSECUTIVE_COMPACT_FAILURES",
    "EMERGENCY_COMPACT_FRACTION",
    "SESSION_COMPACT_TIMEOUT",
    "RECENT_ACTIONS_COUNT",
    "RECENT_ACTIONS_ARGS_HEAD",
    "RECENT_ACTIONS_ARGS_TAIL",
    "RECENT_ACTIONS_RESULT_HEAD",
    "RECENT_ACTIONS_RESULT_TAIL",
    "unwrap_tool_result_content",
]


# Pin-message header doubles as the re-harvest marker across optimizer instances.
_PIN_HEADER = "Skill playbooks already loaded in this task"
_PLAYBOOK_SPAN_RE = re.compile(r'<skill_playbook\s+name="([^"]+)".*?(?:</skill_playbook>|\Z)', re.DOTALL)


@dataclass
class XPanderContextOptimizer(MapReduceMixin, CompressionManager):
    """4-layer context optimizer for xpander.ai agents (+ emergency).

    Plugs into agno's ``compression_manager`` slot but implements its own
    optimisation logic instead of relying on agno's built-in patterns.

    Layers:
        0 — headroom compaction (in tool hook, zero cost)
        1 — Microcompaction (workspace offload + preview)
        2 — Auto-compaction (LLM summarisation, replaces context window)
        3 — Manual compaction (agent-triggered via xpcompact_context)
        Emergency — 88% capacity safety net

    Attributes:
        agent: The xpander Agent instance (provides config + IDs for workspace calls).
        task: The xpander Task instance (provides task ID for storage paths;
              will be used in Layers 2/3 for plan following).
        min_content_length: Skip processing for tool results shorter than this.
        max_content_length: Offload threshold — results larger than this are
            saved to workspace and replaced with a preview.
        preview_length: Characters kept inline as preview for offloaded results.
        context_window: Model context window size in tokens.
        reserved_for_output: Tokens reserved for LLM output.
        buffer_tokens: Safety buffer before auto-compact threshold.
    """

    # xpander context (use Any to avoid dataclass/pydantic conflict)
    agent: Any = None
    task: Any = None

    # Dedicated model for compaction/LLM ops (PRO-1654). When set, all optimizer
    # LLM calls run on this cheaper/large model instead of the agent's own
    # ``model``. None ⇒ fall back to ``self.model``. Resolved by
    # ``agno._load_compaction_model`` by credential-availability priority.
    compaction_model: Any = None

    # Layer 1 settings. The budget sits where keeping a result inline costs
    # less than the retrieve round-trip an offload usually buys.
    min_content_length: int = 100
    max_content_length: int = 16_000
    preview_length: int = 4_000

    # Layer 2 settings
    context_window: int = 200_000
    reserved_for_output: int = 20_000
    buffer_tokens: int = 13_000

    # Map-reduce chunked-compaction settings.
    # When None, defaults to
    # ``int(context_window * DEFAULT_CHUNKED_COMPACT_THRESHOLD_FRAC)`` in
    # ``__post_init__`` (override frac with ``XP_COMPACT_CHUNK_THRESHOLD_FRAC``).
    chunked_compact_threshold: Optional[int] = None
    max_chunked_recursion_depth: int = 3
    # Per-map-chunk input cap in tokens. ``_compute_chunk_char_budget`` takes
    # ``min(provider_budget, max_chunk_input_tokens)`` so smaller chunks run
    # faster and parallelize wider. Override via ``XP_COMPACT_MAX_CHUNK_TOKENS``.
    max_chunk_input_tokens: int = field(
        default_factory=lambda: _env_int(
            "XP_COMPACT_MAX_CHUNK_TOKENS", DEFAULT_MAX_CHUNK_INPUT_TOKENS
        )
    )
    # Concurrency cap on the map phase. Override via
    # ``XP_COMPACT_MAP_CONCURRENCY`` (set to 1 to fall back to serial).
    map_phase_max_concurrency: int = field(
        default_factory=lambda: max(
            1,
            _env_int("XP_COMPACT_MAP_CONCURRENCY", DEFAULT_MAP_PHASE_MAX_CONCURRENCY),
        )
    )

    # Internal state (not dataclass init fields)
    _auto_compact_consecutive_failures: int = field(default=0, init=False, repr=False)
    # Consecutive compaction failures classified as provider-unreachable. Unlike
    # the counter above, this one gates the emergency/pre_retry path too, so a
    # dead compaction model can't spin the "true ceiling" loop forever.
    _emergency_connectivity_failures: int = field(default=0, init=False, repr=False)
    _compaction_attempt: int = field(default=0, init=False, repr=False)
    # Turns of grace remaining after a successful compaction. While > 0,
    # ``_should_auto_compact`` raises the trigger threshold by 5% of
    # ``context_window`` so the agent gets one productive turn before the
    # next compaction can fire.
    _post_compact_grace_remaining: int = field(default=0, init=False, repr=False)

    # Cached provider-reported max input tokens (populated on first overflow
    # error). Used to size chunk budgets elastically for the current model.
    _provider_max_tokens: Optional[int] = field(default=None, init=False, repr=False)

    # Layer 3 flags (set by tool hook, consumed by acompress)
    compact_requested: bool = field(default=False, init=False, repr=False)
    compact_focus: str = field(default="", init=False, repr=False)

    # Tool-call IDs that were already offloaded inline by the tool hook.
    # Used by the fallback layer_1_microcompact loop to avoid re-offloading
    # a message the hook already processed.
    _inline_offloaded_tool_call_ids: set = field(
        default_factory=set, init=False, repr=False
    )

    # context_id -> (fire-and-forget summary task, passes_seen); spliced into
    # its preview by a later microcompact pass, never awaited in the tool hook.
    _pending_offload_summaries: Dict[str, tuple] = field(
        default_factory=dict, init=False, repr=False
    )

    # Tool-call IDs of large xpworkspace-context-retrieve results already
    # shown to the model once. acompress runs pre-model each turn, so a
    # second sighting means the full payload was consumed last turn and can
    # be re-offloaded back to a preview pointing at its original context_id.
    _retrieve_msgs_seen_once: set = field(default_factory=set, init=False, repr=False)
    # skill name -> rendered playbook, harvested from skill-load tool results
    # before each L2 wipe and re-injected after it. Rebuilt from this dict every
    # compaction, so repeated compactions can never duplicate a pin.
    _pinned_skill_playbooks: dict = field(default_factory=dict, init=False, repr=False)
    # Last whole-session token estimate, refreshed once per turn in acompress.
    # One turn stale by construction; it only selects an offload band.
    _last_estimated_tokens: int = field(default=0, init=False, repr=False)
    _prompt_budget_logged: bool = field(default=False, init=False, repr=False)

    _last_emitted_status_pct: Optional[int] = field(
        default=None, init=False, repr=False
    )
    _compacting: bool = field(default=False, init=False, repr=False)

    # In-memory cache + write queue for Layer 1 offloaded blobs. The optimizer
    # writes encrypted bytes here synchronously and the cache spawns the
    # actual workspace POST in the background; the agno tool hook short-
    # circuits ``xpworkspace-context-retrieve`` against this cache and runs a
    # barrier flush before any other ``xpworkspace-*`` op so the sandbox is
    # consistent before bash/exec see it. See ``workspace_cache.py``.
    _workspace_cache: WorkspaceCache = field(
        default_factory=lambda: WorkspaceCache(), init=False, repr=False
    )

    # ---- Robust-L2 state -------------------------------------------- #
    # Compactions fired in the *current arun()*. Reset by ``acompress``
    # at the start of each turn-loop. Bound by MAX_COMPACTIONS_PER_ARUN.
    # This counter is per-optimizer-instance — that's the right scope:
    # a fresh arun starts a fresh budget. The per-task and pre_retry
    # counters live on ``self.task`` (see ``_compactions_this_task``
    # / ``_pre_retry_compactions_this_task`` properties) so they
    # survive optimizer replacement across plan retries.
    _compactions_this_arun: int = field(default=0, init=False, repr=False)

    # Set by the stagnant-compaction guard when consecutive no-progress
    # compactions cross ``STAGNANT_COMPACTION_WARN_AT`` but stay below
    # ``MAX_STAGNANT_COMPACTIONS``. Consumed by the continuation-message
    # builder, which appends a one-line warning and clears the flag.
    _stagnant_warning_pending: bool = field(default=False, init=False, repr=False)

    # Finalize-only state — see ``finalize_mode.py``. Initialized to a
    # default-inactive ``FinalizeOnlyState`` lazily because the import
    # would create a circular dependency if eagerly evaluated here.
    _finalize_state: Any = field(default=None, init=False, repr=False)

    # ---- Task-scoped counter accessors ----------------------------- #
    # The plan-retry loop in ``events_module.handle_task_execution_request``
    # replaces the optimizer instance on every retry (see
    # ``events_module.py:486-492``). Without task-scoped storage the
    # caps would reset on each retry and the cascading-compaction
    # signature (Mode 1) would re-emerge despite our guards. Storing
    # the counters on ``task._xp_*`` mirrors the action-ledger pattern.

    def _task_counter(self, key: str) -> int:
        if self.task is None:
            return 0
        return int(getattr(self.task, f"_xp_compact_{key}", 0))

    def _set_task_counter(self, key: str, value: int) -> None:
        if self.task is None:
            return
        try:
            object.__setattr__(self.task, f"_xp_compact_{key}", value)
        except Exception:
            pass

    @property
    def _compactions_this_task(self) -> int:
        return self._task_counter("total")

    @_compactions_this_task.setter
    def _compactions_this_task(self, value: int) -> None:
        self._set_task_counter("total", value)

    @property
    def _pre_retry_compactions_this_task(self) -> int:
        return self._task_counter("pre_retry")

    @_pre_retry_compactions_this_task.setter
    def _pre_retry_compactions_this_task(self, value: int) -> None:
        self._set_task_counter("pre_retry", value)

    @property
    def _ledger_seq_at_last_compaction(self) -> int:
        return self._task_counter("ledger_seq")

    @_ledger_seq_at_last_compaction.setter
    def _ledger_seq_at_last_compaction(self, value: int) -> None:
        self._set_task_counter("ledger_seq", value)

    @property
    def _stagnant_compactions(self) -> int:
        return self._task_counter("stagnant")

    @_stagnant_compactions.setter
    def _stagnant_compactions(self, value: int) -> None:
        self._set_task_counter("stagnant", value)

    def __post_init__(self):
        self.compress_tool_results = True
        super().__post_init__()
        if self.chunked_compact_threshold is None:
            frac = _env_float(
                "XP_COMPACT_CHUNK_THRESHOLD_FRAC",
                DEFAULT_CHUNKED_COMPACT_THRESHOLD_FRAC,
            )
            frac = max(0.1, min(0.99, frac))
            self.chunked_compact_threshold = int(self.context_window * frac)
        logger.info(
            f"[context-optimizer] initialized "
            f"(max_content={self.max_content_length}, headroom_bands={L1_HEADROOM_BANDS}, "
            f"preview={self.preview_length}, "
            f"context_window={self.context_window}, threshold={self._auto_compact_threshold}, "
            f"chunked_threshold={self.chunked_compact_threshold}, "
            f"max_chunk_input_tokens={self.max_chunk_input_tokens}, "
            f"map_concurrency={self.map_phase_max_concurrency})"
        )

    # ------------------------------------------------------------------ #
    #  Token estimation
    # ------------------------------------------------------------------ #

    @staticmethod
    def _estimate_tokens(messages: List[Message]) -> int:
        """Rough token count: ~4 chars per token, with 1.2x safety margin.

        The chars/4 heuristic underestimates real token counts because it
        misses multi-byte characters, special tokens, and structured message
        overhead.  The 20% padding aligns the trigger with ~80% of the
        context window — the threshold used by production agentic systems.
        """
        raw = len(json.dumps([m.to_dict() for m in messages], default=str)) // 4
        return int(raw * 1.2)

    @staticmethod
    def _estimate_tokens_for_text(text: str) -> int:
        """Token estimate for a single string — same chars/4 * 1.2 heuristic as ``_estimate_tokens``."""
        return int(len(text) / 4 * 1.2)

    @property
    def _auto_compact_threshold(self) -> int:
        return self.context_window - self.reserved_for_output - self.buffer_tokens

    # ------------------------------------------------------------------ #
    #  Workspace storage
    # ------------------------------------------------------------------ #

    @property
    def _workspace_enabled(self) -> bool:
        """Whether workspace I/O is allowed for this agent.

        Driven by ``Agent.workspace_tools_enabled``. When False, all workspace
        writes (L1 offload, L2 session backup) are skipped; L2 summarisation
        still runs.
        """
        return bool(getattr(self.agent, "workspace_tools_enabled", True))

    async def _save_to_workspace(self, content: str) -> Optional[str]:
        """Encrypt *content*, hand the bytes to the workspace cache, and
        return the workspace path immediately.

        The cache stores the encrypted bytes in memory and spawns the actual
        workspace POST in the background. The LLM sees the preview +
        retrieval pointer without waiting for the network round-trip;
        ``xpworkspace-context-retrieve`` short-circuits against the cache,
        and any other ``xpworkspace-*`` op runs a barrier flush via
        ``WorkspaceCache.aflush()`` before executing so the sandbox is
        consistent.

        Returns the workspace path on success, or ``None`` if encryption /
        path construction failed (the cache write itself never blocks). A
        queued workspace-POST failure is surfaced on the next barrier op,
        not here — see ``WorkspaceCache.aflush()``.
        """
        if not self.agent or not self.task:
            logger.warning(
                "[context-optimizer] workspace save skipped: agent or task not set"
            )
            return None

        if not self._workspace_enabled:
            # Workspace tools disabled for this agent — leave content inline
            # (maybe_offload_content treats None as "no offload"). No truncation,
            # no workspace write. Distinct from "workspace unavailable" (a write
            # that was attempted and failed).
            logger.debug(
                "[context-optimizer] workspace save skipped: workspace disabled"
            )
            return None

        file_id = str(uuid.uuid4())
        path = f"CONTEXT_OPTIMIZATION/{file_id}.xp"

        try:
            key = derive_key(
                org_id=self.agent.configuration.organization_id,
                agent_id=self.agent.id,
                task_id=conversation_scope_id(self.task),
            )
            encrypted_content = await aencrypt(content, key)
        except Exception as e:
            logger.warning(f"[context-optimizer] workspace save failed (encrypt): {e}")
            return None

        self._workspace_cache.put(
            context_id=file_id,
            encrypted=encrypted_content,
            size=len(content),
            workspace_path=path,
            do_write_async=lambda p=path, c=encrypted_content: self._do_workspace_write(
                p, c
            ),
        )
        logger.info(
            f"[context-optimizer] queued encrypted tool result for workspace write: "
            f"{path} ({len(content):,} chars)"
        )
        return path

    async def _do_workspace_write(self, path: str, encrypted_content: str) -> None:
        """The actual workspace POST. Spawned by the cache; never awaited
        directly from the optimizer's hot path.
        """
        client = APIClient(configuration=self.agent.configuration)
        await client.make_request(
            path=str(APIRoute.WorkspaceToolInvoke).format(
                agent_id=self.agent.id,
                tool_name="file_write",
            ),
            method="POST",
            payload={"path": path, "content": encrypted_content},
        )
        logger.debug(f"[context-optimizer] flushed workspace write: {path}")

    async def aclose(self) -> None:
        """Drain pending workspace writes and clear the in-memory cache.

        Called from the SDK's ``events_module`` (and the cloud's
        ``agent_executor``) in the ``finally`` block of a task run, after
        ``arun()`` has returned, so any L1 writes queued in the agent's
        last turn finish before the task is marked complete. Errors from
        queued writes are logged at this point — the task is finishing and
        propagating them up serves no purpose.
        """
        try:
            await self._workspace_cache.aclose()
        except Exception as exc:
            logger.warning(f"[context-optimizer] workspace cache close errored: {exc}")

        # ---- Persist action ledger to workspace (best-effort) ------ #
        # Single bulk file_write — same endpoint as the session-backup
        # path. Failures are logged but never propagated; the in-memory
        # ledger has already done its job for the current process.
        if LEDGER_ENABLED and self.task is not None:
            try:
                ledger = get_attached_ledger(self.task)
                if ledger is not None:
                    await ledger.aclose()
            except Exception as exc:
                logger.warning(
                    f"[context-optimizer] action-ledger close errored: {exc}"
                )

    def close(self) -> None:
        """Sync wrapper around :meth:`aclose`.

        Mirrors the SDK's dual async/sync API contract (``compress`` /
        ``acompress``, ``should_compress`` / ``ashould_compress``). Sync
        callers — primarily one-shot scripts and the rare integration that
        does not run inside an event loop — use this to drain L1 writes
        without having to manage an event loop themselves.
        """
        run_sync(self.aclose())

    # ------------------------------------------------------------------ #
    #  Agno interface — should_compress
    # ------------------------------------------------------------------ #

    async def ashould_compress(
        self,
        messages: List[Message],
        tools: Optional[List] = None,
        model: Optional[Model] = None,
        response_format: Optional[Union[Dict, Type[BaseModel]]] = None,
    ) -> bool:
        """Always returns True — Layer 1 runs every turn."""
        return True

    def should_compress(
        self,
        messages: List[Message],
        tools: Optional[List] = None,
        model: Optional[Model] = None,
        response_format: Optional[Union[Dict, Type[BaseModel]]] = None,
    ) -> bool:
        return True

    # ------------------------------------------------------------------ #
    #  Agno interface — compress  (orchestrates all layers)
    # ------------------------------------------------------------------ #

    @property
    def _emergency_compact_threshold(self) -> int:
        return int(self.context_window * EMERGENCY_COMPACT_FRACTION)

    def _should_emergency_compact(
        self, messages: List[Message], estimated: Optional[int] = None
    ) -> bool:
        """Return True when context is near the absolute ceiling (88%).

        Bypasses the circuit breaker — this is a last-resort safety net.
        """
        est = self._estimate_tokens(messages) if estimated is None else estimated
        return est >= self._emergency_compact_threshold

    async def acompress(
        self,
        messages: List[Message],
        run_metrics: Optional["RunMetrics"] = None,
    ) -> None:
        """Run the optimisation pipeline (called by agno every turn)."""
        # Skip all context management when the agent has it disabled.
        if not getattr(self.agent, "with_auto_context_management", True):
            return

        # Reset per-arun compaction counter at the start of each turn so
        # the per-arun guard (MAX_COMPACTIONS_PER_ARUN) is scoped correctly.
        self._compactions_this_arun = 0

        self._log_rendered_prompt_size(messages)

        # Layer 1: always runs — offload large tool results to workspace
        await self.layer_1_microcompact(messages)

        # One token estimate for the whole turn (computed AFTER layer 1 mutates
        # messages), reused by status + both compaction gates below.
        estimated = self._estimate_tokens(messages)
        self._last_estimated_tokens = estimated
        await self._publish_context_status(messages, estimated=estimated)

        # Layer 3: agent-requested manual compaction (takes priority)
        if self.compact_requested:
            focus = self.compact_focus
            self.compact_requested = False
            self.compact_focus = ""
            logger.info(
                f"[context-optimizer] layer 3 triggered: "
                f"manual compact requested (est_tokens={estimated:,}, focus={focus!r})"
            )
            await self.layer_2_auto_compact(
                messages,
                run_metrics,
                custom_instructions=focus,
                trigger="manual",
            )
            return

        # Layer 2: auto-compact at normal threshold (167K)
        if self._should_auto_compact(messages, estimated=estimated):
            logger.info(
                f"[context-optimizer] layer 2 triggered: "
                f"{estimated:,} tokens >= {self._auto_compact_threshold:,} threshold"
            )
            await self.layer_2_auto_compact(messages, run_metrics, trigger="auto")
            return

        # Emergency: near-ceiling safety net at 88% — bypasses circuit breaker
        if self._should_emergency_compact(messages, estimated=estimated):
            pct = estimated / self.context_window * 100
            logger.warning(
                f"[context-optimizer] emergency compact: context at {pct:.0f}% capacity "
                f"({estimated:,} tokens >= {self._emergency_compact_threshold:,}), "
                f"compacting to prevent overflow"
            )
            # Emergency bypasses the failure breaker (overflow is a true ceiling),
            # so a provider that can't be reached would spin this forever. Retry
            # with exponential backoff instead: a transient outage self-recovers,
            # and only a persistently dead provider aborts the task.
            for attempt in range(EMERGENCY_CONNECTIVITY_RETRY_MAX_ATTEMPTS + 1):
                await self.layer_2_auto_compact(
                    messages,
                    run_metrics,
                    custom_instructions="EMERGENCY: context is near overflow. Focus on preserving the most recent work state, pending tasks, and key decisions.",
                    trigger="emergency",
                )
                # Success or a non-connectivity failure — stop here. (The internal
                # handler resets this counter to 0 on both, and only leaves it > 0
                # when the compaction model itself was unreachable.)
                if self._emergency_connectivity_failures == 0:
                    break
                if attempt >= EMERGENCY_CONNECTIVITY_RETRY_MAX_ATTEMPTS:
                    self._emergency_connectivity_failures = 0
                    raise ProviderUnreachableError(
                        f"model provider unreachable through {attempt + 1} emergency "
                        f"compaction attempts; aborting instead of spinning near overflow"
                    )
                delay = min(
                    EMERGENCY_CONNECTIVITY_RETRY_BASE_DELAY * (2 ** attempt),
                    EMERGENCY_CONNECTIVITY_RETRY_MAX_DELAY,
                )
                logger.warning(
                    f"[context-optimizer] emergency compaction blocked by provider "
                    f"connectivity; retry {attempt + 1}/{EMERGENCY_CONNECTIVITY_RETRY_MAX_ATTEMPTS} "
                    f"in {delay:.0f}s"
                )
                await asyncio.sleep(delay)

    def compress(
        self,
        messages: List[Message],
        run_metrics: Optional["RunMetrics"] = None,
    ) -> None:
        run_sync(self.acompress(messages, run_metrics=run_metrics))

    # ------------------------------------------------------------------ #
    #  Agno interface — _compress_tool_result  (unused, kept for compat)
    # ------------------------------------------------------------------ #

    async def _acompress_tool_result(
        self,
        tool_result: Message,
        run_metrics: Optional["RunMetrics"] = None,
    ) -> Optional[str]:
        """Not used directly — Layer 1 handles compression in bulk."""
        return None

    def _compress_tool_result(
        self,
        tool_result: Message,
        run_metrics: Optional["RunMetrics"] = None,
    ) -> Optional[str]:
        return None

    # ================================================================== #
    #  Layer 1 — Microcompaction (workspace offload + preview)
    # ================================================================== #

    # Tool names for which L1 must NOT offload (reasoning + xp-prefixed
    # internal tools, except the data-shaped ones in L1_XP_OFFLOAD_ELIGIBLE).
    @staticmethod
    def _l1_skip_tool(tool_name: Optional[str]) -> bool:
        if not tool_name:
            return False
        if tool_name in L1_ALWAYS_SKIP:
            return True
        if tool_name.startswith("xp") and tool_name not in L1_XP_OFFLOAD_ELIGIBLE:
            return True
        return False

    def _log_rendered_prompt_size(self, messages: List[Message]) -> None:
        """Log the rendered system message size once per task, sizes only.

        Pairs with the ``[prompt-budget] build`` line the agno builder emits:
        that one covers what the SDK assembled, this one what agno actually
        rendered, and the delta is agno's own scaffolding. Never logs content -
        the prompt carries user memories and org data.
        """
        if self._prompt_budget_logged or not PROMPT_BUDGET_ENABLED:
            return
        self._prompt_budget_logged = True
        try:
            system = next((m for m in messages if m.role == "system"), None)
            if system is None:
                return
            content = system.content if isinstance(system.content, str) else ""
            payload = {
                "task_id": getattr(self.task, "id", "") or "",
                "agent_id": getattr(self.agent, "id", "") or "",
                "system_message_tok": self._estimate_tokens_for_text(content),
                "message_count": len(messages),
            }
            logger.info(
                f"[prompt-budget] rendered {json.dumps(payload, separators=(',', ':'))}"
            )
        except Exception as exc:
            logger.debug(f"[prompt-budget] rendered skipped: {exc}")

    def _effective_max_content_length(self) -> int:
        """Offload threshold scaled by how full the context already is.

        An offload trades a small permanent context saving for a likely
        context-retrieve round-trip, so it is a bad trade while the window is
        mostly empty — a whole extra turn re-reads the entire prompt. Above the
        last band the configured value applies unchanged, so behaviour under
        real pressure matches the pre-band implementation.
        """
        window = max(1, int(self.context_window))
        used_frac = max(0, self._last_estimated_tokens) / window
        for band_frac, multiplier in L1_HEADROOM_BANDS:
            if used_frac < band_frac:
                return self.max_content_length * multiplier
        return self.max_content_length

    @staticmethod
    def _effective_tool_name(msg: Message) -> Optional[str]:
        """Resolve the real tool behind a message, unwrapping the dynamic dispatcher.

        agno records ``xp_execute_tool`` as the tool name for every dynamically
        dispatched call, so the skip check above would exempt arbitrary external
        results. The real id lives in the same ``payload`` shape the retrieve
        path parses. Mirrors ``_effective_tool_identity`` in the agno layer,
        duplicated here to keep the optimizer free of framework imports.
        """
        tool_name = getattr(msg, "tool_name", None)
        if tool_name != DYNAMIC_DISPATCH_META_TOOL:
            return tool_name
        tool_args = getattr(msg, "tool_args", None)
        if isinstance(tool_args, dict):
            payload = tool_args.get("payload")
            inner = payload.get("name") if isinstance(payload, dict) else None
            if isinstance(inner, str) and inner.strip():
                return inner.strip()
        return tool_name

    def _build_offload_preview(
        self, content: str, workspace_path: str, original_len: int
    ) -> str:
        # Derive the context_id from the workspace path: CONTEXT_OPTIMIZATION/{context_id}.xp
        context_id = workspace_path.rsplit("/", 1)[-1]
        if context_id.endswith(".xp"):
            context_id = context_id[:-3]
        est_tokens = self._estimate_tokens_for_text(content)
        sketch = sketch_structure(content)
        structure_line = f"[STRUCTURE] {sketch}\n" if sketch else ""
        decide_from = "the preview and the structure line" if sketch else "the preview"
        return (
            f"{content[: self.preview_length]}\n\n"
            f"[TRUNCATED OUTPUT - {original_len:,} chars (~{est_tokens:,} tokens) total, showing first {self.preview_length:,} chars]\n"
            f"{structure_line}"
            f"Full result saved (encrypted) to: {workspace_path}\n"
            f"Decide from {decide_from} first — when that already answers the "
            f"step you are on, continue without retrieving. "
            f'When you need specific values, call xpworkspace-context-retrieve with context_id="{context_id}" '
            f'and query="<regex>" or semantic_query="<text>" to get back only the matching parts '
            f"instead of all ~{est_tokens:,} tokens. You can call it multiple times on the same context_id with "
            f"different queries to drill in without re-pulling the whole result. "
            f"A retrieve with neither query returns everything — reserve it for when every record matters, "
            f"such as transforming or persisting the whole dataset, and write what comes back to a plaintext "
            f"workspace file in that same step. "
            f"The file is encrypted and scoped to the current task; xpworkspace-context-retrieve is the reader "
            f"that decrypts it. "
            f"If this content contains rules, steps, or procedures you are expected to follow "
            f"(a playbook, runbook, or SOP), retrieve the full content before acting - "
            f"a preview is never a sufficient basis for following a procedure."
        )

    async def maybe_offload_content(
        self,
        content: Any,
        tool_name: Optional[str],
    ) -> tuple:
        """Offload *content* to the workspace when it exceeds the effective threshold.

        Returns ``(replacement, workspace_path)`` when an offload happens,
        where ``replacement`` is the preview + retrieval-pointer string
        that should be used as the visible tool output. Returns
        ``(None, None)`` when the content is skipped, too small, or
        between min/max (passthrough). Also updates ``self.stats`` so
        both the inline (tool-hook) and fallback paths share counters.
        """
        if self._l1_skip_tool(tool_name):
            return None, None
        # Normalize to clean JSON string (strips ToolInvocationResult repr).
        clean = unwrap_tool_result_content(content)
        if not isinstance(clean, str) or len(clean) <= self.min_content_length:
            return None, None
        original_len = len(clean)
        if original_len <= self._effective_max_content_length():
            # Between min and max — passthrough (caller decides whether to
            # mark the message as processed). Count as a passthrough.
            self.stats["tool_results_compressed"] = (
                self.stats.get("tool_results_compressed", 0) + 1
            )
            self.stats["original_size"] = (
                self.stats.get("original_size", 0) + original_len
            )
            self.stats["compressed_size"] = (
                self.stats.get("compressed_size", 0) + original_len
            )
            return None, None

        workspace_path = await self._save_to_workspace(clean)
        if not workspace_path:
            # Workspace unavailable or disabled — leave the content unchanged.
            return None, None

        replacement = self._build_offload_preview(
            content=clean,
            workspace_path=workspace_path,
            original_len=original_len,
        )
        compressed_len = len(replacement)
        self.stats["tool_results_compressed"] = (
            self.stats.get("tool_results_compressed", 0) + 1
        )
        self.stats["original_size"] = self.stats.get("original_size", 0) + original_len
        self.stats["compressed_size"] = (
            self.stats.get("compressed_size", 0) + compressed_len
        )
        logger.info(
            f"[context-optimizer] layer 1: offloaded '{tool_name or 'unknown'}' to workspace "
            f"({original_len:,} -> {compressed_len:,} chars, path={workspace_path})"
        )
        return replacement, workspace_path

    def _pin_skill_playbook(self, name: str, playbook: str) -> None:
        """Upsert one playbook span, newest-wins, bounded by PINNED_SKILLS_MAX."""
        if len(playbook) > PINNED_SKILL_MAX_CHARS:
            cut = PINNED_SKILL_MAX_CHARS - 60
            playbook = playbook[:cut] + "\n[truncated - full files in ./skills/]\n</skill_playbook>"
        self._pinned_skill_playbooks.pop(name, None)
        self._pinned_skill_playbooks[name] = playbook
        while len(self._pinned_skill_playbooks) > PINNED_SKILLS_MAX:
            self._pinned_skill_playbooks.pop(next(iter(self._pinned_skill_playbooks)))

    def _harvest_skill_playbooks(self, messages: List[Message]) -> None:
        """Collect loaded skill playbooks so they survive the L2 wipe.

        Only successful loads carry the <skill_playbook> wrapper; failure
        strings never do, so the tag doubles as the success check. Only the
        tagged span is pinned - the load result's apply-now tail would
        re-instruct a restart from step one on every compaction. A prior
        pin message (role=user, our header) is re-harvested too, so pins
        survive a fresh optimizer instance (e.g. a plan retry).
        """
        for msg in messages:
            role = getattr(msg, "role", None)
            if role == "user" and isinstance(msg.content, str) and msg.content.startswith(_PIN_HEADER):
                for m in re.finditer(_PLAYBOOK_SPAN_RE, msg.content):
                    self._pin_skill_playbook(m.group(1), m.group(0))
                continue
            if role != "tool":
                continue
            if self._effective_tool_name(msg) not in SKILL_PIN_TOOL_NAMES:
                continue
            content = unwrap_tool_result_content(msg.content)
            if not isinstance(content, str):
                continue
            match = re.search(_PLAYBOOK_SPAN_RE, content)
            if match:
                self._pin_skill_playbook(match.group(1), match.group(0))

    def _render_pinned_skill_playbooks(self) -> str:
        """One user message re-carrying every pinned playbook, or '' when none."""
        if not self._pinned_skill_playbooks:
            return ""
        return (
            _PIN_HEADER
            + ", kept across context compaction. "
            "Follow them from wherever the accompanying context summary says you are - do not "
            "restart them and do not load these skills again:\n"
            + "\n".join(self._pinned_skill_playbooks.values())
        )

    def _maybe_reoffload_retrieve(self, msg: Message) -> bool:
        """Collapse a stale full-payload context-retrieve result back to a
        preview pointing at its original context_id (no new workspace blob).

        Returns True when the message was re-offloaded. First sighting of a
        large payload is left intact so the model gets one full view, and while
        there is ample headroom the payload is kept for good — the agent asked
        for it, and evicting it just buys another retrieve.
        """
        content = unwrap_tool_result_content(msg.content)
        if (
            not isinstance(content, str)
            or len(content) <= self._effective_max_content_length()
        ):
            return False
        tool_call_id = getattr(msg, "tool_call_id", None)
        if not tool_call_id:
            return False
        if tool_call_id not in self._retrieve_msgs_seen_once:
            self._retrieve_msgs_seen_once.add(tool_call_id)
            return False

        # Recover the original context_id from the call args (same shape the
        # agno hook parses: payload.body_params.context_id, then top-level).
        context_id = None
        tool_args = getattr(msg, "tool_args", None)
        if isinstance(tool_args, dict):
            payload_obj = tool_args.get("payload")
            body = (
                payload_obj.get("body_params", {})
                if isinstance(payload_obj, dict)
                else {}
            )
            cid = (
                body.get("context_id")
                if isinstance(body, dict)
                else None
            ) or tool_args.get("context_id")
            if isinstance(cid, str) and cid.strip():
                context_id = cid.strip()
        if not context_id:
            return False

        original_len = len(content)
        replacement = self._build_offload_preview(
            content=content,
            workspace_path=f"CONTEXT_OPTIMIZATION/{context_id}.xp",
            original_len=original_len,
        )
        msg.compressed_content = replacement
        self.stats["tool_results_compressed"] = (
            self.stats.get("tool_results_compressed", 0) + 1
        )
        self.stats["original_size"] = self.stats.get("original_size", 0) + original_len
        self.stats["compressed_size"] = (
            self.stats.get("compressed_size", 0) + len(replacement)
        )
        logger.info(
            f"[context-optimizer] layer 1: re-offloaded stale context-retrieve "
            f"({original_len:,} -> {len(replacement):,} chars, ctx={context_id})"
        )
        return True

    def register_pending_summary(self, context_id: str, summary_task: Any) -> None:
        """Track an in-flight offload summary for a later splice into its preview."""
        if not context_id or summary_task is None:
            return
        self._pending_offload_summaries[context_id] = (summary_task, 0)

    @staticmethod
    def _splice_summary_into_preview(
        messages: List[Message], context_id: str, summary: str
    ) -> bool:
        """Insert ``[SUMMARY] ...`` under the truncation marker of one preview."""
        # One line, bounded: the block is line-oriented and the summarizer returns free text.
        summary = " ".join(summary.split())[:OFFLOAD_SUMMARY_MAX_CHARS]
        if not summary:
            return False
        marker = f'context_id="{context_id}"'
        for msg in messages:
            if msg.role != "tool":
                continue
            uses_compressed = msg.compressed_content is not None
            text = msg.compressed_content if uses_compressed else msg.content
            if not isinstance(text, str) or marker not in text or "[SUMMARY]" in text:
                continue
            lines = text.split("\n")
            for idx, line in enumerate(lines):
                if line.startswith("[TRUNCATED OUTPUT -"):
                    lines.insert(idx + 1, f"[SUMMARY] {summary}")
                    break
            else:
                continue
            updated = "\n".join(lines)
            if uses_compressed:
                msg.compressed_content = updated
            else:
                msg.content = updated
            return True
        return False

    def _splice_ready_summaries(self, messages: List[Message]) -> None:
        """Fold resolved offload summaries into their previews, one shot each."""
        for context_id, (summary_task, passes) in list(
            self._pending_offload_summaries.items()
        ):
            try:
                done = summary_task.done()
            except Exception:
                self._pending_offload_summaries.pop(context_id, None)
                continue
            if not done:
                if passes + 1 >= PENDING_SUMMARY_MAX_PASSES:
                    self._pending_offload_summaries.pop(context_id, None)
                    logger.debug(
                        f"[context-optimizer] layer 1: offload summary still pending after "
                        f"{PENDING_SUMMARY_MAX_PASSES} passes, left to warm the cache (ctx={context_id})"
                    )
                else:
                    self._pending_offload_summaries[context_id] = (
                        summary_task,
                        passes + 1,
                    )
                continue
            self._pending_offload_summaries.pop(context_id, None)
            try:
                summary = summary_task.result()
            except Exception as exc:
                logger.debug(f"[context-optimizer] offload summary unavailable: {exc}")
                continue
            if not isinstance(summary, str) or not summary.strip():
                continue
            if self._splice_summary_into_preview(messages, context_id, summary.strip()):
                logger.debug(
                    f"[context-optimizer] layer 1: spliced summary into preview (ctx={context_id})"
                )

    async def layer_1_microcompact(self, messages: List[Message]) -> None:
        """Fallback offload loop for messages the tool hook didn't process.

        With the inline offload from the agno tool hook, fresh tool results
        are already truncated by the time they reach this loop. This loop
        still runs every turn so messages arriving from session history /
        resumed runs (where the hook never fired) are offloaded too.
        """
        if self._pending_offload_summaries:
            self._splice_ready_summaries(messages)

        offloaded_count = 0
        passthrough_count = 0
        skipped_count = 0
        turn_saved_chars = 0

        for msg in messages:
            if msg.role != "tool":
                continue
            if msg.compressed_content is not None:
                skipped_count += 1
                continue
            # Hook already offloaded this message — do not re-process.
            tool_call_id = getattr(msg, "tool_call_id", None)
            if tool_call_id and tool_call_id in self._inline_offloaded_tool_call_ids:
                skipped_count += 1
                continue
            # Stale-retrieve re-offload: a full context-retrieve payload gets
            # exactly one turn on context, then collapses back to a preview
            # pointing at the SAME context_id. Handled before the xp* skip
            # below, which would otherwise exempt it forever.
            if msg.tool_name == "xpworkspace-context-retrieve":
                if self._maybe_reoffload_retrieve(msg):
                    offloaded_count += 1
                else:
                    skipped_count += 1
                continue
            eff_tool_name = self._effective_tool_name(msg)
            if self._l1_skip_tool(eff_tool_name):
                skipped_count += 1
                continue

            # Strip the pydantic ``ToolInvocationResult`` wrapper so only the
            # actual tool result (JSON) is saved to the workspace and previewed
            # to the LLM. Non-xpander tool results pass through unchanged.
            content = unwrap_tool_result_content(msg.content)
            if len(content) <= self.min_content_length:
                skipped_count += 1
                continue

            original_len = len(content)
            tool_name = eff_tool_name or "unknown"

            replacement, workspace_path = await self.maybe_offload_content(
                content=content,
                tool_name=tool_name,
            )
            if replacement is not None:
                msg.compressed_content = replacement
                compressed_len = len(replacement)
                saved = original_len - compressed_len
                turn_saved_chars += saved
                offloaded_count += 1
                logger.info(
                    f"[context-optimizer] layer 1 (fallback): offloaded '{tool_name}' "
                    f"({original_len:,} -> {compressed_len:,} chars, saved {saved:,} chars, "
                    f"path={workspace_path})"
                )
                continue

            effective_max = self._effective_max_content_length()
            if original_len > effective_max:
                # Workspace save failed — leave the content alone.
                logger.warning(
                    f"[context-optimizer] layer 1 (fallback): keeping full result for "
                    f"'{tool_name}' ({original_len:,} chars) — workspace unavailable"
                )
                continue

            # Between min and max — mark as processed so we don't revisit.
            msg.compressed_content = content
            passthrough_count += 1
            logger.debug(
                f"[context-optimizer] layer 1 (fallback): passthrough '{tool_name}' "
                f"({original_len:,} chars, below {effective_max:,} threshold)"
            )

        total_processed = offloaded_count + passthrough_count
        if total_processed > 0 or skipped_count > 0:
            total_original = self.stats.get("original_size", 0)
            total_compressed = self.stats.get("compressed_size", 0)
            total_saved = total_original - total_compressed
            savings_pct = (
                (total_saved / total_original * 100) if total_original > 0 else 0
            )
            logger.info(
                f"[context-optimizer] layer 1 summary: "
                f"offloaded={offloaded_count}, passthrough={passthrough_count}, "
                f"already_processed={skipped_count} | "
                f"this turn saved {turn_saved_chars:,} chars | "
                f"cumulative: {total_original:,} -> {total_compressed:,} chars "
                f"({savings_pct:.1f}% savings)"
            )

    # ================================================================== #
    #  Layer 2 — Auto-compaction (LLM summarisation)
    # ================================================================== #

    def _should_auto_compact(
        self, messages: List[Message], estimated: Optional[int] = None
    ) -> bool:
        """Check whether token usage has crossed the auto-compact threshold.

        Returns ``False`` immediately if the circuit breaker is open
        (too many consecutive failures). Within the post-compaction grace
        window, the trigger threshold is raised by 5% of the context window
        so the agent gets one productive turn between compactions instead
        of immediately re-firing on the continuation summary.
        """
        if self._auto_compact_consecutive_failures >= MAX_CONSECUTIVE_COMPACT_FAILURES:
            return False
        threshold = self._auto_compact_threshold
        if self._post_compact_grace_remaining > 0:
            self._post_compact_grace_remaining -= 1
            threshold = threshold + int(self.context_window * 0.05)
        est = self._estimate_tokens(messages) if estimated is None else estimated
        return est >= threshold

    # -- helpers -------------------------------------------------------- #

    def _has_active_plan(self) -> bool:
        """Return True if a deep-planning plan with tasks is active."""
        return bool(
            self.task
            and self.task.deep_planning
            and self.task.deep_planning.enabled
            and self.task.deep_planning.tasks
        )

    def _build_plan_section(self) -> str:
        """Build the plan-status block for the compaction prompt.

        Returns an empty string when there is no active plan.
        """
        if not self._has_active_plan():
            return ""

        lines = []
        completed = 0
        first_uncompleted = None
        for t in self.task.deep_planning.tasks:
            mark = "✓" if t.completed else " "
            lines.append(f"   [{mark}] {t.title} (ID: {t.id})")
            if t.completed:
                completed += 1
            elif first_uncompleted is None:
                first_uncompleted = t

        total = len(self.task.deep_planning.tasks)
        plan_block = "\n".join(lines)
        next_task_line = (
            f"   Next task: {first_uncompleted.title} (ID: {first_uncompleted.id})"
            if first_uncompleted
            else ""
        )
        return (
            f"\n   {PLAN_BLOCK_LABEL} (status at compaction):\n{plan_block}\n"
            f"   Completed: {completed}/{total} tasks\n"
            f"{next_task_line}"
        )

    def _build_compaction_prompt(
        self,
        messages: List[Message],
        custom_instructions: str = "",
    ) -> str:
        """Render the user-side compaction prompt with conversation + template."""
        conversation = json.dumps(
            [m.to_dict() for m in messages],
            default=str,
            ensure_ascii=False,
        )
        plan_section = self._build_plan_section()
        custom_section = (
            f"\nAdditional focus: {custom_instructions}" if custom_instructions else ""
        )
        return AUTO_COMPACT_USER_PROMPT_TEMPLATE.format(
            conversation=conversation,
            plan_section=plan_section,
            custom_instructions_section=custom_section,
        )

    async def _push_activity_event(
        self,
        event_type: Any,
        data: Any,
    ) -> None:
        """Push an event to the task activity log.

        Fire-and-forget — failures are logged but never block compaction.
        """
        if not self.agent or not self.task:
            return
        try:
            from xpander_sdk.modules.tasks.sub_modules.task import TaskUpdateEvent

            evt = TaskUpdateEvent(
                task_id=self.task.id,
                organization_id=self.task.organization_id,
                time=datetime.now(timezone.utc).isoformat(),
                type=event_type,
                data=data,
            )
            client = APIClient(configuration=self.agent.configuration)
            await client.make_request(
                path=APIRoute.PushExecutionEventToQueue.format(task_id=self.task.id),
                method="POST",
                payload=[evt.model_dump_safe()],
            )
        except Exception as exc:
            logger.warning(
                f"[context-optimizer] layer 2: failed to push activity event: {exc}"
            )

    async def _publish_compaction_start(
        self,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        pre_tokens: int,
        pre_message_count: int,
        focus: str = "",
    ) -> None:
        """Emit a compaction_started event."""
        from xpander_sdk.models.compactization import (
            TaskCompactizationEvent,
            TaskCompactizationStarted,
        )
        from xpander_sdk.models.events import TaskUpdateEventType

        await self._push_activity_event(
            event_type=TaskUpdateEventType.TaskCompactization,
            data=TaskCompactizationEvent(
                type="compaction_started",
                data=TaskCompactizationStarted(
                    trigger=trigger,
                    estimated_tokens=pre_tokens,
                    message_count=pre_message_count,
                    threshold=self._auto_compact_threshold,
                    attempt=self._compaction_attempt,
                    focus=focus or None,
                ),
            ),
        )

    async def _publish_compaction_end(
        self,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        summary: str,
        continuation_message: str,
        pre_tokens: int,
        post_tokens: int,
        llm_tokens_used: int,
        mode: Optional[
            Literal["single", "chunked-proactive", "chunked-reactive"]
        ] = None,
        chunk_count: Optional[int] = None,
        map_phase_seconds: Optional[float] = None,
        reduce_phase_seconds: Optional[float] = None,
    ) -> None:
        """Emit a success event (summarization / manual_compaction / emergency_compaction / pre_retry_compaction)."""
        from xpander_sdk.models.compactization import (
            TaskCompactizationEvent,
            TaskCompactizationOutput,
        )
        from xpander_sdk.models.events import TaskUpdateEventType

        type_map = {
            "auto": "summarization",
            "manual": "manual_compaction",
            "emergency": "emergency_compaction",
            "pre_retry": "pre_retry_compaction",
        }
        await self._push_activity_event(
            event_type=TaskUpdateEventType.TaskCompactization,
            data=TaskCompactizationEvent(
                type=type_map[trigger],
                data=TaskCompactizationOutput(
                    new_task_prompt=continuation_message,
                    task_context=summary,
                    mode=mode,
                    chunk_count=chunk_count,
                    map_phase_seconds=map_phase_seconds,
                    reduce_phase_seconds=reduce_phase_seconds,
                ),
            ),
        )
        logger.info(
            f"[context-optimizer] published compaction events for task {self.task.id} "
            f"(trigger={trigger}, attempt={self._compaction_attempt}, mode={mode}, "
            f"chunks={chunk_count}, map={map_phase_seconds}s, reduce={reduce_phase_seconds}s)"
        )

    async def _publish_compaction_error(
        self,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        error: str,
    ) -> None:
        """Emit a compaction_error event."""
        from xpander_sdk.models.compactization import (
            TaskCompactizationError as CompactionErrorModel,
            TaskCompactizationEvent,
        )
        from xpander_sdk.models.events import TaskUpdateEventType

        await self._push_activity_event(
            event_type=TaskUpdateEventType.TaskCompactization,
            data=TaskCompactizationEvent(
                type="compaction_error",
                data=CompactionErrorModel(
                    trigger=trigger,
                    error=error,
                    attempt=self._compaction_attempt,
                ),
            ),
        )

    async def _publish_compaction_progress(
        self,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        percent: float,
        label: str = "Compacting context",
        detail: Optional[str] = None,
    ) -> None:
        """Emit a customer-facing ``compaction_progress`` activity event.

        Only ``percent`` + ``label`` + ``detail`` are sent over the wire.
        Callers should NOT invoke this directly for rate-limited updates;
        go through ``_emit_progress`` which applies the monotonic /
        cadence guards.
        """
        from xpander_sdk.models.compactization import (
            TaskCompactizationEvent,
            TaskCompactizationProgress,
        )
        from xpander_sdk.models.events import TaskUpdateEventType

        await self._push_activity_event(
            event_type=TaskUpdateEventType.TaskCompactization,
            data=TaskCompactizationEvent(
                type="compaction_progress",
                data=TaskCompactizationProgress(
                    trigger=trigger,
                    attempt=self._compaction_attempt,
                    percent=round(max(0.0, min(100.0, percent)), 1),
                    label=label,
                    detail=detail,
                ),
            ),
        )

    async def apublish_context_status(self, messages: List[Message]) -> "Optional[Any]":
        """Force-emit a context_status snapshot and return the payload; for mid-loop hooks (tool-call completions, sub-execution boundaries) where the caller wants to refresh the indicator without changing the compacting flag."""
        if not messages:
            return None
        return await self._publish_context_status(messages, force=True)

    async def apublish_final_context_status(
        self, messages: List[Message]
    ) -> "Optional[Any]":
        """Force-emit a final context_status with compacting cleared; called at agno run end (RunCompleted/Cancelled/Error) so the indicator settles on post-final-message state."""
        if not messages:
            return None
        self._compacting = False
        return await self._publish_context_status(messages, force=True)

    async def _publish_context_status(
        self,
        messages: List[Message],
        *,
        force: bool = False,
        estimated: Optional[int] = None,
    ) -> "Optional[Any]":
        """Emit a context_status snapshot for the chat UI indicator; returns the payload (or None if unconfigured / estimate failed)."""
        if not self.agent or not self.task:
            return None

        from xpander_sdk.models.context_status import ContextStatus
        from xpander_sdk.models.events import TaskUpdateEventType

        try:
            if estimated is None:
                estimated = self._estimate_tokens(messages)
        except Exception as exc:
            logger.debug(f"[context-optimizer] context_status estimate failed: {exc}")
            return None

        window = max(1, int(self.context_window))
        pct = max(0.0, min(100.0, (estimated / window) * 100.0))
        # throttle: skip re-emitting when the integer percent hasn't moved
        if not force and int(pct) == self._last_emitted_status_pct:
            return None
        self._last_emitted_status_pct = int(pct)

        payload = ContextStatus(
            estimated_tokens=estimated,
            context_window=window,
            percent=round(pct, 1),
            auto_compact_threshold=self._auto_compact_threshold,
            emergency_threshold=self._emergency_compact_threshold,
            compacting=self._compacting,
        )

        coro = self._push_activity_event(
            event_type=TaskUpdateEventType.ContextStatus,
            data=payload,
        )
        try:
            task = asyncio.create_task(coro)
        except RuntimeError as exc:
            logger.debug(f"[context-optimizer] context_status schedule failed: {exc}")
            coro.close()
            return payload

        def _log_status_task_exception(t: "asyncio.Task[Any]") -> None:
            if t.cancelled():
                return
            exc = t.exception()
            if exc is not None:
                logger.debug(
                    f"[context-optimizer] context_status publish failed: {exc}"
                )

        task.add_done_callback(_log_status_task_exception)
        return payload

    # Progress-emission rate-limiter state. Reset at the start of every
    # ``layer_2_auto_compact`` call by ``_reset_progress_state``.
    _progress_last_percent: float = field(default=-1.0, init=False, repr=False)
    _progress_last_label: str = field(default="", init=False, repr=False)
    _progress_last_detail: Optional[str] = field(default=None, init=False, repr=False)
    _progress_last_ts: float = field(default=0.0, init=False, repr=False)

    def _reset_progress_state(self) -> None:
        """Reset the progress rate-limiter for a fresh compaction attempt."""
        self._progress_last_percent = -1.0
        self._progress_last_label = ""
        self._progress_last_detail = None
        self._progress_last_ts = 0.0

    async def _emit_progress(
        self,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        percent: float,
        label: str = "Compacting context",
        detail: Optional[str] = None,
        force: bool = False,
    ) -> None:
        """Rate-limited + monotonic wrapper around ``_publish_compaction_progress``.

        Emits only when at least one of the following is true:
            * ``force`` is True
            * it's the first emit for this attempt (no prior value)
            * ``percent`` advanced by >= 5 since the last emit
            * 2 seconds have passed since the last emit
            * ``label`` or ``detail`` changed

        ``percent`` is clamped to the last-seen value so the user never sees
        it go backwards even if an out-of-order phase call tries to lower it.
        """
        import time as _time

        clamped = max(0.0, min(100.0, float(percent)))
        if self._progress_last_percent >= 0 and clamped < self._progress_last_percent:
            clamped = self._progress_last_percent

        now = _time.monotonic()
        label_changed = label != self._progress_last_label
        detail_changed = detail != self._progress_last_detail
        first = self._progress_last_percent < 0
        percent_changed = clamped - max(self._progress_last_percent, 0.0) >= 5.0
        stale = (now - self._progress_last_ts) >= 2.0 and self._progress_last_ts > 0

        if not (
            force
            or first
            or label_changed
            or detail_changed
            or percent_changed
            or stale
        ):
            return

        self._progress_last_percent = clamped
        self._progress_last_label = label
        self._progress_last_detail = detail
        self._progress_last_ts = now

        try:
            await self._publish_compaction_progress(
                trigger=trigger,
                percent=clamped,
                label=label,
                detail=detail,
            )
        except Exception as exc:
            logger.warning(f"[context-optimizer] failed to emit progress event: {exc}")

    # ------------------------------------------------------------------ #
    #  LLM call helpers (single call + chunked map-reduce)
    # ------------------------------------------------------------------ #

    def _resolve_compaction_model(self) -> Any:
        """Return the resolved model to use for compaction LLM calls.

        Prefers the dedicated ``compaction_model`` (PRO-1654) and falls back to
        the agent's own ``model``. Caches the ``get_model``-resolved instance
        back onto whichever field it came from so repeated calls skip resolution.
        """
        if self.compaction_model is not None:
            self.compaction_model = get_model(self.compaction_model)
            return self.compaction_model
        self.model = get_model(self.model)
        return self.model

    async def _run_llm_compaction_call(
        self,
        system_prompt: str,
        user_prompt: str,
        run_metrics: Optional["RunMetrics"] = None,
        progress_label: str = "layer 2",
        trigger: Optional[Literal["auto", "manual", "emergency", "pre_retry"]] = None,
        percent_start: Optional[float] = None,
        percent_end: Optional[float] = None,
        progress_detail: Optional[str] = None,
    ) -> tuple:
        """Run a single streaming LLM call and return ``(text, in_tok, out_tok)``.

        Used by both the regular L2 single-shot path and each map/reduce step
        of the chunked compaction path. Raises on provider errors so callers
        can decide whether to fall back to chunked compaction.

        When ``trigger``, ``percent_start`` and ``percent_end`` are provided,
        emits sparse customer-facing ``compaction_progress`` events mapped
        linearly from a rough output-char estimate into the
        ``[percent_start, percent_end)`` range. Cadence + monotonic guards
        are enforced by ``_emit_progress``.
        """
        import time
        from agno.models.response import ModelResponse, ModelResponseEvent

        model = self._resolve_compaction_model()
        if not model:
            raise RuntimeError("No model available for compaction")

        content_parts: List[str] = []
        input_tokens = 0
        output_tokens = 0
        cache_read_tokens = 0
        cache_write_tokens = 0
        streamed_chars = 0
        _PROGRESS_LOG_INTERVAL = 2_000
        _next_progress_log = _PROGRESS_LOG_INTERVAL

        messages = [
            Message(role="system", content=system_prompt),
            Message(role="user", content=user_prompt),
        ]

        prompt_chars = len(system_prompt) + len(user_prompt)
        start_ts = time.monotonic()
        first_token_ts: Optional[float] = None
        logger.info(
            f"[context-optimizer] {progress_label}: → LLM call starting "
            f"(model={getattr(model, 'id', '?')}, prompt_chars={prompt_chars:,})"
        )

        # Coarse target used purely to interpolate the percent inside the
        # caller-requested [percent_start, percent_end) window. We intentionally
        # do NOT emit streaming rates or char counts to the wire.
        emit_progress = (
            trigger is not None
            and percent_start is not None
            and percent_end is not None
            and percent_end > percent_start
        )
        est_output_chars = max(500, int(prompt_chars * 0.2)) if emit_progress else 0

        async for chunk in model.aresponse_stream(messages=messages):
            if not isinstance(chunk, ModelResponse):
                continue
            if (
                chunk.event == ModelResponseEvent.assistant_response.value
                and chunk.content
            ):
                text = str(chunk.content)
                if first_token_ts is None:
                    first_token_ts = time.monotonic()
                    logger.info(
                        f"[context-optimizer] {progress_label}: first token "
                        f"(ttft={first_token_ts - start_ts:.2f}s)"
                    )
                content_parts.append(text)
                streamed_chars += len(text)
                if streamed_chars >= _next_progress_log:
                    elapsed = time.monotonic() - start_ts
                    rate = streamed_chars / elapsed if elapsed > 0 else 0
                    logger.info(
                        f"[context-optimizer] {progress_label}: streaming "
                        f"{streamed_chars:,} chars ({rate:,.0f} ch/s, elapsed={elapsed:.1f}s)"
                    )
                    _next_progress_log = streamed_chars + _PROGRESS_LOG_INTERVAL
                # Sparse, rate-limited customer-facing progress event.
                if emit_progress:
                    span = percent_end - percent_start  # type: ignore[operator]
                    frac = (
                        min(1.0, streamed_chars / est_output_chars)
                        if est_output_chars
                        else 0.0
                    )
                    pct = percent_start + span * frac  # type: ignore[operator]
                    await self._emit_progress(
                        trigger=trigger,  # type: ignore[arg-type]
                        percent=pct,
                        detail=progress_detail,
                    )
            if chunk.event == ModelResponseEvent.model_request_completed.value:
                input_tokens = chunk.input_tokens or 0
                output_tokens = chunk.output_tokens or 0
                # Provider prompt-cache counts for this compaction call (reporting
                # only). The compaction model uses the same provider caching as the
                # main model — we never cache anything ourselves here.
                cache_read_tokens = getattr(chunk, "cache_read_tokens", 0) or 0
                cache_write_tokens = getattr(chunk, "cache_write_tokens", 0) or 0

        summary = "".join(content_parts)
        elapsed = time.monotonic() - start_ts

        if run_metrics is not None and (input_tokens or output_tokens):
            self._accumulate_run_metrics(
                run_metrics,
                input_tokens,
                output_tokens,
                cache_read_tokens,
                cache_write_tokens,
            )

        logger.info(
            f"[context-optimizer] {progress_label}: ← LLM call done "
            f"(in={input_tokens:,} tok, out={output_tokens:,} tok, "
            f"summary={len(summary):,} chars, elapsed={elapsed:.1f}s)"
        )
        return summary, input_tokens, output_tokens

    def _accumulate_run_metrics(
        self,
        run_metrics: "RunMetrics",
        input_tokens: int,
        output_tokens: int,
        cache_read_tokens: int = 0,
        cache_write_tokens: int = 0,
    ) -> None:
        """Add compaction-call token usage to the run's compression metrics."""
        from agno.metrics import ModelType, ModelMetrics

        if run_metrics.details is None:
            run_metrics.details = {}

        # Attribute usage to the model actually called — same source of truth as
        # the call sites (the resolver), so metrics can't drift from the call path.
        metrics_model = self._resolve_compaction_model()
        model_id = metrics_model.id
        model_provider = metrics_model.get_provider()
        model_metrics = ModelMetrics(
            id=model_id,
            provider=model_provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
        )
        _type_key = ModelType.COMPRESSION_MODEL.value
        entries = run_metrics.details.get(_type_key)
        if entries is None:
            run_metrics.details[_type_key] = [model_metrics]
        else:
            for entry in entries:
                if entry.id == model_id and entry.provider == model_provider:
                    entry.accumulate(model_metrics)
                    break
            else:
                entries.append(model_metrics)

        run_metrics.input_tokens += input_tokens
        run_metrics.output_tokens += output_tokens
        run_metrics.total_tokens += input_tokens + output_tokens
        run_metrics.cache_read_tokens += cache_read_tokens
        run_metrics.cache_write_tokens += cache_write_tokens

    # -- main entry point ----------------------------------------------- #

    async def layer_2_auto_compact(
        self,
        messages: List[Message],
        run_metrics: Optional["RunMetrics"] = None,
        custom_instructions: str = "",
        trigger: Literal["auto", "manual", "emergency", "pre_retry"] = "auto",
    ) -> None:
        """Summarise the full conversation into a structured working state.

        Replaces the context window contents: clears all conversation messages
        but preserves system messages (agent instructions, tool descriptions),
        then appends the compacted summary as a continuation message.

        On failure the list is left untouched so the agent can continue with
        full context.

        If the conversation is too large for a single compaction call — either
        detected proactively (``pre_tokens > chunked_compact_threshold``) or
        reactively (the provider returns a context-overflow 400) — this method
        falls back to ``_layer_2_chunked_compact`` which does map-reduce
        summarisation over message chunks.
        """
        # Circuit breaker guard (emergency and pre_retry bypass this)
        if (
            trigger not in ("emergency", "pre_retry")
            and self._auto_compact_consecutive_failures
            >= MAX_CONSECUTIVE_COMPACT_FAILURES
        ):
            logger.warning(
                f"[context-optimizer] circuit breaker open "
                f"({self._auto_compact_consecutive_failures} consecutive failures) — skipping"
            )
            return

        # ---- Robust-L2 loop guards --------------------------------- #
        # Skip the guards entirely when finalize is already active —
        # we're on the way out, no point compacting again.
        if FINALIZE_MODE_ENABLED and is_finalize_active(self):
            logger.info("[context-optimizer] finalize-only mode active; skipping L2")
            return

        # Per-task cap. Emergency bypasses (true ceiling); everything
        # else trips the cap and transitions to Finalize-Only.
        if (
            FINALIZE_MODE_ENABLED
            and trigger != "emergency"
            and self._compactions_this_task >= MAX_COMPACTIONS_PER_TASK
        ):
            logger.warning(
                f"[context-optimizer] per-task compaction cap hit "
                f"({self._compactions_this_task}/{MAX_COMPACTIONS_PER_TASK}); "
                "entering finalize-only mode"
            )
            enter_finalize_mode(self, reason="compact_loop")
            return

        # Per-arun cap. Manual + emergency bypass (the agent or the
        # safety net asked for it explicitly); auto + pre_retry are
        # bounded.
        if (
            FINALIZE_MODE_ENABLED
            and trigger in ("auto", "pre_retry")
            and self._compactions_this_arun >= MAX_COMPACTIONS_PER_ARUN
        ):
            logger.warning(
                f"[context-optimizer] per-arun compaction cap hit "
                f"({self._compactions_this_arun}/{MAX_COMPACTIONS_PER_ARUN}); "
                "entering finalize-only mode"
            )
            enter_finalize_mode(self, reason="compact_loop")
            return

        # Pre_retry-specific cap — protects against cascading retries
        # (Mode 1 in the failure-mode catalog).
        if (
            FINALIZE_MODE_ENABLED
            and trigger == "pre_retry"
            and self._pre_retry_compactions_this_task >= MAX_PRE_RETRY_COMPACTIONS
        ):
            logger.warning(
                f"[context-optimizer] pre_retry cap hit "
                f"({self._pre_retry_compactions_this_task}/"
                f"{MAX_PRE_RETRY_COMPACTIONS}); entering finalize-only mode"
            )
            enter_finalize_mode(self, reason="pre_retry_exhausted")
            return

        self._compaction_attempt += 1
        pre_tokens = self._estimate_tokens(messages)
        pre_message_count = len(messages)

        # Snapshot deep-planning state (may be None)
        deep_planning_snapshot = None
        if self._has_active_plan():
            deep_planning_snapshot = self.task.deep_planning.model_copy(deep=True)

        logger.info(
            f"[context-optimizer] starting compaction #{self._compaction_attempt} "
            f"(trigger={trigger}, messages={pre_message_count}, est_tokens={pre_tokens:,}, "
            f"threshold={self._auto_compact_threshold:,})"
        )

        self._compacting = True
        await self._publish_context_status(messages, force=True)

        # Publish start event (fire-and-forget)
        await self._publish_compaction_start(
            trigger=trigger,
            pre_tokens=pre_tokens,
            pre_message_count=pre_message_count,
            focus=custom_instructions if trigger == "manual" else "",
        )

        # Reset and emit an initial 0% progress tick so the UI gets a
        # customer-facing "Compacting context" the moment compaction starts,
        # independent of how fast the LLM eventually produces content.
        self._reset_progress_state()
        await self._emit_progress(trigger=trigger, percent=0.0, force=True)

        try:
            compaction_model = self._resolve_compaction_model()
            if not compaction_model:
                raise RuntimeError("No model available for auto-compaction")

            logger.info(
                f"[context-optimizer] layer 2: calling LLM ({compaction_model.id}) "
                f"to summarise {pre_message_count} messages"
            )

            summary: str = ""
            tokens_used = 0
            compact_mode: Literal["single", "chunked-proactive", "chunked-reactive"] = (
                "single"
            )
            telemetry: Dict[str, Any] = {}

            # Proactive chunked path when we already know the conversation is
            # too large for a single call. Saves a wasted round trip.
            should_chunk = (
                self.chunked_compact_threshold is not None
                and pre_tokens >= self.chunked_compact_threshold
            ) or (self._provider_max_tokens and pre_tokens >= self._provider_max_tokens)
            if should_chunk:
                logger.info(
                    f"[context-optimizer] layer 2: proactively chunking "
                    f"(pre_tokens={pre_tokens:,} ≥ threshold={self.chunked_compact_threshold:,})"
                )
                summary, tokens_used, telemetry = await self._layer_2_chunked_compact(
                    messages=list(messages),
                    run_metrics=run_metrics,
                    custom_instructions=custom_instructions,
                    trigger=trigger,
                )
                compact_mode = "chunked-proactive"
            else:
                # Reactive path: attempt the single compaction call and fall
                # back to chunked on context-overflow errors.
                compaction_prompt = self._build_compaction_prompt(
                    messages,
                    custom_instructions=custom_instructions,
                )
                try:
                    await self._emit_progress(
                        trigger=trigger,
                        percent=5.0,
                        detail="Summarizing conversation",
                    )
                    single_start = time.monotonic()
                    summary, in_tok, out_tok = await self._run_llm_compaction_call(
                        system_prompt=AUTO_COMPACT_SYSTEM_PROMPT,
                        user_prompt=compaction_prompt,
                        run_metrics=run_metrics,
                        progress_label="layer 2",
                        trigger=trigger,
                        percent_start=5.0,
                        percent_end=90.0,
                        progress_detail="Summarizing conversation",
                    )
                    telemetry = {
                        "reduce_phase_seconds": round(
                            time.monotonic() - single_start, 3
                        ),
                    }
                    tokens_used = in_tok + out_tok
                except Exception as exc:
                    if not _is_context_overflow_error(exc):
                        raise
                    provider_max = _parse_provider_max_tokens(exc)
                    if provider_max:
                        self._provider_max_tokens = provider_max
                    logger.warning(
                        f"[context-optimizer] layer 2: single call hit context "
                        f"overflow (provider_max={provider_max or 'unknown'}) — "
                        f"retrying with chunked map-reduce compaction"
                    )
                    summary, tokens_used, telemetry = (
                        await self._layer_2_chunked_compact(
                            messages=list(messages),
                            run_metrics=run_metrics,
                            custom_instructions=custom_instructions,
                            trigger=trigger,
                            provider_max_tokens=provider_max,
                        )
                    )
                    compact_mode = "chunked-reactive"

            if not summary:
                raise RuntimeError("LLM returned empty summary")

            # ---- Replace context window in-place ---------------------- #
            # Capture recent tool calls BEFORE clearing — gives the resuming
            # agent a concrete "where I just was" trace alongside the summary.
            recent_actions_block = ""
            authoritative_ledger_block = ""
            ledger = get_attached_ledger(self.task) if LEDGER_ENABLED else None
            if ledger is not None and ledger.entries:
                # Prefer the durable ledger for both the authoritative block
                # (the binding-rule referent) and the narrative recent-actions
                # slot. Falls back to the message-walk legacy renderer when
                # the ledger is empty (e.g. tests with the flag off).
                authoritative_ledger_block = ledger.render_authoritative_block(
                    context_window=self.context_window,
                )
                recent_actions_block = ledger.render_recent(RECENT_ACTIONS_COUNT)
            else:
                recent_actions_block = _build_recent_actions_block(messages)
            backup_pointer = getattr(self, "_pending_backup_pointer", "")
            self._pending_backup_pointer = ""  # reset after use
            continuation_message = CONTINUATION_MESSAGE_TEMPLATE.format(
                summary=summary,
                backup_pointer=backup_pointer,
                recent_actions_block=recent_actions_block,
                authoritative_ledger_block=authoritative_ledger_block,
            )
            self._harvest_skill_playbooks(messages)
            system_messages = [m for m in messages if m.role == "system"]
            messages.clear()
            messages.extend(system_messages)
            pinned_playbooks = self._render_pinned_skill_playbooks()
            if pinned_playbooks:
                messages.append(Message(role="user", content=pinned_playbooks))
            messages.append(Message(role="user", content=continuation_message))

            # Stagnant-compaction warning injection. The post-compaction
            # guard below sets ``_stagnant_warning_pending`` when we hit
            # ``STAGNANT_COMPACTION_WARN_AT`` consecutive no-progress
            # compactions. We consume the flag here on the *next*
            # compaction so the warning lands as a fresh user message in
            # the rebuilt conversation, in front of the LLM at the very
            # next turn.
            if self._stagnant_warning_pending:
                messages.append(
                    Message(
                        role="user",
                        content=(
                            f"⚠️ STAGNATION DETECTED: "
                            f"{self._stagnant_compactions} consecutive context "
                            f"compactions occurred without any new successful "
                            f"tool call in between. You appear to be looping. "
                            f"Try a different tool or different arguments, or "
                            f"report the task as blocked with a short status. "
                            f"The next stagnant compaction will force "
                            f"finalize-only mode and the task will terminate."
                        ),
                    )
                )
                self._stagnant_warning_pending = False

            # ---- Rehydrate deep-planning state ------------------------ #
            if deep_planning_snapshot is not None and self.task:
                self.task.deep_planning = deep_planning_snapshot
                plan_context = self._build_plan_section()
                if plan_context:
                    messages.append(
                        Message(
                            role="user",
                            content=f"Execution plan state after context compaction:\n{plan_context}",
                        )
                    )

            # Final progress tick before the end event so the UI shows
            # 95% → 100% naturally (the end event marks completion).
            await self._emit_progress(
                trigger=trigger,
                percent=95.0,
                detail="Finalizing",
                force=True,
            )

            # ---- Publish activity event (end) ------------------------- #
            post_tokens = self._estimate_tokens(messages)
            await self._publish_compaction_end(
                trigger=trigger,
                summary=summary,
                continuation_message=continuation_message,
                pre_tokens=pre_tokens,
                post_tokens=post_tokens,
                llm_tokens_used=tokens_used,
                mode=compact_mode,
                chunk_count=telemetry.get("chunk_count"),
                map_phase_seconds=telemetry.get("map_phase_seconds"),
                reduce_phase_seconds=telemetry.get("reduce_phase_seconds"),
            )

            self._compacting = False
            await self._publish_context_status(messages, force=True)

            ratio = (
                f"{(1 - post_tokens / pre_tokens) * 100:.1f}%"
                if pre_tokens > 0
                else "N/A"
            )
            logger.info(
                f"[context-optimizer] compaction #{self._compaction_attempt} succeeded "
                f"(trigger={trigger}, mode={compact_mode}, {pre_tokens:,} -> {post_tokens:,} "
                f"tokens, {ratio} reduction, LLM cost: {tokens_used:,} tokens)"
            )

            self._auto_compact_consecutive_failures = 0
            self._emergency_connectivity_failures = 0
            self._post_compact_grace_remaining = 1
            self.stats["compactions"] = self.stats.get("compactions", 0) + 1
            self.stats["compact_tokens_used"] = (
                self.stats.get("compact_tokens_used", 0) + tokens_used
            )

            # ---- Persist action ledger snapshot (best-effort) ------- #
            # Compaction is a natural durability barrier — any process
            # crash after this point should recover with the ledger
            # entries up to here intact. The ledger now routes its
            # appends through ``WorkspaceCache.enqueue_writeback``, so
            # we drain the cache FIRST (covers the common path) then
            # the ledger's own fallback ``_pending_writes`` list.
            if LEDGER_ENABLED and self.task is not None:
                try:
                    await self._workspace_cache.aflush()
                    ledger_to_flush = get_attached_ledger(self.task)
                    if ledger_to_flush is not None:
                        await ledger_to_flush.aflush()
                except Exception as exc:
                    logger.debug(f"[action-ledger] post-compaction flush failed: {exc}")

            # ---- Robust-L2 counters + token-floor guard ------------- #
            self._compactions_this_task += 1
            self._compactions_this_arun += 1
            if trigger == "pre_retry":
                self._pre_retry_compactions_this_task += 1

            if FINALIZE_MODE_ENABLED:
                ledger = get_attached_ledger(self.task) if LEDGER_ENABLED else None
                ledger_seq_now = ledger.seq if ledger else 0
                no_progress = (
                    ledger_seq_now == self._ledger_seq_at_last_compaction
                    and self._compactions_this_task > 1
                )
                if no_progress and post_tokens < TOKEN_FLOOR_PROGRESS_GUARD:
                    logger.warning(
                        f"[context-optimizer] token-floor guard tripped "
                        f"(post_tokens={post_tokens:,} < "
                        f"{TOKEN_FLOOR_PROGRESS_GUARD:,}, ledger_seq stuck at "
                        f"{ledger_seq_now}); entering finalize-only mode"
                    )
                    enter_finalize_mode(self, reason="token_floor")

                # Stagnant-compaction guard. Independent of token level —
                # catches the high-token loop case where each retry adds
                # context faster than compaction shrinks it but no new
                # tool calls land in the ledger. Only auto/emergency
                # triggers count (manual/pre_retry are user-initiated).
                if trigger in ("auto", "emergency"):
                    if no_progress:
                        self._stagnant_compactions += 1
                        if self._stagnant_compactions >= MAX_STAGNANT_COMPACTIONS:
                            logger.warning(
                                f"[context-optimizer] stagnant-compaction guard "
                                f"tripped ({self._stagnant_compactions} consecutive "
                                f"compactions with no new ledger entries, "
                                f"post_tokens={post_tokens:,}); entering "
                                f"finalize-only mode"
                            )
                            enter_finalize_mode(self, reason="stagnant_compactions")
                        elif self._stagnant_compactions >= STAGNANT_COMPACTION_WARN_AT:
                            self._stagnant_warning_pending = True
                    else:
                        self._stagnant_compactions = 0

                self._ledger_seq_at_last_compaction = ledger_seq_now

        except asyncio.CancelledError:
            # Cancellation is structural — never count it as a compaction
            # failure or trigger the failure-counter circuit breaker.
            raise
        except Exception as exc:
            self._auto_compact_consecutive_failures += 1
            if _is_connectivity_error(exc):
                self._emergency_connectivity_failures += 1
            else:
                self._emergency_connectivity_failures = 0
            logger.error(
                f"[context-optimizer] compaction #{self._compaction_attempt} failed "
                f"(trigger={trigger}, consecutive_failures={self._auto_compact_consecutive_failures}/"
                f"{MAX_CONSECUTIVE_COMPACT_FAILURES}, "
                f"connectivity_failures={self._emergency_connectivity_failures}): {exc}"
            )
            await self._publish_compaction_error(trigger=trigger, error=str(exc))
            self._compacting = False
            await self._publish_context_status(messages, force=True)

    # ================================================================== #
    #  Pre-retry helpers
    # ================================================================== #

    def _inject_last_actions_breadcrumb(self, task: "Task") -> None:
        """Render last WRITE/VERIFY ledger entries into ``task.additional_context``.

        Called when pre_retry compaction is skipped (small session,
        evidence-finalize, etc.) so the resumed agent has a concrete
        breadcrumb of what just happened — without it, the next
        ``arun()`` only sees plan-status text and may restart steps
        already done. Strips any prior ``<last_actions>`` block before
        appending so additional_context stays bounded across retries.
        """
        if not LEDGER_ENABLED or task is None:
            return
        ledger = get_attached_ledger(task)
        if ledger is None:
            return
        # Pick last 8 WRITE/VERIFY/PLAN entries — these are the
        # signal-rich ones for "where did I stop".
        from xpander_sdk.models.action_ledger import LedgerEntryClass

        signal_classes = {
            LedgerEntryClass.WRITE,
            LedgerEntryClass.VERIFY,
            LedgerEntryClass.PLAN,
        }
        relevant = [e for e in ledger.entries if e.entry_class in signal_classes]
        if not relevant:
            return
        tail = relevant[-8:]
        rows: List[str] = []
        for e in tail:
            sig = f" signature={e.result_signature}" if e.result_signature else ""
            target = e.target or "—"
            rows.append(
                f"  - seq={e.seq} tool={e.tool_name} class={e.entry_class.value} "
                f"target={target} status={e.status}{sig}"
            )
        block = (
            "\n<last_actions>\n"
            "Breadcrumb of the last successful tool calls before this retry.\n"
            "RESUME from here — do NOT restart steps already recorded below.\n"
            "If a target shows status=ok, the operation completed; continue from\n"
            "the next logical step instead of re-doing it.\n"
            + "\n".join(rows)
            + "\n</last_actions>"
        )
        try:
            existing = task.additional_context or ""
            existing = re.sub(
                r"\n*<last_actions>.*?</last_actions>\n*",
                "\n",
                existing,
                flags=re.DOTALL,
            ).rstrip()
            task.additional_context = existing + "\n\n" + block.lstrip()
            logger.info(
                f"[context-optimizer] injected <last_actions> breadcrumb "
                f"({len(tail)} entries) into task.additional_context"
            )
        except Exception as exc:
            logger.warning(f"[context-optimizer] last-actions inject failed: {exc}")

    # ================================================================== #
    #  Pre-retry session compaction
    # ================================================================== #

    async def acompact_session_for_retry(
        self,
        agno_agent_or_xpander_agent: Any,
        task: "Task",
        custom_instructions: str = "",
    ) -> "CompactRetryResult":
        """Force L2 compaction on the session before a plan retry.

        Consolidates the pre-retry compaction logic used by both the agent-worker
        (mono) and the events_module (SDK).  Does four things:
        1. Backs up the full session to workspace (encrypted) for grep/search.
        2. Forces L2 compaction (replaces context window in-place).
        3. Persists the compacted summary to task.additional_context so the
           fresh retry agent picks it up.
        4. Deletes the old session from DB so the retry starts clean.

        Args:
            custom_instructions: Optional retry-focus guidance forwarded to
                the L2 compaction LLM (rendered after ``Additional focus:`` in
                the user prompt). Lets callers bias the summary toward
                remaining plan tasks / next action without changing the
                shared template used by ``auto`` / ``manual`` / ``emergency``.

        Returns a CompactRetryResult with token usage for billing.
        """
        result = CompactRetryResult()

        # ---- Already finalizing? Bail out -------------------------- #
        # Both the SDK (events_module) and the cloud agent-worker (mono)
        # call this helper. Putting the cross-cutting checks here
        # ensures every harness inherits Robust-L2 behavior without
        # changes on their side.
        if FINALIZE_MODE_ENABLED and is_finalize_active(self):
            logger.info(
                "[context-optimizer] pre-retry: finalize-only already active; skipping"
            )
            return result

        # ---- Robust-L2 evidence-skip (Mode-2 fix, cross-harness) --- #
        # Pre_retry is the most expensive op the optimizer runs (full
        # session reload, encryption, LLM summarize, session delete).
        # If the durable action ledger already shows write+verify pairs
        # covering the small remaining set of plan items, we skip the
        # pre_retry entirely and engage Finalize-Only Mode. The next
        # agno arun() will see finalize state on the optimizer (via
        # ``task._xp_context_optimizer``) and the tool gate will force
        # ``xpfinalize_task`` — which sets ``task.result`` and toggles
        # the remaining plan items, terminating the retry loop in both
        # the SDK and mono harnesses.
        if FINALIZE_MODE_ENABLED and LEDGER_ENABLED:
            ledger = get_attached_ledger(task)
            deep_planning = getattr(task, "deep_planning", None)
            evidence = detect_completion_evidence(ledger, deep_planning)
            uncompleted: List[Any] = []
            if deep_planning and deep_planning.tasks:
                uncompleted = [t for t in deep_planning.tasks if not t.completed]
            if evidence.has_evidence and len(uncompleted) <= 2:
                logger.info(
                    f"[context-optimizer] pre-retry skipped — evidence detected "
                    f"({evidence.rationale}); engaging finalize-only mode"
                )
                enter_finalize_mode(self, reason="evidence", evidence=evidence)
                return result

        # ---- Hard cap on pre_retry compactions per task ------------- #
        # Belt-and-suspenders: the layer_2 guard also checks this, but
        # we short-circuit here too so the session-backup work doesn't
        # run when we've already given up on retry.
        if (
            FINALIZE_MODE_ENABLED
            and self._pre_retry_compactions_this_task >= MAX_PRE_RETRY_COMPACTIONS
        ):
            logger.warning(
                f"[context-optimizer] pre-retry: cap hit "
                f"({self._pre_retry_compactions_this_task}/"
                f"{MAX_PRE_RETRY_COMPACTIONS}); entering finalize-only mode"
            )
            enter_finalize_mode(self, reason="pre_retry_exhausted")
            return result

        # NOTE: the legacy ``<compacted_context>`` substring breaker was
        # removed once the counter-based ``MAX_PRE_RETRY_COMPACTIONS``
        # cap landed plus the dedupe-on-replace logic in step 5b. The
        # old breaker would short-circuit the second legitimate
        # pre_retry — but by then the agent has new messages worth
        # summarizing, and the dedupe writes the fresh summary in place
        # rather than accumulating, so re-running is safe.

        try:
            # ---- 0. Snapshot deep-planning state (must survive) -------- #
            deep_planning_snapshot = None
            if task.deep_planning:
                deep_planning_snapshot = task.deep_planning.model_copy(deep=True)

            # ---- 1. Load session from DB ------------------------------ #
            agent_obj = agno_agent_or_xpander_agent
            session = None

            # Agno Agent path (mono) — has session_id attr from agno
            if hasattr(agent_obj, "session_id") and hasattr(agent_obj, "db"):
                from agno.agent._session import aget_session as agno_aget_session

                session = await agno_aget_session(agent_obj, session_id=task.id)
            # xpander Agent path (SDK) — use the xpander agent's method
            elif hasattr(agent_obj, "aget_session"):
                session = await agent_obj.aget_session(session_id=task.id)

            if not session:
                logger.warning(
                    "[context-optimizer] pre-retry: no session found in DB — skipping"
                )
                return result

            messages = session.get_messages()
            if not messages or len(messages) < 3:
                logger.info(
                    "[context-optimizer] pre-retry: too few messages to compact — skipping"
                )
                return result

            # ---- Token-budget guard: skip when session is small ------- #
            # Pre_retry pays for an LLM summarize round-trip every time
            # it fires. When the session is well below the auto-compact
            # threshold, the next arun() can fit the full conversation
            # — paying for a compact just to "be safe" is wasteful.
            # Common production trigger: agent stopped on output-cap
            # (8K output tokens), not on context pressure. Plan retry
            # still runs; we just skip the compaction step.
            est_tokens = self._estimate_tokens(messages)
            if est_tokens < MIN_TOKENS_FOR_PRE_RETRY_COMPACT:
                logger.info(
                    f"[context-optimizer] pre-retry: session healthy "
                    f"(est_tokens={est_tokens:,} < "
                    f"{MIN_TOKENS_FOR_PRE_RETRY_COMPACT:,}) — skipping compaction, "
                    "letting plan-retry continue with full session"
                )
                # Even when compaction is skipped, surface a
                # ``<last_actions>`` breadcrumb from the action ledger
                # into ``task.additional_context`` so the resumed agent
                # knows where it stopped and doesn't restart from
                # scratch (e.g. re-scrape completed steps). Without
                # this, a fresh ``arun()`` only sees the plan-status
                # text — no info about the last successful tool call.
                self._inject_last_actions_breadcrumb(task)
                return result

            logger.info(
                f"[context-optimizer] pre-retry: compacting session for task {task.id} "
                f"({len(messages)} messages, est_tokens={est_tokens:,})"
            )

            # ---- 2. Backup full session to workspace (non-blocking) ----- #
            # Skipped when workspace is disabled — backup_path stays None and the
            # continuation pointer below is left empty. Summarisation still runs.
            backup_path = None
            if self._workspace_enabled:
                try:
                    session_json = json.dumps(
                        [m.to_dict() for m in messages],
                        default=str,
                        ensure_ascii=False,
                    )
                    stable_path = f"CONTEXT_OPTIMIZATION/session_backup_{task.id}.xp"
                    key = derive_key(
                        org_id=self.agent.configuration.organization_id,
                        agent_id=self.agent.id,
                        task_id=task.id,
                    )
                    encrypted = await aencrypt(session_json, key)
                    client = APIClient(configuration=self.agent.configuration)
                    await client.make_request(
                        path=str(APIRoute.WorkspaceToolInvoke).format(
                            agent_id=self.agent.id,
                            tool_name="file_write",
                        ),
                        method="POST",
                        payload={"path": stable_path, "content": encrypted},
                    )
                    backup_path = stable_path
                    result.backup_path = backup_path
                    logger.info(
                        f"[context-optimizer] pre-retry: session backup saved to {backup_path}"
                    )
                except Exception as exc:
                    logger.warning(
                        f"[context-optimizer] pre-retry: backup failed (non-blocking): {exc}"
                    )

            # ---- 3. Set backup pointer for continuation message ------- #
            if backup_path:
                self._pending_backup_pointer = (
                    f"\n<session_backup>\n"
                    f"Full session transcript backed up to: {backup_path}\n"
                    f"This file is ENCRYPTED at rest. To read it, call "
                    f"`xpworkspace-file-read` with `path={backup_path}` — the "
                    f"file-read tool decrypts it transparently. Do NOT use "
                    f"bash `cat` or `xpworkspace-bash` (those return ciphertext).\n"
                    f"Use this only when the summary above lacks a specific "
                    f"detail you need (exact code, error message verbatim, "
                    f"complete tool output).\n"
                    f"</session_backup>"
                )
            else:
                self._pending_backup_pointer = ""

            # ---- 4. Force L2 compaction with bounded retry ------------ #
            # The LLM call can stall transiently — wrap it in an
            # exp-backoff retry loop so a single slow provider round-trip
            # doesn't abort the whole pre-retry pass (which would skip
            # the additional_context summary write + session delete +
            # deep-planning restore downstream). The explicit
            # ``except asyncio.CancelledError: raise`` ahead of the
            # broad handler makes cancellation pass-through unambiguous
            # regardless of Python-version subclassing rules.
            from agno.models.metrics import RunMetrics

            compact_metrics = RunMetrics()
            compacted_ok = False
            for attempt in range(PRE_RETRY_COMPACT_MAX_ATTEMPTS):
                # Reset metrics each attempt — failed attempts must not
                # bill, and the success path reads compact_metrics below.
                compact_metrics = RunMetrics()
                try:
                    await asyncio.wait_for(
                        self.layer_2_auto_compact(
                            messages,
                            run_metrics=compact_metrics,
                            custom_instructions=custom_instructions,
                            trigger="pre_retry",
                        ),
                        timeout=SESSION_COMPACT_TIMEOUT,
                    )
                    compacted_ok = True
                    break
                except asyncio.CancelledError:
                    raise
                except (asyncio.TimeoutError, Exception) as exc:
                    is_timeout = isinstance(exc, asyncio.TimeoutError)
                    # Context-overflow can't be cleared by re-sending the same
                    # oversized payload — layer_2 already exhausted its chunked
                    # fallback before raising. Bail to plan-retry at once.
                    if not is_timeout and _is_context_overflow_error(exc):
                        logger.error(
                            f"[context-optimizer] pre-retry: compaction hit a "
                            f"context-overflow ({exc}) — not retryable, giving up"
                        )
                        return result
                    last_attempt = attempt == PRE_RETRY_COMPACT_MAX_ATTEMPTS - 1
                    # Deterministic provider errors won't self-heal, so cap them
                    # well below the timeout budget instead of burning all 10x.
                    if (
                        not is_timeout
                        and attempt >= PRE_RETRY_COMPACT_MAX_NONTIMEOUT_ATTEMPTS - 1
                    ):
                        last_attempt = True
                    reason = (
                        f"timed out after {SESSION_COMPACT_TIMEOUT}s"
                        if is_timeout
                        else f"failed: {exc}"
                    )
                    if last_attempt:
                        logger.error(
                            f"[context-optimizer] pre-retry: compaction {reason} "
                            f"(attempt {attempt + 1}/{PRE_RETRY_COMPACT_MAX_ATTEMPTS}, "
                            f"giving up)"
                        )
                        return result
                    delay = min(
                        PRE_RETRY_COMPACT_RETRY_BASE_DELAY * (2**attempt),
                        PRE_RETRY_COMPACT_RETRY_MAX_DELAY,
                    )
                    delay += random.uniform(
                        -PRE_RETRY_COMPACT_RETRY_JITTER * delay,
                        PRE_RETRY_COMPACT_RETRY_JITTER * delay,
                    )
                    logger.warning(
                        f"[context-optimizer] pre-retry: compaction {reason} "
                        f"(attempt {attempt + 1}/{PRE_RETRY_COMPACT_MAX_ATTEMPTS}), "
                        f"retrying in {delay:.1f}s"
                    )
                    await asyncio.sleep(delay)

            if not compacted_ok:
                return result

            # ---- 5. Capture token usage ------------------------------- #
            result.input_tokens = compact_metrics.input_tokens
            result.output_tokens = compact_metrics.output_tokens
            result.total_tokens = compact_metrics.total_tokens

            # ---- 5b. Persist summary to task.additional_context ------- #
            # L2 replaces the context window in-place but does NOT write to
            # additional_context.  For pre-retry we need the summary there
            # because the session gets deleted and the fresh agent rebuilds
            # its context from additional_context.
            try:
                # Extract summary from the continuation message L2 appended
                continuation_msg = next(
                    (
                        m
                        for m in messages
                        if m.role == "user"
                        and m.content
                        and "<session_resume>" in str(m.content)
                    ),
                    None,
                )
                if continuation_msg:
                    # Strip ANY prior <compacted_context>...</compacted_context>
                    # block before appending the fresh one. Repeated retries
                    # used to accumulate stacked blocks, growing
                    # additional_context unbounded and feeding the
                    # cascading-compaction loop. Replace, don't append.
                    import re as _re

                    existing = task.additional_context or ""
                    existing = _re.sub(
                        r"\n*<compacted_context>.*?</compacted_context>\n*",
                        "\n",
                        existing,
                        flags=_re.DOTALL,
                    ).rstrip()
                    task.additional_context = (
                        existing
                        + "\n\n<compacted_context>\n"
                        + str(continuation_msg.content)
                        + "\n</compacted_context>"
                    )
                    logger.info(
                        "[context-optimizer] pre-retry: persisted compaction summary "
                        "to task.additional_context (replaced any prior block)"
                    )
            except Exception as exc:
                logger.warning(
                    f"[context-optimizer] pre-retry: failed to persist summary to task: {exc}"
                )

            # Always inject the structured ``<last_actions>`` breadcrumb
            # alongside the compacted summary. The summary is LLM-prose
            # (lossy); the breadcrumb is the deterministic last-N
            # ledger entries the agent can grep for "where did I stop".
            self._inject_last_actions_breadcrumb(task)

            # ---- 5c. Persist input file URLs (defensive) -------------- #
            # Belt-and-suspenders: even if the retry prompt or summary drops
            # them, the URLs from task.input.files survive in additional_context
            # so the retry agent can still locate the original attachments.
            try:
                input_files = getattr(getattr(task, "input", None), "files", None)
                if input_files and "<task_input_files>" not in (
                    task.additional_context or ""
                ):
                    files_block = "\n".join(f"- {url}" for url in input_files)
                    task.additional_context = (
                        (task.additional_context or "")
                        + "\n\n<task_input_files>\n"
                        + files_block
                        + "\n</task_input_files>"
                    )
                    logger.info(
                        f"[context-optimizer] pre-retry: persisted {len(input_files)} "
                        f"input file URL(s) to task.additional_context"
                    )
            except Exception as exc:
                logger.warning(
                    f"[context-optimizer] pre-retry: failed to persist input files: {exc}"
                )

            # ---- 6. Delete old session so retry starts clean ---------- #
            # The fresh agent will rebuild its system prompt + pick up the
            # summary from additional_context.
            try:
                if hasattr(agent_obj, "session_id") and hasattr(agent_obj, "db"):
                    # Agno Agent path
                    from agno.agent._session import adelete_session

                    await adelete_session(agent_obj, session_id=task.id)
                elif hasattr(agent_obj, "adelete_session"):
                    # xpander Agent path
                    await agent_obj.adelete_session(session_id=task.id)
                logger.info(
                    f"[context-optimizer] pre-retry: deleted old session {task.id}"
                )
            except Exception as exc:
                logger.warning(
                    f"[context-optimizer] pre-retry: session delete failed (non-critical): {exc}"
                )

            # ---- 7. Restore deep-planning state ----------------------- #
            # Deep planning must survive the retry — it tracks plan tasks,
            # completion status, and question state.
            if deep_planning_snapshot is not None:
                task.deep_planning = deep_planning_snapshot
                logger.info(
                    "[context-optimizer] pre-retry: deep planning state preserved"
                )

            result.compacted = True
            logger.info(
                f"[context-optimizer] pre-retry: compaction complete "
                f"(input={result.input_tokens:,}, output={result.output_tokens:,}, "
                f"total={result.total_tokens:,} tokens)"
            )
            return result

        except Exception as exc:
            logger.error(f"[context-optimizer] pre-retry: compaction failed: {exc}")
            # Restore deep planning even on failure
            if deep_planning_snapshot is not None:
                task.deep_planning = deep_planning_snapshot
            return result
