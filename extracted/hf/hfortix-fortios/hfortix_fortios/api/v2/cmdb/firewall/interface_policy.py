"""
FortiOS CMDB - Firewall interface_policy

Configuration endpoint for managing cmdb firewall/interface_policy objects.

API Endpoints:
    GET    /cmdb/firewall/interface_policy
    POST   /cmdb/firewall/interface_policy
    PUT    /cmdb/firewall/interface_policy/{identifier}
    DELETE /cmdb/firewall/interface_policy/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.firewall_interface_policy.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.firewall_interface_policy.post(
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

class InterfacePolicy(CRUDEndpoint, MetadataMixin):
    """InterfacePolicy Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "interface_policy"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "srcaddr": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "dstaddr": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "service": {
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
        """Initialize InterfacePolicy endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        policyid: int | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve firewall/interface_policy configuration.

        Configure IPv4 interface policies.

        Args:
            policyid: Integer identifier to retrieve specific object.
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
            >>> # Get all firewall/interface_policy objects
            >>> result = fgt.api.cmdb.firewall_interface_policy.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific firewall/interface_policy by policyid
            >>> result = fgt.api.cmdb.firewall_interface_policy.get(policyid=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.firewall_interface_policy.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.firewall_interface_policy.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.firewall_interface_policy.get_schema()

        See Also:
            - post(): Create new firewall/interface_policy object
            - put(): Update existing firewall/interface_policy object
            - delete(): Remove firewall/interface_policy object
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
        
        if policyid:
            endpoint = "/firewall/interface-policy/" + quote_path_param(policyid)
            unwrap_single = True
        else:
            endpoint = "/firewall/interface-policy"
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
            >>> schema = fgt.api.cmdb.firewall_interface_policy.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.firewall_interface_policy.get_schema(format="json-schema")
        
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
        policyid: int | None = None,
        uuid: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        comments: str | None = None,
        logtraffic: Literal["all", "utm", "disable"] | None = None,
        interface: str | None = None,
        srcaddr: str | list[str] | list[dict[str, Any]] | None = None,
        dstaddr: str | list[str] | list[dict[str, Any]] | None = None,
        service: str | list[str] | list[dict[str, Any]] | None = None,
        application_list_status: Literal["enable", "disable"] | None = None,
        application_list: str | None = None,
        ips_sensor_status: Literal["enable", "disable"] | None = None,
        ips_sensor: str | None = None,
        dsri: Literal["enable", "disable"] | None = None,
        av_profile_status: Literal["enable", "disable"] | None = None,
        av_profile: str | None = None,
        webfilter_profile_status: Literal["enable", "disable"] | None = None,
        webfilter_profile: str | None = None,
        casb_profile_status: Literal["enable", "disable"] | None = None,
        casb_profile: str | None = None,
        emailfilter_profile_status: Literal["enable", "disable"] | None = None,
        emailfilter_profile: str | None = None,
        dlp_profile_status: Literal["enable", "disable"] | None = None,
        dlp_profile: str | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing firewall/interface_policy object.

        Configure IPv4 interface policies.

        Args:
            payload_dict: Object data as dict. Must include policyid (primary key).
            policyid: Policy ID (0 - 4294967295).
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            status: Enable/disable this policy.
            comments: Comments.
            logtraffic: Logging type to be used in this policy (Options: all | utm | disable, Default: utm).
            interface: Monitored interface name from available interfaces.
            srcaddr: Address object to limit traffic monitoring to network traffic sent from the specified address or range.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dstaddr: Address object to limit traffic monitoring to network traffic sent to the specified address or range.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            service: Service object from available options.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            application_list_status: Enable/disable application control.
            application_list: Application list name.
            ips_sensor_status: Enable/disable IPS.
            ips_sensor: IPS sensor name.
            dsri: Enable/disable DSRI.
            av_profile_status: Enable/disable antivirus.
            av_profile: Antivirus profile.
            webfilter_profile_status: Enable/disable web filtering.
            webfilter_profile: Web filter profile.
            casb_profile_status: Enable/disable CASB.
            casb_profile: CASB profile.
            emailfilter_profile_status: Enable/disable email filter.
            emailfilter_profile: Email filter profile.
            dlp_profile_status: Enable/disable DLP.
            dlp_profile: DLP profile name.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If policyid is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.firewall_interface_policy.put(
            ...     policyid=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "policyid": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.firewall_interface_policy.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if srcaddr is not None:
            srcaddr = normalize_table_field(
                srcaddr,
                mkey="name",
                required_fields=['name'],
                field_name="srcaddr",
                example="[{'name': 'value'}]",
            )
        if dstaddr is not None:
            dstaddr = normalize_table_field(
                dstaddr,
                mkey="name",
                required_fields=['name'],
                field_name="dstaddr",
                example="[{'name': 'value'}]",
            )
        if service is not None:
            service = normalize_table_field(
                service,
                mkey="name",
                required_fields=['name'],
                field_name="service",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            policyid=policyid,
            uuid=uuid,
            status=status,
            comments=comments,
            logtraffic=logtraffic,
            interface=interface,
            srcaddr=srcaddr,
            dstaddr=dstaddr,
            service=service,
            application_list_status=application_list_status,
            application_list=application_list,
            ips_sensor_status=ips_sensor_status,
            ips_sensor=ips_sensor,
            dsri=dsri,
            av_profile_status=av_profile_status,
            av_profile=av_profile,
            webfilter_profile_status=webfilter_profile_status,
            webfilter_profile=webfilter_profile,
            casb_profile_status=casb_profile_status,
            casb_profile=casb_profile,
            emailfilter_profile_status=emailfilter_profile_status,
            emailfilter_profile=emailfilter_profile,
            dlp_profile_status=dlp_profile_status,
            dlp_profile=dlp_profile,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.interface_policy import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/interface_policy",
            )
        
        policyid_value = payload_data.get("policyid")
        if not policyid_value:
            raise ValueError("policyid is required for PUT")
        endpoint = "/firewall/interface-policy/" + quote_path_param(policyid_value)

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
        policyid: int | None = None,
        uuid: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        comments: str | None = None,
        logtraffic: Literal["all", "utm", "disable"] | None = None,
        interface: str | None = None,
        srcaddr: str | list[str] | list[dict[str, Any]] | None = None,
        dstaddr: str | list[str] | list[dict[str, Any]] | None = None,
        service: str | list[str] | list[dict[str, Any]] | None = None,
        application_list_status: Literal["enable", "disable"] | None = None,
        application_list: str | None = None,
        ips_sensor_status: Literal["enable", "disable"] | None = None,
        ips_sensor: str | None = None,
        dsri: Literal["enable", "disable"] | None = None,
        av_profile_status: Literal["enable", "disable"] | None = None,
        av_profile: str | None = None,
        webfilter_profile_status: Literal["enable", "disable"] | None = None,
        webfilter_profile: str | None = None,
        casb_profile_status: Literal["enable", "disable"] | None = None,
        casb_profile: str | None = None,
        emailfilter_profile_status: Literal["enable", "disable"] | None = None,
        emailfilter_profile: str | None = None,
        dlp_profile_status: Literal["enable", "disable"] | None = None,
        dlp_profile: str | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new firewall/interface_policy object.

        Configure IPv4 interface policies.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            policyid: Policy ID (0 - 4294967295).
            uuid: Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
            status: Enable/disable this policy.
            comments: Comments.
            logtraffic: Logging type to be used in this policy (Options: all | utm | disable, Default: utm).
            interface: Monitored interface name from available interfaces.
            srcaddr: Address object to limit traffic monitoring to network traffic sent from the specified address or range.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            dstaddr: Address object to limit traffic monitoring to network traffic sent to the specified address or range.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            service: Service object from available options.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            application_list_status: Enable/disable application control.
            application_list: Application list name.
            ips_sensor_status: Enable/disable IPS.
            ips_sensor: IPS sensor name.
            dsri: Enable/disable DSRI.
            av_profile_status: Enable/disable antivirus.
            av_profile: Antivirus profile.
            webfilter_profile_status: Enable/disable web filtering.
            webfilter_profile: Web filter profile.
            casb_profile_status: Enable/disable CASB.
            casb_profile: CASB profile.
            emailfilter_profile_status: Enable/disable email filter.
            emailfilter_profile: Email filter profile.
            dlp_profile_status: Enable/disable DLP.
            dlp_profile: DLP profile name.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.firewall_interface_policy.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created policyid: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = InterfacePolicy.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.firewall_interface_policy.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(InterfacePolicy.required_fields()) }}
            
            Use InterfacePolicy.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if srcaddr is not None:
            srcaddr = normalize_table_field(
                srcaddr,
                mkey="name",
                required_fields=['name'],
                field_name="srcaddr",
                example="[{'name': 'value'}]",
            )
        if dstaddr is not None:
            dstaddr = normalize_table_field(
                dstaddr,
                mkey="name",
                required_fields=['name'],
                field_name="dstaddr",
                example="[{'name': 'value'}]",
            )
        if service is not None:
            service = normalize_table_field(
                service,
                mkey="name",
                required_fields=['name'],
                field_name="service",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            policyid=policyid,
            uuid=uuid,
            status=status,
            comments=comments,
            logtraffic=logtraffic,
            interface=interface,
            srcaddr=srcaddr,
            dstaddr=dstaddr,
            service=service,
            application_list_status=application_list_status,
            application_list=application_list,
            ips_sensor_status=ips_sensor_status,
            ips_sensor=ips_sensor,
            dsri=dsri,
            av_profile_status=av_profile_status,
            av_profile=av_profile,
            webfilter_profile_status=webfilter_profile_status,
            webfilter_profile=webfilter_profile,
            casb_profile_status=casb_profile_status,
            casb_profile=casb_profile,
            emailfilter_profile_status=emailfilter_profile_status,
            emailfilter_profile=emailfilter_profile,
            dlp_profile_status=dlp_profile_status,
            dlp_profile=dlp_profile,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.interface_policy import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/firewall/interface_policy",
            )

        endpoint = "/firewall/interface-policy"
        
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
        policyid: int | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete firewall/interface_policy object.

        Configure IPv4 interface policies.

        Args:
            policyid: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If policyid is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.firewall_interface_policy.delete(policyid=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not policyid:
            raise ValueError("policyid is required for DELETE")
        endpoint = "/firewall/interface-policy/" + quote_path_param(policyid)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        policyid: int,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if firewall/interface_policy object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            policyid: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.firewall_interface_policy.exists(policyid=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.firewall_interface_policy.exists(policyid=1):
            ...     fgt.api.cmdb.firewall_interface_policy.delete(policyid=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/firewall/interface-policy"
        endpoint = f"{endpoint}/{quote_path_param(policyid)}"
        
        try:
            result = self.get(policyid=policyid, vdom=vdom)
            
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
        policyid: int | None = None,
        uuid: str | None = None,
        status: Literal["enable", "disable"] | None = None,
        comments: str | None = None,
        logtraffic: Literal["all", "utm", "disable"] | None = None,
        interface: str | None = None,
        srcaddr: str | list[str] | list[dict[str, Any]] | None = None,
        dstaddr: str | list[str] | list[dict[str, Any]] | None = None,
        service: str | list[str] | list[dict[str, Any]] | None = None,
        application_list_status: Literal["enable", "disable"] | None = None,
        application_list: str | None = None,
        ips_sensor_status: Literal["enable", "disable"] | None = None,
        ips_sensor: str | None = None,
        dsri: Literal["enable", "disable"] | None = None,
        av_profile_status: Literal["enable", "disable"] | None = None,
        av_profile: str | None = None,
        webfilter_profile_status: Literal["enable", "disable"] | None = None,
        webfilter_profile: str | None = None,
        casb_profile_status: Literal["enable", "disable"] | None = None,
        casb_profile: str | None = None,
        emailfilter_profile_status: Literal["enable", "disable"] | None = None,
        emailfilter_profile: str | None = None,
        dlp_profile_status: Literal["enable", "disable"] | None = None,
        dlp_profile: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update firewall/interface_policy object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (policyid) in the payload.

        Args:
            payload_dict: Resource data including policyid (primary key)
            policyid: Field policyid
            uuid: Field uuid
            status: Field status
            comments: Field comments
            logtraffic: Field logtraffic
            interface: Field interface
            srcaddr: Field srcaddr
            dstaddr: Field dstaddr
            service: Field service
            application_list_status: Field application-list-status
            application_list: Field application-list
            ips_sensor_status: Field ips-sensor-status
            ips_sensor: Field ips-sensor
            dsri: Field dsri
            av_profile_status: Field av-profile-status
            av_profile: Field av-profile
            webfilter_profile_status: Field webfilter-profile-status
            webfilter_profile: Field webfilter-profile
            casb_profile_status: Field casb-profile-status
            casb_profile: Field casb-profile
            emailfilter_profile_status: Field emailfilter-profile-status
            emailfilter_profile: Field emailfilter-profile
            dlp_profile_status: Field dlp-profile-status
            dlp_profile: Field dlp-profile
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If policyid is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.firewall_interface_policy.set(
            ...     policyid=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "policyid": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.firewall_interface_policy.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.firewall_interface_policy.set(payload_dict=obj_data)
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
        if srcaddr is not None:
            srcaddr = normalize_table_field(
                srcaddr,
                mkey="name",
                required_fields=['name'],
                field_name="srcaddr",
                example="[{'name': 'value'}]",
            )
        if dstaddr is not None:
            dstaddr = normalize_table_field(
                dstaddr,
                mkey="name",
                required_fields=['name'],
                field_name="dstaddr",
                example="[{'name': 'value'}]",
            )
        if service is not None:
            service = normalize_table_field(
                service,
                mkey="name",
                required_fields=['name'],
                field_name="service",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            policyid=policyid,
            uuid=uuid,
            status=status,
            comments=comments,
            logtraffic=logtraffic,
            interface=interface,
            srcaddr=srcaddr,
            dstaddr=dstaddr,
            service=service,
            application_list_status=application_list_status,
            application_list=application_list,
            ips_sensor_status=ips_sensor_status,
            ips_sensor=ips_sensor,
            dsri=dsri,
            av_profile_status=av_profile_status,
            av_profile=av_profile,
            webfilter_profile_status=webfilter_profile_status,
            webfilter_profile=webfilter_profile,
            casb_profile_status=casb_profile_status,
            casb_profile=casb_profile,
            emailfilter_profile_status=emailfilter_profile_status,
            emailfilter_profile=emailfilter_profile,
            dlp_profile_status=dlp_profile_status,
            dlp_profile=dlp_profile,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("policyid")
        if not mkey_value:
            raise ValueError("policyid is required for set()")
        
        # Check if resource exists
        if self.exists(policyid=mkey_value, vdom=vdom):
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
        policyid: int,
        action: Literal["before", "after"],
        reference_policyid: int,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move firewall/interface_policy object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            policyid: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_policyid: Identifier of reference object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.firewall_interface_policy.move(
            ...     policyid=100,
            ...     action="before",
            ...     reference_policyid=50
            ... )
        """
        # Build params for move operation
        params = {
            "policyid": policyid,
            "action": "move",
            action: reference_policyid,
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/firewall/interface-policy"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        policyid: int,
        new_policyid: int,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone firewall/interface_policy object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            policyid: Identifier of object to clone
            new_policyid: Identifier for the cloned object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.firewall_interface_policy.clone(
            ...     policyid=1,
            ...     new_policyid=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "policyid": policyid,
            "new_policyid": new_policyid,
            "action": "clone",
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/firewall/interface-policy"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




