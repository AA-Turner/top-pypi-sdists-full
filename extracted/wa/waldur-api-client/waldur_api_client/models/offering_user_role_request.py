from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingUserRoleRequest")


@_attrs_define
class OfferingUserRoleRequest:
    """
    Attributes:
        name (str):
        offering (str):
        scope_type (Union[Unset, str]): Level this role applies at, e.g. 'cluster', 'project'. Empty means offering-
            wide.
        scope_type_label (Union[Unset, str]): Human-readable label for scope_type shown to end users, e.g. 'Rancher
            Project', 'Cluster Namespace'. Falls back to capitalized scope_type if empty.
    """

    name: str
    offering: str
    scope_type: Union[Unset, str] = UNSET
    scope_type_label: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        offering = self.offering

        scope_type = self.scope_type

        scope_type_label = self.scope_type_label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "offering": offering,
            }
        )
        if scope_type is not UNSET:
            field_dict["scope_type"] = scope_type
        if scope_type_label is not UNSET:
            field_dict["scope_type_label"] = scope_type_label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        offering = d.pop("offering")

        scope_type = d.pop("scope_type", UNSET)

        scope_type_label = d.pop("scope_type_label", UNSET)

        offering_user_role_request = cls(
            name=name,
            offering=offering,
            scope_type=scope_type,
            scope_type_label=scope_type_label,
        )

        offering_user_role_request.additional_properties = d
        return offering_user_role_request

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
