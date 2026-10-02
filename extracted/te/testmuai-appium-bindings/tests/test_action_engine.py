"""Element verb engine: find, ambiguity, failure routing, coordinate fallback."""
import time

import pytest
import testmu_appium
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidElementStateException,
    InvalidSelectorException,
    StaleElementReferenceException,
)

from testmu_appium import _action_engine, _action_web, _config
from testmu_appium import _heal
from testmu_appium._action_engine import _ActionSpec, _run_action, run_driver
# Bound before the autouse fixture replaces the module attribute with a stub, so the
# settle suite below can exercise the real implementation.
from testmu_appium._action_engine import _settle as _real_settle
from testmu_appium._errors import (
    CoordinateFallbackUnavailable, ElementBlocked, ElementNotFound,
)
from testmu_appium._heal import (
    HealDisabled, HealHit, HealNoMatch, HealUnavailable, HealUnresolved, WebHealHit,
)
from testmu_appium._helpers.authoring_web_surface import use_authoring_web_surface
from testmu_appium._step import current_step, step

SELECTORS = [
    {"strategy": "view_id", "selector": "com.app:id/go", "score": 90, "isXPath": False},
    {"strategy": "accessibility_id", "selector": "Go", "score": 80, "isXPath": False},
]

BASIS = {"x_ratio": 0.5, "y_ratio": 0.25, "orientation": "portrait", "window": [1080, 2340]}


class _El:
    def __init__(self, name="el"):
        self.name = name
        self.rect = {"x": 10, "y": 20, "width": 100, "height": 50}


class _StaleEl:
    """An element that detaches between the find and the rect read: `.rect` fires
    a second WebDriver call and raises, exactly as a recycled Android
    RecyclerView row's does mid-scroll."""

    name = "stale"

    @property
    def rect(self):
        raise StaleElementReferenceException("row recycled by the scroll")


class _Driver:
    """Scripted find_elements: a dict of value-substring → result, or a queue."""

    page_source = "<hierarchy rotation='0'/>"

    def __init__(self, results=None, queue=None):
        self.results = results or {}
        self.queue = list(queue) if queue is not None else None
        self.find_calls = []

    def get_window_size(self):
        return {"width": 1080, "height": 2340}

    def find_elements(self, by, value):
        self.find_calls.append((by, value))
        if self.queue is not None:
            return self.queue.pop(0) if self.queue else []
        for needle, result in self.results.items():
            if needle in value:
                return result
        return []


def _spec(runner=None, coord_runner=None, op_type="click"):
    return _ActionSpec(
        runner=runner or (lambda el, ctx: ("ran", el.name)),
        target_mode="element",
        op_type=op_type,
        coord_runner=coord_runner,
    )


@pytest.fixture(autouse=True)
def _fast(monkeypatch):
    """No real sleeping, no real settling, no accidental heal."""
    monkeypatch.setattr(_action_engine.time, "sleep", lambda s: None)
    monkeypatch.setattr(_action_engine, "_settle", lambda driver, deadline: None)
    monkeypatch.setitem(_config._config, "platform", "android")
    # These suites are not about the find timeout; one strategy pass keeps a
    # deliberate miss instantaneous instead of polling for the real budget.
    monkeypatch.setitem(_config._config, "default_action_timeout_ms", 0)
    monkeypatch.setattr(
        _action_engine, "autoheal",
        lambda *a, **kw: HealUnavailable("heal not stubbed in this test"),
    )
    monkeypatch.setattr(
        _action_engine, "autoheal_web",
        lambda *a, **kw: HealUnavailable("web heal not stubbed in this test"),
    )


def _act(driver, spec=None, **kw):
    with step("Tap Go"):
        return _run_action(driver, spec or _spec(), SELECTORS, description="Go button", **kw)


class TestActionTiming:
    def test_native_tree_capture_uses_target_scoped_readiness(self, monkeypatch):
        monkeypatch.setattr(
            _action_engine,
            "_settle",
            lambda *args: pytest.fail("native tree grounding must not read page source"),
        )
        driver = _Driver(results={"com.app:id/go": [_El("primary")]})

        with testmu_appium.capture_action_timings() as timings:
            assert _act(driver, grounded_by="tree") == ("ran", "primary")

        [timing] = timings
        assert timing["action_type"] == "click"
        assert timing["route"] == "native_selector"
        assert timing["settle_strategy"] == "target_scoped"
        assert timing["winning_strategy"] == "view_id"
        assert timing["outcome"] == "success"
        assert timing["counts"] == {
            "find_passes": 1,
            "selector_attempts": 1,
            "gesture_attempts": 1,
            "telemetry_reads": 1,
        }
        assert {
            "selector_compile", "element_lookup", "device_action", "element_telemetry",
        } <= timing["phases_ms"].keys()
        assert "page_source" not in timing["phases_ms"]
        assert "settle_wait" not in timing["phases_ms"]
        assert timing["total_ms"] >= 0
        # Diagnostics carry categories and counts, never target descriptions or
        # selector values that may contain customer data.
        assert "Go button" not in str(timing)
        assert "com.app:id/go" not in str(timing)

    def test_capture_keeps_the_failed_action_and_error_type(self):
        def fail(_element, _ctx):
            raise RuntimeError("device rejected click")

        with testmu_appium.capture_action_timings() as timings:
            with pytest.raises(RuntimeError, match="device rejected"):
                _act(_Driver(results={"com.app:id/go": [_El()]}), _spec(runner=fail))

        [timing] = timings
        assert timing["outcome"] == "error"
        assert timing["error_type"] == "RuntimeError"
        assert timing["counts"]["gesture_attempts"] == 1


class TestFind:
    def test_first_strategy_with_exactly_one_match_wins(self):
        driver = _Driver(results={"com.app:id/go": [_El("primary")]})
        assert _act(driver) == ("ran", "primary")
        assert len(driver.find_calls) == 1

    def test_zero_matches_advances_to_the_next_strategy(self):
        driver = _Driver(queue=[[], [_El("secondary")]])
        assert _act(driver) == ("ran", "secondary")
        assert len(driver.find_calls) == 2

    def test_ambiguous_match_advances_to_the_next_strategy(self):
        """Multiple hits mean this strategy cannot identify the target; the recorded
        order already demoted ambiguous strategies, so the next one is tried."""
        driver = _Driver(queue=[[_El("a"), _El("b")], [_El("secondary")]])
        assert _act(driver) == ("ran", "secondary")

    def test_selectors_are_tried_in_score_order(self):
        driver = _Driver(queue=[[], [_El()]])
        unordered = [
            {"strategy": "accessibility_id", "selector": "Go", "score": 80},
            {"strategy": "view_id", "selector": "com.app:id/go", "score": 90},
        ]
        with step("s"):
            _run_action(driver, _spec(), unordered, description="Go")
        assert "com.app:id/go" in driver.find_calls[0][1]


class TestLocateSelectorsRect:
    """`locate_selectors_rect` re-measures one target through the SAME ranked walk
    the grounding find uses, then reads its live rect — the cheap re-find the band
    nudge runs after each gesture, in place of the old identity probe."""

    def test_returns_the_rect_of_the_single_element_the_top_selector_names(self):
        el = _El("target")
        # Only the view_id query — UiSelector().resourceId(...) — resolves it: the
        # exact query the real grounding uses, and the one AppiumBy.ID (the old
        # probe's path) cannot match on a Compose testTag.
        driver = _Driver(results={"com.app:id/go": [el]})
        assert _action_engine.locate_selectors_rect(driver, SELECTORS, "android") == el.rect
        assert "com.app:id/go" in driver.find_calls[0][1]

    def test_returns_None_when_no_recorded_selector_isolates_the_target(self):
        # Every strategy misses — the target is gone from the screen. None means
        # UNRESOLVED, never "still at the old rect"; the caller must not read the
        # absence as movement and fabricate a scroll.
        driver = _Driver(results={})
        assert _action_engine.locate_selectors_rect(driver, SELECTORS, "android") is None

    def test_all_ambiguous_returns_None_rather_than_guessing_one_match(self):
        # A scroll can bring duplicate list rows on screen so every recorded
        # selector matches several. There is no fabricated pick here: the recorded
        # centre is the PRE-scroll position, so "nearest the old centre" would pick
        # the row that did NOT move. Unresolved -> None -> the nudge reports no move.
        driver = _Driver(queue=[[_El("a"), _El("b")], [_El("c"), _El("d")]])
        assert _action_engine.locate_selectors_rect(driver, SELECTORS, "android") is None

    def test_returns_None_when_the_target_detaches_before_its_rect_is_read(self):
        # `_find_one` returns the element, then `.rect` fires a SECOND WebDriver
        # call — and a scroll is exactly what recycles a RecyclerView row in
        # between. A stale read is UNRESOLVED (None), never an exception a caller
        # written to the "rect, or None" contract is unprepared for; the nudge
        # then reports no movement instead of aborting.
        driver = _Driver(results={"com.app:id/go": [_StaleEl()]})
        assert _action_engine.locate_selectors_rect(driver, SELECTORS, "android") is None


class TestExplicitGrounding:
    """New recordings state whether selectors or vision grounded their target."""

    def test_vision_resolves_the_description_and_runs_only_the_vision_actor(
            self, monkeypatch):
        calls = []
        monkeypatch.setattr(
            _action_engine, "_settle",
            lambda driver, deadline: calls.append(("settle",)),
        )
        monkeypatch.setattr(
            _action_engine, "get_vision_coordinates",
            lambda driver, description, action_type: (
                calls.append(("resolve", description, action_type)) or (321, 654)
            ),
        )
        spec = _ActionSpec(
            runner=lambda *a: pytest.fail("vision must not enter the selector runner"),
            coord_runner=lambda *a: pytest.fail("vision must not use legacy coordinates"),
            vision_runner=lambda driver, x, y, ctx: (
                calls.append(("act", x, y, ctx["description"])) or "done"
            ),
        )
        with step("vision click"):
            result = _run_action(
                _Driver(), spec, None,
                description="the green checkout button",
                grounded_by="vision",
            )
        assert result == "done"
        assert calls == [
            ("settle",),
            ("resolve", "the green checkout button", "click"),
            ("act", 321, 654, "the green checkout button"),
        ]

    @pytest.mark.parametrize("description", ["", "   "])
    def test_vision_requires_a_semantic_description(self, description):
        with pytest.raises(ValueError, match="needs description"):
            _run_action(
                _Driver(), _spec(coord_runner=lambda *a: True), None,
                description=description, grounded_by="vision",
            )

    @pytest.mark.parametrize("mixed", ["selectors", "coordinates"])
    def test_vision_rejects_replay_geometry(self, mixed):
        kwargs = {"selectors": None, "fallback_coordinates": None}
        if mixed == "selectors":
            kwargs["selectors"] = SELECTORS
        else:
            kwargs["fallback_coordinates"] = BASIS
        with pytest.raises(ValueError, match="grounded_by='vision'"):
            _run_action(
                _Driver(), _ActionSpec(
                    runner=lambda *a: True,
                    coord_runner=lambda *a: True,
                    vision_runner=lambda *a: True,
                ),
                kwargs["selectors"],
                description="target",
                fallback_coordinates=kwargs["fallback_coordinates"],
                grounded_by="vision",
            )

    def test_tree_requires_selectors_and_refuses_coordinate_degradation(self):
        with pytest.raises(ValueError, match="needs selectors"):
            _run_action(
                _Driver(), _spec(coord_runner=lambda *a: True), None,
                description="target", grounded_by="tree",
            )
        with pytest.raises(ValueError, match="cannot carry fallback_coordinates"):
            _run_action(
                _Driver(), _spec(coord_runner=lambda *a: True), SELECTORS,
                description="target", fallback_coordinates=BASIS,
                grounded_by="tree",
            )

    def test_legacy_selectorless_coordinate_shape_is_unchanged(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealNoMatch("not on this screen"))
        calls = []
        with step("legacy point"):
            result = _run_action(
                _Driver(),
                _spec(coord_runner=lambda driver, x, y, ctx: calls.append((x, y)) or True),
                None,
                description="legacy",
                fallback_coordinates=BASIS,
            )
        assert result is True
        assert calls == [(540, 585)]


class TestControlCharacterSelectors:
    """A recorded text value legitimately carries control characters — a two-line list
    row, a pasted address, a tab-aligned cell. They are escaped before they reach a
    UiSelector Java string literal, so the strategy walk continues to the next recorded
    locator, then to heal, then to the coordinate basis. A raw one makes the device
    answer with an invalid-selector exception, which escapes the walk entirely.
    """

    MULTILINE = [
        {"strategy": "text", "selector": "221B Baker Street\nLondon", "score": 90},
        {"strategy": "view_id", "selector": "com.app:id/go", "score": 80},
    ]

    class _StrictDriver(_Driver):
        """Rejects a query carrying a raw control character, the way the device does."""

        def find_elements(self, by, value):
            if any(character <= "\x1f" for character in value):
                raise InvalidSelectorException(f"invalid selector: {value!r}")
            return super().find_elements(by, value)

    def test_a_multiline_text_selector_falls_through_to_the_next_strategy(self):
        driver = self._StrictDriver(queue=[[], [_El("by-id")]])
        with step("Tap Go"):
            result = _run_action(driver, _spec(), self.MULTILINE, description="Go")
        assert result == ("ran", "by-id")
        assert "\\n" in driver.find_calls[0][1]

    def test_a_multiline_text_selector_can_itself_be_the_match(self):
        driver = self._StrictDriver(queue=[[_El("multiline")]])
        with step("Tap Go"):
            result = _run_action(driver, _spec(), self.MULTILINE, description="Go")
        assert result == ("ran", "multiline")

    def test_a_multiline_selector_reaches_the_coordinate_fallback(self, monkeypatch):
        """The end of the recovery path: the escaped walk exhausts, heal answers with
        an authoritative miss, and the recorded basis is tapped."""
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        driver = self._StrictDriver(queue=[[], []])
        spec = _ActionSpec(
            runner=lambda el, ctx: None, target_mode="element", op_type="click",
            coord_runner=lambda d, x, y, ctx: ("tapped", x, y),
        )
        with step("Tap Go"):
            result = _run_action(driver, spec, self.MULTILINE, description="Go",
                                 fallback_coordinates=BASIS)
        assert result == ("tapped", 540, 585)


class TestActionTimeout:
    """default_action_timeout_ms bounds the strategy walk.

    The walk is polled until the budget expires, so an element that renders part-way
    into the verb is waited for. Exhaustion — the heal trigger — is declared only once
    the budget is spent.
    """

    class _LateDriver:
        """Materialises the element on the Nth find_elements call."""

        page_source = "<hierarchy rotation='0'/>"

        def __init__(self, appears_on_call):
            self.appears_on_call = appears_on_call
            self.find_calls = []

        def get_window_size(self):
            return {"width": 1080, "height": 2340}

        def find_elements(self, by, value):
            self.find_calls.append((by, value))
            if len(self.find_calls) >= self.appears_on_call:
                return [_El("late")]
            return []

    @pytest.fixture(autouse=True)
    def _budget(self, monkeypatch):
        """A real budget, with the poll sleep stubbed so the wait is instant."""
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", 10000)
        monkeypatch.setattr(_action_engine, "autoheal", self._must_not_heal)

    @staticmethod
    def _must_not_heal(*args, **kwargs):
        raise AssertionError("a late element must be waited for, not healed for")

    @pytest.mark.parametrize("appears_on_call", [3, 5, 12])
    def test_a_late_element_is_waited_for_rather_than_healed_for(self, appears_on_call):
        driver = self._LateDriver(appears_on_call=appears_on_call)
        assert _act(driver) == ("ran", "late")
        assert len(driver.find_calls) >= appears_on_call

    def test_an_element_present_on_the_first_pass_does_not_wait(self, monkeypatch):
        slept = []
        monkeypatch.setattr(_action_engine.time, "sleep", lambda s: slept.append(s))
        driver = _Driver(results={"com.app:id/go": [_El("primary")]})
        assert _act(driver) == ("ran", "primary")
        assert not slept

    def test_the_walk_polls_between_passes(self, monkeypatch):
        slept = []
        monkeypatch.setattr(_action_engine.time, "sleep", lambda s: slept.append(s))
        _act(self._LateDriver(appears_on_call=5))
        assert slept and all(s == _action_engine._FIND_POLL_INTERVAL_S for s in slept)

    def test_an_expired_budget_still_reaches_heal(self, monkeypatch):
        """The timeout delays exhaustion; it never removes it."""
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", 0)
        healed = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: healed.append(1) or HealNoMatch("gone"),
        )
        with pytest.raises(ElementNotFound):
            _act(_Driver(queue=[[], []]))
        assert len(healed) == 1

    @pytest.mark.parametrize("budget", [0, None, "", -1])
    def test_a_zero_or_absent_budget_makes_exactly_one_pass(self, monkeypatch, budget):
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", budget)
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("x"))
        driver = _Driver(queue=[[], []])
        with pytest.raises(ElementNotFound):
            _act(driver)
        assert len(driver.find_calls) == len(SELECTORS)

    class _Ambiguous(_LateDriver):
        """Every strategy matches several elements until the Nth call."""

        def find_elements(self, by, value):
            self.find_calls.append((by, value))
            if len(self.find_calls) < self.appears_on_call:
                return [_El("a"), _El("b")]
            return [_El("late")]

    def test_a_row_duplicated_mid_animation_is_still_waited_out(self):
        """A list rebuilding itself can show two copies of a row for a moment, so
        one all-ambiguous pass is not yet evidence the locator is unusable."""
        driver = self._Ambiguous(appears_on_call=4)
        assert _act(driver) == ("ran", "late")

    def test_a_permanently_ambiguous_walk_stops_instead_of_spending_the_budget(
            self, monkeypatch):
        """A recycled view id does not become unique because it was polled again:
        the screen has rendered and only heal can separate the row."""
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("x"))
        driver = self._Ambiguous(appears_on_call=10_000)
        with pytest.raises(ElementNotFound):
            _act(driver)
        assert len(driver.find_calls) == (
            len(SELECTORS) * _action_engine._AMBIGUOUS_PASSES)

    def test_a_late_render_resets_the_ambiguity_count(self):
        """Ambiguous, then a strategy matching nothing, then ambiguous again is the
        late-render case the poll exists for — the two ambiguous passes are not
        consecutive and must not add up to exhaustion."""

        class _Alternating(self._LateDriver):
            def find_elements(self, by, value):
                self.find_calls.append((by, value))
                index = len(self.find_calls)
                if index >= self.appears_on_call:
                    return [_El("late")]
                return [] if index % 4 in (0, 3) else [_El("a"), _El("b")]

        driver = _Alternating(appears_on_call=9)
        assert _act(driver) == ("ran", "late")


