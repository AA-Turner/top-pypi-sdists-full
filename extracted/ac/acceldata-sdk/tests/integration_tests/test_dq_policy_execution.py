import logging

import pytest
from acceldata_sdk.errors import TorchSdkException, APIError
from acceldata_sdk.models.common_types import (
    PolicyExecutionRequest,
    ExecutionType,
    AssetMarkerConfig,
    BoundsIdMarkerConfig,
    BoundsDateTimeMarkerConfig,
    BoundsFileEventMarkerConfig,
    TimestampBasedMarkerConfig,
    YunikornConfig,
    SparkResourceConfig,
    RuleSparkSQLDynamicFilterVariableMapping,
    Mapping,
)

from . import test_constants as test_const
from ..commons.retry import retry_operation

logger = logging.getLogger(__name__)


def execute_policy_or_accept_running(operation):
    try:
        return retry_operation(
            operation,
            test_const.MAX_RETRIES,
            test_const.RETRY_INTERVAL,
        )

    except APIError as e:
        msg = str(e)
        logger.info(msg)

        # ✅ ACCEPTABLE / PASS CONDITIONS
        if (
                "Previous execution of rule" in msg
                and "has not completed" in msg
        ):
            # Treat as success
            logger.info("Previous execution still running – accepting as PASS")
            return {"status": "ALREADY_RUNNING"}

        # ❌ Anything else is a real failure
        raise


@pytest.mark.integration
def test_execute_full_dq_backward_compatible(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.DQ_POLICY_BACKWARD_COMPATIBLE_NAME
    )

    logger.info("Executing FULL DQ (backward compatible)")

    def operation():
        return adoc_client.execute_dq_rule(rule_id=policy.id)

    result = execute_policy_or_accept_running(operation)
    logger.info("Execution result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_incremental_dq_backward_compatible(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.INCREMENTAL_DQ_POLICY_NAME
    )

    logger.info("Executing INCREMENTAL DQ (backward compatible)")

    def operation():
        return adoc_client.execute_dq_rule(
            rule_id=policy.id,
            incremental=True,
        )

    result = execute_policy_or_accept_running(operation)
    logger.info("Execution result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_full_dq_using_execution_request(adoc_client):
    policy = adoc_client.get_policy(identifier=test_const.DQ_POLICY_NAME)

    request = PolicyExecutionRequest(
        executionType=ExecutionType.FULL
    )

    logger.info("Executing FULL DQ using PolicyExecutionRequest")

    def operation():
        return adoc_client.execute_dq_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(operation)

    logger.info("Execution result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_incremental_dq_using_execution_request(adoc_client):
    policy = adoc_client.get_policy(identifier=test_const.INCREMENTAL_DQ_POLICY_NAME)

    request = PolicyExecutionRequest(
        executionType=ExecutionType.INCREMENTAL
    )

    logger.info("Executing INCREMENTAL DQ using PolicyExecutionRequest")

    def operation():
        return adoc_client.execute_dq_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(operation)

    logger.info("Execution result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_selective_dq_id_based(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.INCREMENTAL_DQ_ID
    )

    marker = BoundsIdMarkerConfig(
        idColumnName="ID",
        fromId=0,
        toId=1000,
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.SELECTIVE,
        markerConfigs=[
            AssetMarkerConfig(
                assetId=test_const.INCREMENTAL_DQ_DATE_TIME_ASSET_ID,
                markerConfig=marker,
            )
        ],
    )

    logger.info("Executing SELECTIVE DQ (ID based)")

    def operation():
        return adoc_client.execute_dq_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(operation)

    assert result is not None


@pytest.mark.integration
def test_execute_selective_dq_without_marker_config(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.INCREMENTAL_DQ_ID
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.SELECTIVE
    )

    logger.info("Executing SELECTIVE DQ without marker config")

    with pytest.raises(TorchSdkException):
        adoc_client.execute_dq_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )


@pytest.mark.integration
def test_execute_selective_dq_datetime_based(adoc_client):
    policy = adoc_client.get_policy(identifier=test_const.INCREMENTAL_DQ_DATE_TIME)

    marker = BoundsDateTimeMarkerConfig(
        dateColumnName="CURRENT_DATE",
        format="yyyy-MM-dd",
        fromDate="2023-07-01 00:00:00.000",
        toDate="2026-01-01 23:59:59.999",
        timeZoneId="Asia/Calcutta",
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.SELECTIVE,
        markerConfigs=[
            AssetMarkerConfig(
                assetId=test_const.INCREMENTAL_DQ_DATE_TIME_ASSET_ID,
                markerConfig=marker,
            )
        ],
    )

    def operation():
        return adoc_client.execute_dq_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(operation)

    assert result is not None


@pytest.mark.integration
def test_execute_selective_dq_file_event_based(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.FILE_EVENT_BASED_DQ_POLICY
    )

    marker = BoundsFileEventMarkerConfig(
        fromDate="2026-01-01 00:00:00.000",
        toDate="2026-02-06 23:59:59.999",
        timeZoneId="Asia/Calcutta",
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.SELECTIVE,
        markerConfigs=[
            AssetMarkerConfig(
                assetId=test_const.FILE_EVENT_BASED_DQ_BACKING_ASSET_ID,
                markerConfig=marker,
            )
        ],
    )

    def operation():
        return adoc_client.execute_dq_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(operation)

    assert result is not None


@pytest.mark.integration
def test_execute_selective_dq_kafka_timestamp_based(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.KAFKA_DQ_POLICY_NAME
    )

    marker = TimestampBasedMarkerConfig(
        format="yyyy-mm-dd",
        initialOffset="2023-06-01",
        timeZoneId="Asia/Calcutta",
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.SELECTIVE,
        markerConfigs=[
            AssetMarkerConfig(
                assetId=test_const.KAFKA_DQ_POLICY_BACKING_ASSET_ID,
                markerConfig=marker,
            )
        ],
    )

    def operation():
        return adoc_client.execute_dq_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(operation)

    assert result is not None
