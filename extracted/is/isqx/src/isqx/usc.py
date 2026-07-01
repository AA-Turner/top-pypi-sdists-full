"""United States customary and British Imperial units.

See: [isqx._citations.SP811][], [isqx._citations.H44][],
[isqx._citations.WMA1985][].
"""

from decimal import Decimal
from fractions import Fraction

from ._core import PI, LazyProduct, Translated
from ._iso80000 import (
    CONST_DENSITY_H2O,
    CONST_DENSITY_HG,
    CONST_STANDARD_GRAVITY,
    HOUR,
    KG,
    KGF,
    M_PERS2,
    MILLI,
    MIN,
    PA,
    G,
    J,
    K,
    L,
    M,
    S,
    W,
)

#
# temperature [H44 C-23]
#

R = (Fraction(5, 9) * K).alias("rankine")
"""Thermodynamic Temperature (Rankine). Absolute scale."""
FAHRENHEIT = Translated(R, Decimal("-459.67"), "fahrenheit")
"""Thermodynamic Temperature (Fahrenheit). Absolute, translated scale.
Cannot be composed with other units."""

#
# length [H44 C-24]
#

FT = (Decimal("0.3048") * M).alias("foot")
"""International foot."""
FT_US_SURVEY = (Fraction(1200, 3937) * M).alias("foot_us_survey")
"""U.S. survey foot, deprecated since Dec 31, 2022."""  # H44 C-10
IN = (Fraction(1, 12) * FT).alias("inch")
"""International inch."""
YD = (3 * FT).alias("yard")
"""International yard."""  # H44 C-25
MI = (5280 * FT).alias("mile")
"""International mile, also known as statute mile."""  # H44 C-25
NMI = (1852 * M).alias("nautical_mile")
"""International nautical mile."""  # H44 C-25
MIL = (Fraction(1, 1000) * IN).alias("mil")
"""Thousandth of an inch, a unit of thickness (also known as thou)."""
HAND = (4 * IN).alias("hand")
"""Unit of length, for measuring the height of horses."""
POINT = (Fraction(1, 72) * IN).alias("point")
"""Typographical point (desktop publishing)."""  # H44 C-25


# gunter's or surveyors chain units
ROD = (Fraction(33, 2) * FT).alias("rod")
"""Rod, also known as pole or perch."""  # H44 C-5, C-25
FURLONG = (40 * ROD).alias("furlong")
"""Furlong."""
FATHOM = (6 * FT).alias("fathom")
"""Fathom, a unit of length used for water depth."""
CABLE = (120 * FATHOM).alias("cable")
"""Cable length."""
LEAGUE = (3 * MI).alias("league")
"""League."""
LINK = (Fraction(66, 100) * FT).alias("link")
"""Gunter's link."""
CHAIN = (100 * LINK).alias("chain")
"""Gunter's chain."""

#
# area
#

SQ_YD = YD**2
ROOD = (1210 * SQ_YD).alias("rood")
"""Rood, an imperial unit of area."""  # WMA1985 1VI
SQ_FT = FT**2
ACRE = (43560 * SQ_FT).alias("acre")
"""International acre."""  # H44 C-25
ACRE_SURVEY = (43560 * (FT_US_SURVEY**2)).alias("acre_survey")
"""U.S. survey acre."""  # H44 C-14
SQ_BUILDING = (100 * SQ_FT).alias("square_building")
"""Square building, used in the U.S. construction industry."""
SQ_MI = MI**2
SQ_MIL = MIL**2
CIRCULAR_MIL = (LazyProduct((PI, (4, -1))) * SQ_MIL).alias("circular_mil")
"""Circular mil, a unit of area for wire cross-sections."""  # SP811 B.8

#
# volume [H44 C-6]
#

