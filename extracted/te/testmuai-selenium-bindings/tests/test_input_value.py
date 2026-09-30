"""Deeper coverage for testmu_selenium._helpers.input_value.

The helper is a verbatim port from the code generator framework. These tests exercise
public surfaces using MagicMock driver/element instances. We avoid asserting
on internal call ordering beyond what the ported behavior requires.
"""
from unittest.mock import MagicMock, patch

import pytest
from selenium.webdriver.common.keys import Keys

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
            ("0412 345 678", True),  # V2: whitespace allowed
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


class TestInputValueNumericPerChar:
    """V2: a numeric value (phone/OTP/date) is typed char-by-char
    even on a plain input, so masked/numeric inputs accept it."""

    def _run(self, value, element_type="text", after_input=None):
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.get_attribute.side_effect = lambda name: {"type": element_type}.get(name, "")
        focused = MagicMock()
        focused.get_attribute.side_effect = lambda name: {
            "pattern": None,
            "tagName": "input",
            "value": value if after_input is None else after_input,
        }.get(name)

        def exec_script(script, *args):
            if "tagName" in script and "type" in script:
                return {"tagName": "input", "type": element_type}
            if "placeholder" in script:
                return {"placeholder": "", "autocomplete": ""}
            return ""

        mock_driver.execute_script.side_effect = exec_script
        with patch.object(iv_module, "WebDriverWait") as mock_wait, \
                patch.object(iv_module, "_perform_js_native_input") as mock_js:
            mock_wait.return_value.until.return_value = focused
            input_value(mock_element, mock_driver, value)
        sent = [c.args[0] for c in focused.send_keys.call_args_list]
        # _move_to_start_of_input walks a date/time caret back with 10 ARROW_LEFT
        # before anything is typed; those are not part of the value.
        sent = [k for k in sent if k != Keys.ARROW_LEFT]
        return sent, mock_js

    def test_spaced_phone_number_typed_per_char(self):
        sent, _ = self._run("04 12")
        assert sent == ["0", "4", " ", "1", "2"]

    def test_text_value_typed_in_bulk(self):
        sent, _ = self._run("hello")
        assert sent == ["hello"]

    def test_iso_date_not_typed_per_char_on_date_input(self):
        """An ISO date reads as numeric, but a date input's segments are not
        filled left-to-right by raw keystrokes, so V2 excludes type=date from
        the per-char branch. Guarding this keeps the value in one send_keys."""
        sent, _ = self._run("2030-01-01", element_type="date")
        assert sent == ["2030-01-01"]

    def test_iso_date_falls_back_to_native_setter_when_field_rejects_it(self):
        """The whole point of routing a date through the else branch: when the
        keystrokes do not land the value, the write-back check sets it through
        the native setter, which takes the ISO form."""
        _, mock_js = self._run("2030-01-01", element_type="date", after_input="")
        assert [c.args[2] for c in mock_js.call_args_list] == ["", "2030-01-01"]

    def test_numeric_date_still_typed_per_char_on_a_text_input(self):
        """The exclusion is keyed on the element, not the value — a masked text
        field still gets the per-char treatment the numeric branch exists for."""
        sent, _ = self._run("12/34/2025")
        assert sent == list("12/34/2025")


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


# ---------------------------------------------------------------------------
# Don't reset the Selection on an EMPTY contenteditable
#
# selectNodeContents + DELETE wipes the editor's pending toolbar marks: a user
# who clicks Bold on an empty editor has formatting armed but no text, and
# re-selecting the range drops it (@buddyboss.com — "Clear being performed on an
# empty text field"). On an empty editor the clear achieves nothing anyway.
# ---------------------------------------------------------------------------

