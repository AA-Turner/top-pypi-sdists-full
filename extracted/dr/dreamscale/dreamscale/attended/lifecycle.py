"""Attended homing, measured hold, and controller ownership, for any rig."""

from __future__ import annotations

import asyncio
import threading
import time

# A lagging camera (frames older than the rig's 1 s freshness limit) is reported at most this
# often per camera; the run continues. A stopped camera still ends the task.
CAMERA_LAG_WARN_EVERY_S = 10.0


def safe_printer(print_fn):
    def emit(message):
        try:
            print_fn(message)
        except Exception:
            # Output failure must never bypass physical cleanup.
            pass

    return emit


class AttendedLifecycle:
    """Never retry failed/interrupted homing or move after an unconfirmed hold.

    A rig without a home pose (has_home False) never moves on its own: startup
    and return home only hold where the arm is.
    """

    def __init__(self, rig, *, print_fn=print, ready=True, arms="arms"):
        self.rig = rig
        self.arms = arms
        self.emit = safe_printer(print_fn)
        self.ready = ready
        self.needs_return_home = True
        self._aborted = False
        self._home_task = None
        self._lag_warned: dict[str, float] = {}
        self._lag_lock = threading.Lock()
        if hasattr(rig, "on_camera_lag"):
            rig.on_camera_lag = self.camera_lag

    def camera_lag(self, role, age_s):
        """Warn, lightly, that a camera's frames are late; called from the rig's threads."""
        now = time.monotonic()
        with self._lag_lock:
            if now - self._lag_warned.get(role, -CAMERA_LAG_WARN_EVERY_S) < CAMERA_LAG_WARN_EVERY_S:
                return
            self._lag_warned[role] = now
        name = str(role).replace("_", " ").title()
        self.emit(f"{name} camera is lagging ({age_s:.1f} s since its last frame); continuing.")

    @property
    def has_home(self):
        return getattr(self.rig, "has_home", True)

    @property
    def homing(self):
        return self._home_task is not None

    def opened(self):
        self.ready = True

    def task_started(self):
        self.needs_return_home = True

    def inhibit_return_home(self, reason):
        self._aborted = True
        self.emit(reason)

    def request_stop(self):
        try:
            self.rig.block_dispatch()
        except BaseException:
            self._aborted = True
            raise
        finally:
            if self.homing:
                self._aborted = True
                self._home_task.cancel()
            elif not self.ready:
                self._aborted = True

    async def wait_for_home(self):
        """Join the cancelled ramp before its controller owner can disconnect."""
        if self._home_task is not None:
            await asyncio.gather(self._home_task, return_exceptions=True)

    def stop_and_hold(self):
        try:
            try:
                self.rig.block_dispatch()
            finally:
                holds = self.rig.stop()
        except BaseException:
            self.inhibit_return_home("Measured-pose hold unconfirmed. Use hardware E-stop.")
            raise
        if not holds or any(held is not True for held in holds.values()):
            self.inhibit_return_home("Measured-pose hold unconfirmed. Use hardware E-stop.")
        return holds

    async def startup_home(self):
        if self._aborted or not self.ready or self.rig.faulted:
            raise RuntimeError("Cannot home automatically; reconnect the hardware first.")
        if not self.has_home:
            self.needs_return_home = False
            return None
        self.emit(f"Homing {self.arms}… Ctrl+C stops and holds.")
        self._home_task = asyncio.create_task(self.rig.home())
        try:
            offset = await self._home_task
            self.needs_return_home = False
            return offset
        except BaseException:
            self._aborted = True
            raise
        finally:
            self._home_task = None

    async def return_home(self):
        if self._aborted or not self.ready:
            return False
        if self.rig.faulted:
            self.inhibit_return_home("Cannot return home automatically after a hardware fault.")
            return False
        if not self.needs_return_home:
            return True
        if not self.has_home:
            # The task already ended in a measured-pose hold; there is nowhere to go.
            self.needs_return_home = False
            return True
        self._home_task = asyncio.create_task(self.rig.home())
        self.emit("Returning home… Ctrl+C to stop.")
        try:
            await self._home_task
            self.needs_return_home = False
            self.emit("✓ Home")
            return True
        except asyncio.CancelledError:
            self.inhibit_return_home("Return home stopped.")
            return False
        except Exception as exc:
            self.inhibit_return_home(f"Cannot return home: {exc}")
            return False
        finally:
            self._home_task = None

    def close(self):
        """Final disconnection; the rig closes every controller and holds again."""
        self.rig.close()


# Pre-refactor name, kept for callers of the YAM modules.
YamLifecycle = AttendedLifecycle
