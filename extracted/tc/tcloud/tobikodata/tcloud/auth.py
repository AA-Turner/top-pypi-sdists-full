from __future__ import annotations

import base64
import json
import math
import os
import shutil
import stat
import threading
import time
import typing as t
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from queue import Queue
from urllib.parse import parse_qs, urlparse

import httpx
from authlib.common.security import generate_token
from authlib.integrations.requests_client import OAuth2Session
from httpx import Auth, Request, Response
from rich.console import Console
from rich.theme import Theme
from ruamel.yaml import YAML

from tobikodata.tcloud.jwt import parse_jwt

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
"""This is to allow the oauthlib to not error when we do the oauth flow with
http://127.0.0.1:29525 as the redirect url"""


# Yaml
yaml = YAML()

# This is duplicated from tcloud in order to avoid pulling in tcloud deps into
# http client
TCLOUD_PATH = Path(os.environ.get("TCLOUD_HOME", Path.home() / ".tcloud"))
"""The location of the tcloud config folder"""

TOBIKO_LOGO = "data:image/png;base64,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"
"""The tobiko logo to use on the SSO success/error page"""


LOCAL_OAUTH_PORT = 29525
""" The string "sql" in base 32"""

SCOPE = os.environ.get("TCLOUD_SCOPE", "tbk:scope:projects")
"""The scopes to request from the tobiko auth service"""

REDIRECT_URI = f"http://127.0.0.1:{LOCAL_OAUTH_PORT}/auth/handler"
"""The local redirect_uri value to use"""

CLIENT_ID = os.environ.get("TCLOUD_CLIENT_ID", "f695a000-bc5b-43c2-bcb7-8e0179ddff0c")
"""The OAuth client ID to use"""

CLIENT_SECRET = os.environ.get("TCLOUD_CLIENT_SECRET")
"""The OAuth client secret to use for the client credentials (service-to-service) flow"""

AUTH_URL = os.environ.get("TCLOUD_AUTH_URL", "https://cloud.tobikodata.com/auth")
"""The OAuth authorization endpoint to use"""

TOKEN_URL = os.environ.get("TCLOUD_TOKEN_URL", "https://cloud.tobikodata.com/auth/token")
"""The OAuth token endpoint to use"""

THEME = Theme(
    {
        "error": "red",
        "success": "green",
        "url": "bright_blue",
        "key": "magenta",
        "provider": "bright_magenta",
        "tobiko": "#FF5700",
    }
)
"""The Rich console theme to use in the CLI"""


class SSOHTTPServer(HTTPServer):
    def __init__(self) -> None:
        self.queue: Queue = Queue()
        super().__init__(("", LOCAL_OAUTH_PORT), SSOHTTPRequestHandler)


class SSOHTTPRequestHandler(BaseHTTPRequestHandler):
    server: SSOHTTPServer

    @staticmethod
    def _html(title: str, message: str) -> str:
        return str(f"""<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" href="https://cloud.tobikodata.com/auth/assets/favicon.svg" sizes="any" type="image/svg+xml" />
    <title>Tobkiko Cloud - Login</title>
  </head>
  <body style="text-align: center; font-family: Inter, sans-serif;">
    <img alt="Tobiko Logo" src="{TOBIKO_LOGO}"/>
    <h1>{title}</h1>
    <p>{message}</p>
    <p><em>You can close this window</em></p>
  </body>
</html>
""")

    @staticmethod
    def success_html() -> str:
        return SSOHTTPRequestHandler._html("Success", "You have logged into the SQLMesh CLI!")

    @staticmethod
    def error_html(message: str) -> str:
        return SSOHTTPRequestHandler._html("Error", message)

    def log_message(self, _: str, *args: t.Any) -> None:
        pass

    def do_GET(self) -> None:
        self.server.queue.put(self.path)

        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if "error" in query:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            message = query["error"][0]
            if query["error_description"]:
                message = message + ": " + query["error_description"][0]
            self.wfile.write(self.error_html(message).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.success_html().encode("utf-8"))


