"""Hy-VLA pose chunks on the two xArm 7s: FK for the state, blend + seeded IK for execution.

A Hy-VLA deployment (``dreamscale_transport.hy_vla_deploy``) never sees joints. Each request
carries a 20-value pose state (per arm, model order fore then aft: TCP xyz, rotation-matrix
rows 0-1, gripper 0-1) and each chunk row is 40 values: both arms' poses relative to that
request's state (0-19), then absolute in each arm's base frame (20-39). This adapter, in the
shape of ``yam_end_effector.py``, turns the rig's 16 measured joint values (aft first: seven
joints in radians and the gripper's drive_joint radians, then fore) into that state, and
each chunk into 16 joint targets before the run loop sees it, exactly as the checkpoint was
evaluated at delivery:

- the active arm (the instruction's, from the deployment's label map) blends the two heads
  (positions and grippers averaged, rotations slerp 0.5), then solves damped least-squares IK
  row by row, the first row seeded on the measured joints sent with that request;
- the inactive arm holds those measured joints and its current gripper intent;
- an unconverged row is never executed: from the first failed row the arm holds the last
  converged row (the measured joints when row 0 fails or a rotation is degenerate), and the
  failure is reported;
- the whole chunk passes the rig's strict ``validate_action`` before it is queued.

RTC: the run loop's committed joint rows become 40-wide pose rows against the new request's
measured state (``rtc_prefix``); the server normalizes and bf16-rounds them.
"""

from __future__ import annotations

import asyncio
import logging
import threading
from dataclasses import dataclass, replace
from typing import Any

import numpy as np

from dreamscale import errors
from dreamscale.policy.cartesian import CartesianConversion
from dreamscale.policy.run_loop import run_policy_loop
from dreamscale.policy.runtime.contract import RuntimeContract
from dreamscale.robot import RobotObservation

from . import xarm7_kinematics as kinematics
from .xarm_arm import XArmError

log = logging.getLogger(__name__)

PRESET = "bimanual_xarm7"
# The model's arm order (values 0-9 the first arm, 10-19 the second, in each head).
MODEL_ARMS = ("fore", "aft")
# The rig's 16 values: aft joints 0-6, aft gripper 7, fore joints 8-14, fore gripper 15.
RIG_OFFSETS = {"aft": 0, "fore": 8}
GRIPPER_INDICES = (7, 15)
JOINTS = 16
POSE_STATE = 20
POSE_ROW = 40
MAX_ROWS = 20
# What this conversion assumes about the arms (recorded with each IK report).
CALIBRATION_ID = "xarm7-nominal-ufactory-aad7e161-tcp-0.185m"
# The trained instructions a refusal lists before eliding the rest.
LISTED_INSTRUCTIONS = 12


class HyVlaXArm7Error(XArmError):
    """A Hy-VLA chunk or state the xArm 7 adapter refuses."""


def _measured(values) -> np.ndarray:
    raw = np.asarray(values)
    if raw.dtype.kind not in "fiu" or raw.shape != (JOINTS,) or not np.isfinite(raw).all():
        raise HyVlaXArm7Error(
            f"Hy-VLA needs the rig's {JOINTS} measured values (aft then fore: seven joints in "
            "radians and the gripper's drive_joint radians)."
        )
    # The checkpoint was trained and evaluated on float32 states; the same rounding keeps
    # execution identical to its evaluation.
    return raw.astype(np.float32)


def _intent(values) -> np.ndarray:
    intent = np.asarray(values, dtype=np.float32)
    if intent.shape != (2,) or not np.isin(intent, [0, 1]).all():
        raise HyVlaXArm7Error("Hy-VLA needs each gripper's binary intent (aft, fore).")
    return intent


def measured_intent(measured) -> tuple[float, float]:
    """Binary intent (aft, fore) read from the measured gripper: closed past half travel."""
    values = _measured(measured)
    return tuple(
        float(values[index] / kinematics.GRIPPER_CLOSED_RAD >= .5) for index in GRIPPER_INDICES
    )


