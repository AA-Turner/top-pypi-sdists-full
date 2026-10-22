"""Load scrapy-ingest Settings from a Scrapy project or overrides."""

from __future__ import annotations

from scrapy_ingest.config.settings import Settings, validate_settings


def load_crawler_settings(*, db_url: str | None = None, search_url: str | None = None):
    try:
        from scrapy.utils.project import get_project_settings

        crawler_settings = get_project_settings()
    except Exception:
        from scrapy.settings import Settings as ScrapySettings

        crawler_settings = ScrapySettings()
    for key, value in (("DB_URL", db_url), ("SEARCH_URL", search_url)):
        if value is not None:
            crawler_settings.set(key, value, priority="cmdline")
    return crawler_settings


def load_ingest_settings(
    *, db_url: str | None = None, search_url: str | None = None
) -> Settings:
    settings = Settings(load_crawler_settings(db_url=db_url, search_url=search_url))
    validate_settings(settings)
    return settings
