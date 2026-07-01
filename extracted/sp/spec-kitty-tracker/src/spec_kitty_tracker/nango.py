from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from spec_kitty_tracker.capabilities import TrackerCapabilities
from spec_kitty_tracker.models import (
    CanonicalIssue,
    CanonicalLink,
    CanonicalStatus,
    ExternalRef,
    Page,
    SyncCheckpoint,
    TrackerEvent,
)
from spec_kitty_tracker.protocols import IssuePatch

NANGO_MANAGED_TOKEN: str = "nango-managed"


@dataclass(frozen=True, slots=True)
class NangoConnectionContext:
    connection_id: str
    provider_config_key: str
    nango_secret_key: str
    nango_base_url: str = "https://api.nango.dev"

    def __post_init__(self) -> None:
        for field_name in ("connection_id", "provider_config_key", "nango_secret_key"):
            value = getattr(self, field_name)
            if not value or not value.strip():
                raise ValueError(f"{field_name} must be non-empty")


class NangoProxyTransport(httpx.AsyncBaseTransport):
    """Custom httpx transport that rewrites requests to route through Nango proxy."""

    def __init__(
        self,
        context: NangoConnectionContext,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._context = context
        self._transport = transport or httpx.AsyncHTTPTransport()

    # Provider- and transport-specific headers that must be stripped when
    # proxying. The Nango proxy authenticates via the injected Authorization
    # header; forwarding provider-native auth headers would leak sentinel
    # values. Forwarding the original upstream Host header can also break proxy
    # routing when the request is rewritten from the provider host to
    # api.nango.dev.
    _STRIP_HEADERS = frozenset({"private-token", "host"})

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        # raw_path includes path + query string, e.g. b"/repos/o/r/issues?state=open"
        raw_path = request.url.raw_path.decode("ascii")

        proxy_url = f"{self._context.nango_base_url}/proxy{raw_path}"

        headers = {
            k: v for k, v in request.headers.items() if k.lower() not in self._STRIP_HEADERS
        }
        headers["authorization"] = f"Bearer {self._context.nango_secret_key}"
        headers["connection-id"] = self._context.connection_id
        headers["provider-config-key"] = self._context.provider_config_key

        proxy_request = httpx.Request(
            method=request.method,
            url=proxy_url,
            headers=headers,
            content=request.content,
        )

        return await self._transport.handle_async_request(proxy_request)

    async def aclose(self) -> None:
        await self._transport.aclose()


class NangoProxyAdapter:
    """Wraps an HTTP connector to route all requests through Nango proxy."""

    def __init__(
        self,
        connector_cls: type,
        config: Any,
        context: NangoConnectionContext,
    ) -> None:
        self._transport = NangoProxyTransport(context)
        self._client = httpx.AsyncClient(transport=self._transport)
        self._connector = connector_cls(config, client=self._client)
        self.name: str = self._connector.name

    # --- TaskTrackerConnector delegation ---

    async def get_capabilities(self) -> TrackerCapabilities:
        return await self._connector.get_capabilities()

    async def list_issues(
        self,
        *,
        updated_since: datetime | None,
        cursor: str | None,
        limit: int,
        filters: Mapping[str, Any] | None,
    ) -> Page[CanonicalIssue]:
        return await self._connector.list_issues(
            updated_since=updated_since,
            cursor=cursor,
            limit=limit,
            filters=filters,
        )

    async def get_issue(self, ref: ExternalRef) -> CanonicalIssue:
        return await self._connector.get_issue(ref)

    async def create_issue(self, issue: CanonicalIssue) -> CanonicalIssue:
        return await self._connector.create_issue(issue)

    async def update_issue(
        self,
        ref: ExternalRef,
        patch: IssuePatch,
        *,
        idempotency_key: str | None,
    ) -> CanonicalIssue:
        return await self._connector.update_issue(
            ref, patch, idempotency_key=idempotency_key
        )

    async def transition_issue(
        self,
        ref: ExternalRef,
        target_status: CanonicalStatus,
    ) -> CanonicalIssue:
        return await self._connector.transition_issue(ref, target_status)

    async def upsert_link(self, ref: ExternalRef, link: CanonicalLink) -> None:
        return await self._connector.upsert_link(ref, link)

    async def add_comment(self, ref: ExternalRef, body: str) -> None:
        return await self._connector.add_comment(ref, body)

    async def list_events(
        self,
        cursor: SyncCheckpoint | None,
        limit: int,
    ) -> tuple[list[TrackerEvent], SyncCheckpoint | None]:
        return await self._connector.list_events(cursor, limit)

    # --- Lifecycle ---

    async def close(self) -> None:
        await self._client.aclose()
        await self._transport.aclose()

    async def __aenter__(self) -> NangoProxyAdapter:
        return self

    async def __aexit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        await self.close()
