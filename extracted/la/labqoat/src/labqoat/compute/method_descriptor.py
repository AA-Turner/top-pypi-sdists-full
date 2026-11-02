"""A descriptor exposing typed bound class methods through the existing compute Run contract."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from types import MethodType
from typing import Generic, ParamSpec, TypeVar, overload

from labqoat.compute.class_signature import ClassSignature
from labqoat.compute.function import Function

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


@dataclass(frozen=True)
class MethodDescriptor(Generic[P, R]):
    """Bind a method to explicit constructor parameters while retaining a fresh worker-owned instance per Run."""

    local: Callable[..., R | Awaitable[R]]

    @overload
    def __get__(self, instance: None, owner: type[object]) -> "MethodDescriptor[P, R]": ...

    @overload
    def __get__(self, instance: object, owner: type[object]) -> Function[P, R]: ...

    def __get__(self, instance: object | None, owner: type[object]) -> "MethodDescriptor[P, R] | Function[P, R]":
        """Capture no process state; publication serializes only the declared immutable parameters."""
        if instance is None:
            return self
        options = ClassSignature(owner).options
        return Function(
            MethodType(self.local, instance),
            options.app_name,
            options.image,
            options.cpu,
            options.memory,
            options.timeout,
            options.gpu,
            owner,
            retries=options.retries,
            registry=options.registry,
            workers=options.workers,
            volumes=options.volumes,
            secrets=options.secrets,
            sandboxes=options.sandboxes,
            gpu_memory=options.gpu_memory,
            gpu_count=options.gpu_count,
            ephemeral_disk=options.ephemeral_disk,
            exact_resources=options.exact_resources,
            spot=options.spot,
            queue_timeout=options.queue_timeout,
            location=options.location,
            fit_allowance=options.fit_allowance,
        )
