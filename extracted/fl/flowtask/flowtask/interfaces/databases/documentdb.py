from typing import Optional
from querysource.conf import (
    DOCUMENTDB_HOSTNAME,
    DOCUMENTDB_PORT,
    DOCUMENTDB_DATABASE,
    DOCUMENTDB_USERNAME,
    DOCUMENTDB_PASSWORD,
    DOCUMENTDB_TLSFILE,
)
from .db import DBSupport


class DocumentDBSupport(DBSupport):
    """DocumentDBSupport.

    Interface for adding AWS DocumentDB Database Support to Components.
    """
    _service_name: str = 'Flowtask'
    driver: str = 'mongo'
    _credentials = {
        "host": str,
        "port": int,
        "username": str,
        "password": str,
        "database": str,
        "dbtype": "documentdb",
        "ssl": True,
        "tlsCAFile": str,
    }

    def default_connection(self, driver: str = 'mongo', credentials: Optional[dict] = None):
        """default_connection.

        Default Connection to RethinkDB.
        """
        if not credentials:
            credentials = {
                "host": DOCUMENTDB_HOSTNAME,
                "port": DOCUMENTDB_PORT,
                "username": DOCUMENTDB_USERNAME,
                "password": DOCUMENTDB_PASSWORD,
                "database": DOCUMENTDB_DATABASE,
                "dbtype": "documentdb",
                "ssl": True,
                "tlsCAFile": DOCUMENTDB_TLSFILE,
            }
        try:
            return self.get_connection(
                driver=driver,
                params=credentials
            )
        except Exception as err:
            raise Exception(
                f"Error getting Default DocumentDB Connection: {err!s}"
            ) from err
