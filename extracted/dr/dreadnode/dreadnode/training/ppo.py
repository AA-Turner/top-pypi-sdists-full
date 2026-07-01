import typing as t


def train_ppo(
    config_dict: dict[str, t.Any],
    prompts: list[str],
    reward_fn: t.Callable[..., t.Any],
) -> t.Any:
    """Train with PPO."""
    from dreadnode.training.ray import PPOConfig, PPOTrainer

    ppo_config = PPOConfig(**config_dict)
    trainer = PPOTrainer(ppo_config)
    return trainer.train(prompts=prompts, reward_fn=reward_fn)
