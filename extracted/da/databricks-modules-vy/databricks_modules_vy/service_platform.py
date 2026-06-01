from dataclasses import dataclass
import requests


@dataclass
class TokenConfig:
    """A simple dataclass to hold the configuration for the Service Platform API.

    Attributes:
        client_id (str): The client ID for the Service Platform API.
        client_secret (str): The client secret for the Service Platform API.
        access_token_url (str): The URL for the access token endpoint.
            i.e. "https://auth.cognito.vydev.io/oauth2/token"
        scopes (str): The scopes you wish to authenticate with.
    """

    client_id: str
    client_secret: str
    access_token_url: str
    scopes: str


class ServicePlatformApi:
    """Class to interact with the Service Platform API.

    This class provides methods to handle authentication and make HTTP GET and POST requests
    to the Service Platform API. It uses OAuth2 client credentials flow to obtain access tokens.

    Attributes:
        api_url (str): The base URL for the Service Platform API.
        token_config (TokenConfig): The configuration details for token generation.
    """

    def __init__(self, api_url: str, token_config: TokenConfig):
        """Initialize the ServicePlatformApi class.

        Args:
            api_url (str): The base URL for the Service Platform API.
            token_config (TokenConfig): An instance of TokenConfig containing authentication details.

        Raises:
            Exception: If the token generation fails.
        """
        self._api_url = api_url
        self._token_config = token_config
        self._access_token = self._get_access_token()

    def _get_access_token(self) -> str:
        token_response = requests.post(
            self._token_config.access_token_url,
            data={"grant_type": "client_credentials", "scope": " ".join(self._token_config.scopes)},
            auth=(self._token_config.client_id, self._token_config.client_secret),
        )
        try:
            token_response.raise_for_status()
        except Exception as e:
            print(e)
            print(token_response.text)
            raise e
        return token_response.json()["access_token"]

    def post(
        self, path: str, json: dict = None, headers: dict = None, timeout: int = 30
    ) -> requests.Response:
        """Send a POST request to the API.

        Args:
            path (str): The endpoint path (relative to the base URL).
            json (dict, optional): The JSON payload to include in the request. Defaults to None.
            headers (dict, optional): Additional headers to include in the request. Defaults to None.
            timeout (int, optional): The request timeout in seconds. Defaults to 30.

        Returns:
            requests.Response: The response object from the API.

        Raises:
            requests.exceptions.HTTPError: If the API returns an error response.
        """
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Bearer {self._access_token}"
        headers["Connection"] = "close"

        api_response: requests.Response = requests.post(
            url=self._api_url + path, json=json, headers=headers, timeout=timeout
        )
        try:
            api_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            print(api_response.text)
            raise e

        return api_response

    def get(
        self, path: str, params: dict = None, headers: dict = None, timeout: int = 30
    ) -> requests.Response:
        """Send a GET request to the API.

        Args:
            path (str): The endpoint path (relative to the base URL).
            params (dict, optional): Query parameters to include in the request. Defaults to None.
            headers (dict, optional): Additional headers to include in the request. Defaults to None.
            timeout (int, optional): The request timeout in seconds. Defaults to 30.

        Returns:
            requests.Response: The response object from the API.

        Raises:
            requests.exceptions.HTTPError: If the API returns an error response.
        """
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Bearer {self._access_token}"
        headers["accept"] = "application/json"

        api_response: requests.Response = requests.get(
            url=self._api_url + path, params=params, headers=headers, timeout=timeout
        )
        try:
            api_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            print(api_response.text)
            raise e

        return api_response