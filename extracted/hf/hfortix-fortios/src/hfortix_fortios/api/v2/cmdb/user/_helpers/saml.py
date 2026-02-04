"""Validation helpers for user/saml - Auto-generated"""

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
    "entity-id",  # SP entity ID.
    "single-sign-on-url",  # SP single sign-on URL.
    "idp-entity-id",  # IDP entity ID.
    "idp-single-sign-on-url",  # IDP single sign-on URL.
    "idp-cert",  # IDP Certificate name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "cert": "",
    "entity-id": "",
    "single-sign-on-url": "",
    "single-logout-url": "",
    "idp-entity-id": "",
    "idp-single-sign-on-url": "",
    "idp-single-logout-url": "",
    "idp-cert": "",
    "scim-client": "",
    "scim-user-attr-type": "user-name",
    "scim-group-attr-type": "display-name",
    "user-name": "",
    "group-name": "",
    "digest-method": "sha1",
    "require-signed-resp-and-asrt": "disable",
    "limit-relaystate": "disable",
    "clock-tolerance": 15,
    "adfs-claim": "disable",
    "user-claim-type": "upn",
    "group-claim-type": "group",
    "reauth": "disable",
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
    "name": "string",  # SAML server entry name.
    "cert": "string",  # Certificate to sign SAML messages.
    "entity-id": "string",  # SP entity ID.
    "single-sign-on-url": "string",  # SP single sign-on URL.
    "single-logout-url": "string",  # SP single logout URL.
    "idp-entity-id": "string",  # IDP entity ID.
    "idp-single-sign-on-url": "string",  # IDP single sign-on URL.
    "idp-single-logout-url": "string",  # IDP single logout url.
    "idp-cert": "string",  # IDP Certificate name.
    "scim-client": "string",  # SCIM client name.
    "scim-user-attr-type": "option",  # User attribute type used to match SCIM users (default = user-name).
    "scim-group-attr-type": "option",  # Group attribute type used to match SCIM groups (default = display-name).
    "user-name": "string",  # User name in assertion statement.
    "group-name": "string",  # Group name in assertion statement.
    "digest-method": "option",  # Digest method algorithm.
    "require-signed-resp-and-asrt": "option",  # Require both response and assertion from IDP to be signed when FGT acts as SP (d
    "limit-relaystate": "option",  # Enable/disable limiting of relay-state parameter when it exceeds SAML 2.0 specif
    "clock-tolerance": "integer",  # Clock skew tolerance in seconds (0 - 300, default = 15, 0 = no tolerance).
    "adfs-claim": "option",  # Enable/disable ADFS Claim for user/group attribute in assertion statement (defau
    "user-claim-type": "option",  # User name claim in assertion statement.
    "group-claim-type": "option",  # Group claim in assertion statement.
    "reauth": "option",  # Enable/disable signalling of IDP to force user re-authentication (default = disa
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "SAML server entry name.",
    "cert": "Certificate to sign SAML messages.",
    "entity-id": "SP entity ID.",
    "single-sign-on-url": "SP single sign-on URL.",
    "single-logout-url": "SP single logout URL.",
    "idp-entity-id": "IDP entity ID.",
    "idp-single-sign-on-url": "IDP single sign-on URL.",
    "idp-single-logout-url": "IDP single logout url.",
    "idp-cert": "IDP Certificate name.",
    "scim-client": "SCIM client name.",
    "scim-user-attr-type": "User attribute type used to match SCIM users (default = user-name).",
    "scim-group-attr-type": "Group attribute type used to match SCIM groups (default = display-name).",
    "user-name": "User name in assertion statement.",
    "group-name": "Group name in assertion statement.",
    "digest-method": "Digest method algorithm.",
    "require-signed-resp-and-asrt": "Require both response and assertion from IDP to be signed when FGT acts as SP (default = disable).",
    "limit-relaystate": "Enable/disable limiting of relay-state parameter when it exceeds SAML 2.0 specification limits (80 bytes).",
    "clock-tolerance": "Clock skew tolerance in seconds (0 - 300, default = 15, 0 = no tolerance).",
    "adfs-claim": "Enable/disable ADFS Claim for user/group attribute in assertion statement (default = disable).",
    "user-claim-type": "User name claim in assertion statement.",
    "group-claim-type": "Group claim in assertion statement.",
    "reauth": "Enable/disable signalling of IDP to force user re-authentication (default = disable).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "cert": {"type": "string", "max_length": 35},
    "entity-id": {"type": "string", "max_length": 255},
    "single-sign-on-url": {"type": "string", "max_length": 255},
    "single-logout-url": {"type": "string", "max_length": 255},
    "idp-entity-id": {"type": "string", "max_length": 255},
    "idp-single-sign-on-url": {"type": "string", "max_length": 255},
    "idp-single-logout-url": {"type": "string", "max_length": 255},
    "idp-cert": {"type": "string", "max_length": 35},
    "scim-client": {"type": "string", "max_length": 35},
    "user-name": {"type": "string", "max_length": 255},
    "group-name": {"type": "string", "max_length": 255},
    "clock-tolerance": {"type": "integer", "min": 0, "max": 300},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_SCIM_USER_ATTR_TYPE = [
    "user-name",
    "display-name",
    "external-id",
    "email",
]
VALID_BODY_SCIM_GROUP_ATTR_TYPE = [
    "display-name",
    "external-id",
]
VALID_BODY_DIGEST_METHOD = [
    "sha1",
    "sha256",
]
VALID_BODY_REQUIRE_SIGNED_RESP_AND_ASRT = [
    "enable",
    "disable",
]
VALID_BODY_LIMIT_RELAYSTATE = [
    "enable",
    "disable",
]
VALID_BODY_ADFS_CLAIM = [
    "enable",
    "disable",
]
VALID_BODY_USER_CLAIM_TYPE = [
    "email",
    "given-name",
    "name",
    "upn",
    "common-name",
    "email-adfs-1x",
    "group",
    "upn-adfs-1x",
    "role",
    "sur-name",
    "ppid",
    "name-identifier",
    "authentication-method",
    "deny-only-group-sid",
    "deny-only-primary-sid",
    "deny-only-primary-group-sid",
    "group-sid",
    "primary-group-sid",
    "primary-sid",
    "windows-account-name",
]
VALID_BODY_GROUP_CLAIM_TYPE = [
    "email",
    "given-name",
    "name",
    "upn",
    "common-name",
    "email-adfs-1x",
    "group",
    "upn-adfs-1x",
    "role",
    "sur-name",
    "ppid",
    "name-identifier",
    "authentication-method",
    "deny-only-group-sid",
    "deny-only-primary-sid",
    "deny-only-primary-group-sid",
    "group-sid",
    "primary-group-sid",
    "primary-sid",
    "windows-account-name",
]
VALID_BODY_REAUTH = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_user_saml_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for user/saml."""
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


def validate_user_saml_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new user/saml object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "scim-user-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "scim-user-attr-type",
            payload["scim-user-attr-type"],
            VALID_BODY_SCIM_USER_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scim-group-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "scim-group-attr-type",
            payload["scim-group-attr-type"],
            VALID_BODY_SCIM_GROUP_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digest-method" in payload:
        is_valid, error = _validate_enum_field(
            "digest-method",
            payload["digest-method"],
            VALID_BODY_DIGEST_METHOD,
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
    if "limit-relaystate" in payload:
        is_valid, error = _validate_enum_field(
            "limit-relaystate",
            payload["limit-relaystate"],
            VALID_BODY_LIMIT_RELAYSTATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adfs-claim" in payload:
        is_valid, error = _validate_enum_field(
            "adfs-claim",
            payload["adfs-claim"],
            VALID_BODY_ADFS_CLAIM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-claim-type" in payload:
        is_valid, error = _validate_enum_field(
            "user-claim-type",
            payload["user-claim-type"],
            VALID_BODY_USER_CLAIM_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-claim-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-claim-type",
            payload["group-claim-type"],
            VALID_BODY_GROUP_CLAIM_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reauth" in payload:
        is_valid, error = _validate_enum_field(
            "reauth",
            payload["reauth"],
            VALID_BODY_REAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_user_saml_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update user/saml."""
    # Validate enum values using central function
    if "scim-user-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "scim-user-attr-type",
            payload["scim-user-attr-type"],
            VALID_BODY_SCIM_USER_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scim-group-attr-type" in payload:
        is_valid, error = _validate_enum_field(
            "scim-group-attr-type",
            payload["scim-group-attr-type"],
            VALID_BODY_SCIM_GROUP_ATTR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digest-method" in payload:
        is_valid, error = _validate_enum_field(
            "digest-method",
            payload["digest-method"],
            VALID_BODY_DIGEST_METHOD,
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
    if "limit-relaystate" in payload:
        is_valid, error = _validate_enum_field(
            "limit-relaystate",
            payload["limit-relaystate"],
            VALID_BODY_LIMIT_RELAYSTATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "adfs-claim" in payload:
        is_valid, error = _validate_enum_field(
            "adfs-claim",
            payload["adfs-claim"],
            VALID_BODY_ADFS_CLAIM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-claim-type" in payload:
        is_valid, error = _validate_enum_field(
            "user-claim-type",
            payload["user-claim-type"],
            VALID_BODY_USER_CLAIM_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-claim-type" in payload:
        is_valid, error = _validate_enum_field(
            "group-claim-type",
            payload["group-claim-type"],
            VALID_BODY_GROUP_CLAIM_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reauth" in payload:
        is_valid, error = _validate_enum_field(
            "reauth",
            payload["reauth"],
            VALID_BODY_REAUTH,
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
    "endpoint": "user/saml",
    "category": "cmdb",
    "api_path": "user/saml",
    "mkey": "name",
    "mkey_type": "string",
    "help": "SAML server entry configuration.",
    "total_fields": 22,
    "required_fields_count": 5,
    "fields_with_defaults_count": 22,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
