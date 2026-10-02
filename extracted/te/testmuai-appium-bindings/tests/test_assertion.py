"""assertion() — local sub-check evaluation (no /evaluate network call)."""
import pytest

from testmu_appium._helpers.assertion import assertion
from testmu_appium._vars import clear_state, set_var


@pytest.fixture(autouse=True)
def _clear_vars():
    clear_state()
    yield
    clear_state()


class _FakeDriver:
    """assertion() evaluates locally; the driver is accepted for verb-interface
    parity with the other query verbs but never touched."""


def test_passing_sub_checks_return_the_evaluate_sub_checks_shape():
    result = assertion(
        _FakeDriver(),
        claim="title says hello",
        sub_checks=[
            {"description": "greeting", "extracted_value": "hello world",
             "expected_value": "hello", "operator": "contains"},
        ],
    )
    assert result["status"] == "passed"
    assert result["composite_operator"] == "and"
    assert len(result["sub_results"]) == 1


def test_failing_sub_check_raises_assertion_error_with_readable_summary():
    with pytest.raises(AssertionError) as exc:
        assertion(
            _FakeDriver(),
            claim="title says goodbye",
            sub_checks=[
                {"description": "greeting", "extracted_value": "hello world",
                 "expected_value": "goodbye", "operator": "contains"},
            ],
        )
    message = str(exc.value)
    assert "greeting" in message
    assert "goodbye" in message
    assert "hello world" in message


def test_composite_operator_or_passes_when_one_sub_check_passes():
    result = assertion(
        _FakeDriver(),
        composite_operator="or",
        sub_checks=[
            {"extracted_value": "a", "expected_value": "z", "operator": "equals"},
            {"extracted_value": "a", "expected_value": "a", "operator": "equals"},
        ],
    )
    assert result["status"] == "passed"


def test_no_driver_touch_the_driver_is_never_called():
    class _ExplodingDriver:
        def __getattr__(self, name):
            raise AssertionError(f"assertion() must not touch the driver ({name})")

    assertion(_ExplodingDriver(), sub_checks=[
        {"extracted_value": "a", "expected_value": "a", "operator": "equals"},
    ])


def test_variable_tokens_are_resolved_in_extracted_and_expected_value():
    set_var("actual_title", "Welcome Home")
    set_var("wanted", "Welcome")
    result = assertion(
        _FakeDriver(),
        sub_checks=[
            {"extracted_value": "{{actual_title}}", "expected_value": "{{wanted}}",
             "operator": "contains"},
        ],
    )
    assert result["status"] == "passed"


def test_mobile_json_operator_family_is_routed_through_the_evaluator():
    """Proves assertion() calls _mobile_operators.evaluate_sub_checks (which knows
    json_*), not the canonical evaluate_sub_checks (which does not)."""
    result = assertion(
        _FakeDriver(),
        sub_checks=[
            {"extracted_value": '{"name": "sid", "roles": ["admin", "dev"]}',
             "expected_value": "name", "operator": "json_key_exists"},
        ],
    )
    assert result["status"] == "passed"


@pytest.mark.parametrize("sub_checks", [[], None], ids=["empty", "omitted"])
def test_no_sub_checks_raises_rather_than_passing_vacuously(sub_checks):
    """An empty "and" is vacuously true, so a producer bug that drops the sub_checks
    would read as a GREEN assertion. verify_assertion refuses an empty tree the same
    way."""
    with pytest.raises(ValueError) as exc:
        assertion(_FakeDriver(), sub_checks=sub_checks)
    assert "sub_checks" in str(exc.value)


def test_omitting_sub_checks_entirely_raises():
    with pytest.raises(ValueError):
        assertion(_FakeDriver(), claim="something is true")


def test_the_two_assertion_entry_points_agree_on_emptiness():
    from testmu_appium._helpers.verify_assertion import verify_assertion

    with pytest.raises(ValueError):
        assertion(_FakeDriver(), sub_checks=[])
    with pytest.raises(ValueError):
        verify_assertion(_FakeDriver(), tree={"claim": "x", "sub_checks": []})


def test_default_composite_operator_is_and():
    """One passing + one failing sub_check must fail the whole "and" — proven by
    the raise, since a passing return only happens on an overall pass."""
    with pytest.raises(AssertionError):
        assertion(
            _FakeDriver(),
            sub_checks=[
                {"extracted_value": "a", "expected_value": "a", "operator": "equals"},
                {"extracted_value": "b", "expected_value": "z", "operator": "equals"},
            ],
        )


# ── evaluate_branch: the if / elif condition of an exported conditional ──

from testmu_appium._helpers.assertion import evaluate_branch


def _popup_check(**overrides):
    check = {
        "description": '"CDN file download Successful" popup is visible',
        "store_key": "popup_visible",
        "expected_value": "true",
        "extracted_value": "{{popup_visible}}",
        "operator": "equals",
        "transforms": ["strip", "lowercase"],
    }
    check.update(overrides)
    return check


def test_evaluate_branch_resolves_the_variable_and_compares():
    set_var("popup_visible", "True")
    assert evaluate_branch([_popup_check()], "and") is True
    set_var("popup_visible", "false")
    assert evaluate_branch([_popup_check()], "and") is False


def test_evaluate_branch_accepts_v16_expected_key_and_defaults():
    set_var("title", "Hello world")
    check = {"description": "title", "extracted_value": "{{title}}", "expected": "Hello"}
    assert evaluate_branch([check]) is True


def test_evaluate_branch_composite_operator():
    set_var("a", "1")
    set_var("b", "2")
    hit = _popup_check(extracted_value="{{a}}", expected_value="1", transforms=[])
    miss = _popup_check(extracted_value="{{b}}", expected_value="1", transforms=[])
    assert evaluate_branch([hit, miss], "or") is True
    assert evaluate_branch([hit, miss], "and") is False
    assert evaluate_branch([hit, miss], "") is False


def test_evaluate_branch_without_sub_checks_is_false():
    assert evaluate_branch([], "and") is False
    assert evaluate_branch(None, "and") is False


def test_evaluate_branch_reads_stored_value_the_blob_branch_key():
    """A branch condition names its variable reference under `stored_value`
    (auteur's blob shape), not `extracted_value`. Both must resolve, or the
    condition compares "" and always takes the false branch."""
    set_var("username_visible_check", "true")
    check = {
        "description": "username is visible",
        "store_key": "username_visible_check",
        "expected_value": "true",
        "stored_value": "{{username_visible_check}}",
        "operator": "equals",
        "transforms": [],
    }
    assert evaluate_branch([check], "and") is True
