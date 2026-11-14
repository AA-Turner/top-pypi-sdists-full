"""A Xiaomi-Robotics-1 deployment's server-described contract (dreamscale_transport.xr1_deploy).

A deployment runs the bimanual YAM preset or a custom robot (1-2 arms, 1-3 cameras by view, an
optional waist and mobile base, a declared end-effector frame and units), so its widths are its
own: the session's deployment block (``semantic.public_embodiment()`` plus its id and RTC) is the
whole contract, checked here against the transport semantic's own rules.

Each request carries one JPEG per declared camera at capture resolution (the server crops and
resizes), the instruction, and one plain state vector of ``state_dim`` values: per arm, left
before right, its joints (``joint_unit``), its gripper (``gripper_unit``), its end-effector
position (xyz, metres, in ``ee_frame``) and rotation as 6D (the rotation matrix's first two
columns); then the waist, when the robot has one; then a mobile base's measured velocity
components (``base_components``, in their declared order). Each chunk row is ``action_dim``
absolute end-effector targets (``absolute_eef_6d``): per arm xyz, 6D and gripper; then the waist,
then the base velocity (3, or the declared components). Between chunks the robot holds its
measured pose (``current_position``); a mobile base holds still (zero velocity). A vector robot
(a run trained with the ``vector`` input) sends its ``vector.state`` values and gets
``vector.action`` absolute values a row, holding its measured values (equal widths) or zeros.

A chunk is ``action_horizon`` rows (30 at 30 Hz; a training run's is about one second at its
data's rate); each answer holds the ``executed_actions`` the robot runs, or all of them when the
deployment returns its whole chunk (``full_chunk``), of which the robot runs the first
``executed_actions``.
Trained RTC's committed rows are those absolute rows as the robot received them; the server
re-expresses them against the request's pose.

Build the state with ``Xr1SessionDeployment.state`` (or ``robot_state`` from a deployment row's
``embodiment``)::

    state = robot_state({"preset": "bimanual_yam"}, arms={
        "left": {"joints": left_q, "gripper": 0.2, "position": left_xyz, "rotation": left_R},
        "right": {"joints": right_q, "gripper": 0.9, "position": right_xyz,
                  "rotation": right_R},  # a 3x3 rotation matrix, or its 6D (6 values)
    })
    observation = dreamscale.robot.observation(cameras={...}, state=state)

A robot that is only a mobile base (a run trained with the ``mobile_base`` input, e.g. a car's
speed and steering) sends no arms, only its components in their declared order::

    state = deployment.state(base={"vx": speed, "wz": steering})   # or base=[...] in order

A vector robot sends its values in its data's order::

    state = deployment.state(vector=[curvature, speed])
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from dreamscale_transport import xr1_deploy as C

LABEL = C.XR1_PUBLIC_NAME
# What the block carries of the robot and its contract (``public_embodiment``), required ...
_REQUIRED = (
    "id", "preset", "arms", "cameras", "ee_frame", "joint_unit", "gripper_unit", "state_dim",
    "action_dim", "gripper_indices", "action_horizon", "executed_actions", "action_hz",
    "action_space", "trained_rtc_max_delay", "rtc_method",
)
# ... and defaulted where the semantic defaults them.
_OPTIONAL = ("waist", "base", "base_components", "vector", "full_chunk", "step",
             "denoising_steps", "max_instruction_tokens", "source_format")
_SEMANTIC_KEYS = tuple(key for key in (*_REQUIRED, *_OPTIONAL) if key not in (
    "id", "state_dim", "action_dim", "gripper_indices", "rtc_method"))


def _semantic(data: Mapping[str, Any]) -> C.Xr1DeploymentSemantic:
    """The transport semantic of a block's robot (strict, its own rules: preset, sides, views,
    frame, units, horizon, RTC bound). What the block doesn't carry (the checkpoint's own
    layout, statistics and frequency weighting) are placeholders its robot rules never read:
    never fingerprint the result."""
    trained = data.get("trained_rtc_max_delay")
    return C.parse_semantic({
        **{key: data[key] for key in _SEMANTIC_KEYS if key in data},
        "layout": "dreamscale_training", "normalization_sha256": "0" * 64,
        "async_train": bool(trained) if type(trained) is int else True,
        "freq_coefficient": 0.0, "freq_excluded_dims": [],
    })


@dataclass(frozen=True)
class Xr1SessionDeployment:
    id: str
    preset: str
    arms: tuple[C.Xr1Arm, ...]
    cameras: tuple[C.Xr1Camera, ...]
    waist: bool
    base: bool
    ee_frame: str
    joint_unit: str
    gripper_unit: str
    state_dim: int
    action_dim: int
    gripper_indices: tuple[int, ...]
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    max_instruction_tokens: int
    trained_rtc_max_delay: int
    rtc_method: str
    rtc_max_delay: int | None
    step: int | None = None
    # A mobile base's velocity components (in its state and rows, in this order).
    base_components: tuple[str, ...] = ()
    # A vector robot's widths and hold (its state and rows are plain values), or None.
    vector: C.Xr1Vector | None = None
    # Whether each answer holds the whole chunk (else the executed rows).
    full_chunk: bool = False
    # The robot's semantic (placeholders for the checkpoint's own fields; see ``_semantic``).
    semantic: C.Xr1DeploymentSemantic | None = field(default=None, repr=False, compare=False)
    # No joint layout of its own: its actions are end-effector poses.
    layout: None = None
    robot: None = None
    joints: bool = False

    @property
    def camera_keys(self) -> tuple[str, ...]:
        return tuple(camera.key for camera in self.cameras)

    @property
    def normalized_gripper_indices(self) -> tuple[int, ...]:
        return self.gripper_indices if self.gripper_unit == "normalized_0_1" else ()

    @property
    def rtc_contract(self) -> str | None:
        return C.rtc_contract_for(self.rtc_method)

    @property
    def returned_actions(self) -> int:
        """Rows each answer holds: the whole chunk (``full_chunk``), else the executed rows."""
        return self.action_horizon if self.full_chunk else self.executed_actions

    @classmethod
    def from_json(cls, data: Any) -> Xr1SessionDeployment:
        """Strict on what it reads, tolerant of fields it doesn't (as Hy-VLA's)."""
        if not isinstance(data, dict) or data.get("base_model") != C.XR1_BASE_MODEL:
            raise ValueError(f"the server returned no {LABEL} deployment contract")
        missing = [key for key in _REQUIRED if key not in data]
        if missing:
            raise ValueError(f"incomplete {LABEL} deployment contract (no {missing[0]})")
        try:
            semantic = _semantic(data)
        except (TypeError, ValueError) as error:
            raise ValueError(f"invalid {LABEL} deployment: {_first(error)}") from None
        widths = (("state_dim", semantic.state_dim), ("action_dim", semantic.action_dim))
        indices = data["gripper_indices"]
        if (
            not isinstance(data["id"], str) or not data["id"]
            or any(type(data[key]) is not int or data[key] != value for key, value in widths)
            or not isinstance(indices, list | tuple)
            or any(type(index) is not int for index in indices)
            or tuple(indices) != semantic.gripper_indices
        ):
            raise ValueError(f"invalid {LABEL} deployment shape: its widths aren't its robot's "
                             f"(state {semantic.state_dim}, actions {semantic.action_dim})")
        method, cap, trained = (data["rtc_method"], data.get("rtc_max_delay"),
                                semantic.trained_rtc_max_delay)
        if method not in C.RTC_METHODS:
            raise ValueError(f"the server returned an unknown RTC setting {method!r} for this "
                             f"{LABEL} deployment")
        if method == "off" and cap is not None:
            raise ValueError(f"a {LABEL} deployment with RTC off has no prefix cap")
        if method == "trained":
            try:
                if type(cap) is not int or C.rtc_cap(trained, cap) != cap:
                    raise ValueError(f"the RTC prefix is 1-{trained} rows for this checkpoint")
            except ValueError as error:
                raise ValueError(f"invalid {LABEL} RTC setting: {error}") from None
        return cls(
            id=data["id"], preset=semantic.preset, arms=semantic.arms, cameras=semantic.cameras,
            waist=semantic.waist, base=semantic.base, ee_frame=semantic.ee_frame,
            joint_unit=semantic.joint_unit, gripper_unit=semantic.gripper_unit,
            state_dim=semantic.state_dim, action_dim=semantic.action_dim,
            gripper_indices=semantic.gripper_indices, action_horizon=semantic.action_horizon,
            executed_actions=semantic.executed_actions, action_hz=semantic.action_hz,
            action_space=semantic.action_space,
            max_instruction_tokens=semantic.max_instruction_tokens,
            trained_rtc_max_delay=trained, rtc_method=method, rtc_max_delay=cap,
            step=semantic.step, base_components=tuple(semantic.base_components),
            vector=semantic.vector, full_chunk=semantic.full_chunk, semantic=semantic,
        )

    @property
    def hold_indices(self) -> tuple[int, ...]:
        """The row that holds the measured pose (``current_position``), as each action value's
        index in the state (RuntimeContract.hold_indices; -1: zero): per arm its xyz, 6D and
        gripper as measured, the waist where it is, the base still: zero velocity, either kind
        of base; a vector robot its measured values (equal widths) or zeros (the transport's
        ``hold_row`` on the same state)."""
        if self.vector is not None:
            if self.vector.hold == "measured":
                return tuple(range(self.action_dim))
            return (-1,) * self.action_dim
        out: list[int] = []
        at = 0
        for arm in self.arms:
            gripper, xyz = at + arm.joints, at + arm.joints + 1
            out += [*range(xyz, xyz + 3), *range(xyz + 3, xyz + 9), gripper]
            at += arm.joints + 10
        if self.waist:
            out.append(at)
        if self.base:
            out += [-1, -1, -1]
        out += [-1] * len(self.base_components)
        return tuple(out)

    def state(self, *, arms: Mapping[str, Mapping[str, Any]] | None = None,
              waist: float | None = None, base: Any = None,
              vector: Any = None) -> list[float]:
        """This deployment's state vector (``robot_state``)."""
        if self.vector is not None or vector is not None:
            return _vector_state(self.vector, arms, waist, base, vector)
        return _state(self.arms, self.waist, arms, waist, self.base_components, base)


def robot_state(embodiment: Xr1SessionDeployment | Mapping[str, Any], *,
                arms: Mapping[str, Mapping[str, Any]] | None = None,
                waist: float | None = None, base: Any = None,
                vector: Any = None) -> list[float]:
    """The state vector a request sends, in the deployment's layout: per declared arm (left
    before right) its ``joints`` (as many as it declared, in ``joint_unit``), ``gripper`` (in
    ``gripper_unit``), end-effector ``position`` (xyz, metres) and ``rotation`` (a 3x3 rotation
    matrix, or its 6D: the first two columns, 6 values), both in ``ee_frame``; then ``waist``
    when the robot has one; then a mobile base's ``base`` (its declared ``base_components``: a
    dict by component, or the values in their declared order). ``embodiment``: a session's
    deployment, or a deployment row's ``embodiment`` (``{"preset": "bimanual_yam"}`` will do for
    the preset). A vector robot's state is its ``vector`` values, in its data's order. Refuses a
    missing or extra arm or base value, a wrong width, a non-finite value and a rotation that
    isn't one."""
    if isinstance(embodiment, Xr1SessionDeployment):
        return embodiment.state(arms=arms, waist=waist, base=base, vector=vector)
    if not isinstance(embodiment, Mapping):
        raise ValueError(f"a {LABEL} embodiment is a deployment or its embodiment dict")
    if embodiment.get("vector") is not None or vector is not None:
        declared_vector = (C.Xr1Vector.model_validate(embodiment["vector"])
                           if embodiment.get("vector") is not None else None)
        return _vector_state(declared_vector, arms, waist, base, vector)
    declared = embodiment.get("arms")
    if declared is None and embodiment.get("preset") == C.PRESET:
        declared = [{"side": side, "joints": C.YAM_JOINTS} for side in C.SIDES]
    components = tuple(embodiment.get("base_components") or ())
    if not declared and not components:
        raise ValueError(f"the {LABEL} embodiment declares no arms")
    layout = tuple(C.Xr1Arm.model_validate(arm) for arm in declared or ())
    if [arm.side for arm in layout] != [side for side in C.SIDES
                                        if side in {arm.side for arm in layout}]:
        raise ValueError("arms are distinct sides, left before right")
    if any(c not in C.BASE_COMPONENTS for c in components):
        raise ValueError(f"base components are {', '.join(C.BASE_COMPONENTS)}")
    return _state(layout, bool(embodiment.get("waist")), arms, waist, components, base)


