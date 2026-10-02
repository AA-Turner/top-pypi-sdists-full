from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="CreateProblemVersionDto")



@_attrs_define
class CreateProblemVersionDto:
    """ Request body for creating a new draft problem version, optionally seeded from an existing version.

        Example:
            {'copyFromVersionId': '0c3ac467-57e1-4074-b57d-b6a7be392f71'}

        Attributes:
            copy_from_version_id (UUID | Unset): Source version to seed the new version from (scalars, rubrics, file
                attachments). Must belong to the same problem. When omitted, the server copies from the most recent locked
                version, or starts blank if none exists.
     """

    copy_from_version_id: UUID | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        copy_from_version_id: str | Unset = UNSET
        if not isinstance(self.copy_from_version_id, Unset):
            copy_from_version_id = str(self.copy_from_version_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if copy_from_version_id is not UNSET:
            field_dict["copyFromVersionId"] = copy_from_version_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _copy_from_version_id = d.pop("copyFromVersionId", UNSET)
        copy_from_version_id: UUID | Unset
        if isinstance(_copy_from_version_id,  Unset):
            copy_from_version_id = UNSET
        else:
            copy_from_version_id = UUID(_copy_from_version_id)




        create_problem_version_dto = cls(
            copy_from_version_id=copy_from_version_id,
        )


        create_problem_version_dto.additional_properties = d
        return create_problem_version_dto

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
