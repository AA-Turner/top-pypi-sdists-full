"""Xiaomi-Robotics-1 deployments of the bimanual YAM preset on `dreamscale run yam`.

An XR-1 deployment of the YAM preset (``dreamscale_transport.xr1_deploy``: ``preset
bimanual_yam``, frame ``YAM_EE_FRAME``) never sees the rig's joint targets. Each request carries
a 32-value state, per arm (left, then right): its six joints (rad), its gripper (0-1), then its
end-effector xyz (m) and rotation as 6D (the rotation matrix's first two columns). Each chunk
row is 20 absolute end-effector targets, per arm xyz, 6D and gripper (``absolute_eef_6d``);
between chunks the arms hold their measured pose (``current_position``).

The pose is each arm's gripper body in its own base: ``model_T_base · base_T_site(q) ·
site_T_tool`` from I2RT's FK at the YAM runner's built-in end-effector profile, the very
kinematics managed training computes its YAM preset's poses with
(``xr1_training.kinematics.YamKinematics``), so a deployment's state is its training data's.
Execution is the YAM runner's own pose executor (``yam_end_effector.YamEndEffectorAdapter``):
each row's poses become joints by I2RT's seeded IK (seeded from the measured joints, then from
the previous row), verified by FK, with the gripper passed through in 0-1 and clipped to it;
every row passes the rig's strict ``validate_action`` before it is queued, and the rig's
joint-step and velocity guards still apply at dispatch.

Trained RTC: the run loop commits the server's own absolute rows (its chunk's
``reference_actions``), which the server re-expresses against the next request's pose.

``dreamscale.deploy_bases.xr1`` declares this module as XR-1's YAM adapter
(``DeployBase.robot_adapters``), which ``yam_runner`` reads.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import numpy as np
from dreamscale_transport import xr1_deploy as C

# The built-in YAM end-effector profile is keyed by the checkpoint it was verified for; managed
# training's YAM preset computes its poses with that same profile (xr1_training.kinematics).
from dreamscale_transport.rho_checkpoints import RHO_YAM_BOX_MODEL_ID

from dreamscale import errors
from dreamscale.policy.cartesian import PoseApproximation
from dreamscale.policy.runtime.contract import RuntimeContract
from dreamscale.robot import RobotObservation

from .yam_end_effector import (
    I2rtKinematics,
    YamEndEffectorAdapter,
    _JointExecutionPolicy,
    builtin_end_effector_profile,
)

NAME = C.XR1_BASE_MODEL
LABEL = C.XR1_PUBLIC_NAME
# The rig the YAM preset's kinematics describe (training's YAM_ARM_TYPE, YAM_GRIPPER_TYPE).
ARM_TYPE, GRIPPER_TYPE = "YAM", "LINEAR_4310"
SIDES = (("left", 0), ("right", 7))
JOINTS = 14
STATE_DIM = C.STATE_DIM
POSE_ROW = C.ACTION_DIM
# The rig's camera role for each of the preset's views (its keys are C.CAMERAS').
ROLES = {"ego": "top", "left_wrist": "left", "right_wrist": "right"}
# The YAM runner's managed budget for pose policies: a seeded, joint-bounded IK candidate is
# admitted even where the solver stops short of the pose (every adjustment is recorded).
MANAGED_POSE_APPROXIMATION = PoseApproximation(None, None)


def _python_fix(checkpoint_id: str | None) -> str:
    ref = checkpoint_id or "<its id>"
    return (f'drive it from Python: dreamscale.connect("{NAME}", deployment="{ref}"), then '
            "policy.next_action(...) with your robot's state "
            "(dreamscale.policy.xr1_deployment.robot_state)")


def _refuse(problem: str, cause: str, fix: str, code: str = "invalid_deployment"):
    return errors.DreamscaleError(errors.ErrorInfo(code=code, problem=problem, cause=cause,
                                                   fix=fix))


def require_yam_rig(config) -> None:
    """Refuse a rig that isn't two YAM arms with LINEAR_4310 grippers: the preset's poses are
    that robot's kinematics."""
    arms = getattr(config, "arms", None) or {}
    if set(arms) != {"left", "right"} or any(
        arm.arm_type != ARM_TYPE or arm.gripper_type != GRIPPER_TYPE for arm in arms.values()
    ):
        raise _refuse(
            f"this rig isn't two {ARM_TYPE} arms with {GRIPPER_TYPE} grippers",
            f"{LABEL}'s bimanual YAM preset was trained on that robot's end-effector "
            "kinematics; another arm or gripper puts the poses elsewhere",
            "set the rig up as two YAM arms with linear grippers (`dreamscale robots yam "
            "setup`), or drive the deployment from Python with your robot's own poses",
            code="invalid_rig",
        )


