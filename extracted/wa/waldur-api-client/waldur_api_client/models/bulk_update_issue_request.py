from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkUpdateIssueRequest")


@_attrs_define
class BulkUpdateIssueRequest:
    """
    Attributes:
        issue_uuids (list[UUID]): List of issue UUIDs to update.
        status (Union[Unset, str]):
        priority (Union[Unset, str]):
        assignee (Union[None, UUID, Unset]):
    """

    issue_uuids: list[UUID]
    status: Union[Unset, str] = UNSET
    priority: Union[Unset, str] = UNSET
    assignee: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        issue_uuids = []
        for issue_uuids_item_data in self.issue_uuids:
            issue_uuids_item = str(issue_uuids_item_data)
            issue_uuids.append(issue_uuids_item)

        status = self.status

        priority = self.priority

        assignee: Union[None, Unset, str]
        if isinstance(self.assignee, Unset):
            assignee = UNSET
        elif isinstance(self.assignee, UUID):
            assignee = str(self.assignee)
        else:
            assignee = self.assignee

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "issue_uuids": issue_uuids,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if assignee is not UNSET:
            field_dict["assignee"] = assignee

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        issue_uuids = []
        _issue_uuids = d.pop("issue_uuids")
        for issue_uuids_item_data in _issue_uuids:
            issue_uuids_item = UUID(issue_uuids_item_data)

            issue_uuids.append(issue_uuids_item)

        status = d.pop("status", UNSET)

        priority = d.pop("priority", UNSET)

        def _parse_assignee(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                assignee_type_0 = UUID(data)

                return assignee_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        assignee = _parse_assignee(d.pop("assignee", UNSET))

        bulk_update_issue_request = cls(
            issue_uuids=issue_uuids,
            status=status,
            priority=priority,
            assignee=assignee,
        )

        bulk_update_issue_request.additional_properties = d
        return bulk_update_issue_request

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
