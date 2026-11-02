from __future__ import annotations

import pytest
import re

from pointblank.thresholds import (
    Thresholds,
    Actions,
    _convert_abs_count_to_fraction,
    _normalize_thresholds_creation,
    _threshold_check,
)


def test_thresholds_default():
    t = Thresholds()

    assert t.warning_fraction is None
    assert t.warning_count is None

    assert t.error_fraction is None
    assert t.error_count is None

    assert t.critical_fraction is None
    assert t.critical_count is None


def test_thresholds_absolute():
    t = Thresholds(warning=1, error=2, critical=3)

    assert t.warning_fraction is None
    assert t.warning_count == 1

    assert t.error_fraction is None
    assert t.error_count == 2

    assert t.critical_fraction is None
    assert t.critical_count == 3


def test_thresholds_fractional_0_1():
    t = Thresholds(warning=0.01, error=0.1464, critical=0.9999)

    assert t.warning_fraction == 0.01
    assert t.warning_count is None

    assert t.error_fraction == 0.1464
    assert t.error_count is None

    assert t.critical_fraction == 0.9999
    assert t.critical_count is None


def test_thresholds_zero():
    t = Thresholds(warning=0, error=0, critical=0)

    assert t.warning_fraction == 0
    assert t.warning_count == 0

    assert t.error_fraction == 0
    assert t.error_count == 0

    assert t.critical_fraction == 0
    assert t.critical_count == 0


def test_thresholds_absolute_rounded():
    t = Thresholds(warning=1.4, error=2.99, critical=4.5)

    assert t.warning_fraction is None
    assert t.warning_count == 1

    assert t.error_fraction is None
    assert t.error_count == 3

    assert t.critical_fraction is None
    assert t.critical_count == 4


@pytest.mark.parametrize(
    "param, value",
    [
        ("warning", -1),
        ("warning", -0.1),
        ("error", -1),
        ("error", -0.1),
        ("critical", -1),
        ("critical", -0.1),
    ],
)
def test_thresholds_raises_on_negative(param, value):
    with pytest.raises(ValueError):
        Thresholds(**{param: value})


def test_thresolds_repr():
    t = Thresholds(warning=1, error=2, critical=3)
    assert repr(t) == "Thresholds(warning=1, error=2, critical=3)"
    assert str(t) == "Thresholds(warning=1, error=2, critical=3)"


@pytest.mark.parametrize("level", ["warning", "error", "critical"])
def test_threshold_get_default(level):
    t = Thresholds()
    assert t._get_threshold_value(level=level) is None


@pytest.mark.parametrize("level", ["warning", "error", "critical"])
def test_threshold_get_zero(level):
    t = Thresholds(warning=0, error=0, critical=0)
    assert t._get_threshold_value(level=level) == 0


@pytest.mark.parametrize(
    "level, expected_value",
    [
        ("warning", 1),
        ("error", 2),
        ("critical", 3),
    ],
)
def test_threshold_get_absolute(level, expected_value):
    t = Thresholds(warning=1, error=2, critical=3)
    assert t._get_threshold_value(level=level) == expected_value


@pytest.mark.parametrize(
    "level, value",
    [
        ("warning", 0.1),
        ("error", 0.2),
        ("critical", 0.3),
    ],
)
def test_threshold_get_fractional_0_1(level, value):
    t = Thresholds(warning=0.1, error=0.2, critical=0.3)
    assert t._get_threshold_value(level=level) == value


@pytest.mark.parametrize(
    "fraction_failing, test_units, level, expected",
    [
        (0.1, 100, "warning", False),
        (0.25, 100, "warning", True),
        (0.3, 100, "warning", True),
        (0.4, 100, "error", False),
        (0.5, 100, "error", True),
        (0.6, 100, "error", True),
        (0.74, 100, "critical", False),
        (0.75, 100, "critical", True),
        (0.76, 100, "critical", True),
    ],
)
def test_threshold_result_fractional(fraction_failing, test_units, level, expected):
    t = Thresholds(warning=0.25, error=0.5, critical=0.75)
    assert (
        t._threshold_result(fraction_failing=fraction_failing, test_units=test_units, level=level)
        == expected
    )


@pytest.mark.parametrize(
    "fraction_failing, test_units, level, expected",
    [
        (0.1, 100, "warning", False),
        (0.25, 100, "warning", True),
        (0.3, 100, "warning", True),
        (0.4, 100, "error", False),
        (0.5, 100, "error", True),
        (0.6, 100, "error", True),
        (0.74, 100, "critical", False),
        (0.75, 100, "critical", True),
        (0.76, 100, "critical", True),
    ],
)
def test_threshold_result_absolute(fraction_failing, test_units, level, expected):
    t = Thresholds(warning=25, error=50, critical=75)
    assert (
        t._threshold_result(fraction_failing=fraction_failing, test_units=test_units, level=level)
        == expected
    )


@pytest.mark.parametrize(
    "level",
    ["warning", "error", "critical"],
)
def test_threshold_result_zero(level):
    t = Thresholds(warning=0, error=0, critical=0)

    assert t._threshold_result(fraction_failing=0, test_units=100, level=level) is True
    assert t._threshold_result(fraction_failing=0.1, test_units=100, level=level) is True
    assert t._threshold_result(fraction_failing=1.5, test_units=100, level=level) is True


@pytest.mark.parametrize(
    "level",
    ["warning", "error", "critical"],
)
def test_threshold_result_none(level):
    t = Thresholds()

    assert t._threshold_result(fraction_failing=0, test_units=100, level=level) is None
    assert t._threshold_result(fraction_failing=0.1, test_units=100, level=level) is None
    assert t._threshold_result(fraction_failing=1.5, test_units=100, level=level) is None


@pytest.mark.parametrize(
    "value, test_units, expected",
    [
        (None, 100, None),
        (1, 100, 0.01),
        (1, 1e7, 1e-07),
        (1, 1e10, 1e-10),
        (0, 100, 0.0),
        (1.6, 10, 0.2),
        (1.4, 10, 0.1),
        (100, 100, 1.0),
        (150, 100, 1.5),
    ],
)
def test_convert_abs_count_to_fraction(value, test_units, expected):
    assert _convert_abs_count_to_fraction(value=value, test_units=test_units) == expected


@pytest.mark.parametrize(
    "value, test_units",
    [
        (0, 100),
    ],
)
def test_convert_abs_count_to_fraction_type(value, test_units):
    assert isinstance(_convert_abs_count_to_fraction(value=value, test_units=test_units), float)


def test_convert_abs_count_to_fraction_raises():
    with pytest.raises(ValueError):
        _convert_abs_count_to_fraction(value=-1, test_units=100)
    with pytest.raises(ValueError):
        _convert_abs_count_to_fraction(value=-0.1, test_units=100)
    with pytest.raises(ValueError):
        _convert_abs_count_to_fraction(value=3, test_units=-100)
    with pytest.raises(ValueError):
        _convert_abs_count_to_fraction(value=3, test_units=0)


