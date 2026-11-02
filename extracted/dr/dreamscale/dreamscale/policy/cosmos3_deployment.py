"""A Cosmos 3 Nano Policy deployment's server-described contract (DSL-350): each session's
deployment block is its checkpoint's own robot (NVIDIA's DROID recipe, or a Dreamscale training
export's), read as the server sends it and checked against the family's limits. RTC is off and
the model reads no history: each request is the current frames (letterboxed to the canvas slot,
the session's ``wire_image``), the state when the checkpoint reads one, and the instruction."""

from __future__ import annotations

import math
from dataclasses import dataclass

from dreamscale_transport.cosmos3_deploy import (
    COSMOS3_BASE_MODEL,
    MAX_ACTION_DIM,
    MAX_ACTION_HORIZON,
    MAX_ACTION_HZ,
    Cosmos3Camera,
)
from dreamscale_transport.images import WireImage

ACTION_SPACES = ("absolute_joint_position", "model_defined")


@dataclass(frozen=True)
class Cosmos3SessionDeployment:
    id: str
    preset: str
    cameras: tuple[Cosmos3Camera, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: int
    action_space: str
    joint_unit: str | None
    gripper_transform: str
    slot: tuple[int, int]
    rtc_method: str = "off"
    layout: None = None
    robot: None = None

    @property
    def camera_keys(self):
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self):
        return self.action_space == "absolute_joint_position"

    @property
    def hold_behavior(self) -> str:
        """Joint targets hold the current position between chunks; anything else waits."""
        return "current_position" if self.joints else "wait"

    @classmethod
    def from_json(cls, data):
        if not isinstance(data, dict) or data.get("base_model") != COSMOS3_BASE_MODEL:
            raise ValueError("the server returned no Cosmos 3 deployment contract")
        try:
            canvas = data["canvas"]
            result = cls(
                **{key: data[key] for key in (
                    "id", "preset", "state_dim", "action_dim", "action_horizon",
                    "executed_actions", "action_hz", "action_space", "gripper_transform",
                )},
                cameras=tuple(Cosmos3Camera.model_validate(camera) for camera in data["cameras"]),
                joint_unit=data.get("joint_unit"),
                slot=(canvas["slot_width"], canvas["slot_height"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete Cosmos 3 deployment contract") from error
        if (
            any(type(value) is not int or not lo <= value <= hi for value, lo, hi in (
                (result.action_dim, 1, MAX_ACTION_DIM),
                (result.action_horizon, 4, MAX_ACTION_HORIZON),
                (result.executed_actions, 1, result.action_horizon),
                (result.action_hz, 1, MAX_ACTION_HZ),
                *((v, 32, 1280) for v in result.slot),
            ))
            or result.state_dim not in (0, result.action_dim)
            or result.preset not in ("custom", "droid")
            or result.action_space not in ACTION_SPACES
            or result.gripper_transform not in ("droid", "none")
            or (result.joints and not result.joint_unit)
            or not 1 <= len(result.cameras) <= 3
            or len(set(result.camera_keys)) != len(result.cameras)
            or not math.isfinite(result.action_hz)
            or data.get("rtc_method") != "off"
        ):
            raise ValueError("invalid Cosmos 3 deployment shape or action contract")
        return result


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, Cosmos3SessionDeployment):
        deployment = Cosmos3SessionDeployment.from_json(deployment)
    expected = {
        "backend": "pytorch", "rtc": "off", "rtc_contract": None,
        "action_hz": deployment.action_hz, "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim, "action_space": deployment.action_space,
        "hold_behavior": deployment.hold_behavior,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("Cosmos 3 runtime differs from the deployment's sealed contract")
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=deployment.hold_behavior,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit,
        # Each camera letterboxed to its canvas slot (the server refuses any other size); the
        # session block's wire_image, when the server sends one, is the same.
        wire_image=WireImage(*deployment.slot, "letterbox", "bilinear", quality=90),
    )
