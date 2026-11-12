"""Anvil's control stack on a Devbox, as the OpenARM rig reads and commands it.

The stack publishes every follower joint on /joint_states (by name, in no promised order),
takes each arm's targets on its forward position controller (joint 1 to joint 7, then the
gripper in metres) and publishes each camera as compressed images. It enforces almost no
limits on what a program commands; OpenArmRig does.
"""

from __future__ import annotations

import base64
import io
import threading
import time
import xml.etree.ElementTree as ElementTree
from collections import deque
from dataclasses import dataclass

import numpy as np

from dreamscale.hardware.rig import RigFault

from .camera_sources import CameraError, FrameUnavailable, RGBFrame
from .openarm_config import ARMS, CAMERAS, DEFAULT_URL, JOINTS
from .openarm_ros import RosBridge, RosBridgeError

SIDES = {"left": "l", "right": "r"}
JOINT_STATES = "/joint_states"
ROBOT_DESCRIPTION = "/robot_description"
# Anvil's documented gripper command range in metres: closed with squeeze force, to open.
GRIPPER_RANGE = (-0.003, 0.05)
# Kept clear of each joint's hard stop.
LIMIT_MARGIN = 0.01
INFERENCE_CONFIG = "config/openarm_v2_inference.yaml"
START_STACK = (
    "Start Anvil's control stack on the Devbox with the inference config "
    f"(ARMS_CONTROL_CONFIG_FILE={INFERENCE_CONFIG} in .env.config), then run this again."
)


class StackError(RigFault):
    """The stack can't be reached, or what it reports can't be commanded safely."""


def joint_names(arm) -> tuple[str, ...]:
    """An arm's joints as the stack names them, in the order its controller takes them."""
    side = SIDES[arm]
    return (
        *(f"follower_{side}_joint{i}" for i in range(1, JOINTS + 1)),
        f"follower_{side}_finger_joint1",
    )


def controller_name(arm) -> str:
    return f"follower_{SIDES[arm]}_forward_position_controller"


def command_topic(arm) -> str:
    return f"/{controller_name(arm)}/commands"


def camera_topic(camera) -> str:
    return f"/cam_{camera}/image_raw/compressed"


@dataclass(frozen=True)
class ArmState:
    """One arm's joints then its gripper, as measured, in the controller's order."""

    position: np.ndarray
    velocity: np.ndarray
    monotonic_ns: int

    def validate(self, max_age_s: float) -> ArmState:
        if not np.isfinite(self.position).all() or not np.isfinite(self.velocity).all():
            raise StackError("The stack reported a joint state that isn't a number.")
        age = (time.monotonic_ns() - self.monotonic_ns) / 1e9
        if age > max_age_s:
            raise StackError(
                f"Joint states stopped arriving {age:.1f} s ago. Check Anvil's control stack."
            )
        return self


def parse_limits(urdf: str, arm) -> np.ndarray:
    """An arm's command range from the stack's robot description, in the controller's order:
    each joint's own limits less a margin, then the gripper's documented range."""
    try:
        root = ElementTree.fromstring(urdf)
    except ElementTree.ParseError as exc:
        raise StackError(f"The stack's robot description isn't readable: {exc}") from exc
    # The robot's own joints only: ros2_control and transmission blocks name them again,
    # without limits.
    joints = {joint.get("name"): joint for joint in root.findall("joint")}
    rows = []
    for name in joint_names(arm)[:JOINTS]:
        limit = joints[name].find("limit") if name in joints else None
        try:
            lower, upper = float(limit.get("lower")), float(limit.get("upper"))
        except (AttributeError, TypeError, ValueError):
            lower = upper = float("nan")
        if not np.isfinite([lower, upper]).all() or upper - lower <= 4 * LIMIT_MARGIN:
            raise StackError(
                f"The stack's robot description gives no usable limits for {name}, so "
                "targets can't be checked."
            )
        rows.append((lower + LIMIT_MARGIN, upper - LIMIT_MARGIN))
    rows.append(GRIPPER_RANGE)
    return np.asarray(rows, dtype=float)


