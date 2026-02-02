"""Validation helpers for system/sdn_connector - Auto-generated"""

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
    "server",  # Server address of the remote SDN connector.
    "server-list",  # Server address list of the remote SDN connector.
    "username",  # Username of the remote SDN connector as login credentials.
    "password",  # Password of the remote SDN connector as login credentials.
    "access-key",  # AWS / ACS access key ID.
    "secret-key",  # AWS / ACS secret access key.
    "region",  # AWS / ACS region name.
    "service-account",  # GCP service account email.
    "private-key",  # Private key of GCP service account.
    "secret-token",  # Secret token of Kubernetes service account.
    "api-key",  # IBM cloud API key or service ID API key.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "status": "enable",
    "type": "aws",
    "proxy": "",
    "use-metadata-iam": "disable",
    "microsoft-365": "disable",
    "ha-status": "disable",
    "verify-certificate": "enable",
    "vdom": "",
    "server": "",
    "server-port": 0,
    "message-server-port": 0,
    "username": "",
    "vcenter-server": "",
    "vcenter-username": "",
    "access-key": "",
    "region": "",
    "vpc-id": "",
    "alt-resource-ip": "disable",
    "tenant-id": "",
    "client-id": "",
    "subscription-id": "",
    "resource-group": "",
    "login-endpoint": "",
    "resource-url": "",
    "azure-region": "global",
    "user-id": "",
    "oci-region-type": "commercial",
    "oci-cert": "",
    "oci-fingerprint": "",
    "service-account": "",
    "private-key": "",
    "secret-token": "",
    "domain": "",
    "group-name": "",
    "server-cert": "",
    "server-ca-cert": "",
    "ibm-region": "dallas",
    "par-id": "",
    "update-interval": 60,
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
    "name": "string",  # SDN connector name.
    "status": "option",  # Enable/disable connection to the remote SDN connector.
    "type": "option",  # Type of SDN connector.
    "proxy": "string",  # SDN proxy.
    "use-metadata-iam": "option",  # Enable/disable use of IAM role from metadata to call API.
    "microsoft-365": "option",  # Enable to use as Microsoft 365 connector.
    "ha-status": "option",  # Enable/disable use for FortiGate HA service.
    "verify-certificate": "option",  # Enable/disable server certificate verification.
    "vdom": "string",  # Virtual domain name of the remote SDN connector.
    "server": "string",  # Server address of the remote SDN connector.
    "server-list": "string",  # Server address list of the remote SDN connector.
    "server-port": "integer",  # Port number of the remote SDN connector.
    "message-server-port": "integer",  # HTTP port number of the SAP message server.
    "username": "string",  # Username of the remote SDN connector as login credentials.
    "password": "password_aes256",  # Password of the remote SDN connector as login credentials.
    "vcenter-server": "string",  # vCenter server address for NSX quarantine.
    "vcenter-username": "string",  # vCenter server username for NSX quarantine.
    "vcenter-password": "password_aes256",  # vCenter server password for NSX quarantine.
    "access-key": "string",  # AWS / ACS access key ID.
    "secret-key": "password",  # AWS / ACS secret access key.
    "region": "string",  # AWS / ACS region name.
    "vpc-id": "string",  # AWS VPC ID.
    "alt-resource-ip": "option",  # Enable/disable AWS alternative resource IP.
    "external-account-list": "string",  # Configure AWS external account list.
    "tenant-id": "string",  # Tenant ID (directory ID).
    "client-id": "string",  # Azure client ID (application ID).
    "client-secret": "password",  # Azure client secret (application key).
    "subscription-id": "string",  # Azure subscription ID.
    "resource-group": "string",  # Azure resource group.
    "login-endpoint": "string",  # Azure Stack login endpoint.
    "resource-url": "string",  # Azure Stack resource URL.
    "azure-region": "option",  # Azure server region.
    "nic": "string",  # Configure Azure network interface.
    "route-table": "string",  # Configure Azure route table.
    "user-id": "string",  # User ID.
    "compartment-list": "string",  # Configure OCI compartment list.
    "oci-region-list": "string",  # Configure OCI region list.
    "oci-region-type": "option",  # OCI region type.
    "oci-cert": "string",  # OCI certificate.
    "oci-fingerprint": "string",  # OCI pubkey fingerprint.
    "external-ip": "string",  # Configure GCP external IP.
    "route": "string",  # Configure GCP route.
    "gcp-project-list": "string",  # Configure GCP project list.
    "forwarding-rule": "string",  # Configure GCP forwarding rule.
    "service-account": "string",  # GCP service account email.
    "private-key": "user",  # Private key of GCP service account.
    "secret-token": "user",  # Secret token of Kubernetes service account.
    "domain": "string",  # Domain name.
    "group-name": "string",  # Full path group name of computers.
    "server-cert": "string",  # Trust servers that contain this certificate only.
    "server-ca-cert": "string",  # Trust only those servers whose certificate is directly/indir
    "api-key": "password",  # IBM cloud API key or service ID API key.
    "ibm-region": "option",  # IBM cloud region name.
    "par-id": "string",  # Public address range ID.
    "update-interval": "integer",  # Dynamic object update interval (30 - 3600 sec, default = 60,
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "SDN connector name.",
    "status": "Enable/disable connection to the remote SDN connector.",
    "type": "Type of SDN connector.",
    "proxy": "SDN proxy.",
    "use-metadata-iam": "Enable/disable use of IAM role from metadata to call API.",
    "microsoft-365": "Enable to use as Microsoft 365 connector.",
    "ha-status": "Enable/disable use for FortiGate HA service.",
    "verify-certificate": "Enable/disable server certificate verification.",
    "vdom": "Virtual domain name of the remote SDN connector.",
    "server": "Server address of the remote SDN connector.",
    "server-list": "Server address list of the remote SDN connector.",
    "server-port": "Port number of the remote SDN connector.",
    "message-server-port": "HTTP port number of the SAP message server.",
    "username": "Username of the remote SDN connector as login credentials.",
    "password": "Password of the remote SDN connector as login credentials.",
    "vcenter-server": "vCenter server address for NSX quarantine.",
    "vcenter-username": "vCenter server username for NSX quarantine.",
    "vcenter-password": "vCenter server password for NSX quarantine.",
    "access-key": "AWS / ACS access key ID.",
    "secret-key": "AWS / ACS secret access key.",
    "region": "AWS / ACS region name.",
    "vpc-id": "AWS VPC ID.",
    "alt-resource-ip": "Enable/disable AWS alternative resource IP.",
    "external-account-list": "Configure AWS external account list.",
    "tenant-id": "Tenant ID (directory ID).",
    "client-id": "Azure client ID (application ID).",
    "client-secret": "Azure client secret (application key).",
    "subscription-id": "Azure subscription ID.",
    "resource-group": "Azure resource group.",
    "login-endpoint": "Azure Stack login endpoint.",
    "resource-url": "Azure Stack resource URL.",
    "azure-region": "Azure server region.",
    "nic": "Configure Azure network interface.",
    "route-table": "Configure Azure route table.",
    "user-id": "User ID.",
    "compartment-list": "Configure OCI compartment list.",
    "oci-region-list": "Configure OCI region list.",
    "oci-region-type": "OCI region type.",
    "oci-cert": "OCI certificate.",
    "oci-fingerprint": "OCI pubkey fingerprint.",
    "external-ip": "Configure GCP external IP.",
    "route": "Configure GCP route.",
    "gcp-project-list": "Configure GCP project list.",
    "forwarding-rule": "Configure GCP forwarding rule.",
    "service-account": "GCP service account email.",
    "private-key": "Private key of GCP service account.",
    "secret-token": "Secret token of Kubernetes service account.",
    "domain": "Domain name.",
    "group-name": "Full path group name of computers.",
    "server-cert": "Trust servers that contain this certificate only.",
    "server-ca-cert": "Trust only those servers whose certificate is directly/indirectly signed by this certificate.",
    "api-key": "IBM cloud API key or service ID API key.",
    "ibm-region": "IBM cloud region name.",
    "par-id": "Public address range ID.",
    "update-interval": "Dynamic object update interval (30 - 3600 sec, default = 60, 0 = disabled).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "proxy": {"type": "string", "max_length": 35},
    "vdom": {"type": "string", "max_length": 31},
    "server": {"type": "string", "max_length": 127},
    "server-port": {"type": "integer", "min": 0, "max": 65535},
    "message-server-port": {"type": "integer", "min": 0, "max": 65535},
    "username": {"type": "string", "max_length": 64},
    "vcenter-server": {"type": "string", "max_length": 127},
    "vcenter-username": {"type": "string", "max_length": 64},
    "access-key": {"type": "string", "max_length": 31},
    "region": {"type": "string", "max_length": 31},
    "vpc-id": {"type": "string", "max_length": 31},
    "tenant-id": {"type": "string", "max_length": 127},
    "client-id": {"type": "string", "max_length": 63},
    "subscription-id": {"type": "string", "max_length": 63},
    "resource-group": {"type": "string", "max_length": 63},
    "login-endpoint": {"type": "string", "max_length": 127},
    "resource-url": {"type": "string", "max_length": 127},
    "user-id": {"type": "string", "max_length": 127},
    "oci-cert": {"type": "string", "max_length": 63},
    "oci-fingerprint": {"type": "string", "max_length": 63},
    "service-account": {"type": "string", "max_length": 127},
    "domain": {"type": "string", "max_length": 127},
    "group-name": {"type": "string", "max_length": 127},
    "server-cert": {"type": "string", "max_length": 127},
    "server-ca-cert": {"type": "string", "max_length": 127},
    "par-id": {"type": "string", "max_length": 63},
    "update-interval": {"type": "integer", "min": 0, "max": 3600},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "server-list": {
        "ip": {
            "type": "string",
            "help": "IPv4 address.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
    },
    "external-account-list": {
        "role-arn": {
            "type": "string",
            "help": "AWS role ARN to assume.",
            "required": True,
            "default": "",
            "max_length": 2047,
        },
        "external-id": {
            "type": "string",
            "help": "AWS external ID.",
            "default": "",
            "max_length": 1399,
        },
        "region-list": {
            "type": "string",
            "help": "AWS region name list.",
            "required": True,
        },
    },
    "nic": {
        "name": {
            "type": "string",
            "help": "Network interface name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "peer-nic": {
            "type": "string",
            "help": "Peer network interface name.",
            "default": "",
            "max_length": 63,
        },
        "ip": {
            "type": "string",
            "help": "Configure IP configuration.",
        },
    },
    "route-table": {
        "name": {
            "type": "string",
            "help": "Route table name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "subscription-id": {
            "type": "string",
            "help": "Subscription ID of Azure route table.",
            "default": "",
            "max_length": 63,
        },
        "resource-group": {
            "type": "string",
            "help": "Resource group of Azure route table.",
            "default": "",
            "max_length": 63,
        },
        "route": {
            "type": "string",
            "help": "Configure Azure route.",
        },
    },
    "compartment-list": {
        "compartment-id": {
            "type": "string",
            "help": "OCI compartment ID.",
            "required": True,
            "default": "",
            "max_length": 127,
        },
    },
    "oci-region-list": {
        "region": {
            "type": "string",
            "help": "OCI region.",
            "required": True,
            "default": "",
            "max_length": 31,
        },
    },
    "external-ip": {
        "name": {
            "type": "string",
            "help": "External IP name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
    },
    "route": {
        "name": {
            "type": "string",
            "help": "Route name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
    },
    "gcp-project-list": {
        "id": {
            "type": "string",
            "help": "GCP project ID.",
            "required": True,
            "default": "",
            "max_length": 127,
        },
        "gcp-zone-list": {
            "type": "string",
            "help": "Configure GCP zone list.",
        },
    },
    "forwarding-rule": {
        "rule-name": {
            "type": "string",
            "help": "Forwarding rule name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "target": {
            "type": "string",
            "help": "Target instance name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_TYPE = [
    "aci",
    "alicloud",
    "aws",
    "azure",
    "gcp",
    "nsx",
    "nuage",
    "oci",
    "openstack",
    "kubernetes",
    "vmware",
    "sepm",
    "aci-direct",
    "ibm",
    "nutanix",
    "sap",
]
VALID_BODY_USE_METADATA_IAM = [
    "disable",
    "enable",
]
VALID_BODY_MICROSOFT_365 = [
    "disable",
    "enable",
]
VALID_BODY_HA_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_VERIFY_CERTIFICATE = [
    "disable",
    "enable",
]
VALID_BODY_ALT_RESOURCE_IP = [
    "disable",
    "enable",
]
VALID_BODY_AZURE_REGION = [
    "global",
    "china",
    "germany",
    "usgov",
    "local",
]
VALID_BODY_OCI_REGION_TYPE = [
    "commercial",
    "government",
]
VALID_BODY_IBM_REGION = [
    "dallas",
    "washington-dc",
    "london",
    "frankfurt",
    "sydney",
    "tokyo",
    "osaka",
    "toronto",
    "sao-paulo",
    "madrid",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_sdn_connector_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/sdn_connector."""
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


def validate_system_sdn_connector_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/sdn_connector object."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-metadata-iam" in payload:
        is_valid, error = _validate_enum_field(
            "use-metadata-iam",
            payload["use-metadata-iam"],
            VALID_BODY_USE_METADATA_IAM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "microsoft-365" in payload:
        is_valid, error = _validate_enum_field(
            "microsoft-365",
            payload["microsoft-365"],
            VALID_BODY_MICROSOFT_365,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-status" in payload:
        is_valid, error = _validate_enum_field(
            "ha-status",
            payload["ha-status"],
            VALID_BODY_HA_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "verify-certificate" in payload:
        is_valid, error = _validate_enum_field(
            "verify-certificate",
            payload["verify-certificate"],
            VALID_BODY_VERIFY_CERTIFICATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "alt-resource-ip" in payload:
        is_valid, error = _validate_enum_field(
            "alt-resource-ip",
            payload["alt-resource-ip"],
            VALID_BODY_ALT_RESOURCE_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "azure-region" in payload:
        is_valid, error = _validate_enum_field(
            "azure-region",
            payload["azure-region"],
            VALID_BODY_AZURE_REGION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "oci-region-type" in payload:
        is_valid, error = _validate_enum_field(
            "oci-region-type",
            payload["oci-region-type"],
            VALID_BODY_OCI_REGION_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ibm-region" in payload:
        is_valid, error = _validate_enum_field(
            "ibm-region",
            payload["ibm-region"],
            VALID_BODY_IBM_REGION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_sdn_connector_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/sdn_connector."""
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
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-metadata-iam" in payload:
        is_valid, error = _validate_enum_field(
            "use-metadata-iam",
            payload["use-metadata-iam"],
            VALID_BODY_USE_METADATA_IAM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "microsoft-365" in payload:
        is_valid, error = _validate_enum_field(
            "microsoft-365",
            payload["microsoft-365"],
            VALID_BODY_MICROSOFT_365,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-status" in payload:
        is_valid, error = _validate_enum_field(
            "ha-status",
            payload["ha-status"],
            VALID_BODY_HA_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "verify-certificate" in payload:
        is_valid, error = _validate_enum_field(
            "verify-certificate",
            payload["verify-certificate"],
            VALID_BODY_VERIFY_CERTIFICATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "alt-resource-ip" in payload:
        is_valid, error = _validate_enum_field(
            "alt-resource-ip",
            payload["alt-resource-ip"],
            VALID_BODY_ALT_RESOURCE_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "azure-region" in payload:
        is_valid, error = _validate_enum_field(
            "azure-region",
            payload["azure-region"],
            VALID_BODY_AZURE_REGION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "oci-region-type" in payload:
        is_valid, error = _validate_enum_field(
            "oci-region-type",
            payload["oci-region-type"],
            VALID_BODY_OCI_REGION_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ibm-region" in payload:
        is_valid, error = _validate_enum_field(
            "ibm-region",
            payload["ibm-region"],
            VALID_BODY_IBM_REGION,
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
    "endpoint": "system/sdn_connector",
    "category": "cmdb",
    "api_path": "system/sdn-connector",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure connection to SDN Connector.",
    "total_fields": 55,
    "required_fields_count": 11,
    "fields_with_defaults_count": 40,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
