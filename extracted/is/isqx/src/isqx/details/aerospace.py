from .. import _iso80000, aerospace
from . import SELF, Details, Equation, Symbol, Wikidata

AEROSPACE: Details = {
    # performance
    aerospace.HEADING: Wikidata("Q4384217"),
    aerospace.PRESSURE_ALTITUDE: Wikidata("Q3233965"),
    aerospace.DENSITY_ALTITUDE: Wikidata("Q1209487"),
    aerospace.GEOPOTENTIAL_ALTITUDE: Wikidata("Q12432978"),
    aerospace.ENERGY_HEIGHT: (
        Equation(
            r"H_e = h + \frac{V^2}{2g}",
            {
                r"H_e": SELF,
                "h": aerospace.GEOMETRIC_ALTITUDE,
                "V": aerospace.TRUE_AIRSPEED,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
            },
        ),
    ),
    aerospace.SPECIFIC_EXCESS_POWER: (
        Equation(
            r"P_s = \frac{dH_e}{dt} = V \left(\frac{T-D}{W}\right)",
            {
                r"P_s": SELF,
                r"H_e": aerospace.ENERGY_HEIGHT,
                "t": _iso80000.TIME,
                "V": aerospace.TRUE_AIRSPEED,
                "T": _iso80000.THRUST,
                "D": _iso80000.DRAG,
                "W": _iso80000.WEIGHT,
            },
        ),
    ),
    # geometry
    aerospace.WINGSPAN: (Wikidata("Q245097"), Symbol("b")),
    aerospace.CHORD: (Wikidata("Q1384332"), Symbol("c")),
    aerospace.MEAN_AERODYNAMIC_CHORD: (
        Equation(
            r"\bar{c} = \frac{2}{S} \int_0^{b/2} c(y)^2 dy",
            {
                r"\bar{c}": SELF,
                "S": aerospace.WING_AREA,
                "b": aerospace.WINGSPAN,
                r"c(y)": (aerospace.CHORD, " at spanwise position y"),
            },
        ),
        Symbol("MAC"),
    ),
    aerospace.WING_AREA: (Symbol("S"), Symbol(r"S_{ref}")),
    aerospace.WETTED_AREA: (Symbol(r"S_{wet}"), Wikidata("Q3505294")),
    aerospace.ASPECT_RATIO: (
        Wikidata("Q1545619"),
        Equation(
            r"AR = \frac{b^2}{S}",
            {
                "AR": SELF,
                "b": aerospace.WINGSPAN,
                "S": aerospace.WING_AREA,
            },
        ),
    ),
    aerospace.TAPER_RATIO: (
        Equation(
            r"\lambda = \frac{c_t}{c_r}",
            {
                r"\lambda": SELF,
                r"c_t": (aerospace.CHORD, " at tip"),
                r"c_r": (aerospace.CHORD, " at root"),
            },
        ),
    ),
    aerospace.SWEEP_ANGLE: (Symbol(r"\Lambda"), Symbol(r"\Delta")),
    aerospace.DIHEDRAL_ANGLE: (Symbol(r"\Gamma"), Wikidata("Q1972636")),
    # aerodynamics
    aerospace.ANGLE_OF_ATTACK: (Symbol(r"\alpha"), Wikidata("Q370906")),
    aerospace.SIDESLIP_ANGLE: Symbol(r"\beta"),
    aerospace.DOWNWASH_ANGLE: (Symbol(r"\varepsilon"), Symbol(r"\epsilon")),
    aerospace.CRITICAL_MACH_NUMBER: (Symbol(r"M_{cr}"), Wikidata("Q1777346")),
    aerospace.DRAG_DIVERGENCE_MACH_NUMBER: (
        Symbol(r"M_{dd}"),
        Wikidata("Q5304818"),
    ),
    aerospace.ZERO_LIFT_DRAG_COEFFICIENT: Symbol(r"C_{D,0}"),
    # TODO drag polar cd0 + k cl^2 at subsonic?
    aerospace.LIFT_INDUCED_DRAG_COEFFICIENT: (
        Wikidata("Q7108183"),
        Equation(
            r"C_{D,i} = \frac{C_L^2}{\pi e AR}",
            {
                r"C_{D,i}": SELF,
                "C_L": _iso80000.LIFT_COEFFICIENT,
                "e": aerospace.OSWALD_EFFICIENCY,
                "AR": aerospace.ASPECT_RATIO,
            },
        ),
    ),
    aerospace.INDUCED_DRAG_COEFFICIENT: Symbol(r"C_{D,i}"),
    aerospace.OSWALD_EFFICIENCY: (Symbol("e"), Wikidata("Q7108183")),
    aerospace.PITCHING_MOMENT_COEFFICIENT: (
        Equation(
            r"C_m = \frac{M}{q_\infty S \bar{c}}",
            {
                r"C_m": SELF,
                "M": aerospace.PITCHING_MOMENT,
                r"q_\infty": ("freestream ", _iso80000.DYNAMIC_PRESSURE),
                "S": aerospace.WING_AREA,
                r"\bar{c}": aerospace.MEAN_AERODYNAMIC_CHORD,
            },
        ),
    ),
    aerospace.ROLLING_MOMENT_COEFFICIENT: (
        Equation(
            r"C_l = \frac{L}{q_\infty S b}",
            {
                r"C_l": SELF,
                "L": aerospace.ROLLING_MOMENT,
                r"q_\infty": ("freestream ", _iso80000.DYNAMIC_PRESSURE),
                "S": aerospace.WING_AREA,
                "b": aerospace.WINGSPAN,
            },
        ),
    ),
    aerospace.YAWING_MOMENT_COEFFICIENT: (
        Equation(
            r"C_n = \frac{N}{q_\infty S b}",
            {
                r"C_n": SELF,
                "N": aerospace.YAWING_MOMENT,
                r"q_\infty": ("freestream ", _iso80000.DYNAMIC_PRESSURE),
                "S": aerospace.WING_AREA,
                "b": aerospace.WINGSPAN,
            },
        ),
    ),
    aerospace.PRESSURE_COEFFICIENT: (
        Wikidata("Q1260777"),
        Equation(
            r"C_p = \frac{p - p_\infty}{q_\infty}",
            {
                r"C_p": SELF,
                "p": _iso80000.STATIC_PRESSURE,
                r"p_\infty": ("freestream ", _iso80000.STATIC_PRESSURE),
                r"q_\infty": ("freestream ", _iso80000.DYNAMIC_PRESSURE),
            },
        ),
    ),
    aerospace.SKIN_FRICTION_COEFFICIENT: Symbol(r"C_f"),
    aerospace.LIFT_SLOPE: (
        Equation(
            r"C_{L_\alpha} = \frac{dC_L}{d\alpha}",
            {
                r"C_{L_\alpha}": SELF,
                r"C_L": _iso80000.LIFT_COEFFICIENT,
                r"\alpha": aerospace.ANGLE_OF_ATTACK,
            },
        ),
        Symbol(r"a"),
    ),
    aerospace.CIRCULATION: (
        Equation(
            r"\Gamma = \oint_C \boldsymbol{v} \cdot d\boldsymbol{l}",
            {
                r"\Gamma": SELF,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
                r"d\boldsymbol{l}": _iso80000.LINE_ELEMENT,
                "C": "Closed curve enclosing the body",
            },
        ),
    ),
    # design
    aerospace.WING_LOADING: (
        Wikidata("Q887216"),
        Equation(
            r"W/S = \frac{W}{S}",
            {
                "W/S": SELF,
                "W": aerospace.GROSS,
                "S": aerospace.WING_AREA,
            },
        ),
    ),
    aerospace.THRUST_LOADING: (
        Equation(
            r"T/W = \frac{T}{W}",
            {
                "T/W": SELF,
                "T": _iso80000.THRUST,
                "W": aerospace.GROSS,
            },
        ),
    ),
    # flight dynamics
    aerospace.LOAD_FACTOR: (
        Wikidata("Q1340282"),
        Equation(
            r"n = \frac{L}{W}",
            {"n": SELF, "L": _iso80000.LIFT, "W": _iso80000.WEIGHT},
        ),
    ),
    aerospace.ROLL_RATE: Symbol("p"),
    aerospace.PITCH_RATE: Symbol("q"),
    aerospace.YAW_RATE: Symbol("r"),
    aerospace.BANK_ANGLE: Symbol(r"\phi"),
    aerospace.PITCH_ANGLE: Symbol(r"\theta"),
    aerospace.FLIGHT_PATH_ANGLE: Symbol(r"\gamma"),
    aerospace.PITCHING_MOMENT: Symbol("M"),
    aerospace.ROLLING_MOMENT: (Symbol("L")),
    aerospace.YAWING_MOMENT: Symbol("N"),
    # stability
    aerospace.STATIC_MARGIN: (
        Wikidata("Q7604177"),
        Equation(
            r"K_n = \frac{x_{np} - x_{cg}}{\bar{c}}",
            {
                "K_n": SELF,
                r"x_{np}": aerospace.NEUTRAL_POINT,
                r"x_{cg}": aerospace.CENTER_OF_GRAVITY,
                r"\bar{c}": aerospace.MEAN_AERODYNAMIC_CHORD,
            },
        ),
        Symbol("SM"),
    ),
    aerospace.NEUTRAL_POINT: Symbol(r"x_{np}"),
    aerospace.CENTER_OF_GRAVITY: Symbol(r"x_{cg}"),
    aerospace.HORIZONTAL_TAIL_VOLUME_COEFFICIENT: (
        Equation(
            r"C_{HT} = \frac{L_{HT} S_{HT}}{\bar{c} S_w}",
            {
                r"C_{HT}": SELF,
                r"L_{HT}": ("horizontal ", aerospace.TAIL_MOMENT_ARM),
                r"S_{HT}": ("horizontal ", aerospace.TAIL_AREA),
                r"\bar{c}": aerospace.MEAN_AERODYNAMIC_CHORD,
                r"S_w": aerospace.WING_AREA,
            },
        ),
        Symbol(r"V_{HT}"),
    ),
    aerospace.VERTICAL_TAIL_VOLUME_COEFFICIENT: (
        Equation(
            r"C_{VT} = \frac{L_{VT} S_{VT}}{b S_w}",
            {
                r"C_{VT}": SELF,
                r"L_{VT}": ("vertical ", aerospace.TAIL_MOMENT_ARM),
                r"S_{VT}": ("vertical ", aerospace.TAIL_AREA),
                "b": aerospace.WINGSPAN,
                r"S_w": aerospace.WING_AREA,
            },
        ),
        Symbol(r"V_{VT}"),
    ),
    # performance
    aerospace.TRUE_AIRSPEED: Symbol("V"),
    aerospace.GROUND_SPEED: Symbol("V_g"),
    aerospace.CORNER_SPEED: (
        Equation(
            r"V^* = \sqrt{\frac{2 n_{\max} W}{\rho C_{L,\max} S}}",
            {
                "V^*": SELF,
                r"n_{\max}": ("maximum ", aerospace.LOAD_FACTOR),
                "W": _iso80000.WEIGHT,
                r"\rho": _iso80000.DENSITY,
                r"C_{L,\max}": (
                    "maximum ",
                    _iso80000.LIFT_COEFFICIENT,
                ),
                "S": aerospace.WING_AREA,
            },
        ),
    ),
    aerospace.VERTICAL_RATE: Symbol("VS"),
    aerospace.TURN_RADIUS: (
        Equation(
            r"R = \frac{V^2}{g\sqrt{n^2-1}}",
            {
                "R": SELF,
                "V": aerospace.TRUE_AIRSPEED,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "n": aerospace.LOAD_FACTOR,
            },
            assumptions={"level coordinated turn"},
        ),
    ),
    # propulsion
    aerospace.THRUST_SPECIFIC_FUEL_CONSUMPTION: (Symbol("TSFC")),
    aerospace.ADVANCE_RATIO: (
        Wikidata("Q4686098"),
        Equation(
            r"J = \frac{v}{n D}",
            {
                "J": SELF,
                "v": _iso80000.SPEED,
                "n": _iso80000.ROTATIONAL_FREQUENCY,
                "D": _iso80000.DIAMETER,
            },
        ),
    ),
}
