"""
Payload building helpers for FortiOS API.

Converts Python-style parameters to FortiOS API payloads with:
- snake_case to kebab-case conversion for body fields
- Python keyword conflict resolution (asn -> as, etc.)
- Context-specific underscore preservation (query params vs body fields)
- Optional list normalization
- None value filtering

Architecture (v0.5.128):
  - CMDB endpoints: Use CMDB_BODY_FIELD_NO_HYPHEN for body fields
  - Monitor/Service endpoints: Use MONITOR_BODY_FIELD_NO_HYPHEN for body fields
  - Query/path parameters: Handled separately (not in these builders)
  - Body fields: Default to kebab-case conversion unless in *_BODY_FIELD_NO_HYPHEN
"""

from typing import Any, Literal

from hfortix_fortios._helpers.normalizers import (
    normalize_to_name_list,
    normalize_to_string_list,
)
from hfortix_fortios._helpers.field_overrides import (
    CMDB_BODY_FIELD_NO_HYPHEN,
    MONITOR_BODY_FIELD_NO_HYPHEN,
    LOG_BODY_FIELD_NO_HYPHEN,
    PYTHON_KEYWORD_TO_API_FIELD,
)


def build_cmdb_payload(**params: Any) -> dict[str, Any]:
    """
    Build a CMDB payload dictionary from keyword arguments (API layer - no normalization).

    Converts Python snake_case parameter names to FortiOS kebab-case API keys
    and filters out None values. This is the base helper used by all CMDB API endpoints.

    Does NOT normalize list fields - caller is responsible for providing data
    in the correct FortiOS format (unless using a wrapper with normalization).

    Args:
        **params: All resource parameters (e.g., name=..., member=..., etc.)

    Returns:
        Dictionary with FortiOS API-compatible keys and non-None values
    """
    # Use build_api_payload with cmdb context for proper underscore handling
    return build_api_payload(auto_normalize=False, api_type="cmdb", **params)


def build_cmdb_payload_normalized(
    normalize_fields: set[str] | None = None, **params: Any
) -> dict[str, Any]:
    """
    Build a CMDB payload with automatic normalization (convenience wrapper layer).

    Converts Python snake_case parameter names to FortiOS kebab-case API keys,
    filters out None values, AND normalizes specified list fields to FortiOS format.

    This is used by convenience wrappers to accept flexible inputs like strings
    or lists and automatically convert them to FortiOS [{'name': '...'}] format.

    Args:
        normalize_fields: Set of field names (snake_case) that should be normalized
                         to [{'name': '...'}] format. If None, common fields like
                         'member', 'interface', 'allowaccess' are normalized.
        **params: All resource parameters

    Returns:
        Dictionary with FortiOS API-compatible keys and normalized values
    """
    # Default fields that commonly need normalization across CMDB endpoints
    DEFAULT_NORMALIZE_FIELDS = {
        "member",  # address groups, service groups, user groups
        "interface",  # various config objects
        "allowaccess",  # system interfaces
        "srcintf",  # firewall policies, routes
        "dstintf",  # firewall policies, routes
        "srcaddr",  # firewall policies
        "dstaddr",  # firewall policies
        "service",  # firewall policies
        "users",  # various auth/policy objects
        "groups",  # various auth/policy objects
    }

    # Use provided fields or defaults
    fields_to_normalize = (
        normalize_fields
        if normalize_fields is not None
        else DEFAULT_NORMALIZE_FIELDS
    )

    payload: dict[str, Any] = {}

    # Extract 'data' parameter if present
    # It should be merged, not added as a key
    data_dict = params.pop("data", None)

    for param_name, value in params.items():
        if value is None:
            continue

        # First, check if this is a Python keyword that needs reverse mapping
        if param_name in PYTHON_KEYWORD_TO_API_FIELD:
            api_key = PYTHON_KEYWORD_TO_API_FIELD[param_name]
        # Check if this BODY field should keep underscores (extremely rare!)
        elif param_name in CMDB_BODY_FIELD_NO_HYPHEN:
            api_key = param_name
        else:
            # Convert snake_case to kebab-case for FortiOS API
            api_key = param_name.replace("_", "-")

        # Normalize list parameters to FortiOS format if specified
        if param_name in fields_to_normalize:
            normalized = normalize_to_name_list(value)
            # Only add if normalization resulted in non-empty list
            if normalized:
                payload[api_key] = normalized
        else:
            payload[api_key] = value

    # Merge 'data' dictionary into payload (override existing keys)
    if data_dict and isinstance(data_dict, dict):
        payload.update(data_dict)

    return payload


def build_api_payload(
    normalize_fields: set[str] | None = None,
    normalize_array_fields: set[str] | None = None,
    auto_normalize: bool = True,
    api_type: Literal["cmdb", "monitor", "log", "service"] | None = None,
    **params: Any,
) -> dict[str, Any]:
    """
    Build a generic API payload with intelligent list normalization.

    Universal helper for all API types (cmdb, monitor, log, service).
    Automatically normalizes common list fields that use [{'name': '...'}] format
    and simple array fields that use plain list format.

    Args:
        normalize_fields: Explicit set of field names (snake_case) to normalize
                         to [{'name': '...'}] format. If provided, only these
                         fields are normalized this way.
        normalize_array_fields: Set of field names (snake_case) to normalize
                               to simple list[str] format. Used for fields like
                               'id_list' that accept flexible input (int/str/list).
        auto_normalize: If True and normalize_fields is None, auto-detect and
                       normalize common list fields. Set False for raw passthrough.
        api_type: Specifies which API type this payload is for ('cmdb', 'monitor',
                 'log', or 'service'). Used for context-specific underscore 
                 preservation. If None, checks all NO_HYPHEN sets (legacy behavior).
        **params: All resource parameters

    Returns:
        Dictionary with FortiOS API-compatible keys and normalized values
    """
    # Common list fields across all API types that use [{'name': '...'}] format
    COMMON_LIST_FIELDS = {
        # Firewall policy fields
        "srcintf",
        "dstintf",
        "srcaddr",
        "dstaddr",
        "srcaddr6",
        "dstaddr6",
        "service",
        "poolname",
        "poolname6",
        "groups",
        "users",
        "fsso_groups",
        "ztna_ems_tag",
        "ztna_ems_tag_secondary",
        "ztna_geo_tag",
        "internet_service_name",
        "internet_service_group",
        "internet_service_custom",
        "internet_service_custom_group",
        "network_service_dynamic",
        "internet_service_src_name",
        "internet_service_src_group",
        "internet_service_src_custom",
        "internet_service_src_custom_group",
        "network_service_src_dynamic",
        "internet_service6_name",
        "internet_service6_group",
        "internet_service6_custom",
        "internet_service6_custom_group",
        "internet_service6_src_name",
        "internet_service6_src_group",
        "internet_service6_src_custom",
        "internet_service6_src_custom_group",
        "src_vendor_mac",
        "rtp_addr",
        "ntlm_enabled_browsers",
        "custom_log_fields",
        "pcp_poolname",
        "sgt",
        "internet_service_fortiguard",
        "internet_service_src_fortiguard",
        "internet_service6_fortiguard",
        "internet_service6_src_fortiguard",
        # Group membership
        "member",
        # System/interface fields
        "interface",
        "allowaccess",
        "device",
        # Router fields
        "gateway",
        "nexthop",
        # VPN fields
        "destination",
        "source",
        # Application fields
        "application",
        "category",
        # User fields
        "group",
        "user",
        # Certificate fields
        "ca",
        "certificate",
        # DNS fields
        "dns_server",
    }

    # Common simple array fields that use plain list format (not [{'name': '...'}])
    COMMON_ARRAY_FIELDS = {
        "id_list",  # monitor.system.config-script.delete
        # Add more as discovered
    }

    # Determine which fields to normalize
    if normalize_fields is not None:
        # Explicit field list provided
        fields_to_normalize = normalize_fields
    elif auto_normalize:
        # Auto-detect common fields
        fields_to_normalize = COMMON_LIST_FIELDS
    else:
        # No normalization
        fields_to_normalize = set()

    # Determine which array fields to normalize
    if normalize_array_fields is not None:
        # Explicit array field list provided
        array_fields_to_normalize = normalize_array_fields
    elif auto_normalize:
        # Auto-detect common array fields
        array_fields_to_normalize = COMMON_ARRAY_FIELDS
    else:
        # No array normalization
        array_fields_to_normalize = set()

    payload: dict[str, Any] = {}

    # Extract 'data' parameter if present
    data_dict = params.pop("data", None)

    for param_name, value in params.items():
        if value is None:
            continue

        # First, check if this is a Python keyword that needs reverse mapping
        if param_name in PYTHON_KEYWORD_TO_API_FIELD:
            api_key = PYTHON_KEYWORD_TO_API_FIELD[param_name]
        # Context-aware underscore preservation based on API type
        elif api_type == "cmdb" and param_name in CMDB_BODY_FIELD_NO_HYPHEN:
            api_key = param_name
        elif api_type == "monitor" and param_name in MONITOR_BODY_FIELD_NO_HYPHEN:
            api_key = param_name
        elif api_type == "log" and param_name in LOG_BODY_FIELD_NO_HYPHEN:
            api_key = param_name
        # Legacy behavior: Check all NO_HYPHEN sets if api_type not specified
        elif api_type is None:
            if param_name in CMDB_BODY_FIELD_NO_HYPHEN:
                api_key = param_name
            elif param_name in MONITOR_BODY_FIELD_NO_HYPHEN:
                api_key = param_name
            elif param_name in LOG_BODY_FIELD_NO_HYPHEN:
                api_key = param_name
            else:
                # Convert snake_case to kebab-case for FortiOS API
                api_key = param_name.replace("_", "-")
        else:
            # Convert snake_case to kebab-case for FortiOS API
            api_key = param_name.replace("_", "-")

        # Normalize simple array parameters (e.g., id_list)
        if param_name in array_fields_to_normalize:
            normalized = normalize_to_string_list(value)
            # Only add if normalization resulted in non-empty/non-None list
            if normalized:
                payload[api_key] = normalized
        # Normalize list parameters to [{'name': '...'}] format
        elif param_name in fields_to_normalize:
            normalized = normalize_to_name_list(value)
            # Only add if normalization resulted in non-empty list
            if normalized:
                payload[api_key] = normalized
        else:
            payload[api_key] = value

    # Merge 'data' dictionary into payload (override existing keys)
    if data_dict and isinstance(data_dict, dict):
        payload.update(data_dict)

    return payload
