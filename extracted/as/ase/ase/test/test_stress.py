import numpy as np
import pytest

from ase.build import bulk
from ase.calculators.fd import calculate_numerical_stress
from ase.calculators.lj import LennardJones
from ase.filters import UnitCellFilter
from ase.optimize import BFGS
from ase.stress import get_elasticity_tensor

# Theoretical infinite-cutoff LJ FCC unit cell parameters
vol0 = 4 * 0.91615977036  # theoretical minimum
a0 = vol0 ** (1 / 3)


@pytest.fixture()
def atoms():
    """two atoms at potential minimum"""
    atoms = bulk('X', 'fcc', a=a0)

    atoms.calc = LennardJones()

    return atoms


def test_stress_voigt_shape(atoms):
    # test voigt shape
    for ideal_gas in (False, True):
        kw = {'include_ideal_gas': ideal_gas}

        assert atoms.get_stress(voigt=True, **kw).shape == (6,)
        assert atoms.get_stress(voigt=False, **kw).shape == (3, 3)

        assert atoms.get_stresses(voigt=True, **kw).shape == (len(atoms), 6)
        assert atoms.get_stresses(voigt=False, **kw).shape == (len(atoms), 3, 3)


@pytest.mark.optimize()
@pytest.mark.slow()
def test_stress(atoms):
    cell0 = atoms.get_cell()

    atoms.set_cell(
        np.dot(
            atoms.cell, [[1.02, 0, 0.03], [0, 0.99, -0.02], [0.1, -0.01, 1.03]]
        ),
        scale_atoms=True,
    )

    atoms *= (1, 2, 3)
    cell0 *= np.array([1, 2, 3])[:, np.newaxis]

    atoms.rattle()

    # Verify analytical stress tensor against numerical value
    s_analytical = atoms.get_stress()
    s_numerical = calculate_numerical_stress(atoms, 1e-5)
    s_p_err = 100 * (s_numerical - s_analytical) / s_numerical

    print('Analytical stress:\n', s_analytical)
    print('Numerical stress:\n', s_numerical)
    print('Percent error in stress:\n', s_p_err)
    assert np.all(abs(s_p_err) < 1e-5)

    # Minimize unit cell
    opt = BFGS(UnitCellFilter(atoms))
    opt.run(fmax=1e-3)

    # Verify minimized unit cell using Niggli tensors
    g_minimized = np.dot(atoms.cell, atoms.cell.T)
    g_theory = np.dot(cell0, cell0.T)
    g_p_err = 100 * (g_minimized - g_theory) / g_theory

    print('Minimized Niggli tensor:\n', g_minimized)
    print('Theoretical Niggli tensor:\n', g_theory)
    print('Percent error in Niggli tensor:\n', g_p_err)
    assert np.all(abs(g_p_err) < 1)


def emt_aluminium_supercell(supercell):
    from ase.calculators.emt import EMT
    from ase.filters import FrechetCellFilter
    from ase.optimize.bfgs import BFGS

    # Do a slightly funny supercell so
    atoms = bulk('Al') * supercell
    atoms.calc = EMT()
    BFGS(FrechetCellFilter(atoms)).run(fmax=1e-9)
    return atoms


def test_elasticity_tensor_displacement():
    from ase.stress import voigt_6_to_full_3x3_stress

    atoms = emt_aluminium_supercell((2, 3, 4))
    e0 = atoms.get_potential_energy()

    eps = 1e-5
    tensor_3333 = get_elasticity_tensor(atoms, h=eps)

    # Atoms must be unchanged-ish after the call, even though we do the
    # displacements in-place.  (Smaller tolerance than 1e-13 does not pass.)
    assert atoms.get_potential_energy() == pytest.approx(e0, abs=1e-13)

    tensor_99 = tensor_3333.reshape((9, 9))
    np.set_printoptions(precision=4, suppress=1)
    # We could test all the tensor's symmetries but here we just do .T:
    assert tensor_99 == pytest.approx(tensor_99.T, abs=1e-10)

    # Strain the atoms randomly, then test that the elasticity tensor
    # predicts the stress:
    rng = np.random.default_rng(42)
    delta = rng.random((3, 3)) * eps
    strain_33 = np.identity(3) + delta
    atoms.set_cell(atoms.cell @ strain_33, scale_atoms=True)

    actual_stress_33 = voigt_6_to_full_3x3_stress(atoms.get_stress())

    assert tensor_99 @ delta.ravel() == pytest.approx(
        actual_stress_33.ravel(), abs=1e-9
    )
