"""Generic agent rollout recorder + runner — domain-neutral.

Captures per-turn assistant + tool data from an ``Agent.run()`` stream into
a :class:`RolloutResult` suitable for RL datum building. No reward shaping,
no Worlds-specific metric namespaces — apply those on top separately.

Used by:
- env-backed RL rollouts (``training.jobs._generate_env_agent_rollout_group``)
- future rollout paths that need per-turn capture without a reward shaper

The Worlds-specific recorder + hooks in ``rollouts.worlds`` predate this
module and still carry Worlds reward metrics + signal handling; they stay
there, untouched, so existing Worlds RL keeps working.
"""

import typing as t
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime

from dreadnode.agents.events import (
    AgentEnd,
    AgentEvent,  # noqa: F401 — re-export parity with worlds.py
    GenerationStep,
    ToolError,
    ToolStep,
)
from dreadnode.agents.trajectory import Trajectory, trajectory_to_openai_format
from dreadnode.core.hook import Hook, hook
from dreadnode.training.rollouts.types import (
    Message,
    RolloutMetrics,
    RolloutResult,
    TurnResult,
)

if t.TYPE_CHECKING:
    from dreadnode.agents import Agent


# ---------------------------------------------------------------------------
# Turn trace (mirrors WorldsTurnTrace's generic fields; no reward_signals)
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class TurnTrace:
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
    stop_reason: str | None = None


# ---------------------------------------------------------------------------
# Internal helpers — copied deliberately rather than importing from worlds.py
# to keep the module dependency graph one-way (worlds CAN depend on us; we
# MUST NOT depend on worlds).
# ---------------------------------------------------------------------------


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


def _message_from_openai_dict(data: dict[str, t.Any]) -> Message:
    """Shape an OpenAI-format message dict as a rollout ``Message``."""
    return t.cast("Message", data)


# ---------------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class AgentRolloutRecorder:
    """Mutable recorder that accumulates per-turn state during a rollout.

    Hook callbacks mutate this recorder during ``agent.run()``. At the end
    :meth:`to_rollout_result` serializes the accumulated state into a
    :class:`RolloutResult`.

    This is the Worlds-free twin of ``rollouts.worlds.WorldsEpisodeRecorder``.
    No ``apply_turn_signals`` / ``apply_terminal_signals`` — shaped rewards
    are the domain module's concern. Callers that want a terminal reward
    can append directly to :attr:`terminal_signals` after the rollout ends.
    """

    goal: str
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    turns: dict[int, TurnTrace] = field(default_factory=dict)
    stop_reason: str | None = None
    tool_errors: list[dict[str, t.Any]] = field(default_factory=list)
    terminal_signals: list[dict[str, t.Any]] = field(default_factory=list)

    def ensure_turn(self, step: int) -> TurnTrace:
        turn = self.turns.get(step)
        if turn is None:
            turn = TurnTrace(step=step)
            self.turns[step] = turn
        return turn

    def record_generation(self, event: GenerationStep) -> TurnTrace:
        turn = self.ensure_turn(event.step)
        if event.messages:
            last_message = event.messages[-1]
            content = last_message.content
            turn.generated_text = (
                content if isinstance(content, str) else str(content or "")
            )
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

    def record_tool_step(self, event: ToolStep) -> TurnTrace:
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

    def record_finish(self, event: AgentEnd) -> None:
        self.stop_reason = event.stop_reason

    def to_rollout_result(
        self,
        *,
        trajectory: Trajectory,
        metadata: dict[str, t.Any] | None = None,
    ) -> RolloutResult:
        turns = [self.turns[step] for step in sorted(self.turns)]
        message_log = [
            _message_from_openai_dict(msg)
            for msg in trajectory_to_openai_format(trajectory)
        ]

        completed_at = datetime.now(UTC)
        total_tool_calls = sum(len(turn.tool_calls) for turn in turns)
        tool_error_count = len(self.tool_errors)
        total_reward = sum(
            float(signal.get("value", 0.0)) for signal in self.terminal_signals
        ) + sum(turn.reward for turn in turns)

        metrics = RolloutMetrics(
            total_turns=len(turns),
            completed_turns=len(turns),
            total_input_tokens=trajectory.usage.input_tokens,
            total_generated_tokens=trajectory.usage.output_tokens,
            total_reward=total_reward,
            mean_reward_per_turn=(total_reward / len(turns)) if turns else 0.0,
            final_reward=total_reward,
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
                terminated=(
                    (self.stop_reason is not None and turn.step == turns[-1].step)
                    if turns
                    else False
                ),
                truncated=(
                    self.stop_reason == "max_steps_reached"
                    and turn.step == turns[-1].step
                    if turns
                    else False
                ),
                tool_calls=list(turn.tool_calls),
                tool_results=list(turn.tool_results),
            )
            for turn in turns
        ]

        result_metadata: dict[str, t.Any] = {
            "stop_reason": self.stop_reason,
            "turns": [asdict(turn) for turn in turns],
            "tool_errors": list(self.tool_errors),
            "terminal_signals": list(self.terminal_signals),
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
            final_reward=total_reward,
            metadata=result_metadata,
        )


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------


def build_agent_rollout_hooks(
    recorder: AgentRolloutRecorder,
) -> list[Hook[t.Any]]:
    """Hook bundle that records events into ``recorder``. No reward shaping.

    Pair with :func:`run_agent_rollout` for full-turn capture, or install on
    an ``Agent`` directly if the caller manages ``agent.run()`` themselves.
    """

    @hook(GenerationStep)
    async def _on_generation(event: GenerationStep) -> None:
        recorder.record_generation(event)

    @hook(ToolStep)
    async def _on_tool_step(event: ToolStep) -> None:
        recorder.record_tool_step(event)

    @hook(ToolError)
    async def _on_tool_error(event: ToolError) -> None:
        recorder.record_tool_error(event)

    @hook(AgentEnd)
    async def _on_agent_end(event: AgentEnd) -> None:
        recorder.record_finish(event)

    return [_on_generation, _on_tool_step, _on_tool_error, _on_agent_end]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


async def run_agent_rollout(
    agent: "Agent",
    goal: str,
    *,
    metadata: dict[str, t.Any] | None = None,
    reset: bool = True,
) -> RolloutResult:
    """Run ``agent`` against ``goal`` with per-turn capture, return a RolloutResult.

    Domain-neutral: installs only the generic recorder hooks, applies no
    reward shaping, and does not touch the ``worlds/reward`` metric namespace.
    Callers that want shaped rewards add their own hooks on top *before*
    calling this — or skip this and compose directly.

    The agent's pre-existing ``hooks`` list is restored on exit (regardless
    of success/exception) so repeated rollouts on the same agent instance
    don't accumulate recorder hooks.
    """

    recorder = AgentRolloutRecorder(goal=goal)
    rollout_hooks = build_agent_rollout_hooks(recorder)

    original_hooks = list(agent.hooks)
    agent.hooks = [*original_hooks, *rollout_hooks]
    try:
        trajectory = await agent.run(goal, reset=reset)
    finally:
        agent.hooks = original_hooks

    return recorder.to_rollout_result(trajectory=trajectory, metadata=metadata)


__all__ = [
    "AgentRolloutRecorder",
    "TurnTrace",
    "build_agent_rollout_hooks",
    "run_agent_rollout",
]
