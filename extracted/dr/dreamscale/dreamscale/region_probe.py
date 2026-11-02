from __future__ import annotations

import asyncio
import inspect
import re
import statistics
import time
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

import httpx
from dreamscale_transport import catalog

from dreamscale.model_names import public_model
from dreamscale.policy.config import OptimizationConfig
from dreamscale.policy.types import RegionPreference

REGION_PROBE_TOTAL_TIMEOUT_S = 2.0
REGION_PROBE_SAMPLES_PER_REGION = 5
REGION_PROBE_MIN_SUCCESSES = 3
REGION_ORDER_SOURCE = "client_https_rtt"
# Region-choice candidates (the region record's probes, region_choice.py) never order a
# session; a connect doesn't ask for them, and drops any it gets.
REGION_CHOICE = "region_choice"
# "auto" is "nearest" by its new name: the same request on the wire.
_REGION_MODES = frozenset(("auto", "nearest", "available"))
_REGION_ID = re.compile(r"^[a-z][a-z0-9-]{0,30}[a-z0-9]$")
# The region record's permanent aliases (dreamscale_transport.regions): sent in their AWS-style
# spelling so control planes that know only those accept the new names too.
_WIRE_NAMES = {
    "us-west": "us-west-2",
    "us-east": "us-east-1",
    "eu-west": "eu-central-1",
    "australia": "ap-southeast-2",
}

ProbeStatus = Literal["ok", "degraded", "failed"]
ProbeCallable = Callable[
    [httpx.AsyncClient, str, str],
    Awaitable[tuple[str, float] | None],
]


@dataclass(frozen=True)
class RegionMeasurement:
    region: str
    median_ms: float | None
    mad_ms: float | None
    successful_samples: int
    attempted_samples: int

    def to_wire(self) -> dict[str, object]:
        return {
            "region": self.region,
            "median_ms": self.median_ms,
            "mad_ms": self.mad_ms,
            "successful_samples": self.successful_samples,
            "attempted_samples": self.attempted_samples,
        }


@dataclass(frozen=True)
class RegionProbeResult:
    order: tuple[str, ...]
    measurements: tuple[RegionMeasurement, ...]
    status: ProbeStatus
    confident_winner: str | None
    # A transparent intercepting proxy answered, so the round trips say nothing about regions.
    intercepted: bool = False


async def create_session_with_rtt_region_order(
    control: Any,
    model: str,
    *,
    region: RegionPreference | None = "auto",
    provider: str | None = None,
    idle_timeout: int | None = None,
    keep_warm: int = 0,
    optimization_config: OptimizationConfig | dict[str, Any] | None = None,
    speed: str | None = None,
    checkpoint: str | None = None,
) -> Any:
    validate_provider_selection(model, provider, region)
    region = validate_speed_selection(model, speed, provider, region)
    resolved_region = _validate_region_preference(region)
    if resolved_region not in _REGION_MODES:
        return await _create_session(
            control,
            model,
            provider=provider,
            speed=speed,
            region_mode="custom",
            preferred_region=_WIRE_NAMES.get(resolved_region, resolved_region),
            region_pin=True,
            idle_timeout=idle_timeout,
            keep_warm=keep_warm,
            optimization_config=optimization_config,
            checkpoint=checkpoint,
            probe_result=None,
        )

    probe_result = (
        None
        if provider == "modal" or speed == "fast"
        else await _best_effort_region_order(
            control, model, optimization_config=optimization_config, provider=provider
        )
    )
    preferred_region = probe_result.order[0] if probe_result and probe_result.order else None
    if resolved_region == "nearest":
        return await _create_session(
            control,
            model,
            provider=provider,
            speed=speed,
            region_mode="nearest",
            preferred_region=preferred_region,
            region_pin=True,
            idle_timeout=idle_timeout,
            keep_warm=keep_warm,
            optimization_config=optimization_config,
            checkpoint=checkpoint,
            probe_result=probe_result,
        )
    return await _create_session(
        control,
        model,
        provider=provider,
        speed=speed,
        region_mode="available",
        preferred_region=None,
        region_pin=False,
        idle_timeout=idle_timeout,
        keep_warm=keep_warm,
        optimization_config=optimization_config,
        checkpoint=checkpoint,
        probe_result=probe_result,
    )


