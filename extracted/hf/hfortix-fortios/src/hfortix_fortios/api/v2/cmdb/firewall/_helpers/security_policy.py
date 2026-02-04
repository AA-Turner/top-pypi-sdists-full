"""Validation helpers for firewall/security_policy - Auto-generated"""

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
    "srcintf",  # Incoming (ingress) interface.
    "dstintf",  # Outgoing (egress) interface.
    "schedule",  # Schedule name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "uuid": "00000000-0000-0000-0000-000000000000",
    "policyid": 0,
    "name": "",
    "srcaddr-negate": "disable",
    "dstaddr-negate": "disable",
    "srcaddr6-negate": "disable",
    "dstaddr6-negate": "disable",
    "internet-service": "disable",
    "internet-service-negate": "disable",
    "internet-service-src": "disable",
    "internet-service-src-negate": "disable",
    "internet-service6": "disable",
    "internet-service6-negate": "disable",
    "internet-service6-src": "disable",
    "internet-service6-src-negate": "disable",
    "enforce-default-app-port": "enable",
    "service-negate": "disable",
    "action": "deny",
    "send-deny-packet": "disable",
    "schedule": "",
    "status": "enable",
    "logtraffic": "utm",
    "learning-mode": "disable",
    "nat46": "disable",
    "nat64": "disable",
    "profile-type": "single",
    "profile-group": "",
    "profile-protocol-options": "default",
    "ssl-ssh-profile": "no-inspection",
    "av-profile": "",
    "webfilter-profile": "",
    "dnsfilter-profile": "",
    "emailfilter-profile": "",
    "dlp-profile": "",
    "file-filter-profile": "",
    "ips-sensor": "",
    "application-list": "",
    "voip-profile": "",
    "ips-voip-filter": "",
    "sctp-filter-profile": "",
    "diameter-filter-profile": "",
    "virtual-patch-profile": "",
    "icap-profile": "",
    "videofilter-profile": "",
    "ssh-filter-profile": "",
    "casb-profile": "",
    "url-category": "",
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
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned but can be manually 
    "policyid": "integer",  # Policy ID.
    "name": "string",  # Policy name.
    "comments": "var-string",  # Comment.
    "srcintf": "string",  # Incoming (ingress) interface.
    "dstintf": "string",  # Outgoing (egress) interface.
    "srcaddr": "string",  # Source IPv4 address name and address group names.
    "srcaddr-negate": "option",  # When enabled srcaddr specifies what the source address must NOT be.
    "dstaddr": "string",  # Destination IPv4 address name and address group names.
    "dstaddr-negate": "option",  # When enabled dstaddr specifies what the destination address must NOT be.
    "srcaddr6": "string",  # Source IPv6 address name and address group names.
    "srcaddr6-negate": "option",  # When enabled srcaddr6 specifies what the source address must NOT be.
    "dstaddr6": "string",  # Destination IPv6 address name and address group names.
    "dstaddr6-negate": "option",  # When enabled dstaddr6 specifies what the destination address must NOT be.
    "internet-service": "option",  # Enable/disable use of Internet Services for this policy. If enabled, destination
    "internet-service-name": "string",  # Internet Service name.
    "internet-service-negate": "option",  # When enabled internet-service specifies what the service must NOT be.
    "internet-service-group": "string",  # Internet Service group name.
    "internet-service-custom": "string",  # Custom Internet Service name.
    "internet-service-custom-group": "string",  # Custom Internet Service group name.
    "internet-service-fortiguard": "string",  # FortiGuard Internet Service name.
    "internet-service-src": "option",  # Enable/disable use of Internet Services in source for this policy. If enabled, s
    "internet-service-src-name": "string",  # Internet Service source name.
    "internet-service-src-negate": "option",  # When enabled internet-service-src specifies what the service must NOT be.
    "internet-service-src-group": "string",  # Internet Service source group name.
    "internet-service-src-custom": "string",  # Custom Internet Service source name.
    "internet-service-src-custom-group": "string",  # Custom Internet Service source group name.
    "internet-service-src-fortiguard": "string",  # FortiGuard Internet Service source name.
    "internet-service6": "option",  # Enable/disable use of IPv6 Internet Services for this policy. If enabled, destin
    "internet-service6-name": "string",  # IPv6 Internet Service name.
    "internet-service6-negate": "option",  # When enabled internet-service6 specifies what the service must NOT be.
    "internet-service6-group": "string",  # Internet Service group name.
    "internet-service6-custom": "string",  # Custom IPv6 Internet Service name.
    "internet-service6-custom-group": "string",  # Custom IPv6 Internet Service group name.
    "internet-service6-fortiguard": "string",  # FortiGuard IPv6 Internet Service name.
    "internet-service6-src": "option",  # Enable/disable use of IPv6 Internet Services in source for this policy. If enabl
    "internet-service6-src-name": "string",  # IPv6 Internet Service source name.
    "internet-service6-src-negate": "option",  # When enabled internet-service6-src specifies what the service must NOT be.
    "internet-service6-src-group": "string",  # Internet Service6 source group name.
    "internet-service6-src-custom": "string",  # Custom IPv6 Internet Service source name.
    "internet-service6-src-custom-group": "string",  # Custom Internet Service6 source group name.
    "internet-service6-src-fortiguard": "string",  # FortiGuard IPv6 Internet Service source name.
    "enforce-default-app-port": "option",  # Enable/disable default application port enforcement for allowed applications.
    "service": "string",  # Service and service group names.
    "service-negate": "option",  # When enabled service specifies what the service must NOT be.
    "action": "option",  # Policy action (accept/deny).
    "send-deny-packet": "option",  # Enable to send a reply when a session is denied or blocked by a firewall policy.
    "schedule": "string",  # Schedule name.
    "status": "option",  # Enable or disable this policy.
    "logtraffic": "option",  # Enable or disable logging. Log all sessions or security profile sessions.
    "learning-mode": "option",  # Enable to allow everything, but log all of the meaningful data for security info
    "nat46": "option",  # Enable/disable NAT46.
    "nat64": "option",  # Enable/disable NAT64.
    "profile-type": "option",  # Determine whether the firewall policy allows security profile groups or single p
    "profile-group": "string",  # Name of profile group.
    "profile-protocol-options": "string",  # Name of an existing Protocol options profile.
    "ssl-ssh-profile": "string",  # Name of an existing SSL SSH profile.
    "av-profile": "string",  # Name of an existing Antivirus profile.
    "webfilter-profile": "string",  # Name of an existing Web filter profile.
    "dnsfilter-profile": "string",  # Name of an existing DNS filter profile.
    "emailfilter-profile": "string",  # Name of an existing email filter profile.
    "dlp-profile": "string",  # Name of an existing DLP profile.
    "file-filter-profile": "string",  # Name of an existing file-filter profile.
    "ips-sensor": "string",  # Name of an existing IPS sensor.
    "application-list": "string",  # Name of an existing Application list.
    "voip-profile": "string",  # Name of an existing VoIP (voipd) profile.
    "ips-voip-filter": "string",  # Name of an existing VoIP (ips) profile.
    "sctp-filter-profile": "string",  # Name of an existing SCTP filter profile.
    "diameter-filter-profile": "string",  # Name of an existing Diameter filter profile.
    "virtual-patch-profile": "string",  # Name of an existing virtual-patch profile.
    "icap-profile": "string",  # Name of an existing ICAP profile.
    "videofilter-profile": "string",  # Name of an existing VideoFilter profile.
    "ssh-filter-profile": "string",  # Name of an existing SSH filter profile.
    "casb-profile": "string",  # Name of an existing CASB profile.
    "application": "string",  # Application ID list.
    "app-category": "string",  # Application category ID list.
    "url-category": "user",  # URL categories or groups.
    "app-group": "string",  # Application group names.
    "groups": "string",  # Names of user groups that can authenticate with this policy.
    "users": "string",  # Names of individual users that can authenticate with this policy.
    "fsso-groups": "string",  # Names of FSSO groups.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "policyid": "Policy ID.",
    "name": "Policy name.",
    "comments": "Comment.",
    "srcintf": "Incoming (ingress) interface.",
    "dstintf": "Outgoing (egress) interface.",
    "srcaddr": "Source IPv4 address name and address group names.",
    "srcaddr-negate": "When enabled srcaddr specifies what the source address must NOT be.",
    "dstaddr": "Destination IPv4 address name and address group names.",
    "dstaddr-negate": "When enabled dstaddr specifies what the destination address must NOT be.",
    "srcaddr6": "Source IPv6 address name and address group names.",
    "srcaddr6-negate": "When enabled srcaddr6 specifies what the source address must NOT be.",
    "dstaddr6": "Destination IPv6 address name and address group names.",
    "dstaddr6-negate": "When enabled dstaddr6 specifies what the destination address must NOT be.",
    "internet-service": "Enable/disable use of Internet Services for this policy. If enabled, destination address, service and default application port enforcement are not used.",
    "internet-service-name": "Internet Service name.",
    "internet-service-negate": "When enabled internet-service specifies what the service must NOT be.",
    "internet-service-group": "Internet Service group name.",
    "internet-service-custom": "Custom Internet Service name.",
    "internet-service-custom-group": "Custom Internet Service group name.",
    "internet-service-fortiguard": "FortiGuard Internet Service name.",
    "internet-service-src": "Enable/disable use of Internet Services in source for this policy. If enabled, source address is not used.",
    "internet-service-src-name": "Internet Service source name.",
    "internet-service-src-negate": "When enabled internet-service-src specifies what the service must NOT be.",
    "internet-service-src-group": "Internet Service source group name.",
    "internet-service-src-custom": "Custom Internet Service source name.",
    "internet-service-src-custom-group": "Custom Internet Service source group name.",
    "internet-service-src-fortiguard": "FortiGuard Internet Service source name.",
    "internet-service6": "Enable/disable use of IPv6 Internet Services for this policy. If enabled, destination address, service and default application port enforcement are not used.",
    "internet-service6-name": "IPv6 Internet Service name.",
    "internet-service6-negate": "When enabled internet-service6 specifies what the service must NOT be.",
    "internet-service6-group": "Internet Service group name.",
    "internet-service6-custom": "Custom IPv6 Internet Service name.",
    "internet-service6-custom-group": "Custom IPv6 Internet Service group name.",
    "internet-service6-fortiguard": "FortiGuard IPv6 Internet Service name.",
    "internet-service6-src": "Enable/disable use of IPv6 Internet Services in source for this policy. If enabled, source address is not used.",
    "internet-service6-src-name": "IPv6 Internet Service source name.",
    "internet-service6-src-negate": "When enabled internet-service6-src specifies what the service must NOT be.",
    "internet-service6-src-group": "Internet Service6 source group name.",
    "internet-service6-src-custom": "Custom IPv6 Internet Service source name.",
    "internet-service6-src-custom-group": "Custom Internet Service6 source group name.",
    "internet-service6-src-fortiguard": "FortiGuard IPv6 Internet Service source name.",
    "enforce-default-app-port": "Enable/disable default application port enforcement for allowed applications.",
    "service": "Service and service group names.",
    "service-negate": "When enabled service specifies what the service must NOT be.",
    "action": "Policy action (accept/deny).",
    "send-deny-packet": "Enable to send a reply when a session is denied or blocked by a firewall policy.",
    "schedule": "Schedule name.",
    "status": "Enable or disable this policy.",
    "logtraffic": "Enable or disable logging. Log all sessions or security profile sessions.",
    "learning-mode": "Enable to allow everything, but log all of the meaningful data for security information gathering. A learning report will be generated.",
    "nat46": "Enable/disable NAT46.",
    "nat64": "Enable/disable NAT64.",
    "profile-type": "Determine whether the firewall policy allows security profile groups or single profiles only.",
    "profile-group": "Name of profile group.",
    "profile-protocol-options": "Name of an existing Protocol options profile.",
    "ssl-ssh-profile": "Name of an existing SSL SSH profile.",
    "av-profile": "Name of an existing Antivirus profile.",
    "webfilter-profile": "Name of an existing Web filter profile.",
    "dnsfilter-profile": "Name of an existing DNS filter profile.",
    "emailfilter-profile": "Name of an existing email filter profile.",
    "dlp-profile": "Name of an existing DLP profile.",
    "file-filter-profile": "Name of an existing file-filter profile.",
    "ips-sensor": "Name of an existing IPS sensor.",
    "application-list": "Name of an existing Application list.",
    "voip-profile": "Name of an existing VoIP (voipd) profile.",
    "ips-voip-filter": "Name of an existing VoIP (ips) profile.",
    "sctp-filter-profile": "Name of an existing SCTP filter profile.",
    "diameter-filter-profile": "Name of an existing Diameter filter profile.",
    "virtual-patch-profile": "Name of an existing virtual-patch profile.",
    "icap-profile": "Name of an existing ICAP profile.",
    "videofilter-profile": "Name of an existing VideoFilter profile.",
    "ssh-filter-profile": "Name of an existing SSH filter profile.",
    "casb-profile": "Name of an existing CASB profile.",
    "application": "Application ID list.",
    "app-category": "Application category ID list.",
    "url-category": "URL categories or groups.",
    "app-group": "Application group names.",
    "groups": "Names of user groups that can authenticate with this policy.",
    "users": "Names of individual users that can authenticate with this policy.",
    "fsso-groups": "Names of FSSO groups.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "policyid": {"type": "integer", "min": 0, "max": 4294967294},
    "name": {"type": "string", "max_length": 35},
    "schedule": {"type": "string", "max_length": 35},
    "profile-group": {"type": "string", "max_length": 47},
    "profile-protocol-options": {"type": "string", "max_length": 47},
    "ssl-ssh-profile": {"type": "string", "max_length": 47},
    "av-profile": {"type": "string", "max_length": 47},
    "webfilter-profile": {"type": "string", "max_length": 47},
    "dnsfilter-profile": {"type": "string", "max_length": 47},
    "emailfilter-profile": {"type": "string", "max_length": 47},
    "dlp-profile": {"type": "string", "max_length": 47},
    "file-filter-profile": {"type": "string", "max_length": 47},
    "ips-sensor": {"type": "string", "max_length": 47},
    "application-list": {"type": "string", "max_length": 47},
    "voip-profile": {"type": "string", "max_length": 47},
    "ips-voip-filter": {"type": "string", "max_length": 47},
    "sctp-filter-profile": {"type": "string", "max_length": 47},
    "diameter-filter-profile": {"type": "string", "max_length": 47},
    "virtual-patch-profile": {"type": "string", "max_length": 47},
    "icap-profile": {"type": "string", "max_length": 47},
    "videofilter-profile": {"type": "string", "max_length": 47},
    "ssh-filter-profile": {"type": "string", "max_length": 47},
    "casb-profile": {"type": "string", "max_length": 47},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "srcintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "dstintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-name": {
        "name": {
            "type": "string",
            "help": "IPv6 Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-custom": {
        "name": {
            "type": "string",
            "help": "Custom IPv6 Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom IPv6 Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service6 group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "service": {
        "name": {
            "type": "string",
            "help": "Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "application": {
        "id": {
            "type": "integer",
            "help": "Application IDs.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "app-category": {
        "id": {
            "type": "integer",
            "help": "Category IDs.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "app-group": {
        "name": {
            "type": "string",
            "help": "Application group names.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "groups": {
        "name": {
            "type": "string",
            "help": "User group name.",
            "default": "",
            "max_length": 79,
        },
    },
    "users": {
        "name": {
            "type": "string",
            "help": "User name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "fsso-groups": {
        "name": {
            "type": "string",
            "help": "Names of FSSO groups.",
            "required": True,
            "default": "",
            "max_length": 511,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_SRCADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_DSTADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_SRCADDR6_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_DSTADDR6_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_SRC = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_SRC_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6 = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6_SRC = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_ENFORCE_DEFAULT_APP_PORT = [
    "enable",
    "disable",
]
VALID_BODY_SERVICE_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_ACTION = [
    "accept",
    "deny",
]
VALID_BODY_SEND_DENY_PACKET = [
    "disable",
    "enable",
]
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_LOGTRAFFIC = [
    "all",
    "utm",
    "disable",
]
VALID_BODY_LEARNING_MODE = [
    "enable",
    "disable",
]
VALID_BODY_NAT46 = [
    "enable",
    "disable",
]
VALID_BODY_NAT64 = [
    "enable",
    "disable",
]
VALID_BODY_PROFILE_TYPE = [
    "single",
    "group",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_security_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/security_policy."""
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


def validate_firewall_security_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/security_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "srcaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr-negate",
            payload["srcaddr-negate"],
            VALID_BODY_SRCADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr-negate",
            payload["dstaddr-negate"],
            VALID_BODY_DSTADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr6-negate",
            payload["srcaddr6-negate"],
            VALID_BODY_SRCADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr6-negate",
            payload["dstaddr6-negate"],
            VALID_BODY_DSTADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service",
            payload["internet-service"],
            VALID_BODY_INTERNET_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-negate",
            payload["internet-service-negate"],
            VALID_BODY_INTERNET_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src",
            payload["internet-service-src"],
            VALID_BODY_INTERNET_SERVICE_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src-negate",
            payload["internet-service-src-negate"],
            VALID_BODY_INTERNET_SERVICE_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6",
            payload["internet-service6"],
            VALID_BODY_INTERNET_SERVICE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-negate",
            payload["internet-service6-negate"],
            VALID_BODY_INTERNET_SERVICE6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src",
            payload["internet-service6-src"],
            VALID_BODY_INTERNET_SERVICE6_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src-negate",
            payload["internet-service6-src-negate"],
            VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-default-app-port" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-default-app-port",
            payload["enforce-default-app-port"],
            VALID_BODY_ENFORCE_DEFAULT_APP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "service-negate",
            payload["service-negate"],
            VALID_BODY_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-deny-packet" in payload:
        is_valid, error = _validate_enum_field(
            "send-deny-packet",
            payload["send-deny-packet"],
            VALID_BODY_SEND_DENY_PACKET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "learning-mode" in payload:
        is_valid, error = _validate_enum_field(
            "learning-mode",
            payload["learning-mode"],
            VALID_BODY_LEARNING_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46" in payload:
        is_valid, error = _validate_enum_field(
            "nat46",
            payload["nat46"],
            VALID_BODY_NAT46,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64" in payload:
        is_valid, error = _validate_enum_field(
            "nat64",
            payload["nat64"],
            VALID_BODY_NAT64,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "profile-type" in payload:
        is_valid, error = _validate_enum_field(
            "profile-type",
            payload["profile-type"],
            VALID_BODY_PROFILE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_security_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/security_policy."""
    # Validate enum values using central function
    if "srcaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr-negate",
            payload["srcaddr-negate"],
            VALID_BODY_SRCADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr-negate",
            payload["dstaddr-negate"],
            VALID_BODY_DSTADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr6-negate",
            payload["srcaddr6-negate"],
            VALID_BODY_SRCADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr6-negate",
            payload["dstaddr6-negate"],
            VALID_BODY_DSTADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service",
            payload["internet-service"],
            VALID_BODY_INTERNET_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-negate",
            payload["internet-service-negate"],
            VALID_BODY_INTERNET_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src",
            payload["internet-service-src"],
            VALID_BODY_INTERNET_SERVICE_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src-negate",
            payload["internet-service-src-negate"],
            VALID_BODY_INTERNET_SERVICE_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6",
            payload["internet-service6"],
            VALID_BODY_INTERNET_SERVICE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-negate",
            payload["internet-service6-negate"],
            VALID_BODY_INTERNET_SERVICE6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src",
            payload["internet-service6-src"],
            VALID_BODY_INTERNET_SERVICE6_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src-negate",
            payload["internet-service6-src-negate"],
            VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-default-app-port" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-default-app-port",
            payload["enforce-default-app-port"],
            VALID_BODY_ENFORCE_DEFAULT_APP_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "service-negate",
            payload["service-negate"],
            VALID_BODY_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-deny-packet" in payload:
        is_valid, error = _validate_enum_field(
            "send-deny-packet",
            payload["send-deny-packet"],
            VALID_BODY_SEND_DENY_PACKET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "status" in payload:
        is_valid, error = _validate_enum_field(
            "status",
            payload["status"],
            VALID_BODY_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "learning-mode" in payload:
        is_valid, error = _validate_enum_field(
            "learning-mode",
            payload["learning-mode"],
            VALID_BODY_LEARNING_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46" in payload:
        is_valid, error = _validate_enum_field(
            "nat46",
            payload["nat46"],
            VALID_BODY_NAT46,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64" in payload:
        is_valid, error = _validate_enum_field(
            "nat64",
            payload["nat64"],
            VALID_BODY_NAT64,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "profile-type" in payload:
        is_valid, error = _validate_enum_field(
            "profile-type",
            payload["profile-type"],
            VALID_BODY_PROFILE_TYPE,
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
    "endpoint": "firewall/security_policy",
    "category": "cmdb",
    "api_path": "firewall/security-policy",
    "mkey": "policyid",
    "mkey_type": "integer",
    "help": "Configure NGFW IPv4/IPv6 application policies.",
    "total_fields": 81,
    "required_fields_count": 3,
    "fields_with_defaults_count": 47,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
