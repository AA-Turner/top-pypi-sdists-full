"""Email verification gating for CLI tokens (#414).

A CLI token used to authenticate the moment it was minted -- `CLIToken.is_valid()`
checks only revoked/expired -- so nothing ever required the holder to prove they
control the email address. These cover the new gate and, just as importantly, that
it stays OFF by default: every existing user is unverified, so enabling it
unconditionally would invalidate every live token at once.
"""

from datetime import datetime
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.user import User
from src.middleware.token_auth import (
    UnverifiedEmailError,
    _assert_email_verified,
    require_verified_email,
)


class TestFlagDefaultsOff:
    def test_disabled_by_default(self, monkeypatch):
        monkeypatch.delenv("REQUIRE_VERIFIED_EMAIL", raising=False)
        assert require_verified_email() is False

    @pytest.mark.parametrize("raw", ["1", "true", "TRUE", "yes", "on"])
    def test_enabled_by_truthy_values(self, monkeypatch, raw):
        monkeypatch.setenv("REQUIRE_VERIFIED_EMAIL", raw)
        assert require_verified_email() is True

    @pytest.mark.parametrize("raw", ["0", "false", "no", "off", ""])
    def test_disabled_by_falsy_values(self, monkeypatch, raw):
        monkeypatch.setenv("REQUIRE_VERIFIED_EMAIL", raw)
        assert require_verified_email() is False


class TestAssertEmailVerified:
    def _user(self, verified: bool) -> User:
        return User(
            id=str(uuid4()),
            email="x@example.com",
            full_name="X",
            email_verified_at=datetime.utcnow() if verified else None,
        )

    def test_unverified_passes_while_flag_off(self, monkeypatch):
        monkeypatch.delenv("REQUIRE_VERIFIED_EMAIL", raising=False)
        _assert_email_verified(self._user(verified=False))  # must not raise

    def test_unverified_blocked_when_flag_on(self, monkeypatch):
        monkeypatch.setenv("REQUIRE_VERIFIED_EMAIL", "true")
        with pytest.raises(UnverifiedEmailError) as ei:
            _assert_email_verified(self._user(verified=False))
        assert "not been verified" in str(ei.value)

    def test_verified_passes_when_flag_on(self, monkeypatch):
        monkeypatch.setenv("REQUIRE_VERIFIED_EMAIL", "true")
        _assert_email_verified(self._user(verified=True))  # must not raise


class TestUserModelHelpers:
    def test_email_verified_property(self):
        u = User(email="a@b.c", full_name="A")
        assert u.email_verified is False
        u.mark_email_verified()
        assert u.email_verified is True

    def test_mark_is_idempotent(self):
        u = User(email="a@b.c", full_name="A")
        u.mark_email_verified(datetime(2026, 1, 1))
        u.mark_email_verified(datetime(2026, 6, 1))
        assert u.email_verified_at == datetime(2026, 1, 1)


class TestTokenAuthEndToEnd:
    """The gate must fire on the real CLI-token path, not just the helper."""

    def test_unverified_token_rejected_with_403_when_enforced(
        self, client, make_user_with_cli_token, monkeypatch
    ):
        _user, token = make_user_with_cli_token(is_platform_member=True)
        monkeypatch.setenv("REQUIRE_VERIFIED_EMAIL", "true")
        resp = client.get(
            "/api/v1/platform/reports/project-access",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403, resp.text
        assert "not been verified" in resp.text

    def test_same_token_works_once_verified(
        self, client, db_engine, make_user_with_cli_token, monkeypatch
    ):
        """Verification must not require re-minting the token."""
        user, token = make_user_with_cli_token(is_platform_member=True)
        monkeypatch.setenv("REQUIRE_VERIFIED_EMAIL", "true")

        with Session(db_engine) as s:
            row = s.get(User, user.id)
            row.mark_email_verified()
            s.add(row)
            s.commit()

        resp = client.get(
            "/api/v1/platform/reports/project-access",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code != 403, resp.text

    def test_unverified_token_still_works_while_flag_off(
        self, client, make_user_with_cli_token, monkeypatch
    ):
        """The rollout guarantee: nothing breaks until the flag is flipped."""
        _user, token = make_user_with_cli_token(is_platform_member=True)
        monkeypatch.delenv("REQUIRE_VERIFIED_EMAIL", raising=False)
        resp = client.get(
            "/api/v1/platform/reports/project-access",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code != 403, resp.text


class TestExtractIdentityCapturesConfirmation:
    def test_top_level_claim(self):
        from src.services.supabase_auth import extract_identity

        got = extract_identity(
            {
                "sub": "s1",
                "email": "a@b.c",
                "email_confirmed_at": "2026-01-01T00:00:00Z",
            }
        )
        assert got["email_confirmed_at"] == "2026-01-01T00:00:00Z"

    def test_user_metadata_fallback(self):
        from src.services.supabase_auth import extract_identity

        got = extract_identity(
            {"sub": "s1", "email": "a@b.c", "user_metadata": {"email_verified": True}}
        )
        assert got["email_confirmed_at"] is True

    def test_absent_means_unverified(self):
        from src.services.supabase_auth import extract_identity

        got = extract_identity({"sub": "s1", "email": "a@b.c"})
        assert got["email_confirmed_at"] is None


class TestUserCreationRequiresAuthIdentity:
    """POST /users must not mint a user who could never sign in.

    This is how 8 users ended up with zero rows in auth.users: the row was
    created and the invite was never attempted.
    """

    def test_refuses_when_supabase_unconfigured(self, client, make_user_with_cli_token):
        from unittest.mock import patch

        from src.services.supabase_invite import InviteDispatchResult

        _u, token = make_user_with_cli_token(is_platform_member=True)
        with patch(
            "src.services.user_provisioning.send_supabase_invite",
            return_value=InviteDispatchResult(configured=False),
        ):
            resp = client.post(
                "/api/v1/users",
                json={"email": "new@example.com", "full_name": "New"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert resp.status_code == 503, resp.text
        assert "auth identity" in resp.text

    def test_surfaces_invite_failure(self, client, make_user_with_cli_token):
        from unittest.mock import patch

        from src.services.supabase_invite import InviteDispatchResult

        _u, token = make_user_with_cli_token(is_platform_member=True)
        with patch(
            "src.services.user_provisioning.send_supabase_invite",
            return_value=InviteDispatchResult(configured=True, error="rate limited"),
        ):
            resp = client.post(
                "/api/v1/users",
                json={"email": "new2@example.com", "full_name": "New"},
                headers={"Authorization": f"Bearer {token}"},
            )
        assert resp.status_code == 502, resp.text
        assert "rate limited" in resp.text

    def test_links_identity_and_leaves_email_unverified(
        self, client, db_engine, make_user_with_cli_token, stub_supabase_invite
    ):
        _u, token = make_user_with_cli_token(is_platform_member=True)
        resp = client.post(
            "/api/v1/users",
            json={"email": "invited@example.com", "full_name": "Invited"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201, resp.text
        with Session(db_engine) as s:
            from sqlmodel import select

            row = s.exec(
                select(User).where(User.email == "invited@example.com")
            ).first()
        assert row.supabase_user_id == "stub-supabase-uid"
        # The invite email is what verifies the address; acceptance sets this.
        assert row.email_verified_at is None


class TestAuthCallbackPage:
    """The landing page for a Supabase invite / magic link (#414).

    Three code paths pointed Supabase's ``redirect_to`` at ``/auth/callback``
    while **nothing served it**. A live probe of dev returned 401 — not 404,
    because ``TeamSecretMiddleware`` rejected it before routing. Every invite
    recipient would have hit that wall: confirmed at the IdP, still unverified
    in InnoDay, which is precisely the lockout the flag was meant to avoid.
    """

    def test_page_is_served(self, client):
        resp = client.get("/auth/callback")
        assert resp.status_code == 200, resp.text
        assert "text/html" in resp.headers["content-type"]

    def test_page_needs_no_credential(self, client):
        """It holds no secret — the session is in the fragment, which the
        server never receives. So it must be reachable with no headers."""
        assert client.get("/auth/callback").status_code == 200

    def test_page_reads_the_url_fragment_not_the_query_string(self, client):
        """Supabase returns the session after '#', which is never sent to the
        server. A query-string implementation would silently never work."""
        body = client.get("/auth/callback").text
        assert "location.hash" in body
        assert "access_token" in body

    def test_page_posts_to_confirm_email(self, client):
        assert "/api/v1/auth/confirm-email" in client.get("/auth/callback").text

    def test_page_surfaces_an_idp_error(self, client):
        """An expired link comes back as error_description in the fragment."""
        assert "error_description" in client.get("/auth/callback").text

    def test_page_stores_the_token_where_invite_accept_looks(self, client):
        """So the two pages compose: land here, then accept a pending invite."""
        assert "innoday_token" in client.get("/auth/callback").text


class TestConfirmEmailEndpoint:
    def test_requires_a_credential(self, client):
        assert client.post("/api/v1/auth/confirm-email").status_code == 401

    def test_reports_verification_state(
        self, client, db_engine, make_user_with_cli_token
    ):
        user, token = make_user_with_cli_token()
        resp = client.post(
            "/api/v1/auth/confirm-email",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["email"] == user.email
        assert body["verified"] is False

        with Session(db_engine) as s:
            row = s.get(User, user.id)
            row.mark_email_verified()
            s.add(row)
            s.commit()

        body = client.post(
            "/api/v1/auth/confirm-email",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert body["verified"] is True
        assert body["verified_at"] is not None


class TestTeamSecretExemptions:
    """A browser arriving from an email cannot send X-Team-Secret."""

    def test_callback_and_confirm_are_exempt(self):
        from src.api.middleware.team_secret import EXEMPT_PATHS

        assert "/auth/callback" in EXEMPT_PATHS
        assert "/api/v1/auth/confirm-email" in EXEMPT_PATHS

    def test_confirm_email_is_exempt_from_the_secret_but_not_from_auth(self, client):
        """Exempt from the door key is not the same as public."""
        from src.api.middleware.team_secret import EXEMPT_PATHS

        assert "/api/v1/auth/confirm-email" in EXEMPT_PATHS
        assert client.post("/api/v1/auth/confirm-email").status_code == 401


class TestFetchConfirmedIdentities:
    """`--reconcile` reads the IdP directly, so it must degrade clearly."""

    def test_reports_missing_configuration(self, monkeypatch):
        from src.services.supabase_invite import fetch_confirmed_identities

        monkeypatch.delenv("SUPABASE_URL", raising=False)
        monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
        identities, error = fetch_confirmed_identities()
        assert identities is None
        assert "SUPABASE_URL" in error

    def test_pages_through_and_maps_confirmation(self, monkeypatch):
        from types import SimpleNamespace

        import src.services.supabase_invite as si

        monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
        monkeypatch.setenv("SUPABASE_SERVICE_KEY", "service-key")

        rows = [
            SimpleNamespace(id="s1", email="a@b.c", email_confirmed_at="2026-08-04"),
            SimpleNamespace(id="s2", email="d@e.f", email_confirmed_at=None),
        ]
        fake_client = SimpleNamespace(
            auth=SimpleNamespace(
                admin=SimpleNamespace(list_users=lambda page, per_page: rows)
            )
        )
        monkeypatch.setattr(
            si, "create_client", lambda *a, **k: fake_client, raising=False
        )
        import sys

        monkeypatch.setitem(
            sys.modules,
            "supabase",
            SimpleNamespace(create_client=lambda *a, **k: fake_client),
        )

        identities, error = si.fetch_confirmed_identities()
        assert error is None
        assert [i.supabase_user_id for i in identities] == ["s1", "s2"]
        assert identities[0].email_confirmed_at == "2026-08-04"
        assert identities[1].email_confirmed_at is None
