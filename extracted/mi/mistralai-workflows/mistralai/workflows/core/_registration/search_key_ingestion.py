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

Values are stored UNENCRYPTED.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, timedelta
from enum import Enum
from typing import NoReturn, TypeAlias
from uuid import UUID

import httpx
import structlog
import temporalio.common
import temporalio.exceptions
import temporalio.workflow
import tenacity

from mistralai.workflows.core._registration.execution_registration_interceptor import _hash_token
from mistralai.workflows.core._registration.search_keys import _cap_value, _coerce_leaf
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

SearchKeyValue: TypeAlias = str | int | float | bool | Enum | UUID | date | None

_CONTAINER_TYPES = (Mapping, list, tuple, set, frozenset)

_LOG_KEY_PREVIEW_CHARS = 64

# Retryable alongside 5xx; every other status the server answers with is permanent.
_RETRYABLE_STATUS_CODES = frozenset({408, 429})

# One budget for both dispatch branches, so they retry alike.
_MAX_UPSERT_ATTEMPTS = 3
_RETRY_BACKOFF_SECONDS = 0.2
_UPSERT_TIMEOUT_SECONDS = 10.0


def _raise_invalid(message: str) -> NoReturn:
    raise temporalio.exceptions.ApplicationError(message, non_retryable=True)


def _validate_and_coerce(search_keys: Mapping[str, SearchKeyValue]) -> dict[str, str]:
    if not isinstance(search_keys, Mapping):
        _raise_invalid(f"add_search_keys expects a mapping, got {type(search_keys).__name__}.")
    if len(search_keys) > MAX_SEARCH_KEYS:
        _raise_invalid(f"add_search_keys accepts at most {MAX_SEARCH_KEYS} keys per call, got {len(search_keys)}.")

    coerced: dict[str, str] = {}
    for key, value in search_keys.items():
        if not isinstance(key, str):
            _raise_invalid(f"Search key must be a string, got {type(key).__name__}.")
        if not key or key != key.strip():
            _raise_invalid("Search key must not be empty or padded with whitespace.")
        if ":" in key:
            _raise_invalid(f"Search key `{key}` must not contain ':'.")
        if isinstance(value, _CONTAINER_TYPES):
            _raise_invalid(f"Search key `{key}` must map to a scalar value, got {type(value).__name__}.")

        if value is None:
            logger.debug("Search key value is None; skipping", search_key=key)
            continue
        if len(key) > MAX_SEARCH_KEY_CHARS:
            logger.warning(
                "Search key exceeded length cap; dropping",
                search_key=key[:_LOG_KEY_PREVIEW_CHARS],
                key_chars=len(key),
                max_chars=MAX_SEARCH_KEY_CHARS,
            )
            continue
        coerced[key] = _cap_value(key, _coerce_leaf(value))
    return coerced


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, NoResponseError):
        return True
    return isinstance(exc, SDKError) and (exc.status_code >= 500 or exc.status_code in _RETRYABLE_STATUS_CODES)


def _must_propagate(exc: BaseException) -> bool:
    inner = exc.cause if isinstance(exc, temporalio.exceptions.ActivityError) else exc
    if isinstance(inner, temporalio.exceptions.CancelledError):
        return True
    return isinstance(inner, temporalio.exceptions.ApplicationError) and inner.non_retryable


def _bug(exc: Exception) -> temporalio.exceptions.ApplicationError:
    return temporalio.exceptions.ApplicationError(
        f"add_search_keys hit an unexpected {type(exc).__name__}: {exc}",
        type=type(exc).__name__,
        non_retryable=True,
    )


