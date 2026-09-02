"""Volume models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class VolumeUsage:
    """Volume usage information."""
    used: str | None = None
    available: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> VolumeUsage | None:
        if not d:
            return None
        return cls(used=d.get("used"), available=d.get("available"))


@dataclass(frozen=True)
class Volume:
    """A volume resource."""
    name: str = ""
    type: str | None = None
    labels: dict[str, str] = field(default_factory=dict)
    size: str | None = None
    usage: VolumeUsage | None = None
    is_attached: bool | None = None
    # Present only for ``AzureBlobByo`` volumes.
    storage_container_resource_id: str | None = None
    auth: AzureBlobByoManagedIdentityAuth | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> Volume:
        return cls(
            name=d.get("volumeName", d.get("name", "")),
            type=d.get("type"),
            labels=d.get("labels", {}),
            size=d.get("size"),
            usage=VolumeUsage._from_dict(d.get("usage")),
            is_attached=d.get("isAttached"),
            storage_container_resource_id=d.get("storageContainerResourceId"),
            auth=AzureBlobByoManagedIdentityAuth._from_dict(d.get("auth")),
        )


# ---- Input models ----


@dataclass
class SandboxVolume:
    """Volume reference for sandbox creation.

    Example::

        vol = SandboxVolume(volume_name="my-vol", mountpoint="/data")
    """

    volume_name: str = ""
    mountpoint: str = ""
    read_only: bool | None = None

    def _to_dict(self) -> dict:
        d: dict = {
            "volumeName": self.volume_name,
            "mountpoint": self.mountpoint,
        }
        if self.read_only is not None:
            d["readOnly"] = self.read_only
        return d


@dataclass
class AddVolumeMountRequest:
    """Volume mount request for attaching a volume to a running sandbox.

    Example::

        mount = AddVolumeMountRequest(volume_name="my-volume", mountpoint="/data")
        sandbox.add_volume_mount(mount)
    """

    volume_name: str = ""
    mountpoint: str = ""

    def _to_dict(self) -> dict:
        return {
            "volumeMount": {
                "volumeName": self.volume_name,
                "mountpoint": self.mountpoint,
            }
        }


# ---- Bring-your-own (BYO) Azure Blob volume auth ----


@dataclass
class SandboxGroupIdentitySelector:
    """Selects a managed identity on the sandbox group for BYO volume auth.

    ``kind`` is ``"SystemAssigned"`` (no other fields) or ``"UserAssigned"``
    (carries ``resource_id``, the ARM id of the user-assigned identity).

    Example::

        SandboxGroupIdentitySelector(
            kind="UserAssigned",
            resource_id="/subscriptions/.../userAssignedIdentities/my-mi",
        )
    """

    kind: Literal["SystemAssigned", "UserAssigned"] = "SystemAssigned"
    resource_id: str | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> SandboxGroupIdentitySelector | None:
        if not d:
            return None
        return cls(
            kind=d.get("kind", "SystemAssigned"),
            resource_id=d.get("resourceId"),
        )

    def _to_dict(self) -> dict:
        d: dict = {"kind": self.kind}
        if self.resource_id is not None:
            d["resourceId"] = self.resource_id
        return d

    def validate(self) -> None:
        if self.kind not in ("SystemAssigned", "UserAssigned"):
            raise ValueError(
                "identity selector kind must be 'SystemAssigned' or 'UserAssigned' "
                f"(got {self.kind!r})"
            )
        if self.kind == "UserAssigned" and not self.resource_id:
            raise ValueError(
                "identity selector resource_id is required when kind is 'UserAssigned'"
            )
        if self.kind == "SystemAssigned" and self.resource_id:
            raise ValueError(
                "identity selector resource_id must not be set when kind is "
                "'SystemAssigned'"
            )


@dataclass
class AzureBlobByoManagedIdentityAuth:
    """Managed-identity auth for a bring-your-own (BYO) Azure Blob volume.

    ADC accesses the customer-owned container using a managed identity already
    on the sandbox group, selected by ``identity``. Serializes with ``kind``
    set to ``"ManagedIdentity"``.

    Example::

        auth = AzureBlobByoManagedIdentityAuth(
            identity=SandboxGroupIdentitySelector(kind="SystemAssigned"),
        )
    """

    identity: SandboxGroupIdentitySelector = field(
        default_factory=SandboxGroupIdentitySelector
    )

    @classmethod
    def _from_dict(cls, d: dict | None) -> AzureBlobByoManagedIdentityAuth | None:
        if not d:
            return None
        return cls(
            identity=SandboxGroupIdentitySelector._from_dict(d.get("identity"))
            or SandboxGroupIdentitySelector(),
        )

    def _to_dict(self) -> dict:
        return {"kind": "ManagedIdentity", "identity": self.identity._to_dict()}

    def validate(self) -> None:
        if self.identity is None:
            raise ValueError("BYO blob auth identity must not be None")
        self.identity.validate()
