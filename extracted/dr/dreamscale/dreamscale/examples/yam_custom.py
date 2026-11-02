"""Custom RGB and controller callbacks with an offline, synthetic smoke test.

Run: python -m dreamscale.examples.yam_custom
For hardware, adapt the callbacks, then explicitly call run_attended().
"""

from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import Callable

import numpy as np

from dreamscale.hardware.camera_sources import (
    CameraError,
    CameraReaders,
    CameraSpec,
    FrameUnavailable,
    RGBFrame,
)
from dreamscale.hardware.yam_config import ArmConfig, YamConfig
from dreamscale.hardware.yam_native import ArmState
from dreamscale.hardware.yam_rig import YamRig
from dreamscale.hardware.yam_runner import YamTaskRunner, interactive_tasks


class PushRGBSource:
    """Register publish() with your device's bounded acquisition callback.

    The producer supplies original acquisition clocks and an increasing sequence.
    latest() never creates a fresh timestamp for an old frame. A hardware producer
    should stop/join its acquisition thread in on_close, including after failure.
    """

    def __init__(self, on_open: Callable, on_close: Callable):
        self.on_open, self.on_close = on_open, on_close
        self._lock = threading.Lock()
        self._frame = None
        self._opened = False

    def publish(self, rgb, *, timestamp_ns, monotonic_ns, sequence):
        frame = RGBFrame(np.array(rgb, copy=True), timestamp_ns, monotonic_ns, sequence)
        frame.validate()
        with self._lock:
            self._frame = frame

    def open(self):
        self._opened = True
        try:
            self.on_open(self.publish)
        except BaseException:
            self._opened = False
            raise

    def latest(self, max_age_s=1.0):
        with self._lock:
            if not self._opened:
                raise CameraError("No RGB frame available; source is closed.")
            frame = self._frame
        if frame is None:
            raise FrameUnavailable("No RGB frame acquired yet.")
        return frame.validate(max_age_s)

    def close(self):
        try:
            self.on_close()
        finally:
            with self._lock:
                self._frame = None
                self._opened = False


class CallbackArm:
    """One six-joint arm and one [0,1] gripper in model order.

    read() returns a copied ArmState with the device acquisition Unix timestamp.
    write(target) returns the actual applied seven values, including clipping.
    Bound all three callbacks; blocked vendor calls belong in an owned process.
    The limits must come from your verified hardware profile, never this demo.
    """

    def __init__(self, *, limits, read: Callable, write: Callable, disconnect: Callable):
        self.limits = np.array(limits, dtype=float, copy=True)
        self.read, self.write, self.disconnect = read, write, disconnect

    def snapshot(self):
        return self.read()

    def command(self, target):
        return np.array(self.write(np.array(target, copy=True)), dtype=float, copy=True)

    def close(self):
        self.disconnect()


def make_rig(config, sources, arm_factory):
    # Keys match CameraSpec.device for backend="custom". Built-in UVC/RealSense/
    # ZED readers can coexist in the same config; only custom IDs need a source.
    return YamRig(
        config,
        readers_factory=lambda specs: CameraReaders(specs, custom_sources=sources),
        arm_factory=arm_factory,
    )


def run_attended(config, sources, arm_factory):
    """Explicitly invoked hardware path; opening can enable motors/calibration."""
    print("Confirm camera views, physical left/right cabling, limits and E-stop.")
    print("Connecting enables control and may calibrate/move grippers.")
    if input("Type 'connect' for this attended connection: ").strip() != "connect":
        return
    rig = make_rig(config, sources, arm_factory)
    try:
        rig.open(attended=True)

        # These are complete policy.run callbacks. Preserve rig validation,
        # measured holds and requested/applied feedback when adding your hooks.
        def observe(ctx):
            return rig.observe(ctx)

        def act(action, ctx):
            return rig.act(action, ctx)

        def read_hold_action(ctx):
            return rig.read_hold_action(ctx)

        runner = YamTaskRunner(
            rig,
            observe=observe,
            act=act,
            read_hold_action=read_hold_action,
            keep_warm=60,
        )
        # Preview -> explicit execute; each execution obtains fresh observations.
        # Ctrl+C stops the task and holds; cameras/controllers persist until exit.
        asyncio.run(interactive_tasks(runner, max_actions=300))
    finally:
        rig.close()


def offline_smoke():
    """Synthetic images, measured-state stand-ins; no hardware or cloud access."""
    sources = {}
    for index, role in enumerate(("top", "left", "right")):

        def acquire(publish, value=index):
            publish(
                np.full((16, 16, 3), value * 50, dtype=np.uint8),
                timestamp_ns=time.time_ns(),
                monotonic_ns=time.monotonic_ns(),
                sequence=0,
            )

        sources[role] = PushRGBSource(acquire, lambda: None)
    config = YamConfig(
        cameras=[CameraSpec(role, "custom", f"demo:{role}", role) for role in sources],
        roles={role: role for role in sources},
        arms={
            side: ArmConfig(f"demo{index}", "YAM", "LINEAR_3507")
            for index, side in enumerate(("left", "right"))
        },
    )
    closed = []

    def arm_factory(config):
        state = np.array([0.0] * 6 + [0.5])

        def read():
            # This is a synthetic acquisition. A real driver must use its device
            # sample time, not time.time() when reading a cached state.
            return ArmState(state.copy(), np.zeros(7), time.time())

        def write(target):
            state[:] = target
            return state.copy()

        return CallbackArm(
            limits=[[-1.0, 1.0]] * 6 + [[0.0, 1.0]],
            read=read,
            write=write,
            disconnect=lambda: closed.append(config.can_interface),
        )

    rig = make_rig(config, sources, arm_factory)
    try:
        rig.open(attended=True)  # fake factories only; no native import or cloud
        rig.observe()
        rig.enable_dispatch()
        requested = [0.01] * 6 + [0.25] + [-0.01] * 6 + [0.75]
        result = rig.act(requested)
        assert np.allclose(result.accepted_action, requested)
        assert rig.stop() == {"left": True, "right": True}
        assert len(rig.read_hold_action()) == 14
    finally:
        rig.close()
    assert len(closed) == 2
    print("Offline callback smoke passed: RGB, all 14 actions, holds and cleanup.")


if __name__ == "__main__":
    offline_smoke()
