from unittest import TestCase
from unittest.mock import Mock, patch
from urllib.parse import urljoin

from box import Box
from requests.exceptions import HTTPError, Timeout
from responses import activate, mock, post, registries

from pycarlo.common.errors import GqlError, InvalidSessionError
from pycarlo.common.retries import Backoff
from pycarlo.common.settings import (
    DEFAULT_MCD_API_ENDPOINT,
    DEFAULT_MCD_IGW_ENDPOINT,
    RequestReason,
)
from pycarlo.core import Client, Query, Session

MCD_API_ENDPOINT = DEFAULT_MCD_API_ENDPOINT
MCD_IGW_ENDPOINT = DEFAULT_MCD_IGW_ENDPOINT

MOCK_MCD_ID = "foo"
MOCK_MCD_TOKEN = "bar"
MOCK_SESSION_ID = "qux"
MOCK_TRACE_ID = "baz"
MOCK_USER_ID = "uid"
MOCK_HEADERS = {
    "x-mcd-id": MOCK_MCD_ID,
    "x-mcd-session-id": MOCK_SESSION_ID,
    "x-mcd-telemetry-reason": RequestReason.USER.value,
    "x-mcd-token": MOCK_MCD_TOKEN,
    "x-mcd-trace-id": MOCK_TRACE_ID,
    "user-id": MOCK_USER_ID,
}
MOCK_TIMEOUT = 16
MOCK_EMAIL = "dresden@montecarlodata.com"
MOCK_GET_USER_QUERY = """
query {
  getUser {
    email
  }
}
"""
MOCK_GOOD_RESPONSE = {"data": {"getUser": {"email": MOCK_EMAIL}}, "errors": []}

_AIRFLOW_SCOPE = "AirflowCallbacks"
_AIRFLOW_CALLBACKS_PATH = "/airflow/callbacks"


class MockBackoff(Backoff):
    def __init__(self, count: int):
        super(MockBackoff, self).__init__(start=0, maximum=0)
        self.count = count

    def backoff(self, attempt: int) -> float:
        return 0

    def delays(self):
        for i in range(self.count):
            yield 0


