import pytest
import logging
from datetime import datetime, timedelta

from acceldata_sdk.events.generic_event import GenericEvent
from acceldata_sdk.events.log_events import LogEvent
from acceldata_sdk.models.job import JobMetadata, Node, CreateJob
from acceldata_sdk.models.pipeline import (
    CreatePipeline,
    PipelineMetadata,
    PipelineRunResult,
    PipelineRunStatus,
)

from . import test_constants as test_const

logger = logging.getLogger(__name__)

# =====================================================
# Runtime globals
# =====================================================
parent_span_context = None
pipeline_run_id = None

# =====================================================
# Explicit timestamps
# =====================================================
now = datetime.now()

explicit_pipeline_createdAt = now - timedelta(days=2, hours=6, minutes=30)
explicit_pipeline_updatedAt = explicit_pipeline_createdAt + timedelta(minutes=30)
explicit_pipeline_run_startedAt = explicit_pipeline_createdAt + timedelta(minutes=30)

root_span_created_at = explicit_pipeline_run_startedAt + timedelta(minutes=1)

child_span_1_created_at = explicit_pipeline_run_startedAt + timedelta(minutes=30)
child_span_1_finished_at = child_span_1_created_at + timedelta(minutes=30)

child_span_2_created_at = child_span_1_finished_at + timedelta(minutes=1)
child_span_2_finished_at = child_span_2_created_at + timedelta(minutes=10)

child_span_3_created_at = child_span_2_finished_at + timedelta(minutes=1)

child_span_3_child_1_created_at = child_span_3_created_at + timedelta(minutes=1)
child_span_3_child_1_finished_at = child_span_3_child_1_created_at + timedelta(minutes=10)

child_span_3_child_2_created_at = child_span_3_child_1_finished_at + timedelta(minutes=1)

child_span_3_child_2_child_1_created_at = child_span_3_child_2_created_at + timedelta(minutes=1)
child_span_3_child_2_child_1_finished_at = child_span_3_child_2_child_1_created_at + timedelta(minutes=10)

child_span_3_child_2_child_2_created_at = child_span_3_child_2_child_1_finished_at + timedelta(minutes=1)
child_span_3_child_2_child_2_finished_at = child_span_3_child_2_child_2_created_at + timedelta(minutes=10)

child_span_3_child_2_finished_at = child_span_3_child_2_child_2_finished_at

child_span_3_child_3_created_at = child_span_3_child_2_finished_at + timedelta(minutes=1)
child_span_3_child_3_finished_at = child_span_3_child_3_created_at + timedelta(minutes=10)

child_span_3_finished_at = child_span_3_child_3_finished_at
explicit_pipeline_run_finishedAt = child_span_3_finished_at + timedelta(minutes=1)


# =====================================================
# Pipeline + run setup
# =====================================================
@pytest.mark.integration
@pytest.mark.order(1)
def test_create_pipeline_and_run(adoc_client):
    global parent_span_context, pipeline_run_id

    logger.info("Creating pipeline with explicit timestamps")

    meta = PipelineMetadata(
        owner="sdk/pipeline-user",
        team="ADOC",
        codeLocation="...",
    )

    pipeline = CreatePipeline(
        uid=test_const.EXPLICIT_PIPELINE_UID,
        name=test_const.EXPLICIT_PIPELINE_NAME,
        description="Pipeline created using SDK explicit time flow",
        meta=meta,
        context={
            "pipeline_uid": test_const.EXPLICIT_PIPELINE_UID,
            "pipeline_name": test_const.EXPLICIT_PIPELINE_NAME,
        },
        createdAt=explicit_pipeline_createdAt,
        updatedAt=explicit_pipeline_updatedAt,
    )

    pipeline_res = adoc_client.create_pipeline(pipeline=pipeline)
    logger.info("Pipeline created id=%s", pipeline_res.id)

    pipeline_run = pipeline_res.create_pipeline_run(
        startedAt=explicit_pipeline_run_startedAt
    )

    pipeline_run_id = pipeline_run.id
    logger.info("Pipeline run started id=%s", pipeline_run_id)

    span_uid = f"{test_const.EXPLICIT_PIPELINE_UID}.root.span"

    parent_span_context = pipeline_run.create_span(
        uid=span_uid,
        with_explicit_time=True,
    )

    parent_span_context.start(created_at=root_span_created_at)
    logger.info("Root span started")


