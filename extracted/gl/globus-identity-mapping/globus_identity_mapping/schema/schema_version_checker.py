from __future__ import annotations

import sys
import typing as t
from collections import UserDict

import marshmallow as ma

_message = (
    'The endpoint does not recognize doc {} "{}". Either your '
    "client is misconfigured or the service requires an update to "
    "support it."
)


def _doc_version_error(data_type: str) -> str:
    return _message.format("version", data_type)


def _doc_type_error(data_type: str) -> str:
    return _message.format("type", data_type)


def _do_prefixes_match(s1: str, s2: str, delim: str = "#") -> bool:
    fields1 = s1.split(delim)
    fields2 = s2.split(delim)

    # For our use case, an empty prefix (doc type) is not legal and so we
    # can safely say they do not match
    if len(fields1) == 0 or len(fields1[0]) == 0:
        return False
    if len(fields2) == 0 or len(fields2[0]) == 0:
        return False
    return fields1[0] == fields2[0]


def verify_schema_version(data_type_in: str, data_type_expected: str) -> None:
    # Simple case, exact match
    if data_type_in == data_type_expected:
        return
    # doc type is not recognized
    if not _do_prefixes_match(data_type_in, data_type_expected):
        raise ma.ValidationError(_doc_type_error(data_type_in))
    raise ma.ValidationError(_doc_version_error(data_type_in))


_K = t.TypeVar("_K", bound=str)
_V = t.TypeVar("_V", bound=ma.Schema)

if sys.version_info < (3, 9):
    if t.TYPE_CHECKING:
        TypedUserDict = UserDict[_K, _V]
    else:
        TypedUserDict = UserDict

    class version_safe_type_schemas(TypedUserDict):
        def __getitem__(self, key: _K) -> _V:
            # Simple case, key exists
            if key in self.data:
                return self.data[key]
            verify_schema_version(key, list(self.data.keys())[0])
            raise KeyError(key)

else:

    class version_safe_type_schemas(UserDict[_K, _V]):
        """Doc type and version checking for marshmallow OneOfSchema

        marshamallow OneOfSchema uses the dict field type_schemas
        to demarshal polymorphic schema. This class behaves the same
        as type_schemas with the added benefit of errors messages more
        specific to the type of error (wrong doc type or version).

        Note: We do assume that the doc_type's in type_schema are all
        identical, so we just the first key as the prefix to check.
        """

        def __getitem__(self, key: _K) -> _V:
            # Simple case, key exists
            if key in self.data:
                return self.data[key]
            verify_schema_version(key, list(self.data.keys())[0])
            raise KeyError(key)
