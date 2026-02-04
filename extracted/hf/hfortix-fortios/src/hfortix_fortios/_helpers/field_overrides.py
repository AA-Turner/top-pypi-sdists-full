"""
Field name conversion overrides for FortiOS API

This module defines exceptions and mappings for field name conversions when
communicating with the FortiOS API. Centralizes all field name handling rules
to ensure consistency across the library.

These overrides are used in two places:
1. Payload builders (_helpers/builders.py) - when building request payloads
2. Client wrapper (client.py) - when converting field names before sending

Version History:
- v0.5.129: AUTO-GENERATED body field lists - Scanned all schemas to find fields with underscores
  - CMDB: 4 body fields with underscores in API (block_ack_flood, etc.)
  - Monitor: 200 request body fields with underscores in API (id_list, file_content, etc.)
  - This fixes id_list bug and ensures all underscore fields are preserved correctly
- v0.5.128: MAJOR REFACTOR - Separate query param vs body field whitelists per API type
  - Split NO_HYPHEN_PARAMETERS into context-specific lists (query vs body)
  - Each API type (CMDB, Monitor, Log, Service) now has two separate lists
  - Enables proper handling of dual-context parameters (used as both query AND body)
  - Body fields now correctly convert to hyphens, query params preserve underscores
- v0.5.127: Fixed ems_id bug - removed from NO_HYPHEN_PARAMETERS (needs ems-id in CMDB)
- v0.5.127: Cleaned up NO_HYPHEN_PARAMETERS - removed 97 incorrect entries (211 → 113)
- v0.5.126: Split NO_HYPHEN_PARAMETERS by API type (cmdb/monitor/log/service)
- v0.5.122: Added file_content and key_file_content (bug fix for file upload endpoints)
- v0.5.122: Centralized PYTHON_KEYWORD_TO_API_FIELD mapping

ARCHITECTURE (v0.5.128):
This module now provides context-specific parameter preservation lists:

For each API type, there are TWO separate lists:
  1. *_QUERY_PARAM_NO_HYPHEN: Query/path parameters that must keep underscores
  2. *_BODY_FIELD_NO_HYPHEN: Body fields that exceptionally keep underscores (rare!)

This enables proper handling of parameters used in BOTH contexts:
  - Example: ip_version
    - As query param: ?ip_version=4 (underscore preserved)
    - As body field: {"ip-version": 4} (converted to hyphen)

Usage in payload builders:
  - build_cmdb_payload(): Uses CMDB_BODY_FIELD_NO_HYPHEN
  - build_api_payload(): Uses MONITOR_BODY_FIELD_NO_HYPHEN (for Monitor/Service)
  - Query param building: Uses *_QUERY_PARAM_NO_HYPHEN lists
"""

# Python keyword to API field name mapping
# The generator renames Python keywords to avoid conflicts (e.g., 'as' → 'asn')
# This mapping reverses that transformation when sending to the API
#
# IMPORTANT: This is a reverse mapping - Python parameter name → API field name
#
# Examples:
#   asn="65000" → {"as": "65000"} (reverse Python keyword rename)
#   class_=[...] → {"class": [...]} (reverse trailing underscore)
#   router_id="1.1.1.1" → {"router-id": "1.1.1.1"} (normal snake→kebab)
PYTHON_KEYWORD_TO_API_FIELD = {
    "asn": "as",            # BGP AS number (Python keyword 'as' → 'asn')
    "class_": "class",      # Class fields (Python keyword 'class' → 'class_')
    "type_": "type",        # Type fields (Python keyword 'type' → 'type_')
    "from_": "from",        # From fields (Python keyword 'from' → 'from_')
    "import_": "import",    # Import fields (Python keyword 'import' → 'import_')
    "global_": "global",    # Global fields (Python keyword 'global' → 'global_')
    # Add more as discovered in schemas
}

# ============================================================================
# CMDB API - Parameter Preservation Lists
# ============================================================================

# CMDB query/path parameters that must preserve underscores
CMDB_QUERY_PARAM_NO_HYPHEN = {
    "datasource_format",   # Query param for data source format selection
    "find_all_references", # Query param to include reference checking
    "primary_keys",        # Query param for filtering by primary keys
    "skip_to",             # Query param for pagination (skip to N-th item)
    "unfiltered_count",    # Query param to get total count without filters
    "with_contents_hash",  # Query param to include content hash in response
    "with_meta",           # Query param to include metadata in response
}

# CMDB body fields that must preserve underscores (RARE - most convert to hyphens!)
# Only add here if FortiOS API definitively expects underscores in request body
# Generated from schema analysis - 4 fields found with underscores in API
CMDB_BODY_FIELD_NO_HYPHEN = {
    "block_ack_flood",
    "block_ack_flood_thresh",
    "block_ack_flood_time",
    "switch_dhcp_opt43_key",
}

# ============================================================================
# Monitor API - Parameter Preservation Lists
# ============================================================================

# Monitor query/path parameters that must preserve underscores
MONITOR_QUERY_PARAM_NO_HYPHEN = {
    "all_vdoms",
    "ap_interface",
    "auth_type",
    "cache_query",
    "chart_only",
    "child_path",
    "city_id",
    "client_name",
    "config_id",
    "convert_unrated_id",
    "count_only",
    "country_code",
    "country_id",
    "counts_only",
    "destination_port",
    "dst_uuid",
    "filter_logic",
    "group_attr_type",
    "group_name",
    "health_check_name",
    "incl_local",
    "include_aggregate",
    "include_dynamic",
    "include_fsso",
    "include_ha",
    "include_hit_only",
    "include_notes",
    "include_sla_targets_met",
    "include_ttl",
    "include_unrated",
    "include_vlan",
    "indoor_outdoor",
    "interface_name",
    "intf_name",
    "ip_address",
    "ip_mask",
    "ip_version",
    "ips_sensor",
    "ipv4_mask",
    "ipv6_only",
    "ipv6_prefix",
    "is_ipv6",
    "is_tier2",
    "key_only",
    "lang_name",
    "ldap_filter",
    "mac_address",
    "managed_ssid_only",
    "max_age",
    "min_age",
    "min_sample_interval",
    "min_version",
    "parent_peer1",
    "parent_peer2",
    "path_name",
    "platform_type",
    "policy_type",
    "port_ranges",
    "protocol_number",
    "q_name",
    "q_path",
    "query_id",
    "query_type",
    "region_id",
    "region_name",
    "report_by",
    "report_name",
    "report_type",
    "sampling_interval",
    "search_tables",
    "serial_no",
    "server_info_only",
    "server_name",
    "service_type",
    "session_id",
    "shaper_name",
    "skip_detect",
    "skip_eos",
    "skip_schema",
    "skip_tables",
    "skip_vpn_child",
    "sort_by",
    "source_port",
    "src_uuid",
    "status_only",
    "summary_only",
    "time_period",
    "timestamp_from",
    "timestamp_to",
    "total_only",
    "update_cache",
    "user_db",
    "user_group",
    "user_name",
    "vcluster_id",
    "vdom_name",
    "view_type",
    "with_ca",
    "with_cert",
    "with_crl",
    "with_remote",
    "with_stats",
    "with_triangulation",
    "wtp_id",
}

