"""
Tool nbhead; shows head of notebooks

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.

This tool also illustrates how to extend class Tool, to define a new concrete tool.
"""

from argparse import _ArgumentGroup, SUPPRESS
from pathlib import Path
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'head'


class HeadTool(Tool):
    """Show the first *n* (default 5) source lines of the first cell of each notebook.
    If *n* is negative, show the last *n* source lines of the last cell.

    It overrides:

    * ``config_tool_args_parsing()`` to configure parser for tool-specific arguments
    * ``print_tool_args()`` to print tool-specific arguments (used in verbose mode)
    * ``process_nb()`` to process one notebook
    """

    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            description='Show head or tail of Jupyter notebooks.',
            action=TOOL
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Show head of notebook.

        :param nb: notebook to show head of
        :param nb_path: notebook's path
        :return: empty result
        """
        if nb.cells:
            source = ''
            if self._args.number >= 0:
                if nb.cells[0].source:
                    source = nb.cells[0].source.split('\n')[:self._args.number]  # list of first n source lines
            else:
                if nb.cells[-1].source:
                    source = nb.cells[-1].source.split('\n')[self._args.number:]  # list of last n source lines
            if source:
                print('\n'.join(source))

        return []  # no notebooks produced

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        group.add_argument('-#', '--number', type=int, default=SUPPRESS,
                           help='number of head/tail lines to show of first/last cell; < 0 for tail' +
                                ' (default: {})'.format(self._args.number))

    def print_tool_args(self) -> None:
        print('  Show {0} {1} source lines of {0} cell'.format(
            'first' if self._args.number >= 0 else 'last',
            abs(self._args.number)
        ))


def main(cli_args: Optional[List[str]] = None) -> int:
    return HeadTool().main(cli_args)


if __name__ == "__main__":
    import sys
    sys.exit(main())
