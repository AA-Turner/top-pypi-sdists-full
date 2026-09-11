from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_usage import WorkspaceUsage


T = TypeVar("T", bound="OrganizationUsageByWorkspaceResponse")


@_attrs_define
class OrganizationUsageByWorkspaceResponse:
    """
    Attributes:
        period_end (datetime.datetime): datetime with the constraint that the value must have timezone info
        period_start (datetime.datetime): datetime with the constraint that the value must have timezone info
        workspaces (list[WorkspaceUsage] | Unset): Usage per workspace, zero-usage and playground workspaces included;
            ordered by workspace name.
    """

    period_end: datetime.datetime
    period_start: datetime.datetime
    workspaces: list[WorkspaceUsage] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_end = self.period_end.isoformat()

        period_start = self.period_start.isoformat()

        workspaces: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.workspaces, Unset):
            workspaces = []
            for workspaces_item_data in self.workspaces:
                workspaces_item = workspaces_item_data.to_dict()
                workspaces.append(workspaces_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period_end": period_end,
                "period_start": period_start,
            }
        )
        if workspaces is not UNSET:
            field_dict["workspaces"] = workspaces

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_usage import WorkspaceUsage

        d = dict(src_dict)
        period_end = isoparse(d.pop("period_end"))

        period_start = isoparse(d.pop("period_start"))

        _workspaces = d.pop("workspaces", UNSET)
        workspaces: list[WorkspaceUsage] | Unset = UNSET
        if _workspaces is not UNSET:
            workspaces = []
            for workspaces_item_data in _workspaces:
                workspaces_item = WorkspaceUsage.from_dict(workspaces_item_data)

                workspaces.append(workspaces_item)

        organization_usage_by_workspace_response = cls(
            period_end=period_end,
            period_start=period_start,
            workspaces=workspaces,
        )

        organization_usage_by_workspace_response.additional_properties = d
        return organization_usage_by_workspace_response

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
