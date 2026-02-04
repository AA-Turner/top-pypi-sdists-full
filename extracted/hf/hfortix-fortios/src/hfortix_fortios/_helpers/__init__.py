"""
Central helpers module for hfortix_fortios package.

This module consolidates all helper functions used across the package:
- API endpoints (hfortix_fortios.api.v2.cmdb.*, monitor.*)
- Convenience wrappers (hfortix_fortios.firewall.*)
- Future modules (system, user, router, etc.)

Organized into logical submodules:
- builders: Payload building (build_cmdb_payload,
    build_cmdb_payload_normalized)
- normalizers: List normalization (normalize_to_name_list,
    normalize_member_list)
- validators: All validation functions (generic + domain-specific)
- converters: Type conversion and data cleaning
- response: Response parsing helpers


Import from this module for consistency across the codebase:
    from hfortix_fortios._helpers import build_cmdb_payload, validate_color
"""

# Payload builders
from hfortix_fortios._helpers.builders import (
    build_api_payload,
    build_cmdb_payload,
    build_cmdb_payload_normalized,
)

# Data converters and cleaners
from hfortix_fortios._helpers.converters import (
    convert_boolean_to_str,
    filter_empty_values,
    quote_path_param,
)

# Metadata accessors (shared by all validator modules)
from hfortix_fortios._helpers.metadata import (
    get_all_fields,
    get_field_constraints,
    get_field_default,
    get_field_description,
    get_field_metadata,
    get_field_options,
    get_field_type,
    get_nested_schema,
    validate_field_value,
)

# Metadata mixin for endpoint classes
from hfortix_fortios._helpers.metadata_mixin import MetadataMixin

# List normalizers
from hfortix_fortios._helpers.normalizers import (
    normalize_day_field,
    normalize_member_list,
    normalize_table_field,
    normalize_to_name_list,
    normalize_to_string_list,
)

# Response helpers
from hfortix_fortios._helpers.response import (
    get_mkey,
    get_name,
    get_results,
    is_success,
)

# Central validation functions (used by all endpoint validators)
from hfortix_fortios._helpers.validation import (
    validate_enum_field,
    validate_multiple_enums,
    validate_multiple_query_params,
    validate_query_parameter,
)
from hfortix_fortios._helpers.validation import (
    validate_required_fields as _validate_required_fields_central,
)

# Validators - SSH/SSL proxy-specific
# Validators - Firewall-specific
# Validators - Generic
from hfortix_fortios._helpers.validators import (
    validate_address_pairs,
    validate_color,
    validate_day_names,
    validate_enable_disable,
    validate_integer_range,
    validate_ip_address,
    validate_ip_network,
    validate_ipv6_address,
    validate_mac_address,
    validate_policy_id,
    validate_port_number,
    validate_required_fields,
    validate_schedule_name,
    validate_seq_num,
    validate_ssh_host_key_nid,
    validate_ssh_host_key_status,
    validate_ssh_host_key_type,
    validate_ssh_host_key_usage,
    validate_ssh_source,
    validate_ssl_cipher_action,
    validate_ssl_dh_bits,
    validate_status,
    validate_string_length,
    validate_time_format,
)

__all__ = [
    # Payload building
    "build_api_payload",
    "build_cmdb_payload",
    "build_cmdb_payload_normalized",
    # List normalization
    "normalize_to_name_list",
    "normalize_member_list",
    "normalize_table_field",
    "normalize_to_string_list",
    # Data cleaning and conversion
    "filter_empty_values",
    "convert_boolean_to_str",
    "quote_path_param",
    # Response helpers
    "get_name",
    "get_mkey",  # Alias for backward compatibility
    "get_results",
    "is_success",
    # Metadata accessors
    "get_field_description",
    "get_field_type",
    "get_field_constraints",
    "get_field_default",
    "get_field_options",
    "get_nested_schema",
    "get_all_fields",
    "get_field_metadata",
    "validate_field_value",
    # Metadata mixin
    "MetadataMixin",
    # Central validation functions
    "_validate_required_fields_central",
    "validate_enum_field",
    "validate_query_parameter",
    "validate_multiple_enums",
    "validate_multiple_query_params",
    # Validation - Generic
    "validate_required_fields",
    "validate_color",
    "validate_status",
    "validate_mac_address",
    "validate_ip_address",
    "validate_ipv6_address",
    "validate_ip_network",
    "validate_string_length",
    "validate_integer_range",
    "validate_port_number",
    "validate_enable_disable",
    # Validation - Firewall-specific
    "validate_policy_id",
    "validate_address_pairs",
    "validate_seq_num",
    "validate_schedule_name",
    "validate_time_format",
    "validate_day_names",
    # Validation - SSH/SSL proxy-specific
    "validate_ssh_host_key_type",
    "validate_ssh_host_key_status",
    "validate_ssh_host_key_nid",
    "validate_ssh_host_key_usage",
    "validate_ssh_source",
    "validate_ssl_dh_bits",
    "validate_ssl_cipher_action",
]
