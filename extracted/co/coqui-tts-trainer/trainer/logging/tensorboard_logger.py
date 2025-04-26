import os
import traceback
from typing import Any

import torch
from torch.utils.tensorboard import SummaryWriter

from trainer._types import Audio, Figure
from trainer.config import TrainerConfig
from trainer.logging.base_dash_logger import BaseDashboardLogger


class TensorboardLogger(BaseDashboardLogger):
    def __init__(self, log_dir: str | os.PathLike[Any], model_name: str) -> None:
        self.model_name = model_name
        self.writer = SummaryWriter(log_dir)

    def model_weights(self, model: torch.nn.Module, step: int) -> None:
        layer_num = 1
        for name, param in model.named_parameters():
            if param.numel() == 1:
                self.writer.add_scalar(f"layer{layer_num}-{name}/value", param.max(), step)
            else:
                self.writer.add_scalar(f"layer{layer_num}-{name}/max", param.max(), step)
                self.writer.add_scalar(f"layer{layer_num}-{name}/min", param.min(), step)
                self.writer.add_scalar(f"layer{layer_num}-{name}/mean", param.mean(), step)
                self.writer.add_scalar(f"layer{layer_num}-{name}/std", param.std(), step)
                self.writer.add_histogram(f"layer{layer_num}-{name}/param", param, step)
                self.writer.add_histogram(f"layer{layer_num}-{name}/grad", param.grad, step)
            layer_num += 1

    def add_config(self, config: TrainerConfig) -> None:
        self.add_text("model-config", f"<pre>{config.to_json()}</pre>", 0)

    def add_scalar(self, title: str, value: float, step: int) -> None:
        self.writer.add_scalar(title, value, step)

    def add_audio(self, title: str, audio: Audio, step: int, sample_rate: int) -> None:
        self.writer.add_audio(title, audio, step, sample_rate=sample_rate)

    def add_text(self, title: str, text: str, step: int) -> None:
        self.writer.add_text(title, text, step)

    def add_figure(self, title: str, figure: Figure, step: int) -> None:
        self.writer.add_figure(title, figure, step)

    def add_artifact(
        self, file_or_dir: str | os.PathLike[Any], name: str, artifact_type: str, aliases: list[str] | None = None
    ) -> None:
        pass

    def add_scalars(self, scope_name: str, scalars: dict[str, float], step: int) -> None:
        for key, value in scalars.items():
            self.add_scalar(f"{scope_name}/{key}", value, step)

    def add_figures(self, scope_name: str, figures: dict[str, Figure], step: int) -> None:
        for key, value in figures.items():
            self.writer.add_figure(f"{scope_name}/{key}", value, step)

    def add_audios(self, scope_name: str, audios: dict[str, Audio], step: int, sample_rate: int) -> None:
        for key, value in audios.items():
            if value.dtype == "float16":
                value = value.astype("float32")
            try:
                self.add_audio(
                    f"{scope_name}/{key}",
                    value,
                    step,
                    sample_rate=sample_rate,
                )
            except RuntimeError:
                traceback.print_exc()

    def flush(self) -> None:
        self.writer.flush()

    def finish(self) -> None:
        self.writer.close()
