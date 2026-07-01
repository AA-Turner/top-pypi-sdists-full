"""High-level Prime Intellect training functions.

Provides convenient functions for running training on Prime Intellect's
decentralized GPU infrastructure.

Example:
    from dreadnode.training import train_on_prime

    result = await train_on_prime(
        config={
            "model_name": "meta-llama/Llama-3.1-8B-Instruct",
            "max_steps": 1000,
        },
        gpu_type="H100_80GB",
        gpu_count=8,
    )
"""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from dreadnode.training.prime.trainer import TrainingResult


async def train_on_prime(
    config: dict[str, t.Any] | None = None,
    name: str | None = None,
    gpu_type: str = "H100_80GB",
    gpu_count: int = 1,
    training_type: str = "sft",
    requirements: list[str] | None = None,
    env_vars: dict[str, str] | None = None,
    auto_terminate: bool = True,
    region: str | None = None,
    interruptible: bool = False,
) -> TrainingResult:
    """Run training on Prime Intellect infrastructure.

    This function provides a high-level interface for running training
    jobs on Prime's decentralized GPU compute.

    Args:
        config: Training configuration dict. Common options:
            - model_name: Model name or path
            - max_steps: Maximum training steps
            - batch_size: Batch size per device
            - learning_rate: Learning rate
            - checkpoint_dir: Checkpoint directory
        name: Job name.
        gpu_type: GPU type (H100_80GB, A100_80GB, etc.).
        gpu_count: Number of GPUs.
        training_type: Type of training (sft, grpo, dpo, ppo).
        requirements: Additional Python requirements.
        env_vars: Environment variables.
        auto_terminate: Terminate pods after training.
        region: Preferred region.
        interruptible: Use spot/interruptible instances.

    Returns:
        TrainingResult with final state and checkpoint info.

    Example:
        # SFT training on H100s
        result = await train_on_prime(
            config={
                "model_name": "meta-llama/Llama-3.1-8B-Instruct",
                "max_steps": 1000,
                "batch_size": 32,
            },
            gpu_type="H100_80GB",
            gpu_count=8,
        )

        if result.succeeded:
            print(f"Checkpoint: {result.checkpoint_path}")
    """
    from dreadnode.training.prime import (
        EnvironmentConfig,
        GPUType,
        PodConfig,
        PrimeTrainer,
        PrimeTrainingConfig,
    )

    # Build configuration
    config_dict = config or {}
    config_dict["name"] = name or config_dict.get("name", f"prime-{training_type}")
    config_dict["training_type"] = training_type

    # Build pod config
    try:
        gpu_type_enum = GPUType(gpu_type)
    except ValueError:
        gpu_type_enum = gpu_type

    pod_config = PodConfig(
        gpu_type=gpu_type_enum,
        gpu_count=gpu_count,
        region=region,
        interruptible=interruptible,
    )
    config_dict["pod_config"] = pod_config

    # Build environment config
    env_config = EnvironmentConfig(
        requirements=requirements,
        env_vars=env_vars or {},
    )
    config_dict["environment"] = env_config

    training_config = PrimeTrainingConfig(**config_dict)
    trainer = PrimeTrainer(training_config)

    return await trainer.train(auto_terminate=auto_terminate)


async def run_in_sandbox(
    code: str,
    timeout_seconds: int = 300,
    memory_mb: int = 2048,
) -> dict:
    """Run code in a Prime Intellect sandbox.

    Sandboxes are lightweight execution environments for running
    AI-generated code or quick experiments.

    Args:
        code: Python code to execute.
        timeout_seconds: Execution timeout.
        memory_mb: Memory limit in MB.

    Returns:
        Dict with stdout, stderr, and return_code.

    Example:
        result = await run_in_sandbox('''
            import torch
            print(f"CUDA available: {torch.cuda.is_available()}")
        ''')
        print(result["stdout"])
    """
    from dreadnode.training.prime import PrimeSandbox, SandboxConfig

    config = SandboxConfig(
        timeout_seconds=timeout_seconds,
        memory_mb=memory_mb,
    )

    sandbox = PrimeSandbox(config)
    return await sandbox.run(code)


__all__ = ["run_in_sandbox", "train_on_prime"]
