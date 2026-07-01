import math
from decimal import getcontext
from fractions import Fraction

import pytest

from isqx import (
    CELSIUS,
    DAY,
    HOUR,
    M_PERS,
    MIN,
    RAD,
    A,
    BaseUnit,
    CompositionError,
    Dimensionless,
    DimensionMismatchError,
    Exp,
    KindMismatchError,
    LazyProduct,
    M,
    Mul,
    S,
    Scaled,
    Tagged,
    convert,
    dimension,
    simplify,
)
from isqx.aerospace import GEOMETRIC_ALTITUDE, GEOPOTENTIAL_ALTITUDE
from isqx.usc import FT

#
# OpsMixin
#


def test_op_mixin() -> None:
    # pow
    assert M**2 == Exp(M, 2)
    assert M ** Fraction(1, 2) == Exp(M, Fraction(1, 2))

    # mul expr * expr and flattening
    assert M * S == Mul((M, S))
    assert S * A * M == Mul((S, A, M))
    assert S * (A * M) == Mul((S, A, M))
    # rmul factor * expr, mul expr * factor
    assert 2 * M == Scaled(M, 2)
    assert M * 2 == Scaled(M, 2)

    # truediv expr / expr, expr / factor
    assert M / 2 == Scaled(M, LazyProduct(((2, -1),)))
    assert M / S == Mul((M, Exp(S, -1)))

    assert (M * 2) / S == Mul((Scaled(M, 2), Exp(S, -1)))
    assert 3 * (M * 2) == Scaled(Scaled(M, 2), 3)


#
# Exp
#


def test_exp_invalid() -> None:
    with pytest.raises(CompositionError, match="zero"):
        _u1 = Exp(M, 0)


def test_exp_eq() -> None:
    assert M**2 == Exp(M, Fraction(2))


def test_exp_dimension() -> None:
    assert dimension(M**2) == Exp(dimension(M), 2)
    assert dimension((M**2) ** 3) == Exp(Exp(dimension(M), 2), 3)


def test_exp_simplify() -> None:
    # distribute exponent
    expr0s = simplify((M**2) ** Fraction(1, 2))
    assert isinstance(expr0s, BaseUnit)
    assert expr0s == M

    expr0s = simplify((M**2) ** 3)
    assert isinstance(expr0s, Exp)
    assert expr0s == Exp(M, 6)


#
# Mul
#


def test_mul_invalid() -> None:
    from isqx import MixedKindError

    with pytest.raises(CompositionError, match="empty"):
        _u0 = Mul(tuple())
    with pytest.raises(MixedKindError):
        _u1 = Mul((M, dimension(M)))


FT_PERMIN = FT * MIN**-1


def test_mul_dimension() -> None:
    assert dimension(M_PERS) == Mul((dimension(M), Exp(dimension(S), -1)))


def test_mul_simplify_basic() -> None:
    # cancel terms
    expr1s = simplify(M * M**-1)
    assert isinstance(expr1s, Dimensionless)

    # distribute inner
    expr2s = simplify(M_PERS**2)
    assert isinstance(expr2s, Mul)
    assert expr2s.terms == (M**2 * S**-2).terms

    # combine terms with same base
    expr_s = simplify(M * S**-1 * M**2 * S**-2)
    assert isinstance(expr_s, Mul)
    assert expr_s.terms == (M**3 * S**-3).terms

    # return lone term if it is raised to power of one
    expr_s = simplify(Mul((M**1,)))
    assert isinstance(expr_s, BaseUnit)
    assert expr_s == M


def test_mul_simplify_nested() -> None:
    assert isinstance(simplify((M_PERS * M_PERS**-1)), Dimensionless)


def test_mul_simplify_ordering() -> None:
    PERSM = simplify(S**-1 * M)
    assert isinstance(PERSM, Mul)
    assert PERSM.terms == M_PERS.terms


#
# Scaled
#
CTX_DEFAULT = getcontext()


def test_scaled_dimension() -> None:
    assert dimension(FT) == dimension(M)


def test_scaled_simplify_nested() -> None:
    from isqx import YEAR

    expr3s = simplify(YEAR)
    assert isinstance(expr3s, Scaled)
    assert expr3s.reference == S
    assert isinstance(expr3s.factor, LazyProduct)
    assert expr3s.factor.to_exact(ctx=CTX_DEFAULT) == 86400 * 365.25


