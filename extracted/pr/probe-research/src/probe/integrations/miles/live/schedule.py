"""RolloutSchedule: the step Miles' rollout executor is collecting and the weight version its engines serve, read off
each `RolloutFnTrainInput` it makes (`rollout_executor.py:397-401`), so a try's start names both. Why: DESIGN.md."""

from __future__ import annotations

import functools
import threading
from collections.abc import Callable
from typing import Any

_MARK = "__probe_wrapped__"


class RolloutSchedule:
    """The newest train input per policy (`trainer_model_id`, None for a one-policy run): its rollout id and version."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._inputs: dict[Any, tuple[int | None, int | None]] = {}

    def record_input(self, rollout_input: Any) -> None:
        """A train input Miles made: the executor is about to collect ``rollout_id`` on ``weight_version``."""
        step = _to_count(getattr(rollout_input, "rollout_id", None))
        version = _to_count(getattr(rollout_input, "weight_version", None))
        with self._lock:
            self._inputs[getattr(rollout_input, "trainer_model_id", None)] = (step, version)

    def get_current(self, model_id: Any = None) -> tuple[int | None, int | None]:
        """(step, weight version) for ``model_id``'s rollouts, else the one-policy run's; (None, None) before any."""
        with self._lock:
            found = self._inputs.get(model_id)
            return found if found is not None else self._inputs.get(None, (None, None))


def wrap_train_input(module: Any, record: Callable[[Any], None]) -> None:
    """`miles.rollout.base_types` as it loads: each `RolloutFnTrainInput` (`base_types.py:34-44`) goes to ``record``
    once made. Miles' own `__init__` runs first and unchanged."""
    cls = getattr(module, "RolloutFnTrainInput", None)
    original = cls.__dict__.get("__init__") if isinstance(cls, type) else None
    if not callable(original) or getattr(original, _MARK, False):
        return

    @functools.wraps(original)
    def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
        original(self, *args, **kwargs)
        try:
            record(self)
        except Exception:  # noqa: BLE001 -- fail open: a try then starts without its step and version
            pass

    setattr(__init__, _MARK, True)
    cls.__init__ = __init__


def _to_count(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None
