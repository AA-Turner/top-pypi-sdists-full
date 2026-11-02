"""The in-package guarantee against the 2026-08-30 private-file outage class.

The outage: mx_files_session cookies are HMAC-signed with the middleware's
guest_fingerprint_secret; with per-process random fallback secrets across
containers, a cookie minted on one container fails verification on every
other — every private <img> 401s and NOTHING reached error telemetry.

These tests pin the two in-package guarantees:

1. **Drift detector** — a cookie that is PRESENT, structurally valid
   (v1 + 4 parts + integer exp), UNEXPIRED, but fails HMAC is exactly
   secret drift (or tampering), never a normal anonymous request. The
   middleware logs CRITICAL with the machine-greppable token
   ``MX_COOKIE_SIGNATURE_MISMATCH``, rate-limited per (process, reason)
   burst-window. Expired / malformed / absent stay silent-anonymous.
2. **Ephemeral-secret honesty** — ``AuthMiddleware.secret_is_ephemeral``
   and ``get_session_cookie_secret_source()`` expose whether the process
   fell back to a per-process random secret, so the /files/session mint
   response can carry ``secret_source`` and a client can scream.
"""

from __future__ import annotations

import asyncio
import logging

import pytest
from starlette.requests import Request

from matrx_connect.middleware import session_cookie as sc
from matrx_connect.middleware.auth import COOKIE_DRIFT_LOG_WINDOW_SECONDS, AuthMiddleware
from matrx_connect.middleware.session_cookie import (
    classify_session_cookie_value,
    get_session_cookie_secret_source,
    mint_session_cookie_value,
    register_session_cookie_secret,
)

USER_ID = "87a6e699-3622-4869-8843-d0867456c0dd"
SECRET_A = b"container-a-stable-secret"
SECRET_B = b"container-b-different-secret"
DRIFT_TOKEN = "MX_COOKIE_SIGNATURE_MISMATCH"


@pytest.fixture(autouse=True)
def _isolate_registered_secret():
    """AuthMiddleware construction mutates the module-global registration."""
    saved = (sc._registered_secret, sc._registered_secret_is_ephemeral)
    sc._registered_secret = None
    sc._registered_secret_is_ephemeral = False
    yield
    sc._registered_secret, sc._registered_secret_is_ephemeral = saved


def _middleware(secret: str = "stable-secret-on-every-container") -> AuthMiddleware:
    return AuthMiddleware(app=lambda *a, **kw: None, guest_fingerprint_secret=secret)


def _get_request(path: str, cookie_value: str | None) -> Request:
    headers = []
    if cookie_value is not None:
        headers.append((b"cookie", f"{sc.SESSION_COOKIE_NAME}={cookie_value}".encode()))
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "scheme": "https",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": headers,
        "client": ("127.0.0.1", 4242),
        "server": ("testserver", 443),
    }
    return Request(scope)


def _build(mw: AuthMiddleware, request: Request):
    return asyncio.run(mw._build_context(request))


# ---------------------------------------------------------------------------
# classify_session_cookie_value — the reason taxonomy
# ---------------------------------------------------------------------------


def test_classify_ok() -> None:
    value = mint_session_cookie_value(USER_ID, SECRET_A, now=1_000_000.0)
    assert classify_session_cookie_value(value, SECRET_A, now=1_000_001.0) == (USER_ID, "ok")


def test_classify_signature_mismatch_is_distinct() -> None:
    """Wrong-secret valid cookie == the outage. Never 'malformed'."""
    value = mint_session_cookie_value(USER_ID, SECRET_A, now=1_000_000.0)
    user, reason = classify_session_cookie_value(value, SECRET_B, now=1_000_001.0)
    assert user is None
    assert reason == "signature_mismatch"


def test_classify_expired_and_malformed_and_absent() -> None:
    expired = mint_session_cookie_value(USER_ID, SECRET_A, ttl_seconds=60, now=1_000_000.0)
    assert classify_session_cookie_value(expired, SECRET_A, now=1_000_061.0) == (None, "expired")
    assert classify_session_cookie_value("garbage", SECRET_A) == (None, "malformed")
    assert classify_session_cookie_value("v1.u.not-int.deadbeef", SECRET_A) == (None, "malformed")
    assert classify_session_cookie_value(None, SECRET_A) == (None, "absent")
    assert classify_session_cookie_value("", SECRET_A) == (None, "absent")


def test_classify_expired_wrong_secret_reports_expired_not_drift() -> None:
    """An expired foreign cookie is routine churn, not a drift alarm."""
    expired = mint_session_cookie_value(USER_ID, SECRET_B, ttl_seconds=60, now=1_000_000.0)
    assert classify_session_cookie_value(expired, SECRET_A, now=1_000_061.0) == (None, "expired")


# ---------------------------------------------------------------------------
# The drift detector in the middleware cookie lane
# ---------------------------------------------------------------------------


