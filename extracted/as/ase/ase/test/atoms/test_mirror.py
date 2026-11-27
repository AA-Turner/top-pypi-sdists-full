import numpy as np
import pytest

from ase import Atoms
from ase.build import molecule


def test_mirror_direction():
    atoms = molecule('H2O')

    a1_pos = atoms[1].position.copy()
    atoms.mirror('z')
    assert pytest.approx(atoms[1].position) == a1_pos * (1, 1, -1)

    a1_pos = atoms[1].position.copy().reshape((3, 1))
    atoms.mirror((0, 1, 1))
    matrep = np.array([[1, 0, 0], [0, 0, -1], [0, -1, 0]])
    assert pytest.approx(atoms[1].position) == (matrep @ a1_pos).ravel()


def test_mirror_center():
    atoms = Atoms('CuO', [[0, 0, 0], [1.75, 0, 0]])
    atoms.center(1)

    atoms.mirror('x', center='COU')
    assert pytest.approx(atoms[0].position[0]) == 2.75

    atoms.mirror('x', center='COP')
    assert pytest.approx(atoms[0].position[0]) == 1.0

    atoms.mirror('x', center='COM')
    assert pytest.approx(atoms[0].position[0]) == 1.70396

    atoms.mirror('x', center=(0, 0, 0))
    assert pytest.approx(atoms[0].position[0]) == -1.70396


def test_mirror_mask():
    atoms = molecule('H2')
    atoms.center(1)
    atoms_pos = atoms.positions.copy()

    atoms.mirror('z', center=(0, 0, 0), indices=[True, False])
    assert pytest.approx(atoms[0].position) == atoms_pos[0] * (1, 1, -1)
    assert pytest.approx(atoms[1].position) == atoms_pos[1]


def test_mirror_indices():
    atoms = molecule('H2')
    atoms.center(1)
    atoms_pos = atoms.positions.copy()

    atoms.mirror('z', center=(0, 0, 0), indices=[0])
    assert pytest.approx(atoms[0].position) == atoms_pos[0] * (1, 1, -1)
    assert pytest.approx(atoms[1].position) == atoms_pos[1]


def test_mirror_cell():
    atoms = molecule('H2')
    atoms.center(1)

    atoms_cell = atoms.get_cell().transpose()
    atoms.mirror((0, 1, 1), mirror_cell=True)
    matrep = np.array([[1, 0, 0], [0, 0, -1], [0, -1, 0]])
    assert pytest.approx(atoms.get_cell().transpose()) == matrep @ atoms_cell
