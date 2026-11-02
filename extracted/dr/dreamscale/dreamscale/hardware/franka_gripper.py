"""Gripper drivers: a 0 (open) to 1 (closed) command and state, whatever the hardware.

The Franka Hand's moves block and can't be retargeted mid-stroke, so its driver treats
the policy's continuous command as open or closed, with hysteresis, on its own thread.
Reading its width waits for the Hand's next state message, so another thread keeps the
latest one and state() returns it without waiting.
"""

from __future__ import annotations

import threading
import time

# Commands at or above GRASP_AT close the Hand; at or below OPEN_AT open it.
GRASP_AT = 0.6
OPEN_AT = 0.4
SPEED_M_S = 0.1
FORCE_N = 20.0
# A width older than this means the Hand stopped reporting.
MAX_STATE_AGE_S = 1.0
# The poller's floor between reads, should a read ever return without waiting.
POLL_INTERVAL_S = 0.005


class GripperError(RuntimeError):
    """The gripper could not be reached or refused a command."""


class NoGripper:
    """A rig without a gripper: state stays open and commands are ignored."""

    def open(self) -> NoGripper:
        return self

    def state(self) -> float:
        return 0.0

    def command(self, value: float) -> None:
        pass

    def close(self) -> None:
        pass


class FrankaHand:
    def __init__(self, host: str, *, franky=None):
        self.host = host
        self._franky = franky
        self.gripper = None
        self.max_width = None
        self._wanted = None  # "open" or "closed", the latest decided command
        self._applied = None
        self._error = None
        self._wake = threading.Condition()
        self._running = False
        self._thread = None
        self._poller = None
        self._latest = None  # (width in m, time.monotonic())

    @property
    def franky(self):
        if self._franky is None:
            import franky

            self._franky = franky
        return self._franky

    def open(self) -> FrankaHand:
        fk = self.franky
        try:
            gripper = fk.Gripper(self.host)
            max_width = float(gripper.max_width)
        except fk.Exception as exc:
            raise GripperError(f"Can't reach the Franka Hand at {self.host}: {exc}") from exc
        if not max_width > 0:
            raise GripperError("The Franka Hand has no measured width. Home it in Desk.")
        self.gripper, self.max_width = gripper, max_width
        self._latest = (float(gripper.width), time.monotonic())
        self._running = True
        self._thread = threading.Thread(target=self._loop, name="franka-hand", daemon=True)
        self._poller = threading.Thread(target=self._poll, name="franka-hand-state", daemon=True)
        self._thread.start()
        self._poller.start()
        return self

    def state(self) -> float:
        if self._error is not None:
            raise GripperError(f"Franka Hand command failed: {self._error}")
        if self.gripper is None or self._latest is None:
            raise GripperError("Franka Hand is not connected.")
        width, at = self._latest
        if time.monotonic() - at > MAX_STATE_AGE_S:
            raise GripperError("Franka Hand stopped reporting its width. Check its cable.")
        return min(1.0, max(0.0, 1.0 - width / self.max_width))

    def _poll(self):
        gripper = self.gripper
        while self._running:
            started = time.monotonic()
            try:
                self._latest = (float(gripper.width), time.monotonic())
            except Exception:  # a stale width surfaces through state()
                pass
            time.sleep(max(0.0, POLL_INTERVAL_S - (time.monotonic() - started)))

    def command(self, value: float) -> None:
        value = float(value)
        with self._wake:
            current = self._wanted
            if value >= GRASP_AT:
                wanted = "closed"
            elif value <= OPEN_AT:
                wanted = "open"
            else:
                wanted = current
            if wanted is not None and wanted != current:
                self._wanted = wanted
                self._wake.notify()

    def _loop(self):
        while True:
            with self._wake:
                while self._running and self._wanted == self._applied:
                    self._wake.wait()
                if not self._running:
                    return
                wanted = self._wanted
            try:
                if wanted == "closed":
                    # Width 0 with a wide outer tolerance: any object counts as grasped.
                    self.gripper.grasp(0.0, SPEED_M_S, FORCE_N, epsilon_outer=self.max_width)
                else:
                    self.gripper.move(self.max_width, SPEED_M_S)
                self._applied = wanted
            except Exception as exc:  # surfaced by the next state() read
                self._error = exc
                return

    def close(self) -> None:
        with self._wake:
            self._running = False
            self._wake.notify()
        gripper, self.gripper = self.gripper, None
        if gripper is not None:
            try:
                gripper.stop()
            except Exception:
                pass
        for thread in (self._thread, self._poller):
            if thread is not None:
                thread.join(timeout=5.0)


def make_gripper(gripper_type: str, host: str):
    if gripper_type == "franka_hand":
        return FrankaHand(host)
    if gripper_type == "none":
        return NoGripper()
    raise GripperError(f"The {gripper_type} gripper driver isn't available yet.")
