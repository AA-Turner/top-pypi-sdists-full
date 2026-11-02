"""Minimal non-actuating DreamZero-YAM control loop.

Replace ``capture`` with synchronized YAM camera/state reads whose timestamps
describe the actual captures. ``use_action`` only prints returned absolute
targets; validate local safety limits before replacing it with robot actuation.
"""

from __future__ import annotations

import time

import numpy as np

import dreamscale


def capture(_context):
    capture_time_ns = time.time_ns()
    frame = np.zeros((360, 640, 3), dtype=np.uint8)
    return dreamscale.dreamzero_yam.observation(
        top_frame=frame,
        left_frame=frame,
        right_frame=frame,
        camera_capture_times_ns=(capture_time_ns,) * 3,
        left_joint_positions=[0.0] * 6,
        left_gripper=0.0,
        right_joint_positions=[0.0] * 6,
        right_gripper=0.0,
    )


def use_action(action, _context):
    print(action)


def main() -> None:
    with dreamscale.connect("dreamzero-yam") as policy:
        policy.run(
            instruction="fold the cloth",
            observe=capture,
            act=use_action,
            max_actions=30,
        )


if __name__ == "__main__":
    main()
