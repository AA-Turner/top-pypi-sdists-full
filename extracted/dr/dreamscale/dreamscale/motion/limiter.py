"""Joint-command limits shared by every rig.

Each command is clipped into the intersection of three boxes, per action value:
the hardware range, a velocity box around the previous command (how far one tick
may move), and a tracking envelope around the measured pose (how far a command may
lead an arm that has stopped following, so a blocked joint cannot wind up).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


class LimitConflict(ValueError):
    """Measured motion leaves no command inside every box."""


def step_box(reference, allowance):
    """Closed bounds whose represented differences do not exceed allowance."""
    low, high = reference - allowance, reference + allowance
    # Addition then subtraction can round just outside a strict step cap.
    # Move only those endpoints one float inward, rather than relax the cap.
    low = np.where(reference - low > allowance, np.nextafter(low, reference), low)
    high = np.where(high - reference > allowance, np.nextafter(high, reference), high)
    return low, high


@dataclass(frozen=True)
class MotionLimiter:
    """Bounds for one arm's command vector, in the rig's own units.

    tracking holds the largest lead from the measured pose per value; inf leaves a
    value untracked (a gripper closing on an object is supposed to lead).
    """

    lower: np.ndarray
    upper: np.ndarray
    tracking: np.ndarray | None = None

    def tracking_applies(self, measured):
        # A tracking envelope centered outside the command range can have no legal
        # target. For those values keep angle/velocity caps, but do not turn an
        # encoder range excursion into an angle-only shutdown via the step gate.
        if self.tracking is None:
            return np.zeros(len(self.lower), dtype=bool)
        return np.isfinite(self.tracking) & (measured >= self.lower) & (measured <= self.upper)

    def project(self, target, *, previous, measured, allowance=None):
        """Clip target into every box; allowance is the per-value step this tick."""
        low, high = np.array(self.lower, dtype=float), np.array(self.upper, dtype=float)
        if allowance is not None:
            speed_low, speed_high = step_box(np.asarray(previous, dtype=float), allowance)
            low, high = np.maximum(low, speed_low), np.minimum(high, speed_high)
        applies = self.tracking_applies(measured)
        if applies.any():
            track_low, track_high = step_box(
                np.asarray(measured, dtype=float), np.where(applies, self.tracking, 0.0),
            )
            low = np.where(applies, np.maximum(low, track_low), low)
            high = np.where(applies, np.minimum(high, track_high), high)
        if (low > high).any():
            raise LimitConflict(
                "measured motion leaves no command satisfying both position/tracking "
                "and velocity bounds"
            )
        # Value-wise saturation: outward requests at a boundary are no-ops; the
        # other values and subsequent inward commands remain usable.
        return np.clip(np.asarray(target, dtype=float), low, high)
