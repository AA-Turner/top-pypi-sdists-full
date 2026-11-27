import shutil
import subprocess
import sys

import pytest


@pytest.fixture(scope='module')
def mpiexec():
    pytest.importorskip('mpi4py')
    mpiexec = shutil.which('mpiexec')
    if mpiexec is None:
        pytest.skip('No mpiexec command')
    return mpiexec


ECHO = 'from ase.parallel import world; print(world.rank, world.size)'


@pytest.mark.parametrize(
    'args',
    [
        ['ase', 'parallel', __file__, 'arg1', '--arg2'],
        ['ase', 'parallel', '-m', __name__, 'arg1', '--arg2'],
        ['ase', 'parallel', '-c', ECHO],
    ],
)
def test_ase_parallel(mpiexec, args):
    output = subprocess.check_output(
        [mpiexec, '-n', '4', 'python', '-m', *args],
        encoding='utf-8',
    )

    assert sorted(output.strip().split('\n')) == ['0 4', '1 4', '2 4', '3 4']


def main():
    from ase.parallel import world

    assert sys.argv[1:] == ['arg1', '--arg2']

    assert world.size == 4
    assert world.sum_scalar(world.rank) == 6
    print(world.rank, world.size)


if __name__ == '__main__':
    main()
