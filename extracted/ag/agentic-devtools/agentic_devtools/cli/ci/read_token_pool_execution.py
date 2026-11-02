"""Deadline-aware execution for pooled GitHub read requests."""

from __future__ import annotations

import time
from collections import deque
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from math import floor, isfinite
from typing import Any

from agentic_devtools.cli.ci.read_token_pool import ReadTokenPool, _ReadTokenPoolDeadlineExceeded
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.shared.retry import (
    DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
    DEFAULT_RATE_LIMIT_MAX_DELAY,
    DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
    calculate_rate_limit_delay,
)

_REQUEST_CONTEXT: ContextVar[tuple[float | None, Callable[[], float] | None]] = ContextVar(
    "github_read_pool_request_context",
    default=(None, None),
)
_DEFERRED_RATE_LIMIT_PERSISTENCE: deque[Callable[[], float | None]] = deque()
_RETAINED_RATE_LIMITS: dict[tuple[str, str], float] = {}


class ReadTokenPoolRateLimits:
    """Persist retained and deferred read-pool rate limits."""

    @staticmethod
    def persist_rate_limit(
        provider: Any,
        identity: str,
        error: RetryableError | ProviderRateLimitError,
        *,
        bypass: ContextVar[bool],
        observed_at: float | None = None,
    ) -> float | None:
        deadline, _ = _REQUEST_CONTEXT.get()
        if deadline is not None:
            observed_at = time.time()
            _DEFERRED_RATE_LIMIT_PERSISTENCE.append(
                lambda: ReadTokenPoolRateLimits.persist_rate_limit(
                    provider,
                    identity,
                    error,
                    bypass=bypass,
                    observed_at=observed_at,
                )
            )
            retry_after = error.retry_after if isinstance(error, RetryableError) else error.retry_after_seconds
            resume_at = calculate_rate_limit_delay(
                retry_after_seconds=retry_after,
                reset_timestamp=error.reset_timestamp,
                now=observed_at,
                fallback_delay=DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
                safety_margin=DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
                max_delay=DEFAULT_RATE_LIMIT_MAX_DELAY,
            ).resume_at
            active = ReadTokenPoolRateLimits.merge_cooldowns(provider._repo, {identity: resume_at})
            retained_resume_at = active[identity]
            if isinstance(retained_resume_at, float) and isfinite(retained_resume_at):
                _RETAINED_RATE_LIMITS[(provider._repo, identity)] = retained_resume_at
            return resume_at

        from agentic_devtools.cli.ci.cooldown import persist_cooldown

        retry_after = error.retry_after if isinstance(error, RetryableError) else error.retry_after_seconds
        token = bypass.set(True)
        try:
            persisted = persist_cooldown(
                provider,
                ProviderRateLimitError(
                    retry_after_seconds=retry_after,
                    reset_timestamp=error.reset_timestamp,
                    remaining=error.remaining,
                    provider=error.provider or "github",
                    credential_identity=identity,
                    source=error.source,
                    is_rate_limit=error.is_rate_limit,
                ),
                observed_at=observed_at,
            )
            return persisted[1].resume_at if persisted is not None else None
        finally:
            bypass.reset(token)

    @staticmethod
    def merge_cooldowns(repo: str, cooldowns: dict[str, float | None]) -> dict[str, float | None]:
        """Merge retained repository cooldowns without extending their absolute deadlines."""
        now = time.time()
        for key, resume_at in list(_RETAINED_RATE_LIMITS.items()):
            if resume_at <= now:
                del _RETAINED_RATE_LIMITS[key]
            elif key[0] == repo:
                identity = key[1]
                if identity not in cooldowns:
                    cooldowns[identity] = resume_at
                else:
                    existing_resume_at = cooldowns[identity]
                    if isinstance(existing_resume_at, float) and isfinite(existing_resume_at):
                        cooldowns[identity] = max(resume_at, existing_resume_at)
        return cooldowns

    @staticmethod
    def flush_deferred_rate_limits() -> None:
        if _REQUEST_CONTEXT.get()[0] is not None:
            return
        while True:
            try:
                persist = _DEFERRED_RATE_LIMIT_PERSISTENCE.popleft()
            except IndexError:
                return
            try:
                persist()
            except Exception:
                _DEFERRED_RATE_LIMIT_PERSISTENCE.appendleft(persist)
                raise


class ReadTokenPoolOperations:
    """Execute pooled requests while optionally enforcing an inventory deadline."""

    DeadlineExpired = _ReadTokenPoolDeadlineExceeded

    @staticmethod
    @contextmanager
    def request_context(deadline: float | None, monotonic: Callable[[], float] | None) -> Iterator[None]:
        token = _REQUEST_CONTEXT.set((deadline, monotonic))
        try:
            yield
        finally:
            _REQUEST_CONTEXT.reset(token)

    @staticmethod
    def current_request_context() -> tuple[float | None, Callable[[], float] | None]:
        return _REQUEST_CONTEXT.get()

    @staticmethod
    def resolve_request_context(
        deadline: float | None,
        monotonic: Callable[[], float] | None,
    ) -> tuple[float | None, Callable[[], float] | None]:
        request_deadline, request_monotonic = _REQUEST_CONTEXT.get()
        return (
            deadline if deadline is not None else request_deadline,
            monotonic if monotonic is not None else request_monotonic,
        )

    @staticmethod
    def run_request[Result](
        request: Callable[[], Result],
        *,
        deadline: float | None,
        monotonic: Callable[[], float] | None,
    ) -> Result:
        try:
            return request()
        except RetryableError:
            if deadline is not None:
                ReadTokenPoolOperations.request_timeout(1, deadline, monotonic)
            raise

    @staticmethod
    def check_http_error_deadline(
        deadline: float | None,
        monotonic: Callable[[], float] | None,
        *,
        pool_managed: bool,
        is_rate_limit: bool,
    ) -> None:
        if pool_managed and is_rate_limit:
            return
        ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)

    @staticmethod
    def _run_without_pool[ReadResult](
        operation: Callable[[str | None, str], tuple[ReadResult, int | None]],
        identity_for_token: Callable[[str | None], str],
        deadline: float | None,
        monotonic: Callable[[], float] | None,
    ) -> ReadResult:
        try:
            result, _ = operation(None, identity_for_token(None))
            return result
        except RetryableError:
            ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
            raise

    @staticmethod
    def remaining_seconds(
        deadline: float | None,
        monotonic: Callable[[], float] | None,
    ) -> float | None:
        if deadline is None:
            return None
        remaining = deadline - (monotonic or time.monotonic)()
        if remaining <= 0:
            raise ReadTokenPoolOperations.DeadlineExpired("GitHub API inventory deadline expired")
        return remaining

    @staticmethod
    def request_timeout(
        timeout_seconds: int,
        deadline: float | None,
        monotonic: Callable[[], float] | None,
    ) -> int:
        remaining = ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
        if remaining is None:
            return timeout_seconds
        timeout = min(timeout_seconds, floor(remaining))
        if timeout < 1:
            raise ReadTokenPoolOperations.DeadlineExpired("GitHub API inventory deadline expired")
        return timeout

    @staticmethod
    def run[ReadResult](
        resource: str,
        operation: Callable[[str | None, str], tuple[ReadResult, int | None]],
        pool: ReadTokenPool | None,
        identity_for_token: Callable[[str | None], str],
        *,
        deadline: float | None = None,
        monotonic: Callable[[], float] | None = None,
    ) -> ReadResult:
        if pool is None:
            return ReadTokenPoolOperations._run_without_pool(operation, identity_for_token, deadline, monotonic)

        attempted: set[str] = set()
        last_rate_limit: RetryableError | None = None
        while True:
            ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
            credential = pool.select(resource, excluded=attempted)
            ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
            if credential is None:
                break
            attempted.add(credential.secret_name)
            try:
                result, remaining = operation(credential.token, credential.secret_name)
            except RetryableError as exc:
                if not exc.is_rate_limit:
                    ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
                    raise
                pool.record_remaining(credential.secret_name, resource, exc.remaining)
                pool.mark_rate_limited(credential.secret_name, exc)
                ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
                last_rate_limit = exc
                continue
            pool.record_remaining(credential.secret_name, resource, remaining)
            return result

        if last_rate_limit is not None and not pool.default_token:
            raise ProviderRateLimitError(
                retry_after_seconds=last_rate_limit.retry_after,
                reset_timestamp=last_rate_limit.reset_timestamp,
                remaining=last_rate_limit.remaining,
                provider=last_rate_limit.provider or "github",
                credential_identity=last_rate_limit.credential_identity,
                source=last_rate_limit.source,
                is_rate_limit=True,
            )
        default_is_active = pool.default_is_active
        ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
        if default_is_active:
            raise ProviderRateLimitError(
                provider="github",
                credential_identity=pool.default_identity,
                source="fallback",
                is_rate_limit=True,
            )
        ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
        try:
            result, remaining = operation(pool.default_token or None, pool.default_identity)
        except RetryableError as exc:
            if not exc.is_rate_limit:
                ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
                raise
            pool.record_remaining(pool.default_identity, resource, exc.remaining)
            pool.mark_rate_limited(pool.default_identity, exc)
            ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
            raise ProviderRateLimitError(
                retry_after_seconds=exc.retry_after,
                reset_timestamp=exc.reset_timestamp,
                remaining=exc.remaining,
                provider=exc.provider or "github",
                credential_identity=pool.default_identity,
                source=exc.source,
                is_rate_limit=True,
            ) from exc
        pool.record_remaining(pool.default_identity, resource, remaining)
        return result


def _read_cooldown_value(provider: Any, *, use_writer_token: bool) -> str | None:
    """Read cooldown data without nested retries when an inventory deadline is active."""
    deadline, monotonic = _REQUEST_CONTEXT.get()
    getter = provider.get_variable
    if deadline is not None:
        function = getattr(getter, "__func__", getter)
        original = getattr(function, "__wrapped__", None)
        if original is not None:
            getter = original.__get__(provider, type(provider))
    try:
        from agentic_devtools.cli.ci.cooldown import COOLDOWN_VARIABLE

        return getter(COOLDOWN_VARIABLE, use_writer_token=use_writer_token)
    except RetryableError as exc:
        if deadline is None:
            raise
        ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
        if exc.is_rate_limit:
            raise ProviderRateLimitError(
                retry_after_seconds=exc.retry_after,
                reset_timestamp=exc.reset_timestamp,
                remaining=exc.remaining,
                provider=exc.provider,
                credential_identity=exc.credential_identity,
                source=exc.source,
                is_rate_limit=True,
            ) from exc
        raise
    except Exception:
        if deadline is not None:
            ReadTokenPoolOperations.remaining_seconds(deadline, monotonic)
        raise
