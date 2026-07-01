"""V2-parity RED tests for the V3 Condition (until/while) runtime evaluator.

V2 source of truth (``_compare_atomic`` in the V2 source) is the
canonical authoring semantics that V3 replay must match:
  - contains:      ``right in left``, CASE-INSENSITIVE, ascii/accent-folded.
  - starts_with:   ``left.startswith(right)``, case-insensitive, folded.
  - ends_with:     ``left.endswith(right)``, case-insensitive, folded.
  - OR/AND:        ``A OR B AND C`` == ``A OR (B AND C)`` (AND binds tighter).

The ``Condition`` path (until/while) currently uses raw ``str()`` substring /
prefix / suffix checks (case-SENSITIVE, no fold) and a flat left-fold over
connectors with NO operator precedence. These RED tests encode the V2 behavior
and therefore FAIL against the current implementation; they pass once the
``Condition`` evaluator is brought to V2 parity.

The ``Assertion`` leaf path already normalizes text V2-correctly; the two
PARITY-GUARD tests below lock that in and are expected to PASS now.

Run from selenium-python/ with the worktree on PYTHONPATH:
    PYTHONPATH=$PWD <python> -m pytest tests/test_v2_parity_conditionals.py -v
"""
from __future__ import annotations

from testmu_selenium.condition import (
    Assertion,
    AssertionCondition,
    ConcatenationOperator,
    Condition,
    PossibleCondition,
    ResolvedCondition,
)


def _passthrough(store=None):
    """get_variable_value that resolves a template to its store value, else the
    template literal unchanged (matches the existing test_condition.py helper)."""
    store = store or {}

    def _gv(template, variables=None, *args, **kwargs):
        return store.get(template, template)

    return _gv


# A bare Condition instance is enough to exercise the pure _eval_condition leaf.
# is_v3=True activates the V3 text normalization and precedence fold under test.
_COND = Condition([], [], is_v3=True)


# --------------------------------------------------------------------------- #
# RED — must FAIL now, PASS after the Condition evaluator reaches V2 parity.   #
# --------------------------------------------------------------------------- #
class TestConditionTextNormalizationRED:
    """Condition leaf text ops must be case-insensitive + ascii-folded (V2).
    Current raw str() comparisons make every assert below fail."""

    def test_contains_is_case_insensitive(self):
        # V2: 'world' in 'HELLO WORLD' case-insensitively -> True.
        # Current raw: 'world' in 'HELLO WORLD' -> False.
        assert _COND._eval_condition(
            PossibleCondition.CONTAINS, "HELLO WORLD", "world"
        ) is True

    def test_starts_with_is_case_insensitive(self):
        # V2: 'Hello World'.startswith('hello') folded -> True. Current -> False.
        assert _COND._eval_condition(
            PossibleCondition.STARTS_WITH, "Hello World", "hello"
        ) is True

    def test_ends_with_is_case_insensitive(self):
        # V2: 'Hello World'.endswith('WORLD') folded -> True. Current -> False.
        assert _COND._eval_condition(
            PossibleCondition.ENDS_WITH, "Hello World", "WORLD"
        ) is True

    def test_contains_folds_unicode_accents(self):
        # V2: 'cafe' in 'café au lait' after accent fold -> True.
        # Current raw: é != e -> 'cafe' not in 'café au lait' -> False.
        assert _COND._eval_condition(
            PossibleCondition.CONTAINS, "café au lait", "cafe"
        ) is True


class TestConditionConnectorPrecedenceRED:
    """`A OR B AND C` must bind AND tighter than OR -> A OR (B AND C).
    The current flat left-fold computes ((A OR B) AND C), giving the wrong
    verdict whenever precedence matters."""

    def test_or_and_precedence_true_or_false_and_false(self):
        # A=true, B=false, C=false; connectors [OR, AND].
        # V2 precedence:  A OR (B AND C) = True OR (False AND False) = True.
        # Current flat fold: (A OR B) AND C = (True OR False) AND False = False.
        a = ResolvedCondition("1", PossibleCondition.EQUALS, "1")  # true
        b = ResolvedCondition("1", PossibleCondition.EQUALS, "2")  # false
        c = ResolvedCondition("1", PossibleCondition.EQUALS, "2")  # false
        cond = Condition(
            [a, b, c],
            [ConcatenationOperator.OR, ConcatenationOperator.AND],
            is_v3=True,
        )
        # NOTE: a passthrough resolver is used (not `lambda *a, **k: None`),
        # because any callable short-circuits _resolve_placeholder and a
        # None-returning lambda would collapse every operand to None, defeating
        # the A=true / B=C=false premise.
        result, _ = cond.evaluate({}, _passthrough())
        assert result is True


# --------------------------------------------------------------------------- #
# V4-UNCHANGED GUARD — default is_v3=False must stay byte-identical to pre-   #
# patch behavior so the V4 generated path is not affected.                     #
# --------------------------------------------------------------------------- #
class TestV4UnchangedGuard:
    """With is_v3=False (the default) behavior must be byte-identical to the
    original raw-str implementation. A failure here means the V4 path regressed."""

    def test_v4_contains_is_case_sensitive(self):
        # V4 raw str: 'world' not in 'HELLO WORLD' -> False.
        cond = Condition([], [])  # default is_v3=False
        assert cond._eval_condition(
            PossibleCondition.CONTAINS, "HELLO WORLD", "world"
        ) is False

    def test_v4_precedence_flat_fold(self):
        # V4 flat left-fold: (A OR B) AND C = (True OR False) AND False = False.
        a = ResolvedCondition("1", PossibleCondition.EQUALS, "1")  # True
        b = ResolvedCondition("1", PossibleCondition.EQUALS, "2")  # False
        c = ResolvedCondition("1", PossibleCondition.EQUALS, "2")  # False
        cond = Condition(
            [a, b, c],
            [ConcatenationOperator.OR, ConcatenationOperator.AND],
            # is_v3 defaults to False
        )
        result, _ = cond.evaluate({}, _passthrough())
        assert result is False


# --------------------------------------------------------------------------- #
# PARITY-GUARD — expected to PASS now (lock in already-correct behavior).      #
# --------------------------------------------------------------------------- #
class TestAlreadyCorrectParityGuard:
    """These assert behavior that is ALREADY V2-correct; they must PASS today.
    A failure here means a real regression, not the parity gap under test."""

    def test_assertion_leaf_contains_is_case_insensitive_PASS(self):
        # Assertion._eval_leaf_condition already uses _normalize_text(ci=True).
        assertion = Assertion()
        assert assertion._eval_leaf_condition(
            AssertionCondition.CONTAINS, "HELLO", "hello"
        ) is True

    def test_condition_contains_direction_is_right_in_left_PASS(self):
        # Direction is correct today (right in left); only case/fold is wrong.
        assert _COND._eval_condition(
            PossibleCondition.CONTAINS, "foobar", "foo"
        ) is True
