"""Batch protein cofolding workflow."""

from typing import Annotated, Self

from pydantic import AfterValidator, ConfigDict, model_validator

from ..base import round_float
from ..protein import ProteinSequence
from .protein_cofolding import (
    CofoldingModel,
    CofoldingResult,
    CofoldingTemplate,
    PocketConstraint,
)
from .protein_preparation import ProtonationMethod
from .workflow import FASTAWorkflow


class BatchProteinCofoldingWorkflow(FASTAWorkflow):
    """
    Batch co-folding: each binder is folded separately against the shared
    receptor context. Exactly one of `binder_smiles_list` or
    `binder_sequences_list` must be populated.

    Inherited:
    :param initial_protein_sequences: shared protein sequences
    :param initial_dna_sequences: shared DNA sequences
    :param initial_rna_sequences: shared RNA sequences
    :param initial_smiles_list: shared small-molecule cofactors (e.g. ATP, heme)

    New:
    :param binder_smiles_list: SMILES batch axis
    :param binder_sequences_list: protein-binder batch axis; each entry is one
        binder's chain list (e.g. Fab = [heavy, light])
    :param use_msa_server: whether to use the MSA server
    :param use_potentials: whether to use the potentials (inference-time steering) with Boltz
    :param pocket_constraints: Boltz pocket constraints
    :param templates: structural templates to guide prediction (Boltz-2 / Boltz-2.1 / OpenFold-3)
    :param protonation_method: method used to protonate polymers; `None` skips protonation
        (incompatible with `do_pose_refinement`)
    :param pH: pH value used for protonation
    :param do_pose_refinement: whether to optimize non-rotatable bonds in output poses
        (SMILES batch only)
    :param compute_strain: whether to compute the strain of the pose (if pose_refinement is
        enabled; SMILES batch only)
    :param num_samples: number of samples generated per binder
    :param model: which cofolding model to use
    :param compute_affinity: compute binding affinity for every binder
        (Boltz-2 / Boltz-2.1 for SMILES; Boltz-2.1 for protein binders)
    :param cofolding_results: per-binder list of per-sample outputs
    """

    model_config = ConfigDict(validate_assignment=True)

    binder_smiles_list: list[str] = []
    binder_sequences_list: list[list[ProteinSequence] | list[str]] = []

    use_msa_server: bool = False
    use_potentials: bool = False
    pocket_constraints: list[PocketConstraint] = []
    templates: list[CofoldingTemplate] = []
    protonation_method: ProtonationMethod | None = ProtonationMethod.OPENMM
    pH: Annotated[float, AfterValidator(round_float(2))] = 7.4
    do_pose_refinement: bool = False
    compute_strain: bool = False
    num_samples: int | None = None

    model: CofoldingModel = CofoldingModel.BOLTZ_2
    compute_affinity: bool = False

    cofolding_results: list[list[CofoldingResult]] | None = None

    @model_validator(mode="after")
    def validate_model_compatibility(self) -> Self:
        """Validate feature/model compatibility and batch-specific constraint scope."""
        smiles_batch = bool(self.binder_smiles_list)
        binder_batch = bool(self.binder_sequences_list)
        if smiles_batch == binder_batch:
            raise ValueError("Batch cofolding requires exactly one of `binder_smiles_list` or `binder_sequences_list` to be populated")

        if binder_batch and any(not chains for chains in self.binder_sequences_list):
            raise ValueError("Every entry in `binder_sequences_list` must contain at least one chain")

        ligand_slot_count = (1 if smiles_batch else 0) + len(self.initial_smiles_list)
        for pc in self.pocket_constraints:
            if any(t.input_type == "ligand" for t in pc.contacts):
                raise ValueError("Pocket-constraint contacts must reference polymer residues, not ligands")
            if pc.input_type == "ligand":
                if ligand_slot_count == 0:
                    raise ValueError("Ligand-side pocket constraints require `binder_smiles_list` or `initial_smiles_list`")
                if not 0 <= pc.input_index < ligand_slot_count:
                    raise ValueError(f"Ligand pocket input_index {pc.input_index} out of range [0, {ligand_slot_count})")

        if any(p.force for p in self.pocket_constraints) and not self.use_potentials:
            raise ValueError("use_potentials must be True when any pocket_constraint has force=True")

        boltz_models = {CofoldingModel.BOLTZ_1, CofoldingModel.BOLTZ_2, CofoldingModel.BOLTZ_2_1, CofoldingModel.DECAF_BOLTZ}

        if self.use_potentials and self.model not in boltz_models:
            raise ValueError(f"use_potentials requires a Boltz model, got {self.model}")

        if self.pocket_constraints and self.model not in boltz_models:
            raise ValueError(f"pocket_constraints require a Boltz model, got {self.model}")

        if self.model == CofoldingModel.OPENFOLD_3 and any(t.max_distance is not None for t in self.templates):
            raise ValueError("max_distance in templates is not supported by OpenFold-3")

        if self.templates and self.model not in {CofoldingModel.BOLTZ_2, CofoldingModel.BOLTZ_2_1, CofoldingModel.OPENFOLD_3}:
            raise ValueError(f"templates require Boltz-2, Boltz-2.1, or OpenFold-3, got {self.model}")

        if any(t.max_distance is not None for t in self.templates) and not self.use_potentials:
            raise ValueError("use_potentials must be True when any template specifies max_distance")

        if self.model == CofoldingModel.OPENFOLD_3:
            cyclic_proteins = [seq for seq in self.initial_protein_sequences if hasattr(seq, "cyclic") and seq.cyclic]
            cyclic_binders = [seq for chains in self.binder_sequences_list for seq in chains if hasattr(seq, "cyclic") and seq.cyclic]
            if cyclic_proteins or cyclic_binders:
                raise ValueError("OpenFold-3 does not support cyclic proteins")

        if self.compute_affinity:
            if binder_batch and self.model != CofoldingModel.BOLTZ_2_1:
                raise ValueError(f"compute_affinity on protein binders requires Boltz-2.1, got {self.model}")
            if smiles_batch and self.model not in {CofoldingModel.BOLTZ_2, CofoldingModel.BOLTZ_2_1}:
                raise ValueError(f"compute_affinity requires Boltz-2 or Boltz-2.1, got {self.model}")

        if binder_batch and self.do_pose_refinement:
            raise ValueError("do_pose_refinement is ligand-only and cannot be used with protein-binder batches")

        if binder_batch and self.compute_strain:
            raise ValueError("compute_strain is ligand-only and cannot be used with protein-binder batches")

        if self.compute_strain and not self.do_pose_refinement:
            raise ValueError("compute_strain requires do_pose_refinement=True")

        if self.do_pose_refinement and self.protonation_method is None:
            raise ValueError("do_pose_refinement requires a protonation_method")

        if self.ligand_binding_affinity_index is not None or self.protein_binding_affinity_indices is not None:
            raise ValueError("Use `compute_affinity=True` in batch cofolding; per-item affinity indices are not applicable")

        if self.cofolding_results is not None:
            expected = len(self.binder_smiles_list) if smiles_batch else len(self.binder_sequences_list)
            if len(self.cofolding_results) != expected:
                axis = "binder_smiles_list" if smiles_batch else "binder_sequences_list"
                raise ValueError(f"`cofolding_results` length ({len(self.cofolding_results)}) must match `{axis}` length ({expected})")

        return self
