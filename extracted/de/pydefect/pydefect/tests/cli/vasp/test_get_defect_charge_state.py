# -*- coding: utf-8 -*-
#  Copyright (c) 2020 Kumagai group.
from pathlib import Path

import pytest
from pydefect.cli.vasp.get_defect_charge_state import \
    get_defect_charge_state
from pymatgen.core import Structure, Lattice
from pymatgen.io.vasp import Poscar, Potcar, Incar


def test_get_defect_charge_state(tmpdir, mocker):
    tmpdir.chdir()
    structure = Structure(Lattice.cubic(10), ["H", "He"], [[0.0]*3, [0.5]*3])

    potcar = mocker.MagicMock()
    potcar.symbols = ["H_pv", "He"]

    mock_h  = mocker.Mock(nelectrons=1)
    mock_he = mocker.Mock(nelectrons=2)

    potcar.__iter__.return_value = iter([mock_h, mock_he])

    incar = Incar.from_str("NELECT = 1")
    assert get_defect_charge_state(Poscar(structure), potcar, incar) == 3 - 1

    structure = Structure(Lattice.cubic(10), ["H", "He", "H", "H"],
                          [[0.0]*3, [0.2]*3, [0.4]*3, [0.6]*3])
    with pytest.raises(ValueError):
        get_defect_charge_state(Poscar(structure), potcar, incar)

    incar = Incar.from_str("")
    assert get_defect_charge_state(Poscar(structure), potcar, incar) == 0


