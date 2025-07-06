"""Utility modules for TSAL."""

from .error_dignity import activate_error_dignity
from .github_api import fetch_repo_files, fetch_languages
from .octopus_api import get_products, get_electricity_tariffs
from .wikipedia_api import search as wiki_search, summary as wiki_summary
from .groundnews_api import fetch_news, GroundNewsAPIError
from .intent_metrics import calculate_idm, MetricInputs, timed_idm
from .system_status import get_status, print_status

__all__ = [
    "activate_error_dignity",
    "fetch_repo_files",
    "fetch_languages",
    "get_products",
    "get_electricity_tariffs",
    "wiki_search",
    "wiki_summary",
    "fetch_news",
    "GroundNewsAPIError",
    "calculate_idm",
    "MetricInputs",
    "timed_idm",
    "get_status",
    "print_status",
]
