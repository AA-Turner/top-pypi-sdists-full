"""Any robot: named cameras and one state vector, for deployments with their own
embodiment (``dreamscale.connect("perceptron-isaac05", deployment="ckpt_…")``) and for
models served from a stock LeRobot checkpoint.

The deployment or checkpoint names the cameras (in order) and the state width; values are
sent in the units the checkpoint was trained on, and actions come back the same way::

    observation = dreamscale.robot.observation(
        cameras={"exterior": exterior_rgb, "wrist": wrist_rgb},
        state=joint_positions_and_gripper,
    )
"""

from __future__ import annotations

import math
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
from dreamscale_transport import Observation, ObservationFrame, VectorRobotState

from dreamscale import wire
from dreamscale.observation_checks import check_capture_time_ns

MAX_CAMERAS = 4


@dataclass(frozen=True)
class RobotObservation:
    cameras: tuple[tuple[str, np.ndarray], ...]
    state: tuple[float, ...]
    actions_remaining: int = 0
    # time.time_ns() when the frames and state were read; None: when the request is built.
    capture_time_ns: int | None = None

    @property
    def joint_positions(self) -> tuple[float, ...]:
        """The state vector (the run loop's hold position for absolute joint actions)."""
        return self.state

    def to_wire(self, *, session_id: str, observation_id: int, instruction: str) -> Observation:
        now = time.time_ns()
        encoded = [wire._camera_frame(key, frame) for key, frame in self.cameras]
        return Observation(
            frame=ObservationFrame(
                session_id=session_id,
                observation_id=observation_id,
                capture_time_ns=now,
                send_time_ns=now,
                cameras=[camera for camera, _ in encoded],
                robot_state=VectorRobotState(state=list(self.state)),
                actions_remaining=self.actions_remaining,
                instruction=instruction,
            ),
            camera_payloads={camera.camera_id: payload for camera, payload in encoded},
        )


def observation(
    *,
    cameras: Mapping[str, np.ndarray],
    state: Sequence[float],
    actions_remaining: int = 0,
    capture_time_ns: int | None = None,
) -> RobotObservation:
    """One observation: RGB uint8 frames keyed by the deployment's camera keys, in order."""
    if not 1 <= len(cameras) <= MAX_CAMERAS:
        raise ValueError(f"cameras must name 1 to {MAX_CAMERAS} frames")
    frames = []
    for key, frame in cameras.items():
        array = np.asarray(frame)
        if array.ndim != 3 or array.shape[2] != 3 or array.dtype != np.uint8:
            raise ValueError(f"camera {key!r} must be an RGB uint8 frame (H, W, 3)")
        frames.append((str(key), array))
    values = tuple(float(v) for v in state)
    if not values or any(not math.isfinite(v) for v in values):
        raise ValueError("state must be a non-empty vector of finite numbers")
    if isinstance(actions_remaining, bool) or not isinstance(actions_remaining, int) or (
        actions_remaining < 0
    ):
        raise ValueError("actions_remaining must be a nonnegative integer")
    return RobotObservation(
        tuple(frames), values, actions_remaining, check_capture_time_ns(capture_time_ns)
    )


# The earlier name, kept working (the same function).
observe = observation
