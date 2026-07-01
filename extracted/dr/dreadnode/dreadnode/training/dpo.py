import typing as t


def train_dpo(config_dict: dict[str, t.Any], prompts: list[str]) -> t.Any:
    """Train with DPO."""
    from dreadnode.training.ray import DPOConfig, DPOTrainer

    dpo_config = DPOConfig(**config_dict)
    trainer = DPOTrainer(dpo_config)
    return trainer.train(prompts)
