"""
FortiOS MONITOR - Switch_controller mclag_icl tier_plus_candidates

Configuration endpoint for managing monitor switch_controller/mclag_icl/tier_plus_candidates objects.

API Endpoints:
    GET    /monitor/switch_controller/mclag_icl/tier_plus_candidates
    POST   /monitor/switch_controller/mclag_icl/tier_plus_candidates
    PUT    /monitor/switch_controller/mclag_icl/tier_plus_candidates/{identifier}
    DELETE /monitor/switch_controller/mclag_icl/tier_plus_candidates/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.switch_controller_mclag_icl_tier_plus_candidates.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.switch_controller_mclag_icl_tier_plus_candidates.post(
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

class TierPlusCandidates(CRUDEndpoint, MetadataMixin):
    """TierPlusCandidates Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "tier_plus_candidates"
    
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
        """Initialize TierPlusCandidates endpoint."""
        self._client = client

    # ========================================================================
    # GET Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Endpoint-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def get(  # type: ignore[override]
        self,
        fortilink: str | None = None,
        parent_peer1: str | None = None,
        parent_peer2: str | None = None,
        is_tier2: bool | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, FortiObjectList, Coroutine[Any, Any, Union[FortiObject, FortiObjectList]]]:
        """
        Retrieve switch_controller/mclag_icl/tier_plus_candidates configuration.

        Find a pair of FortiSwitches that are eligible to form a tier 2/3 MC-LAG.

        Args:
            fortilink: FortiLink interface name.
            parent_peer1: FortiSwitch ID for MC-LAG parent peer 1.
            parent_peer2: FortiSwitch ID for MC-LAG parent peer 2.
            is_tier2: Whether candidates are for a Tier 2 MC-LAG.
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
            >>> # Get all switch_controller/mclag_icl/tier_plus_candidates objects
            >>> result = fgt.api.monitor.switch_controller_mclag_icl_tier_plus_candidates.get()
            >>> print(f"Found {len(result['results'])} objects")
            
            >>> # Get with filter
            >>> result = fgt.api.monitor.switch_controller_mclag_icl_tier_plus_candidates.get(
            ...     filter=["name==test", "status==enable"]
            ... )
            
            >>> # Get with pagination
            >>> result = fgt.api.monitor.switch_controller_mclag_icl_tier_plus_candidates.get(
            ...     start=0, count=100
            ... )
            
            >>> # Get schema information  
            >>> schema = fgt.api.monitor.switch_controller_mclag_icl_tier_plus_candidates.get_schema()

        See Also:
            - post(): Create new switch_controller/mclag_icl/tier_plus_candidates object
            - put(): Update existing switch_controller/mclag_icl/tier_plus_candidates object
            - delete(): Remove switch_controller/mclag_icl/tier_plus_candidates object
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
        if fortilink is not None:
            params["fortilink"] = fortilink
        if parent_peer1 is not None:
            params["parent_peer1"] = parent_peer1
        if parent_peer2 is not None:
            params["parent_peer2"] = parent_peer2
        if is_tier2 is not None:
            params["is_tier2"] = is_tier2
        
        endpoint = "/switch-controller/mclag-icl/tier-plus-candidates"
        unwrap_single = False
        
        return self._client.get(  # type: ignore[return-value]
            "monitor", endpoint, params=params, vdom=vdom, unwrap_single=unwrap_single
        )












