"""Async secret operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.async_paging import AsyncItemPaged
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import (
    _get_json_array,
    _ERROR_MAP,
    _validate_segment,
)
from azure.containerapps.sandbox._models import SecretMetadata, SecretValuePeek
from azure.containerapps.sandbox._response_helpers import _normalize_page

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class AsyncSecretOperationsMixin:
    """Async secret operations (list, upsert, delete, keys, peek)."""

    @distributed_trace
    def list_secrets(self, **kwargs: Any) -> AsyncItemPaged[SecretMetadata]:
        """List all secrets in a sandbox group."""
        return self._generated.secrets.list(
            **{
                "error_map": _ERROR_MAP,
                "_continuation_endpoint": self._endpoint,
                "cls": _normalize_page,
                **kwargs,
            },
        )

    @distributed_trace_async
    async def upsert_secret(self, secret_id: str, values: dict[str, str], **kwargs: Any) -> SecretValuePeek:
        """Create or update a secret."""
        _validate_segment(secret_id, "secret_id")
        result = await self._generated.secrets.set(secret_id, {"values": values}, **{"error_map": _ERROR_MAP, **kwargs})
        return SecretValuePeek._from_dict(dict(result)) or SecretValuePeek()

    @distributed_trace_async
    async def delete_secret(self, secret_id: str, **kwargs: Any) -> None:
        """Delete a secret."""
        _validate_segment(secret_id, "secret_id")
        await self._generated.secrets.delete(secret_id, **{"error_map": _ERROR_MAP, **kwargs})

    @distributed_trace_async
    async def list_secret_keys(self, secret_id: str, **kwargs: Any) -> list[str]:
        """List keys of a secret."""
        _validate_segment(secret_id, "secret_id")
        result = dict(await self._generated.secrets.list_keys(secret_id, **{"error_map": _ERROR_MAP, **kwargs}))
        return _get_json_array(result, "keys")

    @distributed_trace_async
    async def peek_secret(self, secret_id: str, **kwargs: Any) -> SecretValuePeek:
        """Peek at secret values."""
        _validate_segment(secret_id, "secret_id")
        result = await self._generated.secrets.peek(secret_id, **{"error_map": _ERROR_MAP, **kwargs})
        return SecretValuePeek._from_dict(dict(result)) or SecretValuePeek()
