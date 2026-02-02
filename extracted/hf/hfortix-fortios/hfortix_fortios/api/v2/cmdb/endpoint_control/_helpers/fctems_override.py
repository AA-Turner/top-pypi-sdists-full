"""Validation helpers for endpoint_control/fctems_override - Auto-generated"""

from typing import Any, TypedDict, Literal
from typing_extensions import NotRequired

# Import common validators from central _helpers module
from hfortix_fortios._helpers import (
    validate_enable_disable,
    validate_integer_range,
    validate_string_length,
    validate_port_number,
    validate_ip_address,
    validate_ipv6_address,
    validate_mac_address,
)

# Import central validation functions (avoid duplication across 1,062 files)
from hfortix_fortios._helpers.validation import (
    validate_required_fields as _validate_required_fields,
    validate_enum_field as _validate_enum_field,
    validate_query_parameter as _validate_query_parameter,
)

# ============================================================================
# Required Fields Validation
# Auto-generated from schema
# ============================================================================

# ⚠️  IMPORTANT: FortiOS schemas have known issues with required field marking:

# Do NOT use this list for strict validation - test with the actual FortiOS API!

# Fields marked as required (after filtering false positives)
REQUIRED_FIELDS = [
    "interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "ems-id": 0,
    "status": "disable",
    "name": "",
    "dirty-reason": "none",
    "fortinetone-cloud-authentication": "disable",
    "server": "",
    "https-port": 443,
    "serial-number": "",
    "tenant-id": "",
    "source-ip": "0.0.0.0",
    "pull-sysinfo": "enable",
    "pull-vulnerabilities": "enable",
    "pull-tags": "enable",
    "pull-malware-hash": "enable",
    "capabilities": "",
    "call-timeout": 30,
    "out-of-sync-threshold": 180,
    "send-tags-to-all-vdoms": "disable",
    "websocket-override": "disable",
    "interface-select-method": "auto",
    "interface": "",
    "trust-ca-cn": "enable",
    "verifying-ca": "",
}

# ============================================================================
# Deprecated Fields
# Auto-generated from schema - warns users about deprecated fields
# ============================================================================

# Deprecated fields with migration guidance
DEPRECATED_FIELDS = {
}

# ============================================================================
# Field Metadata (Type Information & Descriptions)
# Auto-generated from schema - use for IDE autocomplete and documentation
# ============================================================================

# Field types mapping
FIELD_TYPES = {
    "ems-id": "integer",  # EMS ID in order (1 - 7).
    "status": "option",  # Enable or disable this EMS configuration.
    "name": "string",  # FortiClient Enterprise Management Server (EMS) name.
    "dirty-reason": "option",  # Dirty Reason for FortiClient EMS.
    "fortinetone-cloud-authentication": "option",  # Enable/disable authentication of FortiClient EMS Cloud throu
    "cloud-authentication-access-key": "password",  # FortiClient EMS Cloud multitenancy access key
    "server": "string",  # FortiClient EMS FQDN or IPv4 address.
    "https-port": "integer",  # FortiClient EMS HTTPS access port number. (1 - 65535, defaul
    "serial-number": "string",  # EMS Serial Number.
    "tenant-id": "string",  # EMS Tenant ID.
    "source-ip": "ipv4-address-any",  # REST API call source IP.
    "pull-sysinfo": "option",  # Enable/disable pulling SysInfo from EMS.
    "pull-vulnerabilities": "option",  # Enable/disable pulling vulnerabilities from EMS.
    "pull-tags": "option",  # Enable/disable pulling FortiClient user tags from EMS.
    "pull-malware-hash": "option",  # Enable/disable pulling FortiClient malware hash from EMS.
    "capabilities": "option",  # List of EMS capabilities.
    "call-timeout": "integer",  # FortiClient EMS call timeout in seconds (1 - 180 seconds, de
    "out-of-sync-threshold": "integer",  # Outdated resource threshold in seconds (10 - 3600, default =
    "send-tags-to-all-vdoms": "option",  # Relax restrictions on tags to send all EMS tags to all VDOMs
    "websocket-override": "option",  # Enable/disable override behavior for how this FortiGate unit
    "interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "interface": "string",  # Specify outgoing interface to reach server.
    "trust-ca-cn": "option",  # Enable/disable trust of the EMS certificate issuer(CA) and c
    "verifying-ca": "string",  # Lowest CA cert on Fortigate in verified EMS cert chain.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "ems-id": "EMS ID in order (1 - 7).",
    "status": "Enable or disable this EMS configuration.",
    "name": "FortiClient Enterprise Management Server (EMS) name.",
    "dirty-reason": "Dirty Reason for FortiClient EMS.",
    "fortinetone-cloud-authentication": "Enable/disable authentication of FortiClient EMS Cloud through FortiCloud account.",
    "cloud-authentication-access-key": "FortiClient EMS Cloud multitenancy access key",
    "server": "FortiClient EMS FQDN or IPv4 address.",
    "https-port": "FortiClient EMS HTTPS access port number. (1 - 65535, default: 443).",
    "serial-number": "EMS Serial Number.",
    "tenant-id": "EMS Tenant ID.",
    "source-ip": "REST API call source IP.",
    "pull-sysinfo": "Enable/disable pulling SysInfo from EMS.",
    "pull-vulnerabilities": "Enable/disable pulling vulnerabilities from EMS.",
    "pull-tags": "Enable/disable pulling FortiClient user tags from EMS.",
    "pull-malware-hash": "Enable/disable pulling FortiClient malware hash from EMS.",
    "capabilities": "List of EMS capabilities.",
    "call-timeout": "FortiClient EMS call timeout in seconds (1 - 180 seconds, default = 30).",
    "out-of-sync-threshold": "Outdated resource threshold in seconds (10 - 3600, default = 180).",
    "send-tags-to-all-vdoms": "Relax restrictions on tags to send all EMS tags to all VDOMs",
    "websocket-override": "Enable/disable override behavior for how this FortiGate unit connects to EMS using a WebSocket connection.",
    "interface-select-method": "Specify how to select outgoing interface to reach server.",
    "interface": "Specify outgoing interface to reach server.",
    "trust-ca-cn": "Enable/disable trust of the EMS certificate issuer(CA) and common name(CN) for certificate auto-renewal.",
    "verifying-ca": "Lowest CA cert on Fortigate in verified EMS cert chain.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "ems-id": {"type": "integer", "min": 1, "max": 7},
    "name": {"type": "string", "max_length": 35},
    "server": {"type": "string", "max_length": 255},
    "https-port": {"type": "integer", "min": 1, "max": 65535},
    "serial-number": {"type": "string", "max_length": 16},
    "tenant-id": {"type": "string", "max_length": 32},
    "call-timeout": {"type": "integer", "min": 1, "max": 180},
    "out-of-sync-threshold": {"type": "integer", "min": 10, "max": 3600},
    "interface": {"type": "string", "max_length": 15},
    "verifying-ca": {"type": "string", "max_length": 79},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_DIRTY_REASON = [
    "none",
    "mismatched-ems-sn",
]
VALID_BODY_FORTINETONE_CLOUD_AUTHENTICATION = [
    "enable",
    "disable",
]
VALID_BODY_PULL_SYSINFO = [
    "enable",
    "disable",
]
VALID_BODY_PULL_VULNERABILITIES = [
    "enable",
    "disable",
]
VALID_BODY_PULL_TAGS = [
    "enable",
    "disable",
]
VALID_BODY_PULL_MALWARE_HASH = [
    "enable",
    "disable",
]
VALID_BODY_CAPABILITIES = [
    "fabric-auth",
    "silent-approval",
    "websocket",
    "websocket-malware",
    "push-ca-certs",
    "common-tags-api",
    "tenant-id",
    "client-avatars",
    "single-vdom-connector",
    "fgt-sysinfo-api",
    "ztna-server-info",
    "used-tags",
]
VALID_BODY_SEND_TAGS_TO_ALL_VDOMS = [
    "enable",
    "disable",
]
VALID_BODY_WEBSOCKET_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_TRUST_CA_CN = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_endpoint_control_fctems_override_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for endpoint_control/fctems_override."""
    # Validate query parameters using central function
    if "action" in params:
        is_valid, error = _validate_query_parameter(
            "action",
            params.get("action"),
            VALID_QUERY_ACTION
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# POST Validation
# ============================================================================


def validate_endpoint_control_fctems_override_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new endpoint_control/fctems_override object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dirty-reason" in payload:
        is_valid, error = _validate_enum_field(
            "dirty-reason",
            payload["dirty-reason"],
            VALID_BODY_DIRTY_REASON,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortinetone-cloud-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "fortinetone-cloud-authentication",
            payload["fortinetone-cloud-authentication"],
            VALID_BODY_FORTINETONE_CLOUD_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-sysinfo" in payload:
        is_valid, error = _validate_enum_field(
            "pull-sysinfo",
            payload["pull-sysinfo"],
            VALID_BODY_PULL_SYSINFO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-vulnerabilities" in payload:
        is_valid, error = _validate_enum_field(
            "pull-vulnerabilities",
            payload["pull-vulnerabilities"],
            VALID_BODY_PULL_VULNERABILITIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-tags" in payload:
        is_valid, error = _validate_enum_field(
            "pull-tags",
            payload["pull-tags"],
            VALID_BODY_PULL_TAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-malware-hash" in payload:
        is_valid, error = _validate_enum_field(
            "pull-malware-hash",
            payload["pull-malware-hash"],
            VALID_BODY_PULL_MALWARE_HASH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "capabilities" in payload:
        is_valid, error = _validate_enum_field(
            "capabilities",
            payload["capabilities"],
            VALID_BODY_CAPABILITIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-tags-to-all-vdoms" in payload:
        is_valid, error = _validate_enum_field(
            "send-tags-to-all-vdoms",
            payload["send-tags-to-all-vdoms"],
            VALID_BODY_SEND_TAGS_TO_ALL_VDOMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "websocket-override" in payload:
        is_valid, error = _validate_enum_field(
            "websocket-override",
            payload["websocket-override"],
            VALID_BODY_WEBSOCKET_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trust-ca-cn" in payload:
        is_valid, error = _validate_enum_field(
            "trust-ca-cn",
            payload["trust-ca-cn"],
            VALID_BODY_TRUST_CA_CN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_endpoint_control_fctems_override_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update endpoint_control/fctems_override."""
    # Validate enum values using central function
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dirty-reason" in payload:
        is_valid, error = _validate_enum_field(
            "dirty-reason",
            payload["dirty-reason"],
            VALID_BODY_DIRTY_REASON,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortinetone-cloud-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "fortinetone-cloud-authentication",
            payload["fortinetone-cloud-authentication"],
            VALID_BODY_FORTINETONE_CLOUD_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-sysinfo" in payload:
        is_valid, error = _validate_enum_field(
            "pull-sysinfo",
            payload["pull-sysinfo"],
            VALID_BODY_PULL_SYSINFO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-vulnerabilities" in payload:
        is_valid, error = _validate_enum_field(
            "pull-vulnerabilities",
            payload["pull-vulnerabilities"],
            VALID_BODY_PULL_VULNERABILITIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-tags" in payload:
        is_valid, error = _validate_enum_field(
            "pull-tags",
            payload["pull-tags"],
            VALID_BODY_PULL_TAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pull-malware-hash" in payload:
        is_valid, error = _validate_enum_field(
            "pull-malware-hash",
            payload["pull-malware-hash"],
            VALID_BODY_PULL_MALWARE_HASH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "capabilities" in payload:
        is_valid, error = _validate_enum_field(
            "capabilities",
            payload["capabilities"],
            VALID_BODY_CAPABILITIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-tags-to-all-vdoms" in payload:
        is_valid, error = _validate_enum_field(
            "send-tags-to-all-vdoms",
            payload["send-tags-to-all-vdoms"],
            VALID_BODY_SEND_TAGS_TO_ALL_VDOMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "websocket-override" in payload:
        is_valid, error = _validate_enum_field(
            "websocket-override",
            payload["websocket-override"],
            VALID_BODY_WEBSOCKET_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "interface-select-method",
            payload["interface-select-method"],
            VALID_BODY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "trust-ca-cn" in payload:
        is_valid, error = _validate_enum_field(
            "trust-ca-cn",
            payload["trust-ca-cn"],
            VALID_BODY_TRUST_CA_CN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# Metadata Access Functions
# Imported from central module to avoid duplication across 1,062 files
# Bound to this endpoint's data using functools.partial (saves ~7KB per file)
# ============================================================================

from functools import partial
from hfortix_fortios._helpers.metadata import (
    get_field_description,
    get_field_type,
    get_field_constraints,
    get_field_default,
    get_field_options,
    get_nested_schema,
    get_all_fields,
    get_field_metadata,
    validate_field_value,
)

# Bind module-specific data to central functions using partial application
get_field_description = partial(get_field_description, FIELD_DESCRIPTIONS)
get_field_type = partial(get_field_type, FIELD_TYPES)
get_field_constraints = partial(get_field_constraints, FIELD_CONSTRAINTS)
get_field_default = partial(get_field_default, FIELDS_WITH_DEFAULTS)
get_field_options = partial(get_field_options, globals())
get_nested_schema = partial(get_nested_schema, NESTED_SCHEMAS)
get_all_fields = partial(get_all_fields, FIELD_TYPES)
get_field_metadata = partial(get_field_metadata, FIELD_TYPES, FIELD_DESCRIPTIONS, 
                             FIELD_CONSTRAINTS, FIELDS_WITH_DEFAULTS, REQUIRED_FIELDS,
                             NESTED_SCHEMAS, globals())
validate_field_value = partial(validate_field_value, FIELD_TYPES, FIELD_DESCRIPTIONS,
                               FIELD_CONSTRAINTS, globals())


# ============================================================================
# Schema Information
# Metadata about this endpoint schema
# ============================================================================

SCHEMA_INFO = {
    "endpoint": "endpoint_control/fctems_override",
    "category": "cmdb",
    "api_path": "endpoint-control/fctems-override",
    "mkey": "ems-id",
    "mkey_type": "integer",
    "help": "Configure FortiClient Enterprise Management Server (EMS) entries.",
    "total_fields": 24,
    "required_fields_count": 1,
    "fields_with_defaults_count": 23,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
