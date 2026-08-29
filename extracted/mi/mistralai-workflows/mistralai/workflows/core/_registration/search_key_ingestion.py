"""Runtime search key ingestion for RFC-402 (V3).

Keys arrive at runtime, so unlike the V1 input path there is no startup validation to lean
on. Failures split three ways by whether a later attempt could succeed:

- Transient (5xx, 429, 408, no response): retried, then logged at warning and dropped.
- Permanent (any other status, unparseable body): logged at error and dropped. A server
  deploy can produce these fleet-wide mid-run, so they must not fail healthy executions;
  the error log is the alerting signal.
- Bugs (any other in-process exception): non-retryable, and they fail the execution. Only
  an SDK or caller change causes one, so it surfaces on the first run, not in production.

A local activity surfaces application failures bare, but timeouts and cancellation wrapped
in ActivityError, so the caller has to unwrap before classifying.

Both operations name the execution by its Temporal run id. The legacy execution token hash
is no longer sent: it never applied to deletes, and a server predating the run-id path
rejects the request, which the permanent-failure branch already degrades.

Values are stored UNENCRYPTED.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Awaitable, Callable, Mapping, Sequence
from contextlib import asynccontextmanager
from datetime import date, timedelta
from enum import Enum
from itertools import islice
from typing import NoReturn, TypeAlias, TypeVar
from uuid import UUID

import httpx
import structlog
import temporalio.activity
import temporalio.common
import temporalio.exceptions
import temporalio.workflow
import tenacity

from mistralai.workflows.core._registration.search_keys import (
    _RESERVED_KEY_PREFIX,
    _cap_value,
    _coerce_leaf,
)
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.config.config import (
    INTERNAL_ACTIVITY_PREFIX,
    MAX_SEARCH_KEY_CHARS,
    MAX_SEARCH_KEYS,
    config,
)
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.worker_client.errors.no_response_error import NoResponseError
from mistralai.workflows.worker_client.errors.responsevalidationerror import ResponseValidationError
from mistralai.workflows.worker_client.errors.sdkerror import SDKError
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

logger = structlog.get_logger(__name__)

UPSERT_SEARCH_KEYS_ACTIVITY_NAME = f"{INTERNAL_ACTIVITY_PREFIX}upsert_search_keys"
DELETE_SEARCH_KEYS_ACTIVITY_NAME = f"{INTERNAL_ACTIVITY_PREFIX}delete_search_keys"

SearchKeyValue: TypeAlias = str | int | float | bool | Enum | UUID | date | None

_Payload = TypeVar("_Payload", dict[str, str], list[str])

_CONTAINER_TYPES = (Mapping, list, tuple, set, frozenset)

_LOG_KEY_PREVIEW_CHARS = 64

# Retryable alongside 5xx; every other status the server answers with is permanent.
_RETRYABLE_STATUS_CODES = frozenset({408, 429})

# One budget for both dispatch branches and both operations, so they retry alike.
_MAX_REQUEST_ATTEMPTS = 3
_RETRY_BACKOFF_SECONDS = 0.2
_REQUEST_TIMEOUT_SECONDS = 10.0


def _raise_invalid(message: str) -> NoReturn:
    raise temporalio.exceptions.ApplicationError(message, non_retryable=True)


def _validate_key(key: object, allow_reserved: bool) -> bool:
    """Raise on a key the caller must fix; return False for one to drop silently."""
    if not isinstance(key, str):
        _raise_invalid(f"Search key must be a string, got {type(key).__name__}.")
    if not key or key != key.strip():
        _raise_invalid("Search key must not be empty or padded with whitespace.")
    if ":" in key:
        _raise_invalid(f"Search key `{key}` must not contain ':'.")
    if not allow_reserved and key.startswith(_RESERVED_KEY_PREFIX):
        _raise_invalid(f"Search key `{key}` must not start with `{_RESERVED_KEY_PREFIX}`, which the SDK reserves")
    if len(key) > MAX_SEARCH_KEY_CHARS:
        logger.warning(
            "Search key exceeded length cap; dropping",
            search_key=key[:_LOG_KEY_PREVIEW_CHARS],
            key_chars=len(key),
            max_chars=MAX_SEARCH_KEY_CHARS,
        )
        return False
    return True


def _validate_and_coerce(search_keys: Mapping[str, SearchKeyValue], allow_reserved: bool = False) -> dict[str, str]:
    if not isinstance(search_keys, Mapping):
        _raise_invalid(f"add_search_keys expects a mapping, got {type(search_keys).__name__}.")
    if len(search_keys) > MAX_SEARCH_KEYS:
        _raise_invalid(f"add_search_keys accepts at most {MAX_SEARCH_KEYS} keys per call, got {len(search_keys)}.")

    coerced: dict[str, str] = {}
    for key, value in search_keys.items():
        if isinstance(value, _CONTAINER_TYPES):
            _raise_invalid(f"Search key `{key}` must map to a scalar value, got {type(value).__name__}.")
        if not _validate_key(key, allow_reserved):
            continue
        if value is None:
            logger.debug("Search key value is None; skipping", search_key=key)
            continue
        coerced[key] = _cap_value(key, _coerce_leaf(value))
    return coerced


def _validate_keys(keys: Sequence[str], allow_reserved: bool = False) -> list[str]:
    # A bare string is a Sequence, so without this guard it would delete one key per character.
    if isinstance(keys, (str, bytes)) or not isinstance(keys, Sequence):
        _raise_invalid(f"delete_search_keys expects a list or tuple of keys, got {type(keys).__name__}.")
    if len(keys) > MAX_SEARCH_KEYS:
        _raise_invalid(f"delete_search_keys accepts at most {MAX_SEARCH_KEYS} keys per call, got {len(keys)}.")

    validated: dict[str, None] = {}
    for key in islice(keys, MAX_SEARCH_KEYS):
        if _validate_key(key, allow_reserved):
            validated[key] = None
    return list(validated)


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, NoResponseError):
        return True
    return isinstance(exc, SDKError) and (exc.status_code >= 500 or exc.status_code in _RETRYABLE_STATUS_CODES)


def _must_propagate(exc: BaseException) -> bool:
    inner = exc.cause if isinstance(exc, temporalio.exceptions.ActivityError) else exc
    if isinstance(inner, temporalio.exceptions.CancelledError):
        return True
    return isinstance(inner, temporalio.exceptions.ApplicationError) and inner.non_retryable


def _bug(exc: Exception, operation: str) -> temporalio.exceptions.ApplicationError:
    return temporalio.exceptions.ApplicationError(
        f"{operation} hit an unexpected {type(exc).__name__}: {exc}",
        type=type(exc).__name__,
        non_retryable=True,
    )


def _current_run_id() -> str | None:
    if temporalio.workflow.in_workflow():
        return temporalio.workflow.info().run_id
    if temporalio.activity.in_activity():
        return temporalio.activity.info().workflow_run_id
    return None


@asynccontextmanager
async def _degrade_on_failure(operation: str, temporal_workflow_id: str) -> AsyncGenerator[None, None]:
    try:
        yield
    except ResponseValidationError as exc:
        logger.error(
            "Search key response could not be parsed; skipping",
            operation=operation,
            temporal_workflow_id=temporal_workflow_id,
            **extract_error_context(exc),
        )
    except SDKError as exc:
        if _is_retryable(exc):
            raise
        logger.error(
            "Search key request rejected; skipping",
            operation=operation,
            temporal_workflow_id=temporal_workflow_id,
            status_code=exc.status_code,
        )
    except httpx.TransportError as exc:
        raise NoResponseError(f"{operation} transport failure: {exc}") from exc
    except Exception as exc:
        if _is_retryable(exc):
            raise
        raise _bug(exc, operation) from exc


async def _upsert_search_keys_impl(
    client: PrivateWorkerClient,
    temporal_workflow_id: str,
    temporal_run_id: str,
    search_key_metadata: dict[str, str],
) -> None:
    async with _degrade_on_failure("add_search_keys", temporal_workflow_id):
        response = await client.upsert_execution_metadata_async(
            temporal_workflow_id=temporal_workflow_id,
            temporal_run_id=temporal_run_id,
            search_key_metadata=search_key_metadata,
        )
        if response.metadata_status != "ok":
            logger.warning(
                "Search keys only partially persisted",
                temporal_workflow_id=temporal_workflow_id,
                dropped_keys=response.dropped_keys,
                truncated_keys=response.truncated_keys,
            )


async def _delete_search_keys_impl(
    client: PrivateWorkerClient,
    temporal_workflow_id: str,
    temporal_run_id: str,
    keys: list[str],
) -> None:
    async with _degrade_on_failure("delete_search_keys", temporal_workflow_id):
        await client.delete_execution_metadata_async(
            temporal_workflow_id=temporal_workflow_id,
            temporal_run_id=temporal_run_id,
            keys=keys,
        )


# Neither Temporal's RetryPolicy nor @activity's tenacity covers this branch (activity.py).
_retry_transient = tenacity.retry(
    retry=tenacity.retry_if_exception(_is_retryable),
    stop=tenacity.stop_after_attempt(_MAX_REQUEST_ATTEMPTS),
    wait=tenacity.wait_exponential(multiplier=_RETRY_BACKOFF_SECONDS),
    reraise=True,
)
_upsert_with_retries = _retry_transient(_upsert_search_keys_impl)
_delete_with_retries = _retry_transient(_delete_search_keys_impl)


@activity(name=UPSERT_SEARCH_KEYS_ACTIVITY_NAME, _allow_reserved_name=True)
async def _upsert_search_keys(
    temporal_workflow_id: str,
    temporal_run_id: str,
    search_key_metadata: dict[str, str],
) -> None:
    async with get_worker_client(headers=config.worker.mistral_api_headers, timeout=_REQUEST_TIMEOUT_SECONDS) as client:
        try:
            await _upsert_search_keys_impl(client, temporal_workflow_id, temporal_run_id, search_key_metadata)
        except (SDKError, NoResponseError) as exc:
            raise temporalio.exceptions.ApplicationError(
                f"http_status={getattr(exc, 'status_code', None)} body={getattr(exc, 'body', None)}: {exc}",
                type=type(exc).__name__,
            ) from exc


@activity(name=DELETE_SEARCH_KEYS_ACTIVITY_NAME, _allow_reserved_name=True)
async def _delete_search_keys(temporal_workflow_id: str, temporal_run_id: str, keys: list[str]) -> None:
    async with get_worker_client(headers=config.worker.mistral_api_headers, timeout=_REQUEST_TIMEOUT_SECONDS) as client:
        try:
            await _delete_search_keys_impl(client, temporal_workflow_id, temporal_run_id, keys)
        except (SDKError, NoResponseError) as exc:
            raise temporalio.exceptions.ApplicationError(
                f"http_status={getattr(exc, 'status_code', None)} body={getattr(exc, 'body', None)}: {exc}",
                type=type(exc).__name__,
            ) from exc


async def _dispatch(
    activity_fn: Callable[[str, str, _Payload], Awaitable[None]],
    direct_fn: Callable[[PrivateWorkerClient, str, str, _Payload], Awaitable[None]],
    payload: _Payload,
    failure_message: str,
) -> None:
    """Run one search key request against the current execution, degrading on failure."""
    ctx = retrieve_context()
    run_id = _current_run_id()
    if ctx is None or run_id is None:
        logger.warning(
            "No execution run id available; skipping search key request",
            failure_message=failure_message,
            search_keys=sorted(payload),
        )
        return

    try:
        if temporalio.workflow.in_workflow():
            await temporalio.workflow.execute_local_activity(
                activity_fn,
                args=[ctx.execution_id, run_id, payload],
                start_to_close_timeout=timedelta(seconds=_REQUEST_TIMEOUT_SECONDS),
                retry_policy=temporalio.common.RetryPolicy(
                    initial_interval=timedelta(seconds=_RETRY_BACKOFF_SECONDS),
                    backoff_coefficient=2.0,
                    maximum_attempts=_MAX_REQUEST_ATTEMPTS,
                ),
            )
        else:
            async with get_worker_client(
                headers=config.worker.mistral_api_headers, timeout=_REQUEST_TIMEOUT_SECONDS
            ) as client:
                await direct_fn(client, ctx.execution_id, run_id, payload)
    except (
        SDKError,
        NoResponseError,
        temporalio.exceptions.ActivityError,
        temporalio.exceptions.ApplicationError,
    ) as exc:
        # Only exhausted-retry failures are dropped; bugs and cancellation must reach the caller.
        if _must_propagate(exc):
            raise
        logger.warning(failure_message, search_keys=sorted(payload), **extract_error_context(exc))


async def ingest_search_keys(search_keys: Mapping[str, SearchKeyValue], _allow_reserved: bool = False) -> None:
    coerced = _validate_and_coerce(search_keys, allow_reserved=_allow_reserved)
    if coerced:
        await _dispatch(_upsert_search_keys, _upsert_with_retries, coerced, "Failed to upsert search keys")


async def discard_search_keys(keys: Sequence[str], _allow_reserved: bool = False) -> None:
    validated = _validate_keys(keys, allow_reserved=_allow_reserved)
    if validated:
        await _dispatch(_delete_search_keys, _delete_with_retries, validated, "Failed to delete search keys")
