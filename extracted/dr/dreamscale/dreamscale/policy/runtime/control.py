from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import ceil
from typing import Literal

from dreamscale.policy.runtime.calibration import NetworkCalibrationProfile

ControlName = Literal[
    "adaptive",
    "prefer_freshness",
    "balanced",
    "prefer_robustness",
    "ultra_aggressive",
]
MethodOProfileName = Literal["prefer_freshness", "balanced", "prefer_robustness"]
MethodORelaxationPolicy = Literal[
    "safe_band_relaxation", "upper_surplus_relaxation"
]


@dataclass(frozen=True)
class MethodOProfile:
    tail_percentile: str
    lower_fraction: float
    upper_fraction: float
    fresh_reserve_fraction: float
    freshness_target_fraction: float
    risk_decay: float


METHOD_O_PROFILES: dict[MethodOProfileName, MethodOProfile] = {
    "prefer_freshness": MethodOProfile("p90", 0.05, 0.25, 0.15, 0.40, 0.60),
    "balanced": MethodOProfile("p95", 0.10, 0.35, 0.10, 0.50, 0.75),
    "prefer_robustness": MethodOProfile("p95", 0.15, 0.50, 0.05, 0.65, 0.90),
}


@dataclass(frozen=True)
class MethodOConfig:
    profile: MethodOProfileName = "balanced"
    relaxation_policy: MethodORelaxationPolicy = "safe_band_relaxation"
    startup_threshold_fraction: float = 0.50
    max_threshold_fraction: float = 1.0
    warmup_chunks_to_ignore: int = 1
    tail_window_samples: int = 12
    safe_relax_after_samples: int = 4

    def __post_init__(self) -> None:
        if self.relaxation_policy not in {
            "safe_band_relaxation",
            "upper_surplus_relaxation",
        }:
            raise ValueError("unknown Method O relaxation policy")


@dataclass(frozen=True)
class EagerRefillQueueConfig:
    pass


@dataclass(frozen=True)
class MethodODecision:
    latency_steps: int
    observed_slack_steps: int
    lower_bound_steps: int
    upper_bound_steps: int
    threshold_steps: int
    hard_ceiling_steps: int
    classification: Literal["green", "yellow", "red"]


