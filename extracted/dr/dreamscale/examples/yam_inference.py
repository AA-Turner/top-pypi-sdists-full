"""Minimal BimanualYAM inference example using the public Dreamscale SDK."""

from __future__ import annotations

import time

import numpy as np

import dreamscale


def main() -> None:
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    capture_time_ns = time.time_ns()
    observation = dreamscale.yam.observation(
        top_frame=frame,
        left_frame=frame,
        right_frame=frame,
        left_joint_positions=[0.0] * 6,
        left_gripper=0.0,
        right_joint_positions=[0.0] * 6,
        right_gripper=0.0,
        camera_capture_times_ns=(capture_time_ns,) * 3,
    )
    with dreamscale.connect(model="molmoact2-bimanual-yam") as policy:
        chunk = policy.predict(observation, instruction="fold the cloth")
        print(chunk.actions)


if __name__ == "__main__":
    main()