def rig_intent(rig, measured) -> tuple[float, float]:
    """The rig's last commanded gripper intents (aft, fore), as binary closes. A rig holds
    its gripper at its last command, never its reading (``XArm7Rig.intent``, which starts
    from the reading when nothing was commanded yet); without one, the measured gripper."""
    commanded = getattr(rig, "intent", None)
    if isinstance(commanded, dict) and set(RIG_OFFSETS) <= set(commanded):
        return tuple(float(float(commanded[arm]) >= .5) for arm in ("aft", "fore"))
    return measured_intent(measured)


@dataclass(frozen=True)
class HyVlaXArm7Observation(RobotObservation):
    """The rig's frames with the 20-value pose state the deployment reads, and the measured
    joints and gripper intent the chunk answering it is anchored on and seeded from."""

    measured_joints: tuple[float, ...] = ()
    gripper_intent: tuple[float, float] = (0.0, 0.0)

    @property
    def hold_action(self) -> tuple[float, ...]:
        """The rig's hold: the measured joints with each gripper at its intent."""
        values = list(self.measured_joints)
        for index, intent in zip(GRIPPER_INDICES, self.gripper_intent, strict=True):
            values[index] = float(intent)
        return tuple(values)

    @property
    def joint_positions(self) -> tuple[float, ...]:
        return self.hold_action


@dataclass(frozen=True)
class IkFailure:
    """One chunk whose IK did not converge everywhere: from ``row`` (zero-based) on, the
    active arm holds the last converged row (the measured joints from row 0)."""

    row: int
    rows: int
    active_arm: str
    # As the delivery evaluation reports it (its action numbers count from 0).
    error: str
    # The unconverged row's residual; None for a degenerate predicted rotation.
    position_error_m: float | None = None
    rotation_error_rad: float | None = None
    observation_id: int | None = None
    chunk_id: int | None = None

    @property
    def held_rows(self) -> int:
        return self.rows - self.row

    def describe(self) -> str:
        """One line, actions counted from 1."""
        if self.position_error_m is None:
            where = f"degenerate predicted rotation ({self.error})"
        else:
            where = (
                f"IK did not converge at action {self.row + 1} (off by "
                f"{self.position_error_m * 1000:.1f} mm, {self.rotation_error_rad:.3f} rad)"
            )
        hold = "the measured pose" if self.row == 0 else f"action {self.row}'s pose"
        return (
            f"Hy-VLA {self.active_arm} arm: {where}; holding {hold} for "
            f"{self.held_rows} of {self.rows} actions"
        )


