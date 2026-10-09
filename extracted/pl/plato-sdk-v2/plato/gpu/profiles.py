"""What a pod boots: a Docker image and how the wrapper runs it.

A simulator's GPU form is a Docker image (its VM artifact is a Firecracker
rootfs, which no GPU cloud boots). The platform stores that image on the
artifact's metadata (``gpu_pod``, this model as JSON); the world hands it
here; the SDK wraps the image's own start command with ``profiles/wrapper.sh``,
which adds what every pod needs and no game knows about: the session
recording, the idle watchdog, the health wait. ``PROFILES`` are named presets
of the same model for callers without an artifact (the CLI).

The image's contract: its command serves MCP on ``mcp_port`` with an
unauthenticated ``/health``, draws on X display ``:0`` (what the recording
captures) and serves noVNC on ``desktop_port``, reads ``PLATO_MCP_TOKEN``,
``PLATO_MCP_ADMIN_TOKEN``, ``RESOLUTION`` and whatever ``options`` name from
its environment, and ships ``ffmpeg`` and ``curl``.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

SCRIPTS = Path(__file__).with_name("profiles")
WRAPPER = SCRIPTS / "wrapper.sh"


class UnknownProfile(ValueError):
    """No pod profile of that name, or an option it does not take."""


class PodImage(BaseModel):
    """A pod's image and shape. Stored on an artifact as ``gpu_pod``."""

    image: str = Field(
        min_length=1,
        description="The Docker image the provider pulls; a private ECR image pulls with a credential minted per pod",
    )
    command: list[str] = Field(min_length=1, description="The image's start command, run by the wrapper")
    gpu_type_ids: list[str] = Field(default=["NVIDIA GeForce RTX 4090"], min_length=1)
    container_disk_gb: int = Field(default=20, ge=5, le=500)
    mcp_port: int = Field(default=8765, ge=1, le=65535)
    desktop_port: int = Field(default=6080, ge=1, le=65535)
    # Environment the image expects; a caller's options override these.
    env: dict[str, str] = Field(default_factory=dict)
    # Env var name -> key in the bucket, presigned for the pod to GET at boot.
    assets: dict[str, str] = Field(default_factory=dict)
    # Environment names a caller may set beyond ``env``'s defaults.
    options: list[str] = Field(default_factory=list)

    def allowed(self, options: dict[str, str]) -> None:
        refused = sorted(set(options) - set(self.options) - set(self.env))
        if refused:
            raise UnknownProfile(f"{self.image} does not take options {', '.join(refused)}")


PROFILES: dict[str, PodImage] = {
    # Mindustry with the Plato MCP mod on an Xvfb desktop (pod/ in the
    # hub.plato.so/plato/mindustry repo); the GPU form of the `mindustry` artifact
    # and the test bed for the pod lane. The game itself needs no GPU.
    "mindustry-desktop": PodImage(
        image="360831508645.dkr.ecr.us-west-2.amazonaws.com/plato-sims/mindustry:160.5",
        command=["/usr/local/bin/entrypoint"],
        # Any cheap card: the 4090 alone is often out of stock.
        gpu_type_ids=[
            "NVIDIA GeForce RTX 4090",
            "NVIDIA GeForce RTX 3090",
            "NVIDIA RTX A5000",
            "NVIDIA RTX A4000",
            "NVIDIA RTX 4000 Ada Generation",
            "NVIDIA L4",
        ],
        env={"PLATO_MCP_MODE": "campaign", "PLATO_MCP_MAP": "caldera", "RESOLUTION": "1280x720"},
        options=["PLATO_MCP_MODE", "PLATO_MCP_MAP", "RESOLUTION"],
    ),
}


def profile_named(name: str) -> PodImage:
    profile = PROFILES.get(name)
    if profile is None:
        raise UnknownProfile(f"no pod profile named {name}; one of {', '.join(sorted(PROFILES))}")
    return profile


def wrapper_script() -> bytes:
    return WRAPPER.read_bytes()
