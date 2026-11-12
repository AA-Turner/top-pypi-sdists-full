"""Attended OpenARM homing, and saving the arms' current pose as home.

Anvil's control stack holds the arms at their last target, so homing finishes with them
holding at home. Each gripper is held at the opening it reads.
"""

from __future__ import annotations

import asyncio
import math
from dataclasses import replace

import numpy as np

from dreamscale.embodiments import OPENARM

from .openarm_config import JOINTS, load_config, save_config
from .openarm_rig import OpenArmRig
from .openarm_stack import AnvilStack

SET_COMMAND = "dreamscale robots openarm home --set"
# Radians per second below which an arm counts as still.
STILL = 0.02


def _confirm(prompt, input_fn) -> bool:
    try:
        while input_fn(prompt).strip():
            pass
    except (EOFError, KeyboardInterrupt):
        return False
    return True


def home_openarm(config_path, *, input_fn=input, print_fn=print, rig_factory=OpenArmRig) -> bool:
    """Move the arms slowly to the saved home pose. True once home."""
    config = load_config(config_path).validate(complete=True)
    if config.home_pose is None:
        raise ValueError(
            f"No home pose saved yet. With the arms where a run should start, run: {SET_COMMAND}"
        )
    print_fn(
        "The arms move slowly to their home pose. Clear the workspace and keep the E-stop "
        "in reach."
    )
    if not _confirm("Enter to home · Ctrl+C to cancel: ", input_fn):
        return False
    rig = rig_factory(
        config, roles=(), max_joint_step=OPENARM.max_joint_step,
        max_joint_velocity=OPENARM.max_joint_velocity,
    )
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
    print_fn(f"Arms holding position. {OPENARM.held_hint}")
    return homed


def set_home_openarm(
    config_path, *, input_fn=input, print_fn=print, stack_factory=AnvilStack,
) -> tuple[float, ...] | None:
    """Save where the arms are now as home. Reads only; nothing moves."""
    config = load_config(config_path).validate(complete=True)
    print_fn(
        "Home is where the arms start and end every run, with the cameras seeing the work "
        "area. The pose Anvil's control stack brings them to when it starts works."
    )
    if not _confirm("With the arms there and still, Enter · Ctrl+C to cancel: ", input_fn):
        return None
    stack = stack_factory(config.url)
    pose = []
    try:
        stack.open()
        states = stack.wait_for_arms(config.arms)
        for arm in config.arms:
            state, limits = states[arm], stack.limits(arm)
            if float(np.max(np.abs(state.velocity[:JOINTS]))) > STILL:
                raise ValueError(
                    f"The {arm} arm is still moving. Run this again once it's still."
                )
            joints = state.position[:JOINTS]
            if any(not lo <= v <= hi
                   for v, (lo, hi) in zip(joints, limits[:JOINTS], strict=True)):
                raise ValueError(
                    f"A {arm} joint is too close to its limit to command. Move it back, "
                    "then run this again."
                )
            print_fn(
                f"{arm.title()} joints (degrees): "
                + ", ".join(f"{math.degrees(v):.1f}" for v in joints)
            )
            pose += [float(v) for v in joints]
    finally:
        stack.close()
    if config.home_pose is not None:
        print_fn("This replaces the saved home pose.")
    if not _confirm("Enter to save as home · Ctrl+C to cancel: ", input_fn):
        return None
    save_config(replace(config, home_pose=tuple(pose)), config_path)
    print_fn("✓ Home saved. Return to it any time with: dreamscale robots openarm home")
    return tuple(pose)
