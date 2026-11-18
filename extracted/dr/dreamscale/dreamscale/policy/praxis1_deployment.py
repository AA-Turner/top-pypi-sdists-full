"""A Praxis-1 deployment's server-described contract: each session's deployment block
is its checkpoint's own robot (cameras by role, widths, joint names, grippers, units), read as
the server sends it.

The session is the catalog Praxis-1 pools' (``praxis_episode_v1``): the unit keeps the episode,
every executed step's frames ride ahead (``episode_tick_steps`` 1), each request carries the
states of the steps executed since the last one (``measured_state_steps`` 24), and the robot
replans with rows still queued (``min_replan_steps``); 24 rows a chunk, at most 21 executed.

RTC is off, or trained (experimental): the shared late-bound prefix contract, each
request carrying at most ``rtc_max_delay`` committed rows, the deployment's cap in whole 4-row
action tokens within what its export trained."""

from __future__ import annotations

from dataclasses import dataclass

from dreamscale_core.praxis1_deploy import (
    ACTION_HORIZON,
    ACTION_HZ,
    EXECUTION_HORIZON,
    HOLD,
    MAX_CAMERAS,
    MAX_DIM,
    MIN_REPLAN_STEPS,
    PRAXIS1_BASE_MODEL,
    RTC_MAX_PREFIX_ROWS,
    RTC_TOKEN_ROWS,
    Praxis1Camera,
    rtc_contract_for,
)
from dreamscale_core.praxis1_deploy import (
    WIRE_IMAGE as _WIRE_LAYOUT,
)
from dreamscale_transport.images import WireImage

WIRE_IMAGE = WireImage.from_layout(_WIRE_LAYOUT)


def _rtc_valid(method, cap, trained) -> bool:
    """Off with no cap, or trained with a cap of whole action tokens within what the export
    trained (``trained_rtc_max_delay``, where the server says)."""
    if method == "off":
        return cap is None
    bound = RTC_MAX_PREFIX_ROWS
    if trained is not None:
        if type(trained) is not int or not 0 < trained <= RTC_MAX_PREFIX_ROWS:
            return False
        bound = trained
    return (method == "trained" and type(cap) is int and RTC_TOKEN_ROWS <= cap <= bound
            and cap % RTC_TOKEN_ROWS == 0)


