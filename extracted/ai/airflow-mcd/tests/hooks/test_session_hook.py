from typing import Optional
from unittest import TestCase
from unittest.mock import patch, ANY, Mock

from airflow import AirflowException
from airflow.models import Connection
from pycarlo.core import Session, Client

from airflow_mcd.hooks import SessionHook

SAMPLE_ID = 'foo'
SAMPLE_TOKEN = 'bar'
SAMPLE_CONN_ID = 'mcd_default_session'


class SessionHookTest(TestCase):
    def setUp(self) -> None:
        self._session = SessionHook(mcd_session_conn_id=SAMPLE_CONN_ID)

    def test_session_id_is_set(self):
        self.assertEqual(self._session.mcd_session_conn_id, SAMPLE_CONN_ID)

    @patch('airflow_mcd.hooks.session_hook.Session')
    @patch.object(SessionHook, 'get_connection')
    def test_get_conn_with_extra(self, get_connection_mock, session_mock):
        get_connection_mock.return_value = Connection(extra={
            'mcd_id': SAMPLE_ID,
            'mcd_token': SAMPLE_TOKEN
        })
        expected_session = Session(mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN)
        session_mock.return_value = expected_session

        self.assertEqual(self._session.get_conn(), expected_session)
        get_connection_mock.assert_called_once_with(SAMPLE_CONN_ID)
        session_mock.assert_called_once_with(mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN)

    @patch('airflow_mcd.hooks.session_hook.Session')
    @patch.object(SessionHook, 'get_connection')
    def test_get_conn_with_login_and_password(self, get_connection_mock, session_mock):
        get_connection_mock.return_value = Connection(login=SAMPLE_ID, password=SAMPLE_TOKEN)
        expected_session = Session(mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN)
        session_mock.return_value = expected_session

        self.assertEqual(self._session.get_conn(), expected_session)
        get_connection_mock.assert_called_once_with(SAMPLE_CONN_ID)
        session_mock.assert_called_once_with(mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN)

    @patch('airflow_mcd.hooks.session_hook.Session')
    @patch.object(SessionHook, 'get_connection')
    def test_get_conn_with_non_default_host(self, get_connection_mock, session_mock):
        host = 'http://localhost:8080'
        get_connection_mock.return_value = Connection(host=host, login=SAMPLE_ID, password=SAMPLE_TOKEN)
        expected_session = Session(mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN)
        session_mock.return_value = expected_session

        self.assertEqual(self._session.get_conn(), expected_session)
        get_connection_mock.assert_called_once_with(SAMPLE_CONN_ID)
        session_mock.assert_called_once_with(
            endpoint=f'{host}/graphql',
            mcd_id=SAMPLE_ID,
            mcd_token=SAMPLE_TOKEN
        )

    @patch('airflow_mcd.hooks.session_hook.Session')
    @patch.object(SessionHook, 'get_connection')
    def test_get_conn_with_non_default_host_including_path(self, get_connection_mock, session_mock):
        host = 'http://localhost:8080/graphql'
        get_connection_mock.return_value = Connection(host=host, login=SAMPLE_ID, password=SAMPLE_TOKEN)
        expected_session = Session(mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN)
        session_mock.return_value = expected_session

        self.assertEqual(self._session.get_conn(), expected_session)
        get_connection_mock.assert_called_once_with(SAMPLE_CONN_ID)
        session_mock.assert_called_once_with(
            endpoint=host,
            mcd_id=SAMPLE_ID,
            mcd_token=SAMPLE_TOKEN
        )

    @patch.object(SessionHook, 'get_connection')
    def test_get_conn_with_incomplete_config(self, get_connection_mock):
        get_connection_mock.return_value = Connection()

        with self.assertRaises(AirflowException) as context:
            self._session.get_conn()
        self.assertEqual(str(context.exception), 'Missing expected key \'mcd_id\' from connection extra.')

    @patch("airflow_mcd.hooks.session_hook.Session")
    @patch.object(SessionHook, "get_connection")
    @patch("requests.request")
    def test_get_gw_conn(self, mock_request, get_connection_mock, session_mock):
        host = "https://integrations.getmontecarlo.com"
        # when path is not specified, we initialize the session with /graphql, but that's ignored
        # later in make_request
        self._test_gw_conn(
            mock_request,
            get_connection_mock,
            session_mock,
            host,
            f"{host}/graphql"
        )

    @patch("airflow_mcd.hooks.session_hook.Session")
    @patch.object(SessionHook, "get_connection")
    @patch("requests.request")
    def test_get_gw_conn_trailing_slash(self, mock_request, get_connection_mock, session_mock):
        self._test_gw_conn(
            mock_request,
            get_connection_mock,
            session_mock,
            "https://integrations.getmontecarlo.com/"
        )

    @patch("airflow_mcd.hooks.session_hook.Session")
    @patch.object(SessionHook, "get_connection")
    @patch("requests.request")
    def test_get_gw_conn_any_path(self, mock_request, get_connection_mock, session_mock):
        self._test_gw_conn(
            mock_request,
            get_connection_mock,
            session_mock,
            "https://integrations.getmontecarlo.com/ignored/path"
        )

    def _test_gw_conn(
        self,
        mock_request: Mock,
        get_connection_mock: Mock,
        session_mock: Mock,
        host: str,
        expected_endpoint: Optional[str] = None,
    ):
        expected_endpoint = expected_endpoint or host
        get_connection_mock.return_value = Connection(
            host=host, login=SAMPLE_ID, password=SAMPLE_TOKEN
        )
        expected_session = Session(mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN, endpoint=host, scope="AirflowCallbacks")
        session_mock.return_value = expected_session

        self.assertEqual(self._session.get_conn(), expected_session)
        get_connection_mock.assert_called_once_with(SAMPLE_CONN_ID)
        session_mock.assert_called_once_with(
            endpoint=expected_endpoint, mcd_id=SAMPLE_ID, mcd_token=SAMPLE_TOKEN, scope="AirflowCallbacks"
        )

        client = Client(self._session.get_conn())
        client.make_request("/airflow/callbacks", body={})
        mock_request.assert_called_once_with(
            url='https://integrations.getmontecarlo.com/airflow/callbacks',
            method='POST',
            json={},
            headers={
                "x-mcd-id": "foo",
                "x-mcd-token": "bar",
                "x-mcd-session-id": ANY,
                "x-mcd-trace-id": ANY,
                "x-mcd-telemetry-reason": "user",
            },
            timeout=10,
        )