def _state(layout: Sequence[C.Xr1Arm], has_waist: bool,
           arms: Mapping[str, Mapping[str, Any]] | None, waist: Any,
           components: Sequence[str] = (), base: Any = None) -> list[float]:
    sides = [arm.side for arm in layout]
    arms = {} if arms is None and not sides else arms
    if not isinstance(arms, Mapping) or set(arms) != set(sides):
        raise ValueError(f"the state names arms {', '.join(sides)}, got "
                         f"{', '.join(map(str, arms)) if isinstance(arms, Mapping) else arms!r}")
    out: list[float] = []
    for arm in layout:
        given = arms[arm.side]
        if not isinstance(given, Mapping) or set(given) != {"joints", "gripper", "position",
                                                            "rotation"}:
            raise ValueError(f"the {arm.side} arm is its joints, gripper, position and rotation")
        joints = _vector(given["joints"], f"{arm.side} joints", arm.joints)
        gripper = _vector([given["gripper"]], f"{arm.side} gripper", 1)
        position = _vector(given["position"], f"{arm.side} position", 3)
        rotation = np.asarray(given["rotation"], dtype=object)
        if rotation.shape == (3, 3):
            matrix = _vector(rotation.reshape(9), f"{arm.side} rotation", 9).reshape(3, 3)
            if not (np.allclose(matrix.T @ matrix, np.eye(3), atol=1e-3)
                    and np.linalg.det(matrix) > 0):
                raise ValueError(f"the {arm.side} rotation is not a rotation matrix")
            pose = C.pose_to_6d(position, matrix)
        else:
            sixd = _vector(given["rotation"], f"{arm.side} rotation (3x3, or 6D)", 6)
            pose = np.concatenate([position, sixd])
        C.pose_from_6d(pose)  # a 6D whose columns are degenerate is no rotation
        out += [*joints.tolist(), *gripper.tolist(), *(float(v) for v in pose)]
    if has_waist:
        if waist is None:
            raise ValueError("this robot has a waist: pass waist=")
        out += _vector([waist], "waist", 1).tolist()
    elif waist is not None:
        raise ValueError("this robot has no waist")
    if components:
        if isinstance(base, Mapping):
            if set(base) != set(components):
                raise ValueError(f"the base is its {', '.join(components)}, got "
                                 f"{', '.join(map(str, base))}")
            base = [base[c] for c in components]
        if base is None:
            raise ValueError(f"this robot is a mobile base: pass base= its "
                             f"{', '.join(components)}")
        out += _vector(base, f"base's {', '.join(components)}", len(components)).tolist()
    elif base is not None:
        raise ValueError("this robot has no mobile base declared by its components")
    return out


