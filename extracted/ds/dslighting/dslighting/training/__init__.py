"""
DSLighting Training - Agent-Lightning integration.

Provides integration with Microsoft Agent-Lightning for training data science agents.
"""
try:
    # ========== Agents ==========
    from dslighting.training.agents.lit_ds_agent import LitDSAgent

    # ========== Rewards ==========
    from dslighting.training.rewards.base import RewardEvaluator
    from dslighting.training.rewards.presets import (
        KaggleReward,
        ClassificationReward,
        RegressionReward,
    )

    # ========== Datasets ==========
    from dslighting.training.datasets.converters import DatasetConverter

    # ========== Config ==========
    from dslighting.training.config.verl_config import VerlConfigBuilder

except ImportError:
    # Agent-Lightning or other dependencies are unavailable.
    LitDSAgent = None
    RewardEvaluator = None
    KaggleReward = None
    ClassificationReward = None
    RegressionReward = None
    DatasetConverter = None
    VerlConfigBuilder = None

__all__ = [
    # Agents
    "LitDSAgent",
    # Rewards
    "RewardEvaluator",
    "KaggleReward",
    "ClassificationReward",
    "RegressionReward",
    # Datasets
    "DatasetConverter",
    # Config
    "VerlConfigBuilder",
]
