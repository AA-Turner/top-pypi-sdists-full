"""Strict DreamZero-YAM observations for the native 30 Hz control loop."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from dreamscale import wire
from dreamscale.dreamzero import (
    DreamZeroLoopProfile,
    SamplingMode,
    resize_with_pad,
    resolve_dreamzero_sampling,
)

DREAMZERO_YAM_IMAGE_HEIGHT = 360
DREAMZERO_YAM_IMAGE_WIDTH = 640


@dataclass(frozen=True)
class DreamZeroYamObservation:
    top_frame: np.ndarray
    left_frame: np.ndarray
    right_frame: np.ndarray
    # Unix nanoseconds, matching wire timestamps and measured startup checks.
    camera_capture_times_ns: tuple[int, int, int]
    left_joint_positions: tuple[float, ...]
    left_gripper: float
    right_joint_positions: tuple[float, ...]
    right_gripper: float

    @property
    def hold_action(self) -> tuple[float, ...]:
        return (
            *self.left_joint_positions,
            self.left_gripper,
            *self.right_joint_positions,
            self.right_gripper,
        )

    def to_wire(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
    ):
        return self.to_wire_for_step(
            session_id=session_id,
            observation_id=observation_id,
            instruction=instruction,
            source_action_step=-1,
            next_action_step=0,
            control_tick=0,
            replan_epoch=0,
            cache_generation=0,
            sampling="async_latest",
        )

    def to_wire_for_step(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
        source_action_step: int,
        next_action_step: int,
        control_tick: int,
        replan_epoch: int,
        cache_generation: int,
        sampling: SamplingMode,
    ):
        sampling = resolve_dreamzero_sampling("dreamzero-yam", sampling)
        return wire.build_dreamzero_yam_observation(
            session_id=session_id,
            observation_id=observation_id,
            top_frame=self.top_frame,
            left_frame=self.left_frame,
            right_frame=self.right_frame,
            camera_capture_times_ns=self.camera_capture_times_ns,
            left_joint_positions=list(self.left_joint_positions),
            left_gripper=self.left_gripper,
            right_joint_positions=list(self.right_joint_positions),
            right_gripper=self.right_gripper,
            instruction=instruction,
            source_action_step=source_action_step,
            next_action_step=next_action_step,
            control_tick=control_tick,
            replan_epoch=replan_epoch,
            cache_generation=cache_generation,
            sampling=sampling,
        )


DREAMZERO_YAM_LOOP_PROFILE = DreamZeroLoopProfile(
    model_id="dreamzero-yam",
    observation_type=DreamZeroYamObservation,
    action_dim=14,
    gripper_indices=(6, 13),
    threshold_grippers=False,
    control_hz=30.0,
)


def observation(
    *,
    top_frame: np.ndarray,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    camera_capture_times_ns: Sequence[int],
    left_joint_positions: Sequence[float],
    left_gripper: float,
    right_joint_positions: Sequence[float],
    right_gripper: float,
) -> DreamZeroYamObservation:
    timestamps = tuple(camera_capture_times_ns)
    if len(timestamps) != 3 or any(
        isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in timestamps
    ):
        raise ValueError("camera_capture_times_ns must contain exactly 3 nonnegative integers")
    return DreamZeroYamObservation(
        top_frame=resize_with_pad(
            top_frame,
            height=DREAMZERO_YAM_IMAGE_HEIGHT,
            width=DREAMZERO_YAM_IMAGE_WIDTH,
        ),
        left_frame=resize_with_pad(
            left_frame,
            height=DREAMZERO_YAM_IMAGE_HEIGHT,
            width=DREAMZERO_YAM_IMAGE_WIDTH,
        ),
        right_frame=resize_with_pad(
            right_frame,
            height=DREAMZERO_YAM_IMAGE_HEIGHT,
            width=DREAMZERO_YAM_IMAGE_WIDTH,
        ),
        camera_capture_times_ns=(
            int(timestamps[0]),
            int(timestamps[1]),
            int(timestamps[2]),
        ),
        left_joint_positions=_arm(left_joint_positions, "left_joint_positions"),
        left_gripper=_gripper(left_gripper, "left_gripper"),
        right_joint_positions=_arm(right_joint_positions, "right_joint_positions"),
        right_gripper=_gripper(right_gripper, "right_gripper"),
    )


def _arm(values: Sequence[float], name: str) -> tuple[float, ...]:
    raw = tuple(values)
    if any(isinstance(value, (bool, np.bool_)) for value in raw):
        raise TypeError(f"{name} must contain numeric values, not booleans")
    joints = tuple(float(value) for value in raw)
    if len(joints) != 6 or any(not math.isfinite(value) for value in joints):
        raise ValueError(f"{name} must contain exactly 6 finite values")
    return joints


def _gripper(value: float, name: str) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise TypeError(f"{name} must be numeric, not a boolean")
    gripper = float(value)
    if not math.isfinite(gripper):
        raise ValueError(f"{name} must be a finite value")
    return gripper


__all__ = [
    "DREAMZERO_YAM_IMAGE_HEIGHT",
    "DREAMZERO_YAM_IMAGE_WIDTH",
    "DreamZeroYamObservation",
    "observation", "observe",
]


# The earlier name, kept working (the same function).
observe = observation
