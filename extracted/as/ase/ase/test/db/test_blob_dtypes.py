"""Test that ase.db only writes arrays that it can read back.

Calculators may produce arrays of unexpected dtypes, for example the
float32 forces written by FAIRChem (issue #1888).  blob() must either
cast such arrays to the dtype that deblob() reads the field with, or
refuse to write them.
"""

import numpy as np
import pytest

from ase import Atoms
from ase.calculators.singlepoint import SinglePointCalculator
from ase.db import connect

pytestmark = pytest.mark.usefixtures('testdir')

db_name = 'dtypes.db'


def atoms_with_forces(dtype):
    """Water molecule with forces of the given dtype."""
    atoms = Atoms(
        'OH2', positions=[[0.0, 0.0, 0.0], [0.95, 0.0, 0.0], [-0.24, 0.92, 0.0]]
    )
    forces = np.arange(3 * len(atoms), dtype=dtype).reshape(-1, 3)
    atoms.calc = SinglePointCalculator(atoms)
    # Assign directly; the constructor would cast to float64:
    atoms.calc.results['forces'] = forces
    return atoms, forces


def write_and_read(atoms):
    with connect(db_name) as db:
        db.write(atoms)
    with connect(db_name) as db:
        return db.get(1)


@pytest.mark.parametrize('dtype', [np.float16, np.float32, np.int64])
def test_forces_dtype_roundtrip(dtype):
    """Forces of castable dtypes must round trip as float64.

    Before blob had a dtype argument, a calculator writing float32 could lead
    to crashes when it is later read as float64 (issue #1888)"""
    atoms, forces = atoms_with_forces(dtype)
    forces_read = write_and_read(atoms).forces
    assert forces_read.dtype == np.float64
    assert forces_read.shape == forces.shape
    assert np.array_equal(forces_read, forces)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
def test_complex_forces_raise(dtype):
    """Complex values cannot be stored in a float field.

    Before validation was added, they were written anyway and read
    back as garbage float64 values without any error."""
    atoms, _ = atoms_with_forces(dtype)
    with connect(db_name) as db:
        with pytest.raises(ValueError, match='Refusing to write.*complex'):
            db.write(atoms)


def test_float_tags_raise():
    """Floats cannot be written to int fields. Test with tags."""
    atoms = Atoms('H2', positions=[[0.0, 0.0, 0.0], [0.0, 0.0, 0.74]])
    atoms.new_array('tags', np.array([0.5, 1.5]))
    with connect(db_name) as db:
        with pytest.raises(ValueError, match='Refusing to write.*float64'):
            db.write(atoms)


def test_int_tags_roundtrip():
    """Integer fields downcast int64 to int32.

    This was the behavior before blob had a dtype argument, and is still the
    expected behavior."""
    atoms = Atoms('H2', positions=[[0.0, 0.0, 0.0], [0.0, 0.0, 0.74]])
    atoms.set_tags([3, 5])
    row = write_and_read(atoms)
    assert row.tags.dtype == np.int32
    assert np.array_equal(row.tags, [3, 5])


def test_empty_atoms_roundtrip():
    """Writing an empty Atoms must not be refused.

    blob() replaces empty arrays with np.zeros(0, dtype).  If it used
    the wrong dtype in np.zeros, the write call below would raise."""
    row = write_and_read(Atoms())
    assert len(row.numbers) == 0