class ClientTest(TestCase):
    def setUp(self) -> None:
        self._session = Mock(spec=Session)
        self._session.endpoint = MCD_API_ENDPOINT
        self._session.scope = None
        self._backoff = MockBackoff(count=0)
        self._client = Client(session=self._session)

    def test_get_session_id(self):
        self._session.id = MOCK_MCD_ID
        self.assertEqual(self._client.session_id, MOCK_MCD_ID)

    def test_get_session_name(self):
        self._session.session_name = MOCK_SESSION_ID
        self.assertEqual(self._client.session_name, MOCK_SESSION_ID)

    def test_get_session_endpoint(self):
        endpoint = "test.com"
        self._session.endpoint = endpoint
        self.assertEqual(self._client.session_endpoint, endpoint)

    @patch("pycarlo.core.client.uuid")
    def test_get_headers(self, mock_uuid: Mock):
        self._session.id = MOCK_MCD_ID
        self._session.token = MOCK_MCD_TOKEN
        self._session.session_name = MOCK_SESSION_ID
        self._session.user_id = MOCK_USER_ID

        mock_uuid.uuid4.return_value = MOCK_TRACE_ID

        self.assertEqual(self._client._get_headers(), MOCK_HEADERS)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call(self):
        post(MCD_API_ENDPOINT, json=MOCK_GOOD_RESPONSE, status=200)
        self.assertEqual(
            self._client(
                query=MOCK_GET_USER_QUERY,
                retry_backoff=self._backoff,
                timeout_in_seconds=MOCK_TIMEOUT,
            ),
            Box(MOCK_GOOD_RESPONSE, camel_killer_box=True).data,
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 1)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_object(self):
        post(MCD_API_ENDPOINT, json=MOCK_GOOD_RESPONSE, status=200)

        query = Query()
        query.get_user.__fields__("email")

        response = self._client(
            query=query, retry_backoff=self._backoff, timeout_in_seconds=MOCK_TIMEOUT
        )
        self.assertEqual(response.get_user.email, MOCK_EMAIL)
        mock.assert_call_count(MCD_API_ENDPOINT, 1)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_single_gql_error(self):
        post(
            MCD_API_ENDPOINT,
            json={
                "data": None,
                "errors": [{"message": "Life is a journey. Time is a river. The door is ajar."}],
            },
            status=200,
        )

        with self.assertRaises(GqlError) as err:
            self._client(
                query=MOCK_GET_USER_QUERY,
                retry_backoff=self._backoff,
                timeout_in_seconds=MOCK_TIMEOUT,
            )
        self.assertEqual(
            "Life is a journey. Time is a river. The door is ajar.", err.exception.message
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 1)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_multiple_gql_errors(self):
        post(
            MCD_API_ENDPOINT,
            json={
                "data": None,
                "errors": [{"message": "Life is a journey."}, {"message": "Time is a river."}],
            },
            status=200,
        )

        with self.assertRaises(GqlError) as err:
            self._client(
                query=MOCK_GET_USER_QUERY,
                retry_backoff=self._backoff,
                timeout_in_seconds=MOCK_TIMEOUT,
            )
        self.assertEqual("Life is a journey.\nTime is a river.", err.exception.message)
        mock.assert_call_count(MCD_API_ENDPOINT, 1)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_user_errors(self):
        post(
            MCD_API_ENDPOINT,
            json={"message": "Invalid field value", "field": "name"},
            status=400,
            headers={"X-Custom": "blah blah"},
        )

        backoff = MockBackoff(2)
        with self.assertRaises(GqlError) as err:
            self._client(
                query=MOCK_GET_USER_QUERY, retry_backoff=backoff, timeout_in_seconds=MOCK_TIMEOUT
            )
        self.assertEqual(
            {"Content-Type": "application/json", "X-Custom": "blah blah"},
            err.exception.headers,
        )
        self.assertEqual(
            400,
            err.exception.status_code,
        )
        self.assertEqual(
            "Invalid field value",
            err.exception.message,
        )
        self.assertEqual(
            '{"message": "Invalid field value", "field": "name"}',
            err.exception.body,
        )
        self.assertEqual(
            f"400 Client Error: Bad Request for url: {MCD_API_ENDPOINT}",
            str(err.exception),
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 1)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_network_errors_no_retries(self):
        post(MCD_API_ENDPOINT, body="Oops", status=503)

        with self.assertRaises(GqlError) as err:
            self._client(
                query=MOCK_GET_USER_QUERY,
                retry_backoff=self._backoff,
                timeout_in_seconds=MOCK_TIMEOUT,
            )
        self.assertEqual(
            {"Content-Type": "text/plain"},
            err.exception.headers,
        )
        self.assertEqual(
            503,
            err.exception.status_code,
        )
        self.assertEqual(
            "Oops",
            err.exception.message,
        )
        self.assertEqual(
            "Oops",
            err.exception.body,
        )
        self.assertEqual(
            f"503 Server Error: Service Unavailable for url: {MCD_API_ENDPOINT}",
            str(err.exception),
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 1)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_network_errors_retried_with_success(self):
        post(MCD_API_ENDPOINT, body="Oops", status=503)
        post(MCD_API_ENDPOINT, body="Oops", status=503)
        post(MCD_API_ENDPOINT, json=MOCK_GOOD_RESPONSE, status=200)

        backoff = MockBackoff(2)
        response = self._client(
            query=MOCK_GET_USER_QUERY, retry_backoff=backoff, timeout_in_seconds=MOCK_TIMEOUT
        )
        self.assertEqual(
            MOCK_EMAIL,
            response.get_user.email,  # type: ignore
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 3)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_network_errors_retried_to_exhaustion(self):
        post(MCD_API_ENDPOINT, body="Oops", status=503)
        post(MCD_API_ENDPOINT, body="Oops", status=503)
        post(MCD_API_ENDPOINT, body="Oops", status=503)
        post(MCD_API_ENDPOINT, body="Oops", status=503)
        post(MCD_API_ENDPOINT, body="Oops", status=503)
        post(MCD_API_ENDPOINT, body="Oops", status=503)

        backoff = MockBackoff(4)
        with self.assertRaises(GqlError) as err:
            self._client(
                query=MOCK_GET_USER_QUERY, retry_backoff=backoff, timeout_in_seconds=MOCK_TIMEOUT
            )
        self.assertEqual(
            {"Content-Type": "text/plain"},
            err.exception.headers,
        )
        self.assertEqual(
            503,
            err.exception.status_code,
        )
        self.assertEqual(
            "Oops",
            err.exception.message,
        )
        self.assertEqual(
            "Oops",
            err.exception.body,
        )
        self.assertEqual(
            f"503 Server Error: Service Unavailable for url: {MCD_API_ENDPOINT}",
            str(err.exception),
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 5)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_timeout_retried_with_success(self):
        post(MCD_API_ENDPOINT, body=Timeout())
        post(MCD_API_ENDPOINT, body=Timeout())
        post(MCD_API_ENDPOINT, json=MOCK_GOOD_RESPONSE, status=200)

        backoff = MockBackoff(2)
        response = self._client(
            query=MOCK_GET_USER_QUERY, retry_backoff=backoff, timeout_in_seconds=MOCK_TIMEOUT
        )
        self.assertEqual(
            MOCK_EMAIL,
            response.get_user.email,  # type: ignore
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 3)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_400_errors_not_retried(self):
        def should_retry(exc: Exception) -> bool:
            if isinstance(exc, HTTPError):
                return exc.response.status_code != 400  # type: ignore

            return False

        self._session.scope = _AIRFLOW_SCOPE
        post(
            MCD_API_ENDPOINT,
            json={"errors": [{"message": "Request timed out", "code": "REQUEST_TIMEOUT"}]},
            status=400,
            headers={"X-Custom": "blah blah"},
        )

        backoff = MockBackoff(2)

        with self.assertRaises(HTTPError) as err:
            self._client.make_request(
                path=MCD_API_ENDPOINT, body={}, should_retry=should_retry, retry_backoff=backoff
            )

        self.assertEqual(400, err.exception.response.status_code)  # type: ignore
        mock.assert_call_count(MCD_API_ENDPOINT, 1)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_400_errors_retried(self):
        def should_retry(exc: Exception) -> bool:
            if isinstance(exc, HTTPError):
                return exc.response.status_code == 400  # type: ignore

            return False

        self._session.scope = _AIRFLOW_SCOPE
        post(
            MCD_API_ENDPOINT,
            json={"errors": [{"message": "Request timed out", "code": "REQUEST_TIMEOUT"}]},
            status=400,
            headers={"X-Custom": "blah blah"},
        )
        post(
            MCD_API_ENDPOINT,
            json={"errors": [{"message": "Request timed out", "code": "REQUEST_TIMEOUT"}]},
            status=400,
            headers={"X-Custom": "blah blah"},
        )
        post(
            MCD_API_ENDPOINT,
            json={"errors": [{"message": "Request timed out", "code": "REQUEST_TIMEOUT"}]},
            status=400,
            headers={"X-Custom": "blah blah"},
        )

        backoff = MockBackoff(2)

        with self.assertRaises(HTTPError) as err:
            self._client.make_request(
                path=MCD_API_ENDPOINT, body={}, should_retry=should_retry, retry_backoff=backoff
            )

        self.assertEqual(400, err.exception.response.status_code)  # type: ignore
        mock.assert_call_count(MCD_API_ENDPOINT, 3)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_graphql_server_timeout_retried_to_exhaustion(self):
        post(
            MCD_API_ENDPOINT,
            json={"errors": [{"message": "Request timed out", "code": "REQUEST_TIMEOUT"}]},
            status=200,
            headers={"X-Custom": "blah blah"},
        )
        post(
            MCD_API_ENDPOINT,
            json={"errors": [{"message": "Request timed out", "code": "REQUEST_TIMEOUT"}]},
            status=200,
            headers={"X-Custom": "blah blah"},
        )

        backoff = MockBackoff(1)
        with self.assertRaises(GqlError) as err:
            self._client(
                query=MOCK_GET_USER_QUERY, retry_backoff=backoff, timeout_in_seconds=MOCK_TIMEOUT
            )
        self.assertEqual(
            {},
            err.exception.headers,
        )
        self.assertEqual(
            200,
            err.exception.status_code,
        )
        self.assertEqual(
            "Request timed out",
            err.exception.message,
        )
        self.assertEqual(
            [{"code": "REQUEST_TIMEOUT", "message": "Request timed out"}],
            err.exception.body,
        )
        self.assertEqual(
            "Request timed out",
            str(err.exception),
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 2)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_graphql_server_timeout_retried_with_succes(self):
        post(
            MCD_API_ENDPOINT,
            json={"errors": [{"message": "Request timed out", "code": "REQUEST_TIMEOUT"}]},
            status=200,
            headers={"X-Custom": "blah blah"},
        )
        post(MCD_API_ENDPOINT, json=MOCK_GOOD_RESPONSE, status=200)

        backoff = MockBackoff(2)
        response = self._client(
            query=MOCK_GET_USER_QUERY, retry_backoff=backoff, timeout_in_seconds=MOCK_TIMEOUT
        )
        self.assertEqual(
            MOCK_EMAIL,
            response.get_user.email,  # type: ignore
        )
        mock.assert_call_count(MCD_API_ENDPOINT, 2)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_call_with_timeout_retried_to_exhaustion(self):
        post(MCD_API_ENDPOINT, body=Timeout())
        post(MCD_API_ENDPOINT, body=Timeout())
        post(MCD_API_ENDPOINT, body=Timeout())
        post(MCD_API_ENDPOINT, body=Timeout())
        post(MCD_API_ENDPOINT, body=Timeout())
        post(MCD_API_ENDPOINT, body=Timeout())

        backoff = MockBackoff(4)
        with self.assertRaises(expected_exception=(GqlError, Timeout)) as err:
            self._client(
                query=MOCK_GET_USER_QUERY, retry_backoff=backoff, timeout_in_seconds=MOCK_TIMEOUT
            )
        self.assertIsInstance(err.exception, Timeout)
        mock.assert_call_count(MCD_API_ENDPOINT, 5)

    def test_call_failed_with_scope(self):
        self._session.scope = _AIRFLOW_SCOPE

        with self.assertRaises(InvalidSessionError):
            self._client(
                query=MOCK_GET_USER_QUERY,
                retry_backoff=self._backoff,
                timeout_in_seconds=MOCK_TIMEOUT,
            )

    def test_rest_call_failed_without_scope(self):
        with self.assertRaises(InvalidSessionError):
            self._client.make_request(_AIRFLOW_CALLBACKS_PATH, body={})

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_rest_call_airflow(self):
        self._session.scope = _AIRFLOW_SCOPE
        self._session.endpoint = MCD_IGW_ENDPOINT
        expected_response = {
            "ok": True,
        }
        url = urljoin(MCD_IGW_ENDPOINT, _AIRFLOW_CALLBACKS_PATH)
        post(url, json=expected_response, status=200)
        response = self._client.make_request(_AIRFLOW_CALLBACKS_PATH)
        self.assertEqual(expected_response, response)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_rest_call_airflow_timeout_retry(self):
        self._session.scope = _AIRFLOW_SCOPE
        self._session.endpoint = MCD_IGW_ENDPOINT
        expected_response = {
            "ok": True,
        }
        url = urljoin(MCD_IGW_ENDPOINT, _AIRFLOW_CALLBACKS_PATH)
        post(url, body=Timeout())
        post(url, body=Timeout())
        post(url, json=expected_response, status=200)
        response = self._client.make_request(
            _AIRFLOW_CALLBACKS_PATH,
            retry_backoff=MockBackoff(2),
        )
        self.assertEqual(expected_response, response)

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_rest_call_airflow_timeout_retries_exceeded(self):
        self._session.scope = _AIRFLOW_SCOPE
        self._session.endpoint = MCD_IGW_ENDPOINT

        url = urljoin(MCD_IGW_ENDPOINT, _AIRFLOW_CALLBACKS_PATH)
        post(url, body=Timeout("1"))
        post(url, body=Timeout("2"))
        post(url, body=Timeout("3"))
        with self.assertRaises(Timeout) as exc:
            self._client.make_request(
                _AIRFLOW_CALLBACKS_PATH,
                retry_backoff=MockBackoff(2),
            )
        self.assertEqual("3", str(exc.exception))

    @patch.object(Client, "_get_headers", lambda *args: MOCK_HEADERS)
    @activate(registry=registries.OrderedRegistry)
    def test_rest_call_airflow_with_session(self):
        # test that we're setting the endpoint properly when initializing
        # the session object using a scope
        session = Session(mcd_id="id", mcd_token="token", scope=_AIRFLOW_SCOPE)
        client = Client(session=session)
        expected_response = {
            "ok": True,
        }
        url = urljoin(MCD_IGW_ENDPOINT, _AIRFLOW_CALLBACKS_PATH)
        post(url, json=expected_response, status=200)
        response = client.make_request(_AIRFLOW_CALLBACKS_PATH)
        self.assertEqual(expected_response, response)
