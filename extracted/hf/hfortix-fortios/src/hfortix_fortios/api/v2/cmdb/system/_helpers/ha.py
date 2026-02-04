"""Validation helpers for system/ha - Auto-generated"""

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
    "ipsec-phase2-proposal",  # IPsec phase2 proposal.
]

# Fields with defaults (optional)
FIELDS_WITH_DEFAULTS = {
    "group-id": 0,
    "group-name": "",
    "mode": "standalone",
    "sync-packet-balance": "disable",
    "hbdev": "",
    "unicast-hb": "disable",
    "unicast-hb-peerip": "0.0.0.0",
    "unicast-hb-netmask": "0.0.0.0",
    "session-sync-dev": "",
    "route-ttl": 10,
    "route-wait": 0,
    "route-hold": 10,
    "multicast-ttl": 600,
    "evpn-ttl": 60,
    "load-balance-all": "disable",
    "sync-config": "enable",
    "encryption": "disable",
    "authentication": "disable",
    "hb-interval": 2,
    "hb-interval-in-milliseconds": "100ms",
    "hb-lost-threshold": 20,
    "hello-holddown": 20,
    "gratuitous-arps": "enable",
    "arps": 5,
    "arps-interval": 8,
    "session-pickup": "disable",
    "session-pickup-connectionless": "disable",
    "session-pickup-expectation": "disable",
    "session-pickup-nat": "disable",
    "session-pickup-delay": "disable",
    "link-failed-signal": "disable",
    "upgrade-mode": "uninterruptible",
    "uninterruptible-primary-wait": 30,
    "standalone-mgmt-vdom": "disable",
    "ha-mgmt-status": "disable",
    "ha-eth-type": "8890",
    "hc-eth-type": "8891",
    "l2ep-eth-type": "8893",
    "ha-uptime-diff-margin": 300,
    "standalone-config-sync": "disable",
    "unicast-status": "disable",
    "unicast-gateway": "0.0.0.0",
    "schedule": "round-robin",
    "weight": "0 40",
    "cpu-threshold": "",
    "memory-threshold": "",
    "http-proxy-threshold": "",
    "ftp-proxy-threshold": "",
    "imap-proxy-threshold": "",
    "nntp-proxy-threshold": "",
    "pop3-proxy-threshold": "",
    "smtp-proxy-threshold": "",
    "override": "disable",
    "priority": 128,
    "override-wait-time": 0,
    "monitor": "",
    "pingserver-monitor-interface": "",
    "pingserver-failover-threshold": 0,
    "pingserver-secondary-force-reset": "enable",
    "pingserver-flip-timeout": 60,
    "vcluster-status": "disable",
    "ha-direct": "disable",
    "ssd-failover": "disable",
    "memory-compatible-mode": "disable",
    "memory-based-failover": "disable",
    "memory-failover-threshold": 0,
    "memory-failover-monitor-period": 60,
    "memory-failover-sample-rate": 1,
    "memory-failover-flip-timeout": 6,
    "failover-hold-time": 0,
    "check-secondary-dev-health": "disable",
    "ipsec-phase2-proposal": "",
    "bounce-intf-upon-failover": "disable",
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
    "group-id": "integer",  # HA group ID  (0 - 1023;  or 0 - 7 when there are more than 2 vclusters). Must be
    "group-name": "string",  # Cluster group name. Must be the same for all members.
    "mode": "option",  # HA mode. Must be the same for all members. FGSP requires standalone.
    "sync-packet-balance": "option",  # Enable/disable HA packet distribution to multiple CPUs.
    "password": "password",  # Cluster password. Must be the same for all members.
    "key": "password",  # Key.
    "hbdev": "user",  # Heartbeat interfaces. Must be the same for all members.
    "auto-virtual-mac-interface": "string",  # The physical interface that will be assigned an auto-generated virtual MAC addre
    "backup-hbdev": "string",  # Backup heartbeat interfaces. Must be the same for all members.
    "unicast-hb": "option",  # Enable/disable unicast heartbeat.
    "unicast-hb-peerip": "ipv4-address",  # Unicast heartbeat peer IP.
    "unicast-hb-netmask": "ipv4-netmask",  # Unicast heartbeat netmask.
    "session-sync-dev": "user",  # Offload session-sync process to kernel and sync sessions using connected interfa
    "route-ttl": "integer",  # TTL for primary unit routes (5 - 3600 sec). Increase to maintain active routes d
    "route-wait": "integer",  # Time to wait before sending new routes to the cluster (0 - 3600 sec).
    "route-hold": "integer",  # Time to wait between routing table updates to the cluster (0 - 3600 sec).
    "multicast-ttl": "integer",  # HA multicast TTL on primary (5 - 3600 sec).
    "evpn-ttl": "integer",  # HA EVPN FDB TTL on primary box (5 - 3600 sec).
    "load-balance-all": "option",  # Enable to load balance TCP sessions. Disable to load balance proxy sessions only
    "sync-config": "option",  # Enable/disable configuration synchronization.
    "encryption": "option",  # Enable/disable heartbeat message encryption.
    "authentication": "option",  # Enable/disable heartbeat message authentication.
    "hb-interval": "integer",  # Time between sending heartbeat packets (1 - 20). Increase to reduce false positi
    "hb-interval-in-milliseconds": "option",  # Units of heartbeat interval time between sending heartbeat packets. Default is 1
    "hb-lost-threshold": "integer",  # Number of lost heartbeats to signal a failure (1 - 60). Increase to reduce false
    "hello-holddown": "integer",  # Time to wait before changing from hello to work state (5 - 300 sec).
    "gratuitous-arps": "option",  # Enable/disable gratuitous ARPs. Disable if link-failed-signal enabled.
    "arps": "integer",  # Number of gratuitous ARPs (1 - 60). Lower to reduce traffic. Higher to reduce fa
    "arps-interval": "integer",  # Time between gratuitous ARPs  (1 - 20 sec). Lower to reduce failover time. Highe
    "session-pickup": "option",  # Enable/disable session pickup. Enabling it can reduce session down time when fai
    "session-pickup-connectionless": "option",  # Enable/disable UDP and ICMP session sync.
    "session-pickup-expectation": "option",  # Enable/disable session helper expectation session sync for FGSP.
    "session-pickup-nat": "option",  # Enable/disable NAT session sync for FGSP.
    "session-pickup-delay": "option",  # Enable to sync sessions longer than 30 sec. Only longer lived sessions need to b
    "link-failed-signal": "option",  # Enable to shut down all interfaces for 1 sec after a failover. Use if gratuitous
    "upgrade-mode": "option",  # The mode to upgrade a cluster.
    "uninterruptible-primary-wait": "integer",  # Number of minutes the primary HA unit waits before the secondary HA unit is cons
    "standalone-mgmt-vdom": "option",  # Enable/disable standalone management VDOM.
    "ha-mgmt-status": "option",  # Enable to reserve interfaces to manage individual cluster units.
    "ha-mgmt-interfaces": "string",  # Reserve interfaces to manage individual cluster units.
    "ha-eth-type": "string",  # HA heartbeat packet Ethertype (4-digit hex).
    "hc-eth-type": "string",  # Transparent mode HA heartbeat packet Ethertype (4-digit hex).
    "l2ep-eth-type": "string",  # Telnet session HA heartbeat packet Ethertype (4-digit hex).
    "ha-uptime-diff-margin": "integer",  # Normally you would only reduce this value for failover testing.
    "standalone-config-sync": "option",  # Enable/disable FGSP configuration synchronization.
    "unicast-status": "option",  # Enable/disable unicast connection.
    "unicast-gateway": "ipv4-address",  # Default route gateway for unicast interface.
    "unicast-peers": "string",  # Number of unicast peers.
    "schedule": "option",  # Type of A-A load balancing. Use none if you have external load balancers.
    "weight": "user",  # Weight-round-robin weight for each cluster unit. Syntax <priority> <weight>.
    "cpu-threshold": "user",  # Dynamic weighted load balancing CPU usage weight and high and low thresholds.
    "memory-threshold": "user",  # Dynamic weighted load balancing memory usage weight and high and low thresholds.
    "http-proxy-threshold": "user",  # Dynamic weighted load balancing weight and high and low number of HTTP proxy ses
    "ftp-proxy-threshold": "user",  # Dynamic weighted load balancing weight and high and low number of FTP proxy sess
    "imap-proxy-threshold": "user",  # Dynamic weighted load balancing weight and high and low number of IMAP proxy ses
    "nntp-proxy-threshold": "user",  # Dynamic weighted load balancing weight and high and low number of NNTP proxy ses
    "pop3-proxy-threshold": "user",  # Dynamic weighted load balancing weight and high and low number of POP3 proxy ses
    "smtp-proxy-threshold": "user",  # Dynamic weighted load balancing weight and high and low number of SMTP proxy ses
    "override": "option",  # Enable and increase the priority of the unit that should always be primary (mast
    "priority": "integer",  # Increase the priority to select the primary unit (0 - 255).
    "override-wait-time": "integer",  # Delay negotiating if override is enabled (0 - 3600 sec). Reduces how often the c
    "monitor": "user",  # Interfaces to check for port monitoring (or link failure).
    "pingserver-monitor-interface": "user",  # Interfaces to check for remote IP monitoring.
    "pingserver-failover-threshold": "integer",  # Remote IP monitoring failover threshold (0 - 50).
    "pingserver-secondary-force-reset": "option",  # Enable to force the cluster to negotiate after a remote IP monitoring failover.
    "pingserver-flip-timeout": "integer",  # Time to wait in minutes before renegotiating after a remote IP monitoring failov
    "vcluster-status": "option",  # Enable/disable virtual cluster for virtual clustering.
    "vcluster": "string",  # Virtual cluster table.
    "ha-direct": "option",  # Enable/disable using ha-mgmt interface for syslog, remote authentication (RADIUS
    "ssd-failover": "option",  # Enable/disable automatic HA failover on SSD disk failure.
    "memory-compatible-mode": "option",  # Enable/disable memory compatible mode.
    "memory-based-failover": "option",  # Enable/disable memory based failover.
    "memory-failover-threshold": "integer",  # Memory usage threshold to trigger memory based failover (0 means using conserve 
    "memory-failover-monitor-period": "integer",  # Duration of high memory usage before memory based failover is triggered in secon
    "memory-failover-sample-rate": "integer",  # Rate at which memory usage is sampled in order to measure memory usage in second
    "memory-failover-flip-timeout": "integer",  # Time to wait between subsequent memory based failovers in minutes (6 - 214748364
    "failover-hold-time": "integer",  # Time to wait before failover (0 - 300 sec, default = 0), to avoid flip.
    "check-secondary-dev-health": "option",  # Enable/disable secondary dev health check for session load-balance in HA A-A mod
    "ipsec-phase2-proposal": "option",  # IPsec phase2 proposal.
    "bounce-intf-upon-failover": "option",  # Enable/disable notification of kernel to bring down and up all monitored interfa
    "status": "key",  # list ha status information
}

