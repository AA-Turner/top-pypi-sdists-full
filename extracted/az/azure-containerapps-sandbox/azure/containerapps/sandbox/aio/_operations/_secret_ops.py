"""Async secret operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.async_paging import AsyncItemPaged
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import (
    _validate_continuation_token,
    _validate_segment,
)
from azure.containerapps.sandbox._models import SecretMetadata, SecretValuePeek

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class AsyncSecretOperationsMixin:
    """Async secret operations (list, upsert, delete, keys, peek)."""

    @distributed_trace
    def list_secrets(self, **kwargs: Any) -> AsyncItemPaged[SecretMetadata]:
        """List all secrets in a sandbox group."""
        base_url = f"{self._endpoint}{self._group_path}/secrets"
        params = {"api-version": self._api_version}

        async def _get_next(continuation_token=None):
            if continuation_token:
                _validate_continuation_token(continuation_token, self._endpoint)
                request = HttpRequest("GET", continuation_token)
            else:
                request = HttpRequest("GET", base_url, params=params)
            return await self._send_request(request)

        async def _extract_data(response):
            data = response.json()
            items = [SecretMetadata._from_dict(s) for s in data.get("secrets", [])]
            return data.get("nextLink"), iter(items)

        return AsyncItemPaged(_get_next, extract_data=_extract_data)

    @distributed_trace_async
    async def upsert_secret(self, secret_id: str, values: dict[str, str], **kwargs: Any) -> SecretValuePeek:
        """Create or update a secret."""
        _validate_segment(secret_id, "secret_id")
        path = f"{self._group_path}/secrets/{secret_id}"
        result = await self._dp_put(path, {"values": values})
        return SecretValuePeek._from_dict(result if isinstance(result, dict) else None) or SecretValuePeek()

    @distributed_trace_async
    async def delete_secret(self, secret_id: str, **kwargs: Any) -> None:
        """Delete a secret."""
        _validate_segment(secret_id, "secret_id")
        await self._dp_delete(f"{self._group_path}/secrets/{secret_id}")

    @distributed_trace_async
    async def list_secret_keys(self, secret_id: str, **kwargs: Any) -> list[str]:
        """List keys of a secret."""
        _validate_segment(secret_id, "secret_id")
        path = f"{self._group_path}/secrets/{secret_id}/keys"
        result = await self._dp_get(path)
        if isinstance(result, dict):
            return result.get("keys", [])
        return result if isinstance(result, list) else []

    @distributed_trace_async
    async def peek_secret(self, secret_id: str, **kwargs: Any) -> SecretValuePeek:
        """Peek at secret values."""
        _validate_segment(secret_id, "secret_id")
        path = f"{self._group_path}/secrets/{secret_id}/peek"
        result = await self._dp_post(path)
        return SecretValuePeek._from_dict(result if isinstance(result, dict) else None) or SecretValuePeek()
