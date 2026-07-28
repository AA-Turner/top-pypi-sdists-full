from __future__ import annotations

from dataclasses import dataclass
import json
import math
import os
import stat
import threading
import time
import typing as t
import webbrowser
import requests
from pathlib import Path
from queue import Empty

from authlib.common.security import generate_token
from authlib.integrations.requests_client import OAuth2Session
from query_cache_common.auth import Scope
from rich.console import Console
from rich.theme import Theme

from dbt_state.auth.sso_server import LOCAL_OAUTH_PORT, SsoHttpServer
from dbt_state.auth.utils import parse_jwt
from dbt_state.config import CLIENT_ID_DEFAULT, DBT_RUN_CACHE_PATH, get_env, DbtPlatformToken
from dbt_state.errors import AuthenticationError, RecoverableAuthenticationError
from dbt_state import events

ORGS_SCOPE = "runcache:scope:orgs"
"""The scope to request from the auth service"""

REDIRECT_URI = f"http://127.0.0.1:{LOCAL_OAUTH_PORT}/handler"
"""The local redirect_uri value to use"""

AUTH_URL = get_env("AUTH_URL", "https://auth.state.dbt.com")
"""The OAuth authorization endpoint to use"""

TOKEN_URL = get_env("TOKEN_URL", "https://auth.state.dbt.com/token")
"""The OAuth token endpoint to use"""


THEME = Theme(
    {
        "error": "red",
        "success": "green",
        "url": "bright_blue",
        "key": "magenta",
    }
)
"""The Rich console theme to use in the CLI"""


def _warn_config_dir_not_writable(path: Path, error: OSError) -> None:
    """Warn that the dbt State config directory cannot be written to.

    Credentials are cached in this directory, so an unwritable path means the CLI has to
    re-authenticate on every invocation, but it never prevents the current invocation from
    authenticating.
    """
    events.fire_warn_event_suboptimal(
        "Unable to write to the dbt State config directory ({}): {}. Credentials cannot be cached, "
        "so authentication is repeated on every invocation",
        str(path),
        str(error),
    )


@dataclass
class Org:
    org_id: str
    flags: t.List[str]
    is_dbt: bool
    dimensions: t.Optional[OrgDimensions]
    account_host: t.Optional[str]


@dataclass
class OrgDimensions:
    free_trial_end_date: t.Optional[str]
    in_free_trial: bool


def sso_auth(
    auth_url: str = AUTH_URL,
    token_url: str = TOKEN_URL,
    client_id: str = CLIENT_ID_DEFAULT,
    client_secret: t.Optional[str] = None,
    org_id: t.Optional[str] = None,
    code_verifier: t.Optional[str] = None,
    auth_json_path: Path = DBT_RUN_CACHE_PATH,
    console: t.Optional[Console] = None,
    dbt_platform_tokens: t.Optional[t.List[DbtPlatformToken]] = None,
) -> SsoAuth:
    sso_auth = SsoAuth(
        auth_url=auth_url,
        token_url=token_url,
        client_id=client_id,
        scope=ORGS_SCOPE,
        auth_json_path=auth_json_path,
        client_secret=client_secret,
        code_verifier=code_verifier,
        console=console,
        org_id=org_id,
        dbt_platform_tokens=dbt_platform_tokens,
    )
    sso_auth.init_from_cache()
    return sso_auth


