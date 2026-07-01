# mypy: ignore-errors
from pint import UnitRegistry

ureg = UnitRegistry()
RHO_0 = 1.225 * (ureg.kilogram * ureg.meter**-3)
"""Density of air at mean sea level"""


def eas(tas, air_density):
    """Converts TAS to EAS.

    :param tas: true airspeed (meters per second)
    :param air_density: atmospheric density (kilograms per meter cubed)
    :returns: equivalent airspeed (meters per second)
    """
    return tas * (air_density / RHO_0) ** 0.5


RHO_0_PURE_PY = 1.225


def eas_pure_py(tas, air_density):
    return tas * (air_density / RHO_0_PURE_PY) ** 0.5
