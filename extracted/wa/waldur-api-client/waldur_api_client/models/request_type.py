from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestType")


@_attrs_define
class RequestType:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        issue_type_name (str):
        order (Union[Unset, int]): Display order. First type (lowest order) is the default.
    """

    url: str
    uuid: UUID
    name: str
    issue_type_name: str
    order: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        issue_type_name = self.issue_type_name

        order = self.order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "issue_type_name": issue_type_name,
            }
        )
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        issue_type_name = d.pop("issue_type_name")

        order = d.pop("order", UNSET)

        request_type = cls(
            url=url,
            uuid=uuid,
            name=name,
            issue_type_name=issue_type_name,
            order=order,
        )

        request_type.additional_properties = d
        return request_type

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
