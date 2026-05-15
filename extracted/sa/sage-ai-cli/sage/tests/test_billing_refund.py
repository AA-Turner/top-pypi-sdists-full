"""Tests for the 14-day refund flow.

Mocks the Firestore record + PayPal API responses; exercises every refusal
branch (no subscription / outside window / no captured payment / PayPal error)
plus the happy path.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

import pytest

os.environ.setdefault("SAGE_FIREBASE_API_KEY", "test-dummy")
os.environ.setdefault("FIREBASE_PROJECT_ID", "test-project")


from backend.billing import refund_subscription, REFUND_WINDOW_DAYS


def _user_record(activated_days_ago: int | None = 3, with_sub: bool = True) -> dict:
    rec = {}
    if with_sub:
        rec["paypal_subscription_id"] = "I-SUBFAKE123"
    if activated_days_ago is not None:
        activated = datetime.now(timezone.utc) - timedelta(days=activated_days_ago)
        rec["subscription_activated"] = activated.isoformat()
    return rec


class TestRefundSubscriptionRefusals:

    def test_no_subscription_returns_404_reason(self):
        with patch("backend.billing.get_user_record", return_value={}):
            result = refund_subscription("u-1")
        assert result["ok"] is False
        assert result["reason"] == "no_subscription"

    def test_missing_activation_timestamp(self):
        rec = _user_record(activated_days_ago=None)
        with patch("backend.billing.get_user_record", return_value=rec):
            result = refund_subscription("u-1")
        assert result["ok"] is False
        assert result["reason"] == "no_activation_timestamp"

    def test_bad_activation_timestamp(self):
        rec = {"paypal_subscription_id": "sub-1", "subscription_activated": "garbage"}
        with patch("backend.billing.get_user_record", return_value=rec):
            result = refund_subscription("u-1")
        assert result["ok"] is False
        assert result["reason"] == "bad_activation_timestamp"

    def test_outside_window_refused(self):
        rec = _user_record(activated_days_ago=REFUND_WINDOW_DAYS + 5)
        with patch("backend.billing.get_user_record", return_value=rec):
            result = refund_subscription("u-1")
        assert result["ok"] is False
        assert result["reason"] == "outside_window"
        assert result["days_into_window"] == REFUND_WINDOW_DAYS + 5
        assert result["window_days"] == REFUND_WINDOW_DAYS


class TestRefundSubscriptionHappyPath:

    def test_refund_succeeds_within_window(self):
        rec = _user_record(activated_days_ago=3)
        transactions = {"transactions": [{
            "id": "TXN-1",
            "status": "COMPLETED",
            "time": "2026-05-12T00:00:00Z",
            "amount_with_breakdown": {"gross_amount": {"value": "19.00"}},
        }]}
        refund_resp = MagicMock(status_code=201)
        refund_resp.json.return_value = {"id": "REF-1"}

        with patch("backend.billing.get_user_record", return_value=rec), \
             patch("backend.billing._paypal_token", return_value="ppl-token"), \
             patch("backend.billing.httpx.get") as mock_get, \
             patch("backend.billing.httpx.post", return_value=refund_resp) as mock_post, \
             patch("backend.billing.cancel_subscription") as mock_cancel, \
             patch("backend.billing._get_db", return_value=None):
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = transactions
            mock_get.return_value.raise_for_status = lambda: None
            result = refund_subscription("u-1")

        assert result["ok"] is True
        assert result["reason"] == "refunded"
        assert result["amount"] == "19.00"
        assert result["refund_id"] == "REF-1"
        # Subscription was cancelled after the refund
        mock_cancel.assert_called_once_with("u-1")
        # Refund POST went to the right URL
        assert "/refund" in mock_post.call_args[0][0]


class TestRefundSubscriptionErrors:

    def test_no_captured_payment(self):
        rec = _user_record(activated_days_ago=3)
        with patch("backend.billing.get_user_record", return_value=rec), \
             patch("backend.billing._paypal_token", return_value="ppl"), \
             patch("backend.billing.httpx.get") as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = {"transactions": []}
            mock_get.return_value.raise_for_status = lambda: None
            result = refund_subscription("u-1")
        assert result["ok"] is False
        assert result["reason"] == "no_captured_payment"

    def test_paypal_5xx_on_transactions_fetch(self):
        rec = _user_record(activated_days_ago=3)
        with patch("backend.billing.get_user_record", return_value=rec), \
             patch("backend.billing._paypal_token", return_value="ppl"), \
             patch("backend.billing.httpx.get", side_effect=RuntimeError("paypal 500")):
            result = refund_subscription("u-1")
        assert result["ok"] is False
        assert result["reason"] == "paypal_error"

    def test_paypal_refund_endpoint_returns_4xx(self):
        rec = _user_record(activated_days_ago=3)
        transactions = {"transactions": [{
            "id": "TXN-1", "status": "COMPLETED", "time": "2026-05-12T00:00:00Z",
            "amount_with_breakdown": {"gross_amount": {"value": "19.00"}},
        }]}
        refund_fail = MagicMock(status_code=422, text="Refund denied by PayPal")
        with patch("backend.billing.get_user_record", return_value=rec), \
             patch("backend.billing._paypal_token", return_value="ppl"), \
             patch("backend.billing.httpx.get") as mock_get, \
             patch("backend.billing.httpx.post", return_value=refund_fail):
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = transactions
            mock_get.return_value.raise_for_status = lambda: None
            result = refund_subscription("u-1")
        assert result["ok"] is False
        assert result["reason"] == "paypal_error"
        assert "Refund denied" in result["detail"]


class TestRefundEndpointHttp:
    """Test the /billing/refund FastAPI endpoint round-trip."""

    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        from backend.app import app
        return TestClient(app)

    def test_endpoint_requires_auth(self, client):
        r = client.post("/billing/refund")
        # No Authorization header → either 401 or 403
        assert r.status_code in (401, 403)
