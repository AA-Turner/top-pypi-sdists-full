"""
FortiOS CMDB - System dhcp6 server

Configuration endpoint for managing cmdb system/dhcp6/server objects.

API Endpoints:
    GET    /cmdb/system/dhcp6/server
    POST   /cmdb/system/dhcp6/server
    PUT    /cmdb/system/dhcp6/server/{identifier}
    DELETE /cmdb/system/dhcp6/server/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_dhcp6_server.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_dhcp6_server.post(
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

class Server(CRUDEndpoint, MetadataMixin):
    """Server Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "server"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "options": {
            "mkey": "id",
            "required_fields": ['id', 'code'],
            "example": "[{'id': 1, 'code': 1}]",
        },
        "prefix_range": {
            "mkey": "id",
            "required_fields": ['id', 'start-prefix', 'end-prefix', 'prefix-length'],
            "example": "[{'id': 1, 'start-prefix': 'value', 'end-prefix': 'value', 'prefix-length': 1}]",
        },
        "ip_range": {
            "mkey": "id",
            "required_fields": ['id', 'start-ip', 'end-ip'],
            "example": "[{'id': 1, 'start-ip': 'value', 'end-ip': 'value'}]",
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
    SUPPORTS_CLONE = True
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Server endpoint."""
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
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve system/dhcp6/server configuration.

        Configure DHCPv6 servers.

        Args:
            id: Integer identifier to retrieve specific object.
                If None, returns all objects.
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
            >>> # Get all system/dhcp6/server objects
            >>> result = fgt.api.cmdb.system_dhcp6_server.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/dhcp6/server by id
            >>> result = fgt.api.cmdb.system_dhcp6_server.get(id=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_dhcp6_server.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_dhcp6_server.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_dhcp6_server.get_schema()

        See Also:
            - post(): Create new system/dhcp6/server object
            - put(): Update existing system/dhcp6/server object
            - delete(): Remove system/dhcp6/server object
            - exists(): Check if object exists
            - get_schema(): Get endpoint schema/metadata
        """
        params = payload_dict.copy() if payload_dict else {}
        
        # Add explicit query parameters
        if filter is not None:
            params["filter"] = filter
        if count is not None:
            params["count"] = count
        if start is not None:
            params["start"] = start
        
        if id:
            endpoint = "/system.dhcp6/server/" + quote_path_param(id)
            unwrap_single = True
        else:
            endpoint = "/system.dhcp6/server"
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
            >>> schema = fgt.api.cmdb.system_dhcp6_server.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_dhcp6_server.get_schema(format="json-schema")
        
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
        id: int | None = None,
        status: Literal["disable", "enable"] | None = None,
        rapid_commit: Literal["disable", "enable"] | None = None,
        lease_time: int | None = None,
        dns_service: Literal["delegated", "default", "specify"] | None = None,
        dns_search_list: Literal["delegated", "specify"] | None = None,
        dns_server1: str | None = None,
        dns_server2: str | None = None,
        dns_server3: str | None = None,
        dns_server4: str | None = None,
        domain: str | None = None,
        subnet: str | None = None,
        interface: str | None = None,
        delegated_prefix_route: Literal["disable", "enable"] | None = None,
        options: str | list[str] | list[dict[str, Any]] | None = None,
        upstream_interface: str | None = None,
        delegated_prefix_iaid: int | None = None,
        ip_mode: Literal["range", "delegated"] | None = None,
        prefix_mode: Literal["dhcp6", "ra"] | None = None,
        prefix_range: str | list[str] | list[dict[str, Any]] | None = None,
        ip_range: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/dhcp6/server object.

        Configure DHCPv6 servers.

        Args:
            payload_dict: Object data as dict. Must include id (primary key).
            id: ID.
            status: Enable/disable this DHCPv6 configuration.
            rapid_commit: Enable/disable allow/disallow rapid commit.
            lease_time: Lease time in seconds, 0 means unlimited.
            dns_service: Options for assigning DNS servers to DHCPv6 clients.
            dns_search_list: DNS search list options.
            dns_server1: DNS server 1.
            dns_server2: DNS server 2.
            dns_server3: DNS server 3.
            dns_server4: DNS server 4.
            domain: Domain name suffix for the IP addresses that the DHCP server assigns to clients.
            subnet: Subnet or subnet-id if the IP mode is delegated.
            interface: DHCP server can assign IP configurations to clients connected to this interface.
            delegated_prefix_route: Enable/disable automatically adding of routing for delegated prefix.
            options: DHCPv6 options.
                Default format: [{'id': 1, 'code': 1}]
                Required format: List of dicts with keys: id, code
                  (String format not allowed due to multiple required fields)
            upstream_interface: Interface name from where delegated information is provided.
            delegated_prefix_iaid: IAID of obtained delegated-prefix from the upstream interface.
            ip_mode: Method used to assign client IP.
            prefix_mode: Assigning a prefix from a DHCPv6 client or RA.
            prefix_range: DHCP prefix configuration.
                Default format: [{'id': 1, 'start-prefix': 'value', 'end-prefix': 'value', 'prefix-length': 1}]
                Required format: List of dicts with keys: id, start-prefix, end-prefix, prefix-length
                  (String format not allowed due to multiple required fields)
            ip_range: DHCP IP range configuration.
                Default format: [{'id': 1, 'start-ip': 'value', 'end-ip': 'value'}]
                Required format: List of dicts with keys: id, start-ip, end-ip
                  (String format not allowed due to multiple required fields)
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If id is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_dhcp6_server.put(
            ...     id=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "id": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_dhcp6_server.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if options is not None:
            options = normalize_table_field(
                options,
                mkey="id",
                required_fields=['id', 'code'],
                field_name="options",
                example="[{'id': 1, 'code': 1}]",
            )
        if prefix_range is not None:
            prefix_range = normalize_table_field(
                prefix_range,
                mkey="id",
                required_fields=['id', 'start-prefix', 'end-prefix', 'prefix-length'],
                field_name="prefix_range",
                example="[{'id': 1, 'start-prefix': 'value', 'end-prefix': 'value', 'prefix-length': 1}]",
            )
        if ip_range is not None:
            ip_range = normalize_table_field(
                ip_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="ip_range",
                example="[{'id': 1, 'start-ip': 'value', 'end-ip': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            id=id,
            status=status,
            rapid_commit=rapid_commit,
            lease_time=lease_time,
            dns_service=dns_service,
            dns_search_list=dns_search_list,
            dns_server1=dns_server1,
            dns_server2=dns_server2,
            dns_server3=dns_server3,
            dns_server4=dns_server4,
            domain=domain,
            subnet=subnet,
            interface=interface,
            delegated_prefix_route=delegated_prefix_route,
            options=options,
            upstream_interface=upstream_interface,
            delegated_prefix_iaid=delegated_prefix_iaid,
            ip_mode=ip_mode,
            prefix_mode=prefix_mode,
            prefix_range=prefix_range,
            ip_range=ip_range,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.server import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/dhcp6/server",
            )
        
        id_value = payload_data.get("id")
        if not id_value:
            raise ValueError("id is required for PUT")
        endpoint = "/system.dhcp6/server/" + quote_path_param(id_value)

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
    # POST Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def post(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        id: int | None = None,
        status: Literal["disable", "enable"] | None = None,
        rapid_commit: Literal["disable", "enable"] | None = None,
        lease_time: int | None = None,
        dns_service: Literal["delegated", "default", "specify"] | None = None,
        dns_search_list: Literal["delegated", "specify"] | None = None,
        dns_server1: str | None = None,
        dns_server2: str | None = None,
        dns_server3: str | None = None,
        dns_server4: str | None = None,
        domain: str | None = None,
        subnet: str | None = None,
        interface: str | None = None,
        delegated_prefix_route: Literal["disable", "enable"] | None = None,
        options: str | list[str] | list[dict[str, Any]] | None = None,
        upstream_interface: str | None = None,
        delegated_prefix_iaid: int | None = None,
        ip_mode: Literal["range", "delegated"] | None = None,
        prefix_mode: Literal["dhcp6", "ra"] | None = None,
        prefix_range: str | list[str] | list[dict[str, Any]] | None = None,
        ip_range: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/dhcp6/server object.

        Configure DHCPv6 servers.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            id: ID.
            status: Enable/disable this DHCPv6 configuration.
            rapid_commit: Enable/disable allow/disallow rapid commit.
            lease_time: Lease time in seconds, 0 means unlimited.
            dns_service: Options for assigning DNS servers to DHCPv6 clients.
            dns_search_list: DNS search list options.
            dns_server1: DNS server 1.
            dns_server2: DNS server 2.
            dns_server3: DNS server 3.
            dns_server4: DNS server 4.
            domain: Domain name suffix for the IP addresses that the DHCP server assigns to clients.
            subnet: Subnet or subnet-id if the IP mode is delegated.
            interface: DHCP server can assign IP configurations to clients connected to this interface.
            delegated_prefix_route: Enable/disable automatically adding of routing for delegated prefix.
            options: DHCPv6 options.
                Default format: [{'id': 1, 'code': 1}]
                Required format: List of dicts with keys: id, code
                  (String format not allowed due to multiple required fields)
            upstream_interface: Interface name from where delegated information is provided.
            delegated_prefix_iaid: IAID of obtained delegated-prefix from the upstream interface.
            ip_mode: Method used to assign client IP.
            prefix_mode: Assigning a prefix from a DHCPv6 client or RA.
            prefix_range: DHCP prefix configuration.
                Default format: [{'id': 1, 'start-prefix': 'value', 'end-prefix': 'value', 'prefix-length': 1}]
                Required format: List of dicts with keys: id, start-prefix, end-prefix, prefix-length
                  (String format not allowed due to multiple required fields)
            ip_range: DHCP IP range configuration.
                Default format: [{'id': 1, 'start-ip': 'value', 'end-ip': 'value'}]
                Required format: List of dicts with keys: id, start-ip, end-ip
                  (String format not allowed due to multiple required fields)
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_dhcp6_server.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created id: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Server.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_dhcp6_server.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Server.required_fields()) }}
            
            Use Server.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if options is not None:
            options = normalize_table_field(
                options,
                mkey="id",
                required_fields=['id', 'code'],
                field_name="options",
                example="[{'id': 1, 'code': 1}]",
            )
        if prefix_range is not None:
            prefix_range = normalize_table_field(
                prefix_range,
                mkey="id",
                required_fields=['id', 'start-prefix', 'end-prefix', 'prefix-length'],
                field_name="prefix_range",
                example="[{'id': 1, 'start-prefix': 'value', 'end-prefix': 'value', 'prefix-length': 1}]",
            )
        if ip_range is not None:
            ip_range = normalize_table_field(
                ip_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="ip_range",
                example="[{'id': 1, 'start-ip': 'value', 'end-ip': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            id=id,
            status=status,
            rapid_commit=rapid_commit,
            lease_time=lease_time,
            dns_service=dns_service,
            dns_search_list=dns_search_list,
            dns_server1=dns_server1,
            dns_server2=dns_server2,
            dns_server3=dns_server3,
            dns_server4=dns_server4,
            domain=domain,
            subnet=subnet,
            interface=interface,
            delegated_prefix_route=delegated_prefix_route,
            options=options,
            upstream_interface=upstream_interface,
            delegated_prefix_iaid=delegated_prefix_iaid,
            ip_mode=ip_mode,
            prefix_mode=prefix_mode,
            prefix_range=prefix_range,
            ip_range=ip_range,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.server import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/dhcp6/server",
            )

        endpoint = "/system.dhcp6/server"
        
        # Add explicit query parameters for POST
        params: dict[str, Any] = {}
        if q_action is not None:
            params["action"] = q_action
        if q_nkey is not None:
            params["nkey"] = q_nkey
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, params=params, vdom=vdom        )

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
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete system/dhcp6/server object.

        Configure DHCPv6 servers.

        Args:
            id: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If id is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.system_dhcp6_server.delete(id=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not id:
            raise ValueError("id is required for DELETE")
        endpoint = "/system.dhcp6/server/" + quote_path_param(id)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        id: int,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if system/dhcp6/server object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            id: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_dhcp6_server.exists(id=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_dhcp6_server.exists(id=1):
            ...     fgt.api.cmdb.system_dhcp6_server.delete(id=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system.dhcp6/server"
        endpoint = f"{endpoint}/{quote_path_param(id)}"
        
        try:
            result = self.get(id=id, vdom=vdom)
            
            # Check if result is a coroutine (async) or direct response (sync)
            # Note: Type checkers can't narrow Union[T, Coroutine[T]] in conditionals
            if hasattr(result, '__await__'):
                # Async response - return coroutine that checks status
                async def _check() -> bool:
                    r = await result  # type: ignore[misc]
                    response = r.raw if hasattr(r, 'raw') else r
                    return is_success(response)
                return _check()
            else:
                # Sync response - check status directly
                response = result.raw if hasattr(result, 'raw') else result  # type: ignore[union-attr]
                return is_success(response)
        except Exception:
            # Any error (404, network, etc.) means we can't confirm existence
            return False


    def set(
        self,
        payload_dict: dict[str, Any] | None = None,
        id: int | None = None,
        status: Literal["disable", "enable"] | None = None,
        rapid_commit: Literal["disable", "enable"] | None = None,
        lease_time: int | None = None,
        dns_service: Literal["delegated", "default", "specify"] | None = None,
        dns_search_list: Literal["delegated", "specify"] | None = None,
        dns_server1: str | None = None,
        dns_server2: str | None = None,
        dns_server3: str | None = None,
        dns_server4: str | None = None,
        domain: str | None = None,
        subnet: str | None = None,
        interface: str | None = None,
        delegated_prefix_route: Literal["disable", "enable"] | None = None,
        options: str | list[str] | list[dict[str, Any]] | None = None,
        upstream_interface: str | None = None,
        delegated_prefix_iaid: int | None = None,
        ip_mode: Literal["range", "delegated"] | None = None,
        prefix_mode: Literal["dhcp6", "ra"] | None = None,
        prefix_range: str | list[str] | list[dict[str, Any]] | None = None,
        ip_range: str | list[str] | list[dict[str, Any]] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/dhcp6/server object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (id) in the payload.

        Args:
            payload_dict: Resource data including id (primary key)
            id: Field id
            status: Field status
            rapid_commit: Field rapid-commit
            lease_time: Field lease-time
            dns_service: Field dns-service
            dns_search_list: Field dns-search-list
            dns_server1: Field dns-server1
            dns_server2: Field dns-server2
            dns_server3: Field dns-server3
            dns_server4: Field dns-server4
            domain: Field domain
            subnet: Field subnet
            interface: Field interface
            delegated_prefix_route: Field delegated-prefix-route
            options: Field options
            upstream_interface: Field upstream-interface
            delegated_prefix_iaid: Field delegated-prefix-iaid
            ip_mode: Field ip-mode
            prefix_mode: Field prefix-mode
            prefix_range: Field prefix-range
            ip_range: Field ip-range
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If id is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_dhcp6_server.set(
            ...     id=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "id": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_dhcp6_server.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_dhcp6_server.set(payload_dict=obj_data)
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
        if options is not None:
            options = normalize_table_field(
                options,
                mkey="id",
                required_fields=['id', 'code'],
                field_name="options",
                example="[{'id': 1, 'code': 1}]",
            )
        if prefix_range is not None:
            prefix_range = normalize_table_field(
                prefix_range,
                mkey="id",
                required_fields=['id', 'start-prefix', 'end-prefix', 'prefix-length'],
                field_name="prefix_range",
                example="[{'id': 1, 'start-prefix': 'value', 'end-prefix': 'value', 'prefix-length': 1}]",
            )
        if ip_range is not None:
            ip_range = normalize_table_field(
                ip_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="ip_range",
                example="[{'id': 1, 'start-ip': 'value', 'end-ip': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            id=id,
            status=status,
            rapid_commit=rapid_commit,
            lease_time=lease_time,
            dns_service=dns_service,
            dns_search_list=dns_search_list,
            dns_server1=dns_server1,
            dns_server2=dns_server2,
            dns_server3=dns_server3,
            dns_server4=dns_server4,
            domain=domain,
            subnet=subnet,
            interface=interface,
            delegated_prefix_route=delegated_prefix_route,
            options=options,
            upstream_interface=upstream_interface,
            delegated_prefix_iaid=delegated_prefix_iaid,
            ip_mode=ip_mode,
            prefix_mode=prefix_mode,
            prefix_range=prefix_range,
            ip_range=ip_range,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("id")
        if not mkey_value:
            raise ValueError("id is required for set()")
        
        # Check if resource exists
        if self.exists(id=mkey_value, vdom=vdom):
            # Update existing resource
            return self.put(payload_dict=payload_data, vdom=vdom, **kwargs)
        else:
            # Create new resource
            return self.post(payload_dict=payload_data, vdom=vdom, **kwargs)

    # ========================================================================
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        id: int,
        action: Literal["before", "after"],
        reference_id: int,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/dhcp6/server object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            id: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_id: Identifier of reference object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.system_dhcp6_server.move(
            ...     id=100,
            ...     action="before",
            ...     reference_id=50
            ... )
        """
        # Build params for move operation
        params = {
            "id": id,
            "action": "move",
            action: reference_id,
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/system.dhcp6/server"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        id: int,
        new_id: int,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone system/dhcp6/server object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            id: Identifier of object to clone
            new_id: Identifier for the cloned object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.system_dhcp6_server.clone(
            ...     id=1,
            ...     new_id=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "id": id,
            "new_id": new_id,
            "action": "clone",
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/system.dhcp6/server"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




