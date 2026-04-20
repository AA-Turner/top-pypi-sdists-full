"""Selective auto-propose runner (#1454).

Shared post-turn orchestration. Both the web chat router and the
interactive CLI REPL invoke ``run_auto_propose(...)`` after a final
assistant turn. The runner:

1. Skips early when ``config.memory.auto_propose.enabled`` is false.
2. Calls :func:`memory_extractor.extract_candidates` to surface durable
   facts from the assistant text.
3. Filters surviving candidates against a per-conversation cooldown
   that suppresses near-immediate restatements of the same fact.
4. Persists each surviving candidate via
   :func:`memory_promotion.propose_candidate` with ``proposer="agent"``.
5. Emits exactly one ``memory.proposed`` lineage entry per successful
   write — single audit-emission site so both interfaces inherit the
   same audit shape automatically.
6. Returns a :class:`AutoProposeResult` describing what landed. Never
   raises: every exception path is captured and reflected in the result
   so the caller can keep streaming the assistant turn.
"""

from __future__ import annotations

import hashlib
import logging
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from . import lineage
from .memory_extractor import extract_candidates
from .memory_promotion import (
    PromotionAgentDisabledError,
    PromotionRateLimitError,
    propose_candidate,
)

if TYPE_CHECKING:
    from ..config import AppConfig
    from ..db import ThreadSafeConnection
    from .ai_service import AIService
    from .audit import AuditWriter
    from .memory_recall import RecalledMemory

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProposedItem:
    """A candidate that was successfully persisted by the runner."""

    fqn: str
    category: str
    content_preview: str  # truncated for inline display


@dataclass
class AutoProposeResult:
    """Outcome of one ``run_auto_propose`` invocation.

    ``reason`` is one of ``"ok" | "disabled" | "no_results" | "failed" |
    "rate_limited" | "agent_disabled" | "empty_input" |
    "cooldown_skipped"``. ``"empty_input"`` and ``"failed"`` come from
    the extractor; the others are runner outcomes. The caller uses
    ``items`` for rendering and the SSE payload; ``reason`` matters for
    tests, debug logging, and deciding whether to render anything at all.

    Note: there is no ``"dedupe_skipped"`` reason today — recall-based
    dedupe happens inside the extractor, so candidates that overlap
    semantically with already-recalled memories never reach this layer
    and are reported as part of ``"no_results"`` from the extractor.
    """

    items: list[ProposedItem] = field(default_factory=list)
    reason: str = "no_results"


