"""
FortiOS MONITOR - Firewall proxy sessions

Configuration endpoint for managing monitor firewall/proxy/sessions objects.

API Endpoints:
    GET    /monitor/firewall/proxy/sessions
    POST   /monitor/firewall/proxy/sessions
    PUT    /monitor/firewall/proxy/sessions/{identifier}
    DELETE /monitor/firewall/proxy/sessions/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.firewall_proxy_sessions.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.firewall_proxy_sessions.post(
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

class Sessions(CRUDEndpoint, MetadataMixin):
    """Sessions Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "sessions"
    
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
    SUPPORTS_PAGINATION = True
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Sessions endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        ip_version: Literal["ipv4", "ipv6", "ipboth"] | None = None,
        summary: bool | None = None,
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
        src_uuid: str | None = None,
        dst_uuid: str | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve firewall/proxy/sessions configuration.

        List all active proxy sessions (optionally filtered).

        Args:
            ip_version: IP version [*ipv4 | ipv6 | ipboth].
            count: Maximum number of entries to return. Valid range is [20, 1000]; if a value is specified out of that range, it will be rounded up or down.
            summary: Enable/disable inclusion of session summary (setup rate, total sessions, etc).
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
            src_uuid: UUID of source.
            dst_uuid: UUID of destination.
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
            >>> # Get all firewall/proxy/sessions objects
            >>> result = fgt.api.monitor.firewall_proxy_sessions.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.monitor.firewall_proxy_sessions.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.monitor.firewall_proxy_sessions.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.monitor.firewall_proxy_sessions.get_schema()

        See Also:
            - post(): Create new firewall/proxy/sessions object
            - put(): Update existing firewall/proxy/sessions object
            - delete(): Remove firewall/proxy/sessions object
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
        if ip_version is not None:
            params["ip_version"] = ip_version
        if summary is not None:
            params["summary"] = summary
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
        if src_uuid is not None:
            params["src_uuid"] = src_uuid
        if dst_uuid is not None:
            params["dst_uuid"] = dst_uuid
        
        endpoint = "/firewall/proxy/sessions"
        unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "monitor", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )












