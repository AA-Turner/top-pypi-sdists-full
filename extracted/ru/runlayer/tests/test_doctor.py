"""Tests for `runlayer doctor` (read-only OAuth/connectivity preflight)."""

from __future__ import annotations

import io
import json
import socket
import sys
from typing import Any, Callable
from unittest.mock import MagicMock, patch

import anyio
import httpx
import pytest
from typer.testing import CliRunner

from runlayer_cli.commands.doctor import (
    CheckResult,
    _issuer_matches,
    as_metadata_candidates,
    base_url_of,
    callback_port_check,
    check_registration_endpoint,
    check_resource_match,
    effective_callback_port,
    issuer_from_prm,
    manual_oauth_checks,
    print_results,
    prm_candidates,
    redact_url,
    resource_metadata_from_www_authenticate,
    run_network_checks,
    run_verified_local_checks,
)
from runlayer_cli.main import app
from runlayer_cli.models import ServerDetails

runner = CliRunner()

SERVER_URL = "https://mcp.example.com/mcp"
SERVER_ID = "12345678-1234-1234-1234-123456789012"


def make_server(**overrides: Any) -> ServerDetails:
    payload: dict[str, Any] = {
        "id": SERVER_ID,
        "name": "Example MCP",
        "url": SERVER_URL,
        "transport_type": "streaming-http",
        "deployment_mode": "LOCAL",
    }
    payload.update(overrides)
    return ServerDetails.model_validate(payload)


def factory_for(
    handler: Callable[[httpx.Request], httpx.Response],
) -> Callable[[dict[str, str]], httpx.AsyncClient]:
    return lambda headers: httpx.AsyncClient(
        transport=httpx.MockTransport(handler), headers=headers
    )


def run_checks(
    server: ServerDetails,
    handler: Callable[[httpx.Request], httpx.Response],
    flag_port: int | None = None,
    cached_port: int | None = None,
):
    return anyio.run(
        lambda: run_network_checks(
            server,
            flag_port,
            client_factory=factory_for(handler),
            cached_port_lookup=lambda _url: cached_port,
        )
    )


INITIALIZE_RESULT = {
    "protocolVersion": "2025-03-26",
    "capabilities": {},
    "serverInfo": {"name": "fake-server", "version": "1.0.0"},
}


def mcp_ok_response() -> httpx.Response:
    """A 2xx initialize reply with a valid MCP InitializeResult."""
    return httpx.Response(
        200, json={"jsonrpc": "2.0", "id": 0, "result": INITIALIZE_RESULT}
    )


def sse_endpoint_response() -> httpx.Response:
    """A 2xx SSE stream whose first event is the MCP `endpoint` event."""
    return httpx.Response(
        200,
        headers={"content-type": "text/event-stream"},
        content=b"event: endpoint\ndata: /messages/?session_id=abc\n\n",
    )


def by_title(results, title):
    matches = [r for r in results if r.title == title]
    assert matches, f"no result titled {title!r} in {[r.title for r in results]}"
    return matches[0]


class TestUrlHelpers:
    def test_base_url_strips_query_and_fragment(self):
        assert (
            base_url_of("https://mcp.example.com/mcp?x=1#f")
            == "https://mcp.example.com/mcp"
        )

    def test_prm_candidates_path_appended_then_root(self):
        assert prm_candidates("https://mcp.example.com/mcp/") == [
            "https://mcp.example.com/.well-known/oauth-protected-resource/mcp",
            "https://mcp.example.com/.well-known/oauth-protected-resource",
        ]

    def test_prm_candidates_root_url_only_root(self):
        assert prm_candidates("https://mcp.example.com/") == [
            "https://mcp.example.com/.well-known/oauth-protected-resource",
        ]

    def test_as_metadata_candidates_with_path(self):
        candidates = as_metadata_candidates("https://idp.example.com/oauth2/abc")
        assert candidates == [
            "https://idp.example.com/.well-known/oauth-authorization-server/oauth2/abc",
            "https://idp.example.com/oauth2/abc/.well-known/oauth-authorization-server",
            "https://idp.example.com/.well-known/openid-configuration/oauth2/abc",
            "https://idp.example.com/oauth2/abc/.well-known/openid-configuration",
        ]

    def test_as_metadata_candidates_without_path_dedupes(self):
        candidates = as_metadata_candidates("https://idp.example.com")
        assert candidates == [
            "https://idp.example.com/.well-known/oauth-authorization-server",
            "https://idp.example.com/.well-known/openid-configuration",
        ]

    def test_issuer_from_prm_prefers_authorization_servers(self):
        issuer, from_prm = issuer_from_prm(
            {"authorization_servers": ["https://idp.example.com"]}, SERVER_URL
        )
        assert issuer == "https://idp.example.com"
        assert from_prm is True

    def test_issuer_falls_back_to_server_origin(self):
        issuer, from_prm = issuer_from_prm(None, SERVER_URL)
        assert issuer == "https://mcp.example.com"
        assert from_prm is False


class TestWwwAuthenticateParsing:
    def test_quoted_resource_metadata(self):
        header = (
            'Bearer realm="mcp", resource_metadata="https://mcp.example.com/custom/prm"'
        )
        assert (
            resource_metadata_from_www_authenticate(header)
            == "https://mcp.example.com/custom/prm"
        )

    def test_unquoted_resource_metadata(self):
        header = "Bearer resource_metadata=https://mcp.example.com/prm, realm=x"
        assert (
            resource_metadata_from_www_authenticate(header)
            == "https://mcp.example.com/prm"
        )

    def test_absent_parameter(self):
        assert resource_metadata_from_www_authenticate('Bearer realm="mcp"') is None

    def test_missing_header(self):
        assert resource_metadata_from_www_authenticate(None) is None
        assert resource_metadata_from_www_authenticate("") is None


class TestUrlRedaction:
    def test_query_values_masked_keys_kept(self):
        assert (
            redact_url("https://api.tinybird.co/mcp?token=SECRET123&x=1")
            == "https://api.tinybird.co/mcp?token=***&x=***"
        )

    def test_userinfo_stripped(self):
        assert (
            redact_url("https://alice:hunter2@mcp.example.com/mcp")
            == "https://mcp.example.com/mcp"
        )

    def test_fragment_dropped(self):
        assert redact_url("https://mcp.example.com/mcp#frag") == (
            "https://mcp.example.com/mcp"
        )

    def test_plain_url_unchanged(self):
        assert redact_url(SERVER_URL) == SERVER_URL

    def test_bare_query_component_masked(self):
        # `?SECRET_TOKEN` with no `=` is as much a credential as a keyed one.
        assert (
            redact_url("https://mcp.example.com/mcp?SECRET_TOKEN")
            == "https://mcp.example.com/mcp?***"
        )
        assert (
            redact_url("https://mcp.example.com/mcp?BARE&k=v")
            == "https://mcp.example.com/mcp?***&k=***"
        )

    def test_unparseable_url_never_returns_raw_input(self):
        # urlsplit raises on this (invalid IPv6 bracket); the fallback must
        # still strip userinfo and query secrets, never echo the input.
        malformed = "https://user:pass@[bad?token=secret"
        redacted = redact_url(malformed)
        assert "user:pass" not in redacted
        assert "token=secret" not in redacted
        assert "secret" not in redacted

    def test_unparseable_url_caps_length(self):
        malformed = "https://[bad/" + "a" * 500
        assert len(redact_url(malformed)) <= 200


class TestResourceMatch:
    def test_exact_match_ok(self):
        result = check_resource_match({"resource": SERVER_URL}, SERVER_URL)
        assert result.status == "ok"

    def test_mismatch_fails_and_prints_both_values(self):
        result = check_resource_match(
            {"resource": "https://mcp.example.com/mcp/"}, SERVER_URL
        )
        assert result.status == "fail"
        assert "https://mcp.example.com/mcp/" in result.detail
        assert SERVER_URL in result.detail

    def test_trailing_slash_difference_is_a_mismatch(self):
        result = check_resource_match({"resource": SERVER_URL + "/"}, SERVER_URL)
        assert result.status == "fail"

    def test_missing_resource_field_warns(self):
        result = check_resource_match({}, SERVER_URL)
        assert result.status == "warn"


