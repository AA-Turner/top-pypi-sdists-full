"""Async egress policy operations for sandbox-scoped client."""
from __future__ import annotations

import logging
from typing import Any, Literal

from azure.core.tracing.decorator_async import distributed_trace_async
from azure.containerapps.sandbox._helpers import _ERROR_MAP
from azure.containerapps.sandbox._egress_helpers import _add_host_rule, _add_rule, validate_egress_policy
from azure.containerapps.sandbox._response_helpers import _normalize_response, _normalize_response_lists

from azure.containerapps.sandbox._models import (
    EgressDecisions,
    EgressHeader,
    EgressPolicy,
    EgressRule,
    EgressRuleAction,
    EgressRuleMatch,
)

logger = logging.getLogger("azure.containerapps.sandbox")
_VALID_EGRESS_ACTIONS = ("Allow", "Deny")


class AsyncEgressOperationsMixin:
    """Async egress policy operations on a sandbox."""

    @distributed_trace_async
    async def set_egress_policy(self, policy: EgressPolicy, **kwargs: Any) -> EgressPolicy:
        """Set full egress policy.

        Auto-resumes a stopped/suspended sandbox first — the egress
        endpoint returns 409 ``SandboxNotRunning`` otherwise, matching
        the Rust CLI's ``ensure_running_with_client()`` pattern.
        """
        validate_egress_policy(policy)
        await self.ensure_running(**kwargs)
        result = await self._generated.sandboxes.set_egress_policy(
            self._sandbox_id,
            policy,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )
        return result

    @distributed_trace_async
    async def get_egress_policy(self, **kwargs: Any) -> EgressPolicy:
        """Get current egress policy."""
        policy = (await self.get(**kwargs)).egress_policy
        return _normalize_response_lists(policy if policy is not None else EgressPolicy(default_action="Allow"))

    @distributed_trace_async
    async def add_egress_host_rule(self, pattern: str, *,
                                   action: Literal["Allow", "Deny"] = "Allow",
                                   **kwargs: Any) -> EgressPolicy:
        """Add a host allow/deny rule (e.g., '*.github.com')."""
        if action not in _VALID_EGRESS_ACTIONS:
            raise ValueError(f"Invalid egress action {action!r}. Must be one of {_VALID_EGRESS_ACTIONS}")
        policy = await self.get_egress_policy(**kwargs)
        _add_host_rule(policy, pattern, action)
        return await self.set_egress_policy(policy, **kwargs)

    @distributed_trace_async
    async def add_egress_transform_rule(self, host: str, headers: list[EgressHeader], *,
                                        name: str | None = None,
                                        path: str | None = None,
                                        methods: list[str] | None = None,
                                        **kwargs: Any) -> EgressPolicy:
        """Add a Transform rule that modifies headers on outbound requests."""
        policy = await self.get_egress_policy(**kwargs)
        rule = EgressRule(
            name=name,
            match=EgressRuleMatch(host=host, path=path, methods=methods),
            action=EgressRuleAction(type="Transform", headers=list(headers)),
        )
        _add_rule(policy, rule)
        return await self.set_egress_policy(policy, **kwargs)

    @distributed_trace_async
    async def add_egress_rewrite_rule(self, host: str, *,
                                      rewrite_host: str | None = None,
                                      rewrite_path: str | None = None,
                                      rewrite_scheme: str | None = None,
                                      headers: list[EgressHeader] | None = None,
                                      name: str | None = None,
                                      **kwargs: Any) -> EgressPolicy:
        """Add a Rewrite rule that changes the destination of outbound requests."""
        policy = await self.get_egress_policy(**kwargs)
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
        _add_rule(policy, rule)
        return await self.set_egress_policy(policy, **kwargs)

    @distributed_trace_async
    async def get_egress_decisions(self, **kwargs: Any) -> EgressDecisions:
        """Get egress decision audit log."""
        return await self._generated.sandboxes.get_egress_decisions(
            self._sandbox_id,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )
