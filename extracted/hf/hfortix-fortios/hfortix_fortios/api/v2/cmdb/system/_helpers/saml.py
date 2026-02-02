"""Validation helpers for system/saml - Auto-generated"""

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
    "default-profile",  # Default profile for new SSO admin.
    "entity-id",  # SP entity ID.
    "idp-cert",  # IDP certificate name.
    "server-address",  # Server address.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "status": "disable",
    "role": "service-provider",
    "default-login-page": "normal",
    "default-profile": "",
    "cert": "",
    "binding-protocol": "redirect",
    "portal-url": "",
    "entity-id": "",
    "single-sign-on-url": "",
    "single-logout-url": "",
    "idp-entity-id": "",
    "idp-single-sign-on-url": "",
    "idp-single-logout-url": "",
    "idp-cert": "",
    "server-address": "",
    "require-signed-resp-and-asrt": "disable",
    "tolerance": 5,
    "life": 30,
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
    "status": "option",  # Enable/disable SAML authentication (default = disable).
    "role": "option",  # SAML role.
    "default-login-page": "option",  # Choose default login page.
    "default-profile": "string",  # Default profile for new SSO admin.
    "cert": "string",  # Certificate to sign SAML messages.
    "binding-protocol": "option",  # IdP Binding protocol.
    "portal-url": "string",  # SP portal URL.
    "entity-id": "string",  # SP entity ID.
    "single-sign-on-url": "string",  # SP single sign-on URL.
    "single-logout-url": "string",  # SP single logout URL.
    "idp-entity-id": "string",  # IDP entity ID.
    "idp-single-sign-on-url": "string",  # IDP single sign-on URL.
    "idp-single-logout-url": "string",  # IDP single logout URL.
    "idp-cert": "string",  # IDP certificate name.
    "server-address": "string",  # Server address.
    "require-signed-resp-and-asrt": "option",  # Require both response and assertion from IDP to be signed wh
    "tolerance": "integer",  # Tolerance to the range of time when the assertion is valid (
    "life": "integer",  # Length of the range of time when the assertion is valid (in 
    "service-providers": "string",  # Authorized service providers.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable SAML authentication (default = disable).",
    "role": "SAML role.",
    "default-login-page": "Choose default login page.",
    "default-profile": "Default profile for new SSO admin.",
    "cert": "Certificate to sign SAML messages.",
    "binding-protocol": "IdP Binding protocol.",
    "portal-url": "SP portal URL.",
    "entity-id": "SP entity ID.",
    "single-sign-on-url": "SP single sign-on URL.",
    "single-logout-url": "SP single logout URL.",
    "idp-entity-id": "IDP entity ID.",
    "idp-single-sign-on-url": "IDP single sign-on URL.",
    "idp-single-logout-url": "IDP single logout URL.",
    "idp-cert": "IDP certificate name.",
    "server-address": "Server address.",
    "require-signed-resp-and-asrt": "Require both response and assertion from IDP to be signed when FGT acts as SP (default = disable).",
    "tolerance": "Tolerance to the range of time when the assertion is valid (in minutes).",
    "life": "Length of the range of time when the assertion is valid (in minutes).",
    "service-providers": "Authorized service providers.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "default-profile": {"type": "string", "max_length": 35},
    "cert": {"type": "string", "max_length": 35},
    "portal-url": {"type": "string", "max_length": 255},
    "entity-id": {"type": "string", "max_length": 255},
    "single-sign-on-url": {"type": "string", "max_length": 255},
    "single-logout-url": {"type": "string", "max_length": 255},
    "idp-entity-id": {"type": "string", "max_length": 255},
    "idp-single-sign-on-url": {"type": "string", "max_length": 255},
    "idp-single-logout-url": {"type": "string", "max_length": 255},
    "idp-cert": {"type": "string", "max_length": 35},
    "server-address": {"type": "string", "max_length": 63},
    "tolerance": {"type": "integer", "min": 0, "max": 4294967295},
    "life": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "service-providers": {
        "name": {
            "type": "string",
            "help": "Name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "prefix": {
            "type": "string",
            "help": "Prefix.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "sp-binding-protocol": {
            "type": "option",
            "help": "SP binding protocol.",
            "default": "post",
            "options": ["post", "redirect"],
        },
        "sp-cert": {
            "type": "string",
            "help": "SP certificate name.",
            "default": "",
            "max_length": 35,
        },
        "sp-entity-id": {
            "type": "string",
            "help": "SP entity ID.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
        "sp-single-sign-on-url": {
            "type": "string",
            "help": "SP single sign-on URL.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
        "sp-single-logout-url": {
            "type": "string",
            "help": "SP single logout URL.",
            "default": "",
            "max_length": 255,
        },
        "sp-portal-url": {
            "type": "string",
            "help": "SP portal URL.",
            "default": "",
            "max_length": 255,
        },
        "idp-entity-id": {
            "type": "string",
            "help": "IDP entity ID.",
            "default": "",
            "max_length": 255,
        },
        "idp-single-sign-on-url": {
            "type": "string",
            "help": "IDP single sign-on URL.",
            "default": "",
            "max_length": 255,
        },
        "idp-single-logout-url": {
            "type": "string",
            "help": "IDP single logout URL.",
            "default": "",
            "max_length": 255,
        },
        "assertion-attributes": {
            "type": "string",
            "help": "Customized SAML attributes to send along with assertion.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_ROLE = [
    "identity-provider",
    "service-provider",
]
VALID_BODY_DEFAULT_LOGIN_PAGE = [
    "normal",
    "sso",
]
VALID_BODY_BINDING_PROTOCOL = [
    "post",
    "redirect",
]
VALID_BODY_REQUIRE_SIGNED_RESP_AND_ASRT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_saml_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/saml."""
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


def validate_system_saml_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/saml object."""
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
    if "role" in payload:
        is_valid, error = _validate_enum_field(
            "role",
            payload["role"],
            VALID_BODY_ROLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-login-page" in payload:
        is_valid, error = _validate_enum_field(
            "default-login-page",
            payload["default-login-page"],
            VALID_BODY_DEFAULT_LOGIN_PAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "binding-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "binding-protocol",
            payload["binding-protocol"],
            VALID_BODY_BINDING_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "require-signed-resp-and-asrt" in payload:
        is_valid, error = _validate_enum_field(
            "require-signed-resp-and-asrt",
            payload["require-signed-resp-and-asrt"],
            VALID_BODY_REQUIRE_SIGNED_RESP_AND_ASRT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_saml_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/saml."""
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
    if "role" in payload:
        is_valid, error = _validate_enum_field(
            "role",
            payload["role"],
            VALID_BODY_ROLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-login-page" in payload:
        is_valid, error = _validate_enum_field(
            "default-login-page",
            payload["default-login-page"],
            VALID_BODY_DEFAULT_LOGIN_PAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "binding-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "binding-protocol",
            payload["binding-protocol"],
            VALID_BODY_BINDING_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "require-signed-resp-and-asrt" in payload:
        is_valid, error = _validate_enum_field(
            "require-signed-resp-and-asrt",
            payload["require-signed-resp-and-asrt"],
            VALID_BODY_REQUIRE_SIGNED_RESP_AND_ASRT,
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
    "endpoint": "system/saml",
    "category": "cmdb",
    "api_path": "system/saml",
    "help": "Global settings for SAML authentication.",
    "total_fields": 19,
    "required_fields_count": 4,
    "fields_with_defaults_count": 18,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
