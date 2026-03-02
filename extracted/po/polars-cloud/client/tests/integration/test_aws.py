import polars as pl
import polars_cloud as pc
import polars_cloud.constants
import pytest
from polars.testing import assert_frame_equal
from polars_cloud import ComputeContext, Workspace

from .conftest import ComputeContextSpecsInput  # noqa: TID252


@pytest.mark.parametrize("aws_s3_uri", ["proxy_query.parquet"], indirect=True)
@pytest.mark.parametrize(
    "proxy_compute",
    [ComputeContextSpecsInput(instance_type="t3.micro", storage=128)],
    indirect=True,
)
def test_proxy_query(
    workspace: Workspace, proxy_compute: ComputeContext, aws_s3_uri: str
) -> None:
    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
    lf = lf.with_columns(pl.col("a").max().over("b").alias("ab_max"))

    _query_result = pc.spawn_blocking(lf, dst=aws_s3_uri, context=proxy_compute)
    result = pl.read_parquet(aws_s3_uri)
    assert_frame_equal(lf.collect(), result)

    # Test if node info is correct
    nodes = polars_cloud.constants.API_CLIENT.get_compute_cluster_nodes(
        workspace.id,
        proxy_compute._compute_id,  # type: ignore[arg-type]
    )
    assert len(nodes) == 1

    total_cpu = sum(node.cpus for node in nodes if node.cpus is not None)
    total_memory = sum(node.memory_mb for node in nodes if node.memory_mb is not None)
    total_storage = sum(
        node.storage_mb for node in nodes if node.storage_mb is not None
    )
    # The exact value depends on the system availability, for ease I have added ranges
    assert total_cpu == 2
    assert 900 < total_memory < 1100
    assert 120000 < total_storage < 140000


@pytest.mark.parametrize(
    "aws_s3_uri", ["proxy_query_instance_specs.parquet"], indirect=True
)
@pytest.mark.parametrize(
    "proxy_compute", [ComputeContextSpecsInput(memory=2, cpus=2)], indirect=True
)
def test_proxy_query_instance_req(
    proxy_compute: ComputeContext, aws_s3_uri: str
) -> None:
    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
    lf = lf.with_columns(pl.col("a").max().over("b").alias("ab_max"))

    _query = pc.spawn_blocking(lf, dst=aws_s3_uri, context=proxy_compute)
    result = pl.read_parquet(aws_s3_uri)
    assert_frame_equal(lf.collect(), result)


@pytest.mark.parametrize(
    "proxy_compute",
    [ComputeContextSpecsInput(memory=2, cpus=2, cluster_size=2)],
    indirect=True,
)
@pytest.mark.parametrize(
    "aws_s3_uri",
    ["proxy_query_distributed.parquet", "proxy_query_distributed/"],
    indirect=True,
)
def test_proxy_query_distributed(
    proxy_compute: ComputeContext, aws_s3_uri: str
) -> None:
    lf = (
        pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
        .group_by("a")
        .agg(pl.col("b").sum())
        .sort(by="a")
    )
    _query = (
        lf.remote(context=proxy_compute)
        .distributed()
        .sink_parquet(aws_s3_uri, sink_to_single_file=aws_s3_uri.endswith(".parquet"))
        .await_result()
    )
    result = pl.read_parquet(aws_s3_uri)
    assert_frame_equal(lf.collect(), result)


@pytest.mark.parametrize("aws_s3_uri", ["direct_query.parquet"], indirect=True)
@pytest.mark.parametrize(
    "direct_compute",
    [ComputeContextSpecsInput(instance_type="t3.micro")],
    indirect=True,
)
def test_direct_query(direct_compute: ComputeContext, aws_s3_uri: str) -> None:
    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
    lf = lf.with_columns(pl.col("a").max().over("b").alias("ab_max"))

    query_result = pc.spawn_blocking(
        lf, dst=aws_s3_uri, context=direct_compute, sink_to_single_file=True
    )

    result = pl.read_parquet(aws_s3_uri)
    assert_frame_equal(lf.collect(), result)

    # Check if head matches, assuming it will give at least len(lf) rows back
    head_result = query_result.head
    assert_frame_equal(lf.collect(), head_result)  # type: ignore[arg-type]


@pytest.mark.parametrize("aws_s3_uri", ["direct_reconnect.parquet"], indirect=True)
@pytest.mark.parametrize(
    "direct_compute",
    [ComputeContextSpecsInput(instance_type="t3.micro")],
    indirect=True,
)
def test_reconnect_context(
    direct_compute: ComputeContext,
    aws_s3_uri: str,
) -> None:
    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
    lf = lf.with_columns(pl.col("a").max().over("b").alias("ab_max"))

    # Attempt to reconnect with the cluster id
    reconnected_context = pc.ComputeContext.connect(
        workspace=direct_compute.workspace.name,
        compute_id=direct_compute._compute_id,  # type: ignore[arg-type]
    )
    _query_result = pc.spawn_blocking(lf, dst=aws_s3_uri, context=reconnected_context)
    result = pl.read_parquet(aws_s3_uri)
    assert_frame_equal(lf.collect(), result)


@pytest.mark.parametrize("aws_s3_uri", ["direct_profile.parquet"], indirect=True)
@pytest.mark.parametrize(
    "direct_compute",
    [ComputeContextSpecsInput(instance_type="t3.micro")],
    indirect=True,
)
def test_direct_profile(direct_compute: ComputeContext, aws_s3_uri: str) -> None:
    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
    lf = lf.with_columns(pl.col("a").max().over("b").alias("ab_max"))

    in_progress = pc.spawn(
        lf, dst=aws_s3_uri, context=direct_compute, sink_to_single_file=True
    )
    assert isinstance(in_progress, pc.DirectQuery)
    profile = in_progress.await_profile()

    # The first progress update may just be the physical plan,
    # we may not have any trace data yet
    assert profile.data is not None
    while profile.data.is_empty():
        profile = in_progress.await_profile()

    assert profile.data is not None
    assert not profile.data.is_empty()
