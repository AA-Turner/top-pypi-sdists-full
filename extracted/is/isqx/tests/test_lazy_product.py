from __future__ import annotations

from dataclasses import dataclass
from decimal import (
    Decimal,
    InvalidOperation,
    getcontext,
    localcontext,
)
from fractions import Fraction

import pytest
from isqx import (
    LazyProduct,
    Number,
)

LP = 8
DP = 28
HP = 50


@dataclass
class LFCase:
    products_input: tuple[tuple[Number, Fraction | int] | Number, ...]
    expected_value: Fraction | str | None
    precision: int | None
    expected_exception: type[Exception] | None


LF_CASES = [
    # no exponent
    LFCase(tuple(), Fraction(1), DP, None),
    LFCase((0,), Fraction(0), DP, None),
    LFCase((1,), Fraction(1), DP, None),
    LFCase((5,), Fraction(5), DP, None),
    LFCase((-5,), Fraction(-5), DP, None),
    LFCase((Fraction(3, 4),), Fraction(3, 4), DP, None),
    LFCase((2.5,), Fraction(5, 2), DP, None),
    LFCase((0.125,), Fraction(1, 8), DP, None),
    LFCase((0.1,), Fraction(3602879701896397, 36028797018963968), DP, None),
    LFCase((Decimal("2.5"),), Fraction(5, 2), DP, None),
    LFCase((Decimal("0.1"),), Fraction(1, 10), DP, None),
    # (Decimal, int)
    LFCase(((Decimal("0.5"), 3),), Fraction(1, 8), DP, None),
    LFCase(((Decimal("0.5"), -3),), Fraction(8), DP, None),
    # (Fraction, int)
    LFCase(((Fraction(2, 3), 2),), Fraction(4, 9), DP, None),
    LFCase(((Fraction(2, 3), -2),), Fraction(9, 4), DP, None),
    # (float, int)
    LFCase(((2.5, 2),), "6.25", DP, None),
    LFCase(((2.0, -2),), "0.25", DP, None),
    LFCase(((0.1, 2),), "0.01000000000000000111022302462", DP, None),  # inexact
    # (int, int)
    LFCase(((2, 3),), Fraction(8), DP, None),
    LFCase(((2, -3),), Fraction(1, 8), DP, None),
    LFCase(((2, 0),), Fraction(1), DP, None),
    LFCase(((2, 1),), Fraction(2), DP, None),
    # (Decimal, Fraction)
    LFCase(
        ((Decimal("16"), Fraction(1, 4)),),
        "2.000000000000000000000000000",
        DP,
        None,
    ),
    LFCase(
        ((Decimal("2"), Fraction(1, 2)),),
        "1.414213562373095048801688724",
        DP,
        None,
    ),
    # (Fraction, Fraction)
    LFCase(
        ((Fraction(1, 4), Fraction(1, 2)),),
        "0.5000000000000000000000000000",
        DP,
        None,
    ),
    LFCase(
        ((Fraction(1, 2), Fraction(1, 2)),),
        "0.7071067811865475244008443621",
        DP,
        None,
    ),
    # (float, Fraction)
    LFCase(((4.0, Fraction(1, 2)),), "2.000000000000000000000000000", DP, None),
    LFCase(
        ((0.1, Fraction(1, 2)),), "0.3162277660168379419769730258", DP, None
    ),
    # (int, Fraction)
    LFCase(((4, Fraction(1, 2)),), "2.000000000000000000000000000", DP, None),
    LFCase(((2, Fraction(1, 2)),), "1.414213562373095048801688724", DP, None),
    LFCase(((27, Fraction(2, 3)),), "9.000000000000000000000000001", DP, None),
    LFCase(((4, Fraction(-1, 2)),), "0.5000000000000000000000000000", DP, None),
    LFCase(((4, Fraction(0, 1)),), Fraction(1), DP, None),
    # 0
    LFCase(((0, 2),), Fraction(0), DP, None),
    LFCase(((0, 0),), Fraction(1), DP, None),
    LFCase(((0, Fraction(1, 2)),), Fraction(0), DP, None),
    LFCase(((0, Fraction(0, 1)),), Fraction(1), DP, None),
    LFCase(((0, -2),), None, DP, ZeroDivisionError),
    LFCase(((0, Fraction(-1, 2)),), None, DP, ZeroDivisionError),
    # 1
    LFCase(((1, 10),), Fraction(1), DP, None),
    LFCase(((1, Fraction(2, 3)),), Fraction(1), DP, None),
    # -ve
    LFCase(((-2, 2),), Fraction(4), DP, None),
    LFCase(((-2.0, 2),), "4", DP, None),
    LFCase(((-4, Fraction(1, 2)),), None, DP, InvalidOperation),
    LFCase(((-8, Fraction(1, 3)),), None, DP, InvalidOperation),
    LFCase(((Decimal("-27"), Fraction(1, 3)),), None, DP, InvalidOperation),
    # mixed
    LFCase((2, Fraction(1, 3), Decimal("3")), Fraction(2), DP, None),
    LFCase(((2.0, 2), (0.5, 1)), "2.0", DP, None),
    LFCase(
        (Fraction(1, 3), (9, Fraction(1, 2))),
        "0.9999999999999999999999999999",
        DP,
        None,
    ),
    LFCase(
        (Fraction(1, 2), (Decimal("4"), Fraction(1, 2)), (Decimal("0.5"), 1)),
        "0.5000000000000000000000000000",
        DP,
        None,
    ),
    # precision
    LFCase(((2, Fraction(1, 2)),), "1.4142136", LP, None),
    LFCase(((2, Fraction(1, 2)),), "1.414213562373095048801688724", DP, None),
    LFCase(
        ((2, Fraction(1, 2)),),
        "1.4142135623730950488016887242096980785696718753769",
        HP,
        None,
    ),
]


@pytest.mark.parametrize(
    "tc",
    [pytest.param(tc, id=f"case_{tc.products_input}") for tc in LF_CASES],
)
def test_lazy_product(
    tc: LFCase,
) -> None:
    lpwe = LazyProduct(tc.products_input)

    ctx_old = getcontext()
    with localcontext() as ctx:
        if tc.precision is not None:
            ctx.prec = tc.precision
        if tc.expected_exception:
            with pytest.raises(tc.expected_exception):
                lpwe.to_exact(ctx=ctx_old)
        else:
            result_exact = lpwe.to_exact(ctx=ctx)
            result_approx = lpwe.to_approx()
            if isinstance(tc.expected_value, Fraction):
                assert isinstance(result_exact, Fraction)
                assert result_exact == tc.expected_value
                assert result_approx == pytest.approx(float(tc.expected_value))
            elif isinstance(tc.expected_value, str):
                assert isinstance(result_exact, Decimal)
                assert str(result_exact) == tc.expected_value
                assert result_approx == pytest.approx(float(tc.expected_value))
            else:
                raise ValueError(f"unexpected {type(tc.expected_value)=}")
