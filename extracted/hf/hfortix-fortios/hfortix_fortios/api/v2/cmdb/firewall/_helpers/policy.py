"""Validation helpers for firewall/policy - Auto-generated"""

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
    "srcintf",  # Incoming (ingress) interface.
    "dstintf",  # Outgoing (egress) interface.
    "schedule",  # Schedule name.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "policyid": 0,
    "status": "enable",
    "name": "",
    "uuid": "00000000-0000-0000-0000-000000000000",
    "action": "deny",
    "nat64": "disable",
    "nat46": "disable",
    "ztna-status": "disable",
    "ztna-device-ownership": "disable",
    "ztna-tags-match-logic": "or",
    "internet-service": "disable",
    "internet-service-src": "disable",
    "reputation-minimum": 0,
    "reputation-direction": "destination",
    "internet-service6": "disable",
    "internet-service6-src": "disable",
    "reputation-minimum6": 0,
    "reputation-direction6": "destination",
    "rtp-nat": "disable",
    "send-deny-packet": "disable",
    "firewall-session-dirty": "check-all",
    "schedule": "",
    "schedule-timeout": "disable",
    "policy-expiry": "disable",
    "policy-expiry-date": "0000-00-00 00:00:00",
    "policy-expiry-date-utc": "",
    "tos-mask": "",
    "tos": "",
    "tos-negate": "disable",
    "anti-replay": "enable",
    "tcp-session-without-syn": "disable",
    "geoip-anycast": "disable",
    "geoip-match": "physical-location",
    "dynamic-shaping": "disable",
    "passive-wan-health-measurement": "disable",
    "app-monitor": "disable",
    "utm-status": "disable",
    "inspection-mode": "flow",
    "http-policy-redirect": "disable",
    "ssh-policy-redirect": "disable",
    "ztna-policy-redirect": "disable",
    "webproxy-profile": "",
    "profile-type": "single",
    "profile-group": "",
    "profile-protocol-options": "default",
    "ssl-ssh-profile": "no-inspection",
    "av-profile": "",
    "webfilter-profile": "",
    "dnsfilter-profile": "",
    "emailfilter-profile": "",
    "dlp-profile": "",
    "file-filter-profile": "",
    "ips-sensor": "",
    "application-list": "",
    "voip-profile": "",
    "ips-voip-filter": "",
    "sctp-filter-profile": "",
    "diameter-filter-profile": "",
    "virtual-patch-profile": "",
    "icap-profile": "",
    "videofilter-profile": "",
    "waf-profile": "",
    "ssh-filter-profile": "",
    "casb-profile": "",
    "logtraffic": "utm",
    "logtraffic-start": "disable",
    "log-http-transaction": "disable",
    "capture-packet": "disable",
    "auto-asic-offload": "enable",
    "wanopt": "disable",
    "wanopt-detection": "active",
    "wanopt-passive-opt": "default",
    "wanopt-profile": "",
    "wanopt-peer": "",
    "webcache": "disable",
    "webcache-https": "disable",
    "webproxy-forward-server": "",
    "traffic-shaper": "",
    "traffic-shaper-reverse": "",
    "per-ip-shaper": "",
    "nat": "disable",
    "pcp-outbound": "disable",
    "pcp-inbound": "disable",
    "permit-any-host": "disable",
    "permit-stun-host": "disable",
    "fixedport": "disable",
    "port-preserve": "enable",
    "port-random": "disable",
    "ippool": "disable",
    "session-ttl": "",
    "vlan-cos-fwd": 255,
    "vlan-cos-rev": 255,
    "inbound": "disable",
    "outbound": "enable",
    "natinbound": "disable",
    "natoutbound": "disable",
    "fec": "disable",
    "wccp": "disable",
    "ntlm": "disable",
    "ntlm-guest": "disable",
    "fsso-agent-for-ntlm": "",
    "auth-path": "disable",
    "disclaimer": "disable",
    "email-collect": "disable",
    "vpntunnel": "",
    "natip": "0.0.0.0 0.0.0.0",
    "match-vip": "enable",
    "match-vip-only": "disable",
    "diffserv-copy": "disable",
    "diffserv-forward": "disable",
    "diffserv-reverse": "disable",
    "diffservcode-forward": "",
    "diffservcode-rev": "",
    "tcp-mss-sender": 0,
    "tcp-mss-receiver": 0,
    "auth-cert": "",
    "auth-redirect-addr": "",
    "identity-based-route": "",
    "block-notification": "disable",
    "replacemsg-override-group": "",
    "srcaddr-negate": "disable",
    "srcaddr6-negate": "disable",
    "dstaddr-negate": "disable",
    "dstaddr6-negate": "disable",
    "ztna-ems-tag-negate": "disable",
    "service-negate": "disable",
    "internet-service-negate": "disable",
    "internet-service-src-negate": "disable",
    "internet-service6-negate": "disable",
    "internet-service6-src-negate": "disable",
    "timeout-send-rst": "disable",
    "captive-portal-exempt": "disable",
    "decrypted-traffic-mirror": "",
    "dsri": "disable",
    "radius-mac-auth-bypass": "disable",
    "radius-ip-auth-bypass": "disable",
    "delay-tcp-npu-session": "disable",
    "vlan-filter": "",
    "sgt-check": "disable",
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
    "policyid": "integer",  # Policy ID (0 - 4294967294).
    "status": "option",  # Enable or disable this policy.
    "name": "string",  # Policy name.
    "uuid": "uuid",  # Universally Unique Identifier (UUID; automatically assigned 
    "srcintf": "string",  # Incoming (ingress) interface.
    "dstintf": "string",  # Outgoing (egress) interface.
    "action": "option",  # Policy action (accept/deny/ipsec).
    "nat64": "option",  # Enable/disable NAT64.
    "nat46": "option",  # Enable/disable NAT46.
    "ztna-status": "option",  # Enable/disable zero trust access.
    "ztna-device-ownership": "option",  # Enable/disable zero trust device ownership.
    "srcaddr": "string",  # Source IPv4 address and address group names.
    "dstaddr": "string",  # Destination IPv4 address and address group names.
    "srcaddr6": "string",  # Source IPv6 address name and address group names.
    "dstaddr6": "string",  # Destination IPv6 address name and address group names.
    "ztna-ems-tag": "string",  # Source ztna-ems-tag names.
    "ztna-ems-tag-secondary": "string",  # Source ztna-ems-tag-secondary names.
    "ztna-tags-match-logic": "option",  # ZTNA tag matching logic.
    "ztna-geo-tag": "string",  # Source ztna-geo-tag names.
    "internet-service": "option",  # Enable/disable use of Internet Services for this policy. If 
    "internet-service-name": "string",  # Internet Service name.
    "internet-service-group": "string",  # Internet Service group name.
    "internet-service-custom": "string",  # Custom Internet Service name.
    "network-service-dynamic": "string",  # Dynamic Network Service name.
    "internet-service-custom-group": "string",  # Custom Internet Service group name.
    "internet-service-src": "option",  # Enable/disable use of Internet Services in source for this p
    "internet-service-src-name": "string",  # Internet Service source name.
    "internet-service-src-group": "string",  # Internet Service source group name.
    "internet-service-src-custom": "string",  # Custom Internet Service source name.
    "network-service-src-dynamic": "string",  # Dynamic Network Service source name.
    "internet-service-src-custom-group": "string",  # Custom Internet Service source group name.
    "reputation-minimum": "integer",  # Minimum Reputation to take action.
    "reputation-direction": "option",  # Direction of the initial traffic for reputation to take effe
    "src-vendor-mac": "string",  # Vendor MAC source ID.
    "internet-service6": "option",  # Enable/disable use of IPv6 Internet Services for this policy
    "internet-service6-name": "string",  # IPv6 Internet Service name.
    "internet-service6-group": "string",  # Internet Service group name.
    "internet-service6-custom": "string",  # Custom IPv6 Internet Service name.
    "internet-service6-custom-group": "string",  # Custom Internet Service6 group name.
    "internet-service6-src": "option",  # Enable/disable use of IPv6 Internet Services in source for t
    "internet-service6-src-name": "string",  # IPv6 Internet Service source name.
    "internet-service6-src-group": "string",  # Internet Service6 source group name.
    "internet-service6-src-custom": "string",  # Custom IPv6 Internet Service source name.
    "internet-service6-src-custom-group": "string",  # Custom Internet Service6 source group name.
    "reputation-minimum6": "integer",  # IPv6 Minimum Reputation to take action.
    "reputation-direction6": "option",  # Direction of the initial traffic for IPv6 reputation to take
    "rtp-nat": "option",  # Enable Real Time Protocol (RTP) NAT.
    "rtp-addr": "string",  # Address names if this is an RTP NAT policy.
    "send-deny-packet": "option",  # Enable to send a reply when a session is denied or blocked b
    "firewall-session-dirty": "option",  # How to handle sessions if the configuration of this firewall
    "schedule": "string",  # Schedule name.
    "schedule-timeout": "option",  # Enable to force current sessions to end when the schedule ob
    "policy-expiry": "option",  # Enable/disable policy expiry.
    "policy-expiry-date": "datetime",  # Policy expiry date (YYYY-MM-DD HH:MM:SS).
    "policy-expiry-date-utc": "user",  # Policy expiry date and time, in epoch format.
    "service": "string",  # Service and service group names.
    "tos-mask": "user",  # Non-zero bit positions are used for comparison while zero bi
    "tos": "user",  # ToS (Type of Service) value used for comparison.
    "tos-negate": "option",  # Enable negated TOS match.
    "anti-replay": "option",  # Enable/disable anti-replay check.
    "tcp-session-without-syn": "option",  # Enable/disable creation of TCP session without SYN flag.
    "geoip-anycast": "option",  # Enable/disable recognition of anycast IP addresses using the
    "geoip-match": "option",  # Match geography address based either on its physical locatio
    "dynamic-shaping": "option",  # Enable/disable dynamic RADIUS defined traffic shaping.
    "passive-wan-health-measurement": "option",  # Enable/disable passive WAN health measurement. When enabled,
    "app-monitor": "option",  # Enable/disable application TCP metrics in session logs.When 
    "utm-status": "option",  # Enable to add one or more security profiles (AV, IPS, etc.) 
    "inspection-mode": "option",  # Policy inspection mode (Flow/proxy). Default is Flow mode.
    "http-policy-redirect": "option",  # Redirect HTTP(S) traffic to matching transparent web proxy p
    "ssh-policy-redirect": "option",  # Redirect SSH traffic to matching transparent proxy policy.
    "ztna-policy-redirect": "option",  # Redirect ZTNA traffic to matching Access-Proxy proxy-policy.
    "webproxy-profile": "string",  # Webproxy profile name.
    "profile-type": "option",  # Determine whether the firewall policy allows security profil
    "profile-group": "string",  # Name of profile group.
    "profile-protocol-options": "string",  # Name of an existing Protocol options profile.
    "ssl-ssh-profile": "string",  # Name of an existing SSL SSH profile.
    "av-profile": "string",  # Name of an existing Antivirus profile.
    "webfilter-profile": "string",  # Name of an existing Web filter profile.
    "dnsfilter-profile": "string",  # Name of an existing DNS filter profile.
    "emailfilter-profile": "string",  # Name of an existing email filter profile.
    "dlp-profile": "string",  # Name of an existing DLP profile.
    "file-filter-profile": "string",  # Name of an existing file-filter profile.
    "ips-sensor": "string",  # Name of an existing IPS sensor.
    "application-list": "string",  # Name of an existing Application list.
    "voip-profile": "string",  # Name of an existing VoIP (voipd) profile.
    "ips-voip-filter": "string",  # Name of an existing VoIP (ips) profile.
    "sctp-filter-profile": "string",  # Name of an existing SCTP filter profile.
    "diameter-filter-profile": "string",  # Name of an existing Diameter filter profile.
    "virtual-patch-profile": "string",  # Name of an existing virtual-patch profile.
    "icap-profile": "string",  # Name of an existing ICAP profile.
    "videofilter-profile": "string",  # Name of an existing VideoFilter profile.
    "waf-profile": "string",  # Name of an existing Web application firewall profile.
    "ssh-filter-profile": "string",  # Name of an existing SSH filter profile.
    "casb-profile": "string",  # Name of an existing CASB profile.
    "logtraffic": "option",  # Enable or disable logging. Log all sessions or security prof
    "logtraffic-start": "option",  # Record logs when a session starts.
    "log-http-transaction": "option",  # Enable/disable HTTP transaction log.
    "capture-packet": "option",  # Enable/disable capture packets.
    "auto-asic-offload": "option",  # Enable/disable policy traffic ASIC offloading.
    "wanopt": "option",  # Enable/disable WAN optimization.
    "wanopt-detection": "option",  # WAN optimization auto-detection mode.
    "wanopt-passive-opt": "option",  # WAN optimization passive mode options. This option decides w
    "wanopt-profile": "string",  # WAN optimization profile.
    "wanopt-peer": "string",  # WAN optimization peer.
    "webcache": "option",  # Enable/disable web cache.
    "webcache-https": "option",  # Enable/disable web cache for HTTPS.
    "webproxy-forward-server": "string",  # Webproxy forward server name.
    "traffic-shaper": "string",  # Traffic shaper.
    "traffic-shaper-reverse": "string",  # Reverse traffic shaper.
    "per-ip-shaper": "string",  # Per-IP traffic shaper.
    "nat": "option",  # Enable/disable source NAT.
    "pcp-outbound": "option",  # Enable/disable PCP outbound SNAT.
    "pcp-inbound": "option",  # Enable/disable PCP inbound DNAT.
    "pcp-poolname": "string",  # PCP pool names.
    "permit-any-host": "option",  # Enable/disable fullcone NAT. Accept UDP packets from any hos
    "permit-stun-host": "option",  # Accept UDP packets from any Session Traversal Utilities for 
    "fixedport": "option",  # Enable to prevent source NAT from changing a session's sourc
    "port-preserve": "option",  # Enable/disable preservation of the original source port from
    "port-random": "option",  # Enable/disable random source port selection for source NAT.
    "ippool": "option",  # Enable to use IP Pools for source NAT.
    "poolname": "string",  # IP Pool names.
    "poolname6": "string",  # IPv6 pool names.
    "session-ttl": "user",  # TTL in seconds for sessions accepted by this policy (0 means
    "vlan-cos-fwd": "integer",  # VLAN forward direction user priority: 255 passthrough, 0 low
    "vlan-cos-rev": "integer",  # VLAN reverse direction user priority: 255 passthrough, 0 low
    "inbound": "option",  # Policy-based IPsec VPN: only traffic from the remote network
    "outbound": "option",  # Policy-based IPsec VPN: only traffic from the internal netwo
    "natinbound": "option",  # Policy-based IPsec VPN: apply destination NAT to inbound tra
    "natoutbound": "option",  # Policy-based IPsec VPN: apply source NAT to outbound traffic
    "fec": "option",  # Enable/disable Forward Error Correction on traffic matching 
    "wccp": "option",  # Enable/disable forwarding traffic matching this policy to a 
    "ntlm": "option",  # Enable/disable NTLM authentication.
    "ntlm-guest": "option",  # Enable/disable NTLM guest user access.
    "ntlm-enabled-browsers": "string",  # HTTP-User-Agent value of supported browsers.
    "fsso-agent-for-ntlm": "string",  # FSSO agent to use for NTLM authentication.
    "groups": "string",  # Names of user groups that can authenticate with this policy.
    "users": "string",  # Names of individual users that can authenticate with this po
    "fsso-groups": "string",  # Names of FSSO groups.
    "auth-path": "option",  # Enable/disable authentication-based routing.
    "disclaimer": "option",  # Enable/disable user authentication disclaimer.
    "email-collect": "option",  # Enable/disable email collection.
    "vpntunnel": "string",  # Policy-based IPsec VPN: name of the IPsec VPN Phase 1.
    "natip": "ipv4-classnet",  # Policy-based IPsec VPN: source NAT IP address for outgoing t
    "match-vip": "option",  # Enable to match packets that have had their destination addr
    "match-vip-only": "option",  # Enable/disable matching of only those packets that have had 
    "diffserv-copy": "option",  # Enable to copy packet's DiffServ values from session's origi
    "diffserv-forward": "option",  # Enable to change packet's DiffServ values to the specified d
    "diffserv-reverse": "option",  # Enable to change packet's reverse (reply) DiffServ values to
    "diffservcode-forward": "user",  # Change packet's DiffServ to this value.
    "diffservcode-rev": "user",  # Change packet's reverse (reply) DiffServ to this value.
    "tcp-mss-sender": "integer",  # Sender TCP maximum segment size (MSS).
    "tcp-mss-receiver": "integer",  # Receiver TCP maximum segment size (MSS).
    "comments": "var-string",  # Comment.
    "auth-cert": "string",  # HTTPS server certificate for policy authentication.
    "auth-redirect-addr": "string",  # HTTP-to-HTTPS redirect address for firewall authentication.
    "redirect-url": "var-string",  # URL users are directed to after seeing and accepting the dis
    "identity-based-route": "string",  # Name of identity-based routing rule.
    "block-notification": "option",  # Enable/disable block notification.
    "custom-log-fields": "string",  # Custom fields to append to log messages for this policy.
    "replacemsg-override-group": "string",  # Override the default replacement message group for this poli
    "srcaddr-negate": "option",  # When enabled srcaddr specifies what the source address must 
    "srcaddr6-negate": "option",  # When enabled srcaddr6 specifies what the source address must
    "dstaddr-negate": "option",  # When enabled dstaddr specifies what the destination address 
    "dstaddr6-negate": "option",  # When enabled dstaddr6 specifies what the destination address
    "ztna-ems-tag-negate": "option",  # When enabled ztna-ems-tag specifies what the tags must NOT b
    "service-negate": "option",  # When enabled service specifies what the service must NOT be.
    "internet-service-negate": "option",  # When enabled internet-service specifies what the service mus
    "internet-service-src-negate": "option",  # When enabled internet-service-src specifies what the service
    "internet-service6-negate": "option",  # When enabled internet-service6 specifies what the service mu
    "internet-service6-src-negate": "option",  # When enabled internet-service6-src specifies what the servic
    "timeout-send-rst": "option",  # Enable/disable sending RST packets when TCP sessions expire.
    "captive-portal-exempt": "option",  # Enable to exempt some users from the captive portal.
    "decrypted-traffic-mirror": "string",  # Decrypted traffic mirror.
    "dsri": "option",  # Enable DSRI to ignore HTTP server responses.
    "radius-mac-auth-bypass": "option",  # Enable MAC authentication bypass. The bypassed MAC address m
    "radius-ip-auth-bypass": "option",  # Enable IP authentication bypass. The bypassed IP address mus
    "delay-tcp-npu-session": "option",  # Enable TCP NPU session delay to guarantee packet order of 3-
    "vlan-filter": "user",  # VLAN ranges to allow
    "sgt-check": "option",  # Enable/disable security group tags (SGT) check.
    "sgt": "string",  # Security group tags.
    "internet-service-fortiguard": "string",  # FortiGuard Internet Service name.
    "internet-service-src-fortiguard": "string",  # FortiGuard Internet Service source name.
    "internet-service6-fortiguard": "string",  # FortiGuard IPv6 Internet Service name.
    "internet-service6-src-fortiguard": "string",  # FortiGuard IPv6 Internet Service source name.
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "policyid": "Policy ID (0 - 4294967294).",
    "status": "Enable or disable this policy.",
    "name": "Policy name.",
    "uuid": "Universally Unique Identifier (UUID; automatically assigned but can be manually reset).",
    "srcintf": "Incoming (ingress) interface.",
    "dstintf": "Outgoing (egress) interface.",
    "action": "Policy action (accept/deny/ipsec).",
    "nat64": "Enable/disable NAT64.",
    "nat46": "Enable/disable NAT46.",
    "ztna-status": "Enable/disable zero trust access.",
    "ztna-device-ownership": "Enable/disable zero trust device ownership.",
    "srcaddr": "Source IPv4 address and address group names.",
    "dstaddr": "Destination IPv4 address and address group names.",
    "srcaddr6": "Source IPv6 address name and address group names.",
    "dstaddr6": "Destination IPv6 address name and address group names.",
    "ztna-ems-tag": "Source ztna-ems-tag names.",
    "ztna-ems-tag-secondary": "Source ztna-ems-tag-secondary names.",
    "ztna-tags-match-logic": "ZTNA tag matching logic.",
    "ztna-geo-tag": "Source ztna-geo-tag names.",
    "internet-service": "Enable/disable use of Internet Services for this policy. If enabled, destination address and service are not used.",
    "internet-service-name": "Internet Service name.",
    "internet-service-group": "Internet Service group name.",
    "internet-service-custom": "Custom Internet Service name.",
    "network-service-dynamic": "Dynamic Network Service name.",
    "internet-service-custom-group": "Custom Internet Service group name.",
    "internet-service-src": "Enable/disable use of Internet Services in source for this policy. If enabled, source address is not used.",
    "internet-service-src-name": "Internet Service source name.",
    "internet-service-src-group": "Internet Service source group name.",
    "internet-service-src-custom": "Custom Internet Service source name.",
    "network-service-src-dynamic": "Dynamic Network Service source name.",
    "internet-service-src-custom-group": "Custom Internet Service source group name.",
    "reputation-minimum": "Minimum Reputation to take action.",
    "reputation-direction": "Direction of the initial traffic for reputation to take effect.",
    "src-vendor-mac": "Vendor MAC source ID.",
    "internet-service6": "Enable/disable use of IPv6 Internet Services for this policy. If enabled, destination address and service are not used.",
    "internet-service6-name": "IPv6 Internet Service name.",
    "internet-service6-group": "Internet Service group name.",
    "internet-service6-custom": "Custom IPv6 Internet Service name.",
    "internet-service6-custom-group": "Custom Internet Service6 group name.",
    "internet-service6-src": "Enable/disable use of IPv6 Internet Services in source for this policy. If enabled, source address is not used.",
    "internet-service6-src-name": "IPv6 Internet Service source name.",
    "internet-service6-src-group": "Internet Service6 source group name.",
    "internet-service6-src-custom": "Custom IPv6 Internet Service source name.",
    "internet-service6-src-custom-group": "Custom Internet Service6 source group name.",
    "reputation-minimum6": "IPv6 Minimum Reputation to take action.",
    "reputation-direction6": "Direction of the initial traffic for IPv6 reputation to take effect.",
    "rtp-nat": "Enable Real Time Protocol (RTP) NAT.",
    "rtp-addr": "Address names if this is an RTP NAT policy.",
    "send-deny-packet": "Enable to send a reply when a session is denied or blocked by a firewall policy.",
    "firewall-session-dirty": "How to handle sessions if the configuration of this firewall policy changes.",
    "schedule": "Schedule name.",
    "schedule-timeout": "Enable to force current sessions to end when the schedule object times out. Disable allows them to end from inactivity.",
    "policy-expiry": "Enable/disable policy expiry.",
    "policy-expiry-date": "Policy expiry date (YYYY-MM-DD HH:MM:SS).",
    "policy-expiry-date-utc": "Policy expiry date and time, in epoch format.",
    "service": "Service and service group names.",
    "tos-mask": "Non-zero bit positions are used for comparison while zero bit positions are ignored.",
    "tos": "ToS (Type of Service) value used for comparison.",
    "tos-negate": "Enable negated TOS match.",
    "anti-replay": "Enable/disable anti-replay check.",
    "tcp-session-without-syn": "Enable/disable creation of TCP session without SYN flag.",
    "geoip-anycast": "Enable/disable recognition of anycast IP addresses using the geography IP database.",
    "geoip-match": "Match geography address based either on its physical location or registered location.",
    "dynamic-shaping": "Enable/disable dynamic RADIUS defined traffic shaping.",
    "passive-wan-health-measurement": "Enable/disable passive WAN health measurement. When enabled, auto-asic-offload is disabled.",
    "app-monitor": "Enable/disable application TCP metrics in session logs.When enabled, auto-asic-offload is disabled.",
    "utm-status": "Enable to add one or more security profiles (AV, IPS, etc.) to the firewall policy.",
    "inspection-mode": "Policy inspection mode (Flow/proxy). Default is Flow mode.",
    "http-policy-redirect": "Redirect HTTP(S) traffic to matching transparent web proxy policy.",
    "ssh-policy-redirect": "Redirect SSH traffic to matching transparent proxy policy.",
    "ztna-policy-redirect": "Redirect ZTNA traffic to matching Access-Proxy proxy-policy.",
    "webproxy-profile": "Webproxy profile name.",
    "profile-type": "Determine whether the firewall policy allows security profile groups or single profiles only.",
    "profile-group": "Name of profile group.",
    "profile-protocol-options": "Name of an existing Protocol options profile.",
    "ssl-ssh-profile": "Name of an existing SSL SSH profile.",
    "av-profile": "Name of an existing Antivirus profile.",
    "webfilter-profile": "Name of an existing Web filter profile.",
    "dnsfilter-profile": "Name of an existing DNS filter profile.",
    "emailfilter-profile": "Name of an existing email filter profile.",
    "dlp-profile": "Name of an existing DLP profile.",
    "file-filter-profile": "Name of an existing file-filter profile.",
    "ips-sensor": "Name of an existing IPS sensor.",
    "application-list": "Name of an existing Application list.",
    "voip-profile": "Name of an existing VoIP (voipd) profile.",
    "ips-voip-filter": "Name of an existing VoIP (ips) profile.",
    "sctp-filter-profile": "Name of an existing SCTP filter profile.",
    "diameter-filter-profile": "Name of an existing Diameter filter profile.",
    "virtual-patch-profile": "Name of an existing virtual-patch profile.",
    "icap-profile": "Name of an existing ICAP profile.",
    "videofilter-profile": "Name of an existing VideoFilter profile.",
    "waf-profile": "Name of an existing Web application firewall profile.",
    "ssh-filter-profile": "Name of an existing SSH filter profile.",
    "casb-profile": "Name of an existing CASB profile.",
    "logtraffic": "Enable or disable logging. Log all sessions or security profile sessions.",
    "logtraffic-start": "Record logs when a session starts.",
    "log-http-transaction": "Enable/disable HTTP transaction log.",
    "capture-packet": "Enable/disable capture packets.",
    "auto-asic-offload": "Enable/disable policy traffic ASIC offloading.",
    "wanopt": "Enable/disable WAN optimization.",
    "wanopt-detection": "WAN optimization auto-detection mode.",
    "wanopt-passive-opt": "WAN optimization passive mode options. This option decides what IP address will be used to connect server.",
    "wanopt-profile": "WAN optimization profile.",
    "wanopt-peer": "WAN optimization peer.",
    "webcache": "Enable/disable web cache.",
    "webcache-https": "Enable/disable web cache for HTTPS.",
    "webproxy-forward-server": "Webproxy forward server name.",
    "traffic-shaper": "Traffic shaper.",
    "traffic-shaper-reverse": "Reverse traffic shaper.",
    "per-ip-shaper": "Per-IP traffic shaper.",
    "nat": "Enable/disable source NAT.",
    "pcp-outbound": "Enable/disable PCP outbound SNAT.",
    "pcp-inbound": "Enable/disable PCP inbound DNAT.",
    "pcp-poolname": "PCP pool names.",
    "permit-any-host": "Enable/disable fullcone NAT. Accept UDP packets from any host.",
    "permit-stun-host": "Accept UDP packets from any Session Traversal Utilities for NAT (STUN) host.",
    "fixedport": "Enable to prevent source NAT from changing a session's source port.",
    "port-preserve": "Enable/disable preservation of the original source port from source NAT if it has not been used.",
    "port-random": "Enable/disable random source port selection for source NAT.",
    "ippool": "Enable to use IP Pools for source NAT.",
    "poolname": "IP Pool names.",
    "poolname6": "IPv6 pool names.",
    "session-ttl": "TTL in seconds for sessions accepted by this policy (0 means use the system default session TTL).",
    "vlan-cos-fwd": "VLAN forward direction user priority: 255 passthrough, 0 lowest, 7 highest.",
    "vlan-cos-rev": "VLAN reverse direction user priority: 255 passthrough, 0 lowest, 7 highest.",
    "inbound": "Policy-based IPsec VPN: only traffic from the remote network can initiate a VPN.",
    "outbound": "Policy-based IPsec VPN: only traffic from the internal network can initiate a VPN.",
    "natinbound": "Policy-based IPsec VPN: apply destination NAT to inbound traffic.",
    "natoutbound": "Policy-based IPsec VPN: apply source NAT to outbound traffic.",
    "fec": "Enable/disable Forward Error Correction on traffic matching this policy on a FEC device.",
    "wccp": "Enable/disable forwarding traffic matching this policy to a configured WCCP server.",
    "ntlm": "Enable/disable NTLM authentication.",
    "ntlm-guest": "Enable/disable NTLM guest user access.",
    "ntlm-enabled-browsers": "HTTP-User-Agent value of supported browsers.",
    "fsso-agent-for-ntlm": "FSSO agent to use for NTLM authentication.",
    "groups": "Names of user groups that can authenticate with this policy.",
    "users": "Names of individual users that can authenticate with this policy.",
    "fsso-groups": "Names of FSSO groups.",
    "auth-path": "Enable/disable authentication-based routing.",
    "disclaimer": "Enable/disable user authentication disclaimer.",
    "email-collect": "Enable/disable email collection.",
    "vpntunnel": "Policy-based IPsec VPN: name of the IPsec VPN Phase 1.",
    "natip": "Policy-based IPsec VPN: source NAT IP address for outgoing traffic.",
    "match-vip": "Enable to match packets that have had their destination addresses changed by a VIP.",
    "match-vip-only": "Enable/disable matching of only those packets that have had their destination addresses changed by a VIP.",
    "diffserv-copy": "Enable to copy packet's DiffServ values from session's original direction to its reply direction.",
    "diffserv-forward": "Enable to change packet's DiffServ values to the specified diffservcode-forward value.",
    "diffserv-reverse": "Enable to change packet's reverse (reply) DiffServ values to the specified diffservcode-rev value.",
    "diffservcode-forward": "Change packet's DiffServ to this value.",
    "diffservcode-rev": "Change packet's reverse (reply) DiffServ to this value.",
    "tcp-mss-sender": "Sender TCP maximum segment size (MSS).",
    "tcp-mss-receiver": "Receiver TCP maximum segment size (MSS).",
    "comments": "Comment.",
    "auth-cert": "HTTPS server certificate for policy authentication.",
    "auth-redirect-addr": "HTTP-to-HTTPS redirect address for firewall authentication.",
    "redirect-url": "URL users are directed to after seeing and accepting the disclaimer or authenticating.",
    "identity-based-route": "Name of identity-based routing rule.",
    "block-notification": "Enable/disable block notification.",
    "custom-log-fields": "Custom fields to append to log messages for this policy.",
    "replacemsg-override-group": "Override the default replacement message group for this policy.",
    "srcaddr-negate": "When enabled srcaddr specifies what the source address must NOT be.",
    "srcaddr6-negate": "When enabled srcaddr6 specifies what the source address must NOT be.",
    "dstaddr-negate": "When enabled dstaddr specifies what the destination address must NOT be.",
    "dstaddr6-negate": "When enabled dstaddr6 specifies what the destination address must NOT be.",
    "ztna-ems-tag-negate": "When enabled ztna-ems-tag specifies what the tags must NOT be.",
    "service-negate": "When enabled service specifies what the service must NOT be.",
    "internet-service-negate": "When enabled internet-service specifies what the service must NOT be.",
    "internet-service-src-negate": "When enabled internet-service-src specifies what the service must NOT be.",
    "internet-service6-negate": "When enabled internet-service6 specifies what the service must NOT be.",
    "internet-service6-src-negate": "When enabled internet-service6-src specifies what the service must NOT be.",
    "timeout-send-rst": "Enable/disable sending RST packets when TCP sessions expire.",
    "captive-portal-exempt": "Enable to exempt some users from the captive portal.",
    "decrypted-traffic-mirror": "Decrypted traffic mirror.",
    "dsri": "Enable DSRI to ignore HTTP server responses.",
    "radius-mac-auth-bypass": "Enable MAC authentication bypass. The bypassed MAC address must be received from RADIUS server.",
    "radius-ip-auth-bypass": "Enable IP authentication bypass. The bypassed IP address must be received from RADIUS server.",
    "delay-tcp-npu-session": "Enable TCP NPU session delay to guarantee packet order of 3-way handshake.",
    "vlan-filter": "VLAN ranges to allow",
    "sgt-check": "Enable/disable security group tags (SGT) check.",
    "sgt": "Security group tags.",
    "internet-service-fortiguard": "FortiGuard Internet Service name.",
    "internet-service-src-fortiguard": "FortiGuard Internet Service source name.",
    "internet-service6-fortiguard": "FortiGuard IPv6 Internet Service name.",
    "internet-service6-src-fortiguard": "FortiGuard IPv6 Internet Service source name.",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "policyid": {"type": "integer", "min": 0, "max": 4294967294},
    "name": {"type": "string", "max_length": 35},
    "reputation-minimum": {"type": "integer", "min": 0, "max": 4294967295},
    "reputation-minimum6": {"type": "integer", "min": 0, "max": 4294967295},
    "schedule": {"type": "string", "max_length": 35},
    "webproxy-profile": {"type": "string", "max_length": 63},
    "profile-group": {"type": "string", "max_length": 47},
    "profile-protocol-options": {"type": "string", "max_length": 47},
    "ssl-ssh-profile": {"type": "string", "max_length": 47},
    "av-profile": {"type": "string", "max_length": 47},
    "webfilter-profile": {"type": "string", "max_length": 47},
    "dnsfilter-profile": {"type": "string", "max_length": 47},
    "emailfilter-profile": {"type": "string", "max_length": 47},
    "dlp-profile": {"type": "string", "max_length": 47},
    "file-filter-profile": {"type": "string", "max_length": 47},
    "ips-sensor": {"type": "string", "max_length": 47},
    "application-list": {"type": "string", "max_length": 47},
    "voip-profile": {"type": "string", "max_length": 47},
    "ips-voip-filter": {"type": "string", "max_length": 47},
    "sctp-filter-profile": {"type": "string", "max_length": 47},
    "diameter-filter-profile": {"type": "string", "max_length": 47},
    "virtual-patch-profile": {"type": "string", "max_length": 47},
    "icap-profile": {"type": "string", "max_length": 47},
    "videofilter-profile": {"type": "string", "max_length": 47},
    "waf-profile": {"type": "string", "max_length": 47},
    "ssh-filter-profile": {"type": "string", "max_length": 47},
    "casb-profile": {"type": "string", "max_length": 47},
    "wanopt-profile": {"type": "string", "max_length": 35},
    "wanopt-peer": {"type": "string", "max_length": 35},
    "webproxy-forward-server": {"type": "string", "max_length": 63},
    "traffic-shaper": {"type": "string", "max_length": 35},
    "traffic-shaper-reverse": {"type": "string", "max_length": 35},
    "per-ip-shaper": {"type": "string", "max_length": 35},
    "vlan-cos-fwd": {"type": "integer", "min": 0, "max": 7},
    "vlan-cos-rev": {"type": "integer", "min": 0, "max": 7},
    "fsso-agent-for-ntlm": {"type": "string", "max_length": 35},
    "vpntunnel": {"type": "string", "max_length": 35},
    "tcp-mss-sender": {"type": "integer", "min": 0, "max": 65535},
    "tcp-mss-receiver": {"type": "integer", "min": 0, "max": 65535},
    "auth-cert": {"type": "string", "max_length": 35},
    "auth-redirect-addr": {"type": "string", "max_length": 63},
    "identity-based-route": {"type": "string", "max_length": 35},
    "replacemsg-override-group": {"type": "string", "max_length": 35},
    "decrypted-traffic-mirror": {"type": "string", "max_length": 35},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "srcintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "dstintf": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "srcaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "dstaddr6": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "ztna-ems-tag": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "ztna-ems-tag-secondary": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "ztna-geo-tag": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "network-service-dynamic": {
        "name": {
            "type": "string",
            "help": "Dynamic Network Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "network-service-src-dynamic": {
        "name": {
            "type": "string",
            "help": "Dynamic Network Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "src-vendor-mac": {
        "id": {
            "type": "integer",
            "help": "Vendor MAC ID.",
            "required": True,
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
    },
    "internet-service6-name": {
        "name": {
            "type": "string",
            "help": "IPv6 Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service6 group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-name": {
        "name": {
            "type": "string",
            "help": "Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-group": {
        "name": {
            "type": "string",
            "help": "Internet Service group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-custom": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-custom-group": {
        "name": {
            "type": "string",
            "help": "Custom Internet Service6 group name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "rtp-addr": {
        "name": {
            "type": "string",
            "help": "Address name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "service": {
        "name": {
            "type": "string",
            "help": "Service and service group names.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "pcp-poolname": {
        "name": {
            "type": "string",
            "help": "PCP pool name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "poolname": {
        "name": {
            "type": "string",
            "help": "IP pool name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "poolname6": {
        "name": {
            "type": "string",
            "help": "IPv6 pool name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "ntlm-enabled-browsers": {
        "user-agent-string": {
            "type": "string",
            "help": "User agent string.",
            "default": "",
            "max_length": 79,
        },
    },
    "groups": {
        "name": {
            "type": "string",
            "help": "Group name.",
            "default": "",
            "max_length": 79,
        },
    },
    "users": {
        "name": {
            "type": "string",
            "help": "Names of individual users that can authenticate with this policy.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "fsso-groups": {
        "name": {
            "type": "string",
            "help": "Names of FSSO groups.",
            "required": True,
            "default": "",
            "max_length": 511,
        },
    },
    "custom-log-fields": {
        "field-id": {
            "type": "string",
            "help": "Custom log field.",
            "default": "",
            "max_length": 35,
        },
    },
    "sgt": {
        "id": {
            "type": "integer",
            "help": "Security group tag (1 - 65535).",
            "required": True,
            "default": 0,
            "min_value": 1,
            "max_value": 65535,
        },
    },
    "internet-service-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service-src-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
    "internet-service6-src-fortiguard": {
        "name": {
            "type": "string",
            "help": "FortiGuard Internet Service name.",
            "required": True,
            "default": "",
            "max_length": 79,
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_ACTION = [
    "accept",
    "deny",
    "ipsec",
]
VALID_BODY_NAT64 = [
    "enable",
    "disable",
]
VALID_BODY_NAT46 = [
    "enable",
    "disable",
]
VALID_BODY_ZTNA_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_ZTNA_DEVICE_OWNERSHIP = [
    "enable",
    "disable",
]
VALID_BODY_ZTNA_TAGS_MATCH_LOGIC = [
    "or",
    "and",
]
VALID_BODY_INTERNET_SERVICE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_SRC = [
    "enable",
    "disable",
]
VALID_BODY_REPUTATION_DIRECTION = [
    "source",
    "destination",
]
VALID_BODY_INTERNET_SERVICE6 = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6_SRC = [
    "enable",
    "disable",
]
VALID_BODY_REPUTATION_DIRECTION6 = [
    "source",
    "destination",
]
VALID_BODY_RTP_NAT = [
    "disable",
    "enable",
]
VALID_BODY_SEND_DENY_PACKET = [
    "disable",
    "enable",
]
VALID_BODY_FIREWALL_SESSION_DIRTY = [
    "check-all",
    "check-new",
]
VALID_BODY_SCHEDULE_TIMEOUT = [
    "enable",
    "disable",
]
VALID_BODY_POLICY_EXPIRY = [
    "enable",
    "disable",
]
VALID_BODY_TOS_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_ANTI_REPLAY = [
    "enable",
    "disable",
]
VALID_BODY_TCP_SESSION_WITHOUT_SYN = [
    "all",
    "data-only",
    "disable",
]
VALID_BODY_GEOIP_ANYCAST = [
    "enable",
    "disable",
]
VALID_BODY_GEOIP_MATCH = [
    "physical-location",
    "registered-location",
]
VALID_BODY_DYNAMIC_SHAPING = [
    "enable",
    "disable",
]
VALID_BODY_PASSIVE_WAN_HEALTH_MEASUREMENT = [
    "enable",
    "disable",
]
VALID_BODY_APP_MONITOR = [
    "enable",
    "disable",
]
VALID_BODY_UTM_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_INSPECTION_MODE = [
    "proxy",
    "flow",
]
VALID_BODY_HTTP_POLICY_REDIRECT = [
    "enable",
    "disable",
    "legacy",
]
VALID_BODY_SSH_POLICY_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_ZTNA_POLICY_REDIRECT = [
    "enable",
    "disable",
]
VALID_BODY_PROFILE_TYPE = [
    "single",
    "group",
]
VALID_BODY_LOGTRAFFIC = [
    "all",
    "utm",
    "disable",
]
VALID_BODY_LOGTRAFFIC_START = [
    "enable",
    "disable",
]
VALID_BODY_LOG_HTTP_TRANSACTION = [
    "enable",
    "disable",
]
VALID_BODY_CAPTURE_PACKET = [
    "enable",
    "disable",
]
VALID_BODY_AUTO_ASIC_OFFLOAD = [
    "enable",
    "disable",
]
VALID_BODY_WANOPT = [
    "enable",
    "disable",
]
VALID_BODY_WANOPT_DETECTION = [
    "active",
    "passive",
    "off",
]
VALID_BODY_WANOPT_PASSIVE_OPT = [
    "default",
    "transparent",
    "non-transparent",
]
VALID_BODY_WEBCACHE = [
    "enable",
    "disable",
]
VALID_BODY_WEBCACHE_HTTPS = [
    "disable",
    "enable",
]
VALID_BODY_NAT = [
    "enable",
    "disable",
]
VALID_BODY_PCP_OUTBOUND = [
    "enable",
    "disable",
]
VALID_BODY_PCP_INBOUND = [
    "enable",
    "disable",
]
VALID_BODY_PERMIT_ANY_HOST = [
    "enable",
    "disable",
]
VALID_BODY_PERMIT_STUN_HOST = [
    "enable",
    "disable",
]
VALID_BODY_FIXEDPORT = [
    "enable",
    "disable",
]
VALID_BODY_PORT_PRESERVE = [
    "enable",
    "disable",
]
VALID_BODY_PORT_RANDOM = [
    "enable",
    "disable",
]
VALID_BODY_IPPOOL = [
    "enable",
    "disable",
]
VALID_BODY_INBOUND = [
    "enable",
    "disable",
]
VALID_BODY_OUTBOUND = [
    "enable",
    "disable",
]
VALID_BODY_NATINBOUND = [
    "enable",
    "disable",
]
VALID_BODY_NATOUTBOUND = [
    "enable",
    "disable",
]
VALID_BODY_FEC = [
    "enable",
    "disable",
]
VALID_BODY_WCCP = [
    "enable",
    "disable",
]
VALID_BODY_NTLM = [
    "enable",
    "disable",
]
VALID_BODY_NTLM_GUEST = [
    "enable",
    "disable",
]
VALID_BODY_AUTH_PATH = [
    "enable",
    "disable",
]
VALID_BODY_DISCLAIMER = [
    "enable",
    "disable",
]
VALID_BODY_EMAIL_COLLECT = [
    "enable",
    "disable",
]
VALID_BODY_MATCH_VIP = [
    "enable",
    "disable",
]
VALID_BODY_MATCH_VIP_ONLY = [
    "enable",
    "disable",
]
VALID_BODY_DIFFSERV_COPY = [
    "enable",
    "disable",
]
VALID_BODY_DIFFSERV_FORWARD = [
    "enable",
    "disable",
]
VALID_BODY_DIFFSERV_REVERSE = [
    "enable",
    "disable",
]
VALID_BODY_BLOCK_NOTIFICATION = [
    "enable",
    "disable",
]
VALID_BODY_SRCADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_SRCADDR6_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_DSTADDR_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_DSTADDR6_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_ZTNA_EMS_TAG_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_SERVICE_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE_SRC_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE = [
    "enable",
    "disable",
]
VALID_BODY_TIMEOUT_SEND_RST = [
    "enable",
    "disable",
]
VALID_BODY_CAPTIVE_PORTAL_EXEMPT = [
    "enable",
    "disable",
]
VALID_BODY_DSRI = [
    "enable",
    "disable",
]
VALID_BODY_RADIUS_MAC_AUTH_BYPASS = [
    "enable",
    "disable",
]
VALID_BODY_RADIUS_IP_AUTH_BYPASS = [
    "enable",
    "disable",
]
VALID_BODY_DELAY_TCP_NPU_SESSION = [
    "enable",
    "disable",
]
VALID_BODY_SGT_CHECK = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_firewall_policy_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for firewall/policy."""
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


def validate_firewall_policy_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new firewall/policy object."""
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
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64" in payload:
        is_valid, error = _validate_enum_field(
            "nat64",
            payload["nat64"],
            VALID_BODY_NAT64,
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
    if "ztna-status" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-status",
            payload["ztna-status"],
            VALID_BODY_ZTNA_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-device-ownership" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-device-ownership",
            payload["ztna-device-ownership"],
            VALID_BODY_ZTNA_DEVICE_OWNERSHIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-tags-match-logic" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-tags-match-logic",
            payload["ztna-tags-match-logic"],
            VALID_BODY_ZTNA_TAGS_MATCH_LOGIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service",
            payload["internet-service"],
            VALID_BODY_INTERNET_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src",
            payload["internet-service-src"],
            VALID_BODY_INTERNET_SERVICE_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reputation-direction" in payload:
        is_valid, error = _validate_enum_field(
            "reputation-direction",
            payload["reputation-direction"],
            VALID_BODY_REPUTATION_DIRECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6",
            payload["internet-service6"],
            VALID_BODY_INTERNET_SERVICE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src",
            payload["internet-service6-src"],
            VALID_BODY_INTERNET_SERVICE6_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reputation-direction6" in payload:
        is_valid, error = _validate_enum_field(
            "reputation-direction6",
            payload["reputation-direction6"],
            VALID_BODY_REPUTATION_DIRECTION6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rtp-nat" in payload:
        is_valid, error = _validate_enum_field(
            "rtp-nat",
            payload["rtp-nat"],
            VALID_BODY_RTP_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-deny-packet" in payload:
        is_valid, error = _validate_enum_field(
            "send-deny-packet",
            payload["send-deny-packet"],
            VALID_BODY_SEND_DENY_PACKET,
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
    if "schedule-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-timeout",
            payload["schedule-timeout"],
            VALID_BODY_SCHEDULE_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-expiry" in payload:
        is_valid, error = _validate_enum_field(
            "policy-expiry",
            payload["policy-expiry"],
            VALID_BODY_POLICY_EXPIRY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tos-negate" in payload:
        is_valid, error = _validate_enum_field(
            "tos-negate",
            payload["tos-negate"],
            VALID_BODY_TOS_NEGATE,
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
    if "tcp-session-without-syn" in payload:
        is_valid, error = _validate_enum_field(
            "tcp-session-without-syn",
            payload["tcp-session-without-syn"],
            VALID_BODY_TCP_SESSION_WITHOUT_SYN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "geoip-anycast" in payload:
        is_valid, error = _validate_enum_field(
            "geoip-anycast",
            payload["geoip-anycast"],
            VALID_BODY_GEOIP_ANYCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "geoip-match" in payload:
        is_valid, error = _validate_enum_field(
            "geoip-match",
            payload["geoip-match"],
            VALID_BODY_GEOIP_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-shaping" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-shaping",
            payload["dynamic-shaping"],
            VALID_BODY_DYNAMIC_SHAPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "passive-wan-health-measurement" in payload:
        is_valid, error = _validate_enum_field(
            "passive-wan-health-measurement",
            payload["passive-wan-health-measurement"],
            VALID_BODY_PASSIVE_WAN_HEALTH_MEASUREMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "app-monitor" in payload:
        is_valid, error = _validate_enum_field(
            "app-monitor",
            payload["app-monitor"],
            VALID_BODY_APP_MONITOR,
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
    if "inspection-mode" in payload:
        is_valid, error = _validate_enum_field(
            "inspection-mode",
            payload["inspection-mode"],
            VALID_BODY_INSPECTION_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "http-policy-redirect",
            payload["http-policy-redirect"],
            VALID_BODY_HTTP_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-policy-redirect",
            payload["ssh-policy-redirect"],
            VALID_BODY_SSH_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-policy-redirect",
            payload["ztna-policy-redirect"],
            VALID_BODY_ZTNA_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "profile-type" in payload:
        is_valid, error = _validate_enum_field(
            "profile-type",
            payload["profile-type"],
            VALID_BODY_PROFILE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic-start" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic-start",
            payload["logtraffic-start"],
            VALID_BODY_LOGTRAFFIC_START,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-http-transaction" in payload:
        is_valid, error = _validate_enum_field(
            "log-http-transaction",
            payload["log-http-transaction"],
            VALID_BODY_LOG_HTTP_TRANSACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "capture-packet" in payload:
        is_valid, error = _validate_enum_field(
            "capture-packet",
            payload["capture-packet"],
            VALID_BODY_CAPTURE_PACKET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-asic-offload" in payload:
        is_valid, error = _validate_enum_field(
            "auto-asic-offload",
            payload["auto-asic-offload"],
            VALID_BODY_AUTO_ASIC_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt",
            payload["wanopt"],
            VALID_BODY_WANOPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt-detection" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt-detection",
            payload["wanopt-detection"],
            VALID_BODY_WANOPT_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt-passive-opt" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt-passive-opt",
            payload["wanopt-passive-opt"],
            VALID_BODY_WANOPT_PASSIVE_OPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache" in payload:
        is_valid, error = _validate_enum_field(
            "webcache",
            payload["webcache"],
            VALID_BODY_WEBCACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache-https" in payload:
        is_valid, error = _validate_enum_field(
            "webcache-https",
            payload["webcache-https"],
            VALID_BODY_WEBCACHE_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat" in payload:
        is_valid, error = _validate_enum_field(
            "nat",
            payload["nat"],
            VALID_BODY_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pcp-outbound" in payload:
        is_valid, error = _validate_enum_field(
            "pcp-outbound",
            payload["pcp-outbound"],
            VALID_BODY_PCP_OUTBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pcp-inbound" in payload:
        is_valid, error = _validate_enum_field(
            "pcp-inbound",
            payload["pcp-inbound"],
            VALID_BODY_PCP_INBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "permit-any-host" in payload:
        is_valid, error = _validate_enum_field(
            "permit-any-host",
            payload["permit-any-host"],
            VALID_BODY_PERMIT_ANY_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "permit-stun-host" in payload:
        is_valid, error = _validate_enum_field(
            "permit-stun-host",
            payload["permit-stun-host"],
            VALID_BODY_PERMIT_STUN_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fixedport" in payload:
        is_valid, error = _validate_enum_field(
            "fixedport",
            payload["fixedport"],
            VALID_BODY_FIXEDPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-preserve" in payload:
        is_valid, error = _validate_enum_field(
            "port-preserve",
            payload["port-preserve"],
            VALID_BODY_PORT_PRESERVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-random" in payload:
        is_valid, error = _validate_enum_field(
            "port-random",
            payload["port-random"],
            VALID_BODY_PORT_RANDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ippool" in payload:
        is_valid, error = _validate_enum_field(
            "ippool",
            payload["ippool"],
            VALID_BODY_IPPOOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inbound" in payload:
        is_valid, error = _validate_enum_field(
            "inbound",
            payload["inbound"],
            VALID_BODY_INBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbound" in payload:
        is_valid, error = _validate_enum_field(
            "outbound",
            payload["outbound"],
            VALID_BODY_OUTBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "natinbound" in payload:
        is_valid, error = _validate_enum_field(
            "natinbound",
            payload["natinbound"],
            VALID_BODY_NATINBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "natoutbound" in payload:
        is_valid, error = _validate_enum_field(
            "natoutbound",
            payload["natoutbound"],
            VALID_BODY_NATOUTBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec" in payload:
        is_valid, error = _validate_enum_field(
            "fec",
            payload["fec"],
            VALID_BODY_FEC,
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
    if "ntlm" in payload:
        is_valid, error = _validate_enum_field(
            "ntlm",
            payload["ntlm"],
            VALID_BODY_NTLM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ntlm-guest" in payload:
        is_valid, error = _validate_enum_field(
            "ntlm-guest",
            payload["ntlm-guest"],
            VALID_BODY_NTLM_GUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-path" in payload:
        is_valid, error = _validate_enum_field(
            "auth-path",
            payload["auth-path"],
            VALID_BODY_AUTH_PATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "disclaimer",
            payload["disclaimer"],
            VALID_BODY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email-collect" in payload:
        is_valid, error = _validate_enum_field(
            "email-collect",
            payload["email-collect"],
            VALID_BODY_EMAIL_COLLECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-vip" in payload:
        is_valid, error = _validate_enum_field(
            "match-vip",
            payload["match-vip"],
            VALID_BODY_MATCH_VIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-vip-only" in payload:
        is_valid, error = _validate_enum_field(
            "match-vip-only",
            payload["match-vip-only"],
            VALID_BODY_MATCH_VIP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-copy" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-copy",
            payload["diffserv-copy"],
            VALID_BODY_DIFFSERV_COPY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-forward" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-forward",
            payload["diffserv-forward"],
            VALID_BODY_DIFFSERV_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-reverse" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-reverse",
            payload["diffserv-reverse"],
            VALID_BODY_DIFFSERV_REVERSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-notification" in payload:
        is_valid, error = _validate_enum_field(
            "block-notification",
            payload["block-notification"],
            VALID_BODY_BLOCK_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr-negate",
            payload["srcaddr-negate"],
            VALID_BODY_SRCADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr6-negate",
            payload["srcaddr6-negate"],
            VALID_BODY_SRCADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr-negate",
            payload["dstaddr-negate"],
            VALID_BODY_DSTADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr6-negate",
            payload["dstaddr6-negate"],
            VALID_BODY_DSTADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-ems-tag-negate" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-ems-tag-negate",
            payload["ztna-ems-tag-negate"],
            VALID_BODY_ZTNA_EMS_TAG_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "service-negate",
            payload["service-negate"],
            VALID_BODY_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-negate",
            payload["internet-service-negate"],
            VALID_BODY_INTERNET_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src-negate",
            payload["internet-service-src-negate"],
            VALID_BODY_INTERNET_SERVICE_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-negate",
            payload["internet-service6-negate"],
            VALID_BODY_INTERNET_SERVICE6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src-negate",
            payload["internet-service6-src-negate"],
            VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "timeout-send-rst" in payload:
        is_valid, error = _validate_enum_field(
            "timeout-send-rst",
            payload["timeout-send-rst"],
            VALID_BODY_TIMEOUT_SEND_RST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal-exempt" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal-exempt",
            payload["captive-portal-exempt"],
            VALID_BODY_CAPTIVE_PORTAL_EXEMPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dsri" in payload:
        is_valid, error = _validate_enum_field(
            "dsri",
            payload["dsri"],
            VALID_BODY_DSRI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "radius-mac-auth-bypass",
            payload["radius-mac-auth-bypass"],
            VALID_BODY_RADIUS_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-ip-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "radius-ip-auth-bypass",
            payload["radius-ip-auth-bypass"],
            VALID_BODY_RADIUS_IP_AUTH_BYPASS,
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
    if "sgt-check" in payload:
        is_valid, error = _validate_enum_field(
            "sgt-check",
            payload["sgt-check"],
            VALID_BODY_SGT_CHECK,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_firewall_policy_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update firewall/policy."""
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
    if "action" in payload:
        is_valid, error = _validate_enum_field(
            "action",
            payload["action"],
            VALID_BODY_ACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat64" in payload:
        is_valid, error = _validate_enum_field(
            "nat64",
            payload["nat64"],
            VALID_BODY_NAT64,
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
    if "ztna-status" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-status",
            payload["ztna-status"],
            VALID_BODY_ZTNA_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-device-ownership" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-device-ownership",
            payload["ztna-device-ownership"],
            VALID_BODY_ZTNA_DEVICE_OWNERSHIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-tags-match-logic" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-tags-match-logic",
            payload["ztna-tags-match-logic"],
            VALID_BODY_ZTNA_TAGS_MATCH_LOGIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service",
            payload["internet-service"],
            VALID_BODY_INTERNET_SERVICE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src",
            payload["internet-service-src"],
            VALID_BODY_INTERNET_SERVICE_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reputation-direction" in payload:
        is_valid, error = _validate_enum_field(
            "reputation-direction",
            payload["reputation-direction"],
            VALID_BODY_REPUTATION_DIRECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6",
            payload["internet-service6"],
            VALID_BODY_INTERNET_SERVICE6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src",
            payload["internet-service6-src"],
            VALID_BODY_INTERNET_SERVICE6_SRC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "reputation-direction6" in payload:
        is_valid, error = _validate_enum_field(
            "reputation-direction6",
            payload["reputation-direction6"],
            VALID_BODY_REPUTATION_DIRECTION6,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "rtp-nat" in payload:
        is_valid, error = _validate_enum_field(
            "rtp-nat",
            payload["rtp-nat"],
            VALID_BODY_RTP_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "send-deny-packet" in payload:
        is_valid, error = _validate_enum_field(
            "send-deny-packet",
            payload["send-deny-packet"],
            VALID_BODY_SEND_DENY_PACKET,
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
    if "schedule-timeout" in payload:
        is_valid, error = _validate_enum_field(
            "schedule-timeout",
            payload["schedule-timeout"],
            VALID_BODY_SCHEDULE_TIMEOUT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "policy-expiry" in payload:
        is_valid, error = _validate_enum_field(
            "policy-expiry",
            payload["policy-expiry"],
            VALID_BODY_POLICY_EXPIRY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "tos-negate" in payload:
        is_valid, error = _validate_enum_field(
            "tos-negate",
            payload["tos-negate"],
            VALID_BODY_TOS_NEGATE,
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
    if "tcp-session-without-syn" in payload:
        is_valid, error = _validate_enum_field(
            "tcp-session-without-syn",
            payload["tcp-session-without-syn"],
            VALID_BODY_TCP_SESSION_WITHOUT_SYN,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "geoip-anycast" in payload:
        is_valid, error = _validate_enum_field(
            "geoip-anycast",
            payload["geoip-anycast"],
            VALID_BODY_GEOIP_ANYCAST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "geoip-match" in payload:
        is_valid, error = _validate_enum_field(
            "geoip-match",
            payload["geoip-match"],
            VALID_BODY_GEOIP_MATCH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dynamic-shaping" in payload:
        is_valid, error = _validate_enum_field(
            "dynamic-shaping",
            payload["dynamic-shaping"],
            VALID_BODY_DYNAMIC_SHAPING,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "passive-wan-health-measurement" in payload:
        is_valid, error = _validate_enum_field(
            "passive-wan-health-measurement",
            payload["passive-wan-health-measurement"],
            VALID_BODY_PASSIVE_WAN_HEALTH_MEASUREMENT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "app-monitor" in payload:
        is_valid, error = _validate_enum_field(
            "app-monitor",
            payload["app-monitor"],
            VALID_BODY_APP_MONITOR,
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
    if "inspection-mode" in payload:
        is_valid, error = _validate_enum_field(
            "inspection-mode",
            payload["inspection-mode"],
            VALID_BODY_INSPECTION_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "http-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "http-policy-redirect",
            payload["http-policy-redirect"],
            VALID_BODY_HTTP_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssh-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ssh-policy-redirect",
            payload["ssh-policy-redirect"],
            VALID_BODY_SSH_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-policy-redirect" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-policy-redirect",
            payload["ztna-policy-redirect"],
            VALID_BODY_ZTNA_POLICY_REDIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "profile-type" in payload:
        is_valid, error = _validate_enum_field(
            "profile-type",
            payload["profile-type"],
            VALID_BODY_PROFILE_TYPE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic",
            payload["logtraffic"],
            VALID_BODY_LOGTRAFFIC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "logtraffic-start" in payload:
        is_valid, error = _validate_enum_field(
            "logtraffic-start",
            payload["logtraffic-start"],
            VALID_BODY_LOGTRAFFIC_START,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "log-http-transaction" in payload:
        is_valid, error = _validate_enum_field(
            "log-http-transaction",
            payload["log-http-transaction"],
            VALID_BODY_LOG_HTTP_TRANSACTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "capture-packet" in payload:
        is_valid, error = _validate_enum_field(
            "capture-packet",
            payload["capture-packet"],
            VALID_BODY_CAPTURE_PACKET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auto-asic-offload" in payload:
        is_valid, error = _validate_enum_field(
            "auto-asic-offload",
            payload["auto-asic-offload"],
            VALID_BODY_AUTO_ASIC_OFFLOAD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt",
            payload["wanopt"],
            VALID_BODY_WANOPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt-detection" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt-detection",
            payload["wanopt-detection"],
            VALID_BODY_WANOPT_DETECTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "wanopt-passive-opt" in payload:
        is_valid, error = _validate_enum_field(
            "wanopt-passive-opt",
            payload["wanopt-passive-opt"],
            VALID_BODY_WANOPT_PASSIVE_OPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache" in payload:
        is_valid, error = _validate_enum_field(
            "webcache",
            payload["webcache"],
            VALID_BODY_WEBCACHE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "webcache-https" in payload:
        is_valid, error = _validate_enum_field(
            "webcache-https",
            payload["webcache-https"],
            VALID_BODY_WEBCACHE_HTTPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "nat" in payload:
        is_valid, error = _validate_enum_field(
            "nat",
            payload["nat"],
            VALID_BODY_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pcp-outbound" in payload:
        is_valid, error = _validate_enum_field(
            "pcp-outbound",
            payload["pcp-outbound"],
            VALID_BODY_PCP_OUTBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pcp-inbound" in payload:
        is_valid, error = _validate_enum_field(
            "pcp-inbound",
            payload["pcp-inbound"],
            VALID_BODY_PCP_INBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "permit-any-host" in payload:
        is_valid, error = _validate_enum_field(
            "permit-any-host",
            payload["permit-any-host"],
            VALID_BODY_PERMIT_ANY_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "permit-stun-host" in payload:
        is_valid, error = _validate_enum_field(
            "permit-stun-host",
            payload["permit-stun-host"],
            VALID_BODY_PERMIT_STUN_HOST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fixedport" in payload:
        is_valid, error = _validate_enum_field(
            "fixedport",
            payload["fixedport"],
            VALID_BODY_FIXEDPORT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-preserve" in payload:
        is_valid, error = _validate_enum_field(
            "port-preserve",
            payload["port-preserve"],
            VALID_BODY_PORT_PRESERVE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "port-random" in payload:
        is_valid, error = _validate_enum_field(
            "port-random",
            payload["port-random"],
            VALID_BODY_PORT_RANDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ippool" in payload:
        is_valid, error = _validate_enum_field(
            "ippool",
            payload["ippool"],
            VALID_BODY_IPPOOL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "inbound" in payload:
        is_valid, error = _validate_enum_field(
            "inbound",
            payload["inbound"],
            VALID_BODY_INBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "outbound" in payload:
        is_valid, error = _validate_enum_field(
            "outbound",
            payload["outbound"],
            VALID_BODY_OUTBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "natinbound" in payload:
        is_valid, error = _validate_enum_field(
            "natinbound",
            payload["natinbound"],
            VALID_BODY_NATINBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "natoutbound" in payload:
        is_valid, error = _validate_enum_field(
            "natoutbound",
            payload["natoutbound"],
            VALID_BODY_NATOUTBOUND,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "fec" in payload:
        is_valid, error = _validate_enum_field(
            "fec",
            payload["fec"],
            VALID_BODY_FEC,
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
    if "ntlm" in payload:
        is_valid, error = _validate_enum_field(
            "ntlm",
            payload["ntlm"],
            VALID_BODY_NTLM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ntlm-guest" in payload:
        is_valid, error = _validate_enum_field(
            "ntlm-guest",
            payload["ntlm-guest"],
            VALID_BODY_NTLM_GUEST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "auth-path" in payload:
        is_valid, error = _validate_enum_field(
            "auth-path",
            payload["auth-path"],
            VALID_BODY_AUTH_PATH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "disclaimer" in payload:
        is_valid, error = _validate_enum_field(
            "disclaimer",
            payload["disclaimer"],
            VALID_BODY_DISCLAIMER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "email-collect" in payload:
        is_valid, error = _validate_enum_field(
            "email-collect",
            payload["email-collect"],
            VALID_BODY_EMAIL_COLLECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-vip" in payload:
        is_valid, error = _validate_enum_field(
            "match-vip",
            payload["match-vip"],
            VALID_BODY_MATCH_VIP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "match-vip-only" in payload:
        is_valid, error = _validate_enum_field(
            "match-vip-only",
            payload["match-vip-only"],
            VALID_BODY_MATCH_VIP_ONLY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-copy" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-copy",
            payload["diffserv-copy"],
            VALID_BODY_DIFFSERV_COPY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-forward" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-forward",
            payload["diffserv-forward"],
            VALID_BODY_DIFFSERV_FORWARD,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "diffserv-reverse" in payload:
        is_valid, error = _validate_enum_field(
            "diffserv-reverse",
            payload["diffserv-reverse"],
            VALID_BODY_DIFFSERV_REVERSE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "block-notification" in payload:
        is_valid, error = _validate_enum_field(
            "block-notification",
            payload["block-notification"],
            VALID_BODY_BLOCK_NOTIFICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr-negate",
            payload["srcaddr-negate"],
            VALID_BODY_SRCADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "srcaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "srcaddr6-negate",
            payload["srcaddr6-negate"],
            VALID_BODY_SRCADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr-negate",
            payload["dstaddr-negate"],
            VALID_BODY_DSTADDR_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dstaddr6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "dstaddr6-negate",
            payload["dstaddr6-negate"],
            VALID_BODY_DSTADDR6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ztna-ems-tag-negate" in payload:
        is_valid, error = _validate_enum_field(
            "ztna-ems-tag-negate",
            payload["ztna-ems-tag-negate"],
            VALID_BODY_ZTNA_EMS_TAG_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "service-negate",
            payload["service-negate"],
            VALID_BODY_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-negate",
            payload["internet-service-negate"],
            VALID_BODY_INTERNET_SERVICE_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service-src-negate",
            payload["internet-service-src-negate"],
            VALID_BODY_INTERNET_SERVICE_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-negate",
            payload["internet-service6-negate"],
            VALID_BODY_INTERNET_SERVICE6_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "internet-service6-src-negate" in payload:
        is_valid, error = _validate_enum_field(
            "internet-service6-src-negate",
            payload["internet-service6-src-negate"],
            VALID_BODY_INTERNET_SERVICE6_SRC_NEGATE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "timeout-send-rst" in payload:
        is_valid, error = _validate_enum_field(
            "timeout-send-rst",
            payload["timeout-send-rst"],
            VALID_BODY_TIMEOUT_SEND_RST,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "captive-portal-exempt" in payload:
        is_valid, error = _validate_enum_field(
            "captive-portal-exempt",
            payload["captive-portal-exempt"],
            VALID_BODY_CAPTIVE_PORTAL_EXEMPT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "dsri" in payload:
        is_valid, error = _validate_enum_field(
            "dsri",
            payload["dsri"],
            VALID_BODY_DSRI,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-mac-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "radius-mac-auth-bypass",
            payload["radius-mac-auth-bypass"],
            VALID_BODY_RADIUS_MAC_AUTH_BYPASS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "radius-ip-auth-bypass" in payload:
        is_valid, error = _validate_enum_field(
            "radius-ip-auth-bypass",
            payload["radius-ip-auth-bypass"],
            VALID_BODY_RADIUS_IP_AUTH_BYPASS,
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
    if "sgt-check" in payload:
        is_valid, error = _validate_enum_field(
            "sgt-check",
            payload["sgt-check"],
            VALID_BODY_SGT_CHECK,
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
    "endpoint": "firewall/policy",
    "category": "cmdb",
    "api_path": "firewall/policy",
    "mkey": "policyid",
    "mkey_type": "integer",
    "help": "Configure IPv4/IPv6 policies.",
    "total_fields": 184,
    "required_fields_count": 3,
    "fields_with_defaults_count": 139,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
