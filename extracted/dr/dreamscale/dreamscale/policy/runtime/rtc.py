from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass
from math import ceil, floor, isfinite
from typing import Any, Literal

from dreamscale_transport import RtcRequestContext

from dreamscale.policy.runtime.control import METHOD_O_PROFILES, MethodOProfileName

RtcProfileName = Literal["green", "yellow", "red"]
RtcDelayEstimatorSource = Literal[
    "unavailable",
    "network_calibration",
    "network_calibration_light",
    "runtime_merge_delay",
]

DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID = "dynamic_full_horizon_v1"
# Training-time RTC (Isaac 0.5, the MolmoAct2 YAM train-time checkpoint): the client
# sends its next planned rows and timing; the server decides, when inference starts, how
# many rows to pin as a hard prefix, capped by its own artifact (Isaac 12, MolmoAct2 15).
LATE_BOUND_PREFIX_RTC_CONTRACT_ID = "isaac05_late_bound_prefix_v1"
# The rows a request carries when its deployment declares no cap of its own (the shared
# models' artifacts pin at most 15); a deployment's cap (late_bound_prefix_rows) replaces it.
LATE_BOUND_PREFIX_MAX_ROWS = 15


def late_bound_prefix_rows(deployment: Any) -> int | None:
    """The most committed rows a deployment pins per request (what its checkpoint trained, or
    the cap its owner set), or None when it declares none."""
    for name in ("rtc_max_prefix_rows", "rtc_max_delay"):
        value = getattr(deployment, name, None)
        if type(value) is int and value > 0:
            return value
    return None

STATIC_RTC_PROFILE_PREFIX_RATIOS: dict[RtcProfileName, float] = {
    "green": 0.50,
    "yellow": 0.60,
    "red": 0.80,
}


@dataclass(frozen=True)
class RtcConfig:
    enabled: bool = False
    contract_id: str | None = None
    prefix_attention_schedule: Literal["linear", "exp", "ones", "zeros"] = "exp"
    max_guidance_weight: float = 10.0


@dataclass(frozen=True)
class RtcEstimatorState:
    chunk_size: int
    action_hz: float
    latency_steps_p50: int
    latency_steps_p75: int
    latency_steps_p90: int
    latency_steps_p95: int
    tail_latency_steps: int
    lower_slack_steps: int
    upper_slack_steps: int
    fresh_reserve_steps: int
    control_mode: str = "adaptive"
    guarded_delay_target_steps: int | None = None
    feasibility_mode: RtcProfileName | None = None


class RtcDelayEstimator:
    def __init__(
        self,
        *,
        chunk_size: int,
        action_hz: float,
        control_mode: str,
        window_samples: int = 32,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if action_hz <= 0.0:
            raise ValueError("action_hz must be positive")
        if window_samples <= 0:
            raise ValueError("window_samples must be positive")
        self._chunk_size = int(chunk_size)
        self._action_hz = float(action_hz)
        self._control_mode = str(control_mode)
        self._runtime_delay_steps: deque[int] = deque(maxlen=int(window_samples))
        self._calibration_state: RtcEstimatorState | None = None
        self._calibration_source: RtcDelayEstimatorSource = "unavailable"
        self._calibration_sample_count = 0

    @property
    def source(self) -> RtcDelayEstimatorSource:
        if self._runtime_delay_steps:
            return "runtime_merge_delay"
        if self._calibration_state is not None:
            return self._calibration_source
        return "unavailable"

    @property
    def sample_count(self) -> int:
        if self._runtime_delay_steps:
            return len(self._runtime_delay_steps)
        return self._calibration_sample_count

    def seed_calibration(self, profile: object) -> None:
        usage = str(getattr(profile, "runtime_calibration_usage", "not_used"))
        if usage not in {"light", "normal"}:
            return
        self._calibration_sample_count = max(
            0,
            int(
                getattr(
                    profile,
                    "retained_sample_count",
                    getattr(profile, "usable_sample_count", 0),
                )
                or 0
            ),
        )
        method_profile = (
            self._control_mode
            if self._control_mode in METHOD_O_PROFILES
            else "balanced"
        )
        state = build_rtc_estimator_state_from_calibration(
            profile,
            chunk_size=self._chunk_size,
            action_hz=self._action_hz,
            method_o_profile=method_profile,
            control_mode=self._control_mode,
        )
        if usage == "light":
            p50 = max(0, int(state.latency_steps_p50))
            state = RtcEstimatorState(
                chunk_size=state.chunk_size,
                action_hz=state.action_hz,
                latency_steps_p50=p50,
                latency_steps_p75=p50,
                latency_steps_p90=p50,
                latency_steps_p95=p50,
                tail_latency_steps=p50,
                lower_slack_steps=state.lower_slack_steps,
                upper_slack_steps=state.upper_slack_steps,
                fresh_reserve_steps=state.fresh_reserve_steps,
                control_mode=state.control_mode,
            )
            self._calibration_source = "network_calibration_light"
        else:
            self._calibration_source = "network_calibration"
        self._calibration_state = state

    def record(self, delay_steps: int, *, eligible: bool) -> bool:
        if not eligible:
            return False
        delay = int(delay_steps)
        if delay < 0:
            raise ValueError("delay_steps must be non-negative")
        self._runtime_delay_steps.append(delay)
        return True

    def state(self) -> RtcEstimatorState:
        if self._runtime_delay_steps:
            samples = list(self._runtime_delay_steps)
            p50 = _percentile_steps(samples, 50.0)
            p75 = _percentile_steps(samples, 75.0)
            p90 = _percentile_steps(samples, 90.0)
            p95 = _percentile_steps(samples, 95.0)
            lower, upper, fresh_reserve = _runtime_estimator_bounds(
                chunk_size=self._chunk_size,
                p50=p50,
                p90=p90,
                control_mode=self._control_mode,
            )
            return RtcEstimatorState(
                chunk_size=self._chunk_size,
                action_hz=self._action_hz,
                latency_steps_p50=p50,
                latency_steps_p75=max(p50, p75),
                latency_steps_p90=max(p75, p90),
                latency_steps_p95=max(p90, p95),
                tail_latency_steps=max(p75, p90),
                lower_slack_steps=lower,
                upper_slack_steps=upper,
                fresh_reserve_steps=fresh_reserve,
                control_mode=self._control_mode,
            )
        if self._calibration_state is not None:
            return self._calibration_state
        lower, upper, fresh_reserve = _runtime_estimator_bounds(
            chunk_size=self._chunk_size,
            p50=0,
            p90=0,
            control_mode=self._control_mode,
        )
        return RtcEstimatorState(
            chunk_size=self._chunk_size,
            action_hz=self._action_hz,
            latency_steps_p50=0,
            latency_steps_p75=0,
            latency_steps_p90=0,
            latency_steps_p95=0,
            tail_latency_steps=0,
            lower_slack_steps=lower,
            upper_slack_steps=upper,
            fresh_reserve_steps=fresh_reserve,
            control_mode=self._control_mode,
        )


@dataclass(frozen=True)
class RtcGeometryProfile:
    name: RtcProfileName
    inference_delay_steps: int
    execution_horizon_steps: int
    chunk_size: int

    @property
    def fixed_steps(self) -> int:
        return self.inference_delay_steps

    @property
    def modifiable_steps(self) -> int:
        return max(0, self.execution_horizon_steps - self.inference_delay_steps)

    @property
    def new_actions(self) -> int:
        return max(0, self.chunk_size - self.execution_horizon_steps)


@dataclass(frozen=True)
class RtcProfileSet:
    profiles: tuple[RtcGeometryProfile, ...]
    static: bool = False
    source: str = "runtime"

    def profile(self, name: RtcProfileName) -> RtcGeometryProfile:
        for profile in self.profiles:
            if profile.name == name:
                return profile
        raise ValueError(f"RTC profile {name!r} is not present")

    def mark_static(self, source: str) -> RtcProfileSet:
        return RtcProfileSet(profiles=self.profiles, static=True, source=source)


@dataclass(frozen=True)
class StaticRtcProfile:
    name: RtcProfileName
    prefix_steps: int
    chunk_size: int
    contract_id: str = "fixed_ratio_v1"

    @property
    def inference_delay_steps(self) -> int:
        return 0

    @property
    def execution_horizon_steps(self) -> int:
        return self.prefix_steps

    @property
    def fixed_steps(self) -> int:
        return 0

    @property
    def modifiable_steps(self) -> int:
        return self.prefix_steps

    @property
    def new_actions(self) -> int:
        return self.chunk_size - self.prefix_steps

    @property
    def prefix_tensor_steps(self) -> int:
        return self.chunk_size


def build_static_rtc_profile_set(
    *,
    chunk_size: int,
    contract_id: str = "fixed_ratio_v1",
) -> list[StaticRtcProfile]:
    if contract_id != "fixed_ratio_v1":
        raise ValueError("only fixed_ratio_v1 is supported by the static RTC builder")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    return [
        StaticRtcProfile(
            name=name,
            prefix_steps=min(chunk_size, _round_half_up(ratio * chunk_size)),
            chunk_size=chunk_size,
            contract_id=contract_id,
        )
        for name, ratio in STATIC_RTC_PROFILE_PREFIX_RATIOS.items()
    ]


def build_rtc_profile_set(
    config: RtcConfig,
    state: RtcEstimatorState,
) -> RtcProfileSet:
    chunk_size = int(state.chunk_size)
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if float(state.action_hz) <= 0.0:
        raise ValueError("action_hz must be positive")
    if not config.enabled:
        return RtcProfileSet(profiles=())

    p50 = max(0, int(state.latency_steps_p50))
    p75 = max(p50, int(state.latency_steps_p75))
    tail = max(p75, int(state.tail_latency_steps))
    p95 = max(tail, int(state.latency_steps_p95))
    if state.guarded_delay_target_steps is not None:
        p95 = max(p95, int(state.guarded_delay_target_steps))

    specs: tuple[tuple[RtcProfileName, int, int], ...] = (
        ("green", p50, p75),
        ("yellow", p75, tail),
        ("red", tail, p95),
    )
    return RtcProfileSet(
        profiles=tuple(
            _profile_from_latency_pair(
                name=name,
                fixed_seed=fixed_seed,
                tail_seed=tail_seed,
                chunk_size=chunk_size,
                lower_slack_steps=state.lower_slack_steps,
                fresh_reserve_steps=state.fresh_reserve_steps,
                control_mode=state.control_mode,
            )
            for name, fixed_seed, tail_seed in specs
        )
    )


def build_rtc_estimator_state_from_calibration(
    profile: object,
    *,
    chunk_size: int,
    action_hz: float,
    method_o_profile: MethodOProfileName = "balanced",
    control_mode: str = "adaptive",
) -> RtcEstimatorState:
    latency_steps = getattr(profile, "latency_steps", {}) or {}
    method_profile = METHOD_O_PROFILES.get(method_o_profile, METHOD_O_PROFILES["balanced"])
    resolved_chunk_size = int(getattr(profile, "chunk_size", chunk_size) or chunk_size)
    resolved_action_hz = float(getattr(profile, "control_hz", action_hz) or action_hz)
    p50 = _latency_step(
        latency_steps,
        "p50",
        getattr(profile, "p50_ms", 0.0),
        action_hz=resolved_action_hz,
    )
    p75 = _latency_step(
        latency_steps,
        "p75",
        getattr(profile, "p75_ms", 0.0),
        action_hz=resolved_action_hz,
    )
    p90 = _latency_step(
        latency_steps,
        "p90",
        getattr(profile, "p90_ms", 0.0),
        action_hz=resolved_action_hz,
    )
    p95 = _latency_step(
        latency_steps,
        "p95",
        getattr(profile, "p95_ms", 0.0),
        action_hz=resolved_action_hz,
    )
    tail_key = "p95" if getattr(profile, "recommended_percentile", "p90") == "p95" else "p90"
    tail = p95 if tail_key == "p95" else p90
    jitter = max(0, int(tail) - int(p50))
    lower = max(ceil(method_profile.lower_fraction * resolved_chunk_size), jitter)
    upper = max(
        ceil(method_profile.upper_fraction * resolved_chunk_size),
        lower + ceil(0.10 * resolved_chunk_size),
    )
    fresh_reserve = (
        1
        if control_mode == "ultra_aggressive"
        else ceil(method_profile.fresh_reserve_fraction * resolved_chunk_size)
    )
    return RtcEstimatorState(
        chunk_size=resolved_chunk_size,
        action_hz=resolved_action_hz,
        latency_steps_p50=p50,
        latency_steps_p75=p75,
        latency_steps_p90=p90,
        latency_steps_p95=p95,
        tail_latency_steps=tail,
        lower_slack_steps=lower,
        upper_slack_steps=upper,
        fresh_reserve_steps=fresh_reserve,
        control_mode=control_mode,
    )


def select_static_rtc_profile_name(classification: str | None) -> RtcProfileName:
    if classification == "red":
        return "red"
    if classification == "yellow":
        return "yellow"
    return "green"


def build_rtc_context_for_queue(
    *,
    config: RtcConfig,
    chunk_size: int,
    action_dim: int | None,
    profile_name: RtcProfileName,
    reference_actions: Sequence[Sequence[float]] | None,
    profile_set: RtcProfileSet | None = None,
    desired_execution_horizon_steps: int | None = None,
    estimator_state: RtcEstimatorState | None = None,
    estimator_source: RtcDelayEstimatorSource = "unavailable",
    estimator_sample_count: int = 0,
) -> RtcRequestContext:
    if not config.enabled:
        return RtcRequestContext(enabled=False)
    contract_id = config.contract_id or "calibrated_static"
    if contract_id == DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID:
        if estimator_state is None:
            raise ValueError("dynamic RTC requires an estimator state")
        return build_dynamic_full_horizon_rtc_request(
            config=config,
            state=estimator_state,
            action_dim=action_dim,
            reference_actions=reference_actions or (),
            estimator_source=estimator_source,
            estimator_sample_count=estimator_sample_count,
        )
    if contract_id == "calibrated_static":
        return build_calibrated_static_rtc_request(
            config=config,
            chunk_size=chunk_size,
            action_dim=action_dim,
            profile_name=profile_name,
            reference_actions=reference_actions or (),
            profile_set=profile_set,
            desired_execution_horizon_steps=desired_execution_horizon_steps,
        )
    return build_static_rtc_request(
        config=config,
        chunk_size=chunk_size,
        action_dim=action_dim,
        profile_name=profile_name,
        reference_actions=reference_actions or (),
    )


def build_late_bound_prefix_rtc_request(
    *,
    reference_actions: Sequence[Sequence[float]],
    previous_chunk_id: int | None,
    previous_chunk_receipt_unix_ns: int | None,
    client_send_unix_ns: int,
    max_rows: int | None = None,
) -> RtcRequestContext:
    """Next planned rows (at most ``max_rows``, the deployment's cap; 15 without one) plus the
    timing the server's late binding needs."""
    rows = [[float(value) for value in row] for row in reference_actions][
        : LATE_BOUND_PREFIX_MAX_ROWS if max_rows is None else max_rows
    ]
    telemetry: dict[str, int] = {"client_send_unix_ns": int(client_send_unix_ns)}
    if previous_chunk_id is not None and previous_chunk_receipt_unix_ns is not None:
        telemetry["previous_chunk_id"] = int(previous_chunk_id)
        telemetry["previous_chunk_receipt_unix_ns"] = int(previous_chunk_receipt_unix_ns)
    return RtcRequestContext(
        enabled=True,
        contract_id=LATE_BOUND_PREFIX_RTC_CONTRACT_ID,
        reference_actions=rows,
        reference_action_valid_steps=len(rows),
        telemetry=telemetry,
    )


def build_dynamic_full_horizon_rtc_request(
    *,
    config: RtcConfig,
    state: RtcEstimatorState,
    action_dim: int | None,
    reference_actions: Sequence[Sequence[float]],
    estimator_source: RtcDelayEstimatorSource = "unavailable",
    estimator_sample_count: int = 0,
) -> RtcRequestContext:
    if not config.enabled:
        return RtcRequestContext(enabled=False)
    contract_id = config.contract_id or DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID
    if contract_id != DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID:
        raise ValueError(
            f"RTC contract {contract_id!r} is not supported by dynamic request generation"
        )
    chunk_size = int(state.chunk_size)
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if float(state.action_hz) <= 0.0:
        raise ValueError("action_hz must be positive")
    fresh_reserve = _clamp(
        int(state.fresh_reserve_steps),
        1,
        max(1, chunk_size - 1),
    )
    fixed = _clamp(
        max(0, int(state.latency_steps_p75)),
        0,
        max(0, chunk_size - fresh_reserve),
    )
    target_delay = max(fixed, int(state.latency_steps_p90))
    transition_cap = max(1, ceil(float(state.action_hz) * 0.1))
    modifiable = min(max(0, target_delay - fixed), transition_cap)
    modifiable = _clamp(
        modifiable,
        0,
        max(0, chunk_size - fresh_reserve - fixed),
    )
    execution_horizon = fixed + modifiable
    padded_reference_actions, valid_steps = _pad_reference_actions(
        reference_actions,
        target_steps=chunk_size,
        action_dim=action_dim,
    )
    return RtcRequestContext(
        enabled=True,
        inference_delay_steps=fixed,
        execution_horizon_steps=execution_horizon,
        fixed_steps=fixed,
        modifiable_steps=modifiable,
        new_actions=chunk_size - execution_horizon,
        prefix_tensor_steps=chunk_size,
        prefix_attention_schedule=config.prefix_attention_schedule,
        max_guidance_weight=config.max_guidance_weight,
        reference_actions=padded_reference_actions,
        reference_action_valid_steps=valid_steps,
        profile=None,
        contract_id=contract_id,
        telemetry={
            "delay_estimator_source": estimator_source,
            "delay_estimator_sample_count": max(0, int(estimator_sample_count)),
            "latency_steps_p50": max(0, int(state.latency_steps_p50)),
            "latency_steps_p75": max(0, int(state.latency_steps_p75)),
            "latency_steps_p90": max(0, int(state.latency_steps_p90)),
            "latency_steps_p95": max(0, int(state.latency_steps_p95)),
            "fresh_reserve_steps": fresh_reserve,
            "transition_cap_steps": transition_cap,
        },
    )


def build_calibrated_static_rtc_request(
    *,
    config: RtcConfig,
    chunk_size: int,
    profile_name: RtcProfileName,
    reference_actions: Sequence[Sequence[float]],
    action_dim: int | None = None,
    profile_set: RtcProfileSet | None = None,
    desired_execution_horizon_steps: int | None = None,
) -> RtcRequestContext:
    if not config.enabled:
        return RtcRequestContext(enabled=False)
    contract_id = config.contract_id or "calibrated_static"
    if contract_id != "calibrated_static":
        raise ValueError(
            f"RTC contract {contract_id!r} is not supported by calibrated-static request generation"
        )
    profile = _select_calibrated_static_profile(
        profile_name=profile_name,
        profile_set=profile_set,
        chunk_size=chunk_size,
        desired_execution_horizon_steps=desired_execution_horizon_steps,
    )
    reference_prefix = _slice_reference_actions(
        reference_actions,
        max_steps=profile.execution_horizon_steps,
        action_dim=action_dim,
    )
    return RtcRequestContext(
        enabled=True,
        inference_delay_steps=profile.inference_delay_steps,
        execution_horizon_steps=profile.execution_horizon_steps,
        fixed_steps=profile.fixed_steps,
        modifiable_steps=profile.modifiable_steps,
        new_actions=profile.new_actions,
        prefix_attention_schedule=config.prefix_attention_schedule,
        max_guidance_weight=config.max_guidance_weight,
        reference_actions=reference_prefix or None,
        reference_action_valid_steps=len(reference_prefix),
        profile=profile.name,
        contract_id=None,
    )


def build_static_rtc_request(
    *,
    config: RtcConfig,
    chunk_size: int,
    profile_name: RtcProfileName,
    reference_actions: Sequence[Sequence[float]],
    action_dim: int | None = None,
) -> RtcRequestContext:
    if not config.enabled:
        return RtcRequestContext(enabled=False)
    contract_id = config.contract_id or "fixed_ratio_v1"
    if contract_id != "fixed_ratio_v1":
        raise ValueError(
            f"RTC contract {contract_id!r} is not supported by fixed-ratio request generation"
        )
    profile = next(
        candidate
        for candidate in build_static_rtc_profile_set(
            chunk_size=chunk_size, contract_id=contract_id
        )
        if candidate.name == profile_name
    )
    padded_reference_actions, valid_steps = _pad_reference_actions(
        reference_actions,
        target_steps=profile.prefix_tensor_steps,
        action_dim=action_dim,
    )
    return RtcRequestContext(
        enabled=True,
        inference_delay_steps=profile.inference_delay_steps,
        execution_horizon_steps=profile.execution_horizon_steps,
        fixed_steps=profile.fixed_steps,
        modifiable_steps=profile.modifiable_steps,
        new_actions=profile.new_actions,
        prefix_tensor_steps=profile.prefix_tensor_steps,
        prefix_attention_schedule=config.prefix_attention_schedule,
        max_guidance_weight=config.max_guidance_weight,
        reference_actions=padded_reference_actions,
        reference_action_valid_steps=valid_steps,
        profile=profile.name,
        contract_id=profile.contract_id,
    )


def _round_half_up(value: float) -> int:
    return int(float(value) + 0.5)


def _select_calibrated_static_profile(
    *,
    profile_name: RtcProfileName,
    profile_set: RtcProfileSet | None,
    chunk_size: int,
    desired_execution_horizon_steps: int | None,
) -> RtcGeometryProfile | StaticRtcProfile:
    profiles: Sequence[RtcGeometryProfile | StaticRtcProfile]
    if profile_set is not None and profile_set.profiles:
        profiles = profile_set.profiles
    else:
        profiles = build_static_rtc_profile_set(
            chunk_size=chunk_size, contract_id="fixed_ratio_v1"
        )
    if desired_execution_horizon_steps is None:
        for profile in profiles:
            if profile.name == profile_name:
                return profile
        raise ValueError(f"RTC profile {profile_name!r} is not present")

    floor_index = {"green": 0, "yellow": 1, "red": 2}[profile_name]
    selected = profiles[-1]
    for index, profile in enumerate(profiles):
        if index < floor_index:
            continue
        if int(profile.execution_horizon_steps) >= int(desired_execution_horizon_steps):
            selected = profile
            break
    return selected


def _profile_from_latency_pair(
    *,
    name: RtcProfileName,
    fixed_seed: int,
    tail_seed: int,
    chunk_size: int,
    lower_slack_steps: int,
    fresh_reserve_steps: int,
    control_mode: str,
) -> RtcGeometryProfile:
    fresh_reserve = _clamp(int(fresh_reserve_steps), 0, max(0, chunk_size - 1))
    fixed = _clamp(max(0, int(fixed_seed)), 0, max(0, chunk_size - fresh_reserve))
    jitter = max(0, int(tail_seed) - fixed)
    modifiable = (
        jitter
        if control_mode == "ultra_aggressive"
        else max(jitter, int(lower_slack_steps))
    )
    max_modifiable = max(0, chunk_size - fresh_reserve - fixed)
    modifiable = _clamp(modifiable, 0, max_modifiable)
    return RtcGeometryProfile(
        name=name,
        inference_delay_steps=fixed,
        execution_horizon_steps=fixed + modifiable,
        chunk_size=chunk_size,
    )


def _latency_step(
    latency_steps: object,
    key: str,
    fallback_ms: float,
    *,
    action_hz: float,
) -> int:
    if isinstance(latency_steps, dict) and key in latency_steps:
        return max(0, int(latency_steps[key]))
    return max(0, ceil(float(fallback_ms) * float(action_hz) / 1000.0))


def _runtime_estimator_bounds(
    *,
    chunk_size: int,
    p50: int,
    p90: int,
    control_mode: str,
) -> tuple[int, int, int]:
    method_profile_name = (
        control_mode if control_mode in METHOD_O_PROFILES else "balanced"
    )
    profile = METHOD_O_PROFILES[method_profile_name]
    jitter = max(0, int(p90) - int(p50))
    lower = max(ceil(profile.lower_fraction * chunk_size), jitter)
    upper = max(
        ceil(profile.upper_fraction * chunk_size),
        lower + ceil(0.10 * chunk_size),
    )
    fresh_reserve = (
        1
        if control_mode == "ultra_aggressive"
        else ceil(profile.fresh_reserve_fraction * chunk_size)
    )
    return lower, upper, max(1, fresh_reserve)


def _percentile_steps(values: Sequence[int], percentile: float) -> int:
    if not values:
        return 0
    if percentile < 0.0 or percentile > 100.0:
        raise ValueError("percentile must be within [0, 100]")
    ordered = sorted(float(max(0, int(value))) for value in values)
    if len(ordered) == 1:
        return int(ceil(ordered[0]))
    rank = (float(percentile) / 100.0) * float(len(ordered) - 1)
    lower_index = int(floor(rank))
    upper_index = int(ceil(rank))
    if lower_index == upper_index:
        return int(ceil(ordered[lower_index]))
    weight = rank - float(lower_index)
    interpolated = (ordered[lower_index] * (1.0 - weight)) + (
        ordered[upper_index] * weight
    )
    return int(ceil(interpolated))


def _clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def _pad_reference_actions(
    reference_actions: Sequence[Sequence[float]],
    *,
    target_steps: int,
    action_dim: int | None,
) -> tuple[list[list[float]], int]:
    actions = [list(map(float, action)) for action in reference_actions[:target_steps]]
    valid_steps = len(actions)
    resolved_action_dim = int(action_dim) if action_dim is not None else None
    if resolved_action_dim is not None and resolved_action_dim <= 0:
        raise ValueError("action_dim must be positive when provided")
    if actions:
        row_dim = len(actions[0])
        if any(len(action) != row_dim for action in actions):
            raise ValueError("reference_actions must have a consistent action dimension")
        resolved_action_dim = row_dim if resolved_action_dim is None else resolved_action_dim
        if resolved_action_dim != row_dim:
            raise ValueError("action_dim does not match reference action dimension")
        if any(not isfinite(value) for action in actions for value in action):
            raise ValueError("reference_actions must contain only finite values")
    if target_steps <= valid_steps:
        return actions, valid_steps
    if resolved_action_dim is None:
        raise ValueError("action_dim is required to pad an empty RTC reference tensor")
    padded = list(actions)
    padded.extend([[0.0] * resolved_action_dim for _ in range(target_steps - valid_steps)])
    return padded, valid_steps


def _slice_reference_actions(
    reference_actions: Sequence[Sequence[float]],
    *,
    max_steps: int,
    action_dim: int | None,
) -> list[list[float]]:
    if max_steps <= 0:
        return []
    actions = [list(map(float, action)) for action in reference_actions[:max_steps]]
    if not actions:
        return []
    row_dim = len(actions[0])
    if any(len(action) != row_dim for action in actions):
        raise ValueError("reference_actions must have a consistent action dimension")
    if any(not isfinite(value) for action in actions for value in action):
        raise ValueError("reference_actions must contain only finite values")
    if action_dim is not None and int(action_dim) != row_dim:
        raise ValueError("action_dim does not match reference action dimension")
    return actions
