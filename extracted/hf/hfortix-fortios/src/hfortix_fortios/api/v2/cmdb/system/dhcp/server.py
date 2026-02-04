"""
FortiOS CMDB - System dhcp server

Configuration endpoint for managing cmdb system/dhcp/server objects.

API Endpoints:
    GET    /cmdb/system/dhcp/server
    POST   /cmdb/system/dhcp/server
    PUT    /cmdb/system/dhcp/server/{identifier}
    DELETE /cmdb/system/dhcp/server/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_dhcp_server.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_dhcp_server.post(
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
        "ip_range": {
            "mkey": "id",
            "required_fields": ['id', 'start-ip', 'end-ip'],
            "example": "[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
        },
        "tftp_server": {
            "mkey": "tftp-server",
            "required_fields": ['tftp-server'],
            "example": "[{'tftp-server': 'value'}]",
        },
        "options": {
            "mkey": "id",
            "required_fields": ['id', 'code'],
            "example": "[{'id': 1, 'code': 1}]",
        },
        "vci_string": {
            "mkey": "vci-string",
            "required_fields": ['vci-string'],
            "example": "[{'vci-string': 'value'}]",
        },
        "exclude_range": {
            "mkey": "id",
            "required_fields": ['id', 'start-ip', 'end-ip'],
            "example": "[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
        },
        "reserved_address": {
            "mkey": "id",
            "required_fields": ['id', 'ip', 'mac'],
            "example": "[{'id': 1, 'ip': '192.168.1.10', 'mac': 'value'}]",
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
        Retrieve system/dhcp/server configuration.

        Configure DHCP servers.

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
            >>> # Get all system/dhcp/server objects
            >>> result = fgt.api.cmdb.system_dhcp_server.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/dhcp/server by id
            >>> result = fgt.api.cmdb.system_dhcp_server.get(id=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_dhcp_server.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_dhcp_server.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_dhcp_server.get_schema()

        See Also:
            - post(): Create new system/dhcp/server object
            - put(): Update existing system/dhcp/server object
            - delete(): Remove system/dhcp/server object
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
            endpoint = "/system.dhcp/server/" + quote_path_param(id)
            unwrap_single = True
        else:
            endpoint = "/system.dhcp/server"
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
            >>> schema = fgt.api.cmdb.system_dhcp_server.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_dhcp_server.get_schema(format="json-schema")
        
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
        lease_time: int | None = None,
        mac_acl_default_action: Literal["assign", "block"] | None = None,
        forticlient_on_net_status: Literal["disable", "enable"] | None = None,
        dns_service: Literal["local", "default", "specify"] | None = None,
        dns_server1: str | None = None,
        dns_server2: str | None = None,
        dns_server3: str | None = None,
        dns_server4: str | None = None,
        wifi_ac_service: Literal["specify", "local"] | None = None,
        wifi_ac1: str | None = None,
        wifi_ac2: str | None = None,
        wifi_ac3: str | None = None,
        ntp_service: Literal["local", "default", "specify"] | None = None,
        ntp_server1: str | None = None,
        ntp_server2: str | None = None,
        ntp_server3: str | None = None,
        domain: str | None = None,
        wins_server1: str | None = None,
        wins_server2: str | None = None,
        default_gateway: str | None = None,
        next_server: str | None = None,
        netmask: str | None = None,
        interface: str | None = None,
        ip_range: str | list[str] | list[dict[str, Any]] | None = None,
        timezone_option: Literal["disable", "default", "specify"] | None = None,
        timezone: str | None = None,
        tftp_server: str | list[str] | list[dict[str, Any]] | None = None,
        filename: str | None = None,
        options: str | list[str] | list[dict[str, Any]] | None = None,
        server_type: Literal["regular", "ipsec"] | None = None,
        ip_mode: Literal["range", "usrgrp"] | None = None,
        conflicted_ip_timeout: int | None = None,
        ipsec_lease_hold: int | None = None,
        auto_configuration: Literal["disable", "enable"] | None = None,
        dhcp_settings_from_fortiipam: Literal["disable", "enable"] | None = None,
        auto_managed_status: Literal["disable", "enable"] | None = None,
        ddns_update: Literal["disable", "enable"] | None = None,
        ddns_update_override: Literal["disable", "enable"] | None = None,
        ddns_server_ip: str | None = None,
        ddns_zone: str | None = None,
        ddns_auth: Literal["disable", "tsig"] | None = None,
        ddns_keyname: str | None = None,
        ddns_key: Any | None = None,
        ddns_ttl: int | None = None,
        vci_match: Literal["disable", "enable"] | None = None,
        vci_string: str | list[str] | list[dict[str, Any]] | None = None,
        exclude_range: str | list[str] | list[dict[str, Any]] | None = None,
        shared_subnet: Literal["disable", "enable"] | None = None,
        relay_agent: str | None = None,
        reserved_address: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/dhcp/server object.

        Configure DHCP servers.

        Args:
            payload_dict: Object data as dict. Must include id (primary key).
            id: ID.
            status: Enable/disable this DHCP configuration.
            lease_time: Lease time in seconds, 0 means unlimited.
            mac_acl_default_action: MAC access control default action (allow or block assigning IP settings).
            forticlient_on_net_status: Enable/disable FortiClient-On-Net service for this DHCP server.
            dns_service: Options for assigning DNS servers to DHCP clients.
            dns_server1: DNS server 1.
            dns_server2: DNS server 2.
            dns_server3: DNS server 3.
            dns_server4: DNS server 4.
            wifi_ac_service: Options for assigning WiFi access controllers to DHCP clients.
            wifi_ac1: WiFi Access Controller 1 IP address (DHCP option 138, RFC 5417).
            wifi_ac2: WiFi Access Controller 2 IP address (DHCP option 138, RFC 5417).
            wifi_ac3: WiFi Access Controller 3 IP address (DHCP option 138, RFC 5417).
            ntp_service: Options for assigning Network Time Protocol (NTP) servers to DHCP clients.
            ntp_server1: NTP server 1.
            ntp_server2: NTP server 2.
            ntp_server3: NTP server 3.
            domain: Domain name suffix for the IP addresses that the DHCP server assigns to clients.
            wins_server1: WINS server 1.
            wins_server2: WINS server 2.
            default_gateway: Default gateway IP address assigned by the DHCP server.
            next_server: IP address of a server (for example, a TFTP sever) that DHCP clients can download a boot file from.
            netmask: Netmask assigned by the DHCP server.
            interface: DHCP server can assign IP configurations to clients connected to this interface.
            ip_range: DHCP IP range configuration.
                Default format: [{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]
                Required format: List of dicts with keys: id, start-ip, end-ip
                  (String format not allowed due to multiple required fields)
            timezone_option: Options for the DHCP server to set the client's time zone.
            timezone: Select the time zone to be assigned to DHCP clients.
            tftp_server: One or more hostnames or IP addresses of the TFTP servers in quotes separated by spaces.
                Default format: [{'tftp-server': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'tftp-server': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'tftp-server': 'val1'}, ...]
                  - List of dicts: [{'tftp-server': 'value'}] (recommended)
            filename: Name of the boot file on the TFTP server.
            options: DHCP options.
                Default format: [{'id': 1, 'code': 1}]
                Required format: List of dicts with keys: id, code
                  (String format not allowed due to multiple required fields)
            server_type: DHCP server can be a normal DHCP server or an IPsec DHCP server.
            ip_mode: Method used to assign client IP.
            conflicted_ip_timeout: Time in seconds to wait after a conflicted IP address is removed from the DHCP range before it can be reused.
            ipsec_lease_hold: DHCP over IPsec leases expire this many seconds after tunnel down (0 to disable forced-expiry).
            auto_configuration: Enable/disable auto configuration.
            dhcp_settings_from_fortiipam: Enable/disable populating of DHCP server settings from FortiIPAM.
            auto_managed_status: Enable/disable use of this DHCP server once this interface has been assigned an IP address from FortiIPAM.
            ddns_update: Enable/disable DDNS update for DHCP.
            ddns_update_override: Enable/disable DDNS update override for DHCP.
            ddns_server_ip: DDNS server IP.
            ddns_zone: Zone of your domain name (ex. DDNS.com).
            ddns_auth: DDNS authentication mode.
            ddns_keyname: DDNS update key name.
            ddns_key: DDNS update key (base 64 encoding).
            ddns_ttl: TTL.
            vci_match: Enable/disable vendor class identifier (VCI) matching. When enabled only DHCP requests with a matching VCI are served.
            vci_string: One or more VCI strings in quotes separated by spaces.
                Default format: [{'vci-string': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'vci-string': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'vci-string': 'val1'}, ...]
                  - List of dicts: [{'vci-string': 'value'}] (recommended)
            exclude_range: Exclude one or more ranges of IP addresses from being assigned to clients.
                Default format: [{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]
                Required format: List of dicts with keys: id, start-ip, end-ip
                  (String format not allowed due to multiple required fields)
            shared_subnet: Enable/disable shared subnet.
            relay_agent: Relay agent IP.
            reserved_address: Options for the DHCP server to assign IP settings to specific MAC addresses.
                Default format: [{'id': 1, 'ip': '192.168.1.10', 'mac': 'value'}]
                Required format: List of dicts with keys: id, ip, mac
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
            >>> result = fgt.api.cmdb.system_dhcp_server.put(
            ...     id=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "id": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_dhcp_server.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if ip_range is not None:
            ip_range = normalize_table_field(
                ip_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="ip_range",
                example="[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
            )
        if tftp_server is not None:
            tftp_server = normalize_table_field(
                tftp_server,
                mkey="tftp-server",
                required_fields=['tftp-server'],
                field_name="tftp_server",
                example="[{'tftp-server': 'value'}]",
            )
        if options is not None:
            options = normalize_table_field(
                options,
                mkey="id",
                required_fields=['id', 'code'],
                field_name="options",
                example="[{'id': 1, 'code': 1}]",
            )
        if vci_string is not None:
            vci_string = normalize_table_field(
                vci_string,
                mkey="vci-string",
                required_fields=['vci-string'],
                field_name="vci_string",
                example="[{'vci-string': 'value'}]",
            )
        if exclude_range is not None:
            exclude_range = normalize_table_field(
                exclude_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="exclude_range",
                example="[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
            )
        if reserved_address is not None:
            reserved_address = normalize_table_field(
                reserved_address,
                mkey="id",
                required_fields=['id', 'ip', 'mac'],
                field_name="reserved_address",
                example="[{'id': 1, 'ip': '192.168.1.10', 'mac': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            id=id,
            status=status,
            lease_time=lease_time,
            mac_acl_default_action=mac_acl_default_action,
            forticlient_on_net_status=forticlient_on_net_status,
            dns_service=dns_service,
            dns_server1=dns_server1,
            dns_server2=dns_server2,
            dns_server3=dns_server3,
            dns_server4=dns_server4,
            wifi_ac_service=wifi_ac_service,
            wifi_ac1=wifi_ac1,
            wifi_ac2=wifi_ac2,
            wifi_ac3=wifi_ac3,
            ntp_service=ntp_service,
            ntp_server1=ntp_server1,
            ntp_server2=ntp_server2,
            ntp_server3=ntp_server3,
            domain=domain,
            wins_server1=wins_server1,
            wins_server2=wins_server2,
            default_gateway=default_gateway,
            next_server=next_server,
            netmask=netmask,
            interface=interface,
            ip_range=ip_range,
            timezone_option=timezone_option,
            timezone=timezone,
            tftp_server=tftp_server,
            filename=filename,
            options=options,
            server_type=server_type,
            ip_mode=ip_mode,
            conflicted_ip_timeout=conflicted_ip_timeout,
            ipsec_lease_hold=ipsec_lease_hold,
            auto_configuration=auto_configuration,
            dhcp_settings_from_fortiipam=dhcp_settings_from_fortiipam,
            auto_managed_status=auto_managed_status,
            ddns_update=ddns_update,
            ddns_update_override=ddns_update_override,
            ddns_server_ip=ddns_server_ip,
            ddns_zone=ddns_zone,
            ddns_auth=ddns_auth,
            ddns_keyname=ddns_keyname,
            ddns_key=ddns_key,
            ddns_ttl=ddns_ttl,
            vci_match=vci_match,
            vci_string=vci_string,
            exclude_range=exclude_range,
            shared_subnet=shared_subnet,
            relay_agent=relay_agent,
            reserved_address=reserved_address,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.server import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/dhcp/server",
            )
        
        id_value = payload_data.get("id")
        if not id_value:
            raise ValueError("id is required for PUT")
        endpoint = "/system.dhcp/server/" + quote_path_param(id_value)

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
        lease_time: int | None = None,
        mac_acl_default_action: Literal["assign", "block"] | None = None,
        forticlient_on_net_status: Literal["disable", "enable"] | None = None,
        dns_service: Literal["local", "default", "specify"] | None = None,
        dns_server1: str | None = None,
        dns_server2: str | None = None,
        dns_server3: str | None = None,
        dns_server4: str | None = None,
        wifi_ac_service: Literal["specify", "local"] | None = None,
        wifi_ac1: str | None = None,
        wifi_ac2: str | None = None,
        wifi_ac3: str | None = None,
        ntp_service: Literal["local", "default", "specify"] | None = None,
        ntp_server1: str | None = None,
        ntp_server2: str | None = None,
        ntp_server3: str | None = None,
        domain: str | None = None,
        wins_server1: str | None = None,
        wins_server2: str | None = None,
        default_gateway: str | None = None,
        next_server: str | None = None,
        netmask: str | None = None,
        interface: str | None = None,
        ip_range: str | list[str] | list[dict[str, Any]] | None = None,
        timezone_option: Literal["disable", "default", "specify"] | None = None,
        timezone: str | None = None,
        tftp_server: str | list[str] | list[dict[str, Any]] | None = None,
        filename: str | None = None,
        options: str | list[str] | list[dict[str, Any]] | None = None,
        server_type: Literal["regular", "ipsec"] | None = None,
        ip_mode: Literal["range", "usrgrp"] | None = None,
        conflicted_ip_timeout: int | None = None,
        ipsec_lease_hold: int | None = None,
        auto_configuration: Literal["disable", "enable"] | None = None,
        dhcp_settings_from_fortiipam: Literal["disable", "enable"] | None = None,
        auto_managed_status: Literal["disable", "enable"] | None = None,
        ddns_update: Literal["disable", "enable"] | None = None,
        ddns_update_override: Literal["disable", "enable"] | None = None,
        ddns_server_ip: str | None = None,
        ddns_zone: str | None = None,
        ddns_auth: Literal["disable", "tsig"] | None = None,
        ddns_keyname: str | None = None,
        ddns_key: Any | None = None,
        ddns_ttl: int | None = None,
        vci_match: Literal["disable", "enable"] | None = None,
        vci_string: str | list[str] | list[dict[str, Any]] | None = None,
        exclude_range: str | list[str] | list[dict[str, Any]] | None = None,
        shared_subnet: Literal["disable", "enable"] | None = None,
        relay_agent: str | None = None,
        reserved_address: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/dhcp/server object.

        Configure DHCP servers.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            id: ID.
            status: Enable/disable this DHCP configuration.
            lease_time: Lease time in seconds, 0 means unlimited.
            mac_acl_default_action: MAC access control default action (allow or block assigning IP settings).
            forticlient_on_net_status: Enable/disable FortiClient-On-Net service for this DHCP server.
            dns_service: Options for assigning DNS servers to DHCP clients.
            dns_server1: DNS server 1.
            dns_server2: DNS server 2.
            dns_server3: DNS server 3.
            dns_server4: DNS server 4.
            wifi_ac_service: Options for assigning WiFi access controllers to DHCP clients.
            wifi_ac1: WiFi Access Controller 1 IP address (DHCP option 138, RFC 5417).
            wifi_ac2: WiFi Access Controller 2 IP address (DHCP option 138, RFC 5417).
            wifi_ac3: WiFi Access Controller 3 IP address (DHCP option 138, RFC 5417).
            ntp_service: Options for assigning Network Time Protocol (NTP) servers to DHCP clients.
            ntp_server1: NTP server 1.
            ntp_server2: NTP server 2.
            ntp_server3: NTP server 3.
            domain: Domain name suffix for the IP addresses that the DHCP server assigns to clients.
            wins_server1: WINS server 1.
            wins_server2: WINS server 2.
            default_gateway: Default gateway IP address assigned by the DHCP server.
            next_server: IP address of a server (for example, a TFTP sever) that DHCP clients can download a boot file from.
            netmask: Netmask assigned by the DHCP server.
            interface: DHCP server can assign IP configurations to clients connected to this interface.
            ip_range: DHCP IP range configuration.
                Default format: [{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]
                Required format: List of dicts with keys: id, start-ip, end-ip
                  (String format not allowed due to multiple required fields)
            timezone_option: Options for the DHCP server to set the client's time zone.
            timezone: Select the time zone to be assigned to DHCP clients.
            tftp_server: One or more hostnames or IP addresses of the TFTP servers in quotes separated by spaces.
                Default format: [{'tftp-server': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'tftp-server': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'tftp-server': 'val1'}, ...]
                  - List of dicts: [{'tftp-server': 'value'}] (recommended)
            filename: Name of the boot file on the TFTP server.
            options: DHCP options.
                Default format: [{'id': 1, 'code': 1}]
                Required format: List of dicts with keys: id, code
                  (String format not allowed due to multiple required fields)
            server_type: DHCP server can be a normal DHCP server or an IPsec DHCP server.
            ip_mode: Method used to assign client IP.
            conflicted_ip_timeout: Time in seconds to wait after a conflicted IP address is removed from the DHCP range before it can be reused.
            ipsec_lease_hold: DHCP over IPsec leases expire this many seconds after tunnel down (0 to disable forced-expiry).
            auto_configuration: Enable/disable auto configuration.
            dhcp_settings_from_fortiipam: Enable/disable populating of DHCP server settings from FortiIPAM.
            auto_managed_status: Enable/disable use of this DHCP server once this interface has been assigned an IP address from FortiIPAM.
            ddns_update: Enable/disable DDNS update for DHCP.
            ddns_update_override: Enable/disable DDNS update override for DHCP.
            ddns_server_ip: DDNS server IP.
            ddns_zone: Zone of your domain name (ex. DDNS.com).
            ddns_auth: DDNS authentication mode.
            ddns_keyname: DDNS update key name.
            ddns_key: DDNS update key (base 64 encoding).
            ddns_ttl: TTL.
            vci_match: Enable/disable vendor class identifier (VCI) matching. When enabled only DHCP requests with a matching VCI are served.
            vci_string: One or more VCI strings in quotes separated by spaces.
                Default format: [{'vci-string': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'vci-string': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'vci-string': 'val1'}, ...]
                  - List of dicts: [{'vci-string': 'value'}] (recommended)
            exclude_range: Exclude one or more ranges of IP addresses from being assigned to clients.
                Default format: [{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]
                Required format: List of dicts with keys: id, start-ip, end-ip
                  (String format not allowed due to multiple required fields)
            shared_subnet: Enable/disable shared subnet.
            relay_agent: Relay agent IP.
            reserved_address: Options for the DHCP server to assign IP settings to specific MAC addresses.
                Default format: [{'id': 1, 'ip': '192.168.1.10', 'mac': 'value'}]
                Required format: List of dicts with keys: id, ip, mac
                  (String format not allowed due to multiple required fields)
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_dhcp_server.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created id: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Server.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_dhcp_server.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Server.required_fields()) }}
            
            Use Server.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if ip_range is not None:
            ip_range = normalize_table_field(
                ip_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="ip_range",
                example="[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
            )
        if tftp_server is not None:
            tftp_server = normalize_table_field(
                tftp_server,
                mkey="tftp-server",
                required_fields=['tftp-server'],
                field_name="tftp_server",
                example="[{'tftp-server': 'value'}]",
            )
        if options is not None:
            options = normalize_table_field(
                options,
                mkey="id",
                required_fields=['id', 'code'],
                field_name="options",
                example="[{'id': 1, 'code': 1}]",
            )
        if vci_string is not None:
            vci_string = normalize_table_field(
                vci_string,
                mkey="vci-string",
                required_fields=['vci-string'],
                field_name="vci_string",
                example="[{'vci-string': 'value'}]",
            )
        if exclude_range is not None:
            exclude_range = normalize_table_field(
                exclude_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="exclude_range",
                example="[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
            )
        if reserved_address is not None:
            reserved_address = normalize_table_field(
                reserved_address,
                mkey="id",
                required_fields=['id', 'ip', 'mac'],
                field_name="reserved_address",
                example="[{'id': 1, 'ip': '192.168.1.10', 'mac': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            id=id,
            status=status,
            lease_time=lease_time,
            mac_acl_default_action=mac_acl_default_action,
            forticlient_on_net_status=forticlient_on_net_status,
            dns_service=dns_service,
            dns_server1=dns_server1,
            dns_server2=dns_server2,
            dns_server3=dns_server3,
            dns_server4=dns_server4,
            wifi_ac_service=wifi_ac_service,
            wifi_ac1=wifi_ac1,
            wifi_ac2=wifi_ac2,
            wifi_ac3=wifi_ac3,
            ntp_service=ntp_service,
            ntp_server1=ntp_server1,
            ntp_server2=ntp_server2,
            ntp_server3=ntp_server3,
            domain=domain,
            wins_server1=wins_server1,
            wins_server2=wins_server2,
            default_gateway=default_gateway,
            next_server=next_server,
            netmask=netmask,
            interface=interface,
            ip_range=ip_range,
            timezone_option=timezone_option,
            timezone=timezone,
            tftp_server=tftp_server,
            filename=filename,
            options=options,
            server_type=server_type,
            ip_mode=ip_mode,
            conflicted_ip_timeout=conflicted_ip_timeout,
            ipsec_lease_hold=ipsec_lease_hold,
            auto_configuration=auto_configuration,
            dhcp_settings_from_fortiipam=dhcp_settings_from_fortiipam,
            auto_managed_status=auto_managed_status,
            ddns_update=ddns_update,
            ddns_update_override=ddns_update_override,
            ddns_server_ip=ddns_server_ip,
            ddns_zone=ddns_zone,
            ddns_auth=ddns_auth,
            ddns_keyname=ddns_keyname,
            ddns_key=ddns_key,
            ddns_ttl=ddns_ttl,
            vci_match=vci_match,
            vci_string=vci_string,
            exclude_range=exclude_range,
            shared_subnet=shared_subnet,
            relay_agent=relay_agent,
            reserved_address=reserved_address,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.server import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/dhcp/server",
            )

        endpoint = "/system.dhcp/server"
        
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
        Delete system/dhcp/server object.

        Configure DHCP servers.

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
            >>> result = fgt.api.cmdb.system_dhcp_server.delete(id=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not id:
            raise ValueError("id is required for DELETE")
        endpoint = "/system.dhcp/server/" + quote_path_param(id)

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
        Check if system/dhcp/server object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            id: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_dhcp_server.exists(id=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_dhcp_server.exists(id=1):
            ...     fgt.api.cmdb.system_dhcp_server.delete(id=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system.dhcp/server"
        endpoint = f"{endpoint}/{quote_path_param(id)}"
        
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
        id: int | None = None,
        status: Literal["disable", "enable"] | None = None,
        lease_time: int | None = None,
        mac_acl_default_action: Literal["assign", "block"] | None = None,
        forticlient_on_net_status: Literal["disable", "enable"] | None = None,
        dns_service: Literal["local", "default", "specify"] | None = None,
        dns_server1: str | None = None,
        dns_server2: str | None = None,
        dns_server3: str | None = None,
        dns_server4: str | None = None,
        wifi_ac_service: Literal["specify", "local"] | None = None,
        wifi_ac1: str | None = None,
        wifi_ac2: str | None = None,
        wifi_ac3: str | None = None,
        ntp_service: Literal["local", "default", "specify"] | None = None,
        ntp_server1: str | None = None,
        ntp_server2: str | None = None,
        ntp_server3: str | None = None,
        domain: str | None = None,
        wins_server1: str | None = None,
        wins_server2: str | None = None,
        default_gateway: str | None = None,
        next_server: str | None = None,
        netmask: str | None = None,
        interface: str | None = None,
        ip_range: str | list[str] | list[dict[str, Any]] | None = None,
        timezone_option: Literal["disable", "default", "specify"] | None = None,
        timezone: str | None = None,
        tftp_server: str | list[str] | list[dict[str, Any]] | None = None,
        filename: str | None = None,
        options: str | list[str] | list[dict[str, Any]] | None = None,
        server_type: Literal["regular", "ipsec"] | None = None,
        ip_mode: Literal["range", "usrgrp"] | None = None,
        conflicted_ip_timeout: int | None = None,
        ipsec_lease_hold: int | None = None,
        auto_configuration: Literal["disable", "enable"] | None = None,
        dhcp_settings_from_fortiipam: Literal["disable", "enable"] | None = None,
        auto_managed_status: Literal["disable", "enable"] | None = None,
        ddns_update: Literal["disable", "enable"] | None = None,
        ddns_update_override: Literal["disable", "enable"] | None = None,
        ddns_server_ip: str | None = None,
        ddns_zone: str | None = None,
        ddns_auth: Literal["disable", "tsig"] | None = None,
        ddns_keyname: str | None = None,
        ddns_key: Any | None = None,
        ddns_ttl: int | None = None,
        vci_match: Literal["disable", "enable"] | None = None,
        vci_string: str | list[str] | list[dict[str, Any]] | None = None,
        exclude_range: str | list[str] | list[dict[str, Any]] | None = None,
        shared_subnet: Literal["disable", "enable"] | None = None,
        relay_agent: str | None = None,
        reserved_address: str | list[str] | list[dict[str, Any]] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/dhcp/server object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (id) in the payload.

        Args:
            payload_dict: Resource data including id (primary key)
            id: Field id
            status: Field status
            lease_time: Field lease-time
            mac_acl_default_action: Field mac-acl-default-action
            forticlient_on_net_status: Field forticlient-on-net-status
            dns_service: Field dns-service
            dns_server1: Field dns-server1
            dns_server2: Field dns-server2
            dns_server3: Field dns-server3
            dns_server4: Field dns-server4
            wifi_ac_service: Field wifi-ac-service
            wifi_ac1: Field wifi-ac1
            wifi_ac2: Field wifi-ac2
            wifi_ac3: Field wifi-ac3
            ntp_service: Field ntp-service
            ntp_server1: Field ntp-server1
            ntp_server2: Field ntp-server2
            ntp_server3: Field ntp-server3
            domain: Field domain
            wins_server1: Field wins-server1
            wins_server2: Field wins-server2
            default_gateway: Field default-gateway
            next_server: Field next-server
            netmask: Field netmask
            interface: Field interface
            ip_range: Field ip-range
            timezone_option: Field timezone-option
            timezone: Field timezone
            tftp_server: Field tftp-server
            filename: Field filename
            options: Field options
            server_type: Field server-type
            ip_mode: Field ip-mode
            conflicted_ip_timeout: Field conflicted-ip-timeout
            ipsec_lease_hold: Field ipsec-lease-hold
            auto_configuration: Field auto-configuration
            dhcp_settings_from_fortiipam: Field dhcp-settings-from-fortiipam
            auto_managed_status: Field auto-managed-status
            ddns_update: Field ddns-update
            ddns_update_override: Field ddns-update-override
            ddns_server_ip: Field ddns-server-ip
            ddns_zone: Field ddns-zone
            ddns_auth: Field ddns-auth
            ddns_keyname: Field ddns-keyname
            ddns_key: Field ddns-key
            ddns_ttl: Field ddns-ttl
            vci_match: Field vci-match
            vci_string: Field vci-string
            exclude_range: Field exclude-range
            shared_subnet: Field shared-subnet
            relay_agent: Field relay-agent
            reserved_address: Field reserved-address
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If id is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_dhcp_server.set(
            ...     id=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "id": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_dhcp_server.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_dhcp_server.set(payload_dict=obj_data)
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
        if ip_range is not None:
            ip_range = normalize_table_field(
                ip_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="ip_range",
                example="[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
            )
        if tftp_server is not None:
            tftp_server = normalize_table_field(
                tftp_server,
                mkey="tftp-server",
                required_fields=['tftp-server'],
                field_name="tftp_server",
                example="[{'tftp-server': 'value'}]",
            )
        if options is not None:
            options = normalize_table_field(
                options,
                mkey="id",
                required_fields=['id', 'code'],
                field_name="options",
                example="[{'id': 1, 'code': 1}]",
            )
        if vci_string is not None:
            vci_string = normalize_table_field(
                vci_string,
                mkey="vci-string",
                required_fields=['vci-string'],
                field_name="vci_string",
                example="[{'vci-string': 'value'}]",
            )
        if exclude_range is not None:
            exclude_range = normalize_table_field(
                exclude_range,
                mkey="id",
                required_fields=['id', 'start-ip', 'end-ip'],
                field_name="exclude_range",
                example="[{'id': 1, 'start-ip': '192.168.1.10', 'end-ip': '192.168.1.10'}]",
            )
        if reserved_address is not None:
            reserved_address = normalize_table_field(
                reserved_address,
                mkey="id",
                required_fields=['id', 'ip', 'mac'],
                field_name="reserved_address",
                example="[{'id': 1, 'ip': '192.168.1.10', 'mac': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            id=id,
            status=status,
            lease_time=lease_time,
            mac_acl_default_action=mac_acl_default_action,
            forticlient_on_net_status=forticlient_on_net_status,
            dns_service=dns_service,
            dns_server1=dns_server1,
            dns_server2=dns_server2,
            dns_server3=dns_server3,
            dns_server4=dns_server4,
            wifi_ac_service=wifi_ac_service,
            wifi_ac1=wifi_ac1,
            wifi_ac2=wifi_ac2,
            wifi_ac3=wifi_ac3,
            ntp_service=ntp_service,
            ntp_server1=ntp_server1,
            ntp_server2=ntp_server2,
            ntp_server3=ntp_server3,
            domain=domain,
            wins_server1=wins_server1,
            wins_server2=wins_server2,
            default_gateway=default_gateway,
            next_server=next_server,
            netmask=netmask,
            interface=interface,
            ip_range=ip_range,
            timezone_option=timezone_option,
            timezone=timezone,
            tftp_server=tftp_server,
            filename=filename,
            options=options,
            server_type=server_type,
            ip_mode=ip_mode,
            conflicted_ip_timeout=conflicted_ip_timeout,
            ipsec_lease_hold=ipsec_lease_hold,
            auto_configuration=auto_configuration,
            dhcp_settings_from_fortiipam=dhcp_settings_from_fortiipam,
            auto_managed_status=auto_managed_status,
            ddns_update=ddns_update,
            ddns_update_override=ddns_update_override,
            ddns_server_ip=ddns_server_ip,
            ddns_zone=ddns_zone,
            ddns_auth=ddns_auth,
            ddns_keyname=ddns_keyname,
            ddns_key=ddns_key,
            ddns_ttl=ddns_ttl,
            vci_match=vci_match,
            vci_string=vci_string,
            exclude_range=exclude_range,
            shared_subnet=shared_subnet,
            relay_agent=relay_agent,
            reserved_address=reserved_address,
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
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_id: int | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/dhcp/server object to a new position.
        
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
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.system_dhcp_server.move(
            ...     id=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.system_dhcp_server.move(
            ...     id=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.system_dhcp_server.move(
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
            all_objects = self.get(vdom=vdom)
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
        endpoint = "/system.dhcp/server/" + quote_path_param(id)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





