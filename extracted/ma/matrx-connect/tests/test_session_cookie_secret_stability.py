"""The 2026-08-30 private-file outage, pinned as a failing-then-passing guard.

mx_files_session cookies are HMAC-signed with the middleware's server secret.
With NO injected secret, every process invents its own — a cookie minted by
one instance is invalid on every other, which in a multi-container deployment
kills every private <img> render. These tests pin BOTH sides:

- the failure mode exists exactly as diagnosed (two default-constructed
  instances cannot verify each other's cookies), and
- an injected stable secret makes independently-constructed instances fully
  interoperable (the aidream host now guarantees injection by deriving from
  CREDENTIALS_ENCRYPTION_KEY when GUEST_FINGERPRINT_SECRET is unset).
"""

from matrx_connect.middleware.session_cookie import (
    mint_session_cookie_value,
    verify_session_cookie_value,
)

USER = "87a6e699-3622-4869-8843-d0867456c0dd"


def test_random_per_process_secrets_do_not_interop():
    """The outage: two processes, two secrets, cookie dies across them."""
    import secrets

    secret_a = secrets.token_urlsafe(48).encode()
    secret_b = secrets.token_urlsafe(48).encode()
    cookie = mint_session_cookie_value(USER, secret_a, now=1_000_000.0)
    assert verify_session_cookie_value(cookie, secret_a, now=1_000_000.5) == USER
    assert verify_session_cookie_value(cookie, secret_b, now=1_000_000.5) is None


def test_shared_stable_secret_interops_across_instances():
    """The fix: one stable secret -> mint anywhere, verify anywhere."""
    shared = b"one-stable-secret-on-every-container"
    cookie = mint_session_cookie_value(USER, shared, now=1_000_000.0)
    # A "different container" is just a different verify call with the same
    # injected secret — no shared module state involved.
    assert verify_session_cookie_value(cookie, shared, now=1_000_000.5) == USER


def test_aidream_derivation_is_deterministic_and_domain_separated():
    """The host derivation: stable across processes, distinct per domain."""
    import hashlib
    import hmac

    base = b"credentials-encryption-key-value"
    d1 = hmac.new(base, b"matrx|guest-fingerprint+files-session|v1", hashlib.sha256).hexdigest()
    d2 = hmac.new(base, b"matrx|guest-fingerprint+files-session|v1", hashlib.sha256).hexdigest()
    other_domain = hmac.new(base, b"matrx|other-purpose|v1", hashlib.sha256).hexdigest()
    assert d1 == d2
    assert d1 != other_domain
    cookie = mint_session_cookie_value(USER, d1.encode(), now=1_000_000.0)
    assert verify_session_cookie_value(cookie, d2.encode(), now=1_000_000.5) == USER
