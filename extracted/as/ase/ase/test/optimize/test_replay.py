import shutil
from math import sqrt

import pytest

from ase import Atom, Atoms
from ase.calculators.calculator import compare_atoms
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from ase.optimize import (
    BFGS,
    LBFGS,
    BFGSLineSearch,
    LBFGSLineSearch,
)

optclasses = [
    BFGS,
    LBFGS,
    BFGSLineSearch,
    LBFGSLineSearch,
]


@pytest.fixture(name='optcls', params=optclasses)
def fixture_optcls(request):
    optcls = request.param
    return optcls


@pytest.fixture(name='atoms')
def fixture_atoms() -> Atoms:
    # Distance between Cu atoms on a (100) surface:
    d = 3.6 / sqrt(2)
    atoms = Atoms(
        'Cu',
        positions=[(0, 0, 0)],
        cell=(d, d, 1.0),
        pbc=(True, True, False),
    )
    atoms *= (2, 2, 1)  # 2x2 (100) surface-cell

    # Approximate height of Ag atom on Cu(100) surfece:
    h0 = 2.0
    atoms += Atom('Ag', (d / 2, d / 2, h0))

    constraint = FixAtoms(range(len(atoms) - 1))
    atoms.set_constraint(constraint)

    return atoms


@pytest.mark.optimize()
def test_replay(testdir, optcls, atoms):
    """Test if `replay_trajectory` reproduces the optimizer state."""

    # The initial structure is first loosely optimized.
    atoms.calc = EMT()
    dyn = optcls(atoms, trajectory='ase.traj')
    dyn.run(fmax=0.1)

    # The present structure and the trajectory file are copied.
    atoms_loosely_optimized = atoms.copy()
    shutil.copy2('ase.traj', 'tmp.traj')

    # The structure is further more tightly optimized.
    dyn.run(fmax=0.01)

    # Test that the final structure differs from the intermediate one.
    assert compare_atoms(atoms, atoms_loosely_optimized)

    # Test that a new tight optimization starting from the intermediate
    # structure without replay results in a different final structure.
    atoms_reoptimized_from_scratch = atoms_loosely_optimized.copy()
    atoms_reoptimized_from_scratch.calc = EMT()
    dyn_from_scratch = optcls(atoms_reoptimized_from_scratch)
    dyn_from_scratch.run(fmax=0.01)
    assert compare_atoms(atoms_reoptimized_from_scratch, atoms)

    # Test that a new tight optimization starting from the intermediate
    # structure with replay results in the same final structure.
    atoms_reoptimized_after_replay = atoms_loosely_optimized.copy()
    atoms_reoptimized_after_replay.calc = EMT()
    dyn_after_replay = optcls(atoms_reoptimized_after_replay)
    dyn_after_replay.replay_trajectory('tmp.traj')
    dyn_after_replay.run(fmax=0.01)
    assert not compare_atoms(atoms_reoptimized_after_replay, atoms)
