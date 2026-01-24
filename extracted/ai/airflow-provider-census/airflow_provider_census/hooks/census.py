import requests
from typing import Dict

from airflow.exceptions import AirflowException
from airflow.providers.http.hooks.http import HttpHook

class CensusHook(HttpHook):
    """Census API hook

    :param census_conn_id: `Conn ID` of the Connection to be used to configure this hook.
    :type census_conn_id: str
    """

    conn_name_attr = 'census_conn_id'
    default_conn_name = 'census_default'
    conn_type = 'census'
    hook_name = 'Census'

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        return {
            'hidden_fields': ['login', 'port', 'schema', 'extra', 'host'],
            'relabeling': {
                'password': 'Census Secret Token'
            }
        }

    def __init__(self, census_conn_id: str = default_conn_name, *args, **kwargs) -> None:
        super().__init__(http_conn_id = census_conn_id, *args, **kwargs)
        self.census_conn_id = census_conn_id

    def _get_secret_token(self) -> str:
        conn = self.get_connection(self.http_conn_id)
        secret_token = conn.password
        if not secret_token:
            raise AirflowException('Census Secret Token is required for this hook.')
        return secret_token

    def get_conn(self, headers, extra_options=None) -> requests.Session:
        secret_token = self._get_secret_token()

        auth_header = {
            'Authorization': 'Bearer {secret_token}'.format(secret_token = secret_token)
        }

        all_headers = {**auth_header, **headers} if headers else auth_header

        session = super().get_conn(all_headers, extra_options)

        conn = self.get_connection(self.census_conn_id)
        if not conn.host:
            self.base_url = 'https://app.getcensus.com'

        return session

    def trigger_sync(self, sync_id):
        endpoint = 'api/v1/syncs/{sync_id}/trigger'.format(sync_id = sync_id)

        self.method = 'POST'
        response = self.run(endpoint)
        response.raise_for_status()

        return response.json()['data']['sync_run_id']

    def get_sync_run_info(self, sync_run_id):
        endpoint = 'api/v1/sync_runs/{sync_run_id}'.format(sync_run_id = sync_run_id)

        self.method = 'GET'
        response = self.run(endpoint)
        response.raise_for_status()

        return response.json()['data']
