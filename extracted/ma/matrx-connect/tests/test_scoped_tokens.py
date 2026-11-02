import time
import uuid
from datetime import datetime

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from matrx_connect import ScopedTokenError, ScopedTokenIssuer
from matrx_connect.middleware.auth import AuthMiddleware


def _keypair_pem() -> str:
    key = ec.generate_private_key(ec.SECP256R1())
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")


@pytest.fixture()
def issuer() -> ScopedTokenIssuer:
    return ScopedTokenIssuer(issuer="matrx-broker", private_key_pem=_keypair_pem())


def test_mint_verify_roundtrip(issuer: ScopedTokenIssuer):
    token, expires_at = issuer.mint(
        user_id="u-1", audience="anthropic", tier_policy="mid", scopes=("messages",)
    )
    grant = issuer.verify(token, audience="anthropic")
    assert grant.user_id == "u-1"
    assert grant.audience == "anthropic"
    assert grant.tier_policy == "mid"
    assert grant.scopes == ("messages",)
    assert grant.expires_at == expires_at
    assert grant.token_id


def test_wrong_audience_rejected(issuer: ScopedTokenIssuer):
    token, _ = issuer.mint(user_id="u-1", audience="anthropic", tier_policy="none")
    with pytest.raises(ScopedTokenError):
        issuer.verify(token, audience="openai_realtime")


def test_tier_policy_is_required_and_explicit(issuer: ScopedTokenIssuer):
    with pytest.raises(ValueError):
        issuer.mint(user_id="u-1", audience="a", tier_policy="")
    with pytest.raises(ValueError):
        issuer.mint(user_id="u-1", audience="a", tier_policy="premium")


def test_expired_token_rejected(issuer: ScopedTokenIssuer):
    token, _ = issuer.mint(
        user_id="u-1", audience="a", tier_policy="none", ttl_seconds=1
    )
    # Clamp floor is 1s — wait it out.
    time.sleep(1.2)
    with pytest.raises(ScopedTokenError):
        issuer.verify(token, audience="a")


def test_tampered_token_rejected(issuer: ScopedTokenIssuer):
    token, _ = issuer.mint(user_id="u-1", audience="a", tier_policy="none")
    header, payload, sig = token.split(".")
    with pytest.raises(ScopedTokenError):
        issuer.verify(f"{header}.{payload}x.{sig}", audience="a")


def test_foreign_issuer_rejected(issuer: ScopedTokenIssuer):
    other = ScopedTokenIssuer(issuer="someone-else", private_key_pem=_keypair_pem())
    token, _ = other.mint(user_id="u-1", audience="a", tier_policy="none")
    with pytest.raises(ScopedTokenError):
        issuer.verify(token, audience="a")


def test_extra_claims_cannot_override_identity(issuer: ScopedTokenIssuer):
    token, _ = issuer.mint(
        user_id="u-1",
        audience="a",
        tier_policy="none",
        extra_claims={"sub": "attacker", "aud": "everything", "custom": "ok"},
    )
    grant = issuer.verify(token, audience="a")
    assert grant.user_id == "u-1"
    assert grant.claims.get("custom") == "ok"


def test_bearer_grant_parses_header(issuer: ScopedTokenIssuer):
    token, _ = issuer.mint(user_id="u-1", audience="a", tier_policy="guest")
    grant = issuer.bearer_grant(f"Bearer {token}", audience="a")
    assert grant.tier_policy == "guest"
    for bad in (None, "", "Basic abc", "Bearer"):
        with pytest.raises(ScopedTokenError):
            issuer.bearer_grant(bad, audience="a")


@pytest.mark.asyncio
async def test_middleware_passthrough_issuer_silently_falls_through(
    issuer: ScopedTokenIssuer,
):
    async def noop_app(scope, receive, send):
        return None

    mw = AuthMiddleware(
        noop_app,
        jwt_secret="test-secret",
        passthrough_issuers=("matrx-broker",),
    )
    token, _ = issuer.mint(user_id="u-1", audience="a", tier_policy="none")
    assert await mw.verify_token_raw(token) is None

    # A non-passthrough HS256 token still verifies normally.
    user_token = jwt.encode(
        {"sub": "u-2", "aud": "authenticated", "exp": int(time.time()) + 60},
        "test-secret",
        algorithm="HS256",
    )
    verified = await mw.verify_token_raw(user_token)
    assert verified is not None and verified.user_id == "u-2"


def test_bound_mint_verify_preserves_persisted_authority(issuer: ScopedTokenIssuer):
    now_ms = int(time.time() * 1000)
    jti = "11111111-1111-4111-8111-111111111111"
    token = issuer.mint_bound(
        user_id="u-1",
        audience="bound",
        tier_policy="none",
        scopes=(),
        issued_at_ms=now_ms - 1_000,
        deadline_ms=now_ms + 30_000,
        jti=jti,
        extra_claims={"v": 1},
    )
    bound = issuer.verify_bound(token, audience="bound")
    assert bound.token_id == jti and bound.issued_at == (now_ms - 1_000) // 1000
    assert bound.claims["v"] == 1 and bound.tier_policy == "none" and bound.scopes == ()