def require_yam_deployment(deployment: Any) -> None:
    """Refuse a deployment `dreamscale run yam` can't drive: one that isn't the bimanual YAM
    preset, or whose end-effector frame isn't ``YAM_EE_FRAME``."""
    checkpoint_id = getattr(deployment, "id", None)
    preset = getattr(deployment, "preset", None)
    if preset != C.PRESET:
        raise _refuse(
            f"this {LABEL} deployment is for a custom robot, not bimanual YAM",
            f"`dreamscale run yam` drives {LABEL} deployments of the {C.PRESET} preset only "
            "(its cameras, arms, end-effector frame and units)",
            _python_fix(checkpoint_id),
        )
    frame = getattr(deployment, "ee_frame", None)
    if frame != C.YAM_EE_FRAME:
        raise _refuse(
            f"this {LABEL} deployment's end-effector poses are in frame {frame!r}, not "
            f"{C.YAM_EE_FRAME!r}",
            f"`dreamscale run yam` computes and executes poses in {C.YAM_EE_FRAME} (each arm's "
            "gripper body in its own base, I2RT's YAM model), as managed training does",
            _python_fix(checkpoint_id),
        )


@dataclass(frozen=True)
class Xr1YamObservation(RobotObservation):
    """The rig's three frames under the preset's camera keys and the 32-value state, with the
    measured joints (the rig's hold) and each camera's capture time."""

    measured_joints: tuple[float, ...] = ()
    camera_capture_times_ns: tuple[int, ...] | None = None

    @property
    def hold_action(self) -> tuple[float, ...]:
        """The rig's 14 measured values (per arm six joints, then the gripper)."""
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


class _Xr1JointPolicy(_JointExecutionPolicy):
    """The YAM pose executor's session wrapper, with trained RTC: the committed rows the run
    loop sends are the server's own absolute rows (each chunk keeps its raw
    ``reference_actions``), never the executed joints."""

    async def _predict_chunk_with_queue_depth(self, observation, **kwargs):
        rtc = kwargs.get("rtc_context")
        rows = getattr(rtc, "reference_actions", None) if rtc is not None else None
        if rtc is not None and rtc.enabled and rows and any(len(r) != POSE_ROW for r in rows):
            raise _refuse(
                f"{LABEL}'s committed rows must be its {POSE_ROW}-value end-effector rows",
                "the run committed rows of another width",
                "run it with --rtc off",
                code="invalid_rtc",
            )
        predictor = getattr(self.remote, "_predict_chunk_with_queue_depth", None)
        if predictor is None:
            chunk = await self.remote.predict(
                observation, instruction=kwargs["instruction"], timeout_s=kwargs["timeout_s"]
            )
        else:
            chunk = await predictor(observation, **kwargs)
        return await self._convert(chunk)


