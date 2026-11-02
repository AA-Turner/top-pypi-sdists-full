"""What a sandbox the platform places may set besides its image and entrypoint."""

from collections.abc import Mapping, Sequence
from typing import TypedDict

from labqoat.compute.secret import Secret
from labqoat.sandbox.probe import Probe


class SandboxPlatformOptions(TypedDict, total=False):
    """Keyword arguments of ``Sandbox.create`` besides ``image``, every one optional; ``create`` documents each."""

    cpu: float
    memory: int
    gpu: str
    env: Mapping[str, str] | None
    secrets: Sequence[Secret]
    sandbox_id: str | None
    name: str | None
    tags: Mapping[str, str] | None
    timeout: float
    idle_timeout: float | None
    workdir: str | None
    readiness_probe: Probe | None
    network: bool | Sequence[str]
    wait: float
