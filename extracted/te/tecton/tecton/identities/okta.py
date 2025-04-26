import base64
import enum
import hashlib
import http.server as http_server
import secrets
import socketserver
import sys
import time
from typing import Optional
from typing import Tuple
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse

import attrs
import click
import requests

from tecton_core import conf
from tecton_core import http


AUTH_SERVER = "https://login.tecton.ai/oauth2/default/.well-known/oauth-authorization-server"
USER_INFO_ENDPOINT = "https://login.tecton.ai/oauth2/default/v1/userinfo"

# this must match the uri that the okta application was configured with
OKTA_EXPECTED_PORTS = [10003, 10013, 10023]

# our http server will populate this when it receives the callback from okta
_CALLBACK_PATH = None


@attrs.frozen
class UserProfile:
    name: str
    email: str
    id: str


class OktaCallbackReceivingServer(http_server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        global _CALLBACK_PATH
        _CALLBACK_PATH = self.path
        self.send_response(301)
        self.send_header("Location", "https://www.tecton.ai/authentication-success")
        self.end_headers()


def get_metadata():
    try:
        response = http.session().get(AUTH_SERVER)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(e)
    return response.json()


# Okta docs: https://developer.okta.com/docs/guides/refresh-tokens/use-refresh-token/
class RefreshFlow:
    def __init__(self):
        self.metadata = get_metadata()

    def get_tokens(self, refresh_token):
        params = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": conf.get_or_none("CLI_CLIENT_ID"),
            "scope": "openid profile email",
        }
        try:
            return get_tokens_helper(self.metadata["token_endpoint"], params)
        except requests.RequestException as e:
            msg = "Authorization token expired. Please reauthenticate with `tecton login`"
            raise PermissionError(msg)


class AuthFlowType(enum.Enum):
    # Spin up local http server that can intercept the okta callback and avoid having to
    # copy & paste
    BROWSER_HANDS_FREE = 1

    # User manually opens link to login, and has to copy & paste the code.
    # Also used for notebook login (tecton.login())
    # Relies in Python's built in input() function
    BROWSER_MANUAL = 2

    # Tecton-internal session token authorization.
    SESSION_TOKEN = 3

    # Pyspark notebooks cannot use input() so BROWSER_MANUAL will not work.
    # Used for 2 step notebook login (tecton.login(interactive=False) + tecton.complete_login())
    NOTEBOOK_2_STEP = 4


