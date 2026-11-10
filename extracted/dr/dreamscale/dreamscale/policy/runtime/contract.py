from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from math import isfinite
from typing import Any

from dreamscale_transport import catalog, families
from dreamscale_transport.images import WireImage

from dreamscale.model_names import internal_model, public_model
from dreamscale.policy.deployment import session_base
from dreamscale.policy.exported_deployments import exported_base
from dreamscale.policy.runtime import served

MIN_CONTROL_HZ = 5
MAX_CONTROL_HZ = 30


@dataclass(frozen=True)
class RuntimeContract:
    action_hz: float
    chunk_size: int
    action_dim: int | None = None
    action_space: str = "unknown"
    hold_behavior: str = "zero"
    # The rate the checkpoint itself emits actions at. `action_hz` is the rate
    # the caller executes them at, which is the tunable one. They are equal by
    # default; where they differ, every emitted action is still executed and the
    # chunk's wall-clock horizon scales with the commanded rate.
    native_action_hz: float | None = None
    # These coordinates have a model-level [0, 1] contract, independent of any
    # robot's site-specific joint limits. Raw DreamZero YAM grippers are excluded.
    normalized_gripper_indices: tuple[int, ...] = ()
    fixed_rate: bool = False
    # Robot coordinates, independent of checkpoint identity or gripper scaling.
    joint_groups: tuple[tuple[int, ...], ...] = ()
    gripper_indices: tuple[int, ...] = ()
    joint_unit: str | None = None
    startup_motion_delay_s: float = 0.0
    # A checkpoint may generate a longer sequence than its qualified executable
    # prefix. Wire requests retain chunk_size; local queues admit only this prefix.
    execution_horizon: int | None = None
    task_prepare_timeout_s: float = 120.0
    # The image the model's server consumes. Cameras are resized to it before JPEG
    # encoding (smaller uploads, a shorter transmission tail); the server's own resize
    # then passes them through untouched. None sends frames at capture resolution.
    wire_image: WireImage | None = None
    # Used instead when the server predates ``wire_image`` (no ``context_v1`` capability).
    legacy_wire_image: WireImage | None = None
    # The checkpoint conditions on its recent commands: each request carries up to this
    # many actions executed on the ticks before the observation, oldest first.
    action_history: int = 0
    # The checkpoint also sees older camera frames at fixed offsets: each request carries
    # the frames captured this many control ticks before the observation, oldest first,
    # where the server advertises history frames.
    history_offsets: tuple[int, ...] = ()
    # Those older observations' robot states travel too (``state_history``), oldest first.
    state_history: bool = False
    # FLUX exports condition on every measured control tick, independently of sparse VAE
    # snapshots. This is distinct from older models' snapshot-only state_history.
    measured_state_steps: int = 0
    # InternW0: the episode's first frames are also sent (its anchor), oldest first, with
    # the frames ``history_offsets`` ticks back (policy.context.EpisodeHistory).
    history_anchor: bool = False
    # Hy-VLA: the frames this many EXECUTED actions before the observation, oldest first,
    # those the episode has reached (policy.context.TickHistory); the server fills the rest.
    history_ticks: tuple[int, ...] = ()
    # Long-WAM: offsets the episode hasn't reached send its first frame once (the server
    # repeats it, as upstream's window does) instead of nothing.
    history_start: bool = False
    # The server keeps the episode (Verne V0.5): the frames of every this-many executed steps
    # are sent ahead, and each request names its step (policy.context.EpisodeTicks).
    episode_tick_steps: int = 0
    # Executed actions between two replans at least (0: as the control mode decides): the next
    # request waits until the plan has this many fewer rows than a fresh chunk (Verne V0.5:
    # 12 of 18, the per-robot request rate its units are sized for).
    min_replan_steps: int = 0
    # Rows that aren't the state (end-effector poses) held at ``current_position``: each
    # action value's index in the state vector (-1: zero, e.g. a mobile base held still).
    # Empty: the hold is the observation's own (``hold_action`` or its joint positions).
    hold_indices: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if not isfinite(self.task_prepare_timeout_s) or self.task_prepare_timeout_s <= 0:
            raise ValueError("task_prepare_timeout_s must be finite and positive")
        if not isfinite(float(self.action_hz)) or float(self.action_hz) <= 0.0:
            raise ValueError("action_hz must be finite and positive")
        if int(self.chunk_size) <= 0:
            raise ValueError("chunk_size must be positive")
        if self.execution_horizon is not None and (
            type(self.execution_horizon) is not int
            or not 1 <= self.execution_horizon <= self.chunk_size
        ):
            raise ValueError("execution_horizon must be an integer from 1 to chunk_size")
        if self.action_dim is not None and int(self.action_dim) <= 0:
            raise ValueError("action_dim must be positive when provided")
        if type(self.action_history) is not int or not 0 <= self.action_history <= 32:
            raise ValueError("action_history must be an integer from 0 to 32")
        offsets = self.history_offsets
        if (
            not isinstance(offsets, tuple)
            or len(offsets) > 2
            or any(type(offset) is not int or not 1 <= offset <= 32 for offset in offsets)
            or list(offsets) != sorted(set(offsets), reverse=True)
        ):
            raise ValueError("history_offsets must be at most two distinct ticks, oldest first")
        if self.state_history and not offsets:
            raise ValueError("state_history needs the older observations of history_offsets")
        if self.history_anchor and (len(offsets) != 1 or self.state_history
                                    or self.measured_state_steps):
            raise ValueError("an anchored history takes one recent offset and no states")
        ticks = self.history_ticks
        if (
            not isinstance(ticks, tuple)
            or len(ticks) > 15
            or any(type(tick) is not int or not 1 <= tick <= 64 for tick in ticks)
            or list(ticks) != sorted(set(ticks), reverse=True)
        ):
            # A camera's strip carries them and the current frame (at most 16, messages.py).
            raise ValueError("history_ticks must be at most 15 distinct ticks, oldest first")
        if ticks and (offsets or self.history_anchor or self.state_history
                      or self.measured_state_steps):
            raise ValueError("a tick history takes no other observation history")
        if self.history_start and not ticks:
            raise ValueError("history_start needs a tick history")
        if type(self.measured_state_steps) is not int or not 0 <= self.measured_state_steps <= 31:
            raise ValueError("measured_state_steps must be 0-31")
        if type(self.episode_tick_steps) is not int or not 0 <= self.episode_tick_steps <= 64:
            raise ValueError("episode_tick_steps must be 0-64")
        if type(self.min_replan_steps) is not int or not (
                0 <= self.min_replan_steps < self.execution_chunk_size):
            raise ValueError("min_replan_steps must be 0 to the executed rows - 1")
        if self.episode_tick_steps and (ticks or offsets or self.history_anchor
                                        or self.state_history or self.measured_state_steps):
            raise ValueError("an episode kept by the server takes no other observation history")
        native = self.action_hz if self.native_action_hz is None else self.native_action_hz
        if not isfinite(float(native)) or float(native) <= 0.0:
            raise ValueError("native_action_hz must be finite and positive")
        indices = self.normalized_gripper_indices
        if len(set(indices)) != len(indices) or any(
            type(index) is not int
            or index < 0
            or self.action_dim is None
            or index >= self.action_dim
            for index in indices
        ):
            raise ValueError("normalized gripper indices must identify distinct action coordinates")
        coordinates = (*self.joint_indices, *self.gripper_indices)
        if self.joint_groups and (
            any(not group for group in self.joint_groups)
            or any(type(index) is not int for index in coordinates)
            or len(set(coordinates)) != len(coordinates)
            or set(coordinates) != set(range(self.action_dim or 0))
            or not set(indices).issubset(self.gripper_indices)
            or self.joint_unit not in {"rad", "deg"}
            or self.action_space not in {"absolute_joint_position", "raw_absolute_joint"}
            or self.hold_behavior != "current_position"
        ):
            raise ValueError("joint layout must describe every absolute joint/gripper coordinate")
        if not isfinite(self.startup_motion_delay_s) or self.startup_motion_delay_s < 0:
            raise ValueError("startup_motion_delay_s must be finite and nonnegative")
        if self.startup_motion_delay_s and not self.joint_groups:
            raise ValueError("measured startup requires an explicit joint layout")

    @property
    def joint_indices(self) -> tuple[int, ...]:
        return tuple(index for group in self.joint_groups for index in group)

    @property
    def measured_bootstrap(self) -> bool:
        return self.startup_motion_delay_s > 0

    @property
    def native_hz(self) -> float:
        return self.action_hz if self.native_action_hz is None else self.native_action_hz

    @property
    def horizon_s(self) -> float:
        """Wall-clock span of one emitted chunk at the commanded rate."""

        return self.chunk_size / self.action_hz

    @property
    def execution_chunk_size(self) -> int:
        return self.chunk_size if self.execution_horizon is None else self.execution_horizon

    @property
    def supported_control_hz(self) -> tuple[int, ...]:
        """Command rates the caller may ask for.

        Every emitted action is executed, so the chunk stretches or compresses
        in time rather than being resampled. That means any whole rate in range
        qualifies: nothing is dropped, interpolated, or otherwise transformed
        between what the checkpoint emitted and what the robot executes.
        """

        if self.fixed_rate:
            return (int(self.native_hz),)
        return tuple(range(MIN_CONTROL_HZ, MAX_CONTROL_HZ + 1))


