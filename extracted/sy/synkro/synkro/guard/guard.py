"""PolicyGuard — Real-time policy compliance guard for LLM gateways."""

from __future__ import annotations

import asyncio
import time
from pathlib import Path
from typing import Any

from synkro.guard.types import GuardResult
from synkro.llm.client import LLM
from synkro.remediation.detector import PolicyDetector
from synkro.remediation.types import Violation
from synkro.types.logic_map import LogicMap
from synkro.verify.types import Report, Verdict


class PolicyGuard:
    """Real-time policy compliance guard for LLM gateway/proxy use.

    Load a policy once, then call check() on every agent response.
    Stateless after initialization — check() is a pure function
    with no side effects.

    Supports two modes:
    - **Policy-only**: Checks conversations against extracted policy rules
    - **Policy + SQL**: Also verifies factual claims against database ground truth

    Examples:
        >>> guard = await PolicyGuard.from_policy("Uber expenses max $50/week")
        >>> result = await guard.check_async(messages)
        >>> if not result.passed:
        ...     print(result.issues)

        >>> # With SQL verification
        >>> guard = await PolicyGuard.from_policy(
        ...     policy_text,
        ...     sql_configs="./verifiers/",
        ...     dsn="${DATABASE_URL}",
        ... )

        >>> # From pre-extracted LogicMap
        >>> guard = PolicyGuard(logic_map=logic_map)
    """

    def __init__(
        self,
        logic_map: LogicMap,
        model: str | None = None,
        base_url: str | None = None,
        sql_configs: str | Path | dict | list | None = None,
        dsn: str | None = None,
        concurrency: int = 20,
    ):
        """Initialize PolicyGuard with a pre-extracted LogicMap.

        For most users, prefer PolicyGuard.from_policy() which handles
        extraction automatically.

        Args:
            logic_map: Pre-extracted policy rules (LogicMap)
            model: Model for detection (auto-detected if not specified)
            base_url: Optional API base URL for local providers
            sql_configs: Optional SQL verifier configs (path, dict, or list)
            dsn: Database connection string for SQL verification
            concurrency: Max concurrent checks for batch operations
        """
        from synkro.utils.model_detection import get_default_grading_model

        if model is None:
            model = get_default_grading_model()

        self._logic_map = logic_map
        self._model = model
        self._base_url = base_url
        self._concurrency = concurrency

        # Warm LLM client (reused across all check() calls)
        self._llm = LLM(model=model, base_url=base_url, temperature=0.1)

        # Core detection engine
        self._detector = PolicyDetector(logic_map, llm=self._llm)

        # SQL verification (optional) — store raw configs for verify()
        self._sql_configs = sql_configs
        self._dsn = dsn
        self._verifier_llm = None
        if sql_configs is not None:
            from synkro.verify.llm import VerifierLLM

            self._verifier_llm = VerifierLLM()

    @classmethod
    async def from_policy(
        cls,
        policy: str,
        model: str | None = None,
        base_url: str | None = None,
        sql_configs: str | Path | dict | list | None = None,
        dsn: str | None = None,
        concurrency: int = 20,
    ) -> PolicyGuard:
        """Create a PolicyGuard by extracting rules from a policy document.

        This is the recommended constructor. Extracts the LogicMap
        automatically and returns a ready-to-use guard.

        Args:
            policy: Policy text
            model: Model for detection (auto-detected if not specified)
            base_url: Optional API base URL for local providers
            sql_configs: Optional SQL verifier configs (path, dict, or list)
            dsn: Database connection string for SQL verification
            concurrency: Max concurrent checks for batch operations

        Returns:
            Initialized PolicyGuard ready for check() calls

        Examples:
            >>> guard = await PolicyGuard.from_policy("Max $50 Uber per week")
            >>> guard = await PolicyGuard.from_policy(
            ...     policy_text,
            ...     model="gpt-4o",
            ...     sql_configs="./verifiers/",
            ... )
        """
        from synkro.api import extract_rules_async

        result = await extract_rules_async(policy, model=model, base_url=base_url)

        return cls(
            logic_map=result.logic_map,
            model=model,
            base_url=base_url,
            sql_configs=sql_configs,
            dsn=dsn,
            concurrency=concurrency,
        )

    @classmethod
    def from_policy_sync(
        cls,
        policy: str,
        model: str | None = None,
        base_url: str | None = None,
        sql_configs: str | Path | dict | list | None = None,
        dsn: str | None = None,
        concurrency: int = 20,
    ) -> PolicyGuard:
        """Create a PolicyGuard synchronously. See from_policy for docs."""
        return asyncio.run(cls.from_policy(policy, model, base_url, sql_configs, dsn, concurrency))

    # =========================================================================
    # PROPERTIES
    # =========================================================================

    @property
    def logic_map(self) -> LogicMap:
        """The LogicMap this guard checks against."""
        return self._logic_map

    @property
    def model(self) -> str:
        """The model used for detection."""
        return self._model

    @property
    def has_sql(self) -> bool:
        """True if SQL verification is configured."""
        return self._sql_configs is not None

    @property
    def total_cost(self) -> float:
        """Cumulative LLM cost across all check() calls."""
        return self._llm.total_cost

    @property
    def call_count(self) -> int:
        """Total LLM calls made across all check() calls."""
        return self._llm.call_count

    # =========================================================================
    # SINGLE CHECK
    # =========================================================================

    async def check_async(
        self,
        messages: list[dict[str, Any]],
        trace_id: str | None = None,
    ) -> GuardResult:
        """Check a single conversation for policy violations.

        Stateless — no side effects. Safe to call concurrently.

        Args:
            messages: OpenAI-format chat messages
            trace_id: Optional trace identifier for observability

        Returns:
            GuardResult with pass/fail verdict and details

        Examples:
            >>> result = await guard.check_async(messages)
            >>> if not result.passed:
            ...     log_to_db(result.to_dict())
        """
        start = time.monotonic()

        if trace_id is None:
            trace_id = Violation.generate_id(messages)

        # Run policy detection and SQL verification in parallel
        policy_coro = self._detector.detect_single(messages, trace_id=trace_id)

        if self._sql_configs is not None and self._verifier_llm is not None:
            from synkro.verify.engine import verify as sql_verify

            # Pass raw configs — verify() handles parsing internally
            configs = (
                self._sql_configs
                if isinstance(self._sql_configs, (list, tuple))
                else [self._sql_configs]
            )
            sql_coro = sql_verify(
                *configs,
                messages=messages,
                trace_id=trace_id,
                dsn=self._dsn,
                llm=self._verifier_llm,
            )
            violation, sql_report = await asyncio.gather(policy_coro, sql_coro)
        else:
            violation = await policy_coro
            sql_report = None

        elapsed_ms = (time.monotonic() - start) * 1000
        return self._build_result(
            violation=violation,
            sql_report=sql_report,
            trace_id=trace_id,
            latency_ms=elapsed_ms,
        )

    def check(
        self,
        messages: list[dict[str, Any]],
        trace_id: str | None = None,
    ) -> GuardResult:
        """Check a single conversation (sync wrapper). See check_async."""
        return asyncio.run(self.check_async(messages, trace_id))

    # =========================================================================
    # BATCH CHECK
    # =========================================================================

    async def check_batch_async(
        self,
        traces: list[list[dict[str, Any]]],
        concurrency: int | None = None,
    ) -> list[GuardResult]:
        """Check multiple conversations for policy violations.

        Args:
            traces: List of conversations (each is a list of message dicts)
            concurrency: Max parallel checks (default: self._concurrency)

        Returns:
            List of GuardResult, one per conversation
        """
        effective_concurrency = concurrency or self._concurrency
        semaphore = asyncio.Semaphore(effective_concurrency)

        async def _check_one(msgs: list[dict], idx: int) -> GuardResult:
            async with semaphore:
                return await self.check_async(msgs, trace_id=f"trace_{idx}")

        tasks = [_check_one(msgs, i) for i, msgs in enumerate(traces)]
        return list(await asyncio.gather(*tasks))

    def check_batch(
        self,
        traces: list[list[dict[str, Any]]],
        concurrency: int | None = None,
    ) -> list[GuardResult]:
        """Check multiple conversations (sync wrapper). See check_batch_async."""
        return asyncio.run(self.check_batch_async(traces, concurrency))

    # =========================================================================
    # INTERNAL
    # =========================================================================

    def _build_result(
        self,
        violation: Violation | None,
        sql_report: Report | None,
        trace_id: str,
        latency_ms: float,
    ) -> GuardResult:
        """Merge policy detection + SQL verification into unified GuardResult."""
        issues: list[str] = []
        rules_violated: list[str] = []
        severity = "none"

        # Merge policy detection
        if violation is not None:
            issues.extend(violation.issues)
            rules_violated.extend(violation.rules_violated)
            severity = violation.severity

        # Merge SQL verification
        if sql_report is not None:
            for r in sql_report.results:
                if r.value == Verdict.VIOLATION:
                    issues.append(f"[SQL:{r.name}] {r.comment}")
                    if severity == "none":
                        severity = "high"
                elif r.value == Verdict.ERROR:
                    issues.append(f"[SQL:{r.name}] Error: {r.comment}")

        passed = violation is None and (sql_report is None or sql_report.passed)

        return GuardResult(
            passed=passed,
            trace_id=trace_id,
            violation=violation,
            sql_report=sql_report,
            issues=issues,
            severity=severity,
            rules_violated=rules_violated,
            latency_ms=latency_ms,
            cost=self._llm.total_cost,
        )
