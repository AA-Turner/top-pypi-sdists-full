"""Tests for force-field utilities."""

import numpy as np

from ase.build import molecule
from ase.utils.ff import (
    Angle,
    Bond,
    Coulomb,
    Dihedral,
    Morse,
    get_angle_potential_gradient,
    get_angle_potential_reduced_hessian,
    get_angle_potential_value,
    get_bond_potential_gradient,
    get_bond_potential_reduced_hessian,
    get_bond_potential_value,
    get_coulomb_potential_gradient,
    get_coulomb_potential_hessian,
    get_coulomb_potential_value,
    get_dihedral_potential_gradient,
    get_dihedral_potential_reduced_hessian,
    get_dihedral_potential_value,
    get_morse_potential_gradient,
    get_morse_potential_reduced_hessian,
    get_morse_potential_value,
)


def test_morse_potential_reduced_hessian() -> None:
    """Test the reduced Hessian using the energy and gradient."""
    atoms = molecule('H2', vacuum=5.0)

    # https://cccbdb.nist.gov/exp2x.asp?casno=1333740
    morse = Morse(0, 1, D=5.0, alpha=2.0, r0=0.741)

    energy = get_morse_potential_value(atoms, morse)[-1]
    gradient = get_morse_potential_gradient(atoms, morse)[-1]
    hessian = get_morse_potential_reduced_hessian(atoms, morse)[-1]

    u = np.exp(-morse.alpha * (morse.r - morse.r0))
    expected = (
        np.outer(gradient, gradient)
        * np.abs(2.0 * u - 1.0)
        / (2.0 * u * energy)
    )

    np.testing.assert_allclose(hessian, expected)


def test_bond_potential_reduced_hessian() -> None:
    """Test the reduced Hessian using the energy and gradient."""
    atoms = molecule('H2', vacuum=5.0)

    # https://cccbdb.nist.gov/exp2x.asp?casno=1333740
    bond = Bond(0, 1, k=2.0, b0=0.741)

    energy = get_bond_potential_value(atoms, bond)[-1]
    gradient = get_bond_potential_gradient(atoms, bond)[-1]
    hessian = get_bond_potential_reduced_hessian(atoms, bond)[-1]

    expected = np.outer(gradient, gradient) / (2.0 * energy)

    np.testing.assert_allclose(hessian, expected)


def test_angle_potential_reduced_hessian() -> None:
    """Test the reduced Hessian using the energy and gradient."""
    atoms = molecule('H2O', vacuum=5.0)

    # https://cccbdb.nist.gov/exp2x.asp?casno=7732185
    angle = Angle(1, 0, 2, k=2.0, a0=np.deg2rad(104.4776))

    energy = get_angle_potential_value(atoms, angle)[-1]
    gradient = get_angle_potential_gradient(atoms, angle)[-1]
    hessian = get_angle_potential_reduced_hessian(atoms, angle)[-1]

    expected = np.outer(gradient, gradient) / (2.0 * energy)

    np.testing.assert_allclose(hessian, expected, atol=1e-15)


def test_dihedral_potential_reduced_hessian() -> None:
    """Test the reduced Hessian using the energy and gradient."""
    atoms = molecule('H2O2', vacuum=5.0)

    # https://cccbdb.nist.gov/exp2x.asp?casno=7722841
    dihedral = Dihedral(2, 0, 1, 3, k=2.0, d0=np.deg2rad(119.8))

    energy = get_dihedral_potential_value(atoms, dihedral)[-1]
    gradient = get_dihedral_potential_gradient(atoms, dihedral)[-1]
    hessian = get_dihedral_potential_reduced_hessian(atoms, dihedral)[-1]

    expected = np.outer(gradient, gradient) / (2.0 * energy)

    np.testing.assert_allclose(hessian, expected)


def test_dihedral_potential_reduced_hessian_periodic() -> None:
    """Test the reduced Hessian using the energy gradient."""
    atoms = molecule('H2O2', vacuum=5.0)

    # https://cccbdb.nist.gov/exp2x.asp?casno=7722841
    dihedral = Dihedral(0, 1, 2, 3, k=2.0, d0=np.deg2rad(119.8), n=2)

    gradient = get_dihedral_potential_gradient(atoms, dihedral)[-1]
    hessian = get_dihedral_potential_reduced_hessian(atoms, dihedral)[-1]

    arg = dihedral.n * dihedral.d - dihedral.d0
    expected = (
        np.outer(gradient, gradient)
        * np.abs(np.cos(arg))
        / (dihedral.k * np.sin(arg) ** 2)
    )

    np.testing.assert_allclose(hessian, expected)


def test_coulomb_potential_hessian() -> None:
    """Test the longitudinal Hessian using the energy and gradient."""
    atoms = molecule('HF', vacuum=5.0)

    coulomb = Coulomb(0, 1, chargeij=1.0)

    energy = get_coulomb_potential_value(atoms, coulomb)[-1]
    gradient = get_coulomb_potential_gradient(atoms, coulomb)[-1]
    hessian = get_coulomb_potential_hessian(atoms, coulomb)[-1]

    expected = 2.0 * np.outer(gradient, gradient) / energy

    # Check the longitudinal Hessian components along the bond axis.
    np.testing.assert_allclose(
        hessian[np.ix_([2, 5], [2, 5])],
        expected[np.ix_([2, 5], [2, 5])],
    )