# Each catalog model's own runtime contract (dreamscale_transport.catalog, its ``client``).
_MODEL_CONTRACTS: dict[str, RuntimeContract] = {
    entry.id: RuntimeContract(**entry.client.contract)
    for entry in catalog.CATALOG if entry.client.contract is not None
}


@cache
def _base_previews() -> dict[str, RuntimeContract]:
    """What a caller sees of a deployment base's sessions before one opens (its
    ``preview_contract``), by the base's id: the session's resolved contract replaces it."""
    from dreamscale import deploy_bases

    return {
        families.family(base.family).deploy.base: RuntimeContract(**base.preview_contract)
        for base in deploy_bases.bases() if base.preview_contract is not None
    }


def _known_contract(model: str) -> RuntimeContract | None:
    return _MODEL_CONTRACTS.get(model) or _base_previews().get(model)


def deployment_preview_contract() -> RuntimeContract:
    """What a robot deployment's contract is before its session opens (the default base's
    preview: joint targets held in place); the session's contract replaces it."""
    from dreamscale import deploy_bases

    return _base_previews()[families.family(deploy_bases.default().family).deploy.base]


def has_runtime_contract(model: str) -> bool:
    """Whether this SDK carries the model's own runtime contract (a model it knows)."""
    return _known_contract(internal_model(model)) is not None


