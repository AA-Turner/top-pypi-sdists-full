import typing as t


def train_grpo(
    config_dict: dict[str, t.Any],
    prompts: list[str],
    reward_fn: t.Callable[..., t.Any],
) -> t.Any:
    """Train with GRPO."""
    from dreadnode.training.ray import RayGRPOConfig, RayGRPOTrainer

    grpo_config = RayGRPOConfig(**config_dict)

    trainer = RayGRPOTrainer(grpo_config)

    return trainer.train(prompts=prompts, reward_fn=reward_fn)
