"""Validation helpers for firewall/proxy_policy - Auto-generated"""

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
    "proxy",  # Type of explicit proxy.
    "srcintf",  # Source interface names.
    "dstintf",  # Destination interface names.
    "schedule",  # Name of schedule object.
    "isolator-server",  # Isolator server name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "uuid": "00000000-0000-0000-0000-000000000000",
    "policyid": 0,
    "name": "",
    "proxy": "",
    "ztna-tags-match-logic": "or",
    "device-ownership": "disable",
    "internet-service": "disable",
    "internet-service-negate": "disable",
    "internet-service6": "disable",
    "internet-service6-negate": "disable",
    "srcaddr-negate": "disable",
    "dstaddr-negate": "disable",
    "ztna-ems-tag-negate": "disable",
    "service-negate": "disable",
    "action": "deny",
    "status": "enable",
    "schedule": "",
    "logtraffic": "utm",
    "session-ttl": 0,
    "http-tunnel-auth": "disable",
    "ssh-policy-redirect": "disable",
    "webproxy-forward-server": "",
    "isolator-server": "",
    "webproxy-profile": "",
    "transparent": "disable",
    "webcache": "disable",
    "webcache-https": "disable",
    "disclaimer": "disable",
    "utm-status": "disable",
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
    "ips-voip-filter": "",
    "sctp-filter-profile": "",
    "icap-profile": "",
    "videofilter-profile": "",
    "waf-profile": "",
    "ssh-filter-profile": "",
    "casb-profile": "",
    "replacemsg-override-group": "",
    "logtraffic-start": "disable",
    "log-http-transaction": "disable",
    "block-notification": "disable",
    "https-sub-category": "disable",
    "decrypted-traffic-mirror": "",
    "detect-https-in-http-request": "disable",
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
    "proxy": "option",  # Type of explicit proxy.
    "access-proxy": "string",  # IPv4 access proxy.
    "access-proxy6": "string",  # IPv6 access proxy.
    "ztna-proxy": "string",  # ZTNA proxies.
    "srcintf": "string",  # Source interface names.
    "dstintf": "string",  # Destination interface names.
    "srcaddr": "string",  # Source address objects.
    "poolname": "string",  # Name of IP pool object.
    "poolname6": "string",  # Name of IPv6 pool object.
    "dstaddr": "string",  # Destination address objects.
    "ztna-ems-tag": "string",  # ZTNA EMS Tag names.
    "ztna-tags-match-logic": "option",  # ZTNA tag matching logic.
    "device-ownership": "option",  # When enabled, the ownership enforcement will be done at policy level.
    "url-risk": "string",  # URL risk level name.
    "internet-service": "option",  # Enable/disable use of Internet Services for this policy. If enabled, destination
    "internet-service-negate": "option",  # When enabled, Internet Services match against any internet service EXCEPT the se
    "internet-service-name": "string",  # Internet Service name.
    "internet-service-group": "string",  # Internet Service group name.
    "internet-service-custom": "string",  # Custom Internet Service name.
    "internet-service-custom-group": "string",  # Custom Internet Service group name.
    "internet-service-fortiguard": "string",  # FortiGuard Internet Service name.
    "internet-service6": "option",  # Enable/disable use of Internet Services IPv6 for this policy. If enabled, destin
    "internet-service6-negate": "option",  # When enabled, Internet Services match against any internet service IPv6 EXCEPT t
    "internet-service6-name": "string",  # Internet Service IPv6 name.
    "internet-service6-group": "string",  # Internet Service IPv6 group name.
    "internet-service6-custom": "string",  # Custom Internet Service IPv6 name.
    "internet-service6-custom-group": "string",  # Custom Internet Service IPv6 group name.
    "internet-service6-fortiguard": "string",  # FortiGuard Internet Service IPv6 name.
    "service": "string",  # Name of service objects.
    "srcaddr-negate": "option",  # When enabled, source addresses match against any address EXCEPT the specified so
    "dstaddr-negate": "option",  # When enabled, destination addresses match against any address EXCEPT the specifi
    "ztna-ems-tag-negate": "option",  # When enabled, ZTNA EMS tags match against any tag EXCEPT the specified ZTNA EMS 
    "service-negate": "option",  # When enabled, services match against any service EXCEPT the specified destinatio
    "action": "option",  # Accept or deny traffic matching the policy parameters.
    "status": "option",  # Enable/disable the active status of the policy.
    "schedule": "string",  # Name of schedule object.
    "logtraffic": "option",  # Enable/disable logging traffic through the policy.
    "session-ttl": "integer",  # TTL in seconds for sessions accepted by this policy (0 means use the system defa
    "srcaddr6": "string",  # IPv6 source address objects.
    "dstaddr6": "string",  # IPv6 destination address objects.
    "groups": "string",  # Names of group objects.
    "users": "string",  # Names of user objects.
    "http-tunnel-auth": "option",  # Enable/disable HTTP tunnel authentication.
    "ssh-policy-redirect": "option",  # Redirect SSH traffic to matching transparent proxy policy.
    "webproxy-forward-server": "string",  # Web proxy forward server name.
    "isolator-server": "string",  # Isolator server name.
    "webproxy-profile": "string",  # Name of web proxy profile.
    "transparent": "option",  # Enable to use the IP address of the client to connect to the server.
    "webcache": "option",  # Enable/disable web caching.
    "webcache-https": "option",  # Enable/disable web caching for HTTPS (Requires deep-inspection enabled in ssl-ss
    "disclaimer": "option",  # Web proxy disclaimer setting: by domain, policy, or user.
    "utm-status": "option",  # Enable the use of UTM profiles/sensors/lists.
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
    "ips-voip-filter": "string",  # Name of an existing VoIP (ips) profile.
    "sctp-filter-profile": "string",  # Name of an existing SCTP filter profile.
    "icap-profile": "string",  # Name of an existing ICAP profile.
    "videofilter-profile": "string",  # Name of an existing VideoFilter profile.
    "waf-profile": "string",  # Name of an existing Web application firewall profile.
    "ssh-filter-profile": "string",  # Name of an existing SSH filter profile.
    "casb-profile": "string",  # Name of an existing CASB profile.
    "replacemsg-override-group": "string",  # Authentication replacement message override group.
    "logtraffic-start": "option",  # Enable/disable policy log traffic start.
    "log-http-transaction": "option",  # Enable/disable HTTP transaction log.
    "comments": "var-string",  # Optional comments.
    "block-notification": "option",  # Enable/disable block notification.
    "redirect-url": "var-string",  # Redirect URL for further explicit web proxy processing.
    "https-sub-category": "option",  # Enable/disable HTTPS sub-category policy matching.
    "decrypted-traffic-mirror": "string",  # Decrypted traffic mirror.
    "detect-https-in-http-request": "option",  # Enable/disable detection of HTTPS in HTTP request.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "policyid": "Policy ID.",
    "name": "Policy name.",
    "proxy": "Type of explicit proxy.",
    "access-proxy": "IPv4 access proxy.",
    "access-proxy6": "IPv6 access proxy.",
    "ztna-proxy": "ZTNA proxies.",
    "srcintf": "Source interface names.",
    "dstintf": "Destination interface names.",
    "srcaddr": "Source address objects.",
    "poolname": "Name of IP pool object.",
    "poolname6": "Name of IPv6 pool object.",
    "dstaddr": "Destination address objects.",
    "ztna-ems-tag": "ZTNA EMS Tag names.",
    "ztna-tags-match-logic": "ZTNA tag matching logic.",
    "device-ownership": "When enabled, the ownership enforcement will be done at policy level.",
    "url-risk": "URL risk level name.",
    "internet-service": "Enable/disable use of Internet Services for this policy. If enabled, destination address and service are not used.",
    "internet-service-negate": "When enabled, Internet Services match against any internet service EXCEPT the selected Internet Service.",
    "internet-service-name": "Internet Service name.",
    "internet-service-group": "Internet Service group name.",
    "internet-service-custom": "Custom Internet Service name.",
    "internet-service-custom-group": "Custom Internet Service group name.",
    "internet-service-fortiguard": "FortiGuard Internet Service name.",
    "internet-service6": "Enable/disable use of Internet Services IPv6 for this policy. If enabled, destination IPv6 address and service are not used.",
    "internet-service6-negate": "When enabled, Internet Services match against any internet service IPv6 EXCEPT the selected Internet Service IPv6.",
    "internet-service6-name": "Internet Service IPv6 name.",
    "internet-service6-group": "Internet Service IPv6 group name.",
    "internet-service6-custom": "Custom Internet Service IPv6 name.",
    "internet-service6-custom-group": "Custom Internet Service IPv6 group name.",
    "internet-service6-fortiguard": "FortiGuard Internet Service IPv6 name.",
    "service": "Name of service objects.",
    "srcaddr-negate": "When enabled, source addresses match against any address EXCEPT the specified source addresses.",
    "dstaddr-negate": "When enabled, destination addresses match against any address EXCEPT the specified destination addresses.",
    "ztna-ems-tag-negate": "When enabled, ZTNA EMS tags match against any tag EXCEPT the specified ZTNA EMS tags.",
    "service-negate": "When enabled, services match against any service EXCEPT the specified destination services.",
    "action": "Accept or deny traffic matching the policy parameters.",
    "status": "Enable/disable the active status of the policy.",
    "schedule": "Name of schedule object.",
    "logtraffic": "Enable/disable logging traffic through the policy.",
    "session-ttl": "TTL in seconds for sessions accepted by this policy (0 means use the system default session TTL).",
    "srcaddr6": "IPv6 source address objects.",
    "dstaddr6": "IPv6 destination address objects.",
    "groups": "Names of group objects.",
    "users": "Names of user objects.",
    "http-tunnel-auth": "Enable/disable HTTP tunnel authentication.",
    "ssh-policy-redirect": "Redirect SSH traffic to matching transparent proxy policy.",
    "webproxy-forward-server": "Web proxy forward server name.",
    "isolator-server": "Isolator server name.",
    "webproxy-profile": "Name of web proxy profile.",
    "transparent": "Enable to use the IP address of the client to connect to the server.",
    "webcache": "Enable/disable web caching.",
    "webcache-https": "Enable/disable web caching for HTTPS (Requires deep-inspection enabled in ssl-ssh-profile).",
    "disclaimer": "Web proxy disclaimer setting: by domain, policy, or user.",
    "utm-status": "Enable the use of UTM profiles/sensors/lists.",
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
    "ips-voip-filter": "Name of an existing VoIP (ips) profile.",
    "sctp-filter-profile": "Name of an existing SCTP filter profile.",
    "icap-profile": "Name of an existing ICAP profile.",
    "videofilter-profile": "Name of an existing VideoFilter profile.",
    "waf-profile": "Name of an existing Web application firewall profile.",
    "ssh-filter-profile": "Name of an existing SSH filter profile.",
    "casb-profile": "Name of an existing CASB profile.",
    "replacemsg-override-group": "Authentication replacement message override group.",
    "logtraffic-start": "Enable/disable policy log traffic start.",
    "log-http-transaction": "Enable/disable HTTP transaction log.",
    "comments": "Optional comments.",
    "block-notification": "Enable/disable block notification.",
    "redirect-url": "Redirect URL for further explicit web proxy processing.",
    "https-sub-category": "Enable/disable HTTPS sub-category policy matching.",
    "decrypted-traffic-mirror": "Decrypted traffic mirror.",
    "detect-https-in-http-request": "Enable/disable detection of HTTPS in HTTP request.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "policyid": {"type": "integer", "min": 0, "max": 4294967295},
    "name": {"type": "string", "max_length": 35},
    "schedule": {"type": "string", "max_length": 35},
    "session-ttl": {"type": "integer", "min": 300, "max": 2764800},
    "webproxy-forward-server": {"type": "string", "max_length": 63},
    "isolator-server": {"type": "string", "max_length": 63},
    "webproxy-profile": {"type": "string", "max_length": 63},
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
    "ips-voip-filter": {"type": "string", "max_length": 47},
    "sctp-filter-profile": {"type": "string", "max_length": 47},
    "icap-profile": {"type": "string", "max_length": 47},
    "videofilter-profile": {"type": "string", "max_length": 47},
    "waf-profile": {"type": "string", "max_length": 47},
    "ssh-filter-profile": {"type": "string", "max_length": 47},
    "casb-profile": {"type": "string", "max_length": 47},
    "replacemsg-override-group": {"type": "string", "max_length": 35},
    "decrypted-traffic-mirror": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "access-proxy": {
        "name": {
            "type": "string",
            "help": "Access Proxy name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "access-proxy6": {
        "name": {
            "type": "string",
            "help": "Access proxy name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "ztna-proxy": {
        "name": {
            "type": "string",
            "help": "ZTNA proxy name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
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
    "poolname": {
        "name": {
            "type": "string",
            "help": "IP pool name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "poolname6": {
        "name": {
            "type": "string",
            "help": "IPv6 pool name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "default": "",
            "max_length": 79,
        },
    },
    "ztna-ems-tag": {
        "name": {
            "type": "string",
            "help": "EMS Tag name.",
            "default": "",
            "max_length": 79,
        },
    },
    "url-risk": {
        "name": {
            "type": "string",
            "help": "Risk level name.",
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
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
    "internet-service6-name": {
        "name": {
            "type": "string",
            "help": "Internet Service IPv6 name.",
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-group": {
        "name": {
            "type": "string",
            "help": "Internet Service IPv6 group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service IPv6 name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service IPv6 group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service IPv6 name.",
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
    "groups": {
        "name": {
            "type": "string",
            "help": "Group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "users": {
        "name": {
            "type": "string",
            "help": "Group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_PROXY = [
    "explicit-web",
    "transparent-web",
    "ftp",
    "ssh",
    "ssh-tunnel",
    "access-proxy",
    "ztna-proxy",
    "wanopt",
]
VALID_BODY_ZTNA_TAGS_MATCH_LOGIC = [
    "or",
    "and",
]
VALID_BODY_DEVICE_OWNERSHIP = [
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
VALID_BODY_INTERNET_SERVICE6 = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_SRCADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_DSTADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_ZTNA_EMS_TAG_NEGATE = [
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
    "redirect",
    "isolate",
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
VALID_BODY_HTTP_TUNNEL_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_SSH_POLICY_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_TRANSPARENT = [
    "enable",
    "disable",
]
VALID_BODY_WEBCACHE = [
    "enable",
    "disable",
]
VALID_BODY_WEBCACHE_HTTPS = [
    "disable",
    "enable",
]
VALID_BODY_DISCLAIMER = [
    "disable",
    "domain",
    "policy",
    "user",
]
VALID_BODY_UTM_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_PROFILE_TYPE = [
    "single",
    "group",
]
VALID_BODY_LOGTRAFFIC_START = [
    "enable",
    "disable",
]
VALID_BODY_LOG_HTTP_TRANSACTION = [
    "enable",
    "disable",
]
VALID_BODY_BLOCK_NOTIFICATION = [
    "enable",
    "disable",
]
VALID_BODY_HTTPS_SUB_CATEGORY = [
    "enable",
    "disable",
]
VALID_BODY_DETECT_HTTPS_IN_HTTP_REQUEST = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_proxy_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/proxy_policy."""
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


def validate_firewall_proxy_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/proxy_policy object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "proxy" in payload:
        is_valid, error = _validate_enum_field(
            "proxy",
            payload["proxy"],
            VALID_BODY_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-tags-match-logic" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-tags-match-logic",
            payload["ztna-tags-match-logic"],
            VALID_BODY_ZTNA_TAGS_MATCH_LOGIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-ownership" in payload:
        is_valid, error = _validate_enum_field(
            "device-ownership",
            payload["device-ownership"],
            VALID_BODY_DEVICE_OWNERSHIP,
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
    if "ztna-ems-tag-negate" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-ems-tag-negate",
            payload["ztna-ems-tag-negate"],
            VALID_BODY_ZTNA_EMS_TAG_NEGATE,
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
    if "http-tunnel-auth" in payload:
        is_valid, error = _validate_enum_field(
            "http-tunnel-auth",
            payload["http-tunnel-auth"],
            VALID_BODY_HTTP_TUNNEL_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-policy-redirect",
            payload["ssh-policy-redirect"],
            VALID_BODY_SSH_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transparent" in payload:
        is_valid, error = _validate_enum_field(
            "transparent",
            payload["transparent"],
            VALID_BODY_TRANSPARENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache" in payload:
        is_valid, error = _validate_enum_field(
            "webcache",
            payload["webcache"],
            VALID_BODY_WEBCACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache-https" in payload:
        is_valid, error = _validate_enum_field(
            "webcache-https",
            payload["webcache-https"],
            VALID_BODY_WEBCACHE_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "disclaimer",
            payload["disclaimer"],
            VALID_BODY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utm-status" in payload:
        is_valid, error = _validate_enum_field(
            "utm-status",
            payload["utm-status"],
            VALID_BODY_UTM_STATUS,
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
    if "logtraffic-start" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic-start",
            payload["logtraffic-start"],
            VALID_BODY_LOGTRAFFIC_START,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-http-transaction" in payload:
        is_valid, error = _validate_enum_field(
            "log-http-transaction",
            payload["log-http-transaction"],
            VALID_BODY_LOG_HTTP_TRANSACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-notification" in payload:
        is_valid, error = _validate_enum_field(
            "block-notification",
            payload["block-notification"],
            VALID_BODY_BLOCK_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-sub-category" in payload:
        is_valid, error = _validate_enum_field(
            "https-sub-category",
            payload["https-sub-category"],
            VALID_BODY_HTTPS_SUB_CATEGORY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "detect-https-in-http-request" in payload:
        is_valid, error = _validate_enum_field(
            "detect-https-in-http-request",
            payload["detect-https-in-http-request"],
            VALID_BODY_DETECT_HTTPS_IN_HTTP_REQUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_proxy_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/proxy_policy."""
    # Validate enum values using central function
    if "proxy" in payload:
        is_valid, error = _validate_enum_field(
            "proxy",
            payload["proxy"],
            VALID_BODY_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-tags-match-logic" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-tags-match-logic",
            payload["ztna-tags-match-logic"],
            VALID_BODY_ZTNA_TAGS_MATCH_LOGIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-ownership" in payload:
        is_valid, error = _validate_enum_field(
            "device-ownership",
            payload["device-ownership"],
            VALID_BODY_DEVICE_OWNERSHIP,
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
    if "ztna-ems-tag-negate" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-ems-tag-negate",
            payload["ztna-ems-tag-negate"],
            VALID_BODY_ZTNA_EMS_TAG_NEGATE,
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
    if "http-tunnel-auth" in payload:
        is_valid, error = _validate_enum_field(
            "http-tunnel-auth",
            payload["http-tunnel-auth"],
            VALID_BODY_HTTP_TUNNEL_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-policy-redirect",
            payload["ssh-policy-redirect"],
            VALID_BODY_SSH_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transparent" in payload:
        is_valid, error = _validate_enum_field(
            "transparent",
            payload["transparent"],
            VALID_BODY_TRANSPARENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache" in payload:
        is_valid, error = _validate_enum_field(
            "webcache",
            payload["webcache"],
            VALID_BODY_WEBCACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache-https" in payload:
        is_valid, error = _validate_enum_field(
            "webcache-https",
            payload["webcache-https"],
            VALID_BODY_WEBCACHE_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "disclaimer",
            payload["disclaimer"],
            VALID_BODY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utm-status" in payload:
        is_valid, error = _validate_enum_field(
            "utm-status",
            payload["utm-status"],
            VALID_BODY_UTM_STATUS,
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
    if "logtraffic-start" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic-start",
            payload["logtraffic-start"],
            VALID_BODY_LOGTRAFFIC_START,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-http-transaction" in payload:
        is_valid, error = _validate_enum_field(
            "log-http-transaction",
            payload["log-http-transaction"],
            VALID_BODY_LOG_HTTP_TRANSACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-notification" in payload:
        is_valid, error = _validate_enum_field(
            "block-notification",
            payload["block-notification"],
            VALID_BODY_BLOCK_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-sub-category" in payload:
        is_valid, error = _validate_enum_field(
            "https-sub-category",
            payload["https-sub-category"],
            VALID_BODY_HTTPS_SUB_CATEGORY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "detect-https-in-http-request" in payload:
        is_valid, error = _validate_enum_field(
            "detect-https-in-http-request",
            payload["detect-https-in-http-request"],
            VALID_BODY_DETECT_HTTPS_IN_HTTP_REQUEST,
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
    "endpoint": "firewall/proxy_policy",
    "category": "cmdb",
    "api_path": "firewall/proxy-policy",
    "mkey": "policyid",
    "mkey_type": "integer",
    "help": "Configure proxy policies.",
    "total_fields": 83,
    "required_fields_count": 5,
    "fields_with_defaults_count": 55,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
