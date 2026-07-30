"""Regression guard for the unary NOT fold in Assertion.evaluate.

``ConcatenationOperator.NOT`` was added to ``condition.py`` together with a
unary NOT fold in ``Assertion.evaluate``: when the group operator is NOT, the
single child is evaluated and its result is negated.  This makes assertion trees
emitted by cgf for "does not contain" / "is not integer" produce the correct
verdict instead of silently ignoring the negation.

JSON shape emitted by cgf for a NOT group::

    {"operator": [], "assertion_operands": ["NOT"], "operands": [<leaf>]}

Tests pin three key behaviors:

1. Plain NOT[contains] negates correctly (the primary fix case).
2. AND[NOT[contains], equals] nests correctly (compound compound case).
3. Plain leaf (contains / equals / not_contains) still evaluates correctly
   (sanity that the NOT branch did not disturb existing AND/OR/leaf paths).
"""
from __future__ import annotations

import pytest

from testmu_selenium.condition import Assertion


# ---------------------------------------------------------------------------
# Helpers — mirrors the pattern in test_condition.py (_passthrough) and
# test_assertion_v2_parity.py (_leaf / _ev).
# ---------------------------------------------------------------------------

def _passthrough(store=None):
    """Return a ``get_variable_value`` callable that resolves full template keys.

    Matching the pattern in ``test_condition.py`` / ``test_assertion_v2_parity``:
    the store is keyed by the raw template string (e.g. ``"{{u}}"``), so
    ``_passthrough({"{{u}}": "http://x/prod"})`` mimics a real var resolver.
    """
    store = store or {}

    def _gv(template, variables=None, *args, **kwargs):
        return store.get(template, template)

    return _gv


def _leaf(op: str, left, right) -> dict:
    """Leaf assertion node — shape cgf emits for a single comparison."""
    return {
        "operator": [op],
        "assertion_operands": [],
        "left_operand": left,
        "right_operand": right,
        "operands": [],
    }


def _not_group(child_dict: dict) -> dict:
    """NOT group — cgf shape: assertion_operands=['NOT'], single child operand."""
    return {
        "operator": [],
        "assertion_operands": ["NOT"],
        "operands": [child_dict],
    }


def _and_group(*child_dicts: dict) -> dict:
    """AND group wrapping two or more children."""
    return {
        "operator": [],
        "assertion_operands": ["AND"],
        "operands": list(child_dicts),
    }


def _ev(node_dict: dict, store: dict | None = None) -> bool:
    """Evaluate *node_dict* and return the boolean result."""
    return Assertion.from_json(node_dict).evaluate({}, _passthrough(store))[0]


# ---------------------------------------------------------------------------
# 1. Primary fix: NOT[contains] negates the child verdict
# ---------------------------------------------------------------------------

class TestNotOperatorNegation:
    """The NOT fold must negate the child verdict for the primary fix case.

    "does not contain 'staging'" is emitted as NOT[contains leaf]; the NOT
    group must flip the contains result.
    """

    def test_not_contains_staging_url_is_false_when_url_contains_staging(self):
        # URL DOES contain 'staging' → contains=True → NOT → False.
        node = _not_group(_leaf("contains", "{{u}}", "staging"))
        gv = _passthrough({"{{u}}": "http://x/staging"})
        result, _ = Assertion.from_json(node).evaluate({}, gv)
        assert result is False

    def test_not_contains_staging_url_is_true_when_url_lacks_staging(self):
        # URL does NOT contain 'staging' → contains=False → NOT → True.
        node = _not_group(_leaf("contains", "{{u}}", "staging"))
        gv = _passthrough({"{{u}}": "http://x/prod"})
        result, _ = Assertion.from_json(node).evaluate({}, gv)
        assert result is True

    def test_not_equals_matching_value_is_false(self):
        # Exact match → equals=True → NOT → False.
        node = _not_group(_leaf("equals", "{{val}}", "active"))
        gv = _passthrough({"{{val}}": "active"})
        result, _ = Assertion.from_json(node).evaluate({}, gv)
        assert result is False

    def test_not_equals_non_matching_value_is_true(self):
        # Different value → equals=False → NOT → True.
        node = _not_group(_leaf("equals", "{{val}}", "active"))
        gv = _passthrough({"{{val}}": "inactive"})
        result, _ = Assertion.from_json(node).evaluate({}, gv)
        assert result is True

    def test_not_group_used_vars_propagated(self):
        # The used_variables dict returned alongside the bool must still carry
        # the variable that was resolved inside the child.
        node = _not_group(_leaf("contains", "{{u}}", "staging"))
        gv = _passthrough({"{{u}}": "http://x/prod"})
        _, used = Assertion.from_json(node).evaluate({}, gv)
        assert "{{u}}" in used