# Monitor body fields that must preserve underscores (RARE - most convert to hyphens!)
# Only add here if FortiOS API definitively expects underscores in request body
# Generated from schema analysis - 200 fields found with underscores in API
MONITOR_BODY_FIELD_NO_HYPHEN = {
    "account_id",
    "account_password",
    "acme_ca_url",
    "acme_domain",
    "acme_email",
    "acme_renew_window",
    "acme_rsa_key_size",
    "addr_from",
    "addr_to",
    "agent_ip",
    "agreement_accepted",
    "all_vdoms",
    "ap_interface",
    "application_error",
    "application_id",
    "application_name",
    "apply_to",
    "auth_type",
    "cache_query",
    "chart_only",
    "check_status_only",
    "child_path",
    "city_id",
    "client_name",
    "common_name",
    "config_id",
    "config_ids",
    "confirm_not_ga_certified",
    "confirm_not_signed",
    "confirm_password_mask",
    "count_only",
    "country_code",
    "country_id",
    "counts_only",
    "cteid_addr",
    "cteid_addr6",
    "daddr_from",
    "daddr_to",
    "db_name",
    "destination_port",
    "dport_from",
    "dport_to",
    "dst_uuid",
    "ems_id",
    "end_vlan_id",
    "endpoint_ip",
    "event_log_message",
    "file_content",
    "file_format",
    "file_id",
    "filter_logic",
    "find_all_references",
    "first_name",
    "format_partition",
    "fteid_addr",
    "fteid_addr6",
    "group_attr_type",
    "group_name",
    "gtp_profile",
    "health_check_name",
    "id_list",
    "ignore_admin_lockout_upon_downgrade",
    "ignore_invalid_signature",
    "image_id",
    "image_type",
    "import_method",
    "incl_local",
    "include_aggregate",
    "include_dynamic",
    "include_fsso",
    "include_ha",
    "include_notes",
    "include_sla_targets_met",
    "include_ttl",
    "include_vlan",
    "indoor_outdoor",
    "industry_id",
    "interface_name",
    "intf_name",
    "ip_address",
    "ip_addresses",
    "ip_mask",
    "ip_version",
    "ips_sensor",
    "ipv4_mask",
    "ipv6_only",
    "ipv6_prefix",
    "is_government",
    "is_ipv6",
    "is_tier2",
    "isl_port_group",
    "key_file_content",
    "key_length",
    "key_only",
    "lang_comments",
    "lang_name",
    "last_connection_time",
    "last_name",
    "last_update_time",
    "ldap_filter",
    "license_key",
    "mac_address",
    "managed_ssid_only",
    "max_age",
    "mgmt_ip",
    "mgmt_port",
    "mgmt_url_parameters",
    "min_age",
    "min_sample_interval",
    "min_version",
    "mpsk_profile",
    "ms_addr",
    "ms_addr6",
    "new_password",
    "num_packets",
    "old_email",
    "old_password",
    "orgsize_id",
    "packet_loss",
    "parent_peer1",
    "parent_peer2",
    "password_mask",
    "path_name",
    "platform_type",
    "policy_type",
    "port_from",
    "port_ranges",
    "port_to",
    "postal_code",
    "protocol_number",
    "protocol_option",
    "proxy_url",
    "q_name",
    "q_path",
    "query_id",
    "query_type",
    "radio_id",
    "region_id",
    "region_name",
    "registration_code",
    "remote_script",
    "report_by",
    "report_name",
    "reseller_id",
    "reseller_name",
    "saddr_from",
    "saddr_to",
    "sampling_interval",
    "scep_ca_id",
    "scep_password",
    "scep_url",
    "search_tables",
    "secureon_password",
    "send_logs",
    "serial_no",
    "server_info_only",
    "server_name",
    "service_type",
    "session_id",
    "shaper_name",
    "skip_detect",
    "skip_eos",
    "skip_schema",
    "skip_tables",
    "skip_vpn_child",
    "sms_phone",
    "sort_by",
    "source_ip",
    "source_port",
    "sport_from",
    "sport_to",
    "src_uuid",
    "start_vlan_id",
    "state_code",
    "status_only",
    "subject_alt_name",
    "summary_only",
    "switch_id",
    "switch_ids",
    "time_period",
    "timestamp_from",
    "timestamp_to",
    "total_only",
    "update_cache",
    "usb_filename",
    "user_db",
    "user_group",
    "user_name",
    "user_type",
    "vcluster_id",
    "vdom_name",
    "view_level",
    "view_type",
    "with_ca",
    "with_cert",
    "with_crl",
    "with_remote",
    "with_stats",
    "with_triangulation",
    "wtp_id",
}

# ============================================================================
# Log API - Parameter Preservation Lists
# ============================================================================