# Okta docs: https://developer.okta.com/docs/guides/implement-auth-code-pkce/use-flow/
class OktaAuthorizationFlow:
    def __init__(
        self, auth_flow_type: AuthFlowType = AuthFlowType.BROWSER_HANDS_FREE, okta_session_token: Optional[str] = None
    ):
        self.metadata = get_metadata()
        self.auth_flow_type = auth_flow_type

        self.okta_session_token = okta_session_token

    def build_authorization_url(
        self,
        code_verifier: str,
        redirect_uri: str,
        cli_client_id: str,
    ) -> Tuple[str, str, str]:
        # base64's `urlsafe_b64encode` uses '=' as padding. These are not URL safe when used in URL paramaters.
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).rstrip(b"=")

        state = str(secrets.randbits(64))

        params = {
            "response_type": "code",
            "client_id": cli_client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": "openid offline_access profile email",
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        }
        if self.auth_flow_type == AuthFlowType.SESSION_TOKEN:
            params["sessionToken"] = self.okta_session_token
            params["response_mode"] = "query"
        authorize_url = f"{self.metadata['authorization_endpoint']}?{urlencode(params)}"
        return authorize_url, state

    def _browser_auth(self, code_verifier: str, cli_client_id: str) -> Tuple[str, str]:
        e: Optional[OSError] = None
        for port in OKTA_EXPECTED_PORTS:
            try:
                httpd = socketserver.TCPServer(("", int(port)), OktaCallbackReceivingServer)
                break
            except OSError as e:
                # socket in use, try other port
                if e.errno == 48:
                    continue
                else:
                    print(
                        "Encountered error with authorization callback. Your environment may not support automatic login; try running `tecton login --manual` instead.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
        else:
            if e:
                raise e

        redirect_uri = f"http://localhost:{port}/authorization/callback"
        authorize_url, state = self.build_authorization_url(code_verifier, redirect_uri, cli_client_id)
        print("Requesting authorization for Tecton CLI via browser. ")
        # Sleep before opening the browser to improve the UX and make it less jarring.
        time.sleep(1)
        try:
            print("If browser doesn't open automatically, use `tecton login --manual`")
            click.launch(authorize_url)
            httpd.handle_request()
        finally:
            httpd.server_close()

        return self._extract_code_from_url(_CALLBACK_PATH, state), redirect_uri

    def _extract_code_from_url(self, url: str, state: str) -> str:
        parsed = parse_qs(urlparse(url).query)
        if "error" in parsed:
            print(f"Encountered error: {parsed['error']}", file=sys.stderr)
            if "access_denied" in parsed["error"]:
                print(
                    "Please contact your Tecton administrator to verify you have been granted cluster access.",
                    file=sys.stderr,
                )
            sys.exit(1)
        code = parsed["code"][0]
        assert state == parsed["state"][0]
        from tecton.cli import printer

        printer.safe_print("✅ Authentication successful!")
        return code

    def _manual_auth(self, authorize_url):
        print("Please visit the following link to login and access the authentication code:")
        print(f"{authorize_url}")
        code = input("Paste authentication code here and press [Enter]:").strip()
        return code

    # NOTE: this is for internal use only. Requires an Okta session token.
    # This works by leveraging the Okta session token to skip browser-based
    # Okta authentication. The parameters are stored in the redirect uri from
    # Okta. https://developer.okta.com/docs/reference/api/oidc/#authorize
    def _session_token_auth(self, authorize_url: str, state: str) -> str:
        # We disallow redirects so that we can extract the code from the
        # redirect location.
        r = http.session().get(authorize_url, allow_redirects=False)
        r.raise_for_status()
        if r.status_code != 302:
            print("Unsuccessful headless Okta auth.", file=sys.stderr)
            sys.exit(1)
        url = r.headers.get("location")
        return self._extract_code_from_url(url, state)

    # To receive the auth code, we send the user to their browser to login to okta.
    # Once they've logged in, Okta will redirect them to a locally served webpage with the auth code.
    # Then, this function will return that auth code.
    def get_authorization_code(self, cli_client_id: str) -> Tuple[str, str, str]:
        code_verifier = secrets.token_urlsafe(43)

        if self.auth_flow_type == AuthFlowType.BROWSER_HANDS_FREE:
            code, redirect_uri = self._browser_auth(code_verifier, cli_client_id)
            return code, code_verifier, redirect_uri

        code_verifier, authorize_url, redirect_uri, state = self.generate_pkce_and_login_link(cli_client_id)

        if self.auth_flow_type == AuthFlowType.SESSION_TOKEN:
            code = self._session_token_auth(authorize_url, state)
        elif self.auth_flow_type == AuthFlowType.BROWSER_MANUAL:
            code = self._manual_auth(authorize_url)
        else:
            # NOTEBOOK_2_STEP gets the authorization code via manual user input
            msg = "AuthFlowType.NOTEBOOK_2_STEP should use generate_pkce_and_login_link"
            raise NotImplementedError(msg)
        return code, code_verifier, redirect_uri

    def generate_pkce_and_login_link(self, cli_client_id) -> Tuple[str, str, str, str]:
        """
        Generates the PKCE for OAuth: https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/#create-the-proof-key-for-code-exchange
        And /authorize URL and params needed to request an auth code: https://developer.okta.com/docs/guides/implement-grant-type/authcodepkce/main/#create-the-proof-key-for-code-exchange

        :return: Tuple of:
            1. code_verifier
            2. authorize_url
            3. redirect_uri
            4. state
            which are documented in the above 2 links
        """
        if self.auth_flow_type == AuthFlowType.BROWSER_HANDS_FREE:
            msg = "Not supported for AuthFlowType.BROWSER_HANDS_FREE."
            raise NotImplementedError(msg)

        code_verifier = secrets.token_urlsafe(43)
        redirect_uri = "https://www.tecton.ai/authorization-callback"
        authorize_url, state = self.build_authorization_url(code_verifier, redirect_uri, cli_client_id)

        return code_verifier, authorize_url, redirect_uri, state

    def get_tokens(self, auth_code, code_verifier, redirect_uri, cli_client_id):
        params = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "code_verifier": code_verifier,
            "redirect_uri": redirect_uri,
            "client_id": cli_client_id,
        }
        try:
            return get_tokens_helper(self.metadata["token_endpoint"], params)
        except Exception as e:
            raise SystemExit(e)


def get_tokens_helper(endpoint, params):
    response = http.session().post(endpoint, data=params)
    response.raise_for_status()

    response_json = response.json()
    access_token = response_json.get("access_token", None)
    id_token = response_json.get("id_token", None)
    refresh_token = response_json.get("refresh_token", None)
    expiration = time.time() + int(response_json.get("expires_in"))
    return access_token, id_token, refresh_token, expiration


# returns None if neither access nor refresh token are found in config
def get_token_refresh_if_needed():
    token = conf.get_or_none("OAUTH_ACCESS_TOKEN")
    if not token:
        return None
    expiration = conf.get_or_none("OAUTH_ACCESS_TOKEN_EXPIRATION")
    if expiration and time.time() < int(expiration):
        return token
    else:
        f = RefreshFlow()
        refresh_token = conf.get_or_none("OAUTH_REFRESH_TOKEN")
        if not refresh_token:
            return None
        access_token, _, _, expiration = f.get_tokens(refresh_token)
        conf.set_okta_tokens(access_token, expiration, refresh_token)
        return access_token


def get_user_profile() -> Optional[UserProfile]:
    token = get_token_refresh_if_needed()

    if not token:
        return None

    try:
        header = {"Authorization": f"Bearer {token}"}
        response = http.session().get(USER_INFO_ENDPOINT, headers=header)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Unable to get user info. Please try logging in again using `tecton login`")
        raise SystemExit(e)

    response = response.json()
    return UserProfile(
        name=response.get("name", ""),
        email=response.get("email", ""),
        id=response.get("sub", ""),
    )


if __name__ == "__main__":
    # what does this do?
    f = OktaAuthorizationFlow()
    code, verifier, redirect_uri = f.get_authorization_code()
    access_token, id_token, refresh_token, expiration = f.get_tokens(code, verifier, redirect_uri)

    rf = RefreshFlow()
    print(rf.get_tokens(refresh_token))
