"""
FortiOS CMDB - System dns

Configuration endpoint for managing cmdb system/dns objects.

API Endpoints:
    GET    /cmdb/system/dns
    POST   /cmdb/system/dns
    PUT    /cmdb/system/dns/{identifier}
    DELETE /cmdb/system/dns/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_dns.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_dns.post(
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
    normalize_table_field,  # For table field normalization
)
# Import metadata mixin for schema introspection
from hfortix_fortios._helpers.metadata_mixin import MetadataMixin

# Import Protocol-based type hints (eliminates need for local @overload decorators)
from hfortix_fortios._protocols import CRUDEndpoint

class Dns(CRUDEndpoint, MetadataMixin):
    """Dns Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "dns"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "server_hostname": {
            "mkey": "hostname",
            "required_fields": ['hostname'],
            "example": "[{'hostname': 'value'}]",
        },
        "domain": {
            "mkey": "domain",
            "required_fields": ['domain'],
            "example": "[{'domain': 'value'}]",
        },
    }
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = False
    SUPPORTS_READ = True
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = False
    SUPPORTS_MOVE = True
    # SUPPORTS_CLONE = True  # Disabled - unreliable across endpoints
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Dns endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        sort: str | None = None,
        format: str | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve system/dns configuration.

        Configure DNS.

        Args:
            name: Name identifier to retrieve specific object. If None, returns all objects.
            filter: List of filter expressions to limit results.
                Each filter uses format: "field==value" or "field!=value"
                Operators: ==, !=, =@ (contains), !@ (not contains), <=, <, >=, >
                Multiple filters use AND logic. For OR, use comma in single string.
                Example: ["name==test", "status==enable"] or ["name==test,name==prod"]
            sort: Sort results by field. Format: "field" or "field,asc" or "field,dsc"
                Example: "name" (ascending) or "name,dsc" (descending)
                Multiple sorts: Use multiple sort parameters in order of priority
            format: Return only specific fields. Format: "field1|field2|field3"
                Example: "name|type|subnet"
            count: Maximum number of entries to return (pagination).
            start: Starting entry index for pagination (0-based).
            payload_dict: Additional query parameters for advanced options:
                - datasource (bool): Include datasource information
                - with_meta (bool): Include metadata about each object
                - with_contents_hash (bool): Include checksum of object contents
                - scope (str): Query scope - "global", "vdom", or "both"
                - action (str): Special actions - "schema", "default"
                See FortiOS REST API documentation for complete list.
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
            >>> # Get all system/dns objects
            >>> result = fgt.api.cmdb.system_dns.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_dns.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_dns.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_dns.get_schema()

        See Also:
            - post(): Create new system/dns object
            - put(): Update existing system/dns object
            - delete(): Remove system/dns object
            - exists(): Check if object exists
            - get_schema(): Get endpoint schema/metadata
        """
        params = payload_dict.copy() if payload_dict else {}
        
        # Add explicit query parameters
        # Handle filter parameter specially to support FortiOS AND syntax with multiple filters
        # FortiOS uses: ?filter=a&filter=b for AND operations
        # Normalize filter syntax to support all common formats:
        #   1. name=@test&name!@web (implicit & separator)
        #   2. name=@test&filter=name!@web (mixed implicit/explicit)
        #   3. filter=name=@test&filter=name!@web (explicit with filter= prefix)
        #   4. filter=name=@test&name!@web (explicit prefix with implicit separator)
        if filter is not None:
            normalized_filter = filter
            
            # Step 1: Remove leading "filter=" if present (normalize input format)
            # "filter=name=@test&..." -> "name=@test&..."
            if normalized_filter.startswith("filter="):
                normalized_filter = normalized_filter[7:]  # Remove "filter=" prefix
            
            # Step 2: Normalize & separators to &filter=
            # This handles all variations: "a&b", "a&filter=b", etc.
            if "&" in normalized_filter:
                # Split on both & and &filter= to get all filter parts
                # Then rejoin with &filter= for consistency
                parts = []
                current = normalized_filter
                
                # Split on &filter= first to preserve already-explicit parts
                while "&filter=" in current:
                    before, after = current.split("&filter=", 1)
                    # Now split 'before' on & if it contains any
                    if "&" in before:
                        parts.extend(before.split("&"))
                    else:
                        parts.append(before)
                    current = after
                
                # Handle remaining part (after last &filter= or the whole string if no &filter=)
                if "&" in current:
                    parts.extend(current.split("&"))
                else:
                    parts.append(current)
                
                # Rejoin with &filter= separator
                if len(parts) > 1:
                    normalized_filter = parts[0] + "".join(f"&filter={part}" for part in parts[1:])
            
            # Step 3: Check if we have multiple filters (AND operation)
            if "&filter=" in normalized_filter:
                # Multiple filters for AND operation: "filter1&filter=filter2&filter=filter3"
                # Split and create list of filter values
                filters = [normalized_filter.split("&filter=")[0]]  # First filter before &filter=
                filters.extend(normalized_filter.split("&filter=")[1:])  # Remaining filters after each &filter=
                params["filter"] = filters
            else:
                params["filter"] = normalized_filter
        if sort is not None:
            params["sort"] = sort
        if format is not None:
            params["format"] = format
        if count is not None:
            params["count"] = count
        if start is not None:
            params["start"] = start
        
        if name:
            endpoint = f"/system/dns/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/system/dns"
            unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=False, unwrap_single=unwrap_single
        )

    def get_schema(
        self,
        format: str = "schema",
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Get schema/metadata for this endpoint.
        
        Returns the FortiOS schema definition including available fields,
        their types, required vs optional properties, enum values, nested
        structures, and default values.
        
        This queries the live firewall for its current schema, which may
        vary between FortiOS versions.
        
        Args:
            format: Schema format - "schema" (FortiOS native) or "json-schema" (JSON Schema standard).
                Defaults to "schema".
                
        Returns:
            Schema definition as dict. Returns Coroutine if using async client.
            
        Example:
            >>> # Get FortiOS native schema
            >>> schema = fgt.api.cmdb.system_dns.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_dns.get_schema(format="json-schema")
        
        Note:
            Not all endpoints support all schema formats. The "schema" format
            is most widely supported.
        """
        return self.get(payload_dict={"action": format})


    # ========================================================================
    # PUT Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def put(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        primary: str | None = None,
        secondary: str | None = None,
        protocol: Literal["cleartext", "dot", "doh"] | list[str] | None = None,
        ssl_certificate: str | None = None,
        server_hostname: str | list[str] | list[dict[str, Any]] | None = None,
        domain: str | list[str] | list[dict[str, Any]] | None = None,
        ip6_primary: str | None = None,
        ip6_secondary: str | None = None,
        timeout: int | None = None,
        retry: int | None = None,
        dns_cache_limit: int | None = None,
        dns_cache_ttl: int | None = None,
        cache_notfound_responses: Literal["disable", "enable"] | None = None,
        source_ip: str | None = None,
        source_ip_interface: str | None = None,
        root_servers: str | list[str] | None = None,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = None,
        interface: str | None = None,
        vrf_select: int | None = None,
        server_select_method: Literal["least-rtt", "failover"] | None = None,
        alt_primary: str | None = None,
        alt_secondary: str | None = None,
        log: Literal["disable", "error", "all"] | None = None,
        fqdn_cache_ttl: int | None = None,
        fqdn_max_refresh: int | None = None,
        fqdn_min_refresh: int | None = None,
        hostname_ttl: int | None = None,
        hostname_limit: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/dns object.

        Configure DNS.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            primary: Primary DNS server IP address.
            secondary: Secondary DNS server IP address.
            protocol: DNS transport protocols.
            ssl_certificate: Name of local certificate for SSL connections.
            server_hostname: DNS server host name list.
                Default format: [{'hostname': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'hostname': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'hostname': 'val1'}, ...]
                  - List of dicts: [{'hostname': 'value'}] (recommended)
            domain: Search suffix list for hostname lookup.
                Default format: [{'domain': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'domain': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'domain': 'val1'}, ...]
                  - List of dicts: [{'domain': 'value'}] (recommended)
            ip6_primary: Primary DNS server IPv6 address.
            ip6_secondary: Secondary DNS server IPv6 address.
            timeout: DNS query timeout interval in seconds (1 - 10).
            retry: Number of times to retry (0 - 5).
            dns_cache_limit: Maximum number of records in the DNS cache.
            dns_cache_ttl: Duration in seconds that the DNS cache retains information.
            cache_notfound_responses: Enable/disable response from the DNS server when a record is not in cache.
            source_ip: IP address used by the DNS server as its source IP.
            source_ip_interface: IP address of the specified interface as the source IP address.
            root_servers: Configure up to two preferred servers that serve the DNS root zone (default uses all 13 root servers).
            interface_select_method: Specify how to select outgoing interface to reach server.
            interface: Specify outgoing interface to reach server.
            vrf_select: VRF ID used for connection to server.
            server_select_method: Specify how configured servers are prioritized.
            alt_primary: Alternate primary DNS server. This is not used as a failover DNS server.
            alt_secondary: Alternate secondary DNS server. This is not used as a failover DNS server.
            log: Local DNS log setting.
            fqdn_cache_ttl: FQDN cache time to live in seconds (0 - 86400, default = 0).
            fqdn_max_refresh: FQDN cache maximum refresh time in seconds (3600 - 86400, default = 3600).
            fqdn_min_refresh: FQDN cache minimum refresh time in seconds (10 - 3600, default = 60).
            hostname_ttl: TTL of hostname table entries (60 - 86400).
            hostname_limit: Limit of the number of hostname table entries (0 - 50000).
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_dns.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_dns.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if server_hostname is not None:
            server_hostname = normalize_table_field(
                server_hostname,
                mkey="hostname",
                required_fields=['hostname'],
                field_name="server_hostname",
                example="[{'hostname': 'value'}]",
            )
        if domain is not None:
            domain = normalize_table_field(
                domain,
                mkey="domain",
                required_fields=['domain'],
                field_name="domain",
                example="[{'domain': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            primary=primary,
            secondary=secondary,
            protocol=protocol,
            ssl_certificate=ssl_certificate,
            server_hostname=server_hostname,
            domain=domain,
            ip6_primary=ip6_primary,
            ip6_secondary=ip6_secondary,
            timeout=timeout,
            retry=retry,
            dns_cache_limit=dns_cache_limit,
            dns_cache_ttl=dns_cache_ttl,
            cache_notfound_responses=cache_notfound_responses,
            source_ip=source_ip,
            source_ip_interface=source_ip_interface,
            root_servers=root_servers,
            interface_select_method=interface_select_method,
            interface=interface,
            vrf_select=vrf_select,
            server_select_method=server_select_method,
            alt_primary=alt_primary,
            alt_secondary=alt_secondary,
            log=log,
            fqdn_cache_ttl=fqdn_cache_ttl,
            fqdn_max_refresh=fqdn_max_refresh,
            fqdn_min_refresh=fqdn_min_refresh,
            hostname_ttl=hostname_ttl,
            hostname_limit=hostname_limit,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.dns import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/dns",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/system/dns"

        # Add explicit query parameters for PUT
        params: dict[str, Any] = {}
        if q_action is not None:
            params["action"] = q_action
        if q_before is not None:
            params["before"] = q_before
        if q_after is not None:
            params["after"] = q_after
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, params=params, vdom=False        )





    # ========================================================================
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/dns object to a new position.
        
        Reorders objects by moving one before/after another, to top/bottom, or to a specific position.
        
        Args:
            name: Name of object to move
            position: Where to move the object:
                - "before": Move before reference object (requires reference_name)
                - "after": Move after reference object (requires reference_name)
                - "top": Move to first position (reference not needed)
                - "bottom": Move to last position (reference not needed)
                - int (1-based): Move to specific position number (e.g., position=3 for 3rd place)
            reference_name: Name of reference object (required for before/after)
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.system_dns.move(
            ...     name="object1",
            ...     position="before",
            ...     reference_name="object2"
            ... )
        """
        # Handle numeric position (1-based index)
        if isinstance(position, int):
            if position < 1:
                raise ValueError(f"Position must be >= 1, got {position}")
            
            # Get all objects to find the target position
            all_objects = self.get()
            if not all_objects:
                raise ValueError("Cannot move to position {position} - no objects found")
            
            # Validate position is within range (can be len+1 to append at end)
            if position > len(all_objects) + 1:
                raise ValueError(
                    f"Position {position} is out of range. Valid range: 1-{len(all_objects) + 1} "
                    f"({len(all_objects)} objects exist)"
                )
            
            # Convert to before/after operation
            if position == 1:
                # Move to first position
                reference_name = all_objects[0].name
                actual_position = "before"
            elif position > len(all_objects):
                # Move to last position (after all existing objects)
                reference_name = all_objects[-1].name
                actual_position = "after"
            else:
                # Move before the object currently at that position
                reference_name = all_objects[position - 1].name
                actual_position = "before"
        
        # Handle top/bottom string positions
        elif position in ("top", "bottom"):
            # Get all objects to find first/last
            all_objects = self.get()
            if not all_objects:
                raise ValueError(f"Cannot move to {position} - no objects found")
            
            if position == "top":
                # Move before first object
                reference_name = all_objects[0].name
                actual_position = "before"
            else:  # bottom
                # Move after last object
                reference_name = all_objects[-1].name
                actual_position = "after"
        
        # Handle before/after string positions
        else:
            # Validate reference is provided for before/after
            if reference_name is None:
                raise ValueError(f"reference_name is required when position='{position}'")
            actual_position = position
        
        # Build params for move operation
        params = {
            "action": "move",
            actual_position: reference_name,
            **kwargs,
        }
        
        # Move requires the mkey in the endpoint path
        endpoint = "/system/dns/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )





