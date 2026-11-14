"""Server-described LingBot-VLA 2.0 deployment wire: the bimanual xArm 7 (its joint targets) or a
custom robot its export's record declares, and its RTC. The session paces at the block's rate
(the deployment record's: the export's, or the create's declaration), 1 to MAX_HZ."""

from __future__ import annotations

import math
from dataclasses import dataclass

from dreamscale_transport.lingbot_vla_deploy import (
    CUSTOM_PRESET,
    GRIPPER_INDICES,
    HORIZON,
    LINGBOT_VLA_BASE_MODEL,
    MAX_HORIZON,
    MAX_TRAINED_RTC_DELAY,
    MODEL_WIDTH,
    ROLES,
    TRAINED_RTC_CONTRACT,
    XARM7_CAMERAS,
    XARM7_PRESET,
    XARM7_PRESET_FIELDS,
    LingbotVlaCamera,
)
from dreamscale_transport.units_reference import MAX_HZ


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
    joint_unit: str | None
    gripper_indices: tuple[int, ...]
    gripper_unit: str | None
    prompts: tuple[str, ...]
    rtc_method: str
    rtc_max_delay: int | None

    @property
    def camera_keys(self):
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self):
        return self.action_space == "absolute_joint_position"

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
        if isinstance(result.action_hz, bool) or not isinstance(result.action_hz, int | float) or (
            not math.isfinite(result.action_hz) or not 1 <= result.action_hz <= MAX_HZ
        ):
            raise ValueError(f"the server's LingBot-VLA rate must be 1-{MAX_HZ} Hz")
        if result.preset == CUSTOM_PRESET:
            _check_custom(result)
        else:
            fields = {key: getattr(result, key) for key in XARM7_PRESET_FIELDS}
            if (
                result.preset != XARM7_PRESET
                or tuple((c.key, c.role) for c in result.cameras) != XARM7_CAMERAS
                or fields != XARM7_PRESET_FIELDS
                or tuple(result.gripper_indices) != GRIPPER_INDICES
                or result.action_horizon != HORIZON
                or type(result.executed_actions) is not int
                or not 1 <= result.executed_actions <= HORIZON
            ):
                raise ValueError("the server's LingBot-VLA deployment isn't the bimanual xArm 7 "
                                 "wire")
        trained = data.get("trained_rtc_max_delay")
        if result.rtc_method == "off":
            if result.rtc_max_delay is not None:
                raise ValueError("a LingBot-VLA deployment with RTC off has no prefix cap")
        elif result.rtc_method != "trained" or (
            type(trained) is not int
            or type(result.rtc_max_delay) is not int
            or not 1 <= result.rtc_max_delay <= min(trained, MAX_TRAINED_RTC_DELAY,
                                                    result.action_horizon - 1)
        ):
            raise ValueError(
                f"the server returned an unknown RTC setting {result.rtc_method!r} for this "
                "LingBot-VLA deployment"
            )
        return result


def _check_custom(result: LingbotVlaSessionDeployment) -> None:
    """A custom robot's block within the family's bounds (its record's widths, views, chunk)."""
    roles = [c.role for c in result.cameras]
    ints = (result.state_dim, result.action_dim, result.action_horizon, result.executed_actions)
    if (
        not 1 <= len(roles) <= 3 or roles != sorted(set(roles), key=ROLES.index)
        or len({c.key for c in result.cameras}) != len(roles)
        or any(type(v) is not int for v in ints)
        or not 1 <= result.state_dim <= MODEL_WIDTH or not 1 <= result.action_dim <= MODEL_WIDTH
        or not 1 <= result.action_horizon <= MAX_HORIZON
        or not 1 <= result.executed_actions <= result.action_horizon
        or result.action_space not in ("absolute_joint_position", "model_defined")
        or (result.action_space == "absolute_joint_position"
            and result.state_dim != result.action_dim)
        or len(set(result.gripper_indices)) != len(result.gripper_indices)
        or any(type(i) is not int or not 0 <= i < result.action_dim
               for i in result.gripper_indices)
        or (result.gripper_indices and result.gripper_unit != "normalized_0_1")
    ):
        raise ValueError("the server's custom LingBot-VLA robot is outside the family's bounds")


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, LingbotVlaSessionDeployment):
        deployment = LingbotVlaSessionDeployment.from_json(deployment)
    trained = deployment.rtc_method == "trained"
    hold = "current_position" if deployment.joints else "wait"
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
        raise ValueError("LingBot-VLA runtime differs from the deployment's sealed contract")
    xarm7 = deployment.preset == XARM7_PRESET
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
        # The xArm 7: aft joints 1-7 and fore joints 1-7; the grippers are intents, never
        # motion-limited. A custom robot's joints aren't named by its record: no groups.
        **({"joint_groups": (tuple(range(7)), tuple(range(8, 15))),
            "gripper_indices": deployment.gripper_indices} if xarm7 else {}),
    )
