from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectOrderAutoApprovalRequest")


@_attrs_define
class ProjectOrderAutoApprovalRequest:
    """
    Attributes:
        project (str):
        monthly_cost_limit (str):
        enabled (Union[Unset, bool]):
    """

    project: str
    monthly_cost_limit: str
    enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        monthly_cost_limit = self.monthly_cost_limit

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "monthly_cost_limit": monthly_cost_limit,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project")

        monthly_cost_limit = d.pop("monthly_cost_limit")

        enabled = d.pop("enabled", UNSET)

        project_order_auto_approval_request = cls(
            project=project,
            monthly_cost_limit=monthly_cost_limit,
            enabled=enabled,
        )

        project_order_auto_approval_request.additional_properties = d
        return project_order_auto_approval_request

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
