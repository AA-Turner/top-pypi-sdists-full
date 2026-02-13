"""Tests for PolicyGuard verification API.

Unit tests for GuardResult (no LLM calls) + integration tests using
Cerebras gpt-oss-120b for real PolicyGuard checks.

Run: source .env && .venv/bin/python -m pytest tests/test_guard.py -v
"""

import json
import os

import pytest

from synkro.guard import GuardResult, PolicyGuard
from synkro.remediation.types import Violation
from synkro.types.logic_map import LogicMap, Rule, RuleCategory
from synkro.verify.types import Report, Result, Verdict

# ---------------------------------------------------------------------------
# Skip all integration tests if CEREBRAS_API_KEY is missing
# ---------------------------------------------------------------------------

CEREBRAS_MODEL = "cerebras/gpt-oss-120b"

requires_cerebras = pytest.mark.skipif(
    not os.getenv("CEREBRAS_API_KEY"),
    reason="CEREBRAS_API_KEY not set",
)

# ---------------------------------------------------------------------------
# Policy text used across all integration tests
# ---------------------------------------------------------------------------

EXPENSE_POLICY = """
Company Expense Policy (effective 2024):

1. All employee expense claims must include a receipt.
2. Individual meal expenses are capped at $50 per person.
3. Uber/Lyft rides for business travel are limited to $30 per trip.
4. Any single expense over $100 requires prior manager approval.
5. Alcohol purchases are never reimbursable.
6. Employees may expense up to $200/month on professional development (books, courses).
7. Travel between offices is reimbursed at the IRS mileage rate.
8. Hotel stays require booking through the company travel portal.
"""

# ---------------------------------------------------------------------------
# Test conversations
# ---------------------------------------------------------------------------

COMPLIANT_MESSAGES = [
    {"role": "user", "content": "I had a $35 lunch with a client. I have the receipt. Can I expense it?"},
    {
        "role": "assistant",
        "content": (
            "Yes, a $35 meal expense is within the $50 per-person cap. "
            "Please submit your receipt through the expense portal and it will be approved."
        ),
    },
]

VIOLATING_MESSAGES = [
    {"role": "user", "content": "I took a $75 Uber to the airport. Can I expense it?"},
    {
        "role": "assistant",
        "content": (
            "Sure, go ahead and submit that $75 Uber ride. "
            "It will be reimbursed in your next paycheck."
        ),
    },
]

ALCOHOL_VIOLATION_MESSAGES = [
    {"role": "user", "content": "I bought a $40 bottle of wine for a team dinner. Can I expense this?"},
    {
        "role": "assistant",
        "content": (
            "Absolutely! Submit the receipt and it will be reimbursed as a team meal expense."
        ),
    },
]

EDGE_CASE_MESSAGES = [
    {"role": "user", "content": "I spent exactly $50 on lunch. Is that ok to expense?"},
    {
        "role": "assistant",
        "content": (
            "$50 is exactly at the per-person meal cap, so yes, that is within policy. "
            "Please submit your receipt."
        ),
    },
]


# ---------------------------------------------------------------------------
# Helpers for unit tests
# ---------------------------------------------------------------------------


def _make_logic_map() -> LogicMap:
    """Create a minimal LogicMap for unit tests."""
    return LogicMap(
        rules=[
            Rule(
                rule_id="R001",
                text="Expenses over $50 require manager approval",
                condition="expense amount > $50",
                action="require manager approval",
                dependencies=[],
                category=RuleCategory.CONSTRAINT,
            ),
        ],
        root_rules=["R001"],
    )


def _make_violation(trace_id: str = "test-trace") -> Violation:
    """Create a Violation for unit tests."""
    return Violation(
        id="v_abc123_0001",
        trace_id=trace_id,
        name="policy_compliance",
        score=0.8,
        value="violation",
        comment="Response approved $75 expense without manager approval",
        rules_violated=["R001"],
        issues=["Approved expense over $50 without manager approval"],
        severity="high",
        trace=[
            {"role": "user", "content": "Can I expense $75 for dinner?"},
            {"role": "assistant", "content": "Sure, that's approved!"},
        ],
    )


def _make_sql_report(passed: bool = True, trace_id: str = "test-trace") -> Report:
    """Create a SQL Report for unit tests."""
    if passed:
        return Report(
            trace_id=trace_id,
            response="",
            results=[Result(name="check", score=1.0, value=Verdict.PASS, comment="OK")],
        )
    return Report(
        trace_id=trace_id,
        response="",
        results=[
            Result(name="check", score=0.0, value=Verdict.VIOLATION, comment="Bad"),
        ],
    )


# ===========================================================================
# UNIT TESTS — GuardResult (no LLM calls)
# ===========================================================================


