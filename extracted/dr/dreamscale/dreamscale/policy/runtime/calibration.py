from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Literal

NetworkReadiness = Literal["green", "yellow", "red", "unknown"]
NetworkCalibrationModeName = Literal["off", "fast", "default", "rtc_graph", "extended"]
LatencyBurstClass = Literal[
    "stable",
    "sparse_spike",
    "sustained_hump",
    "bad_baseline",
    "out_of_envelope",
]
CalibrationConfidenceName = Literal["none", "very_low", "low", "normal", "strong"]
CalibrationRuntimeUsageName = Literal["not_used", "light", "normal"]
LatencyHealthName = Literal["excellent", "healthy", "variable", "constrained", "unknown"]
FixedThresholdCalibrationMode = Literal["off", "profiled"]

NETWORK_CALIBRATION_TIME_BUDGET_S: dict[NetworkCalibrationModeName, float] = {
    "off": 0.0,
    "fast": 2.0,
    "default": 7.0,
    "rtc_graph": 10.0,
    "extended": 30.0,
}
DEFAULT_FIXED_THRESHOLD_CALIBRATION_SLACK_STEPS = 2


@dataclass(frozen=True)
class NetworkCalibrationConfig:
    mode: NetworkCalibrationModeName = "default"
    time_budget_s: float | None = None
    fixed_threshold_mode: FixedThresholdCalibrationMode = "off"
    late_budget_steps: int | None = None

    def __post_init__(self) -> None:
        if self.mode not in NETWORK_CALIBRATION_TIME_BUDGET_S:
            raise ValueError(
                "network calibration mode must be one of "
                f"{list(NETWORK_CALIBRATION_TIME_BUDGET_S)}"
            )
        if self.mode == "off" and self.time_budget_s is not None:
            raise ValueError("time_budget_s is only valid when calibration is not off")
        if self.time_budget_s is not None and (
            not math.isfinite(float(self.time_budget_s))
            or float(self.time_budget_s) <= 0.0
        ):
            raise ValueError("time_budget_s must be finite and positive")
        if self.fixed_threshold_mode not in {"off", "profiled"}:
            raise ValueError("fixed_threshold_mode must be one of ['off', 'profiled']")
        if self.late_budget_steps is not None and self.late_budget_steps <= 0:
            raise ValueError("late_budget_steps must be positive when provided")

    @property
    def enabled(self) -> bool:
        return self.mode != "off"

    @property
    def resolved_time_budget_s(self) -> float:
        if self.time_budget_s is not None:
            return float(self.time_budget_s)
        return float(NETWORK_CALIBRATION_TIME_BUDGET_S[self.mode])


@dataclass(frozen=True)
class NetworkCalibrationSample:
    roundtrip_ms: float
    server_ms: float | None = None
    action_dim: int | None = None
    request_id: str = ""
    timing_ms: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        roundtrip_ms = float(self.roundtrip_ms)
        if not math.isfinite(roundtrip_ms) or roundtrip_ms < 0.0:
            raise ValueError("roundtrip_ms must be finite and non-negative")
        if self.action_dim is not None and self.action_dim <= 0:
            raise ValueError("action_dim must be positive when provided")
        timing: dict[str, float] = {}
        for key, value in self.timing_ms.items():
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                continue
            if math.isfinite(numeric):
                timing[str(key)] = numeric
        if self.server_ms is not None:
            server_ms = float(self.server_ms)
            if math.isfinite(server_ms):
                timing.setdefault("server_total", server_ms)
        object.__setattr__(self, "roundtrip_ms", roundtrip_ms)
        object.__setattr__(self, "timing_ms", timing)


