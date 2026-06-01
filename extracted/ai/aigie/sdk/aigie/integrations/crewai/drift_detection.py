"""
Drift Detection for CrewAI Workflows.

Tracks crew execution expectations vs actual behavior to detect drifts.
Useful for monitoring agent behavior, task completion, and execution quality.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in CrewAI workflows."""

    # Task drifts
    TASK_FAILURE = "task_failure"  # Task did not complete
    TASK_MISSING_OUTPUT = "task_missing_output"  # Expected output not produced
    TASK_SKIPPED = "task_skipped"  # Task was not executed
    TASK_REORDERING = "task_reordering"  # Tasks executed out of order

    # Agent drifts
    AGENT_OVERUSE = "agent_overuse"  # Agent used more than expected
    AGENT_UNDERUSE = "agent_underuse"  # Agent used less than expected
    WRONG_AGENT = "wrong_agent"  # Task assigned to unexpected agent
    AGENT_STUCK = "agent_stuck"  # Agent in repetitive loop

    # Step drifts
    EXCESSIVE_STEPS = "excessive_steps"  # Too many steps to complete
    STEP_FAILURE = "step_failure"  # Step failed
    STEP_LOOP = "step_loop"  # Repetitive step pattern

    # Tool drifts
    UNEXPECTED_TOOL = "unexpected_tool"  # Tool used not expected
    MISSING_TOOL_USE = "missing_tool_use"  # Expected tool not used
    TOOL_FAILURE_RATE = "tool_failure_rate"  # High tool failure rate
    EXCESSIVE_TOOL_USE = "excessive_tool_use"  # Too many tool calls

    # Delegation drifts
    UNEXPECTED_DELEGATION = "unexpected_delegation"  # Unplanned delegation
    DELEGATION_FAILURE = "delegation_failure"  # Delegation did not succeed
    DELEGATION_LOOP = "delegation_loop"  # Circular delegation

    # Output drifts
    OUTPUT_LENGTH_ANOMALY = "output_length_anomaly"  # Unusual output length
    EMPTY_OUTPUT = "empty_output"  # Empty or minimal output

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Task took too long
    TOKEN_ANOMALY = "token_anomaly"  # Unusual token usage
    COST_ANOMALY = "cost_anomaly"  # Unusual cost

    # Quality drifts
    INCOMPLETE_RESULT = "incomplete_result"  # Result seems incomplete
    LOW_QUALITY_OUTPUT = "low_quality_output"  # Output quality concerns


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
    agent_role: str | None = None
    task_id: str | None = None
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
            "agent_role": self.agent_role,
            "task_id": self.task_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class PlannedTask:
    """Represents a planned task in the crew."""

    task_id: str
    description: str
    agent_role: str
    expected_output: str | None = None
    context_from: List[str] = field(default_factory=list)  # Task IDs providing context

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description[:200],
            "agent_role": self.agent_role,
            "expected_output": self.expected_output[:100] if self.expected_output else None,
            "context_from": self.context_from,
        }


