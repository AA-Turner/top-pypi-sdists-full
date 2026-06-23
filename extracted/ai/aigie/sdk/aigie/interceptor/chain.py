"""
InterceptorChain - Orchestrates pre-call and post-call hooks for LLM interception.

The chain manages ordered lists of hooks and executes them with proper
priority ordering and short-circuit logic. The autonomous-mode backend
consultation has been removed; the chain is now purely local and additive.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from aigie.drift.monitor import DriftLevel, DriftMonitor
from aigie.interceptor.protocols import (
    FixAction,
    InterceptionContext,
    InterceptionDecision,
    PostCallHook,
    PostCallResult,
    PreCallHook,
    PreCallResult,
)

if TYPE_CHECKING:
    from aigie.client import Aigie
    from aigie.rules.engine import LocalRulesEngine

logger = logging.getLogger("aigie.interceptor")


@dataclass
class HookEntry:
    """Entry in the hook chain with priority."""

    hook: Any  # PreCallHook or PostCallHook
    priority: int
    name: str
    enabled: bool = True


class InterceptorChain:
    """
    Orchestrates pre-call and post-call hooks for LLM interception.

    Hooks run in priority order (lower = earlier). BLOCK short-circuits the
    chain; MODIFY decisions are aggregated; ALLOW/DEFER continues. The
    autonomous backend consultation path was removed along with the rest of
    the remediation subsystem.
    """

    def __init__(
        self,
        aigie_client: Optional["Aigie"] = None,
        rules_engine: Optional["LocalRulesEngine"] = None,
        local_timeout_ms: float = 5.0,
    ):
        self._aigie = aigie_client
        self._rules_engine = rules_engine
        self._local_timeout_ms = local_timeout_ms

        self._pre_hooks: list[HookEntry] = []
        self._post_hooks: list[HookEntry] = []

        # DriftMonitor stays — local-only drift scoring on post-call.
        self._drift_monitor = DriftMonitor()

        # Statistics
        self._stats = {
            "pre_calls": 0,
            "post_calls": 0,
            "blocks": 0,
            "modifications": 0,
            "errors": 0,
            "total_latency_ms": 0.0,
        }

    def set_aigie_client(self, client: "Aigie") -> None:
        """Set the Aigie client reference."""
        self._aigie = client

    def set_rules_engine(self, engine: "LocalRulesEngine") -> None:
        """Set the local rules engine."""
        self._rules_engine = engine

    def add_pre_hook(
        self,
        hook: PreCallHook,
        priority: int | None = None,
        name: str | None = None,
    ) -> None:
        entry = HookEntry(
            hook=hook,
            priority=priority if priority is not None else getattr(hook, "priority", 50),
            name=name or getattr(hook, "name", hook.__class__.__name__),
        )
        self._pre_hooks.append(entry)
        self._pre_hooks.sort(key=lambda e: e.priority)
        logger.debug(f"Added pre-call hook: {entry.name} (priority: {entry.priority})")

    def add_post_hook(
        self,
        hook: PostCallHook,
        priority: int | None = None,
        name: str | None = None,
    ) -> None:
        entry = HookEntry(
            hook=hook,
            priority=priority if priority is not None else getattr(hook, "priority", 50),
            name=name or getattr(hook, "name", hook.__class__.__name__),
        )
        self._post_hooks.append(entry)
        self._post_hooks.sort(key=lambda e: e.priority)
        logger.debug(f"Added post-call hook: {entry.name} (priority: {entry.priority})")

    def remove_pre_hook(self, name: str) -> bool:
        for i, entry in enumerate(self._pre_hooks):
            if entry.name == name:
                del self._pre_hooks[i]
                return True
        return False

    def remove_post_hook(self, name: str) -> bool:
        for i, entry in enumerate(self._post_hooks):
            if entry.name == name:
                del self._post_hooks[i]
                return True
        return False

    def enable_hook(self, name: str, enabled: bool = True) -> bool:
        for entry in self._pre_hooks + self._post_hooks:
            if entry.name == name:
                entry.enabled = enabled
                return True
        return False

    async def pre_call(self, ctx: InterceptionContext) -> PreCallResult:
        start_time = time.perf_counter()
        self._stats["pre_calls"] += 1

        ctx.context_hash = ctx.compute_context_hash()

        if self._rules_engine:
            try:
                rules_result = await self._run_rules_engine(ctx)
                if rules_result.decision == InterceptionDecision.BLOCK:
                    self._stats["blocks"] += 1
                    return rules_result
            except Exception as e:
                logger.warning(f"Rules engine error: {e}")
                self._stats["errors"] += 1

        aggregated_messages = None
        aggregated_kwargs = None
        all_fixes: list[FixAction] = []
        total_latency = 0.0

        for entry in self._pre_hooks:
            if not entry.enabled:
                continue
            try:
                hook_start = time.perf_counter()
                result = await asyncio.wait_for(
                    entry.hook(ctx),
                    timeout=self._local_timeout_ms / 1000.0,
                )
                hook_latency = (time.perf_counter() - hook_start) * 1000
                total_latency += hook_latency
                result.latency_ms = hook_latency
                result.hook_name = entry.name

                if result.decision == InterceptionDecision.BLOCK:
                    self._stats["blocks"] += 1
                    result.latency_ms = total_latency
                    return result

                if result.decision == InterceptionDecision.MODIFY:
                    self._stats["modifications"] += 1
                    if result.modified_messages:
                        aggregated_messages = result.modified_messages
                    if result.modified_kwargs:
                        aggregated_kwargs = {
                            **(aggregated_kwargs or {}),
                            **result.modified_kwargs,
                        }
                    all_fixes.extend(result.fixes_applied)

            except asyncio.TimeoutError:
                logger.warning(f"Pre-call hook {entry.name} timed out")
                self._stats["errors"] += 1
            except Exception as e:
                logger.error(f"Pre-call hook {entry.name} error: {e}")
                self._stats["errors"] += 1

        total_latency = (time.perf_counter() - start_time) * 1000
        self._stats["total_latency_ms"] += total_latency

        if aggregated_messages or aggregated_kwargs or all_fixes:
            return PreCallResult(
                decision=InterceptionDecision.MODIFY,
                modified_messages=aggregated_messages,
                modified_kwargs=aggregated_kwargs,
                fixes_applied=all_fixes,
                latency_ms=total_latency,
            )

        return PreCallResult(
            decision=InterceptionDecision.ALLOW,
            latency_ms=total_latency,
        )

    async def post_call(self, ctx: InterceptionContext) -> PostCallResult:
        start_time = time.perf_counter()
        self._stats["post_calls"] += 1

        ctx = await self._run_drift_monitor(ctx)

        modified_response = None
        modified_content = None
        all_fixes: list[FixAction] = []
        should_retry = False
        retry_kwargs = None
        total_latency = 0.0

        for entry in self._post_hooks:
            if not entry.enabled:
                continue
            try:
                hook_start = time.perf_counter()
                result = await asyncio.wait_for(
                    entry.hook(ctx),
                    timeout=self._local_timeout_ms / 1000.0,
                )
                hook_latency = (time.perf_counter() - hook_start) * 1000
                total_latency += hook_latency
                result.latency_ms = hook_latency
                result.hook_name = entry.name

                if result.decision == InterceptionDecision.MODIFY:
                    self._stats["modifications"] += 1
                    if result.modified_response:
                        modified_response = result.modified_response
                    if result.modified_content:
                        modified_content = result.modified_content
                    all_fixes.extend(result.fixes_applied)

                if result.should_retry:
                    should_retry = True
                    retry_kwargs = result.retry_kwargs or retry_kwargs

            except asyncio.TimeoutError:
                logger.warning(f"Post-call hook {entry.name} timed out")
                self._stats["errors"] += 1
            except Exception as e:
                logger.error(f"Post-call hook {entry.name} error: {e}")
                self._stats["errors"] += 1

        total_latency = (time.perf_counter() - start_time) * 1000
        self._stats["total_latency_ms"] += total_latency

        if should_retry:
            return PostCallResult(
                decision=InterceptionDecision.RETRY,
                should_retry=True,
                retry_kwargs=retry_kwargs,
                fixes_applied=all_fixes,
                latency_ms=total_latency,
            )

        if modified_response or modified_content or all_fixes:
            return PostCallResult(
                decision=InterceptionDecision.MODIFY,
                modified_response=modified_response,
                modified_content=modified_content,
                fixes_applied=all_fixes,
                latency_ms=total_latency,
            )

        return PostCallResult(
            decision=InterceptionDecision.ALLOW,
            latency_ms=total_latency,
        )

    async def _run_rules_engine(self, ctx: InterceptionContext) -> PreCallResult:
        if not self._rules_engine:
            return PreCallResult.defer()
        try:
            return await self._rules_engine.evaluate(ctx)
        except Exception as e:
            logger.error(f"Rules engine error: {e}")
            return PreCallResult.defer()

    async def _run_drift_monitor(self, ctx: InterceptionContext) -> InterceptionContext:
        try:
            alerts = await self._drift_monitor.check_drift(ctx)
            if not alerts:
                ctx.drift_score = 0.0
            else:
                level_scores = {
                    DriftLevel.NONE: 0.0,
                    DriftLevel.LOW: 0.2,
                    DriftLevel.MODERATE: 0.5,
                    DriftLevel.HIGH: 0.75,
                    DriftLevel.CRITICAL: 1.0,
                }
                max_level = max(alerts, key=lambda a: level_scores.get(a.level, 0.0)).level
                ctx.drift_score = level_scores.get(max_level, 0.0)
        except Exception as e:
            logger.warning(f"DriftMonitor failed: {e}")
            ctx.drift_score = 0.0
        return ctx

    def get_stats(self) -> dict[str, Any]:
        return {
            **self._stats,
            "pre_hooks_count": len(self._pre_hooks),
            "post_hooks_count": len(self._post_hooks),
            "avg_latency_ms": (
                self._stats["total_latency_ms"]
                / max(self._stats["pre_calls"] + self._stats["post_calls"], 1)
            ),
        }

    def reset_stats(self) -> None:
        self._stats = {
            "pre_calls": 0,
            "post_calls": 0,
            "blocks": 0,
            "modifications": 0,
            "errors": 0,
            "total_latency_ms": 0.0,
        }
