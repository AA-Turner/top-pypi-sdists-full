from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from operator import attrgetter
from typing import Any, Literal, Mapping, overload
from urllib.parse import quote

__all__ = ['pct_encode', 'URITemplate']

reserved_characters = b"!#$%&'()*+,/:;=?@[]"

# Find % character that isn't in a pct-encoded triplet
pct_not_encoded_pattern = re.compile(r'%(?![0-9a-fA-F]{2})')

# Accept zero-length variables. This is not in the RFC
expression_pattern = re.compile(r'\{([+#]?)(.*?)\}')


def pct_encode(a: str, *, reserved_expansion=False) -> str:
    '''
    Percent-Encoding based on RFC 3986
    https://datatracker.ietf.org/doc/html/rfc3986#section-2.1
    '''
    result = quote(a, safe=reserved_characters if reserved_expansion else b'', encoding='utf-8', errors='replace')
    # RFC 6570 Reserved Expansion only accepts % in pct-encoded triplets
    return pct_not_encoded_pattern.sub('%25', result) if reserved_expansion else result


@dataclass
class Variable:
    operator: str
    variable: str
    start: int
    end: int


class URITemplate(str):
    '''
    RFC 6570 URI Template (Levels 1 and 2)
    https://datatracker.ietf.org/doc/html/rfc6570
    '''

    variables: defaultdict[str, list[Variable]]

    def __new__(cls, a: str) -> URITemplate:
        self = super().__new__(cls, a)

        self.variables = defaultdict(list)

        for exp in expression_pattern.finditer(self):
            operator = exp.group(1)
            variable = exp.group(2)
            start, end = exp.span()
            self.variables[variable].append(Variable(operator, variable, start, end))

        return self

    @overload
    def expand(self, values: Mapping[str, Any], *, partial: Literal[False] = False) -> str:
        ...

    @overload
    def expand(self, values: Mapping[str, Any], *, partial: Literal[True] = True) -> URITemplate:
        ...

    @overload
    def expand(self, values: Mapping[str, Any], *, partial: bool = False) -> str | URITemplate:
        ...

    def expand(self, values: Mapping[str, Any], *, partial=False) -> str | URITemplate:
        result = self[:]

        if partial:
            vars = chain.from_iterable(self.variables.get(v, ()) for v in values)
        else:
            vars = chain.from_iterable(self.variables.values())

        for v in sorted(vars, key=attrgetter('start'), reverse=True):
            value = values.get(v.variable)
            if value is None:
                if not partial:
                    result = result[: v.start] + result[v.end :]
                continue

            value = str(value)

            if v.operator == '+':
                value = pct_encode(value, reserved_expansion=True)
            elif v.operator == '#':
                value = '#' + pct_encode(value, reserved_expansion=True)
            else:
                value = pct_encode(value)

            result = result[: v.start] + value + result[v.end :]

        return URITemplate(result) if partial else result
