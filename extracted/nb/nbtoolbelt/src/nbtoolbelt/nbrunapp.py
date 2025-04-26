"""
Main for nbrun

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import _ArgumentGroup, SUPPRESS
from pathlib import Path
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.arguments import NegatableAction, quote_help
from nbtoolbelt.counting import nb_code_execution_stats
from nbtoolbelt.printing import print_dict
from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.running import run_nb
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'run'


class RunTool(Tool):
    """Run each notebook, with optional pre-/post-cleaning, and return results.
    """
    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            action=TOOL,
            description="""Run Jupyter notebooks, with optional pre/post-cleaning."""
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Run notebook nb.

        .. note:: **Modifies**: ``nb``

        :param nb: notebook to run
        :param nb_path: path to ``nb``
        :return: resulting (notebook, notebook-path) pair
        """
        args = self._args

        run_nb(nb, args)

        # print statistics, unless in quiet mode
        stats = nb_code_execution_stats(nb)
        if not args.quiet:
            print_dict(stats, "Execution statistics")
        self._aggregate['outputs'][-1].update(stats)

        # set up destination path
        if args.inplace:
            nb_run_path = nb_path
        else:
            nb_run_path = nb_path.with_name(nb_path.stem + args.run_result_name + nb_path.suffix)

        if args.debug:  # TODO is this needed here (or should it happen in Tool.process_file?
            print('Destination of run:', nb_run_path)

        return [(nb, nb_run_path)]

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        group.add_argument('-e', '--allow-errors',
                           action=NegatableAction,
                           help='continue on errors' +
                                ' (default: {})'.format(self._args.allow_errors))
        group.add_argument('-b', '--clean-before',
                           action=NegatableAction,
                           help='clean code output before running' +
                                ' (default: {}'.format(self._args.clean_before))
        group.add_argument('-a', '--clean-after',
                           action=NegatableAction,
                           help='clean code metadata after running' +
                                ' (default: {})'.format(self._args.clean_after))
        group.add_argument('-k', '--kernel-name',
                           dest='kernel_name', default=SUPPRESS,
                           help='name of kernel to use, e.g. python3; '' for kernel specified in notebook;' +
                                " default: '{}')".format(self._args.kernel_name))
        group.add_argument('-p', '--run-path',
                           dest='run_path', default=SUPPRESS,
                           help='working directory for execution ;"" for current working directory' +
                                " (default: '{}')".format(self._args.run_path))
        group.add_argument('-t', '--timeout',
                           type=int, default=SUPPRESS,
                           help='timeout time in seconds per cell; -1 for unlimited' +
                                ' (default: {})'.format(self._args.timeout))
        group.add_argument('-i', '--interrupt-on-timeout',
                           action=NegatableAction, default=SUPPRESS,
                           help='interrupt execution on timeout' +
                                ' (default: {})'.format(self._args.interrupt_on_timeout))
        group.add_argument('-r', '--record-timing',
                           action=NegatableAction, default=SUPPRESS,
                           help='record execution times' +
                                ' (default: {})'.format(self._args.record_timing))
        group.add_argument('-w', '--append-cell',
                           action=NegatableAction, default=SUPPRESS,
                           help='append special code cell' +
                                " (default: '{}') ".format(quote_help(self._args.appended_cell)) +
                                'before executing notebooks' +
                                ' (default: {})'.format(self._args.append_cell))
        group.add_argument('--streams-head',
                           type=int, default=SUPPRESS,
                           help='limit output streams to a maximum number of lines per cell; -1 for unlimited' +
                                ' (default: {})'.format(self._args.streams_head))
        group.add_argument('--ipc',
                           default=SUPPRESS,
                           help='Use IPC with given path to communicate with the kernel; \'\' for TCP' +
                                " (default: '{}')".format(self._args.ipc))

    def print_tool_args(self) -> None:
        if self._args.clean_before:
            action = 'Cleaning'
        else:
            action = 'Keeping'
        what = f" and {self._args.clean_before_metadata} metadata" if self._args.clean_before_metadata else ''
        print('  {} code output{} before running'.format(action, what))

        print('  Timeout:', 'unlimited' if self._args.timeout < 0 else '{} s'.format(self._args.timeout))
        print('  Kernel name:', self._args.kernel_name if self._args.kernel_name else 'from notebook')
        print('  Working dir:', self._args.run_path if self._args.run_path else 'current directory')

        if self._args.allow_errors:
            action = 'Not stopping at errors'
        else:
            action = 'Stopping at first error'
        print('  {}'.format(action))

        if self._args.timeout >= 0:
            action = 'times out after {} seconds'.format(self._args.timeout)
        else:
            action = 'does not time out'
        print('  Cell execution {}'.format(action))

        if self._args.timeout >= 0:
            if self._args.interrupt_on_timeout:
                action = 'I'
            else:
                action = 'Not i'
            print('  {}nterrupting kernel on timeout'.format(action))

        if self._args.record_timing:
            action = 'R'
        else:
            action = 'Not r'
        print('  {}ecording execution times'.format(action))

        if self._args.append_cell:
            action = 'Appending'
        else:
            action = 'Not appending'
        print('  {} code cell with %whos'.format(action))

        if self._args.clean_after:
            action = 'Cleaning {}'.format(self._args.clean_after_metadata)
        else:
            action = 'Keeping'
        print('  {} code metadata after running'.format(action))

        if self._args.streams_head >= 0:
            print('  Limiting output streams to {} lines'.format(self._args.streams_head))
        else:
            print('  Not limiting output streams')


def main(cli_args: Optional[List[str]] = None) -> int:
    return RunTool().main(cli_args)


if __name__ == "__main__":
    import sys
    sys.exit(main())
