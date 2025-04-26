# Copyright 2023 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.utils import MutableKwargs

# fmt: off


def test_union_inputs():
    defaults = {'a': 1, 'b': 2}
    actuals = {'b': 3, 'c': 4}
    expected_result = {'a': 1, 'b': 3, 'c': 4}

    instance = MutableKwargs(defaults, actuals)
    result = instance.union()

    assert result == expected_result


def test_union_invalid_inputs():
    defaults = {'a': 1, 'b': 2}
    actuals = 'not a dict'

    with pytest.raises(ValueError):
        instance = MutableKwargs(defaults, actuals)
        instance.union()


def test_subtract_inputs():
    defaults = {'a': 1, 'b': 2, 'c': 3}
    actuals = {'b': 2, 'c': 3, 'd': 4}
    expected_result = {'d': 4}

    instance = MutableKwargs(defaults, actuals)
    result = instance.subtract()

    assert result == expected_result


def test_subtract_empty_inputs():
    defaults = {}
    actuals = {}
    expected_result = {}

    instance = MutableKwargs(defaults, actuals)
    result = instance.subtract()

    assert result == expected_result


def test_subtract_missing_defaults():
    defaults = {'a': 1, 'b': 2}
    actuals = {'c': 3}

    instance = MutableKwargs(defaults, actuals)
    result = instance.subtract()

    assert result == actuals
