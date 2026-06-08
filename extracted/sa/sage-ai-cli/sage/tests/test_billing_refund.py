"""Tests for the no-refunds policy.

Sage AI does not offer refunds. `refund_subscription()` always returns
`{ok: False, reason: "not_offered", ...}` and the `/billing/refund`
endpoint always returns HTTP 400. These tests pin that contract so a
future refactor can't accidentally re-introduce a refund path.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("SAGE_FIREBASE_API_KEY", "test-dummy")
os.environ.setdefault("FIREBASE_PROJECT_ID", "test-project")


from backend.billing import refund_subscription, REFUND_WINDOW_DAYS


class TestRefundsAreNeverIssued:
    """The function-level contract: refund_subscription always refuses."""

    def test_returns_not_offered(self):
        result = refund_subscription("any-uid")
        assert result["ok"] is False
        assert result["reason"] == "not_offered"

    def test_includes_policy_message(self):
        result = refund_subscription("any-uid")
        msg = result.get("message", "").lower()
        # Must mention no-refunds posture and cancellation path
        assert "no refund" in msg or "all sales are final" in msg
        assert "cancel" in msg

    def test_points_to_cancel_endpoint(self):
        result = refund_subscription("any-uid")
        assert result.get("cancel_endpoint") == "DELETE /billing/subscription"

    def test_works_with_unknown_uid(self):
        # Even with a uid that has no Firestore record, the refusal still
        # comes back consistently — we don't leak account-existence info.
        result = refund_subscription("zzz-totally-fake")
        assert result["ok"] is False
        assert result["reason"] == "not_offered"

    def test_works_with_empty_uid(self):
        result = refund_subscription("")
        assert result["ok"] is False
        assert result["reason"] == "not_offered"


class TestRefundWindowConstantSentinel:
    """REFUND_WINDOW_DAYS = 0 — sentinel meaning 'no window exists'."""

    def test_constant_is_zero(self):
        assert REFUND_WINDOW_DAYS == 0


class TestRefundEndpointHttp:
    """The /billing/refund endpoint should 400 with the policy message."""

    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        from backend.app import app
        return TestClient(app)

    def test_endpoint_requires_auth(self, client):
        r = client.post("/billing/refund")
        # No Authorization → either 401 or 403
        assert r.status_code in (401, 403)
