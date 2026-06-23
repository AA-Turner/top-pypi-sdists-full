"""
Base Guardrail Framework for SLA Production Runtime.

Kytte is an SLA production tool, NOT a security tool.
Guardrails detect issues and trigger remediation actions:
- RETRY: Retry with adjusted approach
- REDIRECT: Use fallback model/strategy
- ADJUST: Modify content and continue
- ESCALATE: Escalate for remediation plan

We do NOT block content - we ensure uptime through intelligent remediation.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aigie.client import Aigie

logger = logging.getLogger(__name__)


class GuardrailAction(Enum):
    """Actions that can be taken by guardrails.

    Kytte is an SLA production tool, NOT a security tool.
    We do NOT block - we retry, redirect, or adjust to maintain uptime.
    """

    PASS = "pass"  # Content is good, allow through
    WARN = "warn"  # Content has issues, allow through with warning/signal
    RETRY = "retry"  # Issue detected - trigger retry with adjusted approach
    REDIRECT = "redirect"  # Issue detected - redirect to fallback model/strategy
    ADJUST = "adjust"  # Modify content and continue (e.g., truncate, rephrase)
    ESCALATE = "escalate"  # Issue too complex - escalate for remediation plan


@dataclass
class GuardrailResult:
    """Result of a guardrail check.

    Attributes:
        guardrail_name: Name of the guardrail that produced this result
        action: The action taken/recommended
        passed: Whether the content passed the check
        score: Confidence score (0.0 to 1.0)
        issues: List of detected issues
        modified_content: Modified content if action is REDACT or MODIFY
        details: Additional details about the check
        timestamp: When the check was performed
        duration_ms: Time taken for the check
    """

    guardrail_name: str
    action: GuardrailAction
    passed: bool
    score: float = 1.0
    issues: list[str] = field(default_factory=list)
    modified_content: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "guardrail_name": self.guardrail_name,
            "action": self.action.value,
            "passed": self.passed,
            "score": self.score,
            "issues": self.issues,
            "modified_content": self.modified_content,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
        }


class BaseGuardrail(ABC):
    """
    Base class for content guardrails.

    Subclasses must implement the `check` method to analyze content
    and return a GuardrailResult.
    """

    def __init__(self, name: str | None = None):
        self.name = name or self.__class__.__name__
        self.enabled = True

    @abstractmethod
    async def check(self, content: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        """
        Check content against this guardrail.

        Args:
            content: The content to check
            context: Optional context (e.g., input, conversation history)

        Returns:
            GuardrailResult with action and details
        """
        pass

    def enable(self) -> None:
        """Enable this guardrail."""
        self.enabled = True

    def disable(self) -> None:
        """Disable this guardrail."""
        self.enabled = False


class GuardrailChain:
    """
    Chain of guardrails for comprehensive content checking.

    Executes multiple guardrails in sequence and aggregates results.

    Example:
        >>> chain = GuardrailChain()
        >>> chain.add(PIIDetector())
        >>> chain.add(ToxicityDetector())
        >>> result = await chain.check("Some content to verify")
        >>> if not result.passed:
        ...     print(f"Blocked: {result.issues}")

    With Kytte backend reporting:
        >>> from aigie import get_aigie
        >>> chain = GuardrailChain(aigie_client=get_aigie())
        >>> result = await chain.check("Content", trace_id="abc-123")
        >>> # Results are automatically sent to Kytte for monitoring
    """

    def __init__(
        self,
        guardrails: list[BaseGuardrail] | None = None,
        fail_fast: bool = True,
        on_remediation: Callable[[str, GuardrailResult], None] | None = None,
        aigie_client: Optional["Aigie"] = None,
        auto_report: bool = True,
    ):
        """
        Initialize the guardrail chain.

        Args:
            guardrails: Initial list of guardrails
            fail_fast: Stop on first escalation if True
            on_remediation: Callback when remediation action is needed (retry/redirect/escalate)
            aigie_client: Optional Aigie client for reporting guardrail checks to backend
            auto_report: If True and aigie_client is set, automatically report all checks
        """
        self.guardrails: list[BaseGuardrail] = guardrails or []
        self.fail_fast = fail_fast
        self.on_remediation = on_remediation
        self._aigie_client = aigie_client
        self._auto_report = auto_report

    def add(self, guardrail: BaseGuardrail) -> "GuardrailChain":
        """
        Add a guardrail to the chain.

        Args:
            guardrail: Guardrail to add

        Returns:
            Self for chaining
        """
        self.guardrails.append(guardrail)
        return self

    def remove(self, guardrail_name: str) -> bool:
        """
        Remove a guardrail by name.

        Args:
            guardrail_name: Name of guardrail to remove

        Returns:
            True if removed, False if not found
        """
        for i, g in enumerate(self.guardrails):
            if g.name == guardrail_name:
                self.guardrails.pop(i)
                return True
        return False

    async def check(
        self,
        content: str,
        context: dict[str, Any] | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
    ) -> GuardrailResult:
        """
        Run all guardrails and return aggregated result.

        Args:
            content: Content to check
            context: Optional context
            trace_id: Optional trace ID for reporting to Kytte backend
            span_id: Optional span ID for reporting to Kytte backend

        Returns:
            Aggregated GuardrailResult
        """
        import time

        start_time = time.time()

        all_issues = []
        all_details = {}
        min_score = 1.0
        final_action = GuardrailAction.PASS
        modified_content = None
        individual_results = []

        for guardrail in self.guardrails:
            if not guardrail.enabled:
                continue

            try:
                result = await guardrail.check(content, context)
                individual_results.append(result.to_dict())

                # Track issues
                all_issues.extend(result.issues)
                all_details[guardrail.name] = result.to_dict()

                # Track minimum score
                min_score = min(min_score, result.score)

                # Determine action priority: ESCALATE > REDIRECT > RETRY > ADJUST > WARN > PASS
                # Note: We don't block - we escalate for remediation
                action_priority = {
                    GuardrailAction.PASS: 0,
                    GuardrailAction.WARN: 1,
                    GuardrailAction.ADJUST: 2,
                    GuardrailAction.RETRY: 3,
                    GuardrailAction.REDIRECT: 4,
                    GuardrailAction.ESCALATE: 5,
                }
                if action_priority[result.action] > action_priority[final_action]:
                    final_action = result.action

                # Handle modified content
                if result.modified_content:
                    modified_content = result.modified_content
                    content = modified_content  # Use modified content for subsequent checks

                # Fail fast if escalation needed (requires remediation)
                if self.fail_fast and result.action == GuardrailAction.ESCALATE:
                    break

            except Exception as e:
                logger.error(f"Guardrail {guardrail.name} failed: {e}")
                all_issues.append(f"Guardrail error: {guardrail.name}")
                all_details[guardrail.name] = {"error": str(e)}

        # Create aggregated result
        # In Kytte's SLA model: PASS/WARN/ADJUST are "passed", RETRY/REDIRECT/ESCALATE need remediation
        needs_remediation = final_action in [
            GuardrailAction.RETRY,
            GuardrailAction.REDIRECT,
            GuardrailAction.ESCALATE,
        ]
        passed = not needs_remediation
        duration_ms = (time.time() - start_time) * 1000

        result = GuardrailResult(
            guardrail_name="GuardrailChain",
            action=final_action,
            passed=passed,
            score=min_score,
            issues=all_issues,
            modified_content=modified_content,
            details={
                "guardrails_run": len(individual_results),
                "individual_results": individual_results,
                "needs_remediation": needs_remediation,
                **all_details,
            },
            duration_ms=duration_ms,
        )

        # Call remediation callback if action needed
        if needs_remediation and self.on_remediation:
            try:
                self.on_remediation(content, result)
            except Exception as e:
                logger.error(f"on_remediation callback failed: {e}")

        return result

    async def check_and_remediate(
        self,
        content: str,
        context: dict[str, Any] | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
    ) -> tuple[str, GuardrailResult | None]:
        """
        Check content and return it with any needed remediation info.

        Kytte is an SLA tool - we don't block, we provide remediation guidance.

        Args:
            content: Content to check
            context: Optional context
            trace_id: Optional trace ID for reporting to Kytte backend
            span_id: Optional span ID for reporting to Kytte backend

        Returns:
            Tuple of (content, remediation_result):
            - content: Original or adjusted content
            - remediation_result: None if passed, GuardrailResult if remediation needed
        """
        result = await self.check(content, context, trace_id=trace_id, span_id=span_id)

        # Return adjusted content if available
        output_content = result.modified_content if result.modified_content else content

        # If needs remediation (RETRY, REDIRECT, ESCALATE), return the result for handling
        if result.action in [
            GuardrailAction.RETRY,
            GuardrailAction.REDIRECT,
            GuardrailAction.ESCALATE,
        ]:
            return output_content, result

        # PASS, WARN, ADJUST - continue normally
        return output_content, None

    async def get_remediation_trigger(
        self,
        content: str,
        context: dict[str, Any] | None = None,
        trace_id: str | None = None,
        span_id: str | None = None,
    ) -> dict[str, Any] | None:
        """
        Check content and return remediation trigger info for the backend.

        This integrates with Kytte's RemediationService by providing
        trigger information for remediation plans.

        Args:
            content: Content to check
            context: Optional context
            trace_id: Optional trace ID for reporting to Kytte backend
            span_id: Optional span ID for reporting to Kytte backend

        Returns:
            Remediation trigger dict or None if no remediation needed
        """
        result = await self.check(content, context, trace_id=trace_id, span_id=span_id)

        if result.action not in [
            GuardrailAction.RETRY,
            GuardrailAction.REDIRECT,
            GuardrailAction.ESCALATE,
        ]:
            return None

        # Map guardrail actions to remediation trigger types
        trigger_type_map = {
            GuardrailAction.RETRY: "validation_error",
            GuardrailAction.REDIRECT: "api_error",
            GuardrailAction.ESCALATE: "context_drift",
        }

        return {
            "trigger_type": trigger_type_map.get(result.action, "validation_error"),
            "trigger_metadata": {
                "guardrail_action": result.action.value,
                "issues": result.issues,
                "score": result.score,
                "guardrail_name": result.guardrail_name,
            },
            "suggestions": [
                {
                    "action": result.action.value,
                    "description": f"Guardrail detected: {', '.join(result.issues[:3])}",
                    "confidence": result.score,
                }
            ],
        }

    def list_guardrails(self) -> list[str]:
        """List all guardrail names in the chain."""
        return [g.name for g in self.guardrails]

    def set_aigie_client(self, client: "Aigie", auto_report: bool = True) -> "GuardrailChain":
        """
        Set the Aigie client for reporting guardrail checks.

        Args:
            client: Aigie client instance
            auto_report: If True, automatically report all checks

        Returns:
            Self for chaining
        """
        self._aigie_client = client
        self._auto_report = auto_report
        return self


class GuardrailRemediationNeeded(Exception):
    """
    Exception raised when guardrails detect content needing remediation.

    Note: This is rarely used in Kytte's SLA model. Prefer using
    check_and_remediate() or get_remediation_trigger() which return
    remediation info without raising exceptions.
    """

    def __init__(self, message: str, result: GuardrailResult | None = None):
        super().__init__(message)
        self.result = result
        self.remediation_action = result.action if result else None
