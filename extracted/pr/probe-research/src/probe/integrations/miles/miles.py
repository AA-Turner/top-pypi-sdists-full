"""The Miles tracking backend (RL plan §6.1 W16): every Miles process writes through its own SDK outbox. The
driver is the run's owner; the rollout executor and the train ranks join it as `rank` producers. Nothing
is shared on disk and nothing is sent from Miles' loop: the detached outbox worker sends."""

from __future__ import annotations

import logging
import os
from typing import Any

from probe.integrations.miles.scrub import _capture_config, _to_scalar
from probe.integrations.miles.spec import set_arg

logger = logging.getLogger(__name__)

#: `PROBE_MILES=off` keeps a registered backend from starting (upstream's `is_supported`).
DISABLE_ENV = "PROBE_MILES"
#: Miles' step counters (`metric_utils.py:23-30`); a row's own namespace prefixes them.
_STEP_AXES = ("train/step", "rollout/step", "eval/step")


def _list_axis_keys(step_key: str | None) -> frozenset[str]:
    """The row's step key and its sibling counters: upstream train rows also carry
    `rollout/step` (`backends/training_utils/metrics/log_utils.py:562`)."""
    if not step_key:
        return frozenset()
    for axis in _STEP_AXES:
        if step_key.endswith(axis):
            namespace = step_key[: -len(axis)]
            return frozenset({step_key, *(namespace + sibling for sibling in _STEP_AXES)})
    return frozenset({step_key})


def _is_disabled() -> bool:
    """`PROBE_MODE=disabled`: no client, no run, nothing on disk (TODOS.md, closed by W16)."""
    from probe.sdk.settings.settings import Mode, resolve_mode

    return resolve_mode(None) is Mode.DISABLED


