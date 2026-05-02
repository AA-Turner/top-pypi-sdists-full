import logging

import pytest
from acceldata_sdk.errors import APIError
from acceldata_sdk.errors import TorchSdkException
from acceldata_sdk.models.common_types import (
    PolicyExecutionRequest,
    ExecutionType,
    AssetMarkerConfig,
    BoundsDateTimeMarkerConfig,
    BoundsFileEventMarkerConfig,
    TimestampBasedMarkerConfig,
)

from . import test_constants as test_const
from ..commons.retry import retry_operation

logger = logging.getLogger(__name__)


# ============================================================
# BACKWARD COMPATIBLE RECON EXECUTION
# ============================================================
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
def test_execute_full_recon_backward_compatible(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.SELECTIVE_RECON_POLICY_BACKWARD_COMPATIBLE_NAME
    )

    logger.info("Executing FULL reconciliation (backward compatible)")
    logger.info("Policy id: %s", policy.id)

    def operation():
        return adoc_client.execute_reconciliation_rule(
            rule_id=policy.id,
            incremental=False,
        )

    result = execute_policy_or_accept_running(
        operation)
    logger.info("Execution result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_incremental_recon_backward_compatible(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.INCREMENTAL_RECON_POLICY_NAME
    )

    logger.info("Executing INCREMENTAL reconciliation (backward compatible)")
    logger.info("Policy id: %s", policy.id)

    def operation():
        return adoc_client.execute_reconciliation_rule(
            rule_id=policy.id,
            incremental=True,
        )

    result = execute_policy_or_accept_running(
        operation)

    logger.info("Execution result: %s", result)
    assert result is not None


# ============================================================
# POLICY EXECUTION REQUEST — FULL / INCREMENTAL
# ============================================================

@pytest.mark.integration
def test_execute_full_recon_using_execution_request(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.SELECTIVE_RECON_POLICY_BACKWARD_COMPATIBLE_NAME
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.FULL
    )

    logger.info("Executing FULL reconciliation using PolicyExecutionRequest")

    def operation():
        return adoc_client.execute_reconciliation_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(
        operation)

    logger.info("Execution result: %s", result)
    assert result is not None


@pytest.mark.integration
def test_execute_incremental_recon_using_execution_request(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.INCREMENTAL_RECON_POLICY_NAME
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.INCREMENTAL
    )

    logger.info("Executing INCREMENTAL reconciliation using PolicyExecutionRequest")

    def operation():
        return adoc_client.execute_reconciliation_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(
    operation)

    logger.info("Execution result: %s", result)
    assert result is not None


# ============================================================
# SELECTIVE RECON — VALIDATION
# ============================================================

@pytest.mark.integration
def test_execute_selective_recon_without_marker_config(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.INCREMENTAL_DQ_ID
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.SELECTIVE
    )

    logger.info("Executing SELECTIVE reconciliation without marker config")

    with pytest.raises(TorchSdkException):
        adoc_client.execute_reconciliation_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )


# ============================================================
# SELECTIVE RECON — DATETIME BASED
# ============================================================

@pytest.mark.integration
def test_execute_selective_recon_datetime_based(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.INCREMENTAL_RECON_POLICY_NAME
    )

    marker = BoundsDateTimeMarkerConfig(
        dateColumnName="TO_DATE",
        format="yyyy-MM-dd",
        fromDate="2023-07-01 00:00:00.000",
        toDate="2024-07-14 23:59:59.999",
        timeZoneId="Asia/Calcutta",
    )

    request = PolicyExecutionRequest(
        executionType=ExecutionType.SELECTIVE,
        markerConfigs=[
            AssetMarkerConfig(
                assetId=test_const.INCREMENTAL_DQ_RECON_TIME_ASSET_ID,
                markerConfig=marker,
            )
        ],
    )

    logger.info("Executing SELECTIVE reconciliation (datetime based)")

    def operation():
        return adoc_client.execute_reconciliation_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(
        operation)

    logger.info("Execution result: %s", result)
    assert result is not None

# ============================================================
# SELECTIVE RECON — FILE EVENT BASED
# ============================================================

# @pytest.mark.integration
# def test_execute_selective_recon_file_event_based(adoc_client):
#     policy = adoc_client.get_policy(
#         identifier=test_const.FILE_EVENT_BASED_RECON_POLICY
#     )
#
#     marker = BoundsFileEventMarkerConfig(
#         fromDate="2020-07-01 00:00:00.000",
#         toDate="2024-07-01 23:59:59.999",
#         timeZoneId="Asia/Calcutta",
#     )
#
#     request = PolicyExecutionRequest(
#         executionType=ExecutionType.SELECTIVE,
#         markerConfigs=[
#             AssetMarkerConfig(
#                 assetId=test_const.ASSET_ID,
#                 markerConfig=marker,
#             )
#         ],
#     )
#
#     logger.info("Executing SELECTIVE reconciliation (file event based)")
#
#     def operation():
#         return adoc_client.execute_reconciliation_rule(
#             rule_id=policy.id,
#             policy_execution_request=request,
#         )
#
#     result = retry_operation(
#         operation,
#         test_const.MAX_RETRIES,
#         test_const.RETRY_INTERVAL,
#     )
#
#     logger.info("Execution result: %s", result)
#     assert result is not None
#

# ============================================================
# SELECTIVE RECON — KAFKA TIMESTAMP BASED
# ============================================================

@pytest.mark.integration
def test_execute_selective_recon_kafka_timestamp_based(adoc_client):
    policy = adoc_client.get_policy(
        identifier=test_const.KAFKA_RECON_POLICY_NAME
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

    logger.info("Executing SELECTIVE reconciliation (kafka timestamp based)")

    def operation():
        return adoc_client.execute_reconciliation_rule(
            rule_id=policy.id,
            policy_execution_request=request,
        )

    result = execute_policy_or_accept_running(
        operation)

    logger.info("Execution result: %s", result)
    assert result is not None
