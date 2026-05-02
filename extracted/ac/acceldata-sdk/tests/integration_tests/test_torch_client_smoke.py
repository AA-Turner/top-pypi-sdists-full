import logging
import pprint
import random
from datetime import datetime

import acceldata_sdk.constants as const
import pytest
from acceldata_sdk.errors import APIError
from acceldata_sdk.events.generic_event import GenericEvent
from acceldata_sdk.events.log_events import LogEvent
from acceldata_sdk.models.job import CreateJob, JobMetadata, Node
from acceldata_sdk.models.pipeline import (
    CreatePipeline,
    PipelineMetadata,
    PipelineRunResult,
    PipelineRunStatus,
)
from acceldata_sdk.models.profile import ProfilingType
from acceldata_sdk.models.ruleExecutionResult import RuleType, PolicyFilter
from acceldata_sdk.models.tags import AssetLabel, CustomAssetMetadata

from . import test_constants as test_const

pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger(__name__)


# ============================================================
# TORCH VERSION
# ============================================================

@pytest.mark.integration
def test_get_torch_version(adoc_client):
    version = adoc_client.get_torch_version()
    logger.info("Torch version: %s", version)
    assert version is not None


@pytest.mark.integration
def test_get_supported_sdk_versions(adoc_client):
    versions = adoc_client.get_supported_sdk_versions()
    logger.info("Supported SDK versions: %s", versions)
    assert versions is not None


# ============================================================
# PIPELINE
# ============================================================

@pytest.mark.integration
def test_create_pipeline(adoc_client):
    meta = PipelineMetadata(
        owner="sdk/pipeline-user",
        team="TORCH",
        codeLocation="...",
    )

    pipeline = CreatePipeline(
        uid=test_const.PIPELINE_UID,
        name=test_const.PIPELINE_NAME,
        description="Created from torch-sdk",
        meta=meta,
        context={
            "pipeline_uid": test_const.PIPELINE_UID,
            "pipeline_name": test_const.PIPELINE_NAME,
        },
    )

    res = adoc_client.create_pipeline(pipeline)
    fetched = adoc_client.get_pipeline(res.id)

    assert fetched is not None


