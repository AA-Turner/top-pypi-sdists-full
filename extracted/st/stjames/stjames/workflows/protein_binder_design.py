"""Protein-binder-design workflow."""

from enum import Enum
from typing import Annotated

from pydantic import AfterValidator

from ..base import Base, LowercaseStrEnum, round_optional_float
from ..protein import ProteinSequence
from ..types import ProteinUUID
from .workflow import Workflow


class BoltzGenSecondaryStructure(Base):
    """Represents the secondary structure assignments for a protein.

    Attributes:
        id: Identifier for this secondary structure annotation.
        sheet: String encoding the residue indices comprising β-sheet structures
                  (e.g., "1,3..11" for residues 1, and 3 through 11).

        helix: String encoding residue indices comprising helices.
        loop: String encoding residue indices comprising loop or coil regions.
    """

    id: str | None = None
    sheet: str | None = None
    helix: str | None = None
    loop: str | None = None


class BoltzGenProteinEntity(Base):
    """Represents a protein entity, either a designed or natural sequence.

    Attributes:
        id: Unique identifier for the protein.
        sequence: Protein sequence, may contain amino acids and numbers for designed regions.
        secondary_structure: Assigned secondary structure.
        cyclic: Indicates whether the protein is cyclic.
    """

    id: str
    sequence: str  # can include amino acids as well as numbers for designed regions
    secondary_structure: BoltzGenSecondaryStructure | None = None
    # binding_types: BindingType | None = None - we may want to add this later but not used in examples.
    cyclic: bool | None = None


class BoltzGenLigandEntity(Base):
    """Represents a ligand entity (non-protein), such as a small molecule.

    Attributes:
        id: Unique identifier for the ligand.
        smiles: SMILES string representation of the ligand.
    """

    id: str
    smiles: str
    # binding_types: str | None = None - we may want to add this later but not used in examples.


class BoltzGenRegionSelection(Base):
    """Defines a region of a protein chain by specifying its chain identifier and (optionally) residue indices.

    Attributes:
        chain_id: Identifier for the protein chain (e.g., 'A', 'B', etc.).
        residue_indices: Residues to select, specified as a string in the format "5..7,13" or "5..15,50..".
    """

    chain_id: str | None = None
    residue_indices: str | None = None


class BoltzGenProximityRegionSelection(BoltzGenRegionSelection):
    """Defines a region of a protein chain based on spatial proximity to a selection of residues.

    Inherits:
        BoltzGenRegionSelection

    Attributes:
        radius: Radius in angstroms (Å) used to select all residues within proximity to the specified region.
    """

    radius: int | None = None


class BoltzGenBindingType(Base):
    """Represents the binding interface specification for a given protein chain.

    Attributes:
        chain_id: Identifier for the protein chain (e.g., 'A', 'B', etc.).
        binding: Residue indices or regions that are required to participate in binding
            (e.g., "5..7,13" or "all" for the whole chain).

        not_binding: Residue indices or regions that should explicitly not participate in binding
            (e.g., "5..7,13" or "all" for excluding the entire chain).
    """

    chain_id: str | None = None
    binding: str | None = None
    not_binding: str | None = None


class BoltzGenSecondaryStructureOptions(str, Enum):
    """Select a secondary structure constraint for binder design."""

    UNSPECIFIED = "UNSPECIFIED"
    LOOP = "LOOP"
    HELIX = "HELIX"
    SHEET = "SHEET"


class BoltzGenDesignInsertion(Base):
    """Represents an insertion site for protein design in a specific chain.

    Attributes:
        chain_id: Identifier of the chain where the insertion occurs.
        residue_index: Position in the chain after which the insertion is to be made.
        number_of_residues: Number of residues to insert at the specified site (can be a string pattern).
        secondary_structure: Desired secondary structure type for the inserted residues
            ("UNSPECIFIED", "LOOP", "HELIX", or "SHEET").
    """

    chain_id: str
    residue_index: int
    number_of_residues: str
    secondary_structure: BoltzGenSecondaryStructureOptions | None = None


class BoltzGenFileEntity(Base):
    """Represent a protein structure input for the BoltzGen binder design workflow.

    Region selections and design specifications accompany the structure.

    Attributes:
        uuid: Unique identifier for the protein structure.
        include: List of regions to include in the design or analysis context.
        exclude: List of regions to explicitly exclude from consideration (e.g., for ignoring noisy/irrelevant regions).
        include_proximity: List of regions defined by spatial proximity (e.g., residues within a given radius).
        binding_types: List of binding type constraints or permitted interface regions.
        design: List of regions that are being subject to design (mutable, allowed to change).
        secondary_structure: List of desired or annotated secondary structure definitions for selected regions.
        design_insertions: List of new regions to be inserted with specified properties (e.g., insertion sites, structure preferences).
    """

    uuid: ProteinUUID
    include: list[BoltzGenRegionSelection] = []
    exclude: list[BoltzGenRegionSelection] = []
    # fuse: None  - we may want to add this later but not used in examples.
    include_proximity: list[BoltzGenProximityRegionSelection] = []
    binding_types: list[BoltzGenBindingType] = []
    # structure_groups: None - we may want to add this later but not used in examples.
    design: list[BoltzGenRegionSelection] = []
    secondary_structure: list[BoltzGenSecondaryStructure] = []
    design_insertions: list[BoltzGenDesignInsertion] = []


