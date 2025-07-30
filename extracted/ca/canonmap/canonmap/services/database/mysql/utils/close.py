import logging
from typing import TYPE_CHECKING

import mysql.connector

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from mysql.connector import MySQLConnection

def _close_util(connection: "MySQLConnection") -> None:
    """Close a MySQL connection with proper error handling and logging.
    
    Args:
        connection: The MySQL connection to close
        
    Note:
        This method will log any errors that occur during connection closure
        but will not re-raise them to avoid masking other errors.
    """
    if connection is None:
        logger.debug("Attempted to close None connection - ignoring")
        return
        
    try:
        if connection.is_connected():
            logger.debug("Closing MySQL connection")
            connection.close()
            logger.info("MySQL connection closed successfully")
        else:
            logger.debug("MySQL connection was already closed")
    except mysql.connector.Error as e:
        logger.warning(f"Error occurred while closing MySQL connection: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error while closing MySQL connection: {e}")

