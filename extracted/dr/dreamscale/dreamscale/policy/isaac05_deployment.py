"""An Isaac 0.5 deployment's server-described contract (dreamscale_core.isaac05_deploy).

Isaac 0.5 reads 1 or 3 frames per camera (the deployment's ``n_obs_steps``, sealed at create):
the newest and the frames 1 and 2 control ticks before it (the checkpoint's own rate), oldest
first, and the newest frame's state; it predicts the checkpoint's chunk (``model_horizon``: 50
for the base, 60 for Perceptron's Isaac-0.5-YAM) of which the deployment executes
``executed_actions``. The window is the deployment block's, never a preparation reply's: a
unit's ``task_prepared`` carries no context. Older frames ride ahead of the request where the
server takes history frames (``history_frames_v1``), else in each camera's strip.

Every new instruction is prepared before its first observation (``task_prepare_v1``: the
server captures its layouts), within 300 s.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

from dreamscale_core.isaac05_deploy import (
    CONTEXT_FRAMES,
    ISAAC05_BASE_MODEL,
    ISAAC05_SOURCE_FORMAT,
    MAX_ACTION_DIM,
    MAX_CAMERAS,
    MAX_MODEL_HORIZON,
    MAX_PACKAGE_RTC_DELAY,
    MAX_STATE_DIM,
    PRESET_FIELDS,
    PRESETS,
    TRAINED_RTC_CONTRACT,
    Isaac05Camera,
    preset_cameras,
)

from dreamscale.policy.deployment import PresetLayout
from dreamscale.policy.pi05_deployment import PRESET_LAYOUTS

# Allow the server to prepare each new instruction before its first observation.
TASK_PREPARE_TIMEOUT_S = 300.0
_FIELDS = (
    "id", "preset", "image_hw", "state_dim", "action_dim", "action_layout", "action_space",
    "frame", "n_obs_steps", "model_horizon", "executed_actions", "action_hz",
    "trained_rtc_max_delay", "rtc_method",
)


@dataclass(frozen=True)
class Isaac05SessionDeployment:
    id: str
    preset: str
    cameras: tuple[Isaac05Camera, ...]
    image_hw: tuple[int, int]
    state_dim: int
    action_dim: int
    action_layout: tuple[str, ...]
    action_space: str
    frame: str
    n_obs_steps: int
    model_horizon: int
    executed_actions: int
    action_hz: float
    trained_rtc_max_delay: int
    rtc_method: str
    rtc_max_delay: int | None
    joint_unit: str | None = None
    gripper_unit: str | None = None
    gripper_indices: tuple[int, ...] = ()
    # The bundle's layout (a Perceptron package renders some presets under its own camera names).
    bundle_layout: str | None = None

    @property
    def camera_keys(self) -> tuple[str, ...]:
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self) -> bool:
        return self.action_space == "absolute_joint_position"

    @property
    def robot(self) -> str | None:
        """The preset robot it drives (Bimanual YAM or SO-101 keep that robot's wire)."""
        return self.preset if self.preset in PRESET_FIELDS else None

    @property
    def layout(self) -> PresetLayout | None:
        """That robot's joint layout and observe helper (the shared preset wire)."""
        return PRESET_LAYOUTS.get(self.robot) if self.robot else None

    @property
    def normalized_gripper_indices(self) -> tuple[int, ...]:
        return self.gripper_indices if self.gripper_unit == "normalized_0_1" else ()

    @property
    def so101_cameras(self) -> tuple[str, str] | None:
        """Its side and wrist camera keys when `dreamscale run so101` drives it (the SO-101
        preset, whichever slots its bundle renders them in), else None."""
        if self.preset != "so101":
            return None
        cameras = preset_cameras(self.preset, self.bundle_layout)
        return tuple(key for key, _, _ in cameras)  # type: ignore[return-value]

    @classmethod
    def from_json(cls, data):
        if not isinstance(data, dict) or data.get("base_model") != ISAAC05_BASE_MODEL or (
            data.get("source_format", ISAAC05_SOURCE_FORMAT) != ISAAC05_SOURCE_FORMAT
        ):
            raise ValueError("the server returned no Isaac 0.5 deployment contract")
        try:
            values = {key: data[key] for key in _FIELDS}
            result = cls(
                **{**values, "image_hw": tuple(values["image_hw"]),
                   "action_layout": tuple(values["action_layout"])},
                cameras=tuple(Isaac05Camera.model_validate(camera) for camera in data["cameras"]),
                rtc_max_delay=data.get("rtc_max_delay"),
                joint_unit=data.get("joint_unit"),
                gripper_unit=data.get("gripper_unit"),
                gripper_indices=tuple(data.get("gripper_indices") or ()),
                bundle_layout=data.get("layout"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete Isaac 0.5 deployment contract") from error
        if (
            any(type(value) is not int or not 1 <= value <= bound for value, bound in (
                (result.state_dim, MAX_STATE_DIM),
                (result.action_dim, MAX_ACTION_DIM),
                (result.model_horizon, MAX_MODEL_HORIZON),
                (result.executed_actions, result.model_horizon),
            ))
            or result.model_horizon < 2
            or result.n_obs_steps not in CONTEXT_FRAMES
            or isinstance(result.action_hz, bool)
            or not isinstance(result.action_hz, int | float)
            or not math.isfinite(result.action_hz)
            or not 1 <= result.action_hz <= 100
            or result.action_space not in ("model_defined", "absolute_joint_position")
            or (result.joints and (not result.joint_unit or result.state_dim != result.action_dim))
            or not 1 <= len(result.cameras) <= MAX_CAMERAS
            or len(set(result.camera_keys)) != len(result.cameras)
            or len(result.action_layout) != result.action_dim
            or any(type(i) is not int or not 0 <= i < result.action_dim
                   for i in result.gripper_indices)
            or result.preset not in PRESETS
            or result.frame not in ("none", "so101_model_frame_v1")
            or type(result.trained_rtc_max_delay) is not int
            or not 0 <= result.trained_rtc_max_delay <= MAX_PACKAGE_RTC_DELAY
        ):
            raise ValueError("invalid Isaac 0.5 deployment shape or action contract")
        if result.preset in PRESET_FIELDS and (
            tuple((c.key, c.view, c.slot) for c in result.cameras)
            != preset_cameras(result.preset, result.bundle_layout)
            # The fields the block carries (the dataset and robot type stay on the server).
            or any(getattr(result, key) != value
                   for key, value in PRESET_FIELDS[result.preset].items()
                   if key in cls.__dataclass_fields__)
        ):
            raise ValueError(f"the server's {result.preset} Isaac 0.5 deployment isn't that "
                             "robot's wire")
        if result.rtc_method == "off":
            if result.rtc_max_delay is not None:
                raise ValueError("an Isaac 0.5 deployment with RTC off has no prefix cap")
        elif result.rtc_method not in ("trained", "test_time") or (
            type(result.rtc_max_delay) is not int
            or not 1 <= result.rtc_max_delay <= (
                result.trained_rtc_max_delay if result.rtc_method == "trained"
                else MAX_MODEL_HORIZON - 1
            )
        ):
            raise ValueError(
                f"the server returned an unknown RTC setting {result.rtc_method!r} for this "
                "Isaac 0.5 deployment"
            )
        return result


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, Isaac05SessionDeployment):
        deployment = Isaac05SessionDeployment.from_json(deployment)
    hold = "current_position" if deployment.joints else "wait"
    # Both RTC methods ride the late-bound prefix contract (test-time: the server guides).
    trained = deployment.rtc_method in ("trained", "test_time")
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
        raise ValueError("Isaac 0.5 runtime differs from the deployment's sealed contract")
    layout = deployment.layout
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit if deployment.joints else None,
        normalized_gripper_indices=deployment.normalized_gripper_indices,
        task_prepare_timeout_s=TASK_PREPARE_TIMEOUT_S,
        observation_frames=deployment.n_obs_steps,
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


def catalog_runtime_contract(resolved, deployment):
    """The isaac-0.5-yam catalog model's contract: its deployment's, run in sync by default
    (each chunk to its end, as Perceptron's own loop runs it); ``--mode async`` replans with
    the deployment's training-time RTC."""
    return replace(runtime_contract(resolved, deployment), default_mode="sync")
