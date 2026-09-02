from __future__ import annotations

import json

import httpx
import pytest

from spec_kitty_tracker.connectors.github import GitHubConnector, GitHubConnectorConfig
from spec_kitty_tracker.errors import ConnectorRequestError, FailureClass
from spec_kitty_tracker.nango import (
    NANGO_MANAGED_TOKEN,
    NangoConnectionContext,
    NangoProxyTransport,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class RecordingTransport(httpx.AsyncBaseTransport):
    """Captures the request and returns a canned response."""

    def __init__(
        self,
        response_json: dict | list,
        status_code: int = 200,
        response_headers: dict[str, str] | None = None,
    ) -> None:
        self.last_request: httpx.Request | None = None
        self._body = json.dumps(response_json).encode()
        self._status_code = status_code
        self._response_headers = response_headers or {}

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        self.last_request = request
        headers = {"content-type": "application/json", **self._response_headers}
        return httpx.Response(
            status_code=self._status_code,
            content=self._body,
            headers=headers,
        )

    async def aclose(self) -> None:
        pass


def _make_context() -> NangoConnectionContext:
    return NangoConnectionContext(
        connection_id="sk:team1:proj1:github:bind1:user42",
        provider_config_key="github",
        nango_secret_key="test-secret-key",
    )


def _make_github_chain(
    recording: RecordingTransport,
) -> tuple[GitHubConnector, httpx.AsyncClient]:
    context = _make_context()
    config = GitHubConnectorConfig(owner="myorg", repo="myrepo", token=NANGO_MANAGED_TOKEN)
    transport = NangoProxyTransport(context, transport=recording)
    client = httpx.AsyncClient(transport=transport)
    connector = GitHubConnector(config, client=client)
    return connector, client


# ---------------------------------------------------------------------------
# T015: Package exports validation
# ---------------------------------------------------------------------------


class TestPackageExports:
    def test_all_nango_symbols_importable(self) -> None:
        from spec_kitty_tracker import (
            NANGO_MANAGED_TOKEN,
            NangoConnectionContext,
            NangoProxyAdapter,
            NangoProxyTransport,
        )

        assert NANGO_MANAGED_TOKEN is not None
        assert NangoConnectionContext is not None
        assert NangoProxyAdapter is not None
        assert NangoProxyTransport is not None

    def test_all_discovery_symbols_importable(self) -> None:
        from spec_kitty_tracker import (
            DiscoveredResource,
            DiscoveredWorkspace,
            DiscoveryResult,
            JSONValue,
            discover_resources,
            discover_workspaces,
        )

        assert DiscoveredWorkspace is not None
        assert DiscoveredResource is not None
        assert DiscoveryResult is not None
        assert discover_workspaces is not None
        assert discover_resources is not None
        assert JSONValue is not None

    def test_all_new_symbols_in_dunder_all(self) -> None:
        import spec_kitty_tracker

        expected = {
            "NANGO_MANAGED_TOKEN",
            "NangoConnectionContext",
            "NangoProxyAdapter",
            "NangoProxyTransport",
            "DiscoveredWorkspace",
            "DiscoveredResource",
            "DiscoveryResult",
            "discover_workspaces",
            "discover_resources",
            "JSONValue",
        }
        assert expected.issubset(set(spec_kitty_tracker.__all__))


# ---------------------------------------------------------------------------
# T016: Integration smoke test
# ---------------------------------------------------------------------------


class TestIntegrationSmokeTest:
    @pytest.mark.asyncio
    async def test_adapter_wraps_github_connector_end_to_end(self) -> None:
        """Full chain: NangoProxyTransport → GitHubConnector → mock."""
        recording = RecordingTransport(response_json=[])
        connector, client = _make_github_chain(recording)

        page = await connector.list_issues(updated_since=None, cursor=None, limit=10, filters=None)

        assert recording.last_request is not None
        url = str(recording.last_request.url)
        assert "/proxy/" in url
        assert "repos/myorg/myrepo/issues" in url

        headers = dict(recording.last_request.headers)
        assert headers["connection-id"] == "sk:team1:proj1:github:bind1:user42"
        assert headers["provider-config-key"] == "github"
        assert "test-secret-key" in headers["authorization"]

        assert page.items == []
        await client.aclose()


# ---------------------------------------------------------------------------
# T018: Error handling validation
# ---------------------------------------------------------------------------


class TestErrorHandlingThroughProxy:
    @pytest.mark.asyncio
    async def test_proxy_401_raises_authentication_error(self) -> None:
        """Expired/revoked connection -> Nango returns 401 -> ConnectorRequestError."""
        recording = RecordingTransport(
            response_json={"error": "invalid_connection"},
            status_code=401,
        )
        connector, client = _make_github_chain(recording)

        with pytest.raises(ConnectorRequestError) as exc_info:
            await connector.list_issues(updated_since=None, cursor=None, limit=10, filters=None)
        assert exc_info.value.failure_class == FailureClass.AUTHENTICATION
        assert exc_info.value.status_code == 401
        await client.aclose()

    @pytest.mark.asyncio
    async def test_proxy_429_raises_rate_limit_error(self) -> None:
        """Rate limit from Nango -> ConnectorRequestError with RATE_LIMIT class."""
        recording = RecordingTransport(
            response_json={"error": "rate_limited"},
            status_code=429,
            response_headers={"Retry-After": "60"},
        )
        connector, client = _make_github_chain(recording)

        with pytest.raises(ConnectorRequestError) as exc_info:
            await connector.list_issues(updated_since=None, cursor=None, limit=10, filters=None)
        assert exc_info.value.failure_class == FailureClass.RATE_LIMIT
        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after_seconds == 60
        await client.aclose()

    @pytest.mark.asyncio
    async def test_proxy_500_raises_transient_error(self) -> None:
        """Nango server error -> ConnectorRequestError with TRANSIENT class."""
        recording = RecordingTransport(
            response_json={"error": "internal_server_error"},
            status_code=500,
        )
        connector, client = _make_github_chain(recording)

        with pytest.raises(ConnectorRequestError) as exc_info:
            await connector.list_issues(updated_since=None, cursor=None, limit=10, filters=None)
        assert exc_info.value.failure_class == FailureClass.TRANSIENT
        assert exc_info.value.status_code == 500
        await client.aclose()

    @pytest.mark.asyncio
    async def test_proxy_403_raises_permission_error(self) -> None:
        """Forbidden -> ConnectorRequestError with PERMISSION class."""
        recording = RecordingTransport(
            response_json={"error": "forbidden"},
            status_code=403,
        )
        connector, client = _make_github_chain(recording)

        with pytest.raises(ConnectorRequestError) as exc_info:
            await connector.list_issues(updated_since=None, cursor=None, limit=10, filters=None)
        assert exc_info.value.failure_class == FailureClass.PERMISSION
        assert exc_info.value.status_code == 403
        await client.aclose()
