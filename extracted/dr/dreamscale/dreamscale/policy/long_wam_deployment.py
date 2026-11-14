"""Server-described Long-WAM deployment wire: its robot (the Bimanual YAM preset, checked
against dreamscale_transport.long_wam_deploy by the shared preset session; or a custom robot a
managed run trained, its cameras, widths, units and rate the block's own within the family's
bounds: docs/plans/2026-11-14-long-wam-any-robot.md), its actions (joint targets held between
chunks, other targets waited for; RTC off), and what it adds to them: each request carries per
camera one strip of 224x224 frames, those 48, 44, ..., 4 executed ticks back that the episode
has reached, then the current one (``context.TickHistory``). Before the oldest offset, the
episode's first frame travels once ahead of them, and the server repeats it for the offsets
not yet reached, as upstream's window does (``history_start``). The session paces at the
block's rate (the export's)."""

from __future__ import annotations

import dataclasses
import math
from typing import Any

from dreamscale_transport import long_wam_deploy as C
from dreamscale_transport.images import WireImage
from dreamscale_transport.long_wam_deploy import HISTORY_OFFSETS, IMAGE_SIZE

from dreamscale.deploy_bases.long_wam import UNITS
from dreamscale.policy.preset_deployment import (
    PresetCamera,
    PresetSessionDeployment,
    preset_runtime_contract,
)

# Each camera stretched to 224x224 (upstream's processor resizes without cropping).
WIRE_IMAGE = WireImage(IMAGE_SIZE, IMAGE_SIZE, mode="stretch", resample="bilinear", quality=90)


def _whole(value: Any, low: int, high: int) -> bool:
    return type(value) is int and low <= value <= high


class LongWamSessionDeployment(PresetSessionDeployment):
    units = UNITS

    @classmethod
    def from_json(cls, data: Any) -> LongWamSessionDeployment:
        """The YAM preset's block exactly (the shared preset session), or a custom robot's: its
        cameras (1-3, each filling a view once, in the views' order, distinct keys), widths
        (1-32), rate (20-30 Hz), units and grippers, RTC off."""
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
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"incomplete {cls.units.label} deployment contract") from error
        views = [camera.feature for camera in result.cameras]
        hz = result.action_hz
        if (
            not 1 <= len(views) <= C.MAX_CAMERAS
            or views != [view for view in C.VIEWS if view in views]
            or len(set(result.camera_keys)) != len(views)
            or not all(_whole(v, 1, C.MAX_DIM) for v in (result.state_dim, result.action_dim))
            or result.action_horizon != C.ACTION_HORIZON
            or not _whole(result.executed_actions, 1, C.ACTION_HORIZON)
            or isinstance(hz, bool) or not isinstance(hz, int | float) or not math.isfinite(hz)
            or not C.MIN_HZ <= hz <= C.MAX_HZ
            or result.action_space not in C.HOLD
            or (result.joints and result.joint_unit != C.JOINT_UNIT)
            or result.gripper_unit not in (None, C.GRIPPER_UNIT)
            or len(set(result.gripper_indices)) != len(result.gripper_indices)
            or not all(_whole(i, 0, result.action_dim - 1) for i in result.gripper_indices)
            or result.rtc_method != "off" or result.rtc_max_delay is not None
        ):
            raise ValueError(f"the server's {cls.units.label} deployment isn't a custom robot "
                             "it can run")
        return result


def runtime_contract(resolved: Any, deployment: Any) -> Any:
    contract = preset_runtime_contract(LongWamSessionDeployment, resolved, deployment)
    return dataclasses.replace(contract, wire_image=WIRE_IMAGE, history_ticks=HISTORY_OFFSETS,
                               history_start=True)