class TestContentEditableEmptyGuard:
    def test_empty_editor_reports_no_text(self):
        drv = MagicMock()
        drv.execute_script.return_value = False
        assert iv_module._contenteditable_has_text(drv, MagicMock()) is False

    def test_populated_editor_reports_text(self):
        drv = MagicMock()
        drv.execute_script.return_value = True
        assert iv_module._contenteditable_has_text(drv, MagicMock()) is True

    def test_probe_failure_errs_towards_clearing(self):
        """Leaving stale text behind corrupts the typed value — worse than
        losing a pending mark."""
        drv = MagicMock()
        drv.execute_script.side_effect = RuntimeError("stale element")
        assert iv_module._contenteditable_has_text(drv, MagicMock()) is True

    def test_empty_editor_skips_the_selection_reset(self):
        el = MagicMock()
        el.get_attribute.side_effect = lambda n: "true" if n == "contenteditable" else None
        drv = MagicMock()
        # value probe -> "", textContent probe -> False (empty editor)
        drv.execute_script.side_effect = ["", False]
        iv_module._clear(drv, el)
        scripts = [c.args[0] for c in drv.execute_script.call_args_list]
        assert not any("selectNodeContents" in s for s in scripts), \
            "an empty editor must not have its Selection reset"

    def test_populated_editor_still_gets_the_selection_reset(self):
        el = MagicMock()
        el.get_attribute.side_effect = lambda n: "true" if n == "contenteditable" else None
        drv = MagicMock()
        drv.execute_script.side_effect = ["", True]  # empty value, but editor has text
        iv_module._clear(drv, el)
        scripts = [c.args[0] for c in drv.execute_script.call_args_list]
        assert any("selectNodeContents" in s for s in scripts)

# Never click an already-empty field
#
# _clear() starts with element.click(). That pointer move fires mouseleave on
# the parent trigger of a hover-opened popup, dismissing the very overlay the
# field lives in (reported on codewalla.com: "Hover popup disappears while
# typing"). So the caller must decide whether a clear is needed BEFORE _clear
# gets a chance to click.
# ---------------------------------------------------------------------------

class TestNeedsClearGuard:
    def _element(self, value="", contenteditable=None, text=""):
        el = MagicMock()
        el.get_attribute.side_effect = lambda name: (
            contenteditable if name == "contenteditable" else None
        )
        el.text = text
        return el

    def _driver(self, value=""):
        drv = MagicMock()
        drv.execute_script.return_value = value
        return drv

    def test_empty_native_input_needs_no_clear(self):
        assert iv_module._needs_clear(self._driver(""), self._element()) is False

    def test_populated_native_input_needs_clear(self):
        assert iv_module._needs_clear(self._driver("hello"), self._element()) is True

    def test_empty_contenteditable_needs_no_clear(self):
        el = self._element(contenteditable="true", text="")
        assert iv_module._needs_clear(self._driver(None), el) is False

    def test_populated_contenteditable_needs_clear(self):
        el = self._element(contenteditable="true", text="draft")
        assert iv_module._needs_clear(self._driver(None), el) is True

    def test_probe_failure_errs_towards_clearing(self):
        """Clearing an empty field is harmless; skipping a needed clear would
        leave the old value and corrupt the typed result."""
        drv = MagicMock()
        drv.execute_script.side_effect = RuntimeError("stale element")
        assert iv_module._needs_clear(drv, self._element()) is True

    def test_input_value_skips_clear_on_an_empty_field(self):
        el = MagicMock()
        el.get_attribute.return_value = None
        drv = MagicMock()
        drv.execute_script.return_value = ""  # empty field
        with patch.object(iv_module, "_clear") as mock_clear, \
             patch.object(iv_module, "_element_to_be_input_and_text"), \
             patch("testmu_selenium._helpers.input_value.WebDriverWait"):
            iv_module.input_value(el, drv, value="typed")
        mock_clear.assert_not_called()

    def test_input_value_still_clears_a_populated_field(self):
        el = MagicMock()
        el.get_attribute.return_value = None
        drv = MagicMock()
        drv.execute_script.return_value = "old value"
        with patch.object(iv_module, "_clear") as mock_clear, \
             patch.object(iv_module, "_element_to_be_input_and_text"), \
             patch("testmu_selenium._helpers.input_value.WebDriverWait"):
            iv_module.input_value(el, drv, value="typed")
        mock_clear.assert_called_once()
