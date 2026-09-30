"""Automind ``page_not_ready`` (409) retry — V2 parity.

The VQE does not retry internally: on ``loader_detected`` it answers 409 with
``{"error": "page_not_ready"}`` and the client owns the retry budget
(auteur-automind ``app/api/endpoints/healer.py``). Retrying at the transport
layer would re-POST the same stale screenshot, so the budget has to wrap the
screenshot capture — these tests pin exactly that.

Reference: the V2 source
``Heal.vision_query`` — 3 POSTs, 3s apart, fresh screenshot per attempt.
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import httpx
import pytest
import respx

from testmu_selenium._helpers import _page_ready

AUTOMIND_URL = "https://kaneai-api.lambdatest.com"
VISION_URL = f"{AUTOMIND_URL}/v1/heal/vision"

PAGE_NOT_READY_BODY = {
    "error": "page_not_ready",
    "loader_reason": "spinner@center",
}


@pytest.fixture(autouse=True)
def _no_real_sleep():
    """The budget sleeps 3s between attempts; tests must not actually wait."""
    with patch.object(_page_ready.time, "sleep") as m_sleep:
        yield m_sleep


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.session_id = "sess-pnr-1"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    driver.get_screenshot_as_base64.return_value = "FAKE_B64_SCREENSHOT"
    return driver


@pytest.fixture()
def heal(mock_driver):
    from testmu_selenium._heal import Heal
    return Heal(
        {"operation_type": "VISION_QUERY", "operation_intent": "is X present?"},
        mock_driver,
        username="user", accesskey="key", test_id="t1", commit_id="c1", org_id=1,
    )


# ---------------------------------------------------------------------------
# is_page_not_ready_response — BOTH halves required
# ---------------------------------------------------------------------------

def test_detects_409_with_page_not_ready_body():
    resp = httpx.Response(409, json=PAGE_NOT_READY_BODY)
    assert _page_ready.is_page_not_ready_response(resp) is True


def test_409_with_a_different_error_is_not_a_loader_signal():
    resp = httpx.Response(409, json={"error": "something_else"})
    assert _page_ready.is_page_not_ready_response(resp) is False


def test_page_not_ready_body_on_a_non_409_is_not_a_loader_signal():
    resp = httpx.Response(500, json=PAGE_NOT_READY_BODY)
    assert _page_ready.is_page_not_ready_response(resp) is False


def test_non_json_409_is_not_a_loader_signal():
    resp = httpx.Response(409, text="<html>gateway</html>")
    assert _page_ready.is_page_not_ready_response(resp) is False


def test_none_response_is_not_a_loader_signal():
    assert _page_ready.is_page_not_ready_response(None) is False


# ---------------------------------------------------------------------------
# retry_on_page_not_ready — budget shape
# ---------------------------------------------------------------------------

def test_success_on_first_attempt_makes_exactly_one_call(_no_real_sleep):
    attempt = MagicMock(return_value=httpx.Response(200, json={"vision_query": True}))
    out = _page_ready.retry_on_page_not_ready(attempt, label="t")
    assert attempt.call_count == 1
    assert out.status_code == 200
    _no_real_sleep.assert_not_called()


def test_exhausts_three_attempts_with_two_sleeps(_no_real_sleep):
    attempt = MagicMock(return_value=httpx.Response(409, json=PAGE_NOT_READY_BODY))
    out = _page_ready.retry_on_page_not_ready(attempt, label="t")
    assert attempt.call_count == _page_ready.MAX_ATTEMPTS == 3
    # No sleep after the final attempt — that would be dead latency on the
    # failure path (V2 parity).
    assert _no_real_sleep.call_count == 2
    _no_real_sleep.assert_called_with(_page_ready.SLEEP_SECONDS)
    # The terminal 409 is handed back, not swallowed — the caller raises from
    # its body so loader_reason survives.
    assert out.status_code == 409


def test_recovers_when_a_later_attempt_succeeds(_no_real_sleep):
    attempt = MagicMock(side_effect=[
        httpx.Response(409, json=PAGE_NOT_READY_BODY),
        httpx.Response(200, json={"vision_query": True}),
    ])
    out = _page_ready.retry_on_page_not_ready(attempt, label="t")
    assert attempt.call_count == 2
    assert out.status_code == 200
    assert _no_real_sleep.call_count == 1


# ---------------------------------------------------------------------------
# Heal.vision_query — the retry must retake the screenshot
# ---------------------------------------------------------------------------

@respx.mock
def test_vision_query_retakes_screenshot_every_attempt(heal):
    respx.post(VISION_URL).mock(return_value=httpx.Response(409, json=PAGE_NOT_READY_BODY))

    with patch.object(heal, "_take_screenshot", return_value="SHOT") as m_shot:
        resp = heal.vision_query()

    # 3 POSTs, and critically 3 screenshots — a retry that reuses the stale
    # capture can never observe a settled page.
    assert m_shot.call_count == 3
    assert respx.calls.call_count == 3
    assert resp.status_code == 409


@respx.mock
def test_vision_query_sends_a_fresh_request_id_per_attempt(heal):
    respx.post(VISION_URL).mock(return_value=httpx.Response(409, json=PAGE_NOT_READY_BODY))

    with patch.object(heal, "_take_screenshot", return_value="SHOT"):
        heal.vision_query()

    ids = [json.loads(c.request.content)["request_id"] for c in respx.calls]
    assert len(ids) == 3
    # Distinct ids keep each attempt's VQE debug data in its own Azure folder
    # ({org_id}/vqe/{request_id}) instead of overwriting the previous attempt.
    assert len(set(ids)) == 3


@respx.mock
def test_vision_query_v2_shares_the_same_budget(heal):
    respx.post(VISION_URL).mock(return_value=httpx.Response(409, json=PAGE_NOT_READY_BODY))

    with patch.object(heal, "_take_screenshot", return_value="SHOT") as m_shot:
        resp = heal.vision_query_v2()

    assert m_shot.call_count == 3
    assert respx.calls.call_count == 3
    assert resp.status_code == 409


@respx.mock
def test_vision_query_does_not_retry_a_plain_success(heal):
    respx.post(VISION_URL).mock(return_value=httpx.Response(200, json={"vision_query": True}))

    with patch.object(heal, "_take_screenshot", return_value="SHOT") as m_shot:
        resp = heal.vision_query()

    assert m_shot.call_count == 1
    assert respx.calls.call_count == 1
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# visionQuery — the terminal error keeps the loader diagnostics
# ---------------------------------------------------------------------------

def test_visionQuery_raises_with_loader_reason_after_the_budget():
    from testmu_selenium._helpers.vision_query import visionQuery

    with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
         patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
         patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
        m_heal.return_value.vision_query.return_value.json.return_value = PAGE_NOT_READY_BODY
        with pytest.raises(RuntimeError) as exc:
            visionQuery("Is X present?", "bool")

    msg = str(exc.value)
    # auteur's code_generation.py routes on `"page_not_ready" in str(e)` to show
    # PAGE_NOT_READY_AFTER_RETRIES instead of a generic action failure — the
    # substring is load-bearing, not cosmetic.
    assert "page_not_ready" in msg
    assert "spinner@center" in msg
    assert "client_attempts=3" in msg


def test_visionQuery_other_errors_keep_the_plain_message():
    from testmu_selenium._helpers.vision_query import visionQuery

    with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
         patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
         patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
        m_heal.return_value.vision_query.return_value.json.return_value = {"error": "boom"}
        with pytest.raises(RuntimeError, match="visionQuery failed: boom"):
            visionQuery("Is X present?", "bool")
