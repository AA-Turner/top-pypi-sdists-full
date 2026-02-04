"""Validation helpers for wireless_controller/vap - Auto-generated"""

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
    "name",  # Virtual AP name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "pre-auth": "enable",
    "external-pre-auth": "disable",
    "mesh-backhaul": "disable",
    "atf-weight": 20,
    "max-clients": 0,
    "max-clients-ap": 0,
    "ssid": "fortinet",
    "broadcast-ssid": "enable",
    "security": "wpa2-only-personal",
    "pmf": "disable",
    "pmf-assoc-comeback-timeout": 1,
    "pmf-sa-query-retry-timeout": 2,
    "beacon-protection": "disable",
    "okc": "enable",
    "mbo": "disable",
    "gas-comeback-delay": 500,
    "gas-fragmentation-limit": 1024,
    "mbo-cell-data-conn-pref": "prefer-not",
    "80211k": "enable",
    "80211v": "enable",
    "neighbor-report-dual-band": "disable",
    "fast-bss-transition": "disable",
    "ft-mobility-domain": 1000,
    "ft-r0-key-lifetime": 480,
    "ft-over-ds": "disable",
    "sae-groups": "",
    "owe-groups": "",
    "owe-transition": "disable",
    "owe-transition-ssid": "",
    "additional-akms": "",
    "eapol-key-retries": "enable",
    "tkip-counter-measure": "enable",
    "external-web-format": "auto-detect",
    "external-logout": "",
    "mac-username-delimiter": "hyphen",
    "mac-password-delimiter": "hyphen",
    "mac-calling-station-delimiter": "hyphen",
    "mac-called-station-delimiter": "hyphen",
    "mac-case": "uppercase",
    "called-station-id-type": "mac",
    "mac-auth-bypass": "disable",
    "radius-mac-auth": "disable",
    "radius-mac-auth-server": "",
    "radius-mac-auth-block-interval": 0,
    "radius-mac-mpsk-auth": "disable",
    "radius-mac-mpsk-timeout": 86400,
    "auth": "",
    "encrypt": "AES",
    "keyindex": 1,
    "sae-h2e-only": "disable",
    "sae-hnp-only": "disable",
    "sae-pk": "disable",
    "sae-private-key": "",
    "akm24-only": "disable",
    "radius-server": "",
    "nas-filter-rule": "disable",
    "domain-name-stripping": "disable",
    "mlo": "disable",
    "local-standalone": "disable",
    "local-standalone-nat": "disable",
    "ip": "0.0.0.0 0.0.0.0",
    "dhcp-lease-time": 2400,
    "local-standalone-dns": "disable",
    "local-standalone-dns-ip": "",
    "local-lan-partition": "disable",
    "local-bridging": "disable",
    "local-lan": "allow",
    "local-authentication": "disable",
    "captive-portal": "disable",
    "captive-network-assistant-bypass": "disable",
    "portal-message-override-group": "",
    "portal-type": "auth",
    "security-exempt-list": "",
    "auth-cert": "",
    "auth-portal-addr": "",
    "intra-vap-privacy": "disable",
    "ldpc": "rxtx",
    "high-efficiency": "enable",
    "target-wake-time": "enable",
    "port-macauth": "disable",
    "port-macauth-timeout": 600,
    "port-macauth-reauth-timeout": 7200,
    "bss-color-partial": "enable",
    "mpsk-profile": "",
    "split-tunneling": "disable",
    "nac": "disable",
    "nac-profile": "",
    "vlanid": 0,
    "vlan-auto": "disable",
    "dynamic-vlan": "disable",
    "captive-portal-fw-accounting": "disable",
    "captive-portal-ac-name": "",
    "captive-portal-auth-timeout": 0,
    "multicast-rate": "0",
    "multicast-enhance": "disable",
    "igmp-snooping": "disable",
    "dhcp-address-enforcement": "disable",
    "broadcast-suppression": "dhcp-up dhcp-ucast arp-known",
    "ipv6-rules": "drop-icmp6ra drop-icmp6rs drop-llmnr6 drop-icmp6mld2 drop-dhcp6s drop-dhcp6c ndp-proxy drop-ns-dad",
    "me-disable-thresh": 32,
    "mu-mimo": "enable",
    "probe-resp-suppression": "disable",
    "probe-resp-threshold": "-80",
    "radio-sensitivity": "disable",
    "quarantine": "disable",
    "radio-5g-threshold": "-76",
    "radio-2g-threshold": "-79",
    "vlan-pooling": "disable",
    "dhcp-option43-insertion": "enable",
    "dhcp-option82-insertion": "disable",
    "dhcp-option82-circuit-id-insertion": "disable",
    "dhcp-option82-remote-id-insertion": "disable",
    "ptk-rekey": "disable",
    "ptk-rekey-intv": 86400,
    "gtk-rekey": "disable",
    "gtk-rekey-intv": 86400,
    "eap-reauth": "disable",
    "eap-reauth-intv": 86400,
    "roaming-acct-interim-update": "disable",
    "qos-profile": "",
    "hotspot20-profile": "",
    "access-control-list": "",
    "primary-wag-profile": "",
    "secondary-wag-profile": "",
    "tunnel-echo-interval": 300,
    "tunnel-fallback-interval": 7200,
    "rates-11a": "",
    "rates-11bg": "",
    "rates-11n-ss12": "",
    "rates-11n-ss34": "",
    "rates-11ac-mcs-map": "",
    "rates-11ax-mcs-map": "",
    "rates-11be-mcs-map": "",
    "rates-11be-mcs-map-160": "",
    "rates-11be-mcs-map-320": "",
    "utm-profile": "",
    "utm-status": "disable",
    "utm-log": "enable",
    "ips-sensor": "",
    "application-list": "",
    "antivirus-profile": "",
    "webfilter-profile": "",
    "scan-botnet-connections": "monitor",
    "address-group": "",
    "address-group-policy": "disable",
    "sticky-client-remove": "disable",
    "sticky-client-threshold-5g": "-76",
    "sticky-client-threshold-2g": "-79",
    "sticky-client-threshold-6g": "-76",
    "bstm-rssi-disassoc-timer": 200,
    "bstm-load-balancing-disassoc-timer": 10,
    "bstm-disassociation-imminent": "enable",
    "beacon-advertising": "",
    "osen": "disable",
    "application-detection-engine": "disable",
    "application-dscp-marking": "disable",
    "application-report-intv": 120,
    "l3-roaming": "disable",
    "l3-roaming-mode": "direct",
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
    "name": "string",  # Virtual AP name.
    "pre-auth": "option",  # Enable/disable pre-authentication, where supported by clients (default = enable)
    "external-pre-auth": "option",  # Enable/disable pre-authentication with external APs not managed by the FortiGate
    "mesh-backhaul": "option",  # Enable/disable using this VAP as a WiFi mesh backhaul (default = disable). This 
    "atf-weight": "integer",  # Airtime weight in percentage (default = 20).
    "max-clients": "integer",  # Maximum number of clients that can connect simultaneously to the VAP (default = 
    "max-clients-ap": "integer",  # Maximum number of clients that can connect simultaneously to the VAP per AP radi
    "ssid": "string",  # IEEE 802.11 service set identifier (SSID) for the wireless interface. Users who 
    "broadcast-ssid": "option",  # Enable/disable broadcasting the SSID (default = enable).
    "security": "option",  # Security mode for the wireless interface (default = wpa2-only-personal).
    "pmf": "option",  # Protected Management Frames (PMF) support (default = disable).
    "pmf-assoc-comeback-timeout": "integer",  # Protected Management Frames (PMF) comeback maximum timeout (1-20 sec).
    "pmf-sa-query-retry-timeout": "integer",  # Protected Management Frames (PMF) SA query retry timeout interval (1 - 5 100s of
    "beacon-protection": "option",  # Enable/disable beacon protection support (default = disable).
    "okc": "option",  # Enable/disable Opportunistic Key Caching (OKC) (default = enable).
    "mbo": "option",  # Enable/disable Multiband Operation (default = disable).
    "gas-comeback-delay": "integer",  # GAS comeback delay (0 or 100 - 10000 milliseconds, default = 500).
    "gas-fragmentation-limit": "integer",  # GAS fragmentation limit (512 - 4096, default = 1024).
    "mbo-cell-data-conn-pref": "option",  # MBO cell data connection preference (0, 1, or 255, default = 1).
    "80211k": "option",  # Enable/disable 802.11k assisted roaming (default = enable).
    "80211v": "option",  # Enable/disable 802.11v assisted roaming (default = enable).
    "neighbor-report-dual-band": "option",  # Enable/disable dual-band neighbor report (default = disable).
    "fast-bss-transition": "option",  # Enable/disable 802.11r Fast BSS Transition (FT) (default = disable).
    "ft-mobility-domain": "integer",  # Mobility domain identifier in FT (1 - 65535, default = 1000).
    "ft-r0-key-lifetime": "integer",  # Lifetime of the PMK-R0 key in FT, 1-65535 minutes.
    "ft-over-ds": "option",  # Enable/disable FT over the Distribution System (DS).
    "sae-groups": "option",  # SAE-Groups.
    "owe-groups": "option",  # OWE-Groups.
    "owe-transition": "option",  # Enable/disable OWE transition mode support.
    "owe-transition-ssid": "string",  # OWE transition mode peer SSID.
    "additional-akms": "option",  # Additional AKMs.
    "eapol-key-retries": "option",  # Enable/disable retransmission of EAPOL-Key frames (message 3/4 and group message
    "tkip-counter-measure": "option",  # Enable/disable TKIP counter measure.
    "external-web": "var-string",  # URL of external authentication web server.
    "external-web-format": "option",  # URL query parameter detection (default = auto-detect).
    "external-logout": "string",  # URL of external authentication logout server.
    "mac-username-delimiter": "option",  # MAC authentication username delimiter (default = hyphen).
    "mac-password-delimiter": "option",  # MAC authentication password delimiter (default = hyphen).
    "mac-calling-station-delimiter": "option",  # MAC calling station delimiter (default = hyphen).
    "mac-called-station-delimiter": "option",  # MAC called station delimiter (default = hyphen).
    "mac-case": "option",  # MAC case (default = uppercase).
    "called-station-id-type": "option",  # The format type of RADIUS attribute Called-Station-Id (default = mac).
    "mac-auth-bypass": "option",  # Enable/disable MAC authentication bypass.
    "radius-mac-auth": "option",  # Enable/disable RADIUS-based MAC authentication of clients (default = disable).
    "radius-mac-auth-server": "string",  # RADIUS-based MAC authentication server.
    "radius-mac-auth-block-interval": "integer",  # Don't send RADIUS MAC auth request again if the client has been rejected within 
    "radius-mac-mpsk-auth": "option",  # Enable/disable RADIUS-based MAC authentication of clients for MPSK authenticatio
    "radius-mac-mpsk-timeout": "integer",  # RADIUS MAC MPSK cache timeout interval (0 or 300 - 864000, default = 86400, 0 to
    "radius-mac-auth-usergroups": "string",  # Selective user groups that are permitted for RADIUS mac authentication.
    "auth": "option",  # Authentication protocol.
    "encrypt": "option",  # Encryption protocol to use (only available when security is set to a WPA type).
    "keyindex": "integer",  # WEP key index (1 - 4).
    "key": "password",  # WEP Key.
    "passphrase": "password",  # WPA pre-shared key (PSK) to be used to authenticate WiFi users.
    "sae-password": "password",  # WPA3 SAE password to be used to authenticate WiFi users.
    "sae-h2e-only": "option",  # Use hash-to-element-only mechanism for PWE derivation (default = disable).
    "sae-hnp-only": "option",  # Use hunting-and-pecking-only mechanism for PWE derivation (default = disable).
    "sae-pk": "option",  # Enable/disable WPA3 SAE-PK (default = disable).
    "sae-private-key": "string",  # Private key used for WPA3 SAE-PK authentication.
    "akm24-only": "option",  # WPA3 SAE using group-dependent hash only (default = disable).
    "radius-server": "string",  # RADIUS server to be used to authenticate WiFi users.
    "nas-filter-rule": "option",  # Enable/disable NAS filter rule support (default = disable).
    "domain-name-stripping": "option",  # Enable/disable stripping domain name from identity (default = disable).
    "mlo": "option",  # Enable/disable WiFi7 Multi-Link-Operation (default = disable).
    "local-standalone": "option",  # Enable/disable AP local standalone (default = disable).
    "local-standalone-nat": "option",  # Enable/disable AP local standalone NAT mode.
    "ip": "ipv4-classnet-host",  # IP address and subnet mask for the local standalone NAT subnet.
    "dhcp-lease-time": "integer",  # DHCP lease time in seconds for NAT IP address.
    "local-standalone-dns": "option",  # Enable/disable AP local standalone DNS.
    "local-standalone-dns-ip": "ipv4-address",  # IPv4 addresses for the local standalone DNS.
    "local-lan-partition": "option",  # Enable/disable segregating client traffic to local LAN side (default = disable).
    "local-bridging": "option",  # Enable/disable bridging of wireless and Ethernet interfaces on the FortiAP (defa
    "local-lan": "option",  # Allow/deny traffic destined for a Class A, B, or C private IP address (default =
    "local-authentication": "option",  # Enable/disable AP local authentication.
    "usergroup": "string",  # Firewall user group to be used to authenticate WiFi users.
    "captive-portal": "option",  # Enable/disable captive portal.
    "captive-network-assistant-bypass": "option",  # Enable/disable Captive Network Assistant bypass.
    "portal-message-override-group": "string",  # Replacement message group for this VAP (only available when security is set to a
    "portal-message-overrides": "string",  # Individual message overrides.
    "portal-type": "option",  # Captive portal functionality. Configure how the captive portal authenticates use
    "selected-usergroups": "string",  # Selective user groups that are permitted to authenticate.
    "security-exempt-list": "string",  # Optional security exempt list for captive portal authentication.
    "security-redirect-url": "var-string",  # Optional URL for redirecting users after they pass captive portal authentication
    "auth-cert": "string",  # HTTPS server certificate.
    "auth-portal-addr": "string",  # Address of captive portal.
    "intra-vap-privacy": "option",  # Enable/disable blocking communication between clients on the same SSID (called i
    "schedule": "string",  # Firewall schedules for enabling this VAP on the FortiAP. This VAP will be enable
    "ldpc": "option",  # VAP low-density parity-check (LDPC) coding configuration.
    "high-efficiency": "option",  # Enable/disable 802.11ax high efficiency (default = enable).
    "target-wake-time": "option",  # Enable/disable 802.11ax target wake time (default = enable).
    "port-macauth": "option",  # Enable/disable LAN port MAC authentication (default = disable).
    "port-macauth-timeout": "integer",  # LAN port MAC authentication idle timeout value (default = 600 sec).
    "port-macauth-reauth-timeout": "integer",  # LAN port MAC authentication re-authentication timeout value (default = 7200 sec)
    "bss-color-partial": "option",  # Enable/disable 802.11ax partial BSS color (default = enable).
    "mpsk-profile": "string",  # MPSK profile name.
    "split-tunneling": "option",  # Enable/disable split tunneling (default = disable).
    "nac": "option",  # Enable/disable network access control.
    "nac-profile": "string",  # NAC profile name.
    "vlanid": "integer",  # Optional VLAN ID.
    "vlan-auto": "option",  # Enable/disable automatic management of SSID VLAN interface.
    "dynamic-vlan": "option",  # Enable/disable dynamic VLAN assignment.
    "captive-portal-fw-accounting": "option",  # Enable/disable RADIUS accounting for captive portal firewall authentication sess
    "captive-portal-ac-name": "string",  # Local-bridging captive portal ac-name.
    "captive-portal-auth-timeout": "integer",  # Hard timeout - AP will always clear the session after timeout regardless of traf
    "multicast-rate": "option",  # Multicast rate (0, 6000, 12000, or 24000 kbps, default = 0).
    "multicast-enhance": "option",  # Enable/disable converting multicast to unicast to improve performance (default =
    "igmp-snooping": "option",  # Enable/disable IGMP snooping.
    "dhcp-address-enforcement": "option",  # Enable/disable DHCP address enforcement (default = disable).
    "broadcast-suppression": "option",  # Optional suppression of broadcast messages. For example, you can keep DHCP messa
    "ipv6-rules": "option",  # Optional rules of IPv6 packets. For example, you can keep RA, RS and so on off o
    "me-disable-thresh": "integer",  # Disable multicast enhancement when this many clients are receiving multicast tra
    "mu-mimo": "option",  # Enable/disable Multi-user MIMO (default = enable).
    "probe-resp-suppression": "option",  # Enable/disable probe response suppression (to ignore weak signals) (default = di
    "probe-resp-threshold": "string",  # Minimum signal level/threshold in dBm required for the AP response to probe requ
    "radio-sensitivity": "option",  # Enable/disable software radio sensitivity (to ignore weak signals) (default = di
    "quarantine": "option",  # Enable/disable station quarantine (default = disable).
    "radio-5g-threshold": "string",  # Minimum signal level/threshold in dBm required for the AP response to receive a 
    "radio-2g-threshold": "string",  # Minimum signal level/threshold in dBm required for the AP response to receive a 
    "vlan-name": "string",  # Table for mapping VLAN name to VLAN ID.
    "vlan-pooling": "option",  # Enable/disable VLAN pooling, to allow grouping of multiple wireless controller V
    "vlan-pool": "string",  # VLAN pool.
    "dhcp-option43-insertion": "option",  # Enable/disable insertion of DHCP option 43 (default = enable).
    "dhcp-option82-insertion": "option",  # Enable/disable DHCP option 82 insert (default = disable).
    "dhcp-option82-circuit-id-insertion": "option",  # Enable/disable DHCP option 82 circuit-id insert (default = disable).
    "dhcp-option82-remote-id-insertion": "option",  # Enable/disable DHCP option 82 remote-id insert (default = disable).
    "ptk-rekey": "option",  # Enable/disable PTK rekey for WPA-Enterprise security.
    "ptk-rekey-intv": "integer",  # PTK rekey interval (600 - 864000 sec, default = 86400).
    "gtk-rekey": "option",  # Enable/disable GTK rekey for WPA security.
    "gtk-rekey-intv": "integer",  # GTK rekey interval (600 - 864000 sec, default = 86400).
    "eap-reauth": "option",  # Enable/disable EAP re-authentication for WPA-Enterprise security.
    "eap-reauth-intv": "integer",  # EAP re-authentication interval (1800 - 864000 sec, default = 86400).
    "roaming-acct-interim-update": "option",  # Enable/disable using accounting interim update instead of accounting start/stop 
    "qos-profile": "string",  # Quality of service profile name.
    "hotspot20-profile": "string",  # Hotspot 2.0 profile name.
    "access-control-list": "string",  # Profile name for access-control-list.
    "primary-wag-profile": "string",  # Primary wireless access gateway profile name.
    "secondary-wag-profile": "string",  # Secondary wireless access gateway profile name.
    "tunnel-echo-interval": "integer",  # The time interval to send echo to both primary and secondary tunnel peers (1 - 6
    "tunnel-fallback-interval": "integer",  # The time interval for secondary tunnel to fall back to primary tunnel (0 - 65535
    "rates-11a": "option",  # Allowed data rates for 802.11a.
    "rates-11bg": "option",  # Allowed data rates for 802.11b/g.
    "rates-11n-ss12": "option",  # Allowed data rates for 802.11n with 1 or 2 spatial streams.
    "rates-11n-ss34": "option",  # Allowed data rates for 802.11n with 3 or 4 spatial streams.
    "rates-11ac-mcs-map": "string",  # Comma separated list of max supported VHT MCS for spatial streams 1 through 8.
    "rates-11ax-mcs-map": "string",  # Comma separated list of max supported HE MCS for spatial streams 1 through 8.
    "rates-11be-mcs-map": "string",  # Comma separated list of max nss that supports EHT-MCS 0-9, 10-11, 12-13 for 20MH
    "rates-11be-mcs-map-160": "string",  # Comma separated list of max nss that supports EHT-MCS 0-9, 10-11, 12-13 for 160M
    "rates-11be-mcs-map-320": "string",  # Comma separated list of max nss that supports EHT-MCS 0-9, 10-11, 12-13 for 320M
    "utm-profile": "string",  # UTM profile name.
    "utm-status": "option",  # Enable to add one or more security profiles (AV, IPS, etc.) to the VAP.
    "utm-log": "option",  # Enable/disable UTM logging.
    "ips-sensor": "string",  # IPS sensor name.
    "application-list": "string",  # Application control list name.
    "antivirus-profile": "string",  # AntiVirus profile name.
    "webfilter-profile": "string",  # WebFilter profile name.
    "scan-botnet-connections": "option",  # Block or monitor connections to Botnet servers or disable Botnet scanning.
    "address-group": "string",  # Firewall Address Group Name.
    "address-group-policy": "option",  # Configure MAC address filtering policy for MAC addresses that are in the address
    "sticky-client-remove": "option",  # Enable/disable sticky client remove to maintain good signal level clients in SSI
    "sticky-client-threshold-5g": "string",  # Minimum signal level/threshold in dBm required for the 5G client to be serviced 
    "sticky-client-threshold-2g": "string",  # Minimum signal level/threshold in dBm required for the 2G client to be serviced 
    "sticky-client-threshold-6g": "string",  # Minimum signal level/threshold in dBm required for the 6G client to be serviced 
    "bstm-rssi-disassoc-timer": "integer",  # Time interval for client to voluntarily leave AP before forcing a disassociation
    "bstm-load-balancing-disassoc-timer": "integer",  # Time interval for client to voluntarily leave AP before forcing a disassociation
    "bstm-disassociation-imminent": "option",  # Enable/disable forcing of disassociation after the BSTM request timer has been r
    "beacon-advertising": "option",  # Fortinet beacon advertising IE data   (default = empty).
    "osen": "option",  # Enable/disable OSEN as part of key management (default = disable).
    "application-detection-engine": "option",  # Enable/disable application detection engine (default = disable).
    "application-dscp-marking": "option",  # Enable/disable application attribute based DSCP marking (default = disable).
    "application-report-intv": "integer",  # Application report interval (30 - 864000 sec, default = 120).
    "l3-roaming": "option",  # Enable/disable layer 3 roaming (default = disable).
    "l3-roaming-mode": "option",  # Select the way that layer 3 roaming traffic is passed (default = direct).
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Virtual AP name.",
    "pre-auth": "Enable/disable pre-authentication, where supported by clients (default = enable).",
    "external-pre-auth": "Enable/disable pre-authentication with external APs not managed by the FortiGate (default = disable).",
    "mesh-backhaul": "Enable/disable using this VAP as a WiFi mesh backhaul (default = disable). This entry is only available when security is set to a WPA type or open.",
    "atf-weight": "Airtime weight in percentage (default = 20).",
    "max-clients": "Maximum number of clients that can connect simultaneously to the VAP (default = 0, meaning no limitation).",
    "max-clients-ap": "Maximum number of clients that can connect simultaneously to the VAP per AP radio (default = 0, meaning no limitation).",
    "ssid": "IEEE 802.11 service set identifier (SSID) for the wireless interface. Users who wish to use the wireless network must configure their computers to access this SSID name.",
    "broadcast-ssid": "Enable/disable broadcasting the SSID (default = enable).",
    "security": "Security mode for the wireless interface (default = wpa2-only-personal).",
    "pmf": "Protected Management Frames (PMF) support (default = disable).",
    "pmf-assoc-comeback-timeout": "Protected Management Frames (PMF) comeback maximum timeout (1-20 sec).",
    "pmf-sa-query-retry-timeout": "Protected Management Frames (PMF) SA query retry timeout interval (1 - 5 100s of msec).",
    "beacon-protection": "Enable/disable beacon protection support (default = disable).",
    "okc": "Enable/disable Opportunistic Key Caching (OKC) (default = enable).",
    "mbo": "Enable/disable Multiband Operation (default = disable).",
    "gas-comeback-delay": "GAS comeback delay (0 or 100 - 10000 milliseconds, default = 500).",
    "gas-fragmentation-limit": "GAS fragmentation limit (512 - 4096, default = 1024).",
    "mbo-cell-data-conn-pref": "MBO cell data connection preference (0, 1, or 255, default = 1).",
    "80211k": "Enable/disable 802.11k assisted roaming (default = enable).",
    "80211v": "Enable/disable 802.11v assisted roaming (default = enable).",
    "neighbor-report-dual-band": "Enable/disable dual-band neighbor report (default = disable).",
    "fast-bss-transition": "Enable/disable 802.11r Fast BSS Transition (FT) (default = disable).",
    "ft-mobility-domain": "Mobility domain identifier in FT (1 - 65535, default = 1000).",
    "ft-r0-key-lifetime": "Lifetime of the PMK-R0 key in FT, 1-65535 minutes.",
    "ft-over-ds": "Enable/disable FT over the Distribution System (DS).",
    "sae-groups": "SAE-Groups.",
    "owe-groups": "OWE-Groups.",
    "owe-transition": "Enable/disable OWE transition mode support.",
    "owe-transition-ssid": "OWE transition mode peer SSID.",
    "additional-akms": "Additional AKMs.",
    "eapol-key-retries": "Enable/disable retransmission of EAPOL-Key frames (message 3/4 and group message 1/2) (default = enable).",
    "tkip-counter-measure": "Enable/disable TKIP counter measure.",
    "external-web": "URL of external authentication web server.",
    "external-web-format": "URL query parameter detection (default = auto-detect).",
    "external-logout": "URL of external authentication logout server.",
    "mac-username-delimiter": "MAC authentication username delimiter (default = hyphen).",
    "mac-password-delimiter": "MAC authentication password delimiter (default = hyphen).",
    "mac-calling-station-delimiter": "MAC calling station delimiter (default = hyphen).",
    "mac-called-station-delimiter": "MAC called station delimiter (default = hyphen).",
    "mac-case": "MAC case (default = uppercase).",
    "called-station-id-type": "The format type of RADIUS attribute Called-Station-Id (default = mac).",
    "mac-auth-bypass": "Enable/disable MAC authentication bypass.",
    "radius-mac-auth": "Enable/disable RADIUS-based MAC authentication of clients (default = disable).",
    "radius-mac-auth-server": "RADIUS-based MAC authentication server.",
    "radius-mac-auth-block-interval": "Don't send RADIUS MAC auth request again if the client has been rejected within specific interval (0 or 30 - 864000 seconds, default = 0, 0 to disable blocking).",
    "radius-mac-mpsk-auth": "Enable/disable RADIUS-based MAC authentication of clients for MPSK authentication (default = disable).",
    "radius-mac-mpsk-timeout": "RADIUS MAC MPSK cache timeout interval (0 or 300 - 864000, default = 86400, 0 to disable caching).",
    "radius-mac-auth-usergroups": "Selective user groups that are permitted for RADIUS mac authentication.",
    "auth": "Authentication protocol.",
    "encrypt": "Encryption protocol to use (only available when security is set to a WPA type).",
    "keyindex": "WEP key index (1 - 4).",
    "key": "WEP Key.",
    "passphrase": "WPA pre-shared key (PSK) to be used to authenticate WiFi users.",
    "sae-password": "WPA3 SAE password to be used to authenticate WiFi users.",
    "sae-h2e-only": "Use hash-to-element-only mechanism for PWE derivation (default = disable).",
    "sae-hnp-only": "Use hunting-and-pecking-only mechanism for PWE derivation (default = disable).",
    "sae-pk": "Enable/disable WPA3 SAE-PK (default = disable).",
    "sae-private-key": "Private key used for WPA3 SAE-PK authentication.",
    "akm24-only": "WPA3 SAE using group-dependent hash only (default = disable).",
    "radius-server": "RADIUS server to be used to authenticate WiFi users.",
    "nas-filter-rule": "Enable/disable NAS filter rule support (default = disable).",
    "domain-name-stripping": "Enable/disable stripping domain name from identity (default = disable).",
    "mlo": "Enable/disable WiFi7 Multi-Link-Operation (default = disable).",
    "local-standalone": "Enable/disable AP local standalone (default = disable).",
    "local-standalone-nat": "Enable/disable AP local standalone NAT mode.",
    "ip": "IP address and subnet mask for the local standalone NAT subnet.",
    "dhcp-lease-time": "DHCP lease time in seconds for NAT IP address.",
    "local-standalone-dns": "Enable/disable AP local standalone DNS.",
    "local-standalone-dns-ip": "IPv4 addresses for the local standalone DNS.",
    "local-lan-partition": "Enable/disable segregating client traffic to local LAN side (default = disable).",
    "local-bridging": "Enable/disable bridging of wireless and Ethernet interfaces on the FortiAP (default = disable).",
    "local-lan": "Allow/deny traffic destined for a Class A, B, or C private IP address (default = allow).",
    "local-authentication": "Enable/disable AP local authentication.",
    "usergroup": "Firewall user group to be used to authenticate WiFi users.",
    "captive-portal": "Enable/disable captive portal.",
    "captive-network-assistant-bypass": "Enable/disable Captive Network Assistant bypass.",
    "portal-message-override-group": "Replacement message group for this VAP (only available when security is set to a captive portal type).",
    "portal-message-overrides": "Individual message overrides.",
    "portal-type": "Captive portal functionality. Configure how the captive portal authenticates users and whether it includes a disclaimer.",
    "selected-usergroups": "Selective user groups that are permitted to authenticate.",
    "security-exempt-list": "Optional security exempt list for captive portal authentication.",
    "security-redirect-url": "Optional URL for redirecting users after they pass captive portal authentication.",
    "auth-cert": "HTTPS server certificate.",
    "auth-portal-addr": "Address of captive portal.",
    "intra-vap-privacy": "Enable/disable blocking communication between clients on the same SSID (called intra-SSID privacy) (default = disable).",
    "schedule": "Firewall schedules for enabling this VAP on the FortiAP. This VAP will be enabled when at least one of the schedules is valid. Separate multiple schedule names with a space.",
    "ldpc": "VAP low-density parity-check (LDPC) coding configuration.",
    "high-efficiency": "Enable/disable 802.11ax high efficiency (default = enable).",
    "target-wake-time": "Enable/disable 802.11ax target wake time (default = enable).",
    "port-macauth": "Enable/disable LAN port MAC authentication (default = disable).",
    "port-macauth-timeout": "LAN port MAC authentication idle timeout value (default = 600 sec).",
    "port-macauth-reauth-timeout": "LAN port MAC authentication re-authentication timeout value (default = 7200 sec).",
    "bss-color-partial": "Enable/disable 802.11ax partial BSS color (default = enable).",
    "mpsk-profile": "MPSK profile name.",
    "split-tunneling": "Enable/disable split tunneling (default = disable).",
    "nac": "Enable/disable network access control.",
    "nac-profile": "NAC profile name.",
    "vlanid": "Optional VLAN ID.",
    "vlan-auto": "Enable/disable automatic management of SSID VLAN interface.",
    "dynamic-vlan": "Enable/disable dynamic VLAN assignment.",
    "captive-portal-fw-accounting": "Enable/disable RADIUS accounting for captive portal firewall authentication session.",
    "captive-portal-ac-name": "Local-bridging captive portal ac-name.",
    "captive-portal-auth-timeout": "Hard timeout - AP will always clear the session after timeout regardless of traffic (0 - 864000 sec, default = 0).",
    "multicast-rate": "Multicast rate (0, 6000, 12000, or 24000 kbps, default = 0).",
    "multicast-enhance": "Enable/disable converting multicast to unicast to improve performance (default = disable).",
    "igmp-snooping": "Enable/disable IGMP snooping.",
    "dhcp-address-enforcement": "Enable/disable DHCP address enforcement (default = disable).",
    "broadcast-suppression": "Optional suppression of broadcast messages. For example, you can keep DHCP messages, ARP broadcasts, and so on off of the wireless network.",
    "ipv6-rules": "Optional rules of IPv6 packets. For example, you can keep RA, RS and so on off of the wireless network.",
    "me-disable-thresh": "Disable multicast enhancement when this many clients are receiving multicast traffic.",
    "mu-mimo": "Enable/disable Multi-user MIMO (default = enable).",
    "probe-resp-suppression": "Enable/disable probe response suppression (to ignore weak signals) (default = disable).",
    "probe-resp-threshold": "Minimum signal level/threshold in dBm required for the AP response to probe requests (-95 to -20, default = -80).",
    "radio-sensitivity": "Enable/disable software radio sensitivity (to ignore weak signals) (default = disable).",
    "quarantine": "Enable/disable station quarantine (default = disable).",
    "radio-5g-threshold": "Minimum signal level/threshold in dBm required for the AP response to receive a packet in 5G band(-95 to -20, default = -76).",
    "radio-2g-threshold": "Minimum signal level/threshold in dBm required for the AP response to receive a packet in 2.4G band (-95 to -20, default = -79).",
    "vlan-name": "Table for mapping VLAN name to VLAN ID.",
    "vlan-pooling": "Enable/disable VLAN pooling, to allow grouping of multiple wireless controller VLANs into VLAN pools (default = disable). When set to wtp-group, VLAN pooling occurs with VLAN assignment by wtp-group.",
    "vlan-pool": "VLAN pool.",
    "dhcp-option43-insertion": "Enable/disable insertion of DHCP option 43 (default = enable).",
    "dhcp-option82-insertion": "Enable/disable DHCP option 82 insert (default = disable).",
    "dhcp-option82-circuit-id-insertion": "Enable/disable DHCP option 82 circuit-id insert (default = disable).",
    "dhcp-option82-remote-id-insertion": "Enable/disable DHCP option 82 remote-id insert (default = disable).",
    "ptk-rekey": "Enable/disable PTK rekey for WPA-Enterprise security.",
    "ptk-rekey-intv": "PTK rekey interval (600 - 864000 sec, default = 86400).",
    "gtk-rekey": "Enable/disable GTK rekey for WPA security.",
    "gtk-rekey-intv": "GTK rekey interval (600 - 864000 sec, default = 86400).",
    "eap-reauth": "Enable/disable EAP re-authentication for WPA-Enterprise security.",
    "eap-reauth-intv": "EAP re-authentication interval (1800 - 864000 sec, default = 86400).",
    "roaming-acct-interim-update": "Enable/disable using accounting interim update instead of accounting start/stop on roaming for WPA-Enterprise security.",
    "qos-profile": "Quality of service profile name.",
    "hotspot20-profile": "Hotspot 2.0 profile name.",
    "access-control-list": "Profile name for access-control-list.",
    "primary-wag-profile": "Primary wireless access gateway profile name.",
    "secondary-wag-profile": "Secondary wireless access gateway profile name.",
    "tunnel-echo-interval": "The time interval to send echo to both primary and secondary tunnel peers (1 - 65535 sec, default = 300).",
    "tunnel-fallback-interval": "The time interval for secondary tunnel to fall back to primary tunnel (0 - 65535 sec, default = 7200).",
    "rates-11a": "Allowed data rates for 802.11a.",
    "rates-11bg": "Allowed data rates for 802.11b/g.",
    "rates-11n-ss12": "Allowed data rates for 802.11n with 1 or 2 spatial streams.",
    "rates-11n-ss34": "Allowed data rates for 802.11n with 3 or 4 spatial streams.",
    "rates-11ac-mcs-map": "Comma separated list of max supported VHT MCS for spatial streams 1 through 8.",
    "rates-11ax-mcs-map": "Comma separated list of max supported HE MCS for spatial streams 1 through 8.",
    "rates-11be-mcs-map": "Comma separated list of max nss that supports EHT-MCS 0-9, 10-11, 12-13 for 20MHz/40MHz/80MHz bandwidth.",
    "rates-11be-mcs-map-160": "Comma separated list of max nss that supports EHT-MCS 0-9, 10-11, 12-13 for 160MHz bandwidth.",
    "rates-11be-mcs-map-320": "Comma separated list of max nss that supports EHT-MCS 0-9, 10-11, 12-13 for 320MHz bandwidth.",
    "utm-profile": "UTM profile name.",
    "utm-status": "Enable to add one or more security profiles (AV, IPS, etc.) to the VAP.",
    "utm-log": "Enable/disable UTM logging.",
    "ips-sensor": "IPS sensor name.",
    "application-list": "Application control list name.",
    "antivirus-profile": "AntiVirus profile name.",
    "webfilter-profile": "WebFilter profile name.",
    "scan-botnet-connections": "Block or monitor connections to Botnet servers or disable Botnet scanning.",
    "address-group": "Firewall Address Group Name.",
    "address-group-policy": "Configure MAC address filtering policy for MAC addresses that are in the address-group.",
    "sticky-client-remove": "Enable/disable sticky client remove to maintain good signal level clients in SSID (default = disable).",
    "sticky-client-threshold-5g": "Minimum signal level/threshold in dBm required for the 5G client to be serviced by the AP (-95 to -20, default = -76).",
    "sticky-client-threshold-2g": "Minimum signal level/threshold in dBm required for the 2G client to be serviced by the AP (-95 to -20, default = -79).",
    "sticky-client-threshold-6g": "Minimum signal level/threshold in dBm required for the 6G client to be serviced by the AP (-95 to -20, default = -76).",
    "bstm-rssi-disassoc-timer": "Time interval for client to voluntarily leave AP before forcing a disassociation due to low RSSI (0 to 2000, default = 200).",
    "bstm-load-balancing-disassoc-timer": "Time interval for client to voluntarily leave AP before forcing a disassociation due to AP load-balancing (0 to 30, default = 10).",
    "bstm-disassociation-imminent": "Enable/disable forcing of disassociation after the BSTM request timer has been reached (default = enable).",
    "beacon-advertising": "Fortinet beacon advertising IE data   (default = empty).",
    "osen": "Enable/disable OSEN as part of key management (default = disable).",
    "application-detection-engine": "Enable/disable application detection engine (default = disable).",
    "application-dscp-marking": "Enable/disable application attribute based DSCP marking (default = disable).",
    "application-report-intv": "Application report interval (30 - 864000 sec, default = 120).",
    "l3-roaming": "Enable/disable layer 3 roaming (default = disable).",
    "l3-roaming-mode": "Select the way that layer 3 roaming traffic is passed (default = direct).",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 15},
    "atf-weight": {"type": "integer", "min": 0, "max": 100},
    "max-clients": {"type": "integer", "min": 0, "max": 4294967295},
    "max-clients-ap": {"type": "integer", "min": 0, "max": 4294967295},
    "ssid": {"type": "string", "max_length": 32},
    "pmf-assoc-comeback-timeout": {"type": "integer", "min": 1, "max": 20},
    "pmf-sa-query-retry-timeout": {"type": "integer", "min": 1, "max": 5},
    "gas-comeback-delay": {"type": "integer", "min": 100, "max": 10000},
    "gas-fragmentation-limit": {"type": "integer", "min": 512, "max": 4096},
    "ft-mobility-domain": {"type": "integer", "min": 1, "max": 65535},
    "ft-r0-key-lifetime": {"type": "integer", "min": 1, "max": 65535},
    "owe-transition-ssid": {"type": "string", "max_length": 32},
    "external-logout": {"type": "string", "max_length": 127},
    "radius-mac-auth-server": {"type": "string", "max_length": 35},
    "radius-mac-auth-block-interval": {"type": "integer", "min": 30, "max": 864000},
    "radius-mac-mpsk-timeout": {"type": "integer", "min": 300, "max": 864000},
    "keyindex": {"type": "integer", "min": 1, "max": 4},
    "sae-private-key": {"type": "string", "max_length": 359},
    "radius-server": {"type": "string", "max_length": 35},
    "dhcp-lease-time": {"type": "integer", "min": 300, "max": 8640000},
    "portal-message-override-group": {"type": "string", "max_length": 35},
    "security-exempt-list": {"type": "string", "max_length": 35},
    "auth-cert": {"type": "string", "max_length": 35},
    "auth-portal-addr": {"type": "string", "max_length": 63},
    "port-macauth-timeout": {"type": "integer", "min": 60, "max": 65535},
    "port-macauth-reauth-timeout": {"type": "integer", "min": 120, "max": 65535},
    "mpsk-profile": {"type": "string", "max_length": 35},
    "nac-profile": {"type": "string", "max_length": 35},
    "vlanid": {"type": "integer", "min": 0, "max": 4094},
    "captive-portal-ac-name": {"type": "string", "max_length": 35},
    "captive-portal-auth-timeout": {"type": "integer", "min": 0, "max": 864000},
    "me-disable-thresh": {"type": "integer", "min": 2, "max": 256},
    "probe-resp-threshold": {"type": "string", "max_length": 7},
    "radio-5g-threshold": {"type": "string", "max_length": 7},
    "radio-2g-threshold": {"type": "string", "max_length": 7},
    "ptk-rekey-intv": {"type": "integer", "min": 600, "max": 864000},
    "gtk-rekey-intv": {"type": "integer", "min": 600, "max": 864000},
    "eap-reauth-intv": {"type": "integer", "min": 1800, "max": 864000},
    "qos-profile": {"type": "string", "max_length": 35},
    "hotspot20-profile": {"type": "string", "max_length": 35},
    "access-control-list": {"type": "string", "max_length": 35},
    "primary-wag-profile": {"type": "string", "max_length": 35},
    "secondary-wag-profile": {"type": "string", "max_length": 35},
    "tunnel-echo-interval": {"type": "integer", "min": 1, "max": 65535},
    "tunnel-fallback-interval": {"type": "integer", "min": 0, "max": 65535},
    "rates-11ac-mcs-map": {"type": "string", "max_length": 63},
    "rates-11ax-mcs-map": {"type": "string", "max_length": 63},
    "rates-11be-mcs-map": {"type": "string", "max_length": 15},
    "rates-11be-mcs-map-160": {"type": "string", "max_length": 15},
    "rates-11be-mcs-map-320": {"type": "string", "max_length": 15},
    "utm-profile": {"type": "string", "max_length": 35},
    "ips-sensor": {"type": "string", "max_length": 47},
    "application-list": {"type": "string", "max_length": 47},
    "antivirus-profile": {"type": "string", "max_length": 47},
    "webfilter-profile": {"type": "string", "max_length": 47},
    "address-group": {"type": "string", "max_length": 79},
    "sticky-client-threshold-5g": {"type": "string", "max_length": 7},
    "sticky-client-threshold-2g": {"type": "string", "max_length": 7},
    "sticky-client-threshold-6g": {"type": "string", "max_length": 7},
    "bstm-rssi-disassoc-timer": {"type": "integer", "min": 1, "max": 2000},
    "bstm-load-balancing-disassoc-timer": {"type": "integer", "min": 1, "max": 30},
    "application-report-intv": {"type": "integer", "min": 30, "max": 864000},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "radius-mac-auth-usergroups": {
        "name": {
            "type": "string",
            "help": "User group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "usergroup": {
        "name": {
            "type": "string",
            "help": "User group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "portal-message-overrides": {
        "auth-disclaimer-page": {
            "type": "string",
            "help": "Override auth-disclaimer-page message with message from portal-message-overrides group.",
            "default": "",
            "max_length": 35,
        },
        "auth-reject-page": {
            "type": "string",
            "help": "Override auth-reject-page message with message from portal-message-overrides group.",
            "default": "",
            "max_length": 35,
        },
        "auth-login-page": {
            "type": "string",
            "help": "Override auth-login-page message with message from portal-message-overrides group.",
            "default": "",
            "max_length": 35,
        },
        "auth-login-failed-page": {
            "type": "string",
            "help": "Override auth-login-failed-page message with message from portal-message-overrides group.",
            "default": "",
            "max_length": 35,
        },
    },
    "selected-usergroups": {
        "name": {
            "type": "string",
            "help": "User group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "schedule": {
        "name": {
            "type": "string",
            "help": "Schedule name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
    },
    "vlan-name": {
        "name": {
            "type": "string",
            "help": "VLAN name.",
            "required": True,
            "default": "",
            "max_length": 35,
        },
        "vlan-id": {
            "type": "integer",
            "help": "VLAN IDs (maximum 8 VLAN IDs).",
            "default": "",
            "min_value": 0,
            "max_value": 4094,
        },
    },
    "vlan-pool": {
        "id": {
            "type": "integer",
            "help": "ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4094,
        },
        "wtp-group": {
            "type": "string",
            "help": "WTP group name.",
            "default": "",
            "max_length": 35,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_PRE_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_EXTERNAL_PRE_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_MESH_BACKHAUL = [
    "enable",
    "disable",
]
VALID_BODY_BROADCAST_SSID = [
    "enable",
    "disable",
]
VALID_BODY_SECURITY = [
    "open",
    "wep64",
    "wep128",
    "wpa-personal",
    "wpa-enterprise",
    "wpa-only-personal",
    "wpa-only-enterprise",
    "wpa2-only-personal",
    "wpa2-only-enterprise",
    "wpa3-enterprise",
    "wpa3-only-enterprise",
    "wpa3-enterprise-transition",
    "wpa3-sae",
    "wpa3-sae-transition",
    "owe",
    "osen",
]
VALID_BODY_PMF = [
    "disable",
    "enable",
    "optional",
]
VALID_BODY_BEACON_PROTECTION = [
    "disable",
    "enable",
]
VALID_BODY_OKC = [
    "disable",
    "enable",
]
VALID_BODY_MBO = [
    "disable",
    "enable",
]
VALID_BODY_MBO_CELL_DATA_CONN_PREF = [
    "excluded",
    "prefer-not",
    "prefer-use",
]
VALID_BODY_80211K = [
    "disable",
    "enable",
]
VALID_BODY_80211V = [
    "disable",
    "enable",
]
VALID_BODY_NEIGHBOR_REPORT_DUAL_BAND = [
    "disable",
    "enable",
]
VALID_BODY_FAST_BSS_TRANSITION = [
    "disable",
    "enable",
]
VALID_BODY_FT_OVER_DS = [
    "disable",
    "enable",
]
VALID_BODY_SAE_GROUPS = [
    "19",
    "20",
    "21",
]
VALID_BODY_OWE_GROUPS = [
    "19",
    "20",
    "21",
]
VALID_BODY_OWE_TRANSITION = [
    "disable",
    "enable",
]
VALID_BODY_ADDITIONAL_AKMS = [
    "akm6",
    "akm24",
]
VALID_BODY_EAPOL_KEY_RETRIES = [
    "disable",
    "enable",
]
VALID_BODY_TKIP_COUNTER_MEASURE = [
    "enable",
    "disable",
]
VALID_BODY_EXTERNAL_WEB_FORMAT = [
    "auto-detect",
    "no-query-string",
    "partial-query-string",
]
VALID_BODY_MAC_USERNAME_DELIMITER = [
    "hyphen",
    "single-hyphen",
    "colon",
    "none",
]
VALID_BODY_MAC_PASSWORD_DELIMITER = [
    "hyphen",
    "single-hyphen",
    "colon",
    "none",
]
VALID_BODY_MAC_CALLING_STATION_DELIMITER = [
    "hyphen",
    "single-hyphen",
    "colon",
    "none",
]
VALID_BODY_MAC_CALLED_STATION_DELIMITER = [
    "hyphen",
    "single-hyphen",
    "colon",
    "none",
]
VALID_BODY_MAC_CASE = [
    "uppercase",
    "lowercase",
]
VALID_BODY_CALLED_STATION_ID_TYPE = [
    "mac",
    "ip",
    "apname",
]
VALID_BODY_MAC_AUTH_BYPASS = [
    "enable",
    "disable",
]
VALID_BODY_RADIUS_MAC_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_RADIUS_MAC_MPSK_AUTH = [
    "enable",
    "disable",
]
VALID_BODY_AUTH = [
    "radius",
    "usergroup",
]
VALID_BODY_ENCRYPT = [
    "TKIP",
    "AES",
    "TKIP-AES",
]
VALID_BODY_SAE_H2E_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_SAE_HNP_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_SAE_PK = [
    "enable",
    "disable",
]
VALID_BODY_AKM24_ONLY = [
    "disable",
    "enable",
]
VALID_BODY_NAS_FILTER_RULE = [
    "enable",
    "disable",
]
VALID_BODY_DOMAIN_NAME_STRIPPING = [
    "disable",
    "enable",
]
VALID_BODY_MLO = [
    "disable",
    "enable",
]
VALID_BODY_LOCAL_STANDALONE = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_STANDALONE_NAT = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_STANDALONE_DNS = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_LAN_PARTITION = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_BRIDGING = [
    "enable",
    "disable",
]
VALID_BODY_LOCAL_LAN = [
    "allow",
    "deny",
]
VALID_BODY_LOCAL_AUTHENTICATION = [
    "enable",
    "disable",
]
VALID_BODY_CAPTIVE_PORTAL = [
    "enable",
    "disable",
]
VALID_BODY_CAPTIVE_NETWORK_ASSISTANT_BYPASS = [
    "enable",
    "disable",
]
VALID_BODY_PORTAL_TYPE = [
    "auth",
    "auth+disclaimer",
    "disclaimer",
    "email-collect",
    "cmcc",
    "cmcc-macauth",
    "auth-mac",
    "external-auth",
    "external-macauth",
]
VALID_BODY_INTRA_VAP_PRIVACY = [
    "enable",
    "disable",
]
VALID_BODY_LDPC = [
    "disable",
    "rx",
    "tx",
    "rxtx",
]
VALID_BODY_HIGH_EFFICIENCY = [
    "enable",
    "disable",
]
VALID_BODY_TARGET_WAKE_TIME = [
    "enable",
    "disable",
]
VALID_BODY_PORT_MACAUTH = [
    "disable",
    "radius",
    "address-group",
]
VALID_BODY_BSS_COLOR_PARTIAL = [
    "enable",
    "disable",
]
VALID_BODY_SPLIT_TUNNELING = [
    "enable",
    "disable",
]
VALID_BODY_NAC = [
    "enable",
    "disable",
]
VALID_BODY_VLAN_AUTO = [
    "enable",
    "disable",
]
VALID_BODY_DYNAMIC_VLAN = [
    "enable",
    "disable",
]
VALID_BODY_CAPTIVE_PORTAL_FW_ACCOUNTING = [
    "enable",
    "disable",
]
VALID_BODY_MULTICAST_RATE = [
    "0",
    "6000",
    "12000",
    "24000",
]
VALID_BODY_MULTICAST_ENHANCE = [
    "enable",
    "disable",
]
VALID_BODY_IGMP_SNOOPING = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_ADDRESS_ENFORCEMENT = [
    "enable",
    "disable",
]
VALID_BODY_BROADCAST_SUPPRESSION = [
    "dhcp-up",
    "dhcp-down",
    "dhcp-starvation",
    "dhcp-ucast",
    "arp-known",
    "arp-unknown",
    "arp-reply",
    "arp-poison",
    "arp-proxy",
    "netbios-ns",
    "netbios-ds",
    "ipv6",
    "all-other-mc",
    "all-other-bc",
]
VALID_BODY_IPV6_RULES = [
    "drop-icmp6ra",
    "drop-icmp6rs",
    "drop-llmnr6",
    "drop-icmp6mld2",
    "drop-dhcp6s",
    "drop-dhcp6c",
    "ndp-proxy",
    "drop-ns-dad",
    "drop-ns-nondad",
]
VALID_BODY_MU_MIMO = [
    "enable",
    "disable",
]
VALID_BODY_PROBE_RESP_SUPPRESSION = [
    "enable",
    "disable",
]
VALID_BODY_RADIO_SENSITIVITY = [
    "enable",
    "disable",
]
VALID_BODY_QUARANTINE = [
    "enable",
    "disable",
]
VALID_BODY_VLAN_POOLING = [
    "wtp-group",
    "round-robin",
    "hash",
    "disable",
]
VALID_BODY_DHCP_OPTION43_INSERTION = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_OPTION82_INSERTION = [
    "enable",
    "disable",
]
VALID_BODY_DHCP_OPTION82_CIRCUIT_ID_INSERTION = [
    "style-1",
    "style-2",
    "style-3",
    "disable",
]
VALID_BODY_DHCP_OPTION82_REMOTE_ID_INSERTION = [
    "style-1",
    "disable",
]
VALID_BODY_PTK_REKEY = [
    "enable",
    "disable",
]
VALID_BODY_GTK_REKEY = [
    "enable",
    "disable",
]
VALID_BODY_EAP_REAUTH = [
    "enable",
    "disable",
]
VALID_BODY_ROAMING_ACCT_INTERIM_UPDATE = [
    "enable",
    "disable",
]
VALID_BODY_RATES_11A = [
    "6",
    "6-basic",
    "9",
    "9-basic",
    "12",
    "12-basic",
    "18",
    "18-basic",
    "24",
    "24-basic",
    "36",
    "36-basic",
    "48",
    "48-basic",
    "54",
    "54-basic",
]
VALID_BODY_RATES_11BG = [
    "1",
    "1-basic",
    "2",
    "2-basic",
    "5.5",
    "5.5-basic",
    "11",
    "11-basic",
    "6",
    "6-basic",
    "9",
    "9-basic",
    "12",
    "12-basic",
    "18",
    "18-basic",
    "24",
    "24-basic",
    "36",
    "36-basic",
    "48",
    "48-basic",
    "54",
    "54-basic",
]
VALID_BODY_RATES_11N_SS12 = [
    "mcs0/1",
    "mcs1/1",
    "mcs2/1",
    "mcs3/1",
    "mcs4/1",
    "mcs5/1",
    "mcs6/1",
    "mcs7/1",
    "mcs8/2",
    "mcs9/2",
    "mcs10/2",
    "mcs11/2",
    "mcs12/2",
    "mcs13/2",
    "mcs14/2",
    "mcs15/2",
]
VALID_BODY_RATES_11N_SS34 = [
    "mcs16/3",
    "mcs17/3",
    "mcs18/3",
    "mcs19/3",
    "mcs20/3",
    "mcs21/3",
    "mcs22/3",
    "mcs23/3",
    "mcs24/4",
    "mcs25/4",
    "mcs26/4",
    "mcs27/4",
    "mcs28/4",
    "mcs29/4",
    "mcs30/4",
    "mcs31/4",
]
VALID_BODY_UTM_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_UTM_LOG = [
    "enable",
    "disable",
]
VALID_BODY_SCAN_BOTNET_CONNECTIONS = [
    "disable",
    "monitor",
    "block",
]
VALID_BODY_ADDRESS_GROUP_POLICY = [
    "disable",
    "allow",
    "deny",
]
VALID_BODY_STICKY_CLIENT_REMOVE = [
    "enable",
    "disable",
]
VALID_BODY_BSTM_DISASSOCIATION_IMMINENT = [
    "enable",
    "disable",
]
VALID_BODY_BEACON_ADVERTISING = [
    "name",
    "model",
    "serial-number",
]
VALID_BODY_OSEN = [
    "enable",
    "disable",
]
VALID_BODY_APPLICATION_DETECTION_ENGINE = [
    "enable",
    "disable",
]
VALID_BODY_APPLICATION_DSCP_MARKING = [
    "enable",
    "disable",
]
VALID_BODY_L3_ROAMING = [
    "enable",
    "disable",
]
VALID_BODY_L3_ROAMING_MODE = [
    "direct",
    "indirect",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_wireless_controller_vap_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for wireless_controller/vap."""
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


def validate_wireless_controller_vap_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new wireless_controller/vap object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "pre-auth" in payload:
        is_valid, error = _validate_enum_field(
            "pre-auth",
            payload["pre-auth"],
            VALID_BODY_PRE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external-pre-auth" in payload:
        is_valid, error = _validate_enum_field(
            "external-pre-auth",
            payload["external-pre-auth"],
            VALID_BODY_EXTERNAL_PRE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mesh-backhaul" in payload:
        is_valid, error = _validate_enum_field(
            "mesh-backhaul",
            payload["mesh-backhaul"],
            VALID_BODY_MESH_BACKHAUL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-ssid",
            payload["broadcast-ssid"],
            VALID_BODY_BROADCAST_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security" in payload:
        is_valid, error = _validate_enum_field(
            "security",
            payload["security"],
            VALID_BODY_SECURITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pmf" in payload:
        is_valid, error = _validate_enum_field(
            "pmf",
            payload["pmf"],
            VALID_BODY_PMF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "beacon-protection" in payload:
        is_valid, error = _validate_enum_field(
            "beacon-protection",
            payload["beacon-protection"],
            VALID_BODY_BEACON_PROTECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "okc" in payload:
        is_valid, error = _validate_enum_field(
            "okc",
            payload["okc"],
            VALID_BODY_OKC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mbo" in payload:
        is_valid, error = _validate_enum_field(
            "mbo",
            payload["mbo"],
            VALID_BODY_MBO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mbo-cell-data-conn-pref" in payload:
        is_valid, error = _validate_enum_field(
            "mbo-cell-data-conn-pref",
            payload["mbo-cell-data-conn-pref"],
            VALID_BODY_MBO_CELL_DATA_CONN_PREF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "80211k" in payload:
        is_valid, error = _validate_enum_field(
            "80211k",
            payload["80211k"],
            VALID_BODY_80211K,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "80211v" in payload:
        is_valid, error = _validate_enum_field(
            "80211v",
            payload["80211v"],
            VALID_BODY_80211V,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "neighbor-report-dual-band" in payload:
        is_valid, error = _validate_enum_field(
            "neighbor-report-dual-band",
            payload["neighbor-report-dual-band"],
            VALID_BODY_NEIGHBOR_REPORT_DUAL_BAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fast-bss-transition" in payload:
        is_valid, error = _validate_enum_field(
            "fast-bss-transition",
            payload["fast-bss-transition"],
            VALID_BODY_FAST_BSS_TRANSITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ft-over-ds" in payload:
        is_valid, error = _validate_enum_field(
            "ft-over-ds",
            payload["ft-over-ds"],
            VALID_BODY_FT_OVER_DS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-groups" in payload:
        is_valid, error = _validate_enum_field(
            "sae-groups",
            payload["sae-groups"],
            VALID_BODY_SAE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "owe-groups" in payload:
        is_valid, error = _validate_enum_field(
            "owe-groups",
            payload["owe-groups"],
            VALID_BODY_OWE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "owe-transition" in payload:
        is_valid, error = _validate_enum_field(
            "owe-transition",
            payload["owe-transition"],
            VALID_BODY_OWE_TRANSITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "additional-akms" in payload:
        is_valid, error = _validate_enum_field(
            "additional-akms",
            payload["additional-akms"],
            VALID_BODY_ADDITIONAL_AKMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-key-retries" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-key-retries",
            payload["eapol-key-retries"],
            VALID_BODY_EAPOL_KEY_RETRIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tkip-counter-measure" in payload:
        is_valid, error = _validate_enum_field(
            "tkip-counter-measure",
            payload["tkip-counter-measure"],
            VALID_BODY_TKIP_COUNTER_MEASURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external-web-format" in payload:
        is_valid, error = _validate_enum_field(
            "external-web-format",
            payload["external-web-format"],
            VALID_BODY_EXTERNAL_WEB_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-username-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-username-delimiter",
            payload["mac-username-delimiter"],
            VALID_BODY_MAC_USERNAME_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-password-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-password-delimiter",
            payload["mac-password-delimiter"],
            VALID_BODY_MAC_PASSWORD_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-calling-station-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-calling-station-delimiter",
            payload["mac-calling-station-delimiter"],
            VALID_BODY_MAC_CALLING_STATION_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-called-station-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-called-station-delimiter",
            payload["mac-called-station-delimiter"],
            VALID_BODY_MAC_CALLED_STATION_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-case" in payload:
        is_valid, error = _validate_enum_field(
            "mac-case",
            payload["mac-case"],
            VALID_BODY_MAC_CASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "called-station-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "called-station-id-type",
            payload["called-station-id-type"],
            VALID_BODY_CALLED_STATION_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "mac-auth-bypass",
            payload["mac-auth-bypass"],
            VALID_BODY_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-mac-auth" in payload:
        is_valid, error = _validate_enum_field(
            "radius-mac-auth",
            payload["radius-mac-auth"],
            VALID_BODY_RADIUS_MAC_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-mac-mpsk-auth" in payload:
        is_valid, error = _validate_enum_field(
            "radius-mac-mpsk-auth",
            payload["radius-mac-mpsk-auth"],
            VALID_BODY_RADIUS_MAC_MPSK_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth" in payload:
        is_valid, error = _validate_enum_field(
            "auth",
            payload["auth"],
            VALID_BODY_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encrypt" in payload:
        is_valid, error = _validate_enum_field(
            "encrypt",
            payload["encrypt"],
            VALID_BODY_ENCRYPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-h2e-only" in payload:
        is_valid, error = _validate_enum_field(
            "sae-h2e-only",
            payload["sae-h2e-only"],
            VALID_BODY_SAE_H2E_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-hnp-only" in payload:
        is_valid, error = _validate_enum_field(
            "sae-hnp-only",
            payload["sae-hnp-only"],
            VALID_BODY_SAE_HNP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-pk" in payload:
        is_valid, error = _validate_enum_field(
            "sae-pk",
            payload["sae-pk"],
            VALID_BODY_SAE_PK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "akm24-only" in payload:
        is_valid, error = _validate_enum_field(
            "akm24-only",
            payload["akm24-only"],
            VALID_BODY_AKM24_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nas-filter-rule" in payload:
        is_valid, error = _validate_enum_field(
            "nas-filter-rule",
            payload["nas-filter-rule"],
            VALID_BODY_NAS_FILTER_RULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "domain-name-stripping" in payload:
        is_valid, error = _validate_enum_field(
            "domain-name-stripping",
            payload["domain-name-stripping"],
            VALID_BODY_DOMAIN_NAME_STRIPPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mlo" in payload:
        is_valid, error = _validate_enum_field(
            "mlo",
            payload["mlo"],
            VALID_BODY_MLO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-standalone" in payload:
        is_valid, error = _validate_enum_field(
            "local-standalone",
            payload["local-standalone"],
            VALID_BODY_LOCAL_STANDALONE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-standalone-nat" in payload:
        is_valid, error = _validate_enum_field(
            "local-standalone-nat",
            payload["local-standalone-nat"],
            VALID_BODY_LOCAL_STANDALONE_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-standalone-dns" in payload:
        is_valid, error = _validate_enum_field(
            "local-standalone-dns",
            payload["local-standalone-dns"],
            VALID_BODY_LOCAL_STANDALONE_DNS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-lan-partition" in payload:
        is_valid, error = _validate_enum_field(
            "local-lan-partition",
            payload["local-lan-partition"],
            VALID_BODY_LOCAL_LAN_PARTITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-bridging" in payload:
        is_valid, error = _validate_enum_field(
            "local-bridging",
            payload["local-bridging"],
            VALID_BODY_LOCAL_BRIDGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-lan" in payload:
        is_valid, error = _validate_enum_field(
            "local-lan",
            payload["local-lan"],
            VALID_BODY_LOCAL_LAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "local-authentication",
            payload["local-authentication"],
            VALID_BODY_LOCAL_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal",
            payload["captive-portal"],
            VALID_BODY_CAPTIVE_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-network-assistant-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "captive-network-assistant-bypass",
            payload["captive-network-assistant-bypass"],
            VALID_BODY_CAPTIVE_NETWORK_ASSISTANT_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "portal-type" in payload:
        is_valid, error = _validate_enum_field(
            "portal-type",
            payload["portal-type"],
            VALID_BODY_PORTAL_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "intra-vap-privacy" in payload:
        is_valid, error = _validate_enum_field(
            "intra-vap-privacy",
            payload["intra-vap-privacy"],
            VALID_BODY_INTRA_VAP_PRIVACY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldpc" in payload:
        is_valid, error = _validate_enum_field(
            "ldpc",
            payload["ldpc"],
            VALID_BODY_LDPC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "high-efficiency" in payload:
        is_valid, error = _validate_enum_field(
            "high-efficiency",
            payload["high-efficiency"],
            VALID_BODY_HIGH_EFFICIENCY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "target-wake-time" in payload:
        is_valid, error = _validate_enum_field(
            "target-wake-time",
            payload["target-wake-time"],
            VALID_BODY_TARGET_WAKE_TIME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-macauth" in payload:
        is_valid, error = _validate_enum_field(
            "port-macauth",
            payload["port-macauth"],
            VALID_BODY_PORT_MACAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bss-color-partial" in payload:
        is_valid, error = _validate_enum_field(
            "bss-color-partial",
            payload["bss-color-partial"],
            VALID_BODY_BSS_COLOR_PARTIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "split-tunneling" in payload:
        is_valid, error = _validate_enum_field(
            "split-tunneling",
            payload["split-tunneling"],
            VALID_BODY_SPLIT_TUNNELING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nac" in payload:
        is_valid, error = _validate_enum_field(
            "nac",
            payload["nac"],
            VALID_BODY_NAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-auto" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-auto",
            payload["vlan-auto"],
            VALID_BODY_VLAN_AUTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-vlan",
            payload["dynamic-vlan"],
            VALID_BODY_DYNAMIC_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal-fw-accounting" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal-fw-accounting",
            payload["captive-portal-fw-accounting"],
            VALID_BODY_CAPTIVE_PORTAL_FW_ACCOUNTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-rate" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-rate",
            payload["multicast-rate"],
            VALID_BODY_MULTICAST_RATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-enhance" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-enhance",
            payload["multicast-enhance"],
            VALID_BODY_MULTICAST_ENHANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "igmp-snooping" in payload:
        is_valid, error = _validate_enum_field(
            "igmp-snooping",
            payload["igmp-snooping"],
            VALID_BODY_IGMP_SNOOPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-address-enforcement" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-address-enforcement",
            payload["dhcp-address-enforcement"],
            VALID_BODY_DHCP_ADDRESS_ENFORCEMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-suppression" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-suppression",
            payload["broadcast-suppression"],
            VALID_BODY_BROADCAST_SUPPRESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-rules" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-rules",
            payload["ipv6-rules"],
            VALID_BODY_IPV6_RULES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mu-mimo" in payload:
        is_valid, error = _validate_enum_field(
            "mu-mimo",
            payload["mu-mimo"],
            VALID_BODY_MU_MIMO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "probe-resp-suppression" in payload:
        is_valid, error = _validate_enum_field(
            "probe-resp-suppression",
            payload["probe-resp-suppression"],
            VALID_BODY_PROBE_RESP_SUPPRESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radio-sensitivity" in payload:
        is_valid, error = _validate_enum_field(
            "radio-sensitivity",
            payload["radio-sensitivity"],
            VALID_BODY_RADIO_SENSITIVITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quarantine" in payload:
        is_valid, error = _validate_enum_field(
            "quarantine",
            payload["quarantine"],
            VALID_BODY_QUARANTINE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-pooling" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-pooling",
            payload["vlan-pooling"],
            VALID_BODY_VLAN_POOLING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option43-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option43-insertion",
            payload["dhcp-option43-insertion"],
            VALID_BODY_DHCP_OPTION43_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-insertion",
            payload["dhcp-option82-insertion"],
            VALID_BODY_DHCP_OPTION82_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-circuit-id-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-circuit-id-insertion",
            payload["dhcp-option82-circuit-id-insertion"],
            VALID_BODY_DHCP_OPTION82_CIRCUIT_ID_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-remote-id-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-remote-id-insertion",
            payload["dhcp-option82-remote-id-insertion"],
            VALID_BODY_DHCP_OPTION82_REMOTE_ID_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ptk-rekey" in payload:
        is_valid, error = _validate_enum_field(
            "ptk-rekey",
            payload["ptk-rekey"],
            VALID_BODY_PTK_REKEY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gtk-rekey" in payload:
        is_valid, error = _validate_enum_field(
            "gtk-rekey",
            payload["gtk-rekey"],
            VALID_BODY_GTK_REKEY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-reauth" in payload:
        is_valid, error = _validate_enum_field(
            "eap-reauth",
            payload["eap-reauth"],
            VALID_BODY_EAP_REAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "roaming-acct-interim-update" in payload:
        is_valid, error = _validate_enum_field(
            "roaming-acct-interim-update",
            payload["roaming-acct-interim-update"],
            VALID_BODY_ROAMING_ACCT_INTERIM_UPDATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11a" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11a",
            payload["rates-11a"],
            VALID_BODY_RATES_11A,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11bg" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11bg",
            payload["rates-11bg"],
            VALID_BODY_RATES_11BG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11n-ss12" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11n-ss12",
            payload["rates-11n-ss12"],
            VALID_BODY_RATES_11N_SS12,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11n-ss34" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11n-ss34",
            payload["rates-11n-ss34"],
            VALID_BODY_RATES_11N_SS34,
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
    if "utm-log" in payload:
        is_valid, error = _validate_enum_field(
            "utm-log",
            payload["utm-log"],
            VALID_BODY_UTM_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scan-botnet-connections" in payload:
        is_valid, error = _validate_enum_field(
            "scan-botnet-connections",
            payload["scan-botnet-connections"],
            VALID_BODY_SCAN_BOTNET_CONNECTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "address-group-policy" in payload:
        is_valid, error = _validate_enum_field(
            "address-group-policy",
            payload["address-group-policy"],
            VALID_BODY_ADDRESS_GROUP_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sticky-client-remove" in payload:
        is_valid, error = _validate_enum_field(
            "sticky-client-remove",
            payload["sticky-client-remove"],
            VALID_BODY_STICKY_CLIENT_REMOVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bstm-disassociation-imminent" in payload:
        is_valid, error = _validate_enum_field(
            "bstm-disassociation-imminent",
            payload["bstm-disassociation-imminent"],
            VALID_BODY_BSTM_DISASSOCIATION_IMMINENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "beacon-advertising" in payload:
        is_valid, error = _validate_enum_field(
            "beacon-advertising",
            payload["beacon-advertising"],
            VALID_BODY_BEACON_ADVERTISING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "osen" in payload:
        is_valid, error = _validate_enum_field(
            "osen",
            payload["osen"],
            VALID_BODY_OSEN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-detection-engine" in payload:
        is_valid, error = _validate_enum_field(
            "application-detection-engine",
            payload["application-detection-engine"],
            VALID_BODY_APPLICATION_DETECTION_ENGINE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-dscp-marking" in payload:
        is_valid, error = _validate_enum_field(
            "application-dscp-marking",
            payload["application-dscp-marking"],
            VALID_BODY_APPLICATION_DSCP_MARKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l3-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "l3-roaming",
            payload["l3-roaming"],
            VALID_BODY_L3_ROAMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l3-roaming-mode" in payload:
        is_valid, error = _validate_enum_field(
            "l3-roaming-mode",
            payload["l3-roaming-mode"],
            VALID_BODY_L3_ROAMING_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_wireless_controller_vap_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update wireless_controller/vap."""
    # Validate enum values using central function
    if "pre-auth" in payload:
        is_valid, error = _validate_enum_field(
            "pre-auth",
            payload["pre-auth"],
            VALID_BODY_PRE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external-pre-auth" in payload:
        is_valid, error = _validate_enum_field(
            "external-pre-auth",
            payload["external-pre-auth"],
            VALID_BODY_EXTERNAL_PRE_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mesh-backhaul" in payload:
        is_valid, error = _validate_enum_field(
            "mesh-backhaul",
            payload["mesh-backhaul"],
            VALID_BODY_MESH_BACKHAUL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-ssid" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-ssid",
            payload["broadcast-ssid"],
            VALID_BODY_BROADCAST_SSID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "security" in payload:
        is_valid, error = _validate_enum_field(
            "security",
            payload["security"],
            VALID_BODY_SECURITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pmf" in payload:
        is_valid, error = _validate_enum_field(
            "pmf",
            payload["pmf"],
            VALID_BODY_PMF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "beacon-protection" in payload:
        is_valid, error = _validate_enum_field(
            "beacon-protection",
            payload["beacon-protection"],
            VALID_BODY_BEACON_PROTECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "okc" in payload:
        is_valid, error = _validate_enum_field(
            "okc",
            payload["okc"],
            VALID_BODY_OKC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mbo" in payload:
        is_valid, error = _validate_enum_field(
            "mbo",
            payload["mbo"],
            VALID_BODY_MBO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mbo-cell-data-conn-pref" in payload:
        is_valid, error = _validate_enum_field(
            "mbo-cell-data-conn-pref",
            payload["mbo-cell-data-conn-pref"],
            VALID_BODY_MBO_CELL_DATA_CONN_PREF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "80211k" in payload:
        is_valid, error = _validate_enum_field(
            "80211k",
            payload["80211k"],
            VALID_BODY_80211K,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "80211v" in payload:
        is_valid, error = _validate_enum_field(
            "80211v",
            payload["80211v"],
            VALID_BODY_80211V,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "neighbor-report-dual-band" in payload:
        is_valid, error = _validate_enum_field(
            "neighbor-report-dual-band",
            payload["neighbor-report-dual-band"],
            VALID_BODY_NEIGHBOR_REPORT_DUAL_BAND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fast-bss-transition" in payload:
        is_valid, error = _validate_enum_field(
            "fast-bss-transition",
            payload["fast-bss-transition"],
            VALID_BODY_FAST_BSS_TRANSITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ft-over-ds" in payload:
        is_valid, error = _validate_enum_field(
            "ft-over-ds",
            payload["ft-over-ds"],
            VALID_BODY_FT_OVER_DS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-groups" in payload:
        is_valid, error = _validate_enum_field(
            "sae-groups",
            payload["sae-groups"],
            VALID_BODY_SAE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "owe-groups" in payload:
        is_valid, error = _validate_enum_field(
            "owe-groups",
            payload["owe-groups"],
            VALID_BODY_OWE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "owe-transition" in payload:
        is_valid, error = _validate_enum_field(
            "owe-transition",
            payload["owe-transition"],
            VALID_BODY_OWE_TRANSITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "additional-akms" in payload:
        is_valid, error = _validate_enum_field(
            "additional-akms",
            payload["additional-akms"],
            VALID_BODY_ADDITIONAL_AKMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eapol-key-retries" in payload:
        is_valid, error = _validate_enum_field(
            "eapol-key-retries",
            payload["eapol-key-retries"],
            VALID_BODY_EAPOL_KEY_RETRIES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tkip-counter-measure" in payload:
        is_valid, error = _validate_enum_field(
            "tkip-counter-measure",
            payload["tkip-counter-measure"],
            VALID_BODY_TKIP_COUNTER_MEASURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "external-web-format" in payload:
        is_valid, error = _validate_enum_field(
            "external-web-format",
            payload["external-web-format"],
            VALID_BODY_EXTERNAL_WEB_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-username-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-username-delimiter",
            payload["mac-username-delimiter"],
            VALID_BODY_MAC_USERNAME_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-password-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-password-delimiter",
            payload["mac-password-delimiter"],
            VALID_BODY_MAC_PASSWORD_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-calling-station-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-calling-station-delimiter",
            payload["mac-calling-station-delimiter"],
            VALID_BODY_MAC_CALLING_STATION_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-called-station-delimiter" in payload:
        is_valid, error = _validate_enum_field(
            "mac-called-station-delimiter",
            payload["mac-called-station-delimiter"],
            VALID_BODY_MAC_CALLED_STATION_DELIMITER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-case" in payload:
        is_valid, error = _validate_enum_field(
            "mac-case",
            payload["mac-case"],
            VALID_BODY_MAC_CASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "called-station-id-type" in payload:
        is_valid, error = _validate_enum_field(
            "called-station-id-type",
            payload["called-station-id-type"],
            VALID_BODY_CALLED_STATION_ID_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "mac-auth-bypass",
            payload["mac-auth-bypass"],
            VALID_BODY_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-mac-auth" in payload:
        is_valid, error = _validate_enum_field(
            "radius-mac-auth",
            payload["radius-mac-auth"],
            VALID_BODY_RADIUS_MAC_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-mac-mpsk-auth" in payload:
        is_valid, error = _validate_enum_field(
            "radius-mac-mpsk-auth",
            payload["radius-mac-mpsk-auth"],
            VALID_BODY_RADIUS_MAC_MPSK_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth" in payload:
        is_valid, error = _validate_enum_field(
            "auth",
            payload["auth"],
            VALID_BODY_AUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encrypt" in payload:
        is_valid, error = _validate_enum_field(
            "encrypt",
            payload["encrypt"],
            VALID_BODY_ENCRYPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-h2e-only" in payload:
        is_valid, error = _validate_enum_field(
            "sae-h2e-only",
            payload["sae-h2e-only"],
            VALID_BODY_SAE_H2E_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-hnp-only" in payload:
        is_valid, error = _validate_enum_field(
            "sae-hnp-only",
            payload["sae-hnp-only"],
            VALID_BODY_SAE_HNP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sae-pk" in payload:
        is_valid, error = _validate_enum_field(
            "sae-pk",
            payload["sae-pk"],
            VALID_BODY_SAE_PK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "akm24-only" in payload:
        is_valid, error = _validate_enum_field(
            "akm24-only",
            payload["akm24-only"],
            VALID_BODY_AKM24_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nas-filter-rule" in payload:
        is_valid, error = _validate_enum_field(
            "nas-filter-rule",
            payload["nas-filter-rule"],
            VALID_BODY_NAS_FILTER_RULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "domain-name-stripping" in payload:
        is_valid, error = _validate_enum_field(
            "domain-name-stripping",
            payload["domain-name-stripping"],
            VALID_BODY_DOMAIN_NAME_STRIPPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mlo" in payload:
        is_valid, error = _validate_enum_field(
            "mlo",
            payload["mlo"],
            VALID_BODY_MLO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-standalone" in payload:
        is_valid, error = _validate_enum_field(
            "local-standalone",
            payload["local-standalone"],
            VALID_BODY_LOCAL_STANDALONE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-standalone-nat" in payload:
        is_valid, error = _validate_enum_field(
            "local-standalone-nat",
            payload["local-standalone-nat"],
            VALID_BODY_LOCAL_STANDALONE_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-standalone-dns" in payload:
        is_valid, error = _validate_enum_field(
            "local-standalone-dns",
            payload["local-standalone-dns"],
            VALID_BODY_LOCAL_STANDALONE_DNS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-lan-partition" in payload:
        is_valid, error = _validate_enum_field(
            "local-lan-partition",
            payload["local-lan-partition"],
            VALID_BODY_LOCAL_LAN_PARTITION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-bridging" in payload:
        is_valid, error = _validate_enum_field(
            "local-bridging",
            payload["local-bridging"],
            VALID_BODY_LOCAL_BRIDGING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-lan" in payload:
        is_valid, error = _validate_enum_field(
            "local-lan",
            payload["local-lan"],
            VALID_BODY_LOCAL_LAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "local-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "local-authentication",
            payload["local-authentication"],
            VALID_BODY_LOCAL_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal",
            payload["captive-portal"],
            VALID_BODY_CAPTIVE_PORTAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-network-assistant-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "captive-network-assistant-bypass",
            payload["captive-network-assistant-bypass"],
            VALID_BODY_CAPTIVE_NETWORK_ASSISTANT_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "portal-type" in payload:
        is_valid, error = _validate_enum_field(
            "portal-type",
            payload["portal-type"],
            VALID_BODY_PORTAL_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "intra-vap-privacy" in payload:
        is_valid, error = _validate_enum_field(
            "intra-vap-privacy",
            payload["intra-vap-privacy"],
            VALID_BODY_INTRA_VAP_PRIVACY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldpc" in payload:
        is_valid, error = _validate_enum_field(
            "ldpc",
            payload["ldpc"],
            VALID_BODY_LDPC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "high-efficiency" in payload:
        is_valid, error = _validate_enum_field(
            "high-efficiency",
            payload["high-efficiency"],
            VALID_BODY_HIGH_EFFICIENCY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "target-wake-time" in payload:
        is_valid, error = _validate_enum_field(
            "target-wake-time",
            payload["target-wake-time"],
            VALID_BODY_TARGET_WAKE_TIME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-macauth" in payload:
        is_valid, error = _validate_enum_field(
            "port-macauth",
            payload["port-macauth"],
            VALID_BODY_PORT_MACAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bss-color-partial" in payload:
        is_valid, error = _validate_enum_field(
            "bss-color-partial",
            payload["bss-color-partial"],
            VALID_BODY_BSS_COLOR_PARTIAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "split-tunneling" in payload:
        is_valid, error = _validate_enum_field(
            "split-tunneling",
            payload["split-tunneling"],
            VALID_BODY_SPLIT_TUNNELING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nac" in payload:
        is_valid, error = _validate_enum_field(
            "nac",
            payload["nac"],
            VALID_BODY_NAC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-auto" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-auto",
            payload["vlan-auto"],
            VALID_BODY_VLAN_AUTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-vlan" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-vlan",
            payload["dynamic-vlan"],
            VALID_BODY_DYNAMIC_VLAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal-fw-accounting" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal-fw-accounting",
            payload["captive-portal-fw-accounting"],
            VALID_BODY_CAPTIVE_PORTAL_FW_ACCOUNTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-rate" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-rate",
            payload["multicast-rate"],
            VALID_BODY_MULTICAST_RATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multicast-enhance" in payload:
        is_valid, error = _validate_enum_field(
            "multicast-enhance",
            payload["multicast-enhance"],
            VALID_BODY_MULTICAST_ENHANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "igmp-snooping" in payload:
        is_valid, error = _validate_enum_field(
            "igmp-snooping",
            payload["igmp-snooping"],
            VALID_BODY_IGMP_SNOOPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-address-enforcement" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-address-enforcement",
            payload["dhcp-address-enforcement"],
            VALID_BODY_DHCP_ADDRESS_ENFORCEMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "broadcast-suppression" in payload:
        is_valid, error = _validate_enum_field(
            "broadcast-suppression",
            payload["broadcast-suppression"],
            VALID_BODY_BROADCAST_SUPPRESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-rules" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-rules",
            payload["ipv6-rules"],
            VALID_BODY_IPV6_RULES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "mu-mimo" in payload:
        is_valid, error = _validate_enum_field(
            "mu-mimo",
            payload["mu-mimo"],
            VALID_BODY_MU_MIMO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "probe-resp-suppression" in payload:
        is_valid, error = _validate_enum_field(
            "probe-resp-suppression",
            payload["probe-resp-suppression"],
            VALID_BODY_PROBE_RESP_SUPPRESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radio-sensitivity" in payload:
        is_valid, error = _validate_enum_field(
            "radio-sensitivity",
            payload["radio-sensitivity"],
            VALID_BODY_RADIO_SENSITIVITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quarantine" in payload:
        is_valid, error = _validate_enum_field(
            "quarantine",
            payload["quarantine"],
            VALID_BODY_QUARANTINE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vlan-pooling" in payload:
        is_valid, error = _validate_enum_field(
            "vlan-pooling",
            payload["vlan-pooling"],
            VALID_BODY_VLAN_POOLING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option43-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option43-insertion",
            payload["dhcp-option43-insertion"],
            VALID_BODY_DHCP_OPTION43_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-insertion",
            payload["dhcp-option82-insertion"],
            VALID_BODY_DHCP_OPTION82_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-circuit-id-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-circuit-id-insertion",
            payload["dhcp-option82-circuit-id-insertion"],
            VALID_BODY_DHCP_OPTION82_CIRCUIT_ID_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dhcp-option82-remote-id-insertion" in payload:
        is_valid, error = _validate_enum_field(
            "dhcp-option82-remote-id-insertion",
            payload["dhcp-option82-remote-id-insertion"],
            VALID_BODY_DHCP_OPTION82_REMOTE_ID_INSERTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ptk-rekey" in payload:
        is_valid, error = _validate_enum_field(
            "ptk-rekey",
            payload["ptk-rekey"],
            VALID_BODY_PTK_REKEY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gtk-rekey" in payload:
        is_valid, error = _validate_enum_field(
            "gtk-rekey",
            payload["gtk-rekey"],
            VALID_BODY_GTK_REKEY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "eap-reauth" in payload:
        is_valid, error = _validate_enum_field(
            "eap-reauth",
            payload["eap-reauth"],
            VALID_BODY_EAP_REAUTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "roaming-acct-interim-update" in payload:
        is_valid, error = _validate_enum_field(
            "roaming-acct-interim-update",
            payload["roaming-acct-interim-update"],
            VALID_BODY_ROAMING_ACCT_INTERIM_UPDATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11a" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11a",
            payload["rates-11a"],
            VALID_BODY_RATES_11A,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11bg" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11bg",
            payload["rates-11bg"],
            VALID_BODY_RATES_11BG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11n-ss12" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11n-ss12",
            payload["rates-11n-ss12"],
            VALID_BODY_RATES_11N_SS12,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rates-11n-ss34" in payload:
        is_valid, error = _validate_enum_field(
            "rates-11n-ss34",
            payload["rates-11n-ss34"],
            VALID_BODY_RATES_11N_SS34,
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
    if "utm-log" in payload:
        is_valid, error = _validate_enum_field(
            "utm-log",
            payload["utm-log"],
            VALID_BODY_UTM_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "scan-botnet-connections" in payload:
        is_valid, error = _validate_enum_field(
            "scan-botnet-connections",
            payload["scan-botnet-connections"],
            VALID_BODY_SCAN_BOTNET_CONNECTIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "address-group-policy" in payload:
        is_valid, error = _validate_enum_field(
            "address-group-policy",
            payload["address-group-policy"],
            VALID_BODY_ADDRESS_GROUP_POLICY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sticky-client-remove" in payload:
        is_valid, error = _validate_enum_field(
            "sticky-client-remove",
            payload["sticky-client-remove"],
            VALID_BODY_STICKY_CLIENT_REMOVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bstm-disassociation-imminent" in payload:
        is_valid, error = _validate_enum_field(
            "bstm-disassociation-imminent",
            payload["bstm-disassociation-imminent"],
            VALID_BODY_BSTM_DISASSOCIATION_IMMINENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "beacon-advertising" in payload:
        is_valid, error = _validate_enum_field(
            "beacon-advertising",
            payload["beacon-advertising"],
            VALID_BODY_BEACON_ADVERTISING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "osen" in payload:
        is_valid, error = _validate_enum_field(
            "osen",
            payload["osen"],
            VALID_BODY_OSEN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-detection-engine" in payload:
        is_valid, error = _validate_enum_field(
            "application-detection-engine",
            payload["application-detection-engine"],
            VALID_BODY_APPLICATION_DETECTION_ENGINE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-dscp-marking" in payload:
        is_valid, error = _validate_enum_field(
            "application-dscp-marking",
            payload["application-dscp-marking"],
            VALID_BODY_APPLICATION_DSCP_MARKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l3-roaming" in payload:
        is_valid, error = _validate_enum_field(
            "l3-roaming",
            payload["l3-roaming"],
            VALID_BODY_L3_ROAMING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "l3-roaming-mode" in payload:
        is_valid, error = _validate_enum_field(
            "l3-roaming-mode",
            payload["l3-roaming-mode"],
            VALID_BODY_L3_ROAMING_MODE,
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
    "endpoint": "wireless_controller/vap",
    "category": "cmdb",
    "api_path": "wireless-controller/vap",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure Virtual Access Points (VAPs).",
    "total_fields": 172,
    "required_fields_count": 1,
    "fields_with_defaults_count": 160,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
