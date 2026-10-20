"""Test protein md behavior and validation."""

import re

import pytest
from pytest import fixture

from stjames.pdb import PDB, read_pdb
from stjames.workflows import ProteinMolecularDynamicsWorkflow
from stjames.workflows.protein_md import Binder, BindingPoseTrajectory, HydrationSite


@pytest.mark.parametrize("random_seed", [0, 2147483648])
def test_random_seed_outside_openmm_range(multichain: PDB, random_seed: int) -> None:
    """Reject OpenMM's automatic-seed sentinel and signed-integer overflow."""
    with pytest.raises(ValueError, match="random_seed"):
        ProteinMolecularDynamicsWorkflow.model_validate({"protein": multichain, "random_seed": random_seed})


@fixture
def multichain() -> PDB:
    """Two-chain protein with a small-molecule ligand (chains A, B; ligand LIG)."""
    return read_pdb("tests/data/multichain_with_ligand.pdb")


def test_legacy_keys_accepted() -> None:
    """Map legacy ligand trajectory and hydration keys to current binder fields."""
    traj = BindingPoseTrajectory.model_validate({"uuid": "test-uuid", "ligand_rmsd": [1.0, 2.0]})
    assert traj.binder_rmsd == [1.0, 2.0]

    site = HydrationSite.model_validate({"centroid": (0.0, 0.0, 0.0), "abs_occ": 0.5, "lig_only_abs_occ": 0.3})
    assert site.binder_only_abs_occ == 0.3


def test_binder_raises_no_components() -> None:
    """Verify binder raises no components."""
    with pytest.raises(ValueError, match=re.escape("at least one of chain_ids or small_molecule_residues must be set")):
        Binder()


def test_workflow_raises_empty_smiles(multichain: PDB) -> None:
    """Verify workflow raises empty smiles."""
    with pytest.raises(ValueError, match=re.escape("non-polymer residue entry 'LIG' has an empty SMILES string")):
        ProteinMolecularDynamicsWorkflow(protein=multichain, small_molecules={"LIG": ""})


def test_workflow_raises_none_smiles_for_non_ion(multichain: PDB) -> None:
    """Verify workflow raises none smiles for non ion."""
    with pytest.raises(ValueError, match="requires a SMILES string"):
        ProteinMolecularDynamicsWorkflow(protein=multichain, small_molecules={"LIG": None})


def test_workflow_combined_binder(multichain: PDB) -> None:
    """Verify workflow combined binder."""
    ProteinMolecularDynamicsWorkflow(
        protein=multichain,
        small_molecules={"LIG": "CCO"},
        binder=Binder(chain_ids=["A"], small_molecule_residues=["LIG"]),
    )


def test_workflow_raises_missing_chain(multichain: PDB) -> None:
    """Verify workflow raises missing chain."""
    with pytest.raises(ValueError, match=re.escape("binder chain_ids ['Z'] not found in PDB (available chains: ['A', 'B'])")):
        ProteinMolecularDynamicsWorkflow(protein=multichain, binder=Binder(chain_ids=["Z"]))


def test_workflow_raises_all_chains_are_binder(multichain: PDB) -> None:
    """Verify workflow raises all chains are binder."""
    with pytest.raises(ValueError, match=re.escape("binder chain_ids covers every polymer chain (['A', 'B']); no receptor would remain")):
        ProteinMolecularDynamicsWorkflow(protein=multichain, binder=Binder(chain_ids=["A", "B"]))


def test_frame_save_interval_valid(multichain: PDB) -> None:
    """Verify frame save interval valid."""
    wf = ProteinMolecularDynamicsWorkflow(protein=multichain, timestep_fs=4, frame_save_interval_ps=2.5)
    assert wf.frame_save_interval_ps == 2.5


def test_frame_save_interval_not_multiple_of_timestep(multichain: PDB) -> None:
    """Verify frame save interval not multiple of timestep."""
    with pytest.raises(ValueError, match="integer multiple of timestep_fs"):
        ProteinMolecularDynamicsWorkflow(protein=multichain, timestep_fs=6, frame_save_interval_ps=1.0)
