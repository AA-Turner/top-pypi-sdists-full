"""ConfigProvider ABC + HttpEtag smart-poll impl + ResolvedConfig + AutonomousConfig.

EnvOverrides: apply_env_overrides(cfg) zeroes enabled when AIGIE_AUTONOMOUS_DISABLE=1.
Compose with HttpEtagConfigProvider by calling apply_env_overrides on resolved.autonomous
before handing it to downstream consumers.

No imports from any other aigie.autonomous.* module. No _pb imports.
"""

from __future__ import annotations

import abc
import logging
import os
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import httpx

import aigie.telemetry as _telemetry

if TYPE_CHECKING:
    from aigie.autonomous.flows import Flow

logger = logging.getLogger(__name__)

tracer = _telemetry.get_tracer("aigie.autonomous")

_CONFIG_PATH = "/v1/sdk/config"
_DEFAULT_POLL_SECONDS = 30.0
_BACKOFF_INITIAL = 2.0
_BACKOFF_MAX = 60.0


# ---------------------------------------------------------------------------
# AutonomousConfig — mirrors KytteAutonomousConfig.spec from ADR 0001
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BlastRadiusThresholds:
    next_step_min_confidence: float = 0.0
    trajectory_min_confidence: float = 0.0
    trajectory_min_prior_successes: int = 0


@dataclass(frozen=True)
class BlastRadiusConfig:
    max: int = 0
    thresholds: BlastRadiusThresholds = field(default_factory=BlastRadiusThresholds)


@dataclass(frozen=True)
class LatencyConfig:
    reflex_budget_ms: int = 0
    judge_wait_ms: int = 0


@dataclass(frozen=True)
class JudgeConfig:
    model_override: str = ""


@dataclass(frozen=True)
class ReconnectConfig:
    initial_backoff_ms: int = 500
    max_backoff_ms: int = 30000


@dataclass(frozen=True)
class PlatformConfig:
    endpoint: str = ""
    api_key_secret: str = ""
    reconnect: ReconnectConfig = field(default_factory=ReconnectConfig)


@dataclass(frozen=True)
class ObservabilityConfig:
    log_level: str = "INFO"
    emit_directive_decisions: bool = False


@dataclass(frozen=True)
class AutonomousConfig:
    enabled: bool = False
    kill_switch: bool = False
    blast_radius: BlastRadiusConfig = field(default_factory=BlastRadiusConfig)
    latency: LatencyConfig = field(default_factory=LatencyConfig)
    judge: JudgeConfig = field(default_factory=JudgeConfig)
    platform: PlatformConfig = field(default_factory=PlatformConfig)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)


# ---------------------------------------------------------------------------
# ResolvedConfig — full envelope from the server
# ---------------------------------------------------------------------------


@dataclass
class ResolvedConfig:
    version: str
    raw: dict

    def section(self, name: str) -> dict | None:
        """Return raw section payload or None if missing."""
        val = self.raw.get(name)
        return val if isinstance(val, dict) else None

    @property
    def autonomous(self) -> AutonomousConfig | None:
        """Typed convenience: parses raw["autonomous"]["config"] into AutonomousConfig."""
        sec = self.section("autonomous")
        if sec is None:
            return None
        cfg = sec.get("config")
        if not isinstance(cfg, dict):
            return None
        return _parse_autonomous_config(cfg)

    def universal_rules(self) -> list[dict]:
        """Raw universal rule dicts from raw["autonomous"]["universal_rules"]."""
        sec = self.section("autonomous") or {}
        rules = sec.get("universal_rules", [])
        return rules if isinstance(rules, list) else []

    def workflow_rules(self) -> list[dict]:
        """Raw workflow rule dicts from raw["autonomous"]["workflow_rules"]."""
        sec = self.section("autonomous") or {}
        rules = sec.get("workflow_rules", [])
        return rules if isinstance(rules, list) else []

    def flows_raw(self) -> list[dict]:
        """Raw RemediationFlow dicts from the new envelope shape.

        Accepts either top-level ``raw["flows"]`` (per the autonomous-v2 plan)
        or nested ``raw["autonomous"]["flows"]`` while the platform endpoint
        is behind a feature flag and may dual-emit.
        """
        top = self.raw.get("flows")
        if isinstance(top, list):
            return top
        sec = self.section("autonomous") or {}
        nested = sec.get("flows", [])
        return nested if isinstance(nested, list) else []

    def flows(self) -> list[Flow]:
        """Parsed Flow dataclasses from the envelope. Malformed rows skipped."""
        from aigie.autonomous.flows import parse_flows

        return parse_flows(self.flows_raw())


_SENTINEL = ResolvedConfig(version="", raw={})


# ---------------------------------------------------------------------------
# Parsing helpers (keep each function ≤ 20 statements)
# ---------------------------------------------------------------------------


def _parse_blast_radius_thresholds(d: dict) -> BlastRadiusThresholds:
    return BlastRadiusThresholds(
        next_step_min_confidence=float(d.get("nextStepMinConfidence", 0.0)),
        trajectory_min_confidence=float(d.get("trajectoryMinConfidence", 0.0)),
        trajectory_min_prior_successes=int(d.get("trajectoryMinPriorSuccesses", 0)),
    )