class TestSharedDeadline:
    """One monotonic deadline per verb call, shared by settle → find → heal → re-find.

    Each phase gets its own configured budget or whatever is left of the verb,
    whichever expires first. The stale and healed re-finders poll on that budget too,
    so a re-find landing mid-rebuild waits instead of failing on its first miss.
    """

    class _RefindDriver:
        """Hits once (the initial find), then misses N times, then hits again."""

        page_source = "<hierarchy rotation='0'/>"

        def __init__(self, misses):
            self.misses = misses
            self.find_calls = []

        def get_window_size(self):
            return {"width": 1080, "height": 2340}

        def find_elements(self, by, value):
            self.find_calls.append((by, value))
            if len(self.find_calls) == 1:
                return [_El("first")]
            if len(self.find_calls) <= 1 + self.misses:
                return []
            return [_El("re-found")]

    @staticmethod
    def _stale_once():
        runs = {"n": 0}

        def runner(el, ctx):
            runs["n"] += 1
            if runs["n"] == 1:
                raise StaleElementReferenceException("gone")
            return ("ran", el.name)

        return runner

    def test_a_stale_re_find_polls_instead_of_giving_up_on_the_first_miss(self, monkeypatch):
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", 10000)
        driver = self._RefindDriver(misses=3)
        assert _act(driver, _spec(self._stale_once())) == ("ran", "re-found")

    def test_the_same_re_find_fails_when_no_budget_was_configured(self, monkeypatch):
        """Guards the premise: with a zero budget the re-find is one pass, so a
        mid-rebuild re-find raises instead of waiting."""
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", 0)
        driver = self._RefindDriver(misses=3)
        with pytest.raises(StaleElementReferenceException):
            _act(driver, _spec(self._stale_once()))

    def test_a_healed_re_find_polls_too(self, monkeypatch):
        # A short budget: the recorded walk has to EXHAUST it to reach heal at all,
        # and the healed re-find then runs on what is left of the same deadline.
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", 200)
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=_El("healed"), by="id", value="v", dom_index=3),
        )

        class _HealedLookupSettles(_Driver):
            """The recorded strategies never hit; the healed lookup hits on its third."""

            def __init__(self):
                super().__init__()
                self.healed_lookups = 0

            def find_elements(self, by, value):
                self.find_calls.append((by, value))
                if value != "v":
                    return []
                self.healed_lookups += 1
                return [_El("fresh")] if self.healed_lookups > 2 else []

        driver = _HealedLookupSettles()
        assert _act(driver, _spec(self._stale_once())) == ("ran", "fresh")
        assert driver.healed_lookups == 3, "a single-shot healed lookup would have failed"

    def test_the_re_find_poll_stops_at_the_shared_deadline(self, monkeypatch):
        """The re-find gets the find budget OR whatever is left of the verb, whichever
        expires first — it cannot outlive the step it belongs to."""
        monkeypatch.setitem(_config._config, "settle_timeout_ms", 0)
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", 10000)
        monkeypatch.setitem(_config._config, "heal_timeout_ms", 0)
        deadline = _action_engine._Deadline()
        deadline.expires_at = _action_engine.time.monotonic()  # nothing left
        assert deadline.remaining_s() == 0.0
        assert deadline.phase_end(10000) <= deadline.expires_at

    def test_heal_is_given_no_more_time_than_the_verb_has_left(self, monkeypatch):
        monkeypatch.setitem(_config._config, "settle_timeout_ms", 0)
        monkeypatch.setitem(_config._config, "default_action_timeout_ms", 0)
        monkeypatch.setitem(_config._config, "heal_timeout_ms", 5000)
        seen = {}

        def fake(driver_, instruction, action_type, budget_s=None):
            seen["budget_s"] = budget_s
            return HealNoMatch("gone")

        monkeypatch.setattr(_action_engine, "autoheal", fake)
        with pytest.raises(ElementNotFound):
            _act(_Driver(queue=[[], []]))
        assert 0 < seen["budget_s"] <= 5.0

    def test_settling_is_measured_on_the_monotonic_clock(self, monkeypatch):
        """A wall-clock correction landing mid-settle must not end the wait early —
        or extend it. Settling is measured against a monotonic deadline, so an NTP
        step between two reads leaves it running."""

        class _Churning:
            """A screen that never stops changing, so only the budget can stop settling."""

            def __init__(self):
                self.reads = 0

            @property
            def page_source(self):
                self.reads += 1
                return f"<hierarchy n='{self.reads}'/>"

        monkeypatch.setitem(_config._config, "settle_timeout_ms", 50)
        monkeypatch.setattr(_action_engine.time, "sleep", lambda s: None)
        # Wall clock leaps forward by a day on every read; monotonic is untouched.
        jumps = iter(range(0, 10_000_000, 86_400))
        monkeypatch.setattr(_action_engine.time, "time", lambda: next(jumps))

        driver = _Churning()
        _real_settle(driver, _action_engine._Deadline())
        assert driver.reads > 1, "the wall-clock jump ended the settle after one read"


