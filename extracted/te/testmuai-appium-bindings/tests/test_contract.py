"""The binding↔generator contract.

The public-surface pin (test_public_surface.py) encodes the same contract
structurally; this file pins the BEHAVIOUR behind each new or widened parameter.
"""
import httpx
import pytest
import respx

from testmu_appium import _action_engine, _config
from testmu_appium._action_select import select
from testmu_appium._action_type import search, type as type_
from testmu_appium._errors import CoordinateFallbackUnavailable, ElementNotFound
from testmu_appium._heal import HealNoMatch
from testmu_appium._helpers.condition import check_until_condition
from testmu_appium._helpers.device_control import device_control
from testmu_appium._helpers.evaluate_math import evaluate_math
from testmu_appium._helpers.verify_assertion import verify_assertion
from testmu_appium._helpers.wait import wait
from testmu_appium._step import step
from testmu_appium._vars import _variable_store, set_var

SELECTORS = [{"strategy": "view_id", "selector": "com.app:id/go", "score": 90}]
BASIS = {"x_ratio": 0.5, "y_ratio": 0.5, "orientation": "portrait", "window": [1080, 2340]}
_AI = "https://ai.example.test/v16-server"


class _El:
    def __init__(self, rect=None, attributes=None, texts=None):
        self.rect = rect or {"x": 100, "y": 200, "width": 200, "height": 100}
        self.attributes = attributes or {}
        self.calls = []
        self._texts = list(texts) if texts else None

    def click(self):
        self.calls.append(("click",))

    def clear(self):
        self.calls.append(("clear",))

    def send_keys(self, text):
        self.calls.append(("send_keys", text))

    def get_attribute(self, name):
        if name == "text" and self._texts is not None:
            return self._texts.pop(0) if len(self._texts) > 1 else self._texts[0]
        return self.attributes.get(name)


class _Driver:
    page_source = "<hierarchy rotation='0'/>"

    def __init__(self, found=None, queue=None):
        self.found = found or {}
        self.queue = list(queue) if queue is not None else None
        self.scripts = []
        self.find_calls = []
        self.keycodes = []

    def get_window_size(self):
        return {"width": 1080, "height": 2340}

    def get_screenshot_as_png(self):
        return b"\x89PNG"

    def find_elements(self, by, value):
        self.find_calls.append((by, value))
        if self.queue is not None:
            return self.queue.pop(0) if self.queue else []
        for needle, result in self.found.items():
            if needle in value:
                return result
        return []

    def execute_script(self, script, args=None):
        self.scripts.append((script, args))
        return True

    def press_keycode(self, code):
        self.keycodes.append(code)

    def hide_keyboard(self):
        self.scripts.append(("hide_keyboard", None))


@pytest.fixture(autouse=True)
def _fast(monkeypatch):
    monkeypatch.setattr(_action_engine, "_settle", lambda driver, deadline: None)
    monkeypatch.setattr(_action_engine.time, "sleep", lambda s: None)
    monkeypatch.setitem(_config._config, "platform", "android")
    # These suites are not about the find timeout; one strategy pass keeps a
    # deliberate miss instantaneous instead of polling for the real budget.
    monkeypatch.setitem(_config._config, "default_action_timeout_ms", 0)
    monkeypatch.setattr(_config, "smart", True)
    # _config.resolved() reads the env live unless the key was set through
    # configure(), so the env var — not the seeded dict value — is what steers it.
    monkeypatch.setenv("TESTMU_AI_API_HOST", _AI)
    _variable_store.clear()
    yield
    _variable_store.clear()


def _found(element):
    return _Driver(found={"com.app:id/go": [element]})


class TestTypeContract:
    """`type` gains explicit clear_first + delay_ms beside the legacy skip flags."""

    def test_clear_first_defaults_true(self):
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="hi")
        assert ("clear",) in el.calls

    def test_clear_first_false_skips_the_clear(self):
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="hi", clear_first=False)
        assert ("clear",) not in el.calls

    @pytest.mark.parametrize("flag", ["multiple_inputs", "manual_interaction_tag"])
    def test_legacy_skip_flags_still_override_clear_first(self, flag):
        """The recorded flags mean "another step already put text here"; they win
        over the recorded clear_first, which describes the field, not the sequence."""
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="hi", clear_first=True, **{flag: True})
        assert ("clear",) not in el.calls

    def test_delay_ms_types_one_character_at_a_time(self, monkeypatch):
        slept = []
        monkeypatch.setattr("time.sleep", lambda s: slept.append(s))
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="abc", delay_ms=50)
        assert [c for c in el.calls if c[0] == "send_keys"] == [
            ("send_keys", "a"), ("send_keys", "b"), ("send_keys", "c")
        ]
        assert slept == [0.05, 0.05]

    def test_delay_ms_zero_sends_the_whole_string_at_once(self):
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="abc", delay_ms=0)
        assert ("send_keys", "abc") in el.calls

    def test_negative_delay_is_rejected(self):
        with pytest.raises(ValueError):
            with step("s"):
                type_(_found(_El()), selectors=SELECTORS, text="a", delay_ms=-1)


