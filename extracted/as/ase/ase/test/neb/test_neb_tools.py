"""Tests for `NEBTools`."""

import numpy as np
import pytest

import ase.io
from ase import Atoms
from ase.calculators.emt import EMT
from ase.mep.neb import NEB, NEBTools, _guess_nimages
from ase.optimize import BFGS


@pytest.fixture
def images() -> list[Atoms]:
    symbols = 7 * ['Cu']
    cell = [
        [0.000, 1.805, 1.805],
        [1.805, 0.000, 1.805],
        [1.805, 1.805, 0.000],
    ]
    images = []
    for pos in np.linspace(0.0, 0.5, 6):
        scaled_positions = [
            [0.0, 0.0, pos],
            [0.0, 0.5, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.0],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
            [0.5, 0.5, 0.5],
        ]
        atoms = Atoms(
            symbols,
            scaled_positions=scaled_positions,
            cell=cell,
            pbc=True,
        )
        images.append(atoms)
    return images


@pytest.mark.parametrize('repetition', [1, 2])
def test_guess_nimages(images: list[Atoms], repetition: int) -> None:
    """Test if `_guess_nimages` return the expected values.

    This tests a symmetric path with 1 or 2 bands in the images.
    """
    number_of_images = len(images)

    images_extended = []
    for _ in range(repetition):
        for atoms_ref in images:
            atoms = atoms_ref.copy()
            atoms.calc = EMT()
            atoms.get_potential_energy()
            images_extended.append(atoms)

    assert _guess_nimages(images_extended) == number_of_images


class _HeavyWeightEMT(EMT):
    """`EMT` mimicking a heavy-weight calculator.

    A "heavy-weight" calculator does not compute forces when
    `get_potential_energy` is called.
    This class mimics such a calculator by removing `forces` from the results.
    """

    def get_potential_energy(self, *args, **kwargs):
        # store forces if already computed
        forces = self.results.pop('forces', None)
        energy = super().get_potential_energy(*args, **kwargs)
        # restore the previous forces
        self.results['forces'] = forces
        return energy


def test_heavy_weight_calculator(tmp_path, images):
    """Test if `NEBTools` works for heavy-weight calculators.

    This function tests the case where (1) end-point images used heavy-weight
    calculators that did not compute forces when `get_potential_energy` was
    called and (2) the computed data are transferred to `SinglePointCalculator`,
    where the properties cannot be recomputed.
    """
    for atoms in images:
        atoms.calc = _HeavyWeightEMT()

    BFGS(NEB(images)).run(steps=1)

    # write images and then read again to switch to `SinglePointCalculator`
    ase.io.write(tmp_path / 'tmp.traj', images)
    images = ase.io.read(tmp_path / 'tmp.traj', index=':')

    NEBTools(images).get_barrier(fit=True)
