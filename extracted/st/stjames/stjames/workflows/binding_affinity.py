from typing import Annotated, Literal, Self

from pydantic import AfterValidator, BaseModel, Field, PositiveFloat, model_validator

from ..base import Base, round_float
from ..method import Method
from ..molecule import Molecule
from ..pdb import PDB
from ..protein import ProteinSequence
from ..settings import Settings
from ..solvent import Solvent, SolventModel, SolventSettings
from ..types import UUID
from .multistage_opt import MultiStageOptSettings
from .workflow import ProteinStructureWorkflow


class SinglePointEnergySettings(BaseModel):
    """
    Settings to control running SQM-based binding affinity.

    :param multistage_opt_settings: how to compute energies
    :param truncation_radius: radius beyond which the protein will be truncated, in Å
    """

    multistage_opt_settings: MultiStageOptSettings = MultiStageOptSettings(
        optimization_settings=[
            Settings(
                method=Method.PM6_D3H4X,
                solvent_settings=SolventSettings(
                    solvent=Solvent.WATER,
                    model=SolventModel.COSMO,
                ),
            )
        ],
        singlepoint_settings=Settings(
            method=Method.PM6_D3H4X,
            solvent_settings=SolventSettings(
                solvent=Solvent.WATER,
                model=SolventModel.COSMO2,
            ),
        ),
    )

    truncation_radius: PositiveFloat = 6.0
    settings_type: Literal["single_point_energy"] = "single_point_energy"


class GninaAffinitySettings(BaseModel):
    """Settings for GNINA affinity scoring."""

    settings_type: Literal["gnina"] = "gnina"


class AEVPLIGAffinitySettings(BaseModel):
    """Settings for AEV-PLIG affinity scoring."""

    settings_type: Literal["aev_plig"] = "aev_plig"


class NessoAffinitySettings(BaseModel):
    """Settings for Nesso-1 affinity prediction."""

    settings_type: Literal["nesso"] = "nesso"


BindingAffinitySettings = Annotated[
    SinglePointEnergySettings | GninaAffinitySettings | AEVPLIGAffinitySettings | NessoAffinitySettings,
    Field(discriminator="settings_type"),
]


class BindingAffinityResult(Base):
    """
    Result of computing binding affinity for a given pose.

    :param binding_affinity: binding affinity in kcal/mol for single-point energy
        calculations, or log10(M) for GNINA, AEV-PLIG, and Nesso-1 calculations
    """

    binding_affinity: Annotated[float, AfterValidator(round_float(3))]


class BindingAffinityWorkflow(ProteinStructureWorkflow):
    """
    Workflow for predicting binding affinity of protein–ligand complexes.

    Inherited:
    :param protein: PDB or UUID of the (holo) protein. Nesso-1 instead accepts
        `protein_sequences`.

    New:
    :param ligand_residue_name: which residue to use as the ligand. Requires `protein`
        and exactly one `ligand_smiles` entry.
    :param ligand_structures: which external poses to score. Per-pose topology belongs on
        `Molecule.smiles`, so `ligand_smiles` is not accepted alongside these.
    :param protein_sequences: direct protein sequence input for Nesso-1, in place of `protein`.
    :param ligand_smiles: SMILES of the ligand. Required with `ligand_residue_name`, where
        it supplies the residue's bond orders and formal charge. For Nesso-1 only, may
        instead stand alone as the ligand input.
    :param binding_affinity_settings: how to compute binding affinity

    Results:
    :param binding_affinity_results: the binding affinity for each molecule.
        A value of `None` indicates a failed row.
    """

    protein: PDB | UUID | None = None
    ligand_residue_name: str | None = None
    ligand_structures: list[Molecule] = []
    protein_sequences: list[ProteinSequence] | list[str] = []
    ligand_smiles: list[str] = []

    binding_affinity_settings: BindingAffinitySettings = SinglePointEnergySettings()

    binding_affinity_results: list[BindingAffinityResult | None] = []

    @model_validator(mode="after")
    def validate_pose_input(self) -> Self:
        """Ensure that a valid combination of input types is set."""
        is_nesso = isinstance(self.binding_affinity_settings, NessoAffinitySettings)

        if self.protein_sequences and not is_nesso:
            raise ValueError("`protein_sequences` is only supported by Nesso-1")

        if self.protein is not None and self.protein_sequences:
            raise ValueError("Can only set one of `protein` and `protein_sequences`")
        if self.protein is None and not self.protein_sequences:
            raise ValueError("Must set one of `protein` and `protein_sequences`")

        structural_inputs = [
            name
            for name, value in (
                ("ligand_residue_name", self.ligand_residue_name),
                ("ligand_structures", self.ligand_structures),
            )
            if value
        ]
        if len(structural_inputs) > 1:
            raise ValueError(f"Can only set one structural ligand input, got: {', '.join(structural_inputs)}")
        if not structural_inputs and not self.ligand_smiles:
            raise ValueError("Must set one of `ligand_residue_name`, `ligand_structures`, or `ligand_smiles`")
        if self.ligand_residue_name and self.protein is None:
            raise ValueError("`ligand_residue_name` requires `protein`")

        # A named holo residue carries no reliable bond orders or formal charge, so its
        # topology has to be supplied explicitly.
        if self.ligand_residue_name and len(self.ligand_smiles) != 1:
            raise ValueError(f"`ligand_residue_name` requires exactly one `ligand_smiles` entry giving the ligand's topology, got {len(self.ligand_smiles)}")
        # `ligand_structures` carry their own per-pose topology on `Molecule.smiles`.
        if self.ligand_structures and self.ligand_smiles:
            raise ValueError("`ligand_smiles` is not accepted with `ligand_structures`; set `Molecule.smiles` instead")
        # Standalone SMILES, with no structure to attach to, is accepted only by Nesso-1.
        if self.ligand_smiles and not structural_inputs and not is_nesso:
            raise ValueError("`ligand_smiles` without a structural ligand input is only supported by Nesso-1")

        for sequence in self.protein_sequences:
            value = sequence.sequence if isinstance(sequence, ProteinSequence) else sequence
            if not value.strip():
                raise ValueError("Protein sequences must not be empty for Nesso-1")
        if any(not smiles.strip() for smiles in self.ligand_smiles):
            raise ValueError("`ligand_smiles` entries must not be empty")

        return self
