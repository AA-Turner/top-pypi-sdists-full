"""Egress policy operations for sandbox-scoped client."""
from __future__ import annotations

import logging
from typing import Any, Literal

from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._models import (
    EgressDecisions,
    EgressHeader,
    EgressHostRule,
    EgressPolicy,
    EgressRule,
    EgressRuleAction,
    EgressRuleMatch,
)

logger = logging.getLogger("azure.containerapps.sandbox")


class EgressOperationsMixin:
    """Egress policy operations on a sandbox."""

    @distributed_trace
    def set_egress_policy(self, policy: EgressPolicy, **kwargs: Any) -> EgressPolicy:
        """Set full egress policy.

        Auto-resumes a stopped/suspended sandbox first — the egress
        endpoint returns 409 ``SandboxNotRunning`` otherwise, matching
        the Rust CLI's ``ensure_running_with_client()`` pattern.
        """
        self.ensure_running()
        result = self._dp_post(f"{self._sbx_path}/egresspolicy", policy._to_dict())
        return EgressPolicy._from_dict(result if isinstance(result, dict) else None) or EgressPolicy(default_action="Allow")

    @distributed_trace
    def get_egress_policy(self, **kwargs: Any) -> EgressPolicy:
        """Get current egress policy."""
        raw = self._dp_get(self._sbx_path)
        if isinstance(raw, dict):
            return EgressPolicy._from_dict(raw.get("egressPolicy")) or EgressPolicy(default_action="Allow")
        return EgressPolicy(default_action="Allow")

    @distributed_trace
    def set_egress_default(self, action: Literal["Allow", "Deny"] = "Deny", **kwargs: Any) -> EgressPolicy:
        """Set default egress action (Allow or Deny)."""
        _VALID_ACTIONS = ("Allow", "Deny")
        if action not in _VALID_ACTIONS:
            raise ValueError(f"Invalid egress action {action!r}. Must be one of {_VALID_ACTIONS}")
        policy = self.get_egress_policy()
        policy.default_action = action
        return self.set_egress_policy(policy)

    @distributed_trace
    def add_egress_host_rule(self, pattern: str, *,
                             action: Literal["Allow", "Deny"] = "Allow",
                             **kwargs: Any) -> EgressPolicy:
        """Add a host allow/deny rule (e.g., '*.github.com')."""
        policy = self.get_egress_policy()
        policy.host_rules.append(EgressHostRule(pattern=pattern, action=action))
        return self.set_egress_policy(policy)

    @distributed_trace
    def add_egress_transform_rule(self, host: str, headers: list[EgressHeader], *,
                                  name: str | None = None,
                                  path: str | None = None,
                                  methods: list[str] | None = None,
                                  **kwargs: Any) -> EgressPolicy:
        """Add a Transform rule that modifies headers on outbound requests."""
        policy = self.get_egress_policy()
        rule = EgressRule(
            name=name,
            match=EgressRuleMatch(host=host, path=path, methods=methods),
            action=EgressRuleAction(type="Transform", headers=list(headers)),
        )
        policy.rules.append(rule)
        return self.set_egress_policy(policy)

    @distributed_trace
    def add_egress_rewrite_rule(self, host: str, *,
                                rewrite_host: str | None = None,
                                rewrite_path: str | None = None,
                                rewrite_scheme: str | None = None,
                                headers: list[EgressHeader] | None = None,
                                name: str | None = None,
                                **kwargs: Any) -> EgressPolicy:
        """Add a Rewrite rule that changes the destination of outbound requests."""
        policy = self.get_egress_policy()
        rule = EgressRule(
            name=name,
            match=EgressRuleMatch(host=host),
            action=EgressRuleAction(
                type="Rewrite",
                host=rewrite_host,
                path=rewrite_path,
                scheme=rewrite_scheme,
                headers=list(headers) if headers else None,
            ),
        )
        policy.rules.append(rule)
        return self.set_egress_policy(policy)

    @distributed_trace
    def get_egress_decisions(self, **kwargs: Any) -> EgressDecisions:
        """Get egress decision audit log."""
        raw = self._dp_get(f"{self._sbx_path}/egress-decisions")
        return EgressDecisions._from_dict(raw if isinstance(raw, dict) else None) or EgressDecisions()
