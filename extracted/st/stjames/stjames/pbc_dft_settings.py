"""Define periodic density functional theory settings."""

from typing import Literal

from pydantic import BaseModel, PositiveFloat, PositiveInt

from .base import LowercaseStrEnum


class PBCDFTSmearing(LowercaseStrEnum):
    """Smearing types for occupations in PBC DFT calculations."""

    MARZARI_VANDERBILT = "marzari_vanderbilt"
    METHFESSEL_PAXTON = "methfessel_paxton"
    FERMI_DIRAC = "fermi_dirac"
    GAUSSIAN = "gaussian"


class PBCDFTSettings(BaseModel):
    """PBC DFT settings.

    Attributes:
        plane_wave_cutoff: plane-wave kinetic-energy cutoff (Hartree);
            None = use highest cutoff from pseudopotential metadata of elements in structure

        charge_density_cutoff: charge-density plane-wave cutoff (Hartree);
            None = use highest cutoff from pseudopotential metadata of elements in structure

        kpoints: Monkhorst–Pack k-point-grid dimensions; (None -> Å⁻¹ = .3)
        smearing_type: occupations smearing type
        smearing_width: smearing width, if relevant (Hartree)
        hubbard_u: DFT+U on-site Coulomb repulsion per element symbol (Hartree)
            None = no DFT+U; "auto" = automatic U values from MP database
    """

    plane_wave_cutoff: PositiveFloat | None = None
    charge_density_cutoff: PositiveFloat | None = None
    kpoints: tuple[PositiveInt, PositiveInt, PositiveInt] | None = None

    smearing_type: PBCDFTSmearing | None = None
    smearing_width: PositiveFloat = 0.005

    hubbard_u: dict[str, PositiveFloat] | Literal["auto"] | None = None
