"""Port models — auth config is shared (input+output), port views differ."""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, field
from typing import Literal

# Server-side limits, mirrored from the ADC service
# (Adc.Common.WebApp.GlobalViews.IpAccessControlLimits /
# PortIpAccessControlValidator). Kept in sync so create/update_ports reject the
# same payloads the per-port add/patch endpoints would — the bulk PUT path does
# not re-run this validation server-side, so the client is the only guard there.
_IP_ACL_MAX_RULES = 10
_IP_ACL_MAX_CIDRS_PER_RULE = 10
_IP_ACL_MIN_PRIORITY = 0
_IP_ACL_MAX_PRIORITY = 1000
_IP_ACL_MAX_RULE_NAME_LEN = 63
# Rule name: start/end alphanumeric, interior alphanumeric or hyphen.
_IP_ACL_RULE_NAME_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$")


# ---- Shared models (input + output) ----


@dataclass
class PortIpAccessControlRule:
    """A single source-IP allow/deny rule for a sandbox port.

    Rules restrict which *inbound* client IPs may reach the port, matched by
    CIDR range. Lower ``priority`` values are evaluated first.
    """

    name: str = ""
    action: Literal["Allow", "Deny"] = "Allow"
    priority: int = 0
    source_cidrs: list[str] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict | None) -> PortIpAccessControlRule | None:
        if not d:
            return None
        return cls(
            name=d.get("name", ""),
            action=d.get("action", "Allow"),
            priority=d.get("priority", 0),
            source_cidrs=d.get("sourceCidrs", []),
        )

    def _to_dict(self) -> dict:
        return {
            "name": self.name,
            "action": self.action,
            "priority": self.priority,
            "sourceCidrs": self.source_cidrs,
        }

    def validate(self) -> None:
        """Validate a single rule, mirroring the server's per-rule checks.

        :raises ValueError: If the name, priority, or source CIDRs are invalid.
        """
        # Name: non-empty, <= 63 chars, DNS-label-like.
        if not self.name or not self.name.strip():
            raise ValueError("ip access control rule name must not be empty")
        if len(self.name) > _IP_ACL_MAX_RULE_NAME_LEN:
            raise ValueError(
                f"ip access control rule name {self.name!r} must be between 1 and "
                f"{_IP_ACL_MAX_RULE_NAME_LEN} characters (got {len(self.name)})"
            )
        if not _IP_ACL_RULE_NAME_RE.match(self.name):
            raise ValueError(
                f"ip access control rule name {self.name!r} must start and end with "
                "an alphanumeric character and contain only alphanumeric characters "
                "and hyphens"
            )
        # Priority range.
        if not _IP_ACL_MIN_PRIORITY <= self.priority <= _IP_ACL_MAX_PRIORITY:
            raise ValueError(
                f"ip access control rule {self.name!r} priority must be between "
                f"{_IP_ACL_MIN_PRIORITY} and {_IP_ACL_MAX_PRIORITY} (got {self.priority})"
            )
        # Source CIDRs: at least one, at most the cap, each a valid network.
        if not self.source_cidrs:
            raise ValueError(
                f"ip access control rule {self.name!r} must have at least one source CIDR"
            )
        if len(self.source_cidrs) > _IP_ACL_MAX_CIDRS_PER_RULE:
            raise ValueError(
                f"ip access control rule {self.name!r} has {len(self.source_cidrs)} "
                f"source CIDRs, maximum is {_IP_ACL_MAX_CIDRS_PER_RULE}"
            )
        for cidr in self.source_cidrs:
            # strict=True mirrors the server's System.Net.IPNetwork.TryParse,
            # which rejects CIDRs with non-zero host bits (e.g. "10.0.0.5/8").
            try:
                ipaddress.ip_network(cidr, strict=True)
            except ValueError as exc:
                raise ValueError(
                    f"source CIDR {cidr!r} in ip access control rule {self.name!r} "
                    f"is not a valid CIDR: {exc}"
                ) from exc


