"""Teleoperation device adapters for cold-start demo collection and live clutch takeover.

First-class adapters:
- ``GelloLeaderAdapter``: YAM bimanual 14-DoF GELLO leader arms (serial or injectable reader).
- ``Quest3SWebXRAdapter``: YAM bimanual Quest 3S WebXR controller bridge (local UDP JSON poses
  with damped relative-pose IK and grip-button clutch).
- ``So101LeaderAdapter``: SO-101 6-DoF Feetech leader arm (calibrated degrees + 0-100 gripper).
- ``MockTeleopDevice``: deterministic scriptable device for automated tests and qualification.

All hardware drivers are imported lazily inside ``open()`` so lean SDK installs remain unaffected.
"""

from __future__ import annotations

import json
import math
import socket
import threading
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import numpy as np


@dataclass(frozen=True)
class TeleopSample:
    """One non-blocking reading from a teleoperation input device."""

    target: tuple[float, ...]
    clutch: bool
    timestamp_s: float
    note: str | None = None


@runtime_checkable
class TeleopDevice(Protocol):
    """Contract shared by every leader arm, VR controller bridge, or mock teleop source."""

    name: str
    kind: str
    action_dim: int

    def open(self) -> None: ...
    def read(self) -> TeleopSample: ...
    def sync_pose(self, current_pose: Sequence[float]) -> None: ...
    def close(self) -> None: ...


class ClutchSignal:
    """Thread-safe clutch state (pedal, button, or programmatic toggle/hold)."""

    def __init__(self, *, engaged: bool = False) -> None:
        self._event = threading.Event()
        if engaged:
            self._event.set()

    @property
    def engaged(self) -> bool:
        return self._event.is_set()

    def set(self, engaged: bool) -> None:
        if engaged:
            self._event.set()
        else:
            self._event.clear()

    def toggle(self) -> bool:
        if self._event.is_set():
            self._event.clear()
            return False
        self._event.set()
        return True


def _normalize_vector(values: Sequence[float], expected_dim: int, label: str) -> tuple[float, ...]:
    vec = tuple(float(v) for v in values)
    if len(vec) != expected_dim:
        raise ValueError(f"{label} returned {len(vec)} values; expected {expected_dim}")
    if any(not math.isfinite(v) for v in vec):
        raise ValueError(f"{label} returned non-finite joint values")
    return vec


class GelloLeaderAdapter:
    """Bimanual YAM 14-DoF GELLO leader arm adapter (6 rad + 0..1 gripper per arm).

    Connects either to a pair of serial Dynamixel GELLO buses (left/right) or an
    injectable ``reader`` callback returning ``(position_14, clutch_bool)``.
    """

    kind = "gello"
    action_dim = 14

    def __init__(
        self,
        *,
        left_port: str | None = None,
        right_port: str | None = None,
        joint_signs: Sequence[float] | None = None,
        joint_offsets: Sequence[float] | None = None,
        clutch_signal: ClutchSignal | None = None,
        always_engaged: bool = False,
        reader: Callable[[], tuple[Sequence[float], bool]] | None = None,
        name: str = "yam-gello",
    ) -> None:
        self.name = name
        self.left_port = left_port
        self.right_port = right_port
        self.joint_signs = tuple(float(v) for v in (joint_signs or (1.0,) * 14))
        self.joint_offsets = tuple(float(v) for v in (joint_offsets or (0.0,) * 14))
        if len(self.joint_signs) != 14 or len(self.joint_offsets) != 14:
            raise ValueError("GELLO joint_signs and joint_offsets must each have 14 values")
        self.clutch_signal = clutch_signal or ClutchSignal(engaged=always_engaged)
        self.always_engaged = bool(always_engaged)
        self._reader = reader
        self._opened = False
        self._drivers: list[Any] = []
        self._last_pose: tuple[float, ...] = (0.0,) * 6 + (1.0,) + (0.0,) * 6 + (1.0,)

    def open(self) -> None:
        if self._opened:
            return
        if self._reader is not None:
            self._opened = True
            return
        if not self.left_port or not self.right_port:
            raise RuntimeError(
                "GELLO leader requires left and right serial ports "
                "(e.g. --teleop gello:left=/dev/ttyUSB0,right=/dev/ttyUSB1)."
            )
        try:
            import serial  # type: ignore[import-untyped]
        except ImportError as exc:
            raise RuntimeError(
                "GELLO serial teleop requires pyserial (`pip install pyserial`)."
            ) from exc
        self._drivers = [
            serial.Serial(self.left_port, baudrate=1_000_000, timeout=0.02),
            serial.Serial(self.right_port, baudrate=1_000_000, timeout=0.02),
        ]
        self._opened = True

    def sync_pose(self, current_pose: Sequence[float]) -> None:
        self._last_pose = _normalize_vector(current_pose, self.action_dim, self.name)

    def read(self) -> TeleopSample:
        if not self._opened:
            self.open()
        now = time.monotonic()
        if self._reader is not None:
            raw, hw_clutch = self._reader()
            vec = _normalize_vector(raw, self.action_dim, self.name)
            mapped = tuple(
                vec[i] * self.joint_signs[i] + self.joint_offsets[i] for i in range(14)
            )
            # Clamp normalized grippers (indices 6, 13) to [0.0, 1.0].
            clamped = tuple(
                min(1.0, max(0.0, mapped[i])) if i in (6, 13) else mapped[i] for i in range(14)
            )
            self._last_pose = clamped
            engaged = bool(hw_clutch or self.always_engaged or self.clutch_signal.engaged)
            return TeleopSample(target=clamped, clutch=engaged, timestamp_s=now)
        # Hardware serial path: read newline-delimited JSON / CSV frames if streaming, else hold.
        for idx, drv in enumerate(self._drivers):
            line = drv.readline()
            if not line:
                continue
            decoded = line.decode("utf-8", errors="ignore").strip()
            parts = [float(x) for x in decoded.split(",") if x]
            if len(parts) == 7:
                offset = idx * 7
                cur = list(self._last_pose)
                for j in range(7):
                    val = parts[j] * self.joint_signs[offset + j] + self.joint_offsets[offset + j]
                    cur[offset + j] = min(1.0, max(0.0, val)) if j == 6 else val
                self._last_pose = tuple(cur)
        engaged = bool(self.always_engaged or self.clutch_signal.engaged)
        return TeleopSample(target=self._last_pose, clutch=engaged, timestamp_s=now)

    def close(self) -> None:
        for drv in self._drivers:
            try:
                drv.close()
            except Exception:  # noqa: BLE001
                pass
        self._drivers.clear()
        self._opened = False


def _default_quest_delta_ik(
    base_pose: tuple[float, ...],
    left_delta: Sequence[float],
    right_delta: Sequence[float],
    left_gripper: float,
    right_gripper: float,
) -> tuple[float, ...]:
    """Smooth damped relative-pose mapping from Quest 3S controller deltas to 14-DoF YAM joints.

    Used when no custom analytical IK solver is injected: maps relative (dx, dy, dz, droll,
    dpitch, dyaw) deltas with conservative scaling around ``base_pose`` captured at clutch engage.
    """
    scale = (1.5, 1.5, 1.5, 0.8, 0.8, 0.8)
    out = list(base_pose)
    arms = ((left_delta, left_gripper), (right_delta, right_gripper))
    for arm_idx, (delta, grip) in enumerate(arms):
        off = arm_idx * 7
        for j in range(min(6, len(delta))):
            out[off + j] = float(base_pose[off + j]) + float(delta[j]) * scale[j]
        out[off + 6] = min(1.0, max(0.0, float(grip)))
    return tuple(out)


class Quest3SWebXRAdapter:
    """YAM bimanual Quest 3S WebXR teleop adapter with relative-origin clutch engagement.

    Receives JSON packets over local UDP (default ``127.0.0.1:8765``) or via an injectable
    ``pose_provider`` returning::

        {
            "left": {"pose": [x, y, z, rx, ry, rz], "gripper": 0.0..1.0, "clutch": bool},
            "right": {"pose": [x, y, z, rx, ry, rz], "gripper": 0.0..1.0, "clutch": bool},
        }

    On clutch rising edge, ``sync_pose(current_pose)`` latches the follower's current joint pose
    and the controller's current pose as the relative origin so engaging the Quest grip button
    never causes a motion jump.
    """

    kind = "quest"
    action_dim = 14

    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
        pose_provider: Callable[[], dict[str, Any] | None] | None = None,
        ik_solver: Callable[
            [tuple[float, ...], Sequence[float], Sequence[float], float, float],
            Sequence[float],
        ]
        | None = None,
        clutch_signal: ClutchSignal | None = None,
        always_engaged: bool = False,
        name: str = "yam-quest3s",
    ) -> None:
        self.name = name
        self.host = host
        self.port = int(port)
        self._pose_provider = pose_provider
        self._ik_solver = ik_solver or _default_quest_delta_ik
        self.clutch_signal = clutch_signal or ClutchSignal(engaged=always_engaged)
        self.always_engaged = bool(always_engaged)
        self._sock: socket.socket | None = None
        self._opened = False
        self._base_joint_pose: tuple[float, ...] = (0.0,) * 6 + (1.0,) + (0.0,) * 6 + (1.0,)
        self._origin_left: np.ndarray | None = None
        self._origin_right: np.ndarray | None = None
        self._last_packet: dict[str, Any] | None = None
        self._last_target: tuple[float, ...] = self._base_joint_pose

    def open(self) -> None:
        if self._opened:
            return
        if self._pose_provider is None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.setblocking(False)
            self._sock = sock
        self._opened = True

    def sync_pose(self, current_pose: Sequence[float]) -> None:
        self._base_joint_pose = _normalize_vector(current_pose, self.action_dim, self.name)
        self._last_target = self._base_joint_pose
        self._origin_left = None
        self._origin_right = None

    def _poll_packet(self) -> dict[str, Any] | None:
        if self._pose_provider is not None:
            pkt = self._pose_provider()
            if pkt is not None:
                self._last_packet = pkt
            return self._last_packet
        if self._sock is not None:
            while True:
                try:
                    raw, _ = self._sock.recvfrom(8192)
                except BlockingIOError:
                    break
                try:
                    self._last_packet = json.loads(raw.decode("utf-8"))
                except ValueError:
                    continue
        return self._last_packet

    def read(self) -> TeleopSample:
        if not self._opened:
            self.open()
        now = time.monotonic()
        pkt = self._poll_packet()
        if not pkt:
            return TeleopSample(
                target=self._last_target,
                clutch=bool(self.always_engaged or self.clutch_signal.engaged),
                timestamp_s=now,
            )
        left = pkt.get("left") or {}
        right = pkt.get("right") or {}
        engaged = bool(
            left.get("clutch")
            or right.get("clutch")
            or self.always_engaged
            or self.clutch_signal.engaged
        )
        left_pose = np.asarray(left.get("pose") or [0.0] * 6, dtype=np.float64)
        right_pose = np.asarray(right.get("pose") or [0.0] * 6, dtype=np.float64)
        left_grip = float(left.get("gripper", self._base_joint_pose[6]))
        right_grip = float(right.get("gripper", self._base_joint_pose[13]))

        if not engaged:
            self._origin_left = None
            self._origin_right = None
            return TeleopSample(target=self._last_target, clutch=False, timestamp_s=now)

        if self._origin_left is None or self._origin_right is None:
            self._origin_left = left_pose.copy()
            self._origin_right = right_pose.copy()

        left_delta = (left_pose - self._origin_left).tolist()
        right_delta = (right_pose - self._origin_right).tolist()
        solved = _normalize_vector(
            self._ik_solver(self._base_joint_pose, left_delta, right_delta, left_grip, right_grip),
            self.action_dim,
            self.name,
        )
        self._last_target = solved
        return TeleopSample(target=solved, clutch=True, timestamp_s=now)

    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            except Exception:  # noqa: BLE001
                pass
            self._sock = None
        self._opened = False


class So101LeaderAdapter:
    """SO-101 6-DoF Feetech leader arm adapter (5 calibrated joints in deg + 0..100 gripper)."""

    kind = "so101-leader"
    action_dim = 6

    def __init__(
        self,
        *,
        port: str | None = None,
        calibration_path: str | None = None,
        clutch_signal: ClutchSignal | None = None,
        always_engaged: bool = False,
        reader: Callable[[], tuple[Sequence[float], bool]] | None = None,
        name: str = "so101-leader",
    ) -> None:
        self.name = name
        self.port = port
        self.calibration_path = calibration_path
        self.clutch_signal = clutch_signal or ClutchSignal(engaged=always_engaged)
        self.always_engaged = bool(always_engaged)
        self._reader = reader
        self._bus: Any = None
        self._opened = False
        self._last_pose: tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 50.0)

    def open(self) -> None:
        if self._opened:
            return
        if self._reader is not None:
            self._opened = True
            return
        if not self.port:
            raise RuntimeError(
                "SO-101 leader requires a serial port "
                "(e.g. --teleop so101-leader:port=/dev/ttyACM1)."
            )
        try:
            from lerobot.teleoperators.so_leader import (  # type: ignore[import-not-found]
                SO101Leader,
                SO101LeaderConfig,
            )
        except ImportError as exc:
            raise RuntimeError(
                "SO-101 leader teleop requires the SO-101 extra (`dreamscale robots so101 setup`)."
            ) from exc
        cfg_kwargs: dict[str, Any] = {"port": self.port, "use_degrees": True}
        if self.calibration_path:
            cal = Path(self.calibration_path).expanduser()
            cfg_kwargs["id"] = cal.stem
            cfg_kwargs["calibration_dir"] = cal.parent
        cfg = SO101LeaderConfig(**cfg_kwargs)
        self._bus = SO101Leader(cfg)
        self._bus.connect(calibrate=False)
        self._opened = True

    def sync_pose(self, current_pose: Sequence[float]) -> None:
        self._last_pose = _normalize_vector(current_pose, self.action_dim, self.name)

    def read(self) -> TeleopSample:
        if not self._opened:
            self.open()
        now = time.monotonic()
        if self._reader is not None:
            raw, hw_clutch = self._reader()
            vec = _normalize_vector(raw, self.action_dim, self.name)
            clamped = (*vec[:5], min(100.0, max(0.0, vec[5])))
            self._last_pose = clamped
            engaged = bool(hw_clutch or self.always_engaged or self.clutch_signal.engaged)
            return TeleopSample(target=clamped, clutch=engaged, timestamp_s=now)
        from dreamscale.constants import JOINT_NAMES

        action_dict = self._bus.get_action()
        values = [float(action_dict[f"{joint}.pos"]) for joint in JOINT_NAMES]
        clamped = (*values[:5], min(100.0, max(0.0, values[5])))
        self._last_pose = clamped
        engaged = bool(self.always_engaged or self.clutch_signal.engaged)
        return TeleopSample(target=clamped, clutch=engaged, timestamp_s=now)

    def close(self) -> None:
        if self._bus is not None:
            try:
                self._bus.disconnect()
            except Exception:  # noqa: BLE001
                pass
            self._bus = None
        self._opened = False


