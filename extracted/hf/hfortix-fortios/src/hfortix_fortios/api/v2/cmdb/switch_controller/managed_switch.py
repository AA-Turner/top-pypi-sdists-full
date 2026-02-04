"""
FortiOS CMDB - Switch_controller managed_switch

Configuration endpoint for managing cmdb switch_controller/managed_switch objects.

API Endpoints:
    GET    /cmdb/switch_controller/managed_switch
    POST   /cmdb/switch_controller/managed_switch
    PUT    /cmdb/switch_controller/managed_switch/{identifier}
    DELETE /cmdb/switch_controller/managed_switch/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.switch_controller_managed_switch.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.switch_controller_managed_switch.post(
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

class ManagedSwitch(CRUDEndpoint, MetadataMixin):
    """ManagedSwitch Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "managed_switch"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "route_offload_router": {
            "mkey": "vlan-name",
            "required_fields": ['router-ip'],
            "example": "[{'router-ip': '192.168.1.10'}]",
        },
        "vlan": {
            "mkey": "vlan-name",
            "required_fields": ['assignment-priority'],
            "example": "[{'assignment-priority': 1}]",
        },
        "ports": {
            "mkey": "port-name",
            "required_fields": ['port-name'],
            "example": "[{'port-name': 'value'}]",
        },
        "ip_source_guard": {
            "mkey": "port",
            "required_fields": ['binding-entry'],
            "example": "[{'binding-entry': 'value'}]",
        },
        "stp_instance": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
        },
        "snmp_community": {
            "mkey": "id",
            "required_fields": ['id', 'name'],
            "example": "[{'id': 1, 'name': 'value'}]",
        },
        "snmp_user": {
            "mkey": "name",
            "required_fields": ['auth-pwd', 'priv-pwd'],
            "example": "[{'auth-pwd': 'value', 'priv-pwd': 'value'}]",
        },
        "remote_log": {
            "mkey": "name",
            "required_fields": ['name', 'server'],
            "example": "[{'name': 'value', 'server': '192.168.1.10'}]",
        },
        "mirror": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "static_mac": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
        },
        "custom_command": {
            "mkey": "command-entry",
            "required_fields": ['command-name'],
            "example": "[{'command-name': 'value'}]",
        },
        "dhcp_snooping_static_client": {
            "mkey": "name",
            "required_fields": ['vlan', 'ip', 'mac', 'port'],
            "example": "[{'vlan': 'value', 'ip': '192.168.1.10', 'mac': 'value', 'port': 443}]",
        },
        "router_vrf": {
            "mkey": "name",
            "required_fields": ['name', 'vrfid'],
            "example": "[{'name': 'value', 'vrfid': 1}]",
        },
        "system_interface": {
            "mkey": "name",
            "required_fields": ['ip', 'vlan', 'interface'],
            "example": "[{'ip': '192.168.1.10', 'vlan': 'value', 'interface': 'value'}]",
        },
        "router_static": {
            "mkey": "id",
            "required_fields": ['dst', 'gateway'],
            "example": "[{'dst': 'value', 'gateway': '192.168.1.10'}]",
        },
        "system_dhcp_server": {
            "mkey": "id",
            "required_fields": ['netmask', 'interface'],
            "example": "[{'netmask': 'value', 'interface': 'value'}]",
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
        """Initialize ManagedSwitch endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        switch_id: str | None = None,
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
        Retrieve switch_controller/managed_switch configuration.

        Configure FortiSwitch devices that are managed by this FortiGate.

        Args:
            switch_id: String identifier to retrieve specific object.
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
            >>> # Get all switch_controller/managed_switch objects
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific switch_controller/managed_switch by switch-id
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.get(switch_id=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.switch_controller_managed_switch.get_schema()

        See Also:
            - post(): Create new switch_controller/managed_switch object
            - put(): Update existing switch_controller/managed_switch object
            - delete(): Remove switch_controller/managed_switch object
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
        
        if switch_id:
            endpoint = "/switch-controller/managed-switch/" + quote_path_param(switch_id)
            unwrap_single = True
        else:
            endpoint = "/switch-controller/managed-switch"
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
            >>> schema = fgt.api.cmdb.switch_controller_managed_switch.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.switch_controller_managed_switch.get_schema(format="json-schema")
        
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
        switch_id: str | None = None,
        sn: str | None = None,
        description: str | None = None,
        switch_profile: str | None = None,
        access_profile: str | None = None,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = None,
        fsw_wan1_peer: str | None = None,
        fsw_wan1_admin: Literal["discovered", "disable", "enable"] | None = None,
        poe_pre_standard_detection: Literal["enable", "disable"] | None = None,
        dhcp_server_access_list: Literal["global", "enable", "disable"] | None = None,
        poe_detection_type: int | None = None,
        max_poe_budget: int | None = None,
        directly_connected: int | None = None,
        version: int | None = None,
        max_allowed_trunk_members: int | None = None,
        pre_provisioned: int | None = None,
        l3_discovered: int | None = None,
        mgmt_mode: int | None = None,
        tunnel_discovered: int | None = None,
        tdr_supported: str | None = None,
        dynamic_capability: str | None = None,
        switch_device_tag: str | None = None,
        switch_dhcp_opt43_key: str | None = None,
        mclag_igmp_snooping_aware: Literal["enable", "disable"] | None = None,
        dynamically_discovered: int | None = None,
        ptp_status: Literal["disable", "enable"] | None = None,
        ptp_profile: str | None = None,
        radius_nas_ip_override: Literal["disable", "enable"] | None = None,
        radius_nas_ip: str | None = None,
        route_offload: Literal["disable", "enable"] | None = None,
        route_offload_mclag: Literal["disable", "enable"] | None = None,
        route_offload_router: str | list[str] | list[dict[str, Any]] | None = None,
        vlan: str | list[str] | list[dict[str, Any]] | None = None,
        type: Literal["virtual", "physical"] | None = None,
        owner_vdom: str | None = None,
        flow_identity: str | None = None,
        staged_image_version: str | None = None,
        delayed_restart_trigger: int | None = None,
        firmware_provision: Literal["enable", "disable"] | None = None,
        firmware_provision_version: str | None = None,
        firmware_provision_latest: Literal["disable", "once"] | None = None,
        ports: str | list[str] | list[dict[str, Any]] | None = None,
        ip_source_guard: str | list[str] | list[dict[str, Any]] | None = None,
        stp_settings: str | None = None,
        stp_instance: str | list[str] | list[dict[str, Any]] | None = None,
        override_snmp_sysinfo: Literal["disable", "enable"] | None = None,
        snmp_sysinfo: str | None = None,
        override_snmp_trap_threshold: Literal["enable", "disable"] | None = None,
        snmp_trap_threshold: str | None = None,
        override_snmp_community: Literal["enable", "disable"] | None = None,
        snmp_community: str | list[str] | list[dict[str, Any]] | None = None,
        override_snmp_user: Literal["enable", "disable"] | None = None,
        snmp_user: str | list[str] | list[dict[str, Any]] | None = None,
        qos_drop_policy: Literal["taildrop", "random-early-detection"] | None = None,
        qos_red_probability: int | None = None,
        switch_log: str | None = None,
        remote_log: str | list[str] | list[dict[str, Any]] | None = None,
        storm_control: str | None = None,
        mirror: str | list[str] | list[dict[str, Any]] | None = None,
        static_mac: str | list[str] | list[dict[str, Any]] | None = None,
        custom_command: str | list[str] | list[dict[str, Any]] | None = None,
        dhcp_snooping_static_client: str | list[str] | list[dict[str, Any]] | None = None,
        igmp_snooping: str | None = None,
        x802_1X_settings: str | None = None,
        router_vrf: str | list[str] | list[dict[str, Any]] | None = None,
        system_interface: str | list[str] | list[dict[str, Any]] | None = None,
        router_static: str | list[str] | list[dict[str, Any]] | None = None,
        system_dhcp_server: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing switch_controller/managed_switch object.

        Configure FortiSwitch devices that are managed by this FortiGate.

        Args:
            payload_dict: Object data as dict. Must include switch-id (primary key).
            switch_id: Managed-switch name.
            sn: Managed-switch serial number.
            description: Description.
            switch_profile: FortiSwitch profile.
            access_profile: FortiSwitch access profile.
            purdue_level: Purdue Level of this FortiSwitch.
            fsw_wan1_peer: FortiSwitch WAN1 peer port.
            fsw_wan1_admin: FortiSwitch WAN1 admin status; enable to authorize the FortiSwitch as a managed switch.
            poe_pre_standard_detection: Enable/disable PoE pre-standard detection.
            dhcp_server_access_list: DHCP snooping server access list.
            poe_detection_type: PoE detection type for FortiSwitch.
            max_poe_budget: Max PoE budget for FortiSwitch.
            directly_connected: Directly connected FortiSwitch.
            version: FortiSwitch version.
            max_allowed_trunk_members: FortiSwitch maximum allowed trunk members.
            pre_provisioned: Pre-provisioned managed switch.
            l3_discovered: Layer 3 management discovered.
            mgmt_mode: FortiLink management mode.
            tunnel_discovered: SOCKS tunnel management discovered.
            tdr_supported: TDR supported.
            dynamic_capability: List of features this FortiSwitch supports (not configurable) that is sent to the FortiGate device for subsequent configuration initiated by the FortiGate device.
            switch_device_tag: User definable label/tag.
            switch_dhcp_opt43_key: DHCP option43 key.
            mclag_igmp_snooping_aware: Enable/disable MCLAG IGMP-snooping awareness.
            dynamically_discovered: Dynamically discovered FortiSwitch.
            ptp_status: Enable/disable PTP profile on this FortiSwitch.
            ptp_profile: PTP profile configuration.
            radius_nas_ip_override: Use locally defined NAS-IP.
            radius_nas_ip: NAS-IP address.
            route_offload: Enable/disable route offload on this FortiSwitch.
            route_offload_mclag: Enable/disable route offload MCLAG on this FortiSwitch.
            route_offload_router: Configure route offload MCLAG IP address.
                Default format: [{'router-ip': '192.168.1.10'}]
                Supported formats:
                  - Single string: "value" → [{'vlan-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'vlan-name': 'val1'}, ...]
                  - List of dicts: [{'router-ip': '192.168.1.10'}] (recommended)
            vlan: Configure VLAN assignment priority.
                Default format: [{'assignment-priority': 1}]
                Supported formats:
                  - Single string: "value" → [{'vlan-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'vlan-name': 'val1'}, ...]
                  - List of dicts: [{'assignment-priority': 1}] (recommended)
            type: Indication of switch type, physical or virtual.
            owner_vdom: VDOM which owner of port belongs to.
            flow_identity: Flow-tracking netflow ipfix switch identity in hex format(00000000-FFFFFFFF default=0).
            staged_image_version: Staged image version for FortiSwitch.
            delayed_restart_trigger: Delayed restart triggered for this FortiSwitch.
            firmware_provision: Enable/disable provisioning of firmware to FortiSwitches on join connection.
            firmware_provision_version: Firmware version to provision to this FortiSwitch on bootup (major.minor.build, i.e. 6.2.1234).
            firmware_provision_latest: Enable/disable one-time automatic provisioning of the latest firmware version.
            ports: Managed-switch port list.
                Default format: [{'port-name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'port-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'port-name': 'val1'}, ...]
                  - List of dicts: [{'port-name': 'value'}] (recommended)
            ip_source_guard: IP source guard.
                Default format: [{'binding-entry': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'port': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'port': 'val1'}, ...]
                  - List of dicts: [{'binding-entry': 'value'}] (recommended)
            stp_settings: Configuration method to edit Spanning Tree Protocol (STP) settings used to prevent bridge loops.
            stp_instance: Configuration method to edit Spanning Tree Protocol (STP) instances.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            override_snmp_sysinfo: Enable/disable overriding the global SNMP system information.
            snmp_sysinfo: Configuration method to edit Simple Network Management Protocol (SNMP) system info.
            override_snmp_trap_threshold: Enable/disable overriding the global SNMP trap threshold values.
            snmp_trap_threshold: Configuration method to edit Simple Network Management Protocol (SNMP) trap threshold values.
            override_snmp_community: Enable/disable overriding the global SNMP communities.
            snmp_community: Configuration method to edit Simple Network Management Protocol (SNMP) communities.
                Default format: [{'id': 1, 'name': 'value'}]
                Required format: List of dicts with keys: id, name
                  (String format not allowed due to multiple required fields)
            override_snmp_user: Enable/disable overriding the global SNMP users.
            snmp_user: Configuration method to edit Simple Network Management Protocol (SNMP) users.
                Default format: [{'auth-pwd': 'value', 'priv-pwd': 'value'}]
                Required format: List of dicts with keys: auth-pwd, priv-pwd
                  (String format not allowed due to multiple required fields)
            qos_drop_policy: Set QoS drop-policy.
            qos_red_probability: Set QoS RED/WRED drop probability.
            switch_log: Configuration method to edit FortiSwitch logging settings (logs are transferred to and inserted into the FortiGate event log).
            remote_log: Configure logging by FortiSwitch device to a remote syslog server.
                Default format: [{'name': 'value', 'server': '192.168.1.10'}]
                Required format: List of dicts with keys: name, server
                  (String format not allowed due to multiple required fields)
            storm_control: Configuration method to edit FortiSwitch storm control for measuring traffic activity using data rates to prevent traffic disruption.
            mirror: Configuration method to edit FortiSwitch packet mirror.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            static_mac: Configuration method to edit FortiSwitch Static and Sticky MAC.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            custom_command: Configuration method to edit FortiSwitch commands to be pushed to this FortiSwitch device upon rebooting the FortiGate switch controller or the FortiSwitch.
                Default format: [{'command-name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'command-entry': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'command-entry': 'val1'}, ...]
                  - List of dicts: [{'command-name': 'value'}] (recommended)
            dhcp_snooping_static_client: Configure FortiSwitch DHCP snooping static clients.
                Default format: [{'vlan': 'value', 'ip': '192.168.1.10', 'mac': 'value', 'port': 443}]
                Required format: List of dicts with keys: vlan, ip, mac, port
                  (String format not allowed due to multiple required fields)
            igmp_snooping: Configure FortiSwitch IGMP snooping global settings.
            x802_1X_settings: Configuration method to edit FortiSwitch 802.1X global settings.
            router_vrf: Configure VRF.
                Default format: [{'name': 'value', 'vrfid': 1}]
                Required format: List of dicts with keys: name, vrfid
                  (String format not allowed due to multiple required fields)
            system_interface: Configure system interface on FortiSwitch.
                Default format: [{'ip': '192.168.1.10', 'vlan': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: ip, vlan, interface
                  (String format not allowed due to multiple required fields)
            router_static: Configure static routes.
                Default format: [{'dst': 'value', 'gateway': '192.168.1.10'}]
                Required format: List of dicts with keys: dst, gateway
                  (String format not allowed due to multiple required fields)
            system_dhcp_server: Configure DHCP servers.
                Default format: [{'netmask': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: netmask, interface
                  (String format not allowed due to multiple required fields)
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If switch-id is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.put(
            ...     switch_id=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "switch-id": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if route_offload_router is not None:
            route_offload_router = normalize_table_field(
                route_offload_router,
                mkey="vlan-name",
                required_fields=['router-ip'],
                field_name="route_offload_router",
                example="[{'router-ip': '192.168.1.10'}]",
            )
        if vlan is not None:
            vlan = normalize_table_field(
                vlan,
                mkey="vlan-name",
                required_fields=['assignment-priority'],
                field_name="vlan",
                example="[{'assignment-priority': 1}]",
            )
        if ports is not None:
            ports = normalize_table_field(
                ports,
                mkey="port-name",
                required_fields=['port-name'],
                field_name="ports",
                example="[{'port-name': 'value'}]",
            )
        if ip_source_guard is not None:
            ip_source_guard = normalize_table_field(
                ip_source_guard,
                mkey="port",
                required_fields=['binding-entry'],
                field_name="ip_source_guard",
                example="[{'binding-entry': 'value'}]",
            )
        if stp_instance is not None:
            stp_instance = normalize_table_field(
                stp_instance,
                mkey="id",
                required_fields=['id'],
                field_name="stp_instance",
                example="[{'id': 1}]",
            )
        if snmp_community is not None:
            snmp_community = normalize_table_field(
                snmp_community,
                mkey="id",
                required_fields=['id', 'name'],
                field_name="snmp_community",
                example="[{'id': 1, 'name': 'value'}]",
            )
        if snmp_user is not None:
            snmp_user = normalize_table_field(
                snmp_user,
                mkey="name",
                required_fields=['auth-pwd', 'priv-pwd'],
                field_name="snmp_user",
                example="[{'auth-pwd': 'value', 'priv-pwd': 'value'}]",
            )
        if remote_log is not None:
            remote_log = normalize_table_field(
                remote_log,
                mkey="name",
                required_fields=['name', 'server'],
                field_name="remote_log",
                example="[{'name': 'value', 'server': '192.168.1.10'}]",
            )
        if mirror is not None:
            mirror = normalize_table_field(
                mirror,
                mkey="name",
                required_fields=['name'],
                field_name="mirror",
                example="[{'name': 'value'}]",
            )
        if static_mac is not None:
            static_mac = normalize_table_field(
                static_mac,
                mkey="id",
                required_fields=['id'],
                field_name="static_mac",
                example="[{'id': 1}]",
            )
        if custom_command is not None:
            custom_command = normalize_table_field(
                custom_command,
                mkey="command-entry",
                required_fields=['command-name'],
                field_name="custom_command",
                example="[{'command-name': 'value'}]",
            )
        if dhcp_snooping_static_client is not None:
            dhcp_snooping_static_client = normalize_table_field(
                dhcp_snooping_static_client,
                mkey="name",
                required_fields=['vlan', 'ip', 'mac', 'port'],
                field_name="dhcp_snooping_static_client",
                example="[{'vlan': 'value', 'ip': '192.168.1.10', 'mac': 'value', 'port': 443}]",
            )
        if router_vrf is not None:
            router_vrf = normalize_table_field(
                router_vrf,
                mkey="name",
                required_fields=['name', 'vrfid'],
                field_name="router_vrf",
                example="[{'name': 'value', 'vrfid': 1}]",
            )
        if system_interface is not None:
            system_interface = normalize_table_field(
                system_interface,
                mkey="name",
                required_fields=['ip', 'vlan', 'interface'],
                field_name="system_interface",
                example="[{'ip': '192.168.1.10', 'vlan': 'value', 'interface': 'value'}]",
            )
        if router_static is not None:
            router_static = normalize_table_field(
                router_static,
                mkey="id",
                required_fields=['dst', 'gateway'],
                field_name="router_static",
                example="[{'dst': 'value', 'gateway': '192.168.1.10'}]",
            )
        if system_dhcp_server is not None:
            system_dhcp_server = normalize_table_field(
                system_dhcp_server,
                mkey="id",
                required_fields=['netmask', 'interface'],
                field_name="system_dhcp_server",
                example="[{'netmask': 'value', 'interface': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            switch_id=switch_id,
            sn=sn,
            description=description,
            switch_profile=switch_profile,
            access_profile=access_profile,
            purdue_level=purdue_level,
            fsw_wan1_peer=fsw_wan1_peer,
            fsw_wan1_admin=fsw_wan1_admin,
            poe_pre_standard_detection=poe_pre_standard_detection,
            dhcp_server_access_list=dhcp_server_access_list,
            poe_detection_type=poe_detection_type,
            max_poe_budget=max_poe_budget,
            directly_connected=directly_connected,
            version=version,
            max_allowed_trunk_members=max_allowed_trunk_members,
            pre_provisioned=pre_provisioned,
            l3_discovered=l3_discovered,
            mgmt_mode=mgmt_mode,
            tunnel_discovered=tunnel_discovered,
            tdr_supported=tdr_supported,
            dynamic_capability=dynamic_capability,
            switch_device_tag=switch_device_tag,
            switch_dhcp_opt43_key=switch_dhcp_opt43_key,
            mclag_igmp_snooping_aware=mclag_igmp_snooping_aware,
            dynamically_discovered=dynamically_discovered,
            ptp_status=ptp_status,
            ptp_profile=ptp_profile,
            radius_nas_ip_override=radius_nas_ip_override,
            radius_nas_ip=radius_nas_ip,
            route_offload=route_offload,
            route_offload_mclag=route_offload_mclag,
            route_offload_router=route_offload_router,
            vlan=vlan,
            type=type,
            owner_vdom=owner_vdom,
            flow_identity=flow_identity,
            staged_image_version=staged_image_version,
            delayed_restart_trigger=delayed_restart_trigger,
            firmware_provision=firmware_provision,
            firmware_provision_version=firmware_provision_version,
            firmware_provision_latest=firmware_provision_latest,
            ports=ports,
            ip_source_guard=ip_source_guard,
            stp_settings=stp_settings,
            stp_instance=stp_instance,
            override_snmp_sysinfo=override_snmp_sysinfo,
            snmp_sysinfo=snmp_sysinfo,
            override_snmp_trap_threshold=override_snmp_trap_threshold,
            snmp_trap_threshold=snmp_trap_threshold,
            override_snmp_community=override_snmp_community,
            snmp_community=snmp_community,
            override_snmp_user=override_snmp_user,
            snmp_user=snmp_user,
            qos_drop_policy=qos_drop_policy,
            qos_red_probability=qos_red_probability,
            switch_log=switch_log,
            remote_log=remote_log,
            storm_control=storm_control,
            mirror=mirror,
            static_mac=static_mac,
            custom_command=custom_command,
            dhcp_snooping_static_client=dhcp_snooping_static_client,
            igmp_snooping=igmp_snooping,
            x802_1X_settings=x802_1X_settings,
            router_vrf=router_vrf,
            system_interface=system_interface,
            router_static=router_static,
            system_dhcp_server=system_dhcp_server,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.managed_switch import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/switch_controller/managed_switch",
            )
        
        switch_id_value = payload_data.get("switch-id")
        if not switch_id_value:
            raise ValueError("switch-id is required for PUT")
        endpoint = "/switch-controller/managed-switch/" + quote_path_param(switch_id_value)

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
        switch_id: str | None = None,
        sn: str | None = None,
        description: str | None = None,
        switch_profile: str | None = None,
        access_profile: str | None = None,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = None,
        fsw_wan1_peer: str | None = None,
        fsw_wan1_admin: Literal["discovered", "disable", "enable"] | None = None,
        poe_pre_standard_detection: Literal["enable", "disable"] | None = None,
        dhcp_server_access_list: Literal["global", "enable", "disable"] | None = None,
        poe_detection_type: int | None = None,
        max_poe_budget: int | None = None,
        directly_connected: int | None = None,
        version: int | None = None,
        max_allowed_trunk_members: int | None = None,
        pre_provisioned: int | None = None,
        l3_discovered: int | None = None,
        mgmt_mode: int | None = None,
        tunnel_discovered: int | None = None,
        tdr_supported: str | None = None,
        dynamic_capability: str | None = None,
        switch_device_tag: str | None = None,
        switch_dhcp_opt43_key: str | None = None,
        mclag_igmp_snooping_aware: Literal["enable", "disable"] | None = None,
        dynamically_discovered: int | None = None,
        ptp_status: Literal["disable", "enable"] | None = None,
        ptp_profile: str | None = None,
        radius_nas_ip_override: Literal["disable", "enable"] | None = None,
        radius_nas_ip: str | None = None,
        route_offload: Literal["disable", "enable"] | None = None,
        route_offload_mclag: Literal["disable", "enable"] | None = None,
        route_offload_router: str | list[str] | list[dict[str, Any]] | None = None,
        vlan: str | list[str] | list[dict[str, Any]] | None = None,
        type: Literal["virtual", "physical"] | None = None,
        owner_vdom: str | None = None,
        flow_identity: str | None = None,
        staged_image_version: str | None = None,
        delayed_restart_trigger: int | None = None,
        firmware_provision: Literal["enable", "disable"] | None = None,
        firmware_provision_version: str | None = None,
        firmware_provision_latest: Literal["disable", "once"] | None = None,
        ports: str | list[str] | list[dict[str, Any]] | None = None,
        ip_source_guard: str | list[str] | list[dict[str, Any]] | None = None,
        stp_settings: str | None = None,
        stp_instance: str | list[str] | list[dict[str, Any]] | None = None,
        override_snmp_sysinfo: Literal["disable", "enable"] | None = None,
        snmp_sysinfo: str | None = None,
        override_snmp_trap_threshold: Literal["enable", "disable"] | None = None,
        snmp_trap_threshold: str | None = None,
        override_snmp_community: Literal["enable", "disable"] | None = None,
        snmp_community: str | list[str] | list[dict[str, Any]] | None = None,
        override_snmp_user: Literal["enable", "disable"] | None = None,
        snmp_user: str | list[str] | list[dict[str, Any]] | None = None,
        qos_drop_policy: Literal["taildrop", "random-early-detection"] | None = None,
        qos_red_probability: int | None = None,
        switch_log: str | None = None,
        remote_log: str | list[str] | list[dict[str, Any]] | None = None,
        storm_control: str | None = None,
        mirror: str | list[str] | list[dict[str, Any]] | None = None,
        static_mac: str | list[str] | list[dict[str, Any]] | None = None,
        custom_command: str | list[str] | list[dict[str, Any]] | None = None,
        dhcp_snooping_static_client: str | list[str] | list[dict[str, Any]] | None = None,
        igmp_snooping: str | None = None,
        x802_1X_settings: str | None = None,
        router_vrf: str | list[str] | list[dict[str, Any]] | None = None,
        system_interface: str | list[str] | list[dict[str, Any]] | None = None,
        router_static: str | list[str] | list[dict[str, Any]] | None = None,
        system_dhcp_server: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new switch_controller/managed_switch object.

        Configure FortiSwitch devices that are managed by this FortiGate.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            switch_id: Managed-switch name.
            sn: Managed-switch serial number.
            description: Description.
            switch_profile: FortiSwitch profile.
            access_profile: FortiSwitch access profile.
            purdue_level: Purdue Level of this FortiSwitch.
            fsw_wan1_peer: FortiSwitch WAN1 peer port.
            fsw_wan1_admin: FortiSwitch WAN1 admin status; enable to authorize the FortiSwitch as a managed switch.
            poe_pre_standard_detection: Enable/disable PoE pre-standard detection.
            dhcp_server_access_list: DHCP snooping server access list.
            poe_detection_type: PoE detection type for FortiSwitch.
            max_poe_budget: Max PoE budget for FortiSwitch.
            directly_connected: Directly connected FortiSwitch.
            version: FortiSwitch version.
            max_allowed_trunk_members: FortiSwitch maximum allowed trunk members.
            pre_provisioned: Pre-provisioned managed switch.
            l3_discovered: Layer 3 management discovered.
            mgmt_mode: FortiLink management mode.
            tunnel_discovered: SOCKS tunnel management discovered.
            tdr_supported: TDR supported.
            dynamic_capability: List of features this FortiSwitch supports (not configurable) that is sent to the FortiGate device for subsequent configuration initiated by the FortiGate device.
            switch_device_tag: User definable label/tag.
            switch_dhcp_opt43_key: DHCP option43 key.
            mclag_igmp_snooping_aware: Enable/disable MCLAG IGMP-snooping awareness.
            dynamically_discovered: Dynamically discovered FortiSwitch.
            ptp_status: Enable/disable PTP profile on this FortiSwitch.
            ptp_profile: PTP profile configuration.
            radius_nas_ip_override: Use locally defined NAS-IP.
            radius_nas_ip: NAS-IP address.
            route_offload: Enable/disable route offload on this FortiSwitch.
            route_offload_mclag: Enable/disable route offload MCLAG on this FortiSwitch.
            route_offload_router: Configure route offload MCLAG IP address.
                Default format: [{'router-ip': '192.168.1.10'}]
                Supported formats:
                  - Single string: "value" → [{'vlan-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'vlan-name': 'val1'}, ...]
                  - List of dicts: [{'router-ip': '192.168.1.10'}] (recommended)
            vlan: Configure VLAN assignment priority.
                Default format: [{'assignment-priority': 1}]
                Supported formats:
                  - Single string: "value" → [{'vlan-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'vlan-name': 'val1'}, ...]
                  - List of dicts: [{'assignment-priority': 1}] (recommended)
            type: Indication of switch type, physical or virtual.
            owner_vdom: VDOM which owner of port belongs to.
            flow_identity: Flow-tracking netflow ipfix switch identity in hex format(00000000-FFFFFFFF default=0).
            staged_image_version: Staged image version for FortiSwitch.
            delayed_restart_trigger: Delayed restart triggered for this FortiSwitch.
            firmware_provision: Enable/disable provisioning of firmware to FortiSwitches on join connection.
            firmware_provision_version: Firmware version to provision to this FortiSwitch on bootup (major.minor.build, i.e. 6.2.1234).
            firmware_provision_latest: Enable/disable one-time automatic provisioning of the latest firmware version.
            ports: Managed-switch port list.
                Default format: [{'port-name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'port-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'port-name': 'val1'}, ...]
                  - List of dicts: [{'port-name': 'value'}] (recommended)
            ip_source_guard: IP source guard.
                Default format: [{'binding-entry': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'port': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'port': 'val1'}, ...]
                  - List of dicts: [{'binding-entry': 'value'}] (recommended)
            stp_settings: Configuration method to edit Spanning Tree Protocol (STP) settings used to prevent bridge loops.
            stp_instance: Configuration method to edit Spanning Tree Protocol (STP) instances.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            override_snmp_sysinfo: Enable/disable overriding the global SNMP system information.
            snmp_sysinfo: Configuration method to edit Simple Network Management Protocol (SNMP) system info.
            override_snmp_trap_threshold: Enable/disable overriding the global SNMP trap threshold values.
            snmp_trap_threshold: Configuration method to edit Simple Network Management Protocol (SNMP) trap threshold values.
            override_snmp_community: Enable/disable overriding the global SNMP communities.
            snmp_community: Configuration method to edit Simple Network Management Protocol (SNMP) communities.
                Default format: [{'id': 1, 'name': 'value'}]
                Required format: List of dicts with keys: id, name
                  (String format not allowed due to multiple required fields)
            override_snmp_user: Enable/disable overriding the global SNMP users.
            snmp_user: Configuration method to edit Simple Network Management Protocol (SNMP) users.
                Default format: [{'auth-pwd': 'value', 'priv-pwd': 'value'}]
                Required format: List of dicts with keys: auth-pwd, priv-pwd
                  (String format not allowed due to multiple required fields)
            qos_drop_policy: Set QoS drop-policy.
            qos_red_probability: Set QoS RED/WRED drop probability.
            switch_log: Configuration method to edit FortiSwitch logging settings (logs are transferred to and inserted into the FortiGate event log).
            remote_log: Configure logging by FortiSwitch device to a remote syslog server.
                Default format: [{'name': 'value', 'server': '192.168.1.10'}]
                Required format: List of dicts with keys: name, server
                  (String format not allowed due to multiple required fields)
            storm_control: Configuration method to edit FortiSwitch storm control for measuring traffic activity using data rates to prevent traffic disruption.
            mirror: Configuration method to edit FortiSwitch packet mirror.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            static_mac: Configuration method to edit FortiSwitch Static and Sticky MAC.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            custom_command: Configuration method to edit FortiSwitch commands to be pushed to this FortiSwitch device upon rebooting the FortiGate switch controller or the FortiSwitch.
                Default format: [{'command-name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'command-entry': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'command-entry': 'val1'}, ...]
                  - List of dicts: [{'command-name': 'value'}] (recommended)
            dhcp_snooping_static_client: Configure FortiSwitch DHCP snooping static clients.
                Default format: [{'vlan': 'value', 'ip': '192.168.1.10', 'mac': 'value', 'port': 443}]
                Required format: List of dicts with keys: vlan, ip, mac, port
                  (String format not allowed due to multiple required fields)
            igmp_snooping: Configure FortiSwitch IGMP snooping global settings.
            x802_1X_settings: Configuration method to edit FortiSwitch 802.1X global settings.
            router_vrf: Configure VRF.
                Default format: [{'name': 'value', 'vrfid': 1}]
                Required format: List of dicts with keys: name, vrfid
                  (String format not allowed due to multiple required fields)
            system_interface: Configure system interface on FortiSwitch.
                Default format: [{'ip': '192.168.1.10', 'vlan': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: ip, vlan, interface
                  (String format not allowed due to multiple required fields)
            router_static: Configure static routes.
                Default format: [{'dst': 'value', 'gateway': '192.168.1.10'}]
                Required format: List of dicts with keys: dst, gateway
                  (String format not allowed due to multiple required fields)
            system_dhcp_server: Configure DHCP servers.
                Default format: [{'netmask': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: netmask, interface
                  (String format not allowed due to multiple required fields)
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created switch-id: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = ManagedSwitch.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(ManagedSwitch.required_fields()) }}
            
            Use ManagedSwitch.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if route_offload_router is not None:
            route_offload_router = normalize_table_field(
                route_offload_router,
                mkey="vlan-name",
                required_fields=['router-ip'],
                field_name="route_offload_router",
                example="[{'router-ip': '192.168.1.10'}]",
            )
        if vlan is not None:
            vlan = normalize_table_field(
                vlan,
                mkey="vlan-name",
                required_fields=['assignment-priority'],
                field_name="vlan",
                example="[{'assignment-priority': 1}]",
            )
        if ports is not None:
            ports = normalize_table_field(
                ports,
                mkey="port-name",
                required_fields=['port-name'],
                field_name="ports",
                example="[{'port-name': 'value'}]",
            )
        if ip_source_guard is not None:
            ip_source_guard = normalize_table_field(
                ip_source_guard,
                mkey="port",
                required_fields=['binding-entry'],
                field_name="ip_source_guard",
                example="[{'binding-entry': 'value'}]",
            )
        if stp_instance is not None:
            stp_instance = normalize_table_field(
                stp_instance,
                mkey="id",
                required_fields=['id'],
                field_name="stp_instance",
                example="[{'id': 1}]",
            )
        if snmp_community is not None:
            snmp_community = normalize_table_field(
                snmp_community,
                mkey="id",
                required_fields=['id', 'name'],
                field_name="snmp_community",
                example="[{'id': 1, 'name': 'value'}]",
            )
        if snmp_user is not None:
            snmp_user = normalize_table_field(
                snmp_user,
                mkey="name",
                required_fields=['auth-pwd', 'priv-pwd'],
                field_name="snmp_user",
                example="[{'auth-pwd': 'value', 'priv-pwd': 'value'}]",
            )
        if remote_log is not None:
            remote_log = normalize_table_field(
                remote_log,
                mkey="name",
                required_fields=['name', 'server'],
                field_name="remote_log",
                example="[{'name': 'value', 'server': '192.168.1.10'}]",
            )
        if mirror is not None:
            mirror = normalize_table_field(
                mirror,
                mkey="name",
                required_fields=['name'],
                field_name="mirror",
                example="[{'name': 'value'}]",
            )
        if static_mac is not None:
            static_mac = normalize_table_field(
                static_mac,
                mkey="id",
                required_fields=['id'],
                field_name="static_mac",
                example="[{'id': 1}]",
            )
        if custom_command is not None:
            custom_command = normalize_table_field(
                custom_command,
                mkey="command-entry",
                required_fields=['command-name'],
                field_name="custom_command",
                example="[{'command-name': 'value'}]",
            )
        if dhcp_snooping_static_client is not None:
            dhcp_snooping_static_client = normalize_table_field(
                dhcp_snooping_static_client,
                mkey="name",
                required_fields=['vlan', 'ip', 'mac', 'port'],
                field_name="dhcp_snooping_static_client",
                example="[{'vlan': 'value', 'ip': '192.168.1.10', 'mac': 'value', 'port': 443}]",
            )
        if router_vrf is not None:
            router_vrf = normalize_table_field(
                router_vrf,
                mkey="name",
                required_fields=['name', 'vrfid'],
                field_name="router_vrf",
                example="[{'name': 'value', 'vrfid': 1}]",
            )
        if system_interface is not None:
            system_interface = normalize_table_field(
                system_interface,
                mkey="name",
                required_fields=['ip', 'vlan', 'interface'],
                field_name="system_interface",
                example="[{'ip': '192.168.1.10', 'vlan': 'value', 'interface': 'value'}]",
            )
        if router_static is not None:
            router_static = normalize_table_field(
                router_static,
                mkey="id",
                required_fields=['dst', 'gateway'],
                field_name="router_static",
                example="[{'dst': 'value', 'gateway': '192.168.1.10'}]",
            )
        if system_dhcp_server is not None:
            system_dhcp_server = normalize_table_field(
                system_dhcp_server,
                mkey="id",
                required_fields=['netmask', 'interface'],
                field_name="system_dhcp_server",
                example="[{'netmask': 'value', 'interface': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            switch_id=switch_id,
            sn=sn,
            description=description,
            switch_profile=switch_profile,
            access_profile=access_profile,
            purdue_level=purdue_level,
            fsw_wan1_peer=fsw_wan1_peer,
            fsw_wan1_admin=fsw_wan1_admin,
            poe_pre_standard_detection=poe_pre_standard_detection,
            dhcp_server_access_list=dhcp_server_access_list,
            poe_detection_type=poe_detection_type,
            max_poe_budget=max_poe_budget,
            directly_connected=directly_connected,
            version=version,
            max_allowed_trunk_members=max_allowed_trunk_members,
            pre_provisioned=pre_provisioned,
            l3_discovered=l3_discovered,
            mgmt_mode=mgmt_mode,
            tunnel_discovered=tunnel_discovered,
            tdr_supported=tdr_supported,
            dynamic_capability=dynamic_capability,
            switch_device_tag=switch_device_tag,
            switch_dhcp_opt43_key=switch_dhcp_opt43_key,
            mclag_igmp_snooping_aware=mclag_igmp_snooping_aware,
            dynamically_discovered=dynamically_discovered,
            ptp_status=ptp_status,
            ptp_profile=ptp_profile,
            radius_nas_ip_override=radius_nas_ip_override,
            radius_nas_ip=radius_nas_ip,
            route_offload=route_offload,
            route_offload_mclag=route_offload_mclag,
            route_offload_router=route_offload_router,
            vlan=vlan,
            type=type,
            owner_vdom=owner_vdom,
            flow_identity=flow_identity,
            staged_image_version=staged_image_version,
            delayed_restart_trigger=delayed_restart_trigger,
            firmware_provision=firmware_provision,
            firmware_provision_version=firmware_provision_version,
            firmware_provision_latest=firmware_provision_latest,
            ports=ports,
            ip_source_guard=ip_source_guard,
            stp_settings=stp_settings,
            stp_instance=stp_instance,
            override_snmp_sysinfo=override_snmp_sysinfo,
            snmp_sysinfo=snmp_sysinfo,
            override_snmp_trap_threshold=override_snmp_trap_threshold,
            snmp_trap_threshold=snmp_trap_threshold,
            override_snmp_community=override_snmp_community,
            snmp_community=snmp_community,
            override_snmp_user=override_snmp_user,
            snmp_user=snmp_user,
            qos_drop_policy=qos_drop_policy,
            qos_red_probability=qos_red_probability,
            switch_log=switch_log,
            remote_log=remote_log,
            storm_control=storm_control,
            mirror=mirror,
            static_mac=static_mac,
            custom_command=custom_command,
            dhcp_snooping_static_client=dhcp_snooping_static_client,
            igmp_snooping=igmp_snooping,
            x802_1X_settings=x802_1X_settings,
            router_vrf=router_vrf,
            system_interface=system_interface,
            router_static=router_static,
            system_dhcp_server=system_dhcp_server,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.managed_switch import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/switch_controller/managed_switch",
            )

        endpoint = "/switch-controller/managed-switch"
        
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
        switch_id: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete switch_controller/managed_switch object.

        Configure FortiSwitch devices that are managed by this FortiGate.

        Args:
            switch_id: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If switch-id is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.delete(switch_id=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not switch_id:
            raise ValueError("switch-id is required for DELETE")
        endpoint = "/switch-controller/managed-switch/" + quote_path_param(switch_id)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        switch_id: str,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if switch_controller/managed_switch object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            switch_id: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.switch_controller_managed_switch.exists(switch_id=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.switch_controller_managed_switch.exists(switch_id=1):
            ...     fgt.api.cmdb.switch_controller_managed_switch.delete(switch_id=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/switch-controller/managed-switch"
        endpoint = f"{endpoint}/{quote_path_param(switch_id)}"
        
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
        switch_id: str | None = None,
        sn: str | None = None,
        description: str | None = None,
        switch_profile: str | None = None,
        access_profile: str | None = None,
        purdue_level: Literal["1", "1.5", "2", "2.5", "3", "3.5", "4", "5", "5.5"] | None = None,
        fsw_wan1_peer: str | None = None,
        fsw_wan1_admin: Literal["discovered", "disable", "enable"] | None = None,
        poe_pre_standard_detection: Literal["enable", "disable"] | None = None,
        dhcp_server_access_list: Literal["global", "enable", "disable"] | None = None,
        poe_detection_type: int | None = None,
        max_poe_budget: int | None = None,
        directly_connected: int | None = None,
        version: int | None = None,
        max_allowed_trunk_members: int | None = None,
        pre_provisioned: int | None = None,
        l3_discovered: int | None = None,
        mgmt_mode: int | None = None,
        tunnel_discovered: int | None = None,
        tdr_supported: str | None = None,
        dynamic_capability: str | None = None,
        switch_device_tag: str | None = None,
        switch_dhcp_opt43_key: str | None = None,
        mclag_igmp_snooping_aware: Literal["enable", "disable"] | None = None,
        dynamically_discovered: int | None = None,
        ptp_status: Literal["disable", "enable"] | None = None,
        ptp_profile: str | None = None,
        radius_nas_ip_override: Literal["disable", "enable"] | None = None,
        radius_nas_ip: str | None = None,
        route_offload: Literal["disable", "enable"] | None = None,
        route_offload_mclag: Literal["disable", "enable"] | None = None,
        route_offload_router: str | list[str] | list[dict[str, Any]] | None = None,
        vlan: str | list[str] | list[dict[str, Any]] | None = None,
        type: Literal["virtual", "physical"] | None = None,
        owner_vdom: str | None = None,
        flow_identity: str | None = None,
        staged_image_version: str | None = None,
        delayed_restart_trigger: int | None = None,
        firmware_provision: Literal["enable", "disable"] | None = None,
        firmware_provision_version: str | None = None,
        firmware_provision_latest: Literal["disable", "once"] | None = None,
        ports: str | list[str] | list[dict[str, Any]] | None = None,
        ip_source_guard: str | list[str] | list[dict[str, Any]] | None = None,
        stp_settings: str | None = None,
        stp_instance: str | list[str] | list[dict[str, Any]] | None = None,
        override_snmp_sysinfo: Literal["disable", "enable"] | None = None,
        snmp_sysinfo: str | None = None,
        override_snmp_trap_threshold: Literal["enable", "disable"] | None = None,
        snmp_trap_threshold: str | None = None,
        override_snmp_community: Literal["enable", "disable"] | None = None,
        snmp_community: str | list[str] | list[dict[str, Any]] | None = None,
        override_snmp_user: Literal["enable", "disable"] | None = None,
        snmp_user: str | list[str] | list[dict[str, Any]] | None = None,
        qos_drop_policy: Literal["taildrop", "random-early-detection"] | None = None,
        qos_red_probability: int | None = None,
        switch_log: str | None = None,
        remote_log: str | list[str] | list[dict[str, Any]] | None = None,
        storm_control: str | None = None,
        mirror: str | list[str] | list[dict[str, Any]] | None = None,
        static_mac: str | list[str] | list[dict[str, Any]] | None = None,
        custom_command: str | list[str] | list[dict[str, Any]] | None = None,
        dhcp_snooping_static_client: str | list[str] | list[dict[str, Any]] | None = None,
        igmp_snooping: str | None = None,
        x802_1X_settings: str | None = None,
        router_vrf: str | list[str] | list[dict[str, Any]] | None = None,
        system_interface: str | list[str] | list[dict[str, Any]] | None = None,
        router_static: str | list[str] | list[dict[str, Any]] | None = None,
        system_dhcp_server: str | list[str] | list[dict[str, Any]] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update switch_controller/managed_switch object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (switch-id) in the payload.

        Args:
            payload_dict: Resource data including switch-id (primary key)
            switch_id: Field switch-id
            sn: Field sn
            description: Field description
            switch_profile: Field switch-profile
            access_profile: Field access-profile
            purdue_level: Field purdue-level
            fsw_wan1_peer: Field fsw-wan1-peer
            fsw_wan1_admin: Field fsw-wan1-admin
            poe_pre_standard_detection: Field poe-pre-standard-detection
            dhcp_server_access_list: Field dhcp-server-access-list
            poe_detection_type: Field poe-detection-type
            max_poe_budget: Field max-poe-budget
            directly_connected: Field directly-connected
            version: Field version
            max_allowed_trunk_members: Field max-allowed-trunk-members
            pre_provisioned: Field pre-provisioned
            l3_discovered: Field l3-discovered
            mgmt_mode: Field mgmt-mode
            tunnel_discovered: Field tunnel-discovered
            tdr_supported: Field tdr-supported
            dynamic_capability: Field dynamic-capability
            switch_device_tag: Field switch-device-tag
            switch_dhcp_opt43_key: Field switch-dhcp_opt43_key
            mclag_igmp_snooping_aware: Field mclag-igmp-snooping-aware
            dynamically_discovered: Field dynamically-discovered
            ptp_status: Field ptp-status
            ptp_profile: Field ptp-profile
            radius_nas_ip_override: Field radius-nas-ip-override
            radius_nas_ip: Field radius-nas-ip
            route_offload: Field route-offload
            route_offload_mclag: Field route-offload-mclag
            route_offload_router: Field route-offload-router
            vlan: Field vlan
            type: Field type
            owner_vdom: Field owner-vdom
            flow_identity: Field flow-identity
            staged_image_version: Field staged-image-version
            delayed_restart_trigger: Field delayed-restart-trigger
            firmware_provision: Field firmware-provision
            firmware_provision_version: Field firmware-provision-version
            firmware_provision_latest: Field firmware-provision-latest
            ports: Field ports
            ip_source_guard: Field ip-source-guard
            stp_settings: Field stp-settings
            stp_instance: Field stp-instance
            override_snmp_sysinfo: Field override-snmp-sysinfo
            snmp_sysinfo: Field snmp-sysinfo
            override_snmp_trap_threshold: Field override-snmp-trap-threshold
            snmp_trap_threshold: Field snmp-trap-threshold
            override_snmp_community: Field override-snmp-community
            snmp_community: Field snmp-community
            override_snmp_user: Field override-snmp-user
            snmp_user: Field snmp-user
            qos_drop_policy: Field qos-drop-policy
            qos_red_probability: Field qos-red-probability
            switch_log: Field switch-log
            remote_log: Field remote-log
            storm_control: Field storm-control
            mirror: Field mirror
            static_mac: Field static-mac
            custom_command: Field custom-command
            dhcp_snooping_static_client: Field dhcp-snooping-static-client
            igmp_snooping: Field igmp-snooping
            x802_1X_settings: Field 802-1X-settings
            router_vrf: Field router-vrf
            system_interface: Field system-interface
            router_static: Field router-static
            system_dhcp_server: Field system-dhcp-server
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If switch-id is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.set(
            ...     switch_id=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "switch-id": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.switch_controller_managed_switch.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.switch_controller_managed_switch.set(payload_dict=obj_data)
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
        if route_offload_router is not None:
            route_offload_router = normalize_table_field(
                route_offload_router,
                mkey="vlan-name",
                required_fields=['router-ip'],
                field_name="route_offload_router",
                example="[{'router-ip': '192.168.1.10'}]",
            )
        if vlan is not None:
            vlan = normalize_table_field(
                vlan,
                mkey="vlan-name",
                required_fields=['assignment-priority'],
                field_name="vlan",
                example="[{'assignment-priority': 1}]",
            )
        if ports is not None:
            ports = normalize_table_field(
                ports,
                mkey="port-name",
                required_fields=['port-name'],
                field_name="ports",
                example="[{'port-name': 'value'}]",
            )
        if ip_source_guard is not None:
            ip_source_guard = normalize_table_field(
                ip_source_guard,
                mkey="port",
                required_fields=['binding-entry'],
                field_name="ip_source_guard",
                example="[{'binding-entry': 'value'}]",
            )
        if stp_instance is not None:
            stp_instance = normalize_table_field(
                stp_instance,
                mkey="id",
                required_fields=['id'],
                field_name="stp_instance",
                example="[{'id': 1}]",
            )
        if snmp_community is not None:
            snmp_community = normalize_table_field(
                snmp_community,
                mkey="id",
                required_fields=['id', 'name'],
                field_name="snmp_community",
                example="[{'id': 1, 'name': 'value'}]",
            )
        if snmp_user is not None:
            snmp_user = normalize_table_field(
                snmp_user,
                mkey="name",
                required_fields=['auth-pwd', 'priv-pwd'],
                field_name="snmp_user",
                example="[{'auth-pwd': 'value', 'priv-pwd': 'value'}]",
            )
        if remote_log is not None:
            remote_log = normalize_table_field(
                remote_log,
                mkey="name",
                required_fields=['name', 'server'],
                field_name="remote_log",
                example="[{'name': 'value', 'server': '192.168.1.10'}]",
            )
        if mirror is not None:
            mirror = normalize_table_field(
                mirror,
                mkey="name",
                required_fields=['name'],
                field_name="mirror",
                example="[{'name': 'value'}]",
            )
        if static_mac is not None:
            static_mac = normalize_table_field(
                static_mac,
                mkey="id",
                required_fields=['id'],
                field_name="static_mac",
                example="[{'id': 1}]",
            )
        if custom_command is not None:
            custom_command = normalize_table_field(
                custom_command,
                mkey="command-entry",
                required_fields=['command-name'],
                field_name="custom_command",
                example="[{'command-name': 'value'}]",
            )
        if dhcp_snooping_static_client is not None:
            dhcp_snooping_static_client = normalize_table_field(
                dhcp_snooping_static_client,
                mkey="name",
                required_fields=['vlan', 'ip', 'mac', 'port'],
                field_name="dhcp_snooping_static_client",
                example="[{'vlan': 'value', 'ip': '192.168.1.10', 'mac': 'value', 'port': 443}]",
            )
        if router_vrf is not None:
            router_vrf = normalize_table_field(
                router_vrf,
                mkey="name",
                required_fields=['name', 'vrfid'],
                field_name="router_vrf",
                example="[{'name': 'value', 'vrfid': 1}]",
            )
        if system_interface is not None:
            system_interface = normalize_table_field(
                system_interface,
                mkey="name",
                required_fields=['ip', 'vlan', 'interface'],
                field_name="system_interface",
                example="[{'ip': '192.168.1.10', 'vlan': 'value', 'interface': 'value'}]",
            )
        if router_static is not None:
            router_static = normalize_table_field(
                router_static,
                mkey="id",
                required_fields=['dst', 'gateway'],
                field_name="router_static",
                example="[{'dst': 'value', 'gateway': '192.168.1.10'}]",
            )
        if system_dhcp_server is not None:
            system_dhcp_server = normalize_table_field(
                system_dhcp_server,
                mkey="id",
                required_fields=['netmask', 'interface'],
                field_name="system_dhcp_server",
                example="[{'netmask': 'value', 'interface': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            switch_id=switch_id,
            sn=sn,
            description=description,
            switch_profile=switch_profile,
            access_profile=access_profile,
            purdue_level=purdue_level,
            fsw_wan1_peer=fsw_wan1_peer,
            fsw_wan1_admin=fsw_wan1_admin,
            poe_pre_standard_detection=poe_pre_standard_detection,
            dhcp_server_access_list=dhcp_server_access_list,
            poe_detection_type=poe_detection_type,
            max_poe_budget=max_poe_budget,
            directly_connected=directly_connected,
            version=version,
            max_allowed_trunk_members=max_allowed_trunk_members,
            pre_provisioned=pre_provisioned,
            l3_discovered=l3_discovered,
            mgmt_mode=mgmt_mode,
            tunnel_discovered=tunnel_discovered,
            tdr_supported=tdr_supported,
            dynamic_capability=dynamic_capability,
            switch_device_tag=switch_device_tag,
            switch_dhcp_opt43_key=switch_dhcp_opt43_key,
            mclag_igmp_snooping_aware=mclag_igmp_snooping_aware,
            dynamically_discovered=dynamically_discovered,
            ptp_status=ptp_status,
            ptp_profile=ptp_profile,
            radius_nas_ip_override=radius_nas_ip_override,
            radius_nas_ip=radius_nas_ip,
            route_offload=route_offload,
            route_offload_mclag=route_offload_mclag,
            route_offload_router=route_offload_router,
            vlan=vlan,
            type=type,
            owner_vdom=owner_vdom,
            flow_identity=flow_identity,
            staged_image_version=staged_image_version,
            delayed_restart_trigger=delayed_restart_trigger,
            firmware_provision=firmware_provision,
            firmware_provision_version=firmware_provision_version,
            firmware_provision_latest=firmware_provision_latest,
            ports=ports,
            ip_source_guard=ip_source_guard,
            stp_settings=stp_settings,
            stp_instance=stp_instance,
            override_snmp_sysinfo=override_snmp_sysinfo,
            snmp_sysinfo=snmp_sysinfo,
            override_snmp_trap_threshold=override_snmp_trap_threshold,
            snmp_trap_threshold=snmp_trap_threshold,
            override_snmp_community=override_snmp_community,
            snmp_community=snmp_community,
            override_snmp_user=override_snmp_user,
            snmp_user=snmp_user,
            qos_drop_policy=qos_drop_policy,
            qos_red_probability=qos_red_probability,
            switch_log=switch_log,
            remote_log=remote_log,
            storm_control=storm_control,
            mirror=mirror,
            static_mac=static_mac,
            custom_command=custom_command,
            dhcp_snooping_static_client=dhcp_snooping_static_client,
            igmp_snooping=igmp_snooping,
            x802_1X_settings=x802_1X_settings,
            router_vrf=router_vrf,
            system_interface=system_interface,
            router_static=router_static,
            system_dhcp_server=system_dhcp_server,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("switch-id")
        if not mkey_value:
            raise ValueError("switch-id is required for set()")
        
        # Check if resource exists
        if self.exists(switch_id=mkey_value, vdom=vdom):
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
        switch_id: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_switch_id: str | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move switch_controller/managed_switch object to a new position.
        
        Reorders objects by moving one before/after another, to top/bottom, or to a specific position.
        
        Args:
            switch_id: Identifier of object to move
            position: Where to move the object:
                - "before": Move before reference object (requires reference_switch_id)
                - "after": Move after reference object (requires reference_switch_id)
                - "top": Move to first position (reference not needed)
                - "bottom": Move to last position (reference not needed)
                - int (1-based): Move to specific position number (e.g., position=3 for 3rd place)
            reference_switch_id: Identifier of reference object (required for before/after)
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.switch_controller_managed_switch.move(
            ...     switch_id=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.switch_controller_managed_switch.move(
            ...     switch_id=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.switch_controller_managed_switch.move(
            ...     switch_id=100,
            ...     position="before",
            ...     reference_switch_id=50
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
                reference_switch_id = all_objects[0].switch_id
                actual_position = "before"
            elif position > len(all_objects):
                # Move to last position (after all existing objects)
                reference_switch_id = all_objects[-1].switch_id
                actual_position = "after"
            else:
                # Move before the object currently at that position
                reference_switch_id = all_objects[position - 1].switch_id
                actual_position = "before"
        
        # Handle top/bottom string positions
        elif position in ("top", "bottom"):
            # Get all objects to find first/last
            all_objects = self.get(vdom=vdom)
            if not all_objects:
                raise ValueError(f"Cannot move to {position} - no objects found")
            
            if position == "top":
                # Move before first object
                reference_switch_id = all_objects[0].switch_id
                actual_position = "before"
            else:  # bottom
                # Move after last object
                reference_switch_id = all_objects[-1].switch_id
                actual_position = "after"
        
        # Handle before/after string positions
        else:
            # Validate reference is provided for before/after
            if reference_switch_id is None:
                raise ValueError(f"reference_switch_id is required when position='{position}'")
            actual_position = position
        
        # Build params for move operation
        params = {
            "action": "move",
            actual_position: reference_switch_id,
            **kwargs,
        }
        
        # Move requires the mkey in the endpoint path
        endpoint = "/switch-controller/managed-switch/" + quote_path_param(switch_id)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





