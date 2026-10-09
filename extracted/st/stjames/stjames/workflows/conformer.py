"""Deprecated conformer search workflow, use ConformerSearchWorkflow instead."""

from typing import Annotated, Any

from pydantic import AfterValidator

from ..base import Base, round_float, round_optional_float
from ..constraint import Constraint
from ..method import Method
from ..mode import Mode
from ..solvent import Solvent
from .workflow import MoleculeWorkflow


class ConformerSettings(Base):
    """Configure the deprecated conformer search workflow.

    Attributes:
        num_confs_considered: conformers considered for final selection
        num_confs_taken: conformers retained after selection
        rmsd_cutoff: RMSD threshold for duplicate conformers
        transition_state: search for transition-state conformers when true
        final_method: method used for final energies
        solvent: solvent used during the search
        max_energy: maximum energy above the minimum for retained conformers
        constraints: geometric constraints applied during the search
    """

    num_confs_considered: int = 100
    num_confs_taken: int = 50
    rmsd_cutoff: float = 0.1

    transition_state: bool = False
    final_method: Method = Method.AIMNET2_WB97MD3
    solvent: Solvent | None = Solvent.WATER
    max_energy: float = 5

    constraints: list[Constraint] = []


class RdkitConformerSettings(ConformerSettings):
    """Configure RDKit conformer generation for the deprecated workflow.

    Attributes:
        num_initial_confs: initial conformers to generate
        max_mmff_energy: MMFF energy cutoff
        max_mmff_iterations: maximum MMFF optimization iterations
    """

    num_initial_confs: int = 100
    max_mmff_energy: float = 10
    max_mmff_iterations: int = 500


class CrestConformerSettings(ConformerSettings):
    """Configure CREST conformer generation for the deprecated workflow.

    Attributes:
        flags: command-line flags passed to CREST
        gfn: GFN method or force field used by CREST
    """

    flags: str = "--quick --ewin 10"
    gfn: int | str = "ff"


class Conformer(Base):
    """Store a conformer produced by the deprecated workflow.

    Attributes:
        energy: conformer energy in Hartree
        weight: conformer population weight, if available
        uuid: identifier of the conformer, if available
    """

    energy: Annotated[float, AfterValidator(round_float(6))]
    weight: Annotated[float | None, AfterValidator(round_optional_float(6))] = None

    uuid: str | None = None


class ConformerWorkflow(MoleculeWorkflow):
    """Configure the deprecated conformer search workflow.

    Attributes:
        mode: effort mode for the search
        settings: conformer generation and selection settings
        conformers: generated conformers
    """

    mode: Mode = Mode.RAPID
    settings: ConformerSettings = ConformerSettings()
    conformers: list[Conformer] = []

    def model_post_init(self, __context: Any, /) -> None:
        """Resolve conformer settings from the selected effort mode."""
        self.settings = csearch_settings_by_mode(self.mode, self.settings)


def csearch_settings_by_mode(mode: Mode, old_settings: ConformerSettings | None = None) -> ConformerSettings:
    """Choose deprecated conformer search settings for an effort mode.

    Args:
        mode: effort mode used to select defaults
        old_settings: existing settings whose method, solvent, and constraints are retained

    Returns:
        conformer search settings for the selected mode
    """
    if mode == Mode.MANUAL:
        assert old_settings is not None
        return old_settings

    settings: ConformerSettings

    if mode == Mode.METICULOUS:
        settings = CrestConformerSettings(
            gfn=2,
            flags="--ewin 15 --noreftopo",
            max_energy=10,
            num_confs_considered=500,
            num_confs_taken=150,
        )

    elif mode == Mode.CAREFUL:
        settings = CrestConformerSettings(
            gfn="ff",
            flags="--quick --ewin 10 --noreftopo",
            num_confs_considered=150,
            num_confs_taken=50,
        )

    elif mode == Mode.RAPID or Mode.AUTO:
        settings = RdkitConformerSettings(
            num_initial_confs=300,
            max_mmff_energy=15,
            num_confs_considered=100,
            num_confs_taken=50,
        )

    elif mode == Mode.RECKLESS:
        settings = RdkitConformerSettings(
            num_initial_confs=200,
            max_mmff_energy=10,
            num_confs_considered=50,
            num_confs_taken=20,
            rmsd_cutoff=0.25,
        )

    else:
        raise ValueError(f"invalid mode {mode.value} for conformer settings")

    if old_settings is not None:
        settings.final_method = old_settings.final_method
        settings.solvent = old_settings.solvent
        settings.constraints = old_settings.constraints

    return settings