# ---------------------------------------------------------------------------
# 2. Compound case: AND[NOT[contains], equals]
# ---------------------------------------------------------------------------

class TestNotNestedInAnd:
    """AND[NOT[contains], equals] must honour both children independently."""

    def test_and_not_contains_and_equals_both_satisfied(self):
        # NOT('staging' in url)=True AND status='ok'=True → True.
        node = _and_group(
            _not_group(_leaf("contains", "{{u}}", "staging")),
            _leaf("equals", "{{status}}", "ok"),
        )
        gv = _passthrough({"{{u}}": "http://x/prod", "{{status}}": "ok"})
        result, _ = Assertion.from_json(node).evaluate({}, gv)
        assert result is True

    def test_and_not_contains_fails_when_url_contains_staging(self):
        # URL DOES contain 'staging' → NOT=False → AND=False even if equals passes.
        node = _and_group(
            _not_group(_leaf("contains", "{{u}}", "staging")),
            _leaf("equals", "{{status}}", "ok"),
        )
        gv = _passthrough({"{{u}}": "http://x/staging", "{{status}}": "ok"})
        result, _ = Assertion.from_json(node).evaluate({}, gv)
        assert result is False

    def test_and_not_contains_fails_when_equals_fails(self):
        # NOT=True but equals=False → AND=False.
        node = _and_group(
            _not_group(_leaf("contains", "{{u}}", "staging")),
            _leaf("equals", "{{status}}", "ok"),
        )
        gv = _passthrough({"{{u}}": "http://x/prod", "{{status}}": "error"})
        result, _ = Assertion.from_json(node).evaluate({}, gv)
        assert result is False


# ---------------------------------------------------------------------------
# 3. Regression sanity: plain leaf nodes still evaluate correctly
# ---------------------------------------------------------------------------

class TestLeafRegressionSanity:
    """Plain leaf nodes (contains / equals / not_contains) must be unaffected.

    Sanity guard: the NOT branch must not disturb AND/OR/leaf paths.
    """

    def test_contains_leaf_substring_present(self):
        assert _ev(_leaf("contains", "http://x/staging", "staging")) is True

    def test_contains_leaf_substring_absent(self):
        assert _ev(_leaf("contains", "http://x/prod", "staging")) is False

    def test_equals_leaf_matching(self):
        assert _ev(_leaf("equals", "active", "active")) is True

    def test_equals_leaf_non_matching(self):
        assert _ev(_leaf("equals", "active", "inactive")) is False

    def test_not_contains_assertion_condition_coexists_with_not_group(self):
        # AssertionCondition.NOT_CONTAINS (a leaf-level operator) is distinct
        # from ConcatenationOperator.NOT (a group-level negation).  Confirm they
        # coexist without interference.
        assert _ev(_leaf("not_contains", "http://x/prod", "staging")) is True
        assert _ev(_leaf("not_contains", "http://x/staging", "staging")) is False

    @pytest.mark.parametrize(
        "op,left,right,expected",
        [
            ("equals",      "hello", "hello",   True),
            ("equals",      "hello", "world",   False),
            ("contains",    "hello world", "world", True),
            ("contains",    "hello world", "xyz",   False),
            ("not_contains","hello world", "xyz",   True),
            ("not_contains","hello world", "world", False),
        ],
    )
    def test_leaf_operators_parametrized(self, op, left, right, expected):
        assert _ev(_leaf(op, left, right)) is expected