async def _upsert_search_keys_impl(
    client: PrivateWorkerClient,
    temporal_workflow_id: str,
    execution_token_hash: str,
    search_key_metadata: dict[str, str],
) -> None:
    try:
        response = await client.upsert_execution_metadata_async(
            temporal_workflow_id=temporal_workflow_id,
            execution_token_hash=execution_token_hash,
            search_key_metadata=search_key_metadata,
        )
        metadata_status = response.metadata_status
        dropped_keys = response.dropped_keys
        truncated_keys = response.truncated_keys
    except ResponseValidationError as exc:
        logger.error(
            "Search key upsert response could not be parsed; skipping",
            temporal_workflow_id=temporal_workflow_id,
            **extract_error_context(exc),
        )
        return
    except SDKError as exc:
        if _is_retryable(exc):
            raise
        logger.error(
            "Search key upsert rejected; skipping",
            temporal_workflow_id=temporal_workflow_id,
            status_code=exc.status_code,
        )
        return
    except httpx.TransportError as exc:
        raise NoResponseError(f"upsert_search_keys transport failure: {exc}") from exc
    except Exception as exc:
        if _is_retryable(exc):
            raise
        raise _bug(exc) from exc

    if metadata_status != "ok":
        logger.warning(
            "Search keys only partially persisted",
            temporal_workflow_id=temporal_workflow_id,
            dropped_keys=dropped_keys,
            truncated_keys=truncated_keys,
        )


# Neither Temporal's RetryPolicy nor @activity's tenacity covers this branch (activity.py).
_upsert_with_retries = tenacity.retry(
    retry=tenacity.retry_if_exception(_is_retryable),
    stop=tenacity.stop_after_attempt(_MAX_UPSERT_ATTEMPTS),
    wait=tenacity.wait_exponential(multiplier=_RETRY_BACKOFF_SECONDS),
    reraise=True,
)(_upsert_search_keys_impl)


@activity(name=UPSERT_SEARCH_KEYS_ACTIVITY_NAME, _allow_reserved_name=True)
async def _upsert_search_keys(
    temporal_workflow_id: str,
    execution_token_hash: str,
    search_key_metadata: dict[str, str],
) -> None:
    async with get_worker_client(headers=config.worker.mistral_api_headers) as client:
        try:
            await _upsert_search_keys_impl(client, temporal_workflow_id, execution_token_hash, search_key_metadata)
        except (SDKError, NoResponseError) as exc:
            raise temporalio.exceptions.ApplicationError(
                f"http_status={getattr(exc, 'status_code', None)} body={getattr(exc, 'body', None)}: {exc}",
                type=type(exc).__name__,
            ) from exc


async def ingest_search_keys(search_keys: Mapping[str, SearchKeyValue]) -> None:
    coerced = _validate_and_coerce(search_keys)
    if not coerced:
        return

    ctx = retrieve_context()
    raw_token = ctx.execution_token if ctx else None
    if ctx is None or raw_token is None:
        logger.warning(
            "No execution token available; skipping search key upsert",
            search_keys=sorted(coerced),
        )
        return

    token_hash = _hash_token(raw_token)
    try:
        if temporalio.workflow.in_workflow():
            await temporalio.workflow.execute_local_activity(
                _upsert_search_keys,
                args=[ctx.execution_id, token_hash, coerced],
                start_to_close_timeout=timedelta(seconds=_UPSERT_TIMEOUT_SECONDS),
                retry_policy=temporalio.common.RetryPolicy(
                    initial_interval=timedelta(seconds=_RETRY_BACKOFF_SECONDS),
                    backoff_coefficient=2.0,
                    maximum_attempts=_MAX_UPSERT_ATTEMPTS,
                ),
            )
        else:
            async with get_worker_client(headers=config.worker.mistral_api_headers) as client:
                await _upsert_with_retries(client, ctx.execution_id, token_hash, coerced)
    except (
        SDKError,
        NoResponseError,
        temporalio.exceptions.ActivityError,
        temporalio.exceptions.ApplicationError,
    ) as exc:
        # Only exhausted-retry failures are dropped; bugs and cancellation must reach the caller.
        if _must_propagate(exc):
            raise
        logger.warning(
            "Failed to upsert search keys",
            search_keys=sorted(coerced),
            **extract_error_context(exc),
        )
