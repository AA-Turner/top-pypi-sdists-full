"""Training module with lazy imports for heavy dependencies.

This module uses lazy loading to avoid importing torch/ray unless needed.
Heavy dependencies (torch, ray, transformers, vllm) are only loaded when
the user actually accesses training-related classes.
"""

import importlib
import typing as t
from pathlib import Path

if t.TYPE_CHECKING:
    # Type-checking imports for IDE support
    from dreadnode.training.anyscale import (
        AnyscaleJobConfig,
        AnyscaleTrainer,
        AnyscaleTrainingConfig,
        submit_anyscale_job,
        train_on_anyscale,
    )
    from dreadnode.training.anyscale import (
        ComputeConfig as AnyscaleComputeConfig,
    )
    from dreadnode.training.azureml import (
        AzureMLClient,
        AzureMLTrainer,
        AzureMLTrainingConfig,
        cancel_azureml_job,
        download_azureml_model,
        get_azureml_job_status,
        submit_azureml_job,
        train_on_azureml,
    )
    from dreadnode.training.azureml import (
        ComputeConfig as AzureMLComputeConfig,
    )
    from dreadnode.training.azureml import (
        ComputeTier as AzureMLComputeTier,
    )
    from dreadnode.training.azureml import (
        DataConfig as AzureMLDataConfig,
    )
    from dreadnode.training.azureml import (
        EnvironmentConfig as AzureMLEnvironmentConfig,
    )
    from dreadnode.training.azureml import (
        JobStatus as AzureMLJobStatus,
    )
    from dreadnode.training.azureml import (
        VMSize as AzureMLVMSize,
    )
    from dreadnode.training.azureml import (
        WorkspaceConfig as AzureMLWorkspaceConfig,
    )
    from dreadnode.training.dpo import train_dpo
    from dreadnode.training.env_rollouts import (
        VerificationResult,
        batched_environments,
        verify_env_state,
    )
    from dreadnode.training.grpo import train_grpo
    from dreadnode.training.models import (
        TrainingModel,
        TrainingModelPricing,
    )
    from dreadnode.training.ppo import train_ppo
    from dreadnode.training.prime import (
        GPUType as PrimeGPUType,
    )
    from dreadnode.training.prime import (
        PodConfig as PrimePodConfig,
    )
    from dreadnode.training.prime import (
        PrimeTrainer,
        PrimeTrainingConfig,
        run_in_sandbox,
        train_on_prime,
    )
    from dreadnode.training.ray import (
        AsyncRayGRPOTrainer,
        DPOConfig,
        DPOTrainer,
        PPOConfig,
        PPOTrainer,
        RayGRPOConfig,
        RayGRPOTrainer,
        RewardModelTrainer,
        RMConfig,
        SFTConfig,
        SFTTrainer,
    )
    from dreadnode.training.sagemaker import (
        InstanceType as SageMakerInstanceType,
    )
    from dreadnode.training.sagemaker import (
        ResourceConfig as SageMakerResourceConfig,
    )
    from dreadnode.training.sagemaker import (
        SageMakerTrainer,
        SageMakerTrainingConfig,
        get_sagemaker_job_status,
        stop_sagemaker_job,
        submit_sagemaker_job,
        train_on_sagemaker,
    )
    from dreadnode.training.sft import train_sft
    from dreadnode.training.tinker import (
        TinkerSFTConfig,
        TinkerSFTTrainer,
        train_tinker_sft,
    )


# Mapping of lazy-loaded components to their source modules
__lazy_components__: dict[str, tuple[str, str | None]] = {
    # Anyscale training (module, optional rename)
    "AnyscaleJobConfig": ("dreadnode.training.anyscale", None),
    "AnyscaleTrainer": ("dreadnode.training.anyscale", None),
    "AnyscaleTrainingConfig": ("dreadnode.training.anyscale", None),
    "AnyscaleComputeConfig": ("dreadnode.training.anyscale", "ComputeConfig"),
    "submit_anyscale_job": ("dreadnode.training.anyscale", None),
    "train_on_anyscale": ("dreadnode.training.anyscale", None),
    # Azure ML training
    "AzureMLClient": ("dreadnode.training.azureml", None),
    "AzureMLTrainer": ("dreadnode.training.azureml", None),
    "AzureMLTrainingConfig": ("dreadnode.training.azureml", None),
    "AzureMLComputeConfig": ("dreadnode.training.azureml", "ComputeConfig"),
    "AzureMLComputeTier": ("dreadnode.training.azureml", "ComputeTier"),
    "AzureMLDataConfig": ("dreadnode.training.azureml", "DataConfig"),
    "AzureMLEnvironmentConfig": ("dreadnode.training.azureml", "EnvironmentConfig"),
    "AzureMLJobStatus": ("dreadnode.training.azureml", "JobStatus"),
    "AzureMLVMSize": ("dreadnode.training.azureml", "VMSize"),
    "AzureMLWorkspaceConfig": ("dreadnode.training.azureml", "WorkspaceConfig"),
    "cancel_azureml_job": ("dreadnode.training.azureml", None),
    "download_azureml_model": ("dreadnode.training.azureml", None),
    "get_azureml_job_status": ("dreadnode.training.azureml", None),
    "submit_azureml_job": ("dreadnode.training.azureml", None),
    "train_on_azureml": ("dreadnode.training.azureml", None),
    # High-level training functions
    "train_dpo": ("dreadnode.training.dpo", None),
    "train_grpo": ("dreadnode.training.grpo", None),
    "train_ppo": ("dreadnode.training.ppo", None),
    "train_sft": ("dreadnode.training.sft", None),
    # Prime Intellect training
    "PrimeGPUType": ("dreadnode.training.prime", "GPUType"),
    "PrimePodConfig": ("dreadnode.training.prime", "PodConfig"),
    "PrimeTrainer": ("dreadnode.training.prime", None),
    "PrimeTrainingConfig": ("dreadnode.training.prime", None),
    "run_in_sandbox": ("dreadnode.training.prime", None),
    "train_on_prime": ("dreadnode.training.prime", None),
    # Ray training (heavy - requires torch)
    "AsyncRayGRPOTrainer": ("dreadnode.training.ray", None),
    "DPOConfig": ("dreadnode.training.ray", None),
    "DPOTrainer": ("dreadnode.training.ray", None),
    "PPOConfig": ("dreadnode.training.ray", None),
    "PPOTrainer": ("dreadnode.training.ray", None),
    "RayGRPOConfig": ("dreadnode.training.ray", None),
    "RayGRPOTrainer": ("dreadnode.training.ray", None),
    "RewardModelTrainer": ("dreadnode.training.ray", None),
    "RMConfig": ("dreadnode.training.ray", None),
    "SFTConfig": ("dreadnode.training.ray", None),
    "SFTTrainer": ("dreadnode.training.ray", None),
    # SageMaker training
    "SageMakerInstanceType": ("dreadnode.training.sagemaker", "InstanceType"),
    "SageMakerResourceConfig": ("dreadnode.training.sagemaker", "ResourceConfig"),
    "SageMakerTrainer": ("dreadnode.training.sagemaker", None),
    "SageMakerTrainingConfig": ("dreadnode.training.sagemaker", None),
    "get_sagemaker_job_status": ("dreadnode.training.sagemaker", None),
    "stop_sagemaker_job": ("dreadnode.training.sagemaker", None),
    "submit_sagemaker_job": ("dreadnode.training.sagemaker", None),
    "train_on_sagemaker": ("dreadnode.training.sagemaker", None),
    # Tinker training
    "TinkerSFTConfig": ("dreadnode.training.tinker", None),
    "TinkerSFTTrainer": ("dreadnode.training.tinker", None),
    "train_tinker_sft": ("dreadnode.training.tinker", None),
    # Env-backed rollout helpers (in-process, used by both hosted training
    # and SDK-direct training; no torch/ray deps)
    "VerificationResult": ("dreadnode.training.env_rollouts", None),
    "batched_environments": ("dreadnode.training.env_rollouts", None),
    "verify_env_state": ("dreadnode.training.env_rollouts", None),
    # Tinker training model catalog — types only; the actual list lives on
    # the API and is fetched via ``dn.api.get_training_catalog(...)``.
    "TrainingModel": ("dreadnode.training.models", None),
    "TrainingModelPricing": ("dreadnode.training.models", None),
}


