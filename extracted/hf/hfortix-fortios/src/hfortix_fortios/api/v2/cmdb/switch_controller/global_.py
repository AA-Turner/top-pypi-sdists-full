"""
FortiOS CMDB - Switch_controller global_

Configuration endpoint for managing cmdb switch_controller/global_ objects.

API Endpoints:
    GET    /cmdb/switch_controller/global_
    POST   /cmdb/switch_controller/global_
    PUT    /cmdb/switch_controller/global_/{identifier}
    DELETE /cmdb/switch_controller/global_/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.switch_controller_global.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.switch_controller_global.post(
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

class Global(CRUDEndpoint, MetadataMixin):
    """Global Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "global_"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "disable_discovery": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "custom_command": {
            "mkey": "command-entry",
            "required_fields": ['command-name'],
            "example": "[{'command-name': 'value'}]",
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
        """Initialize Global endpoint."""
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
        Retrieve switch_controller/global_ configuration.

        Configure FortiSwitch global settings.

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
            >>> # Get all switch_controller/global_ objects
            >>> result = fgt.api.cmdb.switch_controller_global.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.switch_controller_global.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.switch_controller_global.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.switch_controller_global.get_schema()

        See Also:
            - post(): Create new switch_controller/global_ object
            - put(): Update existing switch_controller/global_ object
            - delete(): Remove switch_controller/global_ object
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
            endpoint = f"/switch-controller/global/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/switch-controller/global"
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
            >>> schema = fgt.api.cmdb.switch_controller_global.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.switch_controller_global.get_schema(format="json-schema")
        
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
        mac_aging_interval: int | None = None,
        https_image_push: Literal["enable", "disable"] | None = None,
        vlan_all_mode: Literal["all", "defined"] | None = None,
        vlan_optimization: Literal["prune", "configured", "none"] | None = None,
        vlan_identity: Literal["description", "name"] | None = None,
        disable_discovery: str | list[str] | list[dict[str, Any]] | None = None,
        mac_retention_period: int | None = None,
        default_virtual_switch_vlan: str | None = None,
        dhcp_server_access_list: Literal["enable", "disable"] | None = None,
        dhcp_option82_format: Literal["ascii", "legacy"] | None = None,
        dhcp_option82_circuit_id: Literal["intfname", "vlan", "hostname", "mode", "description"] | list[str] | None = None,
        dhcp_option82_remote_id: Literal["mac", "hostname", "ip"] | list[str] | None = None,
        dhcp_snoop_client_req: Literal["drop-untrusted", "forward-untrusted"] | None = None,
        dhcp_snoop_client_db_exp: int | None = None,
        dhcp_snoop_db_per_port_learn_limit: int | None = None,
        log_mac_limit_violations: Literal["enable", "disable"] | None = None,
        mac_violation_timer: int | None = None,
        sn_dns_resolution: Literal["enable", "disable"] | None = None,
        mac_event_logging: Literal["enable", "disable"] | None = None,
        bounce_quarantined_link: Literal["disable", "enable"] | None = None,
        quarantine_mode: Literal["by-vlan", "by-redirect"] | None = None,
        update_user_device: Literal["mac-cache", "lldp", "dhcp-snooping", "l2-db", "l3-db"] | list[str] | None = None,
        custom_command: str | list[str] | list[dict[str, Any]] | None = None,
        fips_enforce: Literal["disable", "enable"] | None = None,
        firmware_provision_on_authorization: Literal["enable", "disable"] | None = None,
        switch_on_deauth: Literal["no-op", "factory-reset"] | None = None,
        firewall_auth_user_hold_period: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing switch_controller/global_ object.

        Configure FortiSwitch global settings.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            mac_aging_interval: Time after which an inactive MAC is aged out (10 - 1000000 sec, default = 300, 0 = disable).
            https_image_push: Enable/disable image push to FortiSwitch using HTTPS.
            vlan_all_mode: VLAN configuration mode, user-defined-vlans or all-possible-vlans.
            vlan_optimization: FortiLink VLAN optimization.
            vlan_identity: Identity of the VLAN. Commonly used for RADIUS Tunnel-Private-Group-Id.
            disable_discovery: Prevent this FortiSwitch from discovering.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            mac_retention_period: Time in hours after which an inactive MAC is removed from client DB (0 = aged out based on mac-aging-interval).
            default_virtual_switch_vlan: Default VLAN for ports when added to the virtual-switch.
            dhcp_server_access_list: Enable/disable DHCP snooping server access list.
            dhcp_option82_format: DHCP option-82 format string.
            dhcp_option82_circuit_id: List the parameters to be included to inform about client identification.
            dhcp_option82_remote_id: List the parameters to be included to inform about client identification.
            dhcp_snoop_client_req: Client DHCP packet broadcast mode.
            dhcp_snoop_client_db_exp: Expiry time for DHCP snooping server database entries (300 - 259200 sec, default = 86400 sec).
            dhcp_snoop_db_per_port_learn_limit: Per Interface dhcp-server entries learn limit (0 - 1024, default = 64).
            log_mac_limit_violations: Enable/disable logs for Learning Limit Violations.
            mac_violation_timer: Set timeout for Learning Limit Violations (0 = disabled).
            sn_dns_resolution: Enable/disable DNS resolution of the FortiSwitch unit's IP address with switch name.
            mac_event_logging: Enable/disable MAC address event logging.
            bounce_quarantined_link: Enable/disable bouncing (administratively bring the link down, up) of a switch port where a quarantined device was seen last. Helps to re-initiate the DHCP process for a device.
            quarantine_mode: Quarantine mode.
            update_user_device: Control which sources update the device user list.
            custom_command: List of custom commands to be pushed to all FortiSwitches in the VDOM.
                Default format: [{'command-name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'command-entry': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'command-entry': 'val1'}, ...]
                  - List of dicts: [{'command-name': 'value'}] (recommended)
            fips_enforce: Enable/disable enforcement of FIPS on managed FortiSwitch devices.
            firmware_provision_on_authorization: Enable/disable automatic provisioning of latest firmware on authorization.
            switch_on_deauth: No-operation/Factory-reset the managed FortiSwitch on deauthorization.
            firewall_auth_user_hold_period: Time period in minutes to hold firewall authenticated MAC users (5 - 1440, default = 5, disable = 0).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.switch_controller_global.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.switch_controller_global.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if disable_discovery is not None:
            disable_discovery = normalize_table_field(
                disable_discovery,
                mkey="name",
                required_fields=['name'],
                field_name="disable_discovery",
                example="[{'name': 'value'}]",
            )
        if custom_command is not None:
            custom_command = normalize_table_field(
                custom_command,
                mkey="command-entry",
                required_fields=['command-name'],
                field_name="custom_command",
                example="[{'command-name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            mac_aging_interval=mac_aging_interval,
            https_image_push=https_image_push,
            vlan_all_mode=vlan_all_mode,
            vlan_optimization=vlan_optimization,
            vlan_identity=vlan_identity,
            disable_discovery=disable_discovery,
            mac_retention_period=mac_retention_period,
            default_virtual_switch_vlan=default_virtual_switch_vlan,
            dhcp_server_access_list=dhcp_server_access_list,
            dhcp_option82_format=dhcp_option82_format,
            dhcp_option82_circuit_id=dhcp_option82_circuit_id,
            dhcp_option82_remote_id=dhcp_option82_remote_id,
            dhcp_snoop_client_req=dhcp_snoop_client_req,
            dhcp_snoop_client_db_exp=dhcp_snoop_client_db_exp,
            dhcp_snoop_db_per_port_learn_limit=dhcp_snoop_db_per_port_learn_limit,
            log_mac_limit_violations=log_mac_limit_violations,
            mac_violation_timer=mac_violation_timer,
            sn_dns_resolution=sn_dns_resolution,
            mac_event_logging=mac_event_logging,
            bounce_quarantined_link=bounce_quarantined_link,
            quarantine_mode=quarantine_mode,
            update_user_device=update_user_device,
            custom_command=custom_command,
            fips_enforce=fips_enforce,
            firmware_provision_on_authorization=firmware_provision_on_authorization,
            switch_on_deauth=switch_on_deauth,
            firewall_auth_user_hold_period=firewall_auth_user_hold_period,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.global_ import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/switch_controller/global_",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/switch-controller/global"

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
        Move switch_controller/global_ object to a new position.
        
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
            >>> fgt.api.cmdb.switch_controller_global.move(
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
        endpoint = "/switch-controller/global/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





