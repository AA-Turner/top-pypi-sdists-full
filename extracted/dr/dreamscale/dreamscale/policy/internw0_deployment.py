"""An InternW0-Δ deployment's server-described contract and its episode memory (DSL-284).

The model reads, besides the current frames, the episode's first frames (its anchor) and,
from tick 32 on, the frames 32 executed actions back. ``EpisodeHistory`` keeps both and sends
them, oldest first, with each request; the server rebuilds the episode from them every
request (it keeps no robot's memory).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from dreamscale_transport.internw0_deploy import (
    ACTION_HORIZON,
    INTERNW0_BASE_MODEL,
    MAX_WIRE_ACTION_DIM,
    RECENT_OFFSET,
    InternW0Camera,
)

from dreamscale.policy.context import (
    EpisodeHistory,  # noqa: F401 - its first user's name
)


@dataclass(frozen=True)
class InternW0SessionDeployment:
    id: str
    cameras: tuple[InternW0Camera, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    joint_unit: str | None
    recent_offset: int
    rtc_method: str = "off"
    preset: str = "custom"
    layout: None = None
    robot: None = None

    @property
    def camera_keys(self):
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self):
        return self.action_space == "absolute_joint_position"

    @classmethod
    def from_json(cls, data):
        if not isinstance(data, dict) or data.get("base_model") != INTERNW0_BASE_MODEL:
            raise ValueError("the server returned no InternW0 deployment contract")
        try:
            result = cls(
                **{key: data[key] for key in (
                    "id", "state_dim", "action_dim", "action_horizon", "executed_actions",
                    "action_hz", "action_space", "recent_offset",
                )},
                cameras=tuple(InternW0Camera.model_validate(camera)
                              for camera in data["cameras"]),
                joint_unit=data.get("joint_unit"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete InternW0 deployment contract") from error
        if (
            any(type(value) is not int or not 1 <= value <= bound for value, bound in (
                (result.state_dim, 80),
                (result.action_dim, MAX_WIRE_ACTION_DIM),
                (result.executed_actions, ACTION_HORIZON),
            ))
            or result.action_horizon != ACTION_HORIZON
            or result.recent_offset != RECENT_OFFSET
            or isinstance(result.action_hz, bool)
            or not isinstance(result.action_hz, int | float)
            or not math.isfinite(result.action_hz)
            or not 1 <= result.action_hz <= 100
            or result.action_space not in ("model_defined", "absolute_joint_position")
            or (result.joints and not result.joint_unit)
            or not 1 <= len(result.cameras) <= 4
            or len(set(result.camera_keys)) != len(result.cameras)
            or data.get("rtc_method") != "off"
        ):
            raise ValueError("invalid InternW0 deployment shape or action contract")
        return result


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, InternW0SessionDeployment):
        deployment = InternW0SessionDeployment.from_json(deployment)
    # The robot waits for each chunk and runs it from its first action (RTC off: upstream's
    # sync loop), joint positions or not.
    hold = "wait"
    expected = {
        "backend": "pytorch", "rtc": "off", "rtc_contract": None,
        "action_hz": deployment.action_hz, "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim, "action_space": deployment.action_space,
        "hold_behavior": hold,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("InternW0 runtime differs from the deployment's sealed contract")
    return RuntimeContract(
        action_hz=deployment.action_hz,
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit,
        history_offsets=(deployment.recent_offset,),
        history_anchor=True,
    )
