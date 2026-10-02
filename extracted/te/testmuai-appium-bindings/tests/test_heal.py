"""Autoheal client: typed outcomes, descriptor re-find, cache semantics."""
import json
from pathlib import Path

import httpx
import pytest
import respx

from testmu_appium import _action_web, _config, _heal
from testmu_appium._heal import (
    HealDisabled, HealHit, HealNoMatch, HealProtocolError, HealUnavailable, HealUnresolved,
    WebHealHit, autoheal, autoheal_web, cache_key, read_cache, write_cache,
)
from testmu_appium.perception import parse_tree
from testmu_appium._step import step

_XML = (Path(__file__).resolve().parent / "fixtures" / "page_source_gmail.xml").read_text()
_URL = "https://ai.example.test/v16-server/api/v1/autoheal"
_COMPOSE_INDEX = next(
    entry["index"] for entry in parse_tree(_XML, 1080, 2340)
    if entry["resource_id"] == "com.google.android.gm:id/compose"
)


class _FakeElement:
    def __init__(self, tag="el"):
        self.tag = tag


class _FakeDriver:
    """Records find_elements calls and replays a scripted result queue."""

    page_source = _XML

    def __init__(self, found=None):
        # found: list of results, one per find_elements call
        self._found = list(found or [])
        self.find_calls = []

    def get_window_size(self):
        return {"width": 1080, "height": 2340}

    def get_screenshot_as_png(self):
        return b"\x89PNG"

    def find_elements(self, by, value):
        self.find_calls.append((by, value))
        return self._found.pop(0) if self._found else []


@pytest.fixture(autouse=True)
def _ai_host(monkeypatch):
    monkeypatch.setenv("TESTMU_AI_API_HOST", "https://ai.example.test/v16-server")
    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", True)
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "ai_api_host", "https://ai.example.test/v16-server")


def _run(driver, action_type="click"):
    with step("Tap Compose"):
        return autoheal(driver, "PRIMARY: Compose button", action_type)


def _web_surface():
    element = {
        "tag": "BUTTON", "label": "Continue", "css": "#continue", "path": "",
        "dom_path": [{"kind": "element", "nodes": [0, 1]}],
        "interactive": True, "editable": False, "disabled": False, "states": [],
        "x": 10, "y": 20, "w": 100, "h": 40,
    }
    page = {
        "dpr": 3, "scale": 1, "offsetLeft": 0, "offsetTop": 0,
        "visualWidth": 360, "visualHeight": 800,
    }
    return _action_web.Surface(
        channel=object(), elements=[element], all_elements=[element],
        page=page, origin=(0, 0), twins={},
    )


@respx.mock
def test_hit_resolves_dom_index_to_exactly_one_live_element():
    element = _FakeElement()
    driver = _FakeDriver(found=[[element]])
    respx.post(_URL).mock(
        return_value=httpx.Response(
            200, json={"dom_index": _COMPOSE_INDEX, "reasoning": "the FAB"})
    )
    outcome = _run(driver)
    assert isinstance(outcome, HealHit)
    assert outcome.element is element
    assert outcome.dom_index == _COMPOSE_INDEX
    assert outcome.reasoning == "the FAB"
    assert outcome.source == "v16-autoheal"


@respx.mock
def test_request_body_carries_the_wire_entries_and_screenshot():
    driver = _FakeDriver(found=[[_FakeElement()]])
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={"dom_index": 1}))
    _run(driver)
    body = json.loads(route.calls[0].request.content)
    assert body["action_instruction"] == "PRIMARY: Compose button"
    assert body["action_type"] == "click"
    assert body["screenshot_b64"]
    assert body["full_dom_list"][0]["index"] == 1
    assert set(body["full_dom_list"][0]) == {
        "index", "role", "name", "states", "position_hint"
    }


@respx.mock
def test_web_heal_uses_the_same_wire_tree_and_keeps_dom_identity_private():
    driver = _FakeDriver()
    route = respx.post(_URL).mock(
        return_value=httpx.Response(200, json={"dom_index": 1})
    )
    with step("Continue"):
        outcome = autoheal_web(
            driver, _web_surface(), "Continue button", "click"
        )
    assert isinstance(outcome, WebHealHit)
    body = json.loads(route.calls[0].request.content)
    assert body["surface"] == "web"
    assert set(body["full_dom_list"][0]) == {
        "index", "role", "name", "states", "position_hint"
    }
    assert "dom_path" not in body["full_dom_list"][0]
    assert outcome.descriptor["dom_path"]


