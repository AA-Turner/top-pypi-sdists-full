from __future__ import annotations

import json as _json
from typing import (
    Any,
    ClassVar,
    Type,
    cast,
)

import pyarrow as pa

from chalk._gen.chalk.arrow.v1 import arrow_pb2 as pb
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.utils.json import pyarrow_json_type

from ._base import (
    _ScalarConverterBase,
    _unwrap_scalar_value,
    FeatureConverter,
)

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportReturnType=false, reportUnnecessaryCast=false, reportUnnecessaryComparison=false

try:
    import polars as pl
except ImportError:
    pl = None

def _to_json_str(value: Any) -> str:
    """Coerce a rich value to a JSON string.

    Accepts already-serialized strings (passed through unchanged), as well as
    dicts, lists, and other JSON-serializable objects (e.g. a resolver returns
    a ``dict`` for a feature whose PyArrow dtype is the JSON extension type).
    """
    if isinstance(value, str):
        return value
    return _json.dumps(value)


_JSON_EXTENSION_PB = pb.Extension(
    name="arrow.json",
    storage_type=pb.ArrowType(large_utf8=pb.EmptyMessage()),
)
_JSON_NULL_PB = pb.ScalarValue(null_value=pb.ArrowType(extension=_JSON_EXTENSION_PB))


class JsonFeatureConverter(
    _ScalarConverterBase[str, str],
    FeatureConverter[str, str],
):
    """Converter for the ``arrow.json`` PyArrow extension type.

    The logical (rich/primitive) type is ``str`` — JSON values are stored as
    strings.  The PyArrow dtype is the ``_JSONType`` extension type that wraps
    ``pa.large_utf8()``.
    """

    _rich_type_value: ClassVar[Type[str]] = str
    _primitive_type_value: ClassVar[Type[str]] = str
    _pyarrow_dtype_value: ClassVar[pa.DataType] = pyarrow_json_type()
    _proto_arrow_type: ClassVar[pb.ArrowType] = pb.ArrowType(extension=_JSON_EXTENSION_PB)
    _polars_dtype_value: ClassVar[Any] = pl.Utf8() if pl is not None else None

    _coerce_fn = staticmethod(_to_json_str)
    _arrow_coerce_fn = staticmethod(_to_json_str)

    def from_primitive_to_rich(self, value: str | None) -> str:
        if value is None:
            return cast(str, None)
        return str(value)

    def from_primitive_to_protobuf(self, value: str | pa.Scalar) -> pb.ScalarValue:
        scalar_value = _unwrap_scalar_value(value)
        if scalar_value is None or scalar_value is ...:
            return _JSON_NULL_PB
        str_val = str(scalar_value)
        return pb.ScalarValue(
            extension_value=pb.ExtensionValue(
                extension_type=_JSON_EXTENSION_PB,
                storage_value=pb.ScalarValue(large_utf8_value=str_val),
            )
        )

    def from_rich_to_protobuf(
        self,
        value: str | ellipsis | None,
        missing_value_strategy: MissingValueStrategy = "default_or_allow",
    ) -> pb.ScalarValue:
        prim = cast(str | None, self.from_rich_to_primitive(value, missing_value_strategy))
        if prim is None or prim is ...:
            return _JSON_NULL_PB
        return pb.ScalarValue(
            extension_value=pb.ExtensionValue(
                extension_type=_JSON_EXTENSION_PB,
                storage_value=pb.ScalarValue(large_utf8_value=prim),
            )
        )

    def from_pyarrow_to_protobuf(self, value: pa.Scalar) -> pb.ScalarValue:
        py_val = value.as_py()
        if py_val is None:
            return _JSON_NULL_PB
        # For extension scalars, as_py() returns the storage value (a str for large_utf8).
        str_val = str(py_val)
        return pb.ScalarValue(
            extension_value=pb.ExtensionValue(
                extension_type=_JSON_EXTENSION_PB,
                storage_value=pb.ScalarValue(large_utf8_value=str_val),
            )
        )

    def from_protobuf_to_pyarrow(self, pb_value: pb.ScalarValue) -> pa.Scalar:
        json_type = pyarrow_json_type()
        if pb_value.HasField("null_value"):
            return pa.nulls(1, type=json_type)[0]
        if pb_value.HasField("extension_value"):
            str_val = pb_value.extension_value.storage_value.large_utf8_value
            storage_scalar = pa.scalar(str_val, type=pa.large_string())
            return pa.ExtensionScalar.from_storage(json_type, storage_scalar)
        # Fallback: treat a bare large_utf8 value as JSON
        str_val = pb_value.large_utf8_value
        storage_scalar = pa.scalar(str_val, type=pa.large_string())
        return pa.ExtensionScalar.from_storage(json_type, storage_scalar)
