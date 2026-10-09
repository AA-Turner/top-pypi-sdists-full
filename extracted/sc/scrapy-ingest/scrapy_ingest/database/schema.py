"""
Database schema management utilities for scrapy_ingest.
"""
import logging
import re

from ..exceptions import SchemaError

logger = logging.getLogger(__name__)


class SchemaManager:
    """Create ingest tables if they do not already exist."""

    def __init__(self, db_connection, settings):
        self.db = db_connection
        self.settings = settings
        dialect = getattr(settings, "db_dialect", "postgres")
        self._dialect = dialect
        mysql = dialect == "mysql"
        sqlite = dialect == "sqlite"
        if sqlite:
            self._pk = "INTEGER PRIMARY KEY AUTOINCREMENT"
            self._json = "TEXT"
            self._bool = "INTEGER"
            self._suffix = ""
            self._time = "time"
        elif mysql:
            self._pk = "INT NOT NULL AUTO_INCREMENT PRIMARY KEY"
            self._json = "JSON"
            self._bool = "BOOLEAN"
            self._suffix = " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
            self._time = "`time`"
        else:
            self._pk = "SERIAL PRIMARY KEY"
            self._json = "JSONB"
            self._bool = "BOOLEAN"
            self._suffix = ""
            self._time = "time"

    @staticmethod
    def _slug(identifier: str) -> str:
        """Safe fragment for index / FK names (custom table names allowed)."""
        out = "".join(c if c.isalnum() else "_" for c in str(identifier))
        return out.strip("_") or "ingest"

    def _fk_name(self, table: str, column: str) -> str:
        return f"fk_{self._slug(table)}_{self._slug(column)}"[:62]

    def _ix_name(self, table: str, column: str) -> str:
        return f"ix_{self._slug(table)}_{self._slug(column)}"[:62]

    def _uq_name(self, table: str, column: str) -> str:
        return f"uq_{self._slug(table)}_{self._slug(column)}"[:62]

    def _uq(self, table: str, column: str) -> str:
        name = self._uq_name(table, column)
        return f"CONSTRAINT {name} UNIQUE ({column})"

    def _fk(self, table: str, column: str, ref_table: str, ref_column: str = "id", on_delete=None):
        name = self._fk_name(table, column)
        clause = (
            f"CONSTRAINT {name} FOREIGN KEY ({column}) "
            f"REFERENCES {ref_table}({ref_column})"
        )
        if on_delete:
            clause += f" ON DELETE {on_delete}"
        return clause

    @staticmethod
    def _duplicate_index_error(exc: BaseException) -> bool:
        """MySQL/MariaDB: index already exists (1061)."""
        for err in (exc, getattr(exc, "__cause__", None), getattr(exc, "__context__", None)):
            if err is None:
                continue
            args = getattr(err, "args", ())
            if args and args[0] == 1061:
                return True
        return False

    def _quote_ident(self, name: str) -> str:
        if self._dialect == "mysql":
            return f"`{name}`"
        return name

    def _ensure_index(self, table: str, column: str) -> None:
        name = self._ix_name(table, column)
        table_sql = self._quote_ident(table)
        column_sql = self._quote_ident(column)
        if self._dialect == "mysql":
            sql = f"CREATE INDEX {name} ON {table_sql} ({column_sql})"
            try:
                self.db.execute(sql)
            except Exception as e:
                if self._duplicate_index_error(e):
                    logger.debug("Index %s already exists on %s", name, table)
                    return
                raise
            return
        sql = f"CREATE INDEX IF NOT EXISTS {name} ON {table_sql} ({column_sql})"
        self.db.execute(sql)

    def create_jobs_table(self):
        jobs = self.settings.db_jobs_table
        uq_job_id = self._uq(jobs, "job_id")
        sql = f"""
        CREATE TABLE IF NOT EXISTS {jobs} (
            id {self._pk},
            job_id VARCHAR(255) NOT NULL,
            spider_name VARCHAR(255),
            status VARCHAR(32),
            started_at TIMESTAMP,
            finished_at TIMESTAMP,
            finish_reason VARCHAR(255),
            requests_count INTEGER DEFAULT 0,
            success_requests INTEGER DEFAULT 0,
            failed_requests INTEGER DEFAULT 0,
            items_count INTEGER DEFAULT 0,
            logs_count INTEGER DEFAULT 0,
            errors_count INTEGER DEFAULT 0,
            items_per_min FLOAT DEFAULT 0,
            elapsed_seconds FLOAT DEFAULT 0,
            stats {self._json},
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            {uq_job_id}
        ){self._suffix}
        """
        self.db.execute(sql)
        logger.info("Jobs table %s created/verified", jobs)

    def create_items_table(self):
        jobs = self.settings.db_jobs_table
        items = self.settings.db_items_table
        fk = self._fk(items, "job_id", jobs, on_delete="CASCADE")
        sql = f"""
        CREATE TABLE IF NOT EXISTS {items} (
            id {self._pk},
            job_id INTEGER,
            item {self._json},
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            {fk}
        ){self._suffix}
        """
        self.db.execute(sql)
        logger.info("Items table %s created/verified", self.settings.db_items_table)

    def create_requests_table(self):
        jobs = self.settings.db_jobs_table
        requests = self.settings.db_requests_table
        fk_job = self._fk(requests, "job_id", jobs, on_delete="CASCADE")
        fk_parent = self._fk(requests, "parent_id", requests)
        sql = f"""
        CREATE TABLE IF NOT EXISTS {requests} (
            id {self._pk},
            job_id INTEGER,
            url TEXT,
            method VARCHAR(10),
            status_code INTEGER,
            response_time_secs FLOAT,
            response_size_bytes VARCHAR(32),
            fingerprint VARCHAR(64),
            parent_id INTEGER,
            parent_url TEXT,
            error TEXT,
            success {self._bool},
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            {fk_job},
            {fk_parent}
        ){self._suffix}
        """
        self.db.execute(sql)
        logger.info("Requests table %s created/verified", self.settings.db_requests_table)

    def create_logs_table(self):
        jobs = self.settings.db_jobs_table
        logs = self.settings.db_logs_table
        fk = self._fk(logs, "job_id", jobs, on_delete="CASCADE")
        sql = f"""
        CREATE TABLE IF NOT EXISTS {logs} (
            id {self._pk},
            job_id INTEGER,
            {self._time} VARCHAR(32),
            level VARCHAR(50),
            logger VARCHAR(255),
            message TEXT,
            exception TEXT,
            {fk}
        ){self._suffix}
        """
        self.db.execute(sql)
        logger.info("Logs table %s created/verified", self.settings.db_logs_table)

    def ensure_indexes(self):
        """Create standard indexes (safe to re-run on existing databases)."""
        jobs = self.settings.db_jobs_table
        items = self.settings.db_items_table
        requests = self.settings.db_requests_table
        logs = self.settings.db_logs_table

        specs = [
            (jobs, "spider_name"),
            (jobs, "status"),
            (jobs, "started_at"),
            (items, "job_id"),
            (items, "created_at"),
            (requests, "job_id"),
            (requests, "parent_id"),
            (requests, "fingerprint"),
            (requests, "created_at"),
            (logs, "job_id"),
            (logs, "level"),
        ]
        for table, column in specs:
            self._ensure_index(table, column)
        logger.info("Ingest indexes created/verified")

    def _prepare_postgres(self):
        """Ensure a writable schema is on ``search_path`` (fixes empty search_path)."""
        if self._dialect != "postgres":
            return
        schema = getattr(self.settings, "db_schema", "public") or "public"
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema):
            raise SchemaError(f"Invalid DB_SCHEMA identifier: {schema!r}")
        self.db.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        self.db.execute(f"SET search_path TO {schema}")

    def ensure_tables_exist(self):
        if not self.settings.create_tables:
            logger.info("Table creation disabled. Skipping table creation.")
            return

        try:
            self._prepare_postgres()
            self.create_jobs_table()
            self.create_items_table()
            self.create_requests_table()
            self.create_logs_table()
            self.ensure_indexes()
            self.db.commit()
            logger.info("All tables created/verified successfully")
        except Exception as e:
            logger.error("Failed to create tables: %s", e)
            self.db.rollback()
            raise SchemaError(f"Failed to create tables: {e}") from e