@respx.mock
def test_the_healed_lookup_is_compiled_from_the_retained_descriptor():
    """The Compose row's lookup comes from its retained id and text."""
    driver = _FakeDriver(found=[[_FakeElement()]])
    respx.post(_URL).mock(
        return_value=httpx.Response(200, json={"dom_index": _COMPOSE_INDEX}))
    _run(driver)
    by, value = driver.find_calls[0]
    assert "com.google.android.gm:id/compose" in value
    assert "Compose" in value


@respx.mock
def test_zero_live_matches_is_unresolved_not_authoritative():
    """A 200 the binding could not turn into one live element is NOT a no-match. The
    server never said the element is gone; the local lookup did, and a screen that
    moved between the snapshot and the lookup explains that just as well."""
    driver = _FakeDriver(found=[[]])
    respx.post(_URL).mock(
        return_value=httpx.Response(200, json={"dom_index": _COMPOSE_INDEX}))
    outcome = _run(driver)
    assert isinstance(outcome, HealUnresolved)
    assert not isinstance(outcome, HealNoMatch)
    assert outcome.authoritative is False
    assert "0" in outcome.reason or "zero" in outcome.reason.lower()


@respx.mock
def test_many_live_matches_is_unresolved_not_authoritative():
    driver = _FakeDriver(found=[[_FakeElement("a"), _FakeElement("b")]])
    respx.post(_URL).mock(
        return_value=httpx.Response(200, json={"dom_index": _COMPOSE_INDEX}))
    outcome = _run(driver)
    assert isinstance(outcome, HealUnresolved)
    assert outcome.authoritative is False


@respx.mock
def test_404_is_the_authoritative_no_match():
    driver = _FakeDriver()
    respx.post(_URL).mock(return_value=httpx.Response(404, json={"detail": "no_match"}))
    outcome = _run(driver)
    assert isinstance(outcome, HealNoMatch)
    assert outcome.authoritative is True


@respx.mock
def test_500_is_unavailable_not_authoritative():
    driver = _FakeDriver()
    respx.post(_URL).mock(return_value=httpx.Response(500, text="boom"))
    outcome = _run(driver)
    assert isinstance(outcome, HealUnavailable)


def test_explicit_heal_off_has_its_own_outcome_but_smart_off_does_not(monkeypatch):
    """Only the dedicated heal flag permits deterministic recorded grounding."""
    with step("Tap Compose"):
        monkeypatch.setattr(_config, "heal", False)
        disabled = autoheal(None, "PRIMARY: Compose button", "click")
    assert isinstance(disabled, HealDisabled)
    assert not isinstance(disabled, HealUnavailable)
    assert disabled.reason == "autoheal is off (TESTMU_HEAL)"

    with step("Tap Compose"):
        monkeypatch.setattr(_config, "heal", True)
        monkeypatch.setattr(_config, "smart", False)
        unavailable = autoheal(None, "PRIMARY: Compose button", "click")
    assert isinstance(unavailable, HealUnavailable)
    assert "TESTMU_SMART" in unavailable.cause


def test_transport_error_is_unavailable(monkeypatch):
    driver = _FakeDriver()

    def _boom(*a, **kw):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(_heal, "request_with_retry", _boom)
    outcome = _run(driver)
    assert isinstance(outcome, HealUnavailable)
    assert "connection refused" in outcome.cause


@respx.mock
def test_200_without_dom_index_is_a_protocol_error():
    driver = _FakeDriver()
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"reasoning": "hm"}))
    assert isinstance(_run(driver), HealProtocolError)


@respx.mock
def test_non_json_body_is_a_protocol_error():
    driver = _FakeDriver()
    respx.post(_URL).mock(return_value=httpx.Response(200, text="<html>gateway</html>"))
    assert isinstance(_run(driver), HealProtocolError)


@respx.mock
def test_dom_index_outside_the_captured_list_is_a_protocol_error():
    driver = _FakeDriver()
    respx.post(_URL).mock(return_value=httpx.Response(200, json={"dom_index": 999}))
    assert isinstance(_run(driver), HealProtocolError)


