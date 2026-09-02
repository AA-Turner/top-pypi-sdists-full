"""Host-injection registry for matrx-scraper's DB binding (tiny, dependency-free).

The host calls :func:`matrx_scraper.configure_db` once at startup; the bind layer
reads the pool name back here. Mirrors matrx-runtime/_config.py.
"""

from __future__ import annotations


_registry: dict[str, object] = {"db_config_name": None}


def set_db_config_name(name: str) -> None:
    _registry["db_config_name"] = name


def get_db_config_name() -> str:
    """Resolve the host's matrx-orm pool name — ONE name, platform-wide.

    Order: the name injected via ``configure_db(db_config_name=...)`` → the
    canonical ``MATRX_DB_CONFIG_NAME`` env var. Raises if neither is set.

    This is a matrx-orm CONFIG NAME, not a connection — it says "alias onto the
    pool the host already opened" and can never point at a different database.
    It was ``MATRX_SCRAPER_DB_NAME`` until 2026-08-09; three packages each had
    their own name for one concept, which is exactly how agents come to believe
    the packages connect to different places.
    """
    from matrx_orm import host_db_config_name

    return host_db_config_name(injected=_registry.get("db_config_name"), who="matrx-scraper")