def __getattr__(name: str) -> t.Any:
    """Lazy load training components to avoid importing torch/ray at module load."""
    if name in __lazy_components__:
        module_name, attr_name = __lazy_components__[name]
        module = importlib.import_module(module_name)
        # Use the original name if no rename is specified
        component = getattr(module, attr_name or name)
        # Cache in globals for subsequent access
        globals()[name] = component
        return component
    raise AttributeError(f"module 'dreadnode.training' has no attribute '{name}'")


def _scorers_to_reward_fn(
    scorers: list[t.Any],
) -> t.Callable[[list[str], list[str]], list[float]]:
    """Convert dreadnode Scorers to a reward function.

    Multiple scorers are averaged to produce the final reward.
    """
    import asyncio

    from dreadnode.core.metric import Metric

    def reward_fn(_prompts: list[str], completions: list[str]) -> list[float]:
        rewards = []

        for completion in completions:
            scores = []
            for scorer in scorers:
                try:
                    # Call scorer with completion
                    result = scorer(completion)

                    # Handle async scorers
                    if asyncio.iscoroutine(result):
                        result = asyncio.get_event_loop().run_until_complete(result)

                    # Extract float value
                    if isinstance(result, Metric):
                        scores.append(result.value)
                    elif isinstance(result, (int, float, bool)):
                        scores.append(float(result))
                    elif isinstance(result, (list, tuple)):
                        # Multiple metrics - average them
                        for r in result:
                            if isinstance(r, Metric):
                                scores.append(r.value)
                            else:
                                scores.append(float(r))
                except Exception:
                    scores.append(0.0)

            # Average scores from all scorers
            reward = sum(scores) / len(scores) if scores else 0.0
            rewards.append(reward)

        return rewards

    return reward_fn


def _build_reward_fn(
    reward_config: dict[str, t.Any],
    prompts: list[str],  # noqa: ARG001
) -> t.Callable[[list[str], list[str]], list[float]]:
    """Build reward function from configuration."""
    reward_type = reward_config.get("type", "custom")

    if reward_type == "correctness":
        # Simple correctness reward - requires answer_field in prompts
        reward_config.get("tolerance", 0.01)
        reward_config.get("correct_reward", 1.0)
        reward_config.get("incorrect_reward", -0.5)

        def correctness_reward(_prompts: list[str], completions: list[str]) -> list[float]:
            # Default implementation - override with actual logic
            return [0.0] * len(completions)

        return correctness_reward

    if reward_type == "length":
        # Reward based on completion length
        target_length = reward_config.get("target_length", 100)
        max_reward = reward_config.get("max_reward", 1.0)

        def length_reward(_prompts: list[str], completions: list[str]) -> list[float]:
            rewards = []
            for c in completions:
                length_diff = abs(len(c) - target_length)
                reward = max_reward * max(0, 1 - length_diff / target_length)
                rewards.append(reward)
            return rewards

        return length_reward

    if reward_type == "contains":
        # Reward if completion contains certain strings
        required = reward_config.get("required", [])
        reward_per_match = reward_config.get("reward_per_match", 0.5)

        def contains_reward(_prompts: list[str], completions: list[str]) -> list[float]:
            rewards = []
            for c in completions:
                matches = sum(1 for r in required if r.lower() in c.lower())
                rewards.append(matches * reward_per_match)
            return rewards

        return contains_reward

    raise ValueError(f"Unknown reward type: {reward_type}. Use custom reward_fn instead.")


