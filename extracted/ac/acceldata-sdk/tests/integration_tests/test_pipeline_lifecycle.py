import logging
import pytest
from datetime import datetime
import random

from acceldata_sdk.models.pipeline import (
    CreatePipeline,
    PipelineMetadata,
    PipelineRunResult,
    PipelineRunStatus,
)
from acceldata_sdk.models.job import CreateJob, JobMetadata, Node
from acceldata_sdk.events.generic_event import GenericEvent

from . import test_constants as test_const

logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_list_all_pipelines(adoc_client):
    logger.info("Listing all pipelines")
    pipelines = adoc_client.get_pipelines()
    assert pipelines
    logger.info("Fetched %d pipelines", len(pipelines))


@pytest.mark.integration
def test_create_pipeline(adoc_client):
    logger.info("Creating pipeline")

    meta = PipelineMetadata(
        owner="sdk/pipeline-user",
        team="ADOC",
        codeLocation="...",
    )

    pipeline = CreatePipeline(
        uid=test_const.PIPELINE_UID,
        name=test_const.PIPELINE_NAME,
        description="Pipeline created using Acceldata SDK",
        meta=meta,
        context={
            "pipeline_uid": test_const.PIPELINE_UID,
            "pipeline_name": test_const.PIPELINE_NAME,
        },
    )

    pipeline_res = adoc_client.create_pipeline(pipeline=pipeline)
    assert pipeline_res is not None

    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    assert pipeline is not None

    logger.info("Pipeline created successfully")


@pytest.mark.integration
def test_create_pipeline_run(adoc_client):
    logger.info("Creating pipeline run")

    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    pipeline_run = pipeline.create_pipeline_run()

    fetched_run = pipeline.get_run(pipeline_run.id)
    assert fetched_run is not None
    assert pipeline_run.id == fetched_run.id

    logger.info("Pipeline run created with id=%s", pipeline_run.id)


@pytest.mark.integration
def test_latest_pipeline_run(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)

    latest_run = pipeline.get_latest_pipeline_run()
    runs = pipeline.get_runs()

    assert latest_run.id == runs[0].id
    logger.info("Latest pipeline run verified")


@pytest.mark.integration
def test_create_root_span(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    span = run.create_span(uid=f"{test_const.PIPELINE_UID}.root.span")
    assert span is not None

    logger.info("Root span created")


@pytest.mark.integration
def test_update_pipeline_run(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    result = run.update_pipeline_run(
        context_data={"name": "backend"},
        result=PipelineRunResult.SUCCESS,
        status=PipelineRunStatus.COMPLETED,
    )

    assert result is not None
    logger.info("Pipeline run updated")


@pytest.mark.integration
def test_pipeline_run_details(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    details = run.get_details()
    assert details is not None

    logger.info("Fetched pipeline run details")


@pytest.mark.integration
def test_create_job(adoc_client):
    logger.info("Creating job")

    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    job = CreateJob(
        uid=test_const.PIPELINE_JOB_UID,
        name=f"{test_const.PIPELINE_JOB_UID} Job",
        pipeline_run_id=run.id,
        description="Job created using torch SDK",
        inputs=[Node(job_uid="customers.data-generation")],
        outputs=[Node(asset_uid="S3-DS.s3_customers")],
        meta=JobMetadata(
            "ADOC Pipeline",
            "DR Team",
            "https://github.com/coke/reports/customers.kt",
        ),
        context={
            "job": "data_gene",
            "operator": "write_file_func",
            "time": str(datetime.now()),
        },
    )

    job_res = pipeline.create_job(job)
    assert job_res is not None

    logger.info("Job created successfully")


@pytest.mark.integration
def test_create_child_span(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    root_span = run.get_root_span()
    child_span = root_span.create_child_span(
        uid=f"{test_const.PIPELINE_JOB_UID}.span",
        context_data={"time": str(datetime.now())},
        associatedJobUids=[test_const.PIPELINE_JOB_UID],
    )

    child_span.start()
    child_span.send_event(
        GenericEvent(
            context_data={
                "total_file": 1,
                "schema": "name,address,dept_id",
            },
            event_uid="customers.data.generation.metadata",
        )
    )
    child_span.end()
    root_span.end()

    spans = root_span.get_child_spans()
    assert spans
    logger.info("Child span created and validated")


@pytest.mark.integration
def test_spans_pipeline_run(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    spans = run.get_spans()
    assert spans is not None

    logger.info("Fetched pipeline spans")

@pytest.mark.integration
def test_create_pipeline_run_with_continuation_id(adoc_client):
    create_pipeline_payload = CreatePipeline(
        uid=test_const.PIPELINE_UID_WITH_CONTINUATION_ID,
        name=test_const.PIPELINE_NAME_WITH_CONTINUATION_ID,
        description=f'The has been created from sdk',
    )
    pipeline = adoc_client.create_pipeline(pipeline=create_pipeline_payload)
    logger.info("Validating test_create_pipeline_run_with_continuation_id")
    continuation_id=f'run.{random.random()}'
    pipeline_run = pipeline.create_pipeline_run(continuation_id=continuation_id)
    logger.info(pipeline_run)
    run_with_id = pipeline.get_run(continuation_id=continuation_id)
    logger.info(run_with_id)
    assert pipeline_run == run_with_id

@pytest.mark.integration
def test_delete_pipeline(adoc_client):

    logger.info("Creating pipeline")

    meta = PipelineMetadata(
        owner="sdk/pipeline-user",
        team="ADOC",
        codeLocation="...",
    )

    pipeline = CreatePipeline(
        uid=test_const.PIPELINE_UID_DELETION,
        name=test_const.PIPELINE_NAME_DELETION,
        description="Pipeline created using Acceldata SDK",
        meta=meta,
        context={
            "pipeline_uid": test_const.PIPELINE_UID_DELETION,
            "pipeline_name": test_const.PIPELINE_NAME_DELETION,
        },
    )

    pipeline_res = adoc_client.create_pipeline(pipeline=pipeline)
    res = pipeline_res.delete()

    assert res is not None
    logger.info("Pipeline deleted successfully")
