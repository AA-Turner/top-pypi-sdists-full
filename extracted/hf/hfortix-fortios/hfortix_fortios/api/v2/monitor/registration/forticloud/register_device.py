"""
FortiOS MONITOR - Registration forticloud register_device

Configuration endpoint for managing monitor registration/forticloud/register_device objects.

API Endpoints:
    GET    /monitor/registration/forticloud/register_device
    POST   /monitor/registration/forticloud/register_device
    PUT    /monitor/registration/forticloud/register_device/{identifier}
    DELETE /monitor/registration/forticloud/register_device/{identifier}

Example Usage:
    >>> from hfortix_fortios import FortiOS
    >>> fgt = FortiOS(host="192.168.1.99", token="your-api-token")
    >>>
    >>> # List all items
    >>> items = fgt.api.monitor.registration_forticloud_register_device.get()
    >>>
    >>> # Create with auto-normalization (strings/lists converted automatically)
    >>> result = fgt.api.monitor.registration_forticloud_register_device.post(
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

class RegisterDevice(CRUDEndpoint, MetadataMixin):
    """RegisterDevice Operations."""
    
    # Configure metadata mixin to use this endpoint's helper module
    _helper_module_name = "register_device"
    
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
        """Initialize RegisterDevice endpoint."""
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
        serial: str | None = None,
        email: str | None = None,
        password: str | None = None,
        reseller: str | None = None,
        reseller_id: Any | None = None,
        country: str | None = None,
        is_government: Any | None = None,
        agreement_accepted: Any | None = None,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> Union[FortiObject, Coroutine[Any, Any, FortiObject]]:
        """
        Create new registration/forticloud/register_device object.

        Register a device to FortiCloud through FortiGate. Currently FortiSwitches, FortiAPs and FortiExtenders are supported.

        Args:
            payload_dict: Complete object data as dict. Alternative to individual parameters.
            serial: serial
            email: email
            password: password
            reseller: reseller
            reseller_id: reseller_id
            country: country
            is_government: is_government
            agreement_accepted: agreement_accepted
            vdom: Virtual domain name. Use True for global, string for specific VDOM.
            error_mode: Override client-level error_mode. "raise" raises exceptions, "return" returns error dict, "print" prints errors.
            error_format: Override client-level error_format. "detailed" provides full context, "simple" is concise, "code_only" returns just status code.

        Returns:
            API response as dictionary. Returns Coroutine if using async client.

        Examples:
            >>> # Create using individual parameters
            >>> result = fgt.api.monitor.registration_forticloud_register_device.post(
            ...     name="example",
            ...     # ... other required fields
            ... )
            >>> print(f"Created object: {result['results']}")
            
            >>> # Create using payload dict
            >>> payload = RegisterDevice.defaults()  # Start with defaults
            >>> payload['name'] = 'my-object'
            >>> result = fgt.api.monitor.registration_forticloud_register_device.post(payload_dict=payload)

        Note:
            Required fields: {{ ", ".join(RegisterDevice.required_fields()) }}
            
            Use RegisterDevice.help('field_name') to get field details.

        See Also:
            - get(): Retrieve objects
            - put(): Update existing object
            - set(): Intelligent create or update
        """
        # Build payload using helper function
        payload_data = build_api_payload(
            api_type="monitor",
            serial=serial,
            email=email,
            password=password,
            reseller=reseller,
            reseller_id=reseller_id,
            country=country,
            is_government=is_government,
            agreement_accepted=agreement_accepted,
            data=payload_dict,
        )

        # Check for deprecated fields and warn users
        from ._helpers.register_device import DEPRECATED_FIELDS
        if DEPRECATED_FIELDS:
            from hfortix_core import check_deprecated_fields
            check_deprecated_fields(
                payload=payload_data,
                deprecated_fields=DEPRECATED_FIELDS,
                endpoint="monitor/registration/forticloud/register_device",
            )

        endpoint = "/registration/forticloud/register-device"
        return self._client.post(  # type: ignore[return-value]
            "monitor", endpoint, data=payload_data, vdom=vdom        )









