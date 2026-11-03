"""
Module for managing and validating crawler settings.
"""

from urllib.parse import quote_plus

from .sqlite_path import default_sqlite_url


class Settings:
    """
    Handles settings configuration for crawlers, providing access to default values,
    database table names, and other operational parameters defined in crawler settings.
    """

    DEFAULT_ITEMS_TABLE = "ingest_items"
    DEFAULT_REQUESTS_TABLE = "ingest_requests"
    DEFAULT_LOGS_TABLE = "ingest_logs"
    DEFAULT_JOBS_TABLE = "ingest_jobs"
    DEFAULT_SPIDERS_TABLE = "ingest_spiders"
    DEFAULT_JOB_META_TABLE = "ingest_job_meta"
    DEFAULT_DB_TYPE = "postgres"
    DEFAULT_TIMEZONE = "Asia/Karachi"
    DEFAULT_BATCH_SIZE = 50
    DEFAULT_FLUSH_INTERVAL = 10.0
    DEFAULT_SHOW_SUMMARY = True
    DEFAULT_SQLITE_FILENAME = "ingest.db"
    _DB_SCHEMES = {
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "mysql": "mysql",
        "mariadb": "mysql",
    }
    _DB_PORTS = {
        "postgres": 5432,
        "postgresql": 5432,
        "mysql": 3306,
        "mariadb": 3306,
    }
    _URL_DIALECTS = {
        "postgres": "postgres",
        "postgresql": "postgres",
        "mysql": "mysql",
        "mariadb": "mysql",
        "sqlite": "sqlite",
    }

    def __init__(self, crawler_settings):
        self.crawler_settings = crawler_settings

    @property
    def ingest_sqlite_enabled(self):
        """Use local SQLite when no ``DB_URL`` / ``DB_*`` and no ``SEARCH_URL``."""
        return self.crawler_settings.getbool("INGEST_SQLITE_ENABLED", True)

    @property
    def ingest_sqlite_path(self):
        return self.crawler_settings.get(
            "INGEST_SQLITE_PATH", self.DEFAULT_SQLITE_FILENAME
        )

    @property
    def using_default_sqlite(self):
        return (
            not self._has_db_config()
            and not self.ingest_to_search
            and self.ingest_sqlite_enabled
        )

    @property
    def db_url(self):
        """Database URL from DB_URL, discrete DB_* fields, or default SQLite."""
        url = self.crawler_settings.get("DB_URL")
        if url:
            return url

        host = self.crawler_settings.get("DB_HOST")
        if host:
            user = self.crawler_settings.get("DB_USER") or ""
            password = self.crawler_settings.get("DB_PASSWORD") or ""
            port = self.crawler_settings.get("DB_PORT", self._default_port())
            name = self.crawler_settings.get("DB_NAME") or ""
            scheme = self._DB_SCHEMES.get(self.db_type, self.db_type)
            return (
                f"{scheme}://{quote_plus(str(user))}:{quote_plus(str(password))}"
                f"@{host}:{port}/{name}"
            )

        if self.using_default_sqlite:
            return default_sqlite_url(self.ingest_sqlite_path)
        return None

    @property
    def db_type(self):
        """Database engine from ``DB_TYPE`` (default: postgres)."""
        raw = self.crawler_settings.get("DB_TYPE", self.DEFAULT_DB_TYPE)
        if raw in (None, ""):
            return self.DEFAULT_DB_TYPE
        return str(raw).strip().lower()

    def _default_port(self):
        return self._DB_PORTS.get(self.db_type, 5432)

    @property
    def db_dialect(self):
        """``postgres``, ``mysql``, or ``sqlite``."""
        url = self.db_url
        if url and "://" in str(url):
            scheme = str(url).split("://", 1)[0].lower().split("+")[0]
            if scheme in self._URL_DIALECTS:
                return self._URL_DIALECTS[scheme]
        if self.db_type in ("mysql", "mariadb"):
            return "mysql"
        return "postgres"

    @property
    def db_items_table(self):
        return self.crawler_settings.get("ITEMS_TABLE", self.DEFAULT_ITEMS_TABLE)

    @property
    def db_requests_table(self):
        return self.crawler_settings.get("REQUESTS_TABLE", self.DEFAULT_REQUESTS_TABLE)

    @property
    def db_logs_table(self):
        return self.crawler_settings.get("LOGS_TABLE", self.DEFAULT_LOGS_TABLE)

    @property
    def db_jobs_table(self):
        return (
            self.crawler_settings.get("JOBS_TABLE")
            or self.crawler_settings.get("DETAILS_TABLE")
            or self.DEFAULT_JOBS_TABLE
        )

    @property
    def db_spiders_table(self):
        return self.crawler_settings.get("SPIDERS_TABLE", self.DEFAULT_SPIDERS_TABLE)

    @property
    def db_job_meta_table(self):
        return self.crawler_settings.get("JOB_META_TABLE", self.DEFAULT_JOB_META_TABLE)

    @property
    def job_session_id(self):
        raw = self.crawler_settings.get("JOB_SESSION_ID")
        return int(raw) if raw not in (None, "") else None

    @property
    def job_new_session_per_crawl(self):
        return self.crawler_settings.getbool("JOB_NEW_SESSION_PER_CRAWL", False)

    @property
    def create_tables(self):
        return self.crawler_settings.getbool("CREATE_TABLES", True)

    @property
    def db_schema(self):
        """PostgreSQL schema for ingest tables (``DB_SCHEMA``, default ``public``)."""
        raw = self.crawler_settings.get("DB_SCHEMA", "public")
        return str(raw).strip() or "public"

    @property
    def ingest_batch_size(self):
        return self.crawler_settings.getint(
            "INGEST_BATCH_SIZE", self.DEFAULT_BATCH_SIZE
        )

    @property
    def ingest_flush_interval(self):
        return self.crawler_settings.getfloat(
            "INGEST_FLUSH_INTERVAL", self.DEFAULT_FLUSH_INTERVAL
        )

    @property
    def ingest_show_summary(self):
        """Print the end-of-crawl summary table (default: True)."""
        return self.crawler_settings.getbool(
            "INGEST_SHOW_SUMMARY", self.DEFAULT_SHOW_SUMMARY
        )

    def _has_db_config(self):
        if self.crawler_settings.get("DB_URL"):
            return True
        return bool(self.crawler_settings.get("DB_HOST"))

    @property
    def ingest_to_search(self):
        return bool(self.search_url)

    @property
    def ingest_to_database(self):
        if self._has_db_config():
            return True
        if self.ingest_to_search:
            return False
        return self.ingest_sqlite_enabled

    @property
    def search_url(self):
        return self.crawler_settings.get("SEARCH_URL")

    @property
    def search_user(self):
        return self.crawler_settings.get("SEARCH_USER")

    @property
    def search_password(self):
        return self.crawler_settings.get("SEARCH_PASSWORD")

    @property
    def search_ssl_verify(self):
        return self.crawler_settings.getbool("SEARCH_SSL_VERIFY", True)

    def get_tz(self):
        return self.crawler_settings.get("TIMEZONE", self.DEFAULT_TIMEZONE)

    @staticmethod
    def get_identifier_column():
        return "job_id"

    def get_identifier_value(self, spider):
        """Explicit ``JOB_ID`` or id allocated at job start (``spider_id/run``)."""
        from ..database.job_sequence import resolve_configured_job_id
        from ..utils.job_id import cached_job_id

        configured = resolve_configured_job_id(self, spider)
        if configured:
            return configured
        return cached_job_id(spider)


def validate_settings(settings):
    """Validate the configured ingest destinations."""
    from ..exceptions import ConfigurationError

    if not settings.ingest_to_database and not settings.ingest_to_search:
        raise ConfigurationError(
            "Configure at least one destination: set DB_URL (or DB_* fields), "
            "SEARCH_URL, or enable default SQLite (INGEST_SQLITE_ENABLED)"
        )
    if settings.ingest_to_database:
        url = settings.db_url
        if url and "://" in str(url):
            scheme = str(url).split("://", 1)[0].lower().split("+")[0]
            if scheme not in settings._URL_DIALECTS:
                supported = ", ".join(sorted(settings._URL_DIALECTS))
                raise ConfigurationError(
                    f"Unsupported database URL scheme {scheme!r}. Supported: {supported}"
                )
        elif settings.db_type not in settings._DB_SCHEMES:
            supported = ", ".join(sorted(settings._DB_SCHEMES))
            raise ConfigurationError(
                f"Unsupported DB_TYPE={settings.db_type!r}. Supported: {supported}"
            )
        if not url:
            raise ConfigurationError(
                "Database connection is incomplete: set DB_URL or "
                "DB_HOST / DB_USER / DB_PASSWORD / DB_NAME"
            )
    return True
