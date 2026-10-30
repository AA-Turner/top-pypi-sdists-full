# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""One `--read-timeout` for a comparison read, from the command's start to its report.

The workflow's READ step hands the CLI a single budget inside its own
`timeout-minutes`. In comparison mode the control and the target read one
after the other, so giving each side the whole budget lets two long reads run
for twice it, and GitHub kills the step before anything is reported. The
command owns the budget instead, from the moment it starts:

- A reserve for the comparison and the report comes off the top: ten minutes,
  or a tenth of the budget when that is less, so it is never negative and
  never most of a small budget.
- The control gets at most 60% of the read time left when it starts. It is
  the live read, and usually the slow one.
- The target gets all the read time left when it starts. It usually replays
  the control's recorded HTTP traffic and is fast. With nothing left it does
  not start, and is reported as stopped at its deadline. The control does
  the same in the unlikely case that setup used up the read time.

A single-version read keeps the same reserve and gets all the read time left
when it starts, so its report is written inside the step as well.

The work around each read (setup before the control, parsing each side's
output after it) is charged to the clock as it happens, which is why each side
takes its share when it starts rather than up front.

The workflow's 170-minute budget keeps 10 minutes back and leaves 160 for
reading:

- A live control gets at most 96 minutes: 60% of the 160, less 60% of
  whatever setup took. A control read that needs longer is stopped at its
  deadline, and the run ends INCOMPLETE. The cap is deliberate: it is what
  leaves the target time to read at all.
- The target gets what is left of the 160 when it starts. That is at most 64
  minutes when the control reads to its deadline, less 40% of the setup time
  and the time spent parsing the control's output. When the control finishes
  sooner, the target gets the minutes the control did not use as well.

Raising `--read-timeout` raises the whole budget, and both shares with it. In
CI the budget is the READ step's `timeout-minutes` less ten minutes, so a
longer control read needs both raised.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic

REPORT_RESERVE_SECONDS = 600
"""The most a budget keeps back for the comparison and the report."""

REPORT_RESERVE_DIVISOR = 10
"""A small budget keeps back this fraction of itself instead: 1/10."""

CONTROL_READ_PERCENT = 60
"""The control's share of the read time left when it starts, in percent."""


def report_reserve_s(budget_s: int) -> int:
    """Seconds kept back from the reads for the comparison and the report."""
    return max(0, min(REPORT_RESERVE_SECONDS, budget_s // REPORT_RESERVE_DIVISOR))


@dataclass(frozen=True)
class ReadBudget:
    """The seconds a comparison read has left, measured from the command's start."""

    budget_s: int
    started: float

    @classmethod
    def start(cls, budget_s: int) -> ReadBudget:
        return cls(budget_s=budget_s, started=monotonic())

    @property
    def reserve_s(self) -> int:
        return report_reserve_s(self.budget_s)

    def read_time_left_s(self) -> int:
        """Whole seconds left to read in: the budget less the reserve and time spent."""
        spent = monotonic() - self.started
        return max(0, int(self.budget_s - self.reserve_s - spent))

    def control_share_s(self) -> int:
        """The control's deadline, taken when it starts."""
        return self.read_time_left_s() * CONTROL_READ_PERCENT // 100

    def target_share_s(self) -> int:
        """The target's deadline, taken when it starts; 0 means it does not run."""
        return self.read_time_left_s()
