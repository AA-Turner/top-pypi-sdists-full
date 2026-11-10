"""Opt-in Console reporting through the training model's existing writer."""

import asyncio
import logging
import os
from collections.abc import Mapping
from dataclasses import dataclass

from river_client._run_metrics import MAX_BATCH_VALUES, _check_values

from .losses import _positive


@dataclass(frozen=True)
class Metrics:
    """Opt-in AsyncTrainer reporting to River Console through ``model.log()``.

    Both streams are off by default; enable only those your script does not
    already publish. ``RIVER_METRICS_DISABLED=1`` disables both.

    Attributes:
        steps: Publish each completed Step's metrics.
        interval: Seconds between ``progress/*`` snapshots, such as 60.
            ``None`` disables progress reporting independently of steps.
    """

    steps: bool = False
    interval: float | None = None

    def __post_init__(self):
        if not isinstance(self.steps, bool):
            raise TypeError("steps must be a bool")
        if self.interval is not None:
            _positive(self.interval, "interval")


def _scalar_metrics(values, prefix="", *, skip_metadata=False):
    result, rejected = {}, 0
    for key, value in values.items():
        if not isinstance(key, str):
            rejected += 1
            continue
        name = f"{prefix}/{key}" if prefix else key
        if isinstance(value, Mapping):
            nested, skipped = _scalar_metrics(value, name, skip_metadata=skip_metadata)
            result.update(nested)
            rejected += skipped
            continue
        try:
            result.update(_check_values({name: value}))
        except TypeError:
            if not (
                skip_metadata and (value is None or isinstance(value, (str, bool)))
            ):
                rejected += 1
        except ValueError:
            rejected += 1
    return result, rejected


class MetricsReporter:
    def __init__(self, model, *, steps, interval):
        self.model, self.steps, self.interval = model, steps, interval
        self.enabled = (
            (steps or interval is not None)
            and callable(getattr(model, "log", None))
            and os.environ.get("RIVER_METRICS_DISABLED", "").strip().lower()
            not in {"1", "true", "yes", "on"}
        )
        self._disabled_streams = set()
        self._warnings = set()
        self.include_rollouts = False

    def _warn(self, kind, detail):
        if kind not in self._warnings:
            self._warnings.add(kind)
            try:
                logging.getLogger(__name__).warning(
                    "AsyncTrainer metrics %s: %s", kind, detail
                )
            except Exception:
                pass

    def _define_metrics(self, values, coordinates):
        get_writer = getattr(self.model, "_get_metrics", None)
        if not callable(get_writer):
            return
        try:
            get_writer()._define_metric_defaults(
                coordinates | values,
                step_metric="model_step" if coordinates else "_river/timestamp",
                hidden=coordinates,
            )
        except Exception as error:
            self._warn("chart setup failed", error)

    def _log(self, values, prefix="", coordinates=None):
        stream = "progress" if prefix else "step"
        if not self.enabled or stream in self._disabled_streams:
            return
        try:
            values, rejected = _scalar_metrics(
                values, prefix, skip_metadata=bool(prefix)
            )
            if rejected:
                self._warn(
                    "skipped invalid entries",
                    "invalid names or unsupported/non-finite values",
                )
            coordinates = coordinates or {}
            values.update(coordinates)
            items = [
                (key, value) for key, value in values.items() if key not in coordinates
            ]
            size = MAX_BATCH_VALUES - len(coordinates)
            for start in range(0, max(1, len(items)), size):
                chunk = dict(items[start : start + size]) | coordinates
                if chunk:
                    self._define_metrics(chunk, coordinates)
                    self.model.log(chunk)
        except Exception as error:
            self._disabled_streams.add(stream)
            self._warn(f"{stream} reporting disabled for this run", error)

    def log_step(self, step):
        if self.steps:
            self._log(
                step.metrics,
                coordinates={
                    "batch_step": step.n,
                    "model_step": step.model_step,
                    "optimizer_step": step.model_step,
                },
            )

    def log_progress(self, trainer):
        if (
            not self.enabled
            or self.interval is None
            or "progress" in self._disabled_streams
        ):
            return
        try:
            progress = dict(trainer.progress())
            if not self.include_rollouts:
                progress.pop("rollouts", None)
            self._log(progress, "progress")
        except Exception as error:
            self._warn("progress snapshot failed", error)

    async def _report_progress(self, trainer):
        while self.enabled and "progress" not in self._disabled_streams:
            self.log_progress(trainer)
            await asyncio.sleep(self.interval)
