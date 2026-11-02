"""Three-view observations for the π0.5 ARX5 multitask policy (bimanual ARX5).

Joints are absolute radians and grippers are opening widths in metres, as the checkpoint
was trained; neither is rescaled. Frames may be any size: the SDK letterboxes each view to
224x224 for the wire, as the model does. No robot drivers or training dependencies are
required.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from numbers import Integral, Real

import numpy as np
from dreamscale_transport import BimanualRobotState, Observation

from dreamscale import wire
from dreamscale.constants import MODEL_PI05_ARX5

ARX5_MODEL_ID = MODEL_PI05_ARX5
# High, left wrist, right wrist: the checkpoint's camera order (its three image slots).
ARX5_CAMERA_KEYS = (
    "observation.images.cam_high",
    "observation.images.cam_left_wrist",
    "observation.images.cam_right_wrist",
)
ARX5_ARM_JOINTS = 6


@dataclass(frozen=True)
class Arx5Observation:
    high_frame: np.ndarray
    left_wrist_frame: np.ndarray
    right_wrist_frame: np.ndarray
    robot_state: BimanualRobotState
    actions_remaining: int = 0
    camera_capture_times_ns: tuple[int, int, int] | None = None

    def __post_init__(self) -> None:
        for name in ("high_frame", "left_wrist_frame", "right_wrist_frame"):
            frame = getattr(self, name)
            if (
                not isinstance(frame, np.ndarray)
                or frame.dtype != np.uint8
                or frame.ndim != 3
                or frame.shape[2] != 3
                or min(frame.shape[:2]) < 16
            ):
                raise ValueError(f"{name} must be an HxWx3 uint8 RGB array")
        if not isinstance(self.robot_state, BimanualRobotState):
            raise TypeError("robot_state must be a BimanualRobotState")
        if (
            isinstance(self.actions_remaining, bool | np.bool_)
            or not isinstance(self.actions_remaining, Integral)
            or self.actions_remaining < 0
        ):
            raise ValueError("actions_remaining must be a nonnegative integer")
        object.__setattr__(self, "actions_remaining", int(self.actions_remaining))
        if self.camera_capture_times_ns is not None:
            times = tuple(self.camera_capture_times_ns)
            if len(times) != 3 or any(
                isinstance(value, bool | np.bool_) or not isinstance(value, Integral) or value <= 0
                for value in times
            ):
                raise ValueError("camera_capture_times_ns must contain three positive integers")
            object.__setattr__(self, "camera_capture_times_ns", tuple(int(v) for v in times))

    @property
    def hold_action(self) -> tuple[float, ...]:
        """Current absolute left-arm block followed by the right-arm block."""
        state = self.robot_state
        return (
            *state.left_joint_positions,
            state.left_gripper,
            *state.right_joint_positions,
            state.right_gripper,
        )

    def to_wire(self, *, session_id: str, observation_id: int, instruction: str) -> Observation:
        return wire.build_three_view_bimanual_observation(
            session_id=session_id,
            observation_id=observation_id,
            camera_keys=ARX5_CAMERA_KEYS,
            frames=(self.high_frame, self.left_wrist_frame, self.right_wrist_frame),
            robot_state=self.robot_state,
            instruction=instruction,
            actions_remaining=self.actions_remaining,
            camera_capture_times_ns=self.camera_capture_times_ns,
        )


def observation(
    *,
    high_frame: np.ndarray,
    left_wrist_frame: np.ndarray,
    right_wrist_frame: np.ndarray,
    left_joint_positions: Sequence[float],
    left_gripper: float,
    right_joint_positions: Sequence[float],
    right_gripper: float,
    actions_remaining: int = 0,
    camera_capture_times_ns: Sequence[int] | None = None,
) -> Arx5Observation:
    """Build an observation in high/left-wrist/right-wrist camera order."""
    for name, value in (("left_gripper", left_gripper), ("right_gripper", right_gripper)):
        if (
            isinstance(value, bool | np.bool_)
            or not isinstance(value, Real)
            or not math.isfinite(float(value))
        ):
            raise ValueError(f"{name} must be a finite gripper width in metres")
    for name, joints in (
        ("left_joint_positions", left_joint_positions),
        ("right_joint_positions", right_joint_positions),
    ):
        if len(joints) != ARX5_ARM_JOINTS:
            raise ValueError(f"{name} must contain {ARX5_ARM_JOINTS} joint positions")
    zeros = [0.0] * ARX5_ARM_JOINTS
    return Arx5Observation(
        high_frame=high_frame,
        left_wrist_frame=left_wrist_frame,
        right_wrist_frame=right_wrist_frame,
        robot_state=BimanualRobotState(
            left_joint_positions=list(left_joint_positions),
            left_joint_velocities=zeros,
            left_gripper=float(left_gripper),
            right_joint_positions=list(right_joint_positions),
            right_joint_velocities=zeros,
            right_gripper=float(right_gripper),
        ),
        actions_remaining=actions_remaining,
        camera_capture_times_ns=(
            None if camera_capture_times_ns is None else tuple(camera_capture_times_ns)
        ),
    )


__all__ = [
    "ARX5_CAMERA_KEYS",
    "ARX5_MODEL_ID",
    "Arx5Observation",
    "observation", "observe",
]


# The earlier name, kept working (the same function).
observe = observation
