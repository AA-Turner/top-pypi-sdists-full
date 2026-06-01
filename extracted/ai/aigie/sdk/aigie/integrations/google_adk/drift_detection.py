"""
Drift Detection for Google ADK.

Tracks agent planning vs actual execution to detect behavioral drifts.
Useful for monitoring agent reliability and detecting deviations.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift."""

    # Planning drifts
    MISSING_STEP = "missing_step"  # Planned step not executed
    EXTRA_STEP = "extra_step"  # Unplanned step executed
    STEP_ORDER = "step_order"  # Steps executed in wrong order

    # Tool usage drifts
    UNEXPECTED_TOOL = "unexpected_tool"  # Tool used that wasn't mentioned
    MISSING_TOOL = "missing_tool"  # Expected tool not used
    TOOL_OVERUSE = "tool_overuse"  # Tool used more than expected

    # Agent drifts
    EXTRA_AGENT = "extra_agent"  # More agent calls than planned
    MISSING_AGENT = "missing_agent"  # Fewer agent calls than planned
    AGENT_RETRY = "agent_retry"  # Agent had to be retried

    # Output drifts
    INCOMPLETE_OUTPUT = "incomplete_output"  # Output missing expected components
    FORMAT_DRIFT = "format_drift"  # Output format differs from plan

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Execution took much longer/shorter
    TOKEN_ANOMALY = "token_anomaly"  # Token usage anomaly


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
class AgentPlan:
    """Captures the agent's plan/intent for execution."""

    # Raw planning text
    raw_plan: str | None = None
    system_prompt: str | None = None
    initial_prompt: str | None = None

    # Extracted plan components
    planned_steps: List[str] = field(default_factory=list)
    expected_tools: Set[str] = field(default_factory=set)
    expected_agents: List[Dict[str, str]] = field(default_factory=list)
    expected_outputs: List[str] = field(default_factory=list)

    # Planning step outputs
    planning_step_outputs: List[Dict[str, Any]] = field(default_factory=list)

    # Plan metadata
    timestamp: datetime = field(default_factory=datetime.now)
    model: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "raw_plan": self.raw_plan,
            "system_prompt": self.system_prompt if self.system_prompt else None,
            "initial_prompt_preview": self.initial_prompt[:200] if self.initial_prompt else None,
            "planned_steps": self.planned_steps,
            "expected_tools": list(self.expected_tools),
            "expected_agents": self.expected_agents,
            "expected_outputs": self.expected_outputs,
            "planning_step_outputs": self.planning_step_outputs,
            "timestamp": self.timestamp.isoformat(),
            "model": self.model,
        }


