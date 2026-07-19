"""Tests for connector manager OAuth configuration."""

from pathlib import Path

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient

from airbyte_ops_webapp import serve as serve_module
from airbyte_ops_webapp import state as state_module
from airbyte_ops_webapp.auth import oauth as oauth_module
from airbyte_ops_webapp.pages.connector_version_manager.defaults import (
    CONNECTOR_VERSION_MANAGER_PATH,
)
from airbyte_ops_webapp.pages.customer_billing.defaults import CUSTOMER_BILLING_PATH
from airbyte_ops_webapp.pages.login.page import OPS_LOGIN_PATH
from airbyte_ops_webapp.pages.motherduck_diagnostics.defaults import (
    MOTHERDUCK_DIAGNOSTICS_PATH,
)
from airbyte_ops_webapp.serve import add_oauth_routes

_IMPORTMAP = "<script type='importmap'>{}</script>"

_PROTECTED_ROUTES = [
    pytest.param(serve_module.add_home_routes, "/home", id="home"),
    pytest.param(
        serve_module.add_connector_version_manager_routes,
        CONNECTOR_VERSION_MANAGER_PATH,
        id="connector_version_manager",
    ),
    pytest.param(
        serve_module.add_customer_billing_routes,
        CUSTOMER_BILLING_PATH,
        id="customer_billing",
    ),
    pytest.param(
        serve_module.add_motherduck_diagnostics_routes,
        MOTHERDUCK_DIAGNOSTICS_PATH,
        id="motherduck_diagnostics",
    ),
]

REPO_ROOT = Path(__file__).resolve().parents[2]


def _sample_oauth_config() -> state_module.OAuthConfigState:
    return state_module.OAuthConfigState(
        enabled=True,
        issuer="https://cloud.airbyte.com/auth/realms/airbyte",
        client_id="airbyte-ops-webapp-client",
        redirect_uri="http://localhost:3000/oauth/callback",
        authorization_endpoint="https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/auth",
        token_endpoint="https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/token",
        session_endpoint="/oauth/session",
        token_exchange_endpoint="/oauth/token",
    )


def test_oauth_config_defaults_to_airbyte_realm_client(
    monkeypatch,
) -> None:
    monkeypatch.delenv(state_module.OAUTH_CLIENT_ID_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ENABLED_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ISSUER_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_PUBLIC_URL_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_REDIRECT_URI_ENV_VAR, raising=False)

    config = oauth_module.oauth_config()

    assert config.enabled is True
    assert config.issuer == "https://cloud.airbyte.com/auth/realms/airbyte"
    assert config.client_id == "airbyte-ops-webapp-client"
    assert config.redirect_uri == "http://localhost:3000/oauth/callback"
    assert (
        config.authorization_endpoint
        == "https://cloud.airbyte.com/auth/realms/airbyte/protocol/openid-connect/auth"
    )
    assert config.session_endpoint == "/oauth/session"
    assert config.token_exchange_endpoint == "/oauth/token"


def test_oauth_redirect_uri_uses_public_url(
    monkeypatch,
) -> None:
    monkeypatch.delenv(state_module.OAUTH_REDIRECT_URI_ENV_VAR, raising=False)
    monkeypatch.setenv(
        state_module.OAUTH_PUBLIC_URL_ENV_VAR,
        "https://ops.internal.airbyte.ai/",
    )

    assert (
        oauth_module._oauth_redirect_uri()
        == "https://ops.internal.airbyte.ai/oauth/callback"
    )


def test_oauth_redirect_uri_override_wins(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        state_module.OAUTH_REDIRECT_URI_ENV_VAR,
        "http://localhost:3000/oauth/callback",
    )
    monkeypatch.setenv(
        state_module.OAUTH_PUBLIC_URL_ENV_VAR,
        "https://ops.internal.airbyte.ai",
    )

    assert oauth_module._oauth_redirect_uri() == "http://localhost:3000/oauth/callback"


