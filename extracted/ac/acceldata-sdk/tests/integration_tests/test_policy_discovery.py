import logging
import pprint
import pytest
import acceldata_sdk.constants as const

from acceldata_sdk.models.ruleExecutionResult import (
    RuleType,
    PolicyFilter,
)

from . import test_constants as test_const
from ..commons.retry import retry_operation

pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger()


# ============================================================
# DQ POLICY TESTS
# ============================================================

@pytest.mark.integration
def test_get_dq_policy(adoc_client):
    policy = adoc_client.get_policy(
        const.PolicyType.DATA_QUALITY,
        test_const.DQ_POLICY_NAME,
    )

    logger.info("DQ policy response:")
    logger.info(pp.pformat(policy))

    assert policy is not None


@pytest.mark.integration
def test_get_dq_policy_without_type(adoc_client):
    policy_response = adoc_client.get_policy(
        const.PolicyType.DATA_QUALITY,
        test_const.DQ_POLICY_NAME,
    )

    policy_by_id = adoc_client.get_policy(identifier=policy_response.rule.id)

    logger.info("DQ policy without type:")
    logger.info(pp.pformat(policy_by_id))

    assert policy_by_id is not None


@pytest.mark.integration
def test_list_all_dq_policies(adoc_client):
    filter_ = PolicyFilter(
        policyType=RuleType.DATA_QUALITY,
        enable=True,
    )

    policies = adoc_client.list_all_policies(filter=filter_)

    logger.info("DQ policies list:")
    logger.info(pp.pformat(policies))

    assert policies is not None


@pytest.mark.integration
def test_execute_dq_policy_async(adoc_client):
    policy = adoc_client.get_policy(
        type=const.PolicyType.DATA_QUALITY,
        identifier=test_const.DQ_POLICY_NAME,
    )

    def operation():
        return policy.execute(sync=False)

    executor = retry_operation(
        operation,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL,
    )

    if executor.errorMessage:
        pytest.skip(executor.errorMessage)

    status = executor.get_status()
    logger.info("DQ execution status:")
    logger.info(pp.pformat(status))

    result = executor.get_result()
    logger.info("DQ execution result:")
    logger.info(pp.pformat(result))

    assert result is not None


@pytest.mark.integration
def test_cancel_dq_policy(adoc_client):
    policy_response = adoc_client.get_policy(
        const.PolicyType.DATA_QUALITY,
        test_const.DQ_POLICY_NAME,
    )

    executor = policy_response.execute(sync=False)
    logger.info("executor:")
    logger.info(pp.pformat(executor))
    if executor.errorMessage:
        pytest.skip("Execution did not start")

    executor.cancel()
    rule_result = executor.get_result(executor.id)
    logger.info("DQ cancel response:")
    logger.info(pp.pformat(rule_result))

    assert rule_result is not None


@pytest.mark.integration
def test_get_dq_policy_executions(adoc_client):
    policy_response = adoc_client.get_policy(
        const.PolicyType.DATA_QUALITY,
        test_const.DQ_POLICY_NAME,
    )

    executions = adoc_client.policy_executions(
        policy_response.rule.id,
        RuleType.DATA_QUALITY,
    )

    logger.info("DQ executions:")
    logger.info(pp.pformat(executions))

    assert executions is not None


# ============================================================
# RECON POLICY TESTS
# ============================================================

@pytest.mark.integration
def test_get_recon_policy(adoc_client):
    policy = adoc_client.get_policy(
        const.PolicyType.RECONCILIATION,
        test_const.RECON_POLICY_NAME,
    )

    logger.info("Recon policy response:")
    logger.info(pp.pformat(policy))

    assert policy is not None


@pytest.mark.integration
def test_get_recon_policy_without_type(adoc_client):
    policy_response = adoc_client.get_policy(
        const.PolicyType.RECONCILIATION,
        test_const.RECON_POLICY_NAME,
    )

    policy_by_id = adoc_client.get_policy(identifier=policy_response.rule.id)

    logger.info("Recon policy without type:")
    logger.info(pp.pformat(policy_by_id))

    assert policy_by_id is not None


@pytest.mark.integration
def test_list_all_recon_policies(adoc_client):
    filter_ = PolicyFilter(
        policyType=RuleType.RECONCILIATION,
        enable=True,
    )

    policies = adoc_client.list_all_policies(filter=filter_)

    logger.info("Recon policies list:")
    logger.info(pp.pformat(policies))

    assert policies is not None


@pytest.mark.integration
def test_execute_recon_policy_async(adoc_client):
    policy_response = adoc_client.get_policy(
        const.PolicyType.RECONCILIATION,
        test_const.RECON_POLICY_NAME,
    )

    def operation():
        return policy_response.execute(sync=False)

    executor = retry_operation(
        operation,
        test_const.MAX_RETRIES,
        test_const.RETRY_INTERVAL,
    )

    if executor.errorMessage:
        pytest.skip(executor.errorMessage)

    status = executor.get_status()
    logger.info("Recon execution status:")
    logger.info(pp.pformat(status))

    result = executor.get_result()
    logger.info("Recon execution result:")
    logger.info(pp.pformat(result))

    assert result is not None


@pytest.mark.integration
def test_cancel_recon_policy(adoc_client):
    policy_response = adoc_client.get_policy(
        const.PolicyType.RECONCILIATION,
        test_const.RECON_POLICY_NAME,
    )

    executor = policy_response.execute(sync=False)

    if executor.errorMessage:
        pytest.skip("Execution did not start")

    executor.cancel()
    rule_result = executor.get_result(executor.id)
    logger.info("Recon cancel response:")
    logger.info(pp.pformat(rule_result))

    assert rule_result is not None


@pytest.mark.integration
def test_get_recon_policy_executions(adoc_client):
    policy_response = adoc_client.get_policy(
        const.PolicyType.RECONCILIATION,
        test_const.RECON_POLICY_NAME,
    )

    executions = adoc_client.policy_executions(
        policy_response.rule.id,
        RuleType.RECONCILIATION,
    )

    logger.info("Recon executions:")
    logger.info(pp.pformat(executions))

    assert executions is not None
