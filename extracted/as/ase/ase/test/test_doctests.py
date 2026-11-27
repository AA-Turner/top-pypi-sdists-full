import doctest
import importlib
import pkgutil

import numpy as np
import pytest

import ase

all_module_names = [
    module.name for module in pkgutil.walk_packages(ase.__path__, prefix='ase.')
]

skip_module_names = """
ase.calculators.abinit
ase.calculators.dmol
ase.calculators.elk
ase.calculators.exciting.exciting
ase.calculators.gamess_us
ase.calculators.kim
ase.calculators.kim.kimpy_wrappers
ase.calculators.kim.neighborlist
ase.calculators.lammpslib
ase.calculators.mopac
ase.calculators.nwchem
ase.calculators.openmx.reader
ase.calculators.orca
ase.dft.band_structure
ase.io.elk
ase.io.eon
ase.io.espresso
ase.io.vasp
ase.transport.calculators
ase.utils.cube
ase.utils.sphinx_create_png
ase.utils.structure_comparator
ase.vibrations.infrared
""".split()


module_names = set(all_module_names) - set(skip_module_names)

# remove some modules like ase.test, ase.gui
rem_modules = [
    modname
    for name in ['ase.test', 'ase.gui', 'ase.ga']
    for modname in module_names
    if name in modname
]
module_names -= set(rem_modules)

sorted_module_names = sorted(module_names)


@pytest.mark.parametrize('modname', sorted_module_names)
def test_doctest(testdir, modname):
    if int(np.__version__.split('.')[0]) < 2:
        pytest.skip('Doctests need numpy2+')
    mod = importlib.import_module(modname)
    doctest.testmod(mod, raise_on_error=True, verbose=True)