@dataclass
class ExecutionTrace:
    """Tracks actual execution for comparison against plan."""

    # Execution events
    tools_used: List[Dict[str, Any]] = field(default_factory=list)
    agents_executed: List[Dict[str, Any]] = field(default_factory=list)
    llm_responses: List[Dict[str, Any]] = field(default_factory=list)

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0
    error_count: int = 0
    retry_count: int = 0

    # Outputs
    final_output: str | None = None

    def add_tool_use(
        self, tool_name: str, tool_input: Dict, duration_ms: float, is_error: bool = False
    ) -> None:
        """Record a tool use."""
        self.tools_used.append(
            {
                "tool_name": tool_name,
                "tool_input_preview": str(tool_input)[:200],
                "duration_ms": duration_ms,
                "is_error": is_error,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if is_error:
            self.error_count += 1

    def add_agent_execution(
        self, agent_name: str, tool_count: int = 0, is_retry: bool = False
    ) -> None:
        """Record an agent execution."""
        self.agents_executed.append(
            {
                "agent_name": agent_name,
                "tool_count": tool_count,
                "is_retry": is_retry,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if is_retry:
            self.retry_count += 1

    def add_llm_response(self, text_preview: str, model: str | None = None) -> None:
        """Record an LLM response."""
        self.llm_responses.append(
            {
                "text_preview": text_preview[:200],
                "model": model,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "tools_used": self.tools_used,
            "tools_summary": self._get_tools_summary(),
            "agents_executed": self.agents_executed,
            "agents_summary": self._get_agents_summary(),
            "llm_response_count": len(self.llm_responses),
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "error_count": self.error_count,
            "retry_count": self.retry_count,
        }

    def _get_tools_summary(self) -> Dict[str, int]:
        """Get summary of tools used."""
        summary = {}
        for tool in self.tools_used:
            name = tool["tool_name"]
            summary[name] = summary.get(name, 0) + 1
        return summary

    def _get_agents_summary(self) -> Dict[str, int]:
        """Get summary of agents executed."""
        summary = {}
        for agent in self.agents_executed:
            name = agent["agent_name"]
            summary[name] = summary.get(name, 0) + 1
        return summary


class DriftDetector:
    """
    Detects drift between agent planning and actual execution.

    Captures:
    - Initial plan from system prompts and first responses
    - Actual execution path (tools, agents, outputs)
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = AgentPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []
        self._plan_captured = False

    def capture_system_prompt(self, system_prompt: str) -> None:
        """Capture system prompt for plan extraction."""
        self.plan.system_prompt = system_prompt
        self._extract_plan_from_prompt(system_prompt)

    def capture_initial_prompt(self, prompt: str) -> None:
        """Capture initial user prompt."""
        self.plan.initial_prompt = prompt

    def capture_planning_response(self, response_text: str, model: str | None = None) -> None:
        """
        Capture agent's planning response (typically first response).

        Looks for planning patterns like:
        - "I'll start by..."
        - "Steps: 1. ... 2. ..."
        - "First, I will..."
        """
        if self._plan_captured:
            return

        self.plan.raw_plan = response_text
        self.plan.model = model
        self._extract_plan_from_response(response_text)
        self._plan_captured = True

    def record_tool_use(
        self,
        tool_name: str,
        tool_input: Dict[str, Any],
        duration_ms: float = 0,
        is_error: bool = False,
    ) -> DetectedDrift | None:
        """Record a tool use and check for drift."""
        self.execution.add_tool_use(tool_name, tool_input, duration_ms, is_error)

        # Check for unexpected tool
        if self.plan.expected_tools and tool_name not in self.plan.expected_tools:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_TOOL,
                severity=DriftSeverity.INFO,
                description=f"Tool '{tool_name}' used but not in original plan",
                expected=f"Expected tools: {', '.join(self.plan.expected_tools)}",
                actual=tool_name,
                metadata={"tool_input_preview": str(tool_input)[:100]},
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_agent_execution(
        self,
        agent_name: str,
        tool_count: int = 0,
        is_retry: bool = False,
    ) -> DetectedDrift | None:
        """Record an agent execution and check for drift."""
        self.execution.add_agent_execution(agent_name, tool_count, is_retry)

        # Check for retry drift
        if is_retry:
            drift = DetectedDrift(
                drift_type=DriftType.AGENT_RETRY,
                severity=DriftSeverity.WARNING,
                description=f"Agent '{agent_name}' was retried",
                expected="Single execution",
                actual="Retry required",
            )
            self.detected_drifts.append(drift)
            return drift

        return None

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
    ) -> List[DetectedDrift]:
        """
        Finalize execution tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.total_duration_ms = total_duration_ms
        self.execution.total_tokens = total_tokens
        self.execution.total_cost = total_cost
        self.execution.final_output = final_output

        # Perform final drift analysis
        self._analyze_agent_count()
        self._analyze_tool_coverage()

        return self.detected_drifts

    def _extract_plan_from_prompt(self, text: str) -> None:
        """Extract planning hints from system prompt."""
        # Look for tool mentions
        tool_patterns = [
            r"use (?:the )?(\w+) tool",
            r"tools?[:\s]+([A-Z][a-z]+(?:,\s*[A-Z][a-z]+)*)",
            r"can use[:\s]+([A-Z][a-z]+(?:,\s*[A-Z][a-z]+)*)",
            r"available tools?[:\s]+([A-Za-z_]+(?:,\s*[A-Za-z_]+)*)",
            r"call(?:ing)?\s+(?:the\s+)?(\w+)\s+(?:tool|function)",
        ]

        for pattern in tool_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                tools = [t.strip() for t in match.split(",")]
                self.plan.expected_tools.update(tools)

        # Look for step indicators
        step_patterns = [
            r"(?:step\s*\d+[:.]\s*)(.+?)(?=step\s*\d+|$)",
            r"(?:\d+\.\s*)(.+?)(?=\d+\.|$)",
            r"(?:first|then|next|finally)[,:]?\s+(.+?)(?=\.|first|then|next|finally|$)",
        ]

        for pattern in step_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                self.plan.planned_steps.extend(
                    [m.strip()[:100] for m in matches if len(m.strip()) > 10]
                )

    def _extract_plan_from_response(self, text: str) -> None:
        """Extract planning from agent's first response."""
        # Look for tool mentions in planning
        tool_mentions = re.findall(r"\[(?:Using|Calling)\s+(?:tool:\s*)?(\w+)\]", text)
        self.plan.expected_tools.update(tool_mentions)

        # Additional tool patterns
        tool_patterns = [
            r"(?:I'll|I will|going to)\s+(?:use|call|invoke)\s+(?:the\s+)?(\w+)",
            r"using\s+(?:the\s+)?(\w+)\s+(?:tool|function)",
        ]
        for pattern in tool_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            self.plan.expected_tools.update(matches)

        # Look for numbered lists (1. 2. 3.)
        numbered_steps = re.findall(
            r"(?:^|\n)\s*(\d+)[.)]\s*(.+?)(?=\n\s*\d+[.)]|\n\n|$)", text, re.MULTILINE
        )
        if numbered_steps and not self.plan.planned_steps:
            self.plan.planned_steps = [
                step[1].strip()[:100] for step in numbered_steps if len(step[1].strip()) > 5
            ]

        # Look for "I will..." / "I'll..." patterns
        will_patterns = re.findall(
            r"(?:I'll|I will|Let me|I'm going to)\s+(.+?)(?:\.|,|then|and then|$)",
            text,
            re.IGNORECASE,
        )
        if will_patterns and not self.plan.planned_steps:
            self.plan.planned_steps = [
                p.strip()[:100] for p in will_patterns if len(p.strip()) > 10
            ]

        # Look for expected outputs
        output_patterns = [
            r"(?:create|generate|produce|write)\s+(?:a\s+)?(.+?(?:report|file|document|response))",
            r"(?:output|result)[:\s]+(.+?)(?:\.|$)",
        ]
        for pattern in output_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            self.plan.expected_outputs.extend([m.strip() for m in matches if len(m.strip()) > 5])

    def _analyze_agent_count(self) -> None:
        """Analyze if agent count matches plan."""
        if not self.plan.expected_agents:
            return

        expected = len(self.plan.expected_agents)
        actual = len([a for a in self.execution.agents_executed if not a.get("is_retry")])

        if actual > expected:
            drift = DetectedDrift(
                drift_type=DriftType.EXTRA_AGENT,
                severity=DriftSeverity.INFO,
                description=f"More agent executions than planned ({actual} vs {expected})",
                expected=str(expected),
                actual=str(actual),
            )
            self.detected_drifts.append(drift)
        elif actual < expected:
            drift = DetectedDrift(
                drift_type=DriftType.MISSING_AGENT,
                severity=DriftSeverity.WARNING,
                description=f"Fewer agent executions than planned ({actual} vs {expected})",
                expected=str(expected),
                actual=str(actual),
            )
            self.detected_drifts.append(drift)

    def _analyze_tool_coverage(self) -> None:
        """Analyze if expected tools were used."""
        if not self.plan.expected_tools:
            return

        used_tools = set(self.execution._get_tools_summary().keys())
        missing = self.plan.expected_tools - used_tools

        if missing:
            drift = DetectedDrift(
                drift_type=DriftType.MISSING_TOOL,
                severity=DriftSeverity.INFO,
                description=f"Expected tools not used: {', '.join(missing)}",
                expected=f"Tools: {', '.join(self.plan.expected_tools)}",
                actual=f"Used: {', '.join(used_tools)}",
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


# Global drift detector instance
_global_drift_detector: DriftDetector | None = None


def get_drift_detector() -> DriftDetector:
    """
    Get or create the global drift detector instance.

    Provides a singleton pattern for drift detection, allowing
    drift to be tracked across multiple agent invocations without
    explicit passing of the detector instance.

    Returns:
        The global DriftDetector instance.
    """
    global _global_drift_detector
    if _global_drift_detector is None:
        _global_drift_detector = DriftDetector()
    return _global_drift_detector


def reset_drift_detector() -> None:
    """
    Reset the global drift detector.

    Clears all detected drifts and resets the detector state.
    Useful for testing or when starting a new monitoring session.
    """
    global _global_drift_detector
    _global_drift_detector = None
