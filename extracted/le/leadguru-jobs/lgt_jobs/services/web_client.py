import requests
from lgt_jobs.env import v3_server_host, v1_server_host, service_account_email, service_account_password


class BaseHttpClient:
    api_version: str = None
    token: str = None

    def _create_default_headers(self):
        return {'Authorization': f"Bearer {self.token}"}


class V3ServerClient(BaseHttpClient):
    api_version = 'api/v3'

    def __init__(self):
        self.token = BillingServerClient.login(service_account_email, service_account_password)

    def update_user_lead(self, message_id: str, email: str, slack_channel: str,
                         board_id: str = None, status: str = None, followup_date=None) -> dict:
        payload = {
            'message_id': message_id,
            'user_email': email
        }

        update_lead_payload = {
            'slack_channel': slack_channel,
            'board_id': board_id,
            'status': status,
            'followup_date': followup_date
        }
        headers = self._create_default_headers()
        return requests.post(f'{v3_server_host}/{self.api_version}/user_leads/update',
                             headers=headers, params=payload, json=update_lead_payload).json()


class BillingServerClient:
    api_version = 'api'

    @staticmethod
    def login(email: str, password: str) -> str:
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(f'{v1_server_host}/{BillingServerClient.api_version}/login', json=payload).json()
        return response['access_token']
