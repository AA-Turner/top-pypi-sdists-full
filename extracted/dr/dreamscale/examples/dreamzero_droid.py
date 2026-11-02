"""Minimal DreamZero-DROID control loop.

Replace ``capture`` and ``apply_action`` with the customer's synchronized DROID
camera/robot adapters. Camera timestamps must describe the actual captures.
"""

from __future__ import annotations

import time

import numpy as np

import dreamscale
from dreamscale import dreamzero


def capture(_ctx):
    timestamp = time.time_ns()
    frame = np.zeros((180, 320, 3), dtype=np.uint8)
    return dreamzero.observation(
        exterior_frame=frame,
        second_exterior_frame=frame,
        wrist_frame=frame,
        camera_capture_times_ns=(timestamp, timestamp, timestamp),
        joint_positions=[0.0] * 7,
        gripper=0.0,
    )


def apply_action(action, _ctx):
    print(action)


with dreamscale.connect("dreamzero-droid") as policy:
    policy.run(
        instruction="pick up the object",
        observe=capture,
        act=apply_action,
        max_actions=120,
    )
