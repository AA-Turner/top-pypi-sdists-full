"""
FortiOS MONITOR - Firewall gtp flush

Configuration endpoint for managing monitor firewall/gtp/flush objects.

API Endpoints:
    GET    /monitor/firewall/gtp/flush
    POST   /monitor/firewall/gtp/flush
    PUT    /monitor/firewall/gtp/flush/{identifier}
    DELETE /monitor/firewall/gtp/flush/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.firewall_gtp_flush.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.firewall_gtp_flush.post(
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

class Flush(CRUDEndpoint, MetadataMixin):
    """Flush Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "flush"
    
    # ========================================================================
    # Capabilities (from schema metadata)
    # ========================================================================
    SUPPORTS_CREATE = True
    SUPPORTS_READ = False
    SUPPORTS_UPDATE = True
    SUPPORTS_DELETE = False
    SUPPORTS_MOVE = False
    SUPPORTS_CLONE = False
    SUPPORTS_FILTERING = False
    SUPPORTS_PAGINATION = False
    SUPPORTS_SEARCH = False
    SUPPORTS_SORTING = False

    def __init__(self, client: "IHTTPClient"):
        """Initialize Flush endpoint."""
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
        scope: Literal["global", "vdom"] | None = None,
        gtp_profile: str | None = None,
        version: Any | None = None,
        imsi: str | None = None,
        msisdn: str | None = None,
        ms_addr: str | None = None,
        ms_addr6: str | None = None,
        cteid: Any | None = None,
        cteid_addr: str | None = None,
        cteid_addr6: str | None = None,
        fteid: Any | None = None,
        fteid_addr: str | None = None,
        fteid_addr6: str | None = None,
        apn: str | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new firewall/gtp/flush object.

        Flush GTP tunnels.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            scope: scope
            gtp_profile: gtp_profile
            version: version
            imsi: imsi
            msisdn: msisdn
            ms_addr: ms_addr
            ms_addr6: ms_addr6
            cteid: cteid
            cteid_addr: cteid_addr
            cteid_addr6: cteid_addr6
            fteid: fteid
            fteid_addr: fteid_addr
            fteid_addr6: fteid_addr6
            apn: apn
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.monitor.firewall_gtp_flush.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created object: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Flush.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.monitor.firewall_gtp_flush.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Flush.required_fields()) }}
            
            Use Flush.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="monitor",
            scope=scope,
            gtp_profile=gtp_profile,
            version=version,
            imsi=imsi,
            msisdn=msisdn,
            ms_addr=ms_addr,
            ms_addr6=ms_addr6,
            cteid=cteid,
            cteid_addr=cteid_addr,
            cteid_addr6=cteid_addr6,
            fteid=fteid,
            fteid_addr=fteid_addr,
            fteid_addr6=fteid_addr6,
            apn=apn,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.flush import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="monitor/firewall/gtp/flush",
            )

        endpoint = "/firewall/gtp/flush"
        return self._client.post(  # type: ignore[return-value]
            "monitor", endpoint, data=payload_data, vdom=vdom        )









