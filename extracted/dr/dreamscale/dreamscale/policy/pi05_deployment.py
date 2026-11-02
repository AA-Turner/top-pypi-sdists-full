"""π0.5 deployments: the robot a session's deployment serves, from the session response.

A π0.5 deployment (``dreamscale.connect("pi0.5", deployment="ckpt_…")``) is an organization's
own fine-tune with its own robot: cameras (in order, each filling one of the model's image
slots), a state width, and the chunk geometry and rate it was trained at. The control plane
returns that robot with the session (``deployment``), and the SDK checks every observation
against it before anything is sent. Its runtime contract (rate, chunk, width, RTC) comes
from the session's resolved configuration, never from a table in this package.

The SDK's shared code reaches this module through π0.5's deployment base
(``dreamscale.deploy_bases.pi05``: ``DeployBase.session``, ``robot_presets``).
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from dreamscale_transport.pi05_deploy import (
    MAX_ACTION_DIM,
    MAX_CAMERAS,
    MAX_HORIZON,
    MAX_HZ,
    PI05_DEPLOY_SLOTS,
    RTC_METHODS,
    rtc_contract_for,
)
from dreamscale_transport.pi05_rtc import (
    PI05_PRESET_MODELS,
    PI05_RTC_EMBODIMENTS,
    pi05_preset_robot,
    pi05_unit_grippers,
)

from dreamscale.policy.deployment import PresetLayout, joint_actions
from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

# Public names of the base (the internal id is PI05_BASE_MODEL).
PI05_PUBLIC_BASE = "pi0.5"

# The shared models' image slots, by the deployments' names.
_SLOTS = {"top": "base", "left": "left_wrist", "right": "right_wrist"}


def _layout(preset: str, label: str, helper: str, command: str | None, startup: float):
    embodiment = PI05_RTC_EMBODIMENTS[PI05_PRESET_MODELS[preset]]
    unit = pi05_unit_grippers(preset, embodiment.camera_keys, embodiment.action_dim)
    return PresetLayout(
        label=label,
        cameras=tuple(
            (key, _SLOTS[slot])
            for key, slot in zip(embodiment.camera_keys, embodiment.slots, strict=True)
        ),
        action_hz=float(embodiment.action_hz),
        action_dim=embodiment.action_dim,
        joint_groups=embodiment.joint_groups,
        gripper_indices=embodiment.gripper_indices,
        normalized_gripper_indices=unit[0] if unit and unit[1] == (0.0, 1.0) else (),
        joint_unit=embodiment.joint_unit,
        startup_motion_delay_s=startup,
        observe_helper=helper,
        run_command=command,
    )


# A preset fixes the robot's wire: the same robots, units and helpers as the shared π0.5
# models (dreamscale_transport.pi05_rtc). Blank ("custom") has no layout.
PRESET_LAYOUTS: dict[str, PresetLayout] = {
    "bimanual_yam": _layout(
        "bimanual_yam", "Bimanual YAM", "dreamscale.yam.observation", "dreamscale run yam", 0.1
    ),
    "so101": _layout(
        "so101", "SO-101", "dreamscale.so101.observation", "dreamscale run so101", 0.0
    ),
    "arx5": _layout("arx5", "Bimanual ARX5", "dreamscale.arx5.observation", None, 0.1),
}


def robot_preset(
    preset: str | None,
    camera_keys: tuple[str, ...],
    action_dim: int,
    state_dim: int | None = None,
) -> str | None:
    """The preset whose robot this is: its own when it kept the preset's width, else the
    preset whose wire it sends (a preset with an edited rate or geometry is still that
    robot), else None. The server clips grippers by the same rule (``pi05_preset_robot``).
    A deployment whose actions aren't joint targets (``state_dim`` given and different) is
    no preset's robot."""
    if state_dim is not None and not joint_actions(state_dim, action_dim):
        return None
    return pi05_preset_robot(preset, tuple(camera_keys), action_dim)


@dataclass(frozen=True)
class DeploymentCamera:
    key: str
    slot: str


