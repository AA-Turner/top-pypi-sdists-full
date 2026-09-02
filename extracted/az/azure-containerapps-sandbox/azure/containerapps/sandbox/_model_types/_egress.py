"""Egress policy models — shared between requests and responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class EgressSecretRef:
    """Reference to a sandbox secret to source a header value from."""

    secret_id: str = ""
    secret_key: str | None = None
    format: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressSecretRef | None:
        if not d:
            return None
        return cls(
            secret_id=d.get("secretId", ""),
            secret_key=d.get("secretKey"),
            format=d.get("format"),
        )

    def _to_dict(self) -> dict:
        d: dict = {"secretId": self.secret_id}
        if self.secret_key is not None:
            d["secretKey"] = self.secret_key
        if self.format is not None:
            d["format"] = self.format
        return d

    def validate(self) -> None:
        if not self.secret_id:
            raise ValueError("egress secretRef.secretId must not be empty")


@dataclass
class EgressManagedIdentityRef:
    """Reference to a managed identity to source a header value (token) from."""

    # NOTE: serializes as ``type`` on the wire; ``identity_type`` avoids shadowing
    # the Python builtin.
    identity_type: Literal["SystemAssigned", "UserAssigned"] = "SystemAssigned"
    resource: str = ""
    identity_resource_id: str | None = None
    format: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressManagedIdentityRef | None:
        if not d:
            return None
        return cls(
            identity_type=d.get("type", "SystemAssigned"),
            resource=d.get("resource", ""),
            identity_resource_id=d.get("identityResourceId"),
            format=d.get("format"),
        )

    def _to_dict(self) -> dict:
        d: dict = {"type": self.identity_type, "resource": self.resource}
        if self.identity_resource_id is not None:
            d["identityResourceId"] = self.identity_resource_id
        if self.format is not None:
            d["format"] = self.format
        return d

    def validate(self) -> None:
        if self.identity_type not in ("SystemAssigned", "UserAssigned"):
            raise ValueError(
                "egress managedIdentityRef.type must be 'SystemAssigned' or "
                f"'UserAssigned' (got {self.identity_type!r})"
            )
        if not self.resource:
            raise ValueError(
                "egress managedIdentityRef.resource must not be empty"
            )
        if self.identity_type == "UserAssigned" and not self.identity_resource_id:
            raise ValueError(
                "egress managedIdentityRef.identityResourceId is required when "
                "type is 'UserAssigned'"
            )
        if self.identity_type == "SystemAssigned" and self.identity_resource_id:
            raise ValueError(
                "egress managedIdentityRef.identityResourceId must not be set when "
                "type is 'SystemAssigned'"
            )


@dataclass
class EgressHeaderValueRef:
    """Indirect header value — exactly one of ``secret_ref`` / ``managed_identity_ref``."""

    secret_ref: EgressSecretRef | None = None
    managed_identity_ref: EgressManagedIdentityRef | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressHeaderValueRef | None:
        if not d:
            return None
        return cls(
            secret_ref=EgressSecretRef._from_dict(d.get("secretRef")),
            managed_identity_ref=EgressManagedIdentityRef._from_dict(
                d.get("managedIdentityRef")
            ),
        )

    def _to_dict(self) -> dict:
        d: dict = {}
        if self.secret_ref is not None:
            d["secretRef"] = self.secret_ref._to_dict()
        if self.managed_identity_ref is not None:
            d["managedIdentityRef"] = self.managed_identity_ref._to_dict()
        return d

    def validate(self) -> None:
        has_secret = self.secret_ref is not None
        has_mi = self.managed_identity_ref is not None
        if has_secret == has_mi:
            raise ValueError(
                "egress valueRef must set exactly one of secretRef or "
                "managedIdentityRef"
            )
        if has_secret:
            self.secret_ref.validate()  # type: ignore[union-attr]
        else:
            self.managed_identity_ref.validate()  # type: ignore[union-attr]


@dataclass
class EgressHeader:
    """Header transform for an egress rule action."""

    operation: Literal["Set", "Insert", "Remove"] = "Set"
    name: str = ""
    value: str | None = None
    value_ref: EgressHeaderValueRef | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressHeader | None:
        if not d:
            return None
        return cls(
            operation=d.get("operation", "Set"),
            name=d.get("name", ""),
            value=d.get("value"),
            value_ref=EgressHeaderValueRef._from_dict(d.get("valueRef")),
        )

    def _to_dict(self) -> dict:
        d: dict = {"operation": self.operation, "name": self.name}
        if self.value is not None:
            d["value"] = self.value
        if self.value_ref is not None:
            d["valueRef"] = self.value_ref._to_dict()
        return d

    def validate(self) -> None:
        if not self.name:
            raise ValueError("egress header.name must not be empty")
        has_value = self.value is not None
        has_ref = self.value_ref is not None
        if has_value and has_ref:
            raise ValueError(
                "egress header must set at most one of value or valueRef "
                f"(header {self.name!r})"
            )
        if self.operation in ("Set", "Insert"):
            if not has_value and not has_ref:
                raise ValueError(
                    f"egress header {self.name!r} with operation "
                    f"{self.operation!r} requires value or valueRef"
                )
        elif self.operation == "Remove":
            if has_value or has_ref:
                raise ValueError(
                    f"egress header {self.name!r} with operation 'Remove' "
                    "must not set value or valueRef"
                )
        if has_ref:
            self.value_ref.validate()  # type: ignore[union-attr]


@dataclass
class EgressRuleMatch:
    """Match conditions for an egress rule."""

    host: str = ""
    path: str | None = None
    methods: list[str] | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressRuleMatch | None:
        if not d:
            return None
        return cls(
            host=d.get("host", ""),
            path=d.get("path"),
            methods=d.get("methods"),
        )

    def _to_dict(self) -> dict:
        d: dict = {"host": self.host}
        if self.path is not None:
            d["path"] = self.path
        if self.methods is not None:
            d["methods"] = self.methods
        return d


@dataclass
class EgressRuleAction:
    """Action for an egress rule (Allow/Deny/Transform/Rewrite)."""

    type: Literal["Allow", "Deny", "Transform", "Rewrite"] = "Allow"
    host: str | None = None
    path: str | None = None
    scheme: str | None = None
    headers: list[EgressHeader] | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressRuleAction | None:
        if not d:
            return None
        raw_headers = d.get("headers")
        headers = (
            [EgressHeader._from_dict(h) for h in raw_headers]
            if raw_headers is not None
            else None
        )
        return cls(
            type=d.get("type", "Allow"),
            host=d.get("host"),
            path=d.get("path"),
            scheme=d.get("scheme"),
            headers=headers,
        )

    def _to_dict(self) -> dict:
        d: dict = {"type": self.type}
        if self.host is not None:
            d["host"] = self.host
        if self.path is not None:
            d["path"] = self.path
        if self.scheme is not None:
            d["scheme"] = self.scheme
        if self.headers is not None:
            d["headers"] = [h._to_dict() for h in self.headers]
        return d


@dataclass
class EgressRule:
    """Advanced egress rule with match conditions and action."""

    name: str | None = None
    match: EgressRuleMatch | None = None
    action: EgressRuleAction | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressRule | None:
        if not d:
            return None
        return cls(
            name=d.get("name"),
            match=EgressRuleMatch._from_dict(d.get("match")),
            action=EgressRuleAction._from_dict(d.get("action")),
        )

    def _to_dict(self) -> dict:
        d: dict = {}
        if self.name is not None:
            d["name"] = self.name
        if self.match is not None:
            d["match"] = self.match._to_dict()
        if self.action is not None:
            d["action"] = self.action._to_dict()
        return d


@dataclass
class EgressHostRule:
    """Simple host-pattern egress rule."""

    pattern: str = ""
    action: Literal["Allow", "Deny"] = "Allow"

    @classmethod
    def _from_dict(cls, d: dict) -> EgressHostRule:
        return cls(pattern=d.get("pattern", ""), action=d.get("action", "Allow"))

    def _to_dict(self) -> dict:
        return {"pattern": self.pattern, "action": self.action}


@dataclass
class EgressPolicy:
    """Egress policy for a sandbox — used for both input and output."""

    default_action: Literal["Allow", "Deny"] = "Allow"
    host_rules: list[EgressHostRule] = field(default_factory=list)
    rules: list[EgressRule] = field(default_factory=list)
    traffic_inspection: Literal["Legacy", "Full", "Partial", "None"] | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressPolicy | None:
        if not d:
            return None
        return cls(
            default_action=d.get("defaultAction", "Allow"),
            host_rules=[EgressHostRule._from_dict(r) for r in d.get("hostRules", [])],
            rules=[EgressRule._from_dict(r) for r in d.get("rules", [])],
            traffic_inspection=d.get("trafficInspection"),
        )

    def _to_dict(self) -> dict:
        d: dict = {"defaultAction": self.default_action}
        if self.host_rules:
            d["hostRules"] = [r._to_dict() for r in self.host_rules]
        if self.rules:
            d["rules"] = [r._to_dict() for r in self.rules]
        if self.traffic_inspection is not None:
            d["trafficInspection"] = self.traffic_inspection
        return d

    def validate(self) -> None:
        for rule in self.rules:
            if rule.action is None or rule.action.headers is None:
                continue
            for header in rule.action.headers:
                header.validate()


# ---- Response-only models (frozen) ----


@dataclass(frozen=True)
class EgressDecisionEntry:
    """A single egress decision audit entry."""

    timestamp: str | None = None
    host: str | None = None
    method: str | None = None
    path: str | None = None
    scheme: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressDecisionEntry | None:
        if not d:
            return None
        return cls(
            timestamp=d.get("timestamp"),
            host=d.get("host"),
            method=d.get("method"),
            path=d.get("path"),
            scheme=d.get("scheme"),
        )


@dataclass(frozen=True)
class EgressDecisions:
    """Egress decision audit log for a sandbox."""

    network_egress: "NetworkEgressDecisions | None" = None
    last_updated: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> EgressDecisions | None:
        if not d:
            return None
        from azure.containerapps.sandbox._model_types._stats import (
            NetworkEgressDecisions as _NED,
        )

        return cls(
            network_egress=_NED._from_dict(d.get("networkEgress")),
            last_updated=d.get("lastUpdated"),
        )
