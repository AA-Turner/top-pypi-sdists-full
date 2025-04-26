"""
Functions for notebook reading and writing

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import sys
from argparse import Namespace
from pathlib import Path
from typing import List, Union

import nbformat
from nbformat import NotebookNode


def read_nb(nb_path: Path, args: Namespace) -> Union[None, NotebookNode]:
    """Read notebook from given path, and return it.
    Uses ``args.debug``: in debug mode, a read error results in an exception, else it returns ``None``.

    :param nb_path: path to read from
    :param args: to check debug mode
    :return: notebook read from ``nb_path`` or None if reading failed and not ``args.debug``
    """
    try:
        with nb_path.open(encoding='utf-8') as nb_file:
            nb = nbformat.read(nb_file, as_version=4)
    except Exception as e:
        e_name = type(e).__name__
        print('Reading of "{}" failed ({}):\n  {}'.format(nb_path.name, e_name, e), file=sys.stderr)
        if args.debug:
            print('  Tried to read notebook from file:', nb_path.resolve(), file=sys.stderr)
            raise
        else:
            return None

    return nb


def write_nb(nb: NotebookNode, nb_path: Path, args: Namespace) -> Union[None, bool]:
    """Write given notebook to given path.
    Uses ``args.debug``: in debug mode, a write error results in an exception, else it returns ``None``.

    :param nb: notebook to be written
    :param nb_path: path to write to
    :param args: to check debug mode
    :return:
    """
    try:
        with nb_path.open('w', encoding='utf-8') as nb_file:
            nbformat.write(nb, nb_file)
    except Exception as e:
        e_name = type(e).__name__
        print('Writing of "{}" failed ({}):\n  {}.'.format(nb_path.name, e_name, e), file=sys.stderr)
        if args.debug:
            print('  Tried to write notebook to file:', nb_path.resolve(), file=sys.stderr)
            raise
        else:
            return

    return True


def cell_lines(cell: NotebookNode) -> List[str]:
    """Return list of source lines for given cell.

    :param cell: cell whose source lines to return as list
    :return: list of source lines in cell
    """
    if cell.source:
        lines = cell.source.split('\n')
    else:
        lines = []

    return lines
