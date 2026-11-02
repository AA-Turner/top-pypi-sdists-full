"""Server-described ABC-VLA deployment wire: the robot, its action meaning and its RTC."""

from __future__ import annotations

import math
from dataclasses import dataclass

from dreamscale_transport.abc_vla_deploy import (
    ABC_VLA_BASE_MODEL,
    MAX_CAMERAS,
    MAX_DIM,
    MAX_HORIZON,
    MAX_HZ,
    MAX_TRAINED_RTC_DELAY,
    PRESETS,
    TRAINED_RTC_CONTRACT,
    YAM_CAMERAS,
    YAM_PRESET,
    YAM_PRESET_FIELDS,
    AbcVlaCamera,
)

from dreamscale.policy.deployment import PresetLayout
from dreamscale.policy.pi05_deployment import PRESET_LAYOUTS


@dataclass(frozen=True)
class AbcVlaSessionDeployment:
    id: str
    preset: str
    cameras: tuple[AbcVlaCamera, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    joint_unit: str | None
    gripper_indices: tuple[int, ...]
    gripper_unit: str | None
    rtc_method: str
    rtc_max_delay: int | None

    @property
    def camera_keys(self):
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self):
        return self.action_space == "absolute_joint_position"

    @property
    def robot(self) -> str | None:
        """The preset robot it drives: Bimanual YAM keeps that robot's wire exactly."""
        return YAM_PRESET if self.preset == YAM_PRESET else None

    @property
    def layout(self) -> PresetLayout | None:
        """That robot's joint layout, units and observe helper (the shared YAM wire)."""
        return PRESET_LAYOUTS[YAM_PRESET] if self.robot else None

    @classmethod
    def from_json(cls, data):
        if not isinstance(data, dict) or data.get("base_model") != ABC_VLA_BASE_MODEL:
            raise ValueError("the server returned no ABC-VLA deployment contract")
        try:
            result = cls(
                **{
                    key: data[key]
                    for key in (
                        "id",
                        "preset",
                        "state_dim",
                        "action_dim",
                        "action_horizon",
                        "executed_actions",
                        "action_hz",
                        "action_space",
                        "rtc_method",
                    )
                },
                cameras=tuple(AbcVlaCamera.model_validate(camera) for camera in data["cameras"]),
                joint_unit=data.get("joint_unit"),
                gripper_unit=data.get("gripper_unit"),
                gripper_indices=tuple(data.get("gripper_indices") or ()),
                rtc_max_delay=data.get("rtc_max_delay"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete ABC-VLA deployment contract") from error
        trained = data.get("trained_rtc_max_delay")
        if (
            any(
                type(value) is not int or not 1 <= value <= bound
                for value, bound in (
                    (result.state_dim, MAX_DIM),
                    (result.action_dim, MAX_DIM),
                    (result.action_horizon, MAX_HORIZON),
                    (result.executed_actions, result.action_horizon),
                )
            )
            or isinstance(result.action_hz, bool)
            or not isinstance(result.action_hz, int | float)
            or not math.isfinite(result.action_hz)
            or not 1 <= result.action_hz <= MAX_HZ
            or result.action_space not in ("model_defined", "absolute_joint_position")
            or (result.joints and (not result.joint_unit or result.state_dim != result.action_dim))
            or not 1 <= len(result.cameras) <= MAX_CAMERAS
            or len(set(result.camera_keys)) != len(result.cameras)
            or any(type(i) is not int or not 0 <= i < result.action_dim
                   for i in result.gripper_indices)
            or result.preset not in PRESETS
        ):
            raise ValueError("invalid ABC-VLA deployment shape or action contract")
        if result.preset == YAM_PRESET and (
            tuple((camera.key, camera.feature) for camera in result.cameras) != YAM_CAMERAS
            or any(getattr(result, key) != value for key, value in YAM_PRESET_FIELDS.items())
        ):
            raise ValueError("the server's Bimanual YAM deployment isn't the YAM wire")
        if result.rtc_method == "off":
            if result.rtc_max_delay is not None:
                raise ValueError("an ABC-VLA deployment with RTC off has no prefix cap")
        elif result.rtc_method != "trained" or (
            type(trained) is not int
            or type(result.rtc_max_delay) is not int
            or not 1 <= result.rtc_max_delay <= min(trained, MAX_TRAINED_RTC_DELAY)
        ):
            raise ValueError(
                f"the server returned an unknown RTC setting {result.rtc_method!r} for this "
                "ABC-VLA deployment"
            )
        return result

    @property
    def normalized_gripper_indices(self) -> tuple[int, ...]:
        return self.gripper_indices if self.gripper_unit == "normalized_0_1" else ()


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, AbcVlaSessionDeployment):
        deployment = AbcVlaSessionDeployment.from_json(deployment)
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
        raise ValueError("ABC-VLA runtime differs from the deployment's sealed contract")
    layout = deployment.layout
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit,
        normalized_gripper_indices=deployment.normalized_gripper_indices,
        **(
            {
                "joint_groups": layout.joint_groups,
                "gripper_indices": layout.gripper_indices,
                "startup_motion_delay_s": layout.startup_motion_delay_s,
            }
            if layout is not None
            else {}
        ),
    )
