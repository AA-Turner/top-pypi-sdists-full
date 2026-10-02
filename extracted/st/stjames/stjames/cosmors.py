"""Data model for COSMO-RS-derived properties."""

from typing import Annotated

from pydantic import AfterValidator, NonNegativeInt, PositiveFloat, computed_field

from .base import Base, LowercaseStrEnum, round_float, round_optional_float
from .solvent import Solvent


class COSMORSParameterization(LowercaseStrEnum):
    """COSMO-RS parameter set."""

    OPENCOSMO_RS_24A = "opencosmo_rs_24a"


class COSMORSData(Base):
    """
    COSMO-RS solvation free energy and its component breakdown.

    Components are signed as they enter ΔG_solv and sum to `solvation_free_energy`.

    :param solvent: solvent ΔG_solv refers to
    :param temperature: temperature, in K
    :param parameterization: COSMO-RS parameter set
    :param e_diel: dielectric energy E_COSMO - E_gas, in Hartree
    :param mu_res: residual chemical potential RT ln γ_res^∞, in Hartree
    :param mu_comb: combinatorial chemical potential RT ln γ_comb^∞, in Hartree
    :param g_disp: cavity-formation and dispersion term, in Hartree
    :param ring_correction: ring correction, in Hartree
    :param standard_state: mole fraction to molarity correction, in Hartree
    :param eta: global offset, in Hartree
    :param n_rings: rings in solute
    :param gas_phase_energy: gas-phase SCF total energy, in Hartree
    """

    solvent: Solvent
    temperature: Annotated[PositiveFloat, AfterValidator(round_float(2))]
    parameterization: COSMORSParameterization

    e_diel: Annotated[float, AfterValidator(round_float(6))]
    mu_res: Annotated[float, AfterValidator(round_float(6))]
    mu_comb: Annotated[float, AfterValidator(round_float(6))]
    g_disp: Annotated[float, AfterValidator(round_float(6))]
    ring_correction: Annotated[float, AfterValidator(round_float(6))]
    standard_state: Annotated[float, AfterValidator(round_float(6))]
    eta: Annotated[float, AfterValidator(round_float(6))]
    n_rings: NonNegativeInt

    gas_phase_energy: Annotated[float | None, AfterValidator(round_optional_float(6))] = None

    @computed_field
    @property
    def solvation_free_energy(self) -> float:
        """ΔG_solv, in Hartree."""
        return self.e_diel + self.mu_res + self.mu_comb + self.g_disp + self.ring_correction + self.standard_state + self.eta