class TestFailureRouting:
    def test_stale_element_re_finds_and_retries_without_healing(self, monkeypatch):
        healed = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: healed.append(1) or HealUnavailable("x"),
        )
        driver = _Driver(results={"com.app:id/go": [_El("fresh")]})
        calls = {"n": 0}

        def runner(el, ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise StaleElementReferenceException("gone")
            return ("ran", el.name)

        assert _act(driver, _spec(runner)) == ("ran", "fresh")
        assert calls["n"] == 2
        assert not healed

    def test_persistent_staleness_eventually_fails(self):
        driver = _Driver(results={"com.app:id/go": [_El()]})

        def runner(el, ctx):
            raise StaleElementReferenceException("gone")

        with pytest.raises(StaleElementReferenceException):
            _act(driver, _spec(runner))

    @pytest.mark.parametrize(
        "exc", [ElementClickInterceptedException, ElementNotInteractableException]
    )
    def test_blocked_element_retries_then_fails_without_healing(self, exc, monkeypatch):
        healed = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: healed.append(1) or HealUnavailable("x"),
        )
        driver = _Driver(results={"com.app:id/go": [_El()]})

        def runner(el, ctx):
            raise exc("covered by an overlay")

        with pytest.raises(ElementBlocked):
            _act(driver, _spec(runner))
        assert not healed, "a present-but-covered element must never be routed to heal"

    def test_blocked_native_tree_element_settles_only_after_blockage(self, monkeypatch):
        driver = _Driver(results={"com.app:id/go": [_El("free")]})
        calls = {"n": 0}
        settles = []
        monkeypatch.setattr(
            _action_engine, "_settle",
            lambda driver, deadline: settles.append("blocked"),
        )

        def runner(el, ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise ElementClickInterceptedException("overlay")
            return ("ran", el.name)

        assert _act(driver, _spec(runner), grounded_by="tree") == ("ran", "free")
        assert settles == ["blocked"]

    def test_an_element_in_the_wrong_state_fails_on_the_first_attempt(self, monkeypatch):
        """`InvalidElementStateException` is a property of the element, not of the
        moment: sendKeys to a LinearLayout is refused, and settling does not make a
        LinearLayout editable. Retrying it spends the blocked budget on a verdict
        that cannot change — measured at 15s per occurrence on a real app."""
        settles = []
        monkeypatch.setattr(_action_engine, "_settle",
                            lambda *a, **kw: settles.append(1))
        driver = _Driver(results={"com.app:id/go": [_El()]})
        attempts = {"n": 0}

        def runner(el, ctx):
            attempts["n"] += 1
            raise InvalidElementStateException("Cannot set the element to 'x'")

        with pytest.raises(ElementBlocked):
            _act(driver, _spec(runner))
        assert attempts["n"] == 1
        # The one settle is the pre-action one every element verb does; what must
        # not happen is a settle-and-retry ROUND after the verdict.
        assert len(settles) == 1

    def test_blocked_element_never_falls_back_to_coordinates(self):
        """Coordinates would punch through whatever is covering the element."""
        driver = _Driver(results={"com.app:id/go": [_El()]})
        coord_calls = []

        def runner(el, ctx):
            raise ElementClickInterceptedException("overlay")

        with pytest.raises(ElementBlocked):
            _act(driver, _spec(runner, coord_runner=lambda *a: coord_calls.append(1)),
                 fallback_coordinates=BASIS)
        assert not coord_calls


class TestHeal:
    def test_exhaustion_triggers_heal_and_acts_on_the_healed_element(self, monkeypatch):
        driver = _Driver(queue=[[], []])
        healed_el = _El("healed")
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=healed_el, by="id", value="v", dom_index=3),
        )
        assert _act(driver) == ("ran", "healed")

    def test_heal_marks_the_step_telemetry(self, monkeypatch):
        driver = _Driver(queue=[[], []])
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=_El(), by="id", value="v", dom_index=3),
        )
        seen = {}
        with step("Tap Go"):
            _run_action(driver, _spec(), SELECTORS, description="Go")
            seen["info"] = current_step()
        assert seen["info"].is_autohealed is True
        assert seen["info"].autoheal_source == "v16-autoheal"

    def test_heal_is_attempted_once_per_verb_call(self, monkeypatch):
        driver = _Driver(queue=[[], [], [], []])
        calls = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: calls.append(1) or HealNoMatch("gone"),
        )
        with pytest.raises(ElementNotFound):
            _act(driver)
        assert len(calls) == 1

    def test_authoritative_miss_is_cached_and_short_circuits_the_next_call(self, monkeypatch):
        driver = _Driver(queue=[[], [], [], []])
        calls = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: calls.append(1) or HealNoMatch("gone"),
        )
        with step("Tap Go"):
            for _ in range(2):
                with pytest.raises(ElementNotFound):
                    _run_action(driver, _spec(), SELECTORS, description="Go")
        assert len(calls) == 1, "the negative sentinel must suppress the second call"

    def test_unavailable_heal_is_not_cached(self, monkeypatch):
        driver = _Driver(queue=[[], [], [], []])
        calls = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: calls.append(1) or HealUnavailable("gateway down"),
        )
        with step("Tap Go"):
            for _ in range(2):
                with pytest.raises(ElementNotFound):
                    _run_action(driver, _spec(), SELECTORS, description="Go")
        assert len(calls) == 2, "a transport failure is not evidence the element is gone"

    def test_unavailable_heal_does_not_unlock_coordinates(self, monkeypatch):
        driver = _Driver(queue=[[], []])
        monkeypatch.setattr(
            _action_engine, "autoheal", lambda *a, **kw: HealUnavailable("gateway down")
        )
        coord_calls = []
        with pytest.raises(ElementNotFound) as exc:
            _act(driver, _spec(coord_runner=lambda *a: coord_calls.append(1)),
                 fallback_coordinates=BASIS)
        assert not coord_calls
        assert "gateway down" in str(exc.value)

    def test_heal_op_type_comes_from_the_spec(self, monkeypatch):
        driver = _Driver(queue=[[], []])
        seen = {}

        def fake(driver_, instruction, action_type, **kwargs):
            seen["action_type"] = action_type
            return HealNoMatch("gone")

        monkeypatch.setattr(_action_engine, "autoheal", fake)
        with pytest.raises(ElementNotFound):
            _act(driver, _spec(op_type="scroll"))
        assert seen["action_type"] == "scroll"


class TestUnresolvedHeal:
    """A 200 whose answer would not resolve LOCALLY to one live element.

    It arrives as HealUnresolved, not HealNoMatch: it gets one fresh-perception retry,
    is never cached as the negative sentinel, and never unlocks coordinates.
    """

    def _heal_returning(self, monkeypatch, outcomes):
        calls = []

        def fake(*args, **kwargs):
            calls.append(1)
            return outcomes[min(len(calls) - 1, len(outcomes) - 1)]

        monkeypatch.setattr(_action_engine, "autoheal", fake)
        return calls

    def test_one_fresh_retry_is_allowed_and_a_hit_on_it_wins(self, monkeypatch):
        calls = self._heal_returning(monkeypatch, [
            HealUnresolved("matched 0 live elements, expected 1"),
            HealHit(element=_El("second-look"), by="id", value="v", dom_index=3),
        ])
        assert _act(_Driver(queue=[[], []])) == ("ran", "second-look")
        assert len(calls) == 2, "the answer arrived; a fresh look at the screen is owed"

    def test_the_retry_is_bounded_at_one(self, monkeypatch):
        calls = self._heal_returning(
            monkeypatch, [HealUnresolved("matched 3 live elements, expected 1")]
        )
        with pytest.raises(ElementNotFound) as exc:
            _act(_Driver(queue=[[], []]))
        assert len(calls) == 2
        assert "did not resolve" in str(exc.value)

    def test_unresolved_never_unlocks_coordinates(self, monkeypatch):
        """No 404 was received, so nothing established that the element is gone —
        and a blind tap at a recorded ratio assumes it is."""
        self._heal_returning(monkeypatch, [HealUnresolved("matched 0 live elements")])
        coord_calls = []
        with pytest.raises(ElementNotFound):
            _act(_Driver(queue=[[], []]),
                 _spec(coord_runner=lambda *a: coord_calls.append(1)),
                 fallback_coordinates=BASIS)
        assert not coord_calls

    def test_unresolved_is_not_cached_as_an_authoritative_miss(self, monkeypatch):
        calls = self._heal_returning(monkeypatch, [HealUnresolved("matched 0")])
        driver = _Driver(queue=[[], [], [], []])
        with step("Tap Go") as info:
            for _ in range(2):
                with pytest.raises(ElementNotFound):
                    _run_action(driver, _spec(), SELECTORS, description="Go")
            assert None not in info.heal_cache.values()
        assert len(calls) == 4, "a local lookup miss must not suppress the next heal"


class TestPositiveHealCache:
    """The cached POSITIVE remap branch.

    Sequence in every test here: attempt 1 heals and caches (by, value); attempt 2 in
    the SAME step re-finds through the cached pair instead of re-asking the server.
    """

    HEALED = ("id", "healed-locator")

    def _healing_driver(self, monkeypatch, second_attempt_matches):
        """A driver whose recorded strategies always miss, plus a heal that hits once.

        The find queue is: [miss, miss] for attempt 1's strategy walk, [healed] for
        heal's own re-find, [miss, miss] for attempt 2's walk, then whatever attempt
        2's cached-remap lookup should see.
        """
        healed_el = _El("healed")
        calls = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: calls.append(1) or HealHit(
                element=healed_el, by=self.HEALED[0], value=self.HEALED[1], dom_index=3,
            ),
        )
        driver = _Driver(queue=[[], [], [], [], second_attempt_matches])
        return driver, calls, healed_el

    def test_a_live_cached_remap_is_replayed_without_re_asking_the_server(self, monkeypatch):
        cached_el = _El("cached")
        driver, calls, _ = self._healing_driver(monkeypatch, [cached_el])
        with step("Tap Go"):
            first = _run_action(driver, _spec(), SELECTORS, description="Go")
            second = _run_action(driver, _spec(), SELECTORS, description="Go")
        assert first == ("ran", "healed")
        assert second == ("ran", "cached")
        assert len(calls) == 1, "the cached remap must not re-ask the server"
        assert driver.find_calls[-1] == self.HEALED

    def test_the_cached_remap_path_stamps_the_autoheal_source(self, monkeypatch):
        driver, _, _ = self._healing_driver(monkeypatch, [_El("cached")])
        seen = {}
        with step("Tap Go"):
            _run_action(driver, _spec(), SELECTORS, description="Go")
            current_step().is_autohealed = False
            current_step().autoheal_source = ""
            _run_action(driver, _spec(), SELECTORS, description="Go")
            seen["info"] = current_step()
        assert seen["info"].is_autohealed is True
        assert seen["info"].autoheal_source == "v16-autoheal"

    @pytest.mark.parametrize(
        "stale_matches", [[], [_El("a"), _El("b")]], ids=["gone", "ambiguous"]
    )
    def test_a_stale_cached_remap_re_heals_instead_of_claiming_a_miss(
        self, monkeypatch, stale_matches
    ):
        """A cached remap that no longer resolves drops its entry and re-asks the
        server; it does not synthesise HealNoMatch, write the negative sentinel or
        unlock a coordinate tap."""
        driver, calls, healed_el = self._healing_driver(monkeypatch, stale_matches)
        coord_calls = []
        spec = _spec(coord_runner=lambda *a: coord_calls.append(1) or "tapped")
        with step("Tap Go"):
            _run_action(driver, spec, SELECTORS, description="Go",
                        fallback_coordinates=BASIS)
            second = _run_action(driver, spec, SELECTORS, description="Go",
                                 fallback_coordinates=BASIS)
        assert second == ("ran", "healed"), "the stale entry must fall through to a heal"
        assert len(calls) == 2, "the fresh heal is the only way to regain authority"
        assert not coord_calls, "a local lookup miss must never unlock coordinates"

    def test_a_stale_cached_remap_never_writes_the_negative_sentinel(self, monkeypatch):
        driver, _, _ = self._healing_driver(monkeypatch, [])
        with step("Tap Go") as info:
            _run_action(driver, _spec(), SELECTORS, description="Go")
            _run_action(driver, _spec(), SELECTORS, description="Go")
            assert None not in info.heal_cache.values()

    def test_a_cached_remap_whose_lookup_errors_re_heals(self, monkeypatch):
        """An exception out of the cached lookup is a miss, not a crash — and not
        evidence about the element either."""
        healed_el = _El("healed")
        calls = []
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: calls.append(1) or HealHit(
                element=healed_el, by=self.HEALED[0], value=self.HEALED[1], dom_index=3,
            ),
        )

        class _Exploding(_Driver):
            def find_elements(self, by, value):
                self.find_calls.append((by, value))
                if value == "healed-locator" and len(calls) == 1:
                    raise RuntimeError("driver session hiccup")
                return self.queue.pop(0) if self.queue else []

        driver = _Exploding(queue=[[], [], [], [], []])
        with step("Tap Go"):
            _run_action(driver, _spec(), SELECTORS, description="Go")
            assert _run_action(driver, _spec(), SELECTORS, description="Go") == (
                "ran", "healed"
            )
        assert len(calls) == 2

    def test_a_healed_element_that_goes_stale_re_finds_via_the_healed_locator(
        self, monkeypatch
    ):
        """Re-finding through the exhausted RECORDED strategies would miss by
        construction — they are why heal ran in the first place."""
        healed_el, fresh_el = _El("healed"), _El("fresh")
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(
                element=healed_el, by=self.HEALED[0], value=self.HEALED[1], dom_index=3,
            ),
        )
        driver = _Driver(queue=[[], [], [fresh_el]])
        runs = {"n": 0}

        def runner(el, ctx):
            runs["n"] += 1
            if runs["n"] == 1:
                raise StaleElementReferenceException("gone")
            return ("ran", el.name)

        assert _act(driver, _spec(runner)) == ("ran", "fresh")
        assert driver.find_calls[-1] == self.HEALED


class TestCoordinateFallback:
    def _exhausted(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        return _Driver(queue=[[], []])

    def test_authoritative_miss_unlocks_the_ratio_fallback(self, monkeypatch):
        driver = self._exhausted(monkeypatch)
        got = {}
        spec = _ActionSpec(
            runner=lambda el, ctx: None, target_mode="element", op_type="click",
            coord_runner=lambda d, x, y, ctx: got.update(x=x, y=y) or "tapped",
        )
        assert _act(driver, spec, fallback_coordinates=BASIS) == "tapped"
        assert got == {"x": 540, "y": 585}

    def test_orientation_mismatch_refuses_the_fallback(self, monkeypatch):
        driver = self._exhausted(monkeypatch)
        landscape = dict(BASIS, orientation="landscape")
        spec = _ActionSpec(
            runner=lambda el, ctx: None, target_mode="element", op_type="click",
            coord_runner=lambda *a: "tapped",
        )
        with pytest.raises(ElementNotFound) as exc:
            _act(driver, spec, fallback_coordinates=landscape)
        assert isinstance(exc.value.__cause__, CoordinateFallbackUnavailable)
        assert "orientation" in str(exc.value.__cause__)

    def test_incomplete_basis_refuses_the_fallback(self, monkeypatch):
        driver = self._exhausted(monkeypatch)
        spec = _ActionSpec(
            runner=lambda el, ctx: None, target_mode="element", op_type="click",
            coord_runner=lambda *a: "tapped",
        )
        with pytest.raises(ElementNotFound) as exc:
            _act(driver, spec, fallback_coordinates={"x_ratio": 0.5, "y_ratio": 0.25})
        assert isinstance(exc.value.__cause__, CoordinateFallbackUnavailable)

    def test_no_basis_recorded_is_a_plain_element_not_found(self, monkeypatch):
        driver = self._exhausted(monkeypatch)
        with pytest.raises(ElementNotFound) as exc:
            _act(driver, _spec(coord_runner=lambda *a: "tapped"))
        assert exc.value.__cause__ is None

    def test_verb_without_a_coord_runner_cannot_fall_back(self, monkeypatch):
        driver = self._exhausted(monkeypatch)
        with pytest.raises(ElementNotFound):
            _act(driver, _spec(), fallback_coordinates=BASIS)

    def test_ratios_scale_to_the_live_window_not_the_recorded_one(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))

        class _Small(_Driver):
            def get_window_size(self):
                return {"width": 720, "height": 1560}

        driver = _Small(queue=[[], []])
        got = {}
        spec = _ActionSpec(
            runner=lambda el, ctx: None, target_mode="element", op_type="click",
            coord_runner=lambda d, x, y, ctx: got.update(x=x, y=y),
        )
        _act(driver, spec, fallback_coordinates=BASIS)
        assert got == {"x": 360, "y": 390}


class TestTelemetry:
    def test_successful_act_records_the_interacted_element(self):
        driver = _Driver(results={"com.app:id/go": [_El()]})
        seen = {}
        with step("Tap Go"):
            _run_action(driver, _spec(), SELECTORS, description="Go")
            seen["info"] = current_step()
        payload = seen["info"].interacted_element
        assert payload["bounds"] == [10, 20, 110, 70]
        assert payload["center"] == [60, 45]
        assert "com.app:id/go" in payload["original_locator"]

    def test_telemetry_failure_does_not_fail_the_verb(self):
        class _NoRect:
            name = "el"

            @property
            def rect(self):
                raise RuntimeError("stale")

        driver = _Driver(results={"com.app:id/go": [_NoRect()]})
        assert _act(driver) == ("ran", "el")


class TestTargetMode:
    def test_driver_mode_bypasses_find_entirely(self):
        driver = _Driver()
        spec = _ActionSpec(
            runner=lambda d, ctx: ("driver-ran", ctx["value"]),
            target_mode="driver", op_type="",
        )
        with step("Press back"):
            assert run_driver(driver, spec, value="BACK") == ("driver-ran", "BACK")
        assert driver.find_calls == []

    def test_element_mode_rejects_an_empty_selector_set_it_cannot_name(self):
        """An empty selector set is legal when the description names the target —
        heal re-grounds it. With neither, there is nothing to act on at all."""
        with pytest.raises(ValueError):
            with step("s"):
                _run_action(_Driver(), _spec(), [], description="")


