import logging

from ..integration.database import DatabaseConnection, get_parameters
from .base import Arguments, CommandRegistrar

logger = logging.getLogger("dap")


class AbstractDbCommandRegistrar(CommandRegistrar):
    async def _before_execute(self, args: Arguments) -> None:
        if not args.connection_string:
            raise ValueError("missing database connection string")

        logger.debug("Checking for valid database connection string")
        try:
            _, _ = get_parameters(args.connection_string)
        except ValueError:
            logger.error(
                "Invalid database connection string, please check its format and URL-encoding of special characters"
            )
            raise

        logger.debug("Checking connection to database")
        connection = DatabaseConnection(args.connection_string)
        async with connection.connection as conn:
            # log database version information
            version_sql = None
            if connection.dialect in ["postgresql", "mysql"]:
                version_sql = "SELECT version()"
            elif connection.dialect == "mssql":
                version_sql = "SELECT @@VERSION"
            if version_sql:
                version = await conn.query_one(signature=str, statement=version_sql)
            else:
                version = "unknown"
            logger.info(f"Database version: {version}")
            pass
