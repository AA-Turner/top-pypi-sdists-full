import logging

from tecton_core import errors


logger = logging.getLogger(__name__)


class SnowflakeContext:
    """
    Get access to Snowflake connection and session.
    """

    _current_context_instance = None
    _session = None
    _connection = None

    def __init__(self, connection):
        self._connection = connection
        from snowflake.snowpark import Session

        connection_parameters = {
            "connection": connection,
        }
        self._session = Session.builder.configs(connection_parameters).create()

    def get_session(self):
        if self._session is None:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET
        return self._session

    def get_connection(self):
        if self._connection is None:
            raise errors.SNOWFLAKE_CONNECTION_NOT_SET
        return self._connection

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
    def set_connection(cls, connection) -> "SnowflakeContext":  # noqa: ANN001
        logger.debug("Generating new Snowflake session")
        # validate snowflake connection
        if not connection.database:
            msg = "database"
            raise errors.MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)
        if not connection.warehouse:
            msg = "warehouse"
            raise errors.MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)
        if not connection.schema:
            msg = "schema"
            raise errors.MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS(msg)

        cls._current_context_instance = cls(connection)
        return cls._current_context_instance
