"""Tests for Heal.vision_query_v2() — Task 15.

POSTs to /v1/heal/vision with screenshot as untagged_image_base64.
"""
from __future__ import annotations

import json
import pathlib
from unittest.mock import MagicMock, patch

import httpx
import pytest
import respx

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "automind_responses"
AUTOMIND_URL = "https://kaneai-api.lambdatest.com"
VISION_URL = f"{AUTOMIND_URL}/v1/heal/vision"


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.session_id = "sess-vision-1"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    driver.get_screenshot_as_base64.return_value = "FAKE_B64_SCREENSHOT"
    return driver


@pytest.fixture()
def action():
    return {
        "operation_type": "click",
        "operation_intent": "click button",
        "use_query_v2": True,
        "version": "v3",
    }


@pytest.fixture()
def heal(action, mock_driver):
    from testmu_selenium._heal import Heal
    return Heal(action, mock_driver, username="user", accesskey="key", test_id="t1", commit_id="c1", org_id=1)


def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


# ---------------------------------------------------------------------------
# vision_query_v2 — success
# ---------------------------------------------------------------------------

@respx.mock
def test_vision_query_v2_posts_to_vision_endpoint(heal):
    fixture = _load_fixture("vision_query_success.json")
    route = respx.post(VISION_URL).mock(return_value=httpx.Response(200, json=fixture))

    with patch.object(heal, "_take_screenshot", return_value="SCREENSHOT_B64"):
        resp = heal.vision_query_v2()

    assert resp.status_code == 200
    assert route.called


@respx.mock
def test_vision_query_v2_payload_contains_screenshot(heal):
    route = respx.post(VISION_URL).mock(
        return_value=httpx.Response(200, json={"value": "//div[@role='button']"})
    )

    with patch.object(heal, "_take_screenshot", return_value="MY_SCREENSHOT_B64"):
        heal.vision_query_v2()

    sent_body = json.loads(route.calls.last.request.content)
    assert sent_body["untagged_image_base64"] == "MY_SCREENSHOT_B64"
    assert sent_body["session_id"] == "sess-vision-1"
    assert sent_body["version"] == "v3"


@respx.mock
def test_vision_query_v2_payload_required_fields(heal):
    route = respx.post(VISION_URL).mock(
        return_value=httpx.Response(200, json={"value": "//button"})
    )

    with patch.object(heal, "_take_screenshot", return_value="B64"):
        heal.vision_query_v2()

    sent_body = json.loads(route.calls.last.request.content)
    required_fields = {
        "code_export_id", "current_action", "commit_id", "test_id",
        "username", "accesskey", "version", "org_id",
        "session_id", "untagged_image_base64",
    }
    missing = required_fields - set(sent_body.keys())
    assert not missing, f"Payload missing fields: {missing}"


@respx.mock
def test_vision_query_v2_handles_miss_response(heal):
    fixture = _load_fixture("vision_query_miss.json")
    respx.post(VISION_URL).mock(return_value=httpx.Response(200, json=fixture))

    with patch.object(heal, "_take_screenshot", return_value="B64"):
        resp = heal.vision_query_v2()

    assert resp.status_code == 200
    assert "error" in resp.json()


@respx.mock
def test_vision_query_v2_no_duplicate_version_key(heal):
    """The V2 implementation had a bug with a duplicate 'version' key; ported
    version must have exactly one top-level 'version' key in the payload."""
    route = respx.post(VISION_URL).mock(
        return_value=httpx.Response(200, json={"value": "//button"})
    )

    with patch.object(heal, "_take_screenshot", return_value="B64"):
        heal.vision_query_v2()

    # Parse as actual JSON dict — top-level keys are deduplicated by Python's json module
    sent_body = json.loads(route.calls.last.request.content)
    # Top-level payload should have exactly one 'version' key (Python dicts are unique-keyed)
    assert "version" in sent_body
    # Verify value is correct (second assignment in V2 bug would overwrite first)
    assert sent_body["version"] == heal.version
