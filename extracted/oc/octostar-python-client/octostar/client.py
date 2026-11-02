"""
client.py

This module provides functionalities to impersonate users for access with the OctoStar API.
User instances contain info like name, email, jwt-related data and, crucially, a client to execute API calls with.
A default user is provided via as_launching_user() (the user who launched the app).

Be careful! Imported modules in streamlit share their variables and functions between threads (= user sessions),
so you cannot pass around clients between modules of your code!

Example usage:
--------------
- Manually creating and using a client:
client = make_client(my_fixed_jwt, my_os_api_endpoint, my_ontology_name)
client.execute(query_ontology.sync, my_sql_query)

- Using a client with the context manager (passing the default client):
with as_launching_user() as client:
    client.execute(query_ontology.sync, my_sql_query)

- Using a client via the default client decorator:
@impersonating_launching_user()
def my_function(client):
    client.execute(query_ontology.sync, my_sql_query)

- Wrapper for local development via flag:
@impersonating_launching_user()
@dev_mode(dev_flag=os.environ.get('OS_DEV_MODE'), fixed_jwt=os.environ.get('OS_JWT'), api_endpoint=os.environ.get('OS_API_ENDPOINT'), ontology_name=os.environ.get('OS_ONTOLOGY'))
def my_function(client):
    client.execute(query_ontology.sync, my_sql_query)
"""

import base64
import json
import os
import ssl
import time
import re
from urllib.parse import urlparse, urlunparse
import jwt
import logging
from pathlib import Path
from typing import Any, Callable, Dict, Union, List, TypeVar
from functools import wraps
import attr
import hashlib
from warnings import warn

# Streamlit imports are lazy-loaded when needed

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

T = TypeVar("T")

OS_JWT_SECRET_PATH = "/etc/secrets/OS_JWT"
REQUIRED_ENV_VARS = ["OS_API_ENDPOINT", "OS_ONTOLOGY"]


@attr.s(auto_attribs=True)
class Client:
    """A class for keeping track of data related to the API

    Attributes:
        base_url: The base URL for the API, all requests are made to a relative path to this URL
        cookies: A dictionary of cookies to be sent with every request
        headers: A dictionary of headers to be sent with every request
        timeout: The maximum amount of a time in seconds a request can take. API functions will raise
            httpx.TimeoutException if this is exceeded.
        verify_ssl: Whether or not to verify the SSL certificate of the API server. This should be True in production,
            but can be set to False for testing purposes.
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document.
        follow_redirects: Whether or not to follow redirects. Default value is False.
    """

    base_url: str
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(5.0, kw_only=True)
    verify_ssl: Union[str, bool, ssl.SSLContext] = attr.ib(True, kw_only=True)
    raise_on_unexpected_status: bool = attr.ib(False, kw_only=True)
    follow_redirects: bool = attr.ib(False, kw_only=True)

    @property
    def ontology(self) -> str:
        return self.headers["x-ontology"]

    @ontology.setter
    def ontology(self, value) -> None:
        self.headers["x-ontology"] = value

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in all endpoints"""
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        return attr.evolve(self, timeout=timeout)

    def execute(self, callable_fn: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute an OS API call passing the client as ourselves."""
        return callable_fn(*args, **{**kwargs, "client": self})

    def get_base_url_v1(self):
        return self.base_url.rstrip("/")


def fetch_token_from_file() -> Union[str, None]:
    token_file = Path(OS_JWT_SECRET_PATH)
    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        try:
            if token_file.is_file():
                return token_file.read_text().strip()
            else:
                print(f"{OS_JWT_SECRET_PATH} not found. Retrying...")
        except (OSError, UnicodeDecodeError) as e:
            print(f"Error reading {OS_JWT_SECRET_PATH}: {e}. Retrying...")

        time.sleep(1)
        attempts += 1

    print("Maximum number of attempts reached. Giving up.")
    return None


def is_valid_jwt(token: str) -> bool:
    try:
        header, payload, signature = token.split(".")
        decoded_payload = base64.urlsafe_b64decode(payload + "==").decode("utf-8")
        payload_data = json.loads(decoded_payload)
        if "exp" in payload_data and payload_data["exp"] > time.time():
            return True
        return False
    except (ValueError, json.JSONDecodeError, KeyError):
        return False


