"""Tests for check_until_condition — local Selenium condition evaluator.

The Selenium V3 export evaluates generated Condition(...) expressions locally
(it must NOT call the V16 visual wait/check endpoint). A successfully-evaluated
condition returns its boolean. A condition that cannot be evaluated as a Python
expression (natural language, syntax error, unknown name) raises
ConditionEvaluationError instead of silently returning False, so a never-
evaluable condition fails loudly rather than exhausting the retry budget.
"""
from unittest.mock import MagicMock

import pytest

from testmu_selenium import set_var
from testmu_selenium._errors import ConditionEvaluationError
from testmu_selenium._helpers.wait import check_until_condition
from testmu_selenium._vars import clear_state


@pytest.fixture
def fake_driver():
    return MagicMock()


def _button_visible_eq_true():
    return (
        "Condition(conditions=[ResolvedCondition("
        "left_operand='{{five_second_button_visible}}', "
        "operator=PossibleCondition('=='), right_operand='true')], "
        "connectors=[]).evaluate({}, get_variable_value)[0]"
    )


class TestCheckUntilConditionLocalEval:
    def test_returns_true_when_condition_met(self, fake_driver):
        clear_state()
        set_var("five_second_button_visible", True)
        assert check_until_condition(fake_driver, _button_visible_eq_true()) is True
        fake_driver.get_screenshot_as_png.assert_not_called()

    def test_returns_false_when_condition_unmet(self, fake_driver):
        clear_state()
        set_var("five_second_button_visible", False)
        assert check_until_condition(fake_driver, _button_visible_eq_true()) is False
        fake_driver.get_screenshot_as_png.assert_not_called()

    def test_unresolved_variable_is_unmet_not_error(self, fake_driver):
        # A condition referencing a not-yet-set variable resolves to the literal
        # placeholder and compares unequal -> unmet (False), NOT an error. This
        # keeps legitimately-pending conditions retryable.
        clear_state()
        cond = (
            "Condition(conditions=[ResolvedCondition("
            "left_operand='{{never_set}}', operator=PossibleCondition('=='), "
            "right_operand='ready')], connectors=[]).evaluate({}, get_variable_value)[0]"
        )
        assert check_until_condition(fake_driver, cond) is False


class TestCheckUntilConditionRaisesOnUnevaluable:
    def test_natural_language_condition_raises(self, fake_driver):
        with pytest.raises(ConditionEvaluationError):
            check_until_condition(fake_driver, "spinner gone")

    def test_unknown_name_condition_raises(self, fake_driver):
        with pytest.raises(ConditionEvaluationError):
            check_until_condition(fake_driver, "SomeUndefinedThing() == 1")

    def test_syntax_error_condition_raises(self, fake_driver):
        with pytest.raises(ConditionEvaluationError):
            check_until_condition(fake_driver, "1 === not python")


class TestCheckUntilConditionConcatenationOperator:
    """Composite while-conditions bake ConcatenationOperator.AND/OR — the local
    eval sandbox must expose that name or every AND/OR while-loop raises."""

    def _and_condition(self, right_b: str) -> str:
        return (
            "Condition(conditions=["
            "ResolvedCondition(left_operand='{{a}}', operator=PossibleCondition('=='), right_operand='1'), "
            "ResolvedCondition(left_operand='{{b}}', operator=PossibleCondition('=='), right_operand='%s')"
            "], connectors=[ConcatenationOperator.AND], is_v3=True)"
            ".evaluate({}, get_variable_value)[0]" % right_b
        )

    def _or_condition(self, right_b: str) -> str:
        return (
            "Condition(conditions=["
            "ResolvedCondition(left_operand='{{a}}', operator=PossibleCondition('=='), right_operand='1'), "
            "ResolvedCondition(left_operand='{{b}}', operator=PossibleCondition('=='), right_operand='%s')"
            "], connectors=[ConcatenationOperator.OR], is_v3=True)"
            ".evaluate({}, get_variable_value)[0]" % right_b
        )

    def test_and_condition_true_when_both_hold(self, fake_driver):
        clear_state()
        set_var("a", 1)
        set_var("b", 2)
        assert check_until_condition(fake_driver, self._and_condition("2")) is True

    def test_and_condition_false_when_one_fails(self, fake_driver):
        clear_state()
        set_var("a", 1)
        set_var("b", 2)
        assert check_until_condition(fake_driver, self._and_condition("99")) is False

    def test_or_condition_true_when_one_holds(self, fake_driver):
        clear_state()
        set_var("a", 1)
        set_var("b", 2)
        assert check_until_condition(fake_driver, self._or_condition("99")) is True


class TestNoVisionEndpoint:
    """Regression guard: the V16 vision wait/check path stays removed."""

    def test_no_http_helper_or_host_referenced(self):
        from testmu_selenium._helpers import wait as wait_helper

        assert not hasattr(wait_helper, "make_http_request_with_retry")
        assert not hasattr(wait_helper, "_AI_API_HOST_DEFAULT")

    def test_screenshot_not_taken_for_condition(self, fake_driver):
        clear_state()
        set_var("five_second_button_visible", True)
        check_until_condition(fake_driver, _button_visible_eq_true())
        fake_driver.get_screenshot_as_png.assert_not_called()


def test_check_until_condition_exported_as_camelcase_alias():
    """Codegen emits the bare name `checkUntilCondition` in test.py."""
    import testmu_selenium

    assert hasattr(testmu_selenium, "checkUntilCondition")
    assert hasattr(testmu_selenium, "check_until_condition")
    assert testmu_selenium.checkUntilCondition is testmu_selenium.check_until_condition
