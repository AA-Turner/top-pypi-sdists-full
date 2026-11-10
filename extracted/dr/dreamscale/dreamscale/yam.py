"""Typed BimanualYAM observation surface for MolmoAct2."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from dreamscale_transport import BimanualEndEffectorState, Observation

from dreamscale import wire
from dreamscale.errors import observation_error
from dreamscale.observation_checks import check_capture_time_ns, check_frame, check_values

YAM_ARM_JOINT_POSITION_SIZE = 6
YAM_ARM_JOINTS = "the arm's six joint angles in radians, base to wrist"
YAM_ARM_VELOCITIES = "the arm's six joint velocities in radians per second"


@dataclass(frozen=True)
class YamObservation:
    top_frame: np.ndarray
    left_frame: np.ndarray
    right_frame: np.ndarray
    left_joint_positions: tuple[float, ...]
    left_joint_velocities: tuple[float, ...]
    left_gripper: float
    right_joint_positions: tuple[float, ...]
    right_joint_velocities: tuple[float, ...]
    right_gripper: float
    actions_remaining: int = 0
    # Unix nanoseconds, matching ObservationFrame/CameraFrame wire timestamps.
    camera_capture_times_ns: tuple[int, int, int] | None = None
    # One capture time for the whole observation (time.time_ns()); per-camera times say more.
    capture_time_ns: int | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "camera_capture_times_ns",
            _validate_camera_capture_times(self.camera_capture_times_ns),
        )
        _one_capture_time(self.camera_capture_times_ns, self.capture_time_ns)

    @property
    def hold_action(self) -> tuple[float, ...]:
        """Current absolute left-arm block followed by the right-arm block."""
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
    ) -> Observation:
        return wire.build_yam_observation(
            session_id=session_id,
            observation_id=observation_id,
            top_frame=self.top_frame,
            left_frame=self.left_frame,
            right_frame=self.right_frame,
            left_joint_positions=list(self.left_joint_positions),
            left_joint_velocities=list(self.left_joint_velocities),
            left_gripper=self.left_gripper,
            right_joint_positions=list(self.right_joint_positions),
            right_joint_velocities=list(self.right_joint_velocities),
            right_gripper=self.right_gripper,
            instruction=instruction,
            actions_remaining=self.actions_remaining,
            camera_capture_times_ns=self.camera_capture_times_ns,
        )


@dataclass(frozen=True)
class YamEndEffectorObservation:
    """Calibrated pose observation, with checkpoint gripper coordinates."""

    top_frame: np.ndarray
    left_frame: np.ndarray
    right_frame: np.ndarray
    robot_state: BimanualEndEffectorState
    actions_remaining: int = 0
    camera_capture_times_ns: tuple[int, int, int] | None = None

    def __post_init__(self):
        for name in ("top_frame", "left_frame", "right_frame"):
            _validate_frame(getattr(self, name), name)
        _validate_actions_remaining(self.actions_remaining)
        object.__setattr__(self, "camera_capture_times_ns",
                           _validate_camera_capture_times(self.camera_capture_times_ns))

    @property
    def hold_action(self) -> tuple[float, ...]:
        return self.robot_state.model_state()

    def to_wire(self, *, session_id: str, observation_id: int, instruction: str) -> Observation:
        return wire.build_yam_end_effector_observation(
            session_id=session_id, observation_id=observation_id, instruction=instruction,
            top_frame=self.top_frame, left_frame=self.left_frame, right_frame=self.right_frame,
            robot_state=self.robot_state, actions_remaining=self.actions_remaining,
            camera_capture_times_ns=self.camera_capture_times_ns,
        )


def observation(
    *,
    top_frame: np.ndarray,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    left_joint_positions: Sequence[float],
    left_gripper: float,
    right_joint_positions: Sequence[float],
    right_gripper: float,
    left_joint_velocities: Sequence[float] | None = None,
    right_joint_velocities: Sequence[float] | None = None,
    actions_remaining: int = 0,
    camera_capture_times_ns: Sequence[int] | None = None,
    capture_time_ns: int | None = None,
) -> YamObservation:
    return YamObservation(
        top_frame=_validate_frame(top_frame, "top_frame"),
        left_frame=_validate_frame(left_frame, "left_frame"),
        right_frame=_validate_frame(right_frame, "right_frame"),
        left_joint_positions=_validate_joint_values(
            left_joint_positions,
            "left_joint_positions",
        ),
        left_joint_velocities=_validate_joint_values(
            [0.0] * YAM_ARM_JOINT_POSITION_SIZE
            if left_joint_velocities is None
            else left_joint_velocities,
            "left_joint_velocities",
        ),
        left_gripper=_validate_gripper(left_gripper, "left_gripper"),
        right_joint_positions=_validate_joint_values(
            right_joint_positions,
            "right_joint_positions",
        ),
        right_joint_velocities=_validate_joint_values(
            [0.0] * YAM_ARM_JOINT_POSITION_SIZE
            if right_joint_velocities is None
            else right_joint_velocities,
            "right_joint_velocities",
        ),
        right_gripper=_validate_gripper(right_gripper, "right_gripper"),
        actions_remaining=_validate_actions_remaining(actions_remaining),
        camera_capture_times_ns=_validate_camera_capture_times(camera_capture_times_ns),
        capture_time_ns=check_capture_time_ns(capture_time_ns),
    )


def _one_capture_time(camera_times: tuple[int, ...] | None, capture_time_ns: int | None) -> None:
    if camera_times is not None and capture_time_ns is not None:
        raise observation_error(
            "capture_time_ns", "together with camera_capture_times_ns",
            "one of them: per-camera capture times, or one capture time for the observation",
        )


def _validate_frame(frame: np.ndarray, name: str) -> np.ndarray:
    return check_frame(name, frame)


def _validate_joint_values(values: Sequence[float], name: str) -> tuple[float, ...]:
    expected = YAM_ARM_VELOCITIES if name.endswith("velocities") else YAM_ARM_JOINTS
    return check_values(name, values, YAM_ARM_JOINT_POSITION_SIZE, expected)


def _validate_gripper(value: float, name: str) -> float:
    expected = "one number from 0 (closed) to 1 (open)"
    if isinstance(value, (bool, np.bool_)):
        raise observation_error(name, "a boolean", expected)
    try:
        gripper = float(value)
    except (TypeError, ValueError, OverflowError):
        raise observation_error(name, type(value).__name__, expected) from None
    if not math.isfinite(gripper) or not 0.0 <= gripper <= 1.0:
        raise observation_error(name, f"{gripper!r}", expected)
    return gripper


def _validate_actions_remaining(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TypeError("actions_remaining must be a nonnegative integer")
    return value


def _validate_camera_capture_times(
    values: Sequence[int] | None,
) -> tuple[int, int, int] | None:
    if values is None:
        return None
    timestamps = tuple(values)
    if len(timestamps) != 3 or any(
        isinstance(value, (bool, np.bool_)) or not isinstance(value, int) or value <= 0
        for value in timestamps
    ):
        raise ValueError("camera_capture_times_ns must contain exactly 3 positive integers")
    return (timestamps[0], timestamps[1], timestamps[2])


__all__ = [
    "YAM_ARM_JOINT_POSITION_SIZE", "YamObservation", "YamEndEffectorObservation", "observation",
    "observe",
]


# The earlier name, kept working (the same function).
observe = observation
