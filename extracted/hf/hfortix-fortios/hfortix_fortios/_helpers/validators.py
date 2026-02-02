"""
Validation helpers for FortiOS API and convenience wrappers.

Provides validators for:
- Generic fields (color, status, enable/disable)
- Network fields (IP, MAC, port, network)
- String and integer ranges
- FortiOS-specific fields (policy ID, schedule names, etc.)
- SSH/SSL proxy settings
"""

import ipaddress
from datetime import datetime
from typing import Any, Union

# ============================================================================
# Generic Field Validators
# ============================================================================


def validate_required_fields(
    payload: dict[str, Any],
    required_fields: list[str],
) -> tuple[bool, list[str]]:
    """
    Validate that required fields are present in payload.

    Args:
        payload: Payload dictionary to validate
        required_fields: List of required field names (in kebab-case)

    Returns:
        Tuple of (is_valid, missing_fields)

    Example:
        >>> payload = {'name': 'test', 'subnet': '10.0.0.0/24'}
        >>> validate_required_fields(payload, ['name', 'subnet'])
        (True, [])
        >>> validate_required_fields(payload, ['name', 'subnet', 'interface'])
        (False, ['interface'])
    """
    missing = [field for field in required_fields if field not in payload]
    return (len(missing) == 0, missing)


def validate_color(color: int) -> None:
    """
    Validate color index for FortiOS objects.

    Used across firewall, system, user, and other objects.

    Args:
        color: Color index (0-32)

    Raises:
        ValueError: If color is out of range

    Example:
        >>> validate_color(10)   # Valid
        >>> validate_color(33)   # Raises ValueError
    """
    if color < 0 or color > 32:
        raise ValueError(f"Color must be between 0 and 32, got {color}")


def validate_status(status: str) -> None:
    """
    Validate status field (enable/disable).

    Used across all FortiOS configuration objects.

    Args:
        status: Status value

    Raises:
        ValueError: If status is not 'enable' or 'disable'

    Example:
        >>> validate_status("enable")   # Valid
        >>> validate_status("invalid")  # Raises ValueError
    """
    if status not in ("enable", "disable"):
        raise ValueError(
            f"Status must be 'enable' or 'disable', got: {status}"
        )


def validate_enable_disable(value: Union[str, None], field_name: str) -> None:
    """
    Validate value is 'enable' or 'disable'.

    Args:
        value: Value to validate
        field_name: Name of the field (for error messages)

    Raises:
        ValueError: If value is not 'enable' or 'disable'

    Example:
        >>> validate_enable_disable("enable", "status")  # OK
        >>> validate_enable_disable("on", "status")  # Raises ValueError
    """
    if value is not None and value not in ("enable", "disable"):
        raise ValueError(
            f"{field_name} must be 'enable' or 'disable', got: {value}"
        )


def validate_string_length(
    value: Union[str, None], max_length: int, field_name: str
) -> None:
    """
    Validate string length does not exceed maximum.

    Args:
        value: String value to validate
        max_length: Maximum allowed length
        field_name: Name of the field (for error messages)

    Raises:
        ValueError: If string exceeds max_length

    Example:
        >>> validate_string_length("test", 10, "name")  # OK
        >>> validate_string_length(
        ...     "very_long_string", 5, "name"
        ... )  # Raises ValueError
    """
    if value is not None and len(value) > max_length:
        raise ValueError(
            f"{field_name} exceeds maximum length of {max_length} characters"
        )


def validate_integer_range(
    value: Union[int, None],
    min_value: int,
    max_value: int,
    field_name: str,
) -> None:
    """
    Validate integer is within specified range.

    Args:
        value: Integer value to validate
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)
        field_name: Name of the field (for error messages)

    Raises:
        ValueError: If value is outside the range

    Example:
        >>> validate_integer_range(50, 1, 100, "timeout")  # OK
        >>> validate_integer_range(150, 1, 100, "timeout")  # Raises ValueError
    """
    if value is not None and not (min_value <= value <= max_value):
        raise ValueError(
            f"{field_name} must be between {min_value} and {max_value}, "
            f"got: {value}"
        )


# ============================================================================
# Network Validators
# ============================================================================


