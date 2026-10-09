"""Test batch protein cofolding behavior and validation."""

from typing import Literal

from pydantic import ValidationError
from pytest import fixture, raises

from stjames import CofoldingModel
from stjames.workflows import BatchProteinCofoldingWorkflow
from stjames.workflows.protein_cofolding import CofoldingResult, PocketConstraint, Token


@fixture
def rec() -> list[str]:
    """Provide receptor sequences for batch cofolding."""
    return ["MK"]


def _pocket(input_type: Literal["ligand", "protein", "dna", "rna"] = "protein", input_index: int = 0) -> PocketConstraint:
    return PocketConstraint(
        input_type=input_type,
        input_index=input_index,
        contacts=[Token(input_type="protein", input_index=0, token_index=5)],
        max_distance=6.0,
    )


def test_axis_must_be_exactly_one(rec: list[str]) -> None:
    """Verify axis must be exactly one."""
    msg = "Batch cofolding requires exactly one of `binder_smiles_list` or `binder_sequences_list` to be populated"

    with raises(ValidationError) as exc:
        BatchProteinCofoldingWorkflow(initial_protein_sequences=rec)
    assert msg in str(exc.value)

    with raises(ValidationError) as exc:
        BatchProteinCofoldingWorkflow(
            initial_protein_sequences=rec,
            binder_smiles_list=["CCO"],
            binder_sequences_list=[["A"]],
        )
    assert msg in str(exc.value)


def test_ligand_pocket_index_in_range(rec: list[str]) -> None:
    # slot 0 is the batch ligand, slot 1 is the cofactor
    """Verify ligand pocket index in range."""
    BatchProteinCofoldingWorkflow(
        initial_protein_sequences=rec,
        binder_smiles_list=["CCO"],
        initial_smiles_list=["N"],
        pocket_constraints=[_pocket("ligand", 1)],
    )

    with raises(ValidationError) as exc:
        BatchProteinCofoldingWorkflow(
            initial_protein_sequences=rec,
            binder_smiles_list=["CCO"],
            pocket_constraints=[_pocket("ligand", 5)],
        )
    assert "Ligand pocket input_index 5 out of range [0, 1)" in str(exc.value)

    with raises(ValidationError) as exc:
        BatchProteinCofoldingWorkflow(
            initial_protein_sequences=rec,
            binder_sequences_list=[["A"]],
            pocket_constraints=[_pocket("ligand", 0)],
        )
    assert "Ligand-side pocket constraints require `binder_smiles_list` or `initial_smiles_list`" in str(exc.value)


def test_per_item_affinity_indices_rejected(rec: list[str]) -> None:
    """Verify per item affinity indices rejected."""
    msg = "Use `compute_affinity=True` in batch cofolding; per-item affinity indices are not applicable"

    with raises(ValidationError) as exc:
        BatchProteinCofoldingWorkflow(
            initial_protein_sequences=rec,
            binder_smiles_list=["CCO"],
            ligand_binding_affinity_index=0,
        )
    assert msg in str(exc.value)

    with raises(ValidationError) as exc:
        BatchProteinCofoldingWorkflow(
            initial_protein_sequences=rec,
            binder_sequences_list=[["A"]],
            protein_binding_affinity_indices=[0],
            model=CofoldingModel.BOLTZ_2_1,
        )
    assert msg in str(exc.value)


def test_cofolding_results_length_must_match_batch(rec: list[str]) -> None:
    """Verify cofolding results length must match batch."""
    wf = BatchProteinCofoldingWorkflow(initial_protein_sequences=rec, binder_smiles_list=["CCO", "CCN"])

    with raises(ValidationError) as exc:
        wf.cofolding_results = [[CofoldingResult()]]
    assert "`cofolding_results` length (1) must match `binder_smiles_list` length (2)" in str(exc.value)
