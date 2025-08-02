"""Database related functionality."""


class TableSizeMixin:
    """Add a table size functionality to a Django Manager."""

    def db_table_size(self) -> int:
        """Calculate the database table size in bytes.

        This method works for MySQL/MariaDB databases only.
        """
        from django.db import connection

        is_mysql = connection.settings_dict.get("ENGINE") == "django.db.backends.mysql"
        if not is_mysql:
            raise RuntimeError("This method only works for MySQL like databases.")
        database_name = connection.settings_dict["NAME"]
        table_name = self.model._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    table_name AS `Table`,
                    round(data_length + index_length, 2)
                FROM information_schema.TABLES
                WHERE table_schema = %s
                    AND table_name = %s;
                """,
                [database_name, table_name],
            )
            row = cursor.fetchone()
        try:
            return int(row[1])
        except (TypeError, IndexError, ValueError):
            raise ValueError(
                f"Failed to calculate table size for {database_name}.{table_name}"
            ) from None
