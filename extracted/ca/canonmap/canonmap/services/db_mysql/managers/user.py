# canonmap/services/db_mysql/managers/user.py

import logging
from typing import Optional

from canonmap.services.db_mysql.adapters.connection import ConnectionManager
from canonmap.services.db_mysql.adapters.cursor import get_cursor

logger = logging.getLogger(__name__)


class UserManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    def create_user(
        self,
        username: str,
        password: str,
        host: str = '%',
        privileges: Optional[str] = None,
        on_database: Optional[str] = None
    ) -> None:
        conn = self.connection_manager.connect()
        with get_cursor(conn) as cursor:
            cursor.execute(
                f"CREATE USER IF NOT EXISTS `{username}`@`{host}` IDENTIFIED BY %s",
                (password,)
            )
            if privileges:
                target = f"`{on_database}`.*" if on_database else "*.*"
                cursor.execute(
                    f"GRANT {privileges} ON {target} TO `{username}`@`{host}`"
                )
            cursor.execute("FLUSH PRIVILEGES")
        conn.commit()

        logger.info(
            f"User '{username}'@'{host}' has been created"
            + (f" with privileges '{privileges}' on {on_database}" if privileges else "")
        )

    def delete_user(self, username: str, host: str = '%') -> None:
        conn = self.connection_manager.connect()
        with get_cursor(conn) as cursor:
            cursor.execute(f"DROP USER IF EXISTS `{username}`@`{host}`")
            cursor.execute("FLUSH PRIVILEGES")
        conn.commit()

        logger.info(f"User '{username}'@'{host}' has been deleted")