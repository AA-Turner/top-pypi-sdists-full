"""Tests for testmu_selenium.drag_drop wrapper.

V2-parity sentinel: gesture sequence must match the explicit ActionChains chain
with the (0.1, 0.1) drop-zone-activation jiggle from the V2 drag implementation.
Reverting to ActionChains.drag_and_drop() shortcut MUST fail these tests.

Heal path (spec §10.1): selector-list endpoints resolve per-endpoint
(findElement → DESKTOP_LOCATE with drop_aware=<is_target> → resolve_coordinate),
then dispatch the legacy element gesture (both elements) or the V2
ActionBuilder coordinate gesture (any coordinate endpoint). Heal is mocked at
the module boundary — no live HTTP.
"""
from unittest.mock import MagicMock, patch, call

import pytest
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from testmu_selenium._action_drag_drop import drag_drop
from testmu_selenium._errors import AutohealExhausted, HealTierMiss
from testmu_selenium._helpers._coordinate_resolver import ResolvedTarget

M = "testmu_selenium._action_drag_drop"

SRC_SEL = [{"selector": "#src", "isXPath": False}]
TGT_SEL = [{"selector": "#tgt", "isXPath": False}]


def _make_fluent_chain():
    """MagicMock that returns itself on chained-method calls."""
    chain = MagicMock()
    for method in ("move_to_element", "click_and_hold", "move_by_offset",
                   "release"):
        getattr(chain, method).return_value = chain
    return chain


@patch("testmu_selenium._action_drag_drop.ActionChains")
def test_drag_drop_emits_v2_parity_gesture_sequence(mock_action_chains):
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain

    driver = MagicMock(name="driver")
    src = MagicMock(name="source_element")
    tgt = MagicMock(name="target_element")

    drag_drop(driver, src, tgt)

    mock_action_chains.assert_called_once_with(driver)
    assert chain.method_calls == [
        call.move_to_element(src),
        call.click_and_hold(src),
        call.move_to_element(tgt),
        call.move_by_offset(0.1, 0.1),
        call.release(),
        call.perform(),
    ]


@patch("testmu_selenium._action_drag_drop.ActionChains")
def test_drag_drop_takes_webelements_not_selectors(mock_action_chains):
    """drag_drop wrapper must accept already-resolved WebElements,
    not raw selectors. Heal happens upstream in FindElementNode's emit."""
    chain = _make_fluent_chain()
    mock_action_chains.return_value = chain

    driver = MagicMock(name="driver")
    # WebElements are already-resolved objects — wrapper should not
    # try to resolve them through findElement / heal.
    src = MagicMock(name="source_element")
    tgt = MagicMock(name="target_element")

    drag_drop(driver, src, tgt)

    # Sentinel: src and tgt are passed as-is into move_to_element.
    chain.move_to_element.assert_any_call(src)
    chain.move_to_element.assert_any_call(tgt)


def test_drag_drop_is_publicly_exported():
    import testmu_selenium
    assert hasattr(testmu_selenium, "drag_drop")
    assert "drag_drop" in testmu_selenium.__all__


# =============================================================================
# Spec §10.1 — heal-capable selector-pair form
# =============================================================================

# V2 coordinate pointer gesture, as ab.pointer_action method calls.
def _coord_gesture_calls(src_xy, tgt_xy):
    return [
        call.move_to_location(src_xy[0], src_xy[1]),
        call.pointer_down(),
        call.pause(0.1),
        call.move_to_location(tgt_xy[0], tgt_xy[1]),
        call.pause(0.1),
        call.pointer_up(),
    ]


class TestWebElementShapeByteParity:
    def test_webelement_pair_never_constructs_heal_and_ignores_heal_kwargs(self):
        """WebElement pair → legacy gesture; Heal never constructed; findElement
        never called — even when heal kwargs are supplied (they are ignored)."""
        chain = _make_fluent_chain()
        driver = MagicMock(name="driver")
        src = MagicMock(name="source_element")
        tgt = MagicMock(name="target_element")

        with patch(f"{M}.ActionChains", return_value=chain) as m_ac, \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.findElement") as m_find:
            drag_drop(driver, src, tgt,
                      source_description="src", target_description="tgt",
                      fallback_coordinates=((1, 2), (3, 4)))

        m_heal.assert_not_called()
        m_find.assert_not_called()
        m_ac.assert_called_once_with(driver)
        assert chain.method_calls == [
            call.move_to_element(src),
            call.click_and_hold(src),
            call.move_to_element(tgt),
            call.move_by_offset(0.1, 0.1),
            call.release(),
            call.perform(),
        ]