async def _best_effort_region_order(
    control: Any,
    model: str,
    *,
    optimization_config: OptimizationConfig | dict[str, Any] | None,
    provider: str | None = None,
) -> RegionProbeResult | None:
    probe_candidates = getattr(control, "probe_candidates", None)
    if probe_candidates is None:
        return _failed_probe_result()
    try:
        candidates = await probe_candidates(
            model,
            optimization_config=optimization_config,
            **({"provider": provider} if provider is not None else {}),
        )
        candidates = [
            candidate
            for candidate in candidates or ()
            if isinstance(candidate, Mapping) and candidate.get("purpose") != REGION_CHOICE
        ]
        if not candidates:
            # No regions to measure (e.g. a Modal-only model): routing doesn't
            # use a probe, so report none rather than a failed one.
            return None
        return await rank_regions_by_https_rtt(candidates)
    except Exception:
        if provider is not None:
            raise
        # Probe failure is a valid degraded network condition, not grounds to
        # fail session creation. Keep it explicit in the request so the control
        # plane does not misrepresent its deterministic fallback as measured.
        return _failed_probe_result()


async def rank_regions_by_https_rtt(
    candidates: list[dict[str, str]],
    *,
    timeout_s: float = REGION_PROBE_TOTAL_TIMEOUT_S,
    samples_per_region: int = REGION_PROBE_SAMPLES_PER_REGION,
    probe: ProbeCallable | None = None,
) -> RegionProbeResult:
    filtered = [
        {"region": str(candidate.get("region")), "url": str(candidate.get("url"))}
        for candidate in candidates
        if candidate.get("region") and candidate.get("url")
    ]
    if not filtered:
        return _failed_probe_result()

    attempted = max(1, samples_per_region)
    per_request_timeout = max(0.05, min(0.35, timeout_s))
    timeout = httpx.Timeout(per_request_timeout, connect=min(0.25, per_request_timeout))
    probe_once = probe or _probe_once
    samples: dict[str, list[float]] = {candidate["region"]: [] for candidate in filtered}
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
        tasks = [
            asyncio.create_task(
                _probe_region_sequentially(
                    client,
                    candidate["region"],
                    candidate["url"],
                    attempted,
                    probe_once,
                )
            )
            for candidate in filtered
        ]
        done, pending = await asyncio.wait(tasks, timeout=timeout_s)
        for task in pending:
            task.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        for task in done:
            region, region_samples = task.result()
            samples[region].extend(region_samples)

    return rank_region_samples(
        samples,
        candidate_order=tuple(candidate["region"] for candidate in filtered),
        attempted_samples=attempted,
    )


async def _probe_region_sequentially(
    client: httpx.AsyncClient,
    region: str,
    url: str,
    samples: int,
    probe: ProbeCallable,
) -> tuple[str, list[float]]:
    """Probe one region serially so connection reuse approximates steady RTT.

    Different regions execute concurrently, bounding user-visible delay without
    creating same-region request bursts that distort the measurement.
    """
    timings: list[float] = []
    for _ in range(samples):
        result = await probe(client, region, url)
        if result is not None:
            timings.append(float(result[1]))
    return region, timings


def rank_region_samples(
    samples: Mapping[str, Sequence[float]],
    *,
    candidate_order: Sequence[str] | None = None,
    attempted_samples: int = REGION_PROBE_SAMPLES_PER_REGION,
) -> RegionProbeResult:
    order_hint = tuple(candidate_order or samples.keys())
    all_regions = tuple(dict.fromkeys((*order_hint, *samples.keys())))
    measurements = tuple(
        _measurement(
            region,
            samples.get(region, ()),
            attempted_samples=max(attempted_samples, len(samples.get(region, ()))),
        )
        for region in all_regions
    )
    hint_index = {region: index for index, region in enumerate(all_regions)}
    usable = [
        measurement
        for measurement in measurements
        if measurement.successful_samples >= REGION_PROBE_MIN_SUCCESSES
        and measurement.median_ms is not None
    ]
    usable.sort(
        key=lambda measurement: (
            measurement.median_ms,
            hint_index[measurement.region],
        )
    )
    unusable = [measurement for measurement in measurements if measurement not in usable]
    if not usable:
        status: ProbeStatus = "failed"
        # No region met the minimum evidence threshold. Preserve the individual
        # measurements for diagnostics, but do not mislabel candidate order as
        # a measured latency ranking.
        ranked: tuple[str, ...] = ()
    elif len(usable) != len(measurements):
        status = "degraded"
        ranked = tuple(measurement.region for measurement in (*usable, *unusable))
    else:
        status = "ok"
        ranked = tuple(measurement.region for measurement in usable)
    confident_winner = _confident_winner(usable)
    return RegionProbeResult(
        order=ranked,
        measurements=measurements,
        status=status,
        confident_winner=confident_winner,
    )


