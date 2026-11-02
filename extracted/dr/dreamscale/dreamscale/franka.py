"""Typed Franka / DROID observation surface for DROID-trained models (experimental).

Franka support is experimental: its names and behaviour may change between releases.
See https://docs.dreamscalelabs.com/robots/franka.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from dreamscale_transport import Observation

from dreamscale import wire

FRANKA_JOINT_POSITION_SIZE = 7


@dataclass(frozen=True)
class FrankaObservation:
    exterior_frame: np.ndarray
    wrist_frame: np.ndarray
    joint_positions: tuple[float, ...]
    gripper: float
    second_exterior_frame: np.ndarray | None = None
    actions_remaining: int = 0
    chunk_size: int | None = None

    # Its frames under the Franka's camera roles, as recorders read them.
    @property
    def exterior_1_frame(self) -> np.ndarray:
        return self.exterior_frame

    @property
    def exterior_2_frame(self) -> np.ndarray | None:
        return self.second_exterior_frame

    @property
    def hold_action(self) -> tuple[float, ...]:
        """Current absolute 7-joint target plus unit-interval gripper state."""
        return (*self.joint_positions, self.gripper)

    def to_wire(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
    ) -> Observation:
        return wire.build_franka_observation(
            session_id=session_id,
            observation_id=observation_id,
            exterior_frame=self.exterior_frame,
            second_exterior_frame=self.second_exterior_frame,
            wrist_frame=self.wrist_frame,
            joint_positions=list(self.joint_positions),
            gripper=self.gripper,
            instruction=instruction,
            actions_remaining=self.actions_remaining,
            chunk_size=self.chunk_size,
        )


def observation(
    *,
    exterior_frame: np.ndarray,
    wrist_frame: np.ndarray,
    joint_positions: Sequence[float],
    gripper: float,
    second_exterior_frame: np.ndarray | None = None,
    actions_remaining: int = 0,
    chunk_size: int | None = None,
) -> FrankaObservation:
    """One Franka / DROID observation (experimental): two exterior views at most, the
    wrist view, seven joint positions in radians and the gripper from 0 open to 1 closed."""
    return FrankaObservation(
        exterior_frame=_validate_frame(exterior_frame, "exterior_frame"),
        second_exterior_frame=(
            None
            if second_exterior_frame is None
            else _validate_frame(second_exterior_frame, "second_exterior_frame")
        ),
        wrist_frame=_validate_frame(wrist_frame, "wrist_frame"),
        joint_positions=_validate_joint_positions(joint_positions),
        gripper=_validate_gripper(gripper),
        actions_remaining=_validate_actions_remaining(actions_remaining),
        chunk_size=chunk_size,
    )


def _validate_frame(frame: np.ndarray, name: str) -> np.ndarray:
    if not isinstance(frame, np.ndarray):
        raise TypeError(f"{name} must be a numpy array")
    if frame.dtype != np.uint8 or frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError(f"{name} must be an HxWx3 uint8 RGB array")
    if frame.shape[0] <= 0 or frame.shape[1] <= 0:
        raise ValueError(f"{name} must have nonzero width and height")
    return frame


def _validate_joint_positions(values: Sequence[float]) -> tuple[float, ...]:
    raw = tuple(values)
    if any(isinstance(value, (bool, np.bool_)) for value in raw):
        raise TypeError("joint_positions must contain numeric values, not booleans")
    joints = tuple(float(value) for value in raw)
    if len(joints) != FRANKA_JOINT_POSITION_SIZE or any(
        not math.isfinite(value) for value in joints
    ):
        raise ValueError("joint_positions must contain exactly 7 finite values")
    return joints


def _validate_gripper(value: float) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise TypeError("gripper must be numeric, not a boolean")
    gripper = float(value)
    if not math.isfinite(gripper) or not 0.0 <= gripper <= 1.0:
        raise ValueError("gripper must be a finite value between 0 and 1")
    return gripper


def _validate_actions_remaining(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("actions_remaining must be a nonnegative integer")
    if value < 0:
        raise ValueError("actions_remaining must be a nonnegative integer")
    return value


# The earlier name, kept working (the same function).
observe = observation
