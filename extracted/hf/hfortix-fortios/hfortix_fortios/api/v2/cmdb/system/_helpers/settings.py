"""Validation helpers for system/settings - Auto-generated"""

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
    "manageip",  # Transparent mode IPv4 management IP address and netmask.
    "device",  # Interface to use for management access for NAT mode.
    "dhcp-proxy-interface",  # Specify outgoing interface to reach server.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "vdom-type": "traffic",
    "lan-extension-controller-addr": "",
    "lan-extension-controller-port": 5246,
    "opmode": "nat",
    "ngfw-mode": "profile-based",
    "http-external-dest": "fortiweb",
    "firewall-session-dirty": "check-all",
    "manageip": "",
    "gateway": "0.0.0.0",
    "ip": "0.0.0.0 0.0.0.0",
    "manageip6": "::/0",
    "gateway6": "::",
    "ip6": "::/0",
    "device": "",
    "bfd": "disable",
    "bfd-desired-min-tx": 250,
    "bfd-required-min-rx": 250,
    "bfd-detect-mult": 3,
    "bfd-dont-enforce-src-port": "disable",
    "utf8-spam-tagging": "enable",
    "wccp-cache-engine": "disable",
    "vpn-stats-log": "ipsec pptp l2tp ssl",
    "vpn-stats-period": 600,
    "v4-ecmp-mode": "source-ip-based",
    "mac-ttl": 300,
    "fw-session-hairpin": "disable",
    "prp-trailer-action": "disable",
    "snat-hairpin-traffic": "enable",
    "dhcp-proxy": "disable",
    "dhcp-proxy-interface-select-method": "auto",
    "dhcp-proxy-interface": "",
    "dhcp-proxy-vrf-select": 0,
    "dhcp-server-ip": "",
    "dhcp6-server-ip": "",
    "central-nat": "disable",
    "lldp-reception": "global",
    "lldp-transmission": "global",
    "link-down-access": "enable",
    "nat46-generate-ipv6-fragment-header": "disable",
    "nat46-force-ipv4-packet-forwarding": "disable",
    "nat64-force-ipv6-packet-forwarding": "enable",
    "detect-unknown-esp": "enable",
    "intree-ses-best-route": "disable",
    "auxiliary-session": "disable",
    "asymroute": "disable",
    "asymroute-icmp": "disable",
    "tcp-session-without-syn": "disable",
    "ses-denied-traffic": "disable",
    "ses-denied-multicast-traffic": "disable",
    "strict-src-check": "disable",
    "allow-linkdown-path": "disable",
    "asymroute6": "disable",
    "asymroute6-icmp": "disable",
    "sctp-session-without-init": "disable",
    "sip-expectation": "disable",
    "sip-nat-trace": "enable",
    "h323-direct-model": "disable",
    "status": "enable",
    "sip-tcp-port": 5060,
    "sip-udp-port": 5060,
    "sip-ssl-port": 5061,
    "sccp-port": 2000,
    "multicast-forward": "enable",
    "multicast-ttl-notchange": "disable",
    "multicast-skip-policy": "disable",
    "allow-subnet-overlap": "disable",
    "deny-tcp-with-icmp": "disable",
    "ecmp-max-paths": 255,
    "discovered-device-timeout": 28,
    "email-portal-check-dns": "enable",
    "default-voip-alg-mode": "proxy-based",
    "gui-icap": "disable",
    "gui-implicit-policy": "enable",
    "gui-dns-database": "disable",
    "gui-load-balance": "disable",
    "gui-multicast-policy": "disable",
    "gui-dos-policy": "enable",
    "gui-object-colors": "enable",
    "gui-route-tag-address-creation": "disable",
    "gui-voip-profile": "disable",
    "gui-ap-profile": "enable",
    "gui-security-profile-group": "disable",
    "gui-local-in-policy": "disable",
    "gui-wanopt-cache": "disable",
    "gui-explicit-proxy": "disable",
    "gui-dynamic-routing": "enable",
    "gui-sslvpn-personal-bookmarks": "disable",
    "gui-sslvpn-realms": "disable",
    "gui-policy-based-ipsec": "disable",
    "gui-threat-weight": "enable",
    "gui-spamfilter": "disable",
    "gui-file-filter": "enable",
    "gui-application-control": "enable",
    "gui-ips": "enable",
    "gui-dhcp-advanced": "enable",
    "gui-vpn": "enable",
    "gui-sslvpn": "disable",
    "gui-wireless-controller": "enable",
    "gui-advanced-wireless-features": "disable",
    "gui-switch-controller": "enable",
    "gui-fortiap-split-tunneling": "disable",
    "gui-webfilter-advanced": "disable",
    "gui-traffic-shaping": "enable",
    "gui-wan-load-balancing": "enable",
    "gui-antivirus": "enable",
    "gui-webfilter": "enable",
    "gui-videofilter": "enable",
    "gui-dnsfilter": "enable",
    "gui-waf-profile": "disable",
    "gui-dlp-profile": "disable",
    "gui-dlp-advanced": "disable",
    "gui-virtual-patch-profile": "disable",
    "gui-casb": "disable",
    "gui-fortiextender-controller": "disable",
    "gui-advanced-policy": "disable",
    "gui-allow-unnamed-policy": "disable",
    "gui-email-collection": "disable",
    "gui-multiple-interface-policy": "disable",
    "gui-policy-disclaimer": "disable",
    "gui-ztna": "disable",
    "gui-ot": "disable",
    "gui-dynamic-device-os-id": "disable",
    "gui-gtp": "enable",
    "location-id": "0.0.0.0",
    "ike-session-resume": "disable",
    "ike-quick-crash-detect": "disable",
    "ike-dn-format": "with-space",
    "ike-port": 500,
    "ike-tcp-port": 443,
    "ike-policy-route": "disable",
    "ike-detailed-event-logs": "disable",
    "block-land-attack": "disable",
    "default-app-port-as-service": "enable",
    "fqdn-session-check": "disable",
    "ext-resource-session-check": "disable",
    "dyn-addr-session-check": "disable",
    "default-policy-expiry-days": 30,
    "gui-enforce-change-summary": "require",
    "internet-service-database-cache": "disable",
    "internet-service-app-ctrl-size": 32768,
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
    "comments": "var-string",  # VDOM comments.
    "vdom-type": "option",  # Vdom type (traffic, lan-extension or admin).
    "lan-extension-controller-addr": "string",  # Controller IP address or FQDN to connect.
    "lan-extension-controller-port": "integer",  # Controller port to connect.
    "opmode": "option",  # Firewall operation mode (NAT or Transparent).
    "ngfw-mode": "option",  # Next Generation Firewall (NGFW) mode.
    "http-external-dest": "option",  # Offload HTTP traffic to FortiWeb or FortiCache.
    "firewall-session-dirty": "option",  # Select how to manage sessions affected by firewall policy co
    "manageip": "user",  # Transparent mode IPv4 management IP address and netmask.
    "gateway": "ipv4-address",  # Transparent mode IPv4 default gateway IP address.
    "ip": "ipv4-classnet-host",  # IP address and netmask.
    "manageip6": "ipv6-prefix",  # Transparent mode IPv6 management IP address and netmask.
    "gateway6": "ipv6-address",  # Transparent mode IPv6 default gateway IP address.
    "ip6": "ipv6-prefix",  # IPv6 address prefix for NAT mode.
    "device": "string",  # Interface to use for management access for NAT mode.
    "bfd": "option",  # Enable/disable Bi-directional Forwarding Detection (BFD) on 
    "bfd-desired-min-tx": "integer",  # BFD desired minimal transmit interval (1 - 100000 ms, defaul
    "bfd-required-min-rx": "integer",  # BFD required minimal receive interval (1 - 100000 ms, defaul
    "bfd-detect-mult": "integer",  # BFD detection multiplier (1 - 50, default = 3).
    "bfd-dont-enforce-src-port": "option",  # Enable to not enforce verifying the source port of BFD Packe
    "utf8-spam-tagging": "option",  # Enable/disable converting antispam tags to UTF-8 for better 
    "wccp-cache-engine": "option",  # Enable/disable WCCP cache engine.
    "vpn-stats-log": "option",  # Enable/disable periodic VPN log statistics for one or more t
    "vpn-stats-period": "integer",  # Period to send VPN log statistics (0 or 60 - 86400 sec).
    "v4-ecmp-mode": "option",  # IPv4 Equal-cost multi-path (ECMP) routing and load balancing
    "mac-ttl": "integer",  # Duration of MAC addresses in Transparent mode (300 - 8640000
    "fw-session-hairpin": "option",  # Enable/disable checking for a matching policy each time hair
    "prp-trailer-action": "option",  # Enable/disable action to take on PRP trailer.
    "snat-hairpin-traffic": "option",  # Enable/disable source NAT (SNAT) for VIP hairpin traffic.
    "dhcp-proxy": "option",  # Enable/disable the DHCP Proxy.
    "dhcp-proxy-interface-select-method": "option",  # Specify how to select outgoing interface to reach server.
    "dhcp-proxy-interface": "string",  # Specify outgoing interface to reach server.
    "dhcp-proxy-vrf-select": "integer",  # VRF ID used for connection to server.
    "dhcp-server-ip": "user",  # DHCP Server IPv4 address.
    "dhcp6-server-ip": "user",  # DHCPv6 server IPv6 address.
    "central-nat": "option",  # Enable/disable central NAT.
    "gui-default-policy-columns": "string",  # Default columns to display for policy lists on GUI.
    "lldp-reception": "option",  # Enable/disable Link Layer Discovery Protocol (LLDP) receptio
    "lldp-transmission": "option",  # Enable/disable Link Layer Discovery Protocol (LLDP) transmis
    "link-down-access": "option",  # Enable/disable link down access traffic.
    "nat46-generate-ipv6-fragment-header": "option",  # Enable/disable NAT46 IPv6 fragment header generation.
    "nat46-force-ipv4-packet-forwarding": "option",  # Enable/disable mandatory IPv4 packet forwarding in NAT46.
    "nat64-force-ipv6-packet-forwarding": "option",  # Enable/disable mandatory IPv6 packet forwarding in NAT64.
    "detect-unknown-esp": "option",  # Enable/disable detection of unknown ESP packets (default = e
    "intree-ses-best-route": "option",  # Force the intree session to always use the best route.
    "auxiliary-session": "option",  # Enable/disable auxiliary session.
    "asymroute": "option",  # Enable/disable IPv4 asymmetric routing.
    "asymroute-icmp": "option",  # Enable/disable ICMP asymmetric routing.
    "tcp-session-without-syn": "option",  # Enable/disable allowing TCP session without SYN flags.
    "ses-denied-traffic": "option",  # Enable/disable including denied session in the session table
    "ses-denied-multicast-traffic": "option",  # Enable/disable including denied multicast session in the ses
    "strict-src-check": "option",  # Enable/disable strict source verification.
    "allow-linkdown-path": "option",  # Enable/disable link down path.
    "asymroute6": "option",  # Enable/disable asymmetric IPv6 routing.
    "asymroute6-icmp": "option",  # Enable/disable asymmetric ICMPv6 routing.
    "sctp-session-without-init": "option",  # Enable/disable SCTP session creation without SCTP INIT.
    "sip-expectation": "option",  # Enable/disable the SIP kernel session helper to create an ex
    "sip-nat-trace": "option",  # Enable/disable recording the original SIP source IP address 
    "h323-direct-model": "option",  # Enable/disable H323 direct model.
    "status": "option",  # Enable/disable this VDOM.
    "sip-tcp-port": "integer",  # TCP port the SIP proxy monitors for SIP traffic (0 - 65535, 
    "sip-udp-port": "integer",  # UDP port the SIP proxy monitors for SIP traffic (0 - 65535, 
    "sip-ssl-port": "integer",  # TCP port the SIP proxy monitors for SIP SSL/TLS traffic (0 -
    "sccp-port": "integer",  # TCP port the SCCP proxy monitors for SCCP traffic (0 - 65535
    "multicast-forward": "option",  # Enable/disable multicast forwarding.
    "multicast-ttl-notchange": "option",  # Enable/disable preventing the FortiGate from changing the TT
    "multicast-skip-policy": "option",  # Enable/disable allowing multicast traffic through the FortiG
    "allow-subnet-overlap": "option",  # Enable/disable allowing interface subnets to use overlapping
    "deny-tcp-with-icmp": "option",  # Enable/disable denying TCP by sending an ICMP communication 
    "ecmp-max-paths": "integer",  # Maximum number of Equal Cost Multi-Path (ECMP) next-hops. Se
    "discovered-device-timeout": "integer",  # Timeout for discovered devices (1 - 365 days, default = 28).
    "email-portal-check-dns": "option",  # Enable/disable using DNS to validate email addresses collect
    "default-voip-alg-mode": "option",  # Configure how the FortiGate handles VoIP traffic when a poli
    "gui-icap": "option",  # Enable/disable ICAP on the GUI.
    "gui-implicit-policy": "option",  # Enable/disable implicit firewall policies on the GUI.
    "gui-dns-database": "option",  # Enable/disable DNS database settings on the GUI.
    "gui-load-balance": "option",  # Enable/disable server load balancing on the GUI.
    "gui-multicast-policy": "option",  # Enable/disable multicast firewall policies on the GUI.
    "gui-dos-policy": "option",  # Enable/disable DoS policies on the GUI.
    "gui-object-colors": "option",  # Enable/disable object colors on the GUI.
    "gui-route-tag-address-creation": "option",  # Enable/disable route-tag addresses on the GUI.
    "gui-voip-profile": "option",  # Enable/disable VoIP profiles on the GUI.
    "gui-ap-profile": "option",  # Enable/disable FortiAP profiles on the GUI.
    "gui-security-profile-group": "option",  # Enable/disable Security Profile Groups on the GUI.
    "gui-local-in-policy": "option",  # Enable/disable Local-In policies on the GUI.
    "gui-wanopt-cache": "option",  # Enable/disable WAN Optimization and Web Caching on the GUI.
    "gui-explicit-proxy": "option",  # Enable/disable the explicit proxy on the GUI.
    "gui-dynamic-routing": "option",  # Enable/disable dynamic routing on the GUI.
    "gui-sslvpn-personal-bookmarks": "option",  # Enable/disable SSL-VPN personal bookmark management on the G
    "gui-sslvpn-realms": "option",  # Enable/disable SSL-VPN realms on the GUI.
    "gui-policy-based-ipsec": "option",  # Enable/disable policy-based IPsec VPN on the GUI.
    "gui-threat-weight": "option",  # Enable/disable threat weight on the GUI.
    "gui-spamfilter": "option",  # Enable/disable Antispam on the GUI.
    "gui-file-filter": "option",  # Enable/disable File-filter on the GUI.
    "gui-application-control": "option",  # Enable/disable application control on the GUI.
    "gui-ips": "option",  # Enable/disable IPS on the GUI.
    "gui-dhcp-advanced": "option",  # Enable/disable advanced DHCP options on the GUI.
    "gui-vpn": "option",  # Enable/disable IPsec VPN settings pages on the GUI.
    "gui-sslvpn": "option",  # Enable/disable SSL-VPN settings pages on the GUI.
    "gui-wireless-controller": "option",  # Enable/disable the wireless controller on the GUI.
    "gui-advanced-wireless-features": "option",  # Enable/disable advanced wireless features in GUI.
    "gui-switch-controller": "option",  # Enable/disable the switch controller on the GUI.
    "gui-fortiap-split-tunneling": "option",  # Enable/disable FortiAP split tunneling on the GUI.
    "gui-webfilter-advanced": "option",  # Enable/disable advanced web filtering on the GUI.
    "gui-traffic-shaping": "option",  # Enable/disable traffic shaping on the GUI.
    "gui-wan-load-balancing": "option",  # Enable/disable SD-WAN on the GUI.
    "gui-antivirus": "option",  # Enable/disable AntiVirus on the GUI.
    "gui-webfilter": "option",  # Enable/disable Web filtering on the GUI.
    "gui-videofilter": "option",  # Enable/disable Video filtering on the GUI.
    "gui-dnsfilter": "option",  # Enable/disable DNS Filtering on the GUI.
    "gui-waf-profile": "option",  # Enable/disable Web Application Firewall on the GUI.
    "gui-dlp-profile": "option",  # Enable/disable Data Loss Prevention on the GUI.
    "gui-dlp-advanced": "option",  # Enable/disable Show advanced DLP expressions on the GUI.
    "gui-virtual-patch-profile": "option",  # Enable/disable Virtual Patching on the GUI.
    "gui-casb": "option",  # Enable/disable Inline-CASB on the GUI.
    "gui-fortiextender-controller": "option",  # Enable/disable FortiExtender on the GUI.
    "gui-advanced-policy": "option",  # Enable/disable advanced policy configuration on the GUI.
    "gui-allow-unnamed-policy": "option",  # Enable/disable the requirement for policy naming on the GUI.
    "gui-email-collection": "option",  # Enable/disable email collection on the GUI.
    "gui-multiple-interface-policy": "option",  # Enable/disable adding multiple interfaces to a policy on the
    "gui-policy-disclaimer": "option",  # Enable/disable policy disclaimer on the GUI.
    "gui-ztna": "option",  # Enable/disable Zero Trust Network Access features on the GUI
    "gui-ot": "option",  # Enable/disable Operational technology features on the GUI.
    "gui-dynamic-device-os-id": "option",  # Enable/disable Create dynamic addresses to manage known devi
    "gui-gtp": "option",  # Enable/disable Manage general radio packet service (GPRS) pr
    "location-id": "ipv4-address",  # Local location ID in the form of an IPv4 address.
    "ike-session-resume": "option",  # Enable/disable IKEv2 session resumption (RFC 5723).
    "ike-quick-crash-detect": "option",  # Enable/disable IKE quick crash detection (RFC 6290).
    "ike-dn-format": "option",  # Configure IKE ASN.1 Distinguished Name format conventions.
    "ike-port": "integer",  # UDP port for IKE/IPsec traffic (default 500).
    "ike-tcp-port": "integer",  # TCP port for IKE/IPsec traffic (default 443).
    "ike-policy-route": "option",  # Enable/disable IKE Policy Based Routing (PBR).
    "ike-detailed-event-logs": "option",  # Enable/disable detail log for IKE events.
    "block-land-attack": "option",  # Enable/disable blocking of land attacks.
    "default-app-port-as-service": "option",  # Enable/disable policy service enforcement based on applicati
    "fqdn-session-check": "option",  # Enable/disable dirty session check caused by FQDN updates.
    "ext-resource-session-check": "option",  # Enable/disable dirty session check caused by external resour
    "dyn-addr-session-check": "option",  # Enable/disable dirty session check caused by dynamic address
    "default-policy-expiry-days": "integer",  # Default policy expiry in days (0 - 365 days, default = 30).
    "gui-enforce-change-summary": "option",  # Enforce change summaries for select tables in the GUI.
    "internet-service-database-cache": "option",  # Enable/disable Internet Service database caching.
    "internet-service-app-ctrl-size": "integer",  # Maximum number of tuple entries (protocol, port, IP address,
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "comments": "VDOM comments.",
    "vdom-type": "Vdom type (traffic, lan-extension or admin).",
    "lan-extension-controller-addr": "Controller IP address or FQDN to connect.",
    "lan-extension-controller-port": "Controller port to connect.",
    "opmode": "Firewall operation mode (NAT or Transparent).",
    "ngfw-mode": "Next Generation Firewall (NGFW) mode.",
    "http-external-dest": "Offload HTTP traffic to FortiWeb or FortiCache.",
    "firewall-session-dirty": "Select how to manage sessions affected by firewall policy configuration changes.",
    "manageip": "Transparent mode IPv4 management IP address and netmask.",
    "gateway": "Transparent mode IPv4 default gateway IP address.",
    "ip": "IP address and netmask.",
    "manageip6": "Transparent mode IPv6 management IP address and netmask.",
    "gateway6": "Transparent mode IPv6 default gateway IP address.",
    "ip6": "IPv6 address prefix for NAT mode.",
    "device": "Interface to use for management access for NAT mode.",
    "bfd": "Enable/disable Bi-directional Forwarding Detection (BFD) on all interfaces.",
    "bfd-desired-min-tx": "BFD desired minimal transmit interval (1 - 100000 ms, default = 250).",
    "bfd-required-min-rx": "BFD required minimal receive interval (1 - 100000 ms, default = 250).",
    "bfd-detect-mult": "BFD detection multiplier (1 - 50, default = 3).",
    "bfd-dont-enforce-src-port": "Enable to not enforce verifying the source port of BFD Packets.",
    "utf8-spam-tagging": "Enable/disable converting antispam tags to UTF-8 for better non-ASCII character support.",
    "wccp-cache-engine": "Enable/disable WCCP cache engine.",
    "vpn-stats-log": "Enable/disable periodic VPN log statistics for one or more types of VPN. Separate names with a space.",
    "vpn-stats-period": "Period to send VPN log statistics (0 or 60 - 86400 sec).",
    "v4-ecmp-mode": "IPv4 Equal-cost multi-path (ECMP) routing and load balancing mode.",
    "mac-ttl": "Duration of MAC addresses in Transparent mode (300 - 8640000 sec, default = 300).",
    "fw-session-hairpin": "Enable/disable checking for a matching policy each time hairpin traffic goes through the FortiGate.",
    "prp-trailer-action": "Enable/disable action to take on PRP trailer.",
    "snat-hairpin-traffic": "Enable/disable source NAT (SNAT) for VIP hairpin traffic.",
    "dhcp-proxy": "Enable/disable the DHCP Proxy.",
    "dhcp-proxy-interface-select-method": "Specify how to select outgoing interface to reach server.",
    "dhcp-proxy-interface": "Specify outgoing interface to reach server.",
    "dhcp-proxy-vrf-select": "VRF ID used for connection to server.",
    "dhcp-server-ip": "DHCP Server IPv4 address.",
    "dhcp6-server-ip": "DHCPv6 server IPv6 address.",
    "central-nat": "Enable/disable central NAT.",
    "gui-default-policy-columns": "Default columns to display for policy lists on GUI.",
    "lldp-reception": "Enable/disable Link Layer Discovery Protocol (LLDP) reception for this VDOM or apply global settings to this VDOM.",
    "lldp-transmission": "Enable/disable Link Layer Discovery Protocol (LLDP) transmission for this VDOM or apply global settings to this VDOM.",
    "link-down-access": "Enable/disable link down access traffic.",
    "nat46-generate-ipv6-fragment-header": "Enable/disable NAT46 IPv6 fragment header generation.",
    "nat46-force-ipv4-packet-forwarding": "Enable/disable mandatory IPv4 packet forwarding in NAT46.",
    "nat64-force-ipv6-packet-forwarding": "Enable/disable mandatory IPv6 packet forwarding in NAT64.",
    "detect-unknown-esp": "Enable/disable detection of unknown ESP packets (default = enable).",
    "intree-ses-best-route": "Force the intree session to always use the best route.",
    "auxiliary-session": "Enable/disable auxiliary session.",
    "asymroute": "Enable/disable IPv4 asymmetric routing.",
    "asymroute-icmp": "Enable/disable ICMP asymmetric routing.",
    "tcp-session-without-syn": "Enable/disable allowing TCP session without SYN flags.",
    "ses-denied-traffic": "Enable/disable including denied session in the session table.",
    "ses-denied-multicast-traffic": "Enable/disable including denied multicast session in the session table.",
    "strict-src-check": "Enable/disable strict source verification.",
    "allow-linkdown-path": "Enable/disable link down path.",
    "asymroute6": "Enable/disable asymmetric IPv6 routing.",
    "asymroute6-icmp": "Enable/disable asymmetric ICMPv6 routing.",
    "sctp-session-without-init": "Enable/disable SCTP session creation without SCTP INIT.",
    "sip-expectation": "Enable/disable the SIP kernel session helper to create an expectation for port 5060.",
    "sip-nat-trace": "Enable/disable recording the original SIP source IP address when NAT is used.",
    "h323-direct-model": "Enable/disable H323 direct model.",
    "status": "Enable/disable this VDOM.",
    "sip-tcp-port": "TCP port the SIP proxy monitors for SIP traffic (0 - 65535, default = 5060).",
    "sip-udp-port": "UDP port the SIP proxy monitors for SIP traffic (0 - 65535, default = 5060).",
    "sip-ssl-port": "TCP port the SIP proxy monitors for SIP SSL/TLS traffic (0 - 65535, default = 5061).",
    "sccp-port": "TCP port the SCCP proxy monitors for SCCP traffic (0 - 65535, default = 2000).",
    "multicast-forward": "Enable/disable multicast forwarding.",
    "multicast-ttl-notchange": "Enable/disable preventing the FortiGate from changing the TTL for forwarded multicast packets.",
    "multicast-skip-policy": "Enable/disable allowing multicast traffic through the FortiGate without a policy check.",
    "allow-subnet-overlap": "Enable/disable allowing interface subnets to use overlapping IP addresses.",
    "deny-tcp-with-icmp": "Enable/disable denying TCP by sending an ICMP communication prohibited packet.",
    "ecmp-max-paths": "Maximum number of Equal Cost Multi-Path (ECMP) next-hops. Set to 1 to disable ECMP routing (1 - 255, default = 255).",
    "discovered-device-timeout": "Timeout for discovered devices (1 - 365 days, default = 28).",
    "email-portal-check-dns": "Enable/disable using DNS to validate email addresses collected by a captive portal.",
    "default-voip-alg-mode": "Configure how the FortiGate handles VoIP traffic when a policy that accepts the traffic doesn't include a VoIP profile.",
    "gui-icap": "Enable/disable ICAP on the GUI.",
    "gui-implicit-policy": "Enable/disable implicit firewall policies on the GUI.",
    "gui-dns-database": "Enable/disable DNS database settings on the GUI.",
    "gui-load-balance": "Enable/disable server load balancing on the GUI.",
    "gui-multicast-policy": "Enable/disable multicast firewall policies on the GUI.",
    "gui-dos-policy": "Enable/disable DoS policies on the GUI.",
    "gui-object-colors": "Enable/disable object colors on the GUI.",
    "gui-route-tag-address-creation": "Enable/disable route-tag addresses on the GUI.",
    "gui-voip-profile": "Enable/disable VoIP profiles on the GUI.",
    "gui-ap-profile": "Enable/disable FortiAP profiles on the GUI.",
    "gui-security-profile-group": "Enable/disable Security Profile Groups on the GUI.",
    "gui-local-in-policy": "Enable/disable Local-In policies on the GUI.",
    "gui-wanopt-cache": "Enable/disable WAN Optimization and Web Caching on the GUI.",
    "gui-explicit-proxy": "Enable/disable the explicit proxy on the GUI.",
    "gui-dynamic-routing": "Enable/disable dynamic routing on the GUI.",
    "gui-sslvpn-personal-bookmarks": "Enable/disable SSL-VPN personal bookmark management on the GUI.",
    "gui-sslvpn-realms": "Enable/disable SSL-VPN realms on the GUI.",
    "gui-policy-based-ipsec": "Enable/disable policy-based IPsec VPN on the GUI.",
    "gui-threat-weight": "Enable/disable threat weight on the GUI.",
    "gui-spamfilter": "Enable/disable Antispam on the GUI.",
    "gui-file-filter": "Enable/disable File-filter on the GUI.",
    "gui-application-control": "Enable/disable application control on the GUI.",
    "gui-ips": "Enable/disable IPS on the GUI.",
    "gui-dhcp-advanced": "Enable/disable advanced DHCP options on the GUI.",
    "gui-vpn": "Enable/disable IPsec VPN settings pages on the GUI.",
    "gui-sslvpn": "Enable/disable SSL-VPN settings pages on the GUI.",
    "gui-wireless-controller": "Enable/disable the wireless controller on the GUI.",
    "gui-advanced-wireless-features": "Enable/disable advanced wireless features in GUI.",
    "gui-switch-controller": "Enable/disable the switch controller on the GUI.",
    "gui-fortiap-split-tunneling": "Enable/disable FortiAP split tunneling on the GUI.",
    "gui-webfilter-advanced": "Enable/disable advanced web filtering on the GUI.",
    "gui-traffic-shaping": "Enable/disable traffic shaping on the GUI.",
    "gui-wan-load-balancing": "Enable/disable SD-WAN on the GUI.",
    "gui-antivirus": "Enable/disable AntiVirus on the GUI.",
    "gui-webfilter": "Enable/disable Web filtering on the GUI.",
    "gui-videofilter": "Enable/disable Video filtering on the GUI.",
    "gui-dnsfilter": "Enable/disable DNS Filtering on the GUI.",
    "gui-waf-profile": "Enable/disable Web Application Firewall on the GUI.",
    "gui-dlp-profile": "Enable/disable Data Loss Prevention on the GUI.",
    "gui-dlp-advanced": "Enable/disable Show advanced DLP expressions on the GUI.",
    "gui-virtual-patch-profile": "Enable/disable Virtual Patching on the GUI.",
    "gui-casb": "Enable/disable Inline-CASB on the GUI.",
    "gui-fortiextender-controller": "Enable/disable FortiExtender on the GUI.",
    "gui-advanced-policy": "Enable/disable advanced policy configuration on the GUI.",
    "gui-allow-unnamed-policy": "Enable/disable the requirement for policy naming on the GUI.",
    "gui-email-collection": "Enable/disable email collection on the GUI.",
    "gui-multiple-interface-policy": "Enable/disable adding multiple interfaces to a policy on the GUI.",
    "gui-policy-disclaimer": "Enable/disable policy disclaimer on the GUI.",
    "gui-ztna": "Enable/disable Zero Trust Network Access features on the GUI.",
    "gui-ot": "Enable/disable Operational technology features on the GUI.",
    "gui-dynamic-device-os-id": "Enable/disable Create dynamic addresses to manage known devices.",
    "gui-gtp": "Enable/disable Manage general radio packet service (GPRS) protocols on the GUI.",
    "location-id": "Local location ID in the form of an IPv4 address.",
    "ike-session-resume": "Enable/disable IKEv2 session resumption (RFC 5723).",
    "ike-quick-crash-detect": "Enable/disable IKE quick crash detection (RFC 6290).",
    "ike-dn-format": "Configure IKE ASN.1 Distinguished Name format conventions.",
    "ike-port": "UDP port for IKE/IPsec traffic (default 500).",
    "ike-tcp-port": "TCP port for IKE/IPsec traffic (default 443).",
    "ike-policy-route": "Enable/disable IKE Policy Based Routing (PBR).",
    "ike-detailed-event-logs": "Enable/disable detail log for IKE events.",
    "block-land-attack": "Enable/disable blocking of land attacks.",
    "default-app-port-as-service": "Enable/disable policy service enforcement based on application default ports.",
    "fqdn-session-check": "Enable/disable dirty session check caused by FQDN updates.",
    "ext-resource-session-check": "Enable/disable dirty session check caused by external resource updates.",
    "dyn-addr-session-check": "Enable/disable dirty session check caused by dynamic address updates.",
    "default-policy-expiry-days": "Default policy expiry in days (0 - 365 days, default = 30).",
    "gui-enforce-change-summary": "Enforce change summaries for select tables in the GUI.",
    "internet-service-database-cache": "Enable/disable Internet Service database caching.",
    "internet-service-app-ctrl-size": "Maximum number of tuple entries (protocol, port, IP address, application ID) stored by the FortiGate unit (0 - 4294967295, default = 32768). A smaller value limits the FortiGate unit from learning about internet applications.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "lan-extension-controller-addr": {"type": "string", "max_length": 255},
    "lan-extension-controller-port": {"type": "integer", "min": 1024, "max": 65535},
    "device": {"type": "string", "max_length": 35},
    "bfd-desired-min-tx": {"type": "integer", "min": 1, "max": 100000},
    "bfd-required-min-rx": {"type": "integer", "min": 1, "max": 100000},
    "bfd-detect-mult": {"type": "integer", "min": 1, "max": 50},
    "vpn-stats-period": {"type": "integer", "min": 0, "max": 4294967295},
    "mac-ttl": {"type": "integer", "min": 300, "max": 8640000},
    "dhcp-proxy-interface": {"type": "string", "max_length": 15},
    "dhcp-proxy-vrf-select": {"type": "integer", "min": 0, "max": 511},
    "sip-tcp-port": {"type": "integer", "min": 1, "max": 65535},
    "sip-udp-port": {"type": "integer", "min": 1, "max": 65535},
    "sip-ssl-port": {"type": "integer", "min": 0, "max": 65535},
    "sccp-port": {"type": "integer", "min": 0, "max": 65535},
    "ecmp-max-paths": {"type": "integer", "min": 1, "max": 255},
    "discovered-device-timeout": {"type": "integer", "min": 1, "max": 365},
    "ike-port": {"type": "integer", "min": 1024, "max": 65535},
    "ike-tcp-port": {"type": "integer", "min": 1, "max": 65535},
    "default-policy-expiry-days": {"type": "integer", "min": 0, "max": 365},
    "internet-service-app-ctrl-size": {"type": "integer", "min": 0, "max": 4294967295},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "gui-default-policy-columns": {
        "name": {
            "type": "string",
            "help": "Select column name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_VDOM_TYPE = [
    "traffic",
    "lan-extension",
    "admin",
]
VALID_BODY_OPMODE = [
    "nat",
    "transparent",
]
VALID_BODY_NGFW_MODE = [
    "profile-based",
    "policy-based",
]
VALID_BODY_HTTP_EXTERNAL_DEST = [
    "fortiweb",
    "forticache",
]
VALID_BODY_FIREWALL_SESSION_DIRTY = [
    "check-all",
    "check-new",
    "check-policy-option",
]
VALID_BODY_BFD = [
    "enable",
    "disable",
]
VALID_BODY_BFD_DONT_ENFORCE_SRC_PORT = [
    "enable",
    "disable",
]
VALID_BODY_UTF8_SPAM_TAGGING = [
    "enable",
    "disable",
]
VALID_BODY_WCCP_CACHE_ENGINE = [
    "enable",
    "disable",
]
VALID_BODY_VPN_STATS_LOG = [
    "ipsec",
    "pptp",
    "l2tp",
    "ssl",
]
VALID_BODY_V4_ECMP_MODE = [
    "source-ip-based",
    "weight-based",
    "usage-based",
    "source-dest-ip-based",
]
VALID_BODY_FW_SESSION_HAIRPIN = [
    "enable",
    "disable",
]
VALID_BODY_PRP_TRAILER_ACTION = [
    "enable",
    "disable",
]
VALID_BODY_SNAT_HAIRPIN_TRAFFIC = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_PROXY = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_PROXY_INTERFACE_SELECT_METHOD = [
    "auto",
    "sdwan",
    "specify",
]
VALID_BODY_CENTRAL_NAT = [
    "enable",
    "disable",
]
VALID_BODY_LLDP_RECEPTION = [
    "enable",
    "disable",
    "global",
]
VALID_BODY_LLDP_TRANSMISSION = [
    "enable",
    "disable",
    "global",
]
VALID_BODY_LINK_DOWN_ACCESS = [
    "enable",
    "disable",
]
VALID_BODY_NAT46_GENERATE_IPV6_FRAGMENT_HEADER = [
    "enable",
    "disable",
]
VALID_BODY_NAT46_FORCE_IPV4_PACKET_FORWARDING = [
    "enable",
    "disable",
]
VALID_BODY_NAT64_FORCE_IPV6_PACKET_FORWARDING = [
    "enable",
    "disable",
]
VALID_BODY_DETECT_UNKNOWN_ESP = [
    "enable",
    "disable",
]
VALID_BODY_INTREE_SES_BEST_ROUTE = [
    "force",
    "disable",
]
VALID_BODY_AUXILIARY_SESSION = [
    "enable",
    "disable",
]
VALID_BODY_ASYMROUTE = [
    "enable",
    "disable",
]
VALID_BODY_ASYMROUTE_ICMP = [
    "enable",
    "disable",
]
VALID_BODY_TCP_SESSION_WITHOUT_SYN = [
    "enable",
    "disable",
]
VALID_BODY_SES_DENIED_TRAFFIC = [
    "enable",
    "disable",
]
VALID_BODY_SES_DENIED_MULTICAST_TRAFFIC = [
    "enable",
    "disable",
]
VALID_BODY_STRICT_SRC_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_LINKDOWN_PATH = [
    "enable",
    "disable",
]
VALID_BODY_ASYMROUTE6 = [
    "enable",
    "disable",
]
VALID_BODY_ASYMROUTE6_ICMP = [
    "enable",
    "disable",
]
VALID_BODY_SCTP_SESSION_WITHOUT_INIT = [
    "enable",
    "disable",
]
VALID_BODY_SIP_EXPECTATION = [
    "enable",
    "disable",
]
VALID_BODY_SIP_NAT_TRACE = [
    "enable",
    "disable",
]
VALID_BODY_H323_DIRECT_MODEL = [
    "disable",
    "enable",
]
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_MULTICAST_FORWARD = [
    "enable",
    "disable",
]
VALID_BODY_MULTICAST_TTL_NOTCHANGE = [
    "enable",
    "disable",
]
VALID_BODY_MULTICAST_SKIP_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_SUBNET_OVERLAP = [
    "enable",
    "disable",
]
VALID_BODY_DENY_TCP_WITH_ICMP = [
    "enable",
    "disable",
]
VALID_BODY_EMAIL_PORTAL_CHECK_DNS = [
    "disable",
    "enable",
]
VALID_BODY_DEFAULT_VOIP_ALG_MODE = [
    "proxy-based",
    "kernel-helper-based",
]
VALID_BODY_GUI_ICAP = [
    "enable",
    "disable",
]
VALID_BODY_GUI_IMPLICIT_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DNS_DATABASE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_LOAD_BALANCE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_MULTICAST_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DOS_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_OBJECT_COLORS = [
    "enable",
    "disable",
]
VALID_BODY_GUI_ROUTE_TAG_ADDRESS_CREATION = [
    "enable",
    "disable",
]
VALID_BODY_GUI_VOIP_PROFILE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_AP_PROFILE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_SECURITY_PROFILE_GROUP = [
    "enable",
    "disable",
]
VALID_BODY_GUI_LOCAL_IN_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WANOPT_CACHE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_EXPLICIT_PROXY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DYNAMIC_ROUTING = [
    "enable",
    "disable",
]
VALID_BODY_GUI_SSLVPN_PERSONAL_BOOKMARKS = [
    "enable",
    "disable",
]
VALID_BODY_GUI_SSLVPN_REALMS = [
    "enable",
    "disable",
]
VALID_BODY_GUI_POLICY_BASED_IPSEC = [
    "enable",
    "disable",
]
VALID_BODY_GUI_THREAT_WEIGHT = [
    "enable",
    "disable",
]
VALID_BODY_GUI_SPAMFILTER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_FILE_FILTER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_APPLICATION_CONTROL = [
    "enable",
    "disable",
]
VALID_BODY_GUI_IPS = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DHCP_ADVANCED = [
    "enable",
    "disable",
]
VALID_BODY_GUI_VPN = [
    "enable",
    "disable",
]
VALID_BODY_GUI_SSLVPN = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WIRELESS_CONTROLLER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_ADVANCED_WIRELESS_FEATURES = [
    "enable",
    "disable",
]
VALID_BODY_GUI_SWITCH_CONTROLLER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_FORTIAP_SPLIT_TUNNELING = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WEBFILTER_ADVANCED = [
    "enable",
    "disable",
]
VALID_BODY_GUI_TRAFFIC_SHAPING = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WAN_LOAD_BALANCING = [
    "enable",
    "disable",
]
VALID_BODY_GUI_ANTIVIRUS = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WEBFILTER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_VIDEOFILTER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DNSFILTER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WAF_PROFILE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DLP_PROFILE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DLP_ADVANCED = [
    "enable",
    "disable",
]
VALID_BODY_GUI_VIRTUAL_PATCH_PROFILE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_CASB = [
    "enable",
    "disable",
]
VALID_BODY_GUI_FORTIEXTENDER_CONTROLLER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_ADVANCED_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_ALLOW_UNNAMED_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_EMAIL_COLLECTION = [
    "enable",
    "disable",
]
VALID_BODY_GUI_MULTIPLE_INTERFACE_POLICY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_POLICY_DISCLAIMER = [
    "enable",
    "disable",
]
VALID_BODY_GUI_ZTNA = [
    "enable",
    "disable",
]
VALID_BODY_GUI_OT = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DYNAMIC_DEVICE_OS_ID = [
    "enable",
    "disable",
]
VALID_BODY_GUI_GTP = [
    "enable",
    "disable",
]
VALID_BODY_IKE_SESSION_RESUME = [
    "enable",
    "disable",
]
VALID_BODY_IKE_QUICK_CRASH_DETECT = [
    "enable",
    "disable",
]
VALID_BODY_IKE_DN_FORMAT = [
    "with-space",
    "no-space",
]
VALID_BODY_IKE_POLICY_ROUTE = [
    "enable",
    "disable",
]
VALID_BODY_IKE_DETAILED_EVENT_LOGS = [
    "disable",
    "enable",
]
VALID_BODY_BLOCK_LAND_ATTACK = [
    "disable",
    "enable",
]
VALID_BODY_DEFAULT_APP_PORT_AS_SERVICE = [
    "enable",
    "disable",
]
VALID_BODY_FQDN_SESSION_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_EXT_RESOURCE_SESSION_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_DYN_ADDR_SESSION_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_GUI_ENFORCE_CHANGE_SUMMARY = [
    "disable",
    "require",
    "optional",
]
VALID_BODY_INTERNET_SERVICE_DATABASE_CACHE = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_settings_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/settings."""
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


def validate_system_settings_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/settings object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "vdom-type" in payload:
        is_valid, error = _validate_enum_field(
            "vdom-type",
            payload["vdom-type"],
            VALID_BODY_VDOM_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "opmode" in payload:
        is_valid, error = _validate_enum_field(
            "opmode",
            payload["opmode"],
            VALID_BODY_OPMODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ngfw-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ngfw-mode",
            payload["ngfw-mode"],
            VALID_BODY_NGFW_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-external-dest" in payload:
        is_valid, error = _validate_enum_field(
            "http-external-dest",
            payload["http-external-dest"],
            VALID_BODY_HTTP_EXTERNAL_DEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firewall-session-dirty" in payload:
        is_valid, error = _validate_enum_field(
            "firewall-session-dirty",
            payload["firewall-session-dirty"],
            VALID_BODY_FIREWALL_SESSION_DIRTY,
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
    if "bfd-dont-enforce-src-port" in payload:
        is_valid, error = _validate_enum_field(
            "bfd-dont-enforce-src-port",
            payload["bfd-dont-enforce-src-port"],
            VALID_BODY_BFD_DONT_ENFORCE_SRC_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utf8-spam-tagging" in payload:
        is_valid, error = _validate_enum_field(
            "utf8-spam-tagging",
            payload["utf8-spam-tagging"],
            VALID_BODY_UTF8_SPAM_TAGGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wccp-cache-engine" in payload:
        is_valid, error = _validate_enum_field(
            "wccp-cache-engine",
            payload["wccp-cache-engine"],
            VALID_BODY_WCCP_CACHE_ENGINE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpn-stats-log" in payload:
        is_valid, error = _validate_enum_field(
            "vpn-stats-log",
            payload["vpn-stats-log"],
            VALID_BODY_VPN_STATS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "v4-ecmp-mode" in payload:
        is_valid, error = _validate_enum_field(
            "v4-ecmp-mode",
            payload["v4-ecmp-mode"],
            VALID_BODY_V4_ECMP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fw-session-hairpin" in payload:
        is_valid, error = _validate_enum_field(
            "fw-session-hairpin",
            payload["fw-session-hairpin"],
            VALID_BODY_FW_SESSION_HAIRPIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "prp-trailer-action" in payload:
        is_valid, error = _validate_enum_field(
            "prp-trailer-action",
            payload["prp-trailer-action"],
            VALID_BODY_PRP_TRAILER_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "snat-hairpin-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "snat-hairpin-traffic",
            payload["snat-hairpin-traffic"],
            VALID_BODY_SNAT_HAIRPIN_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-proxy",
            payload["dhcp-proxy"],
            VALID_BODY_DHCP_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-proxy-interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-proxy-interface-select-method",
            payload["dhcp-proxy-interface-select-method"],
            VALID_BODY_DHCP_PROXY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "central-nat" in payload:
        is_valid, error = _validate_enum_field(
            "central-nat",
            payload["central-nat"],
            VALID_BODY_CENTRAL_NAT,
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
    if "link-down-access" in payload:
        is_valid, error = _validate_enum_field(
            "link-down-access",
            payload["link-down-access"],
            VALID_BODY_LINK_DOWN_ACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46-generate-ipv6-fragment-header" in payload:
        is_valid, error = _validate_enum_field(
            "nat46-generate-ipv6-fragment-header",
            payload["nat46-generate-ipv6-fragment-header"],
            VALID_BODY_NAT46_GENERATE_IPV6_FRAGMENT_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46-force-ipv4-packet-forwarding" in payload:
        is_valid, error = _validate_enum_field(
            "nat46-force-ipv4-packet-forwarding",
            payload["nat46-force-ipv4-packet-forwarding"],
            VALID_BODY_NAT46_FORCE_IPV4_PACKET_FORWARDING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64-force-ipv6-packet-forwarding" in payload:
        is_valid, error = _validate_enum_field(
            "nat64-force-ipv6-packet-forwarding",
            payload["nat64-force-ipv6-packet-forwarding"],
            VALID_BODY_NAT64_FORCE_IPV6_PACKET_FORWARDING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "detect-unknown-esp" in payload:
        is_valid, error = _validate_enum_field(
            "detect-unknown-esp",
            payload["detect-unknown-esp"],
            VALID_BODY_DETECT_UNKNOWN_ESP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "intree-ses-best-route" in payload:
        is_valid, error = _validate_enum_field(
            "intree-ses-best-route",
            payload["intree-ses-best-route"],
            VALID_BODY_INTREE_SES_BEST_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auxiliary-session" in payload:
        is_valid, error = _validate_enum_field(
            "auxiliary-session",
            payload["auxiliary-session"],
            VALID_BODY_AUXILIARY_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute",
            payload["asymroute"],
            VALID_BODY_ASYMROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute-icmp",
            payload["asymroute-icmp"],
            VALID_BODY_ASYMROUTE_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tcp-session-without-syn" in payload:
        is_valid, error = _validate_enum_field(
            "tcp-session-without-syn",
            payload["tcp-session-without-syn"],
            VALID_BODY_TCP_SESSION_WITHOUT_SYN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ses-denied-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "ses-denied-traffic",
            payload["ses-denied-traffic"],
            VALID_BODY_SES_DENIED_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ses-denied-multicast-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "ses-denied-multicast-traffic",
            payload["ses-denied-multicast-traffic"],
            VALID_BODY_SES_DENIED_MULTICAST_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-src-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-src-check",
            payload["strict-src-check"],
            VALID_BODY_STRICT_SRC_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-linkdown-path" in payload:
        is_valid, error = _validate_enum_field(
            "allow-linkdown-path",
            payload["allow-linkdown-path"],
            VALID_BODY_ALLOW_LINKDOWN_PATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute6" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute6",
            payload["asymroute6"],
            VALID_BODY_ASYMROUTE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute6-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute6-icmp",
            payload["asymroute6-icmp"],
            VALID_BODY_ASYMROUTE6_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sctp-session-without-init" in payload:
        is_valid, error = _validate_enum_field(
            "sctp-session-without-init",
            payload["sctp-session-without-init"],
            VALID_BODY_SCTP_SESSION_WITHOUT_INIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sip-expectation" in payload:
        is_valid, error = _validate_enum_field(
            "sip-expectation",
            payload["sip-expectation"],
            VALID_BODY_SIP_EXPECTATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sip-nat-trace" in payload:
        is_valid, error = _validate_enum_field(
            "sip-nat-trace",
            payload["sip-nat-trace"],
            VALID_BODY_SIP_NAT_TRACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h323-direct-model" in payload:
        is_valid, error = _validate_enum_field(
            "h323-direct-model",
            payload["h323-direct-model"],
            VALID_BODY_H323_DIRECT_MODEL,
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
    if "multicast-forward" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-forward",
            payload["multicast-forward"],
            VALID_BODY_MULTICAST_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-ttl-notchange" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-ttl-notchange",
            payload["multicast-ttl-notchange"],
            VALID_BODY_MULTICAST_TTL_NOTCHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-skip-policy" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-skip-policy",
            payload["multicast-skip-policy"],
            VALID_BODY_MULTICAST_SKIP_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-subnet-overlap" in payload:
        is_valid, error = _validate_enum_field(
            "allow-subnet-overlap",
            payload["allow-subnet-overlap"],
            VALID_BODY_ALLOW_SUBNET_OVERLAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "deny-tcp-with-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "deny-tcp-with-icmp",
            payload["deny-tcp-with-icmp"],
            VALID_BODY_DENY_TCP_WITH_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email-portal-check-dns" in payload:
        is_valid, error = _validate_enum_field(
            "email-portal-check-dns",
            payload["email-portal-check-dns"],
            VALID_BODY_EMAIL_PORTAL_CHECK_DNS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-voip-alg-mode" in payload:
        is_valid, error = _validate_enum_field(
            "default-voip-alg-mode",
            payload["default-voip-alg-mode"],
            VALID_BODY_DEFAULT_VOIP_ALG_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-icap" in payload:
        is_valid, error = _validate_enum_field(
            "gui-icap",
            payload["gui-icap"],
            VALID_BODY_GUI_ICAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-implicit-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-implicit-policy",
            payload["gui-implicit-policy"],
            VALID_BODY_GUI_IMPLICIT_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dns-database" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dns-database",
            payload["gui-dns-database"],
            VALID_BODY_GUI_DNS_DATABASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-load-balance" in payload:
        is_valid, error = _validate_enum_field(
            "gui-load-balance",
            payload["gui-load-balance"],
            VALID_BODY_GUI_LOAD_BALANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-multicast-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-multicast-policy",
            payload["gui-multicast-policy"],
            VALID_BODY_GUI_MULTICAST_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dos-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dos-policy",
            payload["gui-dos-policy"],
            VALID_BODY_GUI_DOS_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-object-colors" in payload:
        is_valid, error = _validate_enum_field(
            "gui-object-colors",
            payload["gui-object-colors"],
            VALID_BODY_GUI_OBJECT_COLORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-route-tag-address-creation" in payload:
        is_valid, error = _validate_enum_field(
            "gui-route-tag-address-creation",
            payload["gui-route-tag-address-creation"],
            VALID_BODY_GUI_ROUTE_TAG_ADDRESS_CREATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-voip-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-voip-profile",
            payload["gui-voip-profile"],
            VALID_BODY_GUI_VOIP_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ap-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ap-profile",
            payload["gui-ap-profile"],
            VALID_BODY_GUI_AP_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-security-profile-group" in payload:
        is_valid, error = _validate_enum_field(
            "gui-security-profile-group",
            payload["gui-security-profile-group"],
            VALID_BODY_GUI_SECURITY_PROFILE_GROUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-local-in-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-local-in-policy",
            payload["gui-local-in-policy"],
            VALID_BODY_GUI_LOCAL_IN_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wanopt-cache" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wanopt-cache",
            payload["gui-wanopt-cache"],
            VALID_BODY_GUI_WANOPT_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-explicit-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-explicit-proxy",
            payload["gui-explicit-proxy"],
            VALID_BODY_GUI_EXPLICIT_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dynamic-routing" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dynamic-routing",
            payload["gui-dynamic-routing"],
            VALID_BODY_GUI_DYNAMIC_ROUTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-sslvpn-personal-bookmarks" in payload:
        is_valid, error = _validate_enum_field(
            "gui-sslvpn-personal-bookmarks",
            payload["gui-sslvpn-personal-bookmarks"],
            VALID_BODY_GUI_SSLVPN_PERSONAL_BOOKMARKS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-sslvpn-realms" in payload:
        is_valid, error = _validate_enum_field(
            "gui-sslvpn-realms",
            payload["gui-sslvpn-realms"],
            VALID_BODY_GUI_SSLVPN_REALMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-policy-based-ipsec" in payload:
        is_valid, error = _validate_enum_field(
            "gui-policy-based-ipsec",
            payload["gui-policy-based-ipsec"],
            VALID_BODY_GUI_POLICY_BASED_IPSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-threat-weight" in payload:
        is_valid, error = _validate_enum_field(
            "gui-threat-weight",
            payload["gui-threat-weight"],
            VALID_BODY_GUI_THREAT_WEIGHT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-spamfilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-spamfilter",
            payload["gui-spamfilter"],
            VALID_BODY_GUI_SPAMFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-file-filter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-file-filter",
            payload["gui-file-filter"],
            VALID_BODY_GUI_FILE_FILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-application-control" in payload:
        is_valid, error = _validate_enum_field(
            "gui-application-control",
            payload["gui-application-control"],
            VALID_BODY_GUI_APPLICATION_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ips" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ips",
            payload["gui-ips"],
            VALID_BODY_GUI_IPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dhcp-advanced" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dhcp-advanced",
            payload["gui-dhcp-advanced"],
            VALID_BODY_GUI_DHCP_ADVANCED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-vpn" in payload:
        is_valid, error = _validate_enum_field(
            "gui-vpn",
            payload["gui-vpn"],
            VALID_BODY_GUI_VPN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-sslvpn" in payload:
        is_valid, error = _validate_enum_field(
            "gui-sslvpn",
            payload["gui-sslvpn"],
            VALID_BODY_GUI_SSLVPN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wireless-controller" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wireless-controller",
            payload["gui-wireless-controller"],
            VALID_BODY_GUI_WIRELESS_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-advanced-wireless-features" in payload:
        is_valid, error = _validate_enum_field(
            "gui-advanced-wireless-features",
            payload["gui-advanced-wireless-features"],
            VALID_BODY_GUI_ADVANCED_WIRELESS_FEATURES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-switch-controller" in payload:
        is_valid, error = _validate_enum_field(
            "gui-switch-controller",
            payload["gui-switch-controller"],
            VALID_BODY_GUI_SWITCH_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-fortiap-split-tunneling" in payload:
        is_valid, error = _validate_enum_field(
            "gui-fortiap-split-tunneling",
            payload["gui-fortiap-split-tunneling"],
            VALID_BODY_GUI_FORTIAP_SPLIT_TUNNELING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-webfilter-advanced" in payload:
        is_valid, error = _validate_enum_field(
            "gui-webfilter-advanced",
            payload["gui-webfilter-advanced"],
            VALID_BODY_GUI_WEBFILTER_ADVANCED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-traffic-shaping" in payload:
        is_valid, error = _validate_enum_field(
            "gui-traffic-shaping",
            payload["gui-traffic-shaping"],
            VALID_BODY_GUI_TRAFFIC_SHAPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wan-load-balancing" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wan-load-balancing",
            payload["gui-wan-load-balancing"],
            VALID_BODY_GUI_WAN_LOAD_BALANCING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-antivirus" in payload:
        is_valid, error = _validate_enum_field(
            "gui-antivirus",
            payload["gui-antivirus"],
            VALID_BODY_GUI_ANTIVIRUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-webfilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-webfilter",
            payload["gui-webfilter"],
            VALID_BODY_GUI_WEBFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-videofilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-videofilter",
            payload["gui-videofilter"],
            VALID_BODY_GUI_VIDEOFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dnsfilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dnsfilter",
            payload["gui-dnsfilter"],
            VALID_BODY_GUI_DNSFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-waf-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-waf-profile",
            payload["gui-waf-profile"],
            VALID_BODY_GUI_WAF_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dlp-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dlp-profile",
            payload["gui-dlp-profile"],
            VALID_BODY_GUI_DLP_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dlp-advanced" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dlp-advanced",
            payload["gui-dlp-advanced"],
            VALID_BODY_GUI_DLP_ADVANCED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-virtual-patch-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-virtual-patch-profile",
            payload["gui-virtual-patch-profile"],
            VALID_BODY_GUI_VIRTUAL_PATCH_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-casb" in payload:
        is_valid, error = _validate_enum_field(
            "gui-casb",
            payload["gui-casb"],
            VALID_BODY_GUI_CASB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-fortiextender-controller" in payload:
        is_valid, error = _validate_enum_field(
            "gui-fortiextender-controller",
            payload["gui-fortiextender-controller"],
            VALID_BODY_GUI_FORTIEXTENDER_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-advanced-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-advanced-policy",
            payload["gui-advanced-policy"],
            VALID_BODY_GUI_ADVANCED_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-allow-unnamed-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-allow-unnamed-policy",
            payload["gui-allow-unnamed-policy"],
            VALID_BODY_GUI_ALLOW_UNNAMED_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-email-collection" in payload:
        is_valid, error = _validate_enum_field(
            "gui-email-collection",
            payload["gui-email-collection"],
            VALID_BODY_GUI_EMAIL_COLLECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-multiple-interface-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-multiple-interface-policy",
            payload["gui-multiple-interface-policy"],
            VALID_BODY_GUI_MULTIPLE_INTERFACE_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-policy-disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "gui-policy-disclaimer",
            payload["gui-policy-disclaimer"],
            VALID_BODY_GUI_POLICY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ztna" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ztna",
            payload["gui-ztna"],
            VALID_BODY_GUI_ZTNA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ot" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ot",
            payload["gui-ot"],
            VALID_BODY_GUI_OT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dynamic-device-os-id" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dynamic-device-os-id",
            payload["gui-dynamic-device-os-id"],
            VALID_BODY_GUI_DYNAMIC_DEVICE_OS_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-gtp" in payload:
        is_valid, error = _validate_enum_field(
            "gui-gtp",
            payload["gui-gtp"],
            VALID_BODY_GUI_GTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-session-resume" in payload:
        is_valid, error = _validate_enum_field(
            "ike-session-resume",
            payload["ike-session-resume"],
            VALID_BODY_IKE_SESSION_RESUME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-quick-crash-detect" in payload:
        is_valid, error = _validate_enum_field(
            "ike-quick-crash-detect",
            payload["ike-quick-crash-detect"],
            VALID_BODY_IKE_QUICK_CRASH_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-dn-format" in payload:
        is_valid, error = _validate_enum_field(
            "ike-dn-format",
            payload["ike-dn-format"],
            VALID_BODY_IKE_DN_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-policy-route" in payload:
        is_valid, error = _validate_enum_field(
            "ike-policy-route",
            payload["ike-policy-route"],
            VALID_BODY_IKE_POLICY_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-detailed-event-logs" in payload:
        is_valid, error = _validate_enum_field(
            "ike-detailed-event-logs",
            payload["ike-detailed-event-logs"],
            VALID_BODY_IKE_DETAILED_EVENT_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-land-attack" in payload:
        is_valid, error = _validate_enum_field(
            "block-land-attack",
            payload["block-land-attack"],
            VALID_BODY_BLOCK_LAND_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-app-port-as-service" in payload:
        is_valid, error = _validate_enum_field(
            "default-app-port-as-service",
            payload["default-app-port-as-service"],
            VALID_BODY_DEFAULT_APP_PORT_AS_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fqdn-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "fqdn-session-check",
            payload["fqdn-session-check"],
            VALID_BODY_FQDN_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ext-resource-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "ext-resource-session-check",
            payload["ext-resource-session-check"],
            VALID_BODY_EXT_RESOURCE_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dyn-addr-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "dyn-addr-session-check",
            payload["dyn-addr-session-check"],
            VALID_BODY_DYN_ADDR_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-enforce-change-summary" in payload:
        is_valid, error = _validate_enum_field(
            "gui-enforce-change-summary",
            payload["gui-enforce-change-summary"],
            VALID_BODY_GUI_ENFORCE_CHANGE_SUMMARY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-database-cache" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-database-cache",
            payload["internet-service-database-cache"],
            VALID_BODY_INTERNET_SERVICE_DATABASE_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_settings_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/settings."""
    # Validate enum values using central function
    if "vdom-type" in payload:
        is_valid, error = _validate_enum_field(
            "vdom-type",
            payload["vdom-type"],
            VALID_BODY_VDOM_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "opmode" in payload:
        is_valid, error = _validate_enum_field(
            "opmode",
            payload["opmode"],
            VALID_BODY_OPMODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ngfw-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ngfw-mode",
            payload["ngfw-mode"],
            VALID_BODY_NGFW_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-external-dest" in payload:
        is_valid, error = _validate_enum_field(
            "http-external-dest",
            payload["http-external-dest"],
            VALID_BODY_HTTP_EXTERNAL_DEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "firewall-session-dirty" in payload:
        is_valid, error = _validate_enum_field(
            "firewall-session-dirty",
            payload["firewall-session-dirty"],
            VALID_BODY_FIREWALL_SESSION_DIRTY,
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
    if "bfd-dont-enforce-src-port" in payload:
        is_valid, error = _validate_enum_field(
            "bfd-dont-enforce-src-port",
            payload["bfd-dont-enforce-src-port"],
            VALID_BODY_BFD_DONT_ENFORCE_SRC_PORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "utf8-spam-tagging" in payload:
        is_valid, error = _validate_enum_field(
            "utf8-spam-tagging",
            payload["utf8-spam-tagging"],
            VALID_BODY_UTF8_SPAM_TAGGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wccp-cache-engine" in payload:
        is_valid, error = _validate_enum_field(
            "wccp-cache-engine",
            payload["wccp-cache-engine"],
            VALID_BODY_WCCP_CACHE_ENGINE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vpn-stats-log" in payload:
        is_valid, error = _validate_enum_field(
            "vpn-stats-log",
            payload["vpn-stats-log"],
            VALID_BODY_VPN_STATS_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "v4-ecmp-mode" in payload:
        is_valid, error = _validate_enum_field(
            "v4-ecmp-mode",
            payload["v4-ecmp-mode"],
            VALID_BODY_V4_ECMP_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fw-session-hairpin" in payload:
        is_valid, error = _validate_enum_field(
            "fw-session-hairpin",
            payload["fw-session-hairpin"],
            VALID_BODY_FW_SESSION_HAIRPIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "prp-trailer-action" in payload:
        is_valid, error = _validate_enum_field(
            "prp-trailer-action",
            payload["prp-trailer-action"],
            VALID_BODY_PRP_TRAILER_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "snat-hairpin-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "snat-hairpin-traffic",
            payload["snat-hairpin-traffic"],
            VALID_BODY_SNAT_HAIRPIN_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-proxy",
            payload["dhcp-proxy"],
            VALID_BODY_DHCP_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-proxy-interface-select-method" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-proxy-interface-select-method",
            payload["dhcp-proxy-interface-select-method"],
            VALID_BODY_DHCP_PROXY_INTERFACE_SELECT_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "central-nat" in payload:
        is_valid, error = _validate_enum_field(
            "central-nat",
            payload["central-nat"],
            VALID_BODY_CENTRAL_NAT,
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
    if "link-down-access" in payload:
        is_valid, error = _validate_enum_field(
            "link-down-access",
            payload["link-down-access"],
            VALID_BODY_LINK_DOWN_ACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46-generate-ipv6-fragment-header" in payload:
        is_valid, error = _validate_enum_field(
            "nat46-generate-ipv6-fragment-header",
            payload["nat46-generate-ipv6-fragment-header"],
            VALID_BODY_NAT46_GENERATE_IPV6_FRAGMENT_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46-force-ipv4-packet-forwarding" in payload:
        is_valid, error = _validate_enum_field(
            "nat46-force-ipv4-packet-forwarding",
            payload["nat46-force-ipv4-packet-forwarding"],
            VALID_BODY_NAT46_FORCE_IPV4_PACKET_FORWARDING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64-force-ipv6-packet-forwarding" in payload:
        is_valid, error = _validate_enum_field(
            "nat64-force-ipv6-packet-forwarding",
            payload["nat64-force-ipv6-packet-forwarding"],
            VALID_BODY_NAT64_FORCE_IPV6_PACKET_FORWARDING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "detect-unknown-esp" in payload:
        is_valid, error = _validate_enum_field(
            "detect-unknown-esp",
            payload["detect-unknown-esp"],
            VALID_BODY_DETECT_UNKNOWN_ESP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "intree-ses-best-route" in payload:
        is_valid, error = _validate_enum_field(
            "intree-ses-best-route",
            payload["intree-ses-best-route"],
            VALID_BODY_INTREE_SES_BEST_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auxiliary-session" in payload:
        is_valid, error = _validate_enum_field(
            "auxiliary-session",
            payload["auxiliary-session"],
            VALID_BODY_AUXILIARY_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute",
            payload["asymroute"],
            VALID_BODY_ASYMROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute-icmp",
            payload["asymroute-icmp"],
            VALID_BODY_ASYMROUTE_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tcp-session-without-syn" in payload:
        is_valid, error = _validate_enum_field(
            "tcp-session-without-syn",
            payload["tcp-session-without-syn"],
            VALID_BODY_TCP_SESSION_WITHOUT_SYN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ses-denied-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "ses-denied-traffic",
            payload["ses-denied-traffic"],
            VALID_BODY_SES_DENIED_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ses-denied-multicast-traffic" in payload:
        is_valid, error = _validate_enum_field(
            "ses-denied-multicast-traffic",
            payload["ses-denied-multicast-traffic"],
            VALID_BODY_SES_DENIED_MULTICAST_TRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-src-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-src-check",
            payload["strict-src-check"],
            VALID_BODY_STRICT_SRC_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-linkdown-path" in payload:
        is_valid, error = _validate_enum_field(
            "allow-linkdown-path",
            payload["allow-linkdown-path"],
            VALID_BODY_ALLOW_LINKDOWN_PATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute6" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute6",
            payload["asymroute6"],
            VALID_BODY_ASYMROUTE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "asymroute6-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "asymroute6-icmp",
            payload["asymroute6-icmp"],
            VALID_BODY_ASYMROUTE6_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sctp-session-without-init" in payload:
        is_valid, error = _validate_enum_field(
            "sctp-session-without-init",
            payload["sctp-session-without-init"],
            VALID_BODY_SCTP_SESSION_WITHOUT_INIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sip-expectation" in payload:
        is_valid, error = _validate_enum_field(
            "sip-expectation",
            payload["sip-expectation"],
            VALID_BODY_SIP_EXPECTATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sip-nat-trace" in payload:
        is_valid, error = _validate_enum_field(
            "sip-nat-trace",
            payload["sip-nat-trace"],
            VALID_BODY_SIP_NAT_TRACE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h323-direct-model" in payload:
        is_valid, error = _validate_enum_field(
            "h323-direct-model",
            payload["h323-direct-model"],
            VALID_BODY_H323_DIRECT_MODEL,
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
    if "multicast-forward" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-forward",
            payload["multicast-forward"],
            VALID_BODY_MULTICAST_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-ttl-notchange" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-ttl-notchange",
            payload["multicast-ttl-notchange"],
            VALID_BODY_MULTICAST_TTL_NOTCHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-skip-policy" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-skip-policy",
            payload["multicast-skip-policy"],
            VALID_BODY_MULTICAST_SKIP_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-subnet-overlap" in payload:
        is_valid, error = _validate_enum_field(
            "allow-subnet-overlap",
            payload["allow-subnet-overlap"],
            VALID_BODY_ALLOW_SUBNET_OVERLAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "deny-tcp-with-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "deny-tcp-with-icmp",
            payload["deny-tcp-with-icmp"],
            VALID_BODY_DENY_TCP_WITH_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email-portal-check-dns" in payload:
        is_valid, error = _validate_enum_field(
            "email-portal-check-dns",
            payload["email-portal-check-dns"],
            VALID_BODY_EMAIL_PORTAL_CHECK_DNS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-voip-alg-mode" in payload:
        is_valid, error = _validate_enum_field(
            "default-voip-alg-mode",
            payload["default-voip-alg-mode"],
            VALID_BODY_DEFAULT_VOIP_ALG_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-icap" in payload:
        is_valid, error = _validate_enum_field(
            "gui-icap",
            payload["gui-icap"],
            VALID_BODY_GUI_ICAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-implicit-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-implicit-policy",
            payload["gui-implicit-policy"],
            VALID_BODY_GUI_IMPLICIT_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dns-database" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dns-database",
            payload["gui-dns-database"],
            VALID_BODY_GUI_DNS_DATABASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-load-balance" in payload:
        is_valid, error = _validate_enum_field(
            "gui-load-balance",
            payload["gui-load-balance"],
            VALID_BODY_GUI_LOAD_BALANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-multicast-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-multicast-policy",
            payload["gui-multicast-policy"],
            VALID_BODY_GUI_MULTICAST_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dos-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dos-policy",
            payload["gui-dos-policy"],
            VALID_BODY_GUI_DOS_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-object-colors" in payload:
        is_valid, error = _validate_enum_field(
            "gui-object-colors",
            payload["gui-object-colors"],
            VALID_BODY_GUI_OBJECT_COLORS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-route-tag-address-creation" in payload:
        is_valid, error = _validate_enum_field(
            "gui-route-tag-address-creation",
            payload["gui-route-tag-address-creation"],
            VALID_BODY_GUI_ROUTE_TAG_ADDRESS_CREATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-voip-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-voip-profile",
            payload["gui-voip-profile"],
            VALID_BODY_GUI_VOIP_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ap-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ap-profile",
            payload["gui-ap-profile"],
            VALID_BODY_GUI_AP_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-security-profile-group" in payload:
        is_valid, error = _validate_enum_field(
            "gui-security-profile-group",
            payload["gui-security-profile-group"],
            VALID_BODY_GUI_SECURITY_PROFILE_GROUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-local-in-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-local-in-policy",
            payload["gui-local-in-policy"],
            VALID_BODY_GUI_LOCAL_IN_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wanopt-cache" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wanopt-cache",
            payload["gui-wanopt-cache"],
            VALID_BODY_GUI_WANOPT_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-explicit-proxy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-explicit-proxy",
            payload["gui-explicit-proxy"],
            VALID_BODY_GUI_EXPLICIT_PROXY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dynamic-routing" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dynamic-routing",
            payload["gui-dynamic-routing"],
            VALID_BODY_GUI_DYNAMIC_ROUTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-sslvpn-personal-bookmarks" in payload:
        is_valid, error = _validate_enum_field(
            "gui-sslvpn-personal-bookmarks",
            payload["gui-sslvpn-personal-bookmarks"],
            VALID_BODY_GUI_SSLVPN_PERSONAL_BOOKMARKS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-sslvpn-realms" in payload:
        is_valid, error = _validate_enum_field(
            "gui-sslvpn-realms",
            payload["gui-sslvpn-realms"],
            VALID_BODY_GUI_SSLVPN_REALMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-policy-based-ipsec" in payload:
        is_valid, error = _validate_enum_field(
            "gui-policy-based-ipsec",
            payload["gui-policy-based-ipsec"],
            VALID_BODY_GUI_POLICY_BASED_IPSEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-threat-weight" in payload:
        is_valid, error = _validate_enum_field(
            "gui-threat-weight",
            payload["gui-threat-weight"],
            VALID_BODY_GUI_THREAT_WEIGHT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-spamfilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-spamfilter",
            payload["gui-spamfilter"],
            VALID_BODY_GUI_SPAMFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-file-filter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-file-filter",
            payload["gui-file-filter"],
            VALID_BODY_GUI_FILE_FILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-application-control" in payload:
        is_valid, error = _validate_enum_field(
            "gui-application-control",
            payload["gui-application-control"],
            VALID_BODY_GUI_APPLICATION_CONTROL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ips" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ips",
            payload["gui-ips"],
            VALID_BODY_GUI_IPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dhcp-advanced" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dhcp-advanced",
            payload["gui-dhcp-advanced"],
            VALID_BODY_GUI_DHCP_ADVANCED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-vpn" in payload:
        is_valid, error = _validate_enum_field(
            "gui-vpn",
            payload["gui-vpn"],
            VALID_BODY_GUI_VPN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-sslvpn" in payload:
        is_valid, error = _validate_enum_field(
            "gui-sslvpn",
            payload["gui-sslvpn"],
            VALID_BODY_GUI_SSLVPN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wireless-controller" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wireless-controller",
            payload["gui-wireless-controller"],
            VALID_BODY_GUI_WIRELESS_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-advanced-wireless-features" in payload:
        is_valid, error = _validate_enum_field(
            "gui-advanced-wireless-features",
            payload["gui-advanced-wireless-features"],
            VALID_BODY_GUI_ADVANCED_WIRELESS_FEATURES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-switch-controller" in payload:
        is_valid, error = _validate_enum_field(
            "gui-switch-controller",
            payload["gui-switch-controller"],
            VALID_BODY_GUI_SWITCH_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-fortiap-split-tunneling" in payload:
        is_valid, error = _validate_enum_field(
            "gui-fortiap-split-tunneling",
            payload["gui-fortiap-split-tunneling"],
            VALID_BODY_GUI_FORTIAP_SPLIT_TUNNELING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-webfilter-advanced" in payload:
        is_valid, error = _validate_enum_field(
            "gui-webfilter-advanced",
            payload["gui-webfilter-advanced"],
            VALID_BODY_GUI_WEBFILTER_ADVANCED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-traffic-shaping" in payload:
        is_valid, error = _validate_enum_field(
            "gui-traffic-shaping",
            payload["gui-traffic-shaping"],
            VALID_BODY_GUI_TRAFFIC_SHAPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wan-load-balancing" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wan-load-balancing",
            payload["gui-wan-load-balancing"],
            VALID_BODY_GUI_WAN_LOAD_BALANCING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-antivirus" in payload:
        is_valid, error = _validate_enum_field(
            "gui-antivirus",
            payload["gui-antivirus"],
            VALID_BODY_GUI_ANTIVIRUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-webfilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-webfilter",
            payload["gui-webfilter"],
            VALID_BODY_GUI_WEBFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-videofilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-videofilter",
            payload["gui-videofilter"],
            VALID_BODY_GUI_VIDEOFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dnsfilter" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dnsfilter",
            payload["gui-dnsfilter"],
            VALID_BODY_GUI_DNSFILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-waf-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-waf-profile",
            payload["gui-waf-profile"],
            VALID_BODY_GUI_WAF_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dlp-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dlp-profile",
            payload["gui-dlp-profile"],
            VALID_BODY_GUI_DLP_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dlp-advanced" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dlp-advanced",
            payload["gui-dlp-advanced"],
            VALID_BODY_GUI_DLP_ADVANCED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-virtual-patch-profile" in payload:
        is_valid, error = _validate_enum_field(
            "gui-virtual-patch-profile",
            payload["gui-virtual-patch-profile"],
            VALID_BODY_GUI_VIRTUAL_PATCH_PROFILE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-casb" in payload:
        is_valid, error = _validate_enum_field(
            "gui-casb",
            payload["gui-casb"],
            VALID_BODY_GUI_CASB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-fortiextender-controller" in payload:
        is_valid, error = _validate_enum_field(
            "gui-fortiextender-controller",
            payload["gui-fortiextender-controller"],
            VALID_BODY_GUI_FORTIEXTENDER_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-advanced-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-advanced-policy",
            payload["gui-advanced-policy"],
            VALID_BODY_GUI_ADVANCED_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-allow-unnamed-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-allow-unnamed-policy",
            payload["gui-allow-unnamed-policy"],
            VALID_BODY_GUI_ALLOW_UNNAMED_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-email-collection" in payload:
        is_valid, error = _validate_enum_field(
            "gui-email-collection",
            payload["gui-email-collection"],
            VALID_BODY_GUI_EMAIL_COLLECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-multiple-interface-policy" in payload:
        is_valid, error = _validate_enum_field(
            "gui-multiple-interface-policy",
            payload["gui-multiple-interface-policy"],
            VALID_BODY_GUI_MULTIPLE_INTERFACE_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-policy-disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "gui-policy-disclaimer",
            payload["gui-policy-disclaimer"],
            VALID_BODY_GUI_POLICY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ztna" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ztna",
            payload["gui-ztna"],
            VALID_BODY_GUI_ZTNA,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ot" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ot",
            payload["gui-ot"],
            VALID_BODY_GUI_OT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-dynamic-device-os-id" in payload:
        is_valid, error = _validate_enum_field(
            "gui-dynamic-device-os-id",
            payload["gui-dynamic-device-os-id"],
            VALID_BODY_GUI_DYNAMIC_DEVICE_OS_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-gtp" in payload:
        is_valid, error = _validate_enum_field(
            "gui-gtp",
            payload["gui-gtp"],
            VALID_BODY_GUI_GTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-session-resume" in payload:
        is_valid, error = _validate_enum_field(
            "ike-session-resume",
            payload["ike-session-resume"],
            VALID_BODY_IKE_SESSION_RESUME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-quick-crash-detect" in payload:
        is_valid, error = _validate_enum_field(
            "ike-quick-crash-detect",
            payload["ike-quick-crash-detect"],
            VALID_BODY_IKE_QUICK_CRASH_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-dn-format" in payload:
        is_valid, error = _validate_enum_field(
            "ike-dn-format",
            payload["ike-dn-format"],
            VALID_BODY_IKE_DN_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-policy-route" in payload:
        is_valid, error = _validate_enum_field(
            "ike-policy-route",
            payload["ike-policy-route"],
            VALID_BODY_IKE_POLICY_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-detailed-event-logs" in payload:
        is_valid, error = _validate_enum_field(
            "ike-detailed-event-logs",
            payload["ike-detailed-event-logs"],
            VALID_BODY_IKE_DETAILED_EVENT_LOGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-land-attack" in payload:
        is_valid, error = _validate_enum_field(
            "block-land-attack",
            payload["block-land-attack"],
            VALID_BODY_BLOCK_LAND_ATTACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "default-app-port-as-service" in payload:
        is_valid, error = _validate_enum_field(
            "default-app-port-as-service",
            payload["default-app-port-as-service"],
            VALID_BODY_DEFAULT_APP_PORT_AS_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fqdn-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "fqdn-session-check",
            payload["fqdn-session-check"],
            VALID_BODY_FQDN_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ext-resource-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "ext-resource-session-check",
            payload["ext-resource-session-check"],
            VALID_BODY_EXT_RESOURCE_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dyn-addr-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "dyn-addr-session-check",
            payload["dyn-addr-session-check"],
            VALID_BODY_DYN_ADDR_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-enforce-change-summary" in payload:
        is_valid, error = _validate_enum_field(
            "gui-enforce-change-summary",
            payload["gui-enforce-change-summary"],
            VALID_BODY_GUI_ENFORCE_CHANGE_SUMMARY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-database-cache" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-database-cache",
            payload["internet-service-database-cache"],
            VALID_BODY_INTERNET_SERVICE_DATABASE_CACHE,
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
    "endpoint": "system/settings",
    "category": "cmdb",
    "api_path": "system/settings",
    "help": "Configure VDOM settings.",
    "total_fields": 142,
    "required_fields_count": 3,
    "fields_with_defaults_count": 140,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
