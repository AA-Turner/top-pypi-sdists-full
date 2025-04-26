"""
Tool nbdump; dump cell sources of notebooks

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import _ArgumentGroup, SUPPRESS
from pathlib import Path
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.arguments import NegatableAction, split_csv, join_csv
from nbtoolbelt.counting import REQUIRED_CELL_FIELDS, nb_other_metadata
from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'dump'


class DumpTool(Tool):
    """Show all source lines of each notebook.
    """

    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            description='Dump cell sources of Jupyter notebooks.',
            action=TOOL
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Dump cell sources of notebook.

        :param nb: notebook to dump
        :param nb_path: notebook's path
        :return: empty result
        """
        info_prefix = self._args.dump_info_prefix
        line_indent = ' ' * self._args.dump_source_line_indent
        cell_spacing = '\n' * self._args.dump_cell_spacing

        if self._args.dump_notebook_info:
            print('{} nbformat: {:1d}.{:1d}'
                  .format(info_prefix, nb.get('nbformat', 1), nb.get('nbformat_minor', 0)), end='')
            if 'kernelspec' in nb.metadata:
                print(' | kernel: {}'.format(nb.metadata.kernelspec.name), end='')
            if 'language_info' in nb.metadata:
                l_i = nb.metadata.language_info
                print(' | language: {} {}'.format(l_i.name, l_i.version), end='')
            print(' {}'.format(info_prefix))
            print('{} cells: {}'.format(info_prefix, len(nb.cells)), end='')
            other_metadata = nb_other_metadata(nb)
            if other_metadata:
                print(' | metadata: {}'.format(join_csv(other_metadata.keys())), end='')
            print(' {}'.format(info_prefix))

        spacing = ''

        for index, cell in enumerate(nb.cells):
            ct = cell.cell_type
            if ct in self._args.dump_cell_types:
                print(spacing, end='')
                spacing = cell_spacing
                if self._args.dump_cell_info:
                    print('{} cell {}: {}'.format(info_prefix, index, ct), end='')
                    metadata = set(cell.metadata.keys())
                    metadata.discard('tags')
                    if metadata:
                        print(' | metadata: {}'.format(','.join(metadata)), end='')
                    if 'tags' in cell.metadata:
                        tags = ','.join(cell.metadata.tags)
                        print(' | tags: {}'.format(tags), end='')
                    if (ct == 'markdown' or ct == 'raw') and 'attachments' in cell:
                        print(' | attachments: {}'.format(len(cell.attachments)), end='')
                    if ct == 'code' and cell.outputs:
                        print(' | outputs: {}'.format(len(cell.outputs)), end='')
                    print(' {}'.format(info_prefix))
                if self._args.dump_sources and cell.source:
                    for line_index, line in enumerate(cell.source.split('\n')):
                        if self._args.dump_source_line_numbers:
                            print('{}{:>2}| {}'.format(line_indent, line_index + 1, line), sep='')
                        else:
                            print('{}{}'.format(line_indent, line), sep='')

        return []  # no notebooks produced

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        group.add_argument('-g', '--notebook-info',
                           action=NegatableAction, default=SUPPRESS, dest='dump_notebook_info',
                           help='show global notebook information' +
                                ' (default: {})'.format(self._args.dump_notebook_info))
        group.add_argument('-c', '--cell-info',
                           action=NegatableAction, default=SUPPRESS, dest='dump_cell_info',
                           help='show cell information' +
                                ' (default: {})'.format(self._args.dump_cell_info))
        group.add_argument('-s', '--sources',
                           action=NegatableAction, default=SUPPRESS, dest='dump_sources',
                           help='show cell sources' +
                           ' (default: {})'.format(self._args.dump_sources))
        group.add_argument('-t', '--cell-types', default=SUPPRESS, type=split_csv, dest='dump_cell_types',
                           metavar='TYPES',
                           help='comma-separated list of cell types to dump' +
                                " (default: '{}')".format(join_csv(self._args.dump_cell_types)))
        group.add_argument('-p', '--prefix',
                           default=SUPPRESS, dest='dump_info_prefix', metavar='STRING',
                           help='pre/postfix for information lines' +
                                " (default: '{}')".format(self._args.dump_info_prefix))
        group.add_argument('-i', '--indent',
                           default=SUPPRESS, type=int, dest='dump_source_line_indent', metavar='INT',
                           help='indentation level for source lines' +
                                ' (default: {})'.format(self._args.dump_source_line_indent))
        group.add_argument('-l', '--line-numbers',
                           action=NegatableAction, default=SUPPRESS, dest='dump_source_line_numbers',
                           help='show source line numbers' +
                                ' (default: {})'.format(self._args.dump_source_line_numbers))
        group.add_argument('-e', '--cell-spacing',
                           default=SUPPRESS, type=int, dest='dump_cell_spacing', metavar='INT',
                           help='number of empty lines between cells' +
                                ' (default: {})'.format(self._args.dump_cell_spacing))

    def check_and_adjust_arguments(self) -> None:
        bad = set(self._args.dump_cell_types).difference(REQUIRED_CELL_FIELDS.keys())
        if bad:
            raise ValueError('Invalid cell types with -t: {}'.format(join_csv(bad)))

    def print_tool_args(self) -> None:
        print('  Dump notebook info: {}'.format(self._args.dump_notebook_info))
        print('  Dump cell info: {}'.format(self._args.dump_cell_info))
        print('  Dump cell sources: {}'.format(self._args.dump_sources))
        print('  Dump cell types: {}'.format(join_csv(self._args.dump_cell_types)))
        print('  Prefix for information lines: {}'.format(self._args.dump_info_prefix))
        print('  Source line indentation level: {}'.format(self._args.dump_source_line_indent))
        print('  Show source line numbers: {}'.format(self._args.dump_source_line_numbers))
        print('  Cell spacing lines: {}'.format(self._args.dump_cell_spacing))


def main(cli_args: Optional[List[str]] = None) -> int:
    return DumpTool().main(cli_args)


if __name__ == "__main__":
    import sys
    sys.exit(main())
