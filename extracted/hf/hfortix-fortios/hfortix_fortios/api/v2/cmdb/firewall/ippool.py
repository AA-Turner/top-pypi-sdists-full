"""
FortiOS CMDB - Firewall ippool

Configuration endpoint for managing cmdb firewall/ippool objects.

API Endpoints:
    GET    /cmdb/firewall/ippool
    POST   /cmdb/firewall/ippool
    PUT    /cmdb/firewall/ippool/{identifier}
    DELETE /cmdb/firewall/ippool/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.firewall_ippool.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.firewall_ippool.post(
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

class Ippool(CRUDEndpoint, MetadataMixin):
    """Ippool Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "ippool"
    
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
        """Initialize Ippool endpoint."""
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
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve firewall/ippool configuration.

        Configure IPv4 IP pools.

        Args:
            name: String identifier to retrieve specific object.
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
            >>> # Get all firewall/ippool objects
            >>> result = fgt.api.cmdb.firewall_ippool.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific firewall/ippool by name
            >>> result = fgt.api.cmdb.firewall_ippool.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.firewall_ippool.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.firewall_ippool.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.firewall_ippool.get_schema()

        See Also:
            - post(): Create new firewall/ippool object
            - put(): Update existing firewall/ippool object
            - delete(): Remove firewall/ippool object
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
        
        if name:
            endpoint = "/firewall/ippool/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/firewall/ippool"
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
            >>> schema = fgt.api.cmdb.firewall_ippool.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.firewall_ippool.get_schema(format="json-schema")
        
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
        name: str | None = None,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = None,
        startip: str | None = None,
        endip: str | None = None,
        startport: int | None = None,
        endport: int | None = None,
        source_startip: str | None = None,
        source_endip: str | None = None,
        block_size: int | None = None,
        port_per_user: int | None = None,
        num_blocks_per_user: int | None = None,
        pba_timeout: int | None = None,
        pba_interim_log: int | None = None,
        permit_any_host: Literal["disable", "enable"] | None = None,
        arp_reply: Literal["disable", "enable"] | None = None,
        arp_intf: str | None = None,
        associated_interface: str | None = None,
        comments: str | None = None,
        nat64: Literal["disable", "enable"] | None = None,
        add_nat64_route: Literal["disable", "enable"] | None = None,
        source_prefix6: str | None = None,
        client_prefix_length: int | None = None,
        tcp_session_quota: int | None = None,
        udp_session_quota: int | None = None,
        icmp_session_quota: int | None = None,
        privileged_port_use_pba: Literal["disable", "enable"] | None = None,
        subnet_broadcast_in_ippool: Literal["disable"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing firewall/ippool object.

        Configure IPv4 IP pools.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: IP pool name.
            type: IP pool type: overload, one-to-one, fixed-port-range, port-block-allocation, cgn-resource-allocation (hyperscale vdom only)
            startip: First IPv4 address (inclusive) in the range for the address pool (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).
            endip: Final IPv4 address (inclusive) in the range for the address pool (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).
            startport: First port number (inclusive) in the range for the address pool (1024 - 65535, Default: 5117).
            endport: Final port number (inclusive) in the range for the address pool (1024 - 65535, Default: 65533).
            source_startip: First IPv4 address (inclusive) in the range of the source addresses to be translated (format = xxx.xxx.xxx.xxx, default = 0.0.0.0).
            source_endip: Final IPv4 address (inclusive) in the range of the source addresses to be translated (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).
            block_size: Number of addresses in a block (64 - 4096, default = 128).
            port_per_user: Number of port for each user (32 - 60416, default = 0, which is auto).
            num_blocks_per_user: Number of addresses blocks that can be used by a user (1 to 128, default = 8).
            pba_timeout: Port block allocation timeout (seconds).
            pba_interim_log: Port block allocation interim logging interval (600 - 86400 seconds, default = 0 which disables interim logging).
            permit_any_host: Enable/disable fullcone NAT. Accept UDP packets from any host.
            arp_reply: Enable/disable replying to ARP requests when an IP Pool is added to a policy (default = enable).
            arp_intf: Select an interface from available options that will reply to ARP requests. (If blank, any is selected).
            associated_interface: Associated interface name.
            comments: Comment.
            nat64: Enable/disable NAT64.
            add_nat64_route: Enable/disable adding NAT64 route.
            source_prefix6: Source IPv6 network to be translated (format = xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx, default = ::/0).
            client_prefix_length: Subnet length of a single deterministic NAT64 client (1 - 128, default = 64).
            tcp_session_quota: Maximum number of concurrent TCP sessions allowed per client (0 - 2097000, default = 0 which means no limit).
            udp_session_quota: Maximum number of concurrent UDP sessions allowed per client (0 - 2097000, default = 0 which means no limit).
            icmp_session_quota: Maximum number of concurrent ICMP sessions allowed per client (0 - 2097000, default = 0 which means no limit).
            privileged_port_use_pba: Enable/disable selection of the external port from the port block allocation for NAT'ing privileged ports (deafult = disable).
            subnet_broadcast_in_ippool: Enable/disable inclusion of the subnetwork address and broadcast IP address in the NAT64 IP pool.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.firewall_ippool.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.firewall_ippool.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            type=type,
            startip=startip,
            endip=endip,
            startport=startport,
            endport=endport,
            source_startip=source_startip,
            source_endip=source_endip,
            block_size=block_size,
            port_per_user=port_per_user,
            num_blocks_per_user=num_blocks_per_user,
            pba_timeout=pba_timeout,
            pba_interim_log=pba_interim_log,
            permit_any_host=permit_any_host,
            arp_reply=arp_reply,
            arp_intf=arp_intf,
            associated_interface=associated_interface,
            comments=comments,
            nat64=nat64,
            add_nat64_route=add_nat64_route,
            source_prefix6=source_prefix6,
            client_prefix_length=client_prefix_length,
            tcp_session_quota=tcp_session_quota,
            udp_session_quota=udp_session_quota,
            icmp_session_quota=icmp_session_quota,
            privileged_port_use_pba=privileged_port_use_pba,
            subnet_broadcast_in_ippool=subnet_broadcast_in_ippool,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.ippool import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/ippool",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/firewall/ippool/" + quote_path_param(name_value)

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
        name: str | None = None,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = None,
        startip: str | None = None,
        endip: str | None = None,
        startport: int | None = None,
        endport: int | None = None,
        source_startip: str | None = None,
        source_endip: str | None = None,
        block_size: int | None = None,
        port_per_user: int | None = None,
        num_blocks_per_user: int | None = None,
        pba_timeout: int | None = None,
        pba_interim_log: int | None = None,
        permit_any_host: Literal["disable", "enable"] | None = None,
        arp_reply: Literal["disable", "enable"] | None = None,
        arp_intf: str | None = None,
        associated_interface: str | None = None,
        comments: str | None = None,
        nat64: Literal["disable", "enable"] | None = None,
        add_nat64_route: Literal["disable", "enable"] | None = None,
        source_prefix6: str | None = None,
        client_prefix_length: int | None = None,
        tcp_session_quota: int | None = None,
        udp_session_quota: int | None = None,
        icmp_session_quota: int | None = None,
        privileged_port_use_pba: Literal["disable", "enable"] | None = None,
        subnet_broadcast_in_ippool: Literal["disable"] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new firewall/ippool object.

        Configure IPv4 IP pools.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: IP pool name.
            type: IP pool type: overload, one-to-one, fixed-port-range, port-block-allocation, cgn-resource-allocation (hyperscale vdom only)
            startip: First IPv4 address (inclusive) in the range for the address pool (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).
            endip: Final IPv4 address (inclusive) in the range for the address pool (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).
            startport: First port number (inclusive) in the range for the address pool (1024 - 65535, Default: 5117).
            endport: Final port number (inclusive) in the range for the address pool (1024 - 65535, Default: 65533).
            source_startip: First IPv4 address (inclusive) in the range of the source addresses to be translated (format = xxx.xxx.xxx.xxx, default = 0.0.0.0).
            source_endip: Final IPv4 address (inclusive) in the range of the source addresses to be translated (format xxx.xxx.xxx.xxx, Default: 0.0.0.0).
            block_size: Number of addresses in a block (64 - 4096, default = 128).
            port_per_user: Number of port for each user (32 - 60416, default = 0, which is auto).
            num_blocks_per_user: Number of addresses blocks that can be used by a user (1 to 128, default = 8).
            pba_timeout: Port block allocation timeout (seconds).
            pba_interim_log: Port block allocation interim logging interval (600 - 86400 seconds, default = 0 which disables interim logging).
            permit_any_host: Enable/disable fullcone NAT. Accept UDP packets from any host.
            arp_reply: Enable/disable replying to ARP requests when an IP Pool is added to a policy (default = enable).
            arp_intf: Select an interface from available options that will reply to ARP requests. (If blank, any is selected).
            associated_interface: Associated interface name.
            comments: Comment.
            nat64: Enable/disable NAT64.
            add_nat64_route: Enable/disable adding NAT64 route.
            source_prefix6: Source IPv6 network to be translated (format = xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx, default = ::/0).
            client_prefix_length: Subnet length of a single deterministic NAT64 client (1 - 128, default = 64).
            tcp_session_quota: Maximum number of concurrent TCP sessions allowed per client (0 - 2097000, default = 0 which means no limit).
            udp_session_quota: Maximum number of concurrent UDP sessions allowed per client (0 - 2097000, default = 0 which means no limit).
            icmp_session_quota: Maximum number of concurrent ICMP sessions allowed per client (0 - 2097000, default = 0 which means no limit).
            privileged_port_use_pba: Enable/disable selection of the external port from the port block allocation for NAT'ing privileged ports (deafult = disable).
            subnet_broadcast_in_ippool: Enable/disable inclusion of the subnetwork address and broadcast IP address in the NAT64 IP pool.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.firewall_ippool.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Ippool.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.firewall_ippool.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Ippool.required_fields()) }}
            
            Use Ippool.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            type=type,
            startip=startip,
            endip=endip,
            startport=startport,
            endport=endport,
            source_startip=source_startip,
            source_endip=source_endip,
            block_size=block_size,
            port_per_user=port_per_user,
            num_blocks_per_user=num_blocks_per_user,
            pba_timeout=pba_timeout,
            pba_interim_log=pba_interim_log,
            permit_any_host=permit_any_host,
            arp_reply=arp_reply,
            arp_intf=arp_intf,
            associated_interface=associated_interface,
            comments=comments,
            nat64=nat64,
            add_nat64_route=add_nat64_route,
            source_prefix6=source_prefix6,
            client_prefix_length=client_prefix_length,
            tcp_session_quota=tcp_session_quota,
            udp_session_quota=udp_session_quota,
            icmp_session_quota=icmp_session_quota,
            privileged_port_use_pba=privileged_port_use_pba,
            subnet_broadcast_in_ippool=subnet_broadcast_in_ippool,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.ippool import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/ippool",
            )

        endpoint = "/firewall/ippool"
        
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
        name: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete firewall/ippool object.

        Configure IPv4 IP pools.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.firewall_ippool.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/firewall/ippool/" + quote_path_param(name)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        name: str,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if firewall/ippool object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.firewall_ippool.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.firewall_ippool.exists(name=1):
            ...     fgt.api.cmdb.firewall_ippool.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/firewall/ippool"
        endpoint = f"{endpoint}/{quote_path_param(name)}"
        
        try:
            result = self.get(name=name, vdom=vdom)
            
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
        name: str | None = None,
        type: Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation"] | None = None,
        startip: str | None = None,
        endip: str | None = None,
        startport: int | None = None,
        endport: int | None = None,
        source_startip: str | None = None,
        source_endip: str | None = None,
        block_size: int | None = None,
        port_per_user: int | None = None,
        num_blocks_per_user: int | None = None,
        pba_timeout: int | None = None,
        pba_interim_log: int | None = None,
        permit_any_host: Literal["disable", "enable"] | None = None,
        arp_reply: Literal["disable", "enable"] | None = None,
        arp_intf: str | None = None,
        associated_interface: str | None = None,
        comments: str | None = None,
        nat64: Literal["disable", "enable"] | None = None,
        add_nat64_route: Literal["disable", "enable"] | None = None,
        source_prefix6: str | None = None,
        client_prefix_length: int | None = None,
        tcp_session_quota: int | None = None,
        udp_session_quota: int | None = None,
        icmp_session_quota: int | None = None,
        privileged_port_use_pba: Literal["disable", "enable"] | None = None,
        subnet_broadcast_in_ippool: Literal["disable"] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update firewall/ippool object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            type: Field type
            startip: Field startip
            endip: Field endip
            startport: Field startport
            endport: Field endport
            source_startip: Field source-startip
            source_endip: Field source-endip
            block_size: Field block-size
            port_per_user: Field port-per-user
            num_blocks_per_user: Field num-blocks-per-user
            pba_timeout: Field pba-timeout
            pba_interim_log: Field pba-interim-log
            permit_any_host: Field permit-any-host
            arp_reply: Field arp-reply
            arp_intf: Field arp-intf
            associated_interface: Field associated-interface
            comments: Field comments
            nat64: Field nat64
            add_nat64_route: Field add-nat64-route
            source_prefix6: Field source-prefix6
            client_prefix_length: Field client-prefix-length
            tcp_session_quota: Field tcp-session-quota
            udp_session_quota: Field udp-session-quota
            icmp_session_quota: Field icmp-session-quota
            privileged_port_use_pba: Field privileged-port-use-pba
            subnet_broadcast_in_ippool: Field subnet-broadcast-in-ippool
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.firewall_ippool.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.firewall_ippool.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.firewall_ippool.set(payload_dict=obj_data)
            >>> # Safely applies configuration regardless of current state

        Note:
            This method internally calls exists() then either post() or put().
            For performance-critical code with known state, call post() or put() directly.

        See Also:
            - post(): Create new object
            - put(): Update existing object
            - exists(): Check existence manually
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            type=type,
            startip=startip,
            endip=endip,
            startport=startport,
            endport=endport,
            source_startip=source_startip,
            source_endip=source_endip,
            block_size=block_size,
            port_per_user=port_per_user,
            num_blocks_per_user=num_blocks_per_user,
            pba_timeout=pba_timeout,
            pba_interim_log=pba_interim_log,
            permit_any_host=permit_any_host,
            arp_reply=arp_reply,
            arp_intf=arp_intf,
            associated_interface=associated_interface,
            comments=comments,
            nat64=nat64,
            add_nat64_route=add_nat64_route,
            source_prefix6=source_prefix6,
            client_prefix_length=client_prefix_length,
            tcp_session_quota=tcp_session_quota,
            udp_session_quota=udp_session_quota,
            icmp_session_quota=icmp_session_quota,
            privileged_port_use_pba=privileged_port_use_pba,
            subnet_broadcast_in_ippool=subnet_broadcast_in_ippool,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("name")
        if not mkey_value:
            raise ValueError("name is required for set()")
        
        # Check if resource exists
        if self.exists(name=mkey_value, vdom=vdom):
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
        name: str,
        action: Literal["before", "after"],
        reference_name: str,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move firewall/ippool object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            name: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_name: Identifier of reference object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.firewall_ippool.move(
            ...     name=100,
            ...     action="before",
            ...     reference_name=50
            ... )
        """
        # Build params for move operation
        params = {
            "name": name,
            "action": "move",
            action: reference_name,
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/firewall/ippool"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        name: str,
        new_name: str,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone firewall/ippool object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            name: Identifier of object to clone
            new_name: Identifier for the cloned object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.firewall_ippool.clone(
            ...     name=1,
            ...     new_name=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "name": name,
            "new_name": new_name,
            "action": "clone",
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/firewall/ippool"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




