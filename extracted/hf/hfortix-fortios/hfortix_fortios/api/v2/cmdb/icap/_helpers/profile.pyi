from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_REQUEST: Literal["disable", "enable"]
VALID_BODY_RESPONSE: Literal["disable", "enable"]
VALID_BODY_FILE_TRANSFER: Literal["ssh", "ftp"]
VALID_BODY_STREAMING_CONTENT_BYPASS: Literal["disable", "enable"]
VALID_BODY_OCR_ONLY: Literal["disable", "enable"]
VALID_BODY_204_RESPONSE: Literal["disable", "enable"]
VALID_BODY_PREVIEW: Literal["disable", "enable"]
VALID_BODY_REQUEST_FAILURE: Literal["error", "bypass"]
VALID_BODY_RESPONSE_FAILURE: Literal["error", "bypass"]
VALID_BODY_FILE_TRANSFER_FAILURE: Literal["error", "bypass"]
VALID_BODY_METHODS: Literal["delete", "get", "head", "options", "post", "put", "trace", "connect", "other"]
VALID_BODY_RESPONSE_REQ_HDR: Literal["disable", "enable"]
VALID_BODY_RESPMOD_DEFAULT_ACTION: Literal["forward", "bypass"]
VALID_BODY_ICAP_BLOCK_LOG: Literal["disable", "enable"]
VALID_BODY_CHUNK_ENCAP: Literal["disable", "enable"]
VALID_BODY_EXTENSION_FEATURE: Literal["scan-progress"]

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
    "VALID_BODY_REQUEST",
    "VALID_BODY_RESPONSE",
    "VALID_BODY_FILE_TRANSFER",
    "VALID_BODY_STREAMING_CONTENT_BYPASS",
    "VALID_BODY_OCR_ONLY",
    "VALID_BODY_204_RESPONSE",
    "VALID_BODY_PREVIEW",
    "VALID_BODY_REQUEST_FAILURE",
    "VALID_BODY_RESPONSE_FAILURE",
    "VALID_BODY_FILE_TRANSFER_FAILURE",
    "VALID_BODY_METHODS",
    "VALID_BODY_RESPONSE_REQ_HDR",
    "VALID_BODY_RESPMOD_DEFAULT_ACTION",
    "VALID_BODY_ICAP_BLOCK_LOG",
    "VALID_BODY_CHUNK_ENCAP",
    "VALID_BODY_EXTENSION_FEATURE",
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