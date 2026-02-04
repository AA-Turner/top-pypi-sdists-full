"""
FortiOS CMDB - System fortiguard

Configuration endpoint for managing cmdb system/fortiguard objects.

API Endpoints:
    GET    /cmdb/system/fortiguard
    POST   /cmdb/system/fortiguard
    PUT    /cmdb/system/fortiguard/{identifier}
    DELETE /cmdb/system/fortiguard/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_fortiguard.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_fortiguard.post(
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

class Fortiguard(CRUDEndpoint, MetadataMixin):
    """Fortiguard Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "fortiguard"
    
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
        """Initialize Fortiguard endpoint."""
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
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve system/fortiguard configuration.

        Configure FortiGuard services.

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
            >>> # Get all system/fortiguard objects
            >>> result = fgt.api.cmdb.system_fortiguard.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_fortiguard.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_fortiguard.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_fortiguard.get_schema()

        See Also:
            - post(): Create new system/fortiguard object
            - put(): Update existing system/fortiguard object
            - delete(): Remove system/fortiguard object
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
            endpoint = f"/system/fortiguard/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/system/fortiguard"
            unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=False, unwrap_single=unwrap_single
        )

    def get_schema(
        self,
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
            format: Schema format - "schema" (FortiOS native) or "json-schema" (JSON Schema standard).
                Defaults to "schema".
                
        Returns:
            Schema definition as dict. Returns Coroutine if using async client.
            
        Example:
            >>> # Get FortiOS native schema
            >>> schema = fgt.api.cmdb.system_fortiguard.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_fortiguard.get_schema(format="json-schema")
        
        Note:
            Not all endpoints support all schema formats. The "schema" format
            is most widely supported.
        """
        return self.get(payload_dict={"action": format})


    # ========================================================================
    # PUT Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def put(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        fortiguard_anycast: Literal["enable", "disable"] | None = None,
        fortiguard_anycast_source: Literal["fortinet", "aws", "debug"] | None = None,
        protocol: Literal["udp", "http", "https"] | None = None,
        port: Literal["8888", "53", "80", "443"] | None = None,
        load_balance_servers: int | None = None,
        auto_join_forticloud: Literal["enable", "disable"] | None = None,
        update_server_location: Literal["automatic", "usa", "eu"] | None = None,
        sandbox_region: str | None = None,
        sandbox_inline_scan: Literal["enable", "disable"] | None = None,
        update_ffdb: Literal["enable", "disable"] | None = None,
        update_uwdb: Literal["enable", "disable"] | None = None,
        update_dldb: Literal["enable", "disable"] | None = None,
        update_extdb: Literal["enable", "disable"] | None = None,
        update_build_proxy: Literal["enable", "disable"] | None = None,
        persistent_connection: Literal["enable", "disable"] | None = None,
        auto_firmware_upgrade: Literal["enable", "disable"] | None = None,
        auto_firmware_upgrade_day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | list[str] | None = None,
        auto_firmware_upgrade_delay: int | None = None,
        auto_firmware_upgrade_start_hour: int | None = None,
        auto_firmware_upgrade_end_hour: int | None = None,
        FDS_license_expiring_days: int | None = None,
        subscribe_update_notification: Literal["enable", "disable"] | None = None,
        antispam_force_off: Literal["enable", "disable"] | None = None,
        antispam_cache: Literal["enable", "disable"] | None = None,
        antispam_cache_ttl: int | None = None,
        antispam_cache_mpermille: int | None = None,
        antispam_license: int | None = None,
        antispam_expiration: int | None = None,
        antispam_timeout: int | None = None,
        outbreak_prevention_force_off: Literal["enable", "disable"] | None = None,
        outbreak_prevention_cache: Literal["enable", "disable"] | None = None,
        outbreak_prevention_cache_ttl: int | None = None,
        outbreak_prevention_cache_mpermille: int | None = None,
        outbreak_prevention_license: int | None = None,
        outbreak_prevention_expiration: int | None = None,
        outbreak_prevention_timeout: int | None = None,
        webfilter_force_off: Literal["enable", "disable"] | None = None,
        webfilter_cache: Literal["enable", "disable"] | None = None,
        webfilter_cache_ttl: int | None = None,
        webfilter_license: int | None = None,
        webfilter_expiration: int | None = None,
        webfilter_timeout: int | None = None,
        sdns_server_ip: str | list[str] | None = None,
        sdns_server_port: int | None = None,
        anycast_sdns_server_ip: str | None = None,
        anycast_sdns_server_port: int | None = None,
        sdns_options: Literal["include-question-section"] | list[str] | None = None,
        source_ip: str | None = None,
        source_ip6: str | None = None,
        proxy_server_ip: str | None = None,
        proxy_server_port: int | None = None,
        proxy_username: str | None = None,
        proxy_password: Any | None = None,
        ddns_server_ip: str | None = None,
        ddns_server_ip6: str | None = None,
        ddns_server_port: int | None = None,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = None,
        interface: str | None = None,
        vrf_select: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/fortiguard object.

        Configure FortiGuard services.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            fortiguard_anycast: Enable/disable use of FortiGuard's Anycast network.
            fortiguard_anycast_source: Configure which of Fortinet's servers to provide FortiGuard services in FortiGuard's anycast network. Default is Fortinet.
            protocol: Protocol used to communicate with the FortiGuard servers.
            port: Port used to communicate with the FortiGuard servers.
            load_balance_servers: Number of servers to alternate between as first FortiGuard option.
            auto_join_forticloud: Automatically connect to and login to FortiCloud.
            update_server_location: Location from which to receive FortiGuard updates.
            sandbox_region: FortiCloud Sandbox region.
            sandbox_inline_scan: Enable/disable FortiCloud Sandbox inline-scan.
            update_ffdb: Enable/disable Internet Service Database update.
            update_uwdb: Enable/disable allowlist update.
            update_dldb: Enable/disable DLP signature update.
            update_extdb: Enable/disable external resource update.
            update_build_proxy: Enable/disable proxy dictionary rebuild.
            persistent_connection: Enable/disable use of persistent connection to receive update notification from FortiGuard.
            vdom: FortiGuard Service virtual domain name.
            auto_firmware_upgrade: Enable/disable automatic patch-level firmware upgrade from FortiGuard. The FortiGate unit searches for new patches only in the same major and minor version.
            auto_firmware_upgrade_day: Allowed day(s) of the week to install an automatic patch-level firmware upgrade from FortiGuard (default is none). Disallow any day of the week to use auto-firmware-upgrade-delay instead, which waits for designated days before installing an automatic patch-level firmware upgrade.
            auto_firmware_upgrade_delay: Delay of day(s) before installing an automatic patch-level firmware upgrade from FortiGuard (default = 3). Set it 0 to use auto-firmware-upgrade-day instead, which selects allowed day(s) of the week for installing an automatic patch-level firmware upgrade.
            auto_firmware_upgrade_start_hour: Start time in the designated time window for automatic patch-level firmware upgrade from FortiGuard in 24 hour time (0 ~ 23, default = 2). The actual upgrade time is selected randomly within the time window.
            auto_firmware_upgrade_end_hour: End time in the designated time window for automatic patch-level firmware upgrade from FortiGuard in 24 hour time (0 ~ 23, default = 4). When the end time is smaller than the start time, the end time is interpreted as the next day. The actual upgrade time is selected randomly within the time window.
            FDS_license_expiring_days: Threshold for number of days before FortiGuard license expiration to generate license expiring event log (1 - 100 days, default = 15).
            subscribe_update_notification: Enable/disable subscription to receive update notification from FortiGuard.
            antispam_force_off: Enable/disable turning off the FortiGuard antispam service.
            antispam_cache: Enable/disable FortiGuard antispam request caching. Uses a small amount of memory but improves performance.
            antispam_cache_ttl: Time-to-live for antispam cache entries in seconds (300 - 86400). Lower times reduce the cache size. Higher times may improve performance since the cache will have more entries.
            antispam_cache_mpermille: Maximum permille of FortiGate memory the antispam cache is allowed to use (1 - 150).
            antispam_license: Interval of time between license checks for the FortiGuard antispam contract.
            antispam_expiration: Expiration date of the FortiGuard antispam contract.
            antispam_timeout: Antispam query time out (1 - 30 sec, default = 7).
            outbreak_prevention_force_off: Turn off FortiGuard Virus Outbreak Prevention service.
            outbreak_prevention_cache: Enable/disable FortiGuard Virus Outbreak Prevention cache.
            outbreak_prevention_cache_ttl: Time-to-live for FortiGuard Virus Outbreak Prevention cache entries (300 - 86400 sec, default = 300).
            outbreak_prevention_cache_mpermille: Maximum permille of memory FortiGuard Virus Outbreak Prevention cache can use (1 - 150 permille, default = 1).
            outbreak_prevention_license: Interval of time between license checks for FortiGuard Virus Outbreak Prevention contract.
            outbreak_prevention_expiration: Expiration date of FortiGuard Virus Outbreak Prevention contract.
            outbreak_prevention_timeout: FortiGuard Virus Outbreak Prevention time out (1 - 30 sec, default = 7).
            webfilter_force_off: Enable/disable turning off the FortiGuard web filtering service.
            webfilter_cache: Enable/disable FortiGuard web filter caching.
            webfilter_cache_ttl: Time-to-live for web filter cache entries in seconds (300 - 86400).
            webfilter_license: Interval of time between license checks for the FortiGuard web filter contract.
            webfilter_expiration: Expiration date of the FortiGuard web filter contract.
            webfilter_timeout: Web filter query time out (1 - 30 sec, default = 15).
            sdns_server_ip: IP address of the FortiGuard DNS rating server.
            sdns_server_port: Port to connect to on the FortiGuard DNS rating server.
            anycast_sdns_server_ip: IP address of the FortiGuard anycast DNS rating server.
            anycast_sdns_server_port: Port to connect to on the FortiGuard anycast DNS rating server.
            sdns_options: Customization options for the FortiGuard DNS service.
            source_ip: Source IPv4 address used to communicate with FortiGuard.
            source_ip6: Source IPv6 address used to communicate with FortiGuard.
            proxy_server_ip: Hostname or IPv4 address of the proxy server.
            proxy_server_port: Port used to communicate with the proxy server.
            proxy_username: Proxy user name.
            proxy_password: Proxy user password.
            ddns_server_ip: IP address of the FortiDDNS server.
            ddns_server_ip6: IPv6 address of the FortiDDNS server.
            ddns_server_port: Port used to communicate with FortiDDNS servers.
            interface_select_method: Specify how to select outgoing interface to reach server.
            interface: Specify outgoing interface to reach server.
            vrf_select: VRF ID used for connection to server.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_fortiguard.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_fortiguard.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            fortiguard_anycast=fortiguard_anycast,
            fortiguard_anycast_source=fortiguard_anycast_source,
            protocol=protocol,
            port=port,
            load_balance_servers=load_balance_servers,
            auto_join_forticloud=auto_join_forticloud,
            update_server_location=update_server_location,
            sandbox_region=sandbox_region,
            sandbox_inline_scan=sandbox_inline_scan,
            update_ffdb=update_ffdb,
            update_uwdb=update_uwdb,
            update_dldb=update_dldb,
            update_extdb=update_extdb,
            update_build_proxy=update_build_proxy,
            persistent_connection=persistent_connection,
            auto_firmware_upgrade=auto_firmware_upgrade,
            auto_firmware_upgrade_day=auto_firmware_upgrade_day,
            auto_firmware_upgrade_delay=auto_firmware_upgrade_delay,
            auto_firmware_upgrade_start_hour=auto_firmware_upgrade_start_hour,
            auto_firmware_upgrade_end_hour=auto_firmware_upgrade_end_hour,
            FDS_license_expiring_days=FDS_license_expiring_days,
            subscribe_update_notification=subscribe_update_notification,
            antispam_force_off=antispam_force_off,
            antispam_cache=antispam_cache,
            antispam_cache_ttl=antispam_cache_ttl,
            antispam_cache_mpermille=antispam_cache_mpermille,
            antispam_license=antispam_license,
            antispam_expiration=antispam_expiration,
            antispam_timeout=antispam_timeout,
            outbreak_prevention_force_off=outbreak_prevention_force_off,
            outbreak_prevention_cache=outbreak_prevention_cache,
            outbreak_prevention_cache_ttl=outbreak_prevention_cache_ttl,
            outbreak_prevention_cache_mpermille=outbreak_prevention_cache_mpermille,
            outbreak_prevention_license=outbreak_prevention_license,
            outbreak_prevention_expiration=outbreak_prevention_expiration,
            outbreak_prevention_timeout=outbreak_prevention_timeout,
            webfilter_force_off=webfilter_force_off,
            webfilter_cache=webfilter_cache,
            webfilter_cache_ttl=webfilter_cache_ttl,
            webfilter_license=webfilter_license,
            webfilter_expiration=webfilter_expiration,
            webfilter_timeout=webfilter_timeout,
            sdns_server_ip=sdns_server_ip,
            sdns_server_port=sdns_server_port,
            anycast_sdns_server_ip=anycast_sdns_server_ip,
            anycast_sdns_server_port=anycast_sdns_server_port,
            sdns_options=sdns_options,
            source_ip=source_ip,
            source_ip6=source_ip6,
            proxy_server_ip=proxy_server_ip,
            proxy_server_port=proxy_server_port,
            proxy_username=proxy_username,
            proxy_password=proxy_password,
            ddns_server_ip=ddns_server_ip,
            ddns_server_ip6=ddns_server_ip6,
            ddns_server_port=ddns_server_port,
            interface_select_method=interface_select_method,
            interface=interface,
            vrf_select=vrf_select,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.fortiguard import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/fortiguard",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/system/fortiguard"

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
            "cmdb", endpoint, data=payload_data, params=params, vdom=False        )





    # ========================================================================
    # Action: Move
    # ========================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/fortiguard object to a new position.
        
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
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.system_fortiguard.move(
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
            all_objects = self.get()
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
            all_objects = self.get()
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
        endpoint = "/system/fortiguard/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )





