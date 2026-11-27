import argparse
import os
import runpy
import sys


def main(args, parser):
    from ase.cli.main import CLIError

    assert 'ase.parallel' not in sys.modules

    envvar = 'ASE_PARALLEL_WORLD_HOOK'
    current_hook = os.environ.get(envvar)
    if current_hook is not None:
        raise CLIError('Someone already set ASE_PARALLEL_WORLD_HOOK')

    # As an alternative, we can also start a new Python process
    # with subprocess.check_call([sys.executable, ...], env=...).
    os.environ[envvar] = 'ase.hook_mpi4py'

    if args.script:
        sys.argv[:] = args.script
        runpy.run_path(args.script[0], run_name='__main__')
    elif args.module:
        sys.argv[:] = args.module
        runpy.run_module(args.module[0], run_name='__main__')
    elif args.cmd:
        eval(compile(args.cmd, '<string>', 'single'))
    else:
        raise CLIError('No script, module, or command to run')


class CLICommand:
    """Run Python with ASE in parallel using mpi4py.

    Examples::

      $ mpiexec -n 4 ase parallel myscript.py --options-to-script
      $ mpiexec -n 4 python -m ase parallel -m mymodule --options-to-module
      $ mpiexec -n 4 ase parallel -c "print('hello, world!')"
    """

    @staticmethod
    def add_arguments(parser):
        group = parser.add_mutually_exclusive_group()
        parser.add_argument(
            'script',
            help='script to run and arguments',
            nargs=argparse.REMAINDER,
        )
        group.add_argument(
            '-m',
            '--module',
            help='module to run and arguments',
            nargs=argparse.REMAINDER,
        )
        group.add_argument(
            '-c',
            '--cmd',
            help='program passed as python string',
        )

    @staticmethod
    def run(args, parser):
        main(args, parser)
