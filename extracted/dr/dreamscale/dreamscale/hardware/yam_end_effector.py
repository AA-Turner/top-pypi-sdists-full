"""Calibrated Cartesian policy seam over the existing joint-space YAM rig.

I2RT owns FK/IK and hardware control. This adapter owns coordinate conversion,
validation and policy composition; it never commands motors itself.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Protocol
from xml.etree import ElementTree

import numpy as np
from dreamscale_transport import BimanualEndEffectorState
from dreamscale_transport.rho_checkpoints import RHO_YAM_BOX_MODEL_ID

from dreamscale.policy.cartesian import CartesianConversion, PoseApproximation, PoseConversion
from dreamscale.policy.run_loop import run_policy_loop
from dreamscale.policy.runtime.contract import RuntimeContract

from .yam_native import YamHardwareError, _validate_limits, check_native_pin


class ArmKinematics(Protocol):
    def fk(self, joints: np.ndarray) -> np.ndarray: ...
    def ik(self, pose: np.ndarray, seed: np.ndarray) -> tuple[bool, np.ndarray]: ...

    def set_joint_limits(self, limits: np.ndarray) -> None: ...


def builtin_end_effector_profile(model_id, config):
    """Verified BusyBox physical convention for the supported native YAM rig.

    Public paired YAM data at BusyBox revision 21103bd793e0837557c0253ba21a3fa7c55e5f4c
    is each arm's own base and gripper-body pose under I2RT ac09692's YAM model.
    I2RT 1.3.6 re-derived that model from CAD, so its gripper body now sits within
    about 6 mm of those poses, with the same axes. This is the chosen physical
    deployment convention, not a claim of unpublished midtraining calibration
    provenance. Native FK/IK and its limits remain in charge.
    """
    if model_id != RHO_YAM_BOX_MODEL_ID:
        raise YamHardwareError("No built-in end-effector profile for the selected model.")
    if set(config.arms) != {"left", "right"} or any(
        arm.arm_type != "YAM" or arm.gripper_type != "LINEAR_4310"
        for arm in config.arms.values()
    ):
        raise YamHardwareError(
            "The Rho-YAM default requires two YAM arms with LINEAR_4310 grippers. "
            "Use yam-ee.json to describe your configured rig's frames and tools."
        )
    # inverse(body_T_grasp_site): the native site is -144.65 mm along body Z,
    # rotated Rx(pi). The dataset uses the body origin and axes, not the grasp TCP.
    return {
        "version": 1,
        "model_id": model_id,
        "coordinate_frame": model_id,
        "gripper_unit": "checkpoint",
        "calibration_id": "busybox-21103bd-120c3c8-gripper-body-arm-local-v1",
        "arms": {
            side: {
                "can_interface": arm.can_interface,
                "arm_type": arm.arm_type,
                "gripper_type": arm.gripper_type,
                "site_name": "grasp_site",
                "model_T_base": np.eye(4).tolist(),
                "site_T_tool": [
                    [1, 0, 0, -9.681e-05], [0, -1, 0, 3.8898e-05], [0, 0, -1, -0.14465],
                    [0, 0, 0, 1],
                ],
                "gripper_closed": 0.0,
                "gripper_open": 1.0,
            }
            for side, arm in config.arms.items()
        },
    }


def _vector(value, size, name):
    raw = np.asarray(value)
    if (
        any(isinstance(item, bool | np.bool_) for item in np.asarray(value, dtype=object).flat)
        or raw.dtype.kind not in "fiu"
        or raw.shape != (size,)
        or not np.isfinite(raw).all()
    ):
        raise YamHardwareError(f"{name} requires {size} finite numeric values.")
    return raw.astype(float)


def _transform(value, name):
    matrix = np.asarray(value)
    if (
        any(isinstance(item, bool | np.bool_) for item in np.asarray(value, dtype=object).flat)
        or matrix.dtype.kind not in "fiu"
        or matrix.shape != (4, 4)
        or not np.isfinite(matrix).all()
    ):
        raise YamHardwareError(f"{name} requires a finite 4x4 rigid transform.")
    matrix = matrix.astype(float)
    rotation = matrix[:3, :3]
    if (
        not np.allclose(matrix[3], [0, 0, 0, 1], atol=1e-8)
        or not np.allclose(rotation.T @ rotation, np.eye(3), atol=1e-6)
        or not np.isclose(np.linalg.det(rotation), 1, atol=1e-6)
    ):
        raise YamHardwareError(f"{name} must be a proper rigid transform.")
    matrix.setflags(write=False)
    return matrix


def pose_from_6d(values):
    """Decode position and the first two rotation-matrix columns."""
    values = _vector(values, 9, "end-effector pose")
    first, second = values[3:6].copy(), values[6:9].copy()
    norm = np.linalg.norm(first)
    if norm < 1e-6:
        raise YamHardwareError("End-effector rotation has a zero first column.")
    first /= norm
    second -= first * np.dot(first, second)
    norm = np.linalg.norm(second)
    if norm < 1e-6:
        raise YamHardwareError("End-effector rotation columns are degenerate.")
    second /= norm
    pose = np.eye(4)
    pose[:3, 3] = values[:3]
    pose[:3, :3] = np.column_stack((first, second, np.cross(first, second)))
    return pose


def pose_to_6d(pose):
    pose = _transform(pose, "FK pose")
    return (*pose[:3, 3], *pose[:3, 0], *pose[:3, 1])


@dataclass(frozen=True)
class ArmFrameCalibration:
    can_interface: str
    arm_type: str
    gripper_type: str
    site_name: str
    # model_T_base @ base_T_site @ site_T_tool = model_T_tool.
    model_T_base: np.ndarray
    site_T_tool: np.ndarray
    gripper_closed: float
    gripper_open: float

    def __post_init__(self):
        for name in ("can_interface", "arm_type", "gripper_type", "site_name"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise YamHardwareError(f"Calibration requires {name}.")
        for name in ("model_T_base", "site_T_tool"):
            object.__setattr__(self, name, _transform(getattr(self, name), name))
        endpoints = _vector([self.gripper_closed, self.gripper_open], 2, "gripper endpoints")
        if endpoints[0] == endpoints[1]:
            raise YamHardwareError("Calibrate distinct model gripper closed/open coordinates.")

    def model_gripper(self, unit_value):
        value = float(unit_value)
        if not np.isfinite(value) or not 0 <= value <= 1:
            raise YamHardwareError("Hardware gripper must be normalized in [0,1].")
        return self.gripper_closed + value * (self.gripper_open - self.gripper_closed)

    def hardware_gripper(self, model_value, *, saturate=False):
        value = (model_value - self.gripper_closed) / (self.gripper_open - self.gripper_closed)
        if not np.isfinite(value):
            raise YamHardwareError("Predicted gripper must be finite.")
        if saturate:
            return float(np.clip(value, 0.0, 1.0))
        if not 0 <= value <= 1:
            raise YamHardwareError("Predicted gripper is outside the calibrated closed/open range.")
        return float(value)


class I2rtKinematics:
    """Native configured geometry, with only the six arm coordinates controlled.

    Finger coordinates stay at the model's reference configuration. The selected
    site must be independent of those coordinates; gripper commands retain their
    separate calibrated mapping in the policy adapter.
    """

    def __init__(self, calibration):
        check_native_pin()
        import mink
        import mujoco
        from i2rt.robots.kinematics import Kinematics
        from i2rt.robots.utils import ArmType, GripperType, combine_arm_and_gripper_xml

        arm_type = ArmType[calibration.arm_type]
        gripper_type = GripperType[calibration.gripper_type]
        arm_joints = self._joint_names(arm_type.get_xml_path())
        gripper_joints = self._joint_names(gripper_type.get_xml_path())
        xml = combine_arm_and_gripper_xml(arm_type, gripper_type)
        self.solver = Kinematics(xml, calibration.site_name)
        self.site_name = calibration.site_name
        model = self.solver._configuration.model
        names = tuple(model.joint(index).name for index in range(model.njnt))
        if (
            len(arm_joints) != 6
            or len(set((*arm_joints, *gripper_joints))) != len(names)
            or names != (*arm_joints, *gripper_joints)
            or model.nq != model.nv
            or model.nq != model.njnt
            or not np.array_equal(model.jnt_qposadr, np.arange(model.nq))
            or not np.array_equal(model.jnt_dofadr, np.arange(model.nv))
            or any(int(kind) != int(mujoco.mjtJoint.mjJNT_HINGE)
                   for kind in model.jnt_type[:6])
            or any(
                int(kind) not in (int(mujoco.mjtJoint.mjJNT_HINGE),
                                 int(mujoco.mjtJoint.mjJNT_SLIDE))
                for kind in model.jnt_type[6:]
            )
        ):
            raise YamHardwareError("Unsupported native kinematic coordinate layout.")
        ancestors = set()
        body = int(model.site(calibration.site_name).bodyid[0])
        while body:
            ancestors.add(body)
            body = int(model.body_parentid[body])
        if not set(model.jnt_bodyid[:6]).issubset(ancestors) or set(
            model.jnt_bodyid[6:]
        ).intersection(ancestors):
            raise YamHardwareError("Native site must depend only on all six arm coordinates.")
        self._reference = _vector(model.qpos0, model.nq, "native reference coordinates")
        self._reference.setflags(write=False)
        # Preserve native position limits and additionally freeze every passive
        # gripper coordinate during every Mink solve/integration step.
        self._limits = [
            mink.ConfigurationLimit(model),
            mink.VelocityLimit(model, {name: 0.0 for name in gripper_joints}),
        ]

    @staticmethod
    def _joint_names(path):
        joints = ElementTree.parse(path).findall(".//worldbody//joint")
        names = tuple(joint.get("name") for joint in joints)
        if any(not name for name in names):
            raise YamHardwareError("Native kinematic joints must have distinct names.")
        return names

    def _coordinates(self, joints):
        full = self._reference.copy()
        full[:6] = _vector(joints, 6, "native arm coordinates")
        return full

    def set_joint_limits(self, limits):
        """Use the opened rig's effective arm bounds, preserving passive axes.

        The native controller's declared bounds can differ from the XML ranges.
        Task restrictions are already intersected with those bounds by YamRig.
        Standalone FK/IK retains XML bounds until explicitly bound to a rig.
        """
        import mink

        raw = np.asarray(limits)
        if raw.shape != (6, 2):
            raise YamHardwareError("IK limits require six lower/upper joint bounds.")
        bounds = _vector(raw.reshape(-1), 12, "IK joint limits").reshape(6, 2)
        if not (bounds[:, 0] < bounds[:, 1]).all():
            raise YamHardwareError("IK joint limits require ordered lower/upper bounds.")
        model = self.solver._configuration.model
        model.jnt_range[:6] = bounds
        self._limits[0] = mink.ConfigurationLimit(model)

    def _checked_coordinates(self, coordinates):
        full = _vector(coordinates, len(self._reference), "native kinematic coordinates")
        # A zero-velocity QP constraint can leave machine-level roundoff. This
        # absolute bound admits that only; the site cannot depend on these axes.
        if not np.allclose(full[6:], self._reference[6:], rtol=0, atol=1e-12):
            raise YamHardwareError("Native solver changed an uncontrolled gripper coordinate.")
        return full

    def _require_configuration(self, expected):
        current = self._checked_coordinates(self.solver._configuration.q)
        if not np.array_equal(current, expected):
            raise YamHardwareError("Native solver configuration differs from its coordinates.")

    def fk(self, joints):
        full = self._coordinates(joints)
        pose = self.solver.fk(full)
        self._require_configuration(full)
        return _transform(pose, "native FK pose")

    def ik(self, pose, seed):
        success, coordinates = self.solver.ik(
            _transform(pose, "native IK target"),
            self.site_name,
            init_q=self._coordinates(seed),
            limits=self._limits,
            max_iters=200,
        )
        if not isinstance(success, bool | np.bool_):
            raise YamHardwareError("Native IK must report convergence explicitly.")
        full = self._checked_coordinates(coordinates)
        self._require_configuration(full)
        return bool(success), full[:6].copy()


class YamEndEffectorAdapter:
    def __init__(
        self,
        *,
        model_id,
        coordinate_frame,
        gripper_unit,
        calibration_id,
        arms,
        kinematics,
        observation_factory=None,
        position_tolerance_m=0.001,
        rotation_tolerance_rad=0.01,
        pose_approximation=None,
    ):
        if (
            any(not isinstance(value, str) or not value.strip()
                for value in (model_id, coordinate_frame, gripper_unit, calibration_id))
            or set(arms) != {"left", "right"}
            or set(kinematics) != {"left", "right"}
            or (observation_factory is not None and not callable(observation_factory))
        ):
            raise YamHardwareError("YAM pose control needs calibration for the checkpoint frame.")
        tolerances = _vector([position_tolerance_m, rotation_tolerance_rad], 2, "IK tolerances")
        if (tolerances <= 0).any():
            raise YamHardwareError("IK tolerances must be positive.")
        self.model_id, self.coordinate_frame = model_id, coordinate_frame
        self.gripper_unit, self.calibration_id = gripper_unit, calibration_id
        self.arms, self.kinematics = dict(arms), dict(kinematics)
        self.observation_factory = observation_factory
        self.position_tolerance_m, self.rotation_tolerance_rad = tolerances
        self._lock = threading.RLock()
        if pose_approximation is not None and not isinstance(pose_approximation, PoseApproximation):
            raise YamHardwareError(
                "Pose approximation requires an explicit PoseApproximation budget."
            )
        self.pose_approximation = pose_approximation
        self.last_conversion = None

    @classmethod
    def from_file(
        cls, path, config, *, kinematics_factory=I2rtKinematics, observation_factory=None,
        expected_model_id=None, expected_coordinate_frame=None, expected_gripper_unit=None,
        pose_approximation=None,
    ):
        path = Path(path)
        if not path.is_file():
            raise YamHardwareError(
                f"YAM needs calibrated end-effector frames and gripper endpoints at {path}. "
                "Add the site calibration described in the YAM guide before connecting."
            )
        try:
            value = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise YamHardwareError(f"Cannot read YAM end-effector calibration at {path}.") from exc
        return cls.from_profile(
            value, config, kinematics_factory=kinematics_factory,
            observation_factory=observation_factory, expected_model_id=expected_model_id,
            expected_coordinate_frame=expected_coordinate_frame,
            expected_gripper_unit=expected_gripper_unit,
            pose_approximation=pose_approximation,
        )

    @classmethod
    def from_profile(
        cls, profile, config, *, kinematics_factory=I2rtKinematics, observation_factory=None,
        expected_model_id=None, expected_coordinate_frame=None, expected_gripper_unit=None,
        pose_approximation=None,
    ):
        """Bind a complete profile to the actual rig before loading native solvers."""
        value = dict(profile) if isinstance(profile, dict) else {}
        version = value.pop("version", None)
        if type(version) is not int or version != 1:
            raise YamHardwareError("Unsupported YAM end-effector calibration version.")
        try:
            arms = {side: ArmFrameCalibration(**arm) for side, arm in value.pop("arms").items()}
            for side in ("left", "right"):
                arm, mapped = arms[side], config.arms[side]
                if any(
                    getattr(arm, name) != getattr(mapped, name)
                    for name in ("can_interface", "arm_type", "gripper_type")
                ):
                    raise YamHardwareError(f"{side.title()} calibration does not match the rig.")
            # Validate the complete profile BEFORE loading an optional native solver.
            adapter = cls(
                arms=arms, kinematics={side: None for side in arms},
                observation_factory=observation_factory,
                pose_approximation=pose_approximation, **value,
            )
            adapter.require_policy(
                expected_model_id, coordinate_frame=expected_coordinate_frame,
                gripper_unit=expected_gripper_unit,
            )
            adapter.kinematics = {side: kinematics_factory(arm) for side, arm in arms.items()}
            return adapter
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            raise YamHardwareError("Invalid YAM end-effector calibration fields.") from exc

    def _state(self, joint_action):
        joint_action = _vector(joint_action, 14, "measured YAM state")
        fields = {}
        for side, offset in (("left", 0), ("right", 7)):
            arm = self.arms[side]
            base_T_site = _transform(
                self.kinematics[side].fk(joint_action[offset : offset + 6]), "FK"
            )
            pose = arm.model_T_base @ base_T_site @ arm.site_T_tool
            values = pose_to_6d(pose)
            fields.update(
                {
                    f"{side}_position": values[:3],
                    f"{side}_rotation_6d": values[3:],
                    f"{side}_gripper": arm.model_gripper(joint_action[offset + 6]),
                }
            )
        return BimanualEndEffectorState(
            coordinate_frame=self.coordinate_frame, gripper_unit=self.gripper_unit, **fields
        )

    def observe(self, observation, *, observation_factory=None):
        factory = self.observation_factory if observation_factory is None else observation_factory
        if not callable(factory):
            raise YamHardwareError("Pose observations require an explicit observation factory.")
        with self._lock:
            return factory(
                top_frame=observation.top_frame,
                left_frame=observation.left_frame,
                right_frame=observation.right_frame,
                robot_state=self._state(observation.hold_action),
                actions_remaining=observation.actions_remaining,
                camera_capture_times_ns=observation.camera_capture_times_ns,
            )

    def state(self, joint_action):
        """Convert measured joints for a caller-owned model observation builder."""
        with self._lock:
            return self._state(joint_action)

    def joint_chunk(self, actions, seed, validate, *, saturate_grippers=False, on_conversion=None):
        """Verify a complete chunk before queue admission; validate must enforce strict bounds.

        An explicit approximation policy may admit a native bounded candidate
        despite its exact-convergence flag, after independent tool-pose FK
        verification. Receipt callbacks are diagnostic and never command motors.
        """
        if on_conversion is not None and not callable(on_conversion):
            raise YamHardwareError("Cartesian conversion recording requires a callable.")
        with self._lock:
            records, converted = [], []
            accepted, error = False, None
            try:
                seed = _vector(seed, 14, "IK seed").copy()
                for index, action in enumerate(actions):
                    action = _vector(action, 20, "absolute bimanual end-effector action")
                    target = []
                    for side, offset, joint_offset in (("left", 0, 0), ("right", 10, 7)):
                        arm = self.arms[side]
                        pose = pose_from_6d(action[offset : offset + 9])
                        base_T_site = (
                            np.linalg.inv(arm.model_T_base) @ pose @ np.linalg.inv(arm.site_T_tool)
                        )
                        success, joints = self.kinematics[side].ik(
                            base_T_site, seed[joint_offset : joint_offset + 6]
                        )
                        if not isinstance(success, bool | np.bool_):
                            raise YamHardwareError("Native IK must report convergence explicitly.")
                        joints = _vector(joints, 6, "I2RT IK result")
                        achieved = _transform(
                            self.kinematics[side].fk(joints), "IK verification FK",
                        )
                        achieved_tool = _transform(
                            arm.model_T_base @ achieved @ arm.site_T_tool, "achieved tool pose",
                        )
                        distance = float(np.linalg.norm(achieved_tool[:3, 3] - pose[:3, 3]))
                        angle = float(np.arccos(np.clip(
                            (np.trace(achieved_tool[:3, :3].T @ pose[:3, :3]) - 1) / 2, -1, 1,
                        )))
                        _vector([distance, angle], 2, "IK verification errors")
                        exact = bool(success) and (
                            distance <= self.position_tolerance_m
                            and angle <= self.rotation_tolerance_rad
                        )
                        permitted = (
                            exact if self.pose_approximation is None
                            else self.pose_approximation.accepts(distance, angle)
                        )
                        records.append(PoseConversion(
                            action_index=index + 1, arm=side,
                            requested_pose=tuple(tuple(float(v) for v in row) for row in pose),
                            achieved_pose=tuple(
                                tuple(float(v) for v in row) for row in achieved_tool
                            ),
                            joints=tuple(float(v) for v in joints), native_converged=bool(success),
                            position_error_m=distance, rotation_error_rad=angle,
                            status=(
                                "exact" if exact and permitted
                                else "approximate" if permitted else "rejected"
                            ),
                        ))
                        if not permitted:
                            if self.pose_approximation is not None:
                                budget = self.pose_approximation
                                position_cap = (
                                    f"{budget.max_position_error_m * 1000:g} mm"
                                    if budget.max_position_error_m is not None else "none"
                                )
                                rotation_cap = (
                                    f"{budget.max_rotation_error_rad:g} rad"
                                    if budget.max_rotation_error_rad is not None else "none"
                                )
                                raise YamHardwareError(
                                    f"{side.title()} pose exceeds approximation budget "
                                    f"at action {index + 1}: "
                                    f"position {distance * 1000:.2f} mm "
                                    f"(limit {position_cap}), "
                                    f"rotation {angle:.4f} rad "
                                    f"(limit {rotation_cap})."
                                )
                            if not success:
                                raise YamHardwareError(
                                    f"{side.title()} IK did not converge at action {index + 1}."
                                )
                            raise YamHardwareError(
                                f"{side.title()} IK residual exceeds calibration tolerance."
                            )
                        target.extend((*joints, arm.hardware_gripper(
                            action[offset + 9], saturate=saturate_grippers,
                        )))
                    validate(target, check_step=False)  # strict: never repair a solver's bad joints
                    seed = np.asarray(target)
                    converted.append(tuple(target))
                accepted = True
                return tuple(converted)
            except Exception as exc:
                error = str(exc)
                raise
            finally:
                self.last_conversion = CartesianConversion(tuple(records), accepted, error)
                if on_conversion is not None:
                    try:
                        on_conversion(self.last_conversion)
                    except Exception:
                        logging.getLogger(__name__).warning(
                            "Cartesian conversion recording failed; verification remains enforced.",
                        )

    def execution_contract(self, policy_contract):
        if (
            not isinstance(policy_contract, RuntimeContract)
            or policy_contract.action_dim != 20
            or policy_contract.action_space != "absolute_eef_6d"
            or policy_contract.hold_behavior != "current_position"
        ):
            raise YamHardwareError("YAM pose conversion requires an absolute_eef_6d/20 contract.")
        return RuntimeContract(
            action_hz=policy_contract.action_hz,
            chunk_size=policy_contract.execution_chunk_size,
            native_action_hz=policy_contract.native_action_hz,
            action_dim=14,
            action_space="absolute_joint_position",
            hold_behavior="current_position",
            normalized_gripper_indices=(6, 13),
            fixed_rate=policy_contract.fixed_rate,
            joint_groups=(tuple(range(6)), tuple(range(7, 13))),
            gripper_indices=(6, 13),
            joint_unit="rad",
            startup_motion_delay_s=0.1,
        )

    def require_policy(self, model_id, *, coordinate_frame=None, gripper_unit=None):
        """Check caller-selected model semantics without selecting a checkpoint."""
        if any(expected is not None and expected != actual for expected, actual in (
            (model_id, self.model_id), (coordinate_frame, self.coordinate_frame),
            (gripper_unit, self.gripper_unit),
        )):
            raise YamHardwareError("End-effector calibration does not match the selected model.")

    def bind(self, policy, rig, *, on_conversion=None):
        model_id = getattr(policy, "model", None)
        if not isinstance(model_id, str) or not model_id.strip():
            raise YamHardwareError("A connected pose policy must identify its model.")
        self.require_policy(model_id)
        wrapped = _JointExecutionPolicy(
            policy, rig, self, getattr(policy, "runtime_contract", None), on_conversion,
        )
        # `dreamscale run` connects while the arms are still closed; their bounds
        # are bound before the first conversion then (`_JointExecutionPolicy`).
        if isinstance(getattr(rig, "limits", None), dict) and rig.limits:
            wrapped.bind_limits()
        return wrapped

    def bind_limits(self, rig):
        """Bind native IK to the opened rig's effective hardware/task arm bounds."""
        with self._lock:
            reported = getattr(rig, "limits", None)
            if not isinstance(reported, dict) or set(reported) != {"left", "right"}:
                raise YamHardwareError("Open the YAM rig before binding native IK limits.")
            bounds = {}
            for side in ("left", "right"):
                raw = np.asarray(reported[side])
                if raw.shape != (7, 2):
                    raise YamHardwareError("Expected seven hardware/task joint bounds per arm.")
                bounds[side] = _vector(raw.reshape(-1), 14, "hardware/task limits").reshape(7, 2)
                _validate_limits(bounds[side])
                if not callable(getattr(self.kinematics[side], "set_joint_limits", None)):
                    raise YamHardwareError("Kinematics must accept the rig's hardware/task limits.")
            for side in ("left", "right"):
                self.kinematics[side].set_joint_limits(bounds[side][:6].copy())


class _JointExecutionPolicy:
    """Preserve the remote pose contract; adapt predictions before joint smoothing."""

    def __init__(self, policy, rig, adapter, policy_contract, on_conversion=None):
        self.remote, self.rig, self.adapter = policy, rig, adapter
        self.execution_contract = adapter.execution_contract(policy_contract)
        self.last_run_result = None
        if on_conversion is not None and not callable(on_conversion):
            raise YamHardwareError("Cartesian conversion recording requires a callable.")
        self.on_conversion = on_conversion
        self._limits_bound = False

    def bind_limits(self):
        self.adapter.bind_limits(self.rig)
        self._limits_bound = True

    def __getattr__(self, name):
        return getattr(self.remote, name)

    @property
    def last_run_result(self):
        return getattr(self.remote, "last_run_result", None)

    @last_run_result.setter
    def last_run_result(self, value):
        self.remote.last_run_result = value

    def _validate_target(self, action, *, check_step):
        # Reject invalid solver joints before queueing; measured tracking and
        # velocity projection still apply separately at physical dispatch.
        self.rig.validate_action(action, check_step=check_step, saturate=False)

    def _joint_actions(self, chunk):
        if not self._limits_bound:
            self.bind_limits()

        def record(report):
            if self.on_conversion is not None:
                self.on_conversion(replace(
                    report, observation_id=chunk.observation_id, chunk_id=chunk.chunk_id,
                ))

        return self.adapter.joint_chunk(
            chunk.actions[: self.execution_contract.chunk_size],
            self.rig.read_hold_action(),
            self._validate_target,
            # Model predictions are unbounded regressions, unlike measured
            # encoder state. Project them into the calibrated gripper interval
            # before the normalized joint buffer, just as the rig bounds joints.
            saturate_grippers=True,
            on_conversion=record if self.on_conversion is not None else None,
        )

    async def _convert(self, chunk):
        # Feedback uses bounded native RPCs too. Keep it off the event loop and
        # drain conversion before cancellation lets runner cleanup close the rig.
        conversion = asyncio.create_task(asyncio.to_thread(self._joint_actions, chunk))
        try:
            actions = await asyncio.shield(conversion)
        except asyncio.CancelledError:
            await asyncio.gather(conversion, return_exceptions=True)
            raise
        indices = (
            None
            if chunk.action_indices is None
            else chunk.action_indices[: self.execution_contract.chunk_size]
        )
        return replace(chunk, actions=actions, action_indices=indices)

    async def predict(self, observation, **kwargs):
        return await self._convert(await self.remote.predict(observation, **kwargs))

    async def _predict_chunk_with_queue_depth(self, observation, **kwargs):
        # RTC references would now be joint14 while the model is pose20. Never send them.
        if kwargs.get("rtc_context") is not None and kwargs["rtc_context"].enabled:
            raise YamHardwareError("Cartesian YAM adapters require rtc='off'.")
        predictor = getattr(self.remote, "_predict_chunk_with_queue_depth", None)
        if predictor is None:
            chunk = await self.remote.predict(
                observation, instruction=kwargs["instruction"], timeout_s=kwargs["timeout_s"]
            )
        else:
            chunk = await predictor(observation, **kwargs)
        return await self._convert(chunk)

    async def run(self, **kwargs):
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
