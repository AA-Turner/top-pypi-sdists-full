"""
Rollout orchestration for agent training.

This module provides multi-turn rollout execution matching NeMo RL's pattern,
integrated with DN SDK agents.

Key components:
- RolloutOrchestrator: Manages multi-turn agent-environment interaction
- RolloutConfig: Configuration for rollout execution
- RolloutResult: Result from completed rollout with metrics

Usage:
    from dreadnode.training.rollouts import RolloutOrchestrator, RolloutConfig

    orchestrator = RolloutOrchestrator(config)

    # Single rollout
    result = await orchestrator.run_single(agent, goal, environment)

    # Batch rollouts
    results = await orchestrator.run_batch(agents, goals, environment)
"""

from dreadnode.training.rollouts.adapters import (
    DNAgentAdapter,
    VllmAdapter,
)
from dreadnode.training.rollouts.orchestrator import (
    EnvironmentInterface,
    EnvironmentReturn,
    GenerationInterface,
    RolloutOrchestrator,
)
from dreadnode.training.rollouts.types import (
    Message,
    MessageLog,
    MessageRole,
    RolloutConfig,
    RolloutMetrics,
    RolloutResult,
    TurnResult,
)
from dreadnode.training.rollouts.worlds import (
    BaseWorldsRewardShaper,
    CompositeWorldsRewardShaper,
    CredentialDiscoveryRewardShaper,
    HeuristicWorldsRewardShaper,
    HostDiscoveryRewardShaper,
    PrivilegeEscalationRewardShaper,
    ReasoningTraceRewardShaper,
    RegexToolRewardShaper,
    TerminalStateRewardShaper,
    ToolErrorPenaltyShaper,
    ToolObservationRewardShaper,
    ToolStopRewardShaper,
    WorldsEpisodeRecorder,
    WorldsRewardShaper,
    WorldsRewardSignal,
    WorldsRewardWeights,
    WorldsTurnTrace,
    build_worlds_reward_shaper_from_config,
    build_worlds_rollout_hooks,
    run_worlds_agent_rollout,
)

__all__ = [
    "BaseWorldsRewardShaper",
    "CompositeWorldsRewardShaper",
    "CredentialDiscoveryRewardShaper",
    "DNAgentAdapter",
    "EnvironmentInterface",
    "EnvironmentReturn",
    "GenerationInterface",
    "HeuristicWorldsRewardShaper",
    "HostDiscoveryRewardShaper",
    "Message",
    "MessageLog",
    "MessageRole",
    "PrivilegeEscalationRewardShaper",
    "ReasoningTraceRewardShaper",
    "RegexToolRewardShaper",
    "RolloutConfig",
    "RolloutMetrics",
    "RolloutOrchestrator",
    "RolloutResult",
    "TerminalStateRewardShaper",
    "ToolErrorPenaltyShaper",
    "ToolObservationRewardShaper",
    "ToolStopRewardShaper",
    "TurnResult",
    "VllmAdapter",
    "WorldsEpisodeRecorder",
    "WorldsRewardShaper",
    "WorldsRewardSignal",
    "WorldsRewardWeights",
    "WorldsTurnTrace",
    "build_worlds_reward_shaper_from_config",
    "build_worlds_rollout_hooks",
    "run_worlds_agent_rollout",
]
