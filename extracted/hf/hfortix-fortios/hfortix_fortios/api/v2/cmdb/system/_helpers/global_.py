"""Validation helpers for system/global_ - Auto-generated"""

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
    "restart-time",  # Daily restart time (hh:mm).
    "wad-restart-start-time",  # WAD workers daily restart time (hh:mm).
    "wad-restart-end-time",  # WAD workers daily restart end time (hh:mm).
    "timezone",  # Timezone database name. Enter ? to view the list of timezone.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "language": "english",
    "gui-ipv6": "disable",
    "gui-replacement-message-groups": "disable",
    "gui-local-out": "disable",
    "gui-certificates": "enable",
    "gui-custom-language": "disable",
    "gui-wireless-opensecurity": "disable",
    "gui-app-detection-sdwan": "disable",
    "gui-display-hostname": "disable",
    "gui-fortigate-cloud-sandbox": "disable",
    "gui-firmware-upgrade-warning": "enable",
    "gui-forticare-registration-setup-warning": "enable",
    "gui-auto-upgrade-setup-warning": "enable",
    "gui-workflow-management": "disable",
    "gui-cdn-usage": "enable",
    "admin-https-ssl-versions": "tlsv1-2 tlsv1-3",
    "admin-https-ssl-ciphersuites": "TLS-AES-128-GCM-SHA256 TLS-AES-256-GCM-SHA384 TLS-CHACHA20-POLY1305-SHA256",
    "admin-https-ssl-banned-ciphers": "",
    "admintimeout": 5,
    "admin-console-timeout": 0,
    "ssd-trim-freq": "weekly",
    "ssd-trim-hour": 1,
    "ssd-trim-min": 60,
    "ssd-trim-weekday": "sunday",
    "ssd-trim-date": 1,
    "admin-concurrent": "enable",
    "admin-lockout-threshold": 3,
    "admin-lockout-duration": 60,
    "refresh": 0,
    "interval": 5,
    "failtime": 5,
    "purdue-level": "3",
    "daily-restart": "disable",
    "restart-time": "",
    "wad-restart-mode": "none",
    "wad-restart-start-time": "",
    "wad-restart-end-time": "",
    "wad-p2s-max-body-size": 4,
    "radius-port": 1812,
    "speedtestd-server-port": 5201,
    "speedtestd-ctrl-port": 5200,
    "admin-login-max": 100,
    "remoteauthtimeout": 5,
    "ldapconntimeout": 500,
    "batch-cmdb": "enable",
    "multi-factor-authentication": "optional",
    "ssl-min-proto-version": "TLSv1-2",
    "autorun-log-fsck": "disable",
    "timezone": "",
    "traffic-priority": "tos",
    "traffic-priority-level": "medium",
    "quic-congestion-control-algo": "cubic",
    "quic-max-datagram-size": 1500,
    "quic-udp-payload-size-shaping-per-cid": "enable",
    "quic-ack-thresold": 3,
    "quic-pmtud": "enable",
    "quic-tls-handshake-timeout": 5,
    "anti-replay": "strict",
    "send-pmtu-icmp": "enable",
    "honor-df": "enable",
    "pmtu-discovery": "disable",
    "revision-image-auto-backup": "disable",
    "revision-backup-on-logout": "disable",
    "management-vdom": "root",
    "hostname": "",
    "alias": "",
    "strong-crypto": "enable",
    "ssl-static-key-ciphers": "enable",
    "snat-route-change": "disable",
    "ipv6-snat-route-change": "disable",
    "speedtest-server": "disable",
    "cli-audit-log": "disable",
    "dh-params": "2048",
    "fds-statistics": "enable",
    "fds-statistics-period": 60,
    "tcp-option": "enable",
    "lldp-transmission": "disable",
    "lldp-reception": "disable",
    "proxy-auth-timeout": 10,
    "proxy-keep-alive-mode": "session",
    "proxy-re-authentication-time": 30,
    "proxy-auth-lifetime": "disable",
    "proxy-auth-lifetime-timeout": 480,
    "proxy-resource-mode": "disable",
    "proxy-cert-use-mgmt-vdom": "disable",
    "sys-perf-log-interval": 5,
    "check-protocol-header": "loose",
    "vip-arp-range": "restricted",
    "reset-sessionless-tcp": "disable",
    "allow-traffic-redirect": "disable",
    "ipv6-allow-traffic-redirect": "disable",
    "strict-dirty-session-check": "enable",
    "tcp-halfclose-timer": 120,
    "tcp-halfopen-timer": 10,
    "tcp-timewait-timer": 1,
    "tcp-rst-timer": 5,
    "udp-idle-timer": 180,
    "block-session-timer": 30,
    "ip-src-port-range": "1024-25000",
    "pre-login-banner": "disable",
    "post-login-banner": "disable",
    "tftp": "enable",
    "av-failopen": "pass",
    "av-failopen-session": "disable",
    "memory-use-threshold-extreme": 95,
    "memory-use-threshold-red": 88,
    "memory-use-threshold-green": 82,
    "ip-fragment-mem-thresholds": 32,
    "ip-fragment-timeout": 30,
    "ipv6-fragment-timeout": 60,
    "cpu-use-threshold": 90,
    "log-single-cpu-high": "disable",
    "check-reset-range": "disable",
    "upgrade-report": "enable",
    "admin-port": 80,
    "admin-sport": 443,
    "admin-host": "",
    "admin-https-redirect": "enable",
    "admin-hsts-max-age": 63072000,
    "admin-ssh-password": "enable",
    "admin-restrict-local": "disable",
    "admin-ssh-port": 22,
    "admin-ssh-grace-time": 120,
    "admin-ssh-v1": "disable",
    "admin-telnet": "enable",
    "admin-telnet-port": 23,
    "admin-forticloud-sso-login": "disable",
    "admin-forticloud-sso-default-profile": "",
    "default-service-source-port": "",
    "admin-server-cert": "Fortinet_GUI_Server",
    "admin-https-pki-required": "disable",
    "wifi-certificate": "Fortinet_Wifi",
    "dhcp-lease-backup-interval": 60,
    "wifi-ca-certificate": "Fortinet_Wifi_CA",
    "auth-http-port": 1000,
    "auth-https-port": 1003,
    "auth-ike-saml-port": 1001,
    "auth-keepalive": "disable",
    "policy-auth-concurrent": 0,
    "auth-session-limit": "block-new",
    "auth-cert": "Fortinet_Factory",
    "clt-cert-req": "disable",
    "fortiservice-port": 8013,
    "cfg-save": "automatic",
    "cfg-revert-timeout": 600,
    "reboot-upon-config-restore": "enable",
    "admin-scp": "disable",
    "wireless-controller": "enable",
    "wireless-controller-port": 5246,
    "fortiextender-data-port": 25246,
    "fortiextender": "disable",
    "extender-controller-reserved-network": "10.252.0.1 255.255.0.0",
    "fortiextender-discovery-lockdown": "disable",
    "fortiextender-vlan-mode": "disable",
    "fortiextender-provision-on-authorization": "disable",
    "switch-controller": "disable",
    "switch-controller-reserved-network": "10.255.0.1 255.255.0.0",
    "dnsproxy-worker-count": 1,
    "url-filter-count": 1,
    "httpd-max-worker-count": 0,
    "proxy-worker-count": 0,
    "scanunit-count": 0,
    "fgd-alert-subscription": "",
    "ipv6-accept-dad": 1,
    "ipv6-allow-anycast-probe": "disable",
    "ipv6-allow-multicast-probe": "disable",
    "ipv6-allow-local-in-silent-drop": "enable",
    "csr-ca-attribute": "enable",
    "wimax-4g-usb": "disable",
    "cert-chain-max": 8,
    "sslvpn-max-worker-count": 0,
    "sslvpn-affinity": "0",
    "sslvpn-web-mode": "disable",
    "two-factor-ftk-expiry": 60,
    "two-factor-email-expiry": 60,
    "two-factor-sms-expiry": 60,
    "two-factor-fac-expiry": 60,
    "two-factor-ftm-expiry": 72,
    "per-user-bal": "disable",
    "wad-worker-count": 0,
    "wad-worker-dev-cache": 10240,
    "wad-csvc-cs-count": 1,
    "wad-csvc-db-count": 0,
    "wad-source-affinity": "enable",
    "wad-memory-change-granularity": 10,
    "login-timestamp": "disable",
    "ip-conflict-detection": "disable",
    "miglogd-children": 0,
    "log-daemon-cpu-threshold": 0,
    "special-file-23-support": "disable",
    "log-uuid-address": "disable",
    "log-ssl-connection": "disable",
    "gui-rest-api-cache": "enable",
    "rest-api-key-url-query": "disable",
    "arp-max-entry": 131072,
    "ha-affinity": "1",
    "bfd-affinity": "1",
    "cmdbsvr-affinity": "1",
    "av-affinity": "0",
    "wad-affinity": "0",
    "ips-affinity": "0",
    "miglog-affinity": "0",
    "syslog-affinity": "0",
    "url-filter-affinity": "0",
    "router-affinity": "0",
    "ndp-max-entry": 0,
    "br-fdb-max-entry": 8192,
    "max-route-cache-size": 0,
    "ipsec-qat-offload": "enable",
    "device-idle-timeout": 300,
    "user-device-store-max-devices": 62524,
    "user-device-store-max-device-mem": 2,
    "user-device-store-max-users": 62524,
    "user-device-store-max-unified-mem": 312621670,
    "gui-device-latitude": "",
    "gui-device-longitude": "",
    "private-data-encryption": "disable",
    "auto-auth-extension-device": "enable",
    "gui-theme": "jade",
    "gui-date-format": "yyyy/MM/dd",
    "gui-date-time-source": "system",
    "igmp-state-limit": 3200,
    "cloud-communication": "enable",
    "ipsec-ha-seqjump-rate": 10,
    "fortitoken-cloud": "enable",
    "fortitoken-cloud-push-status": "enable",
    "fortitoken-cloud-region": "",
    "fortitoken-cloud-sync-interval": 24,
    "faz-disk-buffer-size": 0,
    "irq-time-accounting": "auto",
    "management-ip": "",
    "management-port": 443,
    "management-port-use-admin-sport": "enable",
    "forticonverter-integration": "disable",
    "forticonverter-config-upload": "disable",
    "internet-service-database": "full",
    "geoip-full-db": "enable",
    "early-tcp-npu-session": "disable",
    "npu-neighbor-update": "disable",
    "delay-tcp-npu-session": "disable",
    "interface-subnet-usage": "enable",
    "sflowd-max-children-num": 1,
    "fortigslb-integration": "disable",
    "user-history-password-threshold": 3,
    "auth-session-auto-backup": "disable",
    "auth-session-auto-backup-interval": "15min",
    "scim-https-port": 44559,
    "scim-http-port": 44558,
    "scim-server-cert": "Fortinet_Factory",
    "application-bandwidth-tracking": "disable",
    "tls-session-cache": "enable",
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
    "language": "option",  # GUI display language.
    "gui-ipv6": "option",  # Enable/disable IPv6 settings on the GUI.
    "gui-replacement-message-groups": "option",  # Enable/disable replacement message groups on the GUI.
    "gui-local-out": "option",  # Enable/disable Local-out traffic on the GUI.
    "gui-certificates": "option",  # Enable/disable the System > Certificate GUI page, allowing y
    "gui-custom-language": "option",  # Enable/disable custom languages in GUI.
    "gui-wireless-opensecurity": "option",  # Enable/disable wireless open security option on the GUI.
    "gui-app-detection-sdwan": "option",  # Enable/disable Allow app-detection based SD-WAN.
    "gui-display-hostname": "option",  # Enable/disable displaying the FortiGate's hostname on the GU
    "gui-fortigate-cloud-sandbox": "option",  # Enable/disable displaying FortiGate Cloud Sandbox on the GUI
    "gui-firmware-upgrade-warning": "option",  # Enable/disable the firmware upgrade warning on the GUI.
    "gui-forticare-registration-setup-warning": "option",  # Enable/disable the FortiCare registration setup warning on t
    "gui-auto-upgrade-setup-warning": "option",  # Enable/disable the automatic patch upgrade setup prompt on t
    "gui-workflow-management": "option",  # Enable/disable Workflow management features on the GUI.
    "gui-cdn-usage": "option",  # Enable/disable Load GUI static files from a CDN.
    "admin-https-ssl-versions": "option",  # Allowed TLS versions for web administration.
    "admin-https-ssl-ciphersuites": "option",  # Select one or more TLS 1.3 ciphersuites to enable. Does not 
    "admin-https-ssl-banned-ciphers": "option",  # Select one or more cipher technologies that cannot be used i
    "admintimeout": "integer",  # Number of minutes before an idle administrator session times
    "admin-console-timeout": "integer",  # Console login timeout that overrides the admin timeout value
    "ssd-trim-freq": "option",  # How often to run SSD Trim (default = weekly). SSD Trim preve
    "ssd-trim-hour": "integer",  # Hour of the day on which to run SSD Trim (0 - 23, default = 
    "ssd-trim-min": "integer",  # Minute of the hour on which to run SSD Trim (0 - 59, 60 for 
    "ssd-trim-weekday": "option",  # Day of week to run SSD Trim.
    "ssd-trim-date": "integer",  # Date within a month to run ssd trim.
    "admin-concurrent": "option",  # Enable/disable concurrent administrator logins. Use policy-a
    "admin-lockout-threshold": "integer",  # Number of failed login attempts before an administrator acco
    "admin-lockout-duration": "integer",  # Amount of time in seconds that an administrator account is l
    "refresh": "integer",  # Statistics refresh interval second(s) in GUI.
    "interval": "integer",  # Dead gateway detection interval.
    "failtime": "integer",  # Fail-time for server lost.
    "purdue-level": "option",  # Purdue Level of this FortiGate.
    "daily-restart": "option",  # Enable/disable daily restart of FortiGate unit. Use the rest
    "restart-time": "user",  # Daily restart time (hh:mm).
    "wad-restart-mode": "option",  # WAD worker restart mode (default = none).
    "wad-restart-start-time": "user",  # WAD workers daily restart time (hh:mm).
    "wad-restart-end-time": "user",  # WAD workers daily restart end time (hh:mm).
    "wad-p2s-max-body-size": "integer",  # Maximum size of the body of the local out HTTP request (1 - 
    "radius-port": "integer",  # RADIUS service port number.
    "speedtestd-server-port": "integer",  # Speedtest server port number.
    "speedtestd-ctrl-port": "integer",  # Speedtest server controller port number.
    "admin-login-max": "integer",  # Maximum number of administrators who can be logged in at the
    "remoteauthtimeout": "integer",  # Number of seconds that the FortiGate waits for responses fro
    "ldapconntimeout": "integer",  # Global timeout for connections with remote LDAP servers in m
    "batch-cmdb": "option",  # Enable/disable batch mode, allowing you to enter a series of
    "multi-factor-authentication": "option",  # Enforce all login methods to require an additional authentic
    "ssl-min-proto-version": "option",  # Minimum supported protocol version for SSL/TLS connections (
    "autorun-log-fsck": "option",  # Enable/disable automatic log partition check after ungracefu
    "timezone": "string",  # Timezone database name. Enter ? to view the list of timezone
    "traffic-priority": "option",  # Choose Type of Service (ToS) or Differentiated Services Code
    "traffic-priority-level": "option",  # Default system-wide level of priority for traffic prioritiza
    "quic-congestion-control-algo": "option",  # QUIC congestion control algorithm (default = cubic).
    "quic-max-datagram-size": "integer",  # Maximum transmit datagram size (1200 - 1500, default = 1500)
    "quic-udp-payload-size-shaping-per-cid": "option",  # Enable/disable UDP payload size shaping per connection ID (d
    "quic-ack-thresold": "integer",  # Maximum number of unacknowledged packets before sending ACK 
    "quic-pmtud": "option",  # Enable/disable path MTU discovery (default = enable).
    "quic-tls-handshake-timeout": "integer",  # Time-to-live (TTL) for TLS handshake in seconds (1 - 60, def
    "anti-replay": "option",  # Level of checking for packet replay and TCP sequence checkin
    "send-pmtu-icmp": "option",  # Enable/disable sending of path maximum transmission unit (PM
    "honor-df": "option",  # Enable/disable honoring of Don't-Fragment (DF) flag.
    "pmtu-discovery": "option",  # Enable/disable path MTU discovery.
    "revision-image-auto-backup": "option",  # Enable/disable back-up of the latest image revision after th
    "revision-backup-on-logout": "option",  # Enable/disable back-up of the latest configuration revision 
    "management-vdom": "string",  # Management virtual domain name.
    "hostname": "string",  # FortiGate unit's hostname. Most models will truncate names l
    "alias": "string",  # Alias for your FortiGate unit.
    "strong-crypto": "option",  # Enable to use strong encryption and only allow strong cipher
    "ssl-static-key-ciphers": "option",  # Enable/disable static key ciphers in SSL/TLS connections (e.
    "snat-route-change": "option",  # Enable/disable the ability to change the source NAT route.
    "ipv6-snat-route-change": "option",  # Enable/disable the ability to change the IPv6 source NAT rou
    "speedtest-server": "option",  # Enable/disable speed test server.
    "cli-audit-log": "option",  # Enable/disable CLI audit log.
    "dh-params": "option",  # Number of bits to use in the Diffie-Hellman exchange for HTT
    "fds-statistics": "option",  # Enable/disable sending IPS, Application Control, and AntiVir
    "fds-statistics-period": "integer",  # FortiGuard statistics collection period in minutes. (1 - 144
    "tcp-option": "option",  # Enable SACK, timestamp and MSS TCP options.
    "lldp-transmission": "option",  # Enable/disable Link Layer Discovery Protocol (LLDP) transmis
    "lldp-reception": "option",  # Enable/disable Link Layer Discovery Protocol (LLDP) receptio
    "proxy-auth-timeout": "integer",  # Authentication timeout in minutes for authenticated users (1
    "proxy-keep-alive-mode": "option",  # Control if users must re-authenticate after a session is clo
    "proxy-re-authentication-time": "integer",  # The time limit that users must re-authenticate if proxy-keep
    "proxy-auth-lifetime": "option",  # Enable/disable authenticated users lifetime control. This is
    "proxy-auth-lifetime-timeout": "integer",  # Lifetime timeout in minutes for authenticated users (5  - 65
    "proxy-resource-mode": "option",  # Enable/disable use of the maximum memory usage on the FortiG
    "proxy-cert-use-mgmt-vdom": "option",  # Enable/disable using management VDOM to send requests.
    "sys-perf-log-interval": "integer",  # Time in minutes between updates of performance statistics lo
    "check-protocol-header": "option",  # Level of checking performed on protocol headers. Strict chec
    "vip-arp-range": "option",  # Controls the number of ARPs that the FortiGate sends for a V
    "reset-sessionless-tcp": "option",  # Action to perform if the FortiGate receives a TCP packet but
    "allow-traffic-redirect": "option",  # Disable to prevent traffic with same local ingress and egres
    "ipv6-allow-traffic-redirect": "option",  # Disable to prevent IPv6 traffic with same local ingress and 
    "strict-dirty-session-check": "option",  # Enable to check the session against the original policy when
    "tcp-halfclose-timer": "integer",  # Number of seconds the FortiGate unit should wait to close a 
    "tcp-halfopen-timer": "integer",  # Number of seconds the FortiGate unit should wait to close a 
    "tcp-timewait-timer": "integer",  # Length of the TCP TIME-WAIT state in seconds (1 - 300 sec, d
    "tcp-rst-timer": "integer",  # Length of the TCP CLOSE state in seconds (5 - 300 sec, defau
    "udp-idle-timer": "integer",  # UDP connection session timeout. This command can be useful i
    "block-session-timer": "integer",  # Duration in seconds for blocked sessions (1 - 300 sec  (5 mi
    "ip-src-port-range": "user",  # IP source port range used for traffic originating from the F
    "pre-login-banner": "option",  # Enable/disable displaying the administrator access disclaime
    "post-login-banner": "option",  # Enable/disable displaying the administrator access disclaime
    "tftp": "option",  # Enable/disable TFTP.
    "av-failopen": "option",  # Set the action to take if the FortiGate is running low on me
    "av-failopen-session": "option",  # When enabled and a proxy for a protocol runs out of room in 
    "memory-use-threshold-extreme": "integer",  # Threshold at which memory usage is considered extreme (new s
    "memory-use-threshold-red": "integer",  # Threshold at which memory usage forces the FortiGate to ente
    "memory-use-threshold-green": "integer",  # Threshold at which memory usage forces the FortiGate to exit
    "ip-fragment-mem-thresholds": "integer",  # Maximum memory (MB) used to reassemble IPv4/IPv6 fragments.
    "ip-fragment-timeout": "integer",  # Timeout value in seconds for any fragment not being reassemb
    "ipv6-fragment-timeout": "integer",  # Timeout value in seconds for any IPv6 fragment not being rea
    "cpu-use-threshold": "integer",  # Threshold at which CPU usage is reported (% of total CPU, de
    "log-single-cpu-high": "option",  # Enable/disable logging the event of a single CPU core reachi
    "check-reset-range": "option",  # Configure ICMP error message verification. You can either ap
    "upgrade-report": "option",  # Enable/disable the generation of an upgrade report when upgr
    "admin-port": "integer",  # Administrative access port for HTTP. (1 - 65535, default = 8
    "admin-sport": "integer",  # Administrative access port for HTTPS. (1 - 65535, default = 
    "admin-host": "string",  # Administrative host for HTTP and HTTPS. When set, will be us
    "admin-https-redirect": "option",  # Enable/disable redirection of HTTP administration access to 
    "admin-hsts-max-age": "integer",  # HTTPS Strict-Transport-Security header max-age in seconds. A
    "admin-ssh-password": "option",  # Enable/disable password authentication for SSH admin access.
    "admin-restrict-local": "option",  # Enable/disable local admin authentication restriction when r
    "admin-ssh-port": "integer",  # Administrative access port for SSH. (1 - 65535, default = 22
    "admin-ssh-grace-time": "integer",  # Maximum time in seconds permitted between making an SSH conn
    "admin-ssh-v1": "option",  # Enable/disable SSH v1 compatibility.
    "admin-telnet": "option",  # Enable/disable TELNET service.
    "admin-telnet-port": "integer",  # Administrative access port for TELNET. (1 - 65535, default =
    "admin-forticloud-sso-login": "option",  # Enable/disable FortiCloud admin login via SSO.
    "admin-forticloud-sso-default-profile": "string",  # Override access profile.
    "default-service-source-port": "user",  # Default service source port range (default = 1 - 65535).
    "admin-server-cert": "string",  # Server certificate that the FortiGate uses for HTTPS adminis
    "admin-https-pki-required": "option",  # Enable/disable admin login method. Enable to force administr
    "wifi-certificate": "string",  # Certificate to use for WiFi authentication.
    "dhcp-lease-backup-interval": "integer",  # DHCP leases backup interval in seconds (10 - 3600, default =
    "wifi-ca-certificate": "string",  # CA certificate that verifies the WiFi certificate.
    "auth-http-port": "integer",  # User authentication HTTP port. (1 - 65535, default = 1000).
    "auth-https-port": "integer",  # User authentication HTTPS port. (1 - 65535, default = 1003).
    "auth-ike-saml-port": "integer",  # User IKE SAML authentication port (0 - 65535, default = 1001
    "auth-keepalive": "option",  # Enable to prevent user authentication sessions from timing o
    "policy-auth-concurrent": "integer",  # Number of concurrent firewall use logins from the same user 
    "auth-session-limit": "option",  # Action to take when the number of allowed user authenticated
    "auth-cert": "string",  # Server certificate that the FortiGate uses for HTTPS firewal
    "clt-cert-req": "option",  # Enable/disable requiring administrators to have a client cer
    "fortiservice-port": "integer",  # FortiService port (1 - 65535, default = 8013). Used by Forti
    "cfg-save": "option",  # Configuration file save mode for CLI changes.
    "cfg-revert-timeout": "integer",  # Time-out for reverting to the last saved configuration. (10 
    "reboot-upon-config-restore": "option",  # Enable/disable reboot of system upon restoring configuration
    "admin-scp": "option",  # Enable/disable SCP support for system configuration backup, 
    "wireless-controller": "option",  # Enable/disable the wireless controller feature to use the Fo
    "wireless-controller-port": "integer",  # Port used for the control channel in wireless controller mod
    "fortiextender-data-port": "integer",  # FortiExtender data port (1024 - 49150, default = 25246).
    "fortiextender": "option",  # Enable/disable FortiExtender.
    "extender-controller-reserved-network": "ipv4-classnet-host",  # Configure reserved network subnet for managed LAN extension 
    "fortiextender-discovery-lockdown": "option",  # Enable/disable FortiExtender CAPWAP lockdown.
    "fortiextender-vlan-mode": "option",  # Enable/disable FortiExtender VLAN mode.
    "fortiextender-provision-on-authorization": "option",  # Enable/disable automatic provisioning of latest FortiExtende
    "switch-controller": "option",  # Enable/disable switch controller feature. Switch controller 
    "switch-controller-reserved-network": "ipv4-classnet-host",  # Configure reserved network subnet for managed switches. This
    "dnsproxy-worker-count": "integer",  # DNS proxy worker count. For a FortiGate with multiple logica
    "url-filter-count": "integer",  # URL filter daemon count.
    "httpd-max-worker-count": "integer",  # Maximum number of simultaneous HTTP requests that will be se
    "proxy-worker-count": "integer",  # Proxy worker count.
    "scanunit-count": "integer",  # Number of scanunits. The range and the default depend on the
    "fgd-alert-subscription": "option",  # Type of alert to retrieve from FortiGuard.
    "ipv6-accept-dad": "integer",  # Enable/disable acceptance of IPv6 Duplicate Address Detectio
    "ipv6-allow-anycast-probe": "option",  # Enable/disable IPv6 address probe through Anycast.
    "ipv6-allow-multicast-probe": "option",  # Enable/disable IPv6 address probe through Multicast.
    "ipv6-allow-local-in-silent-drop": "option",  # Enable/disable silent drop of IPv6 local-in traffic.
    "csr-ca-attribute": "option",  # Enable/disable the CA attribute in certificates. Some CA ser
    "wimax-4g-usb": "option",  # Enable/disable comparability with WiMAX 4G USB devices.
    "cert-chain-max": "integer",  # Maximum number of certificates that can be traversed in a ce
    "sslvpn-max-worker-count": "integer",  # Maximum number of Agentless VPN processes. Upper limit for t
    "sslvpn-affinity": "string",  # Agentless VPN CPU affinity.
    "sslvpn-web-mode": "option",  # Enable/disable Agentless VPN web mode.
    "two-factor-ftk-expiry": "integer",  # FortiToken authentication session timeout (60 - 600 sec (10 
    "two-factor-email-expiry": "integer",  # Email-based two-factor authentication session timeout (30 - 
    "two-factor-sms-expiry": "integer",  # SMS-based two-factor authentication session timeout (30 - 30
    "two-factor-fac-expiry": "integer",  # FortiAuthenticator token authentication session timeout (10 
    "two-factor-ftm-expiry": "integer",  # FortiToken Mobile session timeout (1 - 168 hours (7 days), d
    "per-user-bal": "option",  # Enable/disable per-user block/allow list filter.
    "wad-worker-count": "integer",  # Number of explicit proxy WAN optimization daemon (WAD) proce
    "wad-worker-dev-cache": "integer",  # Number of cached devices for each ZTNA proxy worker. The def
    "wad-csvc-cs-count": "integer",  # Number of concurrent WAD-cache-service object-cache processe
    "wad-csvc-db-count": "integer",  # Number of concurrent WAD-cache-service byte-cache processes.
    "wad-source-affinity": "option",  # Enable/disable dispatching traffic to WAD workers based on s
    "wad-memory-change-granularity": "integer",  # Minimum percentage change in system memory usage detected by
    "login-timestamp": "option",  # Enable/disable login time recording.
    "ip-conflict-detection": "option",  # Enable/disable logging of IPv4 address conflict detection.
    "miglogd-children": "integer",  # Number of logging (miglogd) processes to be allowed to run. 
    "log-daemon-cpu-threshold": "integer",  # Configure syslog daemon process spawning threshold. Use a pe
    "special-file-23-support": "option",  # Enable/disable detection of those special format files when 
    "log-uuid-address": "option",  # Enable/disable insertion of address UUIDs to traffic logs.
    "log-ssl-connection": "option",  # Enable/disable logging of SSL connection events.
    "gui-rest-api-cache": "option",  # Enable/disable REST API result caching on FortiGate.
    "rest-api-key-url-query": "option",  # Enable/disable support for passing REST API keys through URL
    "arp-max-entry": "integer",  # Maximum number of dynamically learned MAC addresses that can
    "ha-affinity": "string",  # Affinity setting for HA daemons (hexadecimal value up to 256
    "bfd-affinity": "string",  # Affinity setting for BFD daemon (hexadecimal value up to 256
    "cmdbsvr-affinity": "string",  # Affinity setting for cmdbsvr (hexadecimal value up to 256 bi
    "av-affinity": "string",  # Affinity setting for AV scanning (hexadecimal value up to 25
    "wad-affinity": "string",  # Affinity setting for wad (hexadecimal value up to 256 bits i
    "ips-affinity": "string",  # Affinity setting for IPS (hexadecimal value up to 256 bits i
    "miglog-affinity": "string",  # Affinity setting for logging (hexadecimal value up to 256 bi
    "syslog-affinity": "string",  # Affinity setting for syslog (hexadecimal value up to 256 bit
    "url-filter-affinity": "string",  # URL filter CPU affinity.
    "router-affinity": "string",  # Affinity setting for BFD/VRRP/BGP/OSPF daemons (hexadecimal 
    "ndp-max-entry": "integer",  # Maximum number of NDP table entries (set to 65,536 or higher
    "br-fdb-max-entry": "integer",  # Maximum number of bridge forwarding database (FDB) entries.
    "max-route-cache-size": "integer",  # Maximum number of IP route cache entries (0 - 2147483647).
    "ipsec-qat-offload": "option",  # Enable/disable QAT offloading (Intel QuickAssist) for IPsec 
    "device-idle-timeout": "integer",  # Time in seconds that a device must be idle to automatically 
    "user-device-store-max-devices": "integer",  # Maximum number of devices allowed in user device store.
    "user-device-store-max-device-mem": "integer",  # Maximum percentage of total system memory allowed to be used
    "user-device-store-max-users": "integer",  # Maximum number of users allowed in user device store.
    "user-device-store-max-unified-mem": "integer",  # Maximum unified memory allowed in user device store.
    "gui-device-latitude": "string",  # Add the latitude of the location of this FortiGate to positi
    "gui-device-longitude": "string",  # Add the longitude of the location of this FortiGate to posit
    "private-data-encryption": "option",  # Enable/disable private data encryption using an AES 128-bit 
    "auto-auth-extension-device": "option",  # Enable/disable automatic authorization of dedicated Fortinet
    "gui-theme": "option",  # Color scheme for the administration GUI.
    "gui-date-format": "option",  # Default date format used throughout GUI.
    "gui-date-time-source": "option",  # Source from which the FortiGate GUI uses to display date and
    "igmp-state-limit": "integer",  # Maximum number of IGMP memberships (96 - 64000, default = 32
    "cloud-communication": "option",  # Enable/disable all cloud communication.
    "ipsec-ha-seqjump-rate": "integer",  # ESP jump ahead rate (1G - 10G pps equivalent).
    "fortitoken-cloud": "option",  # Enable/disable FortiToken Cloud service.
    "fortitoken-cloud-push-status": "option",  # Enable/disable FTM push service of FortiToken Cloud.
    "fortitoken-cloud-region": "string",  # Region domain of FortiToken Cloud(unset to non-region).
    "fortitoken-cloud-sync-interval": "integer",  # Interval in which to clean up remote users in FortiToken Clo
    "faz-disk-buffer-size": "integer",  # Maximum disk buffer size to temporarily store logs destined 
    "irq-time-accounting": "option",  # Configure CPU IRQ time accounting mode.
    "management-ip": "string",  # Management IP address of this FortiGate. Used to log into th
    "management-port": "integer",  # Overriding port for management connection (Overrides admin p
    "management-port-use-admin-sport": "option",  # Enable/disable use of the admin-sport setting for the manage
    "forticonverter-integration": "option",  # Enable/disable FortiConverter integration service.
    "forticonverter-config-upload": "option",  # Enable/disable config upload to FortiConverter.
    "internet-service-database": "option",  # Configure which Internet Service database size to download f
    "internet-service-download-list": "string",  # Configure which on-demand Internet Service IDs are to be dow
    "geoip-full-db": "option",  # When enabled, the full geographic database will be loaded in
    "early-tcp-npu-session": "option",  # Enable/disable early TCP NPU session.
    "npu-neighbor-update": "option",  # Enable/disable sending of ARP/ICMP6 probing packets to updat
    "delay-tcp-npu-session": "option",  # Enable TCP NPU session delay to guarantee packet order of 3-
    "interface-subnet-usage": "option",  # Enable/disable allowing use of interface-subnet setting in f
    "sflowd-max-children-num": "integer",  # Maximum number of sflowd child processes allowed to run.
    "fortigslb-integration": "option",  # Enable/disable integration with the FortiGSLB cloud service.
    "user-history-password-threshold": "integer",  # Maximum number of previous passwords saved per admin/user (3
    "auth-session-auto-backup": "option",  # Enable/disable automatic and periodic backup of authenticati
    "auth-session-auto-backup-interval": "option",  # Configure automatic authentication session backup interval (
    "scim-https-port": "integer",  # SCIM port (0 - 65535, default = 44559).
    "scim-http-port": "integer",  # SCIM http port (0 - 65535, default = 44558).
    "scim-server-cert": "string",  # Server certificate that the FortiGate uses for SCIM connecti
    "application-bandwidth-tracking": "option",  # Enable/disable application bandwidth tracking.
    "tls-session-cache": "option",  # Enable/disable TLS session cache.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "language": "GUI display language.",
    "gui-ipv6": "Enable/disable IPv6 settings on the GUI.",
    "gui-replacement-message-groups": "Enable/disable replacement message groups on the GUI.",
    "gui-local-out": "Enable/disable Local-out traffic on the GUI.",
    "gui-certificates": "Enable/disable the System > Certificate GUI page, allowing you to add and configure certificates from the GUI.",
    "gui-custom-language": "Enable/disable custom languages in GUI.",
    "gui-wireless-opensecurity": "Enable/disable wireless open security option on the GUI.",
    "gui-app-detection-sdwan": "Enable/disable Allow app-detection based SD-WAN.",
    "gui-display-hostname": "Enable/disable displaying the FortiGate's hostname on the GUI login page.",
    "gui-fortigate-cloud-sandbox": "Enable/disable displaying FortiGate Cloud Sandbox on the GUI.",
    "gui-firmware-upgrade-warning": "Enable/disable the firmware upgrade warning on the GUI.",
    "gui-forticare-registration-setup-warning": "Enable/disable the FortiCare registration setup warning on the GUI.",
    "gui-auto-upgrade-setup-warning": "Enable/disable the automatic patch upgrade setup prompt on the GUI.",
    "gui-workflow-management": "Enable/disable Workflow management features on the GUI.",
    "gui-cdn-usage": "Enable/disable Load GUI static files from a CDN.",
    "admin-https-ssl-versions": "Allowed TLS versions for web administration.",
    "admin-https-ssl-ciphersuites": "Select one or more TLS 1.3 ciphersuites to enable. Does not affect ciphers in TLS 1.2 and below. At least one must be enabled. To disable all, remove TLS1.3 from admin-https-ssl-versions.",
    "admin-https-ssl-banned-ciphers": "Select one or more cipher technologies that cannot be used in GUI HTTPS negotiations. Only applies to TLS 1.2 and below.",
    "admintimeout": "Number of minutes before an idle administrator session times out (1 - 480 minutes (8 hours), default = 5). A shorter idle timeout is more secure.",
    "admin-console-timeout": "Console login timeout that overrides the admin timeout value (15 - 300 seconds, default = 0, which disables the timeout).",
    "ssd-trim-freq": "How often to run SSD Trim (default = weekly). SSD Trim prevents SSD drive data loss by finding and isolating errors.",
    "ssd-trim-hour": "Hour of the day on which to run SSD Trim (0 - 23, default = 1).",
    "ssd-trim-min": "Minute of the hour on which to run SSD Trim (0 - 59, 60 for random).",
    "ssd-trim-weekday": "Day of week to run SSD Trim.",
    "ssd-trim-date": "Date within a month to run ssd trim.",
    "admin-concurrent": "Enable/disable concurrent administrator logins. Use policy-auth-concurrent for firewall authenticated users.",
    "admin-lockout-threshold": "Number of failed login attempts before an administrator account is locked out for the admin-lockout-duration.",
    "admin-lockout-duration": "Amount of time in seconds that an administrator account is locked out after reaching the admin-lockout-threshold for repeated failed login attempts.",
    "refresh": "Statistics refresh interval second(s) in GUI.",
    "interval": "Dead gateway detection interval.",
    "failtime": "Fail-time for server lost.",
    "purdue-level": "Purdue Level of this FortiGate.",
    "daily-restart": "Enable/disable daily restart of FortiGate unit. Use the restart-time option to set the time of day for the restart.",
    "restart-time": "Daily restart time (hh:mm).",
    "wad-restart-mode": "WAD worker restart mode (default = none).",
    "wad-restart-start-time": "WAD workers daily restart time (hh:mm).",
    "wad-restart-end-time": "WAD workers daily restart end time (hh:mm).",
    "wad-p2s-max-body-size": "Maximum size of the body of the local out HTTP request (1 - 32 Mbytes, default = 4).",
    "radius-port": "RADIUS service port number.",
    "speedtestd-server-port": "Speedtest server port number.",
    "speedtestd-ctrl-port": "Speedtest server controller port number.",
    "admin-login-max": "Maximum number of administrators who can be logged in at the same time (1 - 100, default = 100).",
    "remoteauthtimeout": "Number of seconds that the FortiGate waits for responses from remote RADIUS, LDAP, or TACACS+ authentication servers. (1-300 sec, default = 5).",
    "ldapconntimeout": "Global timeout for connections with remote LDAP servers in milliseconds (1 - 300000, default 500).",
    "batch-cmdb": "Enable/disable batch mode, allowing you to enter a series of CLI commands that will execute as a group once they are loaded.",
    "multi-factor-authentication": "Enforce all login methods to require an additional authentication factor (default = optional).",
    "ssl-min-proto-version": "Minimum supported protocol version for SSL/TLS connections (default = TLSv1.2).",
    "autorun-log-fsck": "Enable/disable automatic log partition check after ungraceful shutdown.",
    "timezone": "Timezone database name. Enter ? to view the list of timezone.",
    "traffic-priority": "Choose Type of Service (ToS) or Differentiated Services Code Point (DSCP) for traffic prioritization in traffic shaping.",
    "traffic-priority-level": "Default system-wide level of priority for traffic prioritization.",
    "quic-congestion-control-algo": "QUIC congestion control algorithm (default = cubic).",
    "quic-max-datagram-size": "Maximum transmit datagram size (1200 - 1500, default = 1500).",
    "quic-udp-payload-size-shaping-per-cid": "Enable/disable UDP payload size shaping per connection ID (default = enable).",
    "quic-ack-thresold": "Maximum number of unacknowledged packets before sending ACK (2 - 5, default = 3).",
    "quic-pmtud": "Enable/disable path MTU discovery (default = enable).",
    "quic-tls-handshake-timeout": "Time-to-live (TTL) for TLS handshake in seconds (1 - 60, default = 5).",
    "anti-replay": "Level of checking for packet replay and TCP sequence checking.",
    "send-pmtu-icmp": "Enable/disable sending of path maximum transmission unit (PMTU) - ICMP destination unreachable packet and to support PMTUD protocol on your network to reduce fragmentation of packets.",
    "honor-df": "Enable/disable honoring of Don't-Fragment (DF) flag.",
    "pmtu-discovery": "Enable/disable path MTU discovery.",
    "revision-image-auto-backup": "Enable/disable back-up of the latest image revision after the firmware is upgraded.",
    "revision-backup-on-logout": "Enable/disable back-up of the latest configuration revision when an administrator logs out of the CLI or GUI.",
    "management-vdom": "Management virtual domain name.",
    "hostname": "FortiGate unit's hostname. Most models will truncate names longer than 24 characters. Some models support hostnames up to 35 characters.",
    "alias": "Alias for your FortiGate unit.",
    "strong-crypto": "Enable to use strong encryption and only allow strong ciphers and digest for HTTPS/SSH/TLS/SSL functions.",
    "ssl-static-key-ciphers": "Enable/disable static key ciphers in SSL/TLS connections (e.g. AES128-SHA, AES256-SHA, AES128-SHA256, AES256-SHA256).",
    "snat-route-change": "Enable/disable the ability to change the source NAT route.",
    "ipv6-snat-route-change": "Enable/disable the ability to change the IPv6 source NAT route.",
    "speedtest-server": "Enable/disable speed test server.",
    "cli-audit-log": "Enable/disable CLI audit log.",
    "dh-params": "Number of bits to use in the Diffie-Hellman exchange for HTTPS/SSH protocols.",
    "fds-statistics": "Enable/disable sending IPS, Application Control, and AntiVirus data to FortiGuard. This data is used to improve FortiGuard services and is not shared with external parties and is protected by Fortinet's privacy policy.",
    "fds-statistics-period": "FortiGuard statistics collection period in minutes. (1 - 1440 min (1 min to 24 hours), default = 60).",
    "tcp-option": "Enable SACK, timestamp and MSS TCP options.",
    "lldp-transmission": "Enable/disable Link Layer Discovery Protocol (LLDP) transmission.",
    "lldp-reception": "Enable/disable Link Layer Discovery Protocol (LLDP) reception.",
    "proxy-auth-timeout": "Authentication timeout in minutes for authenticated users (1 - 10000 min, default = 10).",
    "proxy-keep-alive-mode": "Control if users must re-authenticate after a session is closed, traffic has been idle, or from the point at which the user was authenticated.",
    "proxy-re-authentication-time": "The time limit that users must re-authenticate if proxy-keep-alive-mode is set to re-authenticate (1  - 86400 sec, default=30s.",
    "proxy-auth-lifetime": "Enable/disable authenticated users lifetime control. This is a cap on the total time a proxy user can be authenticated for after which re-authentication will take place.",
    "proxy-auth-lifetime-timeout": "Lifetime timeout in minutes for authenticated users (5  - 65535 min, default=480 (8 hours)).",
    "proxy-resource-mode": "Enable/disable use of the maximum memory usage on the FortiGate unit's proxy processing of resources, such as block lists, allow lists, and external resources.",
    "proxy-cert-use-mgmt-vdom": "Enable/disable using management VDOM to send requests.",
    "sys-perf-log-interval": "Time in minutes between updates of performance statistics logging. (1 - 15 min, default = 5, 0 = disabled).",
    "check-protocol-header": "Level of checking performed on protocol headers. Strict checking is more thorough but may affect performance. Loose checking is OK in most cases.",
    "vip-arp-range": "Controls the number of ARPs that the FortiGate sends for a Virtual IP (VIP) address range.",
    "reset-sessionless-tcp": "Action to perform if the FortiGate receives a TCP packet but cannot find a corresponding session in its session table. NAT/Route mode only.",
    "allow-traffic-redirect": "Disable to prevent traffic with same local ingress and egress interface from being forwarded without policy check.",
    "ipv6-allow-traffic-redirect": "Disable to prevent IPv6 traffic with same local ingress and egress interface from being forwarded without policy check.",
    "strict-dirty-session-check": "Enable to check the session against the original policy when revalidating. This can prevent dropping of redirected sessions when web-filtering and authentication are enabled together. If this option is enabled, the FortiGate unit deletes a session if a routing or policy change causes the session to no longer match the policy that originally allowed the session.",
    "tcp-halfclose-timer": "Number of seconds the FortiGate unit should wait to close a session after one peer has sent a FIN packet but the other has not responded (1 - 86400 sec (1 day), default = 120).",
    "tcp-halfopen-timer": "Number of seconds the FortiGate unit should wait to close a session after one peer has sent an open session packet but the other has not responded (1 - 86400 sec (1 day), default = 10).",
    "tcp-timewait-timer": "Length of the TCP TIME-WAIT state in seconds (1 - 300 sec, default = 1).",
    "tcp-rst-timer": "Length of the TCP CLOSE state in seconds (5 - 300 sec, default = 5).",
    "udp-idle-timer": "UDP connection session timeout. This command can be useful in managing CPU and memory resources (1 - 86400 seconds (1 day), default = 60).",
    "block-session-timer": "Duration in seconds for blocked sessions (1 - 300 sec  (5 minutes), default = 30).",
    "ip-src-port-range": "IP source port range used for traffic originating from the FortiGate unit.",
    "pre-login-banner": "Enable/disable displaying the administrator access disclaimer message on the login page before an administrator logs in.",
    "post-login-banner": "Enable/disable displaying the administrator access disclaimer message after an administrator successfully logs in.",
    "tftp": "Enable/disable TFTP.",
    "av-failopen": "Set the action to take if the FortiGate is running low on memory or the proxy connection limit has been reached.",
    "av-failopen-session": "When enabled and a proxy for a protocol runs out of room in its session table, that protocol goes into failopen mode and enacts the action specified by av-failopen.",
    "memory-use-threshold-extreme": "Threshold at which memory usage is considered extreme (new sessions are dropped) (% of total RAM, default = 95).",
    "memory-use-threshold-red": "Threshold at which memory usage forces the FortiGate to enter conserve mode (% of total RAM, default = 88).",
    "memory-use-threshold-green": "Threshold at which memory usage forces the FortiGate to exit conserve mode (% of total RAM, default = 82).",
    "ip-fragment-mem-thresholds": "Maximum memory (MB) used to reassemble IPv4/IPv6 fragments.",
    "ip-fragment-timeout": "Timeout value in seconds for any fragment not being reassembled",
    "ipv6-fragment-timeout": "Timeout value in seconds for any IPv6 fragment not being reassembled",
    "cpu-use-threshold": "Threshold at which CPU usage is reported (% of total CPU, default = 90).",
    "log-single-cpu-high": "Enable/disable logging the event of a single CPU core reaching CPU usage threshold.",
    "check-reset-range": "Configure ICMP error message verification. You can either apply strict RST range checking or disable it.",
    "upgrade-report": "Enable/disable the generation of an upgrade report when upgrading the firmware.",
    "admin-port": "Administrative access port for HTTP. (1 - 65535, default = 80).",
    "admin-sport": "Administrative access port for HTTPS. (1 - 65535, default = 443).",
    "admin-host": "Administrative host for HTTP and HTTPS. When set, will be used in lieu of the client's Host header for any redirection.",
    "admin-https-redirect": "Enable/disable redirection of HTTP administration access to HTTPS.",
    "admin-hsts-max-age": "HTTPS Strict-Transport-Security header max-age in seconds. A value of 0 will reset any HSTS records in the browser.When admin-https-redirect is disabled the header max-age will be 0.",
    "admin-ssh-password": "Enable/disable password authentication for SSH admin access.",
    "admin-restrict-local": "Enable/disable local admin authentication restriction when remote authenticator is up and running (default = disable).",
    "admin-ssh-port": "Administrative access port for SSH. (1 - 65535, default = 22).",
    "admin-ssh-grace-time": "Maximum time in seconds permitted between making an SSH connection to the FortiGate unit and authenticating (10 - 3600 sec (1 hour), default 120).",
    "admin-ssh-v1": "Enable/disable SSH v1 compatibility.",
    "admin-telnet": "Enable/disable TELNET service.",
    "admin-telnet-port": "Administrative access port for TELNET. (1 - 65535, default = 23).",
    "admin-forticloud-sso-login": "Enable/disable FortiCloud admin login via SSO.",
    "admin-forticloud-sso-default-profile": "Override access profile.",
    "default-service-source-port": "Default service source port range (default = 1 - 65535).",
    "admin-server-cert": "Server certificate that the FortiGate uses for HTTPS administrative connections.",
    "admin-https-pki-required": "Enable/disable admin login method. Enable to force administrators to provide a valid certificate to log in if PKI is enabled. Disable to allow administrators to log in with a certificate or password.",
    "wifi-certificate": "Certificate to use for WiFi authentication.",
    "dhcp-lease-backup-interval": "DHCP leases backup interval in seconds (10 - 3600, default = 60).",
    "wifi-ca-certificate": "CA certificate that verifies the WiFi certificate.",
    "auth-http-port": "User authentication HTTP port. (1 - 65535, default = 1000).",
    "auth-https-port": "User authentication HTTPS port. (1 - 65535, default = 1003).",
    "auth-ike-saml-port": "User IKE SAML authentication port (0 - 65535, default = 1001).",
    "auth-keepalive": "Enable to prevent user authentication sessions from timing out when idle.",
    "policy-auth-concurrent": "Number of concurrent firewall use logins from the same user (1 - 100, default = 0 means no limit).",
    "auth-session-limit": "Action to take when the number of allowed user authenticated sessions is reached.",
    "auth-cert": "Server certificate that the FortiGate uses for HTTPS firewall authentication connections.",
    "clt-cert-req": "Enable/disable requiring administrators to have a client certificate to log into the GUI using HTTPS.",
    "fortiservice-port": "FortiService port (1 - 65535, default = 8013). Used by FortiClient endpoint compliance. Older versions of FortiClient used a different port.",
    "cfg-save": "Configuration file save mode for CLI changes.",
    "cfg-revert-timeout": "Time-out for reverting to the last saved configuration. (10 - 4294967295 seconds, default = 600).",
    "reboot-upon-config-restore": "Enable/disable reboot of system upon restoring configuration.",
    "admin-scp": "Enable/disable SCP support for system configuration backup, restore, and firmware file upload.",
    "wireless-controller": "Enable/disable the wireless controller feature to use the FortiGate unit to manage FortiAPs.",
    "wireless-controller-port": "Port used for the control channel in wireless controller mode (wireless-mode is ac). The data channel port is the control channel port number plus one (1024 - 49150, default = 5246).",
    "fortiextender-data-port": "FortiExtender data port (1024 - 49150, default = 25246).",
    "fortiextender": "Enable/disable FortiExtender.",
    "extender-controller-reserved-network": "Configure reserved network subnet for managed LAN extension FortiExtender units. This is available when the FortiExtender daemon is running.",
    "fortiextender-discovery-lockdown": "Enable/disable FortiExtender CAPWAP lockdown.",
    "fortiextender-vlan-mode": "Enable/disable FortiExtender VLAN mode.",
    "fortiextender-provision-on-authorization": "Enable/disable automatic provisioning of latest FortiExtender firmware on authorization.",
    "switch-controller": "Enable/disable switch controller feature. Switch controller allows you to manage FortiSwitch from the FortiGate itself.",
    "switch-controller-reserved-network": "Configure reserved network subnet for managed switches. This is available when the switch controller is enabled.",
    "dnsproxy-worker-count": "DNS proxy worker count. For a FortiGate with multiple logical CPUs, you can set the DNS process number from 1 to the number of logical CPUs.",
    "url-filter-count": "URL filter daemon count.",
    "httpd-max-worker-count": "Maximum number of simultaneous HTTP requests that will be served. This number may affect GUI and REST API performance (0 - 128, default = 0 means let system decide).",
    "proxy-worker-count": "Proxy worker count.",
    "scanunit-count": "Number of scanunits. The range and the default depend on the number of CPUs. Only available on FortiGate units with multiple CPUs.",
    "fgd-alert-subscription": "Type of alert to retrieve from FortiGuard.",
    "ipv6-accept-dad": "Enable/disable acceptance of IPv6 Duplicate Address Detection (DAD).",
    "ipv6-allow-anycast-probe": "Enable/disable IPv6 address probe through Anycast.",
    "ipv6-allow-multicast-probe": "Enable/disable IPv6 address probe through Multicast.",
    "ipv6-allow-local-in-silent-drop": "Enable/disable silent drop of IPv6 local-in traffic.",
    "csr-ca-attribute": "Enable/disable the CA attribute in certificates. Some CA servers reject CSRs that have the CA attribute.",
    "wimax-4g-usb": "Enable/disable comparability with WiMAX 4G USB devices.",
    "cert-chain-max": "Maximum number of certificates that can be traversed in a certificate chain.",
    "sslvpn-max-worker-count": "Maximum number of Agentless VPN processes. Upper limit for this value is the number of CPUs and depends on the model. Default value of zero means the sslvpnd daemon decides the number of worker processes.",
    "sslvpn-affinity": "Agentless VPN CPU affinity.",
    "sslvpn-web-mode": "Enable/disable Agentless VPN web mode.",
    "two-factor-ftk-expiry": "FortiToken authentication session timeout (60 - 600 sec (10 minutes), default = 60).",
    "two-factor-email-expiry": "Email-based two-factor authentication session timeout (30 - 300 seconds (5 minutes), default = 60).",
    "two-factor-sms-expiry": "SMS-based two-factor authentication session timeout (30 - 300 sec, default = 60).",
    "two-factor-fac-expiry": "FortiAuthenticator token authentication session timeout (10 - 3600 seconds (1 hour), default = 60).",
    "two-factor-ftm-expiry": "FortiToken Mobile session timeout (1 - 168 hours (7 days), default = 72).",
    "per-user-bal": "Enable/disable per-user block/allow list filter.",
    "wad-worker-count": "Number of explicit proxy WAN optimization daemon (WAD) processes. By default WAN optimization, explicit proxy, and web caching is handled by all of the CPU cores in a FortiGate unit.",
    "wad-worker-dev-cache": "Number of cached devices for each ZTNA proxy worker. The default value is tuned by memory consumption. Set the option to 0 to disable the cache.",
    "wad-csvc-cs-count": "Number of concurrent WAD-cache-service object-cache processes.",
    "wad-csvc-db-count": "Number of concurrent WAD-cache-service byte-cache processes.",
    "wad-source-affinity": "Enable/disable dispatching traffic to WAD workers based on source affinity.",
    "wad-memory-change-granularity": "Minimum percentage change in system memory usage detected by the wad daemon prior to adjusting TCP window size for any active connection.",
    "login-timestamp": "Enable/disable login time recording.",
    "ip-conflict-detection": "Enable/disable logging of IPv4 address conflict detection.",
    "miglogd-children": "Number of logging (miglogd) processes to be allowed to run. Higher number can reduce performance; lower number can slow log processing time. ",
    "log-daemon-cpu-threshold": "Configure syslog daemon process spawning threshold. Use a percentage threshold of syslogd CPU usage (1 - 99) or set to zero to use dynamic scheduling based on the number of packets in the syslogd queue (default = 0).",
    "special-file-23-support": "Enable/disable detection of those special format files when using Data Loss Prevention.",
    "log-uuid-address": "Enable/disable insertion of address UUIDs to traffic logs.",
    "log-ssl-connection": "Enable/disable logging of SSL connection events.",
    "gui-rest-api-cache": "Enable/disable REST API result caching on FortiGate.",
    "rest-api-key-url-query": "Enable/disable support for passing REST API keys through URL query parameters.",
    "arp-max-entry": "Maximum number of dynamically learned MAC addresses that can be added to the ARP table (131072 - 2147483647, default = 131072).",
    "ha-affinity": "Affinity setting for HA daemons (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "bfd-affinity": "Affinity setting for BFD daemon (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "cmdbsvr-affinity": "Affinity setting for cmdbsvr (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "av-affinity": "Affinity setting for AV scanning (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "wad-affinity": "Affinity setting for wad (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "ips-affinity": "Affinity setting for IPS (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx; allowed CPUs must be less than total number of IPS engine daemons).",
    "miglog-affinity": "Affinity setting for logging (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "syslog-affinity": "Affinity setting for syslog (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "url-filter-affinity": "URL filter CPU affinity.",
    "router-affinity": "Affinity setting for BFD/VRRP/BGP/OSPF daemons (hexadecimal value up to 256 bits in the format of xxxxxxxxxxxxxxxx).",
    "ndp-max-entry": "Maximum number of NDP table entries (set to 65,536 or higher; if set to 0, kernel holds 65,536 entries).",
    "br-fdb-max-entry": "Maximum number of bridge forwarding database (FDB) entries.",
    "max-route-cache-size": "Maximum number of IP route cache entries (0 - 2147483647).",
    "ipsec-qat-offload": "Enable/disable QAT offloading (Intel QuickAssist) for IPsec VPN traffic. QuickAssist can accelerate IPsec encryption and decryption.",
    "device-idle-timeout": "Time in seconds that a device must be idle to automatically log the device user out. (30 - 31536000 sec (30 sec to 1 year), default = 300).",
    "user-device-store-max-devices": "Maximum number of devices allowed in user device store.",
    "user-device-store-max-device-mem": "Maximum percentage of total system memory allowed to be used for devices in the user device store.",
    "user-device-store-max-users": "Maximum number of users allowed in user device store.",
    "user-device-store-max-unified-mem": "Maximum unified memory allowed in user device store.",
    "gui-device-latitude": "Add the latitude of the location of this FortiGate to position it on the Threat Map.",
    "gui-device-longitude": "Add the longitude of the location of this FortiGate to position it on the Threat Map.",
    "private-data-encryption": "Enable/disable private data encryption using an AES 128-bit key or passpharse.",
    "auto-auth-extension-device": "Enable/disable automatic authorization of dedicated Fortinet extension devices.",
    "gui-theme": "Color scheme for the administration GUI.",
    "gui-date-format": "Default date format used throughout GUI.",
    "gui-date-time-source": "Source from which the FortiGate GUI uses to display date and time entries.",
    "igmp-state-limit": "Maximum number of IGMP memberships (96 - 64000, default = 3200).",
    "cloud-communication": "Enable/disable all cloud communication.",
    "ipsec-ha-seqjump-rate": "ESP jump ahead rate (1G - 10G pps equivalent).",
    "fortitoken-cloud": "Enable/disable FortiToken Cloud service.",
    "fortitoken-cloud-push-status": "Enable/disable FTM push service of FortiToken Cloud.",
    "fortitoken-cloud-region": "Region domain of FortiToken Cloud(unset to non-region).",
    "fortitoken-cloud-sync-interval": "Interval in which to clean up remote users in FortiToken Cloud (0 - 336 hours (14 days), default = 24, disable = 0).",
    "faz-disk-buffer-size": "Maximum disk buffer size to temporarily store logs destined for FortiAnalyzer. To be used in the event that FortiAnalyzer is unavailable.",
    "irq-time-accounting": "Configure CPU IRQ time accounting mode.",
    "management-ip": "Management IP address of this FortiGate. Used to log into this FortiGate from another FortiGate in the Security Fabric.",
    "management-port": "Overriding port for management connection (Overrides admin port).",
    "management-port-use-admin-sport": "Enable/disable use of the admin-sport setting for the management port. If disabled, FortiGate will allow user to specify management-port.",
    "forticonverter-integration": "Enable/disable FortiConverter integration service.",
    "forticonverter-config-upload": "Enable/disable config upload to FortiConverter.",
    "internet-service-database": "Configure which Internet Service database size to download from FortiGuard and use.",
    "internet-service-download-list": "Configure which on-demand Internet Service IDs are to be downloaded.",
    "geoip-full-db": "When enabled, the full geographic database will be loaded into the kernel which enables geographic information in traffic logs - required for FortiView countries. Disabling this option will conserve memory.",
    "early-tcp-npu-session": "Enable/disable early TCP NPU session.",
    "npu-neighbor-update": "Enable/disable sending of ARP/ICMP6 probing packets to update neighbors for offloaded sessions.",
    "delay-tcp-npu-session": "Enable TCP NPU session delay to guarantee packet order of 3-way handshake.",
    "interface-subnet-usage": "Enable/disable allowing use of interface-subnet setting in firewall addresses (default = enable).",
    "sflowd-max-children-num": "Maximum number of sflowd child processes allowed to run.",
    "fortigslb-integration": "Enable/disable integration with the FortiGSLB cloud service.",
    "user-history-password-threshold": "Maximum number of previous passwords saved per admin/user (3 - 15, default = 3).",
    "auth-session-auto-backup": "Enable/disable automatic and periodic backup of authentication sessions (default = disable). Sessions are restored upon bootup.",
    "auth-session-auto-backup-interval": "Configure automatic authentication session backup interval (default = 15min).",
    "scim-https-port": "SCIM port (0 - 65535, default = 44559).",
    "scim-http-port": "SCIM http port (0 - 65535, default = 44558).",
    "scim-server-cert": "Server certificate that the FortiGate uses for SCIM connections.",
    "application-bandwidth-tracking": "Enable/disable application bandwidth tracking.",
    "tls-session-cache": "Enable/disable TLS session cache.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "admintimeout": {"type": "integer", "min": 1, "max": 480},
    "admin-console-timeout": {"type": "integer", "min": 15, "max": 300},
    "ssd-trim-hour": {"type": "integer", "min": 0, "max": 23},
    "ssd-trim-min": {"type": "integer", "min": 0, "max": 60},
    "ssd-trim-date": {"type": "integer", "min": 1, "max": 31},
    "admin-lockout-threshold": {"type": "integer", "min": 1, "max": 10},
    "admin-lockout-duration": {"type": "integer", "min": 1, "max": 2147483647},
    "refresh": {"type": "integer", "min": 0, "max": 4294967295},
    "interval": {"type": "integer", "min": 0, "max": 4294967295},
    "failtime": {"type": "integer", "min": 0, "max": 4294967295},
    "wad-p2s-max-body-size": {"type": "integer", "min": 1, "max": 32},
    "radius-port": {"type": "integer", "min": 1, "max": 65535},
    "speedtestd-server-port": {"type": "integer", "min": 1, "max": 65535},
    "speedtestd-ctrl-port": {"type": "integer", "min": 1, "max": 65535},
    "admin-login-max": {"type": "integer", "min": 1, "max": 100},
    "remoteauthtimeout": {"type": "integer", "min": 1, "max": 300},
    "ldapconntimeout": {"type": "integer", "min": 1, "max": 300000},
    "timezone": {"type": "string", "max_length": 63},
    "quic-max-datagram-size": {"type": "integer", "min": 1200, "max": 1500},
    "quic-ack-thresold": {"type": "integer", "min": 2, "max": 5},
    "quic-tls-handshake-timeout": {"type": "integer", "min": 1, "max": 60},
    "management-vdom": {"type": "string", "max_length": 31},
    "hostname": {"type": "string", "max_length": 35},
    "alias": {"type": "string", "max_length": 35},
    "fds-statistics-period": {"type": "integer", "min": 1, "max": 1440},
    "proxy-auth-timeout": {"type": "integer", "min": 1, "max": 10000},
    "proxy-re-authentication-time": {"type": "integer", "min": 1, "max": 86400},
    "proxy-auth-lifetime-timeout": {"type": "integer", "min": 5, "max": 65535},
    "sys-perf-log-interval": {"type": "integer", "min": 0, "max": 15},
    "tcp-halfclose-timer": {"type": "integer", "min": 1, "max": 86400},
    "tcp-halfopen-timer": {"type": "integer", "min": 1, "max": 86400},
    "tcp-timewait-timer": {"type": "integer", "min": 0, "max": 300},
    "tcp-rst-timer": {"type": "integer", "min": 5, "max": 300},
    "udp-idle-timer": {"type": "integer", "min": 1, "max": 86400},
    "block-session-timer": {"type": "integer", "min": 1, "max": 300},
    "memory-use-threshold-extreme": {"type": "integer", "min": 70, "max": 97},
    "memory-use-threshold-red": {"type": "integer", "min": 70, "max": 97},
    "memory-use-threshold-green": {"type": "integer", "min": 70, "max": 97},
    "ip-fragment-mem-thresholds": {"type": "integer", "min": 32, "max": 2047},
    "ip-fragment-timeout": {"type": "integer", "min": 3, "max": 30},
    "ipv6-fragment-timeout": {"type": "integer", "min": 5, "max": 60},
    "cpu-use-threshold": {"type": "integer", "min": 50, "max": 99},
    "admin-port": {"type": "integer", "min": 1, "max": 65535},
    "admin-sport": {"type": "integer", "min": 1, "max": 65535},
    "admin-host": {"type": "string", "max_length": 255},
    "admin-hsts-max-age": {"type": "integer", "min": 0, "max": 2147483647},
    "admin-ssh-port": {"type": "integer", "min": 1, "max": 65535},
    "admin-ssh-grace-time": {"type": "integer", "min": 10, "max": 3600},
    "admin-telnet-port": {"type": "integer", "min": 1, "max": 65535},
    "admin-forticloud-sso-default-profile": {"type": "string", "max_length": 35},
    "admin-server-cert": {"type": "string", "max_length": 35},
    "wifi-certificate": {"type": "string", "max_length": 35},
    "dhcp-lease-backup-interval": {"type": "integer", "min": 10, "max": 3600},
    "wifi-ca-certificate": {"type": "string", "max_length": 79},
    "auth-http-port": {"type": "integer", "min": 1, "max": 65535},
    "auth-https-port": {"type": "integer", "min": 1, "max": 65535},
    "auth-ike-saml-port": {"type": "integer", "min": 0, "max": 65535},
    "policy-auth-concurrent": {"type": "integer", "min": 0, "max": 100},
    "auth-cert": {"type": "string", "max_length": 35},
    "fortiservice-port": {"type": "integer", "min": 1, "max": 65535},
    "cfg-revert-timeout": {"type": "integer", "min": 10, "max": 4294967295},
    "wireless-controller-port": {"type": "integer", "min": 1024, "max": 49150},
    "fortiextender-data-port": {"type": "integer", "min": 1024, "max": 49150},
    "dnsproxy-worker-count": {"type": "integer", "min": 1, "max": 2},
    "url-filter-count": {"type": "integer", "min": 1, "max": 1},
    "httpd-max-worker-count": {"type": "integer", "min": 0, "max": 128},
    "proxy-worker-count": {"type": "integer", "min": 1, "max": 2},
    "scanunit-count": {"type": "integer", "min": 2, "max": 2},
    "ipv6-accept-dad": {"type": "integer", "min": 0, "max": 2},
    "cert-chain-max": {"type": "integer", "min": 1, "max": 2147483647},
    "sslvpn-max-worker-count": {"type": "integer", "min": 0, "max": 1},
    "sslvpn-affinity": {"type": "string", "max_length": 79},
    "two-factor-ftk-expiry": {"type": "integer", "min": 60, "max": 600},
    "two-factor-email-expiry": {"type": "integer", "min": 30, "max": 300},
    "two-factor-sms-expiry": {"type": "integer", "min": 30, "max": 300},
    "two-factor-fac-expiry": {"type": "integer", "min": 10, "max": 3600},
    "two-factor-ftm-expiry": {"type": "integer", "min": 1, "max": 168},
    "wad-worker-count": {"type": "integer", "min": 0, "max": 2},
    "wad-worker-dev-cache": {"type": "integer", "min": 0, "max": 10240},
    "wad-csvc-cs-count": {"type": "integer", "min": 1, "max": 1},
    "wad-csvc-db-count": {"type": "integer", "min": 0, "max": 2},
    "wad-memory-change-granularity": {"type": "integer", "min": 5, "max": 25},
    "miglogd-children": {"type": "integer", "min": 0, "max": 15},
    "log-daemon-cpu-threshold": {"type": "integer", "min": 0, "max": 99},
    "arp-max-entry": {"type": "integer", "min": 131072, "max": 2147483647},
    "ha-affinity": {"type": "string", "max_length": 79},
    "bfd-affinity": {"type": "string", "max_length": 79},
    "cmdbsvr-affinity": {"type": "string", "max_length": 79},
    "av-affinity": {"type": "string", "max_length": 79},
    "wad-affinity": {"type": "string", "max_length": 79},
    "ips-affinity": {"type": "string", "max_length": 79},
    "miglog-affinity": {"type": "string", "max_length": 79},
    "syslog-affinity": {"type": "string", "max_length": 79},
    "url-filter-affinity": {"type": "string", "max_length": 79},
    "router-affinity": {"type": "string", "max_length": 79},
    "ndp-max-entry": {"type": "integer", "min": 65536, "max": 2147483647},
    "br-fdb-max-entry": {"type": "integer", "min": 8192, "max": 2147483647},
    "max-route-cache-size": {"type": "integer", "min": 0, "max": 2147483647},
    "device-idle-timeout": {"type": "integer", "min": 30, "max": 31536000},
    "user-device-store-max-devices": {"type": "integer", "min": 31262, "max": 89320},
    "user-device-store-max-device-mem": {"type": "integer", "min": 1, "max": 5},
    "user-device-store-max-users": {"type": "integer", "min": 31262, "max": 89320},
    "user-device-store-max-unified-mem": {"type": "integer", "min": 62524334, "max": 625243340},
    "gui-device-latitude": {"type": "string", "max_length": 19},
    "gui-device-longitude": {"type": "string", "max_length": 19},
    "igmp-state-limit": {"type": "integer", "min": 96, "max": 128000},
    "ipsec-ha-seqjump-rate": {"type": "integer", "min": 1, "max": 10},
    "fortitoken-cloud-region": {"type": "string", "max_length": 63},
    "fortitoken-cloud-sync-interval": {"type": "integer", "min": 0, "max": 336},
    "management-ip": {"type": "string", "max_length": 255},
    "management-port": {"type": "integer", "min": 1, "max": 65535},
    "sflowd-max-children-num": {"type": "integer", "min": 0, "max": 1},
    "user-history-password-threshold": {"type": "integer", "min": 3, "max": 15},
    "scim-https-port": {"type": "integer", "min": 0, "max": 65535},
    "scim-http-port": {"type": "integer", "min": 0, "max": 65535},
    "scim-server-cert": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "internet-service-download-list": {
        "id": {
            "type": "integer",
            "help": "Internet Service ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_LANGUAGE = [
    "english",
    "french",
    "spanish",
    "portuguese",
    "japanese",
    "trach",
    "simch",
    "korean",
]
VALID_BODY_GUI_IPV6 = [
    "enable",
    "disable",
]
VALID_BODY_GUI_REPLACEMENT_MESSAGE_GROUPS = [
    "enable",
    "disable",
]
VALID_BODY_GUI_LOCAL_OUT = [
    "enable",
    "disable",
]
VALID_BODY_GUI_CERTIFICATES = [
    "enable",
    "disable",
]
VALID_BODY_GUI_CUSTOM_LANGUAGE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WIRELESS_OPENSECURITY = [
    "enable",
    "disable",
]
VALID_BODY_GUI_APP_DETECTION_SDWAN = [
    "enable",
    "disable",
]
VALID_BODY_GUI_DISPLAY_HOSTNAME = [
    "enable",
    "disable",
]
VALID_BODY_GUI_FORTIGATE_CLOUD_SANDBOX = [
    "enable",
    "disable",
]
VALID_BODY_GUI_FIRMWARE_UPGRADE_WARNING = [
    "enable",
    "disable",
]
VALID_BODY_GUI_FORTICARE_REGISTRATION_SETUP_WARNING = [
    "enable",
    "disable",
]
VALID_BODY_GUI_AUTO_UPGRADE_SETUP_WARNING = [
    "enable",
    "disable",
]
VALID_BODY_GUI_WORKFLOW_MANAGEMENT = [
    "enable",
    "disable",
]
VALID_BODY_GUI_CDN_USAGE = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_HTTPS_SSL_VERSIONS = [
    "tlsv1-1",
    "tlsv1-2",
    "tlsv1-3",
]
VALID_BODY_ADMIN_HTTPS_SSL_CIPHERSUITES = [
    "TLS-AES-128-GCM-SHA256",
    "TLS-AES-256-GCM-SHA384",
    "TLS-CHACHA20-POLY1305-SHA256",
    "TLS-AES-128-CCM-SHA256",
    "TLS-AES-128-CCM-8-SHA256",
]
VALID_BODY_ADMIN_HTTPS_SSL_BANNED_CIPHERS = [
    "RSA",
    "DHE",
    "ECDHE",
    "DSS",
    "ECDSA",
    "AES",
    "AESGCM",
    "CAMELLIA",
    "3DES",
    "SHA1",
    "SHA256",
    "SHA384",
    "STATIC",
    "CHACHA20",
    "ARIA",
    "AESCCM",
]
VALID_BODY_SSD_TRIM_FREQ = [
    "never",
    "hourly",
    "daily",
    "weekly",
    "monthly",
]
VALID_BODY_SSD_TRIM_WEEKDAY = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]
VALID_BODY_ADMIN_CONCURRENT = [
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
VALID_BODY_DAILY_RESTART = [
    "enable",
    "disable",
]
VALID_BODY_WAD_RESTART_MODE = [
    "none",
    "time",
    "memory",
]
VALID_BODY_BATCH_CMDB = [
    "enable",
    "disable",
]
VALID_BODY_MULTI_FACTOR_AUTHENTICATION = [
    "optional",
    "mandatory",
]
VALID_BODY_SSL_MIN_PROTO_VERSION = [
    "SSLv3",
    "TLSv1",
    "TLSv1-1",
    "TLSv1-2",
    "TLSv1-3",
]
VALID_BODY_AUTORUN_LOG_FSCK = [
    "enable",
    "disable",
]
VALID_BODY_TRAFFIC_PRIORITY = [
    "tos",
    "dscp",
]
VALID_BODY_TRAFFIC_PRIORITY_LEVEL = [
    "low",
    "medium",
    "high",
]
VALID_BODY_QUIC_CONGESTION_CONTROL_ALGO = [
    "cubic",
    "bbr",
    "bbr2",
    "reno",
]
VALID_BODY_QUIC_UDP_PAYLOAD_SIZE_SHAPING_PER_CID = [
    "enable",
    "disable",
]
VALID_BODY_QUIC_PMTUD = [
    "enable",
    "disable",
]
VALID_BODY_ANTI_REPLAY = [
    "disable",
    "loose",
    "strict",
]
VALID_BODY_SEND_PMTU_ICMP = [
    "enable",
    "disable",
]
VALID_BODY_HONOR_DF = [
    "enable",
    "disable",
]
VALID_BODY_PMTU_DISCOVERY = [
    "enable",
    "disable",
]
VALID_BODY_REVISION_IMAGE_AUTO_BACKUP = [
    "enable",
    "disable",
]
VALID_BODY_REVISION_BACKUP_ON_LOGOUT = [
    "enable",
    "disable",
]
VALID_BODY_STRONG_CRYPTO = [
    "enable",
    "disable",
]
VALID_BODY_SSL_STATIC_KEY_CIPHERS = [
    "enable",
    "disable",
]
VALID_BODY_SNAT_ROUTE_CHANGE = [
    "enable",
    "disable",
]
VALID_BODY_IPV6_SNAT_ROUTE_CHANGE = [
    "enable",
    "disable",
]
VALID_BODY_SPEEDTEST_SERVER = [
    "enable",
    "disable",
]
VALID_BODY_CLI_AUDIT_LOG = [
    "enable",
    "disable",
]
VALID_BODY_DH_PARAMS = [
    "1024",
    "1536",
    "2048",
    "3072",
    "4096",
    "6144",
    "8192",
]
VALID_BODY_FDS_STATISTICS = [
    "enable",
    "disable",
]
VALID_BODY_TCP_OPTION = [
    "enable",
    "disable",
]
VALID_BODY_LLDP_TRANSMISSION = [
    "enable",
    "disable",
]
VALID_BODY_LLDP_RECEPTION = [
    "enable",
    "disable",
]
VALID_BODY_PROXY_KEEP_ALIVE_MODE = [
    "session",
    "traffic",
    "re-authentication",
]
VALID_BODY_PROXY_AUTH_LIFETIME = [
    "enable",
    "disable",
]
VALID_BODY_PROXY_RESOURCE_MODE = [
    "enable",
    "disable",
]
VALID_BODY_PROXY_CERT_USE_MGMT_VDOM = [
    "enable",
    "disable",
]
VALID_BODY_CHECK_PROTOCOL_HEADER = [
    "loose",
    "strict",
]
VALID_BODY_VIP_ARP_RANGE = [
    "unlimited",
    "restricted",
]
VALID_BODY_RESET_SESSIONLESS_TCP = [
    "enable",
    "disable",
]
VALID_BODY_ALLOW_TRAFFIC_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_IPV6_ALLOW_TRAFFIC_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_STRICT_DIRTY_SESSION_CHECK = [
    "enable",
    "disable",
]
VALID_BODY_PRE_LOGIN_BANNER = [
    "enable",
    "disable",
]
VALID_BODY_POST_LOGIN_BANNER = [
    "disable",
    "enable",
]
VALID_BODY_TFTP = [
    "enable",
    "disable",
]
VALID_BODY_AV_FAILOPEN = [
    "pass",
    "off",
    "one-shot",
]
VALID_BODY_AV_FAILOPEN_SESSION = [
    "enable",
    "disable",
]
VALID_BODY_LOG_SINGLE_CPU_HIGH = [
    "enable",
    "disable",
]
VALID_BODY_CHECK_RESET_RANGE = [
    "strict",
    "disable",
]
VALID_BODY_UPGRADE_REPORT = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_HTTPS_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_SSH_PASSWORD = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_RESTRICT_LOCAL = [
    "all",
    "non-console-only",
    "disable",
]
VALID_BODY_ADMIN_SSH_V1 = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_TELNET = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_FORTICLOUD_SSO_LOGIN = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_HTTPS_PKI_REQUIRED = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_KEEPALIVE = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_SESSION_LIMIT = [
    "block-new",
    "logout-inactive",
]
VALID_BODY_CLT_CERT_REQ = [
    "enable",
    "disable",
]
VALID_BODY_CFG_SAVE = [
    "automatic",
    "manual",
    "revert",
]
VALID_BODY_REBOOT_UPON_CONFIG_RESTORE = [
    "enable",
    "disable",
]
VALID_BODY_ADMIN_SCP = [
    "enable",
    "disable",
]
VALID_BODY_WIRELESS_CONTROLLER = [
    "enable",
    "disable",
]
VALID_BODY_FORTIEXTENDER = [
    "disable",
    "enable",
]
VALID_BODY_FORTIEXTENDER_DISCOVERY_LOCKDOWN = [
    "disable",
    "enable",
]
VALID_BODY_FORTIEXTENDER_VLAN_MODE = [
    "enable",
    "disable",
]
VALID_BODY_FORTIEXTENDER_PROVISION_ON_AUTHORIZATION = [
    "enable",
    "disable",
]
VALID_BODY_SWITCH_CONTROLLER = [
    "disable",
    "enable",
]
VALID_BODY_FGD_ALERT_SUBSCRIPTION = [
    "advisory",
    "latest-threat",
    "latest-virus",
    "latest-attack",
    "new-antivirus-db",
    "new-attack-db",
]
VALID_BODY_IPV6_ALLOW_ANYCAST_PROBE = [
    "enable",
    "disable",
]
VALID_BODY_IPV6_ALLOW_MULTICAST_PROBE = [
    "enable",
    "disable",
]
VALID_BODY_IPV6_ALLOW_LOCAL_IN_SILENT_DROP = [
    "enable",
    "disable",
]
VALID_BODY_CSR_CA_ATTRIBUTE = [
    "enable",
    "disable",
]
VALID_BODY_WIMAX_4G_USB = [
    "enable",
    "disable",
]
VALID_BODY_SSLVPN_WEB_MODE = [
    "enable",
    "disable",
]
VALID_BODY_PER_USER_BAL = [
    "enable",
    "disable",
]
VALID_BODY_WAD_SOURCE_AFFINITY = [
    "disable",
    "enable",
]
VALID_BODY_LOGIN_TIMESTAMP = [
    "enable",
    "disable",
]
VALID_BODY_IP_CONFLICT_DETECTION = [
    "enable",
    "disable",
]
VALID_BODY_SPECIAL_FILE_23_SUPPORT = [
    "disable",
    "enable",
]
VALID_BODY_LOG_UUID_ADDRESS = [
    "enable",
    "disable",
]
VALID_BODY_LOG_SSL_CONNECTION = [
    "enable",
    "disable",
]
VALID_BODY_GUI_REST_API_CACHE = [
    "enable",
    "disable",
]
VALID_BODY_REST_API_KEY_URL_QUERY = [
    "enable",
    "disable",
]
VALID_BODY_IPSEC_QAT_OFFLOAD = [
    "enable",
    "disable",
]
VALID_BODY_PRIVATE_DATA_ENCRYPTION = [
    "disable",
    "enable",
]
VALID_BODY_AUTO_AUTH_EXTENSION_DEVICE = [
    "enable",
    "disable",
]
VALID_BODY_GUI_THEME = [
    "jade",
    "neutrino",
    "mariner",
    "graphite",
    "melongene",
    "jet-stream",
    "security-fabric",
    "retro",
    "dark-matter",
    "onyx",
    "eclipse",
]
VALID_BODY_GUI_DATE_FORMAT = [
    "yyyy/MM/dd",
    "dd/MM/yyyy",
    "MM/dd/yyyy",
    "yyyy-MM-dd",
    "dd-MM-yyyy",
    "MM-dd-yyyy",
]
VALID_BODY_GUI_DATE_TIME_SOURCE = [
    "system",
    "browser",
]
VALID_BODY_CLOUD_COMMUNICATION = [
    "enable",
    "disable",
]
VALID_BODY_FORTITOKEN_CLOUD = [
    "enable",
    "disable",
]
VALID_BODY_FORTITOKEN_CLOUD_PUSH_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_IRQ_TIME_ACCOUNTING = [
    "auto",
    "force",
]
VALID_BODY_MANAGEMENT_PORT_USE_ADMIN_SPORT = [
    "enable",
    "disable",
]
VALID_BODY_FORTICONVERTER_INTEGRATION = [
    "enable",
    "disable",
]
VALID_BODY_FORTICONVERTER_CONFIG_UPLOAD = [
    "once",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_DATABASE = [
    "mini",
    "standard",
    "full",
    "on-demand",
]
VALID_BODY_GEOIP_FULL_DB = [
    "enable",
    "disable",
]
VALID_BODY_EARLY_TCP_NPU_SESSION = [
    "enable",
    "disable",
]
VALID_BODY_NPU_NEIGHBOR_UPDATE = [
    "enable",
    "disable",
]
VALID_BODY_DELAY_TCP_NPU_SESSION = [
    "enable",
    "disable",
]
VALID_BODY_INTERFACE_SUBNET_USAGE = [
    "disable",
    "enable",
]
VALID_BODY_FORTIGSLB_INTEGRATION = [
    "disable",
    "enable",
]
VALID_BODY_AUTH_SESSION_AUTO_BACKUP = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_SESSION_AUTO_BACKUP_INTERVAL = [
    "1min",
    "5min",
    "15min",
    "30min",
    "1hr",
]
VALID_BODY_APPLICATION_BANDWIDTH_TRACKING = [
    "disable",
    "enable",
]
VALID_BODY_TLS_SESSION_CACHE = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_global_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/global_."""
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


def validate_system_global_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/global_ object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "language" in payload:
        is_valid, error = _validate_enum_field(
            "language",
            payload["language"],
            VALID_BODY_LANGUAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ipv6" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ipv6",
            payload["gui-ipv6"],
            VALID_BODY_GUI_IPV6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-replacement-message-groups" in payload:
        is_valid, error = _validate_enum_field(
            "gui-replacement-message-groups",
            payload["gui-replacement-message-groups"],
            VALID_BODY_GUI_REPLACEMENT_MESSAGE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-local-out" in payload:
        is_valid, error = _validate_enum_field(
            "gui-local-out",
            payload["gui-local-out"],
            VALID_BODY_GUI_LOCAL_OUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-certificates" in payload:
        is_valid, error = _validate_enum_field(
            "gui-certificates",
            payload["gui-certificates"],
            VALID_BODY_GUI_CERTIFICATES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-custom-language" in payload:
        is_valid, error = _validate_enum_field(
            "gui-custom-language",
            payload["gui-custom-language"],
            VALID_BODY_GUI_CUSTOM_LANGUAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wireless-opensecurity" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wireless-opensecurity",
            payload["gui-wireless-opensecurity"],
            VALID_BODY_GUI_WIRELESS_OPENSECURITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-app-detection-sdwan" in payload:
        is_valid, error = _validate_enum_field(
            "gui-app-detection-sdwan",
            payload["gui-app-detection-sdwan"],
            VALID_BODY_GUI_APP_DETECTION_SDWAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-display-hostname" in payload:
        is_valid, error = _validate_enum_field(
            "gui-display-hostname",
            payload["gui-display-hostname"],
            VALID_BODY_GUI_DISPLAY_HOSTNAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-fortigate-cloud-sandbox" in payload:
        is_valid, error = _validate_enum_field(
            "gui-fortigate-cloud-sandbox",
            payload["gui-fortigate-cloud-sandbox"],
            VALID_BODY_GUI_FORTIGATE_CLOUD_SANDBOX,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-firmware-upgrade-warning" in payload:
        is_valid, error = _validate_enum_field(
            "gui-firmware-upgrade-warning",
            payload["gui-firmware-upgrade-warning"],
            VALID_BODY_GUI_FIRMWARE_UPGRADE_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-forticare-registration-setup-warning" in payload:
        is_valid, error = _validate_enum_field(
            "gui-forticare-registration-setup-warning",
            payload["gui-forticare-registration-setup-warning"],
            VALID_BODY_GUI_FORTICARE_REGISTRATION_SETUP_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-auto-upgrade-setup-warning" in payload:
        is_valid, error = _validate_enum_field(
            "gui-auto-upgrade-setup-warning",
            payload["gui-auto-upgrade-setup-warning"],
            VALID_BODY_GUI_AUTO_UPGRADE_SETUP_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-workflow-management" in payload:
        is_valid, error = _validate_enum_field(
            "gui-workflow-management",
            payload["gui-workflow-management"],
            VALID_BODY_GUI_WORKFLOW_MANAGEMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-cdn-usage" in payload:
        is_valid, error = _validate_enum_field(
            "gui-cdn-usage",
            payload["gui-cdn-usage"],
            VALID_BODY_GUI_CDN_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-ssl-versions" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-ssl-versions",
            payload["admin-https-ssl-versions"],
            VALID_BODY_ADMIN_HTTPS_SSL_VERSIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-ssl-ciphersuites" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-ssl-ciphersuites",
            payload["admin-https-ssl-ciphersuites"],
            VALID_BODY_ADMIN_HTTPS_SSL_CIPHERSUITES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-ssl-banned-ciphers" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-ssl-banned-ciphers",
            payload["admin-https-ssl-banned-ciphers"],
            VALID_BODY_ADMIN_HTTPS_SSL_BANNED_CIPHERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssd-trim-freq" in payload:
        is_valid, error = _validate_enum_field(
            "ssd-trim-freq",
            payload["ssd-trim-freq"],
            VALID_BODY_SSD_TRIM_FREQ,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssd-trim-weekday" in payload:
        is_valid, error = _validate_enum_field(
            "ssd-trim-weekday",
            payload["ssd-trim-weekday"],
            VALID_BODY_SSD_TRIM_WEEKDAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-concurrent" in payload:
        is_valid, error = _validate_enum_field(
            "admin-concurrent",
            payload["admin-concurrent"],
            VALID_BODY_ADMIN_CONCURRENT,
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
    if "daily-restart" in payload:
        is_valid, error = _validate_enum_field(
            "daily-restart",
            payload["daily-restart"],
            VALID_BODY_DAILY_RESTART,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wad-restart-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wad-restart-mode",
            payload["wad-restart-mode"],
            VALID_BODY_WAD_RESTART_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "batch-cmdb" in payload:
        is_valid, error = _validate_enum_field(
            "batch-cmdb",
            payload["batch-cmdb"],
            VALID_BODY_BATCH_CMDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multi-factor-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "multi-factor-authentication",
            payload["multi-factor-authentication"],
            VALID_BODY_MULTI_FACTOR_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "autorun-log-fsck" in payload:
        is_valid, error = _validate_enum_field(
            "autorun-log-fsck",
            payload["autorun-log-fsck"],
            VALID_BODY_AUTORUN_LOG_FSCK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-priority" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-priority",
            payload["traffic-priority"],
            VALID_BODY_TRAFFIC_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-priority-level" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-priority-level",
            payload["traffic-priority-level"],
            VALID_BODY_TRAFFIC_PRIORITY_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quic-congestion-control-algo" in payload:
        is_valid, error = _validate_enum_field(
            "quic-congestion-control-algo",
            payload["quic-congestion-control-algo"],
            VALID_BODY_QUIC_CONGESTION_CONTROL_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quic-udp-payload-size-shaping-per-cid" in payload:
        is_valid, error = _validate_enum_field(
            "quic-udp-payload-size-shaping-per-cid",
            payload["quic-udp-payload-size-shaping-per-cid"],
            VALID_BODY_QUIC_UDP_PAYLOAD_SIZE_SHAPING_PER_CID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quic-pmtud" in payload:
        is_valid, error = _validate_enum_field(
            "quic-pmtud",
            payload["quic-pmtud"],
            VALID_BODY_QUIC_PMTUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "anti-replay" in payload:
        is_valid, error = _validate_enum_field(
            "anti-replay",
            payload["anti-replay"],
            VALID_BODY_ANTI_REPLAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-pmtu-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "send-pmtu-icmp",
            payload["send-pmtu-icmp"],
            VALID_BODY_SEND_PMTU_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "honor-df" in payload:
        is_valid, error = _validate_enum_field(
            "honor-df",
            payload["honor-df"],
            VALID_BODY_HONOR_DF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pmtu-discovery" in payload:
        is_valid, error = _validate_enum_field(
            "pmtu-discovery",
            payload["pmtu-discovery"],
            VALID_BODY_PMTU_DISCOVERY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "revision-image-auto-backup" in payload:
        is_valid, error = _validate_enum_field(
            "revision-image-auto-backup",
            payload["revision-image-auto-backup"],
            VALID_BODY_REVISION_IMAGE_AUTO_BACKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "revision-backup-on-logout" in payload:
        is_valid, error = _validate_enum_field(
            "revision-backup-on-logout",
            payload["revision-backup-on-logout"],
            VALID_BODY_REVISION_BACKUP_ON_LOGOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strong-crypto" in payload:
        is_valid, error = _validate_enum_field(
            "strong-crypto",
            payload["strong-crypto"],
            VALID_BODY_STRONG_CRYPTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-static-key-ciphers" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-static-key-ciphers",
            payload["ssl-static-key-ciphers"],
            VALID_BODY_SSL_STATIC_KEY_CIPHERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "snat-route-change" in payload:
        is_valid, error = _validate_enum_field(
            "snat-route-change",
            payload["snat-route-change"],
            VALID_BODY_SNAT_ROUTE_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-snat-route-change" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-snat-route-change",
            payload["ipv6-snat-route-change"],
            VALID_BODY_IPV6_SNAT_ROUTE_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "speedtest-server" in payload:
        is_valid, error = _validate_enum_field(
            "speedtest-server",
            payload["speedtest-server"],
            VALID_BODY_SPEEDTEST_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-audit-log" in payload:
        is_valid, error = _validate_enum_field(
            "cli-audit-log",
            payload["cli-audit-log"],
            VALID_BODY_CLI_AUDIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-params" in payload:
        is_valid, error = _validate_enum_field(
            "dh-params",
            payload["dh-params"],
            VALID_BODY_DH_PARAMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fds-statistics" in payload:
        is_valid, error = _validate_enum_field(
            "fds-statistics",
            payload["fds-statistics"],
            VALID_BODY_FDS_STATISTICS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tcp-option" in payload:
        is_valid, error = _validate_enum_field(
            "tcp-option",
            payload["tcp-option"],
            VALID_BODY_TCP_OPTION,
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
    if "lldp-reception" in payload:
        is_valid, error = _validate_enum_field(
            "lldp-reception",
            payload["lldp-reception"],
            VALID_BODY_LLDP_RECEPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-keep-alive-mode" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-keep-alive-mode",
            payload["proxy-keep-alive-mode"],
            VALID_BODY_PROXY_KEEP_ALIVE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-auth-lifetime" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-auth-lifetime",
            payload["proxy-auth-lifetime"],
            VALID_BODY_PROXY_AUTH_LIFETIME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-resource-mode" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-resource-mode",
            payload["proxy-resource-mode"],
            VALID_BODY_PROXY_RESOURCE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-cert-use-mgmt-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-cert-use-mgmt-vdom",
            payload["proxy-cert-use-mgmt-vdom"],
            VALID_BODY_PROXY_CERT_USE_MGMT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-protocol-header" in payload:
        is_valid, error = _validate_enum_field(
            "check-protocol-header",
            payload["check-protocol-header"],
            VALID_BODY_CHECK_PROTOCOL_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vip-arp-range" in payload:
        is_valid, error = _validate_enum_field(
            "vip-arp-range",
            payload["vip-arp-range"],
            VALID_BODY_VIP_ARP_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reset-sessionless-tcp" in payload:
        is_valid, error = _validate_enum_field(
            "reset-sessionless-tcp",
            payload["reset-sessionless-tcp"],
            VALID_BODY_RESET_SESSIONLESS_TCP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-traffic-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "allow-traffic-redirect",
            payload["allow-traffic-redirect"],
            VALID_BODY_ALLOW_TRAFFIC_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-traffic-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-traffic-redirect",
            payload["ipv6-allow-traffic-redirect"],
            VALID_BODY_IPV6_ALLOW_TRAFFIC_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-dirty-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-dirty-session-check",
            payload["strict-dirty-session-check"],
            VALID_BODY_STRICT_DIRTY_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pre-login-banner" in payload:
        is_valid, error = _validate_enum_field(
            "pre-login-banner",
            payload["pre-login-banner"],
            VALID_BODY_PRE_LOGIN_BANNER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "post-login-banner" in payload:
        is_valid, error = _validate_enum_field(
            "post-login-banner",
            payload["post-login-banner"],
            VALID_BODY_POST_LOGIN_BANNER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tftp" in payload:
        is_valid, error = _validate_enum_field(
            "tftp",
            payload["tftp"],
            VALID_BODY_TFTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-failopen" in payload:
        is_valid, error = _validate_enum_field(
            "av-failopen",
            payload["av-failopen"],
            VALID_BODY_AV_FAILOPEN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-failopen-session" in payload:
        is_valid, error = _validate_enum_field(
            "av-failopen-session",
            payload["av-failopen-session"],
            VALID_BODY_AV_FAILOPEN_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-single-cpu-high" in payload:
        is_valid, error = _validate_enum_field(
            "log-single-cpu-high",
            payload["log-single-cpu-high"],
            VALID_BODY_LOG_SINGLE_CPU_HIGH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-reset-range" in payload:
        is_valid, error = _validate_enum_field(
            "check-reset-range",
            payload["check-reset-range"],
            VALID_BODY_CHECK_RESET_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upgrade-report" in payload:
        is_valid, error = _validate_enum_field(
            "upgrade-report",
            payload["upgrade-report"],
            VALID_BODY_UPGRADE_REPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-redirect",
            payload["admin-https-redirect"],
            VALID_BODY_ADMIN_HTTPS_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-ssh-password" in payload:
        is_valid, error = _validate_enum_field(
            "admin-ssh-password",
            payload["admin-ssh-password"],
            VALID_BODY_ADMIN_SSH_PASSWORD,
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
    if "admin-ssh-v1" in payload:
        is_valid, error = _validate_enum_field(
            "admin-ssh-v1",
            payload["admin-ssh-v1"],
            VALID_BODY_ADMIN_SSH_V1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-telnet" in payload:
        is_valid, error = _validate_enum_field(
            "admin-telnet",
            payload["admin-telnet"],
            VALID_BODY_ADMIN_TELNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-forticloud-sso-login" in payload:
        is_valid, error = _validate_enum_field(
            "admin-forticloud-sso-login",
            payload["admin-forticloud-sso-login"],
            VALID_BODY_ADMIN_FORTICLOUD_SSO_LOGIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-pki-required" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-pki-required",
            payload["admin-https-pki-required"],
            VALID_BODY_ADMIN_HTTPS_PKI_REQUIRED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-keepalive" in payload:
        is_valid, error = _validate_enum_field(
            "auth-keepalive",
            payload["auth-keepalive"],
            VALID_BODY_AUTH_KEEPALIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-session-limit" in payload:
        is_valid, error = _validate_enum_field(
            "auth-session-limit",
            payload["auth-session-limit"],
            VALID_BODY_AUTH_SESSION_LIMIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clt-cert-req" in payload:
        is_valid, error = _validate_enum_field(
            "clt-cert-req",
            payload["clt-cert-req"],
            VALID_BODY_CLT_CERT_REQ,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cfg-save" in payload:
        is_valid, error = _validate_enum_field(
            "cfg-save",
            payload["cfg-save"],
            VALID_BODY_CFG_SAVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reboot-upon-config-restore" in payload:
        is_valid, error = _validate_enum_field(
            "reboot-upon-config-restore",
            payload["reboot-upon-config-restore"],
            VALID_BODY_REBOOT_UPON_CONFIG_RESTORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-scp" in payload:
        is_valid, error = _validate_enum_field(
            "admin-scp",
            payload["admin-scp"],
            VALID_BODY_ADMIN_SCP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wireless-controller" in payload:
        is_valid, error = _validate_enum_field(
            "wireless-controller",
            payload["wireless-controller"],
            VALID_BODY_WIRELESS_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender",
            payload["fortiextender"],
            VALID_BODY_FORTIEXTENDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender-discovery-lockdown" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender-discovery-lockdown",
            payload["fortiextender-discovery-lockdown"],
            VALID_BODY_FORTIEXTENDER_DISCOVERY_LOCKDOWN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender-vlan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender-vlan-mode",
            payload["fortiextender-vlan-mode"],
            VALID_BODY_FORTIEXTENDER_VLAN_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender-provision-on-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender-provision-on-authorization",
            payload["fortiextender-provision-on-authorization"],
            VALID_BODY_FORTIEXTENDER_PROVISION_ON_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller",
            payload["switch-controller"],
            VALID_BODY_SWITCH_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fgd-alert-subscription" in payload:
        is_valid, error = _validate_enum_field(
            "fgd-alert-subscription",
            payload["fgd-alert-subscription"],
            VALID_BODY_FGD_ALERT_SUBSCRIPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-anycast-probe" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-anycast-probe",
            payload["ipv6-allow-anycast-probe"],
            VALID_BODY_IPV6_ALLOW_ANYCAST_PROBE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-multicast-probe" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-multicast-probe",
            payload["ipv6-allow-multicast-probe"],
            VALID_BODY_IPV6_ALLOW_MULTICAST_PROBE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-local-in-silent-drop" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-local-in-silent-drop",
            payload["ipv6-allow-local-in-silent-drop"],
            VALID_BODY_IPV6_ALLOW_LOCAL_IN_SILENT_DROP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "csr-ca-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "csr-ca-attribute",
            payload["csr-ca-attribute"],
            VALID_BODY_CSR_CA_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wimax-4g-usb" in payload:
        is_valid, error = _validate_enum_field(
            "wimax-4g-usb",
            payload["wimax-4g-usb"],
            VALID_BODY_WIMAX_4G_USB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sslvpn-web-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sslvpn-web-mode",
            payload["sslvpn-web-mode"],
            VALID_BODY_SSLVPN_WEB_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-user-bal" in payload:
        is_valid, error = _validate_enum_field(
            "per-user-bal",
            payload["per-user-bal"],
            VALID_BODY_PER_USER_BAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wad-source-affinity" in payload:
        is_valid, error = _validate_enum_field(
            "wad-source-affinity",
            payload["wad-source-affinity"],
            VALID_BODY_WAD_SOURCE_AFFINITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "login-timestamp" in payload:
        is_valid, error = _validate_enum_field(
            "login-timestamp",
            payload["login-timestamp"],
            VALID_BODY_LOGIN_TIMESTAMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-conflict-detection" in payload:
        is_valid, error = _validate_enum_field(
            "ip-conflict-detection",
            payload["ip-conflict-detection"],
            VALID_BODY_IP_CONFLICT_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "special-file-23-support" in payload:
        is_valid, error = _validate_enum_field(
            "special-file-23-support",
            payload["special-file-23-support"],
            VALID_BODY_SPECIAL_FILE_23_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-uuid-address" in payload:
        is_valid, error = _validate_enum_field(
            "log-uuid-address",
            payload["log-uuid-address"],
            VALID_BODY_LOG_UUID_ADDRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-ssl-connection" in payload:
        is_valid, error = _validate_enum_field(
            "log-ssl-connection",
            payload["log-ssl-connection"],
            VALID_BODY_LOG_SSL_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-rest-api-cache" in payload:
        is_valid, error = _validate_enum_field(
            "gui-rest-api-cache",
            payload["gui-rest-api-cache"],
            VALID_BODY_GUI_REST_API_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-key-url-query" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-key-url-query",
            payload["rest-api-key-url-query"],
            VALID_BODY_REST_API_KEY_URL_QUERY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-qat-offload" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-qat-offload",
            payload["ipsec-qat-offload"],
            VALID_BODY_IPSEC_QAT_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "private-data-encryption" in payload:
        is_valid, error = _validate_enum_field(
            "private-data-encryption",
            payload["private-data-encryption"],
            VALID_BODY_PRIVATE_DATA_ENCRYPTION,
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
    if "gui-theme" in payload:
        is_valid, error = _validate_enum_field(
            "gui-theme",
            payload["gui-theme"],
            VALID_BODY_GUI_THEME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-date-format" in payload:
        is_valid, error = _validate_enum_field(
            "gui-date-format",
            payload["gui-date-format"],
            VALID_BODY_GUI_DATE_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-date-time-source" in payload:
        is_valid, error = _validate_enum_field(
            "gui-date-time-source",
            payload["gui-date-time-source"],
            VALID_BODY_GUI_DATE_TIME_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cloud-communication" in payload:
        is_valid, error = _validate_enum_field(
            "cloud-communication",
            payload["cloud-communication"],
            VALID_BODY_CLOUD_COMMUNICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortitoken-cloud" in payload:
        is_valid, error = _validate_enum_field(
            "fortitoken-cloud",
            payload["fortitoken-cloud"],
            VALID_BODY_FORTITOKEN_CLOUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortitoken-cloud-push-status" in payload:
        is_valid, error = _validate_enum_field(
            "fortitoken-cloud-push-status",
            payload["fortitoken-cloud-push-status"],
            VALID_BODY_FORTITOKEN_CLOUD_PUSH_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "irq-time-accounting" in payload:
        is_valid, error = _validate_enum_field(
            "irq-time-accounting",
            payload["irq-time-accounting"],
            VALID_BODY_IRQ_TIME_ACCOUNTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "management-port-use-admin-sport" in payload:
        is_valid, error = _validate_enum_field(
            "management-port-use-admin-sport",
            payload["management-port-use-admin-sport"],
            VALID_BODY_MANAGEMENT_PORT_USE_ADMIN_SPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticonverter-integration" in payload:
        is_valid, error = _validate_enum_field(
            "forticonverter-integration",
            payload["forticonverter-integration"],
            VALID_BODY_FORTICONVERTER_INTEGRATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticonverter-config-upload" in payload:
        is_valid, error = _validate_enum_field(
            "forticonverter-config-upload",
            payload["forticonverter-config-upload"],
            VALID_BODY_FORTICONVERTER_CONFIG_UPLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-database" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-database",
            payload["internet-service-database"],
            VALID_BODY_INTERNET_SERVICE_DATABASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "geoip-full-db" in payload:
        is_valid, error = _validate_enum_field(
            "geoip-full-db",
            payload["geoip-full-db"],
            VALID_BODY_GEOIP_FULL_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "early-tcp-npu-session" in payload:
        is_valid, error = _validate_enum_field(
            "early-tcp-npu-session",
            payload["early-tcp-npu-session"],
            VALID_BODY_EARLY_TCP_NPU_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-neighbor-update" in payload:
        is_valid, error = _validate_enum_field(
            "npu-neighbor-update",
            payload["npu-neighbor-update"],
            VALID_BODY_NPU_NEIGHBOR_UPDATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "delay-tcp-npu-session" in payload:
        is_valid, error = _validate_enum_field(
            "delay-tcp-npu-session",
            payload["delay-tcp-npu-session"],
            VALID_BODY_DELAY_TCP_NPU_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-subnet-usage" in payload:
        is_valid, error = _validate_enum_field(
            "interface-subnet-usage",
            payload["interface-subnet-usage"],
            VALID_BODY_INTERFACE_SUBNET_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortigslb-integration" in payload:
        is_valid, error = _validate_enum_field(
            "fortigslb-integration",
            payload["fortigslb-integration"],
            VALID_BODY_FORTIGSLB_INTEGRATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-session-auto-backup" in payload:
        is_valid, error = _validate_enum_field(
            "auth-session-auto-backup",
            payload["auth-session-auto-backup"],
            VALID_BODY_AUTH_SESSION_AUTO_BACKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-session-auto-backup-interval" in payload:
        is_valid, error = _validate_enum_field(
            "auth-session-auto-backup-interval",
            payload["auth-session-auto-backup-interval"],
            VALID_BODY_AUTH_SESSION_AUTO_BACKUP_INTERVAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-bandwidth-tracking" in payload:
        is_valid, error = _validate_enum_field(
            "application-bandwidth-tracking",
            payload["application-bandwidth-tracking"],
            VALID_BODY_APPLICATION_BANDWIDTH_TRACKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tls-session-cache" in payload:
        is_valid, error = _validate_enum_field(
            "tls-session-cache",
            payload["tls-session-cache"],
            VALID_BODY_TLS_SESSION_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_global_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/global_."""
    # Validate enum values using central function
    if "language" in payload:
        is_valid, error = _validate_enum_field(
            "language",
            payload["language"],
            VALID_BODY_LANGUAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-ipv6" in payload:
        is_valid, error = _validate_enum_field(
            "gui-ipv6",
            payload["gui-ipv6"],
            VALID_BODY_GUI_IPV6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-replacement-message-groups" in payload:
        is_valid, error = _validate_enum_field(
            "gui-replacement-message-groups",
            payload["gui-replacement-message-groups"],
            VALID_BODY_GUI_REPLACEMENT_MESSAGE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-local-out" in payload:
        is_valid, error = _validate_enum_field(
            "gui-local-out",
            payload["gui-local-out"],
            VALID_BODY_GUI_LOCAL_OUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-certificates" in payload:
        is_valid, error = _validate_enum_field(
            "gui-certificates",
            payload["gui-certificates"],
            VALID_BODY_GUI_CERTIFICATES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-custom-language" in payload:
        is_valid, error = _validate_enum_field(
            "gui-custom-language",
            payload["gui-custom-language"],
            VALID_BODY_GUI_CUSTOM_LANGUAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-wireless-opensecurity" in payload:
        is_valid, error = _validate_enum_field(
            "gui-wireless-opensecurity",
            payload["gui-wireless-opensecurity"],
            VALID_BODY_GUI_WIRELESS_OPENSECURITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-app-detection-sdwan" in payload:
        is_valid, error = _validate_enum_field(
            "gui-app-detection-sdwan",
            payload["gui-app-detection-sdwan"],
            VALID_BODY_GUI_APP_DETECTION_SDWAN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-display-hostname" in payload:
        is_valid, error = _validate_enum_field(
            "gui-display-hostname",
            payload["gui-display-hostname"],
            VALID_BODY_GUI_DISPLAY_HOSTNAME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-fortigate-cloud-sandbox" in payload:
        is_valid, error = _validate_enum_field(
            "gui-fortigate-cloud-sandbox",
            payload["gui-fortigate-cloud-sandbox"],
            VALID_BODY_GUI_FORTIGATE_CLOUD_SANDBOX,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-firmware-upgrade-warning" in payload:
        is_valid, error = _validate_enum_field(
            "gui-firmware-upgrade-warning",
            payload["gui-firmware-upgrade-warning"],
            VALID_BODY_GUI_FIRMWARE_UPGRADE_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-forticare-registration-setup-warning" in payload:
        is_valid, error = _validate_enum_field(
            "gui-forticare-registration-setup-warning",
            payload["gui-forticare-registration-setup-warning"],
            VALID_BODY_GUI_FORTICARE_REGISTRATION_SETUP_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-auto-upgrade-setup-warning" in payload:
        is_valid, error = _validate_enum_field(
            "gui-auto-upgrade-setup-warning",
            payload["gui-auto-upgrade-setup-warning"],
            VALID_BODY_GUI_AUTO_UPGRADE_SETUP_WARNING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-workflow-management" in payload:
        is_valid, error = _validate_enum_field(
            "gui-workflow-management",
            payload["gui-workflow-management"],
            VALID_BODY_GUI_WORKFLOW_MANAGEMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-cdn-usage" in payload:
        is_valid, error = _validate_enum_field(
            "gui-cdn-usage",
            payload["gui-cdn-usage"],
            VALID_BODY_GUI_CDN_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-ssl-versions" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-ssl-versions",
            payload["admin-https-ssl-versions"],
            VALID_BODY_ADMIN_HTTPS_SSL_VERSIONS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-ssl-ciphersuites" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-ssl-ciphersuites",
            payload["admin-https-ssl-ciphersuites"],
            VALID_BODY_ADMIN_HTTPS_SSL_CIPHERSUITES,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-ssl-banned-ciphers" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-ssl-banned-ciphers",
            payload["admin-https-ssl-banned-ciphers"],
            VALID_BODY_ADMIN_HTTPS_SSL_BANNED_CIPHERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssd-trim-freq" in payload:
        is_valid, error = _validate_enum_field(
            "ssd-trim-freq",
            payload["ssd-trim-freq"],
            VALID_BODY_SSD_TRIM_FREQ,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssd-trim-weekday" in payload:
        is_valid, error = _validate_enum_field(
            "ssd-trim-weekday",
            payload["ssd-trim-weekday"],
            VALID_BODY_SSD_TRIM_WEEKDAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-concurrent" in payload:
        is_valid, error = _validate_enum_field(
            "admin-concurrent",
            payload["admin-concurrent"],
            VALID_BODY_ADMIN_CONCURRENT,
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
    if "daily-restart" in payload:
        is_valid, error = _validate_enum_field(
            "daily-restart",
            payload["daily-restart"],
            VALID_BODY_DAILY_RESTART,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wad-restart-mode" in payload:
        is_valid, error = _validate_enum_field(
            "wad-restart-mode",
            payload["wad-restart-mode"],
            VALID_BODY_WAD_RESTART_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "batch-cmdb" in payload:
        is_valid, error = _validate_enum_field(
            "batch-cmdb",
            payload["batch-cmdb"],
            VALID_BODY_BATCH_CMDB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "multi-factor-authentication" in payload:
        is_valid, error = _validate_enum_field(
            "multi-factor-authentication",
            payload["multi-factor-authentication"],
            VALID_BODY_MULTI_FACTOR_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-proto-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-proto-version",
            payload["ssl-min-proto-version"],
            VALID_BODY_SSL_MIN_PROTO_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "autorun-log-fsck" in payload:
        is_valid, error = _validate_enum_field(
            "autorun-log-fsck",
            payload["autorun-log-fsck"],
            VALID_BODY_AUTORUN_LOG_FSCK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-priority" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-priority",
            payload["traffic-priority"],
            VALID_BODY_TRAFFIC_PRIORITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "traffic-priority-level" in payload:
        is_valid, error = _validate_enum_field(
            "traffic-priority-level",
            payload["traffic-priority-level"],
            VALID_BODY_TRAFFIC_PRIORITY_LEVEL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quic-congestion-control-algo" in payload:
        is_valid, error = _validate_enum_field(
            "quic-congestion-control-algo",
            payload["quic-congestion-control-algo"],
            VALID_BODY_QUIC_CONGESTION_CONTROL_ALGO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quic-udp-payload-size-shaping-per-cid" in payload:
        is_valid, error = _validate_enum_field(
            "quic-udp-payload-size-shaping-per-cid",
            payload["quic-udp-payload-size-shaping-per-cid"],
            VALID_BODY_QUIC_UDP_PAYLOAD_SIZE_SHAPING_PER_CID,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "quic-pmtud" in payload:
        is_valid, error = _validate_enum_field(
            "quic-pmtud",
            payload["quic-pmtud"],
            VALID_BODY_QUIC_PMTUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "anti-replay" in payload:
        is_valid, error = _validate_enum_field(
            "anti-replay",
            payload["anti-replay"],
            VALID_BODY_ANTI_REPLAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-pmtu-icmp" in payload:
        is_valid, error = _validate_enum_field(
            "send-pmtu-icmp",
            payload["send-pmtu-icmp"],
            VALID_BODY_SEND_PMTU_ICMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "honor-df" in payload:
        is_valid, error = _validate_enum_field(
            "honor-df",
            payload["honor-df"],
            VALID_BODY_HONOR_DF,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pmtu-discovery" in payload:
        is_valid, error = _validate_enum_field(
            "pmtu-discovery",
            payload["pmtu-discovery"],
            VALID_BODY_PMTU_DISCOVERY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "revision-image-auto-backup" in payload:
        is_valid, error = _validate_enum_field(
            "revision-image-auto-backup",
            payload["revision-image-auto-backup"],
            VALID_BODY_REVISION_IMAGE_AUTO_BACKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "revision-backup-on-logout" in payload:
        is_valid, error = _validate_enum_field(
            "revision-backup-on-logout",
            payload["revision-backup-on-logout"],
            VALID_BODY_REVISION_BACKUP_ON_LOGOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strong-crypto" in payload:
        is_valid, error = _validate_enum_field(
            "strong-crypto",
            payload["strong-crypto"],
            VALID_BODY_STRONG_CRYPTO,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-static-key-ciphers" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-static-key-ciphers",
            payload["ssl-static-key-ciphers"],
            VALID_BODY_SSL_STATIC_KEY_CIPHERS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "snat-route-change" in payload:
        is_valid, error = _validate_enum_field(
            "snat-route-change",
            payload["snat-route-change"],
            VALID_BODY_SNAT_ROUTE_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-snat-route-change" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-snat-route-change",
            payload["ipv6-snat-route-change"],
            VALID_BODY_IPV6_SNAT_ROUTE_CHANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "speedtest-server" in payload:
        is_valid, error = _validate_enum_field(
            "speedtest-server",
            payload["speedtest-server"],
            VALID_BODY_SPEEDTEST_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cli-audit-log" in payload:
        is_valid, error = _validate_enum_field(
            "cli-audit-log",
            payload["cli-audit-log"],
            VALID_BODY_CLI_AUDIT_LOG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dh-params" in payload:
        is_valid, error = _validate_enum_field(
            "dh-params",
            payload["dh-params"],
            VALID_BODY_DH_PARAMS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fds-statistics" in payload:
        is_valid, error = _validate_enum_field(
            "fds-statistics",
            payload["fds-statistics"],
            VALID_BODY_FDS_STATISTICS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tcp-option" in payload:
        is_valid, error = _validate_enum_field(
            "tcp-option",
            payload["tcp-option"],
            VALID_BODY_TCP_OPTION,
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
    if "lldp-reception" in payload:
        is_valid, error = _validate_enum_field(
            "lldp-reception",
            payload["lldp-reception"],
            VALID_BODY_LLDP_RECEPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-keep-alive-mode" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-keep-alive-mode",
            payload["proxy-keep-alive-mode"],
            VALID_BODY_PROXY_KEEP_ALIVE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-auth-lifetime" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-auth-lifetime",
            payload["proxy-auth-lifetime"],
            VALID_BODY_PROXY_AUTH_LIFETIME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-resource-mode" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-resource-mode",
            payload["proxy-resource-mode"],
            VALID_BODY_PROXY_RESOURCE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "proxy-cert-use-mgmt-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "proxy-cert-use-mgmt-vdom",
            payload["proxy-cert-use-mgmt-vdom"],
            VALID_BODY_PROXY_CERT_USE_MGMT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-protocol-header" in payload:
        is_valid, error = _validate_enum_field(
            "check-protocol-header",
            payload["check-protocol-header"],
            VALID_BODY_CHECK_PROTOCOL_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vip-arp-range" in payload:
        is_valid, error = _validate_enum_field(
            "vip-arp-range",
            payload["vip-arp-range"],
            VALID_BODY_VIP_ARP_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reset-sessionless-tcp" in payload:
        is_valid, error = _validate_enum_field(
            "reset-sessionless-tcp",
            payload["reset-sessionless-tcp"],
            VALID_BODY_RESET_SESSIONLESS_TCP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "allow-traffic-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "allow-traffic-redirect",
            payload["allow-traffic-redirect"],
            VALID_BODY_ALLOW_TRAFFIC_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-traffic-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-traffic-redirect",
            payload["ipv6-allow-traffic-redirect"],
            VALID_BODY_IPV6_ALLOW_TRAFFIC_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "strict-dirty-session-check" in payload:
        is_valid, error = _validate_enum_field(
            "strict-dirty-session-check",
            payload["strict-dirty-session-check"],
            VALID_BODY_STRICT_DIRTY_SESSION_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pre-login-banner" in payload:
        is_valid, error = _validate_enum_field(
            "pre-login-banner",
            payload["pre-login-banner"],
            VALID_BODY_PRE_LOGIN_BANNER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "post-login-banner" in payload:
        is_valid, error = _validate_enum_field(
            "post-login-banner",
            payload["post-login-banner"],
            VALID_BODY_POST_LOGIN_BANNER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tftp" in payload:
        is_valid, error = _validate_enum_field(
            "tftp",
            payload["tftp"],
            VALID_BODY_TFTP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-failopen" in payload:
        is_valid, error = _validate_enum_field(
            "av-failopen",
            payload["av-failopen"],
            VALID_BODY_AV_FAILOPEN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "av-failopen-session" in payload:
        is_valid, error = _validate_enum_field(
            "av-failopen-session",
            payload["av-failopen-session"],
            VALID_BODY_AV_FAILOPEN_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-single-cpu-high" in payload:
        is_valid, error = _validate_enum_field(
            "log-single-cpu-high",
            payload["log-single-cpu-high"],
            VALID_BODY_LOG_SINGLE_CPU_HIGH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-reset-range" in payload:
        is_valid, error = _validate_enum_field(
            "check-reset-range",
            payload["check-reset-range"],
            VALID_BODY_CHECK_RESET_RANGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upgrade-report" in payload:
        is_valid, error = _validate_enum_field(
            "upgrade-report",
            payload["upgrade-report"],
            VALID_BODY_UPGRADE_REPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-redirect",
            payload["admin-https-redirect"],
            VALID_BODY_ADMIN_HTTPS_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-ssh-password" in payload:
        is_valid, error = _validate_enum_field(
            "admin-ssh-password",
            payload["admin-ssh-password"],
            VALID_BODY_ADMIN_SSH_PASSWORD,
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
    if "admin-ssh-v1" in payload:
        is_valid, error = _validate_enum_field(
            "admin-ssh-v1",
            payload["admin-ssh-v1"],
            VALID_BODY_ADMIN_SSH_V1,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-telnet" in payload:
        is_valid, error = _validate_enum_field(
            "admin-telnet",
            payload["admin-telnet"],
            VALID_BODY_ADMIN_TELNET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-forticloud-sso-login" in payload:
        is_valid, error = _validate_enum_field(
            "admin-forticloud-sso-login",
            payload["admin-forticloud-sso-login"],
            VALID_BODY_ADMIN_FORTICLOUD_SSO_LOGIN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-https-pki-required" in payload:
        is_valid, error = _validate_enum_field(
            "admin-https-pki-required",
            payload["admin-https-pki-required"],
            VALID_BODY_ADMIN_HTTPS_PKI_REQUIRED,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-keepalive" in payload:
        is_valid, error = _validate_enum_field(
            "auth-keepalive",
            payload["auth-keepalive"],
            VALID_BODY_AUTH_KEEPALIVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-session-limit" in payload:
        is_valid, error = _validate_enum_field(
            "auth-session-limit",
            payload["auth-session-limit"],
            VALID_BODY_AUTH_SESSION_LIMIT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "clt-cert-req" in payload:
        is_valid, error = _validate_enum_field(
            "clt-cert-req",
            payload["clt-cert-req"],
            VALID_BODY_CLT_CERT_REQ,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cfg-save" in payload:
        is_valid, error = _validate_enum_field(
            "cfg-save",
            payload["cfg-save"],
            VALID_BODY_CFG_SAVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reboot-upon-config-restore" in payload:
        is_valid, error = _validate_enum_field(
            "reboot-upon-config-restore",
            payload["reboot-upon-config-restore"],
            VALID_BODY_REBOOT_UPON_CONFIG_RESTORE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "admin-scp" in payload:
        is_valid, error = _validate_enum_field(
            "admin-scp",
            payload["admin-scp"],
            VALID_BODY_ADMIN_SCP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wireless-controller" in payload:
        is_valid, error = _validate_enum_field(
            "wireless-controller",
            payload["wireless-controller"],
            VALID_BODY_WIRELESS_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender",
            payload["fortiextender"],
            VALID_BODY_FORTIEXTENDER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender-discovery-lockdown" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender-discovery-lockdown",
            payload["fortiextender-discovery-lockdown"],
            VALID_BODY_FORTIEXTENDER_DISCOVERY_LOCKDOWN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender-vlan-mode" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender-vlan-mode",
            payload["fortiextender-vlan-mode"],
            VALID_BODY_FORTIEXTENDER_VLAN_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortiextender-provision-on-authorization" in payload:
        is_valid, error = _validate_enum_field(
            "fortiextender-provision-on-authorization",
            payload["fortiextender-provision-on-authorization"],
            VALID_BODY_FORTIEXTENDER_PROVISION_ON_AUTHORIZATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "switch-controller" in payload:
        is_valid, error = _validate_enum_field(
            "switch-controller",
            payload["switch-controller"],
            VALID_BODY_SWITCH_CONTROLLER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fgd-alert-subscription" in payload:
        is_valid, error = _validate_enum_field(
            "fgd-alert-subscription",
            payload["fgd-alert-subscription"],
            VALID_BODY_FGD_ALERT_SUBSCRIPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-anycast-probe" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-anycast-probe",
            payload["ipv6-allow-anycast-probe"],
            VALID_BODY_IPV6_ALLOW_ANYCAST_PROBE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-multicast-probe" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-multicast-probe",
            payload["ipv6-allow-multicast-probe"],
            VALID_BODY_IPV6_ALLOW_MULTICAST_PROBE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipv6-allow-local-in-silent-drop" in payload:
        is_valid, error = _validate_enum_field(
            "ipv6-allow-local-in-silent-drop",
            payload["ipv6-allow-local-in-silent-drop"],
            VALID_BODY_IPV6_ALLOW_LOCAL_IN_SILENT_DROP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "csr-ca-attribute" in payload:
        is_valid, error = _validate_enum_field(
            "csr-ca-attribute",
            payload["csr-ca-attribute"],
            VALID_BODY_CSR_CA_ATTRIBUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wimax-4g-usb" in payload:
        is_valid, error = _validate_enum_field(
            "wimax-4g-usb",
            payload["wimax-4g-usb"],
            VALID_BODY_WIMAX_4G_USB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sslvpn-web-mode" in payload:
        is_valid, error = _validate_enum_field(
            "sslvpn-web-mode",
            payload["sslvpn-web-mode"],
            VALID_BODY_SSLVPN_WEB_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "per-user-bal" in payload:
        is_valid, error = _validate_enum_field(
            "per-user-bal",
            payload["per-user-bal"],
            VALID_BODY_PER_USER_BAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wad-source-affinity" in payload:
        is_valid, error = _validate_enum_field(
            "wad-source-affinity",
            payload["wad-source-affinity"],
            VALID_BODY_WAD_SOURCE_AFFINITY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "login-timestamp" in payload:
        is_valid, error = _validate_enum_field(
            "login-timestamp",
            payload["login-timestamp"],
            VALID_BODY_LOGIN_TIMESTAMP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ip-conflict-detection" in payload:
        is_valid, error = _validate_enum_field(
            "ip-conflict-detection",
            payload["ip-conflict-detection"],
            VALID_BODY_IP_CONFLICT_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "special-file-23-support" in payload:
        is_valid, error = _validate_enum_field(
            "special-file-23-support",
            payload["special-file-23-support"],
            VALID_BODY_SPECIAL_FILE_23_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-uuid-address" in payload:
        is_valid, error = _validate_enum_field(
            "log-uuid-address",
            payload["log-uuid-address"],
            VALID_BODY_LOG_UUID_ADDRESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-ssl-connection" in payload:
        is_valid, error = _validate_enum_field(
            "log-ssl-connection",
            payload["log-ssl-connection"],
            VALID_BODY_LOG_SSL_CONNECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-rest-api-cache" in payload:
        is_valid, error = _validate_enum_field(
            "gui-rest-api-cache",
            payload["gui-rest-api-cache"],
            VALID_BODY_GUI_REST_API_CACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rest-api-key-url-query" in payload:
        is_valid, error = _validate_enum_field(
            "rest-api-key-url-query",
            payload["rest-api-key-url-query"],
            VALID_BODY_REST_API_KEY_URL_QUERY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-qat-offload" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-qat-offload",
            payload["ipsec-qat-offload"],
            VALID_BODY_IPSEC_QAT_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "private-data-encryption" in payload:
        is_valid, error = _validate_enum_field(
            "private-data-encryption",
            payload["private-data-encryption"],
            VALID_BODY_PRIVATE_DATA_ENCRYPTION,
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
    if "gui-theme" in payload:
        is_valid, error = _validate_enum_field(
            "gui-theme",
            payload["gui-theme"],
            VALID_BODY_GUI_THEME,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-date-format" in payload:
        is_valid, error = _validate_enum_field(
            "gui-date-format",
            payload["gui-date-format"],
            VALID_BODY_GUI_DATE_FORMAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gui-date-time-source" in payload:
        is_valid, error = _validate_enum_field(
            "gui-date-time-source",
            payload["gui-date-time-source"],
            VALID_BODY_GUI_DATE_TIME_SOURCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "cloud-communication" in payload:
        is_valid, error = _validate_enum_field(
            "cloud-communication",
            payload["cloud-communication"],
            VALID_BODY_CLOUD_COMMUNICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortitoken-cloud" in payload:
        is_valid, error = _validate_enum_field(
            "fortitoken-cloud",
            payload["fortitoken-cloud"],
            VALID_BODY_FORTITOKEN_CLOUD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortitoken-cloud-push-status" in payload:
        is_valid, error = _validate_enum_field(
            "fortitoken-cloud-push-status",
            payload["fortitoken-cloud-push-status"],
            VALID_BODY_FORTITOKEN_CLOUD_PUSH_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "irq-time-accounting" in payload:
        is_valid, error = _validate_enum_field(
            "irq-time-accounting",
            payload["irq-time-accounting"],
            VALID_BODY_IRQ_TIME_ACCOUNTING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "management-port-use-admin-sport" in payload:
        is_valid, error = _validate_enum_field(
            "management-port-use-admin-sport",
            payload["management-port-use-admin-sport"],
            VALID_BODY_MANAGEMENT_PORT_USE_ADMIN_SPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticonverter-integration" in payload:
        is_valid, error = _validate_enum_field(
            "forticonverter-integration",
            payload["forticonverter-integration"],
            VALID_BODY_FORTICONVERTER_INTEGRATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "forticonverter-config-upload" in payload:
        is_valid, error = _validate_enum_field(
            "forticonverter-config-upload",
            payload["forticonverter-config-upload"],
            VALID_BODY_FORTICONVERTER_CONFIG_UPLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-database" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-database",
            payload["internet-service-database"],
            VALID_BODY_INTERNET_SERVICE_DATABASE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "geoip-full-db" in payload:
        is_valid, error = _validate_enum_field(
            "geoip-full-db",
            payload["geoip-full-db"],
            VALID_BODY_GEOIP_FULL_DB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "early-tcp-npu-session" in payload:
        is_valid, error = _validate_enum_field(
            "early-tcp-npu-session",
            payload["early-tcp-npu-session"],
            VALID_BODY_EARLY_TCP_NPU_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "npu-neighbor-update" in payload:
        is_valid, error = _validate_enum_field(
            "npu-neighbor-update",
            payload["npu-neighbor-update"],
            VALID_BODY_NPU_NEIGHBOR_UPDATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "delay-tcp-npu-session" in payload:
        is_valid, error = _validate_enum_field(
            "delay-tcp-npu-session",
            payload["delay-tcp-npu-session"],
            VALID_BODY_DELAY_TCP_NPU_SESSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "interface-subnet-usage" in payload:
        is_valid, error = _validate_enum_field(
            "interface-subnet-usage",
            payload["interface-subnet-usage"],
            VALID_BODY_INTERFACE_SUBNET_USAGE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fortigslb-integration" in payload:
        is_valid, error = _validate_enum_field(
            "fortigslb-integration",
            payload["fortigslb-integration"],
            VALID_BODY_FORTIGSLB_INTEGRATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-session-auto-backup" in payload:
        is_valid, error = _validate_enum_field(
            "auth-session-auto-backup",
            payload["auth-session-auto-backup"],
            VALID_BODY_AUTH_SESSION_AUTO_BACKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-session-auto-backup-interval" in payload:
        is_valid, error = _validate_enum_field(
            "auth-session-auto-backup-interval",
            payload["auth-session-auto-backup-interval"],
            VALID_BODY_AUTH_SESSION_AUTO_BACKUP_INTERVAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "application-bandwidth-tracking" in payload:
        is_valid, error = _validate_enum_field(
            "application-bandwidth-tracking",
            payload["application-bandwidth-tracking"],
            VALID_BODY_APPLICATION_BANDWIDTH_TRACKING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tls-session-cache" in payload:
        is_valid, error = _validate_enum_field(
            "tls-session-cache",
            payload["tls-session-cache"],
            VALID_BODY_TLS_SESSION_CACHE,
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
    "endpoint": "system/global_",
    "category": "cmdb",
    "api_path": "system/global",
    "help": "Configure global attributes.",
    "total_fields": 252,
    "required_fields_count": 4,
    "fields_with_defaults_count": 251,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
