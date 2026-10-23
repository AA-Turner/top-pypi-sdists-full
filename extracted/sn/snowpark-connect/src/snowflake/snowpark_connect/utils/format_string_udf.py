#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Python body for ``format_string`` / ``printf`` with Spark's Java Formatter text.

Used when ``snowpark.connect.formatString.sparkCompatible`` is true (I024).
Spark formats with ``java.util.Formatter`` (``Locale.US``); Python's ``%``
operator differs in many places. With the flag on:

* a null argument prints ``null`` (``NULL`` for upper-case conversions,
  ``false`` for ``%b``) with Java width and precision;
* negative ``%x``/``%X``/``%o`` print the two's complement of the argument's
  width as SCOS tracks its type (TINYINT 8, SMALLINT 16, INT 32, BIGINT 64);
  an argument whose integral type is unknown keeps the signed legacy text;
* a DOUBLE stays a double (``%s`` of 3.0 is ``3.0``, NaN and Infinity format)
  and a DECIMAL with a scale keeps its digits (``12345678.90``), although the
  argument array would hand them over as int, text and a lossy double;
* ``%f``/``%e``/``%g`` of a double round HALF_UP on the digits JDK 17's
  ``FloatingDecimal`` produces, which are not always the shortest form
  (``%e`` of ``Double.MIN_VALUE`` is ``4.900000e-324``); ``%g`` keeps trailing
  zeros, and NaN/Infinity print as Java does;
* ``%s`` of a double prints JDK 17 ``Double.toString`` text (``1.0E10``,
  ``4.9E-324``);
* the ``,`` and ``(`` flags, ``%#o``, ``%S``, ``%b``/``%B``, ``%c``/``%C``,
  ``%n``, booleans, ``%2$s`` indexes, the ``<`` flag in any position
  (``%<s``, ``%0<8d``) and extra arguments match Java;
* ``%a``, ``%h``/``%H`` and ``%t``/``%T`` raise instead of returning Python
  text.

Inputs where Spark raises but this UDF returns text (Spark checks the Java
class of each argument; the UDF sees only the variant value): ``%d``/``%x`` of
DECIMAL/DOUBLE/BOOLEAN, ``%f``/``%e``/``%g`` of INT or DECIMAL, ``%c`` of
STRING, illegal flag
combinations (``%-08d``, ``%+x``, ``%.2d``, ``%010s``, ``%#s``, ``%,e``) and a
missing argument (NULL instead of an error). A format Java rejects outright
(``%y``) is NULL. ``%s`` of TIMESTAMP, DATE, ARRAY, MAP and BINARY prints the
variant text, where Spark prints its internal value. ``%s`` of FLOAT prints the
double text of the widened value, and ``-0.0`` loses its sign on the way into
the UDF (``%s`` is ``0.0``, ``%.2f`` is ``0.00``).

:func:`make_spark_format_string` returns a closure, so cloudpickle ships it by
value and the UDF sandbox does not need this package.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

from snowflake.snowpark.types import (
    ByteType,
    DataType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    ShortType,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_INTEGRAL_BITS: tuple[tuple[type, int], ...] = (
    (ByteType, 8),
    (ShortType, 16),
    (IntegerType, 32),
    (LongType, 64),
)


def _single_type(typed_arg) -> DataType | None:
    try:
        types = typed_arg.types
    except Exception as exc:  # noqa: BLE001
        # TypedColumn.types runs the type resolver, which can raise
        # SnowparkClientException from a DESCRIBE, and others. An unknown type
        # only costs the argument its kind (signed %x/%o, no double or decimal
        # handling), so narrowing this would turn any other inference failure
        # into an error. The pivot first/last type lookup does the same.
        logger.debug("format_string argument type not inferred: %s", exc)
        return None
    return types[0] if types is not None and len(types) == 1 else None


def argument_kinds(typed_args: Iterable) -> str:
    """Comma-separated kind per argument: a bit width, ``d``, ``n`` or ``0``.

    ``8``/``16``/``32``/``64``: Java prints a negative Byte/Short/Integer/Long
    with ``%x``/``%o`` as the unsigned value of that width, so the width comes
    from the type SCOS tracks for the argument, not from the value. A column
    read back from a Snowflake table may be tracked as BIGINT and then prints
    16 hex digits.

    ``d`` (FLOAT/DOUBLE): the array hands an integral double to the UDF as an
    int and NaN/Infinity as text, so the UDF turns them back into floats.

    ``n`` (DECIMAL with a scale): the array would hand over a lossy double, so
    :func:`format_string_argument` sends the text and the UDF reads a Decimal.

    ``0``: anything else, including a type SCOS cannot resolve.
    """
    kinds = []
    for typed_arg in typed_args:
        typ = _single_type(typed_arg)
        kind = "0"
        for cls, cls_bits in _INTEGRAL_BITS:
            if isinstance(typ, cls):
                kind = str(cls_bits)
                break
        if isinstance(typ, (FloatType, DoubleType)):
            kind = "d"
        elif isinstance(typ, DecimalType) and typ.scale > 0:
            kind = "n"
        kinds.append(kind)
    return ",".join(kinds)


def format_string_argument(col, kind: str):
    """The array element for an argument of ``kind`` (see :func:`argument_kinds`)."""
    if kind == "n":
        import snowflake.snowpark.functions as snowpark_fn

        # TO_VARCHAR keeps the scale: 100.00, not 100.
        return snowpark_fn.to_varchar(col)
    return col


def make_spark_format_string() -> Callable[[str, list, str], str | None]:
    import math
    import re
    import struct
    from decimal import ROUND_HALF_UP, Context, Decimal

    # java.util.Formatter's specifier grammar: '<' is a flag, in any position.
    spec_re = re.compile(
        r"%(?:(?P<index>\d+)\$)?"
        r"(?P<flags>[-#+ 0,(<]*)(?P<width>\d+)?(?P<precision>\.\d+)?"
        r"(?P<conversion>[tT][a-zA-Z]|[a-zA-Z%])"
    )
    ctx = Context(prec=1000, rounding=ROUND_HALF_UP)
    one = Decimal(1)

    # Tables from JDK 17 jdk.internal.math.FloatingDecimal / FDBigInteger.
    insignificant_digits_for_pow2 = (
        (0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6)
        + (6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12)
        + (12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 16, 16)
        + (17, 17, 17, 18, 18, 18, 19)
    )
    n_5_bits = (0, 3, 5, 7, 10, 12, 14, 17, 19, 21, 24, 26, 28, 31, 33, 35, 38) + (
        (40, 42, 45, 47, 49, 52, 54, 56, 59, 61)
    )
    long_5_pow_len = 27
    exp_shift = 52
    fract_hob = 1 << exp_shift
    signif_mask = fract_hob - 1

    def _wrap(value: int, bits: int) -> int:
        value &= (1 << bits) - 1
        return value - (1 << bits) if value >> (bits - 1) else value

    def _double_bits(value: float) -> int:
        return struct.unpack(">q", struct.pack(">d", value))[0]

    def _estimate_dec_exp(fract_bits: int, bin_exp: int) -> int:
        d2 = struct.unpack(
            ">d", struct.pack(">q", (1023 << exp_shift) | (fract_bits & signif_mask))
        )[0]
        d = (d2 - 1.5) * 0.289529654 + 0.176091259 + bin_exp * 0.301029995663981
        d_bits = _double_bits(d)
        exponent = ((d_bits >> exp_shift) & 0x7FF) - 1023
        negative = d_bits < 0
        if 0 <= exponent < 52:
            mask = signif_mask >> exponent
            r = ((d_bits & signif_mask) | fract_hob) >> (exp_shift - exponent)
            if not negative:
                return r
            return -r if (mask & d_bits) == 0 else -r - 1
        if exponent < 0:
            if (d_bits & 0x7FFF_FFFF_FFFF_FFFF) == 0:
                return 0
            return -1 if negative else 0
        return int(d)

    def _long_digits(lvalue: int, insignificant: int) -> tuple[list[int], int]:
        # BinaryToASCIIBuffer.developLongDigits: drop insignificant low digits
        # with rounding, then strip trailing zeros into the exponent.
        dec_exp = 0
        if insignificant:
            pow10 = 10**insignificant
            residue = lvalue % pow10
            lvalue //= pow10
            dec_exp += insignificant
            if residue >= pow10 >> 1:
                lvalue += 1
        text = str(lvalue)
        return [int(c) for c in text.rstrip("0")], dec_exp + len(text)

    def _java_digits(value: float, compatible: bool) -> tuple[list[int], int]:
        """FloatingDecimal digits of a positive finite double: 0.d1d2... * 10^exp.

        A port of JDK 17 ``BinaryToASCIIBuffer.dtoa``, the source of both
        ``Double.toString`` (``compatible``) and Formatter's %e/%f/%g digits.
        Its stopping rule is not always the shortest round trip (4.9E-324,
        6.4975114854988728E16), so Python's ``repr`` cannot stand in for it.
        The names b/s/m/q and b2/b5/s2/s5/m2/m5 are dtoa's: B / S is the value
        scaled into [1, 10), M is half an ULP scaled the same way, and q is the
        next digit.
        """
        bits = _double_bits(value)
        fract_bits = bits & signif_mask
        bin_exp = (bits >> exp_shift) & 0x7FF
        if bin_exp == 0:
            if fract_bits == 0:
                return [0], 0
            n_significant_bits = fract_bits.bit_length()
            shift = (64 - n_significant_bits) - (63 - exp_shift)
            fract_bits <<= shift
            bin_exp = 1 - shift
        else:
            fract_bits |= fract_hob
            n_significant_bits = exp_shift + 1
        bin_exp -= 1023
        tail_zeros = (fract_bits & -fract_bits).bit_length() - 1
        n_fract_bits = exp_shift + 1 - tail_zeros
        n_tiny_bits = max(0, n_fract_bits - bin_exp - 1)
        if (
            -21 <= bin_exp <= 62
            and n_tiny_bits < long_5_pow_len
            and n_fract_bits + n_5_bits[n_tiny_bits] < 64
            and n_tiny_bits == 0
        ):
            p2 = bin_exp - n_significant_bits - 1
            insignificant = (
                insignificant_digits_for_pow2[p2]
                if bin_exp > n_significant_bits
                and 1 < p2 < len(insignificant_digits_for_pow2)
                else 0
            )
            if bin_exp >= exp_shift:
                fract_bits <<= bin_exp - exp_shift
            else:
                fract_bits >>= exp_shift - bin_exp
            return _long_digits(fract_bits, insignificant)

        dec_exp = _estimate_dec_exp(fract_bits, bin_exp)
        b5 = max(0, -dec_exp)
        b2 = b5 + n_tiny_bits + bin_exp
        s5 = max(0, dec_exp)
        s2 = s5 + n_tiny_bits
        m5 = b5
        m2 = b2 - n_significant_bits
        fract_bits >>= tail_zeros
        b2 -= n_fract_bits - 1
        common = min(b2, s2)
        b2 -= common
        s2 -= common
        m2 -= common
        if n_fract_bits == 1:
            m2 -= 1
        if m2 < 0:
            b2 -= m2
            s2 -= m2
            m2 = 0
        b_bits = n_fract_bits + b2 + (n_5_bits[b5] if b5 < len(n_5_bits) else b5 * 3)
        ten_s_bits = (
            s2 + 1 + (n_5_bits[s5 + 1] if s5 + 1 < len(n_5_bits) else (s5 + 1) * 3)
        )
        digits = []
        if b_bits < 64 and ten_s_bits < 64:
            # Java does this in int or long arithmetic. Only m (and b + m) can
            # overflow; wrap them only when they leave the signed range.
            width = 32 if b_bits < 32 and ten_s_bits < 32 else 64
            top = (1 << (width - 1)) - 1
            b = (fract_bits * 5**b5) << b2
            s = (5**s5) << s2
            m = (5**m5) << m2
            tens = s * 10
            q = b // s
            b = 10 * (b % s)
            m *= 10
            if not -top <= m <= top:
                m = _wrap(m, width)
            total = b + m
            low = b < m
            high = (total if total <= top else _wrap(total, width)) > tens
            if q == 0 and not high:
                dec_exp -= 1
            else:
                digits.append(q)
            if not compatible or dec_exp < -3 or dec_exp >= 8:
                high = low = False
            while not low and not high:
                q = b // s
                b = 10 * (b % s)
                m *= 10
                if not -top <= m <= top:
                    m = _wrap(m, width)
                if m > 0:
                    total = b + m
                    low = b < m
                    high = (total if total <= top else _wrap(total, width)) > tens
                else:
                    low = high = True
                digits.append(q)
            low_digit_difference = _wrap((b << 1) - tens, width)
        else:
            s = (5**s5) << s2
            b = (fract_bits * 5**b5) << b2
            m = (5 ** (m5 + 1)) << (m2 + 1)
            ten_s = s * 10
            q, b = divmod(b, s)
            b *= 10
            low = b < m
            high = b + m >= ten_s
            if q == 0 and not high:
                dec_exp -= 1
            else:
                digits.append(q)
            if not compatible or dec_exp < -3 or dec_exp >= 8:
                high = low = False
            while not low and not high:
                q, b = divmod(b, s)
                b *= 10
                m *= 10
                low = b < m
                high = b + m >= ten_s
                digits.append(q)
            low_digit_difference = (b << 1) - ten_s if high and low else 0
        dec_exp += 1
        if high and (
            not low
            or low_digit_difference > 0
            or (low_digit_difference == 0 and digits[-1] % 2)
        ):
            # roundup(): a carry out of the first digit keeps the digit count.
            i = len(digits) - 1
            while digits[i] == 9 and i > 0:
                digits[i] = 0
                i -= 1
            if digits[i] == 9:
                digits[0] = 1
                dec_exp += 1
            else:
                digits[i] += 1
        return digits, dec_exp

    def _apply_precision(digits: list[int], dec_exp: int, prec: int) -> int:
        # FormattedFloatingDecimal.applyPrecision: HALF_UP on the digits.
        if prec >= len(digits) or prec < 0:
            return dec_exp
        if prec == 0:
            carry = digits[0] >= 5
            digits[:] = [1 if carry else 0] + [0] * (len(digits) - 1)
            return dec_exp + 1 if carry else dec_exp
        if digits[prec] >= 5:
            i = prec - 1
            while digits[i] == 9 and i > 0:
                i -= 1
            if digits[i] == 9:
                digits[:] = [1] + [0] * (len(digits) - 1)
                return dec_exp + 1
            digits[i] += 1
            digits[i + 1 :] = [0] * (len(digits) - i - 1)
        else:
            digits[prec:] = [0] * (len(digits) - prec)
        return dec_exp

    def _fill_decimal(digits: list[int], exp: int, precision: int) -> str:
        # FormattedFloatingDecimal.fillDecimal.
        text = "".join(map(str, digits))
        if exp > 0:
            if len(text) < exp:
                return text + "0" * (exp - len(text))
            tail = text[exp : exp + max(0, precision)]
            return text[:exp] + ("." + tail if tail else "")
        zeros = max(0, min(-exp, precision))
        tail = text[: max(0, min(len(text), precision + exp))]
        if zeros or tail:
            return "0." + "0" * zeros + tail
        return "0"

    def _fill_scientific(
        digits: list[int], exp: int, precision: int
    ) -> tuple[str, str]:
        # FormattedFloatingDecimal.fillScientific: (mantissa, signed exponent).
        text = "".join(map(str, digits))
        tail = text[1 : 1 + max(0, min(len(text) - 1, precision))]
        e = exp - 1
        return text[0] + ("." + tail if tail else ""), (
            f"{'-' if e < 0 else '+'}{abs(e):02d}"
        )

    def _add_zeros(mantissa: str, prec: int) -> str:
        # Formatter.FormatSpecifier.addZeros.
        head, _, tail = mantissa.partition(".")
        if len(tail) >= prec:
            return mantissa
        return head + "." + tail + "0" * (prec - len(tail))

    def _java_double(value: float) -> str:
        """``Double.toString`` text (JDK 17 BinaryToASCIIBuffer.getChars)."""
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        sign = "-" if math.copysign(1.0, value) < 0 else ""
        if value == 0:
            return sign + "0.0"
        digits, exp = _java_digits(abs(value), True)
        text = "".join(map(str, digits))
        if 0 < exp < 8:
            if len(text) <= exp:
                return sign + text + "0" * (exp - len(text)) + ".0"
            return sign + text[:exp] + "." + text[exp:]
        if -3 < exp <= 0:
            return sign + "0." + "0" * -exp + text
        return sign + text[0] + "." + (text[1:] or "0") + "E" + str(exp - 1)

    def _java_floating(
        mag: float, kind: str, precision: int | None, alternate: bool
    ) -> str:
        """Formatter's %e/%f/%g text of a non-negative finite double.

        Formatter.FormatSpecifier.print(StringBuilder, double, ...) in JDK 17.
        """
        exponent = ""
        if kind == "g":
            prec = 6 if precision is None else precision or 1
            if mag == 0:
                body = "0"
                prec -= 1
            else:
                digits, exp = _java_digits(mag, False)
                exp = _apply_precision(digits, exp, prec)
                if exp - 1 < -4 or exp - 1 >= prec:
                    body, exponent = _fill_scientific(digits, exp, prec - 1)
                    prec -= 1
                else:
                    body = _fill_decimal(digits, exp, prec - exp)
                    prec -= exp
        else:
            prec = 6 if precision is None else precision
            digits, exp = ([0], 0) if mag == 0 else _java_digits(mag, False)
            if kind == "e":
                exp = _apply_precision(digits, exp, prec + 1)
                body, exponent = _fill_scientific(digits, exp, prec)
                if mag == 0:
                    exponent = "+00"
            else:
                exp = _apply_precision(digits, exp, exp + prec)
                body = _fill_decimal(digits, exp, prec)
        body = _add_zeros(body, prec)
        if alternate and prec == 0:
            body += "."
        return body + ("e" + exponent if exponent else "")

    def _justify(text: str, flags: str, width: str | None) -> str:
        if width is None or len(text) >= int(width):
            return text
        pad = " " * (int(width) - len(text))
        return text + pad if "-" in flags else pad + text

    def _group(text: str) -> str:
        head, dot, tail = text.partition(".")
        parts = []
        while len(head) > 3:
            parts.insert(0, head[-3:])
            head = head[:-3]
        parts.insert(0, head)
        return ",".join(parts) + dot + tail

    def _signed(magnitude: str, negative: bool, flags: str, width: str | None) -> str:
        if negative:
            prefix, suffix = ("(", ")") if "(" in flags else ("-", "")
        else:
            prefix = "+" if "+" in flags else " " if " " in flags else ""
            suffix = ""
        if "0" in flags and width is not None:
            magnitude = magnitude.rjust(int(width) - len(prefix) - len(suffix), "0")
        return _justify(prefix + magnitude + suffix, flags, width)

    def _fixed(mag: Decimal, decimals: int, alternate: bool) -> str:
        text = format(mag.quantize(one.scaleb(-decimals), context=ctx), "f")
        return text + "." if alternate and decimals == 0 else text

    def _scientific(mag: Decimal, decimals: int, alternate: bool) -> str:
        exp = 0 if mag == 0 else mag.adjusted()
        mant = mag.scaleb(-exp).quantize(one.scaleb(-decimals), context=ctx)
        if mant >= 10:
            exp += 1
            mant = mag.scaleb(-exp).quantize(one.scaleb(-decimals), context=ctx)
        text = format(mant, "f") + ("." if alternate and decimals == 0 else "")
        return f"{text}e{'-' if exp < 0 else '+'}{abs(exp):02d}"

    def _decimal_floating(
        mag: Decimal, kind: str, precision: int | None, alternate: bool
    ) -> str:
        # A non-double argument (int, Decimal) has exact digits, as BigDecimal.
        prec = 6 if precision is None else precision
        if kind == "g":
            prec = prec or 1
            if mag == 0:
                return _fixed(mag, prec - 1, False)
            rounded = mag.quantize(one.scaleb(mag.adjusted() - prec + 1), context=ctx)
            if -4 <= rounded.adjusted() < prec:
                return _fixed(rounded, prec - 1 - rounded.adjusted(), False)
            return _scientific(rounded, prec - 1, False)
        if kind == "e":
            return _scientific(mag, prec, alternate)
        return _fixed(mag, prec, alternate)

    def _floating(
        arg: object,
        conversion: str,
        flags: str,
        width: str | None,
        precision: str | None,
    ) -> str:
        if isinstance(arg, str):
            raise TypeError(arg)
        if isinstance(arg, float) and not math.isfinite(arg):
            if math.isnan(arg):
                text = "NaN"
            else:
                text = _signed("Infinity", arg < 0, flags.replace("0", ""), None)
            text = _justify(text, flags, width)
            return text.upper() if conversion.isupper() else text
        prec = None if precision is None else int(precision[1:])
        kind = conversion.lower()
        alternate = "#" in flags
        if isinstance(arg, float):
            negative = math.copysign(1.0, arg) < 0
            body = _java_floating(abs(arg), kind, prec, alternate)
        else:
            dec = Decimal(arg)
            negative = dec.is_signed()
            body = _decimal_floating(abs(dec), kind, prec, alternate)
        if "," in flags and "e" not in body:
            body = _group(body)
        text = _signed(body, negative, flags, width)
        return text.upper() if conversion.isupper() else text

    def _format_one(
        arg: object,
        conversion: str,
        flags: str,
        width: str | None,
        precision: str | None,
        bits: int,
    ) -> str:
        if arg is None or conversion in "sSbB":
            if conversion in "bB":
                truth = arg if isinstance(arg, bool) else arg is not None
                text = "true" if truth else "false"
            elif arg is None:
                text = "null"
            elif isinstance(arg, bool):
                text = "true" if arg else "false"
            elif isinstance(arg, float):
                text = _java_double(arg)
            else:
                text = str(arg)
            if precision is not None:
                text = text[: int(precision[1:])]
            text = _justify(text, flags, width)
            return text.upper() if conversion.isupper() else text
        if conversion in "cC":
            text = _justify(chr(arg) if isinstance(arg, int) else arg, flags, width)
            return text.upper() if conversion == "C" else text
        if conversion == "d":
            if isinstance(arg, str):
                raise TypeError(arg)
            body = str(abs(int(arg)))
            if "," in flags:
                body = _group(body)
            return _signed(body, int(arg) < 0, flags, width)
        if conversion in "eEfgG":
            return _floating(arg, conversion, flags, width, precision)
        if conversion in "xXo" and isinstance(arg, int) and not isinstance(arg, bool):
            if arg < 0 and bits:
                arg &= (1 << bits) - 1
            if conversion == "o" and "#" in flags and arg >= 0:
                # Python writes 0o377; Java writes 0377 and zero-pads
                # between the prefix and the digits.
                digits = format(arg, "o")
                if "0" in flags and width is not None:
                    return "0" + digits.rjust(int(width) - 1, "0")
                return _justify("0" + digits, flags, width)
        return f"%{flags}{width or ''}{precision or ''}{conversion}" % (arg,)

    # No annotations: Snowpark reads them at registration and rejects
    # ``str | None``; the UDF types come from cached_udf's arguments.
    def _argument(value: object, kind: str) -> object:
        if value is None or getattr(value, "is_sql_null", False):
            return None
        if (
            kind == "d"
            and isinstance(value, (int, str))
            and not isinstance(value, bool)
        ):
            # 3.0 arrives as 3 and NaN/Infinity/-Infinity as text. -0.0 also
            # arrives as 0, so its sign is lost.
            return float(value)
        if kind == "n" and isinstance(value, str):
            return Decimal(value)
        return value

    def _format_string_spark_compat(fmt, args, arg_kinds):
        if fmt is None or args is None:
            return None
        kinds = arg_kinds.split(",") if arg_kinds else []
        values = [
            _argument(arg, kinds[i] if i < len(kinds) else "0")
            for i, arg in enumerate(args)
        ]
        bits = [int(width) if width.isdigit() else 0 for width in kinds]

        pieces = []
        pos = 0
        next_ordinary = 0
        last_index = -1
        try:
            for match in spec_re.finditer(fmt):
                gap = fmt[pos : match.start()]
                if "%" in gap:
                    raise ValueError(gap)
                pieces.append(gap)
                pos = match.end()

                conversion = match.group("conversion")
                # Java reads '<' anywhere in the flags (%<s, %0<8d, %-<8d) and
                # then ignores an explicit index.
                previous = "<" in match.group("flags")
                flags = match.group("flags").replace("<", "")
                width = match.group("width")
                if conversion in "aAhH" or conversion[0] in "tT":
                    raise NotImplementedError(
                        f"format_string conversion '%{conversion}' is not supported "
                        "with snowpark.connect.formatString.sparkCompatible=true"
                    )
                if conversion == "%":
                    pieces.append(_justify("%", flags, width))
                    continue
                if conversion == "n":
                    pieces.append("\n")
                    continue

                if previous:
                    index = last_index
                elif match.group("index") is not None:
                    index = int(match.group("index")) - 1
                else:
                    index = next_ordinary
                    next_ordinary += 1
                if index < 0 or index >= len(values):
                    # Java raises MissingFormatArgumentException.
                    return None
                last_index = index
                pieces.append(
                    _format_one(
                        values[index],
                        conversion,
                        flags,
                        width,
                        match.group("precision"),
                        bits[index] if index < len(bits) else 0,
                    )
                )
            tail = fmt[pos:]
            if "%" in tail:
                raise ValueError(tail)
            pieces.append(tail)
        except ValueError:
            # A specifier this parser does not model: keep the legacy Python
            # text so the flag never turns a working format into an error.
            try:
                return fmt % tuple("null" if v is None else v for v in values)
            except (TypeError, ValueError):
                # Java rejects the format too (UnknownFormatConversionException).
                return None
        except TypeError:
            return None
        return "".join(pieces)

    return _format_string_spark_compat
