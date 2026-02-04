"""Validation helpers for vpn/ipsec/phase2 - Auto-generated"""

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
    "phase1name",  # Phase 1 determines the options required for phase 2.
    "proposal",  # Phase2 proposal.
    "src-name",  # Local proxy ID name.
    "src-name6",  # Local proxy ID name.
    "dst-name",  # Remote proxy ID name.
    "dst-name6",  # Remote proxy ID name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "phase1name": "",
    "dhcp-ipsec": "disable",
    "use-natip": "enable",
    "selector-match": "auto",
    "proposal": "",
    "pfs": "enable",
    "dhgrp": "20",
    "addke1": "",
    "addke2": "",
    "addke3": "",
    "addke4": "",
    "addke5": "",
    "addke6": "",
    "addke7": "",
    "replay": "enable",
    "keepalive": "disable",
    "auto-negotiate": "disable",
    "add-route": "phase1",
    "inbound-dscp-copy": "phase1",
    "keylifeseconds": 43200,
    "keylifekbs": 5120,
    "keylife-type": "seconds",
    "single-source": "disable",
    "route-overlap": "use-new",
    "encapsulation": "tunnel-mode",
    "l2tp": "disable",
    "initiator-ts-narrow": "disable",
    "diffserv": "disable",
    "diffservcode": "",
    "protocol": 0,
    "src-name": "",
    "src-name6": "",
    "src-addr-type": "subnet",
    "src-start-ip": "0.0.0.0",
    "src-start-ip6": "::",
    "src-end-ip": "0.0.0.0",
    "src-end-ip6": "::",
    "src-subnet": "0.0.0.0 0.0.0.0",
    "src-subnet6": "::/0",
    "src-port": 0,
    "dst-name": "",
    "dst-name6": "",
    "dst-addr-type": "subnet",
    "dst-start-ip": "0.0.0.0",
    "dst-start-ip6": "::",
    "dst-end-ip": "0.0.0.0",
    "dst-end-ip6": "::",
    "dst-subnet": "0.0.0.0 0.0.0.0",
    "dst-subnet6": "::/0",
    "dst-port": 0,
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
    "name": "string",  # IPsec tunnel name.
    "phase1name": "string",  # Phase 1 determines the options required for phase 2.
    "dhcp-ipsec": "option",  # Enable/disable DHCP-IPsec.
    "use-natip": "option",  # Enable to use the FortiGate public IP as the source selector when outbound NAT i
    "selector-match": "option",  # Match type to use when comparing selectors.
    "proposal": "option",  # Phase2 proposal.
    "pfs": "option",  # Enable/disable PFS feature.
    "dhgrp": "option",  # Phase2 DH group.
    "addke1": "option",  # phase2 ADDKE1 group.
    "addke2": "option",  # phase2 ADDKE2 group.
    "addke3": "option",  # phase2 ADDKE3 group.
    "addke4": "option",  # phase2 ADDKE4 group.
    "addke5": "option",  # phase2 ADDKE5 group.
    "addke6": "option",  # phase2 ADDKE6 group.
    "addke7": "option",  # phase2 ADDKE7 group.
    "replay": "option",  # Enable/disable replay detection.
    "keepalive": "option",  # Enable/disable keep alive.
    "auto-negotiate": "option",  # Enable/disable IPsec SA auto-negotiation.
    "add-route": "option",  # Enable/disable automatic route addition.
    "inbound-dscp-copy": "option",  # Enable/disable copying of the DSCP in the ESP header to the inner IP header.
    "keylifeseconds": "integer",  # Phase2 key life in time in seconds (120 - 172800).
    "keylifekbs": "integer",  # Phase2 key life in number of kilobytes of traffic (5120 - 4294967295).
    "keylife-type": "option",  # Keylife type.
    "single-source": "option",  # Enable/disable single source IP restriction.
    "route-overlap": "option",  # Action for overlapping routes.
    "encapsulation": "option",  # ESP encapsulation mode.
    "l2tp": "option",  # Enable/disable L2TP over IPsec.
    "comments": "var-string",  # Comment.
    "initiator-ts-narrow": "option",  # Enable/disable traffic selector narrowing for IKEv2 initiator.
    "diffserv": "option",  # Enable/disable applying DSCP value to the IPsec tunnel outer IP header.
    "diffservcode": "user",  # DSCP value to be applied to the IPsec tunnel outer IP header.
    "protocol": "integer",  # Quick mode protocol selector (1 - 255 or 0 for all).
    "src-name": "string",  # Local proxy ID name.
    "src-name6": "string",  # Local proxy ID name.
    "src-addr-type": "option",  # Local proxy ID type.
    "src-start-ip": "ipv4-address-any",  # Local proxy ID start.
    "src-start-ip6": "ipv6-address",  # Local proxy ID IPv6 start.
    "src-end-ip": "ipv4-address-any",  # Local proxy ID end.
    "src-end-ip6": "ipv6-address",  # Local proxy ID IPv6 end.
    "src-subnet": "ipv4-classnet-any",  # Local proxy ID subnet.
    "src-subnet6": "ipv6-prefix",  # Local proxy ID IPv6 subnet.
    "src-port": "integer",  # Quick mode source port (1 - 65535 or 0 for all).
    "dst-name": "string",  # Remote proxy ID name.
    "dst-name6": "string",  # Remote proxy ID name.
    "dst-addr-type": "option",  # Remote proxy ID type.
    "dst-start-ip": "ipv4-address-any",  # Remote proxy ID IPv4 start.
    "dst-start-ip6": "ipv6-address",  # Remote proxy ID IPv6 start.
    "dst-end-ip": "ipv4-address-any",  # Remote proxy ID IPv4 end.
    "dst-end-ip6": "ipv6-address",  # Remote proxy ID IPv6 end.
    "dst-subnet": "ipv4-classnet-any",  # Remote proxy ID IPv4 subnet.
    "dst-subnet6": "ipv6-prefix",  # Remote proxy ID IPv6 subnet.
    "dst-port": "integer",  # Quick mode destination port (1 - 65535 or 0 for all).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "IPsec tunnel name.",
    "phase1name": "Phase 1 determines the options required for phase 2.",
    "dhcp-ipsec": "Enable/disable DHCP-IPsec.",
    "use-natip": "Enable to use the FortiGate public IP as the source selector when outbound NAT is used.",
    "selector-match": "Match type to use when comparing selectors.",
    "proposal": "Phase2 proposal.",
    "pfs": "Enable/disable PFS feature.",
    "dhgrp": "Phase2 DH group.",
    "addke1": "phase2 ADDKE1 group.",
    "addke2": "phase2 ADDKE2 group.",
    "addke3": "phase2 ADDKE3 group.",
    "addke4": "phase2 ADDKE4 group.",
    "addke5": "phase2 ADDKE5 group.",
    "addke6": "phase2 ADDKE6 group.",
    "addke7": "phase2 ADDKE7 group.",
    "replay": "Enable/disable replay detection.",
    "keepalive": "Enable/disable keep alive.",
    "auto-negotiate": "Enable/disable IPsec SA auto-negotiation.",
    "add-route": "Enable/disable automatic route addition.",
    "inbound-dscp-copy": "Enable/disable copying of the DSCP in the ESP header to the inner IP header.",
    "keylifeseconds": "Phase2 key life in time in seconds (120 - 172800).",
    "keylifekbs": "Phase2 key life in number of kilobytes of traffic (5120 - 4294967295).",
    "keylife-type": "Keylife type.",
    "single-source": "Enable/disable single source IP restriction.",
    "route-overlap": "Action for overlapping routes.",
    "encapsulation": "ESP encapsulation mode.",
    "l2tp": "Enable/disable L2TP over IPsec.",
    "comments": "Comment.",
    "initiator-ts-narrow": "Enable/disable traffic selector narrowing for IKEv2 initiator.",
    "diffserv": "Enable/disable applying DSCP value to the IPsec tunnel outer IP header.",
    "diffservcode": "DSCP value to be applied to the IPsec tunnel outer IP header.",
    "protocol": "Quick mode protocol selector (1 - 255 or 0 for all).",
    "src-name": "Local proxy ID name.",
    "src-name6": "Local proxy ID name.",
    "src-addr-type": "Local proxy ID type.",
    "src-start-ip": "Local proxy ID start.",
    "src-start-ip6": "Local proxy ID IPv6 start.",
    "src-end-ip": "Local proxy ID end.",
    "src-end-ip6": "Local proxy ID IPv6 end.",
    "src-subnet": "Local proxy ID subnet.",
    "src-subnet6": "Local proxy ID IPv6 subnet.",
    "src-port": "Quick mode source port (1 - 65535 or 0 for all).",
    "dst-name": "Remote proxy ID name.",
    "dst-name6": "Remote proxy ID name.",
    "dst-addr-type": "Remote proxy ID type.",
    "dst-start-ip": "Remote proxy ID IPv4 start.",
    "dst-start-ip6": "Remote proxy ID IPv6 start.",
    "dst-end-ip": "Remote proxy ID IPv4 end.",
    "dst-end-ip6": "Remote proxy ID IPv6 end.",
    "dst-subnet": "Remote proxy ID IPv4 subnet.",
    "dst-subnet6": "Remote proxy ID IPv6 subnet.",
    "dst-port": "Quick mode destination port (1 - 65535 or 0 for all).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "phase1name": {"type": "string", "max_length": 35},
    "keylifeseconds": {"type": "integer", "min": 120, "max": 172800},
    "keylifekbs": {"type": "integer", "min": 5120, "max": 4294967295},
    "protocol": {"type": "integer", "min": 0, "max": 255},
    "src-name": {"type": "string", "max_length": 79},
    "src-name6": {"type": "string", "max_length": 79},
    "src-port": {"type": "integer", "min": 0, "max": 65535},
    "dst-name": {"type": "string", "max_length": 79},
    "dst-name6": {"type": "string", "max_length": 79},
    "dst-port": {"type": "integer", "min": 0, "max": 65535},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_DHCP_IPSEC = [
    "enable",
    "disable",
]
VALID_BODY_USE_NATIP = [
    "enable",
    "disable",
]
VALID_BODY_SELECTOR_MATCH = [
    "exact",
    "subset",
    "auto",
]
VALID_BODY_PROPOSAL = [
    "null-md5",
    "null-sha1",
    "null-sha256",
    "null-sha384",
    "null-sha512",
    "des-null",
    "des-md5",
    "des-sha1",
    "des-sha256",
    "des-sha384",
    "des-sha512",
    "3des-null",
    "3des-md5",
    "3des-sha1",
    "3des-sha256",
    "3des-sha384",
    "3des-sha512",
    "aes128-null",
    "aes128-md5",
    "aes128-sha1",
    "aes128-sha256",
    "aes128-sha384",
    "aes128-sha512",
    "aes128gcm",
    "aes192-null",
    "aes192-md5",
    "aes192-sha1",
    "aes192-sha256",
    "aes192-sha384",
    "aes192-sha512",
    "aes256-null",
    "aes256-md5",
    "aes256-sha1",
    "aes256-sha256",
    "aes256-sha384",
    "aes256-sha512",
    "aes256gcm",
    "chacha20poly1305",
    "aria128-null",
    "aria128-md5",
    "aria128-sha1",
    "aria128-sha256",
    "aria128-sha384",
    "aria128-sha512",
    "aria192-null",
    "aria192-md5",
    "aria192-sha1",
    "aria192-sha256",
    "aria192-sha384",
    "aria192-sha512",
    "aria256-null",
    "aria256-md5",
    "aria256-sha1",
    "aria256-sha256",
    "aria256-sha384",
    "aria256-sha512",
    "seed-null",
    "seed-md5",
    "seed-sha1",
    "seed-sha256",
    "seed-sha384",
    "seed-sha512",
]
VALID_BODY_PFS = [
    "enable",
    "disable",
]
VALID_BODY_DHGRP = [
    "1",
    "2",
    "5",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
]
VALID_BODY_ADDKE1 = [
    "0",
    "35",
    "36",
    "37",
    "1080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1089",
    "1090",
    "1091",
    "1092",
    "1093",
    "1094",
]
VALID_BODY_ADDKE2 = [
    "0",
    "35",
    "36",
    "37",
    "1080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1089",
    "1090",
    "1091",
    "1092",
    "1093",
    "1094",
]
VALID_BODY_ADDKE3 = [
    "0",
    "35",
    "36",
    "37",
    "1080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1089",
    "1090",
    "1091",
    "1092",
    "1093",
    "1094",
]
VALID_BODY_ADDKE4 = [
    "0",
    "35",
    "36",
    "37",
    "1080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1089",
    "1090",
    "1091",
    "1092",
    "1093",
    "1094",
]
VALID_BODY_ADDKE5 = [
    "0",
    "35",
    "36",
    "37",
    "1080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1089",
    "1090",
    "1091",
    "1092",
    "1093",
    "1094",
]
VALID_BODY_ADDKE6 = [
    "0",
    "35",
    "36",
    "37",
    "1080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1089",
    "1090",
    "1091",
    "1092",
    "1093",
    "1094",
]
VALID_BODY_ADDKE7 = [
    "0",
    "35",
    "36",
    "37",
    "1080",
    "1081",
    "1082",
    "1083",
    "1084",
    "1085",
    "1089",
    "1090",
    "1091",
    "1092",
    "1093",
    "1094",
]
VALID_BODY_REPLAY = [
    "enable",
    "disable",
]
VALID_BODY_KEEPALIVE = [
    "enable",
    "disable",
]
VALID_BODY_AUTO_NEGOTIATE = [
    "enable",
    "disable",
]
VALID_BODY_ADD_ROUTE = [
    "phase1",
    "enable",
    "disable",
]
VALID_BODY_INBOUND_DSCP_COPY = [
    "phase1",
    "enable",
    "disable",
]
VALID_BODY_KEYLIFE_TYPE = [
    "seconds",
    "kbs",
    "both",
]
VALID_BODY_SINGLE_SOURCE = [
    "enable",
    "disable",
]
VALID_BODY_ROUTE_OVERLAP = [
    "use-old",
    "use-new",
    "allow",
]
VALID_BODY_ENCAPSULATION = [
    "tunnel-mode",
    "transport-mode",
]
VALID_BODY_L2TP = [
    "enable",
    "disable",
]
VALID_BODY_INITIATOR_TS_NARROW = [
    "enable",
    "disable",
]
VALID_BODY_DIFFSERV = [
    "enable",
    "disable",
]
VALID_BODY_SRC_ADDR_TYPE = [
    "subnet",
    "range",
    "ip",
    "name",
]
VALID_BODY_DST_ADDR_TYPE = [
    "subnet",
    "range",
    "ip",
    "name",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_vpn_ipsec_phase2_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/ipsec/phase2."""
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


def validate_vpn_ipsec_phase2_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/ipsec/phase2 object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "dhcp-ipsec" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-ipsec",
            payload["dhcp-ipsec"],
            VALID_BODY_DHCP_IPSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-natip" in payload:
        is_valid, error = _validate_enum_field(
            "use-natip",
            payload["use-natip"],
            VALID_BODY_USE_NATIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "selector-match" in payload:
        is_valid, error = _validate_enum_field(
            "selector-match",
            payload["selector-match"],
            VALID_BODY_SELECTOR_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proposal" in payload:
        is_valid, error = _validate_enum_field(
            "proposal",
            payload["proposal"],
            VALID_BODY_PROPOSAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pfs" in payload:
        is_valid, error = _validate_enum_field(
            "pfs",
            payload["pfs"],
            VALID_BODY_PFS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhgrp" in payload:
        is_valid, error = _validate_enum_field(
            "dhgrp",
            payload["dhgrp"],
            VALID_BODY_DHGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke1" in payload:
        is_valid, error = _validate_enum_field(
            "addke1",
            payload["addke1"],
            VALID_BODY_ADDKE1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke2" in payload:
        is_valid, error = _validate_enum_field(
            "addke2",
            payload["addke2"],
            VALID_BODY_ADDKE2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke3" in payload:
        is_valid, error = _validate_enum_field(
            "addke3",
            payload["addke3"],
            VALID_BODY_ADDKE3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke4" in payload:
        is_valid, error = _validate_enum_field(
            "addke4",
            payload["addke4"],
            VALID_BODY_ADDKE4,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke5" in payload:
        is_valid, error = _validate_enum_field(
            "addke5",
            payload["addke5"],
            VALID_BODY_ADDKE5,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke6" in payload:
        is_valid, error = _validate_enum_field(
            "addke6",
            payload["addke6"],
            VALID_BODY_ADDKE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke7" in payload:
        is_valid, error = _validate_enum_field(
            "addke7",
            payload["addke7"],
            VALID_BODY_ADDKE7,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "replay" in payload:
        is_valid, error = _validate_enum_field(
            "replay",
            payload["replay"],
            VALID_BODY_REPLAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "keepalive" in payload:
        is_valid, error = _validate_enum_field(
            "keepalive",
            payload["keepalive"],
            VALID_BODY_KEEPALIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "auto-negotiate",
            payload["auto-negotiate"],
            VALID_BODY_AUTO_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-route",
            payload["add-route"],
            VALID_BODY_ADD_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inbound-dscp-copy" in payload:
        is_valid, error = _validate_enum_field(
            "inbound-dscp-copy",
            payload["inbound-dscp-copy"],
            VALID_BODY_INBOUND_DSCP_COPY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "keylife-type" in payload:
        is_valid, error = _validate_enum_field(
            "keylife-type",
            payload["keylife-type"],
            VALID_BODY_KEYLIFE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "single-source" in payload:
        is_valid, error = _validate_enum_field(
            "single-source",
            payload["single-source"],
            VALID_BODY_SINGLE_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "route-overlap" in payload:
        is_valid, error = _validate_enum_field(
            "route-overlap",
            payload["route-overlap"],
            VALID_BODY_ROUTE_OVERLAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encapsulation" in payload:
        is_valid, error = _validate_enum_field(
            "encapsulation",
            payload["encapsulation"],
            VALID_BODY_ENCAPSULATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l2tp" in payload:
        is_valid, error = _validate_enum_field(
            "l2tp",
            payload["l2tp"],
            VALID_BODY_L2TP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "initiator-ts-narrow" in payload:
        is_valid, error = _validate_enum_field(
            "initiator-ts-narrow",
            payload["initiator-ts-narrow"],
            VALID_BODY_INITIATOR_TS_NARROW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv",
            payload["diffserv"],
            VALID_BODY_DIFFSERV,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "src-addr-type",
            payload["src-addr-type"],
            VALID_BODY_SRC_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dst-addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "dst-addr-type",
            payload["dst-addr-type"],
            VALID_BODY_DST_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_vpn_ipsec_phase2_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/ipsec/phase2."""
    # Validate enum values using central function
    if "dhcp-ipsec" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-ipsec",
            payload["dhcp-ipsec"],
            VALID_BODY_DHCP_IPSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "use-natip" in payload:
        is_valid, error = _validate_enum_field(
            "use-natip",
            payload["use-natip"],
            VALID_BODY_USE_NATIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "selector-match" in payload:
        is_valid, error = _validate_enum_field(
            "selector-match",
            payload["selector-match"],
            VALID_BODY_SELECTOR_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proposal" in payload:
        is_valid, error = _validate_enum_field(
            "proposal",
            payload["proposal"],
            VALID_BODY_PROPOSAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pfs" in payload:
        is_valid, error = _validate_enum_field(
            "pfs",
            payload["pfs"],
            VALID_BODY_PFS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhgrp" in payload:
        is_valid, error = _validate_enum_field(
            "dhgrp",
            payload["dhgrp"],
            VALID_BODY_DHGRP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke1" in payload:
        is_valid, error = _validate_enum_field(
            "addke1",
            payload["addke1"],
            VALID_BODY_ADDKE1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke2" in payload:
        is_valid, error = _validate_enum_field(
            "addke2",
            payload["addke2"],
            VALID_BODY_ADDKE2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke3" in payload:
        is_valid, error = _validate_enum_field(
            "addke3",
            payload["addke3"],
            VALID_BODY_ADDKE3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke4" in payload:
        is_valid, error = _validate_enum_field(
            "addke4",
            payload["addke4"],
            VALID_BODY_ADDKE4,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke5" in payload:
        is_valid, error = _validate_enum_field(
            "addke5",
            payload["addke5"],
            VALID_BODY_ADDKE5,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke6" in payload:
        is_valid, error = _validate_enum_field(
            "addke6",
            payload["addke6"],
            VALID_BODY_ADDKE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "addke7" in payload:
        is_valid, error = _validate_enum_field(
            "addke7",
            payload["addke7"],
            VALID_BODY_ADDKE7,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "replay" in payload:
        is_valid, error = _validate_enum_field(
            "replay",
            payload["replay"],
            VALID_BODY_REPLAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "keepalive" in payload:
        is_valid, error = _validate_enum_field(
            "keepalive",
            payload["keepalive"],
            VALID_BODY_KEEPALIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "auto-negotiate",
            payload["auto-negotiate"],
            VALID_BODY_AUTO_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-route",
            payload["add-route"],
            VALID_BODY_ADD_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inbound-dscp-copy" in payload:
        is_valid, error = _validate_enum_field(
            "inbound-dscp-copy",
            payload["inbound-dscp-copy"],
            VALID_BODY_INBOUND_DSCP_COPY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "keylife-type" in payload:
        is_valid, error = _validate_enum_field(
            "keylife-type",
            payload["keylife-type"],
            VALID_BODY_KEYLIFE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "single-source" in payload:
        is_valid, error = _validate_enum_field(
            "single-source",
            payload["single-source"],
            VALID_BODY_SINGLE_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "route-overlap" in payload:
        is_valid, error = _validate_enum_field(
            "route-overlap",
            payload["route-overlap"],
            VALID_BODY_ROUTE_OVERLAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encapsulation" in payload:
        is_valid, error = _validate_enum_field(
            "encapsulation",
            payload["encapsulation"],
            VALID_BODY_ENCAPSULATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l2tp" in payload:
        is_valid, error = _validate_enum_field(
            "l2tp",
            payload["l2tp"],
            VALID_BODY_L2TP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "initiator-ts-narrow" in payload:
        is_valid, error = _validate_enum_field(
            "initiator-ts-narrow",
            payload["initiator-ts-narrow"],
            VALID_BODY_INITIATOR_TS_NARROW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv",
            payload["diffserv"],
            VALID_BODY_DIFFSERV,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "src-addr-type",
            payload["src-addr-type"],
            VALID_BODY_SRC_ADDR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dst-addr-type" in payload:
        is_valid, error = _validate_enum_field(
            "dst-addr-type",
            payload["dst-addr-type"],
            VALID_BODY_DST_ADDR_TYPE,
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
    "endpoint": "vpn/ipsec/phase2",
    "category": "cmdb",
    "api_path": "vpn.ipsec/phase2",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure VPN autokey tunnel.",
    "total_fields": 52,
    "required_fields_count": 6,
    "fields_with_defaults_count": 51,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