@dataclass(frozen=True)
class NetworkCalibrationProfile:
    sample_count: int
    usable_sample_count: int
    raw_sample_count: int
    retained_sample_count: int
    discarded_warmup_sample_count: int
    discarded_warmup_rtt_ms: float | None
    control_hz: float
    chunk_size: int
    rtt_ms: dict[str, float]
    latency_steps: dict[str, int]
    server_timing_ms: dict[str, dict[str, float]]
    late_budget_steps: int
    late_budget_late_count: int
    late_budget_late_fraction: float
    max_consecutive_late_for_budget: int
    r8_late_count: int
    r8_late_fraction: float
    max_consecutive_late_for_r8: int
    full_horizon_violation_count: int
    full_horizon_violation_fraction: float
    max_single_jump_ms: float
    recommended_fixed_threshold_steps: int
    recommended_latency_steps: int
    readiness: NetworkReadiness
    burst_class: LatencyBurstClass | None
    calibration_confidence: CalibrationConfidenceName
    latency_health: LatencyHealthName
    runtime_calibration_usage: CalibrationRuntimeUsageName
    runtime_calibration_usage_label: str

    @property
    def p50_ms(self) -> float:
        return self.rtt_ms["p50"]

    @property
    def p75_ms(self) -> float:
        return self.rtt_ms["p75"]

    @property
    def p90_ms(self) -> float:
        return self.rtt_ms["p90"]

    @property
    def p95_ms(self) -> float:
        return self.rtt_ms["p95"]

    @property
    def max_ms(self) -> float:
        return self.rtt_ms["max"]

    @property
    def recommended_percentile(self) -> Literal["p90", "p95"]:
        return "p95" if self.usable_sample_count >= 8 else "p90"

    @property
    def fixed_threshold_steps(self) -> int:
        return self.recommended_fixed_threshold_steps

    def payload(self) -> dict[str, object]:
        return asdict(self)


