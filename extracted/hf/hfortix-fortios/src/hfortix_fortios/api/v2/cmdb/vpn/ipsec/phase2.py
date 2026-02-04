"""
FortiOS CMDB - Vpn ipsec phase2

Configuration endpoint for managing cmdb vpn/ipsec/phase2 objects.

API Endpoints:
    GET    /cmdb/vpn/ipsec/phase2
    POST   /cmdb/vpn/ipsec/phase2
    PUT    /cmdb/vpn/ipsec/phase2/{identifier}
    DELETE /cmdb/vpn/ipsec/phase2/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.vpn_ipsec_phase2.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.vpn_ipsec_phase2.post(
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

class Phase2(CRUDEndpoint, MetadataMixin):
    """Phase2 Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "phase2"
    
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
        """Initialize Phase2 endpoint."""
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
        Retrieve vpn/ipsec/phase2 configuration.

        Configure VPN autokey tunnel.

        Args:
            name: String identifier to retrieve specific object.
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
            >>> # Get all vpn/ipsec/phase2 objects
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific vpn/ipsec/phase2 by name
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.vpn_ipsec_phase2.get_schema()

        See Also:
            - post(): Create new vpn/ipsec/phase2 object
            - put(): Update existing vpn/ipsec/phase2 object
            - delete(): Remove vpn/ipsec/phase2 object
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
            endpoint = "/vpn.ipsec/phase2/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/vpn.ipsec/phase2"
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
            >>> schema = fgt.api.cmdb.vpn_ipsec_phase2.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.vpn_ipsec_phase2.get_schema(format="json-schema")
        
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
        phase1name: str | None = None,
        dhcp_ipsec: Literal["enable", "disable"] | None = None,
        use_natip: Literal["enable", "disable"] | None = None,
        selector_match: Literal["exact", "subset", "auto"] | None = None,
        proposal: Literal["null-md5", "null-sha1", "null-sha256", "null-sha384", "null-sha512", "des-null", "des-md5", "des-sha1", "des-sha256", "des-sha384", "des-sha512", "3des-null", "3des-md5", "3des-sha1", "3des-sha256", "3des-sha384", "3des-sha512", "aes128-null", "aes128-md5", "aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes128gcm", "aes192-null", "aes192-md5", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-null", "aes256-md5", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes256gcm", "chacha20poly1305", "aria128-null", "aria128-md5", "aria128-sha1", "aria128-sha256", "aria128-sha384", "aria128-sha512", "aria192-null", "aria192-md5", "aria192-sha1", "aria192-sha256", "aria192-sha384", "aria192-sha512", "aria256-null", "aria256-md5", "aria256-sha1", "aria256-sha256", "aria256-sha384", "aria256-sha512", "seed-null", "seed-md5", "seed-sha1", "seed-sha256", "seed-sha384", "seed-sha512"] | list[str] | None = None,
        pfs: Literal["enable", "disable"] | None = None,
        dhgrp: Literal["1", "2", "5", "14", "15", "16", "17", "18", "19", "20", "21", "27", "28", "29", "30", "31", "32"] | list[str] | None = None,
        addke1: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke2: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke3: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke4: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke5: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke6: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke7: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        replay: Literal["enable", "disable"] | None = None,
        keepalive: Literal["enable", "disable"] | None = None,
        auto_negotiate: Literal["enable", "disable"] | None = None,
        add_route: Literal["phase1", "enable", "disable"] | None = None,
        inbound_dscp_copy: Literal["phase1", "enable", "disable"] | None = None,
        keylifeseconds: int | None = None,
        keylifekbs: int | None = None,
        keylife_type: Literal["seconds", "kbs", "both"] | None = None,
        single_source: Literal["enable", "disable"] | None = None,
        route_overlap: Literal["use-old", "use-new", "allow"] | None = None,
        encapsulation: Literal["tunnel-mode", "transport-mode"] | None = None,
        l2tp: Literal["enable", "disable"] | None = None,
        comments: str | None = None,
        initiator_ts_narrow: Literal["enable", "disable"] | None = None,
        diffserv: Literal["enable", "disable"] | None = None,
        diffservcode: str | None = None,
        protocol: int | None = None,
        src_name: str | None = None,
        src_name6: str | None = None,
        src_addr_type: Literal["subnet", "range", "ip", "name"] | None = None,
        src_start_ip: str | None = None,
        src_start_ip6: str | None = None,
        src_end_ip: str | None = None,
        src_end_ip6: str | None = None,
        src_subnet: Any | None = None,
        src_subnet6: str | None = None,
        src_port: int | None = None,
        dst_name: str | None = None,
        dst_name6: str | None = None,
        dst_addr_type: Literal["subnet", "range", "ip", "name"] | None = None,
        dst_start_ip: str | None = None,
        dst_start_ip6: str | None = None,
        dst_end_ip: str | None = None,
        dst_end_ip6: str | None = None,
        dst_subnet: Any | None = None,
        dst_subnet6: str | None = None,
        dst_port: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing vpn/ipsec/phase2 object.

        Configure VPN autokey tunnel.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: IPsec tunnel name.
            phase1name: Phase 1 determines the options required for phase 2.
            dhcp_ipsec: Enable/disable DHCP-IPsec.
            use_natip: Enable to use the FortiGate public IP as the source selector when outbound NAT is used.
            selector_match: Match type to use when comparing selectors.
            proposal: Phase2 proposal.
            pfs: Enable/disable PFS feature.
            dhgrp: Phase2 DH group.
            addke1: phase2 ADDKE1 group.
            addke2: phase2 ADDKE2 group.
            addke3: phase2 ADDKE3 group.
            addke4: phase2 ADDKE4 group.
            addke5: phase2 ADDKE5 group.
            addke6: phase2 ADDKE6 group.
            addke7: phase2 ADDKE7 group.
            replay: Enable/disable replay detection.
            keepalive: Enable/disable keep alive.
            auto_negotiate: Enable/disable IPsec SA auto-negotiation.
            add_route: Enable/disable automatic route addition.
            inbound_dscp_copy: Enable/disable copying of the DSCP in the ESP header to the inner IP header.
            keylifeseconds: Phase2 key life in time in seconds (120 - 172800).
            keylifekbs: Phase2 key life in number of kilobytes of traffic (5120 - 4294967295).
            keylife_type: Keylife type.
            single_source: Enable/disable single source IP restriction.
            route_overlap: Action for overlapping routes.
            encapsulation: ESP encapsulation mode.
            l2tp: Enable/disable L2TP over IPsec.
            comments: Comment.
            initiator_ts_narrow: Enable/disable traffic selector narrowing for IKEv2 initiator.
            diffserv: Enable/disable applying DSCP value to the IPsec tunnel outer IP header.
            diffservcode: DSCP value to be applied to the IPsec tunnel outer IP header.
            protocol: Quick mode protocol selector (1 - 255 or 0 for all).
            src_name: Local proxy ID name.
            src_name6: Local proxy ID name.
            src_addr_type: Local proxy ID type.
            src_start_ip: Local proxy ID start.
            src_start_ip6: Local proxy ID IPv6 start.
            src_end_ip: Local proxy ID end.
            src_end_ip6: Local proxy ID IPv6 end.
            src_subnet: Local proxy ID subnet.
            src_subnet6: Local proxy ID IPv6 subnet.
            src_port: Quick mode source port (1 - 65535 or 0 for all).
            dst_name: Remote proxy ID name.
            dst_name6: Remote proxy ID name.
            dst_addr_type: Remote proxy ID type.
            dst_start_ip: Remote proxy ID IPv4 start.
            dst_start_ip6: Remote proxy ID IPv6 start.
            dst_end_ip: Remote proxy ID IPv4 end.
            dst_end_ip6: Remote proxy ID IPv6 end.
            dst_subnet: Remote proxy ID IPv4 subnet.
            dst_subnet6: Remote proxy ID IPv6 subnet.
            dst_port: Quick mode destination port (1 - 65535 or 0 for all).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            phase1name=phase1name,
            dhcp_ipsec=dhcp_ipsec,
            use_natip=use_natip,
            selector_match=selector_match,
            proposal=proposal,
            pfs=pfs,
            dhgrp=dhgrp,
            addke1=addke1,
            addke2=addke2,
            addke3=addke3,
            addke4=addke4,
            addke5=addke5,
            addke6=addke6,
            addke7=addke7,
            replay=replay,
            keepalive=keepalive,
            auto_negotiate=auto_negotiate,
            add_route=add_route,
            inbound_dscp_copy=inbound_dscp_copy,
            keylifeseconds=keylifeseconds,
            keylifekbs=keylifekbs,
            keylife_type=keylife_type,
            single_source=single_source,
            route_overlap=route_overlap,
            encapsulation=encapsulation,
            l2tp=l2tp,
            comments=comments,
            initiator_ts_narrow=initiator_ts_narrow,
            diffserv=diffserv,
            diffservcode=diffservcode,
            protocol=protocol,
            src_name=src_name,
            src_name6=src_name6,
            src_addr_type=src_addr_type,
            src_start_ip=src_start_ip,
            src_start_ip6=src_start_ip6,
            src_end_ip=src_end_ip,
            src_end_ip6=src_end_ip6,
            src_subnet=src_subnet,
            src_subnet6=src_subnet6,
            src_port=src_port,
            dst_name=dst_name,
            dst_name6=dst_name6,
            dst_addr_type=dst_addr_type,
            dst_start_ip=dst_start_ip,
            dst_start_ip6=dst_start_ip6,
            dst_end_ip=dst_end_ip,
            dst_end_ip6=dst_end_ip6,
            dst_subnet=dst_subnet,
            dst_subnet6=dst_subnet6,
            dst_port=dst_port,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.phase2 import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/vpn/ipsec/phase2",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/vpn.ipsec/phase2/" + quote_path_param(name_value)

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
        phase1name: str | None = None,
        dhcp_ipsec: Literal["enable", "disable"] | None = None,
        use_natip: Literal["enable", "disable"] | None = None,
        selector_match: Literal["exact", "subset", "auto"] | None = None,
        proposal: Literal["null-md5", "null-sha1", "null-sha256", "null-sha384", "null-sha512", "des-null", "des-md5", "des-sha1", "des-sha256", "des-sha384", "des-sha512", "3des-null", "3des-md5", "3des-sha1", "3des-sha256", "3des-sha384", "3des-sha512", "aes128-null", "aes128-md5", "aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes128gcm", "aes192-null", "aes192-md5", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-null", "aes256-md5", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes256gcm", "chacha20poly1305", "aria128-null", "aria128-md5", "aria128-sha1", "aria128-sha256", "aria128-sha384", "aria128-sha512", "aria192-null", "aria192-md5", "aria192-sha1", "aria192-sha256", "aria192-sha384", "aria192-sha512", "aria256-null", "aria256-md5", "aria256-sha1", "aria256-sha256", "aria256-sha384", "aria256-sha512", "seed-null", "seed-md5", "seed-sha1", "seed-sha256", "seed-sha384", "seed-sha512"] | list[str] | None = None,
        pfs: Literal["enable", "disable"] | None = None,
        dhgrp: Literal["1", "2", "5", "14", "15", "16", "17", "18", "19", "20", "21", "27", "28", "29", "30", "31", "32"] | list[str] | None = None,
        addke1: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke2: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke3: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke4: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke5: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke6: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        addke7: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | None = None,
        replay: Literal["enable", "disable"] | None = None,
        keepalive: Literal["enable", "disable"] | None = None,
        auto_negotiate: Literal["enable", "disable"] | None = None,
        add_route: Literal["phase1", "enable", "disable"] | None = None,
        inbound_dscp_copy: Literal["phase1", "enable", "disable"] | None = None,
        keylifeseconds: int | None = None,
        keylifekbs: int | None = None,
        keylife_type: Literal["seconds", "kbs", "both"] | None = None,
        single_source: Literal["enable", "disable"] | None = None,
        route_overlap: Literal["use-old", "use-new", "allow"] | None = None,
        encapsulation: Literal["tunnel-mode", "transport-mode"] | None = None,
        l2tp: Literal["enable", "disable"] | None = None,
        comments: str | None = None,
        initiator_ts_narrow: Literal["enable", "disable"] | None = None,
        diffserv: Literal["enable", "disable"] | None = None,
        diffservcode: str | None = None,
        protocol: int | None = None,
        src_name: str | None = None,
        src_name6: str | None = None,
        src_addr_type: Literal["subnet", "range", "ip", "name"] | None = None,
        src_start_ip: str | None = None,
        src_start_ip6: str | None = None,
        src_end_ip: str | None = None,
        src_end_ip6: str | None = None,
        src_subnet: Any | None = None,
        src_subnet6: str | None = None,
        src_port: int | None = None,
        dst_name: str | None = None,
        dst_name6: str | None = None,
        dst_addr_type: Literal["subnet", "range", "ip", "name"] | None = None,
        dst_start_ip: str | None = None,
        dst_start_ip6: str | None = None,
        dst_end_ip: str | None = None,
        dst_end_ip6: str | None = None,
        dst_subnet: Any | None = None,
        dst_subnet6: str | None = None,
        dst_port: int | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new vpn/ipsec/phase2 object.

        Configure VPN autokey tunnel.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: IPsec tunnel name.
            phase1name: Phase 1 determines the options required for phase 2.
            dhcp_ipsec: Enable/disable DHCP-IPsec.
            use_natip: Enable to use the FortiGate public IP as the source selector when outbound NAT is used.
            selector_match: Match type to use when comparing selectors.
            proposal: Phase2 proposal.
            pfs: Enable/disable PFS feature.
            dhgrp: Phase2 DH group.
            addke1: phase2 ADDKE1 group.
            addke2: phase2 ADDKE2 group.
            addke3: phase2 ADDKE3 group.
            addke4: phase2 ADDKE4 group.
            addke5: phase2 ADDKE5 group.
            addke6: phase2 ADDKE6 group.
            addke7: phase2 ADDKE7 group.
            replay: Enable/disable replay detection.
            keepalive: Enable/disable keep alive.
            auto_negotiate: Enable/disable IPsec SA auto-negotiation.
            add_route: Enable/disable automatic route addition.
            inbound_dscp_copy: Enable/disable copying of the DSCP in the ESP header to the inner IP header.
            keylifeseconds: Phase2 key life in time in seconds (120 - 172800).
            keylifekbs: Phase2 key life in number of kilobytes of traffic (5120 - 4294967295).
            keylife_type: Keylife type.
            single_source: Enable/disable single source IP restriction.
            route_overlap: Action for overlapping routes.
            encapsulation: ESP encapsulation mode.
            l2tp: Enable/disable L2TP over IPsec.
            comments: Comment.
            initiator_ts_narrow: Enable/disable traffic selector narrowing for IKEv2 initiator.
            diffserv: Enable/disable applying DSCP value to the IPsec tunnel outer IP header.
            diffservcode: DSCP value to be applied to the IPsec tunnel outer IP header.
            protocol: Quick mode protocol selector (1 - 255 or 0 for all).
            src_name: Local proxy ID name.
            src_name6: Local proxy ID name.
            src_addr_type: Local proxy ID type.
            src_start_ip: Local proxy ID start.
            src_start_ip6: Local proxy ID IPv6 start.
            src_end_ip: Local proxy ID end.
            src_end_ip6: Local proxy ID IPv6 end.
            src_subnet: Local proxy ID subnet.
            src_subnet6: Local proxy ID IPv6 subnet.
            src_port: Quick mode source port (1 - 65535 or 0 for all).
            dst_name: Remote proxy ID name.
            dst_name6: Remote proxy ID name.
            dst_addr_type: Remote proxy ID type.
            dst_start_ip: Remote proxy ID IPv4 start.
            dst_start_ip6: Remote proxy ID IPv6 start.
            dst_end_ip: Remote proxy ID IPv4 end.
            dst_end_ip6: Remote proxy ID IPv6 end.
            dst_subnet: Remote proxy ID IPv4 subnet.
            dst_subnet6: Remote proxy ID IPv6 subnet.
            dst_port: Quick mode destination port (1 - 65535 or 0 for all).
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Phase2.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Phase2.required_fields()) }}
            
            Use Phase2.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            phase1name=phase1name,
            dhcp_ipsec=dhcp_ipsec,
            use_natip=use_natip,
            selector_match=selector_match,
            proposal=proposal,
            pfs=pfs,
            dhgrp=dhgrp,
            addke1=addke1,
            addke2=addke2,
            addke3=addke3,
            addke4=addke4,
            addke5=addke5,
            addke6=addke6,
            addke7=addke7,
            replay=replay,
            keepalive=keepalive,
            auto_negotiate=auto_negotiate,
            add_route=add_route,
            inbound_dscp_copy=inbound_dscp_copy,
            keylifeseconds=keylifeseconds,
            keylifekbs=keylifekbs,
            keylife_type=keylife_type,
            single_source=single_source,
            route_overlap=route_overlap,
            encapsulation=encapsulation,
            l2tp=l2tp,
            comments=comments,
            initiator_ts_narrow=initiator_ts_narrow,
            diffserv=diffserv,
            diffservcode=diffservcode,
            protocol=protocol,
            src_name=src_name,
            src_name6=src_name6,
            src_addr_type=src_addr_type,
            src_start_ip=src_start_ip,
            src_start_ip6=src_start_ip6,
            src_end_ip=src_end_ip,
            src_end_ip6=src_end_ip6,
            src_subnet=src_subnet,
            src_subnet6=src_subnet6,
            src_port=src_port,
            dst_name=dst_name,
            dst_name6=dst_name6,
            dst_addr_type=dst_addr_type,
            dst_start_ip=dst_start_ip,
            dst_start_ip6=dst_start_ip6,
            dst_end_ip=dst_end_ip,
            dst_end_ip6=dst_end_ip6,
            dst_subnet=dst_subnet,
            dst_subnet6=dst_subnet6,
            dst_port=dst_port,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.phase2 import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/vpn/ipsec/phase2",
            )

        endpoint = "/vpn.ipsec/phase2"
        
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
        Delete vpn/ipsec/phase2 object.

        Configure VPN autokey tunnel.

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
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/vpn.ipsec/phase2/" + quote_path_param(name)

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
        Check if vpn/ipsec/phase2 object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.vpn_ipsec_phase2.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.vpn_ipsec_phase2.exists(name=1):
            ...     fgt.api.cmdb.vpn_ipsec_phase2.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/vpn.ipsec/phase2"
        endpoint = f"{endpoint}/{quote_path_param(name)}"
        
        try:
            # Use silent=True to suppress 404 error logging
            result = self._client.get("cmdb", endpoint, vdom=vdom, silent=True)
            
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
        name: str | None = None,
        phase1name: str | None = None,
        dhcp_ipsec: Literal["enable", "disable"] | None = None,
        use_natip: Literal["enable", "disable"] | None = None,
        selector_match: Literal["exact", "subset", "auto"] | None = None,
        proposal: Literal["null-md5", "null-sha1", "null-sha256", "null-sha384", "null-sha512", "des-null", "des-md5", "des-sha1", "des-sha256", "des-sha384", "des-sha512", "3des-null", "3des-md5", "3des-sha1", "3des-sha256", "3des-sha384", "3des-sha512", "aes128-null", "aes128-md5", "aes128-sha1", "aes128-sha256", "aes128-sha384", "aes128-sha512", "aes128gcm", "aes192-null", "aes192-md5", "aes192-sha1", "aes192-sha256", "aes192-sha384", "aes192-sha512", "aes256-null", "aes256-md5", "aes256-sha1", "aes256-sha256", "aes256-sha384", "aes256-sha512", "aes256gcm", "chacha20poly1305", "aria128-null", "aria128-md5", "aria128-sha1", "aria128-sha256", "aria128-sha384", "aria128-sha512", "aria192-null", "aria192-md5", "aria192-sha1", "aria192-sha256", "aria192-sha384", "aria192-sha512", "aria256-null", "aria256-md5", "aria256-sha1", "aria256-sha256", "aria256-sha384", "aria256-sha512", "seed-null", "seed-md5", "seed-sha1", "seed-sha256", "seed-sha384", "seed-sha512"] | list[str] | list[dict[str, Any]] | None = None,
        pfs: Literal["enable", "disable"] | None = None,
        dhgrp: Literal["1", "2", "5", "14", "15", "16", "17", "18", "19", "20", "21", "27", "28", "29", "30", "31", "32"] | list[str] | list[dict[str, Any]] | None = None,
        addke1: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | list[dict[str, Any]] | None = None,
        addke2: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | list[dict[str, Any]] | None = None,
        addke3: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | list[dict[str, Any]] | None = None,
        addke4: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | list[dict[str, Any]] | None = None,
        addke5: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | list[dict[str, Any]] | None = None,
        addke6: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | list[dict[str, Any]] | None = None,
        addke7: Literal["0", "35", "36", "37", "1080", "1081", "1082", "1083", "1084", "1085", "1089", "1090", "1091", "1092", "1093", "1094"] | list[str] | list[dict[str, Any]] | None = None,
        replay: Literal["enable", "disable"] | None = None,
        keepalive: Literal["enable", "disable"] | None = None,
        auto_negotiate: Literal["enable", "disable"] | None = None,
        add_route: Literal["phase1", "enable", "disable"] | None = None,
        inbound_dscp_copy: Literal["phase1", "enable", "disable"] | None = None,
        keylifeseconds: int | None = None,
        keylifekbs: int | None = None,
        keylife_type: Literal["seconds", "kbs", "both"] | None = None,
        single_source: Literal["enable", "disable"] | None = None,
        route_overlap: Literal["use-old", "use-new", "allow"] | None = None,
        encapsulation: Literal["tunnel-mode", "transport-mode"] | None = None,
        l2tp: Literal["enable", "disable"] | None = None,
        comments: str | None = None,
        initiator_ts_narrow: Literal["enable", "disable"] | None = None,
        diffserv: Literal["enable", "disable"] | None = None,
        diffservcode: str | None = None,
        protocol: int | None = None,
        src_name: str | None = None,
        src_name6: str | None = None,
        src_addr_type: Literal["subnet", "range", "ip", "name"] | None = None,
        src_start_ip: str | None = None,
        src_start_ip6: str | None = None,
        src_end_ip: str | None = None,
        src_end_ip6: str | None = None,
        src_subnet: Any | None = None,
        src_subnet6: str | None = None,
        src_port: int | None = None,
        dst_name: str | None = None,
        dst_name6: str | None = None,
        dst_addr_type: Literal["subnet", "range", "ip", "name"] | None = None,
        dst_start_ip: str | None = None,
        dst_start_ip6: str | None = None,
        dst_end_ip: str | None = None,
        dst_end_ip6: str | None = None,
        dst_subnet: Any | None = None,
        dst_subnet6: str | None = None,
        dst_port: int | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update vpn/ipsec/phase2 object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            phase1name: Field phase1name
            dhcp_ipsec: Field dhcp-ipsec
            use_natip: Field use-natip
            selector_match: Field selector-match
            proposal: Field proposal
            pfs: Field pfs
            dhgrp: Field dhgrp
            addke1: Field addke1
            addke2: Field addke2
            addke3: Field addke3
            addke4: Field addke4
            addke5: Field addke5
            addke6: Field addke6
            addke7: Field addke7
            replay: Field replay
            keepalive: Field keepalive
            auto_negotiate: Field auto-negotiate
            add_route: Field add-route
            inbound_dscp_copy: Field inbound-dscp-copy
            keylifeseconds: Field keylifeseconds
            keylifekbs: Field keylifekbs
            keylife_type: Field keylife-type
            single_source: Field single-source
            route_overlap: Field route-overlap
            encapsulation: Field encapsulation
            l2tp: Field l2tp
            comments: Field comments
            initiator_ts_narrow: Field initiator-ts-narrow
            diffserv: Field diffserv
            diffservcode: Field diffservcode
            protocol: Field protocol
            src_name: Field src-name
            src_name6: Field src-name6
            src_addr_type: Field src-addr-type
            src_start_ip: Field src-start-ip
            src_start_ip6: Field src-start-ip6
            src_end_ip: Field src-end-ip
            src_end_ip6: Field src-end-ip6
            src_subnet: Field src-subnet
            src_subnet6: Field src-subnet6
            src_port: Field src-port
            dst_name: Field dst-name
            dst_name6: Field dst-name6
            dst_addr_type: Field dst-addr-type
            dst_start_ip: Field dst-start-ip
            dst_start_ip6: Field dst-start-ip6
            dst_end_ip: Field dst-end-ip
            dst_end_ip6: Field dst-end-ip6
            dst_subnet: Field dst-subnet
            dst_subnet6: Field dst-subnet6
            dst_port: Field dst-port
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.vpn_ipsec_phase2.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.vpn_ipsec_phase2.set(payload_dict=obj_data)
            >>> # Safely applies configuration regardless of current state

        Note:
            This method internally calls exists() then either post() or put().
            For performance-critical code with known state, call post() or put() directly.

        See Also:
            - post(): Create new object
            - put(): Update existing object
            - exists(): Check existence manually
        """
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            phase1name=phase1name,
            dhcp_ipsec=dhcp_ipsec,
            use_natip=use_natip,
            selector_match=selector_match,
            proposal=proposal,
            pfs=pfs,
            dhgrp=dhgrp,
            addke1=addke1,
            addke2=addke2,
            addke3=addke3,
            addke4=addke4,
            addke5=addke5,
            addke6=addke6,
            addke7=addke7,
            replay=replay,
            keepalive=keepalive,
            auto_negotiate=auto_negotiate,
            add_route=add_route,
            inbound_dscp_copy=inbound_dscp_copy,
            keylifeseconds=keylifeseconds,
            keylifekbs=keylifekbs,
            keylife_type=keylife_type,
            single_source=single_source,
            route_overlap=route_overlap,
            encapsulation=encapsulation,
            l2tp=l2tp,
            comments=comments,
            initiator_ts_narrow=initiator_ts_narrow,
            diffserv=diffserv,
            diffservcode=diffservcode,
            protocol=protocol,
            src_name=src_name,
            src_name6=src_name6,
            src_addr_type=src_addr_type,
            src_start_ip=src_start_ip,
            src_start_ip6=src_start_ip6,
            src_end_ip=src_end_ip,
            src_end_ip6=src_end_ip6,
            src_subnet=src_subnet,
            src_subnet6=src_subnet6,
            src_port=src_port,
            dst_name=dst_name,
            dst_name6=dst_name6,
            dst_addr_type=dst_addr_type,
            dst_start_ip=dst_start_ip,
            dst_start_ip6=dst_start_ip6,
            dst_end_ip=dst_end_ip,
            dst_end_ip6=dst_end_ip6,
            dst_subnet=dst_subnet,
            dst_subnet6=dst_subnet6,
            dst_port=dst_port,
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
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move vpn/ipsec/phase2 object to a new position.
        
        Reorders objects by moving one before/after another, to top/bottom, or to a specific position.
        
        Args:
            name: Identifier of object to move
            position: Where to move the object:
                - "before": Move before reference object (requires reference_name)
                - "after": Move after reference object (requires reference_name)
                - "top": Move to first position (reference not needed)
                - "bottom": Move to last position (reference not needed)
                - int (1-based): Move to specific position number (e.g., position=3 for 3rd place)
            reference_name: Identifier of reference object (required for before/after)
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.vpn_ipsec_phase2.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.vpn_ipsec_phase2.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.vpn_ipsec_phase2.move(
            ...     name=100,
            ...     position="before",
            ...     reference_name=50
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
        endpoint = "/vpn.ipsec/phase2/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





