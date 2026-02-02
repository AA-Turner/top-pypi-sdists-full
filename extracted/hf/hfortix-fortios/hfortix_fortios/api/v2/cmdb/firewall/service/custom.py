"""
FortiOS CMDB - Firewall service custom

Configuration endpoint for managing cmdb firewall/service/custom objects.

API Endpoints:
    GET    /cmdb/firewall/service/custom
    POST   /cmdb/firewall/service/custom
    PUT    /cmdb/firewall/service/custom/{identifier}
    DELETE /cmdb/firewall/service/custom/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.firewall_service_custom.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.firewall_service_custom.post(
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

class Custom(CRUDEndpoint, MetadataMixin):
    """Custom Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "custom"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "app_category": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
        },
        "application": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
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
        """Initialize Custom endpoint."""
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
        Retrieve firewall/service/custom configuration.

        Configure custom services.

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
            >>> # Get all firewall/service/custom objects
            >>> result = fgt.api.cmdb.firewall_service_custom.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific firewall/service/custom by name
            >>> result = fgt.api.cmdb.firewall_service_custom.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.firewall_service_custom.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.firewall_service_custom.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.firewall_service_custom.get_schema()

        See Also:
            - post(): Create new firewall/service/custom object
            - put(): Update existing firewall/service/custom object
            - delete(): Remove firewall/service/custom object
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
            endpoint = "/firewall.service/custom/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/firewall.service/custom"
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
            >>> schema = fgt.api.cmdb.firewall_service_custom.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.firewall_service_custom.get_schema(format="json-schema")
        
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
        uuid: str | None = None,
        proxy: Literal["enable", "disable"] | None = None,
        category: str | None = None,
        protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"] | None = None,
        helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"] | None = None,
        iprange: str | None = None,
        fqdn: str | None = None,
        protocol_number: int | None = None,
        icmptype: int | None = None,
        icmpcode: int | None = None,
        tcp_portrange: str | None = None,
        udp_portrange: str | None = None,
        udplite_portrange: str | None = None,
        sctp_portrange: str | None = None,
        tcp_halfclose_timer: int | None = None,
        tcp_halfopen_timer: int | None = None,
        tcp_timewait_timer: int | None = None,
        tcp_rst_timer: int | None = None,
        udp_idle_timer: int | None = None,
        session_ttl: str | None = None,
        check_reset_range: Literal["disable", "strict", "default"] | None = None,
        comment: str | None = None,
        color: int | None = None,
        app_service_type: Literal["disable", "app-id", "app-category"] | None = None,
        app_category: str | list[str] | list[dict[str, Any]] | None = None,
        application: str | list[str] | list[dict[str, Any]] | None = None,
        fabric_object: Literal["enable", "disable"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing firewall/service/custom object.

        Configure custom services.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Custom service name.
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            proxy: Enable/disable web proxy service.
            category: Service category.
            protocol: Protocol type based on IANA numbers.
            helper: Helper name.
            iprange: Start and end of the IP range associated with service.
            fqdn: Fully qualified domain name.
            protocol_number: IP protocol number.
            icmptype: ICMP type.
            icmpcode: ICMP code.
            tcp_portrange: Multiple TCP port ranges.
            udp_portrange: Multiple UDP port ranges.
            udplite_portrange: Multiple UDP-Lite port ranges.
            sctp_portrange: Multiple SCTP port ranges.
            tcp_halfclose_timer: Wait time to close a TCP session waiting for an unanswered FIN packet (1 - 86400 sec, 0 = default).
            tcp_halfopen_timer: Wait time to close a TCP session waiting for an unanswered open session packet (1 - 86400 sec, 0 = default).
            tcp_timewait_timer: Set the length of the TCP TIME-WAIT state in seconds (1 - 300 sec, 0 = default).
            tcp_rst_timer: Set the length of the TCP CLOSE state in seconds (5 - 300 sec, 0 = default).
            udp_idle_timer: Number of seconds before an idle UDP/UDP-Lite connection times out (0 - 86400 sec, 0 = default).
            session_ttl: Session TTL (300 - 2764800, 0 = default).
            check_reset_range: Configure the type of ICMP error message verification.
            comment: Comment.
            color: Color of icon on the GUI.
            app_service_type: Application service type.
            app_category: Application category ID.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            application: Application ID.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            fabric_object: Security Fabric global object setting.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.firewall_service_custom.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.firewall_service_custom.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if app_category is not None:
            app_category = normalize_table_field(
                app_category,
                mkey="id",
                required_fields=['id'],
                field_name="app_category",
                example="[{'id': 1}]",
            )
        if application is not None:
            application = normalize_table_field(
                application,
                mkey="id",
                required_fields=['id'],
                field_name="application",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            uuid=uuid,
            proxy=proxy,
            category=category,
            protocol=protocol,
            helper=helper,
            iprange=iprange,
            fqdn=fqdn,
            protocol_number=protocol_number,
            icmptype=icmptype,
            icmpcode=icmpcode,
            tcp_portrange=tcp_portrange,
            udp_portrange=udp_portrange,
            udplite_portrange=udplite_portrange,
            sctp_portrange=sctp_portrange,
            tcp_halfclose_timer=tcp_halfclose_timer,
            tcp_halfopen_timer=tcp_halfopen_timer,
            tcp_timewait_timer=tcp_timewait_timer,
            tcp_rst_timer=tcp_rst_timer,
            udp_idle_timer=udp_idle_timer,
            session_ttl=session_ttl,
            check_reset_range=check_reset_range,
            comment=comment,
            color=color,
            app_service_type=app_service_type,
            app_category=app_category,
            application=application,
            fabric_object=fabric_object,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.custom import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/service/custom",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/firewall.service/custom/" + quote_path_param(name_value)

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
        uuid: str | None = None,
        proxy: Literal["enable", "disable"] | None = None,
        category: str | None = None,
        protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"] | None = None,
        helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"] | None = None,
        iprange: str | None = None,
        fqdn: str | None = None,
        protocol_number: int | None = None,
        icmptype: int | None = None,
        icmpcode: int | None = None,
        tcp_portrange: str | None = None,
        udp_portrange: str | None = None,
        udplite_portrange: str | None = None,
        sctp_portrange: str | None = None,
        tcp_halfclose_timer: int | None = None,
        tcp_halfopen_timer: int | None = None,
        tcp_timewait_timer: int | None = None,
        tcp_rst_timer: int | None = None,
        udp_idle_timer: int | None = None,
        session_ttl: str | None = None,
        check_reset_range: Literal["disable", "strict", "default"] | None = None,
        comment: str | None = None,
        color: int | None = None,
        app_service_type: Literal["disable", "app-id", "app-category"] | None = None,
        app_category: str | list[str] | list[dict[str, Any]] | None = None,
        application: str | list[str] | list[dict[str, Any]] | None = None,
        fabric_object: Literal["enable", "disable"] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new firewall/service/custom object.

        Configure custom services.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Custom service name.
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            proxy: Enable/disable web proxy service.
            category: Service category.
            protocol: Protocol type based on IANA numbers.
            helper: Helper name.
            iprange: Start and end of the IP range associated with service.
            fqdn: Fully qualified domain name.
            protocol_number: IP protocol number.
            icmptype: ICMP type.
            icmpcode: ICMP code.
            tcp_portrange: Multiple TCP port ranges.
            udp_portrange: Multiple UDP port ranges.
            udplite_portrange: Multiple UDP-Lite port ranges.
            sctp_portrange: Multiple SCTP port ranges.
            tcp_halfclose_timer: Wait time to close a TCP session waiting for an unanswered FIN packet (1 - 86400 sec, 0 = default).
            tcp_halfopen_timer: Wait time to close a TCP session waiting for an unanswered open session packet (1 - 86400 sec, 0 = default).
            tcp_timewait_timer: Set the length of the TCP TIME-WAIT state in seconds (1 - 300 sec, 0 = default).
            tcp_rst_timer: Set the length of the TCP CLOSE state in seconds (5 - 300 sec, 0 = default).
            udp_idle_timer: Number of seconds before an idle UDP/UDP-Lite connection times out (0 - 86400 sec, 0 = default).
            session_ttl: Session TTL (300 - 2764800, 0 = default).
            check_reset_range: Configure the type of ICMP error message verification.
            comment: Comment.
            color: Color of icon on the GUI.
            app_service_type: Application service type.
            app_category: Application category ID.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            application: Application ID.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            fabric_object: Security Fabric global object setting.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.firewall_service_custom.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Custom.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.firewall_service_custom.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Custom.required_fields()) }}
            
            Use Custom.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if app_category is not None:
            app_category = normalize_table_field(
                app_category,
                mkey="id",
                required_fields=['id'],
                field_name="app_category",
                example="[{'id': 1}]",
            )
        if application is not None:
            application = normalize_table_field(
                application,
                mkey="id",
                required_fields=['id'],
                field_name="application",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            uuid=uuid,
            proxy=proxy,
            category=category,
            protocol=protocol,
            helper=helper,
            iprange=iprange,
            fqdn=fqdn,
            protocol_number=protocol_number,
            icmptype=icmptype,
            icmpcode=icmpcode,
            tcp_portrange=tcp_portrange,
            udp_portrange=udp_portrange,
            udplite_portrange=udplite_portrange,
            sctp_portrange=sctp_portrange,
            tcp_halfclose_timer=tcp_halfclose_timer,
            tcp_halfopen_timer=tcp_halfopen_timer,
            tcp_timewait_timer=tcp_timewait_timer,
            tcp_rst_timer=tcp_rst_timer,
            udp_idle_timer=udp_idle_timer,
            session_ttl=session_ttl,
            check_reset_range=check_reset_range,
            comment=comment,
            color=color,
            app_service_type=app_service_type,
            app_category=app_category,
            application=application,
            fabric_object=fabric_object,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.custom import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/service/custom",
            )

        endpoint = "/firewall.service/custom"
        
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
        Delete firewall/service/custom object.

        Configure custom services.

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
            >>> result = fgt.api.cmdb.firewall_service_custom.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/firewall.service/custom/" + quote_path_param(name)

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
        Check if firewall/service/custom object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.firewall_service_custom.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.firewall_service_custom.exists(name=1):
            ...     fgt.api.cmdb.firewall_service_custom.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/firewall.service/custom"
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
        uuid: str | None = None,
        proxy: Literal["enable", "disable"] | None = None,
        category: str | None = None,
        protocol: Literal["TCP/UDP/UDP-Lite/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"] | None = None,
        helper: Literal["auto", "disable", "ftp", "tftp", "ras", "h323", "tns", "mms", "sip", "pptp", "rtsp", "dns-udp", "dns-tcp", "pmap", "rsh", "dcerpc", "mgcp"] | None = None,
        iprange: str | None = None,
        fqdn: str | None = None,
        protocol_number: int | None = None,
        icmptype: int | None = None,
        icmpcode: int | None = None,
        tcp_portrange: str | None = None,
        udp_portrange: str | None = None,
        udplite_portrange: str | None = None,
        sctp_portrange: str | None = None,
        tcp_halfclose_timer: int | None = None,
        tcp_halfopen_timer: int | None = None,
        tcp_timewait_timer: int | None = None,
        tcp_rst_timer: int | None = None,
        udp_idle_timer: int | None = None,
        session_ttl: str | None = None,
        check_reset_range: Literal["disable", "strict", "default"] | None = None,
        comment: str | None = None,
        color: int | None = None,
        app_service_type: Literal["disable", "app-id", "app-category"] | None = None,
        app_category: str | list[str] | list[dict[str, Any]] | None = None,
        application: str | list[str] | list[dict[str, Any]] | None = None,
        fabric_object: Literal["enable", "disable"] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update firewall/service/custom object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            uuid: Field uuid
            proxy: Field proxy
            category: Field category
            protocol: Field protocol
            helper: Field helper
            iprange: Field iprange
            fqdn: Field fqdn
            protocol_number: Field protocol-number
            icmptype: Field icmptype
            icmpcode: Field icmpcode
            tcp_portrange: Field tcp-portrange
            udp_portrange: Field udp-portrange
            udplite_portrange: Field udplite-portrange
            sctp_portrange: Field sctp-portrange
            tcp_halfclose_timer: Field tcp-halfclose-timer
            tcp_halfopen_timer: Field tcp-halfopen-timer
            tcp_timewait_timer: Field tcp-timewait-timer
            tcp_rst_timer: Field tcp-rst-timer
            udp_idle_timer: Field udp-idle-timer
            session_ttl: Field session-ttl
            check_reset_range: Field check-reset-range
            comment: Field comment
            color: Field color
            app_service_type: Field app-service-type
            app_category: Field app-category
            application: Field application
            fabric_object: Field fabric-object
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.firewall_service_custom.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.firewall_service_custom.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.firewall_service_custom.set(payload_dict=obj_data)
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
        if app_category is not None:
            app_category = normalize_table_field(
                app_category,
                mkey="id",
                required_fields=['id'],
                field_name="app_category",
                example="[{'id': 1}]",
            )
        if application is not None:
            application = normalize_table_field(
                application,
                mkey="id",
                required_fields=['id'],
                field_name="application",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            uuid=uuid,
            proxy=proxy,
            category=category,
            protocol=protocol,
            helper=helper,
            iprange=iprange,
            fqdn=fqdn,
            protocol_number=protocol_number,
            icmptype=icmptype,
            icmpcode=icmpcode,
            tcp_portrange=tcp_portrange,
            udp_portrange=udp_portrange,
            udplite_portrange=udplite_portrange,
            sctp_portrange=sctp_portrange,
            tcp_halfclose_timer=tcp_halfclose_timer,
            tcp_halfopen_timer=tcp_halfopen_timer,
            tcp_timewait_timer=tcp_timewait_timer,
            tcp_rst_timer=tcp_rst_timer,
            udp_idle_timer=udp_idle_timer,
            session_ttl=session_ttl,
            check_reset_range=check_reset_range,
            comment=comment,
            color=color,
            app_service_type=app_service_type,
            app_category=app_category,
            application=application,
            fabric_object=fabric_object,
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
        Move firewall/service/custom object to a new position.
        
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
            >>> fgt.api.cmdb.firewall_service_custom.move(
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
        
        endpoint = "/firewall.service/custom"
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
        Clone firewall/service/custom object.
        
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
            >>> fgt.api.cmdb.firewall_service_custom.clone(
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
        
        endpoint = "/firewall.service/custom"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




