"""Validation helpers for wireless_controller/wtp - Auto-generated"""

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
    "wtp-id",  # WTP ID.
    "wtp-profile",  # WTP profile name to apply to this WTP, AP or FortiAP.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "wtp-id": "",
    "index": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "admin": "enable",
    "name": "",
    "location": "",
    "region": "",
    "region-x": "0",
    "region-y": "0",
    "firmware-provision": "",
    "firmware-provision-latest": "disable",
    "wtp-profile": "",
    "apcfg-profile": "",
    "bonjour-profile": "",
    "ble-major-id": 0,
    "ble-minor-id": 0,
    "override-led-state": "disable",
    "led-state": "enable",
    "override-wan-port-mode": "disable",
    "wan-port-mode": "wan-only",
    "override-ip-fragment": "disable",
    "ip-fragment-preventing": "tcp-mss-adjust",
    "tun-mtu-uplink": 0,
    "tun-mtu-downlink": 0,
    "override-split-tunnel": "disable",
    "split-tunneling-acl-path": "local",
    "split-tunneling-acl-local-ap-subnet": "disable",
    "override-lan": "disable",
    "override-allowaccess": "disable",
    "allowaccess": "",
    "override-login-passwd-change": "disable",
    "login-passwd-change": "no",
    "override-default-mesh-root": "disable",
    "default-mesh-root": "disable",
    "image-download": "enable",
    "mesh-bridge-enable": "default",
    "purdue-level": "3",
    "coordinate-latitude": "",
    "coordinate-longitude": "",
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
    "wtp-id": "string",  # WTP ID.
    "index": "integer",  # Index (0 - 4294967295).
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned 
    "admin": "option",  # Configure how the FortiGate operating as a wireless controll
    "name": "string",  # WTP, AP or FortiAP configuration name.
    "location": "string",  # Field for describing the physical location of the WTP, AP or
    "comment": "var-string",  # Comment.
    "region": "string",  # Region name WTP is associated with.
    "region-x": "string",  # Relative horizontal region coordinate (between 0 and 1).
    "region-y": "string",  # Relative vertical region coordinate (between 0 and 1).
    "firmware-provision": "string",  # Firmware version to provision to this FortiAP on bootup (maj
    "firmware-provision-latest": "option",  # Enable/disable one-time automatic provisioning of the latest
    "wtp-profile": "string",  # WTP profile name to apply to this WTP, AP or FortiAP.
    "apcfg-profile": "string",  # AP local configuration profile name.
    "bonjour-profile": "string",  # Bonjour profile name.
    "ble-major-id": "integer",  # Override BLE Major ID.
    "ble-minor-id": "integer",  # Override BLE Minor ID.
    "override-led-state": "option",  # Enable to override the profile LED state setting for this Fo
    "led-state": "option",  # Enable to allow the FortiAPs LEDs to light. Disable to keep 
    "override-wan-port-mode": "option",  # Enable/disable overriding the wan-port-mode in the WTP profi
    "wan-port-mode": "option",  # Enable/disable using the FortiAP WAN port as a LAN port.
    "override-ip-fragment": "option",  # Enable/disable overriding the WTP profile IP fragment preven
    "ip-fragment-preventing": "option",  # Method(s) by which IP fragmentation is prevented for control
    "tun-mtu-uplink": "integer",  # The maximum transmission unit (MTU) of uplink CAPWAP tunnel 
    "tun-mtu-downlink": "integer",  # The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 
    "override-split-tunnel": "option",  # Enable/disable overriding the WTP profile split tunneling se
    "split-tunneling-acl-path": "option",  # Split tunneling ACL path is local/tunnel.
    "split-tunneling-acl-local-ap-subnet": "option",  # Enable/disable automatically adding local subnetwork of Fort
    "split-tunneling-acl": "string",  # Split tunneling ACL filter list.
    "override-lan": "option",  # Enable to override the WTP profile LAN port setting.
    "lan": "string",  # WTP LAN port mapping.
    "override-allowaccess": "option",  # Enable to override the WTP profile management access configu
    "allowaccess": "option",  # Control management access to the managed WTP, FortiAP, or AP
    "override-login-passwd-change": "option",  # Enable to override the WTP profile login-password (administr
    "login-passwd-change": "option",  # Change or reset the administrator password of a managed WTP,
    "login-passwd": "password",  # Set the managed WTP, FortiAP, or AP's administrator password
    "override-default-mesh-root": "option",  # Enable to override the WTP profile default mesh root SSID se
    "default-mesh-root": "option",  # Configure default mesh root SSID when it is not included by 
    "radio-1": "string",  # Configuration options for radio 1.
    "radio-2": "string",  # Configuration options for radio 2.
    "radio-3": "string",  # Configuration options for radio 3.
    "radio-4": "string",  # Configuration options for radio 4.
    "image-download": "option",  # Enable/disable WTP image download.
    "mesh-bridge-enable": "option",  # Enable/disable mesh Ethernet bridge when WTP is configured a
    "purdue-level": "option",  # Purdue Level of this WTP.
    "coordinate-latitude": "string",  # WTP latitude coordinate.
    "coordinate-longitude": "string",  # WTP longitude coordinate.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "wtp-id": "WTP ID.",
    "index": "Index (0 - 4294967295).",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "admin": "Configure how the FortiGate operating as a wireless controller discovers and manages this WTP, AP or FortiAP.",
    "name": "WTP, AP or FortiAP configuration name.",
    "location": "Field for describing the physical location of the WTP, AP or FortiAP.",
    "comment": "Comment.",
    "region": "Region name WTP is associated with.",
    "region-x": "Relative horizontal region coordinate (between 0 and 1).",
    "region-y": "Relative vertical region coordinate (between 0 and 1).",
    "firmware-provision": "Firmware version to provision to this FortiAP on bootup (major.minor.build, i.e. 6.2.1234).",
    "firmware-provision-latest": "Enable/disable one-time automatic provisioning of the latest firmware version.",
    "wtp-profile": "WTP profile name to apply to this WTP, AP or FortiAP.",
    "apcfg-profile": "AP local configuration profile name.",
    "bonjour-profile": "Bonjour profile name.",
    "ble-major-id": "Override BLE Major ID.",
    "ble-minor-id": "Override BLE Minor ID.",
    "override-led-state": "Enable to override the profile LED state setting for this FortiAP. You must enable this option to use the led-state command to turn off the FortiAP's LEDs.",
    "led-state": "Enable to allow the FortiAPs LEDs to light. Disable to keep the LEDs off. You may want to keep the LEDs off so they are not distracting in low light areas etc.",
    "override-wan-port-mode": "Enable/disable overriding the wan-port-mode in the WTP profile.",
    "wan-port-mode": "Enable/disable using the FortiAP WAN port as a LAN port.",
    "override-ip-fragment": "Enable/disable overriding the WTP profile IP fragment prevention setting.",
    "ip-fragment-preventing": "Method(s) by which IP fragmentation is prevented for control and data packets through CAPWAP tunnel (default = tcp-mss-adjust).",
    "tun-mtu-uplink": "The maximum transmission unit (MTU) of uplink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).",
    "tun-mtu-downlink": "The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).",
    "override-split-tunnel": "Enable/disable overriding the WTP profile split tunneling setting.",
    "split-tunneling-acl-path": "Split tunneling ACL path is local/tunnel.",
    "split-tunneling-acl-local-ap-subnet": "Enable/disable automatically adding local subnetwork of FortiAP to split-tunneling ACL (default = disable).",
    "split-tunneling-acl": "Split tunneling ACL filter list.",
    "override-lan": "Enable to override the WTP profile LAN port setting.",
    "lan": "WTP LAN port mapping.",
    "override-allowaccess": "Enable to override the WTP profile management access configuration.",
    "allowaccess": "Control management access to the managed WTP, FortiAP, or AP. Separate entries with a space.",
    "override-login-passwd-change": "Enable to override the WTP profile login-password (administrator password) setting.",
    "login-passwd-change": "Change or reset the administrator password of a managed WTP, FortiAP or AP (yes, default, or no, default = no).",
    "login-passwd": "Set the managed WTP, FortiAP, or AP's administrator password.",
    "override-default-mesh-root": "Enable to override the WTP profile default mesh root SSID setting.",
    "default-mesh-root": "Configure default mesh root SSID when it is not included by radio's SSID configuration.",
    "radio-1": "Configuration options for radio 1.",
    "radio-2": "Configuration options for radio 2.",
    "radio-3": "Configuration options for radio 3.",
    "radio-4": "Configuration options for radio 4.",
    "image-download": "Enable/disable WTP image download.",
    "mesh-bridge-enable": "Enable/disable mesh Ethernet bridge when WTP is configured as a mesh branch/leaf AP.",
    "purdue-level": "Purdue Level of this WTP.",
    "coordinate-latitude": "WTP latitude coordinate.",
    "coordinate-longitude": "WTP longitude coordinate.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "wtp-id": {"type": "string", "max_length": 35},
    "index": {"type": "integer", "min": 0, "max": 4294967295},
    "name": {"type": "string", "max_length": 35},
    "location": {"type": "string", "max_length": 35},
    "region": {"type": "string", "max_length": 35},
    "region-x": {"type": "string", "max_length": 15},
    "region-y": {"type": "string", "max_length": 15},
    "firmware-provision": {"type": "string", "max_length": 35},
    "wtp-profile": {"type": "string", "max_length": 35},
    "apcfg-profile": {"type": "string", "max_length": 35},
    "bonjour-profile": {"type": "string", "max_length": 35},
    "ble-major-id": {"type": "integer", "min": 0, "max": 65535},
    "ble-minor-id": {"type": "integer", "min": 0, "max": 65535},
    "tun-mtu-uplink": {"type": "integer", "min": 576, "max": 1500},
    "tun-mtu-downlink": {"type": "integer", "min": 576, "max": 1500},
    "coordinate-latitude": {"type": "string", "max_length": 19},
    "coordinate-longitude": {"type": "string", "max_length": 19},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "split-tunneling-acl": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "dest-ip": {
            "type": "ipv4-classnet",
            "help": "Destination IP and mask for the split-tunneling subnet.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
    },
    "lan": {
        "port-mode": {
            "type": "option",
            "help": "LAN port mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port-ssid": {
            "type": "string",
            "help": "Bridge LAN port to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port1-mode": {
            "type": "option",
            "help": "LAN port 1 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port1-ssid": {
            "type": "string",
            "help": "Bridge LAN port 1 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port2-mode": {
            "type": "option",
            "help": "LAN port 2 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port2-ssid": {
            "type": "string",
            "help": "Bridge LAN port 2 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port3-mode": {
            "type": "option",
            "help": "LAN port 3 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port3-ssid": {
            "type": "string",
            "help": "Bridge LAN port 3 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port4-mode": {
            "type": "option",
            "help": "LAN port 4 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port4-ssid": {
            "type": "string",
            "help": "Bridge LAN port 4 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port5-mode": {
            "type": "option",
            "help": "LAN port 5 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port5-ssid": {
            "type": "string",
            "help": "Bridge LAN port 5 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port6-mode": {
            "type": "option",
            "help": "LAN port 6 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port6-ssid": {
            "type": "string",
            "help": "Bridge LAN port 6 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port7-mode": {
            "type": "option",
            "help": "LAN port 7 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port7-ssid": {
            "type": "string",
            "help": "Bridge LAN port 7 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port8-mode": {
            "type": "option",
            "help": "LAN port 8 mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port8-ssid": {
            "type": "string",
            "help": "Bridge LAN port 8 to SSID.",
            "default": "",
            "max_length": 15,
        },
        "port-esl-mode": {
            "type": "option",
            "help": "ESL port mode.",
            "default": "offline",
            "options": ["offline", "nat-to-wan", "bridge-to-wan", "bridge-to-ssid"],
        },
        "port-esl-ssid": {
            "type": "string",
            "help": "Bridge ESL port to SSID.",
            "default": "",
            "max_length": 15,
        },
    },
    "radio-1": {
        "override-band": {
            "type": "option",
            "help": "Enable to override the WTP profile band setting.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 1 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "override-txpower": {
            "type": "option",
            "help": "Enable to override the WTP profile power level configuration.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-high": {
            "type": "integer",
            "help": "The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 17,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-low": {
            "type": "integer",
            "help": "The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 10,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-target": {
            "type": "string",
            "help": "Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).",
            "default": "-70",
            "max_length": 7,
        },
        "power-mode": {
            "type": "option",
            "help": "Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.",
            "default": "percentage",
            "options": ["dBm", "percentage"],
        },
        "power-level": {
            "type": "integer",
            "help": "Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 100,
        },
        "power-value": {
            "type": "integer",
            "help": "Radio EIRP power in dBm (1 - 33, default = 27).",
            "default": 27,
            "min_value": 1,
            "max_value": 33,
        },
        "override-vaps": {
            "type": "option",
            "help": "Enable to override WTP profile Virtual Access Point (VAP) settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "vap-all": {
            "type": "option",
            "help": "Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).",
            "default": "tunnel",
            "options": ["tunnel", "bridge", "manual"],
        },
        "vaps": {
            "type": "string",
            "help": "Manually selected list of Virtual Access Points (VAPs).",
        },
        "override-channel": {
            "type": "option",
            "help": "Enable to override WTP profile channel settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "drma-manual-mode": {
            "type": "option",
            "help": "Radio mode to be used for DRMA manual mode (default = ncf).",
            "default": "ncf",
            "options": ["ap", "monitor", "ncf", "ncf-peek"],
        },
    },
    "radio-2": {
        "override-band": {
            "type": "option",
            "help": "Enable to override the WTP profile band setting.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 2 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "override-txpower": {
            "type": "option",
            "help": "Enable to override the WTP profile power level configuration.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-high": {
            "type": "integer",
            "help": "The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 17,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-low": {
            "type": "integer",
            "help": "The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 10,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-target": {
            "type": "string",
            "help": "Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).",
            "default": "-70",
            "max_length": 7,
        },
        "power-mode": {
            "type": "option",
            "help": "Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.",
            "default": "percentage",
            "options": ["dBm", "percentage"],
        },
        "power-level": {
            "type": "integer",
            "help": "Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 100,
        },
        "power-value": {
            "type": "integer",
            "help": "Radio EIRP power in dBm (1 - 33, default = 27).",
            "default": 27,
            "min_value": 1,
            "max_value": 33,
        },
        "override-vaps": {
            "type": "option",
            "help": "Enable to override WTP profile Virtual Access Point (VAP) settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "vap-all": {
            "type": "option",
            "help": "Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).",
            "default": "tunnel",
            "options": ["tunnel", "bridge", "manual"],
        },
        "vaps": {
            "type": "string",
            "help": "Manually selected list of Virtual Access Points (VAPs).",
        },
        "override-channel": {
            "type": "option",
            "help": "Enable to override WTP profile channel settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "drma-manual-mode": {
            "type": "option",
            "help": "Radio mode to be used for DRMA manual mode (default = ncf).",
            "default": "ncf",
            "options": ["ap", "monitor", "ncf", "ncf-peek"],
        },
    },
    "radio-3": {
        "override-band": {
            "type": "option",
            "help": "Enable to override the WTP profile band setting.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 3 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "override-txpower": {
            "type": "option",
            "help": "Enable to override the WTP profile power level configuration.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-high": {
            "type": "integer",
            "help": "The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 17,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-low": {
            "type": "integer",
            "help": "The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 10,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-target": {
            "type": "string",
            "help": "Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).",
            "default": "-70",
            "max_length": 7,
        },
        "power-mode": {
            "type": "option",
            "help": "Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.",
            "default": "percentage",
            "options": ["dBm", "percentage"],
        },
        "power-level": {
            "type": "integer",
            "help": "Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 100,
        },
        "power-value": {
            "type": "integer",
            "help": "Radio EIRP power in dBm (1 - 33, default = 27).",
            "default": 27,
            "min_value": 1,
            "max_value": 33,
        },
        "override-vaps": {
            "type": "option",
            "help": "Enable to override WTP profile Virtual Access Point (VAP) settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "vap-all": {
            "type": "option",
            "help": "Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).",
            "default": "tunnel",
            "options": ["tunnel", "bridge", "manual"],
        },
        "vaps": {
            "type": "string",
            "help": "Manually selected list of Virtual Access Points (VAPs).",
        },
        "override-channel": {
            "type": "option",
            "help": "Enable to override WTP profile channel settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "drma-manual-mode": {
            "type": "option",
            "help": "Radio mode to be used for DRMA manual mode (default = ncf).",
            "default": "ncf",
            "options": ["ap", "monitor", "ncf", "ncf-peek"],
        },
    },
    "radio-4": {
        "override-band": {
            "type": "option",
            "help": "Enable to override the WTP profile band setting.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 4 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "override-txpower": {
            "type": "option",
            "help": "Enable to override the WTP profile power level configuration.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = enable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "auto-power-high": {
            "type": "integer",
            "help": "The upper bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 17,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-low": {
            "type": "integer",
            "help": "The lower bound of automatic transmit power adjustment in dBm (the actual range of transmit power depends on the AP platform type).",
            "default": 10,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "auto-power-target": {
            "type": "string",
            "help": "Target of automatic transmit power adjustment in dBm (-95 to -20, default = -70).",
            "default": "-70",
            "max_length": 7,
        },
        "power-mode": {
            "type": "option",
            "help": "Set radio effective isotropic radiated power (EIRP) in dBm or by a percentage of the maximum EIRP (default = percentage). This power takes into account both radio transmit power and antenna gain. Higher power level settings may be constrained by local regulatory requirements and AP capabilities.",
            "default": "percentage",
            "options": ["dBm", "percentage"],
        },
        "power-level": {
            "type": "integer",
            "help": "Radio EIRP power level as a percentage of the maximum EIRP power (0 - 100, default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 100,
        },
        "power-value": {
            "type": "integer",
            "help": "Radio EIRP power in dBm (1 - 33, default = 27).",
            "default": 27,
            "min_value": 1,
            "max_value": 33,
        },
        "override-vaps": {
            "type": "option",
            "help": "Enable to override WTP profile Virtual Access Point (VAP) settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "vap-all": {
            "type": "option",
            "help": "Configure method for assigning SSIDs to this FortiAP (default = automatically assign tunnel SSIDs).",
            "default": "tunnel",
            "options": ["tunnel", "bridge", "manual"],
        },
        "vaps": {
            "type": "string",
            "help": "Manually selected list of Virtual Access Points (VAPs).",
        },
        "override-channel": {
            "type": "option",
            "help": "Enable to override WTP profile channel settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "drma-manual-mode": {
            "type": "option",
            "help": "Radio mode to be used for DRMA manual mode (default = ncf).",
            "default": "ncf",
            "options": ["ap", "monitor", "ncf", "ncf-peek"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_ADMIN = [
    "discovered",
    "disable",
    "enable",
]
VALID_BODY_FIRMWARE_PROVISION_LATEST = [
    "disable",
    "once",
]
VALID_BODY_OVERRIDE_LED_STATE = [
    "enable",
    "disable",
]
VALID_BODY_LED_STATE = [
    "enable",
    "disable",
]
VALID_BODY_OVERRIDE_WAN_PORT_MODE = [
    "enable",
    "disable",
]
VALID_BODY_WAN_PORT_MODE = [
    "wan-lan",
    "wan-only",
]
VALID_BODY_OVERRIDE_IP_FRAGMENT = [
    "enable",
    "disable",
]
VALID_BODY_IP_FRAGMENT_PREVENTING = [
    "tcp-mss-adjust",
    "icmp-unreachable",
]
VALID_BODY_OVERRIDE_SPLIT_TUNNEL = [
    "enable",
    "disable",
]
VALID_BODY_SPLIT_TUNNELING_ACL_PATH = [
    "tunnel",
    "local",
]
VALID_BODY_SPLIT_TUNNELING_ACL_LOCAL_AP_SUBNET = [
    "enable",
    "disable",
]
VALID_BODY_OVERRIDE_LAN = [
    "enable",
    "disable",
]
VALID_BODY_OVERRIDE_ALLOWACCESS = [
    "enable",
    "disable",
]
VALID_BODY_ALLOWACCESS = [
    "https",
    "ssh",
    "snmp",
]
VALID_BODY_OVERRIDE_LOGIN_PASSWD_CHANGE = [
    "enable",
    "disable",
]
VALID_BODY_LOGIN_PASSWD_CHANGE = [
    "yes",
    "default",
    "no",
]
VALID_BODY_OVERRIDE_DEFAULT_MESH_ROOT = [
    "enable",
    "disable",
]
VALID_BODY_DEFAULT_MESH_ROOT = [
    "enable",
    "disable",
]
VALID_BODY_IMAGE_DOWNLOAD = [
    "enable",
    "disable",
]
VALID_BODY_MESH_BRIDGE_ENABLE = [
    "default",
    "enable",
    "disable",
]
VALID_BODY_PURDUE_LEVEL = [
    "1",
    "1.5",
    "2",
    "2.5",
    "3",
    "3.5",
    "4",
    "5",
    "5.5",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_wtp_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/wtp."""
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


def validate_wireless_controller_wtp_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/wtp object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "admin" in payload:
        is_valid, error = _validate_enum_field(
            "admin",
            payload["admin"],
            VALID_BODY_ADMIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-latest" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-latest",
            payload["firmware-provision-latest"],
            VALID_BODY_FIRMWARE_PROVISION_LATEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-led-state" in payload:
        is_valid, error = _validate_enum_field(
            "override-led-state",
            payload["override-led-state"],
            VALID_BODY_OVERRIDE_LED_STATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "led-state" in payload:
        is_valid, error = _validate_enum_field(
            "led-state",
            payload["led-state"],
            VALID_BODY_LED_STATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-wan-port-mode" in payload:
        is_valid, error = _validate_enum_field(
            "override-wan-port-mode",
            payload["override-wan-port-mode"],
            VALID_BODY_OVERRIDE_WAN_PORT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-mode",
            payload["wan-port-mode"],
            VALID_BODY_WAN_PORT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-ip-fragment" in payload:
        is_valid, error = _validate_enum_field(
            "override-ip-fragment",
            payload["override-ip-fragment"],
            VALID_BODY_OVERRIDE_IP_FRAGMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-fragment-preventing" in payload:
        is_valid, error = _validate_enum_field(
            "ip-fragment-preventing",
            payload["ip-fragment-preventing"],
            VALID_BODY_IP_FRAGMENT_PREVENTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-split-tunnel" in payload:
        is_valid, error = _validate_enum_field(
            "override-split-tunnel",
            payload["override-split-tunnel"],
            VALID_BODY_OVERRIDE_SPLIT_TUNNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "split-tunneling-acl-path" in payload:
        is_valid, error = _validate_enum_field(
            "split-tunneling-acl-path",
            payload["split-tunneling-acl-path"],
            VALID_BODY_SPLIT_TUNNELING_ACL_PATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "split-tunneling-acl-local-ap-subnet" in payload:
        is_valid, error = _validate_enum_field(
            "split-tunneling-acl-local-ap-subnet",
            payload["split-tunneling-acl-local-ap-subnet"],
            VALID_BODY_SPLIT_TUNNELING_ACL_LOCAL_AP_SUBNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-lan" in payload:
        is_valid, error = _validate_enum_field(
            "override-lan",
            payload["override-lan"],
            VALID_BODY_OVERRIDE_LAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "override-allowaccess",
            payload["override-allowaccess"],
            VALID_BODY_OVERRIDE_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-login-passwd-change" in payload:
        is_valid, error = _validate_enum_field(
            "override-login-passwd-change",
            payload["override-login-passwd-change"],
            VALID_BODY_OVERRIDE_LOGIN_PASSWD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "login-passwd-change" in payload:
        is_valid, error = _validate_enum_field(
            "login-passwd-change",
            payload["login-passwd-change"],
            VALID_BODY_LOGIN_PASSWD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-default-mesh-root" in payload:
        is_valid, error = _validate_enum_field(
            "override-default-mesh-root",
            payload["override-default-mesh-root"],
            VALID_BODY_OVERRIDE_DEFAULT_MESH_ROOT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-mesh-root" in payload:
        is_valid, error = _validate_enum_field(
            "default-mesh-root",
            payload["default-mesh-root"],
            VALID_BODY_DEFAULT_MESH_ROOT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "image-download" in payload:
        is_valid, error = _validate_enum_field(
            "image-download",
            payload["image-download"],
            VALID_BODY_IMAGE_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mesh-bridge-enable" in payload:
        is_valid, error = _validate_enum_field(
            "mesh-bridge-enable",
            payload["mesh-bridge-enable"],
            VALID_BODY_MESH_BRIDGE_ENABLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "purdue-level" in payload:
        is_valid, error = _validate_enum_field(
            "purdue-level",
            payload["purdue-level"],
            VALID_BODY_PURDUE_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_wtp_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/wtp."""
    # Validate enum values using central function
    if "admin" in payload:
        is_valid, error = _validate_enum_field(
            "admin",
            payload["admin"],
            VALID_BODY_ADMIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firmware-provision-latest" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision-latest",
            payload["firmware-provision-latest"],
            VALID_BODY_FIRMWARE_PROVISION_LATEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-led-state" in payload:
        is_valid, error = _validate_enum_field(
            "override-led-state",
            payload["override-led-state"],
            VALID_BODY_OVERRIDE_LED_STATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "led-state" in payload:
        is_valid, error = _validate_enum_field(
            "led-state",
            payload["led-state"],
            VALID_BODY_LED_STATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-wan-port-mode" in payload:
        is_valid, error = _validate_enum_field(
            "override-wan-port-mode",
            payload["override-wan-port-mode"],
            VALID_BODY_OVERRIDE_WAN_PORT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-mode",
            payload["wan-port-mode"],
            VALID_BODY_WAN_PORT_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-ip-fragment" in payload:
        is_valid, error = _validate_enum_field(
            "override-ip-fragment",
            payload["override-ip-fragment"],
            VALID_BODY_OVERRIDE_IP_FRAGMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-fragment-preventing" in payload:
        is_valid, error = _validate_enum_field(
            "ip-fragment-preventing",
            payload["ip-fragment-preventing"],
            VALID_BODY_IP_FRAGMENT_PREVENTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-split-tunnel" in payload:
        is_valid, error = _validate_enum_field(
            "override-split-tunnel",
            payload["override-split-tunnel"],
            VALID_BODY_OVERRIDE_SPLIT_TUNNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "split-tunneling-acl-path" in payload:
        is_valid, error = _validate_enum_field(
            "split-tunneling-acl-path",
            payload["split-tunneling-acl-path"],
            VALID_BODY_SPLIT_TUNNELING_ACL_PATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "split-tunneling-acl-local-ap-subnet" in payload:
        is_valid, error = _validate_enum_field(
            "split-tunneling-acl-local-ap-subnet",
            payload["split-tunneling-acl-local-ap-subnet"],
            VALID_BODY_SPLIT_TUNNELING_ACL_LOCAL_AP_SUBNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-lan" in payload:
        is_valid, error = _validate_enum_field(
            "override-lan",
            payload["override-lan"],
            VALID_BODY_OVERRIDE_LAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "override-allowaccess",
            payload["override-allowaccess"],
            VALID_BODY_OVERRIDE_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-login-passwd-change" in payload:
        is_valid, error = _validate_enum_field(
            "override-login-passwd-change",
            payload["override-login-passwd-change"],
            VALID_BODY_OVERRIDE_LOGIN_PASSWD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "login-passwd-change" in payload:
        is_valid, error = _validate_enum_field(
            "login-passwd-change",
            payload["login-passwd-change"],
            VALID_BODY_LOGIN_PASSWD_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-default-mesh-root" in payload:
        is_valid, error = _validate_enum_field(
            "override-default-mesh-root",
            payload["override-default-mesh-root"],
            VALID_BODY_OVERRIDE_DEFAULT_MESH_ROOT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-mesh-root" in payload:
        is_valid, error = _validate_enum_field(
            "default-mesh-root",
            payload["default-mesh-root"],
            VALID_BODY_DEFAULT_MESH_ROOT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "image-download" in payload:
        is_valid, error = _validate_enum_field(
            "image-download",
            payload["image-download"],
            VALID_BODY_IMAGE_DOWNLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mesh-bridge-enable" in payload:
        is_valid, error = _validate_enum_field(
            "mesh-bridge-enable",
            payload["mesh-bridge-enable"],
            VALID_BODY_MESH_BRIDGE_ENABLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "purdue-level" in payload:
        is_valid, error = _validate_enum_field(
            "purdue-level",
            payload["purdue-level"],
            VALID_BODY_PURDUE_LEVEL,
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
    "endpoint": "wireless_controller/wtp",
    "category": "cmdb",
    "api_path": "wireless-controller/wtp",
    "mkey": "wtp-id",
    "mkey_type": "string",
    "help": "Configure Wireless Termination Points (WTPs), that is, FortiAPs or APs to be managed by FortiGate.",
    "total_fields": 47,
    "required_fields_count": 2,
    "fields_with_defaults_count": 39,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
