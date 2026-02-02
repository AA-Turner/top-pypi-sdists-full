"""Validation helpers for system/automation_action - Auto-generated"""

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
    "system-action",  # System action type.
    "aws-api-key",  # AWS API Gateway API key.
    "alicloud-access-key-id",  # AliCloud AccessKey ID.
    "alicloud-access-key-secret",  # AliCloud AccessKey secret.
    "uri",  # Request API URI.
    "script",  # CLI script.
    "regular-expression",  # Regular expression string.
    "security-tag",  # NSX security tag.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "action-type": "alert",
    "system-action": "",
    "tls-certificate": "",
    "forticare-email": "disable",
    "minimum-interval": 0,
    "azure-function-authorization": "anonymous",
    "alicloud-function-authorization": "anonymous",
    "alicloud-access-key-id": "",
    "message-type": "text",
    "message": "Time: %%log.date%% %%log.time%%\nDevice: %%log.devid%% (%%log.vd%%)\nLevel: %%log.level%%\nEvent: %%log.logdesc%%\nRaw log:\n%%log%%",
    "replacement-message": "disable",
    "replacemsg-group": "",
    "protocol": "http",
    "method": "post",
    "port": 0,
    "verify-host-cert": "enable",
    "output-size": 10,
    "timeout": 0,
    "duration": 5,
    "output-interval": 0,
    "file-only": "disable",
    "execute-security-fabric": "disable",
    "accprofile": "",
    "log-debug-print": "disable",
    "security-tag": "",
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
    "name": "string",  # Name.
    "description": "var-string",  # Description.
    "action-type": "option",  # Action type.
    "system-action": "option",  # System action type.
    "tls-certificate": "string",  # Custom TLS certificate for API request.
    "forticare-email": "option",  # Enable/disable use of your FortiCare email address as the em
    "email-to": "string",  # Email addresses.
    "email-from": "var-string",  # Email sender name.
    "email-subject": "var-string",  # Email subject.
    "minimum-interval": "integer",  # Limit execution to no more than once in this interval (in se
    "aws-api-key": "password",  # AWS API Gateway API key.
    "azure-function-authorization": "option",  # Azure function authorization level.
    "azure-api-key": "password",  # Azure function API key.
    "alicloud-function-authorization": "option",  # AliCloud function authorization type.
    "alicloud-access-key-id": "string",  # AliCloud AccessKey ID.
    "alicloud-access-key-secret": "password",  # AliCloud AccessKey secret.
    "message-type": "option",  # Message type.
    "message": "string",  # Message content.
    "replacement-message": "option",  # Enable/disable replacement message.
    "replacemsg-group": "string",  # Replacement message group.
    "protocol": "option",  # Request protocol.
    "method": "option",  # Request method (POST, PUT, GET, PATCH or DELETE).
    "uri": "var-string",  # Request API URI.
    "http-body": "var-string",  # Request body (if necessary). Should be serialized json strin
    "port": "integer",  # Protocol port.
    "http-headers": "string",  # Request headers.
    "form-data": "string",  # Form data parts for content type multipart/form-data.
    "verify-host-cert": "option",  # Enable/disable verification of the remote host certificate.
    "script": "var-string",  # CLI script.
    "output-size": "integer",  # Number of megabytes to limit script output to (1 - 1024, def
    "timeout": "integer",  # Maximum running time for this script in seconds (0 = no time
    "duration": "integer",  # Maximum running time for this script in seconds.
    "output-interval": "integer",  # Collect the outputs for each output-interval in seconds (0 =
    "file-only": "option",  # Enable/disable the output in files only.
    "execute-security-fabric": "option",  # Enable/disable execution of CLI script on all or only one Fo
    "accprofile": "string",  # Access profile for CLI script action to access FortiGate fea
    "regular-expression": "var-string",  # Regular expression string.
    "log-debug-print": "option",  # Enable/disable logging debug print output from diagnose acti
    "security-tag": "string",  # NSX security tag.
    "sdn-connector": "string",  # NSX SDN connector names.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "description": "Description.",
    "action-type": "Action type.",
    "system-action": "System action type.",
    "tls-certificate": "Custom TLS certificate for API request.",
    "forticare-email": "Enable/disable use of your FortiCare email address as the email-to address.",
    "email-to": "Email addresses.",
    "email-from": "Email sender name.",
    "email-subject": "Email subject.",
    "minimum-interval": "Limit execution to no more than once in this interval (in seconds).",
    "aws-api-key": "AWS API Gateway API key.",
    "azure-function-authorization": "Azure function authorization level.",
    "azure-api-key": "Azure function API key.",
    "alicloud-function-authorization": "AliCloud function authorization type.",
    "alicloud-access-key-id": "AliCloud AccessKey ID.",
    "alicloud-access-key-secret": "AliCloud AccessKey secret.",
    "message-type": "Message type.",
    "message": "Message content.",
    "replacement-message": "Enable/disable replacement message.",
    "replacemsg-group": "Replacement message group.",
    "protocol": "Request protocol.",
    "method": "Request method (POST, PUT, GET, PATCH or DELETE).",
    "uri": "Request API URI.",
    "http-body": "Request body (if necessary). Should be serialized json string.",
    "port": "Protocol port.",
    "http-headers": "Request headers.",
    "form-data": "Form data parts for content type multipart/form-data.",
    "verify-host-cert": "Enable/disable verification of the remote host certificate.",
    "script": "CLI script.",
    "output-size": "Number of megabytes to limit script output to (1 - 1024, default = 10).",
    "timeout": "Maximum running time for this script in seconds (0 = no timeout).",
    "duration": "Maximum running time for this script in seconds.",
    "output-interval": "Collect the outputs for each output-interval in seconds (0 = no intermediate output).",
    "file-only": "Enable/disable the output in files only.",
    "execute-security-fabric": "Enable/disable execution of CLI script on all or only one FortiGate unit in the Security Fabric.",
    "accprofile": "Access profile for CLI script action to access FortiGate features.",
    "regular-expression": "Regular expression string.",
    "log-debug-print": "Enable/disable logging debug print output from diagnose action.",
    "security-tag": "NSX security tag.",
    "sdn-connector": "NSX SDN connector names.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 64},
    "tls-certificate": {"type": "string", "max_length": 35},
    "minimum-interval": {"type": "integer", "min": 0, "max": 2592000},
    "alicloud-access-key-id": {"type": "string", "max_length": 35},
    "message": {"type": "string", "max_length": 4095},
    "replacemsg-group": {"type": "string", "max_length": 35},
    "port": {"type": "integer", "min": 1, "max": 65535},
    "output-size": {"type": "integer", "min": 1, "max": 1024},
    "timeout": {"type": "integer", "min": 0, "max": 300},
    "duration": {"type": "integer", "min": 1, "max": 36000},
    "output-interval": {"type": "integer", "min": 0, "max": 36000},
    "accprofile": {"type": "string", "max_length": 35},
    "security-tag": {"type": "string", "max_length": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "email-to": {
        "name": {
            "type": "string",
            "help": "Email address.",
            "required": True,
            "default": "",
            "max_length": 255,
        },
    },
    "http-headers": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "key": {
            "type": "var-string",
            "help": "Request header key.",
            "required": True,
            "max_length": 1023,
        },
        "value": {
            "type": "var-string",
            "help": "Request header value.",
            "required": True,
            "max_length": 4095,
        },
    },
    "form-data": {
        "id": {
            "type": "integer",
            "help": "Entry ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "key": {
            "type": "var-string",
            "help": "Key of the part of Multipart/form-data.",
            "required": True,
            "max_length": 1023,
        },
        "value": {
            "type": "var-string",
            "help": "Value of the part of Multipart/form-data.",
            "required": True,
            "max_length": 4095,
        },
    },
    "sdn-connector": {
        "name": {
            "type": "string",
            "help": "SDN connector name.",
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ACTION_TYPE = [
    "email",
    "fortiexplorer-notification",
    "alert",
    "disable-ssid",
    "system-actions",
    "quarantine",
    "quarantine-forticlient",
    "quarantine-nsx",
    "quarantine-fortinac",
    "ban-ip",
    "aws-lambda",
    "azure-function",
    "google-cloud-function",
    "alicloud-function",
    "webhook",
    "cli-script",
    "diagnose-script",
    "regular-expression",
    "slack-notification",
    "microsoft-teams-notification",
]
VALID_BODY_SYSTEM_ACTION = [
    "reboot",
    "shutdown",
    "backup-config",
]
VALID_BODY_FORTICARE_EMAIL = [
    "enable",
    "disable",
]
VALID_BODY_AZURE_FUNCTION_AUTHORIZATION = [
    "anonymous",
    "function",
    "admin",
]
VALID_BODY_ALICLOUD_FUNCTION_AUTHORIZATION = [
    "anonymous",
    "function",
]
VALID_BODY_MESSAGE_TYPE = [
    "text",
    "json",
    "form-data",
]
VALID_BODY_REPLACEMENT_MESSAGE = [
    "enable",
    "disable",
]
VALID_BODY_PROTOCOL = [
    "http",
    "https",
]
VALID_BODY_METHOD = [
    "post",
    "put",
    "get",
    "patch",
    "delete",
]
VALID_BODY_VERIFY_HOST_CERT = [
    "enable",
    "disable",
]
VALID_BODY_FILE_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_EXECUTE_SECURITY_FABRIC = [
    "enable",
    "disable",
]
VALID_BODY_LOG_DEBUG_PRINT = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_automation_action_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/automation_action."""
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


def validate_system_automation_action_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/automation_action object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "action-type" in payload:
        is_valid, error = _validate_enum_field(
            "action-type",
            payload["action-type"],
            VALID_BODY_ACTION_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-action" in payload:
        is_valid, error = _validate_enum_field(
            "system-action",
            payload["system-action"],
            VALID_BODY_SYSTEM_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticare-email" in payload:
        is_valid, error = _validate_enum_field(
            "forticare-email",
            payload["forticare-email"],
            VALID_BODY_FORTICARE_EMAIL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "azure-function-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "azure-function-authorization",
            payload["azure-function-authorization"],
            VALID_BODY_AZURE_FUNCTION_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "alicloud-function-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "alicloud-function-authorization",
            payload["alicloud-function-authorization"],
            VALID_BODY_ALICLOUD_FUNCTION_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "message-type" in payload:
        is_valid, error = _validate_enum_field(
            "message-type",
            payload["message-type"],
            VALID_BODY_MESSAGE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "replacement-message" in payload:
        is_valid, error = _validate_enum_field(
            "replacement-message",
            payload["replacement-message"],
            VALID_BODY_REPLACEMENT_MESSAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "method" in payload:
        is_valid, error = _validate_enum_field(
            "method",
            payload["method"],
            VALID_BODY_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "verify-host-cert" in payload:
        is_valid, error = _validate_enum_field(
            "verify-host-cert",
            payload["verify-host-cert"],
            VALID_BODY_VERIFY_HOST_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-only" in payload:
        is_valid, error = _validate_enum_field(
            "file-only",
            payload["file-only"],
            VALID_BODY_FILE_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "execute-security-fabric" in payload:
        is_valid, error = _validate_enum_field(
            "execute-security-fabric",
            payload["execute-security-fabric"],
            VALID_BODY_EXECUTE_SECURITY_FABRIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-debug-print" in payload:
        is_valid, error = _validate_enum_field(
            "log-debug-print",
            payload["log-debug-print"],
            VALID_BODY_LOG_DEBUG_PRINT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_automation_action_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/automation_action."""
    # Validate enum values using central function
    if "action-type" in payload:
        is_valid, error = _validate_enum_field(
            "action-type",
            payload["action-type"],
            VALID_BODY_ACTION_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-action" in payload:
        is_valid, error = _validate_enum_field(
            "system-action",
            payload["system-action"],
            VALID_BODY_SYSTEM_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticare-email" in payload:
        is_valid, error = _validate_enum_field(
            "forticare-email",
            payload["forticare-email"],
            VALID_BODY_FORTICARE_EMAIL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "azure-function-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "azure-function-authorization",
            payload["azure-function-authorization"],
            VALID_BODY_AZURE_FUNCTION_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "alicloud-function-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "alicloud-function-authorization",
            payload["alicloud-function-authorization"],
            VALID_BODY_ALICLOUD_FUNCTION_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "message-type" in payload:
        is_valid, error = _validate_enum_field(
            "message-type",
            payload["message-type"],
            VALID_BODY_MESSAGE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "replacement-message" in payload:
        is_valid, error = _validate_enum_field(
            "replacement-message",
            payload["replacement-message"],
            VALID_BODY_REPLACEMENT_MESSAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "method" in payload:
        is_valid, error = _validate_enum_field(
            "method",
            payload["method"],
            VALID_BODY_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "verify-host-cert" in payload:
        is_valid, error = _validate_enum_field(
            "verify-host-cert",
            payload["verify-host-cert"],
            VALID_BODY_VERIFY_HOST_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "file-only" in payload:
        is_valid, error = _validate_enum_field(
            "file-only",
            payload["file-only"],
            VALID_BODY_FILE_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "execute-security-fabric" in payload:
        is_valid, error = _validate_enum_field(
            "execute-security-fabric",
            payload["execute-security-fabric"],
            VALID_BODY_EXECUTE_SECURITY_FABRIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-debug-print" in payload:
        is_valid, error = _validate_enum_field(
            "log-debug-print",
            payload["log-debug-print"],
            VALID_BODY_LOG_DEBUG_PRINT,
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
    "endpoint": "system/automation_action",
    "category": "cmdb",
    "api_path": "system/automation-action",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Action for automation stitches.",
    "total_fields": 40,
    "required_fields_count": 8,
    "fields_with_defaults_count": 26,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
