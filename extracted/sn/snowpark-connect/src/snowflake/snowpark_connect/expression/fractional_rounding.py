#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Spark-compatible HALF_UP / HALF_EVEN rounding of FLOAT/DOUBLE values.

Spark rounds a double through ``BigDecimal(Double.toString(x))``, i.e. on the
shortest decimal ``D`` that converts back to ``x`` (Java 17 prints a few
values with more digits, see ``_round_long_valued``). Snowflake's
``ROUND(FLOAT)`` and ``CAST(FLOAT AS NUMBER)`` round the exact IEEE value
instead, so ``1.005`` (stored as ``1.00499999999999989...``) rounds to ``1.0``
where Spark returns ``1.01`` (SNOW-4193976).

``spark_round_fractional`` picks, per row, the cheapest rule that is exact:

* ``|x| * 10^s < 2^48`` (``2^52`` at scale 0): ``floor_units = FLOOR(|x| * 10^s)``
  and the tie point ``(floor_units + 0.5) / 10^s`` are exact or correctly
  rounded doubles, and ``|x|`` equals the tie exactly when ``D`` is the tie,
  so the mode settles it.
* up to ``10^16`` units: ``D`` has 16-17 significant digits, which no native
  function produces. ``_round_decimal`` brackets it with NUMBER/DECFLOAT
  decimals converted back to double (Snowflake converts correctly rounded)
  and, near a tie, compares the exact binary value in 38 digits.
* from ``10^16`` units on, NaN and +-Infinity: ``x`` is returned unchanged,
  as the double has no digit below the rounding position.

