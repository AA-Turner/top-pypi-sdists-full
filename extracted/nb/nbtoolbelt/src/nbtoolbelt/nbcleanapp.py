"""
Main for nbclean

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import _ArgumentGroup, SUPPRESS
from pathlib import Path
from typing import Optional, List, Set

from nbformat import NotebookNode

from nbtoolbelt.arguments import split_csv, NegatableAction, join_csv
from nbtoolbelt.cleaning import clean_nb
from nbtoolbelt.counting import REQUIRED_NB_METADATA_FIELDS
from nbtoolbelt.printing import print_dict
from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'clean'


class CleanTool(Tool):
    """Clean each notebook.
    """
    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            action=TOOL,
            description="""Clean Jupyter notebooks by deleting or resetting selected elements."""
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Clean notebook nb.

        .. note:: **Modifies**: ``nb``

        :param nb: notebook to clean
        :param nb_path: path to ``nb``
        :return: sequence of resulting (notebook, notebook-path) pairs
        """
        args = self._args

        # do the cleaning, and collect some statistics
        freq = clean_nb(nb, args)

        # show statistics
        if not args.quiet:
            print_dict(freq, 'Cleaning counts')
        self._aggregate['outputs'][-1].update(freq)

        # set up destination path
        if args.inplace:
            nb_clean_path = nb_path
        else:
            nb_clean_path = nb_path.with_name(nb_path.stem + args.clean_result_name + nb_path.suffix)

        if args.debug:
            print('Clean destination:', nb_clean_path)

        return [(nb, nb_clean_path)]

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        group.add_argument('-g', '--global',
                           dest='clean_notebook_metadata_fields', default=SUPPRESS, type=split_csv,
                           metavar='FIELDS',
                           help='comma-separated list of fields to remove from metadata of notebook' +
                                " (default: '{}')".format(join_csv(self._args.clean_notebook_metadata_fields)))
        group.add_argument('-m', '--metadata',
                           dest='clean_cell_metadata_fields', default=SUPPRESS, type=split_csv,
                           metavar='FIELDS',
                           help='comma-separated list of fields to remove from metadata of all cells' +
                                " (default: '{}')".format(join_csv(self._args.clean_cell_metadata_fields)))
        group.add_argument('-t', '--tags', dest='clean_tags', default=SUPPRESS, type=split_csv,
                           metavar='TAGS',
                           help='comma-separated list of tags to remove from all cells;'
                                " use '-m tags' to remove all tags" +
                                " (default: '{}')".format(join_csv(self._args.clean_tags)))
        group.add_argument('-e', '--empty-cells',
                           action=NegatableAction, dest='clean_empty_cells', default=SUPPRESS,
                           help='delete cells with empty source, i.e. with whitespace only' +
                                ' (default: {})'.format(self._args.clean_empty_cells))
        group.add_argument('-o', '--outputs',
                           action=NegatableAction, dest='clean_outputs', default=SUPPRESS,
                           help='clean all outputs from all code cells ' +
                                ' (default: {})'.format(self._args.clean_outputs))

    def check_and_adjust_arguments(self):
        args = self._args

        nmf = set(args.clean_notebook_metadata_fields)  # type: Set[str]
        if nmf:
            intersection = nmf.intersection(REQUIRED_NB_METADATA_FIELDS)
            if intersection:
                print('WARNING: {} are required notebook metadata fields'.format(intersection))
                print('  These will not be cleaned')
                nmf.difference_update(REQUIRED_NB_METADATA_FIELDS)

    def print_tool_args(self) -> None:
        args = self._args

        if args.clean_notebook_metadata_fields:
            print("  Deleting notebook metadata fields: {}".format(args.clean_notebook_metadata_fields))
        if args.clean_cell_metadata_fields:
            print("  Deleting cell metadata fields: {}".format(args.clean_cell_metadata_fields))
        if args.clean_tags:
            print("  Deleting tags: {}".format(args.clean_tags))
        if args.clean_empty_cells:
            print('  Deleting cells with empty source')
        if args.clean_outputs:
            print('  Deleting outputs from all code cells')


def main(cli_args: Optional[List[str]] = None) -> int:
    return CleanTool().main(cli_args)


if __name__ == "__main__":
    import sys
    sys.exit(main())
