"""One initialized callable with immutable binding checks and scalar or vectorized invocation."""

import asyncio
import importlib
import inspect
import json
from collections.abc import Callable
from dataclasses import replace
from functools import partial
from pathlib import Path

from labqoat.compute.batch_handler import BatchHandler
from labqoat.compute.class_signature import ClassSignature
from labqoat.compute.function_signature import FunctionSignature
from labqoat.compute.pool_worker.accepted_input import AcceptedInput
from labqoat.compute.value_codec import ValueCodec
from labqoat.compute.worker.compile_caches import CompileCaches
from labqoat.compute.worker.delivered_source import DeliveredSource
from labqoat.compute.worker.invocation import Invocation
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.run_context import RunContext
from labqoat.schemas.schema_document import SchemaDocument


class ReusableInvocation:
    """Serialize first initialization and reuse model state only inside an exact retained execution binding.

    A ``deferred`` invocation, preparing a memory snapshot, runs only the class's ``snap=True`` initializer; the one
    every worker runs waits until ``resume`` and the next initialization, whose context is the worker's own.
    """

    def __init__(self, scratch: Path, *, deferred: bool = False) -> None:
        """Own an initialization lock and lifetime-bound model scratch without loading code."""
        self.scratch = scratch
        self._lock = asyncio.Lock()
        self._identity: str | None = None
        self._scalar: Callable[..., object] | None = None
        self._batch: Callable[..., object] | None = None
        self._deferred = deferred
        self._start: Callable[[RunContext], None] | None = None
        self._logged: tuple[str, int] | None = None

    def resume(self) -> None:
        """Let the next initialization run the initializer every worker runs, after a snapshot or restore."""
        self._deferred = False

    def continue_logs(self, context: RunContext) -> None:
        """Number an initialization's logs after an earlier one's of the same attempt.

        A worker that saved a memory snapshot initializes twice in one attempt, and the platform keeps one log
        sequence per attempt; a restored worker is another attempt and starts its own.
        """
        logged = self._logged
        if context._telemetry is not None and logged is not None and logged[0] == context.attempt_id:
            context._telemetry.logs.resume_from(logged[1])

    def remember_logs(self, context: RunContext) -> None:
        """Remember how far an initialization's logs went in its attempt."""
        if context._telemetry is not None:
            self._logged = (context.attempt_id, context._telemetry.logs.sequence)

    async def execute(self, inputs: list[AcceptedInput]) -> list[dict[str, JsonValue]]:
        """Validate every input and the entire result cardinality before exposing any successful batch outputs."""
        for item in inputs:
            await self.prepare(item)
        scalar = self._scalar
        if scalar is None:
            raise ValueError("Reusable invocation requires at least one input")
        signature = FunctionSignature(scalar)
        arguments = [self._decode(item, signature) for item in inputs]
        values: object
        if self._batch is None:
            if len(inputs) != 1:
                raise ValueError("Unbatched execution accepts exactly one input")
            values = [await self._call(partial(scalar, inputs[0].context, **arguments[0]))]
        else:
            columns = {name: [row[name] for row in arguments] for name in signature.signature.parameters}
            values = await self._call(partial(self._batch, [item.context for item in inputs], **columns))
        if not isinstance(values, list) or len(values) != len(inputs):
            raise ValueError("Batch handler must return exactly one ordered result per input")
        return [self._encode(item, value, signature) for item, value in zip(inputs, values, strict=True)]

    async def prepare(self, item: AcceptedInput) -> None:
        """Reject constructor, code, budget or seed drift before sharing initialized mutable state."""
        if item.context.recovery is not None:
            raise ValueError("Restoration requires a fresh process, not a reusable invocation")
        identity = self._binding(item)
        async with self._lock:
            if self._identity is not None and self._identity != identity:
                raise ValueError("Reusable worker received a different immutable execution binding")
            if self._scalar is None:
                await asyncio.to_thread(self._initialize, item)
                self._identity = identity
            await self._started(item)

    async def _started(self, item: AcceptedInput) -> None:
        """Run the initializer every worker runs, once, unless a snapshot is still to be taken."""
        start = self._start
        if start is not None and not self._deferred:
            self._start = None
            await asyncio.to_thread(start, replace(item.context, scratch=self.scratch))

    def _initialize(self, item: AcceptedInput) -> None:
        """Load model state once under physical initialization or legacy first-input authority."""
        DeliveredSource.install(item.publication, item.context.assets, self.scratch)
        CompileCaches.ensure(self.scratch)
        target = Invocation.load(item.publication, item.arguments).target
        owner: object = importlib.import_module(item.publication.function.module)
        scalar: Callable[..., object] = target.local
        if target.class_type is not None:
            signature = ClassSignature(target.class_type)
            owner = signature.create(JsonDocument.expect_dict(item.arguments["parameters"]))
            signature.initialize(owner, replace(item.context, scratch=self.scratch), started=False)
            self._start = partial(signature.initialize, owner, snapshotted=False)
            scalar = getattr(owner, target.local.__name__).local
        batching = None if target.workers is None else target.workers.batching
        if batching is not None:
            batch = getattr(owner, batching.handler)
            BatchHandler(batch).validate(scalar)
            self._batch = batch
        self._scalar = scalar

    @staticmethod
    def _binding(item: AcceptedInput) -> str:
        """Include per-class parameters while allowing independent scalar inputs to share one model."""
        parameters = item.arguments.get("parameters") if item.publication.function.class_name else None
        value = {
            "publication": item.publication.to_dict(),
            "parameters": parameters,
            "seed": item.context.seed,
            "resources": item.context.resources.to_dict(),
        }
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def _decode(item: AcceptedInput, signature: FunctionSignature) -> dict[str, object]:
        """Check the complete captured input schema before decoding scalar method arguments."""
        SchemaDocument.capture(dict(item.publication.function.input_schema)).validate(item.arguments)
        values = item.arguments
        if item.publication.function.class_name is not None:
            values = dict(JsonDocument.expect_dict(values["arguments"]))
        return signature.decode(values)

    @staticmethod
    async def _call(operation: Callable[[], object]) -> object:
        """Execute sync code on a thread and await async code on the worker's shared event loop."""
        result: object
        if inspect.iscoroutinefunction(operation):
            result = operation()
        else:
            result = await asyncio.to_thread(operation)
        if inspect.isawaitable(result):
            result = await result
        return result

    @staticmethod
    def _encode(item: AcceptedInput, value: object, signature: FunctionSignature) -> dict[str, JsonValue]:
        """Bind each output to its own scalar return contract before any batch member is acknowledged."""
        data = ValueCodec(signature.annotations["return"]).encode(value)
        schema = SchemaDocument.capture(dict(item.publication.function.output_schema))
        schema.validate(data)
        return {"schema_digest": schema.digest, "data": data}