def tcloud_sso(
    auth_url: str = AUTH_URL,
    token_url: str = TOKEN_URL,
    client_id: str = CLIENT_ID,
    scope: str = SCOPE,
    auth_yaml_path: Path = TCLOUD_PATH,
    client_secret: t.Optional[str] = CLIENT_SECRET,
    code_verifier: t.Optional[str] = None,
    console: t.Optional[Console] = None,
) -> SSOAuth:
    return SSOAuth(
        auth_url=auth_url,
        token_url=token_url,
        client_id=client_id,
        scope=scope,
        auth_yaml_path=auth_yaml_path,
        client_secret=client_secret,
        code_verifier=code_verifier,
        console=console,
    )


class SSOAuth:
    """
    This class handles the OAuth flows and CLI process for getting an ID token
    to use with API calls that require it.
    """

    def __init__(
        self,
        auth_url: str,
        token_url: str,
        client_id: str,
        scope: str,
        auth_yaml_path: Path,
        client_secret: t.Optional[str] = None,
        console: t.Optional[Console] = None,
        code_verifier: t.Optional[str] = None,
    ) -> None:
        self.auth_url = auth_url
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.console = console or Console(theme=THEME)
        self.code_verifier = code_verifier or generate_token(48)

        if not auth_yaml_path.exists():
            auth_yaml_path.mkdir(parents=True, exist_ok=True)
        self._auth_yaml_path = auth_yaml_path

        self.session = OAuth2Session(
            self.client_id,
            self.client_secret,
            redirect_uri=REDIRECT_URI,
            scope=self.scope,
            code_challenge_method="S256",
        )
        self.token_info = self._load_auth_yaml()

    @property
    def _auth_yaml_file(self) -> Path:
        return self._auth_yaml_path / "auth.yaml"

    @property
    def _impersonate_yaml_file(self) -> Path:
        return self._auth_yaml_path / "impersonate.yaml"

    def _delete_auth_yamls(self) -> None:
        self._delete_auth_yaml()
        self._delete_impersonate_yaml()

    def _delete_auth_yaml(self) -> None:
        """
        Removes the auth.yaml file if it exists.
        """
        auth_file = self._auth_yaml_file
        if auth_file.exists() and os.access(auth_file, os.W_OK):
            os.remove(auth_file)

    def _delete_impersonate_yaml(self) -> None:
        impersonation_file = self._impersonate_yaml_file
        if impersonation_file.exists() and os.access(impersonation_file, os.W_OK):
            os.remove(impersonation_file)

    def _load_auth_yaml(self) -> t.Optional[t.Dict]:
        """
        Loads the full auth.yaml file that might exist in the CLI config folder.
        """
        auth_file = self._auth_yaml_file

        if auth_file.exists() and os.access(auth_file, os.R_OK):
            with auth_file.open("r") as fd:
                return yaml.load(fd.read())

        return None

    def _save_auth_yaml(self, data: t.Dict) -> None:
        """
        Saves the given dictionary to auth.yaml

        Args:
            data: The dictionary to save
        """
        auth_file = self._auth_yaml_file

        with auth_file.open("w") as fd:
            yaml.dump(data, fd)
        os.chmod(auth_file, stat.S_IWUSR | stat.S_IRUSR)

    def auth_info(self) -> t.Dict:
        token_info = self._load_auth_yaml()
        now = time.time()

        if token_info:
            if token_info.get("expires_at", 0.0) > now:
                _, body, _ = parse_jwt(token_info["id_token"])
                return {
                    "logged_in": True,
                    "expires_in": math.floor((token_info["expires_at"] - now) / 60),
                    "claims": body,
                }
            return {
                "logged_in": False,
                "expired": True,
            }

        return {"logged_in": False}

    def status(self) -> None:
        auth_info = self.auth_info()

        if not auth_info["logged_in"]:
            if auth_info.get("expired"):
                self.console.print("Current SSO session expired", style="error")
                return
            self.console.print("Not currently authenticated", style="error")
            return

        self.console.print(
            f"Current [tobiko]Tobiko Cloud[/tobiko] SSO session expires in [success]{auth_info['expires_in']}[/success] minutes"
        )
        claims = auth_info.get("claims", {})
        if claims and claims["sub"] == claims["aud"]:
            client_id = claims["sub"]
            self.console.print("[url]Service to Service Token[/url]")
            self.console.print(f"[key]Client ID:[/key] {client_id}")
        else:
            self.console.print("[url]User Token[/url]")

        if "email" in claims:
            email = claims["email"]
            self.console.print(f"[key]Email:[/key] {email}")
        if "name" in claims:
            name = claims["name"]
            self.console.print(f"[key]Name:[/key] {name}")
        if "scope" in claims:
            scope = claims["scope"]
            self.console.print(f"[key]Scope:[/key] {scope}")

    def undo_impersonation(self, status: bool = True) -> None:
        if not self._impersonate_yaml_file.exists():
            self.console.print("No current impersonation")
            return
        os.replace(self._impersonate_yaml_file, self._auth_yaml_file)
        self.token_info = self._load_auth_yaml()
        self.console.print("Removing impersonation")

        if status:
            self.status()

    def impersonate(
        self,
        scope: str,
        name: t.Optional[str] = None,
        email: t.Optional[str] = None,
    ) -> None:
        if self._impersonate_yaml_file.exists():
            self.undo_impersonation(status=False)

        id_token = self.id_token(login=True)

        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "client_id": self.client_id,
            "scope": scope,
            "subject_token": id_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:id_token",
        }
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        response = httpx.post(self.token_url, data=data)
        response.raise_for_status()

        if self._auth_yaml_file.exists():
            shutil.copy(self._auth_yaml_file, self._impersonate_yaml_file)

        self._create_token_info(response.json())
        self.status()

    def copy_token(self) -> None:
        try:
            import pyperclip

            token = self.id_token()

            pyperclip.copy(token)
            self.console.print(
                "The current token has been copied to your system clipboard :clipboard:"
            )
        except Exception:
            pass

        return None

    def id_token(self, use_device_flow: bool = False, login: bool = False) -> t.Optional[str]:
        """
        Returns the id_token needed for SSO.  Will return the one saved on disk,
        unless it's expired.  If the token on disk is expired, it will try to
        refresh it.  If there is no token on disk, it will start the SSO process
        to get a new one if login is True.
        """

        if self.token_info:
            # If we are within 5 minutes of expire time, run refresh
            if self.token_info.get("expires_at", 0.0) > (time.time() + 300):
                # We have a current token on disk, return it
                return self.token_info["id_token"]

            # Our token is expired, refresh it if possible
            try:
                refreshed_token = self.refresh_token()

                if refreshed_token:
                    return refreshed_token

                # We failed to refresh, logout
                self._delete_auth_yamls()

            except Exception:
                # We failed to refresh, logout
                self._delete_auth_yamls()

        if login:
            # We should get a new token
            return self.login(use_device_flow)

        return None

    def logout(self) -> None:
        self._delete_auth_yamls()
        self.console.print("Logged out of [tobiko]Tobiko Cloud[/tobiko]")

    def login_with_client_credentials(self) -> t.Optional[str]:
        try:
            self.session.fetch_token(
                self.token_url,
                grant_type="client_credentials",
            )
            return self._create_token_info(self.session.token)["id_token"]
        except Exception:
            raise ValueError(
                "Error logging in with client credentials. Please make sure that the TCLOUD_CLIENT_ID and TCLOUD_CLIENT_SECRET environment variables are set to the right values."
            )

    def _open_browser_flow(self, auth_url: str) -> None:
        try:
            webbrowser.open(auth_url)
            self.console.print()
            self.console.print(
                "Opening your browser to the signin URL [success]:globe_with_meridians:[/success]"
            )
        except Exception:
            pass

        self.console.print()
        self.console.print(
            "If a browser doesn't open on your system please go to the following url:"
        )
        self.console.print(f"[url]{auth_url}[/url]")

        try:
            import pyperclip

            pyperclip.copy(auth_url)
            self.console.print()
            self.console.print("This url has also been copied to your system clipboard :clipboard:")
        except Exception:
            pass

    def login(self, use_device_flow: bool) -> t.Optional[str]:
        # Can we use client credentials?
        if self.client_secret:
            return self.login_with_client_credentials()

        if use_device_flow:
            return self.login_device_flow()

        server = SSOHTTPServer()
        thread = threading.Thread(target=server.handle_request)
        thread.start()

        auth_url, _ = self.session.create_authorization_url(
            self.auth_url,
            code_verifier=self.code_verifier,
        )

        self.console.print("Logging into [tobiko]Tobiko Cloud[/tobiko]")
        self._open_browser_flow(auth_url)

        try:
            self.console.print()
            with self.console.status(
                "Waiting... You can [key]Ctrl-C[/key] to cancel this request."
            ):
                thread.join()

            self.console.print("[success]Success![/success] :white_check_mark:")
            self.console.print()

            self.session.fetch_token(
                self.token_url,
                authorization_response=server.queue.get(),
                code_verifier=self.code_verifier,
                include_client_id=True,
            )

            return self._create_token_info(self.session.token)["id_token"]

        except KeyboardInterrupt:
            from rich.control import Control
            from rich.segment import ControlType

            self.console.control(Control(ControlType.CARRIAGE_RETURN))
            self.console.print("Canceling SSO request")
            self.console.print()
            server.server_close()

            return None

    def login_device_flow(self) -> t.Optional[str]:
        response = self.session.request(
            "POST",
            self.auth_url + "/device",
            data={"client_id": self.client_id, "scope": self.scope},
            withhold_token=True,
        )
        if response.status_code != 200:
            raise ValueError("Failed to initiate device flow")
        response_json = response.json()
        device_code = response_json["device_code"]
        user_code = response_json["user_code"]
        full_verification_url = response_json["verification_uri_complete"]

        self.console.print("Logging into [tobiko]Tobiko Cloud[/tobiko]")
        self.console.print(f"Please verify the following device code in your browser: {user_code}")
        self._open_browser_flow(full_verification_url)

        try:
            while True:
                response = self.session.request(
                    "POST",
                    self.token_url,
                    data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "device_code": device_code,
                        "client_id": self.client_id,
                    },
                    withhold_token=True,
                )
                if response.status_code == 400:
                    if response.json().get("error", "") == "authorization_pending":
                        time.sleep(5)
                        continue
                    raise ValueError("Failed to poll device flow")
                if response.status_code != 200:
                    raise ValueError("Failed to poll device flow")
                self.console.print("[success]Success![/success] :white_check_mark:")
                self.console.print()
                return self._create_token_info(response.json())["id_token"]

        except KeyboardInterrupt:
            from rich.control import Control
            from rich.segment import ControlType

            self.console.control(Control(ControlType.CARRIAGE_RETURN))
            self.console.print("Canceling SSO request")
            self.console.print()

            return None

    def refresh_token(self) -> t.Optional[str]:
        # Can we use client credentials?
        if self.client_secret:
            return self.login_with_client_credentials()

        if not self.token_info:
            self.console.print("Not currently authenticated", style="error")
            return None

        current_refresh_token = self.token_info["refresh_token"]

        if not current_refresh_token:
            self.console.print("Refresh token not available", style="error")
            return None

        self.console.print("Refreshing your authentication token :arrows_counterclockwise:")
        self.session.refresh_token(
            self.token_url, refresh_token=current_refresh_token, scope=self.token_info["scope"]
        )

        return self._create_token_info(self.session.token)["id_token"]

    def _create_token_info(self, token: t.Dict) -> t.Dict:
        self.token_info = {
            "scope": token["scope"],
            "token_type": token["token_type"],
            "id_token": token["id_token"],
        }

        if "expires_at" in token:
            self.token_info["expires_at"] = token["expires_at"]
        elif "expires_in" in token:
            self.token_info["expires_at"] = math.floor(time.time() + token["expires_in"])

        if "access_token" in token:
            self.token_info["access_token"] = token["access_token"]

        if "refresh_token" in token:
            self.token_info["refresh_token"] = token["refresh_token"]

        self._save_auth_yaml(self.token_info)

        return self.token_info

    def vscode_status(self) -> t.Tuple[bool, t.Dict]:
        """
        Returns whether the user is logged in and the token payload if they are.
        """
        id_token = self.id_token(login=False)
        if not id_token:
            return False, {}

        parts = id_token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid id_token, expected 3 parts, got %d", len(parts))

        # The payload is base64url encoded, decode it
        payload = parts[1]
        # Add padding if needed
        payload += "=" * (4 - len(payload) % 4) if len(payload) % 4 else ""
        # Replace URL-safe characters and decode
        payload = payload.replace("-", "+").replace("_", "/")
        # Decode the base64 string
        decoded_payload = base64.b64decode(payload)
        # Parse the JSON
        token_payload = json.loads(decoded_payload)

        return True, token_payload

    def vscode_get_login_url(self) -> t.Tuple[str, str]:
        """
        Login to Tobiko Cloud for use in VSCode.

        This will open a browser to the login page and then return the token.
        As well as the verifier code.
        """
        auth_url, _ = self.session.create_authorization_url(
            self.auth_url,
            code_verifier=self.code_verifier,
        )
        return auth_url, self.code_verifier

    def vscode_start_server(self) -> None:
        server = SSOHTTPServer()
        thread = threading.Thread(target=server.handle_request)
        thread.start()
        try:
            thread.join()
            self.session.fetch_token(
                self.token_url,
                authorization_response=server.queue.get(),
                code_verifier=self.code_verifier,
                include_client_id=True,
            )
            self._create_token_info(self.session.token)
            return None

        except KeyboardInterrupt:
            server.server_close()
            return None

    def vscode_initiate_device_flow(self) -> t.Dict:
        response = self.session.request(
            "POST",
            self.auth_url + "/device",
            data={
                "client_id": self.client_id,
                "scope": self.scope,
            },
            withhold_token=True,
        )
        if response.status_code != 200:
            raise ValueError("Failed to initiate device flow")
        return response.json()

    def vscode_poll_device_flow(self, device_code: str) -> bool:
        """
        Poll the device flow for VSCode integration.

        Returns True if the device flow is successful, False otherwise. Throws an error if the device flow fails.
        """
        response = self.session.request(
            "POST",
            self.token_url,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
                "client_id": self.client_id,
            },
            withhold_token=True,
        )
        if response.status_code == 400:
            device_pending = response.json().get("error", "").startswith("authorization_pending")
            if device_pending:
                return False
            raise ValueError("Failed to poll device flow")
        if response.status_code != 200:
            raise ValueError("Failed to poll device flow")
        self._create_token_info(response.json())
        return True


class BearerAuth(Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(self, request: Request) -> t.Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class TobikoAuth(Auth):
    def __init__(self, project_token: t.Optional[str] = None) -> None:
        self.project_token = project_token
        self.sso: t.Optional[SSOAuth] = None

    def sso_request(self, request: Request) -> Request:
        if self.sso:
            id_token = self.sso.id_token(login=True)
            request.headers["Authorization"] = f"Bearer {id_token}"
        return request

    def sync_auth_flow(self, request: Request) -> t.Generator[Request, Response, None]:
        if CLIENT_SECRET:
            self.sso = tcloud_sso()
            yield self.sso_request(request)
            return

        if self.project_token:
            request.headers["Authorization"] = f"Bearer {self.project_token}"
            yield request
            return

        if self.sso:
            yield self.sso_request(request)
            return

        # Try any request and if it fails, get the SSO token and try again
        response = yield request
        if response.status_code == 401:
            # We need SSO!
            self.sso = tcloud_sso()
            yield self.sso_request(request)

    async def async_auth_flow(self, request: Request):  # type: ignore
        raise RuntimeError("Cannot use a sync authentication class with httpx.AsyncClient")
