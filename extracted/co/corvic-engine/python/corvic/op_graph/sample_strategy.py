"""Corvic sample strategy."""

from __future__ import annotations

from typing import Any, Final, overload

from corvic.op_graph.errors import OpParseError
from corvic.proto_wrapper import OneofProtoWrapper
from corvic.result import InvalidArgumentError
from corvic_generated.orm.v1 import table_pb2


@overload
def from_proto(proto: table_pb2.SampleStrategy) -> SampleStrategy: ...


@overload
def from_proto(
    proto: table_pb2.UniformRandom,
) -> UniformRandom: ...


def from_proto(
    proto: (table_pb2.SampleStrategy | table_pb2.UniformRandom),
) -> UniformRandom:
    """Create a SampleStrategy wrapper around a SampleStrategy protobuf message."""
    match proto:
        case table_pb2.SampleStrategy():
            return _from_sample_strategy_type(proto)
        case table_pb2.UniformRandom():
            return SampleStrategy(table_pb2.SampleStrategy(uniform_random=proto))


def _from_sample_strategy_type(proto: table_pb2.SampleStrategy):
    field_name = proto.WhichOneof(_Base.oneof_name())
    new_sample_strategy_type = _SAMPLE_STRATEGY_NAME_TO_SAMPLE_STRATEGY_TYPE.get(
        field_name
    )
    if new_sample_strategy_type is None:
        raise InvalidArgumentError(
            "unsupported sample_strategy type", operation_type=field_name
        )
    return new_sample_strategy_type(proto)


def from_bytes(serialized_proto: bytes) -> SampleStrategy:
    """Deserialize a SampleStrategy protobuf message directly into a wrapper."""
    proto = table_pb2.SampleStrategy()
    proto.ParseFromString(serialized_proto)
    return from_proto(proto)


class _Base(OneofProtoWrapper[table_pb2.SampleStrategy]):
    """Base type for sample_strategy."""

    @classmethod
    def oneof_name(cls) -> str:
        return "sample_strategy"

    @classmethod
    def expected_oneof_field(cls) -> str:
        """Returns the name of field for this sample_strategy."""
        if cls not in _SAMPLE_STRATEGY_TYPE_TO_SAMPLE_STRATEGY_FIELD_NAME:
            raise OpParseError(
                "operation sample_strategy name must registered in "
                + "_SAMPLE_STRATEGY_TYPE_TO_SAMPLE_STRATEGY_FIELD_NAME"
            )
        return _SAMPLE_STRATEGY_TYPE_TO_SAMPLE_STRATEGY_FIELD_NAME[cls]


class UniformRandom(_Base):
    """UniformRandom sample."""

    @property
    def seed(self):
        """Seed for the random number generator."""
        return self._proto.uniform_random.seed


def uniform_random(seed: int | None = None):
    """Build a UniformRandom SampleStrategy."""
    return from_proto(
        table_pb2.UniformRandom(
            seed=seed,
        )
    )


SampleStrategy = UniformRandom


_SAMPLE_STRATEGY_NAME_TO_SAMPLE_STRATEGY_TYPE: Final = {
    "uniform_random": UniformRandom,
}

_SAMPLE_STRATEGY_TYPE_TO_SAMPLE_STRATEGY_FIELD_NAME: Final[dict[type[Any], str]] = {
    op: name for name, op in _SAMPLE_STRATEGY_NAME_TO_SAMPLE_STRATEGY_TYPE.items()
}
