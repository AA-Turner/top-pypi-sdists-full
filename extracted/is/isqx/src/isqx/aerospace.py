"""
Units and quantities common in aerospace engineering.

See: [isqx._citations.ICAO][]
"""
# TODO: ISO 2533:1975 (standard atmosphere)
# TODO: ISO 1151

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Annotated, Literal

from ._core import (
    DELTA,
    Dimensionless,
    OriginAt,
    QtyKind,
    Quantity,
    ratio,
    slots,
)
from ._iso80000 import (
    ALTITUDE,
    AREA,
    DISTANCE,
    DRAG,
    DRAG_COEFFICIENT,
    DYNAMIC_PRESSURE,
    HOUR,
    KG,
    LENGTH,
    LIFT,
    M_PERS,
    MACH_NUMBER,
    MASS,
    MASS_FLOW_RATE,
    MIN,
    MOMENT_OF_FORCE,
    PA,
    POWER,
    PRESSURE,
    RAD,
    RAD_PERS,
    SPECIFIC_ENERGY,
    TEMPERATURE,
    VELOCITY,
    K,
    L,
    M,
    N,
    S,
    W,
)
from .usc import FT

#
# aircraft performance: state
#

# heading: [0, 360) degrees
HEADING = QtyKind(RAD, ("heading",))
HEADING_TRUE = HEADING["true"]
HEADING_MAG = HEADING["magnetic"]
HEADING_TRUE_WIND = HEADING_TRUE["wind"]
HEADING_MAG_WIND = HEADING_MAG["wind"]
GROUND_TRACK = HEADING["ground_track"]
"""Direction of the aircraft's velocity vector relative to the ground."""

PRESSURE_ALTITUDE = ALTITUDE["pressure"]
"""Pressure altitude, as measured by the altimeter (standard pressure setting 1013.25 hPa)."""
DENSITY_ALTITUDE = ALTITUDE["density"]
"""Density altitude, as measured by the altimeter."""
GEOPOTENTIAL_ALTITUDE = ALTITUDE["geopotential"]
"""Geopotential altitude, as measured from mean sea level."""
GEOMETRIC_ALTITUDE = ALTITUDE["geometric"]
"""Altitude measured from mean sea level (e.g. via GNSS)."""
# height: measured from *specific* datum
GEODETIC_HEIGHT = QtyKind(M, ("height", "geodetic"))
"""Height above the reference ellipsoid."""
HEIGHT_ABOVE_GROUND_LEVEL = QtyKind(M, ("height", "above_ground_level"))
"""Height above ground level (radio altimeter)."""

L_OVER_D = ratio(LIFT(N), DRAG(N))

K_PERM = K * M**-1
"""Kelvin per meter, a unit of temperature gradient. For use in ISA."""
ENERGY_HEIGHT = LENGTH["energy_height"]
"""Specific energy expressed as a height."""
SPECIFIC_EXCESS_POWER = QtyKind(M_PERS, ("specific_excess_power",))

#
# aircraft geometry
#

WINGSPAN = LENGTH["wingspan"]
CHORD = LENGTH["chord"]
MEAN_AERODYNAMIC_CHORD = CHORD["mean_aerodynamic"]
"""Mean aerodynamic chord (MAC)."""
MEAN_GEOMETRIC_CHORD = CHORD["mean_geometric"]
"""Mean geometric chord (Standard Mean Chord)."""
WING_AREA = AREA["wing"]
"""Reference wing area."""
WETTED_AREA = AREA["wetted"]
PLANFORM_AREA = AREA["planform"]
FRONTAL_AREA = AREA["frontal"]
"""Cross-sectional area perpendicular to the flow."""
DISK_AREA = AREA["disk"]
"""Area swept by a propeller or rotor."""
TAIL_AREA = AREA["tail"]
TAIL_MOMENT_ARM = LENGTH["tail_moment_arm"]
ASPECT_RATIO = Dimensionless("aspect_ratio")
TAPER_RATIO = Dimensionless("taper_ratio")
SWEEP_ANGLE = QtyKind(RAD, ("angle", "sweep"))
DIHEDRAL_ANGLE = QtyKind(RAD, ("angle", "dihedral"))
TWIST_ANGLE = QtyKind(RAD, ("angle", "twist"))
"""Washout or washin angle."""
FINENESS_RATIO = Dimensionless("fineness_ratio")
"""Ratio of length to maximum diameter for a fuselage or body."""