@dataclass
class PortIpAccessControl:
    """Inbound IP access control for a sandbox port.

    ``default_action`` (required) decides traffic that matches no rule — set it
    to ``"Deny"`` to permit only what the ``rules`` allow. Provide ordered
    ``rules`` (by ``priority``) to allow or deny specific source CIDR ranges.

    Example::

        acl = PortIpAccessControl(
            default_action="Deny",
            rules=[
                PortIpAccessControlRule(
                    name="office", action="Allow",
                    priority=10, source_cidrs=["10.0.0.0/8"],
                ),
            ],
        )
        ports = [AddPortRequest(port=8443, ip_access_control=acl)]
    """

    # Required (no default): the reference SDK and the service both declare
    # defaultAction as required. A default of "Allow" would be fail-open — a
    # policy built only from Allow rules would silently permit all other
    # traffic — so callers must state intent explicitly.
    default_action: Literal["Allow", "Deny"]
    rules: list[PortIpAccessControlRule] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict | None) -> PortIpAccessControl | None:
        if not d:
            return None
        # Read path stays lenient: the service always sends defaultAction, but
        # never raise on deserialization. Fall back to "Allow" only to mirror
        # the server's null-config "allow all" semantics for malformed data.
        return cls(
            default_action=d.get("defaultAction", "Allow"),
            rules=[
                r for r in (
                    PortIpAccessControlRule._from_dict(rule)
                    for rule in d.get("rules", [])
                ) if r is not None
            ],
        )

    def _to_dict(self) -> dict:
        return {
            "defaultAction": self.default_action,
            "rules": [r._to_dict() for r in self.rules],
        }

    def validate(self) -> None:
        """Validate the IP access control policy, mirroring the ADC service.

        Enforces the same constraints the server applies on the per-port
        ``add``/``patch`` endpoints — rule count, per-rule validity, and
        uniqueness of rule names (case-insensitive) and priorities — so the
        bulk ``create``/``update_ports`` paths (which the server does not
        re-validate) cannot silently persist an invalid policy.

        :raises ValueError: If the policy or any rule is invalid.
        """
        if len(self.rules) > _IP_ACL_MAX_RULES:
            raise ValueError(
                f"ip access control allows at most {_IP_ACL_MAX_RULES} rules "
                f"(got {len(self.rules)})"
            )
        seen_names: set[str] = set()
        seen_priorities: set[int] = set()
        for rule in self.rules:
            rule.validate()
            lowered = rule.name.lower()
            if lowered in seen_names:
                raise ValueError(
                    f"duplicate ip access control rule name {rule.name!r} "
                    "(names must be unique, case-insensitive)"
                )
            seen_names.add(lowered)
            if rule.priority in seen_priorities:
                raise ValueError(
                    f"duplicate ip access control rule priority {rule.priority} "
                    "(priorities must be unique)"
                )
            seen_priorities.add(rule.priority)


@dataclass
class PortAuthEntraId:
    """Entra ID authentication config for a port."""

    enabled: bool = False
    emails: list[str] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict | None) -> PortAuthEntraId | None:
        if not d:
            return None
        return cls(enabled=d.get("enabled", False), emails=d.get("emails", []))

    def _to_dict(self) -> dict:
        return {"enabled": self.enabled, "emails": self.emails}


@dataclass
class PortAuthConfig:
    """Authentication configuration for a sandbox port.

    Use ``anonymous=True`` for unauthenticated access, or provide
    ``entra_id`` for Entra ID-based access control.

    :raises ValueError: If both ``anonymous`` and ``entra_id`` are set.
    """

    anonymous: bool | None = None
    entra_id: PortAuthEntraId | None = None

    def __post_init__(self) -> None:
        if self.anonymous and self.entra_id is not None:
            raise ValueError("Cannot set both anonymous=True and entra_id")

    @classmethod
    def _from_dict(cls, d: dict | None) -> PortAuthConfig | None:
        if not d:
            return None
        return cls(
            anonymous=d.get("anonymous"),
            entra_id=PortAuthEntraId._from_dict(d.get("entraId")),
        )

    def _to_dict(self) -> dict:
        d: dict = {}
        if self.anonymous is not None:
            d["anonymous"] = self.anonymous
        if self.entra_id is not None:
            d["entraId"] = self.entra_id._to_dict()
        return d


# ---- Response-only model (frozen) ----


@dataclass(frozen=True)
class SandboxPort:
    """A port exposed by a sandbox (response model)."""

    port: int = 0
    host_port: int | None = None
    protocol: Literal["Http", "Http2"] | None = None
    url: str | None = None
    auth: PortAuthConfig | None = None
    ip_access_control: PortIpAccessControl | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> SandboxPort:
        return cls(
            port=d.get("port", 0),
            host_port=d.get("hostPort"),
            protocol=d.get("protocol"),
            url=d.get("url"),
            auth=PortAuthConfig._from_dict(d.get("auth")),
            ip_access_control=PortIpAccessControl._from_dict(d.get("ipAccessControl")),
        )


# ---- Input-only model ----


@dataclass
class AddPortRequest:
    """Port specification for creating or updating ports.

    Example::

        ports = [
            AddPortRequest(port=8080, auth=PortAuthConfig(anonymous=True)),
            AddPortRequest(port=3000, protocol="Http2"),
            AddPortRequest(
                port=8443,
                ip_access_control=PortIpAccessControl(
                    default_action="Deny",
                    rules=[PortIpAccessControlRule(
                        name="office", action="Allow",
                        priority=10, source_cidrs=["10.0.0.0/8"])],
                ),
            ),
        ]
        sandbox.update_ports(ports)
    """

    port: int = 0
    auth: PortAuthConfig | None = None
    protocol: Literal["Http", "Http2"] | None = None
    activation_mode: Literal["Manual", "OnDemand"] | None = None
    ip_access_control: PortIpAccessControl | None = None

    def _to_dict(self) -> dict:
        d: dict = {"port": self.port}
        if self.auth is not None:
            d["auth"] = self.auth._to_dict()
        if self.protocol is not None:
            d["protocol"] = self.protocol
        if self.activation_mode is not None:
            d["activationMode"] = self.activation_mode
        if self.ip_access_control is not None:
            # Validate at the serialization chokepoint so every write path
            # (create, update_ports) enforces the server's rules — the bulk
            # PUT is not re-validated server-side.
            self.ip_access_control.validate()
            d["ipAccessControl"] = self.ip_access_control._to_dict()
        return d
