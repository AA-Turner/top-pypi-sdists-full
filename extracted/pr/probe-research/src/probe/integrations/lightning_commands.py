"""`ProbeCommands`: the Lightning callback that takes the run's checkpoint, config, stop, pause and resume commands
(agentic W&B C.1, D23), beside `ProbeLogger`::

    trainer = Trainer(logger=ProbeLogger(project="folding"), callbacks=[ProbeCommands()])

On every rank, at a batch end every rank reaches, rank 0's claimed commands are handed to every rank
(`probe.integrations._commands`): a checkpoint is `trainer.save_checkpoint` on every rank (a collective under
DeepSpeed and FSDP), recorded on rank 0 as the run's checkpoint artifact; a stop sets `trainer.should_stop`, a config
sets the learning rate on this rank's optimizers and schedulers, a pause holds every rank at that batch end (rank 0
first sends the batch's row, which Lightning sends only after the hook) until a resume or a stop. A kind the script declared
(`run.on(TrainerCommand.EVAL_NOW, fn)`) runs on rank 0. The run is `ProbeLogger`'s, or the script's active run. Why:
sdk/run/commands/DESIGN.md "Every rank"."""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

try:
    from lightning.fabric.utilities.apply_func import convert_tensors_to_scalars
    from lightning.pytorch.callbacks import Callback
except ImportError:  # pragma: no cover - exercised only without `lightning`
    try:
        from lightning_fabric.utilities.apply_func import convert_tensors_to_scalars  # type: ignore[no-redef]
        from pytorch_lightning.callbacks import Callback  # type: ignore[no-redef]
    except ImportError as _missing:
        # `name` carries the missing module, so callers tell an absent optional extra from a broken import.
        raise ImportError(
            "probe.integrations.lightning_commands needs PyTorch Lightning, which is not installed. "
            "Install it with Probe's extra: pip install 'probe-research[lightning]'",
            name=getattr(_missing, "name", None) or "lightning",
        ) from _missing

from probe.foundation.safe_warn import safe_warn

from probe.sdk.run import trainer_facts

from . import _checkpoints
from ._commands import TrainerCommands, apply_resume_overrides, get_save_result
from .lightning import COMMANDED_OWNER, ProbeLogger

#: Where a checkpoint asked for is saved, under the trainer's root.
CHECKPOINT_FOLDER = "probe-commands"


def _find_run(trainer: Any) -> Any:
    """Rank 0's run: `ProbeLogger`'s, else the script's active run; None on other ranks."""
    if getattr(trainer, "global_rank", 0) != 0:
        return None
    for logger in getattr(trainer, "loggers", None) or []:
        run = getattr(logger, "_run", None)
        if run is not None and hasattr(run, "_commands"):
            return run
    from probe.sdk.fluent.fluent import active_run

    run = active_run()
    return run if run is not None and hasattr(run, "_commands") else None


def _set_fitted_last_step(trainer: Any, step: int | None) -> None:
    """Tell each of the trainer's `ProbeLogger`s the step the fit ended at, so an eval after it never reads past the
    run's total (`ProbeLogger.set_fitted_last_step`)."""
    for logger in getattr(trainer, "loggers", None) or []:
        if isinstance(logger, ProbeLogger):
            logger.set_fitted_last_step(step)


def _send_batch_now(trainer: Any) -> None:
    """Rank 0, before a hold at a batch end: the batch's row to each `ProbeLogger`, as Lightning would send it after
    the hook (`_LoggerConnector.update_train_step_metrics`). Reads Lightning's step cache (no collective, no side
    effect); fails open: on a Lightning that moved these, the row comes at resume."""
    loggers = [logger for logger in getattr(trainer, "loggers", None) or [] if isinstance(logger, ProbeLogger)]
    if not loggers:
        return
    try:
        connector = trainer._logger_connector
        if trainer.fit_loop._should_accumulate() and trainer.lightning_module.automatic_optimization:
            return
        if not (connector.should_update_logs or trainer.fast_dev_run):
            return  # Lightning sends no row for this batch either
        metrics = dict(convert_tensors_to_scalars(connector.metrics["log"]))
        step = metrics.pop("step", None)
        if step is None:
            metrics.setdefault("epoch", trainer.current_epoch)
            step = trainer.fit_loop.epoch_loop._batches_that_stepped
    except Exception as exc:  # noqa: BLE001 -- fail open: the hold goes on, the row comes after it
        safe_warn.warn(f"probe: sending the paused batch's metrics failed ({type(exc).__name__}: {exc}); they are "
                       "sent at resume.")  # fmt: skip
        return
    for logger in loggers:
        logger.send_before_hold(metrics, int(step))


def _apply_checkpoint(commands: TrainerCommands, run: Any, command: dict, trainer: Any) -> None:
    """`trainer.save_checkpoint` on every rank (a collective under sharded strategies); rank 0 records the save and
    answers with its artifact id (agentic W&B C.1), step and path."""
    path = os.path.join(trainer.default_root_dir, CHECKPOINT_FOLDER, f"step={trainer.global_step}.ckpt")
    trainer.save_checkpoint(path)
    if run is None:
        return
    artifact_id = _record_save(trainer, run, path, str(command["id"]))
    commands.answer(run, command, result=get_save_result(trainer.global_step, path, artifact_id))


