"""Dict and queue requests under a person's management credentials."""

from __future__ import annotations

import gzip
import json
from collections.abc import Mapping
from typing import TYPE_CHECKING

from labqoat.base_client import BaseClient
from labqoat.coordination.store_reply import StoreReply
from labqoat.errors.transport_error import TransportError
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.net.http_error import HttpError
from labqoat.net.http_timeout_error import HttpTimeoutError

if TYPE_CHECKING:
    from labqoat._generated.transport import Transport
    from labqoat.net.response import Response


class ManagementChannel:
    """Reach the dicts and queues of the client's project, giving a held request as long as the service may hold it."""

    PREFIX = "/api/v1"

    def __init__(self, transport: Transport) -> None:
        """Share the client's transport, its credentials and its project selection."""
        self._transport = transport

    def send(
        self, method: str, path: str, document: Mapping[str, JsonValue] | None = None, wait: float = 0.0
    ) -> StoreReply:
        """Send one request; a missing name or a full partition is an answer, anything else failing raises."""
        target = self.PREFIX + path
        content, headers = self._body(document)
        timeout = self._transport.timeout_seconds + wait
        client = self._transport.open_client()
        try:
            response = client.request(method, target, content=content, headers=headers, timeout=timeout)
        except HttpTimeoutError as error:
            raise TransportError(f"Request to {target} exceeded its deadline.", timed_out=True) from error
        except HttpError as error:
            raise TransportError(f"Could not reach the API at {target}.") from error
        return ManagementChannel.reply(target, response)

    def _body(self, document: Mapping[str, JsonValue] | None) -> tuple[bytes | None, dict[str, str]]:
        """Authenticate every request and compress large bodies the way other clients do."""
        headers = self._transport.basic_headers(self._transport.username, self._transport.password)
        if document is None:
            return None, headers
        body = json.dumps(document, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
        headers["content-type"] = "application/json"
        if len(body) >= BaseClient.COMPRESSED_FROM:
            body = gzip.compress(body, compresslevel=6, mtime=0)
            headers["content-encoding"] = "gzip"
        return body, headers

    @staticmethod
    def reply(target: str, response: Response) -> StoreReply:
        """Turn a response into a reply, raising the client's usual errors for anything unexpected."""
        if response.status_code in (404, 409):
            return StoreReply(response.status_code)
        BaseClient.raise_for_status(target, response)
        if not response.content:
            return StoreReply(response.status_code)
        return StoreReply(response.status_code, JsonDocument.expect_dict(response.json()))