Snowflake's ``ROUND(FLOAT)`` is not a usable fallback anywhere: it returns
9.999999999999998e19 for ``ROUND(1e20, 3)``.
"""


from collections import defaultdict
from collections.abc import Callable
from decimal import Decimal, localcontext

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark.column import Column
from snowflake.snowpark.types import DecFloatType, DecimalType, DoubleType

# 10**22 is the largest power of ten a double holds exactly.
_MAX_EXACT_POW10_EXPONENT = 22
_MAX_DOUBLE_POW10_EXPONENT = 308
# Below 2**52, k + 0.5 is exact and the result is correctly rounded.
_MAX_SCALED_MAGNITUDE = float(2**52)
# Below 2**48 units, (k + 0.5) / 10^s is the shortest decimal of the tie point.
_MAX_DOUBLE_TIE_SCALED_MAGNITUDE = float(2**48)
_UNCHANGED_SCALED_MAGNITUDE = 1e16
# NUMBER has at most 37 decimals: scale + 6 <= 37.
_MAX_NUMBER_ROUNDING_SCALE = 31
# At scale -21, 10^16 units and the next unit up still fit NUMBER(38, 0).
_MAX_NUMBER_INTEGER_ROUNDING_SCALE = 21
# Beyond 324 + 17 decimals rounding keeps every double.
_MAX_DOUBLE_DECIMAL_PLACES = 341
_MAX_LONG_VALUED_ROUNDING_SCALE = 19
# Column of the UDF body's derived table. The caller query never sees this alias.
_BOUND_INPUT_NAME = "SPARK_FP_INPUT"
# ``register_cached_sql_udf`` names parameters arg0, arg1, ... Unquoted, so it
# matches the parameter (a quoted "arg0" would not).
_UDF_PARAMETER_NAME = "arg0"


class _SqlRenderSession:
    """Session stand-in so expression SQL can be rendered without a connection.

    ``eliminate_numeric_sql_value_cast_enabled`` stays false so the casts the
    rounding rules depend on are not stripped.
    """

    _join_alias_fix = False
    eliminate_numeric_sql_value_cast_enabled = False


def _render_sql(expression: object) -> str:
    from snowflake.snowpark._internal.analyzer.analyzer import Analyzer

    return Analyzer(_SqlRenderSession()).analyze(expression, defaultdict())


def sql_udf_body(build: Callable[[Column], Column]) -> str:
    """SQL UDF body that names ``arg0`` once.

    Snowflake does not CSE, and a correlated scalar subquery in the caller's
    SELECT list is not allowed: a derived table cannot see an outer column
    unless it is LATERAL, which is not valid there. The ``hll_union`` UDF
    reads its parameters inside its own SELECT, which is valid because they
    are function parameters (SNOW-4193976). Same shape:

    ``SELECT (<math on SPARK_FP_INPUT>) FROM (SELECT arg0 AS SPARK_FP_INPUT)``.
    """
    bound_input = snowpark_fn.col(_BOUND_INPUT_NAME)
    body_sql = _render_sql(build(bound_input)._expression)
    alias_sql = _render_sql(bound_input._expression)
    return f"SELECT ({body_sql}) FROM (SELECT {_UDF_PARAMETER_NAME} AS {alias_sql})"


def call_cached_float_sql_udf(body: str, return_type: str, col: Column) -> Column:
    """Register ``body`` and return a call that names ``col`` once.

    Registration needs an active session. ``sql_udf_body`` does not, so unit
    tests can render the body and a ``sql_expr`` call without Snowflake.
    """
    from snowflake.snowpark_connect.utils.udf_cache import register_cached_sql_udf

    return register_cached_sql_udf(["FLOAT"], return_type, body)(col)


def supports_exact_fractional_rounding(scale: int) -> bool:
    return abs(scale) <= _MAX_EXACT_POW10_EXPONENT


def rounded_scaled_magnitude(
    col: Column, scale: int, half_even: bool
) -> tuple[Column, Column]:
    """Return ``(units, in_range)`` for ``|col|`` rounded to ``scale`` digits.

    ``units`` is the integer-valued double ``round(|col| * 10^scale)`` under
    Spark's rounding mode, valid where ``in_range`` is true. ``in_range`` is
    false for NULL, NaN, +-Infinity and magnitudes of ``2^52`` units or more.
    """
    magnitude = snowpark_fn.abs(col)
    pow10 = snowpark_fn.lit(float(10 ** abs(scale)))
    scaled = magnitude * pow10 if scale >= 0 else magnitude / pow10
    floor_units = snowpark_fn.floor(scaled)
    tie_point = floor_units + 0.5
    tie = tie_point / pow10 if scale >= 0 else tie_point * pow10
    if half_even:
        round_up = (magnitude > tie) | (
            (magnitude == tie) & (snowpark_fn.call_function("mod", floor_units, 2) == 1)
        )
    else:
        round_up = magnitude >= tie
    units = floor_units + snowpark_fn.iff(
        round_up, snowpark_fn.lit(1.0), snowpark_fn.lit(0.0)
    )
    in_range = scaled < snowpark_fn.lit(_MAX_SCALED_MAGNITUDE)
    return units, in_range


def _round_number(value: Column, scale: int, half_even: bool) -> Column:
    """ROUND of a NUMBER in Spark's mode (Snowflake's default is half away from zero)."""
    if half_even:
        return snowpark_fn.call_function(
            "ROUND", value, snowpark_fn.lit(scale), snowpark_fn.lit("HALF_TO_EVEN")
        )
    return snowpark_fn.call_function("ROUND", value, snowpark_fn.lit(scale))


def exact_decimal_literal(value: Decimal) -> Column:
    """NUMBER literal of exactly ``value``.

    ``lit(Decimal)`` is typed NUMBER(38, 18), which truncates 1e-19 to 0 and
    overflows at 1e20, and renders ``1E-19``, a FLOAT literal in Snowflake.
    """
    text = f"{value:f}"
    scale = max(0, -value.as_tuple().exponent)
    return snowpark_fn.lit(text, DecimalType(38, scale))


def _decfloat_literal(value: Decimal) -> Column:
    return snowpark_fn.lit(f"{value:E}", DecFloatType())


def _to_double(value: Column) -> Column:
    return snowpark_fn.cast(value, DoubleType())


def _power_of_two_exponent(scale: int) -> int:
    """Largest ``k`` with ``2^k <= 10^(scale - 15)``."""
    if scale >= 15:
        return (10 ** (scale - 15)).bit_length() - 1
    return -((10 ** (15 - scale) - 1).bit_length())


def _times_power_of_two(value: Column, exponent: int) -> Column:
    """``value * 2^exponent``, exact while it stays a normal double."""
    while exponent:
        step = max(-1000, min(1000, exponent))
        value = value * snowpark_fn.lit(2.0**step)
        exponent -= step
    return value


def _power_of_two_decfloat(exponent: int) -> Column:
    with localcontext() as context:
        context.prec = 60
        value = Decimal(2) ** exponent
    return snowpark_fn.lit(f"{value:.37E}", DecFloatType())


def _round_decimal(
    magnitude: Column,
    safe: Column,
    approx: Column,
    scale: int,
    half_even: bool,
    literal,
) -> tuple[Column, Column, Column]:
    """Spark's rounding of ``magnitude`` (finite, >= 0, under 10^16 units).

    Returns ``(K, K + 1 unit, R)``: if ``K`` or ``K + 1 unit`` converts to
    ``magnitude`` that is the result, else the decimal ``R``.

    Spark rounds ``D``, the shortest decimal that converts back to the double.
    ``safe`` is ``magnitude``, or 0 on rows another branch takes, and
    ``approx`` is ``safe`` as a NUMBER or DECFLOAT to well within half a
    unit; it only picks ``K = FLOOR(approx, scale)``, the tie ``H = K + 0.5
    unit`` and ``M+- = H +- 0.05 unit``. The rest compares ``magnitude`` with
    those decimals converted to double, which Snowflake rounds correctly:

    * ``K`` or ``K + 1 unit`` converts to the double: ``D`` has at most
      ``scale`` decimals, so rounding keeps the double;
    * ``magnitude`` above or below ``double(H)``: so is ``D`` against ``H``;
    * otherwise ``D`` has ``scale + 1`` decimals and is the nearest such to the
      double's exact value, so it is above ``H`` if the double is above
      ``M+``, below if below ``M-``, else ``H`` and the rounding mode decides.
      The double settles most of these; if it converts from ``M+`` or ``M-``
      as well (from 2.25e14 units up) the exact value decides, scaled by
      ``2^k`` into [0.1, 10) and read as NUMBER(38, 37) against ``M * 2^k``
      in 38-digit DECFLOAT.
    """
    unit = literal(Decimal(1).scaleb(-scale))
    twentieth = literal(Decimal(5).scaleb(-(scale + 2)))
    floor = snowpark_fn.call_function("FLOOR", approx, snowpark_fn.lit(scale))
    ceil = floor + unit
    tie = floor + literal(Decimal(5).scaleb(-(scale + 1)))
    above, below = tie + twentieth, tie - twentieth
    exponent = _power_of_two_exponent(scale)
    exact = snowpark_fn.cast(_times_power_of_two(safe, exponent), DecimalType(38, 37))
    power = _power_of_two_decfloat(exponent)

    def scale_to_decfloat(decimal_value: Column) -> Column:
        return snowpark_fn.cast(decimal_value, DecFloatType()) * power

    at_tie = _round_number(tie, scale, half_even) if half_even else ceil
    tie_double = _to_double(tie)
    rounded = (
        snowpark_fn.when(magnitude > tie_double, ceil)
        .when(magnitude < tie_double, floor)
        .when(magnitude > _to_double(above), ceil)
        .when(magnitude < _to_double(below), floor)
        .when(exact > scale_to_decfloat(above), ceil)
        .when(exact < scale_to_decfloat(below), floor)
        .otherwise(at_tie)
    )
    return floor, ceil, rounded


def _approx_decimal(
    safe: Column, scale: int
) -> tuple[Column, Callable[[Decimal], Column]]:
    """``safe`` (under 10^16 units) as a NUMBER or DECFLOAT, and its literal type."""
    if -_MAX_NUMBER_INTEGER_ROUNDING_SCALE <= scale <= _MAX_NUMBER_ROUNDING_SCALE:
        # NUMBER(38, scale + 6) holds it to 10^-6 units.
        return (
            snowpark_fn.cast(safe, DecimalType(38, max(0, scale + 6))),
            exact_decimal_literal,
        )
    # DECFLOAT keeps 18 significant digits, a tenth of a unit or better here.
    return snowpark_fn.cast(safe, DecFloatType()), _decfloat_literal


def _with_sign(value: Column, col: Column) -> Column:
    # A product names ``value`` once, where IFF(col < 0, -value, value) would
    # repeat its SQL (and its compile time) twice.
    return value * snowpark_fn.iff(col < 0, snowpark_fn.lit(-1), snowpark_fn.lit(1))


def _spark_fractional_to_decimal_body(
    col: Column, scale: int, precision: int = 38
) -> tuple[Column, Column]:
    """Spark's CAST of a FLOAT column to DECIMAL(``precision``, ``scale``), before the precision check.

    Spark rounds ``BigDecimal(Double.toString(x))`` HALF_UP, where CAST(FLOAT AS
    NUMBER) rounds the exact binary value (1.005 -> 1.00, Spark 1.01). Returns
    the exact decimal and whether it is known: below 2^52 units (where a double
    is closer than one unit to a single ``scale``-decimal value), or above when
    Double.toString has at most 15 significant digits. Other rows (NaN,
    Infinity, longer digit strings) need another rule.
    """
    magnitude = snowpark_fn.abs(col)
    scaled = magnitude * snowpark_fn.lit(10.0**scale)
    in_range = scaled < snowpark_fn.lit(_MAX_SCALED_MAGNITUDE)
    safe = snowpark_fn.iff(in_range, magnitude, snowpark_fn.lit(0.0))
    approx, literal = _approx_decimal(safe, scale)
    floor, ceil, rounded = _round_decimal(
        magnitude, safe, approx, scale, False, literal
    )
    value = (
        snowpark_fn.when(_to_double(floor) == magnitude, floor)
        .when(_to_double(ceil) == magnitude, ceil)
        .otherwise(rounded)
    )
    if supports_exact_fractional_rounding(scale):
        units, _ = rounded_scaled_magnitude(col, scale, half_even=False)
        low = _MAX_SCALED_MAGNITUDE if scale == 0 else _MAX_DOUBLE_TIE_SCALED_MAGNITUDE
        value = snowpark_fn.iff(
            scaled < snowpark_fn.lit(low),
            snowpark_fn.cast(units, DecimalType(38, 0))
            * literal(Decimal(1).scaleb(-scale)),
            value,
        )
    # Beyond 2^52 units Spark's digits reach below the double's precision.
    # When Double.toString has at most 15 significant digits, those digits are
    # the only 15-digit decimal that converts back to the double (15-digit
    # neighbours are over 4 ulps apart). The native CAST is within half a unit
    # of the double, so rounding it to 15 significant digits gives them, and
    # the round trip tells these rows from the rest (16-17 digits, NaN,
    # Infinity), which take the native cast. The rows stop where the rounding
    # would carry to 10^(38 - scale) and overflow NUMBER(38, scale). From one
    # digit past ``precision`` on every row overflows whichever path it takes;
    # the extra digit keeps e.g. 1e20 for DECIMAL(23, 3) here, where the
    # caller's FLOAT ROUND fit check would see 9.999999999999998e19.
    limit = min(38, precision + 1) - scale
    if 10.0**limit <= _MAX_SCALED_MAGNITUDE * 10.0**-scale:
        # No double of 2^52 units or more is below the limit.
        return _with_sign(value, col), in_range
    top = (
        float(10**limit)
        if limit < 38 - scale
        else float(f"9.999999999999995e{limit - 1}")
    )
    big = ~in_range & (magnitude < snowpark_fn.lit(top))
    big_safe = snowpark_fn.iff(big, magnitude, snowpark_fn.lit(1.0))
    native = snowpark_fn.cast(big_safe, DecimalType(38, scale))
    # ROUND(NUMBER, column) keeps the NUMBER type, so one ROUND serves every
    # decade and ``native`` is named once. Off ``big`` the decade is wrong, but
    # ``native`` is 1 there and the result is discarded.
    short = snowpark_fn.call_function(
        "ROUND", native, snowpark_fn.lit(14) - _decade(magnitude, 15 - scale, limit)
    )
    is_short = big & (_to_double(short) == magnitude)
    known = in_range | is_short
    if 10.0**limit > 2.0**52:
        # Java 17 prints whole doubles in [2^52, 2^63) with more digits.
        long_valued = (
            big
            & (magnitude >= snowpark_fn.lit(2.0**52))
            & (magnitude < snowpark_fn.lit(2.0**63))
        )
        digits = _long_valued_digits(
            magnitude, snowpark_fn.iff(long_valued, magnitude, snowpark_fn.lit(0.0))
        )
        short = snowpark_fn.iff(long_valued, digits, short)
        known = known | long_valued
    value = snowpark_fn.iff(in_range, value, short)
    return _with_sign(value, col), known


def fractional_decimal_value_udf_body(scale: int, precision: int = 38) -> str:
    """UDF body for the decimal value of ``spark_fractional_to_decimal``."""

    def decimal_value(bound_input: Column) -> Column:
        value, _known = _spark_fractional_to_decimal_body(bound_input, scale, precision)
        return value

    return sql_udf_body(decimal_value)


def fractional_decimal_known_udf_body(scale: int, precision: int = 38) -> str:
    """UDF body for the known-flag of ``spark_fractional_to_decimal``."""

    def decimal_known(bound_input: Column) -> Column:
        _value, known = _spark_fractional_to_decimal_body(bound_input, scale, precision)
        return known

    return sql_udf_body(decimal_known)


def spark_fractional_to_decimal(
    col: Column, scale: int, precision: int = 38
) -> tuple[Column, Column]:
    """Spark's CAST pieces of a FLOAT column, each a SQL UDF call on ``col``.

    Scale and precision are baked into distinct UDF bodies. The caller names
    ``col`` once per returned column (SNOW-4193976).
    """
    number_type = f"NUMBER(38, {scale})"
    return (
        call_cached_float_sql_udf(
            fractional_decimal_value_udf_body(scale, precision), number_type, col
        ),
        call_cached_float_sql_udf(
            fractional_decimal_known_udf_body(scale, precision), "BOOLEAN", col
        ),
    )


def _decade(value: Column, low: int, high: int) -> Column:
    """``FLOOR(LOG10(value))`` for a positive FLOAT ``value`` in ``[10^low, 10^high)``,
    and a decade in ``[low, high)`` for any other ``value``.

    Compared against the double bounds of each decade rather than computed
    with LOG, which is off by one next to powers of ten (FLOOR(LOG(10, x))
    gives 20 for 9.99999999999999e19) and, at 10^8 rows, costs more to run
    than all the comparisons together.
    """
    result = snowpark_fn.when(
        value < snowpark_fn.lit(float(f"1e{low + 1}")), snowpark_fn.lit(low)
    )
    for e in range(low + 1, high - 1):
        result = result.when(
            value < snowpark_fn.lit(float(f"1e{e + 1}")), snowpark_fn.lit(e)
        )
    return result.otherwise(snowpark_fn.lit(high - 1))


def _long_valued_digits(magnitude: Column, safe: Column) -> Column:
    """Double.toString of a double in ``[2^52, 2^63)``, as NUMBER(38, 0).

    For these (whole) values Java 17's Double.toString prints the exact integer
    instead of the shortest decimal, pre-rounded HALF_UP to tens in
    ``[2^58, 2^61)`` and to hundreds in ``[2^61, 2^63)`` (FloatingDecimal's
    "insignificant digits"), e.g. 2.77980788232166848E17.
    """
    x = snowpark_fn.cast(safe, DecimalType(38, 0))
    return (
        snowpark_fn.when(
            magnitude >= snowpark_fn.lit(float(2**61)),
            snowpark_fn.call_function("ROUND", x, snowpark_fn.lit(-2)),
        )
        .when(
            magnitude >= snowpark_fn.lit(float(2**58)),
            snowpark_fn.call_function("ROUND", x, snowpark_fn.lit(-1)),
        )
        .otherwise(x)
    )


def _round_long_valued(
    magnitude: Column, safe: Column, scale: int, half_even: bool
) -> Column:
    """Spark's rounding at ``scale < 0`` of a double in ``[2^52, 2^63)``."""
    printed = _long_valued_digits(magnitude, safe)
    return _to_double(_round_number(printed, scale, half_even))


