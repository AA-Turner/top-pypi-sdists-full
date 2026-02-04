"""Validation helpers for system/csf - Auto-generated"""

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
    "upstream-interface",  # Specify outgoing interface to reach server.
    "downstream-accprofile",  # Default access profile for requests from downstream devices.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "uid": "",
    "upstream": "",
    "source-ip": "0.0.0.0",
    "upstream-interface-select-method": "auto",
    "upstream-interface": "",
    "upstream-port": 8013,
    "group-name": "",
    "accept-auth-by-cert": "enable",
    "log-unification": "enable",
    "authorization-request-type": "serial",
    "certificate": "",
    "fabric-workers": 2,
    "downstream-access": "disable",
    "legacy-authentication": "disable",
    "downstream-accprofile": "",
    "configuration-sync": "default",
    "fabric-object-unification": "default",
    "saml-configuration-sync": "default",
    "forticloud-account-enforcement": "enable",
    "file-mgmt": "enable",
    "file-quota": 0,
    "file-quota-warning": 90,
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
    "status": "option",  # Enable/disable Security Fabric.
    "uid": "string",  # Unique ID of the current CSF node
    "upstream": "string",  # IP/FQDN of the FortiGate upstream from this FortiGate in the Security Fabric.
    "source-ip": "ipv4-address",  # Source IP address for communication with the upstream FortiGate.
    "upstream-interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "upstream-interface": "string",  # Specify outgoing interface to reach server.
    "upstream-port": "integer",  # The port number to use to communicate with the FortiGate upstream from this Fort
    "group-name": "string",  # Security Fabric group name. All FortiGates in a Security Fabric must have the sa
    "group-password": "password",  # Security Fabric group password. For legacy authentication, fabric members must h
    "accept-auth-by-cert": "option",  # Accept connections with unknown certificates and ask admin for approval.
    "log-unification": "option",  # Enable/disable broadcast of discovery messages for log unification.
    "authorization-request-type": "option",  # Authorization request type.
    "certificate": "string",  # Certificate.
    "fabric-workers": "integer",  # Number of worker processes for Security Fabric daemon.
    "downstream-access": "option",  # Enable/disable downstream device access to this device's configuration and data.
    "legacy-authentication": "option",  # Enable/disable legacy authentication.
    "downstream-accprofile": "string",  # Default access profile for requests from downstream devices.
    "configuration-sync": "option",  # Configuration sync mode.
    "fabric-object-unification": "option",  # Fabric CMDB Object Unification.
    "saml-configuration-sync": "option",  # SAML setting configuration synchronization.
    "trusted-list": "string",  # Pre-authorized and blocked security fabric nodes.
    "fabric-connector": "string",  # Fabric connector configuration.
    "forticloud-account-enforcement": "option",  # Fabric FortiCloud account unification.
    "file-mgmt": "option",  # Enable/disable Security Fabric daemon file management.
    "file-quota": "integer",  # Maximum amount of memory that can be used by the daemon files (in bytes).
    "file-quota-warning": "integer",  # Warn when the set percentage of quota has been used.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable Security Fabric.",
    "uid": "Unique ID of the current CSF node",
    "upstream": "IP/FQDN of the FortiGate upstream from this FortiGate in the Security Fabric.",
    "source-ip": "Source IP address for communication with the upstream FortiGate.",
    "upstream-interface-select-method": "Specify how to select outgoing interface to reach server.",
    "upstream-interface": "Specify outgoing interface to reach server.",
    "upstream-port": "The port number to use to communicate with the FortiGate upstream from this FortiGate in the Security Fabric (default = 8013).",
    "group-name": "Security Fabric group name. All FortiGates in a Security Fabric must have the same group name.",
    "group-password": "Security Fabric group password. For legacy authentication, fabric members must have the same group password.",
    "accept-auth-by-cert": "Accept connections with unknown certificates and ask admin for approval.",
    "log-unification": "Enable/disable broadcast of discovery messages for log unification.",
    "authorization-request-type": "Authorization request type.",
    "certificate": "Certificate.",
    "fabric-workers": "Number of worker processes for Security Fabric daemon.",
    "downstream-access": "Enable/disable downstream device access to this device's configuration and data.",
    "legacy-authentication": "Enable/disable legacy authentication.",
    "downstream-accprofile": "Default access profile for requests from downstream devices.",
    "configuration-sync": "Configuration sync mode.",
    "fabric-object-unification": "Fabric CMDB Object Unification.",
    "saml-configuration-sync": "SAML setting configuration synchronization.",
    "trusted-list": "Pre-authorized and blocked security fabric nodes.",
    "fabric-connector": "Fabric connector configuration.",
    "forticloud-account-enforcement": "Fabric FortiCloud account unification.",
    "file-mgmt": "Enable/disable Security Fabric daemon file management.",
    "file-quota": "Maximum amount of memory that can be used by the daemon files (in bytes).",
    "file-quota-warning": "Warn when the set percentage of quota has been used.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "uid": {"type": "string", "max_length": 35},
    "upstream": {"type": "string", "max_length": 255},
    "upstream-interface": {"type": "string", "max_length": 15},
    "upstream-port": {"type": "integer", "min": 1, "max": 65535},
    "group-name": {"type": "string", "max_length": 35},
    "certificate": {"type": "string", "max_length": 35},
    "fabric-workers": {"type": "integer", "min": 1, "max": 4},
    "downstream-accprofile": {"type": "string", "max_length": 35},
    "file-quota": {"type": "integer", "min": 0, "max": 4294967295},
    "file-quota-warning": {"type": "integer", "min": 1, "max": 99},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "trusted-list": {
        "name": {
            "type": "string",
            "help": "Name.",
            "default": "",
            "max_length": 35,
        },
        "authorization-type": {
            "type": "option",
            "help": "Authorization type.",
            "default": "serial",
            "options": ["serial", "certificate"],
        },
        "serial": {
            "type": "string",
            "help": "Serial.",
            "default": "",
            "max_length": 19,
        },
        "certificate": {
            "type": "var-string",
            "help": "Certificate.",
            "max_length": 32767,
        },
        "action": {
            "type": "option",
            "help": "Security fabric authorization action.",
            "default": "accept",
            "options": ["accept", "deny"],
        },
        "ha-members": {
            "type": "string",
            "help": "HA members.",
            "default": "",
            "max_length": 19,
        },
        "downstream-authorization": {
            "type": "option",
            "help": "Trust authorizations by this node's administrator.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "index": {
            "type": "integer",
            "help": "Index of the downstream in tree.",
            "default": 0,
            "min_value": 1,
            "max_value": 1024,
        },
    },
    "fabric-connector": {
        "serial": {
            "type": "string",
            "help": "Serial.",
            "default": "",
            "max_length": 19,
        },
        "accprofile": {
            "type": "string",
            "help": "Override access profile.",
            "default": "",
            "max_length": 35,
        },
        "configuration-write-access": {
            "type": "option",
            "help": "Enable/disable downstream device write access to configuration.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "vdom": {
            "type": "string",
            "help": "Virtual domains that the connector has access to. If none are set, the connector will only have access to the VDOM that it joins the Security Fabric through.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_UPSTREAM_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_ACCEPT_AUTH_BY_CERT = [
    "disable",
    "enable",
]
VALID_BODY_LOG_UNIFICATION = [
    "disable",
    "enable",
]
VALID_BODY_AUTHORIZATION_REQUEST_TYPE = [
    "serial",
    "certificate",
]
VALID_BODY_DOWNSTREAM_ACCESS = [
    "enable",
    "disable",
]
VALID_BODY_LEGACY_AUTHENTICATION = [
    "disable",
    "enable",
]
VALID_BODY_CONFIGURATION_SYNC = [
    "default",
    "local",
]
VALID_BODY_FABRIC_OBJECT_UNIFICATION = [
    "default",
    "local",
]
VALID_BODY_SAML_CONFIGURATION_SYNC = [
    "default",
    "local",
]
VALID_BODY_FORTICLOUD_ACCOUNT_ENFORCEMENT = [
    "enable",
    "disable",
]
VALID_BODY_FILE_MGMT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_csf_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/csf."""
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


def validate_system_csf_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/csf object."""
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
    if "upstream-interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "upstream-interface-select-method",
            payload["upstream-interface-select-method"],
            VALID_BODY_UPSTREAM_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "accept-auth-by-cert" in payload:
        is_valid, error = _validate_enum_field(
            "accept-auth-by-cert",
            payload["accept-auth-by-cert"],
            VALID_BODY_ACCEPT_AUTH_BY_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-unification" in payload:
        is_valid, error = _validate_enum_field(
            "log-unification",
            payload["log-unification"],
            VALID_BODY_LOG_UNIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authorization-request-type" in payload:
        is_valid, error = _validate_enum_field(
            "authorization-request-type",
            payload["authorization-request-type"],
            VALID_BODY_AUTHORIZATION_REQUEST_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "downstream-access" in payload:
        is_valid, error = _validate_enum_field(
            "downstream-access",
            payload["downstream-access"],
            VALID_BODY_DOWNSTREAM_ACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "legacy-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "legacy-authentication",
            payload["legacy-authentication"],
            VALID_BODY_LEGACY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "configuration-sync" in payload:
        is_valid, error = _validate_enum_field(
            "configuration-sync",
            payload["configuration-sync"],
            VALID_BODY_CONFIGURATION_SYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fabric-object-unification" in payload:
        is_valid, error = _validate_enum_field(
            "fabric-object-unification",
            payload["fabric-object-unification"],
            VALID_BODY_FABRIC_OBJECT_UNIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "saml-configuration-sync" in payload:
        is_valid, error = _validate_enum_field(
            "saml-configuration-sync",
            payload["saml-configuration-sync"],
            VALID_BODY_SAML_CONFIGURATION_SYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticloud-account-enforcement" in payload:
        is_valid, error = _validate_enum_field(
            "forticloud-account-enforcement",
            payload["forticloud-account-enforcement"],
            VALID_BODY_FORTICLOUD_ACCOUNT_ENFORCEMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-mgmt" in payload:
        is_valid, error = _validate_enum_field(
            "file-mgmt",
            payload["file-mgmt"],
            VALID_BODY_FILE_MGMT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_csf_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/csf."""
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
    if "upstream-interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "upstream-interface-select-method",
            payload["upstream-interface-select-method"],
            VALID_BODY_UPSTREAM_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "accept-auth-by-cert" in payload:
        is_valid, error = _validate_enum_field(
            "accept-auth-by-cert",
            payload["accept-auth-by-cert"],
            VALID_BODY_ACCEPT_AUTH_BY_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-unification" in payload:
        is_valid, error = _validate_enum_field(
            "log-unification",
            payload["log-unification"],
            VALID_BODY_LOG_UNIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authorization-request-type" in payload:
        is_valid, error = _validate_enum_field(
            "authorization-request-type",
            payload["authorization-request-type"],
            VALID_BODY_AUTHORIZATION_REQUEST_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "downstream-access" in payload:
        is_valid, error = _validate_enum_field(
            "downstream-access",
            payload["downstream-access"],
            VALID_BODY_DOWNSTREAM_ACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "legacy-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "legacy-authentication",
            payload["legacy-authentication"],
            VALID_BODY_LEGACY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "configuration-sync" in payload:
        is_valid, error = _validate_enum_field(
            "configuration-sync",
            payload["configuration-sync"],
            VALID_BODY_CONFIGURATION_SYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fabric-object-unification" in payload:
        is_valid, error = _validate_enum_field(
            "fabric-object-unification",
            payload["fabric-object-unification"],
            VALID_BODY_FABRIC_OBJECT_UNIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "saml-configuration-sync" in payload:
        is_valid, error = _validate_enum_field(
            "saml-configuration-sync",
            payload["saml-configuration-sync"],
            VALID_BODY_SAML_CONFIGURATION_SYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticloud-account-enforcement" in payload:
        is_valid, error = _validate_enum_field(
            "forticloud-account-enforcement",
            payload["forticloud-account-enforcement"],
            VALID_BODY_FORTICLOUD_ACCOUNT_ENFORCEMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-mgmt" in payload:
        is_valid, error = _validate_enum_field(
            "file-mgmt",
            payload["file-mgmt"],
            VALID_BODY_FILE_MGMT,
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
    "endpoint": "system/csf",
    "category": "cmdb",
    "api_path": "system/csf",
    "help": "Add this FortiGate to a Security Fabric or set up a new Security Fabric on this FortiGate.",
    "total_fields": 26,
    "required_fields_count": 2,
    "fields_with_defaults_count": 23,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
