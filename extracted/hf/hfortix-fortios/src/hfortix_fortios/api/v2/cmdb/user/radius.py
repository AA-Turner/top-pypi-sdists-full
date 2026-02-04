"""
FortiOS CMDB - User radius

Configuration endpoint for managing cmdb user/radius objects.

API Endpoints:
    GET    /cmdb/user/radius
    POST   /cmdb/user/radius
    PUT    /cmdb/user/radius/{identifier}
    DELETE /cmdb/user/radius/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.user_radius.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.user_radius.post(
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

class Radius(CRUDEndpoint, MetadataMixin):
    """Radius Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "radius"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "class_": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "accounting_server": {
            "mkey": "id",
            "required_fields": ['server', 'secret', 'interface'],
            "example": "[{'server': '192.168.1.10', 'secret': 'value', 'interface': 'value'}]",
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
        """Initialize Radius endpoint."""
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
        Retrieve user/radius configuration.

        Configure RADIUS server entries.

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
            >>> # Get all user/radius objects
            >>> result = fgt.api.cmdb.user_radius.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific user/radius by name
            >>> result = fgt.api.cmdb.user_radius.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.user_radius.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.user_radius.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.user_radius.get_schema()

        See Also:
            - post(): Create new user/radius object
            - put(): Update existing user/radius object
            - delete(): Remove user/radius object
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
            endpoint = "/user/radius/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/user/radius"
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
            >>> schema = fgt.api.cmdb.user_radius.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.user_radius.get_schema(format="json-schema")
        
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
        server: str | None = None,
        secret: Any | None = None,
        secondary_server: str | None = None,
        secondary_secret: Any | None = None,
        tertiary_server: str | None = None,
        tertiary_secret: Any | None = None,
        timeout: int | None = None,
        status_ttl: int | None = None,
        all_usergroup: Literal["disable", "enable"] | None = None,
        use_management_vdom: Literal["enable", "disable"] | None = None,
        switch_controller_nas_ip_dynamic: Literal["enable", "disable"] | None = None,
        nas_ip: str | None = None,
        nas_id_type: Literal["legacy", "custom", "hostname"] | None = None,
        call_station_id_type: Literal["legacy", "IP", "MAC"] | None = None,
        nas_id: str | None = None,
        acct_interim_interval: int | None = None,
        radius_coa: Literal["enable", "disable"] | None = None,
        radius_port: int | None = None,
        h3c_compatibility: Literal["enable", "disable"] | None = None,
        auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"] | None = None,
        source_ip: str | None = None,
        source_ip_interface: str | None = None,
        username_case_sensitive: Literal["enable", "disable"] | None = None,
        group_override_attr_type: Literal["filter-Id", "class"] | None = None,
        class_: str | list[str] | list[dict[str, Any]] | None = None,
        password_renewal: Literal["enable", "disable"] | None = None,
        require_message_authenticator: Literal["enable", "disable"] | None = None,
        password_encoding: Literal["auto", "ISO-8859-1"] | None = None,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = None,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = None,
        mac_case: Literal["uppercase", "lowercase"] | None = None,
        acct_all_servers: Literal["enable", "disable"] | None = None,
        switch_controller_acct_fast_framedip_detect: int | None = None,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = None,
        interface: str | None = None,
        vrf_select: int | None = None,
        switch_controller_service_type: Literal["login", "framed", "callback-login", "callback-framed", "outbound", "administrative", "nas-prompt", "authenticate-only", "callback-nas-prompt", "call-check", "callback-administrative"] | list[str] | None = None,
        transport_protocol: Literal["udp", "tcp", "tls"] | None = None,
        tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = None,
        ca_cert: str | None = None,
        client_cert: str | None = None,
        server_identity_check: Literal["enable", "disable"] | None = None,
        account_key_processing: Literal["same", "strip"] | None = None,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = None,
        rsso: Literal["enable", "disable"] | None = None,
        rsso_radius_server_port: int | None = None,
        rsso_radius_response: Literal["enable", "disable"] | None = None,
        rsso_validate_request_secret: Literal["enable", "disable"] | None = None,
        rsso_secret: Any | None = None,
        rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        sso_attribute_key: str | None = None,
        sso_attribute_value_override: Literal["enable", "disable"] | None = None,
        rsso_context_timeout: int | None = None,
        rsso_log_period: int | None = None,
        rsso_log_flags: Literal["protocol-error", "profile-missing", "accounting-stop-missed", "accounting-event", "endpoint-block", "radiusd-other", "none"] | list[str] | None = None,
        rsso_flush_ip_session: Literal["enable", "disable"] | None = None,
        rsso_ep_one_ip_only: Literal["enable", "disable"] | None = None,
        delimiter: Literal["plus", "comma"] | None = None,
        accounting_server: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing user/radius object.

        Configure RADIUS server entries.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: RADIUS server entry name.
            server: Primary RADIUS server CN domain name or IP address.
            secret: Pre-shared secret key used to access the primary RADIUS server.
            secondary_server: Secondary RADIUS CN domain name or IP address.
            secondary_secret: Secret key to access the secondary server.
            tertiary_server: Tertiary RADIUS CN domain name or IP address.
            tertiary_secret: Secret key to access the tertiary server.
            timeout: Time in seconds to retry connecting server.
            status_ttl: Time for which server reachability is cached so that when a server is unreachable, it will not be retried for at least this period of time (0 = cache disabled, default = 300).
            all_usergroup: Enable/disable automatically including this RADIUS server in all user groups.
            use_management_vdom: Enable/disable using management VDOM to send requests.
            switch_controller_nas_ip_dynamic: Enable/Disable switch-controller nas-ip dynamic to dynamically set nas-ip.
            nas_ip: IP address used to communicate with the RADIUS server and used as NAS-IP-Address and Called-Station-ID attributes.
            nas_id_type: NAS identifier type configuration (default = legacy).
            call_station_id_type: Calling & Called station identifier type configuration (default = legacy), this option is not available for 802.1x authentication. 
            nas_id: Custom NAS identifier.
            acct_interim_interval: Time in seconds between each accounting interim update message.
            radius_coa: Enable to allow a mechanism to change the attributes of an authentication, authorization, and accounting session after it is authenticated.
            radius_port: RADIUS service port number.
            h3c_compatibility: Enable/disable compatibility with the H3C, a mechanism that performs security checking for authentication.
            auth_type: Authentication methods/protocols permitted for this RADIUS server.
            source_ip: Source IP address for communications to the RADIUS server.
            source_ip_interface: Source interface for communication with the RADIUS server.
            username_case_sensitive: Enable/disable case sensitive user names.
            group_override_attr_type: RADIUS attribute type to override user group information.
            class_: Class attribute name(s).
            password_renewal: Enable/disable password renewal.
            require_message_authenticator: Require message authenticator in authentication response.
            password_encoding: Password encoding.
            mac_username_delimiter: MAC authentication username delimiter (default = hyphen).
            mac_password_delimiter: MAC authentication password delimiter (default = hyphen).
            mac_case: MAC authentication case (default = lowercase).
            acct_all_servers: Enable/disable sending of accounting messages to all configured servers (default = disable).
            switch_controller_acct_fast_framedip_detect: Switch controller accounting message Framed-IP detection from DHCP snooping (seconds, default=2).
            interface_select_method: Specify how to select outgoing interface to reach server.
            interface: Specify outgoing interface to reach server.
            vrf_select: VRF ID used for connection to server.
            switch_controller_service_type: RADIUS service type.
            transport_protocol: Transport protocol to be used (default = udp).
            tls_min_proto_version: Minimum supported protocol version for TLS connections (default is to follow system global setting).
            ca_cert: CA of server to trust under TLS.
            client_cert: Client certificate to use under TLS.
            server_identity_check: Enable/disable RADIUS server identity check (verify server domain name/IP address against the server certificate).
            account_key_processing: Account key processing operation. The FortiGate will keep either the whole domain or strip the domain from the subject identity.
            account_key_cert_field: Define subject identity field in certificate for user access right checking.
            rsso: Enable/disable RADIUS based single sign on feature.
            rsso_radius_server_port: UDP port to listen on for RADIUS Start and Stop records.
            rsso_radius_response: Enable/disable sending RADIUS response packets after receiving Start and Stop records.
            rsso_validate_request_secret: Enable/disable validating the RADIUS request shared secret in the Start or End record.
            rsso_secret: RADIUS secret used by the RADIUS accounting server.
            rsso_endpoint_attribute: RADIUS attributes used to extract the user end point identifier from the RADIUS Start record.
            rsso_endpoint_block_attribute: RADIUS attributes used to block a user.
            sso_attribute: RADIUS attribute that contains the profile group name to be extracted from the RADIUS Start record.
            sso_attribute_key: Key prefix for SSO group value in the SSO attribute.
            sso_attribute_value_override: Enable/disable override old attribute value with new value for the same endpoint.
            rsso_context_timeout: Time in seconds before the logged out user is removed from the "user context list" of logged on users.
            rsso_log_period: Time interval in seconds that group event log messages will be generated for dynamic profile events.
            rsso_log_flags: Events to log.
            rsso_flush_ip_session: Enable/disable flushing user IP sessions on RADIUS accounting Stop messages.
            rsso_ep_one_ip_only: Enable/disable the replacement of old IP addresses with new ones for the same endpoint on RADIUS accounting Start messages.
            delimiter: Configure delimiter to be used for separating profile group names in the SSO attribute (default = plus character "+").
            accounting_server: Additional accounting servers.
                Default format: [{'server': '192.168.1.10', 'secret': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: server, secret, interface
                  (String format not allowed due to multiple required fields)
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.user_radius.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.user_radius.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if class_ is not None:
            class_ = normalize_table_field(
                class_,
                mkey="name",
                required_fields=['name'],
                field_name="class_",
                example="[{'name': 'value'}]",
            )
        if accounting_server is not None:
            accounting_server = normalize_table_field(
                accounting_server,
                mkey="id",
                required_fields=['server', 'secret', 'interface'],
                field_name="accounting_server",
                example="[{'server': '192.168.1.10', 'secret': 'value', 'interface': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            server=server,
            secret=secret,
            secondary_server=secondary_server,
            secondary_secret=secondary_secret,
            tertiary_server=tertiary_server,
            tertiary_secret=tertiary_secret,
            timeout=timeout,
            status_ttl=status_ttl,
            all_usergroup=all_usergroup,
            use_management_vdom=use_management_vdom,
            switch_controller_nas_ip_dynamic=switch_controller_nas_ip_dynamic,
            nas_ip=nas_ip,
            nas_id_type=nas_id_type,
            call_station_id_type=call_station_id_type,
            nas_id=nas_id,
            acct_interim_interval=acct_interim_interval,
            radius_coa=radius_coa,
            radius_port=radius_port,
            h3c_compatibility=h3c_compatibility,
            auth_type=auth_type,
            source_ip=source_ip,
            source_ip_interface=source_ip_interface,
            username_case_sensitive=username_case_sensitive,
            group_override_attr_type=group_override_attr_type,
            class_=class_,
            password_renewal=password_renewal,
            require_message_authenticator=require_message_authenticator,
            password_encoding=password_encoding,
            mac_username_delimiter=mac_username_delimiter,
            mac_password_delimiter=mac_password_delimiter,
            mac_case=mac_case,
            acct_all_servers=acct_all_servers,
            switch_controller_acct_fast_framedip_detect=switch_controller_acct_fast_framedip_detect,
            interface_select_method=interface_select_method,
            interface=interface,
            vrf_select=vrf_select,
            switch_controller_service_type=switch_controller_service_type,
            transport_protocol=transport_protocol,
            tls_min_proto_version=tls_min_proto_version,
            ca_cert=ca_cert,
            client_cert=client_cert,
            server_identity_check=server_identity_check,
            account_key_processing=account_key_processing,
            account_key_cert_field=account_key_cert_field,
            rsso=rsso,
            rsso_radius_server_port=rsso_radius_server_port,
            rsso_radius_response=rsso_radius_response,
            rsso_validate_request_secret=rsso_validate_request_secret,
            rsso_secret=rsso_secret,
            rsso_endpoint_attribute=rsso_endpoint_attribute,
            rsso_endpoint_block_attribute=rsso_endpoint_block_attribute,
            sso_attribute=sso_attribute,
            sso_attribute_key=sso_attribute_key,
            sso_attribute_value_override=sso_attribute_value_override,
            rsso_context_timeout=rsso_context_timeout,
            rsso_log_period=rsso_log_period,
            rsso_log_flags=rsso_log_flags,
            rsso_flush_ip_session=rsso_flush_ip_session,
            rsso_ep_one_ip_only=rsso_ep_one_ip_only,
            delimiter=delimiter,
            accounting_server=accounting_server,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.radius import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/radius",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/user/radius/" + quote_path_param(name_value)

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
        server: str | None = None,
        secret: Any | None = None,
        secondary_server: str | None = None,
        secondary_secret: Any | None = None,
        tertiary_server: str | None = None,
        tertiary_secret: Any | None = None,
        timeout: int | None = None,
        status_ttl: int | None = None,
        all_usergroup: Literal["disable", "enable"] | None = None,
        use_management_vdom: Literal["enable", "disable"] | None = None,
        switch_controller_nas_ip_dynamic: Literal["enable", "disable"] | None = None,
        nas_ip: str | None = None,
        nas_id_type: Literal["legacy", "custom", "hostname"] | None = None,
        call_station_id_type: Literal["legacy", "IP", "MAC"] | None = None,
        nas_id: str | None = None,
        acct_interim_interval: int | None = None,
        radius_coa: Literal["enable", "disable"] | None = None,
        radius_port: int | None = None,
        h3c_compatibility: Literal["enable", "disable"] | None = None,
        auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"] | None = None,
        source_ip: str | None = None,
        source_ip_interface: str | None = None,
        username_case_sensitive: Literal["enable", "disable"] | None = None,
        group_override_attr_type: Literal["filter-Id", "class"] | None = None,
        class_: str | list[str] | list[dict[str, Any]] | None = None,
        password_renewal: Literal["enable", "disable"] | None = None,
        require_message_authenticator: Literal["enable", "disable"] | None = None,
        password_encoding: Literal["auto", "ISO-8859-1"] | None = None,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = None,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = None,
        mac_case: Literal["uppercase", "lowercase"] | None = None,
        acct_all_servers: Literal["enable", "disable"] | None = None,
        switch_controller_acct_fast_framedip_detect: int | None = None,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = None,
        interface: str | None = None,
        vrf_select: int | None = None,
        switch_controller_service_type: Literal["login", "framed", "callback-login", "callback-framed", "outbound", "administrative", "nas-prompt", "authenticate-only", "callback-nas-prompt", "call-check", "callback-administrative"] | list[str] | None = None,
        transport_protocol: Literal["udp", "tcp", "tls"] | None = None,
        tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = None,
        ca_cert: str | None = None,
        client_cert: str | None = None,
        server_identity_check: Literal["enable", "disable"] | None = None,
        account_key_processing: Literal["same", "strip"] | None = None,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = None,
        rsso: Literal["enable", "disable"] | None = None,
        rsso_radius_server_port: int | None = None,
        rsso_radius_response: Literal["enable", "disable"] | None = None,
        rsso_validate_request_secret: Literal["enable", "disable"] | None = None,
        rsso_secret: Any | None = None,
        rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        sso_attribute_key: str | None = None,
        sso_attribute_value_override: Literal["enable", "disable"] | None = None,
        rsso_context_timeout: int | None = None,
        rsso_log_period: int | None = None,
        rsso_log_flags: Literal["protocol-error", "profile-missing", "accounting-stop-missed", "accounting-event", "endpoint-block", "radiusd-other", "none"] | list[str] | None = None,
        rsso_flush_ip_session: Literal["enable", "disable"] | None = None,
        rsso_ep_one_ip_only: Literal["enable", "disable"] | None = None,
        delimiter: Literal["plus", "comma"] | None = None,
        accounting_server: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new user/radius object.

        Configure RADIUS server entries.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: RADIUS server entry name.
            server: Primary RADIUS server CN domain name or IP address.
            secret: Pre-shared secret key used to access the primary RADIUS server.
            secondary_server: Secondary RADIUS CN domain name or IP address.
            secondary_secret: Secret key to access the secondary server.
            tertiary_server: Tertiary RADIUS CN domain name or IP address.
            tertiary_secret: Secret key to access the tertiary server.
            timeout: Time in seconds to retry connecting server.
            status_ttl: Time for which server reachability is cached so that when a server is unreachable, it will not be retried for at least this period of time (0 = cache disabled, default = 300).
            all_usergroup: Enable/disable automatically including this RADIUS server in all user groups.
            use_management_vdom: Enable/disable using management VDOM to send requests.
            switch_controller_nas_ip_dynamic: Enable/Disable switch-controller nas-ip dynamic to dynamically set nas-ip.
            nas_ip: IP address used to communicate with the RADIUS server and used as NAS-IP-Address and Called-Station-ID attributes.
            nas_id_type: NAS identifier type configuration (default = legacy).
            call_station_id_type: Calling & Called station identifier type configuration (default = legacy), this option is not available for 802.1x authentication. 
            nas_id: Custom NAS identifier.
            acct_interim_interval: Time in seconds between each accounting interim update message.
            radius_coa: Enable to allow a mechanism to change the attributes of an authentication, authorization, and accounting session after it is authenticated.
            radius_port: RADIUS service port number.
            h3c_compatibility: Enable/disable compatibility with the H3C, a mechanism that performs security checking for authentication.
            auth_type: Authentication methods/protocols permitted for this RADIUS server.
            source_ip: Source IP address for communications to the RADIUS server.
            source_ip_interface: Source interface for communication with the RADIUS server.
            username_case_sensitive: Enable/disable case sensitive user names.
            group_override_attr_type: RADIUS attribute type to override user group information.
            class_: Class attribute name(s).
            password_renewal: Enable/disable password renewal.
            require_message_authenticator: Require message authenticator in authentication response.
            password_encoding: Password encoding.
            mac_username_delimiter: MAC authentication username delimiter (default = hyphen).
            mac_password_delimiter: MAC authentication password delimiter (default = hyphen).
            mac_case: MAC authentication case (default = lowercase).
            acct_all_servers: Enable/disable sending of accounting messages to all configured servers (default = disable).
            switch_controller_acct_fast_framedip_detect: Switch controller accounting message Framed-IP detection from DHCP snooping (seconds, default=2).
            interface_select_method: Specify how to select outgoing interface to reach server.
            interface: Specify outgoing interface to reach server.
            vrf_select: VRF ID used for connection to server.
            switch_controller_service_type: RADIUS service type.
            transport_protocol: Transport protocol to be used (default = udp).
            tls_min_proto_version: Minimum supported protocol version for TLS connections (default is to follow system global setting).
            ca_cert: CA of server to trust under TLS.
            client_cert: Client certificate to use under TLS.
            server_identity_check: Enable/disable RADIUS server identity check (verify server domain name/IP address against the server certificate).
            account_key_processing: Account key processing operation. The FortiGate will keep either the whole domain or strip the domain from the subject identity.
            account_key_cert_field: Define subject identity field in certificate for user access right checking.
            rsso: Enable/disable RADIUS based single sign on feature.
            rsso_radius_server_port: UDP port to listen on for RADIUS Start and Stop records.
            rsso_radius_response: Enable/disable sending RADIUS response packets after receiving Start and Stop records.
            rsso_validate_request_secret: Enable/disable validating the RADIUS request shared secret in the Start or End record.
            rsso_secret: RADIUS secret used by the RADIUS accounting server.
            rsso_endpoint_attribute: RADIUS attributes used to extract the user end point identifier from the RADIUS Start record.
            rsso_endpoint_block_attribute: RADIUS attributes used to block a user.
            sso_attribute: RADIUS attribute that contains the profile group name to be extracted from the RADIUS Start record.
            sso_attribute_key: Key prefix for SSO group value in the SSO attribute.
            sso_attribute_value_override: Enable/disable override old attribute value with new value for the same endpoint.
            rsso_context_timeout: Time in seconds before the logged out user is removed from the "user context list" of logged on users.
            rsso_log_period: Time interval in seconds that group event log messages will be generated for dynamic profile events.
            rsso_log_flags: Events to log.
            rsso_flush_ip_session: Enable/disable flushing user IP sessions on RADIUS accounting Stop messages.
            rsso_ep_one_ip_only: Enable/disable the replacement of old IP addresses with new ones for the same endpoint on RADIUS accounting Start messages.
            delimiter: Configure delimiter to be used for separating profile group names in the SSO attribute (default = plus character "+").
            accounting_server: Additional accounting servers.
                Default format: [{'server': '192.168.1.10', 'secret': 'value', 'interface': 'value'}]
                Required format: List of dicts with keys: server, secret, interface
                  (String format not allowed due to multiple required fields)
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.user_radius.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Radius.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.user_radius.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Radius.required_fields()) }}
            
            Use Radius.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if class_ is not None:
            class_ = normalize_table_field(
                class_,
                mkey="name",
                required_fields=['name'],
                field_name="class_",
                example="[{'name': 'value'}]",
            )
        if accounting_server is not None:
            accounting_server = normalize_table_field(
                accounting_server,
                mkey="id",
                required_fields=['server', 'secret', 'interface'],
                field_name="accounting_server",
                example="[{'server': '192.168.1.10', 'secret': 'value', 'interface': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            server=server,
            secret=secret,
            secondary_server=secondary_server,
            secondary_secret=secondary_secret,
            tertiary_server=tertiary_server,
            tertiary_secret=tertiary_secret,
            timeout=timeout,
            status_ttl=status_ttl,
            all_usergroup=all_usergroup,
            use_management_vdom=use_management_vdom,
            switch_controller_nas_ip_dynamic=switch_controller_nas_ip_dynamic,
            nas_ip=nas_ip,
            nas_id_type=nas_id_type,
            call_station_id_type=call_station_id_type,
            nas_id=nas_id,
            acct_interim_interval=acct_interim_interval,
            radius_coa=radius_coa,
            radius_port=radius_port,
            h3c_compatibility=h3c_compatibility,
            auth_type=auth_type,
            source_ip=source_ip,
            source_ip_interface=source_ip_interface,
            username_case_sensitive=username_case_sensitive,
            group_override_attr_type=group_override_attr_type,
            class_=class_,
            password_renewal=password_renewal,
            require_message_authenticator=require_message_authenticator,
            password_encoding=password_encoding,
            mac_username_delimiter=mac_username_delimiter,
            mac_password_delimiter=mac_password_delimiter,
            mac_case=mac_case,
            acct_all_servers=acct_all_servers,
            switch_controller_acct_fast_framedip_detect=switch_controller_acct_fast_framedip_detect,
            interface_select_method=interface_select_method,
            interface=interface,
            vrf_select=vrf_select,
            switch_controller_service_type=switch_controller_service_type,
            transport_protocol=transport_protocol,
            tls_min_proto_version=tls_min_proto_version,
            ca_cert=ca_cert,
            client_cert=client_cert,
            server_identity_check=server_identity_check,
            account_key_processing=account_key_processing,
            account_key_cert_field=account_key_cert_field,
            rsso=rsso,
            rsso_radius_server_port=rsso_radius_server_port,
            rsso_radius_response=rsso_radius_response,
            rsso_validate_request_secret=rsso_validate_request_secret,
            rsso_secret=rsso_secret,
            rsso_endpoint_attribute=rsso_endpoint_attribute,
            rsso_endpoint_block_attribute=rsso_endpoint_block_attribute,
            sso_attribute=sso_attribute,
            sso_attribute_key=sso_attribute_key,
            sso_attribute_value_override=sso_attribute_value_override,
            rsso_context_timeout=rsso_context_timeout,
            rsso_log_period=rsso_log_period,
            rsso_log_flags=rsso_log_flags,
            rsso_flush_ip_session=rsso_flush_ip_session,
            rsso_ep_one_ip_only=rsso_ep_one_ip_only,
            delimiter=delimiter,
            accounting_server=accounting_server,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.radius import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/radius",
            )

        endpoint = "/user/radius"
        
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
        Delete user/radius object.

        Configure RADIUS server entries.

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
            >>> result = fgt.api.cmdb.user_radius.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/user/radius/" + quote_path_param(name)

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
        Check if user/radius object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.user_radius.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.user_radius.exists(name=1):
            ...     fgt.api.cmdb.user_radius.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/user/radius"
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
        server: str | None = None,
        secret: Any | None = None,
        secondary_server: str | None = None,
        secondary_secret: Any | None = None,
        tertiary_server: str | None = None,
        tertiary_secret: Any | None = None,
        timeout: int | None = None,
        status_ttl: int | None = None,
        all_usergroup: Literal["disable", "enable"] | None = None,
        use_management_vdom: Literal["enable", "disable"] | None = None,
        switch_controller_nas_ip_dynamic: Literal["enable", "disable"] | None = None,
        nas_ip: str | None = None,
        nas_id_type: Literal["legacy", "custom", "hostname"] | None = None,
        call_station_id_type: Literal["legacy", "IP", "MAC"] | None = None,
        nas_id: str | None = None,
        acct_interim_interval: int | None = None,
        radius_coa: Literal["enable", "disable"] | None = None,
        radius_port: int | None = None,
        h3c_compatibility: Literal["enable", "disable"] | None = None,
        auth_type: Literal["auto", "ms_chap_v2", "ms_chap", "chap", "pap"] | None = None,
        source_ip: str | None = None,
        source_ip_interface: str | None = None,
        username_case_sensitive: Literal["enable", "disable"] | None = None,
        group_override_attr_type: Literal["filter-Id", "class"] | None = None,
        class_: str | list[str] | list[dict[str, Any]] | None = None,
        password_renewal: Literal["enable", "disable"] | None = None,
        require_message_authenticator: Literal["enable", "disable"] | None = None,
        password_encoding: Literal["auto", "ISO-8859-1"] | None = None,
        mac_username_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = None,
        mac_password_delimiter: Literal["hyphen", "single-hyphen", "colon", "none"] | None = None,
        mac_case: Literal["uppercase", "lowercase"] | None = None,
        acct_all_servers: Literal["enable", "disable"] | None = None,
        switch_controller_acct_fast_framedip_detect: int | None = None,
        interface_select_method: Literal["auto", "sdwan", "specify"] | None = None,
        interface: str | None = None,
        vrf_select: int | None = None,
        switch_controller_service_type: Literal["login", "framed", "callback-login", "callback-framed", "outbound", "administrative", "nas-prompt", "authenticate-only", "callback-nas-prompt", "call-check", "callback-administrative"] | list[str] | list[dict[str, Any]] | None = None,
        transport_protocol: Literal["udp", "tcp", "tls"] | None = None,
        tls_min_proto_version: Literal["default", "SSLv3", "TLSv1", "TLSv1-1", "TLSv1-2", "TLSv1-3"] | None = None,
        ca_cert: str | None = None,
        client_cert: str | None = None,
        server_identity_check: Literal["enable", "disable"] | None = None,
        account_key_processing: Literal["same", "strip"] | None = None,
        account_key_cert_field: Literal["othername", "rfc822name", "dnsname", "cn"] | None = None,
        rsso: Literal["enable", "disable"] | None = None,
        rsso_radius_server_port: int | None = None,
        rsso_radius_response: Literal["enable", "disable"] | None = None,
        rsso_validate_request_secret: Literal["enable", "disable"] | None = None,
        rsso_secret: Any | None = None,
        rsso_endpoint_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        rsso_endpoint_block_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        sso_attribute: Literal["User-Name", "NAS-IP-Address", "Framed-IP-Address", "Framed-IP-Netmask", "Filter-Id", "Login-IP-Host", "Reply-Message", "Callback-Number", "Callback-Id", "Framed-Route", "Framed-IPX-Network", "Class", "Called-Station-Id", "Calling-Station-Id", "NAS-Identifier", "Proxy-State", "Login-LAT-Service", "Login-LAT-Node", "Login-LAT-Group", "Framed-AppleTalk-Zone", "Acct-Session-Id", "Acct-Multi-Session-Id"] | None = None,
        sso_attribute_key: str | None = None,
        sso_attribute_value_override: Literal["enable", "disable"] | None = None,
        rsso_context_timeout: int | None = None,
        rsso_log_period: int | None = None,
        rsso_log_flags: Literal["protocol-error", "profile-missing", "accounting-stop-missed", "accounting-event", "endpoint-block", "radiusd-other", "none"] | list[str] | list[dict[str, Any]] | None = None,
        rsso_flush_ip_session: Literal["enable", "disable"] | None = None,
        rsso_ep_one_ip_only: Literal["enable", "disable"] | None = None,
        delimiter: Literal["plus", "comma"] | None = None,
        accounting_server: str | list[str] | list[dict[str, Any]] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update user/radius object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            server: Field server
            secret: Field secret
            secondary_server: Field secondary-server
            secondary_secret: Field secondary-secret
            tertiary_server: Field tertiary-server
            tertiary_secret: Field tertiary-secret
            timeout: Field timeout
            status_ttl: Field status-ttl
            all_usergroup: Field all-usergroup
            use_management_vdom: Field use-management-vdom
            switch_controller_nas_ip_dynamic: Field switch-controller-nas-ip-dynamic
            nas_ip: Field nas-ip
            nas_id_type: Field nas-id-type
            call_station_id_type: Field call-station-id-type
            nas_id: Field nas-id
            acct_interim_interval: Field acct-interim-interval
            radius_coa: Field radius-coa
            radius_port: Field radius-port
            h3c_compatibility: Field h3c-compatibility
            auth_type: Field auth-type
            source_ip: Field source-ip
            source_ip_interface: Field source-ip-interface
            username_case_sensitive: Field username-case-sensitive
            group_override_attr_type: Field group-override-attr-type
            class_: Field class
            password_renewal: Field password-renewal
            require_message_authenticator: Field require-message-authenticator
            password_encoding: Field password-encoding
            mac_username_delimiter: Field mac-username-delimiter
            mac_password_delimiter: Field mac-password-delimiter
            mac_case: Field mac-case
            acct_all_servers: Field acct-all-servers
            switch_controller_acct_fast_framedip_detect: Field switch-controller-acct-fast-framedip-detect
            interface_select_method: Field interface-select-method
            interface: Field interface
            vrf_select: Field vrf-select
            switch_controller_service_type: Field switch-controller-service-type
            transport_protocol: Field transport-protocol
            tls_min_proto_version: Field tls-min-proto-version
            ca_cert: Field ca-cert
            client_cert: Field client-cert
            server_identity_check: Field server-identity-check
            account_key_processing: Field account-key-processing
            account_key_cert_field: Field account-key-cert-field
            rsso: Field rsso
            rsso_radius_server_port: Field rsso-radius-server-port
            rsso_radius_response: Field rsso-radius-response
            rsso_validate_request_secret: Field rsso-validate-request-secret
            rsso_secret: Field rsso-secret
            rsso_endpoint_attribute: Field rsso-endpoint-attribute
            rsso_endpoint_block_attribute: Field rsso-endpoint-block-attribute
            sso_attribute: Field sso-attribute
            sso_attribute_key: Field sso-attribute-key
            sso_attribute_value_override: Field sso-attribute-value-override
            rsso_context_timeout: Field rsso-context-timeout
            rsso_log_period: Field rsso-log-period
            rsso_log_flags: Field rsso-log-flags
            rsso_flush_ip_session: Field rsso-flush-ip-session
            rsso_ep_one_ip_only: Field rsso-ep-one-ip-only
            delimiter: Field delimiter
            accounting_server: Field accounting-server
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.user_radius.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.user_radius.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.user_radius.set(payload_dict=obj_data)
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
        if class_ is not None:
            class_ = normalize_table_field(
                class_,
                mkey="name",
                required_fields=['name'],
                field_name="class_",
                example="[{'name': 'value'}]",
            )
        if accounting_server is not None:
            accounting_server = normalize_table_field(
                accounting_server,
                mkey="id",
                required_fields=['server', 'secret', 'interface'],
                field_name="accounting_server",
                example="[{'server': '192.168.1.10', 'secret': 'value', 'interface': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            server=server,
            secret=secret,
            secondary_server=secondary_server,
            secondary_secret=secondary_secret,
            tertiary_server=tertiary_server,
            tertiary_secret=tertiary_secret,
            timeout=timeout,
            status_ttl=status_ttl,
            all_usergroup=all_usergroup,
            use_management_vdom=use_management_vdom,
            switch_controller_nas_ip_dynamic=switch_controller_nas_ip_dynamic,
            nas_ip=nas_ip,
            nas_id_type=nas_id_type,
            call_station_id_type=call_station_id_type,
            nas_id=nas_id,
            acct_interim_interval=acct_interim_interval,
            radius_coa=radius_coa,
            radius_port=radius_port,
            h3c_compatibility=h3c_compatibility,
            auth_type=auth_type,
            source_ip=source_ip,
            source_ip_interface=source_ip_interface,
            username_case_sensitive=username_case_sensitive,
            group_override_attr_type=group_override_attr_type,
            class_=class_,
            password_renewal=password_renewal,
            require_message_authenticator=require_message_authenticator,
            password_encoding=password_encoding,
            mac_username_delimiter=mac_username_delimiter,
            mac_password_delimiter=mac_password_delimiter,
            mac_case=mac_case,
            acct_all_servers=acct_all_servers,
            switch_controller_acct_fast_framedip_detect=switch_controller_acct_fast_framedip_detect,
            interface_select_method=interface_select_method,
            interface=interface,
            vrf_select=vrf_select,
            switch_controller_service_type=switch_controller_service_type,
            transport_protocol=transport_protocol,
            tls_min_proto_version=tls_min_proto_version,
            ca_cert=ca_cert,
            client_cert=client_cert,
            server_identity_check=server_identity_check,
            account_key_processing=account_key_processing,
            account_key_cert_field=account_key_cert_field,
            rsso=rsso,
            rsso_radius_server_port=rsso_radius_server_port,
            rsso_radius_response=rsso_radius_response,
            rsso_validate_request_secret=rsso_validate_request_secret,
            rsso_secret=rsso_secret,
            rsso_endpoint_attribute=rsso_endpoint_attribute,
            rsso_endpoint_block_attribute=rsso_endpoint_block_attribute,
            sso_attribute=sso_attribute,
            sso_attribute_key=sso_attribute_key,
            sso_attribute_value_override=sso_attribute_value_override,
            rsso_context_timeout=rsso_context_timeout,
            rsso_log_period=rsso_log_period,
            rsso_log_flags=rsso_log_flags,
            rsso_flush_ip_session=rsso_flush_ip_session,
            rsso_ep_one_ip_only=rsso_ep_one_ip_only,
            delimiter=delimiter,
            accounting_server=accounting_server,
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
        Move user/radius object to a new position.
        
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
            >>> fgt.api.cmdb.user_radius.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.user_radius.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.user_radius.move(
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
        endpoint = "/user/radius/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





