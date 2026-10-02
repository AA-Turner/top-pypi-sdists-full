from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="BatchOrganizationFileMetadataRequestDto")



@_attrs_define
class BatchOrganizationFileMetadataRequestDto:
    """ Request body for a batch org-scoped file-metadata lookup. Rejects the whole batch if any id is missing or out of
    scope.

        Example:
            {'fileIds': ['e2a910d9-32c4-4ed6-8071-c7190a8c1951']}

        Attributes:
            file_ids (list[UUID]): File ids to resolve. Every id must be in the caller org scope or the request fails.
     """

    file_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_ids = []
        for file_ids_item_data in self.file_ids:
            file_ids_item = str(file_ids_item_data)
            file_ids.append(file_ids_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fileIds": file_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_ids = []
        _file_ids = d.pop("fileIds")
        for file_ids_item_data in (_file_ids):
            file_ids_item = UUID(file_ids_item_data)



            file_ids.append(file_ids_item)


        batch_organization_file_metadata_request_dto = cls(
            file_ids=file_ids,
        )


        batch_organization_file_metadata_request_dto.additional_properties = d
        return batch_organization_file_metadata_request_dto

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
