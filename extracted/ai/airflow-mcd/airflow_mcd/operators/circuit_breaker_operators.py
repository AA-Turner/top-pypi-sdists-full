from typing import Dict, Union, Optional
from uuid import UUID

from airflow import AirflowException
from pycarlo.core import Client
from pycarlo.features.circuit_breakers import CircuitBreakerService

from airflow_mcd.operators.base_operator import BaseMcdOperator

try:
    # Use AirflowFailException if available as that is preferred for tasks that can be failed without retrying.
    # https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/exceptions/index.html#airflow.exceptions.AirflowFailException
    from airflow.exceptions import AirflowFailException, AirflowSkipException

    BREACH_EXCEPTION = AirflowFailException
except:
    BREACH_EXCEPTION = AirflowException
    OP_RETRIES = 0
else:
    OP_RETRIES = None


class SimpleCircuitBreakerOperator(BaseMcdOperator):
    def __init__(self,
                 mcd_session_conn_id: str,
                 rule_uuid: Optional[Union[str, UUID]] = None,
                 namespace: Optional[str] = None,
                 rule_name: Optional[str] = None,
                 timeout_in_minutes: Optional[int] = 5,
                 fail_open: Optional[bool] = True,
                 runtime_variables: Optional[Dict[str, str]] = None,
                 *args, **kwargs):
        """
        Operator for Circuit breaking rules (custom SQL monitors) with MCD.

        Raises an AirflowFailException if the rule condition is in breach when using an Airflow version newer
        than 1.10.11, as that is preferred for tasks that can be failed without retrying.

        Older Airflow versions raise an AirflowException In this case retries are also set to zero as this operator is
        not intended to be retried.

        :param mcd_session_conn_id: Connection ID for the MCD session.
        :param rule_uuid: UUID of the rule (custom SQL monitor) to execute. Either the rule_uuid or the rule_name
        must be specified
        :param namespace: Namespace of the rule (custom SQL monitor) to execute.
        :param rule_name: name of the rule (custom SQL monitor) to execute.
        :param timeout_in_minutes: Polling timeout in minutes. Note that The Data Collector Lambda has a max timeout of
        15 minutes when executing a query. Queries that take longer to execute are not supported, so we recommend
        filtering down the query output to improve performance (e.g limit WHERE clause). If you expect a query to
        take the full 15 minutes we recommend padding the timeout to 20 minutes.
        :param fail_open: Prevent any errors or timeouts when executing a rule from stopping your pipeline.
        :param runtime_variables: Runtime variables to pass to the rule.
        Raises AirflowSkipException if set to True.
        """
        retry_handler = dict(retries=OP_RETRIES) if OP_RETRIES is not None else {}
        super().__init__(mcd_session_conn_id=mcd_session_conn_id, *args, **kwargs, **retry_handler)

        self.rule_uuid = rule_uuid
        self.namespace = namespace
        self.rule_name = rule_name
        self.timeout_in_minutes = timeout_in_minutes
        self.fail_open = fail_open
        self.runtime_variables = runtime_variables

    def execute(self, *args, **kwargs) -> None:
        """
        Execute the circuit breaker operator.
        """
        service = CircuitBreakerService(mc_client=Client(self.get_session()), print_func=self.log.info)
        try:
            in_breach = service.trigger_and_poll(rule_uuid=self.rule_uuid,
                                                 namespace=self.namespace,
                                                 rule_name=self.rule_name,
                                                 timeout_in_minutes=self.timeout_in_minutes,
                                                 runtime_variables=self.runtime_variables)
        except Exception as err:
            if not self.fail_open:
                raise AirflowException from err

            message = 'Encountered an error when executing the rule, but failing open.'
            self.log.exception(message)
            raise AirflowSkipException(message)
        else:
            if in_breach:
                raise BREACH_EXCEPTION(f'Rule \'{self.rule_uuid}\' is in breach!')
            self.log.info(f'Rule \'{self.rule_uuid}\' is not in breach.')
