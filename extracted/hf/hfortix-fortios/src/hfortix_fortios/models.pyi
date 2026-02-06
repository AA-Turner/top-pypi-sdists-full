"""
Type stubs for FortiOS Object Models

Provides type hints for zero-maintenance object wrappers for FortiOS API responses.
"""

import builtins
from collections.abc import Mapping
from typing import Any, Generator, Generic, Iterator, Literal, SupportsIndex, TypeVar, overload
from typing_extensions import Self

_T = TypeVar("_T")
_DataT = TypeVar("_DataT", bound=Mapping[str, Any])
_KT = TypeVar("_KT", bound=str)
_VT = TypeVar("_VT")

class FortiObject(Generic[_DataT]):
    """
    Zero-maintenance wrapper for FortiOS API responses.

    Provides clean attribute access to API response data with automatic
    flattening of member_table fields (lists of dicts with 'name' keys).

    Features:
    - No schemas required - works with any FortiOS version
    - No code generation - same class for all endpoints
    - No maintenance - automatically handles new fields
    - Auto-flattening of member_table fields for clean access
    - Escape hatch via get_full() for raw data access

    Common Response Fields (present in most API responses):
        status: API response status ("success" or "error")
        http_status: HTTP status code (200, 404, 500, etc.)
        error: Error code (integer, present when status="error")
        error_description: Human-readable error message
        vdom: Virtual domain name
        serial: Device serial number
        version: API version string
        build: Firmware build number

    Examples:
        >>> # From dict response
        >>> data = {"name": "policy1", "srcaddr": [{"name": "addr1"}]}
        >>> obj = FortiObject(data)
        >>>
        >>> # Clean attribute access
        >>> obj.name
        'policy1'
        >>>
        >>> # Auto-flattened member_table fields
        >>> obj.srcaddr
        ['addr1']
        >>>
        >>> # Get raw data when needed
        >>> obj.get_full('srcaddr')
        [{'name': 'addr1'}]
        >>>
        >>> # Convert back to dict
        >>> obj.to_dict()
        {'name': 'policy1', 'srcaddr': [{'name': 'addr1'}]}
        >>>
        >>> # Common response fields (autocomplete available)
        >>> result = fgt.api.cmdb.firewall.policy.delete(policyid=1)
        >>> result.status  # "success" or "error"
        >>> result.http_status  # 200, 404, etc.

    Args:
        data: Dictionary from FortiOS API response
    """

    _data: dict[str, Any]
    _raw_envelope: dict[str, Any] | None
    _response_time: float | None

    # ========================================================================
    # Explicit envelope properties (for autocomplete - these are common fields)
    # ========================================================================

    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        ...

    @property
    def http_status(self) -> str | None:
        """API response status ('success' or 'error')."""
        ...

    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        ...

    @property
    def fgt_vdom(self) -> str | None:
        """FortiGate virtual domain name from API response."""
        ...

    @property
    def fgt_mkey(self) -> str | int | None:
        """FortiGate primary key (mkey) of created/modified object."""
        ...

    @property
    def fgt_revision(self) -> str | None:
        """FortiGate configuration revision number."""
        ...
    
    @property
    def fgt_revision_changed(self) -> bool:
        """Whether the configuration revision changed (indicates config was modified)."""
        ...
    
    @property
    def fgt_old_revision(self) -> str | None:
        """FortiGate previous configuration revision number (before this change)."""
        ...

    @property
    def fgt_serial(self) -> str | None:
        """FortiGate device serial number."""
        ...

    @property
    def fgt_version(self) -> str | None:
        """FortiOS version string (e.g., 'v7.6.5')."""
        ...

    @property
    def fgt_build(self) -> int | None:
        """FortiOS firmware build number."""
        ...
    
    @property
    def fgt_api_path(self) -> str | None:
        """API path segment (e.g., 'firewall', 'system', 'user')."""
        ...
    
    @property
    def fgt_api_name(self) -> str | None:
        """API endpoint name (e.g., 'address', 'policy', 'interface')."""
        ...
    
    @property
    def fgt_response_size(self) -> int | None:
        """Number of objects returned in the response (for list operations)."""
        ...
    
    @property
    def fgt_action(self) -> str | None:
        """API action performed (appears in some response types)."""
        ...
    
    @property
    def fgt_limit_reached(self) -> bool:
        """Whether the pagination limit was reached in a list query."""
        ...
    
    @property
    def fgt_matched_count(self) -> int | None:
        """Number of objects matching the query criteria."""
        ...
    
    @property
    def fgt_next_idx(self) -> int | None:
        """Index for the next page in paginated results."""
        ...

    @property
    def http_response_time(self) -> float | None:
        """
        Response time in milliseconds for this API request.
        
        Returns None if timing was not tracked.
        
        Examples:
            >>> result = fgt.api.cmdb.firewall.address.get()
            >>> print(f"Query took {result.http_response_time:.1f}ms")
            Query took 45.2ms
        """
        ...

    # ========================================================================
    # FortiManager Proxy Metadata Properties
    # ========================================================================
    
    @property
    def fmg_proxy_status_code(self) -> int | None:
        """FortiManager proxy status code for this request."""
        ...
    
    @property
    def fmg_proxy_status_message(self) -> str | None:
        """FortiManager proxy status message for this request."""
        ...
    
    @property
    def fmg_proxy_target(self) -> str | None:
        """Target device name in FortiManager proxy request."""
        ...
    
    @property
    def fmg_proxy_url(self) -> str | None:
        """FortiManager proxy URL used for this request."""
        ...
    
    @property
    def fmg_url(self) -> str | None:
        """FortiGate API URL called through FortiManager."""
        ...
    
    @property
    def fmg_status_code(self) -> int | None:
        """FortiManager status code for the device response."""
        ...
    
    @property
    def fmg_status_message(self) -> str | None:
        """FortiManager status message for the device response."""
        ...
    
    @property
    def fmg_id(self) -> int | None:
        """FortiManager request ID."""
        ...
    
    @property
    def fmg_raw(self) -> dict | None:
        """Raw FortiManager response data."""
        ...

    @property
    def http_stats(self) -> dict[str, Any]:
        """
        HTTP request/response statistics summary.
        
        Returns a dictionary with key HTTP stats for debugging and monitoring.
        
        Returns:
            Dictionary with:
                - http_status_code: HTTP status code (200, 404, etc.)
                - http_response_time: Response time in milliseconds
                - http_method: HTTP method (GET, POST, PUT, DELETE)
                - http_status: API status ('success' or 'error')
                - vdom: Virtual domain name
        
        Examples:
            >>> result = fgt.api.cmdb.firewall.address.get()
            >>> print(result.http_stats)
            {'http_status_code': 200, 'http_response_time': 45.2, 'http_method': 'GET', 'http_status': 'success', 'vdom': 'root'}
        """
        ...

    def __init__(
        self,
        data: _DataT,
        raw_envelope: dict[str, Any] | None = None,
        response_time: float | None = None,
    ) -> None:
        """
        Initialize FortiObject with API response data.

        Args:
            data: Dictionary containing the API response fields (typed based on _DataT)
        """
        ...

    def get_full(self, name: str) -> Any:
        """
        Get raw field value without automatic processing.

        Use this when you need the full object structure from a member_table
        field instead of the auto-flattened name list.

        Args:
            name: Field name to retrieve

        Returns:
            Raw field value without any processing

        Examples:
            >>> obj.get_full('srcaddr')
            [{'name': 'addr1', 'q_origin_key': 'addr1'}]
        """
        ...

    def to_dict(self) -> dict[str, Any]:
        """
        Get the original dictionary data.

        Returns:
            Original API response dictionary

        Examples:
            >>> obj.to_dict()
            {'policyid': 1, 'name': 'policy1', ...}
        """
        ...
    
    @property
    def json(self) -> str:
        """
        Get pretty-printed JSON string of the object.

        Returns:
            JSON string with 2-space indentation

        Examples:
            >>> policy = fgt.api.cmdb.firewall.policy.get(policyid=1)
            >>> print(policy.json)
            {
              "policyid": 1,
              "name": "my-policy",
              "action": "accept"
            }
        """
        ...
    
    @property
    def dict(self) -> _DataT:
        """
        Get the dictionary representation of the object.

        Alias for `.json` - provides an intuitive way to convert
        FortiObject back to a plain dictionary when needed.

        Returns:
            Original API response dictionary (typed based on the data type)

        Examples:
            >>> policy = fgt.api.cmdb.firewall.policy.get(policyid=1)
            >>> policy.dict
            {'policyid': 1, 'name': 'my-policy', ...}
        """
        ...
    
    @property
    def raw(self) -> builtins.dict[str, Any]:
        """
        Get the raw/full API response envelope.

        Returns the complete API response including metadata like http_status,
        status, vdom, revision, etc. Use this when you need to check response
        status or access envelope-level information.

        Returns:
            Full API response envelope dictionary

        Examples:
            >>> policy = fgt.api.cmdb.firewall.policy.get(policyid=1)
            >>> policy.raw
            {'http_status': 200, 'status': 'success', 'vdom': 'root', 'results': {...}}
            >>> policy.raw['status']
            'success'
        """
        ...

    def __repr__(self) -> str:
        """
        String representation of the object.

        Returns:
            String showing object type and identifier (name or policyid)
        """
        ...

    def __contains__(self, key: str) -> bool:
        """
        Check if field exists in the object.

        Args:
            key: Field name to check

        Returns:
            True if field exists, False otherwise

        Examples:
            >>> 'srcaddr' in obj
            True
        """
        ...

    def __getitem__(self, key: str) -> Any:
        """
        Dictionary-style access to object fields.
        
        For typed access, use .dict["field"] instead.
        
        Args:
            key: Field name to retrieve
        
        Returns:
            Field value (untyped)
        
        Examples:
            >>> obj["name"]
            'my-policy'
        """
        ...

    def __len__(self) -> int:
        """
        Get number of fields in the object.

        Returns:
            Number of fields in the response data

        Examples:
            >>> len(obj)
            15
        """
        ...

    def __iter__(self) -> Iterator[FortiObject[Any]]:
        """
        Iterate over items when FortiObject wraps a list response.

        This method allows iteration over FortiObject instances when the
        underlying data is a list (common in monitor endpoints).

        Returns:
            Iterator yielding FortiObject instances for each list item

        Examples:
            >>> result = fgt.api.monitor.switch_controller.managed_switch.dhcp_snooping.get()
            >>> for entry in result:
            ...     print(entry.switch_id)
        """
        ...

    def keys(self) -> Any:
        """
        Get all field names.

        Returns:
            Dictionary keys view of all field names

        Examples:
            >>> list(obj.keys())
            ['policyid', 'name', 'srcaddr', 'dstaddr', ...]
        """
        ...

    def values(self) -> Generator[Any, None, None]:
        """
        Get all field values (processed).

        Note: This returns processed values (with auto-flattening).
        Use to_dict().values() for raw values.

        Returns:
            Generator of processed field values
        """
        ...

    def items(self) -> Generator[tuple[str, Any], None, None]:
        """
        Get all field name-value pairs (processed).

        Note: This returns processed values (with auto-flattening).
        Use to_dict().items() for raw values.

        Returns:
            Generator of (key, processed_value) tuples
        """
        ...

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get field value with optional default (dict-like interface).

        Args:
            key: Field name to retrieve
            default: Value to return if field doesn't exist

        Returns:
            Processed field value or default

        Examples:
            >>> obj.get('action', 'deny')
            'accept'
            >>> obj.get('nonexistent', 'default')
            'default'
        """
        ...


_ObjectT = TypeVar("_ObjectT", bound=FortiObject)


class FortiObjectList(list[_ObjectT], Generic[_ObjectT]):
    """
    A list of FortiObject instances with convenient access to raw API response.
    
    This class extends the standard list to provide additional properties
    for accessing the data in different formats. It stores the full API
    envelope so you can access metadata like http_status, vdom, etc.
    
    Properties:
        dict: Returns list of dictionaries (each FortiObject as dict)
        json: Returns pretty-printed JSON string  
        raw: Returns the full API response envelope
        response_time: Response time in seconds
        response_time_ms: Response time in milliseconds
    
    Examples:
        >>> policies = fgt.api.cmdb.firewall.policy.get()
        >>> policies[0].name  # Access like normal list of FortiObjects
        'my-policy'
        >>> 
        >>> # Get as list of dicts
        >>> policies.dict
        [{'policyid': 1, 'name': 'my-policy', ...}, ...]
        >>>
        >>> # Get pretty JSON string
        >>> print(policies.json)
        [
          {
            "policyid": 1,
            "name": "my-policy",
            ...
          }
        ]
        >>>
        >>> # Get full API envelope with metadata
        >>> policies.raw
        {'http_status': 200, 'vdom': 'root', 'results': [...], ...}
        >>>
        >>> # Check response timing
        >>> print(f"Query took {policies.response_time_ms:.1f}ms")
        Query took 125.3ms
    """
    
    _raw_envelope: dict[str, Any] | None
    _response_time: float | None
    
    def __init__(
        self, 
        items: list[_ObjectT] | None = None, 
        raw_envelope: dict[str, Any] | None = None,
        response_time: float | None = None,
    ) -> None:
        """
        Initialize FortiObjectList.
        
        Args:
            items: List of FortiObject instances or other items
            raw_envelope: The full API response envelope (optional)
            response_time: Response time in seconds (optional)
        """
        ...

    # ========================================================================
    # Iterator and indexing support for proper type inference
    # ========================================================================
    
    def __iter__(self) -> Iterator[_ObjectT]:
        """Iterate over FortiObject items."""
        ...
    
    @overload
    def __getitem__(self, index: SupportsIndex, /) -> _ObjectT: ...
    @overload
    def __getitem__(self, index: slice, /) -> list[_ObjectT]: ...

    # ========================================================================
    # Response timing properties
    # ========================================================================

    @property
    def http_response_time(self) -> float | None:
        """Response time in milliseconds for this API request."""
        ...

    @property
    def http_stats(self) -> dict[str, Any]:
        """
        HTTP request/response statistics summary.
        
        Returns a dictionary with key HTTP stats for debugging and monitoring.
        
        Returns:
            Dictionary with:
                - http_status_code: HTTP status code (200, 404, etc.)
                - http_response_time: Response time in milliseconds
                - http_method: HTTP method (GET, POST, PUT, DELETE)
                - http_status: API status ('success' or 'error')
                - vdom: Virtual domain name
        """
        ...

    # ========================================================================
    # Envelope properties (common API response fields)
    # ========================================================================

    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        ...

    @property
    def http_status(self) -> str | None:
        """API response status ('success' or 'error')."""
        ...

    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        ...

    @property
    def vdom(self) -> str | None:
        """Virtual domain name."""
        ...

    @property
    def serial(self) -> str | None:
        """Device serial number."""
        ...

    @property
    def version(self) -> str | None:
        """FortiOS version string (e.g., 'v7.6.5')."""
        ...

    @property
    def build(self) -> int | None:
        """FortiOS firmware build number."""
        ...
    
    # ========================================================================
    # FortiManager Proxy Metadata Properties
    # ========================================================================
    
    @property
    def fmg_proxy_status_code(self) -> int | None:
        """FortiManager proxy status code for this request."""
        ...
    
    @property
    def fmg_proxy_status_message(self) -> str | None:
        """FortiManager proxy status message for this request."""
        ...
    
    @property
    def fmg_proxy_target(self) -> str | None:
        """Target device name in FortiManager proxy request."""
        ...
    
    @property
    def fmg_proxy_url(self) -> str | None:
        """FortiManager proxy URL used for this request."""
        ...
    
    @property
    def fmg_url(self) -> str | None:
        """FortiGate API URL called through FortiManager."""
        ...
    
    @property
    def fmg_status_code(self) -> int | None:
        """FortiManager status code for the device response."""
        ...
    
    @property
    def fmg_status_message(self) -> str | None:
        """FortiManager status message for the device response."""
        ...
    
    @property
    def fmg_id(self) -> int | None:
        """FortiManager request ID."""
        ...
    
    @property
    def fmg_raw(self) -> dict | None:
        """Raw FortiManager response data."""
        ...
    
    @property
    def dict(self) -> list[dict[str, Any]]:
        """
        Get list of dictionaries.
        
        Converts each FortiObject back to its dictionary representation.
        Non-FortiObject items are returned as-is.
        
        Returns:
            List of dictionaries
        """
        ...
    
    @property
    def json(self) -> str:
        """
        Get pretty-printed JSON string of the list.
        
        Returns:
            JSON string with 2-space indentation
        """
        ...
    
    @property
    def raw(self) -> builtins.dict[str, Any] | builtins.list[builtins.dict[str, Any]]:
        """
        Get the full API response envelope.
        
        Returns the complete API response including metadata like
        http_status, vdom, revision, build, etc. If no envelope
        was stored, returns the list of dicts.
        
        Returns:
            Full API envelope dict, or list of dicts if no envelope available
        """
        ...


# ============================================================================
# Content Response for Binary/File Download Endpoints
# ============================================================================

CONTENT_ENDPOINTS: dict[str, dict[str, Any]]
"""
Registry of endpoints that return binary/text content.

