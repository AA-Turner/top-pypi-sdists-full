import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectEndDateChangeRequestCreate")


@_attrs_define
class ProjectEndDateChangeRequestCreate:
    """
    Attributes:
        project (str):
        requested_end_date (datetime.date): The requested new end date for the project
        uuid (UUID):
        state (str):
        comment (Union[None, Unset, str]): Optional comment from the requester
    """

    project: str
    requested_end_date: datetime.date
    uuid: UUID
    state: str
    comment: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        requested_end_date = self.requested_end_date.isoformat()

        uuid = str(self.uuid)

        state = self.state

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "requested_end_date": requested_end_date,
                "uuid": uuid,
                "state": state,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project")

        requested_end_date = isoparse(d.pop("requested_end_date")).date()

        uuid = UUID(d.pop("uuid"))

        state = d.pop("state")

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        project_end_date_change_request_create = cls(
            project=project,
            requested_end_date=requested_end_date,
            uuid=uuid,
            state=state,
            comment=comment,
        )

        project_end_date_change_request_create.additional_properties = d
        return project_end_date_change_request_create

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
