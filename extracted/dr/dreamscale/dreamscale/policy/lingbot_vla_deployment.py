"""Server-described LingBot-VLA 2.0 deployment wire: the bimanual xArm 7, its joint targets and
its RTC."""

from __future__ import annotations

from dataclasses import dataclass

from dreamscale_transport.lingbot_vla_deploy import (
    GRIPPER_INDICES,
    HORIZON,
    LINGBOT_VLA_BASE_MODEL,
    MAX_TRAINED_RTC_DELAY,
    TRAINED_RTC_CONTRACT,
    XARM7_CAMERAS,
    XARM7_PRESET,
    XARM7_PRESET_FIELDS,
    LingbotVlaCamera,
)


@dataclass(frozen=True)
class LingbotVlaSessionDeployment:
    id: str
    preset: str
    cameras: tuple[LingbotVlaCamera, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    joint_unit: str
    gripper_indices: tuple[int, ...]
    gripper_unit: str
    prompts: tuple[str, ...]
    rtc_method: str
    rtc_max_delay: int | None

    @property
    def camera_keys(self):
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self):
        return True

    @property
    def normalized_gripper_indices(self) -> tuple[int, ...]:
        return self.gripper_indices

    @classmethod
    def from_json(cls, data):
        if not isinstance(data, dict) or data.get("base_model") != LINGBOT_VLA_BASE_MODEL:
            raise ValueError("the server returned no LingBot-VLA deployment contract")
        try:
            result = cls(
                **{key: data[key] for key in (
                    "id", "preset", "state_dim", "action_dim", "action_horizon",
                    "executed_actions", "action_hz", "action_space", "joint_unit",
                    "gripper_unit", "rtc_method",
                )},
                cameras=tuple(LingbotVlaCamera.model_validate(c) for c in data["cameras"]),
                gripper_indices=tuple(data.get("gripper_indices") or ()),
                prompts=tuple(data.get("prompts") or ()),
                rtc_max_delay=data.get("rtc_max_delay"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete LingBot-VLA deployment contract") from error
        fields = {key: getattr(result, key) for key in XARM7_PRESET_FIELDS}
        if (
            result.preset != XARM7_PRESET
            or tuple((c.key, c.role) for c in result.cameras) != XARM7_CAMERAS
            or fields != XARM7_PRESET_FIELDS
            or tuple(result.gripper_indices) != GRIPPER_INDICES
            or result.action_horizon != HORIZON
            or type(result.executed_actions) is not int
            or not 1 <= result.executed_actions <= HORIZON
            or result.action_hz != 20
        ):
            raise ValueError("the server's LingBot-VLA deployment isn't the bimanual xArm 7 wire")
        trained = data.get("trained_rtc_max_delay")
        if result.rtc_method == "off":
            if result.rtc_max_delay is not None:
                raise ValueError("a LingBot-VLA deployment with RTC off has no prefix cap")
        elif result.rtc_method != "trained" or (
            type(trained) is not int
            or type(result.rtc_max_delay) is not int
            or not 1 <= result.rtc_max_delay <= min(trained, MAX_TRAINED_RTC_DELAY)
        ):
            raise ValueError(
                f"the server returned an unknown RTC setting {result.rtc_method!r} for this "
                "LingBot-VLA deployment"
            )
        return result


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, LingbotVlaSessionDeployment):
        deployment = LingbotVlaSessionDeployment.from_json(deployment)
    trained = deployment.rtc_method == "trained"
    expected = {
        "backend": "pytorch",
        "rtc": "on" if trained else "off",
        "rtc_contract": TRAINED_RTC_CONTRACT if trained else None,
        "action_hz": deployment.action_hz,
        "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim,
        "action_space": deployment.action_space,
        "hold_behavior": "current_position",
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("LingBot-VLA runtime differs from the deployment's sealed contract")
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior="current_position",
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit,
        normalized_gripper_indices=deployment.normalized_gripper_indices,
        # Aft joints 1-7 and fore joints 1-7; the grippers are intents, never motion-limited.
        joint_groups=(tuple(range(7)), tuple(range(8, 15))),
        gripper_indices=deployment.gripper_indices,
    )
