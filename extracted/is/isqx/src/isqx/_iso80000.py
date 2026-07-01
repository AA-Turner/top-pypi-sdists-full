"""Units and quantities as defined by the International System of Quantities
(ISQ), as specified in the ISO/IEC 80000 standard.

Domain-specific units and quantities should be defined elsewhere, in their own
modules (e.g. [aerospace][isqx.aerospace]) for performance reasons.

See: [isqx._citations.SI][], [isqx._citations.IUPAP1][],
[isqx._citations.SP811][]
[isqx._citations.CODATA2022][], [isqx._citations.ISO_80000_2][],
[isqx._citations.ISO_80000_3][], [isqx._citations.ISO_80000_4][],
[isqx._citations.ISO_80000_5][],
[isqx._citations.IEC_80000_6][], [isqx._citations.IEV][],
[isqx._citations.ISO_80000_7][], [isqx._citations.ISO_80000_8][],
[isqx._citations.ISO_80000_9][], [isqx._citations.ISO_80000_10][],
[isqx._citations.ISO_80000_11][], [isqx._citations.ISO_80000_12][],
[isqx._citations.ISO_80000_13][], [isqx._citations.MP_UNITS][].

Quantity kinds in this module are largely derived from Wikidata.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import Annotated

from ._core import (
    _RATIO,
    CARTESIAN,
    COMPLEX,
    DELTA,
    DIFFERENTIAL,
    INEXACT_DIFFERENTIAL,
    TENSOR_SECOND_ORDER,
    VECTOR,
    BaseDimension,
    BaseUnit,
    Dimensionless,
    Exponent,
    LazyProduct,
    Log,
    OriginAt,
    Prefix,
    QtyKind,
    Quantity,
    StdUncertainty,
    Translated,
    ratio,
)
from ._core import PI as _PI
from ._core import E as _E

#
# base units [SI page 130 & section 2.3.3] [IUPAP1 page 20 & table 4]
#

DIM_TIME = BaseDimension("T")
S = BaseUnit(DIM_TIME, "second")
"""Second, a unit of [time][isqx.TIME]."""
DIM_LENGTH = BaseDimension("L")
M = BaseUnit(DIM_LENGTH, "meter")
"""Meter, a unit of [length][isqx.LENGTH]."""
DIM_MASS = BaseDimension("M")
KG = BaseUnit(DIM_MASS, "kilogram")
"""Kilogram, a unit of [mass][isqx.MASS]."""
G = (Fraction(1, 1000) * KG).alias("gram", allow_prefix=True)
"""Gram, a unit of [mass][isqx.MASS]."""
DIM_CURRENT = BaseDimension("I")
A = BaseUnit(DIM_CURRENT, "ampere")
"""Ampere, a unit of electric [current][isqx.CURRENT]."""
DIM_TEMPERATURE = BaseDimension("Θ")
K = BaseUnit(DIM_TEMPERATURE, "kelvin")
"""Kelvin, a unit of thermodynamic [temperature][isqx.TEMPERATURE]."""
DIM_AMOUNT = BaseDimension("N")
MOL = BaseUnit(DIM_AMOUNT, "mole")
"""Mole, a unit of [amount of substance][isqx.AMOUNT_OF_SUBSTANCE]."""
DIM_LUMINOUS_INTENSITY = BaseDimension("J")
CD = BaseUnit(DIM_LUMINOUS_INTENSITY, "candela")
"""Candela, a unit of [luminous intensity][isqx.LUMINOUS_INTENSITY]."""

#
# derived units [SI, page 137, section 2.3.4] [IUPAP1, page 22, table 5]
# important and widely used, but which do not properly fall within the SI.
#

RAD = Dimensionless("radian")
"""Radian, a unit of plane [angle][isqx.ANGLE]. Not to be confused with m m⁻¹."""
SR = Dimensionless("steradian")
"""Steradian, a unit of [solid angle][isqx.SOLID_ANGLE].
Not to be confused with m² m⁻²."""
HZ = (S**-1)["frequency"].alias("hertz", allow_prefix=True)
"""Unit of [frequency][isqx.FREQUENCY].
Shall only be used for periodic phenomena."""
M_PERS = M * S**-1
M_PERS2 = M * S**-2
N = (KG * M_PERS2).alias("newton", allow_prefix=True)
"""Newton, a unit of [force][isqx.FORCE]."""
PA = (N * M**-2).alias("pascal", allow_prefix=True)
"""Pascal, a unit of [pressure][isqx.PRESSURE] and [stress][isqx.STRESS]."""
J = (N * M).alias("joule", allow_prefix=True)
"""Joule, a unit of [energy][isqx.ENERGY], [work][isqx.WORK]
 and amount of [heat][isqx.HEAT]."""
W = (J * S**-1).alias("watt", allow_prefix=True)
"""Watt, a unit of [power][isqx.POWER] and [radiant flux][isqx.RADIANT_FLUX]."""
C = (A * S).alias("coulomb", allow_prefix=True)
"""Coulomb, a unit of electric [charge][isqx.ELECTRIC_CHARGE]."""
V = (W * A**-1).alias("volt", allow_prefix=True)
"""Volt, a unit of electric [potential difference][isqx.ELECTRIC_POTENTIAL_DIFFERENCE]
and [voltage][isqx.VOLTAGE], also known as `electric tension` or `tension`."""
F = (C * V**-1).alias("farad", allow_prefix=True)
"""Farad, a unit of [capacitance][isqx.CAPACITANCE]."""
OHM = (V * A**-1).alias("ohm", allow_prefix=True)
"""Ohm, a unit of electric [resistance][isqx.RESISTANCE]."""
SIEMENS = (A * V**-1).alias("siemens", allow_prefix=True)
"""Siemens, a unit of electric [conductance][isqx.CONDUCTANCE]."""
WB = (V * S).alias("weber", allow_prefix=True)
"""Weber, a unit of [magnetic flux][isqx.MAGNETIC_FLUX]."""
T = (WB * M**-2).alias("tesla", allow_prefix=True)
"""Tesla, a unit of [magnetic flux density][isqx.MAGNETIC_FLUX_DENSITY]."""
H = (WB * A**-1).alias("henry", allow_prefix=True)
"""Henry, a unit of [inductance][isqx.INDUCTANCE]."""
CELSIUS = Translated(K, Decimal("-273.15"), "celsius")
"""Celsius, a unit of thermodynamic [temperature][isqx.TEMPERATURE].
An absolute, translated scale.
Cannot be composed with other units."""
# NOTE: The symbol `sr` for must be included to distinguish luminous flux (lumen)
# from luminous intensity (candela)
LM = (CD * SR).alias("lumen", allow_prefix=True)
"""Lumen, a unit of [luminous flux][isqx.LUMINOUS_FLUX]."""
LX = (LM * M**-2).alias("lux", allow_prefix=True)
"""Lux, a unit of [illuminance][isqx.ILLUMINANCE]."""
BQ = (S**-1)["activity"].alias("becquerel", allow_prefix=True)
"""Unit of [activity][isqx.ACTIVITY] referred to a radionuclide.
Shall only be used for stochastic processes in activity referred to a radionuclide.
Not to be confused with "radioactivity"."""
GY = (J * KG**-1)["absorbed_dose"].alias("gray", allow_prefix=True)
"""Gray, a unit of [absorbed dose][isqx.ABSORBED_DOSE] and [kerma][isqx.KERMA]."""
SV = (J * KG**-1)["dose_equivalent"].alias("sievert", allow_prefix=True)
"""Sievert, a unit of [dose equivalent][isqx.DOSE_EQUIVALENT]."""
KAT = (MOL * S**-1).alias("katal", allow_prefix=True)
"""Katal, a unit of catalytic activity."""

#
# si prefixes [SI page 143] [IUPAP1 page 4 & table 1]
#

YOTTA = Prefix(10**24, "yotta")
ZETTA = Prefix(10**21, "zetta")
EXA = Prefix(10**18, "exa")
PETA = Prefix(10**15, "peta")
TERA = Prefix(10**12, "tera")
GIGA = Prefix(10**9, "giga")
MEGA = Prefix(10**6, "mega")
KILO = Prefix(10**3, "kilo")
HECTO = Prefix(10**2, "hecto")
DECA = Prefix(10**1, "deca")
DECI = Prefix(Fraction(1, 10**1), "deci")
CENTI = Prefix(Fraction(1, 10**2), "centi")
MILLI = Prefix(Fraction(1, 10**3), "milli")
MICRO = Prefix(Fraction(1, 10**6), "micro")
NANO = Prefix(Fraction(1, 10**9), "nano")
PICO = Prefix(Fraction(1, 10**12), "pico")
FEMTO = Prefix(Fraction(1, 10**15), "femto")
ATTO = Prefix(Fraction(1, 10**18), "atto")
ZEPTO = Prefix(Fraction(1, 10**21), "zepto")
YOCTO = Prefix(Fraction(1, 10**24), "yocto")
# see below (iso80000-13) for information theory prefixes

#
# constants from [CODATA2022] and other sources
# always prefer exact values or derivations from other constants over
# floating-point approximations.
#


CONST_SPEED_OF_LIGHT_VACUUM: Annotated[int, M_PERS] = 299_792_458
"""Speed of electromagnetic waves in vacuum, defined by the 17th CGPM (1983)."""
CONST_PLANCK: Annotated[Decimal, J * S] = Decimal("6.62607015e-34")
"""Planck constant, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_REDUCED_PLANCK: Annotated[LazyProduct, J * S] = LazyProduct(
    (CONST_PLANCK, (2, -1), (_PI, -1))
)
CONST_ELEMENTARY_CHARGE: Annotated[Decimal, C] = Decimal("1.602176634e-19")
"""Elementary charge, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_PERMEABILITY_VACUUM: Annotated[Decimal, H * M**-1, StdUncertainty(20)] = (
    Decimal("1.25663706127e-6")
)
"""Permeability of free space, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_PERMITTIVITY_VACUUM: Annotated[LazyProduct, F * M**-1] = LazyProduct(
    ((CONST_PERMEABILITY_VACUUM, -1), (CONST_SPEED_OF_LIGHT_VACUUM, -2))
)
"""Permittivity of free space, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_BOLTZMANN: Annotated[Decimal, J * K**-1] = Decimal("1.380649e-23")
"""Boltzmann constant, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_AVOGADRO: Annotated[Decimal, MOL**-1] = Decimal("6.02214076e23")
"""Avogadro constant, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_STEFAN_BOLTZMANN: Annotated[LazyProduct, W * M**-2 * K**-4] = LazyProduct(
    (
        2,
        (_PI, 5),
        (CONST_BOLTZMANN, 4),
        (15, -1),
        (CONST_SPEED_OF_LIGHT_VACUUM, -2),
        (CONST_PLANCK, -3),
    )
)
"""Stefan-Boltzmann constant, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_FIRST_RADIATION: Annotated[LazyProduct, W * M**-2] = LazyProduct(
    (2, _PI, CONST_PLANCK, (CONST_SPEED_OF_LIGHT_VACUUM, 2))
)
"""First radiation constant, ([CODATA 2022][isqx._citations.CODATA2022])."""
CONST_SECOND_RADIATION: Annotated[LazyProduct, M * K] = LazyProduct(
    (CONST_PLANCK, CONST_SPEED_OF_LIGHT_VACUUM, (CONST_BOLTZMANN, -1))
)
"""Second radiation constant, ([CODATA 2022][isqx._citations.CODATA2022])."""
# the following constants are not defined by CODATA 2022, but are widely used
CONST_DENSITY_HG: Annotated[Decimal, KG * CU_M**-1] = Decimal("13595.1")
"""Density of mercury at 0 °C and 101.325 kPa. For use in [`isqx.MMHG`][]."""
CONST_STANDARD_GRAVITY: Annotated[Decimal, M_PERS2] = Decimal("9.80665")
"""Standard acceleration of gravity, defined by the 3rd CGPM (1901)."""
CONST_DENSITY_H2O: Annotated[int, KG * CU_M**-1] = 1000
"""Conventional density of water. For use in [`isqx.MMH2O`][]."""
CONST_STANDARD_PRESSURE_ATM: Annotated[int, PA] = 101_325
"""Standard pressure, defined by the 10th CGPM (1954)."""
CONST_STANDARD_PRESSURE_IUPAC: Annotated[int, PA] = 100_000
"""Standard pressure, for use in specifying the properties of substances,
defined by the IUPAC (1982)."""


#
# non-si units accepted for use with the si [SI table 8] [SP811 table 6 & 7]
#

# time
MIN = (60 * S).alias("minute")
"""Minute, a unit of [time][isqx.TIME]."""
HOUR = (60 * MIN).alias("hour")
"""Hour, a unit of [time][isqx.TIME]."""
DAY = (24 * HOUR).alias("day")
"""Day, a unit of [time][isqx.TIME]."""
YEAR = (Decimal("365.25") * DAY).alias("year")
ANNUS = (Decimal("365.25") * DAY).alias("annus", allow_prefix=True)

# length
AU = (149_597_870_700 * M).alias("astronomical_unit")
"""Astronomical unit, as defined by IAU 2012 Resolution B2."""
PC = (LazyProduct((648_000, (_PI, -1))) * AU).alias("parsec")
"""Parsec"""
LY = (CONST_SPEED_OF_LIGHT_VACUUM * YEAR).alias("light_year", allow_prefix=True)
"""Light-year, a unit of astronomical [length][isqx.LENGTH], defined as the
[distance][isqx.DISTANCE] that light travels in the vacuum in one year."""

# plane and phase angle
DEG = (LazyProduct((_PI, (180, -1))) * RAD).alias("degree")
"""Degrees (°), a unit of plane [angle][isqx.ANGLE]."""
MIN_ANGLE = (Fraction(1, 60) * DEG).alias("minute_angle")
"""Minutes (′), a unit of plane [angle][isqx.ANGLE]."""
SEC_ANGLE = (Fraction(1, 60) * MIN_ANGLE).alias("second_angle")
"""Seconds (″) or arcseconds in astronomy, a unit of plane [angle][isqx.ANGLE]."""
REV = (LazyProduct((2, _PI)) * RAD).alias("revolution")
"""Revolutions, a unit of plane [angle][isqx.ANGLE]."""

# area
SQ_M = M**2
ARE = (100 * SQ_M).alias("are")
HECTARE = (100 * ARE).alias("hectare")
"""Hectare, a unit of land [area][isqx.AREA], as adopted by the CIPM in 1879."""

# volume
CU_M = M**3
L = (Fraction(1, 10**3) * CU_M).alias("liter", allow_prefix=True)
"""Liter, a unit of [volume][isqx.VOLUME], as adopted by the 16th CGPM in 1979."""

# mass
TONNE = (1_000 * KG).alias("tonne", allow_prefix=True)
"""Tonne, a unit of [mass][isqx.MASS], also known as the `metric ton` in the U.S."""
U = (Decimal("1.660538782e-27") * KG).alias("unified_atomic_mass_unit")
# NOTE: `amu` is not acceptable [SP811 Table 7]
"""Unified atomic mass unit, also known as the `dalton`."""

# energy
EV = (CONST_ELEMENTARY_CHARGE * J).alias("electronvolt", allow_prefix=True)
"""Electronvolt, the kinetic [energy][isqx.ENERGY] acquired by an electron in
passing through a  potential difference of 1 [volt][isqx.V] in vacuum."""

# logarithmic quantities [ISO 80000-3:2006] [SP811 8.7]
BEL = Log(_RATIO, base=10).alias("bel", allow_prefix=True)
r"""Bel, a logarithmic unit of a generic ratio.
When used for a power quantity, it is $L_B = \log_{10}(P/P_{ref})$.
The decibel (dB) is more commonly used."""
NEPER = Log(_RATIO, base=_E).alias("neper", allow_prefix=True)
r"""Neper, a logarithmic unit of a generic ratio.
When used for a root-power quantity, it is $L_{Np} = \ln(F/F_{ref})$."""
DB = DECI * BEL
r"""A decibel level for a power quantity,
$L_{dB} = 10 \log_{10}(\text{ratio})$."""
DB_ROOT_POWER = 2 * (DECI * BEL)
r"""A decibel level for a root-power (field) quantity,
$L_{dB} = 20 \log_{10}(\text{ratio})$."""

