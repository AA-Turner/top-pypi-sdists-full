import pytest
import pprint
import logging
from datetime import datetime

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

# ------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------
logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)

# ------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------
parent_span_context = None
pipeline_run_id = None


@pytest.fixture(scope="module", autouse=True)
def setup_pipeline_and_run(adoc_client):
    global parent_span_context, pipeline_run_id

    logger.info("===== entering create_pipeline_and_run =====")

    meta = PipelineMetadata(
        owner="sdk/pipeline-user",
        team="ADOC",
        codeLocation="...",
    )

    pipeline_name_ = test_const.PIPELINE_NAME

    pipeline = CreatePipeline(
        uid=test_const.PIPELINE_UID,
        name=pipeline_name_,
        description=(
            f"The pipeline {pipeline_name_} has been created "
            f"from acceldata-sdk using External integration"
        ),
        meta=meta,
        context={
            "pipeline_uid": test_const.PIPELINE_UID,
            "pipeline_name": pipeline_name_,
        },
    )

    pipeline_res = adoc_client.create_pipeline(pipeline=pipeline)
    logger.info("Created pipeline with pipeline id :: %s", pipeline_res.id)

    pipeline_run = pipeline_res.create_pipeline_run()
    pipeline_run_id = pipeline_run.id

    span_name_ = f"{test_const.PIPELINE_UID}.root.span"
    parent_span_context = pipeline_run.create_span(uid=span_name_)

    logger.info("Starting root span for pipeline run")
    parent_span_context.start()

    yield

    # ---------------- teardown ----------------
    logger.info("Tearing down pipeline run")

    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    pipeline_run = pipeline.get_run(pipeline_run_id)

    parent_span = pipeline_run.get_root_span()
    parent_span.end(
        context_data={"dag_status": "SUCCESS", "time": str(datetime.now())}
    )

    pipeline_run.update_pipeline_run(
        context_data={"status": "success"},
        result=PipelineRunResult.SUCCESS,
        status=PipelineRunStatus.COMPLETED,
    )

    logger.info("Pipeline run completed successfully")


def create_job_span_not_bounded(
        adoc_client,
        job_uid,
        inputs,
        outputs,
        metadata,
        context_job,
        span_uid,
):
    logger.info(
        "Entering create_job_span_not_bounded for job_uid=%s",
        job_uid,
    )

    span_uid_temp = span_uid

    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    pipeline_run = pipeline.get_run(pipeline_run_id)

    try:
        job = CreateJob(
            uid=job_uid,
            name=f"{job_uid} Job",
            pipeline_run_id=pipeline_run.id,
            description=f"{job_uid} created using torch job decorator",
            inputs=inputs,
            outputs=outputs,
            meta=metadata,
            context=context_job,
        )

        job = pipeline.create_job(job)
        logger.info("Create job response: %s", job)

    except Exception as e:
        logger.exception("Error while creating job %s", job_uid)
        raise

    logger.info("Successfully created job %s", job_uid)

    parent_span_context1 = pipeline_run.get_root_span()

    associated_job_uids = [job_uid]

    if span_uid is None:
        span_uid_temp = job_uid

    span_context = parent_span_context1.create_child_span(
        uid=span_uid_temp,
        context_data={"time": str(datetime.now())},
        associatedJobUids=associated_job_uids,
    )

    logger.info(
        "Created child span uid=%s for job_uid=%s",
        span_uid_temp,
        job_uid,
    )

    return span_context