class TestSearchContract:
    """`search` gains clear_first + a configurable submit key."""

    def test_default_submit_key_is_enter(self):
        driver = _found(_El())
        with step("s"):
            search(driver, selectors=SELECTORS, text="pizza")
        assert driver.keycodes == [66]

    def test_submit_key_is_configurable(self):
        driver = _found(_El())
        with step("s"):
            search(driver, selectors=SELECTORS, text="pizza", submit_key="SEARCH")
        assert driver.keycodes == [84]

    def test_submit_key_is_case_insensitive(self):
        driver = _found(_El())
        with step("s"):
            search(driver, selectors=SELECTORS, text="pizza", submit_key="Enter")
        assert driver.keycodes == [66]

    def test_unknown_submit_key_raises(self):
        from testmu_appium._errors import UnknownKeyEvent

        with pytest.raises(UnknownKeyEvent):
            with step("s"):
                search(_found(_El()), selectors=SELECTORS, text="x", submit_key="SUBMIT")

    def test_clear_first_false_skips_the_clear(self):
        el = _El()
        with step("s"):
            search(_found(el), selectors=SELECTORS, text="x", clear_first=False)
        assert ("clear",) not in el.calls


class TestSelectContract:
    """SelectAction carries value / label / index; at least one is required."""

    def _spinner_driver(self, option=None):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        return _Driver(queue=[[spinner], [option or _El()]]), spinner

    def test_value_selects_by_text(self):
        driver, _ = self._spinner_driver()
        with step("s"):
            select(driver, selectors=SELECTORS, value="Delhi")
        assert 'text("Delhi")' in driver.find_calls[1][1]

    def test_label_selects_by_visible_label(self):
        driver, _ = self._spinner_driver()
        with step("s"):
            select(driver, selectors=SELECTORS, label="Delhi")
        assert 'text("Delhi")' in driver.find_calls[1][1]

    def test_a_spinner_prefers_the_visible_label_over_the_value(self):
        """A spinner's options are matched by the text they RENDER, so the label
        leads and the value stands in only when no label was recorded."""
        driver, _ = self._spinner_driver()
        with step("s"):
            select(driver, selectors=SELECTORS, value="DEL", label="New Delhi")
        assert 'text("New Delhi")' in driver.find_calls[1][1]

    def test_a_number_picker_prefers_the_value_over_the_label(self):
        """A wheel is set to a number; the label is its rendering."""
        picker = _El(attributes={"class": "android.widget.NumberPicker"}, texts=["3"])
        driver = _found(picker)
        with step("s"):
            select(driver, selectors=SELECTORS, value="3", label="Three")
        assert driver.scripts == [], "already on 3; a label target would have scrolled"

    def test_index_selects_the_nth_option(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        first, second = _El(), _El()
        driver = _Driver(queue=[[spinner], [first, second]])
        with step("s"):
            select(driver, selectors=SELECTORS, index=1)
        assert second.calls == [("click",)]
        assert first.calls == []

    def test_index_out_of_range_raises(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        driver = _Driver(queue=[[spinner], [_El()]])
        with pytest.raises(ValueError) as exc:
            with step("s"):
                select(driver, selectors=SELECTORS, index=5)
        assert "5" in str(exc.value)

    def test_index_is_meaningless_for_a_number_picker(self):
        picker = _El(attributes={"class": "android.widget.NumberPicker"}, texts=["3"])
        with pytest.raises(ValueError) as exc:
            with step("s"):
                select(_found(picker), selectors=SELECTORS, index=2)
        assert "index" in str(exc.value)

    def test_at_least_one_target_is_required(self):
        with pytest.raises(ValueError) as exc:
            with step("s"):
                select(_found(_El()), selectors=SELECTORS)
        assert "value" in str(exc.value) and "label" in str(exc.value)

    def test_index_zero_is_a_real_target_not_a_falsy_miss(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        first = _El()
        driver = _Driver(queue=[[spinner], [first, _El()]])
        with step("s"):
            select(driver, selectors=SELECTORS, index=0)
        assert first.calls == [("click",)]


class TestEvaluateMath:
    """MathmaticAction.mathmatic_tree — the V3 operator/operands tree."""

    @pytest.mark.parametrize("tree,expected", [
        ({"operator": "add", "operands": ["1", "2", "3"]}, 6.0),
        ({"operator": "subtract", "operands": ["10", "4"]}, 6.0),
        ({"operator": "multiply", "operands": ["3", "4"]}, 12.0),
        ({"operator": "divide", "operands": ["10", "4"]}, 2.5),
        ({"operator": "mod", "operands": ["10", "3"]}, 1.0),
        ({"operator": "pow", "operands": ["2", "10"]}, 1024.0),
        ({"operator": "negate", "operands": ["5"]}, -5.0),
        ({"operator": "abs", "operands": ["-5"]}, 5.0),
    ])
    def test_operators(self, tree, expected):
        assert evaluate_math(tree=tree) == expected

    def test_nested_trees(self):
        tree = {"operator": "multiply", "operands": [
            {"operator": "add", "operands": ["1", "2"]},
            "4",
        ]}
        assert evaluate_math(tree=tree) == 12.0

    def test_variable_operands_resolve_from_the_store(self):
        set_var("price", "10")
        set_var("qty", "3")
        tree = {"operator": "multiply", "operands": ["{{price}}", "{{qty}}"]}
        assert evaluate_math(tree=tree) == 30.0

    def test_missing_variable_raises(self):
        with pytest.raises(KeyError):
            evaluate_math(tree={"operator": "add", "operands": ["{{nope}}", "1"]})

    def test_output_variable_is_written(self):
        evaluate_math(tree={"operator": "add", "operands": ["2", "2"]}, output_variable="total")
        assert _variable_store["total"] == 4.0

    def test_unknown_operator_raises(self):
        with pytest.raises(ValueError):
            evaluate_math(tree={"operator": "factorial", "operands": ["5"]})

    def test_division_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            evaluate_math(tree={"operator": "divide", "operands": ["1", "0"]})

    @pytest.mark.parametrize("op", ["subtract", "divide", "mod", "pow"])
    def test_binary_operators_require_exactly_two_operands(self, op):
        with pytest.raises(ValueError):
            evaluate_math(tree={"operator": op, "operands": ["1", "2", "3"]})

    @pytest.mark.parametrize("op", ["subtract", "divide", "mod", "pow"])
    def test_binary_operators_reject_a_single_operand(self, op):
        with pytest.raises(ValueError):
            evaluate_math(tree={"operator": op, "operands": ["1"]})

    def test_pow_with_extra_operands_does_not_silently_ignore_them(self):
        """A three-operand pow tree is an arity error, not a two-operand power with
        the third operand dropped."""
        with pytest.raises(ValueError) as exc:
            evaluate_math(tree={"operator": "pow", "operands": ["2", "10", "3"]})
        assert "pow" in str(exc.value) and "2 operands" in str(exc.value)

    def test_non_numeric_operand_raises(self):
        with pytest.raises(ValueError):
            evaluate_math(tree={"operator": "add", "operands": ["one", "2"]})

    @pytest.mark.parametrize(
        "tree",
        [
            {"operands": ["1", "2"]},
            {"operands": []},
            {},
        ],
        ids=["with-operands", "empty-operands", "bare"],
    )
    def test_a_tree_with_no_operator_raises(self, tree):
        """A tree with no operator raises rather than defaulting to "add"."""
        with pytest.raises(ValueError) as exc:
            evaluate_math(tree=tree)
        assert "operator" in str(exc.value)

    def test_test_param_operands_resolve_like_they_do_in_math(self):
        """`${...}` reads test_params first, in a recorded tree exactly as it does
        inside math()."""
        from testmu_appium._vars import _test_params

        _test_params["discount"] = "5"
        set_var("price", "20")
        tree = {"operator": "subtract", "operands": ["{{price}}", "${discount}"]}
        assert evaluate_math(tree=tree) == 15.0

    def test_a_test_param_and_a_store_variable_of_the_same_name_prefer_the_param(self):
        from testmu_appium._vars import _test_params

        _test_params["v"] = "1"
        set_var("v", "9")
        assert evaluate_math(tree={"operator": "add", "operands": ["${v}", "0"]}) == 1.0

    def test_dotted_operands_traverse_into_a_stored_object(self):
        set_var("cart", {"items": [{"price": 7}]})
        tree = {"operator": "multiply", "operands": ["{{cart.items[0].price}}", "2"]}
        assert evaluate_math(tree=tree) == 14.0

    def test_a_missing_test_param_still_raises(self):
        with pytest.raises(KeyError):
            evaluate_math(tree={"operator": "add", "operands": ["${nope}", "1"]})

    def test_a_bare_numeric_operand_is_not_treated_as_a_template(self):
        assert evaluate_math(tree={"operator": "add", "operands": ["2", "3"]}) == 5.0


class TestVerifyAssertion:
    """AssertionAction.assertion_tree — claim + composite_operator + sub_checks."""

    PASSING = {
        "claim": "the total is right",
        "composite_operator": "and",
        "sub_checks": [
            {"description": "total", "extracted_value": "42",
             "expected_value": "42", "operator": "equals"},
        ],
    }
    FAILING = {
        "claim": "the total is right",
        "composite_operator": "and",
        "sub_checks": [
            {"description": "total", "extracted_value": "41",
             "expected_value": "42", "operator": "equals"},
        ],
    }

    def test_passing_tree_returns_the_result(self):
        result = verify_assertion(None, tree=self.PASSING)
        assert result["status"] == "passed"
        assert len(result["sub_results"]) == 1

    def test_failing_tree_raises_by_default(self):
        with pytest.raises(AssertionError) as exc:
            verify_assertion(None, tree=self.FAILING)
        assert "the total is right" in str(exc.value)
        assert "42" in str(exc.value)

    def test_return_result_suppresses_the_raise(self):
        result = verify_assertion(None, tree=self.FAILING, return_result=True)
        assert result["status"] == "failed"

    def test_composite_operator_comes_from_the_tree(self):
        tree = dict(self.FAILING, composite_operator="or")
        tree["sub_checks"] = self.FAILING["sub_checks"] + self.PASSING["sub_checks"]
        result = verify_assertion(None, tree=tree, return_result=True)
        assert result["composite_operator"] == "or"
        assert result["status"] == "passed"

    def test_variable_tokens_resolve_inside_the_tree(self):
        set_var("expected_total", "42")
        tree = {"claim": "c", "composite_operator": "and", "sub_checks": [
            {"extracted_value": "42", "expected_value": "{{expected_total}}",
             "operator": "equals"},
        ]}
        assert verify_assertion(None, tree=tree)["status"] == "passed"

    def test_mobile_json_operators_route_through(self):
        tree = {"claim": "c", "composite_operator": "and", "sub_checks": [
            {"extracted_value": '{"a": 1}', "expected_value": "a",
             "operator": "json_key_exists"},
        ]}
        assert verify_assertion(None, tree=tree)["status"] == "passed"

    def test_missing_tree_raises(self):
        with pytest.raises(ValueError):
            verify_assertion(None, tree=None)

    def test_tree_without_sub_checks_raises(self):
        with pytest.raises(ValueError):
            verify_assertion(None, tree={"claim": "c"})


class TestCheckUntilCondition:
    """Until-loop condition check, routed through the vision_query endpoint path."""

    @respx.mock
    @pytest.mark.parametrize("extracted,expected", [
        (True, True), (False, False),
        ("true", True), ("false", False),
        ("yes", True), ("no", False),
        ("1", True), ("0", False),
        # "met" and "passed" are the until-condition's own vocabulary, and they live
        # in the one truthy set `coerce(..., "boolean")` applies.
        ("met", True), ("MET", True), (" met ", True),
        ("passed", True), ("unmet", False), ("not met", False),
    ])
    def test_boolean_coercion(self, extracted, expected):
        respx.post(f"{_AI}/api/v1/analyzer").mock(
            return_value=httpx.Response(200, json={"extracted_value": extracted})
        )
        with step("s"):
            assert check_until_condition(_Driver(), "the cart badge shows 3") is expected

    @respx.mock
    def test_request_asks_for_a_boolean_return_type(self):
        route = respx.post(f"{_AI}/api/v1/analyzer").mock(
            return_value=httpx.Response(200, json={"extracted_value": True})
        )
        with step("s"):
            check_until_condition(_Driver(), "the cart badge shows 3")
        import json

        body = json.loads(route.calls[0].request.content)
        assert body["type"] == "visual"
        assert body["query"] == "the cart badge shows 3"
        assert body["return_type"] == "boolean"

    @respx.mock
    def test_request_gates_the_analyzers_boolean_check_branch(self):
        """Without expected_value the analyzer answers the EXTRACTION question —
        a found string, which coerces to False and never lets the loop exit."""
        route = respx.post(f"{_AI}/api/v1/analyzer").mock(
            return_value=httpx.Response(200, json={"extracted_value": "true"})
        )
        with step("s"):
            assert check_until_condition(_Driver(), "the cart badge shows 3") is True
        import json

        assert json.loads(route.calls[0].request.content)["expected_value"] == "true"

    def test_there_is_exactly_one_truthy_vocabulary(self):
        """One shared truthy vocabulary; no caller keeps a second copy."""
        from testmu_appium._helpers import condition as condition_module
        from testmu_appium._helpers._return_type import _TRUTHY

        assert not hasattr(condition_module, "_TRUTHY")
        assert "met" in _TRUTHY

    @respx.mock
    def test_condition_variables_resolve(self):
        set_var("count", "3")
        route = respx.post(f"{_AI}/api/v1/analyzer").mock(
            return_value=httpx.Response(200, json={"extracted_value": True})
        )
        with step("s"):
            check_until_condition(_Driver(), "the badge shows {{count}}")
        import json

        assert json.loads(route.calls[0].request.content)["query"] == "the badge shows 3"

    @respx.mock
    def test_transport_failure_raises_rather_than_returning_false(self):
        """A never-evaluable condition returning False would let the caller's
        until-loop burn its whole budget while masking the real problem."""
        respx.post(f"{_AI}/api/v1/analyzer").mock(
            return_value=httpx.Response(500, text="boom")
        )
        with pytest.raises(RuntimeError):
            with step("s"):
                check_until_condition(_Driver(), "anything")

    def test_smart_disabled_raises(self, monkeypatch):
        monkeypatch.setattr(_config, "smart", False)
        with pytest.raises(Exception):
            with step("s"):
                check_until_condition(_Driver(), "anything")


class TestQueryReturnTypeContract:
    """textual_query / vision_query gain return_type + expected_value."""

    class _TreeDriver(_Driver):
        """A driver whose page source yields entries, so an identify answer of
        dom_index=1 names an element the capture actually saw."""

        page_source = (
            "<hierarchy rotation='0'>"
            "<android.widget.TextView resource-id='com.app:id/label' text='Compose' "
            "content-desc='' bounds='[0,0][300,100]' clickable='true' enabled='true'/>"
            "</hierarchy>"
        )

    @respx.mock
    @pytest.mark.parametrize("return_type,extracted,expected", [
        ("string", 42, "42"),
        ("number", "42", 42.0),
        ("boolean", "true", True),
        (None, 42, "42"),
        ("", 42, "42"),
    ])
    def test_return_type_coerces_the_extracted_value(self, return_type, extracted, expected):
        from testmu_appium._helpers.textual_query import textual_query

        respx.post(f"{_AI}/api/v1/analyzer").mock(side_effect=[
            httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
            httpx.Response(200, json={"extracted_value": extracted}),
        ])
        with step("s"):
            assert textual_query(
                self._TreeDriver(), query="q", return_type=return_type
            ) == expected

    def test_a_misspelled_return_type_still_raises(self):
        from testmu_appium._helpers._return_type import coerce

        with pytest.raises(ValueError, match="unknown return_type"):
            coerce(42, "strng")

    @respx.mock
    def test_return_type_and_expected_value_ride_on_the_request(self):
        from testmu_appium._helpers.vision_query import vision_query

        route = respx.post(f"{_AI}/api/v1/analyzer").mock(
            return_value=httpx.Response(200, json={"extracted_value": "red"})
        )
        with step("s"):
            vision_query(_Driver(), query="button colour",
                         return_type="string", expected_value="red")
        import json

        body = json.loads(route.calls[0].request.content)
        assert body["return_type"] == "string"
        assert body["expected_value"] == "red"

    @respx.mock
    def test_omitted_kwargs_stay_off_the_request(self):
        from testmu_appium._helpers.textual_query import textual_query

        route = respx.post(f"{_AI}/api/v1/analyzer").mock(side_effect=[
            httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
            httpx.Response(200, json={"extracted_value": "x"}),
        ])
        with step("s"):
            textual_query(self._TreeDriver(), query="q")
        import json

        for call in route.calls:
            body = json.loads(call.request.content)
            assert "expected_value" not in body

    @respx.mock
    def test_the_extract_call_carries_expected_value(self):
        """It gates the analyzer's boolean-check branch, and only the extract
        step produces a value to check."""
        from testmu_appium._helpers.textual_query import textual_query

        route = respx.post(f"{_AI}/api/v1/analyzer").mock(side_effect=[
            httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
            httpx.Response(200, json={"extracted_value": "true"}),
        ])
        with step("s"):
            textual_query(self._TreeDriver(), query="q", expected_value="true")
        import json

        assert "expected_value" not in json.loads(route.calls[0].request.content)
        assert json.loads(route.calls[1].request.content)["expected_value"] == "true"

    @respx.mock
    def test_unknown_return_type_raises(self):
        from testmu_appium._helpers.textual_query import textual_query

        respx.post(f"{_AI}/api/v1/analyzer").mock(side_effect=[
            httpx.Response(200, json={"extracted_value": "", "dom_index": 1}),
            httpx.Response(200, json={"extracted_value": "x"}),
        ])
        with pytest.raises(ValueError):
            with step("s"):
                textual_query(self._TreeDriver(), query="q", return_type="date")


class TestConfirmedUnchanged:
    """Cells the cgf lane is aligning TO — pinned so they cannot drift."""

    def test_drag_takes_an_element_or_two_recorded_points(self):
        """Selectors choose the mode, as they do for `scroll`.

        Supersedes the coordinate-only pin: a drag that carries no identity
        cannot be re-grounded, so the element arm is what makes a recorded drag
        survive a device of another size.
        """
        import inspect

        from testmu_appium import drag

        parameters = inspect.signature(drag).parameters
        assert set(parameters) == {
            "driver", "selectors", "source_coordinates", "target_coordinates",
            "direction", "fraction", "source_description", "target_description",
            "grounded_by", "hold_duration_ms", "move_duration_ms", "description",
            # Both ends carry identity: the drop point is re-grounded from its
            # own selectors, not derived from the source's.
            "target_selectors", "target_grounded_by",
            # The two pauses are separate asks: the pickup holds BEFORE the
            # move, this one after it. A slide-and-hold control confirms on the
            # second and abandons without it.
            "hold_at_destination_ms",
        }

    def test_bare_xy_coordinate_pairs_are_still_refused(self, monkeypatch):
        """The generator omits these now; the binding must still refuse them, so a
        stale artifact fails loudly instead of tapping an unscaled pixel."""
        from testmu_appium import click

        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        driver = _Driver(queue=[[]])
        with pytest.raises(ElementNotFound) as exc:
            with step("s"):
                click(driver, selectors=SELECTORS, fallback_coordinates={"x": 540, "y": 1170})
        assert isinstance(exc.value.__cause__, CoordinateFallbackUnavailable)

    def test_full_basis_is_still_accepted(self, monkeypatch):
        from testmu_appium import click

        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        driver = _Driver(queue=[[]])
        with step("s"):
            click(driver, selectors=SELECTORS, fallback_coordinates=BASIS)
        assert driver.scripts[0][0] == "mobile: clickGesture"

    def test_hide_keyboard_tolerates_an_empty_value(self):
        driver = _Driver()
        device_control(driver, "hide_keyboard")
        device_control(driver, "hide_keyboard", value="")
        assert driver.scripts == [("hide_keyboard", None)] * 2

    def test_wait_accepts_ms_as_a_keyword(self, monkeypatch):
        slept = []
        monkeypatch.setattr("testmu_appium._helpers.wait.time.sleep", lambda s: slept.append(s))
        wait(None, ms=500)
        assert slept == [0.5]

    def test_wait_still_accepts_seconds(self, monkeypatch):
        slept = []
        monkeypatch.setattr("testmu_appium._helpers.wait.time.sleep", lambda s: slept.append(s))
        wait(None, 1.5)
        assert slept == [1.5]