def test_scaled_simplify_mixed() -> None:
    expr4s = simplify((M * 2) ** 3 * (S * 3) ** 2)
    assert isinstance(expr4s, Scaled)
    assert expr4s.reference == (M**3 * S**2)
    assert isinstance(expr4s.factor, LazyProduct)
    assert expr4s.factor.to_exact(ctx=CTX_DEFAULT) == 2**3 * 3**2

    expr4s = simplify(FT_PERMIN)
    assert isinstance(expr4s, Scaled)
    assert expr4s.reference == M_PERS
    assert isinstance(expr4s.factor, LazyProduct)
    assert expr4s.factor.to_exact(ctx=CTX_DEFAULT) == Fraction(3048, 10000) / 60


def test_scaled_simplify_dimensionless() -> None:
    expr5s = simplify(HOUR * DAY**-1)
    assert isinstance(expr5s, Scaled)
    assert isinstance(expr5s.reference, Dimensionless)
    assert isinstance(expr5s.factor, LazyProduct)
    assert expr5s.factor.to_exact(ctx=CTX_DEFAULT) == Fraction(1, 24)


def test_scaled_simplify_with_lazy_product() -> None:
    from isqx.usc import IN  # -> ft -> m

    result = simplify(Exp(simplify(IN), 2))  # type: ignore

    assert isinstance(result, Scaled)
    assert result.reference == M**2
    assert isinstance(result.factor, LazyProduct)

    assert result.factor.to_approx() == pytest.approx((0.3048 / 12) ** 2)


def test_scaled_simplify_with_lazy_product_multiple_terms() -> None:
    from isqx import PA
    from isqx.usc import PSI

    # defined by lbf -> lbm -> kg and in -> ft -> m
    psi_simplified = simplify(PSI)  # Scaled(simplify(PA), LazyProduct(...))
    assert isinstance(psi_simplified, Scaled)
    assert isinstance(psi_simplified.factor, LazyProduct)
    assert isinstance(psi_simplified.reference, Mul)

    pa_simplified = simplify(PA)
    assert isinstance(pa_simplified, Mul)
    assert set(psi_simplified.reference.terms) == set(pa_simplified.terms)
    PSI_TO_PA_FACTOR = (0.45359237 * 9.80665) / ((0.3048 / 12) ** 2)
    assert psi_simplified.factor.to_approx() == pytest.approx(PSI_TO_PA_FACTOR)

    result = simplify(psi_simplified**2)
    assert isinstance(result, Scaled)
    assert isinstance(result.factor, LazyProduct)
    assert isinstance(result.reference, Mul)

    from isqx import KG

    result_ref_simplified = simplify(result.reference)
    assert isinstance(result_ref_simplified, Mul)
    # P**2 = (F/A)**2
    #      = ((M*L*T**-2) / L**2)**2
    #      = (M * L**-1 * T**-2)**2
    assert set(result_ref_simplified.terms) == set(
        (KG**2 * M**-2 * S**-4).terms
    )
    assert result.factor.to_approx() == pytest.approx(PSI_TO_PA_FACTOR**2)


#
# prefix
#


def test_prefix_invalid() -> None:
    from isqx import KG, KILO, G, W

    KW = KILO * W
    assert isinstance(KW, Scaled)
    assert KW.factor == KILO
    assert KW.reference == W
    with pytest.raises(CompositionError, match="prefixes cannot be applied"):
        _ = KILO * dimension(KG)
    with pytest.raises(CompositionError, match="cannot prefix `kilogram`"):
        _ = KILO * KG
    with pytest.raises(CompositionError, match="apply prefix `kilo` to `gram`"):
        _ = KILO * G
    with pytest.raises(CompositionError, match="prefixes cannot be applied"):
        _ = KILO * M_PERS
    with pytest.raises(
        CompositionError, match="prefixes cannot be applied to `Scaled`"
    ):
        _ = KILO * KW


#
# tagged
#

M_ALT_GEOM: Tagged = GEOMETRIC_ALTITUDE(M)  # type: ignore
M_ALT_GEOP: Tagged = GEOPOTENTIAL_ALTITUDE(M)  # type: ignore


def test_tagged_invalid_construction() -> None:
    with pytest.raises(CompositionError, match="nesting"):
        _ = Tagged(M_ALT_GEOP, ("another_context",))  # type: ignore


