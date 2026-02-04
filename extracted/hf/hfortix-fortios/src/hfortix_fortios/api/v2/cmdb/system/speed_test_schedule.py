"""
FortiOS CMDB - System speed_test_schedule

Configuration endpoint for managing cmdb system/speed_test_schedule objects.

API Endpoints:
    GET    /cmdb/system/speed_test_schedule
    POST   /cmdb/system/speed_test_schedule
    PUT    /cmdb/system/speed_test_schedule/{identifier}
    DELETE /cmdb/system/speed_test_schedule/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_speed_test_schedule.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_speed_test_schedule.post(
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

class SpeedTestSchedule(CRUDEndpoint, MetadataMixin):
    """SpeedTestSchedule Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "speed_test_schedule"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "schedules": {
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
        """Initialize SpeedTestSchedule endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        interface: str | None = None,
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
        Retrieve system/speed_test_schedule configuration.

        Speed test schedule for each interface.

        Args:
            interface: String identifier to retrieve specific object.
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
            >>> # Get all system/speed_test_schedule objects
            >>> result = fgt.api.cmdb.system_speed_test_schedule.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/speed_test_schedule by interface
            >>> result = fgt.api.cmdb.system_speed_test_schedule.get(interface=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_speed_test_schedule.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_speed_test_schedule.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_speed_test_schedule.get_schema()

        See Also:
            - post(): Create new system/speed_test_schedule object
            - put(): Update existing system/speed_test_schedule object
            - delete(): Remove system/speed_test_schedule object
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
        
        if interface:
            endpoint = "/system/speed-test-schedule/" + quote_path_param(interface)
            unwrap_single = True
        else:
            endpoint = "/system/speed-test-schedule"
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
            >>> schema = fgt.api.cmdb.system_speed_test_schedule.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_speed_test_schedule.get_schema(format="json-schema")
        
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
        interface: str | None = None,
        status: Literal["disable", "enable"] | None = None,
        diffserv: str | None = None,
        server_name: str | None = None,
        mode: Literal["UDP", "TCP", "Auto"] | None = None,
        schedules: str | list[str] | list[dict[str, Any]] | None = None,
        dynamic_server: Literal["disable", "enable"] | None = None,
        ctrl_port: int | None = None,
        server_port: int | None = None,
        update_shaper: Literal["disable", "local", "remote", "both"] | None = None,
        update_inbandwidth: Literal["disable", "enable"] | None = None,
        update_outbandwidth: Literal["disable", "enable"] | None = None,
        update_interface_shaping: Literal["disable", "enable"] | None = None,
        update_inbandwidth_maximum: int | None = None,
        update_inbandwidth_minimum: int | None = None,
        update_outbandwidth_maximum: int | None = None,
        update_outbandwidth_minimum: int | None = None,
        expected_inbandwidth_minimum: int | None = None,
        expected_inbandwidth_maximum: int | None = None,
        expected_outbandwidth_minimum: int | None = None,
        expected_outbandwidth_maximum: int | None = None,
        retries: int | None = None,
        retry_pause: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/speed_test_schedule object.

        Speed test schedule for each interface.

        Args:
            payload_dict: Object data as dict. Must include interface (primary key).
            interface: Interface name.
            status: Enable/disable scheduled speed test.
            diffserv: DSCP used for speed test.
            server_name: Speed test server name in system.speed-test-server list or leave it as empty to choose default server "FTNT_Auto".
            mode: Protocol Auto(default), TCP or UDP used for speed test.
            schedules: Schedules for the interface.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dynamic_server: Enable/disable dynamic server option.
            ctrl_port: Port of the controller to get access token.
            server_port: Port of the server to run speed test.
            update_shaper: Set egress shaper based on the test result.
            update_inbandwidth: Enable/disable bypassing interface's inbound bandwidth setting.
            update_outbandwidth: Enable/disable bypassing interface's outbound bandwidth setting.
            update_interface_shaping: Enable/disable using the speedtest results as reference for interface shaping (overriding configured in/outbandwidth).
            update_inbandwidth_maximum: Maximum downloading bandwidth (kbps) to be used in a speed test.
            update_inbandwidth_minimum: Minimum downloading bandwidth (kbps) to be considered effective.
            update_outbandwidth_maximum: Maximum uploading bandwidth (kbps) to be used in a speed test.
            update_outbandwidth_minimum: Minimum uploading bandwidth (kbps) to be considered effective.
            expected_inbandwidth_minimum: Set the minimum inbandwidth threshold for applying speedtest results on shaping-profile.
            expected_inbandwidth_maximum: Set the maximum inbandwidth threshold for applying speedtest results on shaping-profile.
            expected_outbandwidth_minimum: Set the minimum outbandwidth threshold for applying speedtest results on shaping-profile.
            expected_outbandwidth_maximum: Set the maximum outbandwidth threshold for applying speedtest results on shaping-profile.
            retries: Maximum number of times the FortiGate unit will attempt to contact the same server before considering the speed test has failed (1 - 10, default = 5).
            retry_pause: Number of seconds the FortiGate pauses between successive speed tests before trying a different server (60 - 3600, default = 300).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If interface is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_speed_test_schedule.put(
            ...     interface=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "interface": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_speed_test_schedule.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if schedules is not None:
            schedules = normalize_table_field(
                schedules,
                mkey="name",
                required_fields=['name'],
                field_name="schedules",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            interface=interface,
            status=status,
            diffserv=diffserv,
            server_name=server_name,
            mode=mode,
            schedules=schedules,
            dynamic_server=dynamic_server,
            ctrl_port=ctrl_port,
            server_port=server_port,
            update_shaper=update_shaper,
            update_inbandwidth=update_inbandwidth,
            update_outbandwidth=update_outbandwidth,
            update_interface_shaping=update_interface_shaping,
            update_inbandwidth_maximum=update_inbandwidth_maximum,
            update_inbandwidth_minimum=update_inbandwidth_minimum,
            update_outbandwidth_maximum=update_outbandwidth_maximum,
            update_outbandwidth_minimum=update_outbandwidth_minimum,
            expected_inbandwidth_minimum=expected_inbandwidth_minimum,
            expected_inbandwidth_maximum=expected_inbandwidth_maximum,
            expected_outbandwidth_minimum=expected_outbandwidth_minimum,
            expected_outbandwidth_maximum=expected_outbandwidth_maximum,
            retries=retries,
            retry_pause=retry_pause,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.speed_test_schedule import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/speed_test_schedule",
            )
        
        interface_value = payload_data.get("interface")
        if not interface_value:
            raise ValueError("interface is required for PUT")
        endpoint = "/system/speed-test-schedule/" + quote_path_param(interface_value)

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
        interface: str | None = None,
        status: Literal["disable", "enable"] | None = None,
        diffserv: str | None = None,
        server_name: str | None = None,
        mode: Literal["UDP", "TCP", "Auto"] | None = None,
        schedules: str | list[str] | list[dict[str, Any]] | None = None,
        dynamic_server: Literal["disable", "enable"] | None = None,
        ctrl_port: int | None = None,
        server_port: int | None = None,
        update_shaper: Literal["disable", "local", "remote", "both"] | None = None,
        update_inbandwidth: Literal["disable", "enable"] | None = None,
        update_outbandwidth: Literal["disable", "enable"] | None = None,
        update_interface_shaping: Literal["disable", "enable"] | None = None,
        update_inbandwidth_maximum: int | None = None,
        update_inbandwidth_minimum: int | None = None,
        update_outbandwidth_maximum: int | None = None,
        update_outbandwidth_minimum: int | None = None,
        expected_inbandwidth_minimum: int | None = None,
        expected_inbandwidth_maximum: int | None = None,
        expected_outbandwidth_minimum: int | None = None,
        expected_outbandwidth_maximum: int | None = None,
        retries: int | None = None,
        retry_pause: int | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/speed_test_schedule object.

        Speed test schedule for each interface.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            interface: Interface name.
            status: Enable/disable scheduled speed test.
            diffserv: DSCP used for speed test.
            server_name: Speed test server name in system.speed-test-server list or leave it as empty to choose default server "FTNT_Auto".
            mode: Protocol Auto(default), TCP or UDP used for speed test.
            schedules: Schedules for the interface.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dynamic_server: Enable/disable dynamic server option.
            ctrl_port: Port of the controller to get access token.
            server_port: Port of the server to run speed test.
            update_shaper: Set egress shaper based on the test result.
            update_inbandwidth: Enable/disable bypassing interface's inbound bandwidth setting.
            update_outbandwidth: Enable/disable bypassing interface's outbound bandwidth setting.
            update_interface_shaping: Enable/disable using the speedtest results as reference for interface shaping (overriding configured in/outbandwidth).
            update_inbandwidth_maximum: Maximum downloading bandwidth (kbps) to be used in a speed test.
            update_inbandwidth_minimum: Minimum downloading bandwidth (kbps) to be considered effective.
            update_outbandwidth_maximum: Maximum uploading bandwidth (kbps) to be used in a speed test.
            update_outbandwidth_minimum: Minimum uploading bandwidth (kbps) to be considered effective.
            expected_inbandwidth_minimum: Set the minimum inbandwidth threshold for applying speedtest results on shaping-profile.
            expected_inbandwidth_maximum: Set the maximum inbandwidth threshold for applying speedtest results on shaping-profile.
            expected_outbandwidth_minimum: Set the minimum outbandwidth threshold for applying speedtest results on shaping-profile.
            expected_outbandwidth_maximum: Set the maximum outbandwidth threshold for applying speedtest results on shaping-profile.
            retries: Maximum number of times the FortiGate unit will attempt to contact the same server before considering the speed test has failed (1 - 10, default = 5).
            retry_pause: Number of seconds the FortiGate pauses between successive speed tests before trying a different server (60 - 3600, default = 300).
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_speed_test_schedule.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created interface: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = SpeedTestSchedule.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_speed_test_schedule.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(SpeedTestSchedule.required_fields()) }}
            
            Use SpeedTestSchedule.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if schedules is not None:
            schedules = normalize_table_field(
                schedules,
                mkey="name",
                required_fields=['name'],
                field_name="schedules",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            interface=interface,
            status=status,
            diffserv=diffserv,
            server_name=server_name,
            mode=mode,
            schedules=schedules,
            dynamic_server=dynamic_server,
            ctrl_port=ctrl_port,
            server_port=server_port,
            update_shaper=update_shaper,
            update_inbandwidth=update_inbandwidth,
            update_outbandwidth=update_outbandwidth,
            update_interface_shaping=update_interface_shaping,
            update_inbandwidth_maximum=update_inbandwidth_maximum,
            update_inbandwidth_minimum=update_inbandwidth_minimum,
            update_outbandwidth_maximum=update_outbandwidth_maximum,
            update_outbandwidth_minimum=update_outbandwidth_minimum,
            expected_inbandwidth_minimum=expected_inbandwidth_minimum,
            expected_inbandwidth_maximum=expected_inbandwidth_maximum,
            expected_outbandwidth_minimum=expected_outbandwidth_minimum,
            expected_outbandwidth_maximum=expected_outbandwidth_maximum,
            retries=retries,
            retry_pause=retry_pause,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.speed_test_schedule import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/speed_test_schedule",
            )

        endpoint = "/system/speed-test-schedule"
        
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
        interface: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete system/speed_test_schedule object.

        Speed test schedule for each interface.

        Args:
            interface: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If interface is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.system_speed_test_schedule.delete(interface=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not interface:
            raise ValueError("interface is required for DELETE")
        endpoint = "/system/speed-test-schedule/" + quote_path_param(interface)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        interface: str,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if system/speed_test_schedule object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            interface: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_speed_test_schedule.exists(interface=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_speed_test_schedule.exists(interface=1):
            ...     fgt.api.cmdb.system_speed_test_schedule.delete(interface=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system/speed-test-schedule"
        endpoint = f"{endpoint}/{quote_path_param(interface)}"
        
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
        interface: str | None = None,
        status: Literal["disable", "enable"] | None = None,
        diffserv: str | None = None,
        server_name: str | None = None,
        mode: Literal["UDP", "TCP", "Auto"] | None = None,
        schedules: str | list[str] | list[dict[str, Any]] | None = None,
        dynamic_server: Literal["disable", "enable"] | None = None,
        ctrl_port: int | None = None,
        server_port: int | None = None,
        update_shaper: Literal["disable", "local", "remote", "both"] | None = None,
        update_inbandwidth: Literal["disable", "enable"] | None = None,
        update_outbandwidth: Literal["disable", "enable"] | None = None,
        update_interface_shaping: Literal["disable", "enable"] | None = None,
        update_inbandwidth_maximum: int | None = None,
        update_inbandwidth_minimum: int | None = None,
        update_outbandwidth_maximum: int | None = None,
        update_outbandwidth_minimum: int | None = None,
        expected_inbandwidth_minimum: int | None = None,
        expected_inbandwidth_maximum: int | None = None,
        expected_outbandwidth_minimum: int | None = None,
        expected_outbandwidth_maximum: int | None = None,
        retries: int | None = None,
        retry_pause: int | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/speed_test_schedule object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (interface) in the payload.

        Args:
            payload_dict: Resource data including interface (primary key)
            interface: Field interface
            status: Field status
            diffserv: Field diffserv
            server_name: Field server-name
            mode: Field mode
            schedules: Field schedules
            dynamic_server: Field dynamic-server
            ctrl_port: Field ctrl-port
            server_port: Field server-port
            update_shaper: Field update-shaper
            update_inbandwidth: Field update-inbandwidth
            update_outbandwidth: Field update-outbandwidth
            update_interface_shaping: Field update-interface-shaping
            update_inbandwidth_maximum: Field update-inbandwidth-maximum
            update_inbandwidth_minimum: Field update-inbandwidth-minimum
            update_outbandwidth_maximum: Field update-outbandwidth-maximum
            update_outbandwidth_minimum: Field update-outbandwidth-minimum
            expected_inbandwidth_minimum: Field expected-inbandwidth-minimum
            expected_inbandwidth_maximum: Field expected-inbandwidth-maximum
            expected_outbandwidth_minimum: Field expected-outbandwidth-minimum
            expected_outbandwidth_maximum: Field expected-outbandwidth-maximum
            retries: Field retries
            retry_pause: Field retry-pause
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If interface is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_speed_test_schedule.set(
            ...     interface=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "interface": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_speed_test_schedule.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_speed_test_schedule.set(payload_dict=obj_data)
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
        if schedules is not None:
            schedules = normalize_table_field(
                schedules,
                mkey="name",
                required_fields=['name'],
                field_name="schedules",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            interface=interface,
            status=status,
            diffserv=diffserv,
            server_name=server_name,
            mode=mode,
            schedules=schedules,
            dynamic_server=dynamic_server,
            ctrl_port=ctrl_port,
            server_port=server_port,
            update_shaper=update_shaper,
            update_inbandwidth=update_inbandwidth,
            update_outbandwidth=update_outbandwidth,
            update_interface_shaping=update_interface_shaping,
            update_inbandwidth_maximum=update_inbandwidth_maximum,
            update_inbandwidth_minimum=update_inbandwidth_minimum,
            update_outbandwidth_maximum=update_outbandwidth_maximum,
            update_outbandwidth_minimum=update_outbandwidth_minimum,
            expected_inbandwidth_minimum=expected_inbandwidth_minimum,
            expected_inbandwidth_maximum=expected_inbandwidth_maximum,
            expected_outbandwidth_minimum=expected_outbandwidth_minimum,
            expected_outbandwidth_maximum=expected_outbandwidth_maximum,
            retries=retries,
            retry_pause=retry_pause,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("interface")
        if not mkey_value:
            raise ValueError("interface is required for set()")
        
        # Check if resource exists
        if self.exists(interface=mkey_value, vdom=vdom):
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
        interface: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_interface: str | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/speed_test_schedule object to a new position.
        
        Reorders objects by moving one before/after another, to top/bottom, or to a specific position.
        
        Args:
            interface: Identifier of object to move
            position: Where to move the object:
                - "before": Move before reference object (requires reference_interface)
                - "after": Move after reference object (requires reference_interface)
                - "top": Move to first position (reference not needed)
                - "bottom": Move to last position (reference not needed)
                - int (1-based): Move to specific position number (e.g., position=3 for 3rd place)
            reference_interface: Identifier of reference object (required for before/after)
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.system_speed_test_schedule.move(
            ...     interface=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.system_speed_test_schedule.move(
            ...     interface=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.system_speed_test_schedule.move(
            ...     interface=100,
            ...     position="before",
            ...     reference_interface=50
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
                reference_interface = all_objects[0].interface
                actual_position = "before"
            elif position > len(all_objects):
                # Move to last position (after all existing objects)
                reference_interface = all_objects[-1].interface
                actual_position = "after"
            else:
                # Move before the object currently at that position
                reference_interface = all_objects[position - 1].interface
                actual_position = "before"
        
        # Handle top/bottom string positions
        elif position in ("top", "bottom"):
            # Get all objects to find first/last
            all_objects = self.get(vdom=vdom)
            if not all_objects:
                raise ValueError(f"Cannot move to {position} - no objects found")
            
            if position == "top":
                # Move before first object
                reference_interface = all_objects[0].interface
                actual_position = "before"
            else:  # bottom
                # Move after last object
                reference_interface = all_objects[-1].interface
                actual_position = "after"
        
        # Handle before/after string positions
        else:
            # Validate reference is provided for before/after
            if reference_interface is None:
                raise ValueError(f"reference_interface is required when position='{position}'")
            actual_position = position
        
        # Build params for move operation
        params = {
            "action": "move",
            actual_position: reference_interface,
            **kwargs,
        }
        
        # Move requires the mkey in the endpoint path
        endpoint = "/system/speed-test-schedule/" + quote_path_param(interface)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





