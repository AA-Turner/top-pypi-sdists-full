"""Test surface energy behavior and validation."""

from pytest import fixture, mark, raises

from stjames import Atom, Molecule, OptimizationSettings, Settings
from stjames.method import Method
from stjames.molecule import PeriodicCell
from stjames.workflows import (
    WORKFLOW_MAPPING,
    FacetSurfaceEnergy,
    SurfaceEnergyResult,
    SurfaceEnergyWorkflow,
)

CUBIC_CELL = PeriodicCell(lattice_vectors=((3.0, 0, 0), (0, 3.0, 0), (0, 0, 3.0)), is_periodic=(True, True, True))
SLAB_CELL = CUBIC_CELL.model_copy(update={"is_periodic": (True, True, False)})


@fixture
def crystalline_Po() -> Molecule:
    """Provide fully periodic polonium geometry."""
    return Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=84, position=(0, 0, 0))], cell=CUBIC_CELL)


@fixture
def result() -> SurfaceEnergyResult:
    """Provide facet energies, symmetry equivalents, and surface area fractions."""
    return SurfaceEnergyResult(
        facets=[
            FacetSurfaceEnergy(
                miller_indices=(1, 1, 1),
                surface_energy=1.234567,
                termination=0.0,
                equivalents=[(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)],
                eps_bulk=-1.234567,
                area_fraction=0.6,
            ),
            FacetSurfaceEnergy(
                miller_indices=(1, 0, 0),
                surface_energy=1.5,
                termination=0.25,
                equivalents=[(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)],
                eps_bulk=-1.234567,
                area_fraction=0.4,
            ),
        ],
        skipped_facets=[((1, 1, 0), "could not build a slab with two equivalent faces")],
        space_group="Fm-3m",
        mean_surface_energy=1.3407,
        surface_energy_anisotropy=0.097,
    )


def test_registered() -> None:
    """Resolve the workflow name to its registered schema class."""
    assert WORKFLOW_MAPPING["surface_energy"] is SurfaceEnergyWorkflow


@mark.parametrize(("cell", "match"), [(SLAB_CELL, "fully periodic"), (None, "cell is None")], ids=["slab", "molecule"])
def test_requires_a_fully_periodic_crystal(crystalline_Po: Molecule, cell: PeriodicCell | None, match: str) -> None:
    """Verify requires a fully periodic crystal."""
    aperiodic = crystalline_Po.model_copy(update={"cell": cell})

    with raises(ValueError, match=match):
        SurfaceEnergyWorkflow(initial_molecule=aperiodic, settings=Settings(method=Method.PBE, opt_settings=OptimizationSettings(optimize_cell=True)))


@mark.parametrize(
    ("update", "match"),
    [
        ({"pbc_dft_settings": {"kpoints": (4, 4, 4)}}, "resolves k-points per structure"),
        ({"opt_settings": {"constraints": [{"constraint_type": "freeze_atoms", "atoms": [1]}]}}, "does not support constraints"),
        ({"opt_settings": {"transition_state": True}}, "requires relaxed minima"),
    ],
    ids=["kpoints", "constraints", "transition state"],
)
def test_rejects_settings_a_scan_cannot_honor(crystalline_Po: Molecule, update: dict[str, object], match: str) -> None:
    """Verify rejects settings a scan cannot honor."""
    with raises(ValueError, match=match):
        SurfaceEnergyWorkflow(initial_molecule=crystalline_Po, settings={"method": "pbe"} | update)


def test_most_stable_facet(result: SurfaceEnergyResult) -> None:
    """Select the facet with the lowest surface energy."""
    assert result.most_stable_facet is not None
    assert result.most_stable_facet.miller_indices == (1, 1, 1)
    assert result.most_stable_facet.face_multiplicity == 8
    assert SurfaceEnergyResult().most_stable_facet is None


def test_round_trip(result: SurfaceEnergyResult) -> None:
    """Preserve calculation results through JSON serialization and validation."""
    restored = SurfaceEnergyResult.model_validate_json(result.model_dump_json())

    assert restored.facets[0].surface_energy == 1.2346
    assert restored.facets[0].miller_indices == (1, 1, 1)
    assert restored.skipped_facets[0][0] == (1, 1, 0)
    assert "most_stable_facet" not in restored.model_dump()
