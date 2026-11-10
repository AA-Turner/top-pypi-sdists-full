"""`ProbeCommands`: the Lightning callback that takes the run's checkpoint, config and stop commands (agentic W&B C.1),
beside `ProbeLogger`::

    trainer = Trainer(logger=ProbeLogger(project="folding"), callbacks=[ProbeCommands()])

On every rank, at a batch end every rank reaches, rank 0's claimed commands are handed to every rank
(`probe.integrations._commands`): a checkpoint is `trainer.save_checkpoint` on every rank (a collective under
DeepSpeed and FSDP), recorded on rank 0 as the run's checkpoint artifact; a stop sets `trainer.should_stop`, a config
sets the learning rate on this rank's optimizers and schedulers. A kind the script declared
(`run.on(TrainerCommand.EVAL_NOW, fn)`) runs on rank 0. The run is `ProbeLogger`'s, or the script's active run. Why:
sdk/run/commands/DESIGN.md "Every rank"."""

from __future__ import annotations

import os
from typing import Any

try:
    from lightning.pytorch.callbacks import Callback
except ImportError:  # pragma: no cover - exercised only without `lightning`
    try:
        from pytorch_lightning.callbacks import Callback  # type: ignore[no-redef]
    except ImportError as _missing:
        # `name` carries the missing module, so callers tell an absent optional extra from a broken import.
        raise ImportError(
            "probe.integrations.lightning_commands needs PyTorch Lightning, which is not installed. "
            "Install it with Probe's extra: pip install 'probe-research[lightning]'",
            name=getattr(_missing, "name", None) or "lightning",
        ) from _missing

from probe.foundation.safe_warn import safe_warn

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

    def on_train_batch_end(self, trainer: Any, pl_module: Any, outputs: Any, batch: Any, batch_index: int) -> None:
        run = _find_run(trainer)
        for command in self._commands.take(run, trainer.global_step):
            _APPLIERS.get(command["kind"], _run_declared)(self._commands, run, command, trainer)


__all__ = ["CHECKPOINT_FOLDER", "ProbeCommands"]
