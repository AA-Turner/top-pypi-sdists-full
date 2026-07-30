"""Deeper coverage for testmu_selenium._helpers.input_value.

The helper is a verbatim port from the code generator framework. These tests exercise
public surfaces using MagicMock driver/element instances. We avoid asserting
on internal call ordering beyond what the ported behavior requires.
"""
from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium._helpers import input_value as iv_module
from testmu_selenium._helpers.input_value import (
    SET_SELECTION_RANGE_ELIGIBLE_INPUT,
    _coerce_scalar_to_str,
    _is_numeric_input,
    add_input_value_to_webelement,
    input_value,
)


class TestIsNumericInputPureHelper:
    """_is_numeric_input is the only pure helper — exercise it directly."""

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("12345", True),
            ("123-45", True),
            ("12/34/2025", True),
            ("+1-202-555", True),
            ("3.14", True),
            ("abc", False),
            ("123abc", False),
            ("", False),
            (None, False),
        ],
    )
    def test_is_numeric_input(self, text, expected):
        assert _is_numeric_input(text) is expected


class TestSetSelectionRangeEligibleInputs:
    def test_eligible_list_matches_v2_parity(self):
        # Stable contract — codegen relies on this set for caret-move strategy.
        assert SET_SELECTION_RANGE_ELIGIBLE_INPUT == [
            "text", "password", "search", "tel", "url",
        ]


