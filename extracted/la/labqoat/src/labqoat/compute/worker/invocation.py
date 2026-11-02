"""Runtime binding of a retained callable declaration to its authored Python implementation."""

import asyncio
import importlib
import inspect
import time
from contextlib import nullcontext
from dataclasses import dataclass

from labqoat._generated.compute_publication import ComputePublication
from labqoat.compute.function import Function
from labqoat.compute.function_signature import FunctionSignature
from labqoat.compute.value_codec import ValueCodec
from labqoat.json_document import JsonValue
from labqoat.run_context import RunContext
from labqoat.schemas.schema_document import SchemaDocument


@dataclass(frozen=True)
class Invocation:
    """Validate the installed function against its immutable interface before entering authored code."""

    publication: ComputePublication
    target: Function[..., object]

    @classmethod
    def load(cls, publication: ComputePublication, arguments: dict[str, JsonValue] | None = None) -> "Invocation":
        """Import and check the image's declaration while the assignment is still starting."""
        declared = publication.function
        module = importlib.import_module(declared.module)
        owner = module if declared.class_name is None else object.__new__(getattr(module, declared.class_name))
        target = getattr(owner, declared.name)
        differences = cls._differences(target, publication, arguments)
        if differences:
            location = getattr(module, "__file__", declared.module)
            raise ValueError(
                f"Installed callable {declared.module}.{declared.name} ({location}) does not match its captured "
                f"publication; differing fields: {', '.join(differences)}. The decorator's arguments were computed "
                "differently on the worker than at launch: compute them from literals, not from environment "
                "variables, files or other state read at import, then launch again."
            )
        if publication.runtime_version != "1":
            raise ValueError("Unsupported compute runtime version")
        return cls(publication, target)

    @staticmethod
    def _differences(
        target: object, publication: ComputePublication, arguments: dict[str, JsonValue] | None
    ) -> list[str]:
        """Name declaration fields that changed, never their values, so diagnosis cannot leak arguments."""
        if not isinstance(target, Function):
            return [f"type ({type(target).__name__} is not a Labqoat function)"]
        installed = target.capture_for(arguments).to_dict()
        declared = publication.function.to_dict()
        differences = sorted(
            key for key in installed.keys() | declared.keys() if installed.get(key) != declared.get(key)
        )
        if target.app_name != publication.app_name:
            differences.append("app_name")
        return differences

    def execute(self, arguments: dict[str, JsonValue], context: RunContext) -> dict[str, JsonValue]:
        """Inject only assignment identity, decode arguments, and validate a schema-bound result."""
        return asyncio.run(self._execute(arguments, context))

    async def _execute(self, arguments: dict[str, JsonValue], context: RunContext) -> dict[str, JsonValue]:
        """Own an event loop for authored tasks and resolve their result before encoding or acknowledging output."""
        session = nullcontext() if context._runs is None else context.runs.session()
        async with session:
            return await self._invoke(arguments, context)

    @staticmethod
    def _returned(context: RunContext, seconds: float) -> None:
        """Mark the end of authored code in long runs, so what follows reads as delivery rather than work."""
        if context._telemetry is not None and seconds >= 10:
            minutes, rest = divmod(int(seconds), 60)
            context.milestone(f"function returned after {minutes}m{rest:02d}s; delivering its result")

    def _call(self, arguments: dict[str, JsonValue], context: RunContext) -> object:
        """Call authored code as a plain program would see it, with no event loop running.

        A synchronous function owns this thread until it returns, so the worker's loop runs nothing meanwhile either
        way; hiding it lets the function start its own with ``asyncio.run``. A coroutine function only builds its
        coroutine here and is awaited on the worker's loop.
        """
        loop = asyncio.get_running_loop()
        asyncio.events._set_running_loop(None)
        try:
            return self.target.invoke(arguments, context)
        finally:
            asyncio.events._set_running_loop(loop)

    async def _invoke(self, arguments: dict[str, JsonValue], context: RunContext) -> dict[str, JsonValue]:
        """Execute and validate while the caller owns its asynchronous transport lifetime."""
        signature = FunctionSignature(self.target.local)
        started = time.monotonic()
        try:
            value = self._call(arguments, context)
            if inspect.isawaitable(value):
                value = await value
        finally:
            await asyncio.to_thread(context.settle)
        self._returned(context, time.monotonic() - started)
        context.require_restored()
        schema = SchemaDocument.capture(dict(self.publication.function.output_schema))
        try:
            data = ValueCodec(signature.annotations["return"]).encode(value)
            schema.validate(data)
        except (TypeError, ValueError) as error:
            declared = self.publication.function
            raise TypeError(
                f"{declared.module}.{declared.name} returned a value that does not match its declared "
                f"result type: {error}"
            ) from error
        return {"schema_digest": schema.digest, "data": data}
