"""
MongoDB Connection Wrapper Implementation.
"""

import logging
from typing import Any, Dict

from ...constants import ConnectionObjectKey, SparkOptionsKey
from ...utils.jdbc_url_update_helper import JDBCUrlUpdateHelper
from .native_wrapper import NativeConnectionWrapper

logger = logging.getLogger(__name__)


class MongoDBConnectionWrapper(NativeConnectionWrapper):
    """
    MongoDB connection wrapper that extends native wrapper functionality.

    Handles MongoDB/DocumentDB specific connection processing including
    SSL validation, URL updates, and credential removal.
    """

    def get_resolved_connection(self) -> Dict[str, Any]:
        """Get connection with resolved MongoDB spark properties."""
        # Get JDBC configuration as a dictionary
        jdbc_conf = self.get_jdbc_conf()
        connection_options = jdbc_conf.as_map()

        # SSL related options validation
        if connection_options.get(SparkOptionsKey.CUSTOM_JDBC_CERT) or connection_options.get(
            SparkOptionsKey.CUSTOM_JDBC_CERT_STRING
        ):
            raise ValueError("Custom cert is not supported for spark dataframe.")

        # Remove SSL-related options
        connection_options.pop(SparkOptionsKey.CUSTOM_JDBC_CERT, None)
        connection_options.pop(SparkOptionsKey.CUSTOM_JDBC_CERT_STRING, None)
        connection_options.pop(SparkOptionsKey.SKIP_CUSTOM_JDBC_CERT_VALIDATION, None)

        # Signal IAM authentication downstream. GlueSparkConnector-MongoDB's data source
        # keys off this marker to resolve AWS credentials via the SDK default provider
        # chain and rewrite the URI to use MONGODB-AWS.
        auth_config = self._connection.get(ConnectionObjectKey.AUTHENTICATION_CONFIGURATION, {})
        auth_type = (auth_config.get("AuthenticationType") or "") if auth_config else ""
        if auth_type.upper() == "IAM":
            logger.info(
                "GLUE_CONNECTIVITY: DocumentDB/MongoDB IAM auth detected; "
                "marking options for downstream MONGODB-AWS handling."
            )
            connection_options["authenticationType"] = "IAM"
            # TLS is mandatory for IAM auth, so require it here -- at the
            # auth-decision point -- rather than trusting the caller to have set
            # enforceSSL. The connection properties this reads are customer
            # supplied and reach us from CreateConnection/UpdateConnection, so a
            # console form that sets ENFORCE_SSL=true for IAM is not an
            # enforcement point. Without this, the MONGODB-AWS SASL exchange
            # (access key id, session token, signed GetCallerIdentity payload)
            # would go out over a plaintext mongodb:// connection.
            connection_options[SparkOptionsKey.ENFORCE_SSL] = "true"

        logger.debug("updating MongoDB/DocumentDB urls.")

        # Update URL using helper
        connection_type = self._connection.get(ConnectionObjectKey.CONNECTION_TYPE, "").lower()
        full_url = connection_options.get(SparkOptionsKey.FULL_URL, "")

        options_after_url_update = JDBCUrlUpdateHelper.update_url_in_props(
            connection_type, full_url, connection_options, self._additional_options
        )

        # Remove enforceSSL
        options_after_url_update.pop(SparkOptionsKey.ENFORCE_SSL, None)

        # Combine options by removing credentials
        final_options = self._combine_options(options_after_url_update)

        # Add SparkProperties to the original connection
        self._connection[ConnectionObjectKey.SPARK_PROPERTIES] = final_options

        return self._connection

    def _combine_options(self, options_map: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove username and password from options for MongoDB connections.

        Args:
            options_map: Original options dictionary

        Returns:
            Updated options dictionary with credentials removed
        """
        # Remove credential keys
        options_map.pop("username", None)
        options_map.pop("password", None)

        return options_map
