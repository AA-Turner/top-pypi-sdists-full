from pathlib import Path

import pytest

from ase.build import molecule
from ase.io import read, write


@pytest.mark.parametrize('index', [-3, 2])
def test_out_of_range_index(tmp_path: Path, index: int) -> None:
    fd = tmp_path / 'test.xyz'
    images = [molecule('H2'), molecule('H2O')]
    write(fd, images, format='extxyz')
    with pytest.raises(StopIteration):  # TODO: IndexError may be more suitable.
        read(fd, index=index, format='extxyz')
