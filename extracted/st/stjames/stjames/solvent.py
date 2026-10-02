from typing import Self

from pydantic import model_validator

from .base import Base, LowercaseStrEnum


class Solvent(LowercaseStrEnum):
    """Implicit solvent."""

    WATER = "water"
    NITROMETHANE = "nitromethane"
    NITROBENZENE = "nitrobenzene"
    TOLUENE = "toluene"
    BENZENE = "benzene"
    CHLOROBENZENE = "chlorobenzene"
    CARBONTETRACHLORIDE = "carbontetrachloride"
    DICHLOROETHANE = "dichloroethane"
    DICHLOROMETHANE = "dichloromethane"
    CHLOROFORM = "chloroform"
    DIETHYLETHER = "diethylether"
    DIISOPROPYLETHER = "diisopropylether"
    DIMETHYLSULFOXIDE = "dimethylsulfoxide"
    TETRAHYDROFURAN = "tetrahydrofuran"
    CYCLOHEXANE = "cyclohexane"
    ACETICACID = "aceticacid"
    HEXANE = "hexane"
    OCTANE = "octane"
    DECANE = "decane"
    ETHYLACETATE = "ethylacetate"
    ACETONE = "acetone"
    ACETONITRILE = "acetonitrile"
    METHANOL = "methanol"
    ETHANOL = "ethanol"
    ISOPROPANOL = "isopropanol"
    OCTANOL = "octanol"
    DIMETHYLACETAMIDE = "dimethylacetamide"
    DIMETHYLFORMAMIDE = "dimethylformamide"
    N_METHYLPYRROLIDONE = "n_methylpyrrolidone"
    ETHYLENE_GLYCOL = "ethylene_glycol"


class SolventModel(LowercaseStrEnum):
    """Implicit solvation model."""

    PCM = "pcm"
    CPCM = "cpcm"
    ALPB = "alpb"
    COSMO = "cosmo"
    COSMO2 = "cosmo2"
    COSMORS = "cosmors"
    GBSA = "gbsa"
    CPCMX = "cpcmx"
    SMD = "smd"


ALPB_SOLVENTS: frozenset[Solvent] = frozenset(
    {
        Solvent.ACETONE,
        Solvent.ACETONITRILE,
        Solvent.BENZENE,
        Solvent.CHLOROFORM,
        Solvent.DICHLOROMETHANE,
        Solvent.DIETHYLETHER,
        Solvent.DIMETHYLFORMAMIDE,
        Solvent.DIMETHYLSULFOXIDE,
        Solvent.ETHANOL,
        Solvent.ETHYLACETATE,
        Solvent.HEXANE,
        Solvent.METHANOL,
        Solvent.NITROMETHANE,
        Solvent.OCTANOL,
        Solvent.TETRAHYDROFURAN,
        Solvent.TOLUENE,
        Solvent.WATER,
    }
)

CPCMX_SOLVENTS: frozenset[Solvent] = frozenset(
    {
        Solvent.ACETICACID,
        Solvent.ACETONITRILE,
        Solvent.BENZENE,
        Solvent.CARBONTETRACHLORIDE,
        Solvent.CHLOROBENZENE,
        Solvent.CHLOROFORM,
        Solvent.CYCLOHEXANE,
        Solvent.DECANE,
        Solvent.DICHLOROETHANE,
        Solvent.DICHLOROMETHANE,
        Solvent.DIETHYLETHER,
        Solvent.DIISOPROPYLETHER,
        Solvent.DIMETHYLACETAMIDE,
        Solvent.DIMETHYLFORMAMIDE,
        Solvent.DIMETHYLSULFOXIDE,
        Solvent.ETHANOL,
        Solvent.ETHYLACETATE,
        Solvent.HEXANE,
        Solvent.ISOPROPANOL,
        Solvent.NITROBENZENE,
        Solvent.NITROMETHANE,
        Solvent.OCTANE,
        Solvent.OCTANOL,
        Solvent.TETRAHYDROFURAN,
        Solvent.TOLUENE,
        Solvent.WATER,
    }
)

SOLVENT_MODEL_SOLVENTS: dict[SolventModel, frozenset[Solvent]] = {
    SolventModel.ALPB: ALPB_SOLVENTS,
    SolventModel.CPCMX: CPCMX_SOLVENTS,
}


class SolventSettings(Base):
    """
    Implicit solvation settings.

    :param solvent: solvent to use
    :param model: solvation model
    """

    solvent: Solvent
    model: SolventModel

    @model_validator(mode="after")
    def cosmo2_requires_water(self) -> Self:
        """Validate that COSMO2 is only used with water."""
        if self.model == SolventModel.COSMO2 and self.solvent != Solvent.WATER:
            raise ValueError(f"COSMO2 is only parameterized for water, got {self.solvent.value!r}.")
        return self
