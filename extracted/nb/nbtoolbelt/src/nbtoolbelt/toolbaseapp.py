"""
Base class for concrete tools

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import json
import sys
from argparse import Namespace, ArgumentParser, _ArgumentGroup, SUPPRESS
from pathlib import Path
from typing import Any, Optional, List, Dict

import pandas as pd
from nbformat import NotebookNode

from .arguments import LoadConfigFile, ExtendAction, NegatableAction, TestAction
from .config import load_config
from .counting import flatten_mapping, unflatten_dict, clean_dict
from .notebook_io import read_nb, write_nb
from .printing import print_namespace
from .processing import ProcessingResultType
from .running import run_nb
from .validating import validate_nb

TOOL = 'base'

TEST = False


class Tool(object):
    """Base class for concrete tools.
    It is in itself a functional tool that copies notebooks.

    These methods are template methods:

    * ``main()``
    * ``parse_args()``
    * ``process_file()``

    Concrete tools inherit from Tool and override these (hook) methods:

    * ``__init__()`` MUST ``super()`` at begin, when overriding
    * ``config_tool_args_parsing()`` optional; to configure parser for tool-specific arguments
    * ``check_and_adjust_arguments()`` optional
    * ``print_tool_args()`` optional; to print tool-specific arguments (called only in verbose mode)
    * ``process_nb()`` compulsory; to process one notebook; MUST NOT CALL ``super()``
    * ``process_collected_data()`` optional; MUST CALL ``super()`` at begin, when overriding

    About the instance variables:
    """

    OUTPUT_HEADER = ":" * 14  # to set off file names in output

    def __init__(self,
                 name: str = 'nb' + TOOL,
                 action: str = 'copy',
                 description: str = 'Copy Jupyter notebooks.'):
        """Initialize the tool base.

        Overriding method must call ``super()`` at begin.

        :param name: the tool's name (e.g., used to find parameters in configuration files)
        :param action: verb (infinitive) describing tool's main action (usable after 'to') as help
        :param description: short text describing the tool (for usage instruction)
        """
        self._name = name
        self._description = description
        self._action = action
        # load default options from embedded configuration file
        self._args = load_config(self._name)  # type: Namespace  # TODO when to pass in verbose=True?
        # anticipated exit code; tools can set this
        self._exit_code = 0
        # dictionary with results aggregated over multiple notebooks
        # concrete tools initialize their part in __init__()
        self._aggregate = {
            'outputs': [{'file_count': 0}],  # type: List[Dict[str, Any]]
            # outputs[0] is overall; outputs[i] for i > 0 is per notebook argument
            # outputs[0].file_count == number of notebook files fully processed so far
        }

    def tool_name(self) -> str:
        """Get the tool's name.

        :return: the tool's name
        """
        return self._name

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Process notebook nb.

        Can update ``self._aggregate``.

        Hook method to be overridden in concrete tools.
        Overriding method must NOT call ``super()``.


        .. note:: **Modifies**: ``nb``, ``self._aggregate``

        :param nb: notebook to process
        :param nb_path: path to ``nb``
        :return: sequence of resulting (notebook, notebook-path) pairs
        """
        # Copy notebook
        print('Copying: {}'.format(nb_path.name))

        # set up destination path
        if self._args.inplace:
            nb_result_path = nb_path
        else:
            nb_result_path = nb_path.with_name(nb_path.stem + '-copy' + nb_path.suffix)

        return [(nb, nb_result_path)]

    def process_file(self, nb_path: Path) -> None:
        """Process one file, given by its path.

        .. note:: **Modifies**: ``self._aggregate``

        :param nb_path: path of file to process
        :return: exit code
        """
        # read the notebook
        nb = read_nb(nb_path, self._args)
        if nb is None:
            self._exit_code = 1
            return

        # process the notebook
        try:
            # validate the notebook (if requested and it makes sense)
            if self._args.validate and self._name != 'nbvalidate':
                valid = validate_nb(nb, getattr(self._args, 'assert'))
                if not valid:
                    print('Notebook is INVALID')

            # run the notebook (if requested and it makes sense)
            if self._args.run and self._name not in {'nbvalidate', 'nbrun', 'nbhead'}:
                run_nb(nb, self._args)

            processing_results = self.process_nb(nb, nb_path)  # type: ProcessingResultType
        except Exception as e:
            e_name = type(e).__name__
            print('Processing of "{}" failed ({}):\n  {}'.format(nb_path.name, e_name, e), file=sys.stderr)
            if self._args.debug:
                print('  While processing notebook from file:', nb_path.resolve(), file=sys.stderr)
                raise
            else:
                self._exit_code = 1
                return

        # write all resulting notebook files that were returned in processing_results
        if processing_results:
            if self._args.write_files:
                written = set()

                for res_nb, res_nb_path in processing_results:
                    if write_nb(res_nb, res_nb_path, self._args) is None:
                        self._exit_code = 1
                        return
                    written.update({res_nb_path.name})

                if self._args.verbose:
                    print('  Files written: {}'.format(written))
            else:
                print('No file{} written'.format('' if len(processing_results) == 1 else 's'))

    def process_collected_data(self) -> None:
        """Process outputs collected from all processed notebooks.

        Hook method to be overridden in concrete tools.
        Overriding method must call ``super()`` at begin.
        """
        # accumulate int values for all files
        data = [flatten_mapping(d) for d in self._aggregate['outputs'][1:]]
        if data:
            df = pd.DataFrame(data)
            statistics = df.describe(include='all')
            # append row with total for each numeric column
            sums = df.sum(numeric_only=True)
            sums.name = 'total'
            statistics = pd.concat([statistics, sums.to_frame().T])
            # update the aggregate entry of outputs (item 0)
            self._aggregate['outputs'][0].update(clean_dict(unflatten_dict(statistics.to_dict())))

    def write_output(self) -> None:
        """Write accumulated output to JSON.
        """
        fp = Path(self._args.output_json)
        if self._args.debug:
            print('Writing JSON output to:', fp)
        try:
            with fp.open('w', encoding='utf-8') as json_file:
                json.dump(self._aggregate['outputs'], json_file, indent=2, sort_keys=True)
        except Exception as e:
            print('Could not write JSON output for {} to: {}'.format(self._name, fp), file=sys.stderr)
            print('  {}: {}'.format(type(e).__name__, e), file=sys.stderr)
            # TODO should this exit with exit code > 0?
            if self._args.debug:
                raise

    def parser_with_common_arguments(self) -> ArgumentParser:
        """Create argument parser and add common arguments to it.

        :return: the pre-configured parser
        """
        parser = ArgumentParser(
            prog='nbtb ' + self._name[2:],
            description=self._description,
            add_help=True,
        )

        parser.add_argument('notebooks', metavar='NB.ipynb', type=str, nargs='*',
                            action=ExtendAction, default=SUPPRESS,
                            help='notebooks to ' + self._action)

        # TODO reconsider meaning of verbose and quiet together
        parser.add_argument('-v', '--verbose',
                            action=NegatableAction, default=SUPPRESS,
                            help='verbose mode produces extra output' +
                                 ' (default: {})'.format(self._args.verbose))
        parser.add_argument('-q', '--quiet',
                            action=NegatableAction, default=SUPPRESS,
                            help='quiet mode produces less output' +
                                 ' (default: False)'.format(self._args.quiet))
        parser.add_argument('--assert', action=NegatableAction,
                            help='assert mode: when processing fails, abort with exit code 1' +
                                 ' (default: {})'.format(getattr(self._args, 'assert')))
        parser.add_argument('--validate', action=NegatableAction,
                            help='validate notebook before processing' +
                                 ' (default: {})'.format(self._args.validate))
        parser.add_argument('--run', action=NegatableAction,
                            help='run notebook before processing' +
                                 ' (default: {})'.format(self._args.run))
        parser.add_argument('--inplace',
                            action=NegatableAction, dest='inplace', default=SUPPRESS,
                            help='replace original notebooks with processing result' +
                                 ' (default: {})'.format(self._args.inplace))
        parser.add_argument('--write-files', action=NegatableAction,
                            help='do write result files' +
                                 ' (default: {})'.format(self._args.write_files))
        parser.add_argument('-n', action='store_false', dest='write_files', default=SUPPRESS,
                            help='short for --no-write-files: '
                                 'do processing but do not write result files (dry run)')
        parser.add_argument('--config',
                            action=LoadConfigFile, type=Path, const=self._name, default=SUPPRESS,
                            metavar='FILE.json',
                            help='read configuration from FILE.json (in JSON)')
        parser.add_argument('--output-json',
                            action='store', metavar='FILE.json',
                            help='write statistical output to FILE.json')
        parser.add_argument('-d', '--debug',
                            action='store_true',
                            help='debug mode produces diagnostic output (default: False)')
        if TEST:
            parser.add_argument('--test',
                                action=TestAction, nargs='?', const='my_const', default=0,
                                choices=['a', 'b'], required=True, metavar='TEST', dest='my_dest',
                                help="this option prints the action arguments")

        return parser

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        """Add argument configurations that are tool specific to the given argument group.

        Hook method to be overridden in concrete tools.

        :param group: argument group to add into
        """
        pass

    def check_and_adjust_arguments(self):
        """Do tool-specific checks and adjustments of parsed arguments.

        Hook method to be overridden in concrete tools.
        """
        pass

    def print_tool_args(self) -> None:
        """Print tool-specific arguments; used especially in verbose mode.
        Indent the lines by 2 spaces.

        Hook method to be overridden in concrete tools.
        """
        pass

    def parse_args(self, arguments: List[str]) -> None:
        """Configure an argument parser and parse the command-line arguments,
        updating the namespace with the parsed arguments.

        .. note:: **Modifies**: ``self._args``

        :param arguments: list of arguments on command line
        """
        # set up argument parser
        parser = self.parser_with_common_arguments()

        # add tool specific arguments
        group = parser.add_argument_group('optional arguments specific for tool \'{}\''.format(self._name[2:]))
        self.config_tool_args_parsing(group)

        # parse arguments
        self._args = parser.parse_args(arguments, self._args)

        # do tool-specific checking and adjusting of parsed arguments
        self.check_and_adjust_arguments()

        if self._args.debug:
            print_namespace(self._args, 'All option settings')

        if self._args.inplace:
            print('Replacing original notebooks')
        if not self._args.write_files:
            print('Dry run (no files written)')

        if self._args.verbose:
            print('Options for {}:'.format(self._name))
            self.print_tool_args()

    def main(self, cli_args: Optional[List[str]] = None) -> int:
        """Main entry point.
        Processes all files in ``args.notebooks``, returning an exit code (0 = success).

        Can set ``self._exit_code`` to signal abortion.

        :param cli_args: list of command-line arguments (None when used as independent script)
        """
        if cli_args is None:
            # independent script; pick up command-line arguments, dropping program name
            cli_args = sys.argv[1:]

        # parse arguments into namespace self._args
        try:
            self.parse_args(cli_args)
            # TODO: transfer options (incl. e.g. freq) to JSON output: self._aggregate['outputs'][0]
            # TODO: could be tool specific!
        except Exception as e:
            print('Argument parsing failed: {}'.format(e), file=sys.stderr)
            if getattr(getattr(self, '_args'), 'debug', False):
                raise e
            else:
                self._exit_code = 1
                return self._exit_code

        # check if all files exist
        for fn in self._args.notebooks:
            if not Path(fn).exists():
                print("File not found: {}".format(fn), file=sys.stderr)
                self._exit_code = 1
                return self._exit_code

        # process all notebook arguments
        for fn in self._args.notebooks:
            nb_path = Path(fn)
            self._aggregate['outputs'].append({"file_name": nb_path.name})  # TODO: check typing

            # print header if more than one file, or in verbose mode
            if (len(self._args.notebooks) > 1 or self._args.verbose) and not self._args.quiet:
                # print file names with colons (imitating nbshow from nbdime)
                print(self.OUTPUT_HEADER)
                print(nb_path.resolve() if self._args.debug else nb_path.name)
                print(self.OUTPUT_HEADER)

            # process the file
            self.process_file(nb_path)

            if self._exit_code > 0:
                break

            self._aggregate['outputs'][0]['file_count'] += 1

        self.process_collected_data()

        if self._args.output_json:
            self.write_output()

        file_count = self._aggregate['outputs'][0]['file_count']
        if self._args.verbose:
            print("\nNotebooks processed: {}".format(file_count))

        return self._exit_code


def main(cli_args: Optional[List[str]] = None) -> int:
    return Tool().main(cli_args)


if __name__ == "__main__":
    sys.exit(Tool().main())
