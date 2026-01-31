from collections.abc import Callable
from typing import TypeVar

from adam.utils_context import Context

T = TypeVar('T')

NO_SORT = 0
SORT = 1
REVERSE_SORT = -1

def tabulize(lines: list[T],
             fn: Callable[..., T] = None,
             header: str = None,
             dashed_line = False,
             separator = ' ',
             sorted: int = NO_SORT,
             err = False,
             ctx: Context = Context.NULL):
    if fn:
        lines = list(map(fn, lines))

    if sorted == SORT:
        lines.sort()
    elif sorted == REVERSE_SORT:
        lines.sort(reverse=True)

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