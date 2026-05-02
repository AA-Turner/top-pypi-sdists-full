import os
import webbrowser
from socketserver import TCPServer
from threading import Thread
from time import time
from typing import List, Optional
from urllib.parse import urlparse, urlencode

from spotipyio.logic.consts.api_consts import ACCESS_CODE_REQUEST_URL, REDIRECT_URI, CLIENT_ID, SCOPE, RESPONSE_TYPE
from spotipyio.logic.consts.env_consts import SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
from spotipyio.tools.auth.redirect_uri_request_handler import RedirectURIRequestHandler


class AccessCodeFetcher:
    def __init__(self, timeout: int = 60):
        self._timeout = timeout

    def fetch(self, scopes: List[str], client_id: Optional[str] = None, redirect_uri: Optional[str] = None) -> str:
        if redirect_uri is None:
            redirect_uri = os.environ[SPOTIPY_REDIRECT_URI]

        if client_id is None:
            client_id = os.environ[SPOTIPY_CLIENT_ID]

        try:
            return self._fetch_access_code(scopes=scopes, client_id=client_id, redirect_uri=redirect_uri)

        finally:
            RedirectURIRequestHandler.access_code = None

    def _fetch_access_code(self, scopes: List[str], client_id: str, redirect_uri: str) -> str:
        port = self._extract_redirect_uri_port(redirect_uri)
        server_thread = Thread(target=self._start_server, args=(port,), daemon=True)
        server_thread.start()
        url = self._build_authorization_url(scopes=scopes, client_id=client_id, redirect_uri=redirect_uri)
        webbrowser.open(url)

        return self._extract_access_code()

    @staticmethod
    def _extract_redirect_uri_port(redirect_uri: str) -> int:
        parsed_url = urlparse(redirect_uri)
        if parsed_url.hostname != "localhost":
            raise ValueError(
                "Invalid redirect URI! redirect_uri must be a localhost string in the following format: `http://localhost:<some-port>`"
            )

        return parsed_url.port

    @staticmethod
    def _start_server(port: int) -> None:
        with TCPServer(("", port), RedirectURIRequestHandler) as httpd:
            httpd.serve_forever()

    @staticmethod
    def _build_authorization_url(scopes: List[str], client_id: str, redirect_uri: str) -> str:
        params = {
            CLIENT_ID: client_id,
            RESPONSE_TYPE: "code",
            REDIRECT_URI: redirect_uri,
            SCOPE: " ".join(scopes),
        }
        encoded_params = urlencode(params)

        return f"{ACCESS_CODE_REQUEST_URL}?{encoded_params}"

    def _extract_access_code(self) -> str:
        start_time = time()

        while RedirectURIRequestHandler.access_code is None:
            if time() - start_time > self._timeout:
                raise TimeoutError("Access code fetching timed out!")

        return RedirectURIRequestHandler.access_code
