from .db import DBSupport


class RethinkDBSupport(DBSupport):
    """RethinkDBSupport.

    Interface for adding RethinkDB-based Database Support to Components.
    """
    _service_name: str = 'Flowtask'
    _credentials = {
        "user": str,
        "password": str,
        "host": str,
        "port": int,
        "database": str,
    }

    def default_connection(self, driver: str = 'rethink'):
        """default_connection.

        Default Connection to RethinkDB.
        """
        credentials = {}
        try:
            driver = self.get_default_driver(driver)
            credentials = driver.params()
        except ImportError as err:
            raise ImportError(
                f"Error importing RethinkDB driver: {err!s}"
            ) from err
        try:
            return self.get_connection(
                driver=driver.driver,
                params=credentials
            )
        except Exception as err:
            raise Exception(
                f"Error getting Default Rethink Connection: {err!s}"
            ) from err
