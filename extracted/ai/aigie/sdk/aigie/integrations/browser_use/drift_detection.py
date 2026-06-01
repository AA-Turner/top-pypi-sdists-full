"""
Drift Detection for Browser Use Workflows.

Tracks browser action planning vs actual execution to detect behavioral drifts.
Useful for monitoring automation reliability and detecting deviations.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in browser automation."""

    # Planning drifts
    MISSING_STEP = "missing_step"  # Planned step not executed
    EXTRA_STEP = "extra_step"  # Unplanned step executed
    STEP_ORDER = "step_order"  # Steps executed in wrong order

    # Action drifts
    UNEXPECTED_ACTION = "unexpected_action"  # Action used that wasn't planned
    MISSING_ACTION = "missing_action"  # Expected action not performed
    ACTION_RETRY = "action_retry"  # Action had to be retried
    ACTION_OVERUSE = "action_overuse"  # Same action repeated too many times

    # Navigation drifts
    UNEXPECTED_PAGE = "unexpected_page"  # Navigated to unplanned URL
    NAVIGATION_LOOP = "navigation_loop"  # Same pages visited repeatedly
    MISSING_NAVIGATION = "missing_navigation"  # Expected navigation didn't happen

    # Element drifts
    ELEMENT_CHANGE = "element_change"  # Element selector changed
    ELEMENT_MISSING = "element_missing"  # Expected element not found

    # Output drifts
    INCOMPLETE_OUTPUT = "incomplete_output"  # Output missing expected components
    FORMAT_DRIFT = "format_drift"  # Output format differs from plan

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Execution took much longer/shorter
    TOKEN_ANOMALY = "token_anomaly"  # Token usage anomaly
    STEP_COUNT_ANOMALY = "step_count_anomaly"  # More/fewer steps than expected


class DriftSeverity(Enum):
    """Severity of detected drift."""

    INFO = "info"  # Expected variation, informational
    WARNING = "warning"  # Notable deviation, worth monitoring
    ALERT = "alert"  # Significant drift, may need intervention


@dataclass
class DetectedDrift:
    """Represents a detected drift with full context."""

    drift_type: DriftType
    severity: DriftSeverity
    description: str
    expected: str | None = None
    actual: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "drift_type": self.drift_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "expected": self.expected,
            "actual": self.actual,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class BrowserPlan:
    """Captures the automation's plan/intent for execution."""

    # Raw planning text
    raw_plan: str | None = None
    task_description: str | None = None
    initial_url: str | None = None

    # Extracted plan components
    planned_steps: List[str] = field(default_factory=list)
    expected_actions: Set[str] = field(default_factory=set)  # click, type, navigate, etc.
    expected_urls: Set[str] = field(default_factory=set)
    expected_selectors: Set[str] = field(default_factory=set)
    expected_outputs: List[str] = field(default_factory=list)

    # Plan metadata
    timestamp: datetime = field(default_factory=datetime.now)
    model: str | None = None
    max_steps: int | None = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "raw_plan": self.raw_plan,
            "task_description": self.task_description[:200] if self.task_description else None,
            "initial_url": self.initial_url,
            "planned_steps": self.planned_steps,
            "expected_actions": list(self.expected_actions),
            "expected_urls": list(self.expected_urls),
            "expected_selectors": list(self.expected_selectors),
            "expected_outputs": self.expected_outputs,
            "timestamp": self.timestamp.isoformat(),
            "model": self.model,
            "max_steps": self.max_steps,
        }


