"""Attended local homing followed by explicit torque release."""

from __future__ import annotations

import asyncio

from .yam_can import discover_can_interfaces, resolve_arms
from .yam_config import load_config
from .yam_rig import YamRig


def home_yam(
    config_path, *, input_fn=input, print_fn=print, rig_factory=YamRig,
    discover_can=discover_can_interfaces,
):
    config = resolve_arms(
        load_config(config_path).validate(complete=True), discover_can=discover_can
    )
    print_fn("Arms will move home, then release torque. Clear the workspace; support arms at home.")
    try:
        while input_fn("Enter to home and release · Ctrl+C to cancel: ").strip():
            pass
    except (EOFError, KeyboardInterrupt):
        return
    rig = rig_factory(config, max_joint_step=0.15, max_joint_velocity=1.0)
    try:
        rig.open(attended=True, cameras=False)
        print_fn("Homing… Ctrl+C to stop.")
        asyncio.run(rig.home())
        print_fn("✓ Home")
        # Keep both client leases until home succeeds; never detach/reacquire
        # between homing and release, or release after failure/cancellation.
        for arm in rig.arms.values():
            arm.release()
        print_fn("✓ Motor torque released")
    finally:
        rig.close()
