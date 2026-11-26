"""Validation and HTTP rule editing for generated egress models."""

from __future__ import annotations

from typing import Literal

from azure.containerapps.sandbox.models import (
    EgressHeader,
    EgressHttpPolicy,
    EgressPolicy,
    EgressRule,
    EgressRuleAction,
    EgressRuleMatch,
    EgressSecretRef,
)

_EGRESS_HOST_RULES_MIGRATION_ERROR = (
    "egress host_rules (hostRules) is legacy read-only compatibility data. Remove "
    "host_rules and migrate each entry to EgressRule(match=EgressRuleMatch("
    "host=pattern), action=EgressRuleAction(type=action))."
)
_HOST_RULE_PREFIX = "aca-host-rule-"


def _validate_secret_ref(reference: EgressSecretRef) -> None:
    if not reference.secret_id:
        raise ValueError("egress secretRef.secretId must not be empty")


def _validate_header(header: EgressHeader) -> None:
    if header is None:
        raise ValueError("egress hook authHeaders must not contain null entries")
    if not header.name:
        raise ValueError("egress header.name must not be empty")
    has_value = header.value is not None
    has_ref = header.value_ref is not None
    if has_value and has_ref:
        raise ValueError(f"egress header must set at most one of value or valueRef (header {header.name!r})")
    if header.operation in ("Set", "Insert"):
        if not has_value and not has_ref:
            raise ValueError(
                f"egress header {header.name!r} with operation {header.operation!r} requires value or valueRef"
            )
    elif header.operation == "Remove":
        if has_value or has_ref:
            raise ValueError(f"egress header {header.name!r} with operation 'Remove' must not set value or valueRef")
    else:
        raise ValueError("egress header.operation must be 'Set', 'Insert', or 'Remove'")
    if not has_ref:
        return
    reference = header.value_ref
    has_secret = reference.secret_ref is not None
    has_identity = reference.managed_identity_ref is not None
    if has_secret == has_identity:
        raise ValueError("egress valueRef must set exactly one of secretRef or managedIdentityRef")
    if has_secret:
        _validate_secret_ref(reference.secret_ref)
        return
    identity = reference.managed_identity_ref
    if identity.identity_type not in ("SystemAssigned", "UserAssigned"):
        raise ValueError(
            "egress managedIdentityRef.type must be 'SystemAssigned' or "
            f"'UserAssigned' (got {identity.identity_type!r})"
        )
    if not identity.resource:
        raise ValueError("egress managedIdentityRef.resource must not be empty")
    if identity.identity_type == "UserAssigned" and not identity.identity_resource_id:
        raise ValueError("egress managedIdentityRef.identityResourceId is required when type is 'UserAssigned'")
    if identity.identity_type == "SystemAssigned" and identity.identity_resource_id:
        raise ValueError("egress managedIdentityRef.identityResourceId must not be set when type is 'SystemAssigned'")


def validate_egress_policy(policy: EgressPolicy) -> None:
    """Validate a generated policy before writing it.

    Called automatically by sandbox create and set-egress operations. Raises
    ``ValueError`` for invalid header/secret references or legacy host-rule writes.
    Service-side validation remains authoritative for the complete contract.
    """
    if policy.host_rules or (policy.http is not None and policy.http.host_rules):
        raise ValueError(_EGRESS_HOST_RULES_MIGRATION_ERROR)
    http_rules = policy.http.rules if policy.http is not None else None
    for rule in [*(policy.rules or []), *(http_rules or [])]:
        if rule.action is not None:
            for header in rule.action.headers or []:
                _validate_header(header)
        if rule.hook_ref is not None:
            for header in rule.hook_ref.auth_headers or []:
                _validate_header(header)
    for section in (policy.tds, policy.postgres):
        if section is None:
            continue
        for credential in section.credentials or []:
            if credential.secret_ref is not None:
                _validate_secret_ref(credential.secret_ref)
        for rule in section.rules or []:
            if rule.hook_ref is not None:
                for header in rule.hook_ref.auth_headers or []:
                    _validate_header(header)


def _http_rules(policy: EgressPolicy) -> list[EgressRule]:
    if policy.http is not None:
        if policy.http.rules is None:
            policy.http.rules = []
        return policy.http.rules
    if policy.tds is not None or policy.postgres is not None or policy.transport_rules is not None:
        policy.http = EgressHttpPolicy(
            default_action=policy.default_action or "Allow",
            rules=list(policy.rules or []),
            traffic_inspection=policy.traffic_inspection,
            enforcement_mode=policy.enforcement_mode,
        )
        return policy.http.rules
    if policy.rules is None:
        policy.rules = []
    return policy.rules


def _is_host_fallback(rule: EgressRule) -> bool:
    name = rule.name or ""
    suffix = name.removeprefix(_HOST_RULE_PREFIX)
    return (
        name.startswith(_HOST_RULE_PREFIX)
        and suffix.isascii()
        and suffix.isdigit()
        and not suffix.startswith("0")
        and rule.match is not None
        and rule.match.path is None
        and not rule.match.methods
        and rule.match.scheme is None
        and rule.match.normalize_path is None
        and rule.action is not None
        and rule.action.type in ("Allow", "Deny")
        and rule.action.host is None
        and rule.action.path is None
        and rule.action.scheme is None
        and not rule.action.headers
        and rule.action.routing_mode is None
        and rule.action.forward is None
        and rule.action.forward_proxy is None
        and not rule.proxy_actions
        and rule.hook_ref is None
    )


def _host_fallback_index(policy: EgressPolicy) -> int:
    validate_egress_policy(policy)
    rules = _http_rules(policy)
    first = len(rules)
    for index, rule in enumerate(rules):
        if _is_host_fallback(rule):
            first = min(first, index)
        elif first < len(rules):
            raise ValueError(
                "SDK-generated host fallback rules must remain last when using "
                "egress helpers. Use set_egress_policy to order the policy explicitly "
                "and remove reserved aca-host-rule- names from custom rules."
            )
    return first


def _add_host_rule(policy: EgressPolicy, pattern: str, action: Literal["Allow", "Deny"]) -> None:
    _host_fallback_index(policy)
    rules = _http_rules(policy)
    names = {rule.name for rule in rules}
    index = 1
    while f"{_HOST_RULE_PREFIX}{index}" in names:
        index += 1
    rules.append(
        EgressRule(
            name=f"{_HOST_RULE_PREFIX}{index}",
            match=EgressRuleMatch(host=pattern),
            action=EgressRuleAction(type=action),
        )
    )


def _add_rule(policy: EgressPolicy, rule: EgressRule) -> None:
    index = _host_fallback_index(policy)
    _http_rules(policy).insert(index, rule)
