"""Worlds-specific agent rollout helpers for RL data collection.

This module builds on the SDK Agent event stream rather than the algorithmic
Worlds walker trajectory model. The intent is to:

- capture assistant reasoning/tool use as native Agent events
- attach shaped reward metrics through hooks
- return a RolloutResult that can feed downstream RL loops
"""

from __future__ import annotations

import re
import typing as t
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime

from dreadnode.agents.events import AgentEnd, AgentEvent, GenerationStep, ToolError, ToolStep
from dreadnode.agents.trajectory import Trajectory, trajectory_to_openai_format
from dreadnode.core.hook import Hook, hook
from dreadnode.core.metric import MetricSeries
from dreadnode.training.rollouts.types import (
    Message,
    RolloutMetrics,
    RolloutResult,
    TurnResult,
)

if t.TYPE_CHECKING:
    from dreadnode.agents import Agent


_HOST_DISCOVERY_PATTERN = re.compile(
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|dc\d*\.|ldap|kerberos|domain controller)\b",
    re.IGNORECASE,
)
_CREDENTIAL_DISCOVERY_PATTERN = re.compile(
    r"\b(?:password|hash|ticket|ccache|credential|ntlm|krbtgt|asreproast|kerberoast)\b",
    re.IGNORECASE,
)
_PRIV_ESC_PATTERN = re.compile(
    r"\b(?:domain admins?|admin to|write dacl|owns|forcechangepassword|addmember)\b",
    re.IGNORECASE,
)


@dataclass(slots=True)
class WorldsRewardWeights:
    """Default heuristic weights for Worlds RL reward shaping."""

    reasoning_trace_bonus: float = 0.01
    tool_observation_reward: float = 0.02
    host_discovery_reward: float = 0.10
    credential_discovery_reward: float = 0.20
    privilege_escalation_reward: float = 0.35
    stop_tool_bonus: float = 0.15
    terminal_success_reward: float = 1.00
    terminal_stall_penalty: float = -0.25
    terminal_max_steps_penalty: float = -0.35
    terminal_error_penalty: float = -1.00
    tool_error_penalty: float = -0.20


@dataclass(slots=True)
class WorldsRewardSignal:
    """A single shaped reward emitted during a rollout."""

    source: str
    value: float
    reason: str
    metadata: dict[str, t.Any] = field(default_factory=dict)


@dataclass(slots=True)
class WorldsTurnTrace:
    """Captured assistant/tool state for a single agent step."""

    step: int
    generated_text: str = ""
    raw_generated_text: str | None = None
    reasoning_content: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: list[dict[str, t.Any]] = field(default_factory=list)
    tool_results: list[dict[str, t.Any]] = field(default_factory=list)
    reward: float = 0.0
    reward_signals: list[WorldsRewardSignal] = field(default_factory=list)
    stop_reason: str | None = None


