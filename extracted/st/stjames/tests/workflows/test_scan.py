"""Test scan behavior and validation."""

from pytest import approx, fixture, mark, raises

from stjames import Engine, Method, Molecule, Settings
from stjames.coordinate import AngleCoordinate, Coordinate, DihedralCoordinate, DistanceCoordinate, LinearCombinationCoordinate
from stjames.pdb import ResidueAtomRef, ResidueRef
from stjames.workflows import ScanWorkflow
from stjames.workflows.scan import ScanSettings

RESIDUE = ResidueRef("non_polymer", "L.1")


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


def test_concerted_scan(water: Molecule) -> None:
    """Verify concerted scan."""
    ss1 = ScanSettings(type="bond", atoms=[0, 1], start=0.5, stop=1.5, num=11)
    calc_settings = Settings(method=Method.GFN2_XTB)

    scan1d = ScanWorkflow(initial_molecule=water, scan_settings=ss1, calc_settings=calc_settings, calc_engine=Engine.XTB)
    assert isinstance(scan1d.scan_settings, list)

    ss2 = ScanSettings(type="bond", atoms=[2, 1], start=0.5, stop=1.5, num=21)
    with raises(ValueError):
        ScanWorkflow(initial_molecule=water, scan_settings=[ss1, ss2], calc_settings=calc_settings, calc_engine=Engine.XTB)

    ss3 = ScanSettings(type="bond", atoms=[2, 1], start=0.5, stop=1.5, num=11)
    scan1d_concerted = ScanWorkflow(initial_molecule=water, scan_settings=[ss1, ss3], calc_settings=calc_settings, calc_engine=Engine.XTB)
    assert isinstance(scan1d_concerted.scan_settings, list)

    scan2d = ScanWorkflow(initial_molecule=water, scan_settings=ss1, scan_settings_2d=ss2, calc_settings=calc_settings, calc_engine=Engine.XTB)
    assert isinstance(scan2d.scan_settings, list)
    assert isinstance(scan2d.scan_settings_2d, list)

    scan2d_concerted = ScanWorkflow(
        initial_molecule=water, scan_settings=[ss1, ss3], scan_settings_2d=[ss1, ss3], calc_settings=calc_settings, calc_engine=Engine.XTB
    )
    assert isinstance(scan2d_concerted.scan_settings, list)
    assert isinstance(scan2d_concerted.scan_settings_2d, list)


@mark.parametrize(("kind", "atoms"), [("bond", [1, 2]), ("angle", [1, 2, 3]), ("dihedral", [1, 2, 3, 4])])
def test_legacy_coordinate_roundtrip(kind: str, atoms: list[int]) -> None:
    """Resolve legacy geometry without rewriting it during serialization."""
    settings = ScanSettings(type=kind, atoms=atoms, start=3, stop=1, num=3)
    restored = ScanSettings.model_validate_json(settings.model_dump_json())
    assert restored.model_dump() == {"type": kind, "atoms": atoms, "start": 3, "stop": 1, "num": 3}
    assert restored.resolved_coordinate.model_dump(mode="json") == {"type": "distance" if kind == "bond" else kind, "atoms": atoms}


@mark.parametrize(
    "coordinate",
    [
        DistanceCoordinate(atoms=(1, 2)),
        AngleCoordinate(atoms=(1, 2, 3)),
        DihedralCoordinate(atoms=(1, 2, 3, 4)),
        LinearCombinationCoordinate(coordinates=[DistanceCoordinate(atoms=(1, 2)), DistanceCoordinate(atoms=(2, 3))], coefficients=[1, -1]),
    ],
)
def test_explicit_coordinate_roundtrip(coordinate: Coordinate) -> None:
    """Round-trip explicit geometry and preserve the scan grid."""
    settings = ScanSettings(coordinate=coordinate, start=-1, stop=1, num=3)
    restored = ScanSettings.model_validate_json(settings.model_dump_json())
    assert restored.resolved_coordinate == coordinate
    assert restored.model_dump() == {"coordinate": coordinate.model_dump(), "start": -1, "stop": 1, "num": 3}
    assert restored.vals() == approx([-1, 0, 1])


def test_scan_geometry_schema_and_conflicts() -> None:
    """Expose coordinate schemas and reject competing geometry representations."""
    assert "coordinate" in ScanSettings.model_json_schema(mode="serialization")["properties"]
    with raises(ValueError):
        ScanSettings(coordinate=DistanceCoordinate(atoms=(1, 2)), type="bond", atoms=[1, 2], start=-1, stop=1, num=3)


@mark.parametrize("axis", ["scan_settings", "scan_settings_2d"])
@mark.parametrize(
    ("coordinate", "stiffness"),
    [
        (DistanceCoordinate(atoms=(ResidueAtomRef(RESIDUE, "C1"), ResidueAtomRef(RESIDUE, "C2"))), None),
        (LinearCombinationCoordinate(coordinates=[DistanceCoordinate(atoms=(1, 2)), DistanceCoordinate(atoms=(2, 3))], coefficients=[1, -1]), None),
        (DistanceCoordinate(atoms=(1, 2)), 45),
    ],
)
def test_molecule_scan_rejects_unsupported_coordinates(water: Molecule, axis: str, coordinate: Coordinate, stiffness: float | None) -> None:
    """Reject PDB references, combinations, and umbrella stiffness on either axis."""
    valid = ScanSettings(coordinate=DistanceCoordinate(atoms=(1, 2)), start=1, stop=2, num=3)
    payload = {
        "initial_molecule": water,
        "calc_settings": Settings(method=Method.GFN2_XTB),
        "scan_settings": valid,
        axis: ScanSettings(coordinate=coordinate, start=1, stop=2, num=3, force_constant=stiffness),
    }
    with raises(ValueError):
        ScanWorkflow.model_validate(payload)


@mark.parametrize(
    ("pairs", "coefficients"),
    [([], []), ([(1, 2)], []), ([(1, 2)], [0]), ([(1, 2)], [float("nan")]), ([(1, 1)], [1]), ([(1, 2), (2, 1)], [1, -1])],
)
def test_invalid_linear_combination(pairs: list[tuple[int, int]], coefficients: list[float]) -> None:
    """Reject undefined combinations, invalid weights, and duplicate distances."""
    with raises(ValueError):
        LinearCombinationCoordinate.model_validate({"coordinates": [{"atoms": atoms} for atoms in pairs], "coefficients": coefficients})
