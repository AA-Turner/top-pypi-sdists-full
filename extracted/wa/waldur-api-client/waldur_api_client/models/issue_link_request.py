from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.link_type_enum import LinkTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueLinkRequest")


@_attrs_define
class IssueLinkRequest:
    """
    Attributes:
        source (UUID):
        target (UUID):
        link_type (Union[Unset, LinkTypeEnum]):
    """

    source: UUID
    target: UUID
    link_type: Union[Unset, LinkTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = str(self.source)

        target = str(self.target)

        link_type: Union[Unset, str] = UNSET
        if not isinstance(self.link_type, Unset):
            link_type = self.link_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "target": target,
            }
        )
        if link_type is not UNSET:
            field_dict["link_type"] = link_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = UUID(d.pop("source"))

        target = UUID(d.pop("target"))

        _link_type = d.pop("link_type", UNSET)
        link_type: Union[Unset, LinkTypeEnum]
        if isinstance(_link_type, Unset):
            link_type = UNSET
        else:
            link_type = LinkTypeEnum(_link_type)

        issue_link_request = cls(
            source=source,
            target=target,
            link_type=link_type,
        )

        issue_link_request.additional_properties = d
        return issue_link_request

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
