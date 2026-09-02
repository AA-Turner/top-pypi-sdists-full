"""P1 auth: cli_tokens, unified Bearer resolver, and bootstrap (PF-350, #350).

Covers:
  - CLIToken model: hashing, validity (revoked/expired), mark_used
  - resolve_user_from_request: Bearer idt_/ido_/idr_/legacy-innoday_ token
    path + team-secret fallback
  - /api/v1/auth/tokens mint/list/revoke round-trip
  - seed_platform_user bootstrap: platform flag, token mint, idempotency, NO rows
"""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.cli_token import (
    CLIToken,
    generate_cli_token,
    hash_cli_token,
    org_alias_hash,
)
from src.domain.organization import OrganizationMembership
from src.domain.user import User
from src.services.bootstrap import seed_platform_user

# db_engine + client fixtures are provided by tests/conftest.py.


def _revoked(token: CLIToken) -> CLIToken:
    token.revoke()
    return token


def _make_user(session, **kw) -> User:
    user = User(
        id=str(uuid4()),
        email=kw.pop("email", f"{uuid4().hex[:8]}@example.com"),
        full_name=kw.pop("full_name", "Test User"),
        **kw,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


class TestCLITokenModel:
    def test_generate_and_hash_format(self):
        # Default kind is a PAT with the plat0 sentinel (no org alias given).
        raw = generate_cli_token()
        assert raw.startswith("idt_plat0.")
        h = hash_cli_token(raw)
        assert len(h) == 64 and h != raw  # sha256 hex, not the raw value

    @pytest.mark.parametrize(
        "kind, prefix",
        [("pat", "idt_"), ("oauth", "ido_"), ("refresh", "idr_")],
    )
    def test_generate_prefix_per_kind(self, kind, prefix):
        raw = generate_cli_token(kind=kind, org_alias="brightpower")
        assert raw.startswith(prefix)
        # <kind><orghash>.<secret> — org segment then a dot before the secret.
        assert "." in raw
        assert raw.split(".", 1)[0] == f"{prefix}{org_alias_hash('brightpower')}"

    def test_generate_unknown_kind_raises(self):
        with pytest.raises(ValueError):
            generate_cli_token(kind="bogus")

    def test_org_alias_hash_stable_and_sentinel(self):
        assert org_alias_hash("brightpower") == org_alias_hash("brightpower")
        assert len(org_alias_hash("brightpower")) == 5
        assert org_alias_hash(None) == "plat0"
        assert org_alias_hash("") == "plat0"

    @pytest.mark.parametrize(
        "make_token, expected_valid",
        [
            (lambda: CLIToken(user_id="u", token_hash="x"), True),
            (lambda: _revoked(CLIToken(user_id="u", token_hash="x")), False),
            (
                lambda: CLIToken(
                    user_id="u",
                    token_hash="x",
                    expires_at=datetime.now(timezone.utc) - timedelta(days=1),
                ),
                False,
            ),
            (
                lambda: CLIToken(
                    user_id="u",
                    token_hash="x",
                    expires_at=datetime.now(timezone.utc) + timedelta(days=1),
                ),
                True,
            ),
        ],
        ids=["fresh", "revoked", "expired", "future-expiry"],
    )
    def test_is_valid(self, make_token, expected_valid):
        assert make_token().is_valid() is expected_valid

    def test_revoke_sets_timestamp(self):
        t = CLIToken(user_id="u", token_hash="x")
        t.revoke()
        assert t.revoked_at is not None


class TestBearerTokenAuth:
    def test_cli_token_authenticates(self, client, db_engine):
        with Session(db_engine) as s:
            user = _make_user(s)
            user_id = user.id
            raw = generate_cli_token()
            s.add(CLIToken(user_id=user.id, token_hash=hash_cli_token(raw)))
            s.commit()

        resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {raw}"})
        assert resp.status_code == 200
        assert resp.json()["id"] == user_id

    @pytest.mark.parametrize(
        "raw_token",
        [
            "idt_a1b2c." + generate_cli_token(kind="pat").split(".", 1)[1],
            "ido_a1b2c." + generate_cli_token(kind="oauth").split(".", 1)[1],
            "idr_a1b2c." + generate_cli_token(kind="refresh").split(".", 1)[1],
            "innoday_legacyTokenStillWorks123456",  # legacy prefix, still accepted
        ],
        ids=["idt", "ido", "idr", "legacy_innoday"],
    )
    def test_all_prefixes_authenticate(self, client, db_engine, raw_token):
        """The resolver routes every id?_ prefix AND legacy innoday_ to the
        CLI-token hash lookup — proving new prefixes work and old tokens still
        authenticate (backward compatibility for already-seeded users)."""
        with Session(db_engine) as s:
            user = _make_user(s)
            user_id = user.id
            s.add(CLIToken(user_id=user.id, token_hash=hash_cli_token(raw_token)))
            s.commit()

        resp = client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {raw_token}"}
        )
        assert resp.status_code == 200
        assert resp.json()["id"] == user_id

    def test_revoked_cli_token_rejected(self, client, db_engine):
        with Session(db_engine) as s:
            user = _make_user(s)
            raw = generate_cli_token()
            tok = CLIToken(user_id=user.id, token_hash=hash_cli_token(raw))
            tok.revoke()
            s.add(tok)
            s.commit()

        resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {raw}"})
        assert resp.status_code == 401

    def test_unknown_bearer_token_rejected(self, client, db_engine):
        with Session(db_engine) as s:
            _make_user(s)
        resp = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer innoday_nonexistent"},
        )
        assert resp.status_code == 401

    def test_no_auth_rejected(self, client):
        assert client.get("/api/v1/auth/me").status_code == 401

    def test_last_used_stamped(self, client, db_engine):
        with Session(db_engine) as s:
            user = _make_user(s)
            raw = generate_cli_token()
            tok = CLIToken(user_id=user.id, token_hash=hash_cli_token(raw))
            s.add(tok)
            s.commit()
            token_id = tok.id
            assert tok.last_used_at is None

        client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {raw}"})

        with Session(db_engine) as s:
            refreshed = s.get(CLIToken, token_id)
            assert refreshed.last_used_at is not None