class ProbeTracker:
    """One Miles process's tracker. The primary (the driver) owns the run; any other process (the
    rollout executor, a train main rank) is a producer of it."""

    def __init__(self) -> None:
        self._args: Any = None
        self._run: Any = None
        self._is_primary = False
        self._should_fail_open = True
        self._is_owner_here = False
        self._is_finished = False
        self._dashboard: Any = None
        self._compute: Any = None

    def init(self, args, *, primary: bool = True, **kwargs) -> None:
        self._args, self._is_primary = args, primary
        self._should_fail_open = bool(getattr(args, "probe_fail_open", True))
        if _is_disabled() or os.environ.get(DISABLE_ENV, "").strip().lower() == "off":
            return
        try:
            if primary:
                self._open_owner(args)
            else:
                self._join(args, is_rollout=kwargs.get("router_addr") is not None)
        except Exception as exc:  # noqa: BLE001 -- fail open unless the job asked otherwise
            self._handle_error("open the Probe run", exc)

    def _open_owner(self, args) -> None:
        import probe
        from probe.integrations.miles.compute import start_compute_timeline
        from probe.integrations.miles.owner import make_external_id, open_owner_run

        run = probe.active_run()
        if run is None:  # no launcher opened it: open it here (workers then cannot join on upstream)
            external_id = make_external_id(args, os.environ)
            os.environ.setdefault("MILES_RUN_ID", external_id)
            run = open_owner_run(args, external_id=external_id)
            self._is_owner_here = True
        else:
            run.update_config(_capture_config(args))
        self._run = run
        # The fork's actors read the run from args (they get the args after this); upstream's from the env.
        set_arg(args, "probe_run_id", run.id)
        set_arg(args, "probe_experiment_id", getattr(run, "experiment_id", None))
        rollout_count = getattr(args, "num_rollout", None)
        if isinstance(rollout_count, int) and not isinstance(rollout_count, bool) and rollout_count > 0:
            run.samples.plan(expected_steps=rollout_count)
        self._record_base_model(args, run)
        self._start_dashboard_export(args, run)
        self._compute = start_compute_timeline(run, args)

    def _join(self, args, *, is_rollout: bool) -> None:
        from probe.integrations.miles.samples import PROCESS, ROLLOUT, get_trainer_name, install_event_recorder

        producer = ROLLOUT if is_rollout else get_trainer_name(0, getattr(args, "trainer_model_id", None))
        self._run = PROCESS.get_handle(args, producer=producer)
        if is_rollout:
            install_event_recorder()

    def _record_base_model(self, args, run: Any) -> None:
        """`--hf-checkpoint` in the run's lineage (`owner.record_base_model`), once per run; never a reason to stop."""
        try:
            from probe.integrations.miles.owner import record_base_model

            record_base_model(run, args)
        except Exception:  # noqa: BLE001 -- lineage is a convenience
            logger.warning("Probe could not record the Miles run's base model; Miles continues", exc_info=True)

    def _start_dashboard_export(self, args, run: Any) -> None:
        if not getattr(args, "dump_details", None):
            return
        try:
            from probe.integrations.miles.dashboard import start_capture

            self._dashboard = start_capture(args, run.id)
        except Exception:  # noqa: BLE001
            logger.warning("Miles dashboard export could not start; metrics continue", exc_info=True)

    def log(self, metrics: dict[str, Any], step: int | None = None, **kwargs) -> None:
        if self._run is None:
            return
        step_key = kwargs.get("step_key")
        axis_keys = _list_axis_keys(step_key)
        scalars = {
            key: number
            for key, value in metrics.items()
            # Step counters are x-axes, not series.
            if key not in axis_keys and (number := _to_scalar(value)) is not None
        }
        if not scalars:
            return
        dimensions = kwargs.get("dimensions")
        try:
            self._run.log(
                scalars,
                step=int(step) if step is not None else None,
                kind="validation" if step_key == "eval/step" else "model",
                dimensions=dimensions if isinstance(dimensions, dict) else None,
            )
        except Exception as exc:  # noqa: BLE001
            self._handle_error("record metrics", exc)

    def finish(self, status: str | None = None) -> None:
        """Miles' driver calls this from a disposer, which cannot tell a crash from a clean end
        (`utils/orchestration_utils.py:69`): with no ``status`` a run opened here stays open and the
        process's exit closes it with how it really ended (`probe.init`'s exit hooks)."""
        if self._is_finished or self._run is None:
            return
        self._is_finished = True
        if not self._is_primary:
            self._close_producer()
            return
        for closer in (self._compute, self._dashboard):
            try:
                if closer is not None:
                    closer.close()
            except Exception:  # noqa: BLE001
                logger.warning("Probe could not close a Miles export; finishing anyway", exc_info=True)
        try:
            from probe.integrations.miles.owner import close_owner_run

            self._record_last_checkpoint()
            # A run the launcher opened is the launcher's to close; one opened here closes now only with a
            # status a caller gave (`set_terminal_status`), else at the process's exit.
            close_owner_run(self._run, self._args, status=status if self._is_owner_here else None)
        except Exception as exc:  # noqa: BLE001
            self._handle_error("close the run", exc)

    def _close_producer(self) -> None:
        """Journal what this producer still holds; its lease is released when the process exits."""
        try:
            self._run.samples.close()
        except Exception as exc:  # noqa: BLE001
            self._handle_error("close this producer", exc)

    def _record_last_checkpoint(self) -> None:
        """The final save, which no later train step sees (`trainer.py`): the driver records it."""
        from probe.integrations.miles.samples import find_new_checkpoint, record_checkpoint

        saved = find_new_checkpoint(self._args, set())
        rollout_count = getattr(self._args, "num_rollout", None)
        if saved is not None and isinstance(rollout_count, int) and saved.step == rollout_count - 1:
            record_checkpoint(self._run, saved)

    def _handle_error(self, operation: str, exc: Exception) -> None:
        if not self._should_fail_open:
            raise exc
        logger.warning("Probe could not %s; Miles will continue: %s", operation, exc, exc_info=True)


class ProbeBackend:
    """Duck-typed adapter for Miles' tracking manager: the fork's init/log/finish, plus upstream's
    `is_supported` and `define_step_key_metric_group` (`utils/tracking_utils/base.py:29-45`)."""

    #: Set by `probe.connectors.miles.register()` in this process (registry entries are per process).
    _is_registered_here = False

    def __init__(self) -> None:
        self._tracker = ProbeTracker()
        #: Set only by a caller that knows how the run ended; else the process's exit records it.
        self._terminal_status: str | None = None

    @classmethod
    def mark_registered(cls) -> None:
        cls._is_registered_here = True

    @classmethod
    def is_supported(cls, args) -> bool:
        """Upstream's opt-in. Its registry flag is `__class__` (always truthy, since frozen args
        can declare no `use_probe`), so this is the switch: registered here and PROBE_MILES not off."""
        return cls._is_registered_here and os.environ.get(DISABLE_ENV, "").strip().lower() != "off"

    def define_step_key_metric_group(self, prefix: str, step_key: str) -> None:
        """Nothing to declare: every Probe point carries its own step."""

    def init(self, args, *, primary: bool = True, **kwargs) -> None:
        self._tracker.init(args, primary=primary, **kwargs)

    def log(self, metrics: dict[str, Any], step: int | None = None, **kwargs) -> None:
        self._tracker.log(metrics, step=step, **kwargs)

    def set_terminal_status(self, status: str) -> None:
        self._terminal_status = status

    def finish(self) -> None:
        """Upstream and the fork both call this with no status (`base.py:199-207`)."""
        self._tracker.finish(status=self._terminal_status)


MilesMetricTracker = ProbeTracker
MilesMetricBackend = ProbeBackend