@attr.s(auto_attribs=True)
class AuthenticatedClient(Client):
    """A Client which has been authenticated for use on secured endpoints"""

    fixed_token: str = None
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"

    @property
    def token(self) -> str:
        if self.fixed_token:
            return self.fixed_token

        token = fetch_token_from_file()
        if token and is_valid_jwt(token):
            os.environ["OS_JWT"] = (
                f"DEPRECATED: use '{OS_JWT_SECRET_PATH}' instead of the environment variable"
            )
            return token

        print("WARNING: no valid secret found for OS_JWT!")

        token = os.environ.get("OS_JWT")
        if token and is_valid_jwt(token):
            print(
                "WARNING: Using OS_JWT from environment variable: use this for developer mode only!"
            )
            self.fixed_token = token
            return token

        raise RuntimeError("OS_JWT not found")

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in authenticated endpoints"""
        auth_header_value = f"{self.prefix} {self.token}" if self.prefix else self.token
        return {self.auth_header_name: auth_header_value, **self.headers}


class User(object):
    """A User with an associated Client"""

    def __init__(self, client):
        self.client = client

    def decode_jwt(self):
        # algorithms is inert while verify_signature is off, but the platform
        # signs secp256k1 keys as ES256K (RFC 8812) since TEAM-7013 — do not
        # leave a stale ES256-only list for whoever turns verification on.
        return jwt.decode(
            self.client.token,
            algorithms=["ES256", "ES256K"],
            options={"verify_signature": False},
        )

    @property
    def username(self):
        return self.decode_jwt()["username"]

    @property
    def email(self):
        return self.decode_jwt()["email"]

    @property
    def roles(self):
        return self.decode_jwt()["roles"]

    @property
    def jwt(self):
        return self.client.token

    @property
    def ontology(self):
        return self.client.ontology

    @property
    def jwt_issuer(self):
        return self.decode_jwt()["iss"]

    @property
    def jwt_issued_at(self):
        return self.decode_jwt()["iat"]

    @property
    def jwt_expires_at(self):
        return self.decode_jwt()["exp"]

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.client.token == other.client.token

    def __hash__(self):
        return int(hashlib.md5(self.client.token.encode("utf-8")).hexdigest(), 16)


class UserContext:
    def __init__(self, user: User):
        self.user = user

    def __enter__(self):
        return self.user.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def check_required_env_vars(required_vars: List[str]):
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}. Please set these variables and try again."
        )


def make_client(
    fixed_jwt=None,
    api_endpoint=None,
    ontology_name=None,
    timeout=90,
    follow_redirects=True,
) -> AuthenticatedClient:
    local_vars = []
    if ontology_name:
        local_vars.append("OS_ONTOLOGY")
    if api_endpoint:
        local_vars.append("OS_API_ENDPOINT")

    required_env_vars = list(set(REQUIRED_ENV_VARS).difference(set(local_vars)))
    check_required_env_vars(required_env_vars)

    if not ontology_name:
        ontology_name = os.environ["OS_ONTOLOGY"]
    if not api_endpoint:
        api_endpoint = os.environ["OS_API_ENDPOINT"]

    ancestor = os.environ.get("OS_ANCESTOR")
    current_pod_name = os.environ.get("OS_CURRENT_POD_NAME")
    if not ancestor and current_pod_name:
        ancestor = current_pod_name[:-6]
    if not ancestor:
        ancestor = "local-dev"
    app_name = os.environ.get("OS_APP_NAME", "unknown-local-app")

    return AuthenticatedClient(
        fixed_token=fixed_jwt,
        timeout=timeout,
        base_url=api_endpoint,
        headers={
            "x-ontology": ontology_name,
            "x-app-name": app_name,
            "x-ancestor": ancestor,
        },
        follow_redirects=follow_redirects,
        verify_ssl=True,
        raise_on_unexpected_status=False,
    )


def as_launching_user():
    launching_user = User(make_client())
    return UserContext(launching_user)


def as_developer_user(fixed_jwt=None, api_endpoint=None, ontology_name=None, **kwargs):
    warn("A developer user has been instantiated!", Warning, stacklevel=2)
    developer_user = User(make_client(fixed_jwt, api_endpoint, ontology_name, **kwargs))
    return UserContext(developer_user)


def impersonating_launching_user(**client_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client = as_launching_user(**client_kwargs).user.client
            kwargs["client"] = client
            return func(*args, **kwargs)

        return wrapper

    return decorator


def impersonating_developer_user(**client_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client = as_developer_user(**client_kwargs).user.client
            kwargs["client"] = client
            return func(*args, **kwargs)

        return wrapper

    return decorator


def dev_mode(dev_flag, **kwargs):
    def decorator(func):
        if f"{dev_flag}".lower() == "true":
            return impersonating_developer_user(**kwargs)(func)
        else:
            return func

    return decorator


custom_default_client = None

client_missing_msg = """This function is deprecated and will be removed soon.
Please create a client instead using octostar.client.make_client() and run the function via client.execute()."""


def set_default_client(client):
    global custom_default_client
    warn(client_missing_msg, FutureWarning, stacklevel=2)
    custom_default_client = client


def get_default_client():
    global custom_default_client
    warn(client_missing_msg, FutureWarning, stacklevel=2)
    if not custom_default_client:
        custom_default_client = make_client()
    return custom_default_client


def _is_jwt_expired_or_expiring_soon(jwt_token, buffer_seconds=300):
    """Check if JWT is expired or expiring within buffer_seconds (default 5 minutes)"""
    try:
        # Decode without verification to check expiration
        decoded = jwt.decode(jwt_token, options={"verify_signature": False})
        exp = decoded.get("exp")
        if not exp:
            logger.debug("JWT has no expiration claim, treating as expired")
            return True  # No expiration claim, treat as expired

        current_time = int(time.time())
        expires_in = exp - current_time
        is_expired = current_time >= (exp - buffer_seconds)

        logger.debug(
            f"JWT expires in {expires_in}s, buffer={buffer_seconds}s, is_expired={is_expired}"
        )
        return is_expired
    except Exception as e:
        logger.debug(f"Failed to decode JWT: {e}, treating as expired")
        return True  # If we can't decode, treat as expired


def _should_refresh_user(is_first_time, force_refresh, jwt_expired, prev_user_exists):
    """Determine if user/JWT should be refreshed"""
    if is_first_time:
        logger.debug("Refreshing user: first time")
        return True
    if force_refresh:
        logger.debug("Refreshing user: force_refresh=True")
        return True
    if jwt_expired:
        logger.debug("Refreshing user: JWT expired")
        return True
    if not prev_user_exists:
        logger.debug("Refreshing user: no previous user cached")
        return True

    logger.debug("Not refreshing user: using cached user")
    return False


def impersonating_running_user(**client_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client = as_running_user(**client_kwargs).user.client
            kwargs["client"] = client
            return func(*args, **kwargs)

        return wrapper

    return decorator


def as_running_user(force_refresh=False):
    try:
        from octostar_streamlit.desktop import Whoami
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx
    except ImportError as e:
        raise RuntimeError(
            "Running user integration requires the 'streamlit' extra. "
            "Install with `pip install octostar-python-client[streamlit]`."
        ) from e

    script_ctx = get_script_run_ctx()
    internal_st_key = "__run_user"
    if internal_st_key not in st.session_state:
        st.session_state[internal_st_key] = dict()
    prev_run = st.session_state[internal_st_key].get("prev_run")
    prev_user = st.session_state[internal_st_key].get("prev_user")
    prev_jwt = st.session_state[internal_st_key].get("prev_jwt")
    is_first_time = False
    if prev_run is not script_ctx.script_requests:  # this changes at every st rerun
        is_first_time = True
    st.session_state[internal_st_key]["prev_run"] = script_ctx.script_requests

    logger.debug(
        f"as_running_user called: force_refresh={force_refresh}, is_first_time={is_first_time}, has_prev_user={bool(prev_user)}, has_prev_jwt={bool(prev_jwt)}"
    )

    # Check if JWT is expired or expiring soon
    jwt_expired = prev_jwt and _is_jwt_expired_or_expiring_soon(prev_jwt)

    # Determine if we should refresh
    should_refresh = _should_refresh_user(
        is_first_time, force_refresh, jwt_expired, bool(prev_user)
    )

    if not should_refresh:
        logger.debug("Returning cached user")
        return UserContext(prev_user)

    logger.debug("Fetching new user from Whoami()")
    running_user = Whoami()
    running_user_jwt = running_user.os_jwt
    if not running_user:
        if prev_user and not jwt_expired:
            logger.debug("Whoami() failed but using cached user (JWT not expired)")
            return UserContext(prev_user)
        else:
            logger.debug("Whoami() failed and no valid cached user, stopping")
            st.stop()

    running_user_hash = int(
        hashlib.md5(running_user_jwt.encode("utf-8")).hexdigest(), 16
    )
    if not prev_user or hash(prev_user) != running_user_hash or jwt_expired:
        logger.debug("Creating new client and user")
        client = make_client(fixed_jwt=running_user_jwt)
        user = User(client)
        st.session_state[internal_st_key]["prev_user"] = user
        st.session_state[internal_st_key]["prev_jwt"] = running_user_jwt

    logger.debug("Returning user context")
    return UserContext(user)
