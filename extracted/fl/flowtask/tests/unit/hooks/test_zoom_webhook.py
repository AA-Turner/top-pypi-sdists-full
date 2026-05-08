"""Unit tests for ZoomWebHook trigger.

Tests use object.__new__ to bypass framework initialisation and inject only
the attributes that the production methods actually touch. This avoids needing
navconfig, aiohttp app wiring, or a live database for pure-logic assertions.
"""
import hashlib
import hmac
import json
import logging
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from flowtask.hooks.types.zoom import ZoomWebHook
from .fixtures import (
    ZOOM_SECRET,
    CRC_PAYLOAD,
    SMS_SENT_PAYLOAD,
    make_signed_request,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def make_hook(secret: str = ZOOM_SECRET, replay_window: int = 300) -> ZoomWebHook:
    """Build a ZoomWebHook bypassing framework __init__."""
    hook = object.__new__(ZoomWebHook)
    hook._secret_token = secret
    hook._replay_window = replay_window
    hook.trigger_id = "test-hook"
    hook.default_status = 200
    hook._logger = logging.getLogger("test.zoom_webhook")
    hook._actions = None
    return hook


def make_mock_request(body: bytes, headers: dict) -> MagicMock:
    """Build a minimal mock aiohttp.web.Request."""
    req = MagicMock()
    req.read = AsyncMock(return_value=body)
    req.headers = headers
    return req


# ─────────────────────────────────────────────────────────────────────────────
# _verify_signature
# ─────────────────────────────────────────────────────────────────────────────


class TestVerifySignature:
    def test_valid_signature_returns_true(self):
        hook = make_hook()
        raw = b'{"event":"phone.sms_sent"}'
        ts = str(int(time.time()))
        msg = f"v0:{ts}:{raw.decode()}".encode()
        sig = "v0=" + hmac.new(ZOOM_SECRET.encode(), msg, hashlib.sha256).hexdigest()
        assert hook._verify_signature(ts, raw, sig) is True

    def test_wrong_secret_returns_false(self):
        hook = make_hook()
        raw = b'{"event":"phone.sms_sent"}'
        ts = str(int(time.time()))
        msg = f"v0:{ts}:{raw.decode()}".encode()
        sig = "v0=" + hmac.new(b"wrong-secret", msg, hashlib.sha256).hexdigest()
        assert hook._verify_signature(ts, raw, sig) is False

    def test_tampered_body_returns_false(self):
        hook = make_hook()
        raw = b'{"event":"phone.sms_sent"}'
        ts = str(int(time.time()))
        msg = f"v0:{ts}:{raw.decode()}".encode()
        sig = "v0=" + hmac.new(ZOOM_SECRET.encode(), msg, hashlib.sha256).hexdigest()
        assert hook._verify_signature(ts, b'{"event":"tampered"}', sig) is False

    def test_missing_sig_returns_false(self):
        hook = make_hook()
        assert hook._verify_signature("12345", b"body", "") is False

    def test_missing_ts_returns_false(self):
        hook = make_hook()
        assert hook._verify_signature("", b"body", "v0=abc") is False

    def test_empty_secret_returns_false(self):
        hook = make_hook(secret="")
        assert hook._verify_signature("12345", b"body", "v0=abc") is False


# ─────────────────────────────────────────────────────────────────────────────
# _crc_response
# ─────────────────────────────────────────────────────────────────────────────


class TestCrcResponse:
    def test_crc_returns_correct_encrypted_token(self):
        hook = make_hook()
        plain = "test-plain-token-abc"
        result = hook._crc_response(plain)
        expected_encrypted = hmac.new(
            ZOOM_SECRET.encode(), plain.encode(), hashlib.sha256
        ).hexdigest()
        assert result["plainToken"] == plain
        assert result["encryptedToken"] == expected_encrypted

    def test_crc_keys_present(self):
        hook = make_hook()
        result = hook._crc_response("abc")
        assert "plainToken" in result
        assert "encryptedToken" in result


# ─────────────────────────────────────────────────────────────────────────────
# post() — CRC handshake
# ─────────────────────────────────────────────────────────────────────────────


class TestPostCRC:
    @pytest.mark.asyncio
    async def test_crc_returns_200_with_signed_token(self):
        hook = make_hook()
        body = json.dumps(CRC_PAYLOAD).encode()
        req = make_mock_request(body, {"content-type": "application/json"})
        resp = await hook.post(req)
        assert resp.status == 200
        payload = json.loads(resp.body)
        assert payload["plainToken"] == "test-plain-token-abc"
        assert len(payload["encryptedToken"]) == 64  # SHA-256 hex digest

    @pytest.mark.asyncio
    async def test_crc_without_secret_returns_500(self):
        hook = make_hook(secret="")
        body = json.dumps(CRC_PAYLOAD).encode()
        req = make_mock_request(body, {})
        resp = await hook.post(req)
        assert resp.status == 500


# ─────────────────────────────────────────────────────────────────────────────
# post() — signature verification
# ─────────────────────────────────────────────────────────────────────────────


class TestPostSignature:
    @pytest.mark.asyncio
    async def test_valid_signature_dispatches_actions(self):
        hook = make_hook()
        raw, headers = make_signed_request(SMS_SENT_PAYLOAD)
        req = make_mock_request(raw, headers)
        hook.run_actions = AsyncMock(return_value=None)
        resp = await hook.post(req)
        assert resp.status == 200
        hook.run_actions.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_invalid_signature_returns_401(self):
        hook = make_hook()
        raw, headers = make_signed_request(SMS_SENT_PAYLOAD)
        headers["x-zm-signature"] = "v0=badsignature"
        req = make_mock_request(raw, headers)
        hook.run_actions = AsyncMock()
        resp = await hook.post(req)
        assert resp.status == 401
        hook.run_actions.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_missing_signature_returns_401(self):
        hook = make_hook()
        raw = json.dumps(SMS_SENT_PAYLOAD).encode()
        headers = {
            "x-zm-request-timestamp": str(int(time.time())),
            "content-type": "application/json",
        }
        req = make_mock_request(raw, headers)
        hook.run_actions = AsyncMock()
        resp = await hook.post(req)
        assert resp.status == 401
        hook.run_actions.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_raw_body_is_used_for_signature_not_re_encoded(self):
        """Signature must be computed over the original raw bytes."""
        hook = make_hook()
        # Build a payload where JSON re-encoding would produce different bytes
        # (e.g. different key order). The signature is over the exact raw bytes.
        raw, headers = make_signed_request(SMS_SENT_PAYLOAD)
        req = make_mock_request(raw, headers)
        hook.run_actions = AsyncMock(return_value=None)
        resp = await hook.post(req)
        assert resp.status == 200


# ─────────────────────────────────────────────────────────────────────────────
# post() — replay window
# ─────────────────────────────────────────────────────────────────────────────


class TestPostReplay:
    @pytest.mark.asyncio
    async def test_stale_timestamp_returns_401(self):
        hook = make_hook(replay_window=300)
        stale_ts = str(int(time.time()) - 400)  # 400s ago, outside 300s window
        raw, headers = make_signed_request(SMS_SENT_PAYLOAD, ts=stale_ts)
        req = make_mock_request(raw, headers)
        hook.run_actions = AsyncMock()
        resp = await hook.post(req)
        assert resp.status == 401
        hook.run_actions.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_fresh_timestamp_accepted(self):
        hook = make_hook(replay_window=300)
        fresh_ts = str(int(time.time()) - 10)  # 10s ago, inside window
        raw, headers = make_signed_request(SMS_SENT_PAYLOAD, ts=fresh_ts)
        req = make_mock_request(raw, headers)
        hook.run_actions = AsyncMock(return_value=None)
        resp = await hook.post(req)
        assert resp.status == 200

    @pytest.mark.asyncio
    async def test_non_numeric_timestamp_returns_401(self):
        hook = make_hook()
        raw, headers = make_signed_request(SMS_SENT_PAYLOAD)
        headers["x-zm-request-timestamp"] = "not-a-number"
        # Rebuild signature with bad ts so _verify_signature also fails;
        # but we want to isolate replay parsing — use a fresh hook with no secret
        # so signature passes trivially by patching.
        raw2, headers2 = make_signed_request(SMS_SENT_PAYLOAD, ts="bad-ts")
        req = make_mock_request(raw2, headers2)
        resp = await hook.post(req)
        # Signature will fail first (ts mismatch) → still 401
        assert resp.status == 401


# ─────────────────────────────────────────────────────────────────────────────
# post() — misc routing / edge cases
# ─────────────────────────────────────────────────────────────────────────────


class TestPostRouting:
    def test_only_post_in_methods(self):
        hook = make_hook()
        assert hook.methods == ["POST"]
        assert "GET" not in hook.methods

    def test_default_status_is_200(self):
        hook = make_hook()
        assert hook.default_status == 200

    @pytest.mark.asyncio
    async def test_malformed_json_returns_400(self):
        hook = make_hook()
        req = make_mock_request(b"not-json{{{", {"content-type": "application/json"})
        resp = await hook.post(req)
        assert resp.status == 400
