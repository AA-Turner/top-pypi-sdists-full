"""Microsoft Dynamics 365 interface."""

import urllib3
from requests import Session
from requests_ntlm import HttpNtlmAuth
from urllib.parse import urljoin

urllib3.disable_warnings()


class DynamicsAPI(Session):
    """Request session with NLTM auth for Dynamics API.

    Args:
        base_url (str): Base URL for the API.
        username (str): Username for the API.
        password (str): Password for the API.
        domain (str, optional): Domain for the API. Defaults to "dom01".
        verify_cert (bool, optional): Verify certificate. Defaults to True.

    Methods:
        request: Request method to make the API call. Will use the base URL and append the URL to it.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        domain: str = "dom01",
        verify_cert: bool = True,
    ):
        super().__init__()
        self.auth = HttpNtlmAuth(f"{domain}\\{username}", password)
        self.base_url = base_url
        self.verify_cert = verify_cert

    def request(self, method: str, url: str, *args, **kwargs):
        joined_url = urljoin(self.base_url, url)
        return super().request(method, joined_url, *args, verify=self.verify_cert, **kwargs)
