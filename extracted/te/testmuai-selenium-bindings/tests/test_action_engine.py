"""Tests for _run_action engine — find+heal+act loop in isolation.

Strategy: stub findElement and _heal_cascade at the module path used by
_action_engine so we exercise pure cascade/retry semantics without driver
or HTTP machinery.
"""
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

from testmu_selenium._action_engine import _ActionSpec, _run_action, _DEFAULT_HEAL_TIERS
from testmu_selenium._errors import AutohealExhausted, HealTierMiss
from testmu_selenium._heal_cascade import HealResult


PRIMARY = [{"selector": "#a", "isXPath": False}]
HEALED = [{"selector": "//a[@id='a']", "isXPath": True, "score": 50}]
XPATH_HEALED = [{"selector": "//*[@id='btn']", "isXPath": True, "score": 45}]


def _spec(runner, recoverable=(NoSuchElementException, StaleElementReferenceException, TimeoutException)):
    return _ActionSpec(runner=runner, recoverable_exceptions=recoverable)


# -----------------------------------------------------------------------------
# 1. Happy path
# -----------------------------------------------------------------------------

def test_happy_path_returns_runner_result():
    """First findElement succeeds, runner returns sentinel, no heal call."""
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    runner = MagicMock(return_value="OK")
    spec = _spec(runner)

    with patch("testmu_selenium._action_engine.findElement", return_value=el) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade") as m_heal:
        result = _run_action(driver, spec, PRIMARY, description="d")

    assert result == "OK"
    m_find.assert_called_once()
    runner.assert_called_once_with(el, {"driver": driver, "frame_info": None})
    m_heal.assert_not_called()


# -----------------------------------------------------------------------------
# 2. Recoverable -> heal succeeds -> retry succeeds
# -----------------------------------------------------------------------------

def test_recoverable_then_heal_then_success():
    """First call raises NoSuchElementException, heal returns new selector, second call succeeds."""
    driver = MagicMock(name="driver")
    el2 = MagicMock(name="el2")
    runner = MagicMock(return_value="DONE")
    spec = _spec(runner)

    heal_result = HealResult(selectors=HEALED, frame_info=None,
                             selector_payload=None, tier_used="LIST_XPATHS",
                             latency_ms=10)

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=[NoSuchElementException("miss"), el2]) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result) as m_heal, \
         patch("testmu_selenium._action_engine.time.sleep"):
        result = _run_action(driver, spec, PRIMARY, retry_delay=0)

    assert result == "DONE"
    assert m_find.call_count == 2
    m_heal.assert_called_once()
    runner.assert_called_once_with(el2, {"driver": driver, "frame_info": None})


# -----------------------------------------------------------------------------
# 3. Heal-rebind discriminating test — second findElement uses healed selector
# -----------------------------------------------------------------------------

def test_engine_rebinds_selector_from_heal_result():
    """Engine MUST pass heal_result.selectors to the next findElement call."""
    driver = MagicMock(name="driver")
    el2 = MagicMock(name="el2")
    runner = MagicMock(return_value="OK")
    spec = _spec(runner)

    heal_result = HealResult(selectors=HEALED, frame_info=["frame-x"],
                             selector_payload={"k": "v"}, tier_used="LIST_XPATHS",
                             latency_ms=5)

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=[StaleElementReferenceException("stale"), el2]) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result) as m_heal, \
         patch("testmu_selenium._action_engine.time.sleep"):
        _run_action(driver, spec, PRIMARY, description="login button", retry_delay=0)

    # First findElement: original selector
    first_args, first_kwargs = m_find.call_args_list[0]
    assert first_args[1] == PRIMARY
    # Second findElement: healed selector (rebind happened)
    second_args, second_kwargs = m_find.call_args_list[1]
    assert second_args[1] == HEALED
    assert second_args[1] is not PRIMARY  # genuinely new list
    # heal_cascade was passed the original selector + frame_info=None on first call
    heal_kwargs = m_heal.call_args.kwargs
    assert heal_kwargs["current_selector"] == PRIMARY
    assert heal_kwargs["current_frame_info"] is None
    assert heal_kwargs["driver"] is driver
    assert heal_kwargs["description"] == "login button"


# -----------------------------------------------------------------------------
# 4. autoheal=False propagates immediately
# -----------------------------------------------------------------------------

def test_autoheal_false_skips_heal_and_propagates():
    driver = MagicMock(name="driver")
    runner = MagicMock()
    spec = _spec(runner)

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=NoSuchElementException("miss")) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade") as m_heal:
        with pytest.raises(NoSuchElementException):
            _run_action(driver, spec, PRIMARY, autoheal=False)

    assert m_find.call_count == 1
    m_heal.assert_not_called()
    runner.assert_not_called()


# -----------------------------------------------------------------------------
# 5. max_attempts exhausted — last exception raised, heal called N-1 times
# -----------------------------------------------------------------------------

def test_max_attempts_exhausted_raises_last_exception():
    """4 attempts: heal called 3 times (attempts 0,1,2); attempt 3 raises without heal."""
    driver = MagicMock(name="driver")
    runner = MagicMock()
    spec = _spec(runner)

    heal_result = HealResult(selectors=HEALED, frame_info=None,
                             selector_payload=None, tier_used="LIST_XPATHS", latency_ms=1)

    final_exc = NoSuchElementException("final-miss")
    side = [
        NoSuchElementException("a"),
        NoSuchElementException("b"),
        NoSuchElementException("c"),
        final_exc,
    ]
    with patch("testmu_selenium._action_engine.findElement", side_effect=side) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result) as m_heal, \
         patch("testmu_selenium._action_engine.time.sleep"):
        with pytest.raises(NoSuchElementException) as excinfo:
            _run_action(driver, spec, PRIMARY, max_attempts=4, retry_delay=0)

    assert excinfo.value is final_exc
    assert m_find.call_count == 4
    assert m_heal.call_count == 3
    runner.assert_not_called()


# -----------------------------------------------------------------------------
# 6. Non-recoverable exception propagates immediately
# -----------------------------------------------------------------------------

def test_non_recoverable_exception_propagates_immediately():
    """ValueError isn't in spec.recoverable_exceptions → propagates with no heal."""
    driver = MagicMock(name="driver")
    runner = MagicMock()
    spec = _spec(runner, recoverable=(NoSuchElementException,))

    boom = ValueError("not recoverable")
    with patch("testmu_selenium._action_engine.findElement", side_effect=boom) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade") as m_heal:
        with pytest.raises(ValueError):
            _run_action(driver, spec, PRIMARY)

    assert m_find.call_count == 1
    m_heal.assert_not_called()


# -----------------------------------------------------------------------------
# 7. AutohealExhausted from heal cascade propagates
# -----------------------------------------------------------------------------

def test_autoheal_exhausted_propagates():
    driver = MagicMock(name="driver")
    runner = MagicMock()
    spec = _spec(runner)

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=NoSuchElementException("miss")), \
         patch("testmu_selenium._action_engine._heal_cascade",
               side_effect=AutohealExhausted(
                   original=NoSuchElementException("miss"),
                   last_miss=HealTierMiss("LIST_XPATHS", "no xpaths"),
               )):
        with pytest.raises(AutohealExhausted):
            _run_action(driver, spec, PRIMARY)


# -----------------------------------------------------------------------------
# 8. frame_info threading — heal returns new frame_info → next heal sees it
# -----------------------------------------------------------------------------

def test_final_raise_chains_original_exception():
    """On max-attempts exhaustion, the raised exception's __cause__ MUST be the
    FIRST recoverable exception (not the last) — preserves the most informative
    failure for on-call debugging."""
    driver = MagicMock(name="driver")
    runner = MagicMock()
    spec = _spec(runner)

    heal_result = HealResult(selectors=HEALED, frame_info=None,
                             selector_payload=None, tier_used="LIST_XPATHS", latency_ms=1)

    e1 = NoSuchElementException("first")
    e2 = NoSuchElementException("second")
    e3 = NoSuchElementException("third")
    e4 = NoSuchElementException("fourth")
    side = [e1, e2, e3, e4]
    with patch("testmu_selenium._action_engine.findElement", side_effect=side), \
         patch("testmu_selenium._action_engine._heal_cascade", return_value=heal_result), \
         patch("testmu_selenium._action_engine.time.sleep"):
        with pytest.raises(NoSuchElementException) as excinfo:
            _run_action(driver, spec, PRIMARY, max_attempts=4, retry_delay=0)

    assert excinfo.value is e4
    assert excinfo.value.__cause__ is e1
    assert excinfo.value.__cause__ is not e4