class TestGuardResult:
    """Unit tests for the GuardResult dataclass."""

    def test_passed_defaults(self):
        """Passing result has sensible defaults."""
        r = GuardResult(passed=True, trace_id="t1")
        assert r.passed is True
        assert r.issues == []
        assert r.rules_violated == []
        assert r.severity == "none"
        assert r.violation is None
        assert r.sql_report is None

    def test_failed_with_violation(self):
        """Failing result carries violation details."""
        v = _make_violation()
        r = GuardResult(passed=False, trace_id="t1", violation=v, issues=v.issues, severity="high")
        assert r.passed is False
        assert r.has_policy_violation is True
        assert r.has_sql_violation is False

    def test_has_sql_violation(self):
        """has_sql_violation reflects SQL report state."""
        r = GuardResult(passed=False, trace_id="t1", sql_report=_make_sql_report(passed=False))
        assert r.has_sql_violation is True

    def test_sql_results_empty_when_no_sql(self):
        """sql_results returns empty list when SQL not configured."""
        r = GuardResult(passed=True, trace_id="t1")
        assert r.sql_results == []

    def test_to_dict_is_json_serializable(self):
        """to_dict output is valid JSON."""
        r = GuardResult(passed=True, trace_id="t1")
        j = json.dumps(r.to_dict(), default=str)
        assert json.loads(j)["passed"] is True

    def test_to_dict_includes_violation(self):
        """to_dict includes violation details when present."""
        v = _make_violation()
        r = GuardResult(passed=False, trace_id="t1", violation=v)
        d = r.to_dict()
        assert d["violation"]["rules_violated"] == ["R001"]

    def test_to_dict_includes_sql_report(self):
        """to_dict includes SQL report when present."""
        r = GuardResult(passed=False, trace_id="t1", sql_report=_make_sql_report(passed=False))
        d = r.to_dict()
        assert d["sql_report"]["passed"] is False

    def test_to_json(self):
        """to_json returns parseable JSON string."""
        r = GuardResult(passed=True, trace_id="t1")
        assert json.loads(r.to_json())["passed"] is True

    def test_to_langsmith_passing(self):
        """to_langsmith returns score=1.0 for pass."""
        r = GuardResult(passed=True, trace_id="t1")
        assert r.to_langsmith()["score"] == 1.0

    def test_to_langsmith_with_violation(self):
        """to_langsmith delegates to Violation."""
        v = _make_violation(trace_id="t1")
        r = GuardResult(passed=False, trace_id="t1", violation=v)
        assert r.to_langsmith()["score"] == 0.8

    def test_to_langfuse_passing(self):
        """to_langfuse returns pass value."""
        r = GuardResult(passed=True, trace_id="t1")
        assert r.to_langfuse()["value"] == "pass"

    def test_to_datadog_passing(self):
        """to_datadog returns pass value."""
        r = GuardResult(passed=True, trace_id="t1")
        assert r.to_datadog()["value"] == "pass"


# ===========================================================================
# INTEGRATION TESTS — Real Cerebras LLM calls
# ===========================================================================


@requires_cerebras
class TestPolicyGuardFromPolicy:
    """Test from_policy factory with real LLM extraction."""

    @pytest.mark.asyncio
    async def test_from_policy_extracts_rules(self):
        """from_policy extracts a valid LogicMap from policy text."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)

        assert guard.logic_map is not None
        assert len(guard.logic_map.rules) >= 3
        assert guard.model == CEREBRAS_MODEL
        assert guard.has_sql is False


@requires_cerebras
class TestPolicyGuardCheckCompliant:
    """Test check_async on a compliant conversation."""

    @pytest.mark.asyncio
    async def test_compliant_conversation_passes(self):
        """A policy-compliant conversation should pass the guard."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        result = await guard.check_async(COMPLIANT_MESSAGES, trace_id="compliant-1")

        assert result.passed is True
        assert result.trace_id == "compliant-1"
        assert result.violation is None
        assert result.latency_ms > 0
        assert result.cost >= 0

        # Serialization works
        d = result.to_dict()
        assert d["passed"] is True
        json.loads(result.to_json())


@requires_cerebras
class TestPolicyGuardCheckViolation:
    """Test check_async on conversations that violate policy."""

    @pytest.mark.asyncio
    async def test_uber_limit_violation_detected(self):
        """$75 Uber ride exceeds $30 limit — should be flagged."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        result = await guard.check_async(VIOLATING_MESSAGES, trace_id="uber-violation")

        assert result.passed is False
        assert result.violation is not None
        assert len(result.issues) > 0
        assert result.severity != "none"
        assert result.latency_ms > 0

        # Violation carries context
        v = result.violation
        assert v.trace_id == "uber-violation"
        assert len(v.rules_violated) > 0

    @pytest.mark.asyncio
    async def test_alcohol_violation_detected(self):
        """Alcohol purchases are never reimbursable — should be flagged."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        result = await guard.check_async(ALCOHOL_VIOLATION_MESSAGES, trace_id="alcohol-violation")

        assert result.passed is False
        assert result.violation is not None
        assert len(result.issues) > 0


