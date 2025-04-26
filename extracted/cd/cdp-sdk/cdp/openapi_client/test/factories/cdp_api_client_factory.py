import pytest
from cdp.openapi_client.cdp_api_client import CdpApiClient


@pytest.fixture
def cdp_api_client_factory():
    """Create and return a factory for CDP API clients.

    Returns:
        callable: A factory function that creates CDP API clients
    """

    def _create_client(
        api_key="test_api_key",
        private_key="test_private_key",
        host="https://test.api.cdp.coinbase.com/platform",
        wallet_secret="test_wallet_secret",
        debugging=True,
        max_network_retries=3,
        source="test_source",
        source_version="1.0.0",
    ):
        """Factory function to create a CdpApiClient instance with test values."""
        return CdpApiClient(
            api_key_id=api_key,
            api_key_secret=private_key,
            base_path=host,
            wallet_secret=wallet_secret,
            debugging=debugging,
            max_network_retries=max_network_retries,
            source=source,
            source_version=source_version,
        )

    return _create_client