# liquid, US
CU_IN = IN**3
GAL = (231 * CU_IN).alias("gallon")
"""U.S. liquid gallon."""
QUART = (Fraction(1, 4) * GAL).alias("quart")
"""U.S. liquid quart."""
PINT = (Fraction(1, 2) * QUART).alias("pint")
"""U.S. liquid pint."""
CUP = (Fraction(1, 2) * PINT).alias("cup_measuring")
"""U.S. customary cup."""  # H44 C-27
GILL = (Fraction(1, 4) * PINT).alias("gill")
"""U.S. liquid gill."""
FL_OZ = (Fraction(1, 128) * GAL).alias("ounce_fluid")
"""U.S. fluid ounce."""
TABLESPOON = (Fraction(1, 2) * FL_OZ).alias("tablespoon_measuring")
"""U.S. customary tablespoon."""  # H44 C-28
TEASPOON = (Fraction(1, 3) * TABLESPOON).alias("teaspoon_measuring")
"""U.S. customary teaspoon."""  # H44 C-28
# consult federal and state laws for the appropriate barrel definition [H44 C-26]
BBL_FEDERAL_FERMENTED_LIQUOR = (31 * GAL).alias("bbl_federal_fermented_liquor")
BBL_STATE_LIQUID = ((31 + Fraction(1, 2)) * GAL).alias("bbl_state_liquid")
BBL_FEDERAL_CISTERN = (36 * GAL).alias("bbl_federal_cistern")
BBL_PROOF_SPIRIT = (50 * GAL).alias("bbl_proof_spirit")
BBL_OIL = (42 * GAL).alias("bbl_oil", allow_prefix=True)
"""U.S. standard barrel for crude oil and petroleum products."""

# fluid, apothecaries
DRAM_FL = (Fraction(1, 8) * FL_OZ).alias("dram_fluid")
"""U.S. apothecaries' fluid dram."""
MINIM = (Fraction(1, 60) * DRAM_FL).alias("minim")
"""U.S. apothecaries' minim."""

# dry, US
BUSHEL = (Decimal("2150.42") * CU_IN).alias("bushel")
"""U.S. dry bushel."""  # H44 C-26
BUSHEL_HEAPED = (Decimal("2747.715") * CU_IN).alias("bushel_heaped")
"""U.S. heaped bushel."""  # H44 C-26
PECK = (Fraction(1, 4) * BUSHEL).alias("peck")
"""U.S. dry peck."""
QUART_DRY = (Fraction(1, 8) * PECK).alias("quart_dry")
"""U.S. dry quart."""
PINT_DRY = (Fraction(1, 2) * QUART_DRY).alias("pint_dry")
"""U.S. dry pint."""
BBL_DRY = (7056 * CU_IN).alias("bbl_dry")
"""U.S. standard barrel for fruits, vegetables and dry commodities
(excluding cranberries)."""  # H44 C-26
BBL_CRANBERRY = (5826 * CU_IN).alias("bbl_cranberry")
"""U.S. standard barrel for cranberries."""  # H44 C-26

# british imperial [WMA1985 1VI]
GAL_IMP = (Decimal("4.54609") * L).alias("gallon_imperial")
"""British Imperial gallon."""
BUSHEL_IMP = (8 * GAL_IMP).alias("bushel_imperial")
"""British Imperial bushel."""
PECK_IMP = (2 * GAL_IMP).alias("peck_imperial")
"""British Imperial peck."""  # H44 C-8
QUARTER_IMP = (8 * BUSHEL_IMP).alias("quarter_imperial")
"""British Imperial quarter."""  # H44 C-8
QUART_IMP = (Fraction(1, 4) * GAL_IMP).alias("quart_imperial")
"""British Imperial quart."""
PINT_IMP = (Fraction(1, 2) * QUART_IMP).alias("pint_imperial")
"""British Imperial pint."""
FL_OZ_IMP = (Fraction(1, 160) * GAL_IMP).alias("ounce_fluid_imperial")
"""British Imperial fluid ounce."""
DRACHM_FL_IMP = (Fraction(1, 8) * FL_OZ_IMP).alias("drachm_fluid_imperial")
"""British Imperial fluid drachm."""
SCRUPLE_FL_IMP = (Fraction(1, 3) * DRACHM_FL_IMP).alias(
    "scruple_fluid_imperial"
)
"""British Imperial fluid scruple."""  # H44 C-8
MINIM_IMP = (Fraction(1, 20) * SCRUPLE_FL_IMP).alias("minim_imperial")
"""British Imperial minim."""  # H44 C-8

