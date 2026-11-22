"""
Retargeting: a person's motion at a teleop console - a headset's hand or controller, a gamepad, a keyboard - turned into
the robot's joint positions, on the robot, which is where the arm and its limits are known.

    chain = sequence_ai.retarget.Chain.from_urdf("arm.urdf", "base_link", "gripper_link")
    arm_user = sequence_ai.retarget.Arm(chain, hand="right", workspace=([0.1, -0.4, 0.02], [0.6, 0.4, 0.5]))
    out_user = arm_user.step(inputs_user, q_now_user, dt=1 / 30)     # each time the console's newest inputs come
    # out_user.q: the joint positions to command; out_user.gripper: 0 open .. 1 closed, None: leave it;
    # out_user.why: "following", or why the arm holds ("clutch open", "hand lost", "stale", "deadman open")

In one sentence: the console sends its raw inputs as it reads them, the newest alone counting → Arm.step(inputs, q, dt)
→ nothing moves until the clutch closes (a controller's squeeze, or a hand's thumb to its middle finger), which anchors
the hand where it is and the arm's tip where it is → from then the hand's motion since the anchor, turned into the
robot's axes and scaled, moves the tip from where it was, kept inside the workspace and under the tip's top speed and
turn rate → its joints by inverse kinematics on the arm's URDF, each under its top speed → the gripper from the
trigger or the thumb-to-index pinch. Twist does the same from a gamepad's sticks or keys held with a deadman, as the
tip's velocity.

WHY each rule: a person whose hand drifts while they look away must not drive the arm (the clutch); a hand the headset
lost is no command, and one coming back - or a hand taken up for a controller - must not jump the arm to where it
appeared (holding, and a new anchor); a
pose the console sent a while ago is no longer the person's (stale_s); and a fast hand, or a target past the arm's
reach, is followed at the speed the arm is allowed, never in one step. The robot's own stop when its driving console
goes quiet for 3 s stays as it is.


The inputs, as the console sends them - and as a recording keeps them, so another retargeting can make the actions
again from the same motion:

    {"t": 1732140000.123,                          # the console's clock when it read them, in seconds
     "head": {"p": [x, y, z], "q": [x, y, z, w]},  # positions in metres, quaternions x, y, z, w
     "right": {"kind": "controller",               # or "hand"
               "p": [...], "q": [...],             # its grip pose
               "squeeze": 0.0, "trigger": 0.0,     # a controller's grip button and trigger, 0 .. 1
               "joints": [[x, y, z], ...],         # a hand's 25 joints in WebXR's order (wrist, thumb, index ...)
               "tracked": true},
     "left": {...},
     "pad": {"axes": [...], "buttons": [...]},     # a gamepad, the standard mapping: buttons as their values 0 .. 1
     "keys": ["w", "shift"]}                       # the keys held

in WebXR's reference space (x right, y up, -z forward); `axes` turns that into the robot's base (x forward, y left,
z up, as most arms' URDFs are written).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from sequence_ai._core.urdf_chain import Chain, axis_angle, rotation_error

__all__ = ["Arm", "Chain", "Hand", "Step", "Twist", "XR_TO_ROBOT", "pose_matrix", "xr_to_mano21"]


XR_TO_ROBOT = np.array([[0.0, 0.0, -1.0], [-1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

WRIST, THUMB_TIP, INDEX_TIP, MIDDLE_TIP = 0, 4, 9, 14


def pose_matrix(p: Any, q: Any) -> np.ndarray:
    """A 4x4 transform from a position [x, y, z] and a quaternion [x, y, z, w]."""
    x, y, z, w = (float(v) for v in q)
    n = math.sqrt(x * x + y * y + z * z + w * w) or 1.0
    x, y, z, w = x / n, y / n, z / n, w / n
    t = np.eye(4)
    t[:3, :3] = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                 [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                 [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    t[:3, 3] = [float(v) for v in p]
    return t


@dataclass
class Step:
    """What one step of retargeting gives: the joint positions to command, the gripper (0 open .. 1 closed; None:
    leave it as it is), whether the arm follows the person now, why (or why not), and the tip pose it aimed at."""

    q: np.ndarray
    gripper: float | None
    following: bool
    why: str
    target: np.ndarray | None = None


def _joint_position(side: dict, i: int) -> np.ndarray | None:
    joints = side.get("joints")
    if not isinstance(joints, (list, tuple)) or len(joints) <= i:
        return None
    return np.asarray(joints[i][:3], dtype=float)


def _pinch(side: dict, a: int, b: int) -> float | None:
    pa, pb = _joint_position(side, a), _joint_position(side, b)
    return None if pa is None or pb is None else float(np.linalg.norm(pa - pb))


class _Limited:
    """The rules both retargetings share: a target the workspace and the top speeds hold, solved by the chain."""

    def __init__(self, chain: Chain, *, workspace: Any = None, max_speed: float = 0.5, max_turn: float = 2.0,
                 max_joint_speed: float = 2.0, stale_s: float = 0.25, orientation: bool = True,
                 ik_iters: int = 25) -> None:
        self.chain = chain



        self.ik_iters = ik_iters
        self.workspace = None if workspace is None else (np.asarray(workspace[0], float),
                                                         np.asarray(workspace[1], float))
        self.max_speed, self.max_turn, self.max_joint_speed = max_speed, max_turn, max_joint_speed
        self.stale_s, self.orientation = stale_s, orientation
        self._target: np.ndarray | None = None

    def reset(self) -> None:
        """Forget where it aimed: the next step starts from where the arm is."""
        self._target = None

    def _hold(self, q_now: np.ndarray, why: str) -> Step:
        self.reset()
        return Step(np.asarray(q_now, float).copy(), None, False, why)

    def _stale(self, inputs: dict, now: float | None) -> bool:
        t = inputs.get("t")
        return now is not None and isinstance(t, (int, float)) and now - float(t) > self.stale_s

    def _reach(self, want: np.ndarray, q_now: np.ndarray, dt: float, gripper: float | None) -> Step:
        """`want` held inside the workspace, moved from the last target at the top speed and turn rate at most,
        solved for the joints, each moved at its top speed at most."""
        want = want.copy()
        if self.workspace is not None:
            want[:3, 3] = np.clip(want[:3, 3], self.workspace[0], self.workspace[1])
        last = self._target if self._target is not None else self.chain.fk(q_now)
        d = want[:3, 3] - last[:3, 3]
        most = self.max_speed * dt
        if np.linalg.norm(d) > most:
            want[:3, 3] = last[:3, 3] + d / np.linalg.norm(d) * most
        turn = rotation_error(last[:3, :3], want[:3, :3])
        if np.linalg.norm(turn) > self.max_turn * dt:
            angle = self.max_turn * dt
            want[:3, :3] = axis_angle(turn / np.linalg.norm(turn), angle) @ last[:3, :3]
        self._target = want
        q, ok = self.chain.ik(want, q_now, orientation=self.orientation, iters=self.ik_iters)
        step = self.max_joint_speed * dt
        q = self.chain.clip(q_now + np.clip(q - q_now, -step, step))
        return Step(q, gripper, True, "following" if ok else "out of reach", want)


class Arm(_Limited):
    """A headset's hand or controller driving an arm's tip, held: see the module's words.

    hand: "right" or "left". axes: the 3x3 turning the console's axes into the robot base's (XR_TO_ROBOT, or that
    times a turn where the person does not face the robot's x). scale: the tip's motion for the hand's (0.5: half).
    workspace: ([x, y, z] low, [x, y, z] high) in the base, metres, or None. max_speed (m/s) and max_turn (rad/s): the
    tip's; max_joint_speed (rad/s, or m/s for a prismatic joint): each joint's. stale_s: how old a pose may be at
    `now`. orientation: follow the hand's turning too, or its position alone. squeeze_at: a controller's grip value
    that closes the clutch; clutch_pinch_m: a hand's thumb-to-middle distance that does. grip_open_m, grip_closed_m:
    the thumb-to-index distances that read as an open and a closed gripper."""

    def __init__(self, chain: Chain, *, hand: str = "right", axes: Any = XR_TO_ROBOT, scale: float = 1.0,
                 workspace: Any = None, max_speed: float = 0.5, max_turn: float = 2.0, max_joint_speed: float = 2.0,
                 stale_s: float = 0.25, orientation: bool = True, squeeze_at: float = 0.5,
                 clutch_pinch_m: float = 0.025, grip_open_m: float = 0.08, grip_closed_m: float = 0.02,
                 ik_iters: int = 25) -> None:
        if hand not in ("right", "left"):
            raise ValueError(f'hand is "right" or "left", not {hand!r}')
        super().__init__(chain, workspace=workspace, max_speed=max_speed, max_turn=max_turn,
                         max_joint_speed=max_joint_speed, stale_s=stale_s, orientation=orientation, ik_iters=ik_iters)
        self.hand, self.axes, self.scale = hand, np.asarray(axes, float), float(scale)
        self.squeeze_at, self.clutch_pinch_m = squeeze_at, clutch_pinch_m
        self.grip_open_m, self.grip_closed_m = grip_open_m, grip_closed_m
        self._anchor: tuple[np.ndarray, np.ndarray, Any] | None = None

    def reset(self) -> None:
        super().reset()
        self._anchor = None

    def clutch(self, side: dict) -> bool:
        """Whether this side holds the clutch: a controller's squeeze, a hand's thumb on its middle finger."""
        if side.get("kind") == "hand":
            d = _pinch(side, THUMB_TIP, MIDDLE_TIP)
            return d is not None and d < self.clutch_pinch_m
        return float(side.get("squeeze") or 0.0) >= self.squeeze_at

    def gripper(self, side: dict) -> float | None:
        """0 open .. 1 closed: a controller's trigger, a hand's thumb-to-index pinch; None where it says neither."""
        if side.get("kind") == "hand":
            d = _pinch(side, THUMB_TIP, INDEX_TIP)
            if d is None:
                return None
            return float(np.clip((self.grip_open_m - d) / (self.grip_open_m - self.grip_closed_m), 0.0, 1.0))
        return None if side.get("trigger") is None else float(np.clip(float(side["trigger"]), 0.0, 1.0))

    def step(self, inputs: dict, q_now: Any, dt: float, now: float | None = None) -> Step:
        """One step: the joint positions for the console's newest `inputs`, from the arm's `q_now`, `dt` seconds after
        the last step; `now` on the console's clock, to tell a stale pose."""
        q_now = np.asarray(q_now, float)
        if self._stale(inputs, now):
            return self._hold(q_now, "stale")
        side = inputs.get(self.hand)
        if not isinstance(side, dict) or side.get("tracked") is False or "p" not in side or "q" not in side:
            return self._hold(q_now, "hand lost")
        if not self.clutch(side):
            return self._hold(q_now, "clutch open")
        hand = pose_matrix(side["p"], side["q"])
        if self._anchor is not None and self._anchor[2] != side.get("kind"):


            self.reset()
        if self._anchor is None:
            self._anchor = (hand, self.chain.fk(q_now), side.get("kind"))
        hand0, tip0, _ = self._anchor
        want = np.eye(4)
        want[:3, 3] = tip0[:3, 3] + self.axes @ (hand[:3, 3] - hand0[:3, 3]) * self.scale
        turned = self.axes @ (hand[:3, :3] @ hand0[:3, :3].T) @ self.axes.T
        want[:3, :3] = turned @ tip0[:3, :3]
        return self._reach(want, q_now, dt, self.gripper(side))



LX, LY, RX, RY = 0, 1, 2, 3
LB, RB, LT, RT = 4, 5, 6, 7

KEYS = {"w": (0, 1.0), "s": (0, -1.0), "a": (1, 1.0), "d": (1, -1.0), "r": (2, 1.0), "f": (2, -1.0),
        "q": (3, 1.0), "e": (3, -1.0)}


class Twist(_Limited):
    """A gamepad's sticks, or keys, as the tip's velocity in the robot's base while the deadman is held - a pad's left
    shoulder button, or the shift key. The left stick moves forward and sideways, the right stick up and down and
    turns about z; on keys w/s, a/d, r/f and q/e. The gripper: the right trigger closes it as far as it is pressed,
    or c closes and v opens. speed (m/s) and turn (rad/s): at a full stick or a key held. orientation: hold the tip's
    turn as it was (and turn it on q/e and the right stick), or move its position alone - for an arm whose joints cannot
    turn its tip every way, as an arm of fewer than six cannot."""

    def __init__(self, chain: Chain, *, speed: float = 0.15, turn: float = 0.8, dead_zone: float = 0.1,
                 workspace: Any = None, max_joint_speed: float = 2.0, stale_s: float = 0.25,
                 orientation: bool = True) -> None:
        super().__init__(chain, workspace=workspace, max_speed=speed, max_turn=turn, max_joint_speed=max_joint_speed,
                         stale_s=stale_s, orientation=orientation)
        self.speed, self.turn, self.dead_zone = speed, turn, dead_zone

    def _velocity(self, inputs: dict) -> tuple[np.ndarray, bool, float | None]:
        """(vx, vy, vz, yaw rate) as fractions of the top speed, whether the deadman is held, and the gripper."""
        v = np.zeros(4)
        keys = {str(k).lower() for k in inputs.get("keys") or ()}
        pad = inputs.get("pad") or {}
        axes = [float(a) for a in pad.get("axes") or ()]
        buttons = [float(b) for b in pad.get("buttons") or ()]
        held = "shift" in keys or (len(buttons) > LB and buttons[LB] >= 0.5)
        for key, (i, sign) in KEYS.items():
            if key in keys:
                v[i] += sign

        def stick(i: int) -> float:
            a = axes[i] if len(axes) > i else 0.0
            return 0.0 if abs(a) < self.dead_zone else a


        v += [-stick(LY), -stick(LX), -stick(RY), -stick(RX)]
        gripper = None
        if len(buttons) > RT and pad:
            gripper = float(np.clip(buttons[RT], 0.0, 1.0))
        if "c" in keys:
            gripper = 1.0
        elif "v" in keys:
            gripper = 0.0
        return np.clip(v, -1.0, 1.0), held, gripper

    def step(self, inputs: dict, q_now: Any, dt: float, now: float | None = None) -> Step:
        q_now = np.asarray(q_now, float)
        if self._stale(inputs, now):
            return self._hold(q_now, "stale")
        v, held, gripper = self._velocity(inputs)
        if not held:
            return self._hold(q_now, "deadman open")
        last = self._target if self._target is not None else self.chain.fk(q_now)
        want = last.copy()
        want[:3, 3] = last[:3, 3] + v[:3] * self.speed * dt
        if v[3]:
            want[:3, :3] = axis_angle(np.array([0.0, 0.0, 1.0]), v[3] * self.turn * dt) @ last[:3, :3]
        return self._reach(want, q_now, dt, gripper)




MANO21_FROM_XR25 = (0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24)





OPERATOR2MANO = {"right": np.array([[0.0, 0.0, -1.0], [-1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
                 "left": np.array([[0.0, 0.0, -1.0], [1.0, 0.0, 0.0], [0.0, -1.0, 0.0]])}


def _palm_axes(points: np.ndarray) -> np.ndarray:
    """The palm's axes as columns, from MANO's wrist (0), index base (5) and middle base (9): x from the middle base to
    the wrist, y normal to the three, z = x × y turned toward the index finger."""
    wrist, index, middle = points[0], points[5], points[9]
    three = np.stack([wrist, index, middle])
    normal = np.linalg.svd(three - three.mean(axis=0))[2][2]
    x = (wrist - middle) - ((wrist - middle) @ normal) * normal
    x = x / np.linalg.norm(x)
    z = np.cross(x, normal)
    if z @ (index - middle) < 0:
        normal, z = -normal, -z
    return np.stack([x, normal, z], axis=1)


def xr_to_mano21(joints: Any, hand: str | None = None) -> np.ndarray:
    """A WebXR hand's 25 joint positions as MANO's 21 keypoints (21 x 3), relative to the wrist. With `hand` ("right"
    or "left"), in MANO's axes for that hand as well - what dex-retargeting's configs are written in - the same
    whichever way the hand faces."""
    p = np.asarray([j[:3] for j in joints], dtype=float)
    if p.shape != (25, 3):
        raise ValueError(f"a WebXR hand has 25 joints of [x, y, z, ...]; these are {p.shape[0]}")
    points = p[list(MANO21_FROM_XR25)] - p[WRIST]
    if hand is None:
        return points
    if hand not in OPERATOR2MANO:
        raise ValueError(f'hand is "right" or "left", not {hand!r}')
    return points @ _palm_axes(points) @ OPERATOR2MANO[hand]


class Hand:
    """A dexterous hand driven by the person's hand, through dex-retargeting (pip install dex-retargeting torch six:
    its 0.5.0 imports both without installing them, and a CPU torch will do), from its config file for that hand:
    step(inputs) gives the hand's joint positions, or None where the hand was lost."""

    def __init__(self, config_path: str, *, hand: str = "right") -> None:
        if hand not in OPERATOR2MANO:
            raise ValueError(f'hand is "right" or "left", not {hand!r}')
        try:
            from dex_retargeting.retargeting_config import RetargetingConfig
        except ImportError as exc:
            from sequence_ai.errors import MissingPackage

            if (exc.name or "").split(".")[0] == "dex_retargeting":
                raise MissingPackage("a dexterous hand is retargeted by dex-retargeting, which is not installed",
                                     hint="pip install dex-retargeting torch six") from None

            raise MissingPackage(f"dex-retargeting is installed but does not load: {exc}",
                                 hint="pip install dex-retargeting torch six") from exc
        self.hand = hand
        self.retargeting = RetargetingConfig.load_from_file(config_path).build()

    def step(self, inputs: dict) -> np.ndarray | None:
        side = inputs.get(self.hand)
        if not isinstance(side, dict) or side.get("tracked") is False or not side.get("joints"):
            return None
        points = xr_to_mano21(side["joints"], self.hand)
        cfg = self.retargeting.optimizer
        idx = cfg.target_link_human_indices
        ref = points[idx[1], :] - points[idx[0], :] if idx.ndim == 2 else points[idx, :]
        return np.asarray(self.retargeting.retarget(ref))
