"""Test canonical coordinate representations and atom-index validation."""

from pytest import mark, raises

from stjames.coordinate import AngleCoordinate, DihedralCoordinate, DistanceCoordinate
from stjames.pdb import ResidueAtomRef, ResidueRef


@mark.parametrize(
    ("coordinate_class", "atoms"),
    [(DistanceCoordinate, (2, 10)), (AngleCoordinate, (2, 7, 10)), (DihedralCoordinate, (2, 5, 3, 10))],
)
@mark.parametrize("pdb_atoms", [False, True])
def test_coordinate_reversal(
    coordinate_class: type[DistanceCoordinate | AngleCoordinate | DihedralCoordinate], atoms: tuple[int, ...], pdb_atoms: bool
) -> None:
    """Canonicalize full reversal without reordering interior atoms."""
    references = tuple(ResidueAtomRef(ResidueRef("non_polymer", "L.1"), f"C{atom:02}") for atom in atoms) if pdb_atoms else atoms
    coordinate = coordinate_class.model_validate({"atoms": references})
    reversed_coordinate = coordinate_class.model_validate({"atoms": references[::-1]})
    assert coordinate.atoms == references
    assert reversed_coordinate == coordinate
    assert reversed_coordinate.model_dump_json() == coordinate.model_dump_json()


@mark.parametrize(
    ("coordinate_class", "atoms"),
    [(DistanceCoordinate, (1, 2)), (AngleCoordinate, (1, 2, 3)), (DihedralCoordinate, (1, 2, 3, 4))],
)
@mark.parametrize("invalid_index", [0, -1])
def test_coordinate_requires_positive_indices(
    coordinate_class: type[DistanceCoordinate | AngleCoordinate | DihedralCoordinate], atoms: tuple[int, ...], invalid_index: int
) -> None:
    """Reject nonpositive molecule indices for every primitive coordinate."""
    with raises(ValueError):
        coordinate_class.model_validate({"atoms": (invalid_index, *atoms[1:])})