_TIER_NAME_TO_INT = {"instep": 0, "nextstep": 1, "trajectory": 2}


def _coerce_max_tier(raw: Any) -> int:
    """Accept either int (0/1/2) or string ("InStep"/"NextStep"/"Trajectory")."""
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        return _TIER_NAME_TO_INT.get(raw.strip().lower(), 0)
    return 0


def _parse_blast_radius(d: dict) -> BlastRadiusConfig:
    thresh_raw = d.get("thresholds", {})
    thresholds = _parse_blast_radius_thresholds(thresh_raw if isinstance(thresh_raw, dict) else {})
    return BlastRadiusConfig(max=_coerce_max_tier(d.get("max", 0)), thresholds=thresholds)


def _parse_reconnect(d: dict) -> ReconnectConfig:
    return ReconnectConfig(
        initial_backoff_ms=int(d.get("initialBackoffMs", 500)),
        max_backoff_ms=int(d.get("maxBackoffMs", 30000)),
    )


def _parse_platform(d: dict) -> PlatformConfig:
    reconnect_raw = d.get("reconnect", {})
    reconnect = _parse_reconnect(reconnect_raw if isinstance(reconnect_raw, dict) else {})
    return PlatformConfig(
        endpoint=str(d.get("endpoint", "")),
        api_key_secret=str(d.get("apiKeySecret", "")),
        reconnect=reconnect,
    )


def _parse_autonomous_config(d: dict) -> AutonomousConfig:
    br_raw = d.get("blastRadius", {})
    lat_raw = d.get("latency", {})
    judge_raw = d.get("judge", {})
    plat_raw = d.get("platform", {})
    obs_raw = d.get("observability", {})
    return AutonomousConfig(
        enabled=bool(d.get("enabled", False)),
        kill_switch=bool(d.get("killSwitch", False)),
        blast_radius=_parse_blast_radius(br_raw if isinstance(br_raw, dict) else {}),
        latency=LatencyConfig(
            reflex_budget_ms=int(
                lat_raw.get("reflexBudgetMs", 0) if isinstance(lat_raw, dict) else 0
            ),
            judge_wait_ms=int(lat_raw.get("judgeWaitMs", 0) if isinstance(lat_raw, dict) else 0),
        ),
        judge=JudgeConfig(
            model_override=str(
                judge_raw.get("modelOverride", "") if isinstance(judge_raw, dict) else ""
            )
        ),
        platform=_parse_platform(plat_raw if isinstance(plat_raw, dict) else {}),
        observability=ObservabilityConfig(
            log_level=str(obs_raw.get("logLevel", "INFO") if isinstance(obs_raw, dict) else "INFO"),
            emit_directive_decisions=bool(
                obs_raw.get("emitDirectiveDecisions", False) if isinstance(obs_raw, dict) else False
            ),
        ),
    )


# ---------------------------------------------------------------------------
# ConfigProvider ABC
# ---------------------------------------------------------------------------


class ConfigProvider(abc.ABC):
    """Abstract config provider. Implementations must be thread-safe."""

    @abc.abstractmethod
    def start(self) -> None:
        """Begin background polling / watching. Idempotent."""

    @abc.abstractmethod
    def stop(self) -> None:
        """Signal background activity to stop. Blocks up to provider-defined timeout."""

    @abc.abstractmethod
    def get(self) -> ResolvedConfig:
        """Return the latest resolved config. Never raises; returns sentinel if not yet fetched."""

    @abc.abstractmethod
    def subscribe(self, callback: Callable[[ResolvedConfig], None]) -> None:
        """Register callback fired on every config change (new ETag). Thread-safe."""


# ---------------------------------------------------------------------------
# HttpEtagConfigProvider
# ---------------------------------------------------------------------------