def _measurement(
    region: str,
    samples: Sequence[float],
    *,
    attempted_samples: int,
) -> RegionMeasurement:
    values = [float(sample) for sample in samples]
    if not values:
        return RegionMeasurement(region, None, None, 0, attempted_samples)
    median_ms = statistics.median(values)
    raw_mad = statistics.median(abs(sample - median_ms) for sample in values)
    return RegionMeasurement(
        region=region,
        median_ms=round(median_ms, 3),
        mad_ms=round(1.4826 * raw_mad, 3),
        successful_samples=len(values),
        attempted_samples=attempted_samples,
    )


def _confidence_margin(measurement: RegionMeasurement) -> float:
    assert measurement.median_ms is not None
    return max(
        5.0,
        measurement.median_ms * 0.05,
        (measurement.mad_ms or 0.0) * 2.0,
    )


def _confident_winner(measurements: Sequence[RegionMeasurement]) -> str | None:
    if not measurements:
        return None
    first = measurements[0]
    if len(measurements) == 1:
        return first.region
    second = measurements[1]
    assert first.median_ms is not None and second.median_ms is not None
    if first.median_ms + _confidence_margin(first) < second.median_ms - _confidence_margin(second):
        return first.region
    return None


def _failed_probe_result() -> RegionProbeResult:
    return RegionProbeResult((), (), "failed", None)


async def _probe_once(
    client: httpx.AsyncClient,
    region: str,
    url: str,
    *,
    clock: Callable[[], float] = time.perf_counter,
) -> tuple[str, float] | None:
    started = clock()
    try:
        response = await client.get(url)
    except Exception:
        return None
    if response.status_code < 200 or response.status_code >= 400:
        return None
    return region, (clock() - started) * 1000.0


async def _create_session(
    control: Any,
    model: str,
    *,
    region_mode: str,
    provider: str | None,
    speed: str | None = None,
    preferred_region: str | None = None,
    region_pin: bool = False,
    idle_timeout: int | None = None,
    keep_warm: int = 0,
    optimization_config: OptimizationConfig | dict[str, Any] | None = None,
    probe_result: RegionProbeResult | None = None,
    checkpoint: str | None = None,
) -> Any:
    kwargs: dict[str, Any] = {
        "region_mode": region_mode,
        "preferred_region": preferred_region,
        "region_pin": region_pin,
        "idle_timeout": idle_timeout,
    }
    if provider is not None:
        kwargs["provider"] = provider
    if speed == "fast":
        kwargs["speed"] = speed
    if keep_warm:
        kwargs["keep_warm"] = keep_warm
    if checkpoint is not None:
        kwargs["checkpoint"] = checkpoint
    if optimization_config is not None:
        kwargs["optimization_config"] = optimization_config
    if probe_result is not None:
        kwargs["region_probe_status"] = probe_result.status
        kwargs["region_measurements"] = [
            measurement.to_wire() for measurement in probe_result.measurements
        ]
        if probe_result.order:
            kwargs["region_order"] = list(probe_result.order)
            kwargs["region_order_source"] = REGION_ORDER_SOURCE
            if probe_result.confident_winner is not None:
                kwargs["region_probe_confident_winner"] = probe_result.confident_winner
    accepted = _accepted_kwargs(control.create_session, kwargs)
    if provider is not None and "provider" not in accepted:
        raise RuntimeError("control-plane client does not support provider selection")
    if speed == "fast" and "speed" not in accepted:
        raise RuntimeError('control-plane client does not support speed="fast"')
    return await control.create_session(model, **accepted)


