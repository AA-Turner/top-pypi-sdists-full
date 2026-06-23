"""
Tests for contentstack_utils.endpoint.Endpoint and the Utils proxy.
"""

import pytest

from contentstack_utils.endpoint import Endpoint
from contentstack_utils.utils import Utils


@pytest.fixture(autouse=True)
def reset_cache():
    """Isolate each test — forces a fresh regions.json read."""
    Endpoint.reset_cache()
    yield
    Endpoint.reset_cache()


# ---------------------------------------------------------------------------
# Default region (us / na)
# ---------------------------------------------------------------------------

class TestDefaultRegion:
    def test_returns_all_endpoints_when_no_service(self):
        endpoints = Endpoint.get_contentstack_endpoint()
        assert isinstance(endpoints, dict)
        assert "contentDelivery" in endpoints
        assert "contentManagement" in endpoints

    def test_content_delivery_url(self):
        url = Endpoint.get_contentstack_endpoint("us", "contentDelivery")
        assert url == "https://cdn.contentstack.io"

    def test_content_management_url(self):
        url = Endpoint.get_contentstack_endpoint("us", "contentManagement")
        assert url == "https://api.contentstack.io"


# ---------------------------------------------------------------------------
# NA region alias resolution
# ---------------------------------------------------------------------------

NA_ALIASES = ["na", "us", "aws-na", "aws_na", "NA", "US", "AWS-NA", "AWS_NA"]

@pytest.mark.parametrize("alias", NA_ALIASES)
def test_na_aliases_resolve_to_same_cdn(alias):
    url = Endpoint.get_contentstack_endpoint(alias, "contentDelivery")
    assert url == "https://cdn.contentstack.io"


# ---------------------------------------------------------------------------
# All 7 regions — contentDelivery spot-checks
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("region,expected", [
    ("na",       "https://cdn.contentstack.io"),
    ("eu",       "https://eu-cdn.contentstack.com"),
    ("au",       "https://au-cdn.contentstack.com"),
    ("azure-na", "https://azure-na-cdn.contentstack.com"),
    ("azure-eu", "https://azure-eu-cdn.contentstack.com"),
    ("gcp-na",   "https://gcp-na-cdn.contentstack.com"),
    ("gcp-eu",   "https://gcp-eu-cdn.contentstack.com"),
])
def test_content_delivery_by_region(region, expected):
    assert Endpoint.get_contentstack_endpoint(region, "contentDelivery") == expected


# ---------------------------------------------------------------------------
# All 7 regions — contentManagement spot-checks
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("region,expected", [
    ("na",       "https://api.contentstack.io"),
    ("eu",       "https://eu-api.contentstack.com"),
    ("au",       "https://au-api.contentstack.com"),
    ("azure-na", "https://azure-na-api.contentstack.com"),
    ("azure-eu", "https://azure-eu-api.contentstack.com"),
    ("gcp-na",   "https://gcp-na-api.contentstack.com"),
    ("gcp-eu",   "https://gcp-eu-api.contentstack.com"),
])
def test_content_management_by_region(region, expected):
    assert Endpoint.get_contentstack_endpoint(region, "contentManagement") == expected


# ---------------------------------------------------------------------------
# All expected service keys present
# ---------------------------------------------------------------------------

EXPECTED_SERVICE_KEYS = [
    "application", "contentDelivery", "contentManagement", "auth",
    "graphqlDelivery", "preview", "graphqlPreview", "images", "assets",
    "automate", "launch", "developerHub", "brandKit", "genAI",
    "personalizeManagement", "personalizeEdge", "composableStudio",
]

def test_all_service_keys_present_for_eu():
    endpoints = Endpoint.get_contentstack_endpoint("eu")
    for key in EXPECTED_SERVICE_KEYS:
        assert key in endpoints, f"Missing service key: {key}"

def test_na_has_asset_management_key():
    # NA is the only region that currently includes assetManagement.
    endpoints = Endpoint.get_contentstack_endpoint("na")
    assert "assetManagement" in endpoints


# ---------------------------------------------------------------------------
# omit_https flag
# ---------------------------------------------------------------------------

class TestOmitHttps:
    def test_strips_scheme_from_single_service(self):
        host = Endpoint.get_contentstack_endpoint("eu", "contentDelivery", omit_https=True)
        assert host == "eu-cdn.contentstack.com"

    def test_strips_scheme_from_all_services(self):
        endpoints = Endpoint.get_contentstack_endpoint("na", omit_https=True)
        assert isinstance(endpoints, dict)
        for key, url in endpoints.items():
            assert "https://" not in url, f"Service {key} still has https://"
            assert "http://" not in url, f"Service {key} still has http://"

    def test_false_retains_scheme(self):
        url = Endpoint.get_contentstack_endpoint("na", "contentManagement", omit_https=False)
        assert url.startswith("https://")

    def test_omit_https_positional_argument(self):
        # Confirm the third positional arg is honoured (mirrors PHP signature).
        host = Endpoint.get_contentstack_endpoint("gcp-na", "contentDelivery", True)
        assert host == "gcp-na-cdn.contentstack.com"


