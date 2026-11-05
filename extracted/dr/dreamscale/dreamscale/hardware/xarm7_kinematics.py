"""Nominal xArm 7 FK and seeded IK in each arm's own base frame, for Hy-VLA pose chunks.

A port of the kinematics the Hy-VLA xArm 7 checkpoint was trained and evaluated with: the
same constants and the same operations in the
same order, so FK, IK, the pose encoding and ``hy_to_joints`` give bit-identical results for
the same inputs (``sdk/tests/test_xarm7_kinematics.py`` checks it against the original).

Origins: UFACTORY xarm_ros aad7e1611c9c46eb719045414394bfdd42dcb0f8,
xarm_description/config/kinematics/default/xarm7_default_kinematics.yaml.
TCP: the training rig's constants, 172 mm gripper + 13 mm stand plate (0.185 m along flange z).
The two bases are independent. Camera/world extrinsics are not used. Nominal kinematics, not
per-robot calibrated; the rig's own joint limits and motion guards stay in charge.

The joint origins above are UFACTORY's, used under this licence:

    Copyright (c) 2018, UFACTORY Inc.

    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright notice,
          this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice,
          this list of conditions and the following disclaimer in the documentation
          and/or other materials provided with the distribution.
        * Neither the name of the copyright holder nor the names of its contributors
          may be used to endorse or promote products derived from this software
          without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

scipy (``Rotation``) comes with the ``xarm7`` extra and is imported on first use.
"""

from __future__ import annotations

import functools

import numpy as np

ORIGINS = np.array([
    [0, 0, .267, 0, 0, 0], [0, 0, 0, -1.5708, 0, 0],
    [0, -.293, 0, 1.5708, 0, 0], [.0525, 0, 0, 1.5708, 0, 0],
    [.0775, -.3425, 0, 1.5708, 0, 0], [0, 0, 0, 1.5708, 0, 0],
    [.076, .097, 0, -1.5708, 0, 0],
], dtype=np.float64)
LOWER = np.array([-2*np.pi, -2.059, -2*np.pi, -.19198, -2*np.pi, -1.69297, -2*np.pi])
UPPER = np.array([2*np.pi, 2.0944, 2*np.pi, 3.927, 2*np.pi, np.pi, 2*np.pi])
TCP_OFFSET = .185
# Measured gripper drive_joint radians at fully closed: the pose state's gripper is
# clip(measured / GRIPPER_CLOSED_RAD, 0, 1).
GRIPPER_CLOSED_RAD = .85
INSTALL_HINT = (
    "Hy-VLA on the xArm 7s needs scipy for the arms' kinematics: "
    "pip install 'dreamscale[xarm7]' (or uv tool install 'dreamscale[xarm7]')"
)


def _rotation():
    try:
        from scipy.spatial.transform import Rotation
    except ImportError as error:
        raise ImportError(INSTALL_HINT) from error
    return Rotation


@functools.cache
def _fixed() -> np.ndarray:
    fixed = np.tile(np.eye(4), (7, 1, 1))
    fixed[:, :3, :3] = _rotation().from_euler("xyz", ORIGINS[:, 3:]).as_matrix()
    fixed[:, :3, 3] = ORIGINS[:, :3]
    fixed.setflags(write=False)
    return fixed


def forward(joints, *, tcp=TCP_OFFSET, jacobian=False):
    fixed = _fixed()
    q = np.asarray(joints, dtype=np.float64)
    if q.shape[-1] != 7 or not np.isfinite(q).all():
        raise ValueError("Expected seven finite xArm7 joints in radians")
    shape = q.shape[:-1]
    result = np.broadcast_to(np.eye(4), (*shape, 4, 4)).copy()
    origins, axes = [], []
    for i in range(7):
        result = result @ fixed[i]
        if jacobian:
            origins.append(result[..., :3, 3].copy())
            axes.append(result[..., :3, 2].copy())
        c, s = np.cos(q[..., i]), np.sin(q[..., i])
        rot = np.broadcast_to(np.eye(4), (*shape, 4, 4)).copy()
        rot[..., 0, 0] = rot[..., 1, 1] = c
        rot[..., 1, 0], rot[..., 0, 1] = s, -s
        result = result @ rot
    result[..., :3, 3] += tcp * result[..., :3, 2]
    if not jacobian:
        return result
    axes, origins = np.stack(axes, axis=-2), np.stack(origins, axis=-2)
    linear = np.cross(axes, result[..., None, :3, 3] - origins)
    return result, np.concatenate([linear.swapaxes(-1, -2), axes.swapaxes(-1, -2)], axis=-2)