# -----------------------------------------------------------------------------
# 9. COORDINATE-tier heal — engine must dispatch to spec.coord_runner, NOT
#    feed synthetic placeholder selectors back into findElement.
#
# Pre-fix: the COORDINATE tier returned
#   selectors=[{"selector": "coord:0.5,0.5", "isXPath": False, "score": 30}]
# and _run_action blindly rebound that into the next findElement call,
# crashing Chrome with InvalidSelectorException ("invalid selector").
#
# Post-fix contract: HealResult.coordinates carries the resolved viewport
# pixel coords; HealResult.selectors stays empty for COORDINATE tier; engine
# dispatches to spec.coord_runner(driver, x, y, ctx) when coordinates are
# present and skips findElement.
# -----------------------------------------------------------------------------

def test_coordinate_tier_dispatches_to_coord_runner_not_findelement():
    """Heal returns HealResult.coordinates → engine calls spec.coord_runner,
    NEVER calls findElement again with a synthetic 'coord:...' placeholder."""
    driver = MagicMock(name="driver")
    runner = MagicMock(return_value="should-not-be-called")
    coord_runner = MagicMock(return_value="COORD_OK")
    spec = _ActionSpec(runner=runner, coord_runner=coord_runner)

    heal_result = HealResult(
        selectors=[],
        coordinates=(388, 202),
        selector_payload={"response_coordinates": [388, 202]},
        tier_used="COORDINATE",
        latency_ms=1,
    )

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=[NoSuchElementException("primary miss"), Exception("must not be called")]) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result), \
         patch("testmu_selenium._action_engine.time.sleep"):
        result = _run_action(driver, spec, PRIMARY, retry_delay=0)

    assert result == "COORD_OK"
    assert m_find.call_count == 1, (
        "findElement must NOT be called again after COORDINATE heal — pre-fix "
        "regression: synthetic 'coord:0.5,0.5' selector propagated to Chrome."
    )
    coord_runner.assert_called_once()
    coord_args, coord_kwargs = coord_runner.call_args
    assert coord_args[0] is driver
    assert coord_args[1] == 388
    assert coord_args[2] == 202
    runner.assert_not_called()


def test_coordinate_tier_without_coord_runner_raises_typed_error():
    """Spec without coord_runner + COORDINATE heal → typed error, NEVER a
    Chrome InvalidSelectorException leaking through. Pins R5 contract:
    HealResult.selectors must always be actionable; no synthetic placeholders."""
    driver = MagicMock(name="driver")
    runner = MagicMock()
    spec = _ActionSpec(runner=runner)  # no coord_runner

    heal_result = HealResult(
        selectors=[],
        coordinates=(388, 202),
        tier_used="COORDINATE",
        latency_ms=1,
    )

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=NoSuchElementException("primary miss")), \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result), \
         patch("testmu_selenium._action_engine.time.sleep"):
        with pytest.raises(NotImplementedError, match="coord_runner"):
            _run_action(driver, spec, PRIMARY, retry_delay=0)

    runner.assert_not_called()


def test_heal_result_selectors_must_never_contain_coord_placeholder():
    """Class-level invariant — pin per dev guideline R5/Pattern 11: every
    HealResult.selectors entry must be a real CSS/XPath findElement can
    consume. Synthetic 'coord:...' placeholders are an anti-pattern.

    If a future tier regresses and emits a synthetic non-actionable selector
    instead of using HealResult.coordinates, the engine will pass it to
    findElement and Chrome will reject it. This test pins the contract at
    the consumer boundary so the regression surfaces here, not in cluster
    code-validation logs."""
    driver = MagicMock(name="driver")
    runner = MagicMock()
    spec = _spec(runner)

    bad_result = HealResult(
        selectors=[{"selector": "coord:0.5,0.5", "isXPath": False, "score": 30}],
        tier_used="COORDINATE",
        latency_ms=1,
    )

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=[NoSuchElementException("miss"), MagicMock()]) as m_find, \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=bad_result), \
         patch("testmu_selenium._action_engine.time.sleep"):
        # Either the engine refuses the synthetic shape with a typed error,
        # or it dispatches to coord_runner — but it MUST NOT pass the
        # placeholder string back into findElement.
        try:
            _run_action(driver, spec, PRIMARY, retry_delay=0)
        except (NotImplementedError, ValueError, AssertionError):
            pass  # any typed rejection is acceptable
        except Exception:
            raise

    if m_find.call_count >= 2:
        second_call_selector = m_find.call_args_list[1].args[1]
        for s in second_call_selector or []:
            assert "coord:" not in str(s.get("selector", "")), (
                f"Engine fed synthetic placeholder back into findElement: {s}"
            )


def test_frame_info_threaded_into_subsequent_heal_call():
    """When heal returns frame_info, the engine threads it through to the next
    heal call's current_frame_info kwarg."""
    driver = MagicMock(name="driver")
    el3 = MagicMock(name="el3")
    runner = MagicMock(return_value="K")
    spec = _spec(runner)

    heal1 = HealResult(selectors=HEALED, frame_info=["iframe-1"],
                       selector_payload=None, tier_used="LIST_XPATHS", latency_ms=1)
    heal2 = HealResult(selectors=[{"selector": "#z", "isXPath": False}],
                       frame_info=["iframe-2"],
                       selector_payload=None, tier_used="TEXTUAL_QUERY", latency_ms=1)

    side = [NoSuchElementException("a"), NoSuchElementException("b"), el3]
    with patch("testmu_selenium._action_engine.findElement", side_effect=side), \
         patch("testmu_selenium._action_engine._heal_cascade",
               side_effect=[heal1, heal2]) as m_heal, \
         patch("testmu_selenium._action_engine.time.sleep"):
        _run_action(driver, spec, PRIMARY, max_attempts=4, retry_delay=0)

    # First heal call: frame_info=None
    first_kwargs = m_heal.call_args_list[0].kwargs
    assert first_kwargs["current_frame_info"] is None
    # Second heal call: frame_info from heal1
    second_kwargs = m_heal.call_args_list[1].kwargs
    assert second_kwargs["current_frame_info"] == ["iframe-1"]
    # Second heal call also sees the rebound selector from heal1
    assert second_kwargs["current_selector"] == HEALED
    # Final runner call carries the latest frame_info (from heal2)
    runner_ctx = runner.call_args.args[1]
    assert runner_ctx["frame_info"] == ["iframe-2"]


# -----------------------------------------------------------------------------
# TEXTUAL_QUERY is not a relocate tier — only the textual_query action's
# _direct_textual_read uses the textual-query endpoint. Element actions
# (click/type/search/hover/...) heal via COORDINATE -> VISION_QUERY (both
# vision-grounded). LIST_XPATHS was dropped from the default: as the only
# non-vision tier it re-ranks DOM xpaths and returns plausible-but-wrong matches
# that turn real failures into false PASSes (see the _DEFAULT_HEAL_TIERS comment).
# -----------------------------------------------------------------------------

def test_default_heal_tiers_excludes_textual_query():
    """The shared relocate cascade default must not contain TEXTUAL_QUERY, and must
    not contain LIST_XPATHS (dropped — the non-vision tier produced false-positive
    relocates). Default is DESKTOP_LOCATE only — the unified viewport resolver
    replaces the legacy COORDINATE+VISION_QUERY pair."""
    assert "TEXTUAL_QUERY" not in _DEFAULT_HEAL_TIERS
    assert "LIST_XPATHS" not in _DEFAULT_HEAL_TIERS
    assert "COORDINATE" not in _DEFAULT_HEAL_TIERS
    assert "VISION_QUERY" not in _DEFAULT_HEAL_TIERS
    assert list(_DEFAULT_HEAL_TIERS) == ["DESKTOP_LOCATE"]


def test_default_tiers_passed_to_heal_exclude_textual_query():
    """When tiers is None, the engine forwards the default relocate tiers to the
    heal cascade — TEXTUAL_QUERY must not be among them, so click/type/etc.
    never trigger textual-query autoheal."""
    driver = MagicMock(name="driver")
    el2 = MagicMock(name="el2")
    runner = MagicMock(return_value="OK")
    spec = _spec(runner)

    heal_result = HealResult(selectors=HEALED, frame_info=None,
                             selector_payload=None, tier_used="VISION_QUERY",
                             latency_ms=1)

    with patch("testmu_selenium._action_engine.findElement",
               side_effect=[NoSuchElementException("miss"), el2]), \
         patch("testmu_selenium._action_engine._heal_cascade",
               return_value=heal_result) as m_heal, \
         patch("testmu_selenium._action_engine.time.sleep"):
        _run_action(driver, spec, PRIMARY, retry_delay=0)  # tiers=None -> default

    passed_tiers = m_heal.call_args.kwargs["tiers"]
    assert "TEXTUAL_QUERY" not in passed_tiers
    assert "LIST_XPATHS" not in passed_tiers
    assert "COORDINATE" not in passed_tiers
    assert "VISION_QUERY" not in passed_tiers
    assert list(passed_tiers) == ["DESKTOP_LOCATE"]


