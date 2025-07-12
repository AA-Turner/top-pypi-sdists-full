import logging
from typing import Any
from typing import Dict

from tecton._internals.sdk_decorators import sdk_public_method
from tecton_core.snowflake_context import SnowflakeContext


logger = logging.getLogger(__name__)


@sdk_public_method
def set_connection(connection_params: Dict[str, Any]) -> "SnowflakeContext":
    """
    Connect tecton to Snowflake.

    :param connection_params: Dict with connection params for snowflake connector.
    :return: A SnowflakeContext object.
    """
    return SnowflakeContext.set_connection_params(connection_params)
