from __future__ import annotations

import re
from itertools import chain
from typing import Iterable

__all__ = [
    'escape_jsonpointer',
    'unescape_jsonpointer',
    'split_jsonpointer',
    'join_jsonpointer',
    'JSONPointer',
]

# '0', or digits without a leading '0'
array_index_pattern = re.compile(r'0|[1-9][0-9]*')


def escape_jsonpointer(a: str) -> str:
    '''
    Escape a JSON Pointer (RFC 6901) reference token.
    '''
    return a.replace('~', '~0').replace('/', '~1')


def unescape_jsonpointer(a: str) -> str:
    '''
    Unescape a JSON Pointer (RFC 6901) reference token.
    '''
    return a.replace('~1', '/').replace('~0', '~')


def split_jsonpointer(pointer: str) -> tuple[str]:
    '''
    Split a JSON Pointer into its reference tokens.
    '''
    if pointer == '':
        return ()
    return tuple(unescape_jsonpointer(token) for token in pointer.lstrip('/').split('/'))


def join_jsonpointer(tokens: Iterable[str]) -> str:
    '''
    Join a sequence of JSON Pointer reference tokens.
    '''
    return '/'.join(escape_jsonpointer(token) for token in chain('', tokens))


class JSONPointer:
    '''
    RFC 6901 JSON Pointer
    https://datatracker.ietf.org/doc/html/rfc6901
    '''

    tokens: tuple[str]

    def __init__(self, pointer: str):
        self.tokens = split_jsonpointer(pointer)

    def get(self, object, default=None):
        '''
        Get the value at the pointer in the object.
        '''

        for token in self.tokens:
            if array_index_pattern.fullmatch(token):
                try:
                    object = object[int(token)]
                    continue
                except (LookupError, TypeError):
                    pass

            try:
                object = object[token]
            except (LookupError, TypeError):
                return default

        return object
