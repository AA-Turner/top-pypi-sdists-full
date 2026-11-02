"""Argument-derived recovery requirements recomputed from the retained executable on workers."""

from dataclasses import dataclass, replace

from labqoat._generated.compute_function import ComputeFunction
from labqoat.training.budgets.fit_allowance import FitAllowance
from labqoat.training.recovery.recovery_capability import RecoveryCapability


@dataclass(frozen=True)
class RecoveryBinding:
    """Freeze a workload's concrete allowance and scientific compatibility for one invocation."""

    allowance: FitAllowance
    capability: RecoveryCapability

    def apply(self, declaration: ComputeFunction) -> ComputeFunction:
        """Resolve only recovery fields, requiring a fresh isolated execution and no static override."""
        if declaration.fit_budget_ms is not None or declaration.recovery is not None:
            raise ValueError("Argument-bound recovery cannot override static recovery or fit allowance")
        return replace(
            declaration,
            fit_budget_ms=self.allowance.validate_isolation(declaration.workers),
            recovery=self.capability.capture(declaration.workers, self.allowance),
        )