@dataclass
class ExecutionTrace:
    """Tracks actual execution for comparison against plan."""

    # Execution events
    actions_performed: List[Dict[str, Any]] = field(default_factory=list)
    pages_visited: List[Dict[str, Any]] = field(default_factory=list)
    llm_responses: List[Dict[str, Any]] = field(default_factory=list)

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0
    error_count: int = 0
    retry_count: int = 0
    step_count: int = 0

    # Outputs
    final_output: str | None = None
    final_url: str | None = None
    success: bool = False

    def add_action(
        self,
        action_type: str,
        selector: str | None = None,
        value: str | None = None,
        duration_ms: float = 0,
        is_error: bool = False,
        is_retry: bool = False,
    ) -> None:
        """Record an action."""
        self.actions_performed.append(
            {
                "action_type": action_type,
                "selector": selector,
                "value_preview": str(value)[:100] if value else None,
                "duration_ms": duration_ms,
                "is_error": is_error,
                "is_retry": is_retry,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if is_error:
            self.error_count += 1
        if is_retry:
            self.retry_count += 1

    def add_page_visit(self, url: str, title: str | None = None, duration_ms: float = 0) -> None:
        """Record a page visit."""
        self.pages_visited.append(
            {
                "url": url,
                "title": title,
                "duration_ms": duration_ms,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def add_llm_response(self, text_preview: str, model: str | None = None) -> None:
        """Record an LLM response."""
        self.llm_responses.append(
            {
                "text_preview": text_preview[:200],
                "model": model,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def increment_step(self) -> int:
        """Increment step count."""
        self.step_count += 1
        return self.step_count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "actions_performed": self.actions_performed,
            "actions_summary": self._get_actions_summary(),
            "pages_visited": self.pages_visited,
            "urls_visited": list(set(p["url"] for p in self.pages_visited)),
            "llm_response_count": len(self.llm_responses),
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "error_count": self.error_count,
            "retry_count": self.retry_count,
            "step_count": self.step_count,
            "success": self.success,
            "final_url": self.final_url,
        }

    def _get_actions_summary(self) -> Dict[str, int]:
        """Get summary of actions performed."""
        summary = {}
        for action in self.actions_performed:
            action_type = action["action_type"]
            summary[action_type] = summary.get(action_type, 0) + 1
        return summary


class DriftDetector:
    """
    Detects drift between browser automation planning and actual execution.

    Captures:
    - Initial plan from task and agent's first response
    - Actual execution path (actions, pages, outputs)
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = BrowserPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []
        self._plan_captured = False
        self._action_counts: Dict[str, int] = {}  # Track action repetitions

    def capture_task(
        self, task: str, initial_url: str | None = None, max_steps: int | None = None
    ) -> None:
        """Capture task description for plan extraction."""
        self.plan.task_description = task
        self.plan.initial_url = initial_url
        self.plan.max_steps = max_steps
        self._extract_plan_from_task(task)

    def capture_planning_response(self, response_text: str, model: str | None = None) -> None:
        """
        Capture agent's planning response (typically first response).

        Looks for planning patterns like:
        - "I'll first click on..."
        - "Steps: 1. Navigate to... 2. Click..."
        - Action descriptions
        """
        if self._plan_captured:
            return

        self.plan.raw_plan = response_text
        self.plan.model = model
        self._extract_plan_from_response(response_text)
        self._plan_captured = True

    def record_action(
        self,
        action_type: str,
        selector: str | None = None,
        value: str | None = None,
        duration_ms: float = 0,
        is_error: bool = False,
        is_retry: bool = False,
    ) -> DetectedDrift | None:
        """Record an action and check for drift."""
        self.execution.add_action(action_type, selector, value, duration_ms, is_error, is_retry)

        # Track action counts for overuse detection
        self._action_counts[action_type] = self._action_counts.get(action_type, 0) + 1

        # Check for retry drift
        if is_retry:
            drift = DetectedDrift(
                drift_type=DriftType.ACTION_RETRY,
                severity=DriftSeverity.WARNING,
                description=f"Action '{action_type}' was retried",
                expected="Single execution",
                actual="Retry required",
                metadata={"action_type": action_type, "selector": selector},
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for unexpected action
        if self.plan.expected_actions and action_type not in self.plan.expected_actions:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_ACTION,
                severity=DriftSeverity.INFO,
                description=f"Action '{action_type}' used but not in original plan",
                expected=f"Expected actions: {', '.join(self.plan.expected_actions)}",
                actual=action_type,
                metadata={"action_type": action_type, "selector": selector},
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for action overuse (more than 5 of same type)
        if self._action_counts[action_type] > 5:
            drift = DetectedDrift(
                drift_type=DriftType.ACTION_OVERUSE,
                severity=DriftSeverity.WARNING,
                description=f"Action '{action_type}' used {self._action_counts[action_type]} times",
                metadata={"action_type": action_type, "count": self._action_counts[action_type]},
            )
            # Only record once per threshold
            if self._action_counts[action_type] == 6:
                self.detected_drifts.append(drift)
                return drift

        return None

    def record_navigation(
        self,
        url: str,
        title: str | None = None,
        duration_ms: float = 0,
    ) -> DetectedDrift | None:
        """Record a page navigation and check for drift."""
        self.execution.add_page_visit(url, title, duration_ms)
        self.execution.final_url = url

        # Check for navigation loop
        recent_urls = [p["url"] for p in self.execution.pages_visited[-5:]]
        if len(recent_urls) >= 3 and len(set(recent_urls)) <= 2:
            drift = DetectedDrift(
                drift_type=DriftType.NAVIGATION_LOOP,
                severity=DriftSeverity.WARNING,
                description="Detected navigation loop - repeatedly visiting same pages",
                metadata={"recent_urls": recent_urls},
            )
            # Only record once
            if not any(d.drift_type == DriftType.NAVIGATION_LOOP for d in self.detected_drifts):
                self.detected_drifts.append(drift)
                return drift

        return None

    def record_step(self, step_number: int) -> None:
        """Record a step execution."""
        self.execution.step_count = step_number

    def record_llm_response(self, text: str, model: str | None = None) -> None:
        """Record an LLM response."""
        self.execution.add_llm_response(text, model)

        # Capture planning from first substantial response
        if not self._plan_captured and len(text) > 50:
            self.capture_planning_response(text, model)

    def finalize(
        self,
        total_duration_ms: float,
        total_tokens: int,
        total_cost: float,
        final_output: str | None = None,
        success: bool = False,
    ) -> List[DetectedDrift]:
        """
        Finalize execution tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.total_duration_ms = total_duration_ms
        self.execution.total_tokens = total_tokens
        self.execution.total_cost = total_cost
        self.execution.final_output = final_output
        self.execution.success = success

        # Perform final drift analysis
        self._analyze_step_count()
        self._analyze_action_coverage()

        return self.detected_drifts

    def _extract_plan_from_task(self, text: str) -> None:
        """Extract planning hints from task description."""
        # Look for action mentions
        action_patterns = [
            (r"click\s+(?:on\s+)?(.+?)(?:\.|,|$)", "click"),
            (r"type\s+(?:in\s+)?(.+?)(?:\.|,|$)", "type"),
            (r"navigate\s+to\s+(.+?)(?:\.|,|$)", "navigate"),
            (r"go\s+to\s+(.+?)(?:\.|,|$)", "navigate"),
            (r"scroll\s+(?:to\s+)?(.+?)(?:\.|,|$)", "scroll"),
            (r"fill\s+(?:in\s+)?(.+?)(?:\.|,|$)", "type"),
        ]

        for pattern, action_type in action_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                self.plan.expected_actions.add(action_type)

        # Extract URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        self.plan.expected_urls.update(urls)

    def _extract_plan_from_response(self, text: str) -> None:
        """Extract planning from agent's first response."""
        # Look for step patterns
        step_patterns = [
            r"(?:Step \d+[:.]\s*)(.+?)(?=Step \d+|$)",
            r"(?:\d+\.\s*)(.+?)(?=\d+\.|$)",
            r"(?:First,?\s+I(?:'ll)?\s+)(.+?)(?:\.|$)",
            r"(?:Then,?\s+I(?:'ll)?\s+)(.+?)(?:\.|$)",
        ]

        for pattern in step_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                for match in matches[:10]:  # Limit to first 10 steps
                    step = match.strip()[:150]
                    if len(step) > 10:
                        self.plan.planned_steps.append(step)

        # Extract action types from response
        action_keywords = {
            "click": ["click", "clicking", "press", "pressing", "tap"],
            "type": ["type", "typing", "enter", "entering", "fill", "filling", "input"],
            "navigate": ["navigate", "go to", "visit", "open", "load"],
            "scroll": ["scroll", "scrolling"],
            "hover": ["hover", "hovering"],
            "wait": ["wait", "waiting"],
        }

        text_lower = text.lower()
        for action_type, keywords in action_keywords.items():
            if any(kw in text_lower for kw in keywords):
                self.plan.expected_actions.add(action_type)

    def _analyze_step_count(self) -> None:
        """Analyze if step count is anomalous."""
        if self.plan.max_steps and self.execution.step_count > self.plan.max_steps:
            drift = DetectedDrift(
                drift_type=DriftType.STEP_COUNT_ANOMALY,
                severity=DriftSeverity.WARNING,
                description=f"Executed {self.execution.step_count} steps (max was {self.plan.max_steps})",
                expected=str(self.plan.max_steps),
                actual=str(self.execution.step_count),
            )
            self.detected_drifts.append(drift)

    def _analyze_action_coverage(self) -> None:
        """Analyze if expected actions were performed."""
        if not self.plan.expected_actions:
            return

        performed_actions = set(self.execution._get_actions_summary().keys())
        missing = self.plan.expected_actions - performed_actions

        if missing:
            drift = DetectedDrift(
                drift_type=DriftType.MISSING_ACTION,
                severity=DriftSeverity.INFO,
                description=f"Expected actions not performed: {', '.join(missing)}",
                expected=f"Actions: {', '.join(self.plan.expected_actions)}",
                actual=f"Performed: {', '.join(performed_actions)}",
            )
            self.detected_drifts.append(drift)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of plan vs execution."""
        return {
            "plan": self.plan.to_dict(),
            "execution": self.execution.to_dict(),
            "drifts": [d.to_dict() for d in self.detected_drifts],
            "drift_count": len(self.detected_drifts),
            "has_warnings": any(
                d.severity in [DriftSeverity.WARNING, DriftSeverity.ALERT]
                for d in self.detected_drifts
            ),
        }

    def get_drift_report(self) -> str:
        """Get a human-readable drift report."""
        if not self.detected_drifts:
            return "No drifts detected - execution matched plan"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}\n"
            report += f"   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report
