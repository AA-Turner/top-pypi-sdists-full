"""Capture only explicit typed constructor parameters and one context-first worker initializer."""

import inspect
from collections.abc import Callable, Mapping
from typing import cast, get_type_hints

from labqoat.compute.class_options import ClassOptions
from labqoat.compute.value_codec import ValueCodec
from labqoat.json_document import JsonValue
from labqoat.run_context import RunContext


class ClassSignature:
    """Reconstruct class instances from typed immutable bindings rather than serializing host process state."""

    def __init__(self, service: type[object]) -> None:
        """Require an importable direct class and an explicitly authored constructor."""
        if service.__qualname__ != service.__name__ or service.__module__ == "__main__":
            raise ValueError("Compute classes must be importable top-level declarations")
        if service.__bases__ != (object,) or "__init__" not in vars(service):
            raise TypeError("Compute classes require an explicit constructor and direct object inheritance")
        self.service = service
        self.parameters = inspect.signature(service).parameters
        self.annotations = get_type_hints(service.__init__)
        self.options = self._options(service)

    def schema(self) -> dict[str, JsonValue]:
        """Capture every named constructor parameter as a required immutable binding."""
        properties: dict[str, JsonValue] = {}
        for name, parameter in self.parameters.items():
            if parameter.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
                raise TypeError("Compute constructor parameters must have explicit names")
            properties[name] = ValueCodec(self.annotations[name]).schema()
        return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}

    def encode(self, instance: object) -> dict[str, JsonValue]:
        """Read only declared parameter attributes from the host-side binding object."""
        return {name: ValueCodec(self.annotations[name]).encode(getattr(instance, name)) for name in self.parameters}

    def create(self, parameters: Mapping[str, JsonValue]) -> object:
        """Construct a fresh worker-owned instance from already validated transported bindings."""
        constructor = cast(Callable[..., object], self.service)
        return constructor(
            **{name: ValueCodec(self.annotations[name]).decode(parameters[name]) for name in self.parameters}
        )

    def initialize(
        self, instance: object, context: RunContext, *, snapshotted: bool = True, started: bool = True
    ) -> None:
        """Run a fresh instance's initializers: the one a snapshot keeps first, then the one every worker runs."""
        for name, runs in ((self.snapshot_initializer(), snapshotted), (self.initializer(), started)):
            if name and runs:
                getattr(instance, name)(context)

    def initializer(self) -> str:
        """The optional initializer every worker runs, after a memory snapshot restores it too."""
        return self._marked(snap=False)

    def snapshot_initializer(self) -> str:
        """The optional initializer a memory snapshot keeps the result of, run before the snapshot is taken."""
        return self._marked(snap=True)

    def _marked(self, *, snap: bool) -> str:
        """Capture one optional context-first initializer of a kind without invoking user code."""
        names = [
            name
            for name, value in vars(self.service).items()
            if getattr(value, "__labqoat_enter__", False) and getattr(value, "__labqoat_snap__", False) is snap
        ]
        if len(names) > 1:
            raise TypeError("Compute classes support one worker initializer of each kind (snap=True and not)")
        if not names:
            return ""
        return self._validated(names[0])

    def _validated(self, name: str) -> str:
        """Require the initializer's exact synchronous ``(self, context: RunContext) -> None`` shape."""
        method = getattr(self.service, name)
        parameters = tuple(inspect.signature(method).parameters.values())
        hints = get_type_hints(method)
        if (
            len(parameters) != 2
            or hints.get(parameters[1].name) is not RunContext
            or hints.get("return") is not type(None)
        ):
            raise TypeError("Worker initializers must declare (self, context: RunContext) -> None")
        if not inspect.isfunction(method) or inspect.iscoroutinefunction(method):
            raise TypeError("Worker initializers must be synchronous instance methods")
        if any(parameter.kind is not inspect.Parameter.POSITIONAL_OR_KEYWORD for parameter in parameters):
            raise TypeError("Worker initializers require explicit positional self and context parameters")
        return name

    @staticmethod
    def _options(service: type[object]) -> ClassOptions:
        """Require an App-owned class declaration before treating a bound method as remote compute."""
        options = getattr(service, "__labqoat_class__", None)
        if not isinstance(options, ClassOptions):
            raise TypeError("Compute methods require an @app.cls declaration")
        return options