def _load_training_dataset(dataset_config: dict[str, t.Any] | str) -> list[str]:
    """Load prompts from dataset configuration.

    Supports:
    - dreadnode: Load from dreadnode dataset package
    - huggingface: Load from HuggingFace Hub
    - jsonl: Load from JSONL file
    - list: Inline list of prompts
    """
    if isinstance(dataset_config, str):
        dataset_config = {"type": "dreadnode", "name": dataset_config}

    dataset_type = dataset_config.get("type", "huggingface")

    if dataset_type == "dreadnode":
        from dreadnode.datasets.dataset import Dataset

        name = dataset_config["name"]
        prompt_field = dataset_config.get("prompt_field", "prompt")
        prompt_template = dataset_config.get("prompt_template")
        max_samples = dataset_config.get("max_samples", 1000)
        split = dataset_config.get("split")

        ds = Dataset.load(name)
        if not isinstance(ds, Dataset):
            raise ValueError(f"Expected Dataset, got {type(ds)}")

        df = ds.to_pandas(split)

        prompts = []
        for i, row in df.iterrows():
            if i >= max_samples:
                break
            if prompt_template:
                prompt = prompt_template.format(**row.to_dict())
            else:
                prompt = str(row[prompt_field])
            prompts.append(prompt)

        return prompts

    if dataset_type == "huggingface":
        from datasets import load_dataset

        name = dataset_config["name"]
        split = dataset_config.get("split", "train")
        config_name = dataset_config.get("config")
        max_samples = dataset_config.get("max_samples", 1000)
        prompt_field = dataset_config.get("prompt_field", "question")
        prompt_template = dataset_config.get("prompt_template")

        ds = load_dataset(name, config_name, split=split)

        prompts = []
        for i, item in enumerate(ds):
            if i >= max_samples:
                break
            prompt = item[prompt_field]
            if prompt_template:
                prompt = prompt_template.format(**item)
            prompts.append(prompt)

        return prompts

    if dataset_type == "jsonl":
        import json

        path = Path(dataset_config["path"])
        prompt_field = dataset_config.get("prompt_field", "prompt")
        max_samples = dataset_config.get("max_samples", 1000)
        prompt_template = dataset_config.get("prompt_template")

        prompts = []
        with path.open() as f:
            for i, line in enumerate(f):
                if i >= max_samples:
                    break
                item = json.loads(line)
                prompt = prompt_template.format(**item) if prompt_template else item[prompt_field]
                prompts.append(prompt)

        return prompts

    if dataset_type == "list":
        return dataset_config.get("prompts", [])

    raise ValueError(f"Unknown dataset type: {dataset_type}")


__all__ = [
    # Anyscale trainers
    "AnyscaleComputeConfig",
    "AnyscaleJobConfig",
    "AnyscaleTrainer",
    "AnyscaleTrainingConfig",
    # Ray trainers
    "AsyncRayGRPOTrainer",
    # Azure ML trainers
    "AzureMLClient",
    "AzureMLComputeConfig",
    "AzureMLComputeTier",
    "AzureMLDataConfig",
    "AzureMLEnvironmentConfig",
    "AzureMLJobStatus",
    "AzureMLTrainer",
    "AzureMLTrainingConfig",
    "AzureMLVMSize",
    "AzureMLWorkspaceConfig",
    "DPOConfig",
    "DPOTrainer",
    "PPOConfig",
    "PPOTrainer",
    # Prime Intellect trainers
    "PrimeGPUType",
    "PrimePodConfig",
    "PrimeTrainer",
    "PrimeTrainingConfig",
    "RMConfig",
    "RayGRPOConfig",
    "RayGRPOTrainer",
    "RewardModelTrainer",
    "SFTConfig",
    "SFTTrainer",
    # SageMaker trainers
    "SageMakerInstanceType",
    "SageMakerResourceConfig",
    "SageMakerTrainer",
    "SageMakerTrainingConfig",
    # Tinker trainers
    "TinkerSFTConfig",
    "TinkerSFTTrainer",
    # Env-backed rollout helpers
    "VerificationResult",
    "batched_environments",
    "verify_env_state",
    # Tinker training model catalog (types only)
    "TrainingModel",
    "TrainingModelPricing",
    # Helper functions
    "_build_reward_fn",
    "_load_training_dataset",
    "_scorers_to_reward_fn",
    # High-level training functions (Azure ML)
    "cancel_azureml_job",
    "download_azureml_model",
    "get_azureml_job_status",
    # High-level training functions (SageMaker)
    "get_sagemaker_job_status",
    # High-level training functions (Prime)
    "run_in_sandbox",
    "stop_sagemaker_job",
    # High-level training functions (Anyscale)
    "submit_anyscale_job",
    "submit_azureml_job",
    "submit_sagemaker_job",
    # High-level training functions (Ray)
    "train_dpo",
    "train_grpo",
    "train_on_anyscale",
    "train_on_azureml",
    "train_on_prime",
    "train_on_sagemaker",
    "train_ppo",
    "train_sft",
    # High-level training functions (Tinker)
    "train_tinker_sft",
]
