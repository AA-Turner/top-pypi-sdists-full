"""Protein preparation workflow."""

from typing import Literal, Self

from pydantic import NonNegativeInt, field_validator, model_validator

from ..base import LowercaseStrEnum
from ..types import NonPolymerResidueMapping, ProteinUUID
from .workflow import ProteinStructureWorkflow


class AddMissingMethod(LowercaseStrEnum):
    """Method for adding missing atoms and residues to the structure before protonation."""

    BOLTZ_2 = "boltz_2"
    PDBFIXER = "pdbfixer"


class CapResidueSetting(LowercaseStrEnum):
    """Method for capping terminal residues."""

    ACE_NME = "ace_nme"
    TERMINAL_TEMPLATES = "terminal_templates"


class ProtonationMethod(LowercaseStrEnum):
    """Method to use for adding hydrogens."""

    OPENMM = "openmm"
    PROTONATE_UTILS = "protonate_utils"
    PROPKA_3 = "propka_3"


class ProteinPreparationWorkflow(ProteinStructureWorkflow):
    """
    Protein preparation workflow.

    Inherited:
    :param protein: PDB structure of protein, or UUID of PDB record in Rowan

    New:
    :param sequence_overrides: sequences keyed by chain ID; always take precedence over any SEQRES parsed
        for that chain, whether present or missing
    :param add_missing_method: method for adding missing atoms/residues before protonation; None skips this step
    :param cap_residues: method for capping terminal residues; ACE_NME requires add_missing_method and is incompatible with PROTONATE_UTILS
    :param retain_noncanonical_residues: whether to keep modified polymer residues (e.g. phosphorylated
        TPO/SEP/PTR) as-is; False replaces each with its unmodified parent residue before protonation
    :param pocket_ligand: residue name or 0-based residue index of bound ligand around which to build a Vina-style pocket,
        computed before retain_non_polymer removes any non-polymer residues; None skips pocket construction
    :param retain_non_polymer: non-polymer residues to retain, keyed by residue name or index; only ions/water may map to None, others require a SMILES value
    :param protonation_method: method to use for adding hydrogens
    :param pH: pH value for protonation
    :param retain_protonation: whether to retain existing protonation states

    Results:
    :param prepared_protein: UUID of prepared protein structure
    """

    sequence_overrides: dict[str, str] | None = None
    add_missing_method: Literal[AddMissingMethod.BOLTZ_2, AddMissingMethod.PDBFIXER] | None = AddMissingMethod.BOLTZ_2
    cap_residues: CapResidueSetting | None = CapResidueSetting.ACE_NME
    retain_noncanonical_residues: bool = False
    pocket_ligand: str | NonNegativeInt | None = None
    retain_non_polymer: NonPolymerResidueMapping | None = {"NA": None, "CL": None, "MG": None}
    protonation_method: ProtonationMethod = ProtonationMethod.OPENMM
    pH: float = 7.4
    retain_protonation: bool = True

    prepared_protein: ProteinUUID | None = None

    @field_validator("sequence_overrides")
    @classmethod
    def validate_sequence_overrides(cls, sequence_overrides: dict[str, str] | None) -> dict[str, str] | None:
        """
        Validate sequence override chain IDs and sequences are non-empty.

        :raises ValueError: if chain ID or sequence is empty
        """
        if sequence_overrides is None:
            return sequence_overrides
        for chain_id, sequence in sequence_overrides.items():
            if not chain_id:
                raise ValueError("sequence_overrides chain ID must not be empty")
            if not sequence:
                raise ValueError(f"sequence_overrides entry for chain {chain_id!r} must not be empty")
        return sequence_overrides

    @model_validator(mode="after")
    def validate_cap_residues(self) -> Self:
        """
        Validate cap_residues / add_missing_method / protonation_method compatibility.

        :raises ValueError: if cap_residues=ACE_NME but add_missing_method is None
        :raises ValueError: if cap_residues=ACE_NME but protonation_method is PROTONATE_UTILS
        """
        if self.cap_residues == CapResidueSetting.ACE_NME:
            if self.add_missing_method is None:
                raise ValueError("cap_residues=ACE_NME requires an add_missing_method to be set")
            if self.protonation_method == ProtonationMethod.PROTONATE_UTILS:
                raise ValueError("cap_residues=ACE_NME is not supported with protonation_method=PROTONATE_UTILS")
        return self
