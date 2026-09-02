"""
API client for the nanodjango playground.

This module is click-free and can be used independently.
"""

import json
import os
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

DEFAULT_SERVER = "https://nanodjango.dev/api"
_CREDS_DIR = Path.home() / ".config" / "nanodjango"
_CREDS_FILE = _CREDS_DIR / "credentials.json"


class ApiError(Exception):
    """
    HTTP or network errors
    """


class ApiAuthError(ApiError):
    """
    Authentication is missing or rejected
    """


class Api:
    """
    Client for the nanodjango playground REST API
    """

    def __init__(self, server: str | None = None) -> None:
        server_url = server or os.environ.get("NANODJANGO_API_URL") or DEFAULT_SERVER
        parsed = urllib.parse.urlparse(server_url)
        self.host = f"{parsed.scheme}://{parsed.netloc}"
        self.server = self.host + parsed.path.rstrip("/") + "/"
        if os.environ.get("NANODJANGO_API_URL"):
            import ssl

            self._ssl_context = ssl._create_unverified_context()
        else:
            self._ssl_context = None

    def _load_credentials(self) -> dict | None:
        if not _CREDS_FILE.exists():
            return None
        try:
            return json.loads(_CREDS_FILE.read_text())
        except Exception:
            return None

    def _save_credentials(self, api_key: str, username: str) -> None:
        _CREDS_DIR.mkdir(parents=True, exist_ok=True)
        _CREDS_FILE.write_text(json.dumps({"api_key": api_key, "username": username}))
        _CREDS_FILE.chmod(0o600)

    def _clear_credentials(self) -> None:
        if _CREDS_FILE.exists():
            _CREDS_FILE.unlink()

    @property
    def is_authenticated(self) -> bool:
        """Return True if credentials are stored."""
        return bool(self.token)

    @property
    def token(self) -> str | None:
        """Return the current API token, or None if not logged in."""
        creds = self._load_credentials()
        return creds.get("api_key") if creds else None

    @property
    def username(self) -> str:
        """Return the authenticated username. Raises ApiAuthError if not logged in."""
        creds = self._load_credentials()
        if not creds or not creds.get("username"):
            raise ApiAuthError("Not authenticated. Please log in.")
        return creds["username"]

    def login(self) -> None:
        """
        Ensure authenticated. Returns immediately if already logged in.
        Otherwise runs the device-flow login and saves credentials.

        Raises ApiError on failure.
        """
        if self.is_authenticated:
            return

        try:
            resp = self._post("/auth/", {"label": socket.gethostname()})
        except ApiError as e:
            raise ApiError(f"Login failed: {e}")
        approval_url = resp.get("url")
        code = resp.get("code")
        if not approval_url or not code:
            raise ApiError("Login failed: unexpected response from auth endpoint.")

        approval_url = self.host + approval_url
        print(f"Open this URL to approve access:\n  {approval_url}")
        webbrowser.open(approval_url)

        print("Waiting for approval", end="", flush=True)
        while True:
            time.sleep(3)
            print(".", end="", flush=True)
            result = self._post("/auth/token/", {"code": code})

            status = result.get("status")
            if status == "pending":
                continue
            elif status == "denied":
                print()
                raise ApiAuthError("Access request was denied.")
            elif status == "complete":
                print()
                api_key = result.get("api_key")
                username = result.get("username")
                if not api_key or not username:
                    raise ApiError("Incomplete credentials received.")
                self._save_credentials(api_key, username)
                print(f"Logged in as {username}.")
                return
            else:
                print()
                raise ApiError(f"Unexpected auth status: {status!r}")

    def logout(self) -> None:
        """
        Revoke credentials remotely and clear local storage.

        Raises ApiAuthError if not logged in.
        """
        if not self.is_authenticated:
            raise ApiAuthError("Not authenticated. Please log in.")
        try:
            self._post("/auth/logout/")
        except ApiError:
            # ignore remote errors; clear local credentials regardless
            pass
        self._clear_credentials()

    def list(self, user: str | None = None) -> list[dict]:
        """
        List scripts for a user

        If user is None, uses the authenticated user

        Returns a list of script dicts
        """
        self.login()
        resp = self._get(f"/scripts/{user or self.username}/")
        return resp if isinstance(resp, list) else resp.get("scripts", [])

    def pull(self, name: str, user: str | None = None) -> str:
        """
        Fetch a script's code

        If user is None, uses the authenticated user

        Returns the script source code
        """
        self.login()
        resp = self._get(f"/scripts/{user or self.username}/{name}/")
        return resp.get("code", "")

    def push(
        self,
        name: str,
        code: str,
        title: str = "",
        description: str = "",
        packages: str = "",
        environment: dict | None = None,
        force: bool = False,
    ) -> str:
        """
        Upload a script under the authenticated user. Will log in if not already.

        Returns the live URL of the script. Raises ApiError on 409 if the script
        already exists and force is False.
        """
        self.login()
        resp = self._put(
            f"/scripts/{self.username}/{name}/",
            {
                "code": code,
                "title": title or name,
                "description": description,
                "packages": packages,
                "environment": json.dumps(environment or {}),
                "force": force,
            },
        )
        return resp["url"]

    def _request(self, method: str, path: str, data: dict | None = None) -> dict:
        url = self.server + path.lstrip("/")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, context=self._ssl_context) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise ApiAuthError("Authentication failed. Please log in again.")
            try:
                detail = json.loads(e.read().decode()).get("detail", e.reason)
            except Exception:
                detail = e.reason
            if e.code == 409:
                raise ApiError("Script already exists, use --force to overwrite.")
            raise ApiError(f"HTTP {e.code}: {detail}")
        except urllib.error.URLError as e:
            raise ApiError(f"Network error: {e.reason}")

    def _get(self, path: str) -> dict:
        return self._request("GET", path)

    def _post(self, path: str, data: dict | None = None) -> dict:
        return self._request("POST", path, data=data)

    def _put(self, path: str, data: dict) -> dict:
        return self._request("PUT", path, data=data)
