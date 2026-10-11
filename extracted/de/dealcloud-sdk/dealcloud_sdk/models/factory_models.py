"""
Factory models for DealCloud configuration.

Supports two configuration formats:
1. Legacy format: simple site_url, client_id, client_secret
2. Full configuration format (recommended): complete configuration with retry, pagination, concurrency settings
"""

from typing import Dict, Optional, Tuple

import fsspec
from pydantic import BaseModel, Field


# =============================================================================
# Query/Pagination Settings
# =============================================================================

class QuerySettings(BaseModel):
    """Query and pagination settings."""
    pageSize: int = Field(default=1000, description="Default page size for reads")
    cellPaginationLimit: int = Field(default=9000, description="Max cells per write request")
    deletePageSize: int = Field(
        default=5000, 
        ge=1, 
        le=10000,
        description="Max records per delete batch (default: 5000, max: 10000)"
    )


# =============================================================================
# Concurrency Limits
# =============================================================================

class ConcurrencyLimits(BaseModel):
    """
    Concurrency limits for parallel operations.
    
    Separate limits for each operation type allows fine-tuning:
    - read: Higher concurrency OK (read-only)
    - create/update: Lower to avoid conflicts
    - delete: Lower to avoid cascade issues
    
    Note: DealCloud API limits Data endpoints to 5 requests/second.
    Defaults are set to 2 for safety. Values > 5 may trigger 429 errors.
    """
    read: int = Field(
        default=2, 
        description="Max parallel read requests (should be ≤ 5 to respect API limits)"
    )
    delete: int = Field(
        default=2, 
        description="Max parallel delete requests (should be ≤ 5 to respect API limits)"
    )
    create: int = Field(
        default=2, 
        description="Max parallel create/update requests (should be ≤ 5 to respect API limits)"
    )


# =============================================================================
# Response Retry Settings
# =============================================================================

class ResponseRetrySettings(BaseModel):
    """
    Per-status-code retry settings.
    
    This is superior to the legacy Python SDK approach of using a single
    MAX_RETRIES value for all status codes. Different errors warrant
    different retry strategies:
    
    - 429 (Too Many Requests): More retries - rate limits are temporary
    - 500 (Internal Server Error): Fewer retries - may be permanent bug
    - 503 (Service Unavailable): Medium retries - usually temporary
    
    These values should NOT be extremely high (like 100000 in the old SDK).
    Modern best practice is reasonable retry counts with proper backoff.
    """
    tooManyRequests: int = Field(default=5, ge=0, le=20, description="Retries for HTTP 429")
    internalServerError: int = Field(default=2, ge=0, le=10, description="Retries for HTTP 500")
    serviceUnavailable: int = Field(default=2, ge=0, le=10, description="Retries for HTTP 503")
    badGateway: int = Field(default=2, ge=0, le=10, description="Retries for HTTP 502")
    gatewayTimeout: int = Field(default=2, ge=0, le=10, description="Retries for HTTP 504")
    backoffFactor: float = Field(default=2.0, ge=1.0, le=10.0, description="Exponential backoff multiplier")
    maxBackoffSeconds: float = Field(default=300.0, ge=1.0, description="Maximum wait between retries")
    
    def to_retry_count_by_status(self) -> Dict[int, int]:
        """Convert to retry_count_by_status dict for RetryConfig."""
        return {
            429: self.tooManyRequests,
            500: self.internalServerError,
            502: self.badGateway,
            503: self.serviceUnavailable,
            504: self.gatewayTimeout,
        }


# =============================================================================
# Full Configuration Format
# =============================================================================

class DealCloudConfig(BaseModel):
    """
    Full DealCloud configuration.
    
    Example JSON:
    {
        "siteUrl": "client.dealcloud.com",
        "clientId": "1018649",
        "clientSecret": "secret",
        "connectorTimeoutSeconds": 100,
        "querySettings": {
            "pageSize": 1000,
            "cellPaginationLimit": 9000,
            "deletePageSize": 5000
        },
        "concurrencyLimits": {
            "read": 2,
            "delete": 2,
            "create": 2
        },
        "responseRetrySettings": {
            "tooManyRequests": 5,
            "internalServerError": 2,
            "badGateway": 2,
            "serviceUnavailable": 2,
            "gatewayTimeout": 2,
            "backoffFactor": 2.0,
            "maxBackoffSeconds": 300.0
        }
    }
    """
    siteUrl: str = Field(..., description="DealCloud site URL (e.g., client.dealcloud.com)")
    clientId: str = Field(..., description="API client ID")
    clientSecret: str = Field(..., description="API client secret")
    scope: Tuple[str, ...] = Field(
        default=("data", "user_management"),
        description="OAuth2 scopes (e.g. data, user_management)",
    )
    connectorTimeoutSeconds: int = Field(default=100, description="Request timeout in seconds")
    querySettings: QuerySettings = Field(default_factory=QuerySettings)
    concurrencyLimits: ConcurrencyLimits = Field(default_factory=ConcurrencyLimits)
    responseRetrySettings: ResponseRetrySettings = Field(default_factory=ResponseRetrySettings)
    raiseOnRowErrors: bool = Field(
        default=False,
        description="Default raise_on_row_errors for write methods when the parameter is omitted",
    )
    
    @classmethod
    def from_json_file(cls, path: str) -> "DealCloudConfig":
        """Load configuration from JSON file (local path or URI via fsspec)."""
        import json

        with fsspec.open(path, 'r') as f:
            return cls(**json.load(f))

    @classmethod
    def from_yaml_file(cls, path: str) -> "DealCloudConfig":
        """Load configuration from YAML file (local path or URI via fsspec)."""
        import yaml

        with fsspec.open(path, 'r') as f:
            return cls(**yaml.safe_load(f))


# =============================================================================
# Legacy Python SDK Format (for backwards compatibility)
# =============================================================================

class DealCloudFactoryArgs(BaseModel):
    """
    Arguments for DealCloud factory methods (legacy Python SDK format).
    
    For simple use cases. For full configuration, use DealCloudConfig.
    """
    site_url: str
    client_id: str
    client_secret: str
    scope: Tuple[str, ...] = ("data", "user_management")

    def to_config(self) -> DealCloudConfig:
        """Convert to full DealCloudConfig with defaults."""
        return DealCloudConfig(
            siteUrl=self.site_url,
            clientId=self.client_id,
            clientSecret=self.client_secret,
            scope=self.scope,
        )