class MethodOController:
    def __init__(
        self,
        *,
        chunk_size: int,
        control_hz: float,
        config: MethodOConfig | None = None,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if control_hz <= 0:
            raise ValueError("control_hz must be positive")
        self._chunk_size = int(chunk_size)
        self._control_hz = float(control_hz)
        self._config = config or MethodOConfig()
        self._profile = METHOD_O_PROFILES[self._config.profile]
        self._latency_steps: deque[int] = deque(maxlen=self._config.tail_window_samples)
        self._slack_steps: deque[int] = deque(maxlen=self._config.tail_window_samples)
        self._over_upper_flags: deque[bool] = deque(maxlen=self._config.tail_window_samples)
        self._chunks_seen = 0
        self._baseline_latency_steps: int | None = None
        self._tail_latency_steps: int | None = None
        self._risk_premium_steps = 0.0
        self._safe_relax_run = 0
        self._safe_in_band_run = 0
        self._upper_slack_relax_run = 0
        self._recovery_mode: Literal[
            "none", "in_band_safe", "over_upper_surplus"
        ] = "none"
        self._last_decision: MethodODecision | None = None
        self._threshold = self._startup_threshold()

    @property
    def threshold_steps(self) -> int:
        return self._threshold

    @property
    def last_decision(self) -> MethodODecision | None:
        return self._last_decision

    @property
    def risk_premium_steps(self) -> int:
        return int(ceil(self._risk_premium_steps))

    @property
    def config(self) -> MethodOConfig:
        return self._config

    @property
    def recovery_mode(self) -> str:
        return self._recovery_mode

    def seed_calibration(
        self,
        profile: NetworkCalibrationProfile,
        *,
        mode: Literal["light", "normal"] = "normal",
    ) -> None:
        latency_steps = getattr(profile, "latency_steps", {}) or {}
        baseline = int(
            latency_steps.get("p50", self._ms_to_steps(profile.p50_ms))
        )
        if mode == "light":
            self._baseline_latency_steps = baseline
            self._tail_latency_steps = baseline
            self._latency_steps.clear()
            for _ in range(3):
                self._latency_steps.append(max(0, baseline))
            self._risk_premium_steps = 0.0
            self._update_decision(actions_remaining=0, roundtrip_ms=profile.p50_ms)
            return
        recommended_percentile = getattr(profile, "recommended_percentile", "p90")
        tail_key = "p95" if recommended_percentile == "p95" else "p90"
        tail = int(
            latency_steps.get(
                tail_key,
                self._ms_to_steps(
                    profile.p95_ms if tail_key == "p95" else profile.p90_ms
                ),
            )
        )
        self._baseline_latency_steps = baseline
        self._tail_latency_steps = tail
        self._latency_steps.clear()
        for key in ("p50", "p50", "p50", "p75", "p90", "p95", "max"):
            value = int(latency_steps.get(key, baseline))
            self._latency_steps.append(max(0, value))
        if getattr(profile, "burst_class", None) in {"sparse_spike", "sustained_hump"}:
            self._risk_premium_steps = max(
                self._risk_premium_steps,
                float(max(0, tail - baseline)),
            )
        self._update_decision(actions_remaining=0, roundtrip_ms=profile.p50_ms)

    def record_roundtrip_ms(self, roundtrip_ms: float) -> None:
        self.record_roundtrip_result(
            roundtrip_ms=roundtrip_ms,
            request_actions_remaining=None,
            usable_for_slack=False,
        )

    def record_roundtrip_result(
        self,
        *,
        roundtrip_ms: float,
        request_actions_remaining: int | None,
        usable_for_slack: bool,
    ) -> None:
        if roundtrip_ms < 0.0:
            raise ValueError("roundtrip_ms must be non-negative")
        self._chunks_seen += 1
        if self._chunks_seen <= self._config.warmup_chunks_to_ignore:
            return

        latency_steps = self._ms_to_steps(roundtrip_ms)
        self._latency_steps.append(latency_steps)
        tail_percentile = 90 if self._config.profile == "prefer_freshness" else 95
        self._tail_latency_steps = _percentile_nearest(self._latency_steps, tail_percentile)
        baseline_candidate = _percentile_nearest(self._latency_steps, 50)

        if not usable_for_slack or request_actions_remaining is None:
            self._baseline_latency_steps = self._update_baseline(
                baseline_candidate=baseline_candidate,
                allow_relax=False,
            )
            self._update_decision(
                actions_remaining=request_actions_remaining or 0,
                roundtrip_ms=roundtrip_ms,
            )
            return

        baseline_for_bounds = self._baseline_latency_steps or baseline_candidate
        tail_for_bounds = self._tail_latency_steps or baseline_for_bounds
        lower_bound, upper_bound = self._slack_bounds(
            baseline_latency_steps=baseline_for_bounds,
            tail_latency_steps=tail_for_bounds,
        )
        observed_slack = int(request_actions_remaining) - latency_steps
        lower_shortfall = max(0, lower_bound - observed_slack)
        lower_miss = observed_slack < lower_bound
        negative_slack = observed_slack < 0
        over_upper = observed_slack > upper_bound
        safe_in_band = not lower_miss and not negative_slack
        self._slack_steps.append(observed_slack)
        self._over_upper_flags.append(over_upper)
        self._safe_in_band_run = self._safe_in_band_run + 1 if safe_in_band else 0
        self._recovery_mode = "none"
        if self._upper_slack_surplus_is_stable(upper_bound):
            self._upper_slack_relax_run += 1
            self._safe_relax_run += 1
            self._recovery_mode = "over_upper_surplus"
        elif (
            self._config.relaxation_policy == "safe_band_relaxation"
            and self._safe_in_band_run >= self._config.safe_relax_after_samples
        ):
            self._upper_slack_relax_run = 0
            self._safe_relax_run += 1
            self._recovery_mode = "in_band_safe"
        else:
            self._upper_slack_relax_run = 0
            self._safe_relax_run = 0

        if lower_shortfall > 0:
            self._risk_premium_steps = max(
                float(lower_shortfall),
                self._profile.risk_decay * self._risk_premium_steps,
            )
        elif self._recovery_mode != "none":
            self._risk_premium_steps *= self._profile.risk_decay
        self._baseline_latency_steps = self._update_baseline(
            baseline_candidate=baseline_candidate,
            allow_relax=self._recovery_mode != "none",
        )
        self._update_decision(
            actions_remaining=int(request_actions_remaining),
            roundtrip_ms=roundtrip_ms,
        )

    def _startup_threshold(self) -> int:
        return max(
            1,
            min(
                self._max_threshold_steps(),
                ceil(self._config.startup_threshold_fraction * self._chunk_size),
            ),
        )

    def _max_threshold_steps(self) -> int:
        return max(1, ceil(self._config.max_threshold_fraction * self._chunk_size))

    def _ms_to_steps(self, roundtrip_ms: float) -> int:
        return max(0, ceil(float(roundtrip_ms) * self._control_hz / 1000.0))

    def _slack_bounds(
        self,
        *,
        baseline_latency_steps: int,
        tail_latency_steps: int,
    ) -> tuple[int, int]:
        jitter_steps = max(0, int(tail_latency_steps) - int(baseline_latency_steps))
        lower_bound = max(ceil(self._profile.lower_fraction * self._chunk_size), jitter_steps)
        upper_bound = max(
            ceil(self._profile.upper_fraction * self._chunk_size),
            lower_bound + ceil(0.10 * self._chunk_size),
        )
        return lower_bound, upper_bound

    def _upper_slack_surplus_is_stable(self, upper_bound_steps: int) -> bool:
        if len(self._slack_steps) < self._config.safe_relax_after_samples:
            return False
        recent_flags = list(self._over_upper_flags)[-self._config.safe_relax_after_samples :]
        if not all(recent_flags):
            return False
        recent_slack = list(self._slack_steps)[-self._config.safe_relax_after_samples :]
        return min(recent_slack) >= upper_bound_steps + 1

    def _update_baseline(self, *, baseline_candidate: int, allow_relax: bool) -> int:
        if self._baseline_latency_steps is None:
            return int(baseline_candidate)
        if baseline_candidate > self._baseline_latency_steps:
            return int(baseline_candidate)
        if allow_relax:
            return max(1, int(baseline_candidate))
        return self._baseline_latency_steps

    def _update_decision(self, *, actions_remaining: int, roundtrip_ms: float) -> None:
        decision = compute_method_o_threshold(
            roundtrip_ms=roundtrip_ms,
            control_hz=self._control_hz,
            chunk_size=self._chunk_size,
            actions_remaining=actions_remaining,
            profile=self._config.profile,
            baseline_latency_steps=self._baseline_latency_steps,
            tail_latency_steps=self._tail_latency_steps,
            risk_premium_steps=int(ceil(self._risk_premium_steps)),
            max_threshold_steps=self._max_threshold_steps(),
        )
        self._last_decision = decision
        self._threshold = decision.threshold_steps


def control_config_for_name(name: ControlName) -> MethodOConfig | EagerRefillQueueConfig:
    if name == "ultra_aggressive":
        return EagerRefillQueueConfig()
    if name == "adaptive":
        return MethodOConfig("balanced")
    if name not in METHOD_O_PROFILES:
        raise ValueError(f"unknown control mode: {name}")
    return MethodOConfig(name)


def compute_method_o_threshold(
    *,
    roundtrip_ms: float,
    control_hz: float,
    chunk_size: int,
    actions_remaining: int,
    profile: MethodOProfileName = "balanced",
    baseline_latency_steps: int | None = None,
    tail_latency_steps: int | None = None,
    risk_premium_steps: int = 0,
    max_threshold_steps: int | None = None,
) -> MethodODecision:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if control_hz <= 0:
        raise ValueError("control_hz must be positive")
    profile_config = METHOD_O_PROFILES[profile]
    latency_steps = max(0, ceil(roundtrip_ms * control_hz / 1000.0))
    baseline = latency_steps if baseline_latency_steps is None else int(baseline_latency_steps)
    tail = latency_steps if tail_latency_steps is None else int(tail_latency_steps)
    jitter_steps = max(0, tail - baseline)
    lower_bound = max(ceil(profile_config.lower_fraction * chunk_size), jitter_steps)
    upper_bound = max(
        ceil(profile_config.upper_fraction * chunk_size),
        lower_bound + ceil(0.10 * chunk_size),
    )
    risk_latency = max(baseline, tail, baseline + max(0, risk_premium_steps))
    desired = risk_latency + lower_bound
    fresh_reserve = ceil(profile_config.fresh_reserve_fraction * chunk_size)
    hard_ceiling = max(
        1,
        min(max_threshold_steps or chunk_size, max(1, chunk_size - fresh_reserve)),
    )
    freshness_target = min(
        hard_ceiling,
        ceil(profile_config.freshness_target_fraction * chunk_size),
    )
    if desired <= freshness_target:
        classification: Literal["green", "yellow", "red"] = "green"
        threshold = desired
    elif desired <= hard_ceiling:
        classification = "yellow"
        threshold = desired
    else:
        classification = "red"
        threshold = hard_ceiling
    return MethodODecision(
        latency_steps=latency_steps,
        observed_slack_steps=int(actions_remaining) - latency_steps,
        lower_bound_steps=lower_bound,
        upper_bound_steps=upper_bound,
        threshold_steps=threshold,
        hard_ceiling_steps=hard_ceiling,
        classification=classification,
    )


def _percentile_nearest(samples: deque[int], percentile: int) -> int:
    if not samples:
        return 0
    ordered = sorted(int(sample) for sample in samples)
    index = ceil((percentile / 100.0) * len(ordered)) - 1
    return ordered[min(max(index, 0), len(ordered) - 1)]
