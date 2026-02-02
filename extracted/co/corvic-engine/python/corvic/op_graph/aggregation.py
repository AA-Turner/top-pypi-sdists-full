"""Corvic column aggregations."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, Final, overload

import polars as pl

from corvic.op_graph.errors import OpParseError
from corvic.proto_wrapper import OneofProtoWrapper
from corvic.result import InvalidArgumentError
from corvic_generated.orm.v1 import table_pb2


@overload
def from_proto(proto: table_pb2.Aggregation) -> Aggregation: ...


@overload
def from_proto(proto: table_pb2.Min) -> Min: ...


@overload
def from_proto(proto: table_pb2.Max) -> Max: ...


@overload
def from_proto(proto: table_pb2.Mean) -> Mean: ...


@overload
def from_proto(proto: table_pb2.Std) -> Std: ...


@overload
def from_proto(proto: table_pb2.Quantile) -> Quantile: ...


@overload
def from_proto(proto: table_pb2.Count) -> Count: ...


@overload
def from_proto(proto: table_pb2.NullCount) -> NullCount: ...


def from_proto(
    proto: (
        table_pb2.Aggregation
        | table_pb2.Min
        | table_pb2.Max
        | table_pb2.Mean
        | table_pb2.Std
        | table_pb2.Quantile
        | table_pb2.Count
        | table_pb2.NullCount
    ),
) -> Aggregation:
    """Create a Aggregation wrapper around a Aggregation protobuf message."""
    match proto:
        case table_pb2.Aggregation():
            return _from_feature_type(proto)
        case table_pb2.Min():
            return Min(table_pb2.Aggregation(min=proto))
        case table_pb2.Max():
            return Max(table_pb2.Aggregation(max=proto))
        case table_pb2.Mean():
            return Mean(table_pb2.Aggregation(mean=proto))
        case table_pb2.Std():
            return Std(table_pb2.Aggregation(std=proto))
        case table_pb2.Quantile():
            return Quantile(table_pb2.Aggregation(quantile=proto))
        case table_pb2.Count():
            return Count(table_pb2.Aggregation(count=proto))
        case table_pb2.NullCount():
            return NullCount(table_pb2.Aggregation(null_count=proto))


def _from_feature_type(proto: table_pb2.Aggregation):
    field_name = proto.WhichOneof(_Base.oneof_name())
    new_aggregation = _AGGREGATION_FIELD_NAME_TO_AGGREGATION.get(field_name)
    if new_aggregation is None:
        raise InvalidArgumentError("unsupported aggregation", operation_type=field_name)
    return new_aggregation(proto)


def from_bytes(serialized_proto: bytes) -> Aggregation:
    """Deserialize a Aggregation protobuf message directly into a wrapper."""
    proto = table_pb2.Aggregation()
    proto.ParseFromString(serialized_proto)
    return from_proto(proto)


class _Base(OneofProtoWrapper[table_pb2.Aggregation]):
    """Base type for all aggregation."""

    @classmethod
    def oneof_name(cls) -> str:
        return "aggregation"

    @classmethod
    def expected_oneof_field(cls) -> str:
        """Returns the name of field for this aggregation in the root proto op."""
        if cls not in _AGGREGATION_TO_AGGREGATION_FIELD_NAME:
            raise OpParseError(
                "operation aggregation name must registered in "
                + "_AGGREGATION_TO_AGGREGATION_FIELD_NAME"
            )
        return _AGGREGATION_TO_AGGREGATION_FIELD_NAME[cls]

    @abstractmethod
    def output_dtype(self, dtype: pl.DataType) -> pl.DataType: ...


class Min(_Base):
    """Aggregate the columns of this DataFrame to their minimum value."""

    def output_dtype(self, dtype: pl.DataType) -> pl.DataType:
        return dtype


class Max(_Base):
    """Aggregate the columns of this DataFrame to their maximum value."""

    def output_dtype(self, dtype: pl.DataType) -> pl.DataType:
        return dtype


class Mean(_Base):
    """Aggregate the columns of this DataFrame to their mean value."""

    def output_dtype(self, dtype: pl.DataType) -> pl.DataType:
        if dtype.is_numeric():
            return pl.Float64()
        return dtype


class Std(_Base):
    """Aggregate the columns of this DataFrame to their standard deviation value."""

    def output_dtype(self, dtype: pl.DataType) -> pl.DataType:
        if dtype.is_numeric():
            return pl.Float64()
        return dtype


class Quantile(_Base):
    """Aggregate the columns of this DataFrame to their quantile value."""

    def output_dtype(self, dtype: pl.DataType) -> pl.DataType:
        if dtype.is_numeric():
            return pl.Float64()
        return dtype

    @property
    def quantile(self) -> float:
        return self._proto.quantile.quantile


class Count(_Base):
    """Aggregate the columns of this DataFrame to their standard deviation value."""

    def output_dtype(self, dtype: pl.DataType) -> pl.DataType:
        return pl.UInt32()


class NullCount(_Base):
    """Aggregate the columns of this DataFrame to their standard deviation value."""

    def output_dtype(self, dtype: pl.DataType) -> pl.DataType:
        return pl.UInt32()


def min():
    """Build a Min Aggregation."""
    return from_proto(table_pb2.Min())


def max():
    """Build a Max Aggregation."""
    return from_proto(table_pb2.Max())


def mean():
    """Build a Mean Aggregation."""
    return from_proto(table_pb2.Mean())


def std():
    """Build a Std Aggregation."""
    return from_proto(table_pb2.Std())


def quantile(quantile: float):
    """Build a Quantile Aggregation."""
    return from_proto(table_pb2.Quantile(quantile=quantile))


def count():
    """Build a Count Aggregation."""
    return from_proto(table_pb2.Count())


def null_count():
    """Build a NullCount Aggregation."""
    return from_proto(table_pb2.NullCount())


Aggregation = Min | Max | Mean | Std | Quantile | Count | NullCount

_AGGREGATION_FIELD_NAME_TO_AGGREGATION: Final = {
    "min": Min,
    "max": Max,
    "mean": Mean,
    "std": Std,
    "quantile": Quantile,
    "count": Count,
    "null_count": NullCount,
}

_AGGREGATION_TO_AGGREGATION_FIELD_NAME: Final[dict[type[Any], str]] = {
    op: name for name, op in _AGGREGATION_FIELD_NAME_TO_AGGREGATION.items()
}
