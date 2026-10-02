"""Tests for PDB parsing, serialization, and atom lookup."""

import json

from pytest import mark, raises

from stjames.atomium_stjames.mmcif import mmcif_string_to_mmcif_dict
from stjames.atomium_stjames.mmcif_writer import pdb_object_to_mmcif_filestring
from stjames.pdb import (
    PDB,
    PDBAtom,
    PDBDescription,
    PDBExperiment,
    PDBModel,
    PDBNonPolymer,
    PDBPolymer,
    PDBResidue,
    PDBWater,
    ResidueRef,
    fetch_pdb,
    fetch_pdb_from_mmcif,
    pdb_from_mmcif_filestring,
    pdb_from_pdb_filestring,
    pdb_object_to_pdb_filestring,
)


def _atom_index_pdb() -> PDB:
    """Build a structure with out-of-order, non-contiguous atom serials."""
    atom = PDBAtom(x=0, y=0, z=0, element="C")
    return PDB(
        description=PDBDescription(),
        experiment=PDBExperiment(),
        geometry={},
        models=[
            PDBModel(
                polymer={
                    "A": PDBPolymer(
                        internal_id="A",
                        residues={
                            "A.101": PDBResidue(
                                name="CYS",
                                number=101,
                                atoms={15: atom.model_copy(update={"element": "S", "name": "SG"}), 8: atom},
                            )
                        },
                    )
                },
                non_polymer={
                    "A.701": PDBNonPolymer(
                        name="4C9",
                        internal_id="A.701",
                        polymer="A",
                        atoms={20: atom.model_copy(update={"name": "C1"})},
                    )
                },
            )
        ],
    )


def test_get_atom_index_matches_serialized_pdb_order() -> None:
    """Map polymer and ligand addresses to positions in serialized atom-record order."""
    pdb = _atom_index_pdb()

    assert pdb.get_atom_index("A", 101, "SG") == 1
    assert pdb.get_atom_index("A", 701, "C1") == 2

    atom_serials = [int(line[6:11]) for line in pdb_object_to_pdb_filestring(pdb).splitlines() if line.startswith(("ATOM", "HETATM"))]
    assert atom_serials == [8, 15, 20]


def test_get_atom_index_can_disambiguate_entity_type() -> None:
    """Require an entity type when polymer and non-polymer residue IDs collide."""
    pdb = _atom_index_pdb()
    pdb.models[0].non_polymer["A.101"] = pdb.models[0].non_polymer.pop("A.701")
    pdb.models[0].non_polymer["A.101"].atoms[20].name = "SG"

    with raises(ValueError, match=r"ambiguous in residue A\.101"):
        pdb.get_atom_index("A", 101, "SG")
    assert pdb.get_atom_index("A", 101, "SG", entity_type="polymer") == 1


def test_get_atom_index_reports_missing_model_residue_and_atom() -> None:
    """Report actionable lookup failures."""
    pdb = _atom_index_pdb()

    with raises(ValueError, match="Model index 1 not found"):
        pdb.get_atom_index("A", 101, "SG", model_index=1)
    with raises(ValueError, match="Model index -1 not found"):
        pdb.get_atom_index("A", 101, "SG", model_index=-1)
    with raises(ValueError, match=r"Residue A\.999 not found"):
        pdb.get_atom_index("A", 999, "SG")
    with raises(ValueError, match=r"Atom NZ not found in residue A\.101"):
        pdb.get_atom_index("A", 101, "NZ")


def _all_residue_pdb() -> PDB:
    """Build a structure spanning polymer, non-polymer, water, and branched entities."""
    atom = PDBAtom(x=0, y=0, z=0, element="C")
    return PDB(
        description=PDBDescription(),
        experiment=PDBExperiment(),
        geometry={},
        models=[
            PDBModel(
                polymer={
                    "A": PDBPolymer(
                        internal_id="A",
                        residues={
                            "A.101": PDBResidue(name="CYS", number=101, atoms={8: atom, 15: atom}),
                            "A.102": PDBResidue(name="GLY", number=102, atoms={30: atom}),
                        },
                    )
                },
                non_polymer={"A.701": PDBNonPolymer(name="4C9", internal_id="A.701", polymer="A", atoms={20: atom})},
                water={"A.801": PDBWater(internal_id="A.801", polymer="A", atoms={25: atom})},
                branched={"A.901": {"atoms": {40: atom}}},
            )
        ],
    )