def test_tagged_simplify_cancellation() -> None:
    expr_same_ctx = M_ALT_GEOP * M_ALT_GEOP**-1
    simplified_same = simplify(expr_same_ctx)
    assert isinstance(simplified_same, Dimensionless)

    expr_diff_ctx = M_ALT_GEOP * M_ALT_GEOM**-1
    simplified_diff = simplify(expr_diff_ctx)
    assert isinstance(simplified_diff, Mul)  # shouldn't cancel
    assert set(simplified_diff.terms) == set(expr_diff_ctx.terms)


FT_ALT_GEOP: Tagged = GEOPOTENTIAL_ALTITUDE(FT)  # type: ignore


def test_tagged_simplify_propagates_to_reference() -> None:
    simplified = simplify(FT_ALT_GEOP)
    assert isinstance(simplified, Tagged)
    assert simplified.tags == M_ALT_GEOP.tags
    assert isinstance(simplified.reference, Scaled)
    assert simplified.reference.reference == M


def test_tagged_conversion() -> None:
    converter_ok = convert(M_ALT_GEOP, FT_ALT_GEOP)
    assert converter_ok(1) == pytest.approx(1 / 0.3048)

    with pytest.raises(DimensionMismatchError):
        _ = convert(M_ALT_GEOP, M_ALT_GEOM)
    with pytest.raises(DimensionMismatchError):
        _ = convert(M_ALT_GEOP, M)
    with pytest.raises(DimensionMismatchError):
        _ = convert(M, M_ALT_GEOP)


def test_qty_kind_call() -> None:
    from isqx import UnitKindMismatchError
    from isqx.aerospace import TRUE_AIRSPEED
    from isqx.usc import KNOT

    tas_mps = TRUE_AIRSPEED(M_PERS)
    assert isinstance(tas_mps, Tagged)
    assert tas_mps.reference == M_PERS
    assert tas_mps.tags == ("airspeed", "true")

    tas_knots = TRUE_AIRSPEED(KNOT)
    assert isinstance(tas_knots, Tagged)
    assert tas_knots.reference == KNOT
    assert tas_knots.tags == ("airspeed", "true")

    mps_to_knots = convert(tas_mps, tas_knots)
    assert mps_to_knots(1.0) == pytest.approx(1.94384449)

    with pytest.raises(UnitKindMismatchError, match="kind: `L · T⁻¹`"):
        _ = TRUE_AIRSPEED(M)

    alt_m = GEOPOTENTIAL_ALTITUDE(M)
    alt_ft = GEOPOTENTIAL_ALTITUDE(FT)
    assert convert(alt_m, alt_ft)(100) == pytest.approx(328.08399)

    with pytest.raises(DimensionMismatchError):
        _ = convert(tas_mps, alt_m)


#
# alias
#


def test_alias_fail() -> None:
    from isqx import Aliased

    with pytest.raises(CompositionError, match="can only wrap"):
        _ = Aliased(M, "fail")  # type: ignore


#
# Unit conversions
#


def test_convert_dimensionless() -> None:
    from isqx import SR

    assert convert(RAD, RAD)(1) == 1  # -> Dimensionless

    with pytest.raises(DimensionMismatchError):
        _fn = convert(RAD, SR)  # incompatible dim


def test_convert_base_dimension() -> None:
    from isqx import DIM_LENGTH, DIM_TIME

    with pytest.raises(DimensionMismatchError):
        _fn = convert(DIM_LENGTH, DIM_TIME)  # incompatible dim
    with pytest.raises(KindMismatchError):
        _fn = convert(DIM_LENGTH, dimension(RAD))  # -> Dimensionless
    assert convert(DIM_TIME, DIM_TIME)(1) == 1  # -> BaseDimension
    with pytest.raises(KindMismatchError):
        _fn = convert(1 * DIM_TIME, S)  # -> BaseUnit
    assert convert(DIM_TIME, DIM_TIME**1)(1) == 1  # -> Exp
    assert convert(DIM_TIME, Mul((DIM_TIME,)))(1) == 1  # -> Mul
    assert convert(DIM_TIME, 2 * DIM_TIME)(1) == 0.5  # -> Scaled


def test_convert_base_unit() -> None:
    with pytest.raises(DimensionMismatchError):
        _fn = convert(S, M)  # incompatible dim
    with pytest.raises(KindMismatchError):
        _fn = convert(S, RAD)  # -> Dimensionless
    assert convert(S, S)(1) == 1  # -> BaseUnit
    with pytest.raises(KindMismatchError):
        _fn = convert(S, dimension(S))  # -> BaseDimension
    assert convert(S, S**1)(1) == 1  # -> Exp
    assert convert(S, Mul((S,)))(1) == 1  # -> Mul
    assert convert(S, 2 * S)(1) == 0.5  # -> Scaled


