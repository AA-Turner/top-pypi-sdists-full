"""Verne V0.5 deployments of the bimanual YAM preset on `dreamscale run yam`.

A Verne V0.5 deployment (``dreamscale_transport.verne_v05_deploy``) reads and returns absolute
tool poses, both arms in one robot frame: the left arm's base. Each request carries a 20-value
state, per arm (left, then right) xyz in metres, the first two rows of the rotation matrix and
the jaw opening (0 closed, 1 open); each chunk row is 21 values, the same per arm, then the
instruction's progress.

The tool frame is I2RT's ``grasp_site`` (its axes are Verne's: +z along the approach, +x down
and +y left when the gripper points forward and level), the frame Verne's YAM training data
records. The right arm's base sits at the rig's mount in the left base's frame: a translation
of the arm spacing along -y (0.615 m by default; ``--arm-spacing`` or the rig's calibration for
another rig). Execution is the YAM runner's own pose executor
(``yam_end_effector.YamEndEffectorAdapter``) with that profile: each row's poses become joints
by I2RT's seeded IK (seeded from the measured joints, then from the previous row), verified by
FK, the jaw passed through in 0-1; every row passes the rig's ``validate_action`` before it is
queued, and the rig's joint-step and velocity guards still apply at dispatch.

Trained RTC: the run loop commits the server's own absolute rows (its chunk's
``reference_actions``), which the server re-expresses against the next request's pose.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, replace
from typing import Any

import numpy as np
from dreamscale_transport import verne_v05_deploy as C

from dreamscale import errors
from dreamscale.policy.cartesian import PoseApproximation
from dreamscale.policy.runtime.contract import RuntimeContract
from dreamscale.robot import RobotObservation

from .yam_end_effector import (
    I2rtKinematics,
    YamEndEffectorAdapter,
    _JointExecutionPolicy,
    pose_from_6d,
    pose_to_6d,
)
from .yam_native import YamHardwareError

NAME = C.VERNE_V05_BASE_MODEL
LABEL = C.VERNE_V05_PUBLIC_NAME
ARM_TYPE, GRIPPER_TYPE = "YAM", "LINEAR_4310"
SIDES = (("left", 0), ("right", 7))
JOINTS = 14
POSE_ROW = 2 * (C.POSE_WIDTH)  # the executor's rows: per arm xyz, 6D (columns), jaw
# The tool frame and robot frame this adapter computes poses in (the fine-tunes' pose frame).
POSE_FRAME = "yam_grasp_site_left_base_v1"
DEFAULT_ARM_SPACING_M = 0.615
ARM_SPACING_ENV = "DREAMSCALE_YAM_ARM_SPACING_M"
ROLES = {"camera_0": "left", "camera_1": "right", "camera_2": "top"}
MANAGED_POSE_APPROXIMATION = PoseApproximation(None, None)


def _python_fix(checkpoint_id: str | None) -> str:
    ref = checkpoint_id or "<its id>"
    return (f'drive it from Python: dreamscale.connect("{NAME}", deployment="{ref}"), then '
            "policy.next_action(...) with your robot's tool poses")


def _refuse(problem: str, cause: str, fix: str, code: str = "invalid_deployment"):
    return errors.DreamscaleError(errors.ErrorInfo(code=code, problem=problem, cause=cause,
                                                   fix=fix))


def arm_spacing() -> float:
    """The rig's arm spacing in metres: ``DREAMSCALE_YAM_ARM_SPACING_M``, else 0.615 m."""
    raw = os.environ.get(ARM_SPACING_ENV)
    value = DEFAULT_ARM_SPACING_M if raw in (None, "") else float(raw)
    if not np.isfinite(value) or not 0.0 < value < 3.0:
        raise _refuse("the YAM arm spacing must be between 0 and 3 metres",
                      f"{ARM_SPACING_ENV}={raw!r}", f"set {ARM_SPACING_ENV} to the distance "
                      "between the two arms' bases, in metres", code="invalid_rig")
    return value


def mount(spacing: float) -> np.ndarray:
    """The right base's pose in the left base's frame: ``spacing`` metres along -y."""
    out = np.eye(4)
    out[1, 3] = -spacing
    return out


def require_yam_rig(config) -> None:
    arms = getattr(config, "arms", None) or {}
    if set(arms) != {"left", "right"} or any(
        arm.arm_type != ARM_TYPE or arm.gripper_type != GRIPPER_TYPE for arm in arms.values()
    ):
        raise _refuse(
            f"this rig isn't two {ARM_TYPE} arms with {GRIPPER_TYPE} grippers",
            f"{LABEL}'s bimanual YAM preset reads that robot's grasp-site poses",
            "set the rig up as two YAM arms with linear grippers (`dreamscale robots yam "
            "setup`), or drive the deployment from Python with your robot's own poses",
            code="invalid_rig",
        )


