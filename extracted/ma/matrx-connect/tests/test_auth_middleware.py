"""End-to-end tests for `AuthMiddleware._validate_token`.

These tests are platform tests, not artefact tests: every assertion locks in a
behavior the rest of the Matrx ecosystem (and any downstream consumer of
matrx-connect) silently relies on. They are written to fail loudly the moment
the behavior drifts.

Coverage:

* admin-token bearer is accepted exactly when configured
* a real HS256 JWT is decoded, claims are stashed under ``jwt_claims``, and
  the resolved ``AppContext`` reports ``is_authenticated=True``
* an invalid HS256 JWT (correct shape, wrong signature) is rejected loudly
  — that case logs a ``JWT validation FAILED`` ERROR and the middleware
  returns ``None``
* a non-JWT bearer (single opaque segment, no dots) is rejected SILENTLY,
  with no stderr output, regardless of how many times the middleware is
  invoked. This is the regression guard for the sandbox-bridge / future
  service-token classes of bearer scheme — they MUST NOT trigger
  misleading "JWT validation FAILED: Not enough segments" log noise.
"""

from __future__ import annotations

import logging
import asyncio
import time

import jwt
import pytest
from matrx_connect.context.app_context import AppContext
from matrx_connect.emitters.stream_emitter import StreamEmitter
from matrx_connect.middleware.auth import AuthMiddleware

# 64-char secret, matches Supabase production-shape and clears PyJWT's
# 32-byte minimum-length recommendation for HS256 (avoids
# InsecureKeyLengthWarning noise in test output).
JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
WRONG_JWT_SECRET = "wrong-secret-do-not-use-in-prod-wrong-secret-do-not-use-in-pAB12"
USER_ID = "11111111-1111-4111-8111-111111111111"


def _empty_ctx() -> AppContext:
    return AppContext(
        ip_address="127.0.0.1",
        user_agent="pytest",
        emitter=StreamEmitter(debug=False),
        request_id="req-test",
    )


def _middleware(*, jwt_secret: str = JWT_SECRET) -> AuthMiddleware:
    return AuthMiddleware(
        app=lambda *a, **kw: None,  # never invoked by _validate_token
        jwt_secret=jwt_secret,
        guest_fingerprint_secret="synthetic-stable-test-fingerprint-secret",
    )


def _make_jwt(*, claims: dict | None = None, secret: str = JWT_SECRET) -> str:
    payload = {
        "sub": USER_ID,
        "email": "user@example.com",
        "aud": "authenticated",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    if claims:
        payload.update(claims)
    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.mark.asyncio
async def test_static_admin_token_no_longer_accepted() -> None:
    """The admin-token escape hatch was removed in 2026-05. A token that
    isn't a valid Supabase JWT must NOT authenticate anyone, regardless of
    whether admin_token kwargs are passed in."""
    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        # Even if a host accidentally still passes these (back-compat
        # kwargs), they must NOT grant access. The middleware accepts the
        # kwargs but ignores them with a stderr warning.
        admin_token="admin-static-token",
        admin_user_id="00000000-0000-4000-8000-000000000001",
    )
    ctx = await mw._validate_token(
        "Bearer admin-static-token",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    # Either the validator returns None, or it returns an unauthenticated ctx.
    assert ctx is None or ctx.is_authenticated is False, (
        "static admin token authenticated — escape hatch wasn't fully removed"
    )


@pytest.mark.asyncio
async def test_valid_jwt_accepted_and_claims_stashed() -> None:
    mw = _middleware()
    token = _make_jwt(claims={"organization_id": "org-abc"})

    ctx = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )

    assert ctx is not None
    assert ctx.is_authenticated is True
    assert ctx.user_id == USER_ID
    assert ctx.auth_type == "token"
    assert ctx.email == "user@example.com"
    claims = ctx.metadata.get("jwt_claims")
    assert isinstance(claims, dict)
    assert claims.get("organization_id") == "org-abc"
    # The resolver strips signature/exp metadata from the snapshot so
    # downstream code can't accidentally rely on them.
    assert "exp" not in claims
    assert "iat" not in claims


