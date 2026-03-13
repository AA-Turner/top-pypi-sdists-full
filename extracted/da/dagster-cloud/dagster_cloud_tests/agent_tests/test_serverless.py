import datetime
import pickle
from unittest import mock

import boto3
import pytest
from dagster import (
    GraphIn,
    GraphOut,
    In,
    StaticPartitionsDefinition,
    TimeWindowPartitionMapping,
    asset,
    graph,
    job,
    materialize,
    op,
)
from dagster._core.definitions.assets.definition.assets_definition import AssetsDefinition
from dagster._core.definitions.definitions_class import Definitions
from dagster._core.definitions.source_asset import SourceAsset
from dagster._core.definitions.unresolved_asset_job_definition import define_asset_job
from dagster._core.test_utils import environ
from dagster._time import get_current_datetime
from dagster_cloud.serverless.io_manager import (
    PickledObjectServerlessIOManager,
    serverless_io_manager,
)
from mypy_boto3_s3.service_resource import S3ServiceResource


@pytest.fixture
def mock_s3_bucket(s3_resource: S3ServiceResource):
    bucket = s3_resource.create_bucket(Bucket="test-bucket")
    try:
        yield bucket
    finally:
        bucket.objects.all().delete()
        bucket.delete()


@pytest.fixture
def mock_boto_session(s3_resource):
    yield boto3.Session()


@pytest.fixture
def serverless_io_manager_env():
    with environ(
        {
            "DAGSTER_CLOUD_SERVERLESS_STORAGE_S3_BUCKET": "test-bucket",
            "DAGSTER_CLOUD_SERVERLESS_STORAGE_S3_PREFIX": "test-prefix",
        },
    ):
        yield


@pytest.fixture
def mock_refresh_boto_session(mock_boto_session):
    with mock.patch.object(
        PickledObjectServerlessIOManager,
        "_refresh_boto_session",
        return_value=(mock_boto_session, get_current_datetime() + datetime.timedelta(days=3)),
    ):
        yield


def get_inty_job():
    @op
    def first_op(first_input):
        assert first_input == 4
        return first_input * 2

    @op
    def second_op(second_input):
        assert second_input == 8
        return second_input + 3

    source1 = SourceAsset("source1", partitions_def=StaticPartitionsDefinition(["foo", "bar"]))

    @asset
    def asset1(source1):
        return source1["foo"] + source1["bar"]

    @asset
    def asset2(asset1):
        assert asset1 == 3
        return asset1 + 1

    @graph(ins={"asset2": GraphIn()}, out={"asset3": GraphOut()})
    def graph_asset(asset2):
        return second_op(first_op(asset2))

    @asset(partitions_def=StaticPartitionsDefinition(["apple", "orange"]))
    def partitioned():
        return 8

    graph_asset_def = AssetsDefinition.from_graph(graph_asset)
    target_assets = [asset1, asset2, graph_asset_def, partitioned]

    return Definitions(
        assets=[*target_assets, source1],
        jobs=[define_asset_job("assets", target_assets)],
        resources={"io_manager": serverless_io_manager},
    ).resolve_job_def("assets")


@op
def int_op():
    return 1


@op(ins={"int_in": In(int)})
def io_manager_op(context, int_in):
    from dagster_cloud.serverless.io_manager import PickledObjectServerlessIOManager

    assert int_in == 1
    assert type(context.resources.io_manager) == PickledObjectServerlessIOManager
    return 2


@job(resource_defs={"io_manager": serverless_io_manager})
def serverless_io_manager_job():
    io_manager_op(int_in=int_op())


def test_serverless_io_manager_job_execution(
    mock_s3_bucket,
    serverless_io_manager_env,
    agent_instance_local_ursula,
    mock_refresh_boto_session,
):
    instance = agent_instance_local_ursula
    result = serverless_io_manager_job.execute_in_process(instance=instance)
    assert result.success
    assert result.output_for_node("int_op") == 1
    assert result.output_for_node("io_manager_op") == 2


from dagster import AssetExecutionContext, AssetIn, DailyPartitionsDefinition


