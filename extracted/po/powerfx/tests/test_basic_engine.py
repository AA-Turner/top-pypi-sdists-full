import pytest

from powerfx import Engine  # type: ignore


def test_eval_raises_on_incorrect_inputs():
    engine = Engine()

    # expr is a number
    with pytest.raises(TypeError, match="expr must be a string"):
        engine.eval(123, symbols={"x": 1})

    # symbols is a number
    with pytest.raises(TypeError, match=r"symbols must be a dict\[str, Any\] or None"):
        engine.eval("1+1", symbols=123)


def test_eval_raises_on_invalid_expression():
    engine = Engine()
    with pytest.raises(
        ValueError,
        match="Power Fx failed compilation: Error 4 - 14 : Invalid argument type. Expecting one of the following: Decimal, Number, Text, Boolean, Date, Time, DateTimeNoTimeZone, DateTime, UntypedObject.",
    ):
        engine.eval("1 + {Value: 1}")


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("1+1", 2),
        ("Sum(1,2,3)", 6),
        ("With({x:1}, x+2)", 3),
        ("If(true, 10, 20)", 10),
        ("Filter([1,2,3,4], Value > 2)", [3, 4]),
        ("First([1,2,3,5])", {"Value": 1}),
    ],
)
def test_basic_engine_eval(expr, expected):
    engine = Engine()
    result = engine.eval(expr)
    assert result == expected


@pytest.mark.parametrize(
    "expr,symbols,expected",
    [
        ("x + 1", {"x": 2}, 3),
        ("y * 2", {"y": 3}, 6),
        ("If(true, x, y)", {"x": 5, "y": 10}, 5),
        ("Filter(table, Value > threshold)", {"table": [1, 2, 3, 4], "threshold": 2}, [3, 4]),
        ("First(table)", {"table": [10, 20, 30]}, {"Value": 10}),
    ],
)
def test_engine_eval_with_symbols(expr, symbols, expected):
    engine = Engine()
    result = engine.eval(expr, symbols=symbols)
    assert result == expected


def test_engine_eval_locale_language_function():
    engine = Engine()
    result = engine.eval("Language()", locale="fr-FR")
    assert result == "fr-FR"


def test_engine_eval_parser_locale():
    engine = Engine()
    result = engine.eval("1,50 + 2,50", locale="fr-FR")
    assert result == 4.0


def test_engine_eval_timezone_offset_service():
    engine = Engine()
    expr = "TimeZoneOffset(Date(2024, 1, 15))"

    timezone_cases = (
        ("America/Los_Angeles", 480.0),
        ("Pacific Standard Time", 480.0),
        ("Europe/Berlin", -60.0),
        ("W. Europe Standard Time", -60.0),
    )

    for tz_id, expected in timezone_cases:
        try:
            offset = engine.eval(expr, timezone=tz_id)
        except ValueError:
            continue
        assert offset == pytest.approx(expected)
        break
    else:
        pytest.skip("No supported timezone IDs found for this platform")


def test_engine_eval_invalid_locale_empty_string():
    engine = Engine()
    with pytest.raises(ValueError, match="Locale/culture string cannot be empty"):
        engine.eval("1", locale="")


def test_engine_eval_invalid_locale_unknown():
    engine = Engine()
    with pytest.raises(ValueError, match=r"Unknown locale/culture: xx-INVALID"):
        engine.eval("1", locale="xx-INVALID")


def test_engine_eval_invalid_timezone_empty_string():
    engine = Engine()
    with pytest.raises(ValueError, match="TimeZoneInfo id string cannot be empty"):
        engine.eval("1", timezone="")


def test_engine_eval_invalid_timezone_unknown():
    engine = Engine()
    with pytest.raises(ValueError, match=r"Unknown TimeZoneInfo id: Invalid/Zone"):
        engine.eval("1", timezone="Invalid/Zone")
