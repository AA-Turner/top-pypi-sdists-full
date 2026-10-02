from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleCloneRequest")


@_attrs_define
class RoleCloneRequest:
    """
    Attributes:
        customer (UUID):
        description (Union[Unset, str]):
        conceal_template (Union[Unset, bool]):  Default: True.
    """

    customer: UUID
    description: Union[Unset, str] = UNSET
    conceal_template: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer = str(self.customer)

        description = self.description

        conceal_template = self.conceal_template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer": customer,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if conceal_template is not UNSET:
            field_dict["conceal_template"] = conceal_template

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        customer = UUID(d.pop("customer"))

        description = d.pop("description", UNSET)

        conceal_template = d.pop("conceal_template", UNSET)

        role_clone_request = cls(
            customer=customer,
            description=description,
            conceal_template=conceal_template,
        )

        role_clone_request.additional_properties = d
        return role_clone_request

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
