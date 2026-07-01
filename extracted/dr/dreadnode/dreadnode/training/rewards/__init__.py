"""
Reward functions for agent training.



Key components:
- RewardFunction: Protocol for computing rewards from rollout results
- RewardAggregator: Combines multiple reward sources
- ScorerReward: Wraps DN SDK Scorers for training
- Built-in rewards: SuccessReward, ToolPenalty, LengthPenalty

Usage:
    from dreadnode.training.rewards import (
        RewardAggregator,
        ScorerReward,
        SuccessReward,
        ToolPenalty,
    )

    # Create composite reward
    reward_fn = RewardAggregator(
        rewards=[
            SuccessReward(weight=1.0),
            ToolPenalty(weight=0.1),
            ScorerReward(my_scorer, weight=0.5),
        ]
    )

    # Compute reward from rollout
    result = reward_fn.compute(rollout_result)
"""

from dreadnode.training.rewards.aggregator import (
    AggregationStrategy,
    RewardAggregator,
    create_standard_reward,
)
from dreadnode.training.rewards.functions import (
    BaseRewardFunction,
    FormatReward,
    LengthPenalty,
    RewardFunction,
    SuccessReward,
    ToolPenalty,
    TurnPenalty,
)
from dreadnode.training.rewards.scorer_bridge import (
    MetricReward,
    ScorerHookReward,
    ScorerReward,
    create_scorer_reward,
)
from dreadnode.training.rewards.shaping import (
    RewardShaper,
    apply_dapo_penalty,
    apply_scaling,
    clip_reward,
    shape_rewards_for_grpo,
)
from dreadnode.training.rewards.types import (
    RewardComponent,
    RewardConfig,
    RewardMetrics,
    RewardResult,
)

__all__ = [
    "AggregationStrategy",
    "BaseRewardFunction",
    "FormatReward",
    "LengthPenalty",
    "MetricReward",
    # Aggregation
    "RewardAggregator",
    "RewardComponent",
    # Types
    "RewardConfig",
    # Core Functions
    "RewardFunction",
    "RewardMetrics",
    "RewardResult",
    # Shaping (NeMo RL compatible)
    "RewardShaper",
    "ScorerHookReward",
    # DN SDK Integration
    "ScorerReward",
    "SuccessReward",
    "ToolPenalty",
    "TurnPenalty",
    "apply_dapo_penalty",
    "apply_scaling",
    "clip_reward",
    "create_scorer_reward",
    "create_standard_reward",
    "shape_rewards_for_grpo",
]
