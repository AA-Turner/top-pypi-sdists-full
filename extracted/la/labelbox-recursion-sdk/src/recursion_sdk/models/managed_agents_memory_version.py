from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_memory_version_author_kind import ManagedAgentsMemoryVersionAuthorKind
from ..models.managed_agents_memory_version_operation import ManagedAgentsMemoryVersionOperation
from ..models.managed_agents_memory_version_status import ManagedAgentsMemoryVersionStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsMemoryVersion")



@_attrs_define
class ManagedAgentsMemoryVersion:
    """ One immutable change to a memory. Versions belong to the store rather than the memory, so the audit trail survives
    the memory being deleted.

        Example:
            {'author_kind': 'session', 'author_principal': 'example', 'author_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'byte_size': 1, 'content': 'example', 'content_sha256': 'example',
                'created_at': '2026-02-18T09:30:00Z', 'evidence_session_ids': ['example'], 'memory_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'memory_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'operation': 'create', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path': 'example', 'rationale': 'example', 'redacted_at':
                '2026-02-18T09:30:00Z', 'redacted_by': 'example', 'reflection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'status': 'active', 'summary': 'example', 'superseded_by_memory_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            author_kind (ManagedAgentsMemoryVersionAuthorKind): Who wrote this version.
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when this version was written.
            memory_id (str): Memory this version describes. The memory may since have been deleted.
            memory_store_id (str): Store this version belongs to.
            memory_version_id (str): Server-assigned id of the version.
            operation (ManagedAgentsMemoryVersionOperation): What this version records.
            organization_id (str): Organization that owns this record.
            path (str): Path of the memory as it stood at this version.
            author_principal (str | Unset): Caller identity that wrote this version, when an API caller did.
            author_session_id (str | Unset): Session that wrote this version, when a session did.
            byte_size (int | Unset): Size of the content at this version in bytes.
            content (str | Unset): Content as it stood at this version. Empty once redacted, and omitted from listings.
            content_sha256 (str | Unset): SHA-256 of the content at this version.
            evidence_session_ids (list[str] | Unset): Sessions supporting this version, scoped to the same agent and
                organization.
            rationale (str | Unset): Why this memory was added, changed, merged, or retired.
            redacted_at (datetime.datetime | Unset): Set when the content was scrubbed for compliance. Author and timestamp
                are preserved.
            redacted_by (str | Unset): Caller that redacted this version.
            reflection_id (str | Unset): Learning run that produced this version.
            status (ManagedAgentsMemoryVersionStatus | Unset): Memory lifecycle state after this change.
            summary (str | Unset): Summary as it stood at this version.
            superseded_by_memory_id (str | Unset): Surviving memory when this version records a merge.
     """

    author_kind: ManagedAgentsMemoryVersionAuthorKind
    created_at: datetime.datetime
    memory_id: str
    memory_store_id: str
    memory_version_id: str
    operation: ManagedAgentsMemoryVersionOperation
    organization_id: str
    path: str
    author_principal: str | Unset = UNSET
    author_session_id: str | Unset = UNSET
    byte_size: int | Unset = UNSET
    content: str | Unset = UNSET
    content_sha256: str | Unset = UNSET
    evidence_session_ids: list[str] | Unset = UNSET
    rationale: str | Unset = UNSET
    redacted_at: datetime.datetime | Unset = UNSET
    redacted_by: str | Unset = UNSET
    reflection_id: str | Unset = UNSET
    status: ManagedAgentsMemoryVersionStatus | Unset = UNSET
    summary: str | Unset = UNSET
    superseded_by_memory_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        author_kind = self.author_kind.value

        created_at = self.created_at.isoformat()

        memory_id = self.memory_id

        memory_store_id = self.memory_store_id

        memory_version_id = self.memory_version_id

        operation = self.operation.value

        organization_id = self.organization_id

        path = self.path

        author_principal = self.author_principal

        author_session_id = self.author_session_id

        byte_size = self.byte_size

        content = self.content

        content_sha256 = self.content_sha256

        evidence_session_ids: list[str] | Unset = UNSET
        if not isinstance(self.evidence_session_ids, Unset):
            evidence_session_ids = self.evidence_session_ids



        rationale = self.rationale

        redacted_at: str | Unset = UNSET
        if not isinstance(self.redacted_at, Unset):
            redacted_at = self.redacted_at.isoformat()

        redacted_by = self.redacted_by

        reflection_id = self.reflection_id

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        summary = self.summary

        superseded_by_memory_id = self.superseded_by_memory_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "author_kind": author_kind,
            "created_at": created_at,
            "memory_id": memory_id,
            "memory_store_id": memory_store_id,
            "memory_version_id": memory_version_id,
            "operation": operation,
            "organization_id": organization_id,
            "path": path,
        })
        if author_principal is not UNSET:
            field_dict["author_principal"] = author_principal
        if author_session_id is not UNSET:
            field_dict["author_session_id"] = author_session_id
        if byte_size is not UNSET:
            field_dict["byte_size"] = byte_size
        if content is not UNSET:
            field_dict["content"] = content
        if content_sha256 is not UNSET:
            field_dict["content_sha256"] = content_sha256
        if evidence_session_ids is not UNSET:
            field_dict["evidence_session_ids"] = evidence_session_ids
        if rationale is not UNSET:
            field_dict["rationale"] = rationale
        if redacted_at is not UNSET:
            field_dict["redacted_at"] = redacted_at
        if redacted_by is not UNSET:
            field_dict["redacted_by"] = redacted_by
        if reflection_id is not UNSET:
            field_dict["reflection_id"] = reflection_id
        if status is not UNSET:
            field_dict["status"] = status
        if summary is not UNSET:
            field_dict["summary"] = summary
        if superseded_by_memory_id is not UNSET:
            field_dict["superseded_by_memory_id"] = superseded_by_memory_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        author_kind = ManagedAgentsMemoryVersionAuthorKind(d.pop("author_kind"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        memory_id = d.pop("memory_id")

        memory_store_id = d.pop("memory_store_id")

        memory_version_id = d.pop("memory_version_id")

        operation = ManagedAgentsMemoryVersionOperation(d.pop("operation"))




        organization_id = d.pop("organization_id")

        path = d.pop("path")

        author_principal = d.pop("author_principal", UNSET)

        author_session_id = d.pop("author_session_id", UNSET)

        byte_size = d.pop("byte_size", UNSET)

        content = d.pop("content", UNSET)

        content_sha256 = d.pop("content_sha256", UNSET)

        evidence_session_ids = cast(list[str], d.pop("evidence_session_ids", UNSET))


        rationale = d.pop("rationale", UNSET)

        _redacted_at = d.pop("redacted_at", UNSET)
        redacted_at: datetime.datetime | Unset
        if isinstance(_redacted_at,  Unset):
            redacted_at = UNSET
        else:
            redacted_at = datetime.datetime.fromisoformat(_redacted_at)




        redacted_by = d.pop("redacted_by", UNSET)

        reflection_id = d.pop("reflection_id", UNSET)

        _status = d.pop("status", UNSET)
        status: ManagedAgentsMemoryVersionStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = ManagedAgentsMemoryVersionStatus(_status)




        summary = d.pop("summary", UNSET)

        superseded_by_memory_id = d.pop("superseded_by_memory_id", UNSET)

        managed_agents_memory_version = cls(
            author_kind=author_kind,
            created_at=created_at,
            memory_id=memory_id,
            memory_store_id=memory_store_id,
            memory_version_id=memory_version_id,
            operation=operation,
            organization_id=organization_id,
            path=path,
            author_principal=author_principal,
            author_session_id=author_session_id,
            byte_size=byte_size,
            content=content,
            content_sha256=content_sha256,
            evidence_session_ids=evidence_session_ids,
            rationale=rationale,
            redacted_at=redacted_at,
            redacted_by=redacted_by,
            reflection_id=reflection_id,
            status=status,
            summary=summary,
            superseded_by_memory_id=superseded_by_memory_id,
        )


        managed_agents_memory_version.additional_properties = d
        return managed_agents_memory_version

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
