"""Connection identity and filtering independent of atom serial numbering."""

from typing import Any

from pytest import mark

from stjames.atomium_stjames.mmcif import _filter_struct_conn_records, make_connections, mmcif_string_to_mmcif_dict
from stjames.atomium_stjames.mmcif_writer import _build_atom_site_block, pdb_object_to_mmcif_filestring
from stjames.pdb import PDB, PDBAtom, PDBDescription, PDBExperiment, PDBModel, PDBNonPolymer, pdb_from_mmcif_filestring


def _sugar_atom(serial: int, residue: str, insertion: str = "?", alt: str = ".") -> dict[str, Any]:
    return {
        "id": str(serial),
        "label_asym_id": "D",
        "label_comp_id": "NAG",
        "label_seq_id": ".",
        "label_atom_id": "C1",
        "auth_asym_id": "A",
        "auth_seq_id": residue,
        "pdbx_PDB_ins_code": insertion,
        "label_alt_id": alt,
    }


def _sugar_connection(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    connection = {"conn_type_id": "covale"}
    for partner, atom in enumerate((first, second), start=1):
        for field in ("label_asym_id", "label_comp_id", "label_seq_id", "label_atom_id", "auth_asym_id", "auth_seq_id"):
            connection[f"ptnr{partner}_{field}"] = atom[field]
        connection[f"pdbx_ptnr{partner}_PDB_ins_code"] = atom["pdbx_PDB_ins_code"]
        connection[f"pdbx_ptnr{partner}_label_alt_id"] = atom["label_alt_id"]
    return connection


@mark.parametrize("residue,insertion", [("2", "?"), ("1", "A")])
def test_repeated_sugars_resolve_by_author_residue(residue: str, insertion: str) -> None:
    """Resolve identical label addresses using author numbering and insertion codes."""
    atoms = [_sugar_atom(22001, "1"), _sugar_atom(22015, residue, insertion)]
    connection = _sugar_connection(*atoms)
    connection["ptnr1_label_seq_id"] = "?"
    assert make_connections(atoms, [connection]) == [[22001, 22015]]


@mark.parametrize("alt,expected", [("A", [[1, 3]]), ("B", [[2, 3]]), ("?", [])])
def test_alt_locations_remain_unambiguous(alt: str, expected: list[list[int]]) -> None:
    atoms = [_sugar_atom(1, "1", alt="A"), _sugar_atom(2, "1", alt="B"), _sugar_atom(3, "2")]
    connection = _sugar_connection(atoms[0], atoms[2])
    connection["pdbx_ptnr1_label_alt_id"] = alt
    assert make_connections(atoms, [connection]) == expected


@mark.parametrize("kind,symmetry,expected", [("covale", "1_555", True), ("disulf", "?", True), ("hydrog", "1_555", False), ("covale", "2_555", False)])
def test_connection_filter(kind: str, symmetry: str, expected: bool) -> None:
    connection = {"conn_type_id": kind, "ptnr1_symmetry": symmetry, "ptnr2_symmetry": "1_555"}
    assert bool(_filter_struct_conn_records({"struct_conn": [connection]})) is expected


def _ensemble(second_serials: tuple[int, int, int], second_bond: list[int]) -> PDB:
    models = []
    for serials, bond in (((1, 2, 3), [1, 2]), (second_serials, second_bond)):
        atoms = {serial: PDBAtom(x=0, y=0, z=0, element="C", name=f"C{index}") for index, serial in enumerate(serials, start=1)}
        models.append(PDBModel(non_polymer={"A.1": PDBNonPolymer(name="LIG", internal_id="B", polymer="A", atoms=atoms)}, connections=[bond]))
    return PDB(description=PDBDescription(), experiment=PDBExperiment(), geometry={}, models=models)


@mark.parametrize("serials,bond,count", [((11, 12, 13), [12, 11], 1), ((3, 1, 2), [1, 2], 2)])
def test_ensemble_deduplicates_atom_identities(serials: tuple[int, int, int], bond: list[int], count: int) -> None:
    """Serial reuse must not lose bonds, and renumbering must not duplicate them."""
    pdb = _ensemble(serials, bond)
    mmcif = pdb_object_to_mmcif_filestring(pdb)
    assert len(mmcif_string_to_mmcif_dict(mmcif)["struct_conn"]) == count
    restored = pdb_from_mmcif_filestring(mmcif)
    expected = {frozenset(("C1", "C2"))}
    if count == 2:
        expected.add(frozenset(("C2", "C3")))
    for model in restored.models:
        atoms = model.non_polymer["A.1"].atoms
        assert {frozenset(atoms[serial].name for serial in pair) for pair in model.connections} == expected


def test_atom_site_retains_only_connected_identities() -> None:
    pdb = _ensemble((11, 12, 13), [11, 12])
    _, partners = _build_atom_site_block(pdb, {"B": "1"})
    assert set(partners) == {(1, 1), (1, 2), (2, 11), (2, 12)}
    for model in pdb.models:
        model.connections = []
    _, partners = _build_atom_site_block(pdb, {"B": "1"})
    assert not partners
