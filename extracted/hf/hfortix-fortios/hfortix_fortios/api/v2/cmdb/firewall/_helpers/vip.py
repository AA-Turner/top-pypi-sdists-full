"""Validation helpers for firewall/vip - Auto-generated"""

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
    "server-type",  # Protocol to be load balanced by the virtual server (also called the server load balance virtual IP).
    "extip",  # IP address or address range on the external interface that you want to map to an address or address range on the destination network.
    "mappedip",  # IP address or address range on the destination network to which the external IP address is mapped.
    "extintf",  # Interface connected to the source network that receives the packets that will be forwarded to the destination network.
    "extport",  # Incoming port number range that you want to map to a port number range on the destination network.
    "ssl-certificate",  # Name of the certificate to use for SSL handshake.
    "ipv6-mappedip",  # Range of mapped IPv6 addresses. Specify the start IPv6 address followed by a space and the end IPv6 address.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "name": "",
    "id": 0,
    "uuid": "00000000-0000-0000-0000-000000000000",
    "type": "static-nat",
    "server-type": "",
    "dns-mapping-ttl": 0,
    "ldb-method": "static",
    "src-vip-filter": "disable",
    "extip": "",
    "h2-support": "enable",
    "h3-support": "disable",
    "nat44": "enable",
    "nat46": "disable",
    "add-nat46-route": "enable",
    "mapped-addr": "",
    "extintf": "",
    "arp-reply": "enable",
    "http-redirect": "disable",
    "persistence": "none",
    "nat-source-vip": "disable",
    "portforward": "disable",
    "status": "enable",
    "protocol": "tcp",
    "extport": "",
    "mappedport": "",
    "gratuitous-arp-interval": 0,
    "portmapping-type": "1-to-1",
    "empty-cert-action": "block",
    "user-agent-detect": "enable",
    "client-cert": "enable",
    "http-cookie-domain-from-host": "disable",
    "http-cookie-domain": "",
    "http-cookie-path": "",
    "http-cookie-generation": 0,
    "http-cookie-age": 60,
    "http-cookie-share": "same-ip",
    "https-cookie-secure": "disable",
    "http-multiplex": "disable",
    "http-multiplex-ttl": 15,
    "http-multiplex-max-request": 0,
    "http-multiplex-max-concurrent-request": 0,
    "http-ip-header": "disable",
    "http-ip-header-name": "",
    "outlook-web-access": "disable",
    "weblogic-server": "disable",
    "websphere-server": "disable",
    "ssl-mode": "half",
    "ssl-dh-bits": "2048",
    "ssl-algorithm": "high",
    "ssl-server-algorithm": "client",
    "ssl-pfs": "require",
    "ssl-min-version": "tls-1.1",
    "ssl-max-version": "tls-1.3",
    "ssl-server-min-version": "client",
    "ssl-server-max-version": "client",
    "ssl-accept-ffdhe-groups": "enable",
    "ssl-send-empty-frags": "enable",
    "ssl-client-fallback": "enable",
    "ssl-client-renegotiation": "secure",
    "ssl-client-session-state-type": "both",
    "ssl-client-session-state-timeout": 30,
    "ssl-client-session-state-max": 1000,
    "ssl-client-rekey-count": 0,
    "ssl-server-renegotiation": "enable",
    "ssl-server-session-state-type": "both",
    "ssl-server-session-state-timeout": 60,
    "ssl-server-session-state-max": 100,
    "ssl-http-location-conversion": "disable",
    "ssl-http-match-host": "enable",
    "ssl-hpkp": "disable",
    "ssl-hpkp-primary": "",
    "ssl-hpkp-backup": "",
    "ssl-hpkp-age": 5184000,
    "ssl-hpkp-include-subdomains": "disable",
    "ssl-hsts": "disable",
    "ssl-hsts-age": 5184000,
    "ssl-hsts-include-subdomains": "disable",
    "max-embryonic-connections": 1000,
    "color": 0,
    "ipv6-mappedip": "",
    "ipv6-mappedport": "",
    "one-click-gslb-server": "disable",
    "gslb-hostname": "",
    "gslb-domain-name": "",
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
    "name": "string",  # Virtual IP name.
    "id": "integer",  # Custom defined ID.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned 
    "comment": "var-string",  # Comment.
    "type": "option",  # Configure a static NAT, load balance, server load balance, a
    "server-type": "option",  # Protocol to be load balanced by the virtual server (also cal
    "dns-mapping-ttl": "integer",  # DNS mapping TTL (Set to zero to use TTL in DNS response, def
    "ldb-method": "option",  # Method used to distribute sessions to real servers.
    "src-filter": "string",  # Source address filter. Each address must be either an IP/sub
    "src-vip-filter": "option",  # Enable/disable use of 'src-filter' to match destinations for
    "service": "string",  # Service name.
    "extip": "user",  # IP address or address range on the external interface that y
    "extaddr": "string",  # External FQDN address name.
    "h2-support": "option",  # Enable/disable HTTP2 support (default = enable).
    "h3-support": "option",  # Enable/disable HTTP3/QUIC support (default = disable).
    "quic": "string",  # QUIC setting.
    "nat44": "option",  # Enable/disable NAT44.
    "nat46": "option",  # Enable/disable NAT46.
    "add-nat46-route": "option",  # Enable/disable adding NAT46 route.
    "mappedip": "string",  # IP address or address range on the destination network to wh
    "mapped-addr": "string",  # Mapped FQDN address name.
    "extintf": "string",  # Interface connected to the source network that receives the 
    "arp-reply": "option",  # Enable to respond to ARP requests for this virtual IP addres
    "http-redirect": "option",  # Enable/disable redirection of HTTP to HTTPS.
    "persistence": "option",  # Configure how to make sure that clients connect to the same 
    "nat-source-vip": "option",  # Enable/disable forcing the source NAT mapped IP to the exter
    "portforward": "option",  # Enable/disable port forwarding.
    "status": "option",  # Enable/disable VIP.
    "protocol": "option",  # Protocol to use when forwarding packets.
    "extport": "user",  # Incoming port number range that you want to map to a port nu
    "mappedport": "user",  # Port number range on the destination network to which the ex
    "gratuitous-arp-interval": "integer",  # Enable to have the VIP send gratuitous ARPs. 0=disabled. Set
    "srcintf-filter": "string",  # Interfaces to which the VIP applies. Separate the names with
    "portmapping-type": "option",  # Port mapping type.
    "empty-cert-action": "option",  # Action for an empty client certificate.
    "user-agent-detect": "option",  # Enable/disable detecting device type by HTTP user-agent if n
    "client-cert": "option",  # Enable/disable requesting client certificate.
    "realservers": "string",  # Select the real servers that this server load balancing VIP 
    "http-cookie-domain-from-host": "option",  # Enable/disable use of HTTP cookie domain from host field in 
    "http-cookie-domain": "string",  # Domain that HTTP cookie persistence should apply to.
    "http-cookie-path": "string",  # Limit HTTP cookie persistence to the specified path.
    "http-cookie-generation": "integer",  # Generation of HTTP cookie to be accepted. Changing invalidat
    "http-cookie-age": "integer",  # Time in minutes that client web browsers should keep a cooki
    "http-cookie-share": "option",  # Control sharing of cookies across virtual servers. Use of sa
    "https-cookie-secure": "option",  # Enable/disable verification that inserted HTTPS cookies are 
    "http-multiplex": "option",  # Enable/disable HTTP multiplexing.
    "http-multiplex-ttl": "integer",  # Time-to-live for idle connections to servers.
    "http-multiplex-max-request": "integer",  # Maximum number of requests that a multiplex server can handl
    "http-multiplex-max-concurrent-request": "integer",  # Maximum number of concurrent requests that a multiplex serve
    "http-ip-header": "option",  # For HTTP multiplexing, enable to add the original client IP 
    "http-ip-header-name": "string",  # For HTTP multiplexing, enter a custom HTTPS header name. The
    "outlook-web-access": "option",  # Enable to add the Front-End-Https header for Microsoft Outlo
    "weblogic-server": "option",  # Enable to add an HTTP header to indicate SSL offloading for 
    "websphere-server": "option",  # Enable to add an HTTP header to indicate SSL offloading for 
    "ssl-mode": "option",  # Apply SSL offloading between the client and the FortiGate (h
    "ssl-certificate": "string",  # Name of the certificate to use for SSL handshake.
    "ssl-dh-bits": "option",  # Number of bits to use in the Diffie-Hellman exchange for RSA
    "ssl-algorithm": "option",  # Permitted encryption algorithms for SSL sessions according t
    "ssl-cipher-suites": "string",  # SSL/TLS cipher suites acceptable from a client, ordered by p
    "ssl-server-algorithm": "option",  # Permitted encryption algorithms for the server side of SSL f
    "ssl-server-cipher-suites": "string",  # SSL/TLS cipher suites to offer to a server, ordered by prior
    "ssl-pfs": "option",  # Select the cipher suites that can be used for SSL perfect fo
    "ssl-min-version": "option",  # Lowest SSL/TLS version acceptable from a client.
    "ssl-max-version": "option",  # Highest SSL/TLS version acceptable from a client.
    "ssl-server-min-version": "option",  # Lowest SSL/TLS version acceptable from a server. Use the cli
    "ssl-server-max-version": "option",  # Highest SSL/TLS version acceptable from a server. Use the cl
    "ssl-accept-ffdhe-groups": "option",  # Enable/disable FFDHE cipher suite for SSL key exchange.
    "ssl-send-empty-frags": "option",  # Enable/disable sending empty fragments to avoid CBC IV attac
    "ssl-client-fallback": "option",  # Enable/disable support for preventing Downgrade Attacks on c
    "ssl-client-renegotiation": "option",  # Allow, deny, or require secure renegotiation of client sessi
    "ssl-client-session-state-type": "option",  # How to expire SSL sessions for the segment of the SSL connec
    "ssl-client-session-state-timeout": "integer",  # Number of minutes to keep client to FortiGate SSL session st
    "ssl-client-session-state-max": "integer",  # Maximum number of client to FortiGate SSL session states to 
    "ssl-client-rekey-count": "integer",  # Maximum length of data in MB before triggering a client reke
    "ssl-server-renegotiation": "option",  # Enable/disable secure renegotiation to comply with RFC 5746.
    "ssl-server-session-state-type": "option",  # How to expire SSL sessions for the segment of the SSL connec
    "ssl-server-session-state-timeout": "integer",  # Number of minutes to keep FortiGate to Server SSL session st
    "ssl-server-session-state-max": "integer",  # Maximum number of FortiGate to Server SSL session states to 
    "ssl-http-location-conversion": "option",  # Enable to replace HTTP with HTTPS in the reply's Location HT
    "ssl-http-match-host": "option",  # Enable/disable HTTP host matching for location conversion.
    "ssl-hpkp": "option",  # Enable/disable including HPKP header in response.
    "ssl-hpkp-primary": "string",  # Certificate to generate primary HPKP pin from.
    "ssl-hpkp-backup": "string",  # Certificate to generate backup HPKP pin from.
    "ssl-hpkp-age": "integer",  # Number of seconds the client should honor the HPKP setting.
    "ssl-hpkp-report-uri": "var-string",  # URL to report HPKP violations to.
    "ssl-hpkp-include-subdomains": "option",  # Indicate that HPKP header applies to all subdomains.
    "ssl-hsts": "option",  # Enable/disable including HSTS header in response.
    "ssl-hsts-age": "integer",  # Number of seconds the client should honor the HSTS setting.
    "ssl-hsts-include-subdomains": "option",  # Indicate that HSTS header applies to all subdomains.
    "monitor": "string",  # Name of the health check monitor to use when polling to dete
    "max-embryonic-connections": "integer",  # Maximum number of incomplete connections.
    "color": "integer",  # Color of icon on the GUI.
    "ipv6-mappedip": "user",  # Range of mapped IPv6 addresses. Specify the start IPv6 addre
    "ipv6-mappedport": "user",  # IPv6 port number range on the destination network to which t
    "one-click-gslb-server": "option",  # Enable/disable one click GSLB server integration with FortiG
    "gslb-hostname": "string",  # Hostname to use within the configured FortiGSLB domain.
    "gslb-domain-name": "string",  # Domain to use when integrating with FortiGSLB.
    "gslb-public-ips": "string",  # Publicly accessible IP addresses for the FortiGSLB service.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "name": "Virtual IP name.",
    "id": "Custom defined ID.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "comment": "Comment.",
    "type": "Configure a static NAT, load balance, server load balance, access proxy, DNS translation, or FQDN VIP.",
    "server-type": "Protocol to be load balanced by the virtual server (also called the server load balance virtual IP).",
    "dns-mapping-ttl": "DNS mapping TTL (Set to zero to use TTL in DNS response, default = 0).",
    "ldb-method": "Method used to distribute sessions to real servers.",
    "src-filter": "Source address filter. Each address must be either an IP/subnet (x.x.x.x/n) or a range (x.x.x.x-y.y.y.y). Separate addresses with spaces.",
    "src-vip-filter": "Enable/disable use of 'src-filter' to match destinations for the reverse SNAT rule.",
    "service": "Service name.",
    "extip": "IP address or address range on the external interface that you want to map to an address or address range on the destination network.",
    "extaddr": "External FQDN address name.",
    "h2-support": "Enable/disable HTTP2 support (default = enable).",
    "h3-support": "Enable/disable HTTP3/QUIC support (default = disable).",
    "quic": "QUIC setting.",
    "nat44": "Enable/disable NAT44.",
    "nat46": "Enable/disable NAT46.",
    "add-nat46-route": "Enable/disable adding NAT46 route.",
    "mappedip": "IP address or address range on the destination network to which the external IP address is mapped.",
    "mapped-addr": "Mapped FQDN address name.",
    "extintf": "Interface connected to the source network that receives the packets that will be forwarded to the destination network.",
    "arp-reply": "Enable to respond to ARP requests for this virtual IP address. Enabled by default.",
    "http-redirect": "Enable/disable redirection of HTTP to HTTPS.",
    "persistence": "Configure how to make sure that clients connect to the same server every time they make a request that is part of the same session.",
    "nat-source-vip": "Enable/disable forcing the source NAT mapped IP to the external IP for all traffic.",
    "portforward": "Enable/disable port forwarding.",
    "status": "Enable/disable VIP.",
    "protocol": "Protocol to use when forwarding packets.",
    "extport": "Incoming port number range that you want to map to a port number range on the destination network.",
    "mappedport": "Port number range on the destination network to which the external port number range is mapped.",
    "gratuitous-arp-interval": "Enable to have the VIP send gratuitous ARPs. 0=disabled. Set from 5 up to 8640000 seconds to enable.",
    "srcintf-filter": "Interfaces to which the VIP applies. Separate the names with spaces.",
    "portmapping-type": "Port mapping type.",
    "empty-cert-action": "Action for an empty client certificate.",
    "user-agent-detect": "Enable/disable detecting device type by HTTP user-agent if no client certificate is provided.",
    "client-cert": "Enable/disable requesting client certificate.",
    "realservers": "Select the real servers that this server load balancing VIP will distribute traffic to.",
    "http-cookie-domain-from-host": "Enable/disable use of HTTP cookie domain from host field in HTTP.",
    "http-cookie-domain": "Domain that HTTP cookie persistence should apply to.",
    "http-cookie-path": "Limit HTTP cookie persistence to the specified path.",
    "http-cookie-generation": "Generation of HTTP cookie to be accepted. Changing invalidates all existing cookies.",
    "http-cookie-age": "Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit.",
    "http-cookie-share": "Control sharing of cookies across virtual servers. Use of same-ip means a cookie from one virtual server can be used by another. Disable stops cookie sharing.",
    "https-cookie-secure": "Enable/disable verification that inserted HTTPS cookies are secure.",
    "http-multiplex": "Enable/disable HTTP multiplexing.",
    "http-multiplex-ttl": "Time-to-live for idle connections to servers.",
    "http-multiplex-max-request": "Maximum number of requests that a multiplex server can handle before disconnecting sessions (default = unlimited).",
    "http-multiplex-max-concurrent-request": "Maximum number of concurrent requests that a multiplex server can handle (default = unlimited).",
    "http-ip-header": "For HTTP multiplexing, enable to add the original client IP address in the X-Forwarded-For HTTP header.",
    "http-ip-header-name": "For HTTP multiplexing, enter a custom HTTPS header name. The original client IP address is added to this header. If empty, X-Forwarded-For is used.",
    "outlook-web-access": "Enable to add the Front-End-Https header for Microsoft Outlook Web Access.",
    "weblogic-server": "Enable to add an HTTP header to indicate SSL offloading for a WebLogic server.",
    "websphere-server": "Enable to add an HTTP header to indicate SSL offloading for a WebSphere server.",
    "ssl-mode": "Apply SSL offloading between the client and the FortiGate (half) or from the client to the FortiGate and from the FortiGate to the server (full).",
    "ssl-certificate": "Name of the certificate to use for SSL handshake.",
    "ssl-dh-bits": "Number of bits to use in the Diffie-Hellman exchange for RSA encryption of SSL sessions.",
    "ssl-algorithm": "Permitted encryption algorithms for SSL sessions according to encryption strength.",
    "ssl-cipher-suites": "SSL/TLS cipher suites acceptable from a client, ordered by priority.",
    "ssl-server-algorithm": "Permitted encryption algorithms for the server side of SSL full mode sessions according to encryption strength.",
    "ssl-server-cipher-suites": "SSL/TLS cipher suites to offer to a server, ordered by priority.",
    "ssl-pfs": "Select the cipher suites that can be used for SSL perfect forward secrecy (PFS). Applies to both client and server sessions.",
    "ssl-min-version": "Lowest SSL/TLS version acceptable from a client.",
    "ssl-max-version": "Highest SSL/TLS version acceptable from a client.",
    "ssl-server-min-version": "Lowest SSL/TLS version acceptable from a server. Use the client setting by default.",
    "ssl-server-max-version": "Highest SSL/TLS version acceptable from a server. Use the client setting by default.",
    "ssl-accept-ffdhe-groups": "Enable/disable FFDHE cipher suite for SSL key exchange.",
    "ssl-send-empty-frags": "Enable/disable sending empty fragments to avoid CBC IV attacks (SSL 3.0 & TLS 1.0 only). May need to be disabled for compatibility with older systems.",
    "ssl-client-fallback": "Enable/disable support for preventing Downgrade Attacks on client connections (RFC 7507).",
    "ssl-client-renegotiation": "Allow, deny, or require secure renegotiation of client sessions to comply with RFC 5746.",
    "ssl-client-session-state-type": "How to expire SSL sessions for the segment of the SSL connection between the client and the FortiGate.",
    "ssl-client-session-state-timeout": "Number of minutes to keep client to FortiGate SSL session state.",
    "ssl-client-session-state-max": "Maximum number of client to FortiGate SSL session states to keep.",
    "ssl-client-rekey-count": "Maximum length of data in MB before triggering a client rekey (0 = disable).",
    "ssl-server-renegotiation": "Enable/disable secure renegotiation to comply with RFC 5746.",
    "ssl-server-session-state-type": "How to expire SSL sessions for the segment of the SSL connection between the server and the FortiGate.",
    "ssl-server-session-state-timeout": "Number of minutes to keep FortiGate to Server SSL session state.",
    "ssl-server-session-state-max": "Maximum number of FortiGate to Server SSL session states to keep.",
    "ssl-http-location-conversion": "Enable to replace HTTP with HTTPS in the reply's Location HTTP header field.",
    "ssl-http-match-host": "Enable/disable HTTP host matching for location conversion.",
    "ssl-hpkp": "Enable/disable including HPKP header in response.",
    "ssl-hpkp-primary": "Certificate to generate primary HPKP pin from.",
    "ssl-hpkp-backup": "Certificate to generate backup HPKP pin from.",
    "ssl-hpkp-age": "Number of seconds the client should honor the HPKP setting.",
    "ssl-hpkp-report-uri": "URL to report HPKP violations to.",
    "ssl-hpkp-include-subdomains": "Indicate that HPKP header applies to all subdomains.",
    "ssl-hsts": "Enable/disable including HSTS header in response.",
    "ssl-hsts-age": "Number of seconds the client should honor the HSTS setting.",
    "ssl-hsts-include-subdomains": "Indicate that HSTS header applies to all subdomains.",
    "monitor": "Name of the health check monitor to use when polling to determine a virtual server's connectivity status.",
    "max-embryonic-connections": "Maximum number of incomplete connections.",
    "color": "Color of icon on the GUI.",
    "ipv6-mappedip": "Range of mapped IPv6 addresses. Specify the start IPv6 address followed by a space and the end IPv6 address.",
    "ipv6-mappedport": "IPv6 port number range on the destination network to which the external port number range is mapped.",
    "one-click-gslb-server": "Enable/disable one click GSLB server integration with FortiGSLB.",
    "gslb-hostname": "Hostname to use within the configured FortiGSLB domain.",
    "gslb-domain-name": "Domain to use when integrating with FortiGSLB.",
    "gslb-public-ips": "Publicly accessible IP addresses for the FortiGSLB service.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "name": {"type": "string", "max_length": 79},
    "id": {"type": "integer", "min": 0, "max": 65535},
    "dns-mapping-ttl": {"type": "integer", "min": 0, "max": 604800},
    "mapped-addr": {"type": "string", "max_length": 79},
    "extintf": {"type": "string", "max_length": 35},
    "gratuitous-arp-interval": {"type": "integer", "min": 5, "max": 8640000},
    "http-cookie-domain": {"type": "string", "max_length": 35},
    "http-cookie-path": {"type": "string", "max_length": 35},
    "http-cookie-generation": {"type": "integer", "min": 0, "max": 4294967295},
    "http-cookie-age": {"type": "integer", "min": 0, "max": 525600},
    "http-multiplex-ttl": {"type": "integer", "min": 0, "max": 2147483647},
    "http-multiplex-max-request": {"type": "integer", "min": 0, "max": 2147483647},
    "http-multiplex-max-concurrent-request": {"type": "integer", "min": 0, "max": 2147483647},
    "http-ip-header-name": {"type": "string", "max_length": 35},
    "ssl-client-session-state-timeout": {"type": "integer", "min": 1, "max": 14400},
    "ssl-client-session-state-max": {"type": "integer", "min": 1, "max": 10000},
    "ssl-client-rekey-count": {"type": "integer", "min": 200, "max": 1048576},
    "ssl-server-session-state-timeout": {"type": "integer", "min": 1, "max": 14400},
    "ssl-server-session-state-max": {"type": "integer", "min": 1, "max": 10000},
    "ssl-hpkp-primary": {"type": "string", "max_length": 79},
    "ssl-hpkp-backup": {"type": "string", "max_length": 79},
    "ssl-hpkp-age": {"type": "integer", "min": 60, "max": 157680000},
    "ssl-hsts-age": {"type": "integer", "min": 60, "max": 157680000},
    "max-embryonic-connections": {"type": "integer", "min": 0, "max": 100000},
    "color": {"type": "integer", "min": 0, "max": 32},
    "gslb-hostname": {"type": "string", "max_length": 35},
    "gslb-domain-name": {"type": "string", "max_length": 255},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "src-filter": {
        "range": {
            "type": "string",
            "help": "Source-filter range.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "service": {
        "name": {
            "type": "string",
            "help": "Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "extaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "quic": {
        "max-idle-timeout": {
            "type": "integer",
            "help": "Maximum idle timeout milliseconds (1 - 60000, default = 30000).",
            "default": 30000,
            "min_value": 1,
            "max_value": 60000,
        },
        "max-udp-payload-size": {
            "type": "integer",
            "help": "Maximum UDP payload size in bytes (1200 - 1500, default = 1500).",
            "default": 1500,
            "min_value": 1200,
            "max_value": 1500,
        },
        "active-connection-id-limit": {
            "type": "integer",
            "help": "Active connection ID limit (1 - 8, default = 2).",
            "default": 2,
            "min_value": 1,
            "max_value": 8,
        },
        "ack-delay-exponent": {
            "type": "integer",
            "help": "ACK delay exponent (1 - 20, default = 3).",
            "default": 3,
            "min_value": 1,
            "max_value": 20,
        },
        "max-ack-delay": {
            "type": "integer",
            "help": "Maximum ACK delay in milliseconds (1 - 16383, default = 25).",
            "default": 25,
            "min_value": 1,
            "max_value": 16383,
        },
        "max-datagram-frame-size": {
            "type": "integer",
            "help": "Maximum datagram frame size in bytes (1 - 1500, default = 1500).",
            "default": 1500,
            "min_value": 1,
            "max_value": 1500,
        },
        "active-migration": {
            "type": "option",
            "help": "Enable/disable active migration (default = disable).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "grease-quic-bit": {
            "type": "option",
            "help": "Enable/disable grease QUIC bit (default = enable).",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "mappedip": {
        "range": {
            "type": "string",
            "help": "Mapped IP range.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "srcintf-filter": {
        "interface-name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "realservers": {
        "id": {
            "type": "integer",
            "help": "Real server ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "type": {
            "type": "option",
            "help": "Type of address.",
            "required": True,
            "default": "ip",
            "options": ["ip", "address"],
        },
        "address": {
            "type": "string",
            "help": "Dynamic address of the real server.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
        "ip": {
            "type": "user",
            "help": "IP address of the real server.",
            "required": True,
            "default": "",
        },
        "port": {
            "type": "integer",
            "help": "Port for communicating with the real server. Required if port forwarding is enabled.",
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
        "status": {
            "type": "option",
            "help": "Set the status of the real server to active so that it can accept traffic, or on standby or disabled so no traffic is sent.",
            "default": "active",
            "options": ["active", "standby", "disable"],
        },
        "weight": {
            "type": "integer",
            "help": "Weight of the real server. If weighted load balancing is enabled, the server with the highest weight gets more connections.",
            "default": 1,
            "min_value": 1,
            "max_value": 255,
        },
        "holddown-interval": {
            "type": "integer",
            "help": "Time in seconds that the system waits before re-activating a previously down active server in the active-standby mode. This is to prevent any flapping issues.",
            "default": 300,
            "min_value": 30,
            "max_value": 65535,
        },
        "healthcheck": {
            "type": "option",
            "help": "Enable to check the responsiveness of the real server before forwarding traffic.",
            "default": "vip",
            "options": ["disable", "enable", "vip"],
        },
        "http-host": {
            "type": "string",
            "help": "HTTP server domain name in HTTP header.",
            "default": "",
            "max_length": 63,
        },
        "translate-host": {
            "type": "option",
            "help": "Enable/disable translation of hostname/IP from virtual server to real server.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "max-connections": {
            "type": "integer",
            "help": "Max number of active connections that can be directed to the real server. When reached, sessions are sent to other real servers.",
            "default": 0,
            "min_value": 0,
            "max_value": 2147483647,
        },
        "monitor": {
            "type": "string",
            "help": "Name of the health check monitor to use when polling to determine a virtual server's connectivity status.",
        },
        "client-ip": {
            "type": "user",
            "help": "Only clients in this IP range can connect to this real server.",
            "default": "",
        },
        "verify-cert": {
            "type": "option",
            "help": "Enable/disable certificate verification of the real server.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
    },
    "ssl-certificate": {
        "name": {
            "type": "string",
            "help": "Certificate list.",
            "default": "",
            "max_length": 79,
        },
    },
    "ssl-cipher-suites": {
        "priority": {
            "type": "integer",
            "help": "SSL/TLS cipher suites priority.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "cipher": {
            "type": "option",
            "help": "Cipher suite name.",
            "required": True,
            "default": "",
            "options": ["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"],
        },
        "versions": {
            "type": "option",
            "help": "SSL/TLS versions that the cipher suite can be used with.",
            "default": "ssl-3.0 tls-1.0 tls-1.1 tls-1.2 tls-1.3",
            "options": ["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
    },
    "ssl-server-cipher-suites": {
        "priority": {
            "type": "integer",
            "help": "SSL/TLS cipher suites priority.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "cipher": {
            "type": "option",
            "help": "Cipher suite name.",
            "required": True,
            "default": "",
            "options": ["TLS-AES-128-GCM-SHA256", "TLS-AES-256-GCM-SHA384", "TLS-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA", "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256", "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA", "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256", "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256", "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA", "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-AES-128-CBC-SHA", "TLS-RSA-WITH-AES-256-CBC-SHA", "TLS-RSA-WITH-AES-128-CBC-SHA256", "TLS-RSA-WITH-AES-128-GCM-SHA256", "TLS-RSA-WITH-AES-256-CBC-SHA256", "TLS-RSA-WITH-AES-256-GCM-SHA384", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA", "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256", "TLS-DHE-RSA-WITH-SEED-CBC-SHA", "TLS-DHE-DSS-WITH-SEED-CBC-SHA", "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256", "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384", "TLS-RSA-WITH-SEED-CBC-SHA", "TLS-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256", "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384", "TLS-ECDHE-RSA-WITH-RC4-128-SHA", "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-3DES-EDE-CBC-SHA", "TLS-RSA-WITH-RC4-128-MD5", "TLS-RSA-WITH-RC4-128-SHA", "TLS-DHE-RSA-WITH-DES-CBC-SHA", "TLS-DHE-DSS-WITH-DES-CBC-SHA", "TLS-RSA-WITH-DES-CBC-SHA"],
        },
        "versions": {
            "type": "option",
            "help": "SSL/TLS versions that the cipher suite can be used with.",
            "default": "ssl-3.0 tls-1.0 tls-1.1 tls-1.2 tls-1.3",
            "options": ["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"],
        },
    },
    "monitor": {
        "name": {
            "type": "string",
            "help": "Health monitor name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "gslb-public-ips": {
        "index": {
            "type": "integer",
            "help": "Index of this public IP setting.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "ip": {
            "type": "ipv4-address-any",
            "help": "The publicly accessible IP address.",
            "default": "0.0.0.0",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_TYPE = [
    "static-nat",
    "load-balance",
    "server-load-balance",
    "dns-translation",
    "fqdn",
    "access-proxy",
]
VALID_BODY_SERVER_TYPE = [
    "http",
    "https",
    "imaps",
    "pop3s",
    "smtps",
    "ssl",
    "tcp",
    "udp",
    "ip",
]
VALID_BODY_LDB_METHOD = [
    "static",
    "round-robin",
    "weighted",
    "least-session",
    "least-rtt",
    "first-alive",
    "http-host",
]
VALID_BODY_SRC_VIP_FILTER = [
    "disable",
    "enable",
]
VALID_BODY_H2_SUPPORT = [
    "enable",
    "disable",
]
VALID_BODY_H3_SUPPORT = [
    "enable",
    "disable",
]
VALID_BODY_NAT44 = [
    "disable",
    "enable",
]
VALID_BODY_NAT46 = [
    "disable",
    "enable",
]
VALID_BODY_ADD_NAT46_ROUTE = [
    "disable",
    "enable",
]
VALID_BODY_ARP_REPLY = [
    "disable",
    "enable",
]
VALID_BODY_HTTP_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_PERSISTENCE = [
    "none",
    "http-cookie",
    "ssl-session-id",
]
VALID_BODY_NAT_SOURCE_VIP = [
    "disable",
    "enable",
]
VALID_BODY_PORTFORWARD = [
    "disable",
    "enable",
]
VALID_BODY_STATUS = [
    "disable",
    "enable",
]
VALID_BODY_PROTOCOL = [
    "tcp",
    "udp",
    "sctp",
    "icmp",
]
VALID_BODY_PORTMAPPING_TYPE = [
    "1-to-1",
    "m-to-n",
]
VALID_BODY_EMPTY_CERT_ACTION = [
    "accept",
    "block",
    "accept-unmanageable",
]
VALID_BODY_USER_AGENT_DETECT = [
    "disable",
    "enable",
]
VALID_BODY_CLIENT_CERT = [
    "disable",
    "enable",
]
VALID_BODY_HTTP_COOKIE_DOMAIN_FROM_HOST = [
    "disable",
    "enable",
]
VALID_BODY_HTTP_COOKIE_SHARE = [
    "disable",
    "same-ip",
]
VALID_BODY_HTTPS_COOKIE_SECURE = [
    "disable",
    "enable",
]
VALID_BODY_HTTP_MULTIPLEX = [
    "enable",
    "disable",
]
VALID_BODY_HTTP_IP_HEADER = [
    "enable",
    "disable",
]
VALID_BODY_OUTLOOK_WEB_ACCESS = [
    "disable",
    "enable",
]
VALID_BODY_WEBLOGIC_SERVER = [
    "disable",
    "enable",
]
VALID_BODY_WEBSPHERE_SERVER = [
    "disable",
    "enable",
]
VALID_BODY_SSL_MODE = [
    "half",
    "full",
]
VALID_BODY_SSL_DH_BITS = [
    "768",
    "1024",
    "1536",
    "2048",
    "3072",
    "4096",
]
VALID_BODY_SSL_ALGORITHM = [
    "high",
    "medium",
    "low",
    "custom",
]
VALID_BODY_SSL_SERVER_ALGORITHM = [
    "high",
    "medium",
    "low",
    "custom",
    "client",
]
VALID_BODY_SSL_PFS = [
    "require",
    "deny",
    "allow",
]
VALID_BODY_SSL_MIN_VERSION = [
    "ssl-3.0",
    "tls-1.0",
    "tls-1.1",
    "tls-1.2",
    "tls-1.3",
]
VALID_BODY_SSL_MAX_VERSION = [
    "ssl-3.0",
    "tls-1.0",
    "tls-1.1",
    "tls-1.2",
    "tls-1.3",
]
VALID_BODY_SSL_SERVER_MIN_VERSION = [
    "ssl-3.0",
    "tls-1.0",
    "tls-1.1",
    "tls-1.2",
    "tls-1.3",
    "client",
]
VALID_BODY_SSL_SERVER_MAX_VERSION = [
    "ssl-3.0",
    "tls-1.0",
    "tls-1.1",
    "tls-1.2",
    "tls-1.3",
    "client",
]
VALID_BODY_SSL_ACCEPT_FFDHE_GROUPS = [
    "enable",
    "disable",
]
VALID_BODY_SSL_SEND_EMPTY_FRAGS = [
    "enable",
    "disable",
]
VALID_BODY_SSL_CLIENT_FALLBACK = [
    "disable",
    "enable",
]
VALID_BODY_SSL_CLIENT_RENEGOTIATION = [
    "allow",
    "deny",
    "secure",
]
VALID_BODY_SSL_CLIENT_SESSION_STATE_TYPE = [
    "disable",
    "time",
    "count",
    "both",
]
VALID_BODY_SSL_SERVER_RENEGOTIATION = [
    "enable",
    "disable",
]
VALID_BODY_SSL_SERVER_SESSION_STATE_TYPE = [
    "disable",
    "time",
    "count",
    "both",
]
VALID_BODY_SSL_HTTP_LOCATION_CONVERSION = [
    "enable",
    "disable",
]
VALID_BODY_SSL_HTTP_MATCH_HOST = [
    "enable",
    "disable",
]
VALID_BODY_SSL_HPKP = [
    "disable",
    "enable",
    "report-only",
]
VALID_BODY_SSL_HPKP_INCLUDE_SUBDOMAINS = [
    "disable",
    "enable",
]
VALID_BODY_SSL_HSTS = [
    "disable",
    "enable",
]
VALID_BODY_SSL_HSTS_INCLUDE_SUBDOMAINS = [
    "disable",
    "enable",
]
VALID_BODY_ONE_CLICK_GSLB_SERVER = [
    "disable",
    "enable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_vip_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/vip."""
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


def validate_firewall_vip_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/vip object."""
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
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldb-method" in payload:
        is_valid, error = _validate_enum_field(
            "ldb-method",
            payload["ldb-method"],
            VALID_BODY_LDB_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-vip-filter" in payload:
        is_valid, error = _validate_enum_field(
            "src-vip-filter",
            payload["src-vip-filter"],
            VALID_BODY_SRC_VIP_FILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h2-support" in payload:
        is_valid, error = _validate_enum_field(
            "h2-support",
            payload["h2-support"],
            VALID_BODY_H2_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h3-support" in payload:
        is_valid, error = _validate_enum_field(
            "h3-support",
            payload["h3-support"],
            VALID_BODY_H3_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat44" in payload:
        is_valid, error = _validate_enum_field(
            "nat44",
            payload["nat44"],
            VALID_BODY_NAT44,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46" in payload:
        is_valid, error = _validate_enum_field(
            "nat46",
            payload["nat46"],
            VALID_BODY_NAT46,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-nat46-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-nat46-route",
            payload["add-nat46-route"],
            VALID_BODY_ADD_NAT46_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "arp-reply" in payload:
        is_valid, error = _validate_enum_field(
            "arp-reply",
            payload["arp-reply"],
            VALID_BODY_ARP_REPLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "http-redirect",
            payload["http-redirect"],
            VALID_BODY_HTTP_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "persistence" in payload:
        is_valid, error = _validate_enum_field(
            "persistence",
            payload["persistence"],
            VALID_BODY_PERSISTENCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat-source-vip" in payload:
        is_valid, error = _validate_enum_field(
            "nat-source-vip",
            payload["nat-source-vip"],
            VALID_BODY_NAT_SOURCE_VIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "portforward" in payload:
        is_valid, error = _validate_enum_field(
            "portforward",
            payload["portforward"],
            VALID_BODY_PORTFORWARD,
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
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "portmapping-type" in payload:
        is_valid, error = _validate_enum_field(
            "portmapping-type",
            payload["portmapping-type"],
            VALID_BODY_PORTMAPPING_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "empty-cert-action" in payload:
        is_valid, error = _validate_enum_field(
            "empty-cert-action",
            payload["empty-cert-action"],
            VALID_BODY_EMPTY_CERT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-agent-detect" in payload:
        is_valid, error = _validate_enum_field(
            "user-agent-detect",
            payload["user-agent-detect"],
            VALID_BODY_USER_AGENT_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert",
            payload["client-cert"],
            VALID_BODY_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-cookie-domain-from-host" in payload:
        is_valid, error = _validate_enum_field(
            "http-cookie-domain-from-host",
            payload["http-cookie-domain-from-host"],
            VALID_BODY_HTTP_COOKIE_DOMAIN_FROM_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-cookie-share" in payload:
        is_valid, error = _validate_enum_field(
            "http-cookie-share",
            payload["http-cookie-share"],
            VALID_BODY_HTTP_COOKIE_SHARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-cookie-secure" in payload:
        is_valid, error = _validate_enum_field(
            "https-cookie-secure",
            payload["https-cookie-secure"],
            VALID_BODY_HTTPS_COOKIE_SECURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-multiplex" in payload:
        is_valid, error = _validate_enum_field(
            "http-multiplex",
            payload["http-multiplex"],
            VALID_BODY_HTTP_MULTIPLEX,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-ip-header" in payload:
        is_valid, error = _validate_enum_field(
            "http-ip-header",
            payload["http-ip-header"],
            VALID_BODY_HTTP_IP_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outlook-web-access" in payload:
        is_valid, error = _validate_enum_field(
            "outlook-web-access",
            payload["outlook-web-access"],
            VALID_BODY_OUTLOOK_WEB_ACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "weblogic-server" in payload:
        is_valid, error = _validate_enum_field(
            "weblogic-server",
            payload["weblogic-server"],
            VALID_BODY_WEBLOGIC_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "websphere-server" in payload:
        is_valid, error = _validate_enum_field(
            "websphere-server",
            payload["websphere-server"],
            VALID_BODY_WEBSPHERE_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-mode",
            payload["ssl-mode"],
            VALID_BODY_SSL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-dh-bits" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-dh-bits",
            payload["ssl-dh-bits"],
            VALID_BODY_SSL_DH_BITS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-algorithm",
            payload["ssl-algorithm"],
            VALID_BODY_SSL_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-algorithm",
            payload["ssl-server-algorithm"],
            VALID_BODY_SSL_SERVER_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-pfs" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-pfs",
            payload["ssl-pfs"],
            VALID_BODY_SSL_PFS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-version",
            payload["ssl-min-version"],
            VALID_BODY_SSL_MIN_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-max-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-max-version",
            payload["ssl-max-version"],
            VALID_BODY_SSL_MAX_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-min-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-min-version",
            payload["ssl-server-min-version"],
            VALID_BODY_SSL_SERVER_MIN_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-max-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-max-version",
            payload["ssl-server-max-version"],
            VALID_BODY_SSL_SERVER_MAX_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-accept-ffdhe-groups" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-accept-ffdhe-groups",
            payload["ssl-accept-ffdhe-groups"],
            VALID_BODY_SSL_ACCEPT_FFDHE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-send-empty-frags" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-send-empty-frags",
            payload["ssl-send-empty-frags"],
            VALID_BODY_SSL_SEND_EMPTY_FRAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-client-fallback" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-fallback",
            payload["ssl-client-fallback"],
            VALID_BODY_SSL_CLIENT_FALLBACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-client-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-renegotiation",
            payload["ssl-client-renegotiation"],
            VALID_BODY_SSL_CLIENT_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-client-session-state-type" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-session-state-type",
            payload["ssl-client-session-state-type"],
            VALID_BODY_SSL_CLIENT_SESSION_STATE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-renegotiation",
            payload["ssl-server-renegotiation"],
            VALID_BODY_SSL_SERVER_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-session-state-type" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-session-state-type",
            payload["ssl-server-session-state-type"],
            VALID_BODY_SSL_SERVER_SESSION_STATE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-http-location-conversion" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-http-location-conversion",
            payload["ssl-http-location-conversion"],
            VALID_BODY_SSL_HTTP_LOCATION_CONVERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-http-match-host" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-http-match-host",
            payload["ssl-http-match-host"],
            VALID_BODY_SSL_HTTP_MATCH_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hpkp" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hpkp",
            payload["ssl-hpkp"],
            VALID_BODY_SSL_HPKP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hpkp-include-subdomains" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hpkp-include-subdomains",
            payload["ssl-hpkp-include-subdomains"],
            VALID_BODY_SSL_HPKP_INCLUDE_SUBDOMAINS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hsts" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hsts",
            payload["ssl-hsts"],
            VALID_BODY_SSL_HSTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hsts-include-subdomains" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hsts-include-subdomains",
            payload["ssl-hsts-include-subdomains"],
            VALID_BODY_SSL_HSTS_INCLUDE_SUBDOMAINS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "one-click-gslb-server" in payload:
        is_valid, error = _validate_enum_field(
            "one-click-gslb-server",
            payload["one-click-gslb-server"],
            VALID_BODY_ONE_CLICK_GSLB_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_vip_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/vip."""
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
    if "server-type" in payload:
        is_valid, error = _validate_enum_field(
            "server-type",
            payload["server-type"],
            VALID_BODY_SERVER_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ldb-method" in payload:
        is_valid, error = _validate_enum_field(
            "ldb-method",
            payload["ldb-method"],
            VALID_BODY_LDB_METHOD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "src-vip-filter" in payload:
        is_valid, error = _validate_enum_field(
            "src-vip-filter",
            payload["src-vip-filter"],
            VALID_BODY_SRC_VIP_FILTER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h2-support" in payload:
        is_valid, error = _validate_enum_field(
            "h2-support",
            payload["h2-support"],
            VALID_BODY_H2_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "h3-support" in payload:
        is_valid, error = _validate_enum_field(
            "h3-support",
            payload["h3-support"],
            VALID_BODY_H3_SUPPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat44" in payload:
        is_valid, error = _validate_enum_field(
            "nat44",
            payload["nat44"],
            VALID_BODY_NAT44,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat46" in payload:
        is_valid, error = _validate_enum_field(
            "nat46",
            payload["nat46"],
            VALID_BODY_NAT46,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "add-nat46-route" in payload:
        is_valid, error = _validate_enum_field(
            "add-nat46-route",
            payload["add-nat46-route"],
            VALID_BODY_ADD_NAT46_ROUTE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "arp-reply" in payload:
        is_valid, error = _validate_enum_field(
            "arp-reply",
            payload["arp-reply"],
            VALID_BODY_ARP_REPLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "http-redirect",
            payload["http-redirect"],
            VALID_BODY_HTTP_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "persistence" in payload:
        is_valid, error = _validate_enum_field(
            "persistence",
            payload["persistence"],
            VALID_BODY_PERSISTENCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat-source-vip" in payload:
        is_valid, error = _validate_enum_field(
            "nat-source-vip",
            payload["nat-source-vip"],
            VALID_BODY_NAT_SOURCE_VIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "portforward" in payload:
        is_valid, error = _validate_enum_field(
            "portforward",
            payload["portforward"],
            VALID_BODY_PORTFORWARD,
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
    if "protocol" in payload:
        is_valid, error = _validate_enum_field(
            "protocol",
            payload["protocol"],
            VALID_BODY_PROTOCOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "portmapping-type" in payload:
        is_valid, error = _validate_enum_field(
            "portmapping-type",
            payload["portmapping-type"],
            VALID_BODY_PORTMAPPING_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "empty-cert-action" in payload:
        is_valid, error = _validate_enum_field(
            "empty-cert-action",
            payload["empty-cert-action"],
            VALID_BODY_EMPTY_CERT_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "user-agent-detect" in payload:
        is_valid, error = _validate_enum_field(
            "user-agent-detect",
            payload["user-agent-detect"],
            VALID_BODY_USER_AGENT_DETECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "client-cert" in payload:
        is_valid, error = _validate_enum_field(
            "client-cert",
            payload["client-cert"],
            VALID_BODY_CLIENT_CERT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-cookie-domain-from-host" in payload:
        is_valid, error = _validate_enum_field(
            "http-cookie-domain-from-host",
            payload["http-cookie-domain-from-host"],
            VALID_BODY_HTTP_COOKIE_DOMAIN_FROM_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-cookie-share" in payload:
        is_valid, error = _validate_enum_field(
            "http-cookie-share",
            payload["http-cookie-share"],
            VALID_BODY_HTTP_COOKIE_SHARE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "https-cookie-secure" in payload:
        is_valid, error = _validate_enum_field(
            "https-cookie-secure",
            payload["https-cookie-secure"],
            VALID_BODY_HTTPS_COOKIE_SECURE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-multiplex" in payload:
        is_valid, error = _validate_enum_field(
            "http-multiplex",
            payload["http-multiplex"],
            VALID_BODY_HTTP_MULTIPLEX,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-ip-header" in payload:
        is_valid, error = _validate_enum_field(
            "http-ip-header",
            payload["http-ip-header"],
            VALID_BODY_HTTP_IP_HEADER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outlook-web-access" in payload:
        is_valid, error = _validate_enum_field(
            "outlook-web-access",
            payload["outlook-web-access"],
            VALID_BODY_OUTLOOK_WEB_ACCESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "weblogic-server" in payload:
        is_valid, error = _validate_enum_field(
            "weblogic-server",
            payload["weblogic-server"],
            VALID_BODY_WEBLOGIC_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "websphere-server" in payload:
        is_valid, error = _validate_enum_field(
            "websphere-server",
            payload["websphere-server"],
            VALID_BODY_WEBSPHERE_SERVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-mode" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-mode",
            payload["ssl-mode"],
            VALID_BODY_SSL_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-dh-bits" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-dh-bits",
            payload["ssl-dh-bits"],
            VALID_BODY_SSL_DH_BITS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-algorithm",
            payload["ssl-algorithm"],
            VALID_BODY_SSL_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-algorithm" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-algorithm",
            payload["ssl-server-algorithm"],
            VALID_BODY_SSL_SERVER_ALGORITHM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-pfs" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-pfs",
            payload["ssl-pfs"],
            VALID_BODY_SSL_PFS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-min-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-min-version",
            payload["ssl-min-version"],
            VALID_BODY_SSL_MIN_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-max-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-max-version",
            payload["ssl-max-version"],
            VALID_BODY_SSL_MAX_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-min-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-min-version",
            payload["ssl-server-min-version"],
            VALID_BODY_SSL_SERVER_MIN_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-max-version" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-max-version",
            payload["ssl-server-max-version"],
            VALID_BODY_SSL_SERVER_MAX_VERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-accept-ffdhe-groups" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-accept-ffdhe-groups",
            payload["ssl-accept-ffdhe-groups"],
            VALID_BODY_SSL_ACCEPT_FFDHE_GROUPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-send-empty-frags" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-send-empty-frags",
            payload["ssl-send-empty-frags"],
            VALID_BODY_SSL_SEND_EMPTY_FRAGS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-client-fallback" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-fallback",
            payload["ssl-client-fallback"],
            VALID_BODY_SSL_CLIENT_FALLBACK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-client-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-renegotiation",
            payload["ssl-client-renegotiation"],
            VALID_BODY_SSL_CLIENT_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-client-session-state-type" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-client-session-state-type",
            payload["ssl-client-session-state-type"],
            VALID_BODY_SSL_CLIENT_SESSION_STATE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-renegotiation" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-renegotiation",
            payload["ssl-server-renegotiation"],
            VALID_BODY_SSL_SERVER_RENEGOTIATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-server-session-state-type" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-server-session-state-type",
            payload["ssl-server-session-state-type"],
            VALID_BODY_SSL_SERVER_SESSION_STATE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-http-location-conversion" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-http-location-conversion",
            payload["ssl-http-location-conversion"],
            VALID_BODY_SSL_HTTP_LOCATION_CONVERSION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-http-match-host" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-http-match-host",
            payload["ssl-http-match-host"],
            VALID_BODY_SSL_HTTP_MATCH_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hpkp" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hpkp",
            payload["ssl-hpkp"],
            VALID_BODY_SSL_HPKP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hpkp-include-subdomains" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hpkp-include-subdomains",
            payload["ssl-hpkp-include-subdomains"],
            VALID_BODY_SSL_HPKP_INCLUDE_SUBDOMAINS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hsts" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hsts",
            payload["ssl-hsts"],
            VALID_BODY_SSL_HSTS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssl-hsts-include-subdomains" in payload:
        is_valid, error = _validate_enum_field(
            "ssl-hsts-include-subdomains",
            payload["ssl-hsts-include-subdomains"],
            VALID_BODY_SSL_HSTS_INCLUDE_SUBDOMAINS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "one-click-gslb-server" in payload:
        is_valid, error = _validate_enum_field(
            "one-click-gslb-server",
            payload["one-click-gslb-server"],
            VALID_BODY_ONE_CLICK_GSLB_SERVER,
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
    "endpoint": "firewall/vip",
    "category": "cmdb",
    "api_path": "firewall/vip",
    "mkey": "name",
    "mkey_type": "string",
    "help": "Configure virtual IP for IPv4.",
    "total_fields": 98,
    "required_fields_count": 7,
    "fields_with_defaults_count": 84,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