Format: "api_type.module.endpoint" -> metadata dict
"""

def is_content_endpoint(endpoint_path: str) -> bool:
    """
    Check if an endpoint returns binary/text content.
    
    Args:
        endpoint_path: Endpoint path in format "api_type.module.endpoint"
    
    Returns:
        True if endpoint is registered as a content endpoint
    """
    ...


class ContentResponse:
    """
    Response wrapper for endpoints that return binary/text content.
    
    Some FortiOS endpoints return raw content (config files, certificates,
    crash logs, etc.) instead of structured JSON. This class provides a
    consistent interface for accessing both the content and standard
    API response metadata.
    
    Examples:
        >>> result = fgt.api.monitor.system.config_revision.file.get(config_id=45)
        >>> result.content  # Raw bytes
        b'#config-version=...'
        >>> result.text  # As string
        '#config-version=...'
        >>> result.content_type
        'text/plain'
        >>> result.http_status_code
        200
        >>> result.to_dict()  # Parse FortiOS config
        {'global': {'system global': {...}}}
    """
    
    _data: dict[str, Any]
    _raw_envelope: dict[str, Any]
    _response_time: float | None
    _endpoint_path: str | None
    _endpoint_meta: dict[str, Any]
    
    def __init__(
        self,
        data: dict[str, Any],
        raw_envelope: dict[str, Any] | None = None,
        response_time: float | None = None,
        endpoint_path: str | None = None,
    ) -> None: ...
    
    # Content Properties
    
    @property
    def content(self) -> bytes:
        """Raw bytes content from the response."""
        ...
    
    @property
    def content_type(self) -> str:
        """MIME type of the content (e.g., 'text/plain')."""
        ...
    
    @property
    def text(self) -> str:
        """Content decoded as UTF-8 string."""
        ...
    
    # Standard API Response Properties
    
    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        ...
    
    @property
    def http_status(self) -> str | None:
        """API response status ('success' or 'error')."""
        ...
    
    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        ...
    
    @property
    def vdom(self) -> str | None:
        """Virtual domain name."""
        ...
    
    @property
    def serial(self) -> str | None:
        """Device serial number."""
        ...
    
    @property
    def version(self) -> str | None:
        """FortiOS version string (e.g., 'v7.6.5')."""
        ...
    
    @property
    def build(self) -> int | None:
        """FortiOS firmware build number."""
        ...
    
    @property
    def revision(self) -> str | None:
        """Configuration revision number."""
        ...
    
    @property
    def http_response_time(self) -> float | None:
        """Response time in milliseconds for this API request."""
        ...
    
    @property
    def http_stats(self) -> dict[str, Any]:
        """HTTP request/response statistics summary."""
        ...
    
    @property
    def raw(self) -> dict[str, Any]:
        """Full API response envelope."""
        ...
    
    # Content Processing Methods
    
    def to_text(self, encoding: str = "utf-8") -> str:
        """Decode content to string with specified encoding."""
        ...
    
    def to_dict(self) -> dict[str, Any]:
        """
        Parse content to dictionary (for parseable content types).
        
        Raises:
            ValueError: If content type is not parseable
        """
        ...
    
    def to_json(self, indent: int = 2) -> str:
        """
        Get parsed content as JSON string.
        
        Raises:
            ValueError: If content type is not parseable
        """
        ...
    
    def save(self, path: str, mode: str = "wb") -> None:
        """Save content to file."""
        ...
    
    def __getattr__(self, name: str) -> Any:
        """Dynamic attribute access for endpoint-specific fields."""
        ...
    
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...


def parse_fortios_config(content: str) -> dict[str, Any]:
    """
    Parse FortiOS configuration file format to dictionary.
    
    Args:
        content: FortiOS config file content as string
    
    Returns:
        Nested dictionary representing the config structure
    
    Examples:
        >>> config = parse_fortios_config('''
        ... config system global
        ...     set hostname "my-firewall"
        ... end
        ... ''')
        >>> config['system global']['hostname']
        'my-firewall'
    """
    ...


# Overloads for process_response to provide accurate return types
@overload
def process_response(
    result: list[dict[str, Any]],
    unwrap_single: Literal[False] = False,
    raw_envelope: dict[str, Any] | None = None,
    response_time: float | None = None,
) -> FortiObjectList:
    """Process list response - returns FortiObjectList."""
    ...

@overload
def process_response(
    result: list[dict[str, Any]],
    unwrap_single: Literal[True],
    raw_envelope: dict[str, Any] | None = None,
    response_time: float | None = None,
) -> FortiObject:
    """Process list response with unwrap_single - returns single FortiObject."""
    ...

@overload
def process_response(
    result: dict[str, Any],
    unwrap_single: bool = False,
    raw_envelope: dict[str, Any] | None = None,
    response_time: float | None = None,
) -> FortiObject | FortiObjectList:
    """Process dict response - may return FortiObject or FortiObjectList."""
    ...

# Fallback overload for any other types (strings, None, etc.)
@overload
def process_response(
    result: Any,
    unwrap_single: bool = False,
    raw_envelope: dict[str, Any] | None = None,
    response_time: float | None = None,
) -> Any:
    """Fallback for non-dict/list types - returns result as-is."""
    ...