class BoltzGenAtomSpecification(Base):
    """Atom specification for a protein chain, used for applying constraints or referencing atoms.

    Attributes:
        chain_id: Identifier for the protein chain (e.g., "A", "B").
        index: Residue index the atom belongs to (integer, 1-based).
        atom_name: Name of the atom (e.g., "CA", "N", "O", etc.).
    """

    chain_id: str
    index: int
    atom_name: str


class BoltzGenConstraint(Base):
    """Describes a covalent or spatial constraint between two specified atoms in the context of protein design.

    Attributes:
        atom1: First atom in the constraint.
        atom2: Second atom in the constraint.
    """

    atom1: BoltzGenAtomSpecification
    atom2: BoltzGenAtomSpecification


class BoltzGenInput(Base):
    """Represents the primary input schema for the boltzgen application.

    Attributes:
        protein_entities: Protein chains that are designed or targeted for binding.
        ligand_entities: Small molecules or other non-protein ligands relevant to the design.
        file_entities: 3d protein structures and input settings related to them.
        constraints: Covalent bond constraints
    """

    protein_entities: list[BoltzGenProteinEntity] = []
    ligand_entities: list[BoltzGenLigandEntity] = []
    file_entities: list[BoltzGenFileEntity] = []
    constraints: list[BoltzGenConstraint] = []


class BoltzGenScores(Base):
    """Compact, interpretable metrics for a designed binder.

    ↑ higher is better, ↓ lower is better

    Attributes:
        quality_score: aggregate model quality (↑)
        num_filters_passed: number of QC/heuristic filters passed (↑)
        iptm: inter-chain pTM confidence, 0–1 (↑)
        design_ptm: design pTM confidence, 0–1 (↑)
        min_interaction_pae: minimum interface PAE, in Å (↓)
        bb_rmsd: backbone RMSD, in Å (↓)
        delta_sasa_refolded: ΔSASA of interface after refolding, Å² (↑ typically indicates better burial)
        plip_hbonds_refolded: count of hydrogen bonds at the interface (↑)
        plip_saltbridge_refolded: count of salt bridges at the interface (↑)
        liability_score: composite liabilities score (↓)
        liability_high_severity_violations: count of high-severity liabilities (↓)
        liability_num_violations: total liability count (↓)
        helix: fraction helical content, 0–1
        sheet: fraction β-sheet content, 0–1
        loop: fraction loop/coil content, 0–1
        design_largest_hydrophobic_patch_refolded: largest hydrophobic patch area after refolding, Å²
        design_hydrophobicity: overall design hydrophobicity score (unitless)
        num_tokens: sequence length / token count

        min_design_to_target_pae: minimum predicted aligned error between design and target, in Å
        design_to_target_iptm: interface predicted template modeling score between design and target
    """

    quality_score: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    num_filters_passed: int | None = None

    iptm: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    design_ptm: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    min_design_to_target_pae: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    design_to_target_iptm: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    min_interaction_pae: Annotated[float | None, AfterValidator(round_optional_float(3))] = None

    bb_rmsd: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    delta_sasa_refolded: Annotated[float | None, AfterValidator(round_optional_float(3))] = None

    plip_hbonds_refolded: int | None = None
    plip_saltbridge_refolded: int | None = None

    liability_score: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    liability_high_severity_violations: int | None = None
    liability_num_violations: int | None = None

    helix: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    sheet: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    loop: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    design_largest_hydrophobic_patch_refolded: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    design_hydrophobicity: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    num_tokens: int | None = None


class ProteinBinderDesignResult(Base):
    """The output; a designed binder.

    Attributes:
        binder_sequence: legacy sequence of the designed binder
        binder_sequences: designed binder sequences with metadata
        bound_structure: PDB of structure bound to target
        scores: scores for generated structure
    """

    binder_sequence: str | None = None  # deprecated
    binder_sequences: list[ProteinSequence] | None = None
    bound_structure: ProteinUUID | None = None
    scores: BoltzGenScores | None = None


class BoltzGenProtocol(LowercaseStrEnum):
    """The predefined protocol used for generation + filtering."""

    PROTEIN_ANYTHING = "protein-anything"
    PEPTIDE_ANYTHING = "peptide-anything"
    PROTEIN_SMALL_MOLECULE = "protein-small_molecule"
    NANOBODY_ANYTHING = "nanobody-anything"


class BoltzGenSettings(Base):
    """The settings for running BoltzGen.

    Attributes:
        num_designs: how many designs to generate
        protocol: which protocol to use
        budget: budget for the design run
    """

    protocol: BoltzGenProtocol = BoltzGenProtocol.PROTEIN_ANYTHING
    num_designs: int = 100
    budget: int = 20


class ProteinBinderDesignWorkflow(Workflow):
    """A workflow for generating proteins or peptides that bind to something.

    Attributes:
        binder_design_input: input to protein binder design workflow
        binder_design_settings: settings for protein generation method employed
        generated_binders: output structures
    """

    binder_design_input: BoltzGenInput = BoltzGenInput()
    binder_design_settings: BoltzGenSettings = BoltzGenSettings()

    generated_binders: list[ProteinBinderDesignResult] = []
