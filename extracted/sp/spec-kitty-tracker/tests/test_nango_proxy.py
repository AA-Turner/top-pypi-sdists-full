from __future__ import annotations

import json

import httpx
import pytest

from spec_kitty_tracker.nango import (
    NANGO_MANAGED_TOKEN,
    NangoConnectionContext,
    NangoProxyAdapter,
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


def _make_context(**overrides: str) -> NangoConnectionContext:
    defaults = {
        "connection_id": "sk:team1:proj1:github:bind1:user42",
        "provider_config_key": "github",
        "nango_secret_key": "test-secret-key",
    }
    defaults.update(overrides)
    return NangoConnectionContext(**defaults)


# ---------------------------------------------------------------------------
# NangoConnectionContext tests
# ---------------------------------------------------------------------------


class TestNangoConnectionContext:
    def test_valid_construction(self) -> None:
        ctx = _make_context()
        assert ctx.connection_id == "sk:team1:proj1:github:bind1:user42"
        assert ctx.provider_config_key == "github"
        assert ctx.nango_secret_key == "test-secret-key"
        assert ctx.nango_base_url == "https://api.nango.dev"

    def test_custom_base_url(self) -> None:
        ctx = _make_context(nango_base_url="https://nango.self-hosted.example")
        assert ctx.nango_base_url == "https://nango.self-hosted.example"

    def test_empty_connection_id_raises(self) -> None:
        with pytest.raises(ValueError, match="connection_id"):
            NangoConnectionContext(
                connection_id="",
                provider_config_key="github",
                nango_secret_key="secret",
            )

    def test_whitespace_connection_id_raises(self) -> None:
        with pytest.raises(ValueError, match="connection_id"):
            NangoConnectionContext(
                connection_id="   ",
                provider_config_key="github",
                nango_secret_key="secret",
            )

    def test_empty_provider_config_key_raises(self) -> None:
        with pytest.raises(ValueError, match="provider_config_key"):
            NangoConnectionContext(
                connection_id="conn-1",
                provider_config_key="",
                nango_secret_key="secret",
            )

    def test_empty_nango_secret_key_raises(self) -> None:
        with pytest.raises(ValueError, match="nango_secret_key"):
            NangoConnectionContext(
                connection_id="conn-1",
                provider_config_key="github",
                nango_secret_key="",
            )

    def test_frozen(self) -> None:
        ctx = _make_context()
        with pytest.raises(AttributeError):
            ctx.connection_id = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# NangoProxyTransport tests
# ---------------------------------------------------------------------------


class TestNangoProxyTransport:
    @pytest.fixture
    def context(self) -> NangoConnectionContext:
        return _make_context()

    @pytest.fixture
    def recording(self) -> RecordingTransport:
        return RecordingTransport(response_json={"ok": True})

    @pytest.fixture
    def transport(
        self, context: NangoConnectionContext, recording: RecordingTransport
    ) -> NangoProxyTransport:
        return NangoProxyTransport(context, transport=recording)

    @pytest.mark.asyncio
    async def test_url_rewrite_simple_path(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        request = httpx.Request("GET", "https://api.github.com/repos/o/r/issues")
        await transport.handle_async_request(request)

        assert recording.last_request is not None
        url = str(recording.last_request.url)
        assert url == "https://api.nango.dev/proxy/repos/o/r/issues"

    @pytest.mark.asyncio
    async def test_url_rewrite_preserves_query_params(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        request = httpx.Request(
            "GET", "https://api.github.com/repos/o/r/issues?state=open&per_page=50"
        )
        await transport.handle_async_request(request)

        url = str(recording.last_request.url)
        assert "/proxy/repos/o/r/issues" in url
        assert "state=open" in url
        assert "per_page=50" in url

    @pytest.mark.asyncio
    async def test_authorization_header_replaced(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        request = httpx.Request(
            "GET",
            "https://api.github.com/repos/o/r/issues",
            headers={"Authorization": "Bearer original-token"},
        )
        await transport.handle_async_request(request)

        headers = dict(recording.last_request.headers)
        assert headers["authorization"] == "Bearer test-secret-key"

    @pytest.mark.asyncio
    async def test_connection_id_header_injected(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        request = httpx.Request("GET", "https://api.github.com/repos/o/r/issues")
        await transport.handle_async_request(request)

        headers = dict(recording.last_request.headers)
        assert headers["connection-id"] == "sk:team1:proj1:github:bind1:user42"

    @pytest.mark.asyncio
    async def test_provider_config_key_header_injected(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        request = httpx.Request("GET", "https://api.github.com/repos/o/r/issues")
        await transport.handle_async_request(request)

        headers = dict(recording.last_request.headers)
        assert headers["provider-config-key"] == "github"

    @pytest.mark.asyncio
    async def test_http_method_preserved(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        for method in ("GET", "POST", "PATCH", "DELETE"):
            request = httpx.Request(method, "https://api.github.com/repos/o/r/issues")
            await transport.handle_async_request(request)
            assert recording.last_request.method == method

    @pytest.mark.asyncio
    async def test_request_body_forwarded(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        body = json.dumps({"title": "Test Issue"}).encode()
        request = httpx.Request(
            "POST",
            "https://api.github.com/repos/o/r/issues",
            content=body,
        )
        await transport.handle_async_request(request)

        forwarded = recording.last_request.content
        assert json.loads(forwarded) == {"title": "Test Issue"}

    @pytest.mark.asyncio
    async def test_root_path(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        request = httpx.Request("GET", "https://api.github.com/")
        await transport.handle_async_request(request)

        url = str(recording.last_request.url)
        assert url == "https://api.nango.dev/proxy/"

    @pytest.mark.asyncio
    async def test_custom_base_url(self, recording: RecordingTransport) -> None:
        ctx = _make_context(nango_base_url="https://nango.self-hosted.example")
        transport = NangoProxyTransport(ctx, transport=recording)

        request = httpx.Request("GET", "https://api.github.com/repos/o/r/issues")
        await transport.handle_async_request(request)

        url = str(recording.last_request.url)
        assert url.startswith("https://nango.self-hosted.example/proxy/")

    @pytest.mark.asyncio
    async def test_private_token_header_stripped(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        """PRIVATE-TOKEN header (used by GitLab) must be stripped by proxy transport."""
        request = httpx.Request(
            "GET",
            "https://gitlab.com/api/v4/projects/123/issues",
            headers={"PRIVATE-TOKEN": "nango-managed"},
        )
        await transport.handle_async_request(request)

        headers = dict(recording.last_request.headers)
        assert "private-token" not in headers
        assert "PRIVATE-TOKEN" not in headers
        # Authorization header should be the Nango bearer token
        assert headers["authorization"] == "Bearer test-secret-key"

    @pytest.mark.asyncio
    async def test_original_host_header_stripped(
        self, transport: NangoProxyTransport, recording: RecordingTransport
    ) -> None:
        request = httpx.Request(
            "POST",
            "https://api.linear.app/graphql",
            headers={"Host": "api.linear.app", "Content-Type": "application/json"},
            content=json.dumps({"query": "{ organization { id } }"}).encode(),
        )
        await transport.handle_async_request(request)

        headers = dict(recording.last_request.headers)
        assert headers["host"] == "api.nango.dev"
        assert headers["authorization"] == "Bearer test-secret-key"


# ---------------------------------------------------------------------------
# NangoProxyAdapter tests
# ---------------------------------------------------------------------------


class TestNangoProxyAdapter:
    @pytest.mark.asyncio
    async def test_satisfies_protocol(self) -> None:
        from spec_kitty_tracker.protocols import TaskTrackerConnector

        recording = RecordingTransport(response_json=[])
        context = _make_context()

        from spec_kitty_tracker.connectors.github import (
            GitHubConnector,
            GitHubConnectorConfig,
        )

        config = GitHubConnectorConfig(
            owner="myorg", repo="myrepo", token=NANGO_MANAGED_TOKEN
        )
        adapter = NangoProxyAdapter(GitHubConnector, config, context)

        assert isinstance(adapter, TaskTrackerConnector)
        await adapter.close()

    @pytest.mark.asyncio
    async def test_name_delegated(self) -> None:
        recording = RecordingTransport(response_json=[])
        context = _make_context()

        from spec_kitty_tracker.connectors.github import (
            GitHubConnector,
            GitHubConnectorConfig,
        )

        config = GitHubConnectorConfig(
            owner="myorg", repo="myrepo", token=NANGO_MANAGED_TOKEN
        )
        adapter = NangoProxyAdapter(GitHubConnector, config, context)
        assert adapter.name == "github"
        await adapter.close()

    @pytest.mark.asyncio
    async def test_list_issues_delegates_through_transport(self) -> None:
        """End-to-end: adapter → connector → transport → recording."""
        recording = RecordingTransport(response_json=[])
        context = _make_context()

        from spec_kitty_tracker.connectors.github import (
            GitHubConnector,
            GitHubConnectorConfig,
        )

        config = GitHubConnectorConfig(
            owner="myorg", repo="myrepo", token=NANGO_MANAGED_TOKEN
        )

        # Manually wire the transport so we can inject the recording
        transport = NangoProxyTransport(context, transport=recording)
        client = httpx.AsyncClient(transport=transport)
        connector = GitHubConnector(config, client=client)

        page = await connector.list_issues(
            updated_since=None, cursor=None, limit=10, filters=None
        )

        # Verify transport rewrote the request
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

    @pytest.mark.asyncio
    async def test_context_manager(self) -> None:
        from spec_kitty_tracker.connectors.github import (
            GitHubConnector,
            GitHubConnectorConfig,
        )

        config = GitHubConnectorConfig(
            owner="myorg", repo="myrepo", token=NANGO_MANAGED_TOKEN
        )
        context = _make_context()

        async with NangoProxyAdapter(GitHubConnector, config, context) as adapter:
            assert adapter.name == "github"
        # No exception means cleanup succeeded


# ---------------------------------------------------------------------------
# NANGO_MANAGED_TOKEN tests
# ---------------------------------------------------------------------------


class TestNangoManagedToken:
    def test_passes_strip_check(self) -> None:
        assert NANGO_MANAGED_TOKEN.strip() != ""

    def test_is_string(self) -> None:
        assert isinstance(NANGO_MANAGED_TOKEN, str)
