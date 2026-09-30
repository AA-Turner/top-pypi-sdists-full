"""batched fast-find collapses a ranked locator walk into one call.

The ranked lists this binding receives run to a dozen-plus candidates, and each
native miss is its own WebDriver round-trip; on a remote grid that is real
latency for an element the first JS pass would have found.

Port of V2 (_fast_find_locators).

Deliberately conservative: only candidates scoring >= 80 are eligible, scoped
finds are excluded, and ANY miss/exception falls back to the untouched native
loop — so the fast path can save time but can never be the reason an element is
not found.
"""
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import NoSuchElementException

from testmu_selenium._helpers import find_element as fe
from testmu_selenium._helpers.find_element import _FAST_FIND_MIN_SCORE, _fast_find, findElement

HIGH = [{"selector": "#a", "isXPath": False, "score": 95},
        {"selector": "//b", "isXPath": True, "score": 85}]
LOW = [{"selector": "#a", "isXPath": False, "score": 50}]
UNSCORED = [{"selector": "#a", "isXPath": False}]


# ---------------------------------------------------------------------------
# _fast_find eligibility
# ---------------------------------------------------------------------------

def test_batches_only_candidates_at_or_above_the_score_floor():
    driver = MagicMock(name="driver")
    driver.execute_script.return_value = "ELEMENT"
    mixed = HIGH + LOW
    assert _fast_find(driver, mixed) == "ELEMENT"
    batch = driver.execute_script.call_args.args[1]
    assert [b["selector"] for b in batch] == ["#a", "//b"]  # the score-50 one is excluded


@pytest.mark.parametrize("selectors", [[], LOW, UNSCORED, [{"selector": "#a", "score": True}]])
def test_ineligible_lists_never_reach_the_browser(selectors):
    driver = MagicMock(name="driver")
    assert _fast_find(driver, selectors) is None
    driver.execute_script.assert_not_called()


def test_a_bool_score_is_not_a_number():
    # bool is an int subclass; True >= 80 is False but a sloppy check could
    # still admit it. Pin that it is rejected as unscored.
    driver = MagicMock(name="driver")
    assert _fast_find(driver, [{"selector": "#a", "score": True}]) is None


def test_candidates_without_a_selector_are_dropped():
    driver = MagicMock(name="driver")
    driver.execute_script.return_value = None
    _fast_find(driver, [{"selector": "", "score": 90}, {"selector": "#b", "score": 90}])
    batch = driver.execute_script.call_args.args[1]
    assert [b["selector"] for b in batch] == ["#b"]


def test_a_script_failure_falls_back_rather_than_raising():
    driver = MagicMock(name="driver")
    driver.execute_script.side_effect = RuntimeError("javascript error")
    assert _fast_find(driver, HIGH) is None


def test_isxpath_is_normalised_to_a_real_bool():
    driver = MagicMock(name="driver")
    driver.execute_script.return_value = None
    _fast_find(driver, [{"selector": "//a", "isXPath": "true", "score": 90}])
    assert driver.execute_script.call_args.args[1][0]["isXPath"] is True


# ---------------------------------------------------------------------------
# findElement integration
# ---------------------------------------------------------------------------

def test_a_fast_hit_skips_the_native_walk():
    driver = MagicMock(name="driver")
    with patch.object(fe, "_fast_find", return_value="FAST") as m_fast:
        assert findElement(driver, HIGH) == "FAST"
    m_fast.assert_called_once()
    driver.find_element.assert_not_called()


def test_a_fast_miss_runs_the_native_walk_unchanged():
    driver = MagicMock(name="driver")
    driver.find_element.return_value = "NATIVE"
    with patch.object(fe, "_fast_find", return_value=None):
        assert findElement(driver, HIGH) == "NATIVE"
    driver.find_element.assert_called()


def test_scoped_finds_skip_the_fast_path_entirely():
    """A search_root constrains resolution to that subtree; the JS scope rules
    cannot reproduce that faithfully, so scoped finds stay native."""
    driver = MagicMock(name="driver")
    root = MagicMock(name="search_root")
    root.find_element.return_value = "SCOPED"
    with patch.object(fe, "_fast_find") as m_fast:
        assert findElement(driver, HIGH, search_root=root) == "SCOPED"
    m_fast.assert_not_called()


def test_empty_selectors_still_raise_the_recoverable_not_found():
    driver = MagicMock(name="driver")
    with patch.object(fe, "_fast_find", return_value=None):
        with pytest.raises(NoSuchElementException):
            findElement(driver, [])


def test_score_floor_is_eighty():
    assert _FAST_FIND_MIN_SCORE == 80