@dataclass
class CrewPlan:
    """Captures expected crew behavior."""

    # Crew config
    crew_name: str | None = None
    process_type: str = "sequential"  # sequential, hierarchical

    # Agents
    agent_roles: Set[str] = field(default_factory=set)

    # Tasks
    planned_tasks: List[PlannedTask] = field(default_factory=list)
    task_order: List[str] = field(default_factory=list)

    # Expected behaviors
    expected_tools: Set[str] = field(default_factory=set)
    allow_delegation: bool = False
    max_steps_per_task: int = 25

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "crew_name": self.crew_name,
            "process_type": self.process_type,
            "agent_roles": list(self.agent_roles),
            "task_count": len(self.planned_tasks),
            "task_order": self.task_order,
            "expected_tools": list(self.expected_tools),
            "allow_delegation": self.allow_delegation,
            "max_steps_per_task": self.max_steps_per_task,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ExecutionTrace:
    """Tracks actual crew execution for comparison against plan."""

    # Task tracking
    tasks_started: List[str] = field(default_factory=list)
    tasks_completed: List[str] = field(default_factory=list)
    tasks_failed: List[str] = field(default_factory=list)

    # Agent tracking
    agents_active: Set[str] = field(default_factory=set)
    steps_by_agent: Dict[str, int] = field(default_factory=dict)

    # Step tracking
    total_steps: int = 0
    steps_by_task: Dict[str, int] = field(default_factory=dict)

    # Tool tracking
    tools_used: Set[str] = field(default_factory=set)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_failures: int = 0

    # Delegation tracking
    delegations: List[Dict[str, Any]] = field(default_factory=list)
    delegation_failures: int = 0

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0

    # Result
    success: bool = False
    final_output: str | None = None

    def add_task_start(self, task_id: str, agent_role: str) -> None:
        """Record a task starting."""
        self.tasks_started.append(task_id)
        self.agents_active.add(agent_role)

    def add_task_end(self, task_id: str, success: bool, output: str | None = None) -> None:
        """Record a task ending."""
        if success:
            self.tasks_completed.append(task_id)
        else:
            self.tasks_failed.append(task_id)

    def add_step(self, agent_role: str, task_id: str) -> None:
        """Record an agent step."""
        self.total_steps += 1
        self.steps_by_agent[agent_role] = self.steps_by_agent.get(agent_role, 0) + 1
        self.steps_by_task[task_id] = self.steps_by_task.get(task_id, 0) + 1

    def add_tool_call(
        self,
        tool_name: str,
        agent_role: str,
        success: bool,
    ) -> None:
        """Record a tool call."""
        self.tool_calls.append(
            {
                "tool_name": tool_name,
                "agent_role": agent_role,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.tools_used.add(tool_name)
        if not success:
            self.tool_failures += 1

    def add_delegation(
        self,
        from_agent: str,
        to_agent: str,
        success: bool,
    ) -> None:
        """Record a delegation."""
        self.delegations.append(
            {
                "from_agent": from_agent,
                "to_agent": to_agent,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if not success:
            self.delegation_failures += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "tasks_started": self.tasks_started,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "agents_active": list(self.agents_active),
            "steps_by_agent": self.steps_by_agent,
            "total_steps": self.total_steps,
            "steps_by_task": self.steps_by_task,
            "tools_used": list(self.tools_used),
            "tool_call_count": len(self.tool_calls),
            "tool_failures": self.tool_failures,
            "delegation_count": len(self.delegations),
            "delegation_failures": self.delegation_failures,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "success": self.success,
        }


class DriftDetector:
    """
    Detects drift between expected and actual crew execution.

    Captures:
    - Crew and task configuration
    - Actual agent and task execution
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = CrewPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []

    def capture_crew_start(
        self,
        crew_name: str,
        agents: List[Dict[str, Any]],
        tasks: List[Dict[str, Any]],
        process_type: str = "sequential",
    ) -> None:
        """
        Capture crew configuration at start.

        Args:
            crew_name: Name of the crew
            agents: List of agent configurations
            tasks: List of task configurations
            process_type: Type of process (sequential/hierarchical)
        """
        self.plan.crew_name = crew_name
        self.plan.process_type = process_type

        # Extract agent roles
        for agent in agents:
            role = agent.get("role", agent.get("name", "unknown"))
            self.plan.agent_roles.add(role)
            # Check for tools
            if "tools" in agent:
                for tool in agent.get("tools", []):
                    tool_name = (
                        tool if isinstance(tool, str) else getattr(tool, "__name__", str(tool))
                    )
                    self.plan.expected_tools.add(tool_name)

        # Extract tasks
        for i, task in enumerate(tasks):
            task_id = task.get("id", f"task_{i}")
            planned_task = PlannedTask(
                task_id=task_id,
                description=task.get("description", "")[:200],
                agent_role=task.get("agent", {}).get("role", "unknown")
                if isinstance(task.get("agent"), dict)
                else str(task.get("agent", "unknown")),
                expected_output=task.get("expected_output"),
                context_from=task.get("context", []),
            )
            self.plan.planned_tasks.append(planned_task)
            self.plan.task_order.append(task_id)

        # Check allow delegation
        self.plan.allow_delegation = any(agent.get("allow_delegation", False) for agent in agents)

    def capture_expected_tools(self, tools: List[str]) -> None:
        """Capture expected tools that may be called."""
        self.plan.expected_tools = set(tools)

    def record_task_start(
        self,
        task_id: str,
        description: str,
        agent_role: str,
    ) -> DetectedDrift | None:
        """Record a task starting and check for drift."""
        self.execution.add_task_start(task_id, agent_role)

        # Check task ordering (for sequential process)
        if self.plan.process_type == "sequential" and self.plan.task_order:
            expected_index = len(self.execution.tasks_started) - 1
            if expected_index < len(self.plan.task_order):
                expected_task = self.plan.task_order[expected_index]
                if task_id != expected_task:
                    drift = DetectedDrift(
                        drift_type=DriftType.TASK_REORDERING,
                        severity=DriftSeverity.WARNING,
                        description=f"Task '{task_id}' executed out of order",
                        expected=f"Task '{expected_task}' at position {expected_index}",
                        actual=f"Task '{task_id}' at position {expected_index}",
                        task_id=task_id,
                    )
                    self.detected_drifts.append(drift)
                    return drift

        # Check for wrong agent
        planned = next((t for t in self.plan.planned_tasks if t.task_id == task_id), None)
        if planned and planned.agent_role != agent_role:
            drift = DetectedDrift(
                drift_type=DriftType.WRONG_AGENT,
                severity=DriftSeverity.WARNING,
                description=f"Task '{task_id}' assigned to different agent",
                expected=f"Agent: {planned.agent_role}",
                actual=f"Agent: {agent_role}",
                agent_role=agent_role,
                task_id=task_id,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_task_end(
        self,
        task_id: str,
        output: str | None = None,
        success: bool = True,
    ) -> DetectedDrift | None:
        """Record a task ending and check for drift."""
        self.execution.add_task_end(task_id, success, output)

        if not success:
            drift = DetectedDrift(
                drift_type=DriftType.TASK_FAILURE,
                severity=DriftSeverity.ALERT,
                description=f"Task '{task_id}' failed to complete",
                expected="Successful completion",
                actual="Task failed",
                task_id=task_id,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for empty output
        if not output or len(output.strip()) < 10:
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_OUTPUT,
                severity=DriftSeverity.WARNING,
                description=f"Task '{task_id}' produced empty or minimal output",
                task_id=task_id,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_agent_step(
        self,
        agent_role: str,
        step_number: int,
        task_id: str,
        action: str | None = None,
    ) -> DetectedDrift | None:
        """Record an agent step and check for drift."""
        self.execution.add_step(agent_role, task_id)

        # Check for excessive steps
        task_steps = self.execution.steps_by_task.get(task_id, 0)
        if task_steps > self.plan.max_steps_per_task:
            drift = DetectedDrift(
                drift_type=DriftType.EXCESSIVE_STEPS,
                severity=DriftSeverity.WARNING,
                description=f"Task '{task_id}' exceeded max steps ({task_steps}/{self.plan.max_steps_per_task})",
                expected=f"<= {self.plan.max_steps_per_task} steps",
                actual=f"{task_steps} steps",
                agent_role=agent_role,
                task_id=task_id,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_tool_call(
        self,
        tool_name: str,
        agent_role: str,
        success: bool,
    ) -> DetectedDrift | None:
        """Record a tool call and check for drift."""
        self.execution.add_tool_call(tool_name, agent_role, success)

        # Check for unexpected tool
        if self.plan.expected_tools and tool_name not in self.plan.expected_tools:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_TOOL,
                severity=DriftSeverity.INFO,
                description=f"Unexpected tool '{tool_name}' used by '{agent_role}'",
                expected=f"One of: {list(self.plan.expected_tools)[:5]}",
                actual=tool_name,
                agent_role=agent_role,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_delegation(
        self,
        from_agent: str,
        to_agent: str,
        success: bool,
    ) -> DetectedDrift | None:
        """Record a delegation and check for drift."""
        self.execution.add_delegation(from_agent, to_agent, success)

        # Check for unexpected delegation
        if not self.plan.allow_delegation:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_DELEGATION,
                severity=DriftSeverity.WARNING,
                description=f"Unexpected delegation from '{from_agent}' to '{to_agent}'",
                expected="No delegation (not allowed)",
                actual=f"Delegation: {from_agent} -> {to_agent}",
                agent_role=from_agent,
            )
            self.detected_drifts.append(drift)
            return drift

        if not success:
            drift = DetectedDrift(
                drift_type=DriftType.DELEGATION_FAILURE,
                severity=DriftSeverity.WARNING,
                description=f"Delegation from '{from_agent}' to '{to_agent}' failed",
                agent_role=from_agent,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_llm_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        cost: float,
    ) -> None:
        """Record LLM token and cost usage."""
        self.execution.total_tokens += input_tokens + output_tokens
        self.execution.total_cost += cost

    def finalize(
        self,
        success: bool,
        result: Any | None = None,
        error: str | None = None,
        total_duration_ms: float = 0,
    ) -> List[DetectedDrift]:
        """
        Finalize crew tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.success = success
        self.execution.total_duration_ms = total_duration_ms
        if result:
            self.execution.final_output = str(result)[:1000]

        # Check for skipped tasks
        started_set = set(self.execution.tasks_started)
        for planned in self.plan.planned_tasks:
            if planned.task_id not in started_set:
                drift = DetectedDrift(
                    drift_type=DriftType.TASK_SKIPPED,
                    severity=DriftSeverity.WARNING,
                    description=f"Planned task '{planned.task_id}' was never started",
                    expected="Task executed",
                    actual="Task skipped",
                    task_id=planned.task_id,
                    agent_role=planned.agent_role,
                )
                self.detected_drifts.append(drift)

        # Check for missing tool usage
        if self.plan.expected_tools:
            missing = self.plan.expected_tools - self.execution.tools_used
            for tool in missing:
                drift = DetectedDrift(
                    drift_type=DriftType.MISSING_TOOL_USE,
                    severity=DriftSeverity.INFO,
                    description=f"Expected tool '{tool}' was not used",
                    expected="Tool used during execution",
                    actual="Tool never invoked",
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

        # Check for incomplete result
        if not success and error:
            drift = DetectedDrift(
                drift_type=DriftType.INCOMPLETE_RESULT,
                severity=DriftSeverity.ALERT,
                description=f"Crew execution incomplete: {error[:100]}",
                expected="Successful completion",
                actual=f"Failed: {error[:50]}",
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
            return "No drifts detected - crew execution matched expectations"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}"
            if drift.task_id:
                report += f" (task: {drift.task_id})"
            if drift.agent_role:
                report += f" (agent: {drift.agent_role})"
            report += f"\n   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report