@pytest.mark.asyncio
async def test_jwt_with_bad_signature_rejected_loudly(
    caplog: pytest.LogCaptureFixture,
) -> None:
    mw = _middleware()
    token = _make_jwt(secret=WRONG_JWT_SECRET)

    with caplog.at_level(logging.ERROR, logger="matrx_connect.middleware.auth"):
        ctx = await mw._validate_token(
            f"Bearer {token}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )

    assert ctx is None
    # Real JWT-shaped tokens that fail signature/audience MUST log
    # — those are genuinely broken JWTs and silencing them would hide
    # legitimate auth-system regressions. vcprint at ERROR goes through
    # the caller's logger only (no stdout duplicate).
    assert any("JWT validation FAILED" in r.message for r in caplog.records), (
        f"expected loud JWT failure log, got: {[r.message for r in caplog.records]}"
    )


@pytest.mark.asyncio
async def test_expired_jwt_is_rejected_without_integrity_alarm(
    caplog: pytest.LogCaptureFixture,
) -> None:
    mw = _middleware()
    token = _make_jwt(claims={"exp": int(time.time()) - 1})

    with caplog.at_level(logging.ERROR, logger="matrx_connect.middleware.auth"):
        ctx = await mw._validate_token(
            f"Bearer {token}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )

    assert ctx is None
    assert not any("JWT validation FAILED" in record.message for record in caplog.records)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "non_jwt_token",
    [
        # Sandbox-bridge service-token shape: single opaque blob, no dots.
        "6774d33dc8aa1b2c3d4e5f6071829304a1b2c3d4e5f607182930415927",
        # Single-segment hex.
        "deadbeef",
        # Two-segment "almost a JWT" — still not a valid JWT structure.
        "header.payload",
        # Four segments — not a JWT either.
        "a.b.c.d",
        # Empty bearer value (whitespace-stripped to nothing). The split
        # in `_validate_token` requires at least one whitespace, so we
        # use a placeholder that survives the split.
        "x",
    ],
)
async def test_non_jwt_bearer_rejected_silently(
    capsys: pytest.CaptureFixture[str],
    non_jwt_token: str,
) -> None:
    """Regression guard for the sandbox-bridge class of bearer schemes.

    The middleware MUST NOT print ``JWT validation FAILED: Not enough
    segments`` when the bearer token clearly isn't a JWT. The token's
    own auth check (e.g. the cloud-files-bridge router's
    ``_verify_service_token`` dependency) handles validation downstream;
    polluting stderr with one ERROR per request makes real auth
    failures invisible.
    """
    mw = _middleware()

    ctx = await mw._validate_token(
        f"Bearer {non_jwt_token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )

    assert ctx is None
    captured = capsys.readouterr()
    assert captured.err == "", (
        f"Non-JWT bearer token leaked to stderr: {captured.err!r}. "
        "This is the exact class of noise the dot-count guard is meant to prevent."
    )
    assert captured.out == "", f"Non-JWT bearer token leaked to stdout: {captured.out!r}."


@pytest.mark.asyncio
async def test_non_bearer_scheme_rejected() -> None:
    mw = _middleware()
    ctx = await mw._validate_token(
        "Basic dXNlcjpwYXNz",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None


@pytest.mark.asyncio
async def test_malformed_authorization_header_rejected() -> None:
    mw = _middleware()
    # No whitespace at all — split fails.
    ctx = await mw._validate_token(
        "Bearer",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None


@pytest.mark.asyncio
async def test_concurrent_token_misses_share_one_admin_lookup() -> None:
    calls = 0
    started = asyncio.Event()
    release = asyncio.Event()

    async def resolve_admin(_user_id: str) -> str | None:
        nonlocal calls
        calls += 1
        started.set()
        await release.wait()
        return "super_admin"

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        admin_level_resolver=resolve_admin,
    )
    token = _make_jwt()
    waiters = [asyncio.create_task(mw.verify_token_raw(token)) for _ in range(20)]
    await started.wait()
    assert calls == 1

    release.set()
    results = await asyncio.gather(*waiters)
    assert all(result is not None and result.is_admin for result in results)
    assert calls == 1


@pytest.mark.asyncio
async def test_cancelled_token_waiter_does_not_cancel_shared_validation() -> None:
    started = asyncio.Event()
    release = asyncio.Event()
    calls = 0

    async def resolve_admin(_user_id: str) -> str | None:
        nonlocal calls
        calls += 1
        started.set()
        await release.wait()
        return None

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        admin_level_resolver=resolve_admin,
    )
    token = _make_jwt()
    first = asyncio.create_task(mw.verify_token_raw(token))
    await started.wait()
    second = asyncio.create_task(mw.verify_token_raw(token))
    first.cancel()
    with pytest.raises(asyncio.CancelledError):
        await first

    release.set()
    assert await second is not None
    assert calls == 1


@pytest.mark.asyncio
async def test_shared_token_results_do_not_share_mutable_claims() -> None:
    mw = _middleware()
    token = _make_jwt(
        claims={"organization_id": "org-a", "app_metadata": {"roles": ["member"]}}
    )
    first, second = await asyncio.gather(
        mw.verify_token_raw(token),
        mw.verify_token_raw(token),
    )
    assert first is not None and second is not None
    first.claims["organization_id"] = "mutated"
    first.claims["app_metadata"]["roles"].append("super_admin")
    assert second.claims["organization_id"] == "org-a"
    assert second.claims["app_metadata"]["roles"] == ["member"]


# ---------------------------------------------------------------------------
# Phase 6 — JWKS / asymmetric token validation
# ---------------------------------------------------------------------------


def _generate_rsa_keypair() -> tuple:
    """Generate an RSA private/public key pair for RS256 tests."""
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def _make_rs256_jwt(private_key, *, claims: dict | None = None, kid: str = "test-kid") -> str:
    """Sign a JWT with an RSA private key (RS256)."""
    payload = {
        "sub": USER_ID,
        "email": "user@example.com",
        "aud": "authenticated",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    if claims:
        payload.update(claims)
    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": kid})


class _StubSigningKey:
    """Mimics jwt.PyJWK.key: just exposes ``.key`` for jwt.decode()."""

    def __init__(self, public_key, kid: str = "test-kid"):
        self.key = public_key
        self.key_id = kid


class _StubJWKClient:
    """In-memory replacement for jwt.PyJWKClient — returns a fixed public
    key for any token, lookup order doesn't matter for unit tests."""

    def __init__(self, public_key):
        self._public_key = public_key

    def get_signing_key_from_jwt(self, token: str) -> _StubSigningKey:
        return _StubSigningKey(self._public_key)

    def get_signing_keys(self, refresh: bool = False) -> list[_StubSigningKey]:
        del refresh
        return [
            _StubSigningKey(self._public_key, kid="test-kid"),
            _StubSigningKey(self._public_key, kid="es-kid"),
        ]


@pytest.mark.asyncio
async def test_random_unknown_kids_cannot_force_repeated_jwks_fetches() -> None:
    class CountingClient:
        calls = 0

        def get_signing_keys(self, refresh: bool = False) -> list[_StubSigningKey]:
            del refresh
            self.calls += 1
            return [_StubSigningKey(object(), kid="known")]

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("RS256",),
    )
    client = CountingClient()
    mw._jwks_client = client
    results = await asyncio.gather(
        *(mw._get_signing_key(f"random-{index}") for index in range(20)),
        return_exceptions=True,
    )
    assert all(isinstance(result, jwt.PyJWKClientError) for result in results)
    assert client.calls == 1


@pytest.mark.asyncio
async def test_failed_forced_jwks_refresh_starts_cooldown() -> None:
    class FailingRefreshClient:
        calls = 0

        def get_signing_keys(self, refresh: bool = False) -> list[_StubSigningKey]:
            assert refresh is True
            self.calls += 1
            raise jwt.PyJWKClientError("simulated forced refresh failure")

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("RS256",),
    )
    client = FailingRefreshClient()
    mw._jwks_client = client
    mw._jwks_keys = {"known": _StubSigningKey(object(), kid="known")}
    mw._jwks_last_refresh = 0.0

    results = await asyncio.gather(
        *(mw._get_signing_key(f"random-{index}") for index in range(20)),
        return_exceptions=True,
    )

    assert all(isinstance(result, jwt.PyJWKClientError) for result in results)
    assert client.calls == 1


@pytest.mark.asyncio
async def test_rs256_jwt_accepted_via_jwks(monkeypatch) -> None:
    """An RS256-signed Supabase token validates correctly when jwks_url is
    configured and the JWKS document yields a matching public key."""
    private_key, public_key = _generate_rsa_keypair()
    token = _make_rs256_jwt(private_key, claims={"organization_id": "org-rs"})

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        # No jwt_secret — purely asymmetric posture (matrx-local's case
        # under Supabase JWKS-only signing).
        jwt_secret="",
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("RS256",),
    )
    # Inject the stub before any token validation; PyJWKClient is
    # instantiated lazily on first asymmetric token.
    monkeypatch.setattr(jwt, "PyJWKClient", lambda url: _StubJWKClient(public_key))

    ctx = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is not None
    assert ctx.is_authenticated is True
    assert ctx.user_id == USER_ID
    assert ctx.email == "user@example.com"
    claims = ctx.metadata.get("jwt_claims") or {}
    assert claims.get("organization_id") == "org-rs"


