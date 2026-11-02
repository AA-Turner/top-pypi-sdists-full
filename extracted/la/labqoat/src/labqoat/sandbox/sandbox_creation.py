"""A new sandbox as a sandbox host starts it."""

import math
import uuid
from collections.abc import Sequence
from typing import ClassVar

from labqoat.json_document import JsonValue
from labqoat.sandbox.sandbox_options import SandboxOptions
from labqoat.sandbox.sandbox_request import SandboxRequest


class SandboxCreation:
    """Translate ``create`` arguments into the host's sandbox document, in the host's units."""

    DEFAULT_TIMEOUT_SECONDS: ClassVar[float] = 300.0

    @staticmethod
    def request(entrypoint: Sequence[str], options: SandboxOptions) -> SandboxRequest:
        """Describe the sandbox by its identifier, limits and lifetime and only what differs from an idle one.

        Without ``sandbox_id`` a fresh identifier is generated.
        """
        if not all(isinstance(argument, str) for argument in entrypoint):
            raise TypeError(
                "create takes the entrypoint's arguments one by one: create('python3', '-m', 'http.server')"
            )
        identifier = options.get("sandbox_id") or f"sandbox-{uuid.uuid4().hex}"
        required: dict[str, JsonValue] = {
            "id": identifier,
            "cpu_millicores": round(options.get("cpu", 1) * 1000),
            "memory_mb": options.get("memory", 1024),
            "timeout_ms": SandboxCreation._milliseconds(
                options.get("timeout", SandboxCreation.DEFAULT_TIMEOUT_SECONDS)
            ),
        }
        optional = {**SandboxCreation._identity(options), **SandboxCreation._contents(entrypoint, options)}
        document = {**required, **{key: value for key, value in optional.items() if value is not None}}
        return SandboxRequest("POST", "/sandboxes", document=document)

    @staticmethod
    def _identity(options: SandboxOptions) -> dict[str, JsonValue]:
        """Name, tag and time the sandbox as the caller asked, leaving out what was not set."""
        tags, idle = options.get("tags"), options.get("idle_timeout")
        return {
            "image": options.get("image"),
            "gpu": options.get("gpu"),
            "name": options.get("name"),
            "tags": None if tags is None else dict(tags),
            "idle_timeout_ms": None if idle is None else SandboxCreation._milliseconds(idle),
        }

    @staticmethod
    def _contents(entrypoint: Sequence[str], options: SandboxOptions) -> dict[str, JsonValue]:
        """Say what runs in the sandbox, what it sees and what it reaches, leaving out what was not set."""
        env, volumes, probe = options.get("env"), options.get("volumes"), options.get("readiness_probe")
        return {
            "command": list(entrypoint) or None,
            "workdir": options.get("workdir"),
            "readiness": None if probe is None else probe.document(),
            "env": None if env is None else dict(env),
            "volumes": dict(volumes) if volumes else None,
            "network": SandboxCreation._network(options.get("network", False)),
            "ports": True if options.get("ports") else None,
        }

    @staticmethod
    def _network(network: bool | Sequence[str]) -> JsonValue:
        """Send a network only when the sandbox gets one; a bare host name would be read letter by letter."""
        if isinstance(network, str):
            raise TypeError("network is True, False or a sequence of host names; wrap one host as ['pypi.org']")
        if not network:
            return None
        return True if network is True else list(network)

    @staticmethod
    def _milliseconds(seconds: float) -> int:
        """Round seconds up to whole milliseconds, as the host counts them."""
        return math.ceil(seconds * 1000)