# decibel levels for root-power quantities (voltage)
DBV = (20 * Log(ratio(V, Quantity(1, V)), base=10)).alias(
    "dBV", allow_prefix=True
)
"""Decibel, [voltage][isqx.VOLTAGE] relative to 1 volt, regardless of impedance."""
CONST_DBU_REF: Annotated[LazyProduct, V] = LazyProduct(
    ((Decimal("0.6"), Fraction(1, 2)),)
)
DBU = (20 * Log(ratio(V, Quantity(CONST_DBU_REF, V)), base=10)).alias(
    "dBu", allow_prefix=True
)
"""Decibel, [voltage][isqx.VOLTAGE] relative to ~0.775 volt (the voltage that
dissipates 1 milliwatt in a 600 ohm load)."""
DBMV = (20 * Log(ratio(V, Quantity(1, MILLI * V)), base=10)).alias(
    "dBmV", allow_prefix=True
)
"""Decibel, [voltage][isqx.VOLTAGE] relative to 1 millivolt."""
DBUV = (20 * Log(ratio(V, Quantity(1, MICRO * V)), base=10)).alias(
    "dBμV", allow_prefix=True
)
"""Decibel, [voltage][isqx.VOLTAGE] relative to 1 microvolt."""

# decibel levels for power quantities
Z_METEO = (MILLI * M) ** 6 * M**-3
DBZ = (10 * Log(ratio(Z_METEO, Quantity(1, Z_METEO)), base=10)).alias(
    "dBZ", allow_prefix=True
)
"""Decibel, reflectivity factor Z relative to 1 mm⁶ m⁻³ for weather radar."""
DBM = (10 * Log(ratio(W, Quantity(1, MILLI * W)), base=10)).alias(
    "dBm", allow_prefix=True
)
"""Decibel, [power][isqx.POWER] relative to 1 milliwatt."""
DBW = (10 * Log(ratio(W, Quantity(1, W)), base=10)).alias(
    "dBW", allow_prefix=True
)
"""Decibel, [power][isqx.POWER] relative to 1 watt."""

# neper levels
NPV = Log(ratio(V, Quantity(1, V)), base=_E).alias("NpV", allow_prefix=True)
"""Neper, [voltage][isqx.VOLTAGE] relative to 1 volt."""
NPW = (Fraction(1, 2) * Log(ratio(W, Quantity(1, W)), base=_E)).alias(
    "NpW", allow_prefix=True
)
r"""Neper, [power][isqx.POWER] relative to 1 watt."""

# information theory [ISO 80000-1, Annex C]
# misc

# [SP811 table 9]
ANGSTROM = (Fraction(1, 10**10) * M).alias("angstrom")
"""Ångström, a unit of [length][isqx.LENGTH]."""
BARN = (Fraction(1, 10**28) * SQ_M).alias("barn", allow_prefix=True)
"""Barn, a unit of [area][isqx.AREA] for nuclear cross sections."""
BAR = (10**5 * PA).alias("bar", allow_prefix=True)
"""Bar, a unit of [pressure][isqx.PRESSURE]."""

MMHG = (
    LazyProduct((CONST_DENSITY_HG, CONST_STANDARD_GRAVITY)) * (MILLI * M)
).alias("millimeter_of_hg")
"""Millimeter of mercury, a unit of [pressure][isqx.PRESSURE]."""
MMH2O = (
    LazyProduct((CONST_DENSITY_H2O, CONST_STANDARD_GRAVITY)) * (MILLI * M)
).alias("millimeter_of_h2o")
"""Millimeter of water (conventional), a unit of [pressure][isqx.PRESSURE]."""  # [H44 C-59, footnote 12]
CURIE = (Decimal("3.7e10") * BQ).alias("curie")
"""Curie, a legacy unit of radioactivity.
The SI unit [becquerel][isqx.BQ] is preferred."""
ROENTGEN = (Decimal("2.58e-4") * (C * KG**-1)).alias("roentgen")
"""Roentgen, a legacy unit of exposure to ionizing radiation.
The SI unit [coulomb][isqx.C] per [kilogram][isqx.KG] is preferred."""
RD_ABSORBED = (Fraction(1, 100) * GY).alias("rd")
"""Rad, a legacy unit of absorbed dose. The SI unit [gray][isqx.GY] is preferred.
Not to be confused with the [radian][isqx.RAD]."""
REM = (Fraction(1, 100) * SV).alias("rem")
"""Rem (roentgen equivalent in man), a legacy unit of dose equivalent.
The SI unit [sievert][isqx.SV] is preferred."""


# examples of other unacceptable units [SP811 table 11]
FERMI = (Fraction(1, 10**5) * M).alias("fermi")
"""Fermi, an obsolete name for the femtometer."""
ATM = (CONST_STANDARD_PRESSURE_ATM * PA).alias("atmosphere")
"""Standard atmosphere, a unit of [pressure][isqx.PRESSURE]."""
TORR = (Fraction(1, 760) * ATM).alias("torr")
"""Torr, a unit of [pressure][isqx.PRESSURE]."""
KGF = (CONST_STANDARD_GRAVITY * KG * M_PERS2).alias("kg_force")
"""Kilogram-force."""
KWH = ((KILO * W) * HOUR).alias("kilowatt_hour")
"""Kilowatt-hour, commonly used as a billing unit for electric [energy][isqx.ENERGY]."""
KPH = ((KILO * M) * HOUR**-1).alias("kph")
"""Kilometers per hour."""
# TODO: phon, sone
# NOTE: not defining clo, darcy, denier, langley [SP811 B.8]

# other misc units
VA = (V * A).alias("volt_ampere", allow_prefix=True)
"""Volt-ampere, a unit of [apparent power][isqx.APPARENT_POWER]."""
VAR = (V * A).alias("var", allow_prefix=True)
"""Volt-ampere reactive, a unit of [reactive power][isqx.REACTIVE_POWER]."""

#
# quantity kinds
#

#
# space and time [ISO 80000-3] [IEV 113-01]
#

LENGTH = QtyKind(M)
"""Measured dimension of an object in a physical space."""
WIDTH = LENGTH["width"]
"""Horizontal dimension of an entity."""
# NOTE: beam (nautical) should be in a new module
HEIGHT = LENGTH["height"]
"""[Distance][isqx.DISTANCE] between the lowest and highest end of an object.

More specifically, ICAO defines it as "the vertical distance
of a level, a point or an object considered as a point, measured from a specific
datum.". Specify the particular datum using the [`isqx.OriginAt`][] tag.
"""
DEPTH = LENGTH["depth"]
"""A measure of [distance][isqx.DISTANCE] downwards from a surface."""
RELATIVE_TO_MSL = OriginAt("mean_sea_level")
ALTITUDE = LENGTH["altitude", RELATIVE_TO_MSL]
"""The vertical [distance][isqx.DISTANCE] of a level, a point or an object
considered as a point, measured from the
[mean sea level][isqx.RELATIVE_TO_MSL] (as defined by ICAO).

For the different kinds of altitude, see the [`isqx.aerospace`][] module."""
ELEVATION = LENGTH["elevation", RELATIVE_TO_MSL]
"""The vertical [distance][isqx.DISTANCE] of a point or a level, on or affixed
to the surface of the Earth, measured from
[mean sea level][isqx.RELATIVE_TO_MSL] (as defined by ICAO)."""
THICKNESS = LENGTH["thickness"]
"""Extent from one surface to the opposite, usually in the smallest solid
dimension."""
DIAMETER = LENGTH["diameter"]
"""A straight line segment that passes through the center of a circle or
sphere; its [length][isqx.LENGTH]."""
RADIUS = LENGTH["radius"]
"""Segment in a circle or sphere from its center to its perimeter or surface,
and its [length][isqx.LENGTH]."""
ARC_LENGTH = LENGTH["arc_length"]
"""The [distance][isqx.DISTANCE] between two points along a section of a curve."""
DISTANCE = LENGTH["distance"]
"""[Length][isqx.LENGTH] of the straight line that connects two points in a
measurable space or in an observable physical space."""
RADIAL_DISTANCE = DISTANCE["radial"]
"""The radial [distance][isqx.DISTANCE] within a closed non-intersecting
curve/surface. Use [`isqx.OriginAt`][] to specify the origin."""
POSITION = QtyKind(M, ("position", VECTOR))
"""Vector representing the position of a point with respect to a given origin
and axes. Specify the origin with the [`isqx.OriginAt`][] tag and the coordinate
system (e.g. [`isqx.CARTESIAN`][])."""
INITIAL_POSITION = POSITION["initial"]
FINAL_POSITION = POSITION["final"]
DISPLACEMENT = QtyKind(M, ("displacement", VECTOR))
"""Vector that is the shortest [distance][isqx.DISTANCE] from the
[initial][isqx.INITIAL_POSITION] to the [final position][isqx.FINAL_POSITION] of a
point P."""
CURVATURE = QtyKind(M**-1, ("curvature",))
"""A measure of how much a curve deviates from being a straight line."""
RADIUS_OF_CURVATURE = QtyKind(M, ("radius_of_curvature",))
"""[Radius][isqx.RADIUS] of a circle which best approximates a curve at a given
point."""

AREA = QtyKind(SQ_M)
"""Quantity that expresses the extent of a two-dimensional surface or shape, or
planar lamina, in the plane."""
SURFACE_ELEMENT = AREA[DIFFERENTIAL]
"""See: https://en.wikipedia.org/wiki/Surface_integral"""
CROSS_SECTIONAL_AREA = AREA["cross_section"]
VOLUME = QtyKind(CU_M)
"""Quantity of three-dimensional space."""
VOLUME_ELEMENT = VOLUME[DIFFERENTIAL]
"""See: https://en.wikipedia.org/wiki/Volume_element"""
ANGLE = QtyKind(RAD, ("angle",))
"""A measure for how wide an angle is. For signed angles, use
[angular displacement][isqx.ANGULAR_DISPLACEMENT_CCW]."""
ANGULAR_DISPLACEMENT_CCW = ANGLE["displacement", "counterclockwise"]
"""Displacement measured angle-wise when a body is in circular or rotational
motion, positive counterclockwise."""
ANGULAR_DISPLACEMENT_CW = ANGLE["displacement", "clockwise"]
"""Change in the angular position of a point, positive clockwise."""
PHASE_ANGLE = ANGLE["phase"]
"""Angular measure of the phase of a complex number."""
SOLID_ANGLE = QtyKind(SR, ("angle", "solid"))
"""Measure of a subtended portion of a sphere, used to describe the apparent
size of items in a three-dimensional field of view."""  # TODO: differential

TIME = QtyKind(S)
INITIAL_TIME = TIME["initial"]
FINAL_TIME = TIME["final"]
DURATION = TIME[DELTA]
"""Physical quantity for describing the temporal distance between events."""
PERIOD = DURATION["period"]
"""Smallest temporal unit after which a process repeats."""
TIME_CONSTANT = QtyKind(S, ("time_constant",))
"""Measure for the response of a dynamic system to a change of the system
input."""
VELOCITY = QtyKind(M_PERS, (VECTOR,))
SPEED = VELOCITY["magnitude"]
ACCELERATION = QtyKind(M_PERS2, (VECTOR,))

RAD_PERS = RAD * S**-1
RAD_PERS2 = RAD * S**-2
# NOTE: not defining
ANGULAR_VELOCITY_CCW = QtyKind(RAD_PERS, (VECTOR, "counterclockwise"))
ANGULAR_VELOCITY_CW = QtyKind(RAD_PERS, (VECTOR, "clockwise"))
"""[Angular velocity][isqx.ANGULAR_VELOCITY_CCW], but positive clockwise."""
ANGULAR_ACCELERATION_CCW = QtyKind(RAD_PERS2, (VECTOR, "counterclockwise"))
ANGULAR_ACCELERATION_CW = QtyKind(RAD_PERS2, (VECTOR, "clockwise"))
"""[Angular acceleration][isqx.ANGULAR_ACCELERATION_CCW], but positive clockwise."""

FREQUENCY = QtyKind(HZ)
"""Number of occurrences or cycles per [time][isqx.TIME]."""
NUMBER_OF_REVOLUTIONS = Dimensionless("n_revolutions")
"""Physical quantity; number of revolutions of a rotating body or turns in a coil."""
ROTATIONAL_FREQUENCY = QtyKind(NUMBER_OF_REVOLUTIONS * S**-1)
ANGULAR_FREQUENCY = QtyKind(RAD_PERS)
WAVELENGTH = PERIOD["wave"]
"""Spatial [period][isqx.PERIOD] of a wave; the [distance][isqx.DISTANCE] over
which the wave's shape repeats; the inverse of the spatial frequency."""
WAVENUMBER = QtyKind(M**-1, ("wave",))
WAVEVECTOR = QtyKind(M**-1, ("wave", VECTOR))
"""Vector pointing in the direction of a wave and whose magnitude is equal to
the [wavenumber][isqx.WAVENUMBER]."""
ANGULAR_WAVENUMBER = QtyKind(RAD * M**-1, ("wave",))
ANGULAR_WAVEVECTOR = QtyKind(RAD * M**-1, ("wave", VECTOR))
"""See: https://en.wikipedia.org/wiki/Wave_vector"""
PHASE_SPEED = SPEED["phase"]
GROUP_SPEED = SPEED["group"]
"""Speed at which a wave's envelope propagates in space."""
DAMPING_COEFFICIENT = QtyKind(S**-1, ("damping_coefficient",))
LOGARITHMIC_DECREMENT = QtyKind(Dimensionless("logarithmic_decrement"))
"""Measure for the damping of an oscillator."""
ATTENUATION = QtyKind(M**-1, ("attenuation",))
PHASE_COEFFICIENT = QtyKind(RAD * M**-1, ("phase_coefficient",))
PROPAGATION_CONSTANT = QtyKind(M**-1, ("propagation_constant", COMPLEX))

#
# mechanics [ISO 80000-4] [IEV 113-03]
#

MASS = QtyKind(KG)
"""Property of matter to resist changes of the state of motion and to attract
other bodies."""

DENSITY = QtyKind(KG * M**-3)

SPECIFIC_VOLUME = QtyKind(M**3 * KG**-1, ("specific_volume",))
REFERENCE_DENSITY = DENSITY["reference"]
RELATIVE_DENSITY = Dimensionless("specific_gravity")
SURFACE_DENSITY = QtyKind(KG * M**-2, ("density", "surface"))
LINEAR_DENSITY = QtyKind(KG * M**-1, ("density", "linear"))

MOMENTUM = QtyKind(KG * M_PERS, (VECTOR,))
"""Conserved physical quantity related to the motion of a body."""
FORCE = QtyKind(N, (VECTOR,))
"""Physical influence that tends to cause an object to change motion unless
opposed by other forces."""
ACCELERATION_OF_FREE_FALL = QtyKind(M_PERS2, ("free_fall", VECTOR))
"""At a point on Earth, vector sum of gravitational and centrifugal
[acceleration][isqx.ACCELERATION]."""
WEIGHT = FORCE["weight"]
FRICTION = FORCE["friction"]
STATIC_FRICTION = FRICTION["static"]
"""Subconcept of friction."""
KINETIC_FRICTION = FRICTION["kinetic"]
"""[Force][isqx.FORCE] opposing the motion of a body sliding on a surface."""
ROLLING_FRICTION = FRICTION["rolling"]
"""[Force][isqx.FORCE] resisting the motion when a body (such as a ball, tire, or
wheel) rolls on a surface."""
DRAG = FORCE["drag"]
"""Retarding [force][isqx.FORCE] on a body moving in a fluid."""

NORMAL_FORCE = FORCE["normal"]
"""The component of a contact [force][isqx.FORCE] that is perpendicular to the
surface that an object contacts."""
TANGENTIAL_FORCE = FORCE["tangential"]
"""The component of a contact [force][isqx.FORCE] that is parallel to the
surface that an object contacts."""
COEFFICIENT_OF_STATIC_FRICTION = Dimensionless("coefficient_of_friction_static")
COEFFICIENT_OF_KINETIC_FRICTION = Dimensionless(
    "coefficient_of_friction_kinetic"
)
ROLLING_RESISTANCE_FACTOR = Dimensionless("rolling_resistance_factor")
DRAG_COEFFICIENT = Dimensionless("drag_coefficient")
"""Dimensionless parameter to quantify fluid resistance."""  # also defined in ISO 80000-11