def test_convert_exp() -> None:
    M2 = M**2
    with pytest.raises(DimensionMismatchError):
        _fn = convert(M2, M)  # incompatible dim
    with pytest.raises(KindMismatchError):
        _fn = convert(M2, RAD)  # -> Dimensionless
    with pytest.raises(KindMismatchError):
        _fn = convert(M2, dimension(M2))  # unit -> dimension
    assert convert(M2, M2)(1) == 1  # -> Exp
    assert convert(M2, Mul((M2,)))(1) == 1  # -> Mul
    assert convert(M2, 2 * M2)(1) == 0.5  # -> Scaled


def test_convert_mul() -> None:
    with pytest.raises(DimensionMismatchError):
        _fn = convert(M_PERS, M)  # incompatible dim
    with pytest.raises(KindMismatchError):
        _fn = convert(M_PERS, RAD)  # -> Dimensionless
    assert convert(M_PERS, M_PERS)(1) == 1  # -> Mul
    assert convert(M_PERS, 2 * M_PERS)(1) == 0.5  # -> Scaled

    M2_PERS2 = M_PERS**2  # would be simplified to Mul((Exp(...), ...))
    FT2_PERMIN2 = FT_PERMIN**2
    assert convert(M2_PERS2, FT2_PERMIN2)(1) == 60**2 * 0.3048**-2
    assert convert(M2_PERS2, M2_PERS2)(1) == 1


def test_convert_scaled() -> None:
    from isqx import MIN

    with pytest.raises(DimensionMismatchError):
        _fn = convert(DAY, M)  # incompatible dim
    with pytest.raises(KindMismatchError):
        _fn = convert(DAY, RAD)  # -> Dimensionless
    assert convert(DAY, S)(1) == 86400  # -> BaseUnit
    with pytest.raises(KindMismatchError):
        _value = convert(HOUR, dimension(S))  # -> BaseDimension
    assert convert(DAY, S**1)(1) == 86400  # -> Exp
    assert convert(DAY, Mul((S,)))(1) == 86400  # -> Mul
    assert convert(MIN, HOUR)(60) == 1  # -> Scaled
    assert convert(DAY, DAY)(1) == 1


def test_translated_is_terminal() -> None:
    from isqx import KILO, Translated

    with pytest.raises(CompositionError, match="exponentiated"):
        _ = CELSIUS**2
    with pytest.raises(CompositionError, match="part of a product"):
        _ = CELSIUS * M
    with pytest.raises(CompositionError, match="cannot be scaled"):
        _ = CELSIUS * 2
    with pytest.raises(CompositionError, match="prefixes cannot be applied"):
        _ = KILO * CELSIUS
    with pytest.raises(CompositionError, match="nesting"):
        _ = Translated(CELSIUS, 1, "celsius + 1")  # type: ignore
    with pytest.raises(CompositionError, match="must have a"):
        _ = Translated(M_PERS, 1, "m/s + 1")  # type: ignore


def test_convert_translated() -> None:
    from isqx import CELSIUS, DIM_TEMPERATURE, K, NonAffineConverter
    from isqx.usc import FAHRENHEIT, R

    assert dimension(CELSIUS) == DIM_TEMPERATURE

    assert convert(K, CELSIUS)(1.1) == -272.04999999999995  # inexact
    assert convert(K, CELSIUS, exact=True)(Fraction(11, 10)) == Fraction(
        -27205, 100
    )

    c_to_f = convert(CELSIUS, FAHRENHEIT, exact=True)
    assert isinstance(c_to_f, NonAffineConverter)
    assert isinstance(c_to_f.scale, Fraction) and c_to_f.scale == Fraction(9, 5)
    assert isinstance(c_to_f.offset, Fraction) and c_to_f.offset == Fraction(
        32, 1
    )
    assert c_to_f(100) == 212
    assert convert(CELSIUS, FAHRENHEIT).scale == 1.7999999999999998  # inexact

    f_to_c = convert(FAHRENHEIT, CELSIUS, exact=True)
    assert f_to_c(32) == 0
    assert f_to_c(212) == 100
    c_to_r = convert(CELSIUS, R, exact=True)
    assert c_to_r(0) == Fraction("273.15") * Fraction(9, 5)


