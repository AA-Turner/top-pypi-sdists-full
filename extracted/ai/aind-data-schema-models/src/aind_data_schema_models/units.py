"""Module for defining UnitWithValue classes"""

from enum import Enum
from typing import Union


class SizeUnit(str, Enum):
    """Enumeration of Length Measurements"""

    M = "meter"
    CM = "centimeter"
    MM = "millimeter"
    UM = "micrometer"
    NM = "nanometer"
    IN = "inch"
    PX = "pixel"


class MassUnit(str, Enum):
    """Enumeration of Mass Measurements"""

    KG = "kilogram"
    G = "gram"
    MG = "milligram"
    UG = "microgram"
    NG = "nanogram"


class FrequencyUnit(str, Enum):
    """Enumeration of Frequency Measurements"""

    KHZ = "kilohertz"
    HZ = "hertz"
    mHZ = "millihertz"


class PressureUnit(str, Enum):
    """Enumeration of Pressure Measurements"""

    MPA = "millipascal"
    PA = "pascal"
    KPA = "kilopascal"


class SpeedUnit(str, Enum):
    """Enumeration of Speed Measurements"""

    RPM = "rotations per minute"


class VolumeUnit(str, Enum):
    """Enumeration of Volume Measurements"""

    L = "liter"
    ML = "milliliter"
    UL = "microliter"
    NL = "nanoliter"


class AngleUnit(str, Enum):
    """Enumeration of Angle Measurements"""

    RAD = "radians"
    DEG = "degrees"


class TimeUnit(str, Enum):
    """Enumeration of Time Measurements"""

    HR = "hour"
    M = "minute"
    S = "second"
    MS = "millisecond"
    US = "microsecond"
    NS = "nanosecond"


class PowerUnit(str, Enum):
    """Unit for power, set or measured"""

    UW = "microwatt"
    MW = "milliwatt"
    PERCENT = "percent"


class CurrentUnit(str, Enum):
    """Current units"""

    UA = "microamps"


class ConcentrationUnit(str, Enum):
    """Concentraion units"""

    M = "molar"
    UM = "micromolar"
    NM = "nanomolar"
    MASS_PERCENT = "% m/m"
    VOLUME_PERCENT = "% v/v"


class TemperatureUnit(str, Enum):
    """Temperature units"""

    C = "Celsius"
    K = "Kelvin"


class SoundIntensityUnit(str, Enum):
    """Sound intensity units"""

    DB = "decibels"


class VoltageUnit(str, Enum):
    """Voltage units"""

    V = "Volts"


class MemoryUnit(str, Enum):
    """Computer memory units"""

    B = "Byte"
    KB = "Kilobyte"
    MB = "Megabyte"
    GB = "Gigabyte"
    TB = "Terabyte"
    PB = "Petabyte"
    EB = "Exabyte"


class MagneticFieldUnit(str, Enum):
    """Magnetic field units"""

    T = "tesla"
    MT = "millitesla"
    UT = "microtesla"


class UnitlessUnit(str, Enum):
    """Unitless options"""

    PERCENT = "percent"
    FC = "fraction of cycle"


UNITS = Union[
    SizeUnit,
    MassUnit,
    FrequencyUnit,
    SpeedUnit,
    VolumeUnit,
    AngleUnit,
    TimeUnit,
    PowerUnit,
    CurrentUnit,
    ConcentrationUnit,
    TemperatureUnit,
    SoundIntensityUnit,
    VoltageUnit,
    MemoryUnit,
    UnitlessUnit,
    MagneticFieldUnit,
    PressureUnit,
]
