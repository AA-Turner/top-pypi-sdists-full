"""Request one MolmoAct2-DROID action chunk for a Franka observation."""

from __future__ import annotations

import numpy as np

import dreamscale


def infer(
    exterior_rgb: np.ndarray,
    wrist_rgb: np.ndarray,
    current_joint_radians: list[float],
    current_gripper: float,
):
    """Return absolute joint/gripper targets; do not apply them without safety checks."""
    with dreamscale.connect(model="molmoact2-droid") as policy:
        observation = dreamscale.franka.observation(
            exterior_frame=exterior_rgb,
            wrist_frame=wrist_rgb,
            joint_positions=current_joint_radians,
            gripper=current_gripper,
        )
        return policy.predict(
            observation,
            instruction="pick up the blue ring",
        )
