"""
FortiOS MONITOR - Firewall policy_lookup

Configuration endpoint for managing monitor firewall/policy_lookup objects.

API Endpoints:
    GET    /monitor/firewall/policy_lookup
    POST   /monitor/firewall/policy_lookup
    PUT    /monitor/firewall/policy_lookup/{identifier}
    DELETE /monitor/firewall/policy_lookup/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.firewall_policy_lookup.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.firewall_policy_lookup.post(
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

class PolicyLookup(CRUDEndpoint, MetadataMixin):
    """PolicyLookup Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "policy_lookup"
    
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
        """Initialize PolicyLookup endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        ipv6: bool | None = None,
        srcintf: str | None = None,
        sourceport: int | None = None,
        sourceip: str | None = None,
        protocol: str | None = None,
        dest: str | None = None,
        destport: int | None = None,
        icmptype: int | None = None,
        icmpcode: int | None = None,
        policy_type: Literal["policy", "proxy"] | None = None,
        auth_type: Literal["user", "group", "saml", "ldap"] | None = None,
        user_group: list[str] | None = None,
        server_name: str | None = None,
        user_db: str | None = None,
        group_attr_type: Literal["name", "id"] | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve firewall/policy_lookup configuration.

        Performs a policy lookup by creating a dummy packet and asking the kernel which policy would be hit.

        Args:
            ipv6: Perform an IPv6 lookup?
            srcintf: Source interface.
            sourceport: Source port.
            sourceip: Source IP.
            protocol: Protocol.
            dest: Destination IP/FQDN.
            destport: Destination port.
            icmptype: ICMP type.
            icmpcode: ICMP code.
            policy_type: Policy type. [*policy | proxy]
            auth_type: Authentication type. [user | group | saml | ldap] Note: this only works for models that can guarantee WAD workers availability, i.e. those that do not disable proxy features globally.
            user_group: List of remote user groups. ['cn=remote desktop users,cn=builtin,dc=devqa,dc=lab','cn=domain users,cn=users,dc=devqa,dc=lab', ...] Note: this only works for models that can guarantee WAD workers availability, i.e. those that do not disable proxy features globally.
            server_name: Remote user/group server name. Note: this only works for models that can guarantee WAD workers availability, i.e. those that do not disable proxy features globally.
            user_db: Authentication server to contain user information.
            group_attr_type: Remote user group attribute type. [*name | id]
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
            >>> # Get all firewall/policy_lookup objects
            >>> result = fgt.api.monitor.firewall_policy_lookup.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.monitor.firewall_policy_lookup.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.monitor.firewall_policy_lookup.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.monitor.firewall_policy_lookup.get_schema()

        See Also:
            - post(): Create new firewall/policy_lookup object
            - put(): Update existing firewall/policy_lookup object
            - delete(): Remove firewall/policy_lookup object
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
        if ipv6 is not None:
            params["ipv6"] = ipv6
        if srcintf is not None:
            params["srcintf"] = srcintf
        if sourceport is not None:
            params["sourceport"] = sourceport
        if sourceip is not None:
            params["sourceip"] = sourceip
        if protocol is not None:
            params["protocol"] = protocol
        if dest is not None:
            params["dest"] = dest
        if destport is not None:
            params["destport"] = destport
        if icmptype is not None:
            params["icmptype"] = icmptype
        if icmpcode is not None:
            params["icmpcode"] = icmpcode
        if policy_type is not None:
            params["policy_type"] = policy_type
        if auth_type is not None:
            params["auth_type"] = auth_type
        if user_group is not None:
            params["user_group"] = user_group
        if server_name is not None:
            params["server_name"] = server_name
        if user_db is not None:
            params["user_db"] = user_db
        if group_attr_type is not None:
            params["group_attr_type"] = group_attr_type
        
        endpoint = "/firewall/policy-lookup"
        unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "monitor", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )












