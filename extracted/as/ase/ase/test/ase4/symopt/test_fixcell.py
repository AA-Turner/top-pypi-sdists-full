import numpy as np
import pytest

from ase._4.optimize._symopt.relax import SymmetryAdaptedAtoms
from ase._4.optimize.bfgs import BFGSMethod
from ase._4.optimize.run import Optimizer
from ase._4.optimize.symopt import SymOpt
from ase.build import bulk
from ase.calculators.emt import EMT


class NoStressEMT(EMT):
    def __init__(self):
        super().__init__()
        self.ncalculations = 0

    def calculate(self, atoms, properties, system_changes):
        assert 'stress' not in properties

        self.ncalculations += 1
        return super().calculate(atoms, properties, system_changes)

    def get_stress(self, *args, **kwargs):
        raise RuntimeError


def run_symopt_fixcell(atoms):
    symmatoms = SymmetryAdaptedAtoms.from_atoms(atoms, fixcell=True)
    # Arguably we should allow not passing smax when fixing cell.
    target = SymOpt(symmatoms, fmax=0.01, smax=1.234)
    opt = Optimizer(target, BFGSMethod(70 * np.identity(len(target.get_x()))))
    return opt.run()


def test_symopt_nodofs():
    """Test that optimization runs correctly without any dofs at all.

    This happens with fixcell when there would be only cell DOFs.

    Nobody optimizes a system without dofs on purpose, but if they do,
    they are running high throughput and they just want a result.
    This test ensures there's one calculation so trajectories etc.
    will be "normal".
    """
    atoms = bulk('Au')
    atoms.calc = NoStressEMT()

    step = run_symopt_fixcell(atoms)

    assert step.i == 0
    assert len(step.gradient_obj.gradient) == 0
    assert step.gradient_obj.fnorm == 0.0
    assert step.gradient_obj.snorm == 0.0
    # EMT actually evaluates all the properties and puts them in calc.results.
    assert atoms.calc.ncalculations == 1


def test_symmatoms_fixcell():
    """Test that symopt works with fixed cell.

    We test that 1) stress tensor is not computed and 2) cell does not change.
    """
    atoms = bulk('Au') * (2, 2, 1)
    atoms.cell -= 0.1 * np.random.RandomState(42).random((3, 3))
    atoms.rattle(stdev=0.05, seed=17)
    atoms.calc = NoStressEMT()

    with pytest.raises(RuntimeError):
        atoms.get_stress()

    e0 = atoms.get_potential_energy()
    cell0 = atoms.cell.copy()
    step = run_symopt_fixcell(atoms)
    assert step.gradient_obj.converged  # XXX improve API
    assert atoms.cell[:] == pytest.approx(cell0, abs=1e-16)
    # Energy should be at least somewhat lower:
    e1 = atoms.get_potential_energy()
    assert e1 < e0 - 0.05


def test_not_symmetric_enough():
    """If atoms are symmetric but not the cell, we want to complain."""
    from ase.build import bulk

    atoms = bulk('Si')
    atoms.cell[0, 0] += 1e-6
    with pytest.raises(ValueError, match='Symmetrized cell differs'):
        SymmetryAdaptedAtoms.from_atoms(atoms, fixcell=True)
