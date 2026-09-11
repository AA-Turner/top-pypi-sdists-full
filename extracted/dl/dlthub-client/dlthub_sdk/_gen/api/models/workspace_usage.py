from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_member_response import WorkspaceMemberResponse
    from ..models.workspace_usage_duration_seconds_by_type import (
        WorkspaceUsageDurationSecondsByType,
    )


T = TypeVar("T", bound="WorkspaceUsage")


@_attrs_define
class WorkspaceUsage:
    """
    Attributes:
        is_playground (bool): Whether the workspace is a personal playground.
        total_duration_seconds (float): Weighted run-seconds over the reporting period; equals the sum of
            duration_seconds_by_type values.
        workspace_id (UUID): Workspace ID
        workspace_name (str): Workspace display name
        duration_seconds_by_type (WorkspaceUsageDurationSecondsByType | Unset): Weighted run-seconds keyed by job type
            (batch, interactive, stream) over the whole reporting period.
        owner (None | Unset | WorkspaceMemberResponse): Oldest active human owner of the workspace (for playgrounds,
            their sole member); null when the workspace has none.
    """

    is_playground: bool
    total_duration_seconds: float
    workspace_id: UUID
    workspace_name: str
    duration_seconds_by_type: WorkspaceUsageDurationSecondsByType | Unset = UNSET
    owner: None | Unset | WorkspaceMemberResponse = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.workspace_member_response import WorkspaceMemberResponse

        is_playground = self.is_playground

        total_duration_seconds = self.total_duration_seconds

        workspace_id = str(self.workspace_id)

        workspace_name = self.workspace_name

        duration_seconds_by_type: dict[str, Any] | Unset = UNSET
        if not isinstance(self.duration_seconds_by_type, Unset):
            duration_seconds_by_type = self.duration_seconds_by_type.to_dict()

        owner: dict[str, Any] | None | Unset
        if isinstance(self.owner, Unset):
            owner = UNSET
        elif isinstance(self.owner, WorkspaceMemberResponse):
            owner = self.owner.to_dict()
        else:
            owner = self.owner

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_playground": is_playground,
                "total_duration_seconds": total_duration_seconds,
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
            }
        )
        if duration_seconds_by_type is not UNSET:
            field_dict["duration_seconds_by_type"] = duration_seconds_by_type
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_member_response import WorkspaceMemberResponse
        from ..models.workspace_usage_duration_seconds_by_type import (
            WorkspaceUsageDurationSecondsByType,
        )

        d = dict(src_dict)
        is_playground = d.pop("is_playground")

        total_duration_seconds = d.pop("total_duration_seconds")

        workspace_id = UUID(d.pop("workspace_id"))

        workspace_name = d.pop("workspace_name")

        _duration_seconds_by_type = d.pop("duration_seconds_by_type", UNSET)
        duration_seconds_by_type: WorkspaceUsageDurationSecondsByType | Unset
        if isinstance(_duration_seconds_by_type, Unset):
            duration_seconds_by_type = UNSET
        else:
            duration_seconds_by_type = WorkspaceUsageDurationSecondsByType.from_dict(
                _duration_seconds_by_type
            )

        def _parse_owner(data: object) -> None | Unset | WorkspaceMemberResponse:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                owner_type_0 = WorkspaceMemberResponse.from_dict(data)

                return owner_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | WorkspaceMemberResponse, data)

        owner = _parse_owner(d.pop("owner", UNSET))

        workspace_usage = cls(
            is_playground=is_playground,
            total_duration_seconds=total_duration_seconds,
            workspace_id=workspace_id,
            workspace_name=workspace_name,
            duration_seconds_by_type=duration_seconds_by_type,
            owner=owner,
        )

        workspace_usage.additional_properties = d
        return workspace_usage

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
