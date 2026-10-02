from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.link_type_enum import LinkTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedIssueLinkRequest")


@_attrs_define
class PatchedIssueLinkRequest:
    """
    Attributes:
        source (Union[Unset, UUID]):
        target (Union[Unset, UUID]):
        link_type (Union[Unset, LinkTypeEnum]):
    """

    source: Union[Unset, UUID] = UNSET
    target: Union[Unset, UUID] = UNSET
    link_type: Union[Unset, LinkTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = str(self.source)

        target: Union[Unset, str] = UNSET
        if not isinstance(self.target, Unset):
            target = str(self.target)

        link_type: Union[Unset, str] = UNSET
        if not isinstance(self.link_type, Unset):
            link_type = self.link_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if target is not UNSET:
            field_dict["target"] = target
        if link_type is not UNSET:
            field_dict["link_type"] = link_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _source = d.pop("source", UNSET)
        source: Union[Unset, UUID]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = UUID(_source)

        _target = d.pop("target", UNSET)
        target: Union[Unset, UUID]
        if isinstance(_target, Unset):
            target = UNSET
        else:
            target = UUID(_target)

        _link_type = d.pop("link_type", UNSET)
        link_type: Union[Unset, LinkTypeEnum]
        if isinstance(_link_type, Unset):
            link_type = UNSET
        else:
            link_type = LinkTypeEnum(_link_type)

        patched_issue_link_request = cls(
            source=source,
            target=target,
            link_type=link_type,
        )

        patched_issue_link_request.additional_properties = d
        return patched_issue_link_request

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
