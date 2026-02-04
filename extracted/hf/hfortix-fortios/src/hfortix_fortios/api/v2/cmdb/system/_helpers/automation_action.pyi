from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_ACTION_TYPE: Literal["email", "fortiexplorer-notification", "alert", "disable-ssid", "system-actions", "quarantine", "quarantine-forticlient", "quarantine-nsx", "quarantine-fortinac", "ban-ip", "aws-lambda", "azure-function", "google-cloud-function", "alicloud-function", "webhook", "cli-script", "diagnose-script", "regular-expression", "slack-notification", "microsoft-teams-notification"]
VALID_BODY_SYSTEM_ACTION: Literal["reboot", "shutdown", "backup-config"]
VALID_BODY_FORTICARE_EMAIL: Literal["enable", "disable"]
VALID_BODY_AZURE_FUNCTION_AUTHORIZATION: Literal["anonymous", "function", "admin"]
VALID_BODY_ALICLOUD_FUNCTION_AUTHORIZATION: Literal["anonymous", "function"]
VALID_BODY_MESSAGE_TYPE: Literal["text", "json", "form-data"]
VALID_BODY_REPLACEMENT_MESSAGE: Literal["enable", "disable"]
VALID_BODY_PROTOCOL: Literal["http", "https"]
VALID_BODY_METHOD: Literal["post", "put", "get", "patch", "delete"]
VALID_BODY_VERIFY_HOST_CERT: Literal["enable", "disable"]
VALID_BODY_FILE_ONLY: Literal["enable", "disable"]
VALID_BODY_EXECUTE_SECURITY_FABRIC: Literal["enable", "disable"]
VALID_BODY_LOG_DEBUG_PRINT: Literal["enable", "disable"]

# Metadata dictionaries
FIELD_TYPES: dict[str, str]
FIELD_DESCRIPTIONS: dict[str, str]
FIELD_CONSTRAINTS: dict[str, dict[str, Any]]
NESTED_SCHEMAS: dict[str, dict[str, Any]]
FIELDS_WITH_DEFAULTS: dict[str, Any]
DEPRECATED_FIELDS: dict[str, dict[str, str]]
REQUIRED_FIELDS: list[str]

# Helper functions
def get_field_type(field_name: str) -> str | None: ...
def get_field_description(field_name: str) -> str | None: ...
def get_field_default(field_name: str) -> Any: ...
def get_field_constraints(field_name: str) -> dict[str, Any]: ...
def get_nested_schema(field_name: str) -> dict[str, Any] | None: ...
def get_field_metadata(field_name: str) -> dict[str, Any]: ...
def validate_field_value(field_name: str, value: Any) -> bool: ...
def get_all_fields() -> list[str]: ...
def get_required_fields() -> list[str]: ...
def get_schema_info() -> dict[str, Any]: ...


__all__ = [
    "VALID_BODY_ACTION_TYPE",
    "VALID_BODY_SYSTEM_ACTION",
    "VALID_BODY_FORTICARE_EMAIL",
    "VALID_BODY_AZURE_FUNCTION_AUTHORIZATION",
    "VALID_BODY_ALICLOUD_FUNCTION_AUTHORIZATION",
    "VALID_BODY_MESSAGE_TYPE",
    "VALID_BODY_REPLACEMENT_MESSAGE",
    "VALID_BODY_PROTOCOL",
    "VALID_BODY_METHOD",
    "VALID_BODY_VERIFY_HOST_CERT",
    "VALID_BODY_FILE_ONLY",
    "VALID_BODY_EXECUTE_SECURITY_FABRIC",
    "VALID_BODY_LOG_DEBUG_PRINT",
    "FIELD_TYPES",
    "FIELD_DESCRIPTIONS",
    "FIELD_CONSTRAINTS",
    "NESTED_SCHEMAS",
    "FIELDS_WITH_DEFAULTS",
    "DEPRECATED_FIELDS",
    "REQUIRED_FIELDS",
    "get_field_type",
    "get_field_description",
    "get_field_default",
    "get_field_constraints",
    "get_nested_schema",
    "get_field_metadata",
    "validate_field_value",
    "get_all_fields",
    "get_required_fields",
    "get_schema_info",
]