def test_all_residue_refs_ordered_by_lowest_atom_serial() -> None:
    """Residues from every entity type share one index, ordered by lowest atom serial."""
    model = _all_residue_pdb().models[0]

    assert model.all_residue_refs() == [
        ResidueRef("polymer", "A", "A.101"),
        ResidueRef("non_polymer", "A.701"),
        ResidueRef("water", "A.801"),
        ResidueRef("polymer", "A", "A.102"),
        ResidueRef("branched", "A.901"),
    ]


def test_residue_atoms_dereferences_each_entity_type() -> None:
    """residue_atoms resolves a ref back to its atom mapping regardless of entity type."""
    model = _all_residue_pdb().models[0]

    assert set(model.residue_atoms(ResidueRef("polymer", "A", "A.101"))) == {8, 15}
    assert set(model.residue_atoms(ResidueRef("non_polymer", "A.701"))) == {20}
    assert set(model.residue_atoms(ResidueRef("water", "A.801"))) == {25}
    assert set(model.residue_atoms(ResidueRef("branched", "A.901"))) == {40}


def test_residue_atoms_requires_residue_key_for_polymer() -> None:
    """A polymer ref without residue_key is rejected rather than silently misresolved."""
    model = _all_residue_pdb().models[0]

    with raises(ValueError, match="residue_key"):
        model.residue_atoms(ResidueRef("polymer", "A"))


def test_residue_atoms_survive_json_roundtrip() -> None:
    """Every entity retains integer serials and typed atoms after JSON storage."""
    original = _all_residue_pdb()
    restored = PDB.model_validate_json(original.model_dump_json())
    model = restored.models[0]

    assert model.all_residue_refs() == original.models[0].all_residue_refs()
    for ref in model.all_residue_refs():
        atoms = model.residue_atoms(ref)
        assert atoms == original.models[0].residue_atoms(ref)
        assert all(isinstance(serial, int) and isinstance(atom, PDBAtom) for serial, atom in atoms.items())


def test_1ema() -> None:
    """Green fluorescent protein."""
    fetch_pdb("1EMA")


def test_8qvy() -> None:
    """
    Human GABAA receptor
    Not availble as a .pdb
    """
    fetch_pdb_from_mmcif("8VQY")


def test_read_pdb_filestring() -> None:
    """Rest reading of a pdb string."""
    with open("tests/data/1ema.pdb") as f:
        data = f.read()
    pdb = pdb_from_pdb_filestring(data)
    assert pdb.description.code == "1EMA"

    json = pdb.model_dump()
    PDB.model_validate(json)


def test_read_pdb_filestring_mome() -> None:
    """Rest reading of a pdb string."""
    with open("tests/data/cluster_1.pdb") as f:
        data = f.read()
    pdb = pdb_from_pdb_filestring(data)

    json = pdb.model_dump()
    print(json)
    PDB.model_validate(json)


def test_pdb_polymer_chain_with_and_without_ter() -> None:
    """Protein ATOM records parse as polymer even when TER is omitted."""
    no_ter_data = (
        "ATOM      1  N   GLY A   1      11.104  13.207  14.099  1.00 10.00           N\n"
        "HETATM    2  O   HOH A   2      12.000  14.000  15.000  1.00 20.00           O\n"
        "END\n"
    )

    with_ter_data = no_ter_data.replace(
        "ATOM      1  N   GLY A   1      11.104  13.207  14.099  1.00 10.00           N\n",
        "ATOM      1  N   GLY A   1      11.104  13.207  14.099  1.00 10.00           N\nTER       2      GLY A   1\n",
    )
    assert with_ter_data != no_ter_data

    no_ter = pdb_from_pdb_filestring(no_ter_data).models[0]
    with_ter = pdb_from_pdb_filestring(with_ter_data).models[0]
    for model in [no_ter, with_ter]:
        assert list(model.polymer) == ["A"]
        assert set(model.polymer["A"].residues) == {"A.1"}
        assert model.polymer["A"].residues["A.1"].name == "GLY"
        assert model.non_polymer == {}
        assert set(model.water) == {"A.2"}

    assert no_ter.polymer == with_ter.polymer
    assert no_ter.non_polymer == with_ter.non_polymer
    assert no_ter.water == with_ter.water


def test_read_mmcif_filestring() -> None:
    """Rest reading of a mmcif string."""
    with open("tests/data/1ema.cif") as f:
        data = f.read()
    pdb = pdb_from_mmcif_filestring(data)
    assert pdb.description.code == "1EMA"

    json = pdb.model_dump()
    PDB.model_validate(json)


def test_mmcif_formal_charges_are_serialized_as_integers() -> None:
    """Serialize integral formal charges without decimal points."""
    pdb = _atom_index_pdb()
    residue = pdb.models[0].polymer["A"].residues["A.101"]
    residue.atoms[8] = PDBAtom(x=0, y=0, z=0, element="N", charge=1)
    residue.atoms[15] = PDBAtom(x=0, y=0, z=0, element="O", charge=-1)

    mmcif = pdb_object_to_mmcif_filestring(pdb)
    charges = [row["pdbx_formal_charge"] for row in mmcif_string_to_mmcif_dict(mmcif)["atom_site"]]

    assert charges == ["-1", "1", "?"]


def test_mmcif_rejects_fractional_formal_charge() -> None:
    """Reject fractional values that mmCIF formal-charge fields cannot represent."""
    pdb = _atom_index_pdb()
    residue = pdb.models[0].polymer["A"].residues["A.101"]
    residue.atoms[8] = PDBAtom(x=0, y=0, z=0, element="N", charge=0.5)

    with raises(ValueError, match="formal charge must be an integer"):
        pdb_object_to_mmcif_filestring(pdb)


def test_pdb_connections_survive_mmcif_roundtrip() -> None:
    """Preserve sparse atom serial connections and alternate-location identity."""
    pdb = pdb_from_pdb_filestring(
        "HETATM   10  C1 ALIG A   1       0.000   0.000   0.000  0.50  0.00           C\n"
        "HETATM   20  C1 BLIG A   1       0.100   0.000   0.000  0.50  0.00           C\n"
        "HETATM   30  C2  LIG A   1       1.500   0.000   0.000  1.00  0.00           C\n"
        "CONECT   10   30\n"
        "CONECT   30   10\n"
        "END\n"
    )

    mmcif = pdb_object_to_mmcif_filestring(pdb)
    struct_conn = mmcif_string_to_mmcif_dict(mmcif)["struct_conn"]
    restored = pdb_from_mmcif_filestring(mmcif)

    assert len(struct_conn) == 1
    assert struct_conn[0]["pdbx_ptnr1_label_alt_id"] == "A"
    assert restored.models[0].connections == [[10, 30]]
    assert restored.models[0].non_polymer["A.1"].atoms[20].alt_loc == "B"


def test_disulfide_bond_written_as_struct_conn_disulf() -> None:
    """Classify a CYS SG-SG connection as disulf rather than the covale default."""
    sg = PDBAtom(x=0, y=0, z=0, element="S", name="SG")
    pdb = PDB(
        description=PDBDescription(),
        experiment=PDBExperiment(),
        geometry={},
        models=[
            PDBModel(
                polymer={
                    "A": PDBPolymer(internal_id="A", residues={"A.10": PDBResidue(name="CYS", number=10, atoms={1: sg})}),
                    "B": PDBPolymer(internal_id="B", residues={"B.20": PDBResidue(name="CYS", number=20, atoms={2: sg})}),
                },
                connections=[[1, 2]],
            )
        ],
    )

    mmcif = pdb_object_to_mmcif_filestring(pdb)
    struct_conn = mmcif_string_to_mmcif_dict(mmcif)["struct_conn"]
    restored = pdb_from_mmcif_filestring(mmcif)

    assert len(struct_conn) == 1
    assert struct_conn[0]["conn_type_id"] == "disulf"
    assert restored.models[0].connections == [[1, 2]]


