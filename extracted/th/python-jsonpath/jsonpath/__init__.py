# SPDX-FileCopyrightText: 2023-present James Prior <jamesgr.prior@gmail.com>
#
# SPDX-License-Identifier: MIT

from .env import JSONPathEnvironment
from .exceptions import JSONPatchError
from .exceptions import JSONPatchTestFailure
from .exceptions import JSONPathError
from .exceptions import JSONPathIndexError
from .exceptions import JSONPathNameError
from .exceptions import JSONPathSyntaxError
from .exceptions import JSONPathTypeError
from .exceptions import JSONPointerEncodeError
from .exceptions import JSONPointerError
from .exceptions import JSONPointerIndexError
from .exceptions import JSONPointerKeyError
from .exceptions import JSONPointerResolutionError
from .exceptions import JSONPointerTypeError
from .exceptions import RelativeJSONPointerError
from .exceptions import RelativeJSONPointerIndexError
from .exceptions import RelativeJSONPointerSyntaxError
from .filter import UNDEFINED
from .fluent_api import Projection
from .fluent_api import Query
from .lex import Lexer
from .match import JSONPathMatch
from .match import NodeList
from .parse import Parser
from .patch import JSONPatch
from .path import CompoundJSONPath
from .path import JSONPath
from .pointer import JSONPointer
from .pointer import RelativeJSONPointer
from .pointer import resolve

__all__ = (
    "compile",
    "CompoundJSONPath",
    "findall_async",
    "findall",
    "finditer_async",
    "finditer",
    "JSONPatch",
    "JSONPatchError",
    "JSONPatchTestFailure",
    "JSONPath",
    "JSONPathEnvironment",
    "JSONPathError",
    "JSONPathIndexError",
    "JSONPathMatch",
    "JSONPathNameError",
    "JSONPathSyntaxError",
    "JSONPathTypeError",
    "JSONPointer",
    "JSONPointerEncodeError",
    "JSONPointerError",
    "JSONPointerIndexError",
    "JSONPointerKeyError",
    "JSONPointerResolutionError",
    "JSONPointerTypeError",
    "Lexer",
    "NodeList",
    "match",
    "Parser",
    "Projection",
    "query",
    "Query",
    "RelativeJSONPointer",
    "RelativeJSONPointerError",
    "RelativeJSONPointerIndexError",
    "RelativeJSONPointerSyntaxError",
    "resolve",
    "UNDEFINED",
)


# For convenience
DEFAULT_ENV = JSONPathEnvironment()
compile = DEFAULT_ENV.compile  # noqa: A001
findall = DEFAULT_ENV.findall
findall_async = DEFAULT_ENV.findall_async
finditer = DEFAULT_ENV.finditer
finditer_async = DEFAULT_ENV.finditer_async
match = DEFAULT_ENV.match
query = DEFAULT_ENV.query
