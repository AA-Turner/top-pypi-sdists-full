"""
FortiOS CMDB - System sdn_vpn

Configuration endpoint for managing cmdb system/sdn_vpn objects.

API Endpoints:
    GET    /cmdb/system/sdn_vpn
    POST   /cmdb/system/sdn_vpn
    PUT    /cmdb/system/sdn_vpn/{identifier}
    DELETE /cmdb/system/sdn_vpn/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_sdn_vpn.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_sdn_vpn.post(
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

class SdnVpn(CRUDEndpoint, MetadataMixin):
    """SdnVpn Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "sdn_vpn"
    
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
        """Initialize SdnVpn endpoint."""
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
        Retrieve system/sdn_vpn configuration.

        Configure public cloud VPN service.

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
            >>> # Get all system/sdn_vpn objects
            >>> result = fgt.api.cmdb.system_sdn_vpn.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/sdn_vpn by name
            >>> result = fgt.api.cmdb.system_sdn_vpn.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_sdn_vpn.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_sdn_vpn.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_sdn_vpn.get_schema()

        See Also:
            - post(): Create new system/sdn_vpn object
            - put(): Update existing system/sdn_vpn object
            - delete(): Remove system/sdn_vpn object
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
            endpoint = "/system/sdn-vpn/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/system/sdn-vpn"
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
            >>> schema = fgt.api.cmdb.system_sdn_vpn.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_sdn_vpn.get_schema(format="json-schema")
        
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
        name: str | None = None,
        sdn: str | None = None,
        remote_type: Literal["vgw", "tgw"] | None = None,
        routing_type: Literal["static", "dynamic"] | None = None,
        vgw_id: str | None = None,
        tgw_id: str | None = None,
        subnet_id: str | None = None,
        bgp_as: int | None = None,
        cgw_gateway: str | None = None,
        nat_traversal: Literal["disable", "enable"] | None = None,
        tunnel_interface: str | None = None,
        internal_interface: str | None = None,
        local_cidr: str | None = None,
        remote_cidr: str | None = None,
        cgw_name: str | None = None,
        psksecret: Any | None = None,
        type: int | None = None,
        status: int | None = None,
        code: int | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/sdn_vpn object.

        Configure public cloud VPN service.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Public cloud VPN name.
            sdn: SDN connector name.
            remote_type: Type of remote device.
            routing_type: Type of routing.
            vgw_id: Virtual private gateway id.
            tgw_id: Transit gateway id.
            subnet_id: AWS subnet id for TGW route propagation.
            bgp_as: BGP Router AS number.
            cgw_gateway: Public IP address of the customer gateway.
            nat_traversal: Enable/disable use for NAT traversal. Please enable if your FortiGate device is behind a NAT/PAT device.
            tunnel_interface: Tunnel interface with public IP.
            internal_interface: Internal interface with local subnet.
            local_cidr: Local subnet address and subnet mask.
            remote_cidr: Remote subnet address and subnet mask.
            cgw_name: AWS customer gateway name to be created.
            psksecret: Pre-shared secret for PSK authentication. Auto-generated if not specified
            type: SDN VPN type.
            status: SDN VPN status.
            code: SDN VPN error code.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_sdn_vpn.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_sdn_vpn.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            sdn=sdn,
            remote_type=remote_type,
            routing_type=routing_type,
            vgw_id=vgw_id,
            tgw_id=tgw_id,
            subnet_id=subnet_id,
            bgp_as=bgp_as,
            cgw_gateway=cgw_gateway,
            nat_traversal=nat_traversal,
            tunnel_interface=tunnel_interface,
            internal_interface=internal_interface,
            local_cidr=local_cidr,
            remote_cidr=remote_cidr,
            cgw_name=cgw_name,
            psksecret=psksecret,
            type=type,
            status=status,
            code=code,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.sdn_vpn import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/sdn_vpn",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/system/sdn-vpn/" + quote_path_param(name_value)

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
    # POST Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def post(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        name: str | None = None,
        sdn: str | None = None,
        remote_type: Literal["vgw", "tgw"] | None = None,
        routing_type: Literal["static", "dynamic"] | None = None,
        vgw_id: str | None = None,
        tgw_id: str | None = None,
        subnet_id: str | None = None,
        bgp_as: int | None = None,
        cgw_gateway: str | None = None,
        nat_traversal: Literal["disable", "enable"] | None = None,
        tunnel_interface: str | None = None,
        internal_interface: str | None = None,
        local_cidr: str | None = None,
        remote_cidr: str | None = None,
        cgw_name: str | None = None,
        psksecret: Any | None = None,
        type: int | None = None,
        status: int | None = None,
        code: int | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/sdn_vpn object.

        Configure public cloud VPN service.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Public cloud VPN name.
            sdn: SDN connector name.
            remote_type: Type of remote device.
            routing_type: Type of routing.
            vgw_id: Virtual private gateway id.
            tgw_id: Transit gateway id.
            subnet_id: AWS subnet id for TGW route propagation.
            bgp_as: BGP Router AS number.
            cgw_gateway: Public IP address of the customer gateway.
            nat_traversal: Enable/disable use for NAT traversal. Please enable if your FortiGate device is behind a NAT/PAT device.
            tunnel_interface: Tunnel interface with public IP.
            internal_interface: Internal interface with local subnet.
            local_cidr: Local subnet address and subnet mask.
            remote_cidr: Remote subnet address and subnet mask.
            cgw_name: AWS customer gateway name to be created.
            psksecret: Pre-shared secret for PSK authentication. Auto-generated if not specified
            type: SDN VPN type.
            status: SDN VPN status.
            code: SDN VPN error code.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_sdn_vpn.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = SdnVpn.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_sdn_vpn.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(SdnVpn.required_fields()) }}
            
            Use SdnVpn.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            sdn=sdn,
            remote_type=remote_type,
            routing_type=routing_type,
            vgw_id=vgw_id,
            tgw_id=tgw_id,
            subnet_id=subnet_id,
            bgp_as=bgp_as,
            cgw_gateway=cgw_gateway,
            nat_traversal=nat_traversal,
            tunnel_interface=tunnel_interface,
            internal_interface=internal_interface,
            local_cidr=local_cidr,
            remote_cidr=remote_cidr,
            cgw_name=cgw_name,
            psksecret=psksecret,
            type=type,
            status=status,
            code=code,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.sdn_vpn import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/sdn_vpn",
            )

        endpoint = "/system/sdn-vpn"
        
        # Add explicit query parameters for POST
        params: dict[str, Any] = {}
        if q_action is not None:
            params["action"] = q_action
        if q_nkey is not None:
            params["nkey"] = q_nkey
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, params=params, vdom=False        )

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
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete system/sdn_vpn object.

        Configure public cloud VPN service.

        Args:
            name: Primary key identifier
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.system_sdn_vpn.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/system/sdn-vpn/" + quote_path_param(name)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=False        )

    def exists(
        self,
        name: str,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if system/sdn_vpn object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_sdn_vpn.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_sdn_vpn.exists(name=1):
            ...     fgt.api.cmdb.system_sdn_vpn.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system/sdn-vpn"
        endpoint = f"{endpoint}/{quote_path_param(name)}"
        
        try:
            result = self.get(name=name)
            
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
        sdn: str | None = None,
        remote_type: Literal["vgw", "tgw"] | None = None,
        routing_type: Literal["static", "dynamic"] | None = None,
        vgw_id: str | None = None,
        tgw_id: str | None = None,
        subnet_id: str | None = None,
        bgp_as: int | None = None,
        cgw_gateway: str | None = None,
        nat_traversal: Literal["disable", "enable"] | None = None,
        tunnel_interface: str | None = None,
        internal_interface: str | None = None,
        local_cidr: str | None = None,
        remote_cidr: str | None = None,
        cgw_name: str | None = None,
        psksecret: Any | None = None,
        type: int | None = None,
        status: int | None = None,
        code: int | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/sdn_vpn object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            sdn: Field sdn
            remote_type: Field remote-type
            routing_type: Field routing-type
            vgw_id: Field vgw-id
            tgw_id: Field tgw-id
            subnet_id: Field subnet-id
            bgp_as: Field bgp-as
            cgw_gateway: Field cgw-gateway
            nat_traversal: Field nat-traversal
            tunnel_interface: Field tunnel-interface
            internal_interface: Field internal-interface
            local_cidr: Field local-cidr
            remote_cidr: Field remote-cidr
            cgw_name: Field cgw-name
            psksecret: Field psksecret
            type: Field type
            status: Field status
            code: Field code
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_sdn_vpn.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_sdn_vpn.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_sdn_vpn.set(payload_dict=obj_data)
            >>> # Safely applies configuration regardless of current state

        Note:
            This method internally calls exists() then either post() or put().
            For performance-critical code with known state, call post() or put() directly.

        See Also:
            - post(): Create new object
            - put(): Update existing object
            - exists(): Check existence manually
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            sdn=sdn,
            remote_type=remote_type,
            routing_type=routing_type,
            vgw_id=vgw_id,
            tgw_id=tgw_id,
            subnet_id=subnet_id,
            bgp_as=bgp_as,
            cgw_gateway=cgw_gateway,
            nat_traversal=nat_traversal,
            tunnel_interface=tunnel_interface,
            internal_interface=internal_interface,
            local_cidr=local_cidr,
            remote_cidr=remote_cidr,
            cgw_name=cgw_name,
            psksecret=psksecret,
            type=type,
            status=status,
            code=code,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("name")
        if not mkey_value:
            raise ValueError("name is required for set()")
        
        # Check if resource exists
        if self.exists(name=mkey_value):
            # Update existing resource
            return self.put(payload_dict=payload_data, **kwargs)
        else:
            # Create new resource
            return self.post(payload_dict=payload_data, **kwargs)

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
        Move system/sdn_vpn object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            name: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_name: Identifier of reference object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.system_sdn_vpn.move(
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
            **kwargs,
        }
        
        endpoint = "/system/sdn-vpn"
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
        Clone system/sdn_vpn object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            name: Identifier of object to clone
            new_name: Identifier for the cloned object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.system_sdn_vpn.clone(
            ...     name=1,
            ...     new_name=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "name": name,
            "new_name": new_name,
            "action": "clone",
            **kwargs,
        }
        
        endpoint = "/system/sdn-vpn"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )




