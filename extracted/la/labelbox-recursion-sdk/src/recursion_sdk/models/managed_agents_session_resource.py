from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_resource_type import ManagedAgentsSessionResourceType
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsSessionResource")



@_attrs_define
class ManagedAgentsSessionResource:
    """ A file attached to a session. The file is staged read-only into the session's sandbox under its files directory and
    the session's system prompt names the path, so the agent can read it with read_file or from a shell without being
    told where to look.

        Example:
            {'byte_size': 1, 'created_at': '2026-02-18T09:30:00Z', 'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'filename': 'example', 'media_type': 'example', 'mount_path': 'example', 'relative_path': 'example',
                'resource_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sha256': 'example', 'type': 'file'}

        Attributes:
            byte_size (int): Size of the file in bytes.
            created_at (datetime.datetime): When the resource was attached.
            file_id (str): The attached file.
            filename (str): The file's name at upload.
            media_type (str): The file's declared media type.
            relative_path (str): Where the file lands relative to the session's files directory. Defaults to the filename;
                set it on attach to rename the file or place it in a subdirectory.
            resource_id (str): Server-assigned id of the attachment, used to detach it.
            sha256 (str): SHA-256 of the bytes the session mounts. Frozen at attach: a later change to the file does not
                change this session.
            type_ (ManagedAgentsSessionResourceType): Always file.
            mount_path (str | Unset): The absolute path where the file is readable inside the sandbox. Absent until staging
                reaches the sandbox; a resource attached mid-session is staged on the next sandbox call.
     """

    byte_size: int
    created_at: datetime.datetime
    file_id: str
    filename: str
    media_type: str
    relative_path: str
    resource_id: str
    sha256: str
    type_: ManagedAgentsSessionResourceType
    mount_path: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        byte_size = self.byte_size

        created_at = self.created_at.isoformat()

        file_id = self.file_id

        filename = self.filename

        media_type = self.media_type

        relative_path = self.relative_path

        resource_id = self.resource_id

        sha256 = self.sha256

        type_ = self.type_.value

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "byte_size": byte_size,
            "created_at": created_at,
            "file_id": file_id,
            "filename": filename,
            "media_type": media_type,
            "relative_path": relative_path,
            "resource_id": resource_id,
            "sha256": sha256,
            "type": type_,
        })
        if mount_path is not UNSET:
            field_dict["mount_path"] = mount_path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        byte_size = d.pop("byte_size")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        file_id = d.pop("file_id")

        filename = d.pop("filename")

        media_type = d.pop("media_type")

        relative_path = d.pop("relative_path")

        resource_id = d.pop("resource_id")

        sha256 = d.pop("sha256")

        type_ = ManagedAgentsSessionResourceType(d.pop("type"))




        mount_path = d.pop("mount_path", UNSET)

        managed_agents_session_resource = cls(
            byte_size=byte_size,
            created_at=created_at,
            file_id=file_id,
            filename=filename,
            media_type=media_type,
            relative_path=relative_path,
            resource_id=resource_id,
            sha256=sha256,
            type_=type_,
            mount_path=mount_path,
        )


        managed_agents_session_resource.additional_properties = d
        return managed_agents_session_resource

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