# Log query/path parameters that must preserve underscores
LOG_QUERY_PARAM_NO_HYPHEN = {
    "filter_logic",
    "is_ha_member",
    "keep_session_alive",
    "serial_no",
    "session_id",
    "timestamp_from",
    "timestamp_to",
}

# Log body fields that must preserve underscores
LOG_BODY_FIELD_NO_HYPHEN = set()

# ============================================================================
# Service API - Parameter Preservation Lists
# ============================================================================

# Service query/path parameters that must preserve underscores
SERVICE_QUERY_PARAM_NO_HYPHEN = set()

# Service body fields that must preserve underscores
SERVICE_BODY_FIELD_NO_HYPHEN = set()

# ============================================================================
# Backward Compatibility - Unified Lists (DEPRECATED in v0.5.128)
# ============================================================================
# These are maintained for backward compatibility but should not be used in new code
# Use the context-specific lists above instead

# Parameters that must preserve underscores for CMDB endpoints
# DEPRECATED: Use CMDB_QUERY_PARAM_NO_HYPHEN or CMDB_BODY_FIELD_NO_HYPHEN instead
NO_HYPHEN_PARAMETERS_CMDB = CMDB_QUERY_PARAM_NO_HYPHEN | CMDB_BODY_FIELD_NO_HYPHEN

# Parameters that must preserve underscores for Monitor endpoints
# DEPRECATED: Use MONITOR_QUERY_PARAM_NO_HYPHEN or MONITOR_BODY_FIELD_NO_HYPHEN instead
NO_HYPHEN_PARAMETERS_MONITOR = MONITOR_QUERY_PARAM_NO_HYPHEN | MONITOR_BODY_FIELD_NO_HYPHEN

# Parameters that must preserve underscores for Log endpoints
# DEPRECATED: Use LOG_QUERY_PARAM_NO_HYPHEN or LOG_BODY_FIELD_NO_HYPHEN instead
NO_HYPHEN_PARAMETERS_LOG = LOG_QUERY_PARAM_NO_HYPHEN | LOG_BODY_FIELD_NO_HYPHEN

# Parameters that must preserve underscores for Service endpoints
# Currently empty - service endpoints don't have query-only underscore params yet
NO_HYPHEN_PARAMETERS_SERVICE = SERVICE_QUERY_PARAM_NO_HYPHEN | SERVICE_BODY_FIELD_NO_HYPHEN

# Parameters that must preserve underscores for Service endpoints
# Currently empty - service endpoints don't have underscore params yet
NO_HYPHEN_PARAMETERS_SERVICE = set()

# Unified set for backwards compatibility and general use
# Union of all API-specific sets
NO_HYPHEN_PARAMETERS = (
    NO_HYPHEN_PARAMETERS_CMDB |
    NO_HYPHEN_PARAMETERS_MONITOR |
    NO_HYPHEN_PARAMETERS_LOG |
    NO_HYPHEN_PARAMETERS_SERVICE
)

__all__ = [
    "PYTHON_KEYWORD_TO_API_FIELD",
    # Context-specific lists (v0.5.128+)
    "CMDB_QUERY_PARAM_NO_HYPHEN",
    "CMDB_BODY_FIELD_NO_HYPHEN",
    "MONITOR_QUERY_PARAM_NO_HYPHEN",
    "MONITOR_BODY_FIELD_NO_HYPHEN",
    "LOG_QUERY_PARAM_NO_HYPHEN",
    "LOG_BODY_FIELD_NO_HYPHEN",
    "SERVICE_QUERY_PARAM_NO_HYPHEN",
    "SERVICE_BODY_FIELD_NO_HYPHEN",
    # Backward compatibility (deprecated)
    "NO_HYPHEN_PARAMETERS",
    "NO_HYPHEN_PARAMETERS_CMDB",
    "NO_HYPHEN_PARAMETERS_MONITOR",
    "NO_HYPHEN_PARAMETERS_LOG",
    "NO_HYPHEN_PARAMETERS_SERVICE",
]
