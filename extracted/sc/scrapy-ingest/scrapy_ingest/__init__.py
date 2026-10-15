r"""
   _____                                   ____                      __
  / ___/______________ _____  __  __      /  _/___  ____ ____  _____/ /_
  \__ \/ ___/ ___/ __ `/ __ \/ / / /_____ / // __ \/ __ `/ _ \/ ___/ __/
 ___/ / /__/ /  / /_/ / /_/ / /_/ /_____// // / / / /_/ /  __(__  ) /_
/____/\___/_/   \__,_/ .___/\__, /     /___/_/ /_/\__, /\___/____/\__/
                    /_/    /____/                /____/

scrapy-ingest: One pipeline. Full crawl observability in SQL or Elasticsearch.

Documentation: https://scrapy-ingest.readthedocs.io/en/latest/

Quick start
-----------
Add the pipeline to ``settings.py`` (SQLite ``ingest.db`` is used when no DB/search URL is set)::

    ITEM_PIPELINES = {
        "scrapy_ingest.pipelines.IngestPipeline": 300,
    }

    CREATE_TABLES = True
    # DB_URL = "postgresql://user:pass@localhost:5432/db"
    # SEARCH_URL = "http://localhost:9200"

Enabling ``IngestPipeline`` auto-enables request logging (with ``parent_url``),
error logging, full job logs (including ``print()``), and crawl stats.
"""

from .extensions.log_handler import install_early
from .utils.meta_info import _pkg_meta

install_early()

__version__ = _pkg_meta.version or "1.8.0"
__author__ = _pkg_meta.author or "Fawad Ali"
__license__ = _pkg_meta.license or "MIT"
__description__ = "One pipeline. Full crawl observability in SQL or Elasticsearch."

from .pipelines.main import IngestPipeline
from .extensions.logging import LoggingExtension
from .extensions.stats import StatsExtension
from .pipelines.items import ItemsPipeline
from .pipelines.requests import RequestsPipeline
from .extensions.request_logger import RequestLogger
from .config.settings import Settings, validate_settings
from .exceptions import (
    ConfigurationError,
    DatabaseError,
    DependencyError,
    FlushError,
    IngestConnectionError,
    IngestError,
    SchemaError,
    SearchError,
)

__all__ = [
    "IngestPipeline",
    "LoggingExtension",
    "StatsExtension",
    "ItemsPipeline",
    "RequestsPipeline",
    "RequestLogger",
    "Settings",
    "validate_settings",
    "IngestError",
    "ConfigurationError",
    "DependencyError",
    "IngestConnectionError",
    "DatabaseError",
    "SchemaError",
    "SearchError",
    "FlushError",
    "__version__",
    "__author__",
    "__license__",
    "__description__",
]
