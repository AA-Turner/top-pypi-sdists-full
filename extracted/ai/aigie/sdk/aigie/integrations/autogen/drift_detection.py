"""
Drift Detection for AutoGen/AG2 Multi-Agent Workflows.

Tracks conversation flow expectations vs actual execution to detect drifts.
Useful for monitoring agent behavior, conversation patterns, and execution quality.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in AutoGen workflows."""

    # Conversation drifts
    UNEXPECTED_TERMINATION = "unexpected_termination"  # Ended early
    TURN_LIMIT_REACHED = "turn_limit_reached"  # Hit max turns
    CONVERSATION_LOOP = "conversation_loop"  # Repetitive patterns

    # Agent drifts
    UNEXPECTED_AGENT = "unexpected_agent"  # Unplanned agent spoke
    MISSING_AGENT = "missing_agent"  # Expected agent didn't act
    AGENT_OVERUSE = "agent_overuse"  # Agent spoke too often
    AGENT_UNDERUSE = "agent_underuse"  # Agent spoke less than expected

    # Tool drifts
    UNEXPECTED_TOOL = "unexpected_tool"  # Unplanned tool called
    MISSING_TOOL_CALL = "missing_tool_call"  # Expected tool not called
    TOOL_FAILURE_RATE = "tool_failure_rate"  # Too many tool failures
    EXCESSIVE_TOOL_USE = "excessive_tool_use"  # Too many tool calls

    # Code execution drifts
    UNEXPECTED_CODE = "unexpected_code"  # Unplanned code execution
    CODE_FAILURE_RATE = "code_failure_rate"  # Too many code failures
    EXCESSIVE_CODE_EXEC = "excessive_code_exec"  # Too many code blocks

    # Message drifts
    MESSAGE_LENGTH_ANOMALY = "message_length_anomaly"  # Unusual message length
    EMPTY_RESPONSE = "empty_response"  # Agent returned empty

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Conversation took too long
    TOKEN_ANOMALY = "token_anomaly"  # Unusual token usage
    COST_ANOMALY = "cost_anomaly"  # Unusual cost

    # Quality drifts
    LOW_QUALITY_OUTPUT = "low_quality_output"  # Output seems poor
    INCOMPLETE_TASK = "incomplete_task"  # Task not fully completed


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
class ConversationPlan:
    """Captures expected conversation behavior."""

    # Agents
    initiator: str | None = None
    recipient: str | None = None
    expected_agents: Set[str] = field(default_factory=set)

    # Configuration
    max_turns: int | None = None
    conversation_type: str = "two_agent"  # two_agent, group_chat

    # Expectations
    expected_tools: Set[str] = field(default_factory=set)
    expected_code_execution: bool = False

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "initiator": self.initiator,
            "recipient": self.recipient,
            "expected_agents": list(self.expected_agents),
            "max_turns": self.max_turns,
            "conversation_type": self.conversation_type,
            "expected_tools": list(self.expected_tools),
            "expected_code_execution": self.expected_code_execution,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ExecutionTrace:
    """Tracks actual execution for comparison against plan."""

    # Conversation tracking
    turns: List[Dict[str, Any]] = field(default_factory=list)
    messages: List[Dict[str, Any]] = field(default_factory=list)

    # Agent tracking
    agents_active: Set[str] = field(default_factory=set)
    messages_by_agent: Dict[str, int] = field(default_factory=dict)

    # Tool tracking
    tools_called: Set[str] = field(default_factory=set)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_failures: int = 0

    # Code execution tracking
    code_executions: List[Dict[str, Any]] = field(default_factory=list)
    code_failures: int = 0

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0
    turn_count: int = 0
    message_count: int = 0

    # Result
    success: bool = False
    termination_reason: str | None = None

    def add_turn(
        self,
        turn_number: int,
        sender: str,
        recipient: str,
    ) -> None:
        """Record a conversation turn."""
        self.turns.append(
            {
                "turn_number": turn_number,
                "sender": sender,
                "recipient": recipient,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.turn_count = max(self.turn_count, turn_number)
        self.agents_active.add(sender)
        self.agents_active.add(recipient)

    def add_message(
        self,
        sender: str,
        recipient: str,
        content_length: int,
    ) -> None:
        """Record a message exchange."""
        self.messages.append(
            {
                "sender": sender,
                "recipient": recipient,
                "content_length": content_length,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.message_count += 1
        self.messages_by_agent[sender] = self.messages_by_agent.get(sender, 0) + 1

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
        self.tools_called.add(tool_name)
        if not success:
            self.tool_failures += 1

    def add_code_execution(
        self,
        language: str,
        exit_code: int,
        agent_name: str | None = None,
    ) -> None:
        """Record a code execution."""
        success = exit_code == 0
        self.code_executions.append(
            {
                "language": language,
                "exit_code": exit_code,
                "success": success,
                "agent_name": agent_name,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if not success:
            self.code_failures += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "turn_count": self.turn_count,
            "message_count": self.message_count,
            "agents_active": list(self.agents_active),
            "messages_by_agent": self.messages_by_agent,
            "tools_called": list(self.tools_called),
            "tool_call_count": len(self.tool_calls),
            "tool_failures": self.tool_failures,
            "code_execution_count": len(self.code_executions),
            "code_failures": self.code_failures,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "success": self.success,
            "termination_reason": self.termination_reason,
        }


class DriftDetector:
    """
    Detects drift between expected and actual conversation behavior.

    Captures:
    - Conversation flow expectations
    - Actual agent interactions
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = ConversationPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []

    def capture_conversation_start(
        self,
        initiator: str,
        recipient: str,
        max_turns: int | None = None,
        conversation_type: str = "two_agent",
    ) -> None:
        """
        Capture conversation initiation details.

        Args:
            initiator: Name of the initiating agent
            recipient: Name of the recipient agent
            max_turns: Maximum turns configured
            conversation_type: Type of conversation
        """
        self.plan.initiator = initiator
        self.plan.recipient = recipient
        self.plan.max_turns = max_turns
        self.plan.conversation_type = conversation_type
        self.plan.expected_agents.add(initiator)
        self.plan.expected_agents.add(recipient)

    def capture_group_chat_start(
        self,
        agents: List[str],
        max_rounds: int | None = None,
    ) -> None:
        """
        Capture group chat initiation.

        Args:
            agents: List of agent names
            max_rounds: Maximum rounds configured
        """
        self.plan.conversation_type = "group_chat"
        self.plan.expected_agents = set(agents)
        self.plan.max_turns = max_rounds

    def capture_expected_tools(self, tools: List[str]) -> None:
        """Capture expected tools that may be called."""
        self.plan.expected_tools = set(tools)

    def capture_expected_code_execution(self, expected: bool = True) -> None:
        """Capture whether code execution is expected."""
        self.plan.expected_code_execution = expected

    def record_turn(
        self,
        turn_number: int,
        sender: str,
        recipient: str,
    ) -> DetectedDrift | None:
        """
        Record a conversation turn and check for drift.

        Returns DetectedDrift if drift is detected.
        """
        self.execution.add_turn(turn_number, sender, recipient)

        # Check for unexpected agent
        if sender not in self.plan.expected_agents:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_AGENT,
                severity=DriftSeverity.WARNING,
                description=f"Unexpected agent '{sender}' participated in conversation",
                expected=f"One of: {list(self.plan.expected_agents)}",
                actual=sender,
                agent_name=sender,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for turn limit approaching
        if self.plan.max_turns and turn_number >= self.plan.max_turns - 1:
            drift = DetectedDrift(
                drift_type=DriftType.TURN_LIMIT_REACHED,
                severity=DriftSeverity.WARNING,
                description=f"Approaching or reached turn limit ({turn_number + 1}/{self.plan.max_turns})",
                expected=f"Complete within {self.plan.max_turns} turns",
                actual=f"At turn {turn_number + 1}",
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_message(
        self,
        sender: str,
        recipient: str,
        content: str | None = None,
    ) -> DetectedDrift | None:
        """Record a message and check for anomalies."""
        content_length = len(content) if content else 0
        self.execution.add_message(sender, recipient, content_length)

        # Check for empty response
        if content_length == 0:
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_RESPONSE,
                severity=DriftSeverity.WARNING,
                description=f"Agent '{sender}' sent empty message",
                agent_name=sender,
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
        if self.plan.expected_tools and tool_name not in self.plan.expected_tools:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_TOOL,
                severity=DriftSeverity.INFO,
                description=f"Unexpected tool '{tool_name}' called by '{agent_name}'",
                expected=f"One of: {list(self.plan.expected_tools)}",
                actual=tool_name,
                agent_name=agent_name,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_code_execution(
        self,
        language: str,
        exit_code: int,
        agent_name: str | None = None,
    ) -> DetectedDrift | None:
        """Record code execution and check for drift."""
        self.execution.add_code_execution(language, exit_code, agent_name)

        # Check for unexpected code execution
        if not self.plan.expected_code_execution and len(self.execution.code_executions) == 1:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_CODE,
                severity=DriftSeverity.INFO,
                description=f"Unexpected code execution ({language}) by agent",
                expected="No code execution",
                actual=f"Code execution with exit code {exit_code}",
                agent_name=agent_name,
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
        termination_reason: str | None = None,
        total_duration_ms: float = 0,
    ) -> List[DetectedDrift]:
        """
        Finalize conversation tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.success = success
        self.execution.termination_reason = termination_reason
        self.execution.total_duration_ms = total_duration_ms

        # Check for missing agents
        if self.plan.expected_agents:
            missing = self.plan.expected_agents - self.execution.agents_active
            for agent in missing:
                drift = DetectedDrift(
                    drift_type=DriftType.MISSING_AGENT,
                    severity=DriftSeverity.WARNING,
                    description=f"Expected agent '{agent}' did not participate",
                    expected="Agent active in conversation",
                    actual="Agent never spoke",
                    agent_name=agent,
                )
                self.detected_drifts.append(drift)

        # Check for missing tool calls
        if self.plan.expected_tools:
            missing = self.plan.expected_tools - self.execution.tools_called
            for tool in missing:
                drift = DetectedDrift(
                    drift_type=DriftType.MISSING_TOOL_CALL,
                    severity=DriftSeverity.INFO,
                    description=f"Expected tool '{tool}' was not called",
                    expected="Tool called during conversation",
                    actual="Tool never invoked",
                )
                self.detected_drifts.append(drift)

        # Check for high tool failure rate
        total_tool_calls = len(self.execution.tool_calls)
        if total_tool_calls > 0:
            failure_rate = self.execution.tool_failures / total_tool_calls
            if failure_rate > 0.3:  # More than 30% failures
                drift = DetectedDrift(
                    drift_type=DriftType.TOOL_FAILURE_RATE,
                    severity=DriftSeverity.WARNING,
                    description=f"High tool failure rate: {failure_rate:.1%}",
                    expected="< 30% failure rate",
                    actual=f"{failure_rate:.1%} ({self.execution.tool_failures}/{total_tool_calls})",
                )
                self.detected_drifts.append(drift)

        # Check for high code failure rate
        total_code_exec = len(self.execution.code_executions)
        if total_code_exec > 0:
            failure_rate = self.execution.code_failures / total_code_exec
            if failure_rate > 0.3:
                drift = DetectedDrift(
                    drift_type=DriftType.CODE_FAILURE_RATE,
                    severity=DriftSeverity.WARNING,
                    description=f"High code execution failure rate: {failure_rate:.1%}",
                    expected="< 30% failure rate",
                    actual=f"{failure_rate:.1%} ({self.execution.code_failures}/{total_code_exec})",
                )
                self.detected_drifts.append(drift)

        # Check for unexpected termination
        if not success and error:
            drift = DetectedDrift(
                drift_type=DriftType.UNEXPECTED_TERMINATION,
                severity=DriftSeverity.ALERT,
                description=f"Conversation ended unexpectedly: {error[:100]}",
                expected="Successful completion",
                actual=f"Failed: {termination_reason or 'unknown'}",
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
            return "No drifts detected - conversation matched expectations"

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