class AutoProposeCooldown:
    """Per-conversation deque of recently-proposed content hashes.

    Module-level singleton keeps in-process state across requests. Reset
    on process restart (acceptable for v1 — see plan v3 risks). If a
    conversation is touched concurrently from web + REPL in the same
    process, the cooldown will correctly span both interfaces.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._by_conv: dict[str, deque[str]] = {}

    @staticmethod
    def _hash(content: str) -> str:
        return hashlib.sha256(content.strip().lower().encode("utf-8")).hexdigest()[:16]

    def already_seen(self, conversation_id: str, content: str) -> bool:
        if not conversation_id:
            return False
        h = self._hash(content)
        with self._lock:
            return h in self._by_conv.get(conversation_id, deque())

    def remember(self, conversation_id: str, content: str, *, max_items: int) -> None:
        if not conversation_id:
            return
        h = self._hash(content)
        with self._lock:
            buf = self._by_conv.setdefault(conversation_id, deque(maxlen=max_items))
            if buf.maxlen != max_items:
                # max_items can change if config is reloaded — rebuild deque.
                self._by_conv[conversation_id] = deque(buf, maxlen=max_items)
                buf = self._by_conv[conversation_id]
            buf.append(h)


# Module-level singleton — see class docstring for rationale.
_GLOBAL_COOLDOWN = AutoProposeCooldown()


def get_global_cooldown() -> AutoProposeCooldown:
    """Return the module-level cooldown singleton.

    Tests can construct their own :class:`AutoProposeCooldown` for
    isolation; production callers reuse this singleton so multiple
    request paths (web + REPL) share state for the same conversation.
    """
    return _GLOBAL_COOLDOWN


def _content_preview(content: str, *, max_chars: int = 280) -> str:
    """Truncate content for inline display + SSE payload."""
    text = (content or "").strip().replace("\n", " ")
    if len(text) > max_chars:
        return text[: max_chars - 3] + "..."
    return text


async def run_auto_propose(
    *,
    assistant_text: str,
    ai_service: AIService,
    db: ThreadSafeConnection,
    audit_writer: AuditWriter | None,
    config: AppConfig,
    identity_user_id: str,
    recalled_memories: list[RecalledMemory],
    conversation_id: str,
    message_id: str,
    project_slug: str | None = None,
    cooldown: AutoProposeCooldown | None = None,
) -> AutoProposeResult:
    """Run selective auto-propose for one final assistant turn.

    Returns a non-throwing :class:`AutoProposeResult`. Every exception
    path is logged at debug level and reflected in ``reason``; the
    caller never sees an exception so the assistant turn keeps
    streaming uninterrupted.
    """
    ap_config = config.memory.auto_propose
    if not ap_config.enabled:
        return AutoProposeResult(reason="disabled")

    cd = cooldown if cooldown is not None else _GLOBAL_COOLDOWN

    # 1. Extraction — pure, never raises (extractor wraps its own errors).
    extracted, ext_reason = await extract_candidates(
        assistant_text=assistant_text,
        ai_service=ai_service,
        recalled_memories=recalled_memories,
        config=ap_config,
    )
    if not extracted:
        # ext_reason already conveys disabled / empty_input / no_results / failed
        return AutoProposeResult(reason=ext_reason)

    # 2. Cooldown filter.
    surviving = [c for c in extracted if not cd.already_seen(conversation_id, c.content)]
    if not surviving:
        return AutoProposeResult(reason="cooldown_skipped")

    # 3. Persist each via the governed promotion pipeline.  The runner is
    #    the single audit-emission site — both interfaces (web + CLI)
    #    inherit identical memory.proposed entries by construction.
    persisted: list[ProposedItem] = []
    rate_limited = False
    agent_disabled = False
    cooldown_max = max(1, ap_config.cooldown_turns * max(1, ap_config.max_candidates_per_turn))

    for cand in surviving:
        provenance: dict[str, str | None] = {
            "conversation_id": conversation_id,
            "message_id": message_id,
            "source": "auto_propose",
        }
        try:
            mem = propose_candidate(
                db,
                content=cand.content,
                scope=cand.scope,
                category=cand.category,
                proposer="agent",
                proposer_id=identity_user_id,
                provenance=provenance,
                project_slug=project_slug,
                config=config.memory.promotion,
            )
        except PromotionRateLimitError:
            # Per-conversation cap reached — stop trying for this turn,
            # keep whatever already landed.
            rate_limited = True
            logger.debug("auto_propose: rate-limited for conversation %s", conversation_id)
            break
        except PromotionAgentDisabledError:
            # Agent proposals disabled at the promotion layer — give up
            # on the whole turn, nothing will succeed.
            agent_disabled = True
            logger.debug("auto_propose: agent proposals disabled by config")
            break
        except Exception:
            # Any other failure (DB integrity, validation, network) — skip
            # this candidate, keep going.  We never break the turn.
            logger.debug("auto_propose: propose_candidate failed", exc_info=True)
            continue

        # Audit emission — single site for both interfaces.
        try:
            lineage.emit_memory_promotion(
                audit_writer,
                "proposed",
                fqn=mem["fqn"],
                reviewer_id=identity_user_id,
                details={"proposer": "agent", "auto_propose": True},
            )
        except Exception:
            # Audit failure should never block the propose itself.
            logger.debug("auto_propose: lineage emission failed", exc_info=True)

        cd.remember(conversation_id, cand.content, max_items=cooldown_max)
        persisted.append(
            ProposedItem(
                fqn=mem["fqn"],
                category=cand.category,
                content_preview=_content_preview(cand.content),
            )
        )

    if persisted:
        return AutoProposeResult(items=persisted, reason="ok")
    if rate_limited:
        return AutoProposeResult(reason="rate_limited")
    if agent_disabled:
        return AutoProposeResult(reason="agent_disabled")
    return AutoProposeResult(reason="failed")
