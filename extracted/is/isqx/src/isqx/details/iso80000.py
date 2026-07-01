"""Definitions are largely derived from Wikidata."""

from .. import _iso80000
from . import SELF, Details, Equation, Symbol, Wikidata

SPACE_AND_TIME: Details = {
    _iso80000.LENGTH: (Wikidata("Q36253"), Symbol("l"), Symbol("L")),
    _iso80000.WIDTH: (Wikidata("Q35059"), Symbol("b"), Symbol("B")),
    _iso80000.HEIGHT: (Wikidata("Q208826"), Symbol("h"), Symbol("H")),
    _iso80000.DEPTH: (Symbol("d"), Symbol("D")),
    _iso80000.ALTITUDE: (Wikidata("Q190200"), Symbol("h"), Symbol("H")),
    _iso80000.ELEVATION: (Wikidata("Q2633778"), Symbol("z"), Symbol("Z")),
    _iso80000.THICKNESS: (
        Wikidata("Q3589038"),
        Symbol("t"),
        Symbol("d"),
        Symbol(r"\delta"),
    ),
    _iso80000.DIAMETER: (Wikidata("Q37221"), Symbol("D"), Symbol("d")),
    _iso80000.RADIUS: (
        Wikidata("Q173817"),
        Symbol("r"),
        Equation(
            r"R = \frac{D}{2}",
            {"R": SELF, "D": _iso80000.DIAMETER},
        ),
    ),
    _iso80000.ARC_LENGTH: (Wikidata("Q670036"), Symbol("s")),
    _iso80000.DISTANCE: (Wikidata("Q126017"), Symbol("d"), Symbol("r")),
    _iso80000.RADIAL_DISTANCE: (
        Wikidata("Q1578234"),
        Symbol(r"\rho_Q"),
        Symbol(r"\rho"),
    ),
    _iso80000.POSITION: (Wikidata("Q192388"), Symbol(r"\boldsymbol{r}")),
    _iso80000.DISPLACEMENT: (
        Wikidata("Q190291"),
        Symbol(r"\Delta\boldsymbol{r}"),
        Equation(
            r"\boldsymbol{s} = \boldsymbol{r}_2 - \boldsymbol{r}_1",
            {
                r"\boldsymbol{s}": SELF,
                r"\boldsymbol{r}_1": _iso80000.INITIAL_POSITION,
                r"\boldsymbol{r}_2": _iso80000.FINAL_POSITION,
            },
        ),
    ),
    _iso80000.CURVATURE: (Wikidata("Q214881"), Symbol(r"\kappa")),
    _iso80000.RADIUS_OF_CURVATURE: (
        Wikidata("Q1136069"),
        Equation(
            r"\rho = \frac{1}{|\kappa|}",
            {r"\rho": SELF, r"\kappa": _iso80000.CURVATURE},
        ),
    ),
    _iso80000.AREA: (Wikidata("Q11500"), Symbol("A"), Symbol("S")),
    _iso80000.SURFACE_ELEMENT: Symbol("dA"),
    _iso80000.CROSS_SECTIONAL_AREA: Symbol("A"),
    _iso80000.VOLUME: (Wikidata("Q39297"), Symbol("V"), Symbol("S")),
    _iso80000.VOLUME_ELEMENT: Symbol("dV"),
    _iso80000.ANGLE: (
        Wikidata("Q1357788"),
        Equation(
            r"\alpha = \frac{s}{r}",
            {r"\alpha": SELF, "s": _iso80000.ARC_LENGTH, "r": _iso80000.RADIUS},
        ),
        Symbol(r"\beta"),
        Symbol(r"\gamma"),
    ),
    _iso80000.ANGULAR_DISPLACEMENT_CCW: (
        Wikidata("Q3305038"),
        Equation(
            r"\vartheta = \frac{s}{r}",
            {
                r"\vartheta": SELF,
                "s": _iso80000.ARC_LENGTH,
                "r": _iso80000.RADIUS,
            },
        ),
        Symbol(r"\varphi"),
    ),
    _iso80000.ANGULAR_DISPLACEMENT_CW: (
        Wikidata("Q3305038"),
        Equation(
            r"\vartheta = \frac{s}{r}",
            {
                r"\vartheta": SELF,
                "s": _iso80000.ARC_LENGTH,
                "r": _iso80000.RADIUS,
            },
        ),
        Symbol(r"\varphi"),
    ),
    _iso80000.PHASE_ANGLE: (
        Wikidata("Q415829"),
        Symbol(r"\varphi"),
        Symbol(r"\phi"),
    ),
    _iso80000.SOLID_ANGLE: (
        Wikidata("Q208476"),
        Equation(
            r"\Omega = \frac{A}{r^2}",
            {r"\Omega": SELF, "A": _iso80000.AREA, "r": _iso80000.RADIUS},
        ),
    ),
    _iso80000.TIME: Symbol("t"),
    _iso80000.DURATION: (
        Wikidata("Q2199864"),
        Equation(
            r"\Delta t = t_2 - t_1",
            {
                r"\Delta t": SELF,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
            },
        ),
    ),
    _iso80000.VELOCITY: (
        Wikidata("Q11465"),
        Equation(
            r"\boldsymbol{v} = \frac{d\boldsymbol{r}}{dt}",
            {
                r"\boldsymbol{v}": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                "t": _iso80000.TIME,
            },
        ),
        Symbol("u"),
        Symbol("v"),
        Symbol("w"),
    ),
    _iso80000.SPEED: (
        Wikidata("Q3711325"),
        Equation(
            r"v = |\boldsymbol{v}|",
            {"v": SELF, r"\boldsymbol{v}": _iso80000.VELOCITY},
        ),
    ),
    _iso80000.ACCELERATION: (
        Wikidata("Q11376"),
        Equation(
            r"\boldsymbol{a} = \frac{d\boldsymbol{v}}{dt}",
            {
                r"\boldsymbol{a}": SELF,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.ANGULAR_VELOCITY_CCW: (
        Wikidata("Q161635"),
        Equation(
            r"\boldsymbol{\omega} = \frac{d\theta}{dt} \boldsymbol{\hat{u}}",
            {
                r"\boldsymbol{\omega}": SELF,
                r"\theta": _iso80000.ANGULAR_DISPLACEMENT_CCW,
                "t": _iso80000.TIME,
                r"\boldsymbol{\hat{u}}": "Axis of rotation",
            },
        ),
    ),
    _iso80000.ANGULAR_VELOCITY_CW: (
        Wikidata("Q161635"),
        Equation(
            r"\boldsymbol{\omega} = \frac{d\theta}{dt} \boldsymbol{\hat{u}}",
            {
                r"\boldsymbol{\omega}": SELF,
                r"\theta": _iso80000.ANGULAR_DISPLACEMENT_CW,
                "t": _iso80000.TIME,
                r"\boldsymbol{\hat{u}}": "Axis of rotation",
            },
        ),
    ),
    _iso80000.ANGULAR_ACCELERATION_CCW: (
        Wikidata("Q186300"),
        Equation(
            r"\boldsymbol{\alpha} = \frac{d\boldsymbol{\omega}}{dt}",
            {
                r"\boldsymbol{\alpha}": SELF,
                r"\boldsymbol{\omega}": _iso80000.ANGULAR_VELOCITY_CCW,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.ANGULAR_ACCELERATION_CW: (
        Wikidata("Q186300"),
        Equation(
            r"\boldsymbol{\alpha} = \frac{d\boldsymbol{\omega}}{dt}",
            {
                r"\boldsymbol{\alpha}": SELF,
                r"\boldsymbol{\omega}": _iso80000.ANGULAR_VELOCITY_CW,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.PERIOD: (Wikidata("Q2642727"), Symbol("T")),
    _iso80000.TIME_CONSTANT: (
        Wikidata("Q1335249"),
        Symbol(r"\tau"),
        Symbol("T"),
    ),
    _iso80000.NUMBER_OF_REVOLUTIONS: (
        Wikidata("Q76435127"),
        Equation(
            r"N = \frac{\theta}{2\pi}",
            {"N": SELF, r"\theta": _iso80000.ANGULAR_DISPLACEMENT_CCW},
        ),
    ),
    _iso80000.FREQUENCY: (
        Wikidata("Q11652"),
        Equation(
            r"f = \frac{1}{T}",
            {"f": SELF, "T": _iso80000.PERIOD},
        ),
        Symbol(r"\nu"),
    ),
    _iso80000.ROTATIONAL_FREQUENCY: (
        Wikidata("Q30338278"),
        Equation(
            r"n = \frac{dN}{dt}",
            {
                "n": SELF,
                "N": _iso80000.NUMBER_OF_REVOLUTIONS,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.ANGULAR_FREQUENCY: (
        Wikidata("Q834020"),
        Equation(
            r"\omega = \frac{d\phi}{dt} = 2\pi f",
            {
                r"\omega": SELF,
                r"\phi": _iso80000.PHASE_ANGLE,
                "t": _iso80000.TIME,
                "f": _iso80000.FREQUENCY,
            },
        ),
    ),
    _iso80000.WAVELENGTH: (Wikidata("Q41364"), Symbol(r"\lambda")),
    _iso80000.WAVENUMBER: (
        Wikidata("Q192510"),
        Equation(
            r"\tilde{\nu} = \frac{1}{\lambda}",
            {r"\tilde{\nu}": SELF, r"\lambda": _iso80000.WAVELENGTH},
        ),
        Symbol(r"\sigma"),
    ),
    _iso80000.WAVEVECTOR: (Wikidata("Q657009"), Symbol(r"\boldsymbol{k}")),
    _iso80000.ANGULAR_WAVENUMBER: (
        Wikidata("Q30338487"),
        Equation(
            r"k = \frac{2\pi}{\lambda}",
            {"k": SELF, r"\lambda": _iso80000.WAVELENGTH},
        ),
    ),
    _iso80000.ANGULAR_WAVEVECTOR: Symbol(r"\boldsymbol{k}"),
    _iso80000.PHASE_SPEED: (
        Wikidata("Q13824"),
        Equation(
            r"c = \frac{\omega}{k}",
            {
                "c": SELF,
                r"\omega": _iso80000.ANGULAR_FREQUENCY,
                "k": _iso80000.ANGULAR_WAVENUMBER,
            },
        ),
        Symbol("v"),
        Symbol(r"c_\varphi"),
        Symbol(r"v_\varphi"),
    ),
    _iso80000.GROUP_SPEED: (
        Wikidata("Q217361"),
        Equation(
            r"c_g = \frac{\partial\omega}{\partial k}",
            {
                "c_g": SELF,
                r"\omega": _iso80000.ANGULAR_FREQUENCY,
                "k": _iso80000.ANGULAR_WAVENUMBER,
            },
        ),
        Symbol("v_g"),
    ),
    _iso80000.DAMPING_COEFFICIENT: (
        Wikidata("Q321828"),
        Equation(
            r"\zeta = \frac{1}{\tau}",
            {r"\zeta": SELF, r"\tau": _iso80000.TIME_CONSTANT},
        ),
        Symbol(r"\delta"),
    ),
    _iso80000.LOGARITHMIC_DECREMENT: (
        Wikidata("Q1399446"),
        Equation(
            r"\delta = \zeta T",
            {
                r"\delta": SELF,
                r"\zeta": _iso80000.DAMPING_COEFFICIENT,
                "T": _iso80000.PERIOD,
            },
        ),
        Symbol(r"\Lambda"),
    ),
    _iso80000.ATTENUATION: (
        Wikidata("Q902086"),
        Equation(
            r"f(x)\propto e^{-\alpha x}",
            {"x": _iso80000.DISTANCE, r"\alpha": SELF},
        ),
    ),
    _iso80000.PHASE_COEFFICIENT: (
        Wikidata("Q32745742"),
        Equation(
            r"f(x)\propto\cos\beta(x-x_0)",
            {"x": _iso80000.DISTANCE, r"\beta": SELF},
        ),
    ),
    _iso80000.PROPAGATION_CONSTANT: (
        Wikidata("Q1434913"),
        Equation(
            r"\gamma = \alpha + i\beta",
            {
                r"\gamma": SELF,
                r"\alpha": _iso80000.ATTENUATION,
                r"\beta": _iso80000.PHASE_COEFFICIENT,
            },
        ),
    ),
}
MECHANICS: Details = {
    _iso80000.MASS: (Wikidata("Q11423"), Symbol(r"m")),
    _iso80000.DENSITY: (
        Wikidata("Q29539"),
        Equation(
            r"\rho(\boldsymbol{r}) = \frac{m}{V}",
            {
                r"\rho": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                "m": _iso80000.MASS,
                "V": _iso80000.VOLUME,
            },
        ),
        Symbol(r"\rho_m"),
    ),
    _iso80000.SPECIFIC_VOLUME: (
        Wikidata("Q683556"),
        Equation(
            r"v = \frac{1}{\rho}",
            {"v": SELF, r"\rho": _iso80000.DENSITY},
        ),
    ),
    _iso80000.RELATIVE_DENSITY: (
        Wikidata("Q11027905"),
        Symbol("d"),
        Equation(
            r"SG = \frac{\rho}{\rho_0}",
            {
                "SG": SELF,
                r"\rho": _iso80000.DENSITY,
                r"\rho_0": _iso80000.REFERENCE_DENSITY,
            },
        ),
    ),
    _iso80000.SURFACE_DENSITY: (
        Wikidata("Q1907514"),
        Equation(
            r"\rho_A(\boldsymbol{r}) = \frac{dm}{dA}",
            {
                r"\rho_A": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                "m": _iso80000.MASS,
                "A": _iso80000.AREA,
            },
        ),
    ),
    _iso80000.LINEAR_DENSITY: (
        Wikidata("Q56298294"),
        Equation(
            r"\lambda_m(\boldsymbol{r}) = \frac{dm}{dL}",
            {
                r"\lambda_m": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                "m": _iso80000.MASS,
                "L": _iso80000.LENGTH,
            },
        ),
        Symbol(r"\rho_l"),
    ),
    _iso80000.MOMENTUM: (
        Wikidata("Q41273"),
        Equation(
            r"\boldsymbol{p} = m\boldsymbol{v}",
            {
                r"\boldsymbol{p}": SELF,
                "m": _iso80000.MASS,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
            },
        ),
    ),
    _iso80000.FORCE: (
        Wikidata("Q11402"),
        Equation(
            r"\boldsymbol{F} = m\boldsymbol{a}",
            {
                r"\boldsymbol{F}": SELF,
                "m": _iso80000.MASS,
                r"\boldsymbol{a}": _iso80000.ACCELERATION,
            },
        ),
    ),
    _iso80000.ACCELERATION_OF_FREE_FALL: (
        Wikidata("Q103982270"),
        Symbol(r"\boldsymbol{g}"),
    ),
    _iso80000.WEIGHT: (
        Wikidata("Q25288"),
        Symbol(r"\boldsymbol{F}_g"),
        Equation(
            r"\boldsymbol{W} = m\boldsymbol{g}",
            {
                r"\boldsymbol{W}": SELF,
                "m": _iso80000.MASS,
                r"\boldsymbol{g}": _iso80000.ACCELERATION_OF_FREE_FALL,
            },
        ),
    ),
    _iso80000.FRICTION: Symbol(r"\boldsymbol{F}_f"),
    _iso80000.STATIC_FRICTION: (
        Wikidata("Q90862568"),
        Symbol(r"\boldsymbol{F}_s"),
    ),
    _iso80000.KINETIC_FRICTION: (
        Wikidata("Q91005629"),
        Symbol(r"\boldsymbol{F}_\mu"),
    ),
    _iso80000.ROLLING_FRICTION: (
        Wikidata("Q914921"),
        Symbol(r"\boldsymbol{F}_{rr}"),
    ),
    _iso80000.DRAG: (
        Wikidata("Q206621"),
        Symbol(r"\boldsymbol{F}_D"),
        Symbol(r"\boldsymbol{D}"),
    ),
    _iso80000.NORMAL_FORCE: Symbol(r"N"),
    _iso80000.TANGENTIAL_FORCE: Symbol(r"F_t"),
    _iso80000.COEFFICIENT_OF_STATIC_FRICTION: (
        Wikidata("Q73695673"),
        Equation(
            r"F_s \le \mu_s N",
            {
                "F_s": _iso80000.STATIC_FRICTION,
                r"\mu_s": SELF,
                "N": _iso80000.NORMAL_FORCE,
            },
        ),
        Symbol(r"f_s"),
    ),
    _iso80000.COEFFICIENT_OF_KINETIC_FRICTION: (
        Wikidata("Q73695445"),
        Equation(
            r"F_k = \mu_k N",
            {
                "F_k": _iso80000.KINETIC_FRICTION,
                r"\mu_k": SELF,
                "N": _iso80000.NORMAL_FORCE,
            },
        ),
        Symbol(r"\mu"),
        Symbol(r"f"),
    ),
    _iso80000.ROLLING_RESISTANCE_FACTOR: (
        Wikidata("Q91738044"),
        Equation(
            r"F_r = C_{rr} N",
            {
                "F_r": _iso80000.ROLLING_FRICTION,
                r"C_{rr}": SELF,
                "N": _iso80000.NORMAL_FORCE,
            },
        ),
    ),
    _iso80000.DRAG_COEFFICIENT: (
        Wikidata("Q1778961"),
        Equation(
            r"F_D = \frac{1}{2} \rho v^2 S C_D",
            {
                "F_D": (_iso80000.DRAG, " on body"),
                r"\rho": (_iso80000.DENSITY, " of fluid"),
                "v": (_iso80000.SPEED, " of body relative to fluid"),
                "S": (
                    "Reference planform ",
                    _iso80000.AREA,
                    " (wetted, frontal, etc.)",
                ),
                r"C_D": SELF,
            },
        ),
        Symbol("c_d", remarks="for 2D flows"),
    ),
    _iso80000.IMPULSE: (
        Wikidata("Q837940"),
        Equation(
            r"\boldsymbol{J} = \int_{t_1}^{t_2} \boldsymbol{F} dt = \boldsymbol{p}_2 - \boldsymbol{p}_1",
            {
                r"\boldsymbol{J}": SELF,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
                r"\boldsymbol{F}": _iso80000.FORCE,
                "t": _iso80000.TIME,
                r"\boldsymbol{p}": _iso80000.MOMENTUM,
            },
        ),
        Symbol(r"\boldsymbol{I}"),
    ),
    _iso80000.ANGULAR_MOMENTUM: (
        Wikidata("Q161254"),
        Equation(
            r"\boldsymbol{L} = \boldsymbol{r} \times \boldsymbol{p}",
            {
                r"\boldsymbol{L}": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                r"\boldsymbol{p}": _iso80000.MOMENTUM,
            },
        ),
    ),
    _iso80000.MOMENT_OF_FORCE: (
        Wikidata("Q17232562"),
        Equation(
            r"\boldsymbol{M} = \boldsymbol{r} \times \boldsymbol{F}",
            {
                r"\boldsymbol{M}": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                r"\boldsymbol{F}": _iso80000.FORCE,
            },
        ),
    ),
    _iso80000.TORQUE: (
        Wikidata("Q48103"),
        Equation(
            r"T = \boldsymbol{M} \cdot \boldsymbol{e}_Q",
            {
                r"T": SELF,
                r"\boldsymbol{M}": _iso80000.MOMENT_OF_FORCE,
                r"\boldsymbol{e}_Q": "Unit vector in the direction of the axis of rotation",
            },
        ),
        Symbol("M_Q"),
    ),
    _iso80000.ANGULAR_IMPULSE: (
        Wikidata("Q73428743"),
        Equation(
            r"\boldsymbol{H} = \int_{t_1}^{t_2} \boldsymbol{M} dt",
            {
                r"\boldsymbol{H}": SELF,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
                r"\boldsymbol{M}": _iso80000.MOMENT_OF_FORCE,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.PRESSURE: (
        Wikidata("Q39552"),
        Equation(
            r"p = \frac{\boldsymbol{e}_n \boldsymbol{F}}{A}",
            {
                "p": SELF,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                r"\boldsymbol{F}": _iso80000.FORCE,
                "A": _iso80000.AREA,
            },
        ),
    ),
    _iso80000.GAUGE_PRESSURE: (
        Wikidata("Q331466"),
        Equation(
            r"p_g = p - p_\mathrm{s}",
            {
                "p_g": SELF,
                "p": _iso80000.PRESSURE,
                r"p_\mathrm{s}": (_iso80000.STATIC_PRESSURE, "(ambient)"),
            },
        ),
        Symbol("p_e"),
    ),
    _iso80000.DYNAMIC_PRESSURE: (
        Equation(
            r"q = \frac{1}{2} \rho v^2",
            {"q": SELF, r"\rho": _iso80000.DENSITY, "v": _iso80000.SPEED},
        ),  # ISO 80000-11
        Equation(
            r"q = p_0 - p_s",
            {
                "q": SELF,
                "p_0": _iso80000.PRESSURE,
                "p_s": _iso80000.STATIC_PRESSURE,
            },
            assumptions={"incompressible flow"},
        ),
    ),
    _iso80000.STRESS_TENSOR: (
        Wikidata("Q13409892"),
        Symbol(r"\boldsymbol{\sigma}"),
    ),
    _iso80000.NORMAL_STRESS: (
        Wikidata("Q11425837"),
        Equation(
            r"\sigma_n = \frac{dF_n}{dA}",
            {
                r"\sigma_n": SELF,
                "F_n": _iso80000.NORMAL_FORCE,
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
    ),
    _iso80000.SHEAR_STRESS: (
        Wikidata("Q657936"),
        Equation(
            r"\tau = \frac{dF_t}{dA}",
            {
                r"\tau": SELF,
                "F_t": _iso80000.TANGENTIAL_FORCE,
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
        Symbol(r"\tau_s"),
    ),
    _iso80000.STRAIN_TENSOR: (
        Wikidata("Q3083131"),
        Symbol(r"\boldsymbol{\varepsilon}"),
    ),
    _iso80000.LINEAR_STRAIN: (
        Wikidata("Q1990546"),
        Equation(
            r"\varepsilon = \frac{\Delta l}{l_0}",
            {r"\varepsilon": SELF, "l": _iso80000.LENGTH},
        ),
    ),
    _iso80000.SHEAR_STRAIN: (
        Wikidata("Q7561704"),
        Equation(
            r"\gamma = \frac{\Delta x}{d}",
            {
                r"\gamma": SELF,
                r"\Delta x": _iso80000.DISPLACEMENT,
                "d": _iso80000.THICKNESS,
            },
        ),
    ),
    _iso80000.VOLUMETRIC_STRAIN: (
        Wikidata("Q73432507"),
        Equation(
            r"\vartheta = \frac{\Delta V}{V_0}",
            {r"\vartheta": SELF, "V": _iso80000.VOLUME},
        ),
    ),
    _iso80000.POISSONS_RATIO: (
        Wikidata("Q190453"),
        Equation(
            r"\nu = -\frac{d\varepsilon_\text{trans}}{d\varepsilon_\text{axial}}",
            {r"\nu": SELF, r"\varepsilon": _iso80000.LINEAR_STRAIN},
        ),
        Symbol(r"\mu"),
    ),
    _iso80000.YOUNGS_MODULUS: (
        Wikidata("Q2091584"),
        Equation(
            r"E = \frac{\sigma}{\varepsilon}",
            {
                "E": SELF,
                r"\sigma": _iso80000.STRESS_TENSOR,
                r"\varepsilon": _iso80000.LINEAR_STRAIN,
            },
        ),
        Symbol("E_m"),
        Symbol("Y"),
    ),
    _iso80000.SHEAR_MODULUS: (
        Wikidata("Q461466"),
        Equation(
            r"G = \frac{\tau_{xy}}{\gamma_{xy}}",
            {
                "G": SELF,
                r"\tau": _iso80000.SHEAR_STRESS,
                r"\gamma": _iso80000.SHEAR_STRAIN,
            },
        ),
    ),
    _iso80000.BULK_MODULUS: (
        Wikidata("Q900371"),
        Equation(
            r"K = -\frac{p}{\vartheta}",
            {
                "K": SELF,
                "p": _iso80000.PRESSURE,
                r"\vartheta": _iso80000.VOLUMETRIC_STRAIN,
            },
        ),
        Symbol("K_m"),
        Symbol("B"),
    ),
    _iso80000.COMPRESSIBILITY: (
        Wikidata("Q8067817"),
        Equation(
            r"\beta = -\frac{1}{V} \frac{\partial V}{\partial p}",
            {r"\beta": SELF, "V": _iso80000.VOLUME, "p": _iso80000.PRESSURE},
        ),
        Symbol(r"\varkappa"),
    ),
    _iso80000.MOMENT_OF_INERTIA: (
        Wikidata("Q4454677"),
        Equation(
            r"\boldsymbol{L} = \boldsymbol{I} \cdot \boldsymbol{\omega}",
            {
                r"\boldsymbol{L}": _iso80000.ANGULAR_MOMENTUM,
                r"\boldsymbol{I}": SELF,
                r"\boldsymbol{\omega}": _iso80000.ANGULAR_VELOCITY_CCW,
            },
        ),
        Symbol(r"\boldsymbol{J}"),
    ),
    _iso80000.SECOND_AXIAL_MOMENT_OF_AREA: (
        Wikidata("Q91405496"),
        Equation(
            r"I_a = \iint_M \rho^2 dA",
            {
                "I_a": SELF,
                "M": "2D domain of the cross-section of a plane",
                r"\rho": _iso80000.RADIAL_DISTANCE,
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
    ),
    _iso80000.SECOND_POLAR_MOMENT_OF_AREA: (
        Wikidata("Q1049636"),
        Equation(
            r"J = \iint_M \rho^2 dA",
            {
                "J": SELF,
                "M": "2D domain of the cross-section of a plane",
                r"\rho": _iso80000.RADIAL_DISTANCE,
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
        Symbol("I_p"),
    ),
    _iso80000.SECTION_MODULUS: (
        Wikidata("Q1930808"),
        Equation(
            r"S = \frac{I_a}{\rho_\mathrm{max}}",
            {
                "S": SELF,
                "I_a": _iso80000.SECOND_AXIAL_MOMENT_OF_AREA,
                r"\rho": _iso80000.RADIAL_DISTANCE,
            },
        ),
        Symbol("W"),
    ),
    _iso80000.DYNAMIC_VISCOSITY: (
        Wikidata("Q15152757"),
        Equation(
            r"\tau_{xz} = \mu \frac{\partial u_x}{\partial y}",
            {
                r"\tau_{xz}": _iso80000.SHEAR_STRESS,
                r"\mu": SELF,
                "u": _iso80000.VELOCITY,
                "y": "Direction perpendicular to the plane of shear",
            },
            assumptions={"newtonian fluid"},
        ),
        Symbol(r"\eta"),
    ),
    _iso80000.KINEMATIC_VISCOSITY: (
        Wikidata("Q15106259"),
        Equation(
            r"\nu = \frac{\mu}{\rho}",
            {
                r"\nu": SELF,
                r"\mu": _iso80000.DYNAMIC_VISCOSITY,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.SURFACE_TENSION: (
        Wikidata("Q170749"),
        Equation(
            r"\gamma = \frac{F}{L}",
            {r"\gamma": SELF, "F": _iso80000.FORCE, "L": _iso80000.LENGTH},
        ),
        Symbol(r"\sigma"),
    ),
    _iso80000.ENERGY: (Wikidata("Q11379"), Symbol(r"E")),
    _iso80000.POWER: (
        Wikidata("Q80806956"),
        Equation(
            r"P = \boldsymbol{F}\cdot\boldsymbol{v}",
            {
                "P": SELF,
                r"\boldsymbol{F}": _iso80000.FORCE,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
            },
        ),
    ),
    _iso80000.POTENTIAL_ENERGY: (
        Wikidata("Q155640"),
        Symbol(r"V"),
        Symbol("E_p"),
    ),
    _iso80000.KINETIC_ENERGY: (
        Wikidata("Q46276"),
        Equation(
            r"T = \frac{1}{2} mv^2",
            {"T": SELF, "m": _iso80000.MASS, "v": _iso80000.SPEED},
            assumptions={"classical mechanics", "point object", "non-rotating"},
        ),
        Symbol("E_k"),
    ),
    _iso80000.MECHANICAL_ENERGY: (
        Wikidata("Q184550"),
        Equation(
            r"E = T + V",
            {
                "E": SELF,
                "T": _iso80000.KINETIC_ENERGY,
                "V": _iso80000.POTENTIAL_ENERGY,
            },
        ),
        Symbol("W"),
    ),
    _iso80000.LINE_ELEMENT: Symbol(r"d\boldsymbol{s}"),
    _iso80000.WORK: (
        Wikidata("Q42213"),
        Equation(
            r"W = \int_C \boldsymbol{F} \cdot d\boldsymbol{s}",
            {
                "W": SELF,
                r"\boldsymbol{F}": _iso80000.FORCE,
                r"d\boldsymbol{s}": _iso80000.LINE_ELEMENT,
                "C": "Continuous curve",
            },
        ),
        Symbol("A"),
    ),
    _iso80000.MECHANICAL_EFFICIENCY: (
        Wikidata("Q2628085"),
        Equation(
            r"\eta = \frac{P_{\mathrm{out}}}{P_{\mathrm{in}}}",
            {r"\eta": SELF, "P": _iso80000.POWER},
        ),
    ),
    _iso80000.MASS_FLUX: (
        Wikidata("Q3265048"),
        Equation(
            r"\boldsymbol{j}_m = \rho \boldsymbol{v}",
            {
                r"\boldsymbol{j}_m": SELF,
                r"\rho": _iso80000.DENSITY,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
            },
        ),
    ),
    _iso80000.MASS_FLOW_RATE: (
        Wikidata("Q1366187"),
        Equation(
            r"\dot{m} = \frac{dm}{dt} = \iint_A \boldsymbol{j}_m \cdot \boldsymbol{e}_n dA",
            {
                r"\dot{m}": SELF,
                "m": _iso80000.MASS,
                "t": _iso80000.TIME,
                "A": _iso80000.AREA,
                r"\boldsymbol{j}_m": _iso80000.MASS_FLUX,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
        Symbol(r"q_m"),
    ),
    _iso80000.VOLUME_FLOW_RATE: (
        Wikidata("Q1134348"),
        Equation(
            r"\dot{V} = \frac{dV}{dt} = \iint_A \boldsymbol{v} \cdot \boldsymbol{e}_n dA",
            {
                r"\dot{V}": SELF,
                "V": _iso80000.VOLUME,
                "t": _iso80000.TIME,
                "A": _iso80000.AREA,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
        Symbol(r"q_V"),
    ),
    _iso80000.ACTION: (
        Wikidata("Q846785"),
        Equation(
            r"\mathcal{S} = \int_{t_1}^{t_2} E dt",
            {
                r"\mathcal{S}": SELF,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
                "E": _iso80000.ENERGY,
                "t": _iso80000.TIME,
            },
        ),
        Symbol(r"S"),
    ),
}
THERMODYNAMICS: Details = {
    _iso80000.TEMPERATURE: (
        Wikidata("Q264647"),
        Symbol("T"),
        Symbol(r"\theta"),
    ),
    _iso80000.SURFACE_TEMPERATURE: Symbol("T_s"),
    _iso80000.REFERENCE_TEMPERATURE: Symbol("T_r"),
    _iso80000.HOT_RESERVOIR_TEMPERATURE: Symbol("T_H"),
    _iso80000.COLD_RESERVOIR_TEMPERATURE: Symbol("T_C"),
    _iso80000.TEMPERATURE_DIFFERENCE: Symbol(r"\Delta T"),
    _iso80000.LINEAR_EXPANSION_COEFFICIENT: (
        Wikidata("Q74760821"),
        Equation(
            r"\alpha_l = \frac{1}{L} \frac{dL}{dT}",
            {
                r"\alpha_l": SELF,
                "L": _iso80000.LENGTH,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.VOLUMETRIC_EXPANSION_COEFFICIENT: (
        Wikidata("Q74761076"),
        Equation(
            r"\alpha_V = \frac{1}{V} \frac{dV}{dT}",
            {
                r"\alpha_V": SELF,
                "V": _iso80000.VOLUME,
                "T": _iso80000.TEMPERATURE,
            },
        ),
        Symbol(r"\gamma"),
    ),
    _iso80000._RELATIVE_PRESSURE_COEFFICIENT: (
        Wikidata("Q74761852"),
        Equation(
            r"\alpha_p = \frac{1}{p} \left(\frac{\partial p}{\partial T}\right)_V",
            {
                r"\alpha_p": SELF,
                "p": _iso80000.PRESSURE,
                "T": _iso80000.TEMPERATURE,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000._PRESSURE_COEFFICIENT: (
        Wikidata("Q74762732"),
        Equation(
            r"\beta = \left(\frac{\partial p}{\partial T}\right)_V",
            {
                r"\beta": SELF,
                "p": _iso80000.PRESSURE,
                "T": _iso80000.TEMPERATURE,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.ISOTHERMAL_COMPRESSIBILITY: (
        Wikidata("Q2990696"),
        Equation(
            r"\beta_T = -\frac{1}{V} \left(\frac{\partial V}{\partial p}\right)_T",
            {
                r"\beta_T": SELF,
                "V": _iso80000.VOLUME,
                "p": _iso80000.PRESSURE,
                "T": _iso80000.TEMPERATURE,
            },
        ),
        Symbol(r"\varkappa_T"),
        Symbol(r"\kappa_T"),
    ),
    _iso80000.ISENTROPIC_COMPRESSIBILITY: (
        Wikidata("Q2990695"),
        Equation(
            r"\beta_S = -\frac{1}{V} \left(\frac{\partial V}{\partial p}\right)_S",
            {
                r"\beta_S": SELF,
                "V": _iso80000.VOLUME,
                "p": _iso80000.PRESSURE,
                "S": _iso80000.ENTROPY,
            },
        ),
        Symbol(r"\varkappa_S"),
        Symbol(r"\kappa_S"),
    ),
    _iso80000.WORK_BY_SYSTEM: Symbol("W"),
    _iso80000.WORK_ON_SYSTEM: Symbol("W"),
    _iso80000.HEAT: (Wikidata("Q44432"), Symbol("Q")),
    _iso80000.HEAT_TO_SYSTEM: Symbol("Q"),
    _iso80000.INEXACT_DIFFERENTIAL_HEAT: Symbol(r"\delta Q"),
    _iso80000.LATENT_HEAT: (Wikidata("Q207721"), Symbol("L"), Symbol("Q")),
    _iso80000.SPECIFIC_LATENT_HEAT: Symbol("l"),  # todo
    _iso80000.MOLAR_LATENT_HEAT: Symbol("L_m"),  # todo
    _iso80000.HEAT_FLOW_RATE: (Wikidata("Q12160631"), Symbol(r"\dot{Q}")),
    _iso80000.HEAT_FLUX: (
        Wikidata("Q1478382"),
        Equation(
            r"q = \frac{\dot{Q}}{A}",
            {
                "q": SELF,
                r"\dot{Q}": _iso80000.HEAT_FLOW_RATE,
                "A": _iso80000.AREA,
            },
        ),
        Symbol(r"\varphi"),
    ),
    _iso80000.THERMAL_CONDUCTIVITY: (
        Wikidata("Q487005"),
        Equation(
            r"\boldsymbol{q} = -\kappa \nabla T",
            {
                r"\boldsymbol{q}": _iso80000.HEAT_FLUX,
                r"\kappa": SELF,
                "T": _iso80000.TEMPERATURE,
            },
        ),
        Symbol(r"\lambda"),
        Symbol(r"\varkappa"),
    ),
    _iso80000.HEAT_TRANSFER_COEFFICIENT: (
        Wikidata("Q634340"),
        Equation(
            r"h = \frac{|\boldsymbol{q}|}{T_s - T_r}",
            {
                "h": SELF,
                r"\boldsymbol{q}": _iso80000.HEAT_FLUX,
                r"T_s": _iso80000.SURFACE_TEMPERATURE,
                r"T_r": _iso80000.REFERENCE_TEMPERATURE,
            },
        ),
        Symbol(r"\alpha"),
        Symbol("K"),
        Symbol("k"),
    ),
    _iso80000.THERMAL_INSULANCE: (
        Wikidata("Q2596212"),
        Symbol("M"),
        Equation(
            r"R_\mathrm{si} = \frac{1}{h}",
            {r"R_\mathrm{si}": SELF, "h": _iso80000.HEAT_TRANSFER_COEFFICIENT},
        ),
    ),
    _iso80000.THERMAL_RESISTANCE: (
        Wikidata("Q899628"),
        Equation(
            r"R = \frac{\Delta T}{\dot{Q}}",
            {
                "R": SELF,
                r"\Delta T": _iso80000.TEMPERATURE_DIFFERENCE,
                r"\dot{Q}": _iso80000.HEAT_FLOW_RATE,
            },
        ),
    ),
    _iso80000.THERMAL_CONDUCTANCE: (
        Wikidata("Q17176562"),
        Equation(
            r"G = \frac{1}{R}",
            {"G": SELF, "R": _iso80000.THERMAL_RESISTANCE},
        ),
        Symbol("H"),
    ),
    _iso80000.THERMAL_DIFFUSIVITY: (
        Wikidata("Q3381809"),
        Symbol("a"),
        Equation(
            r"\alpha = \frac{\kappa}{\rho c_p}",
            {
                r"\alpha": SELF,
                r"\kappa": _iso80000.THERMAL_CONDUCTIVITY,
                r"\rho": _iso80000.DENSITY,
                "c_p": _iso80000.SPECIFIC_HEAT_CAPACITY_P,
            },
        ),
    ),
    _iso80000.HEAT_CAPACITY: (
        Wikidata("Q179388"),
        Equation(
            r"C = \frac{\delta Q}{dT}",
            {
                "C": SELF,
                r"\delta Q": _iso80000.INEXACT_DIFFERENTIAL_HEAT,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.HEAT_CAPACITY_P: Symbol("C_p"),
    _iso80000.HEAT_CAPACITY_V: Symbol("C_v"),
    _iso80000.SPECIFIC_HEAT_CAPACITY: (
        Wikidata("Q487756"),
        Equation(
            r"c = \frac{C}{m}",
            {"c": SELF, "C": _iso80000.HEAT_CAPACITY, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.SPECIFIC_HEAT_CAPACITY_P: (Wikidata("Q75774282"), Symbol("c_p")),
    _iso80000.SPECIFIC_HEAT_CAPACITY_V: (Wikidata("Q75774757"), Symbol("c_v")),
    _iso80000.SPECIFIC_HEAT_CAPACITY_SAT: (
        Wikidata("Q75775005"),
        Symbol(r"c_\text{sat}"),
    ),
    _iso80000.HEAT_CAPACITY_RATIO: (
        Wikidata("Q503869"),
        Equation(
            r"\gamma = \frac{c_p}{c_v} = \frac{C_p}{C_v}",
            {
                r"\gamma": SELF,
                "c_p": _iso80000.SPECIFIC_HEAT_CAPACITY_P,
                "c_v": _iso80000.SPECIFIC_HEAT_CAPACITY_V,
                "C_p": _iso80000.HEAT_CAPACITY_P,
                "C_v": _iso80000.HEAT_CAPACITY_V,
            },
        ),
        Symbol(r"\kappa"),
    ),
    _iso80000.ISENTROPIC_EXPONENT: (
        Wikidata("Q75775739"),
        Equation(
            r"\varkappa = -\frac{V}{p} \left(\frac{\partial p}{\partial V}\right)_S",
            {
                r"\varkappa": SELF,
                "V": _iso80000.VOLUME,
                "p": _iso80000.PRESSURE,
                "S": _iso80000.ENTROPY,
            },
        ),
    ),
    _iso80000.ENTROPY: (
        Wikidata("Q45003"),
        Equation(
            r"S = k_B \ln W",
            {
                "S": SELF,
                "k_B": _iso80000.CONST_BOLTZMANN,
                "W": _iso80000.MULTIPLICITY,
            },
        ),
        Equation(
            r"dS = \frac{\delta Q_\text{rev}}{T}",
            {
                "S": SELF,
                r"\delta Q": _iso80000.INEXACT_DIFFERENTIAL_HEAT,
                "T": _iso80000.TEMPERATURE,
            },
            assumptions={"reversible process"},
        ),
    ),
    _iso80000.SPECIFIC_ENTROPY: (
        Wikidata("Q69423705"),
        Equation(
            r"s = \frac{S}{m}",
            {"s": SELF, "S": _iso80000.ENTROPY, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.INTERNAL_ENERGY: (
        Wikidata("Q180241"),
        Equation(
            r"\Delta U = Q - W",
            {
                "U": SELF,
                "Q": _iso80000.HEAT_TO_SYSTEM,
                "W": _iso80000.WORK_BY_SYSTEM,
            },
        ),
    ),
    _iso80000.ENTHALPY: (
        Wikidata("Q161064"),
        Equation(
            r"H = U + pV",
            {
                "H": SELF,
                "U": _iso80000.INTERNAL_ENERGY,
                "p": _iso80000.PRESSURE,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.HELMHOLTZ_ENERGY: (
        Wikidata("Q865821"),
        Equation(
            r"A = U - TS",
            {
                "A": SELF,
                "U": _iso80000.INTERNAL_ENERGY,
                "T": _iso80000.TEMPERATURE,
                "S": _iso80000.ENTROPY,
            },
        ),
        Equation(
            r"A = -k_B T \ln Z",
            {
                "A": SELF,
                "k_B": _iso80000.CONST_BOLTZMANN,
                "T": _iso80000.TEMPERATURE,
                "Z": _iso80000.CANONICAL_PARTITION_FUNCTION,
            },
        ),  # ISO 80000-9
        Equation(
            r"A - \sum_\mathrm{B}\mu_\mathrm{B} n_\mathrm{B} = -k_B T \ln \Xi",
            {
                "A": SELF,
                "k_B": _iso80000.CONST_BOLTZMANN,
                r"\mathrm{B}": "Substance",
                "T": _iso80000.TEMPERATURE,
                r"\Xi": _iso80000.GRAND_CANONICAL_PARTITION_FUNCTION,
                r"\mu": _iso80000.CHEMICAL_POTENTIAL,
                r"n": _iso80000.AMOUNT_OF_SUBSTANCE,
            },
        ),  # ISO 80000-9
        Symbol("F"),
    ),
    _iso80000.GIBBS_ENERGY: (
        Wikidata("Q334631"),
        Equation(
            r"G = H - TS",
            {
                "G": SELF,
                "H": _iso80000.ENTHALPY,
                "T": _iso80000.TEMPERATURE,
                "S": _iso80000.ENTROPY,
            },
        ),
    ),
    _iso80000.SPECIFIC_ENERGY: (
        Wikidata("Q3023293"),
        Equation(
            r"e = \frac{E}{m}",
            {"e": SELF, "E": _iso80000.ENERGY, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.SPECIFIC_INTERNAL_ENERGY: (
        Wikidata("Q76357367"),
        Equation(
            r"u = \frac{U}{m}",
            {"u": SELF, "U": _iso80000.INTERNAL_ENERGY, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.SPECIFIC_ENTHALPY: (
        Wikidata("Q21572993"),
        Equation(
            r"h = \frac{H}{m}",
            {"h": SELF, "H": _iso80000.ENTHALPY, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.SPECIFIC_HELMHOLTZ_ENERGY: (
        Wikidata("Q76359554"),
        Equation(
            r"a = \frac{A}{m}",
            {"a": SELF, "A": _iso80000.HELMHOLTZ_ENERGY, "m": _iso80000.MASS},
        ),
        Symbol("f"),
    ),
    _iso80000.SPECIFIC_GIBBS_ENERGY: (
        Wikidata("Q76360636"),
        Equation(
            r"g = \frac{G}{m}",
            {"g": SELF, "G": _iso80000.GIBBS_ENERGY, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.MASSIEU_FUNCTION: (
        Wikidata("Q3077625"),
        Equation(
            r"J = -\frac{A}{T}",
            {
                "J": SELF,
                "A": _iso80000.HELMHOLTZ_ENERGY,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.PLANCK_FUNCTION: (
        Wikidata("Q76364998"),
        Equation(
            r"Y = -\frac{G}{T}",
            {
                "Y": SELF,
                "G": _iso80000.GIBBS_ENERGY,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.JOULE_THOMSON_COEFFICIENT: (
        Wikidata("Q93946998"),
        Equation(
            r"\mu_\mathrm{JT} = \left(\frac{\partial T}{\partial p}\right)_H",
            {
                r"\mu_\mathrm{JT}": SELF,
                "T": _iso80000.TEMPERATURE,
                "p": _iso80000.PRESSURE,
                "H": _iso80000.ENTHALPY,
            },
        ),
    ),
    _iso80000.THERMAL_EFFICIENCY: (
        Wikidata("Q1452104"),
        Equation(
            r"\eta_\mathrm{th} = \frac{W}{Q}",
            {
                r"\eta_\mathrm{th}": SELF,
                "W": _iso80000.WORK_BY_SYSTEM,
                "Q": _iso80000.HEAT_TO_SYSTEM,
            },
        ),
        Symbol(r"\eta"),
    ),
    _iso80000.CARNOT_EFFICIENCY: (
        Wikidata("Q93949862"),
        Equation(
            r"(\eta_\text{th})_\mathrm{max} = 1 - \frac{T_C}{T_H}",
            {
                r"(\eta_\text{th})_\mathrm{max}": SELF,
                "T_C": _iso80000.COLD_RESERVOIR_TEMPERATURE,
                "T_H": _iso80000.HOT_RESERVOIR_TEMPERATURE,
            },
        ),
        Symbol(r"\eta_\mathrm{max}"),
    ),
    _iso80000.MASS_OF_SINGLE_PARTICLE: Symbol("m"),
    _iso80000.SPECIFIC_GAS_CONSTANT: (
        Wikidata("Q94372268"),
        Equation(
            r"R = \frac{k_B}{m}",
            {
                "R": SELF,
                "k_B": _iso80000.CONST_BOLTZMANN,
                "m": _iso80000.MASS_OF_SINGLE_PARTICLE,
            },
        ),
        Symbol("R_s"),
    ),
    _iso80000.MASS_CONCENTRATION: (
        Wikidata("Q589446"),
        Equation(
            r"\rho_\mathrm{X} = \frac{m_\mathrm{X}}{V}",
            {
                r"\rho": SELF,
                "m": _iso80000.MASS,
                "V": _iso80000.VOLUME,
                r"\mathrm{X}": "Substance",
            },
        ),
        Symbol(r"\gamma_X"),
    ),
    _iso80000.WATER_VAPOUR_MASS: Symbol("m"),
    _iso80000.WATER_MASS_CONCENTRATION: (
        Wikidata("Q76378758"),
        Equation(
            r"w = \frac{m}{V}",
            {
                "w": SELF,
                "m": _iso80000.WATER_VAPOUR_MASS,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.WATER_VAPOUR_MASS_CONCENTRATION: (
        Wikidata("Q76378808"),
        Equation(
            r"v = \frac{m}{V}",
            {
                "v": SELF,
                "m": _iso80000.WATER_VAPOUR_MASS,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.WATER_VAPOUR_MASS_CONCENTRATION_AT_SATURATION: Symbol(
        r"v_\mathrm{sat}"
    ),
    _iso80000.DRY_MATTER_MASS: Symbol("m_d"),
    _iso80000.WATER_TO_DRY_MATTER_MASS_RATIO: (
        Wikidata("Q76378860"),
        Equation(
            r"u = \frac{m}{m_d}",
            {
                "u": SELF,
                "m": _iso80000.WATER_VAPOUR_MASS,
                "m_d": _iso80000.DRY_MATTER_MASS,
            },
        ),
    ),
    _iso80000.DRY_GAS_MASS: Symbol("m_d"),
    _iso80000.WATER_VAPOUR_TO_DRY_GAS_MASS_RATIO: (
        Wikidata("Q17232415"),
        Equation(
            r"r = \frac{m}{m_d}",
            {
                "r": SELF,
                "m": _iso80000.WATER_VAPOUR_MASS,
                "m_d": _iso80000.DRY_GAS_MASS,
            },
        ),
        Symbol("x"),
    ),
    _iso80000.WATER_VAPOUR_TO_DRY_GAS_MASS_RATIO_AT_SATURATION: Symbol(
        r"r_\mathrm{sat}"
    ),
    _iso80000.MASS_FRACTION: (
        Wikidata("Q899138"),
        Equation(
            r"w_\mathrm{X} = \frac{m_\mathrm{X}}{m_\text{total}}",
            {"w": SELF, "m": _iso80000.MASS, r"\mathrm{X}": "Substance"},
        ),
    ),
    _iso80000.WATER_MASS_FRACTION: (
        Wikidata("Q76379025"),
        Equation(
            r"w_{\mathrm{H}_2\mathrm{O}} = \frac{u}{1 + u}",
            {
                r"w_{\mathrm{H}_2\mathrm{O}}": SELF,
                "u": _iso80000.WATER_TO_DRY_MATTER_MASS_RATIO,
            },
        ),
    ),
    _iso80000.DRY_MATTER_MASS_FRACTION: (
        Wikidata("Q76379189"),
        Equation(
            r"w_d = 1 - w_{\mathrm{H}_2\mathrm{O}}",
            {
                r"w_d": SELF,
                r"w_{\mathrm{H}_2\mathrm{O}}": _iso80000.MASS_FRACTION,
            },
        ),
    ),
    _iso80000.PARTIAL_PRESSURE: (Wikidata("Q27165"), Symbol("p_X")),
    _iso80000.WATER_VAPOUR_PARTIAL_PRESSURE: Symbol(r"p_{H_2O}"),
    _iso80000.SATURATION_WATER_VAPOUR_PARTIAL_PRESSURE: Symbol(
        r"p_\mathrm{sat}"
    ),
    _iso80000.RELATIVE_HUMIDITY: (
        Wikidata("Q2499617"),
        Equation(
            r"\mathrm{RH} = \frac{p}{p_\mathrm{sat}}",
            {
                r"\mathrm{RH}": SELF,
                "p": _iso80000.WATER_VAPOUR_PARTIAL_PRESSURE,
                r"p_\mathrm{sat}": _iso80000.SATURATION_WATER_VAPOUR_PARTIAL_PRESSURE,
            },
        ),
        Symbol(r"\phi"),
    ),
    _iso80000.RELATIVE_MASS_CONCENTRATION_VAPOUR: (
        Wikidata("Q76379357"),
        Equation(
            r"\phi = \frac{v}{v_\mathrm{sat}}",
            {
                r"\phi": SELF,
                "v": _iso80000.WATER_VAPOUR_MASS_CONCENTRATION,
                r"v_\mathrm{sat}": _iso80000.WATER_VAPOUR_MASS_CONCENTRATION_AT_SATURATION,
            },
        ),
    ),
    _iso80000.RELATIVE_MASS_RATIO_VAPOUR: (
        Wikidata("Q76379414"),
        Equation(
            r"\psi = \frac{r}{r_\mathrm{sat}}",
            {
                r"\psi": SELF,
                "r": _iso80000.WATER_VAPOUR_TO_DRY_GAS_MASS_RATIO,
                r"r_\mathrm{sat}": _iso80000.WATER_VAPOUR_TO_DRY_GAS_MASS_RATIO_AT_SATURATION,
            },
        ),
    ),
    _iso80000.DEW_POINT: (Wikidata("Q178828"), Symbol("T_d")),
}
ELECTROMAGNETISM: Details = {
    _iso80000.CONST_ELEMENTARY_CHARGE: (Wikidata("Q2101"), Symbol("e")),
    _iso80000.CONST_PERMITTIVITY_VACUUM: (
        Wikidata("Q6158"),
        Symbol(r"\varepsilon_0"),
    ),
    _iso80000.CURRENT: (
        Wikidata("Q29996"),
        Equation(
            r"I = \frac{dq}{dt}",
            {"I": SELF, "q": _iso80000.ELECTRIC_CHARGE, "t": _iso80000.TIME},
        ),
        Symbol("i"),
    ),
    _iso80000.INSTANTANEOUS_CURRENT: Symbol("i(t)"),
    _iso80000.RMS_CURRENT: Symbol(r"I_\mathrm{rms}"),
    _iso80000.ELECTRIC_CHARGE: (Wikidata("Q1111"), Symbol("Q"), Symbol("q")),
    _iso80000.CHARGE_DENSITY: (
        Wikidata("Q69425629"),
        Equation(
            r"\rho(\boldsymbol{r}) = \frac{dq}{dV}",
            {
                r"\rho": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                "q": _iso80000.ELECTRIC_CHARGE,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.SURFACE_CHARGE_DENSITY: (
        Wikidata("Q12799324"),
        Equation(
            r"\sigma(\boldsymbol{r}) = \frac{dq}{dA}",
            {
                r"\sigma": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                "q": _iso80000.ELECTRIC_CHARGE,
                "A": _iso80000.AREA,
            },
        ),
    ),
    _iso80000.LINEAR_CHARGE_DENSITY: (
        Wikidata("Q77267838"),
        Equation(
            r"\lambda(\boldsymbol{r}) = \frac{dq}{dl}",
            {
                r"\lambda": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                "q": _iso80000.ELECTRIC_CHARGE,
                "l": _iso80000.LENGTH,
            },
        ),
        Symbol(r"\tau"),
    ),
    _iso80000.ELECTRIC_DIPOLE_MOMENT: (
        Wikidata("Q735135"),
        Equation(
            r"\boldsymbol{p} = q(r_+ - r_-)",
            {
                r"\boldsymbol{p}": SELF,
                "q": _iso80000.ELECTRIC_CHARGE,
                "r": _iso80000.POSITION,
            },
        ),
    ),
    _iso80000.POLARIZATION_DENSITY: (
        Wikidata("Q1050425"),
        Equation(
            r"\boldsymbol{P}(\boldsymbol{r}) = \frac{d\boldsymbol{p}}{dV}",
            {
                r"\boldsymbol{P}": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                r"\boldsymbol{p}": _iso80000.ELECTRIC_DIPOLE_MOMENT,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.CURRENT_DENSITY: (
        Wikidata("Q234072"),
        Equation(
            r"\boldsymbol{J}(\boldsymbol{r}) = \rho \boldsymbol{v}",
            {
                r"\boldsymbol{J}": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                r"\rho": _iso80000.CHARGE_DENSITY,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
            },
        ),
        Equation(
            r"I = \int_S \boldsymbol{J} \cdot \boldsymbol{e}_n dA",
            {
                "I": _iso80000.CURRENT,
                r"\boldsymbol{J}": SELF,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "S": "Surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
    ),
    _iso80000.LINEAR_CURRENT_DENSITY: (
        Wikidata("Q2356741"),
        Equation(
            r"\boldsymbol{J}_s = \sigma \boldsymbol{v}",
            {
                r"\boldsymbol{J}_s": SELF,
                r"\sigma": _iso80000.SURFACE_CHARGE_DENSITY,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
            },
        ),
    ),
    _iso80000.ELECTRIC_FIELD_STRENGTH: (
        Wikidata("Q20989"),
        Equation(
            r"\boldsymbol{E}(\boldsymbol{r}) = \frac{\boldsymbol{F}}{q}",
            {
                r"\boldsymbol{E}": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                r"\boldsymbol{F}": _iso80000.FORCE,
                "q": _iso80000.ELECTRIC_CHARGE,
            },
        ),
    ),
    _iso80000.ELECTRIC_POTENTIAL: (
        Wikidata("Q55451"),
        Equation(
            r"-\nabla V = \boldsymbol{E} + \frac{\partial \boldsymbol{A}}{\partial t}",
            {
                "V": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\boldsymbol{A}": _iso80000.MAGNETIC_VECTOR_POTENTIAL,
                "t": _iso80000.TIME,
            },
        ),
        Symbol(r"\varphi"),
    ),
    _iso80000.ELECTRIC_POTENTIAL_DIFFERENCE: (
        Wikidata("Q77597807"),
        Equation(
            r"V_\mathrm{ab} = V_\mathrm{a} - V_\mathrm{b}",
            {r"V_\mathrm{ab}": SELF, "V": _iso80000.ELECTRIC_POTENTIAL},
        ),
        Equation(
            r"V_\mathrm{ab} = \int_C \left(\boldsymbol{E} + \frac{\partial \boldsymbol{A}}{\partial t}\right) \cdot d\boldsymbol{r}",
            {
                r"V_\mathrm{ab}": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\boldsymbol{A}": _iso80000.MAGNETIC_VECTOR_POTENTIAL,
                "t": _iso80000.TIME,
                r"d\boldsymbol{r}": _iso80000.LINE_ELEMENT,
            },
        ),
    ),
    _iso80000.VOLTAGE: (
        Wikidata("Q118309876"),
        Equation(
            r"U = V_\mathrm{ab}",
            {
                "U": SELF,
                r"V_\mathrm{ab}": _iso80000.ELECTRIC_POTENTIAL_DIFFERENCE,
            },
            assumptions={"conductor"},
        ),
        Symbol("u"),
    ),
    _iso80000.INDUCED_VOLTAGE: (
        Wikidata("Q1097002"),
        Equation(
            r"\mathcal{E} = -\frac{d}{dt}\int_C \boldsymbol{A} \cdot d\boldsymbol{r}",
            {
                r"\mathcal{E}": SELF,
                "t": _iso80000.TIME,
                r"\boldsymbol{A}": _iso80000.PROTOFLUX,
                r"d\boldsymbol{r}": _iso80000.LINE_ELEMENT,
            },
        ),
        Equation(
            r"\mathcal{E} = -\frac{d\Phi_B}{dt}",
            {
                r"\mathcal{E}": SELF,
                "t": _iso80000.TIME,
                r"\Phi_B": _iso80000.MAGNETIC_FLUX,
            },
            assumptions={"closed loop"},
        ),
        Symbol("U_i"),
    ),
    _iso80000.INSTANTANEOUS_VOLTAGE: Symbol("u(t)"),
    _iso80000.RMS_VOLTAGE: Symbol(r"U_\mathrm{rms}"),
    _iso80000.ELECTRIC_FLUX_DENSITY: (
        Wikidata("Q371907"),
        Equation(
            r"\boldsymbol{D} = \varepsilon_0 \boldsymbol{E} + \boldsymbol{P}",
            {
                r"\boldsymbol{D}": SELF,
                r"\varepsilon_0": _iso80000.CONST_PERMITTIVITY_VACUUM,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\boldsymbol{P}": _iso80000.POLARIZATION_DENSITY,
            },
        ),
        Equation(
            r"\nabla \cdot \boldsymbol{D} = \rho",
            {r"\boldsymbol{D}": SELF, r"\rho": _iso80000.CHARGE_DENSITY},
        ),
    ),
    _iso80000.CAPACITANCE: (
        Wikidata("Q164399"),
        Equation(
            r"C = \frac{q}{U}",
            {"C": SELF, "q": _iso80000.ELECTRIC_CHARGE, "U": _iso80000.VOLTAGE},
        ),
    ),
    _iso80000.PERMITTIVITY: (
        Wikidata("Q211569"),
        Equation(
            r"\boldsymbol{D} = \varepsilon \boldsymbol{E}",
            {
                r"\boldsymbol{D}": _iso80000.ELECTRIC_FLUX_DENSITY,
                r"\varepsilon": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
            },
        ),
    ),
    _iso80000.RELATIVE_PERMITTIVITY: (
        Wikidata("Q4027242"),
        Equation(
            r"\varepsilon_r = \frac{\varepsilon}{\varepsilon_0}",
            {
                r"\varepsilon_r": SELF,
                r"\varepsilon": _iso80000.PERMITTIVITY,
                r"\varepsilon_0": _iso80000.CONST_PERMITTIVITY_VACUUM,
            },
        ),
    ),
    _iso80000.ELECTRIC_SUSCEPTIBILITY: (
        Wikidata("Q598305"),
        Symbol(r"\chi"),
        Equation(
            r"\boldsymbol{P} = \varepsilon_0 \chi_\mathrm{e} \boldsymbol{E}",
            {
                r"\boldsymbol{P}": _iso80000.POLARIZATION_DENSITY,
                r"\varepsilon_0": _iso80000.CONST_PERMITTIVITY_VACUUM,
                r"\chi_\mathrm{e}": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
            },
        ),
    ),
    _iso80000.ELECTRIC_FLUX: (
        Wikidata("Q501267"),
        Symbol(r"\Psi"),
        Equation(
            r"\Phi_E = \iint_S \boldsymbol{D} \cdot \boldsymbol{e}_n dA",
            {
                r"\Phi_E": SELF,
                r"\boldsymbol{D}": _iso80000.ELECTRIC_FLUX_DENSITY,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
    ),
    _iso80000.DISPLACEMENT_CURRENT_DENSITY: (
        Wikidata("Q77614612"),
        Equation(
            r"\boldsymbol{J}_D = \frac{\partial \boldsymbol{D}}{\partial t}",
            {
                r"\boldsymbol{J}_D": SELF,
                r"\boldsymbol{D}": _iso80000.ELECTRIC_FLUX_DENSITY,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.DISPLACEMENT_CURRENT: (
        Wikidata("Q853178"),
        Equation(
            r"I_D = \iint_S \boldsymbol{J}_D \cdot \boldsymbol{e}_n dA",
            {
                "I_D": SELF,
                "S": "Surface",
                r"\boldsymbol{J}_D": _iso80000.DISPLACEMENT_CURRENT_DENSITY,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
    ),
    _iso80000.TOTAL_CURRENT_DENSITY: (
        Wikidata("Q77680811"),
        Equation(
            r"\boldsymbol{J}_\text{total} = \boldsymbol{J} + \boldsymbol{J}_D",
            {
                r"\boldsymbol{J}_\text{total}": SELF,
                r"\boldsymbol{J}": _iso80000.CURRENT_DENSITY,
                r"\boldsymbol{J}_D": _iso80000.DISPLACEMENT_CURRENT_DENSITY,
            },
        ),
        Symbol(r"\boldsymbol{J}_t"),
    ),
    _iso80000.TOTAL_CURRENT: (
        Wikidata("Q77679732"),
        Equation(
            r"I_\text{total} = I + I_D",
            {
                r"I_\text{total}": SELF,
                "I": _iso80000.CURRENT,
                "I_D": _iso80000.DISPLACEMENT_CURRENT,
            },
        ),
        Symbol("I_t"),
    ),
    _iso80000.MAGNETIC_FLUX_DENSITY: (
        Wikidata("Q30204"),
        Equation(
            r"\boldsymbol{F} = q \boldsymbol{v} \times \boldsymbol{B}",
            {
                r"\boldsymbol{F}": _iso80000.FORCE,
                "q": _iso80000.ELECTRIC_CHARGE,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
                r"\boldsymbol{B}": SELF,
            },
        ),
    ),
    _iso80000.MAGNETIC_FLUX: (
        Wikidata("Q177831"),
        Symbol(r"\Phi"),
        Equation(
            r"\Phi_B = \iint_S \boldsymbol{B} \cdot \boldsymbol{e}_n dA",
            {
                r"\Phi_B": SELF,
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
        Equation(
            r"\Phi_B = \int_C \boldsymbol{A} \cdot d\boldsymbol{r}",
            {
                r"\Phi_B": SELF,
                "C": "Curve",
                r"\boldsymbol{A}": _iso80000.MAGNETIC_VECTOR_POTENTIAL,
                r"d\boldsymbol{r}": _iso80000.LINE_ELEMENT,
            },
        ),
    ),
    _iso80000.PROTOFLUX: (
        Wikidata("Q118540114"),
        Equation(
            r"\Phi_p = \int_C \boldsymbol{A} \cdot d\boldsymbol{r}",
            {
                r"\Phi_p": SELF,
                "C": "Curve",
                r"\boldsymbol{A}": _iso80000.MAGNETIC_VECTOR_POTENTIAL,
                r"d\boldsymbol{r}": _iso80000.LINE_ELEMENT,
            },
        ),
        Symbol(r"\Psi_p"),
    ),
    _iso80000.LINKED_MAGNETIC_FLUX: (
        Wikidata("Q118574738"),
        Symbol(r"\Phi_L"),
        Equation(
            r"\lambda = N \Phi_B",
            {
                r"\lambda": SELF,
                "N": _iso80000.N_TURNS_WINDING,
                r"\Phi_B": _iso80000.MAGNETIC_FLUX,
            },
        ),
    ),
    _iso80000.TOTAL_MAGNETIC_FLUX: (
        Wikidata("Q118255404"),
        Symbol(r"\Psi"),
        Equation(
            r"\Phi_{AB} = \int_{t_1}^{t_2} u_{AB}(\tau) d\tau",
            {
                r"\Phi_{AB}": SELF,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
                "u": _iso80000.VOLTAGE,
                r"\tau": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.MAGNETIC_MOMENT: (
        Wikidata("Q242657"),
        Equation(
            r"\boldsymbol{m} = I \boldsymbol{e}_n A",
            {
                r"\boldsymbol{m}": SELF,
                "I": _iso80000.CURRENT,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "A": _iso80000.AREA,
            },
            assumptions={"infinitesimal planar current loop"},
        ),
    ),
    _iso80000.MAGNETIZATION: (
        Wikidata("Q856711"),
        Equation(
            r"\boldsymbol{M}(\boldsymbol{r}) = \frac{d\boldsymbol{m}}{dV}",
            {
                r"\boldsymbol{M}": SELF,
                r"\boldsymbol{r}": _iso80000.POSITION,
                r"\boldsymbol{m}": _iso80000.MAGNETIC_MOMENT,
                "V": _iso80000.VOLUME,
            },
        ),
        Symbol(r"\boldsymbol{H}_i"),
    ),
    _iso80000.MAGNETIC_FIELD_STRENGTH: (
        Wikidata("Q28123"),
        Equation(
            r"\boldsymbol{H} = \frac{\boldsymbol{B}}{\mu_0} - \boldsymbol{M}",
            {
                r"\boldsymbol{H}": SELF,
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
                r"\mu_0": _iso80000.CONST_PERMEABILITY_VACUUM,
                r"\boldsymbol{M}": _iso80000.MAGNETIZATION,
            },
        ),
        Equation(
            r"\nabla \times \boldsymbol{H} = \boldsymbol{J}_\text{total}",
            {
                r"\boldsymbol{H}": SELF,
                r"\boldsymbol{J}_\text{total}": _iso80000.TOTAL_CURRENT_DENSITY,
            },
        ),
    ),
    _iso80000.CONST_PERMEABILITY_VACUUM: (
        Wikidata("Q1515261"),
        Symbol(r"\mu_0"),
    ),
    _iso80000.PERMEABILITY: (
        Wikidata("Q28352"),
        Equation(
            r"\boldsymbol{B} = \mu \boldsymbol{H}",
            {
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
                r"\mu": SELF,
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
            },
            assumptions={"linear isotropic media"},
        ),
    ),
    _iso80000.RELATIVE_PERMEABILITY: (
        Wikidata("Q77785645"),
        Equation(
            r"\mu_\mathrm{r} = \frac{\mu}{\mu_0}",
            {
                r"\mu_\mathrm{r}": SELF,
                r"\mu": _iso80000.PERMEABILITY,
                r"\mu_0": _iso80000.CONST_PERMEABILITY_VACUUM,
            },
            assumptions={"linear isotropic media"},
        ),
    ),
    _iso80000.MAGNETIC_SUSCEPTIBILITY: (
        Wikidata("Q691463"),
        Symbol(r"\kappa"),
        Equation(
            r"\boldsymbol{M} = \chi_\mathrm{m} \boldsymbol{H}",
            {
                r"\boldsymbol{M}": _iso80000.MAGNETIZATION,
                r"\chi_\mathrm{m}": SELF,
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
            },
            assumptions={"linear isotropic media"},
        ),
    ),
    _iso80000.MAGNETIC_POLARIZATION: (
        Wikidata("Q1884336"),
        Equation(
            r"\boldsymbol{J}_m = \mu_0 \boldsymbol{M}",
            {
                r"\boldsymbol{J}_m": SELF,
                r"\mu_0": _iso80000.CONST_PERMEABILITY_VACUUM,
                r"\boldsymbol{M}": _iso80000.MAGNETIZATION,
            },
        ),
    ),
    _iso80000.MAGNETIC_DIPOLE_MOMENT: (
        Wikidata("Q71008556"),
        Equation(
            r"\boldsymbol{j}_m = \mu_0 \boldsymbol{m}",
            {
                r"\boldsymbol{j}_m": SELF,
                r"\mu_0": _iso80000.CONST_PERMEABILITY_VACUUM,
                r"\boldsymbol{m}": _iso80000.MAGNETIC_MOMENT,
            },
        ),
        Symbol(r"\boldsymbol{j}"),
    ),
    _iso80000.COERCIVITY: (Wikidata("Q432635"), Symbol("H_c")),
    _iso80000.MAGNETIC_VECTOR_POTENTIAL: (
        Wikidata("Q2299100"),
        Equation(
            r"\boldsymbol{B} = \nabla \times \boldsymbol{A}",
            {
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
                r"\boldsymbol{A}": SELF,
            },
        ),
    ),
    _iso80000.ELECTROMAGNETIC_ENERGY_DENSITY: (
        Wikidata("Q77989624"),
        Equation(
            r"w_\mathrm{e} = \frac{1}{2}(\boldsymbol{E} \cdot \boldsymbol{D} + \boldsymbol{B} \cdot \boldsymbol{H})",
            {
                r"w_\mathrm{e}": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\boldsymbol{D}": _iso80000.ELECTRIC_FLUX_DENSITY,
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
            },
        ),
        Symbol("w"),
    ),
    _iso80000.POYNTING_VECTOR: (
        Wikidata("Q504186"),
        Equation(
            r"\boldsymbol{S} = \boldsymbol{E} \times \boldsymbol{H}",
            {
                r"\boldsymbol{S}": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
            },
        ),
    ),
    _iso80000.CONST_SPEED_OF_LIGHT_VACUUM: (Wikidata("Q2111"), Symbol("c_0")),
    _iso80000.SPEED_OF_LIGHT: (Wikidata("Q9092845"), Symbol("c")),
    _iso80000.SOURCE_VOLTAGE: (Wikidata("Q185329"), Symbol("U_s")),
    _iso80000.MAGNETIC_POTENTIAL: (
        Wikidata("Q17162107"),
        Equation(
            r"\boldsymbol{H} = -\nabla V_m",
            {
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
                r"V_m": SELF,
            },
            assumptions={"irrotational magnetic field strength"},
        ),
        Symbol(r"\varphi"),
    ),
    _iso80000.MAGNETIC_TENSION: (
        Wikidata("Q77993836"),
        Equation(
            r"U_m = \int_C \boldsymbol{H} \cdot d\boldsymbol{r}",
            {
                "U_m": SELF,
                "C": "Curve",
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
                r"d\boldsymbol{r}": _iso80000.LINE_ELEMENT,
            },
        ),
    ),
    _iso80000.N_TURNS_WINDING: (Wikidata("Q77995997"), Symbol("N")),
    _iso80000.MAGNETOMOTIVE_FORCE: (
        Wikidata("Q1266982"),
        Equation(
            r"\mathcal{F}_m = \oint_C \boldsymbol{H} \cdot d\boldsymbol{r}",
            {
                r"\mathcal{F}_m": SELF,
                "C": "Closed curve",
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
                r"d\boldsymbol{r}": _iso80000.LINE_ELEMENT,
            },
        ),
    ),
    _iso80000.RELUCTANCE: (
        Wikidata("Q863390"),
        Symbol("R_m"),
        Equation(
            r"\mathcal{R} = \frac{U_m}{\Phi_M}",
            {
                r"\mathcal{R}": SELF,
                r"U_m": _iso80000.MAGNETIC_TENSION,
                r"\Phi_M": _iso80000.TOTAL_MAGNETIC_FLUX,
            },
        ),
    ),
    _iso80000.PERMEANCE: (
        Wikidata("Q77997985"),
        Equation(
            r"\mathcal{P} = \frac{1}{\mathcal{R}}",
            {r"\mathcal{P}": SELF, r"\mathcal{R}": _iso80000.RELUCTANCE},
        ),
        Symbol(r"\Lambda"),
    ),
    _iso80000.INDUCTANCE: (
        Wikidata("Q177897"),
        Equation(
            r"L = \frac{\Psi_{AB}}{I}",
            {
                "L": SELF,
                r"\Psi": _iso80000.TOTAL_MAGNETIC_FLUX,
                "I": _iso80000.CURRENT,
            },
        ),
        Symbol("L_m"),
    ),
    _iso80000.MUTUAL_INDUCTANCE: (
        Wikidata("Q78101401"),
        Equation(
            r"L_{mn} = \frac{\Phi_m}{I_n}",
            {
                r"L_{mn}": SELF,
                "m": "Thin conducting loop 1",
                "n": "Thin conducting loop 2",
                r"\Phi": _iso80000.LINKED_MAGNETIC_FLUX,
                "I": _iso80000.CURRENT,
            },
        ),
    ),
    _iso80000.COUPLING_FACTOR: (
        Wikidata("Q78101715"),
        Equation(
            r"k = \frac{|L_{mn}|}{\sqrt{L_m L_n}}",
            {
                "k": SELF,
                r"L_{mn}": _iso80000.MUTUAL_INDUCTANCE,
                "m": "Thin conducting loop 1",
                "n": "Thin conducting loop 2",
                "L": _iso80000.INDUCTANCE,
            },
        ),
    ),
    _iso80000.LEAKAGE_FACTOR: (
        Wikidata("Q78102042"),
        Equation(
            r"\sigma = 1 - k^2",
            {r"\sigma": SELF, "k": _iso80000.COUPLING_FACTOR},
        ),
    ),
    _iso80000.CONDUCTIVITY: (
        Wikidata("Q4593291"),
        Equation(
            r"\boldsymbol{J} = \sigma \boldsymbol{E}",
            {
                r"\boldsymbol{J}": _iso80000.CURRENT_DENSITY,
                r"\sigma": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
            },
        ),
        Symbol(r"\kappa"),
    ),
    _iso80000.RESISTIVITY: (
        Wikidata("Q108193"),
        Equation(
            r"\rho = \frac{1}{\sigma}",
            {r"\rho": SELF, r"\sigma": _iso80000.CONDUCTIVITY},
        ),
    ),
    _iso80000.INSTANTANEOUS_POWER: (
        Wikidata("Q11784325"),
        Equation(
            r"P(t) = u(t) i(t)",
            {
                "P(t)": SELF,
                "u(t)": _iso80000.INSTANTANEOUS_VOLTAGE,
                "i(t)": _iso80000.INSTANTANEOUS_CURRENT,
            },
        ),
        Symbol("p"),
    ),
    _iso80000.RESISTANCE: (
        Wikidata("Q25358"),
        Equation(
            r"R = \frac{U}{I}",
            {"R": SELF, "U": _iso80000.VOLTAGE, "I": _iso80000.CURRENT},
            assumptions={"ohmic device"},
        ),
    ),
    _iso80000.CONDUCTANCE: (
        Wikidata("Q309017"),
        Equation(
            r"G = \frac{1}{R}",
            {"G": SELF, "R": _iso80000.RESISTANCE},
            assumptions={"ohmic device"},
        ),
    ),
    _iso80000.VOLTAGE_PHASE_ANGLE: Symbol(r"\phi_u"),
    _iso80000.CURRENT_PHASE_ANGLE: Symbol(r"\phi_i"),
    _iso80000.PHASE_DIFFERENCE: (
        Wikidata("Q78514588"),
        Equation(
            r"\phi = \phi_u - \phi_i",
            {
                r"\phi": SELF,
                r"\phi_u": _iso80000.VOLTAGE_PHASE_ANGLE,
                r"\phi_i": _iso80000.CURRENT_PHASE_ANGLE,
            },
        ),
    ),
    _iso80000.CURRENT_PHASOR: (
        Wikidata("Q78514596"),
        Equation(
            r"\underline{I} = \hat{I} e^{j\phi}",
            {
                r"\underline{I}": SELF,
                r"\hat{I}": "Amplitude",
                r"\phi": _iso80000.PHASE_ANGLE,
            },
        ),
    ),
    _iso80000.VOLTAGE_PHASOR: (
        Wikidata("Q78514605"),
        Equation(
            r"\underline{U} = \hat{U} e^{j\phi}",
            {
                r"\underline{U}": SELF,
                r"\hat{U}": "Amplitude",
                r"\phi": _iso80000.PHASE_ANGLE,
            },
        ),
    ),
    _iso80000.IMPEDANCE: (
        Wikidata("Q179043"),
        Equation(
            r"\underline{Z} = \frac{\underline{U}}{\underline{I}}",
            {
                r"\underline{Z}": SELF,
                r"\underline{U}": _iso80000.VOLTAGE_PHASOR,
                r"\underline{I}": _iso80000.CURRENT_PHASOR,
            },
        ),
    ),
    _iso80000.IMPEDANCE_APPARENT: (
        Wikidata("Q119313368"),
        Equation(
            r"Z = \frac{V_\mathrm{rms}}{I_\mathrm{rms}}",
            {
                "Z": SELF,
                r"V_\mathrm{rms}": _iso80000.RMS_VOLTAGE,
                r"I_\mathrm{rms}": _iso80000.RMS_CURRENT,
            },
        ),
    ),
    _iso80000.IMPEDANCE_OF_VACUUM: (
        Wikidata("Q269492"),
        Equation(
            r"Z_0 = \frac{|\boldsymbol{E}|}{|\boldsymbol{H}|}",
            {
                r"Z_0": SELF,
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\boldsymbol{H}": _iso80000.MAGNETIC_FIELD_STRENGTH,
            },
            assumptions={"in vacuum"},
        ),
    ),
    _iso80000.AC_RESISTANCE: (
        Wikidata("Q1048490"),
        Equation(
            r"R = \Re(\underline{Z})",
            {"R": SELF, r"\underline{Z}": _iso80000.IMPEDANCE},
        ),
    ),
    _iso80000.REACTANCE: (
        Wikidata("Q193972"),
        Equation(
            r"X = \Im(\underline{Z})",
            {"X": SELF, r"\underline{Z}": _iso80000.IMPEDANCE},
        ),
    ),
    _iso80000.ADMITTANCE: (
        Wikidata("Q214518"),
        Equation(
            r"\underline{Y} = \frac{1}{\underline{Z}}",
            {r"\underline{Y}": SELF, r"\underline{Z}": _iso80000.IMPEDANCE},
        ),
    ),
    _iso80000.ADMITTANCE_APPARENT: (
        Wikidata("Q119396649"),
        Equation(
            r"Y = \frac{I_\mathrm{rms}}{V_\mathrm{rms}}",
            {
                "Y": SELF,
                r"I_\mathrm{rms}": _iso80000.RMS_CURRENT,
                r"V_\mathrm{rms}": _iso80000.RMS_VOLTAGE,
            },
        ),
    ),
    _iso80000.ADMITTANCE_OF_VACUUM: (
        Wikidata("Q119348262"),
        Equation(
            r"Y_0 = \frac{1}{Z_0}",
            {r"Y_0": SELF, r"Z_0": _iso80000.IMPEDANCE_OF_VACUUM},
        ),
    ),
    _iso80000.AC_CONDUCTANCE: (
        Wikidata("Q79464628"),
        Equation(
            r"G = \Re(\underline{Y})",
            {"G": SELF, r"\underline{Y}": _iso80000.ADMITTANCE},
        ),
    ),
    _iso80000.SUSCEPTANCE: (
        Wikidata("Q509598"),
        Equation(
            r"B = \Im(\underline{Y})",
            {"B": SELF, r"\underline{Y}": _iso80000.ADMITTANCE},
        ),
    ),
    _iso80000.QUALITY_FACTOR: (
        Wikidata("Q79467569"),
        Equation(
            r"Q = \frac{|X|}{R}",
            {"Q": SELF, "X": _iso80000.REACTANCE, "R": _iso80000.RESISTANCE},
            assumptions={"non-radiating systems"},
        ),
        Equation(
            r"Q = \frac{|\Im(\underline{S})|}{\Re(\underline{S})}",
            {
                "Q": SELF,
                r"\Im(\underline{S})": _iso80000.REACTIVE_POWER,
                r"\Re(\underline{S})": _iso80000.ACTIVE_POWER,
            },
            assumptions={
                "linear non-radiating two-terminal system or circuit under sinusoidal conditions"
            },
        ),
        Equation(
            r"Q = 2\pi\frac{E_\mathrm{stored}}{E_\mathrm{dissipated per cycle}}",
            {"Q": SELF, "E": _iso80000.ENERGY},
            assumptions={"resonant system"},
        ),
    ),
    _iso80000.DISSIPATION_FACTOR: (
        Wikidata("Q79468728"),
        Equation(
            r"\mathrm{DF} = \frac{1}{Q}",
            {r"\mathrm{DF}": SELF, "Q": _iso80000.QUALITY_FACTOR},
        ),
        Symbol("d"),
    ),
    _iso80000.LOSS_ANGLE: (
        Wikidata("Q20820438"),
        Equation(
            r"\delta = \arctan \mathrm{DF}",
            {r"\delta": SELF, r"\mathrm{DF}": _iso80000.DISSIPATION_FACTOR},
        ),
    ),
    _iso80000.ACTIVE_POWER: (
        Wikidata("Q12713281"),
        Equation(
            r"P = \frac{1}{T}\int_0^T p(t) dt",
            {
                "P": SELF,
                r"p(t)": _iso80000.INSTANTANEOUS_POWER,
                "T": _iso80000.PERIOD,
                r"dt": _iso80000.TIME,
            },
            assumptions={"periodic"},
        ),
        Equation(
            r"P = \Re(\underline{S})",
            {"P": SELF, r"\underline{S}": _iso80000.COMPLEX_POWER},
        ),
    ),
    _iso80000.APPARENT_POWER: (
        Wikidata("Q1930258"),
        Equation(
            r"S = U_\mathrm{rms} I_\mathrm{rms}",
            {
                "S": SELF,
                r"U_\mathrm{rms}": _iso80000.RMS_VOLTAGE,
                r"I_\mathrm{rms}": _iso80000.RMS_CURRENT,
            },
        ),
        Symbol(r"|\underline{S}|"),
    ),
    _iso80000.POWER_FACTOR: (
        Wikidata("Q750454"),
        Equation(
            r"\mathrm{pf} = \frac{P}{S}",
            {
                r"\mathrm{pf}": SELF,
                "P": _iso80000.ACTIVE_POWER,
                "S": _iso80000.APPARENT_POWER,
            },
        ),
        Symbol(r"\lambda"),
    ),
    _iso80000.COMPLEX_POWER: (
        Wikidata("Q65239736"),
        Equation(
            r"\underline{S} = \underline{U} \underline{I}^*",
            {
                r"\underline{S}": SELF,
                r"\underline{U}": _iso80000.VOLTAGE_PHASOR,
                r"\underline{I}": _iso80000.CURRENT_PHASOR,
                "*": "Complex conjugate",
            },
        ),
    ),
    _iso80000.REACTIVE_POWER: (
        Wikidata("Q2144613"),
        Equation(
            r"Q = \Im(\underline{S})",
            {"Q": SELF, r"\underline{S}": _iso80000.COMPLEX_POWER},
        ),
    ),
    _iso80000.NONACTIVE_POWER: (
        Wikidata("Q79813060"),
        Equation(
            r"Q_~ = \sqrt{S^2 - P^2}",
            {
                r"Q_~": SELF,
                "S": _iso80000.APPARENT_POWER,
                "P": _iso80000.ACTIVE_POWER,
            },
            assumptions={"sinusoidal"},
        ),
        Symbol("Q'"),
    ),
    _iso80000.ACTIVE_ENERGY: (
        Wikidata("Q79813678"),
        Equation(
            r"W = \int_{t_1}^{t_2} p(t) dt",
            {
                "W": SELF,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
                "p(t)": _iso80000.INSTANTANEOUS_POWER,
                "t": _iso80000.TIME,
            },
        ),
    ),
}
LIGHT_AND_RADIATION: Details = {
    _iso80000.REFRACTIVE_INDEX: (
        Wikidata("Q174102"),
        Equation(
            r"n = \frac{c_0}{c}",
            {
                "n": SELF,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
                "c": _iso80000.SPEED_OF_LIGHT,
            },
        ),
    ),
    _iso80000.RADIANT_ENERGY: (
        Wikidata("Q10932713"),
        Equation(
            r"Q_e = \int_{t_1}^{t_2} \Phi_e dt",
            {
                "Q_e": SELF,
                r"\Phi_e": _iso80000.RADIANT_FLUX,
                "t": _iso80000.TIME,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
            },
        ),
        Symbol("W"),
        Symbol("U"),
        Symbol("Q"),
    ),
    _iso80000.SPECTRAL_RADIANT_ENERGY: (
        Wikidata("Q80237041"),
        Equation(
            r"Q_{e,\lambda} = \frac{dQ_e}{d\lambda}",
            {
                r"Q_{e,\lambda}": SELF,
                "Q_e": _iso80000.RADIANT_ENERGY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
        Symbol(r"W_\lambda"),
        Symbol(r"U_\lambda"),
        Symbol(r"Q_\lambda"),
    ),
    _iso80000.RADIANT_ENERGY_DENSITY: (
        Wikidata("Q15054312"),
        Equation(
            r"w_e = \frac{dQ_e}{dV}",
            {
                "w_e": SELF,
                "Q_e": _iso80000.RADIANT_ENERGY,
                "V": _iso80000.VOLUME,
            },
        ),
        Equation(
            r"w_e = \frac{4\sigma}{c_0} T^4",
            {
                "w_e": SELF,
                r"\sigma": _iso80000.CONST_STEFAN_BOLTZMANN,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
                "T": _iso80000.TEMPERATURE,
            },
            assumptions={"planckian radiator"},
        ),
        Symbol(r"\rho_e"),
        Symbol("w"),
    ),
    _iso80000.SPECTRAL_RADIANT_ENERGY_DENSITY_WAVELENGTH: (
        Wikidata("Q80372486"),
        Equation(
            r"w_{e,\lambda} = \frac{dQ_{e,\lambda}}{dV}",
            {
                r"w_{e,\lambda}": SELF,
                r"Q_{e,\lambda}": _iso80000.SPECTRAL_RADIANT_ENERGY,
                "V": _iso80000.VOLUME,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
        Equation(
            r"w_{e,\lambda} = 8\pi h c_0 \frac{\lambda^{-5}}{\exp(c_2\lambda^{-1}T^{-1})-1}",
            {
                r"w_{e,\lambda}": SELF,
                "h": _iso80000.CONST_PLANCK,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
                r"c_2": _iso80000.CONST_SECOND_RADIATION,
                "T": _iso80000.TEMPERATURE,
                r"\lambda": _iso80000.WAVELENGTH,
            },
            assumptions={"planckian radiator"},
        ),
        Symbol(r"w_\lambda"),
    ),
    _iso80000.SPECTRAL_RADIANT_ENERGY_DENSITY_WAVENUMBER: (
        Wikidata("Q80373928"),
        Equation(
            r"w_{e,\tilde{\nu}} = \frac{dQ_{e,\tilde{\nu}}}{dV}",
            {
                r"w_{e,\tilde{\nu}}": SELF,
                r"Q_{e,\tilde{\nu}}": _iso80000.SPECTRAL_RADIANT_ENERGY,
                "V": _iso80000.VOLUME,
                r"\tilde{\nu}": _iso80000.WAVENUMBER,
            },
        ),
        Symbol(r"\rho_{e,\tilde{\nu}}"),
        Symbol(r"w_{\tilde{\nu}}"),
    ),
    _iso80000.RADIANT_FLUX: (
        Wikidata("Q1253356"),
        Equation(
            r"\Phi_e = \frac{dQ_e}{dt}",
            {
                r"\Phi_e": SELF,
                "Q_e": _iso80000.RADIANT_ENERGY,
                "t": _iso80000.TIME,
            },
        ),
        Equation(
            r"\Phi_e = \iint_\Omega I_e(\vartheta, \varphi) \sin\vartheta d\varphi d\vartheta",
            {
                r"\Phi_e": _iso80000.RADIANT_FLUX,
                r"I_e": _iso80000.RADIANT_INTENSITY,
                r"\vartheta": "Polar angle",
                r"\varphi": "Azimuthal angle",
                r"\Omega": _iso80000.SOLID_ANGLE,
            },
        ),
        Symbol(r"P_e"),
    ),
    _iso80000.SPECTRAL_RADIANT_FLUX: (
        Wikidata("Q81062859"),
        Equation(
            r"\Phi_{e,\lambda} = \frac{d\Phi_e}{d\lambda}",
            {
                r"\Phi_{e,\lambda}": SELF,
                r"\Phi_e": _iso80000.RADIANT_FLUX,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
        Symbol(r"P_{e,\lambda}"),
    ),
    _iso80000.RADIANT_INTENSITY: (
        Wikidata("Q1253365"),
        Equation(
            r"I_e = \frac{d\Phi_e}{d\Omega}",
            {
                r"I_e": SELF,
                r"\Phi_e": _iso80000.RADIANT_FLUX,
                r"\Omega": _iso80000.SOLID_ANGLE,
            },
            assumptions={"point source"},
        ),
    ),
    _iso80000.SPECTRAL_RADIANT_INTENSITY: (
        Wikidata("Q81072410"),
        Equation(
            r"I_{e,\lambda} = \frac{dI_e}{d\lambda}",
            {
                r"I_{e,\lambda}": SELF,
                r"I_e": _iso80000.RADIANT_INTENSITY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.RADIANCE: (
        Wikidata("Q1411145"),
        Equation(
            r"L_e = \frac{dI_e}{dA} \frac{1}{\cos\theta}",
            {
                "L_e": SELF,
                r"I_e": _iso80000.RADIANT_INTENSITY,
                "A": _iso80000.AREA,
                r"\theta": (
                    _iso80000.ANGLE,
                    " between the surface normal and the specified direction",
                ),
            },
        ),
        Equation(
            r"L_e = \frac{\sigma}{\pi} T^4",
            {
                "L_e": SELF,
                r"\sigma": _iso80000.CONST_STEFAN_BOLTZMANN,
                "T": _iso80000.TEMPERATURE,
            },
            assumptions={"planckian radiator"},
        ),
    ),
    _iso80000.SPECTRAL_RADIANCE: (
        Wikidata("Q27649052"),
        Equation(
            r"L_{e,\lambda} = \frac{dL_e}{d\lambda}",
            {
                r"L_{e,\lambda}": SELF,
                r"L_e": _iso80000.RADIANCE,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
        Equation(
            r"L_{e,\lambda}(\lambda) = \frac{c(\lambda)}{4\pi} \omega_\lambda(\lambda)=h c_0^2 \frac{\lambda^{-5}}{\exp(c_2 \lambda^{-1} T^{-1}) - 1}",
            {
                r"L_{e,\lambda}": SELF,
                r"\lambda": _iso80000.WAVELENGTH,
                r"c(\lambda)": _iso80000.SPEED_OF_LIGHT,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
                "h": _iso80000.CONST_PLANCK,
                r"c_2": _iso80000.CONST_SECOND_RADIATION,
                "T": _iso80000.TEMPERATURE,
                r"\omega_\lambda": _iso80000.SPECTRAL_RADIANT_ENERGY_DENSITY_WAVELENGTH,
            },
            assumptions={"planckian radiator"},
        ),
    ),
    _iso80000.IRRADIANCE: (
        Wikidata("Q830654"),
        Equation(
            r"E_e = \frac{d\Phi_e}{dA}",
            {
                "E_e": SELF,
                r"\Phi_e": _iso80000.RADIANT_FLUX,
                "A": _iso80000.AREA,
            },
        ),
    ),
    _iso80000.SPECTRAL_IRRADIANCE: (
        Wikidata("Q81382741"),
        Equation(
            r"E_{e,\lambda} = \frac{dE_e}{d\lambda}",
            {
                r"E_{e,\lambda}": SELF,
                "E_e": _iso80000.IRRADIANCE,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.RADIANT_EXITANCE: (
        Wikidata("Q15054698"),
        Equation(
            r"M_e = \frac{d\Phi_e}{dA}",
            {
                "M_e": SELF,
                r"\Phi_e": _iso80000.RADIANT_FLUX,
                "A": _iso80000.AREA,
            },
        ),
        Equation(
            r"M_e = \sigma T^4",
            {
                "M_e": SELF,
                r"\sigma": _iso80000.CONST_STEFAN_BOLTZMANN,
                "T": _iso80000.TEMPERATURE,
            },
            assumptions={"planckian radiator"},
        ),
    ),  #
    _iso80000.SPECTRAL_RADIANT_EXITANCE: (
        Wikidata("Q81664734"),
        Equation(
            r"M_{e,\lambda} = \frac{dM_e}{d\lambda}",
            {
                r"M_{e,\lambda}": SELF,
                "M_e": _iso80000.RADIANT_EXITANCE,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.RADIANT_EXPOSURE: (
        Wikidata("Q1418023"),
        Equation(
            r"H_e = \frac{dQ_e}{dA}",
            {"H_e": SELF, "Q_e": _iso80000.RADIANT_ENERGY, "A": _iso80000.AREA},
        ),
    ),
    _iso80000.SPECTRAL_RADIANT_EXPOSURE: (
        Wikidata("Q82969329"),
        Equation(
            r"H_{e,\lambda} = \frac{dH_e}{d\lambda}",
            {
                r"H_{e,\lambda}": SELF,
                "H_e": _iso80000.RADIANT_EXPOSURE,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.LUMINOUS_EFFICIENCY: (
        Wikidata("Q83293942"),
        Equation(
            r"V = \frac{K}{K_m}",
            {
                "V": SELF,
                "K": _iso80000.LUMINOUS_EFFICACY_OF_RADIATION,
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
            },
            assumptions={"photopic vision"},
        ),
    ),
    _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY: (Wikidata("Q899219"),),
    _iso80000.LUMINOUS_EFFICACY_OF_RADIATION: (
        Wikidata("Q1504173"),
        Equation(
            r"K = \frac{\Phi_\nu}{\Phi_e}",
            {
                "K": SELF,
                r"\Phi_\nu": _iso80000.LUMINOUS_FLUX,
                r"\Phi_e": _iso80000.RADIANT_FLUX,
            },
        ),
    ),
    _iso80000.SPECTRAL_LUMINOUS_EFFICACY: (
        Wikidata("Q83387222"),
        Equation(
            r"K(\lambda) = K_m V(\lambda)",
            {
                r"K": SELF,
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
                r"V": _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.MAXIMUM_LUMINOUS_EFFICACY: (
        Wikidata("Q83387484"),
        Symbol(r"K_m"),
    ),
    _iso80000.LUMINOUS_EFFICACY_OF_SOURCE: (
        Wikidata("Q3425218"),
        Equation(
            r"\eta_\nu = \frac{\Phi_\nu}{P}",
            {
                r"\eta_\nu": SELF,
                r"\Phi_\nu": _iso80000.LUMINOUS_FLUX,
                "P": _iso80000.POWER,
            },
        ),
    ),
    _iso80000.LUMINOUS_ENERGY: (
        Wikidata("Q900164"),
        Equation(
            r"Q_\nu = \int_{t_1}^{t_2} \Phi_\nu(t) dt",
            {
                r"Q_\nu": SELF,
                r"\Phi_\nu": _iso80000.LUMINOUS_FLUX,
                "t": _iso80000.TIME,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
            },
        ),
    ),
    _iso80000.LUMINOUS_FLUX: (
        Wikidata("Q107780"),
        Equation(
            r"\Phi_\nu = \frac{dQ_\nu}{dt} = K_m \int_0^\infty \Phi_{e,\lambda}(\lambda) V(\lambda) d\lambda",
            {
                r"\Phi_\nu": SELF,
                r"Q_\nu": _iso80000.LUMINOUS_ENERGY,
                "t": _iso80000.TIME,
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
                r"\Phi_{e,\lambda}": _iso80000.SPECTRAL_RADIANT_FLUX,
                r"V(\lambda)": _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.LUMINOUS_INTENSITY: (
        Wikidata("Q104831"),
        Equation(
            r"I_\nu = \frac{d\Phi_\nu}{d\Omega} = K_m \int_0^\infty I_{e,\lambda}(\lambda) V(\lambda) d\lambda",
            {
                r"I_\nu": SELF,
                r"\Phi_\nu": _iso80000.LUMINOUS_FLUX,
                r"\Omega": _iso80000.SOLID_ANGLE,
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
                r"I_{e,\lambda}": _iso80000.SPECTRAL_RADIANT_INTENSITY,
                r"V(\lambda)": _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.LUMINANCE: (
        Wikidata("Q355386"),
        Equation(
            r"L_\nu = \frac{dI_\nu}{dA}\frac{1}{\cos\theta} = K_m \int_0^\infty L_{e,\lambda}(\lambda) V(\lambda) d\lambda",
            {
                r"L_\nu": SELF,
                r"I_\nu": _iso80000.LUMINOUS_INTENSITY,
                "A": _iso80000.AREA,
                r"\theta": (
                    _iso80000.ANGLE,
                    " between the surface normal at the point and the specified direction",
                ),
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
                r"L_{e,\lambda}": _iso80000.SPECTRAL_RADIANCE,
                r"V(\lambda)": _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.ILLUMINANCE: (
        Wikidata("Q194411"),
        Equation(
            r"E_\nu = \frac{d\Phi_\nu}{dA} = K_m \int_0^\infty E_{e,\lambda}(\lambda) V(\lambda) d\lambda",
            {
                r"E_\nu": SELF,
                r"\Phi_\nu": _iso80000.LUMINOUS_FLUX,
                "A": _iso80000.AREA,
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
                r"E_{e,\lambda}": _iso80000.SPECTRAL_IRRADIANCE,
                r"V(\lambda)": _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.LUMINOUS_EXITANCE: (
        Wikidata("Q11721922"),
        Equation(
            r"M_\nu = \frac{d\Phi_\nu}{dA} = K_m \int_0^\infty M_{e,\lambda}(\lambda) V(\lambda) d\lambda",
            {
                r"M_\nu": SELF,
                r"\Phi_\nu": _iso80000.LUMINOUS_FLUX,
                "A": _iso80000.AREA,
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
                r"M_{e,\lambda}": _iso80000.SPECTRAL_RADIANT_EXITANCE,
                r"V(\lambda)": _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.LUMINOUS_EXPOSURE: (
        Wikidata("Q815588"),
        Equation(
            r"H_\nu = \frac{dQ_\nu}{dA} = K_m \int_0^\infty H_{e,\lambda}(\lambda) V(\lambda) d\lambda",
            {
                r"H_\nu": SELF,
                r"Q_\nu": _iso80000.LUMINOUS_ENERGY,
                "A": _iso80000.AREA,
                "K_m": _iso80000.MAXIMUM_LUMINOUS_EFFICACY,
                r"H_{e,\lambda}": _iso80000.SPECTRAL_RADIANT_EXPOSURE,
                r"V(\lambda)": _iso80000.SPECTRAL_LUMINOUS_EFFICIENCY,
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.NUMBER_OF_PHOTONS: (
        Wikidata("Q83698917"),
        Equation(
            r"N_p = \frac{Q_e}{hf} = \int_{t_1}^{t_2} \Phi_p dt",
            {
                "N_p": SELF,
                "Q_e": _iso80000.RADIANT_ENERGY,
                "h": _iso80000.CONST_PLANCK,
                "f": _iso80000.FREQUENCY,
                r"\Phi_p": _iso80000.PHOTON_FLUX,
                "t": _iso80000.TIME,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
            },
        ),
    ),
    _iso80000.PHOTON_ENERGY: (
        Wikidata("Q25303639"),
        Equation(
            r"E_p = hf",
            {
                "E_p": SELF,
                "h": _iso80000.CONST_PLANCK,
                "f": _iso80000.FREQUENCY,
            },
        ),
        Symbol("Q"),
    ),
    _iso80000.PHOTON_FLUX: (
        Wikidata("Q83699542"),
        Equation(
            r"\Phi_p = \frac{dN_p}{dt}",
            {
                r"\Phi_p": SELF,
                "N_p": _iso80000.NUMBER_OF_PHOTONS,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.PHOTON_INTENSITY: (
        Wikidata("Q83853335"),
        Equation(
            r"I_p = \frac{d\Phi_p}{d\Omega}",
            {
                r"I_p": SELF,
                r"\Phi_p": _iso80000.PHOTON_FLUX,
                r"\Omega": _iso80000.SOLID_ANGLE,
            },
        ),
    ),
    _iso80000.PHOTON_RADIANCE: (
        Wikidata("Q10498337"),
        Equation(
            r"L_p = \frac{dI_p}{dA} \frac{1}{\cos\theta}",
            {
                "L_p": SELF,
                r"I_p": _iso80000.PHOTON_INTENSITY,
                "A": _iso80000.AREA,
                r"\cos\theta": "Angle between the surface normal at the point and the specified direction",
            },
        ),
    ),
    _iso80000.PHOTON_IRRADIANCE: (
        Wikidata("Q83950903"),
        Equation(
            r"E_p = \frac{d\Phi_p}{dA}",
            {
                r"E_p": SELF,
                r"\Phi_p": _iso80000.PHOTON_FLUX,
                "A": (_iso80000.AREA, " over which the flux is incident"),
            },
        ),
    ),
    _iso80000.PHOTON_EXITANCE: (
        Wikidata("Q84025202"),
        Equation(
            r"M_p = \frac{d\Phi_p}{dA}",
            {
                r"M_p": SELF,
                r"\Phi_p": _iso80000.PHOTON_FLUX,
                "A": (_iso80000.AREA, " from which the flux is emitted"),
            },
        ),
    ),
    _iso80000.PHOTON_EXPOSURE: (
        Wikidata("Q84026278"),
        Equation(
            r"H_p = \frac{dN_p}{dA}",
            {
                r"H_p": SELF,
                "N_p": _iso80000.NUMBER_OF_PHOTONS,
                "A": _iso80000.AREA,
            },
        ),
    ),
    _iso80000.CIE_COLOUR_MATCHING_FUNCTIONS_1931: (
        Wikidata("Q84413021"),
        Symbol(r"\bar{x}(\lambda), \bar{y}(\lambda), \bar{z}(\lambda)"),
    ),
    _iso80000.CIE_COLOUR_MATCHING_FUNCTIONS_1964: (
        Wikidata("Q84413310"),
        Symbol(
            r"\bar{x}_{10}(\lambda), \bar{y}_{10}(\lambda), \bar{z}_{10}(\lambda)"
        ),
    ),
    _iso80000.CHROMATICITY_COORDINATES_1931: (
        Wikidata("Q84413341"),
        Equation(
            r"\begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} \frac{X}{X + Y + Z} \\ \frac{Y}{X + Y + Z} \\ \frac{Z}{X + Y + Z} \end{bmatrix}",
            {
                r"\begin{bmatrix} x \\ y \\ z \end{bmatrix}": SELF,
                "X": "CIE 1931 tristimulus value X",
                "Y": "CIE 1931 tristimulus value Y",
                "Z": "CIE 1931 tristimulus value Z",
            },
        ),
    ),
    _iso80000.CHROMATICITY_COORDINATES_1964: (
        Wikidata("Q84413536"),
        Equation(
            r"\begin{bmatrix} x_{10} \\ y_{10} \\ z_{10} \end{bmatrix} = \begin{bmatrix} \frac{X_{10}}{X_{10} + Y_{10} + Z_{10}} \\ \frac{Y_{10}}{X_{10} + Y_{10} + Z_{10}} \\ \frac{Z_{10}}{X_{10} + Y_{10} + Z_{10}} \end{bmatrix}",
            {
                r"\begin{bmatrix} x_{10} \\ y_{10} \\ z_{10} \end{bmatrix}": SELF,
                r"X_{10}": "CIE 1964 tristimulus value X",
                r"Y_{10}": "CIE 1964 tristimulus value Y",
                r"Z_{10}": "CIE 1964 tristimulus value Z",
            },
        ),
    ),
    _iso80000.COLOUR_TEMPERATURE: (Wikidata("Q327408"), Symbol("T_c")),
    _iso80000.CORRELATED_COLOUR_TEMPERATURE: (
        Wikidata("Q25452284"),
        Symbol(r"T_{cp}"),
    ),
    _iso80000.EMISSIVITY: (
        Wikidata("Q899670"),
        Equation(
            r"\varepsilon = \frac{M_e}{(M_{e})_{bb}}",
            {
                r"\varepsilon": SELF,
                "M_e": _iso80000.RADIANT_EXITANCE,
                "bb": "Planckian radiator at the same temperature",
            },
        ),
        Symbol(r"\varepsilon_T"),
    ),
    _iso80000.EMISSIVITY_AT_SPECIFIC_WAVELENGTH: (
        Wikidata("Q84710157"),
        Symbol(r"\varepsilon(\lambda)"),
    ),
    _iso80000.ABSORPTANCE: (
        Wikidata("Q16635541"),
        Equation(
            r"\alpha = \frac{\Phi_{e,a}}{\Phi_{e,i}}",
            {
                r"\alpha": SELF,
                r"\Phi_{e,a}": _iso80000.ABSORBED_RADIANT_FLUX,
                r"\Phi_{e,i}": _iso80000.INCIDENT_RADIANT_FLUX,
            },
        ),
        Symbol("a"),
    ),
    _iso80000.LUMINOUS_ABSORPTANCE: (
        Wikidata("Q84827265"),
        Equation(
            r"\alpha_\nu = \frac{\Phi_{\nu,a}}{\Phi_{\nu,i}}",
            {
                r"\alpha_\nu": SELF,
                r"\Phi_{\nu,a}": _iso80000.ABSORBED_LUMINOUS_FLUX,
                r"\Phi_{\nu,i}": _iso80000.INCIDENT_LUMINOUS_FLUX,
            },
        ),
    ),
    _iso80000.REFLECTANCE: (
        Wikidata("Q663650"),
        Equation(
            r"\rho = \frac{\Phi_{e,r}}{\Phi_{e,i}}",
            {
                r"\rho": SELF,
                r"\Phi_{e,r}": _iso80000.REFLECTED_RADIANT_FLUX,
                r"\Phi_{e,i}": _iso80000.INCIDENT_RADIANT_FLUX,
            },
        ),
    ),
    _iso80000.LUMINOUS_REFLECTANCE: (
        Wikidata("Q84932761"),
        Equation(
            r"\rho_\nu = \frac{\Phi_{\nu,r}}{\Phi_{\nu,i}}",
            {
                r"\rho_\nu": SELF,
                r"\Phi_{\nu,r}": _iso80000.REFLECTED_LUMINOUS_FLUX,
                r"\Phi_{\nu,i}": _iso80000.INCIDENT_LUMINOUS_FLUX,
            },
        ),
    ),
    _iso80000.TRANSMITTANCE: (
        Wikidata("Q1427863"),
        Equation(
            r"\tau = \frac{\Phi_{e,t}}{\Phi_{e,i}}",
            {
                r"\tau": SELF,
                r"\Phi_{e,t}": _iso80000.TRANSMITTED_RADIANT_FLUX,
                r"\Phi_{e,i}": _iso80000.INCIDENT_RADIANT_FLUX,
            },
        ),
        Symbol("T"),
    ),
    _iso80000.LUMINOUS_TRANSMITTANCE: (
        Wikidata("Q84935567"),
        Equation(
            r"\tau_\nu = \frac{\Phi_{\nu,t}}{\Phi_{\nu,i}}",
            {
                r"\tau_\nu": SELF,
                r"\Phi_{\nu,t}": _iso80000.TRANSMITTED_LUMINOUS_FLUX,
                r"\Phi_{\nu,i}": _iso80000.INCIDENT_LUMINOUS_FLUX,
            },
        ),
    ),
    _iso80000.ABSORBANCE: (
        Wikidata("Q907315"),
        Symbol("D"),
        Symbol(r"A_{10}"),
        Symbol(r"D_\tau"),
    ),
    _iso80000.NAPIERIAN_ABSORBANCE: (
        Wikidata("Q85664557"),
        Symbol("A_n"),
        Symbol("B"),
    ),
    _iso80000.RADIANCE_FACTOR: (
        Wikidata("Q85811846"),
        Equation(
            r"\beta_e = \frac{(L_e)_n}{(L_e)_d}",
            {
                r"\beta_e": SELF,
                "L_e": _iso80000.RADIANCE,
                "n": "Surface element in a given direction",
                "d": "Perfect reflecting or transmitting diffuser",
            },
        ),
    ),
    _iso80000.LUMINANCE_FACTOR: (
        Wikidata("Q1821355"),
        Equation(
            r"\beta_\nu = \frac{(L_\nu)_n}{(L_\nu)_d}",
            {
                r"\beta_\nu": SELF,
                r"L_\nu": _iso80000.LUMINANCE,
                "n": "Surface element in a given direction",
                "d": "Perfect reflecting or transmitting diffuser",
            },
        ),
    ),
    _iso80000.REFLECTANCE_FACTOR: (
        Wikidata("Q86078369"),
        Equation(
            r"R = \frac{(\Phi_{e,r})_n}{(\Phi_{e,r})_d}",
            {
                "R": SELF,
                r"\Phi_{e,r}": _iso80000.REFLECTED_RADIANT_FLUX,
                "n": "A given cone",
                "d": "Identically irradiated diffuser of reflectance 1",
            },
        ),
    ),
    _iso80000.PROPAGATION_LENGTH: Symbol("l"),
    _iso80000.PROPAGATION_LENGTH_ABSORBING_AND_SCATTERING: Symbol("l"),
    _iso80000.LINEAR_ATTENUATION_COEFFICIENT: (
        Wikidata("Q86204330"),
        Equation(
            r"\mu(\lambda) = -\frac{1}{\Phi_{e,\lambda}(\lambda)}\frac{d\Phi_{e,\lambda}(\lambda)}{dl}",
            {
                r"\mu": SELF,
                r"\Phi_{e,\lambda}(\lambda)": _iso80000.SPECTRAL_RADIANT_FLUX,
                "l": _iso80000.PROPAGATION_LENGTH_ABSORBING_AND_SCATTERING,
            },
        ),
        Symbol(r"\mu_l"),
    ),
    _iso80000.PROPAGATION_LENGTH_ABSORBING: Symbol("l"),
    _iso80000.LINEAR_ABSORPTION_COEFFICIENT: (
        Wikidata("Q86204782"),
        Equation(
            r"\alpha(\lambda) = -\frac{1}{\Phi_{e,\lambda}(\lambda)}\frac{d\Phi_{e,\lambda}(\lambda)}{dl}",
            {
                r"\alpha": SELF,
                r"\Phi_{e,\lambda}(\lambda)": _iso80000.SPECTRAL_RADIANT_FLUX,
                "l": _iso80000.PROPAGATION_LENGTH_ABSORBING,
            },
        ),
        Symbol(r"\alpha_l"),
        Symbol("a_l"),
        Symbol(r"\alpha"),
    ),
    _iso80000.MASS_ATTENUATION_COEFFICIENT: (
        Wikidata("Q1907558"),
        Equation(
            r"\mu_m(\lambda) = \frac{\mu(\lambda)}{\rho}",
            {
                r"\mu_m": SELF,
                r"\lambda": _iso80000.WAVELENGTH,
                r"\mu": _iso80000.LINEAR_ATTENUATION_COEFFICIENT,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.MASS_ABSORPTION_COEFFICIENT: (
        Wikidata("Q86202147"),
        Equation(
            r"\alpha_m(\lambda) = \frac{\alpha(\lambda)}{\rho}",
            {
                r"\alpha_m": SELF,
                r"\lambda": _iso80000.WAVELENGTH,
                r"\alpha": _iso80000.LINEAR_ABSORPTION_COEFFICIENT,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.MOLAR_ABSORPTION_COEFFICIENT: (
        Wikidata("Q11784888"),
        Equation(
            r"\chi = \alpha V_m",
            {
                r"\chi": SELF,
                r"\alpha": _iso80000.LINEAR_ABSORPTION_COEFFICIENT,
                "V_m": _iso80000.MOLAR_VOLUME,
            },
        ),
    ),
}
ACOUSTICS: Details = {
    _iso80000.SOUND_PRESSURE: (
        Wikidata("Q1068172"),
        Equation(
            r"p = p_\text{total} - p_\text{static}",
            {
                "p": SELF,
                r"p_\text{total}": _iso80000.PRESSURE,
                r"p_\text{static}": _iso80000.STATIC_PRESSURE,
            },
        ),
    ),
    _iso80000.SOUND_PARTICLE_DISPLACEMENT: (
        Wikidata("Q779457"),
        Symbol(r"\boldsymbol{\delta}"),
    ),
    _iso80000.SOUND_PARTICLE_VELOCITY: (
        Wikidata("Q336894"),
        Equation(
            r"\boldsymbol{u} = \frac{\partial\boldsymbol{\delta}}{\partial t}",
            {
                r"\boldsymbol{u}": SELF,
                r"\boldsymbol{\delta}": _iso80000.SOUND_PARTICLE_DISPLACEMENT,
                "t": _iso80000.TIME,
            },
            assumptions={"magnitude small relative to phase speed"},
        ),
        Symbol("v"),
    ),
    _iso80000.SOUND_PARTICLE_ACCELERATION: (
        Wikidata("Q7140491"),
        Equation(
            r"\boldsymbol{a} = \frac{\partial\boldsymbol{u}}{\partial t}",
            {
                r"\boldsymbol{a}": SELF,
                r"\boldsymbol{u}": _iso80000.SOUND_PARTICLE_VELOCITY,
                "t": _iso80000.TIME,
            },
            assumptions={"magnitude small relative to phase speed"},
        ),
    ),
    _iso80000.SOUND_VOLUME_FLOW_RATE: (
        Wikidata("Q1640308"),
        Equation(
            r"q = \iint_S \boldsymbol{u} \cdot \boldsymbol{e}_n dA",
            {
                "q": SELF,
                r"\boldsymbol{u}": _iso80000.SOUND_PARTICLE_VELOCITY,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
        ),
        Symbol("q_V"),
    ),
    _iso80000.SOUND_ENERGY_DENSITY: (
        Wikidata("Q2230505"),
        Equation(
            r"w = \frac{1}{2}\rho_m u^2 + \frac{p^2}{2\rho_m c^2}",
            {
                "w": SELF,
                r"\rho_m": _iso80000.DENSITY,
                "u": _iso80000.SOUND_PARTICLE_VELOCITY,
                "p": _iso80000.SOUND_PRESSURE,
                "c": _iso80000.SPEED_OF_SOUND,
            },
            assumptions={"low mean fluid flow"},
        ),
    ),
    _iso80000.SOUND_ENERGY: (
        Wikidata("Q351281"),
        Equation(
            r"Q = \int_V w dV",
            {
                "Q": SELF,
                "w": _iso80000.SOUND_ENERGY_DENSITY,
                "dV": _iso80000.VOLUME_ELEMENT,
            },
        ),
    ),
    _iso80000.SOUND_POWER: (
        Wikidata("Q1588477"),
        Equation(
            r"P = \iint_S p \boldsymbol{u} \cdot \boldsymbol{e}_n dA",
            {
                "P": SELF,
                "p": _iso80000.SOUND_PRESSURE,
                r"\boldsymbol{u}": _iso80000.SOUND_PARTICLE_VELOCITY,
                r"\boldsymbol{e}_n": "Unit normal vector to the surface",
                "dA": _iso80000.SURFACE_ELEMENT,
            },
            assumptions={"homogeneous gas or fluid", "low mean fluid flow"},
        ),
        Symbol("W"),
    ),
    _iso80000.SOUND_INTENSITY: (
        Wikidata("Q1140289"),
        Equation(
            r"\boldsymbol{I} = p \boldsymbol{u}",
            {
                r"\boldsymbol{I}": SELF,
                "p": _iso80000.SOUND_PRESSURE,
                r"\boldsymbol{u}": _iso80000.SOUND_PARTICLE_VELOCITY,
            },
            assumptions={"low mean fluid flow"},
        ),
    ),
    _iso80000.SOUND_EXPOSURE: (
        Wikidata("Q2230528"),
        Equation(
            r"E = \int_{t_1}^{t_2} (p(t))^2 dt",
            {
                "E": SELF,
                "p(t)": _iso80000.SOUND_PRESSURE,
                "t": _iso80000.TIME,
                "t_1": _iso80000.INITIAL_TIME,
                "t_2": _iso80000.FINAL_TIME,
            },
        ),
    ),
    _iso80000.CHARACTERISTIC_IMPEDANCE_LONGITUDINAL: (
        Wikidata("Q87051330"),
        Equation(
            r"Z_c = \frac{p}{\boldsymbol{u} \cdot \boldsymbol{e}_n}",
            {
                "Z_c": SELF,
                "p": _iso80000.SOUND_PRESSURE,
                r"\boldsymbol{u}": _iso80000.SOUND_PARTICLE_VELOCITY,
                r"\boldsymbol{e}_n": "Unit normal vector to the direction of wave propagation",
            },
            assumptions={
                "progressive plane wave",
                "non-dissipative homogeneous gas or fluid",
            },
        ),
    ),
    _iso80000.ACOUSTIC_IMPEDANCE: (
        Wikidata("Q975684"),
        Equation(
            r"Z_a = \frac{p_\mathrm{avg}}{q}",
            {
                "Z_a": SELF,
                "p": _iso80000.SOUND_PRESSURE,
                "q": _iso80000.SOUND_VOLUME_FLOW_RATE,
            },
            assumptions={"real if zero phase difference"},
        ),
    ),
    _iso80000.REVERBERATION_TIME: (Wikidata("Q606646"), Symbol("T")),
}
# notation:
# - _X, _A, _B = of substance B
# - ^* = pure
# - ^{\minuso} = standard
PHYSICAL_CHEMISTRY_AND_MOLECULAR_PHYSICS: Details = {
    _iso80000.NUMBER_OF_ENTITIES: (Wikidata("Q614112"), Symbol("N")),
    _iso80000.AMOUNT_OF_SUBSTANCE: (
        Wikidata("Q104946"),
        Equation(
            r"n(\mathrm{X}) = \frac{N(\mathrm{X})}{N_A}",
            {
                "n": SELF,
                r"\mathrm{X}": "Substance",
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "N_A": _iso80000.CONST_AVOGADRO,
            },
        ),
    ),
    _iso80000.RELATIVE_ATOMIC_MASS: (
        Wikidata("Q41377"),
        Equation(
            r"A_r(\mathrm{X}) = \frac{m_\mathrm{average}(\mathrm{X})}{m_u}",
            {
                "A_r": SELF,
                r"\mathrm{X}": "Atom or molecule",
                r"m": _iso80000.MASS,
                "u": "Unified atomic mass",
            },
        ),
    ),
    _iso80000.MOLAR_MASS: (
        Wikidata("Q145623"),
        Equation(
            r"M(\mathrm{X}) = \frac{m(\mathrm{X})}{n(\mathrm{X})}",
            {
                "M": SELF,
                r"\mathrm{X}": "Pure substance",
                "m": _iso80000.MASS,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
            },
        ),
    ),
    _iso80000.MOLAR_VOLUME: (
        Wikidata("Q487112"),
        Equation(
            r"V_m = \frac{V}{n(\mathrm{X})}",
            {
                "V_m": SELF,
                "V": _iso80000.VOLUME,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"\mathrm{X}": "Pure substance",
            },
        ),
    ),
    _iso80000.MOLAR_ENERGY: (Wikidata("Q45721316"),),
    _iso80000.MOLAR_INTERNAL_ENERGY: (
        Wikidata("Q88523106"),
        Equation(
            r"U_m = \frac{U}{n(\mathrm{X})}",
            {
                "U_m": SELF,
                "U": _iso80000.INTERNAL_ENERGY,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"\mathrm{X}": "Substance (commonly pure)",
            },
        ),
    ),
    _iso80000.MOLAR_ENTHALPY: (
        Wikidata("Q88769977"),
        Equation(
            r"H_m = \frac{H}{n(\mathrm{X})}",
            {
                "H_m": SELF,
                "H": _iso80000.ENTHALPY,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"\mathrm{X}": "Substance (commonly pure)",
            },
        ),
    ),
    _iso80000.MOLAR_HELMHOLTZ_ENERGY: (
        Wikidata("Q88862986"),
        Equation(
            r"A_m = \frac{A}{n(\mathrm{X})}",
            {
                "A_m": SELF,
                "A": _iso80000.HELMHOLTZ_ENERGY,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"\mathrm{X}": "Substance (commonly pure)",
            },
        ),
        Symbol("F_m"),
    ),
    _iso80000.MOLAR_GIBBS_ENERGY: (
        Wikidata("Q88863324"),
        Equation(
            r"G_m = \frac{G}{n(\mathrm{X})}",
            {
                "G_m": SELF,
                "G": _iso80000.GIBBS_ENERGY,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"\mathrm{X}": "Substance (commonly pure)",
            },
        ),
    ),
    _iso80000.MOLAR_HEAT_CAPACITY: (
        Wikidata("Q2937190"),
        Equation(
            r"C_m = \frac{C}{n(\mathrm{X})}",
            {
                "C_m": SELF,
                "C": _iso80000.HEAT_CAPACITY,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"\mathrm{X}": "Substance (commonly pure)",
            },
        ),
    ),
    _iso80000.MOLAR_ENTROPY: (
        Wikidata("Q68972876"),
        Equation(
            r"S_m = \frac{S}{n(\mathrm{X})}",
            {
                "S_m": SELF,
                "S": _iso80000.ENTROPY,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"\mathrm{X}": "Substance (commonly pure)",
            },
        ),
    ),
    _iso80000.NUMBER_DENSITY: (
        Wikidata("Q39078574"),
        Equation(
            r"n = \frac{N}{V}",
            {
                "n": SELF,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.MOLECULAR_CONCENTRATION: (
        Wikidata("Q88865973"),
        Symbol(r"C(\mathrm{X})", where={r"\mathrm{X}": "Substance"}),
        Symbol(r"C_\mathrm{X}", where={r"\mathrm{X}": "Substance"}),
    ),
    _iso80000.MOLE_FRACTION: (
        Wikidata("Q125264"),
        Equation(
            r"x_\mathrm{X} = \frac{n_\mathrm{X}}{n_\text{total}}",
            {
                "x": SELF,
                r"\mathrm{X}": "Substance, single molecule for every species in the mixture",
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
            },
        ),
        Symbol(
            r"y_\mathrm{X}",
            where={
                r"\mathrm{X}": "Substance, single molecule for every species in the mixture"
            },
            remarks="for gaseous mixtures",
        ),
    ),
    _iso80000.MOLAR_CONCENTRATION: (
        Wikidata("Q672821"),
        Equation(
            r"c_\mathrm{X} = \frac{n_\mathrm{X}}{V}",
            {
                "c": SELF,
                r"\mathrm{X}": "Substance",
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.STANDARD_MOLAR_CONCENTRATION: Symbol(
        r"c^\circ(\mathrm{X})", where={r"\mathrm{X}": "Substance"}
    ),
    _iso80000.VOLUME_FRACTION: (
        Wikidata("Q909482"),
        Equation(
            r"\phi_\mathrm{X} = \frac{x_\mathrm{X} ({V_m})_\mathrm{X}}{\sum_i x_i ({V_m})_i}",
            {
                r"\phi": SELF,
                r"\mathrm{X}": "Substance",
                "x": _iso80000.MOLE_FRACTION,
                "V_m": _iso80000.MOLAR_VOLUME,
                "i": "All pure substances in mixture",
            },
        ),
    ),
    _iso80000.MOLALITY: (
        Wikidata("Q172623"),
        Equation(
            r"b_\mathrm{B} = \frac{n_\mathrm{B}}{m_\mathrm{A}}",
            {
                "b": SELF,
                r"\mathrm{B}": "Solute",
                r"n": _iso80000.AMOUNT_OF_SUBSTANCE,
                r"m": _iso80000.MASS,
                r"\mathrm{A}": "Solvent",
            },
        ),
        Symbol("m_B", where={"B": "Solute"}),
    ),
    _iso80000.LATENT_HEAT_OF_PHASE_TRANSITION: (
        Wikidata("Q106553458"),
        Symbol(r"L_{pt}"),
    ),
    _iso80000.CHEMICAL_POTENTIAL: (
        Wikidata("Q737004"),
        Equation(
            r"\mu_\mathrm{X} = \left(\frac{\partial G}{\partial n_\mathrm{X}}\right)_{T,p}",
            {
                r"\mu": SELF,
                r"\mathrm{X}": "Substance",
                "G": _iso80000.GIBBS_ENERGY,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
                "T": _iso80000.TEMPERATURE,
                "p": _iso80000.PRESSURE,
            },
        ),
    ),
    _iso80000.ABSOLUTE_ACTIVITY: (
        Wikidata("Q56638155"),
        Equation(
            r"\lambda_\mathrm{X} = \exp{\left(\frac{\mu_\mathrm{X}}{RT}\right)}",
            {
                r"\lambda": SELF,
                r"\mathrm{X}": "Substance",
                r"\mu": _iso80000.CHEMICAL_POTENTIAL,
                "R": _iso80000.MOLAR_GAS_CONSTANT,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.FUGACITY: (
        Wikidata("Q898412"),
        Equation(
            r"f_\mathrm{X} = \lambda_\mathrm{X} \lim_{p_\mathrm{X} \to 0}\left(\frac{p_\mathrm{X}}{\lambda_\mathrm{X}}\right)",
            {
                r"f": SELF,
                r"\lambda": (
                    _iso80000.ABSOLUTE_ACTIVITY,
                    " (function of ",
                    _iso80000.TEMPERATURE,
                    " only)",
                ),
                "p": _iso80000.PARTIAL_PRESSURE,
                r"\mathrm{X}": "Substance",
            },
        ),
        Symbol(r"\tilde{p}_\mathrm{X}", where={r"\mathrm{X}": "Substance"}),
    ),
    _iso80000.STANDARD_CHEMICAL_POTENTIAL: (
        Wikidata("Q89333468"),
        Equation(
            r"\mu^{\minuso}_\mathrm{B}(T, p=p^{\minuso}) = RT\ln \lambda^{\minuso}",
            {
                r"\mu^{\minuso}": SELF,
                "p": _iso80000.PRESSURE,
                r"p^{\minuso}": _iso80000.CONST_STANDARD_PRESSURE_IUPAC,
                r"\mathrm{B}": "Substance",
                "R": _iso80000.MOLAR_GAS_CONSTANT,
                "T": _iso80000.TEMPERATURE,
                r"\lambda^{\minuso}": _iso80000.STANDARD_ABSOLUTE_ACTIVITY,
            },
        ),
        Symbol(r"\mu^{\minuso}"),
    ),
    _iso80000.ACTIVITY_FACTOR: (
        Wikidata("Q89335167"),
        Equation(
            r"\gamma_\mathrm{X} = \frac{\lambda_\mathrm{X}}{\lambda_\mathrm{X}^* x_\mathrm{X}}",
            {
                r"\gamma": SELF,
                r"\mathrm{X}": "Substance in a liquid or solid mixture",
                r"\lambda": _iso80000.ABSOLUTE_ACTIVITY,
                "*": "Pure",
                "x": (
                    _iso80000.MOLE_FRACTION,
                    " at the same ",
                    _iso80000.TEMPERATURE,
                ),
            },
        ),
        Symbol(
            r"f_\mathrm{X}",
            where={r"\mathrm{X}": "Substance in a liquid or solid mixture"},
        ),
    ),
    _iso80000.STANDARD_ABSOLUTE_ACTIVITY: (
        Wikidata("Q89406159"),
        Equation(
            r"\lambda^{\minuso}_\mathrm{X}(T) = \lambda_\mathrm{X}^*(p^{\minuso})",
            {
                r"\lambda^{\minuso}": SELF,
                "T": _iso80000.TEMPERATURE,
                r"\mathrm{X}": "Substance in a liquid or solid mixture",
                r"\lambda": (
                    _iso80000.ABSOLUTE_ACTIVITY,
                    " at the same ",
                    _iso80000.TEMPERATURE,
                ),
                "*": "Pure",
                r"p^{\minuso}": _iso80000.CONST_STANDARD_PRESSURE_IUPAC,
            },
        ),
    ),
    _iso80000.ACTIVITY_OF_SOLUTE: (
        Wikidata("Q89408862"),
        Equation(
            r"a_\mathrm{X} = \lambda_\mathrm{X} \lim_{\sum b_\mathrm{X} \to 0}\left(\frac{b_\mathrm{X}/b^{\minuso}}{\lambda_\mathrm{X}}\right)^{-1}",
            {
                "a": SELF,
                r"\mathrm{X}": "Solute in a solution",
                r"\lambda": _iso80000.ABSOLUTE_ACTIVITY,
                "b": _iso80000.MOLALITY,
                r"b^{\minuso}": _iso80000.STANDARD_MOLALITY,
            },
        ),
        Symbol(
            r"a_{m,\mathrm{X}}", where={r"\mathrm{X}": "Solute in a solution"}
        ),
    ),
    _iso80000.ACTIVITY_COEFFICIENT: (
        Wikidata("Q745224"),
        Equation(
            r"\gamma_\mathrm{B} = \frac{a_\mathrm{B}}{b_\mathrm{B}/b^{\minuso}}",
            {
                r"\gamma": SELF,
                r"\mathrm{B}": "Solute in a solution",
                "a": _iso80000.ACTIVITY_OF_SOLUTE,
                "b": _iso80000.MOLALITY,
                r"b^{\minuso}": _iso80000.STANDARD_MOLALITY,
            },
        ),
    ),
    _iso80000.STANDARD_ABSOLUTE_ACTIVITY_IN_SOLUTION: (
        Wikidata("Q89485936"),
        Equation(
            r"\lambda^{\minuso}_\mathrm{B}(T) = \lim_{\sum b_\mathrm{B} \to 0}\left[\lambda_\mathrm{B}\frac{(p^{\minuso})b^{\minuso}}{b_\mathrm{B}}\right]",
            {
                r"\lambda^{\minuso}": SELF,
                "T": _iso80000.TEMPERATURE,
                r"\mathrm{B}": "Solute in a solution",
                "b": _iso80000.MOLALITY,
                r"p^{\minuso}": _iso80000.CONST_STANDARD_PRESSURE_IUPAC,
                r"b^{\minuso}": _iso80000.STANDARD_MOLALITY,
            },
        ),
    ),
    _iso80000.ACTIVITY_OF_SOLVENT: (
        Wikidata("Q89486193"),
        Equation(
            r"a_\mathrm{A} = \frac{\lambda_\mathrm{A}}{\lambda^{\minuso}_\mathrm{A}}",
            {
                "a": SELF,
                r"\mathrm{A}": "Solvent in a solution",
                r"\lambda": _iso80000.ABSOLUTE_ACTIVITY,
                r"\lambda^{\minuso}": _iso80000.STANDARD_ABSOLUTE_ACTIVITY_OF_SOLVENT,
            },
        ),
    ),
    _iso80000.OSMOTIC_PRESSURE: (Wikidata("Q193135"), Symbol(r"\Pi")),
    _iso80000.OSMOTIC_COEFFICIENT_OF_SOLVENT: (
        Wikidata("Q5776102"),
        Equation(
            r"\varphi = -\left(M_\mathrm{A}\sum_{\mathrm{B}}b_\mathrm{B}\right)^{-1}\ln a_\mathrm{A}",
            {
                r"\varphi": SELF,
                r"M": _iso80000.MOLAR_MASS,
                r"\mathrm{A}": "Solvent",
                r"\mathrm{B}": "Solutes",
                r"b": _iso80000.MOLALITY,
                r"a": _iso80000.ACTIVITY_OF_SOLVENT,
            },
        ),
    ),
    _iso80000.STANDARD_ABSOLUTE_ACTIVITY_OF_SOLVENT: (
        Wikidata("Q89556185"),
        Equation(
            r"\lambda^{\minuso}_\mathrm{A} = \lambda_\mathrm{A}^* p^{\minuso}",
            {
                r"\lambda^{\minuso}": SELF,
                r"\mathrm{A}": "Solvent",
                r"\lambda": (
                    _iso80000.ABSOLUTE_ACTIVITY,
                    " at the same ",
                    _iso80000.TEMPERATURE,
                ),
                "*": "Pure",
                r"p^{\minuso}": _iso80000.CONST_STANDARD_PRESSURE_IUPAC,
            },
        ),
    ),
    _iso80000.STOICHIOMETRIC_NUMBER: (
        Wikidata("Q17326453"),
        Equation(
            r"0 = \sum_\mathrm{B} \nu_\mathrm{B}",
            {r"\mathrm{B}": "Substance", r"\nu": SELF},
        ),
    ),
    _iso80000.AFFINITY_OF_CHEMICAL_REACTION: (
        Wikidata("Q382783"),
        Equation(
            r"A = -\sum_\mathrm{B} \nu_\mathrm{B}\mu_\mathrm{B} = \left(\frac{\partial G}{\partial \xi}\right)_{p,T}",
            {
                "A": SELF,
                r"\mathrm{B}": "Substance",
                r"\nu": _iso80000.STOICHIOMETRIC_NUMBER,
                r"\mu": _iso80000.CHEMICAL_POTENTIAL,
                "G": _iso80000.GIBBS_ENERGY,
                r"\xi": _iso80000.EXTENT_OF_REACTION,
                "p": _iso80000.PRESSURE,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.EXTENT_OF_REACTION: (
        Wikidata("Q899046"),
        Equation(
            r"\xi = \frac{(n_\mathrm{eq})_\mathrm{B} - (n_\mathrm{initial})_\mathrm{B}}{\nu_\mathrm{B}}",
            {
                r"\xi": SELF,
                r"\mathrm{B}": "Substance",
                r"n_\mathrm{eq}": _iso80000.EQUILIBRIUM_AMOUNT_OF_SUBSTANCE,
                r"n_\mathrm{initial}": _iso80000.INITIAL_AMOUNT_OF_SUBSTANCE,
                r"\nu": _iso80000.STOICHIOMETRIC_NUMBER,
            },
        ),
    ),
    _iso80000.STANDARD_EQUILIBRIUM_CONSTANT: (
        Wikidata("Q95993378"),
        Equation(
            r"K^{\minuso} = \prod_\mathrm{B} (\lambda^{\minuso}_\mathrm{B})^{-\nu_\mathrm{B}}",
            {
                r"K^{\minuso}": SELF,
                r"\mathrm{B}": "Substance",
                r"\lambda^{\minuso}": _iso80000.STANDARD_ABSOLUTE_ACTIVITY,
                r"\nu": _iso80000.STOICHIOMETRIC_NUMBER,
            },
        ),
    ),
    _iso80000.equilibrium_constant_pressure_basis: (
        Wikidata("Q96096019"),
        Equation(
            r"K_p = \prod_\mathrm{B} (p_\mathrm{B})^{\nu_\mathrm{B}}",
            {
                r"K_p": SELF,
                r"\mathrm{B}": "Substance in gas",
                r"p_\mathrm{B}": _iso80000.PARTIAL_PRESSURE,
                r"\nu": _iso80000.STOICHIOMETRIC_NUMBER,
            },
        ),
    ),
    _iso80000.equilibrium_constant_concentration_basis: (
        Wikidata("Q96096049"),
        Equation(
            r"K_c = \prod_\mathrm{B} (c_\mathrm{B})^{\nu_\mathrm{B}}",
            {
                r"K_c": SELF,
                r"\mathrm{B}": "Substance in solution",
                "c": _iso80000.MOLAR_CONCENTRATION,
                r"\nu": _iso80000.STOICHIOMETRIC_NUMBER,
            },
        ),
    ),
    _iso80000.MICROCANONICAL_PARTITION_FUNCTION: (
        Wikidata("Q96106546"),
        Equation(
            r"\Omega = \sum_r 1",
            {
                r"\Omega": SELF,
                "r": (
                    "quantum states consistent with given ",
                    _iso80000.ENERGY,
                    ", ",
                    _iso80000.VOLUME,
                    " and external fields",
                ),
            },
        ),
    ),
    _iso80000.CANONICAL_PARTITION_FUNCTION: (
        Wikidata("Q96142389"),
        Equation(
            r"Z = \sum_r \exp{\left(\frac{-E_r}{kT}\right)}",
            {
                "Z": SELF,
                "r": "Quantum states",
                "E_r": _iso80000.ENERGY,
                "k": _iso80000.CONST_BOLTZMANN,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.GRAND_CANONICAL_PARTITION_FUNCTION: (
        Wikidata("Q96176022"),
        Equation(
            r"\Xi = \sum_{N_\mathrm{A},N_\mathrm{B},...} Z(N_\mathrm{A},N_\mathrm{B},...)\lambda_\mathrm{A}^{N_\mathrm{A}}\lambda_\mathrm{B}^{N_\mathrm{B}}...",
            {
                r"\Xi": SELF,
                "Z": _iso80000.CANONICAL_PARTITION_FUNCTION,
                r"\lambda": _iso80000.ABSOLUTE_ACTIVITY,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                r"\mathrm{A}": "Particle type A",
                r"\mathrm{B}": "Particle type B",
            },
        ),
    ),
    _iso80000.MOLECULAR_PARTITION_FUNCTION: (
        Wikidata("Q96192064"),
        Equation(
            r"q = \sum_r \exp{\left(\frac{-\varepsilon_r}{kT}\right)}",
            {
                "q": SELF,
                "r": (
                    "energy level of the molecule consistent with the given ",
                    _iso80000.VOLUME,
                    " and external fields",
                ),
                r"\varepsilon": _iso80000.ENERGY,
                "k": _iso80000.CONST_AVOGADRO,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.STATISTICAL_WEIGHT_OF_SUBSYSTEM: (
        Wikidata("Q96207431"),
        Symbol("g"),
    ),
    _iso80000.MULTIPLICITY: (Wikidata("Q902301"), Symbol("g")),
    _iso80000.MOLAR_GAS_CONSTANT: (
        Wikidata("Q182333"),
        Equation(
            r"R = N_A k",
            {
                "R": SELF,
                "N_A": _iso80000.CONST_AVOGADRO,
                "k": _iso80000.CONST_BOLTZMANN,
            },
        ),
        Equation(
            r"p V_m = R T",
            {
                "p": _iso80000.PRESSURE,
                "V_m": _iso80000.MOLAR_VOLUME,
                "R": SELF,
                "T": _iso80000.TEMPERATURE,
            },
            assumptions={"ideal gas"},
        ),
        Symbol("R_m"),
    ),
    _iso80000.MEAN_FREE_PATH: (
        Wikidata("Q756307"),
        Symbol("l"),
        Symbol(r"\lambda"),
    ),
    _iso80000.DIFFUSION_COEFFICIENT: (
        Wikidata("Q604008"),
        Equation(
            r"C_\mathrm{B}\langle(\boldsymbol{v}_\mathrm{average})_\mathrm{B}\rangle = -D\nabla C_\mathrm{B}",
            {
                r"C": ("Local ", _iso80000.NUMBER_DENSITY),
                r"\mathrm{B}": "Substance in the mixture",
                r"\boldsymbol{v}": ("Local ", _iso80000.VELOCITY),
                "D": SELF,
            },
        ),
    ),
    _iso80000.THERMAL_DIFFUSION_RATIO: (
        Wikidata("Q96249433"),
        Equation(
            r"\nabla x_\mathrm{B} = -\frac{k_T}{T} \nabla T",
            {
                r"x": _iso80000.MOLE_FRACTION,
                "k_T": SELF,
                "T": ("Local ", _iso80000.TEMPERATURE),
                r"\mathrm{B}": "Heavier substance",
            },
            assumptions={"steady state", "binary mixture"},
        ),
    ),
    _iso80000.THERMAL_DIFFUSION_FACTOR: (
        Wikidata("Q96249629"),
        Equation(
            r"\alpha_T = \frac{k_T}{x_\mathrm{A} x_\mathrm{B}}",
            {
                r"\alpha_T": SELF,
                "k_T": _iso80000.THERMAL_DIFFUSION_RATIO,
                "x": _iso80000.MOLE_FRACTION,
                r"\mathrm{A}": "Substance A",
                r"\mathrm{B}": "Substance B",
            },
        ),
    ),
    _iso80000.THERMAL_DIFFUSION_COEFFICIENT: (
        Wikidata("Q96249751"),
        Equation(
            r"D_T = k_T D",
            {
                "D_T": SELF,
                "k_T": _iso80000.THERMAL_DIFFUSION_RATIO,
                "D": _iso80000.DIFFUSION_COEFFICIENT,
            },
        ),
    ),
    _iso80000.IONIC_STRENGTH: (
        Wikidata("Q898396"),
        Equation(
            r"I = \frac{1}{2}\sum_i z_i^2 b_i",
            {
                "I": SELF,
                "z": _iso80000.CHARGE_NUMBER,
                "b": _iso80000.MOLALITY,
                "i": "Ions",
            },
        ),
    ),
    _iso80000.DEGREE_OF_DISSOCIATION: (
        Wikidata("Q907334"),
        Equation(
            r"\alpha = \frac{n_d}{n_\text{total}}",
            {
                r"\alpha": SELF,
                "n": _iso80000.NUMBER_OF_ENTITIES,
                "d": "Dissociated molecules",
            },
        ),
    ),
    _iso80000.ELECTROLYTIC_CONDUCTIVITY: (
        Wikidata("Q907564"),
        Equation(
            r"\kappa = \frac{J}{E}",
            {
                r"\kappa": SELF,
                "J": _iso80000.CURRENT_DENSITY,
                "E": _iso80000.ELECTRIC_FIELD_STRENGTH,
            },
        ),
    ),
    _iso80000.MOLAR_CONDUCTIVITY: (
        Wikidata("Q1943278"),
        Equation(
            r"\Lambda_\mathrm{m} = \frac{\kappa}{c_\mathrm{B}}",
            {
                r"\Lambda": SELF,
                r"\kappa": _iso80000.ELECTROLYTIC_CONDUCTIVITY,
                "c": _iso80000.MOLAR_CONCENTRATION,
                r"\mathrm{B}": "Substance",
            },
        ),
    ),
    _iso80000.TRANSPORT_NUMBER_OF_ION: (
        Wikidata("Q331854"),
        Equation(
            r"t_\mathrm{B} = \frac{i_\mathrm{B}}{i_\text{total}}",
            {"t": SELF, r"\mathrm{B}": "Ion", "i": _iso80000.CURRENT},
        ),
    ),
    _iso80000.ANGLE_OF_OPTICAL_ROTATION: (
        Wikidata("Q96323385"),
        Symbol(r"\alpha"),
    ),
    _iso80000.MOLAR_OPTICAL_ROTATORY_POWER: (
        Wikidata("Q96346994"),
        Equation(
            r"\alpha_n = \alpha\frac{A}{n}",
            {
                r"\alpha_n": SELF,
                r"\alpha": _iso80000.ANGLE_OF_OPTICAL_ROTATION,
                "A": _iso80000.AREA_CROSS_SECTION_LINEARLY_POLARIZED,
                "n": _iso80000.AMOUNT_OF_SUBSTANCE,
            },
        ),
    ),
    _iso80000.SPECIFIC_OPTICAL_ROTATORY_POWER: (
        Wikidata("Q2191631"),
        Equation(
            r"\alpha_m = \alpha\frac{A}{m}",
            {
                r"\alpha_m": SELF,
                r"\alpha": _iso80000.ANGLE_OF_OPTICAL_ROTATION,
                "A": _iso80000.AREA_CROSS_SECTION_LINEARLY_POLARIZED,
                "m": _iso80000.MASS,
            },
        ),
    ),
}
ATOMIC_AND_NUCLEAR_PHYSICS: Details = {
    _iso80000.ATOMIC_NUMBER: (Wikidata("Q23809"), Symbol("Z")),
    _iso80000.NEUTRON_NUMBER: (Wikidata("Q970319"), Symbol("N")),
    _iso80000.NUCLEON_NUMBER: (
        Wikidata("Q101395"),
        Equation(
            r"A = Z + N",
            {
                "A": SELF,
                "Z": _iso80000.ATOMIC_NUMBER,
                "N": _iso80000.NEUTRON_NUMBER,
            },
        ),
    ),
    _iso80000.REST_MASS: (
        Wikidata("Q96941619"),
        Symbol(r"m(\mathrm{X})", {r"\mathrm{X}": "Particle"}),
        Symbol(r"m_\mathrm{X}", {r"\mathrm{X}": "Particle"}),
    ),
    _iso80000.REST_ENERGY: (
        Wikidata("Q11663629"),
        Equation(
            r"E_0 = m_0 c_0^2",
            {
                "E_0": SELF,
                "m_0": _iso80000.REST_MASS,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
            },
        ),
    ),
    _iso80000.ATOMIC_MASS: (
        Wikidata("Q3840065"),
        Symbol(r"m(\mathrm{X})", where={r"\mathrm{X}": "Atom"}),
        Symbol(r"m_\mathrm{X}", where={r"\mathrm{X}": "Atom"}),
    ),
    _iso80000.NUCLIDIC_MASS: (
        Wikidata("Q97010809"),
        Symbol(r"m(\mathrm{X})", where={r"\mathrm{X}": "Nuclide"}),
        Symbol(r"m_\mathrm{X}", where={r"\mathrm{X}": "Nuclide"}),
    ),
    _iso80000.UNIFIED_ATOMIC_MASS_CONSTANT: (
        Wikidata("Q4817337"),
        Symbol(r"m_u"),
    ),
    _iso80000.CHARGE_NUMBER: (Wikidata("Q1800063"), Symbol("c")),
    _iso80000.BOHR_RADIUS: (
        Wikidata("Q652571"),
        Equation(
            r"a_0 = \frac{4\pi\varepsilon_0 \hbar^2}{m_e e^2}",
            {
                "a_0": SELF,
                r"\varepsilon_0": _iso80000.CONST_PERMITTIVITY_VACUUM,
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                "m_e": _iso80000.REST_MASS,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
            },
        ),
    ),  # TODO: make constant
    _iso80000.RYDBERG_CONSTANT: (
        Wikidata("Q658065"),
        Equation(
            r"R_\infty = \frac{m_e e^4}{8\varepsilon_0^2 h^2 c_0}",
            {
                r"R_\infty": SELF,
                "m_e": _iso80000.REST_MASS,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                r"\varepsilon_0": _iso80000.CONST_PERMITTIVITY_VACUUM,
                "h": _iso80000.CONST_PLANCK,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
            },
        ),
    ),  # TODO: make constant
    _iso80000.HARTREE_ENERGY: (
        Wikidata("Q476572"),
        Equation(
            r"E_H = \frac{e^2}{4\pi\varepsilon_0 a_0}",
            {
                "E_H": SELF,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                r"\varepsilon_0": _iso80000.CONST_PERMITTIVITY_VACUUM,
                "a_0": _iso80000.BOHR_RADIUS,
            },
        ),
    ),
    _iso80000.ATOMIC_MAGNETIC_DIPOLE_MOMENT: (
        Wikidata("Q97143703"),
        Equation(
            r"\Delta W = -\boldsymbol{\mu} \cdot \boldsymbol{B}",
            {
                r"\Delta W": _iso80000.ENERGY,
                r"\boldsymbol{\mu}": SELF,
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.BOHR_MAGNETON: (
        Wikidata("Q737120"),
        Equation(
            r"\mu_B = \frac{e\hbar}{2m_e}",
            {
                r"\mu_B": SELF,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                "m_e": _iso80000.REST_MASS,
            },
        ),
    ),  # TODO: make constant
    _iso80000.NUCLEAR_MAGNETON: (
        Wikidata("Q1166093"),
        Equation(
            r"\mu_N = \frac{e\hbar}{2m_p}",
            {
                r"\mu_N": SELF,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                "m_p": _iso80000.REST_MASS,
            },
        ),
    ),  # TODO: make constant
    _iso80000.SPIN: (Wikidata("Q133673"), Symbol("s")),
    _iso80000.TOTAL_ANGULAR_MOMENTUM: (
        Wikidata("Q97496506"),
        Equation(
            r"\boldsymbol{J} = \boldsymbol{L} + \boldsymbol{s}",
            {
                r"\boldsymbol{J}": SELF,
                r"\boldsymbol{L}": _iso80000.ANGULAR_MOMENTUM,
                r"\boldsymbol{s}": _iso80000.SPIN,
            },
        ),
    ),
    _iso80000.GYROMAGNETIC_RATIO: (
        Wikidata("Q634552"),
        Equation(
            r"\boldsymbol{\mu} = \gamma \boldsymbol{J}",
            {
                r"\boldsymbol{\mu}": _iso80000.ATOMIC_MAGNETIC_DIPOLE_MOMENT,
                r"\gamma": SELF,
                r"\boldsymbol{J}": _iso80000.TOTAL_ANGULAR_MOMENTUM,
            },
        ),
    ),  # NOTE: wikidata missing this
    _iso80000.ELECTRON_GYROMAGNETIC_RATIO: (
        Wikidata("Q97543076"),
        Equation(
            r"\boldsymbol{\mu} = \gamma_e \boldsymbol{J}",
            {
                r"\boldsymbol{\mu}": _iso80000.ATOMIC_MAGNETIC_DIPOLE_MOMENT,
                r"\gamma_e": SELF,
                r"\boldsymbol{J}": _iso80000.TOTAL_ANGULAR_MOMENTUM,
            },
        ),
    ),
    _iso80000.QUANTUM_NUMBER: (
        Wikidata("Q232431"),
        Symbol("N"),
        Symbol("L"),
        Symbol("m"),
        Symbol("j"),
        Symbol("s"),
        Symbol("F"),
    ),
    _iso80000.PRINCIPAL_QUANTUM_NUMBER: (Wikidata("Q867448"), Symbol("n")),
    _iso80000.ORBITAL_ANGULAR_MOMENTUM_QUANTUM_NUMBER: (
        Wikidata("Q1916324"),
        Symbol("l"),
        Symbol("L"),
    ),
    _iso80000.MAGNETIC_QUANTUM_NUMBER: (
        Wikidata("Q2009727"),
        Symbol("m"),
        Symbol(r"m_l"),
        Symbol("M"),
    ),
    _iso80000.SPIN_QUANTUM_NUMBER: (
        Wikidata("Q3879445"),
        Equation(
            r"|\boldsymbol{s}|^2 = \hbar^2 s(s+1)",
            {
                r"\boldsymbol{s}": _iso80000.SPIN,
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                "s": SELF,
            },
        ),
    ),
    _iso80000.TOTAL_ANGULAR_MOMENTUM_QUANTUM_NUMBER: (
        Wikidata("Q1141095"),
        Symbol("j"),
        Symbol(r"j_j"),
        Symbol("J"),
    ),
    _iso80000.NUCLEAR_SPIN_QUANTUM_NUMBER: (
        Wikidata("Q97577403"),
        Equation(
            r"|\boldsymbol{J}|^2 = \hbar^2 I(I+1)",
            {
                r"\boldsymbol{J}": (
                    _iso80000.ANGULAR_MOMENTUM,
                    " of a nucleus",
                ),
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                "I": SELF,
            },
        ),
    ),
    _iso80000.HYPERFINE_STRUCTURE_QUANTUM_NUMBER: (
        Wikidata("Q97577449"),
        Symbol("F"),
    ),
    _iso80000.LANDE_FACTOR: (
        Wikidata("Q1191684"),
        Equation(
            r"g = \frac{\mu}{J\mu_B}",
            {
                "g": SELF,
                r"\mu": _iso80000.ATOMIC_MAGNETIC_DIPOLE_MOMENT,
                "J": _iso80000.TOTAL_ANGULAR_MOMENTUM_QUANTUM_NUMBER,
                r"\mu_B": _iso80000.BOHR_MAGNETON,
            },
        ),
    ),
    _iso80000.G_FACTOR_NUCLEUS: (
        Wikidata("Q97591250"),
        Equation(
            r"g = \frac{\mu}{I\mu_N}",
            {
                "g": SELF,
                r"\mu": _iso80000.ATOMIC_MAGNETIC_DIPOLE_MOMENT,
                "I": _iso80000.NUCLEAR_SPIN_QUANTUM_NUMBER,
                r"\mu_N": _iso80000.NUCLEAR_MAGNETON,
            },
        ),
    ),
    _iso80000.LARMOR_ANGULAR_FREQUENCY: (
        Wikidata("Q97617059"),
        Equation(
            r"\omega_L = -\frac{e}{2m_e}B",
            {
                r"\omega_L": SELF,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                "m_e": (_iso80000.REST_MASS, " of electron"),
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.LARMOR_FREQUENCY: (
        Wikidata("Q97617324"),
        Equation(
            r"\nu_L = \frac{\omega_L}{2\pi}",
            {r"\nu_L": SELF, r"\omega_L": _iso80000.LARMOR_ANGULAR_FREQUENCY},
        ),
    ),
    _iso80000.LARMOR_PRECESSION_ANGULAR_FREQUENCY: (
        Wikidata("Q97641779"),
        Equation(
            r"\omega_N = \gamma B",
            {
                r"\omega_N": SELF,
                r"\gamma": _iso80000.GYROMAGNETIC_RATIO,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.CYCLOTRON_ANGULAR_FREQUENCY: (
        Wikidata("Q97708211"),
        Equation(
            r"\omega_c = \frac{|q|}{m}B",
            {
                r"\omega_c": SELF,
                "q": _iso80000.ELECTRIC_CHARGE,
                "m": _iso80000.MASS,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.GYRORADIUS: (
        Wikidata("Q1194458"),
        Equation(
            r"r_c = \frac{m|\boldsymbol{v}\times\boldsymbol{B}|}{qB^2}",
            {
                r"r_c": SELF,
                "m": _iso80000.MASS,
                r"\boldsymbol{v}": _iso80000.VELOCITY,
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
                "q": _iso80000.ELECTRIC_CHARGE,
            },
        ),
        Symbol("r_L"),
    ),
    _iso80000.NUCLEAR_QUADRUPOLE_MOMENT: (
        Wikidata("Q97921226"),
        Equation(
            r"Q = \frac{1}{e}\int (3z^2-r^2)\rho(x,y,z)dV",
            {
                "Q": SELF,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                "z": _iso80000.POSITION,
                "r": _iso80000.RADIUS,
                r"\rho": _iso80000.CHARGE_DENSITY,
                "dV": _iso80000.VOLUME_ELEMENT,
            },
        ),
    ),
    _iso80000.NUCLEAR_RADIUS: (
        Wikidata("Q3535676"),
        Equation(
            r"R = r_0 A^{1/3}",
            {
                "R": SELF,
                "r_0": "Empirical constant",
                "A": _iso80000.NUCLEON_NUMBER,
            },
        ),
    ),
    _iso80000.ELECTRON_RADIUS: (
        Wikidata("Q2152581"),
        Equation(
            r"r_e = \frac{e^2}{4\pi\varepsilon_0 m_e c_0^2}",
            {
                "r_e": SELF,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                r"\varepsilon_0": _iso80000.CONST_PERMITTIVITY_VACUUM,
                "m_e": _iso80000.REST_MASS,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
            },
        ),
    ),
    _iso80000.COMPTON_WAVELENGTH: (
        Wikidata("Q1145377"),
        Equation(
            r"\lambda_C = \frac{h}{m c_0}",
            {
                r"\lambda_C": SELF,
                "h": _iso80000.CONST_PLANCK,
                "m": _iso80000.REST_MASS,
                "c_0": _iso80000.CONST_SPEED_OF_LIGHT_VACUUM,
            },
        ),
    ),
    _iso80000.MASS_EXCESS: (
        Wikidata("Q1571163"),
        Equation(
            r"\Delta = m_a - A m_u",
            {
                r"\Delta": SELF,
                "m_a": _iso80000.ATOMIC_MASS,
                "A": _iso80000.NUCLEON_NUMBER,
                "m_u": _iso80000.UNIFIED_ATOMIC_MASS_CONSTANT,
            },
        ),
    ),
    _iso80000.MASS_DEFECT: (
        Wikidata("Q26897126"),
        Equation(
            r"B = Z m(^1\mathrm{H}) + N m_n - m_a",
            {
                "B": SELF,
                "Z": _iso80000.ATOMIC_NUMBER,
                "m": _iso80000.ATOMIC_MASS,
                "N": _iso80000.NEUTRON_NUMBER,
                "m_n": _iso80000.REST_MASS,
                "m_a": _iso80000.ATOMIC_MASS,
            },
        ),
    ),
    _iso80000.RELATIVE_MASS_EXCESS: (
        Wikidata("Q98038610"),
        Equation(
            r"\Delta_r = \frac{\Delta}{m_u}",
            {
                r"\Delta_r": SELF,
                r"\Delta": _iso80000.MASS_EXCESS,
                "m_u": _iso80000.UNIFIED_ATOMIC_MASS_CONSTANT,
            },
        ),
    ),
    _iso80000.RELATIVE_MASS_DEFECT: (
        Wikidata("Q98038718"),
        Equation(
            r"B_r = \frac{B}{m_u}",
            {
                "B_r": SELF,
                "B": _iso80000.MASS_DEFECT,
                "m_u": _iso80000.UNIFIED_ATOMIC_MASS_CONSTANT,
            },
        ),
    ),
    _iso80000.PACKING_FRACTION: (
        Wikidata("Q98058276"),
        Equation(
            r"f = \frac{\Delta_r}{A}",
            {
                "f": SELF,
                r"\Delta_r": _iso80000.RELATIVE_MASS_EXCESS,
                "A": _iso80000.NUCLEON_NUMBER,
            },
        ),
    ),
    _iso80000.BINDING_FRACTION: (
        Wikidata("Q98058362"),
        Equation(
            r"b = \frac{B_r}{A}",
            {
                "b": SELF,
                "B_r": _iso80000.RELATIVE_MASS_DEFECT,
                "A": _iso80000.NUCLEON_NUMBER,
            },
        ),
    ),
    _iso80000.DECAY_CONSTANT: (
        Wikidata("Q11477200"),
        Equation(
            r"\lambda = -\frac{1}{N}\frac{dN}{dt}",
            {
                r"\lambda": SELF,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.MEAN_LIFE_TIME: (
        Wikidata("Q1758559"),
        Equation(
            r"\tau = \frac{1}{\lambda}",
            {r"\tau": SELF, r"\lambda": _iso80000.DECAY_CONSTANT},
        ),
    ),
    _iso80000.LEVEL_WIDTH: (
        Wikidata("Q98082340"),
        Equation(
            r"\Gamma = \frac{\hbar}{\tau}",
            {
                r"\Gamma": SELF,
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                r"\tau": _iso80000.MEAN_LIFE_TIME,
            },
        ),
    ),
    _iso80000.ACTIVITY: (
        Wikidata("Q317949"),
        Equation(
            r"A = -\frac{dN}{dt}",
            {"A": SELF, "N": _iso80000.NUMBER_OF_ENTITIES, "t": _iso80000.TIME},
        ),
    ),
    _iso80000.SPECIFIC_ACTIVITY: (
        Wikidata("Q2823748"),
        Equation(
            r"a = \frac{A}{m}",
            {"a": SELF, "A": _iso80000.ACTIVITY, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.ACTIVITY_DENSITY: (
        Wikidata("Q423263"),
        Equation(
            r"c_A = \frac{A}{V}",
            {"c_A": SELF, "A": _iso80000.ACTIVITY, "V": _iso80000.VOLUME},
        ),
    ),
    _iso80000.SURFACE_ACTIVITY_DENSITY: (
        Wikidata("Q98103005"),
        Equation(
            r"a_S = \frac{A}{S}",
            {"a_S": SELF, "A": _iso80000.ACTIVITY, "S": _iso80000.AREA},
        ),
    ),
    _iso80000.HALF_LIFE: (
        Wikidata("Q98118544"),
        Equation(
            r"T_{1/2} = \frac{\ln 2}{\lambda}",
            {"T_{1/2}": SELF, r"\lambda": _iso80000.DECAY_CONSTANT},
        ),
    ),
    _iso80000.ALPHA_DISINTEGRATION_ENERGY: (
        Wikidata("Q98146025"),
        Symbol(r"Q_\alpha"),
    ),
    _iso80000.MAXIMUM_BETA_PARTICLE_ENERGY: (
        Wikidata("Q98148038"),
        Symbol(r"E_\beta"),
    ),
    _iso80000.BETA_DISINTEGRATION_ENERGY: (
        Wikidata("Q98148340"),
        Symbol(r"Q_\beta"),
    ),
    _iso80000.INTERNAL_CONVERSION_FACTOR: (
        Wikidata("Q6047819"),
        Symbol(r"\alpha"),
    ),
    _iso80000.PARTICLE_EMISSION_RATE: (
        Wikidata("Q98153151"),
        Equation(
            r"\dot{N} = \frac{dN}{dt}",
            {
                r"\dot{N}": SELF,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.REACTION_ENERGY: (Wikidata("Q98164745"), Symbol("Q")),
    _iso80000.RESONANCE_ENERGY: (
        Wikidata("Q98165187"),
        Symbol(r"E_\text{res}"),
    ),
    _iso80000.CROSS_SECTION: (Wikidata("Q17128025"), Symbol(r"\sigma")),
    _iso80000.TOTAL_CROSS_SECTION: (
        Wikidata("Q98206553"),
        Symbol(r"\sigma_\text{tot}"),
    ),
    _iso80000.DIRECTION_DISTRIBUTION_OF_CROSS_SECTION: (
        Wikidata("Q98266630"),
        Equation(
            r"\sigma_\Omega = \frac{d\sigma}{d\Omega}",
            {
                r"\sigma_\Omega": SELF,
                r"\sigma": _iso80000.CROSS_SECTION,
                r"\Omega": _iso80000.SOLID_ANGLE,
            },
        ),
    ),
    _iso80000.ENERGY_DISTRIBUTION_OF_CROSS_SECTION: (
        Wikidata("Q98267245"),
        Equation(
            r"\sigma_E = \frac{d\sigma}{dE}",
            {
                r"\sigma_E": SELF,
                r"\sigma": _iso80000.CROSS_SECTION,
                "E": _iso80000.ENERGY,
            },
        ),
    ),
    _iso80000.DIRECTION_AND_ENERGY_DISTRIBUTION_OF_CROSS_SECTION: (
        Wikidata("Q98269571"),
        Equation(
            r"\sigma_{\Omega,E} = \frac{\partial^2\sigma}{\partial\Omega\partial E}",
            {
                r"\sigma_{\Omega,E}": SELF,
                r"\sigma": _iso80000.CROSS_SECTION,
                r"\Omega": _iso80000.SOLID_ANGLE,
                "E": _iso80000.ENERGY,
            },
        ),
    ),
    _iso80000.VOLUMIC_CROSS_SECTION: (
        Wikidata("Q98280520"),
        Equation(
            r"\Sigma = n_a \sigma_a",
            {
                r"\Sigma": SELF,
                "n_a": _iso80000.NUMBER_DENSITY,
                r"\sigma_a": _iso80000.CROSS_SECTION,
            },
        ),
    ),
    _iso80000.VOLUMIC_TOTAL_CROSS_SECTION: (
        Wikidata("Q98280548"),
        Equation(
            r"\Sigma_\text{tot} = n_a \sigma_\text{tot}",
            {
                r"\Sigma_\text{tot}": SELF,
                "n_a": _iso80000.NUMBER_DENSITY,
                r"\sigma_\text{tot}": _iso80000.TOTAL_CROSS_SECTION,
            },
        ),
    ),
    _iso80000.PARTICLE_FLUENCE: (
        Wikidata("Q82965908"),
        Equation(
            r"\Phi = \frac{dN}{da}",
            {
                r"\Phi": SELF,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "a": _iso80000.CROSS_SECTION,
            },
        ),
    ),
    _iso80000.PARTICLE_FLUENCE_RATE: (
        Wikidata("Q98497410"),
        Equation(
            r"\dot{\Phi} = \frac{d\Phi}{dt}",
            {
                r"\dot{\Phi}": SELF,
                r"\Phi": _iso80000.PARTICLE_FLUENCE,
                "t": _iso80000.TIME,
            },
        ),
        Symbol(r"\varphi"),
    ),
    _iso80000.IONIZING_RADIANT_ENERGY: (Wikidata("Q98538346"), Symbol("R")),
    _iso80000.ENERGY_FLUENCE: (
        Wikidata("Q98538612"),
        Equation(
            r"\Psi = \frac{dR}{da}",
            {
                r"\Psi": SELF,
                "R": _iso80000.IONIZING_RADIANT_ENERGY,
                "a": _iso80000.CROSS_SECTION,
            },
        ),
    ),
    _iso80000.ENERGY_FLUENCE_RATE: (
        Wikidata("Q65274525"),
        Equation(
            r"\dot{\Psi} = \frac{d\Psi}{dt}",
            {
                r"\dot{\Psi}": SELF,
                r"\Psi": _iso80000.ENERGY_FLUENCE,
                "t": _iso80000.TIME,
            },
        ),
        Symbol(r"\psi"),
    ),
    _iso80000.PARTICLE_CURRENT_DENSITY: (Wikidata("Q2400689"), Symbol("J")),
    _iso80000.IONIZING_LINEAR_ATTENUATION_COEFFICIENT: (
        Wikidata("Q98583077"),
        Equation(
            r"\mu = \frac{1}{N}\frac{dN}{dl}",
            {
                r"\mu": SELF,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "l": _iso80000.LENGTH,
            },
        ),
        Symbol(r"\mu_l"),
    ),
    _iso80000.IONIZING_MASS_ATTENUATION_COEFFICIENT: (
        Wikidata("Q98591983"),
        Equation(
            r"\mu_m = \frac{\mu}{\rho}",
            {
                r"\mu_m": SELF,
                r"\mu": _iso80000.IONIZING_LINEAR_ATTENUATION_COEFFICIENT,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.MOLAR_ATTENUATION_COEFFICIENT: (
        Wikidata("Q98592828"),
        Equation(
            r"\mu_c = \frac{\mu}{c}",
            {
                r"\mu_c": SELF,
                r"\mu": _iso80000.IONIZING_LINEAR_ATTENUATION_COEFFICIENT,
                "c": _iso80000.MOLAR_CONCENTRATION,
            },
        ),
    ),
    _iso80000.ATOMIC_ATTENUATION_COEFFICIENT: (
        Wikidata("Q98592911"),
        Equation(
            r"\mu_a = \frac{\mu}{n}",
            {
                r"\mu_a": SELF,
                r"\mu": _iso80000.IONIZING_LINEAR_ATTENUATION_COEFFICIENT,
                "n": _iso80000.NUMBER_DENSITY,
            },
        ),
    ),
    _iso80000.HALF_VALUE_THICKNESS: (Wikidata("Q127526"), Symbol(r"d_{1/2}")),
    _iso80000.TOTAL_LINEAR_STOPPING_POWER: (
        Wikidata("Q908474"),
        Equation(
            r"S = -\frac{dE}{dx}",
            {
                "S": SELF,
                "E": (_iso80000.ENERGY, " lost by charged particles"),
                "x": _iso80000.DISTANCE,
            },
        ),
        Symbol("S_l"),
    ),
    _iso80000.TOTAL_MASS_STOPPING_POWER: (
        Wikidata("Q98642795"),
        Equation(
            r"S_m = \frac{S_l}{\rho}",
            {
                "S_m": SELF,
                "S_l": _iso80000.TOTAL_LINEAR_STOPPING_POWER,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.MEAN_LINEAR_RANGE: (
        Wikidata("Q98681589"),
        Symbol("R"),
        Symbol(r"R_l"),
    ),
    _iso80000.MEAN_MASS_RANGE: (
        Wikidata("Q98681670"),
        Symbol(r"R_\rho"),
        Equation(
            r"R_m = R_l \rho",
            {
                "R_m": SELF,
                r"R_l": _iso80000.MEAN_LINEAR_RANGE,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.LINEAR_IONIZATION: (
        Wikidata("Q98690755"),
        Equation(
            r"N_\mathrm{il} = \frac{1}{e}\frac{dq}{dl}",
            {
                r"N_\mathrm{il}": SELF,
                "e": _iso80000.CONST_ELEMENTARY_CHARGE,
                "q": _iso80000.ELECTRIC_CHARGE,
                "l": _iso80000.LENGTH,
            },
        ),
    ),
    _iso80000.TOTAL_IONIZATION: (
        Wikidata("Q98690787"),
        Equation(
            r"N_i = \int N_\mathrm{il} dl",
            {
                "N_i": SELF,
                r"N_\mathrm{il}": _iso80000.LINEAR_IONIZATION,
                "l": _iso80000.LENGTH,
            },
        ),
    ),
    _iso80000.AVERAGE_ENERGY_LOSS_PER_ELEMENTARY_CHARGE_PRODUCED: (
        Wikidata("Q98793042"),
        Equation(
            r"W_i = \frac{E_k}{N_i}",
            {
                "W_i": SELF,
                "E_k": _iso80000.KINETIC_ENERGY,
                "N_i": _iso80000.TOTAL_IONIZATION,
            },
        ),
    ),
    _iso80000.MOBILITY: (Wikidata("Q900648"), Symbol(r"\mu"), Symbol(r"\mu_m")),
    _iso80000.PARTICLE_NUMBER_DENSITY: (
        Wikidata("Q98601569"),
        Equation(
            r"n = \frac{N}{V}",
            {
                "n": SELF,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.ION_NUMBER_DENSITY: (
        Wikidata("Q98831218"),
        Equation(
            r"n^\pm = \frac{N^\pm}{V}",
            {
                "n": SELF,
                "N": _iso80000.NUMBER_OF_ENTITIES,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.RECOMBINATION_COEFFICIENT: (
        Wikidata("Q98842099"),
        Equation(
            r"-\frac{dn^\pm}{dt} = \alpha n^+ n^-",
            {
                r"\alpha": SELF,
                "n": _iso80000.ION_NUMBER_DENSITY,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.DIFFUSION_COEFFICIENT_PARTICLE_NUMBER_DENSITY: (
        Wikidata("Q98875545"),
        Equation(
            r"J = -D_n \nabla n",
            {
                "J": _iso80000.PARTICLE_CURRENT_DENSITY,
                "D_n": SELF,
                "n": _iso80000.PARTICLE_NUMBER_DENSITY,
            },
        ),
        Symbol("D"),
    ),
    _iso80000.DIFFUSION_COEFFICIENT_FLUENCE_RATE: (
        Wikidata("Q98876254"),
        Equation(
            r"J = -D \nabla \dot{\Phi}",
            {
                "J": _iso80000.PARTICLE_CURRENT_DENSITY,
                r"D": SELF,
                r"\dot{\Phi}": _iso80000.PARTICLE_FLUENCE_RATE,
            },
        ),
        Symbol(r"D_\Phi"),
    ),
    _iso80000.PARTICLE_SOURCE_DENSITY: (Wikidata("Q98915762"), Symbol("S")),
    _iso80000.SLOWING_DOWN_DENSITY: (
        Wikidata("Q98915830"),
        Equation(
            r"q = \frac{dn}{dt}",  # NOTE: wikidata has negative sign?
            {"q": SELF, "n": _iso80000.NUMBER_OF_ENTITIES, "t": _iso80000.TIME},
        ),
    ),
    _iso80000.RESONANCE_ESCAPE_PROBABILITY: (Wikidata("Q4108072"), Symbol("p")),
    _iso80000.LETHARGY: (
        Wikidata("Q25508781"),
        Equation(
            r"u = \ln(E_0/E)",
            {"u": SELF, "E_0": "Reference energy", "E": _iso80000.ENERGY},
        ),
    ),
    _iso80000.AVERAGE_LOGARITHMIC_ENERGY_DECREMENT: (
        Wikidata("Q1940739"),
        Symbol(r"\xi"),
    ),
    _iso80000.MEAN_FREE_PATH_ATOMIC: (
        Wikidata("Q98950584"),
        Symbol("l"),
        Symbol(r"\lambda"),
    ),
    _iso80000.SLOWING_DOWN_AREA: (Wikidata("Q98950918"), Symbol(r"L_s^2")),
    _iso80000.DIFFUSION_AREA: (Wikidata("Q98966292"), Symbol(r"L^2")),
    _iso80000.MIGRATION_AREA: (Wikidata("Q98966325"), Symbol(r"M^2")),
    _iso80000.SLOWING_DOWN_LENGTH: (
        Wikidata("Q98996963"),
        Equation(
            r"L_s = \sqrt{L_s^2}",
            {"L_s": SELF, r"L_s^2": _iso80000.SLOWING_DOWN_AREA},
        ),
    ),
    _iso80000.DIFFUSION_LENGTH_ATOMIC: (
        Wikidata("Q98997762"),
        Equation(
            r"L = \sqrt{L^2}", {"L": SELF, r"L^2": _iso80000.DIFFUSION_AREA}
        ),
    ),
    _iso80000.MIGRATION_LENGTH: (
        Wikidata("Q98998318"),
        Equation(
            r"M = \sqrt{M^2}", {"M": SELF, r"M^2": _iso80000.MIGRATION_AREA}
        ),
    ),
    _iso80000.NEUTRON_YIELD_PER_FISSION: (
        Wikidata("Q99157909"),
        Symbol(r"\nu"),
    ),
    _iso80000.NEUTRON_YIELD_PER_ABSORPTION: (
        Wikidata("Q99159075"),
        Symbol(r"\eta"),
    ),
    _iso80000.FAST_FISSION_FACTOR: (Wikidata("Q99197493"), Symbol(r"\varphi")),
    _iso80000.THERMAL_UTILIZATION_FACTOR: (Wikidata("Q99197650"), Symbol("f")),
    _iso80000.NON_LEAKAGE_PROBABILITY: (
        Wikidata("Q99415566"),
        Symbol(r"\Lambda"),
    ),
    _iso80000.MULTIPLICATION_FACTOR: (Wikidata("Q99440471"), Symbol("k")),
    _iso80000.INFINITE_MULTIPLICATION_FACTOR: (
        Wikidata("Q99440487"),
        Symbol(r"k_\infty"),
    ),
    _iso80000.REACTOR_TIME_CONSTANT: (Wikidata("Q99518950"), Symbol("T")),
    _iso80000.ENERGY_IMPARTED: (
        Wikidata("Q99526944"),
        Equation(r"\varepsilon = \sum_i \varepsilon_i", {r"\varepsilon": SELF}),
    ),
    _iso80000.MEAN_ENERGY_IMPARTED: (
        Wikidata("Q99526969"),
        Equation(
            r"\bar{\varepsilon} = R_\text{in} - R_\text{out} + \sum Q",
            {
                r"\bar{\varepsilon}": SELF,
                "R": _iso80000.IONIZING_RADIANT_ENERGY,
                "Q": _iso80000.REST_ENERGY,
            },
        ),
    ),
    _iso80000.ABSORBED_DOSE: (
        Wikidata("Q215313"),
        Equation(
            r"D = \frac{d\bar{\varepsilon}}{dm}",
            {
                "D": SELF,
                r"\bar{\varepsilon}": _iso80000.MEAN_ENERGY_IMPARTED,
                "m": _iso80000.MASS,
            },
        ),
    ),
    _iso80000.SPECIFIC_ENERGY_IMPARTED: (
        Wikidata("Q99566195"),
        Equation(
            r"z = \frac{\varepsilon}{m}",
            {
                "z": SELF,
                r"\varepsilon": _iso80000.ENERGY_IMPARTED,
                "m": _iso80000.MASS,
            },
        ),
    ),
    _iso80000.IONIZING_QUALITY_FACTOR: (Wikidata("Q2122099"), Symbol("Q")),
    _iso80000.DOSE_EQUIVALENT: (
        Wikidata("Q256106"),
        Equation(
            r"H = DQ",
            {
                "H": SELF,
                "D": _iso80000.ABSORBED_DOSE,
                "Q": _iso80000.IONIZING_QUALITY_FACTOR,
            },
        ),
    ),
    _iso80000.DOSE_EQUIVALENT_RATE: (
        Wikidata("Q99604810"),
        Equation(
            r"\dot{H} = \frac{dH}{dt}",
            {
                r"\dot{H}": SELF,
                "H": _iso80000.DOSE_EQUIVALENT,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.ABSORBED_DOSE_RATE: (
        Wikidata("Q69428958"),
        Equation(
            r"\dot{D} = \frac{dD}{dt}",
            {
                r"\dot{D}": SELF,
                "D": _iso80000.ABSORBED_DOSE,
                "t": _iso80000.TIME,
            },
        ),
    ),
    _iso80000.LINEAR_ENERGY_TRANSFER: (
        Wikidata("Q1699996"),
        Equation(
            r"L_\Delta = \frac{dE_\Delta}{dl}",
            {r"L_\Delta": SELF, "E": _iso80000.ENERGY, "l": _iso80000.LENGTH},
        ),
    ),
    _iso80000.KERMA: (
        Wikidata("Q1739288"),
        Equation(
            r"K = \frac{dE_\mathrm{tr}}{dm}",
            {
                "K": SELF,
                r"E_\mathrm{tr}": _iso80000.ENERGY,
                "m": _iso80000.MASS,
            },
        ),
    ),
    _iso80000.KERMA_RATE: (
        Wikidata("Q1739280"),
        Equation(
            r"\dot{K} = \frac{dK}{dt}",
            {r"\dot{K}": SELF, "K": _iso80000.KERMA, "t": _iso80000.TIME},
        ),
    ),
    _iso80000.MASS_ENERGY_TRANSFER_COEFFICIENT: (
        Wikidata("Q99714619"),
        Equation(
            r"\frac{\mu_\mathrm{tr}}{\rho} = \frac{1}{\rho}\frac{1}{R}\frac{dR_\mathrm{tr}}{dl}",
            {
                r"\frac{\mu_\mathrm{tr}}{\rho}": SELF,
                r"\rho": _iso80000.DENSITY,
                "R": _iso80000.IONIZING_RADIANT_ENERGY,
                "l": _iso80000.LENGTH,
            },
        ),
    ),
    _iso80000.IONIZING_EXPOSURE: (
        Wikidata("Q336938"),
        Equation(
            r"X = \frac{dq}{dm}",
            {"X": SELF, "q": _iso80000.ELECTRIC_CHARGE, "m": _iso80000.MASS},
        ),
    ),
    _iso80000.EXPOSURE_RATE: (
        Wikidata("Q99720212"),
        Equation(
            r"\dot{X} = \frac{dX}{dt}",
            {
                r"\dot{X}": SELF,
                "X": _iso80000.IONIZING_EXPOSURE,
                "t": _iso80000.TIME,
            },
        ),
    ),
}
# use the following symbols (which are more common in fluid mechanics):
# - $L$ for (characteristic) length
# - $u$ for velocity
# - $D$ for diameter
# - $\sigma$ for surface tension
# - $\mu$ for dynamic viscosity
CHARACTERISTIC_NUMBERS: Details = {
    _iso80000.PRESSURE_DROP: Equation(
        r"\Delta p = p_u - p_d",
        {
            r"\Delta p": SELF,
            "p_u": (_iso80000.PRESSURE, " upstream"),
            "p_d": (_iso80000.PRESSURE, " downstream"),
        },
    ),
    _iso80000.REYNOLDS_NUMBER: (
        Wikidata("Q178932"),
        Equation(
            r"Re = \frac{\rho u L}{\eta} = \frac{u L}{\nu}",
            {
                "Re": SELF,
                r"\rho": _iso80000.DENSITY,
                "u": (_iso80000.SPEED, " of fluid"),
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\eta": _iso80000.DYNAMIC_VISCOSITY,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.EULER_NUMBER: (
        Wikidata("Q1340031"),
        Equation(
            r"Eu = \frac{\Delta p}{\rho u^2}",
            {
                "Eu": SELF,
                r"\Delta p": _iso80000.PRESSURE_DROP,
                r"\rho": _iso80000.DENSITY,
                "u": (_iso80000.SPEED, " of fluid"),
            },
        ),
    ),
    _iso80000.FROUDE_NUMBER: (
        Wikidata("Q273090"),
        Equation(
            r"Fr = \frac{u}{\sqrt{Lg}}",
            {
                "Fr": SELF,
                "u": (_iso80000.SPEED, " of fluid"),
                "L": ("characteristic ", _iso80000.LENGTH),
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
            },
        ),
    ),
    _iso80000.GRASHOF_NUMBER: (
        Wikidata("Q868719"),
        Equation(
            r"Gr = \frac{g \alpha_V (T_s - T_\infty) L^3}{\nu^2}",
            {
                "Gr": SELF,
                "L": ("characteristic ", _iso80000.LENGTH),
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                r"\alpha_V": _iso80000.VOLUMETRIC_EXPANSION_COEFFICIENT,
                r"T_s": _iso80000.SURFACE_TEMPERATURE,  # NOTE: wikidata uses $\Delta T$
                r"T_\infty": _iso80000.REFERENCE_TEMPERATURE,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.WEBER_NUMBER: (
        Wikidata("Q947531"),
        Equation(
            r"We = \frac{\rho u^2 L}{\sigma}",
            {
                "We": SELF,
                r"\rho": _iso80000.DENSITY,
                "u": _iso80000.SPEED,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\sigma": _iso80000.SURFACE_TENSION,
            },
        ),
    ),
    _iso80000.MACH_NUMBER: (
        Wikidata("Q160669"),
        Symbol("M"),
        Equation(
            r"Ma = \frac{u}{c}",
            {"Ma": SELF, "u": _iso80000.SPEED, "c": _iso80000.SPEED_OF_SOUND},
        ),
    ),
    _iso80000.KNUDSEN_NUMBER: (
        Wikidata("Q898463"),
        Equation(
            r"Kn = \frac{\lambda}{L}",
            {
                "Kn": SELF,
                r"\lambda": _iso80000.MEAN_FREE_PATH,
                "L": ("characteristic ", _iso80000.LENGTH),
            },
        ),
    ),
    # NOTE: drag coefficient defined in ISO80000-4 above
    _iso80000.STROUHAL_NUMBER: (
        Wikidata("Q646627"),
        Equation(
            r"Sr = \frac{f L}{u}",
            {
                "Sr": SELF,
                "f": _iso80000.FREQUENCY,
                "L": ("characteristic ", _iso80000.LENGTH),
                "u": _iso80000.SPEED,
            },
        ),
        Symbol("Sh"),
    ),
    _iso80000.BAGNOLD_NUMBER: (
        Wikidata("Q101584387"),
        Equation(
            r"Bg = \frac{c_D \rho u^2}{L g \rho_b}",
            {
                "Bg": SELF,
                "c_D": _iso80000.DRAG_COEFFICIENT,
                r"\rho": (_iso80000.DENSITY, " of fluid"),
                "u": _iso80000.SPEED,
                "L": ("characteristic", _iso80000.LENGTH),
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                r"\rho_b": (_iso80000.DENSITY, " of body"),
            },
        ),
    ),
    _iso80000.BAGNOLD_NUMBER_SOLID_PARTICLES: (
        Wikidata("Q2472733"),
        Equation(
            r"Ba = \frac{\rho_s d^2 \dot{\gamma}}{\eta} \left(\frac{1}{f_s^{1/2}-1}\right)",
            {
                r"Ba": SELF,
                r"\rho_s": (_iso80000.DENSITY, " of particles"),
                "d": (_iso80000.DIAMETER, " of particles"),
                r"\dot{\gamma}": _iso80000.SHEAR_RATE,
                r"\eta": (_iso80000.DYNAMIC_VISCOSITY, " of fluid"),
                "f_s": (_iso80000.VOLUME_FRACTION, " of solid particles"),
            },
        ),
    ),
    _iso80000.LIFT_COEFFICIENT: (
        Wikidata("Q760106"),
        Equation(
            r"c_L = \frac{L}{qS} = \frac{L}{\frac{1}{2}\rho u^2 S}",
            {
                "c_L": SELF,
                "L": (_iso80000.LIFT, " of wing"),
                "q": _iso80000.DYNAMIC_PRESSURE,
                r"\rho": (_iso80000.DENSITY, " of fluid"),
                "u": (_iso80000.SPEED, " of body relative to fluid"),
                "S": ("Planform ", _iso80000.AREA),
            },
        ),
        Symbol("c_l", remarks="for 2D flows"),
        Symbol("c_A"),
    ),
    _iso80000.THRUST_COEFFICIENT: (
        Wikidata("Q102040931"),
        Equation(
            r"c_t = \frac{T}{\rho n^2 D^4}",
            {
                "c_t": SELF,
                "T": (_iso80000.THRUST, " of propeller"),
                r"\rho": (_iso80000.DENSITY, " of fluid"),
                "n": _iso80000.ROTATIONAL_FREQUENCY,
                "D": ("tip ", _iso80000.DIAMETER, " of propeller"),
            },
            assumptions={"propellers"},
        ),
        Symbol(r"c_\tau"),
    ),
    _iso80000.DEAN_NUMBER: (
        Wikidata("Q674181"),
        Equation(
            r"Dn = \frac{2ur}{\nu}\sqrt{\frac{r}{R}}",
            {
                "Dn": SELF,
                "u": _iso80000.AXIAL_SPEED,
                "r": (_iso80000.RADIUS, " of pipe"),
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                "R": _iso80000.RADIUS_OF_CURVATURE,
            },
        ),
    ),
    _iso80000.BEJAN_NUMBER: (
        Wikidata("Q50814076"),
        Equation(
            r"Be = \frac{\Delta p L^2}{\eta \nu} = \frac{\rho \Delta p L^2}{\eta^2}",
            {
                "Be": SELF,
                r"\Delta p": _iso80000.PRESSURE_DROP,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\eta": _iso80000.DYNAMIC_VISCOSITY,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.LAGRANGE_NUMBER: (
        Wikidata("Q102066153"),
        Equation(
            r"Lg = \frac{L \Delta p}{\mu u}",
            {
                "Lg": SELF,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\Delta p": _iso80000.PRESSURE_DROP,
                r"\mu": _iso80000.DYNAMIC_VISCOSITY,
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.BINGHAM_NUMBER: (
        Wikidata("Q3343011"),
        Equation(
            r"Bm = \frac{\tau D}{\mu u}",
            {
                "Bm": SELF,
                r"\tau": _iso80000.SHEAR_STRESS,
                "D": ("characteristic", _iso80000.DIAMETER),
                r"\mu": _iso80000.DYNAMIC_VISCOSITY,
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.HEDSTROM_NUMBER: (
        Wikidata("Q3343027"),
        Equation(
            r"He = \frac{\tau_0 D^2 \rho}{\mu^2}",
            {
                "He": SELF,
                r"\tau_0": (_iso80000.SHEAR_STRESS, " at flow limit"),
                "D": ("characteristic", _iso80000.DIAMETER),
                r"\rho": _iso80000.DENSITY,
                r"\mu": _iso80000.DYNAMIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.BODENSTEIN_NUMBER: (
        Wikidata("Q370662"),
        Equation(
            r"Bo = \frac{uL}{D_{ax}} = Pe^* = Re \cdot Sc",
            {
                "Bo": SELF,
                "u": _iso80000.SPEED,
                "L": (_iso80000.LENGTH, " of the reactor"),
                r"D_{ax}": _iso80000.DIFFUSION_COEFFICIENT,
                "Pe^*": (_iso80000.PECLET_NUMBER, " for mass transfer"),
                "Re": _iso80000.REYNOLDS_NUMBER,
                "Sc": _iso80000.SCHMIDT_NUMBER,
            },
        ),
        Symbol("Bd"),
    ),
    _iso80000.ROSSBY_NUMBER: (
        Wikidata("Q676622"),
        Equation(
            r"Ro = \frac{u}{2 L \omega_E \sin\phi}",  # wikipedia uses f = 2ω_Esinϕ
            {
                "Ro": SELF,
                "u": (_iso80000.SPEED, " of motion"),
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\omega_E": (
                    _iso80000.ANGULAR_VELOCITY_CCW,
                    " of Earth's rotation",
                ),
                r"\phi": _iso80000.LATITUDE,
            },
        ),
    ),
    _iso80000.EKMAN_NUMBER: (
        Wikidata("Q1323330"),
        Equation(
            r"Ek = \frac{\nu}{2 L^2 \omega_E \sin\phi}",
            {
                "Ek": SELF,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\omega_E": (
                    _iso80000.ANGULAR_VELOCITY_CCW,
                    " of Earth's rotation",
                ),
                r"\phi": _iso80000.LATITUDE,
            },
        ),
    ),
    _iso80000.ELASTICITY_NUMBER: (
        Wikidata("Q102310770"),
        Equation(
            r"El = \frac{t_r \nu}{r^2}",
            {
                "El": SELF,
                "t_r": _iso80000.RELAXATION_TIME,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                "r": (_iso80000.RADIUS, " of the pipe"),
            },
        ),
    ),
    _iso80000.DARCY_FRICTION_FACTOR: (
        Wikidata("Q1253446"),
        Equation(
            r"f_D = \frac{2\Delta p D}{\rho u^2 L}",
            {
                "f_D": SELF,
                r"\Delta p": (_iso80000.PRESSURE_DROP, " due to friction"),
                r"\rho": _iso80000.DENSITY,
                "u": ("average ", _iso80000.SPEED, " of fluid flow in pipe"),
                "D": (_iso80000.DIAMETER, " of pipe"),
                "L": (_iso80000.LENGTH, " of pipe"),
            },
        ),
    ),
    _iso80000.FANNING_NUMBER: (
        Wikidata("Q2004420"),
        Equation(
            r"f_n = \frac{\tau_w}{\frac{1}{2}\rho u^2}",
            {
                "f_n": SELF,
                r"\tau_w": _iso80000.SHEAR_STRESS,
                r"\rho": _iso80000.DENSITY,
                "u": _iso80000.SPEED,
            },
        ),
        Symbol("f"),
    ),
    _iso80000.GOERTLER_NUMBER: (
        Wikidata("Q102723670"),
        Equation(
            r"Go = \frac{u l_b}{\nu} \sqrt{\frac{l_b}{r_c}}",
            {
                "Go": SELF,
                "u": ("external ", _iso80000.SPEED),
                "l_b": _iso80000.BOUNDARY_LAYER_THICKNESS,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                "r_c": _iso80000.RADIUS_OF_CURVATURE,
            },
        ),
    ),
    _iso80000.HAGEN_NUMBER: (
        Wikidata("Q1568363"),
        Equation(
            r"Hg = -\frac{1}{\rho}\frac{dp}{dx}\frac{L^3}{\nu^2}",
            {
                "Hg": SELF,
                r"\rho": _iso80000.DENSITY,
                r"\frac{dp}{dx}": _iso80000.PRESSURE_GRADIENT,
                "L": _iso80000.LENGTH,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
        Equation(
            r"Hg = Gr",
            {"Hg": SELF, "Gr": _iso80000.GRASHOF_NUMBER},
            assumptions={"free convection"},
        ),
    ),
    _iso80000.LAVAL_NUMBER: (
        Wikidata("Q1808802"),
        Equation(
            r"La = \frac{u}{\sqrt{\frac{R_s T 2\gamma}{\gamma+1}}}",
            {
                "La": SELF,
                "u": _iso80000.SPEED,
                "R_s": _iso80000.SPECIFIC_GAS_CONSTANT,
                "T": _iso80000.TEMPERATURE,
                r"\gamma": _iso80000.HEAT_CAPACITY_RATIO,
            },
        ),
    ),
    _iso80000.POISEUILLE_NUMBER: (
        Wikidata("Q2513351"),
        Equation(
            r"Poi = -\frac{\Delta p D^2}{L \mu u}",
            {
                "Poi": SELF,
                r"\Delta p": _iso80000.PRESSURE_DROP,
                "L": (_iso80000.LENGTH, " of pipe"),
                "D": (_iso80000.DIAMETER, " of pipe"),
                r"\mu": (_iso80000.DYNAMIC_VISCOSITY, " of fluid"),
                "u": (_iso80000.SPEED, " of fluid flow in pipe"),
            },
        ),
    ),
    _iso80000.POWER_NUMBER: (
        Wikidata("Q1462550"),
        Equation(
            r"N_p = \frac{P}{\rho n^3 D^5}",
            {
                "N_p": SELF,
                "P": (_iso80000.ACTIVE_POWER, " of stirrer"),
                r"\rho": (_iso80000.DENSITY, " of fluid"),
                "n": _iso80000.ROTATIONAL_FREQUENCY,
                "D": (_iso80000.DIAMETER, " of stirrer"),
            },
        ),
    ),
    _iso80000.RICHARDSON_NUMBER: (
        Wikidata("Q961847"),
        Equation(
            r"Ri = \frac{gh}{u^2}",
            {
                "Ri": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "h": _iso80000.HEIGHT,
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.REECH_NUMBER: (
        Wikidata("Q25401602"),
        Equation(
            r"Ree = \frac{\sqrt{gl}}{u}",
            {
                "Ree": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "l": _iso80000.LENGTH,
                "u": (_iso80000.SPEED, " of object relative to water"),
            },
        ),
    ),
    _iso80000.BOUSSINESQ_NUMBER: Equation(
        r"Bs = \frac{v}{\sqrt{2gl}}",
        {
            "Bs": SELF,
            "v": (_iso80000.SPEED, " of object relative to water"),
            "g": _iso80000.ACCELERATION_OF_FREE_FALL,
            "l": _iso80000.LENGTH,
        },
    ),
    _iso80000.STOKES_NUMBER: (
        Wikidata("Q1545546"),
        Equation(
            r"Stk = \frac{t_r}{t_a}",
            {
                "Stk": SELF,
                "t_r": (_iso80000.RELAXATION_TIME, " of particles"),
                "t_a": (_iso80000.DURATION, " of fluid to alter its velocity"),
            },
        ),
    ),
    _iso80000.STOKES_NUMBER_VIBRATING_PARTICLES: (
        Wikidata("Q103820258"),
        Equation(
            r"Stk_1 = \frac{\nu}{D^2 f}",
            {
                r"Stk_1": SELF,
                r"\nu": (_iso80000.KINEMATIC_VISCOSITY, " of fluid or plasma"),
                "D": (_iso80000.DIAMETER, " of particle"),
                "f": (_iso80000.FREQUENCY, " of particle vibrations"),
            },
        ),
    ),
    _iso80000.STOKES_NUMBER_ROTAMETER: (
        Wikidata("Q103896907"),
        Equation(
            r"Stk_2 = \frac{r^3 g m (\rho_b - \rho)}{\eta^2}",
            {
                r"Stk_2": SELF,
                "r": "Ratio of pipe and float radii",
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "m": (_iso80000.MASS, " of the floating body"),
                r"\rho_b": (_iso80000.DENSITY, " of the floating body"),
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                r"\eta": (_iso80000.DYNAMIC_VISCOSITY, " of the fluid"),
            },
        ),
    ),  # check this
    _iso80000.STOKES_NUMBER_GRAVITY: (
        Wikidata("Q103982174"),
        Equation(
            r"Stk_3 = \frac{v \nu}{g L^2}",
            {
                r"Stk_3": SELF,
                "v": (_iso80000.SPEED, " of particles"),
                r"\nu": (_iso80000.KINEMATIC_VISCOSITY, " of the fluid"),
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "L": (_iso80000.LENGTH, " of fall"),
            },
        ),
    ),
    _iso80000.STOKES_NUMBER_DRAG: (
        Wikidata("Q103982443"),
        Equation(
            r"Stk_4 = \frac{F_D}{\mu u L}",
            {
                "Stk_4": SELF,
                "F_D": _iso80000.DRAG,
                r"\mu": (_iso80000.DYNAMIC_VISCOSITY, " of the fluid"),
                "u": _iso80000.SPEED,
                "L": ("characteristic ", _iso80000.LENGTH),
            },
        ),
    ),
    _iso80000.LAPLACE_NUMBER: (
        Wikidata("Q179814"),
        Equation(
            r"La = \frac{\sigma \rho L}{\mu^2}",
            {
                "La": SELF,
                r"\sigma": _iso80000.SURFACE_TENSION,
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\mu": (_iso80000.DYNAMIC_VISCOSITY, " of the fluid"),
            },
        ),
    ),
    _iso80000.BLAKE_NUMBER: (
        Wikidata("Q3343009"),
        Equation(
            r"Bl = \frac{u \rho L}{\mu(1-\varepsilon)}",
            {
                "Bl": SELF,
                "u": (_iso80000.SPEED, " of the fluid"),
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\mu": (_iso80000.DYNAMIC_VISCOSITY, " of the fluid"),
                r"\varepsilon": _iso80000.POROSITY,
            },
        ),
    ),
    _iso80000.SOMMERFELD_NUMBER: (
        Wikidata("Q6047623"),
        Equation(
            r"So = \frac{\mu n}{p} \left(\frac{r}{c}\right)^2",
            {
                "So": SELF,
                r"\mu": (_iso80000.DYNAMIC_VISCOSITY, " of lubricant"),
                "n": _iso80000.ROTATIONAL_FREQUENCY,
                "p": _iso80000.MEAN_BEARING_PRESSURE,
                "r": (_iso80000.RADIUS, " of the shaft"),
                "c": (
                    "radial ",
                    _iso80000.DISTANCE,
                    " between rotating shaft and annulus",
                ),
            },
        ),
    ),
    _iso80000.TAYLOR_NUMBER: (
        Wikidata("Q1935046"),
        Equation(
            r"Ta = \frac{4 \omega^2 L^4}{\nu^2}",  # NOTE: wikidata \nu should not be ^4
            {
                "Ta": SELF,
                r"\omega": (_iso80000.ANGULAR_VELOCITY_CCW, " of rotation"),
                "L": (_iso80000.LENGTH, " perpendicular to the rotation axis"),
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.GALILEI_NUMBER: (
        Wikidata("Q1492101"),
        Equation(
            r"Ga = \frac{g L^3}{\nu^2}",
            {
                "Ga": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\nu": (_iso80000.KINEMATIC_VISCOSITY, " of the fluid"),
            },
        ),
    ),
    _iso80000.WOMERSLEY_NUMBER: (
        Wikidata("Q2066584"),
        Equation(
            r"\alpha = R \sqrt{\frac{\omega}{\nu}}",
            {
                r"\alpha": SELF,
                "R": (_iso80000.RADIUS, " of the pipe"),
                r"\omega": (_iso80000.ANGULAR_FREQUENCY, " of oscillations"),
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
        Symbol("Wo"),
    ),
    _iso80000.FOURIER_NUMBER: (
        Wikidata("Q901793"),
        Equation(
            r"Fo = \frac{\alpha t}{L^2}",
            {
                "Fo": SELF,
                r"\alpha": _iso80000.THERMAL_DIFFUSIVITY,
                "t": _iso80000.TIME,
                "L": ("characteristic ", _iso80000.LENGTH),
            },
        ),
    ),
    _iso80000.PECLET_NUMBER: (
        Wikidata("Q899769"),
        Equation(
            r"Pe = \frac{uL}{\alpha}",
            {
                "Pe": SELF,
                "u": _iso80000.SPEED,
                "L": (_iso80000.LENGTH, " in the direction of heat transfer"),
                r"\alpha": _iso80000.THERMAL_DIFFUSIVITY,
            },
        ),
    ),
    _iso80000.RAYLEIGH_NUMBER: (
        Wikidata("Q898249"),
        Equation(
            r"Ra_L = \frac{L^3 g \alpha_V (T_s - T_r)}{\nu \alpha}",
            {
                "Ra": SELF,
                "L": ("characteristic ", _iso80000.LENGTH),
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                r"\alpha_V": (
                    _iso80000.VOLUMETRIC_EXPANSION_COEFFICIENT,
                    " of the fluid",
                ),
                r"T_s": _iso80000.SURFACE_TEMPERATURE,
                r"T_r": _iso80000.REFERENCE_TEMPERATURE,
                r"\nu": (_iso80000.KINEMATIC_VISCOSITY, " of the fluid"),
                r"\alpha": (_iso80000.THERMAL_DIFFUSIVITY, " of the fluid"),
            },
        ),
    ),
    _iso80000.FROUDE_NUMBER_HEAT_TRANSFER: (
        Wikidata("Q104175687"),
        Equation(
            r"Fr^* = \frac{g L^3}{\alpha^2}",  # NOTE: wikidata incorrectly omits powers for l and \alpha
            {
                r"Fr^*": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\alpha": _iso80000.THERMAL_DIFFUSIVITY,
            },
        ),
    ),
    _iso80000.NUSSELT_NUMBER: (
        Wikidata("Q898280"),
        Equation(
            r"Nu_L = \frac{hL}{\kappa}",
            {
                "Nu": SELF,
                "h": _iso80000.HEAT_TRANSFER_COEFFICIENT,
                "L": (
                    _iso80000.LENGTH,
                    " of the body in direction of heat flow",
                ),
                r"\kappa": _iso80000.THERMAL_CONDUCTIVITY,
            },
        ),
    ),
    _iso80000.BIOT_NUMBER: (
        Wikidata("Q864844"),
        Equation(
            r"Bi = \frac{hL_C}{\kappa}",
            {
                "Bi": SELF,
                "h": _iso80000.HEAT_TRANSFER_COEFFICIENT,
                "L_c": ("characteristic ", _iso80000.LENGTH),
                r"\kappa": (_iso80000.THERMAL_CONDUCTIVITY, " of the body"),
            },
        ),
    ),
    _iso80000.STANTON_NUMBER: (
        Wikidata("Q901845"),
        Equation(
            r"St = \frac{h}{\rho u c_p}",
            {
                "St": SELF,
                "h": _iso80000.HEAT_TRANSFER_COEFFICIENT,
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                "u": _iso80000.SPEED,
                "c_p": (_iso80000.SPECIFIC_HEAT_CAPACITY_P, " of the fluid"),
            },
        ),
    ),
    _iso80000.J_FACTOR_HEAT_TRANSFER: (
        Wikidata("Q1107639"),
        Equation(
            r"j = \frac{h}{c_p \rho u} \left(\frac{c_p \eta}{\kappa}\right)^{2/3} = \frac{h}{c_p G} Pr^{2/3}",
            {
                "j": SELF,
                "h": _iso80000.HEAT_TRANSFER_COEFFICIENT,
                "c_p": _iso80000.SPECIFIC_HEAT_CAPACITY_P,
                r"\rho": _iso80000.DENSITY,
                "u": _iso80000.SPEED,
                r"\eta": _iso80000.DYNAMIC_VISCOSITY,
                r"\kappa": _iso80000.THERMAL_CONDUCTIVITY,
                r"G": _iso80000.MASS_FLUX,
            },
        ),
    ),
    _iso80000.BEJAN_NUMBER_HEAT_TRANSFER: (
        Wikidata("Q104209862"),
        Equation(
            r"Be = \frac{\Delta p L^2}{\eta \alpha}",
            {
                "Be": SELF,
                r"\Delta p": (_iso80000.PRESSURE_DROP, " along a pipe"),
                "L": (_iso80000.LENGTH, " of the pipe"),
                r"\eta": _iso80000.DYNAMIC_VISCOSITY,
                r"\alpha": _iso80000.THERMAL_DIFFUSIVITY,
            },
        ),
    ),
    _iso80000.BEJAN_NUMBER_ENTROPY: (
        Wikidata("Q3110607"),
        Equation(
            r"Be = \frac{S(\Delta T)}{S(\Delta T) + S(\Delta p)}",
            {
                r"Be": SELF,
                "S": (_iso80000.ENTROPY, " generation"),
                r"\Delta T": _iso80000.TEMPERATURE_DIFFERENCE,
                r"\Delta p": _iso80000.PRESSURE_DROP,
            },
        ),
    ),
    _iso80000.STEFAN_NUMBER: (
        Wikidata("Q909876"),
        Equation(
            r"Ste = \frac{c_p \Delta T}{L}",  # not using Q for *specific* latent heat
            {
                "Ste": SELF,
                "c_p": _iso80000.SPECIFIC_HEAT_CAPACITY_P,
                r"\Delta T": (
                    _iso80000.TEMPERATURE_DIFFERENCE,
                    " between the phases",
                ),
                "L": _iso80000.SPECIFIC_LATENT_HEAT,
            },
        ),
    ),
    _iso80000.BRINKMAN_NUMBER: (
        Wikidata("Q917504"),
        Equation(
            r"Br = \frac{\eta u^2}{\kappa \Delta T}",
            {
                "Br": SELF,
                r"\eta": _iso80000.DYNAMIC_VISCOSITY,
                "u": ("characteristic ", _iso80000.SPEED),
                r"\kappa": _iso80000.THERMAL_CONDUCTIVITY,
                r"\Delta T": (
                    _iso80000.TEMPERATURE_DIFFERENCE,
                    " between wall and bulk fluid",
                ),
            },
        ),
    ),
    _iso80000.CLAUSIUS_NUMBER: (
        Wikidata("Q3343019"),
        Equation(
            r"Cl = \frac{u^3 L \rho}{\lambda \Delta T}",  # NOTE: wikidata uses u^3
            {
                "Cl": SELF,
                "u": _iso80000.SPEED,
                "L": (_iso80000.LENGTH, " of the path of energy transfer"),
                r"\rho": _iso80000.DENSITY,
                r"\lambda": _iso80000.THERMAL_CONDUCTIVITY,
                r"\Delta T": (
                    _iso80000.TEMPERATURE_DIFFERENCE,
                    " along length L",
                ),
            },
        ),
    ),
    _iso80000.ECKERT_NUMBER: (
        Wikidata("Q905744"),
        Equation(
            r"Ec = \frac{u^2}{c_p \Delta T}",
            {
                "Ec": SELF,
                "u": ("characteristic ", _iso80000.SPEED),
                "c_p": (_iso80000.SPECIFIC_HEAT_CAPACITY_P, " of the flow"),
                r"\Delta T": (
                    _iso80000.TEMPERATURE_DIFFERENCE,
                    " due to dissipation",
                ),
            },
        ),
    ),
    _iso80000.GRAETZ_NUMBER: (
        Wikidata("Q903886"),
        Equation(
            r"Gz = \frac{u D^2}{\alpha l}",
            {
                "Gz": SELF,
                "u": (_iso80000.SPEED, " of the fluid"),
                "D": (_iso80000.DIAMETER, " of the pipe"),
                r"\alpha": (_iso80000.THERMAL_DIFFUSIVITY, " of the fluid"),
                "l": (_iso80000.LENGTH, " of the pipe"),
            },
        ),
        Equation(
            r"Gz = \frac{D}{l} Re Pr",
            {
                "Gz": SELF,
                "D": (_iso80000.DIAMETER, " of the pipe"),
                "l": (_iso80000.LENGTH, " of the pipe"),
                "Re": _iso80000.REYNOLDS_NUMBER,
                "Pr": _iso80000.PRANDTL_NUMBER,
            },
        ),
    ),
    _iso80000.HEAT_TRANSFER_NUMBER: (
        Wikidata("Q104379084"),
        Equation(
            r"K_Q = \frac{\Phi}{u^3 L^2 \rho}",
            {
                "K_Q": SELF,
                r"\Phi": _iso80000.HEAT_FLOW_RATE,
                "u": ("characteristic ", _iso80000.SPEED),
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.POMERANTSEV_NUMBER: (
        Wikidata("Q104379986"),
        Equation(
            r"Po = \frac{Q_m L^2}{\lambda \Delta T}",
            {
                "Po": SELF,
                "Q_m": _iso80000.VOLUMIC_HEAT_GENERATION_RATE,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\lambda": _iso80000.THERMAL_CONDUCTIVITY,
                r"\Delta T": (
                    _iso80000.TEMPERATURE_DIFFERENCE,
                    " between medium and initial body temperature",
                ),
            },
        ),
    ),
    _iso80000.BOLTZMANN_NUMBER: (
        Wikidata("Q3343051"),
        Equation(
            r"Bo = \frac{\rho_0 u c_p}{\varepsilon \sigma T_0^3}",
            {
                "Bo": SELF,
                r"\rho_0": (_iso80000.DENSITY, " of the fluid"),
                "u": (_iso80000.SPEED, " of the fluid"),
                "c_p": _iso80000.SPECIFIC_HEAT_CAPACITY_P,
                r"\varepsilon": _iso80000.EMISSIVITY,
                r"\sigma": _iso80000.CONST_STEFAN_BOLTZMANN,
                "T_0": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.STARK_NUMBER: (
        Wikidata("Q104407222"),
        Equation(
            r"Sk = \frac{\varepsilon \sigma T^3 L}{\lambda}",
            {
                "Sk": SELF,
                r"\varepsilon": (_iso80000.EMISSIVITY, " of the surface"),
                r"\sigma": _iso80000.CONST_STEFAN_BOLTZMANN,
                "T": _iso80000.TEMPERATURE,
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\lambda": _iso80000.THERMAL_CONDUCTIVITY,
            },
        ),
    ),
    _iso80000.FOURIER_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104542186"),
        Equation(
            r"Fo^* = \frac{D t}{L^2}",
            {
                r"Fo^*": SELF,
                "D": _iso80000.DIFFUSION_COEFFICIENT,
                "t": (_iso80000.DURATION, " of observation"),
                "L": (_iso80000.LENGTH, " of transfer"),
            },
        ),
    ),
    _iso80000.PECLET_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104542217"),
        Equation(
            r"Pe^* = \frac{Lu}{D}",
            {
                r"Pe^*": SELF,
                "L": ("characteristic ", _iso80000.LENGTH),
                "u": _iso80000.SPEED,
                "D": _iso80000.DIFFUSION_COEFFICIENT,
            },
        ),
    ),
    _iso80000.GRASHOF_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104578635"),
        Equation(
            r"Gr^* = \frac{g \left(-\frac{1}{\rho}\left(\frac{\partial\rho}{\partial x}\right)_{T,p}\right) \Delta x L^3}{\nu^2}",
            {
                r"Gr^*": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                r"x": _iso80000.MOLE_FRACTION,
                r"\Delta x": (
                    "Difference of ",
                    _iso80000.MOLE_FRACTION,
                    " along length l",
                ),
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.NUSSELT_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104598868"),
        Equation(
            r"Nu^* = \frac{k' L}{\rho D}",
            {
                r"Nu^*": SELF,
                "k'": _iso80000.MASS_FLUX_DENSITY,
                "L": _iso80000.THICKNESS,
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                "D": _iso80000.DIFFUSION_COEFFICIENT,
            },
        ),
    ),
    _iso80000.STANTON_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104627433"),
        Equation(
            r"St^* = \frac{k'}{\rho u}",
            {
                r"St^*": SELF,
                "k'": _iso80000.MASS_FLUX_DENSITY,
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.GRAETZ_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104638971"),
        Equation(
            r"Gz^* = \frac{u d}{L D} = \frac{d}{L} Pe^*",
            {
                r"Gz^*": SELF,
                "u": (_iso80000.SPEED, " of the fluid"),
                "d": (_iso80000.DIAMETER, " of the pipe"),
                "L": (_iso80000.LENGTH, " of the pipe"),
                "D": _iso80000.DIFFUSION_COEFFICIENT,
                r"Pe^*": _iso80000.PECLET_NUMBER_MASS_TRANSFER,
            },
        ),
    ),
    _iso80000.J_FACTOR_MASS_TRANSFER: (
        Wikidata("Q104654483"),
        Equation(
            r"j^* = \frac{k_c}{u} \left(\frac{\nu}{D}\right)^{2/3} = \frac{k_c}{u} Sc^{2/3}",
            {
                "j^*": SELF,
                "k_c": _iso80000.MASS_TRANSFER_COEFFICIENT,
                "u": _iso80000.SPEED,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                "D": _iso80000.DIFFUSION_COEFFICIENT,
                "Sc": _iso80000.SCHMIDT_NUMBER,
            },
        ),
    ),
    _iso80000.ATWOOD_NUMBER: (
        Wikidata("Q2373823"),
        Equation(
            r"At = \frac{\rho_1 - \rho_2}{\rho_1 + \rho_2}",
            {
                "At": SELF,
                r"\rho_1": (_iso80000.DENSITY, " of heavier fluid"),
                r"\rho_2": (_iso80000.DENSITY, " of lighter fluid"),
            },
        ),
    ),
    _iso80000.BIOT_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104713187"),
        Equation(
            r"Bi^* = \frac{k L}{D_\text{int}}",
            {
                r"Bi^*": SELF,
                "k": _iso80000.MASS_TRANSFER_COEFFICIENT,
                "L": _iso80000.THICKNESS,
                r"D_\text{int}": (
                    _iso80000.DIFFUSION_COEFFICIENT,
                    " at the interface",
                ),
            },
        ),
    ),
    _iso80000.MORTON_NUMBER: (
        Wikidata("Q1346119"),
        Equation(
            r"Mo = \frac{g \eta^4}{\rho \sigma^3} \left(\frac{\rho_b}{\rho} - 1\right)",
            {
                "Mo": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                r"\eta": (_iso80000.DYNAMIC_VISCOSITY, " of surrounding fluid"),
                r"\rho": (_iso80000.DENSITY, " of surrounding fluid"),
                r"\sigma": (_iso80000.SURFACE_TENSION, " of the interface"),
                r"\rho_b": (_iso80000.DENSITY, " of the bubble or drop"),
            },
        ),
    ),
    _iso80000.BOND_NUMBER: (
        Wikidata("Q892173"),
        Equation(
            r"Bo = \frac{a \rho L^2}{\sigma} \left(\frac{\rho_b}{\rho} - 1\right)",
            {
                "Bo": SELF,
                "a": (_iso80000.ACCELERATION, " of the body"),
                r"\rho": (_iso80000.DENSITY, " of the medium"),
                "L": ("characteristic ", _iso80000.LENGTH),
                r"\sigma": (_iso80000.SURFACE_TENSION, " of the interface"),
                r"\rho_b": (_iso80000.DENSITY, " of the bubble or drop"),
            },
        ),
    ),
    _iso80000.ARCHIMEDES_NUMBER: (
        Wikidata("Q634307"),
        Equation(
            r"Ar = \frac{g L^3}{\nu^2} \left(\frac{\rho_b}{\rho} - 1\right)",
            {
                "Ar": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "L": ("characteristic ", _iso80000.LENGTH, " of the body"),
                r"\nu": (_iso80000.KINEMATIC_VISCOSITY, " of the fluid"),
                r"\rho_b": (_iso80000.DENSITY, " of the body"),
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
            },
        ),
    ),
    _iso80000.EXPANSION_NUMBER: (
        Wikidata("Q104774294"),
        Equation(
            r"Ex = \frac{g d}{u^2} \left(1 - \frac{\rho_b}{\rho}\right)",
            {
                "Ex": SELF,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                "d": (_iso80000.DIAMETER, " of bubbles"),
                "u": (_iso80000.SPEED, " of bubbles"),
                r"\rho_b": (_iso80000.DENSITY, " of bubbles"),
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
            },
        ),
    ),
    _iso80000.MARANGONI_NUMBER: (
        Wikidata("Q1861030"),
        Equation(
            r"Mg = \left(-\frac{d\gamma}{dT}\right) \frac{L\Delta T}{\eta \alpha}",
            {
                "Mg": SELF,
                r"\gamma": (_iso80000.SURFACE_TENSION, " of the film"),
                "T": _iso80000.TEMPERATURE,
                "L": (_iso80000.THICKNESS, " of the film"),
                r"\Delta T": (
                    _iso80000.TEMPERATURE_DIFFERENCE,
                    " across the film",
                ),
                r"\eta": (_iso80000.DYNAMIC_VISCOSITY, " of the liquid"),
                r"\alpha": (_iso80000.THERMAL_DIFFUSIVITY, " of the liquid"),
            },
        ),
    ),
    _iso80000.LOCKHART_MARTINELLI_PARAMETER: (
        Wikidata("Q29211"),
        Equation(
            r"Lp = \frac{\dot{m}_l}{\dot{m}_g}\sqrt{\frac{\rho_g}{\rho_l}}",
            {
                "Lp": SELF,
                r"\dot{m}_l": (_iso80000.MASS_FLOW_RATE, " of liquid phase"),
                r"\dot{m}_g": (_iso80000.MASS_FLOW_RATE, " of gas phase"),
                r"\rho_g": (_iso80000.DENSITY, " of gas phase"),
                r"\rho_l": (_iso80000.DENSITY, " of liquid phase"),
            },
        ),
    ),
    _iso80000.BEJAN_NUMBER_MASS_TRANSFER: (
        Wikidata("Q104785959"),
        Equation(
            r"Be^* = \frac{\Delta p L^2}{\mu D}",
            {
                r"Be^*": SELF,
                r"\Delta p": (
                    _iso80000.PRESSURE_DROP,
                    " along a pipe or channel",
                ),
                "L": (_iso80000.LENGTH, " of the channel"),
                r"\mu": (_iso80000.DYNAMIC_VISCOSITY, " of the fluid"),
                "D": _iso80000.DIFFUSION_COEFFICIENT,
            },
        ),
    ),
    _iso80000.CAVITATION_NUMBER: (
        Wikidata("Q1737262"),
        Equation(
            r"Ca = \frac{p - p_v}{\rho u^2 / 2}",
            {
                "Ca": SELF,
                "p": _iso80000.STATIC_PRESSURE,
                "p_v": _iso80000.VAPOUR_PRESSURE,
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                "u": (_iso80000.SPEED, " of the flow"),
            },
        ),
    ),
    _iso80000.ABSORPTION_NUMBER: (
        Wikidata("Q3343003"),
        Equation(
            r"Ab = k \sqrt{\frac{L D_\text{film}}{D_\text{diff} q_v}}",
            {
                "Ab": SELF,
                "k": _iso80000.MASS_TRANSFER_COEFFICIENT,
                "L": (_iso80000.LENGTH, " of wetted surface"),
                r"D_\text{film}": (_iso80000.THICKNESS, " of liquid film"),
                r"D_\text{diff}": _iso80000.DIFFUSION_COEFFICIENT,
                "q_v": (_iso80000.VOLUME_FLOW_RATE, " per wetted perimeter"),
            },
        ),
    ),
    _iso80000.CAPILLARY_NUMBER: (
        Wikidata("Q104815730"),
        Equation(
            r"Ca = \frac{d^2 \rho g}{\sigma}",
            {
                "Ca": SELF,
                "d": (_iso80000.DIAMETER, " of the pipe"),
                r"\rho": (_iso80000.DENSITY, " of the fluid"),
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                r"\sigma": (_iso80000.SURFACE_TENSION, " of the fluid"),
            },
        ),
    ),
    _iso80000.DYNAMIC_CAPILLARY_NUMBER: (
        Wikidata("Q785542"),
        Equation(
            r"Ca^* = \frac{\mu u}{\sigma}",
            {
                r"Ca^*": SELF,
                r"\mu": (_iso80000.DYNAMIC_VISCOSITY, " of the fluid"),
                "u": ("characteristic ", _iso80000.SPEED),
                r"\sigma": (_iso80000.SURFACE_TENSION, " of the fluid"),
            },
        ),
    ),
    _iso80000.PRANDTL_NUMBER: (
        Wikidata("Q815306"),
        Equation(
            r"Pr = \frac{\nu}{\alpha}",
            {
                "Pr": SELF,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                r"\alpha": _iso80000.THERMAL_DIFFUSIVITY,
            },
        ),
    ),
    _iso80000.SCHMIDT_NUMBER: (
        Wikidata("Q581997"),
        Equation(
            r"Sc = \frac{\nu}{D}",
            {
                "Sc": SELF,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                "D": _iso80000.DIFFUSION_COEFFICIENT,
            },
        ),
    ),
    _iso80000.LEWIS_NUMBER: (
        Wikidata("Q901840"),
        Equation(
            r"Le = \frac{\alpha}{D}",
            {
                "Le": SELF,
                r"\alpha": _iso80000.THERMAL_DIFFUSIVITY,
                "D": _iso80000.DIFFUSION_COEFFICIENT,
            },
        ),
    ),
    _iso80000.OHNESORGE_NUMBER: (
        Wikidata("Q1302335"),
        Equation(
            r"Oh = \frac{\mu}{\sqrt{\sigma \rho L}}",
            {
                "Oh": SELF,
                r"\mu": _iso80000.DYNAMIC_VISCOSITY,
                r"\sigma": _iso80000.SURFACE_TENSION,
                r"\rho": _iso80000.DENSITY,
                "L": ("characteristic ", _iso80000.LENGTH),
            },
        ),
    ),
    _iso80000.CAUCHY_NUMBER: (
        Wikidata("Q957179"),
        Equation(
            r"Cy = \frac{\rho u^2}{K}",
            {
                "Cy": SELF,
                r"\rho": _iso80000.DENSITY,
                "u": _iso80000.SPEED,
                "K": _iso80000.BULK_MODULUS,
            },
        ),
    ),
    _iso80000.HOOKE_NUMBER: (
        Wikidata("Q104864070"),
        Equation(
            r"Ho_2 = \frac{\rho u^2}{E}",
            {
                "Ho_2": SELF,
                r"\rho": _iso80000.DENSITY,
                "u": _iso80000.SPEED,
                "E": _iso80000.YOUNGS_MODULUS,
            },
        ),
    ),
    _iso80000.WEISSENBERG_NUMBER: (
        Wikidata("Q1753014"),
        Equation(
            r"Wi = \dot{\gamma} t_r",
            {
                "Wi": SELF,
                r"\dot{\gamma}": _iso80000.SHEAR_RATE,
                "t_r": _iso80000.RELAXATION_TIME,
            },
        ),
    ),
    _iso80000.DEBORAH_NUMBER: (
        Wikidata("Q1138045"),
        Equation(
            r"De = \frac{t_c}{t_p}",
            {
                "De": SELF,
                "t_c": (_iso80000.RELAXATION_TIME, " (stress)"),
                "t_p": _iso80000.OBSERVATION_DURATION,
            },
        ),
    ),
    _iso80000.LORENTZ_NUMBER: (
        Wikidata("Q104901522"),
        Equation(
            r"Lo = \frac{\sigma (\Delta U)^2}{\kappa \Delta T}",
            {
                "Lo": SELF,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\Delta U": _iso80000.VOLTAGE,
                r"\kappa": _iso80000.THERMAL_CONDUCTIVITY,
                r"\Delta T": _iso80000.TEMPERATURE_DIFFERENCE,
            },
        ),
    ),
    _iso80000.COMPRESSIBILITY_NUMBER: (
        Wikidata("Q736895"),
        Equation(
            r"Z = \frac{p}{\rho R_s T}",
            {
                "Z": SELF,
                "p": _iso80000.PRESSURE,
                r"\rho": _iso80000.DENSITY,
                "R_s": _iso80000.SPECIFIC_GAS_CONSTANT,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.REYNOLDS_MAGNETIC_NUMBER: (
        Wikidata("Q1852720"),
        Equation(
            r"Rm = u L \mu \sigma",
            {
                "Rm": SELF,
                "u": _iso80000.SPEED,
                "L": _iso80000.LENGTH,
                r"\mu": _iso80000.PERMEABILITY,
                r"\sigma": _iso80000.CONDUCTIVITY,
            },
        ),
    ),
    _iso80000.BATCHELOR_NUMBER: (
        Wikidata("Q105061807"),
        Equation(
            r"Bt = \frac{u L \sigma \mu}{\varepsilon_r \mu_r}",
            {
                "Bt": SELF,
                "u": _iso80000.SPEED,
                "L": _iso80000.LENGTH,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\mu": _iso80000.PERMEABILITY,
                r"\varepsilon_r": _iso80000.RELATIVE_PERMITTIVITY,
                r"\mu_r": _iso80000.RELATIVE_PERMEABILITY,
            },
        ),
    ),
    _iso80000.NUSSELT_ELECTRIC_NUMBER: (
        Wikidata("Q105070806"),
        Equation(
            r"Ne = \frac{uL}{D^*}",
            {
                "Ne": SELF,
                "u": _iso80000.SPEED,
                "L": _iso80000.LENGTH,
                "D^*": _iso80000.DIFFUSION_COEFFICIENT,
            },
        ),
    ),
    _iso80000.ALFVEN_NUMBER: (
        Wikidata("Q3342997"),
        Equation(
            r"Al = \frac{u}{B / \sqrt{\rho \mu}}",
            {
                "Al": SELF,
                "u": _iso80000.SPEED,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                r"\rho": _iso80000.DENSITY,
                r"\mu": _iso80000.PERMEABILITY,
            },
        ),
    ),
    _iso80000.HARTMANN_NUMBER: (
        Wikidata("Q1587280"),
        Equation(
            r"Ha = B L \sqrt{\frac{\sigma}{\mu}}",
            {
                "Ha": SELF,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                "L": _iso80000.LENGTH,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\mu": _iso80000.DYNAMIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.COWLING_NUMBER: (
        Wikidata("Q3343018"),
        Equation(
            r"Co = \frac{B^2}{\mu \rho u^2}",
            {
                "Co": SELF,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                r"\mu": _iso80000.PERMEABILITY,
                r"\rho": _iso80000.DENSITY,
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.STUART_ELECTRICAL_NUMBER: (
        Wikidata("Q105093880"),
        Equation(
            r"Se = \frac{\varepsilon E^2}{\rho u^2}",
            {
                "Se": SELF,
                r"\varepsilon": _iso80000.PERMITTIVITY,
                "E": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\rho": _iso80000.DENSITY,
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.MAGNETIC_PRESSURE_NUMBER: (
        Wikidata("Q105102313"),
        Equation(
            r"N_{mp} = \frac{2\mu p}{B^2}",
            {
                "N_{mp}": SELF,
                r"\mu": _iso80000.PERMEABILITY,
                "p": _iso80000.PRESSURE,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.CHANDRASEKHAR_NUMBER: (
        Wikidata("Q4516333"),
        Equation(
            r"Q = \frac{(B L)^2 \sigma}{\rho \nu}",
            {
                "Q": SELF,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                "L": _iso80000.LENGTH,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\rho": _iso80000.DENSITY,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.PRANDTL_MAGNETIC_NUMBER: (
        Wikidata("Q2510107"),
        Equation(
            r"Pr_m = \nu \sigma \mu",
            {
                r"Pr_m": SELF,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\mu": _iso80000.PERMEABILITY,
            },
        ),
    ),
    _iso80000.ROBERTS_NUMBER: (
        Wikidata("Q105190387"),
        Equation(
            r"Ro = \alpha \sigma \mu",
            {
                r"Ro": SELF,
                r"\alpha": _iso80000.THERMAL_DIFFUSIVITY,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\mu": _iso80000.PERMEABILITY,
            },
        ),
    ),
    _iso80000.STUART_NUMBER: (
        Wikidata("Q1386798"),
        Equation(
            r"Stw = \frac{B^2 L \sigma}{u \rho}",
            {
                "Stw": SELF,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                "L": _iso80000.LENGTH,
                r"\sigma": _iso80000.CONDUCTIVITY,
                "u": _iso80000.SPEED,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.MAGNETIC_NUMBER: (
        Wikidata("Q105221904"),
        Equation(
            r"N_{mg} = B \sqrt{\frac{L \sigma}{\mu u}}",
            {
                r"N_{mg}": SELF,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                "L": _iso80000.LENGTH,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\mu": _iso80000.DYNAMIC_VISCOSITY,
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.ELECTRIC_FIELD_PARAMETER: (
        Wikidata("Q105221927"),
        Equation(
            r"Ef = \frac{E}{u B}",
            {
                "Ef": SELF,
                "E": _iso80000.ELECTRIC_FIELD_STRENGTH,
                "u": _iso80000.SPEED,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.HALL_NUMBER: (
        Wikidata("Q105266119"),
        Equation(
            r"H_c = \frac{\omega_c \lambda}{2\pi u}",
            {
                r"H_c": SELF,
                r"\omega_c": _iso80000.CYCLOTRON_ANGULAR_FREQUENCY,
                r"\lambda": _iso80000.MEAN_FREE_PATH,
                "u": _iso80000.SPEED,
            },
        ),
    ),
    _iso80000.LUNDQUIST_NUMBER: (
        Wikidata("Q2066377"),
        Equation(
            r"Lu = B L \sigma \sqrt{\frac{\mu}{\rho}}",
            {
                "Lu": SELF,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                "L": _iso80000.LENGTH,
                r"\sigma": _iso80000.CONDUCTIVITY,
                r"\mu": _iso80000.PERMEABILITY,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.JOULE_MAGNETIC_NUMBER: (
        Wikidata("Q3343031"),
        Equation(
            r"Jo_m = \frac{2 \rho \mu c_p \Delta T}{B^2}",
            {
                r"Jo_m": SELF,
                r"\rho": _iso80000.DENSITY,
                r"\mu": _iso80000.PERMEABILITY,
                "c_p": _iso80000.SPECIFIC_HEAT_CAPACITY_P,
                r"\Delta T": _iso80000.TEMPERATURE_DIFFERENCE,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.GRASHOF_MAGNETIC_NUMBER: (
        Wikidata("Q105356815"),
        Equation(
            r"Gr_m = \frac{4\pi \sigma_e \mu_e g \alpha_V (T_s - T_\infty) L^3}{\nu}",
            {
                r"Gr_m": SELF,
                r"\sigma_e": _iso80000.CONDUCTIVITY,
                r"\mu_e": _iso80000.PERMEABILITY,
                "g": _iso80000.ACCELERATION_OF_FREE_FALL,
                r"\alpha_V": _iso80000.VOLUMETRIC_EXPANSION_COEFFICIENT,
                r"T_s": _iso80000.SURFACE_TEMPERATURE,
                r"T_\infty": _iso80000.REFERENCE_TEMPERATURE,
                "L": _iso80000.LENGTH,
                r"\nu": _iso80000.KINEMATIC_VISCOSITY,
            },
        ),
    ),
    _iso80000.NAZE_NUMBER: (
        Wikidata("Q105385595"),
        Equation(
            r"Na = \frac{B}{c \sqrt{\rho \mu}}",
            {
                "Na": SELF,
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                "c": _iso80000.SPEED_OF_SOUND,
                r"\rho": _iso80000.DENSITY,
                r"\mu": _iso80000.PERMEABILITY,
            },
        ),
    ),
    _iso80000.REYNOLDS_ELECTRIC_NUMBER: (
        Wikidata("Q105395962"),
        Equation(
            r"Re_e = \frac{u \varepsilon_e}{L \rho_e \mu}",
            {
                r"Re_e": SELF,
                "u": _iso80000.SPEED,
                r"\varepsilon_e": _iso80000.PERMITTIVITY,
                "L": _iso80000.LENGTH,
                r"\rho_e": _iso80000.CHARGE_DENSITY,
                r"\mu": _iso80000.MOBILITY,
            },
        ),
    ),
    _iso80000.AMPERE_NUMBER: (
        Wikidata("Q105404651"),
        Equation(
            r"Am = \frac{I_A}{L H}",
            {
                "Am": SELF,
                "I_A": ("electric surface ", _iso80000.CURRENT),
                "L": _iso80000.LENGTH,
                "H": _iso80000.MAGNETIC_FIELD_STRENGTH,
            },
        ),
    ),
    _iso80000.ARRHENIUS_NUMBER: (
        Wikidata("Q105415606"),
        Equation(
            r"\alpha = \frac{E_0}{RT}",
            {
                r"\alpha": SELF,
                "E_0": _iso80000.ACTIVATION_ENERGY,
                "R": _iso80000.MOLAR_GAS_CONSTANT,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.LANDAU_GINZBURG_NUMBER: (
        Wikidata("Q105421034"),
        Equation(
            r"\kappa = \frac{\lambda_L}{\xi \sqrt{2}}",
            {
                r"\kappa": SELF,
                r"\lambda_L": _iso80000.LONDON_PENETRATION_DEPTH,
                r"\xi": _iso80000.COHERENCE_LENGTH,
            },
        ),
    ),
}
CONDENSED_MATTER_PHYSICS: Details = {
    _iso80000.LATTICE_VECTOR: (
        Wikidata("Q105435234"),
        Symbol(r"\boldsymbol{R}"),
    ),
    _iso80000.FUNDAMENTAL_LATTICE_VECTORS: (
        Wikidata("Q105451063"),
        Symbol(r"\boldsymbol{a}_1"),
        Symbol(r"\boldsymbol{a}_2"),
        Symbol(r"\boldsymbol{a}_3"),
    ),
    _iso80000.ANGULAR_RECIPROCAL_LATTICE_VECTOR: (
        Wikidata("Q105475278"),
        Symbol(r"\boldsymbol{G}"),
    ),
    _iso80000.FUNDAMENTAL_RECIPROCAL_LATTICE_VECTORS: (
        Wikidata("Q105475399"),
        Symbol(r"\boldsymbol{b}_1"),
        Symbol(r"\boldsymbol{b}_2"),
        Symbol(r"\boldsymbol{b}_3"),
    ),
    _iso80000.LATTICE_PLANE_SPACING: (Wikidata("Q105488046"), Symbol("d")),
    _iso80000.BRAGG_ANGLE: (
        Wikidata("Q105488118"),
        Equation(
            r"2d\sin\theta = n\lambda",
            {
                "d": _iso80000.LATTICE_PLANE_SPACING,
                r"\theta": SELF,
                "n": "Order of reflection",
                r"\lambda": _iso80000.WAVELENGTH,
            },
        ),
    ),
    _iso80000.SHORT_RANGE_ORDER_PARAMETER: (
        Wikidata("Q105495979"),
        Symbol("r"),
        Symbol(r"\sigma"),
    ),
    _iso80000.LONG_RANGE_ORDER_PARAMETER: (
        Wikidata("Q105496124"),
        Symbol("R"),
        Symbol("s"),
    ),
    _iso80000.ATOMIC_SCATTERING_FACTOR: (
        Wikidata("Q837866"),
        Equation(
            r"f = \frac{E_a}{E_e}",
            {
                "f": SELF,
                "E_a": ("Radiation amplitude scattered by atom",),
                "E_e": ("Radiation amplitude scattered by a single electron",),
            },
        ),
    ),
    _iso80000.STRUCTURE_FACTOR: (
        Wikidata("Q900684"),
        Equation(
            r"F(h,k,l) = \sum_{n=1}^{N} f_n \exp[2\pi i (hx_n + ky_n + lz_n)]",
            {
                "F(h,k,l)": SELF,
                "N": "Total number of atoms in unit cell",
                "f_n": _iso80000.ATOMIC_SCATTERING_FACTOR,
                "h,k,l": "Miller indices",
                "x,y,z": "Fractional coordinates",
                "n": "atom",
            },
        ),
    ),
    _iso80000.BURGERS_VECTOR: (Wikidata("Q623093"), Symbol(r"\boldsymbol{b}")),
    _iso80000.PARTICLE_POSITION_VECTOR: (
        Wikidata("Q105533324"),
        Symbol(r"\boldsymbol{r}"),
        Symbol(r"\boldsymbol{R}"),
    ),
    _iso80000.EQUILIBRIUM_POSITION_VECTOR: (
        Wikidata("Q105533477"),
        Symbol(r"\boldsymbol{R}_0"),
    ),
    _iso80000.DISPLACEMENT_VECTOR_LATTICE: (
        Wikidata("Q105533558"),
        Equation(
            r"\boldsymbol{u} = \boldsymbol{R} - \boldsymbol{R}_0",
            {
                r"\boldsymbol{u}": SELF,
                r"\boldsymbol{R}": _iso80000.PARTICLE_POSITION_VECTOR,
                r"\boldsymbol{R}_0": _iso80000.EQUILIBRIUM_POSITION_VECTOR,
            },
        ),
    ),
    _iso80000.DEBYE_WALLER_FACTOR: (
        Wikidata("Q902587"),
        Symbol("D"),
        Symbol("B"),
    ),
    _iso80000.ANGULAR_WAVENUMBER_LATTICE: (
        Wikidata("Q105542089"),
        Symbol("k"),
        Symbol("q"),
    ),
    _iso80000.FERMI_ANGULAR_WAVENUMBER: (Wikidata("Q105554303"), Symbol("k_F")),
    _iso80000.DEBYE_ANGULAR_WAVENUMBER: (Wikidata("Q105554370"), Symbol("q_D")),
    _iso80000.DEBYE_ANGULAR_FREQUENCY: (
        Wikidata("Q105580986"),
        Symbol(r"\omega_D"),
    ),
    _iso80000.DEBYE_TEMPERATURE: (
        Wikidata("Q3517821"),
        Equation(
            r"\Theta_D = \frac{\hbar\omega_D}{k}",
            {
                r"\Theta_D": SELF,
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                r"\omega_D": _iso80000.DEBYE_ANGULAR_FREQUENCY,
                "k": _iso80000.CONST_BOLTZMANN,
            },
        ),
    ),
    _iso80000.DENSITY_OF_VIBRATIONAL_STATES: (
        Wikidata("Q105637294"),
        Equation(
            r"g(\omega) = \frac{dn(\omega)}{d\omega}",
            {
                r"g": SELF,
                r"n": (
                    r"Number of vibrational modes per ",
                    _iso80000.VOLUME,
                    r" with angular frequency less than $\omega$",
                ),
                r"\omega": _iso80000.ANGULAR_FREQUENCY,
            },
        ),
    ),
    _iso80000.THERMODYNAMIC_GRUNEISEN_PARAMETER: (
        Wikidata("Q105658620"),
        Equation(
            r"\gamma_G = \frac{\alpha_V}{\kappa_T c_V \rho}",
            {
                r"\gamma_G": SELF,
                r"\alpha_V": _iso80000.VOLUMETRIC_EXPANSION_COEFFICIENT,
                r"\kappa_T": _iso80000.ISOTHERMAL_COMPRESSIBILITY,
                "c_V": _iso80000.SPECIFIC_HEAT_CAPACITY_V,
                r"\rho": _iso80000.DENSITY,
            },
        ),
    ),
    _iso80000.GRUNEISEN_PARAMETER: (
        Wikidata("Q444656"),
        Equation(
            r"\gamma = -\frac{\partial\ln\omega}{\partial\ln V}",
            {
                r"\gamma": SELF,
                r"\omega": _iso80000.LATTICE_VIBRATION_FREQUENCY,
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.MEAN_FREE_PATH_OF_PHONONS: (
        Wikidata("Q105672255"),
        Symbol("l_p"),
    ),
    _iso80000.MEAN_FREE_PATH_OF_ELECTRONS: (
        Wikidata("Q105672307"),
        Symbol("l_e"),
    ),
    _iso80000.ENERGY_DENSITY_OF_STATES: (
        Wikidata("Q105687031"),
        Equation(
            r"n_E(E) = \frac{dn(E)}{dE}",
            {
                r"n_E": SELF,
                r"n": _iso80000.NUMBER_OF_ONE_ELECTRON_STATES_PER_VOLUME,
                "E": _iso80000.ENERGY,
            },
        ),
    ),
    _iso80000.RESIDUAL_RESISTIVITY: (Wikidata("Q25098876"), Symbol(r"\rho_0")),
    _iso80000.LORENZ_COEFFICIENT: (
        Wikidata("Q105728754"),
        Equation(
            r"L = \frac{\kappa}{\sigma T}",
            {
                "L": SELF,
                r"\kappa": _iso80000.THERMAL_CONDUCTIVITY,
                r"\sigma": _iso80000.CONDUCTIVITY,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.HALL_COEFFICIENT: (
        Wikidata("Q997439"),
        Equation(
            r"\boldsymbol{E} = \rho\boldsymbol{J} + R_H(\boldsymbol{B}\times\boldsymbol{J})",
            {
                r"\boldsymbol{E}": _iso80000.ELECTRIC_FIELD_STRENGTH,
                r"\rho": _iso80000.RESISTIVITY,
                r"\boldsymbol{J}": _iso80000.CURRENT_DENSITY,
                "R_H": SELF,
                r"\boldsymbol{B}": _iso80000.MAGNETIC_FLUX_DENSITY,
            },
        ),
    ),
    _iso80000.THERMOELECTRIC_VOLTAGE: (
        Wikidata("Q105761637"),
        Symbol(r"E_{ab}"),
    ),
    _iso80000.SEEBECK_COEFFICIENT: (
        Wikidata("Q1091448"),
        Equation(
            r"S_{ab} = \frac{dE_{ab}}{dT}",
            {
                r"S_{ab}": SELF,
                r"E_{ab}": _iso80000.THERMOELECTRIC_VOLTAGE,
                "T": _iso80000.TEMPERATURE,
            },
        ),
    ),
    _iso80000.PELTIER_COEFFICIENT: (
        Wikidata("Q105801003"),
        Symbol(r"\Pi_{ab}"),
    ),
    _iso80000.THOMSON_COEFFICIENT: (Wikidata("Q105801233"), Symbol(r"\mu")),
    _iso80000.WORK_FUNCTION: (Wikidata("Q783800"), Symbol(r"\Phi")),
    _iso80000.IONIZATION_ENERGY: (Wikidata("Q483769"), Symbol("E_i")),
    _iso80000.ELECTRON_AFFINITY: (Wikidata("Q105846486"), Symbol(r"\chi")),
    _iso80000.RICHARDSON_CONSTANT: (
        Wikidata("Q105883079"),
        Equation(
            r"J = A T^2 \exp\left(-\frac{\Phi}{kT}\right)",
            {
                "J": ("Thermionic emission ", _iso80000.CURRENT_DENSITY),
                "A": SELF,
                "T": _iso80000.TEMPERATURE,
                r"\Phi": _iso80000.WORK_FUNCTION,
                "k": _iso80000.CONST_BOLTZMANN,
            },
        ),
    ),
    _iso80000.FERMI_ENERGY: (Wikidata("Q431335"), Symbol("E_F")),
    _iso80000.GAP_ENERGY: (Wikidata("Q103982939"), Symbol("E_g")),
    _iso80000.FERMI_TEMPERATURE: (
        Wikidata("Q105942324"),
        Equation(
            r"T_F = \frac{E_F}{k}",
            {
                "T_F": SELF,
                "E_F": _iso80000.FERMI_ENERGY,
                "k": _iso80000.CONST_BOLTZMANN,
            },
        ),
    ),
    _iso80000.ELECTRON_DENSITY: (Wikidata("Q105971077"), Symbol("n")),
    _iso80000.HOLE_DENSITY: (Wikidata("Q105971101"), Symbol("p")),
    _iso80000.INTRINSIC_CARRIER_DENSITY: (
        Wikidata("Q1303188"),
        Equation(
            r"n_i = \sqrt{np}",
            {
                "n_i": SELF,
                "n": _iso80000.ELECTRON_DENSITY,
                "p": _iso80000.HOLE_DENSITY,
            },
        ),
    ),
    _iso80000.DONOR_DENSITY: (Wikidata("Q105979886"), Symbol("n_d")),
    _iso80000.ACCEPTOR_DENSITY: (Wikidata("Q105979968"), Symbol("n_a")),
    _iso80000.EFFECTIVE_MASS: (
        Wikidata("Q1064434"),
        Equation(
            r"m^* = \hbar^2 \left(\frac{d^2\varepsilon}{dk^2}\right)^{-1}",
            {
                "m^*": SELF,
                r"\hbar": _iso80000.CONST_REDUCED_PLANCK,
                r"\varepsilon": (_iso80000.ENERGY, " of an electron"),
                "k": _iso80000.ANGULAR_WAVENUMBER_LATTICE,
            },
        ),
    ),
    _iso80000.MOBILITY_RATIO: (
        Wikidata("Q106010255"),
        Equation(
            r"b = \frac{\mu_n}{\mu_p}",
            {
                "b": SELF,
                r"\mu_n": _iso80000.MOBILITY_OF_ELECTRONS,
                r"\mu_p": _iso80000.MOBILITY_OF_HOLES,
            },
        ),
    ),
    _iso80000.RELAXATION_TIME_LATTICE: (
        Wikidata("Q106041085"),
        Symbol(r"\tau"),
    ),
    _iso80000.CARRIER_LIFETIME: (
        Wikidata("Q5046374"),
        Symbol(r"\tau"),
        Symbol(r"\tau_n"),
        Symbol(r"\tau_p"),
    ),
    _iso80000.DIFFUSION_LENGTH: (
        Wikidata("Q106097176"),
        Equation(
            r"L = \sqrt{D\tau}",
            {
                "L": SELF,
                "D": _iso80000.DIFFUSION_COEFFICIENT,
                r"\tau": _iso80000.LIFETIME,
            },
        ),
    ),
    _iso80000.EXCHANGE_INTEGRAL: (
        Wikidata("Q10882959"),
        Symbol("K"),
        Symbol("J"),
    ),
    _iso80000.CURIE_TEMPERATURE: (Wikidata("Q191073"), Symbol("T_C")),
    _iso80000.NEEL_TEMPERATURE: (Wikidata("Q830311"), Symbol("T_N")),
    _iso80000.SUPERCONDUCTION_TRANSITION_TEMPERATURE: (
        Wikidata("Q106103037"),
        Symbol("T_c"),
    ),
    _iso80000.THERMODYNAMIC_CRITICAL_MAGNETIC_FLUX_DENSITY: (
        Wikidata("Q106103200"),
        Equation(
            r"B_c = \sqrt{\frac{2\mu_0(G_n - G_s)}{V}}",
            {
                "B_c": SELF,
                r"\mu_0": _iso80000.CONST_PERMEABILITY_VACUUM,
                "G_n": (_iso80000.GIBBS_ENERGY, " (normal conductor)"),
                "G_s": (_iso80000.GIBBS_ENERGY, " (superconductor)"),
                "V": _iso80000.VOLUME,
            },
        ),
    ),
    _iso80000.LOWER_CRITICAL_MAGNETIC_FLUX_DENSITY: (
        Wikidata("Q106127355"),
        Symbol(r"B_{c1}"),
    ),
    _iso80000.UPPER_CRITICAL_MAGNETIC_FLUX_DENSITY: (
        Wikidata("Q106127634"),
        Symbol(r"B_{c2}"),
    ),
    _iso80000.SUPERCONDUCTOR_ENERGY_GAP: (
        Wikidata("Q106127898"),
        Symbol(r"\Delta"),
    ),
    _iso80000.LONDON_PENETRATION_DEPTH: (
        Wikidata("Q3277853"),
        Symbol(r"\lambda_L"),
        Equation(
            r"B(x) = B(0) \exp\left(-\frac{x}{\lambda_L}\right)",
            {
                "B": _iso80000.MAGNETIC_FLUX_DENSITY,
                "x": _iso80000.DISTANCE,
                r"\lambda_L": SELF,
            },
        ),
    ),
    _iso80000.COHERENCE_LENGTH: (Wikidata("Q7643174"), Symbol(r"\xi")),
}
INFORMATION_SCIENCE_AND_TECHNOLOGY: Details = {
    _iso80000.TRAFFIC_INTENSITY: (Wikidata("Q1421101"), Symbol("A")),
    _iso80000.TRAFFIC_OFFERED_INTENSITY: (
        Wikidata("Q106213722"),
        Symbol("A_0"),
    ),
    _iso80000.TRAFFIC_CARRIED_INTENSITY: (Wikidata("Q106213953"), Symbol("Y")),
    _iso80000.MEAN_QUEUE_LENGTH: (
        Wikidata("Q106237523"),
        Symbol("L"),
        Symbol(r"\Omega"),
    ),
    _iso80000.LOSS_PROBABILITY: (Wikidata("Q106237587"), Symbol("B")),
    _iso80000.WAITING_PROBABILITY: (Wikidata("Q106237674"), Symbol("W")),
    _iso80000.CALL_INTENSITY: (Wikidata("Q106237881"), Symbol(r"\lambda")),
    _iso80000.COMPLETED_CALL_INTENSITY: (
        Wikidata("Q106237945"),
        Symbol(r"\mu"),
    ),
    _iso80000.STORAGE_CAPACITY: (Wikidata("Q2308599"), Symbol("M")),
    _iso80000.EQUIVALENT_BINARY_STORAGE_CAPACITY: (
        Wikidata("Q106247681"),
        Equation(
            r"M_e = \log_2 n",
            {"M_e": SELF, "n": "Number of possible states"},
        ),
    ),
    _iso80000.TRANSFER_RATE: (Wikidata("Q495092"), Symbol("r"), Symbol(r"\nu")),
    _iso80000.PERIOD_OF_DATA_ELEMENTS: (
        Wikidata("Q106268500"),
        Equation(
            r"T = 1/r",
            {"T": SELF, "r": _iso80000.TRANSFER_RATE},
        ),
    ),
    _iso80000.BIT_RATE: (Wikidata("Q194158"), Symbol(r"r_\text{bit}")),
    _iso80000.BIT_PERIOD: (
        Wikidata("Q106282183"),
        Equation(
            r"T_\text{bit} = 1/r_\text{bit}",
            {r"T_\text{bit}": SELF, r"r_\text{bit}": _iso80000.BIT_RATE},
        ),
    ),
    _iso80000.EQUIVALENT_BIT_RATE: (Wikidata("Q5227354"), Symbol("r_e")),
    _iso80000.MODULATION_RATE: (Wikidata("Q428083"), Symbol("r_m")),
    _iso80000.QUANTIZING_DISTORTION: (Wikidata("Q106321197"), Symbol("T_Q")),
    _iso80000.CARRIER_POWER: (Wikidata("Q25381657"), Symbol("P_c")),
    _iso80000.SIGNAL_ENERGY_PER_BINARY_DIGIT: (
        Wikidata("Q106344792"),
        Equation(
            r"E_\text{bit} = P_c T_\text{bit}",
            {
                r"E_\text{bit}": SELF,
                "P_c": _iso80000.CARRIER_POWER,
                r"T_\text{bit}": _iso80000.BIT_PERIOD,
            },
        ),
    ),
    _iso80000.ERROR_PROBABILITY: (Wikidata("Q106344844"), Symbol("P")),
    _iso80000.HAMMING_DISTANCE: (Wikidata("Q272172"), Symbol("d_h")),
    _iso80000.CLOCK_FREQUENCY: (Wikidata("Q911691"), Symbol(r"f_{cl}")),
    _iso80000.DECISION_CONTENT: (
        Wikidata("Q106378242"),
        Equation(
            r"D_a = \log_a n",
            {
                "D_a": SELF,
                "a": "Number of possibilities at each decision",
                "n": "Number of events",
            },
        ),
    ),
    _iso80000.INFORMATION_CONTENT: (
        Wikidata("Q735075"),
        Equation(
            r"I(x) = \log_b \frac{1}{p(x)}",
            {
                "I(x)": SELF,
                "b": "Base of logarithm (2 for shannon, 10 for hartley, e for nat)",
                "p(x)": "Probability of event x",
            },
        ),
    ),
    _iso80000.ENTROPY: (
        Wikidata("Q204570"),
        Equation(
            r"H(X) = \sum_{i=1}^n p(x_i) I(x_i)",
            {
                "H(X)": SELF,
                "p(x_i)": "Probability of event x_i",
                "x_i": "Event i",
                "I": _iso80000.INFORMATION_CONTENT,
            },
        ),
    ),
    _iso80000.MAXIMUM_ENTROPY: (Wikidata("Q106416338"), Symbol("H_0")),
    _iso80000.RELATIVE_ENTROPY: (
        Wikidata("Q106432207"),
        Equation(
            r"H_r = H / H_0",
            {
                "H_r": SELF,
                "H": _iso80000.ENTROPY,
                "H_0": _iso80000.MAXIMUM_ENTROPY,
            },
        ),
    ),
    _iso80000.REDUNDANCY: (
        Wikidata("Q122192"),
        Equation(
            r"R = H_0 - H",
            {
                "R": SELF,
                "H_0": _iso80000.MAXIMUM_ENTROPY,
                "H": _iso80000.ENTROPY,
            },
        ),
    ),
    _iso80000.RELATIVE_REDUNDANCY: (
        Wikidata("Q106432457"),
        Equation(
            r"r = R / H_0",
            {
                "r": SELF,
                "R": _iso80000.REDUNDANCY,
                "H_0": _iso80000.MAXIMUM_ENTROPY,
            },
        ),
    ),
    _iso80000.JOINT_INFORMATION_CONTENT: (
        Wikidata("Q106448630"),
        Symbol("I(x,y)"),
    ),
    _iso80000.CONDITIONAL_INFORMATION_CONTENT: (
        Wikidata("Q106449009"),
        Equation(
            r"I(x|y) = I(x,y) - I(y)",
            {
                "I(x|y)": SELF,
                "I(x,y)": _iso80000.JOINT_INFORMATION_CONTENT,
                "I(y)": _iso80000.INFORMATION_CONTENT,
            },
        ),
    ),
    _iso80000.CONDITIONAL_ENTROPY: (
        Wikidata("Q813908"),
        Equation(
            r"H(X|Y) = \sum_{i=1}^n \sum_{j=1}^m p(x_i, y_j) I(x_i|y_j)",
            {
                "H(X|Y)": SELF,
                r"p(x_i, y_j)": "Joint probability",
                r"I(x_i|y_j)": _iso80000.CONDITIONAL_INFORMATION_CONTENT,
            },
        ),
    ),
    _iso80000.EQUIVOCATION: (Wikidata("Q256358"), Symbol(r"H_\Delta(X|Y)")),
    _iso80000.IRRELEVANCE: (Wikidata("Q106453686"), Symbol(r"H_\nabla(Y|X)")),
    _iso80000.TRANSINFORMATION_CONTENT: (
        Wikidata("Q252973"),
        Equation(
            r"T(x,y) = I(x) + I(y) - I(x,y)",
            {
                "T(x,y)": SELF,
                "I(x)": _iso80000.INFORMATION_CONTENT,
                "I(y)": _iso80000.INFORMATION_CONTENT,
                "I(x,y)": _iso80000.JOINT_INFORMATION_CONTENT,
            },
        ),
    ),
    _iso80000.MEAN_TRANSINFORMATION_CONTENT: (
        Wikidata("Q106460818"),
        Symbol("T"),
    ),
    _iso80000.CHARACTER_MEAN_ENTROPY: (Wikidata("Q106460846"), Symbol("H'")),
    _iso80000.AVERAGE_INFORMATION_RATE: (
        Wikidata("Q106466934"),
        Equation(
            r"H^* = H' / \bar{t}(X)",
            {
                "H^*": SELF,
                "H'": _iso80000.CHARACTER_MEAN_ENTROPY,
                r"\bar{t}(X)": (
                    "Mean value of the ",
                    _iso80000.DURATION,
                    " of a character in the set X",
                ),
            },
        ),
    ),
    _iso80000.CHARACTER_MEAN_TRANSINFORMATION_CONTENT: (
        Wikidata("Q106483683"),
        Symbol("T'"),
    ),
    _iso80000.AVERAGE_TRANSINFORMATION_RATE: (
        Wikidata("Q106492181"),
        Symbol("T^*"),
    ),
    _iso80000.CHANNEL_CAPACITY_PER_CHARACTER: (
        Wikidata("Q106505959"),
        Equation(
            r"C' = \max T'",
            {
                "C'": SELF,
                "T'": _iso80000.CHARACTER_MEAN_TRANSINFORMATION_CONTENT,
            },
        ),
    ),
    _iso80000.CHANNEL_TIME_CAPACITY: (
        Wikidata("Q870845"),
        Equation(
            r"C^* = \max T^*",
            {"C^*": SELF, "T^*": _iso80000.AVERAGE_TRANSINFORMATION_RATE},
        ),
    ),
}
