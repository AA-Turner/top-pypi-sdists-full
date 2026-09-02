from __future__ import annotations

import asyncio
import time
from collections import deque
from dataclasses import dataclass
from types import TracebackType
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError, classify_provider_error


@dataclass(frozen=True, slots=True)
class ProviderAdmissionPolicy:
    initial_concurrency: int = 32
    max_concurrency: int = 512
    requests_per_minute: int | None = None


class _ProviderAdmissionState:
    def __init__(self, policy: ProviderAdmissionPolicy) -> None:
        self.policy = policy
        self.current_concurrency = policy.initial_concurrency
        self.active = 0
        self.cooldown_until = 0.0
        self.successes_since_increase = 0
        self.starts: deque[float] = deque()
        self.condition = asyncio.Condition()

    async def acquire(self) -> None:
        async with self.condition:
            while True:
                now = time.monotonic()
                while self.starts and self.starts[0] <= now - 60.0:
                    self.starts.popleft()

                rpm_available = (
                    self.policy.requests_per_minute is None
                    or len(self.starts) < self.policy.requests_per_minute
                )
                if (
                    now >= self.cooldown_until
                    and self.active < self.current_concurrency
                    and rpm_available
                ):
                    self.active += 1
                    self.starts.append(now)
                    return

                waits: list[float] = []
                if now < self.cooldown_until:
                    waits.append(self.cooldown_until - now)
                if not rpm_available and self.starts:
                    waits.append(max(0.001, self.starts[0] + 60.0 - now))

                if waits:
                    try:
                        await asyncio.wait_for(self.condition.wait(), timeout=min(waits))
                    except TimeoutError:
                        pass
                else:
                    await self.condition.wait()

    async def release(self, error: RetryableError | None, *, succeeded: bool) -> None:
        async with self.condition:
            self.active = max(0, self.active - 1)
            if error is not None and error.error_type == "rate_limit":
                previous = self.current_concurrency
                self.current_concurrency = max(1, self.current_concurrency // 2)
                self.cooldown_until = max(
                    self.cooldown_until,
                    time.monotonic() + max(0.0, error.retry_after or 10.0),
                )
                self.successes_since_increase = 0
                vcprint(
                    {
                        "previous_concurrency": previous,
                        "new_concurrency": self.current_concurrency,
                        "retry_after_seconds": error.retry_after or 10.0,
                    },
                    title="PROVIDER ADMISSION THROTTLED",
                    color="yellow",
                )
            elif succeeded:
                self.successes_since_increase += 1
                if (
                    self.successes_since_increase >= self.current_concurrency
                    and self.current_concurrency < self.policy.max_concurrency
                ):
                    self.current_concurrency += 1
                    self.successes_since_increase = 0
            self.condition.notify_all()


_states: dict[str, _ProviderAdmissionState] = {}
_states_lock = asyncio.Lock()


def _positive_int(value: Any, fallback: int | None) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return fallback
    return value


def policy_from_profile(profile: Any) -> ProviderAdmissionPolicy:
    metadata = getattr(profile, "offering_metadata", None)
    raw = metadata.get("provider_admission") if isinstance(metadata, dict) else None
    if not isinstance(raw, dict):
        raw = {}

    initial = _positive_int(raw.get("initial_concurrency"), 32) or 32
    maximum = _positive_int(raw.get("max_concurrency"), 512) or 512
    maximum = max(initial, maximum)
    rpm = _positive_int(raw.get("requests_per_minute"), None)
    return ProviderAdmissionPolicy(
        initial_concurrency=initial,
        max_concurrency=maximum,
        requests_per_minute=rpm,
    )


def admission_key(profile: Any) -> str:
    endpoint_id = str(getattr(profile, "endpoint_id", "") or "")
    vendor = str(getattr(profile, "vendor", "unknown") or "unknown").lower()
    base_url = str(getattr(profile, "base_url", "") or "")
    return f"{vendor}:{endpoint_id}:{base_url}"


async def _state_for(profile: Any) -> _ProviderAdmissionState:
    key = admission_key(profile)
    async with _states_lock:
        state = _states.get(key)
        if state is None:
            state = _ProviderAdmissionState(policy_from_profile(profile))
            _states[key] = state
        return state


def _rate_limit_error(profile: Any, exc: BaseException | None) -> RetryableError | None:
    if exc is None or isinstance(exc, asyncio.CancelledError):
        return None
    attached = getattr(exc, "error_info", None)
    if isinstance(attached, RetryableError):
        return attached if attached.error_type == "rate_limit" else None
    if not isinstance(exc, Exception):
        return None
    vendor = str(getattr(profile, "vendor", "provider") or "provider")
    classified = classify_provider_error(vendor, exc)
    return classified if classified.error_type == "rate_limit" else None


class ProviderAdmission:
    def __init__(self, profile: Any) -> None:
        self.profile = profile
        self.state: _ProviderAdmissionState | None = None

    async def __aenter__(self) -> ProviderAdmission:
        self.state = await _state_for(self.profile)
        await self.state.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self.state is not None:
            await self.state.release(_rate_limit_error(self.profile, exc), succeeded=exc is None)
        return False


def admit_provider_call(profile: Any) -> ProviderAdmission:
    return ProviderAdmission(profile)


def reset_provider_admission_for_tests() -> None:
    _states.clear()


def provider_admission_snapshot() -> dict[str, dict[str, int | float | None]]:
    return {
        key: {
            "active": state.active,
            "current_concurrency": state.current_concurrency,
            "max_concurrency": state.policy.max_concurrency,
            "requests_per_minute": state.policy.requests_per_minute,
            "cooldown_seconds": max(0.0, state.cooldown_until - time.monotonic()),
            "starts_in_window": len(state.starts),
        }
        for key, state in _states.items()
    }