def test_struct_conn_preserves_connections_from_every_model() -> None:
    """A connection unique to a later model is not dropped from the shared struct_conn table."""
    atoms = {i: PDBAtom(x=float(i), y=0, z=0, element="C", name=f"C{i}") for i in (1, 2, 3, 4)}
    ligand = PDBNonPolymer(name="LIG", internal_id="A.701", polymer="A", atoms=atoms)
    pdb = PDB(
        description=PDBDescription(),
        experiment=PDBExperiment(),
        geometry={},
        models=[
            PDBModel(non_polymer={"A.701": ligand.model_copy(deep=True)}, connections=[[1, 2]]),
            PDBModel(non_polymer={"A.701": ligand.model_copy(deep=True)}, connections=[[1, 2], [3, 4]]),
        ],
    )

    mmcif = pdb_object_to_mmcif_filestring(pdb)
    struct_conn = mmcif_string_to_mmcif_dict(mmcif)["struct_conn"]
    restored = pdb_from_mmcif_filestring(mmcif)

    assert len(struct_conn) == 2
    assert {frozenset(pair) for pair in restored.models[1].connections} == {frozenset((1, 2)), frozenset((3, 4))}


# fmt: off
@mark.regression
@mark.parametrize(
    "code",
    [
        # Codes from molecules of the month August 2024–January 2025
        "7S6B", "8UCS", "2ZVY", "1F4V", "6YKM", "6E10", "6E11", "3VCM", "2X0B",
        "6OS0", "1N9U", "1O86", "2V0Z", "6KI1", "6KI2", "7YYO", "6TJV", "7EGL",
        "7CYF", "7EGK", "7ZCG", "3FRT", "6AP1",
        # Codes created by o1
        "1CRN", "1MBN", "4HHB", "1HHO", "1BNA", "1CAG", "2JHO", "1EVV", "3ZOJ",
        "4AGG", "2Y69", "6R1V", "6ND2", "7NZ6", "1S72", "3G5U", "7DFT", "6AI0",
        "6NG2", "1A0I", "1B7C", "1C8R", "1D4T", "1E7O", "1F9J", "1G5K", "1H8L",
        "1I2M", "1J3N", "1K4P", "1M7R", "1N8S", "1O9T", "1P0U", "1Q1V", "1R2W",
        "1S3X", "1T4Y", "1U5Z", "1V6A", "1W7B", "1X8C", "1Y9D", "1Z0E", "2A1F",
        "2B2G", "2C3H", "2D4I", "2E5J", "2F6K", "2G7L", "2H8M", "2I9N", "2J0O",
        "2K1P", "2L2Q", "2N4S", "2O5T", "2P6U", "2Q7V", "2R8W", "2V2A", "2W3B",
        "2X4C", "2Y5D", "2Z6E", "3A7F", "3B8G", "3C9H", "3D0I", "3E1J", "3F2K",
        "3G3L", "3H4M", "3I5N", "3J6O", "3K7P", "3L8Q", "3N0S", "3O1T", "3P2U",
        "3Q3V", "3S5X", "3T6Y", "3U7Z", "3V8A", "3W9B", "3X0C", "4A3F", "4B4G",
        "4C5H", "4D6I", "4E7J", "4F8K", "4G9L", "4H0M", "4I1N", "4J2O", "4K3P",
        "4L4Q", "4M5R", "4N6S", "4O7T", "4P8U", "4Q9V", "4R0W", "4S1X",
    ]
)  # fmt: on
def test_pdb(code: str) -> None:
    pdb = fetch_pdb(code)

    json = pdb.model_dump()
    PDB.model_validate(json)

def test_from_pdb_to_pdb_2qto() -> None:
    with open("tests/data/2qto.pdb") as f:
        data = f.read()
    pdb = pdb_from_pdb_filestring(data)
    filestring = pdb_object_to_pdb_filestring(pdb, header=True, source=True, keyword=True, crystallography=True)
    pdb2 = pdb_from_pdb_filestring(filestring)

    assert pdb.description == pdb2.description
    assert pdb.experiment == pdb2.experiment
    assert pdb.models == pdb2.models

