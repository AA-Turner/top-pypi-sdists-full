from typing import Any, Literal

# Enum type aliases for validation
VALID_BODY_STATUS: Literal["disable", "enable"]
VALID_BODY_TYPE: Literal["aci", "alicloud", "aws", "azure", "gcp", "nsx", "nuage", "oci", "openstack", "kubernetes", "vmware", "sepm", "aci-direct", "ibm", "nutanix", "sap"]
VALID_BODY_USE_METADATA_IAM: Literal["disable", "enable"]
VALID_BODY_MICROSOFT_365: Literal["disable", "enable"]
VALID_BODY_HA_STATUS: Literal["disable", "enable"]
VALID_BODY_VERIFY_CERTIFICATE: Literal["disable", "enable"]
VALID_BODY_ALT_RESOURCE_IP: Literal["disable", "enable"]
VALID_BODY_AZURE_REGION: Literal["global", "china", "germany", "usgov", "local"]
VALID_BODY_OCI_REGION_TYPE: Literal["commercial", "government"]
VALID_BODY_IBM_REGION: Literal["dallas", "washington-dc", "london", "frankfurt", "sydney", "tokyo", "osaka", "toronto", "sao-paulo", "madrid"]

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
    "VALID_BODY_STATUS",
    "VALID_BODY_TYPE",
    "VALID_BODY_USE_METADATA_IAM",
    "VALID_BODY_MICROSOFT_365",
    "VALID_BODY_HA_STATUS",
    "VALID_BODY_VERIFY_CERTIFICATE",
    "VALID_BODY_ALT_RESOURCE_IP",
    "VALID_BODY_AZURE_REGION",
    "VALID_BODY_OCI_REGION_TYPE",
    "VALID_BODY_IBM_REGION",
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