# The providers a request may name for each model, and the Modal regions a provider="modal"
# request may name (their catalog entries' ``client.providers`` and ``modal_regions``).
_PROVIDERS = {entry.id: entry.client.providers for entry in catalog.CATALOG}
_MODAL_REGIONS = {entry.id: entry.client.modal_regions for entry in catalog.CATALOG}
# Modal-only US-West endpoints, checked before the sets above, by the name they're refused by
# (their catalog entries' ``client.modal_only``). The π0.5 train-time-RTC runtime replaced
# pi05-yam's AWS route.
_MODAL_ONLY_MODELS = {
    entry.id: entry.client.modal_only for entry in catalog.CATALOG if entry.client.modal_only
}
# Models offering speed="fast" (a dedicated H100 route at its own price): their catalog
# entries' ``client.fast``.
FAST_MODELS = frozenset(entry.id for entry in catalog.CATALOG if entry.client.fast)
# What "served from us-west-2" accepts: automatic choice, availability, or US West by name.
_US_WEST_OK = (None, "auto", "nearest", "available", "us-west-2", "us-west")


def validate_speed_selection(
    model: str, speed: str | None, provider: str | None, region: str | None
) -> str | None:
    """Validate speed and return the region to request (fast defaults to available)."""
    if speed in (None, "standard"):
        return region
    if speed != "fast":
        raise ValueError('speed must be "standard" or "fast"')
    if model not in FAST_MODELS:
        raise ValueError(f'speed="fast" is not available for {public_model(model)}')
    if provider == "aws":
        raise ValueError('speed="fast" runs on Modal H100; omit provider or use provider="modal"')
    if region in (None, "auto", "nearest"):
        return "available"
    if region not in ("available", "us-west-2", "us-west"):
        raise ValueError('speed="fast" is served from us-west-2; use region="available"')
    return region


def validate_provider_selection(model: str, provider: str | None, region: str | None) -> None:
    from dreamscale.policy.runtime import served

    # A model's wire may settle its placement itself (policy.runtime.served: ``placement``).
    placement = served.hook(model, "placement")
    if placement is not None and placement(model, provider, region):
        return
    if model in _MODAL_ONLY_MODELS:
        name = _MODAL_ONLY_MODELS[model]
        if provider not in (None, "modal"):
            raise ValueError(f"{name} runs on Modal; omit provider or use provider='modal'")
        if region not in _US_WEST_OK:
            raise ValueError(f"{name} is served from us-west-2")
        return
    if provider is None:
        return
    if provider not in _PROVIDERS.get(model, ()):
        raise ValueError("provider selection requires a qualified aws/modal model")
    if provider == "modal":
        allowed = _MODAL_REGIONS[model]
        if _WIRE_NAMES.get(str(region), region) not in allowed:
            raise ValueError(
                f"Modal region for {public_model(model)} must be one of {', '.join(allowed)}"
            )


def pins_region(requested: str | None, served: str | None) -> bool:
    """Whether a session served in ``served`` honours the region asked for: any region for
    ``auto``/``available``, else that region by either name (``us-west`` or ``us-west-2``)."""
    if requested is None or requested.strip().lower() in _REGION_MODES:
        return True
    wanted = requested.strip().lower()
    return served in (wanted, _WIRE_NAMES.get(wanted, wanted))


def validate_region(region: RegionPreference | None) -> str:
    """``auto`` (``nearest``), ``available`` or a well-formed region id, lowercased; the
    control plane decides whether it runs there. Raises ValueError otherwise."""
    return _validate_region_preference(region)


def _validate_region_preference(region: RegionPreference | None) -> str:
    """``nearest`` for ``auto`` (the same request), ``available``, or a region id."""
    if region is None:
        return "nearest"
    if isinstance(region, str):
        value = region.strip().lower()
        if value in _REGION_MODES or _REGION_ID.match(value):
            return "nearest" if value == "auto" else value
    raise ValueError(
        "region must be one of auto, available or a region id such as us-west "
        f"(GET /v1/regions lists them), not {region!r}"
    )


def _accepted_kwargs(fn: Callable[..., Any], kwargs: dict[str, Any]) -> dict[str, Any]:
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return kwargs
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in params.values()):
        return kwargs
    return {key: value for key, value in kwargs.items() if key in params}
