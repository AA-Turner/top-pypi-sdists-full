"""What a new sandbox may set besides its entrypoint."""

from collections.abc import Mapping, Sequence
from typing import TypedDict

from labqoat.sandbox.probe import Probe


class SandboxOptions(TypedDict, total=False):
    """Keyword arguments of ``SandboxClient.create``, every one optional; ``create`` documents each."""

    image: str | None
    cpu: float
    memory: int
    gpu: int
    env: Mapping[str, str] | None
    sandbox_id: str | None
    name: str | None
    tags: Mapping[str, str] | None
    timeout: float
    idle_timeout: float | None
    workdir: str | None
    readiness_probe: Probe | None
    volumes: Mapping[str, str] | None
    network: bool | Sequence[str]
    ports: Sequence[int]
    wait: float
