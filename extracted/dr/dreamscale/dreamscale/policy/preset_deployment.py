"""Server-described deployment wire of a units base whose deployments run one robot preset
(``dreamscale.deploy_bases._preset.PresetUnits``): the session's deployment block must be that
preset's robot exactly (its cameras, widths, units, chunk and rate), and its RTC off or trained
within the checkpoint's prefixes.

A base's ``dreamscale.policy.<family>_deployment`` module subclasses
``PresetSessionDeployment`` with its ``units`` and binds ``preset_runtime_contract`` to it; its
``ExportedBase`` names both.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from dreamscale import deploy_bases
from dreamscale.deploy_bases._preset import PresetUnits
from dreamscale.policy.deployment import PresetLayout


@dataclass(frozen=True)
class PresetCamera:
    key: str  # what the robot sends its frames under
    feature: str  # the checkpoint camera it fills

    @classmethod
    def from_json(cls, data: Any) -> PresetCamera:
        if not isinstance(data, dict) or set(data) != {"key", "feature"} or not all(
            isinstance(value, str) and value for value in data.values()
        ):
            raise ValueError("a camera is its key and the checkpoint camera it fills")
        return cls(data["key"], data["feature"])


@dataclass(frozen=True)
class PresetSessionDeployment:
    units: ClassVar[PresetUnits]

    id: str
    preset: str
    cameras: tuple[PresetCamera, ...]
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
    def camera_keys(self) -> tuple[str, ...]:
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self) -> bool:
        return self.action_space == "absolute_joint_position"

    @property
    def robot(self) -> str | None:
        """The SDK robot preset it drives, where a base declares that robot's layout."""
        return self.preset if self.layout is not None else None

    @property
    def layout(self) -> PresetLayout | None:
        """That robot's joint layout, units and observe helper (``robot_presets``)."""
        return deploy_bases.robot_presets().get(self.preset)

    @property
    def normalized_gripper_indices(self) -> tuple[int, ...]:
        return self.gripper_indices if self.gripper_unit == "normalized_0_1" else ()

    @classmethod
    def from_json(cls, data: Any) -> PresetSessionDeployment:
        units = cls.units
        if not isinstance(data, dict) or data.get("base_model") != units.name:
            raise ValueError(f"the server returned no {units.label} deployment contract")
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
            raise ValueError(f"incomplete {units.label} deployment contract") from error
        robot = units.robot or units.preset_label
        if (
            result.preset != units.preset
            or tuple((camera.key, camera.feature) for camera in result.cameras) != units.cameras
            or any(type(value) is not int or value != expected for value, expected in (
                (result.state_dim, units.state_dim), (result.action_dim, units.action_dim),
                (result.action_horizon, units.action_horizon),
            ))
            or (result.action_space, result.joint_unit, result.gripper_unit) != (
                units.action_space, units.joint_unit, units.gripper_unit)
            or result.gripper_indices != units.gripper_indices
            or type(result.executed_actions) is not int
            or not 1 <= result.executed_actions <= units.action_horizon
            or isinstance(result.action_hz, bool)
            or result.action_hz != units.action_hz
        ):
            raise ValueError(f"the server's {units.label} deployment isn't the {robot} wire")
        trained = data.get("trained_rtc_max_delay")
        if result.rtc_method == "off":
            if result.rtc_max_delay is not None:
                raise ValueError(f"a {units.label} deployment with RTC off has no prefix cap")
        elif not units.trained or result.rtc_method != "trained" or (
            type(trained) is not int
            or type(result.rtc_max_delay) is not int
            or not 1 <= result.rtc_max_delay <= min(trained, units.max_trained_rtc_delay)
        ):
            raise ValueError(
                f"the server returned an unknown RTC setting {result.rtc_method!r} for this "
                f"{units.label} deployment"
            )
        return result


def preset_runtime_contract(cls: type[PresetSessionDeployment], resolved: Any,
                            deployment: Any) -> Any:
    """The session's contract: the deployment's sealed one, refused where the server's
    resolved runtime differs from it."""
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, cls):
        deployment = cls.from_json(deployment)
    trained = deployment.rtc_method == "trained"
    hold = "current_position" if deployment.joints else "wait"
    expected = {
        "backend": "pytorch",
        "rtc": "on" if trained else "off",
        "rtc_contract": cls.units.rtc_contract if trained else None,
        "action_hz": deployment.action_hz,
        "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim,
        "action_space": deployment.action_space,
        "hold_behavior": hold,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError(f"{cls.units.label} runtime differs from the deployment's sealed "
                         "contract")
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
        **({"joint_groups": layout.joint_groups, "gripper_indices": layout.gripper_indices,
            "startup_motion_delay_s": layout.startup_motion_delay_s}
           if layout is not None and deployment.joints else {}),
    )
