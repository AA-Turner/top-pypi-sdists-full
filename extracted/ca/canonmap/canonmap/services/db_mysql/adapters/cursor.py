# canonmap/services/db_mysql/adapters/cursor.py

import logging
from contextlib import contextmanager
from mysql.connector import MySQLConnection, Error

logger = logging.getLogger(__name__)

@contextmanager
def get_cursor(
    connection: MySQLConnection,
    dictionary: bool = False
):
    """
    Context manager for MySQL cursors.
    Yields a cursor and ensures it’s closed afterwards,
    logging any execution errors.
    
    :param connection: an open MySQLConnection
    :param dictionary: if True, cursor returns dicts instead of tuples
    """
    cursor = connection.cursor(dictionary=dictionary)
    try:
        yield cursor
    except Error as e:
        logger.error("Cursor operation failed: %s", e, exc_info=True)
        # Roll back any uncommitted transaction if desired:
        try:
            connection.rollback()
        except Error:
            pass
        raise
    finally:
        cursor.close()