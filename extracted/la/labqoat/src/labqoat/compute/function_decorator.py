"""Function decoration preserves parameters without executing authored code."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field, replace
from pathlib import Path
import inspect
from typing import Concatenate, ParamSpec, TypeVar, overload

from labqoat.compute.function import Function
from labqoat.compute.automatic_recovery import AutomaticRecovery
from labqoat.compute.image import Image
from labqoat.compute.resume_declaration import ResumeDeclaration
from labqoat.compute.images.app_images import AppImages
from labqoat.compute.images.declared_image import DeclaredImage
from labqoat.run_context import RunContext
from labqoat.compute.workers import Workers
from labqoat.compute.volume import Volume
from labqoat.compute.sandboxes import Sandboxes
from labqoat.compute.secret import Secret
from labqoat.training.budgets.fit_allowance import FitAllowance
from labqoat.training.recovery.recovery_capability import RecoveryCapability
from labqoat.training.recovery.recovery_binding import RecoveryBinding
from labqoat.json_document import JsonDocument

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class FunctionDecorator:
    """Bind one declaration to its App and captured execution options."""

    app_name: str
    image: Image
    cpu: float
    memory: int
    timeout: int
    gpu: str | None = None
    retries: int = 0
    registry: AppImages = field(default_factory=AppImages)
    workers: Workers | None = None
    volumes: tuple[tuple[str, Volume], ...] = ()
    secrets: tuple[Secret, ...] = ()
    sandboxes: Sandboxes | None = None
    gpu_memory: int | None = None
    gpu_count: int | None = None
    ephemeral_disk: int | None = None
    exact_resources: bool = False
    spot: bool = False
    queue_timeout: int | None = None
    location: str | None = None
    fit_allowance: FitAllowance | None = None
    recovery: RecoveryCapability | None = None
    workflow_replay: bool = False
    automatic_recovery: AutomaticRecovery | None = None
    recovery_binding: Callable[[JsonDocument], RecoveryBinding] | None = None
    resume: ResumeDeclaration | None = None
    resume_detection: bool = True
    reuse: bool = False
    memory_snapshot: bool = False

    def __post_init__(self) -> None:
        """A function's own snapshot saves one of its runs; pooled workers snapshot only as initialized classes."""
        if type(self.memory_snapshot) is not bool:
            raise ValueError("memory_snapshot must be a boolean")
        if self.workers is not None and (self.workers.memory_snapshot or self.memory_snapshot):
            raise ValueError(
                "A function with workers= cannot keep a memory snapshot; declare memory_snapshot=True on "
                "@app.function without workers=, or use an @app.cls class with workers=Workers(memory_snapshot=True)"
            )

    def with_reuse(self) -> "FunctionDecorator":
        """Answer a run identical to an earlier successful one from that run's result instead of running it again.

        Identical means the same source, image, arguments and seed in the same project. Use it for functions whose
        result depends only on those, such as data preparation or packing.
        """
        return replace(self, reuse=True)

    def with_resume(self, argument: str | None, *, key_prefix: str | None = None) -> "FunctionDecorator":
        """Name the `Checkpoint | None` parameter this function restores from when its run resumes.

        A function with exactly one such parameter needs no declaration. Use this when it has several, to pick
        from checkpoints whose key starts with ``key_prefix`` (``"latest-"``), or pass ``None`` to never resume.
        """
        if argument is None:
            return replace(self, resume=None, resume_detection=False)
        return replace(self, resume=ResumeDeclaration(argument, key_prefix), resume_detection=True)

    def with_recovery_binding(self, resolver: Callable[[JsonDocument], RecoveryBinding]) -> "FunctionDecorator":
        """Bind concrete recovery requirements using a deterministic retained argument resolver."""
        return replace(self, recovery_binding=resolver)

    def with_automatic_recovery(self, policy: AutomaticRecovery) -> "FunctionDecorator":
        """Retain an explicit automatic policy while preserving the authored retries cap."""
        policy.validate()
        return replace(self, automatic_recovery=policy)

    def with_workflow_replay(self) -> "FunctionDecorator":
        """Declare orchestration with retained decisions and stable child/effect identities."""
        return replace(self, workflow_replay=True)

    def with_recovery(self, capability: RecoveryCapability) -> "FunctionDecorator":
        """Declare the explicit restore adapter implemented by the retained workload entrypoint."""
        return replace(self, recovery=capability)

    def with_fit_budget(self, milliseconds: int) -> "FunctionDecorator":
        """Bind a cumulative allowance before decoration without altering authored arguments."""
        allowance = FitAllowance(milliseconds)
        allowance.validate_isolation(self.workers)
        return replace(self, fit_allowance=allowance)

    @overload
    def __call__(self, function: Callable[Concatenate[RunContext, P], Awaitable[R]]) -> Function[P, R]: ...

    @overload
    def __call__(self, function: Callable[Concatenate[RunContext, P], R]) -> Function[P, R]: ...

    def __call__(self, function: Callable[Concatenate[RunContext, P], object]) -> Function[P, object]:
        """Register a typed declaration without evaluating annotations or touching local files."""
        self.registry.register(
            DeclaredImage(
                function.__module__, function.__qualname__, Path(inspect.getfile(inspect.unwrap(function))), self.image
            )
        )
        return Function(
            function,
            self.app_name,
            self.image,
            self.cpu,
            self.memory,
            self.timeout,
            self.gpu,
            retries=self.retries,
            registry=self.registry,
            workers=self.workers,
            volumes=self.volumes,
            secrets=self.secrets,
            sandboxes=self.sandboxes,
            gpu_memory=self.gpu_memory,
            gpu_count=self.gpu_count,
            ephemeral_disk=self.ephemeral_disk,
            exact_resources=self.exact_resources,
            spot=self.spot,
            queue_timeout=self.queue_timeout,
            location=self.location,
            fit_allowance=self.fit_allowance,
            recovery=self.recovery,
            workflow_replay=self.workflow_replay,
            automatic_recovery=self.automatic_recovery,
            recovery_binding=self.recovery_binding,
            resume=self.resume,
            resume_detection=self.resume_detection,
            reuse=self.reuse,
            memory_snapshot=self.memory_snapshot,
        )