@pytest.mark.asyncio
async def test_rs256_jwt_with_wrong_public_key_rejected(monkeypatch) -> None:
    """A token signed with one private key fails verification when the
    JWKS document returns a different public key — proves the asymmetric
    signature is actually being checked, not bypassed."""
    real_private, _ = _generate_rsa_keypair()
    _, wrong_public = _generate_rsa_keypair()  # different keypair
    token = _make_rs256_jwt(real_private)

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("RS256",),
    )
    monkeypatch.setattr(jwt, "PyJWKClient", lambda url: _StubJWKClient(wrong_public))

    ctx = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None


@pytest.mark.asyncio
async def test_rs256_token_rejected_when_jwks_url_not_configured() -> None:
    """An RS256 token without a configured jwks_url is rejected — the
    middleware never silently downgrades verification."""
    private_key, _ = _generate_rsa_keypair()
    token = _make_rs256_jwt(private_key)

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        jwks_url=None,
        # Even if RS256 is in the allow-list, missing jwks_url blocks it.
        jwt_algorithms=("HS256", "RS256"),
    )
    ctx = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None


@pytest.mark.asyncio
async def test_alg_not_in_allow_list_rejected() -> None:
    """A token signed with an alg outside the allow-list is rejected
    even if the underlying verification would succeed. Prevents alg
    confusion / downgrade attacks."""
    private_key, public_key = _generate_rsa_keypair()
    token = _make_rs256_jwt(private_key)

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        jwks_url="https://example.invalid/.well-known/jwks.json",
        # HS256-only allow-list: an RS256 token must be rejected.
        jwt_algorithms=("HS256",),
    )

    ctx = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None


