from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_file import ManagedAgentsFile





T = TypeVar("T", bound="ManagedAgentsFileListResponse")



@_attrs_define
class ManagedAgentsFileListResponse:
    """ Response body of GET /v1/files.

        Example:
            {'files': [{'byte_size': 1, 'created_at': '2026-02-18T09:30:00Z', 'downloadable': True, 'expires_at':
                '2026-02-18T09:30:00Z', 'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'filename': 'example', 'media_type':
                'example', 'metadata': {'key': 'example'}, 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'scope_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sha256': 'example', 'source': 'upload', 'type':
                'file'}], 'next_page_token': 'example'}

        Attributes:
            files (list[ManagedAgentsFile] | None): Matching files in the caller's organization, newest first.
            next_page_token (str | Unset): Cursor for the next page, present only when more files follow. Pass it back as
                page_token with the same filters and limit.
     """

    files: list[ManagedAgentsFile] | None
    next_page_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_file import ManagedAgentsFile # noqa: PLC0415
        files: list[dict[str, Any]] | None
        if isinstance(self.files, list):
            files = []
            for files_type_0_item_data in self.files:
                files_type_0_item = files_type_0_item_data.to_dict()
                files.append(files_type_0_item)


        else:
            files = self.files

        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "files": files,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_file import ManagedAgentsFile # noqa: PLC0415
        d = dict(src_dict)
        def _parse_files(data: object) -> list[ManagedAgentsFile] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                files_type_0 = []
                _files_type_0 = data
                for files_type_0_item_data in (_files_type_0):
                    files_type_0_item = ManagedAgentsFile.from_dict(files_type_0_item_data)



                    files_type_0.append(files_type_0_item)

                return files_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsFile] | None, data)

        files = _parse_files(d.pop("files"))


        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_file_list_response = cls(
            files=files,
            next_page_token=next_page_token,
        )


        managed_agents_file_list_response.additional_properties = d
        return managed_agents_file_list_response

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