class TestSmartWaitWiring:
    def test_smart_wait_runs_once_before_first_find(self):
        driver = MagicMock(name="driver")
        el = MagicMock(name="element")
        runner = MagicMock(return_value="OK")
        spec = _spec(runner)
        order = []
        sw_instance = MagicMock(name="SmartWait-inst")
        sw_instance.smart_wait.side_effect = lambda **k: order.append(("smart_wait", k))

        def _find(*a, **k):
            order.append(("find",))
            return el

        with patch("testmu_selenium._action_engine.findElement", side_effect=_find), \
             patch("testmu_selenium._action_engine.SmartWait", return_value=sw_instance) as m_sw:
            assert _run_action(driver, spec, PRIMARY) == "OK"
        m_sw.assert_called_once_with(driver)
        sw_instance.smart_wait.assert_called_once_with(is_vision=False)
        assert order == [("smart_wait", {"is_vision": False}), ("find",)]

    def test_smart_wait_runs_in_vision_query(self):
        sw_inst = MagicMock(name="SmartWait-inst")
        with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=sw_inst), \
             patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": True}
            from testmu_selenium import visionQuery
            visionQuery("is x visible?", "bool")
        sw_inst.smart_wait.assert_called_once_with(is_vision=True)

    def test_smart_wait_runs_in_textual_query(self):
        sw_inst = MagicMock(name="SmartWait-inst")
        driver = MagicMock(name="driver")
        with patch("testmu_selenium._helpers.textual_query.SmartWait", return_value=sw_inst), \
             patch("testmu_selenium._helpers.textual_query.findElement", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.textual_query._extract_value", return_value="X"):
            from testmu_selenium._helpers.textual_query import textualQuery
            textualQuery(driver, selector=[{"selector": "#a", "isXPath": False}],
                         selected_attribute_name="text")
        sw_inst.smart_wait.assert_called_once_with(is_vision=False)


class TestIsRetryLog:
    def test_is_retry_false_then_true(self, caplog):
        driver = MagicMock(name="driver")
        el = MagicMock(name="element")
        runner = MagicMock(return_value="OK")
        spec = _spec(runner)
        heal_result = HealResult(selectors=HEALED, frame_info=None, tier_used="LIST_XPATHS")
        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=[NoSuchElementException("miss"), el]), \
             patch("testmu_selenium._action_engine._heal_cascade", return_value=heal_result), \
             patch("testmu_selenium._action_engine.SmartWait"), \
             patch("testmu_selenium._action_engine.time.sleep"), \
             caplog.at_level("INFO"):
            assert _run_action(driver, spec, PRIMARY) == "OK"
        assert "is_retry: False" in caplog.text
        assert "is_retry: True" in caplog.text


class TestHealOutcomeLog:
    def test_logs_autoheal_state_and_resolved_tier(self, caplog):
        driver = MagicMock(name="driver")
        el = MagicMock(name="element")
        runner = MagicMock(return_value="OK")
        spec = _spec(runner)
        heal_result = HealResult(selectors=HEALED, frame_info=None, tier_used="LIST_XPATHS")
        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=[NoSuchElementException("miss"), el]), \
             patch("testmu_selenium._action_engine._heal_cascade", return_value=heal_result), \
             patch("testmu_selenium._action_engine.SmartWait"), \
             patch("testmu_selenium._action_engine.time.sleep"), \
             caplog.at_level("INFO"):
            assert _run_action(driver, spec, PRIMARY) == "OK"
        assert "[AutoHeal] autoheal=True" in caplog.text
        assert "[AutoHeal] relocated via LIST_XPATHS" in caplog.text
        assert caplog.text.count("[AutoHeal] autoheal=") == 1

    def test_logs_coordinate_relocation(self, caplog):
        driver = MagicMock(name="driver")
        runner = MagicMock(return_value="ignored")
        coord_runner = MagicMock(return_value="COORD-OK")
        spec = _ActionSpec(runner=runner, coord_runner=coord_runner)
        heal_result = HealResult(selectors=[], frame_info=None, tier_used="COORDINATE",
                                 coordinates=(12, 34))
        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=NoSuchElementException("miss")) as m_find, \
             patch("testmu_selenium._action_engine._heal_cascade", return_value=heal_result), \
             patch("testmu_selenium._action_engine.SmartWait"), \
             patch("testmu_selenium._action_engine.time.sleep"), \
             caplog.at_level("INFO"):
            assert _run_action(driver, spec, PRIMARY) == "COORD-OK"
        assert "[AutoHeal] relocated via COORDINATE -> coordinates (12, 34)" in caplog.text
        assert m_find.call_count == 1
        assert "-> coordinates" in caplog.text and "relocated via COORDINATE ->" in caplog.text


class TestStepAutoHealMark:
    def test_heal_marks_active_step(self, caplog):
        from testmu_selenium._step import step, _current_step
        driver = MagicMock(name="driver")
        el = MagicMock(name="element")
        runner = MagicMock(return_value="OK")
        spec = _spec(runner)
        heal_result = HealResult(selectors=HEALED, frame_info=None, tier_used="LIST_XPATHS")
        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=[NoSuchElementException("miss"), el]), \
             patch("testmu_selenium._action_engine._heal_cascade", return_value=heal_result), \
             patch("testmu_selenium._action_engine.SmartWait"), \
             patch("testmu_selenium._action_engine.time.sleep"), \
             caplog.at_level("INFO"):
            with step("Type into box") as info:
                _run_action(driver, spec, PRIMARY)
                assert info.auto_heal is True
        assert "auto_heal=True" in caplog.text


# =============================================================================
# Task 3 — selector-first dispatch, pending coord fallback, fallback_coordinates
# =============================================================================

class TestDerivedXpathDispatch:
    def test_both_populated_heal_xpath_succeeds(self):
        """Heal returns selectors+coordinates; engine retries findElement with
        derived xpath; xpath runner succeeds → runner result returned;
        coord_runner NOT called."""
        driver = MagicMock(name="driver")
        el2 = MagicMock(name="el2")
        runner = MagicMock(return_value="XPATH_OK")
        coord_runner = MagicMock(return_value="SHOULD_NOT_REACH")
        spec = _ActionSpec(runner=runner, coord_runner=coord_runner)

        heal_result = HealResult(
            selectors=XPATH_HEALED,
            coordinates=(100, 200),
            tier_used="DESKTOP_LOCATE",
            latency_ms=1,
        )

        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=[NoSuchElementException("miss"), el2]) as m_find, \
             patch("testmu_selenium._action_engine._heal_cascade",
                   return_value=heal_result) as m_heal, \
             patch("testmu_selenium._action_engine.time.sleep"):
            result = _run_action(driver, spec, PRIMARY, retry_delay=0)

        assert result == "XPATH_OK"
        assert m_find.call_count == 2
        m_heal.assert_called_once()
        coord_runner.assert_not_called()
        runner.assert_called_once_with(el2, {"driver": driver, "frame_info": None})

    def test_both_populated_heal_xpath_fails_uses_coords(self):
        """findElement with derived xpath fails → coord_runner called with the
        heal round's coordinates; _heal_cascade called exactly ONCE. The engine
        rebinds frame_info from the heal round before the pending dispatch, so
        coord_runner's ctx must carry the round's frame_info."""
        driver = MagicMock(name="driver")
        runner = MagicMock(return_value="SHOULD_NOT_REACH")
        coord_runner = MagicMock(return_value="COORD_FALLBACK")
        spec = _ActionSpec(runner=runner, coord_runner=coord_runner)

        heal_result = HealResult(
            selectors=XPATH_HEALED,
            coordinates=(100, 200),
            frame_info=["iframe-x"],
            tier_used="DESKTOP_LOCATE",
            latency_ms=1,
        )

        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=[NoSuchElementException("miss1"),
                                 NoSuchElementException("miss2")]) as m_find, \
             patch("testmu_selenium._action_engine._heal_cascade",
                   return_value=heal_result) as m_heal, \
             patch("testmu_selenium._action_engine.time.sleep"):
            result = _run_action(driver, spec, PRIMARY, retry_delay=0)

        assert result == "COORD_FALLBACK"
        assert m_find.call_count == 2
        m_heal.assert_called_once()
        coord_args, _ = coord_runner.call_args
        assert coord_args[0] is driver
        assert coord_args[1] == 100
        assert coord_args[2] == 200
        # Pin frame_info rebinding: ctx carries the heal round's frame_info.
        assert coord_args[3]["frame_info"] == ["iframe-x"]
        runner.assert_not_called()