def test_serverless_io_manager_allow_missing_partitions(
    mock_s3_bucket,
    serverless_io_manager_env,
    agent_instance_local_ursula,
    mock_refresh_boto_session,
):
    start = datetime.datetime(2022, 1, 1)

    daily = DailyPartitionsDefinition(start_date=f"{start:%Y-%m-%d}")

    @asset(partitions_def=daily, io_manager_def=serverless_io_manager)
    def upstream_asset(context: AssetExecutionContext) -> str:
        return context.partition_key

    @asset(
        partitions_def=daily,
        io_manager_def=serverless_io_manager,
        ins={
            "upstream_asset": AssetIn(
                partition_mapping=TimeWindowPartitionMapping(start_offset=-1),
                metadata={"allow_missing_partitions": True},
            )
        },
    )
    def downstream_asset(upstream_asset: dict[str, str]):
        return upstream_asset

    materialize(
        [upstream_asset],
        partition_key=start.strftime(daily.fmt),
        instance=agent_instance_local_ursula,
    )
    result = materialize(
        [upstream_asset.to_source_asset(), downstream_asset],
        partition_key=(start + datetime.timedelta(days=1)).strftime(daily.fmt),
        instance=agent_instance_local_ursula,
    )
    downstream_asset_data = result.output_for_node("downstream_asset", "result")
    assert len(downstream_asset_data) == 1, "1 partition should be missing"


def test_serverless_io_manager_asset_execution(
    mock_s3_bucket,
    serverless_io_manager_env,
    agent_instance_local_ursula,
    mock_refresh_boto_session,
):
    instance = agent_instance_local_ursula

    inty_job = get_inty_job()

    assert not len(list(mock_s3_bucket.objects.all()))

    serverless_prefix = "test-prefix/io_storage/sandbox"

    mock_s3_bucket.put_object(Key=f"{serverless_prefix}/source1/foo", Body=pickle.dumps(1))
    # pickled_source1_bar = pickle.dumps(2)
    mock_s3_bucket.put_object(Key=f"{serverless_prefix}/source1/bar", Body=pickle.dumps(2))

    result = inty_job.execute_in_process(partition_key="apple", instance=instance)

    assert result.output_for_node("asset1") == 3
    assert result.output_for_node("asset2") == 4
    assert result.output_for_node("graph_asset.first_op") == 8
    assert result.output_for_node("graph_asset.second_op") == 11

    objects = list(mock_s3_bucket.objects.all())
    assert len(objects) == 7
    assert {(o.bucket_name, o.key) for o in objects} == {
        ("test-bucket", f"{serverless_prefix}/source1/bar"),
        ("test-bucket", f"{serverless_prefix}/source1/foo"),
        ("test-bucket", f"{serverless_prefix}/asset1"),
        ("test-bucket", f"{serverless_prefix}/asset2"),
        ("test-bucket", f"{serverless_prefix}/asset3"),
        ("test-bucket", f"{serverless_prefix}/partitioned/apple"),
        (
            "test-bucket",
            "/".join(
                [serverless_prefix, "storage", result.run_id, "graph_asset.first_op", "result"]
            ),
        ),
    }

    # re-execution does not cause issues, overwrites the buckets
    result2 = inty_job.execute_in_process(partition_key="apple", instance=instance)

    objects = list(mock_s3_bucket.objects.all())
    assert len(objects) == 8
    assert {(o.bucket_name, o.key) for o in objects} == {
        ("test-bucket", f"{serverless_prefix}/source1/bar"),
        ("test-bucket", f"{serverless_prefix}/source1/foo"),
        ("test-bucket", f"{serverless_prefix}/asset1"),
        ("test-bucket", f"{serverless_prefix}/asset2"),
        ("test-bucket", f"{serverless_prefix}/asset3"),
        ("test-bucket", f"{serverless_prefix}/partitioned/apple"),
        (
            "test-bucket",
            "/".join(
                [serverless_prefix, "storage", result.run_id, "graph_asset.first_op", "result"]
            ),
        ),
        (
            "test-bucket",
            "/".join(
                [
                    serverless_prefix,
                    "storage",
                    result2.run_id,
                    "graph_asset.first_op",
                    "result",
                ]
            ),
        ),
    }
