"""
Functions for counting elements in Jupyter notebooks

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import Namespace
from collections import defaultdict
from typing import Any, Tuple, Dict, Mapping, Callable

import numpy as np
from nbformat import NotebookNode

# TODO these should also be easily available elsewhere, e.g. in cleaning
# TODO consider which can be turned into a frozenset
# TODO consider putting these in the embedded config file
REQUIRED_NB_FIELDS = {"metadata", "nbformat_minor", "nbformat", "cells"}
REQUIRED_NB_METADATA_FIELDS = {"kernelspec", "language_info"}
CELL_TYPES = ('markdown', 'code', 'raw',)
REQUIRED_CELL_FIELDS = {
    'markdown': {"cell_type", "metadata", "source"},
    'code': {"cell_type", "metadata", "source", "execution_count", "outputs"},
    'raw': {"cell_type", "metadata", "source"}
}
OPTIONAL_CELL_FIELDS = {
    'markdown': {"attachments"},
    'code': set(),
    'raw': {"attachments"}
}
OPTIONAL_OUTPUT_TYPES = {
    'execute_result': {'data', 'metadata', 'execution_count'},
    'stream': {'name', 'text'},
    'display_data': {'data', 'metadata', },
    'error': {'ename', 'evalue', 'traceback'},
}

# TODO replace 'sources' by 'source', because that is the field name in the JSON file
#: Fields used in the dictionary returned by ``nb_cell_stats()``.
CELL_STATISTICS = (
    'cell_types',  #: cell type counts
    'sources',  #: cell sources counts
    'cell_metadata',  #: cell metadata counts, including separate ``tags``
    'cell_attachments',  #: cell attachment MIME type counts, and total
    'code_execution',  #: code cell execution count statistics
    'code_outputs',  #: code cell counts per output_type, subcounts per ``stream`` and ``error``, and total
    'cell_extra',  #: counts for extra (unknown) fields in cells
)

# dictionary keys for source statistics
EMPTY_SOURCES = 'total empty sources'
SOURCE_LINES = 'total source lines'
SOURCE_WORDS = 'total source words'
SOURCE_CHARS = 'total source chars'
EMPTY_SOURCES_MD = 'markdown empty sources'
SOURCE_LINES_MD = 'markdown source lines'
SOURCE_WORDS_MD = 'markdown source words'
SOURCE_CHARS_MD = 'markdown source chars'
EMPTY_SOURCES_CODE = 'code empty sources'
SOURCE_LINES_CODE = 'code source lines'
SOURCE_WORDS_CODE = 'code source words'
SOURCE_CHARS_CODE = 'code source chars'
EMPTY_SOURCES_RAW = 'raw empty sources'
SOURCE_LINES_RAW = 'raw source lines'
SOURCE_WORDS_RAW = 'raw source words'
SOURCE_CHARS_RAW = 'raw source chars'

# dictionary keys for code cell outputs statistics
EMPTY_OUTPUTS = 'code cells without outputs'
TOTAL_OUTPUT_COUNT = 'total output count'

# dictionary keys for code_execution cell statistics
EMPTY_EXEC_COUNT = 'not executed'
MAX_EXEC_COUNT = 'maximum In[#]'
LAST_EXEC_COUNT_IN_ORDER = 'executed in linear order'
EXECUTED = 'executed'
NOT_EXEC_IN_ORDER = 'not executed in linear order'


def count_source(source: str) -> Tuple[int, int, int]:
    """Count number of non-blank lines, words, and non-whitespace characters.

    :param source: string to count
    :return: number of non-blank lines, words, and non-whitespace characters
    """
    lines = [line for line in source.split('\n') if line and not line.isspace()]
    words = source.split()
    chars = ''.join(words)

    return len(lines), len(words), len(chars)


def nb_metadata(nb: NotebookNode) -> Dict[str, Any]:
    """Summarize notebook global metadata.

    :param nb: notebook to inspect
    :return: dictionary with format, kernel, and language info
    """
    result = {'format version': '{:1d}.{:1d}'.format(nb.get('nbformat', 1), nb.get('nbformat_minor', 0))}
    if 'kernelspec' in nb.metadata:
        result['kernel'] = nb.metadata.kernelspec.name
    if 'language_info' in nb.metadata:
        l_i = nb.metadata.language_info
        result['language'] = l_i.name + ' ' + l_i.version
    return result


def nb_extra_fields(nb: NotebookNode) -> Dict[str, int]:
    """Extract extra global fields in notebook.

    :param nb: notebook to inspect
    :return: list of extra fields (not set, because that is not JSON serializable)
    """
    return {key: 1 for key in nb.keys() if key not in REQUIRED_NB_FIELDS}


def nb_other_metadata(nb: NotebookNode) -> Dict[str, int]:
    """Extract other global metadata fields in notebook.

    :param nb: notebook to inspect
    :return: set of global metadata fields other than required
    """
    return {key: 1 for key in nb.metadata.keys() if key not in REQUIRED_NB_METADATA_FIELDS}


def nb_cell_stats(nb: NotebookNode, args: Namespace = None) -> Dict[str, Dict[str, int]]:
    """Count occurrences of various elements in notebook cells.

    If ``args`` is not ``None``, then the following boolean arguments are used
    (if present; absent is interpreted as ``False``):

    * sources
    * metadata
    * tags
    * code
    * streams
    * errors

    If ``args`` is ``None``, then all statistics are gathered.

    :param nb: notebook to inspect
    :param args: namespace with arguments; if None, count everything
    :return: dictionary of dictionaries with counts per section;
        each section has its own key; see CELL_STATISTICS
    """
    # process the notebook cells
    result = {key: defaultdict(int) for key in CELL_STATISTICS}
    all_executed_in_order = True  # whether all code cells so far were executed in order

    # traverse all cells and gather statistics
    for index, cell in enumerate(nb.cells):  # index can be used for debug output
        result['cell_types']['total cell count'] += 1  # count all cells
        ct = cell.cell_type
        result['cell_types'][ct] += 1  # count each cell type

        # compute source statistics
        empty_cell = True  # in case of missing source (should not happen)
        if getattr(args, 'sources', False):
            lines, words, chars = count_source(cell.source)  # cell.source should always be present
            empty_cell = chars == 0
            if empty_cell:
                result['sources'][EMPTY_SOURCES] += 1
                if ct == 'markdown':
                    result['sources'][EMPTY_SOURCES_MD] += 1
                elif ct == 'code':
                    result['sources'][EMPTY_SOURCES_CODE] += 1
                elif ct == 'raw':
                    result['sources'][EMPTY_SOURCES_RAW] += 1
            if chars:
                result['sources'][SOURCE_LINES] += lines
                result['sources'][SOURCE_WORDS] += words
                result['sources'][SOURCE_CHARS] += chars
                if ct == 'markdown':
                    result['sources'][SOURCE_LINES_MD] += lines
                    result['sources'][SOURCE_WORDS_MD] += words
                    result['sources'][SOURCE_CHARS_MD] += chars
                elif ct == 'code':
                    result['sources'][SOURCE_LINES_CODE] += lines
                    result['sources'][SOURCE_WORDS_CODE] += words
                    result['sources'][SOURCE_CHARS_CODE] += chars
                elif ct == 'raw':
                    result['sources'][SOURCE_LINES_RAW] += lines
                    result['sources'][SOURCE_WORDS_RAW] += words
                    result['sources'][SOURCE_CHARS_RAW] += chars

        # count each metadata key
        for attr in cell.metadata:  # cell.metadata should always be present
            if args is None or getattr(args, 'metadata', False) or (getattr(args, 'tags', False) and attr == 'tags'):
                result['cell_metadata'][attr] += 1

        # count each tag in tags metadata
        if (args is None or getattr(args, 'tags', False)) and 'tags' in cell.metadata:
            for tag in cell.metadata.tags:
                result['cell_metadata']['tag ' + tag] += 1

        # count each attachment mime type
        if 'attachments' in cell and getattr(args, 'attachments', False):
            result['cell_attachments']['total count of cells with attachments'] += 1
            for attachment in cell.attachments.values():
                for key in attachment:
                    result['cell_attachments']['total attachments count'] += 1
                    result['cell_attachments'][key] += 1

        if ct == 'code':  # process code cell
            ec = cell.get('execution_count')
            if type(ec) is int:
                result['code_execution'][EXECUTED] += 1
                # update maximum execution count
                if ec > result['code_execution'][MAX_EXEC_COUNT]:
                    result['code_execution'][MAX_EXEC_COUNT] = ec
                # update whether all executed in order
                if all_executed_in_order and ec == result['code_execution'][LAST_EXEC_COUNT_IN_ORDER] + 1:
                    result['code_execution'][LAST_EXEC_COUNT_IN_ORDER] = ec
                elif empty_cell:
                    pass  # ignore; should not happen; but nbconvert --execute can produce this
                else:
                    all_executed_in_order = False
                    result['code_execution'][NOT_EXEC_IN_ORDER] += 1
            else:  # it should be None
                result['code_execution'][EMPTY_EXEC_COUNT] += 1
                if not empty_cell:
                    all_executed_in_order = False
                    result['code_execution'][NOT_EXEC_IN_ORDER] += 1

            # process outputs of code cell (should be empty if ec is None)
            if not cell.outputs:  # empty code output
                result['code_outputs'][EMPTY_OUTPUTS] += 1
            for output in cell.outputs:
                outputs = getattr(args, 'outputs', False)
                if args is None or outputs:
                    result['code_outputs'][TOTAL_OUTPUT_COUNT] += 1
                ot = output['output_type']
                streams = getattr(args, 'streams', False)
                errors = getattr(args, 'errors', False)
                if args is None or outputs or (streams and ot == 'stream') or (errors and ot == 'error'):
                    result['code_outputs'][ot] += 1
                if (args is None or streams) and ot == 'stream':
                    result['code_outputs'][ot + ' ' + output['name']] += 1
                if (args is None or errors) and ot == 'error':
                    result['code_outputs'][ot + ' ' + output.ename] += 1

        # count non-standard fields in cells
        for field in cell:
            if field not in REQUIRED_CELL_FIELDS[ct].union(OPTIONAL_CELL_FIELDS[ct]):
                result['cell_extra'][field] += 1

    # result['code_execution'][LAST_EXEC_COUNT_IN_ORDER] is a special case
    # it can be set to 0 by inspection in if-condition above, and remain on 0
    if result['code_execution'][LAST_EXEC_COUNT_IN_ORDER] == 0:
        del result['code_execution'][LAST_EXEC_COUNT_IN_ORDER]

    return result


def nb_code_execution_stats(nb: NotebookNode) -> Dict:
    """Count number of (executed) code cells and errors in notebook.

    :param nb: notebook to inspect
    :return: dictionary with
        'code cells': number of code cells,
        'executed': number of executed cells,
        'with errors': number of execution errors
    """
    result = {  # counts
        'code cells': 0,
        'code cells with empty source': 0,
        'executed': 0,
        'with errors': 0,
    }

    # TODO: introduce constants for the keys in result?
    for cell in nb.cells:
        if cell.cell_type == 'code':
            result['code cells'] += 1
            # N.B. attribute execution_count only, and always, exists in code cells
            result['code cells with empty source'] += int(count_source(cell.source)[2] == 0)
            result['executed'] += int(cell.execution_count is not None)
            # error occurred when cell.outputs contains an output containing output_type 'error'
            result['with errors'] += int(any(output.output_type == 'error' for output in cell.outputs))

    return result


def extract_aggregate(d: Dict[str, Dict[str, Any]], attr: str = 'total',
                      convert: Callable[[Any], Any] = int) -> Dict[str, Any]:
    """Extract converted values for given attribute from nested dictionary.
    """
    return {key: convert(value[attr]) for key, value in d.items()}


PAIRING_TOKEN = ' : '  #: character sequence to combine key pairs


def pair_keys(key1: str, key2: str) -> str:
    """Pair two strings into one string,
    where key2 may also have been paired.

    :param key1: first key
    :param key2: second key
    :return: paired key
    """
    return key1 + PAIRING_TOKEN + key2


def is_key_pair(key: str) -> bool:
    """Return whether key is paired,
    that is, result of ``pair_key``.

    :param key: key to test
    :return: whether key is result of ``pair_key()``
    """
    return ' : ' in key


def unpair_key(key: str) -> Tuple[str, str]:
    """Unpair key into key1, key2 such that
    key1 is not a pair, and ``pair_keys(key1, key2) == key``.

    .. note:: **Assumption**: ``is_key_pair(key)``

    :param key: key to split
    :return: key1, key2 where ``pair_keys(key1, key2) == key``
    """
    i = key.find(PAIRING_TOKEN)
    if i < 0:
        raise ValueError('Pairing token ("{}") missing'.format(PAIRING_TOKEN))
    else:
        return key[:i], key[i + len(PAIRING_TOKEN):]


def flatten_mapping(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    """Return recursively flattened mapping as dict.

    :param mapping: object to flatten
    :return: flattened mapping
    """
    if hasattr(mapping, 'get'):
        result = {}
        for key, value in mapping.items():
            if hasattr(value, 'get'):
                result.update({pair_keys(key, key2): value2 for key2, value2 in value.items()})
            else:
                result.update({key: value})
        return result
    else:
        raise ValueError('Mapping has no "get" attribute')  # return mapping


def unflatten_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Return recursively unflattened dictionary,
    that is, ``flatten_mapping(result) == d``.

    :param d: dictionary to unflatten
    :return: unflattened version of d
    """
    # all key-value pairs in d, where key == pair_keys(key1, key2)
    # with the same key1, give rise to one pair key1: { key2: value, ...}
    result = defaultdict(dict)

    for key, value in d.items():
        if is_key_pair(key):
            key1, key2 = unpair_key(key)
            result[key1].update({key2: value})
        else:
            result.update({key: value})

    # now, recursively unflatten the resulting values
    return {key: (unflatten_dict(value) if type(d) is defaultdict else value) for key, value in result.items()}


def clean_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Remove key-nan pairs and convert non-nan np types to native Python.

    :param d: dict to clean
    :return: cleaned dict
    """
    result = {}

    for key, value in d.items():
        if isinstance(value, dict):
            kv = {key: clean_dict(value)}
        elif isinstance(value, np.integer):  # TODO: check warning for np.integer
            kv = {key: int(value)}
        elif isinstance(value, float):
            if np.isnan(value):
                kv = {}
            else:
                kv = {key: float(value)}
        else:
            kv = {key: value}
        result.update(kv)

    return result
