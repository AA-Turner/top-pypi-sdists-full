"""Validation helpers for system/interface - Auto-generated"""

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
    "vdom",  # Interface is in this virtual domain (VDOM).
    "dhcp-relay-interface",  # Specify outgoing interface to reach server.
    "interface",  # Interface name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "vdom": "",
    "vrf": 0,
    "cli-conn-status": 0,
    "fortilink": "disable",
    "switch-controller-source-ip": "outbound",
    "mode": "static",
    "distance": 5,
    "priority": 1,
    "dhcp-relay-interface-select-method": "auto",
    "dhcp-relay-interface": "",
    "dhcp-relay-vrf-select": -1,
    "dhcp-broadcast-flag": "enable",
    "dhcp-relay-service": "disable",
    "dhcp-relay-ip": "",
    "dhcp-relay-source-ip": "0.0.0.0",
    "dhcp-relay-circuit-id": "",
    "dhcp-relay-link-selection": "0.0.0.0",
    "dhcp-relay-request-all-server": "disable",
    "dhcp-relay-allow-no-end-option": "disable",
    "dhcp-relay-type": "regular",
    "dhcp-smart-relay": "disable",
    "dhcp-relay-agent-option": "enable",
    "dhcp-classless-route-addition": "enable",
    "management-ip": "0.0.0.0 0.0.0.0",
    "ip": "0.0.0.0 0.0.0.0",
    "allowaccess": "",
    "gwdetect": "disable",
    "ping-serv-status": 0,
    "detectserver": "",
    "detectprotocol": "ping",
    "ha-priority": 1,
    "fail-detect": "disable",
    "fail-detect-option": "link-down",
    "fail-alert-method": "link-down",
    "fail-action-on-extender": "soft-restart",
    "dhcp-client-identifier": "",
    "dhcp-renew-time": 0,
    "ipunnumbered": "0.0.0.0",
    "username": "",
    "pppoe-egress-cos": "cos0",
    "pppoe-unnumbered-negotiate": "enable",
    "idle-timeout": 0,
    "multilink": "disable",
    "mrru": 1500,
    "detected-peer-mtu": 0,
    "disc-retry-timeout": 1,
    "padt-retry-timeout": 1,
    "service-name": "",
    "ac-name": "",
    "lcp-echo-interval": 5,
    "lcp-max-echo-fails": 3,
    "defaultgw": "enable",
    "dns-server-override": "enable",
    "dns-server-protocol": "cleartext",
    "auth-type": "auto",
    "pptp-client": "disable",
    "pptp-user": "",
    "pptp-server-ip": "0.0.0.0",
    "pptp-auth-type": "auto",
    "pptp-timeout": 0,
    "arpforward": "enable",
    "ndiscforward": "enable",
    "broadcast-forward": "disable",
    "bfd": "global",
    "bfd-desired-min-tx": 250,
    "bfd-detect-mult": 3,
    "bfd-required-min-rx": 250,
    "l2forward": "disable",
    "icmp-send-redirect": "enable",
    "icmp-accept-redirect": "enable",
    "reachable-time": 30000,
    "vlanforward": "disable",
    "stpforward": "disable",
    "stpforward-mode": "rpl-all-ext-id",
    "ips-sniffer-mode": "disable",
    "ident-accept": "disable",
    "ipmac": "disable",
    "subst": "disable",
    "macaddr": "00:00:00:00:00:00",
    "virtual-mac": "00:00:00:00:00:00",
    "substitute-dst-mac": "00:00:00:00:00:00",
    "speed": "auto",
    "status": "up",
    "netbios-forward": "disable",
    "wins-ip": "0.0.0.0",
    "type": "vlan",
    "dedicated-to": "none",
    "trust-ip-1": "0.0.0.0 0.0.0.0",
    "trust-ip-2": "0.0.0.0 0.0.0.0",
    "trust-ip-3": "0.0.0.0 0.0.0.0",
    "trust-ip6-1": "::/0",
    "trust-ip6-2": "::/0",
    "trust-ip6-3": "::/0",
    "ring-rx": 0,
    "ring-tx": 0,
    "wccp": "disable",
    "netflow-sampler": "disable",
    "netflow-sample-rate": 1,
    "netflow-sampler-id": 0,
    "sflow-sampler": "disable",
    "drop-fragment": "disable",
    "src-check": "enable",
    "sample-rate": 2000,
    "polling-interval": 20,
    "sample-direction": "both",
    "explicit-web-proxy": "disable",
    "explicit-ftp-proxy": "disable",
    "proxy-captive-portal": "disable",
    "tcp-mss": 0,
    "inbandwidth": 0,
    "outbandwidth": 0,
    "egress-shaping-profile": "",
    "ingress-shaping-profile": "",
    "spillover-threshold": 0,
    "ingress-spillover-threshold": 0,
    "weight": 0,
    "interface": "",
    "external": "disable",
    "mtu-override": "disable",
    "mtu": 1500,
    "vlan-protocol": "8021q",
    "vlanid": 0,
    "forward-domain": 0,
    "remote-ip": "0.0.0.0 0.0.0.0",
    "lacp-mode": "active",
    "lacp-ha-secondary": "enable",
    "system-id-type": "auto",
    "system-id": "00:00:00:00:00:00",
    "lacp-speed": "slow",
    "min-links": 1,
    "min-links-down": "operational",
    "algorithm": "L4",
    "link-up-delay": 50,
    "aggregate-type": "physical",
    "priority-override": "enable",
    "aggregate": "",
    "redundant-interface": "",
    "devindex": 0,
    "vindex": 0,
    "switch": "",
    "alias": "",
    "security-mode": "none",
    "security-mac-auth-bypass": "disable",
    "security-ip-auth-bypass": "disable",
    "security-external-logout": "",
    "replacemsg-override-group": "",
    "auth-cert": "",
    "auth-portal-addr": "",
    "security-exempt-list": "",
    "ike-saml-server": "",
    "device-identification": "disable",
    "exclude-signatures": "",
    "device-user-identification": "enable",
    "lldp-reception": "vdom",
    "lldp-transmission": "vdom",
    "lldp-network-policy": "",
    "estimated-upstream-bandwidth": 0,
    "estimated-downstream-bandwidth": 0,
    "measured-upstream-bandwidth": 0,
    "measured-downstream-bandwidth": 0,
    "bandwidth-measure-time": 0,
    "monitor-bandwidth": "disable",
    "vrrp-virtual-mac": "disable",
    "role": "undefined",
    "snmp-index": 0,
    "secondary-IP": "disable",
    "preserve-session-route": "disable",
    "auto-auth-extension-device": "disable",
    "ap-discover": "enable",
    "fortilink-neighbor-detect": "lldp",
    "ip-managed-by-fortiipam": "inherit-global",
    "managed-subnetwork-size": "256",
    "fortilink-split-interface": "enable",
    "internal": 0,
    "fortilink-backup-link": 0,
    "switch-controller-access-vlan": "disable",
    "switch-controller-traffic-policy": "",
    "switch-controller-rspan-mode": "disable",
    "switch-controller-netflow-collect": "disable",
    "switch-controller-mgmt-vlan": 4094,
    "switch-controller-igmp-snooping": "disable",
    "switch-controller-igmp-snooping-proxy": "disable",
    "switch-controller-igmp-snooping-fast-leave": "disable",
    "switch-controller-dhcp-snooping": "disable",
    "switch-controller-dhcp-snooping-verify-mac": "disable",
    "switch-controller-dhcp-snooping-option82": "disable",
    "switch-controller-arp-inspection": "disable",
    "switch-controller-learning-limit": 0,
    "switch-controller-nac": "",
    "switch-controller-dynamic": "",
    "switch-controller-feature": "none",
    "switch-controller-iot-scanning": "disable",
    "switch-controller-offload": "disable",
    "switch-controller-offload-ip": "0.0.0.0",
    "switch-controller-offload-gw": "disable",
    "swc-vlan": 0,
    "swc-first-create": 0,
    "color": 0,
    "eap-supplicant": "disable",
    "eap-method": "",
    "eap-identity": "",
    "eap-ca-cert": "",
    "eap-user-cert": "",
    "default-purdue-level": "3",
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
    "name": "string",  # Name.
    "vdom": "string",  # Interface is in this virtual domain (VDOM).
    "vrf": "integer",  # Virtual Routing Forwarding ID.
    "cli-conn-status": "integer",  # CLI connection status.
    "fortilink": "option",  # Enable FortiLink to dedicate this interface to manage other 
    "switch-controller-source-ip": "option",  # Source IP address used in FortiLink over L3 connections.
    "mode": "option",  # Addressing mode (static, DHCP, PPPoE).
    "client-options": "string",  # DHCP client options.
    "distance": "integer",  # Distance for routes learned through PPPoE or DHCP, lower dis
    "priority": "integer",  # Priority of learned routes.
    "dhcp-relay-interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "dhcp-relay-interface": "string",  # Specify outgoing interface to reach server.
    "dhcp-relay-vrf-select": "integer",  # VRF ID used for connection to server.
    "dhcp-broadcast-flag": "option",  # Enable/disable setting of the broadcast flag in messages sen
    "dhcp-relay-service": "option",  # Enable/disable allowing this interface to act as a DHCP rela
    "dhcp-relay-ip": "user",  # DHCP relay IP address.
    "dhcp-relay-source-ip": "ipv4-address",  # IP address used by the DHCP relay as its source IP.
    "dhcp-relay-circuit-id": "string",  # DHCP relay circuit ID.
    "dhcp-relay-link-selection": "ipv4-address",  # DHCP relay link selection.
    "dhcp-relay-request-all-server": "option",  # Enable/disable sending of DHCP requests to all servers.
    "dhcp-relay-allow-no-end-option": "option",  # Enable/disable relaying DHCP messages with no end option.
    "dhcp-relay-type": "option",  # DHCP relay type (regular or IPsec).
    "dhcp-smart-relay": "option",  # Enable/disable DHCP smart relay.
    "dhcp-relay-agent-option": "option",  # Enable/disable DHCP relay agent option.
    "dhcp-classless-route-addition": "option",  # Enable/disable addition of classless static routes retrieved
    "management-ip": "ipv4-classnet-host",  # High Availability in-band management IP address of this inte
    "ip": "ipv4-classnet-host",  # Interface IPv4 address and subnet mask, syntax: X.X.X.X/24.
    "allowaccess": "option",  # Permitted types of management access to this interface.
    "gwdetect": "option",  # Enable/disable detect gateway alive for first.
    "ping-serv-status": "integer",  # PING server status.
    "detectserver": "user",  # Gateway's ping server for this IP.
    "detectprotocol": "option",  # Protocols used to detect the server.
    "ha-priority": "integer",  # HA election priority for the PING server.
    "fail-detect": "option",  # Enable/disable fail detection features for this interface.
    "fail-detect-option": "option",  # Options for detecting that this interface has failed.
    "fail-alert-method": "option",  # Select link-failed-signal or link-down method to alert about
    "fail-action-on-extender": "option",  # Action on FortiExtender when interface fail.
    "fail-alert-interfaces": "string",  # Names of the FortiGate interfaces to which the link failure 
    "dhcp-client-identifier": "string",  # DHCP client identifier.
    "dhcp-renew-time": "integer",  # DHCP renew time in seconds (300-604800), 0 means use the ren
    "ipunnumbered": "ipv4-address",  # Unnumbered IP used for PPPoE interfaces for which no unique 
    "username": "string",  # Username of the PPPoE account, provided by your ISP.
    "pppoe-egress-cos": "option",  # CoS in VLAN tag for outgoing PPPoE/PPP packets.
    "pppoe-unnumbered-negotiate": "option",  # Enable/disable PPPoE unnumbered negotiation.
    "password": "password",  # PPPoE account's password.
    "idle-timeout": "integer",  # PPPoE auto disconnect after idle timeout seconds, 0 means no
    "multilink": "option",  # Enable/disable PPP multilink support.
    "mrru": "integer",  # PPP MRRU (296 - 65535, default = 1500).
    "detected-peer-mtu": "integer",  # MTU of detected peer (0 - 4294967295).
    "disc-retry-timeout": "integer",  # Time in seconds to wait before retrying to start a PPPoE dis
    "padt-retry-timeout": "integer",  # PPPoE Active Discovery Terminate (PADT) used to terminate se
    "service-name": "string",  # PPPoE service name.
    "ac-name": "string",  # PPPoE server name.
    "lcp-echo-interval": "integer",  # Time in seconds between PPPoE Link Control Protocol (LCP) ec
    "lcp-max-echo-fails": "integer",  # Maximum missed LCP echo messages before disconnect.
    "defaultgw": "option",  # Enable to get the gateway IP from the DHCP or PPPoE server.
    "dns-server-override": "option",  # Enable/disable use DNS acquired by DHCP or PPPoE.
    "dns-server-protocol": "option",  # DNS transport protocols.
    "auth-type": "option",  # PPP authentication type to use.
    "pptp-client": "option",  # Enable/disable PPTP client.
    "pptp-user": "string",  # PPTP user name.
    "pptp-password": "password",  # PPTP password.
    "pptp-server-ip": "ipv4-address",  # PPTP server IP address.
    "pptp-auth-type": "option",  # PPTP authentication type.
    "pptp-timeout": "integer",  # Idle timer in minutes (0 for disabled).
    "arpforward": "option",  # Enable/disable ARP forwarding.
    "ndiscforward": "option",  # Enable/disable NDISC forwarding.
    "broadcast-forward": "option",  # Enable/disable broadcast forwarding.
    "bfd": "option",  # Bidirectional Forwarding Detection (BFD) settings.
    "bfd-desired-min-tx": "integer",  # BFD desired minimal transmit interval.
    "bfd-detect-mult": "integer",  # BFD detection multiplier.
    "bfd-required-min-rx": "integer",  # BFD required minimal receive interval.
    "l2forward": "option",  # Enable/disable l2 forwarding.
    "icmp-send-redirect": "option",  # Enable/disable sending of ICMP redirects.
    "icmp-accept-redirect": "option",  # Enable/disable ICMP accept redirect.
    "reachable-time": "integer",  # IPv4 reachable time in milliseconds (30000 - 3600000, defaul
    "vlanforward": "option",  # Enable/disable traffic forwarding between VLANs on this inte
    "stpforward": "option",  # Enable/disable STP forwarding.
    "stpforward-mode": "option",  # Configure STP forwarding mode.
    "ips-sniffer-mode": "option",  # Enable/disable the use of this interface as a one-armed snif
    "ident-accept": "option",  # Enable/disable authentication for this interface.
    "ipmac": "option",  # Enable/disable IP/MAC binding.
    "subst": "option",  # Enable to always send packets from this interface to a desti
    "macaddr": "mac-address",  # Change the interface's MAC address.
    "virtual-mac": "mac-address",  # Change the interface's virtual MAC address.
    "substitute-dst-mac": "mac-address",  # Destination MAC address that all packets are sent to from th
    "speed": "option",  # Interface speed. The default setting and the options availab
    "status": "option",  # Bring the interface up or shut the interface down.
    "netbios-forward": "option",  # Enable/disable NETBIOS forwarding.
    "wins-ip": "ipv4-address",  # WINS server IP.
    "type": "option",  # Interface type.
    "dedicated-to": "option",  # Configure interface for single purpose.
    "trust-ip-1": "ipv4-classnet-any",  # Trusted host for dedicated management traffic (0.0.0.0/24 fo
    "trust-ip-2": "ipv4-classnet-any",  # Trusted host for dedicated management traffic (0.0.0.0/24 fo
    "trust-ip-3": "ipv4-classnet-any",  # Trusted host for dedicated management traffic (0.0.0.0/24 fo
    "trust-ip6-1": "ipv6-prefix",  # Trusted IPv6 host for dedicated management traffic (::/0 for
    "trust-ip6-2": "ipv6-prefix",  # Trusted IPv6 host for dedicated management traffic (::/0 for
    "trust-ip6-3": "ipv6-prefix",  # Trusted IPv6 host for dedicated management traffic (::/0 for
    "ring-rx": "integer",  # RX ring size.
    "ring-tx": "integer",  # TX ring size.
    "wccp": "option",  # Enable/disable WCCP on this interface. Used for encapsulated
    "netflow-sampler": "option",  # Enable/disable NetFlow on this interface and set the data th
    "netflow-sample-rate": "integer",  # NetFlow sample rate.  Sample one packet every configured num
    "netflow-sampler-id": "integer",  # Netflow sampler ID.
    "sflow-sampler": "option",  # Enable/disable sFlow on this interface.
    "drop-fragment": "option",  # Enable/disable drop fragment packets.
    "src-check": "option",  # Enable/disable source IP check.
    "sample-rate": "integer",  # sFlow sample rate (10 - 99999).
    "polling-interval": "integer",  # sFlow polling interval in seconds (1 - 255).
    "sample-direction": "option",  # Data that NetFlow collects (rx, tx, or both).
    "explicit-web-proxy": "option",  # Enable/disable the explicit web proxy on this interface.
    "explicit-ftp-proxy": "option",  # Enable/disable the explicit FTP proxy on this interface.
    "proxy-captive-portal": "option",  # Enable/disable proxy captive portal on this interface.
    "tcp-mss": "integer",  # TCP maximum segment size. 0 means do not change segment size
    "inbandwidth": "integer",  # Bandwidth limit for incoming traffic (0 - 80000000 kbps), 0 
    "outbandwidth": "integer",  # Bandwidth limit for outgoing traffic (0 - 80000000 kbps).
    "egress-shaping-profile": "string",  # Outgoing traffic shaping profile.
    "ingress-shaping-profile": "string",  # Incoming traffic shaping profile.
    "spillover-threshold": "integer",  # Egress Spillover threshold (0 - 16776000 kbps), 0 means unli
    "ingress-spillover-threshold": "integer",  # Ingress Spillover threshold (0 - 16776000 kbps), 0 means unl
    "weight": "integer",  # Default weight for static routes (if route has no weight con
    "interface": "string",  # Interface name.
    "external": "option",  # Enable/disable identifying the interface as an external inte
    "mtu-override": "option",  # Enable to set a custom MTU for this interface.
    "mtu": "integer",  # MTU value for this interface.
    "vlan-protocol": "option",  # Ethernet protocol of VLAN.
    "vlanid": "integer",  # VLAN ID (1 - 4094).
    "forward-domain": "integer",  # Transparent mode forward domain.
    "remote-ip": "ipv4-classnet-host",  # Remote IP address of tunnel.
    "member": "string",  # Physical interfaces that belong to the aggregate or redundan
    "lacp-mode": "option",  # LACP mode.
    "lacp-ha-secondary": "option",  # LACP HA secondary member.
    "system-id-type": "option",  # Method in which system ID is generated.
    "system-id": "mac-address",  # Define a system ID for the aggregate interface.
    "lacp-speed": "option",  # How often the interface sends LACP messages.
    "min-links": "integer",  # Minimum number of aggregated ports that must be up.
    "min-links-down": "option",  # Action to take when less than the configured minimum number 
    "algorithm": "option",  # Frame distribution algorithm.
    "link-up-delay": "integer",  # Number of milliseconds to wait before considering a link is 
    "aggregate-type": "option",  # Type of aggregation.
    "priority-override": "option",  # Enable/disable fail back to higher priority port once recove
    "aggregate": "string",  # Aggregate interface.
    "redundant-interface": "string",  # Redundant interface.
    "devindex": "integer",  # Device Index.
    "vindex": "integer",  # Switch control interface VLAN ID.
    "switch": "string",  # Contained in switch.
    "description": "var-string",  # Description.
    "alias": "string",  # Alias will be displayed with the interface name to make it e
    "security-mode": "option",  # Turn on captive portal authentication for this interface.
    "security-mac-auth-bypass": "option",  # Enable/disable MAC authentication bypass.
    "security-ip-auth-bypass": "option",  # Enable/disable IP authentication bypass.
    "security-external-web": "var-string",  # URL of external authentication web server.
    "security-external-logout": "string",  # URL of external authentication logout server.
    "replacemsg-override-group": "string",  # Replacement message override group.
    "security-redirect-url": "var-string",  # URL redirection after disclaimer/authentication.
    "auth-cert": "string",  # HTTPS server certificate.
    "auth-portal-addr": "string",  # Address of captive portal.
    "security-exempt-list": "string",  # Name of security-exempt-list.
    "security-groups": "string",  # User groups that can authenticate with the captive portal.
    "ike-saml-server": "string",  # Configure IKE authentication SAML server.
    "device-identification": "option",  # Enable/disable passively gathering of device identity inform
    "exclude-signatures": "option",  # Exclude IOT or OT application signatures.
    "device-user-identification": "option",  # Enable/disable passive gathering of user identity informatio
    "lldp-reception": "option",  # Enable/disable Link Layer Discovery Protocol (LLDP) receptio
    "lldp-transmission": "option",  # Enable/disable Link Layer Discovery Protocol (LLDP) transmis
    "lldp-network-policy": "string",  # LLDP-MED network policy profile.
    "estimated-upstream-bandwidth": "integer",  # Estimated maximum upstream bandwidth (kbps). Used to estimat
    "estimated-downstream-bandwidth": "integer",  # Estimated maximum downstream bandwidth (kbps). Used to estim
    "measured-upstream-bandwidth": "integer",  # Measured upstream bandwidth (kbps).
    "measured-downstream-bandwidth": "integer",  # Measured downstream bandwidth (kbps).
    "bandwidth-measure-time": "integer",  # Bandwidth measure time.
    "monitor-bandwidth": "option",  # Enable monitoring bandwidth on this interface.
    "vrrp-virtual-mac": "option",  # Enable/disable use of virtual MAC for VRRP.
    "vrrp": "string",  # VRRP configuration.
    "phy-setting": "string",  # PHY settings
    "role": "option",  # Interface role.
    "snmp-index": "integer",  # Permanent SNMP Index of the interface.
    "secondary-IP": "option",  # Enable/disable adding a secondary IP to this interface.
    "secondaryip": "string",  # Second IP address of interface.
    "preserve-session-route": "option",  # Enable/disable preservation of session route when dirty.
    "auto-auth-extension-device": "option",  # Enable/disable automatic authorization of dedicated Fortinet
    "ap-discover": "option",  # Enable/disable automatic registration of unknown FortiAP dev
    "fortilink-neighbor-detect": "option",  # Protocol for FortiGate neighbor discovery.
    "ip-managed-by-fortiipam": "option",  # Enable/disable automatic IP address assignment of this inter
    "managed-subnetwork-size": "option",  # Number of IP addresses to be allocated by FortiIPAM and used
    "fortilink-split-interface": "option",  # Enable/disable FortiLink split interface to connect member l
    "internal": "integer",  # Implicitly created.
    "fortilink-backup-link": "integer",  # FortiLink split interface backup link.
    "switch-controller-access-vlan": "option",  # Block FortiSwitch port-to-port traffic.
    "switch-controller-traffic-policy": "string",  # Switch controller traffic policy for the VLAN.
    "switch-controller-rspan-mode": "option",  # Stop Layer2 MAC learning and interception of BPDUs and other
    "switch-controller-netflow-collect": "option",  # NetFlow collection and processing.
    "switch-controller-mgmt-vlan": "integer",  # VLAN to use for FortiLink management purposes.
    "switch-controller-igmp-snooping": "option",  # Switch controller IGMP snooping.
    "switch-controller-igmp-snooping-proxy": "option",  # Switch controller IGMP snooping proxy.
    "switch-controller-igmp-snooping-fast-leave": "option",  # Switch controller IGMP snooping fast-leave.
    "switch-controller-dhcp-snooping": "option",  # Switch controller DHCP snooping.
    "switch-controller-dhcp-snooping-verify-mac": "option",  # Switch controller DHCP snooping verify MAC.
    "switch-controller-dhcp-snooping-option82": "option",  # Switch controller DHCP snooping option82.
    "dhcp-snooping-server-list": "string",  # Configure DHCP server access list.
    "switch-controller-arp-inspection": "option",  # Enable/disable/Monitor FortiSwitch ARP inspection.
    "switch-controller-learning-limit": "integer",  # Limit the number of dynamic MAC addresses on this VLAN (1 - 
    "switch-controller-nac": "string",  # Integrated FortiLink settings for managed FortiSwitch.
    "switch-controller-dynamic": "string",  # Integrated FortiLink settings for managed FortiSwitch.
    "switch-controller-feature": "option",  # Interface's purpose when assigning traffic (read only).
    "switch-controller-iot-scanning": "option",  # Enable/disable managed FortiSwitch IoT scanning.
    "switch-controller-offload": "option",  # Enable/disable managed FortiSwitch routing offload.
    "switch-controller-offload-ip": "ipv4-address",  # IP for routing offload on FortiSwitch.
    "switch-controller-offload-gw": "option",  # Enable/disable managed FortiSwitch routing offload gateway.
    "swc-vlan": "integer",  # Creation status for switch-controller VLANs.
    "swc-first-create": "integer",  # Initial create for switch-controller VLANs.
    "color": "integer",  # Color of icon on the GUI.
    "tagging": "string",  # Config object tagging.
    "eap-supplicant": "option",  # Enable/disable EAP-Supplicant.
    "eap-method": "option",  # EAP method.
    "eap-identity": "string",  # EAP identity.
    "eap-password": "password",  # EAP password.
    "eap-ca-cert": "string",  # EAP CA certificate name.
    "eap-user-cert": "string",  # EAP user certificate name.
    "default-purdue-level": "option",  # default purdue level of device detected on this interface.
    "ipv6": "string",  # IPv6 of interface.
    "physical": "key",  # Print physical interface information.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Name.",
    "vdom": "Interface is in this virtual domain (VDOM).",
    "vrf": "Virtual Routing Forwarding ID.",
    "cli-conn-status": "CLI connection status.",
    "fortilink": "Enable FortiLink to dedicate this interface to manage other Fortinet devices.",
    "switch-controller-source-ip": "Source IP address used in FortiLink over L3 connections.",
    "mode": "Addressing mode (static, DHCP, PPPoE).",
    "client-options": "DHCP client options.",
    "distance": "Distance for routes learned through PPPoE or DHCP, lower distance indicates preferred route.",
    "priority": "Priority of learned routes.",
    "dhcp-relay-interface-select-method": "Specify how to select outgoing interface to reach server.",
    "dhcp-relay-interface": "Specify outgoing interface to reach server.",
    "dhcp-relay-vrf-select": "VRF ID used for connection to server.",
    "dhcp-broadcast-flag": "Enable/disable setting of the broadcast flag in messages sent by the DHCP client (default = enable).",
    "dhcp-relay-service": "Enable/disable allowing this interface to act as a DHCP relay.",
    "dhcp-relay-ip": "DHCP relay IP address.",
    "dhcp-relay-source-ip": "IP address used by the DHCP relay as its source IP.",
    "dhcp-relay-circuit-id": "DHCP relay circuit ID.",
    "dhcp-relay-link-selection": "DHCP relay link selection.",
    "dhcp-relay-request-all-server": "Enable/disable sending of DHCP requests to all servers.",
    "dhcp-relay-allow-no-end-option": "Enable/disable relaying DHCP messages with no end option.",
    "dhcp-relay-type": "DHCP relay type (regular or IPsec).",
    "dhcp-smart-relay": "Enable/disable DHCP smart relay.",
    "dhcp-relay-agent-option": "Enable/disable DHCP relay agent option.",
    "dhcp-classless-route-addition": "Enable/disable addition of classless static routes retrieved from DHCP server.",
    "management-ip": "High Availability in-band management IP address of this interface.",
    "ip": "Interface IPv4 address and subnet mask, syntax: X.X.X.X/24.",
    "allowaccess": "Permitted types of management access to this interface.",
    "gwdetect": "Enable/disable detect gateway alive for first.",
    "ping-serv-status": "PING server status.",
    "detectserver": "Gateway's ping server for this IP.",
    "detectprotocol": "Protocols used to detect the server.",
    "ha-priority": "HA election priority for the PING server.",
    "fail-detect": "Enable/disable fail detection features for this interface.",
    "fail-detect-option": "Options for detecting that this interface has failed.",
    "fail-alert-method": "Select link-failed-signal or link-down method to alert about a failed link.",
    "fail-action-on-extender": "Action on FortiExtender when interface fail.",
    "fail-alert-interfaces": "Names of the FortiGate interfaces to which the link failure alert is sent.",
    "dhcp-client-identifier": "DHCP client identifier.",
    "dhcp-renew-time": "DHCP renew time in seconds (300-604800), 0 means use the renew time provided by the server.",
    "ipunnumbered": "Unnumbered IP used for PPPoE interfaces for which no unique local address is provided.",
    "username": "Username of the PPPoE account, provided by your ISP.",
    "pppoe-egress-cos": "CoS in VLAN tag for outgoing PPPoE/PPP packets.",
    "pppoe-unnumbered-negotiate": "Enable/disable PPPoE unnumbered negotiation.",
    "password": "PPPoE account's password.",
    "idle-timeout": "PPPoE auto disconnect after idle timeout seconds, 0 means no timeout.",
    "multilink": "Enable/disable PPP multilink support.",
    "mrru": "PPP MRRU (296 - 65535, default = 1500).",
    "detected-peer-mtu": "MTU of detected peer (0 - 4294967295).",
    "disc-retry-timeout": "Time in seconds to wait before retrying to start a PPPoE discovery, 0 means no timeout.",
    "padt-retry-timeout": "PPPoE Active Discovery Terminate (PADT) used to terminate sessions after an idle time.",
    "service-name": "PPPoE service name.",
    "ac-name": "PPPoE server name.",
    "lcp-echo-interval": "Time in seconds between PPPoE Link Control Protocol (LCP) echo requests.",
    "lcp-max-echo-fails": "Maximum missed LCP echo messages before disconnect.",
    "defaultgw": "Enable to get the gateway IP from the DHCP or PPPoE server.",
    "dns-server-override": "Enable/disable use DNS acquired by DHCP or PPPoE.",
    "dns-server-protocol": "DNS transport protocols.",
    "auth-type": "PPP authentication type to use.",
    "pptp-client": "Enable/disable PPTP client.",
    "pptp-user": "PPTP user name.",
    "pptp-password": "PPTP password.",
    "pptp-server-ip": "PPTP server IP address.",
    "pptp-auth-type": "PPTP authentication type.",
    "pptp-timeout": "Idle timer in minutes (0 for disabled).",
    "arpforward": "Enable/disable ARP forwarding.",
    "ndiscforward": "Enable/disable NDISC forwarding.",
    "broadcast-forward": "Enable/disable broadcast forwarding.",
    "bfd": "Bidirectional Forwarding Detection (BFD) settings.",
    "bfd-desired-min-tx": "BFD desired minimal transmit interval.",
    "bfd-detect-mult": "BFD detection multiplier.",
    "bfd-required-min-rx": "BFD required minimal receive interval.",
    "l2forward": "Enable/disable l2 forwarding.",
    "icmp-send-redirect": "Enable/disable sending of ICMP redirects.",
    "icmp-accept-redirect": "Enable/disable ICMP accept redirect.",
    "reachable-time": "IPv4 reachable time in milliseconds (30000 - 3600000, default = 30000).",
    "vlanforward": "Enable/disable traffic forwarding between VLANs on this interface.",
    "stpforward": "Enable/disable STP forwarding.",
    "stpforward-mode": "Configure STP forwarding mode.",
    "ips-sniffer-mode": "Enable/disable the use of this interface as a one-armed sniffer.",
    "ident-accept": "Enable/disable authentication for this interface.",
    "ipmac": "Enable/disable IP/MAC binding.",
    "subst": "Enable to always send packets from this interface to a destination MAC address.",
    "macaddr": "Change the interface's MAC address.",
    "virtual-mac": "Change the interface's virtual MAC address.",
    "substitute-dst-mac": "Destination MAC address that all packets are sent to from this interface.",
    "speed": "Interface speed. The default setting and the options available depend on the interface hardware.",
    "status": "Bring the interface up or shut the interface down.",
    "netbios-forward": "Enable/disable NETBIOS forwarding.",
    "wins-ip": "WINS server IP.",
    "type": "Interface type.",
    "dedicated-to": "Configure interface for single purpose.",
    "trust-ip-1": "Trusted host for dedicated management traffic (0.0.0.0/24 for all hosts).",
    "trust-ip-2": "Trusted host for dedicated management traffic (0.0.0.0/24 for all hosts).",
    "trust-ip-3": "Trusted host for dedicated management traffic (0.0.0.0/24 for all hosts).",
    "trust-ip6-1": "Trusted IPv6 host for dedicated management traffic (::/0 for all hosts).",
    "trust-ip6-2": "Trusted IPv6 host for dedicated management traffic (::/0 for all hosts).",
    "trust-ip6-3": "Trusted IPv6 host for dedicated management traffic (::/0 for all hosts).",
    "ring-rx": "RX ring size.",
    "ring-tx": "TX ring size.",
    "wccp": "Enable/disable WCCP on this interface. Used for encapsulated WCCP communication between WCCP clients and servers.",
    "netflow-sampler": "Enable/disable NetFlow on this interface and set the data that NetFlow collects (rx, tx, or both).",
    "netflow-sample-rate": "NetFlow sample rate.  Sample one packet every configured number of packets (1 - 65535, default = 1, which means standard NetFlow where all packets are sampled).",
    "netflow-sampler-id": "Netflow sampler ID.",
    "sflow-sampler": "Enable/disable sFlow on this interface.",
    "drop-fragment": "Enable/disable drop fragment packets.",
    "src-check": "Enable/disable source IP check.",
    "sample-rate": "sFlow sample rate (10 - 99999).",
    "polling-interval": "sFlow polling interval in seconds (1 - 255).",
    "sample-direction": "Data that NetFlow collects (rx, tx, or both).",
    "explicit-web-proxy": "Enable/disable the explicit web proxy on this interface.",
    "explicit-ftp-proxy": "Enable/disable the explicit FTP proxy on this interface.",
    "proxy-captive-portal": "Enable/disable proxy captive portal on this interface.",
    "tcp-mss": "TCP maximum segment size. 0 means do not change segment size.",
    "inbandwidth": "Bandwidth limit for incoming traffic (0 - 80000000 kbps), 0 means unlimited.",
    "outbandwidth": "Bandwidth limit for outgoing traffic (0 - 80000000 kbps).",
    "egress-shaping-profile": "Outgoing traffic shaping profile.",
    "ingress-shaping-profile": "Incoming traffic shaping profile.",
    "spillover-threshold": "Egress Spillover threshold (0 - 16776000 kbps), 0 means unlimited.",
    "ingress-spillover-threshold": "Ingress Spillover threshold (0 - 16776000 kbps), 0 means unlimited.",
    "weight": "Default weight for static routes (if route has no weight configured).",
    "interface": "Interface name.",
    "external": "Enable/disable identifying the interface as an external interface (which usually means it's connected to the Internet).",
    "mtu-override": "Enable to set a custom MTU for this interface.",
    "mtu": "MTU value for this interface.",
    "vlan-protocol": "Ethernet protocol of VLAN.",
    "vlanid": "VLAN ID (1 - 4094).",
    "forward-domain": "Transparent mode forward domain.",
    "remote-ip": "Remote IP address of tunnel.",
    "member": "Physical interfaces that belong to the aggregate or redundant interface.",
    "lacp-mode": "LACP mode.",
    "lacp-ha-secondary": "LACP HA secondary member.",
    "system-id-type": "Method in which system ID is generated.",
    "system-id": "Define a system ID for the aggregate interface.",
    "lacp-speed": "How often the interface sends LACP messages.",
    "min-links": "Minimum number of aggregated ports that must be up.",
    "min-links-down": "Action to take when less than the configured minimum number of links are active.",
    "algorithm": "Frame distribution algorithm.",
    "link-up-delay": "Number of milliseconds to wait before considering a link is up.",
    "aggregate-type": "Type of aggregation.",
    "priority-override": "Enable/disable fail back to higher priority port once recovered.",
    "aggregate": "Aggregate interface.",
    "redundant-interface": "Redundant interface.",
    "devindex": "Device Index.",
    "vindex": "Switch control interface VLAN ID.",
    "switch": "Contained in switch.",
    "description": "Description.",
    "alias": "Alias will be displayed with the interface name to make it easier to distinguish.",
    "security-mode": "Turn on captive portal authentication for this interface.",
    "security-mac-auth-bypass": "Enable/disable MAC authentication bypass.",
    "security-ip-auth-bypass": "Enable/disable IP authentication bypass.",
    "security-external-web": "URL of external authentication web server.",
    "security-external-logout": "URL of external authentication logout server.",
    "replacemsg-override-group": "Replacement message override group.",
    "security-redirect-url": "URL redirection after disclaimer/authentication.",
    "auth-cert": "HTTPS server certificate.",
    "auth-portal-addr": "Address of captive portal.",
    "security-exempt-list": "Name of security-exempt-list.",
    "security-groups": "User groups that can authenticate with the captive portal.",
    "ike-saml-server": "Configure IKE authentication SAML server.",
    "device-identification": "Enable/disable passively gathering of device identity information about the devices on the network connected to this interface.",
    "exclude-signatures": "Exclude IOT or OT application signatures.",
    "device-user-identification": "Enable/disable passive gathering of user identity information about users on this interface.",
    "lldp-reception": "Enable/disable Link Layer Discovery Protocol (LLDP) reception.",
    "lldp-transmission": "Enable/disable Link Layer Discovery Protocol (LLDP) transmission.",
    "lldp-network-policy": "LLDP-MED network policy profile.",
    "estimated-upstream-bandwidth": "Estimated maximum upstream bandwidth (kbps). Used to estimate link utilization.",
    "estimated-downstream-bandwidth": "Estimated maximum downstream bandwidth (kbps). Used to estimate link utilization.",
    "measured-upstream-bandwidth": "Measured upstream bandwidth (kbps).",
    "measured-downstream-bandwidth": "Measured downstream bandwidth (kbps).",
    "bandwidth-measure-time": "Bandwidth measure time.",
    "monitor-bandwidth": "Enable monitoring bandwidth on this interface.",
    "vrrp-virtual-mac": "Enable/disable use of virtual MAC for VRRP.",
    "vrrp": "VRRP configuration.",
    "phy-setting": "PHY settings",
    "role": "Interface role.",
    "snmp-index": "Permanent SNMP Index of the interface.",
    "secondary-IP": "Enable/disable adding a secondary IP to this interface.",
    "secondaryip": "Second IP address of interface.",
    "preserve-session-route": "Enable/disable preservation of session route when dirty.",
    "auto-auth-extension-device": "Enable/disable automatic authorization of dedicated Fortinet extension device on this interface.",
    "ap-discover": "Enable/disable automatic registration of unknown FortiAP devices.",
    "fortilink-neighbor-detect": "Protocol for FortiGate neighbor discovery.",
    "ip-managed-by-fortiipam": "Enable/disable automatic IP address assignment of this interface by FortiIPAM.",
    "managed-subnetwork-size": "Number of IP addresses to be allocated by FortiIPAM and used by this FortiGate unit's DHCP server settings.",
    "fortilink-split-interface": "Enable/disable FortiLink split interface to connect member link to different FortiSwitch in stack for uplink redundancy.",
    "internal": "Implicitly created.",
    "fortilink-backup-link": "FortiLink split interface backup link.",
    "switch-controller-access-vlan": "Block FortiSwitch port-to-port traffic.",
    "switch-controller-traffic-policy": "Switch controller traffic policy for the VLAN.",
    "switch-controller-rspan-mode": "Stop Layer2 MAC learning and interception of BPDUs and other packets on this interface.",
    "switch-controller-netflow-collect": "NetFlow collection and processing.",
    "switch-controller-mgmt-vlan": "VLAN to use for FortiLink management purposes.",
    "switch-controller-igmp-snooping": "Switch controller IGMP snooping.",
    "switch-controller-igmp-snooping-proxy": "Switch controller IGMP snooping proxy.",
    "switch-controller-igmp-snooping-fast-leave": "Switch controller IGMP snooping fast-leave.",
    "switch-controller-dhcp-snooping": "Switch controller DHCP snooping.",
    "switch-controller-dhcp-snooping-verify-mac": "Switch controller DHCP snooping verify MAC.",
    "switch-controller-dhcp-snooping-option82": "Switch controller DHCP snooping option82.",
    "dhcp-snooping-server-list": "Configure DHCP server access list.",
    "switch-controller-arp-inspection": "Enable/disable/Monitor FortiSwitch ARP inspection.",
    "switch-controller-learning-limit": "Limit the number of dynamic MAC addresses on this VLAN (1 - 128, 0 = no limit, default).",
    "switch-controller-nac": "Integrated FortiLink settings for managed FortiSwitch.",
    "switch-controller-dynamic": "Integrated FortiLink settings for managed FortiSwitch.",
    "switch-controller-feature": "Interface's purpose when assigning traffic (read only).",
    "switch-controller-iot-scanning": "Enable/disable managed FortiSwitch IoT scanning.",
    "switch-controller-offload": "Enable/disable managed FortiSwitch routing offload.",
    "switch-controller-offload-ip": "IP for routing offload on FortiSwitch.",
    "switch-controller-offload-gw": "Enable/disable managed FortiSwitch routing offload gateway.",
    "swc-vlan": "Creation status for switch-controller VLANs.",
    "swc-first-create": "Initial create for switch-controller VLANs.",
    "color": "Color of icon on the GUI.",
    "tagging": "Config object tagging.",
    "eap-supplicant": "Enable/disable EAP-Supplicant.",
    "eap-method": "EAP method.",
    "eap-identity": "EAP identity.",
    "eap-password": "EAP password.",
    "eap-ca-cert": "EAP CA certificate name.",
    "eap-user-cert": "EAP user certificate name.",
    "default-purdue-level": "default purdue level of device detected on this interface.",
    "ipv6": "IPv6 of interface.",
    "physical": "Print physical interface information.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 15},
    "vdom": {"type": "string", "max_length": 31},
    "vrf": {"type": "integer", "min": 0, "max": 511},
    "cli-conn-status": {"type": "integer", "min": 0, "max": 4294967295},
    "distance": {"type": "integer", "min": 1, "max": 255},
    "priority": {"type": "integer", "min": 1, "max": 65535},
    "dhcp-relay-interface": {"type": "string", "max_length": 15},
    "dhcp-relay-vrf-select": {"type": "integer", "min": 0, "max": 511},
    "dhcp-relay-circuit-id": {"type": "string", "max_length": 64},
    "ping-serv-status": {"type": "integer", "min": 0, "max": 255},
    "ha-priority": {"type": "integer", "min": 1, "max": 50},
    "dhcp-client-identifier": {"type": "string", "max_length": 48},
    "dhcp-renew-time": {"type": "integer", "min": 300, "max": 604800},
    "username": {"type": "string", "max_length": 64},
    "idle-timeout": {"type": "integer", "min": 0, "max": 32767},
    "mrru": {"type": "integer", "min": 296, "max": 65535},
    "detected-peer-mtu": {"type": "integer", "min": 0, "max": 4294967295},
    "disc-retry-timeout": {"type": "integer", "min": 0, "max": 4294967295},
    "padt-retry-timeout": {"type": "integer", "min": 0, "max": 4294967295},
    "service-name": {"type": "string", "max_length": 63},
    "ac-name": {"type": "string", "max_length": 63},
    "lcp-echo-interval": {"type": "integer", "min": 0, "max": 32767},
    "lcp-max-echo-fails": {"type": "integer", "min": 0, "max": 32767},
    "pptp-user": {"type": "string", "max_length": 64},
    "pptp-timeout": {"type": "integer", "min": 0, "max": 65535},
    "bfd-desired-min-tx": {"type": "integer", "min": 1, "max": 100000},
    "bfd-detect-mult": {"type": "integer", "min": 1, "max": 50},
    "bfd-required-min-rx": {"type": "integer", "min": 1, "max": 100000},
    "reachable-time": {"type": "integer", "min": 30000, "max": 3600000},
    "ring-rx": {"type": "integer", "min": 0, "max": 4294967295},
    "ring-tx": {"type": "integer", "min": 0, "max": 4294967295},
    "netflow-sample-rate": {"type": "integer", "min": 1, "max": 65535},
    "netflow-sampler-id": {"type": "integer", "min": 1, "max": 254},
    "sample-rate": {"type": "integer", "min": 10, "max": 99999},
    "polling-interval": {"type": "integer", "min": 1, "max": 255},
    "tcp-mss": {"type": "integer", "min": 48, "max": 65535},
    "inbandwidth": {"type": "integer", "min": 0, "max": 80000000},
    "outbandwidth": {"type": "integer", "min": 0, "max": 80000000},
    "egress-shaping-profile": {"type": "string", "max_length": 35},
    "ingress-shaping-profile": {"type": "string", "max_length": 35},
    "spillover-threshold": {"type": "integer", "min": 0, "max": 16776000},
    "ingress-spillover-threshold": {"type": "integer", "min": 0, "max": 16776000},
    "weight": {"type": "integer", "min": 0, "max": 255},
    "interface": {"type": "string", "max_length": 15},
    "mtu": {"type": "integer", "min": 0, "max": 4294967295},
    "vlanid": {"type": "integer", "min": 1, "max": 4094},
    "forward-domain": {"type": "integer", "min": 0, "max": 2147483647},
    "min-links": {"type": "integer", "min": 1, "max": 32},
    "link-up-delay": {"type": "integer", "min": 50, "max": 3600000},
    "aggregate": {"type": "string", "max_length": 15},
    "redundant-interface": {"type": "string", "max_length": 15},
    "devindex": {"type": "integer", "min": 0, "max": 4294967295},
    "vindex": {"type": "integer", "min": 0, "max": 65535},
    "switch": {"type": "string", "max_length": 15},
    "alias": {"type": "string", "max_length": 25},
    "security-external-logout": {"type": "string", "max_length": 127},
    "replacemsg-override-group": {"type": "string", "max_length": 35},
    "auth-cert": {"type": "string", "max_length": 35},
    "auth-portal-addr": {"type": "string", "max_length": 63},
    "security-exempt-list": {"type": "string", "max_length": 35},
    "ike-saml-server": {"type": "string", "max_length": 35},
    "lldp-network-policy": {"type": "string", "max_length": 35},
    "estimated-upstream-bandwidth": {"type": "integer", "min": 0, "max": 4294967295},
    "estimated-downstream-bandwidth": {"type": "integer", "min": 0, "max": 4294967295},
    "measured-upstream-bandwidth": {"type": "integer", "min": 0, "max": 4294967295},
    "measured-downstream-bandwidth": {"type": "integer", "min": 0, "max": 4294967295},
    "bandwidth-measure-time": {"type": "integer", "min": 0, "max": 4294967295},
    "snmp-index": {"type": "integer", "min": 0, "max": 2147483647},
    "internal": {"type": "integer", "min": 0, "max": 255},
    "fortilink-backup-link": {"type": "integer", "min": 0, "max": 255},
    "switch-controller-traffic-policy": {"type": "string", "max_length": 63},
    "switch-controller-mgmt-vlan": {"type": "integer", "min": 1, "max": 4094},
    "switch-controller-learning-limit": {"type": "integer", "min": 0, "max": 128},
    "switch-controller-nac": {"type": "string", "max_length": 35},
    "switch-controller-dynamic": {"type": "string", "max_length": 35},
    "swc-vlan": {"type": "integer", "min": 0, "max": 4294967295},
    "swc-first-create": {"type": "integer", "min": 0, "max": 4294967295},
    "color": {"type": "integer", "min": 0, "max": 32},
    "eap-identity": {"type": "string", "max_length": 35},
    "eap-ca-cert": {"type": "string", "max_length": 79},
    "eap-user-cert": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "client-options": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "code": {
            "type": "integer",
            "help": "DHCP client option code.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "type": {
            "type": "option",
            "help": "DHCP client option type.",
            "default": "hex",
            "options": ["hex", "string", "ip", "fqdn"],
        },
        "value": {
            "type": "string",
            "help": "DHCP client option value.",
            "default": "",
            "max_length": 312,
        },
        "ip": {
            "type": "user",
            "help": "DHCP option IPs.",
            "default": "",
        },
    },
    "fail-alert-interfaces": {
        "name": {
            "type": "string",
            "help": "Names of the non-virtual interface.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
    },
    "member": {
        "interface-name": {
            "type": "string",
            "help": "Physical interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "security-groups": {
        "name": {
            "type": "string",
            "help": "Names of user groups that can authenticate with the captive portal.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "vrrp": {
        "vrid": {
            "type": "integer",
            "help": "Virtual router identifier (1 - 255).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 255,
        },
        "version": {
            "type": "option",
            "help": "VRRP version.",
            "default": "2",
            "options": ["2", "3"],
        },
        "vrgrp": {
            "type": "integer",
            "help": "VRRP group ID (1 - 65535).",
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
        "vrip": {
            "type": "ipv4-address-any",
            "help": "IP address of the virtual router.",
            "required": True,
            "default": "0.0.0.0",
        },
        "priority": {
            "type": "integer",
            "help": "Priority of the virtual router (1 - 255).",
            "default": 100,
            "min_value": 1,
            "max_value": 255,
        },
        "adv-interval": {
            "type": "integer",
            "help": "Advertisement interval (250 - 255000 milliseconds).",
            "default": 1000,
            "min_value": 250,
            "max_value": 255000,
        },
        "start-time": {
            "type": "integer",
            "help": "Startup time (1 - 255 seconds).",
            "default": 3,
            "min_value": 1,
            "max_value": 255,
        },
        "preempt": {
            "type": "option",
            "help": "Enable/disable preempt mode.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "accept-mode": {
            "type": "option",
            "help": "Enable/disable accept mode.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "vrdst": {
            "type": "ipv4-address-any",
            "help": "Monitor the route to this destination.",
            "default": "",
        },
        "vrdst-priority": {
            "type": "integer",
            "help": "Priority of the virtual router when the virtual router destination becomes unreachable (0 - 254).",
            "default": 0,
            "min_value": 0,
            "max_value": 254,
        },
        "ignore-default-route": {
            "type": "option",
            "help": "Enable/disable ignoring of default route when checking destination.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "status": {
            "type": "option",
            "help": "Enable/disable this VRRP configuration.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "proxy-arp": {
            "type": "string",
            "help": "VRRP Proxy ARP configuration.",
        },
    },
    "phy-setting": {
        "signal-ok-threshold": {
            "type": "integer",
            "help": "Configure the signal strength value at which the FortiGate unit detects that the receiving signal is idle or that data is not being received. Zero means idle detection is disabled. Higher values mean the signal strength must be higher in order for the FortiGate unit to consider the interface is not idle (0 - 12, default = 0).",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 12,
        },
    },
    "secondaryip": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip": {
            "type": "ipv4-classnet-host",
            "help": "Secondary IP address of the interface.",
            "default": "0.0.0.0 0.0.0.0",
        },
        "secip-relay-ip": {
            "type": "user",
            "help": "DHCP relay IP address.",
            "default": "",
        },
        "allowaccess": {
            "type": "option",
            "help": "Management access settings for the secondary IP address.",
            "default": "",
            "options": ["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "radius-acct", "probe-response", "fabric", "ftm", "speed-test", "scim"],
        },
        "gwdetect": {
            "type": "option",
            "help": "Enable/disable detect gateway alive for first.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ping-serv-status": {
            "type": "integer",
            "help": "PING server status.",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "detectserver": {
            "type": "user",
            "help": "Gateway's ping server for this IP.",
            "default": "",
        },
        "detectprotocol": {
            "type": "option",
            "help": "Protocols used to detect the server.",
            "default": "ping",
            "options": ["ping", "tcp-echo", "udp-echo"],
        },
        "ha-priority": {
            "type": "integer",
            "help": "HA election priority for the PING server.",
            "default": 1,
            "min_value": 1,
            "max_value": 50,
        },
    },
    "dhcp-snooping-server-list": {
        "name": {
            "type": "string",
            "help": "DHCP server name.",
            "default": "default",
            "max_length": 35,
        },
        "server-ip": {
            "type": "ipv4-address",
            "help": "IP address for DHCP server.",
            "default": "0.0.0.0",
        },
    },
    "tagging": {
        "name": {
            "type": "string",
            "help": "Tagging entry name.",
            "default": "",
            "max_length": 63,
        },
        "category": {
            "type": "string",
            "help": "Tag category.",
            "default": "",
            "max_length": 63,
        },
        "tags": {
            "type": "string",
            "help": "Tags.",
        },
    },
    "ipv6": {
        "ip6-mode": {
            "type": "option",
            "help": "Addressing mode (static, DHCP, delegated).",
            "default": "static",
            "options": ["static", "dhcp", "pppoe", "delegated"],
        },
        "client-options": {
            "type": "string",
            "help": "DHCP6 client options.",
        },
        "nd-mode": {
            "type": "option",
            "help": "Neighbor discovery mode.",
            "default": "basic",
            "options": ["basic", "SEND-compatible"],
        },
        "nd-cert": {
            "type": "string",
            "help": "Neighbor discovery certificate.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "nd-security-level": {
            "type": "integer",
            "help": "Neighbor discovery security level (0 - 7; 0 = least secure, default = 0).",
            "default": 0,
            "min_value": 0,
            "max_value": 7,
        },
        "nd-timestamp-delta": {
            "type": "integer",
            "help": "Neighbor discovery timestamp delta value (1 - 3600 sec; default = 300).",
            "default": 300,
            "min_value": 1,
            "max_value": 3600,
        },
        "nd-timestamp-fuzz": {
            "type": "integer",
            "help": "Neighbor discovery timestamp fuzz factor (1 - 60 sec; default = 1).",
            "default": 1,
            "min_value": 1,
            "max_value": 60,
        },
        "nd-cga-modifier": {
            "type": "user",
            "help": "Neighbor discovery CGA modifier.",
            "default": "",
        },
        "ip6-dns-server-override": {
            "type": "option",
            "help": "Enable/disable using the DNS server acquired by DHCP.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ip6-address": {
            "type": "ipv6-prefix",
            "help": "Primary IPv6 address prefix. Syntax: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx.",
            "default": "::/0",
        },
        "ip6-extra-addr": {
            "type": "string",
            "help": "Extra IPv6 address prefixes of interface.",
        },
        "ip6-allowaccess": {
            "type": "option",
            "help": "Allow management access to the interface.",
            "default": "",
            "options": ["ping", "https", "ssh", "snmp", "http", "telnet", "fgfm", "fabric", "scim", "probe-response"],
        },
        "ip6-send-adv": {
            "type": "option",
            "help": "Enable/disable sending advertisements about the interface.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "icmp6-send-redirect": {
            "type": "option",
            "help": "Enable/disable sending of ICMPv6 redirects.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ip6-manage-flag": {
            "type": "option",
            "help": "Enable/disable the managed flag.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ip6-other-flag": {
            "type": "option",
            "help": "Enable/disable the other IPv6 flag.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ip6-max-interval": {
            "type": "integer",
            "help": "IPv6 maximum interval (4 to 1800 sec).",
            "default": 600,
            "min_value": 4,
            "max_value": 1800,
        },
        "ip6-min-interval": {
            "type": "integer",
            "help": "IPv6 minimum interval (3 to 1350 sec).",
            "default": 198,
            "min_value": 3,
            "max_value": 1350,
        },
        "ip6-link-mtu": {
            "type": "integer",
            "help": "IPv6 link MTU.",
            "default": 0,
            "min_value": 1280,
            "max_value": 16000,
        },
        "ra-send-mtu": {
            "type": "option",
            "help": "Enable/disable sending link MTU in RA packet.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "ip6-reachable-time": {
            "type": "integer",
            "help": "IPv6 reachable time (milliseconds; 0 means unspecified).",
            "default": 0,
            "min_value": 0,
            "max_value": 3600000,
        },
        "ip6-retrans-time": {
            "type": "integer",
            "help": "IPv6 retransmit time (milliseconds; 0 means unspecified).",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip6-default-life": {
            "type": "integer",
            "help": "Default life (sec).",
            "default": 1800,
            "min_value": 0,
            "max_value": 9000,
        },
        "ip6-hop-limit": {
            "type": "integer",
            "help": "Hop limit (0 means unspecified).",
            "default": 0,
            "min_value": 0,
            "max_value": 255,
        },
        "ip6-adv-rio": {
            "type": "option",
            "help": "Enable/disable sending advertisements with route information option.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "ip6-route-pref": {
            "type": "option",
            "help": "Set route preference to the interface (default = medium).",
            "default": "medium",
            "options": ["medium", "high", "low"],
        },
        "ip6-route-list": {
            "type": "string",
            "help": "Advertised route list.",
        },
        "autoconf": {
            "type": "option",
            "help": "Enable/disable address auto config.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "unique-autoconf-addr": {
            "type": "option",
            "help": "Enable/disable unique auto config address.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "interface-identifier": {
            "type": "ipv6-address",
            "help": "IPv6 interface identifier.",
            "default": "::",
        },
        "ip6-prefix-mode": {
            "type": "option",
            "help": "Assigning a prefix from DHCP or RA.",
            "default": "dhcp6",
            "options": ["dhcp6", "ra"],
        },
        "ip6-delegated-prefix-iaid": {
            "type": "integer",
            "help": "IAID of obtained delegated-prefix from the upstream interface.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip6-upstream-interface": {
            "type": "string",
            "help": "Interface name providing delegated information.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "ip6-subnet": {
            "type": "ipv6-prefix",
            "help": "Subnet to routing prefix. Syntax: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx.",
            "default": "::/0",
        },
        "ip6-prefix-list": {
            "type": "string",
            "help": "Advertised prefix list.",
        },
        "ip6-rdnss-list": {
            "type": "string",
            "help": "Advertised IPv6 RDNSS list.",
        },
        "ip6-dnssl-list": {
            "type": "string",
            "help": "Advertised IPv6 DNSS list.",
        },
        "ip6-delegated-prefix-list": {
            "type": "string",
            "help": "Advertised IPv6 delegated prefix list.",
        },
        "dhcp6-relay-service": {
            "type": "option",
            "help": "Enable/disable DHCPv6 relay.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "dhcp6-relay-type": {
            "type": "option",
            "help": "DHCPv6 relay type.",
            "default": "regular",
            "options": ["regular"],
        },
        "dhcp6-relay-source-interface": {
            "type": "option",
            "help": "Enable/disable use of address on this interface as the source address of the relay message.",
            "default": "disable",
            "options": ["disable", "enable"],
        },
        "dhcp6-relay-ip": {
            "type": "user",
            "help": "DHCPv6 relay IP address.",
            "default": "",
        },
        "dhcp6-relay-source-ip": {
            "type": "ipv6-address",
            "help": "IPv6 address used by the DHCP6 relay as its source IP.",
            "default": "::",
        },
        "dhcp6-relay-interface-id": {
            "type": "string",
            "help": "DHCP6 relay interface ID.",
            "default": "",
            "max_length": 64,
        },
        "dhcp6-client-options": {
            "type": "option",
            "help": "DHCPv6 client options.",
            "default": "",
            "options": ["rapid", "iapd", "iana"],
        },
        "dhcp6-prefix-delegation": {
            "type": "option",
            "help": "Enable/disable DHCPv6 prefix delegation.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dhcp6-information-request": {
            "type": "option",
            "help": "Enable/disable DHCPv6 information request.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "dhcp6-iapd-list": {
            "type": "string",
            "help": "DHCPv6 IA-PD list.",
        },
        "cli-conn6-status": {
            "type": "integer",
            "help": "CLI IPv6 connection status.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "vrrp-virtual-mac6": {
            "type": "option",
            "help": "Enable/disable virtual MAC for VRRP.",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "vrip6_link_local": {
            "type": "ipv6-address",
            "help": "Link-local IPv6 address of virtual router.",
            "default": "::",
        },
        "vrrp6": {
            "type": "string",
            "help": "IPv6 VRRP configuration.",
        },
    },
    "physical": {
        "<interface>": {
            "type": "value",
            "help": "Interface name.",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_FORTILINK = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_SOURCE_IP = [
    "outbound",
    "fixed",
]
VALID_BODY_MODE = [
    "static",
    "dhcp",
    "pppoe",
]
VALID_BODY_DHCP_RELAY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_DHCP_BROADCAST_FLAG = [
    "disable",
    "enable",
]
VALID_BODY_DHCP_RELAY_SERVICE = [
    "disable",
    "enable",
]
VALID_BODY_DHCP_RELAY_REQUEST_ALL_SERVER = [
    "disable",
    "enable",
]
VALID_BODY_DHCP_RELAY_ALLOW_NO_END_OPTION = [
    "disable",
    "enable",
]
VALID_BODY_DHCP_RELAY_TYPE = [
    "regular",
    "ipsec",
]
VALID_BODY_DHCP_SMART_RELAY = [
    "disable",
    "enable",
]
VALID_BODY_DHCP_RELAY_AGENT_OPTION = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_CLASSLESS_ROUTE_ADDITION = [
    "enable",
    "disable",
]
VALID_BODY_ALLOWACCESS = [
    "ping",
    "https",
    "ssh",
    "snmp",
    "http",
    "telnet",
    "fgfm",
    "radius-acct",
    "probe-response",
    "fabric",
    "ftm",
    "speed-test",
    "scim",
]
VALID_BODY_GWDETECT = [
    "enable",
    "disable",
]
VALID_BODY_DETECTPROTOCOL = [
    "ping",
    "tcp-echo",
    "udp-echo",
]
VALID_BODY_FAIL_DETECT = [
    "enable",
    "disable",
]
VALID_BODY_FAIL_DETECT_OPTION = [
    "detectserver",
    "link-down",
]
VALID_BODY_FAIL_ALERT_METHOD = [
    "link-failed-signal",
    "link-down",
]
VALID_BODY_FAIL_ACTION_ON_EXTENDER = [
    "soft-restart",
    "hard-restart",
    "reboot",
]
VALID_BODY_PPPOE_EGRESS_COS = [
    "cos0",
    "cos1",
    "cos2",
    "cos3",
    "cos4",
    "cos5",
    "cos6",
    "cos7",
]
VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE = [
    "enable",
    "disable",
]
VALID_BODY_MULTILINK = [
    "enable",
    "disable",
]
VALID_BODY_DEFAULTGW = [
    "enable",
    "disable",
]
VALID_BODY_DNS_SERVER_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_DNS_SERVER_PROTOCOL = [
    "cleartext",
    "dot",
    "doh",
]
VALID_BODY_AUTH_TYPE = [
    "auto",
    "pap",
    "chap",
    "mschapv1",
    "mschapv2",
]
VALID_BODY_PPTP_CLIENT = [
    "enable",
    "disable",
]
VALID_BODY_PPTP_AUTH_TYPE = [
    "auto",
    "pap",
    "chap",
    "mschapv1",
    "mschapv2",
]
VALID_BODY_ARPFORWARD = [
    "enable",
    "disable",
]
VALID_BODY_NDISCFORWARD = [
    "enable",
    "disable",
]
VALID_BODY_BROADCAST_FORWARD = [
    "enable",
    "disable",
]
VALID_BODY_BFD = [
    "global",
    "enable",
    "disable",
]
VALID_BODY_L2FORWARD = [
    "enable",
    "disable",
]
VALID_BODY_ICMP_SEND_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_ICMP_ACCEPT_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_VLANFORWARD = [
    "enable",
    "disable",
]
VALID_BODY_STPFORWARD = [
    "enable",
    "disable",
]
VALID_BODY_STPFORWARD_MODE = [
    "rpl-all-ext-id",
    "rpl-bridge-ext-id",
    "rpl-nothing",
]
VALID_BODY_IPS_SNIFFER_MODE = [
    "enable",
    "disable",
]
VALID_BODY_IDENT_ACCEPT = [
    "enable",
    "disable",
]
VALID_BODY_IPMAC = [
    "enable",
    "disable",
]
VALID_BODY_SUBST = [
    "enable",
    "disable",
]
VALID_BODY_SPEED = [
    "auto",
    "10full",
    "10half",
    "100full",
    "100half",
    "100auto",
    "1000full",
    "1000auto",
]
VALID_BODY_STATUS = [
    "up",
    "down",
]
VALID_BODY_NETBIOS_FORWARD = [
    "disable",
    "enable",
]
VALID_BODY_TYPE = [
    "physical",
    "vlan",
    "aggregate",
    "redundant",
    "tunnel",
    "vdom-link",
    "loopback",
    "switch",
    "vap-switch",
    "wl-mesh",
    "fext-wan",
    "vxlan",
    "geneve",
    "switch-vlan",
    "emac-vlan",
    "lan-extension",
]
VALID_BODY_DEDICATED_TO = [
    "none",
    "management",
]
VALID_BODY_WCCP = [
    "enable",
    "disable",
]
VALID_BODY_NETFLOW_SAMPLER = [
    "disable",
    "tx",
    "rx",
    "both",
]
VALID_BODY_SFLOW_SAMPLER = [
    "enable",
    "disable",
]
VALID_BODY_DROP_FRAGMENT = [
    "enable",
    "disable",
]
VALID_BODY_SRC_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_SAMPLE_DIRECTION = [
    "tx",
    "rx",
    "both",
]
VALID_BODY_EXPLICIT_WEB_PROXY = [
    "enable",
    "disable",
]
VALID_BODY_EXPLICIT_FTP_PROXY = [
    "enable",
    "disable",
]
VALID_BODY_PROXY_CAPTIVE_PORTAL = [
    "enable",
    "disable",
]
VALID_BODY_EXTERNAL = [
    "enable",
    "disable",
]
VALID_BODY_MTU_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_VLAN_PROTOCOL = [
    "8021q",
    "8021ad",
]
VALID_BODY_LACP_MODE = [
    "static",
    "passive",
    "active",
]
VALID_BODY_LACP_HA_SECONDARY = [
    "enable",
    "disable",
]
VALID_BODY_SYSTEM_ID_TYPE = [
    "auto",
    "user",
]
VALID_BODY_LACP_SPEED = [
    "slow",
    "fast",
]
VALID_BODY_MIN_LINKS_DOWN = [
    "operational",
    "administrative",
]
VALID_BODY_ALGORITHM = [
    "L2",
    "L3",
    "L4",
    "NPU-GRE",
    "Source-MAC",
]
VALID_BODY_AGGREGATE_TYPE = [
    "physical",
    "vxlan",
]
VALID_BODY_PRIORITY_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_SECURITY_MODE = [
    "none",
    "captive-portal",
    "802.1X",
]
VALID_BODY_SECURITY_MAC_AUTH_BYPASS = [
    "mac-auth-only",
    "enable",
    "disable",
]
VALID_BODY_SECURITY_IP_AUTH_BYPASS = [
    "enable",
    "disable",
]
VALID_BODY_DEVICE_IDENTIFICATION = [
    "enable",
    "disable",
]
VALID_BODY_EXCLUDE_SIGNATURES = [
    "iot",
    "ot",
]
VALID_BODY_DEVICE_USER_IDENTIFICATION = [
    "enable",
    "disable",
]
VALID_BODY_LLDP_RECEPTION = [
    "enable",
    "disable",
    "vdom",
]
VALID_BODY_LLDP_TRANSMISSION = [
    "enable",
    "disable",
    "vdom",
]
VALID_BODY_MONITOR_BANDWIDTH = [
    "enable",
    "disable",
]
VALID_BODY_VRRP_VIRTUAL_MAC = [
    "enable",
    "disable",
]
VALID_BODY_ROLE = [
    "lan",
    "wan",
    "dmz",
    "undefined",
]
VALID_BODY_SECONDARY_IP = [
    "enable",
    "disable",
]
VALID_BODY_PRESERVE_SESSION_ROUTE = [
    "enable",
    "disable",
]
VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE = [
    "enable",
    "disable",
]
VALID_BODY_AP_DISCOVER = [
    "enable",
    "disable",
]
VALID_BODY_FORTILINK_NEIGHBOR_DETECT = [
    "lldp",
    "fortilink",
]
VALID_BODY_IP_MANAGED_BY_FORTIIPAM = [
    "inherit-global",
    "enable",
    "disable",
]
VALID_BODY_MANAGED_SUBNETWORK_SIZE = [
    "4",
    "8",
    "16",
    "32",
    "64",
    "128",
    "256",
    "512",
    "1024",
    "2048",
    "4096",
    "8192",
    "16384",
    "32768",
    "65536",
    "131072",
    "262144",
    "524288",
    "1048576",
    "2097152",
    "4194304",
    "8388608",
    "16777216",
]
VALID_BODY_FORTILINK_SPLIT_INTERFACE = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_ACCESS_VLAN = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_RSPAN_MODE = [
    "disable",
    "enable",
]
VALID_BODY_SWITCH_CONTROLLER_NETFLOW_COLLECT = [
    "disable",
    "enable",
]
VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_PROXY = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_FAST_LEAVE = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_VERIFY_MAC = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_OPTION82 = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_ARP_INSPECTION = [
    "enable",
    "disable",
    "monitor",
]
VALID_BODY_SWITCH_CONTROLLER_FEATURE = [
    "none",
    "default-vlan",
    "quarantine",
    "rspan",
    "voice",
    "video",
    "nac",
    "nac-segment",
]
VALID_BODY_SWITCH_CONTROLLER_IOT_SCANNING = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_OFFLOAD = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER_OFFLOAD_GW = [
    "enable",
    "disable",
]
VALID_BODY_EAP_SUPPLICANT = [
    "enable",
    "disable",
]
VALID_BODY_EAP_METHOD = [
    "tls",
    "peap",
]
VALID_BODY_DEFAULT_PURDUE_LEVEL = [
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


def validate_system_interface_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/interface."""
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


def validate_system_interface_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/interface object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "fortilink" in payload:
        is_valid, error = _validate_enum_field(
            "fortilink",
            payload["fortilink"],
            VALID_BODY_FORTILINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-source-ip" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-source-ip",
            payload["switch-controller-source-ip"],
            VALID_BODY_SWITCH_CONTROLLER_SOURCE_IP,
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
    if "dhcp-relay-interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-interface-select-method",
            payload["dhcp-relay-interface-select-method"],
            VALID_BODY_DHCP_RELAY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-broadcast-flag" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-broadcast-flag",
            payload["dhcp-broadcast-flag"],
            VALID_BODY_DHCP_BROADCAST_FLAG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-service" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-service",
            payload["dhcp-relay-service"],
            VALID_BODY_DHCP_RELAY_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-request-all-server" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-request-all-server",
            payload["dhcp-relay-request-all-server"],
            VALID_BODY_DHCP_RELAY_REQUEST_ALL_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-allow-no-end-option" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-allow-no-end-option",
            payload["dhcp-relay-allow-no-end-option"],
            VALID_BODY_DHCP_RELAY_ALLOW_NO_END_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-type" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-type",
            payload["dhcp-relay-type"],
            VALID_BODY_DHCP_RELAY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-smart-relay" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-smart-relay",
            payload["dhcp-smart-relay"],
            VALID_BODY_DHCP_SMART_RELAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-agent-option" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-agent-option",
            payload["dhcp-relay-agent-option"],
            VALID_BODY_DHCP_RELAY_AGENT_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-classless-route-addition" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-classless-route-addition",
            payload["dhcp-classless-route-addition"],
            VALID_BODY_DHCP_CLASSLESS_ROUTE_ADDITION,
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
    if "gwdetect" in payload:
        is_valid, error = _validate_enum_field(
            "gwdetect",
            payload["gwdetect"],
            VALID_BODY_GWDETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "detectprotocol" in payload:
        is_valid, error = _validate_enum_field(
            "detectprotocol",
            payload["detectprotocol"],
            VALID_BODY_DETECTPROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-detect" in payload:
        is_valid, error = _validate_enum_field(
            "fail-detect",
            payload["fail-detect"],
            VALID_BODY_FAIL_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-detect-option" in payload:
        is_valid, error = _validate_enum_field(
            "fail-detect-option",
            payload["fail-detect-option"],
            VALID_BODY_FAIL_DETECT_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-alert-method" in payload:
        is_valid, error = _validate_enum_field(
            "fail-alert-method",
            payload["fail-alert-method"],
            VALID_BODY_FAIL_ALERT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-action-on-extender" in payload:
        is_valid, error = _validate_enum_field(
            "fail-action-on-extender",
            payload["fail-action-on-extender"],
            VALID_BODY_FAIL_ACTION_ON_EXTENDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pppoe-egress-cos" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-egress-cos",
            payload["pppoe-egress-cos"],
            VALID_BODY_PPPOE_EGRESS_COS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pppoe-unnumbered-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-unnumbered-negotiate",
            payload["pppoe-unnumbered-negotiate"],
            VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multilink" in payload:
        is_valid, error = _validate_enum_field(
            "multilink",
            payload["multilink"],
            VALID_BODY_MULTILINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "defaultgw" in payload:
        is_valid, error = _validate_enum_field(
            "defaultgw",
            payload["defaultgw"],
            VALID_BODY_DEFAULTGW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-server-override" in payload:
        is_valid, error = _validate_enum_field(
            "dns-server-override",
            payload["dns-server-override"],
            VALID_BODY_DNS_SERVER_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-server-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "dns-server-protocol",
            payload["dns-server-protocol"],
            VALID_BODY_DNS_SERVER_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pptp-client" in payload:
        is_valid, error = _validate_enum_field(
            "pptp-client",
            payload["pptp-client"],
            VALID_BODY_PPTP_CLIENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pptp-auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "pptp-auth-type",
            payload["pptp-auth-type"],
            VALID_BODY_PPTP_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "arpforward" in payload:
        is_valid, error = _validate_enum_field(
            "arpforward",
            payload["arpforward"],
            VALID_BODY_ARPFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ndiscforward" in payload:
        is_valid, error = _validate_enum_field(
            "ndiscforward",
            payload["ndiscforward"],
            VALID_BODY_NDISCFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-forward" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-forward",
            payload["broadcast-forward"],
            VALID_BODY_BROADCAST_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bfd" in payload:
        is_valid, error = _validate_enum_field(
            "bfd",
            payload["bfd"],
            VALID_BODY_BFD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l2forward" in payload:
        is_valid, error = _validate_enum_field(
            "l2forward",
            payload["l2forward"],
            VALID_BODY_L2FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "icmp-send-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "icmp-send-redirect",
            payload["icmp-send-redirect"],
            VALID_BODY_ICMP_SEND_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "icmp-accept-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "icmp-accept-redirect",
            payload["icmp-accept-redirect"],
            VALID_BODY_ICMP_ACCEPT_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlanforward" in payload:
        is_valid, error = _validate_enum_field(
            "vlanforward",
            payload["vlanforward"],
            VALID_BODY_VLANFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "stpforward" in payload:
        is_valid, error = _validate_enum_field(
            "stpforward",
            payload["stpforward"],
            VALID_BODY_STPFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "stpforward-mode" in payload:
        is_valid, error = _validate_enum_field(
            "stpforward-mode",
            payload["stpforward-mode"],
            VALID_BODY_STPFORWARD_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-sniffer-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ips-sniffer-mode",
            payload["ips-sniffer-mode"],
            VALID_BODY_IPS_SNIFFER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ident-accept" in payload:
        is_valid, error = _validate_enum_field(
            "ident-accept",
            payload["ident-accept"],
            VALID_BODY_IDENT_ACCEPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipmac" in payload:
        is_valid, error = _validate_enum_field(
            "ipmac",
            payload["ipmac"],
            VALID_BODY_IPMAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subst" in payload:
        is_valid, error = _validate_enum_field(
            "subst",
            payload["subst"],
            VALID_BODY_SUBST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "speed" in payload:
        is_valid, error = _validate_enum_field(
            "speed",
            payload["speed"],
            VALID_BODY_SPEED,
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
    if "netbios-forward" in payload:
        is_valid, error = _validate_enum_field(
            "netbios-forward",
            payload["netbios-forward"],
            VALID_BODY_NETBIOS_FORWARD,
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
    if "dedicated-to" in payload:
        is_valid, error = _validate_enum_field(
            "dedicated-to",
            payload["dedicated-to"],
            VALID_BODY_DEDICATED_TO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wccp" in payload:
        is_valid, error = _validate_enum_field(
            "wccp",
            payload["wccp"],
            VALID_BODY_WCCP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "netflow-sampler" in payload:
        is_valid, error = _validate_enum_field(
            "netflow-sampler",
            payload["netflow-sampler"],
            VALID_BODY_NETFLOW_SAMPLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sflow-sampler" in payload:
        is_valid, error = _validate_enum_field(
            "sflow-sampler",
            payload["sflow-sampler"],
            VALID_BODY_SFLOW_SAMPLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "drop-fragment" in payload:
        is_valid, error = _validate_enum_field(
            "drop-fragment",
            payload["drop-fragment"],
            VALID_BODY_DROP_FRAGMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-check" in payload:
        is_valid, error = _validate_enum_field(
            "src-check",
            payload["src-check"],
            VALID_BODY_SRC_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sample-direction" in payload:
        is_valid, error = _validate_enum_field(
            "sample-direction",
            payload["sample-direction"],
            VALID_BODY_SAMPLE_DIRECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "explicit-web-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "explicit-web-proxy",
            payload["explicit-web-proxy"],
            VALID_BODY_EXPLICIT_WEB_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "explicit-ftp-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "explicit-ftp-proxy",
            payload["explicit-ftp-proxy"],
            VALID_BODY_EXPLICIT_FTP_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-captive-portal" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-captive-portal",
            payload["proxy-captive-portal"],
            VALID_BODY_PROXY_CAPTIVE_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external" in payload:
        is_valid, error = _validate_enum_field(
            "external",
            payload["external"],
            VALID_BODY_EXTERNAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mtu-override" in payload:
        is_valid, error = _validate_enum_field(
            "mtu-override",
            payload["mtu-override"],
            VALID_BODY_MTU_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-protocol",
            payload["vlan-protocol"],
            VALID_BODY_VLAN_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lacp-mode" in payload:
        is_valid, error = _validate_enum_field(
            "lacp-mode",
            payload["lacp-mode"],
            VALID_BODY_LACP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lacp-ha-secondary" in payload:
        is_valid, error = _validate_enum_field(
            "lacp-ha-secondary",
            payload["lacp-ha-secondary"],
            VALID_BODY_LACP_HA_SECONDARY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "system-id-type",
            payload["system-id-type"],
            VALID_BODY_SYSTEM_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lacp-speed" in payload:
        is_valid, error = _validate_enum_field(
            "lacp-speed",
            payload["lacp-speed"],
            VALID_BODY_LACP_SPEED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "min-links-down" in payload:
        is_valid, error = _validate_enum_field(
            "min-links-down",
            payload["min-links-down"],
            VALID_BODY_MIN_LINKS_DOWN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "algorithm",
            payload["algorithm"],
            VALID_BODY_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "aggregate-type" in payload:
        is_valid, error = _validate_enum_field(
            "aggregate-type",
            payload["aggregate-type"],
            VALID_BODY_AGGREGATE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-override" in payload:
        is_valid, error = _validate_enum_field(
            "priority-override",
            payload["priority-override"],
            VALID_BODY_PRIORITY_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "security-mac-auth-bypass",
            payload["security-mac-auth-bypass"],
            VALID_BODY_SECURITY_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-ip-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "security-ip-auth-bypass",
            payload["security-ip-auth-bypass"],
            VALID_BODY_SECURITY_IP_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-identification" in payload:
        is_valid, error = _validate_enum_field(
            "device-identification",
            payload["device-identification"],
            VALID_BODY_DEVICE_IDENTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "exclude-signatures" in payload:
        is_valid, error = _validate_enum_field(
            "exclude-signatures",
            payload["exclude-signatures"],
            VALID_BODY_EXCLUDE_SIGNATURES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-user-identification" in payload:
        is_valid, error = _validate_enum_field(
            "device-user-identification",
            payload["device-user-identification"],
            VALID_BODY_DEVICE_USER_IDENTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lldp-reception" in payload:
        is_valid, error = _validate_enum_field(
            "lldp-reception",
            payload["lldp-reception"],
            VALID_BODY_LLDP_RECEPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lldp-transmission" in payload:
        is_valid, error = _validate_enum_field(
            "lldp-transmission",
            payload["lldp-transmission"],
            VALID_BODY_LLDP_TRANSMISSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "monitor-bandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "monitor-bandwidth",
            payload["monitor-bandwidth"],
            VALID_BODY_MONITOR_BANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vrrp-virtual-mac" in payload:
        is_valid, error = _validate_enum_field(
            "vrrp-virtual-mac",
            payload["vrrp-virtual-mac"],
            VALID_BODY_VRRP_VIRTUAL_MAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "role" in payload:
        is_valid, error = _validate_enum_field(
            "role",
            payload["role"],
            VALID_BODY_ROLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secondary-IP" in payload:
        is_valid, error = _validate_enum_field(
            "secondary-IP",
            payload["secondary-IP"],
            VALID_BODY_SECONDARY_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "preserve-session-route" in payload:
        is_valid, error = _validate_enum_field(
            "preserve-session-route",
            payload["preserve-session-route"],
            VALID_BODY_PRESERVE_SESSION_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-auth-extension-device" in payload:
        is_valid, error = _validate_enum_field(
            "auto-auth-extension-device",
            payload["auto-auth-extension-device"],
            VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-discover" in payload:
        is_valid, error = _validate_enum_field(
            "ap-discover",
            payload["ap-discover"],
            VALID_BODY_AP_DISCOVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortilink-neighbor-detect" in payload:
        is_valid, error = _validate_enum_field(
            "fortilink-neighbor-detect",
            payload["fortilink-neighbor-detect"],
            VALID_BODY_FORTILINK_NEIGHBOR_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-managed-by-fortiipam" in payload:
        is_valid, error = _validate_enum_field(
            "ip-managed-by-fortiipam",
            payload["ip-managed-by-fortiipam"],
            VALID_BODY_IP_MANAGED_BY_FORTIIPAM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "managed-subnetwork-size" in payload:
        is_valid, error = _validate_enum_field(
            "managed-subnetwork-size",
            payload["managed-subnetwork-size"],
            VALID_BODY_MANAGED_SUBNETWORK_SIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortilink-split-interface" in payload:
        is_valid, error = _validate_enum_field(
            "fortilink-split-interface",
            payload["fortilink-split-interface"],
            VALID_BODY_FORTILINK_SPLIT_INTERFACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-access-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-access-vlan",
            payload["switch-controller-access-vlan"],
            VALID_BODY_SWITCH_CONTROLLER_ACCESS_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-rspan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-rspan-mode",
            payload["switch-controller-rspan-mode"],
            VALID_BODY_SWITCH_CONTROLLER_RSPAN_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-netflow-collect" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-netflow-collect",
            payload["switch-controller-netflow-collect"],
            VALID_BODY_SWITCH_CONTROLLER_NETFLOW_COLLECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-igmp-snooping" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-igmp-snooping",
            payload["switch-controller-igmp-snooping"],
            VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-igmp-snooping-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-igmp-snooping-proxy",
            payload["switch-controller-igmp-snooping-proxy"],
            VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-igmp-snooping-fast-leave" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-igmp-snooping-fast-leave",
            payload["switch-controller-igmp-snooping-fast-leave"],
            VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_FAST_LEAVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-dhcp-snooping" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-dhcp-snooping",
            payload["switch-controller-dhcp-snooping"],
            VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-dhcp-snooping-verify-mac" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-dhcp-snooping-verify-mac",
            payload["switch-controller-dhcp-snooping-verify-mac"],
            VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_VERIFY_MAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-dhcp-snooping-option82" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-dhcp-snooping-option82",
            payload["switch-controller-dhcp-snooping-option82"],
            VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_OPTION82,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-arp-inspection" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-arp-inspection",
            payload["switch-controller-arp-inspection"],
            VALID_BODY_SWITCH_CONTROLLER_ARP_INSPECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-feature" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-feature",
            payload["switch-controller-feature"],
            VALID_BODY_SWITCH_CONTROLLER_FEATURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-iot-scanning" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-iot-scanning",
            payload["switch-controller-iot-scanning"],
            VALID_BODY_SWITCH_CONTROLLER_IOT_SCANNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-offload" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-offload",
            payload["switch-controller-offload"],
            VALID_BODY_SWITCH_CONTROLLER_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-offload-gw" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-offload-gw",
            payload["switch-controller-offload-gw"],
            VALID_BODY_SWITCH_CONTROLLER_OFFLOAD_GW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-supplicant" in payload:
        is_valid, error = _validate_enum_field(
            "eap-supplicant",
            payload["eap-supplicant"],
            VALID_BODY_EAP_SUPPLICANT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-method" in payload:
        is_valid, error = _validate_enum_field(
            "eap-method",
            payload["eap-method"],
            VALID_BODY_EAP_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-purdue-level" in payload:
        is_valid, error = _validate_enum_field(
            "default-purdue-level",
            payload["default-purdue-level"],
            VALID_BODY_DEFAULT_PURDUE_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_interface_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/interface."""
    # Validate enum values using central function
    if "fortilink" in payload:
        is_valid, error = _validate_enum_field(
            "fortilink",
            payload["fortilink"],
            VALID_BODY_FORTILINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-source-ip" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-source-ip",
            payload["switch-controller-source-ip"],
            VALID_BODY_SWITCH_CONTROLLER_SOURCE_IP,
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
    if "dhcp-relay-interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-interface-select-method",
            payload["dhcp-relay-interface-select-method"],
            VALID_BODY_DHCP_RELAY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-broadcast-flag" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-broadcast-flag",
            payload["dhcp-broadcast-flag"],
            VALID_BODY_DHCP_BROADCAST_FLAG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-service" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-service",
            payload["dhcp-relay-service"],
            VALID_BODY_DHCP_RELAY_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-request-all-server" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-request-all-server",
            payload["dhcp-relay-request-all-server"],
            VALID_BODY_DHCP_RELAY_REQUEST_ALL_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-allow-no-end-option" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-allow-no-end-option",
            payload["dhcp-relay-allow-no-end-option"],
            VALID_BODY_DHCP_RELAY_ALLOW_NO_END_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-type" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-type",
            payload["dhcp-relay-type"],
            VALID_BODY_DHCP_RELAY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-smart-relay" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-smart-relay",
            payload["dhcp-smart-relay"],
            VALID_BODY_DHCP_SMART_RELAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-relay-agent-option" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-relay-agent-option",
            payload["dhcp-relay-agent-option"],
            VALID_BODY_DHCP_RELAY_AGENT_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-classless-route-addition" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-classless-route-addition",
            payload["dhcp-classless-route-addition"],
            VALID_BODY_DHCP_CLASSLESS_ROUTE_ADDITION,
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
    if "gwdetect" in payload:
        is_valid, error = _validate_enum_field(
            "gwdetect",
            payload["gwdetect"],
            VALID_BODY_GWDETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "detectprotocol" in payload:
        is_valid, error = _validate_enum_field(
            "detectprotocol",
            payload["detectprotocol"],
            VALID_BODY_DETECTPROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-detect" in payload:
        is_valid, error = _validate_enum_field(
            "fail-detect",
            payload["fail-detect"],
            VALID_BODY_FAIL_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-detect-option" in payload:
        is_valid, error = _validate_enum_field(
            "fail-detect-option",
            payload["fail-detect-option"],
            VALID_BODY_FAIL_DETECT_OPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-alert-method" in payload:
        is_valid, error = _validate_enum_field(
            "fail-alert-method",
            payload["fail-alert-method"],
            VALID_BODY_FAIL_ALERT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fail-action-on-extender" in payload:
        is_valid, error = _validate_enum_field(
            "fail-action-on-extender",
            payload["fail-action-on-extender"],
            VALID_BODY_FAIL_ACTION_ON_EXTENDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pppoe-egress-cos" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-egress-cos",
            payload["pppoe-egress-cos"],
            VALID_BODY_PPPOE_EGRESS_COS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pppoe-unnumbered-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "pppoe-unnumbered-negotiate",
            payload["pppoe-unnumbered-negotiate"],
            VALID_BODY_PPPOE_UNNUMBERED_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multilink" in payload:
        is_valid, error = _validate_enum_field(
            "multilink",
            payload["multilink"],
            VALID_BODY_MULTILINK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "defaultgw" in payload:
        is_valid, error = _validate_enum_field(
            "defaultgw",
            payload["defaultgw"],
            VALID_BODY_DEFAULTGW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-server-override" in payload:
        is_valid, error = _validate_enum_field(
            "dns-server-override",
            payload["dns-server-override"],
            VALID_BODY_DNS_SERVER_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-server-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "dns-server-protocol",
            payload["dns-server-protocol"],
            VALID_BODY_DNS_SERVER_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "auth-type",
            payload["auth-type"],
            VALID_BODY_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pptp-client" in payload:
        is_valid, error = _validate_enum_field(
            "pptp-client",
            payload["pptp-client"],
            VALID_BODY_PPTP_CLIENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pptp-auth-type" in payload:
        is_valid, error = _validate_enum_field(
            "pptp-auth-type",
            payload["pptp-auth-type"],
            VALID_BODY_PPTP_AUTH_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "arpforward" in payload:
        is_valid, error = _validate_enum_field(
            "arpforward",
            payload["arpforward"],
            VALID_BODY_ARPFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ndiscforward" in payload:
        is_valid, error = _validate_enum_field(
            "ndiscforward",
            payload["ndiscforward"],
            VALID_BODY_NDISCFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-forward" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-forward",
            payload["broadcast-forward"],
            VALID_BODY_BROADCAST_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bfd" in payload:
        is_valid, error = _validate_enum_field(
            "bfd",
            payload["bfd"],
            VALID_BODY_BFD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l2forward" in payload:
        is_valid, error = _validate_enum_field(
            "l2forward",
            payload["l2forward"],
            VALID_BODY_L2FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "icmp-send-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "icmp-send-redirect",
            payload["icmp-send-redirect"],
            VALID_BODY_ICMP_SEND_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "icmp-accept-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "icmp-accept-redirect",
            payload["icmp-accept-redirect"],
            VALID_BODY_ICMP_ACCEPT_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlanforward" in payload:
        is_valid, error = _validate_enum_field(
            "vlanforward",
            payload["vlanforward"],
            VALID_BODY_VLANFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "stpforward" in payload:
        is_valid, error = _validate_enum_field(
            "stpforward",
            payload["stpforward"],
            VALID_BODY_STPFORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "stpforward-mode" in payload:
        is_valid, error = _validate_enum_field(
            "stpforward-mode",
            payload["stpforward-mode"],
            VALID_BODY_STPFORWARD_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ips-sniffer-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ips-sniffer-mode",
            payload["ips-sniffer-mode"],
            VALID_BODY_IPS_SNIFFER_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ident-accept" in payload:
        is_valid, error = _validate_enum_field(
            "ident-accept",
            payload["ident-accept"],
            VALID_BODY_IDENT_ACCEPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipmac" in payload:
        is_valid, error = _validate_enum_field(
            "ipmac",
            payload["ipmac"],
            VALID_BODY_IPMAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "subst" in payload:
        is_valid, error = _validate_enum_field(
            "subst",
            payload["subst"],
            VALID_BODY_SUBST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "speed" in payload:
        is_valid, error = _validate_enum_field(
            "speed",
            payload["speed"],
            VALID_BODY_SPEED,
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
    if "netbios-forward" in payload:
        is_valid, error = _validate_enum_field(
            "netbios-forward",
            payload["netbios-forward"],
            VALID_BODY_NETBIOS_FORWARD,
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
    if "dedicated-to" in payload:
        is_valid, error = _validate_enum_field(
            "dedicated-to",
            payload["dedicated-to"],
            VALID_BODY_DEDICATED_TO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wccp" in payload:
        is_valid, error = _validate_enum_field(
            "wccp",
            payload["wccp"],
            VALID_BODY_WCCP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "netflow-sampler" in payload:
        is_valid, error = _validate_enum_field(
            "netflow-sampler",
            payload["netflow-sampler"],
            VALID_BODY_NETFLOW_SAMPLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sflow-sampler" in payload:
        is_valid, error = _validate_enum_field(
            "sflow-sampler",
            payload["sflow-sampler"],
            VALID_BODY_SFLOW_SAMPLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "drop-fragment" in payload:
        is_valid, error = _validate_enum_field(
            "drop-fragment",
            payload["drop-fragment"],
            VALID_BODY_DROP_FRAGMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-check" in payload:
        is_valid, error = _validate_enum_field(
            "src-check",
            payload["src-check"],
            VALID_BODY_SRC_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sample-direction" in payload:
        is_valid, error = _validate_enum_field(
            "sample-direction",
            payload["sample-direction"],
            VALID_BODY_SAMPLE_DIRECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "explicit-web-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "explicit-web-proxy",
            payload["explicit-web-proxy"],
            VALID_BODY_EXPLICIT_WEB_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "explicit-ftp-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "explicit-ftp-proxy",
            payload["explicit-ftp-proxy"],
            VALID_BODY_EXPLICIT_FTP_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-captive-portal" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-captive-portal",
            payload["proxy-captive-portal"],
            VALID_BODY_PROXY_CAPTIVE_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external" in payload:
        is_valid, error = _validate_enum_field(
            "external",
            payload["external"],
            VALID_BODY_EXTERNAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mtu-override" in payload:
        is_valid, error = _validate_enum_field(
            "mtu-override",
            payload["mtu-override"],
            VALID_BODY_MTU_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-protocol" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-protocol",
            payload["vlan-protocol"],
            VALID_BODY_VLAN_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lacp-mode" in payload:
        is_valid, error = _validate_enum_field(
            "lacp-mode",
            payload["lacp-mode"],
            VALID_BODY_LACP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lacp-ha-secondary" in payload:
        is_valid, error = _validate_enum_field(
            "lacp-ha-secondary",
            payload["lacp-ha-secondary"],
            VALID_BODY_LACP_HA_SECONDARY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "system-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "system-id-type",
            payload["system-id-type"],
            VALID_BODY_SYSTEM_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lacp-speed" in payload:
        is_valid, error = _validate_enum_field(
            "lacp-speed",
            payload["lacp-speed"],
            VALID_BODY_LACP_SPEED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "min-links-down" in payload:
        is_valid, error = _validate_enum_field(
            "min-links-down",
            payload["min-links-down"],
            VALID_BODY_MIN_LINKS_DOWN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "algorithm",
            payload["algorithm"],
            VALID_BODY_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "aggregate-type" in payload:
        is_valid, error = _validate_enum_field(
            "aggregate-type",
            payload["aggregate-type"],
            VALID_BODY_AGGREGATE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "priority-override" in payload:
        is_valid, error = _validate_enum_field(
            "priority-override",
            payload["priority-override"],
            VALID_BODY_PRIORITY_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mode" in payload:
        is_valid, error = _validate_enum_field(
            "security-mode",
            payload["security-mode"],
            VALID_BODY_SECURITY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "security-mac-auth-bypass",
            payload["security-mac-auth-bypass"],
            VALID_BODY_SECURITY_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security-ip-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "security-ip-auth-bypass",
            payload["security-ip-auth-bypass"],
            VALID_BODY_SECURITY_IP_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-identification" in payload:
        is_valid, error = _validate_enum_field(
            "device-identification",
            payload["device-identification"],
            VALID_BODY_DEVICE_IDENTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "exclude-signatures" in payload:
        is_valid, error = _validate_enum_field(
            "exclude-signatures",
            payload["exclude-signatures"],
            VALID_BODY_EXCLUDE_SIGNATURES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "device-user-identification" in payload:
        is_valid, error = _validate_enum_field(
            "device-user-identification",
            payload["device-user-identification"],
            VALID_BODY_DEVICE_USER_IDENTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lldp-reception" in payload:
        is_valid, error = _validate_enum_field(
            "lldp-reception",
            payload["lldp-reception"],
            VALID_BODY_LLDP_RECEPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "lldp-transmission" in payload:
        is_valid, error = _validate_enum_field(
            "lldp-transmission",
            payload["lldp-transmission"],
            VALID_BODY_LLDP_TRANSMISSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "monitor-bandwidth" in payload:
        is_valid, error = _validate_enum_field(
            "monitor-bandwidth",
            payload["monitor-bandwidth"],
            VALID_BODY_MONITOR_BANDWIDTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vrrp-virtual-mac" in payload:
        is_valid, error = _validate_enum_field(
            "vrrp-virtual-mac",
            payload["vrrp-virtual-mac"],
            VALID_BODY_VRRP_VIRTUAL_MAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "role" in payload:
        is_valid, error = _validate_enum_field(
            "role",
            payload["role"],
            VALID_BODY_ROLE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "secondary-IP" in payload:
        is_valid, error = _validate_enum_field(
            "secondary-IP",
            payload["secondary-IP"],
            VALID_BODY_SECONDARY_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "preserve-session-route" in payload:
        is_valid, error = _validate_enum_field(
            "preserve-session-route",
            payload["preserve-session-route"],
            VALID_BODY_PRESERVE_SESSION_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-auth-extension-device" in payload:
        is_valid, error = _validate_enum_field(
            "auto-auth-extension-device",
            payload["auto-auth-extension-device"],
            VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ap-discover" in payload:
        is_valid, error = _validate_enum_field(
            "ap-discover",
            payload["ap-discover"],
            VALID_BODY_AP_DISCOVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortilink-neighbor-detect" in payload:
        is_valid, error = _validate_enum_field(
            "fortilink-neighbor-detect",
            payload["fortilink-neighbor-detect"],
            VALID_BODY_FORTILINK_NEIGHBOR_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-managed-by-fortiipam" in payload:
        is_valid, error = _validate_enum_field(
            "ip-managed-by-fortiipam",
            payload["ip-managed-by-fortiipam"],
            VALID_BODY_IP_MANAGED_BY_FORTIIPAM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "managed-subnetwork-size" in payload:
        is_valid, error = _validate_enum_field(
            "managed-subnetwork-size",
            payload["managed-subnetwork-size"],
            VALID_BODY_MANAGED_SUBNETWORK_SIZE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortilink-split-interface" in payload:
        is_valid, error = _validate_enum_field(
            "fortilink-split-interface",
            payload["fortilink-split-interface"],
            VALID_BODY_FORTILINK_SPLIT_INTERFACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-access-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-access-vlan",
            payload["switch-controller-access-vlan"],
            VALID_BODY_SWITCH_CONTROLLER_ACCESS_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-rspan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-rspan-mode",
            payload["switch-controller-rspan-mode"],
            VALID_BODY_SWITCH_CONTROLLER_RSPAN_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-netflow-collect" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-netflow-collect",
            payload["switch-controller-netflow-collect"],
            VALID_BODY_SWITCH_CONTROLLER_NETFLOW_COLLECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-igmp-snooping" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-igmp-snooping",
            payload["switch-controller-igmp-snooping"],
            VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-igmp-snooping-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-igmp-snooping-proxy",
            payload["switch-controller-igmp-snooping-proxy"],
            VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-igmp-snooping-fast-leave" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-igmp-snooping-fast-leave",
            payload["switch-controller-igmp-snooping-fast-leave"],
            VALID_BODY_SWITCH_CONTROLLER_IGMP_SNOOPING_FAST_LEAVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-dhcp-snooping" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-dhcp-snooping",
            payload["switch-controller-dhcp-snooping"],
            VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-dhcp-snooping-verify-mac" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-dhcp-snooping-verify-mac",
            payload["switch-controller-dhcp-snooping-verify-mac"],
            VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_VERIFY_MAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-dhcp-snooping-option82" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-dhcp-snooping-option82",
            payload["switch-controller-dhcp-snooping-option82"],
            VALID_BODY_SWITCH_CONTROLLER_DHCP_SNOOPING_OPTION82,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-arp-inspection" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-arp-inspection",
            payload["switch-controller-arp-inspection"],
            VALID_BODY_SWITCH_CONTROLLER_ARP_INSPECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-feature" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-feature",
            payload["switch-controller-feature"],
            VALID_BODY_SWITCH_CONTROLLER_FEATURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-iot-scanning" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-iot-scanning",
            payload["switch-controller-iot-scanning"],
            VALID_BODY_SWITCH_CONTROLLER_IOT_SCANNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-offload" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-offload",
            payload["switch-controller-offload"],
            VALID_BODY_SWITCH_CONTROLLER_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller-offload-gw" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller-offload-gw",
            payload["switch-controller-offload-gw"],
            VALID_BODY_SWITCH_CONTROLLER_OFFLOAD_GW,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-supplicant" in payload:
        is_valid, error = _validate_enum_field(
            "eap-supplicant",
            payload["eap-supplicant"],
            VALID_BODY_EAP_SUPPLICANT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-method" in payload:
        is_valid, error = _validate_enum_field(
            "eap-method",
            payload["eap-method"],
            VALID_BODY_EAP_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-purdue-level" in payload:
        is_valid, error = _validate_enum_field(
            "default-purdue-level",
            payload["default-purdue-level"],
            VALID_BODY_DEFAULT_PURDUE_LEVEL,
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
    "endpoint": "system/interface",
    "category": "cmdb",
    "api_path": "system/interface",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure interfaces.",
    "total_fields": 222,
    "required_fields_count": 3,
    "fields_with_defaults_count": 205,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
