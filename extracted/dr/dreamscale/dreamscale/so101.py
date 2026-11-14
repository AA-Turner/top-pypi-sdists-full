from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from dreamscale_transport import Observation

from dreamscale import wire
from dreamscale.observation_checks import (
    check_actions_remaining,
    check_capture_time_ns,
    check_frame,
    check_values,
)

SO101_JOINT_POSITION_SIZE = 6
# Joint order and units every SO-101 model shares.
SO101_JOINT_POSITIONS = (
    "shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll in degrees, "
    "then the gripper in its native 0-100 units"
)


@dataclass(frozen=True)
class So101Observation:
    side_frame: np.ndarray
    wrist_frame: np.ndarray | None
    joint_positions: tuple[float, ...]
    actions_remaining: int = 0
    # time.time_ns() when the frames and joints were read; None: when the request is built.
    capture_time_ns: int | None = None
    gripper_range: tuple[float, float] | None = None

    @property
    def hold_action(self) -> tuple[float, ...]:
        """The measured pose: what holding still commands."""
        return self.joint_positions

    @property
    def frame(self) -> np.ndarray:
        """Legacy alias for the side camera frame."""
        return self.side_frame

    def to_wire(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
    ) -> Observation:
        return wire.build_so101_observation(
            session_id=session_id,
            observation_id=observation_id,
            joint_positions=list(self.joint_positions),
            side_frame=self.side_frame,
            wrist_frame=self.wrist_frame,
            instruction=instruction,
            actions_remaining=self.actions_remaining,
            views=1 if self.wrist_frame is None else 2,
            gripper_range=self.gripper_range,
        )


def observation(
    *,
    side_frame: np.ndarray | None = None,
    wrist_frame: np.ndarray | None = None,
    frame: np.ndarray | None = None,
    joint_positions: Sequence[float],
    actions_remaining: int = 0,
    capture_time_ns: int | None = None,
    views: int = 2,
    gripper_range: tuple[float, float] | None = None,
) -> So101Observation:
    """One SO-101 observation: the side and wrist cameras plus the measured joints.

    ``views=1`` explicitly omits the wrist (for models supporting a side-only setup).
    ``gripper_range=(closed, open)`` gives measured readings in native 0–100 units,
    for a model that normalizes gripper closure. Omit it to use that model's defaults.
    The connected policy prepares images (resize, encoding) at send time.
    """
    if side_frame is None:
        side_frame = frame
    if side_frame is None:
        raise TypeError("side_frame is required")
    if isinstance(views, bool) or views not in (1, 2):
        raise ValueError("views must be 1 (side) or 2 (side and wrist)")
    if views == 1 and wrist_frame is not None:
        raise ValueError("views=1 omits the wrist; do not pass wrist_frame")
    if wrist_frame is None and views == 2:
        wrist_frame = frame if frame is not None else side_frame
    if gripper_range is not None:
        from dreamscale_transport.praxis import validate_so101_grip_range

        gripper_range = validate_so101_grip_range(gripper_range)
    return So101Observation(
        side_frame=check_frame("side_frame", side_frame),
        wrist_frame=check_frame("wrist_frame", wrist_frame) if views == 2 else None,
        joint_positions=_validate_joint_positions(joint_positions),
        actions_remaining=check_actions_remaining(actions_remaining),
        capture_time_ns=check_capture_time_ns(capture_time_ns),
        gripper_range=gripper_range,
    )


def _validate_joint_positions(joint_positions: Sequence[float]) -> tuple[float, ...]:
    return check_values(
        "joint_positions", joint_positions, SO101_JOINT_POSITION_SIZE, SO101_JOINT_POSITIONS
    )


# The earlier name, kept working (the same function).
observe = observation
