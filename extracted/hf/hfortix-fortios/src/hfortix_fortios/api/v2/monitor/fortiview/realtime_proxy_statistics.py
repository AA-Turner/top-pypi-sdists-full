"""
FortiOS MONITOR - Fortiview realtime_proxy_statistics

Configuration endpoint for managing monitor fortiview/realtime_proxy_statistics objects.

API Endpoints:
    GET    /monitor/fortiview/realtime_proxy_statistics
    POST   /monitor/fortiview/realtime_proxy_statistics
    PUT    /monitor/fortiview/realtime_proxy_statistics/{identifier}
    DELETE /monitor/fortiview/realtime_proxy_statistics/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.fortiview_realtime_proxy_statistics.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.fortiview_realtime_proxy_statistics.post(
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

class RealtimeProxyStatistics(CRUDEndpoint, MetadataMixin):
    """RealtimeProxyStatistics Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "realtime_proxy_statistics"
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = False
    SUPPORTS_READ = True
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = False
    SUPPORTS_MOVE = False
    # SUPPORTS_CLONE = False  # Disabled - unreliable across endpoints
    SUPPORTS_FILTERING = False
    SUPPORTS_PAGINATION = False
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize RealtimeProxyStatistics endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        report_by: str | None = None,
        sort_by: str | None = None,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = None,
        srcaddr: str | None = None,
        dstaddr: str | None = None,
        srcaddr6: str | None = None,
        dstaddr6: str | None = None,
        srcport: str | None = None,
        dstport: str | None = None,
        srcintf: str | None = None,
        dstintf: str | None = None,
        policyid: str | None = None,
        proxy_policyid: str | None = None,
        protocol: str | None = None,
        application: str | None = None,
        country: str | None = None,
        seconds: str | None = None,
        since: str | None = None,
        owner: str | None = None,
        username: str | None = None,
        srcuuid: str | None = None,
        dstuuid: str | None = None,
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
        Retrieve fortiview/realtime_proxy_statistics configuration.

        Retrieve realtime drill-down and summary data for proxy session FortiView statistics.

        Args:
            report_by: Report by field.
            sort_by: Sort by field.
            ip_version: IP version [*ipv4 | ipv6 | ipboth].
            srcaddr: Source IPv4 address.
            dstaddr: Destination IPv4 address.
            srcaddr6: Source IPv6 address.
            dstaddr6: Destination IPv6 address.
            srcport: Source TCP port number.
            dstport: Destination TCP port number.
            srcintf: Source interface name.
            dstintf: Destination interface name.
            policyid: Firewall policy ID.
            proxy_policyid: Explicit proxy policy ID.
            protocol: Protocol type.
            application: Web application type.
            country: Geographic location.
            seconds: Time in seconds, since the session is established.
            since: Time when the session is established.
            owner: Owner.
            username: Session login user name.
            srcuuid: UUID of source.
            dstuuid: UUID of destination.
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
            >>> # Get all fortiview/realtime_proxy_statistics objects
            >>> result = fgt.api.monitor.fortiview_realtime_proxy_statistics.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.monitor.fortiview_realtime_proxy_statistics.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.monitor.fortiview_realtime_proxy_statistics.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.monitor.fortiview_realtime_proxy_statistics.get_schema()

        See Also:
            - post(): Create new fortiview/realtime_proxy_statistics object
            - put(): Update existing fortiview/realtime_proxy_statistics object
            - delete(): Remove fortiview/realtime_proxy_statistics object
            - exists(): Check if object exists
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
        if report_by is not None:
            params["report_by"] = report_by
        if sort_by is not None:
            params["sort_by"] = sort_by
        if ip_version is not None:
            params["ip_version"] = ip_version
        if srcaddr is not None:
            params["srcaddr"] = srcaddr
        if dstaddr is not None:
            params["dstaddr"] = dstaddr
        if srcaddr6 is not None:
            params["srcaddr6"] = srcaddr6
        if dstaddr6 is not None:
            params["dstaddr6"] = dstaddr6
        if srcport is not None:
            params["srcport"] = srcport
        if dstport is not None:
            params["dstport"] = dstport
        if srcintf is not None:
            params["srcintf"] = srcintf
        if dstintf is not None:
            params["dstintf"] = dstintf
        if policyid is not None:
            params["policyid"] = policyid
        if proxy_policyid is not None:
            params["proxy-policyid"] = proxy_policyid
        if protocol is not None:
            params["protocol"] = protocol
        if application is not None:
            params["application"] = application
        if country is not None:
            params["country"] = country
        if seconds is not None:
            params["seconds"] = seconds
        if since is not None:
            params["since"] = since
        if owner is not None:
            params["owner"] = owner
        if username is not None:
            params["username"] = username
        if srcuuid is not None:
            params["srcuuid"] = srcuuid
        if dstuuid is not None:
            params["dstuuid"] = dstuuid
        
        endpoint = "/fortiview/realtime-proxy-statistics"
        unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "monitor", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )












