"""
FortiOS MONITOR - User info query

Configuration endpoint for managing monitor user/info/query objects.

API Endpoints:
    GET    /monitor/user/info/query
    POST   /monitor/user/info/query
    PUT    /monitor/user/info/query/{identifier}
    DELETE /monitor/user/info/query/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.user_info_query.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.user_info_query.post(
    ...     name="example",
    ...     srcintf="port1",  # Auto-converted to [{'name': 'port1'}]
    ...     dstintf=["port2", "port3"],  # Auto-converted to list of dicts
    ... )

Important:
    - Use **POST** to create new objects
    - Use **PUT** to update existing objects
    - Use **GET** to retrieve configuration
    - Use **DELETE** to remove objects
    - **Auto-normalization**: List fields accept strings or lists, automatically
      converted to FortiOS format [{'name': '...'}]
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Union

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from hfortix_core.http.interface import IHTTPClient
    from hfortix_fortios.models import FortiObject, FortiObjectList

# Import helper functions from central _helpers module
from hfortix_fortios._helpers import (
    build_api_payload,
    build_cmdb_payload,  # Keep for backward compatibility / manual usage
    is_success,
    quote_path_param,  # URL encoding for path parameters
)
# Import metadata mixin for schema introspection
from hfortix_fortios._helpers.metadata_mixin import MetadataMixin

# Import Protocol-based type hints (eliminates need for local @overload decorators)
from hfortix_fortios._protocols import CRUDEndpoint

class Query(CRUDEndpoint, MetadataMixin):
    """Query Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "query"
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = False
    SUPPORTS_READ = True
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = False
    SUPPORTS_MOVE = False
    SUPPORTS_CLONE = False
    SUPPORTS_FILTERING = False
    SUPPORTS_PAGINATION = False
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Query endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        timestamp_from: int | None = None,
        timestamp_to: int | None = None,
        filters: list[str] | None = None,
        query_type: Literal["latest", "unified_latest", "unified_history"] | None = None,
        query_id: int | None = None,
        cache_query: bool | None = None,
        key_only: bool | None = None,
        filter_logic: Literal["and", "or"] | None = None,
        total_only: bool | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve user/info/query configuration.

        Query user info.

        Args:
            timestamp_from: To get entries since the timestamp for unified historical query.
            timestamp_to: To get entries before the timestamp for unified historical query.
            filters: A list of filters. Type:{"type": string, "value": string, "op": string}. Op: filter operator [exact|contains|greaterThanEqualTo|lessThanEqualTo]. Default is exact.
            query_type: Query type [latest|unified_latest|unified_history]. Default is latest.
            query_id: Provide a query ID to continue getting data for that unified request. Only available for unified query types.
            cache_query: Cache query result for 5 mins and return query ID. Only available for unified query types. Default is false.
            key_only: Return primary key fields only. Default is false.
            filter_logic: The logic between filters [and|or]). Default is and.
            total_only: Whether the query should return just the total number of identities present.
            filter: List of filter expressions to limit results.
                Each filter uses format: "field==value" or "field!=value"
                Operators: ==, !=, =@ (contains), !@ (not contains), <=, <, >=, >
                Multiple filters use AND logic. For OR, use comma in single string.
                Example: ["name==test", "status==enable"] or ["name==test,name==prod"]
            count: Maximum number of entries to return (pagination).
            start: Starting entry index for pagination (0-based).
            payload_dict: Additional query parameters for advanced options:
                - datasource (bool): Include datasource information
                - with_meta (bool): Include metadata about each object
                - with_contents_hash (bool): Include checksum of object contents
                - format (list[str]): Property names to include (e.g., ["policyid", "srcintf"])
                - scope (str): Query scope - "global", "vdom", or "both"
                - action (str): Special actions - "schema", "default"
                See FortiOS REST API documentation for complete list.
            vdom: Virtual domain name. Use True for global, string for specific VDOM, None for default.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.
            Access results via dictionary keys (e.g., result['results'], result['http_status']).
            
            Response structure:
                - http_method: GET
                - results: Configuration object(s)
                - vdom: Virtual domain
                - path: API path
                - name: Object name (single object queries)
                - status: success/error
                - http_status: HTTP status code
                - build: FortiOS build number

        Examples:
            >>> # Get all user/info/query objects
            >>> result = fgt.api.monitor.user_info_query.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.monitor.user_info_query.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.monitor.user_info_query.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.monitor.user_info_query.get_schema()

        See Also:
            - post(): Create new user/info/query object
            - put(): Update existing user/info/query object
            - delete(): Remove user/info/query object
            - exists(): Check if object exists
        """
        params = payload_dict.copy() if payload_dict else {}
        
        # Add explicit query parameters
        if filter is not None:
            params["filter"] = filter
        if count is not None:
            params["count"] = count
        if start is not None:
            params["start"] = start
        if timestamp_from is not None:
            params["timestamp_from"] = timestamp_from
        if timestamp_to is not None:
            params["timestamp_to"] = timestamp_to
        if filters is not None:
            params["filters"] = filters
        if query_type is not None:
            params["query_type"] = query_type
        if query_id is not None:
            params["query_id"] = query_id
        if cache_query is not None:
            params["cache_query"] = cache_query
        if key_only is not None:
            params["key_only"] = key_only
        if filter_logic is not None:
            params["filter_logic"] = filter_logic
        if total_only is not None:
            params["total_only"] = total_only
        
        endpoint = "/user/info/query"
        unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "monitor", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )












