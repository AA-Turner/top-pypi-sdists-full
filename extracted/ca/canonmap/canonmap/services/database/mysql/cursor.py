# canonmap/services/database/mysql/cursor.py
import logging
logger = logging.getLogger(__name__)

from contextlib import contextmanager
from mysql.connector import MySQLConnection, Error

@contextmanager
def get_cursor(
    connection: MySQLConnection,
    dictionary: bool = False
):
    cursor = connection.cursor(dictionary=dictionary)
    try:
        yield cursor
    except Error as e:
        logger.error("Cursor operation failed: %s", e, exc_info=True)
        try:
            connection.rollback()
        except Error:
            pass
        raise
    finally:
        cursor.close()