# ------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------
@pytest.mark.integration
@pytest.mark.order(1)
def test_write_file_func(adoc_client):
    logger.info("===== entering write_file_func =====")

    context_job = {
        "job": "data_gene",
        "uid": "customers.data-generation",
        "operator": "write_file_func",
    }

    span_context_parent = create_job_span_not_bounded(
        adoc_client=adoc_client,
        job_uid="customers.data-generation",
        inputs=[],
        outputs=[Node(job_uid="customers.s3-upload")],
        metadata=JobMetadata(
            "Jason",
            "COKE",
            "https://github.com/coke/reports/customers.kt",
        ),
        context_job=context_job,
        span_uid="customers.data.generation",
    )

    size = test_const.CSV_SIZE

    logger.info("Starting span customers.data.generation")
    span_context_parent.start()

    span_context_parent.send_event(
        GenericEvent(
            context_data={
                "Size": size - 1,
                "total_file": 1,
                "schema": "name,address,dept_id",
            },
            event_uid="customers.data.generation.metadata",
        )
    )

    logger.info("Sent GenericEvent for data generation")

    span_context_parent.send_event(
        LogEvent(
            context_data={
                "Size": size - 1,
                "total_file": 1,
                "schema": "name,address,dept_id",
            },
            log_data="Customer data generated successfully.",
        )
    )

    logger.info("Sent LogEvent for data generation")

    span_context_parent.end()
    logger.info("Ended span customers.data.generation")

@pytest.mark.integration
@pytest.mark.order(2)
def test_upload_file_to_s3(adoc_client):
    logger.info("===== entering upload_file_to_s3 =====")

    context_job = {
        "job": "data_upload",
        "time": str(datetime.now()),
        "uid": "customers.s3-upload",
        "operator": "upload_file_to_s3",
    }

    span_context_parent = create_job_span_not_bounded(
        adoc_client=adoc_client,
        job_uid="customers.s3-upload",
        inputs=[Node(job_uid="customers.data-generation")],
        outputs=[
            Node(
                asset_uid=f"{test_const.S3_DS}.{test_const.S3_CUSTOMER}"
            )
        ],
        metadata=JobMetadata(
            "Jason",
            "COKE",
            "https://github.com/coke/reports/customers.kt",
        ),
        context_job=context_job,
        span_uid="customers.s3.upload",
    )

    span_context_parent.start()
    logger.info("Started span customers.s3.upload")

    span_context_parent.end()
    logger.info("Ended span customers.s3.upload")

@pytest.mark.integration
@pytest.mark.order(3)
def test_rds_and_s3_clubbing(adoc_client):
    logger.info("===== entering rds_and_s3_clubbing =====")

    context_job = {
        "job": "data_clubbing",
        "time": str(datetime.now()),
        "uid": "customers.s3-snowflake-clubbing",
        "operator": "rds_and_s3_clubbing",
    }

    parent_span_context1 = create_job_span_not_bounded(
        adoc_client=adoc_client,
        job_uid="customers.s3-snowflake-clubbing",
        inputs=[
            Node(
                asset_uid=f"{test_const.S3_DS}.{test_const.S3_CUSTOMER}"
            ),
            Node(
                asset_uid=f"{test_const.SDK_SNOWFLAKE_DATA_SOURCE}.{test_const.SNOWFLAKE_SERVICES}"
            ),
        ],
        outputs=[
            Node(
                asset_uid=f"{test_const.SDK_SNOWFLAKE_DATA_SOURCE}.{test_const.S3_SNOWFLAKE_CUSTOMERS}"
            )
        ],
        metadata=JobMetadata(
            "BEN",
            "COKE",
            "https://github.com/coke/reports/rds_customers.kt",
        ),
        context_job=context_job,
        span_uid="customers.s3.snowflake.clubbing",
    )

    parent_span_context1.start()
    logger.info("Started span customers.s3.snowflake.clubbing")

    read_csv_span = parent_span_context1.create_child_span(uid="read_csv")
    read_csv_span.start()
    logger.info("Started read_csv span")

    read_csv_span.send_event(
        GenericEvent(
            context_data={
                "total_file_to_be_read": 1,
                "RDS_TABLES": "1",
            },
            event_uid="read_csv_data",
        )
    )

    read_csv_span.end()
    logger.info("Ended read_csv span")

    parent_span_context1.send_event(
        GenericEvent(
            context_data={
                "total_file_to_be_read": 1,
                "RDS_TABLES": "1",
                "DATA_INSERTED": 100,
                "RDS_USER": "snowflake",
            },
            event_uid="customers.rds.migration.metadata",
        )
    )

    logger.info("Sent RDS migration metadata event")

    parent_span_context1.end()
    logger.info("Ended span customers.s3.snowflake.clubbing")
