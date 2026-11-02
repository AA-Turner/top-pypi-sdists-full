"""Execution budgets and receipts for Cartesian-to-joint conversion.

These contracts describe approximation of a requested tool pose. They never
change a robot's joint limits, calibration or motor control.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import Literal


@dataclass(frozen=True)
class PoseApproximation:
    """Optional error caps at the controlled tool; None disables that pose cap.

    Both caps set to None admit any finite nonnegative FK error. The robot
    adapter still owns strict joint-bound and candidate-validity checks.
    """

    max_position_error_m: float | None = 0.010
    max_rotation_error_rad: float | None = 0.05

    def __post_init__(self):
        for name in ("max_position_error_m", "max_rotation_error_rad"):
            value = getattr(self, name)
            if value is None:
                continue
            if (
                isinstance(value, bool) or not isinstance(value, Real)
                or not isfinite(value) or value <= 0
            ):
                raise ValueError(
                    "Pose approximation budgets must be positive finite numbers or None."
                )
            object.__setattr__(self, name, float(value))

    def accepts(self, position_error_m: float, rotation_error_rad: float) -> bool:
        return (
            isfinite(position_error_m) and isfinite(rotation_error_rad)
            and position_error_m >= 0 and rotation_error_rad >= 0
            and (self.max_position_error_m is None
                 or position_error_m <= self.max_position_error_m)
            and (self.max_rotation_error_rad is None
                 or rotation_error_rad <= self.max_rotation_error_rad)
        )

    @property
    def mode(self) -> Literal["bounded", "joint_bounds_only"]:
        return (
            "joint_bounds_only"
            if self.max_position_error_m is None and self.max_rotation_error_rad is None
            else "bounded"
        )


@dataclass(frozen=True)
class PoseConversion:
    """One attempted pose; admission does not mean physical execution."""

    action_index: int  # one-based within the executable prediction prefix
    arm: str
    requested_pose: tuple[tuple[float, ...], ...]
    achieved_pose: tuple[tuple[float, ...], ...]
    joints: tuple[float, ...]
    native_converged: bool
    position_error_m: float
    rotation_error_rad: float
    status: Literal["exact", "approximate", "rejected"]


@dataclass(frozen=True)
class CartesianConversion:
    """A whole chunk is admitted atomically, including any approximated poses."""

    poses: tuple[PoseConversion, ...]
    accepted: bool
    error: str | None = None
    observation_id: int | None = None
    chunk_id: int | None = None

    @property
    def adjustment_count(self) -> int:
        return sum(pose.status == "approximate" for pose in self.poses)
