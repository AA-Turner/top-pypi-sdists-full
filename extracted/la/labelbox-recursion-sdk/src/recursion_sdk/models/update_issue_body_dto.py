from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_issue_body_dto_status import UpdateIssueBodyDtoStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateIssueBodyDto")



@_attrs_define
class UpdateIssueBodyDto:
    """ Request body for partially updating an existing issue.

        Example:
            {'description': 'Updated: hairline scratches under 0.5mm should NOT be flagged as defects. Reopening so the task
                description can be revised to state this threshold explicitly.', 'status': 'open'}

        Attributes:
            description (str | Unset): New markdown body for the issue.
            status (UpdateIssueBodyDtoStatus | Unset): New lifecycle status for the issue.
     """

    description: str | Unset = UNSET
    status: UpdateIssueBodyDtoStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        description = self.description

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        _status = d.pop("status", UNSET)
        status: UpdateIssueBodyDtoStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = UpdateIssueBodyDtoStatus(_status)




        update_issue_body_dto = cls(
            description=description,
            status=status,
        )


        update_issue_body_dto.additional_properties = d
        return update_issue_body_dto

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
