import numpy as np
import pytest

from ase.atoms import Atoms
from ase.calculators.vasp import Vasp


def check_written_incar(parameters, expected_output, incar_roundtrip):
    assert incar_roundtrip(Vasp(**parameters)) == expected_output


def test_str_key(incar_roundtrip):
    parameters = {'prec': 'Low'}
    expected_output = 'PREC = Low\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_special_str_key(incar_roundtrip):
    parameters = {'xc': 'PBE'}
    expected_output = 'GGA = PE\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_float_key(incar_roundtrip):
    parameters = {'encut': 400.0}
    expected_output = 'ENCUT = 400.000000\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_exp_key(incar_roundtrip):
    parameters = {'ediff': 1e-6}
    expected_output = 'EDIFF = 1.00e-06\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_int_key(incar_roundtrip):
    parameters = {'ibrion': 2}
    expected_output = 'IBRION = 2\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_list_bool_key(incar_roundtrip):
    parameters = {'lattice_constraints': [False, True, False]}
    expected_output = 'LATTICE_CONSTRAINTS = .FALSE. .TRUE. .FALSE.\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_bool_key(incar_roundtrip):
    parameters = {'lhfcalc': True}
    expected_output = 'LHFCALC = .TRUE.\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_special_key(incar_roundtrip):
    parameters = {'lreal': True}
    expected_output = 'LREAL = .TRUE.\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_list_float_key(incar_roundtrip):
    parameters = {'magmom': [0.5, 1.5]}
    expected_output = (
        'MAGMOM = 1*0.5000 1*1.5000\nISPIN = 2\n'  # Writer uses :.4f
    )
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_dict_key(incar_roundtrip):
    parameters = {'ldau_luj': {'H': {'L': 2, 'U': 4.0, 'J': 0.0}}}
    expected_output = 'LDAU = .TRUE.\nLDAUL = 2\nLDAUU = 4.000\nLDAUJ = 0.000\n'
    check_written_incar(parameters, expected_output, incar_roundtrip)


def test_m_constr_key(incar_roundtrip) -> None:
    parameters = {
        'm_constr': [[0.0, 0.0, 1.5], [1.5, 0.0, 0.0]],
        'lnoncollinear': True,
    }
    expected_output = (
        'M_CONSTR = 2*0.0000 2*1.5000 2*0.0000\nLNONCOLLINEAR = .TRUE.\n'
    )
    check_written_incar(parameters, expected_output, incar_roundtrip)


@pytest.mark.parametrize('key', ['encut', 'npar', 'magmom'])
def test_unset_parameter(key, incar_roundtrip):
    calc = Vasp(**{key: None})
    incar = incar_roundtrip(calc)
    assert key not in calc.asdict()['inputs']
    assert key.upper() not in incar


@pytest.mark.parametrize('dtype', [np.int32, np.int64, np.uint64])
def test_numpy_integer(dtype, incar_roundtrip):
    calc = Vasp(encut=dtype(520), new_list=np.array([1, 2], dtype=dtype))
    incar = incar_roundtrip(calc)
    assert calc.encut == 520
    assert 'ENCUT = 520\n' in incar
    assert 'NEW_LIST = 1 2\n' in incar


@pytest.mark.parametrize('dtype', [int, np.int32, np.int64, float])
@pytest.mark.parametrize('ispin', [None, 1, 2])
def test_magmom_processing(dtype, ispin, incar_roundtrip):
    atoms = Atoms('FeNiFe')
    magmom = np.array([1, -1, 2], dtype=dtype)
    kwargs = {} if ispin is None else {'ispin': ispin}
    calc = Vasp(magmom=magmom, **kwargs)
    incar = incar_roundtrip(calc, atoms)
    assert f'ISPIN = {2 if ispin is None else ispin}\n' in incar
    assert 'MAGMOM = 1*1.0000 1*2.0000 1*-1.0000\n' in incar


def test_magmom_integer_list(incar_roundtrip):
    atoms = Atoms('FeNiFe')
    calc = Vasp(magmom=[1, -1, 2])
    incar = incar_roundtrip(calc, atoms)
    assert 'ISPIN = 2\n' in incar
    assert 'MAGMOM = 1*1.0000 1*2.0000 1*-1.0000\n' in incar


@pytest.mark.parametrize('dtype', [int, float])
def test_noncollinear_integer_magmoms(dtype, incar_roundtrip):
    atoms = Atoms('FeNiFe')
    moments = np.eye(3, dtype=dtype)
    calc = Vasp(magmom=moments, m_constr=moments, lnoncollinear=True)
    incar = incar_roundtrip(calc, atoms)
    sorted_moments = '1*1.0000 4*0.0000 1*1.0000 1*0.0000 1*1.0000 1*0.0000'
    assert f'MAGMOM = {sorted_moments}\n' in incar
    assert f'M_CONSTR = {sorted_moments}\n' in incar
    assert 'ISPIN' not in incar