def inverse(
    target, seed, *, max_iterations=100, translation_tolerance=1e-4, rotation_tolerance=1e-3,
):
    """Damped least-squares IK, continuous from the last measured/commanded pose.

    Return a failure explicitly; never silently execute an unconverged target.
    """
    Rotation = _rotation()
    target, seed = np.asarray(target, dtype=float), np.asarray(seed, dtype=float)
    if target.shape != (4, 4) or seed.shape != (7,) or not np.isfinite(target).all():
        raise ValueError("Malformed IK target or seed")
    q = np.clip(seed.copy(), LOWER + .02, UPPER - .02)
    for iteration in range(max_iterations):
        current, jac = forward(q, jacobian=True)
        position_error = target[:3, 3] - current[:3, 3]
        rotation_error = Rotation.from_matrix(target[:3, :3] @ current[:3, :3].T).as_rotvec()
        if (np.linalg.norm(position_error) <= translation_tolerance
                and np.linalg.norm(rotation_error) <= rotation_tolerance):
            return q, {"converged": True, "iterations": iteration,
                       "position_error_m": float(np.linalg.norm(position_error)),
                       "rotation_error_rad": float(np.linalg.norm(rotation_error))}
        error = np.r_[position_error, rotation_error]
        # Prefer the local solution of the redundant seven-joint arm.
        pinv = jac.T @ np.linalg.solve(jac @ jac.T + 1e-5 * np.eye(6), np.eye(6))
        change = pinv @ error + .02 * (np.eye(7) - pinv @ jac) @ (seed - q)
        change *= min(1., .15 / max(np.max(np.abs(change)), 1e-12))
        q = np.clip(q + change, LOWER + .02, UPPER - .02)
    return q, {"converged": False, "iterations": max_iterations,
               "position_error_m": float(np.linalg.norm(position_error)),
               "rotation_error_rad": float(np.linalg.norm(rotation_error))}


def encode_pose(transform, gripper):
    # Hy uses ROWS 0 and 1 (not columns) of the rotation matrix.
    return np.concatenate([transform[..., :3, 3],
                           transform[..., :2, :3].reshape(*transform.shape[:-2], 6),
                           np.asarray(gripper)[..., None]], axis=-1)


def decode_pose(vector):
    x = np.asarray(vector, dtype=np.float64)
    a, b = x[..., 3:6], x[..., 6:9]
    n = np.linalg.norm(a, axis=-1, keepdims=True)
    if np.any(n < 1e-8) or not np.isfinite(x).all():
        raise ValueError("Degenerate predicted orientation")
    a = a / n
    b = b - np.sum(a * b, axis=-1, keepdims=True) * a
    n = np.linalg.norm(b, axis=-1, keepdims=True)
    if np.any(n < 1e-8):
        raise ValueError("Collinear predicted rotation rows")
    b = b / n
    result = np.broadcast_to(np.eye(4), (*x.shape[:-1], 4, 4)).copy()
    result[..., :3, :3] = np.stack([a, b, np.cross(a, b)], axis=-2)
    result[..., :3, 3] = x[..., :3]
    return result


def hy_targets(state, absolute_commands):
    """Measured current TCP state; commanded future TCP actions, fore then aft.

    ``state`` and ``absolute_commands`` are 16-value joint rows, aft first (per arm seven
    joints in radians, then the gripper: measured drive_joint radians in the state, the
    0-1 close intent in the commands). Returns the 20-value pose state and, for k command
    rows, 2k pose rows: the k rows relative to the state's pose, then the same k absolute.
    """
    states, relative, absolute = [], [], []
    for offset in (8, 0):  # fore=left, aft=right; exported arrays are aft first.
        anchor = forward(state[..., offset:offset + 7])
        target = forward(absolute_commands[..., offset:offset + 7])
        gripper = absolute_commands[..., offset + 7]
        states.append(encode_pose(anchor, np.clip(state[..., offset + 7] / .85, 0., 1.)))
        relative.append(encode_pose(np.linalg.inv(anchor)[..., None, :, :] @ target, gripper))
        absolute.append(encode_pose(target, gripper))
    return (np.concatenate(states, axis=-1).astype(np.float32),
            np.concatenate([np.concatenate(relative, axis=-1),
                            np.concatenate(absolute, axis=-1)], axis=-2).astype(np.float32))