class TestCallbackPort:
    def test_flag_beats_server_configured(self):
        server = make_server(
            requires_manual_oauth_setup=True,
            manual_oauth_client_id="cid",
            manual_oauth_callback_port=9000,
        )
        port, source = effective_callback_port(server, 8000, 7000)
        assert port == 8000
        assert "flag" in source

    def test_server_configured_beats_cached(self):
        server = make_server(
            requires_manual_oauth_setup=True,
            manual_oauth_client_id="cid",
            manual_oauth_callback_port=9000,
        )
        port, source = effective_callback_port(server, None, 7000)
        assert port == 9000
        assert "server" in source

    def test_server_port_ignored_without_manual_oauth(self):
        # Mirrors `runlayer run`: a stale stored port must not constrain
        # DCR/broker flows after the server leaves manual registration.
        server = make_server(manual_oauth_callback_port=9000)
        port, _source = effective_callback_port(server, None, None)
        assert port is None

    def test_cached_beats_random(self):
        server = make_server()
        port, source = effective_callback_port(server, None, 7000)
        assert port == 7000
        assert "cached" in source

    def _manual_server(self) -> ServerDetails:
        return make_server(
            requires_manual_oauth_setup=True, manual_oauth_client_id="cid"
        )

    def test_manual_random_port_warns_about_exact_redirect_matching(self):
        result = callback_port_check(self._manual_server(), None, None)
        assert result.status == "warn"
        assert "exact redirect-URI matching" in result.detail
        assert result.remedy is not None

    def test_dcr_random_port_is_informational_not_warning(self):
        # DCR registers the exact chosen redirect URI (port included), so
        # exact matching is satisfied by construction on the first run.
        result = callback_port_check(make_server(), None, None)
        assert result.status == "ok"
        assert "dynamic client registration" in result.detail
        assert result.remedy is None

    def test_manual_fixed_port_reports_redirect_uri(self):
        result = callback_port_check(self._manual_server(), 8123, None)
        assert result.status == "ok"
        assert "http://localhost:8123/callback" in result.detail

    def test_dcr_fixed_port_reports_port_without_idp_guidance(self):
        result = callback_port_check(make_server(), 8123, None)
        assert result.status == "ok"
        assert "8123" in result.detail
        assert "redirect-URI allowlist" not in result.detail

    def test_fixed_port_already_in_use_warns(self):
        # `runlayer run` refuses to start when another process owns the
        # fixed port (_ensure_callback_port_available); mirror the rule.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            try:
                listener.bind(("127.0.0.1", 0))
            except PermissionError as exc:
                pytest.skip(f"Loopback bind unavailable in this environment: {exc}")
            listener.listen(1)
            port = listener.getsockname()[1]
            result = callback_port_check(self._manual_server(), port, None)
        assert result.status == "warn"
        assert f"callback port {port} is already in use" in result.detail
        assert "close the conflicting process" in (result.remedy or "")


class TestManualOAuthChecks:
    def test_manual_without_client_id_fails(self):
        results = manual_oauth_checks(
            make_server(requires_manual_oauth_setup=True), None
        )
        manual = by_title(results, "Manual OAuth configuration")
        assert manual.status == "fail"

    def test_manual_client_ignored_when_flag_off_warns(self):
        results = manual_oauth_checks(make_server(manual_oauth_client_id="cid"), None)
        manual = by_title(results, "Manual OAuth configuration")
        assert manual.status == "warn"
        assert "IGNORED" in manual.detail

    def test_not_manual_no_client_ok(self):
        results = manual_oauth_checks(make_server(), None)
        manual = by_title(results, "Manual OAuth configuration")
        assert manual.status == "ok"

    def test_least_privilege_scope_subset_is_ok(self):
        # scopes_supported is what the resource supports, not what every
        # client must request; a subset must pass.
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
                manual_oauth_scopes="read:jira-work",
            ),
            {"scopes_supported": ["read:jira-work", "offline_access", "write:x"]},
        )
        scopes = by_title(results, "OAuth scopes")
        assert scopes.status == "ok"
        # Unrequested advertised scopes are listed as info only.
        assert "offline_access" in scopes.detail
        assert "write:x" in scopes.detail
        assert scopes.remedy is None

    def test_configured_scope_not_advertised_warns(self):
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
                manual_oauth_scopes="read made-up-scope",
            ),
            {"scopes_supported": ["read", "write"]},
        )
        scopes = by_title(results, "OAuth scopes")
        assert scopes.status == "warn"
        assert "made-up-scope" in scopes.detail
        assert "read," not in scopes.detail

    def test_empty_configured_scopes_with_advertised_hints(self):
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
            ),
            {"scopes_supported": ["read", "write"]},
        )
        scopes = by_title(results, "OAuth scopes")
        assert scopes.status == "warn"
        assert "read" in scopes.detail
        assert "write" in scopes.detail

    def test_all_advertised_scopes_configured_ok(self):
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
                manual_oauth_scopes="a b",
            ),
            {"scopes_supported": ["a", "b"]},
        )
        assert by_title(results, "OAuth scopes").status == "ok"

    def test_secretless_confidential_method_warns_about_runtime_override(self):
        # OAuth.__init__ overrides a confidential preference to "none" when
        # the secret is absent, so `runlayer run` still authenticates — this
        # is a stale-config heads-up, not a failure prediction.
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
                preferred_token_endpoint_auth_method="client_secret_post",
            ),
            None,
        )
        secret = by_title(results, "Client secret vs token auth method")
        assert secret.status == "warn"
        assert "client_secret_post" in secret.detail
        assert "overridden to 'none' at runtime" in secret.detail

    def test_empty_string_secret_classifies_as_absent(self):
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
                manual_oauth_client_secret="",
                preferred_token_endpoint_auth_method="client_secret_basic",
            ),
            None,
        )
        secret = by_title(results, "Client secret vs token auth method")
        assert secret.status == "warn"
        assert "overridden to 'none' at runtime" in secret.detail

    def test_secretless_public_client_ok(self):
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
                preferred_token_endpoint_auth_method="none",
            ),
            None,
        )
        assert by_title(results, "Client secret vs token auth method").status == "ok"

    def test_confidential_with_secret_ok(self):
        results = manual_oauth_checks(
            make_server(
                requires_manual_oauth_setup=True,
                manual_oauth_client_id="cid",
                manual_oauth_client_secret="shh",
                preferred_token_endpoint_auth_method="client_secret_post",
            ),
            None,
        )
        assert by_title(results, "Client secret vs token auth method").status == "ok"

    def _confidential_server(self, method: str | None = None) -> ServerDetails:
        return make_server(
            requires_manual_oauth_setup=True,
            manual_oauth_client_id="cid",
            manual_oauth_client_secret="shh",
            preferred_token_endpoint_auth_method=method,
        )

    def test_resolved_method_unsupported_by_as_fails_naming_both(self):
        # No stored preference -> runtime resolves to client_secret_post
        # (OAuth.__init__ default), which this AS does not support.
        results = manual_oauth_checks(
            self._confidential_server(),
            None,
            {"token_endpoint_auth_methods_supported": ["client_secret_basic"]},
        )
        method = by_title(results, "Token endpoint auth method support")
        assert method.status == "fail"
        assert "client_secret_post" in method.detail
        assert "client_secret_basic" in method.detail

    def test_resolved_method_supported_by_as_ok(self):
        results = manual_oauth_checks(
            self._confidential_server("client_secret_basic"),
            None,
            {
                "token_endpoint_auth_methods_supported": [
                    "client_secret_basic",
                    "client_secret_post",
                ]
            },
        )
        assert by_title(results, "Token endpoint auth method support").status == "ok"

    def test_no_advertised_methods_no_support_check(self):
        results = manual_oauth_checks(
            self._confidential_server("client_secret_post"),
            None,
            {"issuer": "https://idp.example.com"},
        )
        titles = [r.title for r in results]
        assert "Token endpoint auth method support" not in titles

    def _public_server(self) -> ServerDetails:
        return make_server(
            requires_manual_oauth_setup=True,
            manual_oauth_client_id="cid",
        )

    def test_secretless_none_unsupported_by_as_fails(self):
        # Runtime resolves a secretless client to "none"; an AS advertising
        # only confidential methods fails the token exchange.
        results = manual_oauth_checks(
            self._public_server(),
            None,
            {
                "token_endpoint_auth_methods_supported": [
                    "client_secret_basic",
                    "client_secret_post",
                ]
            },
        )
        method = by_title(results, "Token endpoint auth method support")
        # Definite incompatibility: the token exchange cannot succeed, so
        # it must affect the exit code rather than only warn.
        assert method.status == "fail"
        assert "'none'" in method.detail
        assert "client_secret_basic" in method.detail

    def test_secretless_none_supported_by_as_ok(self):
        results = manual_oauth_checks(
            self._public_server(),
            None,
            {"token_endpoint_auth_methods_supported": ["none", "client_secret_basic"]},
        )
        assert by_title(results, "Token endpoint auth method support").status == "ok"

    def test_secretless_no_advertised_methods_no_support_check(self):
        results = manual_oauth_checks(
            self._public_server(),
            None,
            {"issuer": "https://idp.example.com"},
        )
        assert "Token endpoint auth method support" not in [r.title for r in results]


