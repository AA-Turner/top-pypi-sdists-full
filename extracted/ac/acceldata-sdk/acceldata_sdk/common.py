from time import sleep
import logging
from acceldata_sdk.constants import RuleExecutionStatus, FailureStrategy, PolicyType
from acceldata_sdk.models.ruleExecutionResult import RuleResult, RuleExecutionSummary
from acceldata_sdk.models.common_types import PolicyExecutionRequest
from acceldata_sdk.errors import APIError, TorchSdkException

LOGGER = logging.getLogger("common")


def get_callables(rule_type, torch_client):
    LOGGER.info(f"Fetching the appropriate callable methods for the provided rule type: {rule_type.name}")
    if rule_type.value == PolicyType.RECONCILIATION.value:
        result_call = torch_client.get_reconciliation_rule_result
        exec_call = torch_client.execute_reconciliation_rule
    elif rule_type.value == PolicyType.DATA_QUALITY.value:
        result_call = torch_client.get_dq_rule_result
        exec_call = torch_client.execute_dq_rule
    elif rule_type.value == PolicyType.DATA_CADENCE.value:
        result_call = torch_client.get_freshness_rule_result
        exec_call = torch_client.execute_freshness_rule
    else:
        allowed_values = [t.value for t in PolicyType]
        raise TorchSdkException(f'{rule_type} not found. Please provide correct rule_type. '
                        f'Allowed values are: {", ".join(allowed_values)}')
    return exec_call, result_call

