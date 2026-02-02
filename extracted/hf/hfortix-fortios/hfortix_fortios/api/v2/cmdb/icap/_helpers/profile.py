"""Validation helpers for icap/profile - Auto-generated"""

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
    "request-server",  # ICAP server to use for an HTTP request.
    "response-server",  # ICAP server to use for an HTTP response.
    "file-transfer-server",  # ICAP server to use for a file transfer.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "replacemsg-group": "",
    "name": "",
    "request": "disable",
    "response": "disable",
    "file-transfer": "",
    "streaming-content-bypass": "disable",
    "ocr-only": "disable",
    "204-size-limit": 1,
    "204-response": "disable",
    "preview": "disable",
    "preview-data-length": 0,
    "request-server": "",
    "response-server": "",
    "file-transfer-server": "",
    "request-failure": "error",
    "response-failure": "error",
    "file-transfer-failure": "error",
    "request-path": "",
    "response-path": "",
    "file-transfer-path": "",
    "methods": "delete get head options post put trace connect other",
    "response-req-hdr": "enable",
    "respmod-default-action": "forward",
    "icap-block-log": "disable",
    "chunk-encap": "disable",
    "extension-feature": "",
    "scan-progress-interval": 10,
    "timeout": 30,
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
    "replacemsg-group": "string",  # Replacement message group.
    "name": "string",  # ICAP profile name.
    "comment": "var-string",  # Comment.
    "request": "option",  # Enable/disable whether an HTTP request is passed to an ICAP 
    "response": "option",  # Enable/disable whether an HTTP response is passed to an ICAP
    "file-transfer": "option",  # Configure the file transfer protocols to pass transferred fi
    "streaming-content-bypass": "option",  # Enable/disable bypassing of ICAP server for streaming conten
    "ocr-only": "option",  # Enable/disable this FortiGate unit to submit only OCR intere
    "204-size-limit": "integer",  # 204 response size limit to be saved by ICAP client in megaby
    "204-response": "option",  # Enable/disable allowance of 204 response from ICAP server.
    "preview": "option",  # Enable/disable preview of data to ICAP server.
    "preview-data-length": "integer",  # Preview data length to be sent to ICAP server.
    "request-server": "string",  # ICAP server to use for an HTTP request.
    "response-server": "string",  # ICAP server to use for an HTTP response.
    "file-transfer-server": "string",  # ICAP server to use for a file transfer.
    "request-failure": "option",  # Action to take if the ICAP server cannot be contacted when p
    "response-failure": "option",  # Action to take if the ICAP server cannot be contacted when p
    "file-transfer-failure": "option",  # Action to take if the ICAP server cannot be contacted when p
    "request-path": "string",  # Path component of the ICAP URI that identifies the HTTP requ
    "response-path": "string",  # Path component of the ICAP URI that identifies the HTTP resp
    "file-transfer-path": "string",  # Path component of the ICAP URI that identifies the file tran
    "methods": "option",  # The allowed HTTP methods that will be sent to ICAP server fo
    "response-req-hdr": "option",  # Enable/disable addition of req-hdr for ICAP response modific
    "respmod-default-action": "option",  # Default action to ICAP response modification (respmod) proce
    "icap-block-log": "option",  # Enable/disable UTM log when infection found (default = disab
    "chunk-encap": "option",  # Enable/disable chunked encapsulation (default = disable).
    "extension-feature": "option",  # Enable/disable ICAP extension features.
    "scan-progress-interval": "integer",  # Scan progress interval value.
    "timeout": "integer",  # Time (in seconds) that ICAP client waits for the response fr
    "icap-headers": "string",  # Configure ICAP forwarded request headers.
    "respmod-forward-rules": "string",  # ICAP response mode forward rules.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "replacemsg-group": "Replacement message group.",
    "name": "ICAP profile name.",
    "comment": "Comment.",
    "request": "Enable/disable whether an HTTP request is passed to an ICAP server.",
    "response": "Enable/disable whether an HTTP response is passed to an ICAP server.",
    "file-transfer": "Configure the file transfer protocols to pass transferred files to an ICAP server as REQMOD.",
    "streaming-content-bypass": "Enable/disable bypassing of ICAP server for streaming content.",
    "ocr-only": "Enable/disable this FortiGate unit to submit only OCR interested content to the ICAP server.",
    "204-size-limit": "204 response size limit to be saved by ICAP client in megabytes (1 - 10, default = 1 MB).",
    "204-response": "Enable/disable allowance of 204 response from ICAP server.",
    "preview": "Enable/disable preview of data to ICAP server.",
    "preview-data-length": "Preview data length to be sent to ICAP server.",
    "request-server": "ICAP server to use for an HTTP request.",
    "response-server": "ICAP server to use for an HTTP response.",
    "file-transfer-server": "ICAP server to use for a file transfer.",
    "request-failure": "Action to take if the ICAP server cannot be contacted when processing an HTTP request.",
    "response-failure": "Action to take if the ICAP server cannot be contacted when processing an HTTP response.",
    "file-transfer-failure": "Action to take if the ICAP server cannot be contacted when processing a file transfer.",
    "request-path": "Path component of the ICAP URI that identifies the HTTP request processing service.",
    "response-path": "Path component of the ICAP URI that identifies the HTTP response processing service.",
    "file-transfer-path": "Path component of the ICAP URI that identifies the file transfer processing service.",
    "methods": "The allowed HTTP methods that will be sent to ICAP server for further processing.",
    "response-req-hdr": "Enable/disable addition of req-hdr for ICAP response modification (respmod) processing.",
    "respmod-default-action": "Default action to ICAP response modification (respmod) processing.",
    "icap-block-log": "Enable/disable UTM log when infection found (default = disable).",
    "chunk-encap": "Enable/disable chunked encapsulation (default = disable).",
    "extension-feature": "Enable/disable ICAP extension features.",
    "scan-progress-interval": "Scan progress interval value.",
    "timeout": "Time (in seconds) that ICAP client waits for the response from ICAP server.",
    "icap-headers": "Configure ICAP forwarded request headers.",
    "respmod-forward-rules": "ICAP response mode forward rules.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "replacemsg-group": {"type": "string", "max_length": 35},
    "name": {"type": "string", "max_length": 47},
    "204-size-limit": {"type": "integer", "min": 1, "max": 10},
    "preview-data-length": {"type": "integer", "min": 0, "max": 4096},
    "request-server": {"type": "string", "max_length": 63},
    "response-server": {"type": "string", "max_length": 63},
    "file-transfer-server": {"type": "string", "max_length": 63},
    "request-path": {"type": "string", "max_length": 127},
    "response-path": {"type": "string", "max_length": 127},
    "file-transfer-path": {"type": "string", "max_length": 127},
    "scan-progress-interval": {"type": "integer", "min": 5, "max": 30},
    "timeout": {"type": "integer", "min": 30, "max": 3600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "icap-headers": {
        "id": {
            "type": "integer",
            "help": "HTTP forwarded header ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "name": {
            "type": "string",
            "help": "HTTP forwarded header name.",
            "default": "",
            "max_length": 79,
        },
        "content": {
            "type": "string",
            "help": "HTTP header content.",
            "default": "",
            "max_length": 255,
        },
        "base64-encoding": {
            "type": "option",
            "help": "Enable/disable use of base64 encoding of HTTP content.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
    },
    "respmod-forward-rules": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "default": "",
            "max_length": 63,
        },
        "host": {
            "type": "string",
            "help": "Address object for the host.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "header-group": {
            "type": "string",
            "help": "HTTP header group.",
        },
        "action": {
            "type": "option",
            "help": "Action to be taken for ICAP server.",
            "default": "forward",
            "options": ["forward", "bypass"],
        },
        "http-resp-status-code": {
            "type": "string",
            "help": "HTTP response status code.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_REQUEST = [
    "disable",
    "enable",
]
VALID_BODY_RESPONSE = [
    "disable",
    "enable",
]
VALID_BODY_FILE_TRANSFER = [
    "ssh",
    "ftp",
]
VALID_BODY_STREAMING_CONTENT_BYPASS = [
    "disable",
    "enable",
]
VALID_BODY_OCR_ONLY = [
    "disable",
    "enable",
]
VALID_BODY_204_RESPONSE = [
    "disable",
    "enable",
]
VALID_BODY_PREVIEW = [
    "disable",
    "enable",
]
VALID_BODY_REQUEST_FAILURE = [
    "error",
    "bypass",
]
VALID_BODY_RESPONSE_FAILURE = [
    "error",
    "bypass",
]
VALID_BODY_FILE_TRANSFER_FAILURE = [
    "error",
    "bypass",
]
VALID_BODY_METHODS = [
    "delete",
    "get",
    "head",
    "options",
    "post",
    "put",
    "trace",
    "connect",
    "other",
]
VALID_BODY_RESPONSE_REQ_HDR = [
    "disable",
    "enable",
]
VALID_BODY_RESPMOD_DEFAULT_ACTION = [
    "forward",
    "bypass",
]
VALID_BODY_ICAP_BLOCK_LOG = [
    "disable",
    "enable",
]
VALID_BODY_CHUNK_ENCAP = [
    "disable",
    "enable",
]
VALID_BODY_EXTENSION_FEATURE = [
    "scan-progress",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_icap_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for icap/profile."""
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


def validate_icap_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new icap/profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "request" in payload:
        is_valid, error = _validate_enum_field(
            "request",
            payload["request"],
            VALID_BODY_REQUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "response" in payload:
        is_valid, error = _validate_enum_field(
            "response",
            payload["response"],
            VALID_BODY_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-transfer" in payload:
        is_valid, error = _validate_enum_field(
            "file-transfer",
            payload["file-transfer"],
            VALID_BODY_FILE_TRANSFER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "streaming-content-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "streaming-content-bypass",
            payload["streaming-content-bypass"],
            VALID_BODY_STREAMING_CONTENT_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ocr-only" in payload:
        is_valid, error = _validate_enum_field(
            "ocr-only",
            payload["ocr-only"],
            VALID_BODY_OCR_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "204-response" in payload:
        is_valid, error = _validate_enum_field(
            "204-response",
            payload["204-response"],
            VALID_BODY_204_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "preview" in payload:
        is_valid, error = _validate_enum_field(
            "preview",
            payload["preview"],
            VALID_BODY_PREVIEW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "request-failure" in payload:
        is_valid, error = _validate_enum_field(
            "request-failure",
            payload["request-failure"],
            VALID_BODY_REQUEST_FAILURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "response-failure" in payload:
        is_valid, error = _validate_enum_field(
            "response-failure",
            payload["response-failure"],
            VALID_BODY_RESPONSE_FAILURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-transfer-failure" in payload:
        is_valid, error = _validate_enum_field(
            "file-transfer-failure",
            payload["file-transfer-failure"],
            VALID_BODY_FILE_TRANSFER_FAILURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "methods" in payload:
        is_valid, error = _validate_enum_field(
            "methods",
            payload["methods"],
            VALID_BODY_METHODS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "response-req-hdr" in payload:
        is_valid, error = _validate_enum_field(
            "response-req-hdr",
            payload["response-req-hdr"],
            VALID_BODY_RESPONSE_REQ_HDR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "respmod-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "respmod-default-action",
            payload["respmod-default-action"],
            VALID_BODY_RESPMOD_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "icap-block-log" in payload:
        is_valid, error = _validate_enum_field(
            "icap-block-log",
            payload["icap-block-log"],
            VALID_BODY_ICAP_BLOCK_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "chunk-encap" in payload:
        is_valid, error = _validate_enum_field(
            "chunk-encap",
            payload["chunk-encap"],
            VALID_BODY_CHUNK_ENCAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extension-feature" in payload:
        is_valid, error = _validate_enum_field(
            "extension-feature",
            payload["extension-feature"],
            VALID_BODY_EXTENSION_FEATURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_icap_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update icap/profile."""
    # Validate enum values using central function
    if "request" in payload:
        is_valid, error = _validate_enum_field(
            "request",
            payload["request"],
            VALID_BODY_REQUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "response" in payload:
        is_valid, error = _validate_enum_field(
            "response",
            payload["response"],
            VALID_BODY_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-transfer" in payload:
        is_valid, error = _validate_enum_field(
            "file-transfer",
            payload["file-transfer"],
            VALID_BODY_FILE_TRANSFER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "streaming-content-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "streaming-content-bypass",
            payload["streaming-content-bypass"],
            VALID_BODY_STREAMING_CONTENT_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ocr-only" in payload:
        is_valid, error = _validate_enum_field(
            "ocr-only",
            payload["ocr-only"],
            VALID_BODY_OCR_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "204-response" in payload:
        is_valid, error = _validate_enum_field(
            "204-response",
            payload["204-response"],
            VALID_BODY_204_RESPONSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "preview" in payload:
        is_valid, error = _validate_enum_field(
            "preview",
            payload["preview"],
            VALID_BODY_PREVIEW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "request-failure" in payload:
        is_valid, error = _validate_enum_field(
            "request-failure",
            payload["request-failure"],
            VALID_BODY_REQUEST_FAILURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "response-failure" in payload:
        is_valid, error = _validate_enum_field(
            "response-failure",
            payload["response-failure"],
            VALID_BODY_RESPONSE_FAILURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-transfer-failure" in payload:
        is_valid, error = _validate_enum_field(
            "file-transfer-failure",
            payload["file-transfer-failure"],
            VALID_BODY_FILE_TRANSFER_FAILURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "methods" in payload:
        is_valid, error = _validate_enum_field(
            "methods",
            payload["methods"],
            VALID_BODY_METHODS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "response-req-hdr" in payload:
        is_valid, error = _validate_enum_field(
            "response-req-hdr",
            payload["response-req-hdr"],
            VALID_BODY_RESPONSE_REQ_HDR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "respmod-default-action" in payload:
        is_valid, error = _validate_enum_field(
            "respmod-default-action",
            payload["respmod-default-action"],
            VALID_BODY_RESPMOD_DEFAULT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "icap-block-log" in payload:
        is_valid, error = _validate_enum_field(
            "icap-block-log",
            payload["icap-block-log"],
            VALID_BODY_ICAP_BLOCK_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "chunk-encap" in payload:
        is_valid, error = _validate_enum_field(
            "chunk-encap",
            payload["chunk-encap"],
            VALID_BODY_CHUNK_ENCAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "extension-feature" in payload:
        is_valid, error = _validate_enum_field(
            "extension-feature",
            payload["extension-feature"],
            VALID_BODY_EXTENSION_FEATURE,
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
    "endpoint": "icap/profile",
    "category": "cmdb",
    "api_path": "icap/profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure ICAP profiles.",
    "total_fields": 31,
    "required_fields_count": 3,
    "fields_with_defaults_count": 28,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
