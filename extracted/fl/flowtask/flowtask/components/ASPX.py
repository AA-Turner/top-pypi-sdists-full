from abc import abstractmethod
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import httpx
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import ComponentError


class ASPX(FlowComponent, HTTPService):
    """
    ASPX

    Overview

        The ASPX class is designed for interacting with ASPX-based web applications, particularly those requiring authentication.
        It inherits from the DtComponent and HTTPService classes, providing a structured way to manage sessions, handle state views,
        and perform HTTP requests with ASPX web forms. This class is useful for automating interactions with ASPX web pages, including login
        and data retrieval operations.

    :widths: auto

        | _credentials            |   Yes    | A dictionary containing username and password for authentication.                                  |
        | _views                  |   No     | A dictionary storing state views extracted from ASPX pages.                                        |
        | _client                 |   Yes    | An instance of `httpx.AsyncClient` used for making asynchronous HTTP requests.                     |

    Return

        The methods in this class facilitate the interaction with ASPX-based web applications, including login handling,
        session management, and state view management. The class also allows for abstract extension, enabling customization
        for specific ASPX web forms and interactions.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ASPX:
          # attributes here
        ```
    """
    _version = "1.0.0"
    _credentials: dict = {"username": str, "password": str}

    def _set_views(self, soup: BeautifulSoup):
        """Extract state VIEWS from hidden inputs inside html

        Args:
            soup (BeautifulSoup): soup object with the html tree

        Returns:
            dict[str, str]: state VIEWS
        """
        viewstate = soup.find(id="__VIEWSTATE")["value"]
        soup_eventvalidation = soup.find(id="__EVENTVALIDATION")
        eventvalidation = soup_eventvalidation["value"] if soup_eventvalidation else ""
        viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")["value"]

        self._views = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstategenerator,
            "__EVENTVALIDATION": eventvalidation,
        }

    def check_keys_exists(self, *args, **kwargs):
        """Validate that specified keys are present in the kwargs dict"""
        for _key in args:
            if _key not in kwargs:
                raise ComponentError(f"{_key} must be set!")

    def _get_payload_with_views(self, **kwargs):
        payload = {
            **self._views,
            **kwargs,
        }

        return payload

    async def start(self, **kwargs):
        # handle login and set initial views
        self._proxies = False
        self._user = None
        self.auth_type = None
        self.auth = ""
        self.download = None
        self.headers = None
        self._views: dict = {}
        self.timeout = 120.0
        self._client = httpx.AsyncClient(timeout=self.timeout)

        self.processing_credentials()

        login_url = urljoin(self.base_url, "/Login.aspx")

        self.accept = "text/html"
        await self.aspx_session(login_url)

        payload = {
            **self._views,
            self.login_user_payload_key: self.credentials["username"],
            self.login_password_payload_key: self.credentials["password"],
            self.login_button_payload_key: self.login_button_payload_value,
        }

        await self.aspx_session(
            login_url, method="post", data=payload, follow_redirects=True
        )

        if ".ASPXAUTH" not in self._client.cookies:
            raise ComponentError("Login Failed. Please, check credentials!")
        self._logger.info("Login successful")

        return True

    @abstractmethod
    async def run(self):
        """
        Extend this method: Call super() after your code to make sure
        the client session is closed.
        """
        if hasattr(self, "_client"):
            await self._client.aclose()

    async def close(self):
        pass

    async def aspx_session(
        self,
        url: str,
        method: str = "get",
        data: dict = None,
        **kwargs: dict,
    ):
        result, error = await self.session(
            url,
            method=method,
            data=data,
            **kwargs,
        )

        if error:
            raise ComponentError(error)

        if "text/html" in self.accept:
            self._set_views(result)

        return result
