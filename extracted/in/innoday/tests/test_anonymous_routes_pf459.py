"""PF-459: three anonymous routes said more than a stranger should learn.

* ``/platform/health`` told anyone whether the platform org and platform users
  existed, the licence/config state, and (``?detailed=true``) which
  integrations were configured.
* ``/public/status`` gave out the database hostname, the env file, the port
  and row counts for six tables.
* ``/public/applications`` rate-limited on the left-most ``X-Forwarded-For``
  entry -- the one the client writes -- so a new fake address per request
  reset the limit.

Anonymous callers now get up/down only; a platform admin still gets the detail.
"""

import pytest

from src.routers import public as public_router

HEALTH = "/api/v1/platform/health"
STATUS = "/api/v1/public/status"
DETAIL_ONLY = {"port", "env_file", "db_host", "metrics"}


def _bearer(token):
    return {"Authorization": f"Bearer {token}"}


# --- /platform/health ------------------------------------------------------


def test_health_anonymous_gets_status_only(client):
    body = client.get(f"{HEALTH}?detailed=true").json()
    assert body == {"status": "healthy"}


def test_health_invalid_token_is_treated_as_anonymous_not_401(client):
    resp = client.get(HEALTH, headers=_bearer("idt_not-a-real-token"))
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


def test_health_non_platform_user_gets_status_only(client, make_user_with_cli_token):
    _, token = make_user_with_cli_token(is_platform_member=False)
    body = client.get(HEALTH, headers=_bearer(token)).json()
    assert set(body) == {"status"}


def test_health_platform_admin_gets_checks(client, make_user_with_cli_token):
    _, token = make_user_with_cli_token(is_platform_member=True)
    body = client.get(HEALTH, headers=_bearer(token)).json()
    assert "checks" in body
    assert body["checks"]["database_connection"] is True


# --- /public/status --------------------------------------------------------


def test_status_anonymous_has_no_host_env_file_port_or_counts(client):
    body = client.get(STATUS).json()
    assert body["status"] == "operational"
    assert "version" in body and "environment" in body
    assert DETAIL_ONLY.isdisjoint(body), sorted(DETAIL_ONLY & set(body))


def test_status_non_platform_user_has_no_detail(client, make_user_with_cli_token):
    _, token = make_user_with_cli_token(is_platform_member=False)
    body = client.get(STATUS, headers=_bearer(token)).json()
    assert DETAIL_ONLY.isdisjoint(body)


def test_status_platform_admin_gets_detail(
    client, make_user_with_cli_token, monkeypatch
):
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@myhost:5432/db")
    _, token = make_user_with_cli_token(is_platform_member=True)
    body = client.get(STATUS, headers=_bearer(token)).json()
    assert body["db_host"] == "myhost"
    assert isinstance(body["port"], int)
    assert isinstance(body["env_file"], str)
    assert "users_count" in body["metrics"]
    # A bare hostname: no credentials, port or path.
    assert not any(c in body["db_host"] for c in "@:/")


def test_status_admin_db_host_falls_back_without_database_url(
    client, make_user_with_cli_token, monkeypatch
):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    _, token = make_user_with_cli_token(is_platform_member=True)
    assert client.get(STATUS, headers=_bearer(token)).json()["db_host"] == "(unknown)"


# --- /public/applications rate limit ----------------------------------------


@pytest.fixture(autouse=True)
def _reset_hits():
    public_router._application_hits = {}
    yield
    public_router._application_hits = {}


def test_spoofed_leftmost_forwarded_for_does_not_reset_the_limit():
    """The proxy appends the real address on the right; the client writes the left.

    Four requests from one real address (the last hop), each claiming a new
    left-most address. Keyed on the left-most entry every one looked new.
    """
    from starlette.requests import Request

    def req(xff):
        return Request(
            {
                "type": "http",
                "headers": [(b"x-forwarded-for", xff.encode())],
                "client": ("10.0.0.1", 1234),
            }
        )

    addresses = [
        public_router._client_address(req(f"198.51.100.{i}, 203.0.113.7"))
        for i in range(4)
    ]
    assert set(addresses) == {"203.0.113.7"}
    results = [public_router._too_many_from(a) for a in addresses]
    assert results == [False, False, False, True]


def test_client_address_falls_back_to_the_connection_without_forwarded_for():
    from starlette.requests import Request

    r = Request({"type": "http", "headers": [], "client": ("192.0.2.4", 1)})
    assert public_router._client_address(r) == "192.0.2.4"


def test_railways_real_ip_header_wins():
    """Railway's edge documents `X-Real-IP` as the client's address; it is the
    one header the platform itself promises to set."""
    from starlette.requests import Request

    r = Request(
        {
            "type": "http",
            "headers": [
                (b"x-real-ip", b"203.0.113.9"),
                (b"x-forwarded-for", b"198.51.100.1, 203.0.113.7"),
            ],
            "client": ("10.0.0.1", 1),
        }
    )
    assert public_router._client_address(r) == "203.0.113.9"


def test_the_admin_check_never_raises_on_a_broken_database():
    """A token on a health poll during an outage must not turn "unhealthy"
    into a 500 -- the admin is the one who most needs the answer."""
    from unittest.mock import MagicMock

    from starlette.requests import Request

    from src.middleware.rbac import is_platform_admin_request

    session = MagicMock()
    session.exec.side_effect = RuntimeError("connection lost")
    session.execute.side_effect = RuntimeError("connection lost")
    session.get.side_effect = RuntimeError("connection lost")
    request = Request(
        {"type": "http", "headers": [(b"authorization", b"Bearer idt_anything")]}
    )
    assert is_platform_admin_request(request, session) is False


# --- the admin peek writes nothing (PF-463) --------------------------------


@pytest.mark.parametrize("route", [HEALTH, STATUS])
def test_admin_peek_does_not_stamp_token_last_used(
    client, db_engine, make_user_with_cli_token, route
):
    from sqlmodel import Session, select

    from src.domain.cli_token import CLIToken

    user, token = make_user_with_cli_token(is_platform_member=True)
    assert client.get(route, headers=_bearer(token)).status_code == 200
    with Session(db_engine) as s:
        row = s.exec(select(CLIToken).where(CLIToken.user_id == user.id)).one()
        assert row.last_used_at is None


def test_read_only_jwt_lookup_creates_no_user(db_engine, monkeypatch):
    from sqlmodel import Session, select

    from src.domain.user import User
    from src.middleware import token_auth

    monkeypatch.setattr(token_auth, "supabase_auth_configured", lambda: True)
    monkeypatch.setattr(token_auth, "verify_supabase_jwt", lambda _t: {})
    monkeypatch.setattr(
        token_auth,
        "extract_identity",
        lambda _c: {"supabase_user_id": "sub-new", "email": "new@example.com"},
    )
    with Session(db_engine) as s:
        assert token_auth._user_from_supabase_jwt("jwt", s, record_use=False) is None
        assert (
            s.exec(select(User).where(User.email == "new@example.com")).first() is None
        )