@dataclass(frozen=True)
class SessionDeployment:
    """The ``deployment`` block of a π0.5 deployment session."""

    id: str
    preset: str
    cameras: tuple[DeploymentCamera, ...]
    state_dim: int
    action_dim: int
    executed_actions: int
    action_hz: float
    rtc_method: str
    # The most committed actions a chunk can start with (trained RTC's sealed delay; 0 when
    # RTC isn't trained); None from a server that doesn't send it.
    rtc_max_prefix_rows: int | None = None

    @property
    def camera_keys(self) -> tuple[str, ...]:
        return tuple(camera.key for camera in self.cameras)

    @property
    def joints(self) -> bool:
        """Whether its actions are absolute joint targets (see joint_actions)."""
        return joint_actions(self.state_dim, self.action_dim)

    @property
    def robot(self) -> str | None:
        """The preset robot this deployment drives (see robot_preset), else None."""
        return robot_preset(self.preset, self.camera_keys, self.action_dim, self.state_dim)

    @property
    def layout(self) -> PresetLayout | None:
        """That robot's joint layout, units and observe helper."""
        robot = self.robot
        return None if robot is None else PRESET_LAYOUTS[robot]

    @classmethod
    def from_json(cls, data: Any) -> SessionDeployment:
        """Strict: a block this SDK can't read fails the session (which is then closed)."""
        if not isinstance(data, Mapping):
            raise ValueError("the server returned no deployment for this π0.5 session")
        try:
            cameras = tuple(
                DeploymentCamera(key=str(camera["key"]), slot=str(camera["slot"]))
                for camera in data["cameras"]
            )
            deployment = cls(
                id=str(data["id"]),
                preset=str(data.get("preset") or "custom"),
                cameras=cameras,
                state_dim=_whole(data["state_dim"], 1, MAX_ACTION_DIM),
                action_dim=_whole(data["action_dim"], 1, MAX_ACTION_DIM),
                executed_actions=_whole(data["executed_actions"], 1, MAX_HORIZON),
                action_hz=_rate(data["action_hz"]),
                rtc_method=str(data["rtc_method"]),
                rtc_max_prefix_rows=(
                    None if data.get("rtc_max_prefix_rows") is None
                    else _whole(data["rtc_max_prefix_rows"], 0, MAX_HORIZON)
                ),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                f"the server returned an incomplete deployment for this π0.5 session ({exc})"
            ) from None
        keys = deployment.camera_keys
        slots = [camera.slot for camera in cameras]
        if (
            not 1 <= len(cameras) <= MAX_CAMERAS
            or len(set(keys)) != len(keys)
            or len(set(slots)) != len(slots)
            or any(slot not in PI05_DEPLOY_SLOTS for slot in slots)
        ):
            raise ValueError("the server returned an invalid camera list for this π0.5 deployment")
        if deployment.rtc_method not in RTC_METHODS:
            raise ValueError(
                f"the server returned an unknown RTC method {deployment.rtc_method!r} for this "
                "π0.5 deployment"
            )
        return deployment


def _whole(value: Any, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"{value!r} is not a whole number from {low} to {high}")
    return value


