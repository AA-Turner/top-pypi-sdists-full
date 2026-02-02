"""
FortiOS CMDB - User fortitoken

Configuration endpoint for managing cmdb user/fortitoken objects.

API Endpoints:
    GET    /cmdb/user/fortitoken
    POST   /cmdb/user/fortitoken
    PUT    /cmdb/user/fortitoken/{identifier}
    DELETE /cmdb/user/fortitoken/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.user_fortitoken.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.user_fortitoken.post(
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

class Fortitoken(CRUDEndpoint, MetadataMixin):
    """Fortitoken Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "fortitoken"
    
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
        """Initialize Fortitoken endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        serial_number: str | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve user/fortitoken configuration.

        Configure FortiToken.

        Args:
            serial_number: String identifier to retrieve specific object.
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
            >>> # Get all user/fortitoken objects
            >>> result = fgt.api.cmdb.user_fortitoken.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific user/fortitoken by serial-number
            >>> result = fgt.api.cmdb.user_fortitoken.get(serial_number=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.user_fortitoken.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.user_fortitoken.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.user_fortitoken.get_schema()

        See Also:
            - post(): Create new user/fortitoken object
            - put(): Update existing user/fortitoken object
            - delete(): Remove user/fortitoken object
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
        
        if serial_number:
            endpoint = "/user/fortitoken/" + quote_path_param(serial_number)
            unwrap_single = True
        else:
            endpoint = "/user/fortitoken"
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
            >>> schema = fgt.api.cmdb.user_fortitoken.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.user_fortitoken.get_schema(format="json-schema")
        
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
        serial_number: str | None = None,
        status: Literal["active", "lock"] | None = None,
        comments: str | None = None,
        license: str | None = None,
        activation_code: str | None = None,
        activation_expire: int | None = None,
        reg_id: str | None = None,
        os_ver: str | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing user/fortitoken object.

        Configure FortiToken.

        Args:
            payload_dict: Object data as dict. Must include serial-number (primary key).
            serial_number: Serial number.
            status: Status.
            comments: Comment.
            license: Mobile token license.
            activation_code: Mobile token user activation-code.
            activation_expire: Mobile token user activation-code expire time.
            reg_id: Device Reg ID.
            os_ver: Device Mobile Version.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If serial-number is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.user_fortitoken.put(
            ...     serial_number=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "serial-number": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.user_fortitoken.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            serial_number=serial_number,
            status=status,
            comments=comments,
            license=license,
            activation_code=activation_code,
            activation_expire=activation_expire,
            reg_id=reg_id,
            os_ver=os_ver,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.fortitoken import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/fortitoken",
            )
        
        serial_number_value = payload_data.get("serial-number")
        if not serial_number_value:
            raise ValueError("serial-number is required for PUT")
        endpoint = "/user/fortitoken/" + quote_path_param(serial_number_value)

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
        serial_number: str | None = None,
        status: Literal["active", "lock"] | None = None,
        comments: str | None = None,
        license: str | None = None,
        activation_code: str | None = None,
        activation_expire: int | None = None,
        reg_id: str | None = None,
        os_ver: str | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new user/fortitoken object.

        Configure FortiToken.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            serial_number: Serial number.
            status: Status.
            comments: Comment.
            license: Mobile token license.
            activation_code: Mobile token user activation-code.
            activation_expire: Mobile token user activation-code expire time.
            reg_id: Device Reg ID.
            os_ver: Device Mobile Version.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.user_fortitoken.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created serial-number: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Fortitoken.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.user_fortitoken.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Fortitoken.required_fields()) }}
            
            Use Fortitoken.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            serial_number=serial_number,
            status=status,
            comments=comments,
            license=license,
            activation_code=activation_code,
            activation_expire=activation_expire,
            reg_id=reg_id,
            os_ver=os_ver,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.fortitoken import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/user/fortitoken",
            )

        endpoint = "/user/fortitoken"
        
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
        serial_number: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Delete user/fortitoken object.

        Configure FortiToken.

        Args:
            serial_number: Primary key identifier
            vdom: Virtual domain name
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If serial-number is not provided

        Examples:
            >>> # Delete specific object
            >>> result = fgt.api.cmdb.user_fortitoken.delete(serial_number=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not serial_number:
            raise ValueError("serial-number is required for DELETE")
        endpoint = "/user/fortitoken/" + quote_path_param(serial_number)

        # Add explicit query parameters for DELETE
        params: dict[str, Any] = {}
        if q_scope is not None:
            params["scope"] = q_scope
        
        return self._client.delete(  # type: ignore[return-value]
            "cmdb", endpoint, params=params, vdom=vdom        )

    def exists(
        self,
        serial_number: str,
        vdom: str | bool | None = None,
    ) -> Union[bool, Coroutine[Any, Any, bool]]:
        """
        Check if user/fortitoken object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            serial_number: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.user_fortitoken.exists(serial_number=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.user_fortitoken.exists(serial_number=1):
            ...     fgt.api.cmdb.user_fortitoken.delete(serial_number=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/user/fortitoken"
        endpoint = f"{endpoint}/{quote_path_param(serial_number)}"
        
        try:
            result = self.get(serial_number=serial_number, vdom=vdom)
            
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
        serial_number: str | None = None,
        status: Literal["active", "lock"] | None = None,
        comments: str | None = None,
        license: str | None = None,
        activation_code: str | None = None,
        activation_expire: int | None = None,
        reg_id: str | None = None,
        os_ver: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update user/fortitoken object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (serial-number) in the payload.

        Args:
            payload_dict: Resource data including serial-number (primary key)
            serial_number: Field serial-number
            status: Field status
            comments: Field comments
            license: Field license
            activation_code: Field activation-code
            activation_expire: Field activation-expire
            reg_id: Field reg-id
            os_ver: Field os-ver
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If serial-number is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.user_fortitoken.set(
            ...     serial_number=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "serial-number": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.user_fortitoken.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.user_fortitoken.set(payload_dict=obj_data)
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
            serial_number=serial_number,
            status=status,
            comments=comments,
            license=license,
            activation_code=activation_code,
            activation_expire=activation_expire,
            reg_id=reg_id,
            os_ver=os_ver,
            data=payload_dict,
        )
        
        mkey_value = payload_data.get("serial-number")
        if not mkey_value:
            raise ValueError("serial-number is required for set()")
        
        # Check if resource exists
        if self.exists(serial_number=mkey_value, vdom=vdom):
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
        serial_number: str,
        action: Literal["before", "after"],
        reference_serial_number: str,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Move user/fortitoken object to a new position.
        
        Reorders objects by moving one before or after another.
        
        Args:
            serial_number: Identifier of object to move
            action: Move "before" or "after" reference object
            reference_serial_number: Identifier of reference object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Move policy 100 before policy 50
            >>> fgt.api.cmdb.user_fortitoken.move(
            ...     serial_number=100,
            ...     action="before",
            ...     reference_serial_number=50
            ... )
        """
        # Build params for move operation
        params = {
            "serial-number": serial_number,
            "action": "move",
            action: reference_serial_number,
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/user/fortitoken"
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )

    # ========================================================================
    # Action: Clone
    # ========================================================================
    
    def clone(
        self,
        serial_number: str,
        new_serial_number: str,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Clone user/fortitoken object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            serial_number: Identifier of object to clone
            new_serial_number: Identifier for the cloned object
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.user_fortitoken.clone(
            ...     serial_number=1,
            ...     new_serial_number=100
            ... )
        """
        # Build params for clone operation  
        params = {
            "serial-number": serial_number,
            "new_serial-number": new_serial_number,
            "action": "clone",
            "vdom": vdom,
            **kwargs,
        }
        
        endpoint = "/user/fortitoken"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )




