"""Define legacy implicit solvent settings."""

from pydantic import PositiveFloat, PositiveInt

from .base import Base, LowercaseStrEnum


class ImplicitSolventModel(LowercaseStrEnum):
    """Select the implicit solvent model used by legacy settings."""

    CPCM = "cpcm"
    ALPB = "alpb"
    COSMO = "cosmo"
    NONE = "none"


class SolventSettings(Base):
    """Configure a legacy implicit solvent calculation.

    Attributes:
        model: implicit solvent model
        epsilon: solvent dielectric constant
        grid_points_per_atom: surface grid points assigned to each atom
        vdw_scale: scale factor for van der Waals radii
        weight_cutoff: minimum grid weight retained
    """

    model: ImplicitSolventModel = ImplicitSolventModel.NONE
    epsilon: float = 78.36

    grid_points_per_atom: PositiveInt = 170
    vdw_scale: PositiveFloat = 1.2
    weight_cutoff: PositiveFloat = 1e-8
