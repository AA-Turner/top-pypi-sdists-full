"""
FortiOS CMDB - Web_proxy global_

Configuration endpoint for managing cmdb web_proxy/global_ objects.

API Endpoints:
    GET    /cmdb/web_proxy/global_
    POST   /cmdb/web_proxy/global_
    PUT    /cmdb/web_proxy/global_/{identifier}
    DELETE /cmdb/web_proxy/global_/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.web_proxy_global.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.web_proxy_global.post(
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

class Global(CRUDEndpoint, MetadataMixin):
    """Global Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "global_"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "learn_client_ip_srcaddr": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "learn_client_ip_srcaddr6": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
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
        """Initialize Global endpoint."""
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
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve web_proxy/global_ configuration.

        Configure Web proxy global settings.

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
            >>> # Get all web_proxy/global_ objects
            >>> result = fgt.api.cmdb.web_proxy_global.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.web_proxy_global.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.web_proxy_global.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.web_proxy_global.get_schema()

        See Also:
            - post(): Create new web_proxy/global_ object
            - put(): Update existing web_proxy/global_ object
            - delete(): Remove web_proxy/global_ object
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
            endpoint = f"/web-proxy/global/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/web-proxy/global"
            unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )

    def get_schema(
        self,
        vdom: str | None = None,
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
            vdom: Virtual domain. None uses default VDOM.
            format: Schema format - "schema" (FortiOS native) or "json-schema" (JSON Schema standard).
                Defaults to "schema".
                
        Returns:
            Schema definition as dict. Returns Coroutine if using async client.
            
        Example:
            >>> # Get FortiOS native schema
            >>> schema = fgt.api.cmdb.web_proxy_global.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.web_proxy_global.get_schema(format="json-schema")
        
        Note:
            Not all endpoints support all schema formats. The "schema" format
            is most widely supported.
        """
        return self.get(payload_dict={"action": format}, vdom=vdom)


    # ========================================================================
    # PUT Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def put(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        ssl_cert: str | None = None,
        ssl_ca_cert: str | None = None,
        fast_policy_match: Literal["enable", "disable"] | None = None,
        ldap_user_cache: Literal["enable", "disable"] | None = None,
        proxy_fqdn: str | None = None,
        max_request_length: int | None = None,
        max_message_length: int | None = None,
        http2_client_window_size: int | None = None,
        http2_server_window_size: int | None = None,
        auth_sign_timeout: int | None = None,
        strict_web_check: Literal["enable", "disable"] | None = None,
        forward_proxy_auth: Literal["enable", "disable"] | None = None,
        forward_server_affinity_timeout: int | None = None,
        max_waf_body_cache_length: int | None = None,
        webproxy_profile: str | None = None,
        learn_client_ip: Literal["enable", "disable"] | None = None,
        always_learn_client_ip: Literal["enable", "disable"] | None = None,
        learn_client_ip_from_header: Literal["true-client-ip", "x-real-ip", "x-forwarded-for"] | list[str] | None = None,
        learn_client_ip_srcaddr: str | list[str] | list[dict[str, Any]] | None = None,
        learn_client_ip_srcaddr6: str | list[str] | list[dict[str, Any]] | None = None,
        src_affinity_exempt_addr: str | list[str] | None = None,
        src_affinity_exempt_addr6: str | list[str] | None = None,
        policy_partial_match: Literal["enable", "disable"] | None = None,
        log_policy_pending: Literal["enable", "disable"] | None = None,
        log_forward_server: Literal["enable", "disable"] | None = None,
        log_app_id: Literal["enable", "disable"] | None = None,
        proxy_transparent_cert_inspection: Literal["enable", "disable"] | None = None,
        request_obs_fold: Literal["replace-with-sp", "block", "keep"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing web_proxy/global_ object.

        Configure Web proxy global settings.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            ssl_cert: SSL certificate for SSL interception.
            ssl_ca_cert: SSL CA certificate for SSL interception.
            fast_policy_match: Enable/disable fast matching algorithm for explicit and transparent proxy policy.
            ldap_user_cache: Enable/disable LDAP user cache for explicit and transparent proxy user.
            proxy_fqdn: Fully Qualified Domain Name of the explicit web proxy (default = default.fqdn) that clients connect to.
            max_request_length: Maximum length of HTTP request line (2 - 64 Kbytes, default = 8).
            max_message_length: Maximum length of HTTP message, not including body (16 - 256 Kbytes, default = 32).
            http2_client_window_size: HTTP/2 client initial window size in bytes (65535 - 2147483647, default = 1048576 (1MB)).
            http2_server_window_size: HTTP/2 server initial window size in bytes (65535 - 2147483647, default = 1048576 (1MB)).
            auth_sign_timeout: Proxy auth query sign timeout in seconds (30 - 3600, default = 120).
            strict_web_check: Enable/disable strict web checking to block web sites that send incorrect headers that don't conform to HTTP.
            forward_proxy_auth: Enable/disable forwarding proxy authentication headers.
            forward_server_affinity_timeout: Period of time before the source IP's traffic is no longer assigned to the forwarding server (6 - 60 min, default = 30).
            max_waf_body_cache_length: Maximum length of HTTP messages processed by Web Application Firewall (WAF) (1 - 1024 Kbytes, default = 1).
            webproxy_profile: Name of the web proxy profile to apply when explicit proxy traffic is allowed by default and traffic is accepted that does not match an explicit proxy policy.
            learn_client_ip: Enable/disable learning the client's IP address from headers.
            always_learn_client_ip: Enable/disable learning the client's IP address from headers for every request.
            learn_client_ip_from_header: Learn client IP address from the specified headers.
            learn_client_ip_srcaddr: Source address name (srcaddr or srcaddr6 must be set).
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            learn_client_ip_srcaddr6: IPv6 Source address name (srcaddr or srcaddr6 must be set).
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            src_affinity_exempt_addr: IPv4 source addresses to exempt proxy affinity.
            src_affinity_exempt_addr6: IPv6 source addresses to exempt proxy affinity.
            policy_partial_match: Enable/disable policy partial matching.
            log_policy_pending: Enable/disable logging sessions that are pending on policy matching.
            log_forward_server: Enable/disable forward server name logging in forward traffic log.
            log_app_id: Enable/disable always log application type in traffic log.
            proxy_transparent_cert_inspection: Enable/disable transparent proxy certificate inspection.
            request_obs_fold: Action when HTTP/1.x request header contains obs-fold (default = keep).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.web_proxy_global.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.web_proxy_global.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if learn_client_ip_srcaddr is not None:
            learn_client_ip_srcaddr = normalize_table_field(
                learn_client_ip_srcaddr,
                mkey="name",
                required_fields=['name'],
                field_name="learn_client_ip_srcaddr",
                example="[{'name': 'value'}]",
            )
        if learn_client_ip_srcaddr6 is not None:
            learn_client_ip_srcaddr6 = normalize_table_field(
                learn_client_ip_srcaddr6,
                mkey="name",
                required_fields=['name'],
                field_name="learn_client_ip_srcaddr6",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            ssl_cert=ssl_cert,
            ssl_ca_cert=ssl_ca_cert,
            fast_policy_match=fast_policy_match,
            ldap_user_cache=ldap_user_cache,
            proxy_fqdn=proxy_fqdn,
            max_request_length=max_request_length,
            max_message_length=max_message_length,
            http2_client_window_size=http2_client_window_size,
            http2_server_window_size=http2_server_window_size,
            auth_sign_timeout=auth_sign_timeout,
            strict_web_check=strict_web_check,
            forward_proxy_auth=forward_proxy_auth,
            forward_server_affinity_timeout=forward_server_affinity_timeout,
            max_waf_body_cache_length=max_waf_body_cache_length,
            webproxy_profile=webproxy_profile,
            learn_client_ip=learn_client_ip,
            always_learn_client_ip=always_learn_client_ip,
            learn_client_ip_from_header=learn_client_ip_from_header,
            learn_client_ip_srcaddr=learn_client_ip_srcaddr,
            learn_client_ip_srcaddr6=learn_client_ip_srcaddr6,
            src_affinity_exempt_addr=src_affinity_exempt_addr,
            src_affinity_exempt_addr6=src_affinity_exempt_addr6,
            policy_partial_match=policy_partial_match,
            log_policy_pending=log_policy_pending,
            log_forward_server=log_forward_server,
            log_app_id=log_app_id,
            proxy_transparent_cert_inspection=proxy_transparent_cert_inspection,
            request_obs_fold=request_obs_fold,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.global_ import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/web_proxy/global_",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/web-proxy/global"

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
            "cmdb", endpoint, data=payload_data, params=params, vdom=vdom        )





    # ========================================================================
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move web_proxy/global_ object to a new position.
        
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
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.web_proxy_global.move(
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
            all_objects = self.get(vdom=vdom)
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
            all_objects = self.get(vdom=vdom)
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
        endpoint = "/web-proxy/global/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





