"""The Trainer callback a TRL tracker adds (RL plan §6.6): step ends commit and seal, saves name a weight version's
checkpoint, the train end closes the record. It is a `TrainerCallback` by shape, not by class, so this package never
imports transformers: transformers calls each event by name (`CallbackHandler.call_event`), and every event this
does not handle is a no-op."""

from __future__ import annotations

from typing import Any


def _ignore(*_args: Any, **_kwargs: Any) -> None:
    return None


class TrlCallback:
    """Forwards the events the tracker needs, on the world-zero process only (TRL logs from there too)."""

    def __init__(self, tracker: Any) -> None:
        self.tracker = tracker

    def on_train_begin(self, args: Any, state: Any, control: Any, **kwargs: Any) -> None:
        self.tracker.handle_train_begin(int(state.global_step))

    def on_step_end(self, args: Any, state: Any, control: Any, **kwargs: Any) -> None:
        self.tracker.handle_step_end(int(state.global_step))

    def on_evaluate(self, args: Any, state: Any, control: Any, **kwargs: Any) -> None:
        self.tracker.handle_evaluate(int(state.global_step))

    def on_save(self, args: Any, state: Any, control: Any, **kwargs: Any) -> None:
        self.tracker.handle_save(int(state.global_step))

    def on_train_end(self, args: Any, state: Any, control: Any, **kwargs: Any) -> None:
        self.tracker.handle_train_end(int(state.global_step))

    def __getattr__(self, name: str) -> Any:
        if name.startswith("on_"):
            return _ignore  # an event this callback does not need (on_log, on_substep_end, ...)
        raise AttributeError(name)
