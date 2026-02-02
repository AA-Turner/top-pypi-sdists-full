"""Validation helpers for system/modem - Auto-generated"""

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
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
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
    "status": "option",  # Enable/disable Modem support (equivalent to bringing an inte
    "pin-init": "string",  # AT command to set the PIN (AT+PIN=<pin>).
    "network-init": "string",  # AT command to set the Network name/type (AT+COPS=<mode>,[<fo
    "lockdown-lac": "string",  # Allow connection only to the specified Location Area Code (L
    "mode": "option",  # Set MODEM operation mode to redundant or standalone.   
stan
    "auto-dial": "option",  # Enable/disable auto-dial after a reboot or disconnection.   
    "dial-on-demand": "option",  # Enable/disable to dial the modem when packets are routed to 
    "idle-timer": "integer",  # MODEM connection idle time (1 - 9999 min, default = 5).
    "redial": "option",  # Redial limit (1 - 10 attempts, none = redial forever).   
no
    "reset": "integer",  # Number of dial attempts before resetting modem (0 = never re
    "holddown-timer": "integer",  # Hold down timer in seconds (1 - 60 sec).
    "connect-timeout": "integer",  # Connection completion timeout (30 - 255 sec, default = 90).
    "interface": "string",  # Name of redundant interface.
    "wireless-port": "integer",  # Enter wireless port number: 0 for default, 1 for first port,
    "dont-send-CR1": "option",  # Do not send CR when connected (ISP1).   
enable:Enable setti
    "phone1": "string",  # Phone number to connect to the dialup account (must not cont
    "dial-cmd1": "string",  # Dial command (this is often an ATD or ATDT command).
    "username1": "string",  # User name to access the specified dialup account.
    "passwd1": "string",  # Password to access the specified dialup account.
    "extra-init1": "string",  # Extra initialization string to ISP 1.
    "peer-modem1": "option",  # Specify peer MODEM type for phone1.   
generic:All other mod
    "ppp-echo-request1": "option",  # Enable/disable PPP echo-request to ISP 1.   
enable:Enable s
    "authtype1": "option",  # Allowed authentication types for ISP 1.   
pap:PAP   
chap:C
    "dont-send-CR2": "option",  # Do not send CR when connected (ISP2).   
enable:Enable setti
    "phone2": "string",  # Phone number to connect to the dialup account (must not cont
    "dial-cmd2": "string",  # Dial command (this is often an ATD or ATDT command).
    "username2": "string",  # User name to access the specified dialup account.
    "passwd2": "string",  # Password to access the specified dialup account.
    "extra-init2": "string",  # Extra initialization string to ISP 2.
    "peer-modem2": "option",  # Specify peer MODEM type for phone2.   
generic:All other mod
    "ppp-echo-request2": "option",  # Enable/disable PPP echo-request to ISP 2.   
enable:Enable s
    "authtype2": "option",  # Allowed authentication types for ISP 2.   
pap:PAP   
chap:C
    "dont-send-CR3": "option",  # Do not send CR when connected (ISP3).   
enable:Enable setti
    "phone3": "string",  # Phone number to connect to the dialup account (must not cont
    "dial-cmd3": "string",  # Dial command (this is often an ATD or ATDT command).
    "username3": "string",  # User name to access the specified dialup account.
    "passwd3": "string",  # Password to access the specified dialup account.
    "extra-init3": "string",  # Extra initialization string to ISP 3.
    "peer-modem3": "option",  # Specify peer MODEM type for phone3.   
generic:All other mod
    "ppp-echo-request3": "option",  # Enable/disable PPP echo-request to ISP 3.   
enable:Enable s
    "altmode": "option",  # Enable/disable altmode for installations using PPP in China.
    "authtype3": "option",  # Allowed authentication types for ISP 3.   
pap:PAP   
chap:C
    "traffic-check": "option",  # Enable/disable traffic-check.   
enable:Enable setting.   
d
    "action": "option",  # Dial up/stop MODEM.   
