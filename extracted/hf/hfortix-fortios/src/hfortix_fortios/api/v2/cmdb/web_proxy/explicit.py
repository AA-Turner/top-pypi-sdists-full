"""
FortiOS CMDB - Web_proxy explicit

Configuration endpoint for managing cmdb web_proxy/explicit objects.

API Endpoints:
    GET    /cmdb/web_proxy/explicit
    POST   /cmdb/web_proxy/explicit
    PUT    /cmdb/web_proxy/explicit/{identifier}
    DELETE /cmdb/web_proxy/explicit/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.web_proxy_explicit.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.web_proxy_explicit.post(
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

class Explicit(CRUDEndpoint, MetadataMixin):
    """Explicit Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "explicit"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "secure_web_proxy_cert": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "pac_policy": {
            "mkey": "policyid",
            "required_fields": ['policyid', 'srcaddr', 'dstaddr', 'pac-file-name'],
            "example": "[{'policyid': 1, 'srcaddr': 'value', 'dstaddr': 'value', 'pac-file-name': 'value'}]",
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
        """Initialize Explicit endpoint."""
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
        Retrieve web_proxy/explicit configuration.

        Configure explicit Web proxy settings.

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
            >>> # Get all web_proxy/explicit objects
            >>> result = fgt.api.cmdb.web_proxy_explicit.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.web_proxy_explicit.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.web_proxy_explicit.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.web_proxy_explicit.get_schema()

        See Also:
            - post(): Create new web_proxy/explicit object
            - put(): Update existing web_proxy/explicit object
            - delete(): Remove web_proxy/explicit object
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
            endpoint = f"/web-proxy/explicit/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/web-proxy/explicit"
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
            >>> schema = fgt.api.cmdb.web_proxy_explicit.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.web_proxy_explicit.get_schema(format="json-schema")
        
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
        status: Literal["enable", "disable"] | None = None,
        secure_web_proxy: Literal["disable", "enable", "secure"] | None = None,
        ftp_over_http: Literal["enable", "disable"] | None = None,
        socks: Literal["enable", "disable"] | None = None,
        http_incoming_port: str | None = None,
        http_connection_mode: Literal["static", "multiplex", "serverpool"] | None = None,
        https_incoming_port: str | None = None,
        secure_web_proxy_cert: str | list[str] | list[dict[str, Any]] | None = None,
        client_cert: Literal["disable", "enable"] | None = None,
        user_agent_detect: Literal["disable", "enable"] | None = None,
        empty_cert_action: Literal["accept", "block", "accept-unmanageable"] | None = None,
        ssl_dh_bits: Literal["768", "1024", "1536", "2048"] | None = None,
        ftp_incoming_port: str | None = None,
        socks_incoming_port: str | None = None,
        incoming_ip: str | None = None,
        outgoing_ip: str | list[str] | None = None,
        interface_select_method: Literal["sdwan", "specify"] | None = None,
        interface: str | None = None,
        vrf_select: int | None = None,
        ipv6_status: Literal["enable", "disable"] | None = None,
        incoming_ip6: str | None = None,
        outgoing_ip6: str | list[str] | None = None,
        strict_guest: Literal["enable", "disable"] | None = None,
        pref_dns_result: Literal["ipv4", "ipv6", "ipv4-strict", "ipv6-strict"] | None = None,
        unknown_http_version: Literal["reject", "best-effort"] | None = None,
        realm: str | None = None,
        sec_default_action: Literal["accept", "deny"] | None = None,
        https_replacement_message: Literal["enable", "disable"] | None = None,
        message_upon_server_error: Literal["enable", "disable"] | None = None,
        pac_file_server_status: Literal["enable", "disable"] | None = None,
        pac_file_url: str | None = None,
        pac_file_server_port: str | None = None,
        pac_file_through_https: Literal["enable", "disable"] | None = None,
        pac_file_name: str | None = None,
        pac_file_data: str | None = None,
        pac_policy: str | list[str] | list[dict[str, Any]] | None = None,
        ssl_algorithm: Literal["high", "medium", "low"] | None = None,
        trace_auth_no_rsp: Literal["enable", "disable"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing web_proxy/explicit object.

        Configure explicit Web proxy settings.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            status: Enable/disable the explicit Web proxy for HTTP and HTTPS session.
            secure_web_proxy: Enable/disable/require the secure web proxy for HTTP and HTTPS session.
            ftp_over_http: Enable to proxy FTP-over-HTTP sessions sent from a web browser.
            socks: Enable/disable the SOCKS proxy.
            http_incoming_port: Accept incoming HTTP requests on one or more ports (0 - 65535, default = 8080).
            http_connection_mode: HTTP connection mode (default = static).
            https_incoming_port: Accept incoming HTTPS requests on one or more ports (0 - 65535, default = 0, use the same as HTTP).
            secure_web_proxy_cert: Name of certificates for secure web proxy.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            client_cert: Enable/disable to request client certificate.
            user_agent_detect: Enable/disable to detect device type by HTTP user-agent if no client certificate provided.
            empty_cert_action: Action of an empty client certificate.
            ssl_dh_bits: Bit-size of Diffie-Hellman (DH) prime used in DHE-RSA negotiation (default = 2048).
            ftp_incoming_port: Accept incoming FTP-over-HTTP requests on one or more ports (0 - 65535, default = 0; use the same as HTTP).
            socks_incoming_port: Accept incoming SOCKS proxy requests on one or more ports (0 - 65535, default = 0; use the same as HTTP).
            incoming_ip: Restrict the explicit HTTP proxy to only accept sessions from this IP address. An interface must have this IP address.
            outgoing_ip: Outgoing HTTP requests will have this IP address as their source address. An interface must have this IP address.
            interface_select_method: Specify how to select outgoing interface to reach server.
            interface: Specify outgoing interface to reach server.
            vrf_select: VRF ID used for connection to server.
            ipv6_status: Enable/disable allowing an IPv6 web proxy destination in policies and all IPv6 related entries in this command.
            incoming_ip6: Restrict the explicit web proxy to only accept sessions from this IPv6 address. An interface must have this IPv6 address.
            outgoing_ip6: Outgoing HTTP requests will leave this IPv6. Multiple interfaces can be specified. Interfaces must have these IPv6 addresses.
            strict_guest: Enable/disable strict guest user checking by the explicit web proxy.
            pref_dns_result: Prefer resolving addresses using the configured IPv4 or IPv6 DNS server (default = ipv4).
            unknown_http_version: How to handle HTTP sessions that do not comply with HTTP 0.9, 1.0, or 1.1.
            realm: Authentication realm used to identify the explicit web proxy (maximum of 63 characters).
            sec_default_action: Accept or deny explicit web proxy sessions when no web proxy firewall policy exists.
            https_replacement_message: Enable/disable sending the client a replacement message for HTTPS requests.
            message_upon_server_error: Enable/disable displaying a replacement message when a server error is detected.
            pac_file_server_status: Enable/disable Proxy Auto-Configuration (PAC) for users of this explicit proxy profile.
            pac_file_url: PAC file access URL.
            pac_file_server_port: Port number that PAC traffic from client web browsers uses to connect to the explicit web proxy (0 - 65535, default = 0; use the same as HTTP).
            pac_file_through_https: Enable/disable to get Proxy Auto-Configuration (PAC) through HTTPS.
            pac_file_name: Pac file name.
            pac_file_data: PAC file contents enclosed in quotes (maximum of 256K bytes).
            pac_policy: PAC policies.
                Default format: [{'policyid': 1, 'srcaddr': 'value', 'dstaddr': 'value', 'pac-file-name': 'value'}]
                Required format: List of dicts with keys: policyid, srcaddr, dstaddr, pac-file-name
                  (String format not allowed due to multiple required fields)
            ssl_algorithm: Relative strength of encryption algorithms accepted in HTTPS deep scan: high, medium, or low.
            trace_auth_no_rsp: Enable/disable logging timed-out authentication requests.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.web_proxy_explicit.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.web_proxy_explicit.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if secure_web_proxy_cert is not None:
            secure_web_proxy_cert = normalize_table_field(
                secure_web_proxy_cert,
                mkey="name",
                required_fields=['name'],
                field_name="secure_web_proxy_cert",
                example="[{'name': 'value'}]",
            )
        if pac_policy is not None:
            pac_policy = normalize_table_field(
                pac_policy,
                mkey="policyid",
                required_fields=['policyid', 'srcaddr', 'dstaddr', 'pac-file-name'],
                field_name="pac_policy",
                example="[{'policyid': 1, 'srcaddr': 'value', 'dstaddr': 'value', 'pac-file-name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            status=status,
            secure_web_proxy=secure_web_proxy,
            ftp_over_http=ftp_over_http,
            socks=socks,
            http_incoming_port=http_incoming_port,
            http_connection_mode=http_connection_mode,
            https_incoming_port=https_incoming_port,
            secure_web_proxy_cert=secure_web_proxy_cert,
            client_cert=client_cert,
            user_agent_detect=user_agent_detect,
            empty_cert_action=empty_cert_action,
            ssl_dh_bits=ssl_dh_bits,
            ftp_incoming_port=ftp_incoming_port,
            socks_incoming_port=socks_incoming_port,
            incoming_ip=incoming_ip,
            outgoing_ip=outgoing_ip,
            interface_select_method=interface_select_method,
            interface=interface,
            vrf_select=vrf_select,
            ipv6_status=ipv6_status,
            incoming_ip6=incoming_ip6,
            outgoing_ip6=outgoing_ip6,
            strict_guest=strict_guest,
            pref_dns_result=pref_dns_result,
            unknown_http_version=unknown_http_version,
            realm=realm,
            sec_default_action=sec_default_action,
            https_replacement_message=https_replacement_message,
            message_upon_server_error=message_upon_server_error,
            pac_file_server_status=pac_file_server_status,
            pac_file_url=pac_file_url,
            pac_file_server_port=pac_file_server_port,
            pac_file_through_https=pac_file_through_https,
            pac_file_name=pac_file_name,
            pac_file_data=pac_file_data,
            pac_policy=pac_policy,
            ssl_algorithm=ssl_algorithm,
            trace_auth_no_rsp=trace_auth_no_rsp,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.explicit import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/web_proxy/explicit",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/web-proxy/explicit"

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
        Move web_proxy/explicit object to a new position.
        
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
            >>> fgt.api.cmdb.web_proxy_explicit.move(
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
        endpoint = "/web-proxy/explicit/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