class SsoAuth:
    """This class handles the OAuth flows and CLI process for getting an ID token to use with API calls that require it."""

    def __init__(
        self,
        auth_url: str,
        token_url: str,
        client_id: str,
        scope: str,
        auth_json_path: Path,
        client_secret: t.Optional[str] = None,
        console: t.Optional[Console] = None,
        code_verifier: t.Optional[str] = None,
        org_id: t.Optional[str] = None,
        dbt_platform_tokens: t.Optional[t.List[DbtPlatformToken]] = None,
    ) -> None:
        self._auth_url = auth_url
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._console = console or Console(theme=THEME)
        self._code_verifier = code_verifier or generate_token(48)
        self._configured_org_id = org_id
        self._dbt_platform_tokens = dbt_platform_tokens or []

        try:
            auth_json_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            # a read-only or foreign-owned home directory (common in containers running as an
            # arbitrary uid) must not prevent authentication, only credential caching
            _warn_config_dir_not_writable(auth_json_path, e)
        self._auth_json_path = auth_json_path

        self._session = OAuth2Session(
            self._client_id,
            self._client_secret,
            redirect_uri=REDIRECT_URI,
            scope=self._scope,
            code_challenge_method="S256",
        )
        self._token_info: t.Optional[t.Dict] = None
        self._token_scope: t.Optional[Scope] = None
        self._token_info_lock = threading.Lock()

    def init_from_cache(self) -> None:
        with self._token_info_lock:
            if not self._token_info:
                self._token_info = self._load_auth_json()
                self._token_scope = (
                    Scope.from_string(self._token_info.get("scope", ""))
                    if self._token_info
                    else None
                )

    def auth_info(self) -> t.Dict:
        token_info = self._load_auth_json()
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
                self._console.print("Current SSO session expired", style="error")
                return
            self._console.print("Not currently authenticated", style="error")
            return

        self._console.print(
            f"Current dbt State SSO session expires in [success]{auth_info['expires_in']}[/success] minutes"
        )
        claims = auth_info.get("claims", {})
        if claims and claims["sub"] == claims["aud"]:
            client_id = claims["sub"]
            self._console.print("[url]Service to Service Token[/url]")
            self._console.print(f"[key]Client ID:[/key] {client_id}")
        else:
            self._console.print("[url]User Token[/url]")

        if "email" in claims:
            email = claims["email"]
            self._console.print(f"[key]Email:[/key] {email}")
        if "name" in claims:
            name = claims["name"]
            self._console.print(f"[key]Name:[/key] {name}")
        if "scope" in claims:
            scope = claims["scope"]
            self._console.print(f"[key]Scope:[/key] {scope}")

    def is_logged_in(self) -> bool:
        with self._token_info_lock:
            try:
                self._get_or_refresh_token_info(login=False)
                return True
            except AuthenticationError:
                return False

    def org_id(self, login: bool = False) -> str:
        with self._token_info_lock:
            self._get_or_refresh_token_info(login)
            if self._token_scope is None:
                raise AuthenticationError("Not currently authenticated")
            return self._determine_org_id(self._token_scope)

    def id_token(self, login: bool = False) -> str:
        """Returns the id_token needed for SSO.

        Will return the one saved on disk, unless it's expired. If the token on disk is expired,
        it will try to refresh it. If there is no token on disk, it will start the SSO process
        to get a new one if login is True.
        """
        with self._token_info_lock:
            return self._get_or_refresh_token_info(login)["id_token"]

    def logout(self) -> None:
        with self._token_info_lock:
            self._delete_auth_json()
            self._console.print("Logged out of dbt State")

    def login(self) -> t.Optional[str]:
        with self._token_info_lock:
            return self._login()["id_token"]

    def refresh_token(self) -> t.Optional[str]:
        with self._token_info_lock:
            return self._refresh_token()["id_token"]

    def is_personal_org(self) -> bool:
        """Return True if the authenticated token marks the org as a personal sandbox.

        Orgs are marked as personal if the user is in a personal org only.
        """
        with self._token_info_lock:
            if not self._token_info:
                return False
            try:
                _, claims, _ = parse_jwt(self._token_info["id_token"])
            except Exception:
                return False
            return bool(claims.get("personal", False))

    def get_org_info(self, org_id: str) -> t.Optional[Org]:
        """Fetch organization metadata from the auth service for the given org."""
        try:
            token = self.id_token(login=False)
            response = requests.get(
                f"{self._auth_url}/api/orgs/{org_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
            )
            response.raise_for_status()
            data = response.json()
            org = data["org"]
            dimensions = data.get("dimensions")

            return Org(
                org_id=org_id,
                flags=org.get("flags", []),
                is_dbt=org.get("is_dbt", False),
                dimensions=OrgDimensions(
                    in_free_trial=dimensions.get("in_free_trial", False),
                    free_trial_end_date=dimensions.get("free_trial_end_date"),
                )
                if dimensions
                else None,
                account_host=org.get("account_host"),
            )

        except Exception as e:
            events.fire_debug_event("Failed to fetch org info: {}", str(e))
            return None

    def _get_or_refresh_token_info(self, login: bool) -> t.Dict:
        if self._token_info and self._token_scope:
            # If we are within 5 minutes of expire time, run refresh
            is_fresh = self._token_info.get("expires_at", 0.0) > (time.time() + 300)

            # If a configured org_id isn't in the cached scope, force a refresh in case
            # the user's permissions changed since the cache was last saved.
            needs_scope_refresh = bool(
                self._configured_org_id
                and not self._token_scope.is_org_id_in_scope(self._configured_org_id)
            )

            if is_fresh and not needs_scope_refresh:
                return self._token_info

            try:
                return self._refresh_token()
            except Exception:
                if is_fresh:
                    # Token itself is still valid; return it and let _determine_org_id
                    # surface any scope mismatch as a proper error instead of triggering
                    # browser re-auth.
                    return self._token_info
                # Token is expired and refresh failed; clear cache and fall through to login.
                self._delete_auth_json()

        if login:
            # We should get a new token
            return self._login()

        raise AuthenticationError("Not currently authenticated")

    def _login(self) -> t.Dict:
        if self._client_secret:
            return self._login_with_client_credentials()
        if self._dbt_platform_tokens:
            # this will raise an error and abort if none of the tokens can be exchanged
            # this is deliberate; if platform tokens are present they need to work and not fall back to browser auth
            return self._exchange_dbt_platform_token_for_state_token()

        with SsoHttpServer() as server:
            thread = threading.Thread(target=server.handle_request, daemon=True)
            thread.start()

            auth_url, _ = self._session.create_authorization_url(
                self._auth_url,
                code_verifier=self._code_verifier,
            )

            self._console.print("Logging into dbt State")
            self._open_browser_flow(auth_url)

            try:
                self._console.print()
                with self._console.status(
                    "Waiting... You can [key]Ctrl-C[/key] to cancel this request."
                ):
                    thread.join(timeout=server.timeout)

                # Try to get callback from queue with a short timeout to handle race conditions
                try:
                    callback_url = server.queue.get(timeout=1.0)
                except Empty:
                    raise AuthenticationError(
                        f"Authentication timed out after {server.timeout} seconds. "
                        "Please try again and complete the login in your browser."
                    )

                self._session.fetch_token(
                    self._token_url,
                    authorization_response=callback_url,
                    code_verifier=self._code_verifier,
                    include_client_id=True,
                )

                token_info = self._update_token_info(self._session.token)

                self._console.print("[success]Success![/success] :white_check_mark:")
                self._console.print()

                return token_info

            except KeyboardInterrupt:
                from rich.control import Control
                from rich.segment import ControlType

                self._console.control(Control(ControlType.CARRIAGE_RETURN))
                self._console.print("Canceling SSO request")
                self._console.print()

                raise

    def _login_with_client_credentials(self) -> t.Dict:
        try:
            self._session.fetch_token(
                self._token_url,
                grant_type="client_credentials",
            )
            return self._update_token_info(self._session.token)
        except AuthenticationError:
            raise
        except Exception as e:
            # this also catches failures unrelated to the credentials themselves (e.g. no network
            # egress to the auth service), so log the cause for debugging, but keep it out of the
            # user-facing message where an arbitrary exception string would only confuse
            events.fire_debug_event("Client credentials login failed: {}", str(e))
            raise AuthenticationError(
                "Error logging in with client credentials. Please make sure that the DBT_ENGINE_STATE_OAUTH_CLIENT_ID and DBT_ENV_SECRET_STATE_OAUTH_CLIENT_SECRET environment variables (or associated file-based config) are set to the right values"
            ) from e

    def _exchange_dbt_platform_token_for_state_token(self) -> t.Dict:
        # try all of them, the first one that works wins
        token_count = len(self._dbt_platform_tokens)

        for token in self._dbt_platform_tokens:
            token_prefix = token.token[:8]
            try:
                exchanged_token = self._session.fetch_token(
                    url=self._token_url,
                    grant_type="urn:ietf:params:oauth:grant-type:token-exchange",
                    subject_token_type="dbt",
                    subject_token=token.token,
                    dbt_hostname=token.host,
                    client_id=self._client_id,
                )
                # error responses are missing a `id_token` key and contain error details in the `detail` key
                if (
                    isinstance(exchanged_token, dict)
                    and "id_token" not in exchanged_token
                    and (detail := exchanged_token.get("detail"))
                ):
                    raise AuthenticationError(detail)
                else:
                    token_info = self._update_token_info(exchanged_token)
                    # _update_token_info may throw so don't declare the token "exchanged" until it passes
                    events.fire_debug_event(
                        "Exchanged dbt platform token '{}' for a state token", token_prefix
                    )
                    return token_info
            except Exception as e:
                events.fire_debug_event(
                    "Failed to exchange dbt platform token '{}' (host: '{}') for a dbt state token: {}",
                    token_prefix,
                    token.host,
                    str(e),
                )
                if token_count == 1:
                    # reraise directly if there was only a single token to check, so the user doesnt need to sift through dbt.log
                    raise RecoverableAuthenticationError(
                        f"Failed to obtain dbt State authentication token: {str(e)}"
                    ) from e

        raise RecoverableAuthenticationError(
            f"Unable to exchange dbt platform token for a dbt State authentication token (tried {len(self._dbt_platform_tokens)} tokens).\n"
            "Please see dbt.log for details"
        )

    def _refresh_token(self) -> t.Dict:
        if self._client_secret:
            return self._login_with_client_credentials()

        if not self._token_info:
            raise AuthenticationError("Not currently authenticated")

        current_refresh_token = self._token_info["refresh_token"]
        if not current_refresh_token:
            raise AuthenticationError("Refresh token not available")

        self._session.refresh_token(
            self._token_url, refresh_token=current_refresh_token, scope=None
        )

        return self._update_token_info(self._session.token)

    def _open_browser_flow(self, auth_url: str) -> None:
        try:
            webbrowser.open(auth_url)
            self._console.print()
            self._console.print(
                "Opening your browser to the signin URL [success]:globe_with_meridians:[/success]"
            )
        except Exception:
            pass

        self._console.print()
        self._console.print(
            "If a browser doesn't open on your system please go to the following url:"
        )
        self._console.print(f"[url]{auth_url}[/url]")

    @property
    def _auth_json_file(self) -> Path:
        return self._auth_json_path / "state_auth.json"

    def _delete_auth_json(self) -> None:
        """Removes the auth.json file if it exists."""
        self._token_info = None
        self._token_scope = None
        auth_file = self._auth_json_file
        if auth_file.exists() and os.access(auth_file, os.W_OK):
            os.remove(auth_file)

    def _load_auth_json(self) -> t.Optional[t.Dict]:
        """Loads the full auth.json file that might exist in the CLI config folder."""
        auth_file = self._auth_json_file

        if auth_file.exists() and os.access(auth_file, os.R_OK):
            with auth_file.open("r", encoding="utf-8") as fd:
                data = json.load(fd)

            if SsoAuth._is_legacy_token(data):
                self._delete_auth_json()
                return None

            return data

        return None

    def _save_auth_json(self, data: t.Dict) -> None:
        """Saves the given dictionary to auth.json.

        Args:
            data: The dictionary to save
        """
        auth_file = self._auth_json_file

        try:
            with auth_file.open("w", encoding="utf-8") as fd:
                json.dump(data, fd)
            os.chmod(auth_file, stat.S_IWUSR | stat.S_IRUSR)
        except OSError as e:
            # the token is already usable in memory, so a failed write only costs us the cache
            _warn_config_dir_not_writable(auth_file, e)

    def _update_token_info(self, token: t.Dict) -> t.Dict:
        id_token = token["id_token"]
        claims = parse_jwt(id_token)[1]
        scope_str = claims.get("scope", "")
        token_scope = Scope.from_string(scope_str)

        new_token_info = {
            "scope": scope_str,
            "token_type": token["token_type"],
            "id_token": id_token,
        }

        if "expires_at" in token:
            new_token_info["expires_at"] = token["expires_at"]
        elif "expires_in" in token:
            new_token_info["expires_at"] = math.floor(time.time() + token["expires_in"])

        if "access_token" in token:
            new_token_info["access_token"] = token["access_token"]

        if "refresh_token" in token:
            new_token_info["refresh_token"] = token["refresh_token"]

        self._save_auth_json(new_token_info)
        self._token_info = new_token_info
        self._token_scope = token_scope
        return self._token_info

    def _determine_org_id(self, scope: Scope) -> str:
        """Determine the organization ID from configuration or token scope.

        Priority:
        1. Configured org_id (from constructor)
        2. Auto-detect from single org in scope (excluding wildcards)
        3. Error if ambiguous

        Args:
            scope: The scope from the token claims

        Returns:
            The determined organization ID

        Raises:
            AuthenticationError: If org ID cannot be determined
        """
        if self._configured_org_id:
            if scope.is_org_id_in_scope(self._configured_org_id):
                return self._configured_org_id
            if scope.is_org_id_disabled(self._configured_org_id):
                raise RecoverableAuthenticationError(
                    f"User access to the requested organization (org_id: {self._configured_org_id}) has been disabled."
                )
            raise AuthenticationError(
                f"User does not have access to the requested organization (org_id: {self._configured_org_id}). Please make sure your user account has access to this organization or specify a different organization that you have access to in the project configuration."
            )

        org_ids = scope.org_ids
        if not org_ids:
            disabled_org_ids = scope.disabled_org_ids
            if len(disabled_org_ids) == 1:
                raise RecoverableAuthenticationError(
                    f"User access to the requested organization (org_id: {disabled_org_ids[0]}) has been disabled."
                )
            raise AuthenticationError(
                "Cannot determine organization ID from token. Please specify which organization to use by setting 'state-org-id' in the 'dbt-cloud' config block in the project configuration."
            )
        if len(org_ids) == 1 and org_ids[0] != "*":
            return org_ids[0]
        raise AuthenticationError(
            f"Token has access to multiple organizations: {', '.join(org_ids)}. "
            "Please specify which organization to use by setting by setting 'state-org-id' in the 'dbt-cloud' config block in the project configuration."
        )

    @staticmethod
    def _is_legacy_token(token_info: t.Dict) -> bool:
        """Returns True if the cached token targets the old auth issuer or uses old scopes."""
        scope = token_info.get("scope", "")
        if "conway:scope" in scope:
            return True

        id_token = token_info.get("id_token")
        if id_token:
            try:
                _, claims, _ = parse_jwt(id_token)
                if "auth.conway.fivetran.com" in claims.get("iss", ""):
                    return True
            except Exception:
                pass

        return False
