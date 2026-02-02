"""
FortiOS MONITOR - Fortiview realtime_statistics

Configuration endpoint for managing monitor fortiview/realtime_statistics objects.

API Endpoints:
    GET    /monitor/fortiview/realtime_statistics
    POST   /monitor/fortiview/realtime_statistics
    PUT    /monitor/fortiview/realtime_statistics/{identifier}
    DELETE /monitor/fortiview/realtime_statistics/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.fortiview_realtime_statistics.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.fortiview_realtime_statistics.post(
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

class RealtimeStatistics(CRUDEndpoint, MetadataMixin):
    """RealtimeStatistics Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "realtime_statistics"
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = False
    SUPPORTS_READ = True
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = False
    SUPPORTS_MOVE = False
    SUPPORTS_CLONE = False
    SUPPORTS_FILTERING = False
    SUPPORTS_PAGINATION = False
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize RealtimeStatistics endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        srcaddr: str | None = None,
        dstaddr: str | None = None,
        srcaddr6: str | None = None,
        dstaddr6: str | None = None,
        srcport: str | None = None,
        dstport: str | None = None,
        srcintf: str | None = None,
        srcintfrole: list[str] | None = None,
        dstintf: str | None = None,
        dstintfrole: list[str] | None = None,
        policyid: str | None = None,
        security_policyid: str | None = None,
        protocol: str | None = None,
        web_category: str | None = None,
        web_domain: str | None = None,
        application: str | None = None,
        country: str | None = None,
        seconds: str | None = None,
        since: str | None = None,
        owner: str | None = None,
        username: str | None = None,
        shaper: str | None = None,
        srcuuid: str | None = None,
        dstuuid: str | None = None,
        sessionid: int | None = None,
        report_by: str | None = None,
        sort_by: str | None = None,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve fortiview/realtime_statistics configuration.

        Retrieve realtime drill-down and summary data for FortiView.

        Args:
            srcaddr: Source IPv4 address.
            dstaddr: Destination IPv4 address.
            srcaddr6: Source IPv6 address.
            dstaddr6: Destination IPv6 address.
            srcport: Source TCP port number.
            dstport: Destination TCP port number.
            srcintf: Source interface name.
            srcintfrole: Source interface role name.
            dstintf: Destination interface name.
            dstintfrole: Destination interface role name.
            policyid: Firewall policy ID.
            security_policyid: NGFW policy ID.
            protocol: Protocol type.
            web_category: Web category ID.
            web_domain: Web domain name.
            application: Web application type. It can be ID, or protocol/port pair.
            country: Geographic location.
            seconds: Time in seconds, since the session is established.
            since: Time when the session is established.
            owner: Owner.
            username: Session login user name.
            shaper: Traffic shaper name.
            srcuuid: UUID of source.
            dstuuid: UUID of destination.
            sessionid: FortiView request Session ID.
            report_by: Report by field.
            sort_by: Sort by field.
            ip_version: IP version [*ipv4 | ipv6 | ipboth].
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
            >>> # Get all fortiview/realtime_statistics objects
            >>> result = fgt.api.monitor.fortiview_realtime_statistics.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.monitor.fortiview_realtime_statistics.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.monitor.fortiview_realtime_statistics.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.monitor.fortiview_realtime_statistics.get_schema()

        See Also:
            - post(): Create new fortiview/realtime_statistics object
            - put(): Update existing fortiview/realtime_statistics object
            - delete(): Remove fortiview/realtime_statistics object
            - exists(): Check if object exists
        """
        params = payload_dict.copy() if payload_dict else {}
        
        # Add explicit query parameters
        if filter is not None:
            params["filter"] = filter
        if count is not None:
            params["count"] = count
        if start is not None:
            params["start"] = start
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
        if srcintfrole is not None:
            params["srcintfrole"] = srcintfrole
        if dstintf is not None:
            params["dstintf"] = dstintf
        if dstintfrole is not None:
            params["dstintfrole"] = dstintfrole
        if policyid is not None:
            params["policyid"] = policyid
        if security_policyid is not None:
            params["security-policyid"] = security_policyid
        if protocol is not None:
            params["protocol"] = protocol
        if web_category is not None:
            params["web-category"] = web_category
        if web_domain is not None:
            params["web-domain"] = web_domain
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
        if shaper is not None:
            params["shaper"] = shaper
        if srcuuid is not None:
            params["srcuuid"] = srcuuid
        if dstuuid is not None:
            params["dstuuid"] = dstuuid
        if sessionid is not None:
            params["sessionid"] = sessionid
        if report_by is not None:
            params["report_by"] = report_by
        if sort_by is not None:
            params["sort_by"] = sort_by
        if ip_version is not None:
            params["ip_version"] = ip_version
        
        endpoint = "/fortiview/realtime-statistics"
        unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "monitor", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )












