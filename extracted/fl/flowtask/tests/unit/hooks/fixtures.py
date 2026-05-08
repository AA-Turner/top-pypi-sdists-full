"""Shared helpers and payloads for ZoomWebHook unit tests."""
import hashlib
import hmac
import json
import time

ZOOM_SECRET = "test-secret-do-not-use-in-prod"


def make_signed_request(
    payload: dict,
    secret: str = ZOOM_SECRET,
    ts: str | None = None,
) -> tuple[bytes, dict]:
    """Return (raw_body_bytes, headers_dict) with a valid x-zm-signature."""
    raw = json.dumps(payload).encode("utf-8")
    ts = ts or str(int(time.time()))
    msg = f"v0:{ts}:{raw.decode()}".encode()
    sig = "v0=" + hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()
    return raw, {
        "x-zm-signature": sig,
        "x-zm-request-timestamp": ts,
        "content-type": "application/json",
    }


SMS_SENT_PAYLOAD = {
    "event": "phone.sms_sent",
    "payload": {
        "account_id": "ACCT_FAKE",
        "object": {
            "sender": {"phone_number": "15550000001"},
            "owner": {
                "type": "callQueue",
                "id": "QUEUE_FAKE",
                "sms_sender_user_id": "USER_FAKE_AGENT",
            },
            "message": "Test reply from queue",
            "to_members": [{"phone_number": "15550000002"}],
            "session_id": "SESSION_FAKE_1",
            "message_id": "MSG_FAKE_1",
            "message_type": 1,
            "date_time": "2026-04-30T18:17:33Z",
        },
    },
    "event_ts": 1777573053716,
}

CRC_PAYLOAD = {
    "event": "endpoint.url_validation",
    "payload": {"plainToken": "test-plain-token-abc"},
}