#
# aerodynamics
#

ANGLE_OF_ATTACK = QtyKind(RAD, ("angle", "angle_of_attack"))
"""Angle between the chord line and the relative wind vector."""
SIDESLIP_ANGLE = QtyKind(RAD, ("angle", "sideslip"))
"""Angle between the relative wind vector and the plane of symmetry."""
DOWNWASH_ANGLE = QtyKind(RAD, ("angle", "downwash"))

CRITICAL_MACH_NUMBER = MACH_NUMBER["critical"]
DRAG_DIVERGENCE_MACH_NUMBER = MACH_NUMBER["drag_divergence"]

ZERO_LIFT_DRAG_COEFFICIENT = DRAG_COEFFICIENT["zero_lift"]
LIFT_INDUCED_DRAG_COEFFICIENT = DRAG_COEFFICIENT["lift_induced"]
INDUCED_DRAG_COEFFICIENT = DRAG_COEFFICIENT["induced"]

OSWALD_EFFICIENCY = Dimensionless("oswald_efficiency_factor")
"""Span efficiency factor."""
# TODO: stability derivatives
PITCHING_MOMENT_COEFFICIENT = Dimensionless("pitching_moment_coefficient")
ROLLING_MOMENT_COEFFICIENT = Dimensionless("rolling_moment_coefficient")
YAWING_MOMENT_COEFFICIENT = Dimensionless("yawing_moment_coefficient")
PRESSURE_COEFFICIENT = Dimensionless("pressure_coefficient")
SKIN_FRICTION_COEFFICIENT = Dimensionless("skin_friction_coefficient")
LIFT_SLOPE = Dimensionless("lift_slope")
"""Change in lift coefficient per unit angle of attack (per radian)."""

CIRCULATION = QtyKind(M**2 * S**-1, ("circulation",))

#
# aircraft design
#

AIRCRAFT_MASS = MASS["aircraft"]
GROSS = AIRCRAFT_MASS["gross"]
CARGO_CAPACITY = AIRCRAFT_MASS["cargo_capacity"]
FUEL_CAPACITY = AIRCRAFT_MASS["fuel_capacity"]
TAKEOFF_MASS = AIRCRAFT_MASS["takeoff"]
LANDING_MASS = AIRCRAFT_MASS["landing"]
MAXIMUM_TAKEOFF_WEIGHT = TAKEOFF_MASS["maximum"]
ZERO_FUEL_WEIGHT = AIRCRAFT_MASS["zero_fuel_weight"]
OPERATING_EMPTY_WEIGHT = AIRCRAFT_MASS["operating_empty"]
PAYLOAD = AIRCRAFT_MASS["payload"]
EMPTY_WEIGHT = AIRCRAFT_MASS["empty"]

TANK_CAPACITY = QtyKind(L, ("aircraft", "tank_capacity"))  # ICAO 1.14
ENDURANCE = QtyKind(HOUR, ("aircraft", "endurance"))  # ICAO 1.6

WING_LOADING = QtyKind(N * M**-2, ("wing_loading",))
"""Weight of the aircraft divided by the wing area."""
POWER_LOADING = QtyKind(N * W**-1, ("power_loading",))
"""Weight of the aircraft divided by the engine power."""
THRUST_LOADING = Dimensionless("thrust_loading")
"""Thrust to weight ratio."""

#
# flight dynamics
#

LOAD_FACTOR = Dimensionless("load_factor")
"""Ratio of lift to weight (n)."""

ANGULAR_VELOCITY = QtyKind(RAD_PERS, ("angular_velocity",))
ROLL_RATE = ANGULAR_VELOCITY["roll"]
"""Angular velocity about the body X axis."""
PITCH_RATE = ANGULAR_VELOCITY["pitch"]
"""Angular velocity about the body Y axis."""
YAW_RATE = ANGULAR_VELOCITY["yaw"]
"""Angular velocity about the body Z axis."""
TURN_RATE = ANGULAR_VELOCITY["turn"]
"""Rate of change of heading."""

