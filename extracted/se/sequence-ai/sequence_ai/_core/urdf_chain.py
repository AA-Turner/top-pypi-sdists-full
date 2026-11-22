"""
A robot arm's kinematic chain read from its URDF, for teleoperation's retargeting (sequence_ai.retarget): the joints
from a base link to a tip link, where the tip is at given joint positions (forward kinematics), the Jacobian, and the
joint positions that put the tip at a pose (inverse kinematics by damped least squares, each joint inside its limits).

In one sentence: Chain.from_urdf(urdf, base, tip) → the joints that lead from base to tip, in order, each with its fixed
origin, its axis, its kind and its limits → fk(q) multiplies each origin and each joint's motion along the chain →
jacobian(q) is the geometric one, each movable joint's angular and linear velocity at the tip → ik(target, q0) steps
q by Jᵀ(JJᵀ + λ²I)⁻¹e, e the tip's error in position and orientation, clipped to the limits, until the error is inside
its tolerance or the steps run out.

WHY its own and not a library's: numpy is what sequence-ai installs, and a chain of revolute and prismatic joints is a
few dozen lines; a library that also reads meshes, inertias and collision shapes would be a dependency for what
retargeting never reads.
"""
from __future__ import annotations

import math
import pathlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

import numpy as np

KINDS = ("revolute", "continuous", "prismatic", "fixed")


