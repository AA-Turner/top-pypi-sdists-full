"""Tests for _has_non_standard_float."""

import math

from agentic_devtools.cli.workflows.orchestrator_commands import _has_non_standard_float


def test_returns_false_for_normal_values():
    assert _has_non_standard_float(1) is False
    assert _has_non_standard_float(1.5) is False
    assert _has_non_standard_float("NaN") is False
    assert _has_non_standard_float(None) is False
    assert _has_non_standard_float({"x": 1, "y": "ok"}) is False
    assert _has_non_standard_float([1, 2, 3]) is False


def test_returns_true_for_nan():
    assert _has_non_standard_float(float("nan")) is True


def test_returns_true_for_infinity():
    assert _has_non_standard_float(float("inf")) is True
    assert _has_non_standard_float(float("-inf")) is True
    assert _has_non_standard_float(math.inf) is True


def test_detects_nan_in_nested_dict_value():
    assert _has_non_standard_float({"event": "review", "score": float("nan")}) is True


def test_detects_infinity_in_nested_list():
    assert _has_non_standard_float([1, float("inf"), 3]) is True


def test_detects_nan_in_deeply_nested_structure():
    assert _has_non_standard_float({"a": {"b": [1, float("nan")]}}) is True


def test_returns_false_for_empty_collections():
    assert _has_non_standard_float({}) is False
    assert _has_non_standard_float([]) is False