class TestInputValueCoordsPath:
    """coords-not-None routes to ActionChains/ActionBuilder — no element interaction."""

    def test_coords_path_uses_action_chains_and_returns_none(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()

        with patch.object(iv_module, "ActionChains") as mock_ac, patch.object(
            iv_module, "ActionBuilder"
        ) as mock_ab, patch.object(iv_module, "time") as mock_time:
            mock_time.sleep.return_value = None

            result = input_value(
                mock_element, mock_driver, "hello", coords=(100, 200)
            )

        assert result is None
        # ActionChains used once for the click-at-coordinates step.
        mock_ac.assert_called_once_with(mock_driver)
        # ActionBuilder used twice: clear (BACKSPACE * 50), then send value.
        assert mock_ab.call_count == 2
        # Element is untouched in the coords path.
        mock_element.click.assert_not_called()
        mock_element.send_keys.assert_not_called()


class TestInputValueElementPathHappy:
    """Element-path happy case: focus, type, value-matches → no JS fallback."""

    def test_element_path_sends_value_to_focused_element(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()

        focused = MagicMock()
        # Focused element behaves like a plain text input that echoes the value.
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "tagName": "input",
            "value": "hello",
        }.get(name)

        # The element under test is also a text input — _move_to_start_of_input
        # will see tagName=input, type=text and call setSelectionRange(0,0).
        mock_element.get_attribute.side_effect = lambda name: {
            "type": "text",
        }.get(name, "")

        # driver.execute_script is invoked from _clear, _move_to_start_of_input,
        # etc.  Return shape varies — return a dict that satisfies both the
        # tagName/type lookup and the placeholder/autocomplete lookup.
        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                return {"tagName": "input", "type": "text"}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            # arguments[0].value lookup in _clear:
            return ""

        mock_driver.execute_script.side_effect = exec_script

        # WebDriverWait(...).until(...) — patch to short-circuit to focused.
        with patch.object(iv_module, "WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = focused

            result = input_value(mock_element, mock_driver, "hello")

        assert result is None
        # focused element received the typed value.
        focused.send_keys.assert_any_call("hello")
        # clickElement (focus cascade) was attempted.
        mock_element.clickElement.assert_called_once()


class TestInputValueElementPathEmptyValue:
    """Empty value should not crash the element path."""

    def test_empty_value_does_not_raise(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "text"

        focused = MagicMock()
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "tagName": "input",
            "value": "",
        }.get(name)

        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                return {"tagName": "input", "type": "text"}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            return ""

        mock_driver.execute_script.side_effect = exec_script

        with patch.object(iv_module, "WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = focused
            result = input_value(mock_element, mock_driver, "")

        assert result is None


class TestInputValueMonthBranch:
    """type='month' → split MMYYYY into month / TAB / year."""

    def test_month_input_sends_month_tab_year(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "month"

        focused = MagicMock()
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "tagName": "input",
            "value": "",
        }.get(name)

        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                # _move_to_start_of_input for the focused element.
                return {"tagName": "input", "type": "month"}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            return ""

        mock_driver.execute_script.side_effect = exec_script

        with patch.object(iv_module, "WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = focused
            result = input_value(mock_element, mock_driver, "032025")

        assert result is None
        # 3 calls: month "03", Keys.TAB sentinel, year "2025".
        assert focused.send_keys.call_count == 3
        first_call_arg = focused.send_keys.call_args_list[0].args[0]
        third_call_arg = focused.send_keys.call_args_list[2].args[0]
        assert first_call_arg == "03"
        assert third_call_arg == "2025"


class TestInputValueDateManualInteraction:
    """type='date' + manual_interaction_tag set → js value-set path."""

    def test_date_with_manual_tag_sets_value_via_js(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "date"

        focused = MagicMock()
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "tagName": "input",
            "value": "",
        }.get(name)

        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                return {"tagName": "input", "type": "date"}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            return ""

        mock_driver.execute_script.side_effect = exec_script

        with patch.object(iv_module, "WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = focused
            result = input_value(
                mock_element,
                mock_driver,
                "2025-04-30",
                manual_interaction_tag="manual",
            )

        assert result is None
        # Confirm at least one execute_script call is the value-set form.
        scripts = [c.args[0] for c in mock_driver.execute_script.call_args_list]
        assert any("arguments[0].value = arguments[1];" in s for s in scripts)


class TestInputValueMaxlengthPerChar:
    """maxlength==1 multi-char (OTP/PIN boxes) -> per-char send_keys, no JS fallback.

    Each OTP box is a separate <input maxlength=1>; the widget auto-advances
    focus on input. Typing the full value as one bulk send_keys leaves only the
    first char in box 1 and triggers the destructive js-native write-back, which
    corrupts the widget. The per-char path follows auto-advance focus between
    boxes instead, and must never hit the fallback.
    """

    def test_otp_maxlength_one_types_per_char_no_js_fallback(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.side_effect = lambda name: {
            "type": "text",
        }.get(name, "")

        focused = MagicMock()
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "maxlength": "1",
            "tagName": "input",
            "value": "1",
        }.get(name)

        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                return {"tagName": "input", "type": "text"}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            return ""

        mock_driver.execute_script.side_effect = exec_script

        with patch.object(iv_module, "WebDriverWait") as mock_wait, patch.object(
            iv_module, "_perform_js_native_input"
        ) as mock_js:
            mock_wait.return_value.until.return_value = focused
            result = input_value(mock_element, mock_driver, "123456")

        assert result is None
        # One send_keys per character — per-char auto-advance path.
        assert focused.send_keys.call_count == 6
        sent = [c.args[0] for c in focused.send_keys.call_args_list]
        assert sent == ["1", "2", "3", "4", "5", "6"]
        # Destructive js-native write-back must NOT fire for OTP boxes.
        mock_js.assert_not_called()


class TestCoerceScalarToStr:
    """Contract: int/float/bool -> str (bool -> 'True'/'False'); str/None
    pass through; dict/list are left unchanged (not coerced)."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            (42, "42"),
            (0, "0"),
            (-7, "-7"),
            (3.14, "3.14"),
            (True, "True"),
            (False, "False"),
            ("hello", "hello"),
            ("", ""),
        ],
    )
    def test_scalar_coerced(self, value, expected):
        assert _coerce_scalar_to_str(value) == expected

    def test_none_passes_through(self):
        assert _coerce_scalar_to_str(None) is None

    def test_dict_not_coerced(self):
        d = {"a": 1}
        assert _coerce_scalar_to_str(d) is d

    def test_list_not_coerced(self):
        items = [1, 2]
        assert _coerce_scalar_to_str(items) is items


class TestInputValueScalarCoercion:
    """Numeric/bool variables (from execute_js/set_var/var(), which preserve
    type) must be coerced to str at the input_value entry so the month split,
    per-char, coords and send_keys branches never hit string ops on a non-str.
    """

    def test_int_value_month_branch_types_coerced_string(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "month"

        focused = MagicMock()
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "tagName": "input",
            "value": "",
        }.get(name)

        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                return {"tagName": "input", "type": "month"}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            return ""

        mock_driver.execute_script.side_effect = exec_script

        with patch.object(iv_module, "WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = focused
            result = input_value(mock_element, mock_driver, 122025)

        assert result is None
        # int -> "122025" -> month "12", TAB, year "2025".
        assert focused.send_keys.call_count == 3
        assert focused.send_keys.call_args_list[0].args[0] == "12"
        assert focused.send_keys.call_args_list[2].args[0] == "2025"

    def test_int_value_coords_path_sends_coerced_string(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()

        with patch.object(iv_module, "ActionChains"), patch.object(
            iv_module, "ActionBuilder"
        ) as mock_ab, patch.object(iv_module, "time"):
            input_value(mock_element, mock_driver, 123, coords=(10, 20))

        # The value-typing ActionBuilder delivers the coerced string, not the int.
        mock_ab.return_value.key_action.send_keys.assert_any_call("123")


class TestInputValueRejectsStructuralValue:
    """dict/list must FAIL LOUDLY at the fill boundary — never silently
    stringified or iterated char-by-char by send_keys. Scalars still coerce."""

    def test_dict_coords_path_raises_typeerror_before_typing(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()

        with patch.object(iv_module, "ActionChains"), patch.object(
            iv_module, "ActionBuilder"
        ) as mock_ab, patch.object(iv_module, "time"):
            with pytest.raises(TypeError) as exc:
                input_value(mock_element, mock_driver, {"a": 1}, coords=(10, 20))

        # Error names the offending type.
        assert "dict" in str(exc.value)
        # No typing occurred — guard fired before the ActionBuilder send.
        mock_ab.return_value.key_action.send_keys.assert_not_called()

    def test_list_coords_path_raises_typeerror(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()

        with patch.object(iv_module, "ActionChains"), patch.object(
            iv_module, "ActionBuilder"
        ), patch.object(iv_module, "time"):
            with pytest.raises(TypeError) as exc:
                input_value(mock_element, mock_driver, [1, 2, 3], coords=(10, 20))

        assert "list" in str(exc.value)

    def test_dict_element_path_raises_and_never_send_keys(self):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.side_effect = lambda name: {
            "type": "text",
        }.get(name, "")

        focused = MagicMock()
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "tagName": "input",
            "value": "",
        }.get(name)

        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                return {"tagName": "input", "type": "text"}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            return ""

        mock_driver.execute_script.side_effect = exec_script

        with patch.object(iv_module, "WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = focused
            with pytest.raises(TypeError) as exc:
                input_value(mock_element, mock_driver, {"a": 1})

        assert "dict" in str(exc.value)
        # The dict was never iterated into send_keys.
        focused.send_keys.assert_not_called()


class TestInputValueMonkeyPatch:
    """add_input_value_to_webelement attaches a method named input_value."""

    def test_add_input_value_to_webelement_installs_method(self):
        from selenium.webdriver.remote.webelement import WebElement

        # Snapshot then install — clean up after.
        prior = getattr(WebElement, "input_value", None)
        try:
            add_input_value_to_webelement()
            assert callable(WebElement.input_value)
            # Signature accepts the documented kwargs without TypeError.
            assert WebElement.input_value.__name__ == "input_value_method"
        finally:
            if prior is None:
                delattr(WebElement, "input_value")
            else:
                WebElement.input_value = prior
