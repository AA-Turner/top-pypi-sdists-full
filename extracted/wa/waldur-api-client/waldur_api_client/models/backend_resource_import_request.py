from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackendResourceImportRequest")


@_attrs_define
class BackendResourceImportRequest:
    """
    Attributes:
        plan (Union[Unset, UUID]):
    """

    plan: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = str(self.plan)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, UUID]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = UUID(_plan)

        backend_resource_import_request = cls(
            plan=plan,
        )

        backend_resource_import_request.additional_properties = d
        return backend_resource_import_request

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
