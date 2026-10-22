"""Test protein cofolding model validation."""

from pydantic import ValidationError
from pytest import mark, raises

from stjames import CofoldingModel
from stjames.protein import ProteinSequence
from stjames.workflows import ProteinCofoldingWorkflow
from stjames.workflows.protein_cofolding import BondConstraint, PocketConstraint, Token

ESMFOLD_2_MODELS = [CofoldingModel.ESMFOLD_2, CofoldingModel.ESMFOLD_2_FAST]


@mark.parametrize("model", ESMFOLD_2_MODELS)
def test_esmfold2_rejects_cyclic(model: CofoldingModel) -> None:
    """Reject cyclic proteins for ESMFold2 models."""
    with raises(ValidationError, match="cyclic"):
        ProteinCofoldingWorkflow(
            initial_protein_sequences=[ProteinSequence(sequence="MKTAYIAKQR", cyclic=True)],
            model=model,
        )


@mark.parametrize("model", ESMFOLD_2_MODELS)
def test_esmfold2_accepts_primary_ligand_index(model: CofoldingModel) -> None:
    """Accept `ligand_binding_affinity_index`, which selects the primary ligand for pose refinement."""
    wf = ProteinCofoldingWorkflow(
        initial_protein_sequences=["MKTAYIAKQR"],
        initial_smiles_list=["CCO"],
        ligand_binding_affinity_index=0,
        model=model,
    )
    assert wf.ligand_binding_affinity_index == 0


@mark.parametrize("model", ESMFOLD_2_MODELS)
def test_esmfold2_accepts_bond_constraints(model: CofoldingModel) -> None:
    """Accept covalent bond constraints for ESMFold2 models."""
    wf = ProteinCofoldingWorkflow(
        initial_protein_sequences=["MKTCYIAKQR"],
        initial_smiles_list=["CCS"],
        bond_constraints=[
            BondConstraint(
                atom_1=Token(input_type="protein", input_index=0, token_index=3, atom_name="SG"),
                atom_2=Token(input_type="ligand", input_index=0, token_index=2),
            )
        ],
        model=model,
    )
    assert len(wf.bond_constraints) == 1


@mark.parametrize("model", ESMFOLD_2_MODELS)
def test_esmfold2_rejects_pocket_constraints(model: CofoldingModel) -> None:
    """Reject pocket constraints, which ESMFold2 does not condition on."""
    with raises(ValidationError, match="pocket_constraints"):
        ProteinCofoldingWorkflow(
            initial_protein_sequences=["MKTAYIAKQR"],
            initial_smiles_list=["CCO"],
            pocket_constraints=[
                PocketConstraint(
                    input_type="ligand",
                    input_index=0,
                    contacts=[Token(input_type="protein", input_index=0, token_index=3)],
                    max_distance=6.0,
                )
            ],
            model=model,
        )
