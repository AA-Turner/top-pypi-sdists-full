"""
FortiOS Object Models

Provides zero-maintenance object wrappers for FortiOS API responses.
"""

from __future__ import annotations

import json as json_module
from typing import Any, Iterator


# API field to Python keyword mapping (reverse of PYTHON_KEYWORD_TO_API_FIELD)
# When the API returns fields that are Python keywords, map them to safe names
API_FIELD_TO_PYTHON_KEYWORD = {
    "as": "asn",  # BGP AS number (API 'as' -> Python 'asn')
    "class": "class_",  # Class fields (API 'class' -> Python 'class_')
    "type": "type_",  # Type fields (API 'type' -> Python 'type_')
    "from": "from_",  # From fields
    "import": "import_",  # Import fields
    "global": "global_",  # Global fields
}


class FortiObject:
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
    - Access full API envelope via .raw property

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
        >>> # Access full API envelope
        >>> obj.raw
        {'http_status': 200, 'status': 'success', 'results': {...}}

    Args:
        data: Dictionary from FortiOS API response
        raw_envelope: Optional full API response envelope (with http_status, results, etc.)
    """

    def __init__(
        self,
        data: dict,
        raw_envelope: dict | None = None,
        response_time: float | None = None,
        request_info: dict | None = None,
    ):
        """
        Initialize FortiObject with API response data.

        Args:
            data: Dictionary containing the API response fields
            raw_envelope: Optional full API response envelope
            response_time: Optional response time in seconds (from HTTP request)
            request_info: Optional HTTP request information (method, url, params, data)
        """
        self._data = data
        self._raw_envelope = raw_envelope
        self._response_time = response_time
        self._request_info = request_info

    # ========================================================================
    # Explicit envelope properties (for autocomplete - these are common fields)
    # ========================================================================

    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        if self._raw_envelope:
            return self._raw_envelope.get("http_status")
        return self._data.get("http_status")

    @property
    def http_status(self) -> str | None:
        """API response status ('success' or 'error').
        
        Note: This returns the API envelope status, not object fields.
        Object fields like 'status' are accessed via attribute (obj.status)
        or dict access (obj["status"]).
        """
        if self._raw_envelope:
            return self._raw_envelope.get("status")
        return self._data.get("status")

    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        if self._raw_envelope:
            return self._raw_envelope.get("http_method")
        return self._data.get("http_method")

    @property
    def fgt_vdom(self) -> str | None:
        """FortiGate virtual domain name from API response."""
        if self._raw_envelope:
            return self._raw_envelope.get("vdom")
        return self._data.get("vdom")

    @property
    def fgt_mkey(self) -> str | int | None:
        """FortiGate primary key (mkey) of created/modified object."""
        if self._raw_envelope:
            return self._raw_envelope.get("mkey")
        return self._data.get("mkey")

    @property
    def fgt_revision(self) -> str | None:
        """FortiGate configuration revision number."""
        if self._raw_envelope:
            return self._raw_envelope.get("revision")
        return self._data.get("revision")
    
    @property
    def fgt_revision_changed(self) -> bool:
        """Whether the configuration revision changed (indicates config was modified)."""
        if self._raw_envelope:
            return self._raw_envelope.get("revision_changed", False)
        return self._data.get("revision_changed", False)
    
    @property
    def fgt_old_revision(self) -> str | None:
        """FortiGate previous configuration revision number (before this change)."""
        if self._raw_envelope:
            return self._raw_envelope.get("old_revision")
        return self._data.get("old_revision")

    @property
    def fgt_serial(self) -> str | None:
        """FortiGate device serial number."""
        if self._raw_envelope:
            return self._raw_envelope.get("serial")
        return self._data.get("serial")

    @property
    def fgt_version(self) -> str | None:
        """FortiOS version string (e.g., 'v7.6.5')."""
        if self._raw_envelope:
            return self._raw_envelope.get("version")
        return self._data.get("version")

    @property
    def fgt_build(self) -> int | None:
        """FortiOS firmware build number."""
        if self._raw_envelope:
            return self._raw_envelope.get("build")
        return self._data.get("build")
    
    @property
    def fgt_api_path(self) -> str | None:
        """API path segment (e.g., 'firewall', 'system', 'user')."""
        if self._raw_envelope:
            return self._raw_envelope.get("path")
        return self._data.get("path")
    
    @property
    def fgt_api_name(self) -> str | None:
        """API endpoint name (e.g., 'address', 'policy', 'interface')."""
        if self._raw_envelope:
            return self._raw_envelope.get("name")
        return self._data.get("name")
    
    @property
    def fgt_response_size(self) -> int | None:
        """Number of objects returned in the response (for list operations)."""
        if self._raw_envelope:
            return self._raw_envelope.get("size")
        return self._data.get("size")
    
    @property
    def fgt_action(self) -> str | None:
        """API action performed (appears in some response types)."""
        if self._raw_envelope:
            return self._raw_envelope.get("action")
        return self._data.get("action")
    
    @property
    def fgt_limit_reached(self) -> bool:
        """Whether the pagination limit was reached in a list query."""
        if self._raw_envelope:
            return self._raw_envelope.get("limit_reached", False)
        return self._data.get("limit_reached", False)
    
    @property
    def fgt_matched_count(self) -> int | None:
        """Number of objects matching the query criteria."""
        if self._raw_envelope:
            return self._raw_envelope.get("matched_count")
        return self._data.get("matched_count")
    
    @property
    def fgt_next_idx(self) -> int | None:
        """Index for the next page in paginated results."""
        if self._raw_envelope:
            return self._raw_envelope.get("next_idx")
        return self._data.get("next_idx")

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
        return self._response_time * 1000 if self._response_time else None

    @property
    def http_api_request(self) -> dict[str, Any] | None:
        """
        HTTP API request information for this response.
        
        Returns dictionary with request details including:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: Full URL that was requested
        - endpoint: API endpoint path
        - params: Query parameters sent
        - data: Request body (for POST/PUT)
        - timestamp: Unix timestamp when request was made
        
        Returns None if request information was not tracked.
        
        Examples:
            >>> result = fgt.api.cmdb.firewall.address.get(filter='subnet==10.0.0.0/8')
            >>> print(result.http_api_request)
            {
                'method': 'GET',
                'url': 'https://192.168.1.99/api/v2/cmdb/firewall/address',
                'endpoint': '/api/v2/cmdb/firewall/address',
                'params': {'filter': 'subnet==10.0.0.0/8', 'vdom': 'root'},
                'data': None,
                'timestamp': 1706889600.123
            }
            
            >>> policy = fgt.api.cmdb.firewall.policy.post(
            ...     name="test",
            ...     srcintf=[{"name": "wan1"}],
            ...     dstintf=[{"name": "wan2"}]
            ... )
            >>> print(policy.http_api_request)
            {
                'method': 'POST',
                'url': 'https://192.168.1.99/api/v2/cmdb/firewall/policy',
                'endpoint': '/api/v2/cmdb/firewall/policy',
                'params': {'vdom': 'root'},
                'data': {'name': 'test', 'srcintf': [{'name': 'wan1'}], 'dstintf': [{'name': 'wan2'}]},
                'timestamp': 1706889601.456
            }
        """
        return self._request_info

    @property
    def fmg_api_request(self) -> dict[str, Any] | None:
        """
        Alias for http_api_request when using FortiManager proxy.
        
        This property provides the same information as http_api_request but with
        a name that makes it clearer when working with FortiManager proxy connections.
        
        Returns dictionary with request details including:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: Full FMG proxy URL that was requested
        - endpoint: API endpoint path
        - params: Query parameters sent
        - data: Request body (for POST/PUT)
        - timestamp: Unix timestamp when request was made
        
        Returns None if request information was not tracked.
        
        Examples:
            >>> # Using FortiManager proxy to manage a device
            >>> result = fmg.devices['FGT-01'].api.cmdb.firewall.address.get()
            >>> print(result.fmg_api_request)
            {
                'method': 'GET',
                'url': 'https://fmg.example.com/jsonrpc',
                'endpoint': '/api/v2/cmdb/firewall/address',
                'params': {'vdom': 'root'},
                'data': {...},
                'timestamp': 1706889600.123
            }
        """
        return self._request_info

    # ========================================================================
    # FortiManager Proxy Metadata Properties
    # ========================================================================
    
    @property
    def fmg_proxy_status_code(self) -> int | None:
        """FortiManager proxy status code for this request."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_proxy_status_code")
        return self._data.get("fmg_proxy_status_code")
    
    @property
    def fmg_proxy_status_message(self) -> str | None:
        """FortiManager proxy status message for this request."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_proxy_status_message")
        return self._data.get("fmg_proxy_status_message")
    
    @property
    def fmg_proxy_target(self) -> str | None:
        """Target device name in FortiManager proxy request."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_proxy_target")
        return self._data.get("fmg_proxy_target")
    
    @property
    def fmg_proxy_url(self) -> str | None:
        """FortiManager proxy URL used for this request."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_proxy_url")
        return self._data.get("fmg_proxy_url")
    
    @property
    def fmg_url(self) -> str | None:
        """FortiGate API URL called through FortiManager."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_url")
        return self._data.get("fmg_url")
    
    @property
    def fmg_status_code(self) -> int | None:
        """FortiManager status code for the device response."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_status_code")
        return self._data.get("fmg_status_code")
    
    @property
    def fmg_status_message(self) -> str | None:
        """FortiManager status message for the device response."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_status_message")
        return self._data.get("fmg_status_message")
    
    @property
    def fmg_id(self) -> int | None:
        """FortiManager request ID."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_id")
        return self._data.get("fmg_id")
    
    @property
    def fmg_raw(self) -> dict | None:
        """Raw FortiManager response data."""
        if self._raw_envelope:
            return self._raw_envelope.get("fmg_raw")
        return self._data.get("fmg_raw")

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
        return {
            "http_status_code": self.http_status_code,
            "http_response_time": self.http_response_time,
            "http_method": self.http_method,
            "http_status": self.http_status,
            "vdom": self.vdom,
        }

    def __getattr__(self, name: str) -> Any:
        """
        Dynamic attribute access with automatic wrapping of nested objects.

        For most FortiOS fields (strings, ints, etc.), returns the value as-is.
        For nested objects (dicts) and member_table fields (lists of dicts),
        automatically wraps them in FortiObject for clean attribute access.

        Args:
            name: Attribute name to access

        Returns:
            Field value, with dicts and lists of dicts wrapped in FortiObject

        Raises:
            AttributeError: If accessing private attributes (starting with '_')

        Examples:
            >>> obj.srcaddr  # Member table as list of FortiObjects
            [FortiObject({'name': 'addr1'}), FortiObject({'name': 'addr2'})]
            >>> obj.srcaddr[0].name  # Access name attribute
            'addr1'
            >>> obj.ipv6.ip6_address  # Nested object attribute access
            'fd12:3456:789a:bcde::1/128'
            >>> obj.action  # Regular field
            'accept'
            >>> obj.asn  # Python keyword mapping (API 'as' -> Python 'asn')
            '65001'
        """
        if name.startswith("_"):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

        # Resolve key with priority order:
        # 1. Check if name maps to API keyword (e.g., 'asn' -> 'as')
        # 2. Try exact name match
        # 3. Try snake_case -> hyphen-case conversion
        
        # Check reverse keyword mapping (Python name -> API field)
        reverse_keyword_map = {v: k for k, v in API_FIELD_TO_PYTHON_KEYWORD.items()}
        if name in reverse_keyword_map:
            key = reverse_keyword_map[name]
        elif name in self._data:
            key = name
        else:
            key = name.replace("_", "-")

        # If key not present, behave like previous implementation and return None
        if key not in self._data:
            return None

        value = self._data.get(key)

        # Auto-wrap nested objects (single dict) in FortiObject for attribute access
        if isinstance(value, dict):
            return FortiObject(value)

        # Auto-wrap member_table fields (lists of dicts) in FortiObjectList
        # Wrap both empty and non-empty lists so .dict property is always available
        if isinstance(value, list):
            if not value:
                # Empty list - wrap in FortiObjectList for consistent .dict access
                return FortiObjectList([])
            if isinstance(value[0], dict):
                return FortiObjectList([FortiObject(item) for item in value])

        return value

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
        # Support reverse keyword mapping, exact names, and hyphenated keys
        reverse_keyword_map = {v: k for k, v in API_FIELD_TO_PYTHON_KEYWORD.items()}
        if name in reverse_keyword_map:
            key = reverse_keyword_map[name]
        elif name in self._data:
            key = name
        else:
            key = name.replace("_", "-")
        return self._data.get(key)

    def to_dict(self) -> dict:
        """
        Get the original dictionary data.

        Returns:
            Original API response dictionary

        Examples:
            >>> obj.to_dict()
            {'policyid': 1, 'name': 'policy1', ...}
        """
        return self._data

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
        import json
        
        # Create a sanitized copy to avoid circular reference issues
        # This can happen with FMG proxy responses where fmg_raw contains the full response
        def _sanitize_dict(obj: Any, seen: set | None = None) -> Any:
            """Remove circular references from nested dicts."""
            if seen is None:
                seen = set()
            
            if isinstance(obj, dict):
                obj_id = id(obj)
                if obj_id in seen:
                    return "<circular reference>"
                seen.add(obj_id)
                
                result = {}
                for key, value in obj.items():
                    result[key] = _sanitize_dict(value, seen.copy())
                return result
            elif isinstance(obj, list):
                return [_sanitize_dict(item, seen.copy()) for item in obj]
            else:
                return obj
        
        sanitized_data = _sanitize_dict(self._data)
        return json.dumps(sanitized_data, indent=2)
    
    @property
    def dict(self) -> dict:
        """
        Get the dictionary representation of the object.

        Alias for `.json` property - provides an intuitive way to convert
        FortiObject back to a plain dictionary when needed.

        Returns:
            Original API response dictionary

        Examples:
            >>> policy = fgt.api.cmdb.firewall.policy.get(policyid=1)
            >>> policy.dict
            {'policyid': 1, 'name': 'my-policy', 'action': 'accept', ...}
            >>> 
            >>> # Use when you need dict operations
            >>> policy_dict = policy.dict
            >>> policy_dict.update({'comment': 'Updated via API'})
        """
        return self._data
    
    @property
    def raw(self) -> dict:
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
        # Return the full envelope if available, otherwise fall back to data
        return self._raw_envelope if self._raw_envelope is not None else self._data

    def __repr__(self) -> str:
        """
        String representation of the object.

        For mutation responses (POST/PUT/DELETE with empty or minimal results),
        shows the API response. For GET results with data, shows the object
        identifier or field count.

        Returns:
            String showing API response or object identifier

        Examples:
            >>> repr(delete_result)  # Mutation response
            "FortiOS(status=success, http=200, mkey=Test-Address-01, vdom=test)"
            >>> repr(address)  # GET result with data
            "FortiOS(status=success, http=200, vdom=root) -> FortiObject(my-address)"
        """
        # Build response info from envelope if available
        response_info = None
        if self._raw_envelope is not None:
            status = self._raw_envelope.get("status", "unknown")
            http_status = self._raw_envelope.get("http_status", "?")
            mkey = self._raw_envelope.get("mkey", "")
            vdom = self._raw_envelope.get("vdom", "")
            
            parts = [f"status={status}", f"http={http_status}"]
            if mkey:
                parts.append(f"mkey={mkey}")
            if vdom:
                parts.append(f"vdom={vdom}")
            
            response_info = f"FortiOS({', '.join(parts)})"
        
        # Check if this is a mutation response (POST/PUT/DELETE)
        # Mutation responses have metadata like path/name/revision, not actual object data
        is_mutation = (
            self._raw_envelope is not None and 
            self._raw_envelope.get("http_method") in ("POST", "PUT", "DELETE")
        )
        
        # For mutations, just show the response info (no object data to show)
        if is_mutation:
            return response_info or "FortiOS(mutation)"
        
        # Try to find a meaningful identifier from the data
        identifier = self._data.get("name") or self._data.get("policyid")
        
        # For simple member objects (only name + q_origin_key), just show the name
        # This makes lists of members much cleaner: ['addr1', 'addr2'] vs [FortiObject(addr1), ...]
        keys = set(self._data.keys())
        if keys == {"name"} or keys == {"name", "q_origin_key"}:
            return repr(self._data.get("name"))
        
        # Build object info for GET responses
        if len(self._data) == 0:
            object_info = None  # No data to show
        elif identifier:
            object_info = f"FortiObject({identifier})"
        else:
            object_info = f"FortiObject({len(self._data)} fields)"
        
        # Combine response info and object info
        if response_info and object_info:
            return f"{response_info} -> {object_info}"
        elif response_info:
            return response_info
        elif object_info:
            return object_info
        else:
            return "FortiObject(empty)"

    def __str__(self) -> str:
        """
        User-friendly string representation.

        For mutation responses (POST/PUT/DELETE), returns the same as repr()
        showing the API response. For GET results, returns the primary identifier.

        Examples:
            >>> str(delete_result)  # Mutation
            'FortiOS(status=success, http=200, mkey=test, vdom=root)'
            >>> str(address)  # GET result
            'my-address'
        """
        # Check if this is a mutation response - use repr for those
        if self._raw_envelope is not None:
            http_method = self._raw_envelope.get("http_method")
            if http_method in ("POST", "PUT", "DELETE"):
                return self.__repr__()
        
        # For GET results, return the primary identifier
        return str(
            self._data.get("name")
            or self._data.get("policyid")
            or self.__repr__()
        )

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
        # Consider both exact key and underscore->hyphen variants
        return key in self._data or key.replace("_", "-") in self._data

    def __getitem__(self, key: str) -> Any:
        """
        Dictionary-style access to fields.

        Provides dict-like bracket notation access to object fields,
        with the same auto-flattening behavior as attribute access.

        Args:
            key: Field name to access

        Returns:
            Field value, with member_table fields auto-flattened

        Raises:
            KeyError: If the field does not exist

        Examples:
            >>> obj['srcaddr']
            ['addr1', 'addr2']
            >>> obj['action']
            'accept'
        """
        # Resolve key presence for both formats
        if key in self._data:
            raw_key = key
        elif key.replace("_", "-") in self._data:
            raw_key = key.replace("_", "-")
        else:
            raise KeyError(key)

        # Return processed value (apply same logic as attribute access)
        value = self._data[raw_key]
        if isinstance(value, list) and value and isinstance(value[0], dict):
            return [FortiObject(item) for item in value]
        return value

    def __len__(self) -> int:
        """
        Get number of fields in the object.

        Returns:
            Number of fields in the response data

        Examples:
            >>> len(obj)
            15
        """
        return len(self._data)

    def __iter__(self) -> Iterator[FortiObject]:
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

        Raises:
            TypeError: If the wrapped data is not a list
        """
        # Check if _data contains a list in 'results' key (monitor endpoints)
        if isinstance(self._data, dict):
            results = self._data.get("results", [])
            if isinstance(results, list):
                for item in results:
                    if isinstance(item, dict):
                        yield FortiObject(item, self._raw_envelope, self._response_time)
                    else:
                        yield item
                return

        # If _data itself is a list, iterate over it
        if isinstance(self._data, list):
            for item in self._data:
                if isinstance(item, dict):
                    yield FortiObject(item, self._raw_envelope, self._response_time)
                else:
                    yield item
            return

        # Not iterable - raise error
        raise TypeError(
            f"'{type(self).__name__}' object is not iterable (underlying data is not a list)"
        )

    def keys(self):
        """
        Get all field names.

        Returns:
            Dictionary keys view of all field names

        Examples:
            >>> list(obj.keys())
            ['policyid', 'name', 'srcaddr', 'dstaddr', ...]
        """
        return self._data.keys()

    def values(self):
        """
        Get all field values (processed).

        Note: This returns processed values (with auto-flattening).
        Use to_dict().values() for raw values.

        Returns:
            Generator of processed field values
        """
        for key in self._data.keys():
            yield getattr(self, key)

    def items(self):
        """
        Get all field name-value pairs (processed).

        Note: This returns processed values (with auto-flattening).
        Use to_dict().items() for raw values.

        Returns:
            Generator of (key, processed_value) tuples
        """
        for key in self._data.keys():
            yield (key, getattr(self, key))

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
        # Resolve raw key (support snake_case attribute to hyphenated keys)
        raw_key = key if key in self._data else key.replace("_", "-")
        if raw_key not in self._data:
            return default

        value = self._data[raw_key]
        if isinstance(value, list) and value and isinstance(value[0], dict):
            return FortiObjectList([FortiObject(item) for item in value])
        return value


