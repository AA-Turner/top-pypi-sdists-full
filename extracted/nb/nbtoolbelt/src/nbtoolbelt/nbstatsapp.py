"""
Main for nbstats

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.

Summarize Jupyter notebooks on the command line.
"""

from argparse import _ArgumentGroup, SUPPRESS
from pathlib import Path
from textwrap import dedent
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.arguments import NegatableAction
from nbtoolbelt.counting import nb_metadata, nb_other_metadata, nb_extra_fields, nb_cell_stats, extract_aggregate
from nbtoolbelt.printing import print_dict
from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'stats'


class StatsTool(Tool):
    """Collect and show a statistical summary of each notebook.
    Also compute some statistics over all notebooks.
    """

    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            description=dedent("""\
                Summarize Jupyter notebooks on stdout with statistics.
                By default summarizes all notebook data.
                Limit to specific items by passing options.
                """),
            action='summarize'
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Collect and present statistics about notebook nb.

        :param nb: notebook to count
        :param nb_path: path to ``nb``
        :return: sequence of resulting (notebook, notebook-path) pairs
        """
        args = self._args

        output = {}  # to accumulate JSON output

        # always print summary of required notebook metadata
        metadata = nb_metadata(nb)
        print_dict(metadata, 'Notebook metadata')
        output['notebook_metadata'] = metadata

        # print notebook-level optional metadata fields, if desired
        if args.metadata:
            other_metadata = nb_other_metadata(nb)
            print_dict(other_metadata, 'Other notebook metadata fields')
            output['notebook_other_metadata'] = other_metadata

        # print the notebook extra metadata, if desired
        if args.extra:
            extra_fields = nb_extra_fields(nb)
            print_dict(extra_fields, 'EXTRA NOTEBOOK FIELDS')
            output['notebook_extra_fields'] = extra_fields

        cell_stats = nb_cell_stats(nb, args)

        # print desired cell statistics
        keys = []
        if args.cell_types:
            print_dict(cell_stats['cell_types'], "Cell types")
            keys.append('cell_types')
        if args.sources:
            print_dict(cell_stats['sources'], "Cell sources")
            keys.append('sources')
        if args.metadata or args.tags:
            print_dict(cell_stats['cell_metadata'], "Cell metadata fields")
            keys.append('cell_metadata')
        if args.attachments:
            print_dict(cell_stats['cell_attachments'], "Cell attachments")
            keys.append('cell_attachments')
        if args.outputs or args.streams or args.errors:
            print_dict(cell_stats['code_outputs'], "Code cell outputs")
            keys.append('code_outputs')
        if args.execution:
            print_dict(cell_stats['code_execution'], 'Code cell execution')
            keys.append('code_execution')
        if args.extra:
            print_dict(cell_stats['cell_extra'], "EXTRA CELL FIELDS")
            keys.append('cell_extra')
        output.update({key: value for key, value in cell_stats.items() if key in keys})

        self._aggregate['outputs'][-1].update(output)

        return []

    def process_collected_data(self):
        super().process_collected_data()
        # print some aggregation results
        args = self._args

        if len(args.notebooks) <= 1:
            return

        # print header
        print('\nTotals\n======\n')

        aggregate = self._aggregate['outputs'][0]

        # print notebook-level optional metadata fields, if desired
        if args.metadata:
            other_metadata = extract_aggregate(aggregate.get('notebook_other_metadata', {}))
            print_dict(other_metadata, 'Other notebook metadata fields')

        # print the notebook extra metadata, if desired
        if args.extra:
            extra_fields = extract_aggregate(aggregate.get('notebook_extra_fields', {}))
            print_dict(extra_fields, 'EXTRA NOTEBOOK FIELDS')

        cell_stats = aggregate

        # print desired cell statistics
        if args.cell_types:
            cell_types = extract_aggregate(cell_stats.get('cell_types', {}))
            print_dict(cell_types, "Cell types")
        if args.sources:
            cell_sources = extract_aggregate(cell_stats.get('sources', {}))
            print_dict(cell_sources, "Cell sources")
        if args.metadata or args.tags:
            cell_metadata = extract_aggregate(cell_stats.get('cell_metadata', {}))
            print_dict(cell_metadata, "Cell metadata fields")
        if args.attachments:
            cell_attachments = extract_aggregate(cell_stats.get('cell_attachments', {}))
            print_dict(cell_attachments, "Cell attachments")
        if args.outputs or args.streams or args.errors:
            code_outputs = extract_aggregate(cell_stats.get('code_outputs', {}))
            print_dict(code_outputs, "Code cell outputs")
        if args.execution:
            # delete 'maximum In[#]' from collected outputs, because its statistics don't make much sense
            # TODO improve the following deletion; also: it mentions three attributes twice
            if 'code_execution' in cell_stats and 'maximum In[#]' in cell_stats['code_execution']:
                del cell_stats['code_execution']['maximum In[#]']
            code_execution = extract_aggregate(cell_stats.get('code_execution', {}))
            print_dict(code_execution, 'Code cell execution')
        if args.extra:
            cell_extra = extract_aggregate(cell_stats.get('cell_extra', {}))
            print_dict(cell_extra, "EXTRA CELL FIELDS")

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        group.add_argument('--all',
                           action=NegatableAction, dest='all_stats', default=SUPPRESS,
                           help='show all statistics' +
                           ' (default: {})'.format(self._args.all_stats)),
        group.add_argument('-c', '--cell-types',
                           action=NegatableAction, default=SUPPRESS,
                           help='count cell types' +
                           ' (default: {})'.format(self._args.cell_types))
        group.add_argument('-s', '--sources',
                           action=NegatableAction, default=SUPPRESS,
                           help='statistics for cell sources' +
                           ' (default: {})'.format(self._args.sources))
        group.add_argument('-m', '--metadata',
                           action=NegatableAction, default=SUPPRESS,
                           help='show notebook metadata and count cell metadata' +
                           ' (default: {})'.format(self._args.metadata))
        group.add_argument('-t', '--tags',
                           action=NegatableAction, default=SUPPRESS,
                           help='count individual cell tags' +
                           ' (default: {})'.format(self._args.tags))
        group.add_argument('-a', '--attachments',
                           action=NegatableAction, default=SUPPRESS,
                           help='count cell attachment MIME types' +
                           ' (default: {})'.format(self._args.attachments))
        group.add_argument('-o', '--outputs',
                           action=NegatableAction, default=SUPPRESS,
                           help='count code cell outputs' +
                           ' (default: {})'.format(self._args.outputs))
        group.add_argument('--streams',
                           action=NegatableAction, default=SUPPRESS,
                           help='count code cell output stream names' +
                           ' (default: {})'.format(self._args.streams))
        group.add_argument('-e', '--errors',
                           action=NegatableAction, default=SUPPRESS,
                           help='count code cell error names' +
                           ' (default: {})'.format(self._args.errors))
        group.add_argument('-x', '--execution',
                           action=NegatableAction, default=SUPPRESS,
                           help='statistics for code execution' +
                           ' (default: {})'.format(self._args.execution))
        group.add_argument('--extra',
                           action=NegatableAction, default=SUPPRESS,
                           help='report extra fields outside metadata' +
                           ' (default: {})'.format(self._args.extra))

    def check_and_adjust_arguments(self):
        args = self._args

        # if --all, summarize everything
        if args.all_stats:
            args.cell_types = True
            args.sources = True
            args.metadata = True
            args.tags = True
            args.attachments = True
            args.outputs = True
            args.streams = True
            args.errors = True
            args.execution = True
            args.extra = True


def main(cli_args: Optional[List[str]] = None) -> int:
    return StatsTool().main(cli_args)


if __name__ == "__main__":
    import sys
    sys.exit(main())