IMPULSE = QtyKind(N * S, (VECTOR,))
ANGULAR_MOMENTUM = QtyKind(J * S, (VECTOR,))
"""Measure of the extent to which an object will continue to rotate in the
absence of an applied torque."""
MOMENT_OF_FORCE = QtyKind(N * M, ("moment", VECTOR))
TORQUE = QtyKind(N * M, ("torque", VECTOR))
"""Tendency of a [force][isqx.FORCE] to rotate an object; counterpart of force in
rotational systems."""
ANGULAR_IMPULSE = QtyKind(N * M * S, (VECTOR,))
PRESSURE = QtyKind(PA)
"""The [force][isqx.FORCE] applied perpendicular to the surface of an object per
unit [area][isqx.AREA]. Also known as total pressure."""
STATIC_PRESSURE = PRESSURE["static"]
"""[Pressure][isqx.PRESSURE] in the absence of sound waves."""
GAUGE_PRESSURE = PRESSURE["gauge"]
DYNAMIC_PRESSURE = PRESSURE["dynamic"]
"""See: https://en.wikipedia.org/wiki/Dynamic_pressure"""
STRESS = QtyKind(PA, ("stress",))
STRESS_TENSOR = STRESS[TENSOR_SECOND_ORDER]
"""Tensor that describes the state of stress at a point inside a material."""
NORMAL_STRESS = QtyKind(
    PA, ("stress", "normal")
)  # NOTE: not inheriting from stress because they are not tensors.
SHEAR_STRESS = QtyKind(PA, ("stress", "shear"))
"""Component of [stress][isqx.STRESS] coplanar with a material cross section."""
STRAIN = Dimensionless("strain")
STRAIN_TENSOR = STRAIN[TENSOR_SECOND_ORDER, CARTESIAN]
"""Symmetric tensor quantity of the strain caused by [stress][isqx.STRESS] in
matter."""
LINEAR_STRAIN = Dimensionless(
    "linear_strain"
)  # TODO: allow microstrain and nanostrain
SHEAR_STRAIN = Dimensionless("shear_strain")
VOLUMETRIC_STRAIN = Dimensionless("volumetric_strain")
POISSONS_RATIO = Dimensionless("poissons_ratio")
YOUNGS_MODULUS = QtyKind(PA, ("youngs_modulus",))  # TODO: adiabatic, isothermal
"""A mechanical property that measures stiffness of a solid material."""
SHEAR_MODULUS = QtyKind(PA, ("shear_modulus",))  # TODO: isentropic, isothermal
BULK_MODULUS = QtyKind(PA, ("bulk_modulus",))  # TODO: isentropic, isothermal
"""Measure of how incompressible / resistant to compressibility a substance is."""
COMPRESSIBILITY = QtyKind(
    PA**-1, ("compressibility",)
)  # TODO: isentropic, isothermal
MOMENT_OF_INERTIA = QtyKind(KG * M**2, (TENSOR_SECOND_ORDER,))
SECOND_AXIAL_MOMENT_OF_AREA = QtyKind(M**4, ("second_axial_moment_of_area",))
r"""Property of an [area][isqx.AREA] reflecting how its points are distributed
with respect to an axis."""
SECOND_POLAR_MOMENT_OF_AREA = QtyKind(M**4, ("second_polar_moment_of_area",))
r"""See: https://en.wikipedia.org/wiki/Second_polar_moment_of_area"""
SECTION_MODULUS = QtyKind(M**3, ("section_modulus", "elastic"))
"""Concept in structural analysis."""
# NOTE: not defining plastic section modulus
DYNAMIC_VISCOSITY = QtyKind(PA * S)
"""Physical property of a moving fluid."""
KINEMATIC_VISCOSITY = QtyKind(M**2 * S**-1)
"""Characteristic of a fluid."""
SURFACE_TENSION = QtyKind(N * M**-1, ("surface_tension",))
"""Tendency of a liquid surface to shrink to reduce surface area."""

ENERGY = QtyKind(J)
"""Quantitative property of a physical system, recognizable in the performance
of [work][isqx.WORK] and in the form of [heat][isqx.HEAT] and light."""
POWER = QtyKind(W)
POTENTIAL_ENERGY = ENERGY["potential"]
"""[Energy][isqx.ENERGY] held by an object because of its
[position][isqx.POSITION] relative to other objects or stresses within itself,
rather than its [velocity][isqx.VELOCITY]."""
KINETIC_ENERGY = ENERGY["kinetic"]
"""[Energy][isqx.ENERGY] of a moving physical body."""
MECHANICAL_ENERGY = ENERGY["mechanical"]
LINE_ELEMENT = QtyKind(M, (DIFFERENTIAL, "displacement", VECTOR))
"""See: https://en.wikipedia.org/wiki/Line_element"""
WORK = QtyKind(J, ("work",))
"""[Energy][isqx.ENERGY] transferred to an object via the application of
[force][isqx.FORCE] on it through a [displacement][isqx.DISPLACEMENT]."""

MECHANICAL_EFFICIENCY = Dimensionless("efficiency_mechanical")
MASS_FLUX_DENSITY = QtyKind(KG * M**-2 * S**-1)
MASS_FLUX = QtyKind(KG * M**-2 * S**-1, (VECTOR,))
MASS_FLOW_RATE = QtyKind(KG * S**-1)
VOLUME_FLOW_RATE = QtyKind(M**3 * S**-1)
ACTION = QtyKind(J * S, ("action",))

#
# thermodynamics [ISO 80000-5] [IEV 113-04]
#
TEMPERATURE = QtyKind(K)
"""Thermodynamic temperature, an absolute measure of temperature."""
SURFACE_TEMPERATURE = TEMPERATURE["surface"]
REFERENCE_TEMPERATURE = TEMPERATURE["reference", "surrounding"]
HOT_RESERVOIR_TEMPERATURE = TEMPERATURE["hot_reservoir"]
"""Absolute temperature of hot reservoir."""
COLD_RESERVOIR_TEMPERATURE = TEMPERATURE["cold_reservoir"]
"""Absolute temperature of cold reservoir."""
TEMPERATURE_DIFFERENCE = TEMPERATURE[DELTA]
# NOTE: not defining qtykind(celsius) because temperature[celsius] covers it
LINEAR_EXPANSION_COEFFICIENT = QtyKind(K**-1, ("linear",))
VOLUMETRIC_EXPANSION_COEFFICIENT = QtyKind(K**-1, ("volumetric",))
# NOTE: commenting out the following two: cannot find much information on them
# and would clash with aerodynamics' definition of cp
_RELATIVE_PRESSURE_COEFFICIENT = QtyKind(K**-1, ("relative_pressure",))
_PRESSURE_COEFFICIENT = QtyKind(PA * K**-1, ("pressure_coefficient",))
ISOTHERMAL_COMPRESSIBILITY = COMPRESSIBILITY["isothermal"]
"""Negative relative change of [volume][isqx.VOLUME] per change of
[pressure][isqx.PRESSURE] at constant [temperature][isqx.TEMPERATURE]."""
ISENTROPIC_COMPRESSIBILITY = COMPRESSIBILITY["isentropic"]
"""Negative relative change of [volume][isqx.VOLUME] per change of
[pressure][isqx.PRESSURE] at constant [entropy][isqx.ENTROPY]."""
WORK_BY_SYSTEM = WORK["by_system"]
"""Work done by the system."""
WORK_ON_SYSTEM = WORK["on_system"]
"""Work done on the system."""
HEAT = QtyKind(J, ("heat",))
"""[Energy][isqx.ENERGY] that is transferred from one body to another as the
result of a difference in [temperature][isqx.TEMPERATURE]."""
HEAT_TO_SYSTEM = HEAT["to_system"]
"""Heat transferred to the system."""
INEXACT_DIFFERENTIAL_HEAT = HEAT[INEXACT_DIFFERENTIAL]
LATENT_HEAT = HEAT["latent"]
"""Released or absorbed [energy][isqx.ENERGY] during a constant-temperature
process."""
SPECIFIC_LATENT_HEAT = QtyKind(J * KG**-1, ("specific_latent_heat",))
MOLAR_LATENT_HEAT = QtyKind(J * MOL**-1, ("molar_latent_heat",))
HEAT_FLOW_RATE = QtyKind(W, ("heat_flow",))
HEAT_FLUX = QtyKind(W * M**-2, ("heat_flux", VECTOR))
THERMAL_CONDUCTIVITY = QtyKind(W * M**-1 * K**-1)
"""Capacity of a material to conduct [heat][isqx.HEAT]."""
HEAT_TRANSFER_COEFFICIENT = QtyKind(W * M**-2 * K**-1)
"""Measure of [heat][isqx.HEAT] transfer on a surface."""
THERMAL_INSULANCE = QtyKind(M**2 * K * W**-1)
THERMAL_RESISTANCE = QtyKind(K * W**-1)
"""Objects' resistance to [heat][isqx.HEAT] transfer; reciprocal of
[thermal conductance][isqx.THERMAL_CONDUCTANCE]."""
THERMAL_CONDUCTANCE = QtyKind(W * K**-1)
"""Objects' ability to transfer [heat][isqx.HEAT]; reciprocal of
[thermal resistance][isqx.THERMAL_RESISTANCE]."""
THERMAL_DIFFUSIVITY = QtyKind(M**2 * S**-1)
"""Physical quantity that measures the rate of transfer of [heat][isqx.HEAT] of a
material from the hot side to the cold side."""
HEAT_CAPACITY = QtyKind(J * K**-1, ("heat_capacity",))
"""Thermal property describing the [energy][isqx.ENERGY] required to change a
material's [temperature][isqx.TEMPERATURE]."""
HEAT_CAPACITY_P = HEAT_CAPACITY["constant_pressure"]
"""Heat capacity at constant pressure (isobaric)."""
HEAT_CAPACITY_V = HEAT_CAPACITY["constant_volume"]
"""Heat capacity at constant volume (isochoric)."""
SPECIFIC_HEAT_CAPACITY = QtyKind(
    J * KG**-1 * K**-1, ("specific_heat_capacity",)
)
SPECIFIC_HEAT_CAPACITY_P = SPECIFIC_HEAT_CAPACITY["constant_pressure"]
"""Specific heat capacity at constant pressure (isobaric)."""
SPECIFIC_HEAT_CAPACITY_V = SPECIFIC_HEAT_CAPACITY["constant_volume"]
"""Specific heat capacity at constant volume (isochoric)."""
SPECIFIC_HEAT_CAPACITY_SAT = SPECIFIC_HEAT_CAPACITY["saturation"]
HEAT_CAPACITY_RATIO = Dimensionless("heat_capacity_ratio")
"""Thermodynamic ratio of isobaric to isochoric specific heat capacities."""
ISENTROPIC_EXPONENT = Dimensionless("isentropic_exponent")
"""The negative of the relative [pressure][isqx.PRESSURE] change per relative
[volume][isqx.VOLUME] change at constant [entropy][isqx.ENTROPY]; for an ideal gas
equal to the ratio of specific heat capacities."""
# TODO: molar specific heats with \tilde{c}
ENTROPY = QtyKind(J * K**-1, ("entropy",))
"""Physical property of the state of a system, measure of disorder."""
SPECIFIC_ENTROPY = QtyKind(J * KG**-1 * K**-1, ("specific_entropy",))
INTERNAL_ENERGY = ENERGY["internal"]
"""State quantity, energy of a system whose change is the
[heat transferred to the system][isqx.HEAT_TO_SYSTEM] minus the
[work done by the system][isqx.WORK_BY_SYSTEM] (closed system, no chemical
reactions)."""
ENTHALPY = ENERGY["enthalpy"]
"""Measure of [energy][isqx.ENERGY] in a thermodynamic system; thermodynamic
quantity equivalent to the total [heat][isqx.HEAT] content of a system."""
HELMHOLTZ_ENERGY = ENERGY["helmholtz"]
"""Thermodynamic potential."""
GIBBS_ENERGY = ENERGY["gibbs"]
"""Type of thermodynamic potential; useful for calculating reversible
[work][isqx.WORK] in certain systems."""
ACTIVATION_ENERGY = ENERGY["activation"]
SPECIFIC_ENERGY = QtyKind(J * KG**-1, ("specific_energy",))
"""Physical quantity representing [energy][isqx.ENERGY] content per unit
[mass][isqx.MASS]."""
SPECIFIC_INTERNAL_ENERGY = SPECIFIC_ENERGY["internal"]
SPECIFIC_ENTHALPY = SPECIFIC_ENERGY["enthalpy"]
SPECIFIC_HELMHOLTZ_ENERGY = SPECIFIC_ENERGY["helmholtz"]
SPECIFIC_GIBBS_ENERGY = SPECIFIC_ENERGY["gibbs"]
MASSIEU_FUNCTION = QtyKind(J * K**-1, ("massieu_function",))
PLANCK_FUNCTION = QtyKind(J * K**-1, ("planck_function",))
JOULE_THOMSON_COEFFICIENT = QtyKind(K * PA**-1, ("joule_thomson_coefficient",))
THERMAL_EFFICIENCY = Dimensionless("efficiency_thermal")
CARNOT_EFFICIENCY = Dimensionless("efficiency_thermal_carnot")
"""Efficiency of an ideal heat engine operating according to the Carnot
process."""
MASS_OF_SINGLE_PARTICLE = MASS["single_particle"]
SPECIFIC_GAS_CONSTANT = QtyKind(J * KG**-1 * K**-1, ("specific_gas_constant",))
MASS_CONCENTRATION = QtyKind(KG * M**-3, ("mass_concentration",))
WATER_VAPOUR_MASS = MASS["water"]
WATER_MASS_CONCENTRATION = MASS_CONCENTRATION["water"]
WATER_VAPOUR_MASS = MASS["water_vapour"]
WATER_VAPOUR_MASS_CONCENTRATION = MASS_CONCENTRATION["water_vapour"]
WATER_VAPOUR_MASS_CONCENTRATION_AT_SATURATION = WATER_VAPOUR_MASS_CONCENTRATION[
    "saturation"
]
DRY_MATTER_MASS = MASS["dry_matter"]
WATER_TO_DRY_MATTER_MASS_RATIO = Dimensionless("mass_ratio_water_to_dry_matter")
DRY_GAS_MASS = MASS["dry_gas"]
WATER_VAPOUR_TO_DRY_GAS_MASS_RATIO = Dimensionless(
    "mass_ratio_water_vapour_to_dry_gas"
)
"""Physical / meteorological quantity."""
WATER_VAPOUR_TO_DRY_GAS_MASS_RATIO_AT_SATURATION = (
    WATER_VAPOUR_TO_DRY_GAS_MASS_RATIO["saturation"]
)
"""Also known as mixing ratio."""
MASS_FRACTION = Dimensionless("mass_fraction")  # defined in ISO 80000-9
WATER_MASS_FRACTION = MASS_FRACTION["water"]
DRY_MATTER_MASS_FRACTION = MASS_FRACTION["dry_matter"]
PARTIAL_PRESSURE = PRESSURE["partial"]  # defined in ISO 80000-9
"""Hypothetical [pressure][isqx.PRESSURE] of gas if it alone occupied the
[volume][isqx.VOLUME] of the mixture at the same [temperature][isqx.TEMPERATURE]."""
WATER_VAPOUR_PARTIAL_PRESSURE = PARTIAL_PRESSURE["water_vapour"]
"""Saturation vapour pressure of water."""
SATURATION_WATER_VAPOUR_PARTIAL_PRESSURE = WATER_VAPOUR_PARTIAL_PRESSURE[
    "saturation"
]
RELATIVE_HUMIDITY = Dimensionless("relative_humidity")
r"""Ratio of the [partial pressure][isqx.PARTIAL_PRESSURE] of water vapor in
humid air to the equilibrium vapor pressure of water at a given
[temperature][isqx.TEMPERATURE]."""
RELATIVE_MASS_CONCENTRATION_VAPOUR = Dimensionless(
    "relative_mass_concentration_vapour"
)
"""Quotient of the [mass concentration][isqx.MASS_CONCENTRATION] of water vapor
and the mass concentration at saturation at a given
[temperature][isqx.TEMPERATURE]."""
RELATIVE_MASS_RATIO_VAPOUR = Dimensionless("relative_mass_ratio_vapour")
"""Quotient of the mass ratio of water vapor to dry air and the mass ratio of
water vapor to dry air at saturation at a given
[temperature][isqx.TEMPERATURE]. Approximation to
[relative humidity][isqx.RELATIVE_HUMIDITY]."""
DEW_POINT = TEMPERATURE["dew_point"]
"""The [temperature][isqx.TEMPERATURE] at which air becomes saturated with water
vapour."""
#
# electromagnetism [ISO 80000-6] [IEV]
#
CURRENT = QtyKind(A)
"""Base quantity of the International System of Quantities (ISQ), measured in
[ampere][isqx.A] (A)."""
INSTANTANEOUS_CURRENT = CURRENT["instantaneous"]
RMS_CURRENT = CURRENT["rms"]
"""Root mean square current."""
ELECTRIC_CHARGE = QtyKind(C)
"""Physical property that quantifies an object's interaction with electric
fields."""
CHARGE_DENSITY = QtyKind(C * M**-3)
SURFACE_CHARGE_DENSITY = QtyKind(C * M**-2)
LINEAR_CHARGE_DENSITY = QtyKind(C * M**-1)
ELECTRIC_DIPOLE_MOMENT = QtyKind(C * M, (VECTOR,))
"""Vector physical quantity measuring the separation of positive and negative
electrical charges within a system."""
POLARIZATION_DENSITY = QtyKind(C * M**-2, ("polarization", VECTOR))
CURRENT_DENSITY = QtyKind(A * M**-2, (VECTOR,))
LINEAR_CURRENT_DENSITY = QtyKind(A * M**-1, (VECTOR,))
ELECTRIC_FIELD_STRENGTH = QtyKind(V * M**-1, (VECTOR,))
"""Vector physical quantity of electrostatics and electrodynamics."""
ELECTRIC_POTENTIAL = QtyKind(V, ("potential",))
"""Line integral of the electric field."""
ELECTRIC_POTENTIAL_DIFFERENCE = QtyKind(V, ("potential", DELTA))
VOLTAGE = QtyKind(V, (DELTA,))
"""In circuit theory, for a conductor, electric
[potential difference][isqx.ELECTRIC_POTENTIAL_DIFFERENCE] between two points."""
INDUCED_VOLTAGE = VOLTAGE["induced"]
"""See: https://en.wikipedia.org/wiki/Electromagnetic_induction"""
INSTANTANEOUS_VOLTAGE = VOLTAGE["instantaneous"]
RMS_VOLTAGE = VOLTAGE["rms"]
"""Root mean square voltage."""
# TODO: Vpp, Vpk
ELECTRIC_FLUX_DENSITY = QtyKind(C * M**-2, ("flux_density", VECTOR))
"""Vector field related to displacement current and flux density."""
CAPACITANCE = QtyKind(F)
"""Ability of a body to store electrical [charge][isqx.ELECTRIC_CHARGE]."""
PERMITTIVITY = QtyKind(F * M**-1)
"""Physical quantity, measure of the resistance to the electric field."""
RELATIVE_PERMITTIVITY = Dimensionless("relative_permittivity")
ELECTRIC_SUSCEPTIBILITY = Dimensionless("electric_susceptibility")
"""Degree of polarization."""
ELECTRIC_FLUX = QtyKind(C, ("flux",))
"""Surface integral of the electric [flux density][isqx.ELECTRIC_FLUX_DENSITY];
measured in coulombs."""
DISPLACEMENT_CURRENT_DENSITY = CURRENT_DENSITY["displacement"]
DISPLACEMENT_CURRENT = CURRENT["displacement"]
TOTAL_CURRENT = CURRENT["total"]
TOTAL_CURRENT_DENSITY = CURRENT_DENSITY["total"]
MAGNETIC_FLUX_DENSITY = QtyKind(T, ("flux_density", VECTOR))
"""Vector physical quantity describing production of a potential difference
across a conductor when it is exposed to a varying magnetic field."""
MAGNETIC_FLUX = QtyKind(WB)
PROTOFLUX = QtyKind(WB, ("proto",))
"""Integral of the [magnetic vector potential][isqx.MAGNETIC_VECTOR_POTENTIAL]
along a path."""
LINKED_MAGNETIC_FLUX = MAGNETIC_FLUX["linked"]
"""See: https://en.wikipedia.org/wiki/Flux_linkage"""
TOTAL_MAGNETIC_FLUX = MAGNETIC_FLUX["total"]
"""Highest value of [magnetic flux][isqx.MAGNETIC_FLUX] produced by a current
loop in circuit theory.
The definition is consistent with the more general definition of
[linked flux][isqx.LINKED_MAGNETIC_FLUX].
"""
MAGNETIC_MOMENT = QtyKind(A * M**2, (VECTOR,))
MAGNETIZATION = QtyKind(A * M**-1, ("magnetization", VECTOR))
MAGNETIC_FIELD_STRENGTH = QtyKind(
    A * M**-1, ("magnetic_field_strength", VECTOR)
)
"""Strength of a magnetic field."""
PERMEABILITY = QtyKind(H * M**-1)
"""Measure of the ability of a material to support the formation of a magnetic
field within itself."""
RELATIVE_PERMEABILITY = Dimensionless("relative_permeability")
MAGNETIC_SUSCEPTIBILITY = Dimensionless("magnetic_susceptibility")
"""Measure of how much a material will become magnetized in an applied magnetic
field."""
MAGNETIC_POLARIZATION = QtyKind(T, ("polarization", VECTOR))
MAGNETIC_DIPOLE_MOMENT = QtyKind(WB * M, (VECTOR,))
"""Physical quantity; measured in weber metre."""
COERCIVITY = QtyKind(A * M**-1, ("coercivity",))
"""Measure of the ability of a ferromagnetic material to withstand an external
magnetic field without becoming demagnetized."""
MAGNETIC_VECTOR_POTENTIAL = QtyKind(WB * M**-1, (VECTOR,))
ENERGY_DENSITY = QtyKind(J * M**-3, ("energy_density",))
ELECTROMAGNETIC_ENERGY_DENSITY = ENERGY_DENSITY["electromagnetic"]
POYNTING_VECTOR = QtyKind(W * M**-2, ("poynting", VECTOR))
"""Measure of directional [energy][isqx.ENERGY] flux."""
SPEED_OF_LIGHT = PHASE_SPEED["light"]  # defined in ISO80000-7
"""Phase [speed][isqx.SPEED] of an electromagnetic wave in a medium."""
SOURCE_VOLTAGE = VOLTAGE["ideal_source"]
"""Scalar physical quantity homogeneous to a [voltage][isqx.VOLTAGE], expressing
the modulus of the [force][isqx.FORCE] exerted on a [charge][isqx.ELECTRIC_CHARGE]
in an electric field."""
MAGNETIC_POTENTIAL = QtyKind(A, ("magnetic_potential",))
"""Scalar potential whose negative gradient is the
[magnetic field strength][isqx.MAGNETIC_FIELD_STRENGTH]."""
MAGNETIC_TENSION = QtyKind(A, ("magnetic_tension",))
N_TURNS_WINDING = Dimensionless("n_turns_winding")
MAGNETOMOTIVE_FORCE = QtyKind(A, ("magnetomotive_force",))
"""A quantity representing the sum of magnetizing forces along a circuit."""
RELUCTANCE = QtyKind(H**-1)
"""In physics, the ratio of [magnetomotive force][isqx.MAGNETOMOTIVE_FORCE] to
[magnetic flux][isqx.MAGNETIC_FLUX]; the magnetic analogue of electrical
resistance."""
PERMEANCE = QtyKind(H, ("permeance",))
INDUCTANCE = QtyKind(H, ("inductance",))
"""Property of electrical conductors to oppose changes in [current][isqx.CURRENT]
flow."""
MUTUAL_INDUCTANCE = INDUCTANCE["mutual"]
COUPLING_FACTOR = Dimensionless("coupling_factor")
LEAKAGE_FACTOR = Dimensionless("leakage_factor")
CONDUCTIVITY = QtyKind(SIEMENS * M**-1)
"""Physical quantity and property of material describing how readily a given
material allows the flow of electric [current][isqx.CURRENT]."""
RESISTIVITY = QtyKind(OHM * M)
INSTANTANEOUS_POWER = POWER["instantaneous"]
# TODO: average
RESISTANCE = QtyKind(OHM)
"""Opposition to the passage of an electric [current][isqx.CURRENT]."""
CONDUCTANCE = QtyKind(SIEMENS, ("conductance",))
VOLTAGE_PHASE_ANGLE = PHASE_ANGLE[VOLTAGE]
CURRENT_PHASE_ANGLE = PHASE_ANGLE[CURRENT]
PHASE_DIFFERENCE = PHASE_ANGLE[DELTA]
CURRENT_PHASOR = CURRENT["phasor", COMPLEX]
"""Complex representation of an oscillating electric [current][isqx.CURRENT]."""
VOLTAGE_PHASOR = VOLTAGE["phasor", COMPLEX]
"""Complex representation of an oscillating [voltage][isqx.VOLTAGE]."""
IMPEDANCE = QtyKind(OHM, ("impedance", COMPLEX))
IMPEDANCE_APPARENT = QtyKind(OHM, ("impedance", "apparent"))
IMPEDANCE_OF_VACUUM = IMPEDANCE["vacuum"]
"""Physical constant relating the magnitudes of the electric and magnetic fields
of electromagnetic radiation travelling through free space."""
AC_RESISTANCE = QtyKind(OHM, ("alternating_current",))
"""Real part of the complex [impedance][isqx.IMPEDANCE]."""
REACTANCE = QtyKind(OHM, ("reactance",))
"""A circuit element's opposition to changes in electric [current][isqx.CURRENT]
due to its [inductance][isqx.INDUCTANCE] or [capacitance][isqx.CAPACITANCE]."""
ADMITTANCE = QtyKind(SIEMENS, ("admittance", COMPLEX))
ADMITTANCE_APPARENT = QtyKind(SIEMENS, ("admittance", "apparent"))
ADMITTANCE_OF_VACUUM = QtyKind(SIEMENS, ("admittance", "vacuum"))
AC_CONDUCTANCE = QtyKind(SIEMENS, ("conductance", "alternating_current"))
"""Real part of the complex [admittance][isqx.ADMITTANCE]."""
SUSCEPTANCE = QtyKind(SIEMENS, ("susceptance",))
"""Imaginary part of the [admittance][isqx.ADMITTANCE]."""
QUALITY_FACTOR = Dimensionless("quality_factor")
"""Dimensionless quantity in electromagnetism."""
DISSIPATION_FACTOR = Dimensionless("loss_factor")
LOSS_ANGLE = QtyKind(RAD, ("loss_angle",))
ACTIVE_POWER = POWER["active"]
APPARENT_POWER = QtyKind(VA)
"""Product of RMS [voltage][isqx.VOLTAGE] and RMS [current][isqx.CURRENT] in an AC
electrical system."""
POWER_FACTOR = Dimensionless("power_factor")
COMPLEX_POWER = QtyKind(VA, (COMPLEX,))
"""Quantity in electromagnetism."""
REACTIVE_POWER = QtyKind(VAR)
"""Type of electrical power."""
NONACTIVE_POWER = QtyKind(VA, ("nonactive",))
"""Quantity in electromagnetism."""
ACTIVE_ENERGY = ENERGY["active"]

