from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


if TYPE_CHECKING:
    from ..models.usage import Usage


T = TypeVar("T", bound="UsageResource")


@_attrs_define
class UsageResource:
    """JSON:API resource envelope for the usage report.

    Example:
        {'attributes': {'active_jobs': 2, 'active_jobs_limit': 10, 'period': '2026-06', 'runs_included': 3000,
            'runs_used': 412}, 'id': 'current', 'type': 'usage'}

    Attributes:
        attributes (Usage): Current-period usage against the account's plan allotments.
        id (str | Unset):  Default: 'current'.
        type_ (str | Unset):  Default: 'usage'.
    """

    attributes: Usage
    id: str | Unset = "current"
    type_: str | Unset = "usage"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes = self.attributes.to_dict()

        id = self.id

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage import Usage

        d = dict(src_dict)
        attributes = Usage.from_dict(d.pop("attributes"))

        id = d.pop("id", UNSET)

        type_ = d.pop("type", UNSET)

        usage_resource = cls(
            attributes=attributes,
            id=id,
            type_=type_,
        )

        usage_resource.additional_properties = d
        return usage_resource

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
