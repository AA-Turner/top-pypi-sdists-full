"""
FortiOS CMDB - Log setting

Configuration endpoint for managing cmdb log/setting objects.

API Endpoints:
    GET    /cmdb/log/setting
    POST   /cmdb/log/setting
    PUT    /cmdb/log/setting/{identifier}
    DELETE /cmdb/log/setting/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.log_setting.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.log_setting.post(
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

class Setting(CRUDEndpoint, MetadataMixin):
    """Setting Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "setting"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "custom_log_fields": {
            "mkey": "field-id",
            "required_fields": ['field-id'],
            "example": "[{'field-id': 'value'}]",
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
        """Initialize Setting endpoint."""
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
        Retrieve log/setting configuration.

        Configure general log settings.

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
            >>> # Get all log/setting objects
            >>> result = fgt.api.cmdb.log_setting.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.log_setting.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.log_setting.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.log_setting.get_schema()

        See Also:
            - post(): Create new log/setting object
            - put(): Update existing log/setting object
            - delete(): Remove log/setting object
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
            endpoint = f"/log/setting/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/log/setting"
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
            >>> schema = fgt.api.cmdb.log_setting.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.log_setting.get_schema(format="json-schema")
        
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
        resolve_ip: Literal["enable", "disable"] | None = None,
        resolve_port: Literal["enable", "disable"] | None = None,
        log_user_in_upper: Literal["enable", "disable"] | None = None,
        fwpolicy_implicit_log: Literal["enable", "disable"] | None = None,
        fwpolicy6_implicit_log: Literal["enable", "disable"] | None = None,
        extended_log: Literal["enable", "disable"] | None = None,
        local_in_allow: Literal["enable", "disable"] | None = None,
        local_in_deny_unicast: Literal["enable", "disable"] | None = None,
        local_in_deny_broadcast: Literal["enable", "disable"] | None = None,
        local_in_policy_log: Literal["enable", "disable"] | None = None,
        local_out: Literal["enable", "disable"] | None = None,
        local_out_ioc_detection: Literal["enable", "disable"] | None = None,
        daemon_log: Literal["enable", "disable"] | None = None,
        neighbor_event: Literal["enable", "disable"] | None = None,
        brief_traffic_format: Literal["enable", "disable"] | None = None,
        user_anonymize: Literal["enable", "disable"] | None = None,
        expolicy_implicit_log: Literal["enable", "disable"] | None = None,
        log_policy_comment: Literal["enable", "disable"] | None = None,
        faz_override: Literal["enable", "disable"] | None = None,
        syslog_override: Literal["enable", "disable"] | None = None,
        rest_api_set: Literal["enable", "disable"] | None = None,
        rest_api_get: Literal["enable", "disable"] | None = None,
        rest_api_performance: Literal["enable", "disable"] | None = None,
        long_live_session_stat: Literal["enable", "disable"] | None = None,
        extended_utm_log: Literal["enable", "disable"] | None = None,
        zone_name: Literal["enable", "disable"] | None = None,
        web_svc_perf: Literal["enable", "disable"] | None = None,
        custom_log_fields: str | list[str] | list[dict[str, Any]] | None = None,
        anonymization_hash: str | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing log/setting object.

        Configure general log settings.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            resolve_ip: Enable/disable adding resolved domain names to traffic logs if possible.
            resolve_port: Enable/disable adding resolved service names to traffic logs.
            log_user_in_upper: Enable/disable logs with user-in-upper.
            fwpolicy_implicit_log: Enable/disable implicit firewall policy logging.
            fwpolicy6_implicit_log: Enable/disable implicit firewall policy6 logging.
            extended_log: Enable/disable extended traffic logging.
            local_in_allow: Enable/disable local-in-allow logging.
            local_in_deny_unicast: Enable/disable local-in-deny-unicast logging.
            local_in_deny_broadcast: Enable/disable local-in-deny-broadcast logging.
            local_in_policy_log: Enable/disable local-in-policy logging.
            local_out: Enable/disable local-out logging.
            local_out_ioc_detection: Enable/disable local-out traffic IoC detection. Requires local-out to be enabled.
            daemon_log: Enable/disable daemon logging.
            neighbor_event: Enable/disable neighbor event logging.
            brief_traffic_format: Enable/disable brief format traffic logging.
            user_anonymize: Enable/disable anonymizing user names in log messages.
            expolicy_implicit_log: Enable/disable proxy firewall implicit policy logging.
            log_policy_comment: Enable/disable inserting policy comments into traffic logs.
            faz_override: Enable/disable override FortiAnalyzer settings.
            syslog_override: Enable/disable override Syslog settings.
            rest_api_set: Enable/disable REST API POST/PUT/DELETE request logging.
            rest_api_get: Enable/disable REST API GET request logging.
            rest_api_performance: Enable/disable REST API memory and performance stats in rest-api-get/set logs.
            long_live_session_stat: Enable/disable long-live-session statistics logging.
            extended_utm_log: Enable/disable extended UTM logging.
            zone_name: Enable/disable zone name logging.
            web_svc_perf: Enable/disable web-svc performance logging.
            custom_log_fields: Custom fields to append to all log messages.
                Default format: [{'field-id': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'field-id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'field-id': 'val1'}, ...]
                  - List of dicts: [{'field-id': 'value'}] (recommended)
            anonymization_hash: User name anonymization hash salt.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.log_setting.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.log_setting.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if custom_log_fields is not None:
            custom_log_fields = normalize_table_field(
                custom_log_fields,
                mkey="field-id",
                required_fields=['field-id'],
                field_name="custom_log_fields",
                example="[{'field-id': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            resolve_ip=resolve_ip,
            resolve_port=resolve_port,
            log_user_in_upper=log_user_in_upper,
            fwpolicy_implicit_log=fwpolicy_implicit_log,
            fwpolicy6_implicit_log=fwpolicy6_implicit_log,
            extended_log=extended_log,
            local_in_allow=local_in_allow,
            local_in_deny_unicast=local_in_deny_unicast,
            local_in_deny_broadcast=local_in_deny_broadcast,
            local_in_policy_log=local_in_policy_log,
            local_out=local_out,
            local_out_ioc_detection=local_out_ioc_detection,
            daemon_log=daemon_log,
            neighbor_event=neighbor_event,
            brief_traffic_format=brief_traffic_format,
            user_anonymize=user_anonymize,
            expolicy_implicit_log=expolicy_implicit_log,
            log_policy_comment=log_policy_comment,
            faz_override=faz_override,
            syslog_override=syslog_override,
            rest_api_set=rest_api_set,
            rest_api_get=rest_api_get,
            rest_api_performance=rest_api_performance,
            long_live_session_stat=long_live_session_stat,
            extended_utm_log=extended_utm_log,
            zone_name=zone_name,
            web_svc_perf=web_svc_perf,
            custom_log_fields=custom_log_fields,
            anonymization_hash=anonymization_hash,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.setting import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/log/setting",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/log/setting"

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
        Move log/setting object to a new position.
        
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
            >>> fgt.api.cmdb.log_setting.move(
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
        endpoint = "/log/setting/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





