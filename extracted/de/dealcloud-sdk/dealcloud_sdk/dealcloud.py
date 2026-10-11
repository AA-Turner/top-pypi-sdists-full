"""Main DealCloud class (matching real SDK entry point)."""

from typing import Optional, Union

from .constants.auth import DEFAULT_SCOPE, AvailableScopeTypes
from .merge.dealcloud_merge import DealCloudMerge
from .models.factory_models import DealCloudConfig
from .utils.schema_cache import get_schema_cache


class DealCloud(DealCloudMerge):
    """
    DealCloud API client. Top of the linear inheritance chain; each layer has one
    parent and the order is for composition (one client gets all features), not
    dependency. This avoids explicit mixins.
    This class provides the main entry point for interacting with the DealCloud API.
    It inherits from the complete API chain providing all available operations:
    
    Class Hierarchy:
        DealCloud
            └── DealCloudMerge (merge operations)
                └── DealCloudRelationshipIntelligence (RI operations)
                    └── DealCloudBackups (backup operations)
                        └── DealCloudPublications (event streaming)
                            └── DealCloudUserManagement (user operations)
                                └── DealCloudFiles (file upload/download)
                                    └── DealCloudHistory (audit trail)
                                        └── DealCloudCells (cell-level data)
                                            └── DealCloudData (rows CRUD)
                                                └── DealCloudReports (template reports)
                                                    └── DealCloudSchema (schema operations)
                                                        └── DealCloudBase (auth, URLs)
    
    API Categories:
        - Schema: get_users(), get_schema(), get_fields(), get_objects()
        - Data (Rows): read_data(), query_data(), insert_data(), update_data(), delete_data()
        - Cells: get_cells(), write_cells(), list_entries()
        - History: get_history(), get_historical_data()
        - Files: upload_attachment(), upload_file_to_entry_field(), download_file(), delete_file()
        - User Management: create_user(), get_user_groups(), invite_users()
        - Publications: get_topics(), poll_events(), acknowledge_topic_offsets(), subscribe()
        - Backups: request_backup(), download_backup(), list_backups()
        - Relationship Intelligence: import_emails(), import_meetings()
        - Merge: merge_entries()
        - Template Reports: get_report_templates(), generate_report(), get_report_status()
    
    Example (simple initialization):
        dc = DealCloud(
            site_url="client.dealcloud.com",
            client_id="12345",
            client_secret="your_client_secret",
        )
        
        # Schema operations
        users = dc.get_users()
        schema = dc.get_schema()
        
        # Data operations
        data = dc.read_data("Company", output="pandas", resolve="name")
        dc.delete_data("Company", [123, 456])
        
        # Cell operations
        cells = dc.get_cells("Company", entry_ids=[123])
        
        # File operations
        dc.download_file(123, "Logo", output_path="./logo.png")
        
        # User management
        user = dc.create_user("new@example.com", "John", "Doe")
        
        # Merge duplicates
        dc.merge_entries("Company", winner_entry_id=123, loser_entry_ids=[456])
    
    Example (with full config - RECOMMENDED for production):
        dc = DealCloud.from_config("dealcloud_config.json")
        
        # Or programmatically:
        from dealcloud_sdk.models import DealCloudConfig, ResponseRetrySettings
        
        config = DealCloudConfig(
            siteUrl="client.dealcloud.com",
            clientId="12345",
            clientSecret="secret",
            connectorTimeoutSeconds=120,
            responseRetrySettings=ResponseRetrySettings(
                tooManyRequests=10,  # More retries for rate limits
                backoffFactor=3.0
            )
        )
        dc = DealCloud.from_config_object(config)
    
    Example (with schema caching):
        # Schema is cached by default for 5 minutes
        dc1 = DealCloud(site_url="site.dealcloud.com", ...)
        # Second client reuses cached schema
        dc2 = DealCloud(site_url="site.dealcloud.com", ...)
        
        # Disable caching
        dc = DealCloud(site_url="site.dealcloud.com", ..., cache_schema=False)
        
        # Custom cache TTL
        dc = DealCloud(site_url="site.dealcloud.com", ..., schema_cache_ttl=600)
    
    Example (context manager):
        with DealCloud(site_url="client.dealcloud.com", ...) as dc:
            data = dc.read_data("Company")
        # Connection automatically closed
    
    Example (event subscription):
        def handle_event(event):
            print(f"Received: {event.get('entityType')} at {event.get('topicOffset')}")
        
        dc.subscribe(topics=["data"], callback=handle_event, time_out_ms=30_000)
    """

    def __init__(
        self,
        site_url: Optional[str] = None,
        client_id: Optional[Union[str, int]] = None,
        client_secret: Optional[str] = None,
        scope: AvailableScopeTypes = DEFAULT_SCOPE,
        refresh_id_maps: bool = True,
        config: Optional[DealCloudConfig] = None,
        cache_schema: bool = True,
        schema_cache_ttl: float = 300.0,
    ):
        """
        Initialize DealCloud client.

        Args:
            site_url: DealCloud site (e.g., "client.dealcloud.com")
            client_id: API client ID
            client_secret: API client secret
            scope: OAuth2 scopes, any tuple of strings (default: data, user_management)
            refresh_id_maps: Whether to refresh ID maps on data operations
            config: Full DealCloudConfig object (if provided, overrides other params)
            cache_schema: Whether to use schema caching (default: True)
            schema_cache_ttl: Time-to-live for cached schema in seconds (default: 300)
        
        Note:
            Either provide (site_url, client_id, client_secret) OR config, not both.
            For production use, prefer using from_config() or from_config_object()
            factory methods for full configuration control.
        
        Note on OpenTelemetry:
            For distributed tracing, use opentelemetry-instrumentation-httpx
            which automatically instruments all HTTPX requests. See README.md.
        """
        super().__init__(
            site_url=site_url,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            refresh_id_maps=refresh_id_maps,
            config=config,
        )
        
        self._cache_schema = cache_schema
        self._schema_cache_ttl = schema_cache_ttl
        
        # Load schema (with optional caching). User map is not built on connection;
        # use cached_user_map (lazy) or get_user_map() / build_user_map_on_connect option when added.
        if cache_schema:
            cache = get_schema_cache(schema_cache_ttl)
            if cache.has(self._site, "schema", schema_cache_ttl):
                self._site_schema = cache.get(self._site, "schema", schema_cache_ttl)
            else:
                self._site_schema = self.get_schema()
                cache.set(self._site, "schema", self._site_schema)
        else:
            self._site_schema = self.get_schema()
        # _user_map left as {} from base; populate via cached_user_map (lazy) or opt-in when added
    
    def refresh_schema(self) -> None:
        """
        Force refresh of schema (and cache if enabled).
        
        Call this if schema has changed and you need the latest version.
        Does not refresh the user map; use get_user_map() or cached_user_map as needed.
        """
        self._site_schema = self.get_schema()
        if self._cache_schema:
            cache = get_schema_cache(self._schema_cache_ttl)
            cache.set(self._site, "schema", self._site_schema)
    
    def get_schema_users(self, active_only: bool = False):
        """
        Get users from Schema API (GET .../schema/users). Returns list of User models.
        Use this when you need the same behavior as the legacy SDK's get_users().
        """
        from .schema.dealcloud_schema import DealCloudSchema
        return DealCloudSchema.get_users(self, active_only)

    @property
    def cached_user_map(self) -> dict:
        """
        User email (lowercase) → user ID. Populated on first access via Schema API
        (get_schema_users), not at connection time. Overrides base to provide lazy cohesion.
        """
        if not self._user_map:
            users = self.get_schema_users(active_only=False) or []
            self._user_map = {u.email.lower(): u.id for u in users if getattr(u, "email", None)}
        return self._user_map

    def clear_schema_cache(self) -> None:
        """
        Clear schema cache for this site.
        
        The next DealCloud client for this site will fetch fresh schema.
        """
        cache = get_schema_cache()
        cache.clear(self._site)
    
    @classmethod
    def clear_all_schema_caches(cls) -> None:
        """
        Clear all schema caches for all sites.
        
        Useful when you know schemas have changed globally.
        """
        cache = get_schema_cache()
        cache.clear_all()

    # -------------------------------------------------------------------------
    # Legacy wrappers (old SDK method names)
    # -------------------------------------------------------------------------

    def get_object_history(self, *args, **kwargs):
        """
        Legacy alias for get_history(). Prefer get_history().

        Forwards to get_history(object_id, modified_since, include_calculations=False,
        deleted_only=False). modified_since is required by the API.
        """
        return self.get_history(*args, **kwargs)

    def download_files(self, *args, **kwargs):
        """
        Legacy alias for download_file(). Prefer download_file().

        Forwards to download_file(entry_id, field_id, output_path=None, progress_callback=None).
        """
        return self.download_file(*args, **kwargs)
