from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MatrixTicketDraftCreateIssueRequest")


@_attrs_define
class MatrixTicketDraftCreateIssueRequest:
    """
    Attributes:
        summary (Union[Unset, str]): Replaces the draft's title.
        description (Union[Unset, str]): Replaces the draft's description.
        type_ (Union[Unset, str]): Replaces the draft's request type.
        resource_uuid (Union[None, Unset, str]): Replaces the draft's resource: one of the room's project, or blank or
            null for none.
    """

    summary: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    resource_uuid: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary = self.summary

        description = self.description

        type_ = self.type_

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = self.resource_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

        type_ = d.pop("type", UNSET)

        def _parse_resource_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid", UNSET))

        matrix_ticket_draft_create_issue_request = cls(
            summary=summary,
            description=description,
            type_=type_,
            resource_uuid=resource_uuid,
        )

        matrix_ticket_draft_create_issue_request.additional_properties = d
        return matrix_ticket_draft_create_issue_request

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
