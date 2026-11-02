"""One active interval's bounded monotonic usage cursor."""

from dataclasses import dataclass

from labqoat.training.budgets.fit_grant import FitGrant
from labqoat.training.budgets.fit_report import FitReport


@dataclass
class FitInterval:
    """Attribute physical fit wall time once across consecutive server reservations."""

    grant: FitGrant
    started_at: float
    sequence: int = 0

    def report(self, now: float, *, stopped: bool) -> FitReport:
        """Freeze a usage report before transport replay; advance only the local sequence identity."""
        elapsed = min(self.grant.duration_ms, max(0, int((now - self.started_at) * 1000)))
        report = FitReport(self.sequence, elapsed, stopped)
        self.sequence += 1
        return report
