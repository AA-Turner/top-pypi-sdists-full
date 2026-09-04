import asyncio
import json
from pathlib import Path, PurePath
from typing import Any, Union, List, Dict, Callable
from abc import ABC
from google.oauth2 import service_account
from googleapiclient.discovery import build
from navconfig import BASE_DIR
from ..exceptions import ComponentError, ConfigError
from ..conf import GOOGLE_CREDENTIALS_FILE


# Define the scope
default_scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]


class GoogleClient(ABC):
    """
    Google Client Client.

    Managing Authentication and resources from Google Apps.

    """
    def __init__(self, *args, credentials: Union[str, dict] = None, **kwargs):
        self.credentials_file: PurePath = None
        self.credentials_str: str = None
        self.credentials_dict: dict = None
        self.scopes: list = kwargs.pop('scopes', default_scopes)
        if credentials is None:
            if not GOOGLE_CREDENTIALS_FILE.exists():
                raise ComponentError(
                    "Google: No credentials provided."
                )
            self.credentials_file = GOOGLE_CREDENTIALS_FILE
        if isinstance(credentials, str):
            # end with JSON, then are a credentials file:
            if credentials.endswith(".json"):
                self.credentials_file = Path(credentials).resolve()
                if not self.credentials_file.exists():
                    # Check if File is on BASE PATH env.
                    self.credentials_file = BASE_DIR.joinpath(credentials).resolve()
                    if not self.credentials_file.exists():
                        raise ConfigError(
                            f"Google: Credentials file not found: {self.credentials_file}"
                        )
            else:
                # Assume is a JSON string
                self.credentials_str = credentials
        elif isinstance(credentials, PurePath):
            self.credentials_file = Path(credentials).resolve()
            if not self.credentials_file.exists():
                raise ConfigError(
                    f"Google: No credentials file on {self.credentials_file}"
                )
        elif isinstance(credentials, dict):
            self.credentials_dict = credentials

        super().__init__(*args, **kwargs)

    def connection(self):
        if self.credentials_file:
            self.credentials = service_account.Credentials.from_service_account_file(
                str(self.credentials_file),
                scopes=self.scopes,
            )
        elif self.credentials_dict:
            self.credentials = service_account.Credentials.from_service_account_info(
                self.credentials_dict,
                scopes=self.scopes
            )
        elif self.credentials_str:
            self.credentials = service_account.Credentials.from_service_account_info(
                json.loads(self.credentials_str),
                scopes=self.scopes
            )
        else:
            self.credentials = service_account.Credentials.from_service_account_file(
                str(GOOGLE_CREDENTIALS_FILE),
                scopes=self.scopes
            )
        return self

    def get_service(self, service: str, version: str = 'v3'):
        """
        Get a cached Google API service instance or create one if not cached.

        Args:
            service (str): Name of the Google service (e.g., 'drive', 'sheets').
            version (str): Version of the API (default: 'v3').

        Returns:
            googleapiclient.discovery.Resource: The requested Google API service client.
        """
        if not self.credentials:
            self.connection()
        if (srv := getattr(self, f"_{service}", None)):
            return srv
        srv = build(service, version, credentials=self.credentials)
        setattr(self, f"_{service}", srv)
        return srv

    def get_drive_client(self):
        """Shortcut for accessing the Google Drive client."""
        return self.get_service("drive", "v3")

    def get_sheets_client(self):
        """Shortcut for accessing the Google Sheets client."""
        return self.get_service("sheets", "v4")

    async def execute_request(self, request_factory: Callable[[], Any]) -> Any:
        """Build and execute a googleapiclient request fully off the event loop.

        Args:
            request_factory: A zero-arg callable that both builds the
                request object and calls ``.execute()`` on it. The whole
                callable runs inside ``asyncio.to_thread`` so neither the
                request construction nor the blocking ``.execute()`` call
                ever runs on the event loop thread.

        Returns:
            Whatever ``request_factory()`` returns (typically the parsed
            JSON response from ``.execute()``).
        """
        return await asyncio.to_thread(request_factory)

    def close(self):
        """Clears cached credentials and services."""
        self.credentials = None
        self._services_cache.clear()

    def get_search(self, query: str, version: str = 'v1', cse_id: str = None, **kwargs):
        """
        Get a cached Google API service instance or create one if not cached.

        Args:

            query (str): The search query.
            version (str): Version of the API (default: 'v1').
            cse_id (str): The Custom Search Engine ID.
            **kwargs: Additional arguments for the API request.

        Returns:
            googleapiclient.discovery.Resource: The requested Google API service client.
        """
        if not self.credentials:
            self.connection()
        srv = build("customsearch", version, credentials=self.credentials)
        return srv.cse().list(q=query, cx=cse_id, **kwargs)