class HyVlaXArm7Adapter:
    """Pure conversions plus ``bind``, which wraps a connected Hy-VLA session for the rig."""

    calibration_id = CALIBRATION_ID
    # IK either converges within 0.1 mm / 1 mrad or the arm holds; nothing is approximated.
    pose_approximation = None

    def __init__(self):
        self._lock = threading.RLock()
        self.last_failure: IkFailure | None = None

    # -- conversions -----------------------------------------------------------------------

    def state(self, measured) -> np.ndarray:
        """The 20-value pose state (fore then aft) of 16 measured joint values."""
        values = _measured(measured)
        state, _ = kinematics.hy_targets(values, values[None])
        return state

    def joint_chunk(self, pose_rows, measured, active_arm, gripper_intent, validate=None):
        """Pose rows (N, 40) to joint rows (N, 16), anchored on and seeded from the measured
        joints sent with the request. Returns (rows as float tuples, IkFailure or None).

        ``validate(row, check_step=False)`` must refuse a row outside the rig's limits; it
        runs on every row before anything is returned (never repairing a solver's joints).
        """
        rows = np.asarray(pose_rows)
        if (
            rows.dtype.kind not in "fiu" or rows.ndim != 2 or rows.shape[1] != POSE_ROW
            or not 1 <= len(rows) <= MAX_ROWS or not np.isfinite(rows).all()
        ):
            raise HyVlaXArm7Error(
                f"Hy-VLA chunks are 1-{MAX_ROWS} finite rows of {POSE_ROW} pose values."
            )
        if active_arm not in MODEL_ARMS:
            raise HyVlaXArm7Error("Hy-VLA moves the fore or the aft arm.")
        state = _measured(measured)
        intent = _intent(gripper_intent)
        rows = rows.astype(np.float32)
        with self._lock:
            joints, failure = kinematics.execute(
                rows[:, :POSE_STATE], rows[:, POSE_STATE:], state, active_arm, intent,
            )
        joints = _undo_float32_rounding(joints, RIG_OFFSETS[active_arm])
        diagnostic = (failure or {}).get("diagnostic") or {}
        report = None if failure is None else IkFailure(
            row=failure["row"], rows=len(rows), active_arm=active_arm, error=failure["error"],
            position_error_m=diagnostic.get("position_error_m"),
            rotation_error_rad=diagnostic.get("rotation_error_rad"),
        )
        actions = tuple(tuple(float(v) for v in row) for row in joints)
        if validate is not None:
            for action in actions:
                validate(action, check_step=False)
        return actions, report

    def rtc_prefix(self, committed, measured) -> np.ndarray:
        """Committed joint rows (k, 16) as pose rows (k, 40) against the NEW request's
        measured state: per row the relative block (re-expressed against that state's pose)
        then the absolute block, each fore then aft (``hy_targets``, before normalization)."""
        rows = np.asarray(committed)
        if (
            rows.dtype.kind not in "fiu" or rows.ndim != 2 or rows.shape[1] != JOINTS
            or not np.isfinite(rows).all()
        ):
            raise HyVlaXArm7Error(f"RTC rows are the run's committed {JOINTS}-value joint rows.")
        if not len(rows):
            return np.zeros((0, POSE_ROW), np.float32)
        _, actions = kinematics.hy_targets(_measured(measured), rows.astype(np.float32))
        return np.concatenate([actions[:len(rows)], actions[len(rows):]], axis=-1)

    def observe(self, observation, *, rig=None, gripper_intent=None) -> HyVlaXArm7Observation:
        """The rig's observation (16 measured values) as the deployment's: the pose state,
        with the measured joints and gripper intent this request's chunk is anchored on."""
        measured = _measured(getattr(observation, "state", ()))
        intent = (
            tuple(float(v) for v in _intent(gripper_intent)) if gripper_intent is not None
            else rig_intent(rig, measured)
        )
        state = self.state(measured)
        return HyVlaXArm7Observation(
            cameras=observation.cameras,
            state=tuple(float(v) for v in state),
            actions_remaining=getattr(observation, "actions_remaining", 0),
            capture_time_ns=getattr(observation, "capture_time_ns", None),
            measured_joints=tuple(float(v) for v in measured),
            gripper_intent=intent,
        )

    # -- the run ---------------------------------------------------------------------------

    @staticmethod
    def provisional_contract(chunk_size=MAX_ROWS) -> RuntimeContract:
        """The rig's side before a session names its chunk: 16 joint targets at 20 Hz."""
        return _joint_contract(action_hz=20.0, chunk_size=chunk_size, fixed_rate=True)

    def execution_contract(self, policy_contract, deployment=None) -> RuntimeContract:
        if (
            not isinstance(policy_contract, RuntimeContract)
            or policy_contract.action_dim != POSE_ROW
            or policy_contract.action_space != "model_defined"
        ):
            raise HyVlaXArm7Error(
                "The xArm 7 Hy-VLA adapter needs a Hy-VLA session (40-wide pose rows)."
            )
        executed = getattr(deployment, "executed_actions", None)
        chunk = policy_contract.execution_chunk_size
        if type(executed) is int and executed != chunk:
            raise HyVlaXArm7Error("The session's chunk differs from the deployment's.")
        return _joint_contract(
            action_hz=policy_contract.action_hz, chunk_size=chunk,
            native_action_hz=policy_contract.native_action_hz,
            fixed_rate=policy_contract.fixed_rate,
        )

    def bind(self, policy, rig, *, on_conversion=None):
        return _HyVlaJointPolicy(policy, rig, self, on_conversion)