@respx.mock
def test_unmappable_action_type_never_reaches_the_server():
    driver = _FakeDriver()
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={"dom_index": 1}))
    with step("s"):
        outcome = autoheal(driver, "desc", "keyevent")
    assert isinstance(outcome, HealUnavailable)
    assert not route.called


def test_smart_disabled_skips_the_call(monkeypatch):
    monkeypatch.setattr(_config, "smart", False)
    outcome = _run(_FakeDriver())
    assert isinstance(outcome, HealUnavailable)


def test_heal_disabled_skips_the_call_with_smart_still_on(monkeypatch):
    """Two different questions, and one flag used to answer both.

    `smart` asks whether this test may make AI calls at all. `heal` asks whether
    a find that FAILED may be silently recovered. An authoring run wants the
    second off — a healed locator records selectors that do not describe what was
    touched — while still needing the first on, because a vision-grounded action
    is resolved by an AI call that IS the action, not a recovery from one.
    """
    monkeypatch.setattr(_config, "smart", True)
    monkeypatch.setattr(_config, "heal", False)
    outcome = _run(_FakeDriver())
    assert isinstance(outcome, HealDisabled)
    assert not isinstance(outcome, HealUnavailable)


def test_heal_is_on_unless_it_is_turned_off(monkeypatch):
    """Every existing caller configures no `heal` at all, and must keep healing."""
    monkeypatch.setattr(_config, "smart", True)
    assert _config.heal_enabled() is True


@respx.mock
def test_outside_a_step_heal_does_not_run():
    """Heal is a step-scoped facility — its cache and telemetry live on the step."""
    driver = _FakeDriver()
    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={"dom_index": 1}))
    outcome = autoheal(driver, "desc", "click")
    assert isinstance(outcome, HealUnavailable)
    assert not route.called


@respx.mock
def test_empty_perception_skips_the_call():
    class _Blank(_FakeDriver):
        page_source = "<hierarchy rotation='0'/>"

    route = respx.post(_URL).mock(return_value=httpx.Response(200, json={"dom_index": 1}))
    outcome = _run(_Blank())
    assert isinstance(outcome, HealUnavailable)
    assert not route.called


