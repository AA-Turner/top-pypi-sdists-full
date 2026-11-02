"""Explicit Trainer.fit integration with immutable recovery selection and supervised cumulative fit."""

from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import lightning
from lightning.pytorch import LightningDataModule, LightningModule, Trainer
from lightning.pytorch.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS

from labqoat.run_context import RunContext
from labqoat.training.lightning.lightning_fit_gate import LightningFitGate
from labqoat.training.lightning.lightning_callbacks import LightningCallbacks
from labqoat.training.lightning.lightning_restore_adapter import LightningRestoreAdapter


@dataclass(frozen=True)
class LightningFit:
    """Preserve authored Trainer configuration and require a workload-owned state-verifying adapter."""

    context: RunContext
    adapter: LightningRestoreAdapter

    def fit(
        self,
        trainer: Trainer,
        model: LightningModule,
        *,
        train_dataloaders: TRAIN_DATALOADERS | None = None,
        val_dataloaders: EVAL_DATALOADERS | None = None,
        datamodule: LightningDataModule | None = None,
        ckpt_path: Path | None = None,
    ) -> None:
        """Select the exact checkpoint before fit and clean up supervision on every return or exception."""
        self._validate(trainer)
        selected = self._checkpoint(ckpt_path)
        callbacks = cast(LightningCallbacks, trainer).callbacks
        with ExitStack() as lifetime:
            gate = LightningFitGate(self.context, self.adapter, lifetime)
            callbacks.insert(0, gate)
            lifetime.callback(self._detach, trainer, gate)
            trainer.fit(
                model,
                train_dataloaders=train_dataloaders,
                val_dataloaders=val_dataloaders,
                datamodule=datamodule,
                ckpt_path=selected,
                weights_only=False,
            )
            self.context.require_restored()

    @staticmethod
    def _detach(trainer: Trainer, gate: LightningFitGate) -> None:
        """Detach from the current list after Lightning merges model-owned callbacks."""
        callbacks = cast(LightningCallbacks, trainer).callbacks
        if gate in callbacks:
            callbacks.remove(gate)

    def _validate(self, trainer: Trainer) -> None:
        """Bound restoration to the verified framework ordering and isolated single-worker topology."""
        if lightning.__version__ != "2.6.6":
            raise ValueError("Lightning recovery requires certified runtime version 2.6.6")
        if trainer.world_size != 1 or trainer.num_sanity_val_steps != 0:
            raise ValueError("Lightning recovery requires one worker and num_sanity_val_steps=0")
        if any(isinstance(callback, LightningFitGate) for callback in cast(LightningCallbacks, trainer).callbacks):
            raise ValueError("Lightning Trainer already has a fit gate")

    def _checkpoint(self, explicit: Path | None) -> Path | None:
        """Reject explicit checkpoint drift and finalization plans before entering Trainer.fit."""
        recovery = self.context.recovery
        if recovery is None:
            return explicit
        if recovery.envelope.document["mode"] != "resume":
            raise ValueError("Finalization-only recovery cannot enter Trainer.fit")
        selected = self.adapter.prepare(recovery.prepare(self.adapter)).resolve(strict=True)
        if not selected.is_file():
            raise ValueError("Lightning adapter must prepare a local checkpoint file")
        if explicit is not None and explicit.resolve(strict=True) != selected:
            raise ValueError("Explicit checkpoint conflicts with accepted recovery plan")
        return selected
