"""
Tool nbpunch

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import _ArgumentGroup, SUPPRESS
from pathlib import Path
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.arguments import split_csv, join_csv, NegatableAction, LoadSourceFile
from nbtoolbelt.counting import CELL_TYPES
from nbtoolbelt.printing import print_dict
from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.punching import punch_via_tags, PunchedNotebookProcessor, ChadsNotebookProcessor
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'punch'


class PunchTool(Tool):
    """Punch notebooks, optionally filling holes with material coming from other notebooks,
    writing the results to new notebooks.
    """

    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            description="""Punch holes in Jupyter notebooks.""",
            action=TOOL
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Punch notebook nb.

        .. note:: **Modifies**: ``nb``

        :param nb: notebook to punch
        :param nb_path: path to ``nb``
        :return: sequence of resulting (notebook, notebook-path) pairs
        """
        args = self._args
        freq = {}

        if args.tags:
            freq, nb_punched, nb_chads = punch_via_tags(nb, args)

        # set up destination paths and result
        result = []

        if args.punched:
            if not args.tags:
                freq_punched, nb_punched = PunchedNotebookProcessor(nb, args, nb_path.name).punch_nb()
                freq.update(freq_punched)
            nb_punched_path = nb_path.with_name(nb_path.stem + args.punch_punched_result_name + nb_path.suffix)
            result.append((nb_punched, nb_punched_path))

        if args.chads:
            nb_chads_path = nb_path.with_name(nb_path.stem + args.punch_chads_result_name + nb_path.suffix)
            if not args.tags:
                freq_chads, nb_chads = ChadsNotebookProcessor(nb, args, nb_chads_path.name).punch_nb()
                freq.update(freq_chads)
            result.append((nb_chads, nb_chads_path))

        # print statistics
        if not args.quiet:
            print_dict(freq, 'Punch cell statistics')
        self._aggregate['outputs'][-1].update(freq)

        return result

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        args = self._args

        group.add_argument('-t', '--tags',
                           dest='tags', type=split_csv, default=SUPPRESS,
                           metavar='TAGS',
                           help='comma-separated list of tags that trigger removal of source from cells;' +
                                " e.g. YourTurn (default: '{}')".format(join_csv(args.tags)))
        group.add_argument('-p', '--punched',
                           action=NegatableAction, default=SUPPRESS,
                           help='whether to write punched notebook' +
                                ' (default: {})'.format(args.punched))
        group.add_argument('-c', '--chads',
                           action=NegatableAction, default=SUPPRESS,
                           help='whether to write chads notebook' +
                                ' (default: {})'.format(args.chads))
        group.add_argument('-m', '--keep-marker-lines',
                           action=NegatableAction, default=SUPPRESS,
                           help='whether to keep marker lines' +
                                ' (default: {})'.format(args.keep_marker_lines))
        group.add_argument('-f', '--fill',
                           action=NegatableAction, default=SUPPRESS,
                           help='whether to fill punched holes' +
                                ' (default: {})'.format(args.fill))
        group.add_argument('-s', '--source',
                           action=LoadSourceFile, dest='punch_source', default=SUPPRESS,
                           help='source notebook for filling holes; implies --fill' +
                                ' (default: {!r})'.format(args.punch_source))
        group.add_argument('-l', '--list',
                           action=NegatableAction, default=SUPPRESS,
                           help='list marker labels and descriptions' +
                                ' (default: {})'.format(args.list))
        group.add_argument('-e', '--allow-errors',
                           action=NegatableAction, default=SUPPRESS,
                           help='continue on parsing errors in marker lines' +
                                ' (default: {})'.format(args.allow_errors))
        group.add_argument('--label-regex',
                           dest='label_regex', default=SUPPRESS,
                           help='only process marker lines whose labels match REGEX' +
                                ' (default: {!r}; empty regex matches all)'.format(args.label_regex))

    def check_and_adjust_arguments(self):
        args = self._args

        if args.punch_source:
            # --source implies --fill
            args.fill = True

        if args.tags and args.punch_source:
            raise AssertionError('Cannot use --source with --tags.')

    def print_tool_args(self) -> None:
        args = self._args

        if args.tags:
            print('  Tags that trigger punch: {}'.format(args.tags))
        else:
            if args.debug:
                print('  Markers that trigger punch:')
                for cell_type in CELL_TYPES:
                    print('    {} regex: {}'.format(cell_type, repr(args.marker_regex[cell_type])))
                print('  Marker line parsing to extract transition, label, and description:')
                for cell_type in CELL_TYPES:
                    print('    {} regex: {}'.format(cell_type, repr(args.marker_line_parsing_regex[cell_type])))
                print('  Marker transitions:')
                for transition in 'begin', 'end':
                    print('    {}: {}'.format(transition, repr(args.marker_transitions[transition])))
        print('  Writing punched notebook: {}'.format(args.punched))
        print('  Writing chads notebook: {}'.format(args.chads))
        print('  Keeping marker lines: {}'.format(args.keep_marker_lines))
        print('  Listing labels and descriptions: {}'.format(args.list))
        if args.fill:
            if args.punch_source and not args.tags:
                print('  Fill holes from source notebook: {}'.format(args.punch_source))
            else:  # no source, or using tags
                print('  Fill holes as follows:')
                for cell_type in CELL_TYPES:
                    print('    {}: {}'.format(cell_type, repr(args.filling[cell_type])))
        else:
            print('  Do not fill punched holes')
        if args.allow_errors:
            action = 'Not stopping at errors'
        else:
            action = 'Stopping at first error'
        print('  {}'.format(action))


def main(cli_args: Optional[List[str]] = None) -> int:
    return PunchTool().main(cli_args)


if __name__ == "__main__":
    import sys

    sys.exit(main())
