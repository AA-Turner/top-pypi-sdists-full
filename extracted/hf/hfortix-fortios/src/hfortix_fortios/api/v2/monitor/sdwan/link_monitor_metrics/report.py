"""
FortiOS MONITOR - Sdwan link_monitor_metrics report

Configuration endpoint for managing monitor sdwan/link_monitor_metrics/report objects.

API Endpoints:
    GET    /monitor/sdwan/link_monitor_metrics/report
    POST   /monitor/sdwan/link_monitor_metrics/report
    PUT    /monitor/sdwan/link_monitor_metrics/report/{identifier}
    DELETE /monitor/sdwan/link_monitor_metrics/report/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.sdwan_link_monitor_metrics_report.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.sdwan_link_monitor_metrics_report.post(
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

class Report(CRUDEndpoint, MetadataMixin):
    """Report Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "report"
    
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
        """Initialize Report endpoint."""
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
        agent_ip: str | None = None,
        application_name: str | None = None,
        application_id: Any | None = None,
        latency: Any | None = None,
        jitter: Any | None = None,
        packet_loss: Any | None = None,
        ntt: Any | None = None,
        srt: Any | None = None,
        application_error: Any | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new sdwan/link_monitor_metrics/report object.

        Report the application-level performance metrics collected by other fabric devices.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            agent_ip: agent_ip
            application_name: application_name
            application_id: application_id
            latency: latency
            jitter: jitter
            packet_loss: packet_loss
            ntt: ntt
            srt: srt
            application_error: application_error
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.monitor.sdwan_link_monitor_metrics_report.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created object: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = Report.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.monitor.sdwan_link_monitor_metrics_report.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(Report.required_fields()) }}
            
            Use Report.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="monitor",
            agent_ip=agent_ip,
            application_name=application_name,
            application_id=application_id,
            latency=latency,
            jitter=jitter,
            packet_loss=packet_loss,
            ntt=ntt,
            srt=srt,
            application_error=application_error,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.report import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="monitor/sdwan/link_monitor_metrics/report",
            )

        endpoint = "/sdwan/link-monitor-metrics/report"
        return self._client.post(  # type: ignore[return-value]
            "monitor", endpoint, data=payload_data, vdom=vdom        )









