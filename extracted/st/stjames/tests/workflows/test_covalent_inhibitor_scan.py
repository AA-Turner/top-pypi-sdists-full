"""Test covalent inhibitor scan behavior and validation."""

import pytest
from pytest import fixture, raises

from stjames import Engine, Method
from stjames.pdb import PDB, read_pdb
from stjames.workflows import CovalentInhibitorScanWorkflow
from stjames.workflows.covalent_inhibitor_scan import (
    CovalentInhibitorScanPoint,
    UmbrellaSamplingConvergence,
    UmbrellaSamplingScanSettings,
)


@fixture
def protein() -> PDB:
    """Load protein structure for covalent scan validation."""
    return read_pdb("tests/data/1ema.pdb")


def workflow(protein: PDB, **kwargs) -> CovalentInhibitorScanWorkflow:
    """Build covalent inhibitor scan with caller-supplied settings."""
    return CovalentInhibitorScanWorkflow(
        protein=protein,
        protein_reactive_atom_index=2,
        ligand_reactive_atom_index=0,
        reactant_smiles="C=CC(=O)N",
        **kwargs,
    )


def test_defaults(protein: PDB) -> None:
    """Default settings construct and resolve to the intended engines and grid."""
    wf = workflow(protein)
    assert wf.reactant_smiles == "C=CC(=O)N"
    assert wf.settings.calc_settings.method == Method.ORB_V3_CONSERVATIVE_OMOL
    assert wf.settings.calc_settings.engine == Engine.ORB
    # Refined across the barrier, where 0.1 Å spacing gave no replica round trips.
    assert len(wf.settings.window_centers) == 28
    assert wf.settings.window_centers[5:8] == [2.3, 2.35, 2.4]
    assert wf.points == []
    assert wf.convergence is None


def test_rejects_an_empty_window_schedule() -> None:
    """Verify rejects an empty window schedule."""
    with raises(ValueError):
        UmbrellaSamplingScanSettings(window_centers=[])


def test_window_centers_may_descend() -> None:
    """A non-covalent input seeds from its own end, so the schedule may run inwards."""
    settings = UmbrellaSamplingScanSettings(window_centers=[4.0, 2.4, 1.8])
    assert settings.window_centers == [4.0, 2.4, 1.8]


def test_barrier_is_measured_from_the_non_covalent_end(protein: PDB) -> None:
    """The addition barrier is the interior peak above the non-covalent plateau."""
    wf = workflow(
        protein,
        points=[
            CovalentInhibitorScanPoint(index=0, distance=1.8, force_constant=30.0, free_energy=0.0),
            CovalentInhibitorScanPoint(index=1, distance=2.4, force_constant=30.0, free_energy=6.25),
            CovalentInhibitorScanPoint(index=2, distance=4.0, force_constant=30.0, free_energy=-1.5),
        ],
    )
    assert wf.barrier == 7.75


def test_barrier_ignores_the_order_points_arrive_in(protein: PDB) -> None:
    """Points from a descending schedule give the same barrier as the ascending one."""
    wf = workflow(
        protein,
        points=[
            CovalentInhibitorScanPoint(index=0, distance=4.0, force_constant=30.0, free_energy=-1.5),
            CovalentInhibitorScanPoint(index=1, distance=2.4, force_constant=30.0, free_energy=6.25),
            CovalentInhibitorScanPoint(index=2, distance=1.8, force_constant=30.0, free_energy=0.0),
        ],
    )
    assert wf.barrier == 7.75


@pytest.mark.parametrize(
    "energies",
    [[0.0, 2.0, 5.0], [5.0, 2.0, 0.0], [], [0.0, None, 5.0]],
    ids=["rises to the end", "falls from the start", "no points", "a window failed"],
)
def test_barrier_is_none_without_an_interior_peak(protein: PDB, energies: list[float | None]) -> None:
    """A monotonic profile's highest point is a wall, not a transition state."""
    wf = workflow(
        protein,
        points=[CovalentInhibitorScanPoint(index=i, distance=1.8 + i, force_constant=30.0, free_energy=energy) for i, energy in enumerate(energies)],
    )
    assert wf.barrier is None


def test_roundtrip(protein: PDB) -> None:
    """Nested settings and every result field survive a serialization round-trip."""
    wf = workflow(
        protein,
        settings=UmbrellaSamplingScanSettings(window_centers=[1.8, 2.4, 4.0], force_constant=50.0),
        points=[
            CovalentInhibitorScanPoint(index=0, distance=1.8, force_constant=50.0, free_energy=0.0, mean_distance=1.82, n_samples=500),
            CovalentInhibitorScanPoint(index=1, distance=2.4, force_constant=50.0, free_energy=6.25),
            CovalentInhibitorScanPoint(index=2, distance=4.0, force_constant=50.0, free_energy=-1.5),
        ],
        convergence=UmbrellaSamplingConvergence(overlap_matrix=[[0.7, 0.3], [0.3, 0.7]], round_trips=13, worst_pair_acceptance=0.332),
    )
    restored = CovalentInhibitorScanWorkflow.model_validate(wf.model_dump())
    assert restored.reactant_smiles == "C=CC(=O)N"
    assert restored.settings.window_centers == [1.8, 2.4, 4.0]
    assert restored.settings.timestep_fs == 2.0
    assert restored.points[0].mean_distance == 1.82
    assert restored.convergence is not None
    assert restored.convergence.overlap_matrix == [[0.7, 0.3], [0.3, 0.7]]
    assert restored.convergence.round_trips == 13
    assert restored.barrier == 7.75