def _solve(relative_actions, state, active_arm, gripper_intent, absolute_actions):
    """``hy_to_joints``'s computation, stopping at the first unconverged row: the joint rows
    (rows from the failed one on are unfilled) and None, or (failed row, diagnostic)."""
    Rotation = _rotation()
    relative_actions = np.asarray(relative_actions)
    if absolute_actions is not None and np.shape(absolute_actions) != relative_actions.shape:
        raise ValueError("Relative/absolute head shape mismatch")
    if active_arm not in ("fore", "aft"):
        raise ValueError("Unknown active arm")
    result = np.tile(np.asarray(state, dtype=np.float32), (len(relative_actions), 1))
    intent = np.asarray(gripper_intent)
    if intent.shape != (2,) or not np.isin(intent, [0, 1]).all():
        raise ValueError(
            "Current binary gripper intent (aft, fore) is required to hold the inactive arm"
        )
    result[:, [7, 15]] = intent
    for model_offset, raw_offset, name in ((0, 8, "fore"), (10, 0, "aft")):
        if name != active_arm:
            continue
        seed = np.asarray(state[raw_offset:raw_offset + 7], dtype=float)
        anchor = forward(seed)
        transforms = anchor @ decode_pose(relative_actions[:, model_offset:model_offset + 10])
        gripper = relative_actions[:, model_offset + 9]
        if absolute_actions is not None:
            absolute = decode_pose(absolute_actions[:, model_offset:model_offset + 10])
            transforms[:, :3, 3] = .5 * (transforms[:, :3, 3] + absolute[:, :3, 3])
            # R1 exp(.5 log(R1^-1 R2)) is the shortest-arc quaternion slerp.
            relative_rotation = transforms[:, :3, :3].swapaxes(-1, -2) @ absolute[:, :3, :3]
            half = Rotation.from_rotvec(
                .5 * Rotation.from_matrix(relative_rotation).as_rotvec()
            ).as_matrix()
            transforms[:, :3, :3] = transforms[:, :3, :3] @ half
            gripper = .5 * (gripper + absolute_actions[:, model_offset + 9])
        result[:, raw_offset + 7] = (gripper >= .5).astype(np.float32)
        for i, target in enumerate(transforms):
            seed, diagnostic = inverse(target, seed)
            if not diagnostic["converged"]:
                return result, (i, diagnostic)
            result[i, raw_offset:raw_offset + 7] = seed
    return result, None


def hy_to_joints(relative_actions, state, *, active_arm, gripper_intent, absolute_actions=None):
    """Native paired-head pose blend followed by sequential seeded IK.

    The relative-only interface remains useful for a diagnostic. Delivery
    supplies both heads, averaging position/gripper and quaternion slerp(.5).
    """
    result, failure = _solve(relative_actions, state, active_arm, gripper_intent, absolute_actions)
    if failure is not None:
        raise ValueError(f"Hy IK failed at action {failure[0]}: {failure[1]}")
    return result


def hold(state, intent, rows):
    """``rows`` copies of the measured joints with the gripper intent (aft, fore)."""
    joints = np.tile(np.asarray(state, np.float32), (rows, 1))
    joints[:, [7, 15]] = intent
    return joints


def execute(relative, absolute, state, active_arm, intent):
    """Delivery execution of one chunk, as the checkpoint was evaluated. An unconverged IK
    row is never executed: from the first failure the arm holds the last converged row (or
    the measured state when row 0 fails or a predicted rotation is degenerate), and the
    failure is returned as {row, error}; None when every row converged."""
    try:
        result, failure = _solve(relative, state, active_arm, intent, absolute)
    except ValueError as error:  # degenerate rotations fail the whole chunk
        return hold(state, intent, len(relative)), {"row": 0, "error": str(error)[:160]}
    if failure is None:
        return result, None
    row, diagnostic = failure
    joints = hold(state, intent, len(relative))
    if row:
        joints[:row] = result[:row]
        joints[row:] = joints[row - 1]
    return joints, {"row": row, "error": f"Hy IK failed at action {row}: {diagnostic}"[:160],
                    "diagnostic": diagnostic}
