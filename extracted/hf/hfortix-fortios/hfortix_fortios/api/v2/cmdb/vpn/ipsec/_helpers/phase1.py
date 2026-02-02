"""Validation helpers for vpn/ipsec/phase1 - Auto-generated"""

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
    "interface",  # Local physical, aggregate, or VLAN outgoing interface.
    "remotegw-ddns",  # Domain name of remote gateway. For example, name.ddns.com.
    "certificate",  # Names of up to 4 signed personal certificates.
    "peerid",  # Accept this peer identity.
    "usrgrp",  # User group name for dialup peers.
    "peer",  # Accept this peer certificate.
    "peergrp",  # Accept this peer certificate group.
    "proposal",  # Phase1 proposal.
    "psksecret",  # Pre-shared secret for PSK authentication (ASCII string or hexadecimal encoded with a leading 0x).
    "psksecret-remote",  # Pre-shared secret for remote side PSK authentication (ASCII string or hexadecimal encoded with a leading 0x).
    "ppk-secret",  # IKEv2 Postquantum Preshared Key (ASCII string or hexadecimal encoded with a leading 0x).
    "authusr",  # XAuth user name.
    "authpasswd",  # XAuth password (max 35 characters).
    "group-authentication-secret",  # Password for IKEv2 ID group authentication. ASCII string or hexadecimal indicated by a leading 0x.
    "dev-id",  # Device ID carried by the device ID notification.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "type": "static",
    "interface": "",
    "ike-version": "1",
    "remote-gw": "0.0.0.0",
    "local-gw": "0.0.0.0",
    "remotegw-ddns": "",
    "keylife": 86400,
    "authmethod": "psk",
    "authmethod-remote": "",
    "mode": "main",
    "peertype": "peer",
    "peerid": "",
    "usrgrp": "",
    "peer": "",
    "peergrp": "",
    "mode-cfg": "disable",
    "mode-cfg-allow-client-selector": "disable",
    "assign-ip": "enable",
    "assign-ip-from": "range",
    "ipv4-start-ip": "0.0.0.0",
    "ipv4-end-ip": "0.0.0.0",
    "ipv4-netmask": "255.255.255.255",
    "dhcp-ra-giaddr": "0.0.0.0",
    "dhcp6-ra-linkaddr": "::",
    "dns-mode": "manual",
    "ipv4-dns-server1": "0.0.0.0",
    "ipv4-dns-server2": "0.0.0.0",
    "ipv4-dns-server3": "0.0.0.0",
    "ipv4-wins-server1": "0.0.0.0",
    "ipv4-wins-server2": "0.0.0.0",
    "ipv4-split-include": "",
    "split-include-service": "",
    "ipv4-name": "",
    "ipv6-start-ip": "::",
    "ipv6-end-ip": "::",
    "ipv6-prefix": 128,
    "ipv6-dns-server1": "::",
    "ipv6-dns-server2": "::",
    "ipv6-dns-server3": "::",
    "ipv6-split-include": "",
    "ipv6-name": "",
    "ip-delay-interval": 0,
    "unity-support": "enable",
    "domain": "",
    "include-local-lan": "disable",
    "ipv4-split-exclude": "",
    "ipv6-split-exclude": "",
    "save-password": "disable",
    "client-auto-negotiate": "disable",
    "client-keep-alive": "disable",
    "proposal": "",
    "add-route": "disable",
    "add-gw-route": "disable",
    "keepalive": 10,
    "distance": 15,
    "priority": 1,
    "localid": "",
    "localid-type": "auto",
    "auto-negotiate": "enable",
    "negotiate-timeout": 30,
    "fragmentation": "enable",
    "dpd": "on-demand",
    "dpd-retrycount": 3,
    "dpd-retryinterval": "",
    "npu-offload": "enable",
    "send-cert-chain": "enable",
    "dhgrp": "20",
    "addke1": "",
    "addke2": "",
    "addke3": "",
    "addke4": "",
    "addke5": "",
    "addke6": "",
    "addke7": "",
    "suite-b": "disable",
    "eap": "disable",
    "eap-identity": "use-id-payload",
    "eap-exclude-peergrp": "",
    "eap-cert-auth": "disable",
    "acct-verify": "disable",
    "ppk": "disable",
    "ppk-identity": "",
    "wizard-type": "custom",
    "xauthtype": "disable",
    "reauth": "disable",
    "authusr": "",
    "group-authentication": "disable",
    "authusrgrp": "",
    "mesh-selector-type": "disable",
    "idle-timeout": "disable",
    "shared-idle-timeout": "disable",
    "idle-timeoutinterval": 15,
    "ha-sync-esp-seqno": "enable",
    "fgsp-sync": "disable",
    "inbound-dscp-copy": "disable",
    "nattraversal": "enable",
    "esn": "disable",
    "fragmentation-mtu": 1200,
    "childless-ike": "disable",
    "azure-ad-autoconnect": "disable",
    "client-resume": "disable",
    "client-resume-interval": 7200,
    "rekey": "enable",
    "digital-signature-auth": "disable",
    "signature-hash-alg": "sha2-512",
    "rsa-signature-format": "pkcs1",
    "rsa-signature-hash-override": "disable",
    "enforce-unique-id": "disable",
    "cert-id-validation": "enable",
    "fec-egress": "disable",
    "fec-send-timeout": 5,
    "fec-base": 10,
    "fec-codec": "rs",
    "fec-redundant": 1,
    "fec-ingress": "disable",
    "fec-receive-timeout": 50,
    "fec-health-check": "",
    "fec-mapping-profile": "",
    "network-overlay": "disable",
    "network-id": 0,
    "dev-id-notification": "disable",
    "dev-id": "",
    "loopback-asymroute": "enable",
    "link-cost": 0,
    "kms": "",
    "exchange-fgt-device-id": "disable",
    "ipv6-auto-linklocal": "disable",
    "ems-sn-check": "disable",
    "cert-trust-store": "local",
    "qkd": "disable",
    "qkd-hybrid": "disable",
    "qkd-profile": "",
    "transport": "auto",
    "fortinet-esp": "disable",
    "auto-transport-threshold": 15,
    "remote-gw-match": "any",
    "remote-gw-subnet": "0.0.0.0 0.0.0.0",
    "remote-gw-start-ip": "0.0.0.0",
    "remote-gw-end-ip": "0.0.0.0",
    "remote-gw-country": "",
    "remote-gw6-match": "any",
    "remote-gw6-subnet": "::/0",
    "remote-gw6-start-ip": "::",
    "remote-gw6-end-ip": "::",
    "remote-gw6-country": "",
    "cert-peer-username-validation": "none",
    "cert-peer-username-strip": "disable",
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
    "name": "string",  # IPsec remote gateway name.
    "type": "option",  # Remote gateway type.
    "interface": "string",  # Local physical, aggregate, or VLAN outgoing interface.
    "ike-version": "option",  # IKE protocol version.
    "remote-gw": "ipv4-address",  # Remote VPN gateway.
    "local-gw": "ipv4-address",  # Local VPN gateway.
    "remotegw-ddns": "string",  # Domain name of remote gateway. For example, name.ddns.com.
    "keylife": "integer",  # Time to wait in seconds before phase 1 encryption key expire
    "certificate": "string",  # Names of up to 4 signed personal certificates.
    "authmethod": "option",  # Authentication method.
    "authmethod-remote": "option",  # Authentication method (remote side).
    "mode": "option",  # ID protection mode used to establish a secure channel.
    "peertype": "option",  # Accept this peer type.
    "peerid": "string",  # Accept this peer identity.
    "usrgrp": "string",  # User group name for dialup peers.
    "peer": "string",  # Accept this peer certificate.
    "peergrp": "string",  # Accept this peer certificate group.
    "mode-cfg": "option",  # Enable/disable configuration method.
    "mode-cfg-allow-client-selector": "option",  # Enable/disable mode-cfg client to use custom phase2 selector
    "assign-ip": "option",  # Enable/disable assignment of IP to IPsec interface via confi
    "assign-ip-from": "option",  # Method by which the IP address will be assigned.
    "ipv4-start-ip": "ipv4-address",  # Start of IPv4 range.
    "ipv4-end-ip": "ipv4-address",  # End of IPv4 range.
    "ipv4-netmask": "ipv4-netmask",  # IPv4 Netmask.
    "dhcp-ra-giaddr": "ipv4-address",  # Relay agent gateway IP address to use in the giaddr field of
    "dhcp6-ra-linkaddr": "ipv6-address",  # Relay agent IPv6 link address to use in DHCP6 requests.
    "dns-mode": "option",  # DNS server mode.
    "ipv4-dns-server1": "ipv4-address",  # IPv4 DNS server 1.
    "ipv4-dns-server2": "ipv4-address",  # IPv4 DNS server 2.
    "ipv4-dns-server3": "ipv4-address",  # IPv4 DNS server 3.
    "internal-domain-list": "string",  # One or more internal domain names in quotes separated by spa
    "dns-suffix-search": "string",  # One or more DNS domain name suffixes in quotes separated by 
    "ipv4-wins-server1": "ipv4-address",  # WINS server 1.
    "ipv4-wins-server2": "ipv4-address",  # WINS server 2.
    "ipv4-exclude-range": "string",  # Configuration Method IPv4 exclude ranges.
    "ipv4-split-include": "string",  # IPv4 split-include subnets.
    "split-include-service": "string",  # Split-include services.
    "ipv4-name": "string",  # IPv4 address name.
    "ipv6-start-ip": "ipv6-address",  # Start of IPv6 range.
    "ipv6-end-ip": "ipv6-address",  # End of IPv6 range.
    "ipv6-prefix": "integer",  # IPv6 prefix.
    "ipv6-dns-server1": "ipv6-address",  # IPv6 DNS server 1.
    "ipv6-dns-server2": "ipv6-address",  # IPv6 DNS server 2.
    "ipv6-dns-server3": "ipv6-address",  # IPv6 DNS server 3.
    "ipv6-exclude-range": "string",  # Configuration method IPv6 exclude ranges.
    "ipv6-split-include": "string",  # IPv6 split-include subnets.
    "ipv6-name": "string",  # IPv6 address name.
    "ip-delay-interval": "integer",  # IP address reuse delay interval in seconds (0 - 28800).
    "unity-support": "option",  # Enable/disable support for Cisco UNITY Configuration Method 
    "domain": "string",  # Instruct unity clients about the single default DNS domain.
    "banner": "var-string",  # Message that unity client should display after connecting.
    "include-local-lan": "option",  # Enable/disable allow local LAN access on unity clients.
    "ipv4-split-exclude": "string",  # IPv4 subnets that should not be sent over the IPsec tunnel.
    "ipv6-split-exclude": "string",  # IPv6 subnets that should not be sent over the IPsec tunnel.
    "save-password": "option",  # Enable/disable saving XAuth username and password on VPN cli
    "client-auto-negotiate": "option",  # Enable/disable allowing the VPN client to bring up the tunne
    "client-keep-alive": "option",  # Enable/disable allowing the VPN client to keep the tunnel up
    "backup-gateway": "string",  # Instruct unity clients about the backup gateway address(es).
    "proposal": "option",  # Phase1 proposal.
    "add-route": "option",  # Enable/disable control addition of a route to peer destinati
    "add-gw-route": "option",  # Enable/disable automatically add a route to the remote gatew
    "psksecret": "password-3",  # Pre-shared secret for PSK authentication (ASCII string or he
    "psksecret-remote": "password-3",  # Pre-shared secret for remote side PSK authentication (ASCII 
    "keepalive": "integer",  # NAT-T keep alive interval.
    "distance": "integer",  # Distance for routes added by IKE (1 - 255).
    "priority": "integer",  # Priority for routes added by IKE (1 - 65535).
    "localid": "string",  # Local ID.
    "localid-type": "option",  # Local ID type.
    "auto-negotiate": "option",  # Enable/disable automatic initiation of IKE SA negotiation.
    "negotiate-timeout": "integer",  # IKE SA negotiation timeout in seconds (1 - 300).
    "fragmentation": "option",  # Enable/disable fragment IKE message on re-transmission.
    "dpd": "option",  # Dead Peer Detection mode.
    "dpd-retrycount": "integer",  # Number of DPD retry attempts.
    "dpd-retryinterval": "user",  # DPD retry interval.
    "comments": "var-string",  # Comment.
    "npu-offload": "option",  # Enable/disable offloading NPU.
    "send-cert-chain": "option",  # Enable/disable sending certificate chain.
    "dhgrp": "option",  # DH group.
    "addke1": "option",  # ADDKE1 group.
    "addke2": "option",  # ADDKE2 group.
    "addke3": "option",  # ADDKE3 group.
    "addke4": "option",  # ADDKE4 group.
    "addke5": "option",  # ADDKE5 group.
    "addke6": "option",  # ADDKE6 group.
    "addke7": "option",  # ADDKE7 group.
    "suite-b": "option",  # Use Suite-B.
    "eap": "option",  # Enable/disable IKEv2 EAP authentication.
    "eap-identity": "option",  # IKEv2 EAP peer identity type.
    "eap-exclude-peergrp": "string",  # Peer group excluded from EAP authentication.
    "eap-cert-auth": "option",  # Enable/disable peer certificate authentication in addition t
    "acct-verify": "option",  # Enable/disable verification of RADIUS accounting record.
    "ppk": "option",  # Enable/disable IKEv2 Postquantum Preshared Key (PPK).
    "ppk-secret": "password-3",  # IKEv2 Postquantum Preshared Key (ASCII string or hexadecimal
    "ppk-identity": "string",  # IKEv2 Postquantum Preshared Key Identity.
    "wizard-type": "option",  # GUI VPN Wizard Type.
    "xauthtype": "option",  # XAuth type.
    "reauth": "option",  # Enable/disable re-authentication upon IKE SA lifetime expira
    "authusr": "string",  # XAuth user name.
    "authpasswd": "password",  # XAuth password (max 35 characters).
    "group-authentication": "option",  # Enable/disable IKEv2 IDi group authentication.
    "group-authentication-secret": "password-3",  # Password for IKEv2 ID group authentication. ASCII string or 
    "authusrgrp": "string",  # Authentication user group.
    "mesh-selector-type": "option",  # Add selectors containing subsets of the configuration depend
    "idle-timeout": "option",  # Enable/disable IPsec tunnel idle timeout.
    "shared-idle-timeout": "option",  # Enable/disable IPsec tunnel shared idle timeout.
    "idle-timeoutinterval": "integer",  # IPsec tunnel idle timeout in minutes (5 - 43200).
    "ha-sync-esp-seqno": "option",  # Enable/disable sequence number jump ahead for IPsec HA.
    "fgsp-sync": "option",  # Enable/disable IPsec syncing of tunnels for FGSP IPsec.
    "inbound-dscp-copy": "option",  # Enable/disable copy the dscp in the ESP header to the inner 
    "nattraversal": "option",  # Enable/disable NAT traversal.
    "esn": "option",  # Extended sequence number (ESN) negotiation.
    "fragmentation-mtu": "integer",  # IKE fragmentation MTU (500 - 16000).
    "childless-ike": "option",  # Enable/disable childless IKEv2 initiation (RFC 6023).
    "azure-ad-autoconnect": "option",  # Enable/disable Azure AD Auto-Connect for FortiClient.
    "client-resume": "option",  # Enable/disable resumption of offline FortiClient sessions.  
    "client-resume-interval": "integer",  # Maximum time in seconds during which a VPN client may resume
    "rekey": "option",  # Enable/disable phase1 rekey.
    "digital-signature-auth": "option",  # Enable/disable IKEv2 Digital Signature Authentication (RFC 7
    "signature-hash-alg": "option",  # Digital Signature Authentication hash algorithms.
    "rsa-signature-format": "option",  # Digital Signature Authentication RSA signature format.
    "rsa-signature-hash-override": "option",  # Enable/disable IKEv2 RSA signature hash algorithm override.
    "enforce-unique-id": "option",  # Enable/disable peer ID uniqueness check.
    "cert-id-validation": "option",  # Enable/disable cross validation of peer ID and the identity 
    "fec-egress": "option",  # Enable/disable Forward Error Correction for egress IPsec tra
    "fec-send-timeout": "integer",  # Timeout in milliseconds before sending Forward Error Correct
    "fec-base": "integer",  # Number of base Forward Error Correction packets (1 - 20).
    "fec-codec": "option",  # Forward Error Correction encoding/decoding algorithm.
    "fec-redundant": "integer",  # Number of redundant Forward Error Correction packets (1 - 5 
    "fec-ingress": "option",  # Enable/disable Forward Error Correction for ingress IPsec tr
    "fec-receive-timeout": "integer",  # Timeout in milliseconds before dropping Forward Error Correc
    "fec-health-check": "string",  # SD-WAN health check.
    "fec-mapping-profile": "string",  # Forward Error Correction (FEC) mapping profile.
    "network-overlay": "option",  # Enable/disable network overlays.
    "network-id": "integer",  # VPN gateway network ID.
    "dev-id-notification": "option",  # Enable/disable device ID notification.
    "dev-id": "string",  # Device ID carried by the device ID notification.
    "loopback-asymroute": "option",  # Enable/disable asymmetric routing for IKE traffic on loopbac
    "link-cost": "integer",  # VPN tunnel underlay link cost.
    "kms": "string",  # Key Management Services server.
    "exchange-fgt-device-id": "option",  # Enable/disable device identifier exchange with peer FortiGat
    "ipv6-auto-linklocal": "option",  # Enable/disable auto generation of IPv6 link-local address us
    "ems-sn-check": "option",  # Enable/disable verification of EMS serial number.
    "cert-trust-store": "option",  # CA certificate trust store.
    "qkd": "option",  # Enable/disable use of Quantum Key Distribution (QKD) server.
    "qkd-hybrid": "option",  # Enable/disable use of Quantum Key Distribution (QKD) hybrid 
    "qkd-profile": "string",  # Quantum Key Distribution (QKD) server profile.
    "transport": "option",  # Set IKE transport protocol.
    "fortinet-esp": "option",  # Enable/disable Fortinet ESP encapsulation.
    "auto-transport-threshold": "integer",  # Timeout in seconds before falling back to next transport pro
    "remote-gw-match": "option",  # Set type of IPv4 remote gateway address matching.
    "remote-gw-subnet": "ipv4-classnet-any",  # IPv4 address and subnet mask.
    "remote-gw-start-ip": "ipv4-address-any",  # First IPv4 address in the range.
    "remote-gw-end-ip": "ipv4-address-any",  # Last IPv4 address in the range.
    "remote-gw-country": "string",  # IPv4 addresses associated to a specific country.
    "remote-gw-ztna-tags": "string",  # IPv4 ZTNA posture tags.
    "remote-gw6-match": "option",  # Set type of IPv6 remote gateway address matching.
    "remote-gw6-subnet": "ipv6-network",  # IPv6 address and prefix.
    "remote-gw6-start-ip": "ipv6-address",  # First IPv6 address in the range.
    "remote-gw6-end-ip": "ipv6-address",  # Last IPv6 address in the range.
    "remote-gw6-country": "string",  # IPv6 addresses associated to a specific country.
    "cert-peer-username-validation": "option",  # Enable/disable cross validation of peer username and the ide
    "cert-peer-username-strip": "option",  # Enable/disable domain stripping on certificate identity.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "IPsec remote gateway name.",
    "type": "Remote gateway type.",
    "interface": "Local physical, aggregate, or VLAN outgoing interface.",
    "ike-version": "IKE protocol version.",
    "remote-gw": "Remote VPN gateway.",
    "local-gw": "Local VPN gateway.",
    "remotegw-ddns": "Domain name of remote gateway. For example, name.ddns.com.",
    "keylife": "Time to wait in seconds before phase 1 encryption key expires.",
    "certificate": "Names of up to 4 signed personal certificates.",
    "authmethod": "Authentication method.",
    "authmethod-remote": "Authentication method (remote side).",
    "mode": "ID protection mode used to establish a secure channel.",
    "peertype": "Accept this peer type.",
    "peerid": "Accept this peer identity.",
    "usrgrp": "User group name for dialup peers.",
    "peer": "Accept this peer certificate.",
    "peergrp": "Accept this peer certificate group.",
    "mode-cfg": "Enable/disable configuration method.",
    "mode-cfg-allow-client-selector": "Enable/disable mode-cfg client to use custom phase2 selectors.",
    "assign-ip": "Enable/disable assignment of IP to IPsec interface via configuration method.",
    "assign-ip-from": "Method by which the IP address will be assigned.",
    "ipv4-start-ip": "Start of IPv4 range.",
    "ipv4-end-ip": "End of IPv4 range.",
    "ipv4-netmask": "IPv4 Netmask.",
    "dhcp-ra-giaddr": "Relay agent gateway IP address to use in the giaddr field of DHCP requests.",
    "dhcp6-ra-linkaddr": "Relay agent IPv6 link address to use in DHCP6 requests.",
    "dns-mode": "DNS server mode.",
    "ipv4-dns-server1": "IPv4 DNS server 1.",
    "ipv4-dns-server2": "IPv4 DNS server 2.",
    "ipv4-dns-server3": "IPv4 DNS server 3.",
    "internal-domain-list": "One or more internal domain names in quotes separated by spaces.",
    "dns-suffix-search": "One or more DNS domain name suffixes in quotes separated by spaces.",
    "ipv4-wins-server1": "WINS server 1.",
    "ipv4-wins-server2": "WINS server 2.",
    "ipv4-exclude-range": "Configuration Method IPv4 exclude ranges.",
    "ipv4-split-include": "IPv4 split-include subnets.",
    "split-include-service": "Split-include services.",
    "ipv4-name": "IPv4 address name.",
    "ipv6-start-ip": "Start of IPv6 range.",
    "ipv6-end-ip": "End of IPv6 range.",
    "ipv6-prefix": "IPv6 prefix.",
    "ipv6-dns-server1": "IPv6 DNS server 1.",
    "ipv6-dns-server2": "IPv6 DNS server 2.",
    "ipv6-dns-server3": "IPv6 DNS server 3.",
    "ipv6-exclude-range": "Configuration method IPv6 exclude ranges.",
    "ipv6-split-include": "IPv6 split-include subnets.",
    "ipv6-name": "IPv6 address name.",
    "ip-delay-interval": "IP address reuse delay interval in seconds (0 - 28800).",
    "unity-support": "Enable/disable support for Cisco UNITY Configuration Method extensions.",
    "domain": "Instruct unity clients about the single default DNS domain.",
    "banner": "Message that unity client should display after connecting.",
    "include-local-lan": "Enable/disable allow local LAN access on unity clients.",
    "ipv4-split-exclude": "IPv4 subnets that should not be sent over the IPsec tunnel.",
    "ipv6-split-exclude": "IPv6 subnets that should not be sent over the IPsec tunnel.",
    "save-password": "Enable/disable saving XAuth username and password on VPN clients.",
    "client-auto-negotiate": "Enable/disable allowing the VPN client to bring up the tunnel when there is no traffic.",
    "client-keep-alive": "Enable/disable allowing the VPN client to keep the tunnel up when there is no traffic.",
    "backup-gateway": "Instruct unity clients about the backup gateway address(es).",
    "proposal": "Phase1 proposal.",
    "add-route": "Enable/disable control addition of a route to peer destination selector.",
    "add-gw-route": "Enable/disable automatically add a route to the remote gateway.",
    "psksecret": "Pre-shared secret for PSK authentication (ASCII string or hexadecimal encoded with a leading 0x).",
    "psksecret-remote": "Pre-shared secret for remote side PSK authentication (ASCII string or hexadecimal encoded with a leading 0x).",
    "keepalive": "NAT-T keep alive interval.",
    "distance": "Distance for routes added by IKE (1 - 255).",
    "priority": "Priority for routes added by IKE (1 - 65535).",
    "localid": "Local ID.",
    "localid-type": "Local ID type.",
    "auto-negotiate": "Enable/disable automatic initiation of IKE SA negotiation.",
    "negotiate-timeout": "IKE SA negotiation timeout in seconds (1 - 300).",
    "fragmentation": "Enable/disable fragment IKE message on re-transmission.",
    "dpd": "Dead Peer Detection mode.",
    "dpd-retrycount": "Number of DPD retry attempts.",
    "dpd-retryinterval": "DPD retry interval.",
    "comments": "Comment.",
    "npu-offload": "Enable/disable offloading NPU.",
    "send-cert-chain": "Enable/disable sending certificate chain.",
    "dhgrp": "DH group.",
    "addke1": "ADDKE1 group.",
    "addke2": "ADDKE2 group.",
    "addke3": "ADDKE3 group.",
    "addke4": "ADDKE4 group.",
    "addke5": "ADDKE5 group.",
    "addke6": "ADDKE6 group.",
    "addke7": "ADDKE7 group.",
    "suite-b": "Use Suite-B.",
    "eap": "Enable/disable IKEv2 EAP authentication.",
    "eap-identity": "IKEv2 EAP peer identity type.",
    "eap-exclude-peergrp": "Peer group excluded from EAP authentication.",
    "eap-cert-auth": "Enable/disable peer certificate authentication in addition to EAP if peer is a FortiClient endpoint.",
    "acct-verify": "Enable/disable verification of RADIUS accounting record.",
    "ppk": "Enable/disable IKEv2 Postquantum Preshared Key (PPK).",
    "ppk-secret": "IKEv2 Postquantum Preshared Key (ASCII string or hexadecimal encoded with a leading 0x).",
    "ppk-identity": "IKEv2 Postquantum Preshared Key Identity.",
    "wizard-type": "GUI VPN Wizard Type.",
    "xauthtype": "XAuth type.",
    "reauth": "Enable/disable re-authentication upon IKE SA lifetime expiration.",
    "authusr": "XAuth user name.",
    "authpasswd": "XAuth password (max 35 characters).",
    "group-authentication": "Enable/disable IKEv2 IDi group authentication.",
    "group-authentication-secret": "Password for IKEv2 ID group authentication. ASCII string or hexadecimal indicated by a leading 0x.",
    "authusrgrp": "Authentication user group.",
    "mesh-selector-type": "Add selectors containing subsets of the configuration depending on traffic.",
    "idle-timeout": "Enable/disable IPsec tunnel idle timeout.",
    "shared-idle-timeout": "Enable/disable IPsec tunnel shared idle timeout.",
    "idle-timeoutinterval": "IPsec tunnel idle timeout in minutes (5 - 43200).",
    "ha-sync-esp-seqno": "Enable/disable sequence number jump ahead for IPsec HA.",
    "fgsp-sync": "Enable/disable IPsec syncing of tunnels for FGSP IPsec.",
    "inbound-dscp-copy": "Enable/disable copy the dscp in the ESP header to the inner IP Header.",
    "nattraversal": "Enable/disable NAT traversal.",
    "esn": "Extended sequence number (ESN) negotiation.",
    "fragmentation-mtu": "IKE fragmentation MTU (500 - 16000).",
    "childless-ike": "Enable/disable childless IKEv2 initiation (RFC 6023).",
    "azure-ad-autoconnect": "Enable/disable Azure AD Auto-Connect for FortiClient.",
    "client-resume": "Enable/disable resumption of offline FortiClient sessions.  When a FortiClient enabled laptop is closed or enters sleep/hibernate mode, enabling this feature allows FortiClient to keep the tunnel during this period, and allows users to immediately resume using the IPsec tunnel when the device wakes up.",
    "client-resume-interval": "Maximum time in seconds during which a VPN client may resume using a tunnel after a client PC has entered sleep mode or temporarily lost its network connection (120 - 172800, default = 7200).",
    "rekey": "Enable/disable phase1 rekey.",
    "digital-signature-auth": "Enable/disable IKEv2 Digital Signature Authentication (RFC 7427).",
    "signature-hash-alg": "Digital Signature Authentication hash algorithms.",
    "rsa-signature-format": "Digital Signature Authentication RSA signature format.",
    "rsa-signature-hash-override": "Enable/disable IKEv2 RSA signature hash algorithm override.",
    "enforce-unique-id": "Enable/disable peer ID uniqueness check.",
    "cert-id-validation": "Enable/disable cross validation of peer ID and the identity in the peer's certificate as specified in RFC 4945.",
    "fec-egress": "Enable/disable Forward Error Correction for egress IPsec traffic.",
    "fec-send-timeout": "Timeout in milliseconds before sending Forward Error Correction packets (1 - 1000).",
    "fec-base": "Number of base Forward Error Correction packets (1 - 20).",
    "fec-codec": "Forward Error Correction encoding/decoding algorithm.",
    "fec-redundant": "Number of redundant Forward Error Correction packets (1 - 5 for reed-solomon, 1 for xor).",
    "fec-ingress": "Enable/disable Forward Error Correction for ingress IPsec traffic.",
    "fec-receive-timeout": "Timeout in milliseconds before dropping Forward Error Correction packets (1 - 1000).",
    "fec-health-check": "SD-WAN health check.",
    "fec-mapping-profile": "Forward Error Correction (FEC) mapping profile.",
    "network-overlay": "Enable/disable network overlays.",
    "network-id": "VPN gateway network ID.",
    "dev-id-notification": "Enable/disable device ID notification.",
    "dev-id": "Device ID carried by the device ID notification.",
    "loopback-asymroute": "Enable/disable asymmetric routing for IKE traffic on loopback interface.",
    "link-cost": "VPN tunnel underlay link cost.",
    "kms": "Key Management Services server.",
    "exchange-fgt-device-id": "Enable/disable device identifier exchange with peer FortiGate units for use of VPN monitor data by FortiManager.",
    "ipv6-auto-linklocal": "Enable/disable auto generation of IPv6 link-local address using last 8 bytes of mode-cfg assigned IPv6 address.",
    "ems-sn-check": "Enable/disable verification of EMS serial number.",
    "cert-trust-store": "CA certificate trust store.",
    "qkd": "Enable/disable use of Quantum Key Distribution (QKD) server.",
    "qkd-hybrid": "Enable/disable use of Quantum Key Distribution (QKD) hybrid keys.",
    "qkd-profile": "Quantum Key Distribution (QKD) server profile.",
    "transport": "Set IKE transport protocol.",
    "fortinet-esp": "Enable/disable Fortinet ESP encapsulation.",
    "auto-transport-threshold": "Timeout in seconds before falling back to next transport protocol.",
    "remote-gw-match": "Set type of IPv4 remote gateway address matching.",
    "remote-gw-subnet": "IPv4 address and subnet mask.",
    "remote-gw-start-ip": "First IPv4 address in the range.",
    "remote-gw-end-ip": "Last IPv4 address in the range.",
    "remote-gw-country": "IPv4 addresses associated to a specific country.",
    "remote-gw-ztna-tags": "IPv4 ZTNA posture tags.",
    "remote-gw6-match": "Set type of IPv6 remote gateway address matching.",
    "remote-gw6-subnet": "IPv6 address and prefix.",
    "remote-gw6-start-ip": "First IPv6 address in the range.",
    "remote-gw6-end-ip": "Last IPv6 address in the range.",
    "remote-gw6-country": "IPv6 addresses associated to a specific country.",
    "cert-peer-username-validation": "Enable/disable cross validation of peer username and the identity in the peer's certificate.",
    "cert-peer-username-strip": "Enable/disable domain stripping on certificate identity.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 35},
    "interface": {"type": "string", "max_length": 35},
    "remotegw-ddns": {"type": "string", "max_length": 63},
    "keylife": {"type": "integer", "min": 120, "max": 172800},
    "peerid": {"type": "string", "max_length": 255},
    "usrgrp": {"type": "string", "max_length": 35},
    "peer": {"type": "string", "max_length": 35},
    "peergrp": {"type": "string", "max_length": 35},
    "ipv4-split-include": {"type": "string", "max_length": 79},
    "split-include-service": {"type": "string", "max_length": 79},
    "ipv4-name": {"type": "string", "max_length": 79},
    "ipv6-prefix": {"type": "integer", "min": 1, "max": 128},
    "ipv6-split-include": {"type": "string", "max_length": 79},
    "ipv6-name": {"type": "string", "max_length": 79},
    "ip-delay-interval": {"type": "integer", "min": 0, "max": 28800},
    "domain": {"type": "string", "max_length": 63},
    "ipv4-split-exclude": {"type": "string", "max_length": 79},
    "ipv6-split-exclude": {"type": "string", "max_length": 79},
    "keepalive": {"type": "integer", "min": 5, "max": 900},
    "distance": {"type": "integer", "min": 1, "max": 255},
    "priority": {"type": "integer", "min": 1, "max": 65535},
    "localid": {"type": "string", "max_length": 63},
    "negotiate-timeout": {"type": "integer", "min": 1, "max": 300},
    "dpd-retrycount": {"type": "integer", "min": 1, "max": 10},
    "eap-exclude-peergrp": {"type": "string", "max_length": 35},
    "ppk-identity": {"type": "string", "max_length": 35},
    "authusr": {"type": "string", "max_length": 64},
    "authusrgrp": {"type": "string", "max_length": 35},
    "idle-timeoutinterval": {"type": "integer", "min": 5, "max": 43200},
    "fragmentation-mtu": {"type": "integer", "min": 500, "max": 16000},
    "client-resume-interval": {"type": "integer", "min": 120, "max": 172800},
    "fec-send-timeout": {"type": "integer", "min": 1, "max": 1000},
    "fec-base": {"type": "integer", "min": 1, "max": 20},
    "fec-redundant": {"type": "integer", "min": 1, "max": 5},
    "fec-receive-timeout": {"type": "integer", "min": 1, "max": 1000},
    "fec-health-check": {"type": "string", "max_length": 35},
    "fec-mapping-profile": {"type": "string", "max_length": 35},
    "network-id": {"type": "integer", "min": 0, "max": 255},
    "dev-id": {"type": "string", "max_length": 63},
    "link-cost": {"type": "integer", "min": 0, "max": 255},
    "kms": {"type": "string", "max_length": 35},
    "qkd-profile": {"type": "string", "max_length": 35},
    "auto-transport-threshold": {"type": "integer", "min": 1, "max": 300},
    "remote-gw-country": {"type": "string", "max_length": 2},
    "remote-gw6-country": {"type": "string", "max_length": 2},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "certificate": {
        "name": {
            "type": "string",
            "help": "Certificate name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internal-domain-list": {
        "domain-name": {
            "type": "string",
            "help": "Domain name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dns-suffix-search": {
        "dns-suffix": {
            "type": "string",
            "help": "DNS suffix.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "ipv4-exclude-range": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "start-ip": {
            "type": "ipv4-address",
            "help": "Start of IPv4 exclusive range.",
            "required": True,
            "default": "0.0.0.0",
        },
        "end-ip": {
            "type": "ipv4-address",
            "help": "End of IPv4 exclusive range.",
            "required": True,
            "default": "0.0.0.0",
        },
    },
    "ipv6-exclude-range": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "start-ip": {
            "type": "ipv6-address",
            "help": "Start of IPv6 exclusive range.",
            "required": True,
            "default": "::",
        },
        "end-ip": {
            "type": "ipv6-address",
            "help": "End of IPv6 exclusive range.",
            "required": True,
            "default": "::",
        },
    },
    "backup-gateway": {
        "address": {
            "type": "string",
            "help": "Address of backup gateway.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "remote-gw-ztna-tags": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "static",
    "dynamic",
    "ddns",
]
VALID_BODY_IKE_VERSION = [
    "1",
    "2",
]
VALID_BODY_AUTHMETHOD = [
    "psk",
    "signature",
]
VALID_BODY_AUTHMETHOD_REMOTE = [
    "psk",
    "signature",
]
VALID_BODY_MODE = [
    "aggressive",
    "main",
]
VALID_BODY_PEERTYPE = [
    "any",
    "one",
    "dialup",
    "peer",
    "peergrp",
]
VALID_BODY_MODE_CFG = [
    "disable",
    "enable",
]
VALID_BODY_MODE_CFG_ALLOW_CLIENT_SELECTOR = [
    "disable",
    "enable",
]
VALID_BODY_ASSIGN_IP = [
    "disable",
    "enable",
]
VALID_BODY_ASSIGN_IP_FROM = [
    "range",
    "usrgrp",
    "dhcp",
    "name",
]
VALID_BODY_DNS_MODE = [
    "manual",
    "auto",
]
VALID_BODY_UNITY_SUPPORT = [
    "disable",
    "enable",
]
VALID_BODY_INCLUDE_LOCAL_LAN = [
    "disable",
    "enable",
]
VALID_BODY_SAVE_PASSWORD = [
    "disable",
    "enable",
]
VALID_BODY_CLIENT_AUTO_NEGOTIATE = [
    "disable",
    "enable",
]
VALID_BODY_CLIENT_KEEP_ALIVE = [
    "disable",
    "enable",
]
VALID_BODY_PROPOSAL = [
    "des-md5",
    "des-sha1",
    "des-sha256",
    "des-sha384",
    "des-sha512",
    "3des-md5",
    "3des-sha1",
    "3des-sha256",
    "3des-sha384",
    "3des-sha512",
    "aes128-md5",
    "aes128-sha1",
    "aes128-sha256",
    "aes128-sha384",
    "aes128-sha512",
    "aes128gcm-prfsha1",
    "aes128gcm-prfsha256",
    "aes128gcm-prfsha384",
    "aes128gcm-prfsha512",
    "aes192-md5",
    "aes192-sha1",
    "aes192-sha256",
    "aes192-sha384",
    "aes192-sha512",
    "aes256-md5",
    "aes256-sha1",
    "aes256-sha256",
    "aes256-sha384",
    "aes256-sha512",
    "aes256gcm-prfsha1",
    "aes256gcm-prfsha256",
    "aes256gcm-prfsha384",
    "aes256gcm-prfsha512",
    "chacha20poly1305-prfsha1",
    "chacha20poly1305-prfsha256",
    "chacha20poly1305-prfsha384",
    "chacha20poly1305-prfsha512",
    "aria128-md5",
    "aria128-sha1",
    "aria128-sha256",
    "aria128-sha384",
    "aria128-sha512",
    "aria192-md5",
    "aria192-sha1",
    "aria192-sha256",
    "aria192-sha384",
    "aria192-sha512",
    "aria256-md5",
    "aria256-sha1",
    "aria256-sha256",
    "aria256-sha384",
    "aria256-sha512",
    "seed-md5",
    "seed-sha1",
    "seed-sha256",
    "seed-sha384",
    "seed-sha512",
]
VALID_BODY_ADD_ROUTE = [
    "disable",
    "enable",
]
VALID_BODY_ADD_GW_ROUTE = [
    "enable",
    "disable",
]
VALID_BODY_LOCALID_TYPE = [
    "auto",
    "fqdn",
    "user-fqdn",
    "keyid",
    "address",
    "asn1dn",
]
VALID_BODY_AUTO_NEGOTIATE = [
    "enable",
    "disable",
]
VALID_BODY_FRAGMENTATION = [
    "enable",
    "disable",
]
VALID_BODY_DPD = [
    "disable",
    "on-idle",
    "on-demand",
]
VALID_BODY_NPU_OFFLOAD = [
    "enable",
    "disable",
]
VALID_BODY_SEND_CERT_CHAIN = [
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
VALID_BODY_SUITE_B = [
    "disable",
    "suite-b-gcm-128",
    "suite-b-gcm-256",
]
VALID_BODY_EAP = [
    "enable",
    "disable",
]
VALID_BODY_EAP_IDENTITY = [
    "use-id-payload",
    "send-request",
]
VALID_BODY_EAP_CERT_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_ACCT_VERIFY = [
    "enable",
    "disable",
]
VALID_BODY_PPK = [
    "disable",
    "allow",
    "require",
]
VALID_BODY_WIZARD_TYPE = [
    "custom",
    "dialup-forticlient",
    "dialup-ios",
    "dialup-android",
    "dialup-windows",
    "dialup-cisco",
    "static-fortigate",
    "dialup-fortigate",
    "static-cisco",
    "dialup-cisco-fw",
    "simplified-static-fortigate",
    "hub-fortigate-auto-discovery",
    "spoke-fortigate-auto-discovery",
    "fabric-overlay-orchestrator",
]
VALID_BODY_XAUTHTYPE = [
    "disable",
    "client",
    "pap",
    "chap",
    "auto",
]
VALID_BODY_REAUTH = [
    "disable",
    "enable",
]
VALID_BODY_GROUP_AUTHENTICATION = [
    "enable",
    "disable",
]
VALID_BODY_MESH_SELECTOR_TYPE = [
    "disable",
    "subnet",
    "host",
]
VALID_BODY_IDLE_TIMEOUT = [
    "enable",
    "disable",
]
VALID_BODY_SHARED_IDLE_TIMEOUT = [
    "enable",
    "disable",
]
VALID_BODY_HA_SYNC_ESP_SEQNO = [
    "enable",
    "disable",
]
VALID_BODY_FGSP_SYNC = [
    "enable",
    "disable",
]
VALID_BODY_INBOUND_DSCP_COPY = [
    "enable",
    "disable",
]
VALID_BODY_NATTRAVERSAL = [
    "enable",
    "disable",
    "forced",
]
VALID_BODY_ESN = [
    "require",
    "allow",
    "disable",
]
VALID_BODY_CHILDLESS_IKE = [
    "enable",
    "disable",
]
VALID_BODY_AZURE_AD_AUTOCONNECT = [
    "enable",
    "disable",
]
VALID_BODY_CLIENT_RESUME = [
    "enable",
    "disable",
]
VALID_BODY_REKEY = [
    "enable",
    "disable",
]
VALID_BODY_DIGITAL_SIGNATURE_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_SIGNATURE_HASH_ALG = [
    "sha1",
    "sha2-256",
    "sha2-384",
    "sha2-512",
]
VALID_BODY_RSA_SIGNATURE_FORMAT = [
    "pkcs1",
    "pss",
]
VALID_BODY_RSA_SIGNATURE_HASH_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_ENFORCE_UNIQUE_ID = [
    "disable",
    "keep-new",
    "keep-old",
]
VALID_BODY_CERT_ID_VALIDATION = [
    "enable",
    "disable",
]
VALID_BODY_FEC_EGRESS = [
    "enable",
    "disable",
]
VALID_BODY_FEC_CODEC = [
    "rs",
    "xor",
]
VALID_BODY_FEC_INGRESS = [
    "enable",
    "disable",
]
VALID_BODY_NETWORK_OVERLAY = [
    "disable",
    "enable",
]
VALID_BODY_DEV_ID_NOTIFICATION = [
    "disable",
    "enable",
]
VALID_BODY_LOOPBACK_ASYMROUTE = [
    "enable",
    "disable",
]
VALID_BODY_EXCHANGE_FGT_DEVICE_ID = [
    "enable",
    "disable",
]
VALID_BODY_IPV6_AUTO_LINKLOCAL = [
    "enable",
    "disable",
]
VALID_BODY_EMS_SN_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_CERT_TRUST_STORE = [
    "local",
    "ems",
]
VALID_BODY_QKD = [
    "disable",
    "allow",
    "require",
]
VALID_BODY_QKD_HYBRID = [
    "disable",
    "allow",
    "require",
]
VALID_BODY_TRANSPORT = [
    "udp",
    "auto",
    "tcp",
]
VALID_BODY_FORTINET_ESP = [
    "enable",
    "disable",
]
VALID_BODY_REMOTE_GW_MATCH = [
    "any",
    "ipmask",
    "iprange",
    "geography",
    "ztna",
]
VALID_BODY_REMOTE_GW6_MATCH = [
    "any",
    "ipprefix",
    "iprange",
    "geography",
]
VALID_BODY_CERT_PEER_USERNAME_VALIDATION = [
    "none",
    "othername",
    "rfc822name",
    "cn",
]
VALID_BODY_CERT_PEER_USERNAME_STRIP = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_vpn_ipsec_phase1_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for vpn/ipsec/phase1."""
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


def validate_vpn_ipsec_phase1_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new vpn/ipsec/phase1 object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-version" in payload:
        is_valid, error = _validate_enum_field(
            "ike-version",
            payload["ike-version"],
            VALID_BODY_IKE_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authmethod" in payload:
        is_valid, error = _validate_enum_field(
            "authmethod",
            payload["authmethod"],
            VALID_BODY_AUTHMETHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authmethod-remote" in payload:
        is_valid, error = _validate_enum_field(
            "authmethod-remote",
            payload["authmethod-remote"],
            VALID_BODY_AUTHMETHOD_REMOTE,
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
    if "peertype" in payload:
        is_valid, error = _validate_enum_field(
            "peertype",
            payload["peertype"],
            VALID_BODY_PEERTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mode-cfg" in payload:
        is_valid, error = _validate_enum_field(
            "mode-cfg",
            payload["mode-cfg"],
            VALID_BODY_MODE_CFG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mode-cfg-allow-client-selector" in payload:
        is_valid, error = _validate_enum_field(
            "mode-cfg-allow-client-selector",
            payload["mode-cfg-allow-client-selector"],
            VALID_BODY_MODE_CFG_ALLOW_CLIENT_SELECTOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assign-ip" in payload:
        is_valid, error = _validate_enum_field(
            "assign-ip",
            payload["assign-ip"],
            VALID_BODY_ASSIGN_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assign-ip-from" in payload:
        is_valid, error = _validate_enum_field(
            "assign-ip-from",
            payload["assign-ip-from"],
            VALID_BODY_ASSIGN_IP_FROM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-mode" in payload:
        is_valid, error = _validate_enum_field(
            "dns-mode",
            payload["dns-mode"],
            VALID_BODY_DNS_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unity-support" in payload:
        is_valid, error = _validate_enum_field(
            "unity-support",
            payload["unity-support"],
            VALID_BODY_UNITY_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-local-lan" in payload:
        is_valid, error = _validate_enum_field(
            "include-local-lan",
            payload["include-local-lan"],
            VALID_BODY_INCLUDE_LOCAL_LAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "save-password" in payload:
        is_valid, error = _validate_enum_field(
            "save-password",
            payload["save-password"],
            VALID_BODY_SAVE_PASSWORD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-auto-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "client-auto-negotiate",
            payload["client-auto-negotiate"],
            VALID_BODY_CLIENT_AUTO_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-keep-alive" in payload:
        is_valid, error = _validate_enum_field(
            "client-keep-alive",
            payload["client-keep-alive"],
            VALID_BODY_CLIENT_KEEP_ALIVE,
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
    if "add-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-route",
            payload["add-route"],
            VALID_BODY_ADD_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-gw-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-gw-route",
            payload["add-gw-route"],
            VALID_BODY_ADD_GW_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "localid-type" in payload:
        is_valid, error = _validate_enum_field(
            "localid-type",
            payload["localid-type"],
            VALID_BODY_LOCALID_TYPE,
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
    if "fragmentation" in payload:
        is_valid, error = _validate_enum_field(
            "fragmentation",
            payload["fragmentation"],
            VALID_BODY_FRAGMENTATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dpd" in payload:
        is_valid, error = _validate_enum_field(
            "dpd",
            payload["dpd"],
            VALID_BODY_DPD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-offload" in payload:
        is_valid, error = _validate_enum_field(
            "npu-offload",
            payload["npu-offload"],
            VALID_BODY_NPU_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-cert-chain" in payload:
        is_valid, error = _validate_enum_field(
            "send-cert-chain",
            payload["send-cert-chain"],
            VALID_BODY_SEND_CERT_CHAIN,
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
    if "suite-b" in payload:
        is_valid, error = _validate_enum_field(
            "suite-b",
            payload["suite-b"],
            VALID_BODY_SUITE_B,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap" in payload:
        is_valid, error = _validate_enum_field(
            "eap",
            payload["eap"],
            VALID_BODY_EAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-identity" in payload:
        is_valid, error = _validate_enum_field(
            "eap-identity",
            payload["eap-identity"],
            VALID_BODY_EAP_IDENTITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "eap-cert-auth",
            payload["eap-cert-auth"],
            VALID_BODY_EAP_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "acct-verify" in payload:
        is_valid, error = _validate_enum_field(
            "acct-verify",
            payload["acct-verify"],
            VALID_BODY_ACCT_VERIFY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppk" in payload:
        is_valid, error = _validate_enum_field(
            "ppk",
            payload["ppk"],
            VALID_BODY_PPK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wizard-type" in payload:
        is_valid, error = _validate_enum_field(
            "wizard-type",
            payload["wizard-type"],
            VALID_BODY_WIZARD_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "xauthtype" in payload:
        is_valid, error = _validate_enum_field(
            "xauthtype",
            payload["xauthtype"],
            VALID_BODY_XAUTHTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reauth" in payload:
        is_valid, error = _validate_enum_field(
            "reauth",
            payload["reauth"],
            VALID_BODY_REAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "group-authentication",
            payload["group-authentication"],
            VALID_BODY_GROUP_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mesh-selector-type" in payload:
        is_valid, error = _validate_enum_field(
            "mesh-selector-type",
            payload["mesh-selector-type"],
            VALID_BODY_MESH_SELECTOR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "idle-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "idle-timeout",
            payload["idle-timeout"],
            VALID_BODY_IDLE_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "shared-idle-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "shared-idle-timeout",
            payload["shared-idle-timeout"],
            VALID_BODY_SHARED_IDLE_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-sync-esp-seqno" in payload:
        is_valid, error = _validate_enum_field(
            "ha-sync-esp-seqno",
            payload["ha-sync-esp-seqno"],
            VALID_BODY_HA_SYNC_ESP_SEQNO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fgsp-sync" in payload:
        is_valid, error = _validate_enum_field(
            "fgsp-sync",
            payload["fgsp-sync"],
            VALID_BODY_FGSP_SYNC,
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
    if "nattraversal" in payload:
        is_valid, error = _validate_enum_field(
            "nattraversal",
            payload["nattraversal"],
            VALID_BODY_NATTRAVERSAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "esn" in payload:
        is_valid, error = _validate_enum_field(
            "esn",
            payload["esn"],
            VALID_BODY_ESN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "childless-ike" in payload:
        is_valid, error = _validate_enum_field(
            "childless-ike",
            payload["childless-ike"],
            VALID_BODY_CHILDLESS_IKE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "azure-ad-autoconnect" in payload:
        is_valid, error = _validate_enum_field(
            "azure-ad-autoconnect",
            payload["azure-ad-autoconnect"],
            VALID_BODY_AZURE_AD_AUTOCONNECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-resume" in payload:
        is_valid, error = _validate_enum_field(
            "client-resume",
            payload["client-resume"],
            VALID_BODY_CLIENT_RESUME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rekey" in payload:
        is_valid, error = _validate_enum_field(
            "rekey",
            payload["rekey"],
            VALID_BODY_REKEY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digital-signature-auth" in payload:
        is_valid, error = _validate_enum_field(
            "digital-signature-auth",
            payload["digital-signature-auth"],
            VALID_BODY_DIGITAL_SIGNATURE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "signature-hash-alg" in payload:
        is_valid, error = _validate_enum_field(
            "signature-hash-alg",
            payload["signature-hash-alg"],
            VALID_BODY_SIGNATURE_HASH_ALG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsa-signature-format" in payload:
        is_valid, error = _validate_enum_field(
            "rsa-signature-format",
            payload["rsa-signature-format"],
            VALID_BODY_RSA_SIGNATURE_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsa-signature-hash-override" in payload:
        is_valid, error = _validate_enum_field(
            "rsa-signature-hash-override",
            payload["rsa-signature-hash-override"],
            VALID_BODY_RSA_SIGNATURE_HASH_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-unique-id" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-unique-id",
            payload["enforce-unique-id"],
            VALID_BODY_ENFORCE_UNIQUE_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-id-validation" in payload:
        is_valid, error = _validate_enum_field(
            "cert-id-validation",
            payload["cert-id-validation"],
            VALID_BODY_CERT_ID_VALIDATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec-egress" in payload:
        is_valid, error = _validate_enum_field(
            "fec-egress",
            payload["fec-egress"],
            VALID_BODY_FEC_EGRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec-codec" in payload:
        is_valid, error = _validate_enum_field(
            "fec-codec",
            payload["fec-codec"],
            VALID_BODY_FEC_CODEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec-ingress" in payload:
        is_valid, error = _validate_enum_field(
            "fec-ingress",
            payload["fec-ingress"],
            VALID_BODY_FEC_INGRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "network-overlay" in payload:
        is_valid, error = _validate_enum_field(
            "network-overlay",
            payload["network-overlay"],
            VALID_BODY_NETWORK_OVERLAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dev-id-notification" in payload:
        is_valid, error = _validate_enum_field(
            "dev-id-notification",
            payload["dev-id-notification"],
            VALID_BODY_DEV_ID_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "loopback-asymroute" in payload:
        is_valid, error = _validate_enum_field(
            "loopback-asymroute",
            payload["loopback-asymroute"],
            VALID_BODY_LOOPBACK_ASYMROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "exchange-fgt-device-id" in payload:
        is_valid, error = _validate_enum_field(
            "exchange-fgt-device-id",
            payload["exchange-fgt-device-id"],
            VALID_BODY_EXCHANGE_FGT_DEVICE_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-auto-linklocal" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-auto-linklocal",
            payload["ipv6-auto-linklocal"],
            VALID_BODY_IPV6_AUTO_LINKLOCAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ems-sn-check" in payload:
        is_valid, error = _validate_enum_field(
            "ems-sn-check",
            payload["ems-sn-check"],
            VALID_BODY_EMS_SN_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-trust-store" in payload:
        is_valid, error = _validate_enum_field(
            "cert-trust-store",
            payload["cert-trust-store"],
            VALID_BODY_CERT_TRUST_STORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "qkd" in payload:
        is_valid, error = _validate_enum_field(
            "qkd",
            payload["qkd"],
            VALID_BODY_QKD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "qkd-hybrid" in payload:
        is_valid, error = _validate_enum_field(
            "qkd-hybrid",
            payload["qkd-hybrid"],
            VALID_BODY_QKD_HYBRID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transport" in payload:
        is_valid, error = _validate_enum_field(
            "transport",
            payload["transport"],
            VALID_BODY_TRANSPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortinet-esp" in payload:
        is_valid, error = _validate_enum_field(
            "fortinet-esp",
            payload["fortinet-esp"],
            VALID_BODY_FORTINET_ESP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "remote-gw-match" in payload:
        is_valid, error = _validate_enum_field(
            "remote-gw-match",
            payload["remote-gw-match"],
            VALID_BODY_REMOTE_GW_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "remote-gw6-match" in payload:
        is_valid, error = _validate_enum_field(
            "remote-gw6-match",
            payload["remote-gw6-match"],
            VALID_BODY_REMOTE_GW6_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-peer-username-validation" in payload:
        is_valid, error = _validate_enum_field(
            "cert-peer-username-validation",
            payload["cert-peer-username-validation"],
            VALID_BODY_CERT_PEER_USERNAME_VALIDATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-peer-username-strip" in payload:
        is_valid, error = _validate_enum_field(
            "cert-peer-username-strip",
            payload["cert-peer-username-strip"],
            VALID_BODY_CERT_PEER_USERNAME_STRIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_vpn_ipsec_phase1_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update vpn/ipsec/phase1."""
    # Validate enum values using central function
    if "type" in payload:
        is_valid, error = _validate_enum_field(
            "type",
            payload["type"],
            VALID_BODY_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ike-version" in payload:
        is_valid, error = _validate_enum_field(
            "ike-version",
            payload["ike-version"],
            VALID_BODY_IKE_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authmethod" in payload:
        is_valid, error = _validate_enum_field(
            "authmethod",
            payload["authmethod"],
            VALID_BODY_AUTHMETHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authmethod-remote" in payload:
        is_valid, error = _validate_enum_field(
            "authmethod-remote",
            payload["authmethod-remote"],
            VALID_BODY_AUTHMETHOD_REMOTE,
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
    if "peertype" in payload:
        is_valid, error = _validate_enum_field(
            "peertype",
            payload["peertype"],
            VALID_BODY_PEERTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mode-cfg" in payload:
        is_valid, error = _validate_enum_field(
            "mode-cfg",
            payload["mode-cfg"],
            VALID_BODY_MODE_CFG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mode-cfg-allow-client-selector" in payload:
        is_valid, error = _validate_enum_field(
            "mode-cfg-allow-client-selector",
            payload["mode-cfg-allow-client-selector"],
            VALID_BODY_MODE_CFG_ALLOW_CLIENT_SELECTOR,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assign-ip" in payload:
        is_valid, error = _validate_enum_field(
            "assign-ip",
            payload["assign-ip"],
            VALID_BODY_ASSIGN_IP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "assign-ip-from" in payload:
        is_valid, error = _validate_enum_field(
            "assign-ip-from",
            payload["assign-ip-from"],
            VALID_BODY_ASSIGN_IP_FROM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dns-mode" in payload:
        is_valid, error = _validate_enum_field(
            "dns-mode",
            payload["dns-mode"],
            VALID_BODY_DNS_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unity-support" in payload:
        is_valid, error = _validate_enum_field(
            "unity-support",
            payload["unity-support"],
            VALID_BODY_UNITY_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "include-local-lan" in payload:
        is_valid, error = _validate_enum_field(
            "include-local-lan",
            payload["include-local-lan"],
            VALID_BODY_INCLUDE_LOCAL_LAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "save-password" in payload:
        is_valid, error = _validate_enum_field(
            "save-password",
            payload["save-password"],
            VALID_BODY_SAVE_PASSWORD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-auto-negotiate" in payload:
        is_valid, error = _validate_enum_field(
            "client-auto-negotiate",
            payload["client-auto-negotiate"],
            VALID_BODY_CLIENT_AUTO_NEGOTIATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-keep-alive" in payload:
        is_valid, error = _validate_enum_field(
            "client-keep-alive",
            payload["client-keep-alive"],
            VALID_BODY_CLIENT_KEEP_ALIVE,
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
    if "add-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-route",
            payload["add-route"],
            VALID_BODY_ADD_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-gw-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-gw-route",
            payload["add-gw-route"],
            VALID_BODY_ADD_GW_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "localid-type" in payload:
        is_valid, error = _validate_enum_field(
            "localid-type",
            payload["localid-type"],
            VALID_BODY_LOCALID_TYPE,
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
    if "fragmentation" in payload:
        is_valid, error = _validate_enum_field(
            "fragmentation",
            payload["fragmentation"],
            VALID_BODY_FRAGMENTATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dpd" in payload:
        is_valid, error = _validate_enum_field(
            "dpd",
            payload["dpd"],
            VALID_BODY_DPD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-offload" in payload:
        is_valid, error = _validate_enum_field(
            "npu-offload",
            payload["npu-offload"],
            VALID_BODY_NPU_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-cert-chain" in payload:
        is_valid, error = _validate_enum_field(
            "send-cert-chain",
            payload["send-cert-chain"],
            VALID_BODY_SEND_CERT_CHAIN,
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
    if "suite-b" in payload:
        is_valid, error = _validate_enum_field(
            "suite-b",
            payload["suite-b"],
            VALID_BODY_SUITE_B,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap" in payload:
        is_valid, error = _validate_enum_field(
            "eap",
            payload["eap"],
            VALID_BODY_EAP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-identity" in payload:
        is_valid, error = _validate_enum_field(
            "eap-identity",
            payload["eap-identity"],
            VALID_BODY_EAP_IDENTITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-cert-auth" in payload:
        is_valid, error = _validate_enum_field(
            "eap-cert-auth",
            payload["eap-cert-auth"],
            VALID_BODY_EAP_CERT_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "acct-verify" in payload:
        is_valid, error = _validate_enum_field(
            "acct-verify",
            payload["acct-verify"],
            VALID_BODY_ACCT_VERIFY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ppk" in payload:
        is_valid, error = _validate_enum_field(
            "ppk",
            payload["ppk"],
            VALID_BODY_PPK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wizard-type" in payload:
        is_valid, error = _validate_enum_field(
            "wizard-type",
            payload["wizard-type"],
            VALID_BODY_WIZARD_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "xauthtype" in payload:
        is_valid, error = _validate_enum_field(
            "xauthtype",
            payload["xauthtype"],
            VALID_BODY_XAUTHTYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reauth" in payload:
        is_valid, error = _validate_enum_field(
            "reauth",
            payload["reauth"],
            VALID_BODY_REAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "group-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "group-authentication",
            payload["group-authentication"],
            VALID_BODY_GROUP_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mesh-selector-type" in payload:
        is_valid, error = _validate_enum_field(
            "mesh-selector-type",
            payload["mesh-selector-type"],
            VALID_BODY_MESH_SELECTOR_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "idle-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "idle-timeout",
            payload["idle-timeout"],
            VALID_BODY_IDLE_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "shared-idle-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "shared-idle-timeout",
            payload["shared-idle-timeout"],
            VALID_BODY_SHARED_IDLE_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-sync-esp-seqno" in payload:
        is_valid, error = _validate_enum_field(
            "ha-sync-esp-seqno",
            payload["ha-sync-esp-seqno"],
            VALID_BODY_HA_SYNC_ESP_SEQNO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fgsp-sync" in payload:
        is_valid, error = _validate_enum_field(
            "fgsp-sync",
            payload["fgsp-sync"],
            VALID_BODY_FGSP_SYNC,
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
    if "nattraversal" in payload:
        is_valid, error = _validate_enum_field(
            "nattraversal",
            payload["nattraversal"],
            VALID_BODY_NATTRAVERSAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "esn" in payload:
        is_valid, error = _validate_enum_field(
            "esn",
            payload["esn"],
            VALID_BODY_ESN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "childless-ike" in payload:
        is_valid, error = _validate_enum_field(
            "childless-ike",
            payload["childless-ike"],
            VALID_BODY_CHILDLESS_IKE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "azure-ad-autoconnect" in payload:
        is_valid, error = _validate_enum_field(
            "azure-ad-autoconnect",
            payload["azure-ad-autoconnect"],
            VALID_BODY_AZURE_AD_AUTOCONNECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-resume" in payload:
        is_valid, error = _validate_enum_field(
            "client-resume",
            payload["client-resume"],
            VALID_BODY_CLIENT_RESUME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rekey" in payload:
        is_valid, error = _validate_enum_field(
            "rekey",
            payload["rekey"],
            VALID_BODY_REKEY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "digital-signature-auth" in payload:
        is_valid, error = _validate_enum_field(
            "digital-signature-auth",
            payload["digital-signature-auth"],
            VALID_BODY_DIGITAL_SIGNATURE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "signature-hash-alg" in payload:
        is_valid, error = _validate_enum_field(
            "signature-hash-alg",
            payload["signature-hash-alg"],
            VALID_BODY_SIGNATURE_HASH_ALG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsa-signature-format" in payload:
        is_valid, error = _validate_enum_field(
            "rsa-signature-format",
            payload["rsa-signature-format"],
            VALID_BODY_RSA_SIGNATURE_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rsa-signature-hash-override" in payload:
        is_valid, error = _validate_enum_field(
            "rsa-signature-hash-override",
            payload["rsa-signature-hash-override"],
            VALID_BODY_RSA_SIGNATURE_HASH_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "enforce-unique-id" in payload:
        is_valid, error = _validate_enum_field(
            "enforce-unique-id",
            payload["enforce-unique-id"],
            VALID_BODY_ENFORCE_UNIQUE_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-id-validation" in payload:
        is_valid, error = _validate_enum_field(
            "cert-id-validation",
            payload["cert-id-validation"],
            VALID_BODY_CERT_ID_VALIDATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec-egress" in payload:
        is_valid, error = _validate_enum_field(
            "fec-egress",
            payload["fec-egress"],
            VALID_BODY_FEC_EGRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec-codec" in payload:
        is_valid, error = _validate_enum_field(
            "fec-codec",
            payload["fec-codec"],
            VALID_BODY_FEC_CODEC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec-ingress" in payload:
        is_valid, error = _validate_enum_field(
            "fec-ingress",
            payload["fec-ingress"],
            VALID_BODY_FEC_INGRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "network-overlay" in payload:
        is_valid, error = _validate_enum_field(
            "network-overlay",
            payload["network-overlay"],
            VALID_BODY_NETWORK_OVERLAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dev-id-notification" in payload:
        is_valid, error = _validate_enum_field(
            "dev-id-notification",
            payload["dev-id-notification"],
            VALID_BODY_DEV_ID_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "loopback-asymroute" in payload:
        is_valid, error = _validate_enum_field(
            "loopback-asymroute",
            payload["loopback-asymroute"],
            VALID_BODY_LOOPBACK_ASYMROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "exchange-fgt-device-id" in payload:
        is_valid, error = _validate_enum_field(
            "exchange-fgt-device-id",
            payload["exchange-fgt-device-id"],
            VALID_BODY_EXCHANGE_FGT_DEVICE_ID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-auto-linklocal" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-auto-linklocal",
            payload["ipv6-auto-linklocal"],
            VALID_BODY_IPV6_AUTO_LINKLOCAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ems-sn-check" in payload:
        is_valid, error = _validate_enum_field(
            "ems-sn-check",
            payload["ems-sn-check"],
            VALID_BODY_EMS_SN_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-trust-store" in payload:
        is_valid, error = _validate_enum_field(
            "cert-trust-store",
            payload["cert-trust-store"],
            VALID_BODY_CERT_TRUST_STORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "qkd" in payload:
        is_valid, error = _validate_enum_field(
            "qkd",
            payload["qkd"],
            VALID_BODY_QKD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "qkd-hybrid" in payload:
        is_valid, error = _validate_enum_field(
            "qkd-hybrid",
            payload["qkd-hybrid"],
            VALID_BODY_QKD_HYBRID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "transport" in payload:
        is_valid, error = _validate_enum_field(
            "transport",
            payload["transport"],
            VALID_BODY_TRANSPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortinet-esp" in payload:
        is_valid, error = _validate_enum_field(
            "fortinet-esp",
            payload["fortinet-esp"],
            VALID_BODY_FORTINET_ESP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "remote-gw-match" in payload:
        is_valid, error = _validate_enum_field(
            "remote-gw-match",
            payload["remote-gw-match"],
            VALID_BODY_REMOTE_GW_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "remote-gw6-match" in payload:
        is_valid, error = _validate_enum_field(
            "remote-gw6-match",
            payload["remote-gw6-match"],
            VALID_BODY_REMOTE_GW6_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-peer-username-validation" in payload:
        is_valid, error = _validate_enum_field(
            "cert-peer-username-validation",
            payload["cert-peer-username-validation"],
            VALID_BODY_CERT_PEER_USERNAME_VALIDATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cert-peer-username-strip" in payload:
        is_valid, error = _validate_enum_field(
            "cert-peer-username-strip",
            payload["cert-peer-username-strip"],
            VALID_BODY_CERT_PEER_USERNAME_STRIP,
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
    "endpoint": "vpn/ipsec/phase1",
    "category": "cmdb",
    "api_path": "vpn.ipsec/phase1",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure VPN remote gateway.",
    "total_fields": 162,
    "required_fields_count": 15,
    "fields_with_defaults_count": 148,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