@pytest.mark.integration
def test_get_pipeline_by_uid(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    assert pipeline is not None


@pytest.mark.integration
def test_create_pipeline_run(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.create_pipeline_run()
    fetched = pipeline.get_run(run.id)
    assert run == fetched


@pytest.mark.integration
def test_create_pipeline_run_with_continuation_id(adoc_client):
    pipeline = adoc_client.create_pipeline(
        CreatePipeline(
            uid=test_const.PIPELINE_UID_CONTINUATION,
            name=test_const.PIPELINE_UID_CONTINUATION,
        )
    )

    run = pipeline.create_pipeline_run(
        continuation_id=f"run.{random.random()}"
    )

    fetched = pipeline.get_run(run.id)
    assert fetched == run


@pytest.mark.integration
def test_get_pipelines(adoc_client):
    pipelines = adoc_client.get_pipelines()
    assert pipelines


@pytest.mark.integration
def test_latest_pipeline_run(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    latest = pipeline.get_latest_pipeline_run()
    runs = pipeline.get_runs()
    assert latest == runs[0]


# ============================================================
# SPANS & JOBS
# ============================================================

@pytest.mark.integration
def test_create_root_span(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()
    span = run.create_span(uid=f"{test_const.PIPELINE_UID}.span")
    assert span is not None


@pytest.mark.integration
def test_create_job_pipeline(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    job = CreateJob(
        uid=test_const.JOB_UID_READ,
        name="customers read",
        pipeline_run_id=run.id,
        inputs=[Node(asset_uid="S3-DS.s3_customers")],
        outputs=[Node(job_uid=test_const.JOB_UID_GENERATE)],
        meta=JobMetadata("DR", "DR team", "https://github.com"),
        context={"time": str(datetime.now())},
        bounded_by_span=True,
        span_uid=f"{test_const.JOB_UID_READ}.span",
    )

    created = pipeline.create_job(job)
    span = run.get_span(f"{test_const.JOB_UID_READ}.span")
    span.end()

    assert created is not None


@pytest.mark.integration
def test_create_child_span(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    parent = run.get_span(f"{test_const.PIPELINE_UID}.span")

    child = parent.create_child_span(
        uid=f"{test_const.JOB_UID_SALES}.span",
        context_data={"time": str(datetime.now())},
        associatedJobUids=[test_const.JOB_UID_SALES],
    )

    child.start()
    child.send_event(
        GenericEvent(
            event_uid="customers.data.metadata",
            context_data={"files": 1},
        )
    )
    child.send_event(
        LogEvent(
            log_data="Sales aggregated",
            context_data={"rows": 100},
        )
    )
    child.end()

    assert child is not None


@pytest.mark.integration
def test_pipeline_run_details(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()
    details = run.get_details()
    assert details is not None


@pytest.mark.integration
def test_update_pipeline_run(adoc_client):
    pipeline = adoc_client.get_pipeline(test_const.PIPELINE_UID)
    run = pipeline.get_latest_pipeline_run()

    res = run.update_pipeline_run(
        context_data={"env": "backend"},
        result=PipelineRunResult.SUCCESS,
        status=PipelineRunStatus.COMPLETED,
    )

    assert res is not None


@pytest.mark.integration
def test_delete_pipeline(adoc_client):
    pipeline = adoc_client.get_pipeline(
        test_const.PIPELINE_UID_CONTINUATION
    )
    res = pipeline.delete()
    assert res is not None


# ============================================================
# DQ POLICY
# ============================================================

@pytest.mark.integration
def test_get_dq_policy(adoc_client):
    policy = adoc_client.get_policy(
        const.PolicyType.DATA_QUALITY,
        test_const.DQ_POLICY_NAME,
    )
    assert policy is not None


@pytest.mark.integration
def test_list_dq_policies(adoc_client):
    rules = adoc_client.list_all_policies(
        filter=PolicyFilter(
            policyType=RuleType.DATA_QUALITY,
            enable=True,
        )
    )
    assert rules


# ============================================================
# RECON POLICY
# ============================================================

@pytest.mark.integration
def test_get_recon_policy(adoc_client):
    policy = adoc_client.get_policy(
        const.PolicyType.RECONCILIATION,
        test_const.RECON_POLICY_NAME,
    )
    assert policy is not None


# ============================================================
# DATASOURCE
# ============================================================

@pytest.mark.integration
def test_get_datasource(adoc_client):
    ds = adoc_client.get_datasource(test_const.DS_NAME, True)
    assert ds is not None


@pytest.mark.integration
def test_get_datasource_by_id(adoc_client):
    ds = adoc_client.get_datasource(test_const.DS_NAME, True)
    ds_by_id = adoc_client.get_datasource(ds.id, False)
    assert ds_by_id is not None


@pytest.mark.integration
def test_start_crawler(adoc_client):
    ds = adoc_client.get_datasource(test_const.DS_NAME, False)
    try:
        res = ds.start_crawler()
    except APIError as e:
        logger.info(e)

        msg = str(e)

        if "422" in msg and "Unable to start the Crawler" in msg:
            pytest.skip("Unable to start the Crawler")

        raise


# ============================================================
# ASSETS
# ============================================================

@pytest.mark.integration
def test_get_asset(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID_TABLE)
    assert asset is not None


@pytest.mark.integration
def test_asset_metadata(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID_TABLE)
    metadata = asset.get_metadata()
    assert metadata is not None


@pytest.mark.integration
def test_asset_labels(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID_TABLE)
    labels = asset.get_labels()
    assert labels is not None


@pytest.mark.integration
def test_add_asset_labels(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID_TABLE)
    asset.add_labels(
        [
            AssetLabel("sdk", "test"),
        ]
    )
    labels = asset.get_labels()
    assert labels is not None


@pytest.mark.integration
def test_asset_custom_metadata(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID_TABLE)
    asset.add_custom_metadata(
        [
            CustomAssetMetadata("sdk_key", "sdk_value"),
        ]
    )
    metadata = asset.get_metadata()
    assert metadata is not None


# ============================================================
# PROFILING
# ============================================================

@pytest.mark.integration
def test_execute_profile(adoc_client):
    asset = adoc_client.get_asset(test_const.ASSET_UID_TABLE)

    try:
        profile = asset.start_profile(ProfilingType.FULL)
        status = profile.get_status()
        assert status is not None

    except APIError as e:
        logger.info(e)

        msg = str(e)

        if "422" in msg and "Asset cannot be profiled" in msg:
            pytest.skip("Asset not profileable in current environment")

        raise
