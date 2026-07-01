"""
Adapters to use DN SDK Scorers as reward functions.

Bridges the gap between DN SDK's scoring infrastructure and training rewards.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from dreadnode.training.rewards.functions import BaseRewardFunction
from dreadnode.training.rewards.types import RewardComponent
from dreadnode.training.rollouts.types import RolloutResult

# Type for extracting content from rollout for scoring
RolloutAdapter = Callable[[RolloutResult], Any]


def default_rollout_adapter(rollout: RolloutResult) -> str:
    """Default adapter: extract final assistant response."""
    for msg in reversed(rollout.message_log):
        if msg["role"] == "assistant":
            return msg["content"]
    return ""


def full_conversation_adapter(rollout: RolloutResult) -> str:
    """Adapter: concatenate all messages."""
    return "\n".join(f"{msg['role']}: {msg['content']}" for msg in rollout.message_log)


def tool_results_adapter(rollout: RolloutResult) -> list[dict[str, Any]]:
    """Adapter: extract all tool results."""
    results = []
    for turn in rollout.turns:
        results.extend(turn.tool_results)
    return results


@dataclass
class ScorerReward(BaseRewardFunction):
    """
    Wraps a DN SDK Scorer as a RewardFunction.

    This is the primary bridge between DN SDK's rich scorer ecosystem
    and NeMo RL training. It allows any DN SDK scorer to be used
    as a reward signal.

    Example:
        from dreadnode import scorer

        @scorer
        async def quality_check(text: str) -> float:
            # LLM-as-judge or custom logic
            return await evaluate_quality(text)

        # Use in training
        reward = ScorerReward(
            scorer=quality_check,
            weight=0.5,
            adapter=lambda r: r.message_log[-1]["content"],
        )

        # In aggregator
        aggregator = RewardAggregator(rewards=[
            SuccessReward(weight=1.0),
            reward,
        ])
    """

    scorer: Any  # dreadnode.Scorer
    weight: float = 1.0
    adapter: RolloutAdapter = field(default=default_rollout_adapter)

    # Scaling to normalize scorer output to reward range
    source_min: float = 0.0
    source_max: float = 1.0
    target_min: float = 0.0
    target_max: float = 1.0

    # Error handling
    catch_errors: bool = True
    error_value: float = 0.0

    def __post_init__(self) -> None:
        # Get name from scorer
        if hasattr(self.scorer, "name"):
            self.name = f"scorer:{self.scorer.name}"
        else:
            self.name = f"scorer:{self.scorer.__class__.__name__}"

    def compute(self, rollout: RolloutResult) -> RewardComponent:
        """
        Compute reward synchronously.

        Note: This wraps async in a sync call. For proper async,
        use compute_async().
        """
        import asyncio

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in async context, use nest_asyncio or return placeholder
                import warnings

                warnings.warn(
                    f"ScorerReward.compute() called in async context. "
                    f"Use compute_async() instead for scorer {self.name}",
                    stacklevel=2,
                )
                return self._make_component(
                    value=0.0,
                    rationale="Use compute_async() in async context",
                )
            return loop.run_until_complete(self.compute_async(rollout))
        except RuntimeError:
            # No event loop
            return asyncio.run(self.compute_async(rollout))

    async def compute_async(self, rollout: RolloutResult) -> RewardComponent:
        """Compute reward asynchronously using the scorer."""
        try:
            # Extract content to score
            content = self.adapter(rollout)

            # Run scorer
            if hasattr(self.scorer, "score"):
                metric = await self.scorer.score(content)
            elif callable(self.scorer):
                result = self.scorer(content)
                if hasattr(result, "__await__"):
                    metric = await result
                else:
                    metric = result
            else:
                raise TypeError(f"Scorer {self.scorer} is not callable")

            # Extract value from metric
            if hasattr(metric, "value"):
                raw_value = metric.value
                rationale = getattr(metric, "rationale", None)
            else:
                raw_value = float(metric)
                rationale = None

            # Scale to target range
            scaled_value = self._scale_value(raw_value)

            return self._make_component(
                value=scaled_value,
                rationale=rationale,
                raw_value=raw_value,
                scorer_name=self.name,
            )

        except Exception as e:
            if not self.catch_errors:
                raise

            return self._make_component(
                value=self.error_value,
                rationale=f"Scorer error: {e!s}",
                error=str(e),
            )

    def _scale_value(self, value: float) -> float:
        """Scale value from source range to target range."""
        if self.source_max == self.source_min:
            return self.target_min

        # Clamp to source range
        clamped = max(self.source_min, min(self.source_max, value))

        # Normalize to [0, 1]
        normalized = (clamped - self.source_min) / (self.source_max - self.source_min)

        # Scale to target range
        return self.target_min + normalized * (self.target_max - self.target_min)


@dataclass
class MetricReward(BaseRewardFunction):
    """
    Creates a reward from a specific metric in the rollout.

    Useful for extracting rewards from agent-reported metrics
    or environment feedback.

    Example:
        reward = MetricReward(
            metric_path="metrics.total_tool_calls",
            transform=lambda x: -x * 0.01,  # Penalize tool usage
            weight=0.1,
        )
    """

    metric_path: str = ""
    weight: float = 1.0
    transform: Callable[[Any], float] | None = None
    default_value: float = 0.0

    def __post_init__(self) -> None:
        self.name = f"metric:{self.metric_path}"

    def compute(self, rollout: RolloutResult) -> RewardComponent:
        """Extract and transform metric from rollout."""
        value = self._extract_metric(rollout, self.metric_path)

        if value is None:
            return self._make_component(
                value=self.default_value,
                rationale=f"Metric {self.metric_path} not found",
            )

        # Apply transform if provided
        if self.transform:
            value = self.transform(value)

        return self._make_component(
            value=float(value),
            rationale=f"Extracted from {self.metric_path}",
            raw_value=value,
        )

    def _extract_metric(self, rollout: RolloutResult, path: str) -> Any | None:
        """Extract a value from rollout using dot-separated path."""
        parts = path.split(".")
        obj: Any = rollout

        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            elif isinstance(obj, dict) and part in obj:
                obj = obj[part]
            else:
                return None

        return obj


def create_scorer_reward(
    scorer: Any,
    weight: float = 1.0,
    adapter: RolloutAdapter | None = None,
    **kwargs: Any,
) -> ScorerReward:
    """
    Convenience function to create a ScorerReward.

    Args:
        scorer: DN SDK Scorer or callable.
        weight: Reward weight.
        adapter: Function to extract content from rollout.
        **kwargs: Additional ScorerReward parameters.

    Returns:
        Configured ScorerReward.
    """
    return ScorerReward(
        scorer=scorer,
        weight=weight,
        adapter=adapter or default_rollout_adapter,
        **kwargs,
    )
