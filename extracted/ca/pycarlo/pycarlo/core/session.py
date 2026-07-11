import configparser
import os
import time
import uuid
from dataclasses import InitVar, dataclass, field
from importlib.metadata import version as get_version
from threading import Lock
from typing import Optional, Tuple

import requests

from pycarlo.common import get_logger
from pycarlo.common.errors import InvalidConfigFileError, InvalidSessionError
from pycarlo.common.retries import ExponentialBackoffJitter, retry_with_backoff
from pycarlo.common.settings import (
    API_OAUTH_SCOPE,
    DEFAULT_CONFIG_PATH,
    DEFAULT_MCD_API_ENDPOINT,
    DEFAULT_MCD_API_ENDPOINT_CONFIG_KEY,
    DEFAULT_MCD_API_ID_CONFIG_KEY,
    DEFAULT_MCD_API_TOKEN_CONFIG_KEY,
    DEFAULT_MCD_IGW_ENDPOINT,
    DEFAULT_MCD_INSTANCE_ID_CONFIG_KEY,
    DEFAULT_MCD_OAUTH_API_ENDPOINT_CONFIG_KEY,
    DEFAULT_MCD_OAUTH_CLIENT_ID_CONFIG_KEY,
    DEFAULT_MCD_OAUTH_CLIENT_SECRET_CONFIG_KEY,
    DEFAULT_MCD_TOKEN_ENDPOINT_CONFIG_KEY,
    DEFAULT_PACKAGE_NAME,
    DEFAULT_PROFILE_NAME,
    DEFAULT_RETRY_INITIAL_WAIT_TIME,
    DEFAULT_RETRY_MAX_WAIT_TIME,
    MCD_API_ENDPOINT,
    MCD_DEFAULT_API_ID,
    MCD_DEFAULT_API_TOKEN,
    MCD_DEFAULT_INSTANCE_ID,
    MCD_DEFAULT_OAUTH_CLIENT_ID,
    MCD_DEFAULT_OAUTH_CLIENT_SECRET,
    MCD_DEFAULT_PROFILE,
    MCD_OAUTH_API_ENDPOINT,
    MCD_TOKEN_ENDPOINT,
    MCD_USER_ID_HEADER,
    PROFILE_FILE_NAME,
    derive_instance_scope,
    derive_token_endpoint,
    validate_instance_id,
)

logger = get_logger(__name__)

# Refresh an OAuth access token this many seconds before its stated expiry, to avoid using a token
# that expires mid-flight.
_TOKEN_EXPIRY_SKEW_SECS = 60
# Timeout for the client-credentials token request.
_TOKEN_REQUEST_TIMEOUT_SECS = 10


def _should_retry_token_request(exc: Exception) -> bool:
    """Retry transient token-endpoint failures — connection errors, timeouts, and 5xx — but not
    4xx (bad credentials / request), which won't succeed on retry."""
    if isinstance(exc, requests.exceptions.HTTPError):
        return exc.response is not None and exc.response.status_code >= 500
    return True


@dataclass
class Session:
    """
    Creates an MC access session.

    Auth resolution hierarchy -
    1. Passing credentials (mcd_id & mcd_token, or mcd_oauth_client_id & mcd_oauth_client_secret)
    2. Environment variables (MCD_DEFAULT_API_ID/TOKEN or MCD_DEFAULT_OAUTH_CLIENT_ID/SECRET)
    3. Config-file by passing profile name (mcd_profile)
    4. Config-file by setting the profile as an environment variable (MCD_DEFAULT_PROFILE)
    5. Config-file by default profile name (default)

    If both API-key (mcd_id/mcd_token) and OAuth (client id/secret) credentials are provided, OAuth
    is used.

    Environment vars can be mixed with passed credentials, but not the config-file profile.

    If necessary the MC API url can be overridden by specifying an endpoint. OAuth defaults to the
    global gateway: the token endpoint is derived from the API endpoint (``/graphql`` ->
    ``/oauth2/token``) and the OAuth API endpoint is the API endpoint unchanged (the gateway routes
    a bearer-token ``/graphql`` request to the OAuth backend). Both can be overridden (e.g. to reach
    an instance directly, bypassing the gateway).

    For OAuth, ``mcd_instance_id`` (e.g. ``us1``, ``eu1``) is required: it selects the
    instance-routing scope requested at token time so the gateway routes to the right instance.

    The config-file path can be set via mcd_config_path.

    An optional scope can be set to configure the Session to use the Integration Gateway REST API
    instead of the GraphQL API (OAuth is not supported for the gateway REST API).
    """

    mcd_id: InitVar[Optional[str]] = None
    mcd_token: InitVar[Optional[str]] = None
    mcd_oauth_client_id: InitVar[Optional[str]] = None
    mcd_oauth_client_secret: InitVar[Optional[str]] = None
    mcd_profile: InitVar[Optional[str]] = None
    mcd_config_path: InitVar[str] = DEFAULT_CONFIG_PATH
    token_endpoint: InitVar[Optional[str]] = None
    oauth_api_endpoint: InitVar[Optional[str]] = None
    mcd_instance_id: InitVar[Optional[str]] = None

    id: str = field(init=False)
    token: str = field(init=False)
    session_name: str = field(init=False)
    endpoint: str = DEFAULT_MCD_API_ENDPOINT
    user_id: Optional[str] = MCD_USER_ID_HEADER
    scope: Optional[str] = None

    is_oauth: bool = field(init=False, default=False)
    oauth_token_endpoint: Optional[str] = field(init=False, default=None)
    # Instance-routing scope requested at token time (None -> gateway's default instance).
    oauth_instance_scope: Optional[str] = field(init=False, default=None)
    _oauth_client_id: Optional[str] = field(init=False, default=None, repr=False)
    _oauth_client_secret: Optional[str] = field(init=False, default=None, repr=False)
    _access_token: Optional[str] = field(init=False, default=None, repr=False)
    _token_expiry: float = field(init=False, default=0.0, repr=False)
    _token_lock: Lock = field(init=False, default_factory=Lock, repr=False)
    # Explicit values captured from the profile (used when deriving OAuth settings).
    _profile_token_endpoint: Optional[str] = field(init=False, default=None, repr=False)
    _profile_oauth_api_endpoint: Optional[str] = field(init=False, default=None, repr=False)
    _profile_instance_id: Optional[str] = field(init=False, default=None, repr=False)

    def __post_init__(
        self,
        mcd_id: Optional[str],
        mcd_token: Optional[str],
        mcd_oauth_client_id: Optional[str],
        mcd_oauth_client_secret: Optional[str],
        mcd_profile: Optional[str],
        mcd_config_path: str,
        token_endpoint: Optional[str],
        oauth_api_endpoint: Optional[str],
        mcd_instance_id: Optional[str],
    ):
        version = get_version(DEFAULT_PACKAGE_NAME)
        self.session_name = f"python-sdk-{version}-{uuid.uuid4()}"
        logger.info(f"Creating named session as '{self.session_name}'.")

        mcd_id = mcd_id or MCD_DEFAULT_API_ID
        mcd_token = mcd_token or MCD_DEFAULT_API_TOKEN
        oauth_id = mcd_oauth_client_id or MCD_DEFAULT_OAUTH_CLIENT_ID
        oauth_secret = mcd_oauth_client_secret or MCD_DEFAULT_OAUTH_CLIENT_SECRET

        has_key = bool(mcd_id and mcd_token)

        if oauth_id and oauth_secret:
            if has_key:
                logger.info("Both API key and OAuth credentials provided; using OAuth credentials.")
            self._configure_oauth(oauth_id, oauth_secret)
        elif mcd_id and mcd_token:
            self.id = mcd_id
            self.token = mcd_token
        elif mcd_id or mcd_token or oauth_id or oauth_secret:
            raise InvalidSessionError("Partially setting a session is not supported.")
        else:
            self._read_config(
                mcd_profile=mcd_profile or MCD_DEFAULT_PROFILE or DEFAULT_PROFILE_NAME,
                mcd_config_path=mcd_config_path,
            )

        # Resolve the base API endpoint (env override wins; else profile/default; IGW when scoped).
        if MCD_API_ENDPOINT:
            self.endpoint = MCD_API_ENDPOINT
        elif self.scope and self.endpoint == DEFAULT_MCD_API_ENDPOINT:
            self.endpoint = DEFAULT_MCD_IGW_ENDPOINT

        if self.is_oauth:
            if self.scope:
                # OAuth targets the API endpoint; a gateway (IGW) scope flips the endpoint to the
                # IGW root, which has no /graphql to derive a token endpoint from. Fail clearly.
                raise InvalidSessionError(
                    "OAuth is not supported together with a gateway scope. Use OAuth against the "
                    "API endpoint, or use API-key auth for the gateway."
                )
            api_endpoint = self.endpoint
            self.oauth_token_endpoint = (
                token_endpoint or MCD_TOKEN_ENDPOINT or self._profile_token_endpoint
            )
            if not self.oauth_token_endpoint:
                try:
                    self.oauth_token_endpoint = derive_token_endpoint(api_endpoint)
                except ValueError as e:
                    raise InvalidSessionError(str(e)) from e
            # OAuth GraphQL calls use the API endpoint unchanged; the global gateway routes a
            # bearer-token /graphql request to the OAuth backend. Overridable for direct access.
            self.endpoint = (
                oauth_api_endpoint
                or MCD_OAUTH_API_ENDPOINT
                or self._profile_oauth_api_endpoint
                or api_endpoint
            )
            instance_id = mcd_instance_id or MCD_DEFAULT_INSTANCE_ID or self._profile_instance_id
            if not instance_id:
                raise InvalidSessionError(
                    "OAuth requires an instance id (e.g. us1). Set it via mcd_instance_id, the "
                    "MCD_DEFAULT_INSTANCE_ID env var, or the profile's 'mcd_instance_id'."
                )
            try:
                instance_id = self.validate_instance_id(instance_id)
            except ValueError as e:
                raise InvalidSessionError(str(e)) from e
            self.oauth_instance_scope = derive_instance_scope(instance_id)

        session_type = (
            "OAUTH_API" if self.is_oauth else ("GATEWAY_API" if self.scope else "APPLICATION_API")
        )
        logger.info(f"Created {session_type} session with MC API ID '{self.id}'.")

    @staticmethod
    def validate_instance_id(instance_id: str) -> str:
        """Validate and normalize a deployment instance id (e.g. ``us1``, ``eu1``).

        Returns the trimmed id, or raises ``ValueError`` if it isn't a valid identifier. Exposed so
        callers (e.g. the CLI) can validate an id at input time, before constructing a Session.
        """
        return validate_instance_id(instance_id)

    def _configure_oauth(self, client_id: str, client_secret: str) -> None:
        self.is_oauth = True
        self._oauth_client_id = client_id
        self._oauth_client_secret = client_secret
        self.id = client_id  # surfaced for logging/telemetry; not a secret
        self.token = ""

    def _read_config(self, mcd_profile: str, mcd_config_path: str) -> None:
        """
        Return configuration from section (profile name) if it exists.
        """
        config_parser = Session._get_config_parser()
        file_path = os.path.join(mcd_config_path, PROFILE_FILE_NAME)
        logger.info(
            "No provided connection details. Looking up session values from "
            f"'{mcd_profile}' in '{file_path}'."
        )

        try:
            config_parser.read(file_path)
            if not config_parser.has_section(mcd_profile):
                raise configparser.NoSectionError(mcd_profile)

            oauth_id = config_parser.get(
                mcd_profile, DEFAULT_MCD_OAUTH_CLIENT_ID_CONFIG_KEY, fallback=None
            )
            oauth_secret = config_parser.get(
                mcd_profile, DEFAULT_MCD_OAUTH_CLIENT_SECRET_CONFIG_KEY, fallback=None
            )
            self.endpoint = config_parser.get(
                mcd_profile,
                DEFAULT_MCD_API_ENDPOINT_CONFIG_KEY,
                fallback=DEFAULT_MCD_API_ENDPOINT,
            )
            self._profile_token_endpoint = config_parser.get(
                mcd_profile, DEFAULT_MCD_TOKEN_ENDPOINT_CONFIG_KEY, fallback=None
            )
            self._profile_oauth_api_endpoint = config_parser.get(
                mcd_profile, DEFAULT_MCD_OAUTH_API_ENDPOINT_CONFIG_KEY, fallback=None
            )
            self._profile_instance_id = config_parser.get(
                mcd_profile, DEFAULT_MCD_INSTANCE_ID_CONFIG_KEY, fallback=None
            )

            if oauth_id and oauth_secret:
                self._configure_oauth(oauth_id, oauth_secret)
            else:
                self.id = config_parser.get(mcd_profile, DEFAULT_MCD_API_ID_CONFIG_KEY)
                self.token = config_parser.get(mcd_profile, DEFAULT_MCD_API_TOKEN_CONFIG_KEY)
        except configparser.NoSectionError:
            raise InvalidSessionError(f"Profile '{mcd_profile}' not found in '{file_path}'.")
        except configparser.NoOptionError as err:
            raise InvalidSessionError(
                f"Profile '{mcd_profile}' is missing required credentials."
            ) from err
        except Exception as err:
            raise InvalidConfigFileError from err

    def get_access_token(self) -> str:
        """Return a valid OAuth access token, refreshing via client-credentials grant as needed."""
        if not self.is_oauth:
            raise InvalidSessionError("Session is not configured for OAuth.")
        with self._token_lock:
            if self._access_token and time.time() < self._token_expiry:
                return self._access_token
            self._access_token, self._token_expiry = self._request_access_token()
            return self._access_token

    def _request_access_token(self) -> Tuple[str, float]:
        logger.info(f"Requesting OAuth access token from '{self.oauth_token_endpoint}'.")
        # Request API access plus the instance-routing scope so the gateway routes both this token
        # request and later API calls to the right instance.
        scope = f"{API_OAUTH_SCOPE} {self.oauth_instance_scope}"

        @retry_with_backoff(
            backoff=ExponentialBackoffJitter(
                DEFAULT_RETRY_INITIAL_WAIT_TIME, DEFAULT_RETRY_MAX_WAIT_TIME
            ),
            exceptions=(
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
            ),
            should_retry=_should_retry_token_request,
        )
        def _post() -> requests.Response:
            resp = requests.post(
                self.oauth_token_endpoint,  # type: ignore[arg-type]
                data={"grant_type": "client_credentials", "scope": scope},
                auth=(self._oauth_client_id or "", self._oauth_client_secret or ""),
                timeout=_TOKEN_REQUEST_TIMEOUT_SECS,
            )
            resp.raise_for_status()
            return resp

        try:
            response = _post()
        except requests.exceptions.HTTPError as err:
            resp = err.response
            detail = f"(status {resp.status_code}): {resp.text}" if resp is not None else str(err)
            raise InvalidSessionError(f"Failed to obtain OAuth access token {detail}") from err
        except requests.exceptions.RequestException as err:
            raise InvalidSessionError(f"Failed to reach the OAuth token endpoint: {err}") from err

        payload = response.json()
        access_token = payload.get("access_token")
        if not access_token:
            raise InvalidSessionError("OAuth token response did not include an access_token.")
        # Tolerate a missing/non-integer expires_in — fall back to 1h rather than escaping the
        # InvalidSessionError contract with a ValueError.
        try:
            expires_in = int(payload.get("expires_in", 3600))
        except (TypeError, ValueError):
            expires_in = 3600
        expiry = time.time() + max(0, expires_in - _TOKEN_EXPIRY_SKEW_SECS)
        return access_token, expiry

    @staticmethod
    def _get_config_parser() -> configparser.ConfigParser:
        """
        Gets a configparser
        """
        return configparser.ConfigParser()
