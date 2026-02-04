"""
FortiOS MONITOR - Switch_controller mclag_icl set_tier_plus

Configuration endpoint for managing monitor switch_controller/mclag_icl/set_tier_plus objects.

API Endpoints:
    GET    /monitor/switch_controller/mclag_icl/set_tier_plus
    POST   /monitor/switch_controller/mclag_icl/set_tier_plus
    PUT    /monitor/switch_controller/mclag_icl/set_tier_plus/{identifier}
    DELETE /monitor/switch_controller/mclag_icl/set_tier_plus/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.switch_controller_mclag_icl_set_tier_plus.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.switch_controller_mclag_icl_set_tier_plus.post(
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

class SetTierPlus(CRUDEndpoint, MetadataMixin):
    """SetTierPlus Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "set_tier_plus"
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = True
    SUPPORTS_READ = False
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = False
    SUPPORTS_MOVE = False
    # SUPPORTS_CLONE = False  # Disabled - unreliable across endpoints
    SUPPORTS_FILTERING = False
    SUPPORTS_PAGINATION = False
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize SetTierPlus endpoint."""
        self._client = client



    # ========================================================================
    # POST Method
    # Type hints provided by CRUDEndpoint protocol (no local @overload needed)
    # Note: Field-specific parameters intentionally extend the protocol's **kwargs
    #       to provide autocomplete. Type checkers may report signature mismatch.
    # ========================================================================
    
    def post(  # type: ignore[override]
        self,
        payload_dict: dict[str, Any] | None = None,
        fortilink: str | None = None,
        parent_peer1: str | None = None,
        parent_peer2: str | None = None,
        peer1: str | None = None,
        peer2: str | None = None,
        isl_port_group: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new switch_controller/mclag_icl/set_tier_plus object.

        Setup a tier 2/3 MC-LAG link between a pair of FortiSwitches.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            fortilink: fortilink
            parent_peer1: parent_peer1
            parent_peer2: parent_peer2
            peer1: peer1
            peer2: peer2
            isl_port_group: isl_port_group
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.monitor.switch_controller_mclag_icl_set_tier_plus.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created object: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = SetTierPlus.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.monitor.switch_controller_mclag_icl_set_tier_plus.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(SetTierPlus.required_fields()) }}
            
            Use SetTierPlus.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="monitor",
            fortilink=fortilink,
            parent_peer1=parent_peer1,
            parent_peer2=parent_peer2,
            peer1=peer1,
            peer2=peer2,
            isl_port_group=isl_port_group,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.set_tier_plus import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="monitor/switch_controller/mclag_icl/set_tier_plus",
            )

        endpoint = "/switch-controller/mclag-icl/set-tier-plus"
        return self._client.post(  # type: ignore[return-value]
            "monitor", endpoint, data=payload_data, vdom=vdom        )