def _joint_contract(*, action_hz, chunk_size, native_action_hz=None, fixed_rate=True):
    return RuntimeContract(
        action_hz=float(action_hz),
        chunk_size=int(chunk_size),
        native_action_hz=native_action_hz,
        action_dim=JOINTS,
        action_space="absolute_joint_position",
        hold_behavior="current_position",
        normalized_gripper_indices=GRIPPER_INDICES,
        fixed_rate=fixed_rate,
        joint_groups=(tuple(range(0, 7)), tuple(range(8, 15))),
        gripper_indices=GRIPPER_INDICES,
        joint_unit="rad",
    )


def _undo_float32_rounding(joints, offset):
    """Joint rows as float64. IK clips each joint to [LOWER + .02, UPPER - .02], the rig's
    command limits; float32 rows can round a joint the solver left exactly on that
    bound a few 1e-8 rad outside it. Only that rounding is undone (at most 1e-6 rad)."""
    values = np.asarray(joints, dtype=np.float64)
    low, high = kinematics.LOWER + .02, kinematics.UPPER - .02
    arm = values[:, offset:offset + 7]
    arm[:] = np.where((arm < low) & (arm >= low - 1e-6), low, arm)
    arm[:] = np.where((arm > high) & (arm <= high + 1e-6), high, arm)
    return values


def _deployment_labels(deployment) -> dict[str, str]:
    labels = getattr(deployment, "label_arms", None)
    if labels is None and isinstance(deployment, dict):
        labels = deployment.get("label_arms")
    return dict(labels or ())


def _refuse_instruction(instruction, labels) -> errors.DreamscaleError:
    trained = sorted(labels)
    if not trained:
        return errors.DreamscaleError(errors.ErrorInfo(
            code="invalid_instruction",
            problem="This Hy-VLA deployment records no instruction for either arm, so the "
            "xArm 7s can't tell which arm it moves",
            cause="the deployment's export has no label-to-arm map",
            fix="deploy the checkpoint again from an export with its label map",
        ))
    listed = ", ".join(f'"{label}"' for label in trained[:LISTED_INSTRUCTIONS])
    more = len(trained) - LISTED_INSTRUCTIONS
    if more > 0:
        listed += f" and {more} more"
    return errors.DreamscaleError(errors.ErrorInfo(
        code="invalid_instruction",
        problem=f'"{instruction.strip()}" isn\'t one of this deployment\'s trained '
        f"instructions: {listed}",
        cause="Hy-VLA moves one arm per instruction, chosen by the instructions it was "
        "trained on",
        fix="enter one of the trained instructions",
    ))


class _JointReferences:
    """The server's chunk with its RTC reference rows (``runtime_metadata.reference_actions``,
    which the run loop commits with each action) replaced by the executed joint rows: the
    next request re-expresses the committed physical rows against its own measured state
    (``rtc_prefix``), as the checkpoint was trained and evaluated with the prefix.
    ``pose_chunk`` is the server's own."""

    def __init__(self, chunk, metadata):
        self.pose_chunk = chunk
        self.runtime_metadata = metadata

    def __getattr__(self, name):
        return getattr(self.pose_chunk, name)

    @classmethod
    def of(cls, chunk, actions):
        metadata = getattr(chunk, "runtime_metadata", None)
        if getattr(metadata, "reference_actions", None) is None:
            return chunk  # no RTC on this chunk: nothing is committed for a prefix
        rows = [list(action) for action in actions]
        copy = getattr(metadata, "model_copy", None)
        return cls(chunk, copy(update={"reference_actions": rows}) if callable(copy)
                   else replace(metadata, reference_actions=rows))