def rpy_matrix(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """The rotation URDF writes as rpy: about x by roll, then y by pitch, then z by yaw (fixed axes), Rz·Ry·Rx."""
    cr, sr, cp, sp = math.cos(roll), math.sin(roll), math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    return np.array([[cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
                     [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
                     [-sp, cp * sr, cp * cr]])


def axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
    """The rotation by `angle` about the unit vector `axis` (Rodrigues)."""
    x, y, z = axis
    c, s, t = math.cos(angle), math.sin(angle), 1.0 - math.cos(angle)
    return np.array([[t * x * x + c, t * x * y - s * z, t * x * z + s * y],
                     [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
                     [t * x * z - s * y, t * y * z + s * x, t * z * z + c]])


def rotation_error(current: np.ndarray, target: np.ndarray) -> np.ndarray:
    """The rotation vector (axis times angle, in the base frame) that turns `current` into `target`."""
    r = target @ current.T
    cos = max(-1.0, min(1.0, (np.trace(r) - 1.0) / 2.0))
    angle = math.acos(cos)
    if angle < 1e-9:
        return np.zeros(3)
    if math.pi - angle < 1e-6:

        k = int(np.argmax(np.diag(r)))
        v = (r[:, k] + np.eye(3)[:, k]) / math.sqrt(2.0 * (1.0 + r[k, k]))
        return v / np.linalg.norm(v) * angle
    w = np.array([r[2, 1] - r[1, 2], r[0, 2] - r[2, 0], r[1, 0] - r[0, 1]])
    return w / (2.0 * math.sin(angle)) * angle


def _origin(el: ET.Element | None) -> np.ndarray:
    t = np.eye(4)
    if el is None:
        return t
    xyz = [float(v) for v in (el.get("xyz") or "0 0 0").split()]
    rpy = [float(v) for v in (el.get("rpy") or "0 0 0").split()]
    t[:3, :3] = rpy_matrix(*rpy)
    t[:3, 3] = xyz
    return t


@dataclass
class Joint:
    """One URDF joint of the chain: its fixed origin in its parent link, its axis in its own frame, its kind, and its
    limits (radians or metres; ±inf where it has none: a continuous joint)."""

    name: str
    kind: str
    origin: np.ndarray
    axis: np.ndarray = field(default_factory=lambda: np.array([1.0, 0.0, 0.0]))
    lower: float = -math.inf
    upper: float = math.inf

    def motion(self, q: float) -> np.ndarray:
        """The joint's own motion at position q, as a transform."""
        t = np.eye(4)
        if self.kind in ("revolute", "continuous"):
            t[:3, :3] = axis_angle(self.axis, q)
        elif self.kind == "prismatic":
            t[:3, 3] = self.axis * q
        return t


class Chain:
    """The joints from a base link to a tip link (fixed ones included, in order), and the movable ones' count, `dof`."""

    def __init__(self, joints: list[Joint], tip_offset: np.ndarray | None = None) -> None:
        self.joints = joints
        self.movable = [j for j in joints if j.kind != "fixed"]
        self.dof = len(self.movable)

        self.tip_offset = np.eye(4) if tip_offset is None else tip_offset
        self.lower = np.array([j.lower for j in self.movable])
        self.upper = np.array([j.upper for j in self.movable])

    @classmethod
    def from_urdf(cls, urdf: str | pathlib.Path, base: str, tip: str, *, tip_offset: np.ndarray | None = None) -> Chain:
        """The chain from link `base` to link `tip` of a URDF - its text, or a path to its file. A link the URDF has
        no way to from `base` raises ValueError, naming the links it does have."""
        text = urdf
        if isinstance(urdf, pathlib.Path) or (isinstance(urdf, str) and not urdf.lstrip().startswith("<")):
            text = pathlib.Path(urdf).read_text()
        root = ET.fromstring(text)
        by_child: dict[str, ET.Element] = {}
        links = [el.get("name") for el in root.findall("link")]
        for el in root.findall("joint"):
            child = el.find("child")
            if child is not None:
                by_child[child.get("link")] = el
        path: list[ET.Element] = []
        at = tip
        while at != base:
            el = by_child.get(at)
            if el is None:
                raise ValueError(f"no chain from {base!r} to {tip!r} in this URDF: its links are {', '.join(links)}")
            path.append(el)
            at = el.find("parent").get("link")
        joints = []
        for el in reversed(path):
            kind = el.get("type") or "fixed"
            if kind not in KINDS:
                raise ValueError(f"joint {el.get('name')!r} is {kind!r}: retargeting reads {', '.join(KINDS)} joints")
            axis_el = el.find("axis")
            axis = np.array([float(v) for v in (axis_el.get("xyz") if axis_el is not None else "1 0 0").split()])
            axis = axis / np.linalg.norm(axis)
            lim = el.find("limit")
            lower, upper = -math.inf, math.inf
            if kind in ("revolute", "prismatic") and lim is not None:
                lower, upper = float(lim.get("lower", "-inf")), float(lim.get("upper", "inf"))
            joints.append(Joint(el.get("name"), kind, _origin(el.find("origin")), axis, lower, upper))
        return cls(joints, tip_offset)

    def clip(self, q: np.ndarray) -> np.ndarray:
        return np.clip(q, self.lower, self.upper)

    def _frames(self, q: np.ndarray) -> tuple[list[np.ndarray], np.ndarray]:
        """Each movable joint's frame in the base (at its origin, before its own motion), and the tip's pose."""
        t = np.eye(4)
        frames = []
        i = 0
        for j in self.joints:
            t = t @ j.origin
            if j.kind != "fixed":
                frames.append(t.copy())
                t = t @ j.motion(float(q[i]))
                i += 1
        return frames, t @ self.tip_offset

    def fk(self, q: np.ndarray) -> np.ndarray:
        """The tip's pose in the base link at joint positions q, a 4x4 transform."""
        return self._frames(np.asarray(q, dtype=float))[1]

    def jacobian(self, q: np.ndarray) -> np.ndarray:
        """The geometric Jacobian at q: 6 x dof, the tip's linear velocity (rows 0-2) and angular velocity (3-5) in the
        base frame for each movable joint's unit speed."""
        return self.fk_and_jacobian(q)[1]

    def fk_and_jacobian(self, q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """fk(q) and jacobian(q) from one walk down the chain, as each step of ik needs both."""
        frames, tip = self._frames(np.asarray(q, dtype=float))
        p = tip[:3, 3]
        jac = np.zeros((6, self.dof))
        for i, (frame, j) in enumerate(zip(frames, self.movable)):
            axis = frame[:3, :3] @ j.axis
            if j.kind == "prismatic":
                jac[:3, i] = axis
            else:
                jac[:3, i] = np.cross(axis, p - frame[:3, 3])
                jac[3:, i] = axis
        return tip, jac

    def ik(self, target: np.ndarray, q0: np.ndarray, *, orientation: bool = True, iters: int = 100,
           tol_pos: float = 1e-4, tol_rot: float = 1e-3, damping: float = 0.05,
           step_most: float = 0.2, stall: int = 5) -> tuple[np.ndarray, bool]:
        """The joint positions nearest q0's that put the tip at `target` (a 4x4 pose; with orientation False its
        position alone), by damped least squares, every joint inside its limits; and whether it got within tol_pos
        metres and tol_rot radians. Each step moves a joint step_most at most, so a far target is walked to, never
        jumped to; the steps stop early once the error has not shrunk for `stall` of them (a target past reach, or a
        limit in the way), and the nearest q met is what comes back."""
        q = self.clip(np.asarray(q0, dtype=float).copy())
        rows = 6 if orientation else 3
        damp = damping ** 2 * np.eye(rows)
        best_q, best_err, since = q, math.inf, 0
        for _ in range(iters):
            tip, jac = self.fk_and_jacobian(q)
            e = np.empty(rows)
            e[:3] = target[:3, 3] - tip[:3, 3]
            if orientation:
                e[3:] = rotation_error(tip[:3, :3], target[:3, :3])
            pos_err = float(np.linalg.norm(e[:3]))
            rot_err = float(np.linalg.norm(e[3:])) if orientation else 0.0
            if pos_err < tol_pos and rot_err < tol_rot:
                return q, True
            err = pos_err + 0.1 * rot_err
            if err < best_err - 1e-9:
                best_q, best_err, since = q, err, 0
            else:
                since += 1
                if since >= stall:
                    break
            jac = jac[:rows]
            dq = jac.T @ np.linalg.solve(jac @ jac.T + damp, e)
            most = np.max(np.abs(dq))
            if most > step_most:
                dq *= step_most / most
            q = self.clip(q + dq)
        return best_q, False
