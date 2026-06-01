"""
Drift Detection for LangChain Workflows.

Tracks chain/agent planning vs actual execution to detect behavioral drifts.
Useful for monitoring workflow reliability and detecting deviations.
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

    # Chain/agent drifts
    EXTRA_CHAIN = "extra_chain"  # More chains executed than planned
    MISSING_CHAIN = "missing_chain"  # Fewer chains than planned
    CHAIN_RETRY = "chain_retry"  # Chain had to be retried

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
class WorkflowPlan:
    """Captures the workflow's plan/intent for execution."""

    # Raw planning text
    raw_plan: str | None = None
    system_prompt: str | None = None
    initial_input: str | None = None

    # Extracted plan components
    planned_steps: List[str] = field(default_factory=list)
    expected_tools: Set[str] = field(default_factory=set)
    expected_chains: List[Dict[str, str]] = field(default_factory=list)
    expected_outputs: List[str] = field(default_factory=list)

    # Planning chain outputs (from chains like "planner", "think", etc.)
    planning_chain_outputs: List[Dict[str, Any]] = field(default_factory=list)

    # Plan metadata
    timestamp: datetime = field(default_factory=datetime.now)
    model: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "raw_plan": self.raw_plan,
            "system_prompt": self.system_prompt if self.system_prompt else None,
            "initial_input_preview": self.initial_input[:200] if self.initial_input else None,
            "planned_steps": self.planned_steps,
            "expected_tools": list(self.expected_tools),
            "expected_chains": self.expected_chains,
            "expected_outputs": self.expected_outputs,
            "planning_chain_outputs": self.planning_chain_outputs,
            "timestamp": self.timestamp.isoformat(),
            "model": self.model,
        }