def validate_mac_address(mac: str, allow_wildcard: bool = True) -> None:
    """
    Validate MAC address format.

    Used across firewall, system, and switch-controller objects.

    Args:
        mac: MAC address to validate (format: xx:xx:xx:xx:xx:xx)
        allow_wildcard: Allow 00:00:00:00:00:00 as wildcard (default: True)

    Raises:
        ValueError: If MAC address format is invalid

    Example:
        >>> validate_mac_address("00:11:22:33:44:55")  # Valid
        >>> validate_mac_address("00:00:00:00:00:00")  # Valid wildcard
        >>> validate_mac_address("invalid")  # Raises ValueError
    """
    if not mac:
        raise ValueError("MAC address is required")

    # Check format: xx:xx:xx:xx:xx:xx
    parts = mac.split(":")
    if len(parts) != 6:
        raise ValueError(
            f"MAC address must be in format xx:xx:xx:xx:xx:xx, got: {mac}"
        )

    for part in parts:
        if len(part) != 2:
            raise ValueError(
                f"Each MAC address octet must be 2 hex digits, got: {mac}"
            )
        try:
            int(part, 16)
        except ValueError:
            raise ValueError(
                f"MAC address must contain hex digits (0-9, a-f), got: {mac}"
            )

    # Check if wildcard when not allowed
    if not allow_wildcard and mac.lower() == "00:00:00:00:00:00":
        raise ValueError(
            "Wildcard MAC address (00:00:00:00:00:00) not allowed"
        )


def validate_ip_address(ip: str, allow_wildcard: bool = True) -> None:
    """
    Validate IPv4 address format using Python's ipaddress module.

    Used across firewall, system, router, and VPN objects.

    Args:
        ip: IPv4 address to validate
        allow_wildcard: Allow 0.0.0.0 as wildcard (default: True)

    Raises:
        ValueError: If IP address format is invalid

    Example:
        >>> validate_ip_address("192.168.1.1")  # Valid
        >>> validate_ip_address("0.0.0.0")  # Valid wildcard
        >>> validate_ip_address("invalid")  # Raises ValueError
        >>> validate_ip_address("256.1.1.1")  # Raises ValueError
    """
    if not ip:
        raise ValueError("IP address is required")

    # Try to parse as IPv4 address
    try:
        ip_obj = ipaddress.IPv4Address(ip)
    except (ipaddress.AddressValueError, ValueError) as e:
        raise ValueError(f"Invalid IPv4 address format: {ip}") from e

    # Check if wildcard when not allowed
    if not allow_wildcard and str(ip_obj) == "0.0.0.0":  # nosec B104
        raise ValueError("Wildcard IP address (0.0.0.0) not allowed")


def validate_ipv6_address(ip: str, allow_wildcard: bool = True) -> None:
    """
    Validate IPv6 address format using Python's ipaddress module.

    Used across firewall, system, router, and VPN objects.

    Args:
        ip: IPv6 address to validate
        allow_wildcard: Allow :: as wildcard (default: True)

    Raises:
        ValueError: If IP address format is invalid

    Example:
        >>> validate_ipv6_address("2001:db8::1")  # Valid
        >>> validate_ipv6_address("::")  # Valid wildcard
        >>> validate_ipv6_address("invalid")  # Raises ValueError
    """
    if not ip:
        raise ValueError("IPv6 address is required")

    # Try to parse as IPv6 address
    try:
        ip_obj = ipaddress.IPv6Address(ip)
    except (ipaddress.AddressValueError, ValueError) as e:
        raise ValueError(f"Invalid IPv6 address format: {ip}") from e

    # Check if wildcard when not allowed
    if not allow_wildcard and str(ip_obj) == "::":
        raise ValueError("Wildcard IPv6 address (::) not allowed")


def validate_ip_network(network: str, version: int = 4) -> None:
    """
    Validate IP network/subnet format (CIDR notation).

    Used across firewall, system, router, and VPN objects.

    Args:
        network: IP network in CIDR notation (e.g., '192.168.1.0/24')
        version: IP version (4 or 6, default: 4)

    Raises:
        ValueError: If network format is invalid

    Example:
        >>> validate_ip_network("192.168.1.0/24")  # Valid IPv4
        >>> validate_ip_network("2001:db8::/32", version=6)  # Valid IPv6
        >>> validate_ip_network("invalid")  # Raises ValueError
    """
    if not network:
        raise ValueError("IP network is required")

    try:
        if version == 4:
            ipaddress.IPv4Network(network, strict=False)
        elif version == 6:
            ipaddress.IPv6Network(network, strict=False)
        else:
            raise ValueError(f"IP version must be 4 or 6, got {version}")
    except (
        ipaddress.AddressValueError,
        ipaddress.NetmaskValueError,
        ValueError,
    ) as e:
        raise ValueError(
            f"Invalid IPv{version} network format: {network}"
        ) from e


def validate_port_number(
    port: Union[int, None], field_name: str = "port"
) -> None:
    """
    Validate TCP/UDP port number is within valid range (0-65535).

    This validator is for actual network port numbers used in TCP/UDP
    protocols. For FortiOS integer fields that use 32-bit ranges,
    use validate_integer_range() directly.

    Args:
        port: Port number to validate
        field_name: Name of the field (for error messages)

    Raises:
        ValueError: If port is outside valid range (0-65535)

    Example:
        >>> validate_port_number(22, "ssh_port")  # OK
        >>> validate_port_number(443, "https_port")  # OK
        >>> validate_port_number(70000, "port")  # Raises ValueError
    """
    validate_integer_range(port, 0, 65535, field_name)


