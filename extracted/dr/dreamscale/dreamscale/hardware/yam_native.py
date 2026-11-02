"""Optional, process-owned adapter for one explicitly mapped I2RT arm.

The native controller is never imported by discovery or configuration. Each arm
owns a non-daemon process, so a hung constructor/command/close cannot leave an
unjoined controller thread in this interpreter. Forced termination stops host
control traffic; it cannot prove physical torque-off. Use the hardware E-stop
when teardown is unconfirmed.
"""

from __future__ import annotations

import json
import multiprocessing as mp
import time
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Protocol

import numpy as np

from .rig import RigFault
from .yam_config import ArmConfig

# Dreamscale's PyPI build of I2RT at the qualified upstream revision below
# (v1.3.6), with packaging-only changes. An upstream git install of that same
# revision is also accepted.
I2RT_DISTRIBUTION = "dreamscale-i2rt"
I2RT_VERSION = "1.3.6.post1"
I2RT_REVISION = "120c3c81400171174604e503943f8d1ebc891058"
# The pinned DM driver encodes position in 16 bits over [-12.5, 12.5] rad.
# Zero decodes to +/- half a count. This is measurement resolution, not extra
# travel: commanded targets must still stay inside the native controller limits.
I2RT_POSITION_QUANTUM_RAD = 25.0 / ((1 << 16) - 1)


class YamHardwareError(RigFault):
    pass


def native_driver_detail() -> str:
    """Describe the installed qualified driver, or raise pointing to setup."""
    try:
        if metadata.version(I2RT_DISTRIBUTION) == I2RT_VERSION:
            return f"{I2RT_DISTRIBUTION} {I2RT_VERSION}"
    except metadata.PackageNotFoundError:
        pass
    try:
        direct = json.loads(metadata.distribution("i2rt").read_text("direct_url.json") or "{}")
        if direct.get("vcs_info", {}).get("commit_id") == I2RT_REVISION:
            return f"I2RT {I2RT_REVISION[:7]} (git)"
    except metadata.PackageNotFoundError:
        pass
    # Setup installs (or reinstalls) the pinned driver in whatever environment runs it.
    raise YamHardwareError(
        f"The qualified YAM driver ({I2RT_DISTRIBUTION} {I2RT_VERSION}) is not installed. "
        "Run: dreamscale robots yam setup"
    )


def check_native_pin() -> None:
    native_driver_detail()


@dataclass(frozen=True)
class ArmState:
    position: np.ndarray  # six radians, then normalized gripper
    velocity: np.ndarray
    timestamp: float  # actual acquisition Unix seconds, never invocation time
    healthy: bool = True

    def validate(self, max_age_s=0.25):
        if (
            not self.healthy
            or self.position.shape != (7,)
            or self.velocity.shape != (7,)
            or not np.isfinite(self.position).all()
            or not np.isfinite(self.velocity).all()
            or not np.isfinite(self.timestamp)
            or not -0.1 <= time.time() - self.timestamp <= max_age_s
            or not 0 <= self.position[6] <= 1
        ):
            raise YamHardwareError(
                "Arm state is stale, invalid, or controller stopped. Stop and reconnect."
            )
        return self


class Arm(Protocol):
    limits: np.ndarray  # strict hardware profile, (7, 2), normalized gripper

    def snapshot(self) -> ArmState: ...
    def command(self, target: np.ndarray) -> np.ndarray: ...
    def close(self) -> None: ...


class NativeArm:
    """Pinned implementation, constructed only inside an attended child process."""

    def __init__(self, config: ArmConfig):
        check_native_pin()
        from i2rt.robots.get_robot import get_yam_robot
        from i2rt.robots.utils import ArmType, GripperType

        arm_type, gripper_type = ArmType[config.arm_type], GripperType[config.gripper_type]
        self.robot = get_yam_robot(
            channel=config.can_interface,
            arm_type=arm_type,
            gripper_type=gripper_type,
            zero_gravity_mode=False,
            enable_auto_recovery=False,
        )
        try:
            info = self.robot.get_robot_info()
            # Use the same bounds that the pinned controller enforces. Its YAM
            # profile includes a 0.15-rad margin beyond the XML model ranges.
            # Reloading the XML here falsely rejects valid near-zero targets.
            try:
                limits = np.array(info.get("joint_limits"), dtype=float, copy=True)
            except (TypeError, ValueError) as exc:
                raise YamHardwareError("Driver returned invalid hardware joint limits.") from exc
            if limits.shape != (6, 2):
                raise YamHardwareError("Driver must report six hardware joint limits.")
            self.limits = np.vstack((limits, [0.0, 1.0]))
            _validate_limits(self.limits)
            if (
                info["gripper_index"] != 6
                or info["gripper_limits"] is None
                or np.asarray(info["gripper_limits"]).shape != (2,)
                or not np.isfinite(info["gripper_limits"]).all()
                or info["gripper_limits"][0] == info["gripper_limits"][1]
            ):
                raise YamHardwareError(
                    "Driver has no calibrated normalized six-joint gripper profile."
                )
            self.snapshot().validate()
        except BaseException:
            self.robot.close()
            raise

    def snapshot(self):
        robot = self.robot
        if not robot._state_lock.acquire(timeout=0.1):
            raise YamHardwareError("Arm state lock timed out.")
        try:
            state = robot._joint_state
            healthy = robot._server_thread.is_alive() and robot.motor_chain.running
            return ArmState(state.pos.copy(), state.vel.copy(), state.timestamp, healthy)
        finally:
            robot._state_lock.release()

    def command(self, target):
        self.snapshot().validate()
        applied = np.array(target, dtype=float, copy=True)
        self.robot.command_joint_pos(applied)  # upstream clips this array in-place
        return applied

    def close(self):
        self.robot.close()


def _validate_limits(limits):
    if (
        limits.shape != (7, 2)
        or not np.isfinite(limits).all()
        or not (limits[:, 0] < limits[:, 1]).all()
        or not np.array_equal(limits[6], [0.0, 1.0])
    ):
        raise YamHardwareError(
            "Expected six finite hardware joint limits and normalized gripper [0, 1]."
        )


def _arm_process(pipe, config, factory):
    # Prevent two Dreamscale instances owning the same explicit CAN interface.
    import fcntl
    import os
    import signal
    import sys
    import tempfile
    import threading

    # The parent owns terminal cancellation: hold first, then close by RPC.
    # A foreground-group SIGINT must not tear down a controller independently.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    parent_pid = os.getppid()

    def watch_parent():
        while True:
            time.sleep(0.2)
            if os.getppid() != parent_pid:
                # Parent cannot join us after it dies. Terminate every native
                # controller thread here; physical torque-off is unconfirmed.
                os._exit(1)

    threading.Thread(target=watch_parent, daemon=True).start()

    lock = None
    arm = None
    diagnostics = None
    try:
        # Native libraries print directly and may write from controller threads.
        # Redirect only this child process; the parent still receives every RPC
        # fault and remains responsible for visible recovery instructions.
        from .yam_output import open_diagnostic_log

        try:
            _, diagnostics = open_diagnostic_log(f"native-{config.can_interface}")
            sys.stdout.flush()
            sys.stderr.flush()
            os.dup2(diagnostics.fileno(), 1)
            os.dup2(diagnostics.fileno(), 2)
            sys.stdout.reconfigure(line_buffering=True)
            sys.stderr.reconfigure(line_buffering=True)
        except OSError:
            print("Native diagnostic log unavailable; showing driver details.", file=sys.stderr)
        # Keep the pre-rename name: an older `dropbear` process on the same arm
        # must see this lock too.
        lock_path = (
            Path(tempfile.gettempdir()) / f"dropbear-yam-{os.getuid()}-{config.can_interface}.lock"
        )
        lock = lock_path.open("a")
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        arm = factory(config)
        _validate_limits(arm.limits)
        pipe.send(("ok", arm.limits))
        while True:
            method, arg = pipe.recv()  # parent death closes the pipe
            if method == "close":
                arm.close()
                arm = None
                pipe.send(("ok", None))
                break
            value = arm.snapshot() if method == "snapshot" else arm.command(arg)
            pipe.send(("ok", value))
    except EOFError:
        pass
    except BaseException as exc:
        try:
            pipe.send(("error", str(exc)))
        except (BrokenPipeError, EOFError, OSError):
            pass
    finally:
        if arm is not None:
            arm.close()
        if lock is not None:
            lock.close()
        pipe.close()
        if diagnostics is not None:
            sys.stdout.flush()
            sys.stderr.flush()
            diagnostics.close()


class ProcessArm:
    """Bounded synchronous arm interface. Factory must be spawn-picklable.

    Constructor requires consent at the owning YamRig.open boundary. Native
    initialization may calibrate the gripper and sends CAN motor traffic.
    """

    def __init__(
        self,
        config,
        *,
        factory=NativeArm,
        startup_timeout_s=45.0,
        command_timeout_s=0.5,
        close_timeout_s=2.0,
    ):
        self.command_timeout_s, self.close_timeout_s = command_timeout_s, close_timeout_s
        ctx = mp.get_context("spawn")
        self.pipe, child = ctx.Pipe()
        self.process = ctx.Process(target=_arm_process, args=(child, config, factory))
        self.closed = False
        self.process.start()
        child.close()
        try:
            self.limits = np.asarray(self._receive(startup_timeout_s))
            _validate_limits(self.limits)
        except BaseException as exc:
            self._terminate()
            raise YamHardwareError(
                "Native connection did not complete; its controller process stopped. "
                "Physical torque-off is unconfirmed; check the hardware E-stop. " + str(exc)
            ) from exc

    def _terminate(self):
        self.closed = True
        self.pipe.close()
        if self.process.is_alive():
            self.process.terminate()
        self.process.join(self.close_timeout_s)
        if self.process.is_alive():
            self.process.kill()
            self.process.join(self.close_timeout_s)
        if self.process.is_alive():
            raise YamHardwareError("Controller process could not stop. Use the hardware E-stop.")

    def _receive(self, timeout):
        if not self.pipe.poll(timeout):
            raise YamHardwareError(
                "Native driver timed out; torque-off unconfirmed. Use the hardware E-stop."
            )
        try:
            kind, result = self.pipe.recv()
        except (EOFError, OSError) as exc:
            raise YamHardwareError(
                "Native controller exited; physical hold is unconfirmed."
            ) from exc
        if kind != "ok":
            raise YamHardwareError(result)
        return result

    def _request(self, method, arg=None, timeout=None):
        if self.closed:
            raise YamHardwareError("Arm disconnected. Reconnect hardware before running.")
        try:
            self.pipe.send((method, arg))
            return self._receive(self.command_timeout_s if timeout is None else timeout)
        except BaseException:
            self._terminate()
            raise

    def snapshot(self):
        return self._request("snapshot")

    def command(self, target):
        return self._request("command", target)

    def close(self):
        if self.closed:
            return
        try:
            self._request("close", timeout=self.close_timeout_s)
        finally:
            self._terminate()