# =====================================================
# Helper
# =====================================================
def create_job_span_not_bounded(
        adoc_client,
        job_uid,
        inputs,
        outputs,
        metadata,
        context_job,
        span_uid,
):
    logger.info("Creating job %s", job_uid)

    pipeline = adoc_client.get_pipeline(test_const.EXPLICIT_PIPELINE_UID)
    pipeline_run = pipeline.get_run(pipeline_run_id)

    job = CreateJob(
        uid=job_uid,
        name=f"{job_uid} Job",
        pipeline_run_id=pipeline_run.id,
        description=f"{job_uid} created via SDK",
        inputs=inputs,
        outputs=outputs,
        meta=metadata,
        context=context_job,
        with_explicit_time=True,
    )

    job = pipeline.create_job(job)
    logger.info("Job created %s", job_uid)

    root_span = pipeline_run.get_root_span()

    return root_span.create_child_span(
        uid=span_uid or job_uid,
        context_data={"time": str(datetime.now())},
        associatedJobUids=[job_uid],
        with_explicit_time=True,
    )


# =====================================================
# Job executions
# =====================================================
@pytest.mark.integration
@pytest.mark.order(2)
def test_write_file_func(adoc_client):
    span = create_job_span_not_bounded(
        adoc_client,
        "customers.data-generation",
        [],
        [Node(job_uid="customers.s3-upload")],
        JobMetadata("Jason", "COKE", "https://github.com/coke/reports/customers.kt"),
        {"job": "data_gene"},
        "customers.data.generation",
    )

    span.start(created_at=child_span_1_created_at)

    span.send_event(
        GenericEvent(
            context_data={
                "Size": test_const.CSV_SIZE - 1,
                "total_file": 1,
            },
            event_uid="customers.data.generation.metadata",
            created_at=child_span_1_created_at,
        )
    )

    span.send_event(
        LogEvent(
            context_data={"Size": test_const.CSV_SIZE - 1},
            log_data="Customer data generated successfully",
            created_at=child_span_1_created_at,
        )
    )

    span.end(created_at=child_span_1_finished_at)
    logger.info("Data generation completed")


@pytest.mark.integration
@pytest.mark.order(3)
def test_upload_file_to_s3(adoc_client):
    span = create_job_span_not_bounded(
        adoc_client,
        "customers.s3-upload",
        [Node(job_uid="customers.data-generation")],
        [Node(asset_uid=f"{test_const.S3_DS}.{test_const.S3_CUSTOMER}")],
        JobMetadata("Jason", "COKE", "https://github.com/coke/reports/customers.kt"),
        {"job": "data_upload"},
        "customers.s3.upload",
    )

    span.start(created_at=child_span_2_created_at)
    span.end(created_at=child_span_2_finished_at)
    logger.info("Upload to S3 completed")

@pytest.mark.integration
@pytest.mark.order(4)
def test_rds_and_s3_clubbing(adoc_client):
    span = create_job_span_not_bounded(
        adoc_client,
        "customers.s3-snowflake-clubbing",
        [
            Node(asset_uid=f"{test_const.S3_DS}.{test_const.S3_CUSTOMER}"),
            Node(asset_uid=f"{test_const.SDK_SNOWFLAKE_DATA_SOURCE}.{test_const.SNOWFLAKE_SERVICES}"),
        ],
        [Node(asset_uid=f"{test_const.SDK_SNOWFLAKE_DATA_SOURCE}.{test_const.S3_SNOWFLAKE_CUSTOMERS}")],
        JobMetadata("BEN", "COKE", "https://github.com/coke/reports/rds_customers.kt"),
        {"job": "data_clubbing"},
        "customers.s3.snowflake.clubbing",
    )

    span.start(created_at=child_span_3_created_at)
    span.end(created_at=child_span_3_finished_at)

    logger.info("RDS + S3 clubbing completed")

@pytest.mark.integration
@pytest.mark.order(5)
def test_close_pipeline_run(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.EXPLICIT_PIPELINE_UID)
    pipeline_run = pipeline.get_run(pipeline_run_id)

    pipeline_run.get_root_span().end(
        context_data={"dag_status": "SUCCESS"},
        created_at=explicit_pipeline_run_finishedAt,
    )

    pipeline_run.update_pipeline_run(
        context_data={"status": "success"},
        result=PipelineRunResult.SUCCESS,
        status=PipelineRunStatus.COMPLETED,
    )

    logger.info("Pipeline run closed successfully")
