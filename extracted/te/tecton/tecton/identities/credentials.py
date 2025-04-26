import sys
import urllib
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import requests

from tecton._internals import metadata_service
from tecton._internals.utils import cluster_url
from tecton.cli import printer
from tecton.cli import workspace
from tecton.cli.workspace_utils import switch_to_workspace
from tecton.identities import api_keys
from tecton.identities import okta
from tecton_core import conf
from tecton_core import http
from tecton_core.errors import TectonNotFoundError
from tecton_core.id_helper import IdHelper
from tecton_proto.auth.authorization_service__client_pb2 import GetIsAuthorizedRequest
from tecton_proto.auth.authorization_service__client_pb2 import Permission
from tecton_proto.auth.principal__client_pb2 import PrincipalType
from tecton_proto.auth.resource__client_pb2 import ResourceType


@attrs.frozen
class ServiceAccountProfile:
    id: str
    name: str
    description: str
    created_by: str
    is_active: bool
    obscured_key: str


@attrs.frozen
class LoginTempState:
    login_configs: Dict[str, Any]
    code_verifier: str
    redirect_uri: str
    tecton_url: str
    # between requesting the auth code and exchanging it to complete login, okta_auth_flow
    okta_auth_flow: okta.OktaAuthorizationFlow


notebook_login_temp_result = None


def _set_credentials_impl(tecton_api_service_url: Optional[str], tecton_api_key: Optional[str]) -> None:
    """
    Implementation for the deprecated set_credentials. Params must be Optional to still provide support in 1.0.

    :param tecton_api_service_url: Tecton API URL
    :param tecton_api_key: Tecton API Key
    """
    if tecton_api_key:
        conf.set("TECTON_API_KEY", tecton_api_key)
    if tecton_api_service_url:
        conf.validate_api_service_url(tecton_api_service_url)
        conf.set("API_SERVICE", tecton_api_service_url)


def _clear_credentials_impl() -> None:
    for key in (
        "TECTON_API_KEY",
        "API_SERVICE",
        "OAUTH_ACCESS_TOKEN",
        "OAUTH_REFRESH_TOKEN",
        "OAUTH_ACCESS_TOKEN_EXPIRATION",
    ):
        try:
            conf.unset(key)
        except KeyError:
            pass


def get_caller_identity() -> Union[ServiceAccountProfile, okta.UserProfile]:
    """
    Introspect the current User or API Key used to authenticate with Tecton.

    :return: The UserProfile or ServiceAccountProfile of the current User or API Key (respectively)
      if the introspection is successful.
    :raises SystemError: If the credentials are expired, invalid, or not configured.
    """
    print(f"Tecton Endpoint {cluster_url()}")

    user_profile = okta.get_user_profile()
    if user_profile:
        user_is_on_cluster = _check_user_can_read_org(user_profile.id)
        if user_is_on_cluster:
            return user_profile
        else:
            msg = (
                "Unable to authenticate using the configured user credentials. "
                "Please rerun `tecton login` with the CLI "
                "or `tecton.login(tecton_url=<tecton_url>)` in your notebook."
            )
            raise SystemError(msg)
    else:
        token = conf.get_or_none("TECTON_API_KEY")
        if token:
            token_invalid = False
            try:
                introspect_result = api_keys.introspect(token)
            except (PermissionError, TectonNotFoundError):
                token_invalid = True
            # raise this error outside of the except to avoid chaining errors, to avoid eyesore in notebook envs
            if token_invalid:
                msg = (
                    "Permissions error when introspecting the Tecton API key. "
                    "The API key is invalid, please try authenticating again."
                )
                raise SystemError(msg)
            if introspect_result is not None:
                return ServiceAccountProfile(
                    id=IdHelper.to_string(introspect_result.id),
                    name=introspect_result.name,
                    description=introspect_result.description,
                    created_by=introspect_result.created_by,
                    is_active=introspect_result.active,
                    obscured_key=f"****{token[-4:]}",
                )

    msg = (
        "No user profile or service account configured. To authenticate "
        "using an API key, run `tecton.login(tecton_url=<tecton_url>, tecton_api_key=<key>)`. "
        "To authenticate as your user, run `tecton login` with the CLI or "
        "`tecton.login(tecton_url=<tecton_url>)` in your notebook."
    )
    raise SystemError(msg)


def _check_user_can_read_org(user_id: str) -> bool:
    request = GetIsAuthorizedRequest(
        principal_type=PrincipalType.PRINCIPAL_TYPE_USER,
        principal_id=user_id,
        permissions=[
            Permission(
                resource_type=ResourceType.RESOURCE_TYPE_ORGANIZATION,
                action="read_organization",
            )
        ],
    )
    try:
        response = metadata_service.instance().GetIsAuthorized(request)
    except PermissionError as e:
        # if the user doesn't exist in SpiceDB, it will say resource not found
        return False
    return len(response.permissions) > 0 and response.permissions[0].action == "read_organization"


def logout() -> None:
    """
    Clear credentials from the interactive Python session that were previously set via `login()`.
    """
    _clear_credentials_impl()
    global notebook_login_temp_result
    notebook_login_temp_result = None
    printer.safe_print(
        "✅ Successfully cleared Service Account API key and User credentials from session. Use `tecton.login()` to re-authenticate."
    )
    if conf.get_or_none("TECTON_API_KEY") is not None:
        print(
            "👉️ TECTON_API_KEY is still set in an environment variable or in a Secret Manager, so that credential will still be used until it is cleared."
        )


def login(
    tecton_url: str,
    interactive: bool = True,
    tecton_api_key: Optional[str] = None,
) -> None:
    """
    Authenticate to a Tecton instance either as a user or with a Tecton API key.

    These credentials last for the duration of the interactive Python session. If
    both Service Account API key credentials and user credentials are set in the same
    session with multiple invocations of this method, user credentials will take priority
    when authenticating.

    If logging in as a user, the method will prompt you to open a link in your browser.
    Sign in to Tecton and it will display an authorization code to copy and paste into
    standard input back in your notebook.

    If your interactive environment does not support standard input (for example EMR
    notebooks do not), you can set `interactive=False` and use the 2-step login
    flow. First, run:
    ```
    tecton.login(tecton_url="https://<example>.tecton.ai", interactive=False)
    ```
    Then follow the URL to get your authorization code, and finally, run:
    ```
    tecton.complete_login("<authorization_code>")
    ```
    #### Example usages:
    To authenticate interactively as a user:
    ```
    tecton.login(tecton_url="https://<example>.tecton.ai")
    ```
    To authenticate non-interactively as a user
    ```
    tecton.login(tecton_url="https://<example>.tecton.ai", interactive=False)
    ```
    To authenticate with a Tecton API key
    ```
    tecton.login(tecton_url="https://<example>.tecton.ai", tecton_api_key="<api_key>")
    ```

    :param tecton_url: HTTP URL of the Tecton instance, e.g. `https://<example>.tecton.ai`
    :param interactive: Only for user login. When set to True, you will be prompted to pass the
                        authorization code via standard input to complete login. This relies on
                        your interactive environment supporting Python's builtin
                        [`input()`](https://docs.python.org/3/library/functions.html#input)
                        function. If your environment does not support this, you can call `login()`
                        with `interactive=False` to bypass the standard input prompt, and then pass
                        the authorization code to `tecton.complete_login("<authorization_code>")`
                        to complete login.
    :param tecton_api_key: Optional Tecton API key. Set to authenticate as a Service Account.
    """
    # Validate inputs
    if tecton_api_key:
        if not interactive:
            printer.safe_print(
                "If using `tecton_api_key`, cannot use the `interactive` parameter. Please use "
                '`tecton.login(tecton_url="https://<example>.tecton.ai", tecton_api_key="<api_key>")`.'
            )
            return

    url = _lint_tecton_url(tecton_url)

    if tecton_api_key:
        conf.delete_okta_tokens()
        tecton_api_service_url = urllib.parse.urljoin(url, "api")
        _set_credentials_impl(tecton_api_service_url=tecton_api_service_url, tecton_api_key=tecton_api_key)
        print("✅ Successfully set credentials.")
    else:
        _user_login(tecton_url, interactive)