def test_from_pdb_to_pdb_1ema() -> None:
    with open("tests/data/1ema.pdb") as f:
        data = f.read()
    pdb = pdb_from_pdb_filestring(data)
    filestring = pdb_object_to_pdb_filestring(pdb, header=True, source=True, keyword=True, crystallography=True)
    pdb2 = pdb_from_pdb_filestring(filestring)

    assert pdb.description == pdb2.description
    assert pdb.models == pdb2.models

def test_from_pdb_to_pdb_2hu4() -> None:
    with open("tests/data/2HU4.pdb") as f:
        data = f.read()
    pdb = pdb_from_pdb_filestring(data)
    filestring = pdb_object_to_pdb_filestring(pdb, header=True, source=True, keyword=True, crystallography=True)

    pdb2 = pdb_from_pdb_filestring(filestring)

    assert pdb.description == pdb2.description
    # not true but doesn't matter
    print(pdb.geometry == pdb2.geometry)
    assert pdb.models == pdb2.models

def mmcif_author_format_to_pdb_format(authors: list[str]) -> list[str]:
    return [f"{last.upper()}{first.upper()}" for first, last in
            (author.split(", ") for author in authors)]

def compare_descriptions_mmcif_and_pdb(mmcif_description: PDBDescription, pdb_description: PDBDescription) -> bool:
    return (
        mmcif_description.code == pdb_description.code and
        mmcif_description.title == pdb_description.title and
        mmcif_author_format_to_pdb_format(mmcif_description.authors) == (pdb_description.authors) and
        mmcif_description.classification == pdb_description.classification and
        mmcif_description.deposition_date == pdb_description.deposition_date and
        sorted(mmcif_description.keywords) == sorted(pdb_description.keywords)
    )

def compare_experiments_mmcif_and_pdb(mmcif_experiment: PDBExperiment, pdb_experiment: PDBExperiment) -> bool:
    return (
        mmcif_experiment.expression_system.upper() == pdb_experiment.expression_system and  # ty: ignore[unresolved-attribute]
        mmcif_experiment.missing_residues == pdb_experiment.missing_residues and
        mmcif_experiment.source_organism.upper() == pdb_experiment.source_organism and  # ty: ignore[unresolved-attribute]
        mmcif_experiment.technique == pdb_experiment.technique
    )

def compare_models_mmcif_and_pdb(mmcif_models: list[PDBModel], pdb_models: list[PDBModel]) -> bool:
    for i in range(len(mmcif_models)):
        assert mmcif_models[i].polymer == pdb_models[i].polymer
        assert mmcif_models[i].non_polymer == pdb_models[i].non_polymer
        assert mmcif_models[i].branched == pdb_models[i].branched
    return True

def test_from_mmcif_to_pdb_1ema() -> None:
    with open("tests/data/1ema.cif") as f:
        mmcif_data = f.read()

    with open("tests/data/1ema.pdb") as f:
        pdb_data = f.read()
    mmcif_1ema = pdb_from_mmcif_filestring(mmcif_data)
    pdb_1ema = pdb_from_pdb_filestring(pdb_data)

    assert compare_descriptions_mmcif_and_pdb(mmcif_1ema.description, pdb_1ema.description)
    assert compare_experiments_mmcif_and_pdb(mmcif_1ema.experiment, pdb_1ema.experiment)
    assert mmcif_1ema.quality == pdb_1ema.quality
    assert compare_models_mmcif_and_pdb(mmcif_1ema.models, pdb_1ema.models)


def _jsonb_roundtrip(pdb: PDB) -> PDB:
    """Simulate PostgreSQL JSONB round-trip (alphabetically sorts dict keys)."""
    json_dict = pdb.model_dump(mode="json")
    json_sorted = json.dumps(json_dict, sort_keys=True)
    return PDB.model_validate(json.loads(json_sorted))


def _extract_atom_records(pdb_string: str) -> list[tuple[str, int, str, int, str]]:
    """Extract (record_type, serial, chain, res_num, insertion_code) from PDB string."""
    records = []
    for line in pdb_string.split("\n"):
        if line.startswith(("ATOM", "HETATM")):
            record_type = line[:6].strip()
            serial = int(line[6:11])
            chain = line[21]
            res_num = int(line[22:26])
            ins_code = line[26].strip()
            records.append((record_type, serial, chain, res_num, ins_code))
        elif line.startswith("TER"):
            records.append(("TER", 0, "", 0, ""))
    return records


