import requests
import warnings
from retry import retry

from requests.exceptions import HTTPError


class UserService:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}/"

    @retry(tries=5, delay=1, jitter=1)
    def refresh_user_permissions(self):
        """
        Refreshes user permissions in Power BI.
        This api call is limited to one request per user per hour.
        """

        url = self.base_url + "RefreshUserPermissions"

        headers = self.client.auth_header
        response = requests.post(url, headers=headers)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:
                warning_message = "Failed to refresh user permissions: number of requests above limit."
                warnings.warn(warning_message, category=UserWarning)
            else:
                raise HTTPError(
                    response, "Failed when trying to refresh user permissions."
                )