class TestStaleTextDegradation:
    """A compiled lookup ANDs the element's text into its identity, and on a
    value-bearing control the text IS the value: a rating slider reads "0.0", then
    "Any rating", then "2+ stars". The server round-trip sits between the parse the
    descriptor came from and the re-find, so the text can move in between — and the
    element is still there, under the same handle.

    Zero matches is the signal that the narrowing clause went stale, so the lookup
    is retried without it. Several matches is the opposite signal and keeps its
    existing route: that is what the retained centre settles.
    """

    #: The fixture's Compose row carries both a resource-id and text, so it compiles
    #: to the compound; dropping the text leaves the resource-id standing alone.
    COMPOUND_INDEX = _COMPOSE_INDEX
    #: resource-id, no text — the text clause was never in the lookup to drop.
    NO_TEXT_INDEX = next(
        entry["index"] for entry in parse_tree(_XML, 1080, 2340)
        if entry["resource_id"] == "com.google.android.gm:id/search"
    )
    #: content-desc + resource-id, no text — compiles the same either way.
    DESC_INDEX = next(
        entry["index"] for entry in parse_tree(_XML, 1080, 2340)
        if entry["resource_id"] == "com.google.android.gm:id/nav"
    )
    COMPOSE_CENTRE = next(
        entry["center"] for entry in parse_tree(_XML, 1080, 2340)
        if entry["index"] == _COMPOSE_INDEX
    )

    class _Positioned:
        """A live element the centre disambiguator can read."""

        def __init__(self, tag, centre, size=(200, 200)):
            self.tag = tag
            self.rect = {"x": centre[0] - size[0] // 2, "y": centre[1] - size[1] // 2,
                         "width": size[0], "height": size[1]}

    def _serve(self, dom_index):
        respx.post(_URL).mock(
            return_value=httpx.Response(200, json={"dom_index": dom_index}))

    @respx.mock
    def test_a_compound_matching_nothing_is_retried_without_its_text(self):
        element = _FakeElement()
        driver = _FakeDriver(found=[[], [element]])
        self._serve(self.COMPOUND_INDEX)
        outcome = _run(driver)
        assert isinstance(outcome, HealHit), outcome
        assert outcome.element is element
        assert len(driver.find_calls) == 2
        first, second = (call[1] for call in driver.find_calls)
        assert ".text(" in first
        assert ".text(" not in second
        assert "com.google.android.gm:id/compose" in second

    @respx.mock
    def test_the_hit_reports_the_lookup_that_actually_found_it(self):
        """The retained `value` is evidence; naming the failed compound would lie."""
        driver = _FakeDriver(found=[[], [_FakeElement()]])
        self._serve(self.COMPOUND_INDEX)
        outcome = _run(driver)
        assert isinstance(outcome, HealHit)
        assert ".text(" not in outcome.value

    @respx.mock
    def test_the_relaxed_lookup_still_settles_several_matches_by_centre(self):
        """Dropping the text loosens identity, which is what the centre is for."""
        wanted = self._Positioned("wanted", self.COMPOSE_CENTRE)
        elsewhere = self._Positioned("elsewhere", (40, 40))
        driver = _FakeDriver(found=[[], [elsewhere, wanted]])
        self._serve(self.COMPOUND_INDEX)
        outcome = _run(driver)
        assert isinstance(outcome, HealHit), outcome
        assert outcome.element is wanted

    @respx.mock
    def test_a_relaxed_lookup_that_also_matches_nothing_is_unresolved(self):
        driver = _FakeDriver(found=[[], []])
        self._serve(self.COMPOUND_INDEX)
        outcome = _run(driver)
        assert isinstance(outcome, HealUnresolved)
        assert not isinstance(outcome, HealNoMatch)
        assert outcome.authoritative is False
        # The message names what was tried LAST, so the log matches the last query.
        assert ".text(" not in outcome.reason

    @respx.mock
    def test_several_matches_first_time_are_never_retried(self):
        """Ambiguity is not staleness — loosening it further is the wrong direction."""
        driver = _FakeDriver(found=[[_FakeElement("a"), _FakeElement("b")]])
        self._serve(self.COMPOUND_INDEX)
        assert isinstance(_run(driver), HealUnresolved)
        assert len(driver.find_calls) == 1

    @respx.mock
    def test_a_compound_that_resolves_first_time_is_not_retried(self):
        driver = _FakeDriver(found=[[_FakeElement()]])
        self._serve(self.COMPOUND_INDEX)
        assert isinstance(_run(driver), HealHit)
        assert len(driver.find_calls) == 1

    @pytest.mark.parametrize("index_attr", ["NO_TEXT_INDEX", "DESC_INDEX"])
    @respx.mock
    def test_a_lookup_with_no_text_clause_to_drop_is_not_retried(self, index_attr):
        """Recompiling these yields a byte-identical query, so a retry would spend a
        round-trip against the device to be told the same thing."""
        driver = _FakeDriver(found=[[]])
        self._serve(getattr(self, index_attr))
        assert isinstance(_run(driver), HealUnresolved)
        assert len(driver.find_calls) == 1