# ============================================================================
# Firewall-specific Validators
# ============================================================================


def validate_policy_id(
    policy_id: Union[str, int, None], operation: str = "operation"
) -> None:
    """
    Validate policy ID is provided and within valid range (0 to 4294967295).

    Args:
        policy_id: The policy ID to validate
        operation: Name of the operation (for error messages)

    Raises:
        ValueError: If policy_id is None, empty, or out of range
    """
    if policy_id is None:
        raise ValueError(f"Policy ID is required for {operation} operation")

    if isinstance(policy_id, str) and not policy_id.strip():
        raise ValueError(
            f"Policy ID cannot be empty for {operation} operation"
        )

    try:
        policy_id_int = int(policy_id)
    except (ValueError, TypeError):
        raise ValueError(
            f"Policy ID must be a valid integer, got: {policy_id}"
        )

    if not 0 <= policy_id_int <= 4294967295:
        raise ValueError(
            f"Policy ID must be between 0 and 4294967295, got {policy_id_int}"
        )


def validate_address_pairs(
    srcaddr: Union[str, list, None],
    dstaddr: Union[str, list, None],
    srcaddr6: Union[str, list, None],
    dstaddr6: Union[str, list, None],
) -> None:
    """
    Validate address pairs are complete and at least one pair is provided.

    Args:
        srcaddr: Source IPv4 address(es)
        dstaddr: Destination IPv4 address(es)
        srcaddr6: Source IPv6 address(es)
        dstaddr6: Destination IPv6 address(es)

    Raises:
        ValueError: If address pairs are incomplete or missing
    """
    has_ipv4_src = srcaddr is not None
    has_ipv4_dst = dstaddr is not None
    has_ipv6_src = srcaddr6 is not None
    has_ipv6_dst = dstaddr6 is not None

    if has_ipv4_src and not has_ipv4_dst:
        raise ValueError(
            "IPv4 source address provided ('srcaddr') but destination "
            "address missing: provide 'dstaddr' to complete the IPv4 "
            "address pair."
        )
    if has_ipv4_dst and not has_ipv4_src:
        raise ValueError(
            "IPv4 destination address provided ('dstaddr') but source "
            "address missing: provide 'srcaddr' to complete the IPv4 "
            "address pair."
        )

    if has_ipv6_src and not has_ipv6_dst:
        raise ValueError(
            "IPv6 source address provided ('srcaddr6') but destination "
            "address missing: provide 'dstaddr6' to complete the IPv6 "
            "address pair."
        )
    if has_ipv6_dst and not has_ipv6_src:
        raise ValueError(
            "IPv6 destination address provided ('dstaddr6') but source "
            "address missing: provide 'srcaddr6' to complete the IPv6 "
            "address pair."
        )

    has_ipv4_pair = has_ipv4_src and has_ipv4_dst
    has_ipv6_pair = has_ipv6_src and has_ipv6_dst

    if not has_ipv4_pair and not has_ipv6_pair:
        raise ValueError(
            "At least one complete address pair is required: "
            "provide either ('srcaddr' AND 'dstaddr') for IPv4, "
            "or ('srcaddr6' AND 'dstaddr6') for IPv6, "
            "or both pairs for dual-stack."
        )


def validate_seq_num(
    seq_num: Union[str, int, None], operation: str = "operation"
) -> None:
    """
    Validate sequence number is provided and within valid range
    (0 to 4294967295).

    Args:
        seq_num: The sequence number to validate
        operation: Name of the operation (for error messages)

    Raises:
        ValueError: If seq_num is None, empty, or out of range
    """
    if seq_num is None:
        raise ValueError(
            f"Sequence number is required for {operation} operation"
        )

    if isinstance(seq_num, str) and not seq_num.strip():
        raise ValueError(
            f"Sequence number cannot be empty for {operation} operation"
        )

    try:
        seq_num_int = int(seq_num)
    except (ValueError, TypeError):
        raise ValueError(
            f"Sequence number must be a valid integer, got: {seq_num}"
        )

    if not 0 <= seq_num_int <= 4294967295:
        raise ValueError(
            f"Sequence number must be between 0 and 4294967295, "
            f"got {seq_num_int}"
        )


# ============================================================================
# Schedule Validators
# ============================================================================


