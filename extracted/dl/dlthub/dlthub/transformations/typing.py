from dlt.common.metrics import TDatasetDataLocation
from dlt.common.typing import ParamSpec

TTransformationFunParams = ParamSpec("TTransformationFunParams")


class TTransformationDataLocation(TDatasetDataLocation):
    """A dataset read by a transformation."""

    is_materialized: bool
    """Whether the transformation materialized the data instead of running as a model job."""