ATTITUDE = QtyKind(RAD, ("attitude",))
BANK_ANGLE = ATTITUDE["bank"]
PITCH_ANGLE = ATTITUDE["pitch"]
FLIGHT_PATH_ANGLE = ATTITUDE["flight_path"]
"""Angle between the velocity vector and the horizon."""

AIRCRAFT_MOMENT = MOMENT_OF_FORCE["aircraft"]
PITCHING_MOMENT = AIRCRAFT_MOMENT["pitching"]
ROLLING_MOMENT = AIRCRAFT_MOMENT["rolling"]
YAWING_MOMENT = AIRCRAFT_MOMENT["yawing"]

#
# stability and control
#

STATIC_MARGIN = Dimensionless("static_margin")
"""Distance between the neutral point and the center of gravity, normalized by MAC."""
NEUTRAL_POINT = DISTANCE["neutral_point"]
"""Longitudinal position of the aerodynamic center of the whole aircraft."""
CENTER_OF_GRAVITY = DISTANCE["center_of_gravity"]
TAIL_VOLUME_COEFFICIENT = Dimensionless("tail_volume_coefficient")
HORIZONTAL_TAIL_VOLUME_COEFFICIENT = TAIL_VOLUME_COEFFICIENT["horizontal"]
VERTICAL_TAIL_VOLUME_COEFFICIENT = TAIL_VOLUME_COEFFICIENT["vertical"]

#
# aircraft performance
#

STATIC_TEMPERATURE = TEMPERATURE["static"]
TOTAL_TEMPERATURE = TEMPERATURE["total"]
"""Also known as stagnation temperature."""
CONST_TEMPERATURE_ISA: Annotated[Decimal, STATIC_TEMPERATURE(K)] = Decimal(
    "288.15"
)
TEMPERATURE_DEVIATION_ISA = STATIC_TEMPERATURE[
    DELTA, OriginAt(Quantity(CONST_TEMPERATURE_ISA, K))
]
"""Deviation from the [ISA temperature at sea level][isqx.aerospace.CONST_TEMPERATURE_ISA]."""

TOTAL_PRESSURE = PRESSURE["total"]
IMPACT_PRESSURE = DYNAMIC_PRESSURE["impact"]

PRESSURE_RATIO = Dimensionless("pressure_ratio")
"""Ratio of static pressure to standard sea level pressure."""
TEMPERATURE_RATIO = Dimensionless("temperature_ratio")
"""Ratio of static temperature to standard sea level temperature."""
DENSITY_RATIO = Dimensionless("density_ratio")
"""Ratio of air density to standard sea level density."""

# linear velocity
AIRSPEED = QtyKind(M_PERS, ("airspeed",))
INDICATED_AIRSPEED = AIRSPEED["indicated"]
"""Indicated airspeed (IAS), as measured directly from the pitot-static system."""
CALIBRATED_AIRSPEED = AIRSPEED["calibrated"]
"""Calibrated airspeed (CAS), [IAS][isqx.aerospace.INDICATED_AIRSPEED] corrected for instrument and position errors."""
EQUIVALENT_AIRSPEED = AIRSPEED["equivalent"]
"""Equivalent airspeed (EAS), [CAS][isqx.aerospace.CALIBRATED_AIRSPEED] corrected for compressibility."""
TRUE_AIRSPEED = AIRSPEED["true"]
"""True airspeed (TAS), speed relative to the airmass."""
GROUND_SPEED = AIRSPEED["ground"]
"""Speed relative to the ground."""
STALL_SPEED = AIRSPEED["stall"]
APPROACH_SPEED = AIRSPEED["approach"]
TAKEOFF_SPEED = AIRSPEED["takeoff"]
ROTATE_SPEED = AIRSPEED["rotate"]
V1_SPEED = AIRSPEED["v1"]
V2_SPEED = AIRSPEED["v2"]
VREF_SPEED = AIRSPEED["vref"]
# TODO: other v speeds
CORNER_SPEED = AIRSPEED["corner"]
"""The speed at which the maximum lift coefficient and the maximum load factor are reached simultaneously."""
WIND_SPEED = QtyKind(M_PERS, ("wind",))
"""Wind speed."""
SPEED_OF_SOUND = QtyKind(M_PERS, ("sound",))
"""Speed of sound."""

