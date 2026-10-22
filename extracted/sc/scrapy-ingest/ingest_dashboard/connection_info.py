"""Safe connection summary for the dashboard UI."""

from __future__ import annotations

from scrapy_ingest.utils.summary import display_database

_DIALECT_TITLES = {"postgres": "PostgreSQL", "mysql": "MySQL", "sqlite": "SQLite"}


def build_connection_info(settings, *, uses_sql: bool) -> dict:
    """Return display-safe destination details (no credentials)."""
    base = {
        "jobs_table": settings.db_jobs_table,
        "items_table": settings.db_items_table,
    }
    if uses_sql:
        dialect = getattr(settings, "db_dialect", "postgres") or "postgres"
        info = {
            **base,
            "destination": "database",
            "kind": dialect,
            "title": _DIALECT_TITLES.get(dialect, dialect.upper()),
            "display_url": display_database(settings.db_url),
        }
        if dialect == "postgres":
            info["schema"] = getattr(settings, "db_schema", "public")
        return info

    url = settings.search_url or ""
    return {
        **base,
        "destination": "search",
        "kind": "search",
        "title": "OpenSearch / Elasticsearch",
        "display_url": display_database(url) if "://" in str(url) else str(url),
    }
