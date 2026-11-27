"""Tests for velocity distributions."""

from contextlib import nullcontext

import numpy as np
import pytest

from ase import Atoms
from ase.constraints import FixAtoms
from ase.lattice.cubic import FaceCenteredCubic
from ase.md import thermalize_momenta
from ase.md.velocitydistribution import (
    MaxwellBoltzmannDistribution,
    Stationary,
    ZeroRotation,
    force_temperature,
)
from ase.units import kB


@pytest.fixture(name='atoms')
def fixture_atoms() -> Atoms:
    """Fixture of atoms for testing."""
    return FaceCenteredCubic(size=(50, 50, 50), symbol='Cu', pbc=False)


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_maxwell_boltzmann_distribution(atoms: Atoms) -> None:
    """Test deprecated `MaxwellBoltzmannDistribution`."""
    temperature = 300.0  # in K

    rng = np.random.default_rng(42)
    thermalize_momenta(atoms, temperature, rng=rng)
    momenta_ref = atoms.get_momenta().copy()

    rng = np.random.default_rng(42)
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature, rng=rng)
    momenta = atoms.get_momenta().copy()

    np.testing.assert_allclose(momenta, momenta_ref)


def test_thermalize_momenta(atoms: Atoms) -> None:
    """Test `thermalize_momenta`."""
    print('Number of atoms:', len(atoms))
    thermalize_momenta(atoms, temperature_K=0.1 / kB)
    temp = atoms.get_kinetic_energy() / (1.5 * len(atoms))

    print('Temperature', temp, ' (should be 0.1)')
    assert abs(temp - 0.1) < 1e-3


def test_maxwellboltzmann_dof(atoms: Atoms) -> None:
    atoms.set_constraint(FixAtoms(range(250000)))

    thermalize_momenta(atoms, 1000.0)
    assert pytest.approx(atoms.get_temperature(), 5) == 1000

    thermalize_momenta(atoms, 1000.0, exact_temperature=True)
    assert pytest.approx(atoms.get_temperature(), 1e-8) == 1000

    Stationary(atoms, preserve_temperature=True)
    assert pytest.approx(atoms.get_temperature(), 1e-8) == 1000

    ZeroRotation(atoms, preserve_temperature=True)
    assert pytest.approx(atoms.get_temperature(), 1e-8) == 1000


@pytest.mark.parametrize(
    ('temperature', 'expectation'),
    [(0.0, nullcontext()), (1000.0, pytest.raises(RuntimeError))],
)
def test_force_temperature_with_zero_velocities(
    atoms: Atoms,
    temperature: float,
    expectation,
) -> None:
    """Test `force_temperature` for `Atoms` with zero temperature."""
    with expectation:
        force_temperature(atoms, temperature=temperature)
