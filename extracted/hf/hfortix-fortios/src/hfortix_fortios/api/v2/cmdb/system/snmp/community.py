"""
FortiOS CMDB - System snmp community

Configuration endpoint for managing cmdb system/snmp/community objects.

API Endpoints:
    GET    /cmdb/system/snmp/community
    POST   /cmdb/system/snmp/community
    PUT    /cmdb/system/snmp/community/{identifier}
    DELETE /cmdb/system/snmp/community/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_snmp_community.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_snmp_community.post(
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

class Community(CRUDEndpoint, MetadataMixin):
    """Community Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "community"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "hosts": {
            "mkey": "id",
            "required_fields": ['id', 'ip', 'interface'],
            "example": "[{'id': 1, 'ip': '192.168.1.10', 'interface': 'value'}]",
        },
        "hosts6": {
            "mkey": "id",
            "required_fields": ['id', 'ipv6', 'interface'],
            "example": "[{'id': 1, 'ipv6': 'value', 'interface': 'value'}]",
        },
        "vdoms": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
    }
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = True
    SUPPORTS_READ = True
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = True
    SUPPORTS_MOVE = True
    # SUPPORTS_CLONE = True  # Disabled - unreliable across endpoints
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Community endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        id: int | None = None,
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
        Retrieve system/snmp/community configuration.

        SNMP community configuration.

        Args:
            id: Integer identifier to retrieve specific object.
                If None, returns all objects.
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
            >>> # Get all system/snmp/community objects
            >>> result = fgt.api.cmdb.system_snmp_community.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/snmp/community by id
            >>> result = fgt.api.cmdb.system_snmp_community.get(id=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_snmp_community.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_snmp_community.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_snmp_community.get_schema()

        See Also:
            - post(): Create new system/snmp/community object
            - put(): Update existing system/snmp/community object
            - delete(): Remove system/snmp/community object
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
        
        if id:
            endpoint = "/system.snmp/community/" + quote_path_param(id)
            unwrap_single = True
        else:
            endpoint = "/system.snmp/community"
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
            >>> schema = fgt.api.cmdb.system_snmp_community.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_snmp_community.get_schema(format="json-schema")
        
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
        id: int | None = None,
        name: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        hosts: str | list[str] | list[dict[str, Any]] | None = None,
        hosts6: str | list[str] | list[dict[str, Any]] | None = None,
        query_v1_status: Literal["enable", "disable"] | None = None,
        query_v1_port: int | None = None,
        query_v2c_status: Literal["enable", "disable"] | None = None,
        query_v2c_port: int | None = None,
        trap_v1_status: Literal["enable", "disable"] | None = None,
        trap_v1_lport: int | None = None,
        trap_v1_rport: int | None = None,
        trap_v2c_status: Literal["enable", "disable"] | None = None,
        trap_v2c_lport: int | None = None,
        trap_v2c_rport: int | None = None,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "vpn-tun-up", "vpn-tun-down", "ha-switch", "ha-hb-failure", "ips-signature", "ips-anomaly", "av-virus", "av-oversize", "av-pattern", "av-fragmented", "fm-if-change", "fm-conf-change", "bgp-established", "bgp-backward-transition", "ha-member-up", "ha-member-down", "ent-conf-change", "av-conserve", "av-bypass", "av-oversize-passed", "av-oversize-blocked", "ips-pkg-update", "ips-fail-open", "faz-disconnect", "faz", "wc-ap-up", "wc-ap-down", "fswctl-session-up", "fswctl-session-down", "load-balance-real-server-down", "device-new", "per-cpu-high", "dhcp", "pool-usage", "ippool", "interface", "ospf-nbr-state-change", "ospf-virtnbr-state-change", "bfd"] | list[str] | None = None,
        mib_view: str | None = None,
        vdoms: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/snmp/community object.

        SNMP community configuration.

        Args:
            payload_dict: Object data as dict. Must include id (primary key).
            id: Community ID.
            name: Community name.
            status: Enable/disable this SNMP community.
            hosts: Configure IPv4 SNMP managers (hosts).
                Default format: [{'id': 1, 'ip': '192.168.1.10', 'interface': 'value'}]
                Required format: List of dicts with keys: id, ip, interface
                  (String format not allowed due to multiple required fields)
            hosts6: Configure IPv6 SNMP managers.
                Default format: [{'id': 1, 'ipv6': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: id, ipv6, interface
                  (String format not allowed due to multiple required fields)
            query_v1_status: Enable/disable SNMP v1 queries.
            query_v1_port: SNMP v1 query port (default = 161).
            query_v2c_status: Enable/disable SNMP v2c queries.
            query_v2c_port: SNMP v2c query port (default = 161).
            trap_v1_status: Enable/disable SNMP v1 traps.
            trap_v1_lport: SNMP v1 trap local port (default = 162).
            trap_v1_rport: SNMP v1 trap remote port (default = 162).
            trap_v2c_status: Enable/disable SNMP v2c traps.
            trap_v2c_lport: SNMP v2c trap local port (default = 162).
            trap_v2c_rport: SNMP v2c trap remote port (default = 162).
            events: SNMP trap events.
            mib_view: SNMP access control MIB view.
            vdoms: SNMP access control VDOMs.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If id is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_snmp_community.put(
            ...     id=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "id": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_snmp_community.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if hosts is not None:
            hosts = normalize_table_field(
                hosts,
                mkey="id",
                required_fields=['id', 'ip', 'interface'],
                field_name="hosts",
                example="[{'id': 1, 'ip': '192.168.1.10', 'interface': 'value'}]",
            )
        if hosts6 is not None:
            hosts6 = normalize_table_field(
                hosts6,
                mkey="id",
                required_fields=['id', 'ipv6', 'interface'],
                field_name="hosts6",
                example="[{'id': 1, 'ipv6': 'value', 'interface': 'value'}]",
            )
        if vdoms is not None:
            vdoms = normalize_table_field(
                vdoms,
                mkey="name",
                required_fields=['name'],
                field_name="vdoms",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            id=id,
            name=name,
            status=status,
            hosts=hosts,
            hosts6=hosts6,
            query_v1_status=query_v1_status,
            query_v1_port=query_v1_port,
            query_v2c_status=query_v2c_status,
            query_v2c_port=query_v2c_port,
            trap_v1_status=trap_v1_status,
            trap_v1_lport=trap_v1_lport,
            trap_v1_rport=trap_v1_rport,
            trap_v2c_status=trap_v2c_status,
            trap_v2c_lport=trap_v2c_lport,
            trap_v2c_rport=trap_v2c_rport,
            events=events,
            mib_view=mib_view,
            vdoms=vdoms,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.community import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/snmp/community",
            )
        
        id_value = payload_data.get("id")
        if not id_value:
            raise ValueError("id is required for PUT")
        endpoint = "/system.snmp/community/" + quote_path_param(id_value)

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
    # POST Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def post(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        id: int | None = None,
        name: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        hosts: str | list[str] | list[dict[str, Any]] | None = None,
        hosts6: str | list[str] | list[dict[str, Any]] | None = None,
        query_v1_status: Literal["enable", "disable"] | None = None,
        query_v1_port: int | None = None,
        query_v2c_status: Literal["enable", "disable"] | None = None,
        query_v2c_port: int | None = None,
        trap_v1_status: Literal["enable", "disable"] | None = None,
        trap_v1_lport: int | None = None,
        trap_v1_rport: int | None = None,
        trap_v2c_status: Literal["enable", "disable"] | None = None,
        trap_v2c_lport: int | None = None,
        trap_v2c_rport: int | None = None,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "vpn-tun-up", "vpn-tun-down", "ha-switch", "ha-hb-failure", "ips-signature", "ips-anomaly", "av-virus", "av-oversize", "av-pattern", "av-fragmented", "fm-if-change", "fm-conf-change", "bgp-established", "bgp-backward-transition", "ha-member-up", "ha-member-down", "ent-conf-change", "av-conserve", "av-bypass", "av-oversize-passed", "av-oversize-blocked", "ips-pkg-update", "ips-fail-open", "faz-disconnect", "faz", "wc-ap-up", "wc-ap-down", "fswctl-session-up", "fswctl-session-down", "load-balance-real-server-down", "device-new", "per-cpu-high", "dhcp", "pool-usage", "ippool", "interface", "ospf-nbr-state-change", "ospf-virtnbr-state-change", "bfd"] | list[str] | None = None,
        mib_view: str | None = None,
        vdoms: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/snmp/community object.

        SNMP community configuration.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            id: Community ID.
            name: Community name.
            status: Enable/disable this SNMP community.
            hosts: Configure IPv4 SNMP managers (hosts).
                Default format: [{'id': 1, 'ip': '192.168.1.10', 'interface': 'value'}]
                Required format: List of dicts with keys: id, ip, interface
                  (String format not allowed due to multiple required fields)
            hosts6: Configure IPv6 SNMP managers.
                Default format: [{'id': 1, 'ipv6': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: id, ipv6, interface
                  (String format not allowed due to multiple required fields)
            query_v1_status: Enable/disable SNMP v1 queries.
            query_v1_port: SNMP v1 query port (default = 161).
            query_v2c_status: Enable/disable SNMP v2c queries.
            query_v2c_port: SNMP v2c query port (default = 161).
            trap_v1_status: Enable/disable SNMP v1 traps.
            trap_v1_lport: SNMP v1 trap local port (default = 162).
            trap_v1_rport: SNMP v1 trap remote port (default = 162).
            trap_v2c_status: Enable/disable SNMP v2c traps.
            trap_v2c_lport: SNMP v2c trap local port (default = 162).
            trap_v2c_rport: SNMP v2c trap remote port (default = 162).
            events: SNMP trap events.
            mib_view: SNMP access control MIB view.
            vdoms: SNMP access control VDOMs.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_snmp_community.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created id: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Community.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_snmp_community.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Community.required_fields()) }}
            
            Use Community.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if hosts is not None:
            hosts = normalize_table_field(
                hosts,
                mkey="id",
                required_fields=['id', 'ip', 'interface'],
                field_name="hosts",
                example="[{'id': 1, 'ip': '192.168.1.10', 'interface': 'value'}]",
            )
        if hosts6 is not None:
            hosts6 = normalize_table_field(
                hosts6,
                mkey="id",
                required_fields=['id', 'ipv6', 'interface'],
                field_name="hosts6",
                example="[{'id': 1, 'ipv6': 'value', 'interface': 'value'}]",
            )
        if vdoms is not None:
            vdoms = normalize_table_field(
                vdoms,
                mkey="name",
                required_fields=['name'],
                field_name="vdoms",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            id=id,
            name=name,
            status=status,
            hosts=hosts,
            hosts6=hosts6,
            query_v1_status=query_v1_status,
            query_v1_port=query_v1_port,
            query_v2c_status=query_v2c_status,
            query_v2c_port=query_v2c_port,
            trap_v1_status=trap_v1_status,
            trap_v1_lport=trap_v1_lport,
            trap_v1_rport=trap_v1_rport,
            trap_v2c_status=trap_v2c_status,
            trap_v2c_lport=trap_v2c_lport,
            trap_v2c_rport=trap_v2c_rport,
            events=events,
            mib_view=mib_view,
            vdoms=vdoms,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.community import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/snmp/community",
            )

        endpoint = "/system.snmp/community"
        
        # Add explicit query parameters for POST
        params: dict[str, Any] = {}
        if q_action is not None:
            params["action"] = q_action
        if q_nkey is not None:
            params["nkey"] = q_nkey
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, params=params, vdom=False        )

    # ========================================================================
    # DELETE Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Identifier parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def delete(  # type: ignore[override]
        self,
        id: int | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete system/snmp/community object.

        SNMP community configuration.

        Args:
            id: Primary key identifier
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If id is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.system_snmp_community.delete(id=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not id:
            raise ValueError("id is required for DELETE")
        endpoint = "/system.snmp/community/" + quote_path_param(id)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=False        )

    def exists(
        self,
        id: int,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if system/snmp/community object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            id: Primary key identifier

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_snmp_community.exists(id=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_snmp_community.exists(id=1):
            ...     fgt.api.cmdb.system_snmp_community.delete(id=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system.snmp/community"
        endpoint = f"{endpoint}/{quote_path_param(id)}"
        
        try:
            # Use silent=True to suppress 404 error logging
            result = self._client.get("cmdb", endpoint, vdom=False, silent=True)
            
            # Check if result is a coroutine (async) or direct response (sync)
            # Note: Type checkers can't narrow Union[T, Coroutine[T]] in conditionals
            if hasattr(result, '__await__'):
                # Async response - return coroutine that checks status
                async def _check() -> bool:
                    r = await result  # type: ignore[misc]
                    return r.http_status == "success"  # type: ignore[union-attr]
                return _check()
            else:
                # Sync response - check status directly from FortiObject
                return result.http_status == "success"  # type: ignore[union-attr]
        except Exception:
            # Any error (404, network, etc.) means we can't confirm existence
            return False


    def set(
        self,
        payload_dict: dict[str, Any] | None = None,
        id: int | None = None,
        name: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        hosts: str | list[str] | list[dict[str, Any]] | None = None,
        hosts6: str | list[str] | list[dict[str, Any]] | None = None,
        query_v1_status: Literal["enable", "disable"] | None = None,
        query_v1_port: int | None = None,
        query_v2c_status: Literal["enable", "disable"] | None = None,
        query_v2c_port: int | None = None,
        trap_v1_status: Literal["enable", "disable"] | None = None,
        trap_v1_lport: int | None = None,
        trap_v1_rport: int | None = None,
        trap_v2c_status: Literal["enable", "disable"] | None = None,
        trap_v2c_lport: int | None = None,
        trap_v2c_rport: int | None = None,
        events: Literal["cpu-high", "mem-low", "log-full", "intf-ip", "vpn-tun-up", "vpn-tun-down", "ha-switch", "ha-hb-failure", "ips-signature", "ips-anomaly", "av-virus", "av-oversize", "av-pattern", "av-fragmented", "fm-if-change", "fm-conf-change", "bgp-established", "bgp-backward-transition", "ha-member-up", "ha-member-down", "ent-conf-change", "av-conserve", "av-bypass", "av-oversize-passed", "av-oversize-blocked", "ips-pkg-update", "ips-fail-open", "faz-disconnect", "faz", "wc-ap-up", "wc-ap-down", "fswctl-session-up", "fswctl-session-down", "load-balance-real-server-down", "device-new", "per-cpu-high", "dhcp", "pool-usage", "ippool", "interface", "ospf-nbr-state-change", "ospf-virtnbr-state-change", "bfd"] | list[str] | list[dict[str, Any]] | None = None,
        mib_view: str | None = None,
        vdoms: str | list[str] | list[dict[str, Any]] | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/snmp/community object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (id) in the payload.

        Args:
            payload_dict: Resource data including id (primary key)
            id: Field id
            name: Field name
            status: Field status
            hosts: Field hosts
            hosts6: Field hosts6
            query_v1_status: Field query-v1-status
            query_v1_port: Field query-v1-port
            query_v2c_status: Field query-v2c-status
            query_v2c_port: Field query-v2c-port
            trap_v1_status: Field trap-v1-status
            trap_v1_lport: Field trap-v1-lport
            trap_v1_rport: Field trap-v1-rport
            trap_v2c_status: Field trap-v2c-status
            trap_v2c_lport: Field trap-v2c-lport
            trap_v2c_rport: Field trap-v2c-rport
            events: Field events
            mib_view: Field mib-view
            vdoms: Field vdoms
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If id is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_snmp_community.set(
            ...     id=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "id": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_snmp_community.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_snmp_community.set(payload_dict=obj_data)
            >>> # Safely applies configuration regardless of current state

        Note:
            This method internally calls exists() then either post() or put().
            For performance-critical code with known state, call post() or put() directly.

        See Also:
            - post(): Create new object
            - put(): Update existing object
            - exists(): Check existence manually
        """
        # Apply normalization for table fields (supports flexible input formats)
        if hosts is not None:
            hosts = normalize_table_field(
                hosts,
                mkey="id",
                required_fields=['id', 'ip', 'interface'],
                field_name="hosts",
                example="[{'id': 1, 'ip': '192.168.1.10', 'interface': 'value'}]",
            )
        if hosts6 is not None:
            hosts6 = normalize_table_field(
                hosts6,
                mkey="id",
                required_fields=['id', 'ipv6', 'interface'],
                field_name="hosts6",
                example="[{'id': 1, 'ipv6': 'value', 'interface': 'value'}]",
            )
        if vdoms is not None:
            vdoms = normalize_table_field(
                vdoms,
                mkey="name",
                required_fields=['name'],
                field_name="vdoms",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            id=id,
            name=name,
            status=status,
            hosts=hosts,
            hosts6=hosts6,
            query_v1_status=query_v1_status,
            query_v1_port=query_v1_port,
            query_v2c_status=query_v2c_status,
            query_v2c_port=query_v2c_port,
            trap_v1_status=trap_v1_status,
            trap_v1_lport=trap_v1_lport,
            trap_v1_rport=trap_v1_rport,
            trap_v2c_status=trap_v2c_status,
            trap_v2c_lport=trap_v2c_lport,
            trap_v2c_rport=trap_v2c_rport,
            events=events,
            mib_view=mib_view,
            vdoms=vdoms,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("id")
        if not mkey_value:
            raise ValueError("id is required for set()")
        
        # Check if resource exists
        if self.exists(id=mkey_value):
            # Update existing resource
            return self.put(payload_dict=payload_data, **kwargs)
        else:
            # Create new resource
            return self.post(payload_dict=payload_data, **kwargs)

    # ========================================================================
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        id: int,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/snmp/community object to a new position.
        
        Reorders objects by moving one before/after another, to top/bottom, or to a specific position.
        
        Args:
            id: Identifier of object to move
            position: Where to move the object:
                - "before": Move before reference object (requires reference_id)
                - "after": Move after reference object (requires reference_id)
                - "top": Move to first position (reference not needed)
                - "bottom": Move to last position (reference not needed)
                - int (1-based): Move to specific position number (e.g., position=3 for 3rd place)
            reference_id: Identifier of reference object (required for before/after)
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.system_snmp_community.move(
            ...     id=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.system_snmp_community.move(
            ...     id=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.system_snmp_community.move(
            ...     id=100,
            ...     position="before",
            ...     reference_id=50
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
                reference_id = all_objects[0].id
                actual_position = "before"
            elif position > len(all_objects):
                # Move to last position (after all existing objects)
                reference_id = all_objects[-1].id
                actual_position = "after"
            else:
                # Move before the object currently at that position
                reference_id = all_objects[position - 1].id
                actual_position = "before"
        
        # Handle top/bottom string positions
        elif position in ("top", "bottom"):
            # Get all objects to find first/last
            all_objects = self.get()
            if not all_objects:
                raise ValueError(f"Cannot move to {position} - no objects found")
            
            if position == "top":
                # Move before first object
                reference_id = all_objects[0].id
                actual_position = "before"
            else:  # bottom
                # Move after last object
                reference_id = all_objects[-1].id
                actual_position = "after"
        
        # Handle before/after string positions
        else:
            # Validate reference is provided for before/after
            if reference_id is None:
                raise ValueError(f"reference_id is required when position='{position}'")
            actual_position = position
        
        # Build params for move operation
        params = {
            "action": "move",
            actual_position: reference_id,
            **kwargs,
        }
        
        # Move requires the mkey in the endpoint path
        endpoint = "/system.snmp/community/" + quote_path_param(id)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )





