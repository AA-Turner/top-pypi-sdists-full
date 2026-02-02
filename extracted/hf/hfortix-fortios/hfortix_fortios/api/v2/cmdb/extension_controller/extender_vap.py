"""
FortiOS CMDB - Extension_controller extender_vap

Configuration endpoint for managing cmdb extension_controller/extender_vap objects.

API Endpoints:
    GET    /cmdb/extension_controller/extender_vap
    POST   /cmdb/extension_controller/extender_vap
    PUT    /cmdb/extension_controller/extender_vap/{identifier}
    DELETE /cmdb/extension_controller/extender_vap/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.extension_controller_extender_vap.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.extension_controller_extender_vap.post(
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

class ExtenderVap(CRUDEndpoint, MetadataMixin):
    """ExtenderVap Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "extender_vap"
    
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
        """Initialize ExtenderVap endpoint."""
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
        Retrieve extension_controller/extender_vap configuration.

        FortiExtender wifi vap configuration.

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
            >>> # Get all extension_controller/extender_vap objects
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific extension_controller/extender_vap by name
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.extension_controller_extender_vap.get_schema()

        See Also:
            - post(): Create new extension_controller/extender_vap object
            - put(): Update existing extension_controller/extender_vap object
            - delete(): Remove extension_controller/extender_vap object
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
            endpoint = "/extension-controller/extender-vap/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/extension-controller/extender-vap"
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
            >>> schema = fgt.api.cmdb.extension_controller_extender_vap.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.extension_controller_extender_vap.get_schema(format="json-schema")
        
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
        type: Literal["local-vap", "lan-ext-vap"] | None = None,
        ssid: str | None = None,
        max_clients: int | None = None,
        broadcast_ssid: Literal["disable", "enable"] | None = None,
        security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"] | None = None,
        dtim: int | None = None,
        rts_threshold: int | None = None,
        pmf: Literal["disabled", "optional", "required"] | None = None,
        target_wake_time: Literal["disable", "enable"] | None = None,
        bss_color_partial: Literal["disable", "enable"] | None = None,
        mu_mimo: Literal["disable", "enable"] | None = None,
        passphrase: Any | None = None,
        sae_password: Any | None = None,
        auth_server_address: str | None = None,
        auth_server_port: int | None = None,
        auth_server_secret: str | None = None,
        ip_address: Any | None = None,
        start_ip: str | None = None,
        end_ip: str | None = None,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing extension_controller/extender_vap object.

        FortiExtender wifi vap configuration.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Wi-Fi VAP name.
            type: Wi-Fi VAP type local-vap / lan-extension-vap.
            ssid: Wi-Fi SSID.
            max_clients: Wi-Fi max clients (0 - 512), default = 0 (no limit) 
            broadcast_ssid: Wi-Fi broadcast SSID enable / disable.
            security: Wi-Fi security.
            dtim: Wi-Fi DTIM (1 - 255) default = 1.
            rts_threshold: Wi-Fi RTS Threshold (256 - 2347), default = 2347 (RTS/CTS disabled).
            pmf: Wi-Fi pmf enable/disable, default = disable.
            target_wake_time: Wi-Fi 802.11AX target wake time enable / disable, default = enable.
            bss_color_partial: Wi-Fi 802.11AX bss color partial enable / disable, default = enable.
            mu_mimo: Wi-Fi multi-user MIMO enable / disable, default = enable.
            passphrase: Wi-Fi passphrase.
            sae_password: Wi-Fi SAE Password.
            auth_server_address: Wi-Fi Authentication Server Address (IPv4 format).
            auth_server_port: Wi-Fi Authentication Server Port.
            auth_server_secret: Wi-Fi Authentication Server Secret.
            ip_address: Extender ip address.
            start_ip: Start ip address.
            end_ip: End ip address.
            allowaccess: Control management access to the managed extender. Separate entries with a space.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.put(payload_dict=payload)

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
            name=name,
            type=type,
            ssid=ssid,
            max_clients=max_clients,
            broadcast_ssid=broadcast_ssid,
            security=security,
            dtim=dtim,
            rts_threshold=rts_threshold,
            pmf=pmf,
            target_wake_time=target_wake_time,
            bss_color_partial=bss_color_partial,
            mu_mimo=mu_mimo,
            passphrase=passphrase,
            sae_password=sae_password,
            auth_server_address=auth_server_address,
            auth_server_port=auth_server_port,
            auth_server_secret=auth_server_secret,
            ip_address=ip_address,
            start_ip=start_ip,
            end_ip=end_ip,
            allowaccess=allowaccess,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.extender_vap import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/extension_controller/extender_vap",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/extension-controller/extender-vap/" + quote_path_param(name_value)

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
        type: Literal["local-vap", "lan-ext-vap"] | None = None,
        ssid: str | None = None,
        max_clients: int | None = None,
        broadcast_ssid: Literal["disable", "enable"] | None = None,
        security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"] | None = None,
        dtim: int | None = None,
        rts_threshold: int | None = None,
        pmf: Literal["disabled", "optional", "required"] | None = None,
        target_wake_time: Literal["disable", "enable"] | None = None,
        bss_color_partial: Literal["disable", "enable"] | None = None,
        mu_mimo: Literal["disable", "enable"] | None = None,
        passphrase: Any | None = None,
        sae_password: Any | None = None,
        auth_server_address: str | None = None,
        auth_server_port: int | None = None,
        auth_server_secret: str | None = None,
        ip_address: Any | None = None,
        start_ip: str | None = None,
        end_ip: str | None = None,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new extension_controller/extender_vap object.

        FortiExtender wifi vap configuration.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Wi-Fi VAP name.
            type: Wi-Fi VAP type local-vap / lan-extension-vap.
            ssid: Wi-Fi SSID.
            max_clients: Wi-Fi max clients (0 - 512), default = 0 (no limit) 
            broadcast_ssid: Wi-Fi broadcast SSID enable / disable.
            security: Wi-Fi security.
            dtim: Wi-Fi DTIM (1 - 255) default = 1.
            rts_threshold: Wi-Fi RTS Threshold (256 - 2347), default = 2347 (RTS/CTS disabled).
            pmf: Wi-Fi pmf enable/disable, default = disable.
            target_wake_time: Wi-Fi 802.11AX target wake time enable / disable, default = enable.
            bss_color_partial: Wi-Fi 802.11AX bss color partial enable / disable, default = enable.
            mu_mimo: Wi-Fi multi-user MIMO enable / disable, default = enable.
            passphrase: Wi-Fi passphrase.
            sae_password: Wi-Fi SAE Password.
            auth_server_address: Wi-Fi Authentication Server Address (IPv4 format).
            auth_server_port: Wi-Fi Authentication Server Port.
            auth_server_secret: Wi-Fi Authentication Server Secret.
            ip_address: Extender ip address.
            start_ip: Start ip address.
            end_ip: End ip address.
            allowaccess: Control management access to the managed extender. Separate entries with a space.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = ExtenderVap.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(ExtenderVap.required_fields()) }}
            
            Use ExtenderVap.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            type=type,
            ssid=ssid,
            max_clients=max_clients,
            broadcast_ssid=broadcast_ssid,
            security=security,
            dtim=dtim,
            rts_threshold=rts_threshold,
            pmf=pmf,
            target_wake_time=target_wake_time,
            bss_color_partial=bss_color_partial,
            mu_mimo=mu_mimo,
            passphrase=passphrase,
            sae_password=sae_password,
            auth_server_address=auth_server_address,
            auth_server_port=auth_server_port,
            auth_server_secret=auth_server_secret,
            ip_address=ip_address,
            start_ip=start_ip,
            end_ip=end_ip,
            allowaccess=allowaccess,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.extender_vap import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/extension_controller/extender_vap",
            )

        endpoint = "/extension-controller/extender-vap"
        
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
        Delete extension_controller/extender_vap object.

        FortiExtender wifi vap configuration.

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
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/extension-controller/extender-vap/" + quote_path_param(name)

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
        Check if extension_controller/extender_vap object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.extension_controller_extender_vap.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.extension_controller_extender_vap.exists(name=1):
            ...     fgt.api.cmdb.extension_controller_extender_vap.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/extension-controller/extender-vap"
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
        type: Literal["local-vap", "lan-ext-vap"] | None = None,
        ssid: str | None = None,
        max_clients: int | None = None,
        broadcast_ssid: Literal["disable", "enable"] | None = None,
        security: Literal["OPEN", "WPA2-Personal", "WPA-WPA2-Personal", "WPA3-SAE", "WPA3-SAE-Transition", "WPA2-Enterprise", "WPA3-Enterprise-only", "WPA3-Enterprise-transition", "WPA3-Enterprise-192-bit"] | None = None,
        dtim: int | None = None,
        rts_threshold: int | None = None,
        pmf: Literal["disabled", "optional", "required"] | None = None,
        target_wake_time: Literal["disable", "enable"] | None = None,
        bss_color_partial: Literal["disable", "enable"] | None = None,
        mu_mimo: Literal["disable", "enable"] | None = None,
        passphrase: Any | None = None,
        sae_password: Any | None = None,
        auth_server_address: str | None = None,
        auth_server_port: int | None = None,
        auth_server_secret: str | None = None,
        ip_address: Any | None = None,
        start_ip: str | None = None,
        end_ip: str | None = None,
        allowaccess: Literal["ping", "telnet", "http", "https", "ssh", "snmp"] | list[str] | list[dict[str, Any]] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update extension_controller/extender_vap object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            type: Field type
            ssid: Field ssid
            max_clients: Field max-clients
            broadcast_ssid: Field broadcast-ssid
            security: Field security
            dtim: Field dtim
            rts_threshold: Field rts-threshold
            pmf: Field pmf
            target_wake_time: Field target-wake-time
            bss_color_partial: Field bss-color-partial
            mu_mimo: Field mu-mimo
            passphrase: Field passphrase
            sae_password: Field sae-password
            auth_server_address: Field auth-server-address
            auth_server_port: Field auth-server-port
            auth_server_secret: Field auth-server-secret
            ip_address: Field ip-address
            start_ip: Field start-ip
            end_ip: Field end-ip
            allowaccess: Field allowaccess
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.extension_controller_extender_vap.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.extension_controller_extender_vap.set(payload_dict=obj_data)
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
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            type=type,
            ssid=ssid,
            max_clients=max_clients,
            broadcast_ssid=broadcast_ssid,
            security=security,
            dtim=dtim,
            rts_threshold=rts_threshold,
            pmf=pmf,
            target_wake_time=target_wake_time,
            bss_color_partial=bss_color_partial,
            mu_mimo=mu_mimo,
            passphrase=passphrase,
            sae_password=sae_password,
            auth_server_address=auth_server_address,
            auth_server_port=auth_server_port,
            auth_server_secret=auth_server_secret,
            ip_address=ip_address,
            start_ip=start_ip,
            end_ip=end_ip,
            allowaccess=allowaccess,
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
        Move extension_controller/extender_vap object to a new position.
        
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
            >>> fgt.api.cmdb.extension_controller_extender_vap.move(
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
        
        endpoint = "/extension-controller/extender-vap"
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
        Clone extension_controller/extender_vap object.
        
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
            >>> fgt.api.cmdb.extension_controller_extender_vap.clone(
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
        
        endpoint = "/extension-controller/extender-vap"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




