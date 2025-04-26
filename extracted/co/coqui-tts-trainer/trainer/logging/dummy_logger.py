import os
from typing import TYPE_CHECKING, Any

from trainer._types import Audio, Figure
from trainer.config import TrainerConfig
from trainer.logging.base_dash_logger import BaseDashboardLogger

if TYPE_CHECKING:
    import torch


class DummyLogger(BaseDashboardLogger):
    """DummyLogger that implements the API but does nothing."""

    def model_weights(self, model: "torch.nn.Module", step: int) -> None:
        pass

    def add_scalar(self, title: str, value: float, step: int) -> None:
        pass

    def add_figure(self, title: str, figure: Figure, step: int) -> None:
        pass

    def add_config(self, config: TrainerConfig) -> None:
        pass

    def add_audio(self, title: str, audio: Audio, step: int, sample_rate: int) -> None:
        pass

    def add_text(self, title: str, text: str, step: int) -> None:
        pass

    def add_artifact(
        self, file_or_dir: str | os.PathLike[Any], name: str, artifact_type: str, aliases: list[str] | None = None
    ) -> None:
        pass

    def add_scalars(self, scope_name: str, scalars: dict[str, float], step: int) -> None:
        pass

    def add_figures(self, scope_name: str, figures: dict[str, Figure], step: int) -> None:
        pass

    def add_audios(self, scope_name: str, audios: dict[str, Audio], step: int, sample_rate: int) -> None:
        pass

    def flush(self) -> None:
        pass

    def finish(self) -> None:
        pass

    def train_step_stats(self, step: int, stats: dict[str, float]) -> None:
        self.add_scalars(scope_name="TrainIterStats", scalars=stats, step=step)

    def train_epoch_stats(self, step, stats):
        self.add_scalars(scope_name="TrainEpochStats", scalars=stats, step=step)

    def train_figures(self, step, figures):
        self.add_figures(scope_name="TrainFigures", figures=figures, step=step)

    def train_audios(self, step, audios, sample_rate):
        self.add_audios(scope_name="TrainAudios", audios=audios, step=step, sample_rate=sample_rate)

    def eval_stats(self, step, stats):
        self.add_scalars(scope_name="EvalStats", scalars=stats, step=step)

    def eval_figures(self, step, figures):
        self.add_figures(scope_name="EvalFigures", figures=figures, step=step)

    def eval_audios(self, step, audios, sample_rate):
        self.add_audios(scope_name="EvalAudios", audios=audios, step=step, sample_rate=sample_rate)

    def test_audios(self, step, audios, sample_rate):
        self.add_audios(scope_name="TestAudios", audios=audios, step=step, sample_rate=sample_rate)

    def test_figures(self, step, figures):
        self.add_figures(scope_name="TestFigures", figures=figures, step=step)