def test_oauth_callback_html_exchanges_code_with_configured_client() -> None:
    config = _sample_oauth_config()

    html = oauth_module._oauth_callback_html(config)

    assert "airbyte-ops-webapp-client" in html
    assert "http://localhost:3000/oauth/callback" in html
    assert "code_verifier" in html
    assert "token_exchange_endpoint" in html
    assert "airbyte_ops_webapp_nonce" in html
    assert "claims.nonce !== expectedNonce" in html
    assert "config.session_endpoint" in html
    assert "OAuth session setup failed." in html


def test_oauth_callback_csp_restricts_connections_to_self() -> None:
    csp = oauth_module._oauth_callback_csp()

    assert "default-src 'none'" in csp
    assert "connect-src 'self'" in csp
    assert "script-src 'unsafe-inline'" in csp


def test_webapp_host_serves_oauth_routes(monkeypatch) -> None:
    monkeypatch.delenv(state_module.OAUTH_CLIENT_ID_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ENABLED_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_ISSUER_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_PUBLIC_URL_ENV_VAR, raising=False)
    monkeypatch.delenv(state_module.OAUTH_REDIRECT_URI_ENV_VAR, raising=False)
    monkeypatch.setattr(
        oauth_module,
        "_exchange_oauth_token",
        lambda code, code_verifier: {
            "access_token": f"{code}-{code_verifier}",
            "id_token": "header.payload.signature",
            "expires_in": 180,
        },
    )
    app = Starlette()
    add_oauth_routes(app)

    client = TestClient(app)
    callback_response = client.get("/oauth/callback")
    token_response = client.post(
        "/oauth/token",
        json={"code": "code_value", "code_verifier": "verifier_value"},
    )

    assert callback_response.status_code == 200
    assert "Completing Airbyte sign-in" in callback_response.text
    assert token_response.status_code == 200
    assert token_response.json()["access_token"] == "code_value-verifier_value"
    assert token_response.headers["Cache-Control"] == "no-store"


def test_prefab_renderer_route_injects_oauth_js_handlers(monkeypatch) -> None:
    renderer_uri = "ui://prefab/tool/c10065b16275/renderer.html"

    async def read_resource(_mcp_url: str, uri: str) -> str | None:
        if uri == renderer_uri:
            return "<html><head></head><body>Prefab</body></html>"
        return None

    monkeypatch.setattr(serve_module, "_read_mcp_resource", read_resource)
    app = Starlette()
    serve_module.add_prefab_renderer_route(app, "http://localhost:8000/mcp")

    response = TestClient(app).get(
        "/ui-resource",
        params={"uri": renderer_uri},
    )

    assert response.status_code == 200
    assert "window.__prefab_handlers" in response.text
    assert "startOAuth" in response.text
    assert "hydrateOAuth" in response.text
    assert "logoutOAuth" in response.text
    assert "hydrateOAuth: async (...args) =>" in response.text
    assert "logoutOAuth: async (...args) =>" in response.text
    assert "window.top?.crypto" in response.text
    assert "browserCrypto.subtle.digest" in response.text
    assert response.text.index("window.__prefab_handlers") < response.text.index(
        "</head>"
    )


def test_webapp_root_redirects_to_home_path() -> None:
    app = Starlette()
    serve_module.add_home_routes(app, "<script type='importmap'>{}</script>")

    response = TestClient(app).get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/home"


def test_webapp_home_path_hosts_home_app(monkeypatch) -> None:
    monkeypatch.setattr(serve_module, "request_has_valid_session", lambda request: True)
    app = Starlette()
    serve_module.add_home_routes(app, "<script type='importmap'>{}</script>")

    response = TestClient(app).get("/home")

    assert response.status_code == 200
    assert response.history == []
    assert "Airbyte Internal Ops" in response.text
    assert 'const toolName = "ops_home";' in response.text
    assert "const toolArgs = {};" in response.text