def test_convert_tagged_translated() -> None:
    from isqx import CELSIUS, K

    SURFACE_TEMP_C = CELSIUS["surface"]
    SURFACE_TEMP_K = K["surface"]

    c_to_k_exact = convert(SURFACE_TEMP_C, SURFACE_TEMP_K, exact=True)
    assert c_to_k_exact(10) == Fraction(28315, 100)
    k_to_c_exact = convert(SURFACE_TEMP_K, SURFACE_TEMP_C, exact=True)
    assert k_to_c_exact(c_to_k_exact(10)) == 10

    with pytest.raises(DimensionMismatchError):
        convert(SURFACE_TEMP_C, K)
    with pytest.raises(DimensionMismatchError):
        convert(K, SURFACE_TEMP_C)


def test_log_level_invalid() -> None:
    from isqx import BEL, DB, DBV, HZ, KILO, Log, M, Quantity, V
    from isqx._core import _RATIO, _RatioBetween

    # NOTE: we allow logarithmic units to be composed with others,
    # TODO: in the future harden `convert` so we dont mess it up
    assert isinstance(DB**2, Exp)
    assert isinstance(DB * HZ**-1, Mul)
    assert isinstance(DB * 2, Scaled)
    assert isinstance(KILO * BEL, Scaled)

    assert isinstance(DBV**2, Exp)
    assert isinstance(DBV * M, Mul)
    assert isinstance(DBV * 2, Scaled)
    assert isinstance(KILO * DBV, Scaled)

    # other invalid compositions
    rb_tag = _RatioBetween(V, Quantity(1, V))
    with pytest.raises(CompositionError, match="only be applied to a ratio"):
        _ = M[rb_tag]
    with pytest.raises(CompositionError, match="wrap a `Dimensionless`"):
        _ = Log(DBV, base=10)  # type: ignore
    # with pytest.raises(CompositionError, match="must be physical"):
    #     _ = Relative(dimension(M), V)
    with pytest.raises(
        CompositionError, match="cannot be applied multiple times"
    ):
        _ = _RATIO[rb_tag, rb_tag]


def test_convert_logarithmic() -> None:
    from isqx import (
        DBM,
        DBUV,
        DBV,
        DBW,
        NPV,
        NPW,
        Converter,
        NonAffineConverter,
    )

    assert isinstance(dimension(DBM), Dimensionless)

    # power -> power
    dbw_to_dbm = convert(DBW, DBM)
    assert isinstance(dbw_to_dbm, NonAffineConverter)
    assert dbw_to_dbm.scale == 1
    assert dbw_to_dbm.offset == pytest.approx(30)
    assert dbw_to_dbm(10) == 40

    # root-power -> root-power
    dbv_to_dbuv = convert(DBV, DBUV, exact=True)
    assert isinstance(dbv_to_dbuv, NonAffineConverter)
    assert dbv_to_dbuv.scale == 1
    assert dbv_to_dbuv.offset == 120
    assert dbv_to_dbuv(1) == 121

    # neper <-> decibel (root-power, power)
    npv_to_dbv = convert(NPV, DBV)
    assert isinstance(npv_to_dbv, Converter)
    assert npv_to_dbv.scale == pytest.approx(20 / math.log(10))
    assert npv_to_dbv(1) == pytest.approx(8.6858896)
    dbv_to_npv = convert(DBV, NPV)
    assert isinstance(dbv_to_npv, Converter)
    assert dbv_to_npv.scale == pytest.approx(math.log(10) / 20)
    assert dbv_to_npv(20) == pytest.approx(2.302585)
    npw_to_dbw = convert(NPW, DBW)
    assert isinstance(npw_to_dbw, Converter)
    assert npw_to_dbw.scale == pytest.approx(20 / math.log(10))
    assert npw_to_dbw(1) == pytest.approx(8.6858896)


def test_convert_logarithmic_with_prefix() -> None:
    from isqx import DBV, DECI, MILLI, NPV, Converter

    npv_to_decinpv = convert(NPV, DECI * NPV, exact=True)
    assert isinstance(npv_to_decinpv, Converter)  # no offset
    assert npv_to_decinpv.scale == 10
    millinpv_to_decinpv = convert(MILLI * NPV, DECI * NPV, exact=True)
    assert millinpv_to_decinpv.scale == Fraction(1, 100)
    decinpv_to_dbv = convert(DECI * NPV, DBV)
    assert isinstance(decinpv_to_dbv, Converter)
    assert decinpv_to_dbv.scale == pytest.approx(200 / math.log(10))


