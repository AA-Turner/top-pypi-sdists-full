"""Tests for CLI-side identity-forward header injection."""

from __future__ import annotations

import time
from types import SimpleNamespace
from unittest.mock import MagicMock

import anyio
import pytest

from runlayer_cli import identity_forward as idf
from runlayer_cli.api import RunlayerClient
from runlayer_cli.models import ServerDetails
from runlayer_cli.models_api import IdentityForwardBundle


def _details(bundle: IdentityForwardBundle | None) -> ServerDetails:
    return ServerDetails(
        id="sid",
        name="test",
        url="http://127.0.0.1:9999/mcp",
        transport_type="streaming-http",
        identity_forward=bundle,
    )


class TestServerDetailsBundleParsing:
    def test_bundle_parsed_from_server_details(self) -> None:
        details = ServerDetails.model_validate(
            {
                "id": "sid",
                "name": "test",
                "url": "http://u",
                "transport_type": "streaming-http",
                "identity_forward": {
                    "headers": {"X-Runlayer-Subject-Type": "user"},
                    "expires_at": 1_720_000_000,
                    "applied": True,
                },
            }
        )
        assert details.identity_forward is not None
        assert details.identity_forward.applied is True
        assert details.identity_forward.expires_at == 1_720_000_000
        assert details.identity_forward.needs_refresh is True

    def test_older_backend_omits_field(self) -> None:
        """Backends that predate identity-forward embedding simply omit the
        field — must parse as None with no special-casing."""
        details = ServerDetails.model_validate(
            {
                "id": "sid",
                "name": "test",
                "url": "http://u",
                "transport_type": "streaming-http",
            }
        )
        assert details.identity_forward is None

    def test_needs_refresh_false_for_unsigned(self) -> None:
        bundle = IdentityForwardBundle(
            headers={"X-Runlayer-Subject-Type": "user"},
            expires_at=None,
            applied=True,
        )
        assert bundle.needs_refresh is False


def test_reserved_header_names_pin() -> None:
    """Hand-copied mirror of the backend's RESERVED_IDENTITY_HEADERS (the CLI
    can't import backend code). If the backend starts minting a new header
    name, add it here too — otherwise downgrades stop stripping it."""
    assert idf._RESERVED_HEADER_NAMES == frozenset(
        {
            "x-runlayer-subject-type",
            "x-runlayer-org-id",
            "x-runlayer-user-email",
            "x-runlayer-user-id",
            "x-runlayer-agent-id",
            "x-runlayer-agent-name",
            "x-runlayer-identity-token",
        }
    )


class TestTransportHoldsHeadersByReference:
    """The refresh design assumes fastmcp transports keep the passed headers
    dict by reference and re-read it at session (re)connect. Pin that so a
    fastmcp upgrade that copies the dict fails here, instead of silently
    turning the refresh loop into dead code."""

    def test_streamable_http_transport_sees_dict_mutation(self) -> None:
        from fastmcp.client.transports import StreamableHttpTransport

        headers = {"User-Agent": "Runlayer"}
        transport = StreamableHttpTransport("http://127.0.0.1:9/mcp", headers=headers)
        idf.merge_bundle_into_headers(
            headers,
            IdentityForwardBundle(
                headers={"X-Runlayer-Identity-Token": "fresh"},
                expires_at=None,
                applied=True,
            ),
        )
        assert transport.headers["X-Runlayer-Identity-Token"] == "fresh"

    def test_sse_transport_sees_dict_mutation(self) -> None:
        from fastmcp.client.transports import SSETransport

        headers = {"User-Agent": "Runlayer"}
        transport = SSETransport("http://127.0.0.1:9/sse", headers=headers)
        idf.merge_bundle_into_headers(
            headers,
            IdentityForwardBundle(
                headers={"X-Runlayer-Identity-Token": "fresh"},
                expires_at=None,
                applied=True,
            ),
        )
        assert transport.headers["X-Runlayer-Identity-Token"] == "fresh"


class TestMergeBundleIntoHeaders:
    def test_applied_bundle_overwrites_reserved_headers(self) -> None:
        headers = {
            "User-Agent": "Runlayer",
            "X-Runlayer-User-Id": "stale",
            "X-Runlayer-Custom-Foo": "keep",
        }
        bundle = IdentityForwardBundle(
            headers={
                "X-Runlayer-Subject-Type": "user",
                "X-Runlayer-User-Id": "fresh",
            },
            expires_at=None,
            applied=True,
        )

        idf.merge_bundle_into_headers(headers, bundle)

        assert headers["User-Agent"] == "Runlayer"
        assert headers["X-Runlayer-User-Id"] == "fresh"
        assert headers["X-Runlayer-Subject-Type"] == "user"
        assert headers["X-Runlayer-Custom-Foo"] == "keep"

    def test_unapplied_bundle_still_strips_stale_reserved_headers(self) -> None:
        headers = {
            "X-Runlayer-User-Id": "stale",
            "X-Runlayer-Identity-Token": "stale",
            "X-Other": "keep",
        }
        idf.merge_bundle_into_headers(headers, IdentityForwardBundle())
        assert "X-Runlayer-User-Id" not in headers
        assert "X-Runlayer-Identity-Token" not in headers
        assert headers["X-Other"] == "keep"

    def test_none_bundle_still_strips_stale_reserved_headers(self) -> None:
        headers = {"X-Runlayer-User-Id": "stale", "X-Other": "keep"}
        idf.merge_bundle_into_headers(headers, None)
        assert "X-Runlayer-User-Id" not in headers
        assert headers["X-Other"] == "keep"

    def test_case_insensitive_strip(self) -> None:
        headers = {"x-runlayer-user-id": "stale"}
        idf.merge_bundle_into_headers(headers, None)
        assert headers == {}


class TestRefreshLoop:
    def test_returns_immediately_when_bundle_unapplied(self) -> None:
        client = MagicMock(spec=RunlayerClient)
        headers: dict[str, str] = {}

        anyio.run(
            idf.refresh_loop,
            client,
            "sid",
            IdentityForwardBundle(),
            headers,
        )

        client.get_server_details.assert_not_called()
        assert headers == {}

    def test_returns_immediately_when_expires_at_none(self) -> None:
        client = MagicMock(spec=RunlayerClient)
        headers = {"X-Runlayer-Subject-Type": "user"}

        anyio.run(
            idf.refresh_loop,
            client,
            "sid",
            IdentityForwardBundle(
                headers={"X-Runlayer-Subject-Type": "user"},
                expires_at=None,
                applied=True,
            ),
            headers,
        )

        client.get_server_details.assert_not_called()

    def test_replaces_token_and_stops_on_downgrade(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Refresh returns a details read with no bundle (admin turned the
        toggle off mid-session) ⇒ stale headers are stripped and the loop
        stops. Verifies both the mutation contract and the downgrade path."""

        # Skip real sleeps — the loop should perform exactly one refresh
        # before the downgrade breaks it out.
        async def _no_sleep(*_a, **_kw) -> None:
            return None

        monkeypatch.setattr(anyio, "sleep", _no_sleep)

        client = MagicMock(spec=RunlayerClient)
        now = int(time.time())
        client.get_server_details.return_value = _details(None)
        headers: dict[str, str] = {"X-Runlayer-Identity-Token": "old-token"}

        anyio.run(
            idf.refresh_loop,
            client,
            "sid",
            IdentityForwardBundle(
                headers={"X-Runlayer-Identity-Token": "old-token"},
                expires_at=now + 30,
                applied=True,
            ),
            headers,
        )

        assert client.get_server_details.call_count == 1
        # Downgrade ⇒ reserved headers are stripped and nothing new injected.
        assert "X-Runlayer-Identity-Token" not in headers

    def test_replaces_token_with_fresh_mint(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A signed refresh swaps the token in the shared dict, then the
        following downgrade read ends the loop."""

        async def _no_sleep(*_a, **_kw) -> None:
            return None

        monkeypatch.setattr(anyio, "sleep", _no_sleep)

        client = MagicMock(spec=RunlayerClient)
        now = int(time.time())
        fresh = IdentityForwardBundle(
            headers={"X-Runlayer-Identity-Token": "new-token"},
            expires_at=now + 300,
            applied=True,
        )
        seen_tokens: list[str | None] = []
        headers: dict[str, str] = {"X-Runlayer-Identity-Token": "old-token"}

        def _reads(_server_id: str) -> ServerDetails:
            seen_tokens.append(headers.get("X-Runlayer-Identity-Token"))
            return _details(fresh) if len(seen_tokens) == 1 else _details(None)

        client.get_server_details.side_effect = _reads

        anyio.run(
            idf.refresh_loop,
            client,
            "sid",
            IdentityForwardBundle(
                headers={"X-Runlayer-Identity-Token": "old-token"},
                expires_at=now + 30,
                applied=True,
            ),
            headers,
        )

        # First read saw the old token still in place; the second read
        # (post-swap) saw the fresh one before the downgrade cleared it.
        assert seen_tokens == ["old-token", "new-token"]
        assert "X-Runlayer-Identity-Token" not in headers

    def test_survives_non_http_fetch_errors(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A malformed backend response raises from ``model_validate``, not
        httpx — the loop must retry it like any other fetch failure instead
        of escaping and killing the proxy's task group."""

        async def _no_sleep(*_a, **_kw) -> None:
            return None

        monkeypatch.setattr(anyio, "sleep", _no_sleep)

        client = MagicMock(spec=RunlayerClient)
        now = int(time.time())
        client.get_server_details.side_effect = [
            RuntimeError("malformed response"),
            _details(None),  # no bundle ⇒ loop stops after retry
        ]
        headers: dict[str, str] = {"X-Runlayer-Identity-Token": "old-token"}

        anyio.run(
            idf.refresh_loop,
            client,
            "sid",
            IdentityForwardBundle(
                headers={"X-Runlayer-Identity-Token": "old-token"},
                expires_at=now + 30,
                applied=True,
            ),
            headers,
        )

        assert client.get_server_details.call_count == 2


def test_run_verified_proxy_wires_identity_forward(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``run_proxy`` schedules the refresher inside its anyio scope."""

    from runlayer_cli.verified_local_proxy import proxy as vlp

    monkeypatch.setattr(vlp, "wait_for_target", lambda *a, **k: None)
    monkeypatch.setattr(vlp, "verify_target", lambda *a, **k: None)

    fake_proxy = SimpleNamespace(run_stdio_async=MagicMock())

    async def _run_stdio(**_kw) -> None:
        # Give the refresher a chance to fire before the proxy exits.
        await anyio.sleep(0)

    fake_proxy.run_stdio_async = _run_stdio  # type: ignore[assignment]
    monkeypatch.setattr(vlp, "create_proxy", lambda *a, **k: fake_proxy)

    refresh_calls = 0

    async def _refresher() -> None:
        nonlocal refresh_calls
        refresh_calls += 1
        # Sleep forever; cancellation from the task group will unblock us.
        await anyio.sleep(3600)

    config = SimpleNamespace(
        reverify_interval_seconds=None,
        wait_for_target=False,
        display_name="test",
    )
    vlp.run_proxy(
        config,  # type: ignore[arg-type]
        skip_verification=True,
        identity_forward_headers={"X-Runlayer-Subject-Type": "user"},
        identity_forward_refresher=_refresher,
    )

    assert refresh_calls == 1