@dataclass
class ExecutionTrace:
    """Tracks actual execution for comparison against plan."""

    # Execution events
    tools_used: List[Dict[str, Any]] = field(default_factory=list)
    chains_executed: List[Dict[str, Any]] = field(default_factory=list)
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

    def add_chain(
        self, chain_name: str, chain_type: str, duration_ms: float = 0, is_retry: bool = False
    ) -> None:
        """Record a chain execution."""
        self.chains_executed.append(
            {
                "chain_name": chain_name,
                "chain_type": chain_type,
                "duration_ms": duration_ms,
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
            "chains_executed": self.chains_executed,
            "chains_summary": self._get_chains_summary(),
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

    def _get_chains_summary(self) -> Dict[str, int]:
        """Get summary of chains executed."""
        summary = {}
        for chain in self.chains_executed:
            name = chain["chain_name"]
            summary[name] = summary.get(name, 0) + 1
        return summary


class DriftDetector:
    """
    Detects drift between workflow planning and actual execution.

    Captures:
    - Initial plan from chain inputs and first responses
    - Actual execution path (tools, chains, outputs)
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = WorkflowPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []
        self._plan_captured = False
        self._max_plan_length: int = 2000

    def capture_system_prompt(self, system_prompt: str) -> None:
        """Capture system prompt for plan extraction."""
        self.plan.system_prompt = system_prompt
        self._extract_plan_from_prompt(system_prompt)

    def capture_initial_input(self, input_data: Any) -> None:
        """Capture initial workflow input."""
        if isinstance(input_data, dict):
            self.plan.initial_input = str(input_data.get("input", input_data))[:500]
        else:
            self.plan.initial_input = str(input_data)[:500]

    def capture_planning_chain_output(
        self,
        chain_name: str,
        chain_type: str,
        output: Any,
        is_planning_chain: bool = False,
    ) -> None:
        """
        Capture output from a planning chain.

        Planning chains are chains that contain planning logic, typically named:
        - planner, plan, planning
        - think, thinking, reason, reasoning
        - decide, decision
        - route, router
        """
        output_str = str(output) if output else ""

        # Check if this looks like a planning chain by name
        planning_keywords = {
            "planner",
            "plan",
            "planning",
            "think",
            "thinking",
            "reason",
            "reasoning",
            "decide",
            "decision",
            "route",
            "router",
        }
        chain_lower = chain_name.lower()
        is_planning = is_planning_chain or any(kw in chain_lower for kw in planning_keywords)

        if is_planning and output_str:
            self.plan.planning_chain_outputs.append(
                {
                    "chain_name": chain_name,
                    "chain_type": chain_type,
                    "output_preview": output_str[:1000],
                    "timestamp": datetime.now().isoformat(),
                }
            )
            # Store full plan text (up to max length)
            self.plan.raw_plan = output_str[: self._max_plan_length]
            # Extract planning from this output
            self._extract_plan_from_response(output_str)
            self._plan_captured = True

    def capture_planning_response(self, response_text: str, model: str | None = None) -> None:
        """
        Capture agent's/chain's planning response (typically first response).

        Looks for planning patterns like:
        - "I'll first..."
        - "Steps: 1. ... 2. ..."
        - "Using tools: ..."
        """
        if self._plan_captured:
            return

        self.plan.raw_plan = response_text[: self._max_plan_length]
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

    def record_chain_execution(
        self,
        chain_name: str,
        chain_type: str,
        duration_ms: float = 0,
        is_retry: bool = False,
    ) -> DetectedDrift | None:
        """Record a chain execution and check for drift."""
        self.execution.add_chain(chain_name, chain_type, duration_ms, is_retry)

        # Check for retry drift
        if is_retry:
            drift = DetectedDrift(
                drift_type=DriftType.CHAIN_RETRY,
                severity=DriftSeverity.WARNING,
                description=f"Chain '{chain_name}' was retried",
                expected="Single execution",
                actual="Retry required",
                metadata={"chain_type": chain_type},
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
        self._analyze_chain_count()
        self._analyze_tool_coverage()

        return self.detected_drifts

    def _extract_plan_from_prompt(self, text: str) -> None:
        """Extract planning hints from system prompt."""
        if not text:
            return

        # Extract tool definitions/mentions from prompt
        tool_patterns = [
            r"use (?:the )?(\w+) tool",
            r"tools?[:\s]+\[([^\]]+)\]",  # tools: [search, analyze]
            r"tools?[:\s]+([A-Z][a-z]+(?:,\s*[A-Z][a-z]+)*)",
            r"can use[:\s]+([A-Z][a-z]+(?:,\s*[A-Z][a-z]+)*)",
            r"available tools?[:\s]*([^\n]+)",
            r"you (?:have access to|can use)[:\s]*([^\n]+tools?[^\n]*)",
        ]

        for pattern in tool_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract individual tool names
                tools = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", match)
                # Filter out common words
                stopwords = {
                    "the",
                    "and",
                    "or",
                    "to",
                    "a",
                    "an",
                    "use",
                    "using",
                    "tools",
                    "tool",
                    "following",
                }
                self.plan.expected_tools.update(t for t in tools if t.lower() not in stopwords)

        # Look for step indicators
        step_patterns = [
            r"(?:step\s*\d+[:.]\s*)(.+?)(?=step\s*\d+|$)",
            r"(?:\d+\.\s*)(.+?)(?=\d+\.|$)",
            r"(?:first|then|next|finally)[,:\s]+([^\n]+)",
        ]

        for pattern in step_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                for m in matches:
                    step_text = m.strip()[:200]
                    if len(step_text) > 5 and step_text not in self.plan.planned_steps:
                        self.plan.planned_steps.append(step_text)

    def _extract_plan_from_response(self, text: str) -> None:
        """Extract planning from agent's/chain's first response with improved pattern matching."""
        if not text:
            return

        # Look for tool mentions - multiple patterns
        tool_patterns = [
            r"\[(?:Using|Tool)[:\s]*(\w+)\]",  # [Using: search]
            r"(?:use|using|call|calling)\s+(?:the\s+)?(\w+)\s+tool",  # use the search tool
            r"(?:invoke|invoking)\s+(?:the\s+)?(\w+)",  # invoke search
            r"tool[:\s]+['\"]?(\w+)['\"]?",  # tool: "search"
            r"function[:\s]+['\"]?(\w+)['\"]?",  # function: "search"
        ]
        for pattern in tool_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            self.plan.expected_tools.update(matches)

        # Extract planned steps from numbered lists
        numbered_steps = re.findall(r"(?:^|\n)\s*(\d+)[.):]\s*([^\n]+)", text)
        for num, step in numbered_steps:
            step_text = step.strip()
            if step_text and len(step_text) > 5 and step_text not in self.plan.planned_steps:
                self.plan.planned_steps.append(step_text[:200])

        # Extract steps from "I will..." or "Let me..." patterns
        plan_patterns = [
            r"(?:I will|I'll|I'm going to|Let me|My plan is to)[:\s]*([^\n.]+)",
            r"(?:First|Then|Next|Finally|After that)[,:\s]+(?:I will|I'll|we)?[:\s]*([^\n.]+)",
            r"(?:Step \d+|Phase \d+)[:\s]*([^\n]+)",
        ]
        for pattern in plan_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                step_text = match.strip()
                if step_text and len(step_text) > 5 and step_text not in self.plan.planned_steps:
                    self.plan.planned_steps.append(step_text[:200])

        # Extract from arrow notation: search -> analyze -> output
        arrow_pattern = r"(\w+)\s*(?:->|→|=>)\s*(\w+)"
        arrow_matches = re.findall(arrow_pattern, text)
        for from_step, to_step in arrow_matches:
            if from_step not in self.plan.planned_steps:
                self.plan.planned_steps.append(from_step)
            if to_step not in self.plan.planned_steps:
                self.plan.planned_steps.append(to_step)

        # Look for expected outputs
        output_patterns = [
            r"(?:create|generate|produce|write|return)\s+(?:a\s+)?(.+?(?:report|response|answer|output|result))",
            r"(?:output|result)[:\s]+(.+?)(?:\.|$)",
        ]
        for pattern in output_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            self.plan.expected_outputs.extend([m.strip() for m in matches if len(m.strip()) > 5])

    def _analyze_chain_count(self) -> None:
        """Analyze if chain execution count matches plan."""
        if not self.plan.expected_chains:
            return

        expected = len(self.plan.expected_chains)
        actual = len([c for c in self.execution.chains_executed if not c.get("is_retry")])

        if actual > expected:
            drift = DetectedDrift(
                drift_type=DriftType.EXTRA_CHAIN,
                severity=DriftSeverity.INFO,
                description=f"More chains executed than planned ({actual} vs {expected})",
                expected=str(expected),
                actual=str(actual),
            )
            self.detected_drifts.append(drift)
        elif actual < expected:
            drift = DetectedDrift(
                drift_type=DriftType.MISSING_CHAIN,
                severity=DriftSeverity.WARNING,
                description=f"Fewer chains executed than planned ({actual} vs {expected})",
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

    def get_plan_metadata(self, source: str = "first_llm_response") -> Dict[str, Any] | None:
        """
        Returns structured plan metadata for TRACE_UPDATE.

        Returns None if no plan has been captured yet.
        """
        if not self._plan_captured or not self.plan.raw_plan:
            return None

        return {
            "raw_plan": self.plan.raw_plan,
            "planned_steps": self.plan.planned_steps,
            "expected_tools": list(self.plan.expected_tools),
            "source": source,
            "model": self.plan.model,
            "detected_at": datetime.now().isoformat(),
        }

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
