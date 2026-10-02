"""textual_query() — two-step DOM read via POST /api/v1/analyzer, type "dom"."""
import json
from pathlib import Path

import httpx
import pytest
import respx
from selenium.common.exceptions import StaleElementReferenceException

from testmu_appium import _config
from testmu_appium._errors import (
    TestmuConfigError,
    UnknownStrategy,
    UnsupportedOnPlatform,
)
from testmu_appium._helpers.textual_query import textual_query
from testmu_appium._vars import _variable_store, clear_state, set_var

_XML = (Path(__file__).resolve().parent / "fixtures" / "page_source_gmail.xml").read_text()
_URL = "https://ai.example.test/v16-server/api/v1/analyzer"


class _FakeDriver:
    page_source = _XML

    def get_window_size(self):
        return {"width": 1080, "height": 2340}

    def get_screenshot_as_png(self):
        return b"\x89PNG-fake"


class _LocalElement:
    def __init__(self, attributes):
        self.attributes = attributes
        self.attribute_calls = []

    def get_attribute(self, name):
        self.attribute_calls.append(name)
        value = self.attributes.get(name)
        if isinstance(value, Exception):
            raise value
        return value


class _LocalDriver(_FakeDriver):
    def __init__(self, responses):
        self.responses = list(responses)
        self.find_calls = []

    def find_elements(self, by, value):
        self.find_calls.append((by, value))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


_SELECTORS = [
    {"strategy": "text", "selector": "Compose", "score": 90},
]


def _two_step(value="Compose", dom_index=1):
    """The identify response followed by the extract response."""
    return [
        httpx.Response(200, json={"extracted_value": "", "dom_index": dom_index}),
        httpx.Response(200, json={"extracted_value": value}),
    ]


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setitem(_config._config, "platform", "android")
    clear_state()
    yield
    clear_state()


@respx.mock
def test_returns_the_extracted_value_as_a_string():
    respx.post(_URL).mock(side_effect=_two_step())
    result = textual_query(_FakeDriver(), query="What does the FAB button say?")
    assert result == "Compose"


@respx.mock
def test_dom_abstention_falls_back_to_vision_with_the_same_query():
    route = respx.post(_URL).mock(side_effect=[
        httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
        httpx.Response(200, json={"extracted_value": "__not_visible__"}),
        httpx.Response(200, json={"extracted_value": "none"}),
    ])

    result = textual_query(
        _FakeDriver(),
        query="the text inside the left-hand drag-and-drop list",
        description="left list contents",
        return_type="string",
        expected_value="none",
    )

    assert result == "none"
    assert len(route.calls) == 3
    visual = json.loads(route.calls[2].request.content)
    assert visual["type"] == "visual"
    assert visual["query"] == "the text inside the left-hand drag-and-drop list"
    assert visual["expected_value"] == "none"
    assert visual["return_type"] == "string"
    assert visual["screenshot_b64"]


@respx.mock
def test_dom_and_visual_abstention_does_not_overwrite_the_output_variable():
    set_var("left_contents", "previous")
    respx.post(_URL).mock(side_effect=[
        httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
        httpx.Response(200, json={"extracted_value": "__not_visible__"}),
        httpx.Response(200, json={"extracted_value": "__not_visible__"}),
    ])

    with pytest.raises(RuntimeError, match="current screenshot"):
        textual_query(
            _FakeDriver(), query="left list contents", output_variable="left_contents"
        )

    assert _variable_store["left_contents"] == "previous"


@respx.mock
def test_identify_carries_the_dom_type_and_the_flat_perception_entries():
    route = respx.post(_URL).mock(side_effect=_two_step())
    textual_query(_FakeDriver(), query="find the compose button")
    payload = json.loads(route.calls[0].request.content)
    assert payload["type"] == "dom"
    assert payload["query"] == "find the compose button"
    assert payload["full_dom_list"]
    assert set(payload["full_dom_list"][0]) == {"index", "role", "name", "states", "position_hint"}
    assert "screenshot_b64" not in payload


@respx.mock
def test_extract_carries_the_snapshot_of_the_identified_element():
    route = respx.post(_URL).mock(side_effect=_two_step(dom_index=2))
    textual_query(_FakeDriver(), query="q")
    payload = json.loads(route.calls[1].request.content)
    assert payload["type"] == "dom"
    assert payload["query"] == "q"
    assert set(payload["element_snapshot"]) == {
        "tag_name", "text_content", "attributes", "styles", "states",
    }
    assert "full_dom_list" not in payload


@respx.mock
def test_an_identify_response_without_a_dom_index_raises():
    respx.post(_URL).mock(
        return_value=httpx.Response(200, json={"extracted_value": "", "dom_index": None})
    )
    with pytest.raises(RuntimeError) as exc:
        textual_query(_FakeDriver(), query="q")
    assert "dom_index" in str(exc.value)


@respx.mock
def test_a_dom_index_absent_from_the_perception_raises():
    """The answer must name an element this capture actually saw."""
    respx.post(_URL).mock(
        return_value=httpx.Response(200, json={"extracted_value": "", "dom_index": 9999})
    )
    with pytest.raises(RuntimeError) as exc:
        textual_query(_FakeDriver(), query="q")
    assert "9999" in str(exc.value)


@respx.mock
def test_output_variable_is_written():
    respx.post(_URL).mock(side_effect=_two_step())
    result = textual_query(_FakeDriver(), query="q", output_variable="btn_label")
    assert _variable_store["btn_label"] == result == "Compose"


@respx.mock
def test_query_resolves_variable_tokens_on_both_calls():
    set_var("target", "the send button")
    route = respx.post(_URL).mock(side_effect=_two_step())
    textual_query(_FakeDriver(), query="find {{target}}")
    for call in route.calls:
        assert json.loads(call.request.content)["query"] == "find the send button"


def test_smart_disabled_raises_config_error(monkeypatch):
    monkeypatch.setattr(_config, "smart", False)
    monkeypatch.setitem(
        textual_query.__globals__,
        "_resolve_query",
        lambda _: pytest.fail("selectorless smart-off query must not be resolved"),
    )
    with pytest.raises(TestmuConfigError) as exc:
        textual_query(_FakeDriver(), query="{{global/legacy_query}}")
    assert str(exc.value) == (
        "textual_query requires TESTMU_SMART=1 (AI-backed read, no local fallback)"
    )