# ---------------------------------------------------------------------------
# Case-insensitive and underscore alias matching
# ---------------------------------------------------------------------------

class TestAliasMatching:
    def test_uppercase_alias(self):
        url = Endpoint.get_contentstack_endpoint("AWS-NA", "contentDelivery")
        assert url == "https://cdn.contentstack.io"

    def test_underscore_azure_alias(self):
        url = Endpoint.get_contentstack_endpoint("azure_na", "contentDelivery")
        assert url == "https://azure-na-cdn.contentstack.com"

    def test_underscore_gcp_alias(self):
        url = Endpoint.get_contentstack_endpoint("gcp_eu", "contentManagement")
        assert url == "https://gcp-eu-api.contentstack.com"

    def test_mixed_case_eu(self):
        url = Endpoint.get_contentstack_endpoint("EU", "contentDelivery")
        assert url == "https://eu-cdn.contentstack.com"

    def test_mixed_case_au(self):
        url = Endpoint.get_contentstack_endpoint("AU", "contentDelivery")
        assert url == "https://au-cdn.contentstack.com"


# ---------------------------------------------------------------------------
# Return-all-endpoints (no service argument)
# ---------------------------------------------------------------------------

class TestNoService:
    def test_returns_dict(self):
        result = Endpoint.get_contentstack_endpoint("au")
        assert isinstance(result, dict)
        assert len(result) > 1

    def test_dict_contains_correct_urls(self):
        endpoints = Endpoint.get_contentstack_endpoint("au")
        assert endpoints["contentDelivery"] == "https://au-cdn.contentstack.com"
        assert endpoints["contentManagement"] == "https://au-api.contentstack.com"

    def test_default_call_returns_na(self):
        endpoints = Endpoint.get_contentstack_endpoint()
        assert endpoints["contentDelivery"] == "https://cdn.contentstack.io"


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

class TestErrorCases:
    def test_empty_region_raises_value_error(self):
        with pytest.raises(ValueError, match="Empty region provided"):
            Endpoint.get_contentstack_endpoint("")

    def test_unknown_region_raises_lookup_error(self):
        with pytest.raises(LookupError, match="Invalid region: invalid-region"):
            Endpoint.get_contentstack_endpoint("invalid-region")

    def test_unknown_service_raises_lookup_error(self):
        with pytest.raises(LookupError, match='Service "unknownService" not found'):
            Endpoint.get_contentstack_endpoint("na", "unknownService")

    def test_whitespace_region_raises_value_error(self):
        with pytest.raises(ValueError, match="Empty region provided"):
            Endpoint.get_contentstack_endpoint("   ")


# ---------------------------------------------------------------------------
# camelCase alias (cross-SDK parity)
# ---------------------------------------------------------------------------

class TestCamelCaseAlias:
    def test_get_contentstack_endpoint_camel_case(self):
        url = Endpoint.getContentstackEndpoint("na", "contentDelivery")
        assert url == "https://cdn.contentstack.io"

    def test_camel_case_and_snake_case_return_same(self):
        snake = Endpoint.get_contentstack_endpoint("eu", "contentDelivery")
        camel = Endpoint.getContentstackEndpoint("eu", "contentDelivery")
        assert snake == camel


# ---------------------------------------------------------------------------
# Utils proxy
# ---------------------------------------------------------------------------

class TestUtilsProxy:
    def test_proxy_returns_same_as_endpoint_class(self):
        via_endpoint = Endpoint.get_contentstack_endpoint("eu", "contentDelivery")
        via_utils = Utils.get_contentstack_endpoint("eu", "contentDelivery")
        assert via_endpoint == via_utils

    def test_proxy_default_region(self):
        url = Utils.get_contentstack_endpoint("us", "contentManagement")
        assert url == "https://api.contentstack.io"

    def test_proxy_omit_https(self):
        host = Utils.get_contentstack_endpoint("gcp-na", "contentDelivery", omit_https=True)
        assert host == "gcp-na-cdn.contentstack.com"

    def test_proxy_all_endpoints(self):
        endpoints = Utils.get_contentstack_endpoint("azure-eu")
        assert isinstance(endpoints, dict)
        assert "contentDelivery" in endpoints

    def test_proxy_camel_case_alias(self):
        url = Utils.getContentstackEndpoint("na", "contentDelivery")
        assert url == "https://cdn.contentstack.io"

    def test_proxy_error_propagates(self):
        with pytest.raises(LookupError):
            Utils.get_contentstack_endpoint("not-a-region", "contentDelivery")


# ---------------------------------------------------------------------------
# Cache behaviour
# ---------------------------------------------------------------------------

class TestCache:
    def test_second_call_uses_cache(self, reset_cache):
        from unittest.mock import patch, MagicMock
        Endpoint.get_contentstack_endpoint("na", "contentDelivery")
        with patch("builtins.open", wraps=open) as spy:
            Endpoint.get_contentstack_endpoint("eu", "contentDelivery")
            spy.assert_not_called()

    def test_reset_cache_clears_data(self):
        Endpoint.get_contentstack_endpoint("na")  # primes cache
        assert Endpoint._regions_data is not None
        Endpoint.reset_cache()
        assert Endpoint._regions_data is None
