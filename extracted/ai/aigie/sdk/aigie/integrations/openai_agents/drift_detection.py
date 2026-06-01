"""
Drift Detection for OpenAI Agents SDK Workflows.

Tracks agent execution expectations vs actual behavior to detect drifts.
Useful for monitoring agent behavior, tool usage, handoffs, and execution quality.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in OpenAI Agents workflows."""

    # Agent drifts
    UNEXPECTED_AGENT = "unexpected_agent"  # Unplanned agent activated
    MISSING_AGENT = "missing_agent"  # Expected agent not used
    AGENT_FAILURE = "agent_failure"  # Agent execution failed
    AGENT_OVERUSE = "agent_overuse"  # Agent used more than expected

    # Generation drifts
    EMPTY_GENERATION = "empty_generation"  # Empty response
    GENERATION_TRUNCATED = "generation_truncated"  # Response appears cut off
    EXCESSIVE_GENERATIONS = "excessive_generations"  # Too many LLM calls

    # Tool drifts
    UNEXPECTED_TOOL = "unexpected_tool"  # Tool used not in agent's list
    MISSING_TOOL_CALL = "missing_tool_call"  # Expected tool not called
    TOOL_FAILURE_RATE = "tool_failure_rate"  # High tool failure rate
    EXCESSIVE_TOOL_USE = "excessive_tool_use"  # Too many tool calls

    # Handoff drifts
    UNEXPECTED_HANDOFF = "unexpected_handoff"  # Unplanned handoff occurred
    MISSING_HANDOFF = "missing_handoff"  # Expected handoff didn't happen
    HANDOFF_FAILURE = "handoff_failure"  # Handoff failed
    HANDOFF_LOOP = "handoff_loop"  # Circular handoff detected

    # Guardrail drifts
    GUARDRAIL_TRIGGERED = "guardrail_triggered"  # Guardrail blocked execution
    GUARDRAIL_FAILURE = "guardrail_failure"  # Guardrail check failed

    # Workflow drifts
    WORKFLOW_FAILURE = "workflow_failure"  # Workflow did not complete
    WORKFLOW_TIMEOUT = "workflow_timeout"  # Workflow took too long

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Execution took too long
    TOKEN_ANOMALY = "token_anomaly"  # Unusual token usage
    COST_ANOMALY = "cost_anomaly"  # Unusual cost

    # Quality drifts
    LOW_QUALITY_OUTPUT = "low_quality_output"  # Output quality concerns
    INCOMPLETE_OUTPUT = "incomplete_output"  # Output seems incomplete


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
    agent_name: str | None = None
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
            "agent_name": self.agent_name,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class AgentConfig:
    """Configuration for an agent."""

    name: str
    model: str | None = None
    tools: Set[str] = field(default_factory=set)
    handoffs: Set[str] = field(default_factory=set)
    has_guardrails: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "model": self.model,
            "tools": list(self.tools),
            "handoffs": list(self.handoffs),
            "has_guardrails": self.has_guardrails,
        }