def test_normalize_thresholds_creation():
    # None should be equivalent to the default Thresholds object
    assert _normalize_thresholds_creation(thresholds=None) == Thresholds()

    # Use of integers or floats should be equivalent, applying the value to the `warning` attribute
    assert _normalize_thresholds_creation(thresholds=1) == Thresholds(
        warning=1, error=None, critical=None
    )
    assert _normalize_thresholds_creation(thresholds=0.5) == Thresholds(
        warning=0.5, error=None, critical=None
    )

    # Use of a tuple will vary depending on the length of the tuple
    assert _normalize_thresholds_creation(thresholds=(1,)) == Thresholds(
        warning=1, error=None, critical=None
    )
    assert _normalize_thresholds_creation(thresholds=(0.2, 20)) == Thresholds(
        warning=0.2, error=20, critical=None
    )
    assert _normalize_thresholds_creation(thresholds=(0.2, 20, 0.5)) == Thresholds(
        warning=0.2, error=20, critical=0.5
    )

    # ...but the tuple should have 1-3 elements, otherwise it should raise an error
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds=(1, 2, 3, 4))
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds=())

    # Use of a dictionary should convert the dictionary to a Thresholds object
    assert _normalize_thresholds_creation(thresholds={"warning": 1}) == Thresholds(
        warning=1, error=None, critical=None
    )
    assert _normalize_thresholds_creation(thresholds={"warning": 0.2, "error": 20}) == Thresholds(
        warning=0.2, error=20, critical=None
    )
    assert _normalize_thresholds_creation(
        thresholds={"warning": 0.2, "error": 20, "critical": 0.5}
    ) == Thresholds(warning=0.2, error=20, critical=0.5)
    assert _normalize_thresholds_creation(thresholds={}) == Thresholds()

    # ...but the dictionary keys need to be valid Thresholds attributes
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(
            thresholds={"warning": 1, "error": 2, "critical": 3, "extra": 4}
        )
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds={"warning": 1, "error": 2, "invalid": 3})
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds={"warnings_at": 1})

    # Use of a Thresholds object should return the object as is
    assert _normalize_thresholds_creation(thresholds=Thresholds()) == Thresholds()
    assert _normalize_thresholds_creation(
        thresholds=Thresholds(warning=1, critical=0.5)
    ) == Thresholds(warning=1, critical=0.5)

    # Anything else should raise an error
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds="not a valid value")
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds=1.0 + 1j)
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds=[])
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds=[0.2])
    with pytest.raises(ValueError):
        _normalize_thresholds_creation(thresholds=object())


def test_threshold_check():
    assert _threshold_check(failing_test_units=6, threshold=5) is False
    assert _threshold_check(failing_test_units=5, threshold=5) is False
    assert _threshold_check(failing_test_units=4, threshold=5) is True
    assert _threshold_check(failing_test_units=0, threshold=0) is False
    assert _threshold_check(failing_test_units=80, threshold=None) is False


def test_actions_default():
    a = Actions()

    assert a.warning is None
    assert a.error is None
    assert a.critical is None


def test_actions_repr():
    a = Actions()
    assert repr(a) == "Actions(warning=None, error=None, critical=None)"
    assert str(a) == "Actions(warning=None, error=None, critical=None)"


def test_actions_str_inputs():
    a = Actions(warning="bad", error="badder", critical="worst")

    assert a.warning == ["bad"]
    assert a.error == ["badder"]
    assert a.critical == ["worst"]


def test_actions_callable_inputs():
    def warn():
        return "warning"

    def stop():
        return "stopping"

    def notify():
        return "notifying"

    a = Actions(warning=warn, error=stop, critical=notify)

    assert callable(a.warning[0])
    assert callable(a.error[0])
    assert callable(a.critical[0])

    assert a.warning[0]() == "warning"
    assert a.error[0]() == "stopping"
    assert a.critical[0]() == "notifying"

    pattern = (
        r"Actions\(warning=\[<function.*?>\], error=\[<function.*?>\], critical=\[<function.*?>\]\)"
    )
    assert re.match(pattern, repr(a))


def test_actions_list_inputs():
    def warn():
        return "warning function"

    def stop():
        return "stopping function"

    def notify():
        return "notifying function"

    a = Actions(
        warning=[warn, "warning string"], error=["stopping string", stop], critical=[notify]
    )

    assert callable(a.warning[0])
    assert isinstance(a.warning[1], str)
    assert isinstance(a.error[0], str)
    assert callable(a.error[1])
    assert callable(a.critical[0])

    assert a.warning[0]() == "warning function"
    assert a.warning[1] == "warning string"
    assert a.error[0] == "stopping string"
    assert a.error[1]() == "stopping function"
    assert a.critical[0]() == "notifying function"
