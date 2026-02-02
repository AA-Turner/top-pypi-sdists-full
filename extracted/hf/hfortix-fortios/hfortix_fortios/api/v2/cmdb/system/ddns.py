"""
FortiOS CMDB - System ddns

Configuration endpoint for managing cmdb system/ddns objects.

API Endpoints:
    GET    /cmdb/system/ddns
    POST   /cmdb/system/ddns
    PUT    /cmdb/system/ddns/{identifier}
    DELETE /cmdb/system/ddns/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_ddns.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_ddns.post(
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

class Ddns(CRUDEndpoint, MetadataMixin):
    """Ddns Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "ddns"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "ddns_server_addr": {
            "mkey": "addr",
            "required_fields": ['addr'],
            "example": "[{'addr': 'value'}]",
        },
        "monitor_interface": {
            "mkey": "interface-name",
            "required_fields": ['interface-name'],
            "example": "[{'interface-name': 'value'}]",
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
        """Initialize Ddns endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        ddnsid: int | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve system/ddns configuration.

        Configure DDNS.

        Args:
            ddnsid: Integer identifier to retrieve specific object.
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
            >>> # Get all system/ddns objects
            >>> result = fgt.api.cmdb.system_ddns.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific system/ddns by ddnsid
            >>> result = fgt.api.cmdb.system_ddns.get(ddnsid=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_ddns.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_ddns.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_ddns.get_schema()

        See Also:
            - post(): Create new system/ddns object
            - put(): Update existing system/ddns object
            - delete(): Remove system/ddns object
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
        
        if ddnsid:
            endpoint = "/system/ddns/" + quote_path_param(ddnsid)
            unwrap_single = True
        else:
            endpoint = "/system/ddns"
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
            >>> schema = fgt.api.cmdb.system_ddns.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_ddns.get_schema(format="json-schema")
        
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
        ddnsid: int | None = None,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = None,
        addr_type: Literal["ipv4", "ipv6"] | None = None,
        server_type: Literal["ipv4", "ipv6"] | None = None,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = None,
        ddns_zone: str | None = None,
        ddns_ttl: int | None = None,
        ddns_auth: Literal["disable", "tsig"] | None = None,
        ddns_keyname: str | None = None,
        ddns_key: Any | None = None,
        ddns_domain: str | None = None,
        ddns_username: str | None = None,
        ddns_sn: str | None = None,
        ddns_password: Any | None = None,
        use_public_ip: Literal["disable", "enable"] | None = None,
        update_interval: int | None = None,
        clear_text: Literal["disable", "enable"] | None = None,
        ssl_certificate: str | None = None,
        bound_ip: str | None = None,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/ddns object.

        Configure DDNS.

        Args:
            payload_dict: Object data as dict. Must include ddnsid (primary key).
            ddnsid: DDNS ID.
            ddns_server: Select a DDNS service provider.
            addr_type: Address type of interface address in DDNS update.
            server_type: Address type of the DDNS server.
            ddns_server_addr: Generic DDNS server IP/FQDN list.
                Default format: [{'addr': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'addr': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'addr': 'val1'}, ...]
                  - List of dicts: [{'addr': 'value'}] (recommended)
            ddns_zone: Zone of your domain name (for example, DDNS.com).
            ddns_ttl: Time-to-live for DDNS packets.
            ddns_auth: Enable/disable TSIG authentication for your DDNS server.
            ddns_keyname: DDNS update key name.
            ddns_key: DDNS update key (base 64 encoding).
            ddns_domain: Your fully qualified domain name. For example, yourname.ddns.com.
            ddns_username: DDNS user name.
            ddns_sn: DDNS Serial Number.
            ddns_password: DDNS password.
            use_public_ip: Enable/disable use of public IP address.
            update_interval: DDNS update interval (60 - 2592000 sec, 0 means default).
            clear_text: Enable/disable use of clear text connections.
            ssl_certificate: Name of local certificate for SSL connections.
            bound_ip: Bound IP address.
            monitor_interface: Monitored interface.
                Default format: [{'interface-name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'interface-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'interface-name': 'val1'}, ...]
                  - List of dicts: [{'interface-name': 'value'}] (recommended)
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If ddnsid is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_ddns.put(
            ...     ddnsid=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "ddnsid": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_ddns.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if ddns_server_addr is not None:
            ddns_server_addr = normalize_table_field(
                ddns_server_addr,
                mkey="addr",
                required_fields=['addr'],
                field_name="ddns_server_addr",
                example="[{'addr': 'value'}]",
            )
        if monitor_interface is not None:
            monitor_interface = normalize_table_field(
                monitor_interface,
                mkey="interface-name",
                required_fields=['interface-name'],
                field_name="monitor_interface",
                example="[{'interface-name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            ddnsid=ddnsid,
            ddns_server=ddns_server,
            addr_type=addr_type,
            server_type=server_type,
            ddns_server_addr=ddns_server_addr,
            ddns_zone=ddns_zone,
            ddns_ttl=ddns_ttl,
            ddns_auth=ddns_auth,
            ddns_keyname=ddns_keyname,
            ddns_key=ddns_key,
            ddns_domain=ddns_domain,
            ddns_username=ddns_username,
            ddns_sn=ddns_sn,
            ddns_password=ddns_password,
            use_public_ip=use_public_ip,
            update_interval=update_interval,
            clear_text=clear_text,
            ssl_certificate=ssl_certificate,
            bound_ip=bound_ip,
            monitor_interface=monitor_interface,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.ddns import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/ddns",
            )
        
        ddnsid_value = payload_data.get("ddnsid")
        if not ddnsid_value:
            raise ValueError("ddnsid is required for PUT")
        endpoint = "/system/ddns/" + quote_path_param(ddnsid_value)

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
        ddnsid: int | None = None,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = None,
        addr_type: Literal["ipv4", "ipv6"] | None = None,
        server_type: Literal["ipv4", "ipv6"] | None = None,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = None,
        ddns_zone: str | None = None,
        ddns_ttl: int | None = None,
        ddns_auth: Literal["disable", "tsig"] | None = None,
        ddns_keyname: str | None = None,
        ddns_key: Any | None = None,
        ddns_domain: str | None = None,
        ddns_username: str | None = None,
        ddns_sn: str | None = None,
        ddns_password: Any | None = None,
        use_public_ip: Literal["disable", "enable"] | None = None,
        update_interval: int | None = None,
        clear_text: Literal["disable", "enable"] | None = None,
        ssl_certificate: str | None = None,
        bound_ip: str | None = None,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new system/ddns object.

        Configure DDNS.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            ddnsid: DDNS ID.
            ddns_server: Select a DDNS service provider.
            addr_type: Address type of interface address in DDNS update.
            server_type: Address type of the DDNS server.
            ddns_server_addr: Generic DDNS server IP/FQDN list.
                Default format: [{'addr': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'addr': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'addr': 'val1'}, ...]
                  - List of dicts: [{'addr': 'value'}] (recommended)
            ddns_zone: Zone of your domain name (for example, DDNS.com).
            ddns_ttl: Time-to-live for DDNS packets.
            ddns_auth: Enable/disable TSIG authentication for your DDNS server.
            ddns_keyname: DDNS update key name.
            ddns_key: DDNS update key (base 64 encoding).
            ddns_domain: Your fully qualified domain name. For example, yourname.ddns.com.
            ddns_username: DDNS user name.
            ddns_sn: DDNS Serial Number.
            ddns_password: DDNS password.
            use_public_ip: Enable/disable use of public IP address.
            update_interval: DDNS update interval (60 - 2592000 sec, 0 means default).
            clear_text: Enable/disable use of clear text connections.
            ssl_certificate: Name of local certificate for SSL connections.
            bound_ip: Bound IP address.
            monitor_interface: Monitored interface.
                Default format: [{'interface-name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'interface-name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'interface-name': 'val1'}, ...]
                  - List of dicts: [{'interface-name': 'value'}] (recommended)
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.system_ddns.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created ddnsid: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Ddns.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.system_ddns.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Ddns.required_fields()) }}
            
            Use Ddns.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if ddns_server_addr is not None:
            ddns_server_addr = normalize_table_field(
                ddns_server_addr,
                mkey="addr",
                required_fields=['addr'],
                field_name="ddns_server_addr",
                example="[{'addr': 'value'}]",
            )
        if monitor_interface is not None:
            monitor_interface = normalize_table_field(
                monitor_interface,
                mkey="interface-name",
                required_fields=['interface-name'],
                field_name="monitor_interface",
                example="[{'interface-name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            ddnsid=ddnsid,
            ddns_server=ddns_server,
            addr_type=addr_type,
            server_type=server_type,
            ddns_server_addr=ddns_server_addr,
            ddns_zone=ddns_zone,
            ddns_ttl=ddns_ttl,
            ddns_auth=ddns_auth,
            ddns_keyname=ddns_keyname,
            ddns_key=ddns_key,
            ddns_domain=ddns_domain,
            ddns_username=ddns_username,
            ddns_sn=ddns_sn,
            ddns_password=ddns_password,
            use_public_ip=use_public_ip,
            update_interval=update_interval,
            clear_text=clear_text,
            ssl_certificate=ssl_certificate,
            bound_ip=bound_ip,
            monitor_interface=monitor_interface,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.ddns import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/ddns",
            )

        endpoint = "/system/ddns"
        
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
        ddnsid: int | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete system/ddns object.

        Configure DDNS.

        Args:
            ddnsid: Primary key identifier
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If ddnsid is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.system_ddns.delete(ddnsid=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not ddnsid:
            raise ValueError("ddnsid is required for DELETE")
        endpoint = "/system/ddns/" + quote_path_param(ddnsid)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=False        )

    def exists(
        self,
        ddnsid: int,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if system/ddns object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            ddnsid: Primary key identifier

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.system_ddns.exists(ddnsid=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.system_ddns.exists(ddnsid=1):
            ...     fgt.api.cmdb.system_ddns.delete(ddnsid=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/system/ddns"
        endpoint = f"{endpoint}/{quote_path_param(ddnsid)}"
        
        try:
            result = self.get(ddnsid=ddnsid)
            
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
        ddnsid: int | None = None,
        ddns_server: Literal["dyndns.org", "dyns.net", "tzo.com", "vavic.com", "dipdns.net", "now.net.cn", "dhs.org", "easydns.com", "genericDDNS", "FortiGuardDDNS", "noip.com"] | None = None,
        addr_type: Literal["ipv4", "ipv6"] | None = None,
        server_type: Literal["ipv4", "ipv6"] | None = None,
        ddns_server_addr: str | list[str] | list[dict[str, Any]] | None = None,
        ddns_zone: str | None = None,
        ddns_ttl: int | None = None,
        ddns_auth: Literal["disable", "tsig"] | None = None,
        ddns_keyname: str | None = None,
        ddns_key: Any | None = None,
        ddns_domain: str | None = None,
        ddns_username: str | None = None,
        ddns_sn: str | None = None,
        ddns_password: Any | None = None,
        use_public_ip: Literal["disable", "enable"] | None = None,
        update_interval: int | None = None,
        clear_text: Literal["disable", "enable"] | None = None,
        ssl_certificate: str | None = None,
        bound_ip: str | None = None,
        monitor_interface: str | list[str] | list[dict[str, Any]] | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update system/ddns object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (ddnsid) in the payload.

        Args:
            payload_dict: Resource data including ddnsid (primary key)
            ddnsid: Field ddnsid
            ddns_server: Field ddns-server
            addr_type: Field addr-type
            server_type: Field server-type
            ddns_server_addr: Field ddns-server-addr
            ddns_zone: Field ddns-zone
            ddns_ttl: Field ddns-ttl
            ddns_auth: Field ddns-auth
            ddns_keyname: Field ddns-keyname
            ddns_key: Field ddns-key
            ddns_domain: Field ddns-domain
            ddns_username: Field ddns-username
            ddns_sn: Field ddns-sn
            ddns_password: Field ddns-password
            use_public_ip: Field use-public-ip
            update_interval: Field update-interval
            clear_text: Field clear-text
            ssl_certificate: Field ssl-certificate
            bound_ip: Field bound-ip
            monitor_interface: Field monitor-interface
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If ddnsid is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.system_ddns.set(
            ...     ddnsid=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "ddnsid": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.system_ddns.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.system_ddns.set(payload_dict=obj_data)
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
        if ddns_server_addr is not None:
            ddns_server_addr = normalize_table_field(
                ddns_server_addr,
                mkey="addr",
                required_fields=['addr'],
                field_name="ddns_server_addr",
                example="[{'addr': 'value'}]",
            )
        if monitor_interface is not None:
            monitor_interface = normalize_table_field(
                monitor_interface,
                mkey="interface-name",
                required_fields=['interface-name'],
                field_name="monitor_interface",
                example="[{'interface-name': 'value'}]",
            )
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            ddnsid=ddnsid,
            ddns_server=ddns_server,
            addr_type=addr_type,
            server_type=server_type,
            ddns_server_addr=ddns_server_addr,
            ddns_zone=ddns_zone,
            ddns_ttl=ddns_ttl,
            ddns_auth=ddns_auth,
            ddns_keyname=ddns_keyname,
            ddns_key=ddns_key,
            ddns_domain=ddns_domain,
            ddns_username=ddns_username,
            ddns_sn=ddns_sn,
            ddns_password=ddns_password,
            use_public_ip=use_public_ip,
            update_interval=update_interval,
            clear_text=clear_text,
            ssl_certificate=ssl_certificate,
            bound_ip=bound_ip,
            monitor_interface=monitor_interface,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("ddnsid")
        if not mkey_value:
            raise ValueError("ddnsid is required for set()")
        
        # Check if resource exists
        if self.exists(ddnsid=mkey_value):
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
        ddnsid: int,
        action: Literal["before", "after"],
        reference_ddnsid: int,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move system/ddns object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            ddnsid: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_ddnsid: Identifier of reference object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.system_ddns.move(
            ...     ddnsid=100,
            ...     action="before",
            ...     reference_ddnsid=50
            ... )
        """
        # Build params for move operation
        params = {
            "ddnsid": ddnsid,
            "action": "move",
            action: reference_ddnsid,
            **kwargs,
        }
        
        endpoint = "/system/ddns"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        ddnsid: int,
        new_ddnsid: int,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone system/ddns object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            ddnsid: Identifier of object to clone
            new_ddnsid: Identifier for the cloned object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.system_ddns.clone(
            ...     ddnsid=1,
            ...     new_ddnsid=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "ddnsid": ddnsid,
            "new_ddnsid": new_ddnsid,
            "action": "clone",
            **kwargs,
        }
        
        endpoint = "/system/ddns"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )




