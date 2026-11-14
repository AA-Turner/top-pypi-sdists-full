"""Server-described Flex-π deployment wire: its robot (the Bimanual YAM preset, checked against
dreamscale_transport.flexpi_deploy by the shared preset session; or a custom robot its run
describes, its cameras, widths, units and rate the block's own within the family's bounds:
docs/plans/2026-11-14-flexpi-any-robot.md), its actions and its RTC (off). The session paces at
the block's rate, the deployment record's.

On the YAM, Flex-π anchors each chunk on the last command the robot executed (its training
data's state is the previous command, not the measured pose), so every request carries that
command (``action_history``): the unit builds the model's end-effector state from it. A custom
robot sends its state as its data recorded it and no command.
"""

from __future__ import annotations

import dataclasses
import math
from typing import Any

from dreamscale_transport import flexpi_deploy as C

from dreamscale.deploy_bases.flexpi import UNITS
from dreamscale.policy.preset_deployment import (
    PresetCamera,
    PresetSessionDeployment,
    preset_runtime_contract,
)


def _whole(value: Any, low: int, high: int) -> bool:
    return type(value) is int and low <= value <= high


@dataclasses.dataclass(frozen=True)
class FlexpiSessionDeployment(PresetSessionDeployment):
    units = UNITS
    # Executed commands each request carries: the YAM's last one; a custom robot's none.
    action_history: int = C.ACTION_HISTORY

    @classmethod
    def from_json(cls, data: Any) -> FlexpiSessionDeployment:
        """The YAM preset's block exactly (the shared preset session), or a custom robot's: 1-3
        cameras each filling a view once in the model's order under distinct keys, widths that
        fit the head, a rate of 1-100 Hz, joint targets with their unit or model-defined values,
        0-1 grippers where declared, no command history, RTC off."""
        if not isinstance(data, dict) or data.get("preset") != C.CUSTOM:
            return super().from_json(data)
        if data.get("base_model") != cls.units.name:
            raise ValueError(f"the server returned no {cls.units.label} deployment contract")
        try:
            result = cls(
                **{key: data[key] for key in (
                    "id", "preset", "state_dim", "action_dim", "action_horizon",
                    "executed_actions", "action_hz", "action_space", "rtc_method",
                )},
                cameras=tuple(PresetCamera.from_json(camera) for camera in data["cameras"]),
                joint_unit=data.get("joint_unit"),
                gripper_unit=data.get("gripper_unit"),
                gripper_indices=tuple(data.get("gripper_indices") or ()),
                rtc_max_delay=data.get("rtc_max_delay"),
                action_history=data.get("action_history", 0),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"incomplete {cls.units.label} deployment contract") from error
        views = [camera.feature for camera in result.cameras]
        hz = result.action_hz
        if (
            not 1 <= len(views) <= len(C.VIEWS)
            or views != [view for view in C.VIEWS if view in views]
            or len(set(result.camera_keys)) != len(views)
            or not all(_whole(v, 1, 34) for v in (result.state_dim, result.action_dim))
            or result.action_horizon != C.ACTION_HORIZON
            or not _whole(result.executed_actions, 1, C.ACTION_HORIZON)
            or isinstance(hz, bool) or not isinstance(hz, int | float) or not math.isfinite(hz)
            or not C.MIN_HZ <= hz <= C.MAX_HZ
            or result.action_space not in C.ACTION_SPACES
            or (result.joints != (result.joint_unit is not None))
            or (result.joint_unit is not None and result.joint_unit not in C.JOINT_UNITS)
            or result.gripper_unit not in (None, C.GRIPPER_UNIT)
            or (result.gripper_unit is None) != (not result.gripper_indices)
            or len(set(result.gripper_indices)) != len(result.gripper_indices)
            or not all(_whole(i, 0, result.action_dim - 1) for i in result.gripper_indices)
            or result.action_history != 0
            or result.rtc_method != "off" or result.rtc_max_delay is not None
        ):
            raise ValueError(f"the server's {cls.units.label} deployment isn't a custom robot "
                             "it can run")
        return result


def runtime_contract(resolved: Any, deployment: Any) -> Any:
    if not isinstance(deployment, FlexpiSessionDeployment):
        deployment = FlexpiSessionDeployment.from_json(deployment)
    contract = preset_runtime_contract(FlexpiSessionDeployment, resolved, deployment)
    return dataclasses.replace(contract, action_history=deployment.action_history)
