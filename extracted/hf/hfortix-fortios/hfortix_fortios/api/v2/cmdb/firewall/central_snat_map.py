"""
FortiOS CMDB - Firewall central_snat_map

Configuration endpoint for managing cmdb firewall/central_snat_map objects.

API Endpoints:
    GET    /cmdb/firewall/central_snat_map
    POST   /cmdb/firewall/central_snat_map
    PUT    /cmdb/firewall/central_snat_map/{identifier}
    DELETE /cmdb/firewall/central_snat_map/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.firewall_central_snat_map.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.firewall_central_snat_map.post(
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

class CentralSnatMap(CRUDEndpoint, MetadataMixin):
    """CentralSnatMap Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "central_snat_map"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "srcintf": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "dstintf": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "orig_addr": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "orig_addr6": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "dst_addr": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "dst_addr6": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "nat_ippool": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "nat_ippool6": {
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
    SUPPORTS_CLONE = True
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize CentralSnatMap endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        policyid: int | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve firewall/central_snat_map configuration.

        Configure IPv4 and IPv6 central SNAT policies.

        Args:
            policyid: Integer identifier to retrieve specific object.
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
            >>> # Get all firewall/central_snat_map objects
            >>> result = fgt.api.cmdb.firewall_central_snat_map.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific firewall/central_snat_map by policyid
            >>> result = fgt.api.cmdb.firewall_central_snat_map.get(policyid=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.firewall_central_snat_map.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.firewall_central_snat_map.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.firewall_central_snat_map.get_schema()

        See Also:
            - post(): Create new firewall/central_snat_map object
            - put(): Update existing firewall/central_snat_map object
            - delete(): Remove firewall/central_snat_map object
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
        
        if policyid:
            endpoint = "/firewall/central-snat-map/" + quote_path_param(policyid)
            unwrap_single = True
        else:
            endpoint = "/firewall/central-snat-map"
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
            >>> schema = fgt.api.cmdb.firewall_central_snat_map.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.firewall_central_snat_map.get_schema(format="json-schema")
        
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
        policyid: int | None = None,
        uuid: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        type: Literal["ipv4", "ipv6"] | None = None,
        srcintf: str | list[str] | list[dict[str, Any]] | None = None,
        dstintf: str | list[str] | list[dict[str, Any]] | None = None,
        orig_addr: str | list[str] | list[dict[str, Any]] | None = None,
        orig_addr6: str | list[str] | list[dict[str, Any]] | None = None,
        dst_addr: str | list[str] | list[dict[str, Any]] | None = None,
        dst_addr6: str | list[str] | list[dict[str, Any]] | None = None,
        protocol: int | None = None,
        orig_port: str | None = None,
        nat: Literal["disable", "enable"] | None = None,
        nat46: Literal["enable", "disable"] | None = None,
        nat64: Literal["enable", "disable"] | None = None,
        nat_ippool: str | list[str] | list[dict[str, Any]] | None = None,
        nat_ippool6: str | list[str] | list[dict[str, Any]] | None = None,
        port_preserve: Literal["enable", "disable"] | None = None,
        port_random: Literal["enable", "disable"] | None = None,
        nat_port: str | None = None,
        dst_port: str | None = None,
        comments: str | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing firewall/central_snat_map object.

        Configure IPv4 and IPv6 central SNAT policies.

        Args:
            payload_dict: Object data as dict. Must include policyid (primary key).
            policyid: Policy ID.
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            status: Enable/disable the active status of this policy.
            type: IPv4/IPv6 source NAT.
            srcintf: Source interface name from available interfaces.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dstintf: Destination interface name from available interfaces.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            orig_addr: IPv4 Original address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            orig_addr6: IPv6 Original address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dst_addr: IPv4 Destination address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dst_addr6: IPv6 Destination address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            protocol: Integer value for the protocol type (0 - 255).
            orig_port: Original TCP port (1 to 65535, 0 means any port).
            nat: Enable/disable source NAT.
            nat46: Enable/disable NAT46.
            nat64: Enable/disable NAT64.
            nat_ippool: Name of the IP pools to be used to translate addresses from available IP Pools.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            nat_ippool6: IPv6 pools to be used for source NAT.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            port_preserve: Enable/disable preservation of the original source port from source NAT if it has not been used.
            port_random: Enable/disable random source port selection for source NAT.
            nat_port: Translated port or port range (1 to 65535, 0 means any port).
            dst_port: Destination port or port range (1 to 65535, 0 means any port).
            comments: Comment.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If policyid is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.firewall_central_snat_map.put(
            ...     policyid=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "policyid": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.firewall_central_snat_map.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if srcintf is not None:
            srcintf = normalize_table_field(
                srcintf,
                mkey="name",
                required_fields=['name'],
                field_name="srcintf",
                example="[{'name': 'value'}]",
            )
        if dstintf is not None:
            dstintf = normalize_table_field(
                dstintf,
                mkey="name",
                required_fields=['name'],
                field_name="dstintf",
                example="[{'name': 'value'}]",
            )
        if orig_addr is not None:
            orig_addr = normalize_table_field(
                orig_addr,
                mkey="name",
                required_fields=['name'],
                field_name="orig_addr",
                example="[{'name': 'value'}]",
            )
        if orig_addr6 is not None:
            orig_addr6 = normalize_table_field(
                orig_addr6,
                mkey="name",
                required_fields=['name'],
                field_name="orig_addr6",
                example="[{'name': 'value'}]",
            )
        if dst_addr is not None:
            dst_addr = normalize_table_field(
                dst_addr,
                mkey="name",
                required_fields=['name'],
                field_name="dst_addr",
                example="[{'name': 'value'}]",
            )
        if dst_addr6 is not None:
            dst_addr6 = normalize_table_field(
                dst_addr6,
                mkey="name",
                required_fields=['name'],
                field_name="dst_addr6",
                example="[{'name': 'value'}]",
            )
        if nat_ippool is not None:
            nat_ippool = normalize_table_field(
                nat_ippool,
                mkey="name",
                required_fields=['name'],
                field_name="nat_ippool",
                example="[{'name': 'value'}]",
            )
        if nat_ippool6 is not None:
            nat_ippool6 = normalize_table_field(
                nat_ippool6,
                mkey="name",
                required_fields=['name'],
                field_name="nat_ippool6",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            policyid=policyid,
            uuid=uuid,
            status=status,
            type=type,
            srcintf=srcintf,
            dstintf=dstintf,
            orig_addr=orig_addr,
            orig_addr6=orig_addr6,
            dst_addr=dst_addr,
            dst_addr6=dst_addr6,
            protocol=protocol,
            orig_port=orig_port,
            nat=nat,
            nat46=nat46,
            nat64=nat64,
            nat_ippool=nat_ippool,
            nat_ippool6=nat_ippool6,
            port_preserve=port_preserve,
            port_random=port_random,
            nat_port=nat_port,
            dst_port=dst_port,
            comments=comments,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.central_snat_map import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/central_snat_map",
            )
        
        policyid_value = payload_data.get("policyid")
        if not policyid_value:
            raise ValueError("policyid is required for PUT")
        endpoint = "/firewall/central-snat-map/" + quote_path_param(policyid_value)

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
        policyid: int | None = None,
        uuid: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        type: Literal["ipv4", "ipv6"] | None = None,
        srcintf: str | list[str] | list[dict[str, Any]] | None = None,
        dstintf: str | list[str] | list[dict[str, Any]] | None = None,
        orig_addr: str | list[str] | list[dict[str, Any]] | None = None,
        orig_addr6: str | list[str] | list[dict[str, Any]] | None = None,
        dst_addr: str | list[str] | list[dict[str, Any]] | None = None,
        dst_addr6: str | list[str] | list[dict[str, Any]] | None = None,
        protocol: int | None = None,
        orig_port: str | None = None,
        nat: Literal["disable", "enable"] | None = None,
        nat46: Literal["enable", "disable"] | None = None,
        nat64: Literal["enable", "disable"] | None = None,
        nat_ippool: str | list[str] | list[dict[str, Any]] | None = None,
        nat_ippool6: str | list[str] | list[dict[str, Any]] | None = None,
        port_preserve: Literal["enable", "disable"] | None = None,
        port_random: Literal["enable", "disable"] | None = None,
        nat_port: str | None = None,
        dst_port: str | None = None,
        comments: str | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new firewall/central_snat_map object.

        Configure IPv4 and IPv6 central SNAT policies.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            policyid: Policy ID.
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            status: Enable/disable the active status of this policy.
            type: IPv4/IPv6 source NAT.
            srcintf: Source interface name from available interfaces.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dstintf: Destination interface name from available interfaces.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            orig_addr: IPv4 Original address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            orig_addr6: IPv6 Original address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dst_addr: IPv4 Destination address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dst_addr6: IPv6 Destination address.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            protocol: Integer value for the protocol type (0 - 255).
            orig_port: Original TCP port (1 to 65535, 0 means any port).
            nat: Enable/disable source NAT.
            nat46: Enable/disable NAT46.
            nat64: Enable/disable NAT64.
            nat_ippool: Name of the IP pools to be used to translate addresses from available IP Pools.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            nat_ippool6: IPv6 pools to be used for source NAT.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            port_preserve: Enable/disable preservation of the original source port from source NAT if it has not been used.
            port_random: Enable/disable random source port selection for source NAT.
            nat_port: Translated port or port range (1 to 65535, 0 means any port).
            dst_port: Destination port or port range (1 to 65535, 0 means any port).
            comments: Comment.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.firewall_central_snat_map.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created policyid: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = CentralSnatMap.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.firewall_central_snat_map.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(CentralSnatMap.required_fields()) }}
            
            Use CentralSnatMap.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if srcintf is not None:
            srcintf = normalize_table_field(
                srcintf,
                mkey="name",
                required_fields=['name'],
                field_name="srcintf",
                example="[{'name': 'value'}]",
            )
        if dstintf is not None:
            dstintf = normalize_table_field(
                dstintf,
                mkey="name",
                required_fields=['name'],
                field_name="dstintf",
                example="[{'name': 'value'}]",
            )
        if orig_addr is not None:
            orig_addr = normalize_table_field(
                orig_addr,
                mkey="name",
                required_fields=['name'],
                field_name="orig_addr",
                example="[{'name': 'value'}]",
            )
        if orig_addr6 is not None:
            orig_addr6 = normalize_table_field(
                orig_addr6,
                mkey="name",
                required_fields=['name'],
                field_name="orig_addr6",
                example="[{'name': 'value'}]",
            )
        if dst_addr is not None:
            dst_addr = normalize_table_field(
                dst_addr,
                mkey="name",
                required_fields=['name'],
                field_name="dst_addr",
                example="[{'name': 'value'}]",
            )
        if dst_addr6 is not None:
            dst_addr6 = normalize_table_field(
                dst_addr6,
                mkey="name",
                required_fields=['name'],
                field_name="dst_addr6",
                example="[{'name': 'value'}]",
            )
        if nat_ippool is not None:
            nat_ippool = normalize_table_field(
                nat_ippool,
                mkey="name",
                required_fields=['name'],
                field_name="nat_ippool",
                example="[{'name': 'value'}]",
            )
        if nat_ippool6 is not None:
            nat_ippool6 = normalize_table_field(
                nat_ippool6,
                mkey="name",
                required_fields=['name'],
                field_name="nat_ippool6",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            policyid=policyid,
            uuid=uuid,
            status=status,
            type=type,
            srcintf=srcintf,
            dstintf=dstintf,
            orig_addr=orig_addr,
            orig_addr6=orig_addr6,
            dst_addr=dst_addr,
            dst_addr6=dst_addr6,
            protocol=protocol,
            orig_port=orig_port,
            nat=nat,
            nat46=nat46,
            nat64=nat64,
            nat_ippool=nat_ippool,
            nat_ippool6=nat_ippool6,
            port_preserve=port_preserve,
            port_random=port_random,
            nat_port=nat_port,
            dst_port=dst_port,
            comments=comments,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.central_snat_map import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/central_snat_map",
            )

        endpoint = "/firewall/central-snat-map"
        
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
        policyid: int | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete firewall/central_snat_map object.

        Configure IPv4 and IPv6 central SNAT policies.

        Args:
            policyid: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If policyid is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.firewall_central_snat_map.delete(policyid=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not policyid:
            raise ValueError("policyid is required for DELETE")
        endpoint = "/firewall/central-snat-map/" + quote_path_param(policyid)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        policyid: int,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if firewall/central_snat_map object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            policyid: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.firewall_central_snat_map.exists(policyid=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.firewall_central_snat_map.exists(policyid=1):
            ...     fgt.api.cmdb.firewall_central_snat_map.delete(policyid=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/firewall/central-snat-map"
        endpoint = f"{endpoint}/{quote_path_param(policyid)}"
        
        try:
            result = self.get(policyid=policyid, vdom=vdom)
            
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
        policyid: int | None = None,
        uuid: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        type: Literal["ipv4", "ipv6"] | None = None,
        srcintf: str | list[str] | list[dict[str, Any]] | None = None,
        dstintf: str | list[str] | list[dict[str, Any]] | None = None,
        orig_addr: str | list[str] | list[dict[str, Any]] | None = None,
        orig_addr6: str | list[str] | list[dict[str, Any]] | None = None,
        dst_addr: str | list[str] | list[dict[str, Any]] | None = None,
        dst_addr6: str | list[str] | list[dict[str, Any]] | None = None,
        protocol: int | None = None,
        orig_port: str | None = None,
        nat: Literal["disable", "enable"] | None = None,
        nat46: Literal["enable", "disable"] | None = None,
        nat64: Literal["enable", "disable"] | None = None,
        nat_ippool: str | list[str] | list[dict[str, Any]] | None = None,
        nat_ippool6: str | list[str] | list[dict[str, Any]] | None = None,
        port_preserve: Literal["enable", "disable"] | None = None,
        port_random: Literal["enable", "disable"] | None = None,
        nat_port: str | None = None,
        dst_port: str | None = None,
        comments: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update firewall/central_snat_map object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (policyid) in the payload.

        Args:
            payload_dict: Resource data including policyid (primary key)
            policyid: Field policyid
            uuid: Field uuid
            status: Field status
            type: Field type
            srcintf: Field srcintf
            dstintf: Field dstintf
            orig_addr: Field orig-addr
            orig_addr6: Field orig-addr6
            dst_addr: Field dst-addr
            dst_addr6: Field dst-addr6
            protocol: Field protocol
            orig_port: Field orig-port
            nat: Field nat
            nat46: Field nat46
            nat64: Field nat64
            nat_ippool: Field nat-ippool
            nat_ippool6: Field nat-ippool6
            port_preserve: Field port-preserve
            port_random: Field port-random
            nat_port: Field nat-port
            dst_port: Field dst-port
            comments: Field comments
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If policyid is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.firewall_central_snat_map.set(
            ...     policyid=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "policyid": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.firewall_central_snat_map.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.firewall_central_snat_map.set(payload_dict=obj_data)
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
        if srcintf is not None:
            srcintf = normalize_table_field(
                srcintf,
                mkey="name",
                required_fields=['name'],
                field_name="srcintf",
                example="[{'name': 'value'}]",
            )
        if dstintf is not None:
            dstintf = normalize_table_field(
                dstintf,
                mkey="name",
                required_fields=['name'],
                field_name="dstintf",
                example="[{'name': 'value'}]",
            )
        if orig_addr is not None:
            orig_addr = normalize_table_field(
                orig_addr,
                mkey="name",
                required_fields=['name'],
                field_name="orig_addr",
                example="[{'name': 'value'}]",
            )
        if orig_addr6 is not None:
            orig_addr6 = normalize_table_field(
                orig_addr6,
                mkey="name",
                required_fields=['name'],
                field_name="orig_addr6",
                example="[{'name': 'value'}]",
            )
        if dst_addr is not None:
            dst_addr = normalize_table_field(
                dst_addr,
                mkey="name",
                required_fields=['name'],
                field_name="dst_addr",
                example="[{'name': 'value'}]",
            )
        if dst_addr6 is not None:
            dst_addr6 = normalize_table_field(
                dst_addr6,
                mkey="name",
                required_fields=['name'],
                field_name="dst_addr6",
                example="[{'name': 'value'}]",
            )
        if nat_ippool is not None:
            nat_ippool = normalize_table_field(
                nat_ippool,
                mkey="name",
                required_fields=['name'],
                field_name="nat_ippool",
                example="[{'name': 'value'}]",
            )
        if nat_ippool6 is not None:
            nat_ippool6 = normalize_table_field(
                nat_ippool6,
                mkey="name",
                required_fields=['name'],
                field_name="nat_ippool6",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            policyid=policyid,
            uuid=uuid,
            status=status,
            type=type,
            srcintf=srcintf,
            dstintf=dstintf,
            orig_addr=orig_addr,
            orig_addr6=orig_addr6,
            dst_addr=dst_addr,
            dst_addr6=dst_addr6,
            protocol=protocol,
            orig_port=orig_port,
            nat=nat,
            nat46=nat46,
            nat64=nat64,
            nat_ippool=nat_ippool,
            nat_ippool6=nat_ippool6,
            port_preserve=port_preserve,
            port_random=port_random,
            nat_port=nat_port,
            dst_port=dst_port,
            comments=comments,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("policyid")
        if not mkey_value:
            raise ValueError("policyid is required for set()")
        
        # Check if resource exists
        if self.exists(policyid=mkey_value, vdom=vdom):
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
        policyid: int,
        action: Literal["before", "after"],
        reference_policyid: int,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move firewall/central_snat_map object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            policyid: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_policyid: Identifier of reference object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.firewall_central_snat_map.move(
            ...     policyid=100,
            ...     action="before",
            ...     reference_policyid=50
            ... )
        """
        # Build params for move operation
        params = {
            "policyid": policyid,
            "action": "move",
            action: reference_policyid,
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/firewall/central-snat-map"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        policyid: int,
        new_policyid: int,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone firewall/central_snat_map object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            policyid: Identifier of object to clone
            new_policyid: Identifier for the cloned object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.firewall_central_snat_map.clone(
            ...     policyid=1,
            ...     new_policyid=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "policyid": policyid,
            "new_policyid": new_policyid,
            "action": "clone",
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/firewall/central-snat-map"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