class TestDragDropEndpointResolution:
    def test_per_endpoint_heal_sequential_and_drop_aware_flags(self):
        """Both lookups fail → source healed first (drop_aware=False), then
        target (drop_aware=True); each Heal carries that endpoint's intent."""
        driver = MagicMock(name="driver")

        with patch(f"{M}.findElement",
                   side_effect=NoSuchElementException("miss")), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate", return_value=None), \
             patch(f"{M}.ActionBuilder"), \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.side_effect = [(100, 110), (300, 310)]
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src card", target_description="drop zone")

        locate_calls = m_heal.return_value.desktop_locate.call_args_list
        assert locate_calls == [call(drop_aware=False), call(drop_aware=True)]
        actions = [c.args[0] for c in m_heal.call_args_list]
        assert actions[0]["operation_intent"] == "src card"
        assert actions[1]["operation_intent"] == "drop zone"
        # Heal constructed with the driver positionally, like _heal_cascade.
        assert all(c.args[1] is driver for c in m_heal.call_args_list)

    def test_heal_derived_xpath_becomes_element_endpoint(self):
        """resolve_coordinate derives an xpath → endpoint re-looked-up via
        findElement with the verified-xpath selector shape → element gesture."""
        driver = MagicMock(name="driver")
        src_healed_el = MagicMock(name="src_healed_el")
        tgt_el = MagicMock(name="tgt_el")
        chain = _make_fluent_chain()

        with patch(f"{M}.findElement",
                   side_effect=[NoSuchElementException("miss"), src_healed_el,
                                tgt_el]) as m_find, \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate",
                   return_value=ResolvedTarget(xpath="//*[@id='x']", meta={})), \
             patch(f"{M}.ActionChains", return_value=chain), \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.return_value = (100, 110)
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt")

        # Second findElement call consumes the derived-xpath selector shape.
        xpath_call = m_find.call_args_list[1]
        assert xpath_call.args[1] == [{"selector": "//*[@id='x']", "isXPath": True}]
        # Both endpoints are elements → legacy chain, no coordinate gesture.
        m_ab.assert_not_called()
        assert chain.method_calls == [
            call.move_to_element(src_healed_el),
            call.click_and_hold(src_healed_el),
            call.move_to_element(tgt_el),
            call.move_by_offset(0.1, 0.1),
            call.release(),
            call.perform(),
        ]

    def test_derived_xpath_relookup_failure_falls_back_to_same_round_coords(self):
        """resolve_coordinate derives an xpath but the re-lookup misses → the
        SAME round's healed coordinates carry the gesture; no extra locate."""
        driver = MagicMock(name="driver")
        driver.execute_script.return_value = [50.0, 60.0, 1280, 720]
        src_el = MagicMock(name="src_el")

        with patch(f"{M}.findElement",
                   side_effect=[src_el, NoSuchElementException("miss"),
                                NoSuchElementException("xpath-gone")]) as m_find, \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate",
                   return_value=ResolvedTarget(xpath="//*[@id='t']", meta={})), \
             patch(f"{M}.ActionChains") as m_ac, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.return_value = (300, 310)
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt")

        # ONE locate round serves both derivation and fallback coords.
        m_heal.return_value.desktop_locate.assert_called_once_with(drop_aware=True)
        # Third findElement call consumed the derived-xpath shape and missed.
        assert m_find.call_args_list[2].args[1] == [
            {"selector": "//*[@id='t']", "isXPath": True}]
        # Coordinate gesture at the healed coords; no legacy chain.
        m_ac.assert_not_called()
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((50, 60), (300, 310))

    def test_mixed_webelement_source_selector_target_heals_target_only(self):
        """Mixed shape: WebElement source passes through unresolved/unhealed;
        selector target heals; gesture matrix applies (element center + coords)."""
        driver = MagicMock(name="driver")
        driver.execute_script.return_value = [50.0, 60.0, 1280, 720]
        src_el = MagicMock(name="source_webelement")

        with patch(f"{M}.findElement",
                   side_effect=NoSuchElementException("miss")) as m_find, \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate", return_value=None), \
             patch(f"{M}.ActionChains") as m_ac, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.return_value = (300, 310)
            drag_drop(driver, src_el, TGT_SEL, target_description="drop zone")

        # Only the target endpoint goes through lookup/heal.
        m_find.assert_called_once()
        assert m_find.call_args.args[1] == TGT_SEL
        m_heal.assert_called_once()
        m_heal.return_value.desktop_locate.assert_called_once_with(drop_aware=True)
        assert m_heal.call_args.args[0]["operation_intent"] == "drop zone"
        # Gesture matrix: WebElement converts via rect center; target coords.
        m_ac.assert_not_called()
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((50, 60), (300, 310))

    def test_autoheal_false_raises_lookup_error_without_heal(self):
        """autoheal=False → lookup error propagates; Heal never constructed."""
        driver = MagicMock(name="driver")

        with patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.ActionBuilder") as m_ab:
            with pytest.raises(NoSuchElementException):
                drag_drop(driver, [], [], source_description="src",
                          target_description="tgt", autoheal=False)

        m_heal.assert_not_called()
        m_ab.assert_not_called()