def test_convert_logarithmic_fail() -> None:
    from isqx import DBM, DBV, NonLinearConversionError, V

    with pytest.raises(NonLinearConversionError):
        convert(V, DBV)
    with pytest.raises(NonLinearConversionError):
        convert(DBV, V)
    with pytest.raises(DimensionMismatchError):
        convert(DBV, DBM)


def test_angle_conversion() -> None:
    from decimal import Decimal, localcontext

    from isqx import DEG, PI, REV, E

    with localcontext() as ctx:
        assert PI.to_decimal(ctx) == Decimal("3.141592653589793238462643383")
        assert E.to_decimal(ctx) == Decimal("2.718281828459045235360287471")

    deg_to_rad = convert(DEG, RAD)
    assert deg_to_rad(180) == pytest.approx(math.pi)
    assert deg_to_rad(360) == pytest.approx(2 * math.pi)

    rad_to_deg = convert(RAD, DEG)
    assert rad_to_deg(math.pi) == pytest.approx(180.0)
    assert rad_to_deg(1) == pytest.approx(180 / math.pi)

    with localcontext() as ctx:
        ctx.prec = 100
        pi_100 = PI.to_decimal(ctx)

        assert convert(DEG, RAD, exact=True, ctx=ctx)(180) == pi_100
        assert convert(RAD, DEG, exact=True, ctx=ctx)(Fraction(pi_100)) == 180

    assert convert(REV, RAD)(1) == pytest.approx(2 * math.pi)
    assert convert(RAD, REV)(math.pi) == pytest.approx(0.5)
    assert convert(DEG, REV)(360) == pytest.approx(1.0)


def test_derived_angle_conversion() -> None:
    from isqx import DEG

    DEG_PER_S = DEG * S**-1
    RAD_PER_S = RAD * S**-1

    assert convert(DEG_PER_S, RAD_PER_S)(180) == pytest.approx(math.pi)

    result = convert(DEG_PER_S, RAD_PER_S, exact=True)(Fraction(180))
    assert isinstance(result, Fraction)
    assert result == pytest.approx(Fraction(math.pi))


#
# integration test
#


def test_xkcd_whatif_11() -> None:  # https://what-if.xkcd.com/11/
    from math import pi

    from isqx import CENTI, KILO, YEAR, BaseDimension, BaseUnit

    BIRD = BaseUnit(BaseDimension("bird"), "bird")
    POOP = BaseUnit(BaseDimension("poop"), "poop")
    MOUTH = BaseUnit(BaseDimension("mouth"), "mouth")

    PERIOD = simplify(
        (
            (BIRD * (KILO * M) ** -2)
            * (POOP * BIRD**-1 * HOUR**-1)
            * (HOUR * DAY**-1)
            * (MOUTH * POOP**-1)
            * ((CENTI * M) ** 2 * MOUTH**-1)
        )
        ** -1
    )  # = (km^2 * day) / cm^2
    assert isinstance(PERIOD, Scaled)
    assert isinstance(PERIOD.factor, LazyProduct)
    assert PERIOD.factor.to_exact(ctx=CTX_DEFAULT) == 100_000**2 * 86400
    assert PERIOD.reference == S

    num_birds = 300e9
    earth_surface_area = 4 * pi * 6378**2
    period_yr = convert(PERIOD, YEAR)(
        1
        / (
            (num_birds / earth_surface_area)  # bird / km^2
            * 1  # poop / (bird * hour)
            * 16  # hours / day
            * 1  # mouth / poop
            * 15  # cm^2 / mouth
        )
    )
    assert period_yr == pytest.approx(195, abs=0.7)

    from isqx import MILLI, YEAR
    from isqx.usc import FL_OZ, MI, MPG

    MM2 = (MILLI * M) ** 2
    assert convert(MPG**-1, MM2)(1 / 20) == pytest.approx(0.11760729)
    poop_dropping_rate = 0.5  # fl_oz / (day * bird)
    total_distance_driven_rate = 3e12  # mi / year
    assert 1 / (
        convert(
            BIRD  #
            * (FL_OZ * DAY**-1 * BIRD**-1)
            * (MI * YEAR**-1) ** -1,
            MPG**-1,
        )(num_birds * poop_dropping_rate / total_distance_driven_rate)
    ) == pytest.approx(7.009, rel=1e-3)  #  xkcd's 13MPG is wrong
