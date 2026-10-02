from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_file_source import ManagedAgentsFileSource
from ..models.managed_agents_file_type import ManagedAgentsFileType
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_file_metadata import ManagedAgentsFileMetadata





T = TypeVar("T", bound="ManagedAgentsFile")



@_attrs_define
class ManagedAgentsFile:
    """ A file object: bytes uploaded once and attachable to any number of sessions as a resource, or bytes a session
    produced. Attaching a file mounts it read-only into the session's sandbox at a path the session is told about.

        Example:
            {'byte_size': 1, 'created_at': '2026-02-18T09:30:00Z', 'downloadable': True, 'expires_at':
                '2026-02-18T09:30:00Z', 'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'filename': 'example', 'media_type':
                'example', 'metadata': {'key': 'example'}, 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'scope_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sha256': 'example', 'source': 'upload', 'type':
                'file'}

        Attributes:
            byte_size (int): Size of the file in bytes.
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the upload.
            downloadable (bool): Whether GET /v1/files/{file_id}/content serves the bytes. True for every live file, upload
                or session output; expiry, not source, is what closes the content route. Kept so a client written when uploads
                were not served keeps a field to read.
            file_id (str): Server-assigned id, used to attach the file to a session as a resource.
            filename (str): The name the file was uploaded under, without any directory. This is the name it is mounted
                under in a sandbox unless a resource says otherwise.
            media_type (str): The upload's declared Content-Type. When the part declared none, or declared
                application/octet-stream, the type is detected from the filename's extension, through a fixed table rather than
                the host's, and then from the bytes, falling back to application/octet-stream when neither says anything.
                Informational: the platform does not transcode or validate against it.
            organization_id (str): Organization that owns the file. Server-assigned from the caller's credentials.
            sha256 (str): SHA-256 of the file's contents. Two uploads of identical bytes share one stored object.
            source (ManagedAgentsFileSource): How the file came to exist: upload for a caller upload, session_output for a
                file the platform captured from a finished session.
            type_ (ManagedAgentsFileType): Always file.
            expires_at (datetime.datetime | Unset): When the file stops being attachable and its content stops being served.
                Its metadata stays readable and listed, with this in the past, for a grace before the file is reclaimed. Absent
                means it does not expire.
            metadata (ManagedAgentsFileMetadata | Unset): Caller-owned key/value data stored with the file and returned
                unchanged.
            scope_session_id (str | Unset): For a session output, the session that produced it. Absent on an upload, which
                belongs to the organization rather than to any one session.
     """

    byte_size: int
    created_at: datetime.datetime
    downloadable: bool
    file_id: str
    filename: str
    media_type: str
    organization_id: str
    sha256: str
    source: ManagedAgentsFileSource
    type_: ManagedAgentsFileType
    expires_at: datetime.datetime | Unset = UNSET
    metadata: ManagedAgentsFileMetadata | Unset = UNSET
    scope_session_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_file_metadata import ManagedAgentsFileMetadata # noqa: PLC0415
        byte_size = self.byte_size

        created_at = self.created_at.isoformat()

        downloadable = self.downloadable

        file_id = self.file_id

        filename = self.filename

        media_type = self.media_type

        organization_id = self.organization_id

        sha256 = self.sha256

        source = self.source.value

        type_ = self.type_.value

        expires_at: str | Unset = UNSET
        if not isinstance(self.expires_at, Unset):
            expires_at = self.expires_at.isoformat()

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        scope_session_id = self.scope_session_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "byte_size": byte_size,
            "created_at": created_at,
            "downloadable": downloadable,
            "file_id": file_id,
            "filename": filename,
            "media_type": media_type,
            "organization_id": organization_id,
            "sha256": sha256,
            "source": source,
            "type": type_,
        })
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if scope_session_id is not UNSET:
            field_dict["scope_session_id"] = scope_session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_file_metadata import ManagedAgentsFileMetadata # noqa: PLC0415
        d = dict(src_dict)
        byte_size = d.pop("byte_size")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        downloadable = d.pop("downloadable")

        file_id = d.pop("file_id")

        filename = d.pop("filename")

        media_type = d.pop("media_type")

        organization_id = d.pop("organization_id")

        sha256 = d.pop("sha256")

        source = ManagedAgentsFileSource(d.pop("source"))




        type_ = ManagedAgentsFileType(d.pop("type"))




        _expires_at = d.pop("expires_at", UNSET)
        expires_at: datetime.datetime | Unset
        if isinstance(_expires_at,  Unset):
            expires_at = UNSET
        else:
            expires_at = datetime.datetime.fromisoformat(_expires_at)




        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsFileMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsFileMetadata.from_dict(_metadata)




        scope_session_id = d.pop("scope_session_id", UNSET)

        managed_agents_file = cls(
            byte_size=byte_size,
            created_at=created_at,
            downloadable=downloadable,
            file_id=file_id,
            filename=filename,
            media_type=media_type,
            organization_id=organization_id,
            sha256=sha256,
            source=source,
            type_=type_,
            expires_at=expires_at,
            metadata=metadata,
            scope_session_id=scope_session_id,
        )


        managed_agents_file.additional_properties = d
        return managed_agents_file

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