class TestTokenEndpoints:
    def test_mint_list_revoke_roundtrip(self, client, db_engine):
        with Session(db_engine) as s:
            user = _make_user(s)
            raw = generate_cli_token()
            s.add(CLIToken(user_id=user.id, token_hash=hash_cli_token(raw)))
            s.commit()

        auth = {"Authorization": f"Bearer {raw}"}

        # mint a second token
        mint = client.post("/api/v1/auth/tokens", json={"name": "laptop"}, headers=auth)
        assert mint.status_code == 200
        minted = mint.json()
        # PAT endpoint mints an idt_ token; this user has no default org → plat0.
        assert minted["token"].startswith("idt_plat0.")
        assert minted["name"] == "laptop"
        new_id = minted["id"]

        # the freshly minted token also authenticates
        assert (
            client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {minted['token']}"},
            ).status_code
            == 200
        )

        # list shows both
        listing = client.get("/api/v1/auth/tokens", headers=auth)
        assert listing.status_code == 200
        assert len(listing.json()) == 2

        # revoke the new one
        rev = client.delete(f"/api/v1/auth/tokens/{new_id}", headers=auth)
        assert rev.status_code == 200

        # now the revoked token no longer authenticates
        assert (
            client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {minted['token']}"},
            ).status_code
            == 401
        )


class TestBootstrapSeeding:
    def test_seed_creates_platform_user_and_token(self, db_engine):
        with Session(db_engine) as s:
            result = seed_platform_user(s, email="founder@hs.com", full_name="Founder")
            assert result.created_user is True
            assert result.user.is_platform_member is True
            # Platform users are cross-org → PAT with the plat0 sentinel.
            assert result.raw_token.startswith("idt_plat0.")

            # token is persisted (hashed) and valid
            tok = s.exec(
                select_cli_token_by_hash(hash_cli_token(result.raw_token))
            ).first()
            assert tok is not None
            assert tok.is_valid()

            # NO membership rows created — platform access is by bypass
            rows = s.exec(select_memberships_for_user(result.user.id)).all()
            assert rows == []

    def test_seed_is_idempotent_on_existing_user(self, db_engine):
        with Session(db_engine) as s:
            u = _make_user(s, email="dev@hs.com", is_platform_member=False)
            uid = u.id

        with Session(db_engine) as s:
            result = seed_platform_user(s, email="dev@hs.com")
            assert result.created_user is False
            assert result.user.id == uid  # reused, not duplicated
            assert result.user.is_platform_member is True  # promoted


# Small helpers to keep the select imports local to this test file.
def select_cli_token_by_hash(token_hash):
    from sqlmodel import select

    return select(CLIToken).where(CLIToken.token_hash == token_hash)


def select_memberships_for_user(user_id):
    from sqlmodel import select

    return select(OrganizationMembership).where(
        OrganizationMembership.user_id == user_id
    )
