from datetime import datetime

import polars as pl
import polars_xdt as xdt
import pytest
from polars.testing import assert_frame_equal
from polars_cloud import ComputeContext, Workspace


@pytest.mark.parametrize(
    "aws_s3_uri", ["proxy_query_plugin.parquet", "proxy_query_plugin/"], indirect=True
)
def test_query_plugin(workspace: Workspace, aws_s3_uri: str) -> None:
    with ComputeContext(
        workspace=workspace, instance_type="t3.micro", requirements=b"polars-xdt"
    ) as ctx:
        lf = pl.LazyFrame(
            {
                "local_dt": [
                    datetime(2020, 10, 10, 1),
                    datetime(2020, 10, 10, 2),
                    datetime(2020, 10, 9, 20),
                ],
                "timezone": [
                    "Europe/London",
                    "Africa/Kigali",
                    "America/New_York",
                ],
            }
        ).with_columns(
            xdt.from_local_datetime("local_dt", pl.col("timezone"), "UTC").alias("date")
        )
        _query = (
            lf.remote(context=ctx).single_node().sink_parquet(aws_s3_uri).await_result()
        )

        result = pl.read_parquet(aws_s3_uri)
        assert_frame_equal(lf.collect(), result)