def _user_login(url: str, interactive: bool) -> None:
    current_url = cluster_url()
    if current_url:
        if current_url == url:
            # logging into same cluster
            user_profile = None
            try:
                user_profile = okta.get_user_profile()
            except PermissionError as e:
                # Okta token expired
                print("Re-authenticating. Previous credentials no longer valid.")

            if user_profile:
                # test that the user can authenticate to the cluster
                if _check_user_can_read_org(user_profile.id):
                    print(
                        f"Already logged in to {current_url} as {user_profile}. To switch users, run `tecton.logout` then `tecton.login`"
                    )
                    return
                else:
                    print("Re-authenticating. Previous credentials no longer valid.")
        else:
            print(f"Re-authenticating. Switching from {current_url} to {url}")

    if interactive:
        try:
            # use BROWSER_MANUAL for now, can always make it nicer later
            temp_result, auth_code = _initiate_login_and_get_auth_code(url, okta.AuthFlowType.BROWSER_MANUAL)
        except EOFError:
            msg = "This environment does not support interactive login. Please use `tecton.login(tecton_url=<url>, interactive=False)`"
            raise SystemExit(msg)
        _complete_login_with_auth_code(temp_result, auth_code)
        printer.safe_print("✅ Authentication successful!")
    else:
        global notebook_login_temp_result
        notebook_login_temp_result = _initiate_noninterative_login(url)


def complete_login(authorization_code: str) -> None:
    """
    Complete non-interactive authentication to a Tecton instance as a user, by exchanging the authorization code for an access token.

    This requires that an authorization code was already first requested by calling
    `tecton.login(tecton_url="https://<example>.tecton.ai", interactive=False)`.
    Please see `login()` documentation for more details and example usage.

    :param authorization_code: Authorization code, copied from opening the URL printed after running
                               `tecton.login(tecton_url="https://<example>.tecton.ai", interactive=False)`
    """
    global notebook_login_temp_result
    if not notebook_login_temp_result:
        print(
            'Please generate an authorization code using `tecton.login(tecton_url="https://<example>.tecton.ai", interactive=False)` first.'
        )
        raise SystemExit()

    _complete_login_with_auth_code(
        temp_login_state=notebook_login_temp_result,
        auth_code=authorization_code,
    )

    printer.safe_print("✅ Authentication successful!")
    notebook_login_temp_result = None


def _initiate_noninterative_login(host: str) -> LoginTempState:
    """
    Used by Notebook SDK `tecton.login(interactive=False)` to request an auth code, but does not
    interactively get it. Does not return the auth code because the user will manually pass it later

    :param host:
    :return: LoginTempState with some login metadata that will be used to complete login in _complete_login_with_auth_code
    """
    host = _lint_tecton_url(host)
    login_configs = _get_login_configs(host)
    cli_client_id = login_configs["OKTA_CLI_CLIENT_ID"]

    flow = okta.OktaAuthorizationFlow(auth_flow_type=okta.AuthFlowType.NOTEBOOK_2_STEP)
    code_verifier, authorize_url, redirect_uri, _ = flow.generate_pkce_and_login_link(cli_client_id)

    print("Please visit the following link to login and access the authentication code:")
    print(f"{authorize_url}")
    print()
    print("Then use `tecton.complete_login(<authentication_code>)` to complete login")

    return LoginTempState(
        login_configs=login_configs,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
        tecton_url=host,
        okta_auth_flow=flow,
    )


