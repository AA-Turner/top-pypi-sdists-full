import typing as t


def train_sft(config_dict: dict[str, t.Any], prompts: list[str]) -> t.Any:
    """Train with SFT."""
    from dreadnode.training.ray import SFTConfig, SFTTrainer

    sft_config = SFTConfig(**config_dict)
    trainer = SFTTrainer(sft_config)
    return trainer.train(prompts)
