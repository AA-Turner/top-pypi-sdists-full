"""Abstract base class for world runtimes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Annotated, Final, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag

from plato.v2.async_.environment import Environment

_UNSERIALIZABLE: Final = object()


class VMMetadata(BaseModel):
    """Metadata for Plato VM runtimes."""

    kind: Literal["vm"] = "vm"
    job_id: str = ""
    alias: str = ""
    hostname: str = ""
    """Resolved hostname (e.g. mesh IP) that may override RuntimeInfo.hostname."""


class AppleContainerMetadata(BaseModel):
    """Metadata for Apple container runtimes."""

    kind: Literal["apple_container"] = "apple_container"
    container_id: str = ""
    image: str = ""
    alias: str = ""


RuntimeMetadata = Annotated[
    Annotated[VMMetadata, Tag("vm")] | Annotated[AppleContainerMetadata, Tag("apple_container")],
    Discriminator("kind"),
]


class RuntimeInfo(BaseModel):
    """Information about a running runtime environment."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    runtime_id: str
    """Unique identifier for this runtime instance (VM job ID, container ID, etc.)."""

    hostname: str
    """SSH-reachable hostname or IP address."""

    ssh_user: str = "root"
    """SSH user for connections."""

    ssh_key_path: Path | None = None
    """Path to the SSH private key. None if the runtime handles auth internally."""

    serialized_session: object | None = None
    """Serialized Plato session for VM runtimes. When present, the world
    restores a live session for heartbeat, env access, and agent provisioning."""

    metadata: RuntimeMetadata = Field(default_factory=VMMetadata)
    """Runtime-specific metadata, discriminated by runtime kind."""

    env: Environment | None = Field(default=None, exclude=True)
    """Live Environment handle for VM runtimes. Not serializable — excluded
    from model serialization and runner payloads."""

    def to_runner_payload(self) -> dict[str, object]:
        """Return a JSON-safe payload for passing runtime info through runner config.

        ``serialized_session`` is preserved and validated strictly because VM-backed
        worlds require it for session restoration.
        """
        payload: dict[str, object] = {
            "runtime_id": self.runtime_id,
            "hostname": self.hostname,
            "ssh_user": self.ssh_user,
        }
        if self.ssh_key_path is not None:
            payload["ssh_key_path"] = str(self.ssh_key_path)
        if self.serialized_session is not None:
            payload["serialized_session"] = _json_safe_value(self.serialized_session, prune_unsupported=False)
        metadata = self.metadata.model_dump()
        if any(v for k, v in metadata.items() if k != "kind" and v):
            payload["metadata"] = metadata
        return payload


def _json_safe_mapping(value: Mapping[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, item in value.items():
        coerced = _json_safe_value(item, prune_unsupported=True)
        if coerced is _UNSERIALIZABLE:
            continue
        result[str(key)] = coerced
    return result


def _json_safe_value(value: object, *, prune_unsupported: bool) -> object:
    if value is None or isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, BaseModel):
        return _json_safe_value(value.model_dump(mode="json", exclude_none=True), prune_unsupported=prune_unsupported)
    if isinstance(value, Mapping):
        return _json_safe_mapping({str(key): item for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, str):
        result: list[object] = []
        for item in value:
            coerced = _json_safe_value(item, prune_unsupported=prune_unsupported)
            if coerced is _UNSERIALIZABLE:
                if prune_unsupported:
                    continue
                raise TypeError(f"Unsupported runtime payload value: {type(item).__name__}")
            result.append(coerced)
        return result
    if prune_unsupported:
        return _UNSERIALIZABLE
    raise TypeError(f"Unsupported runtime payload value: {type(value).__name__}")


class Runtime(ABC):
    """Abstract base for world execution runtimes.

    A runtime manages the lifecycle of the environment where a world runs.
    Implementations handle provisioning, command execution, and teardown for
    their specific backend (Plato VMs or Apple containers).

    Args:
        image: Container/VM image to use for the runtime environment.
    """

    def __init__(self, image: str) -> None:
        self.image = image

    @abstractmethod
    async def start(self, *, timeout: int = 300, alias: str | None = None) -> RuntimeInfo:
        """Provision and start the runtime environment.

        Args:
            timeout: Maximum seconds to wait for the environment to be ready.

        Returns:
            RuntimeInfo with connection details for the running environment.

        Raises:
            RuntimeError: If provisioning fails.
            TimeoutError: If the environment is not ready within the timeout.
        """

    @abstractmethod
    async def stop(self, runtime_id: str) -> None:
        """Stop and clean up the runtime environment.

        Args:
            runtime_id: The identifier from ``RuntimeInfo.runtime_id``.
        """

    @abstractmethod
    async def exec(
        self,
        runtime_id: str,
        command: str,
        *,
        timeout: int = 300,
        stream: bool = False,
    ) -> tuple[int, str, str]:
        """Execute a command on the runtime.

        Args:
            runtime_id: The identifier from ``RuntimeInfo.runtime_id``.
            command: Shell command to execute.
            timeout: Maximum seconds to wait for the command.
            stream: If True, stream stdout/stderr to the logger in real time.
                When streaming, the returned stdout/stderr may be empty.

        Returns:
            Tuple of (exit_code, stdout, stderr).
        """
