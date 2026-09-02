"""P1 auth: Supabase JWT verification (PF-350, #350).

Exercises the HS256 shared-secret fallback path (no network) and the
identity extraction / config-detection helpers. The JWKS (RS256) path is
covered structurally via config detection; a full RS256 round-trip would
require standing up a fake JWKS endpoint, deferred to integration tests.
"""

from datetime import datetime, timedelta, timezone

import jwt
import pytest

from src.services.supabase_auth import (
    SupabaseAuthError,
    extract_identity,
    supabase_auth_configured,
    verify_supabase_jwt,
)

SECRET = "test-supabase-jwt-secret"


def _make_jwt(claims, secret=SECRET, alg="HS256"):
    base = {
        "sub": "sb-user-123",
        "email": "person@example.com",
        "aud": "authenticated",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    base.update(claims)
    return jwt.encode(base, secret, algorithm=alg)


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for var in (
        "SUPABASE_URL",
        "SUPABASE_JWKS_URL",
        "SUPABASE_JWT_SECRET",
        "SUPABASE_JWT_AUD",
    ):
        monkeypatch.delenv(var, raising=False)
    yield


class TestConfigDetection:
    @pytest.mark.parametrize(
        "env_var, value, expected",
        [
            (None, None, False),  # nothing set
            ("SUPABASE_JWT_SECRET", SECRET, True),
            ("SUPABASE_URL", "https://abc.supabase.co", True),
        ],
        ids=["unset", "via-secret", "via-url"],
    )
    def test_configured(self, monkeypatch, env_var, value, expected):
        if env_var:
            monkeypatch.setenv(env_var, value)
        assert supabase_auth_configured() is expected


class TestHS256Verification:
    def test_valid_token_returns_claims(self, monkeypatch):
        monkeypatch.setenv("SUPABASE_JWT_SECRET", SECRET)
        token = _make_jwt({"sub": "sb-42", "email": "a@b.com"})
        claims = verify_supabase_jwt(token)
        assert claims["sub"] == "sb-42"
        assert claims["email"] == "a@b.com"

    def test_wrong_secret_rejected(self, monkeypatch):
        monkeypatch.setenv("SUPABASE_JWT_SECRET", SECRET)
        token = _make_jwt({}, secret="wrong-secret")
        with pytest.raises(SupabaseAuthError):
            verify_supabase_jwt(token)

    def test_wrong_audience_rejected(self, monkeypatch):
        monkeypatch.setenv("SUPABASE_JWT_SECRET", SECRET)
        token = _make_jwt({"aud": "not-authenticated"})
        with pytest.raises(SupabaseAuthError):
            verify_supabase_jwt(token)

    def test_expired_token_rejected(self, monkeypatch):
        monkeypatch.setenv("SUPABASE_JWT_SECRET", SECRET)
        token = _make_jwt({"exp": datetime.now(timezone.utc) - timedelta(hours=1)})
        with pytest.raises(SupabaseAuthError):
            verify_supabase_jwt(token)

    def test_no_config_raises(self):
        token = _make_jwt({})
        with pytest.raises(SupabaseAuthError):
            verify_supabase_jwt(token)


class TestIdentityExtraction:
    def test_extracts_sub_email_name(self):
        claims = {
            "sub": "sb-1",
            "email": "x@y.com",
            "user_metadata": {"full_name": "Ex Ample"},
        }
        ident = extract_identity(claims)
        assert ident["supabase_user_id"] == "sb-1"
        assert ident["email"] == "x@y.com"
        assert ident["full_name"] == "Ex Ample"

    def test_falls_back_to_metadata_email_and_name(self):
        claims = {"sub": "sb-2", "user_metadata": {"email": "m@e.com", "name": "M E"}}
        ident = extract_identity(claims)
        assert ident["email"] == "m@e.com"
        assert ident["full_name"] == "M E"
