import polars as pl
import pytest
from polars.testing import assert_frame_equal
from polars_cloud import ComputeContext

from .conftest import ComputeContextSpecsInput  # noqa: TID252


@pytest.mark.parametrize(
    "proxy_compute", [ComputeContextSpecsInput(instance_type="t3.micro")], indirect=True
)
@pytest.mark.parametrize("aws_s3_uri", ["partition_sink/"], indirect=True)
def test_partition_sink(proxy_compute: ComputeContext, aws_s3_uri: str) -> None:
    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": ["A", "B", "C", "D", "E"]})
    _query = (
        lf.remote(context=proxy_compute)
        .single_node()
        .sink_ipc(
            pl.PartitionBy(aws_s3_uri, key="a"),
        )
        .await_result()
    )
    result = pl.scan_ipc(
        aws_s3_uri + "a=*/*.ipc",
        hive_partitioning=True,
        hive_schema={
            "a": pl.Int64,
        },
    )
    assert_frame_equal(lf, result, check_row_order=False)
