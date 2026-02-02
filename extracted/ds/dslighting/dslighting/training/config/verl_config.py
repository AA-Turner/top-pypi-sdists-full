"""
VERL configuration builder.
"""
from typing import Dict, Any, Optional


class VerlConfigBuilder:
    """
    VERL training configuration builder.

    Usage:
    >>> config = VerlConfigBuilder.default()
    >>> config = VerlConfigBuilder.qwen()
    >>> config = VerlConfigBuilder.custom(
    ...     model_path="Qwen/Qwen2.5-Coder-1.5B-Instruct",
    ...     learning_rate=1e-6,
    ... )
    """

    @staticmethod
    def default() -> Dict[str, Any]:
        """Default configuration."""
        return {
            "algorithm": {
                "adv_estimator": "grpo",
                "use_kl_in_reward": False,
            },
            "data": {
                "train_batch_size": 32,
                "max_prompt_length": 4096,
                "max_response_length": 2048,
            },
            "actor_rollout_ref": {
                "rollout": {
                    "name": "vllm",
                    "n": 4,  # GRPO group size
                    "multi_turn": {"format": "hermes"},
                },
                "actor": {
                    "ppo_mini_batch_size": 32,
                    "optim": {"lr": 1e-6},
                },
                "model": {
                    "path": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
                },
            },
            "trainer": {
                "n_gpus_per_node": 1,
                "val_before_train": True,
                "test_freq": 32,
                "save_freq": 64,
                "total_epochs": 2,
            },
        }

    @staticmethod
    def qwen() -> Dict[str, Any]:
        """Preset for Qwen models."""
        config = VerlConfigBuilder.default()
        config["actor_rollout_ref"]["model"]["path"] = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
        return config

    @staticmethod
    def llama() -> Dict[str, Any]:
        """Preset for LLaMA models."""
        config = VerlConfigBuilder.default()
        config["actor_rollout_ref"]["model"]["path"] = "meta-llama/Llama-3.2-1B-Instruct"
        config["actor_rollout_ref"]["rollout"]["multi_turn"]["format"] = "llama3_json"
        return config

    @staticmethod
    def custom(
        model_path: str,
        learning_rate: float = 1e-6,
        train_batch_size: int = 32,
        group_size: int = 4,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Custom configuration.

        Parameters
        ----------
        model_path : str
            Model path.
        learning_rate : float
            Learning rate.
        train_batch_size : int
            Training batch size.
        group_size : int
            GRPO group size
        **kwargs
            Additional config parameters.

        Returns
        -------
        Dict[str, Any]
            VERL configuration.
        """
        config = VerlConfigBuilder.default()

        # Apply custom parameters.
        config["actor_rollout_ref"]["model"]["path"] = model_path
        config["actor_rollout_ref"]["actor"]["optim"]["lr"] = learning_rate
        config["data"]["train_batch_size"] = train_batch_size
        config["actor_rollout_ref"]["rollout"]["n"] = group_size

        # Apply extra parameters using dot notation.
        for key, value in kwargs.items():
            keys = key.split(".")
            config_part = config
            for k in keys[:-1]:
                config_part = config_part[k]
            config_part[keys[-1]] = value

        return config


__all__ = ["VerlConfigBuilder"]
