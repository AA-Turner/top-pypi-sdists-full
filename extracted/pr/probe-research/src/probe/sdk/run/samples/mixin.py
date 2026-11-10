"""SamplesMixin, Run's part: `run.samples`. Light on purpose: a run that never logs a sample never
imports the sample contract (about 80 ms)."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .samples import RunSamples

#: The producer a run's own `run.samples` writes as, unless `as_producer` names another.
DEFAULT_PRODUCER = "main"


class SamplesMixin:
    """Part of Run: `run.samples`. Its methods run with `self` the Run; compose() folds them into Run."""

    @property
    def samples(self) -> RunSamples:
        """This run's RL samples, written as this process's producer (`as_producer` for others)."""
        found = self.__dict__.get("_samples_view")
        if found is None:
            with self._steps_lock:
                found = self.__dict__.get("_samples_view")
                if found is None:
                    from .samples import RunSamples

                    producer = os.environ.get("PROBE_SAMPLES_PRODUCER") or DEFAULT_PRODUCER
                    found = self.__dict__["_samples_view"] = RunSamples(self, producer)
        return found

    def _check_sample_commands(self, seq: object) -> None:
        """A lease beat's `commands_seq`: the sample command listener's backstop (rl-next W34). Never raises."""
        view = self.__dict__.get("_samples_view")
        if view is not None:
            view._check_commands_seq(seq)

    def _close_samples(self) -> None:
        """At finish: journal what `run.samples` still holds, ahead of the drain. Never raises."""
        view = self.__dict__.get("_samples_view")
        if view is not None:
            view.close()