class TestRepeatedResourceIdRows:
    """RecyclerView rows share one resource-id and carry no text of their own, so the
    compiled descriptor lookup matches EVERY row. The descriptor carries the bounds
    and centre naming which row was meant, from the same parse the dom_index refers
    to.
    """

    XML = (Path(__file__).resolve().parent / "fixtures" / "page_source_recycler.xml").read_text()
    #: dom_index → (row label, recorded centre) in the fixture's parse order.
    ROWS = {
        entry["index"]: (entry["name"].split(" ·", 1)[0], entry["center"])
        for entry in parse_tree(XML, 1080, 2340)
        if entry["resource_id"].endswith("order_row")
    }
    ORDER_1003_INDEX = next(
        index for index, (label, _center) in ROWS.items()
        if label == "Order #1003"
    )

    class _Row:
        """A live row, positioned like its fixture counterpart."""

        def __init__(self, label, top):
            self.label = label
            self.rect = {"x": 0, "y": top, "width": 1080, "height": 300}

    class _RowDriver(_FakeDriver):
        def __init__(self, xml, rows):
            super().__init__()
            self.page_source = xml
            self.rows = rows

        def find_elements(self, by, value):
            self.find_calls.append((by, value))
            return list(self.rows)

    def _driver(self):
        rows = [self._Row("Order #1001", 300), self._Row("Order #1002", 600),
                self._Row("Order #1003", 900), self._Row("Order #1004", 1200)]
        return self._RowDriver(self.XML, rows)

    def test_the_lookup_really_is_ambiguous(self):
        """Guards the premise: without disambiguation this is four matches."""
        from testmu_appium._helpers._strategy import compile_descriptor
        from testmu_appium._helpers._tree import parse_tree

        rows = [e for e in parse_tree(self.XML, 1080, 2340)
                if e["resource_id"].endswith("order_row")]
        assert len(rows) == 4
        compiled = {compile_descriptor(row, "android") for row in rows}
        assert len(compiled) == 1, "every row compiles to the same lookup"

    @pytest.mark.parametrize("dom_index", sorted(ROWS))
    @respx.mock
    def test_each_row_heals_to_itself(self, dom_index):
        driver = self._driver()
        respx.post(_URL).mock(
            return_value=httpx.Response(200, json={"dom_index": dom_index})
        )
        outcome = _run(driver)
        assert isinstance(outcome, HealHit), outcome
        assert outcome.element.label == self.ROWS[dom_index][0]

    @respx.mock
    def test_a_recorded_centre_matching_nothing_is_still_unresolved(self):
        """Disambiguation resolves ambiguity; it never invents a target."""
        driver = self._driver()
        driver.rows = [self._Row("Order #9999", 1800)]  # nowhere near any recorded row
        driver.rows = driver.rows * 2                   # ...and still ambiguous
        respx.post(_URL).mock(return_value=httpx.Response(
            200, json={"dom_index": self.ORDER_1003_INDEX}))
        assert isinstance(_run(driver), HealUnresolved)

    @respx.mock
    def test_overlapping_rows_that_position_cannot_separate_are_unresolved(self):
        driver = self._driver()
        driver.rows = [self._Row("a", 900), self._Row("b", 900)]
        respx.post(_URL).mock(return_value=httpx.Response(
            200, json={"dom_index": self.ORDER_1003_INDEX}))
        assert isinstance(_run(driver), HealUnresolved)

    @respx.mock
    def test_an_unambiguous_lookup_never_consults_the_centre(self):
        driver = self._driver()
        driver.rows = [self._Row("Order #1003", 1800)]  # single match, wrong position
        respx.post(_URL).mock(return_value=httpx.Response(
            200, json={"dom_index": self.ORDER_1003_INDEX}))
        outcome = _run(driver)
        assert isinstance(outcome, HealHit)
        assert outcome.element.label == "Order #1003"

    @respx.mock
    def test_rows_whose_geometry_cannot_be_read_are_skipped(self):
        class _Unreadable:
            @property
            def rect(self):
                raise RuntimeError("stale")

        driver = self._driver()
        driver.rows = [_Unreadable(), self._Row("Order #1003", 900)]
        respx.post(_URL).mock(return_value=httpx.Response(
            200, json={"dom_index": self.ORDER_1003_INDEX}))
        outcome = _run(driver)
        assert isinstance(outcome, HealHit)
        assert outcome.element.label == "Order #1003"


