"""Validation helpers for switch_controller/managed_switch - Auto-generated"""

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
    "switch-id",  # Managed-switch name.
    "sn",  # Managed-switch serial number.
    "fsw-wan1-peer",  # FortiSwitch WAN1 peer port.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "switch-id": "",
    "sn": "",
    "description": "",
    "switch-profile": "default",
    "access-profile": "default",
    "purdue-level": "3",
    "fsw-wan1-peer": "",
    "fsw-wan1-admin": "discovered",
    "poe-pre-standard-detection": "disable",
    "dhcp-server-access-list": "global",
    "poe-detection-type": 0,
    "max-poe-budget": 0,
    "directly-connected": 0,
    "version": 0,
    "max-allowed-trunk-members": 0,
    "pre-provisioned": 0,
    "l3-discovered": 0,
    "mgmt-mode": 0,
    "tunnel-discovered": 0,
    "tdr-supported": "",
    "dynamic-capability": "0x00000000000000000000000000000000",
    "switch-device-tag": "",
    "switch-dhcp_opt43_key": "",
    "mclag-igmp-snooping-aware": "enable",
    "dynamically-discovered": 0,
    "ptp-status": "disable",
    "ptp-profile": "default",
    "radius-nas-ip-override": "disable",
    "radius-nas-ip": "0.0.0.0",
    "route-offload": "disable",
    "route-offload-mclag": "disable",
    "type": "physical",
    "owner-vdom": "",
    "flow-identity": "00000000",
    "staged-image-version": "",
    "delayed-restart-trigger": 0,
    "firmware-provision": "disable",
    "firmware-provision-version": "",
    "firmware-provision-latest": "disable",
    "override-snmp-sysinfo": "disable",
    "override-snmp-trap-threshold": "disable",
    "override-snmp-community": "disable",
    "override-snmp-user": "disable",
    "qos-drop-policy": "taildrop",
    "qos-red-probability": 12,
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
    "switch-id": "string",  # Managed-switch name.
    "sn": "string",  # Managed-switch serial number.
    "description": "string",  # Description.
    "switch-profile": "string",  # FortiSwitch profile.
    "access-profile": "string",  # FortiSwitch access profile.
    "purdue-level": "option",  # Purdue Level of this FortiSwitch.
    "fsw-wan1-peer": "string",  # FortiSwitch WAN1 peer port.
    "fsw-wan1-admin": "option",  # FortiSwitch WAN1 admin status; enable to authorize the Forti
    "poe-pre-standard-detection": "option",  # Enable/disable PoE pre-standard detection.
    "dhcp-server-access-list": "option",  # DHCP snooping server access list.
    "poe-detection-type": "integer",  # PoE detection type for FortiSwitch.
    "max-poe-budget": "integer",  # Max PoE budget for FortiSwitch.
    "directly-connected": "integer",  # Directly connected FortiSwitch.
    "version": "integer",  # FortiSwitch version.
    "max-allowed-trunk-members": "integer",  # FortiSwitch maximum allowed trunk members.
    "pre-provisioned": "integer",  # Pre-provisioned managed switch.
    "l3-discovered": "integer",  # Layer 3 management discovered.
    "mgmt-mode": "integer",  # FortiLink management mode.
    "tunnel-discovered": "integer",  # SOCKS tunnel management discovered.
    "tdr-supported": "string",  # TDR supported.
    "dynamic-capability": "user",  # List of features this FortiSwitch supports (not configurable
    "switch-device-tag": "string",  # User definable label/tag.
    "switch-dhcp_opt43_key": "string",  # DHCP option43 key.
    "mclag-igmp-snooping-aware": "option",  # Enable/disable MCLAG IGMP-snooping awareness.
    "dynamically-discovered": "integer",  # Dynamically discovered FortiSwitch.
    "ptp-status": "option",  # Enable/disable PTP profile on this FortiSwitch.
    "ptp-profile": "string",  # PTP profile configuration.
    "radius-nas-ip-override": "option",  # Use locally defined NAS-IP.
    "radius-nas-ip": "ipv4-address",  # NAS-IP address.
    "route-offload": "option",  # Enable/disable route offload on this FortiSwitch.
    "route-offload-mclag": "option",  # Enable/disable route offload MCLAG on this FortiSwitch.
    "route-offload-router": "string",  # Configure route offload MCLAG IP address.
    "vlan": "string",  # Configure VLAN assignment priority.
    "type": "option",  # Indication of switch type, physical or virtual.
    "owner-vdom": "string",  # VDOM which owner of port belongs to.
    "flow-identity": "user",  # Flow-tracking netflow ipfix switch identity in hex format(00
    "staged-image-version": "string",  # Staged image version for FortiSwitch.
    "delayed-restart-trigger": "integer",  # Delayed restart triggered for this FortiSwitch.
    "firmware-provision": "option",  # Enable/disable provisioning of firmware to FortiSwitches on 
    "firmware-provision-version": "string",  # Firmware version to provision to this FortiSwitch on bootup 
    "firmware-provision-latest": "option",  # Enable/disable one-time automatic provisioning of the latest
    "ports": "string",  # Managed-switch port list.
    "ip-source-guard": "string",  # IP source guard.
    "stp-settings": "string",  # Configuration method to edit Spanning Tree Protocol (STP) se
    "stp-instance": "string",  # Configuration method to edit Spanning Tree Protocol (STP) in
    "override-snmp-sysinfo": "option",  # Enable/disable overriding the global SNMP system information
    "snmp-sysinfo": "string",  # Configuration method to edit Simple Network Management Proto
    "override-snmp-trap-threshold": "option",  # Enable/disable overriding the global SNMP trap threshold val
    "snmp-trap-threshold": "string",  # Configuration method to edit Simple Network Management Proto
    "override-snmp-community": "option",  # Enable/disable overriding the global SNMP communities.
    "snmp-community": "string",  # Configuration method to edit Simple Network Management Proto
    "override-snmp-user": "option",  # Enable/disable overriding the global SNMP users.
    "snmp-user": "string",  # Configuration method to edit Simple Network Management Proto
    "qos-drop-policy": "option",  # Set QoS drop-policy.
    "qos-red-probability": "integer",  # Set QoS RED/WRED drop probability.
    "switch-log": "string",  # Configuration method to edit FortiSwitch logging settings (l
    "remote-log": "string",  # Configure logging by FortiSwitch device to a remote syslog s
    "storm-control": "string",  # Configuration method to edit FortiSwitch storm control for m
    "mirror": "string",  # Configuration method to edit FortiSwitch packet mirror.
    "static-mac": "string",  # Configuration method to edit FortiSwitch Static and Sticky M
    "custom-command": "string",  # Configuration method to edit FortiSwitch commands to be push
    "dhcp-snooping-static-client": "string",  # Configure FortiSwitch DHCP snooping static clients.
    "igmp-snooping": "string",  # Configure FortiSwitch IGMP snooping global settings.
    "802-1X-settings": "string",  # Configuration method to edit FortiSwitch 802.1X global setti
    "router-vrf": "string",  # Configure VRF.
    "system-interface": "string",  # Configure system interface on FortiSwitch.
    "router-static": "string",  # Configure static routes.
    "system-dhcp-server": "string",  # Configure DHCP servers.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "switch-id": "Managed-switch name.",
    "sn": "Managed-switch serial number.",
    "description": "Description.",
    "switch-profile": "FortiSwitch profile.",
    "access-profile": "FortiSwitch access profile.",
    "purdue-level": "Purdue Level of this FortiSwitch.",
    "fsw-wan1-peer": "FortiSwitch WAN1 peer port.",
    "fsw-wan1-admin": "FortiSwitch WAN1 admin status; enable to authorize the FortiSwitch as a managed switch.",
    "poe-pre-standard-detection": "Enable/disable PoE pre-standard detection.",
    "dhcp-server-access-list": "DHCP snooping server access list.",
    "poe-detection-type": "PoE detection type for FortiSwitch.",
    "max-poe-budget": "Max PoE budget for FortiSwitch.",
    "directly-connected": "Directly connected FortiSwitch.",
    "version": "FortiSwitch version.",
    "max-allowed-trunk-members": "FortiSwitch maximum allowed trunk members.",
    "pre-provisioned": "Pre-provisioned managed switch.",
    "l3-discovered": "Layer 3 management discovered.",
    "mgmt-mode": "FortiLink management mode.",
    "tunnel-discovered": "SOCKS tunnel management discovered.",
    "tdr-supported": "TDR supported.",
    "dynamic-capability": "List of features this FortiSwitch supports (not configurable) that is sent to the FortiGate device for subsequent configuration initiated by the FortiGate device.",
    "switch-device-tag": "User definable label/tag.",
    "switch-dhcp_opt43_key": "DHCP option43 key.",
    "mclag-igmp-snooping-aware": "Enable/disable MCLAG IGMP-snooping awareness.",
    "dynamically-discovered": "Dynamically discovered FortiSwitch.",
    "ptp-status": "Enable/disable PTP profile on this FortiSwitch.",
    "ptp-profile": "PTP profile configuration.",
    "radius-nas-ip-override": "Use locally defined NAS-IP.",
    "radius-nas-ip": "NAS-IP address.",
    "route-offload": "Enable/disable route offload on this FortiSwitch.",
    "route-offload-mclag": "Enable/disable route offload MCLAG on this FortiSwitch.",
    "route-offload-router": "Configure route offload MCLAG IP address.",
    "vlan": "Configure VLAN assignment priority.",
    "type": "Indication of switch type, physical or virtual.",
    "owner-vdom": "VDOM which owner of port belongs to.",
    "flow-identity": "Flow-tracking netflow ipfix switch identity in hex format(00000000-FFFFFFFF default=0).",
    "staged-image-version": "Staged image version for FortiSwitch.",
    "delayed-restart-trigger": "Delayed restart triggered for this FortiSwitch.",
    "firmware-provision": "Enable/disable provisioning of firmware to FortiSwitches on join connection.",
    "firmware-provision-version": "Firmware version to provision to this FortiSwitch on bootup (major.minor.build, i.e. 6.2.1234).",
    "firmware-provision-latest": "Enable/disable one-time automatic provisioning of the latest firmware version.",
    "ports": "Managed-switch port list.",
    "ip-source-guard": "IP source guard.",
    "stp-settings": "Configuration method to edit Spanning Tree Protocol (STP) settings used to prevent bridge loops.",
    "stp-instance": "Configuration method to edit Spanning Tree Protocol (STP) instances.",
    "override-snmp-sysinfo": "Enable/disable overriding the global SNMP system information.",
    "snmp-sysinfo": "Configuration method to edit Simple Network Management Protocol (SNMP) system info.",
    "override-snmp-trap-threshold": "Enable/disable overriding the global SNMP trap threshold values.",
    "snmp-trap-threshold": "Configuration method to edit Simple Network Management Protocol (SNMP) trap threshold values.",
    "override-snmp-community": "Enable/disable overriding the global SNMP communities.",
    "snmp-community": "Configuration method to edit Simple Network Management Protocol (SNMP) communities.",
    "override-snmp-user": "Enable/disable overriding the global SNMP users.",
    "snmp-user": "Configuration method to edit Simple Network Management Protocol (SNMP) users.",
    "qos-drop-policy": "Set QoS drop-policy.",
    "qos-red-probability": "Set QoS RED/WRED drop probability.",
    "switch-log": "Configuration method to edit FortiSwitch logging settings (logs are transferred to and inserted into the FortiGate event log).",
    "remote-log": "Configure logging by FortiSwitch device to a remote syslog server.",
    "storm-control": "Configuration method to edit FortiSwitch storm control for measuring traffic activity using data rates to prevent traffic disruption.",
    "mirror": "Configuration method to edit FortiSwitch packet mirror.",
    "static-mac": "Configuration method to edit FortiSwitch Static and Sticky MAC.",
    "custom-command": "Configuration method to edit FortiSwitch commands to be pushed to this FortiSwitch device upon rebooting the FortiGate switch controller or the FortiSwitch.",
    "dhcp-snooping-static-client": "Configure FortiSwitch DHCP snooping static clients.",
    "igmp-snooping": "Configure FortiSwitch IGMP snooping global settings.",
    "802-1X-settings": "Configuration method to edit FortiSwitch 802.1X global settings.",
    "router-vrf": "Configure VRF.",
    "system-interface": "Configure system interface on FortiSwitch.",
    "router-static": "Configure static routes.",
    "system-dhcp-server": "Configure DHCP servers.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "switch-id": {"type": "string", "max_length": 35},
    "sn": {"type": "string", "max_length": 16},
    "description": {"type": "string", "max_length": 63},
    "switch-profile": {"type": "string", "max_length": 35},
    "access-profile": {"type": "string", "max_length": 31},
    "fsw-wan1-peer": {"type": "string", "max_length": 35},
    "poe-detection-type": {"type": "integer", "min": 0, "max": 255},
    "max-poe-budget": {"type": "integer", "min": 0, "max": 65535},
    "directly-connected": {"type": "integer", "min": 0, "max": 1},
    "version": {"type": "integer", "min": 0, "max": 255},
    "max-allowed-trunk-members": {"type": "integer", "min": 0, "max": 255},
    "pre-provisioned": {"type": "integer", "min": 0, "max": 255},
    "l3-discovered": {"type": "integer", "min": 0, "max": 1},
    "mgmt-mode": {"type": "integer", "min": 0, "max": 255},
    "tunnel-discovered": {"type": "integer", "min": 0, "max": 1},
    "tdr-supported": {"type": "string", "max_length": 31},
    "switch-device-tag": {"type": "string", "max_length": 32},
    "switch-dhcp_opt43_key": {"type": "string", "max_length": 63},
    "dynamically-discovered": {"type": "integer", "min": 0, "max": 1},
    "ptp-profile": {"type": "string", "max_length": 63},
    "owner-vdom": {"type": "string", "max_length": 31},
    "staged-image-version": {"type": "string", "max_length": 127},
    "delayed-restart-trigger": {"type": "integer", "min": 0, "max": 255},
    "firmware-provision-version": {"type": "string", "max_length": 35},
    "qos-red-probability": {"type": "integer", "min": 0, "max": 100},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "route-offload-router": {
        "vlan-name": {
            "type": "string",
            "help": "VLAN name.",
            "default": "",
            "max_length": 15,
        },
        "router-ip": {
            "type": "ipv4-address",
            "help": "Router IP address.",
            "required": True,
            "default": "0.0.0.0",
        },
    },
    "vlan": {
        "vlan-name": {
            "type": "string",
            "help": "VLAN name.",
            "default": "",
            "max_length": 15,
        },
        "assignment-priority": {
            "type": "integer",
            "help": "802.1x Radius (Tunnel-Private-Group-Id) VLANID assign-by-name priority. A smaller value has a higher priority.",
            "required": True,
            "default": 128,
            "min_value": 1,
            "max_value": 255,
        },
    },
    "ports": {
        "port-name": {
            "type": "string",
            "help": "Switch port name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "port-owner": {
            "type": "string",
            "help": "Switch port name.",
            "default": "",
            "max_length": 15,
        },
        "switch-id": {
            "type": "string",
            "help": "Switch id.",
            "default": "",
            "max_length": 35,
        },
        "speed": {
            "type": "option",
            "help": "Switch port speed; default and available settings depend on hardware.",
            "default": "auto",
            "options": ["10half", "10full", "100half", "100full", "1000full", "10000full", "auto", "1000auto", "1000full-fiber", "40000full", "auto-module", "100FX-half", "100FX-full", "100000full", "2500auto", "2500full", "25000full", "50000full", "10000cr", "10000sr", "100000sr4", "100000cr4", "40000sr4", "40000cr4", "40000auto", "25000cr", "25000sr", "50000cr", "50000sr", "5000auto", "sgmii-auto"],
        },
        "status": {
            "type": "option",
            "help": "Switch port admin status: up or down.",
            "default": "up",
            "options": ["up", "down"],
        },
        "poe-status": {
            "type": "option",
            "help": "Enable/disable PoE status.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ip-source-guard": {
            "type": "option",
            "help": "Enable/disable IP source guard.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "ptp-status": {
            "type": "option",
            "help": "Enable/disable PTP policy on this FortiSwitch port.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "ptp-policy": {
            "type": "string",
            "help": "PTP policy configuration.",
            "default": "default",
            "max_length": 63,
        },
        "aggregator-mode": {
            "type": "option",
            "help": "LACP member select mode.",
            "default": "bandwidth",
            "options": ["bandwidth", "count"],
        },
        "flapguard": {
            "type": "option",
            "help": "Enable/disable flap guard.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "flap-rate": {
            "type": "integer",
            "help": "Number of stage change events needed within flap-duration.",
            "default": 5,
            "min_value": 1,
            "max_value": 30,
        },
        "flap-duration": {
            "type": "integer",
            "help": "Period over which flap events are calculated (seconds).",
            "default": 30,
            "min_value": 5,
            "max_value": 300,
        },
        "flap-timeout": {
            "type": "integer",
            "help": "Flap guard disabling protection (min).",
            "default": 0,
            "min_value": 0,
            "max_value": 120,
        },
        "rpvst-port": {
            "type": "option",
            "help": "Enable/disable inter-operability with rapid PVST on this interface.",
            "default": "disabled",
            "options": ["disabled", "enabled"],
        },
        "poe-pre-standard-detection": {
            "type": "option",
            "help": "Enable/disable PoE pre-standard detection.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "port-number": {
            "type": "integer",
            "help": "Port number.",
            "default": 0,
            "min_value": 1,
            "max_value": 64,
        },
        "port-prefix-type": {
            "type": "integer",
            "help": "Port prefix type.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "fortilink-port": {
            "type": "integer",
            "help": "FortiLink uplink port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "poe-capable": {
            "type": "integer",
            "help": "PoE capable.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "pd-capable": {
            "type": "integer",
            "help": "Powered device capable.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "stacking-port": {
            "type": "integer",
            "help": "Stacking port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "p2p-port": {
            "type": "integer",
            "help": "General peer to peer tunnel port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "mclag-icl-port": {
            "type": "integer",
            "help": "MCLAG-ICL port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "authenticated-port": {
            "type": "integer",
            "help": "Peer to Peer Authenticated port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "restricted-auth-port": {
            "type": "integer",
            "help": "Peer to Peer Restricted Authenticated port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "encrypted-port": {
            "type": "integer",
            "help": "Peer to Peer Encrypted port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "fiber-port": {
            "type": "integer",
            "help": "Fiber-port.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "media-type": {
            "type": "string",
            "help": "Media type.",
            "default": "",
            "max_length": 31,
        },
        "poe-standard": {
            "type": "string",
            "help": "PoE standard supported.",
            "default": "",
            "max_length": 63,
        },
        "poe-max-power": {
            "type": "string",
            "help": "PoE maximum power.",
            "default": "",
            "max_length": 35,
        },
        "poe-mode-bt-cabable": {
            "type": "integer",
            "help": "PoE mode IEEE 802.3BT capable.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "poe-port-mode": {
            "type": "option",
            "help": "Configure PoE port mode.",
            "default": "ieee802-3at",
            "options": ["ieee802-3af", "ieee802-3at", "ieee802-3bt"],
        },
        "poe-port-priority": {
            "type": "option",
            "help": "Configure PoE port priority.",
            "default": "low-priority",
            "options": ["critical-priority", "high-priority", "low-priority", "medium-priority"],
        },
        "poe-port-power": {
            "type": "option",
            "help": "Configure PoE port power.",
            "default": "normal",
            "options": ["normal", "perpetual", "perpetual-fast"],
        },
        "flags": {
            "type": "integer",
            "help": "Port properties flags.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "isl-local-trunk-name": {
            "type": "string",
            "help": "ISL local trunk name.",
            "default": "",
            "max_length": 15,
        },
        "isl-peer-port-name": {
            "type": "string",
            "help": "ISL peer port name.",
            "default": "",
            "max_length": 15,
        },
        "isl-peer-device-name": {
            "type": "string",
            "help": "ISL peer device name.",
            "default": "",
            "max_length": 35,
        },
        "isl-peer-device-sn": {
            "type": "string",
            "help": "ISL peer device serial number.",
            "default": "",
            "max_length": 16,
        },
        "fgt-peer-port-name": {
            "type": "string",
            "help": "FGT peer port name.",
            "default": "",
            "max_length": 15,
        },
        "fgt-peer-device-name": {
            "type": "string",
            "help": "FGT peer device name.",
            "default": "",
            "max_length": 35,
        },
        "vlan": {
            "type": "string",
            "help": "Assign switch ports to a VLAN.",
            "default": "",
            "max_length": 15,
        },
        "allowed-vlans-all": {
            "type": "option",
            "help": "Enable/disable all defined vlans on this port.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "allowed-vlans": {
            "type": "string",
            "help": "Configure switch port tagged VLANs.",
        },
        "untagged-vlans": {
            "type": "string",
            "help": "Configure switch port untagged VLANs.",
        },
        "type": {
            "type": "option",
            "help": "Interface type: physical or trunk port.",
            "default": "physical",
            "options": ["physical", "trunk"],
        },
        "access-mode": {
            "type": "option",
            "help": "Access mode of the port.",
            "default": "static",
            "options": ["dynamic", "nac", "static"],
        },
        "matched-dpp-policy": {
            "type": "string",
            "help": "Matched child policy in the dynamic port policy.",
            "default": "",
            "max_length": 63,
        },
        "matched-dpp-intf-tags": {
            "type": "string",
            "help": "Matched interface tags in the dynamic port policy.",
            "default": "",
            "max_length": 63,
        },
        "acl-group": {
            "type": "string",
            "help": "ACL groups on this port.",
        },
        "fortiswitch-acls": {
            "type": "string",
            "help": "ACLs on this port.",
        },
        "dhcp-snooping": {
            "type": "option",
            "help": "Trusted or untrusted DHCP-snooping interface.",
            "default": "untrusted",
            "options": ["untrusted", "trusted"],
        },
        "dhcp-snoop-option82-trust": {
            "type": "option",
            "help": "Enable/disable allowance of DHCP with option-82 on untrusted interface.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dhcp-snoop-option82-override": {
            "type": "string",
            "help": "Configure DHCP snooping option 82 override.",
        },
        "arp-inspection-trust": {
            "type": "option",
            "help": "Trusted or untrusted dynamic ARP inspection.",
            "default": "untrusted",
            "options": ["untrusted", "trusted"],
        },
        "igmp-snooping-flood-reports": {
            "type": "option",
            "help": "Enable/disable flooding of IGMP reports to this interface when igmp-snooping enabled.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "mcast-snooping-flood-traffic": {
            "type": "option",
            "help": "Enable/disable flooding of IGMP snooping traffic to this interface.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "stp-state": {
            "type": "option",
            "help": "Enable/disable Spanning Tree Protocol (STP) on this interface.",
            "default": "enabled",
            "options": ["enabled", "disabled"],
        },
        "stp-root-guard": {
            "type": "option",
            "help": "Enable/disable STP root guard on this interface.",
            "default": "disabled",
            "options": ["enabled", "disabled"],
        },
        "stp-bpdu-guard": {
            "type": "option",
            "help": "Enable/disable STP BPDU guard on this interface.",
            "default": "disabled",
            "options": ["enabled", "disabled"],
        },
        "stp-bpdu-guard-timeout": {
            "type": "integer",
            "help": "BPDU Guard disabling protection (0 - 120 min).",
            "default": 5,
            "min_value": 0,
            "max_value": 120,
        },
        "edge-port": {
            "type": "option",
            "help": "Enable/disable this interface as an edge port, bridging connections between workstations and/or computers.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "discard-mode": {
            "type": "option",
            "help": "Configure discard mode for port.",
            "default": "none",
            "options": ["none", "all-untagged", "all-tagged"],
        },
        "packet-sampler": {
            "type": "option",
            "help": "Enable/disable packet sampling on this interface.",
            "default": "disabled",
            "options": ["enabled", "disabled"],
        },
        "packet-sample-rate": {
            "type": "integer",
            "help": "Packet sampling rate (0 - 99999 p/sec).",
            "default": 512,
            "min_value": 0,
            "max_value": 99999,
        },
        "sflow-counter-interval": {
            "type": "integer",
            "help": "sFlow sampling counter polling interval in seconds (0 - 255).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "sample-direction": {
            "type": "option",
            "help": "Packet sampling direction.",
            "default": "both",
            "options": ["tx", "rx", "both"],
        },
        "fec-capable": {
            "type": "integer",
            "help": "FEC capable.",
            "default": 0,
            "min_value": 0,
            "max_value": 1,
        },
        "fec-state": {
            "type": "option",
            "help": "State of forward error correction.",
            "default": "detect-by-module",
            "options": ["disabled", "cl74", "cl91", "detect-by-module"],
        },
        "flow-control": {
            "type": "option",
            "help": "Flow control direction.",
            "default": "disable",
            "options": ["disable", "tx", "rx", "both"],
        },
        "pause-meter": {
            "type": "integer",
            "help": "Configure ingress pause metering rate, in kbps (default = 0, disabled).",
            "default": 0,
            "min_value": 128,
            "max_value": 2147483647,
        },
        "pause-meter-resume": {
            "type": "option",
            "help": "Resume threshold for resuming traffic on ingress port.",
            "default": "50%",
            "options": ["75%", "50%", "25%"],
        },
        "loop-guard": {
            "type": "option",
            "help": "Enable/disable loop-guard on this interface, an STP optimization used to prevent network loops.",
            "default": "disabled",
            "options": ["enabled", "disabled"],
        },
        "loop-guard-timeout": {
            "type": "integer",
            "help": "Loop-guard timeout (0 - 120 min, default = 45).",
            "default": 45,
            "min_value": 0,
            "max_value": 120,
        },
        "port-policy": {
            "type": "string",
            "help": "Switch controller dynamic port policy from available options.",
            "default": "",
            "max_length": 63,
        },
        "qos-policy": {
            "type": "string",
            "help": "Switch controller QoS policy from available options.",
            "default": "default",
            "max_length": 63,
        },
        "storm-control-policy": {
            "type": "string",
            "help": "Switch controller storm control policy from available options.",
            "default": "default",
            "max_length": 63,
        },
        "port-security-policy": {
            "type": "string",
            "help": "Switch controller authentication policy to apply to this managed switch from available options.",
            "default": "",
            "max_length": 31,
        },
        "export-to-pool": {
            "type": "string",
            "help": "Switch controller export port to pool-list.",
            "default": "",
            "max_length": 35,
        },
        "interface-tags": {
            "type": "string",
            "help": "Tag(s) associated with the interface for various features including virtual port pool, dynamic port policy.",
        },
        "learning-limit": {
            "type": "integer",
            "help": "Limit the number of dynamic MAC addresses on this Port (1 - 128, 0 = no limit, default).",
            "default": 0,
            "min_value": 0,
            "max_value": 128,
        },
        "sticky-mac": {
            "type": "option",
            "help": "Enable or disable sticky-mac on the interface.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "lldp-status": {
            "type": "option",
            "help": "LLDP transmit and receive status.",
            "default": "tx-rx",
            "options": ["disable", "rx-only", "tx-only", "tx-rx"],
        },
        "lldp-profile": {
            "type": "string",
            "help": "LLDP port TLV profile.",
            "default": "default-auto-isl",
            "max_length": 63,
        },
        "export-to": {
            "type": "string",
            "help": "Export managed-switch port to a tenant VDOM.",
            "default": "",
            "max_length": 31,
        },
        "mac-addr": {
            "type": "mac-address",
            "help": "Port/Trunk MAC.",
            "default": "00:00:00:00:00:00",
        },
        "allow-arp-monitor": {
            "type": "option",
            "help": "Enable/Disable allow ARP monitor.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "qnq": {
            "type": "string",
            "help": "802.1AD VLANs in the VDom.",
            "default": "",
            "max_length": 15,
        },
        "log-mac-event": {
            "type": "option",
            "help": "Enable/disable logging for dynamic MAC address events.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "port-selection-criteria": {
            "type": "option",
            "help": "Algorithm for aggregate port selection.",
            "default": "src-dst-ip",
            "options": ["src-mac", "dst-mac", "src-dst-mac", "src-ip", "dst-ip", "src-dst-ip"],
        },
        "description": {
            "type": "string",
            "help": "Description for port.",
            "default": "",
            "max_length": 63,
        },
        "lacp-speed": {
            "type": "option",
            "help": "End Link Aggregation Control Protocol (LACP) messages every 30 seconds (slow) or every second (fast).",
            "default": "slow",
            "options": ["slow", "fast"],
        },
        "mode": {
            "type": "option",
            "help": "LACP mode: ignore and do not send control messages, or negotiate 802.3ad aggregation passively or actively.",
            "default": "static",
            "options": ["static", "lacp-passive", "lacp-active"],
        },
        "bundle": {
            "type": "option",
            "help": "Enable/disable Link Aggregation Group (LAG) bundling for non-FortiLink interfaces.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "member-withdrawal-behavior": {
            "type": "option",
            "help": "Port behavior after it withdraws because of loss of control packets.",
            "default": "block",
            "options": ["forward", "block"],
        },
        "mclag": {
            "type": "option",
            "help": "Enable/disable multi-chassis link aggregation (MCLAG).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "min-bundle": {
            "type": "integer",
            "help": "Minimum size of LAG bundle (1 - 24, default = 1).",
            "default": 1,
            "min_value": 1,
            "max_value": 24,
        },
        "max-bundle": {
            "type": "integer",
            "help": "Maximum size of LAG bundle (1 - 24, default = 24).",
            "default": 24,
            "min_value": 1,
            "max_value": 24,
        },
        "members": {
            "type": "string",
            "help": "Aggregated LAG bundle interfaces.",
        },
        "fallback-port": {
            "type": "string",
            "help": "LACP fallback port.",
            "default": "",
            "max_length": 79,
        },
    },
    "ip-source-guard": {
        "port": {
            "type": "string",
            "help": "Ingress interface to which source guard is bound.",
            "default": "",
            "max_length": 15,
        },
        "description": {
            "type": "string",
            "help": "Description.",
            "default": "",
            "max_length": 63,
        },
        "binding-entry": {
            "type": "string",
            "help": "IP and MAC address configuration.",
            "required": True,
        },
    },
    "stp-settings": {
        "local-override": {
            "type": "option",
            "help": "Enable to configure local STP settings that override global STP settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "name": {
            "type": "string",
            "help": "Name of local STP settings configuration.",
            "default": "",
            "max_length": 31,
        },
        "revision": {
            "type": "integer",
            "help": "STP revision number (0 - 65535).",
            "default": 0,
            "min_value": 0,
            "max_value": 65535,
        },
        "hello-time": {
            "type": "integer",
            "help": "Period of time between successive STP frame Bridge Protocol Data Units (BPDUs) sent on a port (1 - 10 sec, default = 2).",
            "default": 2,
            "min_value": 1,
            "max_value": 10,
        },
        "forward-time": {
            "type": "integer",
            "help": "Period of time a port is in listening and learning state (4 - 30 sec, default = 15).",
            "default": 15,
            "min_value": 4,
            "max_value": 30,
        },
        "max-age": {
            "type": "integer",
            "help": "Maximum time before a bridge port saves its configuration BPDU information (6 - 40 sec, default = 20).",
            "default": 20,
            "min_value": 6,
            "max_value": 40,
        },
        "max-hops": {
            "type": "integer",
            "help": "Maximum number of hops between the root bridge and the furthest bridge (1- 40, default = 20).",
            "default": 20,
            "min_value": 1,
            "max_value": 40,
        },
        "pending-timer": {
            "type": "integer",
            "help": "Pending time (1 - 15 sec, default = 4).",
            "default": 4,
            "min_value": 1,
            "max_value": 15,
        },
    },
    "stp-instance": {
        "id": {
            "type": "string",
            "help": "Instance ID.",
            "default": "",
            "max_length": 2,
        },
        "priority": {
            "type": "option",
            "help": "Priority.",
            "default": "32768",
            "options": ["0", "4096", "8192", "12288", "16384", "20480", "24576", "28672", "32768", "36864", "40960", "45056", "49152", "53248", "57344", "61440"],
        },
    },
    "snmp-sysinfo": {
        "status": {
            "type": "option",
            "help": "Enable/disable SNMP.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "engine-id": {
            "type": "string",
            "help": "Local SNMP engine ID string (max 24 char).",
            "default": "",
            "max_length": 24,
        },
        "description": {
            "type": "string",
            "help": "System description.",
            "default": "",
            "max_length": 35,
        },
        "contact-info": {
            "type": "string",
            "help": "Contact information.",
            "default": "",
            "max_length": 35,
        },
        "location": {
            "type": "string",
            "help": "System location.",
            "default": "",
            "max_length": 35,
        },
    },
    "snmp-trap-threshold": {
        "trap-high-cpu-threshold": {
            "type": "integer",
            "help": "CPU usage when trap is sent.",
            "default": 80,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "trap-low-memory-threshold": {
            "type": "integer",
            "help": "Memory usage when trap is sent.",
            "default": 80,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "trap-log-full-threshold": {
            "type": "integer",
            "help": "Log disk usage when trap is sent.",
            "default": 90,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "snmp-community": {
        "id": {
            "type": "integer",
            "help": "SNMP community ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "name": {
            "type": "string",
            "help": "SNMP community name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this SNMP community.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "hosts": {
            "type": "string",
            "help": "Configure IPv4 SNMP managers (hosts).",
        },
        "query-v1-status": {
            "type": "option",
            "help": "Enable/disable SNMP v1 queries.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "query-v1-port": {
            "type": "integer",
            "help": "SNMP v1 query port (default = 161).",
            "default": 161,
            "min_value": 0,
            "max_value": 65535,
        },
        "query-v2c-status": {
            "type": "option",
            "help": "Enable/disable SNMP v2c queries.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "query-v2c-port": {
            "type": "integer",
            "help": "SNMP v2c query port (default = 161).",
            "default": 161,
            "min_value": 0,
            "max_value": 65535,
        },
        "trap-v1-status": {
            "type": "option",
            "help": "Enable/disable SNMP v1 traps.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "trap-v1-lport": {
            "type": "integer",
            "help": "SNMP v2c trap local port (default = 162).",
            "default": 162,
            "min_value": 0,
            "max_value": 65535,
        },
        "trap-v1-rport": {
            "type": "integer",
            "help": "SNMP v2c trap remote port (default = 162).",
            "default": 162,
            "min_value": 0,
            "max_value": 65535,
        },
        "trap-v2c-status": {
            "type": "option",
            "help": "Enable/disable SNMP v2c traps.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "trap-v2c-lport": {
            "type": "integer",
            "help": "SNMP v2c trap local port (default = 162).",
            "default": 162,
            "min_value": 0,
            "max_value": 65535,
        },
        "trap-v2c-rport": {
            "type": "integer",
            "help": "SNMP v2c trap remote port (default = 162).",
            "default": 162,
            "min_value": 0,
            "max_value": 65535,
        },
        "events": {
            "type": "option",
            "help": "SNMP notifications (traps) to send.",
            "default": "cpu-high mem-low log-full intf-ip ent-conf-change l2mac",
            "options": ["cpu-high", "mem-low", "log-full", "intf-ip", "ent-conf-change", "l2mac"],
        },
    },
    "snmp-user": {
        "name": {
            "type": "string",
            "help": "SNMP user name.",
            "default": "",
            "max_length": 32,
        },
        "queries": {
            "type": "option",
            "help": "Enable/disable SNMP queries for this user.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "query-port": {
            "type": "integer",
            "help": "SNMPv3 query port (default = 161).",
            "default": 161,
            "min_value": 0,
            "max_value": 65535,
        },
        "security-level": {
            "type": "option",
            "help": "Security level for message authentication and encryption.",
            "default": "no-auth-no-priv",
            "options": ["no-auth-no-priv", "auth-no-priv", "auth-priv"],
        },
        "auth-proto": {
            "type": "option",
            "help": "Authentication protocol.",
            "default": "sha256",
            "options": ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],
        },
        "auth-pwd": {
            "type": "password",
            "help": "Password for authentication protocol.",
            "required": True,
            "max_length": 128,
        },
        "priv-proto": {
            "type": "option",
            "help": "Privacy (encryption) protocol.",
            "default": "aes128",
            "options": ["aes128", "aes192", "aes192c", "aes256", "aes256c", "des"],
        },
        "priv-pwd": {
            "type": "password",
            "help": "Password for privacy (encryption) protocol.",
            "required": True,
            "max_length": 128,
        },
    },
    "switch-log": {
        "local-override": {
            "type": "option",
            "help": "Enable to configure local logging settings that override global logging settings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "status": {
            "type": "option",
            "help": "Enable/disable adding FortiSwitch logs to the FortiGate event log.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "severity": {
            "type": "option",
            "help": "Severity of FortiSwitch logs that are added to the FortiGate event log.",
            "default": "notification",
            "options": ["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"],
        },
    },
    "remote-log": {
        "name": {
            "type": "string",
            "help": "Remote log name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable logging by FortiSwitch device to a remote syslog server.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "server": {
            "type": "string",
            "help": "IPv4 address of the remote syslog server.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "port": {
            "type": "integer",
            "help": "Remote syslog server listening port.",
            "default": 514,
            "min_value": 0,
            "max_value": 65535,
        },
        "severity": {
            "type": "option",
            "help": "Severity of logs to be transferred to remote log server.",
            "default": "information",
            "options": ["emergency", "alert", "critical", "error", "warning", "notification", "information", "debug"],
        },
        "csv": {
            "type": "option",
            "help": "Enable/disable comma-separated value (CSV) strings.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "facility": {
            "type": "option",
            "help": "Facility to log to remote syslog server.",
            "default": "local7",
            "options": ["kernel", "user", "mail", "daemon", "auth", "syslog", "lpr", "news", "uucp", "cron", "authpriv", "ftp", "ntp", "audit", "alert", "clock", "local0", "local1", "local2", "local3", "local4", "local5", "local6", "local7"],
        },
    },
    "storm-control": {
        "local-override": {
            "type": "option",
            "help": "Enable to override global FortiSwitch storm control settings for this FortiSwitch.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "rate": {
            "type": "integer",
            "help": "Rate in packets per second at which storm control drops excess traffic(0-10000000, default=500, drop-all=0).",
            "default": 500,
            "min_value": 0,
            "max_value": 10000000,
        },
        "burst-size-level": {
            "type": "integer",
            "help": "Increase level to handle bursty traffic (0 - 4, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 4,
        },
        "unknown-unicast": {
            "type": "option",
            "help": "Enable/disable storm control to drop unknown unicast traffic.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "unknown-multicast": {
            "type": "option",
            "help": "Enable/disable storm control to drop unknown multicast traffic.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "broadcast": {
            "type": "option",
            "help": "Enable/disable storm control to drop broadcast traffic.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
    },
    "mirror": {
        "name": {
            "type": "string",
            "help": "Mirror name.",
            "default": "",
            "max_length": 63,
        },
        "status": {
            "type": "option",
            "help": "Active/inactive mirror configuration.",
            "default": "inactive",
            "options": ["active", "inactive"],
        },
        "switching-packet": {
            "type": "option",
            "help": "Enable/disable switching functionality when mirroring.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dst": {
            "type": "string",
            "help": "Destination port.",
            "default": "",
            "max_length": 63,
        },
        "src-ingress": {
            "type": "string",
            "help": "Source ingress interfaces.",
        },
        "src-egress": {
            "type": "string",
            "help": "Source egress interfaces.",
        },
    },
    "static-mac": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "type": {
            "type": "option",
            "help": "Type.",
            "default": "static",
            "options": ["static", "sticky"],
        },
        "vlan": {
            "type": "string",
            "help": "Vlan.",
            "default": "",
            "max_length": 15,
        },
        "mac": {
            "type": "mac-address",
            "help": "MAC address.",
            "default": "00:00:00:00:00:00",
        },
        "interface": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 35,
        },
        "description": {
            "type": "string",
            "help": "Description.",
            "default": "",
            "max_length": 63,
        },
    },
    "custom-command": {
        "command-entry": {
            "type": "string",
            "help": "List of FortiSwitch commands.",
            "default": "",
            "max_length": 35,
        },
        "command-name": {
            "type": "string",
            "help": "Names of commands to be pushed to this FortiSwitch device, as configured under config switch-controller custom-command.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
    "dhcp-snooping-static-client": {
        "name": {
            "type": "string",
            "help": "Client name.",
            "default": "",
            "max_length": 35,
        },
        "vlan": {
            "type": "string",
            "help": "VLAN name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "ip": {
            "type": "ipv4-address",
            "help": "Client static IP address.",
            "required": True,
            "default": "0.0.0.0",
        },
        "mac": {
            "type": "mac-address",
            "help": "Client MAC address.",
            "required": True,
            "default": "00:00:00:00:00:00",
        },
        "port": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
    },
    "igmp-snooping": {
        "local-override": {
            "type": "option",
            "help": "Enable/disable overriding the global IGMP snooping configuration.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "aging-time": {
            "type": "integer",
            "help": "Maximum time to retain a multicast snooping entry for which no packets have been seen (15 - 3600 sec, default = 300).",
            "default": 300,
            "min_value": 15,
            "max_value": 3600,
        },
        "flood-unknown-multicast": {
            "type": "option",
            "help": "Enable/disable unknown multicast flooding.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "vlans": {
            "type": "string",
            "help": "Configure IGMP snooping VLAN.",
        },
    },
    "802-1X-settings": {
        "local-override": {
            "type": "option",
            "help": "Enable to override global 802.1X settings on individual FortiSwitches.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "link-down-auth": {
            "type": "option",
            "help": "Authentication state to set if a link is down.",
            "default": "set-unauth",
            "options": ["set-unauth", "no-action"],
        },
        "reauth-period": {
            "type": "integer",
            "help": "Reauthentication time interval (1 - 1440 min, default = 60, 0 = disable).",
            "default": 60,
            "min_value": 0,
            "max_value": 1440,
        },
        "max-reauth-attempt": {
            "type": "integer",
            "help": "Maximum number of authentication attempts (0 - 15, default = 3).",
            "default": 3,
            "min_value": 0,
            "max_value": 15,
        },
        "tx-period": {
            "type": "integer",
            "help": "802.1X Tx period (seconds, default=30).",
            "default": 30,
            "min_value": 12,
            "max_value": 60,
        },
        "mab-reauth": {
            "type": "option",
            "help": "Enable or disable MAB reauthentication settings.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "mac-username-delimiter": {
            "type": "option",
            "help": "MAC authentication username delimiter (default = hyphen).",
            "default": "hyphen",
            "options": ["colon", "hyphen", "none", "single-hyphen"],
        },
        "mac-password-delimiter": {
            "type": "option",
            "help": "MAC authentication password delimiter (default = hyphen).",
            "default": "hyphen",
            "options": ["colon", "hyphen", "none", "single-hyphen"],
        },
        "mac-calling-station-delimiter": {
            "type": "option",
            "help": "MAC calling station delimiter (default = hyphen).",
            "default": "hyphen",
            "options": ["colon", "hyphen", "none", "single-hyphen"],
        },
        "mac-called-station-delimiter": {
            "type": "option",
            "help": "MAC called station delimiter (default = hyphen).",
            "default": "hyphen",
            "options": ["colon", "hyphen", "none", "single-hyphen"],
        },
        "mac-case": {
            "type": "option",
            "help": "MAC case (default = lowercase).",
            "default": "lowercase",
            "options": ["lowercase", "uppercase"],
        },
    },
    "router-vrf": {
        "name": {
            "type": "string",
            "help": "VRF entry name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "switch-id": {
            "type": "string",
            "help": "Switch ID.",
            "default": "",
            "max_length": 35,
        },
        "vrfid": {
            "type": "integer",
            "help": "VRF ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 1023,
        },
    },
    "system-interface": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 15,
        },
        "switch-id": {
            "type": "string",
            "help": "Switch ID.",
            "default": "",
            "max_length": 35,
        },
        "mode": {
            "type": "option",
            "help": "Interface addressing mode.",
            "default": "static",
            "options": ["static", "dhcp"],
        },
        "ip": {
            "type": "ipv4-classnet-host",
            "help": "IP and mask for this interface.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
        "status": {
            "type": "option",
            "help": "Enable/disable interface status.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "allowaccess": {
            "type": "option",
            "help": "Permitted types of management access to this interface.",
            "default": "",
            "options": ["ping", "https", "http", "ssh", "snmp", "telnet", "radius-acct"],
        },
        "vlan": {
            "type": "string",
            "help": "VLAN name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "type": {
            "type": "option",
            "help": "Interface type.",
            "default": "vlan",
            "options": ["vlan", "physical"],
        },
        "interface": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 63,
        },
        "vrf": {
            "type": "string",
            "help": "VRF for this route.",
            "default": "",
            "max_length": 63,
        },
    },
    "router-static": {
        "id": {
            "type": "integer",
            "help": "Entry sequence number.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "switch-id": {
            "type": "string",
            "help": "Switch ID.",
            "default": "",
            "max_length": 35,
        },
        "blackhole": {
            "type": "option",
            "help": "Enable/disable blackhole on this route.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "comment": {
            "type": "string",
            "help": "Comment.",
            "default": "",
            "max_length": 63,
        },
        "device": {
            "type": "string",
            "help": "Gateway out interface.",
            "default": "",
            "max_length": 35,
        },
        "distance": {
            "type": "integer",
            "help": "Administrative distance for the route (1 - 255, default = 10).",
            "default": 10,
            "min_value": 1,
            "max_value": 255,
        },
        "dst": {
            "type": "ipv4-classnet",
            "help": "Destination ip and mask for this route.",
            "required": True,
            "default": "0.0.0.0 0.0.0.0",
        },
        "dynamic-gateway": {
            "type": "option",
            "help": "Enable/disable dynamic gateway.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "gateway": {
            "type": "ipv4-address",
            "help": "Gateway ip for this route.",
            "required": True,
            "default": "0.0.0.0",
        },
        "status": {
            "type": "option",
            "help": "Enable/disable route status.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "vrf": {
            "type": "string",
            "help": "VRF for this route.",
            "default": "",
            "max_length": 35,
        },
    },
    "system-dhcp-server": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "switch-id": {
            "type": "string",
            "help": "Switch ID.",
            "default": "",
            "max_length": 35,
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this DHCP configuration.",
            "default": "enable",
            "options": ["disable", "enable"],
        },
        "lease-time": {
            "type": "integer",
            "help": "Lease time in seconds, 0 means unlimited.",
            "default": 604800,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "dns-service": {
            "type": "option",
            "help": "Options for assigning DNS servers to DHCP clients.",
            "default": "specify",
            "options": ["local", "default", "specify"],
        },
        "dns-server1": {
            "type": "ipv4-address",
            "help": "DNS server 1.",
            "default": "0.0.0.0",
        },
        "dns-server2": {
            "type": "ipv4-address",
            "help": "DNS server 2.",
            "default": "0.0.0.0",
        },
        "dns-server3": {
            "type": "ipv4-address",
            "help": "DNS server 3.",
            "default": "0.0.0.0",
        },
        "ntp-service": {
            "type": "option",
            "help": "Options for assigning Network Time Protocol (NTP) servers to DHCP clients.",
            "default": "specify",
            "options": ["local", "default", "specify"],
        },
        "ntp-server1": {
            "type": "ipv4-address",
            "help": "NTP server 1.",
            "default": "0.0.0.0",
        },
        "ntp-server2": {
            "type": "ipv4-address",
            "help": "NTP server 2.",
            "default": "0.0.0.0",
        },
        "ntp-server3": {
            "type": "ipv4-address",
            "help": "NTP server 3.",
            "default": "0.0.0.0",
        },
        "default-gateway": {
            "type": "ipv4-address",
            "help": "Default gateway IP address assigned by the DHCP server.",
            "default": "0.0.0.0",
        },
        "netmask": {
            "type": "ipv4-netmask",
            "help": "Netmask assigned by the DHCP server.",
            "required": True,
            "default": "0.0.0.0",
        },
        "interface": {
            "type": "string",
            "help": "DHCP server can assign IP configurations to clients connected to this interface.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "ip-range": {
            "type": "string",
            "help": "DHCP IP range configuration.",
        },
        "options": {
            "type": "string",
            "help": "DHCP options.",
        },
    },
}


# Valid enum values from API documentation
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
VALID_BODY_FSW_WAN1_ADMIN = [
    "discovered",
    "disable",
    "enable",
]
VALID_BODY_POE_PRE_STANDARD_DETECTION = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_SERVER_ACCESS_LIST = [
    "global",
    "enable",
    "disable",
]
VALID_BODY_MCLAG_IGMP_SNOOPING_AWARE = [
    "enable",
    "disable",
]
VALID_BODY_PTP_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_RADIUS_NAS_IP_OVERRIDE = [
    "disable",
    "enable",
]
VALID_BODY_ROUTE_OFFLOAD = [
    "disable",
    "enable",
]
VALID_BODY_ROUTE_OFFLOAD_MCLAG = [
    "disable",
    "enable",
]
VALID_BODY_TYPE = [
    "virtual",
    "physical",
]
VALID_BODY_FIRMWARE_PROVISION = [
    "enable",
    "disable",
]
VALID_BODY_FIRMWARE_PROVISION_LATEST = [
    "disable",
    "once",
]
VALID_BODY_OVERRIDE_SNMP_SYSINFO = [
    "disable",
    "enable",
]
VALID_BODY_OVERRIDE_SNMP_TRAP_THRESHOLD = [
    "enable",
    "disable",
]
VALID_BODY_OVERRIDE_SNMP_COMMUNITY = [
    "enable",
    "disable",
]
VALID_BODY_OVERRIDE_SNMP_USER = [
    "enable",
    "disable",
]
VALID_BODY_QOS_DROP_POLICY = [
    "taildrop",
    "random-early-detection",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_switch_controller_managed_switch_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for switch_controller/managed_switch."""
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


def validate_switch_controller_managed_switch_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new switch_controller/managed_switch object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "purdue-level" in payload:
        is_valid, error = _validate_enum_field(
            "purdue-level",
            payload["purdue-level"],
            VALID_BODY_PURDUE_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fsw-wan1-admin" in payload:
        is_valid, error = _validate_enum_field(
            "fsw-wan1-admin",
            payload["fsw-wan1-admin"],
            VALID_BODY_FSW_WAN1_ADMIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "poe-pre-standard-detection" in payload:
        is_valid, error = _validate_enum_field(
            "poe-pre-standard-detection",
            payload["poe-pre-standard-detection"],
            VALID_BODY_POE_PRE_STANDARD_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-server-access-list" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-server-access-list",
            payload["dhcp-server-access-list"],
            VALID_BODY_DHCP_SERVER_ACCESS_LIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mclag-igmp-snooping-aware" in payload:
        is_valid, error = _validate_enum_field(
            "mclag-igmp-snooping-aware",
            payload["mclag-igmp-snooping-aware"],
            VALID_BODY_MCLAG_IGMP_SNOOPING_AWARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ptp-status" in payload:
        is_valid, error = _validate_enum_field(
            "ptp-status",
            payload["ptp-status"],
            VALID_BODY_PTP_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-nas-ip-override" in payload:
        is_valid, error = _validate_enum_field(
            "radius-nas-ip-override",
            payload["radius-nas-ip-override"],
            VALID_BODY_RADIUS_NAS_IP_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "route-offload" in payload:
        is_valid, error = _validate_enum_field(
            "route-offload",
            payload["route-offload"],
            VALID_BODY_ROUTE_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "route-offload-mclag" in payload:
        is_valid, error = _validate_enum_field(
            "route-offload-mclag",
            payload["route-offload-mclag"],
            VALID_BODY_ROUTE_OFFLOAD_MCLAG,
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
    if "firmware-provision" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision",
            payload["firmware-provision"],
            VALID_BODY_FIRMWARE_PROVISION,
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
    if "override-snmp-sysinfo" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-sysinfo",
            payload["override-snmp-sysinfo"],
            VALID_BODY_OVERRIDE_SNMP_SYSINFO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-snmp-trap-threshold" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-trap-threshold",
            payload["override-snmp-trap-threshold"],
            VALID_BODY_OVERRIDE_SNMP_TRAP_THRESHOLD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-snmp-community" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-community",
            payload["override-snmp-community"],
            VALID_BODY_OVERRIDE_SNMP_COMMUNITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-snmp-user" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-user",
            payload["override-snmp-user"],
            VALID_BODY_OVERRIDE_SNMP_USER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "qos-drop-policy" in payload:
        is_valid, error = _validate_enum_field(
            "qos-drop-policy",
            payload["qos-drop-policy"],
            VALID_BODY_QOS_DROP_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_switch_controller_managed_switch_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update switch_controller/managed_switch."""
    # Validate enum values using central function
    if "purdue-level" in payload:
        is_valid, error = _validate_enum_field(
            "purdue-level",
            payload["purdue-level"],
            VALID_BODY_PURDUE_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fsw-wan1-admin" in payload:
        is_valid, error = _validate_enum_field(
            "fsw-wan1-admin",
            payload["fsw-wan1-admin"],
            VALID_BODY_FSW_WAN1_ADMIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "poe-pre-standard-detection" in payload:
        is_valid, error = _validate_enum_field(
            "poe-pre-standard-detection",
            payload["poe-pre-standard-detection"],
            VALID_BODY_POE_PRE_STANDARD_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-server-access-list" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-server-access-list",
            payload["dhcp-server-access-list"],
            VALID_BODY_DHCP_SERVER_ACCESS_LIST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mclag-igmp-snooping-aware" in payload:
        is_valid, error = _validate_enum_field(
            "mclag-igmp-snooping-aware",
            payload["mclag-igmp-snooping-aware"],
            VALID_BODY_MCLAG_IGMP_SNOOPING_AWARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ptp-status" in payload:
        is_valid, error = _validate_enum_field(
            "ptp-status",
            payload["ptp-status"],
            VALID_BODY_PTP_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-nas-ip-override" in payload:
        is_valid, error = _validate_enum_field(
            "radius-nas-ip-override",
            payload["radius-nas-ip-override"],
            VALID_BODY_RADIUS_NAS_IP_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "route-offload" in payload:
        is_valid, error = _validate_enum_field(
            "route-offload",
            payload["route-offload"],
            VALID_BODY_ROUTE_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "route-offload-mclag" in payload:
        is_valid, error = _validate_enum_field(
            "route-offload-mclag",
            payload["route-offload-mclag"],
            VALID_BODY_ROUTE_OFFLOAD_MCLAG,
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
    if "firmware-provision" in payload:
        is_valid, error = _validate_enum_field(
            "firmware-provision",
            payload["firmware-provision"],
            VALID_BODY_FIRMWARE_PROVISION,
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
    if "override-snmp-sysinfo" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-sysinfo",
            payload["override-snmp-sysinfo"],
            VALID_BODY_OVERRIDE_SNMP_SYSINFO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-snmp-trap-threshold" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-trap-threshold",
            payload["override-snmp-trap-threshold"],
            VALID_BODY_OVERRIDE_SNMP_TRAP_THRESHOLD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-snmp-community" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-community",
            payload["override-snmp-community"],
            VALID_BODY_OVERRIDE_SNMP_COMMUNITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override-snmp-user" in payload:
        is_valid, error = _validate_enum_field(
            "override-snmp-user",
            payload["override-snmp-user"],
            VALID_BODY_OVERRIDE_SNMP_USER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "qos-drop-policy" in payload:
        is_valid, error = _validate_enum_field(
            "qos-drop-policy",
            payload["qos-drop-policy"],
            VALID_BODY_QOS_DROP_POLICY,
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
    "endpoint": "switch_controller/managed_switch",
    "category": "cmdb",
    "api_path": "switch-controller/managed-switch",
    "mkey": "switch-id",
    "mkey_type": "string",
    "help": "Configure FortiSwitch devices that are managed by this FortiGate.",
    "total_fields": 68,
    "required_fields_count": 3,
    "fields_with_defaults_count": 45,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