def test_webapp_login_path_redirects_to_authorization() -> None:
    app = Starlette()
    serve_module.add_login_routes(app, "<script type='importmap'>{}</script>")

    response = TestClient(app).get(OPS_LOGIN_PATH, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "/authorization"


def test_webapp_index_path_is_not_supported() -> None:
    app = Starlette()
    serve_module.add_home_routes(app, "<script type='importmap'>{}</script>")

    response = TestClient(app).get("/index")

    assert response.status_code == 404


def test_connector_versions_path_hosts_connector_version_manager_app(
    monkeypatch,
) -> None:
    monkeypatch.setattr(serve_module, "request_has_valid_session", lambda request: True)
    app = Starlette()
    serve_module.add_connector_version_manager_routes(
        app,
        "<script type='importmap'>{}</script>",
    )

    response = TestClient(app).get(
        f"{CONNECTOR_VERSION_MANAGER_PATH}?query=destination-snowflake"
    )

    assert response.status_code == 200
    assert response.history == []
    assert "Airbyte Ops \u2014 Connector Versions" in response.text
    assert 'const toolName = "manage_connector_versions";' in response.text
    assert 'const toolArgs = {"query": "destination-snowflake"};' in response.text
    assert "mcp-log-panel" not in response.text
    assert "/api/logs" not in response.text


def test_generic_fastmcp_app_routes_are_removed() -> None:
    async def unused_route(_request) -> Response:
        return Response("unused")

    app = Starlette(
        routes=[
            Route("/", unused_route),
            Route("/picker-app", unused_route),
            Route("/launch", unused_route),
            Route("/api/launch", unused_route, methods=["POST"]),
            Route("/api/logs", unused_route),
            Route("/api/logs/bridge", unused_route, methods=["POST"]),
            Route("/api/logs/clear", unused_route, methods=["POST"]),
            Route("/ui-resource", unused_route),
        ]
    )

    serve_module.remove_generic_app_routes(app)

    route_paths = {route.path for route in app.routes}
    assert "/" not in route_paths
    assert "/picker-app" not in route_paths
    assert "/launch" not in route_paths
    assert "/api/launch" not in route_paths
    assert "/api/logs" not in route_paths
    assert "/api/logs/bridge" not in route_paths
    assert "/api/logs/clear" not in route_paths
    assert "/ui-resource" in route_paths


def test_production_message_log_discards_mcp_messages() -> None:
    fake_token = "fake-sensitive-access-token"
    message_log = serve_module._NullMessageLog()

    message_log.log_request(
        {
            "method": "tools/call",
            "params": {"arguments": {"auth_bearer_token": fake_token}},
        }
    )
    message_log.log_response({"result": {"secret_field": fake_token}})
    message_log.log_bridge({"state": {"auth_bearer_token": fake_token}})

    assert message_log.get_since() == []


def test_local_display_url_uses_localhost() -> None:
    assert serve_module._local_display_url(3000) == "http://localhost:3000"
    assert "0.0.0.0" not in serve_module._local_display_url(3000)


def test_oauth_token_route_rejects_incomplete_payload() -> None:
    app = Starlette()
    add_oauth_routes(app)

    response = TestClient(app).post("/oauth/token", json={"code": "code_value"})

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_request"


def test_home_state_preserves_oauth_session_endpoint() -> None:
    state = state_module.OpsPageState(
        default_connector_from_args=False,
        is_mock_only=True,
        oauth_config=oauth_module.oauth_config(),
        oauth_enabled=True,
    ).to_prefab_state()

    assert state["oauth_config"]["session_endpoint"] == "/oauth/session"


def test_hydrate_oauth_action_fetches_session_and_sets_state() -> None:
    action = oauth_module.hydrate_oauth_action().model_dump(
        by_alias=True,
        exclude_none=True,
    )

    assert action["action"] == "fetch"
    assert action["url"] == "/oauth/session"
    assert action["method"] == "GET"
    assert action["onSuccess"] == [
        {
            "action": "setState",
            "key": "auth_bearer_token",
            "value": "{{ $result.auth_bearer_token }}",
        },
        {
            "action": "setState",
            "key": "admin_user_email",
            "value": "{{ $result.admin_user_email || admin_user_email }}",
        },
        {
            "action": "setState",
            "key": "oauth_authenticated",
            "value": "{{ $result.oauth_authenticated }}",
        },
        {
            "action": "setState",
            "key": "oauth_user_email",
            "value": "{{ $result.oauth_user_email }}",
        },
        {
            "action": "setState",
            "key": "oauth_status",
            "value": "{{ $result.oauth_status }}",
        },
    ]
    assert action["onError"] == [
        {
            "action": "setState",
            "key": "auth_bearer_token",
            "value": "{{ auth_bearer_token }}",
        },
        {
            "action": "setState",
            "key": "admin_user_email",
            "value": "{{ admin_user_email }}",
        },
        {
            "action": "setState",
            "key": "oauth_authenticated",
            "value": "{{ oauth_authenticated }}",
        },
        {
            "action": "setState",
            "key": "oauth_user_email",
            "value": "{{ oauth_user_email }}",
        },
        {
            "action": "setState",
            "key": "oauth_status",
            "value": "Unable to refresh OAuth session. Sign in again.",
        },
    ]


def test_oauth_session_route_round_trips_signed_cookie(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    app = Starlette()
    add_oauth_routes(app)
    client = TestClient(app)

    created = client.post(
        "/oauth/session",
        json={
            "access_token": "access-token-value",
            "email": "aj@airbyte.io",
            "expires_in": 60,
        },
    )
    hydrated = client.get("/oauth/session")
    deleted = client.delete("/oauth/session")
    signed_out = client.get("/oauth/session")

    assert created.status_code == 200
    assert created.json()["auth_bearer_token"] == "access-token-value"
    assert created.json()["oauth_authenticated"] is True
    assert "HttpOnly" in created.headers["set-cookie"]
    assert "SameSite=lax" in created.headers["set-cookie"]
    assert "access-token-value" not in created.headers["set-cookie"]
    assert hydrated.status_code == 200
    assert hydrated.json()["auth_bearer_token"] == "access-token-value"
    assert hydrated.json()["oauth_user_email"] == "aj@airbyte.io"
    assert deleted.status_code == 200
    assert deleted.json()["oauth_authenticated"] is False
    assert signed_out.status_code == 200
    assert signed_out.json()["oauth_authenticated"] is False


def test_oauth_session_route_refreshes_expired_access_token(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    monkeypatch.setattr(oauth_module, "_now_ms", lambda: 100_000)

    def refresh_oauth_token(refresh_token: str) -> dict[str, object]:
        assert refresh_token == "refresh-token-value"
        return {
            "access_token": "refreshed-access-token",
            "expires_in": 60,
            "refresh_token": "refreshed-refresh-token",
            "refresh_expires_in": 120,
        }

    monkeypatch.setattr(oauth_module, "_refresh_oauth_token", refresh_oauth_token)
    app = Starlette()
    add_oauth_routes(app)
    client = TestClient(app)
    client.post(
        "/oauth/session",
        json={
            "access_token": "expired-access-token",
            "email": "aj@airbyte.io",
            "expires_at": 101_000,
            "refresh_token": "refresh-token-value",
            "refresh_expires_at": 200_000,
        },
    )

    response = client.get("/oauth/session")

    assert response.status_code == 200
    assert response.json()["auth_bearer_token"] == "refreshed-access-token"
    assert response.json()["oauth_authenticated"] is True


def test_oauth_session_route_rejects_missing_access_token(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    app = Starlette()
    add_oauth_routes(app)

    response = TestClient(app).post("/oauth/session", json={"email": "aj@airbyte.io"})

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_request"


def test_oauth_session_route_rejects_non_object_payload(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    app = Starlette()
    add_oauth_routes(app)

    response = TestClient(app).post("/oauth/session", json=["access-token-value"])

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_request"


def test_oauth_session_route_rejects_invalid_json(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    app = Starlette()
    add_oauth_routes(app)

    response = TestClient(app).post(
        "/oauth/session",
        content="{",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_request"


def test_oauth_session_route_rejects_non_string_access_token(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    app = Starlette()
    add_oauth_routes(app)

    response = TestClient(app).post("/oauth/session", json={"access_token": None})

    assert response.status_code == 400
    assert response.json()["error"] == "invalid_request"


def test_oauth_session_route_requires_oauth_client_secret(monkeypatch) -> None:
    monkeypatch.delenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, raising=False)
    monkeypatch.setenv(state_module.OAUTH_CLIENT_ID_ENV_VAR, "public-client-id")
    app = Starlette()
    add_oauth_routes(app)
    client = TestClient(app)

    signed_out = client.get("/oauth/session")
    created = client.post("/oauth/session", json={"access_token": "access-token-value"})

    assert signed_out.status_code == 200
    assert signed_out.json()["oauth_authenticated"] is False
    assert created.status_code == 500
    assert created.json()["error"] == "server_error"


def test_oauth_session_route_rejects_refresh_without_access_token(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    monkeypatch.setattr(oauth_module, "_now_ms", lambda: 100_000)

    def refresh_oauth_token(_refresh_token: str) -> dict[str, object]:
        return {"expires_in": 60}

    monkeypatch.setattr(oauth_module, "_refresh_oauth_token", refresh_oauth_token)
    app = Starlette()
    add_oauth_routes(app)
    client = TestClient(app)
    client.post(
        "/oauth/session",
        json={
            "access_token": "expired-access-token",
            "email": "aj@airbyte.io",
            "expires_at": 101_000,
            "refresh_token": "refresh-token-value",
            "refresh_expires_at": 200_000,
        },
    )

    response = client.get("/oauth/session")

    assert response.status_code == 200
    assert response.json()["oauth_authenticated"] is False


def test_oauth_session_route_rejects_tampered_cookie(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    app = Starlette()
    add_oauth_routes(app)
    client = TestClient(app)
    client.cookies.set("airbyte_ops_webapp_session", "invalid-cookie")

    response = client.get("/oauth/session")

    assert response.status_code == 200
    assert response.json()["oauth_authenticated"] is False


def test_ops_webapp_cloud_run_uses_oauth_secret_only() -> None:
    stack_source = (REPO_ROOT / "infra/ops-webapp/__main__.py").read_text()
    bootstrap_source = (REPO_ROOT / "infra/ops-webapp/BOOTSTRAP.md").read_text()

    assert "AIRBYTE_OPS_WEBAPP_OAUTH_CLIENT_SECRET" in stack_source
    assert "AIRBYTE_CLOUD_CLIENT_ID" not in stack_source
    assert "AIRBYTE_CLOUD_CLIENT_SECRET" not in stack_source
    assert "ops-webapp-airbyte-cloud-client" not in bootstrap_source


# --- Airbyte login gate tests ---


def _request_with_session_cookie(cookie_value: str) -> Request:
    headers: list[tuple[bytes, bytes]] = []
    if cookie_value:
        headers.append(
            (
                b"cookie",
                f"{oauth_module.OAUTH_SESSION_COOKIE_NAME}={cookie_value}".encode(),
            )
        )
    return Request({"type": "http", "headers": headers})


@pytest.mark.parametrize("add_routes,path", _PROTECTED_ROUTES)
def test_protected_page_redirects_unauthenticated(
    monkeypatch, add_routes, path
) -> None:
    monkeypatch.setattr(serve_module, "mock_only_enabled", lambda: False)
    app = Starlette()
    add_routes(app, _IMPORTMAP)

    response = TestClient(app).get(path, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "/authorization"


@pytest.mark.parametrize("add_routes,path", _PROTECTED_ROUTES)
def test_protected_page_served_when_authenticated(
    monkeypatch, add_routes, path
) -> None:
    monkeypatch.setattr(serve_module, "mock_only_enabled", lambda: False)
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    app = Starlette()
    add_oauth_routes(app)
    add_routes(app, _IMPORTMAP)
    client = TestClient(app)
    client.post(
        "/oauth/session",
        json={
            "access_token": "access-token-value",
            "email": "aj@airbyte.io",
            "expires_in": 60,
        },
    )

    response = client.get(path, follow_redirects=False)

    assert response.status_code == 200


@pytest.mark.parametrize("add_routes,path", _PROTECTED_ROUTES)
def test_protected_page_served_in_mock_mode(monkeypatch, add_routes, path) -> None:
    monkeypatch.setattr(serve_module, "mock_only_enabled", lambda: True)
    app = Starlette()
    add_routes(app, _IMPORTMAP)

    response = TestClient(app).get(path, follow_redirects=False)

    assert response.status_code == 200


def test_authorization_page_accessible_without_session(monkeypatch) -> None:
    monkeypatch.setattr(serve_module, "mock_only_enabled", lambda: False)
    app = Starlette()
    serve_module.add_authorization_routes(app, _IMPORTMAP)

    response = TestClient(app).get("/authorization", follow_redirects=False)

    assert response.status_code == 200
    assert 'const toolName = "ops_authorization";' in response.text


@pytest.mark.parametrize(
    "payload,expected",
    [
        pytest.param(
            {"access_token": "tok", "expires_at": 200_000},
            True,
            id="valid_unexpired_access_token",
        ),
        pytest.param(
            {
                "access_token": "tok",
                "expires_at": 90_000,
                "refresh_token": "ref",
                "refresh_expires_at": 200_000,
            },
            True,
            id="expired_access_token_live_refresh_token",
        ),
        pytest.param(
            {"access_token": "tok", "expires_at": 90_000, "refresh_token": "ref"},
            True,
            id="expired_access_token_refresh_without_expiry",
        ),
        pytest.param(
            {
                "access_token": "tok",
                "expires_at": 90_000,
                "refresh_token": "ref",
                "refresh_expires_at": 90_000,
            },
            False,
            id="expired_access_token_expired_refresh_token",
        ),
        pytest.param(
            {"access_token": "tok", "expires_at": 90_000},
            False,
            id="expired_access_token_no_refresh_token",
        ),
        pytest.param(
            {"access_token": "tok", "expires_at": 120_000},
            False,
            id="near_expiry_within_buffer_no_refresh",
        ),
        pytest.param(
            {
                "access_token": "tok",
                "expires_at": 120_000,
                "refresh_token": "ref",
                "refresh_expires_at": 200_000,
            },
            True,
            id="near_expiry_within_buffer_live_refresh",
        ),
    ],
)
def test_request_has_valid_session_evaluates_payload(
    monkeypatch, payload, expected
) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")
    monkeypatch.setattr(oauth_module, "_now_ms", lambda: 100_000)
    cookie_value = oauth_module._encode_oauth_session(payload)

    request = _request_with_session_cookie(cookie_value)

    assert oauth_module.request_has_valid_session(request) is expected


def test_request_has_valid_session_rejects_missing_cookie(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")

    request = _request_with_session_cookie("")

    assert oauth_module.request_has_valid_session(request) is False


def test_request_has_valid_session_rejects_tampered_cookie(monkeypatch) -> None:
    monkeypatch.setenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, "test-secret")

    request = _request_with_session_cookie("invalid-cookie")

    assert oauth_module.request_has_valid_session(request) is False


def test_request_has_valid_session_false_without_secret(monkeypatch) -> None:
    monkeypatch.delenv(state_module.OAUTH_CLIENT_SECRET_ENV_VAR, raising=False)

    request = _request_with_session_cookie("some-cookie")

    assert oauth_module.request_has_valid_session(request) is False


# --- Google login removal ---


@pytest.mark.parametrize(
    "method,path",
    [
        pytest.param("GET", "/google-oauth/callback", id="callback"),
        pytest.param("POST", "/google-oauth/token", id="token"),
        pytest.param("GET", "/google-oauth/session", id="session-get"),
        pytest.param("POST", "/google-oauth/session", id="session-post"),
        pytest.param("DELETE", "/google-oauth/session", id="session-delete"),
    ],
)
def test_google_oauth_routes_are_absent(method: str, path: str) -> None:
    """Removing the per-user Google login means the Google OAuth routes no
    longer exist; the webapp reaches the GCS tier export via the runtime
    service account."""
    app = Starlette()
    add_oauth_routes(app)

    registered = {route.path for route in app.routes if isinstance(route, Route)}
    assert path not in registered

    response = TestClient(app).request(method, path)
    assert response.status_code == 404


def test_no_google_module_and_actions() -> None:
    """The Google OAuth module is deleted and its JS actions are not aggregated
    into the webapp's action set."""
    with pytest.raises(ModuleNotFoundError):
        __import__("airbyte_ops_webapp.auth.google_oauth")

    script = serve_module._oauth_handlers_script()
    assert "startGoogleOAuth" not in script
    assert "google-oauth" not in script