class WorldsRewardShaper(t.Protocol):
    """Protocol for Worlds rollout reward shaping."""

    def generation_signals(
        self,
        event: GenerationStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        """Return reward signals for a generation step."""

    def tool_signals(
        self,
        event: ToolStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        """Return reward signals for a tool result step."""

    def tool_error_signals(
        self,
        event: ToolError,
    ) -> t.Sequence[WorldsRewardSignal]:
        """Return reward signals for a tool execution failure."""

    def terminal_signals(
        self,
        event: AgentEnd,
    ) -> t.Sequence[WorldsRewardSignal]:
        """Return reward signals for terminal agent state."""


class BaseWorldsRewardShaper:
    """Convenience base class for concrete Worlds reward shapers."""

    def generation_signals(
        self,
        event: GenerationStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        del event, turn
        return []

    def tool_signals(
        self,
        event: ToolStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        del event, turn
        return []

    def tool_error_signals(
        self,
        event: ToolError,
    ) -> t.Sequence[WorldsRewardSignal]:
        del event
        return []

    def terminal_signals(
        self,
        event: AgentEnd,
    ) -> t.Sequence[WorldsRewardSignal]:
        del event
        return []


class ReasoningTraceRewardShaper(BaseWorldsRewardShaper):
    """Reward assistant reasoning traces when they are present."""

    def __init__(self, *, value: float = 0.01) -> None:
        self.value = value

    def generation_signals(
        self,
        event: GenerationStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        del event
        reasoning = turn.reasoning_content
        if not reasoning or not reasoning.strip():
            return []
        return [
            WorldsRewardSignal(
                source="generation.reasoning",
                value=self.value,
                reason="Assistant emitted a reasoning trace.",
            )
        ]


class ToolObservationRewardShaper(BaseWorldsRewardShaper):
    """Reward tool calls that produce non-empty observations."""

    def __init__(self, *, value: float = 0.02) -> None:
        self.value = value

    def tool_signals(
        self,
        event: ToolStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        del turn
        result_text = _tool_result_text(event)
        if not result_text.strip():
            return []
        return [
            WorldsRewardSignal(
                source="tool.observation",
                value=self.value,
                reason="Tool produced an observation.",
                metadata={"tool_name": event.tool_call.name},
            )
        ]


class RegexToolRewardShaper(BaseWorldsRewardShaper):
    """Reward tool outputs whose text matches a regular expression."""

    def __init__(
        self,
        *,
        pattern: re.Pattern[str],
        value: float,
        source: str,
        reason: str,
    ) -> None:
        self.pattern = pattern
        self.value = value
        self.source = source
        self.reason = reason

    def tool_signals(
        self,
        event: ToolStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        del turn
        result_text = _tool_result_text(event)
        if not self.pattern.search(result_text):
            return []
        return [
            WorldsRewardSignal(
                source=self.source,
                value=self.value,
                reason=self.reason,
                metadata={"tool_name": event.tool_call.name},
            )
        ]


class HostDiscoveryRewardShaper(RegexToolRewardShaper):
    """Reward host or service discovery evidence in tool output."""

    def __init__(self, *, value: float = 0.10) -> None:
        super().__init__(
            pattern=_HOST_DISCOVERY_PATTERN,
            value=value,
            source="tool.discovery.host",
            reason="Tool output contains host or service discovery evidence.",
        )


class CredentialDiscoveryRewardShaper(RegexToolRewardShaper):
    """Reward credential-discovery evidence in tool output."""

    def __init__(self, *, value: float = 0.20) -> None:
        super().__init__(
            pattern=_CREDENTIAL_DISCOVERY_PATTERN,
            value=value,
            source="tool.discovery.credential",
            reason="Tool output contains credential discovery evidence.",
        )


class PrivilegeEscalationRewardShaper(RegexToolRewardShaper):
    """Reward privilege-escalation evidence in tool output."""

    def __init__(self, *, value: float = 0.35) -> None:
        super().__init__(
            pattern=_PRIV_ESC_PATTERN,
            value=value,
            source="tool.discovery.privesc",
            reason="Tool output suggests a privilege-escalation opportunity.",
        )


class ToolStopRewardShaper(BaseWorldsRewardShaper):
    """Reward tools that explicitly request agent termination."""

    def __init__(self, *, value: float = 0.15) -> None:
        self.value = value

    def tool_signals(
        self,
        event: ToolStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        del turn
        if not event.stop:
            return []
        return [
            WorldsRewardSignal(
                source="tool.stop",
                value=self.value,
                reason="Tool explicitly requested agent termination.",
                metadata={"tool_name": event.tool_call.name},
            )
        ]


class ToolErrorPenaltyShaper(BaseWorldsRewardShaper):
    """Penalize tool execution errors."""

    def __init__(self, *, value: float = -0.20) -> None:
        self.value = value

    def tool_error_signals(
        self,
        event: ToolError,
    ) -> t.Sequence[WorldsRewardSignal]:
        return [
            WorldsRewardSignal(
                source="tool.error",
                value=self.value,
                reason="Tool execution raised an error.",
                metadata={
                    "tool_name": event.tool_call.name,
                    "error_type": type(event.error).__name__,
                },
            )
        ]


class TerminalStateRewardShaper(BaseWorldsRewardShaper):
    """Reward or penalize rollout terminal states."""

    def __init__(
        self,
        *,
        success_reward: float = 1.00,
        stall_penalty: float = -0.25,
        max_steps_penalty: float = -0.35,
        error_penalty: float = -1.00,
    ) -> None:
        self.success_reward = success_reward
        self.stall_penalty = stall_penalty
        self.max_steps_penalty = max_steps_penalty
        self.error_penalty = error_penalty

    def terminal_signals(
        self,
        event: AgentEnd,
    ) -> t.Sequence[WorldsRewardSignal]:
        if event.stop_reason == "finished":
            return [
                WorldsRewardSignal(
                    source="terminal.success",
                    value=self.success_reward,
                    reason="Agent finished successfully.",
                )
            ]
        if event.stop_reason == "stalled":
            return [
                WorldsRewardSignal(
                    source="terminal.stalled",
                    value=self.stall_penalty,
                    reason="Agent stalled before completing the task.",
                )
            ]
        if event.stop_reason == "max_steps_reached":
            return [
                WorldsRewardSignal(
                    source="terminal.max_steps",
                    value=self.max_steps_penalty,
                    reason="Agent hit the maximum step budget.",
                )
            ]
        if event.stop_reason == "error":
            return [
                WorldsRewardSignal(
                    source="terminal.error",
                    value=self.error_penalty,
                    reason="Agent terminated with an error.",
                )
            ]
        return []


class CompositeWorldsRewardShaper(BaseWorldsRewardShaper):
    """Compose multiple Worlds reward shapers into one reward policy."""

    def __init__(self, *shapers: WorldsRewardShaper) -> None:
        self.shapers = list(shapers)

    @classmethod
    def from_weights(
        cls,
        weights: WorldsRewardWeights | None = None,
    ) -> CompositeWorldsRewardShaper:
        resolved = weights or WorldsRewardWeights()
        return cls(
            ReasoningTraceRewardShaper(value=resolved.reasoning_trace_bonus),
            ToolObservationRewardShaper(value=resolved.tool_observation_reward),
            HostDiscoveryRewardShaper(value=resolved.host_discovery_reward),
            CredentialDiscoveryRewardShaper(
                value=resolved.credential_discovery_reward
            ),
            PrivilegeEscalationRewardShaper(
                value=resolved.privilege_escalation_reward
            ),
            ToolStopRewardShaper(value=resolved.stop_tool_bonus),
            ToolErrorPenaltyShaper(value=resolved.tool_error_penalty),
            TerminalStateRewardShaper(
                success_reward=resolved.terminal_success_reward,
                stall_penalty=resolved.terminal_stall_penalty,
                max_steps_penalty=resolved.terminal_max_steps_penalty,
                error_penalty=resolved.terminal_error_penalty,
            ),
        )

    def generation_signals(
        self,
        event: GenerationStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        return [
            signal
            for shaper in self.shapers
            for signal in shaper.generation_signals(event, turn=turn)
        ]

    def tool_signals(
        self,
        event: ToolStep,
        *,
        turn: WorldsTurnTrace,
    ) -> t.Sequence[WorldsRewardSignal]:
        return [
            signal
            for shaper in self.shapers
            for signal in shaper.tool_signals(event, turn=turn)
        ]

    def tool_error_signals(
        self,
        event: ToolError,
    ) -> t.Sequence[WorldsRewardSignal]:
        return [
            signal
            for shaper in self.shapers
            for signal in shaper.tool_error_signals(event)
        ]

    def terminal_signals(
        self,
        event: AgentEnd,
    ) -> t.Sequence[WorldsRewardSignal]:
        return [
            signal
            for shaper in self.shapers
            for signal in shaper.terminal_signals(event)
        ]


class HeuristicWorldsRewardShaper(CompositeWorldsRewardShaper):
    """Default heuristic reward shaping for Worlds agent rollouts."""

    def __init__(self, weights: WorldsRewardWeights | None = None) -> None:
        self.weights = weights or WorldsRewardWeights()
        composite = CompositeWorldsRewardShaper.from_weights(self.weights)
        super().__init__(*composite.shapers)


@dataclass(slots=True)
class WorldsEpisodeRecorder:
    """Mutable recorder used by hook callbacks during a single rollout."""

    goal: str
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    turns: dict[int, WorldsTurnTrace] = field(default_factory=dict)
    total_reward: float = 0.0
    stop_reason: str | None = None
    tool_errors: list[dict[str, t.Any]] = field(default_factory=list)
    terminal_signals: list[WorldsRewardSignal] = field(default_factory=list)

    def ensure_turn(self, step: int) -> WorldsTurnTrace:
        turn = self.turns.get(step)
        if turn is None:
            turn = WorldsTurnTrace(step=step)
            self.turns[step] = turn
        return turn

    def record_generation(self, event: GenerationStep) -> WorldsTurnTrace:
        turn = self.ensure_turn(event.step)
        if event.messages:
            last_message = event.messages[-1]
            content = last_message.content
            turn.generated_text = content if isinstance(content, str) else str(content or "")
            turn.tool_calls = [
                {
                    "id": tool_call.id,
                    "name": tool_call.name,
                    "arguments": tool_call.arguments,
                }
                for tool_call in (last_message.tool_calls or [])
            ]
        turn.input_tokens = event.usage.input_tokens
        turn.output_tokens = event.usage.output_tokens
        turn.stop_reason = event.stop_reason
        turn.reasoning_content = _extract_reasoning_content(event)
        turn.raw_generated_text = _extract_raw_generated_text(event)
        return turn

    def record_tool_step(self, event: ToolStep) -> WorldsTurnTrace:
        turn = self.ensure_turn(event.step)
        result_text = ""
        if event.messages:
            content = event.messages[-1].content
            result_text = content if isinstance(content, str) else str(content or "")
        turn.tool_results.append(
            {
                "tool_call_id": event.tool_call.id,
                "tool_name": event.tool_call.name,
                "content": result_text,
                "stop": event.stop,
            }
        )
        return turn

    def record_tool_error(self, event: ToolError) -> None:
        self.tool_errors.append(
            {
                "tool_call_id": event.tool_call.id,
                "tool_name": event.tool_call.name,
                "error": str(event.error),
                "error_type": type(event.error).__name__,
            }
        )

    def latest_step(self) -> int:
        return max(self.turns) if self.turns else 0

    def apply_turn_signals(
        self,
        *,
        event: AgentEvent,
        step: int,
        signals: t.Sequence[WorldsRewardSignal],
    ) -> None:
        if not signals:
            return

        turn = self.ensure_turn(step)
        reward_series = event.metrics.setdefault("worlds/reward", MetricSeries())

        for signal in signals:
            turn.reward_signals.append(signal)
            turn.reward += signal.value
            self.total_reward += signal.value
            reward_series.append(signal.value, step=step)
            metric_name = f"worlds/reward/{_metric_key(signal.source)}"
            event.metrics.setdefault(metric_name, MetricSeries()).append(signal.value, step=step)

    def apply_terminal_signals(
        self,
        *,
        event: AgentEnd,
        signals: t.Sequence[WorldsRewardSignal],
    ) -> None:
        self.stop_reason = event.stop_reason
        if not signals:
            return
        reward_series = event.metrics.setdefault("worlds/reward", MetricSeries())
        for signal in signals:
            self.terminal_signals.append(signal)
            self.total_reward += signal.value
            reward_series.append(signal.value, step=len(self.turns))
            metric_name = f"worlds/reward/{_metric_key(signal.source)}"
            event.metrics.setdefault(metric_name, MetricSeries()).append(
                signal.value,
                step=len(self.turns),
            )

    def to_rollout_result(
        self,
        *,
        trajectory: Trajectory,
        metadata: dict[str, t.Any] | None = None,
    ) -> RolloutResult:
        turns = [self.turns[step] for step in sorted(self.turns)]
        message_log = [
            _message_from_openai_dict(msg) for msg in trajectory_to_openai_format(trajectory)
        ]

        completed_at = datetime.now(UTC)
        total_tool_calls = sum(len(turn.tool_calls) for turn in turns)
        tool_error_count = len(self.tool_errors)
        metrics = RolloutMetrics(
            total_turns=len(turns),
            completed_turns=len(turns),
            total_input_tokens=trajectory.usage.input_tokens,
            total_generated_tokens=trajectory.usage.output_tokens,
            total_reward=self.total_reward,
            mean_reward_per_turn=(self.total_reward / len(turns)) if turns else 0.0,
            final_reward=self.total_reward,
            natural_termination=self.stop_reason == "finished",
            truncated=self.stop_reason == "max_steps_reached",
            errored=self.stop_reason == "error",
            total_time=(completed_at - self.started_at).total_seconds(),
            total_tool_calls=total_tool_calls,
            successful_tool_calls=max(total_tool_calls - tool_error_count, 0),
            failed_tool_calls=tool_error_count,
        )

        rollout_turns = [
            TurnResult(
                turn_number=turn.step,
                generated_text=turn.generated_text,
                generated_tokens=turn.output_tokens,
                input_tokens=turn.input_tokens,
                reward=turn.reward,
                terminated=(self.stop_reason is not None and turn.step == turns[-1].step)
                if turns
                else False,
                truncated=self.stop_reason == "max_steps_reached" and turn.step == turns[-1].step
                if turns
                else False,
                tool_calls=list(turn.tool_calls),
                tool_results=list(turn.tool_results),
            )
            for turn in turns
        ]

        result_metadata: dict[str, t.Any] = {
            "stop_reason": self.stop_reason,
            "turns": [asdict(turn) for turn in turns],
            "tool_errors": list(self.tool_errors),
            "terminal_signals": [asdict(signal) for signal in self.terminal_signals],
        }
        if metadata:
            result_metadata.update(metadata)

        return RolloutResult(
            rollout_id=str(trajectory.session_id),
            agent_id=str(trajectory.agent_id) if trajectory.agent_id else None,
            goal=self.goal,
            message_log=message_log,
            turns=rollout_turns,
            metrics=metrics,
            started_at=self.started_at,
            completed_at=completed_at,
            success=self.stop_reason == "finished",
            final_reward=self.total_reward,
            metadata=result_metadata,
        )


def build_worlds_rollout_hooks(
    recorder: WorldsEpisodeRecorder,
    *,
    reward_shaper: WorldsRewardShaper | None = None,
) -> list[Hook[t.Any]]:
    """Build hook bundle for a Worlds agent rollout."""

    shaper = reward_shaper or HeuristicWorldsRewardShaper()

    @hook(GenerationStep)
    async def worlds_generation_step(event: GenerationStep) -> None:
        turn = recorder.record_generation(event)
        recorder.apply_turn_signals(
            event=event,
            step=event.step,
            signals=shaper.generation_signals(event, turn=turn),
        )

    @hook(ToolStep)
    async def worlds_tool_step(event: ToolStep) -> None:
        turn = recorder.record_tool_step(event)
        recorder.apply_turn_signals(
            event=event,
            step=event.step,
            signals=shaper.tool_signals(event, turn=turn),
        )

    @hook(ToolError)
    async def worlds_tool_error(event: ToolError) -> None:
        recorder.record_tool_error(event)
        recorder.apply_turn_signals(
            event=event,
            step=recorder.latest_step(),
            signals=shaper.tool_error_signals(event),
        )

    @hook(AgentEnd)
    async def worlds_agent_end(event: AgentEnd) -> None:
        recorder.apply_terminal_signals(
            event=event,
            signals=shaper.terminal_signals(event),
        )

    return [
        worlds_generation_step,
        worlds_tool_step,
        worlds_tool_error,
        worlds_agent_end,
    ]


async def run_worlds_agent_rollout(
    agent: Agent,
    goal: str,
    *,
    reward_shaper: WorldsRewardShaper | None = None,
    metadata: dict[str, t.Any] | None = None,
    reset: bool = True,
) -> RolloutResult:
    """Run a single Worlds-style agent rollout and return an RL-friendly result."""

    recorder = WorldsEpisodeRecorder(goal=goal)
    rollout_hooks = build_worlds_rollout_hooks(
        recorder,
        reward_shaper=reward_shaper,
    )
    original_hooks = list(agent.hooks)
    agent.hooks = [*original_hooks, *rollout_hooks]

    try:
        trajectory = await agent.run(goal, reset=reset)
    finally:
        agent.hooks = original_hooks

    return recorder.to_rollout_result(trajectory=trajectory, metadata=metadata)


def _tool_result_text(event: ToolStep) -> str:
    if not event.messages:
        return ""
    content = event.messages[-1].content
    return content if isinstance(content, str) else str(content or "")


def _extract_reasoning_content(event: GenerationStep) -> str | None:
    value = event.extra.get("reasoning_content")
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    return None


def _extract_raw_generated_text(event: GenerationStep) -> str | None:
    value = event.extra.get("raw_generated_text")
    if isinstance(value, str):
        return value
    return None


def build_worlds_reward_shaper_from_config(
    config: dict[str, t.Any] | None,
) -> WorldsRewardShaper:
    """Build a Worlds reward shaper from a simple preset or component config."""

    if not config:
        return HeuristicWorldsRewardShaper()

    components = config.get("components")
    if isinstance(components, list):
        shapers: list[WorldsRewardShaper] = []
        for raw_component in components:
            if not isinstance(raw_component, dict):
                continue
            name = raw_component.get("name")
            params = raw_component.get("params")
            if not isinstance(name, str):
                continue
            params_dict = params if isinstance(params, dict) else {}
            shaper = _build_worlds_reward_component(name=name, params=params_dict)
            if shaper is not None:
                shapers.append(shaper)
        return CompositeWorldsRewardShaper(*shapers) if shapers else HeuristicWorldsRewardShaper()

    policy_name = config.get("name")
    params = config.get("params")
    params_dict = params if isinstance(params, dict) else {}
    if not isinstance(policy_name, str) or policy_name == "heuristic_v1":
        return HeuristicWorldsRewardShaper(_weights_from_config(params_dict))
    if policy_name == "goal_only_v1":
        return TerminalStateRewardShaper(
            success_reward=float(params_dict.get("success_reward", 1.0)),
            stall_penalty=float(params_dict.get("stall_penalty", -0.25)),
            max_steps_penalty=float(params_dict.get("max_steps_penalty", -0.35)),
            error_penalty=float(params_dict.get("error_penalty", -1.0)),
        )
    if policy_name == "discovery_v1":
        return CompositeWorldsRewardShaper(
            HostDiscoveryRewardShaper(
                value=float(params_dict.get("host_discovery_reward", 0.10))
            ),
            CredentialDiscoveryRewardShaper(
                value=float(params_dict.get("credential_discovery_reward", 0.20))
            ),
            PrivilegeEscalationRewardShaper(
                value=float(params_dict.get("privilege_escalation_reward", 0.35))
            ),
            TerminalStateRewardShaper(
                success_reward=float(params_dict.get("success_reward", 1.0)),
                stall_penalty=float(params_dict.get("stall_penalty", -0.25)),
                max_steps_penalty=float(params_dict.get("max_steps_penalty", -0.35)),
                error_penalty=float(params_dict.get("error_penalty", -1.0)),
            ),
        )
    return HeuristicWorldsRewardShaper(_weights_from_config(params_dict))


def _weights_from_config(config: dict[str, t.Any]) -> WorldsRewardWeights:
    return WorldsRewardWeights(
        reasoning_trace_bonus=float(config.get("reasoning_trace_bonus", 0.01)),
        tool_observation_reward=float(config.get("tool_observation_reward", 0.02)),
        host_discovery_reward=float(config.get("host_discovery_reward", 0.10)),
        credential_discovery_reward=float(
            config.get("credential_discovery_reward", 0.20)
        ),
        privilege_escalation_reward=float(
            config.get("privilege_escalation_reward", 0.35)
        ),
        stop_tool_bonus=float(config.get("stop_tool_bonus", 0.15)),
        terminal_success_reward=float(config.get("terminal_success_reward", 1.0)),
        terminal_stall_penalty=float(config.get("terminal_stall_penalty", -0.25)),
        terminal_max_steps_penalty=float(
            config.get("terminal_max_steps_penalty", -0.35)
        ),
        terminal_error_penalty=float(config.get("terminal_error_penalty", -1.0)),
        tool_error_penalty=float(config.get("tool_error_penalty", -0.20)),
    )


def _build_worlds_reward_component(
    *,
    name: str,
    params: dict[str, t.Any],
) -> WorldsRewardShaper | None:
    def _build_terminal_state() -> WorldsRewardShaper:
        return TerminalStateRewardShaper(
            success_reward=float(params.get("success_reward", 1.0)),
            stall_penalty=float(params.get("stall_penalty", -0.25)),
            max_steps_penalty=float(params.get("max_steps_penalty", -0.35)),
            error_penalty=float(params.get("error_penalty", -1.0)),
        )

    builders: dict[str, t.Callable[[], WorldsRewardShaper]] = {
        "reasoning_trace": lambda: ReasoningTraceRewardShaper(
            value=float(params.get("value", 0.01))
        ),
        "tool_observation": lambda: ToolObservationRewardShaper(
            value=float(params.get("value", 0.02))
        ),
        "host_discovery": lambda: HostDiscoveryRewardShaper(
            value=float(params.get("value", 0.10))
        ),
        "credential_discovery": lambda: CredentialDiscoveryRewardShaper(
            value=float(params.get("value", 0.20))
        ),
        "privilege_escalation": lambda: PrivilegeEscalationRewardShaper(
            value=float(params.get("value", 0.35))
        ),
        "tool_stop": lambda: ToolStopRewardShaper(
            value=float(params.get("value", 0.15))
        ),
        "tool_error_penalty": lambda: ToolErrorPenaltyShaper(
            value=float(params.get("value", -0.20))
        ),
        "terminal_state": _build_terminal_state,
    }
    builder = builders.get(name)
    return builder() if builder is not None else None


def _message_from_openai_dict(raw: dict[str, t.Any]) -> Message:
    message = t.cast(
        "Message",
        {
            "role": str(raw["role"]),
            "content": str(raw.get("content", "")),
        },
    )
    tool_calls = raw.get("tool_calls")
    if isinstance(tool_calls, list):
        message["tool_calls"] = tool_calls
    tool_call_id = raw.get("tool_call_id")
    if isinstance(tool_call_id, str):
        message["tool_call_id"] = tool_call_id
    name = raw.get("name")
    if isinstance(name, str):
        message["name"] = name
    return message


def _metric_key(source: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", source).strip("_").lower()


__all__ = [
    "BaseWorldsRewardShaper",
    "CompositeWorldsRewardShaper",
    "CredentialDiscoveryRewardShaper",
    "HeuristicWorldsRewardShaper",
    "HostDiscoveryRewardShaper",
    "PrivilegeEscalationRewardShaper",
    "ReasoningTraceRewardShaper",
    "RegexToolRewardShaper",
    "TerminalStateRewardShaper",
    "ToolErrorPenaltyShaper",
    "ToolObservationRewardShaper",
    "ToolStopRewardShaper",
    "WorldsEpisodeRecorder",
    "WorldsRewardShaper",
    "WorldsRewardSignal",
    "WorldsRewardWeights",
    "WorldsTurnTrace",
    "build_worlds_reward_shaper_from_config",
    "build_worlds_rollout_hooks",
    "run_worlds_agent_rollout",
]
