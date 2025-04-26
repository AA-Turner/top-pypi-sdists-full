import logging
import os

from pysqlsync.base import BaseContext, Explorer

from dap.replicator import meta_schema

logger = logging.getLogger(__name__)

LATEST_VERSION = 1

MYSQL_DIALECT = "mysql"
POSTGRESQL_DIALECT = "postgresql"
MSSQL_DIALECT = "mssql"
SUPPORTED_DIALECTS = [MYSQL_DIALECT, POSTGRESQL_DIALECT, MSSQL_DIALECT]

SCRIPT_FILENAME_TEMPLATE = "{dialect}_{from_version}_to_{to_version}.sql"
SQL_DELETE_TABLE_CONTENTS = "DELETE FROM {table}"
SQL_SWITCH_IDENTITY_INSERT = "SET IDENTITY_INSERT {table} {state}"
SQL_INSERT_VERSION = "INSERT INTO {table} (version) VALUES ({version})"


class VersionUpgrader:
    explorer: Explorer
    base_context: BaseContext
    dialect: str

    def __init__(
        self, explorer: Explorer, base_context: BaseContext, dialect: str
    ) -> None:
        self.explorer = explorer
        self.base_context = base_context
        self.dialect = dialect

    async def upgrade(self) -> None:
        if self.dialect not in SUPPORTED_DIALECTS:
            raise ValueError(
                f"Error during upgrade: Dialect {self.dialect} not supported"
            )
        await self.explorer.synchronize(modules=[meta_schema])
        db_version = await self._get_version_from_db()

        logger.debug(f"Current version: {db_version}; Latest version: {LATEST_VERSION}")
        if db_version == LATEST_VERSION:
            logger.debug("No upgrade needed")
            return

        logger.debug("Upgrading database")
        self._ensure_upgrade_scripts_exist(db_version, LATEST_VERSION)
        await self._run_upgrade_scripts(db_version, LATEST_VERSION)
        await self._update_version_in_db(LATEST_VERSION)

    async def _get_version_from_db(self) -> int:
        table = self.base_context.get_table(meta_schema.database_version)
        records = await self.base_context.query_all(
            meta_schema.database_version, f"SELECT version FROM {table.name}"
        )
        if records:
            logger.debug(f"Found version records: {records}")
            if len(records) > 1:
                raise ValueError(
                    f"Error during upgrade: found more than one version record in {table.name}"
                )
            if not isinstance(records[0].version, int):
                raise ValueError(
                    f"Error during upgrade: version {records[0].version} is not an integer"
                )
            return records[0].version
        else:
            logger.debug(f"No version records found in {table.name}")
            return 0

    async def _update_version_in_db(self, version: int) -> None:
        table = self.base_context.get_table(meta_schema.database_version)
        await self.base_context.execute(
            SQL_DELETE_TABLE_CONTENTS.format(table=table.name)
        )
        # the version table is a misuse of pysqlsync which for some dialects will not work, this is a workaround
        if self.dialect == MSSQL_DIALECT:
            await self.base_context.execute(
                SQL_SWITCH_IDENTITY_INSERT.format(table=table.name, state="ON")
            )
            await self.base_context.execute(
                SQL_INSERT_VERSION.format(table=table.name, version=version)
            )
            await self.base_context.execute(
                SQL_SWITCH_IDENTITY_INSERT.format(table=table.name, state="OFF")
            )
        else:
            await self.base_context.upsert_data(
                meta_schema.database_version,
                [meta_schema.database_version(version=version)],
            )

    async def _run_upgrade_scripts(self, from_version: int, to_version: int) -> None:
        logger.debug(
            f"Running upgrade scripts from version {from_version} to {to_version}"
        )
        for version in range(from_version, to_version):
            logger.debug(f"Upgrading from version {version} to {version + 1}")
            file_name = VersionUpgrader._get_script_filename(
                self.dialect, version, version + 1
            )
            logger.debug(f"Running upgrade script: {file_name}")
            try:
                with open(file_name, "r") as f:
                    sql = f.read()
                    logger.debug(f"Executing SQL: {sql}")
                    await self.base_context.execute(sql)
            except FileNotFoundError:
                logger.error(f"Error during upgrade: file {file_name} not found")
                raise

    def _ensure_upgrade_scripts_exist(self, from_version: int, to_version: int) -> None:
        for version in range(from_version, to_version):
            file_name = VersionUpgrader._get_script_filename(
                self.dialect, version, version + 1
            )
            if not os.path.isfile(file_name):
                raise FileNotFoundError(f"Error: file {file_name} not found")

    @staticmethod
    def _get_script_filename(dialect: str, from_version: int, to_version: int) -> str:
        file_name = SCRIPT_FILENAME_TEMPLATE.format(
            dialect=dialect, from_version=from_version, to_version=to_version
        )
        file_name = os.path.join(os.path.dirname(__file__), file_name)
        return file_name