class MockTeleopDevice:
    """Deterministic scriptable teleop device for automated tests and simulated live checks."""

    kind = "mock"

    def __init__(
        self,
        samples: Sequence[tuple[Sequence[float], bool]],
        *,
        action_dim: int | None = None,
        name: str = "mock-teleop",
    ) -> None:
        if not samples:
            raise ValueError("MockTeleopDevice requires at least one sample")
        self.name = name
        first_target = tuple(float(v) for v in samples[0][0])
        self.action_dim = int(action_dim or len(first_target))
        self._samples = [
            (_normalize_vector(t, self.action_dim, name), bool(c)) for t, c in samples
        ]
        self._idx = 0
        self.opened = False
        self.closed = False
        self.synced_poses: list[tuple[float, ...]] = []

    def open(self) -> None:
        self.opened = True

    def sync_pose(self, current_pose: Sequence[float]) -> None:
        self.synced_poses.append(_normalize_vector(current_pose, self.action_dim, self.name))

    def read(self) -> TeleopSample:
        idx = min(self._idx, len(self._samples) - 1)
        self._idx += 1
        target, clutch = self._samples[idx]
        return TeleopSample(target=target, clutch=clutch, timestamp_s=time.monotonic())

    def close(self) -> None:
        self.closed = True


def create_teleop_device(
    spec: str,
    *,
    embodiment_name: str,
    always_engaged: bool = False,
) -> TeleopDevice:
    """Parse a CLI ``--teleop`` spec into a concrete ``TeleopDevice``.

    Supported forms:
    - ``gello`` or ``gello:left=/dev/ttyUSB0,right=/dev/ttyUSB1`` (YAM)
    - ``quest`` or ``quest:port=8765`` (YAM Quest 3S WebXR)
    - ``so101-leader`` or ``so101-leader:port=/dev/ttyACM1`` (SO-101)
    """
    raw = spec.strip()
    if not raw:
        raise ValueError("Teleop device spec must not be empty.")
    kind, _, opt_str = raw.partition(":")
    kind = kind.strip().lower()
    opts: dict[str, str] = {}
    if opt_str.strip():
        for part in opt_str.split(","):
            key, sep, val = part.partition("=")
            if not sep:
                raise ValueError(f"Invalid teleop option '{part}'; expected key=value.")
            opts[key.strip().lower()] = val.strip()

    emb = embodiment_name.strip().lower()
    if kind == "gello":
        if emb != "yam":
            raise ValueError(
                f"GELLO teleop is currently supported on YAM, not '{embodiment_name}'."
            )
        return GelloLeaderAdapter(
            left_port=opts.get("left"),
            right_port=opts.get("right"),
            always_engaged=always_engaged,
        )
    if kind in ("quest", "quest3s", "webxr"):
        if emb != "yam":
            raise ValueError(
                f"Quest 3S WebXR teleop is currently supported on YAM, not '{embodiment_name}'."
            )
        return Quest3SWebXRAdapter(
            host=opts.get("host", "127.0.0.1"),
            port=int(opts.get("port", "8765")),
            always_engaged=always_engaged,
        )
    if kind in ("so101-leader", "so101", "leader"):
        if emb != "so101":
            raise ValueError(
                f"SO-101 leader teleop is supported on SO-101, not '{embodiment_name}'."
            )
        return So101LeaderAdapter(
            port=opts.get("port"),
            calibration_path=opts.get("calibration"),
            always_engaged=always_engaged,
        )
    raise ValueError(
        f"Unknown teleop device '{kind}'. Supported: gello, quest, so101-leader."
    )
