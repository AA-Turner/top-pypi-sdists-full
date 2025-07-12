import logging
from typing import Any
from typing import Dict
from typing import Optional

from tecton_core import errors


logger = logging.getLogger(__name__)


def decrypt_private_key(private_key_str: str, private_key_passphrase: Optional[str] = None) -> bytes:
    try:
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
    except ImportError as e:
        msg = "cryptography package is required for private key decryption. Install tecton with snowflake support: pip install 'tecton[snowflake]'"
        raise ImportError(msg) from e

    passphrase_bytes = private_key_passphrase.encode("utf-8") if private_key_passphrase else None
    p_key = serialization.load_pem_private_key(
        private_key_str.encode("utf-8"), password=passphrase_bytes, backend=default_backend()
    )

    return p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


class SnowflakeContext:
    """
    Get access to Snowflake connection and session.
    """

    _current_context_instance = None
    _session = None
    _params = None

    def __init__(self, connection_params):
        self._params = connection_params
        from snowflake.snowpark import Session

        self._session = Session.builder.configs(connection_params).create()

    def get_session(self):
        if self._session is None:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET
        return self._session

    def get_connection_params(self):
        if self._params is None:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET
        return self._params

    def get_connection(self):
        import snowflake.connector

        if self._params is None:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET

        return snowflake.connector.connect(**self._params)

    @classmethod
    def is_initialized(cls):
        return cls._current_context_instance is not None

    @classmethod
    def get_instance(cls) -> "SnowflakeContext":
        """
        Get the singleton instance of SnowflakeContext.
        """
        # If the instance doesn't exist, raise the error to instruct user to set connection first. Otherwise
        # return the current snowflake context.
        if cls._current_context_instance is not None:
            return cls._current_context_instance
        else:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET

    @classmethod
    def set_connection_params(cls, params: Dict[str, Any]) -> "SnowflakeContext":
        logger.debug("Generating new Snowflake session")
        # validate snowflake connection
        if not isinstance(params, dict):
            msg = "Connection params must be a dict"
            raise TypeError(msg)

        if not params.get("database"):
            msg = "database"
            raise errors.MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)
        if not params.get("warehouse"):
            msg = "warehouse"
            raise errors.MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)
        if not params.get("schema"):
            msg = "schema"
            raise errors.MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)

        if params.get("private_key"):
            private_key = params["private_key"]
            # Only decrypt if it's still a string. If setting the config from the query_tree_executor,
            # it will have already been decrypted because we do get and then set.
            if isinstance(private_key, str):
                params["private_key"] = decrypt_private_key(private_key, params.get("private_key_passphrase"))

        cls._current_context_instance = cls(params)
        return cls._current_context_instance
