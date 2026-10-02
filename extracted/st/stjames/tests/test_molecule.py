from functools import partial
from pathlib import Path

import pytest
from pydantic import ValidationError
from pytest import raises

pytest.importorskip("rdkit")
from rdkit import Chem
from rdkit.Geometry import Point3D

from stjames import Atom, Molecule

DATA = Path(__file__).parent / "data"


def test_molecule_pbc() -> None:
    # this is a funny joke, because it makes manganese
    glomar_explorer = partial(Molecule, charge=0, multiplicity=2, atoms=[Atom(atomic_number=25, position=(0, 0, 0))])

    mol_nopbc = glomar_explorer()
    assert mol_nopbc.cell is None

    valid_input = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    mol = glomar_explorer(cell={"lattice_vectors": valid_input})
    assert mol.cell is not None
    assert mol.cell.lattice_vectors == valid_input

    mol2 = glomar_explorer(cell={"lattice_vectors": valid_input, "is_periodic": (True, False, True)})
    assert mol2.cell is not None
    assert mol2.cell.lattice_vectors == valid_input
    assert mol2.cell.is_periodic == (True, False, True)

    with raises(ValidationError):
        glomar_explorer(cell={"lattice_vectors": valid_input, "is_periodic": (False, False, False)})

    invalid_input = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0))
    with raises(ValidationError):
        glomar_explorer(cell={"lattice_vectors": invalid_input})

    invalid_input2 = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, "invalid"))
    with raises(ValidationError):
        glomar_explorer(cell={"lattice_vectors": invalid_input2})

    invalid_input3 = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 1.0))
    with raises(ValidationError):
        glomar_explorer(cell={"lattice_vectors": invalid_input3})


def test_xyz() -> None:
    mol = Molecule.from_xyz_lines(
        """3
H2O Molecule; smiles: O; nonsense: data: more nonsense
O        0.000000     0.000000     0.000000
H        0.000000    -0.757000     0.587000
H        0.000000     0.757000     0.587000
""".splitlines()
    )
    assert mol.smiles == "O"
    assert getattr(mol, "nonsense", None) is None

    mol = Molecule.from_xyz_lines(
        """3
name: H2O Molecule; smiles: O
O        0.000000     0.000000     0.000000
H        0.000000    -0.757000     0.587000
H        0.000000     0.757000     0.587000
""".splitlines()
    )

    assert mol.name == "H2O Molecule"
    assert Molecule.from_xyz(mol.to_xyz()).name == "H2O Molecule"

    mol = Molecule.from_xyz_lines(
        """3
cell: [(1, 2, 3), [4, 5, 6e-1], (7.0, 8.0, 9.0)]; smiles: O; is_periodic: [True, False, True]
O        0.000000     0.000000     0.000000
H        0.000000    -0.757000     0.587000
H        0.000000     0.757000     0.587000
""".splitlines()
    )

    assert mol.cell is not None
    assert mol.cell.lattice_vectors == ((1.0, 2.0, 3.0), (4.0, 5.0, 0.6), (7.0, 8.0, 9.0))
    assert mol.cell.is_periodic == (True, False, True)
    assert mol.smiles == "O"

    mol = Molecule.from_xyz_lines(
        """3
cell: [(a, b, c), [4, 5, 6e-1], (7.0, 8.0, 9.0)]; smiles: O; is_periodic: [True, False, True]
O        0.000000     0.000000     0.000000
H        0.000000    -0.757000     0.587000
H        0.000000     0.757000     0.587000
""".splitlines()
    )

    assert mol.cell is None
    assert mol.smiles == "O"
    assert getattr(mol.cell, "is_periodic", None) is None


def test_from_smiles() -> None:
    mol = Molecule.from_smiles("CCO")

    assert len(mol.atoms) == 9


SDF_TWO_MOLS = """\
benzene
     RDKit          3D

  6  6  0  0  0  0  0  0  0  0999 V2000
    1.2124    0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.2124   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000   -1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2124   -0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.2124    0.7000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    0.0000    1.4000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  2  0
  2  3  1  0
  3  4  2  0
  4  5  1  0
  5  6  2  0
  6  1  1  0
M  END
>  <source>
fixture

>  <score>
1.25

$$$$
water
     RDKit          3D

  3  2  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0
    0.9572    0.0000    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
   -0.2399    0.9267    0.0000 H   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0
  1  3  1  0
M  END
$$$$
"""

MOL2_TWO_MOLS = """\
@<TRIPOS>MOLECULE
benzene
 6 6 0 0 0
SMALL
NO_CHARGES

@<TRIPOS>ATOM
      1 C1          1.2124    0.7000    0.0000 C.ar    1  LIG1        0.0000
      2 C2          1.2124   -0.7000    0.0000 C.ar    1  LIG1        0.0000
      3 C3          0.0000   -1.4000    0.0000 C.ar    1  LIG1        0.0000
      4 C4         -1.2124   -0.7000    0.0000 C.ar    1  LIG1        0.0000
      5 C5         -1.2124    0.7000    0.0000 C.ar    1  LIG1        0.0000
      6 C6          0.0000    1.4000    0.0000 C.ar    1  LIG1        0.0000
@<TRIPOS>BOND
     1     1     2   ar
     2     2     3   ar
     3     3     4   ar
     4     4     5   ar
     5     5     6   ar
     6     6     1   ar
@<TRIPOS>MOLECULE
water
 3 2 0 0 0
SMALL
NO_CHARGES

@<TRIPOS>ATOM
      1 O1          0.0000    0.0000    0.0000 O.3     1  LIG1        0.0000
      2 H1          0.9572    0.0000    0.0000 H       1  LIG1        0.0000
      3 H2         -0.2399    0.9267    0.0000 H       1  LIG1        0.0000
@<TRIPOS>BOND
     1     1     2   1
     2     1     3   1
"""


def test_molecules_from_sdf(tmp_path: Path) -> None:
    sdf_file = tmp_path / "test.sdf"
    sdf_file.write_text(SDF_TWO_MOLS)

    mols = Molecule.molecules_from_sdf(sdf_file)
    assert len(mols) == 2
    assert all(len(m.atoms) > 0 for m in mols)
    assert [m.name for m in mols] == ["benzene", "water"]
    assert mols[0].metadata == {"source": "fixture", "score": 1.25}
    assert mols[1].metadata is None


def test_molecules_from_sdf_preserves_smiles_data_field() -> None:
    """SDF <smiles> data field is preserved verbatim, not overwritten by Chem.MolToSmiles."""
    [mol] = Molecule.molecules_from_sdf(DATA / "deazapurine_with_smiles.sdf")
    assert mol.smiles == "c1ncnc2[nH]ccc12"


def test_from_rdkit_falls_back_to_moltosmiles_when_no_property() -> None:
    """Without a 'smiles' property, from_rdkit caches Chem.MolToSmiles."""
    rdkm = Chem.MolFromSmiles("CCO")
    assert not rdkm.HasProp("smiles")
    cached = Molecule.from_rdkit(rdkm).smiles
    assert cached is not None
    assert Chem.CanonSmiles(cached) == Chem.CanonSmiles("CCO")


def test_from_rdkit_leaves_smiles_unset_without_bond_graph() -> None:
    """Mol with atoms but no bonds (raw XYZ-style) refuses to invent a SMILES."""
    rdkm = Chem.RWMol()
    rdkm.AddAtom(Chem.Atom(6))
    rdkm.AddAtom(Chem.Atom(6))
    conf = Chem.Conformer(2)
    conf.SetAtomPosition(0, Point3D(0.0, 0.0, 0.0))
    conf.SetAtomPosition(1, Point3D(1.5, 0.0, 0.0))
    rdkm.AddConformer(conf)

    assert Molecule.from_rdkit(rdkm).smiles is None


def test_molecules_from_mol2(tmp_path: Path) -> None:
    mol2_file = tmp_path / "test.mol2"
    mol2_file.write_text(MOL2_TWO_MOLS)

    mols = Molecule.molecules_from_mol2(mol2_file)
    assert len(mols) == 2
    assert all(len(m.atoms) > 0 for m in mols)
    assert [m.name for m in mols] == ["benzene", "water"]


def test_from_file_sdf(tmp_path: Path) -> None:
    sdf_file = tmp_path / "test.sdf"
    sdf_file.write_text(SDF_TWO_MOLS)

    mol = Molecule.from_file(sdf_file)
    assert len(mol.atoms) > 0
    assert mol.name == "benzene"
    assert mol.metadata == {"source": "fixture", "score": 1.25}


def test_from_file_mol2(tmp_path: Path) -> None:
    mol2_file = tmp_path / "test.mol2"
    mol2_file.write_text(MOL2_TWO_MOLS)

    mol = Molecule.from_file(mol2_file)
    assert len(mol.atoms) > 0
    assert mol.name == "benzene"