def _record_save(trainer: Any, run: Any, path: str, command_id: str) -> str | None:
    """Rank 0: a save no checkpoint callback reports, as the run's checkpoint artifact carrying `meta.command_id`,
    written in hand. The `ProbeLogger` writing this run records it (its ``checkpoints=`` mode and ``log_model``);
    with none, it is a path reference on the run. Its artifact id; None when not recorded or still queued."""
    step = trainer.global_step
    for logger in getattr(trainer, "loggers", None) or []:
        if isinstance(logger, ProbeLogger) and logger._run is run:
            return logger.record_commanded_checkpoint(path, step, command_id)
    local = os.path.abspath(path)
    meta = {"original_filename": os.path.basename(local), "callback": COMMANDED_OWNER, "step": step,
            "written_during_run": True, "command_id": command_id}  # fmt: skip
    try:
        written = run.log_artifact(os.path.basename(local), path=local, kind="checkpoint", reference=True,
                                   step_index=step, meta=meta, sync=True)  # fmt: skip
    except Exception as exc:  # noqa: BLE001 -- the save happened; recording it never stops training
        safe_warn.warn(f"probe: recording the checkpoint asked for at step {step} failed ({type(exc).__name__}: "
                       f"{exc}); it is at {local}, and training continues.")  # fmt: skip
        return None
    return _checkpoints.get_artifact_id(written)


def _apply_stop(commands: TrainerCommands, run: Any, command: dict, trainer: Any) -> None:
    trainer.should_stop = True
    commands.answer(run, command, result={"step": trainer.global_step})


def _apply_config(commands: TrainerCommands, run: Any, command: dict, trainer: Any) -> None:
    schedulers = [config.scheduler for config in getattr(trainer, "lr_scheduler_configs", None) or []]
    commands.apply_config(run, command, getattr(trainer, "optimizers", None) or [], schedulers)


def _run_declared(commands: TrainerCommands, run: Any, command: dict, trainer: Any) -> None:
    commands.run_declared(run, command)


#: What each built-in command does in the Trainer, on every rank (a kind the script declared: its own handler).
_APPLIERS = {"checkpoint": _apply_checkpoint, "stop": _apply_stop, "config": _apply_config}


class ProbeCommands(Callback):
    """Takes the run's commands on every rank; add it on every rank (Lightning adds callbacks everywhere)."""

    def __init__(self) -> None:
        super().__init__()
        self._commands = TrainerCommands()

    def on_train_start(self, trainer: Any, pl_module: Any) -> None:
        run = _find_run(trainer)
        self._commands.begin(run)
        # `probe run resume`: Lightning restored the checkpoint (`fit(ckpt_path=...)`) before this hook, so the asked
        # learning rate goes on now, on every rank (agentic W&B C.2).
        schedulers = [config.scheduler for config in getattr(trainer, "lr_scheduler_configs", None) or []]
        apply_resume_overrides(run, getattr(trainer, "optimizers", None) or [], schedulers)
        self._commands.hold(run, self._make_apply(run, trainer))  # a pause the last fit answered but never held at
        if run is not None:  # rank 0: the trainer's own step count (inf without max_steps or max_epochs: unknown).
            # Lightning logs at `_batches_that_stepped` before it counts the batch, so its steps run 0..count-1.
            trainer_facts.send_total_steps(run, getattr(trainer, "estimated_stepping_batches", None),
                                           is_zero_based=True)  # fmt: skip

    def on_fit_start(self, trainer: Any, pl_module: Any) -> None:
        _set_fitted_last_step(trainer, None)

    def on_fit_end(self, trainer: Any, pl_module: Any) -> None:
        # An eval after the fit logs at `_batches_that_stepped`, the count: one past the fit's last step.
        count = getattr(getattr(getattr(trainer, "fit_loop", None), "epoch_loop", None), "_batches_that_stepped", None)
        _set_fitted_last_step(trainer, count - 1 if isinstance(count, int) and count > 0 else None)

    def on_train_batch_end(self, trainer: Any, pl_module: Any, outputs: Any, batch: Any, batch_index: int) -> None:
        # A pause holds every rank here, at this batch's end, until a resume or a stop (D23). Lightning sends the
        # batch's metrics to its loggers only after this hook, so rank 0 sends them first: the page shows this step.
        run = _find_run(trainer)
        apply = self._make_apply(run, trainer)
        self._commands.run(run, trainer.global_step, apply)
        if self._commands.is_hold_due:
            if run is not None:
                _send_batch_now(trainer)
            self._commands.hold(run, apply)

    def _make_apply(self, run: Any, trainer: Any) -> Callable[[dict], None]:
        return lambda command: _APPLIERS.get(command["kind"], _run_declared)(self._commands, run, command, trainer)


__all__ = ["CHECKPOINT_FOLDER", "ProbeCommands"]
