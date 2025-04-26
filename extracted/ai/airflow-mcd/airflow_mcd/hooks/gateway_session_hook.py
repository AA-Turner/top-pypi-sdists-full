from typing import Tuple

from pycarlo.core import Client
from requests import HTTPError

from airflow_mcd.hooks import SessionHook
from airflow_mcd.hooks.constants import MCD_GATEWAY_CONNECTION_TYPE

_INTEGRATION_GATEWAY_PATH = "/airflow/callbacks"


class GatewaySessionHook(SessionHook):
    conn_name_attr = "mcd_session_conn_id"

    default_conn_name = "mcd_gateway_default_session"

    conn_type = MCD_GATEWAY_CONNECTION_TYPE

    hook_name = "Monte Carlo Data Gateway"

    def test_connection(self) -> Tuple[bool, str]:
        """
        Test MCD Gateway connection.

        :return: tuple of boolean and string for whether the test was successful and a related message
        """
        try:
            mc_client = Client(self.get_conn())
            body = {
                "airflow_operation": "ping",
                "airflow_payload": {},
            }
            json_response = mc_client.make_request(path=_INTEGRATION_GATEWAY_PATH, body=body)
            success = json_response.get("success", False)
            resource_ids = json_response.get("resource_ids", [])

            if not success:
                return False, f"Failed to test MCD connection, returned success=false"

            suffix = f" Using Airflow connection in MCD with UUID={resource_ids[0]}" if resource_ids else ""
            return True, f"Connection to MCD Gateway successfully tested.{suffix}"
        except HTTPError as exc:
            if exc.response.status_code == 401:
                return False, (
                    "Authentication failed, please check you created an Airflow Integration Key following "
                    "the docs at https://docs.getmontecarlo.com/docs/airflow-incidents-dags-and-tasks"
                )
            return False, f"Connection to MCD Gateway failed: {exc}"
        except Exception as exc:
            return False, f"Connection to MCD Gateway failed: {exc}"
