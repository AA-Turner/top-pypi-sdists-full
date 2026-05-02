"""Corvic column encoder."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, Final, overload

import polars as pl
from polars import DataType

from corvic.op_graph.errors import OpParseError
from corvic.proto_wrapper import OneofProtoWrapper
from corvic.result import InvalidArgumentError
from corvic_generated.orm.v1 import table_pb2


@overload
def from_proto(proto: table_pb2.Encoder) -> Encoder: ...


@overload
def from_proto(
    proto: table_pb2.OneHotEncoder,
) -> OneHotEncoder: ...


@overload
def from_proto(
    proto: table_pb2.MinMaxScaler,
) -> MinMaxScaler: ...


@overload
def from_proto(
    proto: table_pb2.LabelBinarizer,
) -> LabelBinarizer: ...


@overload
def from_proto(
    proto: table_pb2.LabelEncoder,
) -> LabelEncoder: ...


@overload
def from_proto(
    proto: table_pb2.KBinsDiscretizer,
) -> KBinsDiscretizer: ...


@overload
def from_proto(
    proto: table_pb2.Binarizer,
) -> Binarizer: ...


@overload
def from_proto(
    proto: table_pb2.MaxAbsScaler,
) -> MaxAbsScaler: ...


@overload
def from_proto(
    proto: table_pb2.StandardScaler,
) -> StandardScaler: ...


def from_proto(
    proto: (
        table_pb2.Encoder
        | table_pb2.OneHotEncoder
        | table_pb2.MinMaxScaler
        | table_pb2.LabelBinarizer
        | table_pb2.LabelEncoder
        | table_pb2.KBinsDiscretizer
        | table_pb2.Binarizer
        | table_pb2.MaxAbsScaler
        | table_pb2.StandardScaler
    ),
) -> Encoder:
    """Create a Encoder wrapper around a Encoder protobuf message."""
    match proto:
        case table_pb2.Encoder():
            return _from_encoder_type(proto)
        case table_pb2.OneHotEncoder():
            return OneHotEncoder(table_pb2.Encoder(one_hot_encoder=proto))
        case table_pb2.MinMaxScaler():
            return MinMaxScaler(table_pb2.Encoder(min_max_scaler=proto))
        case table_pb2.LabelBinarizer():
            return LabelBinarizer(table_pb2.Encoder(label_binarizer=proto))
        case table_pb2.LabelEncoder():
            return LabelEncoder(table_pb2.Encoder(label_encoder=proto))
        case table_pb2.KBinsDiscretizer():
            return KBinsDiscretizer(table_pb2.Encoder(k_bins_discretizer=proto))
        case table_pb2.Binarizer():
            return Binarizer(table_pb2.Encoder(binarizer=proto))
        case table_pb2.MaxAbsScaler():
            return MaxAbsScaler(table_pb2.Encoder(max_abs_scaler=proto))
        case table_pb2.StandardScaler():
            return StandardScaler(table_pb2.Encoder(standard_scaler=proto))


def _from_encoder_type(proto: table_pb2.Encoder):
    field_name = proto.WhichOneof(_Base.oneof_name())
    new_encoder_type = _ENCODER_NAME_TO_ENCODER_TYPE.get(field_name)
    if new_encoder_type is None:
        raise InvalidArgumentError(
            "unsupported encoder type", operation_type=field_name
        )
    return new_encoder_type(proto)


def from_bytes(serialized_proto: bytes) -> Encoder:
    """Deserialize a Encoder protobuf message directly into a wrapper."""
    proto = table_pb2.Encoder()
    proto.ParseFromString(serialized_proto)
    return from_proto(proto)


class _Base(OneofProtoWrapper[table_pb2.Encoder]):
    """Base type for encoders."""

    @classmethod
    def oneof_name(cls) -> str:
        return "encoder"

    @classmethod
    def expected_oneof_field(cls) -> str:
        """Returns the name of field for this encoder in the root proto op encoder."""
        if cls not in _ENCODER_TYPE_TO_ENCODER_FIELD_NAME:
            raise OpParseError(
                "operation encoder name must registered in "
                + "_ENCODER_TYPE_TO_ENCODER_FIELD_NAME"
            )
        return _ENCODER_TYPE_TO_ENCODER_FIELD_NAME[cls]

    @property
    @abstractmethod
    def output_dtype(self) -> DataType: ...


class OneHotEncoder(_Base):
    """Encode categorical features as a one-hot numeric array."""

    @property
    def output_dtype(self) -> DataType:
        return pl.List(pl.Boolean)


class MinMaxScaler(_Base):
    """Transform features by scaling each feature to a given range."""

    @property
    def output_dtype(self) -> DataType:
        return pl.Float32()

    @property
    def feature_range_min(self):
        return self._proto.min_max_scaler.feature_range_min

    @property
    def feature_range_max(self):
        return self._proto.min_max_scaler.feature_range_max


class LabelBinarizer(_Base):
    """Binarize labels in a one-vs-all fashion."""

    @property
    def output_dtype(self) -> DataType:
        return pl.List(pl.Boolean)

    @property
    def neg_label(self):
        return self._proto.label_binarizer.neg_label

    @property
    def pos_label(self):
        return self._proto.label_binarizer.pos_label


class LabelEncoder(_Base):
    """Encode target labels with value between 0 and n_classes-1."""

    @property
    def output_dtype(self) -> DataType:
        return pl.UInt32()


class KBinsDiscretizer(_Base):
    """Bin continuous data into intervals."""

    @property
    def output_dtype(self) -> DataType:
        return pl.Float32()

    @property
    def n_bins(self):
        return self._proto.k_bins_discretizer.n_bins

    @property
    def encode_method(self):
        return self._proto.k_bins_discretizer.encode_method

    @property
    def strategy(self):
        return self._proto.k_bins_discretizer.strategy


class Binarizer(_Base):
    """Binarize data (set feature values to 0 or 1) according to a threshold."""

    @property
    def output_dtype(self) -> DataType:
        return pl.Boolean()

    @property
    def threshold(self):
        return self._proto.binarizer.threshold


class MaxAbsScaler(_Base):
    """Scale each feature by its maximum absolute value."""

    @property
    def output_dtype(self) -> DataType:
        return pl.Float32()


class StandardScaler(_Base):
    """Standardize features by removing the mean and scaling to unit variance."""

    @property
    def output_dtype(self) -> DataType:
        return pl.Float32()

    @property
    def with_mean(self):
        return self._proto.standard_scaler.with_mean

    @property
    def with_std(self):
        return self._proto.standard_scaler.with_std


def one_hot_encoder():
    """Build a OneHotEncoder Encoder."""
    return from_proto(table_pb2.OneHotEncoder())


def min_max_scaler(feature_range_min: int = 0, feature_range_max: int = 1):
    """Build a MinMaxScaler Encoder."""
    return from_proto(
        table_pb2.MinMaxScaler(
            feature_range_min=feature_range_min,
            feature_range_max=feature_range_max,
        )
    )


def label_binarizer(neg_label: int = 0, pos_label: int = 1):
    """Build a LabelBinarizer Encoder."""
    return from_proto(
        table_pb2.LabelBinarizer(
            neg_label=neg_label,
            pos_label=pos_label,
        )
    )


def label_encoder():
    """Build a LabelEncoder Encoder."""
    return from_proto(table_pb2.LabelEncoder())


def k_bins_discretizer(
    n_bins: int, encode_method: str = "ordinal", strategy: str = "quantile"
):
    """Build a KBinsDiscretizer Encoder."""
    return from_proto(
        table_pb2.KBinsDiscretizer(
            n_bins=n_bins,
            encode_method=encode_method,
            strategy=strategy,
        )
    )


def binarizer(threshold: float = 0.0):
    """Build a Binarizer Encoder."""
    return from_proto(table_pb2.Binarizer(threshold=threshold))


def max_abs_scaler():
    """Build a MaxAbsScaler Encoder."""
    return from_proto(table_pb2.MaxAbsScaler())


def standard_scaler(
    *,
    with_mean: bool = True,
    with_std: bool = True,
):
    """Build a StandardScaler Encoder."""
    return from_proto(
        table_pb2.StandardScaler(
            with_mean=with_mean,
            with_std=with_std,
        )
    )


Encoder = (
    OneHotEncoder
    | MinMaxScaler
    | LabelBinarizer
    | LabelEncoder
    | KBinsDiscretizer
    | Binarizer
    | MaxAbsScaler
    | StandardScaler
)


_ENCODER_NAME_TO_ENCODER_TYPE: Final = {
    "one_hot_encoder": OneHotEncoder,
    "min_max_scaler": MinMaxScaler,
    "label_binarizer": LabelBinarizer,
    "label_encoder": LabelEncoder,
    "k_bins_discretizer": KBinsDiscretizer,
    "binarizer": Binarizer,
    "max_abs_scaler": MaxAbsScaler,
    "standard_scaler": StandardScaler,
}

_ENCODER_TYPE_TO_ENCODER_FIELD_NAME: Final[dict[type[Any], str]] = {
    op: name for name, op in _ENCODER_NAME_TO_ENCODER_TYPE.items()
}
