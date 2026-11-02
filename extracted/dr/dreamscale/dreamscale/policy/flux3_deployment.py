"""Server-described FLUX deployment wire, with explicit action meaning and history."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from dreamscale_transport.flux3_deploy import (
    FLUX3_BASE_MODEL,
    TRAINED_RTC_CONTRACT,
    Flux3Camera,
)
from dreamscale_transport.flux3_so101 import POLICY_CAMERA_KEYS as SO101_FEATURES


@dataclass(frozen=True)
class Flux3SessionDeployment:
    id: str
    cameras: tuple[Flux3Camera, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    joint_unit: str | None
    n_obs_steps: int
    history_snapshots: int
    inference_profile: str
    # Off, or trained: the late-bound prefix, at most ``rtc_max_delay`` committed rows pinned.
    rtc_method: str = "off"
    rtc_max_delay: int | None = None
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
        if not isinstance(data, dict) or data.get("base_model") != FLUX3_BASE_MODEL:
            raise ValueError("the server returned no FLUX deployment contract")
        try:
            result = cls(
                **{
                    key: data[key]
                    for key in (
                        "id",
                        "state_dim",
                        "action_dim",
                        "action_horizon",
                        "executed_actions",
                        "action_hz",
                        "action_space",
                        "n_obs_steps",
                        "history_snapshots",
                        "inference_profile",
                    )
                },
                cameras=tuple(Flux3Camera.model_validate(camera) for camera in data["cameras"]),
                joint_unit=data.get("joint_unit"),
                rtc_method=data.get("rtc_method"),
                rtc_max_delay=data.get("rtc_max_delay"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete FLUX deployment contract") from error
        trained = data.get("trained_rtc_max_delay")
        if result.rtc_method == "off":
            rtc_valid = result.rtc_max_delay is None
        else:
            rtc_valid = (
                result.rtc_method == "trained"
                and type(result.rtc_max_delay) is int
                and 1 <= result.rtc_max_delay < result.executed_actions
                and (trained is None or (type(trained) is int and result.rtc_max_delay <= trained))
            )
        if (
            any(
                type(value) is not int or not 1 <= value <= bound
                for value, bound in (
                    (result.state_dim, 32),
                    (result.action_dim, 32),
                    (result.action_horizon, 100),
                    (result.executed_actions, result.action_horizon),
                    (result.n_obs_steps, 32),
                    (result.history_snapshots, min(3, result.n_obs_steps)),
                )
            )
            or result.state_dim != result.action_dim
            or isinstance(result.action_hz, bool)
            or not isinstance(result.action_hz, int | float)
            or not math.isfinite(result.action_hz)
            or not 1 <= result.action_hz <= 100
            or result.action_space not in ("model_defined", "absolute_joint_position")
            or (result.joints and not result.joint_unit)
            or result.inference_profile not in ("default", "history")
            or (
                result.inference_profile == "default"
                and (result.n_obs_steps != 1 or result.history_snapshots != 1)
            )
            or not 1 <= len(result.cameras) <= 4
            or len(set(result.camera_keys)) != len(result.cameras)
            or not rtc_valid
        ):
            raise ValueError("invalid FLUX deployment shape, action or history contract")
        return result

    @property
    def history_offsets(self) -> tuple[int, ...]:
        if self.history_snapshots == 1:
            return ()
        n = self.n_obs_steps - 1
        return tuple(
            n - round(i * n / (self.history_snapshots - 1))
            for i in range(self.history_snapshots - 1)
        )


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, Flux3SessionDeployment):
        deployment = Flux3SessionDeployment.from_json(deployment)
    hold = "current_position" if deployment.joints else "wait"
    trained = deployment.rtc_method == "trained"
    expected = {
        "backend": "pytorch",
        "rtc": "on" if trained else "off",
        "rtc_contract": TRAINED_RTC_CONTRACT if trained else None,
        "action_hz": deployment.action_hz,
        "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim,
        "action_space": deployment.action_space,
        "hold_behavior": hold,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("FLUX runtime differs from the deployment's sealed contract")
    history = deployment.inference_profile == "history"
    return RuntimeContract(
        action_hz=deployment.action_hz,
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit,
        action_history=deployment.n_obs_steps if history else 0,
        history_offsets=deployment.history_offsets if history else (),
        measured_state_steps=deployment.n_obs_steps - 1 if history else 0,
    )


def so101_camera_keys(deployment: Any) -> tuple[str, str] | None:
    """The deployment's camera keys for SO-101's side and wrist cameras when `dreamscale run
    so101` drives it, else None. It drives an export of BFL's SO-101 layout: six joint
    targets in SO-101 degrees (the gripper in percent), from the scene|wrist canvas
    (``images.scene``, ``images.wrist``, in that order). ``deployment`` is a deployment row's
    ``embodiment`` or a session's Flux3SessionDeployment."""

    def get(value: Any, key: str) -> Any:
        return value.get(key) if isinstance(value, Mapping) else getattr(value, key, None)

    cameras = tuple(get(deployment, "cameras") or ())
    if (
        get(deployment, "action_space") != "absolute_joint_position"
        or get(deployment, "joint_unit") != "deg"
        or not get(deployment, "state_dim") == get(deployment, "action_dim") == 6
        or tuple(get(camera, "feature") for camera in cameras) != SO101_FEATURES
    ):
        return None
    side, wrist = (str(get(camera, "key")) for camera in cameras)
    return side, wrist


# A FLUX run on bimanual YAM recordings: its scene|wrist|right_wrist canvas, from the rig's top,
# left and right cameras (training_recipes.contract's slots).
YAM_FEATURES = ("images.scene", "images.wrist", "images.right_wrist")
YAM_ROLES = ("top", "left", "right")


def yam_camera_keys(deployment: Any) -> dict[str, str] | None:
    """The deployment's camera key for each of the YAM rig's cameras (top, left, right) when
    `dreamscale run yam` drives it, else None. It drives a FLUX run trained on bimanual YAM
    recordings: fourteen joint targets, six radians and a 0–1 gripper per arm, left then
    right. ``deployment`` is a deployment row's ``embodiment`` or a session's
    Flux3SessionDeployment."""

    def get(value: Any, key: str) -> Any:
        return value.get(key) if isinstance(value, Mapping) else getattr(value, key, None)

    cameras = tuple(get(deployment, "cameras") or ())
    gripper = get(deployment, "gripper_unit")  # a deployment row's; a session's doesn't say
    if (
        get(deployment, "action_space") != "absolute_joint_position"
        or get(deployment, "joint_unit") != "rad"
        or gripper not in (None, "normalized")
        or not get(deployment, "state_dim") == get(deployment, "action_dim") == 14
        or tuple(get(camera, "feature") for camera in cameras) != YAM_FEATURES
    ):
        return None
    return {role: str(get(camera, "key")) for role, camera in zip(YAM_ROLES, cameras, strict=True)}