@dataclass
class WorkflowPlan:
    """Captures expected workflow behavior."""

    # Workflow info
    workflow_name: str | None = None

    # Agents
    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    expected_agents: Set[str] = field(default_factory=set)
    initial_agent: str | None = None

    # Expected tools across all agents
    all_expected_tools: Set[str] = field(default_factory=set)

    # Expected handoffs
    expected_handoffs: Set[str] = field(default_factory=set)  # "source->target" format

    # Configuration
    max_generations: int = 50
    max_tool_calls: int = 100
    max_handoffs: int = 10

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "workflow_name": self.workflow_name,
            "agents": {k: v.to_dict() for k, v in self.agents.items()},
            "expected_agents": list(self.expected_agents),
            "initial_agent": self.initial_agent,
            "all_expected_tools": list(self.all_expected_tools),
            "expected_handoffs": list(self.expected_handoffs),
            "max_generations": self.max_generations,
            "max_tool_calls": self.max_tool_calls,
            "max_handoffs": self.max_handoffs,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ExecutionTrace:
    """Tracks actual workflow execution for comparison against plan."""

    # Agent tracking
    agents_active: Set[str] = field(default_factory=set)
    agent_activations: List[Dict[str, Any]] = field(default_factory=list)

    # Generation tracking
    generations: List[Dict[str, Any]] = field(default_factory=list)
    empty_generations: int = 0

    # Tool tracking
    tools_used: Set[str] = field(default_factory=set)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_failures: int = 0

    # Handoff tracking
    handoffs: List[Dict[str, Any]] = field(default_factory=list)
    handoff_paths: Set[str] = field(default_factory=set)  # "source->target" format
    handoff_failures: int = 0

    # Guardrail tracking
    guardrail_checks: List[Dict[str, Any]] = field(default_factory=list)
    guardrail_failures: int = 0

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0

    # Result
    success: bool = False
    final_output: str | None = None

    def add_agent_activation(self, agent_name: str, model: str | None = None) -> None:
        """Record an agent activation."""
        self.agents_active.add(agent_name)
        self.agent_activations.append(
            {
                "agent_name": agent_name,
                "model": model,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def add_generation(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float = 0,
        response_length: int = 0,
        agent_name: str | None = None,
    ) -> None:
        """Record a generation."""
        self.generations.append(
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "response_length": response_length,
                "agent_name": agent_name,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += cost
        if response_length < 10:
            self.empty_generations += 1

    def add_tool_call(
        self,
        tool_name: str,
        agent_name: str,
        success: bool,
    ) -> None:
        """Record a tool call."""
        self.tool_calls.append(
            {
                "tool_name": tool_name,
                "agent_name": agent_name,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.tools_used.add(tool_name)
        if not success:
            self.tool_failures += 1

    def add_handoff(
        self,
        source_agent: str,
        target_agent: str,
        success: bool,
    ) -> None:
        """Record a handoff."""
        handoff_path = f"{source_agent}->{target_agent}"
        self.handoffs.append(
            {
                "source_agent": source_agent,
                "target_agent": target_agent,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.handoff_paths.add(handoff_path)
        if not success:
            self.handoff_failures += 1

    def add_guardrail_check(
        self,
        guardrail_name: str,
        guardrail_type: str,
        passed: bool,
    ) -> None:
        """Record a guardrail check."""
        self.guardrail_checks.append(
            {
                "guardrail_name": guardrail_name,
                "guardrail_type": guardrail_type,
                "passed": passed,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if not passed:
            self.guardrail_failures += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "agents_active": list(self.agents_active),
            "agent_activation_count": len(self.agent_activations),
            "generation_count": len(self.generations),
            "empty_generations": self.empty_generations,
            "tools_used": list(self.tools_used),
            "tool_call_count": len(self.tool_calls),
            "tool_failures": self.tool_failures,
            "handoff_count": len(self.handoffs),
            "handoff_paths": list(self.handoff_paths),
            "handoff_failures": self.handoff_failures,
            "guardrail_check_count": len(self.guardrail_checks),
            "guardrail_failures": self.guardrail_failures,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "success": self.success,
        }


class DriftDetector:
    """
    Detects drift between expected and actual workflow execution.

    Captures:
    - Workflow and agent configuration
    - Actual execution patterns
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = WorkflowPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []

    def capture_workflow_start(
        self,
        workflow_name: str,
        agents: List[str] | None = None,
    ) -> None:
        """
        Capture workflow initiation details.

        Args:
            workflow_name: Name of the workflow
            agents: List of agent names in the workflow
        """
        self.plan.workflow_name = workflow_name
        if agents:
            self.plan.expected_agents = set(agents)

    def capture_agent_config(
        self,
        agent_name: str,
        model: str | None = None,
        tools: List[str] | None = None,
        handoffs: List[str] | None = None,
        has_guardrails: bool = False,
    ) -> None:
        """
        Capture agent configuration.

        Args:
            agent_name: Name of the agent
            model: Model used by the agent
            tools: List of available tools
            handoffs: List of possible handoff targets
            has_guardrails: Whether agent has guardrails
        """
        config = AgentConfig(
            name=agent_name,
            model=model,
            tools=set(tools or []),
            handoffs=set(handoffs or []),
            has_guardrails=has_guardrails,
        )
        self.plan.agents[agent_name] = config
        self.plan.expected_agents.add(agent_name)

        # Add tools to global set
        if tools:
            self.plan.all_expected_tools.update(tools)

        # Add expected handoffs
        if handoffs:
            for target in handoffs:
                self.plan.expected_handoffs.add(f"{agent_name}->{target}")

    def record_agent_activation(
        self,
        agent_name: str,
        model: str | None = None,
    ) -> DetectedDrift | None:
        """
        Record an agent activation and check for drift.

        Returns DetectedDrift if drift is detected.
        """
        self.execution.add_agent_activation(agent_name, model)

        # Check for unexpected agent
        if agent_name not in self.plan.expected_agents:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_AGENT,
                severity=DriftSeverity.WARNING,
                description=f"Unexpected agent '{agent_name}' activated",
                expected=f"One of: {list(self.plan.expected_agents)[:5]}",
                actual=agent_name,
                agent_name=agent_name,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_generation(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float = 0,
        response: str | None = None,
        agent_name: str | None = None,
    ) -> DetectedDrift | None:
        """Record a generation and check for drift."""
        response_length = len(response) if response else 0
        self.execution.add_generation(
            model, input_tokens, output_tokens, cost, response_length, agent_name
        )

        # Check for excessive generations
        if len(self.execution.generations) > self.plan.max_generations:
            drift = DetectedDrift(
                drift_type=DriftType.EXCESSIVE_GENERATIONS,
                severity=DriftSeverity.WARNING,
                description=f"Exceeded max generations ({len(self.execution.generations)}/{self.plan.max_generations})",
                expected=f"<= {self.plan.max_generations} generations",
                actual=f"{len(self.execution.generations)} generations",
                agent_name=agent_name,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for empty generation
        if response_length < 10:
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_GENERATION,
                severity=DriftSeverity.WARNING,
                description=f"Empty or minimal generation from {model}",
                expected="Substantive response",
                actual=f"{response_length} characters",
                agent_name=agent_name,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_tool_call(
        self,
        tool_name: str,
        agent_name: str,
        success: bool,
    ) -> DetectedDrift | None:
        """Record a tool call and check for drift."""
        self.execution.add_tool_call(tool_name, agent_name, success)

        # Check for unexpected tool
        agent_config = self.plan.agents.get(agent_name)
        if agent_config and agent_config.tools and tool_name not in agent_config.tools:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_TOOL,
                severity=DriftSeverity.INFO,
                description=f"Agent '{agent_name}' used unexpected tool '{tool_name}'",
                expected=f"One of: {list(agent_config.tools)[:5]}",
                actual=tool_name,
                agent_name=agent_name,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for excessive tool calls
        if len(self.execution.tool_calls) > self.plan.max_tool_calls:
            drift = DetectedDrift(
                drift_type=DriftType.EXCESSIVE_TOOL_USE,
                severity=DriftSeverity.WARNING,
                description=f"Exceeded max tool calls ({len(self.execution.tool_calls)}/{self.plan.max_tool_calls})",
                expected=f"<= {self.plan.max_tool_calls} calls",
                actual=f"{len(self.execution.tool_calls)} calls",
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_handoff(
        self,
        source_agent: str,
        target_agent: str,
        success: bool,
    ) -> DetectedDrift | None:
        """Record a handoff and check for drift."""
        self.execution.add_handoff(source_agent, target_agent, success)

        handoff_path = f"{source_agent}->{target_agent}"

        # Check for unexpected handoff
        if self.plan.expected_handoffs and handoff_path not in self.plan.expected_handoffs:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_HANDOFF,
                severity=DriftSeverity.INFO,
                description=f"Unexpected handoff: {source_agent} -> {target_agent}",
                expected=f"One of: {list(self.plan.expected_handoffs)[:5]}",
                actual=handoff_path,
                agent_name=source_agent,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for handoff failure
        if not success:
            drift = DetectedDrift(
                drift_type=DriftType.HANDOFF_FAILURE,
                severity=DriftSeverity.WARNING,
                description=f"Handoff from '{source_agent}' to '{target_agent}' failed",
                agent_name=source_agent,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for excessive handoffs
        if len(self.execution.handoffs) > self.plan.max_handoffs:
            drift = DetectedDrift(
                drift_type=DriftType.HANDOFF_LOOP,
                severity=DriftSeverity.WARNING,
                description=f"Exceeded max handoffs ({len(self.execution.handoffs)}/{self.plan.max_handoffs}), possible loop",
                expected=f"<= {self.plan.max_handoffs} handoffs",
                actual=f"{len(self.execution.handoffs)} handoffs",
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_guardrail(
        self,
        guardrail_name: str,
        guardrail_type: str,
        passed: bool,
    ) -> DetectedDrift | None:
        """Record a guardrail check and check for drift."""
        self.execution.add_guardrail_check(guardrail_name, guardrail_type, passed)

        if not passed:
            drift = DetectedDrift(
                drift_type=DriftType.GUARDRAIL_TRIGGERED,
                severity=DriftSeverity.WARNING,
                description=f"Guardrail '{guardrail_name}' ({guardrail_type}) blocked execution",
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def finalize(
        self,
        success: bool,
        output: Any | None = None,
        error: str | None = None,
        total_duration_ms: float = 0,
    ) -> List[DetectedDrift]:
        """
        Finalize workflow tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.success = success
        self.execution.total_duration_ms = total_duration_ms
        if output:
            self.execution.final_output = str(output)[:1000]

        # Check for missing agents
        if self.plan.expected_agents:
            missing = self.plan.expected_agents - self.execution.agents_active
            for agent in missing:
                drift = DetectedDrift(
                    drift_type=DriftType.MISSING_AGENT,
                    severity=DriftSeverity.INFO,
                    description=f"Expected agent '{agent}' was not activated",
                    expected="Agent activated",
                    actual="Agent never used",
                    agent_name=agent,
                )
                self.detected_drifts.append(drift)

        # Check for high tool failure rate
        total_tool_calls = len(self.execution.tool_calls)
        if total_tool_calls > 0:
            failure_rate = self.execution.tool_failures / total_tool_calls
            if failure_rate > 0.3:
                drift = DetectedDrift(
                    drift_type=DriftType.TOOL_FAILURE_RATE,
                    severity=DriftSeverity.WARNING,
                    description=f"High tool failure rate: {failure_rate:.1%}",
                    expected="< 30% failure rate",
                    actual=f"{failure_rate:.1%} ({self.execution.tool_failures}/{total_tool_calls})",
                )
                self.detected_drifts.append(drift)

        # Check for workflow failure
        if not success:
            drift = DetectedDrift(
                drift_type=DriftType.WORKFLOW_FAILURE,
                severity=DriftSeverity.ALERT,
                description=f"Workflow failed: {error[:100] if error else 'unknown'}",
                expected="Successful completion",
                actual=f"Failed: {error[:50] if error else 'unknown'}",
            )
            self.detected_drifts.append(drift)

        return self.detected_drifts

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of expected vs actual execution."""
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
            return "No drifts detected - workflow execution matched expectations"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}"
            if drift.agent_name:
                report += f" (agent: {drift.agent_name})"
            report += f"\n   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report
