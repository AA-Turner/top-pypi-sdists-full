"""Type stubs for hfortix_fortios.api.utils module."""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.client import HTTPClient
    from hfortix_core.http.interface import IHTTPClient
    from hfortix_fortios.client import FortiOS

__all__ = ["Utils"]

# Type alias for all acceptable client types
FortiOSClient = FortiOS | HTTPClient | IHTTPClient


class PerformanceTestResults:
    """Results from performance testing."""
    
    def print_summary(self) -> None: ...
    def to_dict(self) -> dict[str, Any]: ...


class Utils:
    """
    Utility functions for FortiOS API operations.

    Provides tools for:
    - Performance testing and benchmarking
    - Connection pool validation
    - Device profiling and recommendations

    Example:
        >>> fgt = FortiOS(host="192.168.1.99", token="token")
        >>> results = fgt.api.utils.performance_test()
        >>> results.print_summary()
    """

    def __init__(
        self,
        client: FortiOS | HTTPClient | IHTTPClient,
    ) -> None:
        """Initialize utilities with HTTP client or FortiOS client reference."""
        ...

    def performance_test(
        self,
        test_validation: bool = True,
        test_endpoints: bool = True,
        test_concurrency: bool = False,
        sequential_count: int = 10,
        concurrent_count: int = 50,
        concurrent_level: int = 20,
        endpoints: Optional[list[str]] = None,
    ) -> PerformanceTestResults:
        """
        Run performance tests on this FortiGate device.

        Args:
            test_validation: Test connection pool validation (default: True)
            test_endpoints: Test various API endpoints (default: True)
            test_concurrency: Test concurrent performance (default: False)
            sequential_count: Number of sequential requests per endpoint
            concurrent_count: Number of concurrent requests
            concurrent_level: Concurrency level for async test
            endpoints: Custom list of endpoints to test

        Returns:
            PerformanceTestResults object with detailed metrics and recommendations
        """
        ...

    def validate_connection_pool(self) -> dict[str, Any]:
        """Validate connection pool settings and return stats."""
        ...

    def get_device_profile(self) -> dict[str, Any]:
        """Get device profile and recommendations."""
        ...

    def benchmark_endpoint(
        self,
        endpoint: str,
        count: int = 10,
    ) -> dict[str, Any]:
        """Benchmark a specific API endpoint."""
        ...
