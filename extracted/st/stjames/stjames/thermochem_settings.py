"""Define thermochemistry calculation settings."""

import pydantic

from .base import Base


class ThermochemistrySettings(Base):
    """Thermochemistry calculation settings.

    Attributes:
        cutoff_frequency: Cramer/Truhlar quasi-harmonic cutoff, in cm⁻¹
        temperature: temperature for thermochemistry, in K
        scaling_factor: frequency scaling factor
        concentration: concentration, in M; None for an ideal gas at 1 atm and `temperature`
    """

    # Cramer/Truhlar cutoff freq (cm⁻¹)
    cutoff_frequency: pydantic.NonNegativeFloat = 100

    # temp (K)
    temperature: pydantic.PositiveFloat = 298.15

    # scaling factor, for frequencies
    scaling_factor: pydantic.NonNegativeFloat = 1.0

    # conc (M)
    concentration: pydantic.PositiveFloat | None = None
