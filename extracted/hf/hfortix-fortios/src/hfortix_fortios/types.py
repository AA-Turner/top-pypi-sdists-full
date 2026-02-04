"""
FortiOS API Response Types

TypedDict classes for FortiOS API responses to provide IDE autocomplete
and type checking.

Auto-generated - DO NOT EDIT
"""

from typing import Any, Literal, TypedDict

from typing_extensions import NotRequired


class FortiOSSuccessResponse(TypedDict):
    """
    Standard successful response from FortiOS API.

    Examples:
        >>> result = fgt.api.cmdb.firewall.address.get(name="web-server")
        >>> result["status"]  # IDE autocompletes!
        'success'
        >>> result["http_status"]
        200
    """

    http_method: str
    """HTTP method used (GET, POST, PUT, DELETE)"""

    results: list[dict[str, Any]] | dict[str, Any]
    """Response data - list for collection queries, dict for single items"""

    vdom: str
    """Virtual domain name"""

    path: str
    """API endpoint path"""

    name: NotRequired[str]
    """Object name (only present for single object queries)"""

    status: Literal["success"]
    """Response status - always 'success' for this type"""

    http_status: int
    """HTTP status code (200 for success)"""

    build: int
    """FortiOS build number"""

    version: str
    """FortiOS version string (e.g., 'v7.6.5')"""

    serial: str
    """Device serial number"""


class FortiOSErrorResponse(TypedDict):
    """
    Error response from FortiOS API.

    Examples:
        >>> try:
        ...     result = fgt.api.cmdb.firewall.address.get(name="nonexistent")
        ... except ResourceNotFoundError as e:
        ...     print(e.response["error"])  # IDE autocompletes!
        ...     404
    """

    http_method: str
    """HTTP method used"""

    error: int
    """Error code (e.g., -3 for object not found)"""

    message: NotRequired[str]
    """Human-readable error message"""

    http_status: int
    """HTTP status code (4xx or 5xx)"""

    status: NotRequired[Literal["error"]]
    """Response status - 'error' when present"""

    vdom: NotRequired[str]
    """Virtual domain name"""

    path: NotRequired[str]
    """API endpoint path"""


class FortiOSResponse(TypedDict):
    """
    Generic FortiOS API response (success or error).

    Use this when the response could be either success or error.
    For better type safety, use FortiOSSuccessResponse or FortiOSErrorResponse.

    Examples:
        >>> result: FortiOSResponse = fgt.api.cmdb.firewall.address.get()
        >>> if result.get("status") == "success":
        ...     # Type narrowed to success response
        ...     items = result["results"]
    """

    http_method: str
    results: NotRequired[list[dict[str, Any]] | dict[str, Any]]
    vdom: NotRequired[str]
    path: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[Literal["success", "error"]]
    http_status: int
    error: NotRequired[int]
    message: NotRequired[str]
    build: NotRequired[int]
    version: NotRequired[str]
    serial: NotRequired[str]


class FortiOSListResponse(TypedDict):
    """
    FortiOS API response with list results (collection queries).
    
    Use this type when you know the response will contain a list of items,
    such as when calling `.get()` without a `name` parameter.
    
    Example:
        >>> response: FortiOSListResponse = fgt.api.cmdb.firewall.address.get()
        >>> first_address = response["results"][0]  # No type error!
    """

    http_method: str
    results: list[dict[str, Any]]
    vdom: str
    path: str
    status: Literal["success"]
    http_status: int
    build: int
    version: str
    serial: str


class FortiOSDictResponse(TypedDict):
    """
    FortiOS API response with dict results (single object queries).
    
    Use this type when you know the response will contain a single object,
    such as when calling `.get(name="...")`.
    
    Example:
        >>> response: FortiOSDictResponse = fgt.api.cmdb.firewall.address.get(name="web-server")
        >>> address_name = response["results"]["name"]  # No type error!
    """

    http_method: str
    results: dict[str, Any]
    vdom: str
    path: str
    name: str
    status: Literal["success"]
    http_status: int
    build: int
    version: str
    serial: str


# Common Literal types used across multiple endpoints
ActionType = Literal["accept", "deny", "ipsec"]
"""Common firewall policy action types"""

StatusType = Literal["enable", "disable"]
"""Common enable/disable status"""

LogSeverity = Literal[
    "emergency",
    "alert",
    "critical",
    "error",
    "warning",
    "notification",
    "information",
    "debug",
]
"""Syslog severity levels"""

ScheduleType = Literal["onetime", "recurring"]
"""Schedule types"""

ProtocolType = Literal["tcp", "udp", "icmp", "icmpv6", "ip", "sctp"]
"""Common IP protocol types"""


__all__ = [
    "FortiOSSuccessResponse",
    "FortiOSListResponse",
    "FortiOSDictResponse",
    "FortiOSErrorResponse",
    "FortiOSResponse",
    "ActionType",
    "StatusType",
    "LogSeverity",
    "ScheduleType",
    "ProtocolType",
]