def require_yam_deployment(deployment: Any) -> None:
    checkpoint_id = getattr(deployment, "id", None)
    frame = getattr(deployment, "ee_frame", None)
    if frame not in (None, POSE_FRAME):
        raise _refuse(
            f"this {LABEL} deployment's poses are in frame {frame!r}, not {POSE_FRAME!r}",
            "`dreamscale run yam` computes poses at YAM's grasp site in the left base, as "
            "Verne's YAM training does",
            _python_fix(checkpoint_id),
        )
    if getattr(deployment, "preset", None) != C.PRESET:
        raise _refuse(
            f"this {LABEL} deployment is for a custom robot, not bimanual YAM",
            f"`dreamscale run yam` drives {LABEL} deployments of the {C.PRESET} preset only",
            _python_fix(checkpoint_id),
        )


def verne_row(pose: np.ndarray, jaw: float) -> list[float]:
    """A [4, 4] pose and a jaw opening as Verne's 10 values (xyz, rotation rows 0-1, jaw)."""
    return [*C.row_from_pose(pose).tolist(), float(jaw)]


def profile(config, spacing: float) -> dict:
    """The executor's profile: the grasp site as the tool, the left base as the model frame."""
    return {
        "version": 1,
        "model_id": NAME,
        "coordinate_frame": POSE_FRAME,
        "gripper_unit": C.GRIPPER_UNIT,
        "calibration_id": f"verne-v05-grasp-site-left-base-{spacing:.3f}m",
        "arms": {
            side: {
                "can_interface": arm.can_interface,
                "arm_type": arm.arm_type,
                "gripper_type": arm.gripper_type,
                "site_name": "grasp_site",
                "model_T_base": (np.eye(4) if side == "left" else mount(spacing)).tolist(),
                "site_T_tool": np.eye(4).tolist(),
                "gripper_closed": 0.0,
                "gripper_open": 1.0,
            }
            for side, arm in config.arms.items()
        },
    }


@dataclass(frozen=True)
class VerneYamObservation(RobotObservation):
    """The rig's frames under the preset's camera keys and the 20-value pose state, with the
    measured joints (the rig's hold) and each camera's capture time."""

    measured_joints: tuple[float, ...] = ()
    camera_capture_times_ns: tuple[int, ...] | None = None

    @property
    def hold_action(self) -> tuple[float, ...]:
        return self.measured_joints

    @property
    def joint_positions(self) -> tuple[float, ...]:
        return self.measured_joints

    def to_wire(self, *, session_id: str, observation_id: int, instruction: str):
        out = super().to_wire(session_id=session_id, observation_id=observation_id,
                              instruction=instruction)
        times = self.camera_capture_times_ns
        if times is None:
            return out
        cameras = [camera.model_copy(update={"capture_time_ns": int(time)})
                   for camera, time in zip(out.frame.cameras, times, strict=True)]
        return replace(out, frame=out.frame.model_copy(update={
            "cameras": cameras, "capture_time_ns": int(max(times)),
        }))


class _VerneJointPolicy(_JointExecutionPolicy):
    """The YAM pose executor's session wrapper: Verne's 21-value rows (rotation rows, then
    progress) become the executor's 20-value rows (rotation columns) before IK."""

    async def _predict_chunk_with_queue_depth(self, observation, **kwargs):
        predictor = getattr(self.remote, "_predict_chunk_with_queue_depth", None)
        if predictor is None:
            chunk = await self.remote.predict(
                observation, instruction=kwargs["instruction"], timeout_s=kwargs["timeout_s"])
        else:
            chunk = await predictor(observation, **kwargs)
        return await self._convert(chunk)


class VerneYamAdapter:
    """The 20-value pose state of the rig's joints (FK) and the joint targets of each 21-value
    pose row (seeded IK), over the YAM runner's pose executor."""

    def __init__(self, config, *, kinematics_factory=I2rtKinematics,
                 pose_approximation=MANAGED_POSE_APPROXIMATION, spacing: float | None = None):
        require_yam_rig(config)
        self.spacing = arm_spacing() if spacing is None else float(spacing)
        self.pose = YamEndEffectorAdapter.from_profile(
            profile(config, self.spacing), config, kinematics_factory=kinematics_factory,
            expected_model_id=NAME, expected_coordinate_frame=POSE_FRAME,
            expected_gripper_unit=C.GRIPPER_UNIT, pose_approximation=pose_approximation,
        )

    @property
    def calibration_id(self) -> str:
        return self.pose.calibration_id

    @property
    def pose_approximation(self) -> PoseApproximation | None:
        return self.pose.pose_approximation

    def state(self, measured) -> tuple[float, ...]:
        """The rig's 14 measured values as Verne's 20-value state in the robot frame."""
        values = np.asarray(measured, dtype=np.float64)
        if values.shape != (JOINTS,) or not np.isfinite(values).all():
            raise _refuse(
                f"{LABEL} on YAM needs the rig's {JOINTS} measured values",
                "the observation's joints aren't six joints and a gripper per arm",
                "observe through the YAM rig (`dreamscale run yam`)",
                code="invalid_observation",
            )
        poses = self.pose.state(values)
        out: list[float] = []
        for side, _ in SIDES:
            pose = pose_from_6d([*getattr(poses, f"{side}_position"),
                                 *getattr(poses, f"{side}_rotation_6d")])
            out += verne_row(pose, getattr(poses, f"{side}_gripper"))
        return tuple(float(v) for v in out)

    @staticmethod
    def executor_rows(rows) -> list[list[float]]:
        """Verne's rows (per arm xyz, rotation rows 0-1, jaw; then progress) as the executor's
        (per arm xyz, rotation columns 0-1, jaw)."""
        out = []
        for row in rows:
            values = np.asarray(row, np.float64)
            converted: list[float] = []
            for arm in range(2):
                span = values[arm * C.POSE_WIDTH:(arm + 1) * C.POSE_WIDTH]
                converted += [*pose_to_6d(C.pose_from_row(span[:9])), float(span[9])]
            out.append(converted)
        return out

    def joint_chunk(self, rows, seed, validate, **options):
        return self.pose.joint_chunk(self.executor_rows(rows), seed, validate, **options)

    def observe(self, observation) -> VerneYamObservation:
        measured = tuple(float(v) for v in observation.hold_action)
        times = getattr(observation, "camera_capture_times_ns", None)
        return VerneYamObservation(
            cameras=tuple((key, getattr(observation, f"{ROLES[feature]}_frame"))
                          for key, feature in C.CAMERAS),
            state=self.state(measured),
            actions_remaining=getattr(observation, "actions_remaining", 0),
            capture_time_ns=int(max(times)) if times else None,
            measured_joints=measured,
            camera_capture_times_ns=tuple(int(t) for t in times) if times else None,
        )

    def execution_contract(self, policy_contract) -> RuntimeContract:
        """The arms' joint contract for Verne's bimanual rows (21 values held by waiting):
        the executor's, for the pose rows ``executor_rows`` gives it (20 values)."""
        if (
            not isinstance(policy_contract, RuntimeContract)
            or policy_contract.action_dim != C.ACTION_DIM
            or policy_contract.action_space != C.ACTION_SPACE
            or policy_contract.hold_behavior != "wait"
        ):
            raise YamHardwareError("Verne V0.5 on the YAM runs its bimanual 21-value contract.")
        return self.pose.execution_contract(replace(
            policy_contract, action_dim=2 * C.POSE_WIDTH, action_space="absolute_eef_6d",
            hold_behavior="current_position"))

    def provisional_contract(self) -> RuntimeContract:
        return self.execution_contract(RuntimeContract(
            action_hz=float(C.ACTION_HZ), chunk_size=C.DEFAULT_EXECUTED_ACTIONS,
            action_dim=C.ACTION_DIM, action_space=C.ACTION_SPACE, hold_behavior="wait",
            fixed_rate=True, execution_horizon=C.DEFAULT_EXECUTED_ACTIONS,
            episode_tick_steps=C.TICK_STEPS,
        ))

    def require_session(self, policy) -> None:
        require_yam_deployment(getattr(policy, "deployment", None))

    def bind(self, policy, rig, *, on_conversion=None):
        self.require_session(policy)
        wrapped = _VerneJointPolicy(
            policy, rig, self, getattr(policy, "runtime_contract", None), on_conversion,
        )
        if isinstance(getattr(rig, "limits", None), dict) and rig.limits:
            wrapped.bind_limits()
        return wrapped

    # The executor's own hooks the joint policy calls through (``_JointExecutionPolicy``).
    def __getattr__(self, name):
        return getattr(self.pose, name)


ADAPTER = VerneYamAdapter
