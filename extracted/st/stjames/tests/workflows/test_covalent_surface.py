"""Validation and serialization of explicit reaction-coordinate scans."""

from pytest import approx, mark, raises

from stjames.coordinate import AngleCoordinate, Coordinate, DihedralCoordinate, DistanceCoordinate, LinearCombinationCoordinate
from stjames.pdb import ResidueAtomRef, ResidueRef
from stjames.restraint import MDRestraints, RestraintType
from stjames.types import SimpleProteinMDTrajectory
from stjames.workflows.covalent_inhibitor_scan import (
    CovalentInhibitorScanSettings,
    CovalentInhibitorScanWorkflow,
    FreeEnergySurface,
    UmbrellaWindowResult,
)
from stjames.workflows.scan import ScanSettings

RESIDUE = ResidueRef("polymer", "A", "A.12")
LIGAND = ResidueRef("non_polymer", "B.1")
DONOR = ResidueAtomRef(residue=RESIDUE, atom_name="SG")
HYDROGEN = ResidueAtomRef(residue=RESIDUE, atom_name="HG")
ACCEPTOR = ResidueAtomRef(residue=LIGAND, atom_name="C1")
TRANSFER = ScanSettings(
    coordinate=LinearCombinationCoordinate(
        coordinates=[DistanceCoordinate(atoms=(DONOR, HYDROGEN)), DistanceCoordinate(atoms=(ACCEPTOR, HYDROGEN))],
        coefficients=[0.5, -0.5],
    ),
    force_constant=45,
    start=-1,
    stop=1,
    num=5,
)
BOND = ScanSettings(coordinate=DistanceCoordinate(atoms=(ACCEPTOR, DONOR)), force_constant=45, start=4, stop=2, num=3)


@mark.parametrize("axes", [[TRANSFER], [BOND, TRANSFER]])
def test_coordinate_roundtrip(axes: list[ScanSettings]) -> None:
    """Preserve coordinates, mixed restraint selections, and missing surface cells."""
    dimensions = len(axes)
    energies = [*range(2**dimensions - 1), None]
    workflow = CovalentInhibitorScanWorkflow(
        protein="00000000-0000-0000-0000-000000000001",
        reactant_smiles="C",
        settings=CovalentInhibitorScanSettings(
            scan_coordinates=axes,
            reactive_region=[RESIDUE, LIGAND],
            ligand=LIGAND,
            bootstrap_samples=50,
            restraints=[
                MDRestraints(restraint_type=RestraintType.POSITION, selections=[RESIDUE], force_constant=1),
                MDRestraints(restraint_type=RestraintType.DISTANCE, selections=[LIGAND, DONOR], target=4, force_constant=2),
                MDRestraints(restraint_type=RestraintType.DISTANCE, selections=[DONOR, HYDROGEN], target=1.3, force_constant=100, flat_bottom_range=0.1),
            ],
        ),
        topology_uuid="00000000-0000-0000-0000-000000000002",
        windows=[
            UmbrellaWindowResult(
                index=[0] * dimensions,
                centers=[axis.start for axis in axes],
                trajectory=SimpleProteinMDTrajectory(uuid="00000000-0000-0000-0000-000000000003"),
            )
        ],
        surface=FreeEnergySurface(
            bin_edges=[[-1, 0, 1], [2, 3, 4]][:dimensions],
            free_energies=energies,
            effective_samples=[20] * (len(energies) - 1) + [0],
            uncertainty=[None] * len(energies),
        ),
    )
    restored = CovalentInhibitorScanWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.model_dump(mode="json") == workflow.model_dump(mode="json")
    assert restored.surface is not None
    assert restored.surface.shape == [2] * dimensions


@mark.parametrize(
    "coordinate",
    [
        DistanceCoordinate(atoms=(1, 2)),
        LinearCombinationCoordinate(coordinates=[DistanceCoordinate(atoms=(1, 2))], coefficients=[1]),
        AngleCoordinate(atoms=(DONOR, HYDROGEN, ACCEPTOR)),
        DihedralCoordinate(atoms=(DONOR, HYDROGEN, ACCEPTOR, ResidueAtomRef(LIGAND, "C2"))),
    ],
)
def test_unsupported_umbrella_coordinate(coordinate: Coordinate) -> None:
    """Restrict covalent umbrellas to PDB distances and distance combinations."""
    with raises(ValueError):
        CovalentInhibitorScanSettings(
            scan_coordinates=[ScanSettings(coordinate=coordinate, start=0, stop=1, num=3)], reactive_region=[RESIDUE, LIGAND], ligand=LIGAND
        )


