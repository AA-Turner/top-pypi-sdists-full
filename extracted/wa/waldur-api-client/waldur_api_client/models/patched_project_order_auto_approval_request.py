from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProjectOrderAutoApprovalRequest")


@_attrs_define
class PatchedProjectOrderAutoApprovalRequest:
    """
    Attributes:
        project (Union[Unset, str]):
        monthly_cost_limit (Union[Unset, str]):
        enabled (Union[Unset, bool]):
    """

    project: Union[Unset, str] = UNSET
    monthly_cost_limit: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        monthly_cost_limit = self.monthly_cost_limit

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if project is not UNSET:
            field_dict["project"] = project
        if monthly_cost_limit is not UNSET:
            field_dict["monthly_cost_limit"] = monthly_cost_limit
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project", UNSET)

        monthly_cost_limit = d.pop("monthly_cost_limit", UNSET)

        enabled = d.pop("enabled", UNSET)

        patched_project_order_auto_approval_request = cls(
            project=project,
            monthly_cost_limit=monthly_cost_limit,
            enabled=enabled,
        )

        patched_project_order_auto_approval_request.additional_properties = d
        return patched_project_order_auto_approval_request

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