#
# light and radiation [ISO 80000-7]
#
# radiometric
REFRACTIVE_INDEX = Dimensionless("refractive_index")
RADIANT_ENERGY = QtyKind(J, ("radiant",))
"""[Energy][isqx.ENERGY] propagated by electromagnetic waves."""
SPECTRAL_RADIANT_ENERGY = QtyKind(J * M**-1, ("radiant", "spectral"))
RADIANT_ENERGY_DENSITY = ENERGY_DENSITY["radiant"]
SPECTRAL_RADIANT_ENERGY_DENSITY_WAVELENGTH = QtyKind(
    J * M**-4, ("radiant", "spectral", "wavelength")
)
SPECTRAL_RADIANT_ENERGY_DENSITY_WAVENUMBER = QtyKind(
    J * M**-2, ("radiant", "spectral", "wavenumber")
)
RADIANT_FLUX = QtyKind(W, ("radiant_flux",))
"""[Power][isqx.POWER] carried by electromagnetic waves."""
ABSORBED_RADIANT_FLUX = RADIANT_FLUX["absorbed"]
INCIDENT_RADIANT_FLUX = RADIANT_FLUX["incident"]
REFLECTED_RADIANT_FLUX = RADIANT_FLUX["reflected"]
TRANSMITTED_RADIANT_FLUX = RADIANT_FLUX["transmitted"]
SPECTRAL_RADIANT_FLUX = QtyKind(W * M**-1, ("radiant_flux", "spectral"))
RADIANT_INTENSITY = QtyKind(W * SR**-1)
SPECTRAL_RADIANT_INTENSITY = QtyKind(W * SR**-1 * M**-1)
RADIANCE = QtyKind(W * SR**-1 * M**-2)
"""Areal density of [radiant intensity][isqx.RADIANT_INTENSITY] in a given
direction."""
SPECTRAL_RADIANCE = QtyKind(W * SR**-1 * M**-3)
"""[Radiance][isqx.RADIANCE] of a surface."""
IRRADIANCE = QtyKind(W * M**-2, ("irradiance",))
SPECTRAL_IRRADIANCE = QtyKind(W * M**-3, ("irradiance",))
RADIANT_EXITANCE = QtyKind(W * M**-2, ("exitance",))
SPECTRAL_RADIANT_EXITANCE = QtyKind(W * M**-3, ("exitance",))
RADIANT_EXPOSURE = QtyKind(J * M**-2, ("radiant_exposure",))
SPECTRAL_RADIANT_EXPOSURE = QtyKind(J * M**-3, ("radiant_exposure", "spectral"))
LUMINOUS_EFFICIENCY = Dimensionless("luminous_efficiency")
"""Specify the [photometric condition][isqx.PhotometricCondition] with
[tags][isqx.Tagged]."""
SPECTRAL_LUMINOUS_EFFICIENCY = Dimensionless("spectral_luminous_efficiency")
"""Spectral sensitivity of human visual perception of brightness."""
LUMINOUS_EFFICACY_OF_RADIATION = QtyKind(LM * W**-1, ("radiation",))
SPECTRAL_LUMINOUS_EFFICACY = QtyKind(LM * W**-1, ("spectral",))
"""Specify the [photometric condition][isqx.PhotometricCondition] with
[tags][isqx.Tagged]."""
MAXIMUM_LUMINOUS_EFFICACY = QtyKind(LM * W**-1, ("maximum",))
LUMINOUS_EFFICACY_OF_SOURCE = QtyKind(LM * W**-1, ("source",))
"""See: https://www.electropedia.org/iev/iev.nsf/display?openform&ievref=845-21-089"""
# photometric
LUMINOUS_ENERGY = QtyKind(LM * S)
LUMINOUS_FLUX = QtyKind(LM)
ABSORBED_LUMINOUS_FLUX = LUMINOUS_FLUX["absorbed"]
INCIDENT_LUMINOUS_FLUX = LUMINOUS_FLUX["incident"]
REFLECTED_LUMINOUS_FLUX = LUMINOUS_FLUX["reflected"]
TRANSMITTED_LUMINOUS_FLUX = LUMINOUS_FLUX["transmitted"]
LUMINOUS_INTENSITY = QtyKind(CD)
LUMINANCE = QtyKind(CD * M**-2)
"""Photometric measure of the [luminous intensity][isqx.LUMINOUS_INTENSITY] per
[area][isqx.AREA] of light travelling in a given direction."""
ILLUMINANCE = QtyKind(LX)
LUMINOUS_EXITANCE = QtyKind(LM * M**-2)
LUMINOUS_EXPOSURE = QtyKind(LX * S)
# for photons
NUMBER_OF_PHOTONS = Dimensionless("photon_number")
PHOTON_ENERGY = QtyKind(J, ("photon",))
"""[Energy][isqx.ENERGY] carried by a single photon."""
PHOTON_FLUX = QtyKind(S**-1, ("photon_flux",))
PHOTON_INTENSITY = QtyKind(S**-1 * SR**-1)
PHOTON_RADIANCE = QtyKind(M**-2 * S**-1 * SR**-1)
"""[Area][isqx.AREA] density of the [photon intensity][isqx.PHOTON_INTENSITY] in a
specified direction."""
PHOTON_IRRADIANCE = QtyKind(M**-2 * S**-1, ("photon_irradiance",))
PHOTON_EXITANCE = QtyKind(M**-2 * S**-1, ("photon_exitance",))
PHOTON_EXPOSURE = QtyKind(M**-2, ("photon_exposure",))
CIE_COLOUR_MATCHING_FUNCTIONS_1931 = Dimensionless(
    "cie_colour_matching_functions_1931"
)
CIE_COLOUR_MATCHING_FUNCTIONS_1964 = Dimensionless(
    "cie_colour_matching_functions_1964"
)
# NOTE: tristimulus values X = k \int_0^\infty \phi_lambda(\lambda) \bar{x}(\lambda) d\lambda
# - sources: k can be maximum luminous efficacy -> units are CD * M**-2
# - object colours: k can be chosen so units become 1.
# applies for 1964 as well
# not defining them for now
CHROMATICITY_COORDINATES_1931 = Dimensionless("chromaticity_coordinates_1931")
"""See: https://en.wikipedia.org/wiki/CIE_1931_color_space"""
CHROMATICITY_COORDINATES_1964 = Dimensionless("chromaticity_coordinates_1964")
COLOUR_TEMPERATURE = TEMPERATURE["colour"]
"""Property of light sources related to black-body radiation."""
CORRELATED_COLOUR_TEMPERATURE = TEMPERATURE["correlated_colour"]
"""Property of light stimulus related to human perception."""
EMISSIVITY = Dimensionless("emissivity")
"""Effectiveness of an object in emitting thermal radiation."""
EMISSIVITY_AT_SPECIFIC_WAVELENGTH = Dimensionless(
    "emissivity_at_specific_wavelength"
)
"""[Emissivity][isqx.EMISSIVITY] as a function of [wavelength][isqx.WAVELENGTH]."""
ABSORPTANCE = Dimensionless("absorptance")
SPECTRAL_ABSORPTANCE = ABSORPTANCE["spectral"]
LUMINOUS_ABSORPTANCE = ABSORPTANCE["luminous"]
REFLECTANCE = Dimensionless("reflectance")
"""Capacity of an object to reflect light."""
SPECTRAL_REFLECTANCE = REFLECTANCE["spectral"]
LUMINOUS_REFLECTANCE = REFLECTANCE["luminous"]
TRANSMITTANCE = Dimensionless("transmittance")
SPECTRAL_TRANSMITTANCE = TRANSMITTANCE["spectral"]
LUMINOUS_TRANSMITTANCE = TRANSMITTANCE["luminous"]
ABSORBANCE = -1 * Log(TRANSMITTANCE, base=10)
"""Common logarithm of the ratio of incident to transmitted radiant power
through a material; the optical depth divided by ln(10)."""
NAPIERIAN_ABSORBANCE = -1 * Log(TRANSMITTANCE, base=_E)
RADIANCE_FACTOR = Dimensionless("radiance_factor")
LUMINANCE_FACTOR = Dimensionless("luminance_factor")
SPECTRAL_LUMINANCE_FACTOR = Dimensionless("spectral_luminance_factor")
REFLECTANCE_FACTOR = Dimensionless("reflectance_factor")
"""See: https://en.wikipedia.org/wiki/Reflectance"""
# NOTE: not defining luminous and photon quantities for linear attentuation|absorption for brevity.
PROPAGATION_LENGTH = QtyKind(M, ("propagation_length",))
PROPAGATION_LENGTH_ABSORBING_AND_SCATTERING = PROPAGATION_LENGTH[
    "absorbing", "scattering"
]
"""Propagation length of a collimated beam at a point in an absorbing and
scattering medium."""
LINEAR_ATTENUATION_COEFFICIENT = QtyKind(M**-1, ("linear_attenuation",))
PROPAGATION_LENGTH_ABSORBING = PROPAGATION_LENGTH["absorbing"]
"""Propagation length of a collimated beam at a point in an absorbing medium."""
LINEAR_ABSORPTION_COEFFICIENT = QtyKind(M**-1, ("linear_absorption",))
MASS_ATTENUATION_COEFFICIENT = QtyKind(KG**-1 * M**2, ("mass_attenuation",))
MASS_ABSORPTION_COEFFICIENT = QtyKind(KG**-1 * M**2, ("mass_absorption",))
MOLAR_ABSORPTION_COEFFICIENT = QtyKind(M**2 * MOL**-1, ("molar_absorption",))

#
# acoustics [ISO 80000-9]
#
OCTAVE = Log(_RATIO, base=2).alias("octave")
DECADE = Log(_RATIO, base=10).alias("decade")
SPEED_OF_SOUND = SPEED["sound"]
"""See: https://en.wikipedia.org/wiki/Speed_of_sound"""
SOUND_PRESSURE = QtyKind(PA, ("sound",))
"""Local [pressure][isqx.PRESSURE] deviation from the ambient atmospheric
pressure, caused by a sound wave."""
SOUND_PRESSURE_RMS = SOUND_PRESSURE["rms"]
SOUND_PARTICLE_DISPLACEMENT = QtyKind(M, ("sound_particle", VECTOR))
"""Instantaneous [displacement][isqx.DISPLACEMENT] of a particle from its
equilibrium [position][isqx.POSITION] in a medium as it transmits a sound
wave."""
SOUND_PARTICLE_VELOCITY = QtyKind(M_PERS, ("sound_particle", VECTOR))
SOUND_PARTICLE_ACCELERATION = QtyKind(M_PERS2, ("sound_particle", VECTOR))
SOUND_VOLUME_FLOW_RATE = VOLUME_FLOW_RATE["sound"]
SOUND_ENERGY_DENSITY = ENERGY_DENSITY["sound"]
SOUND_ENERGY = ENERGY["sound"]
SOUND_POWER = POWER["sound"]
SOUND_POWER_TIME_AVERAGED = SOUND_POWER["time_averaged"]
SOUND_INTENSITY = QtyKind(W * M**-2, ("sound", VECTOR))
SOUND_EXPOSURE = QtyKind(PA**2 * S, ("sound",))
CHARACTERISTIC_IMPEDANCE_LONGITUDINAL = QtyKind(
    PA * S * M**-1, ("characteristic",)
)
ACOUSTIC_IMPEDANCE = QtyKind(PA * S * M**-3, ("acoustic", COMPLEX))
# TODO: time weightings in IEC 61672-1 for exposure, SPL, PWL
PA_SOUND_RMS = SOUND_PRESSURE_RMS(PA)
DB_SPL_AIR = (
    20 * Log(ratio(PA_SOUND_RMS, Quantity(20, MICRO * PA)), base=10)
).alias("dB_spl_air")
"""Sound pressure level in air and other gases."""
DB_SPL_WATER = (
    20 * Log(ratio(PA_SOUND_RMS, Quantity(1, MICRO * PA)), base=10)
).alias("dB_spl_water")
"""Sound pressure level in water and other liquids."""
DB_PWL = (
    10
    * Log(ratio(SOUND_POWER_TIME_AVERAGED(W), Quantity(1, PICO * W)), base=10)
).alias("dB_pwl")
"""Sound power level."""
PA2_PERS_SOUND = SOUND_EXPOSURE(PA**2 * S)
DB_SEL_AIR = (
    10
    * Log(ratio(PA2_PERS_SOUND, Quantity(400, (MICRO * PA) ** 2 * S)), base=10)
).alias("dB_sel_air")
"""Sound exposure level in air and other gases."""
DB_SEL_WATER = (
    10 * Log(ratio(PA2_PERS_SOUND, Quantity(1, (MICRO * PA) ** 2 * S)), base=10)
).alias("dB_sel_water")
"""Sound exposure level in water and other liquids."""
REVERBERATION_TIME = DURATION["reverberation"]
"""[Time][isqx.TIME] after which the
[sound energy density][isqx.SOUND_ENERGY_DENSITY] has fallen to a certain
fraction of the initial value after the sound source has stopped emitting."""

#
# physical chemistry and molecular physics [ISO 80000-9]
#

NUMBER_OF_ENTITIES = Dimensionless("number_of_entities")
"""Discrete quantity; number of entities of a given kind in a system."""
AMOUNT_OF_SUBSTANCE = QtyKind(MOL, ("amount_of_substance",))
"""Extensive physical property."""
INITIAL_AMOUNT_OF_SUBSTANCE = AMOUNT_OF_SUBSTANCE["initial"]
FINAL_AMOUNT_OF_SUBSTANCE = AMOUNT_OF_SUBSTANCE["final"]
EQUILIBRIUM_AMOUNT_OF_SUBSTANCE = AMOUNT_OF_SUBSTANCE["equilibrium"]
RELATIVE_ATOMIC_MASS = Dimensionless("relative_atomic_mass")
RELATIVE_MOLECULAR_MASS = Dimensionless("relative_molecular_mass")
"""The particular molecule should be specified with [tags][isqx.Tagged]."""
MOLAR_MASS = QtyKind(KG * MOL**-1)
MOLAR_VOLUME = QtyKind(M**3 * MOL**-1, ("molar_volume",))
MOLAR_ENERGY = QtyKind(J * MOL**-1, ("molar_energy",))
MOLAR_INTERNAL_ENERGY = MOLAR_ENERGY["internal"]
MOLAR_ENTHALPY = MOLAR_ENERGY["enthalpy"]
MOLAR_HELMHOLTZ_ENERGY = MOLAR_ENERGY["helmholtz"]
MOLAR_GIBBS_ENERGY = MOLAR_ENERGY["gibbs"]
MOLAR_HEAT_CAPACITY = QtyKind(J * MOL**-1 * K**-1, ("heat_capacity",))
MOLAR_ENTROPY = QtyKind(J * MOL**-1 * K**-1, ("entropy",))
NUMBER_DENSITY = QtyKind(M**-3, ("number_density",))
MOLECULAR_CONCENTRATION = NUMBER_DENSITY["molecular"]
"""Number of molecules of a substance in a mixture per [volume][isqx.VOLUME]."""
# mass concentration and mass fraction defined in ISO 80000-5 above
MOLAR_CONCENTRATION = QtyKind(MOL * M**-3, ("concentration",))
"""Measure of the concentration of a solute in a solution, or of any chemical
species, in terms of [amount of substance][isqx.AMOUNT_OF_SUBSTANCE] in a given
[volume][isqx.VOLUME]; most commonly expressed in units of moles of solute per
litre of solution."""
STANDARD_MOLAR_CONCENTRATION: Annotated[int, MOL * L**-1] = 1
MOLE_FRACTION = Dimensionless("molar_fraction")
VOLUME_FRACTION = QtyKind(M**3 * M**-3, ("volume_fraction",))
# NOTE: we want to support VOLUME_FRACTION(MILLI * L * L**-1), but it errors
MOLALITY = QtyKind(MOL * KG**-1, ("molality",))
STANDARD_MOLALITY = MOLALITY["standard"]
"""The chosen value of molality, commonly 1 [mol][isqx.MOL] per [kg][isqx.KG]."""
LATENT_HEAT_OF_PHASE_TRANSITION = LATENT_HEAT["phase_transition"]
"""[Energy][isqx.ENERGY] to be added to or removed from a system under constant
[temperature][isqx.TEMPERATURE] and [pressure][isqx.PRESSURE] to undergo a
complete phase transition."""
CHEMICAL_POTENTIAL = QtyKind(J * MOL**-1, ("chemical_potential",))
ABSOLUTE_ACTIVITY = Dimensionless("absolute_activity")
FUGACITY = QtyKind(PA)
"""Measure of the tendency of a substance to leave a phase."""
STANDARD_CHEMICAL_POTENTIAL = CHEMICAL_POTENTIAL["standard"]
ACTIVITY_FACTOR = Dimensionless("activity_factor")
STANDARD_ABSOLUTE_ACTIVITY = ABSOLUTE_ACTIVITY["standard"]
"""For a substance in a mixture, the
[absolute activity][isqx.ABSOLUTE_ACTIVITY] of the pure substance at the same
[temperature][isqx.TEMPERATURE] but at standard pressure (10⁵ Pa)."""
ACTIVITY_OF_SOLUTE = Dimensionless("activity_of_solute")
ACTIVITY_COEFFICIENT = Dimensionless("activity_coefficient")
"""Value accounting for thermodynamic non-ideality of mixtures."""
STANDARD_ABSOLUTE_ACTIVITY_IN_SOLUTION = ABSOLUTE_ACTIVITY[
    "standard", "solution"
]
"""Property of a solute in a solution."""  # in terms of concentration ratio?
ACTIVITY_OF_SOLVENT = Dimensionless("activity_of_solvent")
OSMOTIC_COEFFICIENT_OF_SOLVENT = Dimensionless("osmotic_factor_of_solvent")
"""Quantity characterizing the deviation of a solvent from ideal behavior."""
STANDARD_ABSOLUTE_ACTIVITY_OF_SOLVENT = ABSOLUTE_ACTIVITY[
    "standard", "of_solvent"
]
OSMOTIC_PRESSURE = PRESSURE["osmotic"]
"""Measure of the tendency of a solution to take in pure solvent by osmosis."""
STOICHIOMETRIC_NUMBER = Dimensionless("stoichiometric_number")
"""In the expression of a chemical reaction, number which is positive for
products and negative for reactants."""
STOICHIOMETRIC_NUMBER_SUM = STOICHIOMETRIC_NUMBER["sum"]
AFFINITY_OF_CHEMICAL_REACTION = QtyKind(J * MOL**-1, ("affinity",))
"""Used to describe or characterise elements' or compounds' readiness to form
bonds."""
EXTENT_OF_REACTION = QtyKind(MOL, ("extent_of_reaction",))
STANDARD_EQUILIBRIUM_CONSTANT = Dimensionless("standard_equilibrium_constant")


def equilibrium_constant_pressure_basis(
    sum_stoichiometric_numbers: Annotated[Exponent, STOICHIOMETRIC_NUMBER_SUM],
) -> QtyKind:
    r""":param sum_stoichiometric_numbers: $\sum_\text{B} \nu_\text{B}$"""
    return QtyKind(PA**sum_stoichiometric_numbers, ("equilibrium_constant",))


def equilibrium_constant_concentration_basis(
    sum_stoichiometric_numbers: Annotated[Exponent, STOICHIOMETRIC_NUMBER_SUM],
) -> QtyKind:
    r""":param sum_stoichiometric_numbers: $\sum_\text{B} \nu_\text{B}$"""
    return QtyKind(
        (MOL * M**-3) ** sum_stoichiometric_numbers, ("equilibrium_constant",)
    )


MICROCANONICAL_PARTITION_FUNCTION = Dimensionless(
    "microcanonical_partition_function"
)
CANONICAL_PARTITION_FUNCTION = Dimensionless("canonical_partition_function")
GRAND_CANONICAL_PARTITION_FUNCTION = Dimensionless(
    "grand_canonical_partition_function"
)
MOLECULAR_PARTITION_FUNCTION = Dimensionless("molecular_partition_function")
STATISTICAL_WEIGHT_OF_SUBSYSTEM = Dimensionless(
    "statistical_weight_of_subsystem"
)
"""Number of microstates of a subsystem."""
MULTIPLICITY = STATISTICAL_WEIGHT_OF_SUBSYSTEM["multiplicity"]
"""Statistical weight of a quantum level."""
MOLAR_GAS_CONSTANT = QtyKind(J * MOL**-1 * K**-1, ("molar_gas_constant",))
"""Physical constant; the molar equivalent to the
[Boltzmann constant][isqx.CONST_BOLTZMANN]."""
# specific gas constant defined in ISO 80000-5
MEAN_FREE_PATH = DISTANCE["mean_free_path"]
"""Average [distance][isqx.DISTANCE] travelled by a moving particle between
successive impacts."""
DIFFUSION_COEFFICIENT = QtyKind(M**2 * S**-1, ("diffusion_coefficient",))
"""Proportionality constant in some physical laws."""
THERMAL_DIFFUSION_RATIO = Dimensionless("thermal_diffusion_ratio")
THERMAL_DIFFUSION_FACTOR = Dimensionless("thermal_diffusion_factor")
THERMAL_DIFFUSION_COEFFICIENT = QtyKind(
    M**2 * S**-1, ("thermal_diffusion_coefficient",)
)
IONIC_STRENGTH = QtyKind(MOL * KG**-1, ("ionic_strength",))
"""Quantification of the electrical interactions between ions in solution."""
DEGREE_OF_DISSOCIATION = Dimensionless("degree_of_dissociation")
"""Portion of dissociated molecules."""
ELECTROLYTIC_CONDUCTIVITY = CONDUCTIVITY["electrolytic", TENSOR_SECOND_ORDER]
"""Measure of the ability of a solution containing electrolytes to conduct
electricity."""
MOLAR_CONDUCTIVITY = QtyKind(SIEMENS * M**2 * MOL**-1)
TRANSPORT_NUMBER_OF_ION = Dimensionless("transport_number_of_ion")
ANGLE_OF_OPTICAL_ROTATION = ANGLE["optical_rotation"]
AREA_CROSS_SECTION_LINEARLY_POLARIZED = CROSS_SECTIONAL_AREA[
    "linearly_polarized"
]
MOLAR_OPTICAL_ROTATORY_POWER = QtyKind(RAD * M**2 * MOL**-1)
SPECIFIC_OPTICAL_ROTATORY_POWER = QtyKind(RAD * M**2 * KG**-1)
"""Optical property of chiral chemical compounds."""

#
# atomic and nuclear physics [ISO 80000-10]
#

