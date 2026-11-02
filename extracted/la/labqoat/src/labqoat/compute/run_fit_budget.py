"""Invocation-owned entry to cumulative scientific fit enforcement."""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from labqoat.training.budgets.fit_budget_client import FitBudgetClient
from labqoat.training.budgets.fit_session import FitSession
from labqoat.training.budgets.fit_supervisor import FitSupervisor
from labqoat.worker.worker_api import WorkerApi
from labqoat.compute.run_recovery import RunRecovery
from labqoat._generated.fit_budget_history import FitBudgetHistory


@dataclass(frozen=True)
class RunFitBudget:
    """Scope fit wall time explicitly, excluding restoration, queueing and final evaluation."""

    api: WorkerApi
    run_id: str
    attempt_id: str
    fence: int
    recovery: RunRecovery | None = None

    def status(self) -> FitBudgetHistory:
        """Read conservative remaining allowance; this observation never grants permission to fit."""
        budget = FitBudgetHistory.from_dict(self.api.json("GET", "/api/v1/worker/fit/budget"))
        if budget.run_id != self.run_id:
            raise ValueError("Fit budget belongs to a different run")
        return budget

    @contextmanager
    def maintained(self) -> Iterator[FitSession]:
        """Use a separate bounded transport and stop fit before closing its scientific usage interval."""
        if self.recovery is not None:
            self.recovery.require_fit()
        api = self.api.fit_api()
        try:
            client = FitBudgetClient(api, self.run_id, self.attempt_id, self.fence)
            with FitSession(client, FitSupervisor()).maintained() as session:
                yield session
        finally:
            api.close()
