"""The interface every TRL trainer kind's sample hooks implement (RL plan §6.6). A recorder wraps its trainer's
instance methods (`install`) and turns what they see into sample parts through the tracker; the tracker owns the run,
the commits, the seals and the close. The registry that picks one is `recorders/`."""

from __future__ import annotations

from typing import Any


class Recorder:
    """One trainer kind's hooks. ``names`` are the TRL class names it records, matched along the trainer's class
    chain, so a subclass (ServerDistillationTrainer) records as its parent."""

    names: tuple[str, ...] = ()

    def __init__(self, tracker: Any) -> None:
        self.tracker = tracker
        self.trainer = tracker.trainer

    def install(self) -> None:
        """Wrap the trainer's instance methods (`tracker.install`). Runs on every process: a hook that records
        checks `tracker.is_main` itself."""

    def get_unsupported(self) -> dict[str, str]:
        """The capture fields (`CaptureField`) this trainer kind cannot give a sample, each with why
        (`plan(unsupported=)`); none by default."""
        return {}

    def handle_micro_batch(self, inputs: Any) -> None:
        """Before each `training_step`, with the micro-batch it trains."""

    def handle_train_begin(self, step: int) -> None:
        """`on_train_begin`, after TRL's own callbacks (an async trainer's first weight sync)."""

    def handle_step_end(self, step: int) -> None:
        """Optimizer step ``step`` succeeded. The synchronous trainers number weight versions by step."""
        self.tracker.samples.weights(step, after_step=step)

    def handle_save(self, step: int, checkpoint: dict) -> None:
        """`on_save`: the checkpoint folder names the weight version that step made."""
        self.tracker.samples.weights(step, after_step=step, checkpoint=checkpoint)
