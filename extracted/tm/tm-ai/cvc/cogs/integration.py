"""
cvc.cogs.integration — Wires the Cognition Compiler into the CVC agent loop.

This module provides :class:`CogBridge`, a self-contained facade that
:class:`AgentSession` can instantiate once and then call at two points:

1. **Pre-flight** (before the LLM call in ``run_turn``):
   ``bridge.try_cache(user_input, inputs)`` — returns a cached Cog
   result or *None* when the LLM must be queried.

2. **Post-commit** (after every ``engine.commit`` or ``_auto_commit``):
   ``bridge.on_commit(commit_hash, messages)`` — queues the commit and,
   once the distillation threshold is reached, asynchronously compiles a
   Cog.  The user never types */distill* — it happens automatically.

A manual ``/distill`` command is also provided for power users.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

from cvc.cogs.cache import CogHitResult, CognitiveCache
from cvc.cogs.compiler import CognitionCompiler, load_commit_messages
from cvc.cogs.executor import SafeExecutor
from cvc.cogs.registry import CogRegistry

logger = logging.getLogger("cvc.cogs.integration")

# After this many commits, attempt automatic distillation of the most
# recent commits.  Low threshold → aggressive learning.
AUTO_DISTILL_EVERY = 3


class CogBridge:
    """
    Facade wiring the Cognition Compiler, Cognitive Cache, and Registry
    into the CVC agent loop.

    Parameters
    ----------
    cvc_root:
        Path to the ``.cvc/`` directory.
    llm_caller:
        Async ``(prompt) -> str`` function used by the compiler.
        Typically a thin wrapper around the session's LLM.
    enabled:
        Master kill-switch (set via ``CVC_COGS=0`` env var).
    """

    def __init__(
        self,
        cvc_root: Path,
        llm_caller: Any | None = None,
        *,
        enabled: bool = True,
    ) -> None:
        self.enabled = enabled
        self.cvc_root = cvc_root
        self._llm_caller = llm_caller

        # Core components
        self.registry = CogRegistry(cvc_root)
        self.cache = CognitiveCache(self.registry)
        self.executor = SafeExecutor(timeout_s=10.0)

        # Compiler (lazy — needs llm_caller)
        self._compiler: CognitionCompiler | None = None

        # Commit accumulator for auto-distill
        self._pending_commits: list[dict[str, Any]] = []
        self._total_commits_since_distill = 0

    @property
    def compiler(self) -> CognitionCompiler | None:
        if self._compiler is None and self._llm_caller is not None:
            self._compiler = CognitionCompiler(
                registry=self.registry,
                llm=self._llm_caller,
                executor=self.executor,
            )
        return self._compiler

    def set_llm_caller(self, caller: Any) -> None:
        """Set/replace the LLM caller (e.g. after provider switch)."""
        self._llm_caller = caller
        self._compiler = None  # force re-init

    # ------------------------------------------------------------------
    # 1.  PRE-FLIGHT CACHE CHECK
    # ------------------------------------------------------------------

    async def try_cache(
        self,
        user_input: str,
        *,
        inputs: dict[str, Any] | None = None,
    ) -> CogHitResult | None:
        """
        Check whether a compiled Cog can answer *user_input* without an
        LLM call.  Returns a :class:`CogHitResult` (call ``.execute()``
        on it) or ``None`` when the LLM must be used.
        """
        if not self.enabled:
            return None
        return await self.cache.lookup(
            intent=user_input,
            inputs=inputs or {},
        )

    # ------------------------------------------------------------------
    # 2.  POST-COMMIT HOOK  (auto-distill)
    # ------------------------------------------------------------------

    def on_commit(
        self,
        commit_hash: str,
        messages: list[dict[str, Any]],
        *,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:
        """
        Record a commit for potential distillation. When the pending
        count reaches ``AUTO_DISTILL_EVERY``, schedule a background
        distillation task.
        """
        if not self.enabled:
            return

        self._pending_commits.append(
            {
                "hash": commit_hash,
                "messages": messages,
                "tokens": input_tokens + output_tokens,
            }
        )
        self._total_commits_since_distill += 1

        if self._total_commits_since_distill >= AUTO_DISTILL_EVERY:
            # Schedule async distillation — fire-and-forget
            asyncio.ensure_future(self._auto_distill())
            self._total_commits_since_distill = 0

    async def _auto_distill(self) -> "Cog | None":  # noqa: F821
        """Distill the accumulated pending commits into a Cog."""
        if not self._pending_commits:
            return None
        compiler = self.compiler
        if compiler is None:
            logger.debug("Auto-distill skipped: no LLM caller configured")
            return None

        # Merge all pending message transcripts into one
        all_messages: list[dict[str, Any]] = []
        provenance: list[str] = []
        total_tokens = 0
        for entry in self._pending_commits:
            all_messages.extend(entry["messages"])
            provenance.append(entry["hash"])
            total_tokens += entry.get("tokens", 0)

        # Clear the accumulator BEFORE the async call
        self._pending_commits.clear()

        try:
            cog = await compiler.distill(
                transcript_messages=all_messages,
                provenance=provenance,
                originating_tokens=total_tokens,
            )
            if cog:
                logger.info(
                    "Auto-distilled Cog %s — '%s'",
                    cog.short_id,
                    cog.signature.intent_summary,
                )
            return cog
        except Exception as exc:
            logger.warning("Auto-distillation failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # 3.  MANUAL /distill COMMAND
    # ------------------------------------------------------------------

    async def manual_distill(
        self,
        engine: Any = None,
        *,
        recent_n: int = 5,
    ) -> "Cog | None":  # noqa: F821
        """
        Manually triggered distillation. Reads the last *recent_n*
        commits from the CVC engine and attempts compilation.
        """
        compiler = self.compiler
        if compiler is None:
            return None

        all_messages: list[dict[str, Any]] = []
        provenance: list[str] = []
        total_tokens = 0

        if engine is not None:
            # Use the live engine's log (preferred path)
            try:
                entries = engine.log(limit=recent_n)
            except Exception as exc:
                logger.warning("Failed to read log from engine: %s", exc)
                entries = []

            for entry in entries:
                h = entry.get("hash", "")
                msgs = load_commit_messages(self.cvc_root, h)
                if msgs:
                    all_messages.extend(msgs)
                    provenance.append(h)
        else:
            # Fallback: open DB directly
            try:
                from cvc.core.database import ContextDatabase
                from cvc.core.models import CVCConfig

                config = CVCConfig(
                    cvc_root=self.cvc_root,
                    db_path=self.cvc_root / "cvc.db",
                    objects_dir=self.cvc_root / "objects",
                    branches_dir=self.cvc_root / "branches",
                    chroma_persist_dir=self.cvc_root / "chroma",
                    pageindex_dir=self.cvc_root / "pageindex",
                )
                db = ContextDatabase(config)
                commits = db.index.list_commits(limit=recent_n)
            except Exception as exc:
                logger.warning("Failed to read recent commits: %s", exc)
                return None

            for c in commits:
                h = c.commit_hash
                msgs = load_commit_messages(self.cvc_root, h)
                if msgs:
                    all_messages.extend(msgs)
                    provenance.append(h)

        if not all_messages:
            return None

        try:
            cog = await compiler.distill(
                transcript_messages=all_messages,
                provenance=provenance,
                originating_tokens=total_tokens,
            )
            return cog
        except Exception as exc:
            logger.warning("Manual distillation failed: %s", exc)
            return None

    # ------------------------------------------------------------------
    # 4.  SHADOW MODE — record agreement after LLM responds
    # ------------------------------------------------------------------

    async def record_shadow_agreement(self, cog_id: str, llm_output: str, cog_output: Any) -> bool:
        """
        Compare the LLM's answer to the shadow Cog's answer.  If they
        agree, increment the agreement counter.  Returns ``True`` if
        this call caused the Cog to be promoted.
        """
        # Simple string-similarity check: does LLM output contain the cog output?
        cog_str = str(cog_output).strip()
        agreed = cog_str in llm_output or llm_output.strip() == cog_str
        return await self.cache.record_shadow(cog_id, agreed=agreed)

    # ------------------------------------------------------------------
    # 5.  REPORTING
    # ------------------------------------------------------------------

    def roi_report(self, top_n: int = 5) -> dict[str, Any]:
        """Return the ROI ledger summary."""
        return self.cache.roi_report(top_n=top_n)

    def list_cogs(self) -> list[dict[str, Any]]:
        """Return summary of all registered Cogs."""
        return self.registry.list_summary()