class _HyVlaJointPolicy:
    """The connected session, its chunks converted to joint targets before the run loop
    (or a sync run) sees them; RTC reference rows converted back to pose rows."""

    def __init__(self, policy, rig, adapter, on_conversion=None):
        self.remote, self.rig, self.adapter = policy, rig, adapter
        deployment = getattr(policy, "deployment", None)
        preset = getattr(deployment, "preset", None)
        arms = tuple(getattr(deployment, "arms", MODEL_ARMS) or MODEL_ARMS)
        if preset not in (None, PRESET) or arms != MODEL_ARMS:
            raise HyVlaXArm7Error(
                "This Hy-VLA deployment isn't the bimanual xArm 7's (cameras top, left and "
                "right; arms fore then aft); drive it from Python instead."
            )
        self.deployment_labels = _deployment_labels(deployment)
        self.execution_contract = adapter.execution_contract(
            getattr(policy, "runtime_contract", None), deployment,
        )
        if on_conversion is not None and not callable(on_conversion):
            raise HyVlaXArm7Error("IK reports need a callable.")
        self.on_conversion = on_conversion
        # The rig's chunk is the deployment's executed actions, and its control period the
        # deployment's rate (the step its velocity caps allow per row).
        try:
            rig.chunk_size = self.execution_contract.chunk_size
            rig.control_period_s = 1.0 / float(self.execution_contract.action_hz)
        except AttributeError:
            pass
        self.ik_chunks = self.ik_failed_chunks = self.ik_failed_rows = 0
        self.ik_failures: list[IkFailure] = []

    def __getattr__(self, name):
        return getattr(self.remote, name)

    @property
    def last_run_result(self):
        return getattr(self.remote, "last_run_result", None)

    @last_run_result.setter
    def last_run_result(self, value):
        self.remote.last_run_result = value

    # -- instructions ----------------------------------------------------------------------

    def active_arm(self, instruction) -> str:
        """The arm a trained instruction moves; refuses any other instruction."""
        deployment = getattr(self.remote, "deployment", None)
        arm_for = getattr(deployment, "arm_for", None)
        if callable(arm_for):
            arm = arm_for(instruction)
        else:
            from dreamscale_transport.hy_vla_deploy import clean_instruction

            arm = self.deployment_labels.get(clean_instruction(instruction))
        if arm not in MODEL_ARMS:
            raise _refuse_instruction(instruction, self.deployment_labels)
        return arm

    require_instruction = active_arm

    # -- requests --------------------------------------------------------------------------

    @staticmethod
    def _anchor(observation):
        measured = getattr(observation, "measured_joints", None)
        intent = getattr(observation, "gripper_intent", None)
        if not measured or intent is None:
            raise HyVlaXArm7Error(
                "Hy-VLA observations on the xArm 7s come from the adapter's observe(), "
                "which records the measured joints each chunk is anchored on."
            )
        return _measured(measured), _intent(intent)

    def _pose_rtc(self, rtc_context, measured):
        rows = getattr(rtc_context, "reference_actions", None)
        if rtc_context is None or not getattr(rtc_context, "enabled", False) or not rows:
            return rtc_context
        if all(len(row) == POSE_ROW for row in rows):
            return rtc_context  # already pose rows: the session re-expresses them itself
        poses = self.adapter.rtc_prefix(rows, measured)
        return rtc_context.model_copy(update={
            "reference_actions": [[float(v) for v in row] for row in poses],
            "reference_action_valid_steps": len(poses),
        })

    def _joint_actions(self, chunk, measured, intent, arm):
        size = self.execution_contract.chunk_size
        actions, failure = self.adapter.joint_chunk(
            chunk.actions[:size], measured, arm, intent, validate=self._validate,
        )
        self.ik_chunks += 1
        if failure is not None:
            failure = replace(
                failure, observation_id=getattr(chunk, "observation_id", None),
                chunk_id=getattr(chunk, "chunk_id", None),
            )
            self.adapter.last_failure = failure
            self.ik_failed_chunks += 1
            self.ik_failed_rows += failure.held_rows
            if len(self.ik_failures) < 20:
                self.ik_failures.append(failure)
            log.warning(failure.describe())
            self._report(failure)
        return actions

    def _validate(self, action, *, check_step):
        # Strict: a solver's joint outside the rig's limits refuses the chunk, never repaired.
        self.rig.validate_action(action, check_step=check_step, saturate=False)

    def _report(self, failure):
        if self.on_conversion is None:
            return
        try:
            self.on_conversion(CartesianConversion(
                poses=(), accepted=True, error=failure.describe(),
                observation_id=failure.observation_id, chunk_id=failure.chunk_id,
            ))
        except Exception:
            log.warning("Recording an IK report failed; the hold still applies.")

    async def _convert(self, chunk, measured, intent, arm):
        # IK takes milliseconds per row: keep it off the event loop, and drain it before a
        # cancellation lets runner cleanup close the rig.
        conversion = asyncio.create_task(
            asyncio.to_thread(self._joint_actions, chunk, measured, intent, arm)
        )
        try:
            actions = await asyncio.shield(conversion)
        except asyncio.CancelledError:
            await asyncio.gather(conversion, return_exceptions=True)
            raise
        size = self.execution_contract.chunk_size
        indices = None if chunk.action_indices is None else chunk.action_indices[:size]
        return replace(
            chunk, actions=actions, action_indices=indices,
            raw_chunk=_JointReferences.of(chunk.raw_chunk, actions),
        )

    async def predict(self, observation, *, instruction, timeout_s=60.0, **kwargs):
        arm = self.active_arm(instruction)
        measured, intent = self._anchor(observation)
        chunk = await self.remote.predict(
            observation, instruction=instruction, timeout_s=timeout_s, **kwargs
        )
        return await self._convert(chunk, measured, intent, arm)

    async def _predict_chunk_with_queue_depth(self, observation, **kwargs):
        arm = self.active_arm(kwargs["instruction"])
        measured, intent = self._anchor(observation)
        if "rtc_context" in kwargs:
            kwargs["rtc_context"] = self._pose_rtc(kwargs["rtc_context"], measured)
        predictor = getattr(self.remote, "_predict_chunk_with_queue_depth", None)
        if predictor is None:
            chunk = await self.remote.predict(
                observation, instruction=kwargs["instruction"], timeout_s=kwargs["timeout_s"]
            )
        else:
            chunk = await predictor(observation, **kwargs)
        return await self._convert(chunk, measured, intent, arm)

    async def run(self, **kwargs):
        self.active_arm(kwargs["instruction"])
        prepared = getattr(self.remote, "requires_task_preparation", False)
        if prepared:
            await self.remote._prepare_task(instruction=kwargs["instruction"], managed=True)
        try:
            result = await run_policy_loop(
                policy=self, execution_contract=self.execution_contract, **kwargs
            )
            self.remote.last_run_result = result
            return result
        finally:
            if prepared:
                self.remote._prepared_run_active = False


# The end-effector adapter `dreamscale run xarm7` runs Hy-VLA deployments through
# (deploy_bases: DeployBase.robot_adapters).
ADAPTER = HyVlaXArm7Adapter


def describe_failures(policy: Any) -> str | None:
    """One line on a run's IK holds, or None when every chunk converged."""
    failed = getattr(policy, "ik_failed_chunks", 0)
    if not failed:
        return None
    return (
        f"Hy-VLA IK held the arm on {failed} of {policy.ik_chunks} chunks "
        f"({policy.ik_failed_rows} actions held)."
    )