ATOMIC_NUMBER = Dimensionless("atomic_number")
"""Number of protons found in the nucleus of an atom."""
NEUTRON_NUMBER = Dimensionless("neutron_number")
"""Number of neutrons in a nuclide."""
NUCLEON_NUMBER = Dimensionless("nucleon_number")
"""Number of heavy particles in the atomic nucleus."""
REST_MASS = MASS["rest"]
"""[Mass][isqx.MASS] of a particle at rest in an intertial frame."""
REST_ENERGY = ENERGY["rest"]
ATOMIC_MASS = MASS["atomic"]
"""[Rest mass][isqx.REST_MASS] of an atom in its ground state."""
NUCLIDIC_MASS = MASS["nuclidic"]
"""[Mass][isqx.MASS] of a nuclide in its ground state."""
UNIFIED_ATOMIC_MASS_CONSTANT = MASS["unified_atomic_mass_constant"]
"""A twelfth of the [mass][isqx.MASS] of a carbon-12 atom in its ground state."""
CHARGE_NUMBER = Dimensionless("charge_number")
BOHR_RADIUS = LENGTH["bohr_radius"]
"""Physical constant; the most probable [distance][isqx.DISTANCE] between an
electron and the nucleus in a nonrelativistic model of the hydrogen atom with
infinitely heavy nucleus."""
RYDBERG_CONSTANT = QtyKind(M**-1, ("rydberg_constant",))
HARTREE_ENERGY = ENERGY["hartree"]
"""Atomic unit of [energy][isqx.ENERGY]."""
ATOMIC_MAGNETIC_DIPOLE_MOMENT = MAGNETIC_MOMENT["atomic"]
BOHR_MAGNETON = QtyKind(A * M**2, ("bohr_magneton",))
"""Unit of [magnetic moment][isqx.MAGNETIC_MOMENT] (approx. 9.2 J/T); the
[magnetic dipole moment][isqx.ATOMIC_MAGNETIC_DIPOLE_MOMENT] of an electron
orbiting an atom with [angular momentum][isqx.ANGULAR_MOMENTUM] ℏ in the Bohr
model."""
NUCLEAR_MAGNETON = QtyKind(A * M**2, ("nuclear_magneton",))
"""Physical constant of [magnetic moment][isqx.MAGNETIC_MOMENT]."""
SPIN = QtyKind(J * S, ("spin", VECTOR))
"""Intrinsic form of [angular momentum][isqx.ANGULAR_MOMENTUM] as a property of
quantum particles."""
TOTAL_ANGULAR_MOMENTUM = ANGULAR_MOMENTUM["total"]
GYROMAGNETIC_RATIO = QtyKind(A * M**2 * (J * S) ** -1, ("gyromagnetic_ratio",))
ELECTRON_GYROMAGNETIC_RATIO = GYROMAGNETIC_RATIO["electron"]
QUANTUM_NUMBER = Dimensionless("quantum_number")
"""Notation for conserved quantities in physics and chemistry."""
PRINCIPAL_QUANTUM_NUMBER = QUANTUM_NUMBER["principal"]
"""One of four quantum numbers which are assigned to each electron in an atom to
describe that electron's state."""
ORBITAL_ANGULAR_MOMENTUM_QUANTUM_NUMBER = QUANTUM_NUMBER[
    "orbital_angular_momentum"
]
"""Quantum number for an atomic orbital that determines its orbital
[angular momentum][isqx.ANGULAR_MOMENTUM] and describes the shape of the orbital,
and is symbolized as ℓ."""
MAGNETIC_QUANTUM_NUMBER = QUANTUM_NUMBER["magnetic"]
"""Third in a set of four quantum numbers that distinguishes the orbitals
available within a subshell and can be used to calculate the azimuthal
component of the orientation of orbital in space."""
SPIN_QUANTUM_NUMBER = QUANTUM_NUMBER["spin"]
TOTAL_ANGULAR_MOMENTUM_QUANTUM_NUMBER = QUANTUM_NUMBER["total_angular_momentum"]
"""Quantum number describing the
[total angular momentum][isqx.TOTAL_ANGULAR_MOMENTUM] of an atom."""
NUCLEAR_SPIN_QUANTUM_NUMBER = QUANTUM_NUMBER["nuclear_spin"]
HYPERFINE_STRUCTURE_QUANTUM_NUMBER = QUANTUM_NUMBER["hyperfine_structure"]
LANDE_FACTOR = Dimensionless("lande_factor")
"""g-factor for electron with [spin][isqx.SPIN] and orbital
[angular momentum][isqx.ANGULAR_MOMENTUM]."""
G_FACTOR_NUCLEUS = Dimensionless("g_factor_nucleus")
LARMOR_ANGULAR_FREQUENCY = ANGULAR_FREQUENCY["larmor"]
LARMOR_FREQUENCY = QtyKind(S**-1, ("larmor_frequency",))
LARMOR_PRECESSION_ANGULAR_FREQUENCY = ANGULAR_FREQUENCY["larmor_precession"]
CYCLOTRON_ANGULAR_FREQUENCY = ANGULAR_FREQUENCY["cyclotron"]
"""Angular [frequency][isqx.FREQUENCY] of a charged particle moving on a circular
path perpendicular to a uniform magnetic field."""
GYRORADIUS = RADIUS["gyroradius"]
"""[Radius][isqx.RADIUS] of the circular movement of an electrically charged
particle in a magnetic field."""
NUCLEAR_QUADRUPOLE_MOMENT = QtyKind(M**2, ("nuclear_quadrupole_moment",))
"""Measure for the deviation of the nuclear [charge density][isqx.CHARGE_DENSITY]
from spherical symmetry."""
NUCLEAR_RADIUS = RADIUS["nuclear"]
"""Measure of the size of atomic nuclei."""
ELECTRON_RADIUS = RADIUS["electron"]
"""Physical constant providing [length][isqx.LENGTH] scale to interatomic
interactions."""
COMPTON_WAVELENGTH = WAVELENGTH["compton"]
"""In quantum mechanics, the [wavelength][isqx.WAVELENGTH] of a photon whose
[energy][isqx.ENERGY] is the same as the [rest energy][isqx.REST_ENERGY] of a
particle."""
MASS_EXCESS = MASS["excess"]
MASS_DEFECT = MASS["defect"]
"""Equivalent [mass][isqx.MASS] of the binding energy of an atomic nucleus."""
RELATIVE_MASS_EXCESS = Dimensionless("relative_mass_excess")
RELATIVE_MASS_DEFECT = Dimensionless("relative_mass_defect")
PACKING_FRACTION = Dimensionless("packing_fraction")
BINDING_FRACTION = Dimensionless("binding_fraction")
DECAY_CONSTANT = QtyKind(S**-1, ("decay_constant",))
MEAN_LIFE_TIME = DURATION["mean_life_time"]
LEVEL_WIDTH = ENERGY["level_width"]
ACTIVITY = QtyKind(BQ, ("activity",))
"""Physical quantity in nuclear physics, measured in becquerel, revealing the
average number of nucleuses experiencing a spontaneous reaction per second."""
SPECIFIC_ACTIVITY = QtyKind(BQ * KG**-1, ("specific_activity",))
ACTIVITY_DENSITY = QtyKind(BQ * M**-3, ("activity_density",))
SURFACE_ACTIVITY_DENSITY = QtyKind(BQ * M**-2, ("surface_activity_density",))
HALF_LIFE = DURATION["half_life"]
"""In nuclear physics, mean [duration][isqx.DURATION] after which half of the
atomic nuclei has decayed."""
ALPHA_DISINTEGRATION_ENERGY = ENERGY["alpha_disintegration"]
MAXIMUM_BETA_PARTICLE_ENERGY = ENERGY["max_beta_particle"]
BETA_DISINTEGRATION_ENERGY = ENERGY["beta_disintegration"]
INTERNAL_CONVERSION_FACTOR = Dimensionless("internal_conversion_factor")
"""Ratio of electron to gamma ray emissions."""
PARTICLE_EMISSION_RATE = QtyKind(S**-1, ("particle_emission_rate",))
REACTION_ENERGY = ENERGY["reaction"]
"""In a nuclear reaction, sum of kinetic and photon energies of the products
minus the energies of the reactants."""
RESONANCE_ENERGY = ENERGY["resonance"]
"""Resonance in a nuclear reaction, determined by the kinetic
[energy][isqx.ENERGY] of an incident particle in the reference frame of the
target particle."""
CROSS_SECTION = AREA["cross_section_atomic"]
"""Measure of probability that a specific process will take place in a
collision of two particles."""
TOTAL_CROSS_SECTION = CROSS_SECTION["total"]
DIRECTION_DISTRIBUTION_OF_CROSS_SECTION = QtyKind(
    M**2 * SR**-1, ("direction_distribution_of_cross_section",)
)
ENERGY_DISTRIBUTION_OF_CROSS_SECTION = QtyKind(
    M**2 * J**-1, ("energy_distribution_of_cross_section",)
)
DIRECTION_AND_ENERGY_DISTRIBUTION_OF_CROSS_SECTION = QtyKind(
    M**2 * J**-1 * SR**-1,
    ("direction_and_energy_distribution_of_cross_section",),
)
VOLUMIC_CROSS_SECTION = QtyKind(M**-1, ("volumic_cross_section",))
VOLUMIC_TOTAL_CROSS_SECTION = QtyKind(M**-1, ("volumic_total_cross_section",))
PARTICLE_FLUENCE = QtyKind(M**-2, ("particle_fluence",))
PARTICLE_FLUENCE_RATE = QtyKind(M**-2 * S**-1, ("particle_fluence_rate",))
IONIZING_RADIANT_ENERGY = ENERGY["radiant_ionizing"]
"""In nuclear physics, mean [energy][isqx.ENERGY] of emitted, transferred or
received particles."""
ENERGY_FLUENCE = QtyKind(J * M**-2, ("energy_fluence",))
ENERGY_FLUENCE_RATE = QtyKind(W * M**-2, ("energy_fluence_rate",))
PARTICLE_CURRENT_DENSITY = QtyKind(M**-2 * S**-1, ("particle_current_density",))
IONIZING_LINEAR_ATTENUATION_COEFFICIENT = QtyKind(
    M**-1, ("linear_attenuation_ionizing",)
)
IONIZING_MASS_ATTENUATION_COEFFICIENT = QtyKind(
    KG**-1 * M**2, ("mass_attenuation_ionizing",)
)
MOLAR_ATTENUATION_COEFFICIENT = QtyKind(
    M**2 * MOL**-1, ("molar_attenuation_coefficient",)
)
ATOMIC_ATTENUATION_COEFFICIENT = QtyKind(
    M**2, ("atomic_attenuation_coefficient",)
)
HALF_VALUE_THICKNESS = THICKNESS["half_value"]
"""[Thickness][isqx.THICKNESS] of an attenuating layer which reduces the value of
a quantity to half of its initial value."""
TOTAL_LINEAR_STOPPING_POWER = QtyKind(
    J * M**-1, ("total_linear_stopping_power",)
)
TOTAL_MASS_STOPPING_POWER = QtyKind(
    J * M**2 * KG**-1, ("total_mass_stopping_power",)
)
MEAN_LINEAR_RANGE = LENGTH["mean_linear_range"]
"""Mean path [length][isqx.LENGTH] traveled by particles of a given initial
[energy][isqx.ENERGY] slowing down to rest in a given material."""
MEAN_MASS_RANGE = QtyKind(KG * M**-2, ("mean_mass_range",))
LINEAR_IONIZATION = QtyKind(M**-1, ("linear_ionization",))
"""Mean number of elementary charges per path [length][isqx.LENGTH] of all ions
produced by an ionizing, charged particle."""
TOTAL_IONIZATION = Dimensionless("total_ionization")
"""Mean number of elementary charges of all ions produced by an ionizing,
charged particle along its entire path."""
AVERAGE_ENERGY_LOSS_PER_ELEMENTARY_CHARGE_PRODUCED = ENERGY[
    "average_energy_loss_per_elementary_charge_produced"
]
MOBILITY = QtyKind(M**2 * V**-1 * S**-1, ("mobility",))
PARTICLE_NUMBER_DENSITY = NUMBER_DENSITY["particle"]
ION_NUMBER_DENSITY = NUMBER_DENSITY["ion"]
"""Number of ions per [volume][isqx.VOLUME]."""
RECOMBINATION_COEFFICIENT = QtyKind(
    M**3 * S**-1, ("recombination_coefficient",)
)
"""Measure for the recombination rate of ions."""
DIFFUSION_COEFFICIENT_PARTICLE_NUMBER_DENSITY = QtyKind(
    M**2 * S**-1, ("diffusion_coefficient_particle_number_density",)
)
DIFFUSION_COEFFICIENT_FLUENCE_RATE = QtyKind(
    M, ("diffusion_coefficient_fluence_rate",)
)
PARTICLE_SOURCE_DENSITY = QtyKind(M**-3 * S**-1, ("particle_source_density",))
SLOWING_DOWN_DENSITY = QtyKind(M**-3 * S**-1, ("slowing_down_density",))
RESONANCE_ESCAPE_PROBABILITY = Dimensionless("resonance_escape_probability")
"""Probability that a high-energy neutron is not captured."""
LETHARGY = Dimensionless("lethargy")
"""Natural logarithm of the quotient of a reference [energy][isqx.ENERGY] and the
kinetic energy of a neutron."""
AVERAGE_LOGARITHMIC_ENERGY_DECREMENT = Dimensionless(
    "average_logarithmic_energy_decrement"
)
"""Average increase in [lethargy][isqx.LETHARGY] per collision of neutrons with
atomic nuclei."""
MEAN_FREE_PATH_ATOMIC = MEAN_FREE_PATH["atomic"]
"""In nuclear physics, average [distance][isqx.DISTANCE] that particles travel
between two specified interactions."""
SLOWING_DOWN_AREA = AREA["slowing_down"]
"""One sixth of the mean squared [distance][isqx.DISTANCE] between a neutron
source and the point at which the neutron reaches a given [energy][isqx.ENERGY]."""
DIFFUSION_AREA = AREA["diffusion"]
"""One sixth of the mean squared [distance][isqx.DISTANCE] where a neutron enters
an [energy][isqx.ENERGY] class and the point where it leaves this class."""
MIGRATION_AREA = AREA["migration"]
"""Sum of the [slowing-down area][isqx.SLOWING_DOWN_AREA] of neutrons from
fission to thermal [energy][isqx.ENERGY] and the
[diffusion area][isqx.DIFFUSION_AREA] of thermal neutrons."""
SLOWING_DOWN_LENGTH = LENGTH["slowing_down"]
DIFFUSION_LENGTH_ATOMIC = LENGTH["diffusion_atomic"]
MIGRATION_LENGTH = LENGTH["migration"]
NEUTRON_YIELD_PER_FISSION = Dimensionless("neutron_yield_per_fission")
"""Average number of fission neutrons emitted per fission event."""
NEUTRON_YIELD_PER_ABSORPTION = Dimensionless("neutron_yield_per_absorption")
"""Average number of fission neutrons emitted per absorbed neutron."""
FAST_FISSION_FACTOR = Dimensionless("fast_fission_factor")
THERMAL_UTILIZATION_FACTOR = Dimensionless("thermal_utilization_factor")
NON_LEAKAGE_PROBABILITY = Dimensionless("non_leakage_probability")
"""Probability, that a neutron won't escape a reactor while slowing down or
while diffusing as thermal neutron."""
MULTIPLICATION_FACTOR = Dimensionless("multiplication_factor")
INFINITE_MULTIPLICATION_FACTOR = Dimensionless("infinite_multiplication_factor")
"""In nuclear physics, the [multiplication factor][isqx.MULTIPLICATION_FACTOR]
for an infinite medium."""
REACTOR_TIME_CONSTANT = DURATION["reactor_time_constant"]
"""[Duration][isqx.DURATION], in which the neutron
[fluence rate][isqx.PARTICLE_FLUENCE_RATE] in a reactor changes by a factor e."""
ENERGY_IMPARTED = ENERGY["imparted"]
MEAN_ENERGY_IMPARTED = ENERGY["mean_imparted"]
"""In nuclear physics, expectation value of the
[energy imparted][isqx.ENERGY_IMPARTED]."""
ABSORBED_DOSE = QtyKind(GY, ("absorbed_dose",))
SPECIFIC_ENERGY_IMPARTED = QtyKind(GY, ("specific_energy_imparted",))
IONIZING_QUALITY_FACTOR = Dimensionless("quality_factor_ionizing")
"""Factor taking into account health effects in the determination of the
[dose equivalent][isqx.DOSE_EQUIVALENT]."""
DOSE_EQUIVALENT = QtyKind(SV, ("dose_equivalent",))
DOSE_EQUIVALENT_RATE = QtyKind(SV * S**-1, ("dose_equivalent_rate",))
ABSORBED_DOSE_RATE = QtyKind(GY * S**-1, ("absorbed_dose_rate",))
LINEAR_ENERGY_TRANSFER = QtyKind(J * M**-1, ("linear_energy_transfer",))
KERMA = QtyKind(GY, ("kerma",))
"""Kinetic [energy][isqx.ENERGY] released per [mass][isqx.MASS]."""
KERMA_RATE = QtyKind(GY * S**-1, ("kerma_rate",))
MASS_ENERGY_TRANSFER_COEFFICIENT = QtyKind(
    KG**-1 * M**2, ("mass_energy_transfer_coefficient",)
)
"""For ionizing uncharged particles, measure for the [energy][isqx.ENERGY]
transferred to charged particles in the form of kinetic energy."""
IONIZING_EXPOSURE = QtyKind(C * KG**-1, ("exposure_ionizing",))
"""Electric [charge][isqx.ELECTRIC_CHARGE] of ions produced in air by X- or gamma
radiation per [mass][isqx.MASS] of air, when all liberated electrons are
completely stopped."""
EXPOSURE_RATE = QtyKind(C * KG**-1 * S**-1, ("exposure_rate",))

