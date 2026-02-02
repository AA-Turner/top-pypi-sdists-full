"""Type stubs for FortiOS API response types."""

from typing import Any, Literal, TypedDict, overload
from typing_extensions import NotRequired


class FortiOSSuccessResponse(TypedDict):
    """
    Standard successful response from FortiOS API.
    
    The `results` field can be either:
    - `list[dict[str, Any]]` for collection queries (e.g., get all addresses)
    - `dict[str, Any]` for single object queries (e.g., get by name)
    
    To safely index into results:
    ```python
    results = response["results"]
    if isinstance(results, list):
        first = results[0]  # Safe list indexing
    else:
        value = results["key"]  # Safe dict access
    ```
    """

    http_method: str
    results: list[dict[str, Any]] | dict[str, Any]
    vdom: str
    path: str
    name: NotRequired[str]
    status: Literal["success"]
    http_status: int
    build: int
    version: str
    serial: str


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


class FortiOSErrorResponse(TypedDict):
    """Error response from FortiOS API."""

    http_method: str
    error: int
    message: NotRequired[str]
    http_status: int
    status: NotRequired[Literal["error"]]
    vdom: NotRequired[str]
    path: NotRequired[str]


class FortiOSResponse(TypedDict, total=False):
    """
    Generic FortiOS API response (success or error).
    
    Use this when the response could be either success or error.
    For better type safety, use FortiOSSuccessResponse, FortiOSListResponse,
    FortiOSDictResponse, or FortiOSErrorResponse.
    """

    http_method: str
    results: list[dict[str, Any]] | dict[str, Any]
    error: int
    message: str
    vdom: str
    path: str
    name: str
    status: Literal["success", "error"]
    http_status: int
    build: int
    version: str
    serial: str


# Type aliases for common Literal types
ActionType = Literal["accept", "deny", "ipsec", "ssl-vpn", "redirect", "isolate"]
StatusType = Literal["enable", "disable"]
LogSeverity = Literal["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"]
ScheduleType = Literal["always", "none", "iCalendar"]
ProtocolType = Literal["TCP/UDP/SCTP", "ICMP", "ICMP6", "IP", "HTTP", "FTP", "CONNECT", "SOCKS-TCP", "SOCKS-UDP", "ALL"]


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