FT_PER_MIN = FT * MIN**-1
VERTICAL_RATE = QtyKind(M_PERS, ("vertical_rate",))
"""Rate of climb or descent.

Commonly expressed in [feet per minute][isqx.aerospace.FT_PER_MIN]."""
VERTICAL_RATE_INERTIAL = VERTICAL_RATE["inertial"]
"""Vertical rate derived from inertial sensors/GNSS."""
VERTICAL_RATE_BAROMETRIC = VERTICAL_RATE["barometric"]
"""Vertical rate derived from barometric pressure changes."""

SPECIFIC_IMPULSE = QtyKind(S, ("specific_impulse",))
RANGE = DISTANCE["range"]
TAKEOFF_DISTANCE = DISTANCE["takeoff"]
LANDING_DISTANCE = DISTANCE["landing"]
TURN_RADIUS = DISTANCE["turn_radius"]

#
# propulsion
#
SHAFT_POWER = POWER["shaft"]
"""Power delivered to a shaft (e.g. turboprop)."""
BRAKE_POWER = POWER["brake"]
EQUIVALENT_SHAFT_POWER = SHAFT_POWER["equivalent"]

ENGINE_MASS_FLOW_RATE = MASS_FLOW_RATE["engine"]
KG_PERS = KG * S**-1
THRUST_SPECIFIC_FUEL_CONSUMPTION = QtyKind(KG_PERS * N**-1, ("engine",))
"""Fuel mass flow rate per unit thrust."""
POWER_SPECIFIC_FUEL_CONSUMPTION = QtyKind(
    KG_PERS * W**-1, ("engine", "power_specific")
)
"""Fuel mass flow rate per unit power."""
FUEL_SPECIFIC_ENERGY = SPECIFIC_ENERGY["fuel"]
EXHAUST_VELOCITY = VELOCITY["exhaust"]
BYPASS_RATIO = Dimensionless("bypass_ratio")
# TODO: make efficieny kinds more specific
PROPULSIVE_EFFICIENCY = Dimensionless("efficiency_propulsive")
PROPELLER_EFFICIENCY = Dimensionless("efficiency_propeller")
ADVANCE_RATIO = Dimensionless("advance_ratio")
"""Ratio of freestream speed to tip speed for propellers."""

#
# aeroacoustics
#
# TODO: dBA, EPNdB etc.

#
# navigation
#


@dataclass(frozen=True, **slots)
class Aerodrome:
    ident: str
    ident_kind: Literal["icao", "iata"] | str


PRESSURE_ALTIMETER = QtyKind(PA, ("altimeter",))
"""Altimeter setting (QNH/QFE)."""
RUNWAY_LENGTH = QtyKind(M, ("runway", "length"))  # ICAO 1.12
RUNWAY_VISUAL_RANGE = QtyKind(M, ("runway", "visual_range"))  # ICAO 1.13
VISIBILITY = QtyKind(M, ("meteo", "visibility"))  # ICAO 1.15

#
# adsb/mode s
#

ICAO_ADDRESS = Dimensionless("icao_address_24_bit")
"""Unique 24-bit aircraft address assigned by ICAO."""
SQUAWK_CODE = Dimensionless("squawk_code_12_bit")
"""Mode A code (4 octal digits)."""

NAVIGATION_UNCERTAINTY_CATEGORY_POSITION = Dimensionless("adsb_nucp")
NAVIGATION_UNCERTAINTY_CATEGORY_VELOCITY = Dimensionless("adsb_nucv")
NAVIGATION_ACCURACY_CATEGORY_POSITION = Dimensionless("adsb_nacp")
NAVIGATION_ACCURACY_CATEGORY_VELOCITY = Dimensionless("adsb_nacv")
NAVIGATION_INTEGRITY_CATEGORY = Dimensionless("adsb_nic")
SURVEILLANCE_INTEGRITY_LEVEL = Dimensionless("adsb_sil")
