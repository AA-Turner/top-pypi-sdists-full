"""Tests for Heal.list_xpaths() — Tier 1 of V3 autoheal cascade.

Uses respx.mock to mock AUTOMIND HTTP calls.
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
XPATHS_URL = f"{AUTOMIND_URL}/v1/heal/xpaths"


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.session_id = "sess-abc-123"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    driver.get_screenshot_as_base64.return_value = "FAKE_B64_SCREENSHOT"
    # execute_script used in non-mobile path: tagifyWebpage, fetchJsonData, etc.
    driver.execute_script.side_effect = lambda script, *args: (
        '{"1": {"xpath": "//button", "frameInformation": null}}'
        if "fetchJsonData" in script
        else None
    )
    return driver


@pytest.fixture()
def action():
    return {
        "operation_type": "click",
        "operation_intent": "click sign-in button",
        "use_query_v2": True,
        "version": "v3",
    }


@pytest.fixture()
def heal(action, mock_driver):
    from testmu_selenium._heal import Heal
    return Heal(
        action,
        mock_driver,
        username="user",
        accesskey="key",
        test_id="t1",
        commit_id="c1",
        org_id=1,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def _make_execute_script_side_effect(xpath_json: str, desc_json: str = '{}', page_source: str = "<html/>"):
    """Return a side_effect callable for driver.execute_script that handles
    the different JS calls made in the non-mobile list_xpaths path."""
    def _side_effect(script, *args):
        if "fetchJsonData" in script and "JSONOutput" in script:
            return xpath_json
        if "fetchJsonData" in script and "descOutput" in script:
            return desc_json
        if "document.body.outerHTML" in script:
            return page_source
        if "window.innerWidth" in script:
            return [1280, 800]
        return None
    return _side_effect


# ---------------------------------------------------------------------------
# list_xpaths — success
# ---------------------------------------------------------------------------

@respx.mock
def test_list_xpaths_returns_200_response(heal, mock_driver):
    fixture = _load_fixture("list_xpaths_success.json")
    route = respx.post(XPATHS_URL).mock(
        return_value=httpx.Response(200, json=fixture)
    )

    mock_driver.execute_script.side_effect = _make_execute_script_side_effect(
        xpath_json='{"1": {"xpath": "//button", "frameInformation": null}}',
    )

    # Patch _take_screenshot so it doesn't need real driver CDP
    with patch.object(heal, "_take_screenshot", return_value="FAKE_B64"):
        resp = heal.list_xpaths()

    assert resp.status_code == 200
    body = resp.json()
    assert "xpaths" in body
    assert route.called


@respx.mock
def test_list_xpaths_payload_includes_required_fields(heal, mock_driver):
    """Verify the POST body contains all fields mandated by the AUTOMIND wire schema."""
    fixture = _load_fixture("list_xpaths_success.json")
    route = respx.post(XPATHS_URL).mock(
        return_value=httpx.Response(200, json=fixture)
    )

    mock_driver.execute_script.side_effect = _make_execute_script_side_effect(
        xpath_json='{"1": {"xpath": "//button", "frameInformation": null}}',
    )

    with patch.object(heal, "_take_screenshot", return_value="FAKE_B64"):
        heal.list_xpaths()

    assert route.called
    sent_body = json.loads(route.calls.last.request.content)

    required_fields = {
        "code_export_id", "current_action", "prev_actions",
        "xpath_mapping", "tagified_image", "commit_id", "test_id",
        "username", "accesskey", "tags_description", "org_id",
        "page_source", "session_id", "use_query_v2",
        "untagged_image_base64", "version",
    }
    missing = required_fields - set(sent_body.keys())
    assert not missing, f"Payload missing fields: {missing}"


@respx.mock
def test_list_xpaths_payload_session_id_and_action(heal, mock_driver):
    fixture = _load_fixture("list_xpaths_success.json")
    route = respx.post(XPATHS_URL).mock(
        return_value=httpx.Response(200, json=fixture)
    )

    mock_driver.execute_script.side_effect = _make_execute_script_side_effect(
        xpath_json='{"1": {"xpath": "//button", "frameInformation": null}}',
    )

    with patch.object(heal, "_take_screenshot", return_value="FAKE_B64"):
        heal.list_xpaths()

    sent_body = json.loads(route.calls.last.request.content)
    assert sent_body["session_id"] == "sess-abc-123"
    assert sent_body["current_action"]["operation_type"] == "click"


# ---------------------------------------------------------------------------
# list_xpaths — miss (empty xpaths array)
# ---------------------------------------------------------------------------

@respx.mock
def test_list_xpaths_handles_empty_xpaths_miss(heal, mock_driver):
    fixture = _load_fixture("list_xpaths_miss.json")
    respx.post(XPATHS_URL).mock(
        return_value=httpx.Response(200, json=fixture)
    )

    mock_driver.execute_script.side_effect = _make_execute_script_side_effect(
        xpath_json='{}',
    )

    with patch.object(heal, "_take_screenshot", return_value="FAKE_B64"):
        resp = heal.list_xpaths()

    assert resp.status_code == 200
    assert resp.json()["xpaths"] == []


# ---------------------------------------------------------------------------
# list_xpaths — 5xx retry
# ---------------------------------------------------------------------------

@respx.mock
def test_list_xpaths_retries_on_non_200(heal, mock_driver):
    """Non-200 response triggers the inner retry loop (max_attempt=2)."""
    route = respx.post(XPATHS_URL).mock(side_effect=[
        httpx.Response(500, json={"error": "server error"}),
        httpx.Response(200, json={"xpaths": ["//button"], "frameInformation": None}),
    ])

    mock_driver.execute_script.side_effect = _make_execute_script_side_effect(
        xpath_json='{"1": {"xpath": "//button", "frameInformation": null}}',
    )

    with patch.object(heal, "_take_screenshot", return_value="FAKE_B64"):
        resp = heal.list_xpaths()

    assert resp.status_code == 200
    assert route.call_count == 2


@respx.mock
def test_list_xpaths_returns_last_response_if_all_attempts_fail(heal, mock_driver):
    """If both attempts fail (non-200), the last response is returned."""
    route = respx.post(XPATHS_URL).mock(
        return_value=httpx.Response(500, json={"error": "server error"})
    )

    mock_driver.execute_script.side_effect = _make_execute_script_side_effect(
        xpath_json='{"1": {"xpath": "//button", "frameInformation": null}}',
    )

    with patch.object(heal, "_take_screenshot", return_value="FAKE_B64"):
        resp = heal.list_xpaths()

    # Both max_attempt iterations exhausted — should still return a response
    assert resp is not None
    assert resp.status_code == 500


# ---------------------------------------------------------------------------
# list_xpaths — mobile_tagify path (with tagify script set)
# ---------------------------------------------------------------------------

@respx.mock
def test_list_xpaths_mobile_tagify_path(action, mock_driver):
    """When mobile_tagify is set, tagifyWebpage is injected and its response used."""
    from testmu_selenium._heal import Heal

    fixture = _load_fixture("list_xpaths_success.json")
    respx.post(XPATHS_URL).mock(return_value=httpx.Response(200, json=fixture))

    # Simulate tagify response from execute_script
    tagify_response = {
        "xpaths": {"1": "//button"},
        "descriptions": {"1": "Button"},
        "outerHTML": "<body></body>",
        "rects": {},
    }

    def _execute_script_side_effect(script, *args):
        # First call is driver.execute_script(self.mobile_tagify) — returns None
        # Second call is tagifyWebpage(...) — returns tagify_response dict
        if "tagifyWebpage" in script:
            return tagify_response
        return None

    mock_driver.execute_script.side_effect = _execute_script_side_effect

    heal = Heal(action, mock_driver, username="u", accesskey="k")
    heal.mobile_tagify = "// mobile tagify script js"  # simulate host runtime

    with patch("testmu_selenium._heal.make_tagged_screenshot", return_value=("TAGGED_B64", 2.0)):
        with patch.object(heal, "_take_screenshot", return_value="UNTAGGED_B64"):
            resp = heal.list_xpaths()

    assert resp.status_code == 200
    assert heal.untagged_image_base64 == "UNTAGGED_B64"
    assert heal.tagified_image == "TAGGED_B64"