# Field descriptions (help text from FortiOS API)
FIELD_DESCRIPTIONS = {
    "group-id": "HA group ID  (0 - 1023;  or 0 - 7 when there are more than 2 vclusters). Must be the same for all members.",
    "group-name": "Cluster group name. Must be the same for all members.",
    "mode": "HA mode. Must be the same for all members. FGSP requires standalone.",
    "sync-packet-balance": "Enable/disable HA packet distribution to multiple CPUs.",
    "password": "Cluster password. Must be the same for all members.",
    "key": "Key.",
    "hbdev": "Heartbeat interfaces. Must be the same for all members.",
    "auto-virtual-mac-interface": "The physical interface that will be assigned an auto-generated virtual MAC address.",
    "backup-hbdev": "Backup heartbeat interfaces. Must be the same for all members.",
    "unicast-hb": "Enable/disable unicast heartbeat.",
    "unicast-hb-peerip": "Unicast heartbeat peer IP.",
    "unicast-hb-netmask": "Unicast heartbeat netmask.",
    "session-sync-dev": "Offload session-sync process to kernel and sync sessions using connected interface(s) directly.",
    "route-ttl": "TTL for primary unit routes (5 - 3600 sec). Increase to maintain active routes during failover.",
    "route-wait": "Time to wait before sending new routes to the cluster (0 - 3600 sec).",
    "route-hold": "Time to wait between routing table updates to the cluster (0 - 3600 sec).",
    "multicast-ttl": "HA multicast TTL on primary (5 - 3600 sec).",
    "evpn-ttl": "HA EVPN FDB TTL on primary box (5 - 3600 sec).",
    "load-balance-all": "Enable to load balance TCP sessions. Disable to load balance proxy sessions only.",
    "sync-config": "Enable/disable configuration synchronization.",
    "encryption": "Enable/disable heartbeat message encryption.",
    "authentication": "Enable/disable heartbeat message authentication.",
    "hb-interval": "Time between sending heartbeat packets (1 - 20). Increase to reduce false positives.",
    "hb-interval-in-milliseconds": "Units of heartbeat interval time between sending heartbeat packets. Default is 100ms.",
    "hb-lost-threshold": "Number of lost heartbeats to signal a failure (1 - 60). Increase to reduce false positives.",
    "hello-holddown": "Time to wait before changing from hello to work state (5 - 300 sec).",
    "gratuitous-arps": "Enable/disable gratuitous ARPs. Disable if link-failed-signal enabled.",
    "arps": "Number of gratuitous ARPs (1 - 60). Lower to reduce traffic. Higher to reduce failover time.",
    "arps-interval": "Time between gratuitous ARPs  (1 - 20 sec). Lower to reduce failover time. Higher to reduce traffic.",
    "session-pickup": "Enable/disable session pickup. Enabling it can reduce session down time when fail over happens.",
    "session-pickup-connectionless": "Enable/disable UDP and ICMP session sync.",
    "session-pickup-expectation": "Enable/disable session helper expectation session sync for FGSP.",
    "session-pickup-nat": "Enable/disable NAT session sync for FGSP.",
    "session-pickup-delay": "Enable to sync sessions longer than 30 sec. Only longer lived sessions need to be synced.",
    "link-failed-signal": "Enable to shut down all interfaces for 1 sec after a failover. Use if gratuitous ARPs do not update network.",
    "upgrade-mode": "The mode to upgrade a cluster.",
    "uninterruptible-primary-wait": "Number of minutes the primary HA unit waits before the secondary HA unit is considered upgraded and the system is started before starting its own upgrade (15 - 300, default = 30).",
    "standalone-mgmt-vdom": "Enable/disable standalone management VDOM.",
    "ha-mgmt-status": "Enable to reserve interfaces to manage individual cluster units.",
    "ha-mgmt-interfaces": "Reserve interfaces to manage individual cluster units.",
    "ha-eth-type": "HA heartbeat packet Ethertype (4-digit hex).",
    "hc-eth-type": "Transparent mode HA heartbeat packet Ethertype (4-digit hex).",
    "l2ep-eth-type": "Telnet session HA heartbeat packet Ethertype (4-digit hex).",
    "ha-uptime-diff-margin": "Normally you would only reduce this value for failover testing.",
    "standalone-config-sync": "Enable/disable FGSP configuration synchronization.",
    "unicast-status": "Enable/disable unicast connection.",
    "unicast-gateway": "Default route gateway for unicast interface.",
    "unicast-peers": "Number of unicast peers.",
    "schedule": "Type of A-A load balancing. Use none if you have external load balancers.",
    "weight": "Weight-round-robin weight for each cluster unit. Syntax <priority> <weight>.",
    "cpu-threshold": "Dynamic weighted load balancing CPU usage weight and high and low thresholds.",
    "memory-threshold": "Dynamic weighted load balancing memory usage weight and high and low thresholds.",
    "http-proxy-threshold": "Dynamic weighted load balancing weight and high and low number of HTTP proxy sessions.",
    "ftp-proxy-threshold": "Dynamic weighted load balancing weight and high and low number of FTP proxy sessions.",
    "imap-proxy-threshold": "Dynamic weighted load balancing weight and high and low number of IMAP proxy sessions.",
    "nntp-proxy-threshold": "Dynamic weighted load balancing weight and high and low number of NNTP proxy sessions.",
    "pop3-proxy-threshold": "Dynamic weighted load balancing weight and high and low number of POP3 proxy sessions.",
    "smtp-proxy-threshold": "Dynamic weighted load balancing weight and high and low number of SMTP proxy sessions.",
    "override": "Enable and increase the priority of the unit that should always be primary (master).",
    "priority": "Increase the priority to select the primary unit (0 - 255).",
    "override-wait-time": "Delay negotiating if override is enabled (0 - 3600 sec). Reduces how often the cluster negotiates.",
    "monitor": "Interfaces to check for port monitoring (or link failure).",
    "pingserver-monitor-interface": "Interfaces to check for remote IP monitoring.",
    "pingserver-failover-threshold": "Remote IP monitoring failover threshold (0 - 50).",
    "pingserver-secondary-force-reset": "Enable to force the cluster to negotiate after a remote IP monitoring failover.",
    "pingserver-flip-timeout": "Time to wait in minutes before renegotiating after a remote IP monitoring failover.",
    "vcluster-status": "Enable/disable virtual cluster for virtual clustering.",
    "vcluster": "Virtual cluster table.",
    "ha-direct": "Enable/disable using ha-mgmt interface for syslog, remote authentication (RADIUS), FortiAnalyzer, FortiSandbox, sFlow, and Netflow.",
    "ssd-failover": "Enable/disable automatic HA failover on SSD disk failure.",
    "memory-compatible-mode": "Enable/disable memory compatible mode.",
    "memory-based-failover": "Enable/disable memory based failover.",
    "memory-failover-threshold": "Memory usage threshold to trigger memory based failover (0 means using conserve mode threshold in system.global).",
    "memory-failover-monitor-period": "Duration of high memory usage before memory based failover is triggered in seconds (1 - 300, default = 60).",
    "memory-failover-sample-rate": "Rate at which memory usage is sampled in order to measure memory usage in seconds (1 - 60, default = 1).",
    "memory-failover-flip-timeout": "Time to wait between subsequent memory based failovers in minutes (6 - 2147483647, default = 6).",
    "failover-hold-time": "Time to wait before failover (0 - 300 sec, default = 0), to avoid flip.",
    "check-secondary-dev-health": "Enable/disable secondary dev health check for session load-balance in HA A-A mode.",
    "ipsec-phase2-proposal": "IPsec phase2 proposal.",
    "bounce-intf-upon-failover": "Enable/disable notification of kernel to bring down and up all monitored interfaces. The setting is used during failovers if gratuitous ARPs do not update the network.",
    "status": "list ha status information",
}

