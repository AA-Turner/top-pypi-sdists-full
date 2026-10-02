from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsSessionSandbox")



@_attrs_define
class ManagedAgentsSessionSandbox:
    """ One continuous residency of a sandbox container in a session tree: when it was bound, when and why it stopped
    serving, which attachment it continues if the compute was revived from a snapshot, and the state of resource
    sampling for it.

        Example:
            {'attached_at': '2026-02-18T09:30:00Z', 'detach_reason': 'example', 'detached_at': '2026-02-18T09:30:00Z',
                'last_drained_at': '2026-02-18T09:30:00Z', 'owner_session_path': 'example', 'revived_from_sandbox_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'role': 'user', 'sample_interval_ms': 1, 'sample_rows': 1,
                'sample_watermark_at': '2026-02-18T09:30:00Z', 'sampling_scope': 'example', 'sampling_source': 'example',
                'sandbox_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_instance_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_provider': 'example'}

        Attributes:
            attached_at (datetime.datetime): RFC 3339 timestamp at which the container was bound to the tree.
            owner_session_path (str): Tree path of the session that attached the container. '/' for the root.
            role (str): What the container is to the session. Always primary today.
            sample_rows (int): Number of minute buckets stored for this attachment.
            sandbox_id (str): Tree-local identifier of this attachment (UUIDv7). A released-and-revived compute is a new
                attachment; follow revived_from_sandbox_id for its predecessor.
            sandbox_instance_id (str): Provider-assigned identity of the container: a compute id or container id. Historical
                self_hosted rows may contain a daemon id.
            sandbox_provider (str): Sandbox runtime that provided the container: runs or docker. Historical rows may report
                the retired self_hosted value.
            detach_reason (str | Unset): Why the attachment ended: released (compute given back, workspace kept), closed
                (session ended), replaced (a different container took over), or lost (the control plane found the binding gone).
            detached_at (datetime.datetime | Unset): RFC 3339 timestamp at which the container stopped serving the tree.
                Absent while attached.
            last_drained_at (datetime.datetime | Unset): RFC 3339 timestamp of the last successful drain from the producer.
            revived_from_sandbox_id (str | Unset): Attachment this one continues, when the container was restored from the
                previous attachment's snapshot.
            sample_interval_ms (int | Unset): Producer sampling cadence in milliseconds.
            sample_watermark_at (datetime.datetime | Unset): Start of the newest minute bucket with samples. Absent until
                the first drain lands data.
            sampling_scope (str | Unset): What the samples describe: cgroup for one container or host for the whole machine.
            sampling_source (str | Unset): Producer of this attachment's resource samples: rma_worker or
                agent_service_daemon. Absent until the first drain, and 'unsupported' when the sandbox cannot measure itself.
     """

    attached_at: datetime.datetime
    owner_session_path: str
    role: str
    sample_rows: int
    sandbox_id: str
    sandbox_instance_id: str
    sandbox_provider: str
    detach_reason: str | Unset = UNSET
    detached_at: datetime.datetime | Unset = UNSET
    last_drained_at: datetime.datetime | Unset = UNSET
    revived_from_sandbox_id: str | Unset = UNSET
    sample_interval_ms: int | Unset = UNSET
    sample_watermark_at: datetime.datetime | Unset = UNSET
    sampling_scope: str | Unset = UNSET
    sampling_source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        attached_at = self.attached_at.isoformat()

        owner_session_path = self.owner_session_path

        role = self.role

        sample_rows = self.sample_rows

        sandbox_id = self.sandbox_id

        sandbox_instance_id = self.sandbox_instance_id

        sandbox_provider = self.sandbox_provider

        detach_reason = self.detach_reason

        detached_at: str | Unset = UNSET
        if not isinstance(self.detached_at, Unset):
            detached_at = self.detached_at.isoformat()

        last_drained_at: str | Unset = UNSET
        if not isinstance(self.last_drained_at, Unset):
            last_drained_at = self.last_drained_at.isoformat()

        revived_from_sandbox_id = self.revived_from_sandbox_id

        sample_interval_ms = self.sample_interval_ms

        sample_watermark_at: str | Unset = UNSET
        if not isinstance(self.sample_watermark_at, Unset):
            sample_watermark_at = self.sample_watermark_at.isoformat()

        sampling_scope = self.sampling_scope

        sampling_source = self.sampling_source


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "attached_at": attached_at,
            "owner_session_path": owner_session_path,
            "role": role,
            "sample_rows": sample_rows,
            "sandbox_id": sandbox_id,
            "sandbox_instance_id": sandbox_instance_id,
            "sandbox_provider": sandbox_provider,
        })
        if detach_reason is not UNSET:
            field_dict["detach_reason"] = detach_reason
        if detached_at is not UNSET:
            field_dict["detached_at"] = detached_at
        if last_drained_at is not UNSET:
            field_dict["last_drained_at"] = last_drained_at
        if revived_from_sandbox_id is not UNSET:
            field_dict["revived_from_sandbox_id"] = revived_from_sandbox_id
        if sample_interval_ms is not UNSET:
            field_dict["sample_interval_ms"] = sample_interval_ms
        if sample_watermark_at is not UNSET:
            field_dict["sample_watermark_at"] = sample_watermark_at
        if sampling_scope is not UNSET:
            field_dict["sampling_scope"] = sampling_scope
        if sampling_source is not UNSET:
            field_dict["sampling_source"] = sampling_source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attached_at = datetime.datetime.fromisoformat(d.pop("attached_at"))




        owner_session_path = d.pop("owner_session_path")

        role = d.pop("role")

        sample_rows = d.pop("sample_rows")

        sandbox_id = d.pop("sandbox_id")

        sandbox_instance_id = d.pop("sandbox_instance_id")

        sandbox_provider = d.pop("sandbox_provider")

        detach_reason = d.pop("detach_reason", UNSET)

        _detached_at = d.pop("detached_at", UNSET)
        detached_at: datetime.datetime | Unset
        if isinstance(_detached_at,  Unset):
            detached_at = UNSET
        else:
            detached_at = datetime.datetime.fromisoformat(_detached_at)




        _last_drained_at = d.pop("last_drained_at", UNSET)
        last_drained_at: datetime.datetime | Unset
        if isinstance(_last_drained_at,  Unset):
            last_drained_at = UNSET
        else:
            last_drained_at = datetime.datetime.fromisoformat(_last_drained_at)




        revived_from_sandbox_id = d.pop("revived_from_sandbox_id", UNSET)

        sample_interval_ms = d.pop("sample_interval_ms", UNSET)

        _sample_watermark_at = d.pop("sample_watermark_at", UNSET)
        sample_watermark_at: datetime.datetime | Unset
        if isinstance(_sample_watermark_at,  Unset):
            sample_watermark_at = UNSET
        else:
            sample_watermark_at = datetime.datetime.fromisoformat(_sample_watermark_at)




        sampling_scope = d.pop("sampling_scope", UNSET)

        sampling_source = d.pop("sampling_source", UNSET)

        managed_agents_session_sandbox = cls(
            attached_at=attached_at,
            owner_session_path=owner_session_path,
            role=role,
            sample_rows=sample_rows,
            sandbox_id=sandbox_id,
            sandbox_instance_id=sandbox_instance_id,
            sandbox_provider=sandbox_provider,
            detach_reason=detach_reason,
            detached_at=detached_at,
            last_drained_at=last_drained_at,
            revived_from_sandbox_id=revived_from_sandbox_id,
            sample_interval_ms=sample_interval_ms,
            sample_watermark_at=sample_watermark_at,
            sampling_scope=sampling_scope,
            sampling_source=sampling_source,
        )


        managed_agents_session_sandbox.additional_properties = d
        return managed_agents_session_sandbox

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