class TestLocalRead:
    @respx.mock
    def test_unique_selector_reads_locally_with_smart_disabled(self, monkeypatch):
        monkeypatch.setattr(_config, "smart", False)
        element = _LocalElement({"text": "42"})
        driver = _LocalDriver([[element]])

        result = textual_query(
            driver,
            query="the item count",
            selectors=_SELECTORS,
            selected_attribute_name="text",
            return_type="number",
            output_variable="item_count",
        )

        assert result == 42.0
        assert _variable_store["item_count"] == 42.0
        assert element.attribute_calls == ["text"]
        assert not respx.calls

    @pytest.mark.parametrize(
        "field,appium_attribute",
        [
            ("text", "text"),
            ("content_desc", "content-desc"),
            ("hint", "hint"),
            ("resource_id", "resource-id"),
        ],
    )
    @respx.mock
    def test_android_field_mapping(self, field, appium_attribute):
        element = _LocalElement({appium_attribute: "local value"})
        assert textual_query(
            _LocalDriver([[element]]),
            query="q",
            selectors=_SELECTORS,
            selected_attribute_name=field,
        ) == "local value"
        assert element.attribute_calls == [appium_attribute]
        assert not respx.calls

    @pytest.mark.parametrize(
        "field,appium_attribute",
        [("text", "value"), ("content_desc", "name")],
    )
    @respx.mock
    def test_ios_field_mapping(self, monkeypatch, field, appium_attribute):
        monkeypatch.setitem(_config._config, "platform", "ios")
        element = _LocalElement({appium_attribute: "local value"})
        ios_selector = [{"strategy": "text", "selector": "Label", "score": 80}]
        assert textual_query(
            _LocalDriver([[element]]),
            query="q",
            selectors=ios_selector,
            selected_attribute_name=field,
        ) == "local value"
        assert element.attribute_calls == [appium_attribute]
        assert not respx.calls

    @respx.mock
    def test_ranked_lookup_skips_an_ambiguous_strategy(self):
        element = _LocalElement({"text": "unique"})
        selectors = [
            {"strategy": "text", "selector": "lower", "score": 10},
            {"strategy": "accessibility_id", "selector": "higher", "score": 90},
        ]
        driver = _LocalDriver([[object(), object()], [element]])

        assert textual_query(
            driver,
            query="q",
            selectors=selectors,
            selected_attribute_name="text",
        ) == "unique"
        assert driver.find_calls[0][1] == "higher"
        assert "lower" in driver.find_calls[1][1]

    @respx.mock
    def test_stale_local_attribute_is_refound_and_retried_once(self):
        stale = _LocalElement({"text": StaleElementReferenceException("gone")})
        fresh = _LocalElement({"text": "fresh"})
        driver = _LocalDriver([[stale], [fresh]])

        assert textual_query(
            driver,
            query="q",
            selectors=_SELECTORS,
            selected_attribute_name="text",
        ) == "fresh"
        assert len(driver.find_calls) == 2
        assert not respx.calls

    @pytest.mark.parametrize("local_value", [None, ""])
    @respx.mock
    def test_empty_local_value_falls_through_to_the_legacy_analyzer(self, local_value):
        route = respx.post(_URL).mock(side_effect=_two_step(value="from AI"))
        driver = _LocalDriver([[_LocalElement({"text": local_value})]])

        assert textual_query(
            driver,
            query="q",
            selectors=_SELECTORS,
            selected_attribute_name="text",
        ) == "from AI"
        assert len(route.calls) == 2

    @pytest.mark.parametrize("failure_site", ["lookup", "attribute"])
    @respx.mock
    def test_local_appium_error_falls_through_to_the_legacy_analyzer(
        self, failure_site
    ):
        route = respx.post(_URL).mock(side_effect=_two_step(value="from AI"))
        if failure_site == "lookup":
            driver = _LocalDriver([RuntimeError("lookup failed")])
        else:
            element = _LocalElement({"text": RuntimeError("read failed")})
            driver = _LocalDriver([[element]])

        assert textual_query(
            driver,
            query="q",
            selectors=_SELECTORS,
            selected_attribute_name="text",
        ) == "from AI"
        assert len(route.calls) == 2

    @respx.mock
    def test_unsupported_ios_field_uses_the_legacy_analyzer(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")
        route = respx.post(_URL).mock(side_effect=_two_step(value="from AI"))
        driver = _LocalDriver([])
        driver.page_source = (
            '<AppiumAUT><XCUIElementTypeApplication type="XCUIElementTypeApplication" '
            'name="Demo" enabled="true" visible="true" accessible="false" '
            'x="0" y="0" width="414" height="896">'
            '<XCUIElementTypeButton type="XCUIElementTypeButton" name="Label" '
            'label="Label" value="Label" enabled="true" visible="true" '
            'accessible="true" x="20" y="20" width="100" height="40"/>'
            "</XCUIElementTypeApplication></AppiumAUT>"
        )

        assert textual_query(
            driver,
            query="q",
            selectors=[{"strategy": "text", "selector": "Label", "score": 80}],
            selected_attribute_name="hint",
        ) == "from AI"
        assert len(route.calls) == 2

    @respx.mock
    def test_unknown_selector_strategy_fails_loudly(self):
        with pytest.raises(UnknownStrategy, match="producer_v2"):
            textual_query(
                _LocalDriver([]),
                query="q",
                selectors=[
                    {"strategy": "producer_v2", "selector": "x", "score": 100}
                ],
                selected_attribute_name="text",
            )
        assert not respx.calls

    @respx.mock
    def test_unknown_lower_ranked_strategy_fails_before_a_local_read(self):
        selectors = [
            {"strategy": "text", "selector": "Compose", "score": 100},
            {"strategy": "producer_v2", "selector": "x", "score": 10},
        ]
        with pytest.raises(UnknownStrategy, match="producer_v2"):
            textual_query(
                _LocalDriver([[_LocalElement({"text": "local"})]]),
                query="q",
                selectors=selectors,
                selected_attribute_name="text",
            )
        assert not respx.calls

    @respx.mock
    def test_unknown_platform_fails_loudly(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "windows_phone")
        with pytest.raises(UnsupportedOnPlatform, match="windows_phone"):
            textual_query(
                _LocalDriver([]),
                query="q",
                selectors=_SELECTORS,
                selected_attribute_name="text",
            )
        assert not respx.calls

    @pytest.mark.parametrize(
        "extra",
        [
            {"selectors": _SELECTORS},
            {"selected_attribute_name": "text"},
        ],
    )
    @respx.mock
    def test_partial_local_metadata_keeps_the_legacy_path(self, extra):
        route = respx.post(_URL).mock(side_effect=_two_step(value="from AI"))
        assert textual_query(_FakeDriver(), query="q", **extra) == "from AI"
        assert len(route.calls) == 2


@respx.mock
def test_non_200_on_identify_raises_naming_the_endpoint():
    respx.post(_URL).mock(return_value=httpx.Response(500, text="boom"))
    with pytest.raises(RuntimeError) as exc:
        textual_query(_FakeDriver(), query="q")
    assert "textual_query" in str(exc.value)


@respx.mock
def test_non_200_on_extract_raises_naming_the_endpoint():
    respx.post(_URL).mock(side_effect=[
        httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
        httpx.Response(500, text="boom"),
    ])
    with pytest.raises(RuntimeError) as exc:
        textual_query(_FakeDriver(), query="q")
    assert "textual_query" in str(exc.value)
    assert len(respx.calls) == 2, "transport failures must not fall back to vision"


@respx.mock
def test_malformed_body_missing_extracted_value_raises():
    respx.post(_URL).mock(side_effect=[
        httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
        httpx.Response(200, json={"unexpected": "shape"}),
    ])
    with pytest.raises(RuntimeError) as exc:
        textual_query(_FakeDriver(), query="q")
    assert "extracted_value" in str(exc.value)


@respx.mock
def test_non_json_response_body_raises():
    respx.post(_URL).mock(return_value=httpx.Response(200, text="<html>gateway</html>"))
    with pytest.raises(RuntimeError):
        textual_query(_FakeDriver(), query="q")


class TestDescriptionIsReal:
    """Same contract as vision_query: the label is logged, and defaults to the
    resolved query so no read is anonymous."""

    @respx.mock
    def test_an_explicit_description_reaches_the_log(self, caplog):
        import logging

        caplog.set_level(logging.INFO, logger="testmu_appium")
        respx.post(_URL).mock(side_effect=_two_step(value="3"))
        textual_query(_FakeDriver(), query="the badge count", description="cart badge")
        assert "cart badge" in caplog.text

    @respx.mock
    def test_an_empty_description_defaults_to_the_resolved_query(self, caplog):
        import logging

        caplog.set_level(logging.INFO, logger="testmu_appium")
        set_var("item", "socks")
        respx.post(_URL).mock(side_effect=_two_step(value="yes"))
        textual_query(_FakeDriver(), query="is {{item}} in the cart")
        assert "is socks in the cart" in caplog.text

    @respx.mock
    def test_the_description_does_not_leak_onto_the_request(self):
        route = respx.post(_URL).mock(side_effect=_two_step())
        textual_query(_FakeDriver(), query="q", description="a label")
        for call in route.calls:
            assert "description" not in json.loads(call.request.content)