def test_drift_detector_fires_critical_on_wrong_secret_cookie(caplog) -> None:
    mw = _middleware()
    foreign = mint_session_cookie_value(USER_ID, SECRET_B)
    with caplog.at_level(logging.CRITICAL, logger="matrx_connect.auth"):
        ctx = _build(mw, _get_request("/files/abc/download", foreign))
    assert ctx.user_id in (None, "")  # stays anonymous
    records = [r for r in caplog.records if DRIFT_TOKEN in r.getMessage()]
    assert len(records) == 1
    assert records[0].levelno == logging.CRITICAL
    # Remedy text names the stable-secret requirement.
    assert "stable" in records[0].getMessage()
    assert "guest_fingerprint_secret" in records[0].getMessage()


def test_drift_detector_silent_on_expired_cookie(caplog) -> None:
    mw = _middleware()
    expired = mint_session_cookie_value(USER_ID, mw._guest_fp_secret, ttl_seconds=-60)
    with caplog.at_level(logging.WARNING, logger="matrx_connect.auth"):
        ctx = _build(mw, _get_request("/files/abc/download", expired))
    assert ctx.user_id in (None, "")
    assert not [r for r in caplog.records if DRIFT_TOKEN in r.getMessage()]


def test_drift_detector_silent_on_malformed_and_absent_cookie(caplog) -> None:
    mw = _middleware()
    with caplog.at_level(logging.WARNING, logger="matrx_connect.auth"):
        _build(mw, _get_request("/files/abc/download", "total-garbage"))
        _build(mw, _get_request("/files/abc/download", None))
    assert not [r for r in caplog.records if DRIFT_TOKEN in r.getMessage()]


def test_drift_detector_silent_off_the_cookie_lane(caplog) -> None:
    """A wrong-secret cookie on a non-byte-serving path never consults the
    cookie lane at all — no alarm."""
    mw = _middleware()
    foreign = mint_session_cookie_value(USER_ID, SECRET_B)
    with caplog.at_level(logging.CRITICAL, logger="matrx_connect.auth"):
        _build(mw, _get_request("/files/abc", foreign))
    assert not [r for r in caplog.records if DRIFT_TOKEN in r.getMessage()]


def test_drift_detector_rate_limits_within_window(caplog) -> None:
    """A broken fleet must not flood: first occurrence logs, repeats within
    the burst window are counted silently, and after the window the next
    occurrence logs again WITH the suppressed count."""
    mw = _middleware()
    foreign = mint_session_cookie_value(USER_ID, SECRET_B)
    with caplog.at_level(logging.CRITICAL, logger="matrx_connect.auth"):
        for _ in range(5):
            _build(mw, _get_request("/files/abc/download", foreign))
    records = [r for r in caplog.records if DRIFT_TOKEN in r.getMessage()]
    assert len(records) == 1

    # Age the window out, then one more mismatch → exactly one new record
    # carrying the 4 suppressed occurrences.
    last, suppressed = mw._drift_log_state["signature_mismatch"]
    assert suppressed == 4
    mw._drift_log_state["signature_mismatch"] = (
        last - COOKIE_DRIFT_LOG_WINDOW_SECONDS - 1.0,
        suppressed,
    )
    caplog.clear()
    with caplog.at_level(logging.CRITICAL, logger="matrx_connect.auth"):
        _build(mw, _get_request("/files/abc/download", foreign))
    records = [r for r in caplog.records if DRIFT_TOKEN in r.getMessage()]
    assert len(records) == 1
    assert "4" in records[0].getMessage()


def test_valid_cookie_still_authenticates_and_never_alarms(caplog) -> None:
    mw = _middleware()
    good = mint_session_cookie_value(USER_ID, mw._guest_fp_secret)
    with caplog.at_level(logging.CRITICAL, logger="matrx_connect.auth"):
        ctx = _build(mw, _get_request("/files/abc/download", good))
    assert ctx.user_id == USER_ID
    assert ctx.auth_type == "cookie"
    assert not [r for r in caplog.records if DRIFT_TOKEN in r.getMessage()]


# ---------------------------------------------------------------------------
# Ephemeral-secret honesty — secret_is_ephemeral + secret_source threading
# ---------------------------------------------------------------------------


def test_injected_secret_reports_stable() -> None:
    mw = _middleware("a-real-injected-secret")
    assert mw.secret_is_ephemeral is False
    assert get_session_cookie_secret_source() == "stable"


def test_fallback_secret_reports_ephemeral() -> None:
    mw = _middleware("")
    assert mw.secret_is_ephemeral is True
    assert get_session_cookie_secret_source() == "ephemeral"


def test_explicit_registration_defaults_to_stable() -> None:
    register_session_cookie_secret(b"explicitly-registered")
    assert get_session_cookie_secret_source() == "stable"
    # STABLE WINS (the 2026-08-30 clobber fix): an ephemeral re-registration
    # is refused once a stable secret is registered — see
    # test_session_cookie_stable_wins.py for the full class pin.
    register_session_cookie_secret(b"some-random", ephemeral=True)
    assert get_session_cookie_secret_source() == "stable"


def test_secret_source_requires_registration() -> None:
    sc._registered_secret = None
    sc._registered_secret_is_ephemeral = False
    with pytest.raises(RuntimeError, match="not registered"):
        get_session_cookie_secret_source()