def round_fractional_udf_body(scale: int, half_even: bool) -> str:
    """UDF body for one ``round`` or ``bround`` scale and mode.

    ``half_even`` is baked in, so HALF_UP and HALF_EVEN are different functions.
    """

    def round_bound_input(bound_input: Column) -> Column:
        return _spark_round_fractional_body(bound_input, scale, half_even)

    return sql_udf_body(round_bound_input)


def spark_round_fractional(col: Column, scale: int, half_even: bool) -> Column:
    """Spark ``round`` (HALF_UP) / ``bround`` (HALF_EVEN) of a FLOAT column.

    The caller is one SQL UDF call, so nested ``round(round(x))`` is
    ``udf(udf(x))`` and the input expression is named once (SNOW-4193976).
    """
    return call_cached_float_sql_udf(
        round_fractional_udf_body(scale, half_even), "FLOAT", col
    )


def _spark_round_fractional_body(col: Column, scale: int, half_even: bool) -> Column:
    """Body of ``spark_round_fractional``. ``col`` is the bound input."""
    magnitude = snowpark_fn.abs(col)
    zero = snowpark_fn.lit(0.0)
    if scale <= -_MAX_DOUBLE_POW10_EXPONENT - 1:
        # Every finite double is below 0.5 * 10^309.
        return snowpark_fn.iff(magnitude < snowpark_fn.lit(float("inf")), zero, col)
    if scale >= _MAX_DOUBLE_DECIMAL_PLACES:
        # Double.toString never has this many decimals.
        return col + zero
    if scale > _MAX_DOUBLE_POW10_EXPONENT:
        scaled = (
            magnitude * snowpark_fn.lit(10.0 ** (scale - 300)) * snowpark_fn.lit(1e300)
        )
    elif scale >= 0:
        scaled = magnitude * snowpark_fn.lit(10.0**scale)
    else:
        scaled = magnitude / snowpark_fn.lit(10.0**-scale)
    # At 10^16 units or more a double has no digit below the rounding position.
    unchanged = ~(scaled < snowpark_fn.lit(_UNCHANGED_SCALED_MAGNITUDE))

    def signed_magnitude(magnitude_value: Column) -> Column:
        # Adding 0.0 turns the -0.0 of a negative value that rounds to zero into
        # 0.0, as Spark's BigDecimal has no negative zero.
        return magnitude_value * snowpark_fn.sign(col) + zero

    result = snowpark_fn.when(unchanged, col)
    # From scale -20 down, every double below 2^63 rounds to 0 on either path.
    if -_MAX_LONG_VALUED_ROUNDING_SCALE <= scale < 0:
        long_valued = (magnitude >= snowpark_fn.lit(float(2**52))) & (
            magnitude < snowpark_fn.lit(float(2**63))
        )
        result = snowpark_fn.when(
            long_valued,
            signed_magnitude(
                _round_long_valued(
                    magnitude,
                    snowpark_fn.iff(long_valued, magnitude, zero),
                    scale,
                    half_even,
                )
            ),
        ).when(unchanged, col)
    if supports_exact_fractional_rounding(scale):
        units, _ = rounded_scaled_magnitude(col, scale, half_even)
        pow10 = snowpark_fn.lit(float(10 ** abs(scale)))
        low = _MAX_SCALED_MAGNITUDE if scale == 0 else _MAX_DOUBLE_TIE_SCALED_MAGNITUDE
        result = result.when(
            scaled < snowpark_fn.lit(low),
            signed_magnitude(units / pow10 if scale >= 0 else units * pow10),
        )
    # The casts see 0 where the branch is not taken, so they cannot overflow
    # whatever order Snowflake evaluates the CASE in.
    safe = snowpark_fn.iff(unchanged, zero, magnitude)
    approx, literal = _approx_decimal(safe, scale)
    floor, ceil, rounded = _round_decimal(
        magnitude, safe, approx, scale, half_even, literal
    )
    keeps = (_to_double(floor) == magnitude) | (_to_double(ceil) == magnitude)
    return result.when(keeps, col + zero).otherwise(
        signed_magnitude(_to_double(rounded))
    )
