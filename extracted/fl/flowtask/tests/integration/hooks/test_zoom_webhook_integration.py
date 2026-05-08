"""End-to-end integration tests for the Zoom webhook receiver (TASK-038).

Each test uses a unique session_id / message_id so the UNIQUE dedupe_hash
constraint prevents cross-test interference without requiring explicit
truncation between runs.

Run with::

    ZOOM_WEBHOOK_TEST_DSN="postgres://user:pass@localhost:5432/testdb" \\
        pytest tests/integration/hooks/ -v -m integration
"""
import hashlib
import hmac
import json

import pytest

from .conftest import ZOOM_SECRET, make_signed_request

_URL = "/api/v1/webhook/zoom-us-test"


def _sms_sent_payload(session_id: str, message_id: str) -> dict:
    return {
        "event": "phone.sms_sent",
        "payload": {
            "account_id": "ACCT_FAKE_INTG",
            "object": {
                "sender": {"phone_number": "15550000011"},
                "owner": {
                    "type": "callQueue",
                    "id": "QUEUE_FAKE_INTG",
                    "sms_sender_user_id": "USER_FAKE_INTG",
                },
                "message": "Integration test reply",
                "to_members": [{"phone_number": "15550000012"}],
                "session_id": session_id,
                "message_id": message_id,
                "message_type": 1,
                "date_time": "2026-04-30T18:17:33Z",
            },
        },
        "event_ts": 1777573053716,
    }


@pytest.mark.integration
async def test_end_to_end_sms_sent(zoom_client, zoom_db):
    """POST a valid phone.sms_sent event → 200 and one row in DB."""
    payload = _sms_sent_payload("SES_INTG_001", "MSG_INTG_001")
    raw, headers = make_signed_request(payload)

    resp = await zoom_client.post(_URL, data=raw, headers=headers)

    assert resp.status == 200
    rows = await zoom_db.fetch_all(
        "SELECT event FROM navigator.zoom_events_raw WHERE event = 'phone.sms_sent' "
        "AND raw->'payload'->'object'->>'session_id' = 'SES_INTG_001'"
    )
    assert rows is not None and len(rows) == 1
    assert rows[0]["event"] == "phone.sms_sent"


@pytest.mark.integration
async def test_dedupe_under_retransmission(zoom_client, zoom_db):
    """POSTing the same event twice inserts exactly one row (dedupe_hash UNIQUE)."""
    payload = _sms_sent_payload("SES_INTG_DEDUP", "MSG_INTG_DEDUP")
    raw, headers = make_signed_request(payload)

    await zoom_client.post(_URL, data=raw, headers=headers)
    resp = await zoom_client.post(_URL, data=raw, headers=headers)

    assert resp.status == 200
    count = await zoom_db.fetchval(
        "SELECT COUNT(*) FROM navigator.zoom_events_raw "
        "WHERE raw->'payload'->'object'->>'session_id' = 'SES_INTG_DEDUP'"
    )
    assert count == 1


@pytest.mark.integration
async def test_invalid_signature_rejected_and_no_persist(zoom_client, zoom_db):
    """A tampered body (signature mismatch) → 401 and zero rows persisted."""
    payload = _sms_sent_payload("SES_INTG_TAMPER", "MSG_INTG_TAMPER")
    raw, headers = make_signed_request(payload)
    raw_tampered = raw.replace(b"SES_INTG_TAMPER", b"SES_INTG_TAMPER_MODIFIED")

    resp = await zoom_client.post(_URL, data=raw_tampered, headers=headers)

    assert resp.status == 401
    count = await zoom_db.fetchval(
        "SELECT COUNT(*) FROM navigator.zoom_events_raw "
        "WHERE raw->'payload'->'object'->>'session_id' = 'SES_INTG_TAMPER_MODIFIED'"
    )
    assert count == 0


@pytest.mark.integration
async def test_persists_unknown_event_type(zoom_client, zoom_db):
    """A non-SMS event type is persisted with a canonical-JSON dedupe_hash."""
    payload = {
        "event": "phone.callee_answered",
        "payload": {"account_id": "ACCT_FAKE_INTG", "object": {"call_id": "CALL_INTG_001"}},
        "event_ts": 1777573053716,
    }
    raw, headers = make_signed_request(payload)

    resp = await zoom_client.post(_URL, data=raw, headers=headers)

    assert resp.status == 200
    row = await zoom_db.fetch_one(
        "SELECT event, dedupe_hash FROM navigator.zoom_events_raw "
        "WHERE event = 'phone.callee_answered' ORDER BY id DESC LIMIT 1"
    )
    assert row is not None
    assert row["event"] == "phone.callee_answered"
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    expected_hash = hashlib.sha256(canonical.encode()).hexdigest()
    assert row["dedupe_hash"] == expected_hash


@pytest.mark.integration
async def test_get_returns_405(zoom_client):
    """GET on the webhook route → 405 (only POST is registered)."""
    resp = await zoom_client.get(_URL)

    assert resp.status == 405


@pytest.mark.integration
async def test_crc_handshake(zoom_client):
    """CRC endpoint.url_validation → 200 with correctly signed encryptedToken."""
    plain_token = "intg-plain-token-xyz"
    payload = {"event": "endpoint.url_validation", "payload": {"plainToken": plain_token}}

    resp = await zoom_client.post(
        _URL,
        data=json.dumps(payload).encode(),
        headers={"content-type": "application/json"},
    )

    assert resp.status == 200
    body = await resp.json()
    expected = hmac.new(ZOOM_SECRET.encode(), plain_token.encode(), __import__("hashlib").sha256).hexdigest()
    assert body == {"plainToken": plain_token, "encryptedToken": expected}
