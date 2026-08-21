"""
Generic Iceberg REST Catalog (IRC) Connection Wrapper Implementation.
"""

import time
from typing import Any, Dict, Optional

from botocore.exceptions import ClientError

from ...constants import ConnectionObjectKey
from .native_wrapper import NativeConnectionWrapper


class IcebergRestCatalogConnectionWrapper(NativeConnectionWrapper):
    """
    Generic Iceberg REST catalog connection wrapper.

    Serves every IRC connection type whose OAuth2 token acquisition can be delegated to
    Glue, which currently covers Databricks Unity Catalog, Snowflake Horizon and the
    vendor-neutral ICEBERGRESTCATALOG type.

    Rather than performing the OAuth2 exchange in this library, this wrapper calls Glue's
    RefreshOAuth2Tokens API. Glue performs the exchange server side using the
    AuthenticationConfiguration already stored on the connection and persists the
    resulting tokens to the connection's Secrets Manager secret. The access token is then
    read back from that secret under the ACCESS_TOKEN key, which is the same convention
    the rest of this library already uses for OAuth2 connections (see
    utils.secret_key_update_helper.add_oauth2_token_keys).

    The refresh is lazy: the token already stored on the secret is used when present,
    and Glue is only called when the secret holds no token or the caller forces a
    refresh through the forceTokenRefresh additional option. Expired stored tokens are
    recovered by the query layer, which retries with a forced refresh when the catalog
    rejects a request as unauthorized.

    Keeping the exchange server side means no per-vendor token endpoint, grant type,
    scope or client secret handling is needed here, so a single implementation serves all
    supported IRC vendors.
    """

    ACCESS_TOKEN_KEY = "ACCESS_TOKEN"
    BEARER_TOKEN_KEY = "BEARER_TOKEN"
    OAUTH2_AUTHENTICATION_TYPE = "OAUTH2"
    REQUIRED_CONNECTION_PROPERTIES = ("INSTANCE_URL", "SOURCE_CATALOG_LIST")
    # additional_options key callers set to force a token refresh (e.g. after the
    # catalog rejected the stored token with a 401).
    FORCE_TOKEN_REFRESH_OPTION = "forceTokenRefresh"
    # Secrets Manager reads are eventually consistent, so a read immediately after
    # RefreshOAuth2Tokens persists new tokens may briefly return the previous value.
    # Poll for the updated value for at most REFRESH_READ_ATTEMPTS * REFRESH_READ_DELAY_SECONDS.
    REFRESH_READ_ATTEMPTS = 4
    REFRESH_READ_DELAY_SECONDS = 0.5

    def get_catalog_configs(self) -> Dict[str, Any]:
        """
        Get the connection's Iceberg REST catalog options with a freshly resolved token.

        Returns:
            The connection properties plus a resolved ACCESS_TOKEN entry.

        Raises:
            ValueError: If required connection properties, the secret, or the Glue client
                needed to refresh OAuth2 tokens are missing.
        """
        connection_properties = self._connection.get(ConnectionObjectKey.CONNECTION_PROPERTIES, {})
        options: Dict[str, Any] = dict(connection_properties)

        missing_properties = [
            connection_property
            for connection_property in self.REQUIRED_CONNECTION_PROPERTIES
            if not options.get(connection_property)
        ]
        if missing_properties:
            raise ValueError(
                "Missing required Iceberg REST catalog connection "
                f"{'properties' if len(missing_properties) > 1 else 'property'}: "
                f"{', '.join(missing_properties)}"
            )

        options[self.ACCESS_TOKEN_KEY] = self._resolve_access_token()

        return options

    def _resolve_access_token(self) -> str:
        """
        Resolve the access token for the connection, refreshing lazily for OAuth2.

        The token stored on the connection's secret is used as-is when present, so
        building catalog configs does not pay a token exchange round trip per call.
        Glue's RefreshOAuth2Tokens API is only invoked when the secret holds no token
        yet, or when the caller explicitly requests a refresh via the
        forceTokenRefresh additional option (set by the query layer after the catalog
        rejects the stored token).

        Returns:
            The access token stored on the connection's secret.
        """
        auth_config = self._connection.get(ConnectionObjectKey.AUTHENTICATION_CONFIGURATION, {})

        secret_arn = auth_config.get("SecretArn")
        if not secret_arn:
            raise ValueError(
                "AuthenticationConfiguration.SecretArn is required to resolve the access token "
                "for an Iceberg REST catalog connection"
            )

        access_token = self._read_token_from_secret(secret_arn)

        # Non-OAuth2 connections carry a long lived token in the secret, so there is
        # nothing for Glue to refresh.
        authentication_type = (auth_config.get("AuthenticationType") or "").upper()
        force_refresh = (
            str(self._additional_options.get(self.FORCE_TOKEN_REFRESH_OPTION, "")).lower() == "true"
        )
        if authentication_type == self.OAUTH2_AUTHENTICATION_TYPE and (
            not access_token or force_refresh
        ):
            self._refresh_oauth2_tokens()
            access_token = self._read_token_after_refresh(secret_arn, access_token)

        if not access_token:
            raise ValueError(
                "Secret referenced by the connection does not contain a non-empty "
                f"'{self.ACCESS_TOKEN_KEY}' or '{self.BEARER_TOKEN_KEY}' entry"
            )

        return access_token

    def _read_token_from_secret(self, secret_arn: str) -> Optional[str]:
        """
        Read the access token from the connection's secret.

        OAuth2 tokens are persisted under ACCESS_TOKEN. CUSTOM authentication stores a
        statically issued token under BEARER_TOKEN, per the connection type templates.
        """
        secret_options = self._get_secret_options_from_secret_manager(secret_arn)
        return secret_options.get(self.ACCESS_TOKEN_KEY) or secret_options.get(
            self.BEARER_TOKEN_KEY
        )

    def _read_token_after_refresh(
        self, secret_arn: str, previous_token: Optional[str]
    ) -> Optional[str]:
        """
        Read the refreshed token, tolerating Secrets Manager's eventual consistency.

        A read immediately after the refresh persists new tokens may briefly return
        the previous secret value (or, for a brand-new connection, no token at all),
        so re-read until a changed, non-empty token appears or the retry budget is
        exhausted. The last read value is returned either way: when the stale value
        comes back it is the previously issued token, which typically remains valid
        until its natural expiry, and the query layer's retry-on-401 path forces
        another refresh if it does not.
        """
        access_token = self._read_token_from_secret(secret_arn)
        attempts = 1
        while (
            not access_token or access_token == previous_token
        ) and attempts < self.REFRESH_READ_ATTEMPTS:
            time.sleep(self.REFRESH_READ_DELAY_SECONDS)
            access_token = self._read_token_from_secret(secret_arn)
            attempts += 1
        return access_token

    def _refresh_oauth2_tokens(self) -> None:
        """
        Ask Glue to refresh the OAuth2 tokens persisted on the connection's secret.

        Raises:
            ValueError: If the Glue client or the connection name is unavailable.
        """
        if self._glue_client is None:
            raise ValueError(
                "A Glue client is required to refresh OAuth2 tokens for an Iceberg REST "
                "catalog connection. Provide glue_client in GlueConnectionWrapperInputs."
            )

        connection_name = self._connection.get(ConnectionObjectKey.NAME)
        if not connection_name:
            raise ValueError("Connection 'Name' is required to refresh OAuth2 tokens")

        self.log.debug("Refreshing OAuth2 tokens for connection %s", connection_name)
        # Note: RefreshOAuth2Tokens returns an empty response; the refreshed tokens are
        # persisted to the connection's secret, which is read by the caller afterwards.
        try:
            self._glue_client.refresh_o_auth2_tokens(  # type: ignore[attr-defined]
                ConnectionName=connection_name
            )
        except ClientError as error:
            # Glue holds a per-connection refresh lock and raises ConflictException when
            # a refresh is already in flight. That refresh persists fresh tokens to the
            # same secret, so proceed to the secret read instead of failing the caller.
            if error.response.get("Error", {}).get("Code") != "ConflictException":
                raise
            self.log.info(
                "OAuth2 token refresh already in progress for connection %s; "
                "proceeding with the token stored on the connection's secret",
                connection_name,
            )