def build_network_calibration_profile(
    samples: list[NetworkCalibrationSample] | None = None,
    *,
    config: NetworkCalibrationConfig | None = None,
    chunk_size: int,
    control_hz: float,
    late_budget_steps: int | None = None,
) -> NetworkCalibrationProfile:
    if control_hz <= 0:
        raise ValueError("control_hz must be positive")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    raw_samples = list(samples or [])
    if not raw_samples:
        raise ValueError("network calibration produced no usable samples")

    resolved_config = config or NetworkCalibrationConfig(
        late_budget_steps=late_budget_steps
    )
    usable, discarded_warmup = _retained_calibration_samples(raw_samples)
    confidence = _classify_calibration_confidence(len(usable))
    runtime_usage = _runtime_usage_for_confidence(confidence)
    runtime_usage_label = _runtime_usage_label(runtime_usage)
    resolved_late_budget_steps = _resolve_late_budget_steps(
        config=resolved_config,
        chunk_size=int(chunk_size),
    )
    if not usable:
        return NetworkCalibrationProfile(
            sample_count=len(raw_samples),
            usable_sample_count=0,
            raw_sample_count=len(raw_samples),
            retained_sample_count=0,
            discarded_warmup_sample_count=1,
            discarded_warmup_rtt_ms=float(discarded_warmup.roundtrip_ms),
            control_hz=float(control_hz),
            chunk_size=int(chunk_size),
            rtt_ms=_empty_rtt_percentiles(),
            latency_steps=_empty_latency_percentiles(),
            server_timing_ms={},
            late_budget_steps=resolved_late_budget_steps,
            late_budget_late_count=0,
            late_budget_late_fraction=0.0,
            max_consecutive_late_for_budget=0,
            r8_late_count=0,
            r8_late_fraction=0.0,
            max_consecutive_late_for_r8=0,
            full_horizon_violation_count=0,
            full_horizon_violation_fraction=0.0,
            max_single_jump_ms=0.0,
            recommended_fixed_threshold_steps=0,
            recommended_latency_steps=0,
            readiness="unknown",
            burst_class=None,
            calibration_confidence=confidence,
            latency_health="unknown",
            runtime_calibration_usage=runtime_usage,
            runtime_calibration_usage_label=runtime_usage_label,
        )

    rtts = [float(sample.roundtrip_ms) for sample in usable]
    latency_values = [_ms_to_steps(value, control_hz=control_hz) for value in rtts]
    full_horizon_steps = int(chunk_size)

    late_budget_flags = [
        value > resolved_late_budget_steps for value in latency_values
    ]
    full_horizon_flags = [value >= full_horizon_steps for value in latency_values]
    late_budget_count = sum(1 for flag in late_budget_flags if flag)
    full_horizon_count = sum(1 for flag in full_horizon_flags if flag)
    max_consecutive_late = _max_consecutive_true(late_budget_flags)

    p50_steps = _percentile_int(latency_values, 50.0)
    p90_steps = _percentile_int(latency_values, 90.0)
    p95_steps = _percentile_int(latency_values, 95.0)
    recommended_latency_steps = p95_steps if len(latency_values) >= 8 else p90_steps
    recommended_fixed_threshold_steps = min(
        int(chunk_size),
        int(recommended_latency_steps) + DEFAULT_FIXED_THRESHOLD_CALIBRATION_SLACK_STEPS,
    )

    burst_class = _classify_burst(
        p50_steps=p50_steps,
        p90_steps=p90_steps,
        late_budget_steps=resolved_late_budget_steps,
        full_horizon_steps=full_horizon_steps,
        full_horizon_count=full_horizon_count,
        late_budget_late_count=late_budget_count,
        max_consecutive_late=max_consecutive_late,
        usable_count=len(usable),
    )
    readiness = _classify_readiness(
        burst_class=burst_class,
        recommended_fixed_threshold_steps=recommended_fixed_threshold_steps,
        chunk_size=int(chunk_size),
    )
    latency_health = _classify_latency_health(
        readiness=readiness,
        burst_class=burst_class,
        latency_steps=latency_values,
        chunk_size=int(chunk_size),
        late_budget_steps=resolved_late_budget_steps,
    )

    return NetworkCalibrationProfile(
        sample_count=len(raw_samples),
        usable_sample_count=len(usable),
        raw_sample_count=len(raw_samples),
        retained_sample_count=len(usable),
        discarded_warmup_sample_count=1,
        discarded_warmup_rtt_ms=float(discarded_warmup.roundtrip_ms),
        control_hz=float(control_hz),
        chunk_size=int(chunk_size),
        rtt_ms={
            "p50": _percentile_float(rtts, 50.0),
            "p75": _percentile_float(rtts, 75.0),
            "p90": _percentile_float(rtts, 90.0),
            "p95": _percentile_float(rtts, 95.0),
            "max": max(rtts),
        },
        latency_steps={
            "p50": p50_steps,
            "p75": _percentile_int(latency_values, 75.0),
            "p90": p90_steps,
            "p95": p95_steps,
            "max": max(latency_values),
        },
        server_timing_ms=_timing_percentiles(usable),
        late_budget_steps=resolved_late_budget_steps,
        late_budget_late_count=late_budget_count,
        late_budget_late_fraction=float(late_budget_count) / float(len(usable)),
        max_consecutive_late_for_budget=max_consecutive_late,
        r8_late_count=late_budget_count,
        r8_late_fraction=float(late_budget_count) / float(len(usable)),
        max_consecutive_late_for_r8=max_consecutive_late,
        full_horizon_violation_count=full_horizon_count,
        full_horizon_violation_fraction=float(full_horizon_count) / float(len(usable)),
        max_single_jump_ms=_max_single_jump_ms(rtts),
        recommended_fixed_threshold_steps=recommended_fixed_threshold_steps,
        recommended_latency_steps=recommended_latency_steps,
        readiness=readiness,
        burst_class=burst_class,
        calibration_confidence=confidence,
        latency_health=latency_health,
        runtime_calibration_usage=runtime_usage,
        runtime_calibration_usage_label=runtime_usage_label,
    )


def _retained_calibration_samples(
    samples: list[NetworkCalibrationSample],
) -> tuple[list[NetworkCalibrationSample], NetworkCalibrationSample]:
    return list(samples[1:]), samples[0]


def _classify_calibration_confidence(retained_count: int) -> CalibrationConfidenceName:
    if retained_count <= 0:
        return "none"
    if retained_count <= 3:
        return "very_low"
    if retained_count <= 7:
        return "low"
    if retained_count <= 11:
        return "normal"
    return "strong"


def _runtime_usage_for_confidence(
    confidence: CalibrationConfidenceName,
) -> CalibrationRuntimeUsageName:
    if confidence == "low":
        return "light"
    if confidence in {"normal", "strong"}:
        return "normal"
    return "not_used"


def _runtime_usage_label(usage: CalibrationRuntimeUsageName) -> str:
    if usage == "normal":
        return "using calibration"
    if usage == "light":
        return "using calibration lightly"
    return "not using calibration"


def _empty_rtt_percentiles() -> dict[str, float]:
    return {"p50": 0.0, "p75": 0.0, "p90": 0.0, "p95": 0.0, "max": 0.0}


