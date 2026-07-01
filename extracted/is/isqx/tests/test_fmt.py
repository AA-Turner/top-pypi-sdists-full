from fractions import Fraction

from isqx import CENTI, HOUR, G, M, S, simplify
from isqx._fmt import BasicFormatter, fmt
from isqx.usc import BTU_IT, FAHRENHEIT, FT, IN, R

K_VALUE = BTU_IT * IN / (HOUR * FT**2 * R)
CM = CENTI * M
DYN = (G * CM * S**-2).alias("dyn")
STATC = (DYN ** Fraction(1, 2) * M).alias("statc")


def test_fmt_basic_tagged() -> None:
    from isqx import M_PERS
    from isqx.aerospace import TRUE_AIRSPEED

    M_PERS_TAS = TRUE_AIRSPEED(M_PERS)
    assert (
        fmt(M_PERS_TAS, formatter=BasicFormatter())
        == "(meter · second⁻¹)['airspeed', 'true']"
    )


def test_fmt_basic_translated() -> None:
    assert (
        fmt(FAHRENHEIT, formatter=BasicFormatter(verbose=True))
        == """fahrenheit
- fahrenheit = rankine - 459.67
  - rankine = 5/9 · kelvin"""
    )


def test_fmt_basic_log() -> None:
    from isqx import DB

    assert (
        fmt(DB, formatter=BasicFormatter(verbose=True))
        == """decibel
- bel = log₁₀(ratio)"""
    )


def test_fmt_basic_log_level() -> None:
    from isqx import DBU

    assert (
        fmt(DBU, formatter=BasicFormatter(verbose=True))
        == """dBu
- dBu = 20 · log₁₀(ratio[`volt` to `0.6¹⸍² · volt`])
  - volt = watt · ampere⁻¹
    - watt = joule · second⁻¹
      - joule = newton · meter
        - newton = kilogram · meter · second⁻²"""
    )


def test_fmt_basic_k_value() -> None:
    assert (
        fmt(K_VALUE, formatter=BasicFormatter(verbose=True))
        == """btu_it · inch · (hour · foot² · rankine)⁻¹
- btu_it = 1055.05585262 · joule
  - joule = newton · meter
    - newton = kilogram · meter · second⁻²
- inch = 1/12 · foot
  - foot = 0.3048 · meter
- hour = 60 · minute
  - minute = 60 · second
- rankine = 5/9 · kelvin"""
    )
    assert (
        fmt(simplify(K_VALUE), formatter=BasicFormatter(verbose=True))
        == "1055.05585262 · 1/12 · 0.3048 · 60⁻¹ · 60⁻¹ · 0.3048⁻² · (5/9)⁻¹ · (meter · kilogram · second⁻³ · kelvin⁻¹)"
    )


def test_fmt_basic_statc() -> None:
    assert (
        fmt(STATC, formatter=BasicFormatter(verbose=True))
        == """statc
- statc = dyn¹⸍² · meter
  - dyn = gram · centimeter · second⁻²
    - gram = 1/1000 · kilogram"""
    )
    assert (
        fmt(simplify(STATC), formatter=BasicFormatter(verbose=True))
        == "(1/1000)¹⸍² · (1/100)¹⸍² · (meter³⸍² · kilogram¹⸍² · second⁻¹)"
    )
