"""
FortiOS CMDB - Webfilter profile

Configuration endpoint for managing cmdb webfilter/profile objects.

API Endpoints:
    GET    /cmdb/webfilter/profile
    POST   /cmdb/webfilter/profile
    PUT    /cmdb/webfilter/profile/{identifier}
    DELETE /cmdb/webfilter/profile/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.cmdb.webfilter_profile.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.cmdb.webfilter_profile.post(
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

class Profile(CRUDEndpoint, MetadataMixin):
    """Profile Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "profile"
    
    # ========================================================================
    # Table Fields Metadata (for normalization)
    # Auto-generated from schema - supports flexible input formats
    # ========================================================================
    _TABLE_FIELDS = {
        "wisp_servers": {
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
    # SUPPORTS_CLONE = True  # Disabled - unreliable across endpoints
    SUPPORTS_FILTERING = True
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Profile endpoint."""
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
        Retrieve webfilter/profile configuration.

        Configure Web filter profiles.

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
            >>> # Get all webfilter/profile objects
            >>> result = fgt.api.cmdb.webfilter_profile.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get specific webfilter/profile by name
            >>> result = fgt.api.cmdb.webfilter_profile.get(name=1)
            >>> print(result['results'])
            
            >>> # Get with filter
            >>> result = fgt.api.cmdb.webfilter_profile.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.cmdb.webfilter_profile.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.cmdb.webfilter_profile.get_schema()

        See Also:
            - post(): Create new webfilter/profile object
            - put(): Update existing webfilter/profile object
            - delete(): Remove webfilter/profile object
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
            endpoint = "/webfilter/profile/" + quote_path_param(name)
            unwrap_single = True
        else:
            endpoint = "/webfilter/profile"
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
            >>> schema = fgt.api.cmdb.webfilter_profile.get_schema()
            >>> print(schema['results'])
            
            >>> # Get JSON Schema format (if supported)
            >>> json_schema = fgt.api.cmdb.webfilter_profile.get_schema(format="json-schema")
        
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
        comment: str | None = None,
        feature_set: Literal["flow", "proxy"] | None = None,
        replacemsg_group: str | None = None,
        options: Literal["activexfilter", "cookiefilter", "javafilter", "block-invalid-url", "jscript", "js", "vbs", "unknown", "intrinsic", "wf-referer", "wf-cookie", "per-user-bal"] | list[str] | None = None,
        https_replacemsg: Literal["enable", "disable"] | None = None,
        web_flow_log_encoding: Literal["utf-8", "punycode"] | None = None,
        ovrd_perm: Literal["bannedword-override", "urlfilter-override", "fortiguard-wf-override", "contenttype-check-override"] | list[str] | None = None,
        post_action: Literal["normal", "block"] | None = None,
        override: str | None = None,
        web: str | None = None,
        ftgd_wf: str | None = None,
        antiphish: str | None = None,
        wisp: Literal["enable", "disable"] | None = None,
        wisp_servers: str | list[str] | list[dict[str, Any]] | None = None,
        wisp_algorithm: Literal["primary-secondary", "round-robin", "auto-learning"] | None = None,
        log_all_url: Literal["enable", "disable"] | None = None,
        web_content_log: Literal["enable", "disable"] | None = None,
        web_filter_activex_log: Literal["enable", "disable"] | None = None,
        web_filter_command_block_log: Literal["enable", "disable"] | None = None,
        web_filter_cookie_log: Literal["enable", "disable"] | None = None,
        web_filter_applet_log: Literal["enable", "disable"] | None = None,
        web_filter_jscript_log: Literal["enable", "disable"] | None = None,
        web_filter_js_log: Literal["enable", "disable"] | None = None,
        web_filter_vbs_log: Literal["enable", "disable"] | None = None,
        web_filter_unknown_log: Literal["enable", "disable"] | None = None,
        web_filter_referer_log: Literal["enable", "disable"] | None = None,
        web_filter_cookie_removal_log: Literal["enable", "disable"] | None = None,
        web_url_log: Literal["enable", "disable"] | None = None,
        web_invalid_domain_log: Literal["enable", "disable"] | None = None,
        web_ftgd_err_log: Literal["enable", "disable"] | None = None,
        web_ftgd_quota_usage: Literal["enable", "disable"] | None = None,
        extended_log: Literal["enable", "disable"] | None = None,
        web_extended_all_action_log: Literal["enable", "disable"] | None = None,
        web_antiphishing_log: Literal["enable", "disable"] | None = None,
        q_action: Literal["move"] | None = None,
        q_before: str | None = None,
        q_after: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Update existing webfilter/profile object.

        Configure Web filter profiles.

        Args:
            payload_dict: Object data as dict. Must include name (primary key).
            name: Profile name.
            comment: Optional comments.
            feature_set: Flow/proxy feature set.
            replacemsg_group: Replacement message group.
            options: Options.
            https_replacemsg: Enable replacement messages for HTTPS.
            web_flow_log_encoding: Log encoding in flow mode.
            ovrd_perm: Permitted override types.
            post_action: Action taken for HTTP POST traffic.
            override: Web Filter override settings.
            web: Web content filtering settings.
            ftgd_wf: FortiGuard Web Filter settings.
            antiphish: AntiPhishing profile.
            wisp: Enable/disable web proxy WISP.
            wisp_servers: WISP servers.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            wisp_algorithm: WISP server selection algorithm.
            log_all_url: Enable/disable logging all URLs visited.
            web_content_log: Enable/disable logging logging blocked web content.
            web_filter_activex_log: Enable/disable logging ActiveX.
            web_filter_command_block_log: Enable/disable logging blocked commands.
            web_filter_cookie_log: Enable/disable logging cookie filtering.
            web_filter_applet_log: Enable/disable logging Java applets.
            web_filter_jscript_log: Enable/disable logging JScripts.
            web_filter_js_log: Enable/disable logging Java scripts.
            web_filter_vbs_log: Enable/disable logging VBS scripts.
            web_filter_unknown_log: Enable/disable logging unknown scripts.
            web_filter_referer_log: Enable/disable logging referrers.
            web_filter_cookie_removal_log: Enable/disable logging blocked cookies.
            web_url_log: Enable/disable logging URL filtering.
            web_invalid_domain_log: Enable/disable logging invalid domain names.
            web_ftgd_err_log: Enable/disable logging rating errors.
            web_ftgd_quota_usage: Enable/disable logging daily quota usage.
            extended_log: Enable/disable extended logging for web filtering.
            web_extended_all_action_log: Enable/disable extended any filter action logging for web filtering.
            web_antiphishing_log: Enable/disable logging of AntiPhishing checks.
            vdom: Virtual domain name.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Update specific fields
            >>> result = fgt.api.cmdb.webfilter_profile.put(
            ...     name=1,
            ...     # ... fields to update
            ... )
            
            >>> # Update using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "new-value",
            ... }
            >>> result = fgt.api.cmdb.webfilter_profile.put(payload_dict=payload)

        See Also:
            - post(): Create new object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if wisp_servers is not None:
            wisp_servers = normalize_table_field(
                wisp_servers,
                mkey="name",
                required_fields=['name'],
                field_name="wisp_servers",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            comment=comment,
            feature_set=feature_set,
            replacemsg_group=replacemsg_group,
            options=options,
            https_replacemsg=https_replacemsg,
            web_flow_log_encoding=web_flow_log_encoding,
            ovrd_perm=ovrd_perm,
            post_action=post_action,
            override=override,
            web=web,
            ftgd_wf=ftgd_wf,
            antiphish=antiphish,
            wisp=wisp,
            wisp_servers=wisp_servers,
            wisp_algorithm=wisp_algorithm,
            log_all_url=log_all_url,
            web_content_log=web_content_log,
            web_filter_activex_log=web_filter_activex_log,
            web_filter_command_block_log=web_filter_command_block_log,
            web_filter_cookie_log=web_filter_cookie_log,
            web_filter_applet_log=web_filter_applet_log,
            web_filter_jscript_log=web_filter_jscript_log,
            web_filter_js_log=web_filter_js_log,
            web_filter_vbs_log=web_filter_vbs_log,
            web_filter_unknown_log=web_filter_unknown_log,
            web_filter_referer_log=web_filter_referer_log,
            web_filter_cookie_removal_log=web_filter_cookie_removal_log,
            web_url_log=web_url_log,
            web_invalid_domain_log=web_invalid_domain_log,
            web_ftgd_err_log=web_ftgd_err_log,
            web_ftgd_quota_usage=web_ftgd_quota_usage,
            extended_log=extended_log,
            web_extended_all_action_log=web_extended_all_action_log,
            web_antiphishing_log=web_antiphishing_log,
            data=payload_dict,
        )
        
        # Check for deprecated fields and warn users
        from ._helpers.profile import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/webfilter/profile",
            )
        
        name_value = payload_data.get("name")
        if not name_value:
            raise ValueError("name is required for PUT")
        endpoint = "/webfilter/profile/" + quote_path_param(name_value)

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
        comment: str | None = None,
        feature_set: Literal["flow", "proxy"] | None = None,
        replacemsg_group: str | None = None,
        options: Literal["activexfilter", "cookiefilter", "javafilter", "block-invalid-url", "jscript", "js", "vbs", "unknown", "intrinsic", "wf-referer", "wf-cookie", "per-user-bal"] | list[str] | None = None,
        https_replacemsg: Literal["enable", "disable"] | None = None,
        web_flow_log_encoding: Literal["utf-8", "punycode"] | None = None,
        ovrd_perm: Literal["bannedword-override", "urlfilter-override", "fortiguard-wf-override", "contenttype-check-override"] | list[str] | None = None,
        post_action: Literal["normal", "block"] | None = None,
        override: str | None = None,
        web: str | None = None,
        ftgd_wf: str | None = None,
        antiphish: str | None = None,
        wisp: Literal["enable", "disable"] | None = None,
        wisp_servers: str | list[str] | list[dict[str, Any]] | None = None,
        wisp_algorithm: Literal["primary-secondary", "round-robin", "auto-learning"] | None = None,
        log_all_url: Literal["enable", "disable"] | None = None,
        web_content_log: Literal["enable", "disable"] | None = None,
        web_filter_activex_log: Literal["enable", "disable"] | None = None,
        web_filter_command_block_log: Literal["enable", "disable"] | None = None,
        web_filter_cookie_log: Literal["enable", "disable"] | None = None,
        web_filter_applet_log: Literal["enable", "disable"] | None = None,
        web_filter_jscript_log: Literal["enable", "disable"] | None = None,
        web_filter_js_log: Literal["enable", "disable"] | None = None,
        web_filter_vbs_log: Literal["enable", "disable"] | None = None,
        web_filter_unknown_log: Literal["enable", "disable"] | None = None,
        web_filter_referer_log: Literal["enable", "disable"] | None = None,
        web_filter_cookie_removal_log: Literal["enable", "disable"] | None = None,
        web_url_log: Literal["enable", "disable"] | None = None,
        web_invalid_domain_log: Literal["enable", "disable"] | None = None,
        web_ftgd_err_log: Literal["enable", "disable"] | None = None,
        web_ftgd_quota_usage: Literal["enable", "disable"] | None = None,
        extended_log: Literal["enable", "disable"] | None = None,
        web_extended_all_action_log: Literal["enable", "disable"] | None = None,
        web_antiphishing_log: Literal["enable", "disable"] | None = None,
        q_action: Literal["clone"] | None = None,
        q_nkey: str | None = None,
        q_scope: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new webfilter/profile object.

        Configure Web filter profiles.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            name: Profile name.
            comment: Optional comments.
            feature_set: Flow/proxy feature set.
            replacemsg_group: Replacement message group.
            options: Options.
            https_replacemsg: Enable replacement messages for HTTPS.
            web_flow_log_encoding: Log encoding in flow mode.
            ovrd_perm: Permitted override types.
            post_action: Action taken for HTTP POST traffic.
            override: Web Filter override settings.
            web: Web content filtering settings.
            ftgd_wf: FortiGuard Web Filter settings.
            antiphish: AntiPhishing profile.
            wisp: Enable/disable web proxy WISP.
            wisp_servers: WISP servers.
                Default format: [{'name': 'value'}]
                Supported formats:
                  - Single string: "value" → [{'name': 'value'}]
                  - List of strings: ["val1", "val2"] → [{'name': 'val1'}, ...]
                  - List of dicts: [{'name': 'value'}] (recommended)
            wisp_algorithm: WISP server selection algorithm.
            log_all_url: Enable/disable logging all URLs visited.
            web_content_log: Enable/disable logging logging blocked web content.
            web_filter_activex_log: Enable/disable logging ActiveX.
            web_filter_command_block_log: Enable/disable logging blocked commands.
            web_filter_cookie_log: Enable/disable logging cookie filtering.
            web_filter_applet_log: Enable/disable logging Java applets.
            web_filter_jscript_log: Enable/disable logging JScripts.
            web_filter_js_log: Enable/disable logging Java scripts.
            web_filter_vbs_log: Enable/disable logging VBS scripts.
            web_filter_unknown_log: Enable/disable logging unknown scripts.
            web_filter_referer_log: Enable/disable logging referrers.
            web_filter_cookie_removal_log: Enable/disable logging blocked cookies.
            web_url_log: Enable/disable logging URL filtering.
            web_invalid_domain_log: Enable/disable logging invalid domain names.
            web_ftgd_err_log: Enable/disable logging rating errors.
            web_ftgd_quota_usage: Enable/disable logging daily quota usage.
            extended_log: Enable/disable extended logging for web filtering.
            web_extended_all_action_log: Enable/disable extended any filter action logging for web filtering.
            web_antiphishing_log: Enable/disable logging of AntiPhishing checks.
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.cmdb.webfilter_profile.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created name: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Profile.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.cmdb.webfilter_profile.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Profile.required_fields()) }}
            
            Use Profile.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Apply normalization for table fields (supports flexible input formats)
        if wisp_servers is not None:
            wisp_servers = normalize_table_field(
                wisp_servers,
                mkey="name",
                required_fields=['name'],
                field_name="wisp_servers",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            comment=comment,
            feature_set=feature_set,
            replacemsg_group=replacemsg_group,
            options=options,
            https_replacemsg=https_replacemsg,
            web_flow_log_encoding=web_flow_log_encoding,
            ovrd_perm=ovrd_perm,
            post_action=post_action,
            override=override,
            web=web,
            ftgd_wf=ftgd_wf,
            antiphish=antiphish,
            wisp=wisp,
            wisp_servers=wisp_servers,
            wisp_algorithm=wisp_algorithm,
            log_all_url=log_all_url,
            web_content_log=web_content_log,
            web_filter_activex_log=web_filter_activex_log,
            web_filter_command_block_log=web_filter_command_block_log,
            web_filter_cookie_log=web_filter_cookie_log,
            web_filter_applet_log=web_filter_applet_log,
            web_filter_jscript_log=web_filter_jscript_log,
            web_filter_js_log=web_filter_js_log,
            web_filter_vbs_log=web_filter_vbs_log,
            web_filter_unknown_log=web_filter_unknown_log,
            web_filter_referer_log=web_filter_referer_log,
            web_filter_cookie_removal_log=web_filter_cookie_removal_log,
            web_url_log=web_url_log,
            web_invalid_domain_log=web_invalid_domain_log,
            web_ftgd_err_log=web_ftgd_err_log,
            web_ftgd_quota_usage=web_ftgd_quota_usage,
            extended_log=extended_log,
            web_extended_all_action_log=web_extended_all_action_log,
            web_antiphishing_log=web_antiphishing_log,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.profile import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="cmdb/webfilter/profile",
            )

        endpoint = "/webfilter/profile"
        
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
        Delete webfilter/profile object.

        Configure Web filter profiles.

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
            >>> result = fgt.api.cmdb.webfilter_profile.delete(name=1)
            
            >>> # Check for errors
            >>> if result.get('status') != 'success':
            ...     print(f"Delete failed: {result.get('error')}")

        See Also:
            - exists(): Check if object exists before deleting
            - get(): Retrieve object to verify it exists
        """
        if not name:
            raise ValueError("name is required for DELETE")
        endpoint = "/webfilter/profile/" + quote_path_param(name)

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
        Check if webfilter/profile object exists.

        Verifies whether an object exists by attempting to retrieve it and checking the response status.

        Args:
            name: Primary key identifier
            vdom: Virtual domain name

        Returns:
            True if object exists, False otherwise

        Examples:
            >>> # Check if object exists before operations
            >>> if fgt.api.cmdb.webfilter_profile.exists(name=1):
            ...     print("Object exists")
            ... else:
            ...     print("Object not found")
            
            >>> # Conditional delete
            >>> if fgt.api.cmdb.webfilter_profile.exists(name=1):
            ...     fgt.api.cmdb.webfilter_profile.delete(name=1)

        See Also:
            - get(): Retrieve full object data
            - set(): Create or update automatically based on existence
        """
        # Use direct GET request to check existence
        # 404 responses are expected and just mean "doesn't exist"
        endpoint = "/webfilter/profile"
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
        comment: str | None = None,
        feature_set: Literal["flow", "proxy"] | None = None,
        replacemsg_group: str | None = None,
        options: Literal["activexfilter", "cookiefilter", "javafilter", "block-invalid-url", "jscript", "js", "vbs", "unknown", "intrinsic", "wf-referer", "wf-cookie", "per-user-bal"] | list[str] | list[dict[str, Any]] | None = None,
        https_replacemsg: Literal["enable", "disable"] | None = None,
        web_flow_log_encoding: Literal["utf-8", "punycode"] | None = None,
        ovrd_perm: Literal["bannedword-override", "urlfilter-override", "fortiguard-wf-override", "contenttype-check-override"] | list[str] | list[dict[str, Any]] | None = None,
        post_action: Literal["normal", "block"] | None = None,
        override: str | None = None,
        web: str | None = None,
        ftgd_wf: str | None = None,
        antiphish: str | None = None,
        wisp: Literal["enable", "disable"] | None = None,
        wisp_servers: str | list[str] | list[dict[str, Any]] | None = None,
        wisp_algorithm: Literal["primary-secondary", "round-robin", "auto-learning"] | None = None,
        log_all_url: Literal["enable", "disable"] | None = None,
        web_content_log: Literal["enable", "disable"] | None = None,
        web_filter_activex_log: Literal["enable", "disable"] | None = None,
        web_filter_command_block_log: Literal["enable", "disable"] | None = None,
        web_filter_cookie_log: Literal["enable", "disable"] | None = None,
        web_filter_applet_log: Literal["enable", "disable"] | None = None,
        web_filter_jscript_log: Literal["enable", "disable"] | None = None,
        web_filter_js_log: Literal["enable", "disable"] | None = None,
        web_filter_vbs_log: Literal["enable", "disable"] | None = None,
        web_filter_unknown_log: Literal["enable", "disable"] | None = None,
        web_filter_referer_log: Literal["enable", "disable"] | None = None,
        web_filter_cookie_removal_log: Literal["enable", "disable"] | None = None,
        web_url_log: Literal["enable", "disable"] | None = None,
        web_invalid_domain_log: Literal["enable", "disable"] | None = None,
        web_ftgd_err_log: Literal["enable", "disable"] | None = None,
        web_ftgd_quota_usage: Literal["enable", "disable"] | None = None,
        extended_log: Literal["enable", "disable"] | None = None,
        web_extended_all_action_log: Literal["enable", "disable"] | None = None,
        web_antiphishing_log: Literal["enable", "disable"] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create or update webfilter/profile object (intelligent operation).

        Automatically determines whether to create (POST) or update (PUT) based on
        whether the resource exists. Requires the primary key (name) in the payload.

        Args:
            payload_dict: Resource data including name (primary key)
            name: Field name
            comment: Field comment
            feature_set: Field feature-set
            replacemsg_group: Field replacemsg-group
            options: Field options
            https_replacemsg: Field https-replacemsg
            web_flow_log_encoding: Field web-flow-log-encoding
            ovrd_perm: Field ovrd-perm
            post_action: Field post-action
            override: Field override
            web: Field web
            ftgd_wf: Field ftgd-wf
            antiphish: Field antiphish
            wisp: Field wisp
            wisp_servers: Field wisp-servers
            wisp_algorithm: Field wisp-algorithm
            log_all_url: Field log-all-url
            web_content_log: Field web-content-log
            web_filter_activex_log: Field web-filter-activex-log
            web_filter_command_block_log: Field web-filter-command-block-log
            web_filter_cookie_log: Field web-filter-cookie-log
            web_filter_applet_log: Field web-filter-applet-log
            web_filter_jscript_log: Field web-filter-jscript-log
            web_filter_js_log: Field web-filter-js-log
            web_filter_vbs_log: Field web-filter-vbs-log
            web_filter_unknown_log: Field web-filter-unknown-log
            web_filter_referer_log: Field web-filter-referer-log
            web_filter_cookie_removal_log: Field web-filter-cookie-removal-log
            web_url_log: Field web-url-log
            web_invalid_domain_log: Field web-invalid-domain-log
            web_ftgd_err_log: Field web-ftgd-err-log
            web_ftgd_quota_usage: Field web-ftgd-quota-usage
            extended_log: Field extended-log
            web_extended_all_action_log: Field web-extended-all-action-log
            web_antiphishing_log: Field web-antiphishing-log
            vdom: Virtual domain name
            **kwargs: Additional parameters passed to PUT or POST

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Raises:
            ValueError: If name is missing from payload

        Examples:
            >>> # Intelligent create or update using field parameters
            >>> result = fgt.api.cmdb.webfilter_profile.set(
            ...     name=1,
            ...     # ... other fields
            ... )
            
            >>> # Or using payload dict
            >>> payload = {
            ...     "name": 1,
            ...     "field1": "value1",
            ...     "field2": "value2",
            ... }
            >>> result = fgt.api.cmdb.webfilter_profile.set(payload_dict=payload)
            >>> # Will POST if object doesn't exist, PUT if it does
            
            >>> # Idempotent configuration
            >>> for obj_data in configuration_list:
            ...     fgt.api.cmdb.webfilter_profile.set(payload_dict=obj_data)
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
        if wisp_servers is not None:
            wisp_servers = normalize_table_field(
                wisp_servers,
                mkey="name",
                required_fields=['name'],
                field_name="wisp_servers",
                example="[{'name': 'value'}]",
            )
        
        # Apply normalization for multi-value option fields (space-separated strings)
        
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="cmdb",
            name=name,
            comment=comment,
            feature_set=feature_set,
            replacemsg_group=replacemsg_group,
            options=options,
            https_replacemsg=https_replacemsg,
            web_flow_log_encoding=web_flow_log_encoding,
            ovrd_perm=ovrd_perm,
            post_action=post_action,
            override=override,
            web=web,
            ftgd_wf=ftgd_wf,
            antiphish=antiphish,
            wisp=wisp,
            wisp_servers=wisp_servers,
            wisp_algorithm=wisp_algorithm,
            log_all_url=log_all_url,
            web_content_log=web_content_log,
            web_filter_activex_log=web_filter_activex_log,
            web_filter_command_block_log=web_filter_command_block_log,
            web_filter_cookie_log=web_filter_cookie_log,
            web_filter_applet_log=web_filter_applet_log,
            web_filter_jscript_log=web_filter_jscript_log,
            web_filter_js_log=web_filter_js_log,
            web_filter_vbs_log=web_filter_vbs_log,
            web_filter_unknown_log=web_filter_unknown_log,
            web_filter_referer_log=web_filter_referer_log,
            web_filter_cookie_removal_log=web_filter_cookie_removal_log,
            web_url_log=web_url_log,
            web_invalid_domain_log=web_invalid_domain_log,
            web_ftgd_err_log=web_ftgd_err_log,
            web_ftgd_quota_usage=web_ftgd_quota_usage,
            extended_log=extended_log,
            web_extended_all_action_log=web_extended_all_action_log,
            web_antiphishing_log=web_antiphishing_log,
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
        Move webfilter/profile object to a new position.
        
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
            >>> fgt.api.cmdb.webfilter_profile.move(
            ...     name=100,
            ...     position="top"
            ... )
            
            >>> # Move to specific position (3rd place)
            >>> fgt.api.cmdb.webfilter_profile.move(
            ...     name=100,
            ...     position=3
            ... )
            
            >>> # Move before another object
            >>> fgt.api.cmdb.webfilter_profile.move(
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
        endpoint = "/webfilter/profile/" + quote_path_param(name)
        return self._client.put(  # type: ignore[return-value]
            "cmdb", endpoint, data={}, params=params, vdom=vdom        )