# other
ACRE_FOOT = (ACRE * FT).alias("acre_foot")
"""Volume of water that covers one acre to a depth of one foot."""  # H44 C-19
CORD = (128 * FT**3).alias("cord")
"""Cord, a unit of volume for firewood."""  # H44 C-26
WATER_TON = (224 * GAL_IMP).alias("water_ton")
"""Water ton, an English unit of volume,
approximately the volume of a long ton of water."""  # H44 C-28


#
# mass
#

# avoirdupois (common) [H44 C-7]
LB = (Decimal("0.45359237") * KG).alias("pound")
"""Avoirdupois pound mass."""  # H44 C-29
GRAIN = (Fraction(1, 7000) * LB).alias("grain")
"""Grain. Equivalent across Avoirdupois, Troy, and Apothecaries' systems."""  # H44 C-29
OZ = (Fraction(1, 16) * LB).alias("ounce")
"""Avoirdupois ounce."""
DRAM = (Fraction(1, 16) * OZ).alias("dram")
"""Avoirdupois dram."""
CWT = (100 * LB).alias("hundredweight")
"""Short hundredweight (also known as cental)"""
TON = (2000 * LB).alias("ton")
"""Short or net ton."""

# british imperial [WMA1985 1VI]
STONE = (14 * LB).alias("stone")
"""Stone, a British unit of mass."""
QUARTER = (28 * LB).alias("quarter")
"""Quarter, a British unit of mass."""
CWT_LONG = (112 * LB).alias("hundredweight_long")
"""Long hundredweight."""
TON_LONG = (2240 * LB).alias("ton_long")
"""Long, gross or shipper's ton."""

# troy (for precious metals) [H44 C-7]
LB_T = (5760 * GRAIN).alias("pound_troy")
"""Troy pound mass."""
OZ_T = (Fraction(1, 12) * LB_T).alias("ounce_troy")
"""Troy ounce."""
DWT = (Fraction(1, 20) * OZ_T).alias("pennyweight")
"""Pennyweight."""

# apothecaries' (for medicine) [H44 C-8]
LB_AP = (5760 * GRAIN).alias("pound_apothecaries")
"""Apothecaries' pound mass."""
OZ_AP = (Fraction(1, 12) * LB_AP).alias("ounce_apothecaries")
"""Apothecaries' ounce."""
DRAM_AP = (Fraction(1, 8) * OZ_AP).alias("dram_apothecaries")
"""Apothecaries' dram."""
SCRUPLE = (Fraction(1, 3) * DRAM_AP).alias("scruple")
"""Apothecaries' scruple."""
# assaying and gemstones
CARAT = (200 * (MILLI * G)).alias("carat")
"""Metric carat, for gemstones."""  # H44 C-29
POINT_MASS = (Fraction(1, 100) * CARAT).alias("point_mass")
"""Point, for gemstones."""  # H44 C-30
ASSAY_TON = (Decimal("29.167") * G).alias("assay_ton")
"""Assay ton. The mass in milligrams of precious metal from one assay ton of ore
gives the troy ounces per short ton."""  # H44 C-29
QUINTAL = (100 * KG).alias("quintal")
"""Quintal, a historical unit of mass, now usually 100 kg."""  # WMA1985 1VI

#
# misc / engineering
#

# linear velocity
KNOT = (NMI * HOUR**-1).alias("knot")
"""Knot, one nautical mile per hour."""
MPH = (MI * HOUR**-1).alias("mph")
"""Miles per hour."""

# acceleration
FT_PERS2 = FT * S**-2
"""Feet per second squared."""
# force
LBF = (CONST_STANDARD_GRAVITY * LB * M_PERS2).alias("lbf")
"""Pound-force."""
POUNDAL = (LB * FT * S**-2).alias("poundal")
"""Poundal, the force required to accelerate 1 lb by 1 ft/s²."""
KIP = (1000 * LBF).alias("kip")

# pressure [H44 C-59]
PSI = (LBF * IN**-2).alias("psi")
"""Pound-force per square inch, a unit of pressure."""
KSI = (1000 * PSI).alias("ksi")
"""Kilo-pound-force per square inch, a unit of pressure."""
PSF = (LBF * SQ_FT**-1).alias("psf")
"""Pound-force per square foot, a unit of pressure."""
INHG = (LazyProduct((CONST_DENSITY_HG, CONST_STANDARD_GRAVITY)) * IN).alias(
    "inch_of_hg"
)
"""Inch of mercury, a unit of pressure."""  # SP811 B.8
INH2O = (LazyProduct((CONST_DENSITY_H2O, CONST_STANDARD_GRAVITY)) * IN).alias(
    "inch_of_h2o"
)
"""Inch of water (conventional), a unit of pressure."""
INH2O_4C = (Decimal("249.082") * PA).alias("inch_of_water_4c")  # approx
"""Inch of water at 4 °C (temperature of maximum water density)."""
INH2O_60F = (Decimal("248.84") * PA).alias("inch_of_water_60f")  # approx
"""Inch of water at 60 °F."""

SLUG = (LBF * FT_PERS2**-1).alias("slug")
"""A unit of mass that accelerates by 1 ft/s² when a force of 1 lbf is exerted on it."""

# energy
FT_LBF = (FT * LBF).alias("foot_pound")
"""Foot-pound, a unit of energy or work."""
# [SP811 B.8 (footnote 10), H44 C-59]
CAL_IT = (Decimal("4.1868") * J).alias("calorie_it")
"""Calorie (International Table)."""
CAL_TH = (Decimal("4.184") * J).alias("calorie_th")
"""Calorie (thermochemical)."""
CAL_MEAN = (Decimal("4.19002") * J).alias("calorie_mean")  # approx
"""Calorie (mean). The heat required to raise 1 g of water from 0 °C to 100 °C,
divided by 100."""
CAL_15C = (Decimal("4.18580") * J).alias("calorie_15c")  # approx
"""Calorie (at 15 °C). The heat required to raise 1 g of water from 14.5 °C to
15.5 °C."""
CAL_20C = (Decimal("4.18190") * J).alias("calorie_20c")  # approx
"""Calorie (at 20 °C). The heat required to raise 1 g of water from 19.5 °C to
20.5 °C."""
# [SP811 B.8 (footnote 9), H44 C-57]
BTU_IT = (Decimal("1055.05585262") * J).alias("btu_it")
"""British thermal unit (International Table). The most widely used definition."""
BTU_TH = (Decimal("1054.350") * J).alias("btu_th")  # approx
"""British thermal unit (thermochemical)."""
BTU_MEAN = (Decimal("1055.87") * J).alias("btu_mean")  # approx
"""British thermal unit (mean, from 32 °F to 212 °F, divided by 180)."""
BTU_39F = (Decimal("1059.67") * J).alias("btu_39f")  # approx
"""British thermal unit (at 39 °F)."""
BTU_59F = (Decimal("1054.80") * J).alias("btu_59f")  # approx
"""British thermal unit (at 59 °F). Used for American natural gas pricing."""
BTU_60F = (Decimal("1054.68") * J).alias("btu_60f")  # approx
"""British thermal unit (at 60 °F)."""
QUAD = (10**15 * BTU_IT).alias("quad")
"""Quad (International Table). Used by U.S. Department of Energy."""  # H44 B.8 footnote 9

# power [SP811 B.8]
HP = (33000 * (FT * LBF * MIN**-1)).alias("horsepower")
"""Mechanical horsepower (imperial).
See: https://en.wikipedia.org/wiki/Horsepower#Imperial_horsepower"""
HP_METRIC = (75 * (KGF * M * S**-1)).alias("horsepower_metric")
"""Metric horsepower.
See: <https://en.wikipedia.org/wiki/Horsepower#Metric_horsepower_(PS,_KM,_cv,_hk,_pk,_k,_ks,_ch)>"""
HP_BOILER = (Decimal("9809.50") * W).alias("horsepower_boiler")  # approx
"""Boiler horsepower."""
HP_ELECTRIC = (746 * W).alias("horsepower_electric")
"""Electrical horsepower."""
HP_UK = (Decimal("745.70") * W).alias("horsepower_uk")  # approx
"""UK horsepower."""
HP_WATER = (Decimal("746.043") * W).alias("horsepower_water")  # approx
"""Water horsepower."""

#
# misc
#
MPG = (MI * GAL**-1).alias("miles_per_gallon")
"""Miles per gallon, a unit of fuel economy."""  # SP811 B.5
# NOTE: not defining R-value (°F·ft²·h/Btu), U-factor (Btu/(h·ft²·°F)), K-value (Btu·in/(h·ft²·°F))
