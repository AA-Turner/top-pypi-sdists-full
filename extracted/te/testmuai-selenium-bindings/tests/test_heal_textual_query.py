"""Tests for Heal.get_outer_html() and Heal.textual_query_v2() — Task 14.

get_outer_html: builds outer-HTML string by switching frames per xpath_mapping.
textual_query_v2: POSTs to /v1/heal/textual_query with a11y + DOM snapshots.
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
TEXTUAL_URL = f"{AUTOMIND_URL}/v1/heal/textual_query"


@pytest.fixture()
def mock_driver():
    driver = MagicMock()
    driver.session_id = "sess-textual-1"
    driver.capabilities = {"platformName": "linux", "browserName": "chrome"}
    driver.get_screenshot_as_base64.return_value = "FAKE_B64"
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


def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


# ---------------------------------------------------------------------------
# get_outer_html
# ---------------------------------------------------------------------------

def test_get_outer_html_returns_string(heal, mock_driver):
    """get_outer_html must return a str (possibly empty if no elements found)."""
    # Simulate execute_async_js returning JSON xpath_mapping
    xpath_mapping_json = json.dumps({
        "1": {"xpath": "//button[@id='btn']", "frameInformation": ""}
    })

    # Set up execute_script to handle execute_async_js calls
    def _execute_script_side_effect(script, *args):
        if "fetchJsonData" in script and "JSONOutput" in script:
            return xpath_mapping_json
        if "annotations" in script and "JSONOutput" in script:
            return None  # clear data
        return None

    mock_driver.execute_script.side_effect = _execute_script_side_effect

    # Mock find_element to return an element with outerHTML
    mock_el = MagicMock()
    mock_el.get_attribute.return_value = "<button id='btn'>Sign in</button>"
    mock_driver.find_element.return_value = mock_el

    result = heal.get_outer_html()

    assert isinstance(result, str)
    assert "<button" in result


def test_get_outer_html_empty_when_no_xpath_mapping(heal, mock_driver):
    """If xpath_mapping is empty, outer_html should be empty string."""
    def _execute_script_side_effect(script, *args):
        if "fetchJsonData" in script and "JSONOutput" in script:
            return "{}"
        return None

    mock_driver.execute_script.side_effect = _execute_script_side_effect
    mock_driver.find_element.side_effect = Exception("no element")

    result = heal.get_outer_html()
    assert result == ""


def test_get_outer_html_skips_non_dict_entries(heal, mock_driver):
    """Entries in xpath_mapping that are not dicts should be skipped gracefully."""
    xpath_mapping_json = json.dumps({
        "1": "not_a_dict",
        "2": {"xpath": "//button", "frameInformation": ""},
    })

    def _execute_script_side_effect(script, *args):
        if "fetchJsonData" in script and "JSONOutput" in script:
            return xpath_mapping_json
        return None

    mock_driver.execute_script.side_effect = _execute_script_side_effect

    mock_el = MagicMock()
    mock_el.get_attribute.return_value = "<button>OK</button>"
    mock_driver.find_element.return_value = mock_el

    result = heal.get_outer_html()
    # Only entry "2" (the dict one) should contribute
    assert "<button>" in result
    assert "not_a_dict" not in result


def test_get_outer_html_continues_on_find_element_error(heal, mock_driver):
    """If find_element raises, that xpath is skipped; method still returns."""
    xpath_mapping_json = json.dumps({
        "1": {"xpath": "//button[@stale='true']", "frameInformation": ""},
        "2": {"xpath": "//a[@id='link']", "frameInformation": ""},
    })

    def _execute_script_side_effect(script, *args):
        if "fetchJsonData" in script and "JSONOutput" in script:
            return xpath_mapping_json
        return None

    mock_driver.execute_script.side_effect = _execute_script_side_effect

    # First find_element raises, second returns an element
    mock_el = MagicMock()
    mock_el.get_attribute.return_value = "<a id='link'>click me</a>"
    mock_driver.find_element.side_effect = [Exception("stale"), mock_el]

    result = heal.get_outer_html()
    assert "<a id='link'>" in result


def test_get_outer_html_switches_frame_when_frame_info_present(heal, mock_driver):
    """When frameInformation is non-empty, driver.switch_to.default_content is called."""
    frame_info = [{"iframe": "//iframe[@id='f1']"}]
    xpath_mapping_json = json.dumps({
        "1": {
            "xpath": "//button",
            "frameInformation": frame_info,
        }
    })

    def _execute_script_side_effect(script, *args):
        if "fetchJsonData" in script and "JSONOutput" in script:
            return xpath_mapping_json
        return None

    mock_driver.execute_script.side_effect = _execute_script_side_effect
    mock_driver.find_element.return_value = MagicMock(
        get_attribute=lambda attr: "<button>OK</button>"
    )

    # Patch switch_to_frame_by_xpath so we don't need real iframe logic
    with patch("testmu_selenium._heal.switch_to_frame_by_xpath") as mock_switch:
        mock_switch.return_value = None
        result = heal.get_outer_html()

    mock_driver.switch_to.default_content.assert_called()
    mock_switch.assert_called_once()


# ---------------------------------------------------------------------------
# textual_query_v2 — success
# ---------------------------------------------------------------------------

@respx.mock
def test_textual_query_v2_posts_to_correct_endpoint(heal):
    fixture = _load_fixture("textual_query_success.json")
    route = respx.post(TEXTUAL_URL).mock(
        return_value=httpx.Response(200, json=fixture)
    )

    resp = heal.textual_query_v2(
        a11y_snapshot={"role": "button", "name": "Sign in"},
        dom_snapshot={"html": "<button>Sign in</button>"},
    )

    assert resp.status_code == 200
    assert route.called


@respx.mock
def test_textual_query_v2_payload_includes_a11y_and_dom(heal):
    route = respx.post(TEXTUAL_URL).mock(
        return_value=httpx.Response(200, json={"value": "//button"})
    )

    a11y = {"role": "button", "name": "Sign in"}
    dom = {"html": "<button>Sign in</button>"}
    heal.textual_query_v2(a11y_snapshot=a11y, dom_snapshot=dom)

    sent_body = json.loads(route.calls.last.request.content)
    assert sent_body["a11y_snapshot"] == a11y
    assert sent_body["dom_snapshot"] == dom
    assert sent_body["is_browser"] is True


@respx.mock
def test_textual_query_v2_includes_viewport_node_indices_when_provided(heal):
    route = respx.post(TEXTUAL_URL).mock(
        return_value=httpx.Response(200, json={"value": "//button"})
    )

    heal.textual_query_v2(
        a11y_snapshot={},
        dom_snapshot={},
        viewport_node_indices=[0, 3, 7],
    )

    sent_body = json.loads(route.calls.last.request.content)
    assert sent_body["viewport_node_indices"] == [0, 3, 7]


@respx.mock
def test_textual_query_v2_omits_viewport_indices_when_none(heal):
    route = respx.post(TEXTUAL_URL).mock(
        return_value=httpx.Response(200, json={"value": "//button"})
    )

    heal.textual_query_v2(a11y_snapshot={}, dom_snapshot={})

    sent_body = json.loads(route.calls.last.request.content)
    assert "viewport_node_indices" not in sent_body


@respx.mock
def test_textual_query_v2_is_mobile_flag_for_android(action, mock_driver):
    """is_mobile should be True when platformName is android."""
    from testmu_selenium._heal import Heal

    mock_driver.capabilities = {"platformName": "Android", "browserName": "chrome"}
    heal = Heal(action, mock_driver, username="u", accesskey="k")

    route = respx.post(TEXTUAL_URL).mock(
        return_value=httpx.Response(200, json={"value": "//button"})
    )

    heal.textual_query_v2(a11y_snapshot={}, dom_snapshot={})

    sent_body = json.loads(route.calls.last.request.content)
    assert sent_body["is_mobile"] is True
    assert sent_body["device_os"] == "android"


@respx.mock
def test_textual_query_v2_handles_miss_response(heal):
    """404 or error body response passes through — no exception raised."""
    fixture = _load_fixture("textual_query_miss.json")
    respx.post(TEXTUAL_URL).mock(
        return_value=httpx.Response(200, json=fixture)
    )

    resp = heal.textual_query_v2(a11y_snapshot={}, dom_snapshot={})
    assert resp.status_code == 200
    assert "error" in resp.json()


@respx.mock
def test_textual_query_v2_retries_on_5xx(heal, monkeypatch):
    """5xx triggers tenacity retry in make_http_request_with_retry."""
    monkeypatch.setattr(
        "testmu_selenium._helpers._http.make_http_request_with_retry.retry",
        type("FakeRetry", (), {"sleep": staticmethod(lambda _: None)})(),
    )

    route = respx.post(TEXTUAL_URL).mock(side_effect=[
        httpx.Response(503, json={"error": "unavailable"}),
        httpx.Response(200, json={"value": "//button"}),
    ])

    resp = heal.textual_query_v2(a11y_snapshot={}, dom_snapshot={})
    assert resp.status_code == 200
    assert route.call_count == 2