def _rate(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{value!r} is not a rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 < rate <= MAX_HZ:
        raise ValueError(f"{value!r} is not a rate up to {MAX_HZ} Hz")
    return rate


# π0.5 deployments (an organization's own fine-tune): everything — rate, chunk, width, RTC and
# the robot — comes from the session (runtime_contract). This is only what a caller sees
# before a session opens; images go up at capture size.
PREVIEW_CONTRACT = {
    "action_hz": 30.0,
    "chunk_size": 50,
    "action_space": "absolute_joint_position",
    "hold_behavior": "current_position",
}


def control_hz(requested: int | float | None) -> float | None:
    """A deployment's rate is the one it was trained at, which the session reports; a caller
    may ask for another whole rate up to the base's cap."""
    if requested is None:
        return None
    if isinstance(requested, bool) or not isinstance(requested, int | float):
        raise ValueError("control_hz must be an integer")
    if not float(requested).is_integer() or not 1 <= requested <= MAX_HZ:
        raise ValueError(
            f"control_hz must be a whole number of hertz from 1 to {MAX_HZ}; omit "
            "it to run at the rate the deployment was trained at"
        )
    return float(requested)


# What a π0.5 deployment acts in, and how it holds: absolute joint targets (its state and
# action widths are equal) held at the measured position, or the model's own space (any
# other deployment: end-effector deltas, say), which has no hold: a missing action waits.
PI05_DEPLOYMENT_HOLDS = {"absolute_joint_position": "current_position", "model_defined": "wait"}
_PI05_RTC_CONTRACTS = tuple(rtc_contract_for(method) for method in ("trained", "test_time"))


def runtime_contract(
    resolved_config: Any | None, deployment: SessionDeployment | dict | None,
    chunk_size_override: int | None = None,
) -> RuntimeContract:
    """A π0.5 deployment session's contract, entirely from the server: the resolved config
    (rate, chunk = execution horizon, width, RTC) and the deployment block (its robot).

    A deployment whose state and action widths are equal acts in absolute joint targets,
    held at the measured position. Any other (end-effector deltas, say) acts in the
    model's own space: no joint layout, and no hold, so a missing action waits."""
    if not isinstance(deployment, SessionDeployment):
        deployment = SessionDeployment.from_json(deployment)
    space = "absolute_joint_position" if deployment.joints else "model_defined"
    served = _optional_attr(resolved_config, "action_space")
    # Either kind, with its hold, is a complete contract; the wrong kind for this
    # deployment fails below, as a contract that doesn't match it.
    expected = {"backend": "jax", "hold_behavior": PI05_DEPLOYMENT_HOLDS.get(served)}
    dim = _optional_attr(resolved_config, "action_dim")
    chunk = _optional_attr(resolved_config, "chunk_size")
    execution = _optional_attr(resolved_config, "execution_horizon")
    rate = _optional_attr(resolved_config, "action_hz")
    rtc = _optional_attr(resolved_config, "rtc")
    rtc_contract = _optional_attr(resolved_config, "rtc_contract")
    if (
        served not in PI05_DEPLOYMENT_HOLDS
        or any(_optional_attr(resolved_config, key) != value for key, value in expected.items())
        or type(dim) is not int
        or type(chunk) is not int
        or execution not in (None, chunk)
        or isinstance(rate, bool)
        or not isinstance(rate, int | float)
        or rtc not in ("on", "off")
    ):
        raise ValueError("the π0.5 deployment server returned an incomplete runtime contract")
    if (
        dim != deployment.action_dim
        or served != space
        or chunk != deployment.executed_actions
        or float(rate) != deployment.action_hz
        # The session's RTC: off, or one of the two contracts the client loop runs
        # (trained: the late-bound prefix; test-time: the dynamic full horizon).
        or rtc_contract not in ((None,) if rtc == "off" else _PI05_RTC_CONTRACTS)
    ):
        raise ValueError(
            f"the π0.5 deployment server returned a runtime contract that doesn't match "
            f"deployment {deployment.id}"
        )
    layout = deployment.layout  # None for a non-joint deployment
    contract = RuntimeContract(
        action_hz=float(rate),
        chunk_size=chunk,
        execution_horizon=chunk,
        action_dim=dim,
        action_space=space,
        hold_behavior=PI05_DEPLOYMENT_HOLDS[space],
        **(
            {
                "joint_groups": layout.joint_groups,
                "gripper_indices": layout.gripper_indices,
                "normalized_gripper_indices": layout.normalized_gripper_indices,
                "joint_unit": layout.joint_unit,
                "startup_motion_delay_s": layout.startup_motion_delay_s,
            }
            if layout is not None
            else {}
        ),
    )
    if chunk_size_override is not None and chunk_size_override != contract.chunk_size:
        raise ValueError(
            f"this π0.5 deployment executes {contract.chunk_size}-action chunks; omit chunk_size"
        )
    return contract
