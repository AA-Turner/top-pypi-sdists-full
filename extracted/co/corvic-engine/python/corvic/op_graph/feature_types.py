"""Corvic feature schemas."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Final, cast, overload

from google.protobuf import struct_pb2

from corvic import orm
from corvic.op_graph.errors import OpParseError
from corvic.proto_wrapper import OneofProtoWrapper
from corvic.result import InvalidArgumentError, Ok
from corvic_generated.orm.v1 import table_pb2


@overload
def from_proto(proto: table_pb2.FeatureType) -> FeatureType: ...


@overload
def from_proto(proto: table_pb2.TextFeatureType, *, is_excluded: bool) -> Text: ...


@overload
def from_proto(
    proto: table_pb2.CategoricalFeatureType, *, is_excluded: bool
) -> Categorical: ...


@overload
def from_proto(
    proto: table_pb2.PrimaryKeyFeatureType, *, is_excluded: bool
) -> PrimaryKey: ...


@overload
def from_proto(
    proto: table_pb2.ForeignKeyFeatureType, *, is_excluded: bool
) -> ForeignKey: ...


@overload
def from_proto(
    proto: table_pb2.IdentifierFeatureType, *, is_excluded: bool
) -> Identifier: ...


@overload
def from_proto(
    proto: table_pb2.NumericalFeatureType, *, is_excluded: bool
) -> Numerical: ...


@overload
def from_proto(
    proto: table_pb2.MultiCategoricalFeatureType, *, is_excluded: bool
) -> MultiCategorical: ...


@overload
def from_proto(
    proto: table_pb2.TimestampFeatureType, *, is_excluded: bool
) -> Timestamp: ...


@overload
def from_proto(
    proto: table_pb2.EmbeddingFeatureType, *, is_excluded: bool
) -> Embedding: ...


@overload
def from_proto(
    proto: table_pb2.UnknownFeatureType, *, is_excluded: bool
) -> Unknown: ...


@overload
def from_proto(proto: table_pb2.ImageFeatureType, *, is_excluded: bool) -> Unknown: ...


def from_proto(  # noqa: C901
    proto: (
        table_pb2.FeatureType
        | table_pb2.TextFeatureType
        | table_pb2.CategoricalFeatureType
        | table_pb2.PrimaryKeyFeatureType
        | table_pb2.ForeignKeyFeatureType
        | table_pb2.IdentifierFeatureType
        | table_pb2.NumericalFeatureType
        | table_pb2.MultiCategoricalFeatureType
        | table_pb2.TimestampFeatureType
        | table_pb2.EmbeddingFeatureType
        | table_pb2.UnknownFeatureType
        | table_pb2.ImageFeatureType
    ),
    *,
    is_excluded: bool = False,
) -> FeatureType:
    """Create a FeatureType wrapper around a FeatureType protobuf message."""
    match proto:
        case table_pb2.FeatureType():
            return _from_feature_type(proto)
        case table_pb2.TextFeatureType():
            return Text(table_pb2.FeatureType(text=proto))
        case table_pb2.CategoricalFeatureType():
            return Categorical(
                table_pb2.FeatureType(categorical=proto, is_excluded=is_excluded)
            )
        case table_pb2.PrimaryKeyFeatureType():
            return PrimaryKey(
                table_pb2.FeatureType(primary_key=proto, is_excluded=is_excluded)
            )
        case table_pb2.ForeignKeyFeatureType():
            return ForeignKey(
                table_pb2.FeatureType(foreign_key=proto, is_excluded=is_excluded)
            )
        case table_pb2.IdentifierFeatureType():
            return Identifier(
                table_pb2.FeatureType(identifier=proto, is_excluded=is_excluded)
            )
        case table_pb2.NumericalFeatureType():
            return Numerical(
                table_pb2.FeatureType(numerical=proto, is_excluded=is_excluded)
            )
        case table_pb2.MultiCategoricalFeatureType():
            return MultiCategorical(
                table_pb2.FeatureType(multi_categorical=proto, is_excluded=is_excluded)
            )
        case table_pb2.TimestampFeatureType():
            return Timestamp(
                table_pb2.FeatureType(timestamp=proto, is_excluded=is_excluded)
            )
        case table_pb2.EmbeddingFeatureType():
            return Embedding(
                table_pb2.FeatureType(embedding=proto, is_excluded=is_excluded)
            )
        case table_pb2.UnknownFeatureType():
            return Unknown(
                table_pb2.FeatureType(unknown=proto, is_excluded=is_excluded)
            )
        case table_pb2.ImageFeatureType():
            return Image(table_pb2.FeatureType(image=proto, is_excluded=is_excluded))


def _from_feature_type(proto: table_pb2.FeatureType):
    field_name = proto.WhichOneof(_Base.oneof_name())
    new_feature_type = _FEATURE_FIELD_NAME_TO_FEATURE_TYPE.get(field_name)
    if new_feature_type is None:
        raise InvalidArgumentError(
            "unsupported feature type", operation_type=field_name
        )
    return new_feature_type(proto)


def from_bytes(serialized_proto: bytes) -> FeatureType:
    """Deserialize a FeatureType protobuf message directly into a wrapper."""
    proto = table_pb2.FeatureType()
    proto.ParseFromString(serialized_proto)
    return from_proto(proto)


class _Base(OneofProtoWrapper[table_pb2.FeatureType]):
    """Base type for all feature types."""

    _is_excluded: bool

    @classmethod
    def oneof_name(cls) -> str:
        return "feature"

    @classmethod
    def expected_oneof_field(cls) -> str:
        """Returns the name of field for this type in the root proto op type."""
        if cls not in _FEATURE_TYPE_TO_FEATURE_FIELD_NAME:
            raise OpParseError(
                "operation field name must registered in "
                + "_FEATURE_TYPE_TO_FEATURE_FIELD_NAME"
            )
        return _FEATURE_TYPE_TO_FEATURE_FIELD_NAME[cls]

    @property
    def is_excluded(self) -> bool:
        return self._proto.is_excluded


class Text(_Base):
    """Column should be treated like text."""


class Categorical(_Base):
    """Column should be treated like a categorical feature."""


class PrimaryKey(_Base):
    """Column should be treated like a primary key."""


class ForeignKey(_Base):
    """Column should be treated like a foreign key."""

    __match_args__ = ("referenced_source_id",)

    @property
    def referenced_source_id(self) -> orm.SourceID:
        return orm.SourceID(self._proto.foreign_key.referenced_source_id)


class Identifier(_Base):
    """Column should be treated like an identifier."""


class Numerical(_Base):
    """Column should be treated like a numerical feature."""


class MultiCategorical(_Base):
    """Column should be treated like a multi categorical feature."""


class Timestamp(_Base):
    """Column should be treated like a timestamp."""


class Embedding(_Base):
    """Column should be treated like an embedding."""


class Unknown(_Base):
    """The feature type is not known."""


class Image(_Base):
    """Column should be treated like an image."""


def text(*, is_excluded: bool = False):
    """Build a Text FeatureType."""
    return from_proto(table_pb2.TextFeatureType(), is_excluded=is_excluded)


def categorical(*, is_excluded: bool = False):
    """Build a Categorical FeatureType."""
    return from_proto(table_pb2.CategoricalFeatureType(), is_excluded=is_excluded)


def primary_key(*, is_excluded: bool = False):
    """Build a PrimaryKey FeatureType."""
    return from_proto(table_pb2.PrimaryKeyFeatureType(), is_excluded=is_excluded)


def foreign_key(
    referenced_source_id: orm.SourceID, *, is_excluded: bool = False
) -> ForeignKey:
    """Build a ForeignKey FeatureType."""
    return from_proto(
        table_pb2.ForeignKeyFeatureType(referenced_source_id=str(referenced_source_id)),
        is_excluded=is_excluded,
    )


def identifier(*, is_excluded: bool = False) -> Identifier:
    """Build an Identifier FeatureType."""
    return from_proto(table_pb2.IdentifierFeatureType(), is_excluded=is_excluded)


def numerical(*, is_excluded: bool = False):
    """Build a Numerical FeatureType."""
    return from_proto(table_pb2.NumericalFeatureType(), is_excluded=is_excluded)


def multi_categorical(*, is_excluded: bool = False):
    """Build a MultiCategorical FeatureType."""
    return from_proto(table_pb2.MultiCategoricalFeatureType(), is_excluded=is_excluded)


def timestamp(*, is_excluded: bool = False):
    """Build a Timestamp FeatureType."""
    return from_proto(table_pb2.TimestampFeatureType(), is_excluded=is_excluded)


def embedding(*, is_excluded: bool = False):
    """Build an Embedding FeatureType."""
    return from_proto(table_pb2.EmbeddingFeatureType(), is_excluded=is_excluded)


def unknown(*, is_excluded: bool = False):
    """Build an Unknown FeatureType."""
    return from_proto(table_pb2.UnknownFeatureType(), is_excluded=is_excluded)


def image(*, is_excluded: bool = False):
    """Build an Image FeatureType."""
    return from_proto(table_pb2.ImageFeatureType(), is_excluded=is_excluded)


FeatureType = (
    Text
    | Categorical
    | PrimaryKey
    | ForeignKey
    | Identifier
    | Numerical
    | MultiCategorical
    | Timestamp
    | Embedding
    | Unknown
    | Image
)

_FEATURE_FIELD_NAME_TO_FEATURE_TYPE: Final = {
    "text": Text,
    "categorical": Categorical,
    "primary_key": PrimaryKey,
    "foreign_key": ForeignKey,
    "identifier": Identifier,
    "numerical": Numerical,
    "multi_categorical": MultiCategorical,
    "timestamp": Timestamp,
    "embedding": Embedding,
    "unknown": Unknown,
    "image": Image,
}

_FEATURE_TYPE_TO_FEATURE_FIELD_NAME: Final[dict[type[Any], str]] = {
    op: name for name, op in _FEATURE_FIELD_NAME_TO_FEATURE_TYPE.items()
}


_DecodedValue = (
    str | int | float | bool | list[str] | list[int] | list[float] | list[bool]
)


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: PrimaryKey | Identifier | ForeignKey,
) -> Ok[str | int] | InvalidArgumentError: ...


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: Numerical,
) -> Ok[int | float] | InvalidArgumentError: ...


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: Text,
) -> Ok[str] | InvalidArgumentError: ...


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: Timestamp,
) -> InvalidArgumentError: ...


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: Categorical,
) -> Ok[list[str] | list[int] | list[float] | list[bool]] | InvalidArgumentError: ...


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: Embedding,
) -> Ok[list[str] | list[int] | list[float] | list[bool]] | InvalidArgumentError: ...


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: MultiCategorical,
) -> InvalidArgumentError: ...


@overload
def decode_value(
    value: struct_pb2.Value,
    feature_type: Unknown,
) -> InvalidArgumentError: ...


def decode_value(  # noqa: C901
    value: struct_pb2.Value,
    feature_type: FeatureType,
) -> Ok[_DecodedValue] | InvalidArgumentError:
    match _deserialize_protobuf_value(value):
        case Ok(deserialized_value):
            pass
        case InvalidArgumentError() as err:
            return err

    match feature_type:
        case PrimaryKey() | Identifier() | ForeignKey():
            return _decode_identifier(deserialized_value)
        case Numerical():
            return _decode_numerical(deserialized_value)
        case Text():
            return _decode_text(deserialized_value)
        case Timestamp():
            return InvalidArgumentError(
                "timestamp feature type unsupported", ftype=str(feature_type)
            )
        case Categorical():
            return _decode_categorical(deserialized_value)
        case Embedding():
            return _decode_embedding(deserialized_value)
        case MultiCategorical():
            return InvalidArgumentError(
                "multi-categorical feature type unsupported", ftype=str(feature_type)
            )
        case Unknown():
            return InvalidArgumentError(
                "cannot decode an unknown value", ftype=str(feature_type)
            )
        case Image():
            return InvalidArgumentError(
                "cannot decode an image value", ftype=str(feature_type)
            )


def _decode_identifier(value: _DecodedValue) -> Ok[str | int] | InvalidArgumentError:
    # python will automatically coerce a bool to an int to pass this check
    if isinstance(value, bool) or not isinstance(value, str | int):
        return InvalidArgumentError(
            "identifier value type invalid", type=str(type(value))
        )
    return Ok(value)


def _decode_text(value: _DecodedValue) -> Ok[str] | InvalidArgumentError:
    if not isinstance(value, str):
        return InvalidArgumentError("text value type invalid", type=str(type(value)))
    return Ok(value)


def _decode_numerical(value: _DecodedValue) -> Ok[int | float] | InvalidArgumentError:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return InvalidArgumentError(
            "numerical value type invalid", type=str(type(value))
        )
    return Ok(value)


def _decode_categorical(
    value: _DecodedValue,
) -> Ok[str | int | float | bool] | InvalidArgumentError:
    if not isinstance(value, str | int | float | bool):
        return InvalidArgumentError(
            "categorical value type invalid", type=str(type(value))
        )
    return Ok(value)


def _decode_embedding(
    value: _DecodedValue,
) -> Ok[list[str] | list[int] | list[float] | list[bool]] | InvalidArgumentError:
    if not isinstance(value, list):
        return InvalidArgumentError(
            "embedding value type invalid", type=str(type(value))
        )
    return Ok(value)


def _deserialize_protobuf_value(
    value: struct_pb2.Value,
) -> Ok[_DecodedValue] | InvalidArgumentError:
    match value.WhichOneof("kind"):
        case "string_value":
            return Ok(value.string_value)
        case "number_value":
            number_value = value.number_value
            if number_value.is_integer():
                number_value = int(number_value)
            return Ok(number_value)
        case "bool_value":
            return Ok(value.bool_value)
        case "list_value":
            return _deserialize_protobuf_list_value(value.list_value.values)
        case "null_value" | "struct_value" | None as value_type:
            return InvalidArgumentError(
                "deserializing protobuf value type not supported", type=str(value_type)
            )


def _deserialize_protobuf_list_value(
    iterable_values: Iterable[struct_pb2.Value],
) -> Ok[list[str] | list[int] | list[float] | list[bool]] | InvalidArgumentError:
    values = list(iterable_values)
    if not values:
        return Ok(list[str]())
    expected_value_kind = values[0].WhichOneof("kind")
    expected_is_integer = (
        expected_value_kind == "number_value" and values[0].number_value.is_integer()
    )
    result: list[str | int | float | bool] = []
    for value in values:
        value_kind = value.WhichOneof("kind")
        if value_kind != expected_value_kind:
            return InvalidArgumentError(
                "protobuf list value had mixed data types",
                expected_type=expected_value_kind,
                type=value_kind,
            )
        match value_kind:
            case "string_value":
                result.append(value.string_value)
            case "number_value":
                number_value = value.number_value
                is_integer = number_value.is_integer()
                if is_integer != expected_is_integer:
                    return InvalidArgumentError(
                        "protobuf list value had mixed numerical data types",
                        expected_integer=expected_is_integer,
                        is_integer=is_integer,
                    )
                if is_integer:
                    number_value = int(number_value)
                result.append(number_value)
            case "bool_value":
                result.append(value.bool_value)
            case "list_value" | "null_value" | "struct_value" | None as value_type:
                return InvalidArgumentError(
                    "deserializing protobuf list value type not supported",
                    type=str(value_type),
                )
    return Ok(cast(list[str] | list[int] | list[float] | list[bool], result))
