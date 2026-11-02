"""Adapters between public SDK models and the generated OpenAPI client."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import runta as _public

from .openapi.models import (
    AllowlistEgressPolicy,
    AllowlistEgressPolicyMode,
    Checkpoint,
    CheckpointRuntimeRestoreRequest,
    ColdRestoreResources,
    DenylistEgressPolicy,
    DenylistEgressPolicyMode,
    ErrorEnvelope,
    FreshRuntimeCreateRequest,
    PatchRuntimeRequest,
    PublicIngressProtocol,
    PublicIngressSpec,
    Runtime,
    SuspendAndWakeupIdlePolicy,
    TimeoutPolicy,
)
from .openapi.models import (
    CreateRuntimeResourceRequests as OpenApiCreateRuntimeResourceRequests,
)
from .openapi.models import (
    CreateRuntimeResources as OpenApiCreateRuntimeResources,
)
from .openapi.models import (
    PatchRuntimeResources as OpenApiPatchRuntimeResources,
)
from .openapi.models import (
    RuntimeResourceLimits as OpenApiRuntimeResourceLimits,
)
from .openapi.types import UNSET, Response, Unset


def unwrap_response(response: Response[Any]) -> Any:
    status_code = int(response.status_code)
    parsed = response.parsed
    if isinstance(parsed, ErrorEnvelope):
        error = _api_error_from_envelope(parsed, status_code=status_code)
    elif status_code >= 400:
        message = response.content.decode(errors="replace").strip()
        error = _public.ApiError(
            message or f"HTTP request failed: {status_code}", status_code=status_code
        )
    else:
        return getattr(parsed, "data", parsed)
    if status_code == 429:
        # Private metadata: public exception signatures and fields stay unchanged.
        error._retry_after = next(
            (
                value
                for key, value in response.headers.items()
                if key.lower() == "retry-after"
            ),
            None,
        )
    raise error


def create_runtime_request(
    name: str | None,
    *,
    checkpoint_id: str | None,
    vcpus: int,
    memory_mib: int,
    memory_max_mib: int | None,
    resources: _public.CreateRuntimeResources | Mapping[str, Any] | None,
    ingress_specs: Sequence[Mapping[str, Any]] | None,
    egress_policy: _public.EgressPolicy | None,
    idle_suspend_after_secs: int | None,
    auto_shutdown_after_secs: int | None = None,
    auto_delete_after_secs: int | None = None,
    tcp_allowlist: Sequence[str] | None = None,
) -> FreshRuntimeCreateRequest | CheckpointRuntimeRestoreRequest:
    policy = egress_policy or _public.EgressPolicy()
    common = {
        "auto_shutdown_policy": timeout_policy_to_openapi(auto_shutdown_after_secs),
        "auto_delete_policy": timeout_policy_to_openapi(auto_delete_after_secs),
        "tcp_allowlist": tcp_allowlist_to_openapi(tcp_allowlist),
        "egress_policy": egress_policy_to_openapi(policy),
        "idle_policy": SuspendAndWakeupIdlePolicy.from_dict(
            {
                "mode": "suspend_and_wakeup",
                "suspend_after_secs": idle_suspend_after_secs,
            }
        )
        if idle_suspend_after_secs is not None
        else UNSET,
        "ingress_specs": [
            ingress_spec_to_openapi(item) for item in ingress_specs or []
        ],
        "name": name if name is not None else UNSET,
    }
    if checkpoint_id is not None:
        return CheckpointRuntimeRestoreRequest(
            checkpoint_id=checkpoint_id,
            resources=ColdRestoreResources.from_dict(
                resources.to_json()
                if isinstance(resources, _public.CreateRuntimeResources)
                else dict(resources)
            )
            if resources is not None
            else UNSET,
            **common,
        )
    return FreshRuntimeCreateRequest(
        resources=create_runtime_resources_to_openapi(
            resources,
            vcpus=vcpus,
            memory_mib=memory_mib,
            memory_max_mib=memory_max_mib,
        ),
        **common,
    )


def patch_runtime_request(
    *,
    resources: _public.PatchRuntimeResources | Mapping[str, Any] | None,
    egress_policy: _public.EgressPolicy | None,
    auto_shutdown_after_secs: int | None = None,
    auto_delete_after_secs: int | None = None,
    tcp_allowlist: Sequence[str] | None = None,
) -> PatchRuntimeRequest:
    return PatchRuntimeRequest(
        auto_shutdown_policy=timeout_policy_to_openapi(auto_shutdown_after_secs),
        auto_delete_policy=timeout_policy_to_openapi(auto_delete_after_secs),
        tcp_allowlist=tcp_allowlist_to_openapi(tcp_allowlist),
        egress_policy=egress_policy_to_openapi(egress_policy)
        if egress_policy is not None
        else UNSET,
        resources=patch_runtime_resources_to_openapi(resources),
    )


def timeout_policy_to_openapi(seconds: int | None) -> TimeoutPolicy | Unset:
    if seconds is None:
        return UNSET
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise ValueError("timeout seconds must be an integer")
    if not 0 <= seconds <= 2147483647:
        raise ValueError("timeout seconds must be between 0 and 2147483647")
    return TimeoutPolicy.from_dict(
        {"mode": "disabled"}
        if seconds == 0
        else {"mode": "enabled", "after_seconds": seconds}
    )


def tcp_allowlist_to_openapi(hosts: Sequence[str] | None) -> list[str] | Unset:
    if hosts is None:
        return UNSET
    if isinstance(hosts, (str, bytes)) or not isinstance(hosts, Sequence):
        raise ValueError("tcp_allowlist must be a sequence of strings")
    entries = list(hosts)
    if len(entries) > 16 or any(
        not isinstance(host, str) or not host.strip() for host in entries
    ):
        raise ValueError("tcp_allowlist must contain at most 16 nonempty strings")
    return entries


def create_runtime_resources_to_openapi(
    resources: _public.CreateRuntimeResources | Mapping[str, Any] | None,
    *,
    vcpus: int,
    memory_mib: int,
    memory_max_mib: int | None,
) -> OpenApiCreateRuntimeResources:
    if resources is None:
        limit_memory_mib = memory_mib if memory_max_mib is None else memory_max_mib
        if limit_memory_mib < memory_mib:
            raise ValueError(
                "memory_max_mib must be greater than or equal to memory_mib"
            )
        return OpenApiCreateRuntimeResources(
            limits=OpenApiRuntimeResourceLimits(memory_mib=limit_memory_mib),
            requests=OpenApiCreateRuntimeResourceRequests(
                memory_mib=memory_mib, vcpus=vcpus
            ),
        )
    data = (
        resources.to_json()
        if isinstance(resources, _public.CreateRuntimeResources)
        else dict(resources)
    )
    return OpenApiCreateRuntimeResources.from_dict(data)


def patch_runtime_resources_to_openapi(
    resources: _public.PatchRuntimeResources | Mapping[str, Any] | None,
) -> OpenApiPatchRuntimeResources | Unset:
    if resources is None:
        return UNSET
    data = (
        resources.to_json()
        if isinstance(resources, _public.PatchRuntimeResources)
        else dict(resources)
    )
    if not data:
        return UNSET
    return OpenApiPatchRuntimeResources.from_dict(data)


def egress_policy_to_openapi(
    policy: _public.EgressPolicy,
) -> AllowlistEgressPolicy | DenylistEgressPolicy:
    if policy.mode is _public.EgressMode.ALLOWLIST:
        return AllowlistEgressPolicy(
            mode=AllowlistEgressPolicyMode.ALLOWLIST,
            allowed_hosts=list(policy.allowed_hosts),
        )
    return DenylistEgressPolicy(
        mode=DenylistEgressPolicyMode.DENYLIST,
        denied_hosts=list(policy.denied_hosts),
    )


def ingress_spec_to_openapi(spec: Mapping[str, Any]) -> PublicIngressSpec:
    return PublicIngressSpec(
        protocol=PublicIngressProtocol(str(spec["protocol"])),
        runtime_port=int(spec["runtime_port"]),
    )


def runtime_info(runtime: Runtime) -> _public.RuntimeInfo:
    return _public.RuntimeInfo.from_json(runtime_to_public_json(runtime))


def checkpoint_info(checkpoint: Checkpoint) -> _public.CheckpointInfo:
    resources = checkpoint.resources
    requests = resources.requests
    limits = resources.limits
    return _public.CheckpointInfo.from_json(
        {
            "id": checkpoint.id,
            "display_name": checkpoint.display_name,
            "state": checkpoint.state.value,
            "kind": None if isinstance(checkpoint.kind, Unset) else checkpoint.kind,
            "safe_error_code": None
            if isinstance(checkpoint.safe_error_code, Unset)
            else checkpoint.safe_error_code,
            "resources": {
                "requests": requests.to_dict(),
                "limits": limits.to_dict(),
            },
        }
    )


def runtime_to_public_json(runtime: Runtime) -> dict[str, Any]:
    resources = runtime.resources
    requests = resources.requests
    limits = resources.limits
    optional = {}
    for name in ("auto_shutdown_policy", "auto_delete_policy"):
        value = getattr(runtime, name)
        if not isinstance(value, Unset):
            optional[name] = value.to_dict()
    for name in ("auto_shutdown_at", "auto_delete_at"):
        value = getattr(runtime, name)
        if not isinstance(value, Unset):
            optional[name] = value.isoformat()
    if not isinstance(runtime.tcp_allowlist, Unset):
        optional["tcp_allowlist"] = list(runtime.tcp_allowlist)
    return {
        **optional,
        "id": runtime.id,
        "display_name": runtime.display_name,
        "resources": {
            "requests": requests.to_dict(),
            "limits": limits.to_dict(),
        },
        "ingress_specs": [item.to_dict() for item in runtime.ingress_specs],
        "egress_policy": runtime.egress_policy.to_dict(),
        "status": runtime.status.value,
    }


def _api_error_from_envelope(
    envelope: ErrorEnvelope, *, status_code: int
) -> _public.ApiError:
    code = envelope.error.code.value
    return _public.ApiError(envelope.error.message, status_code=status_code, code=code)
