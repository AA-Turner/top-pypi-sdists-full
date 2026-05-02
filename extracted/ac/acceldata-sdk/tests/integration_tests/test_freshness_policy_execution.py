import logging
import pytest

import acceldata_sdk.constants as const
from acceldata_sdk.constants import FailureStrategy
from acceldata_sdk.models.ruleExecutionResult import PolicyFilter, RuleType

from . import test_constants as test_const
from ..commons.retry import retry_operation

logger = logging.getLogger(__name__)

FRESHNESS_POLICY_NAME = test_const.FRESHNESS_POLICY_NAME


# =====================================================
# Get freshness policy by name
# =====================================================
@pytest.mark.integration
def test_get_freshness_policy_by_name(adoc_client):
    def operation():
        return adoc_client.get_policy(
            const.PolicyType.DATA_CADENCE,
            FRESHNESS_POLICY_NAME
        )

    policy = retry_operation(
        operation,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    logger.info("Fetched freshness policy by name: %s", policy)
    assert policy is not None


# =====================================================
# List freshness policies by filter
# =====================================================
@pytest.mark.integration
def test_get_freshness_policy_by_filter(adoc_client):
    policy_filter = PolicyFilter(
        policyType=RuleType.DATA_CADENCE,
        enable=True
    )

    def operation():
        return adoc_client.list_all_policies(filter=policy_filter)

    policies = retry_operation(
        operation,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    logger.info("Fetched freshness policies: %s", policies)
    assert policies is not None


# =====================================================
# Execute freshness policy
# =====================================================
@pytest.fixture(scope="module")
def freshness_execution_id(adoc_client):
    def get_policy_op():
        return adoc_client.get_policy(identifier=FRESHNESS_POLICY_NAME)

    policy = retry_operation(
        get_policy_op,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    def execute_op():
        return adoc_client.execute_freshness_rule(
            rule_id=policy.id
        )

    execution = retry_operation(
        execute_op,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    logger.info("Freshness policy execution started: %s", execution)
    return execution.id





# =====================================================
# Get freshness rule result
# =====================================================
@pytest.mark.integration
def test_freshness_policy_rule_result(
        adoc_client,
        freshness_execution_id
):
    logger.info("Freshness execution id: %s",freshness_execution_id)
    def operation():
        return adoc_client.get_freshness_rule_result(
            freshness_execution_id
        )

    result = retry_operation(
        operation,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    logger.info("Freshness rule result: %s", result)
    assert result is not None


# =====================================================
# Execute policy sync
# =====================================================
@pytest.mark.integration
def test_execute_policy_sync(adoc_client):
    def get_policy_op():
        return adoc_client.get_policy(identifier=FRESHNESS_POLICY_NAME)

    policy = retry_operation(
        get_policy_op,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    def execute_op():
        return adoc_client.execute_policy(
            const.PolicyType.DATA_CADENCE,
            policy.id,
            sync=True,
            failure_strategy=FailureStrategy.DoNotFail
        )

    executor = retry_operation(
        execute_op,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    def result_op():
        return executor.get_result(
            failure_strategy=FailureStrategy.DoNotFail
        )

    result = retry_operation(
        result_op,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    logger.info("Sync execution result: %s", result)
    logger.info("Execution status: %s", executor.get_status())


# =====================================================
# Execute async and cancel
# =====================================================
@pytest.mark.integration
def test_execute_policy_async_and_cancel(adoc_client):
    def get_policy_op():
        return adoc_client.get_policy(identifier=FRESHNESS_POLICY_NAME)

    policy = retry_operation(
        get_policy_op,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    def execute_op():
        return adoc_client.execute_policy(
            const.PolicyType.DATA_CADENCE,
            policy.id,
            sync=False,
            failure_strategy=FailureStrategy.DoNotFail
        )

    async_executor = retry_operation(
        execute_op,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL
    )

    # Important safety check
    if not async_executor or not getattr(async_executor, "id", None):
        logger.warning(
            "Skipping cancel — async execution did not start"
        )
        return

    async_executor.cancel()
    logger.info("Async execution cancelled")

    logger.info("Async execution cancelled", )