@requires_cerebras
class TestPolicyGuardEdgeCase:
    """Test check_async on an edge case conversation."""

    @pytest.mark.asyncio
    async def test_exact_limit_passes(self):
        """$50 meal is exactly at the cap — should pass."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        result = await guard.check_async(EDGE_CASE_MESSAGES, trace_id="edge-50")

        assert result.passed is True


@requires_cerebras
class TestPolicyGuardBatch:
    """Test check_batch_async with real LLM calls."""

    @pytest.mark.asyncio
    async def test_batch_mixed_results(self):
        """Batch check returns correct pass/fail for mixed conversations."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)

        results = await guard.check_batch_async(
            [COMPLIANT_MESSAGES, VIOLATING_MESSAGES, EDGE_CASE_MESSAGES]
        )

        assert len(results) == 3

        # Compliant should pass
        assert results[0].passed is True

        # $75 Uber violation should fail
        assert results[1].passed is False
        assert results[1].violation is not None

        # Edge case ($50 exact) should pass
        assert results[2].passed is True

    @pytest.mark.asyncio
    async def test_batch_assigns_trace_ids(self):
        """Batch check assigns sequential trace IDs."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)

        results = await guard.check_batch_async([COMPLIANT_MESSAGES, VIOLATING_MESSAGES])

        assert results[0].trace_id == "trace_0"
        assert results[1].trace_id == "trace_1"


@requires_cerebras
class TestPolicyGuardObservability:
    """Test that observability exports work end-to-end."""

    @pytest.mark.asyncio
    async def test_violation_exports(self):
        """Violation result produces valid LangSmith/Langfuse/Datadog exports."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        result = await guard.check_async(VIOLATING_MESSAGES, trace_id="obs-test")

        assert result.passed is False

        # LangSmith
        ls = result.to_langsmith()
        assert "run_id" in ls
        assert "score" in ls
        assert ls["score"] < 1.0

        # Langfuse
        lf = result.to_langfuse()
        assert "traceId" in lf
        assert "name" in lf

        # Datadog
        dd = result.to_datadog()
        assert "span_context" in dd
        assert "label" in dd

    @pytest.mark.asyncio
    async def test_passing_exports(self):
        """Passing result produces valid observability exports."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        result = await guard.check_async(COMPLIANT_MESSAGES, trace_id="obs-pass")

        assert result.passed is True
        assert result.to_langsmith()["score"] == 1.0
        assert result.to_langfuse()["value"] == "pass"
        assert result.to_datadog()["value"] == "pass"


@requires_cerebras
class TestPolicyGuardCostTracking:
    """Test that cost and call count are tracked across checks."""

    @pytest.mark.asyncio
    async def test_cost_accumulates(self):
        """total_cost and call_count increase after checks."""
        guard = await PolicyGuard.from_policy(EXPENSE_POLICY, model=CEREBRAS_MODEL)

        initial_cost = guard.total_cost
        initial_calls = guard.call_count

        await guard.check_async(COMPLIANT_MESSAGES)
        await guard.check_async(VIOLATING_MESSAGES)

        assert guard.call_count > initial_calls
        assert guard.total_cost >= initial_cost


@requires_cerebras
class TestPolicyGuardSync:
    """Test synchronous wrappers."""

    def test_from_policy_sync(self):
        """from_policy_sync creates a working guard."""
        guard = PolicyGuard.from_policy_sync(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        assert guard.logic_map is not None
        assert len(guard.logic_map.rules) >= 3

    def test_check_sync(self):
        """check() sync wrapper returns valid result."""
        guard = PolicyGuard.from_policy_sync(EXPENSE_POLICY, model=CEREBRAS_MODEL)
        result = guard.check(VIOLATING_MESSAGES, trace_id="sync-test")

        assert result.passed is False
        assert result.violation is not None


# ===========================================================================
# IMPORT TESTS
# ===========================================================================


class TestImports:
    """Verify PolicyGuard is importable from the public API."""

    def test_import_from_synkro(self):
        """PolicyGuard and GuardResult importable from top-level synkro."""
        from synkro import GuardResult, PolicyGuard

        assert PolicyGuard is not None
        assert GuardResult is not None

    def test_import_from_guard_module(self):
        """PolicyGuard importable from synkro.guard."""
        from synkro.guard import GuardResult, PolicyGuard

        assert PolicyGuard is not None
        assert GuardResult is not None