#
# characteristic numbers [ISO 80000-11]
# see: https://en.wikipedia.org/wiki/List_of_dimensionless_quantities
# see: https://en.wikipedia.org/wiki/Dimensionless_physical_constant
# adapted from: https://en.wikipedia.org/wiki/Dimensionless_numbers_in_fluid_mechanics
#
# quantity kinds referenced in details
SHEAR_RATE = QtyKind(S**-1, ("shear_rate",))
VOLUME_FRACTION = QtyKind(M**3 * M**-3, ("volume_fraction",))
MEAN_BEARING_PRESSURE = PRESSURE["mean_bearing"]
BOUNDARY_LAYER_THICKNESS = THICKNESS["boundary_layer"]
PRESSURE_GRADIENT = QtyKind(PA * M**-1, ("pressure_gradient",))
VOLUMIC_HEAT_GENERATION_RATE = QtyKind(
    W * M**-3, ("volumic_heat_generation_rate",)
)
RELAXATION_TIME = DURATION["relaxation"]
OBSERVATION_DURATION = DURATION["observation"]
POROSITY = Dimensionless("porosity")
MASS_TRANSFER_COEFFICIENT = QtyKind(M * S**-1, ("mass_transfer_coefficient",))
AXIAL_SPEED = SPEED["axial"]
LIFT = FORCE["lift"]
THRUST = FORCE["thrust"]
VAPOUR_PRESSURE = PRESSURE["vapour"]
PRESSURE_DROP = PRESSURE[DELTA]
LATITUDE = ANGLE["latitude"]
LONGITUDE = ANGLE["longitude"]

# momentum transfer
REYNOLDS_NUMBER = Dimensionless("reynolds_number")
"""Dimensionless quantity that is used to help predict similar flow patterns in
different fluid flow situations."""
EULER_NUMBER = Dimensionless("euler_number")
"""Dimensionless caracteristic number used in fluid mechanics, defined as the
ratio of pressure forces and inertial forces used to characterize losses in a
moving fluid."""
FROUDE_NUMBER = Dimensionless("froude_number")
"""Dimensionless number defined as the ratio of the flow inertia to the
external field."""
GRASHOF_NUMBER = Dimensionless("grashof_number")
"""Characteristic number in fluid dynamics."""
WEBER_NUMBER = Dimensionless("weber_number")
"""Dimensionless number in fluid mechanics that is often useful in analysing
fluid flows where there is an interface between two different fluids."""
MACH_NUMBER = Dimensionless("mach_number")
KNUDSEN_NUMBER = Dimensionless("knudsen_number")
STROUHAL_NUMBER = Dimensionless("strouhal_number")
"""Dimensionless number describing oscillating flow mechanisms."""
# NOTE: DRAG_COEFFICIENT is defined in mechanics section
BAGNOLD_NUMBER = Dimensionless("bagnold_number")
"""For a body moving in a fluid the quotient of [drag][isqx.DRAG] and
gravitational [force][isqx.FORCE]."""
BAGNOLD_NUMBER_SOLID_PARTICLES = Dimensionless("bagnold_number_solid_particles")
LIFT_COEFFICIENT = Dimensionless("lift_coefficient")
"""Coefficient that relates the [lift][isqx.LIFT] generated by a lifting body to
other parameters."""
THRUST_COEFFICIENT = Dimensionless("thrust_coefficient")
"""Characteristic number of a propeller."""
DEAN_NUMBER = Dimensionless("dean_number")
"""Characteristic number of flows in curved pipes."""
BEJAN_NUMBER = Dimensionless("bejan_number")
"""Dimensionless [pressure drop][isqx.PRESSURE_DROP] along a channel."""
LAGRANGE_NUMBER = Dimensionless("lagrange_number")
"""Characteristic number for a fluid in a pipe."""
BINGHAM_NUMBER = Dimensionless("bingham_number")
HEDSTROM_NUMBER = Dimensionless("hedstrom_number")
BODENSTEIN_NUMBER = Dimensionless("bodenstein_number")
ROSSBY_NUMBER = Dimensionless("rossby_number")
"""Ratio of inertial [force][isqx.FORCE] to Coriolis force."""
EKMAN_NUMBER = Dimensionless("ekman_number")
"""Dimensionless ratio of viscous to Coriolis forces."""
ELASTICITY_NUMBER = Dimensionless("elasticity_number")
"""Characteristic number of viscoelastic flows."""
DARCY_FRICTION_FACTOR = Dimensionless("darcy_friction_factor")
"""Characteristic number for the [pressure drop][isqx.PRESSURE_DROP] in a pipe
due to friction in a laminar or turbulent flow."""
FANNING_NUMBER = Dimensionless("fanning_friction_factor")
"""Characteristic number for the friction on the wall of a fluid in a pipe."""
GOERTLER_NUMBER = Dimensionless("goertler_number")
HAGEN_NUMBER = Dimensionless("hagen_number")
"""Dimensionless number used in forced flow calculations."""
LAVAL_NUMBER = Dimensionless("laval_number")
POISEUILLE_NUMBER = Dimensionless("poiseuille_number")
"""Characteristic number of flows in a pipe."""
POWER_NUMBER = Dimensionless("power_number")
"""Characteristic number for the [power][isqx.POWER] of an agitator."""
RICHARDSON_NUMBER = Dimensionless("richardson_number")
"""Characteristic number of a falling body proportional to the quotient of
potential and kinetic [energy][isqx.ENERGY]."""
REECH_NUMBER = Dimensionless("reech_number")
"""Characteristic number of an object moving in water."""
BOUSSINESQ_NUMBER = Dimensionless("boussinesq_number")
"""See: <https://en.wikipedia.org/wiki/Boussinesq_approximation_(buoyancy)>"""
STOKES_NUMBER = Dimensionless("stokes_number")
"""Characteristic number for particles in a fluid or plasma."""
STOKES_NUMBER_VIBRATING_PARTICLES = Dimensionless(
    "stokes_number_vibrating_particles"
)
"""Characteristic number for particles vibrating in a fluid or plasma."""
STOKES_NUMBER_ROTAMETER = Dimensionless("stokes_number_rotameter")
"""Characteristic number for the calibration of rotameters."""
STOKES_NUMBER_GRAVITY = Dimensionless("stokes_number_gravity")
"""Characteristic number for particles falling in a fluid."""
STOKES_NUMBER_DRAG = Dimensionless("stokes_number_drag")
"""Characteristic number for particles dragged in a fluid."""
LAPLACE_NUMBER = Dimensionless("laplace_number")
"""Characteristic number in fluid dynamics."""
BLAKE_NUMBER = Dimensionless("blake_number")
"""Nondimensional number showing the ratio of inertial [force][isqx.FORCE] to
viscous force."""
SOMMERFELD_NUMBER = Dimensionless("sommerfeld_number")
"""Characteristic number of hydrodynamic bearings."""
TAYLOR_NUMBER = Dimensionless("taylor_number")
"""Characteristic number of a shaft rotating in a fluid."""
GALILEI_NUMBER = Dimensionless("galilei_number")
"""Characteristic number of fluid films flowing over walls."""
WOMERSLEY_NUMBER = Dimensionless("womersley_number")
"""Characteristic number of pulsating flows in a pipe."""

# heat transfer
FOURIER_NUMBER = Dimensionless("fourier_number")
PECLET_NUMBER = Dimensionless("peclet_number")
"""Dimensionless ratio used in fluid dynamics."""
RAYLEIGH_NUMBER = Dimensionless("rayleigh_number")
"""Characteristic number of [heat][isqx.HEAT] transport in fluids."""
FROUDE_NUMBER_HEAT_TRANSFER = Dimensionless("froude_number_heat_transfer")
NUSSELT_NUMBER = Dimensionless("nusselt_number")
BIOT_NUMBER = Dimensionless("biot_number")
"""Characteristic number for [heat][isqx.HEAT] transfer by conduction into a
body."""
STANTON_NUMBER = Dimensionless("stanton_number")
J_FACTOR_HEAT_TRANSFER = Dimensionless("j_factor_heat_transfer")
"""Characteristic number for the relation between [heat][isqx.HEAT] and
[mass][isqx.MASS] transfer in a fluid."""
BEJAN_NUMBER_HEAT_TRANSFER = Dimensionless("bejan_number_heat_transfer")
BEJAN_NUMBER_ENTROPY = Dimensionless("bejan_number_entropy")
"""In thermodynamics, the ratio of [heat][isqx.HEAT] transfer irreversibility to
total irreversibility."""
STEFAN_NUMBER = Dimensionless("stefan_number")
"""Characteristic number for the relation between [heat][isqx.HEAT] and
[latent heat][isqx.LATENT_HEAT] of a binary mixture undergoing a phase
transition."""
BRINKMAN_NUMBER = Dimensionless("brinkman_number")
"""Characteristic number of a fluid for the relation between [heat][isqx.HEAT]
produced by viscosity and heat received from outside by conduction."""
CLAUSIUS_NUMBER = Dimensionless("clausius_number")
"""Characteristic number of a fluid for the relation between
[energy][isqx.ENERGY] transfer by momentum and by thermal conduction."""
# CARNOT_NUMBER defined in ISO 80000-5 above
ECKERT_NUMBER = Dimensionless("eckert_number")
GRAETZ_NUMBER = Dimensionless("graetz_number")
HEAT_TRANSFER_NUMBER = Dimensionless("heat_transfer_number")
POMERANTSEV_NUMBER = Dimensionless("pomerantsev_number")
"""Characteristic number for the relation between [heat][isqx.HEAT] generation
and conduction in a body."""
BOLTZMANN_NUMBER = Dimensionless("boltzmann_number")
"""Characteristic number for the relation between convective [heat][isqx.HEAT] and
radiant heat of a fluid."""
STARK_NUMBER = Dimensionless("stark_number")
"""Characteristic number for the relation between radiant and conductive
[heat][isqx.HEAT] of a body."""

# mass transfer
FOURIER_NUMBER_MASS_TRANSFER = Dimensionless("fourier_number_mass_transfer")
PECLET_NUMBER_MASS_TRANSFER = Dimensionless("peclet_number_mass_transfer")
GRASHOF_NUMBER_MASS_TRANSFER = Dimensionless("grashof_number_mass_transfer")
"""Characteristic number for the relation between buoyancy and viscosity in
convection of fluids."""
NUSSELT_NUMBER_MASS_TRANSFER = Dimensionless("nusselt_number_mass_transfer")
"""Characteristic number for [mass][isqx.MASS] transfer at the boundary of a
fluid."""
STANTON_NUMBER_MASS_TRANSFER = Dimensionless("stanton_number_mass_transfer")
GRAETZ_NUMBER_MASS_TRANSFER = Dimensionless("graetz_number_mass_transfer")
J_FACTOR_MASS_TRANSFER = Dimensionless("j_factor_mass_transfer")
"""Characteristic number for the relation between [mass][isqx.MASS] transport
perpendicular and parallel to the surface of an open fluid flow."""
ATWOOD_NUMBER = Dimensionless("atwood_number")
BIOT_NUMBER_MASS_TRANSFER = Dimensionless("biot_number_mass_transfer")
"""Characteristic number for the relation between [mass][isqx.MASS] transfer rate
at the interface and in the interior of a body."""
MORTON_NUMBER = Dimensionless("morton_number")
"""Characteristic number for bubbles or drops in a liquid or gas, respectively,
under the influence of gravitational an viscous forces."""
BOND_NUMBER = Dimensionless("bond_number")
"""Characteristic number in fluid dynamics."""
ARCHIMEDES_NUMBER = Dimensionless("archimedes_number")
"""Used to determine the motion of fluids due to [density][isqx.DENSITY]
differences."""
EXPANSION_NUMBER = Dimensionless("expansion_number")
"""Characteristic number for the relation of buoyancy and internal
[force][isqx.FORCE] for gas bubbles rising in a liquid."""
MARANGONI_NUMBER = Dimensionless("marangoni_number")
"""Concept in fluid dynamics."""
LOCKHART_MARTINELLI_PARAMETER = Dimensionless("lockhart_martinelli_parameter")
"""Characteristic number used in two-phase flow calculations."""
BEJAN_NUMBER_MASS_TRANSFER = Dimensionless("bejan_number_mass_transfer")
"""Characteristic number for viscous flows in pipes."""
CAVITATION_NUMBER = Dimensionless("cavitation_number")
"""Concept in fluid mechanics."""
ABSORPTION_NUMBER = Dimensionless("absorption_number")
"""Characteristic number for the absorption of gas at a wet surface."""
CAPILLARY_NUMBER = Dimensionless("capillary_number")
"""Quotient of gravitational and capillary forces for fluids in narrow pipes."""
DYNAMIC_CAPILLARY_NUMBER = Dimensionless("dynamic_capillary_number")
"""Ratio of viscous drag forces to [surface tension][isqx.SURFACE_TENSION] in
fluids."""

# other transport phenomena
PRANDTL_NUMBER = Dimensionless("prandtl_number")
SCHMIDT_NUMBER = Dimensionless("schmidt_number")
LEWIS_NUMBER = Dimensionless("lewis_number")
OHNESORGE_NUMBER = Dimensionless("ohnesorge_number")
"""Characteristic number that relates the viscous forces to inertial and
[surface tension][isqx.SURFACE_TENSION] forces."""
CAUCHY_NUMBER = Dimensionless("cauchy_number")
"""Characteristic number in continuum mechanics used in the study of
compressible flows."""
HOOKE_NUMBER = Dimensionless("hooke_number")
"""Characteristic number for elastic fluids."""
WEISSENBERG_NUMBER = Dimensionless("weissenberg_number")
DEBORAH_NUMBER = Dimensionless("deborah_number")
LORENTZ_NUMBER = Dimensionless("lorentz_number")
COMPRESSIBILITY_NUMBER = Dimensionless("compressibility_number")
"""Correction factor which describes the deviation of a real gas from ideal gas
behavior."""

# magnetohydrodynamics
REYNOLDS_MAGNETIC_NUMBER = Dimensionless("reynolds_magnetic_number")
"""Characteristic number of an electrically conducting fluid."""
BATCHELOR_NUMBER = Dimensionless("batchelor_number")
"""Characteristic number of an electrically conducting liquid."""
NUSSELT_ELECTRIC_NUMBER = Dimensionless("nusselt_electric_number")
"""Characteristic number for the relation between convective and diffusive ion
[current][isqx.CURRENT]."""
ALFVEN_NUMBER = Dimensionless("alfven_number")
"""Characteristic number for the relation between plasma [speed][isqx.SPEED] and
Alfvén wave speed."""
HARTMANN_NUMBER = Dimensionless("hartmann_number")
"""Characteristic number for electrically conducting fluids."""
COWLING_NUMBER = Dimensionless("cowling_number")
"""Characteristic number for the relation of magnetic to kinematic
[energy][isqx.ENERGY] in a plasma."""
STUART_ELECTRICAL_NUMBER = Dimensionless("stuart_electrical_number")
"""Characteristic number for the relation of electric to kinematic
[energy][isqx.ENERGY] in a plasma."""
MAGNETIC_PRESSURE_NUMBER = Dimensionless("magnetic_pressure_number")
"""Quotient of gas and magnetic [pressure][isqx.PRESSURE] in a gas or plasma."""
CHANDRASEKHAR_NUMBER = Dimensionless("chandrasekhar_number")
"""Dimensionless quantity used in magnetic convection to represent ratio of the
Lorentz [force][isqx.FORCE] to the viscosity."""
PRANDTL_MAGNETIC_NUMBER = Dimensionless("prandtl_magnetic_number")
ROBERTS_NUMBER = Dimensionless("roberts_number")
STUART_NUMBER = Dimensionless("stuart_number")
"""Quotient of magnetic and inertial [force][isqx.FORCE] in an electrically
conducting fluid."""
MAGNETIC_NUMBER = Dimensionless("magnetic_number")
"""Quotient of magnetic and viscous forces in an electrically conducting
fluid."""
ELECTRIC_FIELD_PARAMETER = Dimensionless("electric_field_parameter")
"""Quotient of Coulomb and Lorentz [force][isqx.FORCE] on moving, electrically
charged particles."""
HALL_NUMBER = Dimensionless("hall_number")
"""Quotient of gyro and collision [frequency][isqx.FREQUENCY] in a plasma."""
LUNDQUIST_NUMBER = Dimensionless("lundquist_number")
"""Quotient of Alfvén and magneto-dynamic [speed][isqx.SPEED] in a plasma."""
JOULE_MAGNETIC_NUMBER = Dimensionless("joule_magnetic_number")
"""Quotient of Joule [heat][isqx.HEAT] and magnetic field [energy][isqx.ENERGY] in
a plasma."""
GRASHOF_MAGNETIC_NUMBER = Dimensionless("grashof_magnetic_number")
"""Characteristic number for the [heat][isqx.HEAT] transfer by thermo-magnetic
convection of a paramagnetic fluid under the influence of gravity."""
NAZE_NUMBER = Dimensionless("naze_number")
"""Quotient of Alfvén wave [speed][isqx.SPEED] and
[sound speed][isqx.SPEED_OF_SOUND] in a plasma."""
REYNOLDS_ELECTRIC_NUMBER = Dimensionless("reynolds_electric_number")
"""Quotient of the [speed][isqx.SPEED] of an electrically conducting fluid and
drift speed of its charged particles."""
AMPERE_NUMBER = Dimensionless("ampere_number")
"""Characteristic number for the relation between electric surface
[current][isqx.CURRENT] and [magnetic field strength][isqx.MAGNETIC_FIELD_STRENGTH]
in an electrically conducting liquid."""

