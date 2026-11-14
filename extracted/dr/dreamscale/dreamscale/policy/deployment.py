"""Robot deployments: what the SDK's shared code knows of a session's deployment.

Each deployment base's own robot, contract and session block live in its base module
(``dreamscale.deploy_bases``) and the policy modules it names (π0.5's
``dreamscale.policy.pi05_deployment``, the exported bases' ``*_deployment``); this module holds
what every base shares: the client features, which models run robot deployments, the
observation checks, and the refusals.
"""

from __future__ import annotations

import dataclasses
import importlib
import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from dreamscale_transport import VectorRobotState, catalog, families

from dreamscale import errors
from dreamscale.policy.exported_deployments import exported_base

# What this SDK tells the control plane it can run. A π0.5 deployment session needs
# ``deployment_runtime_v1`` (the server-driven contract and the ``deployment`` block), and
# one whose actions aren't joint targets also ``model_defined_actions_v1`` (the
# ``model_defined`` action space, which waits rather than holds); without them the control
# plane answers 426 ``sdk_upgrade_required``. ``punched_quic_fallback_v2``: a lost punched
# QUIC path falls back within about a second, resends what it left unanswered and punches
# again, so the control plane may offer it on any Modal session. ``follows_keep_warm_v1``: a
# session on a kept-warm deployment stays open while the code holds the policy and is
# released by close() or exit, so the control plane's idle reap passes it by.
# Then the catalog models' own client features no family declares.
# Each deployment family's own features come from its transport contract module (the family
# manifest's ``contract``): its runtime contract, a later revision of it, then RTC, then the
# catalog models it serves.
_FAMILY_FEATURES = ("CLIENT_FEATURE", "CLIENT_FEATURE_V2", "RTC_CLIENT_FEATURE",
                    "CATALOG_CLIENT_FEATURE")


def _family_features() -> tuple[str, ...]:
    out = []
    for family in families.FAMILIES:
        if family.deploy is None or family.deploy.contract is None:
            continue
        contract = importlib.import_module(family.deploy.contract)
        out += [getattr(contract, name) for name in _FAMILY_FEATURES if hasattr(contract, name)]
    return tuple(out)


def _catalog_features(already: tuple[str, ...]) -> tuple[str, ...]:
    """The client features catalog models need that no deployment family declares, in catalog
    order (Praxis-1's episode states)."""
    out: list[str] = []
    for entry in catalog.CATALOG:
        feature = entry.client_feature[0] if entry.client_feature else None
        if feature and feature not in already and feature not in out:
            out.append(feature)
    return tuple(out)


CLIENT_FEATURES = (
    "deployment_runtime_v1", "model_defined_actions_v1", *_family_features(),
    "punched_quic_fallback_v2", "follows_keep_warm_v1",
)
CLIENT_FEATURES += _catalog_features(CLIENT_FEATURES)
# Praxis-1 sessions may ask for the lightning engine (DSL-429). A literal for
# dreamscale_transport.praxis.ENGINE_CLIENT_FEATURE: the pinned transport release predates it.
CLIENT_FEATURES += ("praxis_engine_v1",)
# Every units family's deployment host, by its id or its public name: `dreamscale run <robot>
# --deployment` drives each at its session's rate and chunk.
_DEPLOYMENT_HOSTS = frozenset(
    name for family in families.FAMILIES if family.deploy is not None and family.deploy.units
    for name in (family.deploy.base, family.deploy.public_id)
)
_SESSION_ID = re.compile(r"\b(?:dropbear_)?sess_[A-Za-z0-9_-]+")


def is_default_base(model: str | None) -> bool:
    """True for the default deployments base (``deploy_bases.default()``, what `--base`
    defaults to), by its id or its public name."""
    from dreamscale import deploy_bases

    base = deploy_bases.of_model(model)
    return base is not None and base.default


def session_base(model: str | None) -> Any:
    """The session hooks (``deploy_bases.SessionBase``) of the base whose sessions ``model``
    (its id or public name) opens, where its sessions carry their robot and take their
    contract from the resolved configuration; else None."""
    from dreamscale import deploy_bases

    base = deploy_bases.of_model(model)
    return base.session if base is not None else None


def runs_robot_deployments(model: str | None) -> bool:
    """Bases whose deployments `dreamscale run <robot> --deployment` drives at the session's
    rate and chunk (the deployment's own): every units family's host, by either name."""
    return model in _DEPLOYMENT_HOSTS


def follows_session_contract(model: str | None) -> bool:
    """Models whose session supplies the run's rate and chunk: the robot deployment bases,
    and the shared catalog models that serve one's contract (abc-vla-yam)."""
    return runs_robot_deployments(model) or exported_base(model) is not None


def waits_for_each_chunk(model: str | None) -> bool:
    """Bases whose robot waits for each chunk and runs it from its first action
    (``hold_behavior: "wait"``; ``deploy_bases``). `dreamscale run` drives them in sync mode."""
    from dreamscale import deploy_bases

    return any(base.waits_for_each_chunk and model == base.name for base in deploy_bases.bases())


def deployment_only_base(model: str | None) -> tuple[str, str] | None:
    """(label, --base name) when ``model`` names a base that runs deployments only: a units
    family's host, by its model or its public name."""
    from dreamscale import deploy_bases

    for base in deploy_bases.bases():
        deploy = families.family(base.family).deploy
        if deploy.units and model in (deploy.base, deploy.public_id):
            return base.label, base.creates_as or base.listed_as or base.name
    return None