# Field constraints (string lengths, integer ranges)
FIELD_CONSTRAINTS = {
    "group-id": {"type": "integer", "min": 0, "max": 1023},
    "group-name": {"type": "string", "max_length": 32},
    "route-ttl": {"type": "integer", "min": 5, "max": 3600},
    "route-wait": {"type": "integer", "min": 0, "max": 3600},
    "route-hold": {"type": "integer", "min": 0, "max": 3600},
    "multicast-ttl": {"type": "integer", "min": 5, "max": 3600},
    "evpn-ttl": {"type": "integer", "min": 5, "max": 3600},
    "hb-interval": {"type": "integer", "min": 1, "max": 20},
    "hb-lost-threshold": {"type": "integer", "min": 1, "max": 60},
    "hello-holddown": {"type": "integer", "min": 5, "max": 300},
    "arps": {"type": "integer", "min": 1, "max": 60},
    "arps-interval": {"type": "integer", "min": 1, "max": 20},
    "uninterruptible-primary-wait": {"type": "integer", "min": 15, "max": 300},
    "ha-eth-type": {"type": "string", "max_length": 4},
    "hc-eth-type": {"type": "string", "max_length": 4},
    "l2ep-eth-type": {"type": "string", "max_length": 4},
    "ha-uptime-diff-margin": {"type": "integer", "min": 1, "max": 65535},
    "priority": {"type": "integer", "min": 0, "max": 255},
    "override-wait-time": {"type": "integer", "min": 0, "max": 3600},
    "pingserver-failover-threshold": {"type": "integer", "min": 0, "max": 50},
    "pingserver-flip-timeout": {"type": "integer", "min": 6, "max": 2147483647},
    "memory-failover-threshold": {"type": "integer", "min": 0, "max": 95},
    "memory-failover-monitor-period": {"type": "integer", "min": 1, "max": 300},
    "memory-failover-sample-rate": {"type": "integer", "min": 1, "max": 60},
    "memory-failover-flip-timeout": {"type": "integer", "min": 6, "max": 2147483647},
    "failover-hold-time": {"type": "integer", "min": 0, "max": 300},
}