class Executor:
    def __init__(self, rule_type: PolicyType, torch_client, sync=False):
        self.id = None
        self.errorMessage = None
        self.sync = sync
        self.client = torch_client
        self.exec_call, self.result_call = get_callables(rule_type, torch_client)

    def is_id_valid(self):
        if self.id is None:
            execution_details = RuleResult()
            execution_details.execution = RuleExecutionSummary(
                executionStatus=RuleExecutionStatus.ERRORED, resultStatus=RuleExecutionStatus.ERRORED,
                executionError='valid execution_id is required.')
            LOGGER.info(execution_details.execution.executionError)
            return execution_details
        else:
            return True

    def get_status(self) -> RuleExecutionStatus:
        execution_id_check_passed = self.is_id_valid()
        if execution_id_check_passed is not True:
            return RuleExecutionStatus.ERRORED
        else:
            return self.get_execution_status(self.id)

    def get_execution_status(self, execution_id) -> RuleExecutionStatus:
        LOGGER.info('Getting rule execution status.')
        try:
            execution_details = self.result_call(execution_id=execution_id)
            return_value = RuleExecutionStatus[execution_details.execution.resultStatus]
        except APIError as e:
            LOGGER.info(f'get_status failed due to http error. Details:{e}')
            return_value = RuleExecutionStatus.ERRORED
        except Exception as e:
            return_value = RuleExecutionStatus.ERRORED
            LOGGER.info(f'get_status failed due to Exception. Details:{e}')
        return return_value

    def get_result(self, sleep_interval=5, total_retries=0, failure_strategy: FailureStrategy = FailureStrategy.DoNotFail) -> RuleResult:
        execution_id_check_passed = self.is_id_valid()
        if execution_id_check_passed is not True:
            if failure_strategy >= FailureStrategy.FailOnError:
                raise TorchSdkException(execution_id_check_passed.execution.executionError)
            else:
                return execution_id_check_passed
        else:
            return self.get_execution_result(self.id, sleep_interval, total_retries, failure_strategy)

    def get_execution_result(self, execution_id, sleep_interval=5, total_retries=0,
                             failure_strategy: FailureStrategy = FailureStrategy.DoNotFail) -> RuleResult:
        retry_count = 0
        try:
            while 1:
                execution_details = self.result_call(execution_id=execution_id)
                LOGGER.info(execution_details)
                if (RuleExecutionStatus[
                        execution_details.execution.executionStatus] == RuleExecutionStatus.RUNNING) or (
                        RuleExecutionStatus[
                            execution_details.execution.executionStatus] == RuleExecutionStatus.WAITING):
                    sleep(sleep_interval)
                    retry_count = retry_count + 1
                    if (total_retries == 0) or (total_retries > 0 and retry_count < total_retries):
                        continue
                    else:
                        execution_details.execution.executionError = f'Exiting after {total_retries} retries.'
                        LOGGER.info(execution_details.execution.executionError)
                        break
                else:
                    LOGGER.info('Rule completed.')
                    break
        except APIError as e:
            LOGGER.error(f'Rule execution failed due to http error. Details:{e}')
            execution_details = RuleResult()
            execution_details.execution = RuleExecutionSummary(
                executionStatus=RuleExecutionStatus.ERRORED, resultStatus=RuleExecutionStatus.ERRORED,
                executionError=f'Rule execution failed due to http error. Details:{e}')
            LOGGER.info(execution_details.execution.executionError)
            if failure_strategy >= FailureStrategy.FailOnError:
                raise TorchSdkException(execution_details.execution.executionError)
        except Exception as e:
            LOGGER.error(f'Rule execution failed due to http error. Details:{e}')
            execution_details = RuleResult()
            execution_details.execution = RuleExecutionSummary(
                executionStatus=RuleExecutionStatus.ERRORED, resultStatus=RuleExecutionStatus.ERRORED,
                executionError=f'Rule execution failed due to Exception. Details:{e}')
            LOGGER.info(execution_details.execution.executionError)
            if failure_strategy >= FailureStrategy.FailOnError:
                raise TorchSdkException(execution_details.execution.executionError)

        if RuleExecutionStatus[execution_details.execution.resultStatus] == RuleExecutionStatus.SUCCESSFUL:
            LOGGER.info('Rule completed successfully.')
        elif RuleExecutionStatus[execution_details.execution.resultStatus] == RuleExecutionStatus.WARNING:
            LOGGER.info('Rule completed with warnings.')
            if failure_strategy == FailureStrategy.FailOnWarning:
                raise TorchSdkException(f'Execution completed with warning. Details: {execution_details}')
        else:
            LOGGER.info(f'Rule execution completed with errors. Details:{execution_details}')
            if failure_strategy >= FailureStrategy.FailOnError:
                raise TorchSdkException(f'Rule execution completed with errors. Details: {execution_details}')
        return execution_details

    def execute(self, rule_id, incremental=False, sleep_interval=5, total_retries=0,
                failure_strategy: FailureStrategy = FailureStrategy.DoNotFail, pipeline_run_id=None,
                policy_execution_request: PolicyExecutionRequest = None):
        try:
            LOGGER.info(f"Policy Execution Request: {policy_execution_request.to_dict() if policy_execution_request else 'None'}")
            execution_obj = self.exec_call(rule_id=rule_id, incremental=incremental, pipeline_run_id=pipeline_run_id,
                                           policy_execution_request=policy_execution_request)
            self.id = execution_obj.id
            if self.sync:
                self.get_execution_result(self.id, sleep_interval, total_retries, failure_strategy)
        except APIError as e:
            self.errorMessage = f'Rule execution failed due to http error. Details:{e}'
            LOGGER.info(self.errorMessage)
            if failure_strategy >= FailureStrategy.FailOnError:
                raise TorchSdkException(self.errorMessage)
        except Exception as e:
            self.errorMessage = f'Rule execution failed due to Exception. Details:{e}'
            LOGGER.error(self.errorMessage)
            if failure_strategy >= FailureStrategy.FailOnError:
                raise TorchSdkException(self.errorMessage)

    def cancel(self):
        try:
            self.client.cancel_rule_execution(self.id)
        except APIError as e:
            self.errorMessage = f'Rule cancellation failed due to http error. Details:{e}'
            LOGGER.info(self.errorMessage)

        except Exception as e:
            self.errorMessage = f'Rule cancellation failed due to Exception. Details:{e}'
            LOGGER.info(self.errorMessage)


