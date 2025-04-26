import logging

from tecton._internals.sdk_decorators import sdk_public_method
from tecton_core import errors
from tecton_core.snowflake_context import SnowflakeContext


logger = logging.getLogger(__name__)


@sdk_public_method
def set_connection(connection) -> "SnowflakeContext":
    """
    Connect tecton to Snowflake.

    :param connection: The SnowflakeConnection object.
    :return: A SnowflakeContext object.
    """
    from snowflake.connector import SnowflakeConnection

    if not isinstance(connection, SnowflakeConnection):
        msg = "connection must be a SnowflakeConnection object"
        raise errors.TectonValidationError(msg)

    return SnowflakeContext.set_connection(connection)
