from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.issue_type_enum import IssueTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.template_attachment import TemplateAttachment


T = TypeVar("T", bound="Template")


@_attrs_define
class Template:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        description (str):
        attachments (list['TemplateAttachment']):
        issue_type (Union[Unset, IssueTypeEnum]):
    """

    url: str
    uuid: UUID
    name: str
    description: str
    attachments: list["TemplateAttachment"]
    issue_type: Union[Unset, IssueTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        description = self.description

        attachments = []
        for attachments_item_data in self.attachments:
            attachments_item = attachments_item_data.to_dict()
            attachments.append(attachments_item)

        issue_type: Union[Unset, str] = UNSET
        if not isinstance(self.issue_type, Unset):
            issue_type = self.issue_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "description": description,
                "attachments": attachments,
            }
        )
        if issue_type is not UNSET:
            field_dict["issue_type"] = issue_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.template_attachment import TemplateAttachment

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        description = d.pop("description")

        attachments = []
        _attachments = d.pop("attachments")
        for attachments_item_data in _attachments:
            attachments_item = TemplateAttachment.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        _issue_type = d.pop("issue_type", UNSET)
        issue_type: Union[Unset, IssueTypeEnum]
        if isinstance(_issue_type, Unset):
            issue_type = UNSET
        else:
            issue_type = IssueTypeEnum(_issue_type)

        template = cls(
            url=url,
            uuid=uuid,
            name=name,
            description=description,
            attachments=attachments,
            issue_type=issue_type,
        )

        template.additional_properties = d
        return template

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
