"""Nuclear-magnetic-resonance spectroscopy workflow."""

from typing import Annotated, Self, TypeAlias

from pydantic import AfterValidator, Field, model_validator

from ..base import Base, LowercaseStrEnum, round_float
from ..conformers import ConformerGenSettingsUnion, OpenConfSettings
from ..method import Method
from ..settings import Settings
from ..solvent import ALPB_SOLVENTS, CPCMX_SOLVENTS, Solvent, SolventModel
from ..task import Task
from ..types import UUID, round_list
from .multistage_opt import MultiStageOptSettings
from .workflow import MoleculeWorkflow

NMR_SUPPORTED_SOLVENTS: frozenset[Solvent] = frozenset(
    {
        Solvent.CHLOROFORM,
        Solvent.TETRAHYDROFURAN,
        Solvent.DICHLOROMETHANE,
        Solvent.ACETONE,
        Solvent.ACETONITRILE,
        Solvent.DIMETHYLSULFOXIDE,
        Solvent.METHANOL,
        Solvent.WATER,
        Solvent.BENZENE,
        Solvent.TOLUENE,
        Solvent.CHLOROBENZENE,
    }
)

NMR_SOLVENT_MODELS: dict[Solvent, SolventModel] = {
    solvent: SolventModel.CPCMX if solvent in CPCMX_SOLVENTS else SolventModel.ALPB
    for solvent in NMR_SUPPORTED_SOLVENTS
    if solvent in CPCMX_SOLVENTS or solvent in ALPB_SOLVENTS
}

AtomPair: TypeAlias = tuple[int, int]
RoundedHz: TypeAlias = Annotated[float, AfterValidator(round_float(3))]


class NMRMethod(LowercaseStrEnum):
    """Select a method for NMR spectrum prediction."""

    MAGNETZERO = "magnet-zero"


class NMRPeak(Base):
    """Represents a single NMR peak.

    Attributes:
        nucleus: atomic number of nucleus in question
        shift: chemical shift of peak
        atom_indices: zero-indices of atoms giving rise to peak
    """

    nucleus: int
    shift: Annotated[float, AfterValidator(round_float(3))]
    atom_indices: list[int]


class NMRCoupling(Base):
    """Represents a predicted NMR coupling between one or more atom pairs.

    Attributes:
        nuclei: nuclear species for the coupling pair
        atom_pairs: atom index pairs contributing to the coupling
        bond_distance: number of bonds between coupled nuclei
        coupling_hz: predicted coupling constant, in Hz
        conformer_sd_hz: standard deviation across conformers, in Hz
        uncertainty_hz: prediction uncertainty, in Hz
        model: model used to predict the coupling
    """

    nuclei: tuple[int, int] = (1, 1)
    atom_pairs: Annotated[list[AtomPair], Field(min_length=1)]
    bond_distance: int

    coupling_hz: RoundedHz
    conformer_sd_hz: RoundedHz | None = None
    uncertainty_hz: RoundedHz | None = None
    model: str


class NMRSpectroscopyWorkflow(MoleculeWorkflow):
    """Workflow for calculating NMR spectra.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (currently unused)

        nmr_method: how to run NMR calculations
        solvent: solvent in which to run calculations; must be a key of NMR_SOLVENT_MODELS
        conf_gen_settings: conformer-search settings; if `None`, no conformer search performed
        multistage_opt_settings: optimization settings; if `None`, no optimization performed

        conformers: list of conformer UUIDs
        boltzmann_weights: Boltzmann weights for each conformer
        per_conformer_chemical_shifts: per-atom shifts for each conformer
        chemical_shifts: per-atom shifts
        symmetry_equivalent_nuclei: 0-indexed atoms which are equivalent to one another
        predicted_peaks: predicted NMR peaks
        predicted_couplings: predicted NMR couplings
    """

    nmr_method: NMRMethod = NMRMethod.MAGNETZERO
    solvent: Solvent = Solvent.CHLOROFORM

    conf_gen_settings: ConformerGenSettingsUnion | None = OpenConfSettings()
    multistage_opt_settings: MultiStageOptSettings | None = MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.AIMNET2_WB97MD3, tasks=[Task.OPTIMIZE])],
    )

    conformers: list[UUID] = []
    boltzmann_weights: Annotated[list[float], AfterValidator(round_list(3))] = []
    per_conformer_chemical_shifts: list[Annotated[list[float | None], AfterValidator(round_list(3))]] = []
    chemical_shifts: Annotated[list[float | None], AfterValidator(round_list(3))] = []
    symmetry_equivalent_nuclei: list[list[int]] = []

    predicted_peaks: dict[int, list[NMRPeak]] = {}
    predicted_couplings: list[NMRCoupling] = []

    @model_validator(mode="after")
    def check_solvent_supported(self) -> Self:
        """Check that the solvent is one MagNet is parameterized for."""
        if self.solvent not in NMR_SUPPORTED_SOLVENTS:
            supported = ", ".join(sorted(s.value for s in NMR_SUPPORTED_SOLVENTS))
            raise ValueError(f"Solvent {self.solvent.value!r} is not supported for NMR prediction. Supported solvents: {supported}.")
        return self
