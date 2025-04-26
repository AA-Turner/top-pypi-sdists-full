from enum import Enum
from typing import Optional
from typing import Union

from tecton_core import conf
from tecton_core.query.dialect import Dialect
from tecton_proto.common import compute_mode__client_pb2 as compute_mode_pb2


class ComputeMode(str, Enum):
    """Represents the compute mode for training data generation queries."""

    SPARK = "spark"
    SNOWFLAKE = "snowflake"
    ATHENA = "athena"
    RIFT = "rift"

    def default_dialect(self) -> Dialect:
        return _COMPUTE_MODE_TO_DIALECT[self]

    def to_batch_compute(self) -> "BatchComputeMode":
        try:
            return _STR_TO_BATCH[self.value]
        except KeyError:
            msg = f"Remote jobs are not supported for {self.value} compute mode"
            RuntimeError(msg)


_COMPUTE_MODE_TO_DIALECT = {
    ComputeMode.SPARK: Dialect.SPARK,
    ComputeMode.SNOWFLAKE: Dialect.SNOWFLAKE,
    ComputeMode.ATHENA: Dialect.ATHENA,
    ComputeMode.RIFT: Dialect.DUCKDB,
}


class ComputeModeValueError(ValueError):
    def __init__(self, compute_mode_str: str) -> None:
        msg = f"Invalid compute mode: {compute_mode_str}. Must be one of {[e.value for e in ComputeMode]}"
        super().__init__(msg)


def _parse_compute_mode(compute_mode_str: str) -> ComputeMode:
    try:
        return ComputeMode(compute_mode_str.lower())
    except ValueError:
        raise ComputeModeValueError(compute_mode_str)


def _default_offline_retrieval_compute_mode() -> ComputeMode:
    return _parse_compute_mode(conf.get_or_raise("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE"))


def offline_retrieval_compute_mode(raw_function_override: Optional[Union[ComputeMode, str]]) -> ComputeMode:
    """Returns offline retrieval compute mode based on the given function-level override and the environment."""
    if raw_function_override is not None:
        return _parse_compute_mode(raw_function_override)
    else:
        return _default_offline_retrieval_compute_mode()


class BatchComputeMode(Enum):
    """Represents that compute mode for batch jobs associated with a FeatureView."""

    SPARK = compute_mode_pb2.BatchComputeMode.BATCH_COMPUTE_MODE_SPARK
    SNOWFLAKE = compute_mode_pb2.BatchComputeMode.BATCH_COMPUTE_MODE_SNOWFLAKE
    RIFT = compute_mode_pb2.BatchComputeMode.BATCH_COMPUTE_MODE_RIFT

    @property
    def value(self) -> compute_mode_pb2.BatchComputeMode:
        return super().value


_STR_TO_BATCH = {
    "spark": BatchComputeMode.SPARK,
    "snowflake": BatchComputeMode.SNOWFLAKE,
    "rift": BatchComputeMode.RIFT,
}


def default_batch_compute_mode() -> BatchComputeMode:
    return _STR_TO_BATCH[conf.get_or_raise("TECTON_BATCH_COMPUTE_MODE").lower()]