class TestCoordinateRecordedAction:
    """`selectors=None` + a complete basis is the generator's coordinate-recorded shape.

    The recorded ratio is the LAST rung of the ladder, not the first. It is
    recomputed against the live window, so it survives a rescaled screen — but not
    a reflowed one, and it carries no locator that would notice it had landed on
    the wrong thing. Heal reads the live screen and returns an element, so it is
    asked first and the ratio is reached only on an authoritative miss, exactly as
    on the path where recorded selectors ran out.
    """

    def _spec_with_coordinates(self, calls):
        return _ActionSpec(
            runner=lambda el, ctx: pytest.fail("a coordinate-recorded action must not find"),
            target_mode="element",
            op_type="click",
            coord_runner=lambda d, x, y, ctx: calls.append((x, y)) or "tapped",
        )

    def test_a_complete_basis_still_heals_first(self, monkeypatch):
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=_El("healed"), by="id", value="v", dom_index=3),
        )
        calls = []
        spec = _ActionSpec(
            runner=lambda el, ctx: ("ran", el.name),
            target_mode="element",
            op_type="click",
            coord_runner=lambda d, x, y, ctx: calls.append((x, y)) or "tapped",
        )
        with step("Tap the canvas"):
            result = _run_action(
                _Driver(), spec, None,
                description="Tap the canvas at the recorded point",
                fallback_coordinates=BASIS,
            )
        assert result == ("ran", "healed")
        assert calls == [], "heal resolved the target; the remembered point is not owed"

    def test_an_authoritative_miss_falls_back_to_the_recorded_point(self, monkeypatch):
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealNoMatch("not on this screen"),
        )
        calls = []
        driver = _Driver()
        with step("Tap the canvas"):
            result = _run_action(
                driver, self._spec_with_coordinates(calls), None,
                description="Tap the canvas at the recorded point",
                fallback_coordinates=BASIS,
            )
        assert result == "tapped"
        assert calls == [(540, 585)]
        assert driver.find_calls == [], "nothing was recorded to find"

    def test_the_recorded_point_is_stamped_as_the_interacted_element(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealNoMatch("not on this screen"))
        calls = []
        with step("Tap the canvas") as info:
            _run_action(
                _Driver(), self._spec_with_coordinates(calls), None,
                description="Tap", fallback_coordinates=BASIS,
            )
            payload = info.interacted_element
        assert payload == {
            "original_locator": "", "bounds": [540, 585, 540, 585], "center": [540, 585],
        }

    def test_the_screen_settles_before_the_recorded_point_is_tapped(self, monkeypatch):
        """The selectorless path settles like every other element verb.

        A recorded point is aimed at a screen that has finished moving. Tapping one
        mid-transition lands on whatever occupies that spot instead, and this path
        carries no locator that would notice — the verb reports success and the
        failure surfaces at a later step, pointing at the wrong element.
        """
        order = []
        monkeypatch.setattr(_action_engine, "_settle",
                            lambda driver, deadline: order.append("settle"))
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealNoMatch("not on this screen"))
        spec = _ActionSpec(
            runner=lambda el, ctx: pytest.fail("a coordinate-recorded action must not find"),
            target_mode="element",
            op_type="click",
            coord_runner=lambda d, x, y, ctx: order.append("tap") or "tapped",
        )
        with step("Tap the canvas"):
            result = _run_action(
                _Driver(), spec, None, description="Tap",
                fallback_coordinates=BASIS,
            )
        assert result == "tapped"
        assert order == ["settle", "tap"]

    def test_an_orientation_mismatch_still_refuses(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealNoMatch("not on this screen"))
        calls = []
        with pytest.raises(ElementNotFound) as exc:
            with step("Tap the canvas"):
                _run_action(
                    _Driver(), self._spec_with_coordinates(calls), None,
                    description="Tap",
                    fallback_coordinates=dict(BASIS, orientation="landscape"),
                )
        assert isinstance(exc.value.__cause__, CoordinateFallbackUnavailable)
        assert "orientation" in str(exc.value.__cause__)
        assert not calls

    @pytest.mark.parametrize(
        "basis",
        [None, {}, {"x_ratio": 0.5, "y_ratio": 0.25}, dict(BASIS, orientation=None)],
        ids=["absent", "empty", "no-orientation", "null-orientation"],
    )
    def test_an_unusable_basis_leaves_heal_as_the_only_locator(self, basis, monkeypatch):
        """An unusable basis is no longer a generation error on its own.

        The description still names the target, so heal owns the action and only
        heal's authoritative miss — with nothing left to fall back to — ends it.
        """
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealNoMatch("not on this screen"))
        calls = []
        with pytest.raises(ElementNotFound):
            with step("s"):
                _run_action(
                    _Driver(), self._spec_with_coordinates(calls), None,
                    description="Tap", fallback_coordinates=basis,
                )
        assert not calls

    def test_a_verb_outside_heals_trained_set_never_reaches_it(self):
        """Every element verb shipped today maps to an op_type heal is trained on
        (`clear` and `search` ride "type"), so nothing exercises this branch yet.
        It is pinned so a verb added outside that set falls to the recorded point
        rather than being sent to an endpoint that cannot answer for it."""
        calls = []
        spec = _ActionSpec(
            runner=lambda el, ctx: pytest.fail("nothing was recorded to find"),
            target_mode="element",
            op_type="fling",
            coord_runner=lambda d, x, y, ctx: calls.append((x, y)) or "tapped",
        )
        with step("s"):
            result = _run_action(_Driver(), spec, None, description="Go",
                                 fallback_coordinates=BASIS)
        assert result == "tapped"
        assert calls == [(540, 585)]

    def test_driver_mode_spec_rejects_selectors(self):
        spec = _ActionSpec(runner=lambda d, ctx: None, target_mode="driver", op_type="")
        with pytest.raises(ValueError):
            with step("s"):
                _run_action(_Driver(), spec, SELECTORS, description="Go")

    def test_unknown_target_mode_raises(self):
        with pytest.raises(ValueError):
            _ActionSpec(runner=lambda el, ctx: None, target_mode="page", op_type="click")


class TestSelectorlessHeals:
    """A recording with no selectors still names its target, and that name is a
    locator: heal resolves it against the live screen.

    This is the same rung the tree path reaches when its recorded strategies run
    out — the two only differ in whether there were selectors to exhaust first.
    """

    HEALABLE = ["click", "type", "select", "scroll"]

    @staticmethod
    def _spec_for(op_type, calls=None):
        return _ActionSpec(
            runner=lambda el, ctx: ("ran", el.name),
            target_mode="element",
            op_type=op_type,
            coord_runner=(
                None if calls is None
                else lambda d, x, y, ctx: calls.append((x, y)) or "tapped"
            ),
        )

    @pytest.mark.parametrize("op_type", HEALABLE)
    def test_a_described_selectorless_action_heals(self, op_type, monkeypatch):
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=_El("healed"), by="id", value="v", dom_index=3),
        )
        with step("Tap it"):
            result = _run_action(
                _Driver(), self._spec_for(op_type), None,
                description='PRIMARY: state option "New York"; role=option',
            )
        assert result == ("ran", "healed")

    def test_the_description_is_what_heal_is_asked_about(self, monkeypatch):
        asked = []

        def _heal(driver, description, op_type, **kw):
            asked.append((description, op_type))
            return HealHit(element=_El("healed"), by="id", value="v", dom_index=3)

        monkeypatch.setattr(_action_engine, "autoheal", _heal)
        with step("Tap it"):
            _run_action(_Driver(), self._spec_for("click"), None, description="Cash on delivery")
        assert asked == [("Cash on delivery", "click")]

    def test_the_route_is_reported_as_a_heal(self, monkeypatch):
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=_El("healed"), by="id", value="v", dom_index=3),
        )
        with testmu_appium.capture_action_timings() as timings:
            with step("Tap it"):
                _run_action(_Driver(), self._spec_for("click"), None, description="Go")
        [timing] = timings
        assert timing["route"] == "heal_or_fallback"

    def test_heal_being_unavailable_does_not_unlock_the_recorded_point(self, monkeypatch):
        """The same rule the tree path applies: only an authoritative 404 says the
        element is gone, and nothing else licenses tapping a remembered position."""
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealUnavailable("heal is off"))
        calls = []
        with pytest.raises(ElementNotFound) as exc:
            with step("Tap it"):
                _run_action(
                    _Driver(), self._spec_for("click", calls), None,
                    description="Go", fallback_coordinates=BASIS,
                )
        assert "heal is off" in str(exc.value)
        assert calls == [], "an unconsulted heal is not evidence the element moved"

    def test_explicit_heal_off_replays_only_a_selectorless_recorded_point(self, monkeypatch):
        calls = []
        monkeypatch.setattr(_config, "heal", False)
        monkeypatch.setattr(
            _action_engine, "autoheal", lambda *a, **kw: pytest.fail("heal must not run"),
        )
        with step("Tap it"):
            result = _run_action(
                _Driver(), self._spec_for("click", calls), None,
                description="Go", fallback_coordinates=BASIS,
            )
        assert result == "tapped"
        assert calls == [(540, 585)]

    def test_explicit_heal_off_rejects_a_tree_miss_even_when_it_has_a_basis(
            self, monkeypatch):
        calls = []
        monkeypatch.setattr(_config, "heal", False)
        with pytest.raises(ElementNotFound, match="recorded selectors did not resolve"):
            _act(_Driver(), self._spec_for("click", calls), fallback_coordinates=BASIS)
        assert calls == []

    def test_smart_off_keeps_the_existing_unavailable_behavior(self, monkeypatch):
        calls = []
        monkeypatch.setattr(_config, "smart", False)
        monkeypatch.setattr(_config, "heal", True)
        monkeypatch.setattr(_action_engine, "autoheal", _heal.autoheal)
        with pytest.raises(ElementNotFound, match="TESTMU_SMART"):
            with step("Tap it"):
                _run_action(
                    _Driver(), self._spec_for("click", calls), None,
                    description="Go", fallback_coordinates=BASIS,
                )
        assert calls == []

    def test_an_undescribed_selectorless_action_is_still_producer_skew(self):
        """Nothing to find and nothing to name it: the generator should never
        have emitted this shape."""
        with pytest.raises(ValueError):
            with step("s"):
                _run_action(_Driver(), self._spec_for("click", []), None, description="")

    def test_an_undescribed_action_with_a_basis_still_replays_the_point(self, monkeypatch):
        """A basis with no description keeps working exactly as it did: there is no
        intent to re-ground, so the recorded ratio is all the recording ever had."""
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: pytest.fail("there is no description to heal from"),
        )
        calls = []
        with step("Tap the canvas"):
            result = _run_action(
                _Driver(), self._spec_for("click", calls), None,
                description="", fallback_coordinates=BASIS,
            )
        assert result == "tapped"
        assert calls == [(540, 585)]

    def test_two_selectorless_actions_in_one_step_get_their_own_heal_answer(self, monkeypatch):
        """The per-step heal cache is keyed on the recorded selectors, and every
        selectorless action shares the same empty tuple. Without the description in
        the key, the second action reads the first one's answer."""
        asked = []

        def _heal(driver, description, op_type, **kw):
            asked.append(description)
            return HealNoMatch("not on this screen")

        monkeypatch.setattr(_action_engine, "autoheal", _heal)
        with step("Two taps"):
            for description in ("Tap A", "Tap B"):
                with pytest.raises(ElementNotFound):
                    _run_action(_Driver(), self._spec_for("click"), None,
                                description=description)
        assert asked == ["Tap A", "Tap B"]


class TestWebSurface:
    """`surface="web"` routes the LOOKUP to the page's DOM. The gesture is the
    same Appium gesture the native path would have used."""

    PAGE = {"dpr": 3, "scale": 1.0, "offsetLeft": 0, "offsetTop": 0,
            "viewportWidth": 360, "viewportHeight": 780, "blockedUrls": [],
            "elements": [
                {"tag": "BUTTON", "label": "Go", "css": "#go", "path": "",
                 "dom_path": [{"kind": "element", "nodes": [0, 1]}],
                 "interactive": True, "editable": False, "states": [],
                 "x": 10, "y": 20, "w": 100, "h": 40},
                {"tag": "A", "label": "Terms", "css": "#terms", "path": "",
                 "dom_path": [{"kind": "element", "nodes": [0, 2]}],
                 "interactive": True, "editable": False, "states": [],
                 "x": 10, "y": 80, "w": 60, "h": 20}]}

    NATIVE = [{"text": "Go", "content_desc": "", "name": "Go",
               "bounds": (30, 310, 330, 430)},
              {"text": "Terms", "content_desc": "", "name": "Terms",
               "bounds": (30, 490, 210, 550)}]

    WEB_SELECTORS = [{"strategy": "css", "selector": "#go", "score": 90}]

    class _Channel:
        def __init__(self, page):
            self._page = page

        def read_page(self):
            return self._page

        def unreachable_frames(self, page, seen=()):
            return []

    @pytest.fixture(autouse=True)
    def _surface(self, monkeypatch):
        monkeypatch.setattr(
            _action_engine._tree, "parse_tree",
            lambda xml, width, height: list(self.NATIVE))
        monkeypatch.setattr(
            _action_engine._action_web, "open_web_surface",
            lambda native, package="": _action_web.open_surface(
                self._Channel(self.PAGE), native))

    def _web_act(self, driver, spec, **kw):
        with step("Tap Go"):
            return _run_action(driver, spec, self.WEB_SELECTORS,
                               description="Go button", surface="web", **kw)

    def _prepared(self):
        return {
            "surface": _action_web.open_surface(self._Channel(self.PAGE), self.NATIVE),
            "prepared_at": time.monotonic(),
            "package": "",
            "window": [1080, 2340],
            "session_id": None,
        }

    def test_a_current_prepared_web_target_skips_global_settle_and_recapture(
            self, monkeypatch):
        monkeypatch.setattr(
            _action_engine._action_web, "prepared_target_is_current",
            lambda surface, element: True,
        )
        monkeypatch.setattr(
            _action_engine, "_settle",
            lambda *args: pytest.fail("prepared web target must not globally settle"),
        )
        monkeypatch.setattr(
            _action_engine, "_open_web_surface",
            lambda *args: pytest.fail("prepared web target must not recapture"),
        )
        with testmu_appium.capture_action_timings() as timings:
            with use_authoring_web_surface(self._prepared()):
                assert self._web_act(
                    _Driver(), _spec(coord_runner=lambda *args: True),
                    grounded_by="tree",
                ) is True
        [timing] = timings
        assert timing["settle_strategy"] == "prepared_web_target"
        assert timing["web_surface_source"] == "prepared"
        assert timing["counts"].get("page_source_reads", 0) == 0

    def test_a_stale_prepared_web_target_falls_back_to_existing_safe_path(
            self, monkeypatch):
        settles = []
        monkeypatch.setattr(
            _action_engine._action_web, "prepared_target_is_current",
            lambda surface, element: False,
        )
        monkeypatch.setattr(
            _action_engine, "_settle",
            lambda *args: settles.append(True) or "<hierarchy settled='1'/>",
        )
        with testmu_appium.capture_action_timings() as timings:
            with use_authoring_web_surface(self._prepared()):
                assert self._web_act(
                    _Driver(), _spec(coord_runner=lambda *args: True),
                    grounded_by="tree",
                ) is True
        assert settles == [True]
        assert timings[0]["settle_strategy"] == "prepared_web_fallback_page_source"

    def test_prepared_web_surface_is_one_use(self, monkeypatch):
        validations = []
        settles = []
        monkeypatch.setattr(
            _action_engine._action_web, "prepared_target_is_current",
            lambda surface, element: validations.append(element["css"]) or True,
        )
        monkeypatch.setattr(
            _action_engine, "_settle",
            lambda *args: settles.append(True) or "<hierarchy settled='1'/>",
        )
        spec = _spec(coord_runner=lambda *args: True)
        with use_authoring_web_surface(self._prepared()):
            assert self._web_act(_Driver(), spec, grounded_by="tree") is True
            assert self._web_act(_Driver(), spec, grounded_by="tree") is True
        assert validations == ["#go"]
        assert settles == [True]

    def test_a_web_element_is_tapped_where_the_conversion_puts_it(self):
        tapped = []
        spec = _spec(coord_runner=lambda driver, x, y, ctx: tapped.append((x, y)) or True)
        assert self._web_act(_Driver(), spec) is True
        assert tapped == [(180, 370)]

    def test_the_native_lookup_never_runs_for_a_web_action(self):
        driver = _Driver(results={"#go": [_El("wrong")]})
        spec = _spec(coord_runner=lambda *a: True)
        self._web_act(driver, spec)
        assert driver.find_calls == []

    def test_an_unresolvable_web_selector_consults_heal(self, monkeypatch):
        calls = []
        monkeypatch.setattr(
            _action_engine, "autoheal_web",
            lambda *args, **kwargs: (
                calls.append((args[2], args[3]))
                or HealUnavailable("server unavailable")
            ),
        )
        spec = _spec(coord_runner=lambda *a: True)
        with pytest.raises(ElementNotFound, match="server unavailable"):
            with step("Tap Go"):
                _run_action(_Driver(), spec,
                            [{"strategy": "css", "selector": "#absent"}],
                            description="Go button", surface="web")
        assert calls == [("Go button", "click")]

    def test_explicit_heal_off_web_selector_miss_never_replays_a_point(self, monkeypatch):
        monkeypatch.setattr(_config, "heal", False)
        monkeypatch.setattr(
            _action_engine, "autoheal_web", lambda *a, **kw: pytest.fail("heal must not run"),
        )
        spec = _spec(
            coord_runner=lambda *a: pytest.fail("web selector misses never tap old points")
        )
        with pytest.raises(ElementNotFound, match="recorded web selectors did not resolve"):
            with step("Tap Go"):
                _run_action(
                    _Driver(), spec,
                    [{"strategy": "css", "selector": "#absent"}],
                    description="Go button", surface="web", fallback_coordinates=BASIS,
                )

    def test_a_web_heal_hit_re_resolves_the_private_descriptor_and_taps(
            self, monkeypatch):
        tapped = []
        descriptor = _action_web.descriptor_for(self.PAGE["elements"][0])
        monkeypatch.setattr(
            _action_engine, "autoheal_web",
            lambda *args, **kwargs: WebHealHit(descriptor, 1, "the Go button"),
        )
        spec = _spec(
            coord_runner=lambda driver, x, y, ctx: tapped.append((x, y)) or True
        )
        with step("Tap Go") as recorded:
            result = _run_action(
                _Driver(), spec,
                [{"strategy": "css", "selector": "#old-go"}],
                description="Go button", surface="web",
            )
        assert result is True
        assert tapped == [(180, 370)]
        assert recorded.is_autohealed is True
        assert recorded.autoheal_source == "v16-autoheal"

    def test_a_web_heal_404_never_unlocks_recorded_coordinates(
            self, monkeypatch):
        monkeypatch.setattr(
            _action_engine, "autoheal_web",
            lambda *args, **kwargs: HealNoMatch("no web match"),
        )
        spec = _spec(
            coord_runner=lambda *a: pytest.fail(
                "a web heal miss must not replay an old point"
            )
        )
        with pytest.raises(ElementNotFound, match="no web match"):
            with step("Tap Go"):
                _run_action(
                    _Driver(), spec,
                    [{"strategy": "css", "selector": "#old-go"}],
                    description="Go button",
                    surface="web",
                    fallback_coordinates=BASIS,
                )

    def test_a_working_web_selector_never_consults_heal(self, monkeypatch):
        monkeypatch.setattr(
            _action_engine, "autoheal_web",
            lambda *a, **kw: pytest.fail("working selectors must not heal"),
        )
        assert self._web_act(
            _Driver(), _spec(coord_runner=lambda *a: True)
        ) is True

    def test_type_css_miss_does_not_fall_back_to_same_named_label(
            self, monkeypatch):
        """An offscreen input is absent from ``surface.elements`` while its
        visible label may remain. Typing must fail closed instead of tapping the
        label and sending the secret to whichever input retained focus.
        """
        label = {
            "tag": "LABEL", "label": "Password", "css": "label", "path": "",
            "dom_path": [{"kind": "element", "nodes": [0, 8]}],
            "interactive": True, "editable": False, "states": [],
            "x": 10, "y": 500, "w": 120, "h": 30,
        }
        offscreen_input = {
            "tag": "INPUT", "label": "Password", "css": "#password", "path": "",
            "dom_path": [{"kind": "element", "nodes": [0, 9]}],
            "interactive": True, "editable": True, "states": [],
            "input_type": "password",
            "x": 10, "y": 900, "w": 250, "h": 40,
        }
        page = {**self.PAGE, "elements": [label, offscreen_input]}
        monkeypatch.setattr(
            _action_engine._action_web,
            "open_web_surface",
            lambda native, package="": _action_web.Surface(
                channel=self._Channel(page),
                elements=[label],
                all_elements=[label, offscreen_input],
                page=page,
                origin=(0, 250),
                twins={},
            ),
        )
        monkeypatch.setattr(
            _action_engine,
            "autoheal_web",
            lambda *args, **kwargs: HealUnavailable("password input is offscreen"),
        )
        acted = []
        with pytest.raises(ElementNotFound, match="password input is offscreen"):
            with step("Type Password"):
                _run_action(
                    _Driver(),
                    _spec(
                        op_type="type",
                        coord_runner=lambda *args: acted.append(args) or True,
                    ),
                    [
                        {"strategy": "css", "selector": "#password"},
                        {"strategy": "text", "selector": "Password"},
                    ],
                    description="Password field",
                    surface="web",
                )
        assert acted == []

    def test_a_cached_web_heal_still_re_resolves_a_fresh_surface(
            self, monkeypatch):
        descriptor = _action_web.descriptor_for(self.PAGE["elements"][0])
        consulted = []
        opened = []

        def heal(*args, **kwargs):
            consulted.append(True)
            return WebHealHit(descriptor, 1)

        original_open = _action_engine._open_web_surface

        def opened_surface(*args, **kwargs):
            opened.append(True)
            return original_open(*args, **kwargs)

        monkeypatch.setattr(_action_engine, "autoheal_web", heal)
        monkeypatch.setattr(_action_engine, "_open_web_surface", opened_surface)
        spec = _spec(coord_runner=lambda *a: True)
        selectors = [{"strategy": "css", "selector": "#old-go"}]
        with step("Tap Go"):
            assert _run_action(
                _Driver(), spec, selectors,
                description="Go button", surface="web",
            ) is True
            opens_after_first = len(opened)
            assert _run_action(
                _Driver(), spec, selectors,
                description="Go button", surface="web",
            ) is True
        assert consulted == [True]
        assert len(opened) > opens_after_first

    def test_an_expired_cached_heal_does_not_start_another_web_recapture(
            self, monkeypatch):
        class _Expired:
            @staticmethod
            def remaining_s():
                return 0.0

        monkeypatch.setattr(
            _action_engine, "read_cache", lambda key: {"dom_path": []}
        )
        monkeypatch.setattr(
            _action_engine, "_resolve_web_descriptor",
            lambda driver, descriptor, deadline=None: None,
        )
        monkeypatch.setattr(
            _action_engine, "_open_web_surface",
            lambda *args, **kwargs: pytest.fail(
                "an expired action must not start another CDP recapture"
            ),
        )
        with pytest.raises(ElementNotFound, match="deadline was exhausted"):
            _action_engine._heal_web_or_fail(
                _Driver(), _spec(coord_runner=lambda *a: True),
                self.WEB_SELECTORS, "Go button", "", ["css"], _Expired(),
            )

    def test_an_offscreen_healed_target_scrolls_then_uses_fresh_geometry(
            self, monkeypatch):
        offscreen = {
            **self.PAGE["elements"][0],
            "y": 1200,
        }
        onscreen = {
            **offscreen,
            "y": 200,
        }
        page = {**self.PAGE, "elements": [offscreen, self.PAGE["elements"][1]]}
        fresh_page = {**self.PAGE, "elements": [onscreen, self.PAGE["elements"][1]]}

        def surface_for(current, element):
            return _action_web.Surface(
                channel=self._Channel(current),
                elements=[element] if element["y"] < current["viewportHeight"] else [],
                all_elements=current["elements"],
                page=current,
                origin=(0, 250),
                twins={},
            )

        surfaces = [surface_for(page, offscreen), surface_for(fresh_page, onscreen)]
        scrolled = []
        monkeypatch.setattr(
            _action_engine, "_open_web_surface",
            lambda driver, page_source=None: surfaces.pop(0),
        )
        monkeypatch.setattr(
            _action_engine._action_web, "scroll_descriptor",
            lambda channel, descriptor: scrolled.append(descriptor) or "visible",
        )
        descriptor = _action_web.descriptor_for(offscreen)
        resolved_surface, resolved_element = (
            _action_engine._resolve_web_descriptor(_Driver(), descriptor)
        )
        assert scrolled == [descriptor]
        assert resolved_element["y"] == 200
        assert resolved_surface.page is fresh_page

    def test_a_screen_with_no_readable_page_says_so(self, monkeypatch):
        monkeypatch.setattr(_action_engine._action_web, "open_web_surface",
                            lambda native, package="": None)
        spec = _spec(coord_runner=lambda *a: True)
        with pytest.raises(ElementNotFound, match="no web page on this screen"):
            self._web_act(_Driver(), spec)

    def test_a_verb_that_cannot_act_on_a_point_refuses_the_action(self):
        """The scroll family deliberately has no coordinate runner; scrolling web
        content is the screen gesture it already was."""
        with pytest.raises(ValueError, match="cannot act on a point"):
            self._web_act(_Driver(), _spec(coord_runner=None))

    def test_the_step_records_the_web_element_it_acted_on(self):
        spec = _spec(coord_runner=lambda *a: True)
        with step("Tap Go") as recorded:
            _run_action(_Driver(), spec, self.WEB_SELECTORS,
                        description="Go button", surface="web")
        assert recorded.interacted_element["original_locator"] == "#go"
        assert recorded.interacted_element["center"] == [180, 370]
        assert recorded.interacted_element["bounds"] == [30, 310, 330, 430]

    def test_a_native_action_is_unaffected_by_the_branch(self):
        driver = _Driver(results={"com.app:id/go": [_El("primary")]})
        assert _act(driver) == ("ran", "primary")

    def test_the_app_on_screen_is_named_so_a_socket_can_be_bound_to_it(self, monkeypatch):
        """A WebView socket names its owning process; without the package every
        other app's WebView is a candidate and a stale one costs a timeout."""
        named = []
        monkeypatch.setattr(
            _action_engine._action_web, "open_web_surface",
            lambda native, package="": named.append(package) or _action_web.open_surface(
                self._Channel(self.PAGE), native))
        driver = _Driver()
        driver.current_package = "com.example.shop"
        self._web_act(driver, _spec(coord_runner=lambda *a: True))
        assert named == ["com.example.shop"]

    def test_an_unknown_surface_is_refused_rather_than_run_natively(self):
        """Looking for a DOM element in the view hierarchy finds nothing, slowly,
        and then heals — which is worse than saying the word is not a surface."""
        with pytest.raises(ValueError, match="unknown surface"):
            with step("Tap Go"):
                _run_action(_Driver(), _spec(), SELECTORS,
                            description="Go", surface="wev")

    def test_settling_hands_its_page_source_to_the_web_read(self, monkeypatch):
        """A page source costs ~2.4s on the reference device; settling has just
        read it twice."""
        monkeypatch.setattr(_action_engine, "_settle",
                            lambda driver, deadline: "<hierarchy settled=\'1\'/>")
        seen = []
        monkeypatch.setattr(_action_engine._tree, "parse_tree",
                            lambda xml, w, h: seen.append(xml) or list(self.NATIVE))
        self._web_act(
            _Driver(), _spec(coord_runner=lambda *a: True), grounded_by="tree",
        )
        assert seen == ["<hierarchy settled=\'1\'/>"]
