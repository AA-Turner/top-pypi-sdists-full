import uuid
from datetime import date, datetime, time
from decimal import Decimal

import pytest
from Microsoft.PowerFx.Types import (  # type: ignore
    BlankValue,
    BooleanValue,
    DateTimeValue,
    DecimalValue,
    FormulaValue,
    GuidValue,
    RecordValue,
    TableValue,
    TimeValue,
)

from powerfx._utility import _formulavalue_to_python, _python_to_formulavalue


def _assert_numeric_roundtrip(py_in, py_out):
    """
    Power Fx 'Number' is double; ints will come back as float.
    Compare numerically using approx for floats/ints; exact for Decimal.
    """
    if isinstance(py_in, Decimal):
        assert isinstance(py_out, Decimal)
        assert py_out == py_in
    else:
        # int or float from Python will likely come back as float
        assert isinstance(py_out, (int, float))
        assert float(py_out) == pytest.approx(float(py_in))


def _assert_deep_equal(a, b):
    """
    Deep equality supporting:
      - numeric tolerance for int/float
      - exact equality for Decimal
      - exact equality for date/datetime/time/UUID
      - recursive compare for dict/list
    """
    # Decimal: exact
    if isinstance(a, Decimal):
        assert isinstance(b, Decimal)
        assert a == b
        return

    # Numeric (int/float): approx
    if isinstance(a, (int, float)):
        assert isinstance(b, (int, float))
        assert float(b) == pytest.approx(float(a))
        return

    # Dates/times
    if isinstance(a, datetime):
        assert isinstance(b, datetime)
        assert a == b
        return

    if isinstance(a, date) and not isinstance(a, datetime):
        assert isinstance(b, date) and not isinstance(b, datetime)
        assert a == b
        return

    if isinstance(a, time):
        assert isinstance(b, time)
        assert a == b
        return

    # UUID
    if isinstance(a, uuid.UUID):
        assert isinstance(b, uuid.UUID)
        assert a == b
        return

    # Dict
    if isinstance(a, dict):
        assert isinstance(b, dict)
        assert set(a.keys()) == set(b.keys())
        for k in a:
            _assert_deep_equal(a[k], b[k])
        return

    # List
    if isinstance(a, list):
        assert isinstance(b, list)
        assert len(a) == len(b)
        for i in range(len(a)):
            _assert_deep_equal(a[i], b[i])
        return

    # Fallback: direct equality
    assert a == b


class TestPythonToFormulaValue:
    """Test conversion from Python objects to PowerFx FormulaValue types, including roundtrip."""

    def test_none_to_blank_roundtrip(self):
        result = _python_to_formulavalue(None)
        assert isinstance(result, BlankValue)
        back = _formulavalue_to_python(result)
        assert back is None

    def test_bool_to_boolean_value_roundtrip(self):
        for b in (True, False):
            fv = _python_to_formulavalue(b)
            assert isinstance(fv, BooleanValue)  # underlying BooleanValue
            back = _formulavalue_to_python(fv)
            assert isinstance(back, bool)
            assert back is b

    def test_string_to_string_value_roundtrip(self):
        test_cases = ["hello", "world", "", "special chars: !@#$%"]
        for s in test_cases:
            fv = _python_to_formulavalue(s)
            assert isinstance(fv, FormulaValue)
            back = _formulavalue_to_python(fv)
            assert isinstance(back, str)
            assert back == s

    def test_int_to_number_value_roundtrip(self):
        # keep ints within double-precision safe integer range for exactness
        test_cases = [0, 1, -1, 42, -999, 1_000_000, 9_007_199_254_740_991 // 2]  # <= 2^53-1
        for n in test_cases:
            fv = _python_to_formulavalue(n)
            assert isinstance(fv, FormulaValue)
            back = _formulavalue_to_python(fv)
            _assert_numeric_roundtrip(n, back)

    def test_float_to_number_value_roundtrip(self):
        test_cases = [0.0, 1.5, -2.7, 3.14159, 1e6, -1e-3]
        for x in test_cases:
            fv = _python_to_formulavalue(x)
            assert isinstance(fv, FormulaValue)
            back = _formulavalue_to_python(fv)
            _assert_numeric_roundtrip(x, back)

    def test_decimal_to_decimal_value_roundtrip(self):
        test_cases = [Decimal("0"), Decimal("1.23"), Decimal("-45.67"), Decimal("999.999")]
        for d in test_cases:
            fv = _python_to_formulavalue(d)
            assert isinstance(fv, DecimalValue)
            back = _formulavalue_to_python(fv)
            _assert_numeric_roundtrip(d, back)

    def test_date_to_date_value_roundtrip(self):
        test_cases = [
            date(2023, 1, 1),
            date(2023, 12, 31),
            date(1900, 1, 1),
            date(2050, 6, 15),
        ]
        for dt in test_cases:
            fv = _python_to_formulavalue(dt)
            assert isinstance(fv, FormulaValue)
            back = _formulavalue_to_python(fv)
            assert isinstance(back, date)
            assert back == dt

    def test_datetime_to_datetime_value_roundtrip(self):
        # use millisecond-aligned microseconds to match common .NET DateTime precision
        test_cases = [
            datetime(2023, 1, 1, 0, 0, 0),
            datetime(2023, 12, 31, 23, 59, 59),
            datetime(2023, 6, 15, 12, 30, 45, 123000),
        ]
        for dt in test_cases:
            fv = _python_to_formulavalue(dt)
            assert isinstance(fv, DateTimeValue)
            back = _formulavalue_to_python(fv)
            assert isinstance(back, datetime)
            assert back == dt  # both are naive (no tz)

    def test_time_to_time_value_roundtrip(self):
        # microseconds chosen to be representable after roundtrip
        test_cases = [
            time(0, 0, 0),
            time(12, 30, 45),
            time(23, 59, 59),
            time(9, 15, 30, 500000),
        ]
        for t in test_cases:
            fv = _python_to_formulavalue(t)
            assert isinstance(fv, TimeValue)
            back = _formulavalue_to_python(fv)
            assert isinstance(back, time)
            assert back == t

    def test_uuid_to_guid_value_roundtrip(self):
        test_cases = [
            uuid.uuid4(),
            uuid.UUID("12345678-1234-5678-1234-567812345678"),
            uuid.UUID("00000000-0000-0000-0000-000000000000"),
        ]
        for g in test_cases:
            fv = _python_to_formulavalue(g)
            assert isinstance(fv, GuidValue)
            back = _formulavalue_to_python(fv)
            assert isinstance(back, uuid.UUID)
            assert back == g

    def test_dict_to_record_value_roundtrip(self):
        guid = uuid.UUID("11111111-2222-3333-4444-555555555555")
        cases = [
            {},
            {"a": 1, "b": "x"},
            {"pi": 3.14159, "flag": True, "n": -7, "d": Decimal("1.2300")},
            {
                "when": date(2024, 2, 29),
                "at": datetime(2024, 2, 29, 6, 7, 8, 999000),
                "t": time(1, 2, 3, 456000),
                "id": guid,
            },
            {
                "nested": {"x": 1, "y": Decimal("2.50")},
                "list": [1, 2, 3],  # becomes a nested TableValue inside the record, back to list
            },
        ]
        for d in cases:
            fv = _python_to_formulavalue(d)
            assert isinstance(fv, RecordValue)
            back = _formulavalue_to_python(fv)
            _assert_deep_equal(d, back)

    def test_list_to_table_value_roundtrip_single_column(self):
        # Single-column table cases (round-trip back to plain list via "flatten" heuristic)
        cases = [
            [],
            [0, 1, -2, 3.5],
            [Decimal("1.10"), Decimal("2.0000"), Decimal("-3.14159")],
            ["a", "b", "c"],
            [True, False, True],
            [uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")],
        ]
        for lst in cases:
            fv = _python_to_formulavalue(lst)
            assert isinstance(fv, TableValue)
            back = _formulavalue_to_python(fv)
            _assert_deep_equal(lst, back)

    def test_list_of_dicts_to_table_value_roundtrip_multi_column(self):
        cases = [
            [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}],
            [
                {
                    "d": Decimal("1.20"),
                    "n": 5.5,
                    "flag": False,
                    "when": date(2023, 1, 1),
                },
                {
                    "d": Decimal("0.00"),
                    "n": -2.25,
                    "flag": True,
                    "when": date(2023, 12, 31),
                },
            ],
            # Nested record inside each row:
            [
                {"k": 1, "meta": {"t": time(9, 15, 0), "id": uuid.uuid4()}},
                {"k": 2, "meta": {"t": time(10, 30, 0), "id": uuid.uuid4()}},
            ],
        ]
        for rows in cases:
            fv = _python_to_formulavalue(rows)
            assert isinstance(fv, TableValue)
            back = _formulavalue_to_python(fv)
            _assert_deep_equal(rows, back)

    def test_unsupported_type_raises_value_error(self):
        test_cases = [object(), {1, 2, 3}, frozenset({1, 2, 3}), lambda x: x]
        for unsupported in test_cases:
            with pytest.raises(ValueError, match="Unsupported Python type"):
                _python_to_formulavalue(unsupported)

    def test_edge_cases(self):
        # Empty string roundtrip
        fv = _python_to_formulavalue("")
        assert isinstance(fv, FormulaValue)
        back = _formulavalue_to_python(fv)
        assert back == ""

        # Zero values roundtrip
        for z in (0, 0.0, Decimal("0")):
            fv = _python_to_formulavalue(z)
            assert isinstance(fv, FormulaValue)
            back = _formulavalue_to_python(fv)
            if isinstance(z, Decimal):
                assert isinstance(back, Decimal)
                assert back == z
            else:
                _assert_numeric_roundtrip(z, back)

        # Large integer: only assert type (double may lose precision)
        large_int = 999_999_999_999_999_999
        fv_large = _python_to_formulavalue(large_int)
        assert isinstance(fv_large, FormulaValue)
