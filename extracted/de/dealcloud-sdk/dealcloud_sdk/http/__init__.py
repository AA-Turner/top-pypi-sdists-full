"""HTTP client adapters for DealCloud (extends intapp_rest_client)."""

from .dealcloud_rest_client import DealCloudRestClient, normalize_plain_text_error_body

__all__ = ["DealCloudRestClient", "normalize_plain_text_error_body"]