class AnvilStack:
    """The stack's joint states, camera frames, limits and command topics over rosbridge."""

    def __init__(self, url=DEFAULT_URL, *, bridge_factory=RosBridge, state_period_ms=0,
                 camera_period_ms=33, timeout_s=5.0, description_timeout_s=3.0):
        self.url, self.bridge_factory = url, bridge_factory
        self.state_period_ms, self.camera_period_ms = state_period_ms, camera_period_ms
        self.timeout_s, self.description_timeout_s = timeout_s, description_timeout_s
        self.bridge = None
        self._lock = threading.Lock()
        self._joints = {}             # name -> (position, velocity, monotonic_ns)
        self._frames = {}             # camera -> (encoded, wall_ns, monotonic_ns, sequence)
        self._decoded = {}            # camera -> RGBFrame of the newest decoded sequence
        self._arrivals = {}           # topic -> recent arrival times, monotonic seconds
        self._description = None      # the URDF, or the StackError reading it raised
        self._described = threading.Event()
        self._urdf = None

    # -- lifecycle ---------------------------------------------------------------------

    def open(self, *, cameras=(), command=()) -> AnvilStack:
        """Connect and subscribe; ``command`` names the arms this connection will command."""
        if self.bridge is not None:
            raise StackError("Already connected to the stack.")
        try:
            self.bridge = self.bridge_factory(self.url).open()
            # Unthrottled: a throttle keeps one message per window, which could be the same
            # arm's every time if each arm's joints come in their own message.
            self.bridge.subscribe(
                JOINT_STATES, "sensor_msgs/msg/JointState", self._on_joints,
                throttle_ms=self.state_period_ms,
            )
            for camera in cameras:
                self.bridge.subscribe(
                    camera_topic(camera), "sensor_msgs/msg/CompressedImage",
                    lambda msg, camera=camera: self._on_frame(camera, msg),
                    throttle_ms=self.camera_period_ms,
                )
            for arm in command:
                self.bridge.advertise(command_topic(arm), "std_msgs/msg/Float64MultiArray")
        except RosBridgeError as exc:
            self.close()
            raise StackError(f"{exc} {START_STACK}") from exc
        return self

    def close(self):
        bridge, self.bridge = self.bridge, None
        if bridge is not None:
            bridge.close()

    @property
    def alive(self) -> bool:
        return self.bridge is not None and self.bridge.alive

    def _require(self) -> RosBridge:
        if not self.alive:
            raise StackError("The connection to Anvil's control stack closed.")
        return self.bridge

    # -- subscriptions -----------------------------------------------------------------

    def _arrived(self, topic):
        self._arrivals.setdefault(topic, deque(maxlen=600)).append(time.monotonic())

    def _on_joints(self, msg):
        names, positions = msg.get("name") or [], msg.get("position") or []
        velocities = msg.get("velocity") or []
        if len(positions) != len(names):
            return
        stamp = time.monotonic_ns()

        def number(values, i, missing):
            # The bridge writes NaN as null: an unknown position stays one (and is refused),
            # an unknown velocity reads as still.
            value = values[i] if i < len(values) else None
            return float(value) if value is not None else missing

        joints = {
            name: (number(positions, i, float("nan")), number(velocities, i, 0.0), stamp)
            for i, name in enumerate(names)
        }
        with self._lock:
            # Broadcasters may publish their joints in separate messages: each joint keeps
            # its own arrival time, so one that stops is seen to stop.
            self._joints.update(joints)
            self._arrived(JOINT_STATES)

    def _on_frame(self, camera, msg):
        data = msg.get("data")
        if not data:
            return
        with self._lock:
            sequence = self._frames[camera][3] + 1 if camera in self._frames else 0
            self._frames[camera] = (data, time.time_ns(), time.monotonic_ns(), sequence)
            self._arrived(camera_topic(camera))

    def _on_description(self, msg):
        if msg.get("data"):
            self._urdf = msg["data"]
            self._described.set()

    # -- reads -------------------------------------------------------------------------

    def joints_seen(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(self._joints)

    def arms_present(self) -> tuple[str, ...]:
        seen = set(self.joints_seen())
        return tuple(arm for arm in ARMS if set(joint_names(arm)) <= seen)

    def arm_state(self, arm, max_age_s=0.25) -> ArmState:
        self._require()
        with self._lock:
            joints = dict(self._joints)
        names = joint_names(arm)
        missing = [name for name in names if name not in joints]
        if not joints:
            raise StackError(f"No joint states from the stack yet. {START_STACK}")
        if missing:
            raise StackError(
                f"The stack reports no {arm} arm (no {missing[0]} in {JOINT_STATES})."
            )
        return ArmState(
            position=np.array([joints[name][0] for name in names]),
            velocity=np.array([joints[name][1] for name in names]),
            monotonic_ns=min(joints[name][2] for name in names),
        ).validate(max_age_s)

    def wait_for_arms(self, arms, *, timeout_s=None, max_age_s=0.25):
        """Every arm's first fresh state, within one deadline."""
        deadline = time.monotonic() + (self.timeout_s if timeout_s is None else timeout_s)
        while True:
            try:
                return {arm: self.arm_state(arm, max_age_s) for arm in arms}
            except StackError:
                if not self.alive or time.monotonic() > deadline:
                    raise
            time.sleep(0.02)

    def latest(self, camera, max_age_s=1.0) -> RGBFrame:
        """A camera's newest frame, decoded once: the cameras interface the rigs share."""
        self._require()
        with self._lock:
            encoded = self._frames.get(camera)
            decoded = self._decoded.get(camera)
        if encoded is None:
            raise FrameUnavailable(f"No frames on {camera_topic(camera)} yet.")
        data, wall_ns, monotonic_ns, sequence = encoded
        if decoded is None or decoded.sequence != sequence:
            from PIL import Image

            try:
                raw = base64.b64decode(data) if isinstance(data, str) else bytes(data)
                rgb = np.asarray(Image.open(io.BytesIO(raw)).convert("RGB"))
            except Exception as exc:
                raise CameraError(f"{camera_topic(camera)} sent an unreadable image.") from exc
            decoded = RGBFrame(rgb, wall_ns, monotonic_ns, sequence)
            with self._lock:
                self._decoded[camera] = decoded
        return decoded.validate(max_age_s)

    def rate(self, topic, window_s=2.0) -> tuple[float, float] | None:
        """(messages per second, 95th percentile gap in seconds) over the last window_s;
        None with fewer than two messages in it."""
        now = time.monotonic()
        with self._lock:
            arrivals = [t for t in self._arrivals.get(topic, ()) if now - t <= window_s]
        if len(arrivals) < 2:
            return None
        gaps = np.diff(arrivals)
        return (len(gaps) / float(arrivals[-1] - arrivals[0]), float(np.percentile(gaps, 95)))

    # -- the graph ---------------------------------------------------------------------

    def robot_description(self) -> str:
        """The stack's URDF: its latched topic, else robot_state_publisher's parameter. Asked
        once per connection."""
        if self._description is None:
            self._description = self._read_description()
        if isinstance(self._description, StackError):
            raise self._description
        return self._description

    def _read_description(self):
        bridge, timeout_s = self._require(), self.description_timeout_s
        try:
            bridge.subscribe(ROBOT_DESCRIPTION, "std_msgs/msg/String", self._on_description)
            self._described.wait(timeout_s)
            bridge.unsubscribe(ROBOT_DESCRIPTION)
            if self._urdf is None:
                values = bridge.call(
                    "/robot_state_publisher/get_parameters", {"names": ["robot_description"]},
                    type="rcl_interfaces/srv/GetParameters", timeout_s=timeout_s,
                ).get("values") or [{}]
                self._urdf = values[0].get("string_value") or None
        except RosBridgeError as exc:
            return StackError(f"The stack's robot description can't be read: {exc}")
        if self._urdf is None:
            return StackError(
                "The stack publishes no robot description, so joint limits can't be read."
            )
        return self._urdf

    def limits(self, arm) -> np.ndarray:
        return parse_limits(self.robot_description(), arm)

    def services(self) -> list[str]:
        try:
            return list(self._require().call("/rosapi/services").get("services") or [])
        except RosBridgeError:
            return []

    def topics(self) -> list[str]:
        try:
            return list(self._require().call("/rosapi/topics").get("topics") or [])
        except RosBridgeError:
            return []

    def publishers(self, topic) -> list[str] | None:
        """The nodes publishing a topic; None when the stack doesn't say."""
        try:
            return list(
                self._require().call("/rosapi/publishers", {"topic": topic}).get("publishers")
                or []
            )
        except RosBridgeError:
            return None

    def controllers(self) -> dict[str, str]:
        """Every ros2_control controller's state, by name."""
        bridge = self._require()
        managers = [s for s in self.services() if s.endswith("/list_controllers")]
        found = {}
        for service in managers or ["/controller_manager/list_controllers"]:
            try:
                listed = bridge.call(
                    service, type="controller_manager_msgs/srv/ListControllers", timeout_s=3.0,
                ).get("controller") or []
            except RosBridgeError:
                continue
            found.update({c.get("name"): c.get("state") for c in listed})
        return found

    def cameras_present(self) -> tuple[str, ...] | None:
        """The cell's cameras the stack publishes; None when it doesn't list its topics."""
        topics = set(self.topics())
        if not topics:
            return None
        return tuple(camera for camera in CAMERAS if camera_topic(camera) in topics)

    # -- commands ----------------------------------------------------------------------

    def command(self, arm, values):
        """An arm's absolute targets: joint 1 to joint 7 in radians, then the gripper in
        metres. The caller has validated them."""
        self._require().publish(command_topic(arm), {
            "layout": {"dim": [], "data_offset": 0},
            "data": [float(v) for v in values],
        })
