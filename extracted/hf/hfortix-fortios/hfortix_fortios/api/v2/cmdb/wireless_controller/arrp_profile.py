"""
FortiOS CMDB - Wireless_controller arrp_profile

Configuration endpoint for managing cmdb wireless_controller/arrp_profile objects.

API Endpoints:
    GET    /cmdb/wireless_controller/arrp_profile
    POST   /cmdb/wireless_controller/arrp_profile
    PUT    /cmdb/wireless_controller/arrp_profile/{identifier}
    DELETE /cmdb/wireless_controller/arrp_profile/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.wireless_controller_arrp_profile.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.post(
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

class ArrpProfile(CRUDEndpoint, MetadataMixin):
    """ArrpProfile Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "arrp_profile"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "darrp_optimize_schedules": {
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
        """Initialize ArrpProfile endpoint."""
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
        Retrieve wireless_controller/arrp_profile configuration.

        Configure WiFi Automatic Radio Resource Provisioning (ARRP) profiles.

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
            >>> # Get all wireless_controller/arrp_profile objects
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific wireless_controller/arrp_profile by name
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.wireless_controller_arrp_profile.get_schema()

        See Also:
            - post(): Create new wireless_controller/arrp_profile object
            - put(): Update existing wireless_controller/arrp_profile object
            - delete(): Remove wireless_controller/arrp_profile object
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
            endpoint = "/wireless-controller/arrp-profile/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/wireless-controller/arrp-profile"
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
            >>> schema = fgt.api.cmdb.wireless_controller_arrp_profile.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.wireless_controller_arrp_profile.get_schema(format="json-schema")
        
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
        comment: str | None = None,
        selection_period: int | None = None,
        monitor_period: int | None = None,
        weight_managed_ap: int | None = None,
        weight_rogue_ap: int | None = None,
        weight_noise_floor: int | None = None,
        weight_channel_load: int | None = None,
        weight_spectral_rssi: int | None = None,
        weight_weather_channel: int | None = None,
        weight_dfs_channel: int | None = None,
        threshold_ap: int | None = None,
        threshold_noise_floor: str | None = None,
        threshold_channel_load: int | None = None,
        threshold_spectral_rssi: str | None = None,
        threshold_tx_retries: int | None = None,
        threshold_rx_errors: int | None = None,
        include_weather_channel: Literal["enable", "disable"] | None = None,
        include_dfs_channel: Literal["enable", "disable"] | None = None,
        override_darrp_optimize: Literal["enable", "disable"] | None = None,
        darrp_optimize: int | None = None,
        darrp_optimize_schedules: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing wireless_controller/arrp_profile object.

        Configure WiFi Automatic Radio Resource Provisioning (ARRP) profiles.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: WiFi ARRP profile name.
            comment: Comment.
            selection_period: Period in seconds to measure average channel load, noise floor, spectral RSSI (default = 3600).
            monitor_period: Period in seconds to measure average transmit retries and receive errors (default = 300).
            weight_managed_ap: Weight in DARRP channel score calculation for managed APs (0 - 2000, default = 50).
            weight_rogue_ap: Weight in DARRP channel score calculation for rogue APs (0 - 2000, default = 10).
            weight_noise_floor: Weight in DARRP channel score calculation for noise floor (0 - 2000, default = 40).
            weight_channel_load: Weight in DARRP channel score calculation for channel load (0 - 2000, default = 20).
            weight_spectral_rssi: Weight in DARRP channel score calculation for spectral RSSI (0 - 2000, default = 40).
            weight_weather_channel: Weight in DARRP channel score calculation for weather channel (0 - 2000, default = 0).
            weight_dfs_channel: Weight in DARRP channel score calculation for DFS channel (0 - 2000, default = 0).
            threshold_ap: Threshold to reject channel in DARRP channel selection phase 1 due to surrounding APs (0 - 500, default = 250).
            threshold_noise_floor: Threshold in dBm to reject channel in DARRP channel selection phase 1 due to noise floor (-95 to -20, default = -85).
            threshold_channel_load: Threshold in percentage to reject channel in DARRP channel selection phase 1 due to channel load (0 - 100, default = 60).
            threshold_spectral_rssi: Threshold in dBm to reject channel in DARRP channel selection phase 1 due to spectral RSSI (-95 to -20, default = -65).
            threshold_tx_retries: Threshold in percentage for transmit retries to trigger channel reselection in DARRP monitor stage (0 - 1000, default = 300).
            threshold_rx_errors: Threshold in percentage for receive errors to trigger channel reselection in DARRP monitor stage (0 - 100, default = 50).
            include_weather_channel: Enable/disable use of weather channel in DARRP channel selection phase 1 (default = enable).
            include_dfs_channel: Enable/disable use of DFS channel in DARRP channel selection phase 1 (default = enable).
            override_darrp_optimize: Enable to override setting darrp-optimize and darrp-optimize-schedules (default = disable).
            darrp_optimize: Time for running Distributed Automatic Radio Resource Provisioning (DARRP) optimizations (0 - 86400 sec, default = 86400, 0 = disable).
            darrp_optimize_schedules: Firewall schedules for DARRP running time. DARRP will run periodically based on darrp-optimize within the schedules. Separate multiple schedule names with a space.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if darrp_optimize_schedules is not None:
            darrp_optimize_schedules = normalize_table_field(
                darrp_optimize_schedules,
                mkey="name",
                required_fields=['name'],
                field_name="darrp_optimize_schedules",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            comment=comment,
            selection_period=selection_period,
            monitor_period=monitor_period,
            weight_managed_ap=weight_managed_ap,
            weight_rogue_ap=weight_rogue_ap,
            weight_noise_floor=weight_noise_floor,
            weight_channel_load=weight_channel_load,
            weight_spectral_rssi=weight_spectral_rssi,
            weight_weather_channel=weight_weather_channel,
            weight_dfs_channel=weight_dfs_channel,
            threshold_ap=threshold_ap,
            threshold_noise_floor=threshold_noise_floor,
            threshold_channel_load=threshold_channel_load,
            threshold_spectral_rssi=threshold_spectral_rssi,
            threshold_tx_retries=threshold_tx_retries,
            threshold_rx_errors=threshold_rx_errors,
            include_weather_channel=include_weather_channel,
            include_dfs_channel=include_dfs_channel,
            override_darrp_optimize=override_darrp_optimize,
            darrp_optimize=darrp_optimize,
            darrp_optimize_schedules=darrp_optimize_schedules,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.arrp_profile import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/wireless_controller/arrp_profile",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/wireless-controller/arrp-profile/" + quote_path_param(name_value)

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
        comment: str | None = None,
        selection_period: int | None = None,
        monitor_period: int | None = None,
        weight_managed_ap: int | None = None,
        weight_rogue_ap: int | None = None,
        weight_noise_floor: int | None = None,
        weight_channel_load: int | None = None,
        weight_spectral_rssi: int | None = None,
        weight_weather_channel: int | None = None,
        weight_dfs_channel: int | None = None,
        threshold_ap: int | None = None,
        threshold_noise_floor: str | None = None,
        threshold_channel_load: int | None = None,
        threshold_spectral_rssi: str | None = None,
        threshold_tx_retries: int | None = None,
        threshold_rx_errors: int | None = None,
        include_weather_channel: Literal["enable", "disable"] | None = None,
        include_dfs_channel: Literal["enable", "disable"] | None = None,
        override_darrp_optimize: Literal["enable", "disable"] | None = None,
        darrp_optimize: int | None = None,
        darrp_optimize_schedules: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new wireless_controller/arrp_profile object.

        Configure WiFi Automatic Radio Resource Provisioning (ARRP) profiles.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: WiFi ARRP profile name.
            comment: Comment.
            selection_period: Period in seconds to measure average channel load, noise floor, spectral RSSI (default = 3600).
            monitor_period: Period in seconds to measure average transmit retries and receive errors (default = 300).
            weight_managed_ap: Weight in DARRP channel score calculation for managed APs (0 - 2000, default = 50).
            weight_rogue_ap: Weight in DARRP channel score calculation for rogue APs (0 - 2000, default = 10).
            weight_noise_floor: Weight in DARRP channel score calculation for noise floor (0 - 2000, default = 40).
            weight_channel_load: Weight in DARRP channel score calculation for channel load (0 - 2000, default = 20).
            weight_spectral_rssi: Weight in DARRP channel score calculation for spectral RSSI (0 - 2000, default = 40).
            weight_weather_channel: Weight in DARRP channel score calculation for weather channel (0 - 2000, default = 0).
            weight_dfs_channel: Weight in DARRP channel score calculation for DFS channel (0 - 2000, default = 0).
            threshold_ap: Threshold to reject channel in DARRP channel selection phase 1 due to surrounding APs (0 - 500, default = 250).
            threshold_noise_floor: Threshold in dBm to reject channel in DARRP channel selection phase 1 due to noise floor (-95 to -20, default = -85).
            threshold_channel_load: Threshold in percentage to reject channel in DARRP channel selection phase 1 due to channel load (0 - 100, default = 60).
            threshold_spectral_rssi: Threshold in dBm to reject channel in DARRP channel selection phase 1 due to spectral RSSI (-95 to -20, default = -65).
            threshold_tx_retries: Threshold in percentage for transmit retries to trigger channel reselection in DARRP monitor stage (0 - 1000, default = 300).
            threshold_rx_errors: Threshold in percentage for receive errors to trigger channel reselection in DARRP monitor stage (0 - 100, default = 50).
            include_weather_channel: Enable/disable use of weather channel in DARRP channel selection phase 1 (default = enable).
            include_dfs_channel: Enable/disable use of DFS channel in DARRP channel selection phase 1 (default = enable).
            override_darrp_optimize: Enable to override setting darrp-optimize and darrp-optimize-schedules (default = disable).
            darrp_optimize: Time for running Distributed Automatic Radio Resource Provisioning (DARRP) optimizations (0 - 86400 sec, default = 86400, 0 = disable).
            darrp_optimize_schedules: Firewall schedules for DARRP running time. DARRP will run periodically based on darrp-optimize within the schedules. Separate multiple schedule names with a space.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = ArrpProfile.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(ArrpProfile.required_fields()) }}
            
            Use ArrpProfile.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if darrp_optimize_schedules is not None:
            darrp_optimize_schedules = normalize_table_field(
                darrp_optimize_schedules,
                mkey="name",
                required_fields=['name'],
                field_name="darrp_optimize_schedules",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            comment=comment,
            selection_period=selection_period,
            monitor_period=monitor_period,
            weight_managed_ap=weight_managed_ap,
            weight_rogue_ap=weight_rogue_ap,
            weight_noise_floor=weight_noise_floor,
            weight_channel_load=weight_channel_load,
            weight_spectral_rssi=weight_spectral_rssi,
            weight_weather_channel=weight_weather_channel,
            weight_dfs_channel=weight_dfs_channel,
            threshold_ap=threshold_ap,
            threshold_noise_floor=threshold_noise_floor,
            threshold_channel_load=threshold_channel_load,
            threshold_spectral_rssi=threshold_spectral_rssi,
            threshold_tx_retries=threshold_tx_retries,
            threshold_rx_errors=threshold_rx_errors,
            include_weather_channel=include_weather_channel,
            include_dfs_channel=include_dfs_channel,
            override_darrp_optimize=override_darrp_optimize,
            darrp_optimize=darrp_optimize,
            darrp_optimize_schedules=darrp_optimize_schedules,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.arrp_profile import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/wireless_controller/arrp_profile",
            )

        endpoint = "/wireless-controller/arrp-profile"
        
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
        Delete wireless_controller/arrp_profile object.

        Configure WiFi Automatic Radio Resource Provisioning (ARRP) profiles.

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
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/wireless-controller/arrp-profile/" + quote_path_param(name)

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
        Check if wireless_controller/arrp_profile object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.wireless_controller_arrp_profile.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.wireless_controller_arrp_profile.exists(name=1):
            ...     fgt.api.cmdb.wireless_controller_arrp_profile.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/wireless-controller/arrp-profile"
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
        comment: str | None = None,
        selection_period: int | None = None,
        monitor_period: int | None = None,
        weight_managed_ap: int | None = None,
        weight_rogue_ap: int | None = None,
        weight_noise_floor: int | None = None,
        weight_channel_load: int | None = None,
        weight_spectral_rssi: int | None = None,
        weight_weather_channel: int | None = None,
        weight_dfs_channel: int | None = None,
        threshold_ap: int | None = None,
        threshold_noise_floor: str | None = None,
        threshold_channel_load: int | None = None,
        threshold_spectral_rssi: str | None = None,
        threshold_tx_retries: int | None = None,
        threshold_rx_errors: int | None = None,
        include_weather_channel: Literal["enable", "disable"] | None = None,
        include_dfs_channel: Literal["enable", "disable"] | None = None,
        override_darrp_optimize: Literal["enable", "disable"] | None = None,
        darrp_optimize: int | None = None,
        darrp_optimize_schedules: str | list[str] | list[dict[str, Any]] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update wireless_controller/arrp_profile object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            comment: Field comment
            selection_period: Field selection-period
            monitor_period: Field monitor-period
            weight_managed_ap: Field weight-managed-ap
            weight_rogue_ap: Field weight-rogue-ap
            weight_noise_floor: Field weight-noise-floor
            weight_channel_load: Field weight-channel-load
            weight_spectral_rssi: Field weight-spectral-rssi
            weight_weather_channel: Field weight-weather-channel
            weight_dfs_channel: Field weight-dfs-channel
            threshold_ap: Field threshold-ap
            threshold_noise_floor: Field threshold-noise-floor
            threshold_channel_load: Field threshold-channel-load
            threshold_spectral_rssi: Field threshold-spectral-rssi
            threshold_tx_retries: Field threshold-tx-retries
            threshold_rx_errors: Field threshold-rx-errors
            include_weather_channel: Field include-weather-channel
            include_dfs_channel: Field include-dfs-channel
            override_darrp_optimize: Field override-darrp-optimize
            darrp_optimize: Field darrp-optimize
            darrp_optimize_schedules: Field darrp-optimize-schedules
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.wireless_controller_arrp_profile.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.wireless_controller_arrp_profile.set(payload_dict=obj_data)
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
        if darrp_optimize_schedules is not None:
            darrp_optimize_schedules = normalize_table_field(
                darrp_optimize_schedules,
                mkey="name",
                required_fields=['name'],
                field_name="darrp_optimize_schedules",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            comment=comment,
            selection_period=selection_period,
            monitor_period=monitor_period,
            weight_managed_ap=weight_managed_ap,
            weight_rogue_ap=weight_rogue_ap,
            weight_noise_floor=weight_noise_floor,
            weight_channel_load=weight_channel_load,
            weight_spectral_rssi=weight_spectral_rssi,
            weight_weather_channel=weight_weather_channel,
            weight_dfs_channel=weight_dfs_channel,
            threshold_ap=threshold_ap,
            threshold_noise_floor=threshold_noise_floor,
            threshold_channel_load=threshold_channel_load,
            threshold_spectral_rssi=threshold_spectral_rssi,
            threshold_tx_retries=threshold_tx_retries,
            threshold_rx_errors=threshold_rx_errors,
            include_weather_channel=include_weather_channel,
            include_dfs_channel=include_dfs_channel,
            override_darrp_optimize=override_darrp_optimize,
            darrp_optimize=darrp_optimize,
            darrp_optimize_schedules=darrp_optimize_schedules,
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
        Move wireless_controller/arrp_profile object to a new position.
        
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
            >>> fgt.api.cmdb.wireless_controller_arrp_profile.move(
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
        
        endpoint = "/wireless-controller/arrp-profile"
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
        Clone wireless_controller/arrp_profile object.
        
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
            >>> fgt.api.cmdb.wireless_controller_arrp_profile.clone(
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
        
        endpoint = "/wireless-controller/arrp-profile"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




