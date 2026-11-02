"""Functions that start an HTTP server the world calls once they are deployed, like Modal's ``web_server``."""

import inspect
import re
from collections.abc import Callable
from dataclasses import dataclass, replace
from functools import wraps
from threading import Event
from typing import ClassVar
from weakref import WeakKeyDictionary, WeakSet

from labqoat.json_document import JsonValue
from labqoat.run_context import RunContext
from labqoat.service.service_target import ServiceTarget


@dataclass(frozen=True, kw_only=True)
class WebServer:
    """Where a deployed function's server listens, who may call it and how many replicas serve it.

    Calls in flight need one replica for every ``target_inputs`` of them, and ``buffer_containers`` spare ones
    while any is in flight. An endpoint keeps ``min_containers`` replicas, never has more than
    ``max_containers``, and stops replicas it no longer needs after ``scaledown_window`` seconds, down to none.
    """

    NAME: ClassVar[re.Pattern[str]] = re.compile(r"[a-z0-9][a-z0-9-]{0,45}")
    SERVICE: ClassVar[str] = "labqoat-endpoint-"
    declared: ClassVar[WeakKeyDictionary[Callable[..., object], "WebServer"]] = WeakKeyDictionary()
    bodies: ClassVar[WeakKeyDictionary[Callable[..., object], Callable[[RunContext], object]]] = WeakKeyDictionary()
    started: ClassVar[WeakSet[Callable[..., object]]] = WeakSet()

    port: int
    startup_timeout: float = 600.0
    label: str | None = None
    public: bool = False
    min_containers: int = 0
    max_containers: int = 1
    buffer_containers: int = 0
    target_inputs: int = 1
    scaledown_window: int = 60

    def __post_init__(self) -> None:
        """Refuse settings the platform would refuse before anything is published."""
        if type(self.port) is not int or not 1 <= self.port <= 65535:
            raise ValueError("web_server port must be an integer between 1 and 65535")
        if self.startup_timeout <= 0:
            raise ValueError("web_server startup_timeout must be positive")
        if self.label is not None and self.NAME.fullmatch(self.label) is None:
            raise ValueError("An endpoint label has 1 to 46 lowercase letters, digits or hyphens and starts with one")
        self._validate_scaling()

    def _validate_scaling(self) -> None:
        """Bound replica counts, calls per replica and the scaledown window as the platform does."""
        counts = (self.min_containers, self.max_containers, self.buffer_containers, self.target_inputs)
        if any(type(value) is not int for value in (*counts, self.scaledown_window)):
            raise ValueError("web_server scaling values must be integers")
        if not 0 <= self.min_containers <= self.max_containers <= 100 or self.max_containers < 1:
            raise ValueError("web_server needs 0 <= min_containers <= max_containers <= 100 and max_containers >= 1")
        if not 0 <= self.buffer_containers <= self.max_containers or not 1 <= self.target_inputs <= 10_000:
            raise ValueError("web_server buffer_containers exceeds max_containers or target_inputs is out of 1..10000")
        if not 0 <= self.scaledown_window <= 86_400:
            raise ValueError("web_server scaledown_window must be between 0 and 86400 seconds")

    @property
    def name(self) -> str:
        """The endpoint's name, which its URL ends with."""
        assert self.label is not None
        return self.label

    def settings(self) -> dict[str, JsonValue]:
        """Who may call the endpoint and how it scales, as a deployment states them."""
        return {
            "public": self.public,
            "min_containers": self.min_containers,
            "max_containers": self.max_containers,
            "buffer_containers": self.buffer_containers,
            "target_inputs": self.target_inputs,
            "scaledown_window": self.scaledown_window,
        }

    @classmethod
    def of(cls, function: Callable[..., object]) -> "WebServer":
        """The web server a function was declared as, or a refusal for an ordinary function."""
        server = cls.declared.get(function)
        if server is None:
            raise ValueError(f"{function.__name__} is not a web server; decorate it with @web_server(port)")
        return server

    def wrap(self, function: Callable[[RunContext], object]) -> Callable[[RunContext], None]:
        """Run the function to start the server, then serve its port until the platform stops this replica."""
        if not inspect.isfunction(function) or inspect.iscoroutinefunction(function):
            raise TypeError("@web_server decorates a plain function; put it under @app.function")
        if len(inspect.signature(function).parameters) != 1:
            raise TypeError("A web server function takes only its RunContext and starts its server")
        named = replace(self, label=self.label or function.__name__.replace("_", "-").lower())

        @wraps(function)
        def serving(context: RunContext) -> None:
            if serving not in self.started:
                function(context)
            with context.serve(self.SERVICE + named.name, port=self.port, startup_timeout=self.startup_timeout):
                named.serve_until_stopped()

        self.declared[serving] = named
        self.bodies[serving] = function
        return serving

    @classmethod
    def start(cls, serving: Callable[..., object], context: RunContext) -> None:
        """Start a web server function's server and wait until it listens, ahead of a memory snapshot.

        The function body runs now, under ``context``, instead of when the replica serves; serving skips it then.
        An ordinary function has no server to start.
        """
        server = cls.declared.get(serving)
        if server is None:
            return
        cls.bodies[serving](context)
        ServiceTarget(port=server.port).wait(server.startup_timeout, f"web server {server.name}")
        cls.started.add(serving)

    def serve_until_stopped(self) -> None:
        """Keep the replica serving; the platform cancels its run once the endpoint no longer needs it."""
        Event().wait()


def web_server(  # noqa: PLR0913 -- Mirrors the platform's endpoint settings one keyword each.
    port: int,
    *,
    startup_timeout: float = 600.0,
    label: str | None = None,
    public: bool = False,
    min_containers: int = 0,
    max_containers: int = 1,
    buffer_containers: int = 0,
    target_inputs: int = 1,
    scaledown_window: int = 60,
) -> Callable[[Callable[[RunContext], object]], Callable[[RunContext], None]]:
    """Serve the HTTP server a function starts on ``port`` to the world once it is deployed.

    Put it under ``@app.function``. The function starts its server, for example ``vllm serve`` in a
    subprocess, and returns; each replica waits up to ``startup_timeout`` seconds for the port to listen and then
    serves it. ``labqoat deploy app.py`` publishes it at ``https://HOST/e/<project>/<label>/``, where ``label``
    defaults to the function's name with hyphens. Callers send ``Authorization: Bearer <token>`` from
    ``labqoat endpoint token create`` unless the endpoint is ``public``.
    """
    return WebServer(
        port=port,
        startup_timeout=startup_timeout,
        label=label,
        public=public,
        min_containers=min_containers,
        max_containers=max_containers,
        buffer_containers=buffer_containers,
        target_inputs=target_inputs,
        scaledown_window=scaledown_window,
    ).wrap
