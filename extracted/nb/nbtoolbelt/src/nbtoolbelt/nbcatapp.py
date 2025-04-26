"""
Main for nbcat

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import Namespace
from pathlib import Path
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.counting import nb_cell_stats, extract_aggregate
from nbtoolbelt.printing import print_dict
from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.toolbaseapp import Tool

TOOL = 'cat'


class CatTool(Tool):
    """Catenate notebooks.
    """
    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            action=TOOL,
            description="""Catenate Jupyter notebooks into one notebook."""
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Collect cells of notebook nb.

        :param nb: notebook to catenate
        :param nb_path: path to ``nb``
        :return: catenation when called on last notebook
        """
        args = self._args

        if 'result' not in self._aggregate:
            self._aggregate['result'] = nb  # catenation of all notebooks so far
            if args.inplace:
                result_path = nb_path
            else:
                result_path = nb_path.with_name(nb_path.stem + args.cat_result_name + nb_path.suffix)
            self._aggregate['result_path'] = result_path
        else:
            self._aggregate['result'].cells.extend(nb.cells)

        # collect some statistics
        namespace = Namespace()
        setattr(namespace, 'cell_types', True)
        freq = nb_cell_stats(nb, namespace)['cell_types']

        # show statistics
        if not args.quiet:
            print_dict(freq, 'Counts')
        self._aggregate['outputs'][-1].update({'cell_types': freq})

        # on last file write result
        result = []
        if self._aggregate['outputs'][0]['file_count'] + 1 == len(self._args.notebooks):
            result.append((self._aggregate['result'], self._aggregate['result_path']))

        return result

    def process_collected_data(self):
        super().process_collected_data()
        totals = extract_aggregate(self._aggregate['outputs'][0]['cell_types'])
        print_dict(totals, 'Total counts')


def main(cli_args: Optional[List[str]] = None) -> int:
    return CatTool().main(cli_args)


if __name__ == "__main__":
    import sys
    sys.exit(main())
