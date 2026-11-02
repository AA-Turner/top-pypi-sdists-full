"""How a model's action rows become a rig's commands, for every robot.

Rigs take one kind of command: absolute joint positions, grippers included, in the
rig's own units. A model that acts in another space is converted here, once, at the
attended runner's act/hold boundary, so no rig grows a second control mode.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


class AbsoluteJointPosition:
    """The rig's own space: rows pass through unchanged."""

    identity = True

    def to_rig(self, action, measured):
        return action

    def hold(self, measured):
        return tuple(measured)

    def preview(self, actions, measured):
        return list(actions)


class DroidJointVelocity:
    """DROID's joint-velocity rows: seven normalized joint velocities, then the absolute
    gripper (0 open, 1 closed).

    DROID executes a row as q_measured + 0.2 * clip(v, -1, 1) radians per 1/15 s step
    (RobotIKSolver.max_joint_delta) and the gripper as a position; holding still is
    zero velocity with the gripper where it is.
    """

    identity = False
    MAX_JOINT_DELTA = 0.2
    JOINTS = 7

    def _step(self, row, reference):
        row = np.asarray(row, dtype=float)
        if row.shape != (self.JOINTS + 1,) or not np.isfinite(row).all():
            raise ValueError("A DROID velocity row is 7 finite joint velocities and a gripper.")
        joints = np.asarray(reference[: self.JOINTS], dtype=float)
        joints = joints + self.MAX_JOINT_DELTA * np.clip(row[: self.JOINTS], -1.0, 1.0)
        return (*joints.tolist(), float(np.clip(row[self.JOINTS], 0.0, 1.0)))

    def to_rig(self, action, measured):
        return self._step(action, measured)

    def hold(self, measured):
        return (0.0,) * self.JOINTS + (float(measured[self.JOINTS]),)

    def preview(self, actions: Sequence, measured):
        """Positions the chunk would reach if every step landed where it aimed."""
        reference, positions = tuple(measured), []
        for row in actions:
            reference = self._step(row, reference)
            positions.append(reference)
        return positions


_SPACES = {"droid_joint_velocity": DroidJointVelocity}


def action_space_for(contract):
    """The converter for a RuntimeContract's action_space; positions pass through."""
    return _SPACES.get(getattr(contract, "action_space", None), AbsoluteJointPosition)()
