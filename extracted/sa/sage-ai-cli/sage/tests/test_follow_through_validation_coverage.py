"""Full-branch tests for sage.core.follow_through_validation.FollowThroughValidator."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from sage.core.follow_through_validation import FollowThroughValidator


@pytest.fixture
def validator():
    return FollowThroughValidator()


class TestPromiseDetection:

    def test_matches_i_will_list_n(self, validator):
        text = "I will list 5 improvements:\n1. one\n2. two"
        ok, issues = validator.validate(text)
        assert not ok
        assert "Promised 5" in issues[0]
        assert "only provided 2" in issues[0]

    def test_matches_here_are_n_items(self, validator):
        text = "Here are 3 items:\n1. a\n2. b\n3. c"
        ok, issues = validator.validate(text)
        assert ok
        assert issues == []

    def test_matches_providing_n(self, validator):
        text = "Providing 4 things\n1. x"
        ok, issues = validator.validate(text)
        assert not ok

    def test_no_promise_no_issue(self, validator):
        text = "Here's an analysis without a promised count."
        ok, issues = validator.validate(text)
        assert ok


class TestPrematureConclusion:

    def test_premature_with_target(self, validator):
        cls = SimpleNamespace(quantity_required=10, min_items=10)
        # Trigger the "that's all items" premature regex specifically.
        text = "1. one\n2. two\nThat's all items."
        ok, issues = validator.validate(text, classification=cls)
        assert not ok
        assert any("Premature conclusion" in i for i in issues)

    def test_premature_below_target_via_min_items(self, validator):
        cls = SimpleNamespace(quantity_required=0, min_items=5)
        text = "1. a\nI hope this helps."
        ok, issues = validator.validate(text, classification=cls)
        assert not ok

    def test_premature_no_target_no_issue(self, validator):
        text = "1. a\nThat's all."
        ok, issues = validator.validate(text)
        # min_items=0 → completion check skipped, premature check skipped
        assert ok


class TestCompletionPercentage:

    def test_below_90_fails(self, validator):
        cls = SimpleNamespace(quantity_required=0, min_items=10)
        text = "1. one\n2. two"  # 20% complete
        ok, issues = validator.validate(text, classification=cls)
        assert not ok
        assert any("20% complete" in i for i in issues)

    def test_at_90_passes(self, validator):
        cls = SimpleNamespace(quantity_required=0, min_items=10)
        body = "\n".join(f"{i}. item" for i in range(1, 10))  # 9 items = 90%
        ok, _ = validator.validate(body, classification=cls)
        assert ok

    def test_no_classification_skips_check(self, validator):
        ok, issues = validator.validate("1. a")
        assert ok
        assert issues == []