def test_bound_rejects_invalid_authority_and_keeps_normal_mint(
    issuer: ScopedTokenIssuer,
):
    now_ms = int(time.time() * 1000)
    with pytest.raises(ValueError):
        issuer.mint_bound(
            user_id="u",
            audience="a",
            tier_policy="none",
            scopes=(),
            issued_at_ms=now_ms,
            deadline_ms=now_ms,
            jti=str(uuid.uuid4()),
            extra_claims={},
        )
    with pytest.raises(ValueError):
        issuer.mint_bound(
            user_id="u",
            audience="a",
            tier_policy="none",
            scopes=(),
            issued_at_ms=now_ms + 6_000,
            deadline_ms=now_ms + 70_000,
            jti=str(uuid.uuid4()),
            extra_claims={},
        )
    token, _ = issuer.mint(user_id="u", audience="normal", tier_policy="guest")
    assert issuer.verify(token, audience="normal").tier_policy == "guest"


def test_bound_verifier_refuses_non_es256_token(issuer: ScopedTokenIssuer):
    forged = jwt.encode(
        {
            "iss": issuer.issuer,
            "aud": "bound",
            "sub": "u",
            "iat": int(time.time()) - 1,
            "exp": int(time.time()) + 60,
            "jti": str(uuid.uuid4()),
            "tier_policy": "none",
            "scopes": [],
        },
        "not-the-es256-key",
        algorithm="HS256",
    )
    with pytest.raises(ScopedTokenError):
        issuer.verify_bound(forged, audience="bound")


def test_bound_remints_preserve_exact_persisted_floor_authority(
    monkeypatch, issuer: ScopedTokenIssuer
):
    import matrx_connect.scoped_tokens as scoped_tokens

    monkeypatch.setattr(scoped_tokens.time, "time", lambda: 2_000.0)

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromtimestamp(2_000.0, tz=tz)

    monkeypatch.setattr(jwt.api_jwt, "datetime", Clock)
    authority = dict(
        issued_at_ms=1_999_100,
        deadline_ms=2_060_900,
        jti="11111111-1111-4111-8111-111111111111",
    )
    first = issuer.mint_bound(
        user_id="u",
        audience="bound",
        tier_policy="none",
        scopes=(),
        extra_claims={"v": 1},
        **authority,
    )
    second = issuer.mint_bound(
        user_id="u",
        audience="bound",
        tier_policy="none",
        scopes=(),
        extra_claims={"v": 1},
        **authority,
    )
    for token in (first, second):
        grant = issuer.verify_bound(token, audience="bound")
        assert (grant.token_id, grant.issued_at, grant.expires_at) == (
            authority["jti"],
            1_999,
            2_060,
        )


def test_bound_iat_five_seconds_is_allowed_but_more_is_refused(
    monkeypatch, issuer: ScopedTokenIssuer
):
    import matrx_connect.scoped_tokens as scoped_tokens

    monkeypatch.setattr(scoped_tokens.time, "time", lambda: 2_000.0)

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromtimestamp(2_000.0, tz=tz)

    monkeypatch.setattr(jwt.api_jwt, "datetime", Clock)
    token = issuer.mint_bound(
        user_id="u",
        audience="bound",
        tier_policy="none",
        scopes=(),
        issued_at_ms=2_005_000,
        deadline_ms=2_060_000,
        jti="11111111-1111-4111-8111-111111111111",
        extra_claims={},
    )
    assert issuer.verify_bound(token, audience="bound").issued_at == 2_005
    monkeypatch.setattr(scoped_tokens.time, "time", lambda: 1_999.0)
    with pytest.raises(ScopedTokenError):
        issuer.verify_bound(token, audience="bound")


def test_bound_expiry_has_zero_leeway(monkeypatch, issuer: ScopedTokenIssuer):
    import matrx_connect.scoped_tokens as scoped_tokens

    monkeypatch.setattr(scoped_tokens.time, "time", lambda: 2_000.0)

    class Clock(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromtimestamp(2_000.0, tz=tz)

    monkeypatch.setattr(jwt.api_jwt, "datetime", Clock)
    token = issuer.mint_bound(
        user_id="u",
        audience="bound",
        tier_policy="none",
        scopes=(),
        issued_at_ms=1_999_000,
        deadline_ms=2_001_000,
        jti="11111111-1111-4111-8111-111111111111",
        extra_claims={},
    )
    monkeypatch.setattr(scoped_tokens.time, "time", lambda: 2_001.0)

    class ExpiredClock(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromtimestamp(2_001.0, tz=tz)

    monkeypatch.setattr(jwt.api_jwt, "datetime", ExpiredClock)
    with pytest.raises(ScopedTokenError):
        issuer.verify_bound(token, audience="bound")
    receipt = issuer.verify_bound_receipt(token, audience="bound")
    assert receipt.token_id == "11111111-1111-4111-8111-111111111111"