def _vector_state(declared: C.Xr1Vector | None, arms: Any, waist: Any, base: Any,
                  vector: Any) -> list[float]:
    """A vector robot's state: its ``vector.state`` values, nothing else."""
    if declared is None:
        raise ValueError("this robot is not a vector robot: pass its arms, waist or base")
    if arms is not None or waist is not None or base is not None:
        raise ValueError("a vector robot's state is its values alone: pass vector=")
    if vector is None:
        raise ValueError(f"this robot is a vector robot: pass vector= its {declared.state} "
                         "values")
    return _vector(vector, "vector's values", declared.state).tolist()


def _vector(values: Any, name: str, width: int) -> np.ndarray:
    items = list(values) if isinstance(values, Sequence | np.ndarray) else None
    if items is None or len(items) != width or not all(
        isinstance(v, int | float | np.integer | np.floating) and not isinstance(v, bool)
        and np.isfinite(v) for v in items
    ):
        raise ValueError(f"the {name} are {width} finite numbers" if width > 1
                         else f"the {name} is a finite number")
    return np.asarray(items, dtype=np.float64)


def _first(error: ValueError) -> str:
    """A validation error's first message, without pydantic's framing."""
    errors = getattr(error, "errors", None)
    if callable(errors):
        first = errors()[0]
        where = ".".join(str(part) for part in first.get("loc", ()))
        return f"{where}: {first.get('msg')}" if where else str(first.get("msg"))
    return str(error)


def runtime_contract(resolved: Any, deployment: Any) -> Any:
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, Xr1SessionDeployment):
        deployment = Xr1SessionDeployment.from_json(deployment)
    trained = deployment.rtc_method == "trained"
    expected = {
        "backend": "pytorch",
        "rtc": "on" if trained else "off",
        "rtc_contract": C.TRAINED_RTC_CONTRACT if trained else None,
        "action_hz": deployment.action_hz,
        "chunk_size": deployment.returned_actions,
        "action_dim": deployment.action_dim,
        "action_space": C.ACTION_SPACE,
        # Absolute end-effector rows: between chunks the robot holds its measured pose.
        "hold_behavior": C.HOLD_BEHAVIOR,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError(f"{LABEL} runtime differs from the deployment's sealed contract")
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        # Each answer's rows (the whole chunk when it returns it); the robot runs the first
        # executed_actions of them.
        chunk_size=deployment.returned_actions,
        action_dim=deployment.action_dim,
        action_space=C.ACTION_SPACE,
        hold_behavior=C.HOLD_BEHAVIOR,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        normalized_gripper_indices=deployment.normalized_gripper_indices,
        # Capture resolution: the server crops to each camera's trained box, then resizes.
        wire_image=None,
        hold_indices=deployment.hold_indices,
    )