class FortiObjectList(list):
    """
    A list of FortiObject instances with convenient access to raw API response.
    
    This class extends the standard list to provide additional properties
    for accessing the data in different formats. It stores the full API
    envelope so you can access metadata like http_status, vdom, etc.
    
    Properties:
        dict: Returns list of dictionaries (each FortiObject as dict)
        json: Returns pretty-printed JSON string  
        raw: Returns the full API response envelope
    
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
    """
    
    def __init__(
        self,
        items: list | None = None,
        raw_envelope: dict | None = None,
        response_time: float | None = None,
        request_info: dict | None = None,
    ):
        """
        Initialize FortiObjectList.
        
        Args:
            items: List of FortiObject instances or other items
            raw_envelope: The full API response envelope (optional)
            response_time: Response time in seconds for the HTTP request (optional)
            request_info: HTTP request information (method, url, params, data) (optional)
        """
        super().__init__(items or [])
        self._raw_envelope = raw_envelope
        self._response_time = response_time
        self._request_info = request_info

    # ========================================================================
    # Response timing properties
    # ========================================================================

    @property
    def http_response_time(self) -> float | None:
        """
        Response time in milliseconds for this API request.
        
        Returns None if timing was not tracked.
        
        Examples:
            >>> policies = fgt.api.cmdb.firewall.policy.get()
            >>> print(f"Query took {policies.http_response_time:.1f}ms")
            Query took 125.3ms
        """
        return self._response_time * 1000 if self._response_time else None

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
            >>> policies = fgt.api.cmdb.firewall.policy.get()
            >>> print(policies.http_stats)
            {'http_status_code': 200, 'http_response_time': 125.3, 'http_method': 'GET', 'http_status': 'success', 'vdom': 'root'}
        """
        return {
            "http_status_code": self.http_status_code,
            "http_response_time": self.http_response_time,
            "http_method": self.http_method,
            "http_status": self.http_status,
            "vdom": self.vdom,
        }

    @property
    def http_api_request(self) -> dict[str, Any] | None:
        """
        HTTP API request information for this response.
        
        Returns dictionary with request details including:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: Full URL that was requested
        - endpoint: API endpoint path
        - params: Query parameters sent
        - data: Request body (for POST/PUT)
        - timestamp: Unix timestamp when request was made
        
        Returns None if request information was not tracked.
        
        Examples:
            >>> policies = fgt.api.cmdb.firewall.policy.get(filter='srcaddr==internal')
            >>> print(policies.http_api_request)
            {
                'method': 'GET',
                'url': 'https://192.168.1.99/api/v2/cmdb/firewall/policy',
                'endpoint': '/api/v2/cmdb/firewall/policy',
                'params': {'filter': 'srcaddr==internal', 'vdom': 'root'},
                'data': None,
                'timestamp': 1706889600.123
            }
        """
        return self._request_info

    @property
    def fmg_api_request(self) -> dict[str, Any] | None:
        """
        Alias for http_api_request when using FortiManager proxy.
        
        This property provides the same information as http_api_request but with
        a name that makes it clearer when working with FortiManager proxy connections.
        
        Returns dictionary with request details including:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: Full FMG proxy URL that was requested
        - endpoint: API endpoint path
        - params: Query parameters sent
        - data: Request body (for POST/PUT)
        - timestamp: Unix timestamp when request was made
        
        Returns None if request information was not tracked.
        
        Examples:
            >>> # Using FortiManager proxy to get policies
            >>> policies = fmg.devices['FGT-01'].api.cmdb.firewall.policy.get()
            >>> print(policies.fmg_api_request)
            {
                'method': 'GET',
                'url': 'https://fmg.example.com/jsonrpc',
                'endpoint': '/api/v2/cmdb/firewall/policy',
                'params': {'vdom': 'root'},
                'data': {...},
                'timestamp': 1706889600.123
            }
        """
        return self._request_info

    # ========================================================================
    # FortiManager Proxy Metadata Properties
    # ========================================================================
    
    @property
    def fmg_proxy_status_code(self) -> int | None:
        """FortiManager proxy status code for this request."""
        return self._raw_envelope.get("fmg_proxy_status_code") if self._raw_envelope else None
    
    @property
    def fmg_proxy_status_message(self) -> str | None:
        """FortiManager proxy status message for this request."""
        return self._raw_envelope.get("fmg_proxy_status_message") if self._raw_envelope else None
    
    @property
    def fmg_proxy_target(self) -> str | None:
        """Target device name in FortiManager proxy request."""
        return self._raw_envelope.get("fmg_proxy_target") if self._raw_envelope else None
    
    @property
    def fmg_proxy_url(self) -> str | None:
        """FortiManager proxy URL used for this request."""
        return self._raw_envelope.get("fmg_proxy_url") if self._raw_envelope else None
    
    @property
    def fmg_url(self) -> str | None:
        """FortiGate API URL called through FortiManager."""
        return self._raw_envelope.get("fmg_url") if self._raw_envelope else None
    
    @property
    def fmg_status_code(self) -> int | None:
        """FortiManager status code for the device response."""
        return self._raw_envelope.get("fmg_status_code") if self._raw_envelope else None
    
    @property
    def fmg_status_message(self) -> str | None:
        """FortiManager status message for the device response."""
        return self._raw_envelope.get("fmg_status_message") if self._raw_envelope else None
    
    @property
    def fmg_id(self) -> int | None:
        """FortiManager request ID."""
        return self._raw_envelope.get("fmg_id") if self._raw_envelope else None
    
    @property
    def fmg_raw(self) -> dict | None:
        """Raw FortiManager response data."""
        return self._raw_envelope.get("fmg_raw") if self._raw_envelope else None

    # ========================================================================
    # Envelope properties (common API response fields)
    # ========================================================================

    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        return self._raw_envelope.get("http_status") if self._raw_envelope else None

    @property
    def http_status(self) -> str | None:
        """API response status ('success' or 'error')."""
        return self._raw_envelope.get("status") if self._raw_envelope else None

    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        return self._raw_envelope.get("http_method") if self._raw_envelope else None

    @property
    def vdom(self) -> str | None:
        """Virtual domain name."""
        return self._raw_envelope.get("vdom") if self._raw_envelope else None

    @property
    def serial(self) -> str | None:
        """Device serial number."""
        return self._raw_envelope.get("serial") if self._raw_envelope else None

    @property
    def version(self) -> str | None:
        """FortiOS version string (e.g., 'v7.6.5')."""
        return self._raw_envelope.get("version") if self._raw_envelope else None

    @property
    def build(self) -> int | None:
        """FortiOS firmware build number."""
        return self._raw_envelope.get("build") if self._raw_envelope else None
    
    @property
    def dict(self) -> list[dict]:
        """
        Get list of dictionaries.
        
        Converts each FortiObject back to its dictionary representation.
        Non-FortiObject items are returned as-is.
        
        Returns:
            List of dictionaries
        """
        return [
            item.to_dict() if isinstance(item, FortiObject) else item
            for item in self
        ]
    
    @property
    def json(self) -> str:
        """
        Get pretty-printed JSON string of the list.
        
        Returns:
            JSON string with 2-space indentation
        """
        import json
        
        # Create a sanitized copy to avoid circular reference issues
        # This can happen with FMG proxy responses where fmg_raw contains the full response
        def _sanitize_dict(obj: Any, seen: set | None = None) -> Any:
            """Remove circular references from nested dicts."""
            if seen is None:
                seen = set()
            
            if isinstance(obj, dict):
                obj_id = id(obj)
                if obj_id in seen:
                    return "<circular reference>"
                seen.add(obj_id)
                
                result = {}
                for key, value in obj.items():
                    result[key] = _sanitize_dict(value, seen.copy())
                return result
            elif isinstance(obj, list):
                return [_sanitize_dict(item, seen.copy()) for item in obj]
            else:
                return obj
        
        sanitized_dict = _sanitize_dict(self.dict)
        return json.dumps(sanitized_dict, indent=2)
    
    @property
    def raw(self) -> dict | list[dict]:
        """
        Get the full API response envelope.
        
        Returns the complete API response including metadata like
        http_status, vdom, revision, build, etc. If no envelope
        was stored, returns the list of dicts.
        
        Returns:
            Full API envelope dict, or list of dicts if no envelope available
        """
        if self._raw_envelope is not None:
            return self._raw_envelope
        return self.dict


# ============================================================================
# Content Response for Binary/File Download Endpoints
# ============================================================================

# Registry of endpoints that return binary/text content instead of structured JSON.
# These endpoints return raw content (config files, certificates, logs, etc.)
# Add endpoints here as they are discovered through testing.
#
# Format: "api_type.module.endpoint" -> metadata dict
# Example: "monitor.system.config_revision.file" for /api/v2/monitor/system/config-revision/file
CONTENT_ENDPOINTS: dict[str, dict[str, Any]] = {
    # Config revision file download - returns FortiOS config in text format
    "monitor.system.config_revision.file": {
        "content_type": "text/plain",
        "parseable": True,  # FortiOS config format can be parsed
        "description": "Download a specific configuration revision",
    },
    # Add more endpoints as discovered through testing:
    # "monitor.system.certificate.download": {
    #     "content_type": "application/x-pem-file",
    #     "parseable": False,
    # },
    # "monitor.system.crash_log.download": {
    #     "content_type": "text/plain",
    #     "parseable": False,
    # },
}


def is_content_endpoint(endpoint_path: str) -> bool:
    """
    Check if an endpoint returns binary/text content.
    
    Args:
        endpoint_path: Endpoint path in format "api_type.module.endpoint"
                      e.g., "monitor.system.config_revision.file"
    
    Returns:
        True if endpoint is registered as a content endpoint
    """
    return endpoint_path in CONTENT_ENDPOINTS


class ContentResponse:
    """
    Response wrapper for endpoints that return binary/text content.
    
    Some FortiOS endpoints return raw content (config files, certificates,
    crash logs, etc.) instead of structured JSON. This class provides a
    consistent interface for accessing both the content and standard
    API response metadata.
    
    Properties:
        content: Raw bytes content from the response
        content_type: MIME type of the content (e.g., "text/plain")
        text: Content decoded as UTF-8 string
        
        # Standard API response fields (same as FortiObject):
        http_status_code: HTTP status code (200, 404, etc.)
        http_status: API status ('success' or 'error')
        http_method: HTTP method used
        http_response_time: Response time in milliseconds
        vdom: Virtual domain name
        serial: Device serial number
        version: FortiOS version
        build: FortiOS build number
        raw: Full API response envelope
        
        # Endpoint-specific fields from query params:
        # These are dynamically available based on the endpoint schema
    
    Methods:
        to_text(encoding): Decode content with specified encoding
        to_dict(): Parse FortiOS config format to dictionary (if parseable)
        to_json(): Get parsed content as JSON string
        save(path): Save content to file
    
    Examples:
        >>> # Download config revision
        >>> result = fgt.api.monitor.system.config_revision.file.get(config_id=45)
        >>> 
        >>> # Access raw content
        >>> result.content
        b'#config-version=FGVM64-7.6.5...'
        >>> 
        >>> # Get as text
        >>> result.text
        '#config-version=FGVM64-7.6.5...'
        >>> 
        >>> # Access standard response fields
        >>> result.http_status_code
        200
        >>> result.content_type
        'text/plain'
        >>> 
        >>> # Access endpoint-specific fields
        >>> result.config_id
        45
        >>> 
        >>> # Parse FortiOS config to dict (if supported)
        >>> config = result.to_dict()
        >>> config['global']['system global']['admin-host']
        'fw.wjacobsen.fo'
        >>> 
        >>> # Save to file
        >>> result.save('/tmp/config_backup.conf')
    """
    
    def __init__(
        self,
        data: dict[str, Any],
        raw_envelope: dict[str, Any] | None = None,
        response_time: float | None = None,
        endpoint_path: str | None = None,
        request_info: dict | None = None,
    ):
        """
        Initialize ContentResponse.
        
        Args:
            data: Response data containing 'content' and 'content_type'
            raw_envelope: Full API response envelope
            response_time: Response time in seconds
            endpoint_path: Endpoint path for metadata lookup
            request_info: HTTP request information (method, url, params, data)
        """
        self._data = data
        self._raw_envelope = raw_envelope or data
        self._response_time = response_time
        self._endpoint_path = endpoint_path
        self._endpoint_meta = CONTENT_ENDPOINTS.get(endpoint_path or "", {})
        self._request_info = request_info
    
    # ========================================================================
    # Content Properties
    # ========================================================================
    
    @property
    def content(self) -> bytes:
        """
        Raw bytes content from the response.
        
        Returns:
            Content as bytes. If content was a string, encodes to UTF-8.
        """
        raw_content = self._data.get("content", b"")
        if isinstance(raw_content, str):
            return raw_content.encode("utf-8")
        return raw_content
    
    @property
    def content_type(self) -> str:
        """
        MIME type of the content.
        
        Returns:
            Content type string (e.g., "text/plain", "application/octet-stream")
        """
        return self._data.get("content_type", "application/octet-stream")
    
    @property
    def text(self) -> str:
        """
        Content decoded as UTF-8 string.
        
        Convenience property for text content. For binary content,
        use .content instead.
        
        Returns:
            Content as string
        """
        return self.to_text()
    
    # ========================================================================
    # Standard API Response Properties (consistent with FortiObject)
    # ========================================================================
    
    @property
    def http_status_code(self) -> int | None:
        """HTTP status code (200, 404, 500, etc.)."""
        return self._raw_envelope.get("http_status")
    
    @property
    def http_status(self) -> str | None:
        """API response status ('success' or 'error')."""
        return self._raw_envelope.get("status")
    
    @property
    def http_method(self) -> str | None:
        """HTTP method used (GET, POST, PUT, DELETE)."""
        return self._raw_envelope.get("http_method")
    
    @property
    def vdom(self) -> str | None:
        """Virtual domain name."""
        return self._raw_envelope.get("vdom")
    
    @property
    def serial(self) -> str | None:
        """Device serial number."""
        return self._raw_envelope.get("serial")
    
    @property
    def version(self) -> str | None:
        """FortiOS version string (e.g., 'v7.6.5')."""
        return self._raw_envelope.get("version")
    
    @property
    def build(self) -> int | None:
        """FortiOS firmware build number."""
        return self._raw_envelope.get("build")
    
    @property
    def revision(self) -> str | None:
        """Configuration revision number."""
        return self._raw_envelope.get("revision")
    
    @property
    def http_response_time(self) -> float | None:
        """
        Response time in milliseconds for this API request.
        
        Returns None if timing was not tracked.
        """
        return self._response_time * 1000 if self._response_time else None
    
    @property
    def http_stats(self) -> dict[str, Any]:
        """
        HTTP request/response statistics summary.
        
        Returns:
            Dictionary with http_status_code, http_response_time, http_method,
            http_status, vdom, and content_type
        """
        return {
            "http_status_code": self.http_status_code,
            "http_response_time": self.http_response_time,
            "http_method": self.http_method,
            "http_status": self.http_status,
            "vdom": self.vdom,
            "content_type": self.content_type,
        }
    
    @property
    def http_api_request(self) -> dict[str, Any] | None:
        """
        HTTP API request information for this response.
        
        Returns dictionary with request details including:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: Full URL that was requested
        - endpoint: API endpoint path
        - params: Query parameters sent
        - data: Request body (for POST/PUT)
        - timestamp: Unix timestamp when request was made
        
        Returns None if request information was not tracked.
        
        Examples:
            >>> config = fgt.api.monitor.system.config_revision.file.get(config_id=45)
            >>> print(config.http_api_request)
            {
                'method': 'GET',
                'url': 'https://192.168.1.99/api/v2/monitor/system/config/revision/file',
                'endpoint': '/api/v2/monitor/system/config/revision/file',
                'params': {'config_id': 45, 'vdom': 'root'},
                'data': None,
                'timestamp': 1706889600.123
            }
        """
        return self._request_info
    
    @property
    def fmg_api_request(self) -> dict[str, Any] | None:
        """
        Alias for http_api_request when using FortiManager proxy.
        
        This property provides the same information as http_api_request but with
        a name that makes it clearer when working with FortiManager proxy connections.
        
        Returns dictionary with request details including:
        - method: HTTP method (GET, POST, PUT, DELETE)
        - url: Full FMG proxy URL that was requested
        - endpoint: API endpoint path
        - params: Query parameters sent
        - data: Request body (for POST/PUT)
        - timestamp: Unix timestamp when request was made
        
        Returns None if request information was not tracked.
        
        Examples:
            >>> # Using FortiManager proxy for monitor endpoint
            >>> config = fmg.devices['FGT-01'].api.monitor.system.config_revision.file.get(config_id=45)
            >>> print(config.fmg_api_request)
            {
                'method': 'GET',
                'url': 'https://fmg.example.com/jsonrpc',
                'endpoint': '/api/v2/monitor/system/config/revision/file',
                'params': {'config_id': 45, 'vdom': 'root'},
                'data': {...},
                'timestamp': 1706889600.123
            }
        """
        return self._request_info
    
    @property
    def raw(self) -> dict[str, Any]:
        """
        Full API response envelope.
        
        Returns:
            Complete API response dict
        """
        return self._raw_envelope
    
    # ========================================================================
    # Dynamic Attribute Access (for endpoint-specific fields)
    # ========================================================================
    
    def __getattr__(self, name: str) -> Any:
        """
        Dynamic attribute access for endpoint-specific fields.
        
        Allows access to query parameters that were echoed back in the response
        (e.g., config_id for config revision downloads).
        
        Args:
            name: Attribute name
        
        Returns:
            Field value from response data
        
        Raises:
            AttributeError: If attribute not found
        """
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        
        # Try exact key, then snake_case -> hyphen-case
        key = name if name in self._data else name.replace("_", "-")
        
        if key in self._data:
            return self._data[key]
        
        # Also check raw envelope for metadata
        if key in self._raw_envelope:
            return self._raw_envelope[key]
        
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    # ========================================================================
    # Content Processing Methods
    # ========================================================================
    
    def to_text(self, encoding: str = "utf-8") -> str:
        """
        Decode content to string with specified encoding.
        
        Args:
            encoding: Character encoding (default: utf-8)
        
        Returns:
            Decoded string content
        """
        content = self.content
        if isinstance(content, bytes):
            return content.decode(encoding)
        return str(content)
    
    def to_dict(self) -> dict[str, Any]:
        """
        Parse content to dictionary (for parseable content types).
        
        For FortiOS config files, parses the config format into a
        nested dictionary structure.
        
        Returns:
            Parsed content as dictionary
        
        Raises:
            ValueError: If content type is not parseable
        
        Examples:
            >>> config = result.to_dict()
            >>> config['global']['system global']['admin-host']
            'fw.wjacobsen.fo'
        """
        if not self._endpoint_meta.get("parseable", False):
            raise ValueError(
                f"Content type '{self.content_type}' is not parseable. "
                f"Use .content or .text for raw access."
            )
        
        return parse_fortios_config(self.text)
    
    def to_json(self, indent: int = 2) -> str:
        """
        Get parsed content as JSON string.
        
        Args:
            indent: JSON indentation (default: 2)
        
        Returns:
            JSON string of parsed content
        
        Raises:
            ValueError: If content type is not parseable
        """
        return json_module.dumps(self.to_dict(), indent=indent)
    
    def save(self, path: str, mode: str = "wb") -> None:
        """
        Save content to file.
        
        Args:
            path: File path to save to
            mode: File open mode ('wb' for binary, 'w' for text)
        
        Examples:
            >>> result.save('/tmp/config_backup.conf')
            >>> result.save('/tmp/config.txt', mode='w')  # As text
        """
        content = self.content if "b" in mode else self.text
        with open(path, mode) as f:
            f.write(content)  # type: ignore
    
    # ========================================================================
    # String Representations
    # ========================================================================
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        size = len(self.content)
        size_str = f"{size} bytes" if size < 1024 else f"{size/1024:.1f} KB"
        return (
            f"ContentResponse("
            f"content_type='{self.content_type}', "
            f"size={size_str}, "
            f"http_status={self.http_status_code}"
            f")"
        )
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        return self.__repr__()


def parse_fortios_config(content: str) -> dict[str, Any]:
    """
    Parse FortiOS configuration file format to dictionary.
    
    Parses the hierarchical FortiOS config format:
        config <section>
            edit <name>
                set <key> <value>
                config <subsection>
                    ...
                end
            next
        end
    
    Args:
        content: FortiOS config file content as string
    
    Returns:
        Nested dictionary representing the config structure
    
    Examples:
        >>> config = parse_fortios_config('''
        ... config system global
        ...     set hostname "my-firewall"
        ...     set admin-port 443
        ... end
        ... ''')
        >>> config['system global']['hostname']
        'my-firewall'
    """
    import re
    
    result: dict[str, Any] = {}
    lines = content.strip().split('\n')
    
    # Stack to track nested config blocks
    # Each entry: (section_name, section_dict, is_edit_block)
    stack: list[tuple[str, dict, bool]] = [("root", result, False)]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            # Extract header comments as metadata
            if line.startswith('#') and '=' in line:
                # Parse header like #config-version=FGVM64-7.6.5-FW-build3651
                if '_metadata' not in result:
                    result['_metadata'] = {}
                parts = line[1:].split(':', 1)
                if '=' in parts[0]:
                    key, value = parts[0].split('=', 1)
                    result['_metadata'][key.strip()] = value.strip()
            continue
        
        # Handle "config <section>" - start a new config block
        if line.startswith('config '):
            section_name = line[7:].strip()
            current_name, current_dict, _ = stack[-1]
            
            # Create new section dict
            if section_name not in current_dict:
                current_dict[section_name] = {}
            
            stack.append((section_name, current_dict[section_name], False))
            continue
        
        # Handle "edit <name>" - start an edit block within config
        if line.startswith('edit '):
            edit_name = line[5:].strip().strip('"')
            current_name, current_dict, _ = stack[-1]
            
            # Create entry for this edit block
            if edit_name not in current_dict:
                current_dict[edit_name] = {}
            
            stack.append((edit_name, current_dict[edit_name], True))
            continue
        
        # Handle "set <key> <value>"
        if line.startswith('set '):
            match = re.match(r'set\s+(\S+)\s+(.*)', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip()
                
                # Remove quotes from string values
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                # Try to convert to int
                elif value.isdigit():
                    value = int(value)  # type: ignore
                # Handle enable/disable as booleans
                elif value == 'enable':
                    value = True  # type: ignore
                elif value == 'disable':
                    value = False  # type: ignore
                
                _, current_dict, _ = stack[-1]
                current_dict[key] = value
            continue
        
        # Handle "unset <key>"
        if line.startswith('unset '):
            key = line[6:].strip()
            _, current_dict, _ = stack[-1]
            current_dict[key] = None
            continue
        
        # Handle "next" - close edit block
        if line == 'next':
            if len(stack) > 1:
                _, _, is_edit = stack[-1]
                if is_edit:
                    stack.pop()
            continue
        
        # Handle "end" - close config block
        if line == 'end':
            if len(stack) > 1:
                stack.pop()
            continue
    
    return result


def process_response(
    result: Any,
    unwrap_single: bool = False,
    raw_envelope: dict | None = None,
    response_time: float | None = None,
    endpoint_path: str | None = None,
    request_info: dict | None = None,
) -> Any:
    """
    Process API response - always returns FortiObject instances.

    Handles list responses (results array) and dict responses (full envelope).

    Args:
        result: Raw API response (list or dict)
        unwrap_single: If True and result is single-item list, return just the item
        raw_envelope: Optional full API envelope to attach to FortiObjectList
        response_time: Optional response time in seconds for the HTTP request
        endpoint_path: Optional endpoint path for content endpoint detection
        request_info: Optional HTTP request information (method, url, params, data)

    Returns:
        Processed response - FortiObject, FortiObjectList, ContentResponse, or dict with FortiObjects

    Examples:
        >>> # List response - returns FortiObjectList
        >>> result = [{"name": "policy1", "srcaddr": [{"name": "addr1"}]}]
        >>> objects = process_response(result)
        >>> objects[0].name
        'policy1'
        >>> objects[0].srcaddr  # Auto-flattened!
        ['addr1']
        >>> objects.raw  # Access full envelope
        {'http_status': 200, 'results': [...]}

        >>> # Single item with unwrap_single
        >>> result = [{"name": "policy1"}]
        >>> obj = process_response(result, unwrap_single=True)
        >>> obj.name
        'policy1'

        >>> # Dict response with 'results' key (full envelope)
        >>> result = {'results': [{"name": "policy1"}], 'http_status': 200}
        >>> response = process_response(result)
        >>> response['results'][0].name
        'policy1'
        >>> response['http_status']
        200
        
        >>> # Content response (file download)
        >>> result = {'content': b'data...', 'content_type': 'text/plain', 'http_status': 200}
        >>> response = process_response(result)
        >>> response.content
        b'data...'
        >>> response.text
        'data...'
    """
    # Wrap in FortiObject based on response type
    if isinstance(result, list):
        # Direct list of results
        # Only wrap dict items in FortiObject; pass through non-dicts (strings, ints, etc.)
        wrapped = [
            FortiObject(item, response_time=response_time, request_info=request_info) if isinstance(item, dict) else item
            for item in result
        ]

        # If unwrap_single=True and we have exactly 1 item, return just that item
        # This happens when querying by mkey (e.g., get(name="specific_object"))
        if unwrap_single and len(wrapped) == 1:
            return wrapped[0]

        # Return FortiObjectList with raw envelope for .raw property access
        return FortiObjectList(wrapped, raw_envelope=raw_envelope, response_time=response_time, request_info=request_info)
    
    elif isinstance(result, dict):
        # Check if this is a content response (file download endpoints)
        # Content responses have 'content' key without 'results' key
        if "content" in result and "results" not in result:
            return ContentResponse(result, raw_envelope=result, response_time=response_time, endpoint_path=endpoint_path, request_info=request_info)
        
        # Check if this is a full response envelope with 'results' key
        if "results" in result:
            results_data = result["results"]
            
            if isinstance(results_data, list):
                # List of results: wrap each in FortiObject
                wrapped_results = [
                    FortiObject(item, raw_envelope=result, response_time=response_time, request_info=request_info) if isinstance(item, dict) else item
                    for item in results_data
                ]

                # If unwrap_single=True and we have exactly 1 item, unwrap it
                if unwrap_single and len(wrapped_results) == 1:
                    return wrapped_results[0]

                # Return FortiObjectList with the full envelope as raw
                return FortiObjectList(wrapped_results, raw_envelope=result, response_time=response_time, request_info=request_info)
            
            elif isinstance(results_data, dict):
                # Singleton endpoint: results is a dict, not a list
                # Wrap just the results content, store envelope for .raw
                return FortiObject(results_data, raw_envelope=result, response_time=response_time, request_info=request_info)
            
            else:
                # results is some other type (string, int, etc.) - wrap envelope
                return FortiObject(result, raw_envelope=result, response_time=response_time, request_info=request_info)
        else:
            # Envelope-only response without 'results' key (e.g., DELETE, some POST/PUT)
            # Store envelope in raw_envelope, use empty dict for _data so object fields
            # don't collide with envelope fields like 'status'
            return FortiObject({}, raw_envelope=result, response_time=response_time, request_info=request_info)

    # Return as-is for any other type
    return result
