from unittest import TestCase
from unittest.mock import patch

from airflow_mcd.operators.base_operator import BaseMcdOperator

SAMPLE_CONN = 'foo'
SAMPLE_CONN_ID = 'mcd_default_session'


class MockSession:
    @staticmethod
    def get_conn():
        return SAMPLE_CONN


class BaseOpTest(TestCase):
    def setUp(self) -> None:
        self._op = BaseMcdOperator(mcd_session_conn_id=SAMPLE_CONN_ID, task_id='test')

    @patch('airflow_mcd.operators.base_operator.SessionHook')
    def test_get_session(self, mock_session):
        mock_session.return_value = MockSession
        self.assertEqual(self._op.get_session(), SAMPLE_CONN)
        mock_session.assert_called_once_with(mcd_session_conn_id=SAMPLE_CONN_ID)
