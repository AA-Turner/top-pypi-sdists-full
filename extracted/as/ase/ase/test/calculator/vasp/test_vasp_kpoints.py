"""
Check the many ways of specifying KPOINTS
"""

import os

import numpy as np
import pytest

from ase.build import bulk
from ase.calculators.vasp import Vasp
from ase.calculators.vasp.create_input import format_kpoints

from .filecmp_ignore_whitespace import filecmp_ignore_whitespace

calc = pytest.mark.calculator


@pytest.fixture()
def atoms():
    return bulk('Al', 'fcc', a=4.5, cubic=True)


def check_kpoints_line(n, contents):
    """Assert the contents of a line"""
    with open('KPOINTS') as fd:
        lines = fd.readlines()
    assert lines[n].strip() == contents


@pytest.fixture()
def write_kpoints(atoms):
    """Helper fixture to write the input kpoints file"""

    def _write_kpoints(factory, **kwargs):
        calc = factory.calc(**kwargs)
        calc.initialize(atoms)
        calc.write_kpoints(atoms=atoms)
        return atoms, calc

    return _write_kpoints


def test_vasp_kpoints_111(atoms):
    # Default to (1 1 1)
    string = format_kpoints(gamma=True, atoms=atoms, kpts=(1, 1, 1))
    check_kpoints_string(string, 2, 'Gamma')
    check_kpoints_string(string, 3, '1 1 1')


def test_vasp_kpoints_3_tuple(atoms):
    string = format_kpoints(gamma=False, kpts=(4, 4, 4), atoms=atoms)
    lines = string.split('\n')
    assert lines[1] == '0'
    assert lines[2] == 'Monkhorst-Pack'
    assert lines[3] == '4 4 4'


def check_kpoints_string(string, lineno, value):
    assert string.splitlines()[lineno].strip() == value


def test_vasp_kpoints_auto(atoms):
    string = format_kpoints(atoms=atoms, kpts=20)
    check_kpoints_string(string, 1, '0')
    check_kpoints_string(string, 2, 'Auto')
    check_kpoints_string(string, 3, '20')


def test_vasp_kpoints_1_element_list_gamma(atoms):
    # 1-element list ok, Gamma ok
    string = format_kpoints(atoms=atoms, kpts=[20], gamma=True)
    check_kpoints_string(string, 1, '0')
    check_kpoints_string(string, 2, 'Auto')
    check_kpoints_string(string, 3, '20')


@calc('vasp')
def test_kspacing_supress_kpoints_file(factory, write_kpoints):
    # KSPACING suppresses KPOINTS file
    Al, calc = write_kpoints(factory, kspacing=0.23)
    calc.write_incar(Al)
    assert not os.path.isfile('KPOINTS')
    with open('INCAR') as fd:
        assert 'KSPACING = 0.230000\n' in fd.readlines()


@calc('vasp')
def test_negative_kspacing_error(factory, write_kpoints):
    # Negative KSPACING raises an error
    with pytest.raises(ValueError):
        write_kpoints(factory, kspacing=-0.5)


@pytest.mark.parametrize('key', ['kspacing', 'kspacing_opt'])
@pytest.mark.parametrize('kspacing', [-0.5, 0.0])
def test_nonpositive_kspacing_error(atoms, tmp_path, key, kspacing):
    spacing = {'kspacing': 0.3, 'kspacing_opt': 0.1}
    spacing[key] = kspacing
    calc = Vasp(**spacing, kpts_opt=(6, 6, 6))
    with pytest.raises(
        ValueError, match=f'{key.upper()} value .* is not allowable'
    ):
        calc.write_kpoints(atoms, directory=tmp_path)


def test_weighted(atoms, testdir):
    # Explicit weighted points with nested lists, Cartesian if not specified
    string = format_kpoints(
        atoms=atoms,
        kpts=[[0.1, 0.2, 0.3, 2], [0.0, 0.0, 0.0, 1], [0.0, 0.5, 0.5, 2]],
    )

    with open('KPOINTS', 'w') as fd:
        fd.write(string)

    with open('KPOINTS.ref', 'w') as fd:
        fd.write("""KPOINTS created by Atomic Simulation Environment
    3 \n\
    Cartesian
    0.100000 0.200000 0.300000 2.000000 \n\
    0.000000 0.000000 0.000000 1.000000 \n\
    0.000000 0.500000 0.500000 2.000000 \n\
    """)

    assert filecmp_ignore_whitespace('KPOINTS', 'KPOINTS.ref')