dial:Dial up number.   
stop:Stop dia
    "distance": "integer",  # Distance of learned routes (1 - 255, default = 1).
    "priority": "integer",  # Priority of learned routes (1 - 65535, default = 1).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "status": "Enable/disable Modem support (equivalent to bringing an interface up or down).    enable:Enable setting.    disable:Disable setting.",
    "pin-init": "AT command to set the PIN (AT+PIN=<pin>).",
    "network-init": "AT command to set the Network name/type (AT+COPS=<mode>,[<format>,<oper>[,<AcT>]]).",
    "lockdown-lac": "Allow connection only to the specified Location Area Code (LAC).",
    "mode": "Set MODEM operation mode to redundant or standalone.    standalone:Standalone.    redundant:Redundant for an interface.",
    "auto-dial": "Enable/disable auto-dial after a reboot or disconnection.    enable:Enable setting.    disable:Disable setting.",
    "dial-on-demand": "Enable/disable to dial the modem when packets are routed to the modem interface.    enable:Enable setting.    disable:Disable setting.",
    "idle-timer": "MODEM connection idle time (1 - 9999 min, default = 5).",
    "redial": "Redial limit (1 - 10 attempts, none = redial forever).    none:Forever.    1:One attempt.    2:Two attempts.    3:Three attempts.    4:Four attempts.    5:Five attempts.    6:Six attempts.    7:Seven attempts.    8:Eight attempts.    9:Nine attempts.    10:Ten attempts.",
    "reset": "Number of dial attempts before resetting modem (0 = never reset).",
    "holddown-timer": "Hold down timer in seconds (1 - 60 sec).",
    "connect-timeout": "Connection completion timeout (30 - 255 sec, default = 90).",
    "interface": "Name of redundant interface.",
    "wireless-port": "Enter wireless port number: 0 for default, 1 for first port, and so on (0 - 4294967295).",
    "dont-send-CR1": "Do not send CR when connected (ISP1).    enable:Enable setting.    disable:Disable setting.",
    "phone1": "Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).",
    "dial-cmd1": "Dial command (this is often an ATD or ATDT command).",
    "username1": "User name to access the specified dialup account.",
    "passwd1": "Password to access the specified dialup account.",
    "extra-init1": "Extra initialization string to ISP 1.",
    "peer-modem1": "Specify peer MODEM type for phone1.    generic:All other modem type.    actiontec:ActionTec modem.    ascend_TNT:Ascend TNT modem.",
    "ppp-echo-request1": "Enable/disable PPP echo-request to ISP 1.    enable:Enable setting.    disable:Disable setting.",
    "authtype1": "Allowed authentication types for ISP 1.    pap:PAP    chap:CHAP    mschap:MSCHAP    mschapv2:MSCHAPv2",
    "dont-send-CR2": "Do not send CR when connected (ISP2).    enable:Enable setting.    disable:Disable setting.",
    "phone2": "Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).",
    "dial-cmd2": "Dial command (this is often an ATD or ATDT command).",
    "username2": "User name to access the specified dialup account.",
    "passwd2": "Password to access the specified dialup account.",
    "extra-init2": "Extra initialization string to ISP 2.",
    "peer-modem2": "Specify peer MODEM type for phone2.    generic:All other modem type.    actiontec:ActionTec modem.    ascend_TNT:Ascend TNT modem.",
    "ppp-echo-request2": "Enable/disable PPP echo-request to ISP 2.    enable:Enable setting.    disable:Disable setting.",
    "authtype2": "Allowed authentication types for ISP 2.    pap:PAP    chap:CHAP    mschap:MSCHAP    mschapv2:MSCHAPv2",
    "dont-send-CR3": "Do not send CR when connected (ISP3).    enable:Enable setting.    disable:Disable setting.",
    "phone3": "Phone number to connect to the dialup account (must not contain spaces, and should include standard special characters).",
    "dial-cmd3": "Dial command (this is often an ATD or ATDT command).",
    "username3": "User name to access the specified dialup account.",
    "passwd3": "Password to access the specified dialup account.",
    "extra-init3": "Extra initialization string to ISP 3.",
    "peer-modem3": "Specify peer MODEM type for phone3.    generic:All other modem type.    actiontec:ActionTec modem.    ascend_TNT:Ascend TNT modem.",
    "ppp-echo-request3": "Enable/disable PPP echo-request to ISP 3.    enable:Enable setting.    disable:Disable setting.",
    "altmode": "Enable/disable altmode for installations using PPP in China.    enable:Enable setting.    disable:Disable setting.",
    "authtype3": "Allowed authentication types for ISP 3.    pap:PAP    chap:CHAP    mschap:MSCHAP    mschapv2:MSCHAPv2",
    "traffic-check": "Enable/disable traffic-check.    enable:Enable setting.    disable:Disable setting.",
    "action": "Dial up/stop MODEM.    dial:Dial up number.    stop:Stop dialup.    none:No action.",
    "distance": "Distance of learned routes (1 - 255, default = 1).",
    "priority": "Priority of learned routes (1 - 65535, default = 1).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_MODE = [
    "standalone",
    "redundant",
]
VALID_BODY_AUTO_DIAL = [
    "enable",
    "disable",
]
VALID_BODY_DIAL_ON_DEMAND = [
    "enable",
    "disable",
]
VALID_BODY_REDIAL = [
    "none",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]
