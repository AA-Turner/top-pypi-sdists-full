"""
FortiOS CMDB - User nac_policy

Configuration endpoint for managing cmdb user/nac_policy objects.

API Endpoints:
    GET    /cmdb/user/nac_policy
    POST   /cmdb/user/nac_policy
    PUT    /cmdb/user/nac_policy/{identifier}
    DELETE /cmdb/user/nac_policy/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.user_nac_policy.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.user_nac_policy.post(
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

class NacPolicy(CRUDEndpoint, MetadataMixin):
    """NacPolicy Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "nac_policy"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "severity": {
            "mkey": "severity-num",
            "required_fields": ['severity-num'],
            "example": "[{'severity-num': 1}]",
        },
        "switch_group": {
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
        """Initialize NacPolicy endpoint."""
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
        Retrieve user/nac_policy configuration.

        Configure NAC policy matching pattern to identify matching NAC devices.

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
            >>> # Get all user/nac_policy objects
            >>> result = fgt.api.cmdb.user_nac_policy.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific user/nac_policy by name
            >>> result = fgt.api.cmdb.user_nac_policy.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.user_nac_policy.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.user_nac_policy.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.user_nac_policy.get_schema()

        See Also:
            - post(): Create new user/nac_policy object
            - put(): Update existing user/nac_policy object
            - delete(): Remove user/nac_policy object
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
            endpoint = "/user/nac-policy/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/user/nac-policy"
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
            >>> schema = fgt.api.cmdb.user_nac_policy.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.user_nac_policy.get_schema(format="json-schema")
        
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
        description: str | None = None,
        category: Literal["device", "firewall-user", "ems-tag", "fortivoice-tag", "vulnerability"] | None = None,
        status: Literal["enable", "disable"] | None = None,
        match_type: Literal["dynamic", "override"] | None = None,
        match_period: int | None = None,
        match_remove: Literal["default", "link-down"] | None = None,
        mac: str | None = None,
        hw_vendor: str | None = None,
        type: str | None = None,
        family: str | None = None,
        os: str | None = None,
        hw_version: str | None = None,
        sw_version: str | None = None,
        host: str | None = None,
        user: str | None = None,
        src: str | None = None,
        user_group: str | None = None,
        ems_tag: str | None = None,
        fortivoice_tag: str | None = None,
        severity: str | list[str] | list[dict[str, Any]] | None = None,
        switch_fortilink: str | None = None,
        switch_group: str | list[str] | list[dict[str, Any]] | None = None,
        switch_mac_policy: str | None = None,
        firewall_address: str | None = None,
        ssid_policy: str | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing user/nac_policy object.

        Configure NAC policy matching pattern to identify matching NAC devices.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: NAC policy name.
            description: Description for the NAC policy matching pattern.
            category: Category of NAC policy.
            status: Enable/disable NAC policy.
            match_type: Match and retain the devices based on the type.
            match_period: Number of days the matched devices will be retained (0 - always retain)
            match_remove: Options to remove the matched override devices.
            mac: NAC policy matching MAC address.
            hw_vendor: NAC policy matching hardware vendor.
            type: NAC policy matching type.
            family: NAC policy matching family.
            os: NAC policy matching operating system.
            hw_version: NAC policy matching hardware version.
            sw_version: NAC policy matching software version.
            host: NAC policy matching host.
            user: NAC policy matching user.
            src: NAC policy matching source.
            user_group: NAC policy matching user group.
            ems_tag: NAC policy matching EMS tag.
            fortivoice_tag: NAC policy matching FortiVoice tag.
            severity: NAC policy matching devices vulnerability severity lists.
                Default format: [{'severity-num': 1}]
                Supported formats:
                  - Single string: "value" → [{'severity-num': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'severity-num': 'val1'}, ...]
                  - List of dicts: [{'severity-num': 1}] (recommended)
            switch_fortilink: FortiLink interface for which this NAC policy belongs to.
            switch_group: List of managed FortiSwitch groups on which NAC policy can be applied.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            switch_mac_policy: Switch MAC policy action to be applied on the matched NAC policy.
            firewall_address: Dynamic firewall address to associate MAC which match this policy.
            ssid_policy: SSID policy to be applied on the matched NAC policy.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.user_nac_policy.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.user_nac_policy.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if severity is not None:
            severity = normalize_table_field(
                severity,
                mkey="severity-num",
                required_fields=['severity-num'],
                field_name="severity",
                example="[{'severity-num': 1}]",
            )
        if switch_group is not None:
            switch_group = normalize_table_field(
                switch_group,
                mkey="name",
                required_fields=['name'],
                field_name="switch_group",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            description=description,
            category=category,
            status=status,
            match_type=match_type,
            match_period=match_period,
            match_remove=match_remove,
            mac=mac,
            hw_vendor=hw_vendor,
            type=type,
            family=family,
            os=os,
            hw_version=hw_version,
            sw_version=sw_version,
            host=host,
            user=user,
            src=src,
            user_group=user_group,
            ems_tag=ems_tag,
            fortivoice_tag=fortivoice_tag,
            severity=severity,
            switch_fortilink=switch_fortilink,
            switch_group=switch_group,
            switch_mac_policy=switch_mac_policy,
            firewall_address=firewall_address,
            ssid_policy=ssid_policy,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.nac_policy import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/nac_policy",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/user/nac-policy/" + quote_path_param(name_value)

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
        description: str | None = None,
        category: Literal["device", "firewall-user", "ems-tag", "fortivoice-tag", "vulnerability"] | None = None,
        status: Literal["enable", "disable"] | None = None,
        match_type: Literal["dynamic", "override"] | None = None,
        match_period: int | None = None,
        match_remove: Literal["default", "link-down"] | None = None,
        mac: str | None = None,
        hw_vendor: str | None = None,
        type: str | None = None,
        family: str | None = None,
        os: str | None = None,
        hw_version: str | None = None,
        sw_version: str | None = None,
        host: str | None = None,
        user: str | None = None,
        src: str | None = None,
        user_group: str | None = None,
        ems_tag: str | None = None,
        fortivoice_tag: str | None = None,
        severity: str | list[str] | list[dict[str, Any]] | None = None,
        switch_fortilink: str | None = None,
        switch_group: str | list[str] | list[dict[str, Any]] | None = None,
        switch_mac_policy: str | None = None,
        firewall_address: str | None = None,
        ssid_policy: str | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new user/nac_policy object.

        Configure NAC policy matching pattern to identify matching NAC devices.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: NAC policy name.
            description: Description for the NAC policy matching pattern.
            category: Category of NAC policy.
            status: Enable/disable NAC policy.
            match_type: Match and retain the devices based on the type.
            match_period: Number of days the matched devices will be retained (0 - always retain)
            match_remove: Options to remove the matched override devices.
            mac: NAC policy matching MAC address.
            hw_vendor: NAC policy matching hardware vendor.
            type: NAC policy matching type.
            family: NAC policy matching family.
            os: NAC policy matching operating system.
            hw_version: NAC policy matching hardware version.
            sw_version: NAC policy matching software version.
            host: NAC policy matching host.
            user: NAC policy matching user.
            src: NAC policy matching source.
            user_group: NAC policy matching user group.
            ems_tag: NAC policy matching EMS tag.
            fortivoice_tag: NAC policy matching FortiVoice tag.
            severity: NAC policy matching devices vulnerability severity lists.
                Default format: [{'severity-num': 1}]
                Supported formats:
                  - Single string: "value" → [{'severity-num': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'severity-num': 'val1'}, ...]
                  - List of dicts: [{'severity-num': 1}] (recommended)
            switch_fortilink: FortiLink interface for which this NAC policy belongs to.
            switch_group: List of managed FortiSwitch groups on which NAC policy can be applied.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            switch_mac_policy: Switch MAC policy action to be applied on the matched NAC policy.
            firewall_address: Dynamic firewall address to associate MAC which match this policy.
            ssid_policy: SSID policy to be applied on the matched NAC policy.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.user_nac_policy.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = NacPolicy.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.user_nac_policy.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(NacPolicy.required_fields()) }}
            
            Use NacPolicy.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if severity is not None:
            severity = normalize_table_field(
                severity,
                mkey="severity-num",
                required_fields=['severity-num'],
                field_name="severity",
                example="[{'severity-num': 1}]",
            )
        if switch_group is not None:
            switch_group = normalize_table_field(
                switch_group,
                mkey="name",
                required_fields=['name'],
                field_name="switch_group",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            description=description,
            category=category,
            status=status,
            match_type=match_type,
            match_period=match_period,
            match_remove=match_remove,
            mac=mac,
            hw_vendor=hw_vendor,
            type=type,
            family=family,
            os=os,
            hw_version=hw_version,
            sw_version=sw_version,
            host=host,
            user=user,
            src=src,
            user_group=user_group,
            ems_tag=ems_tag,
            fortivoice_tag=fortivoice_tag,
            severity=severity,
            switch_fortilink=switch_fortilink,
            switch_group=switch_group,
            switch_mac_policy=switch_mac_policy,
            firewall_address=firewall_address,
            ssid_policy=ssid_policy,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.nac_policy import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/nac_policy",
            )

        endpoint = "/user/nac-policy"
        
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
        Delete user/nac_policy object.

        Configure NAC policy matching pattern to identify matching NAC devices.

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
            >>> result = fgt.api.cmdb.user_nac_policy.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/user/nac-policy/" + quote_path_param(name)

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
        Check if user/nac_policy object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.user_nac_policy.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.user_nac_policy.exists(name=1):
            ...     fgt.api.cmdb.user_nac_policy.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/user/nac-policy"
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
        description: str | None = None,
        category: Literal["device", "firewall-user", "ems-tag", "fortivoice-tag", "vulnerability"] | None = None,
        status: Literal["enable", "disable"] | None = None,
        match_type: Literal["dynamic", "override"] | None = None,
        match_period: int | None = None,
        match_remove: Literal["default", "link-down"] | None = None,
        mac: str | None = None,
        hw_vendor: str | None = None,
        type: str | None = None,
        family: str | None = None,
        os: str | None = None,
        hw_version: str | None = None,
        sw_version: str | None = None,
        host: str | None = None,
        user: str | None = None,
        src: str | None = None,
        user_group: str | None = None,
        ems_tag: str | None = None,
        fortivoice_tag: str | None = None,
        severity: str | list[str] | list[dict[str, Any]] | None = None,
        switch_fortilink: str | None = None,
        switch_group: str | list[str] | list[dict[str, Any]] | None = None,
        switch_mac_policy: str | None = None,
        firewall_address: str | None = None,
        ssid_policy: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update user/nac_policy object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            description: Field description
            category: Field category
            status: Field status
            match_type: Field match-type
            match_period: Field match-period
            match_remove: Field match-remove
            mac: Field mac
            hw_vendor: Field hw-vendor
            type: Field type
            family: Field family
            os: Field os
            hw_version: Field hw-version
            sw_version: Field sw-version
            host: Field host
            user: Field user
            src: Field src
            user_group: Field user-group
            ems_tag: Field ems-tag
            fortivoice_tag: Field fortivoice-tag
            severity: Field severity
            switch_fortilink: Field switch-fortilink
            switch_group: Field switch-group
            switch_mac_policy: Field switch-mac-policy
            firewall_address: Field firewall-address
            ssid_policy: Field ssid-policy
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.user_nac_policy.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.user_nac_policy.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.user_nac_policy.set(payload_dict=obj_data)
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
        if severity is not None:
            severity = normalize_table_field(
                severity,
                mkey="severity-num",
                required_fields=['severity-num'],
                field_name="severity",
                example="[{'severity-num': 1}]",
            )
        if switch_group is not None:
            switch_group = normalize_table_field(
                switch_group,
                mkey="name",
                required_fields=['name'],
                field_name="switch_group",
                example="[{'name': 'value'}]",
            )
        
        # Build payload using helper function
        # Note: auto_normalize=False because this endpoint has unitary fields
        # (like 'interface') that would be incorrectly converted to list format
        payload_data = build_api_payload(
            api_type="cmdb",
            auto_normalize=False,
            name=name,
            description=description,
            category=category,
            status=status,
            match_type=match_type,
            match_period=match_period,
            match_remove=match_remove,
            mac=mac,
            hw_vendor=hw_vendor,
            type=type,
            family=family,
            os=os,
            hw_version=hw_version,
            sw_version=sw_version,
            host=host,
            user=user,
            src=src,
            user_group=user_group,
            ems_tag=ems_tag,
            fortivoice_tag=fortivoice_tag,
            severity=severity,
            switch_fortilink=switch_fortilink,
            switch_group=switch_group,
            switch_mac_policy=switch_mac_policy,
            firewall_address=firewall_address,
            ssid_policy=ssid_policy,
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
        Move user/nac_policy object to a new position.
        
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
            >>> fgt.api.cmdb.user_nac_policy.move(
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
        
        endpoint = "/user/nac-policy"
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
        Clone user/nac_policy object.
        
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
            >>> fgt.api.cmdb.user_nac_policy.clone(
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
        
        endpoint = "/user/nac-policy"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