@pytest.mark.asyncio
async def test_hs256_is_rejected_when_jwks_url_is_set() -> None:
    """JWKS posture ignores an injected shared secret and rejects HS256."""
    token = _make_jwt()  # HS256 with JWT_SECRET

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("HS256", "RS256"),
    )

    ctx = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None


@pytest.mark.asyncio
async def test_jwks_client_built_lazily_and_cached(monkeypatch) -> None:
    """PyJWKClient is instantiated on first asymmetric token, then reused
    for subsequent tokens — no repeated HTTP fetches per request."""
    private_key, public_key = _generate_rsa_keypair()
    token = _make_rs256_jwt(private_key)

    instantiations = []

    def fake_client(url):
        instantiations.append(url)
        return _StubJWKClient(public_key)

    monkeypatch.setattr(jwt, "PyJWKClient", fake_client)

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("RS256",),
    )
    # Not built yet — only on first token.
    assert mw._jwks_client is None

    for _ in range(3):
        ctx = await mw._validate_token(
            f"Bearer {token}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )
        assert ctx is not None and ctx.is_authenticated is True

    # PyJWKClient(url) was called exactly once across three validations.
    assert len(instantiations) == 1
    assert instantiations[0] == "https://example.invalid/.well-known/jwks.json"


@pytest.mark.asyncio
async def test_jwks_lookup_failure_is_rejected_without_application_error(
    monkeypatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A JWKS lookup failure (network error, kid not found, etc.) is
    handled gracefully — the token is rejected with a log line, the
    middleware doesn't crash."""
    private_key, _ = _generate_rsa_keypair()
    token = _make_rs256_jwt(private_key)

    class _FailingJWKClient:
        def __init__(self, url):
            pass

        def get_signing_key_from_jwt(self, token):
            raise jwt.PyJWKClientError("simulated JWKS fetch failure")

        def get_signing_keys(self, refresh: bool = False):
            del refresh
            raise jwt.PyJWKClientError("simulated JWKS fetch failure")

    monkeypatch.setattr(jwt, "PyJWKClient", _FailingJWKClient)

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("RS256",),
    )

    with caplog.at_level(logging.WARNING, logger="matrx_connect.middleware.auth"):
        ctx = await mw._validate_token(
            f"Bearer {token}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )
    assert ctx is None
    assert any("JWKS key lookup rejected token" in record.message for record in caplog.records)
    assert not any(record.levelno >= logging.ERROR for record in caplog.records)


@pytest.mark.asyncio
async def test_alg_none_attack_rejected() -> None:
    """The classic 'I'm not signed' attack: a token with ``alg=none`` and
    no signature. The default allow-list is ``("HS256",)`` and 'none' is
    never in it, so this rejects at the alg-check gate before any
    verification key resolution. Even if a host accidentally widens the
    allow-list, 'none' has to be in it explicitly — there is no path
    where it slips through silently."""
    # Manually craft an unsigned token (alg=none).
    # PyJWT refuses to encode with alg=none by default, so we forge it
    # by hand.
    import base64
    import json as _json

    def _b64(d: bytes) -> str:
        return base64.urlsafe_b64encode(d).rstrip(b"=").decode()

    header = _b64(_json.dumps({"alg": "none", "typ": "JWT"}).encode())
    payload = _b64(_json.dumps({"sub": USER_ID, "aud": "authenticated"}).encode())
    forged = f"{header}.{payload}."  # empty signature segment

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        # Default jwt_algorithms is ("HS256",) — no 'none'.
    )
    ctx = await mw._validate_token(
        f"Bearer {forged}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None, "alg=none must NEVER produce an authenticated context"


@pytest.mark.asyncio
async def test_neither_secret_nor_jwks_url_rejects_all_tokens() -> None:
    """A middleware configured with neither a secret nor a JWKS URL
    rejects every JWT — no silent fallthrough to anonymous."""
    token = _make_jwt()
    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret="",
        jwks_url=None,
    )
    ctx = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None


@pytest.mark.asyncio
async def test_hs256_token_rejected_without_secret_is_warning(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A symmetric token at an asymmetric-only verifier is a denied
    credential, not an application failure for the repair queue."""
    token = _make_jwt()
    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret="",
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("HS256", "ES256"),
    )

    with caplog.at_level(logging.WARNING, logger="matrx_connect.middleware.auth"):
        ctx = await mw._validate_token(
            f"Bearer {token}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )

    assert ctx is None
    assert any("HS256 token rejected" in record.message for record in caplog.records)
    assert not any(record.levelno >= logging.ERROR for record in caplog.records)


# ---------------------------------------------------------------------------
# Token validation cache — the burst-of-Range-requests collapse
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_token_cache_collapses_repeat_validations() -> None:
    """Two validations with the same Bearer token inside the TTL hit the
    admin resolver exactly once. This is the pdf.js Range-request fix:
    one PDF open ⇒ 5–6 HTTP Range requests ⇒ ONE admin DB lookup, not 5–6.
    """
    admin_calls: list[str] = []

    async def _is_admin(user_id: str) -> bool:
        admin_calls.append(user_id)
        return True

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
        token_cache_ttl_seconds=5.0,
    )
    token = _make_jwt()

    for _ in range(6):
        ctx = await mw._validate_token(
            f"Bearer {token}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )
        assert ctx is not None
        assert ctx.is_authenticated is True
        assert ctx.user_id == USER_ID
        assert ctx.is_admin is True

    assert admin_calls == [USER_ID], (
        f"admin resolver hit {len(admin_calls)}x instead of once — "
        "the per-token cache is not collapsing repeat validations"
    )


@pytest.mark.asyncio
async def test_token_cache_disabled_with_zero_ttl() -> None:
    """``token_cache_ttl_seconds=0`` disables the cache entirely — every
    call goes through the full decode + admin lookup."""
    admin_calls: list[str] = []

    async def _is_admin(user_id: str) -> bool:
        admin_calls.append(user_id)
        return False

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
        token_cache_ttl_seconds=0.0,
    )
    token = _make_jwt()

    for _ in range(3):
        ctx = await mw._validate_token(
            f"Bearer {token}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )
        assert ctx is not None

    assert len(admin_calls) == 3, (
        "cache should be disabled when ttl=0; admin resolver should run for every call"
    )


@pytest.mark.asyncio
async def test_token_cache_expires_after_ttl() -> None:
    """After the TTL window passes, the next request re-validates from
    scratch — bounded staleness is the contract."""
    admin_calls: list[str] = []

    async def _is_admin(user_id: str) -> bool:
        admin_calls.append(user_id)
        return False

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
        token_cache_ttl_seconds=0.05,  # 50ms — short enough for a real test
    )
    token = _make_jwt()

    await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    # Within window — cached.
    await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert len(admin_calls) == 1

    # Sleep past the TTL — next call re-validates.
    import asyncio as _asyncio

    await _asyncio.sleep(0.08)
    await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert len(admin_calls) == 2


@pytest.mark.asyncio
async def test_token_cache_keys_by_token_not_user() -> None:
    """Distinct tokens for the same user are cached separately — the cache
    key is SHA256(token), not user_id. A new token from a fresh login does
    NOT serve a stale admin result from a prior session."""
    admin_calls: list[str] = []

    async def _is_admin(user_id: str) -> bool:
        admin_calls.append(user_id)
        return False

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
        token_cache_ttl_seconds=5.0,
    )
    # Two distinct tokens (different iat → different signature) for the
    # same sub.
    token_a = _make_jwt(claims={"jti": "session-A"})
    token_b = _make_jwt(claims={"jti": "session-B"})
    assert token_a != token_b

    await mw._validate_token(
        f"Bearer {token_a}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    await mw._validate_token(
        f"Bearer {token_b}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )

    assert len(admin_calls) == 2, (
        "distinct tokens must each hit the admin resolver — cache keys "
        "must be per-token, not per-user"
    )


@pytest.mark.asyncio
async def test_token_cache_capped_by_jwt_exp() -> None:
    """If the JWT's own ``exp`` expires sooner than the cache TTL, the
    cache entry uses the shorter window so we never serve an expired
    token from cache."""
    admin_calls: list[str] = []

    async def _is_admin(user_id: str) -> bool:
        admin_calls.append(user_id)
        return False

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
        token_cache_ttl_seconds=60.0,  # generous TTL
    )
    # JWT that expires almost immediately (the cache cap, not the TTL,
    # is what we're testing).
    short_lived = jwt.encode(
        {
            "sub": USER_ID,
            "email": "user@example.com",
            "aud": "authenticated",
            "iat": int(time.time()),
            "exp": int(time.time()) + 1,  # 1s
        },
        JWT_SECRET,
        algorithm="HS256",
    )

    await mw._validate_token(
        f"Bearer {short_lived}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert len(admin_calls) == 1

    # Sleep past the JWT's own exp — even though the cache TTL is 60s,
    # the entry must be gone.
    import asyncio as _asyncio

    await _asyncio.sleep(1.2)

    # The JWT itself is now expired, so revalidation will fail (returning
    # None) — but importantly, the cache MUST NOT have short-circuited it.
    ctx = await mw._validate_token(
        f"Bearer {short_lived}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx is None, "expired JWT must NOT be served from cache"


@pytest.mark.asyncio
async def test_token_cache_does_not_cache_failed_validations() -> None:
    """A failed JWT validation (bad signature) is not cached — the next
    request runs the full decode again (and fails again loudly)."""
    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        token_cache_ttl_seconds=5.0,
    )
    bad_token = _make_jwt(secret=WRONG_JWT_SECRET)

    ctx1 = await mw._validate_token(
        f"Bearer {bad_token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    ctx2 = await mw._validate_token(
        f"Bearer {bad_token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    assert ctx1 is None
    assert ctx2 is None
    # Cache should be empty — failed validations never populate it.
    assert mw._token_cache == {}


@pytest.mark.asyncio
async def test_token_cache_eviction_when_full() -> None:
    """When the cache reaches its max size, inserts evict older entries.
    Bounds memory under a burst of distinct tokens."""
    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        token_cache_ttl_seconds=60.0,
        token_cache_max_size=3,
    )

    tokens = [_make_jwt(claims={"jti": f"sess-{i}"}) for i in range(5)]
    for tok in tokens:
        ctx = await mw._validate_token(
            f"Bearer {tok}",
            fingerprint_id=None,
            ctx=_empty_ctx(),
        )
        assert ctx is not None

    # Cache must never exceed the cap.
    assert len(mw._token_cache) <= 3, (
        f"cache exceeded max_size=3, holds {len(mw._token_cache)} entries"
    )


@pytest.mark.asyncio
async def test_token_cache_hit_returns_same_claims_as_miss() -> None:
    """Cache-hit responses are functionally identical to cache-miss
    responses — claims, email, is_admin, user_id all match."""

    async def _is_admin(user_id: str) -> bool:
        return True

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
        token_cache_ttl_seconds=5.0,
    )
    token = _make_jwt(claims={"organization_id": "org-xyz"})

    fresh = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )
    cached = await mw._validate_token(
        f"Bearer {token}",
        fingerprint_id=None,
        ctx=_empty_ctx(),
    )

    assert fresh is not None and cached is not None
    assert fresh.user_id == cached.user_id
    assert fresh.email == cached.email
    assert fresh.is_admin == cached.is_admin
    assert fresh.is_authenticated == cached.is_authenticated
    assert fresh.auth_type == cached.auth_type
    assert fresh.metadata.get("jwt_claims") == cached.metadata.get("jwt_claims")
    assert fresh.metadata["jwt_claims"]["organization_id"] == "org-xyz"
    assert cached.metadata["jwt_claims"]["organization_id"] == "org-xyz"


# ---------------------------------------------------------------------------
# ES256 — the algorithm Matrx Main actually signs with — and verify_token_raw,
# the shared primitive consumed by the MCP OAuth TokenVerifier.
# ---------------------------------------------------------------------------


def _generate_ec_keypair() -> tuple:
    """Generate an EC P-256 private/public key pair for ES256 tests."""
    from cryptography.hazmat.primitives.asymmetric import ec

    private_key = ec.generate_private_key(ec.SECP256R1())
    return private_key, private_key.public_key()


def _make_es256_jwt(private_key, *, claims: dict | None = None, kid: str = "es-kid") -> str:
    payload = {
        "sub": USER_ID,
        "email": "user@example.com",
        "aud": "authenticated",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    if claims:
        payload.update(claims)
    return jwt.encode(payload, private_key, algorithm="ES256", headers={"kid": kid})


@pytest.mark.asyncio
async def test_es256_jwt_accepted_via_jwks(monkeypatch) -> None:
    """Matrx Main signs Supabase JWTs with ES256. With jwks_url wired + ES256
    in the allow-list (aidream's production posture after Phase 0), an ES256
    token validates. This is the exact regression guard for the latent
    full-auth outage that motivated wiring jwks_url — the day Supabase
    promotes ES256 to the current signing key, this path MUST hold."""
    private_key, public_key = _generate_ec_keypair()
    token = _make_es256_jwt(private_key, claims={"organization_id": "org-es"})

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,  # HS256 still configured (rotation window)
        jwks_url="https://example.invalid/.well-known/jwks.json",
        jwt_algorithms=("HS256", "ES256"),
    )
    monkeypatch.setattr(jwt, "PyJWKClient", lambda url: _StubJWKClient(public_key))

    ctx = await mw._validate_token(f"Bearer {token}", fingerprint_id=None, ctx=_empty_ctx())
    assert ctx is not None
    assert ctx.is_authenticated is True
    assert ctx.user_id == USER_ID
    assert (ctx.metadata.get("jwt_claims") or {}).get("organization_id") == "org-es"


@pytest.mark.asyncio
async def test_verify_token_raw_returns_verified_token() -> None:
    """The shared primitive the MCP OAuth TokenVerifier consumes: given a raw
    token (no ``Bearer`` prefix) it returns a ``VerifiedToken`` with identity +
    admin, reusing the same crypto/cache/admin path as the HTTP middleware."""
    from matrx_connect.middleware.auth import VerifiedToken

    async def _is_admin(user_id: str) -> bool:
        return True

    mw = AuthMiddleware(
        app=lambda *a, **kw: None,
        jwt_secret=JWT_SECRET,
        is_admin_resolver=_is_admin,
    )
    token = _make_jwt(claims={"organization_id": "org-raw"})

    result = await mw.verify_token_raw(token)
    assert isinstance(result, VerifiedToken)
    assert result.user_id == USER_ID
    assert result.is_admin is True
    assert result.email == "user@example.com"
    assert result.claims.get("organization_id") == "org-raw"
    assert result.token == token
    assert result.expires_at is not None
    assert result.expires_at > int(time.time())


@pytest.mark.asyncio
async def test_verify_token_raw_preserves_lifecycle_metadata_on_cache_hit() -> None:
    """MCP resource-server adapters receive verified expiry/issuer metadata
    on both the crypto path and the short-lived token-cache path."""
    mw = AuthMiddleware(app=lambda *a, **kw: None, jwt_secret=JWT_SECRET)
    expires_at = int(time.time()) + 3600
    issuer = "https://project-ref.supabase.co/auth/v1"
    token = _make_jwt(claims={"exp": expires_at, "iss": issuer})

    fresh = await mw.verify_token_raw(token)
    cached = await mw.verify_token_raw(token)

    assert fresh is not None and cached is not None
    assert fresh.expires_at == cached.expires_at == expires_at
    assert fresh.issuer == cached.issuer == issuer


@pytest.mark.asyncio
async def test_verify_token_raw_rejects_bad_signature() -> None:
    """``verify_token_raw`` returns None for an invalid token — the MCP
    TokenVerifier maps that to a 401 challenge, never an authenticated call."""
    mw = AuthMiddleware(app=lambda *a, **kw: None, jwt_secret=JWT_SECRET)
    bad = _make_jwt(secret=WRONG_JWT_SECRET)
    assert await mw.verify_token_raw(bad) is None
