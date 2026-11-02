"""Attended Universal Robots homing, and saving the arm's current pose as home.

There is no torque release: a powered UR holds its pose once the program ends, so homing
finishes with the arm holding at home.
"""

from __future__ import annotations

import asyncio
import math
from dataclasses import replace

import numpy as np

from dreamscale.embodiments import UR

from .ur_arm import URArm, flange_pose
from .ur_config import load_config, save_config
from .ur_rig import URRig

SET_COMMAND = "dreamscale robots ur home --set"
# Joint speed below which the arm counts as still, rad/s.
STILL = 0.01


def _confirm(prompt, input_fn) -> bool:
    try:
        while input_fn(prompt).strip():
            pass
    except (EOFError, KeyboardInterrupt):
        return False
    return True


def home_ur(config_path, *, input_fn=input, print_fn=print, rig_factory=URRig) -> bool:
    """Move slowly to the saved home pose and open the gripper. True once home."""
    config = load_config(config_path).validate(complete=True)
    if config.home_pose is None:
        raise ValueError(
            "No home pose saved yet. Freedrive the arm to it on the pendant, then run: "
            f"{SET_COMMAND}"
        )
    print_fn(
        "The arm moves slowly to its home pose and opens the gripper. Clear the workspace "
        "and keep the E-stop in reach."
    )
    if not _confirm("Enter to home · Ctrl+C to cancel: ", input_fn):
        return False
    rig = rig_factory(config, roles=())
    homed = False
    try:
        print_fn(
            f"Starting the {config.arm.program} program (in Local control, press Play on the "
            "pendant)."
        )
        rig.open(attended=True, cameras=False)
        print_fn("Homing… Ctrl+C to stop.")
        asyncio.run(rig.home())
        homed = True
        print_fn("✓ Home")
    except KeyboardInterrupt:
        print_fn("Homing stopped.")
    finally:
        rig.close()
    print_fn(f"Arm holding position. {UR.held_hint}")
    return homed


def describe(q, model: str) -> str:
    """Joints in degrees and where the flange is, for the operator to check."""
    T = flange_pose(q, model)
    x, y, z = T[:3, 3]
    reach = math.hypot(x, y)
    joints = ", ".join(f"{math.degrees(v):.1f}" for v in q)
    return (
        f"Joints (degrees): {joints}\n"
        f"Flange: {z * 100:.0f} cm above the base, {reach * 100:.0f} cm out from it"
    )


def set_home_ur(
    config_path, *, input_fn=input, print_fn=print, arm_factory=None,
) -> tuple[float, ...] | None:
    """Save where the arm is now as home. Reads only; nothing moves."""
    config = load_config(config_path).validate(complete=True)
    print_fn(
        "Move the arm to its home pose with freedrive on the pendant: somewhere it can start "
        "and end every run, with the gripper clear of the table and the wrist camera seeing "
        "the work area."
    )
    if not _confirm("Let go of the arm, then Enter · Ctrl+C to cancel: ", input_fn):
        return None
    arm = (arm_factory or (lambda: URArm(config.arm.host, config.arm.model)))()
    arm.connect(control=False)
    try:
        state = arm.snapshot().validate(1.0)
    finally:
        arm.close()
    q = state.position
    if float(np.max(np.abs(state.velocity))) > STILL:
        raise ValueError("The arm is still moving. Let go of it, then run this again.")
    if any(not lo <= v <= hi for v, (lo, hi) in zip(q, arm.limits, strict=True)):
        raise ValueError(
            "A joint is too close to its limit to command (±360°, the elbow ±180°). Turn it "
            "back toward zero, then run this again."
        )
    print_fn(describe(q, config.arm.model))
    if flange_pose(q, config.arm.model)[2, 2] > -0.5:
        print_fn("Note: the gripper isn't pointing down at this pose.")
    if abs(q[5]) > math.pi:
        print_fn("Note: wrist 3 is turned more than half a turn; its cable winds up.")
    if config.home_pose is not None:
        print_fn("This replaces the saved home pose.")
    if not _confirm("Enter to save as home · Ctrl+C to cancel: ", input_fn):
        return None
    pose = tuple(float(v) for v in q)
    save_config(replace(config, home_pose=pose), config_path)
    print_fn("✓ Home saved. Return to it any time with: dreamscale robots ur home")
    return pose