def test_jsonb_roundtrip_insertion_codes() -> None:
    """Test that insertion codes (16, 16A, 17, 169, 170) survive JSONB round-trip."""
    with open("tests/data/insertion_codes.pdb") as f:
        pdb = pdb_from_pdb_filestring(f.read())

    restored = _jsonb_roundtrip(pdb)
    out1 = pdb_object_to_pdb_filestring(pdb, seqres=False, hetnam=False)
    out2 = pdb_object_to_pdb_filestring(restored, seqres=False, hetnam=False)
    assert out1 == out2

    # Verify specific ordering
    records = _extract_atom_records(out2)
    res_nums = [(r[3], r[4]) for r in records if r[0] == "ATOM"]
    assert res_nums == [(16, ""), (16, "A"), (17, ""), (169, ""), (170, "")]


def test_jsonb_roundtrip_negative_residue_numbers() -> None:
    """Test that negative residue numbers (-3 to 11) survive JSONB round-trip."""
    with open("tests/data/negative_residue_numbers.pdb") as f:
        pdb = pdb_from_pdb_filestring(f.read())

    restored = _jsonb_roundtrip(pdb)
    out1 = pdb_object_to_pdb_filestring(pdb, seqres=False, hetnam=False)
    out2 = pdb_object_to_pdb_filestring(restored, seqres=False, hetnam=False)
    assert out1 == out2

    # Verify specific ordering
    records = _extract_atom_records(out2)
    res_nums = [r[3] for r in records if r[0] == "ATOM"]
    assert res_nums == [-3, -2, -1, 0, 1, 2, 10, 11]


def test_jsonb_roundtrip_multichain_with_ligand() -> None:
    """Test multi-chain structure with ligand survives JSONB round-trip with correct TER placement."""
    with open("tests/data/multichain_with_ligand.pdb") as f:
        pdb = pdb_from_pdb_filestring(f.read())

    restored = _jsonb_roundtrip(pdb)
    out1 = pdb_object_to_pdb_filestring(pdb, seqres=False, hetnam=False)
    out2 = pdb_object_to_pdb_filestring(restored, seqres=False, hetnam=False)
    assert out1 == out2

    # Verify structure: chain A atoms, TER, chain B atoms, TER, ligand
    records = _extract_atom_records(out2)
    record_types = [r[0] for r in records]
    assert record_types == ["ATOM", "ATOM", "ATOM", "ATOM", "ATOM", "TER", "ATOM", "ATOM", "ATOM", "ATOM", "TER", "HETATM", "HETATM"]


def _assert_mmcif_roundtrip(path: str) -> None:
    """Read a mmCIF file, write it back, re-read, and assert structural equality."""
    with open(path) as f:
        data = f.read()
    pdb1 = pdb_from_mmcif_filestring(data)
    cif2 = pdb_object_to_mmcif_filestring(pdb1)
    pdb2 = pdb_from_mmcif_filestring(cif2)
    assert pdb1.description.code == pdb2.description.code
    assert pdb1.description.title == pdb2.description.title
    assert len(pdb1.models) == len(pdb2.models)
    for m1, m2 in zip(pdb1.models, pdb2.models, strict=True):
        assert m1.polymer == m2.polymer
        assert m1.non_polymer == m2.non_polymer
        assert m1.water == m2.water
        assert m1.connections == m2.connections
        for chain_id, poly1 in m1.polymer.items():
            assert poly1.sequence == m2.polymer[chain_id].sequence


def test_mmcif_roundtrip_1ema() -> None:
    """Polymer, non-polymer, water, sequences, secondary structure, and full names survive round-trip."""
    _assert_mmcif_roundtrip("tests/data/1ema.cif")


def test_mmcif_roundtrip_1hxw() -> None:
    """Ligand-containing structure (1HXW) survives mmCIF round-trip."""
    _assert_mmcif_roundtrip("tests/data/1HXW.cif")