def _empty_latency_percentiles() -> dict[str, int]:
    return {"p50": 0, "p75": 0, "p90": 0, "p95": 0, "max": 0}


def _ms_to_steps(value_ms: float, *, control_hz: float) -> int:
    return int(math.ceil((float(value_ms) / 1000.0) * float(control_hz)))


def _resolve_late_budget_steps(
    *,
    config: NetworkCalibrationConfig,
    chunk_size: int,
) -> int:
    if config.late_budget_steps is not None:
        return max(1, min(int(chunk_size), int(config.late_budget_steps)))
    return max(1, int(math.ceil(float(chunk_size) * 0.5)))


def _percentile_float(values: list[float], percentile: float) -> float:
    if not values:
        raise ValueError("percentile requires at least one value")
    if percentile < 0.0 or percentile > 100.0:
        raise ValueError("percentile must be within [0, 100]")
    ordered = sorted(float(value) for value in values)
    if len(ordered) == 1:
        return float(ordered[0])
    rank = (float(percentile) / 100.0) * float(len(ordered) - 1)
    low = int(math.floor(rank))
    high = int(math.ceil(rank))
    if low == high:
        return float(ordered[low])
    weight = rank - float(low)
    return float(ordered[low]) * (1.0 - weight) + float(ordered[high]) * weight


def _percentile_int(values: list[int], percentile: float) -> int:
    return int(math.ceil(_percentile_float([float(value) for value in values], percentile)))


def _timing_percentiles(
    samples: list[NetworkCalibrationSample],
) -> dict[str, dict[str, float]]:
    by_key: dict[str, list[float]] = {}
    for sample in samples:
        for key, raw in sample.timing_ms.items():
            try:
                value = float(raw)
            except (TypeError, ValueError):
                continue
            if math.isfinite(value):
                by_key.setdefault(str(key), []).append(value)
    return {
        key: {
            "p50": _percentile_float(values, 50.0),
            "p90": _percentile_float(values, 90.0),
            "p95": _percentile_float(values, 95.0),
            "max": max(values),
        }
        for key, values in sorted(by_key.items())
        if values
    }


def _classify_burst(
    *,
    p50_steps: int,
    p90_steps: int,
    late_budget_steps: int,
    full_horizon_steps: int,
    full_horizon_count: int,
    late_budget_late_count: int,
    max_consecutive_late: int,
    usable_count: int,
) -> LatencyBurstClass:
    if p50_steps >= full_horizon_steps or full_horizon_count >= 2:
        return "out_of_envelope"
    if max_consecutive_late >= 2:
        return "sustained_hump"
    if p50_steps >= late_budget_steps:
        return "bad_baseline"
    if late_budget_late_count > 0:
        return "sparse_spike"
    if usable_count >= 8 and p90_steps - p50_steps >= 4:
        return "sparse_spike"
    return "stable"


def _classify_readiness(
    *,
    burst_class: LatencyBurstClass,
    recommended_fixed_threshold_steps: int,
    chunk_size: int,
) -> NetworkReadiness:
    if burst_class == "out_of_envelope":
        return "red"
    if recommended_fixed_threshold_steps >= chunk_size:
        return "red"
    if burst_class in {"bad_baseline", "sparse_spike", "sustained_hump"}:
        return "yellow"
    return "green"


def _classify_latency_health(
    *,
    readiness: NetworkReadiness,
    burst_class: LatencyBurstClass,
    latency_steps: list[int],
    chunk_size: int,
    late_budget_steps: int,
) -> LatencyHealthName:
    if not latency_steps or readiness == "unknown":
        return "unknown"
    p50_steps = _percentile_int(latency_steps, 50.0)
    p95_steps = _percentile_int(latency_steps, 95.0)
    if readiness == "red":
        return "constrained"
    if burst_class != "stable" or p95_steps > late_budget_steps:
        return "variable"
    if p50_steps <= max(1, int(math.ceil(float(chunk_size) * 0.25))):
        return "excellent"
    return "healthy"


def _max_consecutive_true(values: list[bool]) -> int:
    best = 0
    current = 0
    for value in values:
        current = current + 1 if value else 0
        best = max(best, current)
    return best


def _max_single_jump_ms(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return max(
        abs(values[index] - values[index - 1])
        for index in range(1, len(values))
    )