class TestFallbackCoordinates:
    def test_autoheal_exhausted_with_fallback_coordinates(self):
        """_heal_cascade raises AutohealExhausted; fallback_coordinates=(7, 9) →
        coord_runner called with (7, 9)."""
        driver = MagicMock(name="driver")
        runner = MagicMock()
        coord_runner = MagicMock(return_value="RECORDED_COORD")
        spec = _ActionSpec(runner=runner, coord_runner=coord_runner)

        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=NoSuchElementException("miss")), \
             patch("testmu_selenium._action_engine._heal_cascade",
                   side_effect=AutohealExhausted(
                       original=NoSuchElementException("miss"),
                       last_miss=HealTierMiss("DESKTOP_LOCATE", "api miss [0,0]"),
                   )):
            result = _run_action(driver, spec, PRIMARY, fallback_coordinates=(7, 9))

        assert result == "RECORDED_COORD"
        coord_args, _ = coord_runner.call_args
        assert coord_args[0] is driver
        assert coord_args[1] == 7
        assert coord_args[2] == 9

    def test_autoheal_exhausted_without_fallback_coordinates(self):
        """No fallback_coordinates → AutohealExhausted propagates."""
        driver = MagicMock(name="driver")
        runner = MagicMock()
        coord_runner = MagicMock()
        spec = _ActionSpec(runner=runner, coord_runner=coord_runner)

        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=NoSuchElementException("miss")), \
             patch("testmu_selenium._action_engine._heal_cascade",
                   side_effect=AutohealExhausted(
                       original=NoSuchElementException("miss"),
                       last_miss=HealTierMiss("DESKTOP_LOCATE", "api miss [0,0]"),
                   )):
            with pytest.raises(AutohealExhausted):
                _run_action(driver, spec, PRIMARY)

        coord_runner.assert_not_called()

    def test_fallback_coordinates_not_consumed_on_cascade_success(self):
        """Cascade returns a working selector → runner result; coord_runner not
        called even though fallback_coordinates was provided."""
        driver = MagicMock(name="driver")
        el2 = MagicMock(name="el2")
        runner = MagicMock(return_value="SELECTOR_OK")
        coord_runner = MagicMock(return_value="SHOULD_NOT_REACH")
        spec = _ActionSpec(runner=runner, coord_runner=coord_runner)

        heal_result = HealResult(
            selectors=HEALED,
            frame_info=None,
            selector_payload=None,
            tier_used="LIST_XPATHS",
            latency_ms=1,
        )

        with patch("testmu_selenium._action_engine.findElement",
                   side_effect=[NoSuchElementException("miss"), el2]), \
             patch("testmu_selenium._action_engine._heal_cascade",
                   return_value=heal_result), \
             patch("testmu_selenium._action_engine.time.sleep"):
            result = _run_action(driver, spec, PRIMARY, fallback_coordinates=(7, 9),
                                 retry_delay=0)

        assert result == "SELECTOR_OK"
        coord_runner.assert_not_called()

    @pytest.mark.parametrize("module,fn_name,extra_args,extra_kwargs", [
        ("testmu_selenium._action_click", "click", (), {}),
        ("testmu_selenium._action_hover", "hover", (), {}),
        ("testmu_selenium._action_type", "type", ("hello",), {}),
        ("testmu_selenium._action_clear", "clear", (), {}),
        # Non-empty selector skips set_input_files' selectorless DOM-first
        # pre-step, so _run_action is hit directly — no extra mocking needed.
        ("testmu_selenium._action_set_input_files", "set_input_files", (),
         {"file_path": "/tmp/upload.txt"}),
    ])
    def test_public_wrappers_forward_fallback_coordinates(
            self, module, fn_name, extra_args, extra_kwargs):
        """Every public verb owning a coord_runner forwards fallback_coordinates
        to _run_action as a NAMED kwarg — must NOT leak into runner_kwargs/ctx."""
        import importlib
        driver = MagicMock(name="driver")

        with patch(f"{module}._run_action") as m_run:
            m_run.return_value = True
            fn = getattr(importlib.import_module(module), fn_name)
            fn(driver, PRIMARY, *extra_args, description="add to cart",
               fallback_coordinates=(7, 9), **extra_kwargs)

        m_run.assert_called_once()
        assert m_run.call_args.kwargs.get("fallback_coordinates") == (7, 9), (
            "fallback_coordinates must be forwarded as a named kwarg to _run_action"
        )
