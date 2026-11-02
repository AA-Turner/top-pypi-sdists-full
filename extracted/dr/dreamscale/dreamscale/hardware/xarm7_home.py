"""Attended xArm 7 homing, and saving the arms' current pose as home.

There is no torque release: an enabled xArm holds its last target, so homing finishes with
both arms holding at home.
"""

from __future__ import annotations

import asyncio
import math
from dataclasses import replace

import numpy as np

from dreamscale.embodiments import XARM7

from .xarm7_config import ARMS, load_config, save_config
from .xarm7_rig import XArm7Rig
from .xarm_arm import STILL, XArm

SET_COMMAND = "dreamscale robots xarm7 home --set"


def _confirm(prompt, input_fn) -> bool:
    try:
        while input_fn(prompt).strip():
            pass
    except (EOFError, KeyboardInterrupt):
        return False
    return True


def home_xarm7(config_path, *, input_fn=input, print_fn=print, rig_factory=XArm7Rig) -> bool:
    """Open the grippers and move both arms slowly to the saved home pose. True once home."""
    config = load_config(config_path).validate(complete=True)
    if config.home_pose is None:
        raise ValueError(
            "No home pose saved yet. Move the arms there in UFACTORY Studio's manual mode, "
            f"then run: {SET_COMMAND}"
        )
    print_fn(
        "Both arms move slowly to their home pose and open their grippers. Clear the bench "
        "and keep the E-stop in reach."
    )
    if not _confirm("Enter to home · Ctrl+C to cancel: ", input_fn):
        return False
    rig = rig_factory(config, roles=())
    homed = False
    try:
        rig.open(attended=True, cameras=False)
        print_fn("Homing… Ctrl+C to stop.")
        asyncio.run(rig.home())
        homed = True
        print_fn("✓ Home")
    except KeyboardInterrupt:
        print_fn("Homing stopped.")
    finally:
        rig.close()
    print_fn(f"Arms holding position. {XARM7.held_hint}")
    return homed


def set_home_xarm7(
    config_path, *, input_fn=input, print_fn=print, arm_factory=None,
) -> tuple[float, ...] | None:
    """Save where both arms are now as home. Reads only; nothing moves."""
    config = load_config(config_path).validate(complete=True)
    print_fn(
        "Move both arms to their home pose (UFACTORY Studio's manual mode): somewhere each "
        "can start and end every run, grippers clear of the bench and the wrist cameras "
        "seeing the work area."
    )
    if not _confirm("Let go of the arms, then Enter · Ctrl+C to cancel: ", input_fn):
        return None
    factory = arm_factory or (lambda name: XArm(config.arms[name].host))
    pose = []
    for name in ARMS:
        arm = factory(name)
        arm.connect(control=False)
        try:
            state = arm.snapshot()
        finally:
            arm.close()
        if float(np.max(np.abs(state.velocity))) > STILL:
            raise ValueError(f"The {name} arm is still moving. Let go of it, then run this again.")
        if any(not lo <= v <= hi for v, (lo, hi) in zip(state.position, arm.limits, strict=True)):
            raise ValueError(
                f"A {name} joint is too close to its limit to command. Move it back, then run "
                "this again."
            )
        joints = ", ".join(f"{math.degrees(v):.1f}" for v in state.position)
        print_fn(f"{name.title()} joints (degrees): {joints}")
        pose += [float(v) for v in state.position]
    if config.home_pose is not None:
        print_fn("This replaces the saved home pose.")
    if not _confirm("Enter to save as home · Ctrl+C to cancel: ", input_fn):
        return None
    save_config(replace(config, home_pose=tuple(pose)), config_path)
    print_fn("✓ Home saved. Return to it any time with: dreamscale robots xarm7 home")
    return tuple(pose)