@dataclass(frozen=True)
class Praxis1SessionDeployment:
    id: str
    cameras: tuple[Praxis1Camera, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    joint_unit: str | None
    # Off, or trained: the late-bound prefix, at most ``rtc_max_delay`` committed rows held.
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
        if not isinstance(data, dict) or data.get("base_model") != PRAXIS1_BASE_MODEL:
            raise ValueError("the server returned no Praxis-1 deployment contract")
        try:
            result = cls(
                **{key: data[key] for key in (
                    "id", "state_dim", "action_dim", "action_horizon", "executed_actions",
                    "action_hz", "action_space",
                )},
                cameras=tuple(Praxis1Camera.model_validate(camera, strict=False)
                              for camera in data["cameras"]),
                joint_unit=data.get("joint_unit"),
                rtc_method=data.get("rtc_method"),
                rtc_max_delay=data.get("rtc_max_delay"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete Praxis-1 deployment contract") from error
        if (
            any(type(value) is not int or not 1 <= value <= bound for value, bound in (
                (result.state_dim, MAX_DIM), (result.action_dim, MAX_DIM),
                (result.executed_actions, EXECUTION_HORIZON),
            ))
            or result.action_horizon != ACTION_HORIZON
            or float(result.action_hz) != float(ACTION_HZ)
            or result.action_space not in HOLD
            or (result.joints and not result.joint_unit)
            or not 1 <= len(result.cameras) <= MAX_CAMERAS
            or len(set(result.camera_keys)) != len(result.cameras)
            or not _rtc_valid(result.rtc_method, result.rtc_max_delay,
                              data.get("trained_rtc_max_delay"))
        ):
            raise ValueError("invalid Praxis-1 deployment shape or action contract")
        return result


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, Praxis1SessionDeployment):
        deployment = Praxis1SessionDeployment.from_json(deployment)
    hold = HOLD[deployment.action_space]
    # Trained: the session runs the late-bound prefix contract, so the policy's queue sends its
    # committed rows (at most the deployment's cap); off: no RTC.
    contract = rtc_contract_for(deployment.rtc_method)
    expected = {
        "backend": "pytorch", "rtc": "on" if contract else "off", "rtc_contract": contract,
        "action_hz": deployment.action_hz, "chunk_size": deployment.action_horizon,
        "action_dim": deployment.action_dim, "action_space": deployment.action_space,
        "hold_behavior": hold,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("Praxis-1 runtime differs from the deployment's sealed contract")
    return RuntimeContract(
        action_hz=deployment.action_hz,
        chunk_size=deployment.action_horizon,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit,
        wire_image=WIRE_IMAGE,
        episode_tick_steps=1,
        measured_state_steps=ACTION_HORIZON,
        min_replan_steps=MIN_REPLAN_STEPS,
    )


# `dreamscale run xarm7`: a Praxis-1 export of bimanual xArm 7 recordings, 16 joint targets aft
# arm first (seven radians and a 0–1 gripper per arm; the rig's state reads each gripper in
# radians, 0 open to 0.85 closed, as the recordings do). Its cameras by role: the rig's top
# (scene) camera is the base tile, its left (fore wrist) the left wrist, its right (aft wrist)
# the right wrist. Each frame is letterboxed to 224 x 224 as the recordings stored it.
XARM7_ROLES = {"top": "base", "left": "left_wrist", "right": "right_wrist"}
XARM7_WIDTH = 16


def _get(value, key):
    from collections.abc import Mapping

    return value.get(key) if isinstance(value, Mapping) else getattr(value, key, None)


def xarm7_camera_keys(deployment) -> dict[str, str] | None:
    """The deployment's camera key for each of the xArm 7 rig's cameras (top, left = fore
    wrist, right = aft wrist), by the roles its export trained, when `dreamscale run xarm7`
    drives it, else None: sixteen joint targets in radians with 0–1 grippers, one camera per
    role. ``deployment`` is a deployment row's ``embodiment`` or a session's
    Praxis1SessionDeployment."""
    cameras = tuple(_get(deployment, "cameras") or ())
    by_role = {str(_get(camera, "role")): str(_get(camera, "key")) for camera in cameras}
    if (
        _get(deployment, "action_space") != "absolute_joint_position"
        or _get(deployment, "joint_unit") != "rad"
        or _get(deployment, "gripper_unit") not in (None, "normalized")
        or not _get(deployment, "state_dim") == _get(deployment, "action_dim") == XARM7_WIDTH
        or len(cameras) != len(XARM7_ROLES)
        or set(by_role) != set(XARM7_ROLES.values())
    ):
        return None
    return {rig: by_role[role] for rig, role in XARM7_ROLES.items()}


def xarm7_deployment_observe(rig, runner):
    """`dreamscale run xarm7`'s observe for a Praxis-1 deployment: the rig's frames under the
    connected deployment's keys, letterboxed as recorded, and the rig's state as read.
    ``runner``: () -> the task runner."""
    from dreamscale import errors
    from dreamscale.policy.flux3_deployment import xarm7_observation

    def observe(ctx=None):
        keys = xarm7_camera_keys(getattr(runner().policy, "deployment", None))
        if keys is None:
            raise errors.DreamscaleError(errors.ErrorInfo(
                code="invalid_deployment",
                problem="this deployment isn't bimanual xArm 7 joint targets from base, left "
                "wrist and right wrist cameras",
                cause="`dreamscale run xarm7` drives Praxis-1 deployments of bimanual xArm 7 "
                "recordings only",
                fix="drive it from Python: dreamscale.connect(...), then policy.next_action(...)",
            ))
        return xarm7_observation(rig.observe(ctx), keys)

    return observe
