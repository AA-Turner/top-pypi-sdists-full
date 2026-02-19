from collections.abc import Callable
from typing import TypeVar

from adam.utils_context import NULL

T = TypeVar('T')

NO_SORT = 0
SORT = 1
FIRST_COLUMN_ORDINAL_SORT = 2
POD_ORDINAL_DICT_SORT = 3
REVERSE_SORT = -1

def tabulize(lines: list[T],
             fn: Callable[..., T] = None,
             header: str = None,
             dashed_line = False,
             separator = ' ',
             sorted: int = NO_SORT,
             err = False,
             ctx = NULL):
    if sorted == POD_ORDINAL_DICT_SORT:
        lines.sort(key=lambda l: dict_sort_key(l))

    if fn:
        lines = list(map(fn, lines))

    if sorted == SORT:
        lines.sort()
    elif sorted == REVERSE_SORT:
        lines.sort(reverse=True)
    elif sorted == FIRST_COLUMN_ORDINAL_SORT:
        lines.sort(key=lambda l: first_column_sort_key(l, separator=separator))

    maxes = []
    nls = []

    def format_line(line: str):
        nl = []
        words = line.split(separator)
        for i, word in enumerate(words):
            nl.append(word.ljust(maxes[i], ' '))
        nls.append('  '.join(nl))

    all_lines = lines
    if header:
        all_lines = [header] + lines

    for line in all_lines:
        words = line.split(separator)
        for i, word in enumerate(words):
            lw = len(word)
            if len(maxes) <= i:
                maxes.append(lw)
            elif maxes[i] < lw:
                maxes[i] = lw

    if header:
        format_line(header)
        if dashed_line:
            nls.append(''.ljust(sum(maxes) + (len(maxes) - 1) * 2, '-'))
    for line in lines:
        format_line(line)

    table = '\n'.join(nls)
    ctx._log(table, err=err, text_color=ctx.text_color)

    return table

def dict_sort_key(l: dict[str, any], key = 'pod'):
    if l and isinstance(l, dict) and key in l:
        k = l[key]
        if (ordinal := k.split('-')[-1]).isdigit():
            return int(ordinal)

        return k

    return '-'

def first_column_sort_key(l: str, separator=','):
    if l and isinstance(l, str):
        k = l.split(separator)[0]
        if (ordinal := k.split('-')[-1]).isdigit():
            return int(ordinal)

        return k

    return '-'