PRM_PATH = "/.well-known/oauth-protected-resource/mcp"
AS_META_PATH = "/.well-known/oauth-authorization-server"
# The endpoints the authorization-code flow needs at runtime; doctor fails
# AS metadata that lacks either, so complete fixtures carry both.
AS_ENDPOINTS = {
    "authorization_endpoint": "https://idp.example.com/authorize",
    "token_endpoint": "https://idp.example.com/token",
}


def healthy_handler(request: httpx.Request) -> httpx.Response:
    url = str(request.url)
    if url == SERVER_URL:
        return httpx.Response(401)
    if url == f"https://mcp.example.com{PRM_PATH}":
        return httpx.Response(
            200,
            json={
                "resource": SERVER_URL,
                "authorization_servers": ["https://idp.example.com"],
                "scopes_supported": ["read", "write"],
            },
        )
    if url == f"https://idp.example.com{AS_META_PATH}":
        return httpx.Response(
            200,
            json={
                "issuer": "https://idp.example.com",
                "registration_endpoint": "https://idp.example.com/register",
                **AS_ENDPOINTS,
            },
        )
    return httpx.Response(404)


class TestNetworkChecks:
    def test_healthy_dcr_server_all_ok(self):
        results = run_checks(make_server(), healthy_handler, flag_port=8123)
        assert all(r.status != "fail" for r in results)
        assert by_title(results, "Upstream reachability").status == "ok"
        assert (
            by_title(results, "Protected-resource metadata (RFC 9728)").status == "ok"
        )
        assert (
            by_title(results, "PRM `resource` matches configured URL (RFC 8707)").status
            == "ok"
        )
        assert by_title(results, "Authorization server metadata").status == "ok"

    def test_unreachable_host_fails_and_skips_discovery(self):
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("nodename nor servname provided", request=request)

        results = run_checks(make_server(), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "host unreachable from this machine (VPN?)" in reach.detail
        assert (
            by_title(results, "Protected-resource metadata (RFC 9728)").status == "skip"
        )
        assert by_title(results, "Authorization server metadata").status == "skip"

    def test_timeout_fails_reachability(self):
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectTimeout("timed out", request=request)

        results = run_checks(make_server(), handler)
        assert by_title(results, "Upstream reachability").status == "fail"

    def test_stale_url_404_fails(self):
        # The deciding initialize POST 404ing means the endpoint isn't
        # there — a hard failure under the transport decision table.
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "stale" in reach.detail

    def test_prm_root_fallback(self):
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == "https://mcp.example.com/.well-known/oauth-protected-resource":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200, json={"issuer": "https://idp.example.com", **AS_ENDPOINTS}
                )
            return httpx.Response(404)

        results = run_checks(
            make_server(manual_oauth_client_id="cid", requires_manual_oauth_setup=True),
            handler,
        )
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "ok"
        assert (
            "found at https://mcp.example.com/.well-known/oauth-protected-resource "
            "(well-known path)" in prm.detail
        )

    def test_resource_mismatch_fails_with_both_values(self):
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": "https://mcp.example.com/mcp/",
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        match = by_title(results, "PRM `resource` matches configured URL (RFC 8707)")
        assert match.status == "fail"
        assert "https://mcp.example.com/mcp/" in match.detail
        assert SERVER_URL in match.detail

    def test_no_registration_endpoint_without_manual_client_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                # Okta-style: metadata exists but no registration_endpoint.
                return httpx.Response(
                    200, json={"issuer": "https://idp.example.com", **AS_ENDPOINTS}
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        registration = by_title(results, "Authorization server metadata")
        assert registration.status == "fail"
        assert "pre-registered client" in (registration.remedy or "")

    def test_no_registration_endpoint_with_manual_client_ok(self):
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200, json={"issuer": "https://idp.example.com", **AS_ENDPOINTS}
                )
            return httpx.Response(404)

        results = run_checks(
            make_server(requires_manual_oauth_setup=True, manual_oauth_client_id="cid"),
            handler,
        )
        assert by_title(results, "Authorization server metadata").status == "ok"

    def test_no_registration_endpoint_with_ignored_manual_client_fails(self):
        # Leftover client id with the flag off: `runlayer run` will still
        # attempt DCR (main._oauth_for_server ignores the id), so doctor
        # must fail instead of treating the id as an active manual client.
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200, json={"issuer": "https://idp.example.com", **AS_ENDPOINTS}
                )
            return httpx.Response(404)

        results = run_checks(
            make_server(manual_oauth_client_id="cid"),
            handler,
        )
        registration = by_title(results, "Authorization server metadata")
        assert registration.status == "fail"
        assert "IGNORED" in registration.detail
        assert "enable Manual OAuth" in (registration.remedy or "")

    def test_advertised_prm_url_is_tried_first(self):
        # PRM served ONLY at the WWW-Authenticate-advertised URL; both
        # well-known candidates 404. Discovery must still succeed.
        advertised = "https://mcp.example.com/custom/prm-location"

        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": (f'Bearer resource_metadata="{advertised}"')
                    },
                )
            if url == advertised:
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "ok"
        assert advertised in prm.detail
        assert "advertised via WWW-Authenticate" in prm.detail
        assert all(r.status != "fail" for r in results)

    def test_post_only_server_passes_via_initialize_probe(self):
        # Streamable HTTP servers can 405 the GET and only advertise the
        # OAuth challenge on the protocol POST (Runlayer's backend proxy is
        # POST-only). Reachability and PRM discovery must still succeed.
        advertised = "https://mcp.example.com/post-only/prm"

        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(405)
                body = json.loads(request.content)
                assert body["method"] == "initialize"
                assert "text/event-stream" in request.headers.get("accept", "")
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": (f'Bearer resource_metadata="{advertised}"')
                    },
                )
            if url == advertised:
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "ok"
        assert "MCP initialize POST" in reach.detail
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "ok"
        assert advertised in prm.detail
        assert "advertised via WWW-Authenticate" in prm.detail
        assert all(r.status != "fail" for r in results)

    def test_identity_forward_headers_are_sent_on_probes(self):
        # `runlayer run` merges the identity_forward bundle into transport
        # headers; identity-gated upstreams reject a probe without them.
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return healthy_handler(request)

        server = make_server(
            identity_forward={
                "headers": {
                    "X-Runlayer-User-Email": "user@example.com",
                    "X-Runlayer-Subject-Type": "user",
                    "X-Runlayer-Identity-Token": "signed-token",
                },
                "applied": True,
            }
        )
        run_checks(server, handler)

        upstream = [r for r in requests if str(r.url) == SERVER_URL]
        assert upstream, "expected upstream probes"
        for request in upstream:
            assert request.headers.get("x-runlayer-user-email") == "user@example.com"
            assert request.headers.get("x-runlayer-subject-type") == "user"
            assert request.headers.get("x-runlayer-identity-token") == "signed-token"
            assert "Runlayer CLI" in request.headers.get("user-agent", "")

    def test_identity_headers_never_reach_discovery_or_idp(self):
        # Hard contract: the bundle (incl. X-Runlayer-Identity-Token — a
        # short-lived token plus user/org PII) is scoped to server.url
        # exactly like `runlayer run`'s transport; PRM and authorization-
        # server metadata fetches must go out with just the User-Agent.
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return healthy_handler(request)

        server = make_server(
            identity_forward={
                "headers": {
                    "X-Runlayer-User-Email": "user@example.com",
                    "X-Runlayer-Identity-Token": "signed-token",
                },
                "applied": True,
            }
        )
        run_checks(server, handler)

        discovery = [r for r in requests if str(r.url) != SERVER_URL]
        assert discovery, "expected PRM/AS metadata fetches"
        for request in discovery:
            leaked = [
                name
                for name in request.headers
                if name.lower().startswith("x-runlayer-")
            ]
            assert not leaked, f"identity headers leaked to {request.url}: {leaked}"

    def _prm_and_as_handler(self, advertised: str):
        """Handler for PRM at `advertised` + AS metadata with DCR."""

        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == advertised:
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        return handler

    def test_streaming_http_get_ok_post_405_fails_as_sse_misconfig(self):
        # The runtime initializes streaming-http via POST; a URL that
        # answers GET but 405s the POST is the classic SSE-URL-configured-
        # as-streaming-http misconfig, not a pass.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(405)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "is this an SSE endpoint configured as Streaming HTTP?" in reach.detail

    def test_streaming_http_post_timeout_warns_naming_post(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                raise httpx.ConnectTimeout("initialize timed out", request=request)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "warn"
        assert "MCP initialize POST failed" in reach.detail

    def test_sse_get_ok_post_dead_passes(self):
        # For sse the runtime connects with the streamed GET; a dead POST
        # is irrelevant.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return sse_endpoint_response()
                raise httpx.ConnectTimeout("no POST here", request=request)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        assert by_title(results, "Upstream reachability").status == "ok"

    def test_sse_content_negotiating_server_passes(self):
        # SSETransport (via httpx-sse) sends Accept: text/event-stream; a
        # content-negotiating server serves the stream ONLY when asked.
        # The deciding GET must send the same Accept or it false-fails.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                if "text/event-stream" in request.headers.get("accept", ""):
                    return sse_endpoint_response()
                return httpx.Response(
                    200,
                    headers={"content-type": "text/html"},
                    content=b"<html><body>docs page</body></html>",
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        assert by_title(results, "Upstream reachability").status == "ok"

    def test_sse_html_200_fails_as_not_event_stream(self):
        # Symmetric with the streaming-http MCP-speak check: a 2xx GET
        # that isn't an event stream is any web page, not SSE.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(
                    200,
                    headers={"content-type": "text/html; charset=utf-8"},
                    content=b"<html><body>Welcome</body></html>",
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "is not an event stream" in reach.detail
        assert "text/html" in reach.detail
        assert "is this actually an SSE MCP endpoint?" in reach.detail

    def test_malformed_advertised_url_does_not_traceback(self):
        # urlparse/urljoin raise on an unclosed IPv6 literal; that must be
        # classified as a malformed advertisement, not escape as a crash.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": 'Bearer resource_metadata="https://[bad"'
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "fail"
        assert "malformed" in prm.detail.lower()

    def test_relative_advertised_prm_joins_mcp_url(self):
        # Mirrors the backend wire-discovery pin: a relative
        # resource_metadata reference joins the MCP URL, and the PRM
        # document exists ONLY at that custom location.
        relative = "/.well-known/oauth-protected-resource/custom-spot"
        joined = f"https://mcp.example.com{relative}"
        fetched: list[str] = []

        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            fetched.append(url)
            if url == SERVER_URL:
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": f'Bearer resource_metadata="{relative}"'
                    },
                )
            if url == joined:
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "ok"
        assert joined in prm.detail
        assert "advertised via WWW-Authenticate" in prm.detail
        # The advertised URL won — the path-based fallback never fetched.
        assert f"https://mcp.example.com{PRM_PATH}" not in fetched
        assert all(r.status != "fail" for r in results)

    def test_streaming_http_post_200_jsonrpc_passes(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return mcp_ok_response()
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "ok"
        assert "HTTP 200 from the MCP initialize POST" in reach.detail

    def test_streaming_http_get_reset_post_401_still_reachable(self):
        # A GET that resets/times out must not preempt the POST — the POST
        # is the operation the runtime actually performs.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    raise httpx.ConnectError(
                        "connection reset by peer", request=request
                    )
                return httpx.Response(401)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "ok"
        assert "GET failed" in reach.detail
        assert "MCP initialize POST 401" in reach.detail

    def test_streaming_http_get_failed_post_405_no_sse_misconfig_claim(self):
        # "URL answers GET" must be true before suggesting the SSE
        # misconfig; a failed GET + POST 405 is a wrong/stale endpoint.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    raise httpx.ConnectError(
                        "connection reset by peer", request=request
                    )
                return httpx.Response(405)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "rejects the MCP initialize POST (405)" in reach.detail
        assert "GET failed" in reach.detail
        assert "likely wrong URL or stale endpoint" in reach.detail
        assert "SSE endpoint configured as Streaming HTTP" not in reach.detail
        assert "switch the server's transport" not in (reach.remedy or "")

    def test_streaming_http_jsonrpc_error_fails_quoting_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200,
                    json={
                        "jsonrpc": "2.0",
                        "id": 0,
                        "error": {"code": -32600, "message": "invalid request"},
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "JSON-RPC error" in reach.detail
        assert "-32600" in reach.detail
        assert "invalid request" in reach.detail

    def test_streaming_http_wrong_id_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200, json={"jsonrpc": "2.0", "id": 99, "result": {}}
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "not a JSON-RPC initialize reply" in reach.detail

    def test_streaming_http_jsonrpc_literal_in_garbage_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200,
                    headers={"content-type": "application/json"},
                    content=b'garbage "jsonrpc" garbage',
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "not a JSON-RPC initialize reply" in reach.detail

    def test_streaming_http_html_200_fails_as_not_mcp(self):
        # Any web handler can 200 an unknown POST with an HTML page; the
        # body/content-type must prove MCP, not just the status.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200,
                    headers={"content-type": "text/html; charset=utf-8"},
                    content=b"<html><body>Welcome</body></html>",
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "not speaking MCP" in reach.detail
        assert "text/html" in reach.detail

    def test_streaming_http_sse_initialize_frame_passes(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                frame = json.dumps(
                    {"jsonrpc": "2.0", "id": 0, "result": INITIALIZE_RESULT}
                )
                return httpx.Response(
                    200,
                    headers={"content-type": "text/event-stream"},
                    content=f"event: message\ndata: {frame}\n\n".encode(),
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        assert by_title(results, "Upstream reachability").status == "ok"

    def test_streaming_http_empty_result_fails_as_incomplete(self):
        # `result: {}` is not an InitializeResult; the runtime's typed
        # parsing would reject it.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200, json={"jsonrpc": "2.0", "id": 0, "result": {}}
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "protocolVersion" in reach.detail
        assert "Field required" in reach.detail
        assert "InitializeResult" in reach.detail

    def test_streaming_http_large_valid_initialize_passes(self):
        # A valid reply larger than the old 4KiB cap must not be truncated
        # mid-JSON into a false failure.
        big_result = {**INITIALIZE_RESULT, "instructions": "x" * 10240}

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200, json={"jsonrpc": "2.0", "id": 0, "result": big_result}
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        assert by_title(results, "Upstream reachability").status == "ok"

    def test_streaming_http_non_string_protocol_version_fails(self):
        # `protocolVersion: null` has the key but the typed InitializeResult
        # requires a string; presence-only would pass a broken endpoint.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200,
                    json={
                        "jsonrpc": "2.0",
                        "id": 0,
                        "result": {**INITIALIZE_RESULT, "protocolVersion": None},
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "protocolVersion" in reach.detail

    def test_streaming_http_complete_but_oversized_reply_warns(self):
        # A single chunk can be both complete and over the cap; the body is
        # truncated to the cap afterwards, so breaking on "complete" first
        # would hand the classifier a mid-document slice and hard-fail a
        # working endpoint instead of warning about size.
        big_result = {**INITIALIZE_RESULT, "instructions": "x" * 70000}

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200, json={"jsonrpc": "2.0", "id": 0, "result": big_result}
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "warn"
        assert "exceeds" in reach.detail

    def test_streaming_http_over_cap_garbage_warns_with_explicit_message(self):
        # Cap genuinely hit without a complete document — ambiguous, not
        # provably invalid.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200,
                    headers={"content-type": "application/json"},
                    content=b"[" + b'"x",' * 30000,  # never-closing JSON
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "warn"
        assert "exceeds" in reach.detail
        assert "without a complete JSON document" in reach.detail

    def test_sse_unrelated_first_event_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(
                    200,
                    headers={"content-type": "text/event-stream"},
                    content=b'event: ticker\ndata: {"price": 1}\n\n',
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "'ticker'" in reach.detail
        assert "unrelated event feed" in reach.detail

    def test_sse_stream_ends_without_endpoint_event_warns(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(
                    200,
                    headers={"content-type": "text/event-stream"},
                    content=b": hello\n\n",  # comment-only, then stream ends
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "warn"
        assert "no MCP endpoint event received" in reach.detail

    def test_sse_endpoint_event_empty_data_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(
                    200,
                    headers={"content-type": "text/event-stream"},
                    content=b"event: endpoint\ndata:\n\n",
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "endpoint event carries an unusable POST URL" in reach.detail

    def test_sse_endpoint_event_garbage_data_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(
                    200,
                    headers={"content-type": "text/event-stream"},
                    content=b"event: endpoint\ndata: http://[bad\n\n",
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "endpoint event carries an unusable POST URL" in reach.detail

    def test_sse_endpoint_event_cross_origin_fails(self):
        # Mirrors the mcp sse client: endpoint origin must equal the
        # connection origin or it raises.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(
                    200,
                    headers={"content-type": "text/event-stream"},
                    content=(
                        b"event: endpoint\ndata: https://other.example.com/messages\n\n"
                    ),
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "endpoint event carries an unusable POST URL" in reach.detail

    def test_as_metadata_missing_issuer_doc_skipped_for_next_candidate(self):
        # RFC 8414 requires `issuer`; an invalid candidate document must
        # not stop discovery — the next well-known location is tried.
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                # Missing issuer -> must be skipped.
                return httpx.Response(
                    200,
                    json={
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            if url == "https://idp.example.com/.well-known/openid-configuration":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        registration = by_title(results, "Authorization server metadata")
        assert registration.status == "ok"
        assert "openid-configuration" in registration.detail

    def test_as_metadata_wrong_issuer_doc_skipped_for_next_candidate(self):
        # A usable-but-wrong issuer is invalid for SELECTION: it must not
        # preempt a later candidate declaring the expected issuer.
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                # Wrong (cross-tenant) issuer -> must be skipped.
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com/other-tenant",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            if url == "https://idp.example.com/.well-known/openid-configuration":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        registration = by_title(results, "Authorization server metadata")
        assert registration.status == "ok"
        assert "openid-configuration" in registration.detail

    def test_as_metadata_all_candidates_mismatched_reports_not_found(self):
        # Every candidate declaring a wrong issuer is skipped by the ladder
        # (they can never be used), so the outcome is "no usable metadata"
        # rather than a mismatch report on a document we rejected.
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://evil.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        registration = by_title(results, "Authorization server metadata")
        # Not-found (warn) rather than a mismatch report: the wrong-issuer
        # documents were never selectable, and doctor can't prove the flow
        # fails outright — it only knows it found nothing usable.
        assert registration.status == "warn"
        assert "evil.example.com" not in registration.detail

    def test_streaming_http_multiline_sse_data_initialize_passes(self):
        # SSE semantics: multiple data: lines join with newlines; a valid
        # reply split across lines must not fail the classifier.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                payload = json.dumps(
                    {"jsonrpc": "2.0", "id": 0, "result": INITIALIZE_RESULT},
                    indent=2,
                )
                assert len(payload.splitlines()) > 2
                data_lines = "".join(f"data: {line}\n" for line in payload.splitlines())
                content = f"event: message\n{data_lines}\n"
                return httpx.Response(
                    200,
                    headers={"content-type": "text/event-stream"},
                    content=content.encode(),
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        assert by_title(results, "Upstream reachability").status == "ok"

    def test_streaming_http_empty_serverinfo_fails_naming_field(self):
        # The typed Implementation model requires name and version.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    200,
                    json={
                        "jsonrpc": "2.0",
                        "id": 0,
                        "result": {
                            "protocolVersion": "2025-03-26",
                            "capabilities": {},
                            "serverInfo": {},
                        },
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "serverInfo.name" in reach.detail

    def test_prm_with_invalid_server_url_continues_ladder(self):
        # authorization_servers elements must be usable URLs; a doc listing
        # "not-a-url" must not be selected over a later valid candidate.
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={"resource": SERVER_URL, "authorization_servers": ["not-a-url"]},
                )
            if url == "https://mcp.example.com/.well-known/oauth-protected-resource":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        assert by_title(results, "Protected-resource metadata (RFC 9728)").status == "ok"
        assert by_title(results, "Authorization server metadata").status == "ok"

    def test_initialize_uses_sdk_protocol_version(self):
        # A pinned literal drifts as the SDK moves; the probe must send
        # whatever version the installed SDK negotiates with.
        from mcp.types import LATEST_PROTOCOL_VERSION

        seen: dict[str, Any] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "POST":
                seen.update(json.loads(request.content))
                return mcp_ok_response()
            if str(request.url) == SERVER_URL:
                return httpx.Response(200)
            return httpx.Response(404)

        run_checks(make_server(transport_type="streaming-http"), handler)
        assert seen["params"]["protocolVersion"] == LATEST_PROTOCOL_VERSION

    def test_initialize_terminates_allocated_session(self):
        # A stateful server allocates a session for the probe; doctor must
        # release it instead of accumulating abandoned sessions.
        deletes: list[str] = []

        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "DELETE":
                deletes.append(request.headers.get("mcp-session-id", ""))
                return httpx.Response(200)
            if str(request.url) == SERVER_URL and request.method == "POST":
                resp = mcp_ok_response()
                resp.headers["mcp-session-id"] = "sess-123"
                return resp
            if str(request.url) == SERVER_URL:
                return httpx.Response(200)
            return httpx.Response(404)

        run_checks(make_server(transport_type="streaming-http"), handler)
        assert deletes == ["sess-123"]

    def test_as_metadata_malformed_optional_field_continues_ladder(self):
        # A malformed OPTIONAL field makes the runtime's OAuthMetadata
        # reject the document, so it must not preempt a valid candidate.
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        # string instead of a list -> OAuthMetadata rejects
                        "token_endpoint_auth_methods_supported": "none",
                        **AS_ENDPOINTS,
                    },
                )
            if url == "https://idp.example.com/.well-known/openid-configuration":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        registration = by_title(results, "Authorization server metadata")
        assert registration.status == "ok"
        assert "openid-configuration" in registration.detail

    def test_401_without_any_metadata_fails(self):
        # The upstream demands auth but publishes no RFC 9728 metadata:
        # the OAuth flow has nothing to discover, so this is broken.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                return httpx.Response(401)
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "fail"
        assert "OAuth cannot start" in prm.detail

    def test_session_delete_carries_protocol_version(self):
        from mcp.types import LATEST_PROTOCOL_VERSION

        seen: dict[str, str] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "DELETE":
                seen.update(dict(request.headers))
                return httpx.Response(200)
            if str(request.url) == SERVER_URL and request.method == "POST":
                resp = mcp_ok_response()
                resp.headers["mcp-session-id"] = "sess-abc"
                return resp
            if str(request.url) == SERVER_URL:
                return httpx.Response(200)
            return httpx.Response(404)

        run_checks(make_server(transport_type="streaming-http"), handler)
        assert seen.get("mcp-protocol-version") == LATEST_PROTOCOL_VERSION
        assert seen.get("mcp-session-id") == "sess-abc"

    def test_invalid_prm_document_continues_ladder(self):
        # Mirrors the backend wire pin: a 200 PRM missing
        # authorization_servers is skipped and the ladder continues to the
        # root PRM URL.
        root_prm = "https://mcp.example.com/.well-known/oauth-protected-resource"

        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                # Invalid: authorization_servers key missing entirely.
                return httpx.Response(200, json={"resource": SERVER_URL})
            if url == root_prm:
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "ok"
        assert root_prm in prm.detail
        assert all(r.status != "fail" for r in results)

    def test_incomplete_as_doc_continues_to_oidc_candidate(self):
        # Mirrors the backend wire pin: completeness is validated BEFORE
        # candidate selection; an incomplete doc moves to the next URL.
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if url == f"https://idp.example.com{AS_META_PATH}":
                # Incomplete: token_endpoint missing.
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "authorization_endpoint": ("https://idp.example.com/authorize"),
                        "registration_endpoint": "https://idp.example.com/register",
                    },
                )
            if url == "https://idp.example.com/.well-known/openid-configuration":
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        registration = by_title(results, "Authorization server metadata")
        assert registration.status == "ok"
        assert "openid-configuration" in registration.detail
        assert all(r.status != "fail" for r in results)

    def test_streaming_http_json_200_without_jsonrpc_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(200, json={"hello": "world"})
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "not a JSON-RPC initialize reply" in reach.detail

    def test_streaming_http_post_403_fails_as_client_rejection(self):
        # 403 on the deciding POST must not fall through to ok — the
        # runtime will hit the same rejection.
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(403)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "HTTP 403" in reach.detail
        assert "rejects this client" in reach.detail

    def test_streaming_http_get_challenge_does_not_skip_deciding_post(self):
        # A GET 401 with usable resource_metadata is harvest material, not
        # a verdict: the POST still runs and a POST 405 still fails.
        advertised = "https://mcp.example.com/challenge-prm"

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(
                        401,
                        headers={
                            "WWW-Authenticate": (
                                f'Bearer resource_metadata="{advertised}"'
                            )
                        },
                    )
                return httpx.Response(405)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="streaming-http"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "is this an SSE endpoint configured as Streaming HTTP?" in reach.detail

    def test_sse_get_405_fails_as_inverse_misconfig(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(405)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "is this a Streaming HTTP endpoint configured as SSE?" in reach.detail

    def test_sse_get_401_passes_as_auth_required(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL and request.method == "GET":
                return httpx.Response(401)
            return httpx.Response(404)

        results = run_checks(make_server(transport_type="sse"), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "ok"
        assert "auth required" in reach.detail

    def test_both_probes_405_fails_as_wrong_endpoint(self):
        # A streaming-http URL answering 405 to BOTH runtime operations
        # supports neither — that's a wrong/stale endpoint, not "reachable".
        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                return httpx.Response(405)
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "fail"
        assert "neither GET nor MCP initialize POST" in reach.detail

    def test_get_404_post_401_challenge_wins(self):
        # A POST-only server can 404 the GET; the initialize POST's
        # 401-with-challenge is the better evidence and must decide.
        advertised = "https://mcp.example.com/post-prm"
        fallthrough = self._prm_and_as_handler(advertised)

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(404)
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": f'Bearer resource_metadata="{advertised}"'
                    },
                )
            return fallthrough(request)

        results = run_checks(make_server(), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "ok"
        assert "MCP initialize POST" in reach.detail
        assert "GET 404" in reach.detail
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "ok"
        assert advertised in prm.detail
        assert all(r.status != "fail" for r in results)

    def test_get_challenge_without_resource_metadata_post_supplies_it(self):
        # A WWW-Authenticate on GET without resource_metadata must not
        # short-circuit the POST that carries the advertised URL.
        advertised = "https://mcp.example.com/post-prm-2"
        fallthrough = self._prm_and_as_handler(advertised)

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(
                        401, headers={"WWW-Authenticate": 'Bearer realm="mcp"'}
                    )
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": f'Bearer resource_metadata="{advertised}"'
                    },
                )
            return fallthrough(request)

        results = run_checks(make_server(), handler)
        assert by_title(results, "Upstream reachability").status == "ok"
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "ok"
        assert advertised in prm.detail
        assert "advertised via WWW-Authenticate" in prm.detail

    def test_get_200_challenge_less_post_401_gives_auth_verdict(self):
        # A challenge-less GET 200 (e.g. a health page) must not mask an
        # OAuth-protected transport: the POST 401 decides.
        advertised = "https://mcp.example.com/post-prm-3"
        fallthrough = self._prm_and_as_handler(advertised)

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                if request.method == "GET":
                    return httpx.Response(200)
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": f'Bearer resource_metadata="{advertised}"'
                    },
                )
            return fallthrough(request)

        results = run_checks(make_server(), handler)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "ok"
        assert "auth required" in reach.detail
        assert "MCP initialize POST" in reach.detail
        assert "GET 200" in reach.detail

    def test_malformed_advertised_url_reports_check_failure_not_traceback(self):
        # httpx.InvalidURL is not an httpx.HTTPError; a nonnumeric port in
        # the advertised resource_metadata must become a check failure.
        malformed = "https://mcp.example.com:notaport/prm"

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == SERVER_URL:
                return httpx.Response(
                    401,
                    headers={
                        "WWW-Authenticate": (f'Bearer resource_metadata="{malformed}"')
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        assert by_title(results, "Upstream reachability").status == "ok"
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "fail"
        assert "advertised metadata URL is malformed" in prm.detail
        assert "notaport" in prm.detail

    def test_sse_server_reachable_without_reading_endless_stream(self):
        # An unauthenticated SSE server answers 200 with a text/event-stream
        # body that never ends. Reachability must key off the response
        # HEADERS and close without reading — a buffered GET would sit on
        # the stream until the read timeout and report a live server dead.
        class HangingStream(httpx.AsyncByteStream):
            def __aiter__(self):
                return self._gen()

            async def _gen(self):
                yield b": ping\n\n"
                await anyio.sleep(3600)  # holds the stream open

            async def aclose(self) -> None:
                pass

        class SSEUpstreamTransport(httpx.AsyncBaseTransport):
            async def handle_async_request(
                self, request: httpx.Request
            ) -> httpx.Response:
                path = request.url.path
                if path == "/mcp":
                    return httpx.Response(
                        200,
                        headers={"content-type": "text/event-stream"},
                        stream=HangingStream(),
                    )
                if path == PRM_PATH:
                    return httpx.Response(
                        200,
                        json={
                            "resource": SERVER_URL,
                            "authorization_servers": ["https://idp.example.com"],
                        },
                    )
                if path == AS_META_PATH:
                    return httpx.Response(
                        200,
                        json={
                            "issuer": "https://idp.example.com",
                            "registration_endpoint": (
                                "https://idp.example.com/register"
                            ),
                            **AS_ENDPOINTS,
                        },
                    )
                return httpx.Response(404)

        async def run_with_guard():
            # Buffering the endless body would hang far past this guard.
            with anyio.fail_after(10):
                return await run_network_checks(
                    make_server(transport_type="sse"),
                    None,
                    client_factory=lambda headers: httpx.AsyncClient(
                        transport=SSEUpstreamTransport(), headers=headers
                    ),
                    cached_port_lookup=lambda _url: None,
                )

        results = anyio.run(run_with_guard)
        reach = by_title(results, "Upstream reachability")
        assert reach.status == "ok"
        assert "HTTP 200" in reach.detail
        assert all(r.status != "fail" for r in results)

    def test_credentialed_url_renders_redacted_in_every_output_path(self):
        # Catalog servers embed secrets in the URL (query token, userinfo);
        # doctor output lands in support tickets, so no rendered detail or
        # remedy may carry them — including the resource-mismatch line,
        # which prints the configured URL (userinfo lives in its netloc).
        secret_url = "https://alice:hunter2@mcp.example.com/mcp?token=SECRET123#frag"

        def handler(request: httpx.Request) -> httpx.Response:
            path = request.url.path
            if path == "/mcp":
                return httpx.Response(401)
            if path == PRM_PATH:
                # Different resource -> forces the mismatch detail that
                # prints both URLs.
                return httpx.Response(
                    200,
                    json={
                        "resource": "https://mcp.example.com/other?key=PRMSECRET",
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            if path == AS_META_PATH:
                return httpx.Response(
                    200,
                    json={
                        "issuer": "https://idp.example.com",
                        "registration_endpoint": "https://idp.example.com/register",
                        **AS_ENDPOINTS,
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(url=secret_url), handler)
        rendered = "\n".join(f"{r.title} {r.detail} {r.remedy or ''}" for r in results)
        assert "SECRET123" not in rendered
        assert "hunter2" not in rendered
        assert "alice" not in rendered
        assert "PRMSECRET" not in rendered
        assert "token=***" in rendered
        mismatch = by_title(results, "PRM `resource` matches configured URL (RFC 8707)")
        assert mismatch.status == "fail"
        assert "key=***" in mismatch.detail

    def test_unusable_prm_issuer_fails_naming_field(self):
        # authorization_servers[0] that is not an absolute http(s) URL must
        # not silently drain into failed discovery with exit 0. The document
        # is skipped for selection (runtime ladder semantics) but the reason
        # is reported on the PRM check — where the defect actually is —
        # rather than degrading to a bare "not found".
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["not-a-url"],
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        prm = by_title(results, "Protected-resource metadata (RFC 9728)")
        assert prm.status == "fail"
        assert "authorization_servers entry is not an absolute http(s) URL" in (
            prm.detail
        )
        assert "not-a-url" in prm.detail

    def test_unfetchable_as_metadata_warns(self):
        def handler(request: httpx.Request) -> httpx.Response:
            url = str(request.url)
            if url == SERVER_URL:
                return httpx.Response(401)
            if url == f"https://mcp.example.com{PRM_PATH}":
                return httpx.Response(
                    200,
                    json={
                        "resource": SERVER_URL,
                        "authorization_servers": ["https://idp.example.com"],
                    },
                )
            return httpx.Response(404)

        results = run_checks(make_server(), handler)
        assert by_title(results, "Authorization server metadata").status == "warn"


def _fake_credentials(*_args: Any, **_kwargs: Any) -> dict[str, str]:
    return {"host": "https://runlayer.example.com", "secret": "test-secret"}


class TestDoctorCommand:
    def _invoke(self, server: ServerDetails, args: list[str] | None = None):
        client = MagicMock()
        client.get_server_details.return_value = server
        with (
            patch(
                "runlayer_cli.commands.doctor.resolve_credentials",
                side_effect=_fake_credentials,
            ),
            patch("runlayer_cli.commands.doctor.RunlayerClient", return_value=client),
            patch(
                "runlayer_cli.commands.doctor._default_client_factory",
                new=lambda headers: factory_for(healthy_handler)(headers),
            ),
            patch(
                "runlayer_cli.commands.doctor._cached_callback_port",
                return_value=None,
            ),
        ):
            return runner.invoke(app, ["doctor", SERVER_ID, *(args or [])])

    def test_healthy_server_exits_zero(self):
        result = self._invoke(make_server(), ["--oauth-callback-port", "8123"])
        assert result.exit_code == 0, result.output
        assert "Server details" in result.output
        assert "deployment_mode=LOCAL" in result.output

    def test_stdio_server_skips_gracefully(self):
        server = make_server(transport_type="stdio", url="npx")
        result = self._invoke(server)
        assert result.exit_code == 0, result.output
        assert "stdio transport" in result.output
        assert "Upstream reachability" not in result.output

    def test_failing_check_exits_nonzero(self):
        # Manual OAuth required but no client id -> ❌.
        server = make_server(requires_manual_oauth_setup=True)
        result = self._invoke(server)
        assert result.exit_code == 1, result.output
        assert "no client ID is configured" in result.output

    def test_random_callback_port_warns_but_passes(self):
        result = self._invoke(make_server())
        assert result.exit_code == 0, result.output
        assert "OAuth callback port" in result.output

    def test_server_details_http_error_exits_nonzero(self):
        client = MagicMock()
        request = httpx.Request("GET", "https://runlayer.example.com/api/v1/local/x")
        client.get_server_details.side_effect = httpx.HTTPStatusError(
            "not found", request=request, response=httpx.Response(404, request=request)
        )
        with (
            patch(
                "runlayer_cli.commands.doctor.resolve_credentials",
                side_effect=_fake_credentials,
            ),
            patch("runlayer_cli.commands.doctor.RunlayerClient", return_value=client),
        ):
            result = runner.invoke(app, ["doctor", SERVER_ID])
        assert result.exit_code == 1
        assert "404" in result.output

    def test_control_plane_error_redacts_credentialed_host(self):
        # --host / config host can carry userinfo or query credentials;
        # the connection-error line must render it redacted.
        def credentialed_host(*_args: Any, **_kwargs: Any) -> dict[str, str]:
            return {
                "host": "https://alice:hunter2@runlayer.example.com?t=SECRET123",
                "secret": "test-secret",
            }

        client = MagicMock()
        request = httpx.Request("GET", "https://runlayer.example.com/api/v1/local/x")
        client.get_server_details.side_effect = httpx.ConnectError(
            "connection refused", request=request
        )
        with (
            patch(
                "runlayer_cli.commands.doctor.resolve_credentials",
                side_effect=credentialed_host,
            ),
            patch("runlayer_cli.commands.doctor.RunlayerClient", return_value=client),
        ):
            result = runner.invoke(app, ["doctor", SERVER_ID])
        assert result.exit_code == 1
        assert "hunter2" not in result.output
        assert "SECRET123" not in result.output
        assert "t=***" in result.output

    def test_resolves_alias_targets(self):
        client = MagicMock()
        client.resolve_server_target.return_value = SERVER_ID
        client.get_server_details.return_value = make_server(transport_type="stdio")
        with (
            patch(
                "runlayer_cli.commands.doctor.resolve_credentials",
                side_effect=_fake_credentials,
            ),
            patch("runlayer_cli.commands.doctor.RunlayerClient", return_value=client),
        ):
            result = runner.invoke(app, ["doctor", "my-alias"])
        assert result.exit_code == 0, result.output
        client.resolve_server_target.assert_called_once_with("my-alias")
        client.get_server_details.assert_called_once_with(SERVER_ID)


class TestVerifiedLocal:
    """Catalog entries like Figma are stdio-typed but `runlayer run`
    verifies + proxies to a localhost desktop app; doctor mirrors that."""

    ENTRY = "com.fake/desktop-mcp"
    TARGET = "http://127.0.0.1:39999/mcp"

    def _server(self) -> ServerDetails:
        return make_server(
            transport_type="stdio",
            url="fake-stdio-command",
            catalog_entry_name=self.ENTRY,
        )

    def _patched_configs(self):
        from runlayer_cli.verified_local_proxy.config import VerificationConfig

        config = VerificationConfig(
            server_id=self.ENTRY,
            display_name="Fake Desktop MCP",
            target_port=39999,
        )
        return patch.dict(
            "runlayer_cli.verified_local_proxy.config.VERIFICATION_CONFIGS",
            {self.ENTRY: config},
        )

    def test_desktop_app_down_fails(self):
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused", request=request)

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET, client_factory=factory_for(handler)
            )
        )
        target = by_title(results, "Verified-local target")
        assert target.status == "fail"
        assert "desktop app not reachable at http://127.0.0.1:39999/mcp" in (
            target.detail
        )

    def test_desktop_app_up_passes(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert str(request.url) == self.TARGET
            return mcp_ok_response()

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET, client_factory=factory_for(handler)
            )
        )
        target = by_title(results, "Verified-local target")
        assert target.status == "ok"
        assert "desktop app is listening" in target.detail

    def test_get_failure_does_not_preempt_deciding_post(self):
        # These targets are StreamableHttpTransport endpoints: the POST is
        # what the runtime uses, so a desktop app that refuses the
        # preliminary GET but answers initialize is reachable.
        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET":
                raise httpx.ConnectError("connection refused", request=request)
            return mcp_ok_response()

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET, client_factory=factory_for(handler)
            )
        )
        target = by_title(results, "Verified-local target")
        assert target.status == "ok"
        assert "desktop app is listening" in target.detail

    def test_desktop_app_mcp_endpoint_404_fails(self):
        # App answers HTTP but 404s the MCP endpoint — the runtime's
        # initialize POST would fail identically, so this is not a pass.
        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "GET":
                return httpx.Response(200)
            return httpx.Response(404)

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET, client_factory=factory_for(handler)
            )
        )
        target = by_title(results, "Verified-local target")
        assert target.status == "fail"
        assert "MCP endpoint is unavailable" in target.detail

    def test_verify_target_failure_fails_even_when_http_succeeds(self):
        # Any process can answer initialize; only the signature-verified
        # app counts — mirrors verify_target refusing unexpected listeners.
        from runlayer_cli.verified_local_proxy.exceptions import VerificationError

        def bad_verifier() -> None:
            raise VerificationError("signature mismatch: unsigned binary")

        def handler(request: httpx.Request) -> httpx.Response:
            return mcp_ok_response()

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET,
                client_factory=factory_for(handler),
                verifier=bad_verifier,
            )
        )
        process = by_title(results, "Verified-local process")
        assert process.status == "fail"
        assert "not the expected signed application" in process.detail
        assert "signature mismatch" in process.detail
        # HTTP probe still reports alongside.
        assert by_title(results, "Verified-local target").status == "ok"

    def test_windows_not_implemented_verifier_warns_and_http_decides(self):
        # WindowsVerifier raises before identifying ANY listener; a genuine
        # desktop app must not be accused of being an impostor.
        from runlayer_cli.verified_local_proxy.exceptions import VerificationError

        def windows_verifier() -> None:
            raise VerificationError(
                "Windows signature verification is not yet implemented. "
                "Please use macOS for now."
            )

        def handler(request: httpx.Request) -> httpx.Response:
            return mcp_ok_response()

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET,
                client_factory=factory_for(handler),
                verifier=windows_verifier,
            )
        )
        process = by_title(results, "Verified-local process")
        assert process.status == "warn"
        assert "process verification unavailable on this platform" in process.detail
        assert "not the expected signed application" not in process.detail
        # HTTP verdict decides: overall passes.
        assert by_title(results, "Verified-local target").status == "ok"
        assert all(r.status != "fail" for r in results)

    def test_unsupported_platform_runtimeerror_warns_and_http_decides(self):
        def unsupported_verifier() -> None:
            raise RuntimeError(
                "Unsupported platform: linux. Only macOS and Windows are supported."
            )

        def handler(request: httpx.Request) -> httpx.Response:
            return mcp_ok_response()

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET,
                client_factory=factory_for(handler),
                verifier=unsupported_verifier,
            )
        )
        process = by_title(results, "Verified-local process")
        assert process.status == "warn"
        assert "process verification unavailable on this platform" in process.detail
        assert all(r.status != "fail" for r in results)

    def test_verify_target_not_running_reports_no_process(self):
        from runlayer_cli.verified_local_proxy.exceptions import (
            TargetNotRunningError,
        )

        def no_process() -> None:
            raise TargetNotRunningError("no process on port 39999")

        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused", request=request)

        results = anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET,
                client_factory=factory_for(handler),
                verifier=no_process,
            )
        )
        process = by_title(results, "Verified-local process")
        assert process.status == "fail"
        assert "no process found listening" in process.detail

    def test_identity_headers_sent_to_target(self):
        # `runlayer run` passes the identity bundle to the verified-local
        # transport too; the probe must match — and the target counts as
        # "upstream" for identity scoping (base client stays identity-free).
        requests: list[httpx.Request] = []
        factories: list[dict[str, str]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return mcp_ok_response()

        def factory(headers: dict[str, str]) -> httpx.AsyncClient:
            factories.append(headers)
            return factory_for(handler)(headers)

        anyio.run(
            lambda: run_verified_local_checks(
                self.TARGET,
                {"X-Runlayer-Identity-Token": "signed-token"},
                client_factory=factory,
            )
        )
        assert requests, "expected target probes"
        for request in requests:
            assert request.headers.get("x-runlayer-identity-token") == "signed-token"
        for base_headers in factories:
            assert not any(
                name.lower().startswith("x-runlayer-") for name in base_headers
            )

    def _invoke(self, handler, verify_side_effect=None):
        client = MagicMock()
        client.get_server_details.return_value = self._server()
        with (
            patch(
                "runlayer_cli.commands.doctor.resolve_credentials",
                side_effect=_fake_credentials,
            ),
            patch("runlayer_cli.commands.doctor.RunlayerClient", return_value=client),
            self._patched_configs(),
            patch(
                "runlayer_cli.commands.doctor._verify_target_once",
                side_effect=verify_side_effect,
            ),
            patch(
                "runlayer_cli.commands.doctor._default_client_factory",
                new=lambda headers: factory_for(handler)(headers),
            ),
        ):
            return runner.invoke(app, ["doctor", SERVER_ID])

    def test_cli_probes_target_not_stdio_skip(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return mcp_ok_response()

        result = self._invoke(handler)
        assert result.exit_code == 0, result.output
        assert "desktop app is listening" in result.output
        assert "stdio transport" not in result.output

    def test_cli_desktop_down_exits_nonzero(self):
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused", request=request)

        result = self._invoke(handler)
        assert result.exit_code == 1, result.output
        assert "desktop app not reachable" in result.output

    def test_cli_unverified_process_exits_nonzero(self):
        from runlayer_cli.verified_local_proxy.exceptions import VerificationError

        def handler(request: httpx.Request) -> httpx.Response:
            return mcp_ok_response()

        result = self._invoke(
            handler,
            verify_side_effect=VerificationError("authority mismatch"),
        )
        assert result.exit_code == 1, result.output
        assert "not the expected signed application" in result.output


class TestIssuerMatching:
    """RFC 8414: declared issuer must EQUAL the discovery target."""

    def test_exact_match_passes(self):
        assert _issuer_matches(
            "https://idp.example.com/oauth2/tenant",
            "https://idp.example.com/oauth2/tenant",
        )

    def test_trailing_slash_difference_is_a_mismatch(self):
        # RFC 8414 uses SIMPLE STRING comparison — no normalization; the
        # runtime's typed parsing rejects this exact pair.
        assert not _issuer_matches(
            "https://idp.example.com/oauth2/tenant/",
            "https://idp.example.com/oauth2/tenant",
        )

    def test_tenant_vs_bare_origin_rejected(self):
        # Prefix acceptance would pass cross-tenant documents.
        assert not _issuer_matches(
            "https://idp.example.com",
            "https://idp.example.com/oauth2/tenant",
        )

    def test_tenant_vs_sibling_tenant_rejected(self):
        assert not _issuer_matches(
            "https://idp.example.com/oauth2/other",
            "https://idp.example.com/oauth2/tenant",
        )


class TestAsMetadataCompleteness:
    """The auth-code flow needs both endpoints, on the DCR and manual paths."""

    FOUND = "https://idp.example.com/.well-known/oauth-authorization-server"
    ISSUER = "https://idp.example.com"

    def test_missing_token_endpoint_fails_dcr_path(self):
        result = check_registration_endpoint(
            {
                "authorization_endpoint": "https://idp.example.com/authorize",
                "registration_endpoint": "https://idp.example.com/register",
            },
            self.FOUND,
            self.ISSUER,
            make_server(),
        )
        assert result.status == "fail"
        assert "token_endpoint" in result.detail

    def test_missing_authorization_endpoint_fails_manual_path(self):
        # Manual clients skip registration but still need both endpoints;
        # incomplete metadata must not pass just because DCR is skipped.
        result = check_registration_endpoint(
            {"token_endpoint": "https://idp.example.com/token"},
            self.FOUND,
            self.ISSUER,
            make_server(requires_manual_oauth_setup=True, manual_oauth_client_id="cid"),
        )
        assert result.status == "fail"
        assert "authorization_endpoint" in result.detail

    def test_unusable_token_endpoint_fails_naming_field(self):
        result = check_registration_endpoint(
            {
                "authorization_endpoint": "https://idp.example.com/authorize",
                "token_endpoint": "not-a-url",
            },
            self.FOUND,
            self.ISSUER,
            make_server(),
        )
        assert result.status == "fail"
        assert "token_endpoint" in result.detail
        assert "not-a-url" in result.detail

    def test_relative_authorization_endpoint_fails(self):
        result = check_registration_endpoint(
            {
                "authorization_endpoint": "/authorize",
                "token_endpoint": "https://idp.example.com/token",
            },
            self.FOUND,
            self.ISSUER,
            make_server(),
        )
        assert result.status == "fail"
        assert "authorization_endpoint" in result.detail

    def test_unusable_registration_endpoint_fails_dcr_path(self):
        result = check_registration_endpoint(
            {**AS_ENDPOINTS, "registration_endpoint": "not-a-url"},
            self.FOUND,
            self.ISSUER,
            make_server(),
        )
        assert result.status == "fail"
        assert "registration_endpoint" in result.detail
        assert "not-a-url" in result.detail

    def test_valid_absolute_endpoints_pass(self):
        result = check_registration_endpoint(
            {
                **AS_ENDPOINTS,
                "registration_endpoint": "https://idp.example.com/register",
            },
            self.FOUND,
            self.ISSUER,
            make_server(),
        )
        assert result.status == "ok"

    def test_complete_metadata_without_dcr_manual_client_ok(self):
        result = check_registration_endpoint(
            {**AS_ENDPOINTS, "issuer": self.ISSUER},
            self.FOUND,
            self.ISSUER,
            make_server(requires_manual_oauth_setup=True, manual_oauth_client_id="cid"),
        )
        assert result.status == "ok"


class TestReadOnlyContract:
    def test_probes_are_read_only(self):
        # GETs everywhere; the only POST allowed is the MCP initialize
        # handshake mirror aimed at the server URL itself.
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return healthy_handler(request)

        run_checks(make_server(), handler)
        assert requests, "expected at least one request"
        assert {r.method for r in requests} <= {"GET", "POST"}
        for request in requests:
            if request.method == "POST":
                assert str(request.url) == SERVER_URL
                body = json.loads(request.content)
                assert body["method"] == "initialize"


class TestAsciiRendering:
    def _results(self) -> list[CheckResult]:
        return [
            CheckResult("ok", "Server details", "em — dash ✅ ‘quotes’ → arrow"),
            CheckResult("warn", "OAuth scopes", "en – dash “double” … ellipsis"),
            CheckResult("fail", "Reachability", "host — unreachable", "fix — it"),
            CheckResult("skip", "Preflight", "stdio — nothing to check"),
        ]

    def test_ascii_stdout_renders_every_line_without_raising(self, monkeypatch):
        buffer = io.BytesIO()
        stream = io.TextIOWrapper(buffer, encoding="ascii")
        monkeypatch.setattr(sys, "stdout", stream)

        passed = print_results(self._results())

        stream.flush()
        output = buffer.getvalue().decode("ascii")
        assert passed is False
        assert "[ok]" in output
        assert "[warn]" in output
        assert "[error]" in output
        assert "[skip]" in output
        assert "em - dash" in output
        assert "-> arrow" in output
        assert "fix - it" in output

    def test_unicode_stdout_keeps_unicode(self, monkeypatch):
        buffer = io.BytesIO()
        stream = io.TextIOWrapper(buffer, encoding="utf-8")
        monkeypatch.setattr(sys, "stdout", stream)

        print_results(self._results())

        stream.flush()
        output = buffer.getvalue().decode("utf-8")
        assert "✅" in output
        assert "em — dash" in output
