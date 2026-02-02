"""
FortiOS CMDB - System central_management

Configuration endpoint for managing cmdb system/central_management objects.

API Endpoints:
    GET    /cmdb/system/central_management
    POST   /cmdb/system/central_management
    PUT    /cmdb/system/central_management/{identifier}
    DELETE /cmdb/system/central_management/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_central_management.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_central_management.post(
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

class CentralManagement(CRUDEndpoint, MetadataMixin):
    """CentralManagement Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "central_management"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "server_list": {
            "mkey": "id",
            "required_fields": ['server-type', 'server-address', 'server-address6', 'fqdn'],
            "example": "[{'server-type': 'update', 'server-address': '192.168.1.10', 'server-address6': 'value', 'fqdn': 'value'}]",
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
    SUPPORTS_CLONE = True
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize CentralManagement endpoint."""
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
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve system/central_management configuration.

        Configure central management.

        Args:
            name: Name identifier to retrieve specific object. If None, returns all objects.
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
            >>> # Get all system/central_management objects
            >>> result = fgt.api.cmdb.system_central_management.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_central_management.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_central_management.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_central_management.get_schema()

        See Also:
            - post(): Create new system/central_management object
            - put(): Update existing system/central_management object
            - delete(): Remove system/central_management object
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
            endpoint = f"/system/central-management/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/system/central-management"
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
            >>> schema = fgt.api.cmdb.system_central_management.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_central_management.get_schema(format="json-schema")
        
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
        mode: Literal["normal", "backup"] | None = None,
        type: Literal["fortimanager", "fortiguard", "none"] | None = None,
        fortigate_cloud_sso_default_profile: str | None = None,
        schedule_config_restore: Literal["enable", "disable"] | None = None,
        schedule_script_restore: Literal["enable", "disable"] | None = None,
        allow_push_configuration: Literal["enable", "disable"] | None = None,
        allow_push_firmware: Literal["enable", "disable"] | None = None,
        allow_remote_firmware_upgrade: Literal["enable", "disable"] | None = None,
        allow_monitor: Literal["enable", "disable"] | None = None,
        serial_number: str | None = None,
        fmg: str | None = None,
        fmg_source_ip: str | None = None,
        fmg_source_ip6: str | None = None,
        local_cert: str | None = None,
        ca_cert: str | None = None,
        server_list: str | list[str] | list[dict[str, Any]] | None = None,
        fmg_update_port: Literal["8890", "443"] | None = None,
        fmg_update_http_header: Literal["enable", "disable"] | None = None,
        include_default_servers: Literal["enable", "disable"] | None = None,
        enc_algorithm: Literal["default", "high", "low"] | None = None,
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
        Update existing system/central_management object.

        Configure central management.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            mode: Central management mode.
            type: Central management type.
            fortigate_cloud_sso_default_profile: Override access profile. Permission is set to read-only without a FortiGate Cloud Central Management license.
            schedule_config_restore: Enable/disable allowing the central management server to restore the configuration of this FortiGate.
            schedule_script_restore: Enable/disable allowing the central management server to restore the scripts stored on this FortiGate.
            allow_push_configuration: Enable/disable allowing the central management server to push configuration changes to this FortiGate.
            allow_push_firmware: Enable/disable allowing the central management server to push firmware updates to this FortiGate.
            allow_remote_firmware_upgrade: Enable/disable remotely upgrading the firmware on this FortiGate from the central management server.
            allow_monitor: Enable/disable allowing the central management server to remotely monitor this FortiGate unit.
            serial_number: Serial number.
            fmg: IP address or FQDN of the FortiManager.
            fmg_source_ip: IPv4 source address that this FortiGate uses when communicating with FortiManager.
            fmg_source_ip6: IPv6 source address that this FortiGate uses when communicating with FortiManager.
            local_cert: Certificate to be used by FGFM protocol.
            ca_cert: CA certificate to be used by FGFM protocol.
            vdom: Virtual domain (VDOM) name to use when communicating with FortiManager.
            server_list: Additional severs that the FortiGate can use for updates (for AV, IPS, updates) and ratings (for web filter and antispam ratings) servers.
                Default format: [{'server-type': 'update', 'server-address': '192.168.1.10', 'server-address6': 'value', 'fqdn': 'value'}]
                Required format: List of dicts with keys: server-type, server-address, server-address6, fqdn
                  (String format not allowed due to multiple required fields)
            fmg_update_port: Port used to communicate with FortiManager that is acting as a FortiGuard update server.
            fmg_update_http_header: Enable/disable inclusion of HTTP header in update request.
            include_default_servers: Enable/disable inclusion of public FortiGuard servers in the override server list.
            enc_algorithm: Encryption strength for communications between the FortiGate and central management.
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
            >>> result = fgt.api.cmdb.system_central_management.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_central_management.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if server_list is not None:
            server_list = normalize_table_field(
                server_list,
                mkey="id",
                required_fields=['server-type', 'server-address', 'server-address6', 'fqdn'],
                field_name="server_list",
                example="[{'server-type': 'update', 'server-address': '192.168.1.10', 'server-address6': 'value', 'fqdn': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            mode=mode,
            type=type,
            fortigate_cloud_sso_default_profile=fortigate_cloud_sso_default_profile,
            schedule_config_restore=schedule_config_restore,
            schedule_script_restore=schedule_script_restore,
            allow_push_configuration=allow_push_configuration,
            allow_push_firmware=allow_push_firmware,
            allow_remote_firmware_upgrade=allow_remote_firmware_upgrade,
            allow_monitor=allow_monitor,
            serial_number=serial_number,
            fmg=fmg,
            fmg_source_ip=fmg_source_ip,
            fmg_source_ip6=fmg_source_ip6,
            local_cert=local_cert,
            ca_cert=ca_cert,
            server_list=server_list,
            fmg_update_port=fmg_update_port,
            fmg_update_http_header=fmg_update_http_header,
            include_default_servers=include_default_servers,
            enc_algorithm=enc_algorithm,
            interface_select_method=interface_select_method,
            interface=interface,
            vrf_select=vrf_select,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.central_management import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/central_management",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/system/central-management"

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
        action: Literal["before", "after"],
        reference_name: str,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/central_management object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            name: Name of object to move
            action: Move "before" or "after" reference object
            reference_name: Name of reference object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.system_central_management.move(
            ...     name="object1",
            ...     action="before",
            ...     reference_name="object2"
            ... )
        """
        # Build params for move operation
        params = {
            "name": name,
            "action": "move",
            action: reference_name,
            **kwargs,
        }
        
        endpoint = "/system/central-management"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        name: str,
        new_name: str,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone system/central_management object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            name: Name of object to clone
            new_name: Name for the cloned object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.system_central_management.clone(
            ...     name="template",
            ...     new_name="new-from-template"
            ... )
        """
        # Build params for clone operation  
        params = {
            "name": name,
            "new_name": new_name,
            "action": "clone",
            **kwargs,
        }
        
        endpoint = "/system/central-management"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )




