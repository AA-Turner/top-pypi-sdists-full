"""A Praxis-1 deployment's server-described contract (DSL-422): each session's deployment block
is its checkpoint's own robot (cameras by role, widths, joint names, grippers, units), read as
the server sends it.

The session is the catalog Praxis-1 pools' (``praxis_episode_v1``): the unit keeps the episode,
every executed step's frames ride ahead (``episode_tick_steps`` 1), each request carries the
states of the steps executed since the last one (``measured_state_steps`` 24), and the robot
replans with rows still queued (``min_replan_steps``); 24 rows a chunk, at most 21 executed.

RTC is off, or trained (DSL-422 T2, experimental): the shared late-bound prefix contract, each
request carrying at most ``rtc_max_delay`` committed rows, the deployment's cap in whole 4-row
action tokens within what its export trained."""

from __future__ import annotations

from dataclasses import dataclass

from dreamscale_transport.praxis1_deploy import (
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
    WIRE_IMAGE,
    Praxis1Camera,
    rtc_contract_for,
)


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
