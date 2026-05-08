"""Unit tests for PersistZoomEvent action.

DB is fully mocked — no real Postgres required.
"""
import hashlib
import json
import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from flowtask.hooks.actions.zoom_event import (
    PersistZoomEvent,
    ZoomEventEnvelope,
    _compute_dedupe_hash,
)
from .fixtures import SMS_SENT_PAYLOAD


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def make_action(row_return={"id": 42}) -> PersistZoomEvent:
    """Build a PersistZoomEvent with mocked _db and _logger."""
    action = object.__new__(PersistZoomEvent)
    action._logger = logging.getLogger("test.persist_zoom_event")
    action.table = "navigator.zoom_events_raw"
    action.dsn = None
    action._db = MagicMock()
    action._db.fetch_one = AsyncMock(return_value=row_return)
    return action


# ─────────────────────────────────────────────────────────────────────────────
# _compute_dedupe_hash
# ─────────────────────────────────────────────────────────────────────────────


class TestComputeDedupeHash:
    def test_sms_sent_uses_session_message_form(self):
        h = _compute_dedupe_hash("phone.sms_sent", SMS_SENT_PAYLOAD)
        expected = hashlib.sha256(
            b"phone.sms_sent:SESSION_FAKE_1:MSG_FAKE_1"
        ).hexdigest()
        assert h == expected

    def test_sms_received_uses_session_message_form(self):
        payload = {
            "event": "phone.sms_received",
            "payload": {
                "object": {
                    "session_id": "SES_RX",
                    "message_id": "MSG_RX",
                }
            },
        }
        h = _compute_dedupe_hash("phone.sms_received", payload)
        expected = hashlib.sha256(b"phone.sms_received:SES_RX:MSG_RX").hexdigest()
        assert h == expected

    def test_sms_missing_session_id_falls_back_to_canonical(self):
        payload = {
            "event": "phone.sms_sent",
            "payload": {"object": {"message_id": "X"}},
        }
        h = _compute_dedupe_hash("phone.sms_sent", payload)
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        assert h == hashlib.sha256(canonical.encode()).hexdigest()

    def test_sms_missing_message_id_falls_back_to_canonical(self):
        payload = {
            "event": "phone.sms_sent",
            "payload": {"object": {"session_id": "X"}},
        }
        h = _compute_dedupe_hash("phone.sms_sent", payload)
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        assert h == hashlib.sha256(canonical.encode()).hexdigest()

    def test_unknown_event_uses_canonical_hash(self):
        payload = {"event": "phone.callee_answered", "payload": {"account_id": "A"}}
        h = _compute_dedupe_hash("phone.callee_answered", payload)
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        assert h == hashlib.sha256(canonical.encode()).hexdigest()

    def test_canonical_hash_stable_under_key_reordering(self):
        a = {"event": "x", "payload": {"a": 1, "b": 2}}
        b = {"payload": {"b": 2, "a": 1}, "event": "x"}
        assert _compute_dedupe_hash("x", a) == _compute_dedupe_hash("x", b)

    def test_canonical_hash_differs_for_different_content(self):
        a = {"event": "x", "value": 1}
        b = {"event": "x", "value": 2}
        assert _compute_dedupe_hash("x", a) != _compute_dedupe_hash("x", b)


# ─────────────────────────────────────────────────────────────────────────────
# ZoomEventEnvelope
# ─────────────────────────────────────────────────────────────────────────────


class TestZoomEventEnvelope:
    def test_empty_event_raises(self):
        with pytest.raises(Exception):
            ZoomEventEnvelope(event="", event_ts="2026-04-30T00:00:00Z")

    def test_valid_envelope(self):
        env = ZoomEventEnvelope(
            event="phone.sms_sent",
            account_id="ACCT",
            event_ts="2026-04-30T18:17:33Z",
        )
        assert env.event == "phone.sms_sent"
        assert env.account_id == "ACCT"

    def test_account_id_optional(self):
        env = ZoomEventEnvelope(event="phone.sms_sent", event_ts="2026-04-30T00:00:00Z")
        assert env.account_id is None


# ─────────────────────────────────────────────────────────────────────────────
# PersistZoomEvent.run()
# ─────────────────────────────────────────────────────────────────────────────


class TestPersistZoomEventRun:
    @pytest.mark.asyncio
    async def test_inserts_sms_sent_returns_id(self):
        action = make_action(row_return={"id": 42})
        rid = await action.run(
            hook=MagicMock(),
            payload=SMS_SENT_PAYLOAD,
            raw_body=json.dumps(SMS_SENT_PAYLOAD).encode(),
            headers={"x-zm-trackingid": "T1", "x-zm-signature": "v0=secret"},
        )
        assert rid == 42

    @pytest.mark.asyncio
    async def test_signature_never_persisted(self):
        action = make_action(row_return={"id": 1})
        await action.run(
            hook=MagicMock(),
            payload=SMS_SENT_PAYLOAD,
            headers={"x-zm-trackingid": "T1", "x-zm-signature": "v0=secret"},
        )
        call_args = action._db.fetch_one.await_args
        persisted_headers = call_args.args[5]
        assert "x-zm-signature" not in persisted_headers
        assert persisted_headers.get("x-zm-trackingid") == "T1"

    @pytest.mark.asyncio
    async def test_tracking_id_persisted(self):
        action = make_action(row_return={"id": 1})
        await action.run(
            hook=MagicMock(),
            payload=SMS_SENT_PAYLOAD,
            headers={"x-zm-trackingid": "TRK-123", "x-zm-request-timestamp": "12345"},
        )
        call_args = action._db.fetch_one.await_args
        persisted_headers = call_args.args[5]
        assert persisted_headers["x-zm-trackingid"] == "TRK-123"
        assert persisted_headers["x-zm-request-timestamp"] == "12345"

    @pytest.mark.asyncio
    async def test_dedupe_conflict_returns_none(self):
        action = make_action(row_return=None)
        rid = await action.run(hook=MagicMock(), payload=SMS_SENT_PAYLOAD)
        assert rid is None

    @pytest.mark.asyncio
    async def test_invalid_envelope_empty_payload_returns_none(self):
        action = make_action()
        rid = await action.run(hook=MagicMock(), payload={})
        assert rid is None
        action._db.fetch_one.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_missing_payload_kwarg_returns_none(self):
        action = make_action()
        rid = await action.run(hook=MagicMock(), payload=None)
        assert rid is None
        action._db.fetch_one.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_persists_unknown_event_via_canonical_hash(self):
        payload = {
            "event": "phone.callee_answered",
            "payload": {"account_id": "ACCT"},
            "event_ts": 1777573053716,
        }
        action = make_action(row_return={"id": 99})
        rid = await action.run(hook=MagicMock(), payload=payload)
        assert rid == 99

    @pytest.mark.asyncio
    async def test_run_without_headers_uses_empty_dict(self):
        action = make_action(row_return={"id": 5})
        rid = await action.run(hook=MagicMock(), payload=SMS_SENT_PAYLOAD)
        assert rid == 5
        call_args = action._db.fetch_one.await_args
        persisted_headers = call_args.args[5]
        assert persisted_headers == {}

    @pytest.mark.asyncio
    async def test_correct_sql_table_used(self):
        action = make_action(row_return={"id": 1})
        await action.run(hook=MagicMock(), payload=SMS_SENT_PAYLOAD)
        sql_arg = action._db.fetch_one.await_args.args[0]
        assert "navigator.zoom_events_raw" in sql_arg
        assert "ON CONFLICT (dedupe_hash) DO NOTHING" in sql_arg
