"""A scoped Lightning callback acknowledges actual restoration before opening scientific fit time."""

from contextlib import ExitStack

from lightning.pytorch import Callback, LightningModule, Trainer

from labqoat.run_context import RunContext
from labqoat.training.budgets.fit_session import FitSession
from labqoat.training.lightning.lightning_restore_adapter import LightningRestoreAdapter


class LightningFitGate(Callback):
    """Use Lightning's post-optimizer-restore boundary, never the earlier on_fit_start notification."""

    def __init__(self, context: RunContext, adapter: LightningRestoreAdapter, lifetime: ExitStack) -> None:
        """Keep grant supervision owned by the Trainer.fit caller even when framework teardown fails."""
        self.context = context
        self.adapter = adapter
        self.lifetime = lifetime
        self.session: FitSession | None = None

    def on_train_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        """Lightning has restored optimizer, scheduler and loop state before this callback executes."""
        if self.session is not None:
            raise ValueError("Lightning fit gate cannot be entered twice")
        if self.context.recovery is not None:
            self.context.recovery.restore(self.adapter)
        self.session = self.lifetime.enter_context(self.context.fit_budget.maintained())

    def on_train_batch_start(self, trainer: Trainer, pl_module: LightningModule, batch: object, batch_idx: int) -> None:
        """Check renewal failures before each batch while independent supervision enforces physical expiry."""
        if self.session is None:
            raise ValueError("Lightning attempted training before acknowledged restoration and fit grant")
        self.session.check()
