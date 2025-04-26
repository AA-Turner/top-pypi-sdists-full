from typing import Dict, Tuple, Optional
from urllib.parse import urlparse, urlunparse

from airflow.exceptions import AirflowException
from airflow.models.connection import Connection

from pycarlo.common.retries import ExponentialBackoff
from pycarlo.core import Session, Client, Query

from airflow_mcd.hooks.constants import (
    MCD_GATEWAY_CONNECTION_TYPE,
    MCD_GATEWAY_SCOPE,
    MCD_GATEWAY_HOSTS,
)

try:
    from airflow.hooks.base import BaseHook

    HOOK_SOURCE = None
except ImportError:
    # For Airflow 1.10.*
    from airflow.hooks.base_hook import BaseHook

    HOOK_SOURCE = 'mcd_session'
from pycarlo.core import Session

_DEFAULT_TIMEOUT_SEC = 10
_DEFAULT_BACKOFF_START_SEC = 2
_DEFAULT_BACKOFF_MAX_SEC = 90
_PERMISSION_TEST_QUERY = """
query getUser {
   getUser {
     auth{
      permissions {
        permission
        effect
      }
    }
   }
 }
"""
_REQUIRED_PERMISSIONS = ["CatalogEdit", "MonitorsAccess"]


class SessionHook(BaseHook):
    API_PATH = '/graphql'

    conn_name_attr = "mcd_session_conn_id"

    default_conn_name = "mcd_default_session"

    conn_type = "mcd"

    hook_name = "Monte Carlo Data"

    def __init__(self, mcd_session_conn_id: str):
        """
        MCD Session Hook. Retrieves connection details from the Airflow `Connection` object.

        The `mcd_id` can be configured via the connection "login", and the `mcd_token` via the connection "password".

        Alternatively, either `mcd_id` or `mcd_token` can be configured in the connection "extra", with values passed
        via "login" or "password" taking precedence.
        {
            "mcd_id": "foo",
            "mcd_token": "bar"
        }

        :param mcd_session_conn_id: Connection ID for the MCD session.
        """
        self.mcd_session_conn_id = mcd_session_conn_id

        super().__init__(**(dict(source=HOOK_SOURCE) if HOOK_SOURCE is not None else {}))

    def get_conn(self) -> Session:
        """
        Gets a connection for the hook.

        :return: MCD access session.
        """
        connection = self.get_connection(self.mcd_session_conn_id)
        connection_extra = connection.extra_dejson
        try:
            return Session(
                mcd_id=connection.login or connection_extra['mcd_id'],
                mcd_token=connection.password or connection_extra['mcd_token'],
                **self._get_session_extra(connection)
            )
        except KeyError as err:
            raise AirflowException(f'Missing expected key {err} from connection extra.')

    def _get_session_extra(self, connection: Connection) -> Dict:
        """
        Extract extra MCD session parameters from an Airflow connection.

        :param connection: Airflow connection
        :return: dictionary of kwargs for MCD Session
        """
        extras = {}
        if connection.host:
            extras['endpoint'] = self._get_api_endpoint(connection.host)
        if self._is_gateway_connection(connection.conn_type, connection.host):
            extras["scope"] = MCD_GATEWAY_SCOPE
        return extras

    @staticmethod
    def _is_gateway_connection(connection_type: str, host: Optional[str]) -> bool:
        if connection_type == MCD_GATEWAY_CONNECTION_TYPE:
            return True
        else:
            # in some environments our custom connection types (like "Monte Carlo Data Gateway") are not
            # showing up, as a workaround we're supporting HTTP connections with the endpoint being the
            # integration gateway
            return urlparse(host).netloc in MCD_GATEWAY_HOSTS

    def _get_api_endpoint(self, host: str) -> str:
        """
        Get MCD API endpoint from Airflow connection host.

        :param host: Airflow connection host
        :return: MCD API endpoint url
        """
        parsed = urlparse(host)
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path or self.API_PATH,  # set root API path if not provided in connection host
            parsed.params,
            parsed.query,
            parsed.fragment
        ))

    def test_connection(self) -> Tuple[bool, str]:
        """
        Test MCD API connection.

        :return: tuple of boolean and string for whether the test was successful and a related message
        """
        try:
            mc_client = Client(self.get_conn())
            result = mc_client(
                query=_PERMISSION_TEST_QUERY,
                retry_backoff=ExponentialBackoff(_DEFAULT_BACKOFF_START_SEC, _DEFAULT_BACKOFF_MAX_SEC),
                timeout_in_seconds=_DEFAULT_TIMEOUT_SEC,
            )
            if "error" in result:
                return False, f"Failed to test MC connection: getUser query failed: {result.error.errors[0].message}"

            if not all(any(p.permission == required_permission and p.effect.lower() == "allow" for p in result.get_user.auth.permissions) for required_permission in _REQUIRED_PERMISSIONS):
                return False, f'Failed to test MC connection: Missing one of the required permissions: {_REQUIRED_PERMISSIONS}'

            return True, 'Connection successfully tested'
        except Exception as exc:
            return False, f'Failed to test MC connection: {exc}'
