"""
FortiOS CMDB - Vpn certificate local

Configuration endpoint for managing cmdb vpn/certificate/local objects.

API Endpoints:
    GET    /cmdb/vpn/certificate/local
    POST   /cmdb/vpn/certificate/local
    PUT    /cmdb/vpn/certificate/local/{identifier}
    DELETE /cmdb/vpn/certificate/local/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.vpn_certificate_local.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.vpn_certificate_local.post(
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
    SUPPORTS_DELETE = False
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
        Retrieve vpn/certificate/local configuration.

        Local keys and certificates.

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
            >>> # Get all vpn/certificate/local objects
            >>> result = fgt.api.cmdb.vpn_certificate_local.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific vpn/certificate/local by name
            >>> result = fgt.api.cmdb.vpn_certificate_local.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.vpn_certificate_local.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.vpn_certificate_local.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.vpn_certificate_local.get_schema()

        See Also:
            - post(): Create new vpn/certificate/local object
            - put(): Update existing vpn/certificate/local object
            - delete(): Remove vpn/certificate/local object
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
            endpoint = "/vpn.certificate/local/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/vpn.certificate/local"
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
            >>> schema = fgt.api.cmdb.vpn_certificate_local.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.vpn_certificate_local.get_schema(format="json-schema")
        
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
        password: Any | None = None,
        comments: str | None = None,
        private_key: str | None = None,
        certificate: str | None = None,
        csr: str | None = None,
        state: str | None = None,
        scep_url: str | None = None,
        range: Literal["global", "vdom"] | None = None,
        source: Literal["factory", "user", "bundle"] | None = None,
        auto_regenerate_days: int | None = None,
        auto_regenerate_days_warning: int | None = None,
        scep_password: Any | None = None,
        ca_identifier: str | None = None,
        name_encoding: Literal["printable", "utf8"] | None = None,
        source_ip: str | None = None,
        ike_localid: str | None = None,
        ike_localid_type: Literal["asn1dn", "fqdn"] | None = None,
        enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"] | None = None,
        private_key_retain: Literal["enable", "disable"] | None = None,
        cmp_server: str | None = None,
        cmp_path: str | None = None,
        cmp_server_cert: str | None = None,
        cmp_regeneration_method: Literal["keyupate", "renewal"] | None = None,
        acme_ca_url: str | None = None,
        acme_domain: str | None = None,
        acme_email: str | None = None,
        acme_eab_key_id: str | None = None,
        acme_eab_key_hmac: Any | None = None,
        acme_rsa_key_size: int | None = None,
        acme_renew_window: int | None = None,
        est_server: str | None = None,
        est_ca_id: str | None = None,
        est_http_username: str | None = None,
        est_http_password: Any | None = None,
        est_client_cert: str | None = None,
        est_server_cert: str | None = None,
        est_srp_username: str | None = None,
        est_srp_password: Any | None = None,
        est_regeneration_method: Literal["create-new-key", "use-existing-key"] | None = None,
        details: Any | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing vpn/certificate/local object.

        Local keys and certificates.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Name.
            password: Password as a PEM file.
            comments: Comment.
            private_key: PEM format key encrypted with a password.
            certificate: PEM format certificate.
            csr: Certificate Signing Request.
            state: Certificate Signing Request State.
            scep_url: SCEP server URL.
            range: Either a global or VDOM IP address range for the certificate.
            source: Certificate source type.
            auto_regenerate_days: Number of days to wait before expiry of an updated local certificate is requested (0 = disabled).
            auto_regenerate_days_warning: Number of days to wait before an expiry warning message is generated (0 = disabled).
            scep_password: SCEP server challenge password for auto-regeneration.
            ca_identifier: CA identifier of the CA server for signing via SCEP.
            name_encoding: Name encoding method for auto-regeneration.
            source_ip: Source IP address for communications to the SCEP server.
            ike_localid: Local ID the FortiGate uses for authentication as a VPN client.
            ike_localid_type: IKE local ID type.
            enroll_protocol: Certificate enrollment protocol.
            private_key_retain: Enable/disable retention of private key during SCEP renewal (default = disable).
            cmp_server: Address and port for CMP server (format = address:port).
            cmp_path: Path location inside CMP server.
            cmp_server_cert: CMP server certificate.
            cmp_regeneration_method: CMP auto-regeneration method.
            acme_ca_url: The URL for the ACME CA server (Let's Encrypt is the default provider).
            acme_domain: A valid domain that resolves to this FortiGate unit.
            acme_email: Contact email address that is required by some CAs like LetsEncrypt.
            acme_eab_key_id: External Account Binding Key ID (optional setting).
            acme_eab_key_hmac: External Account Binding HMAC Key (URL-encoded base64).
            acme_rsa_key_size: Length of the RSA private key of the generated cert (Minimum 2048 bits).
            acme_renew_window: Beginning of the renewal window (in days before certificate expiration, 30 by default).
            est_server: Address and port for EST server (e.g. https://example.com:1234).
            est_ca_id: CA identifier of the CA server for signing via EST.
            est_http_username: HTTP Authentication username for signing via EST.
            est_http_password: HTTP Authentication password for signing via EST.
            est_client_cert: Certificate used to authenticate this FortiGate to EST server.
            est_server_cert: EST server's certificate must be verifiable by this certificate to be authenticated.
            est_srp_username: EST SRP authentication username.
            est_srp_password: EST SRP authentication password.
            est_regeneration_method: EST behavioral options during re-enrollment.
            details: Print local certificate detailed information.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.vpn_certificate_local.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.vpn_certificate_local.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            password=password,
            comments=comments,
            private_key=private_key,
            certificate=certificate,
            csr=csr,
            state=state,
            scep_url=scep_url,
            range=range,
            source=source,
            auto_regenerate_days=auto_regenerate_days,
            auto_regenerate_days_warning=auto_regenerate_days_warning,
            scep_password=scep_password,
            ca_identifier=ca_identifier,
            name_encoding=name_encoding,
            source_ip=source_ip,
            ike_localid=ike_localid,
            ike_localid_type=ike_localid_type,
            enroll_protocol=enroll_protocol,
            private_key_retain=private_key_retain,
            cmp_server=cmp_server,
            cmp_path=cmp_path,
            cmp_server_cert=cmp_server_cert,
            cmp_regeneration_method=cmp_regeneration_method,
            acme_ca_url=acme_ca_url,
            acme_domain=acme_domain,
            acme_email=acme_email,
            acme_eab_key_id=acme_eab_key_id,
            acme_eab_key_hmac=acme_eab_key_hmac,
            acme_rsa_key_size=acme_rsa_key_size,
            acme_renew_window=acme_renew_window,
            est_server=est_server,
            est_ca_id=est_ca_id,
            est_http_username=est_http_username,
            est_http_password=est_http_password,
            est_client_cert=est_client_cert,
            est_server_cert=est_server_cert,
            est_srp_username=est_srp_username,
            est_srp_password=est_srp_password,
            est_regeneration_method=est_regeneration_method,
            details=details,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.local import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/vpn/certificate/local",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/vpn.certificate/local/" + quote_path_param(name_value)

        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data=payload_data, vdom=vdom        )

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
        password: Any | None = None,
        comments: str | None = None,
        private_key: str | None = None,
        certificate: str | None = None,
        csr: str | None = None,
        state: str | None = None,
        scep_url: str | None = None,
        range: Literal["global", "vdom"] | None = None,
        source: Literal["factory", "user", "bundle"] | None = None,
        auto_regenerate_days: int | None = None,
        auto_regenerate_days_warning: int | None = None,
        scep_password: Any | None = None,
        ca_identifier: str | None = None,
        name_encoding: Literal["printable", "utf8"] | None = None,
        source_ip: str | None = None,
        ike_localid: str | None = None,
        ike_localid_type: Literal["asn1dn", "fqdn"] | None = None,
        enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"] | None = None,
        private_key_retain: Literal["enable", "disable"] | None = None,
        cmp_server: str | None = None,
        cmp_path: str | None = None,
        cmp_server_cert: str | None = None,
        cmp_regeneration_method: Literal["keyupate", "renewal"] | None = None,
        acme_ca_url: str | None = None,
        acme_domain: str | None = None,
        acme_email: str | None = None,
        acme_eab_key_id: str | None = None,
        acme_eab_key_hmac: Any | None = None,
        acme_rsa_key_size: int | None = None,
        acme_renew_window: int | None = None,
        est_server: str | None = None,
        est_ca_id: str | None = None,
        est_http_username: str | None = None,
        est_http_password: Any | None = None,
        est_client_cert: str | None = None,
        est_server_cert: str | None = None,
        est_srp_username: str | None = None,
        est_srp_password: Any | None = None,
        est_regeneration_method: Literal["create-new-key", "use-existing-key"] | None = None,
        details: Any | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new vpn/certificate/local object.

        Local keys and certificates.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Name.
            password: Password as a PEM file.
            comments: Comment.
            private_key: PEM format key encrypted with a password.
            certificate: PEM format certificate.
            csr: Certificate Signing Request.
            state: Certificate Signing Request State.
            scep_url: SCEP server URL.
            range: Either a global or VDOM IP address range for the certificate.
            source: Certificate source type.
            auto_regenerate_days: Number of days to wait before expiry of an updated local certificate is requested (0 = disabled).
            auto_regenerate_days_warning: Number of days to wait before an expiry warning message is generated (0 = disabled).
            scep_password: SCEP server challenge password for auto-regeneration.
            ca_identifier: CA identifier of the CA server for signing via SCEP.
            name_encoding: Name encoding method for auto-regeneration.
            source_ip: Source IP address for communications to the SCEP server.
            ike_localid: Local ID the FortiGate uses for authentication as a VPN client.
            ike_localid_type: IKE local ID type.
            enroll_protocol: Certificate enrollment protocol.
            private_key_retain: Enable/disable retention of private key during SCEP renewal (default = disable).
            cmp_server: Address and port for CMP server (format = address:port).
            cmp_path: Path location inside CMP server.
            cmp_server_cert: CMP server certificate.
            cmp_regeneration_method: CMP auto-regeneration method.
            acme_ca_url: The URL for the ACME CA server (Let's Encrypt is the default provider).
            acme_domain: A valid domain that resolves to this FortiGate unit.
            acme_email: Contact email address that is required by some CAs like LetsEncrypt.
            acme_eab_key_id: External Account Binding Key ID (optional setting).
            acme_eab_key_hmac: External Account Binding HMAC Key (URL-encoded base64).
            acme_rsa_key_size: Length of the RSA private key of the generated cert (Minimum 2048 bits).
            acme_renew_window: Beginning of the renewal window (in days before certificate expiration, 30 by default).
            est_server: Address and port for EST server (e.g. https://example.com:1234).
            est_ca_id: CA identifier of the CA server for signing via EST.
            est_http_username: HTTP Authentication username for signing via EST.
            est_http_password: HTTP Authentication password for signing via EST.
            est_client_cert: Certificate used to authenticate this FortiGate to EST server.
            est_server_cert: EST server's certificate must be verifiable by this certificate to be authenticated.
            est_srp_username: EST SRP authentication username.
            est_srp_password: EST SRP authentication password.
            est_regeneration_method: EST behavioral options during re-enrollment.
            details: Print local certificate detailed information.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.vpn_certificate_local.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Local.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.vpn_certificate_local.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Local.required_fields()) }}
            
            Use Local.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            password=password,
            comments=comments,
            private_key=private_key,
            certificate=certificate,
            csr=csr,
            state=state,
            scep_url=scep_url,
            range=range,
            source=source,
            auto_regenerate_days=auto_regenerate_days,
            auto_regenerate_days_warning=auto_regenerate_days_warning,
            scep_password=scep_password,
            ca_identifier=ca_identifier,
            name_encoding=name_encoding,
            source_ip=source_ip,
            ike_localid=ike_localid,
            ike_localid_type=ike_localid_type,
            enroll_protocol=enroll_protocol,
            private_key_retain=private_key_retain,
            cmp_server=cmp_server,
            cmp_path=cmp_path,
            cmp_server_cert=cmp_server_cert,
            cmp_regeneration_method=cmp_regeneration_method,
            acme_ca_url=acme_ca_url,
            acme_domain=acme_domain,
            acme_email=acme_email,
            acme_eab_key_id=acme_eab_key_id,
            acme_eab_key_hmac=acme_eab_key_hmac,
            acme_rsa_key_size=acme_rsa_key_size,
            acme_renew_window=acme_renew_window,
            est_server=est_server,
            est_ca_id=est_ca_id,
            est_http_username=est_http_username,
            est_http_password=est_http_password,
            est_client_cert=est_client_cert,
            est_server_cert=est_server_cert,
            est_srp_username=est_srp_username,
            est_srp_password=est_srp_password,
            est_regeneration_method=est_regeneration_method,
            details=details,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.local import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/vpn/certificate/local",
            )

        endpoint = "/vpn.certificate/local"
        
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
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete vpn/certificate/local object.

        Local keys and certificates.

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
            >>> result = fgt.api.cmdb.vpn_certificate_local.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/vpn.certificate/local/" + quote_path_param(name)

        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, vdom=vdom        )

    def exists(
        self,
        name: str,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if vpn/certificate/local object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.vpn_certificate_local.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.vpn_certificate_local.exists(name=1):
            ...     fgt.api.cmdb.vpn_certificate_local.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/vpn.certificate/local"
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
        password: Any | None = None,
        comments: str | None = None,
        private_key: str | None = None,
        certificate: str | None = None,
        csr: str | None = None,
        state: str | None = None,
        scep_url: str | None = None,
        range: Literal["global", "vdom"] | None = None,
        source: Literal["factory", "user", "bundle"] | None = None,
        auto_regenerate_days: int | None = None,
        auto_regenerate_days_warning: int | None = None,
        scep_password: Any | None = None,
        ca_identifier: str | None = None,
        name_encoding: Literal["printable", "utf8"] | None = None,
        source_ip: str | None = None,
        ike_localid: str | None = None,
        ike_localid_type: Literal["asn1dn", "fqdn"] | None = None,
        enroll_protocol: Literal["none", "scep", "cmpv2", "acme2", "est"] | None = None,
        private_key_retain: Literal["enable", "disable"] | None = None,
        cmp_server: str | None = None,
        cmp_path: str | None = None,
        cmp_server_cert: str | None = None,
        cmp_regeneration_method: Literal["keyupate", "renewal"] | None = None,
        acme_ca_url: str | None = None,
        acme_domain: str | None = None,
        acme_email: str | None = None,
        acme_eab_key_id: str | None = None,
        acme_eab_key_hmac: Any | None = None,
        acme_rsa_key_size: int | None = None,
        acme_renew_window: int | None = None,
        est_server: str | None = None,
        est_ca_id: str | None = None,
        est_http_username: str | None = None,
        est_http_password: Any | None = None,
        est_client_cert: str | None = None,
        est_server_cert: str | None = None,
        est_srp_username: str | None = None,
        est_srp_password: Any | None = None,
        est_regeneration_method: Literal["create-new-key", "use-existing-key"] | None = None,
        details: Any | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update vpn/certificate/local object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            password: Field password
            comments: Field comments
            private_key: Field private-key
            certificate: Field certificate
            csr: Field csr
            state: Field state
            scep_url: Field scep-url
            range: Field range
            source: Field source
            auto_regenerate_days: Field auto-regenerate-days
            auto_regenerate_days_warning: Field auto-regenerate-days-warning
            scep_password: Field scep-password
            ca_identifier: Field ca-identifier
            name_encoding: Field name-encoding
            source_ip: Field source-ip
            ike_localid: Field ike-localid
            ike_localid_type: Field ike-localid-type
            enroll_protocol: Field enroll-protocol
            private_key_retain: Field private-key-retain
            cmp_server: Field cmp-server
            cmp_path: Field cmp-path
            cmp_server_cert: Field cmp-server-cert
            cmp_regeneration_method: Field cmp-regeneration-method
            acme_ca_url: Field acme-ca-url
            acme_domain: Field acme-domain
            acme_email: Field acme-email
            acme_eab_key_id: Field acme-eab-key-id
            acme_eab_key_hmac: Field acme-eab-key-hmac
            acme_rsa_key_size: Field acme-rsa-key-size
            acme_renew_window: Field acme-renew-window
            est_server: Field est-server
            est_ca_id: Field est-ca-id
            est_http_username: Field est-http-username
            est_http_password: Field est-http-password
            est_client_cert: Field est-client-cert
            est_server_cert: Field est-server-cert
            est_srp_username: Field est-srp-username
            est_srp_password: Field est-srp-password
            est_regeneration_method: Field est-regeneration-method
            details: Field details
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.vpn_certificate_local.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.vpn_certificate_local.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.vpn_certificate_local.set(payload_dict=obj_data)
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
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            password=password,
            comments=comments,
            private_key=private_key,
            certificate=certificate,
            csr=csr,
            state=state,
            scep_url=scep_url,
            range=range,
            source=source,
            auto_regenerate_days=auto_regenerate_days,
            auto_regenerate_days_warning=auto_regenerate_days_warning,
            scep_password=scep_password,
            ca_identifier=ca_identifier,
            name_encoding=name_encoding,
            source_ip=source_ip,
            ike_localid=ike_localid,
            ike_localid_type=ike_localid_type,
            enroll_protocol=enroll_protocol,
            private_key_retain=private_key_retain,
            cmp_server=cmp_server,
            cmp_path=cmp_path,
            cmp_server_cert=cmp_server_cert,
            cmp_regeneration_method=cmp_regeneration_method,
            acme_ca_url=acme_ca_url,
            acme_domain=acme_domain,
            acme_email=acme_email,
            acme_eab_key_id=acme_eab_key_id,
            acme_eab_key_hmac=acme_eab_key_hmac,
            acme_rsa_key_size=acme_rsa_key_size,
            acme_renew_window=acme_renew_window,
            est_server=est_server,
            est_ca_id=est_ca_id,
            est_http_username=est_http_username,
            est_http_password=est_http_password,
            est_client_cert=est_client_cert,
            est_server_cert=est_server_cert,
            est_srp_username=est_srp_username,
            est_srp_password=est_srp_password,
            est_regeneration_method=est_regeneration_method,
            details=details,
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
        Move vpn/certificate/local object to a new position.
        
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
            >>> fgt.api.cmdb.vpn_certificate_local.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.vpn_certificate_local.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.vpn_certificate_local.move(
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
        endpoint = "/vpn.certificate/local/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