class Xr1YamAdapter:
    """The 32-value state of the rig's joints (FK) and the joint targets of each 20-value pose
    row (seeded IK), over the YAM runner's pose executor with the built-in profile."""

    def __init__(self, config, *, kinematics_factory=I2rtKinematics,
                 pose_approximation=MANAGED_POSE_APPROXIMATION):
        require_yam_rig(config)
        profile = {
            **builtin_end_effector_profile(RHO_YAM_BOX_MODEL_ID, config),
            "model_id": NAME, "coordinate_frame": C.YAM_EE_FRAME,
            "gripper_unit": C.GRIPPER_UNIT,
        }
        # Validates the profile against the rig before loading a solver (I2RT, MuJoCo, Mink).
        self.pose = YamEndEffectorAdapter.from_profile(
            profile, config, kinematics_factory=kinematics_factory,
            expected_model_id=NAME, expected_coordinate_frame=C.YAM_EE_FRAME,
            expected_gripper_unit=C.GRIPPER_UNIT, pose_approximation=pose_approximation,
        )

    # What the attended runner records with each conversion.
    @property
    def calibration_id(self) -> str:
        return self.pose.calibration_id

    @property
    def pose_approximation(self) -> PoseApproximation | None:
        return self.pose.pose_approximation

    # -- conversions -----------------------------------------------------------------------

    def state(self, measured) -> tuple[float, ...]:
        """The 32-value state of the rig's 14 measured values: per arm (left, then right) its
        six joints, its gripper, its end-effector xyz and 6D rotation in ``YAM_EE_FRAME``."""
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
        for side, offset in SIDES:
            out += [*values[offset:offset + 6], getattr(poses, f"{side}_gripper"),
                    *getattr(poses, f"{side}_position"), *getattr(poses, f"{side}_rotation_6d")]
        return tuple(float(v) for v in out)

    def joint_chunk(self, rows, seed, validate, **options):
        """Pose rows (each ``POSE_ROW`` values) as the rig's 14-value joint targets: the YAM
        pose executor's seeded IK, every row validated before any is returned."""
        return self.pose.joint_chunk(rows, seed, validate, **options)

    def observe(self, observation) -> Xr1YamObservation:
        """The rig's observation (``YamRig.observe``) as the deployment's."""
        measured = tuple(float(v) for v in observation.hold_action)
        times = getattr(observation, "camera_capture_times_ns", None)
        return Xr1YamObservation(
            cameras=tuple((key, getattr(observation, f"{ROLES[view]}_frame"))
                          for key, view in C.CAMERAS),
            state=self.state(measured),
            actions_remaining=getattr(observation, "actions_remaining", 0),
            capture_time_ns=int(max(times)) if times else None,
            measured_joints=measured,
            camera_capture_times_ns=tuple(int(t) for t in times) if times else None,
        )

    # -- the run ---------------------------------------------------------------------------

    def provisional_contract(self) -> RuntimeContract:
        """The rig's side before a session names its rate and chunk: the preset's defaults."""
        return self.pose.execution_contract(RuntimeContract(
            action_hz=float(C.ACTION_HZ), chunk_size=C.DEFAULT_EXECUTED_ACTIONS,
            action_dim=POSE_ROW, action_space=C.ACTION_SPACE, hold_behavior=C.HOLD_BEHAVIOR,
            fixed_rate=True, execution_horizon=C.DEFAULT_EXECUTED_ACTIONS,
        ))

    def require_session(self, policy) -> None:
        """Refuse a connected session whose deployment this rig can't run."""
        require_yam_deployment(getattr(policy, "deployment", None))

    def bind(self, policy, rig, *, on_conversion=None):
        self.require_session(policy)
        wrapped = _Xr1JointPolicy(
            policy, rig, self.pose, getattr(policy, "runtime_contract", None), on_conversion,
        )
        # Connected while the arms are closed: the first conversion binds their bounds.
        if isinstance(getattr(rig, "limits", None), dict) and rig.limits:
            wrapped.bind_limits()
        return wrapped


# The end-effector adapter `dreamscale run yam` runs XR-1 deployments through
# (deploy_bases: DeployBase.robot_adapters); yam_runner constructs it with the rig's config.
ADAPTER = Xr1YamAdapter
