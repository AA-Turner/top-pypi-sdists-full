"""
FortiOS CMDB - System ike

Configuration endpoint for managing cmdb system/ike objects.

API Endpoints:
    GET    /cmdb/system/ike
    POST   /cmdb/system/ike
    PUT    /cmdb/system/ike/{identifier}
    DELETE /cmdb/system/ike/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.system_ike.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.system_ike.post(
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

class Ike(CRUDEndpoint, MetadataMixin):
    """Ike Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "ike"
    
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
        """Initialize Ike endpoint."""
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
        Retrieve system/ike configuration.

        Configure IKE global attributes.

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
            >>> # Get all system/ike objects
            >>> result = fgt.api.cmdb.system_ike.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.system_ike.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.system_ike.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.system_ike.get_schema()

        See Also:
            - post(): Create new system/ike object
            - put(): Update existing system/ike object
            - delete(): Remove system/ike object
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
            endpoint = f"/system/ike/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/system/ike"
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
            >>> schema = fgt.api.cmdb.system_ike.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.system_ike.get_schema(format="json-schema")
        
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
        embryonic_limit: int | None = None,
        dh_multiprocess: Literal["enable", "disable"] | None = None,
        dh_worker_count: int | None = None,
        dh_mode: Literal["software", "hardware"] | None = None,
        dh_keypair_cache: Literal["enable", "disable"] | None = None,
        dh_keypair_count: int | None = None,
        dh_keypair_throttle: Literal["enable", "disable"] | None = None,
        dh_group_1: str | None = None,
        dh_group_2: str | None = None,
        dh_group_5: str | None = None,
        dh_group_14: str | None = None,
        dh_group_15: str | None = None,
        dh_group_16: str | None = None,
        dh_group_17: str | None = None,
        dh_group_18: str | None = None,
        dh_group_19: str | None = None,
        dh_group_20: str | None = None,
        dh_group_21: str | None = None,
        dh_group_27: str | None = None,
        dh_group_28: str | None = None,
        dh_group_29: str | None = None,
        dh_group_30: str | None = None,
        dh_group_31: str | None = None,
        dh_group_32: str | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing system/ike object.

        Configure IKE global attributes.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            embryonic_limit: Maximum number of IPsec tunnels to negotiate simultaneously.
            dh_multiprocess: Enable/disable multiprocess Diffie-Hellman daemon for IKE.
            dh_worker_count: Number of Diffie-Hellman workers to start.
            dh_mode: Use software (CPU) or hardware (CPX) to perform Diffie-Hellman calculations.
            dh_keypair_cache: Enable/disable Diffie-Hellman key pair cache.
            dh_keypair_count: Number of key pairs to pre-generate for each Diffie-Hellman group (per-worker).
            dh_keypair_throttle: Enable/disable Diffie-Hellman key pair cache CPU throttling.
            dh_group_1: Diffie-Hellman group 1 (MODP-768).
            dh_group_2: Diffie-Hellman group 2 (MODP-1024).
            dh_group_5: Diffie-Hellman group 5 (MODP-1536).
            dh_group_14: Diffie-Hellman group 14 (MODP-2048).
            dh_group_15: Diffie-Hellman group 15 (MODP-3072).
            dh_group_16: Diffie-Hellman group 16 (MODP-4096).
            dh_group_17: Diffie-Hellman group 17 (MODP-6144).
            dh_group_18: Diffie-Hellman group 18 (MODP-8192).
            dh_group_19: Diffie-Hellman group 19 (EC-P256).
            dh_group_20: Diffie-Hellman group 20 (EC-P384).
            dh_group_21: Diffie-Hellman group 21 (EC-P521).
            dh_group_27: Diffie-Hellman group 27 (EC-P224BP).
            dh_group_28: Diffie-Hellman group 28 (EC-P256BP).
            dh_group_29: Diffie-Hellman group 29 (EC-P384BP).
            dh_group_30: Diffie-Hellman group 30 (EC-P512BP).
            dh_group_31: Diffie-Hellman group 31 (EC-X25519).
            dh_group_32: Diffie-Hellman group 32 (EC-X448).
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.system_ike.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.system_ike.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            embryonic_limit=embryonic_limit,
            dh_multiprocess=dh_multiprocess,
            dh_worker_count=dh_worker_count,
            dh_mode=dh_mode,
            dh_keypair_cache=dh_keypair_cache,
            dh_keypair_count=dh_keypair_count,
            dh_keypair_throttle=dh_keypair_throttle,
            dh_group_1=dh_group_1,
            dh_group_2=dh_group_2,
            dh_group_5=dh_group_5,
            dh_group_14=dh_group_14,
            dh_group_15=dh_group_15,
            dh_group_16=dh_group_16,
            dh_group_17=dh_group_17,
            dh_group_18=dh_group_18,
            dh_group_19=dh_group_19,
            dh_group_20=dh_group_20,
            dh_group_21=dh_group_21,
            dh_group_27=dh_group_27,
            dh_group_28=dh_group_28,
            dh_group_29=dh_group_29,
            dh_group_30=dh_group_30,
            dh_group_31=dh_group_31,
            dh_group_32=dh_group_32,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.ike import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/system/ike",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/system/ike"

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
        Move system/ike object to a new position.
        
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
            >>> fgt.api.cmdb.system_ike.move(
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
        
        endpoint = "/system/ike"
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
        Clone system/ike object.
        
        Creates a copy of an existing object with a new identifier.
        
        Args:
            name: Name of object to clone
            new_name: Name for the cloned object
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Example:
            >>> # Clone an existing object
            >>> fgt.api.cmdb.system_ike.clone(
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
        
        endpoint = "/system/ike"
        return self._client.post(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=False        )