def follows_server_contract(model: str | None) -> bool:
    """A model this SDK has no contract or wire for (one released after it): its session's
    contract is the one the server sends (``server_contract``)."""
    model = internal_model(model) if model else model
    return model is None or (
        _known_contract(model) is None and exported_base(model) is None
        and session_base(model) is None
        and not any(served.hook(model, name) is not None
                    for name in ("own_contract", "base", "control_hz"))
    )


def _unknown(model: str | None) -> ValueError:
    name = public_model(model) if model else "this model"
    return ValueError(
        f"{name} is not a model this SDK knows, so its runtime contract (rate, chunk, action "
        "width) is the one its server sends with the session; connect to it first, or "
        "upgrade dreamscale"
    )


def server_contract(
    model: str | None, resolved_config: Any | None, *, action_hz: float | None = None,
    chunk_size: int | None = None,
) -> RuntimeContract:
    """The runtime contract the server sends with a session (its resolved config's rate,
    chunk, width, action space and hold), for a model this SDK has no contract for; refused
    when the server sent none (and the caller didn't set the rate and chunk itself)."""
    action_hz = _optional_float_attr(resolved_config, "action_hz") or action_hz
    chunk_size = _optional_int_attr(resolved_config, "chunk_size") or chunk_size
    if action_hz is None or chunk_size is None:
        name = public_model(model) if model else "this model"
        raise ValueError(
            f"the server sent no runtime contract for {name} (its action rate and chunk "
            "size), and this SDK doesn't know the model; upgrade dreamscale"
        )
    return RuntimeContract(
        action_hz=action_hz,
        chunk_size=chunk_size,
        action_dim=_optional_int_attr(resolved_config, "action_dim"),
        action_space=_optional_str_attr(resolved_config, "action_space") or "unknown",
        hold_behavior=_optional_str_attr(resolved_config, "hold_behavior") or "zero",
    )


def runtime_contract_for_model(model: str | None) -> RuntimeContract:
    model = internal_model(model) if model else model
    exported = exported_base(model)
    if exported is not None:
        raise ValueError(
            f"{exported.label} deployments require the server's exported runtime contract"
        )
    own = served.hook(model, "own_contract")
    if own is not None:
        own(model)  # a model whose contract only its server knows refuses here
    known = _known_contract(model) if model is not None else None
    if known is None:
        # No default rate or chunk: a model this SDK doesn't know runs its server's contract.
        raise _unknown(model)
    return known


