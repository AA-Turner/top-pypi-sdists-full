"""SO-101 forward and inverse kinematics, in lerobot's calibrated degrees.

The chain is TheRobotStudio's so101_new_calib.urdf (SO-ARM100 repository), whose zero
pose is lerobot's calibrated zero: each joint's value in lerobot degrees is its URDF
angle. The tool point is the URDF's gripper_frame_link, between the jaw tips; its +z
axis is the approach direction the jaws point along.

The arm has five joints, so a tool pose is reachable only up to five numbers: the tool
position (3), its tilt (how far the approach axis points below horizontal) and its roll
(wrist_roll, which turns the jaws about the approach axis). The shoulder pan sets the
heading toward the target, so it is not a free choice.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from dreamscale.constants import JOINT_NAMES

# (xyz metres, rpy radians) of each revolute joint in its parent link, base to wrist;
# every axis is the joint frame's z.
_JOINTS = (
    ((0.0388353, -8.97657e-09, 0.0624), (3.14159, 4.18253e-17, -3.14159)),     # pan
    ((-0.0303992, -0.0182778, -0.0542), (-1.5708, -1.5708, 0.0)),              # lift
    ((-0.11257, -0.028, 1.73763e-16), (-3.63608e-16, 8.74301e-16, 1.5708)),     # elbow
    ((-0.1349, 0.0052, 3.62355e-17), (4.02456e-15, 8.67362e-16, -1.5708)),     # wrist flex
    ((5.55112e-17, -0.0611, 0.0181), (1.5708, 0.0486795, 3.14159)),            # wrist roll
)
# gripper_link -> gripper_frame_link (fixed): the tool point between the jaws.
_TOOL = ((-0.0079, -0.000218121, -0.0981274), (0.0, 3.14159, 0.0))
ARM_JOINTS = len(_JOINTS)
WRIST_ROLL = JOINT_NAMES.index("wrist_roll")


def _transform(xyz, rpy) -> np.ndarray:
    roll, pitch, yaw = rpy
    cr, sr, cp, sp, cy, sy = (math.cos(roll), math.sin(roll), math.cos(pitch),
                              math.sin(pitch), math.cos(yaw), math.sin(yaw))
    out = np.eye(4)
    out[:3, :3] = [
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr],
    ]
    out[:3, 3] = xyz
    return out


def _rot_z(angle) -> np.ndarray:
    out = np.eye(4)
    c, s = math.cos(angle), math.sin(angle)
    out[:2, :2] = [[c, -s], [s, c]]
    return out


_ORIGINS = tuple(_transform(*joint) for joint in _JOINTS)
_TOOL_T = _transform(*_TOOL)


def tool_pose(joints_deg) -> np.ndarray:
    """4x4 pose of the tool point in the base frame for five arm joints in degrees."""
    pose = np.eye(4)
    for origin, angle in zip(_ORIGINS, joints_deg[:ARM_JOINTS], strict=True):
        pose = pose @ origin @ _rot_z(math.radians(float(angle)))
    return pose @ _TOOL_T


@dataclass(frozen=True)
class ToolState:
    position_m: tuple[float, float, float]
    tilt_deg: float  # approach axis below horizontal: 90 points straight down
    roll_deg: float  # wrist_roll, lerobot degrees

    def as_dict(self) -> dict:
        return {"position_m": [round(v, 4) for v in self.position_m],
                "tilt_deg": round(self.tilt_deg, 1), "roll_deg": round(self.roll_deg, 1)}


def tool_state(joints_deg) -> ToolState:
    pose = tool_pose(joints_deg)
    approach = pose[:3, 2]
    tilt = math.degrees(math.asin(max(-1.0, min(1.0, -approach[2]))))
    return ToolState(tuple(float(v) for v in pose[:3, 3]), tilt, float(joints_deg[WRIST_ROLL]))


class IKFailure(ValueError):
    pass


def solve(position_m, tilt_deg, roll_deg, seed_deg, limits_deg, *, iterations=200,
          position_tolerance_m=0.003, tilt_tolerance_deg=2.0) -> np.ndarray:
    """Five arm joints (degrees) placing the tool at position_m with tilt_deg and roll_deg.

    Damped least squares over pan, lift, elbow and wrist flex from seed_deg, kept
    inside limits_deg (rows [low, high] per arm joint); wrist_roll is roll_deg. Raises
    IKFailure when the target is out of reach within the tolerances.
    """
    target = np.asarray(position_m, dtype=float)
    limits = np.asarray(limits_deg, dtype=float)[:ARM_JOINTS]
    joints = np.clip(np.asarray(seed_deg, dtype=float)[:ARM_JOINTS], limits[:, 0], limits[:, 1])
    if not limits[WRIST_ROLL, 0] <= roll_deg <= limits[WRIST_ROLL, 1]:
        raise IKFailure(f"roll_deg {roll_deg:.1f} is outside wrist_roll's calibrated travel.")
    joints[WRIST_ROLL] = roll_deg
    tilt_weight = 0.05  # metres of position error worth one radian of tilt error

    def residual(q):
        state = tool_state(q)
        return np.r_[np.asarray(state.position_m) - target,
                     tilt_weight * math.radians(state.tilt_deg - tilt_deg)]

    error = residual(joints)
    for _ in range(iterations):
        if (np.linalg.norm(error[:3]) <= position_tolerance_m
                and abs(math.degrees(error[3] / tilt_weight)) <= tilt_tolerance_deg):
            return joints
        jacobian = np.zeros((4, 4))
        for i in range(4):
            step = joints.copy()
            step[i] += 0.01
            jacobian[:, i] = (residual(step) - error) / math.radians(0.01)
        damping = 1e-4
        delta = jacobian.T @ np.linalg.solve(jacobian @ jacobian.T + damping * np.eye(4), -error)
        delta_deg = np.clip(np.degrees(delta), -10.0, 10.0)
        candidate = joints.copy()
        candidate[:4] = np.clip(candidate[:4] + delta_deg, limits[:4, 0], limits[:4, 1])
        candidate_error = residual(candidate)
        if np.linalg.norm(candidate_error) >= np.linalg.norm(error) and np.allclose(
            candidate, joints
        ):
            break
        joints, error = candidate, candidate_error
    state = tool_state(joints)
    miss = np.linalg.norm(np.asarray(state.position_m) - target)
    raise IKFailure(
        f"Target out of reach: closest tool position is {miss * 100:.1f} cm away with tilt "
        f"{state.tilt_deg:.0f}° (asked {tilt_deg:.0f}°)."
    )