VALID_BODY_DONT_SEND_CR1 = [
    "enable",
    "disable",
]
VALID_BODY_PEER_MODEM1 = [
    "generic",
    "actiontec",
    "ascend_TNT",
]
VALID_BODY_PPP_ECHO_REQUEST1 = [
    "enable",
    "disable",
]
VALID_BODY_AUTHTYPE1 = [
    "pap",
    "chap",
    "mschap",
    "mschapv2",
]
VALID_BODY_DONT_SEND_CR2 = [
    "enable",
    "disable",
]
VALID_BODY_PEER_MODEM2 = [
    "generic",
    "actiontec",
    "ascend_TNT",
]
VALID_BODY_PPP_ECHO_REQUEST2 = [
    "enable",
    "disable",
]
VALID_BODY_AUTHTYPE2 = [
    "pap",
    "chap",
    "mschap",
    "mschapv2",
]
VALID_BODY_DONT_SEND_CR3 = [
    "enable",
    "disable",
]
VALID_BODY_PEER_MODEM3 = [
    "generic",
    "actiontec",
    "ascend_TNT",
]
VALID_BODY_PPP_ECHO_REQUEST3 = [
    "enable",
    "disable",
]
VALID_BODY_ALTMODE = [
    "enable",
    "disable",
]
VALID_BODY_AUTHTYPE3 = [
    "pap",
    "chap",
    "mschap",
    "mschapv2",
]
VALID_BODY_TRAFFIC_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_ACTION = [
    "dial",
    "stop",
    "none",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_modem_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/modem."""
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


def validate_system_modem_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/modem object."""
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
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-dial" in payload:
        is_valid, error = _validate_enum_field(
            "auto-dial",
            payload["auto-dial"],
            VALID_BODY_AUTO_DIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dial-on-demand" in payload:
        is_valid, error = _validate_enum_field(
            "dial-on-demand",
            payload["dial-on-demand"],
            VALID_BODY_DIAL_ON_DEMAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redial" in payload:
        is_valid, error = _validate_enum_field(
            "redial",
            payload["redial"],
            VALID_BODY_REDIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dont-send-CR1" in payload:
        is_valid, error = _validate_enum_field(
            "dont-send-CR1",
            payload["dont-send-CR1"],
            VALID_BODY_DONT_SEND_CR1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-modem1" in payload:
        is_valid, error = _validate_enum_field(
            "peer-modem1",
            payload["peer-modem1"],
            VALID_BODY_PEER_MODEM1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppp-echo-request1" in payload:
        is_valid, error = _validate_enum_field(
            "ppp-echo-request1",
            payload["ppp-echo-request1"],
            VALID_BODY_PPP_ECHO_REQUEST1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype1" in payload:
        is_valid, error = _validate_enum_field(
            "authtype1",
            payload["authtype1"],
            VALID_BODY_AUTHTYPE1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dont-send-CR2" in payload:
        is_valid, error = _validate_enum_field(
            "dont-send-CR2",
            payload["dont-send-CR2"],
            VALID_BODY_DONT_SEND_CR2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-modem2" in payload:
        is_valid, error = _validate_enum_field(
            "peer-modem2",
            payload["peer-modem2"],
            VALID_BODY_PEER_MODEM2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppp-echo-request2" in payload:
        is_valid, error = _validate_enum_field(
            "ppp-echo-request2",
            payload["ppp-echo-request2"],
            VALID_BODY_PPP_ECHO_REQUEST2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype2" in payload:
        is_valid, error = _validate_enum_field(
            "authtype2",
            payload["authtype2"],
            VALID_BODY_AUTHTYPE2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dont-send-CR3" in payload:
        is_valid, error = _validate_enum_field(
            "dont-send-CR3",
            payload["dont-send-CR3"],
            VALID_BODY_DONT_SEND_CR3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-modem3" in payload:
        is_valid, error = _validate_enum_field(
            "peer-modem3",
            payload["peer-modem3"],
            VALID_BODY_PEER_MODEM3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppp-echo-request3" in payload:
        is_valid, error = _validate_enum_field(
            "ppp-echo-request3",
            payload["ppp-echo-request3"],
            VALID_BODY_PPP_ECHO_REQUEST3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "altmode" in payload:
        is_valid, error = _validate_enum_field(
            "altmode",
            payload["altmode"],
            VALID_BODY_ALTMODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype3" in payload:
        is_valid, error = _validate_enum_field(
            "authtype3",
            payload["authtype3"],
            VALID_BODY_AUTHTYPE3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-check" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-check",
            payload["traffic-check"],
            VALID_BODY_TRAFFIC_CHECK,
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

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_modem_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/modem."""
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
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-dial" in payload:
        is_valid, error = _validate_enum_field(
            "auto-dial",
            payload["auto-dial"],
            VALID_BODY_AUTO_DIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dial-on-demand" in payload:
        is_valid, error = _validate_enum_field(
            "dial-on-demand",
            payload["dial-on-demand"],
            VALID_BODY_DIAL_ON_DEMAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "redial" in payload:
        is_valid, error = _validate_enum_field(
            "redial",
            payload["redial"],
            VALID_BODY_REDIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dont-send-CR1" in payload:
        is_valid, error = _validate_enum_field(
            "dont-send-CR1",
            payload["dont-send-CR1"],
            VALID_BODY_DONT_SEND_CR1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-modem1" in payload:
        is_valid, error = _validate_enum_field(
            "peer-modem1",
            payload["peer-modem1"],
            VALID_BODY_PEER_MODEM1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppp-echo-request1" in payload:
        is_valid, error = _validate_enum_field(
            "ppp-echo-request1",
            payload["ppp-echo-request1"],
            VALID_BODY_PPP_ECHO_REQUEST1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype1" in payload:
        is_valid, error = _validate_enum_field(
            "authtype1",
            payload["authtype1"],
            VALID_BODY_AUTHTYPE1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dont-send-CR2" in payload:
        is_valid, error = _validate_enum_field(
            "dont-send-CR2",
            payload["dont-send-CR2"],
            VALID_BODY_DONT_SEND_CR2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-modem2" in payload:
        is_valid, error = _validate_enum_field(
            "peer-modem2",
            payload["peer-modem2"],
            VALID_BODY_PEER_MODEM2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppp-echo-request2" in payload:
        is_valid, error = _validate_enum_field(
            "ppp-echo-request2",
            payload["ppp-echo-request2"],
            VALID_BODY_PPP_ECHO_REQUEST2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype2" in payload:
        is_valid, error = _validate_enum_field(
            "authtype2",
            payload["authtype2"],
            VALID_BODY_AUTHTYPE2,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dont-send-CR3" in payload:
        is_valid, error = _validate_enum_field(
            "dont-send-CR3",
            payload["dont-send-CR3"],
            VALID_BODY_DONT_SEND_CR3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "peer-modem3" in payload:
        is_valid, error = _validate_enum_field(
            "peer-modem3",
            payload["peer-modem3"],
            VALID_BODY_PEER_MODEM3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppp-echo-request3" in payload:
        is_valid, error = _validate_enum_field(
            "ppp-echo-request3",
            payload["ppp-echo-request3"],
            VALID_BODY_PPP_ECHO_REQUEST3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "altmode" in payload:
        is_valid, error = _validate_enum_field(
            "altmode",
            payload["altmode"],
            VALID_BODY_ALTMODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authtype3" in payload:
        is_valid, error = _validate_enum_field(
            "authtype3",
            payload["authtype3"],
            VALID_BODY_AUTHTYPE3,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-check" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-check",
            payload["traffic-check"],
            VALID_BODY_TRAFFIC_CHECK,
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
    "endpoint": "system/modem",
    "category": "cmdb",
    "api_path": "system/modem",
    "help": "Configuration for system/modem",
    "total_fields": 46,
    "required_fields_count": 0,
    "fields_with_defaults_count": 0,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
