"""Retry search key requests without null-valued keys on a 422: pre-WFL-2404 backends
reject nulls. Delete this module once no such backend can still be deployed (WFL-2870)."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar

from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.worker_client.errors.sdkerror import SDKError

logger = get_logger(__name__)

_T = TypeVar("_T")


async def call_stripping_nulls_on_rejection(
    call: Callable[[dict[str, str | None] | None], Awaitable[_T]],
    search_key_metadata: dict[str, str | None] | None,
) -> _T:
    try:
        return await call(search_key_metadata)
    except SDKError as exc:
        if exc.status_code != 422 or search_key_metadata is None:
            raise
        null_keys = sorted(key for key, value in search_key_metadata.items() if value is None)
        if not null_keys:
            raise
        logger.info("Backend rejected null search key values; retrying without them", dropped_keys=null_keys)
        return await call({key: value for key, value in search_key_metadata.items() if value is not None})
