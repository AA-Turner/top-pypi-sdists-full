"""
FortiOS CMDB - Authentication scheme

Configuration endpoint for managing cmdb authentication/scheme objects.

API Endpoints:
    GET    /cmdb/authentication/scheme
    POST   /cmdb/authentication/scheme
    PUT    /cmdb/authentication/scheme/{identifier}
    DELETE /cmdb/authentication/scheme/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.authentication_scheme.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.authentication_scheme.post(
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

class Scheme(CRUDEndpoint, MetadataMixin):
    """Scheme Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "scheme"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "user_database": {
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
        """Initialize Scheme endpoint."""
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
        Retrieve authentication/scheme configuration.

        Configure Authentication Schemes.

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
            >>> # Get all authentication/scheme objects
            >>> result = fgt.api.cmdb.authentication_scheme.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific authentication/scheme by name
            >>> result = fgt.api.cmdb.authentication_scheme.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.authentication_scheme.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.authentication_scheme.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.authentication_scheme.get_schema()

        See Also:
            - post(): Create new authentication/scheme object
            - put(): Update existing authentication/scheme object
            - delete(): Remove authentication/scheme object
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
            endpoint = "/authentication/scheme/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/authentication/scheme"
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
            >>> schema = fgt.api.cmdb.authentication_scheme.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.authentication_scheme.get_schema(format="json-schema")
        
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
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = None,
        negotiate_ntlm: Literal["enable", "disable"] | None = None,
        kerberos_keytab: str | None = None,
        domain_controller: str | None = None,
        saml_server: str | None = None,
        saml_timeout: int | None = None,
        fsso_agent_for_ntlm: str | None = None,
        require_tfa: Literal["enable", "disable"] | None = None,
        fsso_guest: Literal["enable", "disable"] | None = None,
        user_cert: Literal["enable", "disable"] | None = None,
        cert_http_header: Literal["enable", "disable"] | None = None,
        user_database: str | list[str] | list[dict[str, Any]] | None = None,
        ssh_ca: str | None = None,
        external_idp: str | None = None,
        group_attr_type: Literal["display-name", "external-id"] | None = None,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = None,
        digest_rfc2069: Literal["enable", "disable"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing authentication/scheme object.

        Configure Authentication Schemes.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Authentication scheme name.
            method: Authentication methods (default = basic).
            negotiate_ntlm: Enable/disable negotiate authentication for NTLM (default = disable).
            kerberos_keytab: Kerberos keytab setting.
            domain_controller: Domain controller setting.
            saml_server: SAML configuration.
            saml_timeout: SAML authentication timeout in seconds.
            fsso_agent_for_ntlm: FSSO agent to use for NTLM authentication.
            require_tfa: Enable/disable two-factor authentication (default = disable).
            fsso_guest: Enable/disable user fsso-guest authentication (default = disable).
            user_cert: Enable/disable authentication with user certificate (default = disable).
            cert_http_header: Enable/disable authentication with user certificate in Client-Cert HTTP header (default = disable).
            user_database: Authentication server to contain user information; "local-user-db" (default) or "123" (for LDAP).
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            ssh_ca: SSH CA name.
            external_idp: External identity provider configuration.
            group_attr_type: Group attribute type used to match SCIM groups (default = display-name).
            digest_algo: Digest Authentication Algorithms.
            digest_rfc2069: Enable/disable support for the deprecated RFC2069 Digest Client (no cnonce field, default = disable).
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.authentication_scheme.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.authentication_scheme.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if user_database is not None:
            user_database = normalize_table_field(
                user_database,
                mkey="name",
                required_fields=['name'],
                field_name="user_database",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            method=method,
            negotiate_ntlm=negotiate_ntlm,
            kerberos_keytab=kerberos_keytab,
            domain_controller=domain_controller,
            saml_server=saml_server,
            saml_timeout=saml_timeout,
            fsso_agent_for_ntlm=fsso_agent_for_ntlm,
            require_tfa=require_tfa,
            fsso_guest=fsso_guest,
            user_cert=user_cert,
            cert_http_header=cert_http_header,
            user_database=user_database,
            ssh_ca=ssh_ca,
            external_idp=external_idp,
            group_attr_type=group_attr_type,
            digest_algo=digest_algo,
            digest_rfc2069=digest_rfc2069,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.scheme import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/authentication/scheme",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/authentication/scheme/" + quote_path_param(name_value)

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
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | None = None,
        negotiate_ntlm: Literal["enable", "disable"] | None = None,
        kerberos_keytab: str | None = None,
        domain_controller: str | None = None,
        saml_server: str | None = None,
        saml_timeout: int | None = None,
        fsso_agent_for_ntlm: str | None = None,
        require_tfa: Literal["enable", "disable"] | None = None,
        fsso_guest: Literal["enable", "disable"] | None = None,
        user_cert: Literal["enable", "disable"] | None = None,
        cert_http_header: Literal["enable", "disable"] | None = None,
        user_database: str | list[str] | list[dict[str, Any]] | None = None,
        ssh_ca: str | None = None,
        external_idp: str | None = None,
        group_attr_type: Literal["display-name", "external-id"] | None = None,
        digest_algo: Literal["md5", "sha-256"] | list[str] | None = None,
        digest_rfc2069: Literal["enable", "disable"] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new authentication/scheme object.

        Configure Authentication Schemes.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Authentication scheme name.
            method: Authentication methods (default = basic).
            negotiate_ntlm: Enable/disable negotiate authentication for NTLM (default = disable).
            kerberos_keytab: Kerberos keytab setting.
            domain_controller: Domain controller setting.
            saml_server: SAML configuration.
            saml_timeout: SAML authentication timeout in seconds.
            fsso_agent_for_ntlm: FSSO agent to use for NTLM authentication.
            require_tfa: Enable/disable two-factor authentication (default = disable).
            fsso_guest: Enable/disable user fsso-guest authentication (default = disable).
            user_cert: Enable/disable authentication with user certificate (default = disable).
            cert_http_header: Enable/disable authentication with user certificate in Client-Cert HTTP header (default = disable).
            user_database: Authentication server to contain user information; "local-user-db" (default) or "123" (for LDAP).
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            ssh_ca: SSH CA name.
            external_idp: External identity provider configuration.
            group_attr_type: Group attribute type used to match SCIM groups (default = display-name).
            digest_algo: Digest Authentication Algorithms.
            digest_rfc2069: Enable/disable support for the deprecated RFC2069 Digest Client (no cnonce field, default = disable).
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.authentication_scheme.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Scheme.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.authentication_scheme.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Scheme.required_fields()) }}
            
            Use Scheme.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if user_database is not None:
            user_database = normalize_table_field(
                user_database,
                mkey="name",
                required_fields=['name'],
                field_name="user_database",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            method=method,
            negotiate_ntlm=negotiate_ntlm,
            kerberos_keytab=kerberos_keytab,
            domain_controller=domain_controller,
            saml_server=saml_server,
            saml_timeout=saml_timeout,
            fsso_agent_for_ntlm=fsso_agent_for_ntlm,
            require_tfa=require_tfa,
            fsso_guest=fsso_guest,
            user_cert=user_cert,
            cert_http_header=cert_http_header,
            user_database=user_database,
            ssh_ca=ssh_ca,
            external_idp=external_idp,
            group_attr_type=group_attr_type,
            digest_algo=digest_algo,
            digest_rfc2069=digest_rfc2069,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.scheme import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/authentication/scheme",
            )

        endpoint = "/authentication/scheme"
        
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
        Delete authentication/scheme object.

        Configure Authentication Schemes.

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
            >>> result = fgt.api.cmdb.authentication_scheme.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/authentication/scheme/" + quote_path_param(name)

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
        Check if authentication/scheme object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.authentication_scheme.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.authentication_scheme.exists(name=1):
            ...     fgt.api.cmdb.authentication_scheme.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/authentication/scheme"
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
        method: Literal["ntlm", "basic", "digest", "form", "negotiate", "fsso", "rsso", "ssh-publickey", "cert", "saml", "entra-sso"] | list[str] | list[dict[str, Any]] | None = None,
        negotiate_ntlm: Literal["enable", "disable"] | None = None,
        kerberos_keytab: str | None = None,
        domain_controller: str | None = None,
        saml_server: str | None = None,
        saml_timeout: int | None = None,
        fsso_agent_for_ntlm: str | None = None,
        require_tfa: Literal["enable", "disable"] | None = None,
        fsso_guest: Literal["enable", "disable"] | None = None,
        user_cert: Literal["enable", "disable"] | None = None,
        cert_http_header: Literal["enable", "disable"] | None = None,
        user_database: str | list[str] | list[dict[str, Any]] | None = None,
        ssh_ca: str | None = None,
        external_idp: str | None = None,
        group_attr_type: Literal["display-name", "external-id"] | None = None,
        digest_algo: Literal["md5", "sha-256"] | list[str] | list[dict[str, Any]] | None = None,
        digest_rfc2069: Literal["enable", "disable"] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update authentication/scheme object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            method: Field method
            negotiate_ntlm: Field negotiate-ntlm
            kerberos_keytab: Field kerberos-keytab
            domain_controller: Field domain-controller
            saml_server: Field saml-server
            saml_timeout: Field saml-timeout
            fsso_agent_for_ntlm: Field fsso-agent-for-ntlm
            require_tfa: Field require-tfa
            fsso_guest: Field fsso-guest
            user_cert: Field user-cert
            cert_http_header: Field cert-http-header
            user_database: Field user-database
            ssh_ca: Field ssh-ca
            external_idp: Field external-idp
            group_attr_type: Field group-attr-type
            digest_algo: Field digest-algo
            digest_rfc2069: Field digest-rfc2069
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.authentication_scheme.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.authentication_scheme.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.authentication_scheme.set(payload_dict=obj_data)
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
        if user_database is not None:
            user_database = normalize_table_field(
                user_database,
                mkey="name",
                required_fields=['name'],
                field_name="user_database",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            method=method,
            negotiate_ntlm=negotiate_ntlm,
            kerberos_keytab=kerberos_keytab,
            domain_controller=domain_controller,
            saml_server=saml_server,
            saml_timeout=saml_timeout,
            fsso_agent_for_ntlm=fsso_agent_for_ntlm,
            require_tfa=require_tfa,
            fsso_guest=fsso_guest,
            user_cert=user_cert,
            cert_http_header=cert_http_header,
            user_database=user_database,
            ssh_ca=ssh_ca,
            external_idp=external_idp,
            group_attr_type=group_attr_type,
            digest_algo=digest_algo,
            digest_rfc2069=digest_rfc2069,
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
        Move authentication/scheme object to a new position.
        
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
            >>> fgt.api.cmdb.authentication_scheme.move(
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
        
        endpoint = "/authentication/scheme"
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
        Clone authentication/scheme object.
        
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
            >>> fgt.api.cmdb.authentication_scheme.clone(
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
        
        endpoint = "/authentication/scheme"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