def test_zero_scan_range() -> None:
    """Reject coincident umbrella centers."""
    with raises(ValueError):
        CovalentInhibitorScanSettings(scan_coordinates=[BOND.model_copy(update={"start": BOND.stop})], reactive_region=[RESIDUE, LIGAND], ligand=LIGAND)


@mark.parametrize(("stiffness", "expected"), [(None, 45), (60, 60)])
def test_umbrella_stiffness_default(stiffness: float | None, expected: float) -> None:
    """Resolve umbrella stiffness without changing the supplied coordinate."""
    coordinate = DistanceCoordinate(atoms=(DONOR, ACCEPTOR))
    bond = ScanSettings(coordinate=coordinate, start=4, stop=2, num=3, force_constant=stiffness)
    settings = CovalentInhibitorScanSettings(scan_coordinates=[bond], reactive_region=[RESIDUE, LIGAND], ligand=LIGAND)
    assert settings.scan_coordinates[0].force_constant == approx(expected)
    assert bond.force_constant == stiffness
    assert settings.distance_expressions == [{coordinate.atoms: 1}]


@mark.parametrize("scale", [-2, 1, 1e-20])
def test_dependent_coordinates(scale: float) -> None:
    """Reject reordered, reversed, and rescaled axes."""
    dependent = ScanSettings(
        coordinate=LinearCombinationCoordinate(
            coordinates=[DistanceCoordinate(atoms=(HYDROGEN, ACCEPTOR)), DistanceCoordinate(atoms=(HYDROGEN, DONOR))],
            coefficients=[-0.5 * scale, 0.5 * scale],
        ),
        force_constant=45,
        start=-2,
        stop=3,
        num=4,
    )
    with raises(ValueError, match="independent"):
        CovalentInhibitorScanSettings(scan_coordinates=[TRANSFER, dependent], reactive_region=[RESIDUE, LIGAND], ligand=LIGAND)


def test_independent_shared_terms() -> None:
    """Allow shared distances without treating independent expressions as duplicates."""
    distance = ScanSettings(coordinate=DistanceCoordinate(atoms=(DONOR, HYDROGEN)), force_constant=45, start=1, stop=2, num=3)
    settings = CovalentInhibitorScanSettings(scan_coordinates=[TRANSFER, distance], reactive_region=[RESIDUE, LIGAND], ligand=LIGAND)
    assert settings.model_dump()["scan_coordinates"] == [TRANSFER.model_dump(), distance.model_dump()]


def test_coordinate_outside_region() -> None:
    """Reject coordinate atoms outside the selected reactive region."""
    with raises(ValueError):
        CovalentInhibitorScanSettings(scan_coordinates=[TRANSFER], reactive_region=[LIGAND], ligand=LIGAND)


def test_surface_shape() -> None:
    """Reject result arrays that do not match the surface grid."""
    with raises(ValueError):
        FreeEnergySurface(bin_edges=[[0, 1, 2]], free_energies=[0], effective_samples=[1], uncertainty=[None])


def test_fractional_frame_step() -> None:
    """Reject frame intervals that cannot be scheduled on integer simulation steps."""
    with raises(ValueError):
        CovalentInhibitorScanSettings(
            scan_coordinates=[TRANSFER],
            reactive_region=[RESIDUE, LIGAND],
            ligand=LIGAND,
            timestep_fs=0.1,
            frame_save_interval_ps=0.00015,
        )


def test_frame_interval_independent_of_sampling() -> None:
    """Preserve sub-femtosecond frame intervals independently of MBAR and exchange cadence."""
    settings = CovalentInhibitorScanSettings(
        scan_coordinates=[TRANSFER],
        reactive_region=[RESIDUE, LIGAND],
        ligand=LIGAND,
        timestep_fs=0.1,
        frame_save_interval_ps=0.0003,
    )
    restored = CovalentInhibitorScanSettings.model_validate_json(settings.model_dump_json())
    assert restored.frame_save_interval_ps == 0.0003
