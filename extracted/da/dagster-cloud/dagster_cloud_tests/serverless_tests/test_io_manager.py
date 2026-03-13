from dagster import In, Int, Out, job, op
from dagster_cloud.serverless.io_manager import serverless_io_manager


@op(out=Out(Int))
def return_one():
    return 1


@op(
    ins={"num": In(Int)},
    out=Out(Int),
)
def add_one(num):
    return num + 1


@job(
    resource_defs={
        "io_manager": serverless_io_manager,
    }
)
def serverless_job():
    add_one(return_one())


def test_set_explicitly():
    # test that we can import and set the serverless_io_manager explicitly if desired
    assert serverless_job
