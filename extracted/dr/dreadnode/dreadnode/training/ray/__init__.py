"""
Native Ray-based GRPO/SFT/DPO/PPO/RM training framework.

This module provides a production-ready Ray-native implementation of GRPO,
SFT, DPO, PPO, and Reward Model training for language models. It uses:

- Ray actors for distributed inference (vLLM)
- Ray Train for distributed training with FSDP2
- Native Ray coordination (no RLlib dependency)
- OpenRLHF-style async architecture for overlapped generation/training

Key components:
- RayGRPOConfig: Configuration for GRPO training
- RayGRPOTrainer: Colocated trainer (single GPU, time-shared)
- AsyncRayGRPOTrainer: Async trainer (existing)
- AsyncGRPOCoordinator: New async coordinator with ExperienceBuffer
- FSDP2Learner: Distributed training with PyTorch FSDP2
- RolloutWorker: vLLM-based experience generation
- train_grpo_distributed: Ray Train integration

Architecture modes:
1. Colocated: Time-share GPU between inference/training (RayGRPOTrainer)
2. Async: Overlapped generation/training (AsyncGRPOCoordinator)
3. Distributed: Multi-node FSDP2 (train_grpo_distributed)

Usage:
    # Mode 1: Colocated (single GPU)
    from dreadnode.training.ray import RayGRPOConfig, RayGRPOTrainer

    config = RayGRPOConfig(model_name="Qwen/Qwen2.5-1.5B-Instruct")
    trainer = RayGRPOTrainer(config)
    trainer.train(prompts, reward_fn)

    # Mode 2: Async (overlapped)
    from dreadnode.training.ray import AsyncGRPOCoordinator

    coordinator = AsyncGRPOCoordinator(
        config=config,
        prompts=prompts,
        reward_fn=reward_fn,
        num_rollout_workers=2,
        buffer_size=2,
    )
    state = await coordinator.train(num_steps=1000)

    # Mode 3: Distributed (multi-node FSDP2)
    from dreadnode.training.ray import train_grpo_distributed

    result = train_grpo_distributed(
        config=config,
        prompts=prompts,
        reward_fn=reward_fn,
        num_workers=8,
    )
"""

# Configuration
from dreadnode.training.ray.async_trainer import AsyncRayGRPOTrainer

# Callbacks
from dreadnode.training.ray.callbacks import (
    CallbackHandler,
    CheckpointCallback,
    EarlyStoppingCallback,
    GradientClippingCallback,
    JSONLoggingCallback,
    MetricHistoryCallback,
    PrintCallback,
    ProgressCallback,
    SampleLoggingCallback,
    TensorBoardCallback,
    ToolCallInfo,
    ToolLoggingCallback,
    TrainerCallback,
    TrainerControl,
    WandbCallback,
)
from dreadnode.training.ray.config import (
    GRPOLossConfig,
    RayGRPOConfig,
    TrainingConfig,
    VLLMConfig,
)

# Coordinators
from dreadnode.training.ray.coordinator import (
    AsyncGRPOConfig,
    AsyncGRPOCoordinator,
    SyncGRPOCoordinator,
    TrainingState,
)

# Distributed training
from dreadnode.training.ray.distributed import (
    DistributedConfig,
    train_grpo_distributed,
    train_sft_distributed,
    tune_grpo,
)

# DPO
from dreadnode.training.ray.dpo import (
    DPOConfig,
    DPOTrainer,
    PreferencePair,
)

# Experience management
from dreadnode.training.ray.experience import (
    Experience,
    ExperienceBatch,
    ExperienceBuffer,
)

# FSDP2 learner
from dreadnode.training.ray.fsdp2_learner import (
    FSDP2Config,
    FSDP2Learner,
    cleanup_distributed,
    init_distributed,
)

# Inference
from dreadnode.training.ray.inference import (
    GenerationOutput,
    VLLMInferenceActor,
    VLLMInferencePool,
)

# Learner utilities
from dreadnode.training.ray.learner import (
    GRPOLearner,
    TrainingBatch,
    compute_log_probs,
    grpo_loss,
)

# Multi-turn rollouts
from dreadnode.training.ray.multi_turn import (
    ConversationResult,
    ConversationTurn,
    MultiTurnConfig,
    MultiTurnRolloutWorker,
    ToolExecutor,
)

# PPO
from dreadnode.training.ray.ppo import (
    PPOConfig,
    PPOTrainer,
    ValueHead,
)

# Reward Model
from dreadnode.training.ray.reward_model import (
    RewardModel,
    RewardModelHead,
    RewardModelTrainer,
    RMConfig,
)

# Rollout environment protocol
from dreadnode.training.ray.rollout_env import (
    MultiTurnRolloutEnvironment,
    RolloutEnvironment,
    StreamingRolloutEnvironment,
)

# Rollout workers
from dreadnode.training.ray.rollout_worker import (
    RolloutConfig,
    RolloutWorker,
    RolloutWorkerPool,
    create_rollout_worker,
)

# SFT
from dreadnode.training.ray.sft import (
    PackedDataset,
    PackedSample,
    SequencePacker,
    SFTConfig,
    SFTTrainer,
)

# Existing trainers
from dreadnode.training.ray.trainer import RayGRPOTrainer

__all__ = [
    "AsyncGRPOConfig",
    # Coordinators
    "AsyncGRPOCoordinator",
    "AsyncRayGRPOTrainer",
    # Callbacks
    "CallbackHandler",
    "CheckpointCallback",
    # Multi-turn
    "ConversationResult",
    "ConversationTurn",
    # DPO
    "DPOConfig",
    "DPOTrainer",
    "DistributedConfig",
    "EarlyStoppingCallback",
    # Experience
    "Experience",
    "ExperienceBatch",
    "ExperienceBuffer",
    "FSDP2Config",
    "FSDP2Learner",
    # Learners
    "GRPOLearner",
    # Configuration
    "GRPOLossConfig",
    # Inference
    "GenerationOutput",
    "GradientClippingCallback",
    "JSONLoggingCallback",
    "MetricHistoryCallback",
    "MultiTurnConfig",
    "MultiTurnRolloutEnvironment",
    "MultiTurnRolloutWorker",
    # PPO
    "PPOConfig",
    "PPOTrainer",
    # SFT
    "PackedDataset",
    "PackedSample",
    "PreferencePair",
    "PrintCallback",
    "ProgressCallback",
    # Reward Model
    "RMConfig",
    "RayGRPOConfig",
    # Trainers
    "RayGRPOTrainer",
    "RewardModel",
    "RewardModelHead",
    "RewardModelTrainer",
    "RolloutConfig",
    # Protocols
    "RolloutEnvironment",
    # Workers
    "RolloutWorker",
    "RolloutWorkerPool",
    "SFTConfig",
    "SFTTrainer",
    "SampleLoggingCallback",
    "SequencePacker",
    "StreamingRolloutEnvironment",
    "SyncGRPOCoordinator",
    "TensorBoardCallback",
    "ToolCallInfo",
    "ToolExecutor",
    "ToolLoggingCallback",
    "TrainerCallback",
    "TrainerControl",
    "TrainingBatch",
    "TrainingConfig",
    "TrainingState",
    "VLLMConfig",
    "VLLMInferenceActor",
    "VLLMInferencePool",
    "ValueHead",
    "WandbCallback",
    "cleanup_distributed",
    "compute_log_probs",
    "create_rollout_worker",
    "grpo_loss",
    "init_distributed",
    # Distributed
    "train_grpo_distributed",
    "train_sft_distributed",
    "tune_grpo",
]