def resolve_control_hz(model: str | None, requested: int | float | None) -> float | None:
    """Resolve one model's command rate, defaulting to its native rate.

    This is the only place a DreamZero control rate is decided. Every other
    layer reads it rather than restating it: the rate had drifted independently
    across the transport constants, the SDK contract, the control-plane
    capabilities, the Inspect adapter, and the published wheel, and each
    disagreement was silent.
    """

    exported = exported_base(model)
    if exported is not None:
        if requested is not None:
            raise ValueError(f"{exported.label} uses its exported action rate; omit control_hz")
        return None
    rate = served.hook(model, "control_hz")
    if rate is not None:
        return rate(model, requested)
    session = session_base(internal_model(model)) if model else None
    if session is not None:
        # A deployment's rate is the one it was trained at, which the session reports.
        return session.resolve_control_hz(requested)
    unknown = follows_server_contract(internal_model(model) if model else model)
    if unknown and requested is None:
        return None  # the server's contract (with the session) sets the rate
    contract = None if unknown else runtime_contract_for_model(model)
    if requested is None:
        return contract.action_hz
    if isinstance(requested, bool) or not isinstance(requested, int | float):
        raise ValueError("control_hz must be an integer")
    if not float(requested).is_integer():
        raise ValueError("control_hz must be a whole number of hertz")
    resolved = int(requested)
    supported = (range(MIN_CONTROL_HZ, MAX_CONTROL_HZ + 1) if contract is None
                 else contract.supported_control_hz)
    if resolved not in supported:
        chunk = "the chunk" if contract is None else contract.chunk_size
        raise ValueError(
            f"control_hz {resolved} is out of range for {public_model(model)}; "
            f"supported rates are {MIN_CONTROL_HZ} to {MAX_CONTROL_HZ} Hz "
            f"inclusive. The emitted chunk is executed in full at the rate you "
            f"choose, so it spans {chunk}/rate seconds."
        )
    return float(resolved)


def resolve_runtime_contract(
    *,
    model: str | None,
    resolved_config: Any | None,
    action_hz_override: float | None = None,
    chunk_size_override: int | None = None,
    control_hz: float | None = None,
    deployment: Any | None = None,
) -> RuntimeContract:
    model = internal_model(model) if model else model
    exported = exported_base(model)
    if exported is not None:
        contract = exported.runtime_contract(resolved_config, deployment)
        if any(value is not None and value != contract.action_hz
               for value in (action_hz_override, control_hz)) or (
            chunk_size_override is not None and chunk_size_override != contract.chunk_size
        ):
            raise ValueError(
                f"{exported.label} uses the checkpoint's exported action rate and horizon"
            )
        return contract
    execution_horizon = _optional_attr(resolved_config, "execution_horizon")
    generated_horizon = _optional_attr(resolved_config, "chunk_size")
    if execution_horizon is not None and (
        type(execution_horizon) is not int
        or type(generated_horizon) is not int
        or not 1 <= execution_horizon <= generated_horizon
    ):
        raise ValueError("execution_horizon must be an integer from 1 to chunk_size")
    # The model's wire checks the served contract and the overrides it takes (served).
    check = served.hook(model, "check")
    if check is not None:
        chunk_size_override = check(
            model, resolved_config, execution_horizon=execution_horizon,
            action_hz_override=action_hz_override, chunk_size_override=chunk_size_override,
            control_hz=control_hz,
        )
    built = served.hook(model, "base")
    if built is not None:
        base = built(model, resolved_config, lambda: runtime_contract_for_model(model))
    elif (session := session_base(model)) is not None:
        # Its sessions' contract, entirely from the server (and its deployment block).
        base = session.runtime_contract(resolved_config, deployment, chunk_size_override)
    elif follows_server_contract(model):
        base = server_contract(model, resolved_config, action_hz=action_hz_override,
                               chunk_size=chunk_size_override)
    else:
        base = runtime_contract_for_model(model)
    action_hz = _optional_float_attr(resolved_config, "action_hz") or base.action_hz
    chunk_size = _optional_int_attr(resolved_config, "chunk_size") or base.chunk_size
    action_dim = _optional_int_attr(resolved_config, "action_dim")
    if action_dim is None:
        action_dim = base.action_dim
    action_space = _optional_str_attr(resolved_config, "action_space") or base.action_space
    hold_behavior = _optional_str_attr(resolved_config, "hold_behavior") or base.hold_behavior
    if action_hz_override is not None:
        action_hz = float(action_hz_override)
    if chunk_size_override is not None:
        chunk_size = int(chunk_size_override)
    native_action_hz = None
    if control_hz is not None and float(control_hz) != float(action_hz):
        # The whole chunk is executed at the commanded rate, so its horizon
        # stretches or compresses with that rate: 24 actions span 0.8 s at
        # 30 Hz and 1.6 s at 15 Hz. Nothing is dropped or interpolated, which
        # is what keeps the executed trajectory identical to the emitted one.
        native_action_hz = float(action_hz)
        action_hz = float(control_hz)
    own_width = action_dim == base.action_dim
    return RuntimeContract(
        action_hz=float(action_hz),
        chunk_size=int(chunk_size),
        action_dim=action_dim,
        action_space=action_space,
        hold_behavior=hold_behavior,
        native_action_hz=native_action_hz,
        fixed_rate=base.fixed_rate,
        # The joint layout, unit grippers and measured startup describe the model's own
        # action width; a session that resolves another width (a deployment's shapes: an
        # Isaac 0.5 custom robot on the YAM host, B26) has none of them here.
        normalized_gripper_indices=base.normalized_gripper_indices if own_width else (),
        joint_groups=base.joint_groups if own_width else (),
        gripper_indices=base.gripper_indices if own_width else (),
        joint_unit=base.joint_unit if own_width else None,
        startup_motion_delay_s=base.startup_motion_delay_s if own_width else 0.0,
        task_prepare_timeout_s=base.task_prepare_timeout_s,
        execution_horizon=(
            base.execution_horizon if execution_horizon is None else execution_horizon
        ),
        wire_image=base.wire_image,
        legacy_wire_image=base.legacy_wire_image,
        action_history=base.action_history,
        history_offsets=base.history_offsets,
        state_history=base.state_history,
        measured_state_steps=base.measured_state_steps,
    )


def _strictly_differs(resolved_config: Any | None, expected: dict) -> bool:
    """A served value that isn't the expected one, or is a bool standing in for a number."""
    return any(
        isinstance(_optional_attr(resolved_config, key), bool)
        or _optional_attr(resolved_config, key) != value
        for key, value in expected.items()
    )


def catalog_check(
    model: str, label: str, resolved_config: Any | None, *, execution_horizon: Any,
    action_hz_override: float | None, chunk_size_override: int | None,
    control_hz: float | None,
) -> int | None:
    """The served contract is the model's catalog contract (rate, chunk, width, space, hold),
    on its default backend and RTC, executing its catalog horizon; overrides keep its rate and
    chunk. ``label`` names the model in refusals."""
    entry = catalog.entry(model)
    contract, defaults = entry.contract, entry.defaults
    expected = {
        "action_hz": contract.action_hz, "chunk_size": contract.chunk_size,
        "action_dim": contract.action_dim, "action_space": contract.action_space,
        "hold_behavior": contract.hold_behavior, "backend": defaults.backend,
        "rtc": defaults.rtc,
    }
    if _strictly_differs(resolved_config, expected):
        raise ValueError(f"{label} server returned an incomplete or incompatible contract")
    horizon = contract.execution_horizon
    if execution_horizon is not None and execution_horizon != horizon:
        raise ValueError(f"{label} requires a {horizon}-action execution horizon")
    if any(value is not None and value != contract.action_hz
           for value in (action_hz_override, control_hz)):
        raise ValueError(f"{label} requires {contract.action_hz} Hz execution")
    if chunk_size_override is not None and chunk_size_override != contract.chunk_size:
        raise ValueError(f"{label} requires {contract.chunk_size}-action chunks")
    return chunk_size_override


def fixed_check(
    label: str, resolved_config: Any | None, expected: dict, *, action_hz: int,
    chunk_size: int, action_dim: int, refused: bool = False,
    action_hz_override: float | None, chunk_size_override: int | None,
    control_hz: float | None,
) -> int | None:
    """The served contract is exactly ``expected`` (a fixed chunk/width/rate geometry, named
    so in the refusal; ``refused``: the wire found another mismatch); overrides keep its rate
    and chunk. ``label`` names the model in refusals."""
    if refused or _strictly_differs(resolved_config, expected):
        raise ValueError(
            f"{label} server returned an incomplete or incompatible "
            f"{chunk_size}/{action_dim}/{action_hz} contract"
        )
    if any(value is not None and value != action_hz
           for value in (action_hz_override, control_hz)):
        raise ValueError(f"{label} requires {action_hz} Hz execution")
    if chunk_size_override is not None and chunk_size_override != chunk_size:
        raise ValueError(f"{label} requires a {chunk_size}-action chunk")
    return chunk_size_override


def _optional_float_attr(value: Any | None, name: str) -> float | None:
    raw = _optional_attr(value, name)
    if raw is None:
        return None
    return float(raw)


def _optional_int_attr(value: Any | None, name: str) -> int | None:
    raw = _optional_attr(value, name)
    if raw is None:
        return None
    return int(raw)


def _optional_str_attr(value: Any | None, name: str) -> str | None:
    raw = _optional_attr(value, name)
    if raw is None:
        return None
    text = str(raw)
    return text or None


def _optional_attr(value: Any | None, name: str) -> Any | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value.get(name)
    return getattr(value, name, None)
