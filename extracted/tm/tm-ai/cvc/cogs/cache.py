"""
cvc.cogs.cache — The Cognitive Cache hit loop.

Before any LLM call, the agent can call :meth:`CognitiveCache.lookup` with a
natural-language description of its intent and the concrete inputs.  The cache:

1. Asks the :class:`CogRegistry` for semantically similar Cogs.
2. Filters by cosine threshold, structural input-schema compatibility, and
   per-Cog eligibility (``success_rate_ewma`` and promotion state).
3. Returns the best qualifying :class:`CogHitResult` — a deferred handle
   whose :meth:`CogHitResult.execute` method runs the Cog in the sandbox.

Unpromoted (fresh) Cogs are returned with ``is_shadow=True``.  The caller is
expected to compare the Cog's output against a parallel LLM call for the
first ``promotion_trials`` invocations and promote the Cog via
:meth:`CognitiveCache.record_shadow` when agreement is reached.  This is
Voyager's self-verification loop lifted to the systems level.

Every cache hit updates the Cog's telemetry (invocations, success_rate_ewma,
tokens_saved_cumulative), which powers the Token-ROI dashboard.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from cvc.cogs.executor import ExecutionResult, SafeExecutor
from cvc.cogs.models import Cog
from cvc.cogs.registry import CogRegistry

logger = logging.getLogger("cvc.cogs.cache")


@dataclass
class CacheDecision:
    """Non-executing summary of a cache lookup (useful for diagnostics/logging)."""

    cog_id: str
    distance: float
    is_shadow: bool
    reason: str = "hit"


@dataclass
class CogHitResult:
    """A deferred cache hit bound to a specific Cog and inputs."""

    cog: Cog
    distance: float
    inputs: dict[str, Any]
    is_shadow: bool
    _cache: "CognitiveCache" = field(repr=False)

    async def execute(self) -> ExecutionResult:
        result = await self._cache.executor.execute(self.cog, self.inputs)
        if result.ok:
            await self._cache.record_hit(
                self.cog.cog_id, success=True, tokens_saved=self.cog.originating_tokens
            )
        else:
            await self._cache.record_hit(
                self.cog.cog_id,
                success=False,
                tokens_saved=0,
                failure_cause=result.error,
            )
        return result


class CognitiveCache:
    """Pre-flight Cog lookup + ROI accounting."""

    def __init__(
        self,
        registry: CogRegistry,
        executor: SafeExecutor | None = None,
        *,
        max_distance: float = 0.12,
        min_success_rate: float = 0.8,
        require_promoted: bool = True,
        promotion_trials: int = 3,
        promotion_agreement: int = 2,
    ) -> None:
        self.registry = registry
        self.executor = executor or SafeExecutor(timeout_s=5.0)
        self.max_distance = max_distance
        self.min_success_rate = min_success_rate
        self.require_promoted = require_promoted
        self.promotion_trials = max(1, promotion_trials)
        self.promotion_agreement = max(1, promotion_agreement)

    # -- lookup ------------------------------------------------------------

    async def lookup(
        self,
        intent: str,
        inputs: dict[str, Any] | None = None,
        *,
        allow_shadow: bool = True,
    ) -> CogHitResult | None:
        """
        Return the best qualifying Cog hit, or None.

        Notes
        -----
        * ``intent`` is an English description of what the agent is trying
          to accomplish. It is embedded and compared against Cog signatures.
        * ``inputs`` is the concrete keyword payload that will be handed to
          the Cog body on execution. When absent, schema matching is skipped.
        * If the best match is eligible but not promoted, the result is
          returned with ``is_shadow=True`` so the caller knows to dual-run
          against the LLM for verification.
        """
        inputs = inputs or {}
        candidates = self.registry.lookup_candidates(intent, n=5)
        for cog, distance in candidates:
            if distance > self.max_distance:
                continue
            if inputs and not self.registry.schema_matches(cog, inputs):
                continue
            eligible_promoted = cog.is_eligible_for_cache(
                min_success_rate=self.min_success_rate, require_promoted=True
            )
            if eligible_promoted:
                return CogHitResult(
                    cog=cog,
                    distance=distance,
                    inputs=inputs,
                    is_shadow=False,
                    _cache=self,
                )
            # Unpromoted but otherwise eligible -> shadow candidate.
            if allow_shadow and cog.is_eligible_for_cache(
                min_success_rate=self.min_success_rate,
                require_promoted=False,
            ):
                return CogHitResult(
                    cog=cog,
                    distance=distance,
                    inputs=inputs,
                    is_shadow=True,
                    _cache=self,
                )
        return None

    # -- telemetry ---------------------------------------------------------

    async def record_hit(
        self,
        cog_id: str,
        *,
        success: bool,
        tokens_saved: int,
        failure_cause: str = "",
    ) -> None:
        cog = self.registry.get(cog_id)
        if cog is None:
            return
        if success:
            cog.telemetry.record_success(tokens_saved)
        else:
            cog.telemetry.record_failure(failure_cause or "unknown")
        self.registry.update_telemetry(cog)

    async def record_shadow(
        self,
        cog_id: str,
        *,
        agreed: bool,
    ) -> bool:
        """
        Record a shadow-mode trial. Returns ``True`` if the Cog was promoted
        on this call (first time the agreement threshold was reached).
        """
        cog = self.registry.get(cog_id)
        if cog is None:
            return False
        cog.telemetry.record_shadow(agreed)
        promoted_now = False
        if (
            not cog.telemetry.promoted
            and cog.telemetry.shadow_runs >= self.promotion_trials
            and cog.telemetry.shadow_agreements >= self.promotion_agreement
        ):
            cog.telemetry.promoted = True
            promoted_now = True
        self.registry.update_telemetry(cog)
        return promoted_now

    def force_promote(self, cog_id: str) -> bool:
        """Mark a Cog as promoted without shadow trials (manual approval)."""
        cog = self.registry.get(cog_id)
        if cog is None:
            return False
        if cog.telemetry.promoted:
            return False
        cog.telemetry.promoted = True
        self.registry.update_telemetry(cog)
        return True

    # -- ROI ---------------------------------------------------------------

    def roi_report(self, *, top_n: int = 10) -> dict[str, Any]:
        """Aggregate the Token-ROI ledger across all Cogs in the registry."""
        summaries = self.registry.list_summary()
        total_saved = sum(int(s.get("tokens_saved_cumulative", 0)) for s in summaries)
        total_invocations = sum(int(s.get("invocations", 0)) for s in summaries)
        promoted = sum(1 for s in summaries if s.get("promoted"))
        ranked = sorted(
            summaries,
            key=lambda s: int(s.get("tokens_saved_cumulative", 0)),
            reverse=True,
        )
        return {
            "total_cogs": len(summaries),
            "promoted_cogs": promoted,
            "total_invocations": total_invocations,
            "tokens_saved_cumulative": total_saved,
            "top": ranked[:top_n],
        }