def test_explicit_auto_weight(atoms, testdir):
    # Explicit points as list of tuples, automatic weighting = 1.
    string = format_kpoints(
        atoms=atoms,
        kpts=[(0.1, 0.2, 0.3), (0.0, 0.0, 0.0), (0.0, 0.5, 0.5)],
        reciprocal=True,
    )

    with open('KPOINTS', 'w') as fd:
        fd.write(string)

    with open('KPOINTS.ref', 'w') as fd:
        fd.write("""KPOINTS created by Atomic Simulation Environment
    3 \n\
    Reciprocal
    0.100000 0.200000 0.300000 1.0 \n\
    0.000000 0.000000 0.000000 1.0 \n\
    0.000000 0.500000 0.500000 1.0 \n\
    """)

    assert filecmp_ignore_whitespace('KPOINTS', 'KPOINTS.ref')


def test_bandpath(atoms):
    bandpath = atoms.cell.bandpath('GXMGRX,MR', npoints=100)
    string = format_kpoints(atoms=atoms, kpts=bandpath.kpts, reciprocal=True)
    check_kpoints_string(string, 1, '100')
    check_kpoints_string(string, 2, 'Reciprocal')
    check_kpoints_string(string, 3, '0.000000 0.000000 0.000000 1.0')
    check_kpoints_string(string, 102, '0.500000 0.500000 0.500000 1.0')


@pytest.mark.parametrize(
    'kpts_opt',
    [
        (6, 6, 6),
        20,
        {'path': 'GX', 'npoints': 10},
        [[0.0, 0.0, 0.0, 1.0], [0.5, 0.0, 0.0, 2.0]],
    ],
)
def test_kpoints_opt(atoms, tmp_path, kpts_opt):
    calc = Vasp(
        kpts=(2, 2, 2), kpts_opt=kpts_opt, gamma=True, reciprocal_opt=True
    )
    calc.write_kpoints(atoms, directory=tmp_path)
    assert (tmp_path / 'KPOINTS').read_text() == format_kpoints(
        (2, 2, 2), atoms, gamma=True
    )
    assert (tmp_path / 'KPOINTS_OPT').read_text() == format_kpoints(
        kpts_opt, atoms, reciprocal=True
    )
    restored = Vasp(gamma_opt=True)
    restored.read_kpoints(tmp_path / 'KPOINTS')
    restored.read_kpoints(tmp_path / 'KPOINTS_OPT', opt=True)
    assert tuple(restored.input_params['kpts']) == (2, 2, 2)
    assert restored.input_params['gamma']
    restored.write_kpoints(atoms, directory=tmp_path)
    actual = (tmp_path / 'KPOINTS_OPT').read_text().splitlines()
    expected = format_kpoints(kpts_opt, atoms, reciprocal=True).splitlines()
    assert actual[:3] == expected[:3]
    np.testing.assert_allclose(
        [float(x) for line in actual[3:] for x in line.split()],
        [float(x) for line in expected[3:] for x in line.split()],
    )


@pytest.mark.parametrize('scf_spacing', [None, 0.3])
@pytest.mark.parametrize('opt_spacing', [None, 0.1])
def test_kspacing_opt(atoms, tmp_path, scf_spacing, opt_spacing):
    spacing = {
        key: value
        for key, value in (
            ('kspacing', scf_spacing),
            ('kspacing_opt', opt_spacing),
        )
        if value is not None
    }
    calc = Vasp(
        **spacing,
        kpts_opt=(6, 6, 6),
        lkpoints_opt=True,
        kpoints_opt_nkbatch=4,
        kpoints_opt_mode=1,
    )
    calc.write_kpoints(atoms, directory=tmp_path)
    assert (tmp_path / 'KPOINTS').exists() == (scf_spacing is None)
    assert (tmp_path / 'KPOINTS_OPT').exists() == (opt_spacing is None)
    calc.spinpol = False
    calc.sort = np.arange(len(atoms))
    calc.write_incar(atoms, directory=tmp_path)
    restored = Vasp()
    restored.read_incar(tmp_path / 'INCAR')
    assert restored.float_params.get('kspacing_opt') == opt_spacing
    assert restored.bool_params['lkpoints_opt']
    assert restored.int_params['kpoints_opt_nkbatch'] == 4
    assert restored.int_params['kpoints_opt_mode'] == 1
    restored.read_kpoints(tmp_path / 'KPOINTS')
    restored.read_kpoints(tmp_path / 'KPOINTS_OPT', opt=True)
    assert (restored.input_params['kpts_opt'] is None) == (
        opt_spacing is not None
    )
    if opt_spacing is None:
        np.testing.assert_array_equal(
            restored.input_params['kpts_opt'], (6, 6, 6)
        )


def test_no_kpoints_opt_by_default(atoms, tmp_path):
    Vasp().write_kpoints(atoms, directory=tmp_path)
    assert (tmp_path / 'KPOINTS').is_file()
    assert not (tmp_path / 'KPOINTS_OPT').exists()