# Nested schemas (for table/list fields with children)
NESTED_SCHEMAS = {
    "auto-virtual-mac-interface": {
        "interface-name": {
            "type": "string",
            "help": "Interface name.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
    },
    "backup-hbdev": {
        "name": {
            "type": "string",
            "help": "Interface name.",
            "default": "",
            "max_length": 79,
        },
    },
    "ha-mgmt-interfaces": {
        "id": {
            "type": "integer",
            "help": "Table ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "interface": {
            "type": "string",
            "help": "Interface to reserve for HA management.",
            "required": True,
            "default": "",
            "max_length": 15,
        },
        "dst": {
            "type": "ipv4-classnet",
            "help": "Default route destination for reserved HA management interface.",
            "default": "0.0.0.0 0.0.0.0",
        },
        "gateway": {
            "type": "ipv4-address",
            "help": "Default route gateway for reserved HA management interface.",
            "default": "0.0.0.0",
        },
        "dst6": {
            "type": "ipv6-prefix",
            "help": "Default IPv6 destination for reserved HA management interface.",
            "default": "::/0",
        },
        "gateway6": {
            "type": "ipv6-address",
            "help": "Default IPv6 gateway for reserved HA management interface.",
            "default": "::",
        },
    },
    "unicast-peers": {
        "id": {
            "type": "integer",
            "help": "Table ID.",
            "default": 0,
            "min_value": 0,
            "max_value": 4294967295,
        },
        "peer-ip": {
            "type": "ipv4-address",
            "help": "Unicast peer IP.",
            "default": "0.0.0.0",
        },
    },
    "vcluster": {
        "vcluster-id": {
            "type": "integer",
            "help": "ID.",
            "default": 1,
            "min_value": 1,
            "max_value": 30,
        },
        "override": {
            "type": "option",
            "help": "Enable and increase the priority of the unit that should always be primary (master).",
            "default": "disable",
            "options": ["enable", "disable"],
        },
        "priority": {
            "type": "integer",
            "help": "Increase the priority to select the primary unit (0 - 255).",
            "default": 128,
            "min_value": 0,
            "max_value": 255,
        },
        "override-wait-time": {
            "type": "integer",
            "help": "Delay negotiating if override is enabled (0 - 3600 sec). Reduces how often the cluster negotiates.",
            "default": 0,
            "min_value": 0,
            "max_value": 3600,
        },
        "monitor": {
            "type": "user",
            "help": "Interfaces to check for port monitoring (or link failure).",
            "default": "",
        },
        "pingserver-monitor-interface": {
            "type": "user",
            "help": "Interfaces to check for remote IP monitoring.",
            "default": "",
        },
        "pingserver-failover-threshold": {
            "type": "integer",
            "help": "Remote IP monitoring failover threshold (0 - 50).",
            "default": 0,
            "min_value": 0,
            "max_value": 50,
        },
        "pingserver-secondary-force-reset": {
            "type": "option",
            "help": "Enable to force the cluster to negotiate after a remote IP monitoring failover.",
            "default": "enable",
            "options": ["enable", "disable"],
        },
        "pingserver-flip-timeout": {
            "type": "integer",
            "help": "Time to wait in minutes before renegotiating after a remote IP monitoring failover.",
            "default": 60,
            "min_value": 6,
            "max_value": 2147483647,
        },
        "vdom": {
            "type": "string",
            "help": "Virtual domain(s) in the virtual cluster.",
        },
    },
    "status": {
        "vcluster-id": {
            "type": "value",
            "help": "<enter> to show all vcluster or input vcluster-id",
        },
    },
}


# Valid enum values from API documentation
VALID_BODY_MODE = [
    "standalone",
    "a-a",
    "a-p",
]
VALID_BODY_SYNC_PACKET_BALANCE = [
    "enable",
    "disable",
]
VALID_BODY_UNICAST_HB = [
    "enable",
    "disable",
]
VALID_BODY_LOAD_BALANCE_ALL = [
    "enable",
    "disable",
]
VALID_BODY_SYNC_CONFIG = [
    "enable",
    "disable",
]
VALID_BODY_ENCRYPTION = [
    "enable",
    "disable",
]
VALID_BODY_AUTHENTICATION = [
    "enable",
    "disable",
]
VALID_BODY_HB_INTERVAL_IN_MILLISECONDS = [
    "100ms",
    "10ms",
]
VALID_BODY_GRATUITOUS_ARPS = [
    "enable",
    "disable",
]
VALID_BODY_SESSION_PICKUP = [
    "enable",
    "disable",
]
VALID_BODY_SESSION_PICKUP_CONNECTIONLESS = [
    "enable",
    "disable",
]
VALID_BODY_SESSION_PICKUP_EXPECTATION = [
    "enable",
    "disable",
]
VALID_BODY_SESSION_PICKUP_NAT = [
    "enable",
    "disable",
]
VALID_BODY_SESSION_PICKUP_DELAY = [
    "enable",
    "disable",
]
VALID_BODY_LINK_FAILED_SIGNAL = [
    "enable",
    "disable",
]
VALID_BODY_UPGRADE_MODE = [
    "simultaneous",
    "uninterruptible",
    "local-only",
    "secondary-only",
]
VALID_BODY_STANDALONE_MGMT_VDOM = [
    "enable",
    "disable",
]
VALID_BODY_HA_MGMT_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_STANDALONE_CONFIG_SYNC = [
    "enable",
    "disable",
]
VALID_BODY_UNICAST_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_SCHEDULE = [
    "none",
    "leastconnection",
    "round-robin",
    "weight-round-robin",
    "random",
    "ip",
    "ipport",
]
VALID_BODY_OVERRIDE = [
    "enable",
    "disable",
]
VALID_BODY_PINGSERVER_SECONDARY_FORCE_RESET = [
    "enable",
    "disable",
]
VALID_BODY_VCLUSTER_STATUS = [
    "enable",
    "disable",
]
VALID_BODY_HA_DIRECT = [
    "enable",
    "disable",
]
VALID_BODY_SSD_FAILOVER = [
    "enable",
    "disable",
]
VALID_BODY_MEMORY_COMPATIBLE_MODE = [
    "enable",
    "disable",
]
VALID_BODY_MEMORY_BASED_FAILOVER = [
    "enable",
    "disable",
]
VALID_BODY_CHECK_SECONDARY_DEV_HEALTH = [
    "enable",
    "disable",
]
VALID_BODY_IPSEC_PHASE2_PROPOSAL = [
    "aes128-sha1",
    "aes128-sha256",
    "aes128-sha384",
    "aes128-sha512",
    "aes192-sha1",
    "aes192-sha256",
    "aes192-sha384",
    "aes192-sha512",
    "aes256-sha1",
    "aes256-sha256",
    "aes256-sha384",
    "aes256-sha512",
    "aes128gcm",
    "aes256gcm",
    "chacha20poly1305",
]
VALID_BODY_BOUNCE_INTF_UPON_FAILOVER = [
    "enable",
    "disable",
]
VALID_QUERY_ACTION = ["default", "schema"]

# ============================================================================
# GET Validation
# ============================================================================


def validate_system_ha_get(
    attr: str | None = None,
    filters: dict[str, Any] | None = None,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate GET request parameters for system/ha."""
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


def validate_system_ha_post(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate POST request to create new system/ha object."""
    # Step 1: Validate required fields using central function
    is_valid, error = _validate_required_fields(
        payload,
        REQUIRED_FIELDS,
        FIELD_DESCRIPTIONS
    )
    if not is_valid:
        return (False, error)

    # Step 2: Validate enum values using central function
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sync-packet-balance" in payload:
        is_valid, error = _validate_enum_field(
            "sync-packet-balance",
            payload["sync-packet-balance"],
            VALID_BODY_SYNC_PACKET_BALANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unicast-hb" in payload:
        is_valid, error = _validate_enum_field(
            "unicast-hb",
            payload["unicast-hb"],
            VALID_BODY_UNICAST_HB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "load-balance-all" in payload:
        is_valid, error = _validate_enum_field(
            "load-balance-all",
            payload["load-balance-all"],
            VALID_BODY_LOAD_BALANCE_ALL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sync-config" in payload:
        is_valid, error = _validate_enum_field(
            "sync-config",
            payload["sync-config"],
            VALID_BODY_SYNC_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encryption" in payload:
        is_valid, error = _validate_enum_field(
            "encryption",
            payload["encryption"],
            VALID_BODY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hb-interval-in-milliseconds" in payload:
        is_valid, error = _validate_enum_field(
            "hb-interval-in-milliseconds",
            payload["hb-interval-in-milliseconds"],
            VALID_BODY_HB_INTERVAL_IN_MILLISECONDS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gratuitous-arps" in payload:
        is_valid, error = _validate_enum_field(
            "gratuitous-arps",
            payload["gratuitous-arps"],
            VALID_BODY_GRATUITOUS_ARPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup",
            payload["session-pickup"],
            VALID_BODY_SESSION_PICKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-connectionless" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-connectionless",
            payload["session-pickup-connectionless"],
            VALID_BODY_SESSION_PICKUP_CONNECTIONLESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-expectation" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-expectation",
            payload["session-pickup-expectation"],
            VALID_BODY_SESSION_PICKUP_EXPECTATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-nat" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-nat",
            payload["session-pickup-nat"],
            VALID_BODY_SESSION_PICKUP_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-delay" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-delay",
            payload["session-pickup-delay"],
            VALID_BODY_SESSION_PICKUP_DELAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "link-failed-signal" in payload:
        is_valid, error = _validate_enum_field(
            "link-failed-signal",
            payload["link-failed-signal"],
            VALID_BODY_LINK_FAILED_SIGNAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upgrade-mode" in payload:
        is_valid, error = _validate_enum_field(
            "upgrade-mode",
            payload["upgrade-mode"],
            VALID_BODY_UPGRADE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "standalone-mgmt-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "standalone-mgmt-vdom",
            payload["standalone-mgmt-vdom"],
            VALID_BODY_STANDALONE_MGMT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-mgmt-status" in payload:
        is_valid, error = _validate_enum_field(
            "ha-mgmt-status",
            payload["ha-mgmt-status"],
            VALID_BODY_HA_MGMT_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "standalone-config-sync" in payload:
        is_valid, error = _validate_enum_field(
            "standalone-config-sync",
            payload["standalone-config-sync"],
            VALID_BODY_STANDALONE_CONFIG_SYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unicast-status" in payload:
        is_valid, error = _validate_enum_field(
            "unicast-status",
            payload["unicast-status"],
            VALID_BODY_UNICAST_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "schedule" in payload:
        is_valid, error = _validate_enum_field(
            "schedule",
            payload["schedule"],
            VALID_BODY_SCHEDULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override" in payload:
        is_valid, error = _validate_enum_field(
            "override",
            payload["override"],
            VALID_BODY_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pingserver-secondary-force-reset" in payload:
        is_valid, error = _validate_enum_field(
            "pingserver-secondary-force-reset",
            payload["pingserver-secondary-force-reset"],
            VALID_BODY_PINGSERVER_SECONDARY_FORCE_RESET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vcluster-status" in payload:
        is_valid, error = _validate_enum_field(
            "vcluster-status",
            payload["vcluster-status"],
            VALID_BODY_VCLUSTER_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-direct" in payload:
        is_valid, error = _validate_enum_field(
            "ha-direct",
            payload["ha-direct"],
            VALID_BODY_HA_DIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssd-failover" in payload:
        is_valid, error = _validate_enum_field(
            "ssd-failover",
            payload["ssd-failover"],
            VALID_BODY_SSD_FAILOVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "memory-compatible-mode" in payload:
        is_valid, error = _validate_enum_field(
            "memory-compatible-mode",
            payload["memory-compatible-mode"],
            VALID_BODY_MEMORY_COMPATIBLE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "memory-based-failover" in payload:
        is_valid, error = _validate_enum_field(
            "memory-based-failover",
            payload["memory-based-failover"],
            VALID_BODY_MEMORY_BASED_FAILOVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-secondary-dev-health" in payload:
        is_valid, error = _validate_enum_field(
            "check-secondary-dev-health",
            payload["check-secondary-dev-health"],
            VALID_BODY_CHECK_SECONDARY_DEV_HEALTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-phase2-proposal" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-phase2-proposal",
            payload["ipsec-phase2-proposal"],
            VALID_BODY_IPSEC_PHASE2_PROPOSAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bounce-intf-upon-failover" in payload:
        is_valid, error = _validate_enum_field(
            "bounce-intf-upon-failover",
            payload["bounce-intf-upon-failover"],
            VALID_BODY_BOUNCE_INTF_UPON_FAILOVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)

    return (True, None)


# ============================================================================
# PUT Validation
# ============================================================================


def validate_system_ha_put(
    payload: dict,
    **params: Any,
) -> tuple[bool, str | None]:
    """Validate PUT request to update system/ha."""
    # Validate enum values using central function
    if "mode" in payload:
        is_valid, error = _validate_enum_field(
            "mode",
            payload["mode"],
            VALID_BODY_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sync-packet-balance" in payload:
        is_valid, error = _validate_enum_field(
            "sync-packet-balance",
            payload["sync-packet-balance"],
            VALID_BODY_SYNC_PACKET_BALANCE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unicast-hb" in payload:
        is_valid, error = _validate_enum_field(
            "unicast-hb",
            payload["unicast-hb"],
            VALID_BODY_UNICAST_HB,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "load-balance-all" in payload:
        is_valid, error = _validate_enum_field(
            "load-balance-all",
            payload["load-balance-all"],
            VALID_BODY_LOAD_BALANCE_ALL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "sync-config" in payload:
        is_valid, error = _validate_enum_field(
            "sync-config",
            payload["sync-config"],
            VALID_BODY_SYNC_CONFIG,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "encryption" in payload:
        is_valid, error = _validate_enum_field(
            "encryption",
            payload["encryption"],
            VALID_BODY_ENCRYPTION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "authentication" in payload:
        is_valid, error = _validate_enum_field(
            "authentication",
            payload["authentication"],
            VALID_BODY_AUTHENTICATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "hb-interval-in-milliseconds" in payload:
        is_valid, error = _validate_enum_field(
            "hb-interval-in-milliseconds",
            payload["hb-interval-in-milliseconds"],
            VALID_BODY_HB_INTERVAL_IN_MILLISECONDS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "gratuitous-arps" in payload:
        is_valid, error = _validate_enum_field(
            "gratuitous-arps",
            payload["gratuitous-arps"],
            VALID_BODY_GRATUITOUS_ARPS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup",
            payload["session-pickup"],
            VALID_BODY_SESSION_PICKUP,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-connectionless" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-connectionless",
            payload["session-pickup-connectionless"],
            VALID_BODY_SESSION_PICKUP_CONNECTIONLESS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-expectation" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-expectation",
            payload["session-pickup-expectation"],
            VALID_BODY_SESSION_PICKUP_EXPECTATION,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-nat" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-nat",
            payload["session-pickup-nat"],
            VALID_BODY_SESSION_PICKUP_NAT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "session-pickup-delay" in payload:
        is_valid, error = _validate_enum_field(
            "session-pickup-delay",
            payload["session-pickup-delay"],
            VALID_BODY_SESSION_PICKUP_DELAY,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "link-failed-signal" in payload:
        is_valid, error = _validate_enum_field(
            "link-failed-signal",
            payload["link-failed-signal"],
            VALID_BODY_LINK_FAILED_SIGNAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "upgrade-mode" in payload:
        is_valid, error = _validate_enum_field(
            "upgrade-mode",
            payload["upgrade-mode"],
            VALID_BODY_UPGRADE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "standalone-mgmt-vdom" in payload:
        is_valid, error = _validate_enum_field(
            "standalone-mgmt-vdom",
            payload["standalone-mgmt-vdom"],
            VALID_BODY_STANDALONE_MGMT_VDOM,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-mgmt-status" in payload:
        is_valid, error = _validate_enum_field(
            "ha-mgmt-status",
            payload["ha-mgmt-status"],
            VALID_BODY_HA_MGMT_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "standalone-config-sync" in payload:
        is_valid, error = _validate_enum_field(
            "standalone-config-sync",
            payload["standalone-config-sync"],
            VALID_BODY_STANDALONE_CONFIG_SYNC,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "unicast-status" in payload:
        is_valid, error = _validate_enum_field(
            "unicast-status",
            payload["unicast-status"],
            VALID_BODY_UNICAST_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "schedule" in payload:
        is_valid, error = _validate_enum_field(
            "schedule",
            payload["schedule"],
            VALID_BODY_SCHEDULE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "override" in payload:
        is_valid, error = _validate_enum_field(
            "override",
            payload["override"],
            VALID_BODY_OVERRIDE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "pingserver-secondary-force-reset" in payload:
        is_valid, error = _validate_enum_field(
            "pingserver-secondary-force-reset",
            payload["pingserver-secondary-force-reset"],
            VALID_BODY_PINGSERVER_SECONDARY_FORCE_RESET,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "vcluster-status" in payload:
        is_valid, error = _validate_enum_field(
            "vcluster-status",
            payload["vcluster-status"],
            VALID_BODY_VCLUSTER_STATUS,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ha-direct" in payload:
        is_valid, error = _validate_enum_field(
            "ha-direct",
            payload["ha-direct"],
            VALID_BODY_HA_DIRECT,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ssd-failover" in payload:
        is_valid, error = _validate_enum_field(
            "ssd-failover",
            payload["ssd-failover"],
            VALID_BODY_SSD_FAILOVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "memory-compatible-mode" in payload:
        is_valid, error = _validate_enum_field(
            "memory-compatible-mode",
            payload["memory-compatible-mode"],
            VALID_BODY_MEMORY_COMPATIBLE_MODE,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "memory-based-failover" in payload:
        is_valid, error = _validate_enum_field(
            "memory-based-failover",
            payload["memory-based-failover"],
            VALID_BODY_MEMORY_BASED_FAILOVER,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "check-secondary-dev-health" in payload:
        is_valid, error = _validate_enum_field(
            "check-secondary-dev-health",
            payload["check-secondary-dev-health"],
            VALID_BODY_CHECK_SECONDARY_DEV_HEALTH,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "ipsec-phase2-proposal" in payload:
        is_valid, error = _validate_enum_field(
            "ipsec-phase2-proposal",
            payload["ipsec-phase2-proposal"],
            VALID_BODY_IPSEC_PHASE2_PROPOSAL,
            FIELD_DESCRIPTIONS
        )
        if not is_valid:
            return (False, error)
    if "bounce-intf-upon-failover" in payload:
        is_valid, error = _validate_enum_field(
            "bounce-intf-upon-failover",
            payload["bounce-intf-upon-failover"],
            VALID_BODY_BOUNCE_INTF_UPON_FAILOVER,
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
    "endpoint": "system/ha",
    "category": "cmdb",
    "api_path": "system/ha",
    "help": "Configure HA.",
    "total_fields": 81,
    "required_fields_count": 1,
    "fields_with_defaults_count": 73,
}


def get_schema_info() -> dict[str, Any]:
    """Get information about this endpoint schema."""
    return SCHEMA_INFO.copy()
