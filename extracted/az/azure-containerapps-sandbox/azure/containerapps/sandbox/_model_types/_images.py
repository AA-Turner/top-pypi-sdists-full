"""Disk image models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DiskImageStatus:
    """Status of a disk image."""
    state: str = ""
    message: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> DiskImageStatus | None:
        if not d:
            return None
        return cls(state=d.get("state", ""), message=d.get("message"))


@dataclass(frozen=True)
class DiskImageSpec:
    """Container image specification for a disk image."""
    base: str = ""
    entrypoint: list[str] | None = None
    cmd: list[str] | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> DiskImageSpec | None:
        if not d:
            return None
        return cls(base=d.get("base", ""), entrypoint=d.get("entrypoint"), cmd=d.get("cmd"))


@dataclass(frozen=True)
class DiskImage:
    """A disk image resource."""
    id: str = ""
    labels: dict[str, str] = field(default_factory=dict)
    image: DiskImageSpec | None = None
    status: DiskImageStatus | None = None
    name: str | None = None
    dockerfile_content: str | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> DiskImage:
        return cls(
            id=d.get("id", ""),
            labels=d.get("labels", {}),
            image=DiskImageSpec._from_dict(d.get("image")),
            status=DiskImageStatus._from_dict(d.get("status")),
            name=d.get("name"),
            dockerfile_content=d.get("dockerfileContent"),
        )


@dataclass(frozen=True)
class PublicDiskImage:
    """A public disk image."""
    name: str = ""
    status: DiskImageStatus | None = None
    id: str = ""
    description: str | None = None
    tags: dict[str, str] = field(default_factory=dict)

    @classmethod
    def _from_dict(cls, d: dict) -> PublicDiskImage:
        return cls(
            name=d.get("name", ""),
            status=DiskImageStatus._from_dict(d.get("status")),
            id=d.get("id", ""),
            description=d.get("description"),
            tags=d.get("tags", {}),
        )


# ---- Input model ----


@dataclass
class RegistryCredentials:
    """Registry credentials for pulling private container images.

    Example::

        creds = RegistryCredentials(username="myuser", token="mytoken")
        group_client.create_disk_image("myacr.azurecr.io/myimage:latest",
                                       registry_credentials=creds)
    """

    username: str = ""
    token: str = ""

    def _to_dict(self) -> dict:
        return {"username": self.username, "token": self.token}
