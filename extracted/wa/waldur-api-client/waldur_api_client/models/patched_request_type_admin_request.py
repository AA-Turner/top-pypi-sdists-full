from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedRequestTypeAdminRequest")


@_attrs_define
class PatchedRequestTypeAdminRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        issue_type_name (Union[Unset, str]):
        is_active (Union[Unset, bool]): Whether this request type is available for issue creation.
        order (Union[Unset, int]): Display order. First type (lowest order) is the default.
    """

    name: Union[Unset, str] = UNSET
    issue_type_name: Union[Unset, str] = UNSET
    is_active: Union[Unset, bool] = UNSET
    order: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        issue_type_name = self.issue_type_name

        is_active = self.is_active

        order = self.order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if issue_type_name is not UNSET:
            field_dict["issue_type_name"] = issue_type_name
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        issue_type_name = d.pop("issue_type_name", UNSET)

        is_active = d.pop("is_active", UNSET)

        order = d.pop("order", UNSET)

        patched_request_type_admin_request = cls(
            name=name,
            issue_type_name=issue_type_name,
            is_active=is_active,
            order=order,
        )

        patched_request_type_admin_request.additional_properties = d
        return patched_request_type_admin_request

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
