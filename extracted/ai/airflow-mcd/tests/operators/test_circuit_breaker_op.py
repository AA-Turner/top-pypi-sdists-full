from unittest import TestCase
from unittest.mock import patch

from airflow import AirflowException
from airflow.exceptions import AirflowSkipException

from airflow_mcd.operators import SimpleCircuitBreakerOperator

SAMPLE_CONN_ID = 'mcd_default_session'
SAMPLE_RULE_ID = 'foo'
SAMPLE_RULE_NAME = 'rule_name'
SAMPLE_NAMESPACE = 'namespace'
SAMPLE_TIMEOUT_IN_MINUTES = 10
SAMPLE_FAIL_OPEN = False


class CbOpTest(TestCase):
    def setUp(self) -> None:
        self._op = SimpleCircuitBreakerOperator(
            mcd_session_conn_id=SAMPLE_CONN_ID,
            rule_uuid=SAMPLE_RULE_ID,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            fail_open=SAMPLE_FAIL_OPEN,
            task_id='test'
        )

    def test_initialization(self):
        self.assertEqual(self._op.rule_uuid, SAMPLE_RULE_ID)
        self.assertEqual(self._op.timeout_in_minutes, SAMPLE_TIMEOUT_IN_MINUTES)
        self.assertEqual(self._op.fail_open, SAMPLE_FAIL_OPEN)
        self.assertEqual(self._op.mcd_session_conn_id, SAMPLE_CONN_ID)

    @patch.object(SimpleCircuitBreakerOperator, 'get_session')
    @patch('airflow_mcd.operators.circuit_breaker_operators.CircuitBreakerService')
    def test_execute_no_breach(self, cd_mock, get_session_mock):
        cd_mock().trigger_and_poll.return_value = False

        self.assertIsNone(self._op.execute())
        cd_mock().trigger_and_poll.assert_called_once_with(
            rule_uuid=SAMPLE_RULE_ID,
            namespace=None,
            rule_name=None,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            runtime_variables=None
        )
        get_session_mock.assert_called_once_with()

    @patch.object(SimpleCircuitBreakerOperator, 'get_session')
    @patch('airflow_mcd.operators.circuit_breaker_operators.CircuitBreakerService')
    def test_execute_no_breach_with_rule_name_and_namespace(self, cd_mock, get_session_mock):
        cd_mock().trigger_and_poll.return_value = False

        operator = SimpleCircuitBreakerOperator(
            mcd_session_conn_id=SAMPLE_CONN_ID,
            rule_name=SAMPLE_RULE_NAME,
            namespace=SAMPLE_NAMESPACE,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            fail_open=SAMPLE_FAIL_OPEN,
            task_id='test1'
        )

        self.assertIsNone(operator.execute())
        cd_mock().trigger_and_poll.assert_called_once_with(
            rule_uuid=None,
            namespace=SAMPLE_NAMESPACE,
            rule_name=SAMPLE_RULE_NAME,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            runtime_variables=None
        )
        get_session_mock.assert_called_once_with()

    @patch.object(SimpleCircuitBreakerOperator, 'get_session')
    @patch('airflow_mcd.operators.circuit_breaker_operators.CircuitBreakerService')
    def test_execute_no_breach_with_rule_name(self, cd_mock, get_session_mock):
        cd_mock().trigger_and_poll.return_value = False

        operator = SimpleCircuitBreakerOperator(
            mcd_session_conn_id=SAMPLE_CONN_ID,
            rule_name=SAMPLE_RULE_NAME,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            fail_open=SAMPLE_FAIL_OPEN,
            task_id='test2'
        )

        self.assertIsNone(operator.execute())
        cd_mock().trigger_and_poll.assert_called_once_with(
            rule_uuid=None,
            namespace=None,
            rule_name=SAMPLE_RULE_NAME,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            runtime_variables=None
        )
        get_session_mock.assert_called_once_with()

    @patch.object(SimpleCircuitBreakerOperator, 'get_session')
    @patch('airflow_mcd.operators.circuit_breaker_operators.CircuitBreakerService')
    def test_execute_with_breach(self, cd_mock, get_session_mock):
        cd_mock().trigger_and_poll.return_value = True

        with self.assertRaises(AirflowException) as context:
            self._op.execute()
        self.assertEqual(str(context.exception), f'Rule \'{SAMPLE_RULE_ID}\' is in breach!')
        cd_mock().trigger_and_poll.assert_called_once_with(
            rule_uuid=SAMPLE_RULE_ID,
            namespace=None,
            rule_name=None,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            runtime_variables=None
        )
        get_session_mock.assert_called_once_with()

    @patch.object(SimpleCircuitBreakerOperator, 'get_session')
    @patch('airflow_mcd.operators.circuit_breaker_operators.CircuitBreakerService')
    def test_execute_with_breach_and_fail_closed(self, cd_mock, get_session_mock):
        cd_mock().trigger_and_poll.side_effect = ValueError

        with self.assertRaises(AirflowException):
            self._op.execute()
        cd_mock().trigger_and_poll.assert_called_once_with(
            rule_uuid=SAMPLE_RULE_ID,
            namespace=None,
            rule_name=None,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            runtime_variables=None
        )
        get_session_mock.assert_called_once_with()

    @patch.object(SimpleCircuitBreakerOperator, 'get_session')
    @patch('airflow_mcd.operators.circuit_breaker_operators.CircuitBreakerService')
    def test_execute_with_breach_and_fail_open(self, cd_mock, get_session_mock):
        op = SimpleCircuitBreakerOperator(
            mcd_session_conn_id=SAMPLE_CONN_ID,
            rule_uuid=SAMPLE_RULE_ID,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            fail_open=True,
            task_id='test'
        )
        cd_mock().trigger_and_poll.side_effect = ValueError

        with self.assertRaises(AirflowSkipException) as context:
            op.execute()
        cd_mock().trigger_and_poll.assert_called_once_with(
            rule_uuid=SAMPLE_RULE_ID,
            namespace=None,
            rule_name=None,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            runtime_variables=None
        )
        get_session_mock.assert_called_once_with()
        self.assertEqual((str(context.exception)), 'Encountered an error when executing the rule, but failing open.')

    @patch.object(SimpleCircuitBreakerOperator, 'get_session')
    @patch('airflow_mcd.operators.circuit_breaker_operators.CircuitBreakerService')
    def test_execute_with_variables(self, cd_mock, get_session_mock):
        op = SimpleCircuitBreakerOperator(
            mcd_session_conn_id=SAMPLE_CONN_ID,
            rule_uuid=SAMPLE_RULE_ID,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            fail_open=SAMPLE_FAIL_OPEN,
            task_id='test',
            runtime_variables={"var1": "value1"}
        )

        cd_mock().trigger_and_poll.return_value = False

        self.assertIsNone(op.execute())
        cd_mock().trigger_and_poll.assert_called_once_with(
            rule_uuid=SAMPLE_RULE_ID,
            namespace=None,
            rule_name=None,
            timeout_in_minutes=SAMPLE_TIMEOUT_IN_MINUTES,
            runtime_variables={"var1": "value1"}
        )
        get_session_mock.assert_called_once_with()