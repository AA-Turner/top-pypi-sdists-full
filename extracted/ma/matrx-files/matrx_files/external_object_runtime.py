"""Immutable injection for protected external-object operations.

No declaration retains the historical SDK behavior; hosts requiring admission
must declare it before starting consumers. This state is independent of configure().
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from dataclasses import dataclass, replace
from threading import Lock
from typing import TYPE_CHECKING, Literal, Protocol

if TYPE_CHECKING:
    from .external_objects import ExternalObjectAdoptionRequest
    from .retention import TemporaryFileRetentionPolicy


@dataclass(frozen=True)
class AdoptionDescriptor:
    owner_id: str
    organization_id: str | None
    storage_uri: str
    file_path: str
    file_name: str
    mime_type: str
    source_kind: str
    source_event_key: str
    retention_policy: str
    policy_sha256: str


def policy_fingerprint(policy: TemporaryFileRetentionPolicy) -> str:
    encoded = json.dumps(policy.model_dump(mode="json"), sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def adoption_descriptor(request: ExternalObjectAdoptionRequest, policy: TemporaryFileRetentionPolicy) -> AdoptionDescriptor:
    return AdoptionDescriptor(
        owner_id=request.owner_id, organization_id=request.organization_id,
        storage_uri=request.storage_uri, file_path=request.file_path, file_name=request.file_name,
        mime_type=request.mime_type, source_kind=request.source_kind, source_event_key=request.source_event_key,
        retention_policy=policy.name, policy_sha256=policy_fingerprint(policy),
    )


class ExternalObjectGuard(Protocol):
    async def admit_remote(self, engine: object, canonical_uri: str, *, operation: object | None, unit: str, file_id: str | None = None, descriptor: AdoptionDescriptor | None = None) -> None: ...
    def publication_scope(self, engine: object, canonical_uri: str, *, operation: object | None, unit: str, file_id: str | None = None, descriptor: AdoptionDescriptor | None = None) -> AbstractAsyncContextManager[None]: ...


@dataclass(frozen=True)
class _Runtime:
    mode: Literal["host_required", "standalone_trusted"]
    namespace_classifier: Callable[[str], bool]
    guard: ExternalObjectGuard | None


_runtime: _Runtime | None = None
_lock = Lock()


def _validate_guard(guard: ExternalObjectGuard) -> None:
    if not callable(getattr(guard, "admit_remote", None)) or not callable(getattr(guard, "publication_scope", None)):
        raise TypeError("external object guard requires admit_remote and publication_scope")


def declare_external_object_runtime(*, mode: Literal["host_required", "standalone_trusted"], namespace_classifier: Callable[[str], bool], guard: ExternalObjectGuard | None = None) -> None:
    if mode not in ("host_required", "standalone_trusted") or not callable(namespace_classifier):
        raise ValueError("valid mode and callable namespace classifier are required")
    if guard is not None:
        _validate_guard(guard)
    if mode == "standalone_trusted" and guard is not None:
        raise ValueError("standalone_trusted does not accept a host guard")
    global _runtime
    with _lock:
        if _runtime is None:
            _runtime = _Runtime(mode, namespace_classifier, guard)
        elif not (_runtime.mode == mode and _runtime.namespace_classifier is namespace_classifier and _runtime.guard is guard):
            raise RuntimeError("external object runtime is already declared")


def bind_external_object_guard(guard: ExternalObjectGuard) -> None:
    _validate_guard(guard)
    global _runtime
    with _lock:
        if _runtime is None or _runtime.mode != "host_required":
            raise RuntimeError("host-required runtime must be declared before binding")
        if _runtime.guard is None:
            _runtime = replace(_runtime, guard=guard)
        elif _runtime.guard is not guard:
            raise RuntimeError("external object guard is already bound")


def _guard_for(uri: str) -> ExternalObjectGuard | None:
    runtime = _runtime
    if runtime is None or runtime.mode == "standalone_trusted" or not runtime.namespace_classifier(uri):
        return None
    if runtime.guard is None:
        raise PermissionError("required external object guard is not bound")
    return runtime.guard


async def admit_remote(engine: object, uri: str, *, operation: object | None, unit: str, file_id: str | None = None, descriptor: AdoptionDescriptor | None = None) -> None:
    guard = _guard_for(uri)
    if guard is not None:
        kwargs = {"operation": operation, "unit": unit, "file_id": file_id}
        if descriptor is not None:
            kwargs["descriptor"] = descriptor
        await guard.admit_remote(engine, uri, **kwargs)


@asynccontextmanager
async def publication_scope(engine: object, uri: str, *, operation: object | None, unit: str, file_id: str | None = None, descriptor: AdoptionDescriptor | None = None):
    guard = _guard_for(uri)
    if guard is None:
        yield
    else:
        kwargs = {"operation": operation, "unit": unit, "file_id": file_id}
        if descriptor is not None:
            kwargs["descriptor"] = descriptor
        async with guard.publication_scope(engine, uri, **kwargs):
            yield
