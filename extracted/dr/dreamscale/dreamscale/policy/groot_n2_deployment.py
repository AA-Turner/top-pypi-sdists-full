"""Server-described GR00T N2 deployment wire: the Bimanual YAM preset exactly as `dreamscale run
yam` sends it, or a custom robot whose cameras, widths, history and horizon its checkpoint
records (dreamscale_transport.groot_n2_deploy). Each camera sends a strip of the frames at its
history offsets (counted in executed ticks, the SDK's TickHistory), as the session's wire image.
RTC is off."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from dreamscale_transport import groot_n2_deploy as C
from dreamscale_transport.images import WireImage

from dreamscale import deploy_bases
from dreamscale.policy.deployment import PresetLayout
from dreamscale.policy.preset_deployment import PresetCamera

# Each preset's robot: its camera keys (paired with the checkpoint's cameras by role, in the
# checkpoint's order) and its widths and units.
_PRESETS = {C.YAM_PRESET: (frozenset(key for key, _ in C.YAM_CAMERAS), C.YAM_FIELDS)}


@dataclass(frozen=True)
class GrootN2SessionDeployment:
    id: str
    preset: str
    embodiment_tag: str
    cameras: tuple[PresetCamera, ...]
    history_offsets: tuple[int, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    joint_unit: str | None
    gripper_unit: str | None
    gripper_indices: tuple[int, ...]
    wire_image: WireImage
    rtc_method: str = "off"
    rtc_max_delay: None = None

    @property
    def camera_keys(self) -> tuple[str, ...]:
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self) -> bool:
        return self.action_space == "absolute_joint_position"

    @property
    def layout(self) -> PresetLayout | None:
        """The preset's robot layout (joint groups, units), where the SDK declares it."""
        return deploy_bases.robot_presets().get(self.preset) if self.preset in _PRESETS else None

    @property
    def robot(self) -> str | None:
        return self.preset if self.layout is not None else None

    @property
    def normalized_gripper_indices(self) -> tuple[int, ...]:
        return self.gripper_indices if self.gripper_unit == "normalized_0_1" else ()

    @classmethod
    def from_json(cls, data: Any) -> GrootN2SessionDeployment:
        if not isinstance(data, dict) or data.get("base_model") != C.GROOT_N2_BASE_MODEL:
            raise ValueError("the server returned no GR00T N2 deployment contract")
        try:
            result = cls(
                **{key: data[key] for key in (
                    "id", "preset", "embodiment_tag", "state_dim", "action_dim",
                    "action_horizon", "executed_actions", "action_hz", "action_space",
                    "rtc_method",
                )},
                cameras=tuple(PresetCamera.from_json(camera) for camera in data["cameras"]),
                history_offsets=tuple(data["history_offsets"]),
                joint_unit=data.get("joint_unit"),
                gripper_unit=data.get("gripper_unit"),
                gripper_indices=tuple(data.get("gripper_indices") or ()),
                wire_image=WireImage.from_json(data["wire_image"]),
                rtc_max_delay=data.get("rtc_max_delay"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete GR00T N2 deployment contract") from error
        if result.rtc_method != "off" or result.rtc_max_delay is not None:
            raise ValueError("GR00T N2 deployments run RTC off")
        offsets = list(result.history_offsets)
        if (
            any(type(value) is not int or not 1 <= value <= bound for value, bound in (
                (result.state_dim, C.MAX_STATE_DIM), (result.action_dim, C.MAX_ACTION_DIM),
                (result.action_horizon, C.MAX_HORIZON),
                (result.executed_actions, result.action_horizon),
            ))
            or isinstance(result.action_hz, bool)
            or not isinstance(result.action_hz, int | float)
            or not math.isfinite(result.action_hz)
            or not 1 <= result.action_hz <= C.MAX_HZ
            or result.action_space not in ("absolute_joint_position", "model_defined")
            or (result.joints and not result.joint_unit)
            or not 1 <= len(result.cameras) <= C.MAX_CAMERAS
            or len(set(result.camera_keys)) != len(result.cameras)
            or any(type(i) is not int or not 0 <= i < result.action_dim
                   for i in result.gripper_indices)
            or offsets != sorted(set(offsets), reverse=True)
            or any(type(o) is not int or not 1 <= o <= C.MAX_HISTORY_OFFSET for o in offsets)
            or len(offsets) >= C.MAX_HISTORY_FRAMES
            or not isinstance(result.embodiment_tag, str) or not result.embodiment_tag
        ):
            raise ValueError("invalid GR00T N2 deployment shape or action contract")
        if result.preset in _PRESETS:
            keys, fields = _PRESETS[result.preset]
            if set(result.camera_keys) != keys or any(
                getattr(result, key) != (tuple(value) if isinstance(value, tuple) else value)
                for key, value in fields.items()
            ):
                raise ValueError(f"the server's GR00T N2 deployment isn't the "
                                 f"{C.PRESET_LABELS[result.preset]} wire")
        elif result.preset != "custom":
            raise ValueError(f"unknown GR00T N2 preset {result.preset!r}")
        return result


def runtime_contract(resolved: Any, deployment: Any) -> Any:
    """The session's contract: the deployment's sealed one, refused where the server's
    resolved runtime differs from it."""
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, GrootN2SessionDeployment):
        deployment = GrootN2SessionDeployment.from_json(deployment)
    hold = "current_position" if deployment.joints else "wait"
    expected = {
        "backend": "pytorch", "rtc": "off", "rtc_contract": None,
        "action_hz": deployment.action_hz, "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim, "action_space": deployment.action_space,
        "hold_behavior": hold,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("GR00T N2 runtime differs from the deployment's sealed contract")
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
        wire_image=deployment.wire_image,
        **({"history_ticks": deployment.history_offsets} if deployment.history_offsets else {}),
        **({"joint_groups": layout.joint_groups, "gripper_indices": layout.gripper_indices,
            "startup_motion_delay_s": layout.startup_motion_delay_s}
           if layout is not None and deployment.joints else {}),
    )
