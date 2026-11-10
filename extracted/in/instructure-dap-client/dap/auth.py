import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Any, Dict, Optional

import aiohttp
import jwt
from strong_typing.serialization import json_to_object

from .dap_error import DAPClientError, OAuthTokenError, TableAccessNotGrantedError
from .dap_types import Credentials, TokenProperties
from .http_json import read_json_body

logger = logging.getLogger("dap")

# the "type" the token issuer's authorization_details entries use
# to grant table-level access
DAP_AUTHORIZATION_DETAILS_TYPE = "dap"


@dataclass(frozen=True)
class TableAccess:
    """
    Identifies the table access a JWT was requested for. Either both `namespace`
    and `table` are set (access to a specific table), or neither is (no access
    to any table — only table-unrelated operations like listing tables or
    namespaces) — a namespace without a table is not a valid combination.

    :param namespace: A namespace identifier such as `canvas` or `mastery`, or None if the
        request carries no table access (table-unrelated operations only).
    :param table: A table identifier such as `submissions`, `quizzes`, or `users`, or None if
        the request carries no table access (table-unrelated operations only).
    """

    namespace: Optional[str]
    table: Optional[str]

    def __post_init__(self) -> None:
        if self.namespace is not None and self.table is None:
            raise DAPClientError(
                "TableAccess with a namespace requires a table; "
                "a namespace without a table is not a valid access level."
            )

    def __str__(self) -> str:
        if self.namespace is None:
            return "(none)"
        return f"{self.namespace}/{self.table}"


class AccessToken:
    """
    A JWT access token. This object is immutable.

    The access token counts as sensitive information not to be exposed (e.g. in logs).
    """

    _token: str
    _expiry: datetime

    def __init__(self, jwt_token: str) -> None:
        "Creates a new JWT access token."

        self._token = jwt_token
        decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False})
        expiry = int(decoded_jwt["exp"])
        self._expiry = datetime.fromtimestamp(expiry, tz=timezone.utc)

    def __str__(self) -> str:
        "Returns the string representation of the JWT access token."

        return self._token

    def is_expiring(self) -> bool:
        """
        Checks if the token is about to expire.

        :returns: True if the token is about to expire.
        """

        latest_accepted_expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        return self._expiry < latest_accepted_expiry


class Authenticator:
    """
    Obtains and caches table-restricted JWT access tokens from the DAP token
    issuer.

    `authenticate()` returns the token rather than installing it anywhere, so
    the caller decides which requests carry it. The `aiohttp` connection pool
    passed in is used only to reach the token endpoint, which is on the same
    host as the API.

    One token is cached at a time, together with the table access it was
    issued for. Requesting a different access level replaces it, which is how
    a caller pins an access level for a sequence of subsequent requests.
    """

    _base_url: str
    _http: aiohttp.ClientSession
    _credentials: Credentials
    _headers: Dict[str, str]
    _access_token: Optional[AccessToken]
    _last_table_access: Optional[TableAccess]

    def __init__(
        self,
        base_url: str,
        http: aiohttp.ClientSession,
        credentials: Credentials,
        headers: Dict[str, str],
    ) -> None:
        self._base_url = base_url
        self._http = http
        self._credentials = credentials
        self._headers = headers
        self._access_token = None
        self._last_table_access = None

    async def authenticate(
        self, table_access: Optional[TableAccess] = None
    ) -> AccessToken:
        """
        Authenticates with API key to receive a table-restricted JWT, and pins it
        as the current access level. Reuses the cached token as long as it is not
        expiring and was requested for this same access level.

        :param table_access: The table the requested JWT should be restricted to.
            Omit to reuse the most recently used access level if one exists,
            otherwise a token with no table access is requested (e.g. on first use).
        :returns: The access token to send as the bearer token.
        """

        if table_access is None:
            # no access level requested: reuse whatever's cached, restricted or not
            table_access = self._last_table_access or TableAccess(
                namespace=None, table=None
            )

        if (
            self._access_token is not None
            and not self._access_token.is_expiring()
            and (self._last_table_access == table_access or table_access.table is None)
        ):
            return self._access_token

        logger.debug(f"Authenticating to DAP for table access '{table_access}'")

        # discard the stale token (expired, or restricted to a different table)
        # before requesting a new one, so a failed request cannot leave the old
        # one in place
        self._access_token = None
        self._last_table_access = None

        properties = await self._post_auth_request(
            self._credentials.basic_credentials, table_access
        )
        if table_access.namespace is not None and table_access.table is not None:
            self._verify_granted_table_access(
                table_access.namespace,
                table_access.table,
                properties.authorization_details,
            )
        access_token = AccessToken(properties.access_token)
        self._access_token = access_token
        self._last_table_access = table_access
        return access_token

    async def _post_auth_request(
        self, basic_credentials: str, table_access: TableAccess
    ) -> TokenProperties:
        """
        Requests a JWT from the token issuer, restricted to a single table, or
        carrying no table access (table-unrelated operations only), depending on
        `table_access`.

        :param basic_credentials: Basic credentials.
        :param table_access: The table access the requested JWT should be restricted to.
        :returns: An access token and metadata.
        :raises Exception: The object returned on failure.
        """

        data = {"grant_type": "client_credentials", "scope": "dap"}
        if table_access.namespace is not None:
            authorization_details = [
                {
                    "type": DAP_AUTHORIZATION_DETAILS_TYPE,
                    "namespaces": {table_access.namespace: [table_access.table]},
                }
            ]
            data["authorization_details"] = json.dumps(authorization_details)

        url = f"{self._base_url}/oauth/token"
        logger.debug(f"POST request to {url}")

        async with self._http.post(
            url,
            data=data,
            headers={"Authorization": "Basic " + basic_credentials} | self._headers,
        ) as response:
            return await self._process_token_response(response)

    async def _process_token_response(
        self, response: aiohttp.ClientResponse
    ) -> TokenProperties:
        """
        Extracts token properties from an OAuth2 token endpoint response body.
        On failure, the token issuer reports errors in the OAuth2 shape
        ({"error": "<code>", "error_description": "<message>"}), unlike the DAP
        API's own {"error": {"type", "uuid", "message"}} shape used elsewhere.
        """

        try:
            response_payload = await read_json_body(response)
        except DAPClientError as e:
            raise DAPClientError(
                f"Authentication request to {response.url} failed: {e} "
                "Check the API base URL and the client ID and secret."
            ) from e

        # HTTP status codes between 400 (inclusive) and 600 (exclusive) indicate an error
        # (includes non-standard 5xx server-side error codes)
        if HTTPStatus.BAD_REQUEST.value <= response.status < 600:
            # per RFC 6749 SS5.2, "error" is required but "error_description" is optional
            error_code = response_payload.get("error", "authentication_failed")
            if not isinstance(error_code, str):
                error_code = str(error_code)
            error_description = response_payload.get("error_description")
            if error_description is not None and not isinstance(error_description, str):
                error_description = str(error_description)
            error_object = OAuthTokenError(
                error=error_code,
                error_description=error_description,
            )
            logger.warning(f"Received error in response: {error_object}")
            raise error_object
        else:
            return json_to_object(TokenProperties, response_payload)

    def _verify_granted_table_access(
        self,
        namespace: str,
        table: str,
        granted_authorization_details: Any,
    ) -> None:
        """
        Verifies that the token issuer's `authorization_details` actually grants
        the requested table access, rather than trusting the issued token blindly.

        :param namespace: The requested namespace.
        :param table: The requested table.
        :raises TableAccessNotGrantedError: The granted access does not contain
            the requested namespace/table.
        """

        if isinstance(granted_authorization_details, list):
            for entry in granted_authorization_details:
                if (
                    not isinstance(entry, dict)
                    or entry.get("type") != DAP_AUTHORIZATION_DETAILS_TYPE
                ):
                    continue
                namespaces = entry.get("namespaces")
                if not isinstance(namespaces, dict):
                    continue
                granted_tables = namespaces.get(namespace)
                if isinstance(granted_tables, list) and table in granted_tables:
                    return

        logger.debug(
            f"Token issuer did not grant access to '{namespace}/{table}'; "
            f"granted authorization_details: {granted_authorization_details!r}"
        )
        raise TableAccessNotGrantedError(requested=f"{namespace}/{table}")
