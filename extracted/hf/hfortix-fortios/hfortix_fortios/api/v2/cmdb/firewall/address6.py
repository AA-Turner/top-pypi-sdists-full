"""
FortiOS CMDB - Firewall address6

Configuration endpoint for managing cmdb firewall/address6 objects.

API Endpoints:
    GET    /cmdb/firewall/address6
    POST   /cmdb/firewall/address6
    PUT    /cmdb/firewall/address6/{identifier}
    DELETE /cmdb/firewall/address6/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.firewall_address6.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.firewall_address6.post(
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

class Address6(CRUDEndpoint, MetadataMixin):
    """Address6 Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "address6"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "macaddr": {
            "mkey": "macaddr",
            "required_fields": ['macaddr'],
            "example": "[{'macaddr': 'value'}]",
        },
        "tagging": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "subnet_segment": {
            "mkey": "name",
            "required_fields": ['name', 'type', 'value'],
            "example": "[{'name': 'value', 'type': 'any', 'value': 'value'}]",
        },
        "list": {
            "mkey": "ip",
            "required_fields": ['ip'],
            "example": "[{'ip': '192.168.1.10'}]",
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
        """Initialize Address6 endpoint."""
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
        Retrieve firewall/address6 configuration.

        Configure IPv6 firewall addresses.

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
            >>> # Get all firewall/address6 objects
            >>> result = fgt.api.cmdb.firewall_address6.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific firewall/address6 by name
            >>> result = fgt.api.cmdb.firewall_address6.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.firewall_address6.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.firewall_address6.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.firewall_address6.get_schema()

        See Also:
            - post(): Create new firewall/address6 object
            - put(): Update existing firewall/address6 object
            - delete(): Remove firewall/address6 object
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
            endpoint = "/firewall/address6/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/firewall/address6"
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
            >>> schema = fgt.api.cmdb.firewall_address6.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.firewall_address6.get_schema(format="json-schema")
        
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
        type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"] | None = None,
        route_tag: int | None = None,
        macaddr: str | list[str] | list[dict[str, Any]] | None = None,
        sdn: str | None = None,
        ip6: str | None = None,
        wildcard: Any | None = None,
        start_ip: str | None = None,
        end_ip: str | None = None,
        fqdn: str | None = None,
        country: str | None = None,
        cache_ttl: int | None = None,
        color: int | None = None,
        obj_id: str | None = None,
        tagging: str | list[str] | list[dict[str, Any]] | None = None,
        comment: str | None = None,
        template: str | None = None,
        subnet_segment: str | list[str] | list[dict[str, Any]] | None = None,
        host_type: Literal["any", "specific"] | None = None,
        host: str | None = None,
        tenant: str | None = None,
        epg_name: str | None = None,
        sdn_tag: str | None = None,
        filter: str | None = None,
        list: str | list[str] | list[dict[str, Any]] | None = None,
        sdn_addr_type: Literal["private", "public", "all"] | None = None,
        passive_fqdn_learning: Literal["disable", "enable"] | None = None,
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
        Update existing firewall/address6 object.

        Configure IPv6 firewall addresses.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Address name.
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            type: Type of IPv6 address object (default = ipprefix).
            route_tag: route-tag address.
            macaddr: Multiple MAC address ranges.
                Default format: [{'macaddr': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'macaddr': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'macaddr': 'val1'}, ...]
                  - List of dicts: [{'macaddr': 'value'}] (recommended)
            sdn: SDN.
            ip6: IPv6 address prefix (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx).
            wildcard: IPv6 address and wildcard netmask.
            start_ip: First IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).
            end_ip: Final IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).
            fqdn: Fully qualified domain name.
            country: IPv6 addresses associated to a specific country.
            cache_ttl: Minimal TTL of individual IPv6 addresses in FQDN cache.
            color: Integer value to determine the color of the icon in the GUI (range 1 to 32, default = 0, which sets the value to 1).
            obj_id: Object ID for NSX.
            tagging: Config object tagging.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            comment: Comment.
            template: IPv6 address template.
            subnet_segment: IPv6 subnet segments.
                Default format: [{'name': 'value', 'type': 'any', 'value': 'value'}]
                Required format: List of dicts with keys: name, type, value
                  (String format not allowed due to multiple required fields)
            host_type: Host type.
            host: Host Address.
            tenant: Tenant.
            epg_name: Endpoint group name.
            sdn_tag: SDN Tag.
            filter: Match criteria filter.
            list: IP address list.
                Default format: [{'ip': '192.168.1.10'}]
                Supported formats:
                  - Single string: "value" → [{'ip': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'ip': 'val1'}, ...]
                  - List of dicts: [{'ip': '192.168.1.10'}] (recommended)
            sdn_addr_type: Type of addresses to collect.
            passive_fqdn_learning: Enable/disable passive learning of FQDNs.  When enabled, the FortiGate learns, trusts, and saves FQDNs from endpoint DNS queries (default = enable).
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
            >>> result = fgt.api.cmdb.firewall_address6.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.firewall_address6.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if macaddr is not None:
            macaddr = normalize_table_field(
                macaddr,
                mkey="macaddr",
                required_fields=['macaddr'],
                field_name="macaddr",
                example="[{'macaddr': 'value'}]",
            )
        if tagging is not None:
            tagging = normalize_table_field(
                tagging,
                mkey="name",
                required_fields=['name'],
                field_name="tagging",
                example="[{'name': 'value'}]",
            )
        if subnet_segment is not None:
            subnet_segment = normalize_table_field(
                subnet_segment,
                mkey="name",
                required_fields=['name', 'type', 'value'],
                field_name="subnet_segment",
                example="[{'name': 'value', 'type': 'any', 'value': 'value'}]",
            )
        if list is not None:
            list = normalize_table_field(
                list,
                mkey="ip",
                required_fields=['ip'],
                field_name="list",
                example="[{'ip': '192.168.1.10'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            uuid=uuid,
            type=type,
            route_tag=route_tag,
            macaddr=macaddr,
            sdn=sdn,
            ip6=ip6,
            wildcard=wildcard,
            start_ip=start_ip,
            end_ip=end_ip,
            fqdn=fqdn,
            country=country,
            cache_ttl=cache_ttl,
            color=color,
            obj_id=obj_id,
            tagging=tagging,
            comment=comment,
            template=template,
            subnet_segment=subnet_segment,
            host_type=host_type,
            host=host,
            tenant=tenant,
            epg_name=epg_name,
            sdn_tag=sdn_tag,
            filter=filter,
            list=list,
            sdn_addr_type=sdn_addr_type,
            passive_fqdn_learning=passive_fqdn_learning,
            fabric_object=fabric_object,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.address6 import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/address6",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/firewall/address6/" + quote_path_param(name_value)

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
        type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"] | None = None,
        route_tag: int | None = None,
        macaddr: str | list[str] | list[dict[str, Any]] | None = None,
        sdn: str | None = None,
        ip6: str | None = None,
        wildcard: Any | None = None,
        start_ip: str | None = None,
        end_ip: str | None = None,
        fqdn: str | None = None,
        country: str | None = None,
        cache_ttl: int | None = None,
        color: int | None = None,
        obj_id: str | None = None,
        tagging: str | list[str] | list[dict[str, Any]] | None = None,
        comment: str | None = None,
        template: str | None = None,
        subnet_segment: str | list[str] | list[dict[str, Any]] | None = None,
        host_type: Literal["any", "specific"] | None = None,
        host: str | None = None,
        tenant: str | None = None,
        epg_name: str | None = None,
        sdn_tag: str | None = None,
        filter: str | None = None,
        list: str | list[str] | list[dict[str, Any]] | None = None,
        sdn_addr_type: Literal["private", "public", "all"] | None = None,
        passive_fqdn_learning: Literal["disable", "enable"] | None = None,
        fabric_object: Literal["enable", "disable"] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new firewall/address6 object.

        Configure IPv6 firewall addresses.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Address name.
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            type: Type of IPv6 address object (default = ipprefix).
            route_tag: route-tag address.
            macaddr: Multiple MAC address ranges.
                Default format: [{'macaddr': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'macaddr': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'macaddr': 'val1'}, ...]
                  - List of dicts: [{'macaddr': 'value'}] (recommended)
            sdn: SDN.
            ip6: IPv6 address prefix (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx).
            wildcard: IPv6 address and wildcard netmask.
            start_ip: First IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).
            end_ip: Final IP address (inclusive) in the range for the address (format: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx).
            fqdn: Fully qualified domain name.
            country: IPv6 addresses associated to a specific country.
            cache_ttl: Minimal TTL of individual IPv6 addresses in FQDN cache.
            color: Integer value to determine the color of the icon in the GUI (range 1 to 32, default = 0, which sets the value to 1).
            obj_id: Object ID for NSX.
            tagging: Config object tagging.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            comment: Comment.
            template: IPv6 address template.
            subnet_segment: IPv6 subnet segments.
                Default format: [{'name': 'value', 'type': 'any', 'value': 'value'}]
                Required format: List of dicts with keys: name, type, value
                  (String format not allowed due to multiple required fields)
            host_type: Host type.
            host: Host Address.
            tenant: Tenant.
            epg_name: Endpoint group name.
            sdn_tag: SDN Tag.
            filter: Match criteria filter.
            list: IP address list.
                Default format: [{'ip': '192.168.1.10'}]
                Supported formats:
                  - Single string: "value" → [{'ip': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'ip': 'val1'}, ...]
                  - List of dicts: [{'ip': '192.168.1.10'}] (recommended)
            sdn_addr_type: Type of addresses to collect.
            passive_fqdn_learning: Enable/disable passive learning of FQDNs.  When enabled, the FortiGate learns, trusts, and saves FQDNs from endpoint DNS queries (default = enable).
            fabric_object: Security Fabric global object setting.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.firewall_address6.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Address6.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.firewall_address6.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Address6.required_fields()) }}
            
            Use Address6.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if macaddr is not None:
            macaddr = normalize_table_field(
                macaddr,
                mkey="macaddr",
                required_fields=['macaddr'],
                field_name="macaddr",
                example="[{'macaddr': 'value'}]",
            )
        if tagging is not None:
            tagging = normalize_table_field(
                tagging,
                mkey="name",
                required_fields=['name'],
                field_name="tagging",
                example="[{'name': 'value'}]",
            )
        if subnet_segment is not None:
            subnet_segment = normalize_table_field(
                subnet_segment,
                mkey="name",
                required_fields=['name', 'type', 'value'],
                field_name="subnet_segment",
                example="[{'name': 'value', 'type': 'any', 'value': 'value'}]",
            )
        if list is not None:
            list = normalize_table_field(
                list,
                mkey="ip",
                required_fields=['ip'],
                field_name="list",
                example="[{'ip': '192.168.1.10'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            uuid=uuid,
            type=type,
            route_tag=route_tag,
            macaddr=macaddr,
            sdn=sdn,
            ip6=ip6,
            wildcard=wildcard,
            start_ip=start_ip,
            end_ip=end_ip,
            fqdn=fqdn,
            country=country,
            cache_ttl=cache_ttl,
            color=color,
            obj_id=obj_id,
            tagging=tagging,
            comment=comment,
            template=template,
            subnet_segment=subnet_segment,
            host_type=host_type,
            host=host,
            tenant=tenant,
            epg_name=epg_name,
            sdn_tag=sdn_tag,
            filter=filter,
            list=list,
            sdn_addr_type=sdn_addr_type,
            passive_fqdn_learning=passive_fqdn_learning,
            fabric_object=fabric_object,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.address6 import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/address6",
            )

        endpoint = "/firewall/address6"
        
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
        Delete firewall/address6 object.

        Configure IPv6 firewall addresses.

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
            >>> result = fgt.api.cmdb.firewall_address6.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/firewall/address6/" + quote_path_param(name)

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
        Check if firewall/address6 object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.firewall_address6.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.firewall_address6.exists(name=1):
            ...     fgt.api.cmdb.firewall_address6.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/firewall/address6"
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
        type: Literal["ipprefix", "iprange", "fqdn", "geography", "dynamic", "template", "mac", "route-tag", "wildcard"] | None = None,
        route_tag: int | None = None,
        macaddr: str | list[str] | list[dict[str, Any]] | None = None,
        sdn: str | None = None,
        ip6: str | None = None,
        wildcard: Any | None = None,
        start_ip: str | None = None,
        end_ip: str | None = None,
        fqdn: str | None = None,
        country: str | None = None,
        cache_ttl: int | None = None,
        color: int | None = None,
        obj_id: str | None = None,
        tagging: str | list[str] | list[dict[str, Any]] | None = None,
        comment: str | None = None,
        template: str | None = None,
        subnet_segment: str | list[str] | list[dict[str, Any]] | None = None,
        host_type: Literal["any", "specific"] | None = None,
        host: str | None = None,
        tenant: str | None = None,
        epg_name: str | None = None,
        sdn_tag: str | None = None,
        filter: str | None = None,
        list: str | list[str] | list[dict[str, Any]] | None = None,
        sdn_addr_type: Literal["private", "public", "all"] | None = None,
        passive_fqdn_learning: Literal["disable", "enable"] | None = None,
        fabric_object: Literal["enable", "disable"] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update firewall/address6 object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            uuid: Field uuid
            type: Field type
            route_tag: Field route-tag
            macaddr: Field macaddr
            sdn: Field sdn
            ip6: Field ip6
            wildcard: Field wildcard
            start_ip: Field start-ip
            end_ip: Field end-ip
            fqdn: Field fqdn
            country: Field country
            cache_ttl: Field cache-ttl
            color: Field color
            obj_id: Field obj-id
            tagging: Field tagging
            comment: Field comment
            template: Field template
            subnet_segment: Field subnet-segment
            host_type: Field host-type
            host: Field host
            tenant: Field tenant
            epg_name: Field epg-name
            sdn_tag: Field sdn-tag
            filter: Field filter
            list: Field list
            sdn_addr_type: Field sdn-addr-type
            passive_fqdn_learning: Field passive-fqdn-learning
            fabric_object: Field fabric-object
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.firewall_address6.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.firewall_address6.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.firewall_address6.set(payload_dict=obj_data)
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
        if macaddr is not None:
            macaddr = normalize_table_field(
                macaddr,
                mkey="macaddr",
                required_fields=['macaddr'],
                field_name="macaddr",
                example="[{'macaddr': 'value'}]",
            )
        if tagging is not None:
            tagging = normalize_table_field(
                tagging,
                mkey="name",
                required_fields=['name'],
                field_name="tagging",
                example="[{'name': 'value'}]",
            )
        if subnet_segment is not None:
            subnet_segment = normalize_table_field(
                subnet_segment,
                mkey="name",
                required_fields=['name', 'type', 'value'],
                field_name="subnet_segment",
                example="[{'name': 'value', 'type': 'any', 'value': 'value'}]",
            )
        if list is not None:
            list = normalize_table_field(
                list,
                mkey="ip",
                required_fields=['ip'],
                field_name="list",
                example="[{'ip': '192.168.1.10'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            uuid=uuid,
            type=type,
            route_tag=route_tag,
            macaddr=macaddr,
            sdn=sdn,
            ip6=ip6,
            wildcard=wildcard,
            start_ip=start_ip,
            end_ip=end_ip,
            fqdn=fqdn,
            country=country,
            cache_ttl=cache_ttl,
            color=color,
            obj_id=obj_id,
            tagging=tagging,
            comment=comment,
            template=template,
            subnet_segment=subnet_segment,
            host_type=host_type,
            host=host,
            tenant=tenant,
            epg_name=epg_name,
            sdn_tag=sdn_tag,
            filter=filter,
            list=list,
            sdn_addr_type=sdn_addr_type,
            passive_fqdn_learning=passive_fqdn_learning,
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
        Move firewall/address6 object to a new position.
        
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
            >>> fgt.api.cmdb.firewall_address6.move(
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
        
        endpoint = "/firewall/address6"
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
        Clone firewall/address6 object.
        
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
            >>> fgt.api.cmdb.firewall_address6.clone(
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
        
        endpoint = "/firewall/address6"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