class TestDragDropGestureMatrix:
    def test_element_element_uses_legacy_chain(self):
        """Both selector endpoints resolve via findElement → legacy element
        gesture; Heal never constructed."""
        driver = MagicMock(name="driver")
        src_el = MagicMock(name="src_el")
        tgt_el = MagicMock(name="tgt_el")
        chain = _make_fluent_chain()

        with patch(f"{M}.findElement", side_effect=[src_el, tgt_el]), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.ActionChains", return_value=chain) as m_ac, \
             patch(f"{M}.ActionBuilder") as m_ab:
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt")

        m_heal.assert_not_called()
        m_ab.assert_not_called()
        m_ac.assert_called_once_with(driver)
        assert chain.method_calls == [
            call.move_to_element(src_el),
            call.click_and_hold(src_el),
            call.move_to_element(tgt_el),
            call.move_by_offset(0.1, 0.1),
            call.release(),
            call.perform(),
        ]

    def test_element_coord_converts_element_to_rect_center(self):
        """Source element + target coords → coordinate gesture; the element
        endpoint converts to viewport coords via its rect center."""
        driver = MagicMock(name="driver")
        driver.execute_script.return_value = [50.0, 60.0, 1280, 720]
        src_el = MagicMock(name="src_el")

        with patch(f"{M}.findElement",
                   side_effect=[src_el, NoSuchElementException("miss")]), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate", return_value=None), \
             patch(f"{M}.ActionChains") as m_ac, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.return_value = (300, 310)
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt")

        m_ac.assert_not_called()
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((50, 60), (300, 310))
        ab.perform.assert_called_once()

    def test_coord_element_clamps_element_center_to_viewport(self):
        """Source coords + target element; an off-viewport rect center is
        clamped to [0, viewport_dim-1]."""
        driver = MagicMock(name="driver")
        driver.execute_script.return_value = [1500.0, -8.0, 1280, 720]
        tgt_el = MagicMock(name="tgt_el")

        with patch(f"{M}.findElement",
                   side_effect=[NoSuchElementException("miss"), tgt_el]), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate", return_value=None), \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.return_value = (100, 110)
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt")

        m_heal.return_value.desktop_locate.assert_called_once_with(drop_aware=False)
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((100, 110), (1279, 0))

    def test_coord_coord_uses_both_healed_coordinates(self):
        """Both endpoints heal to coordinates → pure V2 pointer gesture."""
        driver = MagicMock(name="driver")

        with patch(f"{M}.findElement",
                   side_effect=NoSuchElementException("miss")), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate", return_value=None), \
             patch(f"{M}.ActionChains") as m_ac, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.side_effect = [(100, 110), (300, 310)]
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt")

        m_ac.assert_not_called()
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((100, 110), (300, 310))


class TestDragDropStash:
    def test_stashed_coords_reused_without_relocate(self):
        """Attempt 1: target healed (xpath element, fresh coords stashed);
        element gesture fails recoverably. Attempt 2: target endpoint comes
        from the stash — NO second Heal construction / locate call."""
        driver = MagicMock(name="driver")
        driver.execute_script.return_value = [50.0, 60.0, 1280, 720]
        src_el = MagicMock(name="src_el")
        tgt_healed_el = MagicMock(name="tgt_healed_el")
        chain = _make_fluent_chain()
        chain.perform.side_effect = StaleElementReferenceException("stale")

        with patch(f"{M}.findElement",
                   side_effect=[src_el, NoSuchElementException("miss"),
                                tgt_healed_el, src_el]) as m_find, \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate",
                   return_value=ResolvedTarget(xpath="//*[@id='t']", meta={})), \
             patch(f"{M}.ActionChains", return_value=chain), \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.return_value = (300, 310)
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt")

        # ONE locate call total — attempt 2 consumed the stash.
        m_heal.assert_called_once()
        m_heal.return_value.desktop_locate.assert_called_once()
        # Attempt 2: source re-looked-up (4 findElement calls), target from stash.
        assert m_find.call_count == 4
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((50, 60), (300, 310))


class TestDragDropFallbackCoordinates:
    FALLBACK = ((10, 20), (30, 40))

    def test_fallback_not_consulted_on_success(self):
        """First attempt succeeds → stored pair never dispatched."""
        driver = MagicMock(name="driver")
        src_el = MagicMock(name="src_el")
        tgt_el = MagicMock(name="tgt_el")
        chain = _make_fluent_chain()

        with patch(f"{M}.findElement", side_effect=[src_el, tgt_el]), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.ActionChains", return_value=chain), \
             patch(f"{M}.ActionBuilder") as m_ab:
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt",
                      fallback_coordinates=self.FALLBACK)

        m_heal.assert_not_called()
        m_ab.assert_not_called()

    def test_heal_tier_miss_with_fallback_dispatches_stored_pair(self):
        """Locate misses ([0,0] → HealTierMiss) → ONE final coordinate gesture
        with the stored pair; no AutohealExhausted."""
        driver = MagicMock(name="driver")

        with patch(f"{M}.findElement",
                   side_effect=NoSuchElementException("miss")), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate") as m_resolve, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.side_effect = HealTierMiss(
                "DESKTOP_LOCATE", "element not found")
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt",
                      fallback_coordinates=self.FALLBACK)

        m_resolve.assert_not_called()
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((10, 20), (30, 40))

    def test_heal_tier_miss_without_fallback_raises_autoheal_exhausted(self):
        driver = MagicMock(name="driver")

        with patch(f"{M}.findElement",
                   side_effect=NoSuchElementException("miss")), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            miss = HealTierMiss("DESKTOP_LOCATE", "element not found")
            m_heal.return_value.desktop_locate.side_effect = miss
            with pytest.raises(AutohealExhausted) as exc_info:
                drag_drop(driver, SRC_SEL, TGT_SEL,
                          source_description="src", target_description="tgt")

        assert exc_info.value.last_miss is miss
        m_ab.assert_not_called()

    def test_max_attempts_exhaustion_with_fallback_dispatches_stored_pair(self):
        """Every element-gesture attempt fails recoverably → exhaustion → one
        final stored-pair coordinate gesture (no locate calls at all)."""
        driver = MagicMock(name="driver")
        src_el = MagicMock(name="src_el")
        tgt_el = MagicMock(name="tgt_el")
        chain = _make_fluent_chain()
        chain.perform.side_effect = StaleElementReferenceException("stale")
        finds = [src_el, tgt_el] * 3

        with patch(f"{M}.findElement", side_effect=finds), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.ActionChains", return_value=chain), \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            drag_drop(driver, SRC_SEL, TGT_SEL,
                      source_description="src", target_description="tgt",
                      max_attempts=3, fallback_coordinates=self.FALLBACK)

        assert chain.perform.call_count == 3
        m_heal.assert_not_called()
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((10, 20), (30, 40))

    def test_max_attempts_exhaustion_without_fallback_raises_autoheal_exhausted(self):
        driver = MagicMock(name="driver")
        src_el = MagicMock(name="src_el")
        tgt_el = MagicMock(name="tgt_el")
        chain = _make_fluent_chain()
        first = StaleElementReferenceException("first-stale")
        chain.perform.side_effect = [first,
                                     StaleElementReferenceException("stale"),
                                     StaleElementReferenceException("stale")]

        with patch(f"{M}.findElement", side_effect=[src_el, tgt_el] * 3), \
             patch(f"{M}.ActionChains", return_value=chain), \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            with pytest.raises(AutohealExhausted) as exc_info:
                drag_drop(driver, SRC_SEL, TGT_SEL,
                          source_description="src", target_description="tgt",
                          max_attempts=3)

        assert exc_info.value.original is first
        m_ab.assert_not_called()

    def test_final_fallback_gesture_failure_propagates(self):
        """The stored-pair gesture's OWN failure propagates as-is — it is the
        true last resort, never re-wrapped or retried."""
        driver = MagicMock(name="driver")
        boom = StaleElementReferenceException("fallback-gesture-failed")

        with patch(f"{M}.findElement",
                   side_effect=NoSuchElementException("miss")), \
             patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.side_effect = HealTierMiss(
                "DESKTOP_LOCATE", "element not found")
            m_ab.return_value.perform.side_effect = boom
            with pytest.raises(StaleElementReferenceException) as exc_info:
                drag_drop(driver, SRC_SEL, TGT_SEL,
                          source_description="src", target_description="tgt",
                          fallback_coordinates=self.FALLBACK)

        assert exc_info.value is boom


class TestDragDropHealInfraFailure:
    """Heal-infrastructure exceptions (transport errors after retries,
    malformed JSON, screenshot/driver failures inside desktop_locate) must
    convert to HealTierMiss — mirroring the engine cascade
    (_heal_cascade.py tier-exception conversion) — so the exhaustion path
    still consults fallback_coordinates during an Automind outage."""

    FALLBACK = ((10, 20), (30, 40))

    def test_infra_exception_with_fallback_dispatches_stored_pair(self):
        """Marked drag + locate transport failure → ONE stored-pair gesture;
        the raw infrastructure exception must NOT escape."""
        driver = MagicMock(name="driver")

        with patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.resolve_coordinate") as m_resolve, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.side_effect = ConnectionError(
                "automind unreachable after retries")
            drag_drop(driver, [], [], source_description="src",
                      target_description="tgt",
                      fallback_coordinates=self.FALLBACK)

        m_resolve.assert_not_called()
        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((10, 20), (30, 40))

    def test_infra_exception_without_fallback_raises_autoheal_exhausted(self):
        """No stored pair → AutohealExhausted (NOT the raw transport error),
        with the converted DESKTOP_LOCATE miss chained from it."""
        driver = MagicMock(name="driver")
        boom = ConnectionError("automind unreachable after retries")

        with patch(f"{M}.Heal") as m_heal, \
             patch(f"{M}.ActionBuilder") as m_ab, \
             patch(f"{M}.time.sleep"):
            m_heal.return_value.desktop_locate.side_effect = boom
            with pytest.raises(AutohealExhausted) as exc_info:
                drag_drop(driver, [], [], source_description="src",
                          target_description="tgt")

        assert isinstance(exc_info.value.last_miss, HealTierMiss)
        assert "automind unreachable" in str(exc_info.value.last_miss)
        assert exc_info.value.last_miss.__cause__ is boom
        m_ab.assert_not_called()


class TestDragDropEmptyDescription:
    def test_empty_description_on_failed_endpoint_exhausts(self):
        """Empty selectors + empty description → real Heal.desktop_locate
        raises HealTierMiss (empty intent) before any screenshot/HTTP →
        exhaustion path → AutohealExhausted (no fallback)."""
        driver = MagicMock(name="driver")

        with pytest.raises(AutohealExhausted) as exc_info:
            drag_drop(driver, [], [], source_description="",
                      target_description="")

        assert isinstance(exc_info.value.last_miss, HealTierMiss)
        assert "empty operation_intent" in str(exc_info.value.last_miss)

    def test_empty_description_with_fallback_dispatches_stored_pair(self):
        driver = MagicMock(name="driver")

        with patch(f"{M}.ActionBuilder") as m_ab:
            drag_drop(driver, [], [], source_description="",
                      target_description="",
                      fallback_coordinates=((10, 20), (30, 40)))

        ab = m_ab.return_value
        assert ab.pointer_action.method_calls == _coord_gesture_calls((10, 20), (30, 40))
