"""Write-time port defaults and validation shared by both client surfaces."""

from __future__ import annotations

import ipaddress
import logging
import re

from azure.containerapps.sandbox.models import (
    AddPortRequest,
    PortAuthConfig,
    PortIpAccessControl,
    PortIpAccessControlRule,
    PortsListResponse,
    SandboxPort,
)

logger = logging.getLogger("azure.containerapps.sandbox")

# Mirror PortIpAccessControlValidator: bulk writes do not revalidate server-side.
_IP_ACL_MAX_RULES = 10
_IP_ACL_MAX_CIDRS_PER_RULE = 10
_IP_ACL_MIN_PRIORITY = 0
_IP_ACL_MAX_PRIORITY = 1000
_IP_ACL_MAX_RULE_NAME_LEN = 63
_IP_ACL_RULE_NAME_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$")


def _validate_rule(rule: PortIpAccessControlRule) -> None:
    if not rule.name or not rule.name.strip():
        raise ValueError("ip access control rule name must not be empty")
    if len(rule.name) > _IP_ACL_MAX_RULE_NAME_LEN:
        raise ValueError(
            f"ip access control rule name {rule.name!r} must be between 1 and "
            f"{_IP_ACL_MAX_RULE_NAME_LEN} characters (got {len(rule.name)})"
        )
    if not _IP_ACL_RULE_NAME_RE.match(rule.name):
        raise ValueError(
            f"ip access control rule name {rule.name!r} must start and end with "
            "an alphanumeric character and contain only alphanumeric characters "
            "and hyphens"
        )
    if rule.priority is None or not _IP_ACL_MIN_PRIORITY <= rule.priority <= _IP_ACL_MAX_PRIORITY:
        raise ValueError(
            f"ip access control rule {rule.name!r} priority must be between "
            f"{_IP_ACL_MIN_PRIORITY} and {_IP_ACL_MAX_PRIORITY} (got {rule.priority})"
        )
    if not rule.source_cidrs:
        raise ValueError(f"ip access control rule {rule.name!r} must have at least one source CIDR")
    if len(rule.source_cidrs) > _IP_ACL_MAX_CIDRS_PER_RULE:
        raise ValueError(
            f"ip access control rule {rule.name!r} has {len(rule.source_cidrs)} "
            f"source CIDRs, maximum is {_IP_ACL_MAX_CIDRS_PER_RULE}"
        )
    for cidr in rule.source_cidrs:
        try:
            ipaddress.ip_network(cidr, strict=True)
        except ValueError as exc:
            raise ValueError(
                f"source CIDR {cidr!r} in ip access control rule {rule.name!r} " f"is not a valid CIDR: {exc}"
            ) from exc


def validate_port_ip_access_control(policy: PortIpAccessControl) -> None:
    """Validate an inbound IP policy before writing it.

    All facade port writes call this automatically; model construction and
    deserialization do not validate policies.

    :raises ValueError: If the default action, rules, or source CIDRs are invalid.
    """
    # Generated models allow incomplete construction; never infer a fail-open default.
    if policy.default_action not in ("Allow", "Deny"):
        raise ValueError("ip access control default_action must be Allow or Deny")
    rules = policy.rules if policy.rules is not None else []
    if len(rules) > _IP_ACL_MAX_RULES:
        raise ValueError(f"ip access control allows at most {_IP_ACL_MAX_RULES} rules (got {len(rules)})")
    seen_names: set[str] = set()
    seen_priorities: set[int] = set()
    for rule in rules:
        _validate_rule(rule)
        lowered = rule.name.lower()
        if lowered in seen_names:
            raise ValueError(
                f"duplicate ip access control rule name {rule.name!r} " "(names must be unique, case-insensitive)"
            )
        seen_names.add(lowered)
        if rule.priority in seen_priorities:
            raise ValueError(f"duplicate ip access control rule priority {rule.priority} (priorities must be unique)")
        seen_priorities.add(rule.priority)


def _prepare_port(port: AddPortRequest | int) -> AddPortRequest:
    request = AddPortRequest(port=port) if isinstance(port, int) else AddPortRequest(port.as_dict())
    auth = request.auth
    if auth is not None and auth.anonymous and auth.entra_id is not None:
        raise ValueError("Cannot set both anonymous=True and entra_id")
    if auth is not None and auth.anonymous and auth.github is not None:
        raise ValueError("Cannot set both anonymous=True and github")
    if auth is None or not (
        auth.anonymous
        or (auth.entra_id is not None and auth.entra_id.enabled)
        or (auth.github is not None and auth.github.enabled)
    ):
        request.auth = PortAuthConfig(anonymous=True)
    if request.auth.anonymous:
        logger.warning("Port %d exposed with anonymous access - accessible without authentication.", request.port)
    if request.ip_access_control is not None:
        validate_port_ip_access_control(request.ip_access_control)
    return request


def _extract_port_from_response(response: PortsListResponse, requested_port: int) -> SandboxPort:
    ports = response.ports
    if not ports:
        return SandboxPort(port=requested_port)
    return next((port for port in reversed(ports) if port.port == requested_port), ports[-1])
