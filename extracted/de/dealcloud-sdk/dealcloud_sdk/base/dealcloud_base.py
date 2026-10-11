"""Base DealCloud class with authentication (using intapp_rest_client)."""

import logging
from typing import Optional, Union

from intapp_rest_client import OAuth2Config, RetryConfig

from ..http.dealcloud_rest_client import DealCloudRestClient

# SDK HTTP client subclass (normalizes plain-text API errors to dicts). Unit tests patch this name.
RestClient = DealCloudRestClient

from .._version import SDK_VERSION
from ..constants.auth import DEFAULT_SCOPE, AvailableScopeTypes
from ..constants.request import (
    BACKOFF_FACTOR,
    RETRY_COUNT_BY_STATUS,
    MAX_BACKOFF_SECONDS,
    DEFAULT_TIMEOUT_SECONDS,
)
from ..constants.env_var_names import (
    CLIENT_ID_ENV_NAME,
    CLIENT_SECRET_ENV_NAME,
    SITE_URL_ENV_NAME,
)
from ..factories.from_env import dc_from_environment_variables, normalize_site_url
from ..factories.from_json import dc_from_json_config
from ..factories.from_yaml import dc_from_yaml_config
from ..models.factory_models import DealCloudConfig, DealCloudFactoryArgs


class DealCloudBase:
    """
    Base of the linear inheritance chain. Each class in the chain has one parent;
    the order is for composition (one DealCloud client gets all features), not a
    logical dependency. This approach avoids explicit mixins.
    DealCloudBase provides base authentication and URL building.
    
    Uses ``DealCloudRestClient`` (subclass of ``intapp_rest_client.RestClient``) for HTTP;
    non-JSON error bodies are normalized to ApiResult-like dicts on ``HttpError``.
    
    Supports two initialization modes:
    1. Direct parameters (legacy Python SDK style)
    2. DealCloudConfig object (matches .NET SDK JSON format)
    """

    def __init__(
        self,
        site_url: Optional[str] = None,
        client_id: Optional[Union[str, int]] = None,
        client_secret: Optional[str] = None,
        scope: AvailableScopeTypes = DEFAULT_SCOPE,
        refresh_id_maps: bool = True,
        config: Optional[DealCloudConfig] = None,
    ):
        """
        Initialize DealCloudBase.
        
        Args:
            site_url: DealCloud site (e.g., "client.dealcloud.com")
            client_id: API client ID
            client_secret: API client secret
            scope: Authentication scopes
            refresh_id_maps: Whether to refresh ID maps on data operations
            config: Full DealCloudConfig (if provided, overrides individual params)
        
        Example with config (.NET SDK format):
            config = DealCloudConfig.from_json_file("dealcloud.json")
            dc = DealCloud(config=config)
        
        Example with params (legacy Python SDK format):
            dc = DealCloud(
                site_url="client.dealcloud.com",
                client_id="1018649",
                client_secret="secret"
            )
        
        Note on OpenTelemetry:
            For distributed tracing, use opentelemetry-instrumentation-httpx
            which automatically instruments all HTTPX requests. See README.md
            for setup instructions.
        """
        self._logger = logging.getLogger(__name__)
        
        # Use config if provided, otherwise build from individual params
        if config:
            self._config = config
            self._site = normalize_site_url(config.siteUrl)
            self._client_id = config.clientId
            self._client_secret = config.clientSecret
            timeout = float(config.connectorTimeoutSeconds)
            
            # Extract retry settings from config using helper method
            retry_settings = config.responseRetrySettings
            self._status_retry_map = retry_settings.to_retry_count_by_status()
            backoff = retry_settings.backoffFactor
            max_backoff = retry_settings.maxBackoffSeconds
            
            # Store concurrency limits
            self._concurrency_limits = config.concurrencyLimits
            
            # Store query settings
            self._query_settings = config.querySettings
            self._raise_on_row_errors_default = config.raiseOnRowErrors
            scope = config.scope
        else:
            if not all([site_url, client_id, client_secret]):
                raise ValueError("Must provide either config or site_url/client_id/client_secret")
            
            self._config = None
            self._site = normalize_site_url(site_url)
            self._client_id = client_id
            self._client_secret = client_secret
            timeout = float(DEFAULT_TIMEOUT_SECONDS)
            
            # Use default constants from request.py
            self._status_retry_map = RETRY_COUNT_BY_STATUS.copy()
            backoff = BACKOFF_FACTOR
            max_backoff = MAX_BACKOFF_SECONDS
            
            # Use default concurrency/query settings
            self._concurrency_limits = None
            self._query_settings = None
            self._raise_on_row_errors_default = False
            # scope already set from parameter (default DEFAULT_SCOPE)

        self._scope = " ".join(scope)
        self._refresh_id_maps = refresh_id_maps
        
        # Base URL roots (v4 and v1)
        self._url_root = f"https://{self._site}/api/rest/v4"
        self._url_root_v1 = f"https://{self._site}/api/rest/v1"

        # API base URLs (each starts with https://{site})
        self._schema_url = f"https://{self._site}/api/rest/v4/schema"
        self._data_url = f"https://{self._site}/api/rest/v4/data"
        self._entrydata_url = f"https://{self._site}/api/rest/v4/data/entrydata"
        self._rows_url = f"https://{self._site}/api/rest/v4/data/entrydata/rows"
        self._query_url = f"https://{self._site}/api/rest/v4/data/entrydata/rows/query"
        self._views_url = f"https://{self._site}/api/rest/v4/data/rows/view"
        self._history_url = f"https://{self._site}/api/rest/v4/data/entrydata"
        self._cells_url = f"https://{self._site}/api/rest/v4/data/entrydata"
        self._files_url = f"https://{self._site}/api/rest/v4/data/entryfiles"
        self._merge_url = f"https://{self._site}/api/rest/v4/data/merge"
        self._usermgmt_url = f"https://{self._site}/api/rest/v1/management/user"
        self._backups_url = f"https://{self._site}/api/rest/v4/backups"
        self._publications_url = f"https://{self._site}/api/rest/v1/publication"
        self._ri_url = f"https://{self._site}/api/rest/v4/ri/import"

        # Initialize REST client with OAuth2
        # Use max of status-specific retries for the global max
        max_retries = max(self._status_retry_map.values())
        
        self._client = RestClient(
            base_url=f"https://{self._site}/",
            oauth2_config=OAuth2Config(
                token_url=f"{self._url_root_v1}/oauth/token",
                client_id=str(self._client_id),
                client_secret=self._client_secret,
                scope=self._scope,
                token_refresh_margin=120  # Match real SDK: expires_in - 120
            ),
            retry_config=RetryConfig(
                max_retries=max_retries,
                backoff_factor=backoff,
                retryable_statuses=tuple(self._status_retry_map.keys()),
                retry_count_by_status=self._status_retry_map,
                max_backoff=max_backoff,
            ),
            timeout=timeout,
            # Add DealCloud SDK version header
            headers={"X-Dealcloud-Sdk-Version": SDK_VERSION},
        )
        # Compatibility: some intapp_rest_client versions use .logger, others ._logger
        if not hasattr(self._client, "_logger") and hasattr(self._client, "logger"):
            self._client._logger = self._client.logger

        self._logger.debug("Validating credentials")
        # Validate credentials by triggering token fetch
        self._client._get_auth_headers_sync()
        self._logger.debug("Credentials validated")
        
        # Store schema and user map (populated by subclass)
        self._site_schema = None
        self._user_map: dict = {}
        self._id_map: dict = {}
    
    # =========================================================================
    # Helper Properties for Config Values
    # =========================================================================
    
    @property
    def page_size(self) -> int:
        """Get configured page size for reads."""
        if self._query_settings:
            return self._query_settings.pageSize
        return 1000  # Default
    
    @property
    def cell_pagination_limit(self) -> int:
        """Get configured cell pagination limit for writes."""
        if self._query_settings:
            return self._query_settings.cellPaginationLimit
        return 9000  # Default
    
    @property
    def delete_page_size(self) -> int:
        """
        Get configured page size for deletes.
        
        Default: 10000 (API max)
        Max: 10000 (API limit)
        """
        if self._query_settings:
            page_size = self._query_settings.deletePageSize
            # Enforce max limit
            if page_size > 10000:
                import warnings
                warnings.warn(
                    f"deletePageSize {page_size} exceeds maximum of 10000. Using 10000.",
                    UserWarning
                )
                return 10000
            return page_size
        return 10000  # Default (API max)
    
    @property
    def read_concurrency(self) -> int:
        """
        Get configured concurrency limit for reads.
        
        Note: DealCloud API limits Data endpoints to 5 requests/second.
        Default is 4 to provide a safety margin.
        """
        if self._concurrency_limits:
            return self._concurrency_limits.read
        return 4  # Default - respects 5/second API limit with safety margin
    
    @property
    def delete_concurrency(self) -> int:
        """
        Get configured concurrency limit for deletes.
        
        Note: DealCloud API limits Data endpoints to 5 requests/second.
        Default is 4 to provide a safety margin.
        """
        if self._concurrency_limits:
            return self._concurrency_limits.delete
        return 4  # Default - respects 5/second API limit with safety margin
    
    @property
    def create_concurrency(self) -> int:
        """
        Get configured concurrency limit for creates/updates.
        
        Note: DealCloud API limits Data endpoints to 5 requests/second.
        Default is 4 to provide a safety margin.
        """
        if self._concurrency_limits:
            return self._concurrency_limits.create
        return 4  # Default - respects 5/second API limit with safety margin
    
    # =========================================================================
    # Read-Only State Properties
    # =========================================================================
    
    @property
    def site_url(self) -> str:
        """
        Get the DealCloud site URL.
        
        Returns the site hostname used for all API requests.
        
        Returns:
            str: Site URL (e.g., "client.dealcloud.com")
        
        Example:
            >>> dc = DealCloud.from_env()
            >>> print(f"Connected to: {dc.site_url}")
            Connected to: client.dealcloud.com
        """
        return self._site
    
    @property
    def api_url(self) -> str:
        """
        Get the base API URL for v4 endpoints.
        
        Use this for constructing custom endpoint URLs when needed.
        
        Returns:
            str: Full API URL (e.g., "https://client.dealcloud.com/api/rest/v4")
        
        Example:
            >>> dc = DealCloud.from_env()
            >>> custom_url = f"{dc.api_url}/custom/endpoint"
            >>> print(custom_url)
            https://client.dealcloud.com/api/rest/v4/custom/endpoint
        """
        return self._url_root
    
    @property
    def api_url_v1(self) -> str:
        """
        Get the base API URL for v1 endpoints.
        
        Use this for accessing legacy v1 API endpoints not available in v4.
        
        Returns:
            str: Full v1 API URL (e.g., "https://client.dealcloud.com/api/rest/v1")
        
        Example:
            >>> dc = DealCloud.from_env()
            >>> legacy_url = f"{dc.api_url_v1}/oauth/token"
            >>> print(legacy_url)
            https://client.dealcloud.com/api/rest/v1/oauth/token
        """
        return self._url_root_v1
    
    @property
    def schema_url(self) -> str:
        """
        Get the Schema API base URL.
        
        Equivalent to `{api_url}/schema`. Use for custom schema operations.
        
        Returns:
            str: Schema API URL (e.g., "https://client.dealcloud.com/api/rest/v4/schema")
        
        Example:
            >>> url = f"{dc.schema_url}/objects"
            >>> response = dc.client.get(url)
        """
        return self._schema_url
    
    @property
    def data_url(self) -> str:
        """
        Get the Data API base URL.
        
        Equivalent to `{api_url}/data`. Use for custom data operations.
        
        Returns:
            str: Data API URL (e.g., "https://client.dealcloud.com/api/rest/v4/data")
        
        Example:
            >>> url = f"{dc.data_url}/bulk"
            >>> response = dc.client.post(url, json=payload)
        """
        return self._data_url
    
    @property
    def entrydata_url(self) -> str:
        """
        Get the Entry Data API base URL.
        
        Equivalent to `{data_url}/entrydata`. Use for cell-level operations.
        
        Returns:
            str: Entry Data URL (e.g., "https://client.dealcloud.com/api/rest/v4/data/entrydata")
        
        Example:
            >>> url = f"{dc.entrydata_url}/{object_id}/{entry_id}"
            >>> response = dc.client.get(url)
        """
        return self._entrydata_url
    
    @property
    def rows_url(self) -> str:
        """
        Get the Rows API base URL.
        
        Equivalent to `{entrydata_url}/rows`. Use for row-level operations.
        
        Returns:
            str: Rows URL (e.g., "https://client.dealcloud.com/api/rest/v4/data/entrydata/rows")
        
        Example:
            >>> url = f"{dc.rows_url}/{object_id}"
            >>> response = dc.client.get(url, params={"pageSize": 100})
        """
        return self._rows_url
    
    @property
    def query_url(self) -> str:
        """
        Get the Query API base URL.
        
        Equivalent to `{rows_url}/query`. Use for filtered data queries.
        
        Returns:
            str: Query URL (e.g., "https://client.dealcloud.com/api/rest/v4/data/entrydata/rows/query")
        
        Example:
            >>> url = f"{dc.query_url}/{object_id}"
            >>> response = dc.client.post(url, json={"filters": [...]})
        """
        return self._query_url
    
    @property
    def views_url(self) -> str:
        """
        Get the Views API base URL.
        
        Equivalent to `{data_url}/rows/view`. Use for view-based data access.
        
        Returns:
            str: Views URL (e.g., "https://client.dealcloud.com/api/rest/v4/data/rows/view")
        
        Example:
            >>> url = f"{dc.views_url}/{view_id}"
            >>> response = dc.client.get(url)
        """
        return self._views_url
    
    @property
    def auth_scope(self) -> str:
        """
        Get the OAuth2 scope string used for authentication.
        
        Returns the space-separated scope string configured at initialization.
        
        Returns:
            str: OAuth2 scope string (e.g., "data schema files users")
        
        Example:
            >>> print(f"Authenticated with scopes: {dc.auth_scope}")
            Authenticated with scopes: data schema files users
        """
        return self._scope
    
    @property
    def refresh_id_maps(self) -> bool:
        """
        Get whether ID maps are refreshed during data operations.
        
        When True, reference ID mappings are refreshed during read operations
        to ensure accurate name resolution.
        
        Returns:
            bool: True if ID maps are refreshed automatically
        
        Example:
            >>> if dc.refresh_id_maps:
            ...     print("ID maps will be refreshed during reads")
        """
        return self._refresh_id_maps
    
    @property
    def retry_status_codes(self) -> dict:
        """
        Get the HTTP status code to retry count mapping.
        
        Returns a dict mapping HTTP status codes to the number of retries
        allowed for that status. Modify to adjust retry behavior.
        
        Returns:
            dict: Mapping of status_code (int) to retry_count (int)
        
        Example:
            >>> # Check retry config
            >>> print(dc.retry_status_codes)
            {429: 5, 500: 3, 502: 3, 503: 3, 504: 3}
            
            >>> # Increase retries for rate limiting
            >>> dc.retry_status_codes[429] = 10
        """
        return self._status_retry_map
    
    @property
    def concurrency_limits(self) -> Optional["ConcurrencyLimits"]:
        """
        Get the concurrency limits configuration.
        
        Returns the ConcurrencyLimits object if configured, None otherwise.
        Modify to dynamically adjust parallelism for operations.
        
        Returns:
            Optional[ConcurrencyLimits]: Concurrency settings or None
        
        Example:
            >>> # Check current limits
            >>> if dc.concurrency_limits:
            ...     print(f"Read concurrency: {dc.concurrency_limits.read}")
            
            >>> # Increase read parallelism dynamically
            >>> if dc.concurrency_limits:
            ...     dc.concurrency_limits.read = 16
        
        Note:
            Changes take effect on subsequent operations.
            Use read_concurrency, delete_concurrency, create_concurrency
            properties for safe access with defaults.
        """
        return self._concurrency_limits
    
    @property
    def query_settings(self) -> Optional["QuerySettings"]:
        """
        Get the query/pagination settings configuration.
        
        Returns the QuerySettings object if configured, None otherwise.
        Modify to dynamically adjust pagination behavior.
        
        Returns:
            Optional[QuerySettings]: Query settings or None
        
        Example:
            >>> # Check current settings
            >>> if dc.query_settings:
            ...     print(f"Page size: {dc.query_settings.pageSize}")
            
            >>> # Reduce page size for memory-constrained environment
            >>> if dc.query_settings:
            ...     dc.query_settings.pageSize = 500
        
        Note:
            Changes take effect on subsequent operations.
            Use page_size, cell_pagination_limit, delete_page_size
            properties for safe access with defaults.
        """
        return self._query_settings
    
    @property
    def client(self) -> RestClient:
        """
        Get the underlying REST client for direct API access.
        
        Use this for advanced scenarios where you need direct HTTP access
        with the same authentication, retries, and logging as the SDK.
        
        Returns:
            DealCloudRestClient: Authenticated client (``intapp_rest_client.RestClient`` subclass).
        
        Example:
            >>> # Make a raw request to an undocumented endpoint
            >>> response = dc.client.get("/api/rest/v4/admin/settings")
            
            >>> # Use auth headers with another library
            >>> headers = dc.client.get_auth_headers()
            >>> requests.get(other_url, headers=headers)
        
        Warning:
            Direct client access bypasses SDK-level features like
            schema caching and reference resolution. Use sparingly.
        """
        return self._client
    
    @property
    def cached_schema(self) -> Optional[dict]:
        """
        Get the cached site schema, if available.
        
        Returns the schema that was loaded via refresh_schema() or
        auto-loaded during operations. Returns None if not yet loaded.
        
        Returns:
            Optional[dict]: Cached schema or None
        
        Example:
            >>> # Check if schema is cached
            >>> if dc.cached_schema:
            ...     objects = dc.cached_schema.get("objects", [])
            ...     print(f"Schema has {len(objects)} objects")
            ... else:
            ...     dc.refresh_schema()
            
            >>> # Access cached schema for lookup
            >>> schema = dc.cached_schema
            >>> company_obj = next(
            ...     (o for o in schema["objects"] if o["apiName"] == "Company"),
            ...     None
            ... )
        
        Note:
            Call refresh_schema() to populate if needed.
        """
        return self._site_schema
    
    @property
    def cached_user_map(self) -> dict:
        """
        Get the cached user ID to name mapping.
        
        Returns the user map populated during operations that resolve
        user references. Empty dict if not yet populated.
        
        Returns:
            dict: Mapping of user_id (int) to user_name (str)
        
        Example:
            >>> # Check cached users
            >>> users = dc.cached_user_map
            >>> if 12345 in users:
            ...     print(f"User 12345 is: {users[12345]}")
            
            >>> # Use for ID resolution
            >>> df["OwnerName"] = df["OwnerId"].map(dc.cached_user_map)
        
        Note:
            This map is populated automatically during read_data() operations
            when user fields are encountered and resolve_references is enabled.
        """
        return self._user_map
    
    @property
    def cached_id_map(self) -> dict:
        """
        Get the cached ID mapping for all objects.
        
        Contains reference ID to name mappings built during operations
        that resolve references. Organized by object type.
        
        Returns:
            dict: Nested mapping of object_name -> entry_id -> entry_name
        
        Example:
            >>> id_map = dc.cached_id_map
            >>> if "Company" in id_map:
            ...     company_names = id_map["Company"]
            ...     name = company_names.get(12345, "Unknown")
        
        Note:
            This map is populated during read_data() with resolve_references=True.
        """
        return self._id_map
    
    # =========================================================================
    # Factory Methods (matching real SDK exactly)
    # =========================================================================
    
    @classmethod
    def from_env(
        cls,
        site_url_env_name: str = SITE_URL_ENV_NAME,
        client_id_env_name: str = CLIENT_ID_ENV_NAME,
        client_secret_env_name: str = CLIENT_SECRET_ENV_NAME,
        scope: AvailableScopeTypes = DEFAULT_SCOPE,
        connector_timeout_env_name: Optional[str] = None,
        query_page_size_env_name: Optional[str] = None,
        query_cell_pagination_limit_env_name: Optional[str] = None,
        query_delete_page_size_env_name: Optional[str] = None,
        concurrency_limit_read_env_name: Optional[str] = None,
        concurrency_limit_delete_env_name: Optional[str] = None,
        concurrency_limit_create_env_name: Optional[str] = None,
        retry_too_many_requests_env_name: Optional[str] = None,
        retry_internal_server_error_env_name: Optional[str] = None,
        retry_service_unavailable_env_name: Optional[str] = None,
        retry_bad_gateway_env_name: Optional[str] = None,
        retry_gateway_timeout_env_name: Optional[str] = None,
        retry_backoff_factor_env_name: Optional[str] = None,
        retry_max_backoff_seconds_env_name: Optional[str] = None,
    ):
        """
        Create from environment variables.
        
        Supports all configuration options via environment variables. If only
        credentials are provided, uses defaults for other settings. If any optional
        settings are provided, uses those values.
        """
        from ..constants.env_var_names import (
            CONNECTOR_TIMEOUT_SECONDS_ENV_NAME,
            QUERY_PAGE_SIZE_ENV_NAME,
            QUERY_CELL_PAGINATION_LIMIT_ENV_NAME,
            QUERY_DELETE_PAGE_SIZE_ENV_NAME,
            CONCURRENCY_LIMIT_READ_ENV_NAME,
            CONCURRENCY_LIMIT_DELETE_ENV_NAME,
            CONCURRENCY_LIMIT_CREATE_ENV_NAME,
            RETRY_TOO_MANY_REQUESTS_ENV_NAME,
            RETRY_INTERNAL_SERVER_ERROR_ENV_NAME,
            RETRY_SERVICE_UNAVAILABLE_ENV_NAME,
            RETRY_BAD_GATEWAY_ENV_NAME,
            RETRY_GATEWAY_TIMEOUT_ENV_NAME,
            RETRY_BACKOFF_FACTOR_ENV_NAME,
            RETRY_MAX_BACKOFF_SECONDS_ENV_NAME,
        )
        
        # Use provided env names or defaults
        config_result = dc_from_environment_variables(
            site_url_env_name=site_url_env_name,
            client_id_env_name=client_id_env_name,
            client_secret_env_name=client_secret_env_name,
            scope=scope,
            connector_timeout_env_name=connector_timeout_env_name or CONNECTOR_TIMEOUT_SECONDS_ENV_NAME,
            query_page_size_env_name=query_page_size_env_name or QUERY_PAGE_SIZE_ENV_NAME,
            query_cell_pagination_limit_env_name=query_cell_pagination_limit_env_name or QUERY_CELL_PAGINATION_LIMIT_ENV_NAME,
            query_delete_page_size_env_name=query_delete_page_size_env_name or QUERY_DELETE_PAGE_SIZE_ENV_NAME,
            concurrency_limit_read_env_name=concurrency_limit_read_env_name or CONCURRENCY_LIMIT_READ_ENV_NAME,
            concurrency_limit_delete_env_name=concurrency_limit_delete_env_name or CONCURRENCY_LIMIT_DELETE_ENV_NAME,
            concurrency_limit_create_env_name=concurrency_limit_create_env_name or CONCURRENCY_LIMIT_CREATE_ENV_NAME,
            retry_too_many_requests_env_name=retry_too_many_requests_env_name or RETRY_TOO_MANY_REQUESTS_ENV_NAME,
            retry_internal_server_error_env_name=retry_internal_server_error_env_name or RETRY_INTERNAL_SERVER_ERROR_ENV_NAME,
            retry_service_unavailable_env_name=retry_service_unavailable_env_name or RETRY_SERVICE_UNAVAILABLE_ENV_NAME,
            retry_bad_gateway_env_name=retry_bad_gateway_env_name or RETRY_BAD_GATEWAY_ENV_NAME,
            retry_gateway_timeout_env_name=retry_gateway_timeout_env_name or RETRY_GATEWAY_TIMEOUT_ENV_NAME,
            retry_backoff_factor_env_name=retry_backoff_factor_env_name or RETRY_BACKOFF_FACTOR_ENV_NAME,
            retry_max_backoff_seconds_env_name=retry_max_backoff_seconds_env_name or RETRY_MAX_BACKOFF_SECONDS_ENV_NAME,
        )
        
        # Convert to DealCloudConfig if needed
        if isinstance(config_result, DealCloudConfig):
            config = config_result
        else:
            config = config_result.to_config()
        
        return cls(config=config)
    
    @classmethod
    def from_json(
        cls,
        json_file_path: str,
        json_path_to_credentials: Optional[str] = None,
        scope: AvailableScopeTypes = DEFAULT_SCOPE,
    ):
        """
        Create from JSON config file.
        
        Supports two formats with auto-detection:
        
        1. Legacy format (simple credentials):
            {
                "site_url": "client.dealcloud.com",
                "client_id": "12345",
                "client_secret": "secret"
            }
        
        2. Full configuration format:
            {
                "siteUrl": "client.dealcloud.com",
                "clientId": "12345",
                "clientSecret": "secret",
                "connectorTimeoutSeconds": 100,
                "responseRetrySettings": {...},
                "querySettings": {...},
                "concurrencyLimits": {...}
            }
        
        .. deprecated:: Use `from_config()` for full configuration files.
           This method is primarily for legacy format support and nested configuration paths.
        
        Args:
            json_file_path: Path to JSON config file
            json_path_to_credentials: Optional dot notation path to credentials
        
        Returns:
            DealCloud instance with configuration applied
        """
        import warnings
        result = dc_from_json_config(
            json_file_path, json_path_to_credentials, scope=scope
        )

        if isinstance(result, DealCloudConfig):
            # Full config format detected - recommend from_config()
            warnings.warn(
                "Full configuration format detected. Use DealCloud.from_config() instead of from_json() "
                "for full configuration files. from_json() is primarily for legacy format support.",
                DeprecationWarning,
                stacklevel=2
            )
            return cls(config=result)
        else:
            # Legacy format - use individual params
            return cls(
                result.site_url,
                result.client_id,
                result.client_secret,
            )
    
    @classmethod
    def from_yaml(
        cls,
        yaml_file_path: str,
        yaml_path_to_credentials: Optional[str] = None,
        scope: AvailableScopeTypes = DEFAULT_SCOPE,
    ):
        """
        Create from YAML config file.
        
        Supports two formats with auto-detection:
        
        1. Legacy format (simple credentials):
            site_url: client.dealcloud.com
            client_id: "12345"
            client_secret: secret
        
        2. Full configuration format:
            siteUrl: client.dealcloud.com
            clientId: "12345"
            clientSecret: secret
            connectorTimeoutSeconds: 100
            responseRetrySettings:
                tooManyRequests: 5
                backoffFactor: 2.0
            querySettings:
                pageSize: 1000
            concurrencyLimits:
                read: 2
        
        .. deprecated:: Use `from_config()` for full configuration files.
           This method is primarily for legacy format support and nested configuration paths.
        
        Args:
            yaml_file_path: Path to YAML config file
            yaml_path_to_credentials: Optional dot notation path to credentials
        
        Returns:
            DealCloud instance with configuration applied
        """
        import warnings
        result = dc_from_yaml_config(
            yaml_file_path, yaml_path_to_credentials, scope=scope
        )

        if isinstance(result, DealCloudConfig):
            # Full config format detected - recommend from_config()
            warnings.warn(
                "Full configuration format detected. Use DealCloud.from_config() instead of from_yaml() "
                "for full configuration files. from_yaml() is primarily for legacy format support.",
                DeprecationWarning,
                stacklevel=2
            )
            return cls(config=result)
        else:
            # Legacy format - use individual params
            return cls(
                result.site_url,
                result.client_id,
                result.client_secret,
            )
    
    @classmethod
    def from_config(cls, config_path: str):
        """
        Create from JSON/YAML config file (RECOMMENDED).
        
        This is the preferred method for production use as it provides
        full control over retry settings, concurrency, and pagination.
        Automatically detects JSON or YAML format by file extension.
        
        Example config file (JSON or YAML):
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
                "serviceUnavailable": 2,
                "backoffFactor": 2
            }
        }
        
        Args:
            config_path: Path to JSON or YAML config file (extension determines format)
            
        Returns:
            DealCloud instance with full configuration
        """
        if config_path.endswith('.yaml') or config_path.endswith('.yml'):
            config = DealCloudConfig.from_yaml_file(config_path)
        else:
            config = DealCloudConfig.from_json_file(config_path)
        
        return cls(config=config)
    
    @classmethod
    def from_config_object(cls, config: DealCloudConfig):
        """
        Create from DealCloudConfig object.
        
        Useful when configuration is built programmatically:
        
            from dealcloud_sdk.models import DealCloudConfig, ResponseRetrySettings
            
            config = DealCloudConfig(
                siteUrl="client.dealcloud.com",
                clientId="1018649",
                clientSecret="secret",
                connectorTimeoutSeconds=100,
                responseRetrySettings=ResponseRetrySettings(
                    tooManyRequests=10,  # Higher retry for rate limits
                    backoffFactor=3
                )
            )
            dc = DealCloud.from_config_object(config)
        
        Args:
            config: DealCloudConfig instance
            
        Returns:
            DealCloud instance with full configuration
        """
        return cls(config=config)
    
    def get_schema(self):
        """Placeholder - implemented by DealCloudSchema."""
        pass
    
    def get_users(self):
        """Placeholder - implemented by DealCloudSchema."""
        pass
    
    def close(self) -> None:
        """Close underlying HTTP client."""
        self._client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()


