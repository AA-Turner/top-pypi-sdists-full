"""Blank author chains remain valid across mmCIF tables and models."""

from pytest import mark

from stjames.atomium_stjames.mmcif import mmcif_string_to_mmcif_dict
from stjames.atomium_stjames.mmcif_writer import _assign_missing_asym_ids
from stjames.pdb import pdb_from_mmcif_filestring, pdb_from_pdb_filestring, pdb_object_to_mmcif_filestring


@mark.parametrize(
    "record",
    [
        "ATOM      1  CA  ALA     1       0.000   0.000   0.000  1.00  0.00           C",
        "HETATM    1  C1  LIG     1       0.000   0.000   0.000  1.00  0.00           C",
        "HETATM    1  O   HOH     1       0.000   0.000   0.000  1.00  0.00           O",
    ],
)
def test_blank_chains_across_models(record: str) -> None:
    pdb = pdb_from_pdb_filestring(f"{record}\nEND\n")
    second = pdb.models[0].model_copy(deep=True)
    second._atom_records()[0].atom.x = 1.0
    pdb.models.append(second)
    original = pdb.model_dump()

    mmcif = pdb_object_to_mmcif_filestring(pdb)
    tables = mmcif_string_to_mmcif_dict(mmcif)
    rows = tables["atom_site"]
    assert len(rows) == 2
    assert rows[0]["label_asym_id"] == rows[1]["label_asym_id"]
    assert rows[0]["label_asym_id"].strip()
    assert {row["auth_asym_id"] for row in rows} == {" "}
    assert rows[0]["label_asym_id"] in {row["id"] for row in tables["struct_asym"]}
    restored = pdb_from_mmcif_filestring(mmcif)
    assert [model._atom_records()[0].atom.x for model in restored.models] == [0.0, 1.0]
    assert pdb.model_dump() == original


@mark.parametrize("annotation,table", [("helices", "struct_conf"), ("strands", "struct_sheet_range")])
@mark.parametrize("author_id", ["", " "])
def test_blank_annotations_and_connections(annotation: str, table: str, author_id: str) -> None:
    pdb = pdb_from_pdb_filestring(
        "ATOM      1  SG  CYS     1       0.000   0.000   0.000  1.00  0.00           S\n"
        "ATOM      2  SG  CYS     2       2.000   0.000   0.000  1.00  0.00           S\nEND\n"
    )
    model = pdb.models[0]
    polymer = model.polymer.pop(" ")
    model.polymer[author_id] = polymer
    setattr(polymer, annotation, [[f"{author_id}.1", f"{author_id}.2"]])
    model.connections = [[1, 2]]
    original = pdb.model_dump()
    mmcif = pdb_object_to_mmcif_filestring(pdb)
    tables = mmcif_string_to_mmcif_dict(mmcif)
    for endpoint in ("beg", "end"):
        assert tables[table][0][f"{endpoint}_auth_asym_id"] == author_id
    for partner in (1, 2):
        assert tables["struct_conn"][0][f"ptnr{partner}_auth_asym_id"] == author_id
        assert tables["struct_conn"][0][f"ptnr{partner}_label_asym_id"] == tables["atom_site"][0]["label_asym_id"]
    assert pdb_from_mmcif_filestring(mmcif).models[0].connections == [[1, 2]]
    assert pdb.model_dump() == original


@mark.parametrize("kind", ["polymer", "non_polymer", "water"])
@mark.parametrize("missing_id", ["", " "])
@mark.parametrize("missing_model", [0, 1])
def test_missing_labels_reuse_existing_ids_across_models(kind: str, missing_id: str, missing_model: int) -> None:
    """Preserve shared atom and connection identities when one model lacks labels."""
    pdb = pdb_from_pdb_filestring(
        "ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C\n"
        "HETATM    2  C1  LIG A   2       0.000   0.000   0.000  1.00  0.00           C\n"
        "HETATM    3  O   HOH A   3       0.000   0.000   0.000  1.00  0.00           O\nEND\n"
    )
    pdb.models.append(pdb.models[0].model_copy(deep=True))
    for model in pdb.models:
        model.connections = [[1, 2]]
    existing = next(iter(getattr(pdb.models[1 - missing_model], kind).values()))
    existing.internal_id = "EXISTING"
    next(iter(getattr(pdb.models[missing_model], kind).values())).internal_id = missing_id
    original = pdb.model_dump()

    mmcif = pdb_object_to_mmcif_filestring(pdb)
    tables = mmcif_string_to_mmcif_dict(mmcif)
    serial = {"polymer": "1", "non_polymer": "2", "water": "3"}[kind]
    rows = [row for row in tables["atom_site"] if row["id"] == serial]
    assert len(rows) == 2
    assert {row["label_asym_id"] for row in rows} == {"EXISTING"}
    assert all(row["label_entity_id"] != "?" for row in rows)
    restored = pdb_from_mmcif_filestring(mmcif)
    assert len(restored.models) == 2
    assert [model.connections for model in restored.models] == [[[1, 2]], [[1, 2]]]
    assert pdb.model_dump() == original


def test_generated_labels_avoid_collisions_and_share_atoms() -> None:
    pdb = pdb_from_pdb_filestring(
        "ATOM      1  CA  ALA     1       0.000   0.000   0.000  1.00  0.00           C\n"
        "HETATM    2  C1  LIG     2       0.000   0.000   0.000  1.00  0.00           C\n"
        "HETATM    3  O   HOH     3       0.000   0.000   0.000  1.00  0.00           O\nEND\n"
    )
    # Reserve an ID in a later model, and normalize all supported blank forms.
    model = pdb.models[0]
    next(iter(model.polymer.values())).internal_id = ""
    next(iter(model.non_polymer.values())).internal_id = " "
    next(iter(model.water.values())).internal_id = None
    second = model.model_copy(deep=True)
    water = next(iter(second.water.values())).model_copy(update={"internal_id": "STJAMESASYM1"})
    second.water["B.4"] = water
    pdb.models.append(second)
    original = pdb.model_dump()
    normalized = _assign_missing_asym_ids(pdb)
    ids = [
        entity.internal_id
        for collection in (normalized.models[0].polymer, normalized.models[0].non_polymer, normalized.models[0].water)
        for entity in collection.values()
    ]
    assert len(set(ids)) == 3
    assert "STJAMESASYM1" not in ids
    for first, second in zip(normalized.models[0]._atom_records(), model._atom_records(), strict=True):
        assert first.atom is second.atom
    assert pdb.model_dump() == original
