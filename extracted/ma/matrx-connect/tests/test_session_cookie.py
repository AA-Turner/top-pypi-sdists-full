"""The browser file-session cookie — mint/verify HMAC roundtrip + path gate.

The cookie replaced signed URLs as the browser's credential for durable
byte-serving routes (``/files/{id}/download``, ``/media/{id}/v/{class}``).
Verification is a pure HMAC check: malformed, tampered, or expired values
resolve to ``None`` (anonymous), never an exception. The path regex is
path-only — HTTP-method gating (GET only) lives in AuthMiddleware.
"""

from __future__ import annotations

import pytest

from matrx_connect.middleware.session_cookie import (
    COOKIE_AUTH_PATH_RE,
    SESSION_COOKIE_NAME,
    mint_session_cookie_value,
    session_cookie_header,
    verify_session_cookie_value,
)

SECRET = b"test-secret-0123456789"
USER_ID = "44444444-4444-4444-4444-444444444444"


def test_mint_verify_roundtrip() -> None:
    value = mint_session_cookie_value(USER_ID, SECRET)
    assert verify_session_cookie_value(value, SECRET) == USER_ID


def test_expired_cookie_is_anonymous() -> None:
    value = mint_session_cookie_value(USER_ID, SECRET, ttl_seconds=60, now=1_000_000.0)
    # Valid just before expiry, None just after.
    assert verify_session_cookie_value(value, SECRET, now=1_000_059.0) == USER_ID
    assert verify_session_cookie_value(value, SECRET, now=1_000_061.0) is None


def test_tampered_signature_is_anonymous() -> None:
    value = mint_session_cookie_value(USER_ID, SECRET)
    prefix, sig = value.rsplit(".", 1)
    flipped = ("0" if sig[0] != "0" else "1") + sig[1:]
    assert verify_session_cookie_value(f"{prefix}.{flipped}", SECRET) is None


def test_tampered_user_id_is_anonymous() -> None:
    value = mint_session_cookie_value(USER_ID, SECRET)
    _, _, exp, sig = value.split(".")
    assert verify_session_cookie_value(f"v1.someone-else.{exp}.{sig}", SECRET) is None


def test_wrong_secret_is_anonymous() -> None:
    value = mint_session_cookie_value(USER_ID, SECRET)
    assert verify_session_cookie_value(value, b"other-secret") is None


@pytest.mark.parametrize(
    "malformed",
    [
        None,
        "",
        "garbage",
        "v1.only.three",
        "v2.user.123.deadbeef",  # unknown version
        "v1.user.not-a-number.deadbeef",  # non-integer expiry
        "v1.user.123.deadbeef.extra",  # too many parts
    ],
)
def test_malformed_cookie_is_anonymous(malformed: str | None) -> None:
    assert verify_session_cookie_value(malformed, SECRET) is None


def test_mint_requires_user_id() -> None:
    with pytest.raises(ValueError, match="user_id is required"):
        mint_session_cookie_value("", SECRET)


def test_set_cookie_header_shape() -> None:
    header = session_cookie_header("v1.u.1.abc", ttl_seconds=60)
    assert header.startswith(f"{SESSION_COOKIE_NAME}=v1.u.1.abc; Max-Age=60; Path=/;")
    assert "HttpOnly" in header
    assert "Secure" in header
    assert "SameSite=None" in header


# ---------------------------------------------------------------------------
# COOKIE_AUTH_PATH_RE — the ONLY paths cookie auth may satisfy. The regex is
# path-only; the GET-only rule is enforced by AuthMiddleware, not here.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    [
        "/files/abc/download",
        "/files/abc/download/",
        "/files/11111111-1111-1111-1111-111111111111/download",
        "/media/abc/v/thumb",
        "/media/abc/v/anthropic_opus_hires",
    ],
)
def test_cookie_auth_paths_allowed(path: str) -> None:
    assert COOKIE_AUTH_PATH_RE.match(path)


@pytest.mark.parametrize(
    "path",
    [
        "/files/abc",  # metadata read — Bearer only
        "/files/abc/download/extra",  # deeper than the byte route
        "/files/abc/url",  # the deleted signed-URL route
        "/files",  # listing
        "/files/session",  # the mint route itself (POST, Bearer only)
        "/media/abc",  # media root
        "/media/abc/v",  # missing vision class
        "/media/abc/v/thumb/extra",
        "/admin/files/abc/download",  # never a non-root prefix
        "files/abc/download",  # must be anchored at /
    ],
)
def test_cookie_auth_paths_denied(path: str) -> None:
    assert COOKIE_AUTH_PATH_RE.match(path) is None
