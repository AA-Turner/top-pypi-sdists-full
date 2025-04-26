"""
Tool nbvalidate

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import sys
from argparse import _ArgumentGroup
from pathlib import Path
from typing import Optional, List

from nbformat import NotebookNode

from nbtoolbelt.processing import ProcessingResultType
from nbtoolbelt.toolbaseapp import Tool
from nbtoolbelt.validating import validate_nb

TOOL = 'validate'


class ValidateTool(Tool):
    """Validate each notebook, and report the validation results.
    """

    def __init__(self) -> None:
        super().__init__(
            name='nb' + TOOL,
            action=TOOL,
            description="""Validate Jupyter notebooks."""
        )

    def process_nb(self, nb: NotebookNode, nb_path: Path) -> ProcessingResultType:
        """Validate notebook nb.

        :param nb: notebook to validate
        :param nb_path: path to ``nb``
        :return: empty result
        """
        valid = validate_nb(nb, getattr(self._args, 'assert'))

        if not valid or self._args.verbose:
            print('{} notebook structure is {}'.format(nb_path.name, 'valid' if valid else 'INVALID'))
        self._aggregate['outputs'][-1]['valid'] = valid

        return []

    def config_tool_args_parsing(self, group: _ArgumentGroup) -> None:
        pass

    def print_tool_args(self) -> None:
        print('  Assert mode: {}'.format(getattr(self._args, 'assert')))


def main(cli_args: Optional[List[str]] = None) -> int:
    return ValidateTool().main(cli_args)


if __name__ == "__main__":
    sys.exit(main())