def validate_schedule_name(
    name: Union[str, None], operation: str = "operation"
) -> None:
    """
    Validate schedule name (max 31 characters).

    Args:
        name: Schedule name to validate
        operation: Name of the operation (for error messages)

    Raises:
        ValueError: If name is None, empty, or exceeds max length
    """
    if name is None:
        raise ValueError(
            f"Schedule name is required for {operation} operation"
        )

    if isinstance(name, str) and not name.strip():
        raise ValueError(
            f"Schedule name cannot be empty for {operation} operation"
        )

    if isinstance(name, str) and len(name) > 31:
        raise ValueError(
            f"Schedule name must be 31 characters or less, got {len(name)}"
        )


def validate_time_format(time_str: str, field_name: str = "time") -> None:
    """
    Validate time format is HH:MM (00:00-23:59).

    Args:
        time_str: Time string to validate
        field_name: Name of the field (for error messages)

    Raises:
        ValueError: If time format is invalid
    """
    if not time_str:
        raise ValueError(f"{field_name} time is required")

    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError as e:
        raise ValueError(
            f"{field_name} must be in format HH:MM (00:00-23:59), "
            f"got: {time_str}"
        ) from e


def validate_day_names(day_str: str) -> None:
    """
    Validate day names for recurring schedule.

    Args:
        day_str: Space-separated day names

    Raises:
        ValueError: If day names are invalid
    """
    valid_days = {
        "sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "none",
    }

    if not day_str:
        raise ValueError("At least one day must be specified")

    days = day_str.lower().split()
    for day in days:
        if day not in valid_days:
            raise ValueError(
                f"Invalid day '{day}'. Must be one of: "
                f"{', '.join(sorted(valid_days))}"
            )


# ============================================================================
# SSH/SSL Proxy-specific Validators
# ============================================================================


def validate_ssh_host_key_type(key_type: Union[str, None]) -> None:
    """
    Validate SSH host key type.

    Args:
        key_type: Key type to validate

    Raises:
        ValueError: If key type is invalid
    """
    if key_type is not None:
        valid_types = (
            "RSA",
            "DSA",
            "ECDSA",
            "ED25519",
            "RSA-CA",
            "DSA-CA",
            "ECDSA-CA",
            "ED25519-CA",
        )
        if key_type not in valid_types:
            raise ValueError(
                f"type must be one of: {', '.join(valid_types)}, "
                f"got: {key_type}"
            )


def validate_ssh_host_key_status(status: Union[str, None]) -> None:
    """
    Validate SSH host key status.

    Args:
        status: Status to validate

    Raises:
        ValueError: If status is invalid
    """
    if status is not None:
        valid_statuses = ("trusted", "revoked")
        if status not in valid_statuses:
            raise ValueError(
                f"status must be one of: {', '.join(valid_statuses)}, "
                f"got: {status}"
            )


def validate_ssh_host_key_nid(nid: Union[str, None]) -> None:
    """
    Validate SSH ECDSA key NID.

    Args:
        nid: NID to validate

    Raises:
        ValueError: If NID is invalid
    """
    if nid is not None and nid not in ("256", "384", "521"):
        raise ValueError(f"nid must be one of: 256, 384, 521, got: {nid}")


def validate_ssh_host_key_usage(usage: Union[str, None]) -> None:
    """
    Validate SSH host key usage.

    Args:
        usage: Usage to validate

    Raises:
        ValueError: If usage is invalid
    """
    if usage is not None and usage not in (
        "transparent-proxy",
        "access-proxy",
    ):
        raise ValueError(
            f"usage must be one of: transparent-proxy, access-proxy, "
            f"got: {usage}"
        )


def validate_ssh_source(source: Union[str, None]) -> None:
    """
    Validate SSH local CA/key source type.

    Args:
        source: Source type to validate

    Raises:
        ValueError: If source is invalid
    """
    if source is not None and source not in ("built-in", "user"):
        raise ValueError(f"source must be 'built-in' or 'user', got: {source}")


def validate_ssl_dh_bits(dh_bits: Union[str, None]) -> None:
    """
    Validate SSL Diffie-Hellman bits.

    Args:
        dh_bits: DH bits to validate

    Raises:
        ValueError: If DH bits value is invalid
    """
    if dh_bits is not None and dh_bits not in ("768", "1024", "1536", "2048"):
        raise ValueError(
            f"ssl_dh_bits must be one of: 768, 1024, 1536, 2048, "
            f"got: {dh_bits}"
        )


def validate_ssl_cipher_action(action: Union[str, None]) -> None:
    """
    Validate SSL no-matching-cipher action.

    Args:
        action: Action to validate

    Raises:
        ValueError: If action is invalid
    """
    if action is not None and action not in ("bypass", "drop"):
        raise ValueError(
            f"no_matching_cipher_action must be 'bypass' or 'drop', "
            f"got: {action}"
        )
