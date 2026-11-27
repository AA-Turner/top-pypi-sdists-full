"""Tests for `MelchionnaNPT`."""

import numpy as np
import pytest

from ase import Atoms
from ase.md.melchionna import MelchionnaNPT
from ase.units import fs

strain_rates = [np.triu(np.ones((3, 3))), np.tril(np.ones((3, 3)))]


@pytest.mark.parametrize('strain_rate', strain_rates)
def test_melchionna_npt_set_strain_rate(strain_rate: np.ndarray) -> None:
    """Test `set_strain_rate` for upper and lower triangular matrices."""
    atoms = Atoms('H', cell=10 * np.eye(3), pbc=True)
    dynamics = MelchionnaNPT(
        atoms,
        timestep=1.0 * fs,
        temperature_K=300.0,
    )

    dynamics.set_strain_rate(strain_rate)

    np.testing.assert_array_equal(
        dynamics.get_strain_rate(),
        strain_rate,
    )