class HttpEtagConfigProvider(ConfigProvider):
    """Polls /v1/sdk/config with If-None-Match; smart-poll via ETag.

    304 = no-op; 200 = parse + notify subscribers; 5xx = exponential backoff
    + retain last-good config. Never raises during start().
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str | None = None,
        poll_interval_seconds: float = _DEFAULT_POLL_SECONDS,
        http_client: httpx.Client | None = None,
    ) -> None:
        env_interval = os.environ.get("AIGIE_CONFIG_POLL_INTERVAL_SECONDS")
        self._poll_interval = float(env_interval) if env_interval else poll_interval_seconds
        self._url = endpoint.rstrip("/") + _CONFIG_PATH
        self._api_key = api_key
        self._own_client = http_client is None
        self._client = http_client or httpx.Client(timeout=10.0)
        self._resolved: ResolvedConfig = _SENTINEL
        self._etag: str | None = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._subscribers: list[Callable[[ResolvedConfig], None]] = []
        self._thread: threading.Thread | None = None

    def subscribe(self, callback: Callable[[ResolvedConfig], None]) -> None:
        with self._lock:
            self._subscribers.append(callback)

    def get(self) -> ResolvedConfig:
        with self._lock:
            return self._resolved

    def start(self) -> None:
        """Spawn daemon poll thread. Best-effort initial fetch; never raises."""
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._poll_loop,
            name="aigie-config-poll",
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        """Signal poll thread to exit; join with 5s timeout."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=5.0)
        if self._own_client:
            self._client.close()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self._api_key:
            # Backend uses APIKeyHeader(name="X-API-Key") for auth — matches
            # every other Aigie HTTP call site (client.py, signals.py, datasets.py).
            headers["X-API-Key"] = self._api_key
        if self._etag:
            headers["If-None-Match"] = self._etag
        return headers

    def _notify_subscribers(self, cfg: ResolvedConfig) -> None:
        with self._lock:
            subs = list(self._subscribers)
        for cb in subs:
            try:
                cb(cfg)
            except Exception:
                logger.exception("Config subscriber raised an exception")

    def _apply_update(self, response: httpx.Response) -> None:
        """Parse 200 response and notify subscribers if ETag changed."""
        new_etag = response.headers.get("ETag", "")
        try:
            body = response.json()
        except Exception:
            logger.warning("Config response body is not valid JSON; retaining last-good config")
            return
        version = new_etag or body.get("version", "")
        resolved = ResolvedConfig(version=version, raw=body)
        with self._lock:
            self._resolved = resolved
            self._etag = new_etag
        self._notify_subscribers(resolved)

    def _fetch_once(self) -> float:
        """Fetch config once. Returns next sleep interval in seconds."""
        with tracer.start_as_current_span("config.fetch") as span:
            return self._fetch_once_inner(span)

    def _fetch_once_inner(self, span: object) -> float:
        headers = self._build_headers()
        span.set_attribute("etag", self._etag or "")  # type: ignore[union-attr]
        t0 = time.monotonic()
        try:
            response = self._client.get(self._url, headers=headers)
        except Exception:
            logger.warning("Config fetch failed (network error); retaining last-good config")
            span.set_attribute("http_status", 0)  # type: ignore[union-attr]
            span.set_attribute("changed", False)  # type: ignore[union-attr]
            span.set_attribute("duration_ms", int((time.monotonic() - t0) * 1000))  # type: ignore[union-attr]
            return self._poll_interval
        duration_ms = int((time.monotonic() - t0) * 1000)
        span.set_attribute("http_status", response.status_code)  # type: ignore[union-attr]
        span.set_attribute("duration_ms", duration_ms)  # type: ignore[union-attr]
        if response.status_code == 304:
            span.set_attribute("changed", False)  # type: ignore[union-attr]
            return self._poll_interval
        if response.status_code == 200:
            old_etag = self._etag
            self._apply_update(response)
            changed = self._etag != old_etag
            span.set_attribute("changed", changed)  # type: ignore[union-attr]
            span.set_attribute("sections", str(list(self._resolved.raw.keys())))  # type: ignore[union-attr]
            return self._poll_interval
        if response.status_code >= 500:
            span.set_attribute("changed", False)  # type: ignore[union-attr]
            return self._poll_interval  # caller handles backoff
        logger.warning("Config endpoint returned %s; retaining last-good", response.status_code)
        span.set_attribute("changed", False)  # type: ignore[union-attr]
        return self._poll_interval

    def _poll_loop(self) -> None:
        backoff = _BACKOFF_INITIAL
        while not self._stop_event.is_set():
            headers = self._build_headers()
            try:
                response = self._client.get(self._url, headers=headers)
                ok = self._handle_response(response)
                backoff = _BACKOFF_INITIAL  # reset on any successful communication
            except Exception:
                ok = False
                logger.warning("Config fetch failed (network); retaining last-good config")
            sleep_secs = self._poll_interval if ok else min(backoff, _BACKOFF_MAX)
            if not ok:
                backoff = min(backoff * 2, _BACKOFF_MAX)
            self._stop_event.wait(timeout=sleep_secs)

    def _handle_response(self, response: httpx.Response) -> bool:
        """Process HTTP response. Returns True if no backoff needed."""
        if response.status_code == 304:
            return True
        if response.status_code == 200:
            self._apply_update(response)
            return True
        if response.status_code >= 500:
            logger.warning(
                "Config endpoint returned %s; retaining last-good config", response.status_code
            )
            return False
        logger.warning("Config endpoint returned unexpected %s", response.status_code)
        return True


# ---------------------------------------------------------------------------
# EnvOverrides
# ---------------------------------------------------------------------------


def apply_env_overrides(cfg: AutonomousConfig | None) -> AutonomousConfig | None:
    """Return cfg with enabled=False if AIGIE_AUTONOMOUS_DISABLE=1; else return unchanged.

    If cfg is None and the env var is set, returns a default AutonomousConfig with enabled=False.
    """
    if os.environ.get("AIGIE_AUTONOMOUS_DISABLE") == "1":
        if cfg is None:
            return AutonomousConfig(enabled=False)
        # frozen dataclass — reconstruct with enabled=False
        return AutonomousConfig(
            enabled=False,
            kill_switch=cfg.kill_switch,
            blast_radius=cfg.blast_radius,
            latency=cfg.latency,
            judge=cfg.judge,
            platform=cfg.platform,
            observability=cfg.observability,
        )
    return cfg
