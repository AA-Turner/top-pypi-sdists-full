from __future__ import annotations

from typing import Any, Mapping, Sequence, Union

import pyarrow as pa

__all__ = ["TJSON", "pyarrow_json_type", "is_pyarrow_json_type", "JSON"]

TJSON = Union[None, str, int, float, bool, Sequence["TJSON"], Mapping[str, "TJSON"]]
JSON = Union[None, str, int, float, bool, Sequence, Mapping[str, object]]


class _JSONType(pa.ExtensionType):  # pyright: ignore[reportUntypedBaseClass]
    # Implementation of https://arrow.apache.org/docs/format/CanonicalExtensions.html#json
    def __init__(self):
        super().__init__(pa.large_utf8(), "arrow.json")

    def __eq__(self, other: Any):
        return isinstance(other, _JSONType)

    def __hash__(self):
        return hash(repr(self))

    def __arrow_ext_serialize__(self):
        # since we don't have a parameterized type, we don't need extra
        # metadata to be deserialized
        return b""

    @classmethod
    def __arrow_ext_deserialize__(cls, storage_type: pa.DataType, serialized: bytes):
        # return an instance of this subclass given the serialized
        # metadata.
        return _JSON_TYPE


_JSON_TYPE = _JSONType()

try:
    # If a json type is already registered, unregister it -- we'll use our own
    pa.unregister_extension_type("arrow.json")
except pa.ArrowKeyError:
    pass

pa.register_extension_type(_JSON_TYPE)


def pyarrow_json_type() -> pa.ExtensionType:
    return _JSON_TYPE


def is_pyarrow_json_type(x: pa.DataType):
    return getattr(x, "extension_name", None) == "arrow.json"
