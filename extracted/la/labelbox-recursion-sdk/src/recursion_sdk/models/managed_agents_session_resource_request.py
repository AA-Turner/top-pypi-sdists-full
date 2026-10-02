from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_resource_request_type import ManagedAgentsSessionResourceRequestType
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsSessionResourceRequest")



@_attrs_define
class ManagedAgentsSessionResourceRequest:
    """ One file to attach to a session.

        Example:
            {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'mount_path': 'example', 'relative_path': 'example', 'type':
                'file'}

        Attributes:
            file_id (UUID | Unset): The file to mount. Must belong to the caller's organization and not have expired.
            mount_path (str | Unset): The same place named absolutely, with the session's files directory as its root:
                /data/input.csv lands at data/input.csv, as does the directory's own absolute path copied from a session's
                resource list, and Claude Managed Agents' /mnt/session/uploads/ prefix is accepted as an alias for the
                directory. Any other absolute root is likewise a path beneath the directory, never a mount elsewhere. Paths take
                the same shape rules as relative_path (no . or .. segments, no control characters, at most 255 characters); the
                filename's reserved-character rule does not apply to paths. Set this or relative_path; both are accepted only
                when they agree.
            relative_path (str | Unset): Where the file lands relative to the session's files directory, e.g.
                data/input.csv. Defaults to the file's own name. Must be unique within the session and may not contain . or ..
                segments.
            type_ (ManagedAgentsSessionResourceRequestType | Unset): Always file.
     """

    file_id: UUID | Unset = UNSET
    mount_path: str | Unset = UNSET
    relative_path: str | Unset = UNSET
    type_: ManagedAgentsSessionResourceRequestType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id: str | Unset = UNSET
        if not isinstance(self.file_id, Unset):
            file_id = str(self.file_id)

        mount_path = self.mount_path

        relative_path = self.relative_path

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if file_id is not UNSET:
            field_dict["file_id"] = file_id
        if mount_path is not UNSET:
            field_dict["mount_path"] = mount_path
        if relative_path is not UNSET:
            field_dict["relative_path"] = relative_path
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _file_id = d.pop("file_id", UNSET)
        file_id: UUID | Unset
        if isinstance(_file_id,  Unset):
            file_id = UNSET
        else:
            file_id = UUID(_file_id)




        mount_path = d.pop("mount_path", UNSET)

        relative_path = d.pop("relative_path", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: ManagedAgentsSessionResourceRequestType | Unset
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = ManagedAgentsSessionResourceRequestType(_type_)




        managed_agents_session_resource_request = cls(
            file_id=file_id,
            mount_path=mount_path,
            relative_path=relative_path,
            type_=type_,
        )


        managed_agents_session_resource_request.additional_properties = d
        return managed_agents_session_resource_request

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