@dataclass(frozen=True)
class PresetLayout:
    """A preset's robot, as the runners and the run loop need it."""

    label: str
    # The robot's wire: its cameras (key, image slot) in order, and the rate it runs at.
    cameras: tuple[tuple[str, str], ...]
    action_hz: float
    action_dim: int
    joint_groups: tuple[tuple[int, ...], ...]
    gripper_indices: tuple[int, ...]
    normalized_gripper_indices: tuple[int, ...]
    joint_unit: str
    startup_motion_delay_s: float
    observe_helper: str
    run_command: str | None


def joint_actions(state_dim: Any, action_dim: Any) -> bool:
    """Whether a π0.5 deployment's actions are absolute joint targets: its state and action
    widths are equal. Any other deployment (end-effector deltas, say) acts in its model's
    own space, and runs from Python only: no robot preset, no `dreamscale run`, no hold."""
    return state_dim == action_dim


def state_width(robot_state: Any) -> int | None:
    """The width of a wire robot state the π0.5 runtime reads, or None for another kind."""
    state = getattr(robot_state, "state", None)
    if state is not None:  # VectorRobotState
        return len(state)
    left = getattr(robot_state, "left_joint_positions", None)
    right = getattr(robot_state, "right_joint_positions", None)
    if left is not None and right is not None and hasattr(robot_state, "left_gripper"):
        return len(left) + 1 + len(right) + 1  # BimanualRobotState: joints, gripper per arm
    joints = getattr(robot_state, "joint_positions", None)
    if joints is not None:  # RobotState: the gripper is the last joint position
        return len(joints)
    return None


def with_vector_state(wire_observation: Any) -> Any:
    """The observation with a two-arm state as one plain vector, in ``state_width``'s order
    (left joints, left gripper, right joints, right gripper): what a server reading a vector
    takes from a Bimanual YAM. Any other state is sent as it is."""
    state = wire_observation.frame.robot_state
    if getattr(state, "state", None) is not None or not hasattr(state, "left_gripper"):
        return wire_observation
    vector = VectorRobotState(state=[
        *map(float, state.left_joint_positions), float(state.left_gripper),
        *map(float, state.right_joint_positions), float(state.right_gripper),
    ])
    return dataclasses.replace(
        wire_observation,
        frame=wire_observation.frame.model_copy(update={"robot_state": vector}),
    )


def observation_helper(deployment: Any) -> str:
    """How to build an observation for ``deployment`` (π0.5's, or an exported base's): its
    robot's helper, or ``dreamscale.robot.observation`` with its camera keys and state width."""
    layout = getattr(deployment, "layout", None)
    if layout is not None:
        return layout.observe_helper
    keys = ", ".join(f'"{key}": …' for key in deployment.camera_keys)
    return (
        f"dreamscale.robot.observation(cameras={{{keys}}}, state=[{deployment.state_dim} values])"
    )


def check_observation(
    wire_observation: Any, deployment: Any, *, label: str = "π0.5",
    plain_state: bool = False,
) -> None:
    """Refuse, before sending, an observation that isn't the deployment's robot: the camera
    keys in the deployment's order, and a state of its width (``plain_state``: one plain
    vector, as FLUX's server reads it). ``label`` names the deployment's base (π0.5, FLUX,
    ABC-VLA, InternW0, Hy-VLA)."""
    frame = wire_observation.frame
    given = tuple(camera.camera_id for camera in frame.cameras)
    expected = deployment.camera_keys
    if given != expected:
        raise _mismatch(
            deployment,
            label,
            "cameras",
            f"[{', '.join(given)}]",
            f"[{', '.join(expected)}], in that order (deployment {deployment.id})",
        )
    if plain_state and getattr(frame.robot_state, "state", None) is None:
        raise _mismatch(
            deployment,
            label,
            "state",
            f"a {type(frame.robot_state).__name__}",
            f"one vector of {deployment.state_dim} values (deployment {deployment.id})",
        )
    width = state_width(frame.robot_state)
    if width != deployment.state_dim:
        raise _mismatch(
            deployment,
            label,
            "state",
            f"{width} values" if width is not None else type(frame.robot_state).__name__,
            f"{deployment.state_dim} values (deployment {deployment.id})",
        )


def _mismatch(deployment: Any, label: str, field: str, given: str, expected: str):
    return errors.ObservationError(
        errors.ErrorInfo(
            code="invalid_observation",
            problem=f"`{field}` is {given}; expected {expected}",
            cause=f"the observation is not the robot this {label} deployment was built for",
            fix=f"build it with {observation_helper(deployment)}",
        )
    )


def non_joint_run_error(ref: str, state_dim: Any = None, action_dim: Any = None):
    """`dreamscale run <robot>` refusing a deployment whose actions aren't joint targets."""
    widths = f" (state {state_dim} → {action_dim} actions)" if state_dim and action_dim else ""
    return errors.DreamscaleError(
        errors.ErrorInfo(
            code="invalid_deployment",
            problem=f"{ref}'s actions aren't joint targets{widths}",
            cause="`dreamscale run` sends joint targets and holds the robot in place while it "
            "waits; this deployment runs from Python only",
            fix=f'drive it from Python: dreamscale.connect("{_default_public_id()}", '
            f'deployment="{ref}"), then policy.next_action(...) or policy.predict(...)',
        )
    )


def _default_public_id() -> str:
    """The name sessions open the default deployments base by."""
    from dreamscale import deploy_bases

    return families.family(deploy_bases.default().family).deploy.public_id


def in_use_session_id(error: errors.DreamscaleError, payload: Any) -> str | None:
    """The session holding a deployment, from a 409 ``deployment_in_use``."""
    body = payload.get("error", payload) if isinstance(payload, Mapping) else {}
    if isinstance(body, Mapping) and body.get("session_id"):
        return str(body["session_id"])
    for text in (error.info.problem, error.info.cause, error.info.fix):
        match = _SESSION_ID.search(text)
        if match:
            return match.group(0)
    return None
