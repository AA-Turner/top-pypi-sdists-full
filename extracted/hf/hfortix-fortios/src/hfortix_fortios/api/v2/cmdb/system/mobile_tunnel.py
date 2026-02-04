"""
FortiOS CMDB - System mobile_tunnel

Configuration endpoint for managing cmdb system/mobile_tunnel objects.

API Endpoints:
    GET    /cmdb/system/mobile_tunnel
    POST   /cmdb/system/mobile_tunnel
    PUT    /cmdb/system/mobile_tunnel/{identifier}
    DELETE /cmdb/system/mobile_tunnel/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_mobile_tunnel.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_mobile_tunnel.post(
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

class MobileTunnel(CRUDEndpoint, MetadataMixin):
    """MobileTunnel Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "mobile_tunnel"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "network": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
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
        """Initialize MobileTunnel endpoint."""
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
        Retrieve system/mobile_tunnel configuration.

        Configure Mobile tunnels, an implementation of Network Mobility (NEMO) extensions for Mobile IPv4 RFC5177.

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
            >>> # Get all system/mobile_tunnel objects
            >>> result = fgt.api.cmdb.system_mobile_tunnel.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/mobile_tunnel by name
            >>> result = fgt.api.cmdb.system_mobile_tunnel.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_mobile_tunnel.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_mobile_tunnel.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_mobile_tunnel.get_schema()

        See Also:
            - post(): Create new system/mobile_tunnel object
            - put(): Update existing system/mobile_tunnel object
            - delete(): Remove system/mobile_tunnel object
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
            endpoint = "/system/mobile-tunnel/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/system/mobile-tunnel"
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
            >>> schema = fgt.api.cmdb.system_mobile_tunnel.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_mobile_tunnel.get_schema(format="json-schema")
        
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
        status: Literal["disable", "enable"] | None = None,
        roaming_interface: str | None = None,
        home_agent: str | None = None,
        home_address: str | None = None,
        renew_interval: int | None = None,
        lifetime: int | None = None,
        reg_interval: int | None = None,
        reg_retry: int | None = None,
        n_mhae_spi: int | None = None,
        n_mhae_key_type: Literal["ascii", "base64"] | None = None,
        n_mhae_key: Any | None = None,
        hash_algorithm: Literal["hmac-md5"] | None = None,
        tunnel_mode: Literal["gre"] | None = None,
        network: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/mobile_tunnel object.

        Configure Mobile tunnels, an implementation of Network Mobility (NEMO) extensions for Mobile IPv4 RFC5177.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Tunnel name.
            status: Enable/disable this mobile tunnel.
            roaming_interface: Select the associated interface name from available options.
            home_agent: IPv4 address of the NEMO HA (Format: xxx.xxx.xxx.xxx).
            home_address: Home IP address (Format: xxx.xxx.xxx.xxx).
            renew_interval: Time before lifetime expiration to send NMMO HA re-registration (5 - 60, default = 60).
            lifetime: NMMO HA registration request lifetime (180 - 65535 sec, default = 65535).
            reg_interval: NMMO HA registration interval (5 - 300, default = 5).
            reg_retry: Maximum number of NMMO HA registration retries (1 to 30, default = 3).
            n_mhae_spi: NEMO authentication SPI (default: 256).
            n_mhae_key_type: NEMO authentication key type (ASCII or base64).
            n_mhae_key: NEMO authentication key.
            hash_algorithm: Hash Algorithm (Keyed MD5).
            tunnel_mode: NEMO tunnel mode (GRE tunnel).
            network: NEMO network configuration.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_mobile_tunnel.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_mobile_tunnel.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if network is not None:
            network = normalize_table_field(
                network,
                mkey="id",
                required_fields=['id'],
                field_name="network",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            status=status,
            roaming_interface=roaming_interface,
            home_agent=home_agent,
            home_address=home_address,
            renew_interval=renew_interval,
            lifetime=lifetime,
            reg_interval=reg_interval,
            reg_retry=reg_retry,
            n_mhae_spi=n_mhae_spi,
            n_mhae_key_type=n_mhae_key_type,
            n_mhae_key=n_mhae_key,
            hash_algorithm=hash_algorithm,
            tunnel_mode=tunnel_mode,
            network=network,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.mobile_tunnel import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/mobile_tunnel",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/system/mobile-tunnel/" + quote_path_param(name_value)

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
        status: Literal["disable", "enable"] | None = None,
        roaming_interface: str | None = None,
        home_agent: str | None = None,
        home_address: str | None = None,
        renew_interval: int | None = None,
        lifetime: int | None = None,
        reg_interval: int | None = None,
        reg_retry: int | None = None,
        n_mhae_spi: int | None = None,
        n_mhae_key_type: Literal["ascii", "base64"] | None = None,
        n_mhae_key: Any | None = None,
        hash_algorithm: Literal["hmac-md5"] | None = None,
        tunnel_mode: Literal["gre"] | None = None,
        network: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/mobile_tunnel object.

        Configure Mobile tunnels, an implementation of Network Mobility (NEMO) extensions for Mobile IPv4 RFC5177.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Tunnel name.
            status: Enable/disable this mobile tunnel.
            roaming_interface: Select the associated interface name from available options.
            home_agent: IPv4 address of the NEMO HA (Format: xxx.xxx.xxx.xxx).
            home_address: Home IP address (Format: xxx.xxx.xxx.xxx).
            renew_interval: Time before lifetime expiration to send NMMO HA re-registration (5 - 60, default = 60).
            lifetime: NMMO HA registration request lifetime (180 - 65535 sec, default = 65535).
            reg_interval: NMMO HA registration interval (5 - 300, default = 5).
            reg_retry: Maximum number of NMMO HA registration retries (1 to 30, default = 3).
            n_mhae_spi: NEMO authentication SPI (default: 256).
            n_mhae_key_type: NEMO authentication key type (ASCII or base64).
            n_mhae_key: NEMO authentication key.
            hash_algorithm: Hash Algorithm (Keyed MD5).
            tunnel_mode: NEMO tunnel mode (GRE tunnel).
            network: NEMO network configuration.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_mobile_tunnel.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = MobileTunnel.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_mobile_tunnel.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(MobileTunnel.required_fields()) }}
            
            Use MobileTunnel.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if network is not None:
            network = normalize_table_field(
                network,
                mkey="id",
                required_fields=['id'],
                field_name="network",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            status=status,
            roaming_interface=roaming_interface,
            home_agent=home_agent,
            home_address=home_address,
            renew_interval=renew_interval,
            lifetime=lifetime,
            reg_interval=reg_interval,
            reg_retry=reg_retry,
            n_mhae_spi=n_mhae_spi,
            n_mhae_key_type=n_mhae_key_type,
            n_mhae_key=n_mhae_key,
            hash_algorithm=hash_algorithm,
            tunnel_mode=tunnel_mode,
            network=network,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.mobile_tunnel import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/mobile_tunnel",
            )

        endpoint = "/system/mobile-tunnel"
        
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
        Delete system/mobile_tunnel object.

        Configure Mobile tunnels, an implementation of Network Mobility (NEMO) extensions for Mobile IPv4 RFC5177.

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
            >>> result = fgt.api.cmdb.system_mobile_tunnel.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/system/mobile-tunnel/" + quote_path_param(name)

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
        Check if system/mobile_tunnel object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_mobile_tunnel.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_mobile_tunnel.exists(name=1):
            ...     fgt.api.cmdb.system_mobile_tunnel.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system/mobile-tunnel"
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
        status: Literal["disable", "enable"] | None = None,
        roaming_interface: str | None = None,
        home_agent: str | None = None,
        home_address: str | None = None,
        renew_interval: int | None = None,
        lifetime: int | None = None,
        reg_interval: int | None = None,
        reg_retry: int | None = None,
        n_mhae_spi: int | None = None,
        n_mhae_key_type: Literal["ascii", "base64"] | None = None,
        n_mhae_key: Any | None = None,
        hash_algorithm: Literal["hmac-md5"] | None = None,
        tunnel_mode: Literal["gre"] | None = None,
        network: str | list[str] | list[dict[str, Any]] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/mobile_tunnel object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            status: Field status
            roaming_interface: Field roaming-interface
            home_agent: Field home-agent
            home_address: Field home-address
            renew_interval: Field renew-interval
            lifetime: Field lifetime
            reg_interval: Field reg-interval
            reg_retry: Field reg-retry
            n_mhae_spi: Field n-mhae-spi
            n_mhae_key_type: Field n-mhae-key-type
            n_mhae_key: Field n-mhae-key
            hash_algorithm: Field hash-algorithm
            tunnel_mode: Field tunnel-mode
            network: Field network
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_mobile_tunnel.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_mobile_tunnel.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_mobile_tunnel.set(payload_dict=obj_data)
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
        if network is not None:
            network = normalize_table_field(
                network,
                mkey="id",
                required_fields=['id'],
                field_name="network",
                example="[{'id': 1}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            status=status,
            roaming_interface=roaming_interface,
            home_agent=home_agent,
            home_address=home_address,
            renew_interval=renew_interval,
            lifetime=lifetime,
            reg_interval=reg_interval,
            reg_retry=reg_retry,
            n_mhae_spi=n_mhae_spi,
            n_mhae_key_type=n_mhae_key_type,
            n_mhae_key=n_mhae_key,
            hash_algorithm=hash_algorithm,
            tunnel_mode=tunnel_mode,
            network=network,
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
        Move system/mobile_tunnel object to a new position.
        
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
            >>> fgt.api.cmdb.system_mobile_tunnel.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.system_mobile_tunnel.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.system_mobile_tunnel.move(
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
        endpoint = "/system/mobile-tunnel/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