class TestHealTimeout:
    """httpx takes seconds; the config carries milliseconds."""

    @pytest.mark.parametrize(
        "configured_ms,expected_s",
        [
            (60000, 60),
            (5000, 5),
            (1500, 1),
            # Sub-second values integer-divide to zero and are then floored at one
            # second, rather than falling back to the 60s default.
            (999, 1),
            (500, 1),
            (1, 1),
            # Absent / non-positive falls back to the default.
            (0, 60),
            (-1, 60),
        ],
    )
    def test_timeout_is_seconds_floored_at_one(self, monkeypatch, configured_ms, expected_s):
        monkeypatch.setitem(_config._config, "heal_timeout_ms", configured_ms)
        assert _heal._heal_timeout_s() == expected_s

    @pytest.mark.parametrize(
        "configured_ms,budget_s,expected_s",
        [
            # The caller's remaining per-action budget is the tighter ceiling.
            (60000, 2.5, 2.5),
            (60000, 0.4, 0.4),
            (60000, 0.0, 0.0),
            # ...and the configured timeout is still a ceiling of its own.
            (5000, 30.0, 5),
            (0, 3.0, 3),
        ],
    )
    def test_the_caller_budget_caps_the_configured_timeout(
        self, monkeypatch, configured_ms, budget_s, expected_s
    ):
        """The remaining action budget is an exact ceiling, including below one
        second; it must never be rounded up into time the action no longer owns."""
        monkeypatch.setitem(_config._config, "heal_timeout_ms", configured_ms)
        assert _heal._heal_timeout_s(budget_s) == expected_s

    @respx.mock
    def test_the_budget_reaches_the_request(self, monkeypatch):
        monkeypatch.setitem(_config._config, "heal_timeout_ms", 60000)
        seen = {}

        def _capture(*args, **kwargs):
            seen["timeout"] = kwargs["timeout"]
            seen["total_timeout_s"] = kwargs["total_timeout_s"]
            return httpx.Response(200, json={"dom_index": _COMPOSE_INDEX})

        monkeypatch.setattr(_heal, "request_with_retry", _capture)
        with step("Tap Compose"):
            autoheal(_FakeDriver(found=[[_FakeElement()]]), "Compose", "click", budget_s=3.0)
        assert 0 < seen["timeout"] <= 3
        assert 0 < seen["total_timeout_s"] <= 3

    def test_perception_time_is_charged_to_the_request_budget(self, monkeypatch):
        monkeypatch.setitem(_config._config, "heal_timeout_ms", 60000)
        ticks = iter([10.0, 10.75])
        monkeypatch.setattr(_heal.time, "monotonic", lambda: next(ticks))
        seen = {}

        def _capture(*args, **kwargs):
            seen.update(kwargs)
            return httpx.Response(200, json={"dom_index": _COMPOSE_INDEX})

        monkeypatch.setattr(_heal, "request_with_retry", _capture)
        with step("Tap Compose"):
            autoheal(
                _FakeDriver(found=[[_FakeElement()]]),
                "Compose", "click", budget_s=1.0,
            )
        assert seen["timeout"] == pytest.approx(0.25)
        assert seen["total_timeout_s"] == pytest.approx(0.25)

    @respx.mock
    def test_a_sub_second_budget_reaches_the_request(self, monkeypatch):
        monkeypatch.setitem(_config._config, "heal_timeout_ms", 500)
        seen = {}

        def _capture(*args, **kwargs):
            seen["timeout"] = kwargs["timeout"]
            seen["total_timeout_s"] = kwargs["total_timeout_s"]
            return httpx.Response(200, json={"dom_index": _COMPOSE_INDEX})

        monkeypatch.setattr(_heal, "request_with_retry", _capture)
        _run(_FakeDriver(found=[[_FakeElement()]]))
        assert seen["timeout"] == 1
        assert seen["total_timeout_s"] is None


class TestCacheSemantics:
    """Only an authoritative miss is cached; transport trouble is retried next time."""

    SELECTORS = [{"strategy": "view_id", "selector": "com.app:id/x", "score": 90}]

    def test_cache_key_is_stable_over_the_selector_set(self):
        other = [{"strategy": "view_id", "selector": "com.app:id/x", "score": 90}]
        assert cache_key(self.SELECTORS) == cache_key(other)

    def test_cache_key_distinguishes_different_selector_sets(self):
        other = [{"strategy": "view_id", "selector": "com.app:id/y", "score": 90}]
        assert cache_key(self.SELECTORS) != cache_key(other)

    def test_cache_is_per_step(self):
        key = cache_key(self.SELECTORS)
        with step("a"):
            write_cache(key, ("id", "x"))
            assert read_cache(key) == ("id", "x")
        with step("b"):
            assert read_cache(key) is _heal.CACHE_ABSENT

    def test_negative_sentinel_is_distinguishable_from_absent(self):
        key = cache_key(self.SELECTORS)
        with step("a"):
            assert read_cache(key) is _heal.CACHE_ABSENT
            write_cache(key, None)
            assert read_cache(key) is None

    def test_writes_outside_a_step_are_dropped(self):
        key = cache_key(self.SELECTORS)
        write_cache(key, ("id", "x"))
        assert read_cache(key) is _heal.CACHE_ABSENT

    @respx.mock
    def test_authoritative_miss_is_cached_by_the_caller_contract(self):
        """autoheal itself never writes the cache — the engine owns that decision,
        because only it knows which selector set the attempt belonged to."""
        driver = _FakeDriver()
        respx.post(_URL).mock(return_value=httpx.Response(404, json={"detail": "no_match"}))
        with step("s"):
            outcome = autoheal(driver, "desc", "click")
            assert isinstance(outcome, HealNoMatch)
            assert read_cache(cache_key(self.SELECTORS)) is _heal.CACHE_ABSENT
