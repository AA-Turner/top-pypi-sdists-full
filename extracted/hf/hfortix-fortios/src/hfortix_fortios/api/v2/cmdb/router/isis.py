"""
FortiOS CMDB - Router isis

Configuration endpoint for managing cmdb router/isis objects.

API Endpoints:
    GET    /cmdb/router/isis
    POST   /cmdb/router/isis
    PUT    /cmdb/router/isis/{identifier}
    DELETE /cmdb/router/isis/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.router_isis.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.router_isis.post(
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

# Import child table helpers
from ._isis_child_tables import (
    IsisNetHelper,
    IsisInterfaceHelper,
    SummaryAddressHelper,
    SummaryAddress6Helper,
    RedistributeHelper,
    Redistribute6Helper,
)

# Import Protocol-based type hints (eliminates need for local @overload decorators)
from hfortix_fortios._protocols import CRUDEndpoint

class Isis(CRUDEndpoint, MetadataMixin):
    """Isis Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "isis"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "isis_net": {
            "mkey": "id",
            "required_fields": ['id'],
            "example": "[{'id': 1}]",
        },
        "isis_interface": {
            "mkey": "name",
            "required_fields": ['name'],
            "example": "[{'name': 'value'}]",
        },
        "summary_address": {
            "mkey": "id",
            "required_fields": ['prefix'],
            "example": "[{'prefix': 'value'}]",
        },
        "summary_address6": {
            "mkey": "id",
            "required_fields": ['prefix6'],
            "example": "[{'prefix6': 'value'}]",
        },
        "redistribute": {
            "mkey": "protocol",
            "required_fields": ['protocol'],
            "example": "[{'protocol': 'value'}]",
        },
        "redistribute6": {
            "mkey": "protocol",
            "required_fields": ['protocol'],
            "example": "[{'protocol': 'value'}]",
        },
    }
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = False
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
        """Initialize Isis endpoint."""
        self._client = client

        # Initialize child table helpers
        self.isis_net = IsisNetHelper(self)
        self.isis_interface = IsisInterfaceHelper(self)
        self.summary_address = SummaryAddressHelper(self)
        self.summary_address6 = SummaryAddress6Helper(self)
        self.redistribute = RedistributeHelper(self)
        self.redistribute6 = Redistribute6Helper(self)

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
        Retrieve router/isis configuration.

        Configure IS-IS.

        Args:
            name: Name identifier to retrieve specific object. If None, returns all objects.
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
            >>> # Get all router/isis objects
            >>> result = fgt.api.cmdb.router_isis.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.router_isis.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.router_isis.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.router_isis.get_schema()

        See Also:
            - post(): Create new router/isis object
            - put(): Update existing router/isis object
            - delete(): Remove router/isis object
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
            endpoint = f"/router/isis/{quote_path_param(name)}"
            unwrap_single = True
        else:
            endpoint = "/router/isis"
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
            >>> schema = fgt.api.cmdb.router_isis.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.router_isis.get_schema(format="json-schema")
        
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
        is_type: Literal["level-1-2", "level-1", "level-2-only"] | None = None,
        adv_passive_only: Literal["enable", "disable"] | None = None,
        adv_passive_only6: Literal["enable", "disable"] | None = None,
        auth_mode_l1: Literal["password", "md5"] | None = None,
        auth_mode_l2: Literal["password", "md5"] | None = None,
        auth_password_l1: Any | None = None,
        auth_password_l2: Any | None = None,
        auth_keychain_l1: str | None = None,
        auth_keychain_l2: str | None = None,
        auth_sendonly_l1: Literal["enable", "disable"] | None = None,
        auth_sendonly_l2: Literal["enable", "disable"] | None = None,
        ignore_lsp_errors: Literal["enable", "disable"] | None = None,
        lsp_gen_interval_l1: int | None = None,
        lsp_gen_interval_l2: int | None = None,
        lsp_refresh_interval: int | None = None,
        max_lsp_lifetime: int | None = None,
        spf_interval_exp_l1: str | None = None,
        spf_interval_exp_l2: str | None = None,
        dynamic_hostname: Literal["enable", "disable"] | None = None,
        adjacency_check: Literal["enable", "disable"] | None = None,
        adjacency_check6: Literal["enable", "disable"] | None = None,
        overload_bit: Literal["enable", "disable"] | None = None,
        overload_bit_suppress: Literal["external", "interlevel"] | list[str] | None = None,
        overload_bit_on_startup: int | None = None,
        default_originate: Literal["enable", "disable"] | None = None,
        default_originate6: Literal["enable", "disable"] | None = None,
        metric_style: Literal["narrow", "wide", "transition", "narrow-transition", "narrow-transition-l1", "narrow-transition-l2", "wide-l1", "wide-l2", "wide-transition", "wide-transition-l1", "wide-transition-l2", "transition-l1", "transition-l2"] | None = None,
        redistribute_l1: Literal["enable", "disable"] | None = None,
        redistribute_l1_list: str | None = None,
        redistribute_l2: Literal["enable", "disable"] | None = None,
        redistribute_l2_list: str | None = None,
        redistribute6_l1: Literal["enable", "disable"] | None = None,
        redistribute6_l1_list: str | None = None,
        redistribute6_l2: Literal["enable", "disable"] | None = None,
        redistribute6_l2_list: str | None = None,
        isis_net: str | list[str] | list[dict[str, Any]] | None = None,
        isis_interface: str | list[str] | list[dict[str, Any]] | None = None,
        summary_address: str | list[str] | list[dict[str, Any]] | None = None,
        summary_address6: str | list[str] | list[dict[str, Any]] | None = None,
        redistribute: str | list[str] | list[dict[str, Any]] | None = None,
        redistribute6: str | list[str] | list[dict[str, Any]] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing router/isis object.

        Configure IS-IS.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            is_type: IS type.
            adv_passive_only: Enable/disable IS-IS advertisement of passive interfaces only.
            adv_passive_only6: Enable/disable IPv6 IS-IS advertisement of passive interfaces only.
            auth_mode_l1: Level 1 authentication mode.
            auth_mode_l2: Level 2 authentication mode.
            auth_password_l1: Authentication password for level 1 PDUs.
            auth_password_l2: Authentication password for level 2 PDUs.
            auth_keychain_l1: Authentication key-chain for level 1 PDUs.
            auth_keychain_l2: Authentication key-chain for level 2 PDUs.
            auth_sendonly_l1: Enable/disable level 1 authentication send-only.
            auth_sendonly_l2: Enable/disable level 2 authentication send-only.
            ignore_lsp_errors: Enable/disable ignoring of LSP errors with bad checksums.
            lsp_gen_interval_l1: Minimum interval for level 1 LSP regenerating.
            lsp_gen_interval_l2: Minimum interval for level 2 LSP regenerating.
            lsp_refresh_interval: LSP refresh time in seconds.
            max_lsp_lifetime: Maximum LSP lifetime in seconds.
            spf_interval_exp_l1: Level 1 SPF calculation delay.
            spf_interval_exp_l2: Level 2 SPF calculation delay.
            dynamic_hostname: Enable/disable dynamic hostname.
            adjacency_check: Enable/disable adjacency check.
            adjacency_check6: Enable/disable IPv6 adjacency check.
            overload_bit: Enable/disable signal other routers not to use us in SPF.
            overload_bit_suppress: Suppress overload-bit for the specific prefixes.
            overload_bit_on_startup: Overload-bit only temporarily after reboot.
            default_originate: Enable/disable distribution of default route information.
            default_originate6: Enable/disable distribution of default IPv6 route information.
            metric_style: Use old-style (ISO 10589) or new-style packet formats.
            redistribute_l1: Enable/disable redistribution of level 1 routes into level 2.
            redistribute_l1_list: Access-list for route redistribution from l1 to l2.
            redistribute_l2: Enable/disable redistribution of level 2 routes into level 1.
            redistribute_l2_list: Access-list for route redistribution from l2 to l1.
            redistribute6_l1: Enable/disable redistribution of level 1 IPv6 routes into level 2.
            redistribute6_l1_list: Access-list for IPv6 route redistribution from l1 to l2.
            redistribute6_l2: Enable/disable redistribution of level 2 IPv6 routes into level 1.
            redistribute6_l2_list: Access-list for IPv6 route redistribution from l2 to l1.
            isis_net: IS-IS net configuration.
                Default format: [{'id': 1}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'id': 1}] (recommended)
            isis_interface: IS-IS interface configuration.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            summary_address: IS-IS summary addresses.
                Default format: [{'prefix': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'prefix': 'value'}] (recommended)
            summary_address6: IS-IS IPv6 summary address.
                Default format: [{'prefix6': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'id': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'id': 'val1'}, ...]
                  - List of dicts: [{'prefix6': 'value'}] (recommended)
            redistribute: IS-IS redistribute protocols.
                Default format: [{'protocol': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'protocol': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'protocol': 'val1'}, ...]
                  - List of dicts: [{'protocol': 'value'}] (recommended)
            redistribute6: IS-IS IPv6 redistribution for routing protocols.
                Default format: [{'protocol': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'protocol': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'protocol': 'val1'}, ...]
                  - List of dicts: [{'protocol': 'value'}] (recommended)
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.router_isis.put(
            ...     name="existing-object",
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": "existing-object",
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.router_isis.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if isis_net is not None:
            isis_net = normalize_table_field(
                isis_net,
                mkey="id",
                required_fields=['id'],
                field_name="isis_net",
                example="[{'id': 1}]",
            )
        if isis_interface is not None:
            isis_interface = normalize_table_field(
                isis_interface,
                mkey="name",
                required_fields=['name'],
                field_name="isis_interface",
                example="[{'name': 'value'}]",
            )
        if summary_address is not None:
            summary_address = normalize_table_field(
                summary_address,
                mkey="id",
                required_fields=['prefix'],
                field_name="summary_address",
                example="[{'prefix': 'value'}]",
            )
        if summary_address6 is not None:
            summary_address6 = normalize_table_field(
                summary_address6,
                mkey="id",
                required_fields=['prefix6'],
                field_name="summary_address6",
                example="[{'prefix6': 'value'}]",
            )
        if redistribute is not None:
            redistribute = normalize_table_field(
                redistribute,
                mkey="protocol",
                required_fields=['protocol'],
                field_name="redistribute",
                example="[{'protocol': 'value'}]",
            )
        if redistribute6 is not None:
            redistribute6 = normalize_table_field(
                redistribute6,
                mkey="protocol",
                required_fields=['protocol'],
                field_name="redistribute6",
                example="[{'protocol': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            is_type=is_type,
            adv_passive_only=adv_passive_only,
            adv_passive_only6=adv_passive_only6,
            auth_mode_l1=auth_mode_l1,
            auth_mode_l2=auth_mode_l2,
            auth_password_l1=auth_password_l1,
            auth_password_l2=auth_password_l2,
            auth_keychain_l1=auth_keychain_l1,
            auth_keychain_l2=auth_keychain_l2,
            auth_sendonly_l1=auth_sendonly_l1,
            auth_sendonly_l2=auth_sendonly_l2,
            ignore_lsp_errors=ignore_lsp_errors,
            lsp_gen_interval_l1=lsp_gen_interval_l1,
            lsp_gen_interval_l2=lsp_gen_interval_l2,
            lsp_refresh_interval=lsp_refresh_interval,
            max_lsp_lifetime=max_lsp_lifetime,
            spf_interval_exp_l1=spf_interval_exp_l1,
            spf_interval_exp_l2=spf_interval_exp_l2,
            dynamic_hostname=dynamic_hostname,
            adjacency_check=adjacency_check,
            adjacency_check6=adjacency_check6,
            overload_bit=overload_bit,
            overload_bit_suppress=overload_bit_suppress,
            overload_bit_on_startup=overload_bit_on_startup,
            default_originate=default_originate,
            default_originate6=default_originate6,
            metric_style=metric_style,
            redistribute_l1=redistribute_l1,
            redistribute_l1_list=redistribute_l1_list,
            redistribute_l2=redistribute_l2,
            redistribute_l2_list=redistribute_l2_list,
            redistribute6_l1=redistribute6_l1,
            redistribute6_l1_list=redistribute6_l1_list,
            redistribute6_l2=redistribute6_l2,
            redistribute6_l2_list=redistribute6_l2_list,
            isis_net=isis_net,
            isis_interface=isis_interface,
            summary_address=summary_address,
            summary_address6=summary_address6,
            redistribute=redistribute,
            redistribute6=redistribute6,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.isis import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/router/isis",
            )
        
        # Singleton endpoint - no identifier needed
        endpoint = "/router/isis"

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
        Move router/isis object to a new position.
        
        Reorders objects by moving one before/after another, to top/bottom, or to a specific position.
        
        Args:
            name: Name of object to move
            position: Where to move the object:
                - "before": Move before reference object (requires reference_name)
                - "after": Move after reference object (requires reference_name)
                - "top": Move to first position (reference not needed)
                - "bottom": Move to last position (reference not needed)
                - int (1-based): Move to specific position number (e.g., position=3 for 3rd place)
            reference_name: Name of reference object (required for before/after)
            vdom: Virtual domain name
            **kwargs: Additional parameters
            
        Returns:
            API response dictionary
            
        Examples:
            >>> # Move to top (first position)
            >>> fgt.api.cmdb.router_isis.move(
            ...     name="object1",
            ...     position="before",
            ...     reference_name="object2"
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
        endpoint = "/router/isis/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





