"""The VibeFS manifest a session passes: the volumes to mount and the directories to snapshot.

`mistral-vibefs` eagerly imports httpx, `mistral.vibefs_service`, filesystems and sandbox
probes, so session state carries its own copy of the shape instead of that distribution.

Nuage serves it through the vibefs sandbox daemon. `tests/integrations/vibefs/test_vibefs_manifest.py`
in nuage_v2 (where both packages are installed) checks every field reaches the daemon's manifest.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class MountConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mountpoint: str
    mode: str


class VolumeMountConfig(MountConfig):
    kind: Literal["volume"] = "volume"
    volume: str
    ref: str = "main"


class NydusVolumeMountConfig(MountConfig):
    """Still accepted so existing payloads parse; the daemon does not serve it and Nuage ignores it."""

    kind: Literal["nydus_volume"] = "nydus_volume"
    volume: str
    ref: str = "main"
    prewarm: bool = True


AnyMountConfig = Annotated[
    VolumeMountConfig | NydusVolumeMountConfig,
    Field(discriminator="kind"),
]


class SnapshotDirectoryConfig(BaseModel):
    """A sandbox directory kept as snapshot images on a volume.

    A new sandbox restores it before mounting anything, and a session snapshots it when it
    suspends. ``version`` pins the restore to one volume version instead of the newest image.
    """

    model_config = ConfigDict(extra="forbid")

    directory: str
    volume: str
    version: str | None = None


class FSManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mounts: list[AnyMountConfig]
    snapshots: list[SnapshotDirectoryConfig] = Field(default_factory=list)
