"""Typed context-first remote function declaration."""

from collections.abc import Awaitable, Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass, field
import inspect
from types import MethodType
from typing import TYPE_CHECKING, Concatenate, Generic, NoReturn, ParamSpec, TypeVar, cast

from labqoat._generated.compute_function import ComputeFunction
from labqoat.authoring.resources import Resources
from labqoat.compute.function_signature import FunctionSignature
from labqoat.compute.automatic_recovery import AutomaticRecovery
from labqoat.compute.class_signature import ClassSignature
from labqoat.compute.resume_declaration import ResumeDeclaration
from labqoat.compute.image import Image
from labqoat.compute.images.app_images import AppImages
from labqoat.compute.value_codec import ValueCodec
from labqoat.run_context import RunContext
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.schema_document import SchemaDocument
from labqoat.compute.workers import Workers
from labqoat.compute.batch_handler import BatchHandler
from labqoat.compute.volume import Volume
from labqoat.compute.volume_mounts import VolumeMounts
from labqoat.compute.sandboxes import Sandboxes
from labqoat.compute.secret import Secret
from labqoat.training.budgets.fit_allowance import FitAllowance
from labqoat.training.recovery.recovery_capability import RecoveryCapability
from labqoat.training.recovery.recovery_binding import RecoveryBinding

if TYPE_CHECKING:
    from labqoat.client import Client
    from labqoat.compute.function_calls import FunctionCalls

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


@dataclass(frozen=True)
class Function(Generic[P, R]):
    """Preserve authored parameters and return type while keeping host dispatch explicit."""

    local: Callable[Concatenate[RunContext, P], R | Awaitable[R]]
    app_name: str
    image: Image
    cpu: float
    memory: int
    timeout: int
    gpu: str | None = None
    class_type: type[object] | None = None
    retries: int = 0
    registry: AppImages = field(default_factory=AppImages, compare=False, repr=False)
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

    def __call__(self, *_args: object, **_kwargs: object) -> NoReturn:
        """Refuse a direct call with the ways a decorated function is called instead."""
        name = getattr(self.local, "__qualname__", "function")
        raise TypeError(
            f"{name} is a Labqoat function (@app.function), not a plain callable: launch it with "
            f"`lab run FILE.py::{name}`, start a child with `context.runs.submit({name}, ...)`, or call the "
            f"undecorated body as `{name}.local(context, ...)`. A helper placed between a decorator and its "
            "function takes that decorator; keep helpers above it."
        )

    def with_client(self, client: "Client") -> "FunctionCalls[P, R]":
        """Bind host dispatch to an explicitly configured credential-bearing client."""
        from labqoat.compute.function_calls import FunctionCalls

        return FunctionCalls(self, client.runs)

    def with_context(self, context: RunContext) -> "FunctionCalls[P, R]":
        """Bind child dispatch to this invocation's assignment-scoped authority."""
        from labqoat.compute.function_calls import FunctionCalls

        return FunctionCalls(self, context.runs)

    def capture(self) -> ComputeFunction:
        """Derive the transport interface and resource request directly from the authored function."""
        self.validate_publication()
        signature = FunctionSignature(self.local)
        return ComputeFunction(
            name=self.local.__name__,
            workflow_replay=1 if self.workflow_replay else None,
            reuse=1 if self.reuse else None,
            memory_snapshot=1 if self.memory_snapshot else None,
            automatic_recovery=None if self.automatic_recovery is None else self.automatic_recovery.capture(),
            module=self.local.__module__,
            context_parameter=signature.context_parameter,
            input_schema=self.input_schema(),
            output_schema=ValueCodec(signature.annotations["return"]).schema(),
            resources=self.resources(),
            timeout_seconds=self.timeout,
            fit_budget_ms=None if self.fit_allowance is None else self.fit_allowance.validate_isolation(self.workers),
            recovery=None if self.recovery is None else self.recovery.capture(self.workers, self.fit_allowance),
            resume=self.resume_declaration(signature),
            queue_timeout_seconds=self.patience(),
            location=self.location,
            retries=self.retries or None,
            class_name=None if self.class_type is None else self.class_type.__name__,
            initializer=None if self.class_type is None else ClassSignature(self.class_type).initializer(),
            snapshot_initializer=None
            if self.class_type is None
            else ClassSignature(self.class_type).snapshot_initializer() or None,
            workers=None if self.workers is None else self.workers.to_dict(),
            volumes=VolumeMounts.to_dict(self.volumes),
            secrets=[secret.name for secret in self.secrets] or None,
            sandboxes=None if self.sandboxes is None else self.sandboxes.to_dict(),
        )

    def capture_for(self, arguments: dict[str, JsonValue] | None) -> ComputeFunction:
        """Recompute argument-bound recovery from immutable inputs without changing authored intent."""
        declaration = self.capture()
        if self.recovery_binding is None:
            return declaration
        if arguments is None:
            raise ValueError("Argument-bound recovery requires retained invocation arguments")
        SchemaDocument.capture(self.input_schema()).validate(arguments)
        binding = self.recovery_binding(JsonDocument(deepcopy(arguments)))
        return binding.apply(declaration)

    def validate_publication(self) -> None:
        """Validate importable identity, bounded resources and callable lifecycle before capturing a declaration."""
        expected = (
            self.local.__name__ if self.class_type is None else f"{self.class_type.__name__}.{self.local.__name__}"
        )
        if self.local.__qualname__ != expected or self.local.__module__ == "__main__":
            raise ValueError("Compute functions must be importable top-level module declarations")
        if self.cpu <= 0 or self.memory <= 0 or not 1 <= self.timeout <= 604800:
            raise ValueError("Compute resources must be positive and timeout between one second and seven days")
        if type(self.retries) is not int or not 0 <= self.retries <= 10:
            raise ValueError("Compute retries must be an integer between zero and ten")
        self.validate_queue_timeout()
        if len(self.secrets) > 16:
            raise ValueError("A function may reference at most 16 secrets")
        if self.sandboxes is not None:
            self.sandboxes.validate_block(self.cpu, self.memory)
        self.validate_batch()

    def resume_declaration(self, signature: FunctionSignature) -> dict[str, JsonValue] | None:
        """Name the `Checkpoint | None` parameter a resume fills: the declared one, else the only one there is.

        A declared restore adapter (``with_recovery``) takes precedence; class methods cannot resume this way.
        """
        if self.class_type is not None and self.resume is not None:
            raise ValueError("with_resume applies to functions, not class methods")
        if self.recovery is not None or self.class_type is not None:
            return None
        parameters = signature.checkpoint_parameters()
        if self.resume is not None:
            return self.resume.capture(parameters)
        if self.resume_detection and len(parameters) == 1:
            return {"argument": parameters[0]}
        return None

    def patience(self) -> int:
        """How long the run may wait for capacity: as declared, else 24 h for GPU work and 1 h for CPU work."""
        if self.queue_timeout is not None:
            return self.queue_timeout
        return 86_400 if self.gpu is not None or self.gpu_count else 3600

    def validate_queue_timeout(self) -> None:
        """Bound capacity patience independently from the execution timeout."""
        if self.queue_timeout is None:
            return
        if type(self.queue_timeout) is not int or not 1 <= self.queue_timeout <= 2592000:
            raise ValueError("Compute queue_timeout must be an integer between one second and thirty days")

    def resources(self) -> dict[str, JsonValue]:
        """Capture the physical container budget shared by its admitted input slots."""
        self.validate_gpu_intent()
        if self.ephemeral_disk is not None and (type(self.ephemeral_disk) is not int or self.ephemeral_disk < 1):
            raise ValueError("ephemeral_disk must be a positive integer number of MiB")
        count = int(self.gpu is not None) if self.gpu_count is None else self.gpu_count
        return dict(
            Resources(
                cpu_millicores=int(self.cpu * 1000),
                memory_mb=self.memory,
                gpu_count=count,
                gpu_model=self.gpu,
                gpu_memory_mb=self.gpu_memory,
                ephemeral_storage_mb=self.ephemeral_disk,
                exact=self.exact_resources,
                spot=self.spot,
            ).to_dict()
        )

    def validate_gpu_intent(self) -> None:
        """Model-neutral GPU requests need both a device count and a per-device memory floor."""
        if self.gpu is not None:
            return
        if self.gpu_count not in (None, 0) and self.gpu_memory is None:
            raise ValueError("gpu_count requires gpu (a model such as 'h100' or 'any') or gpu_memory (per-device MiB)")
        if self.gpu_count in (None, 0) and self.gpu_memory is not None:
            raise ValueError("gpu_memory requires gpu (a model such as 'h100' or 'any') or a positive gpu_count")

    def validate_batch(self) -> None:
        """Reject an incompatible vectorized handler before source publication or remote admission."""
        if self.workers is not None and self.workers.batching is not None:
            owner = inspect.getmodule(self.local) if self.class_type is None else object.__new__(self.class_type)
            BatchHandler(getattr(owner, self.workers.batching.handler)).validate(self.local)

    def input_schema(self) -> dict[str, JsonValue]:
        """Retain class parameter and method argument authority in distinct explicit schema positions."""
        arguments = FunctionSignature(self.local).input_schema()
        if self.class_type is None:
            return arguments
        return {
            "type": "object",
            "properties": {"parameters": ClassSignature(self.class_type).schema(), "arguments": arguments},
            "required": ["parameters", "arguments"],
            "additionalProperties": False,
        }

    def encode(self, args: tuple[object, ...], kwargs: Mapping[str, object]) -> dict[str, JsonValue]:
        """Capture method bindings alongside call arguments before any remote side effect."""
        arguments = FunctionSignature(self.local).encode(args, kwargs)
        if self.class_type is not None:
            parameters = ClassSignature(self.class_type).encode(cast(MethodType, self.local).__self__)
            arguments = {"parameters": parameters, "arguments": arguments}
        SchemaDocument.capture(self.input_schema()).validate(arguments)
        return arguments

    def invoke(self, arguments: dict[str, JsonValue], context: RunContext) -> R | Awaitable[R]:
        """Initialize a fresh class under claimed worker authority, then execute the typed callable."""
        SchemaDocument.capture(self.input_schema()).validate(arguments)
        target: Callable[..., R | Awaitable[R]] = self.local
        if self.class_type is not None:
            signature = ClassSignature(self.class_type)
            instance = signature.create(JsonDocument.expect_dict(arguments["parameters"]))
            signature.initialize(instance, context)
            target = getattr(instance, self.local.__name__).local
            arguments = JsonDocument.expect_dict(arguments["arguments"])
        decoded = FunctionSignature(target).decode(arguments)
        return target(context, **decoded)
