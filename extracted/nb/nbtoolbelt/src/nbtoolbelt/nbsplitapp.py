"""
Main for nbsplit

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import copy
from argparse import _ArgumentGroup, SUPPRESS
from pathlib import Path
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.arguments import split_csv, join_csv
from nbtoolbelt.counting import REQUIRED_CELL_FIELDS
from nbtoolbelt.printing import print_dict
from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'split'


class SplitTool(Tool):
    """Split each notebook.
    """
    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            action=TOOL,
            description="""Split Jupyter notebooks into code cells and other cells."""
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Split notebook nb into markdown, code, and raw cells.

        .. note::

          **Modifies**: ``nb``

          **Side effect**: writes new notebook files

        :param nb: notebook to split
        :param nb_path: path to ``nb``
        :return: sequence of resulting (notebook, notebook-path) pairs
        """
        args = self._args

        nb_result = {}
        freq = {'total': len(nb.cells)}
        nb_result_path = {}

        # split the notebook into a part for each cell type
        for cell_type in args.split_cell_types:
            nb_result[cell_type] = copy.deepcopy(nb)  # notebook for cell type
            nb_result[cell_type].cells = [cell for cell in nb.cells if cell.cell_type == cell_type]
            freq[cell_type] = len(nb_result[cell_type].cells)

        # print statistics
        if not args.quiet:
            print_dict(freq, 'Split cell statistics')
        self._aggregate['outputs'][-1].update(freq)

        # set up destination paths
        for cell_type in args.split_cell_types:
            name = nb_path.stem + getattr(args, 'split_' + cell_type + '_result_name') + nb_path.suffix
            nb_result_path[cell_type] = nb_path.with_name(name)
            if args.debug and freq[cell_type]:
                print('Destination of {} cells:'.format(cell_type), nb_result_path[cell_type])

        # only write parts that have cells
        result = [(nb_result[cell_type], nb_result_path[cell_type])
                  for cell_type in args.split_cell_types
                  if freq[cell_type]]

        return result

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        group.add_argument('-t', '--split-cell-types', default=SUPPRESS, type=split_csv,
                           metavar='TYPES',
                           help='comma-separated list of cell types to split'
                                " (default: '{}')".format(join_csv(self._args.split_cell_types)))

    def check_and_adjust_arguments(self) -> None:
        bad = set(self._args.split_cell_types).difference(REQUIRED_CELL_FIELDS.keys())
        if bad:
            raise ValueError('Invalid cell types with -t: {}'.format(join_csv(bad)))

    def print_tool_args(self) -> None:
        print('  Split cell types: {}'.format(join_csv(self._args.split_cell_types)))


def main(cli_args: Optional[List[str]] = None) -> int:
    return SplitTool().main(cli_args)


if __name__ == "__main__":
    import sys
    sys.exit(main())
