"""Validation helpers for wireless_controller/wtp_profile - Auto-generated"""

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
    "name": "",
    "control-message-offload": "ebp-frame aeroscout-tag ap-list sta-list sta-cap-list stats aeroscout-mu sta-health spectral-analysis",
    "bonjour-profile": "",
    "apcfg-profile": "",
    "apcfg-mesh": "disable",
    "apcfg-mesh-ap-type": "ethernet",
    "apcfg-mesh-ssid": "",
    "apcfg-mesh-eth-bridge": "disable",
    "ble-profile": "",
    "lw-profile": "",
    "syslog-profile": "",
    "wan-port-mode": "wan-only",
    "energy-efficient-ethernet": "disable",
    "led-state": "enable",
    "dtls-policy": "clear-text",
    "dtls-in-kernel": "disable",
    "max-clients": 0,
    "handoff-rssi": 25,
    "handoff-sta-thresh": 0,
    "handoff-roaming": "enable",
    "ap-country": "--",
    "ip-fragment-preventing": "tcp-mss-adjust",
    "tun-mtu-uplink": 0,
    "tun-mtu-downlink": 0,
    "split-tunneling-acl-path": "local",
    "split-tunneling-acl-local-ap-subnet": "disable",
    "allowaccess": "",
    "login-passwd-change": "no",
    "lldp": "enable",
    "poe-mode": "auto",
    "usb-port": "enable",
    "frequency-handoff": "disable",
    "ap-handoff": "disable",
    "default-mesh-root": "disable",
    "ext-info-enable": "enable",
    "indoor-outdoor-deployment": "platform-determined",
    "console-login": "enable",
    "wan-port-auth": "none",
    "wan-port-auth-usrname": "",
    "wan-port-auth-methods": "all",
    "wan-port-auth-macsec": "disable",
    "apcfg-auto-cert": "disable",
    "apcfg-auto-cert-enroll-protocol": "none",
    "apcfg-auto-cert-crypto-algo": "ec-secp256r1",
    "apcfg-auto-cert-est-server": "",
    "apcfg-auto-cert-est-ca-id": "",
    "apcfg-auto-cert-est-http-username": "",
    "apcfg-auto-cert-est-subject": "CN=FortiAP,DC=local,DC=COM",
    "apcfg-auto-cert-est-subject-alt-name": "",
    "apcfg-auto-cert-auto-regen-days": 30,
    "apcfg-auto-cert-est-https-ca": "",
    "apcfg-auto-cert-scep-keytype": "rsa",
    "apcfg-auto-cert-scep-keysize": "2048",
    "apcfg-auto-cert-scep-ec-name": "secp256r1",
    "apcfg-auto-cert-scep-sub-fully-dn": "",
    "apcfg-auto-cert-scep-url": "",
    "apcfg-auto-cert-scep-ca-id": "",
    "apcfg-auto-cert-scep-subject-alt-name": "",
    "apcfg-auto-cert-scep-https-ca": "",
    "unii-4-5ghz-band": "disable",
    "admin-auth-tacacs+": "",
    "admin-restrict-local": "disable",
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
    "name": "string",  # WTP (or FortiAP or AP) profile name.
    "comment": "var-string",  # Comment.
    "platform": "string",  # WTP, FortiAP, or AP platform.
    "control-message-offload": "option",  # Enable/disable CAPWAP control message data channel offload.
    "bonjour-profile": "string",  # Bonjour profile name.
    "apcfg-profile": "string",  # AP local configuration profile name.
    "apcfg-mesh": "option",  # Enable/disable AP local mesh configuration (default = disable).
    "apcfg-mesh-ap-type": "option",  # Mesh AP Type (default = ethernet).
    "apcfg-mesh-ssid": "string",  #  Mesh SSID (default = none).
    "apcfg-mesh-eth-bridge": "option",  # Enable/disable mesh ethernet bridge (default = disable).
    "ble-profile": "string",  # Bluetooth Low Energy profile name.
    "lw-profile": "string",  # LoRaWAN profile name.
    "syslog-profile": "string",  # System log server configuration profile name.
    "wan-port-mode": "option",  # Enable/disable using a WAN port as a LAN port.
    "lan": "string",  # WTP LAN port mapping.
    "energy-efficient-ethernet": "option",  # Enable/disable use of energy efficient Ethernet on WTP.
    "led-state": "option",  # Enable/disable use of LEDs on WTP (default = enable).
    "led-schedules": "string",  # Recurring firewall schedules for illuminating LEDs on the FortiAP. If led-state 
    "dtls-policy": "option",  # WTP data channel DTLS policy (default = clear-text).
    "dtls-in-kernel": "option",  # Enable/disable data channel DTLS in kernel.
    "max-clients": "integer",  # Maximum number of stations (STAs) supported by the WTP (default = 0, meaning no 
    "handoff-rssi": "integer",  # Minimum received signal strength indicator (RSSI) value for handoff (20 - 30, de
    "handoff-sta-thresh": "integer",  # Threshold value for AP handoff.
    "handoff-roaming": "option",  # Enable/disable client load balancing during roaming to avoid roaming delay (defa
    "deny-mac-list": "string",  # List of MAC addresses that are denied access to this WTP, FortiAP, or AP.
    "ap-country": "option",  # Country in which this WTP, FortiAP, or AP will operate (default = NA, automatica
    "ip-fragment-preventing": "option",  # Method(s) by which IP fragmentation is prevented for control and data packets th
    "tun-mtu-uplink": "integer",  # The maximum transmission unit (MTU) of uplink CAPWAP tunnel (576 - 1500 bytes or
    "tun-mtu-downlink": "integer",  # The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU 
    "split-tunneling-acl-path": "option",  # Split tunneling ACL path is local/tunnel.
    "split-tunneling-acl-local-ap-subnet": "option",  # Enable/disable automatically adding local subnetwork of FortiAP to split-tunneli
    "split-tunneling-acl": "string",  # Split tunneling ACL filter list.
    "allowaccess": "option",  # Control management access to the managed WTP, FortiAP, or AP. Separate entries w
    "login-passwd-change": "option",  # Change or reset the administrator password of a managed WTP, FortiAP or AP (yes,
    "login-passwd": "password",  # Set the managed WTP, FortiAP, or AP's administrator password.
    "lldp": "option",  # Enable/disable Link Layer Discovery Protocol (LLDP) for the WTP, FortiAP, or AP 
    "poe-mode": "option",  # Set the WTP, FortiAP, or AP's PoE mode.
    "usb-port": "option",  # Enable/disable USB port of the WTP (default = enable).
    "frequency-handoff": "option",  # Enable/disable frequency handoff of clients to other channels (default = disable
    "ap-handoff": "option",  # Enable/disable AP handoff of clients to other APs (default = disable).
    "default-mesh-root": "option",  # Configure default mesh root SSID when it is not included by radio's SSID configu
    "radio-1": "string",  # Configuration options for radio 1.
    "radio-2": "string",  # Configuration options for radio 2.
    "radio-3": "string",  # Configuration options for radio 3.
    "radio-4": "string",  # Configuration options for radio 4.
    "lbs": "string",  # Set various location based service (LBS) options.
    "ext-info-enable": "option",  # Enable/disable station/VAP/radio extension information.
    "indoor-outdoor-deployment": "option",  # Set to allow indoor/outdoor-only channels under regulatory rules (default = plat
    "esl-ses-dongle": "string",  # ESL SES-imagotag dongle configuration.
    "console-login": "option",  # Enable/disable FortiAP console login access (default = enable).
    "wan-port-auth": "option",  # Set WAN port authentication mode (default = none).
    "wan-port-auth-usrname": "string",  # Set WAN port 802.1x supplicant user name.
    "wan-port-auth-password": "password",  # Set WAN port 802.1x supplicant password.
    "wan-port-auth-methods": "option",  # WAN port 802.1x supplicant EAP methods (default = all).
    "wan-port-auth-macsec": "option",  # Enable/disable WAN port 802.1x supplicant MACsec policy (default = disable).
    "apcfg-auto-cert": "option",  # Enable/disable AP local auto cert configuration (default = disable).
    "apcfg-auto-cert-enroll-protocol": "option",  # Certificate enrollment protocol (default = none)
    "apcfg-auto-cert-crypto-algo": "option",  # Cryptography algorithm: rsa-1024, rsa-1536, rsa-2048, rsa-4096, ec-secp256r1, ec
    "apcfg-auto-cert-est-server": "string",  # Address and port for EST server (e.g. https://example.com:1234).
    "apcfg-auto-cert-est-ca-id": "string",  # CA identifier of the CA server for signing via EST.
    "apcfg-auto-cert-est-http-username": "string",  # HTTP Authentication username for signing via EST.
    "apcfg-auto-cert-est-http-password": "password",  # HTTP Authentication password for signing via EST.
    "apcfg-auto-cert-est-subject": "string",  # Subject e.g. \"CN=User,DC=example,DC=COM\" (default = CN=FortiAP,DC=local,DC=COM
    "apcfg-auto-cert-est-subject-alt-name": "string",  # Subject alternative name (optional, e.g. \"DNS:dns1.com,IP:192.168.1.99\")
    "apcfg-auto-cert-auto-regen-days": "integer",  # Number of days to wait before expiry of an updated local certificate is requeste
    "apcfg-auto-cert-est-https-ca": "string",  # PEM format https CA Certificate.
    "apcfg-auto-cert-scep-keytype": "option",  # Key type (default = rsa)
    "apcfg-auto-cert-scep-keysize": "option",  # Key size: 1024, 1536, 2048, 4096 (default 2048).
    "apcfg-auto-cert-scep-ec-name": "option",  # Elliptic curve name: secp256r1, secp384r1 and secp521r1. (default secp256r1).
    "apcfg-auto-cert-scep-sub-fully-dn": "string",  # Full DN of the subject (e.g C=US,ST=CA,L=Sunnyvale,O=Fortinet,OU=Dep1,emailAddre
    "apcfg-auto-cert-scep-url": "string",  # SCEP server URL.
    "apcfg-auto-cert-scep-password": "password",  # SCEP server challenge password for auto-regeneration.
    "apcfg-auto-cert-scep-ca-id": "string",  # CA identifier of the CA server for signing via SCEP.
    "apcfg-auto-cert-scep-subject-alt-name": "string",  # Subject alternative name (optional, e.g. \"DNS:dns1.com,IP:192.168.1.99\")
    "apcfg-auto-cert-scep-https-ca": "string",  # PEM format https CA Certificate.
    "unii-4-5ghz-band": "option",  # Enable/disable UNII-4 5Ghz band channels (default = disable).
    "admin-auth-tacacs+": "string",  # Remote authentication server for admin user.
    "admin-restrict-local": "option",  # Enable/disable local admin authentication restriction when remote authenticator 
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "WTP (or FortiAP or AP) profile name.",
    "comment": "Comment.",
    "platform": "WTP, FortiAP, or AP platform.",
    "control-message-offload": "Enable/disable CAPWAP control message data channel offload.",
    "bonjour-profile": "Bonjour profile name.",
    "apcfg-profile": "AP local configuration profile name.",
    "apcfg-mesh": "Enable/disable AP local mesh configuration (default = disable).",
    "apcfg-mesh-ap-type": "Mesh AP Type (default = ethernet).",
    "apcfg-mesh-ssid": " Mesh SSID (default = none).",
    "apcfg-mesh-eth-bridge": "Enable/disable mesh ethernet bridge (default = disable).",
    "ble-profile": "Bluetooth Low Energy profile name.",
    "lw-profile": "LoRaWAN profile name.",
    "syslog-profile": "System log server configuration profile name.",
    "wan-port-mode": "Enable/disable using a WAN port as a LAN port.",
    "lan": "WTP LAN port mapping.",
    "energy-efficient-ethernet": "Enable/disable use of energy efficient Ethernet on WTP.",
    "led-state": "Enable/disable use of LEDs on WTP (default = enable).",
    "led-schedules": "Recurring firewall schedules for illuminating LEDs on the FortiAP. If led-state is enabled, LEDs will be visible when at least one of the schedules is valid. Separate multiple schedule names with a space.",
    "dtls-policy": "WTP data channel DTLS policy (default = clear-text).",
    "dtls-in-kernel": "Enable/disable data channel DTLS in kernel.",
    "max-clients": "Maximum number of stations (STAs) supported by the WTP (default = 0, meaning no client limitation).",
    "handoff-rssi": "Minimum received signal strength indicator (RSSI) value for handoff (20 - 30, default = 25).",
    "handoff-sta-thresh": "Threshold value for AP handoff.",
    "handoff-roaming": "Enable/disable client load balancing during roaming to avoid roaming delay (default = enable).",
    "deny-mac-list": "List of MAC addresses that are denied access to this WTP, FortiAP, or AP.",
    "ap-country": "Country in which this WTP, FortiAP, or AP will operate (default = NA, automatically use the country configured for the current VDOM).",
    "ip-fragment-preventing": "Method(s) by which IP fragmentation is prevented for control and data packets through CAPWAP tunnel (default = tcp-mss-adjust).",
    "tun-mtu-uplink": "The maximum transmission unit (MTU) of uplink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).",
    "tun-mtu-downlink": "The MTU of downlink CAPWAP tunnel (576 - 1500 bytes or 0; 0 means the local MTU of FortiAP; default = 0).",
    "split-tunneling-acl-path": "Split tunneling ACL path is local/tunnel.",
    "split-tunneling-acl-local-ap-subnet": "Enable/disable automatically adding local subnetwork of FortiAP to split-tunneling ACL (default = disable).",
    "split-tunneling-acl": "Split tunneling ACL filter list.",
    "allowaccess": "Control management access to the managed WTP, FortiAP, or AP. Separate entries with a space.",
    "login-passwd-change": "Change or reset the administrator password of a managed WTP, FortiAP or AP (yes, default, or no, default = no).",
    "login-passwd": "Set the managed WTP, FortiAP, or AP's administrator password.",
    "lldp": "Enable/disable Link Layer Discovery Protocol (LLDP) for the WTP, FortiAP, or AP (default = enable).",
    "poe-mode": "Set the WTP, FortiAP, or AP's PoE mode.",
    "usb-port": "Enable/disable USB port of the WTP (default = enable).",
    "frequency-handoff": "Enable/disable frequency handoff of clients to other channels (default = disable).",
    "ap-handoff": "Enable/disable AP handoff of clients to other APs (default = disable).",
    "default-mesh-root": "Configure default mesh root SSID when it is not included by radio's SSID configuration.",
    "radio-1": "Configuration options for radio 1.",
    "radio-2": "Configuration options for radio 2.",
    "radio-3": "Configuration options for radio 3.",
    "radio-4": "Configuration options for radio 4.",
    "lbs": "Set various location based service (LBS) options.",
    "ext-info-enable": "Enable/disable station/VAP/radio extension information.",
    "indoor-outdoor-deployment": "Set to allow indoor/outdoor-only channels under regulatory rules (default = platform-determined).",
    "esl-ses-dongle": "ESL SES-imagotag dongle configuration.",
    "console-login": "Enable/disable FortiAP console login access (default = enable).",
    "wan-port-auth": "Set WAN port authentication mode (default = none).",
    "wan-port-auth-usrname": "Set WAN port 802.1x supplicant user name.",
    "wan-port-auth-password": "Set WAN port 802.1x supplicant password.",
    "wan-port-auth-methods": "WAN port 802.1x supplicant EAP methods (default = all).",
    "wan-port-auth-macsec": "Enable/disable WAN port 802.1x supplicant MACsec policy (default = disable).",
    "apcfg-auto-cert": "Enable/disable AP local auto cert configuration (default = disable).",
    "apcfg-auto-cert-enroll-protocol": "Certificate enrollment protocol (default = none)",
    "apcfg-auto-cert-crypto-algo": "Cryptography algorithm: rsa-1024, rsa-1536, rsa-2048, rsa-4096, ec-secp256r1, ec-secp384r1, ec-secp521r1 (default = ec-secp256r1)",
    "apcfg-auto-cert-est-server": "Address and port for EST server (e.g. https://example.com:1234).",
    "apcfg-auto-cert-est-ca-id": "CA identifier of the CA server for signing via EST.",
    "apcfg-auto-cert-est-http-username": "HTTP Authentication username for signing via EST.",
    "apcfg-auto-cert-est-http-password": "HTTP Authentication password for signing via EST.",
    "apcfg-auto-cert-est-subject": "Subject e.g. \"CN=User,DC=example,DC=COM\" (default = CN=FortiAP,DC=local,DC=COM)",
    "apcfg-auto-cert-est-subject-alt-name": "Subject alternative name (optional, e.g. \"DNS:dns1.com,IP:192.168.1.99\")",
    "apcfg-auto-cert-auto-regen-days": "Number of days to wait before expiry of an updated local certificate is requested (0 = disabled) (default = 30).",
    "apcfg-auto-cert-est-https-ca": "PEM format https CA Certificate.",
    "apcfg-auto-cert-scep-keytype": "Key type (default = rsa)",
    "apcfg-auto-cert-scep-keysize": "Key size: 1024, 1536, 2048, 4096 (default 2048).",
    "apcfg-auto-cert-scep-ec-name": "Elliptic curve name: secp256r1, secp384r1 and secp521r1. (default secp256r1).",
    "apcfg-auto-cert-scep-sub-fully-dn": "Full DN of the subject (e.g C=US,ST=CA,L=Sunnyvale,O=Fortinet,OU=Dep1,emailAddress=test@example.com). There should be no space in between the attributes. Supported DN attributes (case-sensitive) are:C,ST,L,O,OU,emailAddress. The CN defaults to the device’s SN and cannot be changed.",
    "apcfg-auto-cert-scep-url": "SCEP server URL.",
    "apcfg-auto-cert-scep-password": "SCEP server challenge password for auto-regeneration.",
    "apcfg-auto-cert-scep-ca-id": "CA identifier of the CA server for signing via SCEP.",
    "apcfg-auto-cert-scep-subject-alt-name": "Subject alternative name (optional, e.g. \"DNS:dns1.com,IP:192.168.1.99\")",
    "apcfg-auto-cert-scep-https-ca": "PEM format https CA Certificate.",
    "unii-4-5ghz-band": "Enable/disable UNII-4 5Ghz band channels (default = disable).",
    "admin-auth-tacacs+": "Remote authentication server for admin user.",
    "admin-restrict-local": "Enable/disable local admin authentication restriction when remote authenticator is up and running (default = disable).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "bonjour-profile": {"type": "string", "max_length": 35},
    "apcfg-profile": {"type": "string", "max_length": 35},
    "apcfg-mesh-ssid": {"type": "string", "max_length": 15},
    "ble-profile": {"type": "string", "max_length": 35},
    "lw-profile": {"type": "string", "max_length": 35},
    "syslog-profile": {"type": "string", "max_length": 35},
    "max-clients": {"type": "integer", "min": 0, "max": 4294967295},
    "handoff-rssi": {"type": "integer", "min": 20, "max": 30},
    "handoff-sta-thresh": {"type": "integer", "min": 5, "max": 60},
    "tun-mtu-uplink": {"type": "integer", "min": 576, "max": 1500},
    "tun-mtu-downlink": {"type": "integer", "min": 576, "max": 1500},
    "wan-port-auth-usrname": {"type": "string", "max_length": 63},
    "apcfg-auto-cert-est-server": {"type": "string", "max_length": 255},
    "apcfg-auto-cert-est-ca-id": {"type": "string", "max_length": 255},
    "apcfg-auto-cert-est-http-username": {"type": "string", "max_length": 63},
    "apcfg-auto-cert-est-subject": {"type": "string", "max_length": 127},
    "apcfg-auto-cert-est-subject-alt-name": {"type": "string", "max_length": 127},
    "apcfg-auto-cert-auto-regen-days": {"type": "integer", "min": 0, "max": 4294967295},
    "apcfg-auto-cert-est-https-ca": {"type": "string", "max_length": 79},
    "apcfg-auto-cert-scep-sub-fully-dn": {"type": "string", "max_length": 255},
    "apcfg-auto-cert-scep-url": {"type": "string", "max_length": 255},
    "apcfg-auto-cert-scep-ca-id": {"type": "string", "max_length": 255},
    "apcfg-auto-cert-scep-subject-alt-name": {"type": "string", "max_length": 127},
    "apcfg-auto-cert-scep-https-ca": {"type": "string", "max_length": 79},
    "admin-auth-tacacs+": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "platform": {
        "type": {
            "type": "option",
            "help": "WTP, FortiAP or AP platform type. There are built-in WTP profiles for all supported FortiAP models. You can select a built-in profile and customize it or create a new profile.",
            "default": "221E",
            "options": ["AP-11N", "C24JE", "421E", "423E", "221E", "222E", "223E", "224E", "231E", "321E", "431F", "431FL", "432F", "432FR", "433F", "433FL", "231F", "231FL", "234F", "23JF", "831F", "231G", "233G", "234G", "431G", "432G", "433G", "231K", "231KD", "23JK", "222KL", "241K", "243K", "244K", "441K", "432K", "443K", "U421E", "U422EV", "U423E", "U221EV", "U223EV", "U24JEV", "U321EV", "U323EV", "U431F", "U433F", "U231F", "U234F", "U432F", "U231G", "MVP"],
        },
        "mode": {
            "type": "option",
            "help": "Configure operation mode of 5G radios (default = single-5G).",
            "default": "single-5G",
            "options": ["single-5G", "dual-5G"],
        },
        "ddscan": {
            "type": "option",
            "help": "Enable/disable use of one radio for dedicated full-band scanning to detect RF characterization and wireless threat management.",
            "default": "disable",
            "options": ["enable", "disable"],
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
    "led-schedules": {
        "name": {
            "type": "string",
            "help": "Schedule name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
    "deny-mac-list": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "mac": {
            "type": "mac-address",
            "help": "A WiFi device with this MAC address is denied access to this WTP, FortiAP or AP.",
            "default": "00:00:00:00:00:00",
        },
    },
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
    "radio-1": {
        "mode": {
            "type": "option",
            "help": "Mode of radio 1. Radio 1 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.",
            "default": "ap",
            "options": ["disabled", "ap", "monitor", "sniffer", "sam"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 1 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "band-5g-type": {
            "type": "option",
            "help": "WiFi 5G band type.",
            "default": "5g-full",
            "options": ["5g-full", "5g-high", "5g-low"],
        },
        "drma": {
            "type": "option",
            "help": "Enable/disable dynamic radio mode assignment (DRMA) (default = disable).",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "drma-sensitivity": {
            "type": "option",
            "help": "Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).",
            "default": "low",
            "options": ["low", "medium", "high"],
        },
        "airtime-fairness": {
            "type": "option",
            "help": "Enable/disable airtime fairness (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "protection-mode": {
            "type": "option",
            "help": "Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).",
            "default": "disable",
            "options": ["rtscts", "ctsonly", "disable"],
        },
        "powersave-optimize": {
            "type": "option",
            "help": "Enable client power-saving features such as TIM, AC VO, and OBSS etc.",
            "default": "",
            "options": ["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"],
        },
        "transmit-optimize": {
            "type": "option",
            "help": "Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.",
            "default": "power-save aggr-limit retry-limit send-bar",
            "options": ["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"],
        },
        "amsdu": {
            "type": "option",
            "help": "Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "coexistence": {
            "type": "option",
            "help": "Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "zero-wait-dfs": {
            "type": "option",
            "help": "Enable/disable zero wait DFS on radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "bss-color": {
            "type": "integer",
            "help": "BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
        "bss-color-mode": {
            "type": "option",
            "help": "BSS color mode for this 11ax radio (default = auto).",
            "default": "auto",
            "options": ["auto", "static"],
        },
        "short-guard-interval": {
            "type": "option",
            "help": "Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "mimo-mode": {
            "type": "option",
            "help": "Configure radio MIMO mode (default = default).",
            "default": "default",
            "options": ["default", "1x1", "2x2", "3x3", "4x4", "8x8"],
        },
        "channel-bonding": {
            "type": "option",
            "help": "Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "channel-bonding-ext": {
            "type": "option",
            "help": "Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).",
            "default": "320MHz-2",
            "options": ["320MHz-1", "320MHz-2"],
        },
        "optional-antenna": {
            "type": "option",
            "help": "Optional antenna used on FAP (default = none).",
            "default": "none",
            "options": ["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"],
        },
        "optional-antenna-gain": {
            "type": "string",
            "help": "Optional antenna gain in dBi (0 to 20, default = 0).",
            "default": "0",
            "max_length": 7,
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).",
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
        "dtim": {
            "type": "integer",
            "help": "Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "beacon-interval": {
            "type": "integer",
            "help": "Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 65535,
        },
        "80211d": {
            "type": "option",
            "help": "Enable/disable 802.11d countryie(default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "80211mc": {
            "type": "option",
            "help": "Enable/disable 802.11mc responder mode (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rts-threshold": {
            "type": "integer",
            "help": "Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 256,
            "max_value": 2346,
        },
        "frag-threshold": {
            "type": "integer",
            "help": "Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 800,
            "max_value": 2346,
        },
        "ap-sniffer-bufsize": {
            "type": "integer",
            "help": "Sniffer buffer size (1 - 32 MB, default = 16).",
            "default": 16,
            "min_value": 1,
            "max_value": 32,
        },
        "ap-sniffer-chan": {
            "type": "integer",
            "help": "Channel on which to operate the sniffer (default = 6).",
            "default": 36,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ap-sniffer-chan-width": {
            "type": "option",
            "help": "Channel bandwidth for sniffer.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "ap-sniffer-addr": {
            "type": "mac-address",
            "help": "MAC address to monitor.",
            "default": "00:00:00:00:00:00",
        },
        "ap-sniffer-mgmt-beacon": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management Beacon frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-probe": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management probe frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-other": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management other frames  (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-ctl": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi control frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-data": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi data frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "sam-ssid": {
            "type": "string",
            "help": "SSID for WiFi network.",
            "default": "",
            "max_length": 32,
        },
        "sam-bssid": {
            "type": "mac-address",
            "help": "BSSID for WiFi network.",
            "default": "00:00:00:00:00:00",
        },
        "sam-security-type": {
            "type": "option",
            "help": "Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).",
            "default": "wpa-personal",
            "options": ["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"],
        },
        "sam-captive-portal": {
            "type": "option",
            "help": "Enable/disable Captive Portal Authentication (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "sam-cwp-username": {
            "type": "string",
            "help": "Username for captive portal authentication.",
            "default": "",
            "max_length": 35,
        },
        "sam-cwp-password": {
            "type": "password",
            "help": "Password for captive portal authentication.",
            "max_length": 128,
        },
        "sam-cwp-test-url": {
            "type": "string",
            "help": "Website the client is trying to access.",
            "default": "",
            "max_length": 255,
        },
        "sam-cwp-match-string": {
            "type": "string",
            "help": "Identification string from the captive portal login form.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-success-string": {
            "type": "string",
            "help": "Success identification on the page after a successful login.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-failure-string": {
            "type": "string",
            "help": "Failure identification on the page after an incorrect login.",
            "default": "",
            "max_length": 64,
        },
        "sam-eap-method": {
            "type": "option",
            "help": "Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).",
            "default": "peap",
            "options": ["both", "tls", "peap"],
        },
        "sam-client-certificate": {
            "type": "string",
            "help": "Client certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key": {
            "type": "string",
            "help": "Private key for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key-password": {
            "type": "password",
            "help": "Password for private key file for WPA2/WPA3-ENTERPRISE.",
            "max_length": 128,
        },
        "sam-ca-certificate": {
            "type": "string",
            "help": "CA certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 79,
        },
        "sam-username": {
            "type": "string",
            "help": "Username for WiFi network connection.",
            "default": "",
            "max_length": 35,
        },
        "sam-password": {
            "type": "password",
            "help": "Passphrase for WiFi network connection.",
            "max_length": 128,
        },
        "sam-test": {
            "type": "option",
            "help": "Select SAM test type (default = \"PING\").",
            "default": "ping",
            "options": ["ping", "iperf"],
        },
        "sam-server-type": {
            "type": "option",
            "help": "Select SAM server type (default = \"IP\").",
            "default": "ip",
            "options": ["ip", "fqdn"],
        },
        "sam-server-ip": {
            "type": "ipv4-address",
            "help": "SAM test server IP address.",
            "default": "0.0.0.0",
        },
        "sam-server-fqdn": {
            "type": "string",
            "help": "SAM test server domain name.",
            "default": "",
            "max_length": 255,
        },
        "iperf-server-port": {
            "type": "integer",
            "help": "Iperf service port number.",
            "default": 5001,
            "min_value": 0,
            "max_value": 65535,
        },
        "iperf-protocol": {
            "type": "option",
            "help": "Iperf test protocol (default = \"UDP\").",
            "default": "udp",
            "options": ["udp", "tcp"],
        },
        "sam-report-intv": {
            "type": "integer",
            "help": "SAM report interval (sec), 0 for a one-time report.",
            "default": 0,
            "min_value": 60,
            "max_value": 864000,
        },
        "channel-utilization": {
            "type": "option",
            "help": "Enable/disable measuring channel utilization.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "wids-profile": {
            "type": "string",
            "help": "Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "ai-darrp-support": {
            "type": "option",
            "help": "Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "darrp": {
            "type": "option",
            "help": "Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "arrp-profile": {
            "type": "string",
            "help": "Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "max-clients": {
            "type": "integer",
            "help": "Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "max-distance": {
            "type": "integer",
            "help": "Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 54000,
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
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "call-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "call-capacity": {
            "type": "integer",
            "help": "Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 60,
        },
        "bandwidth-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "bandwidth-capacity": {
            "type": "integer",
            "help": "Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).",
            "default": 2000,
            "min_value": 1,
            "max_value": 600000,
        },
    },
    "radio-2": {
        "mode": {
            "type": "option",
            "help": "Mode of radio 2. Radio 2 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.",
            "default": "ap",
            "options": ["disabled", "ap", "monitor", "sniffer", "sam"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 2 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "band-5g-type": {
            "type": "option",
            "help": "WiFi 5G band type.",
            "default": "5g-full",
            "options": ["5g-full", "5g-high", "5g-low"],
        },
        "drma": {
            "type": "option",
            "help": "Enable/disable dynamic radio mode assignment (DRMA) (default = disable).",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "drma-sensitivity": {
            "type": "option",
            "help": "Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).",
            "default": "low",
            "options": ["low", "medium", "high"],
        },
        "airtime-fairness": {
            "type": "option",
            "help": "Enable/disable airtime fairness (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "protection-mode": {
            "type": "option",
            "help": "Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).",
            "default": "disable",
            "options": ["rtscts", "ctsonly", "disable"],
        },
        "powersave-optimize": {
            "type": "option",
            "help": "Enable client power-saving features such as TIM, AC VO, and OBSS etc.",
            "default": "",
            "options": ["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"],
        },
        "transmit-optimize": {
            "type": "option",
            "help": "Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.",
            "default": "power-save aggr-limit retry-limit send-bar",
            "options": ["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"],
        },
        "amsdu": {
            "type": "option",
            "help": "Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "coexistence": {
            "type": "option",
            "help": "Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "zero-wait-dfs": {
            "type": "option",
            "help": "Enable/disable zero wait DFS on radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "bss-color": {
            "type": "integer",
            "help": "BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
        "bss-color-mode": {
            "type": "option",
            "help": "BSS color mode for this 11ax radio (default = auto).",
            "default": "auto",
            "options": ["auto", "static"],
        },
        "short-guard-interval": {
            "type": "option",
            "help": "Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "mimo-mode": {
            "type": "option",
            "help": "Configure radio MIMO mode (default = default).",
            "default": "default",
            "options": ["default", "1x1", "2x2", "3x3", "4x4", "8x8"],
        },
        "channel-bonding": {
            "type": "option",
            "help": "Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "channel-bonding-ext": {
            "type": "option",
            "help": "Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).",
            "default": "320MHz-2",
            "options": ["320MHz-1", "320MHz-2"],
        },
        "optional-antenna": {
            "type": "option",
            "help": "Optional antenna used on FAP (default = none).",
            "default": "none",
            "options": ["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"],
        },
        "optional-antenna-gain": {
            "type": "string",
            "help": "Optional antenna gain in dBi (0 to 20, default = 0).",
            "default": "0",
            "max_length": 7,
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).",
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
        "dtim": {
            "type": "integer",
            "help": "Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "beacon-interval": {
            "type": "integer",
            "help": "Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 65535,
        },
        "80211d": {
            "type": "option",
            "help": "Enable/disable 802.11d countryie(default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "80211mc": {
            "type": "option",
            "help": "Enable/disable 802.11mc responder mode (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rts-threshold": {
            "type": "integer",
            "help": "Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 256,
            "max_value": 2346,
        },
        "frag-threshold": {
            "type": "integer",
            "help": "Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 800,
            "max_value": 2346,
        },
        "ap-sniffer-bufsize": {
            "type": "integer",
            "help": "Sniffer buffer size (1 - 32 MB, default = 16).",
            "default": 16,
            "min_value": 1,
            "max_value": 32,
        },
        "ap-sniffer-chan": {
            "type": "integer",
            "help": "Channel on which to operate the sniffer (default = 6).",
            "default": 6,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ap-sniffer-chan-width": {
            "type": "option",
            "help": "Channel bandwidth for sniffer.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "ap-sniffer-addr": {
            "type": "mac-address",
            "help": "MAC address to monitor.",
            "default": "00:00:00:00:00:00",
        },
        "ap-sniffer-mgmt-beacon": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management Beacon frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-probe": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management probe frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-other": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management other frames  (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-ctl": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi control frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-data": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi data frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "sam-ssid": {
            "type": "string",
            "help": "SSID for WiFi network.",
            "default": "",
            "max_length": 32,
        },
        "sam-bssid": {
            "type": "mac-address",
            "help": "BSSID for WiFi network.",
            "default": "00:00:00:00:00:00",
        },
        "sam-security-type": {
            "type": "option",
            "help": "Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).",
            "default": "wpa-personal",
            "options": ["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"],
        },
        "sam-captive-portal": {
            "type": "option",
            "help": "Enable/disable Captive Portal Authentication (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "sam-cwp-username": {
            "type": "string",
            "help": "Username for captive portal authentication.",
            "default": "",
            "max_length": 35,
        },
        "sam-cwp-password": {
            "type": "password",
            "help": "Password for captive portal authentication.",
            "max_length": 128,
        },
        "sam-cwp-test-url": {
            "type": "string",
            "help": "Website the client is trying to access.",
            "default": "",
            "max_length": 255,
        },
        "sam-cwp-match-string": {
            "type": "string",
            "help": "Identification string from the captive portal login form.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-success-string": {
            "type": "string",
            "help": "Success identification on the page after a successful login.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-failure-string": {
            "type": "string",
            "help": "Failure identification on the page after an incorrect login.",
            "default": "",
            "max_length": 64,
        },
        "sam-eap-method": {
            "type": "option",
            "help": "Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).",
            "default": "peap",
            "options": ["both", "tls", "peap"],
        },
        "sam-client-certificate": {
            "type": "string",
            "help": "Client certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key": {
            "type": "string",
            "help": "Private key for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key-password": {
            "type": "password",
            "help": "Password for private key file for WPA2/WPA3-ENTERPRISE.",
            "max_length": 128,
        },
        "sam-ca-certificate": {
            "type": "string",
            "help": "CA certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 79,
        },
        "sam-username": {
            "type": "string",
            "help": "Username for WiFi network connection.",
            "default": "",
            "max_length": 35,
        },
        "sam-password": {
            "type": "password",
            "help": "Passphrase for WiFi network connection.",
            "max_length": 128,
        },
        "sam-test": {
            "type": "option",
            "help": "Select SAM test type (default = \"PING\").",
            "default": "ping",
            "options": ["ping", "iperf"],
        },
        "sam-server-type": {
            "type": "option",
            "help": "Select SAM server type (default = \"IP\").",
            "default": "ip",
            "options": ["ip", "fqdn"],
        },
        "sam-server-ip": {
            "type": "ipv4-address",
            "help": "SAM test server IP address.",
            "default": "0.0.0.0",
        },
        "sam-server-fqdn": {
            "type": "string",
            "help": "SAM test server domain name.",
            "default": "",
            "max_length": 255,
        },
        "iperf-server-port": {
            "type": "integer",
            "help": "Iperf service port number.",
            "default": 5001,
            "min_value": 0,
            "max_value": 65535,
        },
        "iperf-protocol": {
            "type": "option",
            "help": "Iperf test protocol (default = \"UDP\").",
            "default": "udp",
            "options": ["udp", "tcp"],
        },
        "sam-report-intv": {
            "type": "integer",
            "help": "SAM report interval (sec), 0 for a one-time report.",
            "default": 0,
            "min_value": 60,
            "max_value": 864000,
        },
        "channel-utilization": {
            "type": "option",
            "help": "Enable/disable measuring channel utilization.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "wids-profile": {
            "type": "string",
            "help": "Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "ai-darrp-support": {
            "type": "option",
            "help": "Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "darrp": {
            "type": "option",
            "help": "Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "arrp-profile": {
            "type": "string",
            "help": "Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "max-clients": {
            "type": "integer",
            "help": "Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "max-distance": {
            "type": "integer",
            "help": "Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 54000,
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
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "call-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "call-capacity": {
            "type": "integer",
            "help": "Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 60,
        },
        "bandwidth-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "bandwidth-capacity": {
            "type": "integer",
            "help": "Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).",
            "default": 2000,
            "min_value": 1,
            "max_value": 600000,
        },
    },
    "radio-3": {
        "mode": {
            "type": "option",
            "help": "Mode of radio 3. Radio 3 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.",
            "default": "ap",
            "options": ["disabled", "ap", "monitor", "sniffer", "sam"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 3 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "band-5g-type": {
            "type": "option",
            "help": "WiFi 5G band type.",
            "default": "5g-full",
            "options": ["5g-full", "5g-high", "5g-low"],
        },
        "drma": {
            "type": "option",
            "help": "Enable/disable dynamic radio mode assignment (DRMA) (default = disable).",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "drma-sensitivity": {
            "type": "option",
            "help": "Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).",
            "default": "low",
            "options": ["low", "medium", "high"],
        },
        "airtime-fairness": {
            "type": "option",
            "help": "Enable/disable airtime fairness (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "protection-mode": {
            "type": "option",
            "help": "Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).",
            "default": "disable",
            "options": ["rtscts", "ctsonly", "disable"],
        },
        "powersave-optimize": {
            "type": "option",
            "help": "Enable client power-saving features such as TIM, AC VO, and OBSS etc.",
            "default": "",
            "options": ["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"],
        },
        "transmit-optimize": {
            "type": "option",
            "help": "Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.",
            "default": "power-save aggr-limit retry-limit send-bar",
            "options": ["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"],
        },
        "amsdu": {
            "type": "option",
            "help": "Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "coexistence": {
            "type": "option",
            "help": "Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "zero-wait-dfs": {
            "type": "option",
            "help": "Enable/disable zero wait DFS on radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "bss-color": {
            "type": "integer",
            "help": "BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
        "bss-color-mode": {
            "type": "option",
            "help": "BSS color mode for this 11ax radio (default = auto).",
            "default": "auto",
            "options": ["auto", "static"],
        },
        "short-guard-interval": {
            "type": "option",
            "help": "Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "mimo-mode": {
            "type": "option",
            "help": "Configure radio MIMO mode (default = default).",
            "default": "default",
            "options": ["default", "1x1", "2x2", "3x3", "4x4", "8x8"],
        },
        "channel-bonding": {
            "type": "option",
            "help": "Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "channel-bonding-ext": {
            "type": "option",
            "help": "Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).",
            "default": "320MHz-2",
            "options": ["320MHz-1", "320MHz-2"],
        },
        "optional-antenna": {
            "type": "option",
            "help": "Optional antenna used on FAP (default = none).",
            "default": "none",
            "options": ["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"],
        },
        "optional-antenna-gain": {
            "type": "string",
            "help": "Optional antenna gain in dBi (0 to 20, default = 0).",
            "default": "0",
            "max_length": 7,
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).",
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
        "dtim": {
            "type": "integer",
            "help": "Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "beacon-interval": {
            "type": "integer",
            "help": "Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 65535,
        },
        "80211d": {
            "type": "option",
            "help": "Enable/disable 802.11d countryie(default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "80211mc": {
            "type": "option",
            "help": "Enable/disable 802.11mc responder mode (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rts-threshold": {
            "type": "integer",
            "help": "Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 256,
            "max_value": 2346,
        },
        "frag-threshold": {
            "type": "integer",
            "help": "Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 800,
            "max_value": 2346,
        },
        "ap-sniffer-bufsize": {
            "type": "integer",
            "help": "Sniffer buffer size (1 - 32 MB, default = 16).",
            "default": 16,
            "min_value": 1,
            "max_value": 32,
        },
        "ap-sniffer-chan": {
            "type": "integer",
            "help": "Channel on which to operate the sniffer (default = 6).",
            "default": 37,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ap-sniffer-chan-width": {
            "type": "option",
            "help": "Channel bandwidth for sniffer.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "ap-sniffer-addr": {
            "type": "mac-address",
            "help": "MAC address to monitor.",
            "default": "00:00:00:00:00:00",
        },
        "ap-sniffer-mgmt-beacon": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management Beacon frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-probe": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management probe frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-other": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management other frames  (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-ctl": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi control frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-data": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi data frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "sam-ssid": {
            "type": "string",
            "help": "SSID for WiFi network.",
            "default": "",
            "max_length": 32,
        },
        "sam-bssid": {
            "type": "mac-address",
            "help": "BSSID for WiFi network.",
            "default": "00:00:00:00:00:00",
        },
        "sam-security-type": {
            "type": "option",
            "help": "Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).",
            "default": "wpa-personal",
            "options": ["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"],
        },
        "sam-captive-portal": {
            "type": "option",
            "help": "Enable/disable Captive Portal Authentication (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "sam-cwp-username": {
            "type": "string",
            "help": "Username for captive portal authentication.",
            "default": "",
            "max_length": 35,
        },
        "sam-cwp-password": {
            "type": "password",
            "help": "Password for captive portal authentication.",
            "max_length": 128,
        },
        "sam-cwp-test-url": {
            "type": "string",
            "help": "Website the client is trying to access.",
            "default": "",
            "max_length": 255,
        },
        "sam-cwp-match-string": {
            "type": "string",
            "help": "Identification string from the captive portal login form.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-success-string": {
            "type": "string",
            "help": "Success identification on the page after a successful login.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-failure-string": {
            "type": "string",
            "help": "Failure identification on the page after an incorrect login.",
            "default": "",
            "max_length": 64,
        },
        "sam-eap-method": {
            "type": "option",
            "help": "Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).",
            "default": "peap",
            "options": ["both", "tls", "peap"],
        },
        "sam-client-certificate": {
            "type": "string",
            "help": "Client certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key": {
            "type": "string",
            "help": "Private key for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key-password": {
            "type": "password",
            "help": "Password for private key file for WPA2/WPA3-ENTERPRISE.",
            "max_length": 128,
        },
        "sam-ca-certificate": {
            "type": "string",
            "help": "CA certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 79,
        },
        "sam-username": {
            "type": "string",
            "help": "Username for WiFi network connection.",
            "default": "",
            "max_length": 35,
        },
        "sam-password": {
            "type": "password",
            "help": "Passphrase for WiFi network connection.",
            "max_length": 128,
        },
        "sam-test": {
            "type": "option",
            "help": "Select SAM test type (default = \"PING\").",
            "default": "ping",
            "options": ["ping", "iperf"],
        },
        "sam-server-type": {
            "type": "option",
            "help": "Select SAM server type (default = \"IP\").",
            "default": "ip",
            "options": ["ip", "fqdn"],
        },
        "sam-server-ip": {
            "type": "ipv4-address",
            "help": "SAM test server IP address.",
            "default": "0.0.0.0",
        },
        "sam-server-fqdn": {
            "type": "string",
            "help": "SAM test server domain name.",
            "default": "",
            "max_length": 255,
        },
        "iperf-server-port": {
            "type": "integer",
            "help": "Iperf service port number.",
            "default": 5001,
            "min_value": 0,
            "max_value": 65535,
        },
        "iperf-protocol": {
            "type": "option",
            "help": "Iperf test protocol (default = \"UDP\").",
            "default": "udp",
            "options": ["udp", "tcp"],
        },
        "sam-report-intv": {
            "type": "integer",
            "help": "SAM report interval (sec), 0 for a one-time report.",
            "default": 0,
            "min_value": 60,
            "max_value": 864000,
        },
        "channel-utilization": {
            "type": "option",
            "help": "Enable/disable measuring channel utilization.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "wids-profile": {
            "type": "string",
            "help": "Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "ai-darrp-support": {
            "type": "option",
            "help": "Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "darrp": {
            "type": "option",
            "help": "Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "arrp-profile": {
            "type": "string",
            "help": "Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "max-clients": {
            "type": "integer",
            "help": "Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "max-distance": {
            "type": "integer",
            "help": "Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 54000,
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
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "call-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "call-capacity": {
            "type": "integer",
            "help": "Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 60,
        },
        "bandwidth-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "bandwidth-capacity": {
            "type": "integer",
            "help": "Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).",
            "default": 2000,
            "min_value": 1,
            "max_value": 600000,
        },
    },
    "radio-4": {
        "mode": {
            "type": "option",
            "help": "Mode of radio 4. Radio 4 can be disabled, configured as an access point, a rogue AP monitor, a sniffer, or a station.",
            "default": "ap",
            "options": ["disabled", "ap", "monitor", "sniffer", "sam"],
        },
        "band": {
            "type": "option",
            "help": "WiFi band that Radio 4 operates on.",
            "default": "",
            "options": ["802.11a", "802.11b", "802.11g", "802.11n-2G", "802.11n-5G", "802.11ac-2G", "802.11ac-5G", "802.11ax-2G", "802.11ax-5G", "802.11ax-6G", "802.11be-2G", "802.11be-5G", "802.11be-6G"],
        },
        "band-5g-type": {
            "type": "option",
            "help": "WiFi 5G band type.",
            "default": "5g-full",
            "options": ["5g-full", "5g-high", "5g-low"],
        },
        "drma": {
            "type": "option",
            "help": "Enable/disable dynamic radio mode assignment (DRMA) (default = disable).",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "drma-sensitivity": {
            "type": "option",
            "help": "Network Coverage Factor (NCF) percentage required to consider a radio as redundant (default = low).",
            "default": "low",
            "options": ["low", "medium", "high"],
        },
        "airtime-fairness": {
            "type": "option",
            "help": "Enable/disable airtime fairness (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "protection-mode": {
            "type": "option",
            "help": "Enable/disable 802.11g protection modes to support backwards compatibility with older clients (rtscts, ctsonly, disable).",
            "default": "disable",
            "options": ["rtscts", "ctsonly", "disable"],
        },
        "powersave-optimize": {
            "type": "option",
            "help": "Enable client power-saving features such as TIM, AC VO, and OBSS etc.",
            "default": "",
            "options": ["tim", "ac-vo", "no-obss-scan", "no-11b-rate", "client-rate-follow"],
        },
        "transmit-optimize": {
            "type": "option",
            "help": "Packet transmission optimization options including power saving, aggregation limiting, retry limiting, etc. All are enabled by default.",
            "default": "power-save aggr-limit retry-limit send-bar",
            "options": ["disable", "power-save", "aggr-limit", "retry-limit", "send-bar"],
        },
        "amsdu": {
            "type": "option",
            "help": "Enable/disable 802.11n AMSDU support. AMSDU can improve performance if supported by your WiFi clients (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "coexistence": {
            "type": "option",
            "help": "Enable/disable allowing both HT20 and HT40 on the same radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "zero-wait-dfs": {
            "type": "option",
            "help": "Enable/disable zero wait DFS on radio (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "bss-color": {
            "type": "integer",
            "help": "BSS color value for this 11ax radio (0 - 63, disable = 0, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 63,
        },
        "bss-color-mode": {
            "type": "option",
            "help": "BSS color mode for this 11ax radio (default = auto).",
            "default": "auto",
            "options": ["auto", "static"],
        },
        "short-guard-interval": {
            "type": "option",
            "help": "Use either the short guard interval (Short GI) of 400 ns or the long guard interval (Long GI) of 800 ns.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "mimo-mode": {
            "type": "option",
            "help": "Configure radio MIMO mode (default = default).",
            "default": "default",
            "options": ["default", "1x1", "2x2", "3x3", "4x4", "8x8"],
        },
        "channel-bonding": {
            "type": "option",
            "help": "Channel bandwidth: 320, 240, 160, 80, 40, or 20MHz. Channels may use both 20 and 40 by enabling coexistence.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "channel-bonding-ext": {
            "type": "option",
            "help": "Channel bandwidth extension: 320 MHz-1 and 320 MHz-2 (default = 320 MHz-2).",
            "default": "320MHz-2",
            "options": ["320MHz-1", "320MHz-2"],
        },
        "optional-antenna": {
            "type": "option",
            "help": "Optional antenna used on FAP (default = none).",
            "default": "none",
            "options": ["none", "custom", "FANT-04ABGN-0606-O-N", "FANT-04ABGN-1414-P-N", "FANT-04ABGN-8065-P-N", "FANT-04ABGN-0606-O-R", "FANT-04ABGN-0606-P-R", "FANT-10ACAX-1213-D-N", "FANT-08ABGN-1213-D-R", "FANT-04BEAX-0606-P-R"],
        },
        "optional-antenna-gain": {
            "type": "string",
            "help": "Optional antenna gain in dBi (0 to 20, default = 0).",
            "default": "0",
            "max_length": 7,
        },
        "auto-power-level": {
            "type": "option",
            "help": "Enable/disable automatic power-level adjustment to prevent co-channel interference (default = disable).",
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
        "dtim": {
            "type": "integer",
            "help": "Delivery Traffic Indication Map (DTIM) period (1 - 255, default = 1). Set higher to save battery life of WiFi client in power-save mode.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "beacon-interval": {
            "type": "integer",
            "help": "Beacon interval. The time between beacon frames in milliseconds. Actual range of beacon interval depends on the AP platform type (default = 100).",
            "default": 100,
            "min_value": 0,
            "max_value": 65535,
        },
        "80211d": {
            "type": "option",
            "help": "Enable/disable 802.11d countryie(default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "80211mc": {
            "type": "option",
            "help": "Enable/disable 802.11mc responder mode (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rts-threshold": {
            "type": "integer",
            "help": "Maximum packet size for RTS transmissions, specifying the maximum size of a data packet before RTS/CTS (256 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 256,
            "max_value": 2346,
        },
        "frag-threshold": {
            "type": "integer",
            "help": "Maximum packet size that can be sent without fragmentation (800 - 2346 bytes, default = 2346).",
            "default": 2346,
            "min_value": 800,
            "max_value": 2346,
        },
        "ap-sniffer-bufsize": {
            "type": "integer",
            "help": "Sniffer buffer size (1 - 32 MB, default = 16).",
            "default": 16,
            "min_value": 1,
            "max_value": 32,
        },
        "ap-sniffer-chan": {
            "type": "integer",
            "help": "Channel on which to operate the sniffer (default = 6).",
            "default": 6,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ap-sniffer-chan-width": {
            "type": "option",
            "help": "Channel bandwidth for sniffer.",
            "default": "20MHz",
            "options": ["320MHz", "240MHz", "160MHz", "80MHz", "40MHz", "20MHz"],
        },
        "ap-sniffer-addr": {
            "type": "mac-address",
            "help": "MAC address to monitor.",
            "default": "00:00:00:00:00:00",
        },
        "ap-sniffer-mgmt-beacon": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management Beacon frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-probe": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management probe frames (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-mgmt-other": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi management other frames  (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-ctl": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi control frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ap-sniffer-data": {
            "type": "option",
            "help": "Enable/disable sniffer on WiFi data frame (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "sam-ssid": {
            "type": "string",
            "help": "SSID for WiFi network.",
            "default": "",
            "max_length": 32,
        },
        "sam-bssid": {
            "type": "mac-address",
            "help": "BSSID for WiFi network.",
            "default": "00:00:00:00:00:00",
        },
        "sam-security-type": {
            "type": "option",
            "help": "Select WiFi network security type (default = \"wpa-personal\" for 2.4/5G radio, \"wpa3-sae\" for 6G radio).",
            "default": "wpa-personal",
            "options": ["open", "wpa-personal", "wpa-enterprise", "wpa3-sae", "owe"],
        },
        "sam-captive-portal": {
            "type": "option",
            "help": "Enable/disable Captive Portal Authentication (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "sam-cwp-username": {
            "type": "string",
            "help": "Username for captive portal authentication.",
            "default": "",
            "max_length": 35,
        },
        "sam-cwp-password": {
            "type": "password",
            "help": "Password for captive portal authentication.",
            "max_length": 128,
        },
        "sam-cwp-test-url": {
            "type": "string",
            "help": "Website the client is trying to access.",
            "default": "",
            "max_length": 255,
        },
        "sam-cwp-match-string": {
            "type": "string",
            "help": "Identification string from the captive portal login form.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-success-string": {
            "type": "string",
            "help": "Success identification on the page after a successful login.",
            "default": "",
            "max_length": 64,
        },
        "sam-cwp-failure-string": {
            "type": "string",
            "help": "Failure identification on the page after an incorrect login.",
            "default": "",
            "max_length": 64,
        },
        "sam-eap-method": {
            "type": "option",
            "help": "Select WPA2/WPA3-ENTERPRISE EAP Method (default = PEAP).",
            "default": "peap",
            "options": ["both", "tls", "peap"],
        },
        "sam-client-certificate": {
            "type": "string",
            "help": "Client certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key": {
            "type": "string",
            "help": "Private key for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 35,
        },
        "sam-private-key-password": {
            "type": "password",
            "help": "Password for private key file for WPA2/WPA3-ENTERPRISE.",
            "max_length": 128,
        },
        "sam-ca-certificate": {
            "type": "string",
            "help": "CA certificate for WPA2/WPA3-ENTERPRISE.",
            "default": "",
            "max_length": 79,
        },
        "sam-username": {
            "type": "string",
            "help": "Username for WiFi network connection.",
            "default": "",
            "max_length": 35,
        },
        "sam-password": {
            "type": "password",
            "help": "Passphrase for WiFi network connection.",
            "max_length": 128,
        },
        "sam-test": {
            "type": "option",
            "help": "Select SAM test type (default = \"PING\").",
            "default": "ping",
            "options": ["ping", "iperf"],
        },
        "sam-server-type": {
            "type": "option",
            "help": "Select SAM server type (default = \"IP\").",
            "default": "ip",
            "options": ["ip", "fqdn"],
        },
        "sam-server-ip": {
            "type": "ipv4-address",
            "help": "SAM test server IP address.",
            "default": "0.0.0.0",
        },
        "sam-server-fqdn": {
            "type": "string",
            "help": "SAM test server domain name.",
            "default": "",
            "max_length": 255,
        },
        "iperf-server-port": {
            "type": "integer",
            "help": "Iperf service port number.",
            "default": 5001,
            "min_value": 0,
            "max_value": 65535,
        },
        "iperf-protocol": {
            "type": "option",
            "help": "Iperf test protocol (default = \"UDP\").",
            "default": "udp",
            "options": ["udp", "tcp"],
        },
        "sam-report-intv": {
            "type": "integer",
            "help": "SAM report interval (sec), 0 for a one-time report.",
            "default": 0,
            "min_value": 60,
            "max_value": 864000,
        },
        "channel-utilization": {
            "type": "option",
            "help": "Enable/disable measuring channel utilization.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "wids-profile": {
            "type": "string",
            "help": "Wireless Intrusion Detection System (WIDS) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "ai-darrp-support": {
            "type": "option",
            "help": "Enable/disable support for FortiAIOps to retrieve Distributed Automatic Radio Resource Provisioning (DARRP) data through REST API calls (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "darrp": {
            "type": "option",
            "help": "Enable/disable Distributed Automatic Radio Resource Provisioning (DARRP) to make sure the radio is always using the most optimal channel (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "arrp-profile": {
            "type": "string",
            "help": "Distributed Automatic Radio Resource Provisioning (DARRP) profile name to assign to the radio.",
            "default": "",
            "max_length": 35,
        },
        "max-clients": {
            "type": "integer",
            "help": "Maximum number of stations (STAs) or WiFi clients supported by the radio. Range depends on the hardware.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "max-distance": {
            "type": "integer",
            "help": "Maximum expected distance between the AP and clients (0 - 54000 m, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 54000,
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
        "channel": {
            "type": "string",
            "help": "Selected list of wireless radio channels.",
        },
        "call-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) call admission control to optimize WiFi bandwidth use for VoIP calls. New VoIP calls are only accepted if there is enough bandwidth available to support them.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "call-capacity": {
            "type": "integer",
            "help": "Maximum number of Voice over WLAN (VoWLAN) phones supported by the radio (0 - 60, default = 10).",
            "default": 10,
            "min_value": 0,
            "max_value": 60,
        },
        "bandwidth-admission-control": {
            "type": "option",
            "help": "Enable/disable WiFi multimedia (WMM) bandwidth admission control to optimize WiFi bandwidth use. A request to join the wireless network is only allowed if the access point has enough bandwidth to support it.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "bandwidth-capacity": {
            "type": "integer",
            "help": "Maximum bandwidth capacity allowed (1 - 600000 Kbps, default = 2000).",
            "default": 2000,
            "min_value": 1,
            "max_value": 600000,
        },
    },
    "lbs": {
        "ekahau-blink-mode": {
            "type": "option",
            "help": "Enable/disable Ekahau blink mode (now known as AiRISTA Flow) to track and locate WiFi tags (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ekahau-tag": {
            "type": "mac-address",
            "help": "WiFi frame MAC address or WiFi Tag.",
            "default": "01:18:8e:00:00:00",
        },
        "erc-server-ip": {
            "type": "ipv4-address-any",
            "help": "IP address of Ekahau RTLS Controller (ERC).",
            "default": "0.0.0.0",
        },
        "erc-server-port": {
            "type": "integer",
            "help": "Ekahau RTLS Controller (ERC) UDP listening port.",
            "default": 8569,
            "min_value": 1024,
            "max_value": 65535,
        },
        "aeroscout": {
            "type": "option",
            "help": "Enable/disable AeroScout Real Time Location Service (RTLS) support (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "aeroscout-server-ip": {
            "type": "ipv4-address-any",
            "help": "IP address of AeroScout server.",
            "default": "0.0.0.0",
        },
        "aeroscout-server-port": {
            "type": "integer",
            "help": "AeroScout server UDP listening port.",
            "default": 0,
            "min_value": 1024,
            "max_value": 65535,
        },
        "aeroscout-mu": {
            "type": "option",
            "help": "Enable/disable AeroScout Mobile Unit (MU) support (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "aeroscout-ap-mac": {
            "type": "option",
            "help": "Use BSSID or board MAC address as AP MAC address in AeroScout AP messages (default = bssid).",
            "default": "bssid",
            "options": ["bssid", "board-mac"],
        },
        "aeroscout-mmu-report": {
            "type": "option",
            "help": "Enable/disable compounded AeroScout tag and MU report (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "aeroscout-mu-factor": {
            "type": "integer",
            "help": "AeroScout MU mode dilution factor (default = 20).",
            "default": 20,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "aeroscout-mu-timeout": {
            "type": "integer",
            "help": "AeroScout MU mode timeout (0 - 65535 sec, default = 5).",
            "default": 5,
            "min_value": 0,
            "max_value": 65535,
        },
        "fortipresence": {
            "type": "option",
            "help": "Enable/disable FortiPresence to monitor the location and activity of WiFi clients even if they don't connect to this WiFi network (default = disable).",
            "default": "disable",
            "options": ["foreign", "both", "disable"],
        },
        "fortipresence-server-addr-type": {
            "type": "option",
            "help": "FortiPresence server address type (default = ipv4).",
            "default": "ipv4",
            "options": ["ipv4", "fqdn"],
        },
        "fortipresence-server": {
            "type": "ipv4-address-any",
            "help": "IP address of FortiPresence server.",
            "default": "0.0.0.0",
        },
        "fortipresence-server-fqdn": {
            "type": "string",
            "help": "FQDN of FortiPresence server.",
            "default": "",
            "max_length": 255,
        },
        "fortipresence-port": {
            "type": "integer",
            "help": "UDP listening port of FortiPresence server (default = 3000).",
            "default": 3000,
            "min_value": 300,
            "max_value": 65535,
        },
        "fortipresence-secret": {
            "type": "password",
            "help": "FortiPresence secret password (max. 16 characters).",
            "max_length": 123,
        },
        "fortipresence-project": {
            "type": "string",
            "help": "FortiPresence project name (max. 16 characters, default = fortipresence).",
            "default": "fortipresence",
            "max_length": 16,
        },
        "fortipresence-frequency": {
            "type": "integer",
            "help": "FortiPresence report transmit frequency (5 - 65535 sec, default = 30).",
            "default": 30,
            "min_value": 5,
            "max_value": 65535,
        },
        "fortipresence-rogue": {
            "type": "option",
            "help": "Enable/disable FortiPresence finding and reporting rogue APs.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "fortipresence-unassoc": {
            "type": "option",
            "help": "Enable/disable FortiPresence finding and reporting unassociated stations.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "fortipresence-ble": {
            "type": "option",
            "help": "Enable/disable FortiPresence finding and reporting BLE devices.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "station-locate": {
            "type": "option",
            "help": "Enable/disable client station locating services for all clients, whether associated or not (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ble-rtls": {
            "type": "option",
            "help": "Set BLE Real Time Location Service (RTLS) support (default = none).",
            "default": "none",
            "options": ["none", "polestar", "evresys"],
        },
        "ble-rtls-protocol": {
            "type": "option",
            "help": "Select the protocol to report Measurements, Advertising Data, or Location Data to Cloud Server (default = WSS).",
            "default": "WSS",
            "options": ["WSS"],
        },
        "ble-rtls-server-fqdn": {
            "type": "string",
            "help": "FQDN of BLE Real Time Location Service (RTLS) Server.",
            "default": "",
            "max_length": 255,
        },
        "ble-rtls-server-path": {
            "type": "string",
            "help": "Path of BLE Real Time Location Service (RTLS) Server.",
            "default": "",
            "max_length": 255,
        },
        "ble-rtls-server-token": {
            "type": "string",
            "help": "Access Token of BLE Real Time Location Service (RTLS) Server.",
            "default": "",
            "max_length": 31,
        },
        "ble-rtls-server-port": {
            "type": "integer",
            "help": "Port of BLE Real Time Location Service (RTLS) Server (default = 443).",
            "default": 443,
            "min_value": 1,
            "max_value": 65535,
        },
        "ble-rtls-accumulation-interval": {
            "type": "integer",
            "help": "Time that measurements should be accumulated in seconds (default = 2).",
            "default": 2,
            "min_value": 1,
            "max_value": 60,
        },
        "ble-rtls-reporting-interval": {
            "type": "integer",
            "help": "Time between reporting accumulated measurements in seconds (default = 2).",
            "default": 2,
            "min_value": 1,
            "max_value": 600,
        },
        "ble-rtls-asset-uuid-list1": {
            "type": "string",
            "help": "Tags and asset UUID list 1 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').",
            "default": "",
            "max_length": 36,
        },
        "ble-rtls-asset-uuid-list2": {
            "type": "string",
            "help": "Tags and asset UUID list 2 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').",
            "default": "",
            "max_length": 36,
        },
        "ble-rtls-asset-uuid-list3": {
            "type": "string",
            "help": "Tags and asset UUID list 3 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').",
            "default": "",
            "max_length": 36,
        },
        "ble-rtls-asset-uuid-list4": {
            "type": "string",
            "help": "Tags and asset UUID list 4 to be reported (string in the format of 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX').",
            "default": "",
            "max_length": 36,
        },
        "ble-rtls-asset-addrgrp-list": {
            "type": "string",
            "help": "Tags and asset addrgrp list to be reported.",
            "default": "",
            "max_length": 79,
        },
    },
    "esl-ses-dongle": {
        "compliance-level": {
            "type": "option",
            "help": "Compliance levels for the ESL solution integration (default = compliance-level-2).",
            "default": "compliance-level-2",
            "options": ["compliance-level-2"],
        },
        "scd-enable": {
            "type": "option",
            "help": "Enable/disable ESL SES-imagotag Serial Communication Daemon (SCD) (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "esl-channel": {
            "type": "option",
            "help": "ESL SES-imagotag dongle channel (default = 127).",
            "default": "127",
            "options": ["-1", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "127"],
        },
        "output-power": {
            "type": "option",
            "help": "ESL SES-imagotag dongle output power (default = A).",
            "default": "a",
            "options": ["a", "b", "c", "d", "e", "f", "g", "h"],
        },
        "apc-addr-type": {
            "type": "option",
            "help": "ESL SES-imagotag APC address type (default = fqdn).",
            "default": "fqdn",
            "options": ["fqdn", "ip"],
        },
        "apc-fqdn": {
            "type": "string",
            "help": "FQDN of ESL SES-imagotag Access Point Controller (APC).",
            "default": "",
            "max_length": 63,
        },
        "apc-ip": {
            "type": "ipv4-address",
            "help": "IP address of ESL SES-imagotag Access Point Controller (APC).",
            "default": "0.0.0.0",
        },
        "apc-port": {
            "type": "integer",
            "help": "Port of ESL SES-imagotag Access Point Controller (APC).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "coex-level": {
            "type": "option",
            "help": "ESL SES-imagotag dongle coexistence level (default = none).",
            "default": "none",
            "options": ["none"],
        },
        "tls-cert-verification": {
            "type": "option",
            "help": "Enable/disable TLS certificate verification (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "tls-fqdn-verification": {
            "type": "option",
            "help": "Enable/disable TLS FQDN verification (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_CONTROL_MESSAGE_OFFLOAD = [
    "ebp-frame",
    "aeroscout-tag",
    "ap-list",
    "sta-list",
    "sta-cap-list",
    "stats",
    "aeroscout-mu",
    "sta-health",
    "spectral-analysis",
]
VALID_BODY_APCFG_MESH = [
    "enable",
    "disable",
]
VALID_BODY_APCFG_MESH_AP_TYPE = [
    "ethernet",
    "mesh",
    "auto",
]
VALID_BODY_APCFG_MESH_ETH_BRIDGE = [
    "enable",
    "disable",
]
VALID_BODY_WAN_PORT_MODE = [
    "wan-lan",
    "wan-only",
]
VALID_BODY_ENERGY_EFFICIENT_ETHERNET = [
    "enable",
    "disable",
]
VALID_BODY_LED_STATE = [
    "enable",
    "disable",
]
VALID_BODY_DTLS_POLICY = [
    "clear-text",
    "dtls-enabled",
    "ipsec-vpn",
    "ipsec-sn-vpn",
]
VALID_BODY_DTLS_IN_KERNEL = [
    "enable",
    "disable",
]
VALID_BODY_HANDOFF_ROAMING = [
    "enable",
    "disable",
]
VALID_BODY_AP_COUNTRY = [
    "--",
    "AF",
    "AL",
    "DZ",
    "AS",
    "AO",
    "AR",
    "AM",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BM",
    "BT",
    "BO",
    "BA",
    "BW",
    "BR",
    "BN",
    "BG",
    "BF",
    "KH",
    "CM",
    "KY",
    "CF",
    "TD",
    "CL",
    "CN",
    "CX",
    "CO",
    "CG",
    "CD",
    "CR",
    "HR",
    "CY",
    "CZ",
    "DK",
    "DJ",
    "DM",
    "DO",
    "EC",
    "EG",
    "SV",
    "ET",
    "EE",
    "GF",
    "PF",
    "FO",
    "FJ",
    "FI",
    "FR",
    "GA",
    "GE",
    "GM",
    "DE",
    "GH",
    "GI",
    "GR",
    "GL",
    "GD",
    "GP",
    "GU",
    "GT",
    "GY",
    "HT",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IQ",
    "IE",
    "IM",
    "IL",
    "IT",
    "CI",
    "JM",
    "JO",
    "KZ",
    "KE",
    "KR",
    "KW",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LI",
    "LT",
    "LU",
    "MO",
    "MK",
    "MG",
    "MW",
    "MY",
    "MV",
    "ML",
    "MT",
    "MH",
    "MQ",
    "MR",
    "MU",
    "YT",
    "MX",
    "FM",
    "MD",
    "MC",
    "MN",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NP",
    "NL",
    "AN",
    "AW",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NO",
    "MP",
    "OM",
    "PK",
    "PW",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PL",
    "PT",
    "PR",
    "QA",
    "RE",
    "RO",
    "RU",
    "RW",
    "BL",
    "KN",
    "LC",
    "MF",
    "PM",
    "VC",
    "SA",
    "SN",
    "RS",
    "ME",
    "SL",
    "SG",
    "SK",
    "SI",
    "SO",
    "ZA",
    "ES",
    "LK",
    "SR",
    "SZ",
    "SE",
    "CH",
    "TW",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TT",
    "TN",
    "TR",
    "TM",
    "AE",
    "TC",
    "UG",
    "UA",
    "GB",
    "US",
    "PS",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "VI",
    "WF",
    "YE",
    "ZM",
    "ZW",
    "JP",
    "CA",
]
VALID_BODY_IP_FRAGMENT_PREVENTING = [
    "tcp-mss-adjust",
    "icmp-unreachable",
]
VALID_BODY_SPLIT_TUNNELING_ACL_PATH = [
    "tunnel",
    "local",
]
VALID_BODY_SPLIT_TUNNELING_ACL_LOCAL_AP_SUBNET = [
    "enable",
    "disable",
]
VALID_BODY_ALLOWACCESS = [
    "https",
    "ssh",
    "snmp",
]
VALID_BODY_LOGIN_PASSWD_CHANGE = [
    "yes",
    "default",
    "no",
]
VALID_BODY_LLDP = [
    "enable",
    "disable",
]
VALID_BODY_POE_MODE = [
    "auto",
    "8023af",
    "8023at",
    "power-adapter",
    "full",
    "high",
    "low",
]
VALID_BODY_USB_PORT = [
    "enable",
    "disable",
]
VALID_BODY_FREQUENCY_HANDOFF = [
    "enable",
    "disable",
]
VALID_BODY_AP_HANDOFF = [
    "enable",
    "disable",
]
VALID_BODY_DEFAULT_MESH_ROOT = [
    "enable",
    "disable",
]
VALID_BODY_EXT_INFO_ENABLE = [
    "enable",
    "disable",
]
VALID_BODY_INDOOR_OUTDOOR_DEPLOYMENT = [
    "platform-determined",
    "outdoor",
    "indoor",
]
VALID_BODY_CONSOLE_LOGIN = [
    "enable",
    "disable",
]
VALID_BODY_WAN_PORT_AUTH = [
    "none",
    "802.1x",
]
VALID_BODY_WAN_PORT_AUTH_METHODS = [
    "all",
    "EAP-FAST",
    "EAP-TLS",
    "EAP-PEAP",
]
VALID_BODY_WAN_PORT_AUTH_MACSEC = [
    "enable",
    "disable",
]
VALID_BODY_APCFG_AUTO_CERT = [
    "enable",
    "disable",
]
VALID_BODY_APCFG_AUTO_CERT_ENROLL_PROTOCOL = [
    "none",
    "est",
    "scep",
]
VALID_BODY_APCFG_AUTO_CERT_CRYPTO_ALGO = [
    "rsa-1024",
    "rsa-1536",
    "rsa-2048",
    "rsa-4096",
    "ec-secp256r1",
    "ec-secp384r1",
    "ec-secp521r1",
]
VALID_BODY_APCFG_AUTO_CERT_SCEP_KEYTYPE = [
    "rsa",
    "ec",
]
VALID_BODY_APCFG_AUTO_CERT_SCEP_KEYSIZE = [
    "1024",
    "1536",
    "2048",
    "4096",
]
VALID_BODY_APCFG_AUTO_CERT_SCEP_EC_NAME = [
    "secp256r1",
    "secp384r1",
    "secp521r1",
]
VALID_BODY_UNII_4_5GHZ_BAND = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_RESTRICT_LOCAL = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_wtp_profile_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/wtp_profile."""
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


def validate_wireless_controller_wtp_profile_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/wtp_profile object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "control-message-offload" in payload:
        is_valid, error = _validate_enum_field(
            "control-message-offload",
            payload["control-message-offload"],
            VALID_BODY_CONTROL_MESSAGE_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-mesh" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-mesh",
            payload["apcfg-mesh"],
            VALID_BODY_APCFG_MESH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-mesh-ap-type" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-mesh-ap-type",
            payload["apcfg-mesh-ap-type"],
            VALID_BODY_APCFG_MESH_AP_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-mesh-eth-bridge" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-mesh-eth-bridge",
            payload["apcfg-mesh-eth-bridge"],
            VALID_BODY_APCFG_MESH_ETH_BRIDGE,
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
    if "energy-efficient-ethernet" in payload:
        is_valid, error = _validate_enum_field(
            "energy-efficient-ethernet",
            payload["energy-efficient-ethernet"],
            VALID_BODY_ENERGY_EFFICIENT_ETHERNET,
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
    if "dtls-policy" in payload:
        is_valid, error = _validate_enum_field(
            "dtls-policy",
            payload["dtls-policy"],
            VALID_BODY_DTLS_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dtls-in-kernel" in payload:
        is_valid, error = _validate_enum_field(
            "dtls-in-kernel",
            payload["dtls-in-kernel"],
            VALID_BODY_DTLS_IN_KERNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "handoff-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "handoff-roaming",
            payload["handoff-roaming"],
            VALID_BODY_HANDOFF_ROAMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-country" in payload:
        is_valid, error = _validate_enum_field(
            "ap-country",
            payload["ap-country"],
            VALID_BODY_AP_COUNTRY,
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
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
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
    if "lldp" in payload:
        is_valid, error = _validate_enum_field(
            "lldp",
            payload["lldp"],
            VALID_BODY_LLDP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "poe-mode" in payload:
        is_valid, error = _validate_enum_field(
            "poe-mode",
            payload["poe-mode"],
            VALID_BODY_POE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "usb-port" in payload:
        is_valid, error = _validate_enum_field(
            "usb-port",
            payload["usb-port"],
            VALID_BODY_USB_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "frequency-handoff" in payload:
        is_valid, error = _validate_enum_field(
            "frequency-handoff",
            payload["frequency-handoff"],
            VALID_BODY_FREQUENCY_HANDOFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-handoff" in payload:
        is_valid, error = _validate_enum_field(
            "ap-handoff",
            payload["ap-handoff"],
            VALID_BODY_AP_HANDOFF,
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
    if "ext-info-enable" in payload:
        is_valid, error = _validate_enum_field(
            "ext-info-enable",
            payload["ext-info-enable"],
            VALID_BODY_EXT_INFO_ENABLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "indoor-outdoor-deployment" in payload:
        is_valid, error = _validate_enum_field(
            "indoor-outdoor-deployment",
            payload["indoor-outdoor-deployment"],
            VALID_BODY_INDOOR_OUTDOOR_DEPLOYMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "console-login" in payload:
        is_valid, error = _validate_enum_field(
            "console-login",
            payload["console-login"],
            VALID_BODY_CONSOLE_LOGIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-auth" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-auth",
            payload["wan-port-auth"],
            VALID_BODY_WAN_PORT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-auth-methods" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-auth-methods",
            payload["wan-port-auth-methods"],
            VALID_BODY_WAN_PORT_AUTH_METHODS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-auth-macsec" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-auth-macsec",
            payload["wan-port-auth-macsec"],
            VALID_BODY_WAN_PORT_AUTH_MACSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert",
            payload["apcfg-auto-cert"],
            VALID_BODY_APCFG_AUTO_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-enroll-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-enroll-protocol",
            payload["apcfg-auto-cert-enroll-protocol"],
            VALID_BODY_APCFG_AUTO_CERT_ENROLL_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-crypto-algo" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-crypto-algo",
            payload["apcfg-auto-cert-crypto-algo"],
            VALID_BODY_APCFG_AUTO_CERT_CRYPTO_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-scep-keytype" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-scep-keytype",
            payload["apcfg-auto-cert-scep-keytype"],
            VALID_BODY_APCFG_AUTO_CERT_SCEP_KEYTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-scep-keysize" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-scep-keysize",
            payload["apcfg-auto-cert-scep-keysize"],
            VALID_BODY_APCFG_AUTO_CERT_SCEP_KEYSIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-scep-ec-name" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-scep-ec-name",
            payload["apcfg-auto-cert-scep-ec-name"],
            VALID_BODY_APCFG_AUTO_CERT_SCEP_EC_NAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unii-4-5ghz-band" in payload:
        is_valid, error = _validate_enum_field(
            "unii-4-5ghz-band",
            payload["unii-4-5ghz-band"],
            VALID_BODY_UNII_4_5GHZ_BAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-restrict-local" in payload:
        is_valid, error = _validate_enum_field(
            "admin-restrict-local",
            payload["admin-restrict-local"],
            VALID_BODY_ADMIN_RESTRICT_LOCAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_wtp_profile_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/wtp_profile."""
    # Validate enum values using central function
    if "control-message-offload" in payload:
        is_valid, error = _validate_enum_field(
            "control-message-offload",
            payload["control-message-offload"],
            VALID_BODY_CONTROL_MESSAGE_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-mesh" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-mesh",
            payload["apcfg-mesh"],
            VALID_BODY_APCFG_MESH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-mesh-ap-type" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-mesh-ap-type",
            payload["apcfg-mesh-ap-type"],
            VALID_BODY_APCFG_MESH_AP_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-mesh-eth-bridge" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-mesh-eth-bridge",
            payload["apcfg-mesh-eth-bridge"],
            VALID_BODY_APCFG_MESH_ETH_BRIDGE,
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
    if "energy-efficient-ethernet" in payload:
        is_valid, error = _validate_enum_field(
            "energy-efficient-ethernet",
            payload["energy-efficient-ethernet"],
            VALID_BODY_ENERGY_EFFICIENT_ETHERNET,
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
    if "dtls-policy" in payload:
        is_valid, error = _validate_enum_field(
            "dtls-policy",
            payload["dtls-policy"],
            VALID_BODY_DTLS_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dtls-in-kernel" in payload:
        is_valid, error = _validate_enum_field(
            "dtls-in-kernel",
            payload["dtls-in-kernel"],
            VALID_BODY_DTLS_IN_KERNEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "handoff-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "handoff-roaming",
            payload["handoff-roaming"],
            VALID_BODY_HANDOFF_ROAMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-country" in payload:
        is_valid, error = _validate_enum_field(
            "ap-country",
            payload["ap-country"],
            VALID_BODY_AP_COUNTRY,
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
    if "allowaccess" in payload:
        is_valid, error = _validate_enum_field(
            "allowaccess",
            payload["allowaccess"],
            VALID_BODY_ALLOWACCESS,
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
    if "lldp" in payload:
        is_valid, error = _validate_enum_field(
            "lldp",
            payload["lldp"],
            VALID_BODY_LLDP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "poe-mode" in payload:
        is_valid, error = _validate_enum_field(
            "poe-mode",
            payload["poe-mode"],
            VALID_BODY_POE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "usb-port" in payload:
        is_valid, error = _validate_enum_field(
            "usb-port",
            payload["usb-port"],
            VALID_BODY_USB_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "frequency-handoff" in payload:
        is_valid, error = _validate_enum_field(
            "frequency-handoff",
            payload["frequency-handoff"],
            VALID_BODY_FREQUENCY_HANDOFF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-handoff" in payload:
        is_valid, error = _validate_enum_field(
            "ap-handoff",
            payload["ap-handoff"],
            VALID_BODY_AP_HANDOFF,
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
    if "ext-info-enable" in payload:
        is_valid, error = _validate_enum_field(
            "ext-info-enable",
            payload["ext-info-enable"],
            VALID_BODY_EXT_INFO_ENABLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "indoor-outdoor-deployment" in payload:
        is_valid, error = _validate_enum_field(
            "indoor-outdoor-deployment",
            payload["indoor-outdoor-deployment"],
            VALID_BODY_INDOOR_OUTDOOR_DEPLOYMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "console-login" in payload:
        is_valid, error = _validate_enum_field(
            "console-login",
            payload["console-login"],
            VALID_BODY_CONSOLE_LOGIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-auth" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-auth",
            payload["wan-port-auth"],
            VALID_BODY_WAN_PORT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-auth-methods" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-auth-methods",
            payload["wan-port-auth-methods"],
            VALID_BODY_WAN_PORT_AUTH_METHODS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wan-port-auth-macsec" in payload:
        is_valid, error = _validate_enum_field(
            "wan-port-auth-macsec",
            payload["wan-port-auth-macsec"],
            VALID_BODY_WAN_PORT_AUTH_MACSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert",
            payload["apcfg-auto-cert"],
            VALID_BODY_APCFG_AUTO_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-enroll-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-enroll-protocol",
            payload["apcfg-auto-cert-enroll-protocol"],
            VALID_BODY_APCFG_AUTO_CERT_ENROLL_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-crypto-algo" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-crypto-algo",
            payload["apcfg-auto-cert-crypto-algo"],
            VALID_BODY_APCFG_AUTO_CERT_CRYPTO_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-scep-keytype" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-scep-keytype",
            payload["apcfg-auto-cert-scep-keytype"],
            VALID_BODY_APCFG_AUTO_CERT_SCEP_KEYTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-scep-keysize" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-scep-keysize",
            payload["apcfg-auto-cert-scep-keysize"],
            VALID_BODY_APCFG_AUTO_CERT_SCEP_KEYSIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "apcfg-auto-cert-scep-ec-name" in payload:
        is_valid, error = _validate_enum_field(
            "apcfg-auto-cert-scep-ec-name",
            payload["apcfg-auto-cert-scep-ec-name"],
            VALID_BODY_APCFG_AUTO_CERT_SCEP_EC_NAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unii-4-5ghz-band" in payload:
        is_valid, error = _validate_enum_field(
            "unii-4-5ghz-band",
            payload["unii-4-5ghz-band"],
            VALID_BODY_UNII_4_5GHZ_BAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-restrict-local" in payload:
        is_valid, error = _validate_enum_field(
            "admin-restrict-local",
            payload["admin-restrict-local"],
            VALID_BODY_ADMIN_RESTRICT_LOCAL,
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
    "endpoint": "wireless_controller/wtp_profile",
    "category": "cmdb",
    "api_path": "wireless-controller/wtp-profile",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure WTP profiles or FortiAP profiles that define radio settings for manageable FortiAP platforms.",
    "total_fields": 78,
    "required_fields_count": 0,
    "fields_with_defaults_count": 62,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