def _initiate_login_and_get_auth_code(
    host: str,
    auth_flow_type: okta.AuthFlowType,
    okta_session_token: Optional[str] = None,
) -> Tuple[LoginTempState, str]:
    """
    Used by both CLI `tecton login` and Notebook SDK `tecton.login(interactive=True)` to request an
    auth code and also get it.

    :param url: URL of Tecton deployment, e.g. https://staging.tecton.ai
    :param auth_flow_type: okta.AuthFlowType (browser, manual, or session token)
    :param okta_session_token: Optional string for auth_flow_type SESSION_TOKEN

    :return: A Tuple with:
             - LoginTempState with some login metadata that will be used to complete login in _complete_login_with_auth_code
             - str: the authorization code
    """
    host = _lint_tecton_url(host)
    login_configs = _get_login_configs(host)
    cli_client_id = login_configs["OKTA_CLI_CLIENT_ID"]

    flow = okta.OktaAuthorizationFlow(auth_flow_type=auth_flow_type, okta_session_token=okta_session_token)
    auth_code, code_verifier, redirect_uri = flow.get_authorization_code(cli_client_id)

    login_temp_state = LoginTempState(
        login_configs=login_configs,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
        tecton_url=host,
        okta_auth_flow=flow,
    )
    return login_temp_state, auth_code


def _complete_login_with_auth_code(
    temp_login_state: LoginTempState,
    auth_code: str,
) -> None:
    """
    Completes login by exchanging the auth code for the oauth access token, and then
    setting tecton confs locally.
    """
    login_configs = temp_login_state.login_configs
    code_verifier = temp_login_state.code_verifier
    redirect_uri = temp_login_state.redirect_uri
    host = temp_login_state.tecton_url
    flow = temp_login_state.okta_auth_flow
    cli_client_id = login_configs["OKTA_CLI_CLIENT_ID"]

    access_token, _, refresh_token, access_token_expiration = flow.get_tokens(
        auth_code, code_verifier, redirect_uri, cli_client_id
    )
    if not access_token:
        printer.safe_print("Unable to obtain Tecton credentials")
        sys.exit(1)

    # when switching clusters
    if conf.get_or_none("API_SERVICE") != urllib.parse.urljoin(host, "api"):
        if conf.save_tecton_configs_enabled:
            # in the CLI, switch current workspace to prod
            switch_to_workspace(workspace.PROD_WORKSPACE_NAME)
        else:
            # in notebooks, clear MDS conf values from previous cluster
            conf._clear_metadata_server_config()
            # metadata service needs to be re-initialized, which will trigger new server config retrieval
            metadata_service.close_instance()

    new_api_service = urllib.parse.urljoin(host, "api")
    conf.set_login_configs(
        cli_client_id=cli_client_id,
        api_service=new_api_service,
        feature_service=new_api_service,
    )

    conf.set_okta_tokens(access_token, access_token_expiration, refresh_token)


def _lint_tecton_url(host: str) -> str:
    try:
        urllib.parse.urlparse(host)
    except Exception:
        printer.safe_print("Tecton Cluster URL must be a valid URL")
        sys.exit(1)
        # add this check for now since it can be hard to debug if you don't specify https and API_SERVICE fails
    if host is None or not (host.startswith(("https://", "http://localhost:"))):
        if host is not None and "//" not in host:
            return f"https://{host}"
        else:
            printer.safe_print("Tecton Cluster URL must start with https://")
            sys.exit(1)
    return host


def _get_login_configs(host: str) -> Dict[str, Any]:
    """
    Returns login configs from auth server
    """
    login_configs_url = urllib.parse.urljoin(host, "api/v1/metadata-service/get-login-configs")
    try:
        response = http.session().post(login_configs_url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(e)
    configs = response.json()["key_values"]

    return configs
