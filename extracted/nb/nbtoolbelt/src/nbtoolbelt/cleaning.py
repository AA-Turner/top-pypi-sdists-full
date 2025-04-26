"""
Functions for cleaning

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import Namespace
from collections import defaultdict
from typing import List, Dict

from nbformat import NotebookNode

from .counting import count_source

TEST = False

# TODO split cleaning into smaller functions


def clean_nb(nb: NotebookNode, args: Namespace) -> Dict:
    """Clean fields and optionally output from notebook.

    If ``args`` is not ``None``, then the following arguments are used:

    * clean_notebook_metadata_fields (collection)
    * clean_cell_metadata_fields (collection)
    * clean_tags (collection)
    * clean_empty_cells (boolean)
    * clean_outputs (boolean)

    .. note:: **Modifies**: ``nb``

    :param nb: notebook to clean
    :param args: namespace with arguments (options)
    :return: dictionary with statistics for removed elements
    """
    freq = defaultdict(int)  # number of cleanings

    # delete notebook (global) metadata fields
    if args.clean_notebook_metadata_fields:
        for field in args.clean_notebook_metadata_fields:
            if field in nb.metadata:
                del nb.metadata[field]
                freq['global ' + field] += 1

    # delete empty cells, if desired
    n = len(nb.cells)
    if args.clean_empty_cells:
        nb.cells = [cell for cell in nb.cells if count_source(cell.source)[0]]
    if n > len(nb.cells):
        freq['empty cells'] = n - len(nb.cells)

    # traverse all cells, and delete fields
    for index, cell in enumerate(nb.cells):  # index is useful for debugging
        ct = cell.cell_type
        if TEST:
            print(ct, 'cell', index)

        # delete cell metadata fields
        if args.clean_cell_metadata_fields:
            for field in args.clean_cell_metadata_fields:
                if field in cell.metadata:
                    del cell.metadata[field]
                    freq['cell ' + field] += 1

        # delete cell tags
        if 'tags' in cell.metadata and args.clean_tags:
            removed_tags = {tag for tag in cell.metadata.tags if tag in args.clean_tags}
            for tag in removed_tags:
                freq['tag ' + tag] += 1
            clean_tags = [tag for tag in cell.metadata.tags if tag not in args.clean_tags]
            if clean_tags:
                cell.metadata.tags = clean_tags
            else:
                del cell.metadata['tags']

        # clean outputs of code cells, if requested
        if ct == 'code' and args.clean_outputs:
            if cell.outputs:
                cell.outputs = []
                freq['outputs'] += 1
            cell.execution_count = None

    return freq


def clean_code_output(nb: NotebookNode) -> None:
    """Clean all output cells and execution counts.

    .. note:: **Modifies**: ``nb``

    :param nb: notebook to clean
    """
    for cell in nb.cells:
        if 'outputs' in cell:
            cell.outputs = []
        if 'execution_count' in cell:
            cell.execution_count = None


def clean_code_metadata(nb: NotebookNode, clean: List[str]) -> None:
    """Clean metadata of code cells, by
    * removing collapsed and scrolled flags on code cells
    * removing ExecuteTime data on code cells

    .. note::

        **Modifies**: ``nb``

    :param nb: notebook to clean
    :param clean: metadata keys to clean
    """
    for cell in nb.cells:
        if cell.cell_type == 'code':
            md = cell.metadata
            for attr in clean:
                if attr in md:
                    del md[attr]


def truncate_output_streams(nb: NotebookNode, args: Namespace) -> None:
    """Limit the output cells to at most `args.limit_output` lines.

    :param nb: notebook to limit
    :param args: namespace with arguments (options)
    """
    for cell in filter(lambda c: c.cell_type == 'code', nb.cells):
        head_per_stream = defaultdict(lambda: args.streams_head)

        new_outputs = []
        for output in cell.outputs:
            if output.output_type == 'stream':
                lines_remaining = head_per_stream[output.name]

                if lines_remaining > 0:
                    text = output.text

                    breakpoint = 0
                    while lines_remaining > 0:
                        next_newline = text.find("\n", breakpoint)
                        if next_newline < 0:
                            break

                        breakpoint = next_newline + 1
                        lines_remaining -= 1

                    if lines_remaining == 0:
                        output.text = text[:breakpoint] + "\n" + args.streams_truncate_message + "\n"

                    head_per_stream[output.name] = lines_remaining
                    new_outputs.append(output)

            else:
                new_outputs.append(output)

        cell.outputs = new_outputs
