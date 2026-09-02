"""AI-tool-facing feature wrappers built on top of the matrx_scraper core."""

from matrx_scraper.features.quick_search import search_web_mcp_quick
from matrx_scraper.features.read_page import read_page_mcp_quick, read_page_mcp_summarized
from matrx_scraper.features.mcp_tool_helpers import scrape_url_core, scrape_urls_from_search_result
from matrx_scraper.features.stock_image_search import (
    parse_stock_image_item,
    search_stock_images,
)
from matrx_scraper.features.utils import format_scraped_pages_section

__all__ = [
    "search_web_mcp_quick",
    "read_page_mcp_quick",
    "read_page_mcp_summarized",
    "scrape_url_core",
    "scrape_urls_from_search_result",
    "search_stock_images",
    "parse_stock_image_item",
    "format_scraped_pages_section",
]
