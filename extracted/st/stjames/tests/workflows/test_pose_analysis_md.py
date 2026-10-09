"""Test pose analysis md behavior and validation."""

from pytest import fixture

from stjames.pdb import PDB, read_pdb
from stjames.workflows import PoseAnalysisMolecularDynamicsWorkflow


@fixture
def gfp() -> PDB:
    """Green fluorescent protein."""
    return read_pdb("tests/data/1ema.pdb")


def test_raises(gfp: str) -> None:
    """Reject pose analysis without required molecular dynamics inputs."""
    PoseAnalysisMolecularDynamicsWorkflow(protein=gfp, initial_smiles="O")

    PoseAnalysisMolecularDynamicsWorkflow(protein=gfp, initial_smiles="O", protein_restraint_cutoff=5.0)