# chemical reactions
ARRHENIUS_NUMBER = Dimensionless("arrhenius_number")
LANDAU_GINZBURG_NUMBER = Dimensionless("landau_ginzburg_number")
"""Characteristic number of a superconductor."""

#
# condensed matter physics [ISO 80000-12]
#

LATTICE_VIBRATION_FREQUENCY = QtyKind(HZ, ("lattice_vibration",))
NUMBER_OF_ONE_ELECTRON_STATES_PER_VOLUME = QtyKind(
    M**-3, ("one_electron_states",)
)
MOBILITY_OF_ELECTRONS = MOBILITY["electron"]
MOBILITY_OF_HOLES = MOBILITY["hole"]
LIFETIME = DURATION["lifetime"]

LATTICE_VECTOR = QtyKind(M, ("lattice", VECTOR))
"""Translation vector which maps a crystal lattice onto itself."""
FUNDAMENTAL_LATTICE_VECTORS = LATTICE_VECTOR["fundamental"]
"""Fundamental translation vector for a crystal lattice."""
ANGULAR_RECIPROCAL_LATTICE_VECTOR = QtyKind(
    M**-1, ("reciprocal_lattice", VECTOR, "angular")
)
"""Vector whose scalar product with a
[fundamental lattice vector][isqx.FUNDAMENTAL_LATTICE_VECTORS] is an integral
multiple of two Pi."""
FUNDAMENTAL_RECIPROCAL_LATTICE_VECTORS = ANGULAR_RECIPROCAL_LATTICE_VECTOR[
    "fundamental"
]
"""Fundamental translation vector for a reciprocal lattice."""
LATTICE_PLANE_SPACING = QtyKind(M, ("lattice_plane_spacing",))
"""[Distance][isqx.DISTANCE] between adjacent lattice planes."""
BRAGG_ANGLE = ANGLE["bragg"]
"""In X-ray crystallography, [angle][isqx.ANGLE] between lattice plane and
scattered ray."""
SHORT_RANGE_ORDER_PARAMETER = Dimensionless("short_range_order_parameter")
LONG_RANGE_ORDER_PARAMETER = Dimensionless("long_range_order_parameter")
ATOMIC_SCATTERING_FACTOR = Dimensionless("atomic_scattering_factor")
"""Measure of the scattering amplitude of a wave by an isolated atom."""
STRUCTURE_FACTOR = Dimensionless("structure_factor")
"""Mathematical description in crystallography."""
BURGERS_VECTOR = QtyKind(M, ("burgers", VECTOR))
"""Vector characterising a dislocation in a crystal lattice."""
PARTICLE_POSITION_VECTOR = POSITION["particle"]
"""[Position][isqx.POSITION] vector of a particle."""
EQUILIBRIUM_POSITION_VECTOR = POSITION["equilibrium"]
"""In condensed matter physics, [position][isqx.POSITION] vector of an atom or
ion in equilibrium."""
DISPLACEMENT_VECTOR_LATTICE = DISPLACEMENT["lattice"]
"""In condensed matter physics, [position][isqx.POSITION] vector of an atom or
ion relative to its equilibrium position."""
DEBYE_WALLER_FACTOR = Dimensionless("debye_waller_factor")
"""Is used in condensed matter physics to describe the attenuation of x-ray
scattering or coherent neutron scattering caused by thermal motion."""
ANGULAR_WAVENUMBER_LATTICE = ANGULAR_WAVENUMBER["lattice"]
FERMI_ANGULAR_WAVENUMBER = ANGULAR_WAVENUMBER_LATTICE["fermi"]
"""Angular [wavenumber][isqx.WAVENUMBER] of an electron in a state on the Fermi
surface."""
DEBYE_ANGULAR_WAVENUMBER = ANGULAR_WAVENUMBER_LATTICE["debye"]
DEBYE_ANGULAR_FREQUENCY = ANGULAR_FREQUENCY["debye"]
DEBYE_TEMPERATURE = QtyKind(K, ("debye",))
DENSITY_OF_VIBRATIONAL_STATES = QtyKind(
    S * M**-3, ("density_of_vibrational_states",)
)
"""Quantity in condensed matter physics."""
THERMODYNAMIC_GRUNEISEN_PARAMETER = Dimensionless(
    "thermodynamic_gruneisen_parameter"
)
GRUNEISEN_PARAMETER = Dimensionless("gruneisen_parameter")
"""Describes the effect that changing the [volume][isqx.VOLUME] of a crystal
lattice has on its vibrational properties, and, as a consequence, the effect
that changing [temperature][isqx.TEMPERATURE] has on the size or dynamics of the
lattice."""
MEAN_FREE_PATH_OF_PHONONS = MEAN_FREE_PATH["phonon"]
MEAN_FREE_PATH_OF_ELECTRONS = MEAN_FREE_PATH["electron"]
ENERGY_DENSITY_OF_STATES = QtyKind(J**-1 * M**-3, ("energy_density_of_states",))
"""Quantity in condensed matter physics."""
RESIDUAL_RESISTIVITY = RESISTIVITY["residual"]
LORENZ_COEFFICIENT = QtyKind(V**2 * K**-2, ("lorenz_coefficient",))
"""Coefficient of proportionality in the Wiedemann-Franz law."""
HALL_COEFFICIENT = QtyKind(M**3 * C**-1, ("hall_coefficient",))
THERMOELECTRIC_VOLTAGE = VOLTAGE["thermoelectric"]
"""[Voltage][isqx.VOLTAGE] caused by the thermoelectric effect."""
SEEBECK_COEFFICIENT = QtyKind(V * K**-1, ("seebeck_coefficient",))
PELTIER_COEFFICIENT = QtyKind(V, ("peltier_coefficient",))
THOMSON_COEFFICIENT = QtyKind(V * K**-1, ("thomson_coefficient",))
WORK_FUNCTION = ENERGY["work_function"]
IONIZATION_ENERGY = ENERGY["ionization"]
"""Minimum amount of [energy][isqx.ENERGY] required to remove an electron from an
atom or molecule in the gaseous state."""
ELECTRON_AFFINITY = ENERGY["electron_affinity"]
"""In condensed matter physics, [energy][isqx.ENERGY] difference between an
electron at rest at infinity and the lowest level of the conduction band in an
insulator or semiconductor."""
RICHARDSON_CONSTANT = QtyKind(A * M**-2 * K**-2, ("richardson_constant",))
FERMI_ENERGY = ENERGY["fermi"]
"""Concept in quantum mechanics referring to the [energy][isqx.ENERGY] difference
between the highest and lowest occupied single-particle states in a quantum
system of non-interacting fermions at absolute zero temperature."""
GAP_ENERGY = ENERGY["gap"]
"""Smallest [energy][isqx.ENERGY] difference between neighboring conduction
bands separated by a forbidden band."""
FERMI_TEMPERATURE = QtyKind(K, ("fermi",))
ELECTRON_DENSITY = NUMBER_DENSITY["electron"]
"""In condensed matter physics, number of electrons in the conduction band per
[volume][isqx.VOLUME]."""
HOLE_DENSITY = NUMBER_DENSITY["hole"]
"""In condensed matter physics, number of holes in the valence band per
[volume][isqx.VOLUME]."""
INTRINSIC_CARRIER_DENSITY = NUMBER_DENSITY["intrinsic_carrier"]
DONOR_DENSITY = NUMBER_DENSITY["donor"]
"""Number of donor levels per [volume][isqx.VOLUME]."""
ACCEPTOR_DENSITY = NUMBER_DENSITY["acceptor"]
"""Number of acceptor levels per [volume][isqx.VOLUME]."""
EFFECTIVE_MASS = MASS["effective"]
"""The [mass][isqx.MASS] that it seems to have when responding to forces, or the
mass that it seems to have when interacting with other identical particles in a
thermal distribution."""
MOBILITY_RATIO = Dimensionless("mobility_ratio")
RELAXATION_TIME_LATTICE = DURATION["relaxation_lattice"]
"""In condensed matter physics, [time constant][isqx.TIME_CONSTANT] for
interactions (scattering, annihilation, etc.) of charge carriers or
quasiparticles (phonons, etc.)."""
CARRIER_LIFETIME = DURATION["carrier_lifetime"]
"""Average [time][isqx.TIME] taken for free semiconductor electrons or holes to
recombine; whichever is the minority carrier."""
DIFFUSION_LENGTH = LENGTH["diffusion"]
"""In condensed matter physics, the square root of the product of
[diffusion coefficient][isqx.DIFFUSION_COEFFICIENT] and
[lifetime][isqx.LIFETIME]."""
EXCHANGE_INTEGRAL = ENERGY["exchange_integral"]
CURIE_TEMPERATURE = TEMPERATURE["curie"]
"""[Temperature][isqx.TEMPERATURE] above which certain materials lose their
permanent magnetic properties."""
NEEL_TEMPERATURE = TEMPERATURE["neel"]
"""Critical [temperature][isqx.TEMPERATURE] of an antiferromagnet."""
SUPERCONDUCTION_TRANSITION_TEMPERATURE = TEMPERATURE[
    "superconduction_transition"
]
"""Critical [temperature][isqx.TEMPERATURE] of a superconductor."""
THERMODYNAMIC_CRITICAL_MAGNETIC_FLUX_DENSITY = MAGNETIC_FLUX_DENSITY[
    "critical", "thermodynamic"
]
LOWER_CRITICAL_MAGNETIC_FLUX_DENSITY = MAGNETIC_FLUX_DENSITY[
    "critical", "lower"
]
UPPER_CRITICAL_MAGNETIC_FLUX_DENSITY = MAGNETIC_FLUX_DENSITY[
    "critical", "upper"
]
SUPERCONDUCTOR_ENERGY_GAP = ENERGY["superconductor_gap"]
"""Width of the forbidden [energy][isqx.ENERGY] band in a superconductor."""
LONDON_PENETRATION_DEPTH = LENGTH["london_penetration_depth"]
"""[Distance][isqx.DISTANCE] to which a magnetic field penetrates into a
superconductor."""
COHERENCE_LENGTH = LENGTH["coherence"]
"""Characteristic [length][isqx.LENGTH] in a superconductor."""

#
# information science and technology [ISO 80000-13]
#

# traffic
ERLANG = Dimensionless("erlang")
"""Erlang, a dimensionless unit for telephone traffic intensity."""
TRAFFIC_INTENSITY = Dimensionless("traffic_intensity")
TRAFFIC_OFFERED_INTENSITY = Dimensionless("traffic_offered_intensity")
TRAFFIC_CARRIED_INTENSITY = Dimensionless("traffic_carried_intensity")
MEAN_QUEUE_LENGTH = Dimensionless("mean_queue_length")
"""[Time][isqx.TIME] average of the [length][isqx.LENGTH] of a queue."""
LOSS_PROBABILITY = Dimensionless("loss_probability")
"""Probability for losing a call attempt."""
WAITING_PROBABILITY = Dimensionless("waiting_probability")
"""Probability for waiting for a resource."""
CALL_INTENSITY = QtyKind(HZ, ("call_intensity",))
COMPLETED_CALL_INTENSITY = QtyKind(HZ, ("completed_call_intensity",))
"""Completed calls per [time][isqx.TIME]."""

# storage and transfer
STORAGE_CAPACITY = Dimensionless("storage_capacity")
BIT = Dimensionless("bit")
BYTE = (8 * BIT).alias("byte", allow_prefix=True)
OCTET = (8 * BIT).alias("octet", allow_prefix=True)
EQUIVALENT_BINARY_STORAGE_CAPACITY = QtyKind(
    BIT, ("equivalent_binary_storage_capacity",)
)
TRANSFER_RATE = QtyKind(S**-1, ("transfer_rate",))
PERIOD_OF_DATA_ELEMENTS = PERIOD["data_elements"]
BIT_RATE = QtyKind(BIT * S**-1, ("bit_rate",))
"""Information transmission rate expressed in bits per second."""
BIT_PERIOD = PERIOD["bit"]
EQUIVALENT_BIT_RATE = QtyKind(BIT * S**-1, ("equivalent_bit_rate",))
BAUD = (S**-1)["modulation_rate"].alias("baud", allow_prefix=True)
"""Baud, a unit of modulation rate (symbol rate)."""
MODULATION_RATE = QtyKind(BAUD)
"""Rate of modulation of a digital signal."""

# signals and errors
QUANTIZING_DISTORTION = QtyKind(W, ("quantizing_distortion",))
CARRIER_POWER = POWER["carrier"]
SIGNAL_ENERGY_PER_BINARY_DIGIT = ENERGY["signal_per_binary_digit"]
ERROR_PROBABILITY = Dimensionless("error_probability")
"""Probability for incorrectly receiving a data element."""
HAMMING_DISTANCE = Dimensionless("hamming_distance")
"""Number of bits that differ between two strings."""
CLOCK_FREQUENCY = FREQUENCY["clock"]
"""[Frequency][isqx.FREQUENCY] at which CPU chip or core is operating."""
DECISION_CONTENT = Dimensionless("decision_content")

# information theory [ISO 80000-1 annex C]
PROBABILITY_RATIO = Dimensionless("probability_ratio")
SHANNON = Log(PROBABILITY_RATIO, base=2).alias("shannon")
"""Logarithmic level of information (base 2)."""
HARTLEY = Log(PROBABILITY_RATIO, base=10).alias("hartley")
"""Logarithmic level of information (base 10), also known as a `ban` or `dit`."""
NAT = Log(PROBABILITY_RATIO, base=_E).alias("nat")
"""Natural level of information (base e)."""
INFORMATION_CONTENT = QtyKind(SHANNON, ("information_content",))
"""Logarithmic quantity derived from the probability of a particular event."""
# entropy defined in ISO 80000-5
MAXIMUM_ENTROPY = ENTROPY["maximum"]
RELATIVE_ENTROPY = Dimensionless("relative_entropy")
REDUNDANCY = QtyKind(SHANNON, ("redundancy",))
"""In information theory, extra bits transmitted without adding information."""
RELATIVE_REDUNDANCY = Dimensionless("relative_redundancy")
JOINT_INFORMATION_CONTENT = INFORMATION_CONTENT["joint"]
CONDITIONAL_INFORMATION_CONTENT = INFORMATION_CONTENT["conditional"]
CONDITIONAL_ENTROPY = ENTROPY["conditional"]
"""Measure of relative information in probability theory and information
theory."""
EQUIVOCATION = CONDITIONAL_ENTROPY["equivocation"]
"""Concept in information theory: the information that is lost during
transmission over a channel between an information source (sender) and an
information sink (receiver)."""
IRRELEVANCE = CONDITIONAL_ENTROPY["irrelevance"]
TRANSINFORMATION_CONTENT = INFORMATION_CONTENT["transinformation"]
"""Measure of dependence between two variables."""
MEAN_TRANSINFORMATION_CONTENT = QtyKind(
    SHANNON, ("mean_transinformation_content",)
)
CHARACTER_MEAN_ENTROPY = QtyKind(SHANNON, ("character_mean_entropy",))
AVERAGE_INFORMATION_RATE = QtyKind(
    SHANNON * S**-1, ("average_information_rate",)
)
CHARACTER_MEAN_TRANSINFORMATION_CONTENT = QtyKind(
    SHANNON, ("character_mean_transinformation_content",)
)
AVERAGE_TRANSINFORMATION_RATE = QtyKind(
    SHANNON * S**-1, ("average_transinformation_rate",)
)
CHANNEL_CAPACITY_PER_CHARACTER = QtyKind(
    SHANNON, ("channel_capacity_per_character",)
)
CHANNEL_TIME_CAPACITY = QtyKind(SHANNON * S**-1, ("channel_time_capacity",))
"""Tight upper bound on the rate at which information can be reliably
transmitted over a communications channel."""

KIBI = Prefix(1024**1, "kibi")
MEBI = Prefix(1024**2, "mebi")
GIBI = Prefix(1024**3, "gibi")
TEBI = Prefix(1024**4, "tebi")
PEBI = Prefix(1024**5, "pebi")
EXBI = Prefix(1024**6, "exbi")
ZEBI = Prefix(1024**7, "zebi")
YOBI = Prefix(1024**8, "yobi")
