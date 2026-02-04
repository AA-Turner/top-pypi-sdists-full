"""
FortiOS CMDB - User local

Configuration endpoint for managing cmdb user/local objects.

API Endpoints:
    GET    /cmdb/user/local
    POST   /cmdb/user/local
    PUT    /cmdb/user/local/{identifier}
    DELETE /cmdb/user/local/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.user_local.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.user_local.post(
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

class Local(CRUDEndpoint, MetadataMixin):
    """Local Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "local"
    
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
        """Initialize Local endpoint."""
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
        Retrieve user/local configuration.

        Configure local users.

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
            >>> # Get all user/local objects
            >>> result = fgt.api.cmdb.user_local.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific user/local by name
            >>> result = fgt.api.cmdb.user_local.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.user_local.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.user_local.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.user_local.get_schema()

        See Also:
            - post(): Create new user/local object
            - put(): Update existing user/local object
            - delete(): Remove user/local object
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
            endpoint = "/user/local/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/user/local"
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
            >>> schema = fgt.api.cmdb.user_local.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.user_local.get_schema(format="json-schema")
        
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
        id: int | None = None,
        status: Literal["enable", "disable"] | None = None,
        type: Literal["password", "radius", "tacacs+", "ldap", "saml"] | None = None,
        passwd: Any | None = None,
        ldap_server: str | None = None,
        radius_server: str | None = None,
        tacacs_plus_server: str | None = None,
        saml_server: str | None = None,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = None,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = None,
        two_factor_notification: Literal["email", "sms"] | None = None,
        fortitoken: str | None = None,
        email_to: str | None = None,
        sms_server: Literal["fortiguard", "custom"] | None = None,
        sms_custom_server: str | None = None,
        sms_phone: str | None = None,
        passwd_policy: str | None = None,
        passwd_time: str | None = None,
        authtimeout: int | None = None,
        workstation: str | None = None,
        auth_concurrent_override: Literal["enable", "disable"] | None = None,
        auth_concurrent_value: int | None = None,
        ppk_secret: Any | None = None,
        ppk_identity: str | None = None,
        qkd_profile: str | None = None,
        username_sensitivity: Literal["disable", "enable"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing user/local object.

        Configure local users.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Local user name.
            id: User ID.
            status: Enable/disable allowing the local user to authenticate with the FortiGate unit.
            type: Authentication method.
            passwd: User's password.
            ldap_server: Name of LDAP server with which the user must authenticate.
            radius_server: Name of RADIUS server with which the user must authenticate.
            tacacs_plus_server: Name of TACACS+ server with which the user must authenticate.
            saml_server: Name of SAML server with which the user must authenticate.
            two_factor: Enable/disable two-factor authentication.
            two_factor_authentication: Authentication method by FortiToken Cloud.
            two_factor_notification: Notification method for user activation by FortiToken Cloud.
            fortitoken: Two-factor recipient's FortiToken serial number.
            email_to: Two-factor recipient's email address.
            sms_server: Send SMS through FortiGuard or other external server.
            sms_custom_server: Two-factor recipient's SMS server.
            sms_phone: Two-factor recipient's mobile phone number.
            passwd_policy: Password policy to apply to this user, as defined in config user password-policy.
            passwd_time: Time of the last password update.
            authtimeout: Time in minutes before the authentication timeout for a user is reached.
            workstation: Name of the remote user workstation, if you want to limit the user to authenticate only from a particular workstation.
            auth_concurrent_override: Enable/disable overriding the policy-auth-concurrent under config system global.
            auth_concurrent_value: Maximum number of concurrent logins permitted from the same user.
            ppk_secret: IKEv2 Postquantum Preshared Key (ASCII string or hexadecimal encoded with a leading 0x).
            ppk_identity: IKEv2 Postquantum Preshared Key Identity.
            qkd_profile: Quantum Key Distribution (QKD) profile.
            username_sensitivity: Enable/disable case and accent sensitivity when performing username matching (accents are stripped and case is ignored when disabled).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.user_local.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.user_local.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            id=id,
            status=status,
            type=type,
            passwd=passwd,
            ldap_server=ldap_server,
            radius_server=radius_server,
            tacacs_plus_server=tacacs_plus_server,
            saml_server=saml_server,
            two_factor=two_factor,
            two_factor_authentication=two_factor_authentication,
            two_factor_notification=two_factor_notification,
            fortitoken=fortitoken,
            email_to=email_to,
            sms_server=sms_server,
            sms_custom_server=sms_custom_server,
            sms_phone=sms_phone,
            passwd_policy=passwd_policy,
            passwd_time=passwd_time,
            authtimeout=authtimeout,
            workstation=workstation,
            auth_concurrent_override=auth_concurrent_override,
            auth_concurrent_value=auth_concurrent_value,
            ppk_secret=ppk_secret,
            ppk_identity=ppk_identity,
            qkd_profile=qkd_profile,
            username_sensitivity=username_sensitivity,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.local import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/local",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/user/local/" + quote_path_param(name_value)

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
        id: int | None = None,
        status: Literal["enable", "disable"] | None = None,
        type: Literal["password", "radius", "tacacs+", "ldap", "saml"] | None = None,
        passwd: Any | None = None,
        ldap_server: str | None = None,
        radius_server: str | None = None,
        tacacs_plus_server: str | None = None,
        saml_server: str | None = None,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = None,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = None,
        two_factor_notification: Literal["email", "sms"] | None = None,
        fortitoken: str | None = None,
        email_to: str | None = None,
        sms_server: Literal["fortiguard", "custom"] | None = None,
        sms_custom_server: str | None = None,
        sms_phone: str | None = None,
        passwd_policy: str | None = None,
        passwd_time: str | None = None,
        authtimeout: int | None = None,
        workstation: str | None = None,
        auth_concurrent_override: Literal["enable", "disable"] | None = None,
        auth_concurrent_value: int | None = None,
        ppk_secret: Any | None = None,
        ppk_identity: str | None = None,
        qkd_profile: str | None = None,
        username_sensitivity: Literal["disable", "enable"] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new user/local object.

        Configure local users.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Local user name.
            id: User ID.
            status: Enable/disable allowing the local user to authenticate with the FortiGate unit.
            type: Authentication method.
            passwd: User's password.
            ldap_server: Name of LDAP server with which the user must authenticate.
            radius_server: Name of RADIUS server with which the user must authenticate.
            tacacs_plus_server: Name of TACACS+ server with which the user must authenticate.
            saml_server: Name of SAML server with which the user must authenticate.
            two_factor: Enable/disable two-factor authentication.
            two_factor_authentication: Authentication method by FortiToken Cloud.
            two_factor_notification: Notification method for user activation by FortiToken Cloud.
            fortitoken: Two-factor recipient's FortiToken serial number.
            email_to: Two-factor recipient's email address.
            sms_server: Send SMS through FortiGuard or other external server.
            sms_custom_server: Two-factor recipient's SMS server.
            sms_phone: Two-factor recipient's mobile phone number.
            passwd_policy: Password policy to apply to this user, as defined in config user password-policy.
            passwd_time: Time of the last password update.
            authtimeout: Time in minutes before the authentication timeout for a user is reached.
            workstation: Name of the remote user workstation, if you want to limit the user to authenticate only from a particular workstation.
            auth_concurrent_override: Enable/disable overriding the policy-auth-concurrent under config system global.
            auth_concurrent_value: Maximum number of concurrent logins permitted from the same user.
            ppk_secret: IKEv2 Postquantum Preshared Key (ASCII string or hexadecimal encoded with a leading 0x).
            ppk_identity: IKEv2 Postquantum Preshared Key Identity.
            qkd_profile: Quantum Key Distribution (QKD) profile.
            username_sensitivity: Enable/disable case and accent sensitivity when performing username matching (accents are stripped and case is ignored when disabled).
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.user_local.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Local.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.user_local.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Local.required_fields()) }}
            
            Use Local.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            id=id,
            status=status,
            type=type,
            passwd=passwd,
            ldap_server=ldap_server,
            radius_server=radius_server,
            tacacs_plus_server=tacacs_plus_server,
            saml_server=saml_server,
            two_factor=two_factor,
            two_factor_authentication=two_factor_authentication,
            two_factor_notification=two_factor_notification,
            fortitoken=fortitoken,
            email_to=email_to,
            sms_server=sms_server,
            sms_custom_server=sms_custom_server,
            sms_phone=sms_phone,
            passwd_policy=passwd_policy,
            passwd_time=passwd_time,
            authtimeout=authtimeout,
            workstation=workstation,
            auth_concurrent_override=auth_concurrent_override,
            auth_concurrent_value=auth_concurrent_value,
            ppk_secret=ppk_secret,
            ppk_identity=ppk_identity,
            qkd_profile=qkd_profile,
            username_sensitivity=username_sensitivity,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.local import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/local",
            )

        endpoint = "/user/local"
        
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
        Delete user/local object.

        Configure local users.

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
            >>> result = fgt.api.cmdb.user_local.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/user/local/" + quote_path_param(name)

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
        Check if user/local object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.user_local.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.user_local.exists(name=1):
            ...     fgt.api.cmdb.user_local.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/user/local"
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
        id: int | None = None,
        status: Literal["enable", "disable"] | None = None,
        type: Literal["password", "radius", "tacacs+", "ldap", "saml"] | None = None,
        passwd: Any | None = None,
        ldap_server: str | None = None,
        radius_server: str | None = None,
        tacacs_plus_server: str | None = None,
        saml_server: str | None = None,
        two_factor: Literal["disable", "fortitoken", "fortitoken-cloud", "email", "sms"] | None = None,
        two_factor_authentication: Literal["fortitoken", "email", "sms"] | None = None,
        two_factor_notification: Literal["email", "sms"] | None = None,
        fortitoken: str | None = None,
        email_to: str | None = None,
        sms_server: Literal["fortiguard", "custom"] | None = None,
        sms_custom_server: str | None = None,
        sms_phone: str | None = None,
        passwd_policy: str | None = None,
        passwd_time: str | None = None,
        authtimeout: int | None = None,
        workstation: str | None = None,
        auth_concurrent_override: Literal["enable", "disable"] | None = None,
        auth_concurrent_value: int | None = None,
        ppk_secret: Any | None = None,
        ppk_identity: str | None = None,
        qkd_profile: str | None = None,
        username_sensitivity: Literal["disable", "enable"] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update user/local object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            id: Field id
            status: Field status
            type: Field type
            passwd: Field passwd
            ldap_server: Field ldap-server
            radius_server: Field radius-server
            tacacs_plus_server: Field tacacs+-server
            saml_server: Field saml-server
            two_factor: Field two-factor
            two_factor_authentication: Field two-factor-authentication
            two_factor_notification: Field two-factor-notification
            fortitoken: Field fortitoken
            email_to: Field email-to
            sms_server: Field sms-server
            sms_custom_server: Field sms-custom-server
            sms_phone: Field sms-phone
            passwd_policy: Field passwd-policy
            passwd_time: Field passwd-time
            authtimeout: Field authtimeout
            workstation: Field workstation
            auth_concurrent_override: Field auth-concurrent-override
            auth_concurrent_value: Field auth-concurrent-value
            ppk_secret: Field ppk-secret
            ppk_identity: Field ppk-identity
            qkd_profile: Field qkd-profile
            username_sensitivity: Field username-sensitivity
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.user_local.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.user_local.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.user_local.set(payload_dict=obj_data)
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
            id=id,
            status=status,
            type=type,
            passwd=passwd,
            ldap_server=ldap_server,
            radius_server=radius_server,
            tacacs_plus_server=tacacs_plus_server,
            saml_server=saml_server,
            two_factor=two_factor,
            two_factor_authentication=two_factor_authentication,
            two_factor_notification=two_factor_notification,
            fortitoken=fortitoken,
            email_to=email_to,
            sms_server=sms_server,
            sms_custom_server=sms_custom_server,
            sms_phone=sms_phone,
            passwd_policy=passwd_policy,
            passwd_time=passwd_time,
            authtimeout=authtimeout,
            workstation=workstation,
            auth_concurrent_override=auth_concurrent_override,
            auth_concurrent_value=auth_concurrent_value,
            ppk_secret=ppk_secret,
            ppk_identity=ppk_identity,
            qkd_profile=qkd_profile,
            username_sensitivity=username_sensitivity,
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
        Move user/local object to a new position.
        
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
            >>> fgt.api.cmdb.user_local.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.user_local.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.user_local.move(
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
        endpoint = "/user/local/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





